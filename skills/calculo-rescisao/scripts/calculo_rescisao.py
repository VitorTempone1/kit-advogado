"""Verbas rescisorias (CLT) com memoria de calculo linha a linha.

O numero sai DAQUI, nunca do modelo. Python stdlib, sem rede.

  uv run calculo_rescisao.py --admissao 10/02/2021 --demissao 15/03/2025 \
      --salario 3000 --tipo sem_justa_causa [--ferias-vencidas 1] [--saldo-fgts 9000]

Tipos: sem_justa_causa | pedido_demissao | justa_causa | acordo (art. 484-A CLT)
Nao calcula INSS nem IR (v1).
"""

import argparse
import calendar
import sys
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RODAPE = "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."
TIPOS = ("sem_justa_causa", "pedido_demissao", "justa_causa", "acordo")
C = Decimal("0.01")


def d(s):
    dia, mes, ano = (int(x) for x in s.split("/"))
    return date(ano, mes, dia)


def fmt(dt):
    return dt.strftime("%d/%m/%Y")


def brl(v):
    v = Decimal(v).quantize(C, ROUND_HALF_UP)
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-R$ " if v < 0 else "R$ ") + s


def q(v):
    return Decimal(v).quantize(C, ROUND_HALF_UP)


def somar_meses(dt, n):
    m = dt.month - 1 + n
    ano, mes = dt.year + m // 12, m % 12 + 1
    return date(ano, mes, min(dt.day, calendar.monthrange(ano, mes)[1]))


def anos_completos(ini, fim):
    a = fim.year - ini.year
    return a - 1 if (fim.month, fim.day) < (ini.month, ini.day) else a


def avos_ferias(ini, fim):
    """Meses do periodo aquisitivo [ini, fim]; fracao >= 15 dias vira 1/12 (art. 146, par. un., CLT)."""
    m = 0
    while somar_meses(ini, m + 1) - timedelta(days=1) <= fim:
        m += 1
    resto = (fim - somar_meses(ini, m)).days + 1
    return m + (1 if resto >= 15 else 0), m, max(resto, 0)


def avos_13(admissao, fim, ano):
    """Meses do ano com 15+ dias trabalhados (Lei 4.090/62, art. 1o, par. 2o)."""
    avos = 0
    for mes in range(1, 13):
        ini_m = date(ano, mes, 1)
        fim_m = date(ano, mes, calendar.monthrange(ano, mes)[1])
        a, b = max(admissao, ini_m), min(fim, fim_m)
        if b >= a and (b - a).days + 1 >= 15:
            avos += 1
    return avos


