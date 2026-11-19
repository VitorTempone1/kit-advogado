"""Teste de fumaça das skills do kit: roda cada skill com o Claude de verdade (claude -p),
numa pasta de escritório fictícia montada como o /setup deixaria, e confere o arquivo que
ela tinha de entregar.

    python3 testes/fumaca_skills.py                     # todas, 4 de cada vez
    python3 testes/fumaca_skills.py calculo-rescisao seo-local
    python3 testes/fumaca_skills.py --saida /caminho/da/evidencia

Nada aqui é dado de cliente: escritório, clientes, CPFs e documentos são inventados.
Sem bypass de permissão: cada skill roda com a lista de ferramentas que precisa
(--allowedTools); o que não está na lista é negado, e a negação aparece no log.
Sem MCP (--strict-mcp-config): o Conector DJEN fica ausente de propósito, para provar
que a skill avisa em vez de inventar. Sem as configurações do usuário (--setting-sources
project,local): roda como na máquina do aluno, só com o kit.

Cada skill tem até 2 turnos: o pedido do "Peça assim" do site e, se o arquivo esperado
não saiu (a skill perguntou algo), a resposta que um advogado daria. A pergunta do
turno 1 fica no log para julgar se fazia sentido.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
HOJE = time.strftime("%d/%m/%Y")

# --------------------------------------------------------------------------- PDF mínimo

def pdf(caminho, texto):
    """PDF de verdade, com camada de texto (Helvetica, latin-1), uma página a cada 45 linhas."""
    linhas = texto.strip("\n").split("\n")
    paginas = [linhas[i:i + 45] for i in range(0, len(linhas), 45)] or [[""]]
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", None,
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"]
    kids = []
    for pg in paginas:
        corpo = "BT /F1 10 Tf 50 800 Td 13 TL\n"
        for l in pg:
            l = l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            corpo += "(%s) '\n" % l
        corpo += "ET"
        dados = zlib.compress(corpo.encode("latin-1", "replace"))
        objs.append(("<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(dados)).encode() + dados + b"\nendstream")
        n_cont = len(objs)
        objs.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents %d 0 R "
                    "/Resources << /Font << /F1 3 0 R >> >> >>" % n_cont)
        kids.append(len(objs))
    objs[1] = "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % k for k in kids), len(kids))
    out = bytearray(b"%PDF-1.4\n")
    pos = []
    for i, o in enumerate(objs, 1):
        pos.append(len(out))
        out += b"%d 0 obj\n" % i + (o if isinstance(o, bytes) else o.encode()) + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % p for p in pos)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho).write_bytes(bytes(out))


PNG_VAZIO = bytes.fromhex(
    "89504e470d0a1a0a0000000d4948445200000001000000010806000000"
    "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082")

# --------------------------------------------------------------------------- o escritório

PERFIL = """# Perfil do escritório: Lima Advocacia (FICTÍCIO, teste do kit)

Este é o manual que o Claude lê antes de trabalhar aqui. É texto normal: se algo mudar, abra e
edite. Rode /setup de novo pra refazer, sem perder nada.

## O escritório
Advogado: Ana Fictícia Lima, OAB/MG 999.999
Clientes: os dois
Equipe: só ele
Endereço profissional: Rua dos Testes, 100, sala 2, Centro, Contagem/MG
E-mail: contato@lima-ficticia.adv.br

## Áreas e regime de prazo
Trabalhista; Cível (contratos e locação); Previdenciário
Regime de contagem: CLT (trabalhista, dias úteis); CPC (cível, dias úteis); previdenciário judicial no JEF
REGRA: com mais de um regime na casa, o Claude NUNCA assume o regime pelo tipo do caso. Pergunta antes de
calcular qualquer prazo, e passa o regime ao calcular_prazo.

## Onde peticiona
Sistemas: PJe (TRT3 e TJMG)
Tribunal e comarca principal: TRT da 3ª Região e TJMG, comarca de Contagem
Feriado forense local: conferir sempre na portaria do tribunal. É a maior fonte de erro de prazo.

## Como escrever
Tom: técnico, direto, sem rebuscamento
Peça mais frequente: petição inicial trabalhista

## O sistema
As regras do sistema estão em .claude/CLAUDE.md, que se atualiza sozinho. Não edite nada em .claude/.
Conector: não ligado
Frentes:
- Casos: clientes/
- Marketing: marketing/
Antes de trabalhar numa frente, leia o AGENTS.md dela.
Registro da entrevista: _contexto/escritorio.md. Mapa das pastas: _contexto/pastas.md.
Decisões: anote em _memoria/decisoes.md, com data.

## Travas que valem sempre aqui
1. Toda saída jurídica é MINUTA. O Claude não protocola, não assina, não peticiona.
   O último clique é sempre do advogado.
2. Prazo calculado é apoio. Confira no sistema do tribunal antes de confiar.
3. Citação sem número do julgado e URL do inteiro teor não entra em peça.
4. Precedente recente e de pé. Nunca julgado antigo havendo mais novo em sentido contrário.
5. Nada de prazo muda em lote sem conferência item a item.
6. Sem o Conector, o Claude não busca intimação, processo nem lei, e avisa em vez de inventar.

## Sobre esta pasta
Esta pasta guarda dado de cliente e por isso NÃO é um repositório git, de propósito.
O dado do escritório fica nesta máquina.
"""

BASE = {
    "AGENTS.md": PERFIL,
    "CLAUDE.md": "@AGENTS.md\n@.claude/CLAUDE.md\n",
    "_contexto/escritorio.md": """O perfil que vale é o `AGENTS.md` da raiz. Aqui fica o registro da entrevista.

Setup em 10/11/2026 (teste do kit, tudo fictício).
A: Ana Fictícia Lima, OAB/MG 999.999, Lima Advocacia, Contagem/MG.
C: trabalhista (reclamante, a maior parte), cível (locação e contratos), previdenciário (aposentadoria).
Clientes: pessoas físicas da região metropolitana de BH e pequenos comércios.
Tribunal: TRT3 e TJMG, comarca de Contagem. Conector: não ligado.
Pasta antiga: nenhuma (começou do zero).

