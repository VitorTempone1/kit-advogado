---
name: escrita-clara
description: Tira a cara de texto de IA de tudo que não é peça processual (e-mail, mensagem a cliente, post de Instagram, proposta de honorários, comunicado, resumo de caso), deixando o texto com a voz do escritório. Use quando o advogado disser "tira a cara de IA", "isso tá com cara de ChatGPT", "deixa mais humano", "deixa mais natural", "reescreve esse e-mail", "melhora essa mensagem", "tá muito robótico", "tá difícil de ler", "simplifica isso", ou colar um texto pedindo revisão. Não serve para petição, recurso, contestação ou parecer (isso é da skill redacao-juridica).
---

# Escrita clara

Texto de IA tem cheiro. O cliente sente, o seguidor sente, o colega sente. E quando sente,
para de confiar no resto. Esta skill reescreve o texto para soar como uma pessoa ocupada e
competente escrevendo, que é o que o advogado é.

## Onde vale, e onde não vale

| Texto | Quem manda |
|---|---|
| E-mail, mensagem de WhatsApp, recado a cliente ou colega | **esta skill** |
| Post, legenda, roteiro de vídeo, texto de site | **esta skill** |
| Proposta de honorários, comunicado, resumo de caso, briefing | **esta skill** |
| Petição, contestação, recurso, manifestação, parecer, defesa administrativa | skill `redacao-juridica` |

## Antes de escrever

1. Se existir `_contexto/estilo-de-escrita.md` na pasta aberta, leia: é o jeito que este
   advogado escreve, aprendido das peças dele. O tom vale aqui também.
2. Se existir `_contexto/marca.md`, leia antes de post e texto de site.
3. Pergunte só se não der para deduzir: para quem é o texto e por qual canal (WhatsApp é
   mais curto que e-mail; post é mais curto que os dois).

## Os vícios que denunciam texto de IA

Procure cada um no texto. Achou, reescreva. A lista é o que mais aparece em português.

**Estrutura**
1. **Abertura de cerimônia.** "Espero que esta mensagem o encontre bem", "Venho por meio
   desta", "Gostaria de compartilhar". Corte. Comece pelo assunto.
2. **Fecho de cerimônia.** "Fico à disposição para quaisquer esclarecimentos", "Qualquer
   dúvida, não hesite em entrar em contato", "Espero ter ajudado". Um "qualquer dúvida, me
   chame" basta, e só se fizer sentido.
3. **Trio automático.** Tudo vem em três: "rápido, seguro e eficiente". Pessoa de verdade
   lista dois, ou quatro, ou um. Corte o adjetivo que não carrega nada.
4. **"Não é só X, é Y."** "Não se trata apenas de um processo, mas de justiça." Diga Y direto.
5. **Pergunta retórica seguida de resposta.** "O resultado? Vitória." "E o melhor?" Troque
   por frase afirmativa.
6. **Lista onde cabia uma frase.** Três tópicos de cinco palavras viram uma frase.
7. **Negrito espalhado.** Um destaque por mensagem, no máximo. Em WhatsApp, quase nunca.
8. **Emoji de enfeite** (🚀 ✨ 💡 ✅) em texto profissional. Só se o advogado já usa.

**Vocabulário**
9. **Palavra inflada.** "Fundamental", "crucial", "essencial", "robusto", "jornada",
   "cenário atual", "no mundo de hoje", "desempenha um papel", "potencializar", "alavancar",
   "de suma importância". Troque pela palavra comum ou corte.
10. **Muleta de ênfase.** "Vale ressaltar que", "É importante destacar", "Cabe mencionar",
    "Em suma", "Nesse sentido". Corte e diga a coisa.
11. **Hesitação em cascata.** "Pode ser que talvez seja possível". Uma ressalva, no lugar
    certo, ou nenhuma.
12. **Elogio à pergunta.** "Ótima pergunta!", "Excelente ponto!". Corte sempre.

**Pontuação e ritmo**
13. **Travessão (—).** É a marca mais conhecida de texto de IA em português. Troque por
    ponto, vírgula, dois-pontos ou parênteses.
14. **Toda frase do mesmo tamanho.** Alterne: uma curta, uma média. Frase com mais de 35
    palavras quase sempre são duas.
15. **Dois-pontos dramático.** "E o motivo é simples: ..." Diga o motivo.

**Conteúdo**
16. **Generalidade no lugar do fato.** "Diversos clientes", "inúmeros casos", "ampla
    experiência". Ponha o número, o caso, o exemplo; se não tiver, corte.
17. **Promessa que o advogado não pode fazer.** "Garantimos o resultado", "você vai ganhar".
    Além de soar falso, viola o Código de Ética da OAB. Troque pelo que ele de fato faz.
18. **Jargão sem tradução para leigo.** "Trânsito em julgado", "tutela de urgência",
    "concluso". Para cliente, explique em palavra comum; o termo técnico pode vir entre
    parênteses se ele for ver o termo em outro lugar.

## Como reescrever

- Mantenha **todo fato, número, data e nome** do original. Escrita clara corta enfeite,
  nunca informação.
- Mantenha a pessoa gramatical do advogado (eu ou nós, você ou o senhor).
- Não invente dado para deixar o texto mais concreto. Faltou o exemplo, deixe
  `[EXEMPLO: ...]` para ele completar.
- Mais curto que o original, quase sempre.

## Antes de entregar

Grave o texto final num arquivo temporário (ou use o arquivo que o advogado mandou) e rode a
varredura mecânica que o kit já tem. Ela conta travessão, palavra inflada, hesitação e
enchimento:

```bash
uv run .claude/skills/redacao-juridica/auditar-peca.py <arquivo.txt|.md|.docx>
```

O script não julga a prosa. Depois dele, releia o texto como o destinatário vai ler: se uma
frase só faz sentido para quem escreveu, reescreva.

## O que entregar

1. O texto reescrito, pronto para copiar.
2. Em até 3 linhas: o que mudou (ex.: "tirei a abertura de cerimônia, 4 travessões e a
   promessa de resultado").
3. Se faltou dado, a lista do que ele precisa completar.

Se o texto veio de um arquivo, pergunte antes de sobrescrever; o padrão é gravar ao lado,
com o mesmo nome e `-revisado` no fim.
