# DAIMO — Ontology for Governed AI Model Assets in Data Spaces

Version: **0.1.1**
Namespace: `https://w3id.org/pionera/daimo#` *(redirect registration pending — see [DEPLOYMENT.md](DEPLOYMENT.md))*
Licence: CC-BY 4.0 (ontology and docs), Apache-2.0 (validation code)
Methodology: [LOT (Linked Open Terms)](https://lot.linkeddata.es/)
DOI: *pending — will be assigned after Zenodo archival; see [DEPLOYMENT.md](DEPLOYMENT.md) §5*

DAIMO is an integration profile connecting DCAT-AP, MLDCAT-AP 3.0.0, ODRL, PROV-O, and Eclipse EDC to support publication, discovery, invocation, execution traceability, and contextualised evaluation of AI model assets exchanged in data spaces.

Design principle: **reuse what already exists, add only the dataspace-bridge layer.** DAIMO does not redefine the AI model, the dataset, the policy, or the catalog — it adds the seven classes that neither MLDCAT-AP nor EDC covers (Offering, Role, Deployment, IOContract, ExecutionAuthorization, DerivedArtifact, CrossParticipantProvenanceRecord, AuditEvidence, SharedEvaluationContext).

## Repository layout

```
daimo/
├── ontology/
│   ├── daimo-core.ttl          - 14 classes, 31 properties, disjointness, functional props
│   └── alignment.ttl           - alignment to DCAT, MLDCAT-AP, ODRL, PROV-O, DSP + external term declarations
├── shapes/
│   └── daimo-shapes.ttl        - 10 completeness shapes + 4 cross-class invariants (SHACL-SPARQL)
├── examples/
│   └── flood-risk-scenario.ttl - UPM / Leganés / INESData running scenario KG
├── queries/
│   └── queries.md              - 23 SPARQL CQ queries
├── tests/
│   ├── negative-examples.ttl   - 4-case deliberately-violating KG
│   └── negative_test.py        - harness that asserts invariants fire on violations
├── ORSD/
│   └── daimo-cqs.md            - 23 natural-language CQs with actor / inference / source
├── docs/                       - WIDOCO-generated HTML + WebVOWL (served by GitHub Pages)
├── reports/
│   ├── validation-results.md   - SHACL + CQ SPARQL run
│   ├── reasoner-report.md      - HermiT + OWL-RL + entailment check
│   ├── oops-report.md          - OOPS! pitfall scan
│   └── negative-test-results.md - negative-test harness run
├── w3id-redirect/
│   └── .htaccess               - redirect config for w3id.org PR (see DEPLOYMENT.md)
├── validate.py                 - SHACL + CQ SPARQL with OWL-RL materialisation
├── reasoner_check.py           - HermiT + OWL-RL + entailment-verification check
├── oops_check.py               - OOPS! REST-API client
├── tests/negative_test.py      - cross-class invariant negative tests
├── CITATION.cff                - citation metadata
├── .zenodo.json                - Zenodo deposit metadata
├── CHANGELOG.md                - version history
├── CONTRIBUTING.md             - contribution guidelines (LOT Phase 4)
├── DEPLOYMENT.md               - step-by-step deploy runbook for w3id / Pages / Zenodo
└── README.md
```

## Reuse map

| Layer | Source vocabulary | Used for |
|---|---|---|
| AI / ML asset | MLDCAT-AP 3.0.0 (`it6:`) | `MachineLearningModel`, `Task`, `Run`, `Flow`, `Evaluation`, `EvaluationMeasure`, `Benchmark`, `ComputerInfrastructure`, `Hardware`, `Library`, `HarmRisk`, `Modality` |
| Catalog | DCAT (`dcat:`) | `Catalog`, `Dataset`, `Distribution`, `DataService` |
| Policy | ODRL (`odrl:`) | `Offer`, `Agreement`, `Permission`, `Prohibition` |
| Provenance | PROV-O (`prov:`) | `Activity`, `Entity`, `Agent`, `Bundle`, `wasDerivedFrom`, `wasAssociatedWith` |
| Dataspace protocol | Dataspace Protocol (`dspace:`) | `ContractOffer`, `ContractNegotiation`, `TransferProcess` (informative `skos:related` / `skos:closeMatch` mappings) |
| EDC extensions | EDC namespace (`edc:`) | `ParticipantContext` only — DAIMO's sole EDC-specific extension reference. EDC itself is a runtime framework, not a vocabulary. |

Every reused term keeps its original IRI — DAIMO adds `rdfs:subPropertyOf` / `rdfs:subClassOf` alignment where appropriate, never `owl:equivalentClass` that would shadow the external vocabulary.

## DAIMO-native vocabulary (what DAIMO actually adds)

| Class | Aligned to | Justification |
|---|---|---|
| `AIAssetOffering` | `dcat:CatalogRecord` | A catalog-record entry that registers an AI model with an ODRL offer policy; neither DCAT nor MLDCAT-AP alone reifies the dataspace-offering event. |
| `ParticipantRole` + 5 subclasses | `prov:Role` | Dataspace role types (ModelProvider, ModelConsumer, PlatformOperator, Evaluator, GovernanceActor) that DCAT / MLDCAT-AP / EDC don't reify. |
| `ModelDeployment` | `prov:Entity` | Running/hosted instance, distinct from the model and from the service. |
| `IOContract` | *(stand-alone)* | Minimum machine-actionable invocation contract — not in DCAT or MLDCAT-AP. |
| `ExecutionAuthorization` | `odrl:Agreement` | ODRL agreement specialised with `authorizesRun`, `grantedTo`, `expiresAt` semantics. |
| `DerivedArtifact` | `prov:Entity`, `dcat:Resource` | Governed, catalog-describable output of a run exchanged across parties. |
| `CrossParticipantProvenanceRecord` | `prov:Bundle` | Dataspace-scoped PROV bundle. |
| `AuditEvidence` | `prov:Entity` | Hash + signature + timestamp evidence record. |
| `SharedEvaluationContext` | *(stand-alone)* | Reified grouping for comparability (task + dataset + version + protocol + seed). |

## Running the validation suite

```bash
cd daimo
python3 -m venv .venv
.venv/bin/pip install rdflib pyshacl owlrl owlready2

# four independent checks — each exits 0 on success
.venv/bin/python validate.py                   # SHACL + 23 CQ SPARQL (with OWL-RL closure)
.venv/bin/python reasoner_check.py             # HermiT + OWL-RL + entailment verification
.venv/bin/python oops_check.py                 # OOPS! pitfall scan (POSTs to oops.linkeddata.es)
.venv/bin/python tests/negative_test.py        # cross-class invariant negative tests
```

Reports are written to [reports/](reports/). Latest status:

| Check | Result |
|---|---|
| SHACL + CQ SPARQL | `conforms=True`, **23/23 CQs pass** ([reports/validation-results.md](reports/validation-results.md)) |
| Reasoner + entailment | HermiT consistent, 0 unsatisfiable, **0 forbidden-entailment warnings** ([reports/reasoner-report.md](reports/reasoner-report.md)) |
| OOPS! pitfalls | **0 Critical, 0 Important**, 2 Minor ([reports/oops-report.md](reports/oops-report.md)) |
| Negative invariant tests | **4/4 invariants fire on designated focus nodes** ([reports/negative-test-results.md](reports/negative-test-results.md)) |

## Competency questions

23 CQs organised in 5 categories:

| Category | Count | Actor(s) |
|---|---|---|
| R — Registration and Publication | 5 | Model Provider |
| D — Discovery and Selection | 4 | Model Consumer |
| E — Execution and Auditability | 5 | Platform Operator, Governance Actor |
| V — Evaluation and Reproducibility | 5 | Evaluator |
| G — Governance Bridge (DAIMO-native) | 4 | Model Consumer, Platform Operator, Governance Actor |

Full natural-language text: [ORSD/daimo-cqs.md](ORSD/daimo-cqs.md).
SPARQL bindings: [queries/queries.md](queries/queries.md).

## How this relates to the paper

The Spanish draft paper (`../daimo-paper-es.pdf`) claims 19 CQs and validates
14. This artefact:

- lifts all 19 into natural-language form (the paper only had codes),
- adds 4 new CQs (CQ-G1..G4) enabled by the dataspace-bridge vocabulary,
- deepens 7 of the 23 CQs so a proper share exercises subclass / subproperty
  reasoning rather than pure property retrieval,
- runs all 23 as executable SPARQL over a conforming example KG (with
  OWL-RL materialised closure so entailed triples are reachable),
- enforces minimum completeness with 10 SHACL shapes **and** four
  cross-class governance invariants (INV-1..INV-4, all tested positively
  and negatively).

## Publication status

| SWJ acceptance criterion | Status |
|---|---|
| C1 Scope | Pass |
| C2 Methodology (LOT) | Pass |
| C3 CQs in NL | Pass |
| C4 Reuse axiomatised | Pass |
| C5 Reasoner consistency + entailment | Pass |
| C6 OOPS! pitfalls | Pass |
| C7 SHACL conformance + invariants | Pass |
| C8 CQ SPARQL | Pass |
| C9 External validation | **Partial** — expert interviews pending |
| C10 FAIR publication | **Partial** — w3id redirect, Zenodo DOI, GitHub Pages pending — see [DEPLOYMENT.md](DEPLOYMENT.md) |

**8 Pass, 2 Partial, 0 Open.** See [../daimo-design-rationale.md](../daimo-design-rationale.md) for the full critique and [DEPLOYMENT.md](DEPLOYMENT.md) for the deployment runbook.

The design rationale and realignment from the current paper are in `../daimo-ontology-design.md`.

## Open items

- Replace placeholder ORCIDs in the ontology header with the authors' real identifiers.
- Register the `w3id.org/pionera/daimo` redirect.
- Generate HTML documentation with WIDOCO.
- Deposit a tagged release on Zenodo for a DOI.
- Run OOPS! pitfall scan and save the report.
- Conduct light expert interviews with one EDC / MLOps / data-space governance stakeholder (LOT phase 1 requirement validation).
