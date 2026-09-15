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
| **Conta no GitHub**, com o convite aceito | Este repositório é privado |
| **Assinatura do Conector DJEN** | Sem ela, o sistema não busca intimação, processo nem lei, e não calcula prazo |
| **git** e **GitHub CLI** | Baixam o kit e trazem as atualizações |

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

```
.claude/commands/   /setup e /iniciar
.claude/skills/     o que o sistema sabe fazer
.claude/agents/     os três advogados de IA
_contexto/          espaço do seu contexto de trabalho
modelos/            suas peças-modelo
```

O cálculo de prazo não está aqui: ele vem do **Conector DJEN**, que guarda no servidor os
calendários de feriado dos 27 tribunais e fica sempre atual. O Passo 11 do INSTALACAO.md liga.

---

## Onde ficam os dados dos seus clientes

**Fora desta pasta, e de propósito.**

O `/setup` cria uma pasta separada no seu computador — em `Documentos`, por exemplo — e é lá que
moram os casos. Aquela pasta **não é um repositório de código**: sem isso, não existe comando que
leve por engano nome, CPF ou processo de cliente pra fora da sua máquina.

A JurisLabs nunca vê o dado do seu cliente. Você é o controlador desses dados, e o sistema é
desenhado pra que continue assim.

---

## Como chegam as atualizações

Rode `/iniciar` ao abrir o dia: ele confere sozinho se tem versão nova do kit e pergunta se pode
puxar.

O cálculo de prazo não precisa de atualização nenhuma da sua parte: regra de contagem e
calendário de feriado moram no servidor do Conector DJEN e mudam lá.

**Uma coisa não se atualiza sozinha:** quando o Conector DJEN ganha uma ferramenta nova, o seu
Claude continua vendo as antigas, sem erro e sem aviso. Quando a mentoria avisar que saiu
ferramenta nova, refaça a ligação do Conector — está no fim do INSTALACAO.md.

---

## Suporte

WhatsApp da mentoria. Travou num passo da instalação, mande o print da tela inteira: quase todo
travamento é identificável pelo texto que apareceu.
