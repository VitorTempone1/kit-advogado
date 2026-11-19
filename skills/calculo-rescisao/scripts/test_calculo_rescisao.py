"""Verificacao do calculo_rescisao. Assert puro, sem rede, sem framework.

    python3 test_calculo_rescisao.py

Cada caso tem a conta feita A MAO no comentario. Se o script divergir, o
teste quebra e mostra o valor que saiu.
"""

import os
import sys
from datetime import date
from decimal import Decimal

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da .claude
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import argparse

from calculo_rescisao import RODAPE, avos_13, avos_ferias, calcular, relatorio


def verbas(r):
    linhas, fgts = r[0], r[1]
    return {n: v for n, _, v in linhas + fgts}


def ok(got, esperado, msg):
    assert got == Decimal(esperado), "%s: saiu %s, esperado %s" % (msg, got, esperado)


def main():
    # --- Caso 1: sem justa causa, aviso indenizado ------------------------
    # Admissao 10/02/2021, demissao 15/03/2025, salario 3.000, saldo FGTS 9.000
    # saldo de salario: 3000/30 x 15 dias = 1.500,00
    # anos completos em 15/03/2025: 4 -> aviso 30 + 3x4 = 42 dias -> 3000/30 x 42 = 4.200,00
    # projecao: 15/03/2025 + 42 dias = 26/04/2025
    # ferias prop.: aquisitivo 10/02/2025 a 26/04/2025 = 2 meses + 17 dias -> 3/12
    #   (3000 + 1000) x 3/12 = 1.000,00
    # 13o 2025: jan, fev, mar, abr(26 dias) -> 4/12 x 3000 = 1.000,00
    # FGTS: 8% x (1500 + 4200 + 1000) = 536,00
    # multa 40%: 0,40 x (9000 + 536) = 3.814,40
    # total bruto: 1500 + 4200 + 1000 + 1000 = 7.700,00
    r = calcular(date(2021, 2, 10), date(2025, 3, 15), "3000", "sem_justa_causa", saldo_fgts=Decimal(9000))
    v = verbas(r)
    ok(v["Saldo de salário"], "1500.00", "c1 saldo")
    ok(v["Aviso prévio indenizado"], "4200.00", "c1 aviso")
    assert r[5] == 42 and r[6] == date(2025, 4, 26), r[5:]
    ok(v["Férias proporcionais + 1/3"], "1000.00", "c1 ferias prop")
    ok(v["13º salário proporcional 2025"], "1000.00", "c1 13o")
    ok(v["FGTS sobre a rescisão"], "536.00", "c1 fgts")
    ok(v["Multa de 40% do FGTS"], "3814.40", "c1 multa")
    ok(r[3], "7700.00", "c1 total")

    # --- Caso 2: pedido de demissao, aviso NAO cumprido ------------------
    # Admissao 01/06/2024, demissao 20/11/2024, salario 2.400
    # saldo: 2400/30 x 20 = 1.600,00
    # desconto do aviso: -2.400,00 (30 dias; proporcional nao vale contra o empregado)
    # ferias prop. (Sumula 261, menos de 1 ano): 01/06 a 20/11 = 5 meses + 20 dias -> 6/12
    #   (2400 + 800) x 6/12 = 1.600,00
    # 13o 2024: jun-out (5) + nov (20 dias) = 6/12 x 2400 = 1.200,00
    # FGTS: 8% x (1600 + 1200) = 224,00 ; sem multa
    # total: 1600 - 2400 + 1600 + 1200 = 2.000,00
    r = calcular(date(2024, 6, 1), date(2024, 11, 20), "2400", "pedido_demissao", aviso="indenizado")
    v = verbas(r)
    ok(v["Saldo de salário"], "1600.00", "c2 saldo")
    ok(v["Desconto do aviso não cumprido"], "-2400", "c2 desconto")
    ok(v["Férias proporcionais + 1/3"], "1600.00", "c2 ferias")
    ok(v["13º salário proporcional 2024"], "1200.00", "c2 13o")
    ok(v["FGTS sobre a rescisão"], "224.00", "c2 fgts")
    assert not any(k.startswith("Multa") for k in v), v
    ok(r[3], "2000.00", "c2 total")

    # --- Caso 3: justa causa, 1 periodo de ferias vencido -----------------
    # Admissao 05/01/2020, demissao 31/08/2023 (ultimo dia do mes), salario 1.800
    # saldo: mes inteiro = 1.800,00
    # ferias vencidas: 1 x (1800 + 600) = 2.400,00
    # sem aviso, sem proporcionais, sem multa. FGTS: 8% x 1800 = 144,00
    # total: 4.200,00
    r = calcular(date(2020, 1, 5), date(2023, 8, 31), "1800", "justa_causa", ferias_vencidas=1)
    v = verbas(r)
    ok(v["Saldo de salário"], "1800", "c3 saldo")
    ok(v["Férias vencidas + 1/3"], "2400.00", "c3 vencidas")
    assert set(v) == {"Saldo de salário", "Férias vencidas + 1/3", "FGTS sobre a rescisão"}, v
    ok(v["FGTS sobre a rescisão"], "144.00", "c3 fgts")
    ok(r[3], "4200.00", "c3 total")

    # --- Caso 4: acordo art. 484-A ----------------------------------------
    # Admissao 01/03/2015, demissao 10/03/2025, salario 5.000, saldo FGTS 40.000
    # saldo: 5000/30 x 10 = 1.666,67
    # 10 anos completos -> aviso 60 dias; metade = 30 dias -> 5.000,00
    # projecao de 30 dias -> 09/04/2025
    # ferias prop.: 01/03/2025 a 09/04/2025 = 1 mes + 9 dias (<15) -> 1/12
    #   6666,67 x 1/12 = 555,56
    # 13o: jan, fev, mar (abr so 9 dias) -> 3/12 x 5000 = 1.250,00
    # FGTS: 8% x (1666,67 + 5000 + 1250) = 633,33
    # multa 20%: 0,20 x (40000 + 633,33) = 8.126,67
    # total: 1666,67 + 5000 + 555,56 + 1250 = 8.472,23
    r = calcular(date(2015, 3, 1), date(2025, 3, 10), "5000", "acordo", saldo_fgts=Decimal(40000))
    v = verbas(r)
    ok(v["Saldo de salário"], "1666.67", "c4 saldo")
    ok(v["Aviso prévio indenizado"], "5000.00", "c4 aviso")
    ok(v["Férias proporcionais + 1/3"], "555.56", "c4 ferias")
    ok(v["13º salário proporcional 2025"], "1250.00", "c4 13o")
    ok(v["FGTS sobre a rescisão"], "633.33", "c4 fgts")
    ok(v["Multa de 20% do FGTS"], "8126.67", "c4 multa")
    ok(r[3], "8472.23", "c4 total")

    # --- teto de 90 dias: 25 anos -> 30 + 75 = 105 -> 90 -----------------
    r = calcular(date(2000, 1, 1), date(2025, 6, 1), "3000", "sem_justa_causa", saldo_fgts=Decimal(0))
    assert r[5] == 90, r[5]

    # --- funcoes de contagem ----------------------------------------------
    assert avos_ferias(date(2025, 1, 1), date(2025, 1, 14))[0] == 0  # 14 dias nao fecha avo
    assert avos_ferias(date(2025, 1, 1), date(2025, 1, 15))[0] == 1  # 15 fecha
    assert avos_13(date(2024, 3, 17), date(2024, 12, 31), 2024) == 10  # mar 17-31 = 15 dias: conta (+ abr-dez 9)
    assert avos_13(date(2024, 3, 18), date(2024, 12, 31), 2024) == 9  # marco 14 dias: nao conta
    # --- o relatorio inteiro renderiza (formatacao com % ja quebrou em irmao) ---
    for tipo in ("sem_justa_causa", "pedido_demissao", "justa_causa", "acordo"):
        a = argparse.Namespace(admissao="10/02/2021", demissao="15/03/2025", salario=Decimal(3000), tipo=tipo,
                               ferias_vencidas=1, ferias_dobro=1, aviso=None, saldo_fgts=None)
        assert relatorio(a).endswith(RODAPE), tipo
    print("ok - 4 casos conferidos a mao + teto do aviso + contagem de avos")


if __name__ == "__main__":
    main()
