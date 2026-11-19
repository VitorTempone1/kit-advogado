"""Tempo de contribuicao (com concomitancia) e regras de transicao da EC 103/2019 (RGPS).

O numero sai DAQUI, nunca do modelo. Python stdlib, sem rede.

  uv run calculo_previdenciario.py vinculos.csv --nascimento 10/05/1968 --sexo F [--der 01/07/2025]

CSV (virgula ou ponto e virgula, com cabecalho):
  inicio,fim,descricao
  01/03/1990,28/02/2000,Empresa A
  01/01/2012,,Empresa C          <- fim vazio = ativo ate a DER

Nao calcula RMI (valor do beneficio) nem converte tempo especial (v1).
"""

import argparse
import calendar
import csv
import sys
from datetime import date, timedelta

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RODAPE = "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."
EC103 = date(2019, 11, 13)
ANO = 365  # convencao de conversao: ano = 365 dias, mes = 30 dias
HORIZONTE = 45 * 366


def d(s):
    dia, mes, ano = (int(x) for x in s.strip().split("/"))
    return date(ano, mes, dia)


def fmt(dt):
    return dt.strftime("%d/%m/%Y")


def somar_meses(dt, n):
    m = dt.month - 1 + n
    a, mm = dt.year + m // 12, m % 12 + 1
    return date(a, mm, min(dt.day, calendar.monthrange(a, mm)[1]))


def amd(dias):
    a, r = divmod(int(dias), ANO)
    m, dd = divmod(r, 30)
    return "%d anos, %d meses e %d dias" % (a, m, dd)


def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig") as f:
        texto = f.read().splitlines()
    delim = ";" if texto[0].count(";") > texto[0].count(",") else ","
    out = []
    for i, r in enumerate(csv.DictReader(texto, delimiter=delim), start=2):
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
        if not r.get("inicio"):
            continue
        try:
            out.append((d(r["inicio"]), d(r["fim"]) if r.get("fim") else None, r.get("descricao", "") or "vínculo %d" % (i - 1)))
        except Exception as e:
            raise SystemExit("Linha %d do CSV ilegivel (%s): %r" % (i, e, r))
    return out


def uniao(vinculos, ate):
    """Intervalos [ini, fim] inclusivos, cortados em `ate`, sem sobreposicao."""
    iv = sorted((i, min(f or ate, ate)) for i, f, _ in vinculos if i <= ate)
    out = []
    for i, f in iv:
        if f < i:
            continue
        if out and i <= out[-1][1] + timedelta(days=1):
            out[-1][1] = max(out[-1][1], f)
        else:
            out.append([i, f])
    return out


def dias(iv):
    return sum((f - i).days + 1 for i, f in iv)


def carencia(iv):
    """Meses civis com ao menos um dia de vinculo."""
    meses = set()
    for i, f in iv:
        a, m = i.year, i.month
        while (a, m) <= (f.year, f.month):
            meses.add((a, m))
            a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return len(meses)


def concomitancias(vinculos, ate):
    out = []
    v = [(i, min(f or ate, ate), n) for i, f, n in vinculos]
    for x in range(len(v)):
        for y in range(x + 1, len(v)):
            ini, fim = max(v[x][0], v[y][0]), min(v[x][1], v[y][1])
            if fim >= ini:
                out.append((v[x][2], v[y][2], ini, fim, (fim - ini).days + 1))
    return out


def idade_em(nasc, dt):
    """Idade em anos com fracao (dias desde o ultimo aniversario / 365)."""
    a = dt.year - nasc.year - ((dt.month, dt.day) < (nasc.month, nasc.day))
    ult = somar_meses(nasc, 12 * a)
    return a + (dt - ult).days / ANO


def fez_idade(nasc, dt, anos):
    """anos pode ter meio ano (61.5)."""
    return dt >= somar_meses(nasc, int(round(anos * 12)))


