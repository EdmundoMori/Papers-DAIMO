# DAIMO — Design & Rationale

Companion to [`00-DAIMO-OVERVIEW.md`](00-DAIMO-OVERVIEW.md). This document is the
main source for the paper's **"Ontología"** section: motivating scenario,
requirements (actors, NFRs, 23 competency questions), the three governing design
decisions, the 14 native classes with their alignment and justification, and —
crucially — the **deliberate non-alignment decisions** that protect the reused
vocabularies.

---

## 1. Motivating scenario (running example)

A **flood-risk** scenario in a Spanish data space grounds every requirement and
the example knowledge graph (`daimo/examples/flood-risk-scenario.ttl`):

- **UPM** (Universidad Politécnica de Madrid) trains and **publishes** a
  flood-risk prediction model as a governed catalog offering — acting as
  **Model Provider (MP)**.
- The **municipality of Leganés** **discovers**, negotiates access to, and
  **invokes** the model — acting as **Model Consumer (MC)**.
- **INESData** runs the data-space platform, **hosts the deployment** and seals
  audit evidence — acting as **Platform Operator (PO)**.
- A benchmarking team compares candidate models under identical conditions —
  **Evaluator (EV)**.
- A compliance body audits the cross-party execution chain — **Governance
  Actor (GA)**.

The scenario exercises the full lifecycle: **registration → discovery →
invocation/execution → evaluation → governance**, spanning **multiple EDC
participant contexts**, which is exactly what a single ML metadata profile
(MLDCAT-AP) cannot express on its own.

---

## 2. Requirements

### 2.1 Actors

| Code | Actor | Responsibility |
|---|---|---|
| MP | Model Provider | Publishes models as governed offerings |
| MC | Model Consumer | Discovers, negotiates, invokes models |
| PO | Platform Operator | Runs the runtime, hosts deployments, seals evidence |
| EV | Evaluator | Evaluates/compares models under shared contexts |
| GA | Governance Actor | Audits evidence, enforces compliance |

### 2.2 Non-functional requirements (part of the ORSD)

- OWL 2 **DL** profile (decidable).
- **Reuse-first:** every native term must justify *why* it is not already
  covered by DCAT/DCAT-AP/MLDCAT-AP/ODRL/PROV-O/EDC.
- **Alignment axioms** declared for every native class that subclasses an
  external term.
- **SHACL** validation must pass for every DAIMO class.
- CC-BY 4.0 (ontology) / Apache-2.0 (code); bilingual labels (en + es).
- **FAIR** publication: persistent `w3id.org` URI, content-negotiated HTML + RDF.

### 2.3 Competency questions (23, five categories)

Each CQ has an actor, a natural-language question, a SPARQL binding
(`daimo/queries/queries.md`), a flag for whether **inference** is needed, and an
elicitation source. Full text in `daimo/ORSD/daimo-cqs.md`.

**R — Registration and Publication (Model Provider), 5**
- CQ-R1 Which models has a provider published as governed catalog assets?
- CQ-R2 For a model, which offering registered it, by whom, and when? *(inference: `offersModel ⊑ foaf:primaryTopic`)*
- CQ-R3 Which licence/usage policy applies to a published model?
- CQ-R4 What I/O contract is declared for the invocation interface?
- CQ-R5 For each offering, what `ParticipantRole` subclass does the provider hold? *(inference: `rdfs:subClassOf+`)*

**D — Discovery and Selection (Model Consumer), 4**
- CQ-D1 Which models solve a given task in a given domain? *(task subtype inference)*
- CQ-D2 Which are usable under a given licence/policy pattern? *(negation-as-failure)*
- CQ-D3 Which expose a service endpoint, and what auth method does each require?
- CQ-D4 Which reach a minimum metric threshold under a shared evaluation context?

**E — Execution and Auditability (Platform Operator / Governance Actor), 5**
- CQ-E1 For an offering, what endpoint, auth method and I/O contract apply to invocation? *(inference via `offersModel`)*
- CQ-E2 For a deployment, which runs ran, by which agents, under which authorization? *(agreement-to-run join)*
- CQ-E3 For a run, what implementation, algorithm, flow and infrastructure were used?
- CQ-E4 What audit evidence (hash, signer, timestamp) supports a run?
- CQ-E5 What derived artefacts did a run produce, under which authorization?

