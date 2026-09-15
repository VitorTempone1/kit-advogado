---
name: setup
description: 'Configura o JurisLabs OS pro jeito que este escritório advoga. Entrevista curta (identidade, OAB, área de atuação, tribunais, tipo de peça, tom, equipe), cria a pasta de casos fora deste repositório e grava o perfil de prática. Todas as outras skills leem esse perfil antes de trabalhar. Use quando o advogado digitar /setup, ou quando disser "configurar", "primeira vez", "instalar o sistema".'
disable-model-invocation: true
---

# /setup — a única configuração do JurisLabs OS

Primeira coisa a rodar depois de baixar o kit. Sai daqui com a casa montada e com o OS sabendo
em que área o advogado atua, em que tribunal ele peticiona e como ele escreve.

**Nunca dispare sozinho.** Esta skill só roda quando o advogado digita `/setup`.

---

## 🔴 Regra que vale acima de tudo nesta skill

**NÃO escreva, não edite e não crie NENHUM arquivo dentro desta pasta do kit.**

Esta pasta é um repositório clonado. Todo arquivo aqui é rastreado pelo git, e o advogado vai
receber atualizações por `git pull`. Se você editar um arquivo daqui, o próximo `git pull` dele
dá conflito — e um advogado leigo parado num conflito de merge é uma instalação morta.

Tudo que esta skill escreve vai para a **pasta do escritório**, que fica FORA daqui.

Exceção única: nenhuma. Se achar que precisa gravar algo aqui, pare e diga ao advogado.

---

## Antes de perguntar qualquer coisa

### 1. Já existe perfil?

Procure um perfil já configurado. Se o advogado já rodou `/setup` antes, o caminho da pasta do
escritório está anotado em `~/.claude/CLAUDE.md` (ou no equivalente do Windows) numa linha
começando com `JurisLabs OS — pasta do escritório:`.

Se achar, e se existir um `CLAUDE.md` naquela pasta, leia e pergunte antes de mexer:

> "Já tem um perfil configurado aqui. Quer **revisar** (eu pergunto tudo de novo e reescrevo)
> ou **ajustar só um ponto**?"

**Nunca sobrescreva calado.**

### 2. Confira se o Conector DJEN está ligado

Olhe se existem, entre as ferramentas disponíveis nesta sessão, ferramentas de um servidor
chamado `conector-djen` (ou nome parecido, escolhido pelo advogado).

- **Se existirem:** ótimo, não comente. Só registre no perfil que o Conector está ligado.
- **Se não existirem:** não trave a entrevista por isso. Siga normalmente, e no fim, na
  mensagem de encerramento, acrescente **uma frase**:
  > "O Conector DJEN não está ligado nesta máquina, então buscar intimação, consultar processo
  > e puxar texto de lei ainda não funcionam. O resto do kit funciona. O passo 11 do
  > INSTALACAO.md liga isso em dois minutos — ou peça acesso na mentoria."

Nunca mostre erro técnico de ferramenta ausente pro advogado.

---

## Bloco A — quem é (conversa normal, não wizard)

Estes cinco dados são texto livre: pergunte conversando, **uma coisa por vez**, esperando a
resposta. Não use menu de opções aqui — menu com campo livre pra digitar nome é pior que a
pergunta direta.

Comece curto:

> "Vou te fazer algumas perguntas pra configurar o sistema pro seu escritório. São uns 5
> minutos. Pode responder do jeito que você falaria."

1. **"Qual é o seu nome completo, do jeito que você assina as peças?"**
2. **"E o nome do escritório, como aparece nos documentos?"**
   *(Se ele advoga sozinho, o nome dele mesmo serve — diga isso se ele hesitar.)*
3. **"Qual o número da sua OAB e a UF?"**
   *(Aceite do jeito que vier: "123456/MG", "MG 123.456", "123456 Minas". Separe você o número
   da UF. Confirme repetindo: "OAB/MG 123456, certo?")*

