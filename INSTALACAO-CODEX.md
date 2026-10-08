# Instalação do JurisLabs OS no Codex (ChatGPT)

Passo a passo do zero absoluto, para quem usa o **ChatGPT**. Você não precisa saber programar.
São cerca de 25 minutos.

O JurisLabs OS nasceu no Claude Code, e o guia principal é o [INSTALACAO.md](INSTALACAO.md).
Este aqui instala **o mesmo sistema** no **Codex**, o assistente de terminal da OpenAI, que vem
incluso na assinatura do ChatGPT. As skills, os três advogados de IA, o Conector DJEN e a
entrevista de configuração são os mesmos.

Cada passo tem **uma única ação** e diz **o que você tem que ver na tela** pra saber que deu
certo. Se o que apareceu na sua tela for diferente do que está escrito aqui, pare e chame no
WhatsApp da mentoria. Não tente adivinhar.

> **Esta instalação é feita junto com o mentor, na Aula 0.** É ele quem te entrega o endereço
> do Conector DJEN, no fim. Não é para ser feita sozinho na primeira vez.

---

## Os 3 pré-requisitos

Confira os três antes de começar. Faltando qualquer um, a instalação para no meio.

### 1. Conta ChatGPT paga

O Codex vem em todos os planos do ChatGPT, mas no gratuito o limite de uso acaba rápido demais
pro trabalho de um escritório. O piso recomendado é o **ChatGPT Plus (US$ 20/mês)**. Pro e
Business também servem.

