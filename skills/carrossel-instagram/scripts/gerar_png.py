"""Transforma cada .html de uma pasta em PNG do tamanho exato, usando o Chrome
(ou Edge, Brave, Chromium) que já está instalado no computador. Sem dependência.

    uv run gerar_png.py <pasta> [--tamanho 1080x1350]
    uv run gerar_png.py --teste

Por que não Playwright: ele baixa um navegador próprio (~150 MB) e pede um passo
de instalação a mais. Quase todo computador já tem Chrome ou Edge (o Edge vem no
Windows), e o modo headless deles fotografa a página do mesmo jeito.
"""
import os, shutil, struct, subprocess, sys, tempfile
from pathlib import Path

CANDIDATOS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]
for base in ("ProgramFiles", "ProgramFiles(x86)", "LocalAppData"):
    raiz = os.environ.get(base)
    if raiz:
        CANDIDATOS += [
            rf"{raiz}\Google\Chrome\Application\chrome.exe",
            rf"{raiz}\Microsoft\Edge\Application\msedge.exe",
            rf"{raiz}\BraveSoftware\Brave-Browser\Application\brave.exe",
        ]


def achar_navegador():
    if os.environ.get("NAVEGADOR"):
        return os.environ["NAVEGADOR"]
    for c in CANDIDATOS:
        if Path(c).is_file():
            return c
    for nome in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        if shutil.which(nome):
            return shutil.which(nome)
    sys.exit("Não achei Chrome, Edge, Brave nem Chromium neste computador. "
             "Instale o Google Chrome (gratuito, google.com/chrome) e rode de novo.")


def tamanho_png(caminho):
    with open(caminho, "rb") as f:
        f.read(16)
        return struct.unpack(">II", f.read(8))


MINIMO = 500


def alvo(h, largura, altura, perfil):
    if largura >= MINIMO:
        return h.resolve().as_uri()
    moldura = Path(perfil, f"moldura-{h.stem}.html")
    moldura.write_text(
        f"<html><body style='margin:0;background:#ddd'><iframe src='{h.resolve().as_uri()}' "
        f"style='border:0;display:block;width:{largura}px;height:{altura}px;background:#fff'>"
        "</iframe></body></html>", encoding="utf-8")
    return moldura.as_uri()


def gerar(pasta, largura, altura):
    nav = achar_navegador()
    htmls = sorted(h for h in Path(pasta).glob("*.html") if not h.name.startswith("._"))  # ._ = lixo do macOS em disco externo
    if not htmls:
        sys.exit(f"Nenhum .html em {pasta}")
    # O Chrome não abre janela com menos de 500 px: largura de celular (390) sairia como
    # página de 500 cortada. Abaixo disso, a página entra num iframe da largura pedida,
    # dentro de uma moldura de 500; a imagem sai com 500 e a página ocupa a esquerda.
    janela = max(largura, MINIMO)
    perfil = tempfile.mkdtemp(prefix="perfil-png-")  # perfil separado: não briga com o Chrome aberto
    erros = 0
    try:
        for h in htmls:
            png = h.with_suffix(".png")
            png.unlink(missing_ok=True)
            subprocess.run([
                nav, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--no-first-run", "--no-default-browser-check",
                f"--user-data-dir={perfil}", "--force-device-scale-factor=1", "--allow-file-access-from-files",
                f"--window-size={janela},{altura}", "--virtual-time-budget=5000",
                f"--screenshot={png.resolve()}", alvo(h, largura, altura, perfil),
            ], capture_output=True, timeout=90)
            if not png.exists():
                print(f"FALHOU  {h.name}: o navegador não gerou a imagem"); erros += 1
                continue
            dim = tamanho_png(png)
            ok = dim == (janela, altura)
            erros += not ok
            print(f"{'ok     ' if ok else 'TAMANHO'} {png.name}  {dim[0]}x{dim[1]}")
    finally:
        shutil.rmtree(perfil, ignore_errors=True)
    return erros


def primeiro_pixel(caminho):
    import zlib  # o 1º pixel da 1ª linha não depende do filtro do PNG
    dados = Path(caminho).read_bytes()
    i, idat = 8, b""
    while i < len(dados):
        n = struct.unpack(">I", dados[i:i + 4])[0]
        if dados[i + 4:i + 8] == b"IDAT":
            idat += dados[i + 8:i + 8 + n]
        i += 12 + n
    return tuple(zlib.decompress(idat)[1:4])


def teste():
    with tempfile.TemporaryDirectory() as d:
        Path(d, "a.html").write_text(
            "<html><body style='margin:0;background:#123'>teste</body></html>", encoding="utf-8")
        assert gerar(d, 1080, 1350) == 0, "PNG fora do tamanho"
        assert tamanho_png(Path(d, "a.png")) == (1080, 1350)
        assert gerar(d, 1080, 1920) == 0
        Path(d, "a.html").write_text(  # celular: a página tem que enxergar 390 px, não 500
            "<html><body style='margin:0;background:#fff'>"
            "<script>if(innerWidth!==390)document.body.style.background='#00f'</script></body></html>",
            encoding="utf-8")
        assert gerar(d, 390, 300) == 0
        assert primeiro_pixel(Path(d, "a.png")) == (255, 255, 255), "celular renderizou largo"
    print("teste ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--teste"]:
        teste(); sys.exit(0)
    if not args:
        sys.exit(__doc__)
    largura, altura = 1080, 1350
    if "--tamanho" in args:
        i = args.index("--tamanho")
        largura, altura = map(int, args[i + 1].lower().split("x"))
        del args[i:i + 2]
    sys.exit(1 if gerar(args[0], largura, altura) else 0)