**Não invente nenhum desses valores.** Se o advogado pular ou responder vago, pergunte de novo
uma vez. Se ainda assim não vier, deixe o campo marcado como `<a preencher>` no perfil e avise
no fim que ele pode abrir o arquivo e escrever à mão.

---

## Bloco B — onde ficam os casos

Pergunte:

> "Onde você quer guardar os casos? Se não tiver preferência, eu crio uma pasta `Escritorio`
> dentro de `Documentos`."

O padrão sugerido:
- Mac: `~/Documentos/Escritorio`
- Windows: `%USERPROFILE%\Documentos\Escritorio`

*(Se o sistema estiver em inglês, é `Documents`.)*

### Três travas obrigatórias antes de aceitar a pasta

**Trava 1 — não pode ser dentro desta pasta do kit.** Se o caminho escolhido estiver dentro do
repositório do kit, recuse em uma frase: "essa pasta é a do sistema, e ela sincroniza com a
JurisLabs. Dado de cliente não pode morar aqui. Escolhe uma fora, tipo `Documentos/Escritorio`."

**Trava 2 — não pode estar dentro de repositório git.** Na pasta escolhida, rode:

```bash
git rev-parse --is-inside-work-tree
```

- Respondeu **erro** (`fatal: not a git repository`) = perfeito, é o esperado. Siga.
- Respondeu **`true`** = **pare**. Explique em uma frase: "essa pasta está dentro de um
  repositório git, e dado de cliente nunca deve entrar em git. Escolhe outra, fora de qualquer
  projeto de código." Peça a pasta nova e refaça a checagem.

**Trava 3 — esta skill NUNCA roda `git init` na pasta do escritório.** Sem repositório, não
existe `git push` acidental levando nome, CPF e processo de cliente pra fora da máquina.

---

## Bloco C — a entrevista de prática

**Uma pergunta por vez, com `AskUserQuestion`.** Espere a resposta antes da próxima. Não
despeje as sete de uma vez, e não resuma várias numa só.

**Não configure `askUserQuestionTimeout`.** O advogado vai sair no meio pra atender o telefone,
pra assinar uma peça, pra falar com cliente. A pergunta tem que estar esperando quando ele
voltar.

Regras de escrita das opções:

- No máximo 4 opções por pergunta. Toda pergunta aceita resposta escrita ("Outra"), então diga
  no enunciado o que fazer se nenhuma servir.
- Cada opção explica o **trade-off em linguagem de advogado**, não de programador. Errado:
  "modo verboso". Certo: "eu escrevo mais longo e você corta o que sobrar".
- Zero jargão de tecnologia. Se precisar de uma sigla, explique em meia linha.

### Pergunta 1 de 7 — Área de atuação (parte 1)

Múltipla escolha (`multiSelect`). **É a pergunta mais importante da entrevista:** é ela que
define qual regime de contagem de prazo o OS carrega. Contar prazo criminal em dia útil, ou
prazo trabalhista pela regra do CPC, é o único erro irreversível do produto.

Enunciado: "Em que você advoga hoje? Pode marcar mais de uma. São duas telas de áreas, essa é a
primeira. Se a sua não estiver em nenhuma das duas, escolha *Outra* e escreva."

| Opção | Como explicar |
|---|---|
| Trabalhista | Reclamatória, audiência na Justiça do Trabalho, cálculo de verbas |
| Cível e Consumidor | Cobrança, indenização, contrato, banco, plano de saúde, aéreo |
| Família e Sucessões | Divórcio, alimentos, guarda, inventário, partilha |
| Previdenciário | INSS, benefício negado, revisão, recurso no CRPS |

### Pergunta 2 de 7 — Área de atuação (parte 2)

Múltipla escolha. Enunciado: "E alguma dessas também? Se nenhuma, escolha *Outra* e escreva
'nenhuma'."

| Opção | Como explicar |
|---|---|
| Criminal | Defesa, inquérito, habeas corpus, execução penal |
| Tributário | Auto de infração, execução fiscal, defesa administrativa |
| Empresarial e Societário | Contrato entre empresas, societário, recuperação |
| Imobiliário | Despejo, locação, usucapião, compra e venda, condomínio |

