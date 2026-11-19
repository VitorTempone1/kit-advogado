---
name: carrossel-instagram
description: 'Monta a ARTE do carrossel do Instagram do escritório: um PNG 1080x1350 por slide, com as cores, as fontes e o logo do escritório, pronto pra subir no Instagram. O texto passa antes pela checagem do Provimento 205/2021 da OAB (a da skill post-instagram). Use quando o advogado disser "faz a arte do carrossel", "gera as imagens do post", "transforma esse post em carrossel", "quero o carrossel pronto pra postar", "monta os slides", "faz os PNG", "não quero abrir o Canva", ou "/carrossel-instagram".'
---

# carrossel-instagram: o post virando imagem

Entrega um PNG por slide, 1080x1350 (o formato retrato do feed), com a marca do
escritório. O texto vem da skill `post-instagram`; esta skill só desenha.

## 1. A marca: `_contexto/marca.md`

Leia `_contexto/marca.md` na pasta aberta. **Se não existir, faça três perguntas, uma
mensagem só**, e grave a resposta no formato abaixo antes de seguir:

1. "Quais as cores do escritório? Pode ser o nome (azul-marinho e dourado) ou o código."
2. "Tem logo em arquivo? Me diga onde está (PNG com fundo transparente é o ideal), ou responda 'sem logo'."
3. "Qual estilo combina mais com você: clássico (fonte com serifa, sóbrio) ou moderno (fonte sem serifa, limpo)?"

```markdown
# Marca do escritório

Cor principal: #1F3A5F        (títulos)
Cor de destaque: #B08D57      (detalhes pequenos)
Fundo: #F6F4EF
Texto: #1B1F27
Fonte dos títulos: Playfair Display   (Google Fonts)
Fonte do texto: Inter                 (Google Fonts)
Logo: _contexto/logo.png              (ou "sem logo")
Estilo: clássico
Tom: <se o advogado disser; senão "sóbrio e didático">
```

Como traduzir a resposta:

- Nome de cor vira código. Fundo claro e quase neutro (creme, branco quebrado) é o
  padrão; a cor da marca vai nos títulos e nos detalhes, não no fundo inteiro.
- **Contraste:** letra sobre fundo precisa de contraste alto (regra prática: 4,5 para 1).
  Cor clara da marca (dourado, amarelo, verde-água) nunca é cor de texto longo: vira
  destaque. Na dúvida, texto quase preto sobre fundo claro.
- Clássico: título Playfair Display ou Lora, texto Inter ou Source Sans 3. (Evite Cormorant Garamond: o acento circunflexo sai deformado no PNG.)
  Moderno: título e texto em Inter, ou título em Manrope. Sempre fonte do Google Fonts.
- Logo: copie o arquivo para `_contexto/logo.png` (ou `.svg`) e anote o caminho.

Sem logo, o rodapé leva o nome do escritório. Com ou sem logo, o rodapé leva o nome do
advogado ou da sociedade e o número da OAB (o `AGENTS.md` da raiz tem os dois).

## 2. O texto

- Se o advogado apontar um post de `marketing/posts/`, use esse texto: ele já passou
  pela checagem.
- Se não houver texto, rode a skill `post-instagram` primeiro (tema, carrossel, legenda
  e checagem do Provimento 205/2021). **Não existe arte sem a checagem.**
- Texto que o advogado trouxe pronto passa pela tabela da seção 4 da `post-instagram`
  antes de virar arte, item por item. Reprovou: reescreva, mostre o antes e o depois.

Regra de frase clara, que vale pra todo slide: cada frase se entende sozinha, numa
lida, sem o slide anterior. Sujeito escrito, nome concreto da coisa (sentença, contrato,
INSS), ordem natural (sujeito, verbo, complemento). No Instagram a pessoa cai no meio
do carrossel. Melhor uma frase um pouco mais longa que uma frase espremida.

## 3. Desenhar

Pasta: `marketing/carrosseis/AAAA-MM-DD-<tema>/` na pasta aberta (`<tema>` em
minúsculas com hífen). Dentro dela:

1. Copie `.claude/skills/carrossel-instagram/modelo/estilo.css` e troque só as seis
   variáveis do `:root` pelos valores do `marca.md`.
2. Copie o logo para a pasta do carrossel (o HTML não enxerga fora dela).
3. Escreva um HTML por slide, `01.html`, `02.html`..., a partir de
   `.claude/skills/carrossel-instagram/modelo/slide.html`. Troque a linha do Google
   Fonts pelas fontes do `marca.md`. Mantenha o `<script>` do fim: ele pinta uma faixa
   vermelha no slide quando o texto não cabe.

Classes do modelo: `slide capa` (primeiro), `slide` (conteúdo), `slide escuro` (fundo
na cor principal, use em no máximo dois: capa ou fecho). Dentro: `h1` só na capa, `h2`
nos outros, `p`, `ul` com até 4 itens curtos, `.ressalva` no slide de limite.

Medidas que cabem: capa com título de até 8 palavras; slide de conteúdo com título de
até 6 palavras e no máximo 45 palavras de corpo. Sem emoji, sem travessão, sem colchete,
sem exclamação. Uma ideia por slide.

## 4. Gerar os PNG

```bash
uv run ".claude/skills/carrossel-instagram/scripts/gerar_png.py" "marketing/carrosseis/AAAA-MM-DD-<tema>"
```

No Windows, o mesmo comando com `\` no caminho. O script usa o Chrome, o Edge ou o
Brave que já estão no computador, em modo invisível: nada pra instalar. Se não achar
nenhum, ele pede pra instalar o Google Chrome (gratuito). Cada linha `ok` é um PNG no
tamanho exato; `TAMANHO` ou `FALHOU` é defeito.

Por que não Playwright: ele baixa um navegador próprio de ~150 MB e exige um passo a
mais. O Edge já vem no Windows e o Chrome está em quase todo Mac.

## 5. Olhar antes de entregar (obrigatório)

Abra **cada PNG** com a ferramenta de leitura de imagem e confira, slide por slide:

- faixa vermelha "TEXTO NÃO COUBE": encurte o texto (não diminua a letra) e gere de novo;
- letra legível no tamanho do celular, contraste bom, nada colado na borda;
- logo inteiro e nítido, rodapé com nome e OAB, contador certo (3/8);
- o texto da arte é o texto aprovado na checagem, sem palavra trocada.

Script verde não prova arte bonita: só o olho prova. Corrigiu, gere e olhe de novo.

## 6. Entregar

Grave `texto.md` na pasta do carrossel (o texto dos slides, a legenda e a tabela da
checagem, no formato da `post-instagram`). Na resposta: o caminho da pasta, a ordem dos
PNG e o aviso:

> A checagem é um filtro, não um parecer. A publicação é sua: você assina com a sua
> OAB e responde pelo conteúdo. Olhe cada imagem antes de postar.

## Erros comuns

| Tentação | Resposta |
|---|---|
| "Diminui a letra que cabe" | Corte texto. Letra pequena some no celular. |
| "Pula a checagem, é só a arte" | A arte carrega o texto; sem checagem não sai. |
| "Põe a foto do cliente / print do processo" | Dado de cliente nunca vai pra arte (item 9 da checagem). |
| "Usa a cor dourada no texto todo" | Cor clara vira destaque; texto longo pede contraste alto. |
| "Gera direto, sem olhar" | Todo PNG é aberto e conferido antes da entrega. |