## Personalização (oferta para um próximo encontro)
Nada achado: sem logo, sem posts antigos. Oferta de marca registrada; marca.md não criado.
""",
    "_contexto/pastas.md": "# Mapa das pastas\n\nComeçou do zero em 10/11/2026.\n",
    "_memoria/decisoes.md": "# Decisões do escritório\n\nUma linha por decisão, com data, a mais nova embaixo.\n\n"
                            "- 2026-11-10: escritório montado pelo /setup. Pastas antigas: nenhuma. Frentes: clientes, marketing.\n",
    "_triagem/.gitkeep": "",
    "desfazer/.gitkeep": "",
    "transcricoes/.gitkeep": "",
    "tutoriais/.gitkeep": "",
    "clientes/CLAUDE.md": "@AGENTS.md\n",
    "clientes/AGENTS.md": """# Casos: como esta pasta funciona

Um caso por cliente.

## Como está organizada
Um caso por cliente, em `clientes/<nome>/` (minúsculas, sem acento, com hífen). Caso novo nasce com
`briefing.md` (cliente, contra quem, o que aconteceu, o que quer, número do processo, prazos, próximo passo).
Dentro do caso: `documentos/` (o que o cliente mandou), `pecas/`, `decisoes/`, `calculos/`, `reuniao/`, `mensagens/`.

## Como funciona hoje
Conte aqui como funciona.

## Regras desta pasta
A regra daqui especifica a da raiz; nunca afrouxa.
""",
    "marketing/CLAUDE.md": "@AGENTS.md\n",
    "marketing/AGENTS.md": """# Marketing: como esta pasta funciona

Posts, artes, textos do site e do perfil do Google.

## Como está organizada
`posts/`, `carrosseis/`, `capas/`, `textos/`, `site/`, `seo-local/`.

## Como funciona hoje
Conte aqui como funciona.

## Regras desta pasta
Todo post passa pela checagem do Provimento 205/2021 antes de publicar.
A regra daqui especifica a da raiz; nunca afrouxa.
""",
}


def briefing(cliente, pasta, corpo):
    return ("# Briefing — %s\n\n> **Documento vivo.** Nunca reescrever o histórico. Fato novo = novo checkpoint no fim, com data.\n\n"
            "| | |\n|---|---|\n| **Cliente** | %s |\n| **Escritório** | Lima Advocacia |\n| **Pasta** | `%s` |\n"
            "| **Responsável** | Ana Fictícia Lima |\n\n---\n\n%s\n\n---\n\n## 11. Checkpoints\n\n"
            "### 10/11/2026 — Primeiro atendimento\n\nCaso aberto (teste do kit, tudo fictício).\n" % (cliente, cliente, pasta, corpo))


JOAO = briefing("João Pereira (fictício)", "clientes/joao-pereira/", """## 1. Identificação
- **Qualificação:** João Pereira, brasileiro, casado, auxiliar de logística, CPF 111.444.777-35 (fictício), Contagem/MG
- **Parte contrária:** Transportes Exemplo Ltda (fictícia), PJ, CNPJ 00.000.000/0001-00

## 2. Classificação da demanda
- **Área:** trabalhista · **Polo:** autor (reclamante) · **Natureza:** contencioso
- **Já existe processo?** ainda não

## 3. Fatos — linha do tempo
| Data | Fato | Fonte | Provado? |
|---|---|---|---|
| 10/02/2021 | Admissão como auxiliar de logística | CTPS digital | doc |
| 15/09/2026 | Dispensa sem justa causa comunicada; aviso prévio indenizado | carta de dispensa | doc |
| 15/09/2026 | Último salário-base: R$ 3.200,00 (fixo, sem comissão) | holerite de agosto/2026 | doc |
| — | Férias: gozou todas as férias vencidas; nenhum período vencido em aberto | relato + recibos | doc |
| — | Saldo do FGTS na data da dispensa: R$ 11.500,00 | extrato da Caixa | doc |
| jun/2026 | Fazia hora extra quase todo dia, inclusive um domingo | cartão de ponto (documentos/) | doc |

## 4. O que o cliente pediu
- **Pedido literal:** "quero saber se a empresa me pagou certo e quanto dá de hora extra"
""")

JOAO_PROC = briefing("João Pereira (fictício)", "clientes/joao-pereira/", """## 1. Identificação
- **Qualificação:** João Pereira, brasileiro, casado, motorista, CPF 111.444.777-35 (fictício), Contagem/MG
- **Parte contrária:** Transportes Exemplo Ltda (fictícia)

## 2. Classificação da demanda
- **Área:** trabalhista · **Polo:** autor (reclamante)
- **Já existe processo?** 0010001-00.2024.5.03.0030, 2ª VT de Contagem, PJe (fictício), ajuizado em 10/05/2024
- Contrato: 10/02/2018 a 01/03/2024, último salário R$ 3.000,00

## 3. Fatos
| Data | Fato | Fonte | Provado? |
|---|---|---|---|
| 20/03/2025 | Sentença de procedência parcial | decisoes/ | doc |
""")

MARIA_REUNIAO = """# Reunião com Maria Souza (FICTÍCIA) — 18/11/2026, presencial, 40 min

Advogada: Bom dia, Dona Maria. Me conta o que aconteceu.
Maria: Eu trabalhei de 2012 até agosto deste ano na Loja Modelo Ltda, de vendedora. Fui
mandada embora no dia 20 de agosto, sem justa causa. Só que eu estava grávida, de uns dois meses,
e eu já tinha contado pra gerente, a Paula, no começo de agosto, pelo WhatsApp.
Advogada: A senhora tem esse WhatsApp?
Maria: Tenho o print. E tenho o ultrassom de 05/08/2026.
Advogada: Pagaram a rescisão?
Maria: Pagaram no dia 29 de agosto, mas eu acho que faltou coisa. Não me deram o papel do seguro
desemprego direito. Eu quero voltar a trabalhar lá, ou receber o que é meu.
Advogada: Tinha horas extras?
Maria: Às vezes ficava até mais tarde no fim do mês, sem receber. Não tenho cartão de ponto, eles
não davam. A colega Juliana viu.
Advogada: Me manda RG, CPF, comprovante de endereço, CTPS digital, o TRCT, os holerites, o print
e o ultrassom.
Maria: Mando sim. CPF é 111.444.777-35, moro na Rua das Flores, 10, Contagem. Sou solteira.
Advogada: A ação a gente entra no TRT3. Volto com a senhora sobre honorários.
"""

MARIA = briefing("Maria Souza (fictícia)", "clientes/maria-souza/", """## 1. Identificação
- **Qualificação:** Maria Souza, brasileira, solteira, vendedora, CPF 111.444.777-35 (fictício), RG MG-00.000.000,
  Rua das Flores, 10, Centro, Contagem/MG, CEP 32000-000
