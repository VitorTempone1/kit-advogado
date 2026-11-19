---
name: atualizacao-monetaria
description: Atualiza um valor entre duas datas com os índices oficiais do Banco Central (IPCA-E, INPC, IPCA, SELIC, TR e taxa legal), em três modos — um índice só, trabalhista (ADC 58/59 do STF e a virada da Lei 14.905/2024) e cível (Lei 14.905/2024) — e entrega a memória de cálculo mês a mês. Use quando o advogado disser "/atualizacao-monetaria", "atualiza esse valor", "corrige pelo IPCA-E", "quanto dá hoje", "aplica SELIC", "atualiza o crédito trabalhista", "correção e juros", "atualiza a condenação".
---

# Atualização monetária

## Regra de ouro

**Número sai do script, nunca de você.** O script busca os índices no Banco Central e faz a conta.
Você não estima índice, não "arredonda a SELIC", não completa mês que falta. Se o script parar
porque um índice ainda não saiu, diga isso e ofereça rodar até o mês anterior.

## Passo 1 — qual regra? O ADVOGADO escolhe

Não escolha por ele. Pergunte o que a decisão (ou o contrato) mandou e mostre as três opções:

| Modo | Quando | O que aplica |
|---|---|---|
| `indice` | a decisão fixou um índice só, ou é conta de conferência | um índice (`--indice IPCA-E`, `INPC`, `IPCA` ou `SELIC`); juros simples opcionais (`--juros-desde` + `--juros-antes 1` = 1% a.m.) |
| `trabalhista` | crédito trabalhista seguindo ADC 58/59 | antes do ajuizamento: IPCA-E + juros TR; do ajuizamento a 08/2024: SELIC; de 09/2024 em diante: IPCA + taxa legal |
| `civel` | dívida civil, Lei 14.905/2024 | até 08/2024: índice escolhido (`--indice`, padrão INPC) + juros escolhidos (`--juros-antes 1` ou `SELIC`); de 09/2024 em diante: IPCA + taxa legal |

Se a decisão manda algo que nenhum modo cobre (outra tabela de tribunal, juros compostos,
pro rata dia), diga que o script não cobre e não force o encaixe.

## Passo 2 — rodar

```bash
uv run ".claude/skills/atualizacao-monetaria/scripts/atualizacao_monetaria.py" --valor 10000 --inicio 15/03/2022 --fim 01/11/2026 --modo trabalhista --ajuizamento 10/05/2023
```

Outros exemplos:

```bash
# cível: INPC + 1% a.m. desde a citação até 08/2024, depois Lei 14.905
uv run ".claude/skills/atualizacao-monetaria/scripts/atualizacao_monetaria.py" --valor 5000 --inicio 10/01/2023 --fim 01/11/2026 --modo civel --indice INPC --juros-desde 20/04/2023 --juros-antes 1

# só IPCA-E, sem juros
uv run ".claude/skills/atualizacao-monetaria/scripts/atualizacao_monetaria.py" --valor 1000 --inicio 01/01/2024 --fim 01/04/2024 --modo indice --indice IPCA-E
```

Windows: troque `/` por `\` no caminho do script. Precisa de internet (só `api.bcb.gov.br`; nenhum
dado do cliente vai na consulta, só datas e o número da série).

## Passo 3 — entregar

1. Grave a saída inteira, sem mudar número, em `clientes/<cliente>/calculos/atualizacao-AAAA-MM-DD.md`
   (nunca sobrescreva; se existir, acrescente a hora).
2. No chat: o modo escolhido, o resultado (original, corrigido, juros, total) e as regras `[conferir]`.
   A tabela mês a mês fica no arquivo.
3. Termine **sempre** com: "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."

## Regras e fontes

- **Índices**: Banco Central, SGS — IPCA-E 10764, INPC 188, IPCA 433, SELIC mensal 4390,
  TR mensal 7811, taxa legal 29543 (Res. CMN 5.171/2024: SELIC menos IPCA, nunca negativa).
  Códigos conferidos na API em 19/11/2026.
- **Convenção de mês**: o mês da data inicial entra inteiro e o mês da data final não entra; sem
  pro rata dia. `[conferir com a tabela do tribunal]`
- **Correção**: IPCA-E, INPC e IPCA se acumulam por multiplicação (composto).
- **SELIC e juros**: soma simples das taxas mensais; os juros incidem sobre o valor já corrigido.
- **Trabalhista**: STF, ADC 58 e 59 (e embargos de declaração): IPCA-E e juros do art. 39, caput,
  Lei 8.177/91 (TR) na fase pré-judicial, SELIC a partir do ajuizamento. Depois da Lei 14.905/2024
  (vigência 30/08/2024): IPCA + taxa legal — TST, SDI-1, E-ED-RR-713-03.2010.5.04.0029 (out/2024).
  `[conferir]`: o mês do ajuizamento já entra como SELIC; a fase pré-judicial depois de 30/08/2024
  tem leitura divergente; algumas ementas do mesmo julgado falam em IPCA-E (e não IPCA) depois de
  30/08/2024 — o script usa IPCA, que é o do art. 389 do CC. Se a decisão mandar IPCA-E, use o modo `indice`
  por trechos (uma rodada por fase) e diga ao advogado que o modo trabalhista não cobre essa leitura.
- **Cível**: arts. 389, par. único, e 406, §§1º a 3º, do CC (Lei 14.905/2024). Antes dela, a taxa do
  art. 406 era disputada (1% a.m. pelo art. 161, §1º, CTN, ou SELIC pelo STJ no REsp 1.795.982):
  por isso o advogado escolhe com `--juros-antes`.

## O que esta skill NÃO faz

Pro rata dia, juros compostos, tabelas próprias de tribunal (ICGJ, tabela prática do TJSP),
correção de parcelas vencidas mês a mês (rode uma vez por parcela), INSS, IR, honorários, multa
do art. 523 CPC. Não decide qual regra a decisão manda: isso é do advogado.

## Verificação

`python3 .claude/skills/atualizacao-monetaria/scripts/test_atualizacao_monetaria.py` — sem rede,
com índices fixos: IPCA-E real de jan-mar/2024, trabalhista atravessando as três fases, cível com
1% e com SELIC antes da Lei 14.905, e mês sem índice que tem que parar a conta.
