---
name: setup
description: 'Monta o escritório dentro do JurisLabs OS. Entrevista curta (quem é, OAB, área, regime de prazo, tribunais, peça, tom, equipe), lê só a ESTRUTURA da pasta que o advogado já tem, propõe a migração por bloco com registro de desfazer, abre as frentes de trabalho (casos, modelos, contratos, financeiro, Instagram, atendimento, administrativo, teses) e termina com uma tarefa pronta pra testar em cada uma. Use quando o advogado digitar /setup, ou disser "configurar", "primeira vez", "montar o escritório".'
disable-model-invocation: true
---

# /setup: monta o escritório dentro do sistema

Primeira coisa a rodar depois da instalação. Sai daqui com a casa montada, as pastas antigas
trazidas pra dentro sem quebrar a lógica do advogado, e o mapa do que o Claude faz em cada frente.
**Nunca dispare sozinho.** Só roda quando o advogado digita `/setup`.

## 🔴 Onde se escreve, e onde nunca

A pasta aberta é a **pasta do escritório**. Dentro dela, `.claude/` é o sistema: um clone do kit,
atualizado por `git pull`.

- **Nada do escritório entra em `.claude/`** (única exceção: `.claude/settings.local.json`, que o
  git ignora). Arquivo editado ali vira conflito no próximo update, e advogado leigo parado num
  conflito é instalação morta. Tudo o mais vai para a raiz da pasta do escritório e subpastas.
- **Nunca `git init`** na pasta do escritório nem na pasta antiga.

## Regras de toda a entrevista

- Uma pergunta por vez. Espere a resposta antes da próxima.
- Menu (`AskUserQuestion`) com no máximo 4 opções. Toda pergunta aceita *Outra*: diga no
  enunciado o que fazer se nenhuma servir.
- Cada opção explica o **trade-off em linguagem de advogado**. Errado: "modo verboso". Certo: "eu
  escrevo mais longo e você corta o que sobrar". Sigla, só explicada em meia linha.
- Nome, OAB e caminho de pasta são **texto livre**, sem menu.
- **Não configure `askUserQuestionTimeout`.** Ele sai pra atender telefone; a pergunta espera.
- **Nunca invente valor.** Pulou ou veio vago: pergunte de novo uma vez. Não veio: grave
  `<a preencher>` e avise no fim.
- **Nunca sobrescreva calado** arquivo que já existe na pasta do escritório.
- Fale como gente. Nada de JSON, caminho técnico ou comando na tela, a não ser que ele peça.

## Bloco 0: abertura

### Já existe perfil?

Olhe se há `AGENTS.md` na raiz da pasta aberta começando por `# Perfil do escritório`. Se houver,
leia e pergunte:

> "Já tem um escritório montado aqui. Quer **revisar tudo** (eu pergunto de novo e reescrevo, sem
> apagar nenhum caso) ou **ajustar só um ponto**?"

**Ajustar um ponto:** pergunte qual, refaça só aquela pergunta e edite só aquela seção, sem
migração. **Revisar tudo:** siga os blocos; pasta de frente que existe fica, o `AGENTS.md` dela só
muda depois de mostrar o que muda e ouvir o sim, e migração já registrada em `desfazer/` não se repete.

### O Conector está ligado?

Confira pelo **nome da ferramenta**, nunca pelo nome do servidor (cada advogado batiza o conector
como quer): procure, entre as ferramentas desta sessão, alguma que termine em `calcular_prazo` ou
`consultar_intimacoes`.

Achou: não comente, só registre no perfil. Não achou: não trave; na vitrine, uma frase só:
  > "O Conector não está ligado nesta máquina, então buscar intimação, consultar processo e puxar
  > texto de lei ainda não funcionam. O resto funciona. O INSTALACAO.md mostra como ligar em dois
  > minutos, ou peça o acesso na mentoria."

Nunca mostre erro técnico de ferramenta ausente.

## Bloco A: quem é

Conversa normal, sem menu. Abra curto:

> "Vou montar o seu escritório aqui dentro. São uns 15 minutos: perguntas sobre você, uma olhada
> nas pastas que você já tem e as frentes em que quer ajuda. Responda do jeito que falaria."

1. **"Qual é o seu nome completo, do jeito que você assina as peças?"**
2. **"E o nome do escritório, como aparece nos documentos?"** (Advoga sozinho? O nome dele serve;
   diga isso se ele hesitar.)
