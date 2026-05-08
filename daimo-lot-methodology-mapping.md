# DAIMO — LOT Methodology Mapping

Date: 2026-04-21
Methodology: LOT (Linked Open Terms), Poveda-Villalón, Fernández-Izquierdo, Fernández-López, García-Castro. 2022. "LOT: An industrial oriented ontology engineering framework." *Engineering Applications of Artificial Intelligence* 111: 104755. https://doi.org/10.1016/j.engappai.2022.104755
LOT reference site: https://lot.linkeddata.es/
LOT resources (ORSD templates, CORAL corpus): https://github.com/oeg-upm/LOT-resources

Purpose of this document: map every LOT activity onto the current state of DAIMO, identify what is already covered, and list the concrete deliverables still needed to present DAIMO as a LOT-compliant SWJ submission.

## Phase coverage at a glance

| LOT phase | Current DAIMO coverage | Status |
|---|---|---|
| 1. Requirements Specification | §3.1 "Especificación de requisitos" + 19 implicit CQs | Partial |
| 2. Implementation | §3.2, §3.3, §4 (classes, properties, SHACL, example graph) | Strong but incomplete |
| 3. Publication | §3.4, §8 (namespace reserved; HTML/repo pending) | Weak |
| 4. Maintenance | §3.4 last paragraph (one sentence) | Not addressed |

## Phase 1. Requirements Specification

LOT output: an `Ontology Requirements Specification Document` (ORSD) using the official LOT template.

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Identify purpose, scope, intended end-users | Stated narratively in §1, §3.1 | Not in ORSD form | Fill in ORSD sections: purpose, scope, implementation language, intended end-users, intended uses |
| Collect pre-glossary of terms | Implicit in Tables 4, 5 | No glossary artefact | Export class/property list as a pre-glossary |
| Elicit functional requirements as competency questions | 19 CQs exist (CQ-R1..R5, CQ-D1..D4, CQ-E1..E4, CQ-V1..V5) | CQs have codes but no natural-language text in the paper | Write each CQ in natural language; store in ORSD |
| Elicit non-functional requirements | Not explicit | Missing | Add: OWL 2 DL, CC-BY 4.0, multilingual labels (en/es), FAIR publication, SHACL validation, persistent URI |
| Validate requirements with domain experts | Not done | Missing (admitted in §6.4) | Schedule review with ≥1 EDC/dataspace expert, ≥1 MLOps operator, ≥1 model provider/consumer |

