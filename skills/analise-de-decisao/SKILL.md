---
name: analise-de-decisao
description: 'Lê uma decisão, sentença ou acórdão e devolve: o que foi decidido (dispositivo), os fundamentos, o que o cliente ganhou e perdeu, o recurso cabível e o prazo, este calculado só pela ferramenta do Conector, nunca de cabeça. Use quando o advogado disser "saiu a sentença, analisa", "o que o juiz decidiu?", "ganhamos ou perdemos?", "cabe recurso dessa decisão?", "qual o recurso e o prazo?", "lê esse acórdão", "a liminar foi negada, e agora?", "resume essa decisão pro cliente", "vale a pena recorrer?".'
---

# Análise de decisão

O advogado traz uma decisão. Você diz o que ela decidiu, por quê, o saldo para o cliente, o que
cabe contra ela e de onde sai o prazo.

## Regras

1. **Saída é MINUTA**, para o advogado conferir nos autos.
2. **Prazo nunca de cabeça.** Data de vencimento só sai da ferramenta `calcular_prazo` do Conector
   DJEN. Sem a ferramenta, escreva "calcule pelo Conector ou à mão" e **não escreva data nenhuma**,
   nem "aproximadamente", nem "por volta de". Sem regime de contagem definido no perfil, pergunte
   antes de calcular.
3. **Nada sem âncora.** Todo ponto do dispositivo e dos fundamentos traz a página ou o trecho de
   onde saiu. O que você não achou vai para "Não localizei".
4. **Julgado só verificado.** Precedente citado na decisão é reproduzido como "citado pela decisão",
   nunca como pesquisa sua. Precedente que você trouxer para o recurso só entra recuperado nesta
   execução (Conector ou WebSearch, sem nome de parte), com número, data e URL; senão
   `⚠️ NÃO VERIFICADO`.
5. **Dado do cliente não sai da máquina.** Nenhuma busca com nome de parte ou número do processo,
   exceto as ferramentas do Conector feitas para isso.

## Passo 1: ler

- PDF: `uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" texto "<arquivo>" --paginas 1-N`
  (decisão longa ou dentro dos autos: rode antes o modo `mapa` e leia só a decisão).
- `.docx`: `uv run ".claude/skills/ler-processo/scripts/texto_docx.py" "<arquivo>" --inicio 400000`.
- Se o advogado só tem o número do processo e o Conector está ligado: `consultar_intimacoes` ou
  `ler_intimacao` trazem o teor publicado.

Pergunte, se não estiver claro: **qual parte é o cliente**, e a data da intimação (ou se veio pelo
Diário, a data de disponibilização).

## Passo 2: identificar

1. **Tipo do ato:** despacho, decisão interlocutória, sentença, decisão monocrática de relator,
   acórdão. O tipo define o recurso. Na dúvida, diga a dúvida.
2. **Rito e justiça:** comum (CPC), Juizado Especial, trabalhista, criminal. Confira com o perfil
   do escritório (`AGENTS.md`, regime de contagem).
3. **Dispositivo:** o que foi decidido, item a item, com o que foi julgado procedente, improcedente,
   extinto sem mérito, deferido, indeferido. Condenação em honorários e custas.
4. **Fundamentos:** por que, em tópicos curtos, ligando cada fundamento ao item do dispositivo.
   Marque fundamento que a decisão não enfrentou (pedido ou tese da parte sem resposta): é matéria
   de embargos de declaração.

## Passo 3: saldo para o cliente

| Pedido / ponto | Resultado para o cliente | Onde |
|---|---|---|
| | ganhou / perdeu / em parte / não decidido | p. ou trecho |

Sucumbência recíproca, honorários e efeito imediato (cumprimento provisório, tutela mantida ou
revogada) entram aqui.

## Passo 4: recurso cabível

Indique o recurso, o dispositivo e o número de dias que a lei dá. Quadro de partida (confira o
texto pelo `buscar_legislacao` quando o Conector estiver ligado):

