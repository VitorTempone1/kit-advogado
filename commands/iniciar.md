---
name: iniciar
description: 'Abre o dia de trabalho no JurisLabs OS. Confere se saiu versão nova do kit, carrega o perfil do escritório e mostra o que está em aberto nos casos. Use quando o advogado digitar /iniciar, ou disser "bom dia", "vamos começar", "o que tem pra hoje".'
disable-model-invocation: true
---

# /iniciar — abre o dia

Três coisas, nesta ordem, e rápido. O advogado digitou `/iniciar` pra começar a trabalhar, não
pra ler relatório.

---

## 1. Tem versão nova do kit?

Nesta pasta do kit, rode:

```bash
git fetch --quiet && git status --short --branch
```

*(No Windows funciona igual: `git` é um programa, não um script de shell.)*

Leia a primeira linha da saída:

- Tem **`behind`** (ex: `## main...origin/main [behind 3]`) → saiu versão nova. Pergunte:
  > "Saiu versão nova do sistema, com N atualização(ões). Posso puxar agora? Leva uns segundos."

  Se ele aceitar: `git pull`. Se der qualquer erro, **não tente consertar sozinho e não rode
  nada destrutivo**: diga em uma frase que a atualização não passou e que é pra mandar o print
  no WhatsApp da mentoria. Siga o dia normalmente — o kit antigo continua funcionando.

- Não tem `behind` → **não comente nada.** Ninguém quer "você já está atualizado" todo dia.

- O comando falhou (sem rede, sem git, sem autenticação) → **silêncio.** Não trave o dia por
  causa disso, e não mostre erro técnico.

## 2. Carregue o perfil

Leia o `CLAUDE.md` da pasta do escritório. O caminho está no `CLAUDE.md` global do usuário, na
linha que começa com `JurisLabs OS — pasta do escritório:`.

**Não existe perfil?** Diga só isto e pare:

> "O sistema ainda não foi configurado. Roda `/setup` que em 5 minutos a gente resolve."

## 3. Mostre o que está em aberto

Varra as pastas de cliente e junte o que está pendente. Ordene pelo que vence primeiro.

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
