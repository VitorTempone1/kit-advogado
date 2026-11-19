"""Verificacao do calculo_previdenciario. Assert puro, sem rede.

    python3 test_calculo_previdenciario.py

Contas feitas a mao nos comentarios (dias inclusivos; ano = 365 dias).
"""

import os
import sys
from datetime import date

sys.dont_write_bytecode = True  # nada de __pycache__ dentro da .claude
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calculo_previdenciario import RODAPE, calcular, relatorio


def regra(r, prefixo):
    for nome, _, situacao, _, dt in r["regras"]:
        if nome.startswith(prefixo):
            return situacao, dt
    raise KeyError(prefixo)


def main():
    # --- Caso 1: homem, um vinculo so -----------------------------------
    # nasc. 01/01/1965; vinculo 01/01/1987 a 31/12/2024; DER 01/01/2025
    # TC = 38 anos com 10 bissextos (1988..2024) = 38x365 + 10 = 13.880 dias
    # TC em 13/11/2019: 01/01/1987..31/12/2018 = 32x365 + 8 = 11.688 ; + 01/01..13/11/2019 = 317
    #   = 12.005 dias = 32,89 anos -> NAO passa de 33 -> pedagio 50% nao se aplica
    # pedagio 100%: faltavam 35x365 - 12.005 = 12.775 - 12.005 = 770 -> precisa 13.545 dias e 60 anos
    #   na DER: 13.880 >= 13.545 e faz 60 em 01/01/2025 -> JA CUMPRE
    # idade progressiva: de 2027 em diante, 65 anos -> 01/01/2030
    # carencia: jan/1987 a dez/2024 = 38 x 12 = 456 meses
    v = [(date(1987, 1, 1), date(2024, 12, 31), "Empresa X")]
    r = calcular(v, date(1965, 1, 1), "M", date(2025, 1, 1))
    assert r["tc"] == 13880, r["tc"]
    assert r["tc2019"] == 12005, r["tc2019"]
    assert r["carencia"] == 456, r["carencia"]
    assert regra(r, "Pedágio de 50%")[0] == "não se aplica"
    assert regra(r, "Pedágio de 100%") == ("JÁ CUMPRE", date(2025, 1, 1)), regra(r, "Pedágio de 100%")
    assert regra(r, "Idade progressiva")[1] == date(2030, 1, 1), regra(r, "Idade progressiva")
    assert regra(r, "Pontos")[0] != "JÁ CUMPRE"  # 60 + 38,03 = 98,03 < 102 (2025)

    # --- Caso 2: mulher, concomitancia, pedagio 50% e pontos -------------
    # nasc. 10/05/1968; DER 01/07/2025
    # A 01/03/1990-28/02/2000 ; B 01/01/1999-31/12/2010 ; C 01/01/2012-ativo
    # concomitancia A x B: 01/01/1999 a 28/02/2000 = 365 + 31 (jan) + 28 (fev ate dia 28) = 424 dias
    # uniao: 01/03/1990-31/12/2010 = 20x365 + 5 bissextos + 306 = 7.611
    #        01/01/2012-01/07/2025 = 13x365 + 4 + 182 = 4.931  -> TC = 12.542 dias (34,36 anos)
    # TC em 13/11/2019: 7.611 + (01/01/2012..13/11/2019 = 7x365 + 2 + 317 = 2.874) = 10.485 (28,73 > 28)
    # pedagio 50%: faltavam 10.950 - 10.485 = 465 -> precisa 10.950 + 232,5 -> 12.542 cumpre: JA CUMPRE
    # pontos 2025 = 92: idade 57 + 52/365 = 57,14247 ; TC 12.542/365 = 34,36164 ; soma 91,50411
    #   cada dia soma 2/365: +90 dias = 91,99726 (nao) ; +91 dias = 92,00274 -> 30/09/2025
    # idade progressiva: 2027 pede 60 (faz em 10/05/2028, mas 2028 pede 60,5) -> 10/11/2028
    v = [(date(1990, 3, 1), date(2000, 2, 28), "A"), (date(1999, 1, 1), date(2010, 12, 31), "B"),
         (date(2012, 1, 1), None, "C")]
    r = calcular(v, date(1968, 5, 10), "F", date(2025, 7, 1))
    assert [c[4] for c in r["concomitancias"]] == [424], r["concomitancias"]
    assert r["tc"] == 12542, r["tc"]
    assert r["tc2019"] == 10485, r["tc2019"]
    assert regra(r, "Pedágio de 50%")[0] == "JÁ CUMPRE", regra(r, "Pedágio de 50%")
    assert regra(r, "Pontos")[1] == date(2025, 9, 30), regra(r, "Pontos")
    assert regra(r, "Idade progressiva")[1] == date(2028, 11, 10), regra(r, "Idade progressiva")

    # --- Caso 3: filiado depois da EC 103 ---------------------------------
    # 01/02/2020 a 01/02/2025 (DER): 5x365 + 2 bissextos (29/02/2020 e 29/02/2024) + 1 (inclusivo) = 1.828
    r = calcular([(date(2020, 2, 1), None, "Z")], date(1990, 1, 1), "M", date(2025, 2, 1))
    assert r["tc"] == 1828, r["tc"]
    assert r["tc2019"] == 0 and not r["filiado_antes"]
    assert all(s == "não se aplica" for _, _, s, _, _ in r["regras"]), r["regras"]
    # --- o relatorio inteiro renderiza ---
    r = calcular(v, date(1968, 5, 10), "F", date(2025, 7, 1))
    assert relatorio("x.csv", v, date(1968, 5, 10), "F", date(2025, 7, 1), r).endswith(RODAPE)
    print("ok - 3 casos conferidos a mao (pedagio 100%, concomitancia + pontos + pedagio 50%, filiacao pos-EC)")


if __name__ == "__main__":
    main()
