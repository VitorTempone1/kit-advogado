# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Texto de um .docx, so com a biblioteca padrao (o .docx e um zip com XML dentro).

Devolve o COMECO e o FIM da peca, que e onde estao o enderecamento e a assinatura,
sem despejar o meio inteiro (poupa o limite do plano):

  uv run texto_docx.py "peca.docx"                 # 4000 primeiros + 1500 ultimos caracteres
  uv run texto_docx.py "peca.docx" --inicio 8000 --fim 2000
  uv run texto_docx.py --demo                      # autoteste, sem arquivo

Nada aqui faz rede. O arquivo nao sai da maquina.
"""

import argparse
import io
import sys
import zipfile
from xml.etree import ElementTree

try:  # Windows legado abre o console em cp1252 e engasga em acento
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def texto(origem) -> str:
    """Um paragrafo por linha. `origem` e caminho ou arquivo aberto."""
    with zipfile.ZipFile(origem) as z:
        raiz = ElementTree.fromstring(z.read("word/document.xml"))
    linhas = []
    for p in raiz.iter(W + "p"):
        partes = []
        for no in p.iter():
            if no.tag == W + "t" and no.text:
                partes.append(no.text)
            elif no.tag == W + "tab":
                partes.append("\t")
            elif no.tag in (W + "br", W + "cr"):
                partes.append("\n")
        linha = "".join(partes).strip()
        if linha:
            linhas.append(linha)
    return "\n".join(linhas)


def recorte(t: str, inicio: int, fim: int) -> str:
    if len(t) <= inicio + fim:
        return t
    pulado = len(t) - inicio - fim
    return f"{t[:inicio]}\n\n[... {pulado} caracteres do meio omitidos ...]\n\n{t[-fim:]}"


def _docx_falso(paragrafos) -> io.BytesIO:
    corpo = "".join(f'<w:p><w:r><w:t xml:space="preserve">{x}</w:t></w:r></w:p>' for x in paragrafos)
    xml = f'<w:document xmlns:w="{W[1:-1]}"><w:body>{corpo}</w:body></w:document>'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("word/document.xml", xml)
    buf.seek(0)
    return buf


def demo() -> None:
    pec = ["EXCELENTÍSSIMO SENHOR JUIZ DE DIREITO DA 2ª VARA CÍVEL DA COMARCA DE ITABIRA/MG",
           "Fulano, já qualificado, vem apresentar CONTESTAÇÃO."] + ["meio"] * 2000 + [
           "Termos em que pede deferimento.", "Advogado Teste, OAB/MG 999.999"]
    t = texto(_docx_falso(pec))
    assert t.splitlines()[0].startswith("EXCELENTÍSSIMO"), "perdeu o enderecamento"
    r = recorte(t, 300, 80)
    assert "COMARCA DE ITABIRA" in r and "OAB/MG 999.999" in r, "recorte perdeu cabeca ou assinatura"
    assert "omitidos" in r and len(r) < 600, "recorte nao cortou o meio"
    assert recorte("curto", 300, 80) == "curto"
    print("demo ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--inicio", type=int, default=4000)
    ap.add_argument("--fim", type=int, default=1500)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo or not a.arquivo:
        demo()
        sys.exit(0)
    try:
        print(recorte(texto(a.arquivo), a.inicio, a.fim))
    except (zipfile.BadZipFile, KeyError):
        print("Nao consegui ler este arquivo como .docx (pode ser .doc antigo ou estar corrompido).")
        sys.exit(1)
