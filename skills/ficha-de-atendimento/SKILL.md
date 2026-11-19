---
name: ficha-de-atendimento
description: Transforma a reunião com o cliente (transcrição, resumo, anotação ou áudio já transcrito) na ficha do caso, com fatos em ordem de data, partes, o que o cliente quer, riscos, próximos passos e a lista de documentos que falta pedir conforme o tipo de caso. Grava tudo no briefing.md da pasta do cliente. Use quando o advogado disser "acabei de atender", "faz a ficha do cliente", "transcrevi a reunião, organiza", "monta a ficha de atendimento", "o que eu peço de documento pra esse caso", "resume a consulta", ou mandar a transcrição de uma reunião.
---

# Ficha de atendimento

Reunião boa se perde em uma semana se não virar ficha. Esta skill lê a reunião e escreve a
ficha do caso **dentro do `briefing.md`** do cliente, que é o documento vivo do caso no kit.
Não cria um arquivo paralelo.

## Antes de escrever

1. **Leia o perfil** (`AGENTS.md` da raiz): nome do escritório e do advogado. Sem perfil,
   peça `/setup` e pare.
2. **Ache ou crie a pasta do caso**, do jeito da skill `escritorio`: organização em
   `clientes/AGENTS.md`; sem ela, `clientes/<slug>/` (nome em minúsculas, sem acento, com
   hífen). Pasta com esse nome já existe: pergunte se é o mesmo cliente.
3. **Pegue a reunião.** Nesta ordem:
   - arquivo de transcrição ou resumo que o advogado mandou (txt, docx, pdf, md);
   - gravação de áudio ou vídeo: rode antes a skill `transcrever-video`, que transcreve na
     própria máquina;
   - nada gravado: entreviste o advogado, uma pergunta por vez: o que o cliente quer, o que
     aconteceu (com datas), o que ele tem para provar, se já existe processo, se tem prazo
     correndo.
   Grave a reunião em `<pasta do caso>/reuniao/AAAA-MM-DD-<assunto>.transcricao.md` (ou
   `.resumo.md`). Se houver os dois, leia o resumo primeiro e só busque trecho na
   transcrição para tirar dúvida: transcrição inteira gasta o limite do plano.
4. Leia os documentos que já estão em `<pasta do caso>/documentos/`. Documento conta o que
   dá para provar; a reunião conta a versão do cliente.

## O que vai para o briefing

O modelo é `.claude/skills/escritorio/referencias/modelo-briefing.md`.

- **Briefing não existe:** copie o modelo, troque `{{ESCRITORIO}}`, `{{ADVOGADO}}`,
  `{{CLIENTE}}`, `{{SLUG}}`, `{{PASTA}}` e `{{DATA}}`, e preencha.
- **Briefing já existe:** leia inteiro, atualize as seções que a reunião muda e acrescente
  um checkpoint no fim. **Nunca reescreva checkpoint antigo.**

O que a ficha preenche, seção por seção do modelo:

| A ficha pede | Seção do briefing |
|---|---|
| Partes: cliente (qualificação), parte contrária, se tem advogado | 1. Identificação |
| Tipo de caso, se já tem processo, urgência | 2. Classificação da demanda |
| Fatos em ordem de data, com a fonte de cada um | 3. Fatos, linha do tempo |
| O que o cliente pediu e o que ele quer de verdade | 4. Pedido × o que quer |
| Riscos: o que só tem a palavra do cliente, prescrição, prova fraca | 3 (fatos sem prova) e 6. Pontos fracos |
| Prazo que pode estar correndo | 7. Prazos (só o fato; a data é do Conector) |
| Documentos que faltam e perguntas que ficaram | 9. Pendências |
| Honorários conversados na reunião | 10. Honorários |
| Próximos passos | checkpoint, campo "Próximo passo" |

Regras da ficha:

- **Só fato que está na reunião ou no documento.** O que não foi dito fica `⚠️ falta`.
  Não complete qualificação, data ou valor por dedução.
- **Separe o provado do só relatado.** A coluna "Provado?" da seção 3 diz "só palavra do
  cliente" sempre que não houver documento. É a lista mais importante para o advogado.
- **Prazo e prescrição:** registre o fato que dispara (data da demissão, da negativa do
  INSS, da citação). A data de vencimento só entra se vier do `calcular_prazo` do Conector
  DJEN. Sem o Conector ou sem o regime definido, escreva `⚠️ calcular` e avise.
  Risco de prescrição ou de prazo perto é a **primeira** linha da entrega.
- Teses (seção 5) ficam vazias nesta etapa, a não ser que o advogado tenha dito na reunião.
  Quem pesquisa tese são os agentes da skill `escritorio`.

## Documentos que faltam

Monte a lista de documentos pelo tipo de caso:

1. Se `clientes/AGENTS.md` tiver o **kit de documentos padrão** do escritório (o `/setup`
   grava lá), ele vence.
2. Senão, use `referencias/checklist-documentos.md` desta skill.
3. Tire da lista o que já está em `documentos/` ou já foi entregue, e acrescente o que a
   reunião mostrou ser necessário (ex.: "o print da conversa com o gerente que ela citou").

A lista vai para a seção 9 do briefing como `- [ ]`, e também na entrega, pronta para o
advogado mandar ao cliente.

## O que entregar ao advogado

Em texto, nesta ordem:

1. ⚠️ Prazo ou prescrição em risco (se houver, vem antes de tudo).
2. O caso em uma linha: área, tipo e quem contra quem.
3. Os 3 fatos que decidem o caso.
4. O que só tem a palavra do cliente.
5. A lista de documentos para pedir ao cliente, em linguagem de leigo, pronta para colar.
6. As perguntas que ficaram sem resposta na reunião.
7. Próximo passo sugerido (ex.: "rodar os agentes da skill escritorio", "gerar o kit de
   contratação").

Nada disso sai da máquina. Você não fala com o cliente; o advogado decide o que mandar.
