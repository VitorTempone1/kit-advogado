# /// script
# requires-python = ">=3.9"
# dependencies = ["pypdf>=5.0"]
# ///
"""Censo de TODAS as pecas de uma pasta de escritorio. Roda na maquina do advogado.

Le o comeco e o fim de cada .docx e .pdf com texto, reconhece peca pelo CONTEUDO (a primeira
linha enderecada ao juiz), nunca pelo nome do arquivo, e devolve SO CONTAGENS: tipos de peca,
justica, comarcas, assinaturas, titulos de secao, formulas e fecho. Nenhum nome de parte,
CPF ou numero de processo sai daqui. No fim, sugere ate 5 pecas para ler o estilo (--amostra N, ate 10).

  uv run censo_pecas.py "<pasta>" --oab 123456   # so as pecas assinadas por esta OAB entram
  uv run censo_pecas.py --demo        # autoteste, sem pasta

Nada aqui faz rede. Os arquivos nao saem da maquina.
"""

import os
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from texto_docx import texto as texto_docx  # noqa: E402

import logging
logging.getLogger("pypdf").setLevel(logging.ERROR)  # PDF quebrado vira "ilegivel", sem barulho na tela

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# PDF e lento de abrir e quase sempre e documento de cliente ou peca baixada do PJe:
# so entra quando o NOME parece de peca. .docx entra sempre.
PDF_DE_PECA = re.compile(r"inicial|peti[cç][aã]o|contesta|r[eé]plica|impugna|recurso|apela|agravo|embargo|"
                         r"contrarraz|manifesta|memoria|alega[cç]|defesa|mandado de seg|habeas|reclama[cç]", re.I)


def candidato(nome: str) -> bool:
    if nome.startswith(("~$", "._")):
        return False
    ext = Path(nome).suffix.lower()
    return ext == ".docx" or (ext == ".pdf" and bool(PDF_DE_PECA.search(nome)))


PULA_PASTA = re.compile(r"pessoal|particular|\.claude|_triagem|desfazer", re.I)
ENDERECO = re.compile(r"\bAO\s+JU\S{1,2}ZO\b|\bEXM[OA]\b|EXCELENT[IÍ]SSIM|SENHOR(?:A|ES)?\s+(?:DOUTOR|JUIZ|DESEMBARGADOR|MINISTRO)|"
                      r"MERIT[IÍ]SSIM|JU[IÍ]Z(?:A|ES)?\s+(?:DE DIREITO|DO TRABALHO|FEDERAL)", re.I)
TIPOS = [  # o que aparece PRIMEIRO no comeco da peca decide
    ("Reclamação trabalhista", r"RECLAMA[ÇC][ÃA]O TRABALHISTA"),
    ("Contestação", r"\bCONTESTA[ÇC][ÃA]O\b"),
    ("Réplica / impugnação", r"\bR[ÉE]PLICA\b|IMPUGNA[ÇC][ÃA]O [ÀA] CONTESTA"),
    ("Recurso inominado", r"RECURSO INOMINADO"),
    ("Recurso ordinário", r"RECURSO ORDIN[ÁA]RIO"),
    ("Apelação", r"\bAPELA[ÇC][ÃA]O\b"),
    ("Agravo", r"\bAGRAVO\b"),
    ("Embargos de declaração", r"EMBARGOS DE DECLARA"),
    ("Contrarrazões", r"CONTRARRAZ|CONTRA-RAZ"),
    ("Mandado de segurança", r"MANDADO DE SEGURAN"),
    ("Habeas corpus", r"HABEAS CORPUS"),
    ("Cumprimento de sentença", r"CUMPRIMENTO DE SENTEN"),
    ("Petição inicial (ação)", r"\b(?:PROPOR|AJUIZAR|PROMOVER)\b.{0,40}\bA[ÇC][ÃA]O\b|\bA[ÇC][ÃA]O DE\b"),
    ("Manifestação / petição simples", r"MANIFESTA[ÇC][ÃA]O|REQUERER|EXPOR E REQUERER"),
]
JUSTICA = [
    ("Justiça do Trabalho", r"JU[IÍ]Z(?:A)? DO TRABALHO|VARA DO TRABALHO|TRIBUNAL REGIONAL DO TRABALHO"),
    ("Justiça Federal", r"JU[IÍ]Z(?:A)? FEDERAL|VARA FEDERAL|TRIBUNAL REGIONAL FEDERAL"),
    ("Turma Recursal", r"TURMA RECURSAL"),
    ("Juizado Especial da Fazenda Pública", r"JUIZADO ESPECIAL DA FAZENDA|JUIZADO DA FAZENDA|FAZENDA P[ÚU]BLICA.{0,60}JUIZADO"),
    ("Juizado Especial", r"JUIZADO ESPECIAL|UNIDADE JURISDICIONAL"),
    ("Tribunal (2º grau)", r"DESEMBARGADOR|TRIBUNAL DE JUSTI[ÇC]A"),
    ("Justiça Estadual (1º grau)", r"JU[IÍ]Z(?:A)? DE DIREITO|VARA C[ÍI]VEL|VARA DE FAM[ÍI]LIA|COMARCA DE"),
]
FORMULAS = ["data venia", "devida vênia", "egrégio", "colendo", "meritíssimo", "ex positis",
            "ante o exposto", "diante do exposto", "termos em que", "nestes termos",
            "pede deferimento", "respeitosamente", "requer a vossa excelência"]