def calcular(admissao, demissao, salario, tipo, ferias_vencidas=0, ferias_dobro=0,
             aviso=None, saldo_fgts=None):
    """Devolve (linhas, notas, totais). linhas = [(verba, conta, valor)]."""
    if tipo not in TIPOS:
        raise ValueError("tipo invalido: %s" % tipo)
    if demissao < admissao:
        raise ValueError("demissao antes da admissao")
    salario = Decimal(str(salario))
    if aviso is None:
        aviso = "trabalhado" if tipo == "pedido_demissao" else "indenizado"
    linhas, notas, fgts_base = [], [], Decimal(0)

    # 1. saldo de salario
    ini_mes = max(admissao, demissao.replace(day=1))
    ultimo_dia = demissao.day == calendar.monthrange(demissao.year, demissao.month)[1]
    if ultimo_dia and ini_mes.day == 1:
        dias, saldo = 30, salario
    else:
        dias = (demissao - ini_mes).days + 1
        saldo = q(salario / 30 * dias)
    linhas.append(("Saldo de salário", "%s / 30 x %d dias (de %s a %s)"
                   % (brl(salario), dias, fmt(ini_mes), fmt(demissao)), saldo))
    fgts_base += saldo

    # 2. aviso previo (Lei 12.506/2011: 30 dias + 3 por ano completo, teto 90)
    anos = anos_completos(admissao, demissao)
    dias_aviso = min(30 + 3 * anos, 90)
    projetado = 0
    if tipo in ("sem_justa_causa", "acordo") and aviso == "indenizado":
        pagos = dias_aviso if tipo == "sem_justa_causa" else dias_aviso / Decimal(2)
        valor = q(salario / 30 * Decimal(pagos))
        txt = "%s / 30 x %s dias (30 + 3 x %d anos completos = %d dias%s)" % (
            brl(salario), str(pagos).rstrip("0").rstrip(".") if tipo == "acordo" else pagos,
            anos, dias_aviso, ", pela metade: art. 484-A, I, a, CLT" if tipo == "acordo" else "")
        linhas.append(("Aviso prévio indenizado", txt, valor))
        fgts_base += valor
        projetado = int(pagos)
        if tipo == "acordo":
            notas.append("[conferir] Projeção no acordo: projetei só os %d dias pagos. "
                         "Há quem projete o aviso inteiro." % projetado)
    elif tipo == "sem_justa_causa" and aviso == "trabalhado":
        notas.append("Aviso trabalhado: a data de demissão informada deve ser o último dia do aviso. "
                     "[conferir] Os %d dias que passam de 30 costumam ser pagos indenizados." % (dias_aviso - 30)
                     if dias_aviso > 30 else
                     "Aviso trabalhado: a data de demissão informada deve ser o último dia do aviso.")
    elif tipo == "pedido_demissao" and aviso == "indenizado":
        desconto = -salario
        linhas.append(("Desconto do aviso não cumprido", "-30 dias de salário (art. 487, par. 2o, CLT). "
                       "A proporcionalidade da Lei 12.506 só vale a favor do empregado", desconto))
    fim_proj = demissao + timedelta(days=projetado)
    if projetado:
        notas.append("Projeção do aviso: %d dias somados ao tempo de serviço (art. 487, par. 1o, CLT; "
                     "OJ 82 SDI-1/TST). Data final projetada: %s." % (projetado, fmt(fim_proj)))

    # 3. ferias vencidas + 1/3
    um_terco = salario / 3
    base_ferias = salario + um_terco
    venc = ferias_vencidas
    anos_proj = anos_completos(admissao, fim_proj)
    if anos_proj > anos:
        venc += anos_proj - anos
        notas.append("A projeção do aviso completou mais %d período(s) aquisitivo(s): entrou como férias "
                     "vencidas simples." % (anos_proj - anos))
    if venc:
        simples = venc - ferias_dobro
        if simples > 0:
            linhas.append(("Férias vencidas + 1/3", "%d x (%s + 1/3 de %s)" % (simples, brl(salario), brl(salario)),
                           q(base_ferias * simples)))
        if ferias_dobro:
            linhas.append(("Férias vencidas em dobro + 1/3", "%d x 2 x (%s + 1/3) - art. 137 CLT"
                           % (ferias_dobro, brl(salario)), q(base_ferias * 2 * ferias_dobro)))

    # 4. ferias proporcionais + 1/3 (Sumula 171 e 261 TST)
    if tipo != "justa_causa":
        ini_aq = somar_meses(admissao, 12 * anos_proj)
        avos, meses, resto = avos_ferias(ini_aq, fim_proj)
        if avos:
            linhas.append(("Férias proporcionais + 1/3",
                           "%s + 1/3 = %s x %d/12 (período aquisitivo de %s a %s: %d meses + %d dias; "
                           "fração de 15+ dias = 1/12)" % (brl(salario), brl(base_ferias), avos, fmt(ini_aq),
                                                           fmt(fim_proj), meses, resto),
                           q(base_ferias * avos / 12)))
    else:
        notas.append("Justa causa: sem férias proporcionais (Súmula 171 TST), sem 13º proporcional "
                     "(Lei 4.090/62, art. 3º), sem aviso e sem multa do FGTS.")

    # 5. 13o proporcional
    if tipo != "justa_causa":
        for ano in range(demissao.year, fim_proj.year + 1):
            fim_ano = min(fim_proj, date(ano, 12, 31))
            avos = avos_13(admissao, fim_ano, ano)
            if avos:
                v = q(salario * avos / 12)
                linhas.append(("13º salário proporcional %d" % ano, "%s x %d/12 (meses com 15+ dias "
                               "trabalhados até %s)" % (brl(salario), avos, fmt(fim_ano)), v))
                fgts_base += v
        notas.append("13º: considerei que nada do 13º do ano foi pago (nem a 1ª parcela). Se foi, desconte.")

    # 6. FGTS
    fgts_mes = q(fgts_base * Decimal("0.08"))
    fgts = [("FGTS sobre a rescisão", "8%% de %s (saldo de salário + aviso indenizado + 13º; "
             "Súmula 305 TST; férias indenizadas não: OJ 195 SDI-1)" % brl(fgts_base), fgts_mes)]
    multa_pct = {"sem_justa_causa": 40, "acordo": 20}.get(tipo, 0)
    if multa_pct:
        if saldo_fgts is None:
            meses_contrato = Decimal((demissao - admissao).days + 1) / 30
            saldo_est = q(salario * Decimal("0.08") * meses_contrato * 13 / 12)
            notas.append("[estimativa] Saldo do FGTS não informado: estimei %s = 8%% x %s x %.1f meses x 13/12 "
                         "(salário constante, sem juros e correção da conta). Use o extrato do FGTS (--saldo-fgts)."
                         % (brl(saldo_est), brl(salario), meses_contrato))
            base_multa, origem = saldo_est + fgts_mes, "estimado"
        else:
            base_multa, origem = Decimal(str(saldo_fgts)) + fgts_mes, "informado"
        fgts.append(("Multa de %d%% do FGTS" % multa_pct,
                     "%d%% de %s (saldo %s + FGTS da rescisão; %s)" % (
                         multa_pct, brl(base_multa), origem,
                         "Lei 8.036/90, art. 18, par. 1o" if multa_pct == 40 else "art. 484-A, I, b, CLT"),
                     q(base_multa * multa_pct / 100)))
    if tipo == "acordo":
        notas.append("Acordo (art. 484-A): saque de até 80% do FGTS e sem seguro-desemprego (par. 1o e 2o).")
    if tipo in ("pedido_demissao", "justa_causa"):
        notas.append("Sem saque do FGTS e sem multa nesta modalidade (Lei 8.036/90, art. 20).")

    total = sum(v for _, _, v in linhas)
    total_fgts = sum(v for _, _, v in fgts)
    return linhas, fgts, notas, total, total_fgts, dias_aviso, fim_proj