3. **"Qual o número da sua OAB e a UF?"** Aceite do jeito que vier ("123456/MG", "MG 123.456").
   Separe número e UF e confirme repetindo: "OAB/MG 123456, certo?"

## Bloco B: a casa

A pasta do escritório é a pasta aberta agora. Confirme em uma frase, com o nome dela:

> "O seu escritório vai morar nesta pasta, `<nome>`. É aqui que o Claude abre daqui pra frente."

Antes de seguir, as travas. Falhou uma: pare, explique em uma frase e não crie nada.

1. **A pasta aberta tem que ser a do escritório, não a do sistema.** Se não existir `.claude/`
   aqui, ou se a pasta aberta for o próprio kit (tem `commands/setup.md` na raiz), diga: "abri na
   pasta errada; feche e abra o Claude na pasta do escritório, a que tem o `.claude` dentro".
2. **A raiz não pode estar dentro de repositório git.** Rode `git rev-parse --is-inside-work-tree`
   **na raiz** (nunca dentro de `.claude/`). Erro (`not a git repository`) é o esperado: siga. Respondeu `true`: pare. "Esta pasta está
   dentro de um repositório git, e dado de cliente nunca entra em git. Mova a pasta pra fora de
   qualquer projeto de código e abra de novo." O `.claude/` **é** repositório, e isso é o certo:
   o git procura para cima, nunca para dentro, então ele não afeta a resposta da raiz.
3. **Nunca `git init`**, nem pra "consertar" a trava 2.
4. **A pasta está dentro de OneDrive, iCloud, Google Drive ou Dropbox?** (No Windows, a pasta
   Documentos costuma ser do OneDrive.) Não trava, mas anote: o perfil vai dizer onde o dado mora
   em vez de prometer que não sai da máquina.

## Bloco C: a prática

Sete perguntas com `AskUserQuestion`, uma por vez.

### 1 de 7: área de atuação (parte 1)

`multiSelect`. **É a pergunta mais importante:** define o regime de contagem de prazo. Contar
prazo criminal em dia útil, ou trabalhista pela regra do CPC, é o único erro irreversível do
produto.

Enunciado: "Em que você advoga hoje? Pode marcar mais de uma. São duas telas de áreas, esta é a
primeira. Se a sua não estiver em nenhuma, escolha *Outra* e escreva."

| Opção | Como explicar |
|---|---|
| Trabalhista | Reclamatória, audiência na Justiça do Trabalho, cálculo de verbas |
| Cível e Consumidor | Cobrança, indenização, contrato, banco, plano de saúde, aéreo |
| Família e Sucessões | Divórcio, alimentos, guarda, inventário, partilha |
| Previdenciário | INSS, benefício negado, revisão, recurso no CRPS |

### 2 de 7: área de atuação (parte 2)

`multiSelect`. "E alguma destas também? Se nenhuma, escolha *Outra* e escreva 'nenhuma'."

| Opção | Como explicar |
|---|---|
| Criminal | Defesa, inquérito, habeas corpus, execução penal |
| Tributário | Auto de infração, execução fiscal, defesa administrativa |
| Empresarial e Societário | Contrato entre empresas, societário, recuperação |
| Imobiliário | Despejo, locação, usucapião, compra e venda, condomínio |

Guarde o regime. Quem lê o perfil é o Claude, que passa o regime ao `calcular_prazo`; o Conector
não guarda nada.

| Área marcada | Regime que o perfil registra |
|---|---|
| Cível, Consumidor, Família, Sucessões, Empresarial, Imobiliário | CPC (dias úteis) |
| Trabalhista | CLT (dias úteis, recesso próprio) |
| Criminal | CPP processual (dias corridos) e CP material (inclui o dia do começo) |
| Previdenciário | CPC no judicial; administrativo em dias corridos no INSS/CRPS |
| Tributário | CPC no judicial; administrativo em dias corridos no fiscal |

Mais de um regime: o perfil registra todos, e a regra passa a ser **perguntar o regime caso a
caso, nunca assumir**. Escreva com essas palavras.

### 3 de 7: tribunais e sistema

`multiSelect`. "Onde você peticiona? Marque os sistemas que usa. Se for outro, escolha *Outra* e
escreva."

