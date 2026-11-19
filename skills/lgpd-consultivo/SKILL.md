---
name: lgpd-consultivo
description: 'Diagnóstico e parecer de LGPD para cliente empresa: checklist de adequação, tabela de lacunas com risco e prioridade, e plano de ação. Use quando o advogado disser "meu cliente quer se adequar à LGPD", "faz um diagnóstico LGPD da empresa", "checklist LGPD pro cliente", "parecer de adequação à LGPD", "o cliente recebeu um pedido de titular, e agora?", "a empresa está em dia com a LGPD?", "monta o gap analysis do cliente", "proposta de adequação LGPD".'
---

# LGPD consultivo: diagnóstico de cliente empresa

O advogado atende uma empresa e precisa dizer onde ela está em relação à LGPD, o que falta e o que
fazer primeiro. A skill conduz o levantamento, devolve a tabela de lacunas e a minuta do parecer.

Para o **próprio escritório**, a skill certa é `lgpd-escritorio`.

## Regras

1. **Tudo é MINUTA**, para revisão do advogado.
2. **Artigo só com certeza.** Dispositivo da LGPD que não estiver nesta skill: confira pelo
   `buscar_legislacao` do Conector DJEN (Lei 13.709/2018) ou marque `[conferir]`. Resolução da ANPD
   cite pelo número, com `[conferir em gov.br/anpd]` quando o detalhe pesar.
3. **Julgado só verificado.** Decisão da ANPD ou de tribunal só entra se recuperada nesta execução,
   com número, data e URL. Sem isso, `⚠️ NÃO VERIFICADO` e fora da conclusão.
4. **Dado do cliente não sai da máquina.** Nenhuma busca na web com nome, CNPJ ou dado da empresa.
   Pesquisa só com termo genérico.
5. **Não invente a empresa.** O que não foi respondido vira "não informado" na tabela, nunca
   suposição.

## Passo 1: levantamento

Se o advogado já tem material (questionário respondido, ata de reunião, política atual, contratos),
leia primeiro. `.docx`: `uv run ".claude/skills/ler-processo/scripts/texto_docx.py" "<arquivo>"
--inicio 200000`. PDF: `uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" texto "<arquivo>"
--paginas 1-N`.

Depois pergunte só o que faltou, em lista:

1. Ramo, porte, número de funcionários, se é ME/EPP ou startup.
2. Quem são os titulares: clientes pessoa física, funcionários, fornecedores, usuários de app ou site.
3. Trata dado sensível (saúde, biometria, religião, filiação sindical) ou de criança?
4. Onde ficam os dados (sistemas, nuvem, planilhas) e se algum fornecedor é estrangeiro.
5. Faz marketing com dado pessoal, perfil de consumo, decisão automatizada (crédito, preço)?
6. Já tem política de privacidade, encarregado, registro das operações, contrato com operadores?
7. Já houve incidente, reclamação de titular, notificação do Procon ou da ANPD?

## Passo 2: checklist

Avalie cada item como **atende**, **atende em parte**, **não atende** ou **não informado**:

| # | Tema | O que se verifica | Base |
|---|---|---|---|
| 1 | Inventário | Registro das operações de tratamento | art. 37 |
| 2 | Bases legais | Cada tratamento com base do art. 7º ou, se sensível, do art. 11 | arts. 7º e 11 |
| 3 | Legítimo interesse | Teste de balanceamento documentado onde for a base | art. 10 |
| 4 | Consentimento | Livre, informado, destacado, revogável, com prova | art. 8º |
| 5 | Transparência | Política e avisos com as informações do art. 9º | art. 9º |
| 6 | Direitos do titular | Canal e procedimento; resposta completa em até 15 dias | arts. 18 e 19 |
| 7 | Encarregado | Indicado e com contato público, ou dispensa justificada (Res. CD/ANPD 2/2022 e 18/2024) | art. 41 |
| 8 | Operadores | Contrato com cláusula de proteção de dados com quem trata em nome da empresa | arts. 39 e 42 `[conferir]` |
| 9 | Segurança | Medidas técnicas e administrativas proporcionais | art. 46 |
| 10 | Incidentes | Plano, registro e comunicação em 3 dias úteis (Res. CD/ANPD 15/2024) | art. 48 |
| 11 | Transferência internacional | Mecanismo válido para fornecedor no exterior (Res. CD/ANPD 19/2024 `[conferir]`) | arts. 33 a 36 |
| 12 | RIPD | Relatório de impacto onde o risco pede | art. 38 |
| 13 | Retenção e descarte | Prazo por categoria e eliminação ao fim do tratamento | arts. 15 e 16 |
| 14 | Criança e adolescente | Melhor interesse e consentimento parental quando for a base | art. 14 |
| 15 | Treinamento e governança | Equipe treinada, responsáveis, programa de boas práticas | art. 50 |

Sem material para avaliar o item, marque **não informado**. Não presuma que atende.

## Passo 3: tabela de lacunas

Só os itens que não atendem ou atendem em parte. Prioridade pela exposição, não pela facilidade:

| Prioridade | Lacuna | Risco concreto para esta empresa | Ação recomendada | Responsável | Prazo sugerido |
|---|---|---|---|---|---|
| Alta | | | | | |

- **Alta:** dado sensível ou de criança sem base, incidente sem plano, fornecedor estrangeiro sem
  mecanismo, ausência total de canal do titular. É o que gera sanção e dano primeiro.
- **Média:** política incompleta, contrato de operador sem cláusula, inventário parcial.
- **Baixa:** formalização e melhoria contínua (treinamento periódico, revisão anual).

"Risco concreto" é do caso, não genérico: "a clínica guarda prontuário em planilha compartilhada
por link aberto", não "risco de vazamento". As sanções do art. 52 entram uma vez, no parecer, sem
número de multa usado como ameaça.

"Prazo sugerido" é cronograma de projeto (30, 60, 90 dias), não prazo legal.

## Passo 4: parecer

Estrutura, curta:

1. **Escopo e fontes:** o que foi lido, quem respondeu, data, o que ficou de fora.
2. **Resumo executivo:** três a cinco linhas que o dono da empresa entende.
3. **Checklist** (Passo 2).
4. **Lacunas e prioridades** (Passo 3).
5. **Plano de ação** em fases: o que fazer em 30, 60 e 90 dias.
6. **Ressalvas:** itens não informados, `[conferir]` pendentes, o que depende de técnico de TI.

Escreva pela régua da skill `redacao-juridica`: frase curta, sem travessão, sem adjetivo sobrando.

## Saída

Na pasta do cliente (organização do `clientes/AGENTS.md`, se existir; senão, ao lado do material
lido), nunca dentro da `.claude/`:

- `lgpd-diagnostico-AAAA-MM-DD.md`: checklist, lacunas e parecer.

Topo: `MINUTA para revisão do advogado. Não informado: N itens. [conferir]: N.` Nunca sobrescreva
versão anterior. `.docx` só se pedido, por `pandoc` se instalado.

No chat: o resumo executivo, as lacunas de prioridade alta e as perguntas que ficaram sem resposta.

## O que esta skill NÃO faz

Não audita sistema nem segurança técnica, não faz RIPD completo (aponta quando ele é necessário e
pode estruturar o esqueleto), não comunica nada à ANPD, não redige toda a documentação de uma vez:
os documentos do plano de ação saem um a um, a pedido.