| Rito | Ato | Recurso | Dispositivo | Dias |
|---|---|---|---|---|
| CPC | Sentença | Apelação | CPC 1.009 | 15 (CPC 1.003, § 5º) |
| CPC | Interlocutória do rol | Agravo de instrumento | CPC 1.015 | 15 |
| CPC | Interlocutória fora do rol | Preliminar de apelação ou contrarrazões | CPC 1.009, § 1º | (sem recurso agora) |
| CPC | Monocrática de relator | Agravo interno | CPC 1.021 | 15 |
| CPC | Acórdão (lei federal / Constituição) | REsp / RE | CF 105, III / CF 102, III; CPC 1.029 | 15 |
| CPC | Omissão, contradição, obscuridade, erro material | Embargos de declaração | CPC 1.022 | 5 (CPC 1.023) |
| JEC | Sentença | Recurso inominado | Lei 9.099/95, art. 41 | 10 (art. 42) |
| JEC | Omissão, contradição, obscuridade | Embargos de declaração | Lei 9.099/95, art. 49 | 5 |
| Trabalho | Sentença | Recurso ordinário | CLT 895 | 8 |
| Trabalho | Omissão, contradição | Embargos de declaração | CLT 897-A | 5 |
| Penal | Sentença | Apelação | CPP 593 | 5 |
| Penal | Hipóteses do art. 581 | Recurso em sentido estrito | CPP 581 e 586 | 5 |
| Penal | Omissão, ambiguidade | Embargos de declaração | CPP 382 e 619 | 2 |

Fora desse quadro (mandado de segurança, execução fiscal, eleitoral, recurso para tribunal
superior com regra própria), não preencha de memória: `buscar_legislacao` ou `[conferir]`.

Diga também se **cabe** e se **convém**: interesse recursal, custo (preparo, honorários recursais
do CPC 85, § 11), chance pelo fundamento da decisão. Recomendação curta; a decisão é do advogado.

## Passo 5: prazo

Com o Conector ligado, chame `calcular_prazo` com:

- `data`: a data de disponibilização, publicação ou ciência (e diga qual em `natureza`);
- `dias`: os dias do Passo 4;
- `regime`: do perfil do escritório (`cpc`, `clt`, `jec`, `cpp-processual`...). Sem regime no
  perfil, **pergunte**;
- `tribunal` ou `uf`, e `parte_publica`, `litisconsortes`, `autos` e `recurso` quando couber.

Copie a data e o aviso que a ferramenta devolver, e diga: "confira no sistema do tribunal". Se a
ferramenta devolver horário limite, ele vai junto.

Sem o Conector: "Este cálculo precisa do Conector DJEN. Calcule pelo Conector ou à mão, a partir
de <data da intimação>, <N> dias, regime <regime>." Nenhuma data além dessa.

## Saída

Ao lado da decisão (ou na pasta do cliente, organização do `clientes/AGENTS.md`), nunca dentro da
`.claude/`: `<nome-da-decisao>-analise-AAAA-MM-DD.md`. Nunca sobrescreva análise anterior.

```markdown
# MINUTA: análise de decisão
Conferir nos autos antes de usar.

Decisão: <tipo> · <órgão> · <data> · cliente: <parte>
## Em uma linha
## O que foi decidido (dispositivo)
## Por quê (fundamentos)
## Saldo para o cliente
## Recurso cabível
## Prazo
## Não localizei
```

No chat: a linha-resumo, o saldo, o recurso e o prazo (ou o aviso de que precisa do Conector).

Se o advogado pedir **resumo para o cliente**: texto à parte, em linguagem simples, sem estratégia
e sem data de prazo que não tenha saído da ferramenta.

## O que esta skill NÃO faz

Não calcula prazo de cabeça, não redige o recurso (isso é `redacao-juridica` e os agentes jurídicos),
não grava prazo em agenda sem o advogado aceitar, não confirma julgado que não recuperou.
