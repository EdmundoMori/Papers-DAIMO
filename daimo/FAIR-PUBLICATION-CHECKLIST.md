# DAIMO FAIR Publication Checklist

This checklist separates work already prepared in the repository from actions
that require author credentials.

Sources checked on 2026-07-06:

- Semantic Web Journal author page: https://www.semantic-web-journal.net/authors
- Sage SWJ author instructions: https://journals.sagepub.com/author-instructions/swj
- Semantic Web Journal Open Science Data policy text on the author page.

## Prepared Locally

| Item | Status | Evidence |
|---|---|---|
| Persistent namespace target | Prepared | `w3id-redirect/.htaccess` |
| RDF serialisations | Prepared | `docs/ontology.ttl`, `.owl`, `.jsonld`, `.nt` |
| Alignment and shapes public files | Prepared | `docs/alignment.ttl`, `docs/daimo-shapes.ttl` |
| CQ document public copy | Prepared | `docs/daimo-cqs.md` |
| Citation metadata | Prepared with placeholders | `CITATION.cff` |
| Zenodo metadata | Prepared with placeholders | `.zenodo.json` |
| Release runbook | Prepared | `DEPLOYMENT.md` |
| Reproducibility guide | Prepared | `REPRODUCIBILITY.md` |
| Validation reports | Prepared | `reports/` |

## Requires Author Action

| Item | Required action |
|---|---|
| Public repository | Create or confirm final GitHub repository URL and update `repository-code` in `CITATION.cff`. |
| GitHub Pages | Enable Pages from `docs/` and verify HTML/RDF files resolve over HTTPS. |
| `w3id` | Submit PR to `perma-id/w3id.org` using `w3id-redirect/.htaccess`. |
| Zenodo DOI | Tag release `v0.1.6`, publish GitHub release, archive in Zenodo, insert versioned DOI. |
| ORCIDs | Replace placeholder ORCID IRIs in ontology headers and citation metadata. |
| WIDOCO HTML | Regenerate `docs/index-en.html` from v0.1.6 sources before public release. |
| Stable archive URL | Provide a long-term stable URL for SWJ evaluation and replication. |
| Post-submission immutability | Do not mutate the archived artefact after submission; publish changes as a new release. |

## SWJ-Relevant Notes

The Semantic Web Journal asks authors to provide resources critical for
evaluation and reproduction whenever feasible. The DAIMO package should
therefore be submitted with:

- the paper PDF;
- a stable archive URL or DOI;
- ontology source modules;
- generated serialisations;
- SHACL shapes;
- example graph;
- SPARQL CQs;
- validation scripts;
- reports;
- instructions in `REPRODUCIBILITY.md`.

