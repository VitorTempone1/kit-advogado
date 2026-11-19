"""Horas extras a partir da jornada (CSV), com reflexos e memoria de calculo.

O numero sai DAQUI, nunca do modelo. Python stdlib, sem rede.

  uv run calculo_horas_extras.py jornada.csv --salario 2200 [--jornada-semanal 44]
      [--jornada-diaria 8] [--divisor 220] [--feriados 29/03/2024,30/05/2024] [--multa-fgts 40]

CSV (virgula ou ponto e virgula, com cabecalho):
  data,entrada,saida,intervalo
  03/06/2024,08:00,18:00,60        <- intervalo em minutos ou HH:MM
Saida menor que entrada = virou a meia-noite.
"""

import argparse
import calendar
import csv
import sys
from collections import OrderedDict
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RODAPE = "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."
C = Decimal("0.01")
TOLERANCIA = 10  # min/dia, art. 58, par. 1o, CLT
VIRADA_OJ394 = date(2023, 3, 20)  # OJ 394 SDI-1, item II (redacao de 2023)


def q(v):
    return Decimal(v).quantize(C, ROUND_HALF_UP)


def brl(v):
    v = q(v)
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-R$ " if v < 0 else "R$ ") + s


def hhmm(minutos):
    return "%dh%02d" % divmod(int(minutos), 60)


def d(s):
    dia, mes, ano = (int(x) for x in s.strip().split("/"))
    return date(ano, mes, dia)


def minutos(s):
    s = s.strip()
    if not s:
        return 0
    if ":" in s:
        h, m = s.split(":")[:2]
        return int(h) * 60 + int(m)
    return int(s)


