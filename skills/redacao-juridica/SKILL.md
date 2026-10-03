---
name: redacao-juridica
description: 'Padrão OBRIGATÓRIO de redação jurídica do escritório. Use SEMPRE que for redigir, revisar ou reduzir qualquer peça: petição inicial, contestação, manifestação, impugnação, recurso, embargos, agravo, apelação, parecer, memorial, notificação ou defesa administrativa (INPI, OAB, tribunal de contas, processo disciplinar). Também ao revisar minuta de terceiro, ao "enxugar" peça longa, ao "montar a peça", "escreve a petição", "redige a manifestação", "revisa essa minuta". Define estrutura do argumento (regra, fato, conexão, consequência), hierarquia das fontes, tamanho dos tópicos, uso de jurisprudência, proibição de travessão, regra antirrepetição e a HIERARQUIA DOS PEDIDOS (principal primeiro, decrescente por importância).'
---

# Redação jurídica técnica, padrão do escritório

Peça altamente técnica, objetiva, persuasiva, de leitura fácil. A prioridade é
**convencer quem decide**, não demonstrar erudição.

Antes de escrever, identifique o destinatário e escreva para ele. Juiz, relator,
assessor, examinador do INPI, conselheiro, comissão processante. Nunca use
"julgador", "Vossa Excelência" ou vocabulário de processo judicial em defesa
administrativa: numa manifestação do INPI quem lê é o **examinador**, e o que o
convence é a lei, o Manual de Marcas e o assentamento do próprio Instituto.

**Qualidade argumentativa prevalece sobre quantidade de páginas.** Sempre que
der para reduzir o texto sem perda de conteúdo jurídico, a versão mais concisa
vence. Isso prevalece em toda petição, recurso, manifestação e parecer.

---

## Princípios

**Clareza.** Um parágrafo, uma ideia. Períodos curtos. Nada rebuscado. O leitor
entende o argumento na primeira leitura.

**Objetividade.** Todo argumento tem finalidade prática. Nunca escreva para
preencher páginas. O que cabe em três parágrafos jamais ocupa oito; o que cabe
em uma frase não ocupa cinco.

**Densidade.** Texto curto não é texto superficial. Cada parágrafo carrega
conteúdo jurídico relevante, decorrente de lei, jurisprudência ou prova
produzida.

**Linguagem técnica.** Sem adjetivação desnecessária, drama, emoção, ironia ou
ataque pessoal. A força vem da argumentação.

---

## Repetição: só quando for estritamente necessária

Nunca repetir o mesmo fundamento com palavras diferentes. Demonstrado o fato ou
o fundamento, avance. Não repita artigo, julgado, fato, pedido nem conclusão.

A regra vale **entre capítulos, não só dentro deles**. Repetição textual espalhada
em tópicos diferentes é a causa número um de peça inchada: cada capítulo reabre a
mesma tese com outras palavras e a peça dobra de tamanho sem ganhar um argumento.

Como resolver quando a mesma matéria reaparece:

- **Remissão em vez de reescrita.** "Como demonstrado no capítulo IV", "pelas
  razões do item II.2". Uma linha substitui um parágrafo.
- **Um fundamento, um lugar.** Cada tese tem um capítulo dono. Os outros
  capítulos usam a conclusão dela, não refazem a demonstração.
- **Citação repetida.** Transcrever o dispositivo, o julgado ou o trecho da peça
  adversa **uma vez**. Nas demais, referir pelo nome ("o art. 124, XIX",
  "o item 5.11.2 do Manual", "o precedente do TRF2 já citado").

A repetição só se justifica quando **muda a função do argumento**: o que foi
demonstrado como fato no mérito pode ser retomado como premissa de um pedido, e
o que fundamenta preliminar pode reaparecer como reforço subsidiário. Nesses
casos, retome em uma frase, nunca no parágrafo original.

Antes de fechar, procure literalmente as frases repetidas. Se dois parágrafos
dizem a mesma coisa, um deles é remissão ou sai.

---

## Travessão: nunca

