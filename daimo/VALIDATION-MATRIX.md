# DAIMO Validation Matrix

Version: **0.1.6**
Date: 2026-07-07
Latest run: [reports/](reports/)

This matrix is the **requirements-to-evidence traceability** for DAIMO. Every
requirement, class, property, axiom, and competency question in the ontology
is mapped to the specific check that validates it and the report file where
the result is recorded.

Read this document when you need to answer: *"how do we know X is correct?"*
The answer should always be a pointer to a script + report + expected
outcome.

---

## Table of contents

1. [Top-level scorecard](#1-top-level-scorecard)
2. [Validation layers](#2-validation-layers)
3. [How to reproduce](#3-how-to-reproduce)
4. [Requirement × Evidence matrix](#4-requirement-evidence-matrix)
5. [Class × Evidence matrix](#5-class-evidence-matrix)
6. [Property × Evidence matrix](#6-property-evidence-matrix)
7. [Axiom × Evidence matrix](#7-axiom-evidence-matrix)
8. [Competency question × Evidence matrix](#8-competency-question-evidence-matrix)
9. [Cross-class invariant × Evidence matrix](#9-cross-class-invariant-evidence-matrix)
10. [Reviewer replay script](#10-reviewer-replay-script)

---

## 1. Top-level scorecard

| # | SWJ criterion | Status | Evidence |
|---|---|---|---|
| C1 | Scope explicit and bounded | **Pass** | [ONTOLOGY-REFERENCE.md](ONTOLOGY-REFERENCE.md) — five lifecycle stages, nine native classes, explicit non-goals |
| C2 | Methodology named and followed | **Pass** | [LOT](https://lot.linkeddata.es/) + phase mapping in [../daimo-lot-methodology-mapping.md](../daimo-lot-methodology-mapping.md) |
| C3 | CQs stated in natural language, numbered, grouped | **Pass** | [ORSD/daimo-cqs.md](ORSD/daimo-cqs.md) — 23 CQs, 5 categories |
| C4 | Reuse axiomatised | **Pass** | [ontology/alignment.ttl](ontology/alignment.ttl) — 8 external class subsumptions and 5 external property subsumptions; the combined source modules expose 6 DAIMO-to-external subproperty declarations because `hasOffering ⊑ foaf:isPrimaryTopicOf` is declared in the core |
| C5 | Reasoner consistency | **Pass** | [reports/reasoner-report.md](reports/reasoner-report.md) — HermiT 0 unsat, OWL-RL 0 forbidden entailments |
| C6 | OOPS! scan | **Pass** | [reports/oops-report.md](reports/oops-report.md) — 0 Critical, 0 Important |
| C7 | SHACL structural conformance | **Pass** | [reports/validation-results.md](reports/validation-results.md) — **9 per-class shapes + 3 conformance shapes + 6 cross-class SHACL-SPARQL invariants** (all conform on the positive KG); SHACL module itself declared as `owl:Ontology` at `https://w3id.org/pionera/daimo/shapes` since v0.1.4 |
| C8 | Each CQ answered by SPARQL | **Pass** | same report — 23/23 CQs return ≥1 row |
| C9 | External validation | **Partial** | Expert interviews pending |
| C10 | FAIR publication | **Partial** | All artefacts ready; live w3id redirect + Zenodo DOI pending DEPLOYMENT.md execution |

**8 Pass / 2 Partial. Both Partials are operational, not engineering.**

---

## 2. Validation layers

Ten independent checks. Each has a single script or tool, a known input set, a known output format, and a pass criterion.

| Layer | Checks | Script / tool | Report | Pass criterion |
|---|---|---|---|---|
| L1 | Turtle syntax | `rdflib` parse in [validate.py](validate.py) | [reports/validation-results.md](reports/validation-results.md) | 0 parse errors |
| L2 | OWL 2 DL logical consistency | HermiT via `owlready2` in [reasoner_check.py](reasoner_check.py) | [reports/reasoner-report.md](reports/reasoner-report.md) | `consistent=True`, 0 unsatisfiable classes |
| L3 | OWL-RL materialisation | `owlrl` in [reasoner_check.py](reasoner_check.py) | same | 0 individuals typed as `owl:Nothing`, 0 unsatisfiable subclasses |
| L4 | **Entailment verification** | Custom check in [reasoner_check.py](reasoner_check.py) | same | 0 forbidden-superclass entailments for 14 DAIMO classes |
| L5 | Pitfall scan | OOPS! REST API in [oops_check.py](oops_check.py) | [reports/oops-report.md](reports/oops-report.md) | 0 Critical, 0 Important |
| L6 | SHACL structural conformance | `pyshacl` in [validate.py](validate.py) | [reports/validation-results.md](reports/validation-results.md) | `conforms=True` on the positive KG |
| L7 | SHACL-SPARQL cross-class invariants | same run | same | all 6 invariants satisfied on the positive KG |
| L8 | **Negative-test harness** | [tests/negative_test.py](tests/negative_test.py) | [reports/negative-test-results.md](reports/negative-test-results.md) | all 6 invariants fire on the designated negative focus nodes |
| L9 | CQ-answering SPARQL | [validate.py](validate.py) post OWL-RL closure | [reports/validation-results.md](reports/validation-results.md) | 23/23 queries return ≥1 row |
| L10 | **Bounded scalability** | [scalability_benchmark.py](scalability_benchmark.py) | [reports/scalability-benchmark.md](reports/scalability-benchmark.md) | 100 and 1,000 synthetic exchange units conform; SPARQL suite remains below 1s at 1,000 units |

---

## 3. How to reproduce

```bash
cd daimo
python3 -m venv .venv
.venv/bin/pip install rdflib pyshacl owlrl owlready2

# One-shot replay of every validation layer
.venv/bin/python validate.py         # L1 + L6 + L7 + L9
.venv/bin/python reasoner_check.py   # L2 + L3 + L4
.venv/bin/python oops_check.py       # L5
.venv/bin/python tests/negative_test.py   # L8
.venv/bin/python scalability_benchmark.py --sizes 100 1000   # L10
```

All five scripts exit 0 iff their layer passes. Exit-code composition is a clean gate: if all five return 0, the ontology passes every layer.

Latest run timestamps are in the respective report files under `reports/`.

---

## 4. Requirement × Evidence matrix

Non-functional requirements declared in [ORSD/daimo-cqs.md](ORSD/daimo-cqs.md).

| Requirement | How validated | Evidence |
|---|---|---|
| OWL 2 DL profile | HermiT accepts (HermiT rejects non-DL) | [reports/reasoner-report.md](reports/reasoner-report.md), reasoning time reported |
| CC-BY 4.0 licence on ontology | `dct:license <https://creativecommons.org/licenses/by/4.0/>` declared in ontology header | [ontology/daimo-core.ttl](ontology/daimo-core.ttl#L26) |
| Persistent w3id URI | `vann:preferredNamespaceUri` + `owl:versionIRI` declared | [ontology/daimo-core.ttl](ontology/daimo-core.ttl#L29-L32); live redirect pending — see [DEPLOYMENT.md](DEPLOYMENT.md) |
| SHACL shapes for every DAIMO class | 9 per-class shapes + 3 conformance shapes | [shapes/daimo-shapes.ttl](shapes/daimo-shapes.ttl) |
| Every DAIMO term reuse-first-justified | Every class comment in the TTL explains the gap being filled | [ontology/daimo-core.ttl](ontology/daimo-core.ttl) + [ONTOLOGY-REFERENCE.md](ONTOLOGY-REFERENCE.md) §2 |
| Machine-readable metadata completeness | WIDOCO HTML renders `dct:title`, `dct:description`, `dct:license`, `dct:issued`, `dct:modified`, `owl:versionIRI` | [docs/index-en.html](docs/index-en.html) header block |
| Axiomatic alignment (not just prefix listing) | Every external subsumption is a triple in [alignment.ttl](ontology/alignment.ttl), reachable by reasoning | L2+L3+L4 reports; all alignments survived the entailment-verification check after v0.1.1 fixes |
| Bounded scalability | Synthetic conforming graphs scale the number of governed exchange instances while keeping the core ontology fixed | L10 report: 1,000 units, 80,053 data triples, SHACL conforms, OWL-RL 53.672s, SHACL 135.010s, SPARQL suite 0.356s |
| Modularity and extensibility | Core, alignment, shapes, examples, queries, and tests are separate artefacts; SemVer and deprecation policy are documented | [CHANGELOG.md](CHANGELOG.md), [CONTRIBUTING.md](CONTRIBUTING.md), [ONTOLOGY-REFERENCE.md](ONTOLOGY-REFERENCE.md), [DEPLOYMENT.md](DEPLOYMENT.md) |

---

## 5. Class × Evidence matrix

For each DAIMO-native class, the shape that checks it, the negative test that proves the shape bites, and the CQ that queries it.

| Class | Completeness shape | Invariant | Negative test | CQ |
|---|---|---|---|---|
| `daimo:AIAssetOffering` | AIAssetOfferingShape (§7.1.1) | — | — | R1, R2, R5, G1 |
| `daimo:ParticipantRole` (+5 subclasses) | ParticipantRoleShape (§7.1.2) | — | — | R5 |
| `daimo:ModelDeployment` | ModelDeploymentShape (§7.1.3) | INV-3 | `bad:INV3-deployment` | E1, E2, E3, G2 |
| `daimo:IOContract` | IOContractShape (§7.1.4) | — | — | R4, D3, E1, G2 |
| `daimo:ExecutionAuthorization` | ExecutionAuthorizationShape (§7.1.5) | INV-4 | `bad:INV4-auth` | E2, E4, E5, G3 |
| `daimo:DerivedArtifact` | DerivedArtifactShape (§7.1.6) | INV-1 | `bad:INV1-artifact` | E5, G4 |
| `daimo:CrossParticipantProvenanceRecord` | CrossParticipantProvenanceRecordShape (§7.1.7) | — | — | G4 |
| `daimo:AuditEvidence` | AuditEvidenceShape (§7.1.8) | — | — | E4 |
| `daimo:SharedEvaluationContext` | SharedEvaluationContextShape (§7.1.9) | — | — | V1, V2, V3, V5 |

Each completeness shape is validated by L6 (positive example conforms) and L8 negative tests, where available, force the shape to fire on a deliberately-malformed instance. If the shape has no negative-test counterpart yet, that cell is `—` (an opportunity for future test expansion).

### Conformance shapes (on reused classes)

| Reused class | Conformance shape | What it mandates in DAIMO graphs |
|---|---|---|
| `odrl:Offer` | OfferInDAIMOShape (§7.2.1) | `odrl:assigner` 1..*; `odrl:target` at Policy OR Permission level |
| `it6:MachineLearningModel` | MachineLearningModelInDAIMOShape (§7.2.2) | `odrl:hasPolicy` 1..*, `dct:title` 1..*, `dct:identifier` 1..* |
| `it6:Run` | RunInDAIMOShape (§7.2.3) | `it6:hasFlow`, `mls:realizes`, `prov:wasAssociatedWith`, `prov:startedAtTime` |

These three shapes are the reason DAIMO is called a *profile*: they specify obligations on reused vocabularies when those vocabularies appear inside a DAIMO graph.

---

## 6. Property × Evidence matrix

The core declares 29 object properties and 8 datatype properties. The table below lists the CQ that is the *primary* exercise of each property when the current CQ suite traverses it; inverse-navigation helpers and optional schema links are documented explicitly instead of being counted as CQ-critical evidence (see [ONTOLOGY-REFERENCE.md](ONTOLOGY-REFERENCE.md) §9 for the complete map).

### 6.1 Object properties

| Property | Primary CQ | Secondary CQs |
|---|---|---|
| `daimo:offersModel` | R1 | R2 (via foaf:primaryTopic entailment), G1 |
| `daimo:offeredBy` | R1 | R2, R5, G1 |
| `daimo:hasOfferPolicy` | R3 | D2 |
| `daimo:hasRole` | R5 | — |
| `daimo:inParticipantContext` | R5 | G4 (via spansParticipantContext) |
| `daimo:deploysModel` | E1 | E2, D3, G2 |
| `daimo:hasDeployment` | inverse helper | inverse of `deploysModel`; not required by current CQ set |
| `daimo:exposedAs` | E1 | D3, G2 |
| `daimo:onInfrastructure` | E3 | G2 |
| `daimo:hasIOContract` | E1 | R4, D3, G2 |
| `daimo:authorizesRun` | E2 | G3 |
| `daimo:authorizedBy` | E2 (inverse path) | — |
| `daimo:grantedTo` | E2 | G3 |
| `daimo:derivedFromRun` | E5 | G4 |
| `daimo:hasDerivedArtifact` | inverse helper | inverse of `derivedFromRun`; not required by current CQ set |
| `daimo:underAuthorization` | E5 | — |
| `daimo:spansParticipantContext` | G4 | — |
| `daimo:records` | G4 | — |
| `daimo:evidenceOf` | E4 | — |
| `daimo:hasAuditEvidence` | inverse helper | inverse of `evidenceOf`; not required by current CQ set |
| `daimo:signedBy` | E4 | — |
| `daimo:integrityHash` | E4 | — |
| `daimo:hasOffering` | inverse helper | inverse of `offersModel` and subproperty of `foaf:isPrimaryTopicOf` |
| `daimo:usesEvaluationContext` | V1 | V2, V3 |
| `daimo:contextTask` | V1 | — |
| `daimo:contextDataset` | V1 | — |
| `daimo:contextFlow` | V5 | — |
| `daimo:inputSchema` | optional schema link | object property to `dcat:Resource`; unused in current example KG |
| `daimo:outputSchema` | optional schema link | object property to `dcat:Resource`; unused in current example KG |

### 6.2 Datatype properties

| Property | Primary CQ | Value example in KG |
|---|---|---|
| `daimo:inputFormat` | R4, E1, D3 | `"application/json"` |
| `daimo:outputFormat` | R4, E1, D3 | `"application/geo+json"` |
| `daimo:authMethod` | R4, E1, D3 | `"oauth2-bearer"` |
| `daimo:recordedAt` | E4 | `"2026-04-20T08:03:00Z"^^xsd:dateTime` |
| `daimo:expiresAt` | G3 | `"2027-04-20T00:00:00Z"^^xsd:dateTime` |
| `daimo:protocol` | V1 | `"holdout"` |
| `daimo:randomSeed` | V1 | `42` |
| `daimo:datasetVersion` | V1 | `"2026.1"` |

---

## 7. Axiom × Evidence matrix

| Axiom | Evidence | Confirmed by |
|---|---|---|
| `AllDisjointClasses(9 top-level DAIMO classes)` | HermiT accepts (no contradictions); entailment check shows none of the 9 classes is inferred to be an instance of another | L2 + L4 |
| 27 `owl:FunctionalProperty` declarations (19 object, 8 datatype) | Functional object properties whose domain is a DAIMO class with a node shape (e.g., `AIAssetOffering`, `ModelDeployment`, `DerivedArtifact`) are paired with `sh:maxCount 1` in that shape; functionality of external-domain DAIMO properties (e.g., `daimo:usesEvaluationContext` on `it6:Evaluation`) is enforced only via the OWL `owl:FunctionalProperty` declaration, since no DAIMO shape targets the external class. SHACL passes on the positive KG. | L6 + L2 |
| `daimo:authorizedBy owl:inverseOf daimo:authorizesRun` | Round-trip: given a run in the example KG, `SELECT ?auth WHERE { ?run daimo:authorizedBy ?auth }` returns the same agreement as `SELECT ?auth WHERE { ?auth daimo:authorizesRun ?run }` | Manual query verification; CQ-E2 uses the direct direction |
| 8 external `rdfs:subClassOf` alignments in `alignment.ttl` | Entailment-verification check: each DAIMO class resolves to exactly its expected superclass set; 0 forbidden entailments | L4 |
| 5 external `rdfs:subPropertyOf` alignments in `alignment.ttl` plus 1 inverse-side alignment in `daimo-core.ttl` | SubPropertyOf chains materialised by OWL-RL; CQ-R2 and CQ-E1 specifically exercise `offersModel ⊑ foaf:primaryTopic` | L3 + L9 |
| 7 documented non-alignments (`offeredBy`, `authorizesRun`, `grantedTo` to PROV, `evidenceOf`, `contextDataset`, `contextFlow`, `datasetVersion`) | Each documented with `rdfs:comment` or alignment-module rationale explaining the semantic reason; entailment check confirms no unintended inferences | L4 |
| 3 SKOS informative mappings to DSP | Not intended to entail; verified by visual inspection of alignment.ttl | N/A |

---

## 8. Competency question × Evidence matrix

All 23 CQs validated by L9. Each CQ has a natural-language statement, a SPARQL binding, and an expected row count on the positive KG.

| CQ | Category | Actor | Inference | Expected ≥ rows | Last run |
|---|---|---|---|---|---|
| R1 | Registration | Model Provider | no | 1 | PASS rows=3 |
| R2 | Registration | Model Provider | subPropertyOf chain | 1 | PASS rows=1 |
| R3 | Registration | Model Provider | no | 1 | PASS rows=1 |
| R4 | Registration | Model Provider | no | 1 | PASS rows=2 |
| R5 | Registration | Model Provider | subClassOf path | 1 | PASS rows=2 |
| D1 | Discovery | Model Consumer | no | 1 | PASS rows=3 |
| D2 | Discovery | Model Consumer | no (negation-as-failure) | 1 | PASS rows=2 |
| D3 | Discovery | Model Consumer | no | 1 | PASS rows=4 |
| D4 | Discovery | Model Consumer | numeric filter | 1 | PASS rows=1 |
| E1 | Execution | Platform Operator | subPropertyOf chain | 1 | PASS rows=4 |
| E2 | Execution | Platform Operator | join | 1 | PASS rows=1 |
| E3 | Execution | Platform Operator | no | 1 | PASS rows=2 |
| E4 | Execution | Governance Actor | no | 1 | PASS rows=1 |
| E5 | Execution | Governance Actor | no | 1 | PASS rows=1 |
| V1 | Evaluation | Evaluator | no | 1 | PASS rows=1 |
| V2 | Evaluation | Evaluator | aggregation (MAX) | 1 | PASS rows=1 |
| V3 | Evaluation | Evaluator | ordering | 2 | PASS rows=2 |
| V4 | Evaluation | Evaluator | no | 1 | PASS rows=1 |
| V5 | Evaluation | Evaluator | no | 1 | PASS rows=4 |
| G1 | Governance | Model Consumer | no | 1 | PASS rows=1 |
| G2 | Governance | Platform Operator | no | 1 | PASS rows=2 |
| G3 | Governance | Governance Actor | direct DAIMO--ODRL bridge | 1 | PASS rows=1 |
| G4 | Governance | Governance Actor | aggregation (GROUP_CONCAT) | 1 | PASS rows=1 |

**Totals**: 23 CQs defined, 23 with SPARQL bindings, 23/23 return ≥1 row on the current example KG.

---

## 9. Cross-class invariant × Evidence matrix

Each invariant must (a) conform on the positive KG, (b) fire on exactly the designated negative focus node.

| Invariant | Positive KG | Negative focus node | Fires? |
|---|---|---|---|
| INV-1 — Derivation-authorization | conforms | `bad:INV1-artifact` | ✓ (PASS) |
| INV-2 — Run-agent-grantee match | conforms | `bad:INV2-run` | ✓ (PASS) |
| INV-3 — Deployment-service model match | conforms | `bad:INV3-deployment` | ✓ (PASS) |
| INV-4 — Authorization-expiry temporal | conforms | `bad:INV4-auth` | ✓ (PASS) |
| INV-5 — Offering model in policy target | conforms | `bad:INV5-offering` | ✓ (PASS) |
| INV-6 — Offering agent ≡ policy assigner | conforms | `bad:INV6-offering` | ✓ (PASS) |

Last negative-test run: [reports/negative-test-results.md](reports/negative-test-results.md).

Both dimensions matter: positive conformance alone proves only that the invariant doesn't false-trigger on valid data; negative firing proves it actually catches violations. Together they demonstrate the invariant is semantically correct and semantically useful.

---

## 10. Reviewer replay script

What a reviewer should do to verify the claims in the DAIMO paper end-to-end, in order:

### Step 1 — open the ontology reference
Read [ONTOLOGY-REFERENCE.md](ONTOLOGY-REFERENCE.md) §§2–4 to verify every class and property has (a) an IRI, (b) an rdfs:label and rdfs:comment, (c) a documented reuse decision. Each section's "Deliberate design choices" block explains the non-obvious modelling trade-offs.

### Step 2 — install and run
```bash
cd daimo
python3 -m venv .venv
.venv/bin/pip install rdflib pyshacl owlrl owlready2
.venv/bin/python validate.py         # expect exit 0
.venv/bin/python reasoner_check.py   # expect exit 0
.venv/bin/python oops_check.py       # expect exit 0
.venv/bin/python tests/negative_test.py   # expect exit 0
```

### Step 3 — inspect the reports
Open each file in [reports/](reports/) and cross-check against the pass criteria in §2 of this matrix.

### Step 4 — verify a specific claim
- *"The three bug-fix alignments are correct"* → open [reports/reasoner-report.md](reports/reasoner-report.md) §Entailment-verification, confirm `daimo:ExecutionAuthorization` is inferred as `odrl:Agreement` and NOT as `prov:Activity`.
- *"Six invariants actually catch violations"* → open [reports/negative-test-results.md](reports/negative-test-results.md), confirm six focus-node-matched violations.
- *"CQ-G4 does not combinatorially explode"* → open [queries/queries.md](queries/queries.md) §CQ-G4, confirm `GROUP BY ?bundle`; run and confirm 1 row returned.
- *"Integrity hashes carry their algorithm"* → open [examples/flood-risk-scenario.ttl](examples/flood-risk-scenario.ttl), search for `ex:audit-run-legs`, confirm the `daimo:integrityHash` points to a blank-node `spdx:Checksum` with `spdx:algorithm` and `spdx:checksumValue`.
- *"ODRL offers carry a target"* → search the same file for `ex:flood-risk-policy`, confirm `odrl:target` and `odrl:assigner` are present.
- *"Exposed-as is not functional"* → open [ontology/daimo-core.ttl](ontology/daimo-core.ttl), search for `daimo:exposedAs`, confirm no `owl:FunctionalProperty` on its declaration.

### Step 5 — verify the paper's numeric claims
Compare:
- Paper abstract says "23/23 CQs return expected rows" → [reports/validation-results.md](reports/validation-results.md) summary line.
- Paper §6.3 says "HermiT consistent, 0.58 s, 0 unsatisfiable" → [reports/reasoner-report.md](reports/reasoner-report.md) HermiT section.
- Paper §6.4 says "0 forbidden-entailment warnings" → same report, Entailment section.
- Paper §6.5 says "OOPS! 0 Critical, 0 Important" → [reports/oops-report.md](reports/oops-report.md).
- Paper §6.7 says "6/6 invariants fire on designated focus nodes" → [reports/negative-test-results.md](reports/negative-test-results.md).

Every numeric claim in the paper is traceable to a line in a report produced by one of the five scripts.

---

## Summary of the traceability guarantee

```
Paper claim
    ↓
Section of ONTOLOGY-REFERENCE.md (meaning)
    ↓
Specific class/property/axiom in TTL (definition)
    ↓
SHACL shape / SPARQL query / entailment check (validator)
    ↓
Report file in reports/ (evidence)
    ↓
Validator script in repository root (reproducibility)
```

No claim in the DAIMO paper should lack a step in this chain. If you find one that does, it's a documentation bug — please open an issue.
