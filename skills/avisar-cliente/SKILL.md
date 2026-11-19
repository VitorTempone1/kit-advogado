---
name: avisar-cliente
description: Transforma movimentação, decisão, sentença, despacho ou intimação do processo numa mensagem curta e em linguagem de leigo para o cliente, pronta para colar no WhatsApp ou mandar por e-mail. Use quando o advogado disser "avisa o cliente", "como eu explico isso pro cliente", "escreve pro cliente o que aconteceu", "manda um zap pro fulano sobre a decisão", "saiu a sentença, prepara a mensagem", "traduz esse despacho pro cliente", ou colar uma intimação pedindo um recado ao cliente.
---

# Avisar o cliente

O cliente não quer saber o que o juiz escreveu. Ele quer saber três coisas: **o que
aconteceu, o que isso muda para ele, e se ele precisa fazer alguma coisa.** A mensagem
responde as três, nessa ordem, em linguagem de quem não é advogado.

## Antes de escrever

1. **Leia o perfil** (`AGENTS.md` da raiz da pasta aberta): nome do advogado e do
   escritório, que assinam a mensagem. Sem perfil, diga em uma frase que é preciso rodar
   `/setup` e pare.
2. **Ache a pasta do caso** (pela organização em `clientes/AGENTS.md`; sem ela,
   `clientes/<slug>/`) e leia o `briefing.md`: o que o cliente pediu, o que ele espera, e a
   seção 4 ("expectativa desalinhada"), que diz o que precisa de cuidado ao falar.
3. **Leia o ato inteiro.** Fonte, nesta ordem:
   - texto colado ou arquivo que o advogado mandou;
   - Conector DJEN: `ler_intimacao` (teor da publicação) ou `consultar_processo` (andamento).
     Sem o Conector, diga em uma frase que ele precisa colar o texto do ato, e espere.
   Nunca escreva a mensagem a partir só do título da movimentação ("Conclusos",
   "Juntada de petição"): título não diz o que foi decidido. **Não invente o conteúdo de um
   ato que você não leu.**
4. Leia `_contexto/estilo-de-escrita.md`, se existir, para acertar o tom (você ou o senhor,
   formal ou próximo).

## As regras da mensagem

1. **Nunca diga de onde veio a informação, nem como.** Nada de "vi no Diário Eletrônico",
   "o sistema avisou", "a ferramenta encontrou", "a inteligência artificial leu", nome de
   site, robô ou programa. O cliente contratou o advogado, não a ferramenta. Escreva como o
   advogado acompanhando o caso: "acompanhando o seu processo, vi que...", "saiu hoje...".
2. **Vende o trabalho, não o método.** Mostre o que o escritório fez ou vai fazer ("já
   estamos preparando o recurso"), não o caminho técnico.
3. **Nunca prometa resultado.** Nada de "vamos ganhar", "é certo", "fique tranquilo que
   reverte". Diga o próximo passo e, se couber, a chance em termos honestos ("é um recurso
   que costuma ser aceito quando..." só se o advogado disser isso).
4. **Prazo só se vier pronto.** Data limite entra na mensagem **somente** se veio do
   `calcular_prazo` do Conector ou da seção 7 do `briefing.md`. Nunca calcule data de cabeça.
   Sem data pronta, escreva a ação sem data ("preciso que me mande o comprovante o quanto
   antes") e avise o advogado, fora da mensagem, que o prazo não foi calculado.
   O prazo do cliente (mandar documento, comparecer) não é o prazo processual: dê ao
   cliente uma data com folga, que o advogado define.
5. **Notícia ruim vai direta, com o próximo passo junto.** Não esconda a derrota em
   eufemismo, nem abra com ela sem dizer o que vem depois.
6. **Juridiquês traduzido.** "Sentença de improcedência" vira "o juiz não aceitou o
   pedido". "Concluso para decisão" vira "o processo está com o juiz para decidir".
   "Trânsito em julgado" vira "a decisão ficou definitiva". Número do processo só se o
   cliente costuma usar.
7. **Curta.** WhatsApp: até 6 linhas, sem negrito espalhado, sem lista se couber em frase.
   E-mail: até 3 parágrafos curtos, com assunto.
8. **Nada de dado sensível desnecessário** (CPF, valor de conta, diagnóstico) em mensagem
   de WhatsApp. Se o cliente precisa saber, diga que explica por ligação.

Antes de entregar, passe o texto pelos vícios da skill `escrita-clara` (abertura e fecho de
cerimônia, travessão, palavra inflada).

## Formato da entrega

```
**WhatsApp**
<mensagem pronta para colar>

**E-mail** (só se o advogado pediu)
Assunto: <assunto curto>
<corpo>

**Para você, advogado (não vai para o cliente)**
- o que o ato decidiu, em uma linha técnica
- prazo: <data e fonte (Conector ou briefing)> | "não calculado: rode calcular_prazo"
- o que deixei de fora da mensagem e por quê
```

Você **não envia nada**. O advogado copia, revisa e manda.

## Onde salvar

Grave a mensagem em `<pasta do caso>/mensagens/AAAA-MM-DD-<assunto>.md` e acrescente um
checkpoint curto no fim do `briefing.md` ("### DD/MM/AAAA — Aviso ao cliente: <assunto>",
com o ato e o que foi dito). Nunca reescreva checkpoint antigo. Sem pasta de caso, entregue
só na conversa e não crie pasta.

## Exemplo

Ato: sentença julgou procedente em parte a ação contra a companhia aérea, condenou a
R$ 4.000 de danos morais, negou o dano material por falta de nota fiscal.

> Oi, Joana. Saiu a decisão do seu processo contra a companhia aérea. O juiz reconheceu que
> você foi prejudicada e mandou a empresa pagar R$ 4.000 pelo transtorno. O pedido de
> reembolso das despesas não foi aceito, porque faltou a nota fiscal. A empresa ainda pode
> recorrer. Vou analisar se vale recorrer da parte negada e te falo até sexta.
> Dr. Paulo