def regras(sexo, tc2019):
    """Cada regra: (nome, fonte, funcao(dt, tc_dias, carencia) -> bool, aplicavel, motivo)."""
    H = sexo == "M"
    req = (35 if H else 30) * ANO

    def pts(y):
        return min(96 + max(0, y - 2019), 105) if H else min(86 + max(0, y - 2019), 100)

    def idprog(y):
        return min(61 + 0.5 * max(0, y - 2019), 65) if H else min(56 + 0.5 * max(0, y - 2019), 62)

    def idade18(y):
        return 65 if H else min(60 + 0.5 * max(0, y - 2019), 62)

    falta = max(0, req - tc2019)
    ped50_ok = tc2019 > (33 if H else 28) * ANO
    return [
        ("Pontos (art. 15)", "EC 103/2019, art. 15: %s anos de TC + idade + TC >= %s pontos (+1/ano desde 2020, teto %s)"
         % ((35, 96, 105) if H else (30, 86, 100)),
         lambda dt, tc, car, nasc: tc >= req and idade_em(nasc, dt) + tc / ANO >= pts(dt.year), True, ""),
        ("Idade progressiva (art. 16)", "EC 103/2019, art. 16: %s anos de TC + idade mínima %s em 2019 (+6 meses/ano, teto %s)"
         % ((35, 61, 65) if H else (30, 56, 62)),
         lambda dt, tc, car, nasc: tc >= req and fez_idade(nasc, dt, idprog(dt.year)), True, ""),
        ("Pedágio de 50% (art. 17)", "EC 103/2019, art. 17: só para quem tinha mais de %d anos de TC em 13/11/2019; "
         "TC mínimo + 50%% do que faltava (%d dias); sem idade mínima; com fator previdenciário" % (33 if H else 28, falta / 2),
         lambda dt, tc, car, nasc: tc >= req + falta / 2, ped50_ok,
         "em 13/11/2019 tinha %s, não passava de %d anos" % (amd(tc2019), 33 if H else 28)),
        ("Pedágio de 100% (art. 20)", "EC 103/2019, art. 20: idade %d + TC mínimo + 100%% do que faltava em 13/11/2019 (%d dias)"
         % (60 if H else 57, falta),
         lambda dt, tc, car, nasc: tc >= req + falta and fez_idade(nasc, dt, 60 if H else 57), True, ""),
        ("Aposentadoria por idade (art. 18)", "EC 103/2019, art. 18: idade %s + 15 anos de TC + 180 meses de carência"
         % ("65" if H else "60 em 2019 (+6 meses/ano até 62 em 2023)"),
         lambda dt, tc, car, nasc: tc >= 15 * ANO and car >= 180 and fez_idade(nasc, dt, idade18(dt.year)), True, ""),
    ]


def primeira_data(regra, nasc, der, tc_der, car_der):
    """Primeira data >= DER em que cumpre, supondo contribuicao ininterrupta depois da DER."""
    for k in range(HORIZONTE):
        dt = der + timedelta(days=k)
        car = car_der + (dt.year - der.year) * 12 + dt.month - der.month
        if regra(dt, tc_der + k, car, nasc):
            return dt
    return None


def calcular(vinculos, nasc, sexo, der):
    iv = uniao(vinculos, der)
    tc = dias(iv)
    iv19 = uniao(vinculos, EC103)
    tc19 = dias(iv19)
    car = carencia(iv)
    filiado_antes = any(i <= EC103 for i, _, _ in vinculos)
    res = {"intervalos": iv, "tc": tc, "tc2019": tc19, "carencia": car, "carencia2019": carencia(iv19),
           "concomitancias": concomitancias(vinculos, der), "filiado_antes": filiado_antes,
           "idade_der": idade_em(nasc, der), "regras": [], "adquirido": []}
    H = sexo == "M"
    if tc19 >= (35 if H else 30) * ANO:
        res["adquirido"].append("Aposentadoria por tempo de contribuição pela regra anterior (TC em 13/11/2019: %s)" % amd(tc19))
    if fez_idade(nasc, EC103, 65 if H else 60) and res["carencia2019"] >= 180:
        res["adquirido"].append("Aposentadoria por idade pela regra anterior (idade e 180 meses de carência em 13/11/2019)")
    for nome, fonte, f, aplicavel, motivo in regras(sexo, tc19):
        if not filiado_antes:
            res["regras"].append((nome, fonte, "não se aplica", "filiação depois de 13/11/2019", None))
        elif not aplicavel:
            res["regras"].append((nome, fonte, "não se aplica", motivo, None))
        else:
            dt = primeira_data(f, nasc, der, tc, car)
            if dt == der:
                res["regras"].append((nome, fonte, "JÁ CUMPRE", "na DER %s" % fmt(der), dt))
            elif dt:
                res["regras"].append((nome, fonte, "cumpre em %s" % fmt(dt), "se contribuir sem parar desde a DER", dt))
            else:
                res["regras"].append((nome, fonte, "não cumpre em 45 anos", "", None))
    return res