def feriados_nacionais(ano):
    """Feriados nacionais FIXOS por lei federal (Lei 662/49, 6.802/80, 14.759/23).
    Sexta-feira Santa, Corpus Christi e feriados locais vem por --feriados."""
    fs = {(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (12, 25)}
    if ano >= 2024:
        fs.add((11, 20))
    return {date(ano, m, dd) for m, dd in fs}


def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig") as f:
        texto = f.read()
    delim = ";" if texto.splitlines()[0].count(";") > texto.splitlines()[0].count(",") else ","
    linhas = []
    for i, r in enumerate(csv.DictReader(texto.splitlines(), delimiter=delim), start=2):
        r = {k.strip().lower(): (v or "") for k, v in r.items() if k}
        try:
            linhas.append((d(r["data"]), minutos(r["entrada"]), minutos(r["saida"]),
                           minutos(r.get("intervalo", ""))))
        except Exception as e:
            raise SystemExit("Linha %d do CSV ilegivel (%s): %r" % (i, e, r))
    return linhas


def calcular(dias, salario, jornada_diaria_h=8, jornada_semanal_h=44, divisor=None,
             feriados_extra=(), multa_fgts=0):
    """dias: [(date, entrada_min, saida_min, intervalo_min)]. Devolve (meses, dias_detalhe, params)."""
    salario = Decimal(str(salario))
    divisor = Decimal(divisor or int(jornada_semanal_h * 5))
    vh = salario / divisor
    jd, js = int(jornada_diaria_h * 60), int(jornada_semanal_h * 60)
    anos = {x[0].year for x in dias}
    feriados = set(feriados_extra)
    for a in anos:
        feriados |= feriados_nacionais(a)

    detalhe, semanas = [], OrderedDict()
    for dt, ent, sai, intv in sorted(dias):
        bruto = (sai - ent) % (24 * 60) - intv
        if bruto < 0:
            raise SystemExit("%s: intervalo maior que a jornada" % dt.strftime("%d/%m/%Y"))
        rec = {"data": dt, "trab": bruto, "he50": 0, "he100": 0, "obs": ""}
        if dt.weekday() == 6 or dt in feriados:
            rec["he100"] = bruto
            rec["obs"] = "domingo" if dt.weekday() == 6 else "feriado"
        else:
            exc = max(0, bruto - jd)
            if 0 < exc <= TOLERANCIA:
                rec["obs"] = "%d min tolerados (art. 58, par. 1o)" % exc
                exc = 0
            rec["he50"] = exc
            semanas.setdefault(dt - timedelta(days=dt.weekday()), []).append(rec)
        detalhe.append(rec)

    # excedente semanal que a apuracao diaria nao pegou
    for seg, recs in semanas.items():
        normal = sum(min(r["trab"], jd) for r in recs)
        exc_sem = max(0, normal - js)
        if exc_sem:
            recs[-1]["he50"] += exc_sem
            recs[-1]["obs"] = (recs[-1]["obs"] + "; " if recs[-1]["obs"] else "") + \
                "+%s excedente da semana (%s normais > %s)" % (hhmm(exc_sem), hhmm(normal), hhmm(js))

    meses = OrderedDict()
    for r in detalhe:
        k = (r["data"].year, r["data"].month)
        m = meses.setdefault(k, {"he50": 0, "he100": 0, "v": Decimal(0), "v_pos": Decimal(0)})
        v = Decimal(r["he50"]) / 60 * vh * Decimal("1.5") + Decimal(r["he100"]) / 60 * vh * 2
        m["he50"] += r["he50"]
        m["he100"] += r["he100"]
        m["v"] += v
        if r["data"] >= VIRADA_OJ394:
            m["v_pos"] += v

    for (ano, mes), m in meses.items():
        ndias = calendar.monthrange(ano, mes)[1]
        repouso = sum(1 for i in range(1, ndias + 1)
                      if date(ano, mes, i).weekday() == 6 or date(ano, mes, i) in feriados)
        m["uteis"], m["repouso"] = ndias - repouso, repouso
        m["v50"] = q(Decimal(m["he50"]) / 60 * vh * Decimal("1.5"))
        m["v100"] = q(Decimal(m["he100"]) / 60 * vh * 2)
        m["he"] = m["v50"] + m["v100"]
        m["dsr"] = q(m["he"] / m["uteis"] * repouso)
        frac = (m["v_pos"] / m["v"]) if m["v"] else Decimal(0)
        m["dsr_refl"] = q(m["dsr"] * frac)
        base = m["he"] + m["dsr_refl"]
        m["d13"] = q(base / 12)
        m["ferias"] = q(base / 12 * 4 / 3)
        m["fgts"] = q((m["he"] + m["dsr_refl"] + m["d13"]) * Decimal("0.08"))
        m["multa"] = q(m["fgts"] * Decimal(multa_fgts) / 100)
    params = {"salario": salario, "divisor": divisor, "vh": vh, "jd": jd, "js": js,
              "feriados": sorted(f for f in feriados if f.year in anos), "multa": multa_fgts}
    return meses, detalhe, params


def relatorio(caminho, meses, detalhe, p):
    tot = {k: sum(m[k] for m in meses.values())
           for k in ("he50", "he100", "v50", "v100", "dsr", "dsr_refl", "d13", "ferias", "fgts", "multa")}
    total = tot["v50"] + tot["v100"] + tot["dsr"] + tot["d13"] + tot["ferias"] + tot["fgts"] + tot["multa"]
    o = ["# Memória de cálculo — horas extras", "", "MINUTA. Não é peça. Conferir antes de usar.", "",
         "- Jornada lida de: `%s` (%d dias, %s a %s)" % (caminho, len(detalhe),
                                                        detalhe[0]["data"].strftime("%d/%m/%Y"),
                                                        detalhe[-1]["data"].strftime("%d/%m/%Y")),
         "- Salário: %s · Divisor: %s · Valor da hora: %s / %s = R$ %s" % (
             brl(p["salario"]), p["divisor"], brl(p["salario"]), p["divisor"],
             str(p["vh"].quantize(Decimal("0.0001"))).replace(".", ",")),
         "- Jornada contratual: %s/dia e %s/semana" % (hhmm(p["jd"]), hhmm(p["js"])),
         "- Feriados considerados: %s" % (", ".join(f.strftime("%d/%m/%Y") for f in p["feriados"]) or "nenhum"),
         "", "## Por mês", "",
         "| Mês | HE 50% | Valor 50% | HE 100% | Valor 100% | DSR (úteis/repouso) | Reflexo 13º | Reflexo férias+1/3 | FGTS 8% |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for (ano, mes), m in meses.items():
        o.append("| %02d/%d | %s | %s | %s | %s | %s (%d/%d) | %s | %s | %s |" % (
            mes, ano, hhmm(m["he50"]), brl(m["v50"]), hhmm(m["he100"]), brl(m["v100"]),
            brl(m["dsr"]), m["uteis"], m["repouso"], brl(m["d13"]), brl(m["ferias"]), brl(m["fgts"])))
    o += ["", "## Totais", "", "| Item | Valor |", "|---|---:|",
          "| Horas extras 50%% (%s) | %s |" % (hhmm(tot["he50"]), brl(tot["v50"])),
          "| Horas extras 100%% (%s) | %s |" % (hhmm(tot["he100"]), brl(tot["v100"])),
          "| Reflexo em DSR | %s |" % brl(tot["dsr"]),
          "| Reflexo em 13º | %s |" % brl(tot["d13"]),
          "| Reflexo em férias + 1/3 | %s |" % brl(tot["ferias"]),
          "| FGTS 8%% (HE + DSR que reflete + 13º) | %s |" % brl(tot["fgts"])]
    if p["multa"]:
        o.append("| Multa de %s%% sobre esse FGTS | %s |" % (p["multa"], brl(tot["multa"])))
    o += ["| **Total (sem correção e juros)** | **%s** |" % brl(total), "", "## Como cada linha foi feita", "",
          "- Hora trabalhada = saída - entrada - intervalo. Excedente da jornada diária = HE 50%%. "
          "Excedente de até %d min no dia é desprezado; acima disso, conta inteiro "
          "(art. 58, §1º, CLT; Súmula 366 TST)." % TOLERANCIA,
          "- Semana (segunda a domingo): as horas normais que passam da jornada semanal viram HE 50%, "
          "lançadas no último dia trabalhado da semana (art. 7º, XIII, CF).",
          "- Domingo e feriado trabalhados: todas as horas a 100%, supondo que não houve folga compensatória "
          "(Lei 605/49, art. 9º; Súmula 146 TST). [conferir: se houve folga, não é 100%]",
          "- DSR: valor das HE do mês / dias úteis do mês x domingos e feriados do mês (Súmula 172 TST; "
          "Lei 605/49, art. 7º). Sábado conta como dia útil.",
          "- DSR nos demais reflexos: só a parte das HE feitas a partir de 20/03/2023 "
          "(OJ 394 SDI-1, redação de 2023, item II). Antes disso, o DSR não repercute (redação antiga).",
          "- 13º e férias + 1/3: 1/12 do valor mensal (HE + DSR que reflete) por mês. "
          "[conferir: aproximação; o PJeCalc apura pela média do período aquisitivo/ano, Súmula 347 TST]",
          "- FGTS: 8% sobre HE, DSR que reflete e reflexo em 13º (Súmula 63 TST). Férias indenizadas não "
          "(OJ 195 SDI-1). [conferir: férias gozadas no curso do contrato têm FGTS]",
          "", "## Dia a dia", "", "| Data | Trabalhado | HE 50% | HE 100% | Obs. |", "|---|---:|---:|---:|---|"]
    for r in detalhe:
        o.append("| %s | %s | %s | %s | %s |" % (r["data"].strftime("%d/%m/%Y %a"), hhmm(r["trab"]),
                                              hhmm(r["he50"]), hhmm(r["he100"]), r["obs"]))
    o += ["", "Não calculei: adicional noturno, intervalo intrajornada suprimido (art. 71, §4º), "
          "reflexo em aviso prévio, INSS, IR, correção e juros.", "", RODAPE]
    return "\n".join(o)


def main():
    p = argparse.ArgumentParser(description="Horas extras com reflexos")
    p.add_argument("csv")
    p.add_argument("--salario", required=True, type=Decimal)
    p.add_argument("--jornada-diaria", type=float, default=8, help="horas (padrao 8)")
    p.add_argument("--jornada-semanal", type=float, default=44, help="horas (padrao 44)")
    p.add_argument("--divisor", type=int, default=None, help="padrao: semanal x 5 (44->220, 40->200, 36->180)")
    p.add_argument("--feriados", default="", help="dd/mm/aaaa separados por virgula (locais, Sexta Santa...)")
    p.add_argument("--multa-fgts", type=int, default=0, choices=(0, 20, 40))
    a = p.parse_args()
    extra = [d(x) for x in a.feriados.split(",") if x.strip()]
    dias = ler_csv(a.csv)
    if not dias:
        raise SystemExit("CSV sem linhas de jornada")
    meses, detalhe, params = calcular(dias, a.salario, a.jornada_diaria, a.jornada_semanal, a.divisor,
                                      extra, a.multa_fgts)
    print(relatorio(a.csv, meses, detalhe, params))


if __name__ == "__main__":
    main()
