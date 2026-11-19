---
name: revisar-peca
description: 'Revisa uma minuta de peça (sua, do estagiário ou de terceiro) pela régua de redação do escritório e devolve um relatório único: o que está limpo, os achados do mais grave ao mais leve com a correção, e o que não mexer. Use quando o advogado disser "revisa essa petição", "dá uma olhada nessa minuta", "o estagiário fez essa contestação, confere", "essa peça está boa?", "tem repetição aqui?", "enxuga essa peça", "revisa o recurso antes de eu protocolar", "confere os pedidos".'
---

# Revisar peça

A régua é a da skill `redacao-juridica`. **Leia o `SKILL.md` dela inteiro antes de revisar** e
aplique de lá: estrutura do argumento (regra, fato, conexão, consequência), hierarquia das fontes,
regra antirrepetição, travessão, os oito padrões de texto de IA, hierarquia dos pedidos e o que
nunca se corta. Esta skill não repete a régua: ela é o roteiro de uso para minuta que já existe.

## Regras

1. **Revisão não é reescrita.** Você aponta e propõe; o texto do advogado só muda se ele pedir.
   Peça alterada sai em arquivo novo, nunca por cima do original.
2. **Citação é intocável.** Transcrição de lei, ementa e trecho da parte contrária ficam como estão.
3. **Julgado citado na minuta não é julgado verificado.** Você não confirma precedente de memória.
   Se o advogado quiser conferir, use o Conector DJEN ou WebSearch **sem nome de parte**, e só
   declare "conferido" o que recuperou nesta execução, com número, data e URL. O resto vai na
   lista "julgados a conferir", sem juízo sobre se existe.
4. **Prazo não se calcula aqui.**
5. **Dado do cliente não sai da máquina.**

## Passo 1: o arquivo e o contexto

Pergunte só o que não estiver claro:

- Que peça é, quem decide (juiz, relator, examinador do INPI, conselheiro) e em que fase.
- Se a revisão é **completa** ou **só estilo** ("só enxuga", "só vê a repetição").
- Se houver, a decisão ou a peça a que esta responde (para conferir se todo ponto foi enfrentado).

Ler o texto: `.docx` com `uv run ".claude/skills/ler-processo/scripts/texto_docx.py" "<arquivo>"
--inicio 400000`; PDF com `uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" texto
"<arquivo>" --paginas 1-N`.

## Passo 2: varredura mecânica

```bash
uv run .claude/skills/redacao-juridica/auditar-peca.py "<arquivo.docx|.txt|.md>"
```

Sobre o arquivo que vai ser protocolado, nunca sobre um rascunho anterior. As leituras do resultado
(seção 3 e 4 como "conferir", repetição de legenda contra rol de documentos) estão na
`redacao-juridica`, Passo 1 da Revisão final.

## Passo 3: passe de julgamento

Na ordem, com a `redacao-juridica` na mão:

1. **Pedidos.** O principal vem primeiro? Se só o item "a" for deferido, o cliente ganha o que veio
   buscar? Um pedido por item? Sem fundamentação dentro? Instrumentais no fim?
2. **Cada tópico:** responde uma pergunta só? Abre pela regra, não por julgado? Fecha com a
   consequência?
3. **Repetição de fundamento** entre capítulos, mesmo com outras palavras.
4. **Fontes:** a lei conduz e o julgado confirma? Doutrina sem necessidade?
5. **Fatos:** documento descrito por inteiro? Narrativa sem repercussão jurídica?
6. **Os oito padrões de IA** e o vocabulário certo para quem decide.
7. Na revisão completa, com a peça respondida em mãos: algum ponto do outro lado ficou sem
   resposta?

## Passo 4: relatório único

Exatamente a forma da `redacao-juridica` (Passo 3 da Revisão final):

1. **Placar:** o que passou limpo, nomeando os padrões verificados e o resultado do auditor.
2. **Achados numerados**, do mais grave ao mais leve: onde (tópico e parágrafo), qual regra, por que
   importa neste caso, correção proposta. Várias ocorrências do mesmo padrão viram tabela.
3. **O que não mexer**, com o motivo.
4. **Julgados a conferir:** os citados na minuta que você não recuperou, com o trecho onde aparecem.

## Saída

Ao lado da minuta (ou na pasta do cliente), nunca dentro da `.claude/`:
`<nome-da-peca>-revisao-AAAA-MM-DD.md`. Nunca sobrescreva revisão anterior.

Se o advogado pedir a versão corrigida: arquivo novo `<nome-da-peca>-revisada-AAAA-MM-DD.md` (ou
`.docx` por `pandoc`, se instalado), e o auditor roda de novo sobre ele, com o placar antes e depois
no chat.

No chat: o placar em uma linha e os três achados mais graves.

## O que esta skill NÃO faz

Não protocola, não pesquisa tese nova (isso é o agente de pesquisa), não decide estratégia, não
confirma julgado que não recuperou, não calcula prazo, não altera o arquivo original.
