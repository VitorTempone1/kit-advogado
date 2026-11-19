---
name: kit-contratacao
description: Gera, em Word (.docx), os três documentos de contratação de um cliente novo a partir do briefing ou da ficha de atendimento: procuração ad judicia, contrato de honorários e declaração de hipossuficiência. O que faltar sai marcado [PREENCHER], nunca inventado. Use quando o advogado disser "fecha o contrato", "faz a procuração", "gera o kit de contratação", "prepara os documentos pra assinar", "contrato de honorários do fulano", "declaração de pobreza", "o cliente fechou, monta a papelada".
---

# Kit de contratação

Cliente fechou. Saem três documentos em Word, prontos para o advogado revisar e mandar
assinar: **procuração**, **contrato de honorários** e, se o cliente vai pedir justiça
gratuita, **declaração de hipossuficiência**.

A regra que não se negocia: **dado que falta vira `[PREENCHER: o que é]`**, grifado em
amarelo no Word. Nunca invente CPF, endereço, estado civil, profissão, valor ou percentual.
Documento com dado inventado é pior que documento incompleto, porque ninguém percebe.

## Antes de gerar

1. **Leia o perfil** (`AGENTS.md` da raiz): nome do advogado, OAB e UF, nome do escritório,
   endereço profissional e e-mail (se houver). Sem perfil, peça `/setup` e pare.
2. **Ache a pasta do caso** (`clientes/AGENTS.md` diz a organização; sem ela,
   `clientes/<slug>/`) e leia o `briefing.md`: seção 1 (qualificação), 2 (área e o que é o
   caso) e 10 (honorários). Sem briefing, use a ficha que o advogado mandar, ou rode antes a
   skill `ficha-de-atendimento`.
3. **Modelo do escritório vence.** Se existir `modelos/` com procuração, contrato ou
   declaração do próprio advogado, use o texto dele como base e só preencha os dados.
   Os textos abaixo são o padrão para quem ainda não tem modelo.
4. **Pergunte, de uma vez só, o que falta e só ele sabe:**
   - honorários: modalidade (fixo, êxito, misto), valor ou percentual, forma e datas de
     pagamento, e se há entrada;
   - se vai pedir justiça gratuita (gera a declaração);
   - poderes especiais que ele quer na procuração (ver abaixo).
   Ele não sabe agora? Siga com `[PREENCHER]` e diga isso no fim.

## Honorários: quem define é o advogado

Você não sugere valor nem percentual. Pode lembrar, em uma frase, que a **tabela de
honorários da OAB da seccional dele** (a UF da OAB no perfil) serve de referência mínima, e
que ele confira lá. Nunca cite valor da tabela de memória.

## 1. Procuração ad judicia

- **Outorgante:** qualificação completa (nome, nacionalidade, estado civil, profissão, CPF,
  RG, endereço). Pessoa jurídica: razão social, CNPJ, sede e quem a representa.
- **Outorgado:** o advogado (nome, OAB/UF, endereço profissional, e-mail).
- **Poderes gerais:** a cláusula ad judicia et extra, para o foro em geral, em qualquer
  instância e tribunal.
- **Poderes especiais**, só os que o advogado escolher, um por um (art. 105 do CPC exige
  que estejam escritos): receber citação, confessar, reconhecer a procedência do pedido,
  transigir, desistir, renunciar ao direito, receber e dar quitação, firmar compromisso e
  **assinar declaração de hipossuficiência econômica** (este último é necessário se o
  próprio advogado for declarar a pobreza no lugar do cliente).
- **Finalidade:** o caso, em uma linha (ex.: "propor ação de indenização contra
  <parte contrária>"), ou "para o foro em geral" se o advogado preferir.
- Substabelecimento: com ou sem reserva, conforme ele disser; sem resposta, `[PREENCHER]`.
- Local, data e linha de assinatura do outorgante.

## 2. Contrato de honorários

Cláusulas, nesta ordem, em linguagem simples:

1. **Partes:** contratante (cliente, qualificação) e contratado (advogado ou sociedade).
2. **Objeto:** o serviço exato, com o que **não** está incluído (ex.: recurso a tribunal
   superior, execução, outra ação). Objeto vago gera briga.
3. **Honorários:** o valor ou percentual que o advogado informou, base de cálculo do
   êxito, forma de pagamento, datas. O que ele não informou, `[PREENCHER]`.
4. **Sucumbência:** os honorários de sucumbência pertencem ao advogado (art. 23 do
   Estatuto da Advocacia, Lei 8.906/1994), salvo se ele disser outra coisa.
5. **Despesas:** custas, perícia, cópias e deslocamento são do contratante, salvo
   combinação diferente.
6. **Obrigações do cliente:** mandar documento e informação verdadeira a tempo, avisar
   mudança de endereço e telefone.
7. **Sem garantia de resultado:** a obrigação do advogado é de meio, não de resultado.
8. **Rescisão e revogação:** o que é devido se o contrato acabar antes do fim.
9. **Foro:** a comarca do perfil, `[PREENCHER]` se ele não tiver.
10. Local, data, assinatura das partes e de duas testemunhas (o contrato com duas
    testemunhas vira título executivo, art. 784, III, do CPC).

Se o êxito for a única remuneração, acrescente a cláusula que o limita: os honorários,
somados aos de sucumbência, não podem passar do que o cliente efetivamente receber (art. 50
do Código de Ética e Disciplina da OAB).

## 3. Declaração de hipossuficiência

Só se o cliente vai pedir justiça gratuita. Texto curto, na primeira pessoa do cliente:
qualificação, a declaração de que não tem condições de pagar as custas do processo e os
honorários sem prejuízo do próprio sustento e da família (art. 99, § 3º, do CPC), ciência
de que a declaração falsa tem consequência legal, local, data e assinatura.

Pessoa jurídica não tem a presunção dessa declaração: precisa provar a falta de recursos
(Súmula 481 do STJ). Avise o advogado em vez de gerar.

## Como gerar o .docx

1. Escreva cada documento em texto simples, num `.md` temporário, com este formato mínimo:
   `# Título` (centralizado), `## Seção` (negrito), `**trecho**` (negrito), linha em branco
   entre parágrafos, e `[PREENCHER: o que é]` em todo dado faltante.
2. Converta:
   ```bash
   uv run .claude/skills/kit-contratacao/scripts/gerar_docx.py <arquivo.md> <arquivo.docx>
   ```
   O script grifa em amarelo cada `[PREENCHER]` e diz quantos ficaram.
3. Salve em `<pasta do caso>/contratacao/`:
   - `1-procuracao-<slug>.docx`
   - `2-contrato-de-honorarios-<slug>.docx`
   - `3-declaracao-de-hipossuficiencia-<slug>.docx`
   Os `.md` temporários vão para `contratacao/fontes/`. Nada vai para fora da pasta do caso.
   Já existe arquivo com esse nome? Não sobrescreva: acrescente a data no nome.
4. Atualize a seção 10 do `briefing.md` ("Contrato assinado: não, minuta em
   contratacao/...") e acrescente um checkpoint: "### DD/MM/AAAA — Kit de contratação gerado".

## O que entregar

- Onde estão os arquivos.
- **A lista de cada `[PREENCHER]`**, por documento, para o advogado pedir ao cliente de uma
  vez só.
- Os poderes especiais que entraram, para ele conferir.
- "São minutas: revise antes de mandar assinar."
