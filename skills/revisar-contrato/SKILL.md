---
name: revisar-contrato
description: 'Lê um contrato (.docx, .pdf ou texto colado), pergunta de que lado está o cliente, marca as cláusulas de risco para esse lado e sugere redação alternativa, numa tabela cláusula, risco e sugestão. Direito brasileiro: Código Civil, CDC quando houver relação de consumo, CPC no foro. Use quando o advogado disser "revisa esse contrato", "o cliente vai assinar isso, tem pegadinha?", "analisa o contrato de prestação de serviços", "quais cláusulas são perigosas pro meu cliente?", "contrato de locação pra revisar", "me dá as sugestões de alteração", "faz o redline", "o fornecedor mandou a minuta do contrato".'
---

# Revisar contrato

O advogado aponta um contrato. Você devolve, cláusula a cláusula, o que expõe o cliente dele e
como reescrever, pronto para virar contraproposta.

## Regras

1. **Saída é MINUTA**, para revisão do advogado.
2. **Lado primeiro.** Sem saber quem é o cliente (contratante ou contratado, locador ou locatário,
   comprador ou vendedor), não revise: a mesma cláusula é proteção para um lado e risco para o
   outro. Pergunte antes de ler a fundo.
3. **Cite o contrato literalmente.** Toda linha da tabela traz o número da cláusula e o trecho
   exato. Cláusula que você não achou no texto não entra.
4. **Artigo só com certeza.** Os dispositivos desta skill foram conferidos; os marcados `[conferir]`
   mudaram há pouco ou dependem de redação. Outro dispositivo: `buscar_legislacao` do Conector DJEN
   ou `[conferir]`. Julgado só se recuperado nesta execução, com número, data e URL; senão
   `⚠️ NÃO VERIFICADO`. Nunca escreva "a jurisprudência tende a" sem um julgado recuperado: sem ele,
   o argumento fica só na lei.
5. **Dado do cliente não sai da máquina.** Nenhuma busca na web com nome de parte, CNPJ ou valor.

## Passo 1: ler e perguntar

Leitura do arquivo, na máquina:

- `.docx`: `uv run ".claude/skills/ler-processo/scripts/texto_docx.py" "<arquivo>" --inicio 400000`
- `.pdf`: `uv run ".claude/skills/ler-processo/scripts/mapear_pdf.py" texto "<arquivo>" --paginas 1-N`
  (se o mapa disser que há página sem camada de texto, avise: a cláusula ali não foi lida)

Pergunte, numa mensagem só:

1. **Qual lado é o seu cliente?**
2. O que mais preocupa o cliente (preço, prazo, saída do contrato, responsabilidade, sigilo)?
3. Há relação de consumo (cliente pessoa física ou destinatário final, contra fornecedor)?
4. O contrato é de adesão (modelo fechado) ou está em negociação?
5. Tem prazo para assinar?

Resposta parcial basta: siga e registre a suposição no topo.

## Passo 2: leitura inteira antes de marcar

Leia o contrato **todo** antes de apontar risco. Cláusulas se compensam: a multa alta de um lado
pode estar equilibrada por um teto de responsabilidade em outra cláusula. Identifique o tipo de
contrato (prestação de serviço, locação, compra e venda, licença de software, parceria,
franquia...), porque o tipo muda o que importa.

## Passo 3: o que verificar

Para o lado do cliente, no mínimo:

| Tema | O que olhar | Base que costuma servir |
|---|---|---|
| Objeto e escopo | Obrigação vaga, entregável sem critério de aceite | CC 422 (boa-fé) |
| Preço e reajuste | Índice, periodicidade, reajuste unilateral | CC 489 na compra e venda (preço ao arbítrio de uma parte) |
| Pagamento e mora | Multa, juros, correção | CC 406 `[conferir redação após Lei 14.905/2024]`; CDC 52, § 1º (multa de mora de 2% no crédito ao consumidor) |
| Cláusula penal | Valor desproporcional, cumulação | CC 412 (teto no valor da obrigação principal) e 413 (redução equitativa) |
| Responsabilidade | Exclusão total, teto irrisório, só para um lado | CDC 51, I (nula no consumo); CC 393 (caso fortuito) |
| Prazo e renovação | Renovação automática com aviso curto | CC 473 e parágrafo único (resilição e investimento feito) |
| Rescisão | Saída só para um lado, sem cura, multa só para um lado | CC 473, 474 e 475 |
| Exclusividade e não concorrência | Sem prazo, sem território, sem contrapartida | CC 421 e 422 |
| Propriedade intelectual | Cessão ampla, inclusive do que o cliente já tinha | Lei 9.610/98 e Lei 9.609/98, conforme o caso `[conferir artigo]` |
| Confidencialidade | Só para um lado, sem prazo, sem exceções usuais | CC 422 |
| Dados pessoais | Quem é controlador e operador, incidente, devolução | LGPD arts. 37, 39, 46 e 48 |
| Garantias | Fiança sem renúncia clara, garantia em excesso | CC 818 e seguintes; Lei 8.245/91 art. 37 na locação |
| Foro e solução | Foro distante do cliente, arbitragem imposta | CPC 63 `[conferir redação após Lei 14.879/2024]`; Lei 9.307/96 art. 4º, § 2º (arbitragem em adesão) |
| Adesão | Cláusula ambígua, renúncia antecipada de direito | CC 423 e 424 |
| Consumo | Cláusula abusiva, falta de destaque na limitação | CDC 51 e 54, §§ 3º e 4º |

Se for contrato paritário entre empresas, lembre a presunção de paridade e simetria (CC 421-A):
o argumento de abusividade é mais fraco ali, e a sugestão deve ser negociação, não nulidade.

## Passo 4: classificar

- **Vermelho:** expõe o cliente a perda grande ou sem teto, ou é nula/abusiva (no consumo, CDC 51).
  Não assinar sem mudar.
- **Amarelo:** desequilibrada, mas comum no mercado. Negociar, com posição de recuo.
- **Verde:** aceitável ou favorável. Só mencione se o advogado pediu revisão completa.
- **Ausente:** cláusula que deveria existir e não existe (ex.: sem teto de responsabilidade, sem
  cláusula de dados pessoais quando há tratamento).

## Passo 5: redação alternativa

Para cada vermelho e amarelo: redação pronta para colar, no mesmo registro do contrato, sem
travessão, e uma posição de recuo para o amarelo. Justificativa em uma frase que dê para mandar à
outra parte, sem tom de ataque.

## Saída

Grave ao lado do contrato (ou na pasta do cliente, organização do `clientes/AGENTS.md`), nunca
dentro da `.claude/`: `<nome-do-contrato>-revisao-AAAA-MM-DD.md`. Nunca sobrescreva revisão
anterior.

```markdown
# MINUTA: revisão de contrato
Não é parecer final. Conferir antes de enviar à outra parte.

Contrato: <arquivo> · <tipo> · lado do cliente: <lado> · consumo: sim/não · adesão: sim/não
Suposições: <o que o advogado não respondeu e você supôs>
Não lido: <páginas sem texto, anexos não enviados>

## Os 3 pontos que mais importam
1. ...

## Tabela
| Cláusula | Trecho | Risco para o cliente | Nível | Sugestão de redação | Recuo |
|---|---|---|---|---|---|

## Cláusulas ausentes
## Perguntas para o cliente
```

No chat: os três pontos que mais importam e a contagem por nível. A tabela fica no arquivo.

Se o advogado pedir o contrato já alterado, gere uma cópia `.md` com as mudanças marcadas
(**negrito** para inclusão, ~~tachado~~ para exclusão). O `.docx` original nunca é alterado.

## O que esta skill NÃO faz

Não assina, não envia à outra parte, não altera o arquivo original, não faz due diligence da outra
parte, não calcula valor de multa ou correção, não revisa a parte tributária do contrato.
