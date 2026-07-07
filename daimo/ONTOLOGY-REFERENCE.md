# DAIMO Ontology Reference

Version: **0.1.6**
Date: 2026-07-07
Namespace: `https://w3id.org/pionera/daimo#`
Licence: CC-BY 4.0

This document is the **authoritative human-readable reference** for every
class, property, axiom, and SHACL shape in DAIMO. It is kept in sync with
the TTL sources in [ontology/](ontology/) and [shapes/](shapes/). Read this
instead of the TTLs when you need to understand what something *means*.

Every class and property section has the same structure:

- **IRI** — the canonical identifier.
- **Kind** — class / object property / datatype property / axiom.
- **Parents** — `rdfs:subClassOf` / `rdfs:subPropertyOf` targets (with
  rationale for each reuse, and any deliberate non-alignments noted).
- **Domain / Range** — for properties.
- **Characteristics** — functional, inverse, etc.
- **OntoClean tags** — rigidity / identity / unity / dependency
  (where relevant).
- **Identity criteria** — what makes two instances `owl:sameAs` (for
  classes where this matters).
- **Role in DAIMO** — why this term exists and what gap it fills.
- **Enforced by SHACL** — which shape(s) constrain it.
- **Used in example KG** — concrete instance from the flood-risk scenario.
- **Answers CQ(s)** — which competency questions traverse this term.
- **Deliberate design choices** — non-obvious decisions documented so
  reviewers see the reasoning, not only the axiom.

---

## Table of contents