- **Contato:** WhatsApp (31) 90000-0000 (fictício)
- **Parte contrária:** Loja Modelo Ltda (fictícia), PJ, CNPJ 00.000.000/0001-00

## 2. Classificação da demanda
- **Área:** trabalhista · **Sub-área:** estabilidade da gestante · **Polo:** autor (reclamante)
- **Já existe processo?** 0010000-00.2026.5.03.0029, 1ª Vara do Trabalho de Contagem, PJe (fictício)
- **Rito:** ordinário · **Valor da causa:** R$ 80.000,00

## 3. Fatos — linha do tempo
| Data | Fato | Fonte | Provado? |
|---|---|---|---|
| 01/01/2012 | Admissão como vendedora | CTPS | doc |
| 05/08/2026 | Ultrassom confirma gestação | exame | doc |
| 20/08/2026 | Dispensa sem justa causa | TRCT | doc |
| 25/09/2026 | Ajuizamento da reclamação | PJe | doc |

## 4. O que o cliente pediu × o que quer
- **Pedido literal:** reintegração ou indenização do período de estabilidade
- **Interesse real:** dinheiro para o período da gravidez; não quer voltar à loja de verdade

## 10. Honorários e contrato
- **Modalidade:** êxito, 30% do proveito econômico (definido pela advogada)
- **Contrato assinado:** não · **Procuração:** não
""")

SENTENCA_MARIA = """PODER JUDICIÁRIO - JUSTIÇA DO TRABALHO (DOCUMENTO FICTÍCIO PARA TESTE)
TRT DA 3ª REGIÃO - 1ª VARA DO TRABALHO DE CONTAGEM
Processo 0010000-00.2026.5.03.0029 - Rito ordinário
Reclamante: MARIA SOUZA   Reclamada: LOJA MODELO LTDA
Data da sentença: 17/11/2026. Intimação das partes pelo DJEN em 18/11/2026.

SENTENÇA

I - RELATÓRIO. Dispensado, na forma do art. 852-I da CLT, por analogia.

II - FUNDAMENTAÇÃO
1. Estabilidade da gestante. A reclamante comprovou, pelo exame de 05/08/2026, que estava grávida
na data da dispensa (20/08/2026). A garantia do art. 10, II, b, do ADCT independe da ciência do
empregador (Súmula 244, I, do TST). A reintegração se mostra desaconselhável diante da animosidade
relatada pelas partes em audiência. Converto em indenização substitutiva: salários do período de
20/08/2026 até cinco meses após o parto, com 13º, férias + 1/3 e FGTS + 40% do período. Procedente.
2. Horas extras. A reclamante não juntou controle de jornada e a única testemunha, Juliana, disse
que não trabalhava no mesmo turno. Não se desincumbiu do ônus (art. 818, I, da CLT). Improcedente.
3. Danos morais. A dispensa de gestante, por si, não gera dano moral presumido. Improcedente.
4. Justiça gratuita deferida à reclamante (art. 790, § 3º, da CLT).
5. Honorários sucumbenciais: 10% sobre o valor líquido da condenação, pela reclamada, ao advogado
da reclamante (art. 791-A da CLT). Pela reclamante, 10% sobre os pedidos improcedentes, sob
condição suspensiva de exigibilidade (art. 791-A, § 4º, da CLT; ADI 5766).
6. Correção monetária e juros: na forma das ADC 58 e 59 do STF e da Lei 14.905/2024.

III - DISPOSITIVO
Julgo PROCEDENTES EM PARTE os pedidos para condenar LOJA MODELO LTDA a pagar a MARIA SOUZA
indenização substitutiva da estabilidade gestante (salários, 13º, férias + 1/3 e FGTS + 40% de
20/08/2026 até cinco meses após o parto). Improcedentes os pedidos de horas extras e danos morais.
Liquidação por cálculos. Custas pela reclamada, de R$ 600,00, calculadas sobre R$ 30.000,00.
Intimem-se.
Contagem, 17 de novembro de 2026. Juiz do Trabalho Substituto (fictício).
"""

SENTENCA_JOAO = """PODER JUDICIÁRIO - JUSTIÇA DO TRABALHO (DOCUMENTO FICTÍCIO PARA TESTE)
TRT DA 3ª REGIÃO - 2ª VARA DO TRABALHO DE CONTAGEM
Processo 0010001-00.2024.5.03.0030
Reclamante: JOÃO PEREIRA   Reclamada: TRANSPORTES EXEMPLO LTDA
Ajuizamento: 10/05/2024. Data da sentença: 20/03/2025.

FUNDAMENTAÇÃO
1. Prescrição. Pronuncio a prescrição quinquenal das parcelas anteriores a 10/05/2019 (art. 7º,
XXIX, da CF).
2. Dados do contrato. Admissão em 10/02/2018, dispensa em 01/03/2024, último salário de R$ 3.000,00,
divisor 220. Jornada fixada: das 07h às 19h, de segunda a sábado, com 1h de intervalo.
3. Horas extras. Defiro as excedentes da 8ª diária e da 44ª semanal, com adicional de 50%, divisor
220, e reflexos em DSR, 13º salários, férias + 1/3, aviso prévio e FGTS + 40%.
4. Intervalo intrajornada. Indefiro: a testemunha confirmou 1h de intervalo.
5. FGTS. Defiro os depósitos não recolhidos de 2022, com multa de 40%.
6. Contribuições previdenciárias e imposto de renda na forma da Súmula 368 do TST.
7. Correção monetária e juros: IPCA-E na fase pré-judicial e, a partir do ajuizamento, SELIC
(ADC 58 e 59 do STF).

