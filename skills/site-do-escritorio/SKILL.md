---
name: site-do-escritorio
description: 'Cria o site de uma página do escritório (um arquivo HTML só, que abre bem no celular e no computador), com as cores e o logo do escritório, texto conferido pelo Provimento 205/2021 da OAB, e ensina passo a passo a colocar no ar de graça pelo Netlify. Use quando o advogado disser "quero um site", "faz o site do escritório", "preciso de uma página pra pôr na bio", "landing page", "meu site tá velho", "coloca meu site no ar", "atualiza o telefone do site", ou "/site-do-escritorio".'
---

# site-do-escritorio: a página do escritório, pronta e no ar

Entrega `marketing/site/index.html` (um arquivo só, com o estilo dentro) e o passo a
passo pra publicar grátis. O site informa quem é o escritório, o que faz, onde fica e
como falar com ele. Não vende.

## 1. Juntar o material

1. `AGENTS.md` da raiz: nome, OAB, áreas, cidade. Sem ele, peça `/setup` e pare.
2. `_contexto/marca.md`: se não existir, seção 1 da skill `carrossel-instagram` (três
   perguntas, grava o arquivo).
3. Pergunte, numa mensagem só, o que faltar: endereço (ou "só online"), telefone e
   WhatsApp, e-mail, horário, Instagram, formação do advogado e ano de inscrição na
   OAB, foto do advogado (arquivo) se quiser.
4. Os textos saem da skill `copy-escritorio` (título, quem somos, áreas). Se o
   advogado já tem texto, ele passa pela checagem dela.

**Nunca invente** endereço, telefone, formação ou ano. Faltou, deixe o bloco de fora e
diga no fim.

## 2. As seções (nesta ordem)

1. **Topo:** logo ou nome, e um botão "Fale com o escritório" (link do WhatsApp).
2. **Abertura:** título com a área e a cidade ("Advocacia de família em Contagem"),
   uma frase dizendo pra quem, e o mesmo botão.
3. **Áreas de atuação:** uma por bloco, 2 a 4 frases cada, em palavras de leigo.
4. **Quem somos:** foto (se houver), formação, inscrição na OAB, como é o atendimento.
5. **Como funciona o atendimento:** presencial, online, horário. Três frases, não um
   fluxograma.
6. **Contato:** endereço, telefone, WhatsApp, e-mail, horário, e o mapa do Google
   (`<iframe>` de "Compartilhar > Incorporar mapa", só se houver endereço).
7. **Rodapé:** nome do advogado ou da sociedade, **número da OAB**, CNPJ se for
   sociedade, e "Este site tem caráter informativo, conforme o Provimento 205/2021 do
   CFOAB."

**Não entra:** preço, "consulta grátis", depoimento de cliente, número de causas ou de
clientes, logos de empresas atendidas, "os melhores", contador de vitórias, pop-up,
formulário que guarda dado (o contato é por WhatsApp, telefone e e-mail: assim o site
não coleta dado pessoal e não precisa de aviso de cookies), Google Analytics ou pixel.

## 3. Como construir

Um `index.html` com o CSS dentro de `<style>`. Imagens (logo, foto) na mesma pasta,
com nome simples (`logo.png`, `foto.jpg`). Nada de framework nem script de terceiros.
Mapa: só o link "Ver no Google Maps" (`https://www.google.com/maps/search/?api=1&query=<endereço>`),
nunca `<iframe>` do Maps: o mapa embutido é script de terceiro, grava cookie do Google no
visitante (aí o site passa a precisar de aviso de cookies) e não aparece no print da seção 4.

Princípios de qualidade visual (escritos pra este kit, a partir de boas práticas de
design de interface):

- **Uma cor manda.** A cor principal da marca nos títulos e no botão; a de destaque só
  em detalhe pequeno; fundo claro e neutro. Nada de degradê em texto, sombra colorida,
  efeito de vidro ou animação de entrada em cada bloco.
- **Tipografia faz a hierarquia.** Título com a fonte de títulos do `marca.md`, grande
  (no celular, uns 2,2rem; no computador, até 3,5rem com `clamp()`); texto em 1.0625 a
  1.125rem com entrelinha 1.6; linha de texto com no máximo uns 68 caracteres
  (`max-width: 68ch`).
- **Espaço separa, caixa não.** Mais espaço acima de um título do que abaixo. Evite
  transformar tudo em cartão igual com ícone; áreas de atuação podem ser uma lista com
  título e parágrafo. Nunca cartão dentro de cartão.
