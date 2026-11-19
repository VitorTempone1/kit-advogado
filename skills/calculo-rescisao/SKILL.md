---
name: calculo-rescisao
description: Calcula as verbas rescisórias de um contrato CLT (saldo de salário, aviso prévio proporcional com projeção, férias vencidas e proporcionais + 1/3, 13º proporcional, FGTS da rescisão e multa de 40% ou 20%) por tipo de rescisão — sem justa causa, pedido de demissão, justa causa ou acordo do art. 484-A — e entrega a memória de cálculo linha a linha. Use quando o advogado disser "/calculo-rescisao", "calcula a rescisão", "quanto ele tem pra receber", "confere o TRCT", "verbas rescisórias", "foi mandado embora, quanto dá", "pediu demissão, o que recebe".
---

# Cálculo de rescisão

## Regra de ouro

**Número sai do script, nunca de você.** Você não soma, não multiplica, não arredonda, não
"ajusta" valor. Se o advogado pedir uma variação (outro salário, outra data, com férias vencidas),
rode o script de novo com o dado novo. Se o script der erro, mostre o erro: não calcule à mão.

## Passo 1 — colher os dados

Pergunte só o que faltar, numa mensagem só:

| Dado | Opção do script | Observação |
|---|---|---|
| Data de admissão | `--admissao dd/mm/aaaa` | da CTPS |
| Data da demissão | `--demissao dd/mm/aaaa` | dia da comunicação (aviso indenizado) ou último dia trabalhado |
| Último salário-base | `--salario 3000` | número, sem R$ e com ponto decimal (`2350.50`) |
| Tipo de rescisão | `--tipo` | `sem_justa_causa`, `pedido_demissao`, `justa_causa`, `acordo` |
| Férias vencidas não gozadas? | `--ferias-vencidas N` | quantos períodos completos; `0` se não |
| Alguma já em dobro? | `--ferias-dobro N` | as que passaram do período concessivo (art. 137 CLT) |
| Aviso | `--aviso indenizado` ou `trabalhado` | padrão: indenizado; no pedido de demissão, trabalhado. No pedido, `indenizado` = não cumpriu, gera desconto |
| Saldo do FGTS | `--saldo-fgts 9000` | do extrato; sem ele, o script **estima** e avisa |

Se o salário variava (comissão, hora extra habitual), avise que a v1 usa salário fixo e que a
média das variáveis fica fora.

## Passo 2 — rodar

```bash
uv run ".claude/skills/calculo-rescisao/scripts/calculo_rescisao.py" --admissao 10/02/2021 --demissao 15/03/2025 --salario 3000 --tipo sem_justa_causa --ferias-vencidas 0 --saldo-fgts 9000
```

No Windows (PowerShell), o mesmo com barra invertida no caminho:
`uv run ".claude\skills\calculo-rescisao\scripts\calculo_rescisao.py" ...`

## Passo 3 — entregar

1. Grave a saída do script, sem alterar número, em
   `clientes/<cliente>/calculos/rescisao-AAAA-MM-DD.md` (ou na pasta do caso que o advogado indicar).
   Nunca sobrescreva: se existir, acrescente a hora no nome.
2. No chat, mostre a tabela de verbas linha a linha (verba, conta, valor), o total bruto, o bloco do
   FGTS e as observações. Destaque toda linha marcada `[estimativa]` ou `[conferir]`.
3. Termine **sempre** com: "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."

## Regras que o script aplica (e a fonte)

| Verba | Regra | Fonte |
|---|---|---|
| Saldo de salário | salário / 30 x dias do mês; mês inteiro trabalhado = salário cheio | art. 64 CLT (mês de 30 dias) |
| Aviso prévio | 30 dias + 3 por ano completo, teto 90. Só sem justa causa (inteiro) e acordo (metade) | Lei 12.506/2011; art. 484-A, I, a, CLT |
| Projeção do aviso | o aviso indenizado conta como tempo de serviço para férias e 13º | art. 487, §1º, CLT; OJ 82 SDI-1 TST |
| Pedido sem cumprir aviso | desconto de 30 dias (a proporcionalidade não vale contra o empregado) | art. 487, §2º, CLT |
| Férias vencidas + 1/3 | salário + 1/3 por período; em dobro se passou o concessivo | arts. 129, 137 e 146 CLT; art. 7º, XVII, CF |
| Férias proporcionais + 1/3 | 1/12 por mês do período aquisitivo; fração de 15+ dias = 1/12. Devidas no pedido de demissão mesmo com menos de 1 ano; não devidas na justa causa | art. 146, par. único, CLT; Súmulas 171 e 261 TST |
| 13º proporcional | 1/12 por mês do ano com 15+ dias trabalhados; não devido na justa causa | Lei 4.090/62, arts. 1º, §2º, e 3º |
| FGTS da rescisão | 8% sobre saldo, aviso indenizado e 13º; não sobre férias indenizadas | Lei 8.036/90, art. 15; Súmula 305 TST; OJ 195 SDI-1 |
| Multa do FGTS | 40% (sem justa causa) ou 20% (acordo) sobre o saldo da conta + depósito da rescisão | Lei 8.036/90, art. 18, §1º; art. 484-A, I, b, CLT |

Pontos marcados `[conferir]` na saída: projeção no acordo (o script projeta só os dias pagos);
dias de aviso além de 30 no aviso trabalhado; saldo do FGTS estimado quando não informado.

## O que esta skill NÃO faz (v1)

Não calcula INSS nem IR: os valores são brutos. Não inclui horas extras, adicionais, médias de
variáveis, multas dos arts. 467 e 477 CLT, estabilidades, nem desconta adiantamentos ou 1ª parcela
do 13º já paga. Não atualiza valor (para isso, `/atualizacao-monetaria`). Não protocola nada.

## Verificação

`python3 .claude/skills/calculo-rescisao/scripts/test_calculo_rescisao.py` — 4 rescisões
conferidas à mão (uma de cada tipo), o teto de 90 dias e a contagem de 15 dias.
