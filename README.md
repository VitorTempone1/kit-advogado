# JurisLabs OS

O funcionário digital do seu escritório de advocacia, rodando no seu computador.

Organiza a pasta de cada cliente, mantém o briefing do caso vivo e datado, lê PDF de processo e
devolve a linha do tempo, redige minuta no padrão do escritório e coloca três advogados de IA
pra trabalhar no seu caso: um que pesquisa, um que ataca do lado de lá e um que decide a
estratégia.

**Comece por [INSTALACAO.md](INSTALACAO.md).** É o passo a passo do zero, para Mac e Windows.

---

## O que este sistema NÃO faz

Antes de tudo, porque é o que evita o problema sério:

- **Não protocola, não assina, não peticiona.** O último clique é sempre seu.
- **Toda saída jurídica é MINUTA**, para a sua revisão. Nenhuma peça sai daqui "pronta para
  protocolar".
- **Não cita julgado que não conseguiu conferir.** Citação sem número e sem link do inteiro
  teor não entra em peça.
- **Não calcula prazo de cabeça.** O cálculo é feito por programa, e mesmo assim é apoio:
  confira no sistema do tribunal antes de confiar.

---

## Do que você precisa

| O quê | Por quê |
|---|---|
| **Claude Pro** (US$ 20/mês) ou maior | O plano gratuito não abre o Claude Code |
| **Assinatura do Conector DJEN** | Sem ela, o sistema não busca intimação, processo nem lei, e não calcula prazo |
| **git** | Baixa o kit e traz as atualizações |
| **uv** | Roda as ferramentas em Python: ler PDF, transcrever vídeo, baixar legenda |

O INSTALACAO.md instala tudo isso, passo por passo.

### Sobre o Conector DJEN

O Conector DJEN é um serviço pago da JurisLabs, cobrado por OAB. É ele que dá ao sistema acesso
ao Diário de Justiça Eletrônico Nacional, ao andamento de processo, ao texto de lei e ao
cálculo de prazo.

**Quem é da mentoria recebe o acesso incluso.**

Sem o Conector, o kit continua funcionando — só fica menor:

| Funciona sem o Conector | Precisa do Conector |
|---|---|
| Organizar a pasta do cliente e o briefing | Buscar intimação nova no Diário |
| Ler PDF de processo e montar a linha do tempo | Consultar andamento de processo |
| Redigir e revisar minuta | Puxar texto de lei |
| Os três advogados de IA raciocinando sobre o que você já tem | Calcular prazo processual |

As skills avisam em uma frase quando a ferramenta faltar. Elas não quebram, e **nunca inventam**
o que não conseguiram buscar.

---

## O que tem aqui dentro

Este repositório é baixado **como a pasta `.claude`** de uma pasta nova do seu escritório, a
`JurisLabs`, na sua pasta de usuário (fora de Documentos, que costuma sincronizar com OneDrive ou iCloud). O Claude abre na `JurisLabs` e enxerga tudo junto:

```
JurisLabs/               a pasta do seu escritório. O Claude abre AQUI
├── AGENTS.md            o perfil e as regras do escritório
├── CLAUDE.md            uma linha: @AGENTS.md
├── .claude/             o sistema: este repositório. Ninguém edita
│   ├── CLAUDE.md        as regras do sistema
│   ├── commands/        /setup e /iniciar
│   ├── skills/          o que o sistema sabe fazer
│   └── agents/          os três advogados de IA
├── _contexto/           quem é o escritório, o mapa das pastas, estilo de escrita, marca
├── _memoria/            as decisões, com data
├── _triagem/            o que a migração não soube classificar
├── desfazer/            o registro de cada movimento, pra voltar tudo
└── clientes/  modelos/  financeiro/  marketing/ ...   as frentes que você escolheu
```

Quem monta tudo que está fora da `.claude` é o `/setup`, com você.

### As skills

Você não precisa decorar o nome: fale como falaria com um assistente ("faz a ficha da Maria",
"avisa o cliente da sentença") e o Claude chama a skill certa. Se preferir, digite `/nome`.

**Casos e clientes**

