---
name: calculo-horas-extras
description: Calcula horas extras a partir da jornada dia a dia (planilha ou CSV com data, entrada, saída e intervalo) e da jornada contratual — HE 50%, HE 100% em domingo e feriado, divisor 220/200/180, reflexos em DSR (Súmula 172 TST e OJ 394 na redação de 2023), 13º, férias + 1/3 e FGTS — com memória de cálculo mês a mês e dia a dia. Use quando o advogado disser "/calculo-horas-extras", "calcula as horas extras", "tenho o cartão de ponto", "quanto dá de hora extra", "liquida as HE", "monta a planilha de jornada".
---

# Cálculo de horas extras

## Regra de ouro

**Número sai do script, nunca de você.** Você monta o CSV de jornada e roda o script. Você não
soma hora, não calcula valor, não arredonda. Mudou um dado, rode de novo.

## Passo 1 — montar o CSV da jornada

O script lê um arquivo `.csv` com cabeçalho e uma linha por dia trabalhado:

```
data,entrada,saida,intervalo
03/06/2024,08:00,18:00,60
04/06/2024,08:00,19:30,01:00
09/06/2024,08:00,12:00,0
```

- `intervalo` em minutos (`60`) ou horas (`01:00`). Saída menor que entrada = passou da meia-noite.
- Aceita vírgula ou ponto e vírgula (o Excel brasileiro salva com `;`).
- Se o advogado mandar planilha `.xlsx`, peça para salvar como CSV no Excel ("Salvar como" → CSV).
  Se mandar o cartão de ponto em PDF, transcreva os dias para o CSV, **mostre ao advogado as
  primeiras linhas e peça conferência** antes de calcular: erro de transcrição vira erro de valor.
- Se a jornada é alegada ("trabalhava das 7h às 19h de segunda a sábado"), gere o CSV pela regra
  alegada para o período, e diga na saída que é jornada **alegada**, não comprovada.
- Grave o CSV na pasta do caso: `clientes/<cliente>/calculos/jornada.csv`.

## Passo 2 — os parâmetros

| Dado | Opção | Padrão |
|---|---|---|
| Salário-base mensal | `--salario 2200` | obrigatório |
| Jornada diária contratual (h) | `--jornada-diaria 8` | 8 |
| Jornada semanal contratual (h) | `--jornada-semanal 44` | 44 |
| Divisor | `--divisor 220` | semanal x 5: 44h→220, 40h→200, 36h→180 (Súmula 431 TST) |
| Feriados locais / Sexta-feira Santa / Corpus Christi | `--feriados 29/03/2024,30/05/2024` | só os nacionais fixos entram sozinhos |
| Multa do FGTS sobre o reflexo | `--multa-fgts 40` | 0 |

Pergunte ao advogado a cidade do trabalho para lembrar dos feriados locais; você não sabe a lista
de cor com segurança, então peça a ele ou deixe só os nacionais e diga isso.

## Passo 3 — rodar

```bash
uv run ".claude/skills/calculo-horas-extras/scripts/calculo_horas_extras.py" "clientes/fulano/calculos/jornada.csv" --salario 2200 --jornada-semanal 44
```

Windows: `uv run ".claude\skills\calculo-horas-extras\scripts\calculo_horas_extras.py" ...`

## Passo 4 — entregar

1. Grave a saída inteira, sem mudar número, em `clientes/<cliente>/calculos/horas-extras-AAAA-MM-DD.md`
   (nunca sobrescreva; se existir, acrescente a hora).
2. No chat: os parâmetros, a tabela por mês, os totais e as regras "[conferir]". A tabela dia a dia
   fica no arquivo (é longa); mostre só se ele pedir.
3. Termine **sempre** com: "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."

## Regras que o script aplica (e a fonte)

| Regra | Como | Fonte |
|---|---|---|
| Valor da hora | salário / divisor | art. 64 CLT; Súmula 431 TST (40h → 200) |
| HE 50% | o que passa da jornada diária; e, na semana, o que passa da semanal sem ter sido contado no dia | art. 7º, XIII e XVI, CF; art. 59 CLT |
| Tolerância | excedente de até 10 min no dia é desprezado; passou disso, conta tudo | art. 58, §1º, CLT; Súmula 366 TST |
| HE 100% | todas as horas de domingo e feriado, supondo **sem folga compensatória** `[conferir]` | Lei 605/49, art. 9º; Súmula 146 TST |
| Feriados nacionais | 01/01, 21/04, 01/05, 07/09, 12/10, 02/11, 15/11, 20/11 (desde 2024), 25/12 | Leis 662/49, 6.802/80, 14.759/23 |
| Reflexo em DSR | HE do mês / dias úteis x domingos e feriados do mês (sábado é dia útil) | Súmula 172 TST; Lei 605/49, art. 7º |
| DSR nos demais reflexos | o DSR majorado repercute em férias, 13º e FGTS só para HE feitas **a partir de 20/03/2023**; antes, não | OJ 394 SDI-1 TST, redação de 2023 (IncJulgRREmbRep-10169-57.2013.5.05.0024) |
| 13º e férias + 1/3 | 1/12 do valor mensal (HE + DSR que reflete); férias x 4/3 `[conferir: aproximação, o PJeCalc usa a média do período]` | Súmula 45 e 347 TST; art. 142, §5º, CLT |
| FGTS | 8% sobre HE, DSR que reflete e 13º; férias indenizadas não `[conferir férias gozadas]` | Súmula 63 TST; OJ 195 SDI-1 |

## O que esta skill NÃO faz (v1)

Adicional noturno e hora reduzida, intervalo intrajornada suprimido (art. 71, §4º), intervalo
interjornada, banco de horas e compensação, reflexo em aviso prévio, salário variável, INSS, IR,
correção e juros (para isso, `/atualizacao-monetaria`). Não lê PDF de cartão de ponto sozinha: o
CSV é montado e conferido antes.

## Verificação

`python3 .claude/skills/calculo-horas-extras/scripts/test_calculo_horas_extras.py` — 3 meses
conferidos à mão (excedente diário + domingo; excedente semanal + tolerância; virada da OJ 394).