**V — Evaluation and Reproducibility (Evaluator), 5**
- CQ-V1 What shared evaluation context (dataset, version, protocol, seed) applies?
- CQ-V2 Under a shared context, which model achieves the highest value of a metric?
- CQ-V3 How do two+ models rank under the same context and metric?
- CQ-V4 On which benchmark suites has a model been evaluated?
- CQ-V5 What reproducibility artefacts (flow, notebook, result table, checksum) back an evaluation?

**G — Governance Bridge (DAIMO-native novelty), 4**
- CQ-G1 Which offerings in the federated catalog include a given model?
- CQ-G2 Which deployments serve a model, on what infrastructure, with what I/O contract?
- CQ-G3 Which execution authorization (and the agreement it derives from) authorised a specific run?
- CQ-G4 Across participant contexts, what is the full provenance bundle for a derived artefact? *(aggregation via `GROUP_CONCAT`)*

> **Narrative for the paper:** the earlier design claimed "19 CQs, 14
> implemented"; after adding the dataspace-bridge classes this becomes
> **"23 CQs, 23 implemented"**. The 4 new G-CQs are precisely the questions
> MLDCAT-AP alone cannot answer and thus carry DAIMO's contribution.

---

## 3. Three governing design decisions

### D1 — Reuse-first integration profile, not a new vocabulary
The AI model, dataset, policy, run, catalog and provenance already have mature
standards. DAIMO **surrounds** the reused `it6:MachineLearningModel` with
dataspace-bridge semantics instead of subclassing it. This keeps the core small
(14 classes) and interoperable, and forces every native term to justify its
existence (reuse-first NFR).

### D2 — Participant roles as anti-rigid reifications (`prov:Role`), not agent subtypes
A `foaf:Agent` **plays** roles (`daimo:hasRole`) scoped to an EDC participant
context (`daimo:inParticipantContext`); it is **not** typed as a role. This is
ontologically correct (roles are *anti-rigid*: an agent gains/loses them over
time) and lets one agent hold several roles at once (e.g. a research group that
is both `Evaluator` and `ModelProvider`). Consequently the five role subclasses
are **intentionally NOT disjoint**.

### D3 — Governance = cross-class invariants, not just per-class completeness
What distinguishes DAIMO from a passive metadata profile is that it enforces
**business rules that cut across classes** (eight SHACL-SPARQL invariants,
INV-1..INV-8). A governance ontology must catch cross-class inconsistencies
(e.g. an artefact derived from a run its authorization never covered, or an I/O
contract that describes a service the deployment does not expose), not only
whether each node has its mandatory fields.

---

## 4. The 14 native classes

### 4.1 Nine top-level bridge classes

| Class | Aligned to (`rdfs:subClassOf`) | Why it is native (not reused) |
|---|---|---|
| `AIAssetOffering` | `dcat:CatalogRecord` | Reifies the **dataspace offering event**: bundles the model (`offersModel`), the issuing agent (`offeredBy`) and an ODRL **offer** policy (`hasOfferPolicy`). Neither DCAT nor MLDCAT-AP reifies this. Relates to DSP `dspace:ContractOffer` (negotiation-time) via informative `skos:related`. |
| `ParticipantRole` (+5 subclasses) | `prov:Role` | Dataspace role types that DCAT/MLDCAT-AP/EDC do not reify (see D2). |
| `ModelDeployment` | `prov:Entity` | A **running/hosted instance** of a model — distinct from the model *and* from the service that exposes it. |
| `IOContract` | *(stand-alone)* | The **minimum machine-actionable invocation contract**: input/output media type, auth method, optional I/O schemas. Absent from DCAT/MLDCAT-AP. Identifies the `dcat:DataService` it applies to via `daimo:forService` (functional), so a multi-endpoint deployment resolves format and auth per endpoint without ambiguity. |
| `ExecutionAuthorization` | `odrl:Agreement` | ODRL agreement **produced by a DSP contract negotiation**, specialised with `authorizesRun`, `grantedTo`, `expiresAt`. |
| `DerivedArtifact` | `prov:Entity`, `dcat:Resource` | A **governed, catalog-describable output** of a run, carrying its own provenance (`derivedFromRun`) and policy pointer (`underAuthorization`). |
| `CrossParticipantProvenanceRecord` | `prov:Bundle` | A PROV bundle aggregating activities/entities across **≥2 EDC participant contexts** into one audit-ready narrative. |
| `AuditEvidence` | `prov:Entity` | Compliance evidence: structured SPDX checksum (`integrityHash`), signer (`signedBy`), timestamp (`recordedAt`). |
| `SharedEvaluationContext` | *(stand-alone)* | Reified grouping that makes evaluations **comparable**: task + dataset + dataset version + protocol + random seed. |

