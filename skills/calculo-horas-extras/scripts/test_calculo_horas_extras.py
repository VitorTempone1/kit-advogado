"""Verificacao do calculo_horas_extras. Assert puro, sem rede.

    python3 test_calculo_horas_extras.py

Contas feitas a mao nos comentarios.
"""

import os
import sys
import tempfile
from datetime import date
from decimal import Decimal

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da .claude
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calculo_horas_extras import RODAPE, calcular, ler_csv, relatorio


def ok(got, esperado, msg):
    assert got == Decimal(esperado), "%s: saiu %s, esperado %s" % (msg, got, esperado)


def dia(s, ent, sai, intv):
    dd, mm, aa = (int(x) for x in s.split("/"))
    h = lambda t: int(t[:2]) * 60 + int(t[3:])
    return (date(aa, mm, dd), h(ent), h(sai), intv)


def main():
    # --- Caso A: excedente diario + domingo -------------------------------
    # salario 2200, 44h -> divisor 220 -> hora = 10,00
    # seg 03/06/2024 a sex 07/06: 08-18 com 1h de intervalo = 9h -> 1h extra/dia = 5h a 50%
    #   5 x 10 x 1,5 = 75,00
    # dom 09/06: 08-12 = 4h a 100% -> 4 x 10 x 2 = 80,00 ; HE do mes = 155,00
    # junho/2024: 30 dias, domingos 2,9,16,23,30 = 5, sem feriado nacional -> 25 uteis
    #   DSR = 155 / 25 x 5 = 31,00 (todo apos 20/03/2023 -> reflete)
    # 13o = (155 + 31)/12 = 15,50 ; ferias+1/3 = 15,50 x 4/3 = 20,67
    # FGTS = 8% x (155 + 31 + 15,50) = 16,12
    dias = [dia("%02d/06/2024" % i, "08:00", "18:00", 60) for i in range(3, 8)]
    dias.append(dia("09/06/2024", "08:00", "12:00", 0))
    m = calcular(dias, "2200")[0][(2024, 6)]
    assert (m["he50"], m["he100"]) == (300, 240), m
    ok(m["v50"], "75.00", "A 50%")
    ok(m["v100"], "80.00", "A 100%")
    assert (m["uteis"], m["repouso"]) == (25, 5), m
    ok(m["dsr"], "31.00", "A dsr")
    ok(m["d13"], "15.50", "A 13o")
    ok(m["ferias"], "20.67", "A ferias")
    ok(m["fgts"], "16.12", "A fgts")

    # --- Caso B: excedente semanal + tolerancia de 10 min -----------------
    # salario 3000, divisor 220 -> hora = 13,636363...
    # seg 01/07 a sab 06/07/2024: 08-17 c/ 1h = 8h/dia, 6 dias = 48h normais (diario: zero)
    #   semana: 48h - 44h = 4h a 50%
    # seg 08/07: 08-17:15 c/ 1h = 8h15 -> 15 min > 10 -> conta inteiro: 0,25h
    # ter 09/07: 08-17:08 c/ 1h = 8h08 -> 8 min <= 10 -> desprezado
    # total 4,25h x 13,6363 x 1,5 = 86,93
    # julho/2024: domingos 7,14,21,28 = 4 -> 27 uteis ; DSR = 86,93/27 x 4 = 12,88
    dias = [dia("%02d/07/2024" % i, "08:00", "17:00", 60) for i in range(1, 7)]
    dias += [dia("08/07/2024", "08:00", "17:15", 60), dia("09/07/2024", "08:00", "17:08", 60)]
    meses, detalhe, _ = calcular(dias, "3000")
    m = meses[(2024, 7)]
    assert m["he50"] == 255 and m["he100"] == 0, m
    ok(m["v50"], "86.93", "B 50%")
    ok(m["dsr"], "12.88", "B dsr")
    assert detalhe[-1]["he50"] == 0 and "tolerados" in detalhe[-1]["obs"], detalhe[-1]

    # --- Caso C: OJ 394 - virada de 20/03/2023 ----------------------------
    # salario 2200 -> hora 10. qua 15/03/2023 e qua 22/03/2023: 08-20 c/ 1h = 11h -> 3h a 50% cada
    #   45,00 + 45,00 = 90,00
    # marco/2023: domingos 5,12,19,26 = 4 -> 27 uteis ; DSR = 90/27 x 4 = 13,33
    # so a metade do dia 22 (apos 20/03/2023) reflete: 13,33 x 45/90 = 6,665 -> 6,67
    # 13o = (90 + 6,67)/12 = 8,06 ; ferias = 96,67/12 x 4/3 = 10,74
    # FGTS = 8% x (90 + 6,67 + 8,06) = 8,38
    dias = [dia("15/03/2023", "08:00", "20:00", 60), dia("22/03/2023", "08:00", "20:00", 60)]
    m = calcular(dias, "2200")[0][(2023, 3)]
    ok(m["he"], "90.00", "C he")
    ok(m["dsr"], "13.33", "C dsr")
    ok(m["dsr_refl"], "6.67", "C dsr que reflete")
    ok(m["d13"], "8.06", "C 13o")
    ok(m["ferias"], "10.74", "C ferias")
    ok(m["fgts"], "8.38", "C fgts")

    # --- feriado nacional e divisor 200 ----------------------------------
    # 15/11/2024 (sexta, feriado) 08-12 = 4h a 100%; 40h -> divisor 200 -> hora 2000/200 = 10 -> 80,00
    m = calcular([dia("15/11/2024", "08:00", "12:00", 0)], "2000", jornada_semanal_h=40)[0][(2024, 11)]
    ok(m["v100"], "80.00", "feriado")

    # --- leitura do CSV com ; e virada da meia-noite ----------------------
    with tempfile.TemporaryDirectory() as t:
        c = os.path.join(t, "j.csv")
        with open(c, "w", encoding="utf-8") as f:
            f.write("Data;Entrada;Saida;Intervalo\n10/06/2024;22:00;07:00;01:00\n")
        (dt, ent, sai, intv), = ler_csv(c)
        assert dt == date(2024, 6, 10) and intv == 60
        assert calcular(ler_csv(c), "2200")[1][0]["trab"] == 480
    # --- o relatorio inteiro renderiza (um "50%" sem escape ja derrubou a saida) ---
    meses, detalhe, p = calcular(dias, "2200", multa_fgts=40)
    assert relatorio("x.csv", meses, detalhe, p).endswith(RODAPE)
    print("ok - 3 casos conferidos a mao + feriado/divisor + leitura de CSV")


if __name__ == "__main__":
    main()
