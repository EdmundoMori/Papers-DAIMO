# DAIMO — Implementation

Companion to [`01-DAIMO-DESIGN.md`](01-DAIMO-DESIGN.md). This document describes
**how** the design is realised in Turtle: the module layout, the OWL 2 DL
constructs, the full class/property reference, the SHACL shapes (completeness,
conformance, and the six cross-class invariants), the example graph, the query
suite, and how to reproduce every check.

---

## 1. Modules, IRIs and namespaces

| Module | File | Ontology IRI | Contents |
|---|---|---|---|
| Core | `daimo/ontology/daimo-core.ttl` | `https://w3id.org/pionera/daimo` | 14 classes, 37 properties, disjointness, functional/asymmetric/inverse axioms |
| Alignment | `daimo/ontology/alignment.ttl` | `https://w3id.org/pionera/daimo/align` | `owl:imports` core; external term stubs + alignment axioms + SKOS mappings |
| Shapes | `daimo/shapes/daimo-shapes.ttl` | `https://w3id.org/pionera/daimo/shapes` | 9 completeness + 3 conformance shapes + 6 SHACL-SPARQL invariants |

All three carry `owl:versionInfo "0.1.6"` and versioned `owl:versionIRI`.

**Prefixes used across the modules:**

```turtle
daimo:  https://w3id.org/pionera/daimo#
dcat:   http://www.w3.org/ns/dcat#
dct:    http://purl.org/dc/terms/
it6:    http://data.europa.eu/it6/            # MLDCAT-AP 3.0.0
mls:    http://www.w3.org/ns/mls#
odrl:   http://www.w3.org/ns/odrl/2/
prov:   http://www.w3.org/ns/prov#
foaf:   http://xmlns.com/foaf/0.1/
dspace: https://w3id.org/dspace/v0.8/          # Dataspace Protocol
edc:    https://w3id.org/edc/v0.0.1/ns/        # EDC extensions
spdx:   http://spdx.org/rdf/terms#
skos:   http://www.w3.org/2004/02/skos/core#
sh:     http://www.w3.org/ns/shacl#
```

---

## 2. OWL 2 DL constructs used

- `owl:Class`, `rdfs:subClassOf` (single- and multi-parent).
- `owl:ObjectProperty`, `owl:DatatypeProperty`, `rdfs:domain`, `rdfs:range`.
- `owl:FunctionalProperty` (all datatype props + many object props).
- `owl:AsymmetricProperty` (distinctness constraints).
- `owl:inverseOf` (reverse-traversal convenience → entailed inverse-functional).
- `owl:AllDisjointClasses` (`daimo:TopLevelKindsDisjointness`).
- `rdfs:subPropertyOf` for property alignment.
- `skos:definition` / `skos:example` / `rdfs:comment` on every native term
  (documentation-rich, drives WIDOCO HTML).
- Header metadata: `dct:title/description/creator/contributor/publisher/license/
  issued/modified`, `owl:priorVersion`, `vann:preferredNamespacePrefix/Uri`,
  `dct:conformsTo <owl2-overview>`.

The profile is **OWL 2 DL** (`dct:conformsTo <https://www.w3.org/TR/owl2-overview/>`).

---

## 3. Class & property reference

### 3.1 Classes (14)

| Class | `rdfs:subClassOf` |
|---|---|
| `AIAssetOffering` | `dcat:CatalogRecord` |
| `ParticipantRole` | `prov:Role` (via alignment) |
| `ModelProvider` / `ModelConsumer` / `PlatformOperator` / `Evaluator` / `GovernanceActor` | `daimo:ParticipantRole` |
| `ModelDeployment` | `prov:Entity` |
| `IOContract` | — (stand-alone) |
| `ExecutionAuthorization` | `odrl:Agreement` |
| `DerivedArtifact` | `prov:Entity`, `dcat:Resource` |
| `CrossParticipantProvenanceRecord` | `prov:Bundle` |
| `AuditEvidence` | `prov:Entity` |
| `SharedEvaluationContext` | — (stand-alone) |

