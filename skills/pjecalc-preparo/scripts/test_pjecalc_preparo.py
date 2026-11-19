"""Verificacao do pjecalc_preparo. Assert puro, sem rede, dados ficticios.

    python3 test_pjecalc_preparo.py
"""

import os
import sys
from datetime import date

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da .claude
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pjecalc_preparo import FALTA, RODAPE, conferir, menos_anos, relatorio_conferencia, roteiro

P = {
    "processo": "0000000-00.2023.5.03.0001",
    "admissao": {"valor": "01/02/2015", "fonte": "sentença, p. 3"},
    "demissao": {"valor": "01/03/2023", "fonte": "p. 3"},
    "ajuizamento": "10/05/2023",
    "prescricao_quinquenal": {"valor": True, "fonte": "p. 5"},
    "salario": {"valor": "R$ 3.000,00", "fonte": "p. 4"},
    "verbas": [
        {"nome": "Horas extras 50%", "periodo": "10/05/2018 a 01/03/2023", "parametros": "excedentes da 8a diaria",
         "reflexos": ["DSR", "13º", "férias + 1/3", "FGTS + 40%"], "fonte": "p. 7"},
        {"nome": "Adicional de insalubridade", "periodo": "10/05/2018 a 01/03/2023", "parametros": "20% do salário mínimo",
         "reflexos": [], "fonte": "p. 9"},
    ],
    "fgts": {"valor": "depósitos + multa de 40%", "fonte": "p. 10"},
    "correcao": {"valor": "IPCA-E na fase pré-judicial e SELIC a partir do ajuizamento (ADC 58)", "fonte": "p. 11"},
    "honorarios": {"valor": "10% sobre o valor líquido, ao advogado do reclamante", "fonte": "p. 12"},
}

RELATORIO = """PJe-Calc Cidadao - Resumo do Calculo
Admissao: 01/02/2015  Demissao: 01/03/2023  Ajuizamento: 10/05/2023
Prescricao quinquenal: 10/05/2018
HORAS EXTRAS 50%  ............  12.345,67
REFLEXO HE EM DSR ............   2.000,00
FGTS 8% ......................   1.000,00
MULTA FGTS 40% ...............     400,00
Correcao monetaria: IPCA-E / TR
Honorarios advocaticios 15% ..   2.000,00
"""


def main():
    # --- prescricao: data - 5 anos, inclusive 29/02 -------------------------
    # 10/05/2023 - 5 anos = 10/05/2018 ; 29/02/2024 - 5 anos = 28/02/2019 (2019 nao e bissexto)
    assert menos_anos(date(2023, 5, 10), 5) == date(2018, 5, 10)
    assert menos_anos(date(2024, 2, 29), 5) == date(2019, 2, 28)

    # --- roteiro -------------------------------------------------------------
    r = roteiro(P)
    assert "**10/05/2018**" in r, r
    assert "ajuizada dentro de 2 anos" in r  # demissao 01/03/2023, ajuizamento 10/05/2023
    assert "Cartão de Ponto" in r  # tem hora extra
    assert r.count(FALTA) >= 5, "inss, ir, custas, juros, carga horaria nao constam: tinha que apontar"
    assert "**sem página**" in r  # ajuizamento veio sem fonte
    # o resumo final lista TODA tela que levou FALTA, com o nome da tela (nao a chave do JSON)
    resumo = r.split("## O que a decisão não disse")[1]
    for rot in ("Faltas e férias", "Carga horária", "Juros", "Custas", "Imposto de renda", "Jornada"):
        assert rot in resumo, (rot, resumo)
    assert "faltas_ferias" not in resumo and "honorarios" not in resumo, resumo
    # bienal: demissao 01/03/2021 com ajuizamento 10/05/2023 -> passou de 10/05/2021
    r2 = roteiro(dict(P, demissao="01/03/2021"))
    assert "Atenção, bienal" in r2, r2

    # --- conferencia ---------------------------------------------------------
    # no relatorio: falta a insalubridade, falta SELIC, honorarios 15% (sentenca 10%)
    res = {(a, b): c for a, b, c, _ in conferir(P, RELATORIO)}
    assert res[("Admissão", "01/02/2015")] == "ok"
    assert res[("Prescrição quinquenal (marco)", "10/05/2018")] == "ok"
    assert res[("Verba", "Horas extras 50%")] == "ok"
    assert res[("Verba", "Adicional de insalubridade")] != "ok"
    assert res[("Índice (correcao)", "IPCA-E")] == "ok"
    assert res[("Índice (correcao)", "SELIC")] != "ok"
    assert ("Índice (correcao)", "IPCA") not in res, "IPCA-E nao pode ser lido como IPCA"
    assert res[("Reflexo de Horas extras 50%", "DSR")] == "ok"
    assert res[("Reflexo de Horas extras 50%", "13º")] != "ok"
    assert res[("Reflexo de Horas extras 50%", "férias + 1/3")] != "ok"
    assert res[("Multa do FGTS", "40%")] == "ok"
    assert res[("Honorários", "10%")] != "ok"
    assert relatorio_conferencia(conferir(P, RELATORIO)).endswith(RODAPE)
    print("ok - prescricao/bienal, roteiro com omissoes, conferencia acha as 5 divergencias plantadas")


if __name__ == "__main__":
    main()