| Skill | O que faz |
|---|---|
| `escritorio` | Abre a pasta do cliente, mantém o `briefing.md` do caso e coloca os três advogados de IA para trabalhar |
| `ficha-de-atendimento` | A reunião com o cliente vira a ficha do caso no briefing, com a lista de documentos para pedir |
| `kit-contratacao` | Procuração, contrato de honorários e declaração de hipossuficiência em Word, com o que falta marcado `[PREENCHER]` |
| `avisar-cliente` | Decisão, sentença ou intimação vira mensagem curta e leiga para o cliente, pronta para o WhatsApp |
| `ler-processo` | Lê o PDF do processo e devolve a linha do tempo, os pedidos e as decisões |

**Peças e protocolo**

| Skill | O que faz |
|---|---|
| `redacao-juridica` | O padrão de escrita de toda peça: petição, recurso, manifestação, parecer |
| `pacote-protocolo` | Monta a pasta de protocolo com os anexos numerados na ordem de envio e nomes que o tribunal aceita |
| `revisar-peca` | Revisa uma minuta pela régua de redação e devolve um relatório único |
| `analise-de-decisao` | Decisão, sentença ou acórdão: o que decidiu, saldo, recurso cabível e prazo pelo Conector |

**Contratos e LGPD**

| Skill | O que faz |
|---|---|
| `revisar-contrato` | Marca as cláusulas de risco para o lado do seu cliente e sugere redação |
| `notificacao-extrajudicial` | Redige a notificação ou a resposta a uma notificação recebida |
| `lgpd-escritorio` | Adequação do seu escritório à LGPD: inventário, bases legais, política, incidente, encarregado |
| `lgpd-consultivo` | Diagnóstico LGPD de cliente empresa, com lacunas e prioridade |

**Escrita, organização e conteúdo**

| Skill | O que faz |
|---|---|
| `escrita-clara` | Tira a cara de IA de e-mail, mensagem e post |
| `organizar-pasta` | Arruma pasta bagunçada sem apagar nada, com registro para desfazer |
| `post-instagram` | Da pauta ao post, com a checagem do Provimento 205/2021 da OAB |
| `transcrever-video` | Transcreve reunião, áudio e vídeo na sua própria máquina |
| `legendas-youtube` | Pega a legenda de um vídeo do YouTube sem baixar o vídeo |

`tutorial` escreve passo a passo para você fazer à mão o que não dá para automatizar. As outras
(`orquestrar`, `instrumentar`) são de bastidor: o próprio sistema usa.

O cálculo de prazo não está aqui: ele vem do **Conector DJEN**, que guarda no servidor os
calendários de feriado dos 27 tribunais e fica sempre atual. O Passo 10 do INSTALACAO.md liga.

---

## Onde ficam os dados dos seus clientes

**Na pasta `JurisLabs`, fora da `.claude`, e de propósito.**

A `.claude` é o sistema e vem da internet. O resto da `JurisLabs` é seu, e é lá que moram os
casos. A pasta `JurisLabs` **não é um repositório de código**: sem isso, não existe comando que
leve por engano nome, CPF ou processo de cliente pra fora da sua máquina. A pasta que você já
usava antes não é tocada na instalação; o `/setup` pergunta por ela e só traz alguma coisa com a
sua aprovação.

A JurisLabs nunca vê o dado do seu cliente. Você é o controlador desses dados, e o sistema é
desenhado pra que continue assim.

---

## Como chegam as atualizações

Sozinhas. Toda vez que você abre o Claude na pasta `JurisLabs`, ele confere se tem versão nova do
kit e já puxa, avisando em uma linha. Pra isso, na primeira abertura, responda **sim** quando o
Claude perguntar se confia na pasta.

O cálculo de prazo não precisa de atualização nenhuma da sua parte: regra de contagem e
calendário de feriado moram no servidor do Conector DJEN e mudam lá.

**Uma coisa não se atualiza sozinha:** quando o Conector DJEN ganha uma ferramenta nova, o seu
Claude continua vendo as antigas, sem erro e sem aviso. Quando a mentoria avisar que saiu
ferramenta nova, refaça a ligação do Conector — está no fim do INSTALACAO.md.

---

## Suporte

WhatsApp da mentoria. Travou num passo da instalação, mande o print da tela inteira: quase todo
travamento é identificável pelo texto que apareceu.
