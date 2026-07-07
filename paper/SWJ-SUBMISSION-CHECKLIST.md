# SWJ Submission Checklist for DAIMO

Sources checked on 2026-07-06:

- Semantic Web Journal authors page: https://www.semantic-web-journal.net/authors
- Sage Semantic Web author instructions: https://journals.sagepub.com/author-instructions/swj
- Semantic Web Journal reviewers page: https://www.semantic-web-journal.net/reviewers

## Recommended Category

Primary recommendation: **Original Research Article with an ontology-engineering contribution**.

Reason: the current manuscript is not only a short ontology description. It
contains methodology, reuse analysis, formal validation, SHACL invariants,
negative tests, CQs, reproducibility, limitations, and a scientific argument
about governed AI-model exchange in dataspaces.

Fallback category: **Descriptions of ontologies**, if the editors prefer a
shorter artefact-oriented submission.

## Manuscript

| Requirement | Status | Action |
|---|---|---|
| English manuscript | Draft prepared | `paper/daimo-paper-en-swj-v4.tex` |
| PDF builds | Prepared | `paper/daimo-paper-en-swj-v4.pdf` |
| Sage LaTeX template | Prepared | Uses `sagej.cls` |
| Structured abstract | Prepared | Purpose/Methods/Results/Conclusions |
| Keywords | Prepared | 5 keywords |
| Figures/tables numbered | Prepared | Verify final order after last edits |
| References | Prepared | Final check before submission |
| Statements/declarations | Missing | Add final declarations section if required by submission system |
| ORCID | Missing | Submitting author required; co-author ORCIDs strongly encouraged |

## Reproducibility Package

| Requirement | Status | Action |
|---|---|---|
| Ontology source | Prepared | `daimo/ontology/` |
| SHACL shapes | Prepared | `daimo/shapes/` |
| Example KG | Prepared | `daimo/examples/` |
| SPARQL CQs | Prepared | `daimo/queries/queries.md` |
| Validation scripts | Prepared | `validate.py`, `reasoner_check.py`, `oops_check.py`, `tests/negative_test.py` |
| Reports | Prepared | `daimo/reports/` |
| Replay instructions | Prepared | `daimo/REPRODUCIBILITY.md` |
| Long-term stable archive | Missing | Publish GitHub release + Zenodo DOI |

## Scientific Evidence

| Evidence | Status |
|---|---|
| LOT methodology | Covered |
| Reuse-first positioning | Covered |
| MLDCAT-AP comparison | Covered |
| OWL reasoning | Covered |
| SHACL validation | Covered |
| Negative tests | Covered |
| 23 CQs | Covered |
| Case study | Covered as anonymised reproducible demonstrator |
| External expert validation | Pending human reviewers |
| Standards impact check | Prepared, but final MLDCAT-AP 3.1.0/DSP 2025-1 delta still pending |

## Submission Files

- Single manuscript PDF.
- LaTeX source package.
- Figure files if separated.
- Supplementary archive URL or DOI.
- Cover letter.
- Declarations text.
- Optional: response document only for resubmission, not initial submission.

