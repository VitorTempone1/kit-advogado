# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx>=1.1"]
# ///
"""Texto simples (.md) vira .docx de documento jurídico, com [PREENCHER] grifado em amarelo.

    uv run gerar_docx.py minuta.md saida.docx
    uv run gerar_docx.py --teste

O que ele entende do .md, e nada além:
    # Título          -> centralizado, negrito, caixa alta
    ## Seção         -> negrito
    **trecho**        -> negrito dentro do parágrafo
    linha em branco   -> separa parágrafos
    [PREENCHER ...]   -> grifo amarelo, para o advogado achar o que falta

Fonte Times New Roman 12, texto justificado, espaçamento 1,5. Nada aqui faz rede.
"""

import re
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import Pt

TROCO = re.compile(r"(\*\*.+?\*\*|\[PREENCHER[^\]]*\])")


def escrever(par, texto, negrito=False):
    for pedaco in TROCO.split(texto):
        if not pedaco:
            continue
        if pedaco.startswith("**") and pedaco.endswith("**"):
            par.add_run(pedaco[2:-2]).bold = True
        elif pedaco.startswith("[PREENCHER"):
            run = par.add_run(pedaco)
            run.bold = True
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            par.add_run(pedaco).bold = negrito or None


def gerar(origem, destino):
    doc = Document()
    estilo = doc.styles["Normal"]
    estilo.font.name = "Times New Roman"
    estilo.font.size = Pt(12)
    estilo.paragraph_format.line_spacing = 1.5
    estilo.paragraph_format.space_after = Pt(6)
    blocos = [b.strip() for b in Path(origem).read_text(encoding="utf-8").split("\n\n") if b.strip()]
    for bloco in blocos:
        texto = " ".join(l.strip() for l in bloco.splitlines())
        par = doc.add_paragraph()
        if texto.startswith("# "):
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            escrever(par, texto[2:].upper(), negrito=True)
        elif texto.startswith("## "):
            escrever(par, texto[3:], negrito=True)
        else:
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            escrever(par, texto)
    doc.save(destino)
    faltam = sum(len(re.findall(r"\[PREENCHER", p.text)) for p in Document(destino).paragraphs)
    return faltam


def _teste():
    with tempfile.TemporaryDirectory() as t:
        md, dx = Path(t) / "a.md", Path(t) / "a.docx"
        md.write_text("# Procuração\n\n**OUTORGANTE:** Maria, CPF [PREENCHER: CPF].\n\n"
                      "## Poderes\n\nOs da cláusula ad judicia\ne mais nada.", encoding="utf-8")
        assert gerar(md, dx) == 1
        pars = Document(dx).paragraphs
        assert pars[0].text == "PROCURAÇÃO" and pars[0].runs[0].bold
        assert pars[1].runs[0].bold and pars[1].runs[0].text == "OUTORGANTE:"
        grifo = [r for r in pars[1].runs if r.text.startswith("[PREENCHER")][0]
        assert grifo.font.highlight_color == WD_COLOR_INDEX.YELLOW
        assert pars[3].text == "Os da cláusula ad judicia e mais nada."
    print("autoteste OK")


if __name__ == "__main__":
    if "--teste" in sys.argv:
        _teste()
    elif len(sys.argv) != 3:
        sys.exit(__doc__)
    else:
        n = gerar(sys.argv[1], sys.argv[2])
        print(f"Gerado: {sys.argv[2]} ({n} campos [PREENCHER] grifados em amarelo)")