def relatorio(caminho, vinculos, nasc, sexo, der, r):
    o = ["# Memória de cálculo — tempo de contribuição e regras de transição", "",
         "MINUTA. Não é peça. Conferir antes de usar.", "",
         "- Segurado(a): %s, nascimento %s, idade na DER %.2f anos" % ("homem" if sexo == "M" else "mulher", fmt(nasc), r["idade_der"]),
         "- DER (data de referência): %s · vínculos lidos de `%s`" % (fmt(der), caminho), "",
         "## Vínculos informados", "", "| # | Início | Fim | Descrição | Dias |", "|---|---|---|---|---:|"]
    for n, (i, f, desc) in enumerate(vinculos, 1):
        ff = min(f or der, der)
        o.append("| %d | %s | %s | %s | %d |" % (n, fmt(i), fmt(ff) + ("" if f else " (ativo)"), desc, max(0, (ff - i).days + 1)))
    o += ["", "## Concomitância (tempo contado UMA vez só)", ""]
    if r["concomitancias"]:
        o += ["| Vínculo | Vínculo | Período em comum | Dias descontados |", "|---|---|---|---:|"]
        o += ["| %s | %s | %s a %s | %d |" % (a, b, fmt(i), fmt(f), n) for a, b, i, f, n in r["concomitancias"]]
        o.append("\nNa concomitância somam-se os salários de contribuição, não o tempo (Lei 8.213/91, art. 32).")
    else:
        o.append("Nenhuma.")
    o += ["", "## Tempo apurado", "", "| Item | Dias | Em anos, meses e dias |", "|---|---:|---|",
          "| Tempo de contribuição na DER | %d | %s |" % (r["tc"], amd(r["tc"])),
          "| Tempo de contribuição em 13/11/2019 (EC 103) | %d | %s |" % (r["tc2019"], amd(r["tc2019"])),
          "| Carência na DER (meses com contribuição) | %d meses | |" % r["carencia"],
          "", "Períodos efetivamente contados: " + "; ".join("%s a %s" % (fmt(i), fmt(f)) for i, f in r["intervalos"]),
          "", "## Direito adquirido até 13/11/2019", ""]
    o += ["- " + x for x in r["adquirido"]] or ["Nenhum pela regra anterior."]
    o += ["", "## Regras de transição da EC 103/2019", "", "| Regra | Situação | Observação |", "|---|---|---|"]
    o += ["| %s | **%s** | %s |" % (n, s, obs) for n, _, s, obs, _ in r["regras"]]
    o += ["", "Requisitos de cada regra:", ""] + ["- %s — %s" % (n, f) for n, f, _, _, _ in r["regras"]]
    o += ["", "## Como foi contado", "",
          "- Cada período conta do primeiro ao último dia, inclusive; períodos sobrepostos contam uma vez.",
          "- Conversão: ano = 365 dias, mês = 30 dias. Pontos = idade + TC, com frações. [conferir com o CNIS/INSS]",
          "- Carência: mês civil com ao menos um dia de vínculo. [conferir: contribuinte individual só conta "
          "competência paga em dia; vínculo abaixo do mínimo pode não contar (EC 103, art. 29)]",
          "- \"Cumpre em\" supõe que a pessoa continue contribuindo sem interrupção desde a DER.",
          "- Não considerei tempo especial, rural, de professor, de serviço militar, nem períodos de benefício "
          "por incapacidade intercalados. Não calculei RMI (valor do benefício).",
          "", RODAPE]
    return "\n".join(o)


def main():
    p = argparse.ArgumentParser(description="Tempo de contribuicao e transicao EC 103")
    p.add_argument("csv")
    p.add_argument("--nascimento", required=True)
    p.add_argument("--sexo", required=True, choices=("M", "F"))
    p.add_argument("--der", default=None, help="dd/mm/aaaa (padrao: hoje)")
    a = p.parse_args()
    der = d(a.der) if a.der else date.today()
    vinculos = ler_csv(a.csv)
    if not vinculos:
        raise SystemExit("CSV sem vinculos")
    for i, f, n in vinculos:
        if f and f < i:
            raise SystemExit("Vinculo '%s' termina antes de comecar" % n)
    r = calcular(vinculos, d(a.nascimento), a.sexo, der)
    print(relatorio(a.csv, vinculos, d(a.nascimento), a.sexo, der, r))


if __name__ == "__main__":
    main()
