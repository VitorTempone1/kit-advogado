"""Um mutante por script de cálculo: troca uma constante da lei e exige que o teste REPROVE.
Teste que passa com o mutante não protege aquela regra. O arquivo volta ao original no fim.

    python3 testes/mutantes_calculos.py
"""
import subprocess
import sys
from pathlib import Path

S = Path(__file__).resolve().parent.parent / "skills"
MUTANTES = [  # (script, trecho original, trecho mutante, teste)
    ("calculo-rescisao/scripts/calculo_rescisao.py", "min(30 + 3 * anos, 90)", "min(30 + 3 * anos, 60)",
     "calculo-rescisao/scripts/test_calculo_rescisao.py"),
    ("calculo-horas-extras/scripts/calculo_horas_extras.py", "TOLERANCIA = 10", "TOLERANCIA = 5",
     "calculo-horas-extras/scripts/test_calculo_horas_extras.py"),
    ("atualizacao-monetaria/scripts/atualizacao_monetaria.py", "LEI_14905 = (2024, 9)", "LEI_14905 = (2024, 10)",
     "atualizacao-monetaria/scripts/test_atualizacao_monetaria.py"),
    ("pjecalc-preparo/scripts/pjecalc_preparo.py", "lim = menos_anos(aj, 5)", "lim = menos_anos(aj, 4)",
     "pjecalc-preparo/scripts/test_pjecalc_preparo.py"),
    ("calculo-previdenciario-basico/scripts/calculo_previdenciario.py", "min(96 + max(0, y - 2019), 105)",
     "min(97 + max(0, y - 2019), 105)", "calculo-previdenciario-basico/scripts/test_calculo_previdenciario.py"),
]

ruins = 0
for script, de, para, teste in MUTANTES:
    p = S / script
    orig = p.read_text(encoding="utf-8")
    assert orig.count(de) == 1, (script, de)
    try:
        p.write_text(orig.replace(de, para), encoding="utf-8")
        rc = subprocess.run([sys.executable, "-B", str(S / teste)], capture_output=True).returncode
    finally:
        p.write_text(orig, encoding="utf-8")
    ok = rc != 0
    ruins += not ok
    print("%s  %s: %s -> %s" % ("reprovou (bom)" if ok else "PASSOU (teste fraco)", script.split("/")[0], de, para))
sys.exit(ruins)