| Opção | Como explicar |
|---|---|
| PJe | O da Justiça do Trabalho e de boa parte da Federal e da estadual |
| eproc | Comum na Justiça Federal do Sul e em alguns TJs |
| e-SAJ ou Projudi | Os sistemas estaduais (e-SAJ no TJSP e outros, Projudi em vários TJs) |
| JEF ou SEEU | Juizado Especial Federal e execução penal |

Em seguida, em texto (não gasta pergunta): "e em qual tribunal e comarca você atua mais? (ex.:
TJMG, comarca de Belo Horizonte)". É o que define o feriado forense local.

### 4 de 7: perfil de cliente

"Seus clientes são mais pessoa física ou empresa?" Muda o tom da peça, os documentos que o Claude
pede e a linguagem com o cliente. Opções: **Pessoa física** · **Empresa** · **Os dois, mais ou
menos metade**.

### 5 de 7: peça mais frequente

"Qual peça você refaz mais vezes por mês?" Três ou quatro opções coerentes com a área (petição
inicial · contestação · recurso · manifestação e petição simples), com *Outra* aberto.

### 6 de 7: tom das minutas

"Como você escreve?" **Direto e curto** (peça enxuta; lê rápido, mas em caso grande você vai querer
engordar a fundamentação) · **Fundamentado e técnico** (mais doutrina e citação; mais robusta, mais
longa pra revisar) · **Formal clássico** ("Egrégio", "data venia"; combina com juízo mais formal).

### 7 de 7: quem mais usa

"Além de você, mais alguém mexe no sistema?" **Só eu** (menos confirmação no meio do caminho) ·
**Eu e estagiário** (peço confirmação antes de mexer em prazo e toda peça sai marcada como minuta) ·
**Eu e secretária ou equipe** (trava alta: nada de prazo muda sem você confirmar, toda peça sai
marcada pra revisão).

## Bloco D: suas pastas

Aqui o setup **lê antes de perguntar**. Lê só a ESTRUTURA (nomes de pasta e de arquivo,
quantidade, profundidade, extensão). **Nunca abre o conteúdo de documento de cliente.**

### 1. Tem pasta?

`AskUserQuestion`: "Você já tem uma pasta onde guarda os arquivos do escritório?" Opções: **Uma
pasta principal** (eu olho a organização e proponho como trazer pra cá) · **Espalhado em várias**
(você me diz quais, uma por vez; os passos 2 a 4 rodam pra cada uma) · **Fica na nuvem** (Drive,
OneDrive ou Dropbox: eu copio, o original fica onde está) · **Começo do zero** (vá para o Bloco E).

### 2. Onde fica?

Texto livre: "Qual o caminho? Pode arrastar a pasta pra cá." Não sabe: procure pelo nome nas pastas
de usuário e da nuvem, e confirme antes de usar. Nuvem: a pasta sincronizada no computador, não o site.

### 3. Travas na pasta antiga

- Não pode ser a pasta do escritório nem estar dentro dela, e não pode ser o `.claude/`.
- `git rev-parse --is-inside-work-tree` **rodado na pasta antiga**: `true` = pare e avise; dado de
  cliente dentro de repositório git é problema que ele resolve antes.
- Está em nuvem (pelo caminho ou pela resposta do passo 1)? Anote: migração vira **cópia**, e o
  perfil diz onde o dado mora.
- **Mesmo disco?** Mac: a pasta antiga e a nova estão no mesmo volume (as duas fora de
  `/Volumes/`, ou as duas no mesmo `/Volumes/<nome>`). Windows: mesma letra de drive. Mesmo disco
  e fora da nuvem = **mover**. Qualquer outra coisa = **copiar, conferir e deixar o original**.

### 4. Leitura

**Para ler:** use as ferramentas do próprio Claude (Glob, listagem de pasta), **nunca script de
shell**: desça nível por nível, olhando nomes.

**Para contar (a única exceção):** a listagem pode vir cortada em pasta grande, então **o total de
arquivos sai de um comando de contar**, nunca da soma de uma lista:

- Mac: `find "<pasta>" -type f | wc -l`
- Windows (PowerShell): `(Get-ChildItem -LiteralPath "<pasta>" -Recurse -File -Force).Count`

Procure três pistas:

- **Prefixo numerado nas pastas** (`1-`, `2.3-`, `01 `): é fase ou ordem. O número carrega
  status; nunca se apaga.
- **Mesmo nome de arquivo repetido em muitas pastas** (`5- Contracheques.pdf` em centenas de
  clientes): é o **kit de documentos padrão** daquele tipo de caso. Anote nome e frequência; vira
  checklist do que falta, no `AGENTS.md` de `clientes/`.
- **Onde está o volume**: qual bloco de topo concentra os arquivos e quão fundo vão os casos.

Anote também, sem abrir nada: compactados (`.zip`, `.rar`, `.7z`); arquivos marcados como "só na
nuvem"; PDFs com nome de digitalização ("scan", "digitalizado", "img_"); pasta com cara de
modelos ou peças (`.docx` com nome de peça); pasta com cara de marca (logo, posts, `.png`, `.psd`,
`.ai`); pasta com cara de pessoal (fotos de família, documentos pessoais). Isso alimenta a
tabela, a oferta do Bloco E e os avisos, uma frase cada, só quando for o caso: compactados ficam
como estão e o Claude não enxerga dentro; arquivo "só na nuvem" precisa estar baixado antes, senão
a cópia sai vazia; PDF escaneado precisa de leitura de imagem, que é a skill `ler-processo`.

**Devolva um resumo em português de gente, sem nome de cliente:** quantos arquivos, onde está o
grosso, como os casos parecem organizados, o que está solto. Ex.: "São 21 mil arquivos. 95% estão
em CLIENTES, organizados por tipo de ação, depois por uma fase numerada, depois pelo cliente.
Quase todo caso tem o mesmo kit de 8 documentos. Fora isso, uma pasta de modelos e outra de
financeiro."

### 5. Confirma a lógica

`AskUserQuestion`, com a lógica achada no enunciado ("Entendi certo: tipo de ação, depois fase,
depois cliente?"). Opções: **Isso mesmo** (mantenho assim dentro de `clientes/`) · **Quase** (você
me corrige em uma frase) · **Prefiro por cliente** (reorganização grande: hoje eu trago como está e
registro a preferência; caso novo já nasce por cliente, o antigo a gente reorganiza depois, com
calma). A resposta (e o kit de documentos padrão) vai pro `AGENTS.md` de `clientes/`.

### 6. A tabela

Uma linha por **bloco de topo** (cerca de 20 linhas no máximo; bloco pequeno e parecido se
agrupa). Nunca uma linha por arquivo.

| Hoje | Arquivos | Vai para | Certeza |
|---|---|---|---|
| `CLIENTES/` | 20.140 | `clientes/` (mesma organização) | sim |
| `Modelos/` | 312 | `modelos/` | sim |
| `Diversos/` | 88 | `_triagem/` | `?` |
| **Tem algo aqui que é pessoal?** (fotos, documentos da família) | | fica **fora** do sistema | ele diz |

Destino é uma frente (a que a tabela usa entra marcada no Bloco E). Linha sem certeza leva `?` e
vai pra `_triagem/`: **o setup nunca chuta.** A linha do pessoal é **obrigatória**, mesmo sem nada
achado; pessoal não migra nem é apontado.

### 7. Como seguir

`AskUserQuestion`: "Como quer seguir?"

| Opção | Como explicar |
|---|---|
| Revisar linha por linha | Eu leio cada linha e você confirma ou muda o destino. Mais lento, zero surpresa |
| Mover o que tenho certeza | As linhas "sim" vão pro lugar; as com `?` vão pra `_triagem/`, pra você decidir com calma |
| Só apontar por enquanto | Nada se mexe. O Claude passa a enxergar a pasta antiga onde ela está, e a gente migra outro dia |

Na nuvem ou em outro disco, diga na pergunta que "mover" vira **copiar**: o original fica, e quem
apaga é ele, quando quiser.

### 8. Aplicar (depois da Confirmação)

A tabela aprovada espera a **Confirmação**, porque as pastas de destino nascem lá. Depois do sim:

**Só apontar.** Grave a pasta antiga em `.claude/settings.local.json`, em
`permissions.additionalDirectories` (lista de caminhos absolutos). Arquivo já existe: acrescente
na lista, nunca reescreva o resto. Some uma linha em `_contexto/pastas.md` e, no `AGENTS.md` da
frente correspondente, a regra "a pasta antiga em `<caminho>` é só consulta: ler, nunca mover,
renomear ou apagar nada lá".

