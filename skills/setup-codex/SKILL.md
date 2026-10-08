---
name: setup-codex
description: 'Só para quem usa o Codex (ChatGPT). Monta o escritório dentro do JurisLabs OS com a mesma entrevista do /setup do Claude. Use quando o advogado digitar $setup-codex no Codex. No Claude Code, use /setup.'
disable-model-invocation: true
---

# $setup-codex: o /setup, rodando no Codex

Você está no **Codex**, não no Claude Code. A entrevista é a mesma: leia
`.claude/commands/setup.md` **inteiro** e siga, com as trocas abaixo. Onde as duas coisas
divergirem, vale esta página.

Antes de começar, leia também `.claude/CLAUDE.md`. São as regras do sistema e valem aqui por
inteiro. O Codex não carrega esse arquivo sozinho, então você lê.

## As trocas

1. **Menus.** O Codex não tem `AskUserQuestion`. Pergunte no chat, **uma pergunta por vez**, com
   as opções numeradas (no máximo 4) e uma última linha: *"Nenhuma serve? Escreva com as suas
   palavras."* Espere a resposta antes da próxima. Onde o setup pede `multiSelect`, diga *"pode
   escolher mais de uma, separe os números por vírgula"*. O resto das regras da entrevista
   (trade-off em linguagem de advogado, texto livre pra nome, OAB e caminho) fica igual.

2. **Pasta antiga em "só apontar".** O Codex não usa `.claude/settings.local.json`. Não crie esse
   arquivo. Registre o caminho em `_contexto/pastas.md` e a regra "só consulta: ler, nunca mover,
   renomear ou apagar" no `AGENTS.md` da frente, como o setup manda. Avise o advogado em uma
   frase que, pra ler fora da pasta `JurisLabs`, o Codex pode pedir permissão na hora.

3. **`AGENTS.md` da raiz.** É ele que o Codex lê sozinho toda vez que abre. Monte do jeito que o
   setup descreve, sem pular a linha que manda ler `.claude/CLAUDE.md` antes de qualquer tarefa.
   O `CLAUDE.md` da raiz pode ser criado igual; não atrapalha o Codex e serve se um dia o
   escritório abrir a pasta no Claude.

4. **Comandos.** Onde o setup fala em `/iniciar`, `/escritorio` ou outra barra, no Codex o
   advogado digita `$` e o nome (`$escritorio`) ou só pede com as próprias palavras. O `/iniciar`
   não existe como skill: quando ele disser "bom dia" ou "o que tem pra hoje", leia
   `.claude/commands/iniciar.md` e siga.

5. **Agentes jurídicos.** No Codex não há agente com nome. Quando o trabalho pedir
   `pesquisa-juridica`, `parte-contraria` ou `head-juridico`, abra um subagente e mande, como
   primeira ordem, ler `.claude/agents/<nome>.md` e seguir aquele arquivo.

6. **Atualização automática.** Já foi ligada na instalação (`.codex/hooks.json`). Não mexa nela.
   Se o advogado disser que o Codex não puxou versão nova, peça que ele digite `/hooks` e
   aprove o do JurisLabs OS.

## No fim

O mesmo fechamento do setup, com os nomes do Codex: as tarefas de teste de cada frente chamam
`$escritorio`, `$ler-processo` e as demais pelo `$`.
