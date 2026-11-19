"""Preparo do PJe-Calc: roteiro de lancamento e conferencia do relatorio.

NAO roda o PJe-Calc. O modelo le a sentenca e preenche um JSON de parametros
(cada item com a pagina de onde saiu); este script, sem modelo nenhum:

  roteiro   parametros.json              -> checklist tela a tela do PJe-Calc,
                                            prescricao quinquenal e bienal calculadas,
                                            e o que a decisao NAO disse
  conferir  parametros.json relatorio.txt -> procura cada parametro no texto do
                                            relatorio exportado do PJe-Calc

  uv run pjecalc_preparo.py roteiro parametros.json
  uv run pjecalc_preparo.py conferir parametros.json relatorio.txt

Python stdlib, sem rede.
"""

import calendar
import json
import re
import sys
import unicodedata
from datetime import date

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RODAPE = "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."
FALTA = "**NÃO CONSTA NA DECISÃO** — conferir; se for omissão, avaliar embargos de declaração"
INDICES = ["ipca-e", "ipca", "selic", "tr", "taxa legal", "inpc"]


def d(s):
    dia, mes, ano = (int(x) for x in s.strip().split("/"))
    return date(ano, mes, dia)


def fmt(dt):
    return dt.strftime("%d/%m/%Y")


def menos_anos(dt, n):
    a = dt.year - n
    return date(a, dt.month, min(dt.day, calendar.monthrange(a, dt.month)[1]))


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[ \t]+", " ", s)


def campo(p, k):
    """(valor, fonte) de um campo que pode ser texto ou {"valor":..., "fonte":...}."""
    v = p.get(k)
    if v in (None, "", [], {}):
        return None, None
    if isinstance(v, dict) and "valor" in v:
        return v.get("valor"), v.get("fonte")
    return v, None


def mostra(p, k):
    v, f = campo(p, k)
    if v is None:
        return FALTA
    return "%s%s" % (v, " (%s)" % f if f else " (**sem página** — localizar na decisão)")


def prazos(p):
    """Prescricao quinquenal e bienal (art. 7o, XXIX, CF; Sumula 308 TST)."""
    out = []
    aj, _ = campo(p, "ajuizamento")
    dem, _ = campo(p, "demissao")
    adm, _ = campo(p, "admissao")
    if not aj:
        return ["- Sem data de ajuizamento: não dá para calcular a prescrição. " + FALTA]
    aj = d(aj)
    lim = menos_anos(aj, 5)
    out.append("- Prescrição quinquenal: ajuizamento %s - 5 anos = **%s**. Parcelas anteriores a essa data ficam de "
               "fora se a prescrição foi acolhida (Súmula 308, I, TST)." % (fmt(aj), fmt(lim)))
    if adm and d(adm) >= lim:
        out.append("  - Admissão (%s) é posterior ao marco: a prescrição quinquenal não corta nada." % adm)
    pq, fq = campo(p, "prescricao_quinquenal")
    out.append("  - A decisão %s" % ("acolheu a prescrição quinquenal (%s): marque no PJe-Calc e use %s como data inicial."
                                  % (fq or "sem página", fmt(lim)) if pq is True else
                                  "rejeitou ou não aplicou a prescrição quinquenal." if pq is False else
                                  "não diz se acolheu a prescrição quinquenal. " + FALTA))
    if dem:
        bienal = menos_anos(aj, 2)
        if d(dem) < bienal:
            out.append("- **Atenção, bienal:** demissão %s é anterior a %s (ajuizamento - 2 anos). Confira a projeção do "
                       "aviso (OJ 83 SDI-1) antes de concluir que prescreveu." % (dem, fmt(bienal)))
        else:
            out.append("- Prescrição bienal: ajuizada dentro de 2 anos da demissão (%s)." % dem)
    return out


