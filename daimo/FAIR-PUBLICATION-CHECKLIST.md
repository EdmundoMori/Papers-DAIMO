# DAIMO FAIR Publication Checklist

This checklist separates work already prepared in the repository from actions
that require author credentials.

Sources checked on 2026-07-08:

- Semantic Web Journal author page: https://www.semantic-web-journal.net/authors
- Sage SWJ author instructions: https://journals.sagepub.com/author-instructions/swj
- Semantic Web Journal Open Science Data policy text on the author page.

## Prepared Locally

| Item | Status | Evidence |
|---|---|---|
| Persistent namespace target | Prepared | `w3id-redirect/.htaccess` (target: GitHub Pages) |
| RDF serialisations | Prepared | `docs/ontology.ttl`, `.owl`, `.jsonld`, `.nt` |
| Alignment and shapes public files | Prepared | `docs/alignment.ttl`, `docs/daimo-shapes.ttl` |
| CQ document public copy | Prepared | `docs/daimo-cqs.md` |
| Citation metadata | Prepared (no fake DOI/ORCID) | `CITATION.cff` |
| Zenodo metadata | Prepared (no fake DOI) | `.zenodo.json` |
| Release runbook | Prepared | `DEPLOYMENT.md` |
| Reproducibility guide | Prepared | `REPRODUCIBILITY.md` |
| Validation reports | Prepared | `reports/` |
| WIDOCO HTML | Regenerated 2026-07-08 | `docs/index-en.html` (version 0.1.6) |
| OOPS! scan | Re-run 2026-07-08 | `reports/oops-report.md` (0/0/2) |
| Frozen review release tag | Prepared | `v0.1.6-swj-submission` |
| GitHub Pages workflow | Prepared | `.github/workflows/daimo-pages.yml` |

## Requires Author Action

| Item | Required action |
|---|---|
| GitHub Pages | Enable Pages with source **GitHub Actions** on `EdmundoMori/Papers-DAIMO`. |
| GitHub release | Publish release from tag `v0.1.6-swj-submission` on GitHub. |
| `w3id` | Submit PR to `perma-id/w3id.org` using `w3id-redirect/.htaccess`. |
| Zenodo DOI | Enable Zenodo–GitHub integration, deposit release, insert versioned DOI in `CITATION.cff` and README. |
| ORCIDs | Optional: add real ORCID IRIs to ontology header and `CITATION.cff`. |
| Expert interviews | Schedule and record LOT Phase 1 expert validation (SWJ C9). |
| Post-submission immutability | Do not mutate the archived artefact after submission; publish changes as a new release. |

## SWJ-Relevant Notes

The Semantic Web Journal asks authors to provide resources critical for
evaluation and reproduction whenever feasible. The DAIMO package should
therefore be submitted with:

- the paper PDF;
- the frozen GitHub release URL `https://github.com/EdmundoMori/Papers-DAIMO/releases/tag/v0.1.6-swj-submission`;
- ontology source modules;
- generated serialisations;
- SHACL shapes;
- example graph;
- SPARQL CQs;
- validation scripts;
- reports;
- instructions in `REPRODUCIBILITY.md`.

Until Zenodo DOI and w3id redirect are live, the GitHub release is the
authoritative immutable snapshot for peer review.