COMARCA = re.compile(r"(?:COMARCA|VARA DO TRABALHO|SUBSE[ÇC][ÃA]O JUDICI[ÁA]RIA) DE ([A-ZÀ-Ú][A-ZÀ-Ú' ]{2,30}?)"
                     r"\s*(?:[/\-–,.(]|$|\bMG\b|\bSP\b|\bRJ\b)", re.I | re.M)
OAB = re.compile(r"OAB\s*[/\-]?\s*([A-Z]{2})\s*(?:n?[º°o.]*\s*)?(\d{1,3}(?:\.?\d{3})+|\d{3,6})", re.I)
SECAO = re.compile(r"^\s*(?:[IVXL]+|\d{1,2})\s*[.\-–)]\s*([A-ZÀ-Ú][A-ZÀ-Ú ,]{3,60})\s*$", re.M)


def ler(arq: Path):
    """Comeco e fim do texto, ou None se nao der pra ler."""
    try:
        if arq.suffix.lower() == ".docx":
            t = texto_docx(arq)
        else:
            from pypdf import PdfReader
            r = PdfReader(str(arq))
            pags = list(range(min(2, len(r.pages)))) + ([len(r.pages) - 1] if len(r.pages) > 2 else [])
            t = "\n".join((r.pages[i].extract_text() or "") for i in pags)
    except Exception:
        return None
    t = t.strip()
    return (t[:3000], t[-1200:]) if len(t) >= 200 else None


def prioridade(lista, txt):
    """O primeiro da LISTA que aparece no texto (a lista vai do orgao mais especifico ao mais geral)."""
    return next((nome for nome, rx in lista if re.search(rx, txt, re.I)), None)


def primeiro(lista, txt):
    achados = [(m.start(), nome) for nome, rx in lista for m in [re.search(rx, txt, re.I)] if m]
    return min(achados)[1] if achados else None


def censo(pasta: Path, oab: str = ""):
    arqs, ilegiveis, pecas, alheias = 0, 0, [], 0
    c = {k: Counter() for k in ("tipo", "justica", "comarca", "oab", "secao", "formula", "fecho")}
    for raiz, dirs, nomes in os.walk(pasta):
        dirs[:] = [d for d in dirs if not PULA_PASTA.search(d)]
        for n in nomes:
            arq = Path(raiz) / n
            if not candidato(n):
                continue
            arqs += 1
            lido = ler(arq)
            if not lido:
                ilegiveis += 1
                continue
            ini, fim = lido
            if not ENDERECO.search(ini[:600]):
                continue  # nao e peca: procuracao, contrato, documento
            assinaturas = {(u.upper(), re.sub(r"\D", "", n)) for u, n in OAB.findall(fim)}
            if oab and not any(num == oab for _, num in assinaturas):
                alheias += 1  # peca de outro advogado (parte contraria baixada do PJe, colega)
                continue
            tipo = primeiro(TIPOS, ini) or "Outra peça"
            c["tipo"][tipo] += 1
            c["justica"][prioridade(JUSTICA, ini[:800]) or "não identificada"] += 1
            for m in {x.strip().title() for x in COMARCA.findall(ini[:800])}:
                c["comarca"][m] += 1
            for uf, num in assinaturas:
                c["oab"][f"OAB/{uf} {num}"] += 1
            for s in {re.sub(r"\s+", " ", x).strip() for x in SECAO.findall(ini + "\n" + fim)}:
                c["secao"][s] += 1
            baixo = (ini + " " + fim).lower()
            for f in FORMULAS:
                if f in baixo:
                    c["formula"][f] += 1
            ult = [l for l in fim.splitlines() if len(l.strip()) > 8][-6:]
            for l in ult:
                if re.search(r"deferimento|termos|respeitosamente|aguarda", l, re.I):
                    c["fecho"][l.strip()[:60]] += 1
                    break
            pecas.append((arq.stat().st_mtime, tipo, arq))
    return arqs, ilegiveis, pecas, c, alheias


