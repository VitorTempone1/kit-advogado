---
name: notificacao-extrajudicial
description: 'Redige notificação extrajudicial e também a resposta (contranotificação) a uma notificação recebida pelo cliente. Use quando o advogado disser "faz uma notificação extrajudicial", "notifica o inquilino", "preciso constituir em mora", "notificação de cobrança", "notificação pra rescindir o contrato", "notificação pra parar de usar a marca", "o cliente recebeu uma notificação, responde", "contranotificação", "responde essa notificação do advogado da outra parte", "manda uma notificação antes de entrar com a ação".'
---

# Notificação extrajudicial e resposta

Dois modos. O advogado diz qual, ou você deduz: se ele trouxe uma notificação **recebida**, é
resposta.

## Regras

1. **Saída é MINUTA.** O envio (cartório, AR, e-mail com confirmação) é decisão e ato do advogado.
2. **Não invente fato.** Datas, valores, cláusulas e nomes saem dos documentos ou do advogado.
   Faltou, `[preencher]` no texto e pergunta na lista final.
3. **Artigo só com certeza.** Os dispositivos desta skill foram conferidos. Outro: `buscar_legislacao`
   do Conector DJEN ou `[conferir]`. Julgado em notificação quase nunca ajuda; se entrar, só
   recuperado nesta execução, com número, data e URL.
4. **Prazo processual não se calcula aqui.** O prazo que a notificação dá à outra parte é prazo
   contratual ou fixado pelo cliente, escrito em dias e sem data de vencimento calculada por você.
   Se o advogado perguntar se um prazo legal ou prescricional está correndo, diga que isso se
   confere à parte, pelo Conector ou à mão.
5. **Dado do cliente não sai da máquina.**
6. **Régua de redação:** siga a skill `redacao-juridica` (sem travessão, frase curta, sem adjetivo
   sobrando, pedido claro). Notificação é curta: uma a duas páginas.

## Modo 1: redigir a notificação

### Pergunte (de uma vez)

1. Quem notifica e quem é notificado (qualificação completa ou onde ela está nos documentos).
2. O que aconteceu, em ordem, com datas.
3. O que o cliente quer: pagamento, cumprimento, cessação de conduta, rescisão, entrega, devolução,
   ciência de um fato.
4. Prazo para atender (dias) e o que acontece se não atender.
5. Há contrato? Ele exige forma de notificação (escrita, endereço, prazo de aviso, cura)?
6. Meio de envio: cartório de títulos e documentos, carta com AR, e-mail, WhatsApp.

Leia os documentos que ele apontar (`.docx` pelo `texto_docx.py`, PDF pelo `mapear_pdf.py texto`,
os dois em `.claude/skills/ler-processo/scripts/`).

### Para que serve, e o que ela não faz

Diga ao advogado, numa linha, o efeito jurídico pretendido, porque isso muda o texto:

- **Constituir em mora** quando a obrigação não tem termo certo (CC 397, parágrafo único). Com
  termo, a mora já existe pelo vencimento (CC 397, caput) e a notificação é reforço e prova.
- **Exercer direito previsto no contrato** (denúncia, resilição com aviso prévio, cura de
  inadimplemento): siga exatamente a forma e o prazo da cláusula, citada pelo número.
- **Dar ciência e criar prova** (uso indevido de marca, concorrência desleal, vício do produto).
- **Notificação não interrompe prescrição.** Interrompe o protesto judicial, o protesto cambial e o
  reconhecimento inequívoco pelo devedor, entre outros (CC 202). Se a prescrição está perto, avise:
  a notificação não resolve, e o prazo é para conferir à parte.

### Estrutura

```
NOTIFICAÇÃO EXTRAJUDICIAL

NOTIFICANTE: <qualificação>, por seu advogado <nome, OAB> (procuração anexa)
NOTIFICADO: <qualificação>

1. Os fatos (só o indispensável, com data e documento)
2. O fundamento (cláusula do contrato e, se precisar, um ou dois artigos)
3. O que se exige, com prazo em dias contados do recebimento
4. A consequência do não atendimento (a medida concreta, sem ameaça genérica)
5. Canal para resposta

<local e data>
<assinatura>
```

Sem adjetivo contra o notificado, sem "sob pena das medidas cabíveis" sozinho: diga a medida
("ajuizamento de ação de cobrança", "rescisão do contrato na forma da cláusula 12"). Ameaça de
representação criminal para forçar pagamento não entra.

## Modo 2: responder a notificação recebida

### Leia e mapeie

Leia a notificação inteira e os documentos do cliente. Monte para o advogado, antes de redigir:

| O que alegam | Documento que eles citam | O que o cliente diz | Prova que o cliente tem |
|---|---|---|---|

E responda a três perguntas:

1. **Responder ou não?** Responder nem sempre convém: a resposta vira prova. Às vezes o silêncio
   ou uma resposta de uma linha (ciência e reserva de direitos) é melhor. Diga o que recomenda e
   por quê; a decisão é do advogado.
2. **O que é reconhecimento?** Nada na resposta pode admitir dívida ou fato sem querer. Lembre que
   ato inequívoco de reconhecimento do devedor interrompe a prescrição (CC 202, VI).
3. **Há prazo dado na notificação?** Aponte o prazo que eles deram, sem calcular data.

### Estrutura da resposta (contranotificação)

```
CONTRANOTIFICAÇÃO

<quem responde>, por seu advogado, em resposta à notificação de <data>, recebida em <data>:

1. Do que não procede (ponto a ponto, na ordem da notificação)
2. Do que efetivamente ocorreu (fatos com documento)
3. Da posição do notificado (o que fará e o que não fará)
4. Reserva de direitos

<local e data, assinatura>
```

Responda cada alegação uma vez, sem repetir. O que não for contestado, diga se é por concordância
ou por irrelevância, para não parecer confissão.

## Saída

Na pasta do cliente (organização do `clientes/AGENTS.md`, se existir; senão ao lado dos documentos),
nunca dentro da `.claude/`:

- `notificacao-<assunto>-AAAA-MM-DD.md` ou `resposta-notificacao-<assunto>-AAAA-MM-DD.md`

Topo do arquivo: `MINUTA. Conferir antes de enviar. [preencher]: N.` Depois do texto, a lista
"Antes de enviar": campos a preencher, documento a anexar, meio de envio recomendado e como guardar
a prova do recebimento. Nunca sobrescreva versão anterior. `.docx` só se pedido, por `pandoc` se
instalado, e rodando depois `uv run .claude/skills/redacao-juridica/auditar-peca.py` sobre o `.docx`.

No chat: o efeito pretendido em uma linha, os `[preencher]` e a recomendação de meio de envio.

## O que esta skill NÃO faz

Não envia, não registra em cartório, não calcula prazo processual nem prescricional, não decide
sozinha responder ou silenciar, não redige petição inicial (isso é `redacao-juridica`).
