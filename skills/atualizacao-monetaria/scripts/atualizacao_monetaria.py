"""Atualizacao monetaria e juros entre duas datas, com indices do Banco Central (SGS).

O numero sai DAQUI, nunca do modelo. Python stdlib. Unica rede: api.bcb.gov.br.

Tres modos (o ADVOGADO escolhe, de acordo com a decisao do caso):

  indice       corrige por UM indice (IPCA-E, INPC, IPCA ou SELIC) e, se pedir, juros simples
  trabalhista  ADC 58/59 STF + TST pos-Lei 14.905/2024:
                 antes do ajuizamento ........ IPCA-E + juros TR (art. 39, caput, Lei 8.177/91)
                 do ajuizamento a 08/2024 .... SELIC (ja inclui juros)
                 de 09/2024 em diante ........ IPCA + juros pela taxa legal (SELIC - IPCA, art. 406 CC)
  civel        Lei 14.905/2024: ate 08/2024 indice escolhido + juros escolhidos;
               de 09/2024 em diante IPCA (art. 389 CC) + taxa legal (art. 406 CC)

  uv run atualizacao_monetaria.py --valor 10000 --inicio 15/03/2022 --fim 01/11/2026 \
      --modo trabalhista --ajuizamento 10/05/2023

Convencao: tudo por MES. O mes da data inicial entra inteiro; o mes da data final nao entra.
"""

import argparse
import json
import sys
import urllib.request
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RODAPE = "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."
# Codigos conferidos na API em 19/11/2026.
SERIES = {"IPCA-E": 10764, "INPC": 188, "IPCA": 433, "SELIC": 4390, "TR": 7811, "TAXA LEGAL": 29543}
UA = "Mozilla/5.0 (kit-advogado JurisLabs; calculo judicial)"  # Cloudflare barra Python-urllib
LEI_14905 = (2024, 9)  # vigencia 30/08/2024 -> por mes, de setembro/2024 em diante
C = Decimal("0.01")


def q(v):
    return Decimal(v).quantize(C, ROUND_HALF_UP)


def brl(v):
    v = q(v)
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-R$ " if v < 0 else "R$ ") + s


def pct(v, casas=4):
    return (str(Decimal(v).quantize(Decimal(10) ** -casas, ROUND_HALF_UP)) + "%").replace(".", ",")


def d(s):
    dia, mes, ano = (int(x) for x in s.split("/"))
    return date(ano, mes, dia)


def meses(ini, fim):
    """Meses de ini (inclusive) a fim (exclusive), como (ano, mes)."""
    a, m = ini.year, ini.month
    out = []
    while (a, m) < (fim.year, fim.month):
        out.append((a, m))
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return out


def buscar(nome, ini, fim):
    """{(ano, mes): Decimal %} da serie SGS. Fatia de 10 em 10 anos (limite da API)."""
    cod, out = SERIES[nome], {}
    for a0 in range(ini[0], fim[0] + 1, 10):
        di, df = "01/%02d/%d" % ((ini[1] if a0 == ini[0] else 1), a0), "31/12/%d" % min(a0 + 9, fim[0])
        url = ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.%d/dados?formato=json"
               "&dataInicial=%s&dataFinal=%s" % (cod, di, df))
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                dados = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            raise SystemExit("Falha ao buscar %s (SGS %d) no Banco Central: %s" % (nome, cod, e))
        for x in dados:
            dd, mm, aa = x["data"].split("/")
            out[(int(aa), int(mm))] = Decimal(x["valor"])
    return out


def plano(modo, ms, ajuizamento=None, indice="IPCA-E", juros_desde=None, juros_antes="1"):
    """Para cada mes: (fase, serie_de_correcao, modo_correcao, serie_ou_taxa_de_juros)."""
    p = []
    jd = (juros_desde.year, juros_desde.month) if juros_desde else None
    for m in ms:
        com_juros = jd is not None and m >= jd
        if modo == "indice":
            jur = Decimal(juros_antes) if com_juros else None
            p.append(("índice escolhido", indice, "soma" if indice == "SELIC" else "composto", jur))
        elif modo == "trabalhista":
            aj = (ajuizamento.year, ajuizamento.month)
            if m >= LEI_14905:
                p.append(("Lei 14.905: IPCA + taxa legal", "IPCA", "composto", "TAXA LEGAL"))
            elif m >= aj:
                p.append(("judicial: SELIC", "SELIC", "soma", None))
            else:
                p.append(("pré-judicial: IPCA-E + TR", "IPCA-E", "composto", "TR"))
        elif modo == "civel":
            if m >= LEI_14905:
                p.append(("Lei 14.905: IPCA + taxa legal", "IPCA", "composto", "TAXA LEGAL" if com_juros else None))
            elif com_juros and juros_antes.upper() == "SELIC":
                p.append(("antes da Lei 14.905: SELIC", "SELIC", "soma", None))
            else:
                p.append(("antes da Lei 14.905: %s%s" % (indice, " + juros" if com_juros else ""), indice,
                          "composto", Decimal(juros_antes) if com_juros else None))
        else:
            raise ValueError(modo)
    return p


