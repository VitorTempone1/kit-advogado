---
name: pjecalc-preparo
description: Prepara a liquidação no PJe-Calc sem rodar o PJe-Calc — lê a sentença ou o acórdão trabalhista, extrai os parâmetros (datas, prescrição, verbas, reflexos, FGTS, INSS, IR, honorários, custas, correção e juros) com a página de cada um, e monta o roteiro de lançamento tela a tela, apontando o que a decisão não disse. Opcionalmente confere um relatório exportado do PJe-Calc (PDF) contra esses parâmetros e lista as divergências. Use quando o advogado disser "/pjecalc-preparo", "vou liquidar a sentença", "me ajuda a lançar no PJe-Calc", "o que eu lanço no PJeCalc", "confere o cálculo do perito", "confere o cálculo da outra parte com a sentença".
---

# Preparo do PJe-Calc

O PJe-Calc é um programa desktop do CSJT: esta skill **não roda o PJe-Calc e não faz a conta**.
Ela entrega o que o advogado precisa ter na mão antes de abrir o programa, e confere o relatório
depois.

## Regra de ouro

- **Nenhum parâmetro sem página.** Cada item que você extrair da decisão leva a página
  (`"fonte": "sentença, p. 7"`). Não achou, deixe o campo vazio: o script marca "NÃO CONSTA NA
  DECISÃO". Nunca preencha por "o usual" (ex.: "deve ser IPCA-E, porque é o padrão").
- **Data e prescrição saem do script**, não de você.
- Acórdão que reformou a sentença: vale o acórdão naquilo que mudou. Registre as duas fontes.

## Passo 1 — ler a decisão

Se for PDF, use a ferramenta da skill `ler-processo` para achar e ler o dispositivo e a
fundamentação de cada verba:

```bash
uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" busca "CAMINHO/sentenca.pdf" --termo "dispositivo"
uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" texto "CAMINHO/sentenca.pdf" --paginas 1-15
```

## Passo 2 — preencher o JSON de parâmetros

Grave em `clientes/<cliente>/calculos/pjecalc-parametros.json`. Formato (campo pode ser texto
simples ou `{"valor": ..., "fonte": ...}`; prefira sempre o segundo):

```json
{
  "processo": "0000000-00.2023.5.03.0001",
  "reclamante": "Nome", "reclamada": "Empresa",
  "admissao": {"valor": "01/02/2015", "fonte": "sentença, p. 3"},
  "demissao": {"valor": "01/03/2023", "fonte": "p. 3"},
  "ajuizamento": {"valor": "10/05/2023", "fonte": "capa / certidão, p. 1"},
  "prescricao_quinquenal": {"valor": true, "fonte": "p. 5"},
  "salario": {"valor": "R$ 3.000,00", "fonte": "p. 4"},
  "carga_horaria": {"valor": "220 h/mês", "fonte": "p. 6"},
  "jornada": {"valor": "07h às 19h, seg a sáb, 1h de intervalo", "fonte": "p. 7"},
  "faltas_ferias": null,
  "verbas": [
    {"nome": "Horas extras 50%", "periodo": "10/05/2018 a 01/03/2023",
     "parametros": "excedentes da 8ª diária e 44ª semanal, divisor 220",
     "reflexos": ["DSR", "13º", "férias + 1/3", "aviso prévio", "FGTS + 40%"], "fonte": "p. 7-8"}
  ],
  "fgts": {"valor": "depósitos não recolhidos + multa de 40%", "fonte": "p. 10"},
  "inss": {"valor": "cota do empregado e do empregador, Súmula 368 TST", "fonte": "p. 12"},
  "ir": {"valor": "art. 12-A Lei 7.713/88, sem incidência sobre juros (OJ 400)", "fonte": "p. 12"},
  "honorarios": {"valor": "10% sobre o valor líquido, ao advogado do reclamante", "fonte": "p. 13"},
  "custas": {"valor": "2% sobre R$ 50.000,00, pela reclamada", "fonte": "p. 13"},
  "correcao": {"valor": "IPCA-E na fase pré-judicial e SELIC a partir do ajuizamento (ADC 58)", "fonte": "p. 11"},
  "juros": {"valor": "englobados na SELIC", "fonte": "p. 11"}
}
```

Mostre o JSON (ou uma tabela dele) ao advogado e peça conferência **antes** do passo 3.

## Passo 3 — gerar o roteiro

```bash
uv run ".claude/skills/pjecalc-preparo/scripts/pjecalc_preparo.py" roteiro "clientes/fulano/calculos/pjecalc-parametros.json"
```

Sai o checklist na ordem das telas do PJe-Calc (Dados do Cálculo → Histórico Salarial → Faltas e
Férias → Verbas → Cartão de Ponto → FGTS → Contribuição Social → Imposto de Renda → Honorários →
Custas → Correção, Juros e Multa → Liquidar), com:

- prescrição quinquenal calculada (ajuizamento − 5 anos; Súmula 308, I, TST; art. 7º, XXIX, CF) e
  alerta de bienal (com lembrete da projeção do aviso, OJ 83 SDI-1);
- cada campo vazio marcado "NÃO CONSTA NA DECISÃO" — candidato a embargos de declaração, que é
  decisão do advogado;
- alerta da Lei 14.905/2024 para decisão anterior a 30/08/2024 (TST, E-ED-RR-713-03.2010.5.04.0029).

Grave em `clientes/<cliente>/calculos/pjecalc-roteiro-AAAA-MM-DD.md`.

## Passo 4 (opcional) — conferir o relatório do PJe-Calc

Quando o advogado tiver o PDF do relatório (o dele, o do perito ou o da parte contrária):

```bash
uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" texto "CAMINHO/relatorio-pjecalc.pdf" --paginas 1-999 > "clientes/fulano/calculos/relatorio-pjecalc.txt"
uv run ".claude/skills/pjecalc-preparo/scripts/pjecalc_preparo.py" conferir "clientes/fulano/calculos/pjecalc-parametros.json" "clientes/fulano/calculos/relatorio-pjecalc.txt"
```

O script procura no relatório: as datas, o marco da prescrição, cada verba e seus reflexos, os índices de correção
e juros, o percentual da multa do FGTS e dos honorários. Devolve a tabela item a item com "ok" ou
"NÃO ACHEI". Explique ao advogado que "não achei" pode ser divergência real ou só redação
diferente, e que a conferência é de **presença** de parâmetros: não refaz a conta.

Grave em `clientes/<cliente>/calculos/pjecalc-conferencia-AAAA-MM-DD.md`.

## Entrega

No chat: o que a decisão não disse (primeiro, porque é o que trava a liquidação), a prescrição, a
lista de verbas com reflexos e, se houve conferência, as divergências. Termine **sempre** com:
"Conferir antes de juntar. Não substitui o PJeCalc nem o perito."

## O que esta skill NÃO faz

Não roda nem controla o PJe-Calc, não calcula valor, não interpreta a decisão por "costume" e não
decide se cabe embargos. Nomes de tela seguem o PJe-Calc Cidadão: `[conferir na sua versão]`.
Não lê PDF escaneado sem camada de texto (veja o passo 4 da skill `ler-processo`).

## Verificação

`python3 .claude/skills/pjecalc-preparo/scripts/test_pjecalc_preparo.py` — prescrição (inclusive
29/02), bienal, campos omitidos apontados, e conferência que acha as 5 divergências plantadas
(verba ausente, dois reflexos ausentes, SELIC ausente, honorários de 15% contra 10%).