def amostra(pecas, n=5):
    """As mais recentes, um tipo de cada antes de repetir tipo."""
    vistos, out = set(), []
    for rodada in (0, 1):
        for _, tipo, arq in sorted(pecas, reverse=True):
            if len(out) == n:
                return out
            if arq in out or (rodada == 0 and tipo in vistos):
                continue
            vistos.add(tipo)
            out.append(arq)
    return out


def relatorio(pasta: Path, oab: str = "", n: int = 5) -> str:
    arqs, ileg, pecas, c, alheias = censo(pasta, oab)
    L = [f"Arquivos olhados (.docx, e .pdf com nome de peça): {arqs} · peças reconhecidas: {len(pecas)} · "
         f"sem texto ou ilegíveis (escaneado, .doc antigo): {ileg}"]
    if oab:
        L.append(f"Peças assinadas por outra OAB (parte contrária, colega), fora da conta: {alheias}")
    def bloco(titulo, cnt, k=10):
        if cnt:
            L.append(f"\n{titulo}:")
            L.extend(f"  {v:>5}  {nome}" for nome, v in cnt.most_common(k))
    bloco("Tipos de peça", c["tipo"])
    bloco("Onde peticiona", c["justica"])
    bloco("Comarcas e varas", c["comarca"], 15)
    bloco("Assinatura (OAB)", c["oab"], 5)
    bloco("Títulos de seção mais usados", c["secao"], 15)
    bloco("Fórmulas (nº de peças em que aparecem)", c["formula"])
    bloco("Fecho", c["fecho"], 3)
    L.append("\nPara ler o estilo (as mais recentes, um tipo de cada):")
    L.extend(f"  {a}" for a in amostra(pecas, n))
    return "\n".join(L)