def relatorio(a):
    linhas, fgts, notas, total, total_fgts, dias_aviso, fim_proj = calcular(
        d(a.admissao), d(a.demissao), a.salario, a.tipo, a.ferias_vencidas, a.ferias_dobro,
        a.aviso, a.saldo_fgts)
    out = ["# Memória de cálculo — verbas rescisórias", "",
           "MINUTA. Não é peça. Conferir antes de usar.", "",
           "- Admissão: %s · Demissão (comunicação/último dia): %s" % (a.admissao, a.demissao),
           "- Salário-base: %s · Modalidade: %s · Aviso: %s"
           % (brl(Decimal(str(a.salario))), a.tipo.replace("_", " "),
              a.aviso or ("trabalhado" if a.tipo == "pedido_demissao" else "indenizado")),
           "- Férias vencidas informadas: %d (em dobro: %d)" % (a.ferias_vencidas, a.ferias_dobro), "",
           "## Verbas a pagar no TRCT (valores brutos)", "", "| Verba | Conta | Valor |", "|---|---|---:|"]
    out += ["| %s | %s | %s |" % (n, c, brl(v)) for n, c, v in linhas]
    out += ["| **Total bruto** | | **%s** |" % brl(total), "",
            "## Depósito na conta do FGTS", "", "| Item | Conta | Valor |", "|---|---|---:|"]
    out += ["| %s | %s | %s |" % (n, c, brl(v)) for n, c, v in fgts]
    out += ["| **Total FGTS** | | **%s** |" % brl(total_fgts), "", "## Observações", ""]
    out += ["- " + n for n in notas]
    out += ["- Não calculei INSS nem IR (v1): os valores acima são brutos.",
            "- Não entram: horas extras, adicionais, médias de variáveis, multa do art. 477 e do art. 467 CLT.",
            "", RODAPE]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Verbas rescisorias com memoria de calculo")
    p.add_argument("--admissao", required=True, help="dd/mm/aaaa")
    p.add_argument("--demissao", required=True, help="dd/mm/aaaa (dia da comunicacao / ultimo dia trabalhado)")
    p.add_argument("--salario", required=True, type=Decimal)
    p.add_argument("--tipo", required=True, choices=TIPOS)
    p.add_argument("--ferias-vencidas", type=int, default=0, help="periodos completos nao gozados")
    p.add_argument("--ferias-dobro", type=int, default=0, help="quantos desses ja passaram do periodo concessivo")
    p.add_argument("--aviso", choices=("indenizado", "trabalhado"), default=None)
    p.add_argument("--saldo-fgts", type=Decimal, default=None, help="saldo da conta (extrato) para a multa")
    a = p.parse_args()
    if a.ferias_dobro > a.ferias_vencidas:
        p.error("--ferias-dobro maior que --ferias-vencidas")
    print(relatorio(a))


if __name__ == "__main__":
    main()
