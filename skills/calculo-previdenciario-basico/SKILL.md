---
name: calculo-previdenciario-basico
description: Soma o tempo de contribuição de uma lista de vínculos (CNIS, CTPS), detecta e desconta a concomitância, apura o tempo em 13/11/2019 e diz, para cada regra de transição da EC 103/2019 (pontos, idade progressiva, pedágio de 50%, pedágio de 100% e aposentadoria por idade), se o segurado já cumpre ou em que data cumpre. Use quando o advogado disser "/calculo-previdenciario-basico", "quanto tempo de contribuição ele tem", "já dá pra aposentar?", "qual regra de transição", "planejamento previdenciário", "conta o tempo do CNIS", "quando ela se aposenta".
---

# Cálculo previdenciário básico

## Regra de ouro

**Número sai do script, nunca de você.** Você monta o CSV de vínculos e roda o script. Você não
soma período, não conta dia, não decide "já tem 35 anos". Mudou um dado, rode de novo.

## Passo 1 — montar o CSV de vínculos

```
inicio,fim,descricao
01/03/1990,28/02/2000,Empresa A
01/01/1999,31/12/2010,Empresa B
01/01/2012,,Empresa C (ativo)
```

- `fim` vazio = vínculo ativo até a DER.
- Se o advogado mandar o CNIS em PDF, use `/ler-processo` (modo `texto`) para extrair o texto, monte
  o CSV com os períodos e **mostre a tabela ao advogado para conferência antes de calcular**.
  **Pare a resposta aí** e espere o "ok" (ou a correção): não rode o script na mesma resposta
  em que transcreveu o CNIS. Erro de transcrição vira data de aposentadoria errada.
  Indicador de pendência no CNIS (PEXT, AEXT-VT, PREC-MENOR-MIN...) não é decidido por você: liste
  o vínculo e pergunte se entra.
- Grave em `clientes/<cliente>/calculos/vinculos.csv`.

Pergunte também: data de nascimento, sexo (a EC 103 tem requisitos diferentes) e a DER (data de
referência; padrão hoje).

## Passo 2 — rodar

```bash
uv run ".claude/skills/calculo-previdenciario-basico/scripts/calculo_previdenciario.py" "clientes/fulana/calculos/vinculos.csv" --nascimento 10/05/1968 --sexo F --der 01/07/2025
```

Windows: troque `/` por `\` no caminho do script.

## Passo 3 — entregar

1. Grave a saída inteira, sem mudar número, em `clientes/<cliente>/calculos/tempo-contribuicao-AAAA-MM-DD.md`
   (nunca sobrescreva; se existir, acrescente a hora).
2. No chat: tempo na DER e em 13/11/2019, concomitâncias, direito adquirido e a tabela das regras
   ("JÁ CUMPRE" / "cumpre em DD/MM/AAAA" / "não se aplica"), com a ressalva de que a data futura supõe
   contribuição sem interrupção.
3. Termine **sempre** com: "Conferir antes de juntar. Não substitui o PJeCalc nem o perito."

## Regras que o script aplica (e a fonte)

| Regra | Homem | Mulher | Fonte |
|---|---|---|---|
| Pontos | 35 anos de TC; 96 pontos em 2019, +1/ano, teto 105 | 30 anos de TC; 86 em 2019, +1/ano, teto 100 | EC 103/2019, art. 15 |
| Idade progressiva | 35 anos de TC; 61 anos em 2019, +6 meses/ano, teto 65 | 30 anos; 56 em 2019, +6 meses/ano, teto 62 | EC 103/2019, art. 16 |
| Pedágio de 50% | só quem tinha mais de 33 anos de TC em 13/11/2019; TC + 50% do que faltava; sem idade | mais de 28 anos; idem | EC 103/2019, art. 17 |
| Pedágio de 100% | 60 anos + TC + 100% do que faltava em 13/11/2019 | 57 anos; idem | EC 103/2019, art. 20 |
| Idade (transição) | 65 anos, 15 de TC, 180 meses de carência | 60 em 2019, +6 meses/ano até 62 (2023) | EC 103/2019, art. 18 |
| Direito adquirido | 35 anos de TC, ou 65 anos + 180 meses, até 13/11/2019 | 30 anos, ou 60 + 180 | EC 103/2019, art. 3º |
| Concomitância | conta o tempo uma vez; somam-se os salários de contribuição | | Lei 8.213/91, art. 32 |

Quem se filiou depois de 13/11/2019 não entra em transição nenhuma: o script marca "não se aplica"
e a regra é a permanente (art. 19 da EC 103), que esta v1 não avalia.

`[conferir]` na saída: conversão em dias (ano = 365, mês = 30) e a contagem da carência por mês
civil com vínculo — confira contra o CNIS, principalmente contribuinte individual e competência
abaixo do mínimo (EC 103, art. 29).

## O que esta skill NÃO faz (v1)

Não calcula RMI (valor do benefício), média salarial nem fator previdenciário. Não converte tempo
especial, não conta tempo rural, de professor, militar ou de benefício por incapacidade, e não
avalia aposentadoria especial, da pessoa com deficiência nem a regra permanente. Não lê o CNIS
sozinho: o CSV é montado e conferido antes.

## Verificação

`python3 .claude/skills/calculo-previdenciario-basico/scripts/test_calculo_previdenciario.py` —
3 segurados conferidos à mão (pedágio de 100% já cumprido; concomitância + pontos + pedágio de 50%;
filiação depois da EC 103).