**Mover ou copiar.** Use o que o sistema dele tiver (no Windows o Claude roda PowerShell; no Mac,
shell), um bloco por vez, sempre nesta ordem:

1. **Antes do primeiro movimento**, crie `desfazer/AAAA-MM-DD-migracao.md` com: data, pasta
   antiga, modo (mover ou copiar) e o total contado na pasta antiga.
2. **Para cada bloco, escreva a linha no registro ANTES de executar:** `origem → destino (N
   arquivos)`. Depois do movimento os nomes velhos não existem em lugar nenhum.
3. Execute o bloco inteiro de uma vez, a pasta e não arquivo por arquivo (mesmo disco: mover é
   renomear, instantâneo; copiar: a pasta inteira, original intacto).
4. Conte o destino com o comando de contar. Bateu com o N da linha: siga. Não bateu ou deu erro:
   acrescente `FALHOU: <o que aconteceu>` no registro, **pare a migração** e conte ao advogado.

**A soma fecha ou é dita.** No fim: arquivos contados antes = arquivos que chegaram (frentes mais
`_triagem/`) + o que ficou na pasta antiga de propósito (pessoal, apontado). Ao copiar: cada bloco
copiado = mesmo número na origem. Divergência é dita com o número, nunca calada. A conta fecha o
registro.

## Bloco E: as frentes

Pergunta pela **necessidade**, não pela pasta. `clientes/` nasce sempre (as skills do kit usam):
apresente Casos como certo, com o exemplo, e as frentes que a leitura achou (ou que a tabela do D
usa) como **já confirmadas**, numa frase: "Na sua pasta achei casos, modelos e financeiro; esses
já entram."

As que sobram vão em `AskUserQuestion` com `multiSelect`, no máximo 4 por tela (duas telas;
sobrou uma só, pergunte em texto). Enunciado: "Em quais destas frentes você quer ajuda? Quanto
mais contexto eu tenho, melhor eu te ajudo. Pode não marcar nenhuma: pasta vazia que ninguém usa
só atrapalha." A descrição de cada opção é o exemplo:

| Frente | Pasta | Exemplo (descrição da opção) |
|---|---|---|
| Casos | `clientes/` | "Me manda o PDF do processo e eu devolvo a linha do tempo e o próximo prazo" |
| Modelos de peça | `modelos/` | "Escrevo a sua próxima contestação no seu estilo, a partir das suas melhores peças" |
| Contratos e honorários | `contratos/` | "Monto o contrato de honorários do cliente novo a partir do seu modelo e do briefing" |
| Financeiro | `financeiro/` | "Cruzo o extrato com os processos e te digo qual honorário de êxito ou alvará ainda não caiu" |
| Instagram e marca | `marketing/` | "Transformo uma decisão favorável num carrossel, conferido com o Provimento 205" |
| Atendimento e comercial | `atendimento/` | "Transcrevo a consulta e devolvo o briefing e a proposta de honorários" |
| Administrativo | `administrativo/` | "Te aviso quando a certidão ou a anuidade estiver vencendo" |
| Estudo e teses | `teses/` | "Guardo cada pesquisa de jurisprudência pra reaproveitar no próximo caso igual" |

- **Nunca prometa ferramenta que o kit não tem.** Diga "posso te ajudar com", nunca "tenho a
  ferramenta". Só Casos, Modelos (redação), Atendimento (transcrição) e Instagram (`post-instagram`) têm skill pronta hoje; nas
  outras o Claude ajuda conversando, com o contexto da pasta.
- **Uma frase opcional por frente criada**, em texto, uma por vez: "Em uma frase, como funciona
  hoje? Pode pular." (Ex.: "cobro 30% no êxito e R$ 1.000 de entrada".) Vai pro `AGENTS.md` da
  frente. Pulou: a pasta nasce com "conte aqui como funciona".
- **Financeiro**, ao criar, uma frase: "aqui vai dado sensível; esta pasta não é git e não
  sincroniza com a JurisLabs."
- **Personalização é oferta, não execução.** A leitura achou peças dele: "na Sessão 0 eu aprendo
  a escrever como você". Achou logo ou posts: "e a postar com a sua cara". Não crie
  `estilo-de-escrita.md` nem `marca.md`; só registre a oferta em `_contexto/escritorio.md`, com a
  pasta onde o material está.