**Guarde também o regime**, que é o que o motor de prazo vai ler:

| Área marcada | Regime que o perfil registra |
|---|---|
| Cível, Consumidor, Família, Sucessões, Empresarial, Imobiliário | CPC (dias úteis) |
| Trabalhista | CLT (dias úteis, recesso próprio) |
| Criminal | CPP processual (dias corridos) e CP material (inclui o dia do começo) |
| Previdenciário | CPC no judicial, administrativo em dias corridos no INSS/CRPS |
| Tributário | CPC no judicial, administrativo em dias corridos no fiscal |

Marcou mais de um regime: o perfil registra todos, e a regra fica sendo **perguntar o regime
caso a caso, nunca assumir**. Escreva isso no perfil com essas palavras.

### Pergunta 3 de 7 — Tribunais e sistema

Múltipla escolha. Define feriado forense local (a maior fonte de erro real de prazo) e o
vocabulário das peças. Enunciado: "Onde você peticiona? Marque os sistemas que você usa. Se usa
um que não está na lista, escolha *Outra* e escreva."

| Opção | Como explicar |
|---|---|
| PJe | O da Justiça do Trabalho e de boa parte da Justiça Federal e estadual |
| eproc | Comum na Justiça Federal do Sul e em alguns TJs |
| e-SAJ ou Projudi | Os sistemas estaduais (e-SAJ no TJSP e outros, Projudi em vários TJs) |
| JEF ou SEEU | Juizado Especial Federal e execução penal |

Depois da resposta, pergunte **em texto normal** (não gasta uma pergunta do wizard) em qual
tribunal e comarca ele atua mais, porque é o que define o feriado forense local. Uma linha:
"e em qual tribunal e comarca você atua mais? (ex: TJMG, comarca de Belo Horizonte)".

### Pergunta 4 de 7 — Perfil de cliente

"Seus clientes são mais pessoa física ou empresa?" Muda o tom da peça, o tipo de documento que
o OS vai pedir e o vocabulário da comunicação com o cliente.

Opções: **Pessoa física** · **Empresa** · **Os dois, mais ou menos metade**.

### Pergunta 5 de 7 — Peça mais frequente

"Qual peça você refaz mais vezes por mês?" É o que o kit vai otimizar primeiro. Ofereça 3 ou 4
opções coerentes com a área que ele marcou (petição inicial · contestação · recurso ·
manifestação e petição simples), sempre com o *Outra* aberto.

### Pergunta 6 de 7 — Tom das minutas

"Como você escreve?" Opções com o trade-off na cara:

| Opção | Como explicar |
|---|---|
| Direto e curto | Peça enxuta, só o necessário. Lê rápido, mas você vai querer engordar a fundamentação em caso grande |
| Fundamentado e técnico | Mais doutrina e citação. Peça mais robusta, mais longa pra revisar |
| Formal clássico | Vocabulário tradicional, "Egrégio", "Data venia". Combina com juiz mais formal |

### Pergunta 7 de 7 — Quem mais vai usar

"Além de você, mais alguém mexe no sistema?" Muda o nível de trava: com equipe, o OS confirma
antes de qualquer coisa que altere prazo ou que gere peça final, e nunca conclui sozinho.

| Opção | Como explicar |
|---|---|
| Só eu | Menos confirmação no meio do caminho |
| Eu e estagiário | O OS pede confirmação antes de mexer em prazo e sempre marca a peça como minuta pra sua revisão |
| Eu e secretária ou equipe | Trava alta: nada de prazo muda sem você confirmar, e toda peça sai marcada pra revisão |

---

## O que escrever no disco

Três coisas: a árvore, o perfil e o ponteiro. Confirme antes de escrever, mostrando um resumo de
5 linhas do que entendeu e onde vai gravar.

Lembre: **tudo abaixo mora na pasta do escritório, nunca nesta pasta do kit.**

### 1. A árvore

Dentro da pasta do escritório:

```
CLAUDE.md                     <- o perfil
clientes/
  _modelo/                    <- copie essa pasta pra cada cliente novo
    briefing.md
    documentos/
    pecas/
modelos/                      <- as peças-modelo dele
```