**Nenhuma peça sai com travessão (—) nem com meia-risca (–).** Regra dura, sem
exceção, incluindo título, legenda de figura, rol de documentos e rodapé.

Substituir, nesta ordem de preferência: ponto (abre frase nova), vírgula (aposto
curto), dois-pontos (introduz explicação), parênteses (aparte verdadeiro). Se
nenhum servir, reescreva o período.

Motivos: o travessão é o sinal mais confiável de texto gerado por IA, e em peça
jurídica ele quase sempre esconde um período mal construído que ficaria melhor
partido em dois.

Também vale para hífen duplo (`--`) usado como travessão. Hífen de palavra
composta (guarda-chuva, jurídico-administrativo) continua normal.

Conferência mecânica antes de entregar:

```bash
grep -c "—\|–" <arquivo>        # tem que responder 0
```

Em peça gerada por script, o autoteste do gerador é que trava isso, e a checagem
tem que rodar sobre o `.docx` final, nunca só sobre o fonte. Já aconteceu de o
travessão entrar pelo modelo de papel timbrado e não pelo texto da peça.

---

## Escrever como pessoa, não como IA

Peça com cara de texto gerado por máquina perde autoridade antes de o juiz chegar
ao mérito. Os oito padrões abaixo são os que de fato aparecem em peça. Varrer
todos antes da revisão final.

| Padrão | Como sai na peça | Correção |
|---|---|---|
| Travessão | vide seção acima | ponto, vírgula, dois-pontos |
| Regra de três | "clara, evidente e inequívoca" | um adjetivo só, o mais preciso |
| Variação elegante | requerentes, autores, demandantes, postulantes, tudo na mesma página | fixar **um** termo por parte e repetir |
| Paralelismo negativo | "não se trata apenas de X, mas de Y" | afirmar direto o que é |
| Ritmo uniforme | todo período com o mesmo tamanho | alternar frase curta e longa |
| Fecho positivo genérico | "medida que se impõe em nome da justiça" | conclusão concreta, ligada ao pedido |
| Vocabulário inflado | "desempenha papel fundamental", "no cenário atual" | dizer o que faz, com o verbo simples |
| Negrito mecânico | meia página em negrito | grifo só na frase que decide o tópico |

Dois limites:

- **Escrever como pessoa não é escrever com personalidade.** Em peça, parecer e
  contrato, o registro neutro e direto já é a voz humana correta. Nada de primeira
  pessoa, opinião pessoal ou coloquialismo.
- **Não mexer em citação.** Transcrição de lei, ementa, súmula, Manual ou trecho
  da peça adversa é literal. Nunca reescrever o que está entre aspas ou em bloco
  de citação, mesmo que contenha travessão ou padrão de IA.

---

## Revisão final: uma passada só

A revisão é **uma passada só**, nesta ordem, e produz **um** relatório.

### Passo 1: varredura mecânica

```bash
uv run .claude/skills/redacao-juridica/auditar-peca.py <arquivo.docx|.txt|.md>
```

Conta o que se conta sem julgar: travessão, tique de apassivadora (`Registre-se`,
`Esclareça-se`, `Antecipe-se`…), tratamento das partes inconsistente, repetição
literal entre parágrafos, metacomentário, tropo de autoridade, vocabulário
inflado, hedging e filler. Roda sobre o `.docx` FINAL, nunca sobre o fonte.

Duas leituras que o script não faz sozinho:

- **Repetição de legenda contra rol de documentos é por desenho.** O rol descreve
  o mesmo documento que a legenda descreve; não é achado. Número de processo, RPI,
  CNPJ e data já saem filtrados.
- **Tratamento das partes** entra como "conferir", não como erro. Minúscula pode
  ser substantivo comum legítimo ("titular do registro nº X") e o singular pode
  designar um dos litisconsortes ("o primeiro Requerente"). O que importa é
  **se a forma minoritária está nomeando parte errada**: peça que sustenta na
  preliminar que Fulano não é parte e depois o chama de "a Requerente" entrega
  contradição de graça.

### Passo 2: passe de julgamento

