# DAIMO — paper source

This directory holds the LaTeX source for the DAIMO paper, transcribed
from [`../daimo-paper-es.pdf`](../daimo-paper-es.pdf) on 2026-04-22.

## Files

| File | Purpose |
|---|---|
| `daimo-paper-es.txt` | Raw text extracted by `pdftotext -layout` from the PDF (reference only, do not edit) |
| `daimo-paper-es.tex` | **The editable LaTeX source** |
| `Makefile` | Build targets (`make`, `make clean`, `make distclean`) |

## What this file currently is

A **faithful transcription** of the Spanish PDF into LaTeX:

- All 9 sections preserved in original order.
- All 8 tables converted to `tabularx` with the same data.
- All ~30 references preserved as `\bibitem` entries with short citation keys.
- Four appendices (A-D) preserved verbatim.

## What this file is **not** yet

This is the **baseline** for the rewrite. It still contains the pre-v0.1.1
ontology (mentions of `daimo:Model`, `daimo:RuntimeProfile`,
`daimo:ReproducibilityArtifact` — classes that were later dropped or
renamed in the actual ontology). It also lacks:

- Running-scenario placement in §1 (currently only in §5).
- Contributions bullet list at end of §1.
- Figures (module diagram, class diagram, instance graph).
- Expanded §6 with reasoner, entailment, OOPS!, cross-class invariants,
  negative tests.
- Live URLs in §8 (currently forward-looking).
- LOT methodology citation in §3.

See `../daimo-rewrite-template.md` and the earlier rewrite plan for the
changes to make.

## Building the PDF

### Option 1 — Overleaf (zero install)

Upload `daimo-paper-es.tex` to https://overleaf.com and press Recompile.
Overleaf has the full TeX Live distribution; no local setup needed.

### Option 2 — Local TeX Live

```bash
# Install a minimal TeX Live with Spanish support
sudo apt install texlive-latex-base texlive-latex-extra \
                 texlive-lang-spanish texlive-fonts-recommended

# Build
make
```

### Option 3 — Tectonic (single-binary LaTeX)

```bash
# One-time install
curl --proto '=https' --tlsv1.2 -sSf https://drop-sh.fullyjustified.net | sh

# Build
tectonic daimo-paper-es.tex
```

## Rewriting workflow

The intended workflow to move from the Spanish baseline to the SWJ-ready
paper is:

1. Keep this `daimo-paper-es.tex` as the **untouched transcription**.
2. Copy it to `daimo-paper-es-v2.tex` and work on the restructure there.
3. Once v2 is stable, translate to `daimo-paper-en.tex`.
4. Final target submission file: `daimo-paper-en.tex` only.

This keeps the original text reachable for comparison while structural
changes are iterated.