Nada de `git init`. Nada de arquivo escondido. Nada além disso: pasta a mais que ninguém usa só
atrapalha quem é leigo.

Em `clientes/_modelo/briefing.md`, um esqueleto curto: cliente, contra quem, o que aconteceu, o
que ele quer, número do processo, prazos, próximo passo.

### 2. O perfil (`CLAUDE.md` da pasta do escritório)

Texto puro. Escreva com a cara de um documento do escritório, não de arquivo de configuração.
Ele é editável à mão: diga isso na primeira linha depois do título.

```markdown
# Perfil de prática — <nome do escritório>

Este arquivo é o que o JurisLabs OS lê antes de trabalhar. É texto normal:
se algo aqui mudar, abra e edite. Rode /setup de novo se quiser refazer tudo.

## O escritório
Advogado: <nome completo> — OAB/<UF> <número>
Clientes: <pessoa física / empresa / os dois>
Equipe: <só ele / estagiário / secretária ou equipe>

## Áreas e regime de prazo
<lista das áreas marcadas>
Regime de contagem: <regimes correspondentes>
<se for mais de um regime:>
REGRA: com mais de um regime na casa, o OS NUNCA assume o regime pelo tipo do caso.
Pergunta qual é antes de calcular qualquer prazo.

## Onde ele peticiona
Sistemas: <PJe / eproc / e-SAJ / Projudi / JEF / SEEU>
Tribunal e comarca principal: <o que ele respondeu>
Feriado forense local: conferir sempre na portaria do tribunal. É a maior fonte de erro de prazo.

## Como escrever
Tom: <tom escolhido>
Peça mais frequente: <peça>

## O sistema
Pasta do kit: <caminho do repositório do kit>
Conector DJEN: <ligado / não ligado>

## Travas que valem sempre aqui
1. Toda saída jurídica é MINUTA. O OS não protocola, não assina, não peticiona.
   O último clique é sempre do advogado.
2. Prazo calculado pelo OS é apoio. Confira no sistema do tribunal antes de confiar.
3. Citação sem número do julgado e URL do inteiro teor não entra em peça.
4. Precedente: recente e de pé. Nunca julgado antigo havendo mais novo em sentido contrário.
5. Nada de prazo muda em lote sem conferência item a item.
6. Sem o Conector DJEN, o OS não busca intimação, processo nem lei — e avisa em vez de inventar.
<se tem equipe:>
7. Equipe usa o sistema: qualquer alteração de prazo passa por confirmação antes.

## Sobre esta pasta
Esta pasta guarda dado de cliente e por isso NÃO é um repositório git, de propósito:
sem git, não tem como um comando levar por engano nome, CPF ou processo de cliente pra fora
da sua máquina. Não rode `git init` aqui.
```

### 3. O ponteiro

Para as outras skills acharem a pasta do escritório numa sessão futura, acrescente **uma linha**
ao `CLAUDE.md` global do advogado (`~/.claude/CLAUDE.md`, criando o arquivo se não existir):

```
JurisLabs OS — pasta do escritório: <caminho completo>
```

Só isso, uma linha. Não reformate o arquivo, não mexa em mais nada que já esteja lá.

---

## Como termina

Fale em português de gente, cinco linhas no máximo:

1. Onde ficou o perfil (caminho completo) e que ele pode abrir e editar quando quiser.
2. As áreas e o regime de prazo que ficaram gravados.
3. Que a pasta não é repositório git, e que isso é proposital.
4. Uma sugestão concreta do que fazer agora, tirada da área dele. Exemplo pra trabalhista:
   "me manda o PDF de um processo seu e eu te devolvo a linha do tempo".
5. Que `/setup` pode ser rodado de novo a qualquer momento, sem perder nada.

Se o Conector DJEN não estiver ligado, acrescente a frase do bloco de checagem — e só ela.

Não liste os arquivos criados um por um. Não mostre JSON. Não mostre comando pra ele copiar, a
não ser que ele peça.
