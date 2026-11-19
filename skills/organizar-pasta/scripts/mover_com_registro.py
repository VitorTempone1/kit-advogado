# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Move (ou copia) arquivos e pastas seguindo um plano, com registro de desfazer.

Nada aqui apaga. Destino que já existe é recusado, nunca sobrescrito.

O plano é um arquivo de texto, uma linha por movimento, origem e destino separados por TAB:

    documentos/IMG_2231.jpg<TAB>documentos/2-RG-frente.jpg
    Downloads/contrato final v2.pdf<TAB>documentos/1-contrato-de-locacao.pdf

    uv run mover_com_registro.py plano.tsv --registro desfazer/2026-11-19-pasta-maria.md
        -> só mostra o que faria e acusa conflito (nada muda no disco)
    uv run mover_com_registro.py plano.tsv --registro <registro.md> --executar
        -> move de verdade; cada linha entra no registro ANTES do movimento
    uv run mover_com_registro.py plano.tsv --registro <registro.md> --executar --copiar
        -> copia em vez de mover (o original fica intacto)
    uv run mover_com_registro.py --desfazer <registro.md>
        -> devolve cada item movido ao lugar de origem, do último para o primeiro
    uv run mover_com_registro.py --teste
        -> autoteste numa pasta temporária

Nada aqui faz rede. Os arquivos não saem da máquina.
"""

import argparse
import re
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

try:  # Windows legado abre o console em cp1252 e engasga em acento
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LINHA = re.compile(r"^- (mover|copiar): `(.+?)` -> `(.+?)`$")


def contar(p: Path) -> int:
    if p.is_file():
        return 1
    return sum(1 for x in p.rglob("*") if x.is_file())


def ler_plano(caminho):
    pares = []
    for n, linha in enumerate(Path(caminho).read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip() or linha.startswith("#"):
            continue
        partes = linha.split("\t")
        if len(partes) != 2:
            sys.exit(f"Linha {n} do plano sem TAB entre origem e destino: {linha!r}")
        pares.append((Path(partes[0].strip()), Path(partes[1].strip())))
    return pares


def conferir(pares):
    problemas, destinos = [], set()
    for o, d in pares:
        if not o.exists():
            problemas.append(f"origem não existe: {o}")
        if d.exists():
            problemas.append(f"destino já existe (não sobrescrevo): {d}")
        if d in destinos:
            problemas.append(f"dois itens indo para o mesmo destino: {d}")
        destinos.add(d)
    return problemas


def executar(pares, registro: Path, copiar: bool):
    verbo = "copiar" if copiar else "mover"
    registro.parent.mkdir(parents=True, exist_ok=True)
    total = sum(contar(o) for o, _ in pares)
    with registro.open("a", encoding="utf-8") as r:
        r.write(f"\n## {datetime.now():%d/%m/%Y %H:%M} ({verbo}, {len(pares)} itens, "
                f"{total} arquivos)\n\nPasta de trabalho: `{Path.cwd()}`\n\n")
    feitos = 0
    for o, d in pares:
        n = contar(o)
        with registro.open("a", encoding="utf-8") as r:  # registra ANTES de mexer
            r.write(f"- {verbo}: `{o}` -> `{d}`\n")
        try:
            d.parent.mkdir(parents=True, exist_ok=True)
            if copiar:
                (shutil.copytree if o.is_dir() else shutil.copy2)(o, d)
            else:
                shutil.move(str(o), str(d))
            if contar(d) != n:
                raise RuntimeError(f"contei {contar(d)} no destino, esperava {n}")
        except Exception as e:
            with registro.open("a", encoding="utf-8") as r:
                r.write(f"  FALHOU: {e}\n")
            print(f"FALHOU em {o}: {e}. Parei aqui; o registro diz o que já foi feito.")
            return feitos, total
        feitos += n
    with registro.open("a", encoding="utf-8") as r:
        r.write(f"\nConta: {total} arquivos no plano, {feitos} chegaram.\n")
    return feitos, total


def desfazer(registro: Path):
    linhas = registro.read_text(encoding="utf-8").splitlines()
    voltou, pulou = 0, []
    for linha in reversed(linhas):
        m = LINHA.match(linha)
        if not m:
            continue
        verbo, o, d = m.group(1), Path(m.group(2)), Path(m.group(3))
        if verbo == "copiar":
            pulou.append(f"cópia, o original segue intacto em {o}: {d}")
            continue
        if not d.exists():
            pulou.append(f"não achei no destino: {d}")
            continue
        if o.exists():
            pulou.append(f"já existe algo na origem, não sobrescrevo: {o}")
            continue
        o.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(d), str(o))
        voltou += 1
    with registro.open("a", encoding="utf-8") as r:
        r.write(f"\n## {datetime.now():%d/%m/%Y %H:%M} DESFEITO: {voltou} itens voltaram\n")
        for p in pulou:
            r.write(f"- não voltou: {p}\n")
    return voltou, pulou


def _teste():
    import os
    with tempfile.TemporaryDirectory() as t:
        os.chdir(t)
        Path("bagunca/sub").mkdir(parents=True)
        Path("bagunca/IMG_1.jpg").write_text("rg")
        Path("bagunca/sub/a.pdf").write_text("a")
        Path("ja-existe.pdf").write_text("x")
        Path("plano.tsv").write_text(
            "bagunca/IMG_1.jpg\tdocs/1-rg.jpg\nbagunca/sub\tdocs/2-provas\n", encoding="utf-8")
        pares = ler_plano("plano.tsv")
        assert conferir(pares) == [], conferir(pares)
        assert conferir([(Path("bagunca/IMG_1.jpg"), Path("ja-existe.pdf"))]), "conflito passou"
        reg = Path("desfazer/teste.md")
        assert executar(pares, reg, copiar=False) == (2, 2)
        assert Path("docs/1-rg.jpg").exists() and not Path("bagunca/IMG_1.jpg").exists()
        assert "`bagunca/sub` -> `docs/2-provas`" in reg.read_text(encoding="utf-8")
        voltou, pulou = desfazer(reg)
        assert voltou == 2 and not pulou, (voltou, pulou)
        assert Path("bagunca/sub/a.pdf").read_text() == "a"
        assert executar(pares, Path("desfazer/c.md"), copiar=True) == (2, 2)
        assert Path("bagunca/IMG_1.jpg").exists() and Path("docs/1-rg.jpg").exists()
        os.chdir("/")
    print("autoteste OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plano", nargs="?")
    ap.add_argument("--registro")
    ap.add_argument("--executar", action="store_true")
    ap.add_argument("--copiar", action="store_true")
    ap.add_argument("--desfazer", metavar="REGISTRO")
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()
    if a.teste:
        return _teste()
    if a.desfazer:
        voltou, pulou = desfazer(Path(a.desfazer))
        print(f"{voltou} itens voltaram ao lugar.")
        for p in pulou:
            print(f"  não voltou: {p}")
        return
    if not a.plano or not a.registro:
        sys.exit("Uso: mover_com_registro.py plano.tsv --registro desfazer/<data>-<assunto>.md [--executar] [--copiar]")
    pares = ler_plano(a.plano)
    problemas = conferir(pares)
    for o, d in pares:
        print(f"{'copiar' if a.copiar else 'mover'}: {o} -> {d} ({contar(o) if o.exists() else 0} arquivos)")
    if problemas:
        print("\nNÃO EXECUTEI. Problemas:")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)
    if not a.executar:
        print(f"\nSimulação: nada mudou. {len(pares)} itens prontos. Rode de novo com --executar.")
        return
    feitos, total = executar(pares, Path(a.registro), a.copiar)
    print(f"\nConta: {total} arquivos no plano, {feitos} chegaram. Registro: {a.registro}")
    if feitos != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
