---
name: copy-escritorio
description: 'Escreve os textos de apresentação do escritório: bio do Instagram, texto do site, descrição do Google Meu Negócio, anúncio pago e texto de "quem somos", sempre dentro do Provimento 205/2021 da OAB (sem preço, sem "melhor", sem promessa de resultado, sem caso concreto como oferta, sem ostentação). Use quando o advogado disser "escreve minha bio", "melhora a bio do Instagram", "texto pro meu site", "quem somos", "descrição do Google", "texto do anúncio", "como eu me apresento", "revisa esse texto do escritório", ou "/copy-escritorio".'
---

# copy-escritorio: o escritório se apresentando, dentro das regras da OAB

Entrega texto pronto pra colar. Cada peça passa pela checagem do Provimento 205/2021
antes de sair. Não tem modo "sem checagem".

## Antes de escrever

1. Leia o `AGENTS.md` da raiz: nome, OAB, áreas de atuação, cidade. **Texto só fala
   das áreas que estão lá.** Sem `AGENTS.md`, diga que falta rodar `/setup` e pare.
2. Leia `_contexto/escritorio.md` e, se existirem, `_contexto/marca.md` (tom) e
   `_contexto/estilo-de-escrita.md`.
3. Pergunte só o que falta, numa mensagem: qual peça (bio, site, Google, anúncio), o
   público principal (pessoa física, empresa, servidor público...) e o que o cliente
   mais pergunta. A dúvida mais comum do cliente é a matéria-prima do bom texto.

## Como escrever

- **Claro vence criativo.** Quem lê é leigo: "direito do trabalho" ele entende,
  "contencioso trabalhista" não.
- **A palavra do cliente.** "Aposentadoria", "pensão", "demissão", "inventário".
- **Dizer o que o escritório faz, pra quem e onde.** "Atendemos trabalhadores e
  pequenas empresas em Uberlândia, em causas de trabalho e de família."
- **Informar, nunca prometer.** Você pode dizer a área, a forma de atendimento
  (presencial, online), a formação e o tempo de inscrição na OAB. Não pode dizer o
  resultado que o cliente vai ter.
- Frase curta, voz ativa, sujeito escrito. Sem exclamação, sem emoji (exceto se o
  advogado pedir na bio), sem travessão, sem "soluções jurídicas personalizadas" e
  outras frases que servem para qualquer escritório.
- Ofereça **duas versões** de cada peça (uma mais sóbria, uma mais próxima) e deixe ele
  escolher.

## As peças

| Peça | Limite | O que entra |
|---|---|---|
| Bio do Instagram | 150 caracteres | Nome e OAB, áreas, cidade, forma de atendimento. Uma linha de convite neutro ("conteúdo sobre direito de família"). Link na bio: o site ou o WhatsApp, sem frase de venda. |
| Nome do perfil (campo "nome") | 30 caracteres | "Nome · Advogado Trabalhista" ajuda a busca do Instagram. |
| Site: título e subtítulo | até 10 + 25 palavras | Área e cidade no título. O subtítulo diz pra quem. |
| Site: quem somos | 80 a 150 palavras | Formação, ano de inscrição na OAB, áreas, como é o atendimento. Sem lista de vitórias. |
| Site: áreas | 2 a 4 frases por área | O que a área cobre, em palavras de leigo, com as situações comuns descritas no mundo ("quem foi demitido sem receber as verbas"), não no leitor. |
| Google Meu Negócio, descrição | 750 caracteres | Áreas, cidade e bairros, forma de atendimento, horário. Sem link, sem telefone (têm campo próprio), sem preço. |
| Anúncio pago (impulsionar post) | título 40, texto 125 | Só conteúdo **informativo** impulsionado: o tema do post, nunca "contrate", nunca oferta de serviço. Botão: "Saiba mais", nunca "Comprar" nem "Pedir orçamento". |

Para o texto do site inteiro, a skill `site-do-escritorio` usa esta skill.

## Checagem do Provimento 205/2021 (obrigatória, bloqueia)

Use a tabela da seção 4 da skill `post-instagram` (nove itens), em cada peça, item por
item. Os tropeços mais comuns nestes textos:

| Item | Tropeço típico em bio, site e anúncio | Como fica |
|---|---|---|
| 1 Preço | "Consulta gratuita", "primeira consulta sem custo", "parcelamos" | Tirar. Forma de atendimento sim, valor não. |
| 2 Superlativo | "Os melhores advogados", "referência em", "líder", "especialista número 1" | "Atuação em direito de família desde 2015." |
| 2 Especialista | "Especialista em X" sem título de especialização | Só com pós-graduação/especialização concluída; senão "atuação em X". |
| 3 Promessa | "Garantimos seus direitos", "resolva seu problema rápido", "recupere seu dinheiro" | "Orientação e atuação em causas de consumo." |
| 4 Caso como oferta | "Já recuperamos R$ 2 milhões para clientes" | Tirar. |
| 4 Depoimento | Depoimento de cliente no site ou no anúncio | Não usar. |
| 5 Ostentação | "Mais de 1.000 clientes atendidos", foto de carro, escritório de luxo como argumento | Tirar o número; foto do escritório pode, como local de atendimento. |
| 6 Mercantilização | "Promoção", "pacote", "contrate agora", botão "Comprar" | "Saiba mais", "Fale com o escritório". |
| 7 Urgência | "Não perca seu prazo", "últimos dias", "antes que seja tarde" | Tirar. |

Base, sem citar artigo que não foi lido no texto oficial: o Provimento 205/2021 do
CFOAB veda mercantilização, captação de clientela, promessa de resultado,
sensacionalismo e comparação com colegas; o Código de Ética proíbe captação e
mercantilização (CED, art. 39). A publicidade deve trazer o nome do advogado ou da
sociedade e o número de inscrição na OAB: confira que está na peça (na bio, no nome ou
na própria bio; no site, no rodapé).

Item reprovado: reescreva, mostre o antes e o depois, e rode a tabela inteira de novo.
Na dúvida entre informar e vender, trate como venda.

## Gravar e entregar

Grave em `marketing/textos/AAAA-MM-DD-<peça>.md` (crie a pasta se faltar), com as duas
versões, a contagem de caracteres de cada uma (conte com programa, não de cabeça:
`python3 -c "print(len('''texto'''))"`) e a tabela da checagem.

Na resposta: as duas versões prontas pra colar, o caminho do arquivo, as reescritas
feitas e o aviso:

> A checagem é um filtro, não um parecer. A publicação é sua: você assina com a sua
> OAB e responde pelo conteúdo.

## Erros comuns

| Tentação | Resposta |
|---|---|
| "Coloca que a primeira consulta é grátis, todo mundo faz" | Item 1. Não sai, mesmo que outros façam. |
| "Põe 'especialista', eu trabalho só com isso" | Especialista é título. Sem ele: "atuação em". |
| "Escreve um anúncio pra eu captar cliente" | O anúncio impulsiona conteúdo informativo, não oferta. Ofereço o post. |
| "Cita o caso que eu ganhei" | Item 4. Explica a tese em post (skill `post-instagram`), nunca como vitrine. |