- **Sem rótulo pequeno em cima do título** ("NOSSAS ÁREAS" em cima de "Áreas de
  atuação") e sem numerar seção (01, 02, 03). O título basta.
- **Ícone só se for desenho de verdade** (SVG simples e do mesmo traço). Emoji não é
  ícone.
- **Detalhes que mostram cuidado:** cor da seleção de texto, contorno de foco e
  sublinhado de link na paleta da marca.

Acessibilidade (obrigatória):

- `<html lang="pt-BR">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Estrutura com `<header>`, `<main>`, `<section>` com `<h2>`, `<footer>`; um só `<h1>`.
- Contraste de pelo menos 4,5 para 1 no texto e no botão. Cor clara da marca não é cor
  de texto.
- Toda imagem com `alt` que descreve (logo: "Logo de <nome do escritório>"); foto
  decorativa com `alt=""`.
- Link "Pular para o conteúdo" no topo; foco visível (`:focus-visible`) em todo link e
  botão; área de toque de pelo menos 44px.
- Links de WhatsApp e telefone com texto que diz o destino ("Falar pelo WhatsApp",
  "Ligar para (31) 0000-0000"), `tel:` e `https://wa.me/55DDDNUMERO`.
- `@media (prefers-reduced-motion: reduce)` desliga qualquer transição.

Pra o Google (ver também a skill `seo-local`):

- `<title>`: "Nome do Escritório | Advocacia de <área> em <cidade>".
- `<meta name="description">` com até 155 caracteres, área e cidade.
- `<meta property="og:title">`, `og:description` e `og:image` (logo ou foto), pra o link
  ficar bonito no WhatsApp.
- Um bloco `<script type="application/ld+json">` com `"@type": "LegalService"`: nome,
  endereço, telefone, horário, `url`. Só com dado real.

## 4. Conferir antes de entregar

1. **Checagem do Provimento 205/2021:** rode a tabela da seção 4 da skill
   `post-instagram` (e os tropeços da tabela da `copy-escritorio`) em todo texto do
   site, incluindo o `alt` das imagens e a descrição. Item reprovado: reescreva e
   mostre o antes e o depois. Confira que nome e OAB estão no rodapé.
2. **Olhar no celular e no computador.** Copie a pasta `marketing/site` inteira para
   `marketing/site-prints/celular` e `marketing/site-prints/computador` (o print não
   pode ficar dentro de `site`, senão sobe junto pro ar) e rode o gerador do carrossel:

   ```bash
   uv run ".claude/skills/carrossel-instagram/scripts/gerar_png.py" "marketing/site-prints/celular" --tamanho 390x3200
   uv run ".claude/skills/carrossel-instagram/scripts/gerar_png.py" "marketing/site-prints/computador" --tamanho 1440x3200
   ```

   Abra os dois `index.png` e confira: nada cortado ou saindo da tela no celular, botão
   visível na primeira tela, texto legível, contraste bom, imagens carregadas. Página
   mais comprida que 3200 px: aumente a altura. Corrigiu, copie e gere de novo. O print de
   celular sai com 500 px de largura (o Chrome não abre janela menor): a página fica nos 390 px
   da esquerda e o resto é faixa cinza, não defeito. `marketing/site-prints` pode ficar: está
   fora de `site` e não sobe pro ar.
3. Abra o `index.html` no navegador do advogado (dois cliques no arquivo) e peça pra ele
   olhar também.

## 5. Colocar no ar, grátis (Netlify)

Escolha deste kit: **Netlify**, porque é arrastar a pasta pro navegador. Sem
programa, sem linha de comando, sem conta de programador. O endereço grátis fica
`nome-do-escritorio.netlify.app`.

Passe ao advogado, nesta forma:

1. Abra `app.netlify.com/signup` e crie a conta grátis (pode entrar com a conta do
   Google). Sem conta o site some depois de pouco tempo.
2. Já dentro, abra `app.netlify.com/drop`.
3. Abra a pasta `marketing` do escritório no Finder (Mac) ou no Explorador de Arquivos
   (Windows) e **arraste a pasta `site` inteira** pra área pontilhada da página.
4. Em alguns segundos aparece o endereço do site, com um nome sorteado. Clique nele e
   confira.
5. Pra trocar o nome sorteado: nas configurações do site, procure "Change site name"
   (mudar nome do site) e escreva o nome do escritório, sem espaço, com hífen.
6. **Pra atualizar depois** (mudou telefone, entrou área nova): eu altero o
   `index.html`, você abre o site no Netlify, vai na aba "Deploys" e arrasta a pasta
   `site` de novo. O endereço continua o mesmo.

Domínio próprio (`seuescritorio.adv.br`) é opcional e pago à parte (registro.br). O
Netlify aceita: nas configurações do site, "Domain management". Ofereça ajudar quando
ele tiver comprado.

Os nomes dos botões do Netlify podem mudar. Se o advogado não achar, peça print da tela
e guie pelo que aparece.

## 6. Entregar

Na resposta: o caminho do `index.html`, o que ficou de fora por falta de dado, as
reescritas da checagem e o passo a passo da seção 5. E o aviso:

> A checagem é um filtro, não um parecer. O site é publicidade sua: você assina com a
> sua OAB e responde pelo conteúdo. Leia a página inteira antes de publicar.

## Erros comuns

| Tentação | Resposta |
|---|---|
| "Põe um formulário de contato" | Formulário guarda dado pessoal e pede política de privacidade. WhatsApp e e-mail resolvem. |
| "Coloca os depoimentos dos clientes" | Depoimento é captação. Não entra. |
| "Põe um contador de processos ganhos" | Ostentação e promessa. Não entra. |
| "Faz com animação em tudo" | Uma página calma passa seriedade. Nada de animação por bloco. |
| "Publica você mesmo" | A publicação é do advogado, na conta dele. Eu preparo e guio. |