def demo():
    import tempfile
    from texto_docx import _docx_falso
    assin = ["Nestes termos, pede deferimento.", "Itabira, 1 de março de 2026.", "FULANA, OAB/MG 123.456"]
    miolo = ["Com a devida vênia, segue a fundamentação."] * 30
    docs = {
        "Clientes/Trab/A/inicial.docx": ["EXCELENTÍSSIMO SENHOR JUIZ DO TRABALHO DA 1ª VARA DO TRABALHO DE ITABIRA/MG",
                                         "FULANO vem propor RECLAMAÇÃO TRABALHISTA", "I. DOS FATOS", "II. DOS PEDIDOS"] + miolo + assin,
        "Clientes/Civ/B/defesa.docx": ["EXCELENTÍSSIMO SENHOR JUIZ DE DIREITO DA 1ª VARA CÍVEL DA COMARCA DE TIMÓTEO/MG",
                                       "BELTRANA vem apresentar CONTESTAÇÃO", "I. DOS FATOS", "II. DO MÉRITO"] + miolo + assin,
        "Clientes/Civ/C/arquivo qualquer.docx": ["EXCELENTÍSSIMO SENHOR JUIZ DE DIREITO DA COMARCA DE TIMÓTEO/MG",
                                                 "CICLANO vem propor AÇÃO DE COBRANÇA", "I. DOS FATOS"] + miolo + assin,
        "Clientes/Civ/D/jec.docx": ["EXCELENTÍSSIMO SENHOR JUIZ DE DIREITO DO JUIZADO ESPECIAL CÍVEL DA COMARCA DE ITABIRA/MG",
                                    "FULANO vem propor AÇÃO DE INDENIZAÇÃO"] + miolo + assin,
        "Clientes/Faz/E/inicial.docx": ["AO", "JUÍZO DO JUIZADO ESPECIAL DA FAZENDA PÚBLICA DA COMARCA DE ITABIRA/MG",
                                        "FULANO vem propor AÇÃO DE COBRANÇA em face do ESTADO DE MINAS GERAIS"] + miolo + assin,
        "Modelos/procuracao.docx": ["PROCURAÇÃO", "Outorgante: X"] + miolo,
        "Clientes/Civ/C/contestacao do reu.docx": ["EXCELENTÍSSIMO SENHOR JUIZ DE DIREITO DA COMARCA DE BELO HORIZONTE/MG",
                                                  "O RÉU vem apresentar CONTESTAÇÃO"] + miolo + ["Advogado do réu, OAB/SP 999.999"],
        "Pessoal/segredo.docx": ["EXCELENTÍSSIMO SENHOR JUIZ", "propor AÇÃO DE DIVÓRCIO"] + miolo + assin,
    }
    with tempfile.TemporaryDirectory() as d:
        for rel, pars in docs.items():
            p = Path(d) / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(_docx_falso(pars).getvalue())
        (Path(d) / "Clientes/vazio.docx").touch()  # docx de 0 byte nao pode quebrar
        arqs, ileg, pecas, c, alheias = censo(Path(d), "123456")
        assert alheias == 1, "peca do advogado do reu tem que ficar fora"
        assert "Belo Horizonte" not in c["comarca"]
        assert c["justica"]["Juizado Especial"] == 1, "Juizado tem prazo proprio: nao pode virar Justica Estadual"
        assert c["justica"]["Juizado Especial da Fazenda Pública"] == 1, "'AO JUÍZO' em duas linhas e Juizado da Fazenda (prazo proprio)"
        assert len(pecas) == 5, f"devia reconhecer 5 pecas, achou {len(pecas)} (procuracao nao e peca; Pessoal pula)"
        assert c["tipo"]["Reclamação trabalhista"] == 1 and c["tipo"]["Contestação"] == 1
        assert c["tipo"]["Petição inicial (ação)"] == 3, "peca com nome de arquivo qualquer tem que ser lida pelo conteudo"
        assert c["comarca"]["Timóteo"] == 2 and c["comarca"]["Itabira"] == 3, dict(c["comarca"])
        assert c["oab"]["OAB/MG 123456"] == 5
        assert c["justica"]["Justiça do Trabalho"] == 1
        assert c["secao"]["DOS FATOS"] == 3
        assert c["formula"]["devida vênia"] == 5 and c["formula"]["pede deferimento"] == 5
        assert ileg == 1, "o docx vazio conta como ilegivel"
        rel = relatorio(Path(d), "123456")
        assert "FULANO" not in rel and "BELTRANA" not in rel and "CICLANO" not in rel, "nome de parte vazou"
        assert len(amostra(pecas)) == 5  # um tipo de cada, depois completa ate 5
        assert len(amostra(pecas, 3)) == 3 and len(amostra(pecas, 10)) == 5  # nunca inventa peca que nao existe
    assert candidato("Peça.docx") and candidato("Contestação final.pdf") and candidato("RECURSO INOMINADO.PDF")
    assert not candidato("RG.pdf") and not candidato("Contracheque 2024.pdf") and not candidato("~$rascunho.docx")
    print("demo ok")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta", nargs="?")
    ap.add_argument("--oab", default="", help="numero da OAB do advogado, so digitos")
    ap.add_argument("--amostra", type=int, default=5, help="quantas pecas sugerir para ler o estilo (1 a 10)")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo or not a.pasta:
        demo()
    elif not Path(a.pasta).is_dir():
        print("Pasta não encontrada:", a.pasta)
        sys.exit(1)
    else:
        print(relatorio(Path(a.pasta), re.sub(r"\D", "", a.oab), max(1, min(a.amostra, 10))))
