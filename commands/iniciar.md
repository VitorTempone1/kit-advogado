---
name: iniciar
description: 'Abre o dia de trabalho no JurisLabs OS. Carrega o perfil do escritório e mostra o que está em aberto nos casos. Use quando o advogado digitar /iniciar, ou disser "bom dia", "vamos começar", "o que tem pra hoje".'
disable-model-invocation: true
---

# /iniciar — abre o dia

Duas coisas, nesta ordem, e rápido. O advogado digitou `/iniciar` pra começar a trabalhar, não
pra ler relatório.

---

## 1. Carregue o perfil

A pasta do escritório é a pasta aberta. Leia o perfil, que é o `AGENTS.md` da raiz dela.

**Não existe perfil?** Diga só isto e pare:

> "O sistema ainda não foi configurado. Roda `/setup` que em 5 minutos a gente resolve."

## 2. Mostre o que está em aberto

Varra as pastas de cliente (na organização descrita em `clientes/AGENTS.md`, se existir) e junte o que está pendente. Ordene pelo que vence primeiro.

Máximo **10 linhas**, em português de gente, uma linha por item:

- Prazo que vence nos próximos 7 dias — **sempre no topo**, com o dia da semana escrito
  ("vence quinta, dia 18").
- Caso sem próximo passo definido no briefing.
- Documento que você pediu ao cliente e não chegou.

Se não tiver nada em aberto, uma linha só: "Nada vencendo essa semana." E pergunte o que ele
quer fazer.

---

## Travas

- **Nunca recalcule prazo aqui.** Mostre o que está escrito no briefing do caso. Recalcular no
  meio de uma varredura é como prazo errado entra em lote — e prazo errado é o único dano
  irreversível deste produto. Ele pede o recálculo quando quiser.
- **Nunca altere status de prazo**, nem de um caso, nem em lote.
- Nenhum número de CPF, nem dado de saúde, na saída desta skill. Nome do cliente basta.