O que exige leitura, com a tabela de padrões acima na mão: regra de três forçada,
paralelismo negativo, variação elegante de sinônimo, ritmo uniforme, negrito
mecânico, fecho positivo genérico, e **repetição de fundamento que não é literal**
(o mesmo argumento refeito com outras palavras em outro capítulo, que nenhum grep
pega).

### Passo 3: relatório único

Sai nesta forma, e só esta:

1. **Placar.** O que passou limpo, nominando os padrões verificados.
2. **Achados numerados**, do mais grave ao mais leve, cada um com: onde está, qual
   padrão violou, por que importa **no caso**, e a correção proposta em tabela
   quando forem várias ocorrências.
3. **O que não mexer**, com o motivo. Obrigatório: é o que impede a revisão de
   virar poda cega.

### O que nunca sai numa revisão de estilo

- A frase de fecho que carrega a tese do capítulo. Uma por capítulo é ritmo, não
  vício; o §31 pune sequência de frases de efeito, não uma por seção.
- Grifo que marca a frase decisiva do tópico, e itálico de transcrição: apagá-los
  destrói a fronteira entre o que se cita e o que se afirma.
- Número concreto trocado por adjetivo ("nenhuma das doze rubricas" nunca vira
  "as rubricas").
- Sujeito da frase quando o sujeito é a autoridade que decide ("este Instituto
  aplicou o registro para indeferir" nunca vira "o registro fundamentou o
  indeferimento").

---

## Estrutura de cada argumento

Ordem fixa. **Jamais inverter.**

1. **Regra jurídica.** "O art. 169 da Lei nº 9.279/96 exige a demonstração do legítimo interesse."
2. **Fato relevante.** "Os requerentes não são titulares dos registros invocados."
3. **Conexão fato e norma.** "Não sendo titulares, incumbia-lhes demonstrar qual seria o legítimo interesse exigido pela lei."
4. **Consequência jurídica.** "Ausente essa demonstração, o pedido não pode ser conhecido."

## Tópicos

Cada tópico responde **uma** pergunta jurídica. "Há legítimo interesse?"
responde, próximo. "Houve prova?" responde, próximo. Um tópico não vira parecer
completo.

Tamanho de referência:

| Parte | Extensão |
|---|---|
| Preliminar | ½ a 1 página |
| Mérito, por fundamento relevante | 1 a 2 páginas |

Nunca cinco ou seis páginas sobre a mesma matéria.

---

## Fundamentação, hierarquia das fontes

1. Constituição Federal
2. Lei específica
3. Código aplicável
4. Regulamentos
5. Manual administrativo (quando houver)
6. Jurisprudência

**Nunca inverter.** A legislação conduz a argumentação; a jurisprudência apenas
confirma.

**Jurisprudência.** Só precedente real, verificável e pertinente. O julgado vem
de busca feita agora, seja por WebSearch/WebFetch, seja pelas ferramentas do
Conector DJEN — que é assinatura à parte. Se a ferramenta do Conector não estiver
na máquina, diga uma vez "isto precisa do Conector DJEN, peça acesso na mentoria"
e siga pela busca na web; sem fonte recuperada, o trecho vai marcado
`⚠️ NÃO VERIFICADO` e fica fora da tese principal. Nunca julgado
inventado, sem relação com o caso, nem excesso de julgados. Um ou dois
precedentes fortes valem mais que dez fracos. Nunca abrir tópico com
jurisprudência: primeiro a lei, depois a aplicação ao caso, só então o julgado
confirmando.

Ver `feedback-precedente-recente-valido` na memória: só julgado de até 5 anos e
de pé; nunca precedente antigo havendo recente em sentido contrário.

**Doutrina.** Não usar, salvo pedido expresso ou quando a doutrina invocada pelo
outro lado responder contra ele.

---

## Fatos e provas

Narrar só o fato indispensável. Fora: narrativa histórica desnecessária,
cronologia irrelevante, detalhe sem repercussão jurídica.

Jamais descrever documento por inteiro. Extraia o fato juridicamente relevante e
emende a consequência: "O documento demonstra que… , de modo que…". Quatro
páginas narrando um documento é erro.

Cada argumento responde: **por que isso importa juridicamente?** Sem resposta, o
argumento sai.

---

## Pedidos, hierarquia obrigatória

Os pedidos são a parte mais lida da peça. Precisam ficar **evidentes e claros a
qualquer leitor**, do juiz ao servidor de secretaria, do examinador ao
conselheiro, não só a advogado.

Regras:

- **Ordem por importância.** O pedido **principal** vem primeiro. O segundo mais
  importante vem em segundo, e assim sucessivamente, em ordem decrescente.
  A ordem da lista É a hierarquia, e quem decide lê como tal.
- Pedido **subsidiário** (o "caso não se entenda assim") vem imediatamente
  depois do pedido principal a que se subordina, marcado como subsidiário.
- Cada pedido em item próprio, numerado (a, b, c… ou 1, 2, 3…). Um item, um
  pedido, nunca dois pedidos no mesmo item.
- Pedido objetivo e completo: verbo, o que se quer, contra quem, com que
  extensão. Quem lê só o rol de pedidos entende o que se está requerendo.
- **Sem fundamentação dentro do pedido.** Sem explicação, sem citação de artigo,
  sem repetir argumento do mérito. A fundamentação ficou no mérito.
- Sem repetição entre itens.
- Requerimentos instrumentais (produção de prova, intimação, gratuidade,
  prioridade, honorários) vêm **depois** dos pedidos de mérito, em bloco
  próprio. Nunca antes.

Antes de fechar, confira: se for deferido apenas o item "a", o cliente consegue o
que veio buscar? Se não, o item "a" não é o pedido principal, reordene.

---

## Estilo

Transmitir segurança. Nunca parecer hesitante. Fora "parece", "talvez",
"possivelmente", "em tese" quando há certeza jurídica.

Preferir: "Não há demonstração." / "Não se verifica." / "Os documentos
comprovam." / "Incide o art. …" / "Não merece prosperar." / "É suficiente para
concluir."

Argumentação progressiva: cada tópico fortalece o seguinte, sem voltar ao mesmo
fundamento. A peça conduz quem decide à conclusão.

---

## Regra de ouro, revisão final

Antes de entregar, percorrer **parágrafo por parágrafo** perguntando:

> Este parágrafo acrescenta algum fundamento novo?

**Não, apaga o parágrafo.**

## Checklist de fechamento

- [ ] Todo tópico segue regra, fato, conexão, consequência
- [ ] Nenhum tópico responde mais de uma pergunta jurídica
- [ ] Tópicos dentro da extensão de referência
- [ ] Vocabulário compatível com o destinatário (nada de "julgador" em peça administrativa)
- [ ] Hierarquia das fontes respeitada; nenhum tópico abre com julgado
- [ ] Todo precedente citado é real, verificável, de até 5 anos e de pé
- [ ] Nenhum documento descrito por inteiro
- [ ] Nenhum fundamento repetido com outras palavras, entre capítulos inclusive
- [ ] Matéria que reaparece entrou por remissão, não por reescrita
- [ ] Cada dispositivo, julgado e trecho adverso transcrito uma única vez
- [ ] `auditar-peca.py` rodado no arquivo FINAL, seções 1, 2, 5, 6, 7 e 8 zeradas
- [ ] Seções 3 e 4 do auditor conferidas uma a uma (podem ser falso positivo)
- [ ] Os oito padrões de texto de IA varridos, sem reescrever citação
- [ ] Citações preservadas literalmente, sem reescrita
- [ ] Pedidos: principal primeiro, ordem decrescente de importância
- [ ] Um pedido por item, numerado, sem fundamentação dentro
- [ ] Requerimentos instrumentais em bloco separado, ao final
- [ ] Regra de ouro aplicada em cada parágrafo

Resultado: peça técnica, objetiva, elegante, persuasiva, fundamentada, sem
prolixidade nem repetição, com fluidez de leitura, escrita como advogado
experiente que domina a matéria e transmite segurança sem excesso de texto.