### 4.2 Five participant-role subclasses (`rdfs:subClassOf daimo:ParticipantRole`)

`ModelProvider`, `ModelConsumer`, `PlatformOperator`, `Evaluator`,
`GovernanceActor` — one per actor, **not mutually disjoint** by design.

### 4.3 Disjointness axiom

`daimo:TopLevelKindsDisjointness` (`owl:AllDisjointClasses`) declares the **nine
top-level kinds pairwise disjoint**. `ParticipantRole` subclasses are
**deliberately excluded** so an agent can hold multiple roles simultaneously.

---

## 5. Alignment strategy

### 5.1 What IS aligned (entailed)

**Class alignments** (`rdfs:subClassOf`): `AIAssetOffering ⊑ dcat:CatalogRecord`;
`ExecutionAuthorization ⊑ odrl:Agreement`; `ModelDeployment ⊑ prov:Entity`;
`DerivedArtifact ⊑ prov:Entity, dcat:Resource`;
`CrossParticipantProvenanceRecord ⊑ prov:Bundle`; `AuditEvidence ⊑ prov:Entity`;
`ParticipantRole ⊑ prov:Role`.

**Property alignments** (`rdfs:subPropertyOf`):
`offersModel ⊑ foaf:primaryTopic`; `hasOfferPolicy ⊑ odrl:hasPolicy`;
`hasOffering ⊑ foaf:isPrimaryTopicOf`; `grantedTo ⊑ odrl:assignee`;
`derivedFromRun ⊑ prov:wasGeneratedBy`; `contextTask ⊑ it6:hasTask`.

**Informative mappings** (SKOS, not entailed) to DSP:
`AIAssetOffering skos:related dspace:ContractOffer`,
`ExecutionAuthorization skos:related dspace:ContractNegotiation`,
`CrossParticipantProvenanceRecord skos:related dspace:TransferProcess`.

### 5.2 What is deliberately NOT aligned (and why) — key novelty argument

These non-alignments are conscious modelling decisions that **prevent semantic
corruption of the reused vocabularies**. They are strong material for the paper's
rationale.

| Native term | Tempting alignment | Why it is REJECTED |
|---|---|---|
| `offeredBy` | `⊑ dct:publisher` | On a `dcat:CatalogRecord`, `dct:publisher` is the **catalog maintainer** (the platform), not the **model author**. Conflating them would (wrongly) entail the registering platform is the model creator. |
| `authorizesRun` | `⊑ prov:used` | `prov:used` has domain `prov:Activity`. An `odrl:Agreement` is a **policy artefact (Entity-like)**, not an Activity; the alignment would silently type every authorization as `prov:Activity`. |
| `grantedTo` | `⊑ prov:qualifiedAssociation` | `prov:qualifiedAssociation` ranges over a reified `prov:Association`, **not the agent itself**. The correct agent-side alignment is `odrl:assignee`. |
| `evidenceOf` | `⊑ prov:hadActivity` | `prov:hadActivity` is used on reified influence objects, not on entities. `AuditEvidence` is an **Entity *about* an activity**; PROV-O has no direct property for this. |
| `contextDataset` / `contextFlow` | `⊑ it6:trainedOn` / `it6:hasFlow` | Their domains (`it6:MachineLearningModel`, `it6:Run`) would **re-type `SharedEvaluationContext`** via RDFS inference. |
| `datasetVersion` | `⊑ dct:hasVersion` | `dct:hasVersion` links a resource to *another version resource*; DAIMO needs a **literal** version token for reproducible benchmarking. |
| `forService` | `⊑ dcat:endpointDescription` | Wrong direction (`dcat:DataService → description`) and different intent: `endpointDescription` points to an **API-description document** (e.g. OpenAPI), not to a structured `IOContract`. No DCAT/MLDCAT-AP/DSP property means "the service this I/O contract describes", so `forService` stays **native and unaligned**. |

