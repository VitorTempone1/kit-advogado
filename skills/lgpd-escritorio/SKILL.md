---
name: lgpd-escritorio
description: 'Adequação do PRÓPRIO escritório à LGPD, com o escritório como controlador dos dados de clientes, partes contrárias, testemunhas, funcionários e contatos. Monta o inventário de dados, a base legal de cada tratamento, a política de privacidade, o termo de consentimento quando cabe, o plano de resposta a incidente e a decisão sobre o encarregado. Use quando o advogado disser "quero adequar meu escritório à LGPD", "preciso de política de privacidade pro site do escritório", "meu escritório precisa de encarregado?", "e se vazar dado de cliente?", "faz o mapeamento de dados do escritório", "plano de incidente", "termo de consentimento do escritório".'
---

# LGPD do próprio escritório

O escritório trata dado pessoal o dia inteiro: cliente, parte contrária, testemunha, funcionário,
estagiário, contato que chegou pelo Instagram. Para esses dados, **o escritório é o controlador**
(LGPD, art. 5º, VI). Esta skill monta, com o advogado, o kit mínimo de adequação e grava os
documentos na pasta do escritório.

Para adequação de **cliente empresa**, a skill certa é `lgpd-consultivo`.

## Regras

1. **Tudo é MINUTA.** Os documentos saem para revisão do advogado, nunca "prontos para publicar".
2. **Artigo só com certeza.** O que está nesta skill foi conferido. Qualquer outro dispositivo,
   resolução ou número que você for escrever: confira pelo `buscar_legislacao` do Conector DJEN
   (lei federal) ou marque `[conferir]` no texto. Resolução da ANPD não está no LexML: cite pelo
   número e deixe `[conferir em gov.br/anpd]` quando for usar redação literal.
3. **Nada sai da máquina por sua conta.** Nenhuma busca na web com nome de cliente, CPF ou número
   de processo. Pesquisa, se precisar, só com termo genérico ("Resolução CD/ANPD 15/2024").
4. **Não invente o escritório.** Nome, CNPJ, endereço, e-mail e quem decide saem do `AGENTS.md` da
   raiz e de `_contexto/escritorio.md`. Faltou, pergunte. Sem perfil, diga que `/setup` resolve e
   pergunte o mínimo (nome, CNPJ ou CPF do titular, e-mail de contato).

## Passo 1: entrevista curta

Pergunte de uma vez, em lista, e aceite resposta incompleta:

1. Quantas pessoas trabalham no escritório (sócios, associados, estagiários, secretária)?
2. É sociedade enquadrada como microempresa ou empresa de pequeno porte, ou advocacia individual?
3. Onde moram os dados: computador, pasta em nuvem (Google Drive, OneDrive, Dropbox), e-mail,
   WhatsApp, sistema de gestão, planilha, papel?
4. Atua em área com **dado sensível** (previdenciário e saúde, família, criminal, trabalhista com
   atestado, ações com dado de criança)?
5. Tem site ou formulário de contato? Faz marketing (lista de e-mail, Instagram, anúncio)?
6. Usa inteligência artificial com documento de cliente (este próprio assistente incluído)?
7. Já teve vazamento, perda de celular, e-mail enviado ao destinatário errado?

## Passo 2: inventário de dados

Monte a tabela, uma linha por tratamento. Sugira as linhas típicas de escritório e deixe o
advogado cortar ou acrescentar:

| Tratamento | Titulares | Dados | Sensível? | Onde fica | Com quem compartilha | Base legal | Guarda até |
|---|---|---|---|---|---|---|---|
| Atendimento e contrato de honorários | clientes | identificação, contato, financeiro | | | | | |
| Condução do processo | clientes, parte contrária, testemunhas | o que os autos trazem | pode ser | | tribunal, perito, correspondente | | |
| Folha e vínculo | funcionários, estagiários | identificação, bancário, saúde (atestado) | sim | | contabilidade | | |
| Prospecção e marketing | contatos, seguidores | nome, telefone, e-mail | | | plataforma de anúncio | | |
| Cobrança e financeiro | clientes | financeiro | | | banco, contabilidade | | |

Para cada ferramenta que guarda ou processa dado fora da máquina (nuvem, e-mail, WhatsApp,
provedor de IA), anote **em que país** o fornecedor processa. Fornecedor estrangeiro é
transferência internacional (arts. 33 a 36), e a regulamentação das cláusulas-padrão é a
Resolução CD/ANPD 19/2024 `[conferir]`. Não esconda isso do advogado: o próprio Claude processa
o texto que recebe em servidor do fornecedor.

A coluna "Guarda até" não tem número fixo em lei para escritório. Proponha o critério (fim do
mandato mais o prazo das pretensões que o documento pode provar) e deixe o número para o advogado
decidir, marcado `[definir]`.

## Passo 3: base legal por tratamento

Uma base por linha, a mais sólida, com o motivo em uma frase. Mapa do que costuma servir:

- **Dado comum (art. 7º):** execução de contrato com o titular (inciso V) para o cliente;
  exercício regular de direitos em processo judicial, administrativo ou arbitral (inciso VI) para
  parte contrária e testemunha; cumprimento de obrigação legal ou regulatória (inciso II) para
  fisco, folha e contabilidade; legítimo interesse (inciso IX, com art. 10) para prospecção e
  contato de quem já se relacionou com o escritório; consentimento (inciso I) só quando nenhuma
  outra base cabe.
- **Dado sensível (art. 11):** consentimento específico e destacado (inciso I), ou, sem
  consentimento, as hipóteses do inciso II, entre elas o exercício regular de direitos, inclusive
  em contrato e em processo (alínea "d"). Legítimo interesse **não** serve para dado sensível.