DISPOSITIVO
Julgo PROCEDENTES EM PARTE os pedidos para condenar TRANSPORTES EXEMPLO LTDA a pagar a JOÃO
PEREIRA horas extras e reflexos e FGTS + 40%, nos termos da fundamentação. Liquidação por cálculos.
Custas pela reclamada, de 2% sobre R$ 50.000,00. Intimem-se.
Contagem, 20 de março de 2025. Juíza do Trabalho (fictícia).
"""

CNIS = """CADASTRO NACIONAL DE INFORMAÇÕES SOCIAIS - CNIS (DOCUMENTO FICTÍCIO PARA TESTE)
Extrato Previdenciário
Filiado: MARIA SOUZA   Nascimento: 10/05/1968   Sexo: Feminino   NIT: 000.00000.00-0
Relações Previdenciárias
Seq. 1  Empregador: COMERCIO ALFA LTDA (fictício)   Início: 01/03/1990   Fim: 28/02/2000   Tipo: Empregado
Seq. 2  Empregador: INDUSTRIA BETA S.A. (fictício)  Início: 01/01/1999   Fim: 31/12/2010   Tipo: Empregado
Seq. 3  Empregador: LOJA MODELO LTDA (fictícia)     Início: 01/01/2012   Fim: 20/08/2026   Tipo: Empregado
Indicadores: nenhum indicador de pendência.
"""

PONTO_JOAO = """data,entrada,saida,intervalo
01/06/2026,08:00,18:30,60
02/06/2026,08:00,19:00,60
03/06/2026,08:00,17:05,60
04/06/2026,08:00,19:30,60
05/06/2026,08:00,18:00,60
06/06/2026,08:00,12:00,0
07/06/2026,08:00,14:00,0
08/06/2026,08:00,18:30,60
09/06/2026,08:00,19:00,60
10/06/2026,08:00,17:00,60
11/06/2026,08:00,19:30,60
12/06/2026,08:00,18:00,60
13/06/2026,08:00,12:00,0
"""

CONTESTACAO_MINUTA = """EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DA 1ª VARA DO TRABALHO DE CONTAGEM/MG

Processo nº 0010002-00.2026.5.03.0029 (FICTÍCIO)

PADARIA PÃO BOM LTDA, já qualificada, vem, por sua advogada, apresentar CONTESTAÇÃO à reclamação
movida por CARLA DIAS, pelos fatos e fundamentos a seguir.

1. DAS HORAS EXTRAS

A reclamante alega que trabalhava das 6h às 16h. Não é verdade — os cartões de ponto (Doc. 3)
mostram jornada das 6h às 14h20, com intervalo de 1 hora. É importante ressaltar que, nesse sentido,
cabe destacar que a jurisprudência é pacífica no sentido de que o cartão de ponto prevalece
(TST, RR 123). Ademais, a reclamante nunca reclamou. Portanto, improcede o pedido.

2. DO ADICIONAL NOTURNO

A reclamante não trabalhava à noite — basta ver os cartões de ponto (Doc. 3), que mostram jornada
das 6h às 14h20, com intervalo de 1 hora, e a jurisprudência é pacífica no sentido de que o cartão de
ponto prevalece. Ademais, a reclamante nunca reclamou.

3. DA MULTA DO ART. 477

As verbas foram pagas no prazo, conforme o recibo (Doc. 4) e o TRCT.

4. DOS PEDIDOS

Diante do exposto, requer: a) a condenação da reclamante em honorários de sucumbência; b) a
total improcedência dos pedidos; c) a produção de todas as provas em direito admitidas.

Termos em que pede deferimento.
Contagem, 19 de novembro de 2026.
Ana Fictícia Lima, OAB/MG 999.999
"""

CONTESTACAO_PROTOCOLO = """EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DA 1ª VARA DO TRABALHO DE CONTAGEM/MG
Processo nº 0010002-00.2026.5.03.0029 (FICTÍCIO)
PADARIA PÃO BOM LTDA, por sua advogada (procuração, Doc. 2), apresenta CONTESTAÇÃO.
Representação: contrato social (Doc. 1).
1. Horas extras. Os cartões de ponto (Doc. 3) mostram jornada das 6h às 14h20, com 1h de intervalo.
2. Multa do art. 477. As verbas foram pagas no prazo, conforme o recibo de pagamento (Doc. 4).
3. Pedidos. Requer a improcedência dos pedidos.
Contagem, 19 de novembro de 2026. Ana Fictícia Lima, OAB/MG 999.999
"""

PADARIA = briefing("Padaria Pão Bom Ltda (fictícia)", "clientes/padaria-pao-bom/", """## 1. Identificação
- **Qualificação:** Padaria Pão Bom Ltda, CNPJ 00.000.000/0001-00 (fictício), Contagem/MG, representada pelo sócio Paulo Bom
- **Parte contrária:** Carla Dias (fictícia), ex-empregada, tem advogado

## 2. Classificação da demanda
- **Área:** trabalhista · **Polo:** réu (reclamada) · **Natureza:** defesa
- **Já existe processo?** 0010002-00.2026.5.03.0029, 1ª VT de Contagem, PJe

## 8. Documentos recebidos
| Arquivo | O que é | Recebido em | Analisado | Serve pra quê |
|---|---|---|---|---|
| documentos/contrato-social.pdf | contrato social | 12/11/2026 | sim | representação |
| documentos/procuracao-assinada.pdf | procuração | 12/11/2026 | sim | representação |
| documentos/cartoes-de-ponto-2025.pdf | cartões de ponto | 12/11/2026 | sim | jornada |
""")

CONTRATO_LOCACAO = """CONTRATO DE LOCAÇÃO COMERCIAL (MINUTA ENVIADA PELO LOCADOR - DOCUMENTO FICTÍCIO)

LOCADOR: IMOBILIÁRIA EXEMPLO LTDA, CNPJ 00.000.000/0001-00.
LOCATÁRIO: CARLOS MENDES, CPF 111.444.777-35 (fictício).