### 3.2 Object properties (29)

| Property | Domain → Range | Characteristics / alignment |
|---|---|---|
| `offersModel` | `AIAssetOffering` → `it6:MachineLearningModel` | Functional, Asymmetric; `⊑ foaf:primaryTopic` |
| `offeredBy` | `AIAssetOffering` → `foaf:Agent` | Functional; **NOT** `⊑ dct:publisher` |
| `hasOfferPolicy` | `AIAssetOffering` → `odrl:Offer` | Functional; `⊑ odrl:hasPolicy` |
| `hasOffering` | `it6:MachineLearningModel` → `AIAssetOffering` | inv. `offersModel`; `⊑ foaf:isPrimaryTopicOf` |
| `hasRole` | `foaf:Agent` → `ParticipantRole` | non-functional |
| `inParticipantContext` | `ParticipantRole` → `edc:ParticipantContext` | Functional |
| `deploysModel` | `ModelDeployment` → `it6:MachineLearningModel` | Functional, Asymmetric |
| `hasDeployment` | `it6:MachineLearningModel` → `ModelDeployment` | inv. `deploysModel` |
| `exposedAs` | `ModelDeployment` → `dcat:DataService` | non-functional (multi-endpoint) |
| `onInfrastructure` | `ModelDeployment` → `it6:ComputerInfrastructure` | Functional |
| `hasIOContract` | `ModelDeployment` → `IOContract` | non-functional (one per service) |
| `inputSchema` | `IOContract` → `dcat:Resource` | Functional (optional) |
| `outputSchema` | `IOContract` → `dcat:Resource` | Functional (optional) |
| `authorizesRun` | `ExecutionAuthorization` → `it6:Run` | Asymmetric, non-functional; **NOT** `⊑ prov:used` |
| `authorizedBy` | `it6:Run` → `ExecutionAuthorization` | Functional; inv. `authorizesRun` |
| `grantedTo` | `ExecutionAuthorization` → `foaf:Agent` | Functional; `⊑ odrl:assignee` |
| `derivedFromRun` | `DerivedArtifact` → `it6:Run` | Functional, Asymmetric; `⊑ prov:wasGeneratedBy` |
| `hasDerivedArtifact` | `it6:Run` → `DerivedArtifact` | inv. `derivedFromRun` |
| `underAuthorization` | `DerivedArtifact` → `ExecutionAuthorization` | Functional |
| `spansParticipantContext` | `CrossParticipantProvenanceRecord` → `edc:ParticipantContext` | non-functional (≥2 by SHACL) |
| `records` | `CrossParticipantProvenanceRecord` → `prov:Activity` | non-functional |
| `evidenceOf` | `AuditEvidence` → `prov:Activity` | Functional, Asymmetric; **NOT** `⊑ prov:hadActivity` |
| `hasAuditEvidence` | `prov:Activity` → `AuditEvidence` | inv. `evidenceOf` |
| `signedBy` | `AuditEvidence` → `foaf:Agent` | Functional |
| `integrityHash` | `AuditEvidence` → `spdx:Checksum` | Functional |
| `usesEvaluationContext` | `it6:Evaluation` → `SharedEvaluationContext` | Functional |
| `contextTask` | `SharedEvaluationContext` → `it6:Task` | Functional; `⊑ it6:hasTask` |
| `contextDataset` | `SharedEvaluationContext` → `dcat:Dataset` | Functional; **NOT** `⊑ it6:trainedOn` |
| `contextFlow` | `SharedEvaluationContext` → `it6:Flow` | Functional; **NOT** `⊑ it6:hasFlow` |

*(`integrityHash`, `inputSchema`, `outputSchema` are `owl:ObjectProperty`; the
other schema/format fields below are datatype properties.)*

