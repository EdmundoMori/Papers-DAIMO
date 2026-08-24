# DAIMO — Overview (executive summary)

> **Single-page map of the whole project.** Read this first, then dive into
> [`01-DAIMO-DESIGN.md`](01-DAIMO-DESIGN.md) (design & rationale),
> [`02-DAIMO-IMPLEMENTATION.md`](02-DAIMO-IMPLEMENTATION.md) (modules, classes,
> SHACL, how to run) and [`03-DAIMO-EVALUATION.md`](03-DAIMO-EVALUATION.md)
> (reasoning, pitfalls, SHACL, negative tests, scalability, CQ coverage).

## What DAIMO is

**DAIMO** (*Dataspace AI Model Ontology*) is an **OWL 2 DL integration profile**
that connects **DCAT-AP, MLDCAT-AP 3.0.0, ODRL, PROV-O and the Dataspace
Protocol (DSP, as operationalised by Eclipse EDC)** so that AI **model assets**
can be **published, discovered, invoked, traced and comparably evaluated** when
they are exchanged inside a **data space**.

- **IRI / namespace:** `https://w3id.org/pionera/daimo#` (prefix `daimo:`)
- **Version:** `0.1.6` (`owl:versionIRI …/daimo/0.1.6`), frozen review tag
  `v0.1.6-swj-submission`
