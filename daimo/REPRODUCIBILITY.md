# DAIMO Reproducibility Guide

This document defines the exact local replay procedure for DAIMO v0.1.6.
It is intended for reviewers and for the Semantic Web Journal supplementary
material package.

## Environment

Tested locally on 2026-07-06 with the repository virtual environment:

```bash
cd daimo
python3 -m venv .venv
.venv/bin/pip install rdflib pyshacl owlrl owlready2
```

The OOPS! check additionally requires network access to
`https://oops.linkeddata.es/rest`.

## One-shot Validation

Run the four core checks and the bounded scalability benchmark from the
`daimo/` directory:

```bash
.venv/bin/python validate.py | tee reports/validation-results.md
.venv/bin/python reasoner_check.py
.venv/bin/python oops_check.py
.venv/bin/python tests/negative_test.py | tee reports/negative-test-results.md
.venv/bin/python scalability_benchmark.py --sizes 100 1000
```

Expected results:

| Check | Expected result |
|---|---|
| Turtle parse | ontology triples: 593; shape triples: 342; data triples: 225 |
| SHACL positive | `conforms=True` |
| Competency questions | 23/23 return at least one row; OWL-RL closure: 1988 triples |
| HermiT | consistent; 0 unsatisfiable classes |
| OWL-RL | pre triples: 818; post triples: 1988; materialised: 1170 |
| Entailment verification | 14 DAIMO classes inspected; 0 forbidden-entailment warnings |
| Negative tests | all 6 invariants fire on designated focus nodes |
| OOPS! | 0 Critical, 0 Important, 2 Minor |
| Bounded scalability | 100 and 1,000 synthetic exchange units conform; 80,053 data triples at 1,000 units; OWL-RL 49.403s, SHACL 126.164s, SPARQL suite 0.363s |

OOPS! can intermittently return an `unexpected_error` response. The script now
treats that as a failed external service call rather than as a zero-pitfall
success. Re-run the check if that happens.

The scalability benchmark is not a production-throughput claim. It exercises
growth in governed exchange instances while the DAIMO core remains fixed at 14
native classes. Larger runs such as 10,000 units are supported by the script,
but should only be cited after they have been executed on the target machine.

## Paper Builds

From the `paper/` directory:

```bash
pdflatex -interaction=nonstopmode daimo-paper-es-v4.tex
pdflatex -interaction=nonstopmode daimo-paper-es-v4.tex

pdflatex -interaction=nonstopmode daimo-paper-en-swj-v4.tex
pdflatex -interaction=nonstopmode daimo-paper-en-swj-v4.tex
```

Expected outputs:

| File | Role |
|---|---|
| `paper/daimo-paper-es-v4.pdf` | Spanish master version |
| `paper/daimo-paper-en-swj-v4.pdf` | English SWJ working version derived from v4 |

## Generated Ontology Serialisations

The public RDF serialisations in `docs/` are regenerated from
`ontology/*.ttl`:

```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from rdflib import Graph
root = Path("daimo")
docs = root / "docs"
g = Graph()
for f in sorted((root / "ontology").glob("*.ttl")):
    g.parse(f, format="turtle")
g.serialize(destination=docs / "ontology.ttl", format="turtle")
g.serialize(destination=docs / "ontology.owl", format="xml")
g.serialize(destination=docs / "ontology.jsonld", format="json-ld", indent=2)
g.serialize(destination=docs / "ontology.nt", format="nt")
PY
```

The WIDOCO HTML page must still be regenerated before final public release,
because no WIDOCO JAR is bundled in this repository.