### 3.3 Datatype properties (8, all functional)

| Property | Domain → Range | Notes |
|---|---|---|
| `inputFormat` | `IOContract` → `xsd:string` | IANA media type of input |
| `outputFormat` | `IOContract` → `xsd:string` | IANA media type of output |
| `authMethod` | `IOContract` → `xsd:string` | controlled vocabulary (see §4.2) |
| `recordedAt` | `AuditEvidence` → `xsd:dateTime` | evidence seal time |
| `expiresAt` | `ExecutionAuthorization` → `xsd:dateTime` | authorization expiry |
| `protocol` | `SharedEvaluationContext` → `xsd:string` | pattern-constrained (see §4.2) |
| `randomSeed` | `SharedEvaluationContext` → `xsd:integer` | reproducibility seed |
| `datasetVersion` | `SharedEvaluationContext` → `xsd:string` | literal version token; **NOT** `⊑ dct:hasVersion` |

---

## 4. SHACL shapes (`daimo/shapes/daimo-shapes.ttl`)

The shapes file enforces three kinds of constraint.

### 4.1 Completeness node shapes (9, one per DAIMO-native kind)

Minimum required properties (with cardinalities) per class:

- **`AIAssetOfferingShape`** — `offersModel` (1..1, `it6:MachineLearningModel`),
  `offeredBy` (1..1, `foaf:Agent`), `hasOfferPolicy` (1..1, `odrl:Offer`),
  `dct:title` (≥1).
- **`ParticipantRoleShape`** — held by ≥1 agent (inverse `hasRole`),
  `inParticipantContext` (1..1).
- **`ModelDeploymentShape`** — `deploysModel` (1..1), `exposedAs` (≥1
  `dcat:DataService`), `hasIOContract` (≥1), `onInfrastructure` (1..1).
- **`IOContractShape`** — `inputFormat`, `outputFormat`, `authMethod` (each
  1..1).
- **`ExecutionAuthorizationShape`** — `odrl:permission` (≥1),
  `authorizesRun` (≥1 `it6:Run`), `grantedTo` (1..1), `expiresAt` (1..1).
- **`DerivedArtifactShape`** — `derivedFromRun` (1..1), `underAuthorization`
  (1..1).
- **`SharedEvaluationContextShape`** — `contextTask` (1..1),
  `contextDataset` (1..1), `datasetVersion` (1..1), `protocol` (1..1,
  pattern), `randomSeed` (1..1).
- **`AuditEvidenceShape`** — `evidenceOf` (1..1), `integrityHash` (1..1
  `spdx:Checksum`) with `spdx:algorithm` (≥1) and `spdx:checksumValue` (≥1,
  minLength 32), `signedBy` (1..1), `recordedAt` (1..1).
- **`CrossParticipantProvenanceRecordShape`** — `records` (≥1 `prov:Activity`),
  `spansParticipantContext` (**≥2** participant contexts).

### 4.2 Controlled vocabularies inside shapes

- **`authMethod`** (`sh:in`): `none`, `api-key`, `basic`, `bearer`,
  `oauth2-bearer`, `oauth2-client-credentials`, `mtls`, `jwt`,
  `dataspace-token`.
- **`protocol`** (`sh:pattern`):
  `^(holdout|stratified-holdout|leave-one-out|temporal-split|\d+-fold-cv|stratified-\d+-fold-cv|bootstrap-\d+)$`.
- **`integrityHash` value** must be ≥ 32 hex characters (SHA-128-bit-or-stronger
  equivalent).

### 4.3 Conformance shapes for reused classes (3)

These enforce DAIMO-context obligations on **reused** classes:

- **`OfferInDAIMOShape`** (`odrl:Offer`) — must declare `odrl:assigner`, and
  `odrl:target` at Policy level **or** on each Permission (`sh:or`).
- **`MachineLearningModelInDAIMOShape`** (`it6:MachineLearningModel`) — must
  carry `odrl:hasPolicy` (≥1) plus `dct:title` and `dct:identifier`.