## Confirmação

Antes de gravar qualquer coisa, um resumo de **5 linhas**: (1) quem: nome, escritório, OAB;
(2) prática: áreas, regime, tribunal principal; (3) frentes que vão nascer; (4) pastas antigas:
mover, copiar, só apontar ou nada, quantos arquivos, quantos na triagem; (5) onde fica o perfil
(`AGENTS.md`, na raiz). "Posso gravar?" Só grava com o sim. Não: pergunte o que mudar e mostre o resumo de novo.

## O que gravar (depois do sim)

Ordem: árvore e arquivos primeiro, migração (D, passo 8) depois. Arquivo que já existe: não
sobrescreva calado (regra do Bloco 0).

### A árvore

```
AGENTS.md              o perfil e as regras do escritório
CLAUDE.md              duas linhas: @AGENTS.md e @.claude/CLAUDE.md
_contexto/
  escritorio.md        o registro da entrevista
  pastas.md            o mapa: o que veio de onde, o que ficou só apontado
_memoria/
  decisoes.md          decisão com data
_triagem/              o que a migração não soube classificar
desfazer/              o registro de cada movimento
clientes/              sempre
transcricoes/          sempre (skills de transcrição gravam aqui)
tutoriais/             sempre (a skill de tutorial grava aqui)
<frentes escolhidas>   modelos/ contratos/ financeiro/ marketing/ atendimento/ administrativo/ teses/
```

Cada frente (inclusive `clientes/`) ganha `AGENTS.md` e um `CLAUDE.md` de uma linha (`@AGENTS.md`),
pro Claude carregar a regra da pasta quando trabalhar nela. Nada de `git init`, nada de arquivo
escondido além do `settings.local.json`.

### `AGENTS.md` de cada frente

Título `# <Frente>: como esta pasta funciona`, uma linha do que vai ali, e três seções:

- **Como está organizada.** Em `clientes/`: a lógica confirmada no D (ex.: "tipo de ação, depois
  fase, depois cliente; o número no começo da pasta é a fase") e o kit de documentos padrão, se a
  leitura achou. Sem organização herdada: "um caso por cliente, em `clientes/<nome>/`". Caso novo
  segue essa organização e nasce com `briefing.md` (cliente, contra quem, o que aconteceu, o que
  quer, número do processo, prazos, próximo passo).
- **Como funciona hoje.** A frase do Bloco E, ou "conte aqui como funciona".
- **Regras desta pasta.** `financeiro/`: dado sensível, não sai daqui, não vai pra post nem pra
  mensagem. `marketing/`: todo post passa pela checagem do Provimento 205/2021 antes de publicar.
  Pasta antiga só apontada: a regra de só consulta do D. E sempre: "a regra daqui especifica a da
  raiz; nunca afrouxa".

### O perfil: `AGENTS.md` da raiz

Texto de escritório, não de configuração. Editável à mão.

```markdown
# Perfil do escritório: <nome do escritório>

Este é o manual que o Claude lê antes de trabalhar aqui. É texto normal: se algo mudar, abra e
edite. Rode /setup de novo pra refazer, sem perder nada.

## O escritório
Advogado: <nome completo>, OAB/<UF> <número>
Clientes: <pessoa física / empresa / os dois>
Equipe: <só ele / estagiário / secretária ou equipe>

## Áreas e regime de prazo
<áreas marcadas>
Regime de contagem: <regimes>
<mais de um regime:> REGRA: com mais de um regime na casa, o Claude NUNCA assume o regime pelo
tipo do caso. Pergunta antes de calcular qualquer prazo, e passa o regime ao calcular_prazo.

## Onde peticiona
Sistemas: <lista>
Tribunal e comarca principal: <resposta>
Feriado forense local: conferir sempre na portaria do tribunal. É a maior fonte de erro de prazo.

## Como escrever
Tom: <tom>
Peça mais frequente: <peça>

## O sistema
Antes de qualquer tarefa, leia .claude/CLAUDE.md: são as regras do sistema, que se atualizam sozinhas. Não edite nada em .claude/.
Conector: <ligado / não ligado>
Frentes: <lista, uma por linha, com a pasta>. Antes de trabalhar numa frente, leia o AGENTS.md dela.
Registro da entrevista: _contexto/escritorio.md. Mapa das pastas: _contexto/pastas.md.
Decisões: anote em _memoria/decisoes.md, com data.

## Travas que valem sempre aqui
1. Toda saída jurídica é MINUTA. O Claude não protocola, não assina, não peticiona.
   O último clique é sempre do advogado.
2. Prazo calculado é apoio. Confira no sistema do tribunal antes de confiar.
3. Citação sem número do julgado e URL do inteiro teor não entra em peça.
4. Precedente recente e de pé. Nunca julgado antigo havendo mais novo em sentido contrário.
5. Nada de prazo muda em lote sem conferência item a item.
6. Sem o Conector, o Claude não busca intimação, processo nem lei, e avisa em vez de inventar.
<com equipe:> 7. Equipe usa o sistema: qualquer alteração de prazo passa por confirmação antes.

## Sobre esta pasta
Esta pasta guarda dado de cliente e por isso NÃO é um repositório git, de propósito: sem git,
nenhum comando leva por engano nome, CPF ou processo de cliente pra fora. Não rode git init aqui.
<fora da nuvem:> O dado do escritório fica nesta máquina.
<pasta nova ou antiga em nuvem:> O dado do escritório também fica em <OneDrive / Drive / Dropbox /
iCloud>, em <caminho>, sob as regras dessa conta. Não está só nesta máquina.
```

### `CLAUDE.md` da raiz

Duas linhas, nesta ordem: `@AGENTS.md` e `@.claude/CLAUDE.md` (a segunda garante que as regras do
sistema carreguem junto). Já existe com outro conteúdo: mostre e pergunte antes.

### `_contexto/` e `_memoria/`

**`escritorio.md`** abre com: "O perfil que vale é o `AGENTS.md` da raiz. Aqui fica o registro da entrevista." Depois:
data do setup; as respostas do A e do C como vieram; tribunal e comarca; Conector; onde estava a
pasta antiga, se é nuvem, outro disco, e o modo escolhido; o resumo da leitura (sem nome de
cliente); os campos `<a preencher>`; e a seção **Personalização (oferta para a Sessão 0)** com o
que foi achado e onde (peças, logo, posts), ou "nada achado".

**`pastas.md`**: uma linha por bloco da tabela, `origem → destino`, com o modo (movido, copiado,
apontado, ficou fora por ser pessoal, triagem). Sem pasta antiga: "começou do zero em <data>".

**`_memoria/decisoes.md`**: título `# Decisões do escritório`, a frase "uma linha por decisão, com
data, a mais nova embaixo" e a primeira: `- <AAAA-MM-DD>: escritório montado pelo /setup. Pastas
antigas: <modo>. Frentes: <lista>.`

## Bloco F: a vitrine

Nada de "configurado". Mostre o **mapa do escritório**: uma linha por frente montada, com uma
tarefa pronta pra testar **agora**, tirada da área dele. Exemplos pra Casos, por área:

| Área | Tarefa pra testar |
|---|---|
| Trabalhista | "Me manda o PDF de uma reclamatória e eu devolvo a linha do tempo e o próximo prazo" |
| Previdenciário | "Me manda a carta de indeferimento do INSS e eu te digo o recurso e o prazo" |
| Cível, Consumidor | "Me manda a sentença e eu te digo onde perdeu, onde ganhou e o recurso cabível" |
| Família | "Me conta o caso de alimentos em três frases e eu monto o briefing e a lista de documentos" |
| Criminal | "Me manda a denúncia e eu devolvo a linha do tempo e os pontos de defesa" |

Nas outras frentes, use o exemplo do Bloco E virado em tarefa ("Modelos: escolha uma peça sua
boa e eu escrevo a próxima no mesmo molde"). Depois do mapa, em poucas linhas:

- O perfil está no `AGENTS.md` desta pasta, editável quando ele quiser; a pasta não é repositório
  git, de propósito; `/setup` roda de novo a qualquer momento, sem perder nada.
- Quando houver: a soma da migração (frase de uma linha), quantos itens estão na `_triagem/`, a
  oferta de personalização, os campos `<a preencher>`, e a frase do Conector do Bloco 0.

Não liste arquivos um por um, não mostre JSON nem comando pra copiar, a não ser que ele peça.