### 5.3 Why alignment lives in a separate module

`alignment.ttl` is kept separate so importing consumers can load DAIMO **without
committing to full external vocabularies in their reasoner**. It also declares
minimal **external term stubs** (with `rdfs:isDefinedBy` pointing to the
authoritative ontology) so reasoners and pitfall scanners can resolve the axioms
without the full imports. Domains/ranges of external properties are kept
**maximally permissive** (`owl:Thing`) to avoid strengthening the source
ontologies.

---

## 6. Property model highlights

- **Functional properties** capture "exactly one" facts: e.g. `offersModel`,
  `offeredBy`, `hasOfferPolicy`, `deploysModel`, `onInfrastructure`,
  `grantedTo`, `derivedFromRun`, `underAuthorization`, `signedBy`,
  `usesEvaluationContext`, `forService` (each I/O contract describes exactly one
  service), and all datatype properties.
- **Asymmetric properties** encode "distinct individuals" (e.g. `offersModel`,
  `deploysModel`, `authorizesRun`, `derivedFromRun`, `evidenceOf`, `forService`):
  an offering is not its model, a deployment is not its model, an I/O contract is
  not the service it describes, etc.
- **Deployment ↔ service ↔ contract triangle.** A `ModelDeployment` may expose
  several `dcat:DataService` endpoints (`exposedAs`, non-functional) and declare
  several `IOContract`s (`hasIOContract`, non-functional). `forService` links
  each contract to the specific exposed service it describes, turning what used
  to be a cartesian `service × contract` join into a direct per-endpoint lookup.
  SHACL invariants INV-7/INV-8 keep the triangle consistent (contract targets an
  exposed service; every exposed service has a contract).
- **Inverse properties** ease reverse traversal of the four most-queried
  one-to-many relations: `hasDeployment` (inv. `deploysModel`),
  `hasDerivedArtifact` (inv. `derivedFromRun`), `hasAuditEvidence` (inv.
  `evidenceOf`), `hasOffering` (inv. `offersModel`), plus `authorizedBy` (inv.
  `authorizesRun`). Because each counterpart is functional, a reasoner entails
  `owl:InverseFunctionalProperty` on the inverse.

The complete class/property reference (domains, ranges, characteristics) is in
[`02-DAIMO-IMPLEMENTATION.md`](02-DAIMO-IMPLEMENTATION.md) §3.

---

## 7. Explicit scope boundaries (what DAIMO is NOT)

Documented in `daimo/ORSD/daimo-cqs.md` as scope notes, useful to pre-empt
reviewer questions:

- **Discovery** concerns AI *model assets*, not payload schemas or sector
  vocabularies (those can attach via `IOContract` schema refs or future
  profiles).
- **Execution** describes governed invocations and their evidence chain; DAIMO
  does **not** implement a federated execution engine, orchestrator, connector
  runtime or TEE model. No `isInvokedBy` property or `AIModelEntity` service
  class is needed — invocation is *reconstructed* from offering → deployment →
  service → I/O contract → authorization → `it6:Run`.
- **Evaluation** represents the shared task/dataset-version/protocol/seed and the
  referenced metric; it does **not** normalise metric formulae or prove
  equivalence between protocols. Bias/fairness metrics fit as evaluation
  measures under a `SharedEvaluationContext` when supplied.
- **Governance** covers ownership, licences, versions, datasets and conformance
  through R/E/V/G CQs plus reused constructs; certification workflows and
  detailed compliance controls belong to **policy profiles**, not the core.