def roteiro(p):
    o = ["# Roteiro de lançamento no PJe-Calc", "", "MINUTA. Não é cálculo. É o checklist para lançar a decisão no PJe-Calc "
         "(menus da versão Cidadão; [conferir na sua versão]).", "",
         "Processo: %s" % mostra(p, "processo"), "",
         "## 1. Dados do Cálculo", "",
         "- [ ] Reclamante: %s" % mostra(p, "reclamante"),
         "- [ ] Reclamada: %s" % mostra(p, "reclamada"),
         "- [ ] Admissão: %s" % mostra(p, "admissao"),
         "- [ ] Demissão: %s" % mostra(p, "demissao"),
         "- [ ] Ajuizamento: %s" % mostra(p, "ajuizamento"),
         "- [ ] Carga horária / divisor: %s" % mostra(p, "carga_horaria"),
         "- [ ] Maior / última remuneração: %s" % mostra(p, "salario"), ""]
    o += prazos(p)
    o += ["", "## 2. Histórico Salarial", "", "- [ ] Base: %s" % mostra(p, "salario"),
          "- [ ] Evolução salarial: lançar mês a mês pelos contracheques/fichas financeiras, se houve reajuste.", "",
          "## 3. Faltas e Férias", "", "- [ ] %s" % mostra(p, "faltas_ferias"), "", "## 4. Verbas", ""]
    verbas = p.get("verbas") or []
    if not verbas:
        o.append("- [ ] Nenhuma verba no JSON. " + FALTA)
    tem_he = False
    for i, v in enumerate(verbas, 1):
        nome = v.get("nome", "?")
        tem_he = tem_he or "extra" in norm(nome)
        o += ["- [ ] **4.%d %s** — %s" % (i, nome, v.get("fonte") or "**sem página**"),
              "  - Período: %s" % (v.get("periodo") or FALTA),
              "  - Parâmetros (adicional, base, quantidade): %s" % (v.get("parametros") or FALTA),
              "  - Reflexos: %s" % (", ".join(v["reflexos"]) if v.get("reflexos") else
                                     "nenhum reflexo na decisão — confirmar se é isso mesmo")]
    if tem_he:
        o += ["", "## 5. Cartão de Ponto", "", "- [ ] Jornada fixada: %s" % mostra(p, "jornada"),
              "- [ ] Feriados, domingos, intervalo e critério de apuração (diário/semanal) conforme a decisão."]
    o += ["", "## 6. FGTS", "", "- [ ] %s" % mostra(p, "fgts"),
          "", "## 7. Contribuição Social (INSS)", "", "- [ ] %s" % mostra(p, "inss"),
          "", "## 8. Imposto de Renda", "", "- [ ] %s" % mostra(p, "ir"),
          "", "## 9. Honorários", "", "- [ ] %s" % mostra(p, "honorarios"),
          "", "## 10. Custas Judiciais", "", "- [ ] %s" % mostra(p, "custas"),
          "", "## 11. Correção, Juros e Multa", "", "- [ ] Correção: %s" % mostra(p, "correcao"),
          "- [ ] Juros: %s" % mostra(p, "juros"),
          "- [ ] Se a decisão é de antes de 30/08/2024 e não tratou da Lei 14.905/2024: o TST (SDI-1, "
          "E-ED-RR-713-03.2010.5.04.0029) manda IPCA + taxa legal a partir de 30/08/2024. Conferir a versão do PJe-Calc.",
          "", "## 12. Liquidar e exportar", "",
          "- [ ] Operações > Liquidar; resolver todo alerta antes de imprimir.",
          "- [ ] Imprimir o relatório completo em PDF e rodar a conferência desta skill contra ele.", ""]
    faltas = [k for k in ("admissao", "demissao", "ajuizamento", "salario", "correcao", "juros", "fgts", "inss", "ir",
                          "honorarios", "custas") if campo(p, k)[0] is None]
    o += ["## O que a decisão não disse", ""]
    o += ["- %s" % k for k in faltas] or ["Nada dos campos principais ficou em branco."]
    o += ["", RODAPE]
    return "\n".join(o)