- **`RunInDAIMOShape`** (`it6:Run`) — must reference `it6:hasFlow`,
  `mls:realizes`, `prov:wasAssociatedWith`, and `prov:startedAtTime` (for
  reproducibility and auditability).

### 4.4 Cross-class invariants (6 SHACL-SPARQL rules, INV-1..INV-6)

These are the **governance business rules** that make DAIMO active rather than
passive. All share the prefix declaration `daimo:_invariantPrefixes`.

| ID | Target | Rule (violation condition) |
|---|---|---|
| **INV-1** | `DerivedArtifact` | its `underAuthorization` does **not** `authorizesRun` the run it `derivedFromRun` → broken authorization chain. |
| **INV-2** | `it6:Run` | the agent `prov:wasAssociatedWith` the run is **not** the `grantedTo` grantee of any authorization covering that run. |
| **INV-3** | `ModelDeployment` | an `exposedAs` service does **not** `it6:servesModel` the same model the deployment `deploysModel`. |
| **INV-4** | `ExecutionAuthorization` | `expiresAt` is **not strictly after** the `prov:startedAtTime` of a run it authorizes (run under expired agreement). |
| **INV-5** | `AIAssetOffering` | the `offersModel` model is **not** an `odrl:target` of the attached offer policy (Policy level or any Permission). |
| **INV-6** | `AIAssetOffering` | `offeredBy` ≠ the `odrl:assigner` of the attached policy → catalog record and ODRL offer attribute publication to different agents. |

Each invariant is validated **positively** (holds on the example graph) and
**negatively** (fires on the deliberately-broken graph) — see
[`03-DAIMO-EVALUATION.md`](03-DAIMO-EVALUATION.md) §5.

---

## 5. Example knowledge graph

`daimo/examples/flood-risk-scenario.ttl` is the running UPM / Leganés / INESData
scenario (≈ **225 data triples**). It instantiates every DAIMO class at least
once and is the graph over which SHACL conformance and the 23 CQ SPARQL queries
are checked. It is designed to be **fully SHACL-conformant** and to make all 23
CQs return ≥ 1 row after OWL-RL materialisation.

---

## 6. Query suite

`daimo/queries/queries.md` holds the **23 SPARQL** competency-question queries
(`CQ-R1..CQ-G4`). The runner (`validate.py`) extracts them, runs each over the
**OWL-RL-materialised closure** of `ontology + alignment + example`, and asserts
each returns ≥ 1 row. Some queries rely on entailment (e.g. `offersModel ⊑
foaf:primaryTopic`, `rdfs:subClassOf+`), which is why materialisation precedes
execution.

---

## 7. Reproducibility — how to run every check

```bash
cd daimo
python3 -m venv .venv
.venv/bin/pip install rdflib pyshacl owlrl owlready2

# four independent checks — each exits 0 on success
.venv/bin/python validate.py                 # SHACL + 23 CQ SPARQL (OWL-RL closure)
.venv/bin/python reasoner_check.py           # HermiT + OWL-RL + entailment verification
.venv/bin/python oops_check.py               # OOPS! pitfall scan (POSTs to oops.linkeddata.es)
.venv/bin/python tests/negative_test.py      # cross-class invariant negative tests
.venv/bin/python scalability_benchmark.py --sizes 100 1000
```

Outputs are written to `daimo/reports/` (`validation-results.md`,
`reasoner-report.md`, `oops-report.md`, `negative-test-results.md`,
`scalability-benchmark.md`). `oops_check.py` requires network access to
`oops.linkeddata.es`.

**Toolchain:** Python 3 with `rdflib`, `pyshacl`, `owlrl`, `owlready2` (HermiT
ships with owlready2). Ontology authoring in Turtle; HTML docs generated with
**WIDOCO** into `daimo/docs/` (served via GitHub Pages).