Confira em [chatgpt.com](https://chatgpt.com), clicando no seu nome e depois em **Plano**.

**O que você vai ver:** a palavra **Plus**, **Pro** ou **Business**. Se aparecer **Free** ou
**Go**, faça o upgrade antes de continuar.

### 2. Assinatura do Conector DJEN

**Sem isso, metade do kit não funciona.** As skills que leem intimação do Diário, que consultam
processo, que buscam legislação e que **calculam prazo** dependem do **Conector DJEN**, um serviço
da JurisLabs cobrado por OAB.

O mentor gera o seu acesso e te entrega um endereço que termina com uma sequência de letras e
números. Esse endereço é a sua chave: **é pessoal, não compartilhe**. Se vazar, avise, que a
gente cancela e gera outro.

### 3. Git e uv

Dois programas gratuitos. O **git** baixa o kit e traz as atualizações depois. O **uv** é quem
roda as ferramentas em Python do kit: ler PDF de processo, transcrever vídeo e baixar legenda do
YouTube. Sem o uv, essas três param.

A instalação dos dois está no caminho do seu sistema, mais abaixo.

---

# Caminho Mac

## Passo 1. Abra o Terminal

Aperte **Command + barra de espaço**, digite `Terminal` e aperte **Enter**.

**O que você vai ver:** uma janela com uma linha de texto terminada por `$` ou `%` e o cursor
piscando.

## Passo 2. Instale o Codex

Copie a linha abaixo inteira, cole no Terminal e aperte **Enter**.

```
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

É o instalador oficial da OpenAI. Vai demorar de 30 segundos a 2 minutos, com texto correndo na
tela. Isso é normal.

**O que você vai ver:** o texto para de correr e o cursor volta a piscar numa linha nova.

## Passo 3. Feche e abra o Terminal de novo

Feche a janela (**Command + Q**) e abra de novo (Passo 1).

Esse passo parece bobo e não é: é ele que faz o computador enxergar o programa recém-instalado.
Pular esse passo é a causa mais comum de "não funcionou".

## Passo 4. Confirme que instalou

```
codex --version
```

**O que você vai ver:** um número de versão, tipo `codex-cli 0.145.0`.

**Se der errado:** apareceu `command not found: codex`. Reinicie o Mac e repita este passo.

## Passo 5. Instale o git

```
git --version
```

**O que você vai ver, se já tiver:** um número de versão, tipo `git version 2.39.5`. Pode pular
pro Passo 6.

**Se não tiver:** o Mac abre sozinho uma janelinha perguntando se você quer instalar as
"Ferramentas de linha de comando". Clique em **Instalar** e espere terminar (alguns minutos).
Depois rode `git --version` de novo pra confirmar.

## Passo 6. Instale o uv

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Demora alguns segundos, com texto correndo na tela.

**O que você vai ver:** algumas linhas terminando com o caminho onde o `uv` foi instalado, tipo
`installing to /Users/SEUNOME/.local/bin`.

**Feche e abra o Terminal de novo** (**Command + Q** e Passo 1). O `uv` só entra no caminho do
sistema numa janela nova. **Se o Codex já estava aberto, feche e abra ele também**, senão ele
continua sem enxergar o `uv`.

Depois confirme:

```
uv --version
```

**O que você vai ver:** um número de versão, tipo `uv 0.9.7`.

**Se der errado:** apareceu `command not found: uv`. Feche e abra o Terminal mais uma vez. Não
resolveu, reinicie o Mac e repita este passo.

**Agora pule para a parte "Baixando o kit"**, que é igual nos dois sistemas.

---

# Caminho Windows

Três avisos antes de começar, e os três são causa de travamento:

1. Use **PowerShell**, não o "Prompt de Comando" (CMD). São programas diferentes.
2. Use o PowerShell normal, **não** o que tem **(x86)** no nome.
3. Você **não** precisa ser administrador do computador.

## Passo 1. Abra o PowerShell certo

Clique no menu Iniciar e digite `PowerShell`. Na lista que aparecer, clique em
**"Windows PowerShell"**.

**NÃO** clique em "Windows PowerShell (x86)". **NÃO** clique em "Prompt de Comando".

**O que você vai ver:** uma janela azul-escura, com a última linha começando com `PS C:\Users\`
seguido do seu nome. **Se não tiver o `PS` no começo da linha, você abriu o programa errado.**

## Passo 2. Instale o Codex

Copie a linha abaixo inteira, cole no PowerShell (botão direito dentro da janela cola) e aperte
**Enter**.

```
irm https://chatgpt.com/codex/install.ps1 | iex
```

É o instalador oficial da OpenAI.

**O que você vai ver:** texto correndo por 30 segundos a 2 minutos, e o cursor voltando a piscar
numa linha que começa com `PS C:\`.

**Se aparecer um erro falando em "execução de scripts desabilitada":** cole a linha abaixo, aperte
**Enter**, e rode a do Codex de novo.

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Passo 3. Instale o git e o uv

Ainda no PowerShell, rode as duas linhas abaixo, **uma de cada vez**, apertando **Enter** depois
de cada uma e esperando terminar:

```
winget install --id Git.Git -e --source winget
```

```
winget install --id astral-sh.uv -e --source winget
```

Cada uma demora de 1 a 3 minutos e mostra uma barra de progresso.

**O que você vai ver:** ao fim de cada uma, a frase **"Instalado com êxito"**
(ou "Successfully installed").

**Se aparecer `winget não é reconhecido`:** seu Windows é antigo demais ou está sem a Loja.
Instale o git pelo instalador oficial, clicando **Avançar** até o fim:
[git-scm.com/download/win](https://git-scm.com/download/win). O `uv` não tem instalador de
clicar: cole a linha abaixo no PowerShell, que é o comando oficial dele.

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Passo 4. Feche e abra o PowerShell de novo

Feche a janela no **X** e abra de novo (Passo 1).

Sem isso, o Windows continua não enxergando os três programas que acabaram de ser instalados.
É o passo que mais se pula e que mais causa erro depois.

## Passo 5. Confirme que os três instalaram

Rode as três linhas, uma de cada vez:

```
codex --version
```
```
git --version
```
```
uv --version
```

**O que você vai ver:** um número de versão em cada uma das três.

Faltou alguma? Vá pra **Os 4 problemas do Windows**, logo abaixo.

---

## Os 4 problemas do Windows

Praticamente todo travamento no Windows é um destes quatro. Ache o seu pelo texto que apareceu na
tela.

### Problema 1: você abriu o Prompt de Comando (CMD) em vez do PowerShell

**Na tela:** `'irm' não é reconhecido como um comando interno ou externo`

**Conserto:** feche a janela. Volte ao Passo 1 e clique em **"Windows PowerShell"**. A prova de
que você está no lugar certo é a linha começar com `PS C:\`.

### Problema 2: você colou um comando de outro tutorial

**Na tela:** `O token '&&' não é um separador de instrução válido nesta versão`

**Conserto:** use exatamente as linhas deste documento.

### Problema 3: o Windows não acha o `codex`, o `git` ou o `uv` depois de instalar

**Na tela:** `O termo 'codex' não é reconhecido como nome de cmdlet, função...` (ou `git`, ou `uv`)

**Por quê:** o programa foi instalado, mas a janela do PowerShell aberta ainda não sabe disso.

**Conserto, na ordem:**
1. Feche o PowerShell e abra de novo. Tente de novo. Resolve na maioria dos casos.
2. Não resolveu: **reinicie o computador** e tente de novo.
3. Ainda não: avise na mentoria, com o print da tela.

### Problema 4: você abriu a versão (x86) do PowerShell

**Na tela:** a instalação parece rodar mas termina com erro. O título da janela é
**"Windows PowerShell (x86)"**.

**Conserto:** feche essa janela. No menu Iniciar, clique em **"Windows PowerShell"**, o item
**sem** o `(x86)`. Refaça a instalação a partir do Passo 2.

---

# Baixando o kit (Mac e Windows)

Daqui pra frente é quase idêntico nos dois sistemas. Onde muda, o passo mostra as duas versões.

> **Veio pelo Windows?** Você foi do Passo 1 ao 5 e agora vai para o Passo 7. **Não falta nada.**
> O uv já foi instalado junto com o git, lá no Passo 3.

## Passo 7. Vá para a pasta Documentos

O sistema vai morar numa pasta nova chamada `JurisLabs`, dentro de `Documentos`. É a pasta do seu
escritório daqui pra frente. A pasta que você já usa hoje **não é tocada** nesta instalação: a
configuração pergunta por ela depois, e só mexe nela com a sua aprovação.

**Mac:**
```
cd ~/Documentos
```

**Windows:**
```
cd "$env:USERPROFILE\Documentos"
```

(Se o seu computador estiver em inglês, troque `Documentos` por `Documents`.)

**O que você vai ver:** nada, só o cursor numa linha nova. No terminal, silêncio quer dizer que
deu certo.

## Passo 8. Baixe o kit para dentro da pasta nova

```
git clone https://github.com/VitorTempone1/kit-advogado.git JurisLabs/.claude
```

Esta linha cria a pasta `JurisLabs` e, dentro dela, uma pasta `.claude` com o sistema. O nome
`.claude` fica assim mesmo, também no Codex: é onde o sistema mora. Copie a linha inteira, com o
`JurisLabs/.claude` no fim.

O repositório é público: não pede senha nem login nenhum.

**O que você vai ver:** algumas linhas com `Cloning into 'JurisLabs/.claude'...` e contagem de
arquivos.

> **Não estranhe se a pasta `.claude` não aparecer no Finder ou no Explorador de Arquivos.**
> Pasta com nome começando por ponto fica escondida. Está lá, e é bom que fique.

## Passo 9. Ligue o kit ao Codex

Entre na pasta `JurisLabs`:

```
cd JurisLabs
```

Agora rode as três linhas do seu sistema, **uma de cada vez**. Elas mostram ao Codex onde estão as
skills do kit e ligam a atualização automática.

**Mac:**
```
mkdir .agents .codex
```
```
ln -s ../.claude/skills .agents/skills
```
```
cp .claude/codex/hooks.json .codex/hooks.json
```

**Windows:**
```
New-Item -ItemType Directory .agents, .codex | Out-Null
```
```
New-Item -ItemType Junction -Path .agents\skills -Target "$PWD\.claude\skills" | Out-Null
```
```
Copy-Item .claude\codex\hooks.json .codex\hooks.json
```

**O que você vai ver:** nada, só o cursor numa linha nova. Silêncio é sucesso.

**Se aparecer `File exists` ou `já existe`:** você já tinha feito este passo. Pode seguir.

## Passo 10. Abra o Codex

Ainda dentro da pasta `JurisLabs`:

```
codex
```

**O que você vai ver:** na primeira vez ele pergunta como você quer entrar. Escolha **Sign in
with ChatGPT**, faça o login no navegador com a sua conta do ChatGPT, autorize e volte pro
terminal.

Em seguida o Codex pergunta se você **confia nesta pasta** (em inglês, algo como *"Do you trust
the contents of this directory?"*). **Responda que sim.** Se você responder que não, o sistema
abre pela metade e **não se atualiza sozinho**.

Agora aprove a atualização automática. Dentro do Codex, digite e aperte **Enter**:

```
/hooks
```

**O que você vai ver:** um item com o comando `git -C .claude pull`, descrito como *"JurisLabs OS:
ao abrir o Codex na pasta do escritório, puxa a versão nova do kit"*. **Aprove esse item.** O
Codex pede essa aprovação por segurança, uma vez só, e de novo apenas se o item mudar.

> **Abra o Codex sempre na pasta `JurisLabs`.** É daqui que ele enxerga o sistema e os arquivos do
> seu escritório, tudo junto.

## Passo 11. Ligue o Conector DJEN

O cálculo de prazo **não** vem no kit, e isso é de propósito: ele mora no Conector DJEN, junto
com os calendários de feriado dos tribunais. Fica no servidor da JurisLabs, sempre atual.

**Saia do Codex** digitando `/quit` e aperte **Enter**. De volta ao terminal, rode a linha abaixo
trocando `ENDERECO_QUE_O_MENTOR_PASSOU` pelo seu:

```
codex mcp add conector-djen --url ENDERECO_QUE_O_MENTOR_PASSOU
```

**O que você vai ver:** uma confirmação de que o servidor `conector-djen` foi adicionado. Ele
passa a valer em qualquer pasta do seu computador.

Abra o Codex de novo (`codex`) e confira, dentro dele:

```
/mcp
```

**O que você vai ver:** `conector-djen` na lista, com **5 ferramentas**.

## Passo 12. Configure o kit pro seu escritório

Dentro do Codex, digite e aperte **Enter**:

```
$setup-codex
```

(No Codex as skills se chamam com `$` na frente, em vez da barra do Claude.)

**O que você vai ver:** o kit começa a te fazer perguntas, uma de cada vez, com as opções
numeradas: seu nome, o nome do escritório, sua OAB, em que área você atua, em que tribunal
peticiona, que peça você mais faz, como você escreve. Responda com o número da opção ou com as
suas palavras.

Pode sair no meio pra atender o telefone. A pergunta fica esperando.

Ele também pergunta onde fica a pasta que você já usa hoje, e só traz alguma coisa de lá com a sua
aprovação. No fim ele organiza a pasta `JurisLabs`, grava o perfil e te mostra o que montou.
**A instalação acabou.**

---

# No dia a dia: o que muda do Claude pro Codex

| No Claude | No Codex |
|---|---|
| `/setup` | `$setup-codex` |
| `/escritorio`, `/ler-processo`... | `$escritorio`, `$ler-processo`... ou peça com as suas palavras |
| `/iniciar` | diga "bom dia" ou "o que tem pra hoje" |
| `/exit` | `/quit` |
| `/mcp` | `/mcp` |

Os três advogados de IA (pesquisa, parte contrária e head) funcionam igual: peça "roda os agentes
no caso do fulano" e o Codex abre um ajudante para cada um.

---

# Depois: como chegam as atualizações

Toda semana da mentoria sai coisa nova no kit. Você não precisa fazer nada: **toda vez que você
abre o Codex na pasta `JurisLabs`, ele confere sozinho se tem versão nova e já puxa.** Sem
internet, ele segue com a versão que você já tem.

Isso só funciona se você respondeu **sim** ao "confia nesta pasta?" e aprovou o item no `/hooks`
(Passo 10).

Se quiser puxar na mão, saia do Codex com `/quit` e rode, dentro da pasta `JurisLabs`:

```
git -C .claude pull
```

**O que você vai ver:** ou `Already up to date.` (você já está na última versão), ou uma lista
de arquivos atualizados.

## Quando o Conector muda

Correção de comportamento do Conector (regra de prazo, calendário de feriado) chega sozinha.
**Ferramenta nova, não**: quando o mentor disser que saiu ferramenta nova, refaça a ligação.

1. `/quit` pra sair do Codex.
2. `codex mcp remove conector-djen`
3. `codex mcp add conector-djen --url ENDERECO_QUE_O_MENTOR_PASSOU`
4. `codex` pra abrir de novo, e `/mcp` pra conferir a contagem de ferramentas.

**Guarde o seu endereço do Conector** num lugar seguro antes de remover. Sem ele você não
consegue ligar de novo.

---

# Resumo do que você tem que ter no fim

- [ ] Plano **Plus** (ou maior) na conta ChatGPT
- [ ] `codex --version`, `git --version` e `uv --version` respondendo com número de versão
- [ ] Pasta `JurisLabs` criada em Documentos, com o kit dentro dela na `.claude`
- [ ] Passo 9 feito: as pastas `.agents` e `.codex` dentro de `JurisLabs`
- [ ] Codex aberto na pasta `JurisLabs`, pasta confiada e item aprovado no `/hooks`
- [ ] Conector DJEN ligado, aparecendo em `/mcp` com **5 ferramentas**
- [ ] `$setup-codex` rodado até o fim, com o perfil gravado
- [ ] Você guardou o endereço do Conector num lugar seguro

---

# Três coisas que valem pra sempre

**Nenhuma saída do sistema é peça pronta.** Tudo que sai daqui é minuta pra sua revisão. O
sistema não protocola, não assina e não peticiona. O último clique é sempre seu.

**A pasta do seu escritório fica só na sua máquina.** A `JurisLabs`, de propósito, **não é um
repositório de código**: sem isso, não existe comando que leve por engano nome, CPF ou processo de
cliente pra fora do seu computador. Só a `.claude`, lá dentro, é repositório: ela traz o sistema e
as atualizações, e nunca leva nada seu pra fora. Nós nunca vemos o dado do seu cliente.

**O endereço do Conector é pessoal e é a sua chave.** Não mande em grupo, não cole em documento
compartilhado, não publique em print. Vazou: avise a mentoria, que a gente cancela na hora e te
manda outro.