Cláusula 1ª. O imóvel da Rua do Comércio, 50, loja 1, Contagem/MG, destina-se a uso comercial.
Cláusula 2ª. Prazo de 60 meses, a contar de 01/12/2026.
Cláusula 3ª. Aluguel mensal de R$ 4.000,00, reajustado anualmente pelo índice que o LOCADOR escolher
no mês do reajuste.
Cláusula 4ª. O LOCATÁRIO renuncia ao direito à renovação da locação e a qualquer indenização ou
retenção por benfeitorias, inclusive as necessárias.
Cláusula 5ª. Em caso de devolução antecipada do imóvel, o LOCATÁRIO pagará multa de 12 (doze)
aluguéis, integral, qualquer que seja o tempo restante do contrato.
Cláusula 6ª. O LOCATÁRIO arcará com o IPTU, o condomínio, inclusive as despesas extraordinárias de
condomínio, e o seguro do imóvel.
Cláusula 7ª. Garantia: fiança e caução de 3 aluguéis, cumulativamente.
Cláusula 8ª. O LOCADOR poderá vistoriar o imóvel a qualquer tempo, sem aviso prévio.
Cláusula 9ª. Fica eleito o foro da comarca de São Paulo/SP.
"""

ROBERTO = briefing("Roberto Alves (fictício)", "clientes/roberto-alves/", """## 1. Identificação
- **Qualificação:** Roberto Alves, brasileiro, casado, aposentado, CPF 111.444.777-35 (fictício), Rua A, 1, Contagem/MG
- **Parte contrária:** Fernando Lopes (fictício), inquilino, CPF 000.000.001-91 (fictício), residente no imóvel locado:
  Rua B, 200, apto 101, Contagem/MG

## 2. Classificação da demanda
- **Área:** cível · **Sub-área:** locação residencial · **Polo:** cliente é o locador

## 3. Fatos — linha do tempo
| Data | Fato | Fonte | Provado? |
|---|---|---|---|
| 01/03/2025 | Contrato de locação residencial, 30 meses, aluguel R$ 2.500,00, vencimento dia 10 | documentos/contrato-locacao.md | doc |
| 10/08/2026 | Aluguel de agosto não pago | extrato bancário | doc |
| 10/09/2026 | Aluguel de setembro não pago | extrato | doc |
| 10/10/2026 | Aluguel de outubro não pago | extrato | doc |

## 4. O que o cliente pediu × o que quer
- **Pedido literal:** que o inquilino pague os três aluguéis atrasados, R$ 7.500,00 sem encargos
- **Interesse real:** receber; se não pagar em 15 dias, quer o imóvel de volta (despejo)
""")

CONTRATO_ROBERTO = """CONTRATO DE LOCAÇÃO RESIDENCIAL (FICTÍCIO)
Locador: Roberto Alves. Locatário: Fernando Lopes. Imóvel: Rua B, 200, apto 101, Contagem/MG.
Prazo: 30 meses desde 01/03/2025. Aluguel: R$ 2.500,00, vencimento todo dia 10.
Multa moratória: 10% sobre o aluguel em atraso. Juros: 1% ao mês. Correção: IGP-M.
Notificações: por escrito, no endereço do imóvel, com prova de recebimento.
Garantia: fiador, Sr. Marcos Lopes (fictício), Rua C, 3, Contagem/MG.
"""

CLINICA = briefing("Clínica Sorriso Fictício Ltda", "clientes/clinica-sorriso/", """## 1. Identificação
- **Qualificação:** Clínica Sorriso Fictício Ltda, clínica odontológica, CNPJ 00.000.000/0001-00 (fictício), Contagem/MG
- Sócios: dois dentistas; 6 funcionários (2 recepcionistas, 3 auxiliares, 1 administrativo)

## 2. Classificação da demanda
- **Área:** consultivo · **Matéria:** adequação à LGPD

## 3. Fatos (o que o cliente contou)
- Prontuário em sistema na nuvem (fornecedor OdontoNuvem, fictício); fichas antigas em papel num armário sem chave.
- Agenda e confirmação de consulta pelo WhatsApp do celular da recepção (aparelho da clínica, sem senha).
- Instagram com fotos de "antes e depois" de pacientes; autorização verbal.
- Formulário de agendamento no site, sem política de privacidade.
- Nunca nomeou encarregado. Nunca teve incidente conhecido.
- Câmera de segurança na recepção, gravação 30 dias.
""")

POST_GESTANTE = """# Post: demissão de gestante (aprovado pela advogada, 10/11/2026)

Slide 1: Foi demitida grávida? Entenda seus direitos.
Slide 2: A lei garante estabilidade desde a confirmação da gravidez até 5 meses depois do parto.
Slide 3: Vale mesmo se a empresa não sabia da gravidez quando demitiu.
Slide 4: Vale também no contrato de experiência e no aviso prévio.
Slide 5: Se a volta ao trabalho não for possível, a empresa paga os salários do período.
Slide 6: Cada caso tem detalhes. Converse com um advogado de sua confiança.

Legenda: A gravidez dá estabilidade no emprego. Saiba o que a lei diz.
"""

EMAIL_CHATGPT = """Prezado Sr. Paulo,

Espero que este e-mail o encontre bem! É com grande satisfação que venho, por meio deste, informá-lo
acerca dos desdobramentos do seu caso — um tema de suma importância. Vale ressaltar que a audiência
foi redesignada para o dia 03/12/2026, às 14h. Além disso, é fundamental destacar que será
imprescindível a sua presença, bem como a apresentação dos cartões de ponto originais.

O resultado? Uma defesa robusta e sólida! Fico à inteira disposição para quaisquer esclarecimentos
que se fizerem necessários. Não hesite em entrar em contato.