def calcular(valor, ms, pl, series):
    """series: {nome: {(ano, mes): Decimal %}}. Devolve (linhas, fator, juros_pct)."""
    valor = Decimal(str(valor))
    faltam = sorted({(n, m) for m, (_, s, _, j) in zip(ms, pl) for n in [s] + ([j] if isinstance(j, str) else [])
                     if m not in series.get(n, {})})
    if faltam:
        raise SystemExit("Índice ainda não publicado (ou fora da série): %s.\nUse uma data final anterior "
                         "ou espere a divulgação." % ", ".join("%s %02d/%d" % (n, m[1], m[0]) for n, m in faltam))
    fator, soma_bloco, juros, linhas = Decimal(1), Decimal(0), Decimal(0), []
    for i, (m, (fase, s, modo_c, j)) in enumerate(zip(ms, pl)):
        taxa = series[s][m]
        if modo_c == "composto":
            fator *= 1 + taxa / 100
        else:  # SELIC: soma simples dentro do bloco; o bloco fecha quando a fase muda
            soma_bloco += taxa
            prox = pl[i + 1] if i + 1 < len(pl) else None
            if not prox or prox[2] != "soma":
                fator *= 1 + soma_bloco / 100
                soma_bloco = Decimal(0)
        jm = Decimal(0)
        if isinstance(j, str):
            jm = max(series[j][m], Decimal(0))
        elif j is not None:
            jm = j
        juros += jm
        linhas.append((m, fase, s, taxa, fator, jm, juros))
    return linhas, fator, juros


def relatorio(a, ms, pl, linhas, fator, juros):
    valor = Decimal(str(a.valor))
    corrigido = q(valor * fator)
    vjuros = q(corrigido * juros / 100)
    o = ["# Memória de cálculo — atualização monetária", "", "MINUTA. Não é peça. Conferir antes de usar.", "",
         "- Valor original: %s em %s · atualizado até %s" % (brl(valor), a.inicio, a.fim),
         "- Modo: **%s**%s" % (a.modo, " · ajuizamento %s" % a.ajuizamento if a.ajuizamento else ""),
         "- Fonte dos índices: Banco Central, SGS (%s)" % ", ".join(
             "%s = série %d" % (n, SERIES[n]) for n in sorted({x[1] for x in pl} |
                                                             {x[3] for x in pl if isinstance(x[3], str)})),
         "- Convenção: por mês; o mês inicial entra inteiro e o mês final não entra (sem pro rata dia).",
         "", "## Mês a mês", "",
         "| Mês | Fase | Correção | Taxa do mês | Fator acumulado | Juros do mês | Juros acumulados |",
         "|---|---|---|---:|---:|---:|---:|"]
    for m, fase, s, taxa, f, jm, jac in linhas:
        o.append("| %02d/%d | %s | %s | %s | %s | %s | %s |" % (
            m[1], m[0], fase, s, pct(taxa), str(f.quantize(Decimal("0.000001"))).replace(".", ","),
            pct(jm), pct(jac)))
    o += ["", "SELIC: as taxas mensais de um mesmo período corrido se SOMAM (juros simples) e o bloco entra no "
          "fator quando a fase muda. Juros: soma simples das taxas mensais, aplicada sobre o valor já corrigido.",
          "", "## Resultado", "", "| Item | Conta | Valor |", "|---|---|---:|",
          "| Valor original | | %s |" % brl(valor),
          "| Valor corrigido | %s x %s | %s |" % (brl(valor), str(fator.quantize(Decimal("0.000001"))).replace(".", ","),
                                               brl(corrigido)),
          "| Juros | %s x %s | %s |" % (brl(corrigido), pct(juros), brl(vjuros)),
          "| **Total atualizado** | | **%s** |" % brl(corrigido + vjuros), "", "## Regra adotada neste modo", ""]
    if a.modo == "trabalhista":
        o += ["- Antes do ajuizamento: IPCA-E + juros pela TR acumulada (art. 39, caput, Lei 8.177/91) — "
              "STF, ADC 58 e 59 (com os embargos de declaração).",
              "- Do ajuizamento até 08/2024: SELIC, que já engloba correção e juros (ADC 58/59).",
              "- A partir de 30/08/2024 (por mês: 09/2024 em diante): IPCA + juros pela taxa legal "
              "(SELIC - IPCA, não negativa), arts. 389 e 406 do CC na redação da Lei 14.905/2024 — "
              "TST, SDI-1, E-ED-RR-713-03.2010.5.04.0029 (out/2024).",
              "- [conferir] Há divergência sobre a fase pré-judicial depois de 30/08/2024 e sobre o mês do "
              "ajuizamento (aqui ele já entra como SELIC); há ementas do julgado do TST que falam em IPCA-E, e não "
              "IPCA, depois de 30/08/2024. Siga o que a sentença mandou."]
    elif a.modo == "civel":
        o += ["- Até 08/2024: correção por %s; juros %s a partir de %s." % (
                  a.indice, "pela SELIC (que substitui a correção nesse período)" if a.juros_antes.upper() == "SELIC"
                  else "de %s%% ao mês, simples" % a.juros_antes, a.juros_desde or "(sem juros)"),
              "- A partir de 30/08/2024 (09/2024 em diante): IPCA (art. 389, par. único, CC) + juros pela taxa "
              "legal (art. 406, §§1º e 3º, CC; Res. CMN 5.171/2024; série 29543 do BCB, não negativa).",
              "- [conferir] Antes da Lei 14.905 a taxa do art. 406 era disputada: 1% a.m. (art. 161, §1º, CTN) "
              "ou SELIC (STJ, Corte Especial, REsp 1.795.982, 2024). E cada tribunal tem sua tabela "
              "(INPC, IPCA-E, ICGJ). Use o que a decisão fixou."]
    else:
        o += ["- Correção só por %s%s." % (a.indice, "; juros de %s%% a.m. simples desde %s" % (
            a.juros_antes, a.juros_desde) if a.juros_desde else ", sem juros")]
    o += ["", RODAPE]
    return "\n".join(o)


