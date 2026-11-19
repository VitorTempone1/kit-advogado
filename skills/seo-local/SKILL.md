---
name: seo-local
description: 'Ajuda o escritório a aparecer quando alguém procura "advogado perto de mim" ou "advogado trabalhista em <cidade>" no Google e no Google Maps: monta e revisa o Perfil da Empresa no Google (o antigo Google Meu Negócio), escolhe categorias, orienta fotos, avaliações dentro da ética da OAB e palavras-chave locais pro site. Use quando o advogado disser "quero aparecer no Google", "meu escritório não aparece no Maps", "Google Meu Negócio", "perfil da empresa no Google", "como pedir avaliação", "respondo essa avaliação como?", "SEO", "palavra-chave", ou "/seo-local".'
---

# seo-local: aparecer pra quem procura advogado na cidade

Entrega um plano de ação com texto pronto e um passo a passo pra fazer no celular ou
no computador. Quem clica nos botões do Google é o advogado; esta skill não entra em
conta nenhuma.

## Antes

1. Leia o `AGENTS.md` da raiz (nome, OAB, áreas, cidade) e `_contexto/escritorio.md`.
2. Pergunte numa mensagem só o que faltar: o escritório já tem perfil no Google? Tem
   endereço onde recebe cliente, ou atende só online? Quais bairros ou cidades atende?
   Tem site?

## 1. Perfil da Empresa no Google

Passo a passo (o advogado faz, você acompanha):

1. Entrar em `google.com/business` com a conta Google do escritório (não a pessoal,
   se puder separar) e procurar o nome do escritório. Se já existir, "reivindicar".
2. **Nome:** exatamente o nome do escritório, como na placa e na OAB. Acrescentar
   "advogado trabalhista Uberlândia" no nome é contra as regras do Google e pode
   derrubar o perfil.
3. **Categoria principal:** a mais específica que existir pra área mais forte
   ("Advogado trabalhista", "Advogado de família", "Advogado previdenciário",
   "Advogado criminalista"). Se não houver, "Advogado" ou "Escritório de advocacia".
   **Categorias secundárias:** as outras áreas do `AGENTS.md`, até umas quatro. Só
   área que o escritório realmente atende.
4. **Endereço:** se recebe cliente, o endereço. Se atende só online ou na casa do
   cliente, escolha "área de atendimento" e esconda o endereço. Endereço de
   coworking só se for o local real de atendimento.
5. **Telefone, site, horário:** iguais aos do site e do Instagram, letra por letra. O
   Google compara; dado diferente em cada lugar pesa contra.
6. **Descrição (750 caracteres):** peça à skill `copy-escritorio`. Sem link, sem preço.
7. **Verificação:** o Google pede vídeo do local, cartão postal ou ligação. Siga o
   que ele oferecer; sem verificação o perfil não aparece.

## 2. Fotos

- Fachada (como o cliente reconhece o prédio), entrada, recepção, sala de reunião,
  o advogado e a equipe com roupa de trabalho. Logo e uma foto de capa.
- Foto real, clara, de dia. Celular na horizontal serve.
- **Não entra:** documento ou processo aparecendo, cliente reconhecível, carro, objeto
  de luxo como argumento (ostentação, item 5 da checagem da `post-instagram`).
- Uma ou duas fotos novas por mês mantêm o perfil vivo.

## 3. Avaliações, dentro da ética da OAB

O que pode e o que não pode:

| Pode | Não pode |
|---|---|
| Ter o link de avaliação à mão e mandar a quem perguntar como ajudar | Pedir avaliação em massa, em lista de transmissão ou pra quem não é cliente |
| Ao encerrar o atendimento, um pedido discreto e sem insistência, se o advogado se sentir confortável | Oferecer qualquer coisa em troca (desconto, brinde, prioridade) |
| Responder toda avaliação, educado e genérico | Comprar avaliação, pedir a parente ou amigo que não foi cliente, avaliar a si mesmo |
| Denunciar ao Google avaliação falsa ou ofensiva | Responder brigando, ou expor qualquer detalhe do caso |

**Sigilo vem antes de tudo na resposta.** A resposta nunca confirma que a pessoa é ou
foi cliente, nunca menciona o caso, o processo, o valor ou o resultado. Isso vale
também pra avaliação negativa, mesmo injusta.

Modelos (ofereça, o advogado adapta):

- Positiva: "Obrigado pelas palavras. Ficamos à disposição."
- Negativa: "Lamentamos a sua impressão. Por dever de sigilo profissional, não
  comentamos atendimentos aqui. Se quiser conversar, o escritório está à disposição
  pelo telefone do perfil."

Depoimento de cliente **não** se copia do Google pro site nem pro Instagram.

## 4. Postagens no perfil do Google

O perfil aceita postagens, como o Instagram. Reaproveite os posts informativos já
feitos pela `post-instagram` (texto curto e a capa). Mesma checagem do Provimento
205/2021; nada de "oferta" nem "evento" de venda.

## 5. Palavras-chave locais

Monte a lista com o advogado, juntando: **área** (trabalhista, família, previdenciário,
"aposentadoria", "pensão alimentícia", "divórcio") + **lugar** (cidade, bairro,
"perto de mim"). Exemplos: "advogado de família em Contagem", "advogado aposentadoria
INSS Uberlândia".

Onde cada palavra vai:

- **Site:** título da página (`<title>`), título principal, texto de cada área, rodapé
  com endereço. A skill `site-do-escritorio` já faz isso.
- **Perfil do Google:** descrição e postagens, em texto natural. Repetir a palavra dez
  vezes piora.
- **Instagram:** campo "nome" do perfil e legenda (primeiras palavras).

Nunca prometa posição no Google. O Google decide a ordem por relevância, distância e
reputação, e ninguém controla.

## 6. Entregar

Grave `marketing/seo-local/AAAA-MM-DD-plano.md` com: o checklist das seções 1 a 5
(marcando o que já está feito, pelo que o advogado contou), a lista de categorias, a
lista de palavras-chave, a descrição do perfil (vinda da `copy-escritorio`) e os
modelos de resposta. Na resposta, os três primeiros passos, na ordem, e o caminho do
arquivo.

## Erros comuns

| Tentação | Resposta |
|---|---|
| "Põe a cidade no nome do perfil, ajuda" | É contra a regra do Google e pode suspender o perfil. A cidade vai na descrição e no site. |
| "Pede pra família avaliar" | Avaliação de quem não é cliente é falsa pro Google e captação pra OAB. |
| "Responde contando o que aconteceu" | Sigilo. Resposta genérica, sempre. |
| "Me garante o primeiro lugar" | Ninguém garante. O plano melhora as chances. |
