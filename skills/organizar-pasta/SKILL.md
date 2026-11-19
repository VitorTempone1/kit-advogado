---
name: organizar-pasta
description: Arruma uma pasta bagunçada do escritório (documentos de cliente, Downloads, pasta de caso, modelos) com nomes claros e numeração na ordem de leitura, sem apagar nada e com registro de desfazer de cada movimento. Use quando o advogado disser "organiza essa pasta", "essa pasta tá uma bagunça", "renomeia esses arquivos", "não acho nada aqui", "separa os documentos do cliente", "arruma os documentos que o cliente mandou", "tem muito arquivo aqui", ou "desfaz a organização".
---

# Organizar pasta

A pergunta que a pasta organizada responde sozinha: **por onde eu começo, e onde está o
documento X?** E a regra que não se negocia: **nada some.** Mover, nunca apagar, e todo
movimento anotado antes de acontecer, para poder voltar.

## Antes de mexer

1. **Leia o perfil** (`AGENTS.md` da raiz) e, se a pasta for de uma frente
   (`clientes/`, `modelos/`...), o `AGENTS.md` dela: a organização que o escritório já
   escolheu vale mais que a sugestão desta skill. `_contexto/pastas.md` tem o mapa.
2. **Pasta só de consulta não se mexe.** Se o perfil ou o `AGENTS.md` da frente diz que uma
   pasta é "só consulta", você lê e não move nada lá.
3. **Leia antes de nomear.** Abra cada arquivo que tem nome sem sentido (`IMG_2231.jpg`,
   `scan001.pdf`, `documento (3).pdf`) para saber o que é. Não chute pelo nome. Não
   conseguiu ler, o arquivo vai para `_a-classificar/` com o nome original.
4. Conte os arquivos da pasta antes de começar. Esse número fecha a conta no fim.

## Como organizar

1. **O que se abre fica na frente, e numerado na ordem de leitura.** Prefixo `N-`. Não é
   ordem alfabética nem de data: é a ordem em que a pessoa lê.
   ```
   documentos/
     1-RG-e-CPF-Maria-Souza.pdf
     2-comprovante-de-residencia-2026-10.pdf
     3-contrato-de-locacao-2024.pdf
     4-notificacao-do-locador-2026-09-12.pdf
   ```
2. **O nome diz o que é**, com data no formato `AAAA-MM-DD` quando a data importa. Sem
   acento e sem símbolo, que é o que o sistema do tribunal aceita.
3. **Nome genérico é proibido:** `novo`, `final`, `final2`, `v2`, `atualizado`, `copia`,
   `doc1`, `sem titulo`, `Untitled`. Todos querem dizer "não decidi o que é isto".
4. **Versão velha não se apaga:** vai para `arquivo/`.
5. **Duplicado não se apaga:** os dois ficam, um deles em `arquivo/` com `-duplicado` no fim.
   Só é duplicado se o conteúdo é igual, não o nome.
6. **Subpasta de máquina não tem número** (`arquivo/`, `_a-classificar/`). O que tem número,
   abre-se; o que não tem, é bastidor.
7. Pasta de caso de cliente segue a estrutura da skill `escritorio` (`reuniao/`,
   `documentos/`, `pesquisa/`...). Não invente outra.

## O plano, antes de qualquer movimento

Mostre ao advogado uma tabela **antes** de mexer:

| Hoje | Vai virar | Por quê |
|---|---|---|
| `IMG_2231.jpg` | `documentos/1-RG-frente-Maria-Souza.jpg` | é o RG (li a imagem) |
| `contrato final v2.pdf` | `documentos/3-contrato-de-locacao-2024.pdf` | |
| `contrato final.pdf` | `arquivo/contrato-de-locacao-2024-versao-anterior.pdf` | versão velha |

Pasta grande: agrupe ("38 fotos de WhatsApp vão para `documentos/fotos-whatsapp/`, nomes
mantidos"). Mexa só com o **sim** dele.

## Mover com registro

Grave o plano em `desfazer/AAAA-MM-DD-<assunto>-plano.tsv` (na raiz da pasta do escritório),
uma linha por movimento, origem e destino separados por TAB. Depois:

```bash
# 1. simula: mostra o que faria e recusa conflito (nada muda no disco)
uv run .claude/skills/organizar-pasta/scripts/mover_com_registro.py desfazer/<data>-<assunto>-plano.tsv --registro desfazer/<data>-<assunto>.md

# 2. executa: cada linha entra no registro ANTES de o arquivo mudar de lugar
uv run .claude/skills/organizar-pasta/scripts/mover_com_registro.py desfazer/<data>-<assunto>-plano.tsv --registro desfazer/<data>-<assunto>.md --executar
```

O script nunca sobrescreve: destino que já existe trava tudo antes de começar. Se um
movimento falha no meio, ele para, anota `FALHOU` no registro e diz o que já foi feito.

**Não mova arquivo de cliente com comando solto** (`mv`, `Move-Item`, arrastar). Sem o
registro, não tem como voltar.

## A conta fecha, ou é dita

No fim, conte de novo. Arquivos antes = arquivos depois, em algum lugar da pasta. O script
imprime "N arquivos no plano, N chegaram". Diferença é dita ao advogado com o número, nunca
calada.

## Desfazer

Quando o advogado pedir "desfaz", "volta como estava":

```bash
uv run .claude/skills/organizar-pasta/scripts/mover_com_registro.py --desfazer desfazer/<data>-<assunto>.md
```

Cada item volta ao lugar de origem, do último para o primeiro. O que não pôde voltar (alguém
já mexeu no destino, ou já existe algo na origem) é listado e nada é sobrescrito.

## Ao terminar

1. Pasta de cliente: acrescente um checkpoint no `briefing.md` do caso ("### DD/MM/AAAA —
   Pasta organizada", com o registro). Se os documentos mudaram de nome, atualize a seção 8
   do briefing com os nomes novos. Caso sem `briefing.md`: crie a partir do modelo da skill
   `escritorio` (`.claude/skills/escritorio/referencias/modelo-briefing.md`), não um
   arquivo avulso.
2. **Depois disso**, a última mensagem ao advogado é a entrega, sempre completa, mesmo que
   você tenha acabado de mexer no briefing:
   - a árvore final (só os nomes, sem conteúdo);
   - a conta: quantos arquivos antes, quantos depois;
   - quantos foram para `_a-classificar/` e por quê;
   - onde está o registro, e o pedido que desfaz tudo ("é só me pedir: desfaz a
     organização da pasta da Maria").

Você **nunca apaga** arquivo, nem com o advogado pedindo de passagem. Se ele quer apagar,
diga o que seria apagado e que ele mesmo faz, ou que vai para `arquivo/`.