- **Criança e adolescente (art. 14):** melhor interesse; consentimento de um dos pais ou
  responsável quando o consentimento for a base.

Consentimento não é a base "mais segura": ele pode ser revogado a qualquer tempo (art. 8º, § 5º).
Quando houver base legal sem consentimento, prefira-a.

## Passo 4: os documentos

Gere só o que o caso pede. Sempre:

1. **Inventário e bases legais** (a tabela dos passos 2 e 3).
2. **Política de privacidade** do escritório, em linguagem de cliente, com o que o art. 9º manda
   informar: finalidade, forma e duração do tratamento, identificação e contato do controlador,
   com quem compartilha e por quê, responsabilidades, e os direitos do art. 18 com o canal para
   exercê-los. Inclua o prazo de resposta ao titular: confirmação e acesso em formato simplificado
   de imediato, ou declaração completa em até 15 dias (art. 19). Diga que o sigilo profissional
   do advogado limita o que se entrega a terceiros.
3. **Plano de resposta a incidente** (ver Passo 5).
4. **Decisão sobre o encarregado** (ver Passo 6).

Quando cabível:

5. **Termo de consentimento**, só para tratamento sem outra base: lista de e-mail e newsletter,
   uso de depoimento, foto ou caso do cliente em divulgação (lembrar o Provimento 205/2021 da
   OAB, o mesmo que a skill `post-instagram` confere), dado sensível fora do processo. Termo destacado, uma
   finalidade por item, com o modo de revogar.
6. **Cláusula LGPD para o contrato de honorários** e para o contrato com fornecedor que trata dado
   pelo escritório (correspondente, contabilidade, sistema).
7. **Regras internas curtas** para a equipe: senha e dois fatores, nada de documento de cliente no
   WhatsApp pessoal, bloqueio de tela, descarte de papel, quem avisar em incidente.

## Passo 5: plano de incidente

Arts. 48 e 49 da LGPD e Resolução CD/ANPD 15/2024 (regulamento de comunicação de incidente).

- **Quando comunicar:** incidente que possa acarretar risco ou dano relevante aos titulares. A
  resolução detalha os critérios (dado sensível, de criança, financeiro, de autenticação, em larga
  escala, entre outros) `[conferir lista na resolução]`.
- **Prazo:** 3 dias úteis contados do conhecimento do incidente, para a ANPD e para os titulares
  afetados (Res. 15/2024). Agente de pequeno porte tem prazo em dobro pela Resolução CD/ANPD 2/2022
  `[conferir se o dobro se mantém para o caso]`.
- **Registro:** todo incidente se registra internamente, comunicado ou não, e o registro se guarda
  por prazo fixado na resolução `[conferir: 5 anos]`.
- **Roteiro no documento:** quem percebe avisa a quem (nome e telefone); conter (trocar senha,
  revogar acesso, bloquear aparelho remotamente); avaliar (quais dados, quantos titulares, se é
  sensível); decidir se comunica e registrar o porquê; comunicar pelo formulário da ANPD no gov.br;
  avisar os titulares em linguagem simples; corrigir a causa.

Em escritório de advocacia, incidente com dado de cliente também é questão de sigilo profissional:
o plano lembra que a comunicação a titular e à ANPD não pode revelar estratégia nem conteúdo
protegido pelo sigilo além do necessário.

## Passo 6: encarregado

- Regra geral: o controlador indica encarregado e divulga identidade e contato de forma clara,
  de preferência no site (art. 41). A Resolução CD/ANPD 18/2024 regulamenta a atuação: pode ser
  pessoa física ou jurídica, de dentro ou de fora, e precisa de autonomia e recursos `[conferir
  redação]`.
- **Dispensa:** o agente de tratamento de pequeno porte fica dispensado de indicar encarregado pela
  Resolução CD/ANPD 2/2022, mas tem de manter um canal de comunicação com o titular `[conferir
  art. 11]`. A dispensa **não vale** para quem faz tratamento de alto risco, e escritório que
  trata dado sensível em volume (previdenciário, saúde, família) pode cair nessa exclusão.
  Diga isso ao advogado e deixe a decisão com ele, registrada no documento.
- Mesmo dispensado, recomende nomear alguém (pode ser o próprio sócio) e publicar o contato. Custa
  pouco e responde ao titular.

## Saída

Grave na pasta do escritório, fora da `.claude/`, em `lgpd/` na raiz (crie se não existir; se o
`AGENTS.md` mapear uma frente administrativa, dentro dela):

```
lgpd/
├── 01-inventario-e-bases-legais-AAAA-MM-DD.md
├── 02-politica-de-privacidade-AAAA-MM-DD.md
├── 03-plano-de-incidente-AAAA-MM-DD.md
├── 04-encarregado-decisao-AAAA-MM-DD.md
└── 05-termo-de-consentimento-...md   (só se cabível)
```

Topo de cada arquivo: `MINUTA para revisão do advogado. Itens [conferir] e [definir] pendentes: N.`
Nunca sobrescreva versão anterior: arquivo novo com a data.

Se o advogado pedir `.docx`: com `pandoc` instalado, `pandoc arquivo.md -o arquivo.docx`. Sem ele,
entregue o `.md` e diga em uma frase que dá para colar no Word.

No chat: lista do que foi gerado, quantos `[conferir]` e `[definir]` ficaram, e as três decisões
que só o advogado toma (prazo de guarda, encarregado, o que entra no termo de consentimento).

## O que esta skill NÃO faz

Não publica nada no site, não comunica incidente à ANPD, não faz RIPD completo (aponta quando ele
é recomendável), não audita segurança técnica de computador ou nuvem, não substitui a leitura das
resoluções da ANPD vigentes.
