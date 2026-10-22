# LoopWAM final manuscript

Open this folder as the project/workspace root. Main source: `main.tex`.
Compiler: **XeLaTeX** (recommended). All manuscript assets and fonts are local.

```text
xelatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Alternatively: `latexmk -xelatex main.tex` or `tectonic main.tex`.
A standard LaTeX installation and its packages are required. pdfLaTeX is not supported.

- `sec/`, `tables/`: final manuscript content.
- `figures/`, `assets/`: only referenced figures and logo.
- `fonts/`: four bundled font styles, loaded by filename.
- `loopwamreport.cls`, `math_commands.tex`: layout and notation.
- `references.bib`: bibliography.
- `THIRD_PARTY_NOTICES.txt`: original template attribution and license.

This is the clean version, without additions markup, review sources, or build caches.
No parent directory or machine-specific manuscript/font path is required.