Atenciosamente,
Ana Fictícia Lima
"""

# --------------------------------------------------------------------------- os casos

FERR_TEXTO = ["Read", "Write", "Edit", "Glob", "Grep", "Skill", "Bash(ls:*)", "Bash(mkdir:*)", "Bash(date:*)"]
FERR_SCRIPT = FERR_TEXTO + ["Bash(uv run:*)", "Bash(python3:*)", "Bash(wc:*)"]
FERR_ARQ = FERR_SCRIPT + ["Bash(cp:*)", "Bash(file:*)"]
MARCA = "Azul-marinho e dourado. Sem logo. Clássico."

CASOS = {
    # ---- cálculos
    "calculo-rescisao": dict(
        arquivos={"clientes/joao-pereira/briefing.md": JOAO},
        pedido="Foi mandado embora sem justa causa: quanto ele tem pra receber?",
        resposta="É o João Pereira, os dados estão no briefing dele. O que faltar, siga com o padrão da skill e me avise.",
        esperado=["clientes/joao-pereira/calculos/rescisao-*.md"], ferramentas=FERR_SCRIPT),
    "calculo-horas-extras": dict(
        arquivos={"clientes/joao-pereira/briefing.md": JOAO,
                  "clientes/joao-pereira/documentos/cartao-de-ponto-2026-06.csv": PONTO_JOAO},
        pedido="Tenho o cartão de ponto: quanto dá de hora extra?",
        resposta="É o João Pereira (clientes/joao-pereira). Trabalhava em Contagem/MG; no período não houve feriado "
                 "local. Jornada contratual 8h/dia e 44h/semana, divisor 220, sem multa do FGTS. Pode calcular.",
        esperado=["clientes/joao-pereira/calculos/horas-extras-*.md"], ferramentas=FERR_SCRIPT),
    "atualizacao-monetaria": dict(
        arquivos={"clientes/joao-pereira/briefing.md": JOAO_PROC,
                  "clientes/joao-pereira/decisoes/sentenca-2025-03-20.md": SENTENCA_JOAO
                  + "\nLIQUIDAÇÃO HOMOLOGADA (fictícia): crédito de R$ 20.000,00 apurado até 31/03/2024.\n"},
        pedido="Atualiza essa condenação trabalhista até hoje.",
        resposta="É a do João Pereira (clientes/joao-pereira/decisoes/sentenca-2025-03-20.md). Valor R$ 20.000,00 "
                 "apurado até 31/03/2024, ajuizamento 10/05/2024, regra trabalhista da ADC 58/59 como manda a sentença. Pode rodar.",
        esperado=["clientes/joao-pereira/calculos/atualizacao-*.md"], ferramentas=FERR_SCRIPT),
    "pjecalc-preparo": dict(
        arquivos={"clientes/joao-pereira/briefing.md": JOAO_PROC,
                  "clientes/joao-pereira/decisoes/sentenca-2025-03-20.pdf": ("pdf", SENTENCA_JOAO)},
        pedido="Vou liquidar a sentença: o que eu lanço no PJe-Calc?",
        resposta="É a sentença do João Pereira, em clientes/joao-pereira/decisoes/. Conferi os parâmetros, estão certos. Pode gerar o roteiro.",
        esperado=["clientes/joao-pereira/calculos/pjecalc-parametros.json", "clientes/joao-pereira/calculos/pjecalc-roteiro-*.md"],
        ferramentas=FERR_SCRIPT),
    "calculo-previdenciario-basico": dict(
        arquivos={"clientes/maria-souza/briefing.md": MARIA,
                  "clientes/maria-souza/documentos/cnis.pdf": ("pdf", CNIS)},
        pedido="Já dá pra ela se aposentar? Conta o tempo do CNIS.",
        resposta="É a Maria Souza, o CNIS está em clientes/maria-souza/documentos/cnis.pdf. Conferi a tabela de "
                 "vínculos, está certa, todos entram. Nascimento 10/05/1968, sexo feminino, DER hoje. Pode calcular.",
        esperado=["clientes/maria-souza/calculos/vinculos.csv", "clientes/maria-souza/calculos/tempo-contribuicao-*.md"],
        ferramentas=FERR_SCRIPT),
    # ---- marketing (sem _contexto/marca.md: a skill tem de perguntar e gravar)
    "carrossel-instagram": dict(
        arquivos={"marketing/posts/2026-11-10-gestante.md": POST_GESTANTE},
        pedido="Transforma esse post em carrossel pronto pra postar: marketing/posts/2026-11-10-gestante.md",
        resposta=MARCA + " Pode gerar.",
        esperado=["_contexto/marca.md", "marketing/carrosseis/*/01.png", "marketing/carrosseis/*/texto.md"],
        ferramentas=FERR_SCRIPT),
    "capa-instagram": dict(
        arquivos={},
        pedido="Faz a capa do reels sobre demissão de gestante.",
        resposta=MARCA + " Fique com a primeira opção de título e pode gerar.",
        esperado=["_contexto/marca.md", "marketing/capas/*/*.png"], ferramentas=FERR_SCRIPT),
    "copy-escritorio": dict(
        arquivos={},
        pedido="Escreve minha bio do Instagram.",
        resposta="É a bio do @limaadvocacia (fictício). Atendo trabalhador demitido, gestante e quem quer se aposentar; "
                 "a dúvida mais comum é 'fui demitido, o que eu recebo?'. Link: WhatsApp. Pode escrever.",
        esperado=["marketing/textos/*.md"], ferramentas=FERR_SCRIPT),
    "site-do-escritorio": dict(
        arquivos={},
        pedido="Faz o site do escritório pra eu pôr na bio.",
        resposta=MARCA + " Endereço: Rua dos Testes, 100, sala 2, Centro, Contagem/MG. WhatsApp (31) 90000-0000 (fictício), "
                 "e-mail contato@lima-ficticia.adv.br. Sem foto. Pode fazer.",
        esperado=["marketing/site/index.html"], ferramentas=FERR_SCRIPT),
    "seo-local": dict(
        arquivos={},
        pedido="Meu escritório não aparece no Google Maps.",
        resposta="Não tenho perfil no Google ainda. Recebo cliente no endereço do perfil, em Contagem; atendo Contagem, "
                 "Betim e Belo Horizonte. Não tenho site. Pode montar o plano.",
        esperado=["marketing/seo-local/*-plano.md"], ferramentas=FERR_TEXTO),
    # ---- o resto
    "ficha-de-atendimento": dict(
        arquivos={"clientes/maria-souza/reuniao/2026-11-18-primeira-reuniao.transcricao.md": MARIA_REUNIAO},
        pedido="Acabei de atender a Maria Souza: faz a ficha do cliente.",
        resposta="A transcrição está em clientes/maria-souza/reuniao/. Pode fazer a ficha com o que tem.",
        esperado=["clientes/maria-souza/briefing.md"], ferramentas=FERR_TEXTO),
    "kit-contratacao": dict(
        arquivos={"clientes/maria-souza/briefing.md": MARIA},
        pedido="O cliente fechou: monta a papelada pra assinar.",
        resposta="É a Maria Souza. Honorários: só êxito, 30% do proveito econômico, pagos quando ela receber. Vai pedir "
                 "justiça gratuita. Poderes especiais: receber e dar quitação, transigir e assinar declaração de "
                 "hipossuficiência. Substabelecimento com reserva. Pode gerar.",
        esperado=["clientes/maria-souza/contratacao/1-procuracao-*.docx", "clientes/maria-souza/contratacao/2-contrato-de-honorarios-*.docx",
                  "clientes/maria-souza/contratacao/3-declaracao-de-hipossuficiencia-*.docx"], ferramentas=FERR_SCRIPT),
    "avisar-cliente": dict(
        arquivos={"clientes/maria-souza/briefing.md": MARIA,
                  "clientes/maria-souza/decisoes/sentenca-2026-11-17.md": SENTENCA_MARIA},
        pedido="Saiu a sentença da Maria Souza: prepara a mensagem pra ela.",
        resposta="A sentença está em clientes/maria-souza/decisoes/sentenca-2026-11-17.md. Mensagem por WhatsApp, "
                 "trate por você. Pode escrever.",
        esperado=["clientes/maria-souza/mensagens/*.md"], ferramentas=FERR_TEXTO),
    "pacote-protocolo": dict(
        arquivos={"clientes/padaria-pao-bom/briefing.md": PADARIA,
                  "clientes/padaria-pao-bom/pecas/contestacao-2026-11-19.pdf": ("pdf", CONTESTACAO_PROTOCOLO),
                  "clientes/padaria-pao-bom/documentos/contrato-social.pdf": ("pdf", "CONTRATO SOCIAL DA PADARIA PÃO BOM LTDA (FICTÍCIO)\nSócio administrador: Paulo Bom."),
                  "clientes/padaria-pao-bom/documentos/procuracao-assinada.pdf": ("pdf", "PROCURAÇÃO (FICTÍCIA)\nOutorgante: Padaria Pão Bom Ltda. Outorgada: Ana Fictícia Lima, OAB/MG 999.999."),
                  "clientes/padaria-pao-bom/documentos/cartoes-de-ponto-2025.pdf": ("pdf", "CARTÕES DE PONTO 2025 (FICTÍCIOS)\nCarla Dias: 06:00 às 14:20, intervalo 1h, seg a sáb.")},
        pedido="Vou peticionar a contestação: monta a pasta do protocolo.",
        resposta="É a da Padaria Pão Bom, clientes/padaria-pao-bom/pecas/contestacao-2026-11-19.pdf. O recibo (Doc. 4) "
                 "o cliente ainda não mandou: deixe como pendência. Nada é sigiloso. Pode montar.",
        esperado=["clientes/padaria-pao-bom/**/*LEIA-ME*", "desfazer/*protocolo*"], ferramentas=FERR_ARQ),
    "revisar-peca": dict(
        arquivos={"clientes/padaria-pao-bom/briefing.md": PADARIA,
                  "clientes/padaria-pao-bom/pecas/contestacao-minuta-estagiario.md": CONTESTACAO_MINUTA},
        pedido="O estagiário fez essa contestação, confere antes de eu protocolar: clientes/padaria-pao-bom/pecas/contestacao-minuta-estagiario.md",
        resposta="Contestação trabalhista, quem decide é o juiz da 1ª VT de Contagem, revisão completa. Não tenho a inicial aqui.",
        esperado=["clientes/padaria-pao-bom/**/*-revisao-*.md"], ferramentas=FERR_SCRIPT),
    "analise-de-decisao": dict(
        arquivos={"clientes/maria-souza/briefing.md": MARIA,
                  "clientes/maria-souza/decisoes/sentenca-2026-11-17.pdf": ("pdf", SENTENCA_MARIA)},
        pedido="Saiu a sentença, analisa: ganhamos ou perdemos?",
        resposta="É a da Maria Souza (clientes/maria-souza/decisoes/sentenca-2026-11-17.pdf). A cliente é a reclamante. "
                 "Intimação pelo DJEN em 18/11/2026. Pode analisar.",
        esperado=["clientes/maria-souza/**/*-analise-*.md"], ferramentas=FERR_SCRIPT),
    "revisar-contrato": dict(
        arquivos={"clientes/carlos-mendes/contrato-locacao-comercial.md": CONTRATO_LOCACAO},
        pedido="O cliente vai assinar esse contrato: tem pegadinha? clientes/carlos-mendes/contrato-locacao-comercial.md",
        resposta="O cliente é o locatário (Carlos Mendes). Ele vai abrir uma padaria e quer ficar os 5 anos; o que mais "
                 "preocupa é a multa e o reajuste. Revisão completa.",
        esperado=["clientes/carlos-mendes/*-revisao-*.md"], ferramentas=FERR_SCRIPT),
    "notificacao-extrajudicial": dict(
        arquivos={"clientes/roberto-alves/briefing.md": ROBERTO,
                  "clientes/roberto-alves/documentos/contrato-locacao.md": CONTRATO_ROBERTO},
        pedido="Notifica o inquilino pra pagar os aluguéis atrasados.",
        resposta="É o caso do Roberto Alves. Prazo de 15 dias para pagar; se não pagar, ação de despejo por falta de "
                 "pagamento e cobrança. Envio por cartório de títulos e documentos. Notificar também o fiador. Pode redigir.",
        esperado=["clientes/roberto-alves/**/notificacao-*.md"], ferramentas=FERR_SCRIPT),
    "lgpd-escritorio": dict(
        arquivos={},
        pedido="Quero adequar meu escritório à LGPD.",
        resposta="1) Só eu, advocacia individual, sem sociedade. 2) Advocacia individual. 3) Notebook, Google Drive, Gmail, "
                 "WhatsApp no celular, PJe. 4) Sim: previdenciário (laudos médicos) e trabalhista com atestado. 5) Instagram, "
                 "sem site, sem lista de e-mail. 6) Sim, uso o Claude com documento de cliente. 7) Nunca tive vazamento. "
                 "Pode montar o kit.",
        esperado=["lgpd/*.md"], ferramentas=FERR_TEXTO),
    "lgpd-consultivo": dict(
        arquivos={"clientes/clinica-sorriso/briefing.md": CLINICA},
        pedido="Meu cliente quer se adequar à LGPD: faz o diagnóstico da empresa.",
        resposta="É a Clínica Sorriso (clientes/clinica-sorriso). O que não está no briefing, marque como não informado e siga.",
        esperado=["clientes/clinica-sorriso/**/lgpd-diagnostico-*.md"], ferramentas=FERR_SCRIPT),
    "escrita-clara": dict(
        arquivos={},
        pedido="Esse e-mail tá com cara de ChatGPT, deixa mais natural.\n\n" + EMAIL_CHATGPT,
        resposta="É para o cliente Paulo, por e-mail. Pode reescrever.",
        esperado=[], ferramentas=FERR_SCRIPT),
    "organizar-pasta": dict(
        arquivos={"clientes/maria-souza/briefing.md": MARIA,
                  "clientes/maria-souza/documentos/scan001.pdf": ("pdf", "CARTEIRA DE IDENTIDADE (FICTÍCIA)\nNome: MARIA SOUZA\nRG MG-00.000.000  CPF 111.444.777-35"),
                  "clientes/maria-souza/documentos/documento (3).pdf": ("pdf", "TERMO DE RESCISÃO DO CONTRATO DE TRABALHO - TRCT (FICTÍCIO)\nEmpregador: Loja Modelo Ltda. Empregada: Maria Souza.\nAfastamento: 20/08/2026. Pagamento: 29/08/2026."),
                  "clientes/maria-souza/documentos/final2.pdf": ("pdf", "ULTRASSONOGRAFIA OBSTÉTRICA (FICTÍCIA)\nPaciente: Maria Souza. Data do exame: 05/08/2026.\nGestação tópica, 8 semanas."),
                  "clientes/maria-souza/documentos/final2 copia.pdf": ("pdf", "ULTRASSONOGRAFIA OBSTÉTRICA (FICTÍCIA)\nPaciente: Maria Souza. Data do exame: 05/08/2026.\nGestação tópica, 8 semanas."),
                  "clientes/maria-souza/documentos/comprovante.pdf": ("pdf", "CONTA DE LUZ (FICTÍCIA) - OUTUBRO/2026\nTitular: Maria Souza. Rua das Flores, 10, Contagem/MG."),
                  "clientes/maria-souza/documentos/IMG_2231.png": ("bin", PNG_VAZIO)},
        pedido="Arruma os documentos que a Maria Souza mandou, tá uma bagunça.",
        resposta="Pode executar o plano.",
        esperado=["desfazer/*-plano.tsv", "desfazer/*.md"], ferramentas=FERR_ARQ),
}

ORDEM = ["calculo-rescisao", "calculo-horas-extras", "atualizacao-monetaria", "pjecalc-preparo",
         "calculo-previdenciario-basico", "carrossel-instagram", "capa-instagram", "copy-escritorio",
         "site-do-escritorio", "seo-local"]
ORDEM += [k for k in CASOS if k not in ORDEM]

# --------------------------------------------------------------------------- rodar


def montar(pasta, caso):
    if pasta.exists():
        shutil.rmtree(pasta)
    pasta.mkdir(parents=True)
    subprocess.run(["git", "clone", "-q", str(KIT), str(pasta / ".claude")], check=True)
    for rel, conteudo in {**BASE, **caso["arquivos"]}.items():
        p = pasta / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(conteudo, tuple):
            pdf(p, conteudo[1]) if conteudo[0] == "pdf" else p.write_bytes(conteudo[1])
        else:
            p.write_text(conteudo, encoding="utf-8")


def turno(pasta, texto, ferramentas, log, sessao=None):
    cmd = ["claude", "-p", texto, "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project,local", "--strict-mcp-config",
           "--allowedTools", *ferramentas]
    if sessao:
        cmd += ["--resume", sessao]
    with open(log, "w") as f:
        try:
            subprocess.run(cmd, cwd=pasta, stdout=f, stderr=subprocess.STDOUT, timeout=1500, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            f.write('\n{"type":"result","subtype":"timeout","result":"TIMEOUT"}\n')
    sess, final, negadas, custo = None, "", [], 0
    for linha in open(log):
        try:
            e = json.loads(linha)
        except ValueError:
            continue
        sess = e.get("session_id") or sess
        if e.get("type") == "result":
            final, custo = e.get("result") or e.get("subtype", ""), e.get("total_cost_usd") or 0
            negadas += [d.get("tool_name", "") + " " + json.dumps(d.get("tool_input", {}), ensure_ascii=False)[:160]
                        for d in e.get("permission_denials") or []]
    return sess, final, negadas, custo


def faltando(pasta, esperado):
    return [g for g in esperado if not glob.glob(str(pasta / g), recursive=True)]


def rodar(nome, raiz):
    caso = CASOS[nome]
    pasta = raiz / nome
    montar(pasta, caso)
    ev = raiz / "_evidencia" / nome
    ev.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sess, r1, neg, c1 = turno(pasta, caso["pedido"], caso["ferramentas"], ev / "turno1.jsonl")
    (ev / "turno1.txt").write_text(r1)
    r2, c2 = "", 0
    falta = faltando(pasta, caso["esperado"])
    if (falta or not caso["esperado"]) and sess and caso.get("resposta"):
        _, r2, neg2, c2 = turno(pasta, caso["resposta"], caso["ferramentas"], ev / "turno2.jsonl", sessao=sess)
        (ev / "turno2.txt").write_text(r2)
        neg += neg2
        falta = faltando(pasta, caso["esperado"])
    res = dict(skill=nome, saiu=not falta, faltou=falta, negadas=neg, segundos=int(time.time() - t0),
               custo_usd=round(c1 + c2, 2), pergunta_turno1=r1[-600:], turnos=2 if r2 else 1)
    (ev / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print("%-30s %s  %ds  falta=%s  negadas=%d" % (nome, "OK " if not falta else "FALTOU", res["segundos"], falta, len(neg)), flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills", nargs="*")
    ap.add_argument("--saida", default=os.environ.get("FUMACA_SAIDA", "/tmp/fumaca-kit"))
    ap.add_argument("-j", type=int, default=4)
    a = ap.parse_args()
    raiz = Path(a.saida)
    nomes = a.skills or ORDEM
    for n in nomes:
        if n not in CASOS:
            sys.exit("skill sem caso: %s" % n)
    with ThreadPoolExecutor(min(a.j, 4)) as ex:
        res = list(ex.map(lambda n: rodar(n, raiz), nomes))
    print("\n| skill | artefato saiu | turnos | negadas | s |\n|---|---|---|---|---|")
    for r in res:
        print("| %s | %s | %d | %d | %d |" % (r["skill"], "sim" if r["saiu"] else "NÃO " + str(r["faltou"]),
                                             r["turnos"], len(r["negadas"]), r["segundos"]))
    sys.exit(0 if all(r["saiu"] for r in res) else 1)


if __name__ == "__main__":
    main()