def main():
    p = argparse.ArgumentParser(description="Atualizacao monetaria com indices do BCB")
    p.add_argument("--valor", required=True, type=Decimal)
    p.add_argument("--inicio", required=True, help="dd/mm/aaaa (vencimento / data do valor)")
    p.add_argument("--fim", required=True, help="dd/mm/aaaa (data da conta)")
    p.add_argument("--modo", required=True, choices=("indice", "trabalhista", "civel"))
    p.add_argument("--indice", default=None, choices=("IPCA-E", "INPC", "IPCA", "SELIC"),
                   help="modo indice: obrigatorio; modo civel: indice ate 08/2024 (padrao INPC)")
    p.add_argument("--ajuizamento", default=None, help="dd/mm/aaaa (obrigatorio no modo trabalhista)")
    p.add_argument("--juros-desde", default=None, help="dd/mm/aaaa (citacao, evento...)")
    p.add_argument("--juros-antes", default="1", help="%% a.m. simples (padrao 1) ou SELIC (civel, ate 08/2024)")
    a = p.parse_args()
    ini, fim = d(a.inicio), d(a.fim)
    if fim <= ini:
        p.error("--fim tem que ser depois de --inicio")
    if a.modo == "trabalhista" and not a.ajuizamento:
        p.error("modo trabalhista precisa de --ajuizamento")
    if a.modo == "indice" and not a.indice:
        p.error("modo indice precisa de --indice")
    if a.modo == "civel" and not a.indice:
        a.indice = "INPC"
    if a.modo == "indice" and a.juros_antes.upper() == "SELIC":
        p.error("no modo indice, --juros-antes e um numero (%% a.m.)")
    ms = meses(ini, fim)
    if not ms:
        p.error("inicio e fim no mesmo mes: nada a corrigir nesta convencao")
    pl = plano(a.modo, ms, d(a.ajuizamento) if a.ajuizamento else None, a.indice or "IPCA-E",
               d(a.juros_desde) if a.juros_desde else None, a.juros_antes)
    nomes = {x[1] for x in pl} | {x[3] for x in pl if isinstance(x[3], str)}
    series = {n: buscar(n, ms[0], ms[-1]) for n in nomes}
    linhas, fator, juros = calcular(a.valor, ms, pl, series)
    print(relatorio(a, ms, pl, linhas, fator, juros))


if __name__ == "__main__":
    main()
