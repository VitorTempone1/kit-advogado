#!/usr/bin/env python3
"""Varredura mecânica de peça jurídica: padrão de redação + marcas de texto de IA, numa passada só.

    python3 auditar-peca.py <arquivo.docx|.txt|.md>
    python3 auditar-peca.py --teste          # autoteste

Reporta só o que se conta sem julgar: travessão, tique de apassivadora, tratamento
das partes inconsistente, repetição literal entre parágrafos, metacomentário,
vocabulário inflado, hedging e filler. O julgamento (se o achado sai ou fica) é do
agente, com o SKILL.md na mão. Citação literal fica fora de tudo: o que está entre
aspas curvas é ignorado antes de qualquer varredura, menos a de travessão.
"""

import html
import re
import sys
from pathlib import Path

TRAVESSAO = "—–"

# Apassivadora e imperativa impessoal. Idiomáticas, o problema é o acúmulo.
APASSIVADORA = re.compile(
    r"\b(?:[Rr]egistre|[Ee]sclareç|[Aa]ntecipe|[Dd]elimite|[Ss]ome|[Dd]iga|[Nn]ote|[Vv]eja"
    r"|[Ff]rise|[Oo]bserve|[Cc]onsigne|[Aa]crescente|[Rr]essalte|[Dd]estaque|[Aa]note)"
    r"[ae]?-se\b")

# Partes do processo: mesma parte tratada ora no singular ora no plural, ora com
# ora sem maiúscula. É o achado que mais rende, porque costuma esconder erro de fato.
PARTES = ("requerente", "requerido", "autor", "ré", "réu", "titular", "impugnante",
          "opoente", "embargante", "embargado", "agravante", "agravado", "apelante",
          "apelado", "recorrente", "recorrido", "exequente", "executado",
          "reclamante", "reclamado")

METACOMENTARIO = [
    # a peça falando de si em vez de argumentar
    r"\b(?:e )?é por isso que a \w+ o enfrenta",
    r"\bem vez de aguardar que seja invocado",
    r"\bum últim[oa] \w+ fecha o (?:capítulo|tópico)",
    r"\bpara que não reste dúvida",
    r"\bsão os \w+ pontos tratados a seguir",
    r"\bnão (?:foi|foram) trazid[ao]s? pela defesa",
    r"\bcomo se passa a demonstrar",
    r"\bconforme se verá adiante",
    r"\bpassa-se, (?:pois|então), a",
    # tropo de autoridade
    r"\bo ponto (?:decisivo|central|nodal|fulcral)",
    r"\bo que realmente importa",
    r"\bna verdade,",
    r"\bem última análise",
    r"\bno fundo,",
    r"\ba distinção não é (?:sutil|meramente)",
]

INFLADO = [
    r"\bdesempenha(?:m)? papel (?:fundamental|central|crucial)",
    r"\bde suma importância", r"\bno (?:atual )?cenário", r"\bpanorama atual",
    r"\bcristalin[oa]", r"\bsolar clareza", r"\bhialin[oa]",
    r"\bnorte(?:ador|adora)", r"\bmister se faz", r"\bdata maxima venia",
    r"\bpor derradeiro", r"\bab initio", r"\bex positis",
]

HEDGING = [r"\bparece que\b", r"\btalvez\b", r"\bpossivelmente\b", r"\beventualmente\b",
           r"\bs\.m\.j\b", r"\bsalvo melhor juízo\b", r"\bacredita-se\b", r"\bentende-se que\b"]

FILLER = [r"\bcom o fito de\b", r"\bno sentido de que\b", r"\bem que pese o fato de\b",
          r"\bna medida em que\b", r"\bdiante do fato de que\b", r"\bconforme já dito\b",
          r"\bcomo já mencionado anteriormente\b", r"\bimporta consignar que\b",
          r"\bcumpre destacar que\b", r"\bfaz-se necessário\b"]


def paragrafos(caminho):
    p = Path(caminho)
    if p.suffix.lower() == ".docx":
        from docx import Document
        return [x.text.strip() for x in Document(str(p)).paragraphs if x.text.strip()]
    bruto = p.read_text()
    if p.suffix.lower() in (".html", ".htm"):
        # Em HTML o travessao quase nunca aparece cru: ele vem como &mdash;, e a
        # varredura passava batido. Um dossie inteiro saiu com 16 deles depois de
        # o conferidor dar "Travessao: 0". Decodificar a entidade ANTES de contar
        # e o que faz a regra dura valer no formato em que a casa entrega.
        bruto = html.unescape(bruto)
    return [b.strip() for b in bruto.split("\n\n") if b.strip()]


def sem_citacao(texto):
    """Tira o que está entre aspas curvas: transcrição é literal e não se reescreve."""
    return re.sub(r"[“”\"][^“”\"]*[“”\"]", " ", texto)


def _achados(regexes, paras):
    saida = []
    for i, p in enumerate(paras):
        alvo = sem_citacao(p)
        for rx in regexes:
            for m in re.finditer(rx, alvo, re.I):
                saida.append((i, m.group(0)))
    return saida


