"""Verificacao da atualizacao_monetaria. SEM REDE: indices fixos gravados aqui.

    python3 test_atualizacao_monetaria.py

Os casos 2 e 3 usam taxas redondas inventadas (1,00%, 0,50%...) so pra a conta
a mao ficar legivel. O caso 1 usa o IPCA-E real de jan-mar/2024 (SGS 10764).
"""

import os
import sys
from datetime import date
from decimal import Decimal as D

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da .claude
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import argparse

from atualizacao_monetaria import RODAPE, calcular, meses, plano, q, relatorio


def rodar(valor, ini, fim, modo, series, **kw):
    ms = meses(ini, fim)
    pl = plano(modo, ms, **kw)
    linhas, fator, juros = calcular(valor, ms, pl, series)
    corr = q(D(valor) * fator)
    vj = q(corr * juros / 100)
    return pl, corr, juros, vj, corr + vj


def ok(got, esp, msg):
    assert got == D(esp), "%s: saiu %s, esperado %s" % (msg, got, esp)


def main():
    assert meses(date(2024, 1, 15), date(2024, 4, 1)) == [(2024, 1), (2024, 2), (2024, 3)]

    # --- Caso 1: so IPCA-E, dados reais jan-mar/2024 ----------------------
    # 1.000 de 15/01/2024 a 01/04/2024 -> jan, fev, mar: 0,31% 0,78% 0,36%
    # 1,0031 x 1,0078 = 1,01092418 ; x 1,0036 = 1,014563507 -> 1.014,56 ; sem juros
    s = {"IPCA-E": {(2024, 1): D("0.31"), (2024, 2): D("0.78"), (2024, 3): D("0.36")}}
    _, corr, juros, vj, tot = rodar(1000, date(2024, 1, 15), date(2024, 4, 1), "indice", s, indice="IPCA-E")
    ok(corr, "1014.56", "c1 corrigido")
    ok(tot, "1014.56", "c1 total")

    # --- Caso 2: trabalhista, atravessa as tres fases ---------------------
    # 1.000 em 01/06/2024; ajuizamento 15/07/2024; conta em 01/11/2024 -> jun..out
    #   jun: pre-judicial  IPCA-E 1,00%  juros TR 0,10%
    #   jul, ago: judicial SELIC 1,00% + 1,00% = 2,00% (soma simples)
    #   set, out: Lei 14.905 IPCA 0,50% e 0,50%, taxa legal 0,40% e 0,40%
    # fator = 1,01 x 1,02 x 1,005 x 1,005 = 1,0302 x 1,010025 = 1,040527755 -> 1.040,53
    # juros = 0,10 + 0,40 + 0,40 = 0,90% -> 1.040,53 x 0,009 = 9,36477 -> 9,36
    # total = 1.049,89
    s = {"IPCA-E": {(2024, 6): D("1.00")}, "TR": {(2024, 6): D("0.10")},
         "SELIC": {(2024, 7): D("1.00"), (2024, 8): D("1.00")},
         "IPCA": {(2024, 9): D("0.50"), (2024, 10): D("0.50")},
         "TAXA LEGAL": {(2024, 9): D("0.40"), (2024, 10): D("0.40")}}
    pl, corr, juros, vj, tot = rodar(1000, date(2024, 6, 1), date(2024, 11, 1), "trabalhista", s,
                                     ajuizamento=date(2024, 7, 15))
    assert [x[1] for x in pl] == ["IPCA-E", "SELIC", "SELIC", "IPCA", "IPCA"], pl
    ok(corr, "1040.53", "c2 corrigido")
    ok(juros, "0.90", "c2 juros %")
    ok(vj, "9.36", "c2 juros R$")
    ok(tot, "1049.89", "c2 total")

    # --- Caso 3: civel, INPC + 1% a.m. ate 08/2024, depois Lei 14.905 -------
    # 1.000 em 01/07/2024; juros desde 01/08/2024 (citacao); conta em 01/11/2024 -> jul..out
    #   jul: INPC 0,50% sem juros ; ago: INPC 0,50% + 1% ; set/out: IPCA 0,50% + taxa legal 0,40%
    # fator = 1,005^4 = 1,0201505 -> 1.020,15
    # juros = 1 + 0,4 + 0,4 = 1,80% -> 1.020,15 x 0,018 = 18,3627 -> 18,36 ; total 1.038,51
    s = {"INPC": {(2024, 7): D("0.50"), (2024, 8): D("0.50")},
         "SELIC": {(2024, 8): D("1.00")},
         "IPCA": {(2024, 9): D("0.50"), (2024, 10): D("0.50")},
         "TAXA LEGAL": {(2024, 9): D("0.40"), (2024, 10): D("0.40")}}
    _, corr, juros, vj, tot = rodar(1000, date(2024, 7, 1), date(2024, 11, 1), "civel", s, indice="INPC",
                                    juros_desde=date(2024, 8, 1), juros_antes="1")
    ok(corr, "1020.15", "c3 corrigido")
    ok(juros, "1.80", "c3 juros %")
    ok(tot, "1038.51", "c3 total")

    # --- Caso 3b: mesmo, mas juros pela SELIC antes da Lei 14.905 ----------
    # ago vira SELIC 1,00% (no lugar de INPC + 1%)
    # fator = 1,005 x 1,01 x 1,005 x 1,005 = 1,015075125 x 1,01 = 1,025225876 -> 1.025,23
    # juros = 0,80% -> 1.025,23 x 0,008 = 8,20 ; total 1.033,43
    _, corr, juros, vj, tot = rodar(1000, date(2024, 7, 1), date(2024, 11, 1), "civel", s, indice="INPC",
                                    juros_desde=date(2024, 8, 1), juros_antes="SELIC")
    ok(corr, "1025.23", "c3b corrigido")
    ok(tot, "1033.43", "c3b total")

    # --- indice faltando: tem que PARAR, nunca seguir calado ----------------
    try:
        rodar(1000, date(2024, 1, 1), date(2024, 5, 1), "indice",
              {"IPCA-E": {(2024, 1): D(1), (2024, 2): D(1), (2024, 3): D(1)}}, indice="IPCA-E")
        raise AssertionError("mes sem indice passou calado")
    except SystemExit as e:
        assert "04/2024" in str(e), e
    # --- o relatorio inteiro renderiza, nos tres modos ---
    for modo, kw in (("trabalhista", {}), ("civel", {"indice": "INPC"}), ("indice", {"indice": "IPCA"})):
        a = argparse.Namespace(valor=D(1000), inicio="01/06/2024", fim="01/11/2024", modo=modo,
                               ajuizamento="15/07/2024", juros_desde="01/08/2024", juros_antes="1",
                               indice=kw.get("indice"))
        ms = meses(date(2024, 6, 1), date(2024, 11, 1))
        tudo = {n: {m: D("0.5") for m in ms} for n in ("IPCA-E", "INPC", "IPCA", "SELIC", "TR", "TAXA LEGAL")}
        pl = plano(modo, ms, ajuizamento=date(2024, 7, 15), indice=a.indice or "IPCA-E",
                   juros_desde=date(2024, 8, 1), juros_antes="1")
        assert relatorio(a, ms, pl, *calcular(1000, ms, pl, tudo)).endswith(RODAPE), modo
    print("ok - 4 casos conferidos a mao (indice, trabalhista 3 fases, civel x2) + indice ausente para")


if __name__ == "__main__":
    main()