- **Licence:** CC-BY 4.0 (ontology + docs), Apache-2.0 (validation code)
- **Methodology:** LOT — Linked Open Terms (<https://lot.linkeddata.es/>)
- **Authors:** Edmundo de Elvira Mori Orrillo, Jiayun Liu (Universidad
  Politécnica de Madrid, ROR `03n6nwv02`)
- **Target venue:** Semantic Web Journal (SWJ), ontology/data-description track

## The core idea: *reuse-first, add only the dataspace bridge*

DAIMO **does not redefine** the AI model, the dataset, the policy, the run or the
catalog. Those already exist in mature vocabularies and are **reused with their
original IRIs**. DAIMO adds **only the "dataspace-bridge" layer** that no reused
vocabulary provides: the governed *offering*, the runtime *deployment* and its
*I/O contract*, the *execution authorization*, the *derived artefact*, the
*cross-participant provenance record*, the *audit evidence*, the *shared
evaluation context*, and the dataspace *participant roles*.

Every reused term keeps its IRI; DAIMO adds `rdfs:subClassOf` /
`rdfs:subPropertyOf` alignment where semantically justified and **never uses
`owl:equivalentClass`** that would shadow an external vocabulary.

## What DAIMO adds (14 classes, 39 properties, 3 modules)

- **14 native classes** = **9 top-level bridge classes** + **5 participant-role
  subclasses**.
- **39 native properties** = **31 object properties** + **8 datatype
  properties**.
- **3 modules** (separate files so consumers can load only what they need):
  1. **Core** — `daimo/ontology/daimo-core.ttl` (classes + properties + axioms)
  2. **Alignment** — `daimo/ontology/alignment.ttl` (links to external vocabularies)
  3. **Shapes** — `daimo/shapes/daimo-shapes.ttl` (SHACL validation)

The 9 top-level classes: `AIAssetOffering`, `ParticipantRole`,
`ModelDeployment`, `IOContract`, `ExecutionAuthorization`, `DerivedArtifact`,
`CrossParticipantProvenanceRecord`, `AuditEvidence`, `SharedEvaluationContext`.
The 5 role subclasses: `ModelProvider`, `ModelConsumer`, `PlatformOperator`,
`Evaluator`, `GovernanceActor`.

## Reused vocabularies (the layers DAIMO bridges)

| Layer | Vocabulary (prefix) | Reused terms (examples) |
|---|---|---|
| AI / ML asset | MLDCAT-AP 3.0.0 (`it6:`) | `MachineLearningModel`, `Task`, `Run`, `Flow`, `Evaluation`, `ComputerInfrastructure` |
| Catalog | DCAT (`dcat:`) | `Catalog`, `CatalogRecord`, `Dataset`, `Distribution`, `DataService`, `Resource` |
| Policy | ODRL (`odrl:`) | `Offer`, `Agreement`, `Permission`, `Policy`, `assigner`, `assignee` |
| Provenance | PROV-O (`prov:`) | `Activity`, `Entity`, `Agent`, `Bundle`, `Role` |
| Dataspace protocol | DSP (`dspace:`) | `ContractOffer`, `ContractNegotiation`, `TransferProcess` (informative `skos:related`) |
| EDC extension | EDC (`edc:`) | `ParticipantContext` (DAIMO's only EDC-specific reference) |
| Integrity / identity | SPDX (`spdx:`), FOAF (`foaf:`) | `Checksum`, `algorithm`, `checksumValue`; `Agent` |

## Competency questions (23, five categories)

| Cat. | Category | # | Actor(s) |
|---|---|---|---|
| R | Registration and Publication | 5 | Model Provider |
| D | Discovery and Selection | 4 | Model Consumer |
| E | Execution and Auditability | 5 | Platform Operator, Governance Actor |
| V | Evaluation and Reproducibility | 5 | Evaluator |
| G | **Governance Bridge (DAIMO-native)** | 4 | Consumer, Operator, Governance Actor |

The **four G-questions (CQ-G1..G4)** are the ones **MLDCAT-AP alone cannot
answer** — they carry the novelty argument. Natural-language text is in
`daimo/ORSD/daimo-cqs.md`; SPARQL bindings in `daimo/queries/queries.md`.

## Validation snapshot (all green)

| Check | Tool | Result |
|---|---|---|
| Logical consistency | HermiT (owlready2) | **Consistent**, 0 unsatisfiable classes, 1.46 s |
| Entailment materialisation | OWL-RL | 853 → 2048 triples (1195 inferred), 0 `owl:Nothing`, 0.64 s |
| Entailment verification | custom check | 14 classes inspected, **0 forbidden-entailment warnings** (incl. no `odrl:Agreement`/`odrl:Policy` on `ExecutionAuthorization`) |
| Ontology pitfalls | OOPS! | **0 Critical, 0 Important, 2 Minor** (both benign/by-design; scan predates `forService`/`derivedFromAgreement`, see evaluation §3) |
| Structural + business constraints | SHACL (pySHACL) | example KG **conforms = True**; reused-class shapes use `sh:targetObjectsOf` (ISSUE-04) |
| Reused-class SHACL scope | `tests/reused_class_scope_test.py` | **9-cell matrix PASS**: unlinked Offer/Model/Run ignored; linked incomplete rejected |
| Question answerability | SPARQL over OWL-RL closure | **23/23 CQs return ≥1 row** |
| Negative testing | SHACL-SPARQL invariants | **9/9 invariants** (INV-1..INV-9) + 2 authorization/agreement per-class rules fire on malformed graphs (conforms = False, as expected) |
| Bounded scalability | synthetic benchmark | 100 & 1000 exchange units **conform**; 87k data triples / 157k closure triples at 1000 units |

See [`03-DAIMO-EVALUATION.md`](03-DAIMO-EVALUATION.md) for the full numbers and interpretation.

## Repository map (what lives where)

```
Papers-DAIMO/
├── docs/                         ← THIS consolidated documentation set
│   ├── 00-DAIMO-OVERVIEW.md
│   ├── 01-DAIMO-DESIGN.md
│   ├── 02-DAIMO-IMPLEMENTATION.md
│   ├── 03-DAIMO-EVALUATION.md
│   └── 04-DAIMO-ISSUE-RESOLUTION.md
├── daimo/
│   ├── ontology/daimo-core.ttl   ← 14 classes, 39 properties, disjointness, functional/asymmetric/inverse axioms
│   ├── ontology/alignment.ttl    ← alignment to DCAT/MLDCAT-AP/ODRL/PROV-O/DSP + external term stubs
│   ├── shapes/daimo-shapes.ttl   ← 9 completeness + 4 conformance shapes + 9 cross-class invariants
│   ├── examples/flood-risk-scenario.ttl   ← running scenario knowledge graph
│   ├── tests/negative-examples.ttl        ← deliberately-violating graph (INV-1..INV-9 + auth/agreement rules)
│   ├── queries/queries.md        ← 23 SPARQL competency-question queries
│   ├── ORSD/daimo-cqs.md         ← 23 natural-language CQs (actor / inference / source)
│   ├── reports/                  ← generated evidence (validation, reasoner, oops, negative, scalability)
│   ├── docs/                     ← WIDOCO HTML + WebVOWL site (GitHub Pages)
│   ├── validate.py / reasoner_check.py / oops_check.py / scalability_benchmark.py
│   ├── tests/negative_test.py
│   ├── tests/random_seed_test.py            ← optional-seed regression (ISSUE-03)
│   ├── tests/reused_class_scope_test.py     ← reused-class SHACL targets (ISSUE-04)
│   ├── CHANGELOG.md / CONTRIBUTING.md / CITATION.cff / .zenodo.json
└── paper/                        ← LaTeX sources & PDFs (SWJ paper, ES + EN)
```

## FAIR / publication status

- **Findable/Accessible:** persistent `w3id.org/pionera/daimo` URI (redirect PR
  pending), content-negotiated HTML (WIDOCO) + RDF, frozen GitHub release.
- **Interoperable:** OWL 2 DL, reuse of standard vocabularies, explicit alignment
  axioms, bilingual labels (en + es where applicable).
- **Reusable:** CC-BY 4.0, `CITATION.cff`, `.zenodo.json` (Zenodo DOI pending
  credentials).
- **Pending items:** w3id redirect PR, Zenodo DOI, and the SWJ **expert
  validation** (C9) — expert interviews still to be scheduled.

## Where to look for what (for paper writing)

- **"Ontología" section** → mostly [`01-DAIMO-DESIGN.md`](01-DAIMO-DESIGN.md)
  (classes, alignment, design decisions, non-alignment rationale) +
  [`02-DAIMO-IMPLEMENTATION.md`](02-DAIMO-IMPLEMENTATION.md) (formal constructs,
  SHACL).
- **"Evaluación" section** → [`03-DAIMO-EVALUATION.md`](03-DAIMO-EVALUATION.md)
  (all metrics, methods, CQ coverage, limitations, SWJ criteria mapping).