def repeticoes(paras, n=8):
    """Trecho literal de n+ palavras que reaparece em outro parágrafo.

    Pré-filtra por n-grama comum e só então mede o trecho inteiro, senão cada janela
    deslizante da mesma frase vira um achado e o relatório tripliica sozinho.
    """
    palavras = [re.findall(r"\w+", sem_citacao(p).lower()) for p in paras]
    grams = [{" ".join(w[j:j + n]) for j in range(len(w) - n + 1)} for w in palavras]

    achados = []
    for i in range(len(paras)):
        for j in range(i + 1, len(paras)):
            if not grams[i] & grams[j]:
                continue
            a, b = palavras[i], palavras[j]
            melhor, fim_a, dp = 0, 0, [0] * (len(b) + 1)
            for x in range(1, len(a) + 1):
                anterior = 0
                for y in range(1, len(b) + 1):
                    atual = dp[y]
                    dp[y] = anterior + 1 if a[x - 1] == b[y - 1] else 0
                    if dp[y] > melhor:
                        melhor, fim_a = dp[y], x
                    anterior = atual
            if melhor < n:
                continue
            trecho = a[fim_a - melhor:fim_a]
            # número de processo, RPI, CNPJ e data reaparecem por dever de precisão, e o rol
            # de documentos repete o corpo por desenho. Repetição de PROSA é que interessa.
            if sum(t.isdigit() for t in trecho) / len(trecho) >= 0.35:
                continue
            achados.append(([i, j], " ".join(trecho)))
    return achados


def tratamento_partes(paras):
    texto = "\n".join(paras)
    fora = []
    for base in PARTES:
        formas = {}
        for m in re.finditer(rf"\b{base}s?\b", texto, re.I):
            formas[m.group(0)] = formas.get(m.group(0), 0) + 1
        if len(formas) > 1:
            fora.append((base, formas))
    return fora


def auditar(caminho):
    paras = paragrafos(caminho)
    texto = "\n".join(paras)
    linhas = []
    add = linhas.append

    add(f"# Auditoria: {Path(caminho).name}")
    add(f"{len(paras)} parágrafos, {len(texto)} caracteres\n")

    trav = [(i, p[:70]) for i, p in enumerate(paras) if any(c in p for c in TRAVESSAO)]
    add(f"## 1. Travessão (regra dura): {len(trav)}")
    add("   OK, zero." if not trav else "\n".join(f"   [{i}] {t}" for i, t in trav))

    ap = _achados([APASSIVADORA.pattern], paras)
    add(f"\n## 2. Apassivadora/imperativa impessoal: {len(ap)}")
    add("   " + (", ".join(f"[{i}] {t}" for i, t in ap) or "nenhuma"))
    if len(ap) > 4:
        add(f"   ⚠️ {len(ap)} ocorrências: o molde fica audível. Trocar parte por sujeito explícito.")

    tp = tratamento_partes(paras)
    add(f"\n## 3. Tratamento das partes inconsistente: {len(tp)}")
    for base, formas in tp:
        add(f"   {base}: " + ", ".join(f"{k} ({v}x)" for k, v in sorted(formas.items(), key=lambda x: -x[1])))
    add("   ⚠️ Conferir se a forma minoritária não está nomeando parte ERRADA." if tp
        else "   OK, uniforme.")

    rep = repeticoes(paras)
    add(f"\n## 4. Repetição literal entre parágrafos: {len(rep)}")
    for idxs, g in rep:
        add(f"   {idxs}: “{g}”")
    if not rep:
        add("   OK, nenhuma.")

    for titulo, regexes in (("5. Metacomentário e tropo de autoridade", METACOMENTARIO),
                            ("6. Vocabulário inflado", INFLADO),
                            ("7. Hedging", HEDGING),
                            ("8. Filler", FILLER)):
        hits = _achados(regexes, paras)
        add(f"\n## {titulo}: {len(hits)}")
        add("   " + (", ".join(f"[{i}] {t!r}" for i, t in hits) or "nenhum"))

    add("\n---\nFalta o passe de julgamento (regra de três forçada, paralelismo negativo,")
    add("ritmo, negrito, repetição de FUNDAMENTO que não é literal). Ver SKILL.md.")
    add("NÃO cortar: frase de fecho que carrega a tese do capítulo, uma por capítulo.")
    return "\n".join(linhas)


def _teste():
    amostra = (
        "Registre-se que a Requerente nada provou.\n\n"
        "O ponto decisivo, porém, é outro: a requerente não registrou hospedagem.\n\n"
        "Esclareça-se que a Titular sempre agiu de boa-fé, e o ônus era dos Requerentes.\n\n"
        "O Manual diz “que um travessão — aqui — dentro de citação nao conta”.\n\n"
        "Uma frase repetida de teste com oito palavras exatas aqui.\n\n"
        "Outro parágrafo com uma frase repetida de teste com oito palavras exatas aqui."
    )
    tmp = Path("/tmp/_auditar_teste.txt")
    tmp.write_text(amostra)
    r = auditar(tmp)
    assert "## 1. Travessão (regra dura): 1" in r, "travessão em citação: conta na regra dura"
    assert "## 2. Apassivadora/imperativa impessoal: 2" in r, r
    assert "requerente:" in r, "singular/plural + caixa deveria acusar"
    assert "o ponto decisivo" in r.lower(), "tropo de autoridade deveria acusar"
    assert "## 4. Repetição literal entre parágrafos: 1" in r, r
    tmp.unlink()

    # HTML: a entidade tem que contar igual ao caractere. Sem isto o conferidor
    # devolve "Travessao: 0" numa pagina cheia deles.
    tmp = Path("/tmp/_auditar_teste.html")
    tmp.write_text("<p>uma frase com &mdash; dentro</p>\n\n<p>outra sem nada</p>")
    r = auditar(tmp)
    assert "## 1. Travessão (regra dura): 1" in r, "&mdash; nao foi decodificado"
    tmp.unlink()

    print("autoteste OK")


if __name__ == "__main__":
    if "--teste" in sys.argv:
        _teste()
    elif len(sys.argv) < 2:
        sys.exit(__doc__)
    else:
        print(auditar(sys.argv[1]))
