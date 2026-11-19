---
name: pacote-protocolo
description: Monta a pasta de protocolo de uma peça (PJe, eproc, e-SAJ, Projudi) com os anexos numerados na ordem de envio, nomes que o sistema do tribunal aceita, e uma folha com o tipo e o sigilo de cada documento. Use quando o advogado disser "monta a pasta do protocolo", "organiza os anexos", "numera os documentos", "vou peticionar, separa os arquivos", "prepara os documentos pra juntar", "junta os áudios", ou quando a prova tiver muitos arquivos de mídia.
---

# Pacote de protocolo

A pasta de protocolo existe para o envio ser mecânico: abrir a pasta, ordenar por **Nome**,
subir um por um na ordem. Sem pensar, sem renomear na hora, sem o sistema recusar arquivo.

## Antes de montar

1. **Leia o perfil** (`AGENTS.md` da raiz): tribunal e sistema em que o advogado peticiona.
   Sem perfil, peça `/setup` e pare.
2. **Ache a pasta do caso** (`clientes/AGENTS.md` diz a organização; sem ela,
   `clientes/<slug>/`) e leia o `briefing.md`, seção 8 (documentos).
3. **Leia a peça**, e anote cada documento que ela cita e como cita ("Doc. 3", "conforme o
   áudio de 12/03"). A ordem e o rótulo da pasta saem da peça, não da pasta de documentos.
4. Documento citado na peça que não está na pasta: liste como pendência. Não monte o
   pacote fingindo que está completo.

## Onde fica

Crie `<pasta do caso>/protocolo/AAAA-MM-DD-<peca>/` (ex.: `2026-11-19-contestacao`).
**Os documentos são COPIADOS para lá, nunca movidos:** o original fica onde estava, com o
nome que tinha, e o briefing continua apontando para ele.

## 1. Numeração

```
1- Peca.pdf
2- Doc 1 - Procuracao.pdf
3- Doc 2 - Contrato de locacao.pdf
3.1- Doc 2 - Aditivo.pdf
4- Doc 3 - Conversa de WhatsApp.pdf
4.01- Doc 3 - Audio 01 - 12-03-2026.mp3
4.02- Doc 3 - Audio 02 - 12-03-2026.mp3
...
4.12- Doc 3 - Audio 12 - 15-03-2026.mp3
```

- Item principal: `N- ` (número, hífen, espaço). Subitem: `N.M- `.
- **Sem parêntese no número**: nada de `1)`, `(1)`, `2.1)`.
- Com 10 ou mais subitens, use dois dígitos (`4.01` a `4.12`). Sem o zero, o `4.10` aparece
  antes do `4.2` na lista do computador.
- O principal vem antes dos seus subitens: a conversa é o `4`, os áudios dela são `4.01`
  em diante.
- O número da pasta não precisa bater com o "Doc. N" da peça (a peça é o 1, então o Doc. 1
  vira o 2). Por isso o rótulo `Doc N` fica no nome: é ele que liga o arquivo à citação.
- Se a peça cita um arquivo pelo nome, o nome citado continua inteiro. Renumerar só mexe no
  prefixo.

## 2. Nome que o sistema aceita

Os sistemas dos tribunais recusam caracteres especiais no nome do arquivo (o eproc diz:
"use somente letras, números, espaços e os caracteres _ e -").

- **Proibido:** `( ) [ ] , ; : / & º ª` e qualquer outro símbolo.
- **Sem acento:** `Declaracao`, `Transcricao`, `Audio`.
- Parêntese vira ` - `: `Perfil do reu - Nome da empresa.pdf`.
- O ponto do prefixo (`3.1`) e o da extensão são aceitos.
- Confira o tamanho: a maioria dos sistemas limita cada arquivo (é comum 10 MB a 30 MB por
  PDF). Arquivo acima do limite do tribunal do perfil vai para a lista de pendências, com
  o tamanho; não comprima nem divida sem o advogado pedir.

## 3. O que não sobe começa com `_`

Tudo que não vai ao processo começa com `_` e fica no fim da lista:

- `_LEIA-ME.txt`: a ordem de envio, o tipo e o sigilo de cada item, e as pendências.
- `_editavel/`: o .docx da peça. Solto na pasta, ele seria enviado por engano.

Documento condicional leva a condição no nome:
`6- Procuracao - JUNTAR SO SE nao estiver nos autos.pdf`.

## 4. A folha `_LEIA-ME.txt`

```
Protocolo: <peça> | <processo> | <sistema do tribunal>
Montado em: DD/MM/AAAA

Ordem | Arquivo | Tipo de documento no sistema | Sigilo
1 | 1- Peca.pdf | Contestação | não
3 | 3- Doc 2 - Extrato bancario.pdf | Extrato | SIM: dado bancário

Pendências:
- Doc 5 citado na peça (laudo médico): não está na pasta do caso
```

O nome do **tipo de documento** muda de sistema para sistema. Escreva o tipo em português
comum (Procuração, Declaração de hipossuficiência, Extrato, Documento de comprovação, Áudio,
Vídeo, Outros) e avise que o advogado escolhe o equivalente na lista do sistema.

**Sigilo:** extrato bancário, declaração de imposto de renda, documento fiscal, prontuário e
laudo médico, e dado de criança ou adolescente vão marcados como SIM. Quem decide e marca no
sistema é o advogado.

## 5. Muitos arquivos de mídia

Com **mais de 10 arquivos de mídia** (áudio, vídeo, print), subir um por um fica inviável.
Ofereça a alternativa, e o advogado decide:

1. Uma pasta na nuvem do escritório, com o nome das partes e do que se prova
   (`Autora x Reu - audios do reu confessando a divida`), os arquivos com a mesma numeração.
2. Na peça, cada citação de áudio leva o arquivo, a minutagem e o link.
3. Um PDF curto juntado aos autos, "Link para os áudios comprobatórios", com o link clicável.

Cuidados que vão para o `_LEIA-ME.txt`:
- Link de leitura para "qualquer pessoa com o link", numa conta do escritório que não vai
  ser apagada: precisa durar até o fim do processo.
- **Dado sensível não vai para a nuvem.** Sobe no processo, com sigilo.
- **A prova decisiva sobe também no processo.** Se o link cair, o fato central fica nos autos.
- Depois do protocolo, a pasta da nuvem não muda. Arquivo novo vai em pasta nova, com data.

Você **não cria nem compartilha pasta na nuvem**: isso tira dado do cliente da máquina, e é o
advogado quem faz, na conta dele.

## 6. Conversa de WhatsApp como prova

Além da conversa exportada (o .txt convertido em PDF), a pasta precisa ligar a conversa à
outra parte: o número do contato no cabeçalho do documento, e o print do perfil do contato
mostrando o número. Faltando, vai para as pendências.

## Como copiar

Monte o plano (uma linha por arquivo, origem TAB destino) e use o script de cópia com
registro, da skill `organizar-pasta`. Ele recusa sobrescrever e anota tudo em `desfazer/`:

```bash
uv run .claude/skills/organizar-pasta/scripts/mover_com_registro.py plano.tsv --registro desfazer/AAAA-MM-DD-protocolo-<slug>.md --copiar
uv run .claude/skills/organizar-pasta/scripts/mover_com_registro.py plano.tsv --registro desfazer/AAAA-MM-DD-protocolo-<slug>.md --copiar --executar
```

O primeiro comando só simula. Mostre o resultado ao advogado e rode o segundo com o sim.
Grave o plano em `desfazer/` também, ao lado do registro.

## Ao terminar

1. Liste a pasta e confira: ordem por nome = ordem da folha; nenhum nome com caractere
   proibido; a contagem de arquivos bate com a folha.
2. Diga ao advogado: quantos arquivos, onde está a pasta, as pendências, e "confira na
   tela do sistema, antes de enviar, a quantidade, a ordem, o tipo e o sigilo".
3. Acrescente um checkpoint no `briefing.md`: "### DD/MM/AAAA — Pacote de protocolo: <peça>".

Você **não protocola**. O último clique é do advogado.