Artefacts to produce in phase 1:
- `DAIMO-ORSD.pdf` (use LOT template from https://github.com/oeg-upm/LOT-resources/tree/master/ORSD)
- `daimo-cqs.md` with 19 CQs in natural language + SPARQL binding
- `daimo-glossary.md`

## Phase 2. Implementation

LOT structures this phase in four sub-activities.

### 2a. Conceptualization

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Organise domain knowledge into a conceptual model | §4.2 text + Tables 4, 5 | No diagram | Produce module diagram in Chowlk notation |
| Create ontology diagrams | None | Missing entirely | Produce (i) module diagram, (ii) class diagram for core, (iii) instance-graph example |

Artefacts:
- `daimo-module-diagram.chowlk` (+ PNG/SVG)
- `daimo-class-diagram.chowlk`
- `daimo-instance-example.chowlk`

### 2b. Ontology Reuse

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Identify reusable terms from CQs and data | Table 6 lists DCAT, ODRL, PROV-O, ML-Schema | Reuse is asserted, not justified per term | For each reused term, add rationale + which CQ(s) it answers |
| Search existing ontologies | Done informally | Not documented | Produce a reuse matrix (term, source ontology, namespace, why, which CQ) |
| Evaluate fit of candidate ontologies | Partly in §2 | Shallow | Extend related-work comparison to include MLDCAT-AP, FAIR4ML, DPROD, Gaia-X SD, IDS-IM, DCAT-AP |
| Declare alignment axioms | Only `daimo:Model ⊑ dcat:Dataset` stated | No axioms shown for other reuses | Write full alignment axioms: `daimo:Run ⊑ mls:Run`, `daimo:hasEvaluation ⊑ mls:hasEvaluation`, policy attachment via `odrl:hasPolicy`, provenance via `prov:wasDerivedFrom`, etc. |

Artefacts:
- `daimo-reuse-matrix.md` (already half-drafted in `daimo-requirements-matrix.md` — promote and extend)
- `daimo-alignment.ttl`

### 2c. Encoding

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Encode in OWL | Exists | Not shown in paper | Confirm OWL 2 DL compliance; state profile |
| Add ontology-level metadata (dct:creator, dct:publisher, dct:license, owl:versionIRI, owl:versionInfo) | `purl.org/pionera/daimo#` namespace declared only | Missing metadata | Add full header: creator, contributor, title, issued, modified, versionIRI, versionInfo, license (CC-BY 4.0), cites |
| Add lexicalisation (rdfs:label, skos:prefLabel in en+es, rdfs:comment) | Unknown | Likely incomplete | Add bilingual labels and comments for all classes and properties |

Artefact:
- Updated `daimo.ttl` with complete annotations

### 2d. Evaluation

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Syntactic check | Implicit | Not reported | Run `riot --validate`; report pass |
| Reasoner consistency | Not reported | Missing | Run HermiT or Pellet; report 0 unsatisfiable classes, reasoning time |
| Pitfall scan | Not reported | Missing | Run OOPS! (https://oops.linkeddata.es/); report scorecard and resolutions |
| Requirement fulfilment | §6.1 claims 14/19 CQs implemented | CQ-to-SPARQL traceability not shown | Produce a table: CQ → SPARQL file → expected vs actual row count |
| SHACL validation | §6.2 asserts shapes pass | No shapes shown, no report numbers | Include 2–3 shape excerpts in paper + full `shapes.ttl` in repo + report (`conformance = true`, validated node count) |

Artefacts:
- `oops-report.html`
- `reasoner-report.txt`
- `validation-results.md`
- `queries/CQ-R1.rq` … `queries/CQ-V5.rq`

## Phase 3. Publication

LOT splits this into documentation and online publication with content negotiation.

### 3a. Documentation

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Generate HTML documentation | §8 admits pending | Missing | Run WIDOCO (https://github.com/dgarijo/Widoco) against `daimo.ttl` to produce `docs/` |
| Include all metadata, diagrams, examples | Not produced | Missing | WIDOCO handles metadata; embed Chowlk diagrams manually |
| Release candidate review | Not done | Missing | Circulate to domain experts for sign-off before publication |

Artefacts:
- `docs/index-en.html` (WIDOCO output)
- `docs/index-es.html` (optional bilingual)

### 3b. Publication

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Serve at persistent URI | `purl.org/pionera/daimo#` reserved | Not live | Configure purl.org redirect OR migrate to w3id.org (recommended by LOT) |
| Content negotiation (HTML + RDF) | None | Missing | Host on GitHub Pages or institutional server with `.htaccess` / nginx rewrite |
| Publish artefact bundle | Not done | Missing | Create GitHub repo with: `ontology/daimo.ttl`, `shapes/`, `queries/`, `examples/`, `docs/`, `LICENSE`, `README.md`, `CHANGELOG.md` |
| Archive release | Not done | Missing | Tag v1.0.0, push to Zenodo for DOI |

Artefacts:
- Public GitHub repo URL
- Live namespace resolvable
- Zenodo DOI

## Phase 4. Maintenance

| LOT activity | DAIMO current state | Gap | Action |
|---|---|---|---|
| Issue tracking for new requirements/errors | Not set up | Missing | Enable GitHub Issues; document triage policy in `README.md` |
| Scheduled iterations | Not defined | Missing | State in §8 that DAIMO follows LOT phase-4 governance with release cadence and deprecation policy |
| Deprecation policy | Not defined | Missing | Commit to `owl:deprecated` pattern for removed terms |

Artefacts:
- GitHub Issues enabled
- `CONTRIBUTING.md`
- Short maintenance paragraph in §8

## Paper-level additions required by LOT

1. In §3, add the LOT-citation paragraph (drafted in the earlier critique).
2. In §3, insert a small table "LOT phase → DAIMO section" mirroring this document's first table.
3. In §3.1, cite the CORAL corpus for CQ elicitation patterns.
4. In §4, cite Chowlk and show the module diagram.
5. In §8, reference WIDOCO for documentation generation and Zenodo for archival.

## Time estimate

| Block | Days |
|---|---|
| Write ORSD + CQs in natural language | 1–2 |
| Draw Chowlk diagrams (3 figures) | 1 |
| Extend reuse matrix + alignment axioms + ontology metadata | 1 |
| Run OOPS!, reasoner, SHACL report, capture outputs | 0.5 |
| Run WIDOCO, prepare GitHub repo, Zenodo DOI | 0.5–1 |
| Expert interviews (3 participants × 30–45 min + write-up) | 1–2 |
| Integrate all of the above into the English paper rewrite | 2–3 |
| **Total** | **7–10 days of focused work** |

This is the same total effort already implied by the SWJ remediation list — adopting LOT does not add work, it organises it.

## Reference checklist for the repo

```
daimo/
├── ontology/
│   ├── daimo.ttl
│   └── alignment.ttl
├── shapes/
│   └── daimo-shapes.ttl
├── queries/
│   ├── CQ-R1.rq ... CQ-V5.rq
├── examples/
│   └── example-kg.ttl
├── docs/
│   ├── index-en.html   (WIDOCO)
│   └── diagrams/*.svg
├── ORSD/
│   └── DAIMO-ORSD.pdf
├── reports/
│   ├── oops-report.html
│   ├── reasoner-report.txt
│   └── validation-results.md
├── LICENSE          (CC-BY 4.0 for ontology, Apache-2.0 for code)
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## Sources

- LOT landing and phase descriptions: https://lot.linkeddata.es/#details
- LOT paper: Poveda-Villalón et al. 2022, EAAI 111, 104755.
- LOT resources (ORSD templates): https://github.com/oeg-upm/LOT-resources
- CORAL corpus: https://w3id.org/CORAL
- Chowlk notation: https://chowlk.linkeddata.es/
- WIDOCO: https://github.com/dgarijo/Widoco
- OOPS! pitfall scanner: https://oops.linkeddata.es/
- Themis (test-based validation): https://themis.linkeddata.es/
