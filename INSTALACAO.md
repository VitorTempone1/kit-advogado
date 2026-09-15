# Instalação do JurisLabs OS

Passo a passo do zero absoluto. Você não precisa saber programar. São cerca de 25 minutos.

Cada passo tem **uma única ação** e diz **o que você tem que ver na tela** pra saber que deu
certo. Se o que apareceu na sua tela for diferente do que está escrito aqui, pare e chame no
WhatsApp da mentoria. Não tente adivinhar.

> **Esta instalação é feita junto com o mentor, na Sessão 0.** Ela envolve autenticar no
> GitHub, e é justamente aí que trava quem nunca usou. Não é para ser feita sozinho na
> primeira vez.

---

## Os 4 pré-requisitos

Confira os quatro antes de começar. Faltando qualquer um, a instalação para no meio.

### 1. Conta Claude paga

**O plano gratuito do Claude não roda o Claude Code.** Não é limite de uso, não é "roda mais
devagar": simplesmente não abre.

O piso é o **Claude Pro (US$ 20/mês)**, e ele roda bem o kit inteiro. Max, Team e Enterprise
também servem.

Confira em [claude.ai/settings/billing](https://claude.ai/settings/billing).

**O que você vai ver:** a palavra **Pro**, **Max**, **Team** ou **Enterprise**. Se aparecer
**Free**, faça o upgrade antes de continuar.

### 2. Conta no GitHub

O kit é entregue por um repositório **privado**: só quem foi convidado tem acesso. Para receber
o convite, você precisa de uma conta gratuita em [github.com/signup](https://github.com/signup).

Depois de criar, **mande seu nome de usuário do GitHub pro mentor**. Ele envia o convite, e
você precisa **aceitar** o convite (chega por e-mail e também aparece em
[github.com/notifications](https://github.com/notifications)) antes do Passo 7.

**O que você vai ver:** um e-mail com o assunto começando por "Invitation to join", e um botão
verde de aceite.

### 3. Assinatura do Conector DJEN

**Sem isso, metade do kit não funciona.** As skills que leem intimação do Diário, que consultam
processo e que buscam legislação dependem do **Conector DJEN**, que é um serviço pago da
JurisLabs, cobrado por OAB.

**Se você é da mentoria, o acesso é incluso** — o mentor gera o seu e te entrega um endereço
que termina com uma sequência de letras e números. Esse endereço é a sua chave: **é pessoal, não
compartilhe**. Se vazar, avise, que a gente cancela e gera outro.

O que funciona **sem** o Conector: organizar a pasta do cliente, manter o briefing do caso, ler
PDF de processo e montar a linha do tempo, redigir e revisar minuta, os três advogados de IA
raciocinando em cima do que você já tem.

O que **não** funciona sem ele: buscar intimação nova no Diário, consultar andamento de processo
e puxar texto de lei. As skills avisam em uma frase quando faltar — elas não quebram e não
inventam o que não conseguiram buscar.

### 4. Git e GitHub CLI

Dois programas gratuitos. São eles que baixam o kit e que trazem as atualizações depois.
A instalação deles está no caminho do seu sistema, mais abaixo.

---

# Caminho Mac

## Passo 1. Abra o Terminal

Aperte **Command + barra de espaço**, digite `Terminal` e aperte **Enter**.

**O que você vai ver:** uma janela com uma linha de texto terminada por `$` ou `%` e o cursor
piscando.

## Passo 2. Instale o Claude Code

Copie a linha abaixo inteira, cole no Terminal e aperte **Enter**.

```
curl -fsSL https://claude.ai/install.sh | bash
```

Vai demorar de 30 segundos a 2 minutos, com texto correndo na tela. Isso é normal.

**O que você vai ver:** o texto para de correr e o cursor volta a piscar numa linha nova.

## Passo 3. Feche e abra o Terminal de novo

Feche a janela (**Command + Q**) e abra de novo (Passo 1).

Esse passo parece bobo e não é: é ele que faz o computador enxergar o programa recém-instalado.
Pular esse passo é a causa mais comum de "não funcionou".

## Passo 4. Confirme que instalou

```
claude --version
```

**O que você vai ver:** um número de versão, tipo `2.1.211 (Claude Code)`.

**Se der errado:** apareceu `command not found: claude`. Reinicie o Mac e repita este passo.

## Passo 5. Instale o git

```
git --version
```

**O que você vai ver, se já tiver:** um número de versão, tipo `git version 2.39.5`. Pode pular
pro Passo 6.

**Se não tiver:** o Mac abre sozinho uma janelinha perguntando se você quer instalar as
"Ferramentas de linha de comando". Clique em **Instalar** e espere terminar (alguns minutos).
Depois rode `git --version` de novo pra confirmar.

## Passo 6. Instale o GitHub CLI

Baixe o instalador em [cli.github.com](https://cli.github.com/), na seção **macOS**, o arquivo
que termina em `.pkg`. Abra o arquivo baixado e clique em **Continuar** até o fim.

Feche e abra o Terminal de novo, e confirme:

```
gh --version
```

**O que você vai ver:** um número de versão, tipo `gh version 2.62.0`.

**Se preferir o Homebrew** (só se você já usa): `brew install gh` faz o mesmo.

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

## Passo 2. Instale o Claude Code

Copie a linha abaixo inteira, cole no PowerShell (botão direito dentro da janela cola) e aperte
**Enter**.

```
irm https://claude.ai/install.ps1 | iex
```

**O que você vai ver:** texto correndo por 30 segundos a 2 minutos, e o cursor voltando a piscar
numa linha que começa com `PS C:\`.

## Passo 3. Instale o git e o GitHub CLI

Ainda no PowerShell, rode as duas linhas abaixo, **uma de cada vez**, apertando **Enter** depois
de cada uma e esperando terminar:

```
winget install --id Git.Git -e --source winget
```

```
winget install --id GitHub.cli -e --source winget
```

Cada uma demora de 1 a 3 minutos e mostra uma barra de progresso.

**O que você vai ver:** ao fim de cada uma, a frase **"Instalado com êxito"**
(ou "Successfully installed").

**Se aparecer `winget não é reconhecido`:** seu Windows é antigo demais ou está sem a Loja.
Instale os dois pelos instaladores oficiais, clicando **Avançar** até o fim:
[git-scm.com/download/win](https://git-scm.com/download/win) e
[cli.github.com](https://cli.github.com/).

## Passo 4. Feche e abra o PowerShell de novo

Feche a janela no **X** e abra de novo (Passo 1).

Sem isso, o Windows continua não enxergando os três programas que acabaram de ser instalados.
É o passo que mais se pula e que mais causa erro depois.

## Passo 5. Confirme que os três instalaram

Rode as três linhas, uma de cada vez:

```
claude --version
```
```
git --version
```
```
gh --version
```

**O que você vai ver:** um número de versão em cada uma das três.

Faltou alguma? Vá pra tabela **Os 6 problemas do Windows**, logo abaixo.

---

## Os 6 problemas do Windows

Praticamente todo travamento no Windows é um destes seis. Ache o seu pelo texto que apareceu na
tela.

### Problema 1: você abriu o Prompt de Comando (CMD) em vez do PowerShell

**Na tela:** `'irm' não é reconhecido como um comando interno ou externo`
(em inglês: `'irm' is not recognized as an internal or external command`)

**Por quê:** `irm` só existe no PowerShell. Você está no CMD.

**Conserto:** feche a janela. Volte ao Passo 1 e clique em **"Windows PowerShell"**. A prova de
que você está no lugar certo é a linha começar com `PS C:\`.

### Problema 2: você colou um comando de CMD dentro do PowerShell

**Na tela:** `O token '&&' não é um separador de instrução válido nesta versão`

**Por quê:** você colou uma linha escrita pro CMD numa janela de PowerShell.

**Conserto:** use exatamente as linhas deste documento. Não use comando copiado de outro
tutorial da internet.

### Problema 3: o Windows não acha o `claude` depois de instalar

**Na tela:** `O termo 'claude' não é reconhecido como nome de cmdlet, função...`

**Por quê:** o programa foi instalado em `C:\Users\SeuNome\.local\bin`, mas a janela do
PowerShell aberta ainda não sabe disso.

**Conserto, na ordem:**
1. Feche o PowerShell e abra de novo. Tente de novo. Resolve na maioria dos casos.
2. Não resolveu: **reinicie o computador** e tente de novo.
3. Ainda não: cole a linha abaixo e tente `claude --version` de novo:
   ```
   $env:Path += ";$env:USERPROFILE\.local\bin"
   ```
   Se funcionar **depois** dessa linha, avise na mentoria.

### Problema 4: você abriu a versão (x86) do PowerShell

**Na tela:** a instalação parece rodar mas termina com erro. O título da janela é
**"Windows PowerShell (x86)"**.

**Conserto:** feche essa janela. No menu Iniciar, clique em **"Windows PowerShell"**, o item
**sem** o `(x86)`. Refaça a instalação a partir do Passo 2.

### Problema 5: o `git` ou o `gh` não é reconhecido depois do winget

**Na tela:** `O termo 'git' não é reconhecido...` ou `O termo 'gh' não é reconhecido...`

**Por quê:** é o mesmo caso do Problema 3. O winget instalou, mas a janela aberta não enxerga.

**Conserto:** feche o PowerShell e abra de novo. Não resolveu, reinicie o computador. É quase
sempre isso.

### Problema 6: o `gh auth login` abre o navegador e não volta

**Na tela:** o navegador abriu, você autorizou, mas o PowerShell continua parado esperando.

**Conserto:** volte pra janela do PowerShell e aperte **Enter** uma vez. Ela estava esperando
você confirmar que terminou no navegador.

---

# Baixando o kit (Mac e Windows, igual)

Daqui pra frente é idêntico nos dois sistemas.

## Passo 7. Entre na sua conta do GitHub

No Terminal (Mac) ou PowerShell (Windows):

```
gh auth login
```

Ele vai fazer 4 perguntas. Responda com as **setas do teclado** e **Enter**:

| Pergunta | O que escolher |
|---|---|
| *What account do you want to log into?* | **GitHub.com** |
| *What is your preferred protocol...?* | **HTTPS** |
| *Authenticate Git with your GitHub credentials?* | **Yes** |
| *How would you like to authenticate?* | **Login with a web browser** |

Ele mostra um **código de 8 caracteres** (tipo `A1B2-C3D4`) e pede pra você apertar **Enter**.
O navegador abre sozinho. Cole o código, autorize, e volte pro Terminal.

**O que você vai ver:** a frase **`✓ Logged in as SEUUSUARIO`**.

> A terceira resposta, o **Yes**, é a que importa pro futuro: é ela que guarda seu acesso no
> cofre do sistema operacional. Sem ela, você teria que fazer login toda vez que fosse buscar
> atualização.

## Passo 8. Escolha onde o kit vai morar

**Mac:**
```
cd ~/Documentos
```
(Se o seu Mac estiver em inglês, troque `Documentos` por `Documents`.)

**Windows:**
```
cd "$env:USERPROFILE\Documentos"
```
(Se o seu Windows estiver em inglês, troque `Documentos` por `Documents`.)

**O que você vai ver:** nada, só o cursor numa linha nova mostrando a pasta. No terminal,
silêncio quer dizer que deu certo.

## Passo 9. Baixe o kit

```
gh repo clone VitorTempone1/kit-advogado
```

**O que você vai ver:** algumas linhas com `Cloning into 'kit-advogado'...` e contagem de
arquivos.

**Se der `Could not resolve to a Repository`:** você ainda não aceitou o convite, ou entrou
numa conta diferente da que foi convidada. Volte ao pré-requisito 2.

## Passo 10. Entre na pasta e abra o Claude

```
cd kit-advogado
```
```
claude
```

**O que você vai ver:** na primeira vez ele abre o navegador pedindo login na sua conta Claude.
Faça o login, autorize, e volte pro terminal. Depois disso, a tela do Claude Code com um campo
de texto esperando. **Você chegou.**

> **Abra o Claude sempre nesta pasta.** É daqui que ele enxerga as skills do kit. Os arquivos
> dos seus clientes ficam em outra pasta, e o sistema sabe chegar lá sozinho — você não precisa
> abrir o Claude lá dentro.

## Passo 11. Instale o motor de prazo

O cálculo de prazo **não** vem no kit, e isso é de propósito: ele é um programa de verdade, com
os calendários de feriado de cada tribunal, e precisa se atualizar sozinho quando um tribunal
publica portaria nova. Por isso ele chega separado, e se mantém sozinho.

Dentro do Claude, digite e aperte **Enter**:

```
/plugin marketplace add VitorTempone1/jurislabs-plugins
```

**O que você vai ver:** uma mensagem confirmando que o marketplace `jurislabs` foi adicionado.

Depois:

```
/plugin install jurislabs-prazos@jurislabs
```

E, pra ele ficar disponível na hora:

```
/reload-plugins
```

**O que você vai ver:** confirmação de que os plugins foram recarregados.

## Passo 12. LIGUE O AUTO-UPDATE (não pule este passo)

**É o passo mais importante depois da instalação.**

Marketplaces que não são da Anthropic vêm com atualização automática **desligada** por padrão.
Quando um tribunal muda o calendário de feriado, a correção sai por aqui. Sem este passo, você
**não recebe** — e não fica sabendo que não recebeu.

1. Digite `/plugin` e aperte **Enter**.

   **O que você vai ver:** um menu com abas no topo, entre elas **Discover**, **Installed**,
   **Marketplaces** e **Errors**.

2. Use as setas do teclado até a aba **Marketplaces** e aperte **Enter**.

3. Selecione **jurislabs** e aperte **Enter**.

4. Selecione **"Enable auto-update"** e aperte **Enter**.

   **O que você vai ver:** a opção vira **"Disable auto-update"**. Parece contraditório e não é:
   ela agora oferece *desligar*, porque já está **ligado**. É essa a confirmação.

5. Aperte **Esc** para sair do menu.

## Passo 13. Ligue o Conector DJEN

O mentor te passou um endereço que começa com `https://` e termina com uma sequência de letras
e números. **Saia do Claude** digitando `/exit` e aperte **Enter**.

De volta ao terminal, rode a linha abaixo trocando `ENDERECO_QUE_O_MENTOR_PASSOU` pelo seu:

```
claude mcp add --transport http --scope user conector-djen ENDERECO_QUE_O_MENTOR_PASSOU
```

**O que você vai ver:** uma confirmação de que o servidor `conector-djen` foi adicionado.

O `--scope user` é o que faz o Conector valer em qualquer pasta do seu computador, não só
nesta.

Abra o Claude de novo:

```
claude
```

E confirme, dentro do Claude:

```
/mcp
```

**O que você vai ver:** `conector-djen` na lista, marcado como **connected**, com **5
ferramentas**.

**Se aparecer com menos de 5 ferramentas ou como failed:** veja **"Quando o Conector muda"**,
no fim deste documento.

## Passo 14. Configure o kit pro seu escritório

Dentro do Claude, digite e aperte **Enter**:

```
/setup
```

**O que você vai ver:** o kit começa a te fazer perguntas, uma de cada vez: seu nome, o nome do
escritório, sua OAB, em que área você atua, em que tribunal peticiona, que peça você mais faz,
como você escreve.

Pode sair no meio pra atender o telefone. A pergunta fica esperando, não tem cronômetro.

No fim ele monta a pasta do seu escritório, grava o perfil e te diz onde ficou.
**A instalação acabou.**

---

# Depois: como chegam as atualizações

Toda semana da mentoria sai coisa nova no kit. Você não precisa fazer nada pra descobrir:
**quando você abrir o Claude nesta pasta e rodar `/iniciar`, ele confere sozinho** e te avisa
se tem versão nova, perguntando se pode puxar.

Se preferir puxar na mão, saia do Claude com `/exit` e rode, dentro da pasta `kit-advogado`:

```
git pull
```

**O que você vai ver:** ou `Already up to date.` (você já está na última versão), ou uma lista
de arquivos atualizados.

## Quando o Conector muda

O Conector DJEN é diferente do kit: correção de comportamento (regra de prazo, calendário de
feriado) chega sozinha, sem você fazer nada.

**Mas ferramenta nova, não.** O Claude pergunta quais ferramentas existem **uma vez, na hora que
conecta**, e não pergunta de novo. Se a JurisLabs publicar uma ferramenta nova, o seu Claude
continua vendo as antigas, **sem dar erro e sem avisar**. Quando o mentor disser que saiu
ferramenta nova, refaça a ligação:

1. `/exit` pra sair do Claude.
2. `claude mcp remove conector-djen`
3. `claude mcp add --transport http --scope user conector-djen ENDERECO_QUE_O_MENTOR_PASSOU`
4. `claude` pra abrir de novo, e `/mcp` pra conferir a contagem de ferramentas.

**Guarde o seu endereço do Conector** num lugar seguro antes de remover. Sem ele você não
consegue ligar de novo — é a sua chave.

---

# Resumo do que você tem que ter no fim

- [ ] Plano **Pro** (ou maior) na conta Claude
- [ ] Convite do GitHub **aceito**
- [ ] `claude --version`, `git --version` e `gh --version` respondendo com número de versão
- [ ] `gh auth login` feito, mostrando `✓ Logged in as SEUUSUARIO`
- [ ] Pasta `kit-advogado` baixada
- [ ] Plugin `jurislabs-prazos` instalado e **auto-update ligado** (o menu mostra "Disable auto-update")
- [ ] Conector DJEN ligado, aparecendo em `/mcp` como **connected** com **5 ferramentas**
- [ ] `/setup` rodado até o fim, com o perfil gravado e a pasta do escritório criada

---

# Três coisas que valem pra sempre

**Nenhuma saída do sistema é peça pronta.** Tudo que sai daqui é minuta pra sua revisão. O
sistema não protocola, não assina e não peticiona. O último clique é sempre seu.

**A pasta do seu escritório fica só na sua máquina.** Ela é criada **fora** desta pasta do kit
e, de propósito, **não é um repositório de código**: sem isso, não existe comando que leve por
engano nome, CPF ou processo de cliente pra fora do seu computador. Nós nunca vemos o dado do
seu cliente. Você é o controlador desses dados.

**O endereço do Conector é pessoal e é a sua chave.** Não mande em grupo, não cole em
documento compartilhado, não publique em print. Vazou: avise a mentoria, que a gente cancela na
hora e te manda outro.