1. [Namespace reuse summary](#1-namespace-reuse-summary)
2. [DAIMO-native classes](#2-daimo-native-classes)
3. [DAIMO-native object properties](#3-daimo-native-object-properties)
4. [DAIMO-native datatype properties](#4-daimo-native-datatype-properties)
5. [Global axioms (disjointness, etc.)](#5-global-axioms)
6. [Alignment axioms (external vocabularies)](#6-alignment-axioms)
7. [SHACL node shapes](#7-shacl-node-shapes)
8. [SHACL-SPARQL cross-class invariants](#8-shacl-sparql-invariants)
9. [CQ → element traversal map](#9-cq--element-traversal-map)
10. [Example KG instance map](#10-example-kg-instance-map)

---

## 1. Namespace reuse summary

| Prefix | IRI | Role in DAIMO |
|---|---|---|
| `daimo:` | `https://w3id.org/pionera/daimo#` | DAIMO-native terms — 14 classes (9 top-level + 5 `ParticipantRole` subclasses), **29 object properties** (25 primary + 4 inverse), **8 datatype properties** |
| `dcat:` | `http://www.w3.org/ns/dcat#` | Catalog, CatalogRecord, Dataset, DataService, Distribution, Resource, endpointURL |
| `dct:` | `http://purl.org/dc/terms/` | title, creator, publisher, issued, modified, licence, hasVersion, identifier, description |
| `it6:` | `http://data.europa.eu/it6/` | MLDCAT-AP 3.0.0 — MachineLearningModel, Task, Run, Flow, Evaluation, ComputerInfrastructure, etc. |
| `mls:` | `http://www.w3.org/ns/mls#` | ML-Schema — Algorithm, realizes |
| `odrl:` | `http://www.w3.org/ns/odrl/2/` | Offer, Agreement, Permission, Prohibition, hasPolicy, target, assigner, assignee |
| `prov:` | `http://www.w3.org/ns/prov#` | Activity, Entity, Agent, Bundle, Role, wasGeneratedBy, wasAssociatedWith, used |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | Agent, Organization, primaryTopic, name |
| `dspace:` | `https://w3id.org/dspace/v0.8/` | Dataspace Protocol (DSP) — informative `skos:related` / `skos:closeMatch` mappings only |
| `edc:` | `https://w3id.org/edc/v0.0.1/ns/` | EDC-specific extensions not in DSP. Only `edc:ParticipantContext` is referenced. |
| `spdx:` | `http://spdx.org/rdf/terms#` | Checksum, algorithm, checksumValue — for audit-evidence integrity |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | related, closeMatch, exactMatch (informative mappings) |

---

## 2. DAIMO-native classes

Nine top-level classes plus five ParticipantRole subclasses, total **fourteen DAIMO-native classes**.

> **Documentation vs. axioms.** Each class entry below includes
> `OntoClean` tags (`+R`/`-R`, `+I`/`-I`, etc.) and `Identity criteria`
> sentences. These are **modelling guidance**, NOT OWL axioms: the TTL
> contains no OntoClean-meta-property vocabulary, no `owl:hasKey`, and
> no `owl:sameAs` assertions encoding these criteria. They describe the
> *intended* identity and rigidity semantics for reviewers and
> modellers; a reasoner will not enforce them. Alignment axioms marked
> with `(alignment.ttl)` live in the alignment module and are visible
> only when that file is loaded alongside `daimo-core.ttl`.

---

### 2.1 `daimo:AIAssetOffering`

- **IRI**: `https://w3id.org/pionera/daimo#AIAssetOffering`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf dcat:CatalogRecord` (declared in both `daimo-core.ttl` and `alignment.ttl`)
- **OntoClean**: `+R` (rigid — if you are an Offering you cannot cease being one without ceasing to exist), `+I` (identity by (offered model, offering agent, policy)), `+U` (a single offering is one atomic registration).
- **Identity criteria**: two AIAssetOffering instances are `owl:sameAs` iff they reference the same model (`daimo:offersModel`), the same provider (`daimo:offeredBy`), and the same policy (`daimo:hasOfferPolicy`) — and the same catalog record issuance (`dct:issued`).
- **Role**: the reified act of publishing an AI model into a dataspace catalog as a governed offer. It bundles three concerns (model, provider, policy) into one record so discovery can filter on any of them.
- **Enforced by SHACL**: [AIAssetOfferingShape](#711-aiassetofferingshape) requires `daimo:offersModel` (1..1), `daimo:offeredBy` (1..1), `daimo:hasOfferPolicy` (1..1), `dct:title` (1..*).
- **Used in example KG**: `ex:offering-flood-v2`, `ex:offering-flood-v1`, `ex:offering-flood-v2-ro` — three offerings in `ex:upm-catalog`.
- **Answers CQs**: CQ-R1, CQ-R2, CQ-R5, CQ-G1.
- **Deliberate design choices**:
  - **Specialises `dcat:CatalogRecord`**, not `odrl:Offer`. DCAT's CatalogRecord carries registration metadata (`dct:issued`, `foaf:primaryTopic`); the ODRL Offer is the policy attached via `daimo:hasOfferPolicy`. They are two distinct resources linked, not conflated.
  - **`daimo:offeredBy` is NOT a subproperty of `dct:publisher`**. On a CatalogRecord, `dct:publisher` is the catalog maintainer (e.g., INESData), not the model author (e.g., UPM). Conflating them would give wrong attribution.
  - **`daimo:offersModel` IS a subproperty of `foaf:primaryTopic`**. This is the standard DCAT convention for CatalogRecord → described resource.

---

### 2.2 `daimo:ParticipantRole` + subclasses

- **IRI**: `https://w3id.org/pionera/daimo#ParticipantRole`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf prov:Role` — **declared only in `alignment.ttl`**; consumers loading only `daimo-core.ttl` will not see this parent.
- **OntoClean**: `-R` (anti-rigid — an agent can gain and lose roles), `-I` (no identity criteria on the role instance; identity comes from the holding agent + context), `-U`, `+D` (role instances depend on an agent to play them).
- **Role**: a dataspace-scoped role that a participant takes with respect to AI assets. Enables queries like "which agents are Model Providers in this context?" without overloading `foaf:Agent` with subclasses.
- **Subclasses**: `daimo:ModelProvider`, `daimo:ModelConsumer`, `daimo:PlatformOperator`, `daimo:Evaluator`, `daimo:GovernanceActor`.
- **Subclasses are intentionally NOT mutually disjoint.** One agent can hold several roles simultaneously (e.g., a research group is both Evaluator and Model Provider).
- **Enforced by SHACL**: [ParticipantRoleShape](#712-participantroleshape) requires at least one holding agent (via `daimo:hasRole` inverse path) and exactly one `daimo:inParticipantContext`.
- **Used in example KG**: `ex:upm-provider-role a daimo:ModelProvider`, `ex:municipality-consumer-role a daimo:ModelConsumer`, and three more.
- **Answers CQs**: CQ-R5.
- **Deliberate design choices**:
  - **Stretched alignment to `prov:Role`**. PROV-O's Role is activity-scoped; DAIMO's is dataspace-scoped. Acceptable but not ideal — a reviewer might ask to downgrade to `skos:related`.
  - **Role instance IS typed as the role class** (`ex:upm-provider-role a daimo:ModelProvider`). Strict OntoClean would separate role-type from role-assignment; current pragmatic modelling conflates them.
  - **Role is not scoped to a specific asset**. An agent is a ModelProvider in a context, not per-offering. This is a known coarse-graining (see `daimo-design-rationale.md` §M-NEW-3).

---

### 2.3 `daimo:ModelDeployment`

- **IRI**: `https://w3id.org/pionera/daimo#ModelDeployment`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf prov:Entity` (declared in both `daimo-core.ttl` and `alignment.ttl`)
- **OntoClean**: `+R`, `+I` (identity by deployed model + infrastructure instance + service endpoint set), `+U`.
- **Role**: a running / hosted instance of an `it6:MachineLearningModel`, exposed through one or more `dcat:DataService`s over a named `it6:ComputerInfrastructure`, governed by a `daimo:IOContract` per service.
- **Enforced by SHACL**: [ModelDeploymentShape](#713-modeldeploymentshape) requires `daimo:deploysModel` (1..1), `daimo:exposedAs` (1..*, non-functional for multi-endpoint support), `daimo:hasIOContract` (1..*), `daimo:onInfrastructure` (1..1).
- **Used in example KG**: `ex:deployment-flood-v2`, deployed on `ex:upm-gpu-cluster`, exposed as `ex:flood-risk-service`, with contract `ex:flood-risk-iocontract`.
- **Answers CQs**: CQ-E1, CQ-E2, CQ-E3, CQ-G2.
- **Deliberate design choices**:
  - **Subclass of `prov:Entity`** rather than `prov:Activity`. A deployment is both the *instance* (an entity with identity) and a *process* (serving requests). The Entity view enables identification; the Activity view is not modelled. Trade-off acknowledged.
  - **`daimo:exposedAs` and `daimo:hasIOContract` are non-functional** so multi-endpoint deployments (REST + gRPC) can be expressed with one deployment instance.
  - **Runtime enforcement is out of core scope**. `ModelDeployment` records where a model is invocable and how it is exposed, but it does not prescribe connector runtime, container orchestration, neutral-node placement, or TEE implementation. Those details can be attached to `it6:ComputerInfrastructure`, `dcat:DataService`, ODRL duties, or deployment-specific profiles.

---

### 2.4 `daimo:IOContract`

- **IRI**: `https://w3id.org/pionera/daimo#IOContract`
- **Kind**: `owl:Class`
- **Parents**: *(no external alignment — stand-alone)*
- **OntoClean**: `+R`, `+I` (identity by (inputFormat, outputFormat, authMethod)), `-U`.
- **Role**: the minimum machine-actionable invocation contract: input media type, output media type, authentication method, optional input/output schemas. Enables a consumer to determine whether its client can invoke the deployment without round-tripping through out-of-band documentation.
- **Enforced by SHACL**: [IOContractShape](#714-iocontractshape) requires `daimo:inputFormat` (1..1), `daimo:outputFormat` (1..1), `daimo:authMethod` (1..1).
- **Used in example KG**: `ex:flood-risk-iocontract` with JSON in, GeoJSON out, OAuth2.
- **Answers CQs**: CQ-R4, CQ-D3, CQ-E1, CQ-G2.
- **Deliberate design choices**:
  - **No external alignment**. No reused vocabulary covers "machine-actionable invocation contract". OpenAPI/JSON-Schema are out-of-band; DCAT's `endpointURL` is too shallow. Stand-alone class is justified.
  - **Intentionally shallow**. `IOContract` records media formats, authentication, and optional schema links; it does not validate semantic data alignment, units of measurement, sector-specific datatypes, or output semantics by itself. Those constraints belong in `IOContract`-based profiles or dataspace-specific SHACL shapes.

---

### 2.5 `daimo:ExecutionAuthorization`

- **IRI**: `https://w3id.org/pionera/daimo#ExecutionAuthorization`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf odrl:Agreement` (declared in both `daimo-core.ttl` and `alignment.ttl`)
- **OntoClean**: `+R`, `+I` (identity by (assigner, assignee, target, expiresAt, permission set)), `+U`.
- **Role**: an ODRL agreement produced by a DSP contract negotiation that authorises a specific agent (the grantee) to invoke specific `it6:Run`s. Bridges the ODRL agreement model with DAIMO's run-level governance.
- **Enforced by SHACL**: [ExecutionAuthorizationShape](#715-executionauthorizationshape) requires at least one `odrl:permission`, at least one `daimo:authorizesRun`, exactly one `daimo:grantedTo`, and exactly one `daimo:expiresAt`.
- **Used in example KG**: `ex:agreement-municipality-flood-v2` grants `ex:municipality` permission to `odrl:use` `ex:flood-risk-v2`, authorising `ex:run-2026-04-20-legs`, expiring 2027-04-20.
- **Answers CQs**: CQ-E2, CQ-E4, CQ-E5, CQ-G3.
- **Deliberate design choices**:
  - **Specialises `odrl:Agreement`**. The SHACL shape enforces at least one `odrl:permission` so the class is ODRL-conformant (a policy without rules is structurally invalid).

---

### 2.6 `daimo:DerivedArtifact`

- **IRI**: `https://w3id.org/pionera/daimo#DerivedArtifact`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf prov:Entity , dcat:Resource` (declared in both `daimo-core.ttl` and `alignment.ttl`)
- **OntoClean**: `+R`, `+I` (identity by (derivedFromRun, underAuthorization, content-hash)), `+U`.
- **Role**: a governed, catalog-describable output produced by an `it6:Run` in a dataspace context (e.g., the flood-risk prediction for district 5). Distinct from `it6:OutputFilePrediction` because it carries its own policy and authorisation pointer, making it a dataspace-first-class resource.
- **Enforced by SHACL**: [DerivedArtifactShape](#716-derivedartifactshape) requires exactly one `daimo:derivedFromRun` and exactly one `daimo:underAuthorization`.
- **Also enforced by SHACL-SPARQL**: [INV-1](#81-inv-1-derivation-authorization-consistency) — the `underAuthorization` must authorise the run that `derivedFromRun` points to.
- **Used in example KG**: `ex:prediction-legs-2026-04-20`, the flood-risk prediction for Leganés on 2026-04-20.
- **Answers CQs**: CQ-E5, CQ-G4.
- **Deliberate design choices**:
  - **Multiple inheritance** (`prov:Entity` and `dcat:Resource`). Both are rigid, compatible. Enables PROV-based provenance queries *and* DCAT-based catalog publication of the derived artefact.

---

### 2.7 `daimo:CrossParticipantProvenanceRecord`

- **IRI**: `https://w3id.org/pionera/daimo#CrossParticipantProvenanceRecord`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf prov:Bundle` (declared in both `daimo-core.ttl` and `alignment.ttl`)
- **OntoClean**: `+R`, `+I`, `-U` (aggregate).
- **Role**: aggregates `prov:Activity` and `prov:Entity` instances across multiple `edc:ParticipantContext`s into one audit-ready bundle. Enables answers to "give me the full provenance chain for this artefact spanning all participants involved".
- **Enforced by SHACL**: [CrossParticipantProvenanceRecordShape](#717-crossparticipantprovenancerecordshape) requires at least one `daimo:records` and **at least two** `daimo:spansParticipantContext` (a record spanning only one context wouldn't be cross-participant).
- **Used in example KG**: `ex:bundle-flood-legs` spans three contexts (UPM, Leganés, INESData) and records the run and evaluation.
- **Answers CQs**: CQ-G4.

---

### 2.8 `daimo:AuditEvidence`

- **IRI**: `https://w3id.org/pionera/daimo#AuditEvidence`
- **Kind**: `owl:Class`
- **Parents**: `rdfs:subClassOf prov:Entity` (declared in both `daimo-core.ttl` and `alignment.ttl`)
- **OntoClean**: `+R`, `+I` (identity by (evidenceOf, signedBy, recordedAt, checksum)), `+U`.
- **Role**: a compliance-oriented evidence record attached to a governed event, carrying a structured `spdx:Checksum` (algorithm + digest), signer, and timestamp. Enables "prove X happened and is unchanged" queries.
- **Enforced by SHACL**: [AuditEvidenceShape](#718-auditevidenceshape) requires exactly one each of: `daimo:evidenceOf`, `daimo:integrityHash` (range `spdx:Checksum`), `daimo:signedBy`, `daimo:recordedAt`. Additional property paths enforce that the Checksum has both `spdx:algorithm` and a `spdx:checksumValue` of ≥32 hex chars.
- **Used in example KG**: `ex:audit-run-legs` attests `ex:run-2026-04-20-legs`, signed by `ex:inesdata-op`, with a SHA-256 Checksum.
- **Answers CQs**: CQ-E4.
- **Deliberate design choices**:
  - **`daimo:integrityHash` points to `spdx:Checksum`**, not an `xsd:string`. A digest without its algorithm is unverifiable. The SHACL shape enforces both fields of the checksum.

---

### 2.9 `daimo:SharedEvaluationContext`

- **IRI**: `https://w3id.org/pionera/daimo#SharedEvaluationContext`
- **Kind**: `owl:Class`
- **Parents**: *(no external alignment — stand-alone)*
- **OntoClean**: `+R`, `+I` (identity by (task, dataset, datasetVersion, protocol, randomSeed)), `+U`.
- **Role**: a reified grouping of the conditions under which evaluations are comparable. Without this reification, a metric value like `accuracy = 0.89` is meaningless in isolation.
- **Enforced by SHACL**: [SharedEvaluationContextShape](#719-sharedevaluationcontextshape) requires exactly one each of: `daimo:contextTask`, `daimo:contextDataset`, `daimo:datasetVersion`, `daimo:protocol`, `daimo:randomSeed`. `daimo:contextFlow` is optional.
- **Used in example KG**: `ex:evalctx-climatebench-v1-2026-1-holdout` fixes the shared context: `ex:flood-risk-task`, `ex:climatebench-v1`, version `2026.1`, protocol `holdout`, seed `42`.
- **Answers CQs**: CQ-V1, CQ-V2, CQ-V3, CQ-V5.
- **Deliberate design choices**:
  - **No external alignment**. MLDCAT-AP has `it6:Task`, `it6:EstimationProcedure`, `it6:Split`, but no single reified grouping. `SharedEvaluationContext` is a genuine DAIMO-native primitive.
  - **Intentionally does not cover every facet** of comparability. Metric definitions, units, calculation procedures, split strategy, hyperparameter settings, and hardware can also affect comparability; the current set is the minimum required by CQ-V1..CQ-V3. Metric or protocol profiles should carry stricter mathematical definitions when a dataspace requires them.

---

## 3. DAIMO-native object properties

**29 object properties** in total (25 primary + 4 inverse properties
added in v0.1.4). The `Func?` column reflects the
`owl:FunctionalProperty` declaration in the TTL; blank cells are
non-functional.

| Property | Domain | Range | Func? | SubPropertyOf | Notes |
|---|---|---|:-:|---|---|
| `daimo:offersModel` | AIAssetOffering | it6:MachineLearningModel | ✓ | foaf:primaryTopic | |
| `daimo:offeredBy` | AIAssetOffering | foaf:Agent | ✓ | *(none)* | Deliberately NOT subproperty of dct:publisher (see class §2.1). |
| `daimo:hasOfferPolicy` | AIAssetOffering | odrl:Offer | ✓ | odrl:hasPolicy | |
| `daimo:hasRole` | foaf:Agent | daimo:ParticipantRole | | | Non-functional: one agent may hold multiple roles. |
| `daimo:inParticipantContext` | daimo:ParticipantRole | edc:ParticipantContext | ✓ | | |
| `daimo:deploysModel` | daimo:ModelDeployment | it6:MachineLearningModel | ✓ | | |
| `daimo:exposedAs` | daimo:ModelDeployment | dcat:DataService | | | Non-functional: multi-endpoint (REST + gRPC). |
| `daimo:onInfrastructure` | daimo:ModelDeployment | it6:ComputerInfrastructure | ✓ | | |
| `daimo:hasIOContract` | daimo:ModelDeployment | daimo:IOContract | | | Non-functional: one per exposed service. |
| `daimo:authorizesRun` | daimo:ExecutionAuthorization | it6:Run | | | Non-functional: subscription-style agreements cover many runs. |
| `daimo:authorizedBy` | it6:Run | daimo:ExecutionAuthorization | ✓ | | `owl:inverseOf authorizesRun` |
| `daimo:grantedTo` | daimo:ExecutionAuthorization | foaf:Agent | ✓ | odrl:assignee | |
| `daimo:derivedFromRun` | daimo:DerivedArtifact | it6:Run | ✓ | prov:wasGeneratedBy | |
| `daimo:underAuthorization` | daimo:DerivedArtifact | daimo:ExecutionAuthorization | ✓ | | |
| `daimo:spansParticipantContext` | daimo:CrossParticipantProvenanceRecord | edc:ParticipantContext | | | Non-functional: bundle spans ≥2 contexts (SHACL-enforced). |
| `daimo:records` | daimo:CrossParticipantProvenanceRecord | prov:Activity | | | Non-functional: a bundle records many activities. |
| `daimo:evidenceOf` | daimo:AuditEvidence | prov:Activity | ✓ | | Deliberately NOT subproperty of prov:hadActivity. |
| `daimo:signedBy` | daimo:AuditEvidence | foaf:Agent | ✓ | | |
| `daimo:integrityHash` | daimo:AuditEvidence | spdx:Checksum | ✓ | | ObjectProperty — points to structured Checksum, not xsd:string. |
| `daimo:usesEvaluationContext` | it6:Evaluation | daimo:SharedEvaluationContext | ✓ | | |
| `daimo:contextTask` | daimo:SharedEvaluationContext | it6:Task | ✓ | it6:hasTask | |
| `daimo:contextDataset` | daimo:SharedEvaluationContext | dcat:Dataset | ✓ | *(none)* | Deliberately NOT subproperty of it6:trainedOn. |
| `daimo:contextFlow` | daimo:SharedEvaluationContext | it6:Flow | ✓ | *(none)* | Deliberately NOT subproperty of it6:hasFlow. |
| `daimo:inputSchema` | daimo:IOContract | dcat:Resource | ✓ | | Optional link to input payload schema (JSON Schema, SHACL). |
| `daimo:outputSchema` | daimo:IOContract | dcat:Resource | ✓ | | Optional link to output payload schema. |
| `daimo:hasDeployment` | it6:MachineLearningModel | daimo:ModelDeployment | | | `owl:inverseOf daimo:deploysModel`. Added v0.1.4. |
| `daimo:hasDerivedArtifact` | it6:Run | daimo:DerivedArtifact | | | `owl:inverseOf daimo:derivedFromRun`. Added v0.1.4. |
| `daimo:hasAuditEvidence` | prov:Activity | daimo:AuditEvidence | | | `owl:inverseOf daimo:evidenceOf`. Added v0.1.4. |
| `daimo:hasOffering` | it6:MachineLearningModel | daimo:AIAssetOffering | | | `owl:inverseOf daimo:offersModel`. Added v0.1.4. |

### Documented non-alignments

- **`daimo:offeredBy` ⊄ `dct:publisher`** — on a `dcat:CatalogRecord`, `dct:publisher` denotes the catalog or record maintainer, not necessarily the model provider.
- **`daimo:authorizesRun` ⊄ `prov:used`** — `prov:used` has domain `prov:Activity`, which would wrongly type ExecutionAuthorization (an `odrl:Agreement`, i.e., Entity) as an Activity.
- **`daimo:evidenceOf` ⊄ `prov:hadActivity`** — `prov:hadActivity` is used on reified influence objects, not on Entities. AuditEvidence is an Entity *about* an Activity; PROV has no direct property for this.
- **`daimo:grantedTo` ⊄ `prov:qualifiedAssociation`** — `qualifiedAssociation` ranges over a reified Association object, not the agent. Correct alignment is `odrl:assignee` only.
- **`daimo:contextDataset` ⊄ `it6:hasDataset`**, **`daimo:contextFlow` ⊄ `it6:hasFlow`**, and **`daimo:datasetVersion`** has no external subproperty — the evaluation context fixes comparison conditions, not the internal structure of an MLDCAT-AP flow.

The PROV-oriented candidates were removed after the entailment-verification check detected silent class pollution in v0.1.0. The remaining non-alignments are documented to avoid attribution errors and over-committing DAIMO's evaluation context to implementation-specific ML workflow semantics.

---

## 4. DAIMO-native datatype properties

**8 datatype properties** in total. All declared `owl:FunctionalProperty`.
(`daimo:inputSchema` and `daimo:outputSchema` are declared as
`owl:ObjectProperty` with range `dcat:Resource`; they appear in §3 above.)

| Property | Domain | Range | SubPropertyOf | Comment |
|---|---|---|---|---|
| `daimo:inputFormat` | daimo:IOContract | xsd:string | | IANA media type of input payload. |
| `daimo:outputFormat` | daimo:IOContract | xsd:string | | IANA media type of output payload. |
| `daimo:authMethod` | daimo:IOContract | xsd:string | | Auth-method token: `oauth2-bearer`, `api-key`, `mtls`. |
| `daimo:recordedAt` | daimo:AuditEvidence | xsd:dateTime | | When the evidence was sealed. |
| `daimo:expiresAt` | daimo:ExecutionAuthorization | xsd:dateTime | | Expiry timestamp. Compared to run `prov:startedAtTime` by INV-4. |
| `daimo:protocol` | daimo:SharedEvaluationContext | xsd:string | | Protocol name: `holdout`, `5-fold-cv`, `bootstrap-1000`. |
| `daimo:randomSeed` | daimo:SharedEvaluationContext | xsd:integer | | Seed value. |
| `daimo:datasetVersion` | daimo:SharedEvaluationContext | xsd:string | *(none)* | Literal version identifier of the evaluation dataset. Not aligned to `dct:hasVersion`, which links resources rather than literal version tokens. |

---

## 5. Global axioms

### 5.1 `owl:AllDisjointClasses` over top-level DAIMO kinds

Asserted: `AIAssetOffering`, `ParticipantRole`, `ModelDeployment`, `IOContract`, `ExecutionAuthorization`, `DerivedArtifact`, `AuditEvidence`, `SharedEvaluationContext`, `CrossParticipantProvenanceRecord` are pairwise disjoint.

Excluded from disjointness: the five `ParticipantRole` subclasses among themselves (so one agent can hold multiple roles in the same context).

### 5.2 One inverse-property pair

`daimo:authorizedBy owl:inverseOf daimo:authorizesRun`. `authorizedBy` is functional; `authorizesRun` is non-functional. Together they model: *one run has exactly one authorising agreement, but one agreement can authorise many runs*.

### 5.3 Functional property declarations

**27 DAIMO properties** are declared `owl:FunctionalProperty`: **19 object
properties** (see §3 — every row with ✓ in the Func? column, plus
`inputSchema` and `outputSchema`) and **all 8 datatype properties** (§4).

**Six DAIMO object properties are deliberately non-functional** (each
with an `rdfs:comment` in the TTL stating the rationale):

- `daimo:hasRole` — one agent may hold multiple participant roles.
- `daimo:exposedAs` — a deployment may expose multiple endpoints (REST + gRPC, multi-region).
- `daimo:hasIOContract` — typically one per exposed service.
- `daimo:authorizesRun` — subscription-style agreements authorise many runs.
- `daimo:spansParticipantContext` — a cross-participant bundle by definition spans ≥2 contexts (enforced by SHACL `sh:minCount 2`).
- `daimo:records` — a bundle records many activities.

---

## 6. Alignment axioms

Stored in [ontology/alignment.ttl](ontology/alignment.ttl).

### 6.1 Class-level `rdfs:subClassOf`

```
daimo:AIAssetOffering                   rdfs:subClassOf dcat:CatalogRecord .
daimo:ExecutionAuthorization            rdfs:subClassOf odrl:Agreement .
daimo:ModelDeployment                   rdfs:subClassOf prov:Entity .
daimo:DerivedArtifact                   rdfs:subClassOf prov:Entity , dcat:Resource .
daimo:CrossParticipantProvenanceRecord  rdfs:subClassOf prov:Bundle .
daimo:AuditEvidence                     rdfs:subClassOf prov:Entity .
daimo:ParticipantRole                   rdfs:subClassOf prov:Role .
```

### 6.2 Property-level `rdfs:subPropertyOf`

```
daimo:offersModel     rdfs:subPropertyOf foaf:primaryTopic .
daimo:hasOfferPolicy  rdfs:subPropertyOf odrl:hasPolicy .
daimo:grantedTo       rdfs:subPropertyOf odrl:assignee .
daimo:derivedFromRun  rdfs:subPropertyOf prov:wasGeneratedBy .
daimo:contextTask     rdfs:subPropertyOf it6:hasTask .
```

`daimo:hasOffering rdfs:subPropertyOf foaf:isPrimaryTopicOf` is declared in
`daimo-core.ttl`, not in `alignment.ttl`, because it is the inverse-side
accessor for `daimo:offersModel`. Therefore `alignment.ttl` contains five
property-level alignments, while the combined source modules contain six
DAIMO-subject `rdfs:subPropertyOf` declarations to external vocabularies.

### 6.3 Informative `skos:related` / `skos:closeMatch` mappings

```
daimo:AIAssetOffering                    skos:related     dspace:ContractOffer .
daimo:ExecutionAuthorization             skos:related     dspace:ContractNegotiation .
daimo:CrossParticipantProvenanceRecord   skos:related     dspace:TransferProcess .
daimo:ModelDeployment                    skos:related     it6:MachineLearningModel .
daimo:SharedEvaluationContext            skos:related     it6:Task , it6:EstimationProcedure .
daimo:inParticipantContext               skos:related     edc:ParticipantContext .
daimo:spansParticipantContext            skos:related     edc:ParticipantContext .
```

---

## 7. SHACL node shapes

Stored in [shapes/daimo-shapes.ttl](shapes/daimo-shapes.ttl). Each shape enforces minimum completeness for its target class.

### 7.1 Per-class completeness shapes

#### 7.1.1 `daimo:AIAssetOfferingShape`
- Target: `daimo:AIAssetOffering`
- Requires: `daimo:offersModel` (1..1, class `it6:MachineLearningModel`), `daimo:offeredBy` (1..1, class `foaf:Agent`), `daimo:hasOfferPolicy` (1..1, class `odrl:Offer`), `dct:title` (1..*).

#### 7.1.2 `daimo:ParticipantRoleShape`
- Target: `daimo:ParticipantRole`
- Requires: at least one inverse `daimo:hasRole` (some agent must hold the role), `daimo:inParticipantContext` (1..1).

#### 7.1.3 `daimo:ModelDeploymentShape`
- Target: `daimo:ModelDeployment`
- Requires: `daimo:deploysModel` (1..1), `daimo:exposedAs` (1..*, non-functional), `daimo:hasIOContract` (1..*, non-functional), `daimo:onInfrastructure` (1..1).

#### 7.1.4 `daimo:IOContractShape`
- Target: `daimo:IOContract`
- Requires: `daimo:inputFormat` (1..1), `daimo:outputFormat` (1..1), `daimo:authMethod` (1..1).

#### 7.1.5 `daimo:ExecutionAuthorizationShape`
- Target: `daimo:ExecutionAuthorization`
- Requires: `odrl:permission` (1..*), `daimo:authorizesRun` (1..*), `daimo:grantedTo` (1..1), `daimo:expiresAt` (1..1).

#### 7.1.6 `daimo:DerivedArtifactShape`
- Target: `daimo:DerivedArtifact`
- Requires: `daimo:derivedFromRun` (1..1), `daimo:underAuthorization` (1..1).

#### 7.1.7 `daimo:CrossParticipantProvenanceRecordShape`
- Target: `daimo:CrossParticipantProvenanceRecord`
- Requires: `daimo:records` (1..*, class `prov:Activity`), `daimo:spansParticipantContext` (**≥2**, class `edc:ParticipantContext`).

#### 7.1.8 `daimo:AuditEvidenceShape`
- Target: `daimo:AuditEvidence`
- Requires: `daimo:evidenceOf` (1..1, class `prov:Activity`), `daimo:integrityHash` (1..1, class `spdx:Checksum`), `daimo:signedBy` (1..1), `daimo:recordedAt` (1..1).
- Plus property paths: `(daimo:integrityHash / spdx:algorithm)` ≥1, `(daimo:integrityHash / spdx:checksumValue)` ≥1 and min-length 32 hex characters.

#### 7.1.9 `daimo:SharedEvaluationContextShape`
- Target: `daimo:SharedEvaluationContext`
- Requires: `daimo:contextTask` (1..1), `daimo:contextDataset` (1..1), `daimo:datasetVersion` (1..1), `daimo:protocol` (1..1), `daimo:randomSeed` (1..1).

### 7.2 Conformance shapes over reused classes

DAIMO asserts two additional shapes over classes it does not own. These transform DAIMO from a pure vocabulary into a *profile*: they specify which existing properties of reused classes are mandatory when those classes are used within a DAIMO graph.

#### 7.2.1 `daimo:OfferInDAIMOShape` (new in v0.1.2)
- Target: `odrl:Offer`
- Requires: `odrl:assigner` (1..*); and `odrl:target` at either Policy level OR on each Permission (via `sh:or`).
- Enforces ODRL-2.2 validity: every offer must identify the asset it licenses and the party issuing it.

#### 7.2.2 `daimo:MachineLearningModelInDAIMOShape`
- Target: `it6:MachineLearningModel`
- Requires: `odrl:hasPolicy` (1..*), `dct:title` (1..*), `dct:identifier` (1..*).

#### 7.2.3 `daimo:RunInDAIMOShape`
- Target: `it6:Run`
- Requires: `it6:hasFlow` (1..*), `mls:realizes` (1..*), `prov:wasAssociatedWith` (1..*), `prov:startedAtTime` (1..*, datatype xsd:dateTime).

---

## 8. SHACL-SPARQL invariants

**Six** cross-class business-rule invariants, implemented as `sh:SPARQLConstraint`.

### 8.1 INV-1: Derivation-authorization consistency
- Target: `daimo:DerivedArtifact`.
- Rule: `underAuthorization` must authorise the run `derivedFromRun` points to.
- Violates when a governed output exists under an agreement that does not cover its generating run.

### 8.2 INV-2: Run-agent matches authorization grantee
- Target: `it6:Run`.
- Rule: the `prov:wasAssociatedWith` agent must match the `daimo:grantedTo` of at least one authorising agreement.
- Violates when a run is executed by an agent other than the agreement's grantee.

### 8.3 INV-3: Deployment-service model consistency
- Target: `daimo:ModelDeployment`.
- Rule: the service in `daimo:exposedAs` must `it6:servesModel` the same model as `daimo:deploysModel`.
- Violates when a deployment's service advertises a different model than the deployment runs.

### 8.4 INV-4: Authorization temporal consistency
- Target: `daimo:ExecutionAuthorization`.
- Rule: `daimo:expiresAt` must be strictly later than every `prov:startedAtTime` of authorised runs.
- Violates when a run started after its authorising agreement expired.

### 8.5 INV-5: Offering-policy target consistency
- Target: `daimo:AIAssetOffering`.
- Rule: the offering's `daimo:offersModel` must appear as `odrl:target` of the attached policy (at Policy level or on any Permission).
- Violates when a catalog record attaches a policy that does not govern the offered model — i.e., the policy is incorrect for this offering.

### 8.6 INV-6: Offering-assigner consistency
- Target: `daimo:AIAssetOffering`.
- Rule: the offering's `daimo:offeredBy` must equal the `odrl:assigner` of the attached policy.
- Violates when the catalog record attributes the publication to one agent while the ODRL offer is issued by another — an internal governance inconsistency.

Every invariant has a designated positive-case test (the flood-risk scenario conforms) and a designated negative-case test ([tests/negative-examples.ttl](tests/negative-examples.ttl) triggers exactly one invariant per focus node: `bad:INV1-artifact`, `bad:INV2-run`, `bad:INV3-deployment`, `bad:INV4-auth`, `bad:INV5-offering`, `bad:INV6-offering`).

---

## 9. CQ → element traversal map

For each of the 23 CQs, which DAIMO classes and properties does the SPARQL exercise?

| CQ | Classes traversed | Properties traversed | Inference needed? |
|---|---|---|---|
| R1 | AIAssetOffering, it6:MachineLearningModel | offersModel, offeredBy, dct:title | no |
| R2 | AIAssetOffering | foaf:primaryTopic *(entailed from offersModel)*, offeredBy, dct:issued | subPropertyOf |
| R3 | it6:MachineLearningModel, odrl:Offer | odrl:hasPolicy | no |
| R4 | ModelDeployment, IOContract | deploysModel, hasIOContract, inputFormat, outputFormat, authMethod | no |
| R5 | AIAssetOffering, ParticipantRole + subclass | offeredBy, hasRole, rdf:type, `rdfs:subClassOf+` | subClassOf path |
| D1 | it6:MachineLearningModel, it6:Task | it6:hasTask | no |
| D2 | it6:MachineLearningModel, odrl:Offer, odrl:Prohibition | odrl:hasPolicy, odrl:prohibition, odrl:action | no (negation-as-failure via `FILTER NOT EXISTS`) |
| D3 | ModelDeployment, dcat:DataService, IOContract | deploysModel, exposedAs, hasIOContract, endpointURL, authMethod | no |
| D4 | it6:Evaluation, it6:EvaluationMeasure, SharedEvaluationContext | usesEvaluationContext, it6:evaluates, it6:hasEvaluationMeasure, it6:hasValue | numeric filter |
| E1 | AIAssetOffering, ModelDeployment, dcat:DataService, IOContract | foaf:primaryTopic *(entailed)*, deploysModel, exposedAs, hasIOContract | subPropertyOf |
| E2 | ModelDeployment, it6:Run, ExecutionAuthorization | deploysModel, mls:realizes, prov:wasAssociatedWith, authorizesRun, grantedTo | join |
| E3 | it6:Run, mls:Algorithm, it6:Flow, it6:ComputerInfrastructure | mls:realizes, it6:hasFlow, it6:runnedOn | no |
| E4 | AuditEvidence, spdx:Checksum | evidenceOf, integrityHash, spdx:algorithm, spdx:checksumValue, signedBy, recordedAt | no |
| E5 | DerivedArtifact, ExecutionAuthorization | derivedFromRun, underAuthorization | no |
| V1 | it6:Evaluation, SharedEvaluationContext | usesEvaluationContext, contextTask, contextDataset, datasetVersion, protocol, randomSeed | no |
| V2 | it6:Evaluation, SharedEvaluationContext | usesEvaluationContext, it6:evaluates, it6:hasEvaluationMeasure | aggregation |
| V3 | it6:Evaluation, SharedEvaluationContext | ... same as V2 | ordering |
| V4 | it6:MachineLearningModel, it6:Benchmark | it6:hasBenchmark | no |
| V5 | it6:Evaluation, SharedEvaluationContext, it6:Flow, it6:Run | contextFlow, mls:realizes, prov:startedAtTime | no |
| G1 | AIAssetOffering | offersModel, offeredBy | no |
| G2 | ModelDeployment, IOContract | deploysModel, onInfrastructure, hasIOContract | no |
| G3 | ExecutionAuthorization | authorizesRun, grantedTo, expiresAt | direct DAIMO--ODRL bridge |
| G4 | CrossParticipantProvenanceRecord, DerivedArtifact | derivedFromRun, records, spansParticipantContext | aggregation (GROUP_CONCAT) |

---

## 10. Example KG instance map

Concrete instance names from [examples/flood-risk-scenario.ttl](examples/flood-risk-scenario.ttl), grouped by DAIMO class.

### 10.1 Participants and roles

| Instance | Class | Role(s) |
|---|---|---|
| `ex:upm` | foaf:Organization | ModelProvider (via `ex:upm-provider-role`) |
| `ex:municipality` | foaf:Organization | ModelConsumer (via `ex:municipality-consumer-role`) |
| `ex:inesdata-op` | foaf:Organization | PlatformOperator |
| `ex:csic-climate` | foaf:Organization | Evaluator |
| `ex:gaia-x-compliance` | foaf:Organization | GovernanceActor |

### 10.2 Participant contexts

- `ex:ctx-upm`, `ex:ctx-municipality`, `ex:ctx-inesdata` — three `edc:ParticipantContext` instances.

### 10.3 Models and offerings

| Model | Offering | Policy |
|---|---|---|
| `ex:flood-risk-v2` | `ex:offering-flood-v2` | `ex:flood-risk-policy` (CC-BY-style: `odrl:use` + `odrl:distribute`) |
| `ex:flood-risk-v1-baseline` | `ex:offering-flood-v1` | `ex:flood-risk-policy` (shared with v2) |
| `ex:flood-risk-v2-commercial` | `ex:offering-flood-v2-ro` | `ex:flood-risk-research-only-policy` (`odrl:use` allowed, `odrl:commercialize` prohibited) |

**Note**: the `dct:title` `"CC-BY 4.0 offer"@en` on `ex:flood-risk-policy`
is a human-readable label; the policy encodes the permissions/prohibitions
directly via ODRL actions rather than declaring formal equivalence to the
CC-BY-4.0 licence URI. The policy is CC-BY-4.0-*consistent* but not
literally the CC-BY-4.0 licence.

### 10.4 Deployment and service

- `ex:deployment-flood-v2` deploys `ex:flood-risk-v2` on `ex:upm-gpu-cluster`, exposed as `ex:flood-risk-service` at `https://api.inesdata.example.org/flood-risk/v2`, with IOContract `ex:flood-risk-iocontract` (JSON/GeoJSON/OAuth2).

### 10.5 Execution

- `ex:agreement-municipality-flood-v2` (`daimo:ExecutionAuthorization`) grants `ex:municipality` `odrl:use` permission on `ex:flood-risk-v2`.
- `ex:run-2026-04-20-legs` is the authorised run, associated with `ex:municipality`.
- `ex:prediction-legs-2026-04-20` (`daimo:DerivedArtifact`) is the output.

### 10.6 Evaluation

- `ex:evalctx-climatebench-v1-2026-1-holdout` — the shared context (ClimateBench v1, 2026.1, holdout, seed 42).
- `ex:eval-flood-v2` (accuracy 0.89) and `ex:eval-flood-v1` (accuracy 0.82) both use the same context.

### 10.7 Audit and provenance

- `ex:audit-run-legs` (`daimo:AuditEvidence`) attests `ex:run-2026-04-20-legs`, signed by `ex:inesdata-op`, SHA-256 checksum.
- `ex:bundle-flood-legs` (`daimo:CrossParticipantProvenanceRecord`) spans `ex:ctx-upm`, `ex:ctx-municipality`, `ex:ctx-inesdata`, recording the run and evaluation.

---

## Change log versus earlier revisions

- **v0.1.5 → v0.1.6** (2026-07-07):
  - Synchronized the human-readable reference version with the validation matrix.
  - No class, property, SHACL shape, validation result, or empirical count is changed by this metadata update.

- **v0.1.4 → v0.1.5** (2026-04-23):
  - Rewrote 14 `skos:example` annotations to describe generic patterns instead of referencing specific IRIs from the example KG (R-1 from the sixth-pass audit).
  - Declared `daimo:hasOffering rdfs:subPropertyOf foaf:isPrimaryTopicOf` for symmetry with `offersModel ⊑ foaf:primaryTopic` (R-6).
  - Verified DSP namespace `https://w3id.org/dspace/v0.8/` resolves via w3id.org; documented the choice inline (R-4).

- **v0.1.3 → v0.1.4** (2026-04-23):
  - Enriched ontology header (`dct:creator`, `dct:contributor`, `dct:publisher`, `owl:priorVersion`, `dct:conformsTo`, `rdfs:seeAlso`).
  - Declared `shapes/daimo-shapes.ttl` as its own `owl:Ontology` with `owl:versionIRI`.
  - Added `skos:definition` and `skos:example` on every DAIMO class (14 classes).
  - Named the pairwise-disjointness axiom `daimo:TopLevelKindsDisjointness`.
  - Added four inverse properties (`hasDeployment`, `hasDerivedArtifact`, `hasAuditEvidence`, `hasOffering`).
  - Declared `owl:AsymmetricProperty` on `offersModel`, `deploysModel`, `authorizesRun`, `derivedFromRun`, `evidenceOf`.
  - Added `rdfs:seeAlso` to source specs on every externally-declared class/property in `alignment.ttl`.

- **v0.1.2 → v0.1.3** (2026-04-23):
  - Added `sh:in` enum for `daimo:authMethod` and `sh:pattern` regex for `daimo:protocol` (data-quality gate).
  - Added two cross-class invariants: INV-5 (offering model ∈ policy target) and INV-6 (offering agent ≡ policy assigner).
  - Promoted `ex:audit-run-legs-checksum` from blank-node to named IRI.
  - Exercised the multi-endpoint capability in the example KG with a second (gRPC/mTLS) service.

- **v0.1.1 → v0.1.2** (2026-04-23):
  - Dropped `daimo:offeredBy rdfs:subPropertyOf dct:publisher` (semantic attribution bug).
  - Added `odrl:target` and `odrl:assigner` on Offer policies (ODRL-2.2 conformance).
  - Migrated `daimo:integrityHash` from `xsd:string` to `spdx:Checksum` (algorithm + value).
  - Removed `owl:FunctionalProperty` on `daimo:exposedAs` and `daimo:hasIOContract` (multi-endpoint support).
  - Added SHACL shape `daimo:OfferInDAIMOShape`.
  - Updated CQ-R2 SPARQL to use `daimo:offeredBy` directly.

See [CHANGELOG.md](CHANGELOG.md) for the v0.1.0 → v0.1.1 delta.
