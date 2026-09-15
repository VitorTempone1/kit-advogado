# JurisLabs OS

Esta pasta é o sistema. **Os dados dos clientes não moram aqui** — moram na pasta do escritório,
que fica fora deste repositório e não é um repositório git.

## Antes de trabalhar, leia o perfil

O perfil de prática deste escritório é o arquivo `CLAUDE.md` que está na **pasta do escritório**.
Ele traz nome do escritório, advogado responsável, OAB, áreas de atuação, regime de contagem de
prazo, tribunal principal e o tom das minutas.

O caminho da pasta do escritório está no `CLAUDE.md` global do usuário, numa linha começando com
`JurisLabs OS — pasta do escritório:`.

**Se o perfil não existir**, diga em uma frase que o sistema ainda não foi configurado e que ele
deve rodar `/setup`. Não tente adivinhar nome, OAB nem área de atuação.

## Regras que valem em qualquer tarefa desta pasta

1. Toda saída jurídica é **MINUTA**. O sistema não protocola, não assina, não peticiona.
2. Prazo é calculado por programa (`jurislabs-prazos`), nunca de cabeça — e, mesmo calculado,
   é apoio: a conferência no sistema do tribunal é do advogado.
3. Sem regime de prazo definido, **não calcule**: pergunte.
4. Citação sem número do julgado e sem URL do inteiro teor não entra em peça.
5. Precedente recente e de pé. Nunca julgado antigo havendo mais novo em sentido contrário.
6. Dado de cliente não entra em git e não sai da máquina. Nunca rode `git init` na pasta do
   escritório.
7. Ferramenta do Conector DJEN ausente: avise em uma frase que precisa do Conector, e siga com
   o que dá pra fazer sem ela. **Nunca invente** intimação, andamento ou julgado.

## Não escreva nesta pasta

Esta pasta é atualizada por `git pull`. Arquivo editado aqui vira conflito de merge no próximo
update, e o advogado não tem como resolver isso. O que o sistema produz vai para a pasta do
escritório.