def conferir(p, texto):
    t = norm(texto)
    linhas = t.splitlines()
    res = []

    def achou(rotulo, esperado, ok, onde=""):
        res.append((rotulo, esperado, "ok" if ok else "**NÃO ACHEI no relatório**", onde))

    for k, r in (("admissao", "Admissão"), ("demissao", "Demissão"), ("ajuizamento", "Ajuizamento")):
        v, _ = campo(p, k)
        if v:
            achou(r, v, v in t)
    pq, _ = campo(p, "prescricao_quinquenal")
    aj, _ = campo(p, "ajuizamento")
    if pq is True and aj:
        lim = fmt(menos_anos(d(aj), 5))
        achou("Prescrição quinquenal (marco)", lim, lim in t)
    for v in p.get("verbas") or []:
        palavras = [w for w in re.findall(r"[a-z0-9%]+", norm(v.get("nome", ""))) if len(w) > 3 or "%" in w]
        hit = next((ln.strip() for ln in linhas if palavras and all(w in ln for w in palavras)), "")
        achou("Verba", v.get("nome"), bool(hit), hit[:80])
        for rf in v.get("reflexos") or []:
            tok = re.findall(r"[a-z0-9]+", norm(rf))
            if not tok or tok[0] == "fgts":  # FGTS tem item proprio abaixo
                continue
            hit = next((ln.strip() for ln in linhas if tok[0] in ln and
                        ("reflex" in ln or any(w in ln for w in palavras))), "")
            achou("Reflexo de %s" % v.get("nome"), rf, bool(hit), hit[:80])
    for k in ("correcao", "juros"):
        v, _ = campo(p, k)
        if v:
            nv = norm(v)
            for idx in INDICES:
                if re.search(r"(?<![a-z-])%s(?![a-z-])" % re.escape(idx), nv):
                    achou("Índice (%s)" % k, idx.upper(), bool(re.search(r"(?<![a-z-])%s(?![a-z-])" % re.escape(idx), t)))
    v, _ = campo(p, "fgts")
    m = re.search(r"(\d+)\s*%", norm(v or ""))
    if m:
        hit = next((ln.strip() for ln in linhas if "multa" in ln and re.search(r"(?<!\d)%s\s*%%" % m.group(1), ln)), "")
        achou("Multa do FGTS", m.group(0), bool(hit), hit[:80])
    v, _ = campo(p, "honorarios")
    m = re.search(r"(\d+)\s*%", norm(v or ""))
    if m:
        hit = next((ln.strip() for ln in linhas if "honor" in ln and re.search(r"(?<!\d)%s\s*%%" % m.group(1), ln)), "")
        achou("Honorários", m.group(0), bool(hit), hit[:80])
    return res


def relatorio_conferencia(res):
    div = [r for r in res if r[2] != "ok"]
    o = ["# Conferência do relatório do PJe-Calc contra a decisão", "",
         "MINUTA. %d itens procurados, %d não achados." % (len(res), len(div)), "",
         "| Item | Na decisão | No relatório | Trecho |", "|---|---|---|---|"]
    o += ["| %s | %s | %s | %s |" % r for r in res]
    o += ["", "\"Não achei\" quer dizer: o texto não aparece no relatório como a decisão diz. Pode ser divergência "
          "de verdade (verba esquecida, índice trocado) ou só outra forma de escrever. Abra o PDF e confira cada um.",
          "A conferência é de PRESENÇA de parâmetros, não refaz a conta do PJe-Calc.", "", RODAPE]
    return "\n".join(o)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("roteiro", "conferir") or (sys.argv[1] == "conferir" and len(sys.argv) < 4):
        raise SystemExit(__doc__)
    with open(sys.argv[2], encoding="utf-8") as f:
        p = json.load(f)
    if sys.argv[1] == "roteiro":
        print(roteiro(p))
    else:
        with open(sys.argv[3], encoding="utf-8", errors="replace") as f:
            print(relatorio_conferencia(conferir(p, f.read())))


if __name__ == "__main__":
    main()
