---
name: capa-instagram
description: 'Faz a capa de Reels do Instagram (1080x1920) ou a miniatura de vídeo do YouTube (1280x720) do escritório, em PNG, com as cores, a fonte e o logo do escritório, e com o título conferido pelo Provimento 205/2021 da OAB. Use quando o advogado disser "faz a capa do reels", "capa do vídeo", "thumbnail", "miniatura do YouTube", "a capa do meu vídeo tá feia", "quero uma capa que chame atenção", "capa pro perfil ficar organizado", ou "/capa-instagram".'
---

# capa-instagram: a capa que se entende em um segundo

Entrega um PNG: capa de Reels (1080x1920) ou miniatura de YouTube (1280x720). Usa a
mesma marca e o mesmo gerador de imagem da skill `carrossel-instagram`.

## 1. Marca

Leia `_contexto/marca.md`. Se não existir, siga a seção 1 da skill `carrossel-instagram`
(três perguntas, grava o arquivo) e só depois continue.

## 2. O título

Pergunte do que trata o vídeo, se o advogado não disse. Escreva **três opções** de
título e deixe ele escolher.

A regra que mais pesa: **quem nunca viu o vídeo lê só a capa e sabe do que se trata.**

- Título de 3 a 7 palavras, frase completa, com as palavras do cliente, não do processo.
  "Fui demitido grávida. E agora?" funciona. "Estabilidade provisória da gestante" é
  aula, não capa.
- A dúvida do cliente ou a consequência concreta funcionam melhor que o nome do instituto.
- Subtítulo opcional, uma frase que completa o título. Nunca repete o título.
- Sem termo técnico que só quem viu o vídeo entende.
- Cada frase com sujeito, nome concreto da coisa e ordem natural.

**Checagem:** título e subtítulo passam pela tabela da seção 4 da skill
`post-instagram` (Provimento 205/2021), item por item. Na capa os tropeços mais comuns
são promessa ("Garanta sua indenização"), urgência ("Você vai perder seu direito") e
orientação de conduta ("Foi demitido? Entre com ação"). Reprovou: reescreva e mostre o
antes e o depois.

## 3. Desenhar

Pasta: `marketing/capas/AAAA-MM-DD-<tema>/`. Copie
`.claude/skills/capa-instagram/modelo-capa.html` para lá como `capa.html`, troque o
`:root` e a linha do Google Fonts pelos valores do `marca.md`, e o texto.

- **Escura** (fundo na cor principal, letra branca) ou **clara** (fundo claro, título na
  cor principal). Se o advogado posta capas em sequência, alterne as duas: a grade do
  perfil fica organizada.
- Só dois focos: o título e, se quiser, o logo. Sem foto de cliente, sem print de
  processo, sem foto de carro, viagem ou dinheiro.
- Foto do próprio advogado pode entrar, se ele mandar o arquivo: copie para a pasta e
  ponha um `<img>` acima do título, com no máximo 40% da altura.
- YouTube: mude `--largura`/`--altura` para 1280px/720px e ponha `class="capa paisagem"`.

**Área segura do Reels:** a grade do perfil mostra a capa cortada em 3:4, mais ou
menos de y=240 a y=1680. O modelo já centraliza tudo; o `<script>` do fim pinta uma
faixa vermelha se o texto sair dessa área.

## 4. Gerar e olhar

```bash
uv run ".claude/skills/carrossel-instagram/scripts/gerar_png.py" "marketing/capas/AAAA-MM-DD-<tema>" --tamanho 1080x1920
```

(YouTube: `--tamanho 1280x720`.) Abra o PNG com a leitura de imagem e confira:

1. faixa vermelha: encurte o título e gere de novo;
2. o teste do segundo: lendo só a capa, dá pra dizer do que é o vídeo?
3. letra grossa e legível mesmo pequena (a grade do celular mostra a capa com ~360 px de largura);
4. nada importante no rodapé, onde o Instagram mostra o número de visualizações.

## 5. Entregar

O caminho do PNG, o título escolhido, as reescritas da checagem (se houve) e o aviso:

> A checagem é um filtro, não um parecer. A publicação é sua: você assina com a sua
> OAB e responde pelo conteúdo.

## Erros comuns

| Tentação | Resposta |
|---|---|
| "Põe 'URGENTE' em vermelho" | Urgência é item 7 da checagem. Clareza chama mais. |
| "Escreve o nome técnico, fica sério" | Capa é a pergunta do cliente. O nome técnico vai no vídeo. |
| "Coloca três frases, cabe" | Dois focos no máximo. Capa cheia não se lê na grade. |
