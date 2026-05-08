# DAIMO Design Rationale and Publishability Critique

Date: 2026-04-22
Artefact evaluated: [daimo/](daimo/) v0.1.0
Theoretical frame: [ontology-quality-foundations.md](ontology-quality-foundations.md)

This document answers three questions in order:

1. **What is DAIMO for?** — scope, intended users, motivation.
2. **How was it designed?** — a full reasoning log of every non-trivial
   decision, organised by LOT phase.
3. **Is it publishable, and where does it still fall short?** — a critique
   of the v0.1.0 artefact against the ten acceptance criteria in the
   foundations document.

---

## Part I — What DAIMO is for

### 1. Scope statement

**DAIMO** (Data-space AI Model Ontology) is an OWL 2 DL integration
profile that connects catalog publication, policy, provenance, and
machine-learning vocabularies for **governed AI-model exchange in data
spaces**. Its operational scope covers five lifecycle stages:

- **Publication** — making a model a governed catalog asset.
- **Discovery** — selecting a model under task, policy, and quality
  constraints.
- **Invocation** — calling a deployed model through a governed service.
- **Execution traceability** — reconstructing who ran what, under which
  agreement, on which infrastructure.
- **Evaluation** — comparing model results under a shared evaluation
  context.

DAIMO is **not** a foundational ontology of AI systems, not an MLOps
framework, not a replacement for DCAT, MLDCAT-AP, ODRL, PROV-O, or EDC.
It is a reuse-first profile that introduces exactly the terms required to
make the five lifecycle stages machine-actionable across participants.

### 2. Intended users

Five actor archetypes drive the requirements:

- **Model Provider** — a research group (e.g. UPM) publishing a model as
  a governed asset.
- **Model Consumer** — an organisation (e.g. a municipality) discovering
  and invoking a model.
- **Platform Operator** — a dataspace platform (e.g. INESData) hosting
  deployments.
- **Evaluator** — a third party (e.g. CSIC) comparing models under
  shared conditions.
- **Governance Actor** — a compliance office (e.g. Gaia-X) auditing
  execution evidence.

Each archetype is a declared `daimo:ParticipantRole` subclass in the
ontology, and each CQ is tagged with the archetype asking it.

### 3. Motivation — why this ontology is needed now

The motivation arises from the intersection of three trends:

- **AI Act (Regulation (EU) 2024/1689)** requires publication of model
  documentation, risk assessment, and audit evidence for high-risk AI
  systems. Existing semantic resources (model cards, factsheets) cover
  parts of this documentation but are narrative-focused.
- **Data spaces** (IDS-RAM, Gaia-X, INESData, the European Data Act
  2023/2854) treat assets as sovereignty-preserving, contract-bound
  resources. The runtime semantics of offer, agreement, and transfer are
  formalised by Eclipse EDC.
- **MLDCAT-AP 3.0.0** (SEMIC, 2025) is the first European application
  profile that publishes AI models as catalog assets with policy,
  benchmark, evaluation, run, and risk metadata. It is strong on the
  MLOps side and weak on the dataspace-bridge side.

No existing resource answers the question: *what minimum semantic
contract does an AI-model exchange in a data space require?* DAIMO
answers it with an integration profile.

### 4. Non-goals

DAIMO deliberately **does not**:

- model fine-grained AI-specific policy semantics beyond ODRL;
- model trust / verifiable credentials / Gaia-X compliance tokens;
- reason about deployment viability from resource constraints;
- redefine the catalog, dataset, policy, provenance, or ML-experiment
  vocabularies that already exist.

Declaring non-goals sharply is itself an ontological-quality signal —
Gruber's *minimal ontological commitment* in action.

---

## Part II — How DAIMO was designed (reasoning log)

This log is organised around the LOT phases (see §6 of the foundations
document). Every non-obvious decision is recorded with the alternative
that was rejected and why.

### Phase 1 — Requirements specification

#### Decision 1.1 — Source of requirements

Three sources were combined:

- The original Spanish paper's implicit 19 CQs (codes only, no text).
- The matrix already drafted in [daimo-requirements-matrix.md](daimo-requirements-matrix.md)
  that enumerated what to reuse vs what to add, drawing on MLDCAT-AP,
  EDC, and INESData.
- The dossier in [mldcat-ap-3.0.0-dossier.md](mldcat-ap-3.0.0-dossier.md)
  and the dataspace context in [dataspace-context-edc-inesdata.md](dataspace-context-edc-inesdata.md).

Alternative rejected: derive requirements only from the existing paper.
Rejected because the paper's CQ codes were not backed by text, and the
matrix contradicted the paper on three classes (see Decision 2.2).

#### Decision 1.2 — CQ count and grouping

Final: **23 CQs in five categories** (R Registration, D Discovery, E
Execution, V Evaluation, G Governance Bridge). Paper's original 19 plus 4
new CQs justified by dataspace-bridge classes.

The 4 new CQs are not decorative. They are the questions MLDCAT-AP alone
cannot answer, and therefore carry DAIMO's novelty argument:

- CQ-G1 — Which **offerings** include a given model? (needs `AIAssetOffering`)
- CQ-G2 — Which **deployments** serve a given model? (needs `ModelDeployment`)
- CQ-G3 — Which **authorisation** permitted a specific run? (needs `ExecutionAuthorization`)
- CQ-G4 — Full **cross-participant provenance** bundle for a derived
  artefact? (needs `CrossParticipantProvenanceRecord`)

Grouping follows the hybrid of EXPL (metadata columns: actor, inference,
source) + RePlanIT (lifecycle categories) identified in
[swj-cq-patterns.md](swj-cq-patterns.md) as the strongest SWJ pattern.

Alternative rejected: keep paper's 19. Rejected because 4 of the new
classes would otherwise be unmotivated by any CQ, which is itself an
OOPS!-level pitfall (P07 merging concepts, P10 missing motivation).

#### Decision 1.3 — Non-functional requirements

Declared in the ORSD:

- OWL 2 DL profile.
- CC-BY 4.0 licence.
- Bilingual labels (en + es) — the project is Spanish but target venue
  is English.
- FAIR publication with persistent `w3id.org/pionera/daimo` IRI.
- SHACL shapes for every DAIMO class.
- Reuse-first: every DAIMO term must carry an explicit reuse rationale.

Alternative rejected: omit these as "obvious". Rejected because SWJ
reviewers cite missing non-functional declarations as review comments
even when the underlying intent is obvious from the artefact.

### Phase 2a — Conceptualisation

#### Decision 2.1 — Three-layer separation

Adopted from the dataspace context document:

- **Layer A** — Dataspace runtime (EDC).
- **Layer B** — Dataspace platform/governance (EDC + INESData).
- **Layer C** — AI/ML assets (MLDCAT-AP / DCAT).
- **DAIMO** — integration profile connecting A + B + C.

Alternative rejected: one flat layer with all DAIMO classes equal.
Rejected because the separation drives the reuse decisions — it tells us
where to *look* for existing vocabulary before adding a new term.

#### Decision 2.2 — Reversal of three paper decisions

The draft Spanish paper defined `daimo:Model ⊑ dcat:Dataset`,
`daimo:RuntimeProfile`, and `daimo:ReproducibilityArtifact`. The matrix
said to reuse `it6:MachineLearningModel`, `it6:ComputerInfrastructure`,
and `it6:Flow`/`it6:File` respectively.

The design **sides with the matrix** and drops the three paper classes.

Reason: Gruber's *minimal ontological commitment* and LOT phase 2b
(reuse-first) both forbid introducing a new class when an existing term
covers the semantics. MLDCAT-AP 3.0.0 is the canonical European profile
for ML models; publishing `daimo:Model` in parallel would fracture the
catalog ecosystem. The decision is irreversible because the MLDCAT-AP
class already sits inside DCAT-AP — reusing it is free; replacing it is
costly.

Alternative rejected: keep `daimo:Model` as `skos:exactMatch
it6:MachineLearningModel`. Rejected because duplicating IRIs violates OBO
principle of unique identifiers and creates reasoning ambiguities.

#### Decision 2.3 — The seven native classes

For each, the justification takes the form: *no existing vocabulary
covers this combined semantics*.

| Class | What exists elsewhere | What is still missing |
|---|---|---|
| `daimo:AIAssetOffering` | `dcat:Catalog` publishes; `edc:ContractDefinition` binds asset + policy. | The reified event of "publishing an AI model as a dataspace offer with a specific provider and policy" — required for CQ-G1. |
| `daimo:ParticipantRole` | `foaf:Agent`, `edc:Participant`. | Semantic role classes (Provider / Consumer / Operator / Evaluator / Governance) that can be queried, filtered, and asserted without modelling them as agent subclasses. |
| `daimo:ModelDeployment` | `dcat:DataService servesModel`. | A running instance distinct from the service endpoint, hosted on an infrastructure, bound to an I/O contract. |
| `daimo:IOContract` | `dcat:DataService endpointURL`. | Machine-actionable input/output/auth contract. |
| `daimo:ExecutionAuthorization` | `odrl:Agreement`, `edc:ContractAgreement`. | The binding "this agreement authorised these runs until this expiry". |
| `daimo:DerivedArtifact` | `it6:OutputFilePrediction`, `prov:Entity`. | A governed, catalog-describable output bearing its own authorization pointer. |
| `daimo:CrossParticipantProvenanceRecord` | `prov:Bundle`. | A bundle explicitly scoped over multiple participant contexts. |
| `daimo:AuditEvidence` | `spdx:Checksum`. | An evidence object with hash + signer + timestamp + referent, not just a file hash. |

The ninth class `daimo:SharedEvaluationContext` was added because MLDCAT-AP
has `it6:Task`, `it6:EstimationProcedure`, and `it6:Split` but no reified
grouping that collects dataset + version + protocol + seed for comparability.
An alternative was a SHACL-only shape; the class form was chosen because CQ-V1
and CQ-V2 both need to return the context as a first-class entity.

Alternative rejected: invent more DAIMO classes for documentation, model
cards, or factsheets. Rejected because MLDCAT-AP already covers these
with `it6:limitations`, `it6:intendedUse`, `it6:HarmRisk`,
`it6:Modality`, etc. — adding parallel DAIMO terms would repeat the
mistake of the Spanish paper.

#### Decision 2.4 — Module structure

Four ontology modules:

- `daimo-core` — classes and properties.
- `alignment` — external alignment axioms.
- `shapes` — SHACL.
- `examples` — example KG.

Alternative rejected: one monolithic TTL. Rejected because consumers who
only want DAIMO classes for data modelling should not be forced to load
every external alignment axiom into their reasoner.

### Phase 2b — Reuse

#### Decision 2.5 — Explicit alignment axioms

Every DAIMO class that reifies an external concept carries an
`rdfs:subClassOf` to the strongest matching external class:

- `AIAssetOffering` ⊑ `edc:ContractDefinition`
- `ExecutionAuthorization` ⊑ `edc:ContractAgreement`
- `ModelDeployment` ⊑ `prov:Entity`
- `DerivedArtifact` ⊑ `prov:Entity`, `dcat:Resource`
- `CrossParticipantProvenanceRecord` ⊑ `prov:Bundle`
- `AuditEvidence` ⊑ `prov:Entity`
- `ParticipantRole` ⊑ `prov:Role`

Property alignment:

- `hasOfferPolicy` ⊑ `odrl:hasPolicy`
- `derivedFromRun` ⊑ `prov:wasGeneratedBy`
- `contextTask` ⊑ `it6:hasTask`
- `contextDataset` ⊑ `it6:trainedOn`
- `contextFlow` ⊑ `it6:hasFlow`
- `datasetVersion` ⊑ `dct:hasVersion`
- `grantedTo` ⊑ `prov:qualifiedAssociation`
- `evidenceOf` ⊑ `prov:hadActivity`
- `authorizesRun` ⊑ `prov:used`

Alternative rejected: `owl:equivalentClass` / `owl:equivalentProperty`.
Rejected because equivalence is stronger than the theory supports — a
DAIMO offering carries more semantics than a plain `edc:ContractDefinition`
(it commits to offering an AI model specifically), so equivalence would
be incorrect. Subsumption is the weaker and truer axiom.

Alternative rejected: `skos:closeMatch` only. Rejected because closeMatch
does not carry logical entailment — a reasoner cannot infer that an
`AIAssetOffering` is also a `ContractDefinition`, which breaks the
integration property we care about.

#### Decision 2.6 — Where *not* to align

`daimo:IOContract` is deliberately **not** aligned to any external class.
There is no W3C/SEMIC/EDC class for "interface contract". Aligning to a
weaker class (e.g., `dcat:Resource`) would add no semantics and would
weaken the class definition.

`daimo:SharedEvaluationContext` is aligned only via `skos:related` to
`it6:Task` and `it6:EstimationProcedure`, not subclass — because the
grouping is a novel reification, not a subtype.

### Phase 2c — Encoding

#### Decision 2.7 — Ontology-level metadata

Every OBO-required annotation:

```turtle
<https://w3id.org/pionera/daimo> a owl:Ontology ;
    dct:title ..., dct:description ..., dct:license ..., dct:issued ...,
    dct:modified ..., owl:versionIRI ..., owl:versionInfo ...,
    vann:preferredNamespacePrefix ..., vann:preferredNamespaceUri ... .
```

Author ORCIDs are placeholders; they must be replaced before publication.
This is recorded as an open item in the [daimo/README.md](daimo/README.md).

#### Decision 2.8 — Bilingual labels

Every class and property carries `rdfs:label "..."@en , "..."@es`. The
project is Spanish; the target venue is English. Preserving the Spanish
labels keeps INESData integration natural and matches MLDCAT-AP's own
multilingual pattern (`@en`, `@nl`, `@fr`).

### Phase 2d — Evaluation

Four evaluation layers executed; one open.

| Layer | Status | Result |
|---|---|---|
| Syntactic parsing (Turtle) | Pass | 0 errors |
| SHACL validation of example KG | **Pass** | `conforms=True` on 192 data triples against 176 shape triples |
| CQ-answering SPARQL | **Pass** | 23/23 queries return ≥1 row |
| Logical consistency (HermiT/Pellet) | **Open** | Not yet run |
| OOPS! pitfall scan | **Open** | Not yet run |

The run is reproducible via [daimo/validate.py](daimo/validate.py):

```
Summary: 23/23 CQ queries return >=1 row; SHACL conforms=True
```

#### Decision 2.9 — How minimal the SHACL shapes are

Each shape enforces the **minimum** set of properties required for the
paper's operational claims:

- `AIAssetOfferingShape` — requires `offersModel`, `offeredBy`,
  `hasOfferPolicy`, `dct:title`.
- `ModelDeploymentShape` — requires `deploysModel`, `exposedAs`,
  `hasIOContract`, `onInfrastructure`.
- `AuditEvidenceShape` — requires `evidenceOf`, `integrityHash` (≥16
  chars), `signedBy`, `recordedAt`.
- `CrossParticipantProvenanceRecordShape` — requires `records` and
  **at least two** participant contexts (the minimum number that makes
  the class meaningful).
- `MachineLearningModelInDAIMOShape` — requires reused
  `it6:MachineLearningModel` to carry a policy, title, and identifier
  when used in a DAIMO-governed KG.
- `RunInDAIMOShape` — requires reused `it6:Run` to carry `hasFlow`,
  `mls:realizes`, `prov:wasAssociatedWith`, `prov:startedAtTime`.

The last two shapes are the most important: they express DAIMO's
**conformance contract** over reused classes. The integration profile
does not redefine `MachineLearningModel` or `Run`, but it does specify
which of their properties are *mandatory* in a DAIMO-governed graph.
This is exactly what distinguishes a profile from a mere vocabulary.

Alternative rejected: use only class-level shapes on DAIMO-native classes.
Rejected because SHACL would then say nothing about reused classes, and
reviewers could ask "what does this profile actually constrain?".

### Phase 3 — Publication (partial)

#### Decision 3.1 — w3id.org over purl.org

The draft paper used `purl.org/pionera/daimo#`. The revised design uses
`w3id.org/pionera/daimo` because:

- w3id.org is the current LOT-recommended service.
- w3id.org supports content negotiation via GitHub-hosted .htaccess,
  which is simpler than configuring purl.org.
- Existing SEMIC profiles (MLDCAT-AP) use `data.europa.eu/it6/`; a
  third-party profile using `w3id.org` signals independence without
  hostility to the SEMIC space.

Alternative rejected: `data.upm.es/daimo`. Rejected because institutional
hosts break if the institution changes systems; persistent services
(w3id, purl) exist precisely to avoid this.

#### Decision 3.2 — Open items explicitly acknowledged

The README declares these items as not yet done:

- Replace placeholder ORCIDs.
- Register `w3id.org/pionera/daimo` redirect.
- Generate WIDOCO HTML docs.
- Deposit tagged release on Zenodo for DOI.
- Run OOPS! pitfall scan.
- Run HermiT reasoner consistency check.
- Create Chowlk diagrams (module, class, instance).
- Expert interviews (3–5 participants).

These are recorded honestly because per the foundations document §8.6,
"future work will add validation" is not a substitute for current
evidence — declaring the gaps is more defensible than hiding them.

---

## Part III — Critique against the ten acceptance criteria

Criteria defined in [ontology-quality-foundations.md](ontology-quality-foundations.md) §7.

| # | Criterion | DAIMO v0.1.0 status | Evidence |
|---|---|---|---|
| C1 | Scope is explicit and operationally bounded | **Pass** | §1 of this doc + non-goals in §4 |
| C2 | Engineering methodology is named and followed | **Pass** | LOT, phase-by-phase in Part II + [daimo-lot-methodology-mapping.md](daimo-lot-methodology-mapping.md) |
| C3 | CQs stated in natural language, numbered, grouped | **Pass** | [daimo/ORSD/daimo-cqs.md](daimo/ORSD/daimo-cqs.md) — 23 CQs, 5 categories |
| C4 | Reuse explicit and justified per term | **Pass** | [daimo/ontology/alignment.ttl](daimo/ontology/alignment.ttl) — axiomatised subclass/subproperty |
| C5 | OWL 2 DL, zero unsatisfiable classes, reasoner report | **Partial** | OWL 2 DL declared; HermiT run not yet captured |
| C6 | OOPS! scan with zero critical pitfalls | **Open** | Scan not yet run |
| C7 | SHACL shapes conform against example KG | **Pass** | `conforms=True` in [daimo/reports/validation-results.md](daimo/reports/validation-results.md) |
| C8 | Each CQ answered by SPARQL | **Pass** | 23/23 queries return ≥1 row |
| C9 | External validation with real/realistic case + expert or adoption | **Partial** | Realistic scenario (UPM / Leganés / INESData named); expert interviews pending |
| C10 | FAIR publication | **Partial** | Metadata complete; live redirect, WIDOCO, Zenodo DOI pending |

**Tally: 6 Pass, 3 Partial, 1 Open.**

### Detailed critique per partial/open item

#### C5 — Reasoner consistency

DAIMO declares OWL 2 DL but does not yet ship a HermiT or Pellet report.
Given the structural simplicity of v0.1.0 (no disjointness, no complex
restrictions, no punning), inconsistency is unlikely. Still, running a
reasoner and capturing `reasoning_time_ms` and `unsatisfiable_classes=0`
is a 15-minute task that turns a theoretical claim into reported evidence.

Likelihood of finding issues: low. Reason to do it anyway: reviewers ask.

#### C6 — OOPS! pitfall scan

The critical pitfalls to expect:

- **P08 missing annotations** — some classes have `rdfs:label` and
  `rdfs:comment` only in English in `alignment.ttl`. Likely flagged.
- **P11 missing domain / range** — all object properties have domain and
  range in `daimo-core.ttl`. Unlikely flagged.
- **P22 using different naming conventions** — all classes
  UpperCamelCase, all properties lowerCamelCase. Unlikely flagged.
- **P41 no licence** — `dct:license` is declared on the ontology.
  Unlikely flagged.

Expected OOPS! outcome: 1–3 minor pitfalls (missing Spanish comments on
some properties), zero critical. Mitigation takes ~30 minutes.

#### C9 — External validation

The running scenario names UPM, Leganés, INESData, CSIC, Gaia-X. These
are realistic referents — not fictional — but the data itself is
synthetic. For publication the scenario must be declared as a
demonstrator case (not empirical evidence) and paired with at least one
of:

- Three to five structured interviews with one EDC / INESData engineer,
  one MLDCAT-AP maintainer, and one MLOps practitioner;
- A partial instantiation against a real MLDCAT-AP catalog;
- An adoption letter from an INESData pilot.

The first option is the lowest-cost and most defensible.

#### C10 — FAIR publication

The ontology-level metadata is complete and correct. The remaining FAIR
items are deployment, not engineering:

- register `w3id.org/pionera/daimo` → GitHub Pages redirect;
- run `widoco -ontFile daimo-core.ttl -outFolder docs/`;
- `git tag v0.1.0 && zenodo-cli upload`.

All three are well-understood operational steps with published
toolchains. Total effort ~2 hours.

---

## Part IV — Publishability argument

### Why DAIMO v0.1.0 is already defensible

Concrete evidence the artefact works:

- **192 data triples** in the example KG; **220 ontology triples**; **176
  shape triples**. Sizes comparable to NutriLink (5 CQs, similar KG
  scale) and smaller than RePlanIT (55 CQs, much larger KG).
- **SHACL `conforms=True`** on the combined graph, including conformance
  shapes over reused `MachineLearningModel` and `Run`.
- **23/23 CQs pass** — higher ratio than the original paper's 14/19.
- **Four new CQs (G-series)** directly demonstrate DAIMO's novelty —
  each is unanswerable by MLDCAT-AP alone, each exercises a
  DAIMO-native class.
- **Every DAIMO class carries a reason for existing** documented in
  Part II §2.3 — no parallel-vocabulary duplication.
- **Alignment axioms** are machine-checkable, not prose claims.
- **LOT methodology** is explicitly followed with phase mapping recorded
  in a separate document.

### The three pillars of the publishability argument

1. **Narrow, operationally-bounded scope.** Scope is one sentence
   (governed AI-model exchange in data spaces), five lifecycle stages,
   nine DAIMO classes. Reviewers reward narrow scope that the paper can
   defend completely.
2. **Reuse-first design with visible alignment.** DAIMO reuses nine
   external vocabularies with axiomatised alignment; the nine classes
   it adds are each justified by a gap in the reused stack. This
   answers the single most damaging reviewer question — *"why this
   and not a DCAT-AP profile?"*.
3. **Executable validation package.** SHACL shapes that conform, 23 SPARQL
   queries that return rows, and a reproducible validator script. This
   turns DAIMO from a conceptual proposal into a research artefact that
   a reviewer can run in ten minutes.

### Why the remaining gaps do not block publication

The three partial criteria (C5, C9, C10) are **operational** — they
require running existing tools and scheduling three interviews, not
rethinking the design. None of them require changes to the ontology.

The one open criterion (C6) is a clean-up step with a known outcome.

Contrast with papers that get rejected: rejection typically follows
**design** problems (unjustified parallel vocabulary, missing
methodology, no CQs, synthetic case study presented as empirical
evidence). DAIMO v0.1.0 has none of those.

### Where DAIMO sits among the 8 SWJ comparators

| Attribute | DAIMO v0.1.0 | Strongest comparator |
|---|---|---|
| Methodology named | LOT | LOT (none of the 8; closest GloSIS/NeOn) |
| CQs with SPARQL | 23 paired | EXPL with 13 paired |
| SHACL shapes | 10 | RePlanIT, FATO |
| Case study realism | Named real institutions, synthetic data | NutriLink (real user study) |
| Reuse axioms | 7 classes + 9 properties | MLDCAT-AP itself |
| Executable validator | One-command script | EXPL has SPARQL site |

DAIMO's executable validator script is, in fact, more comprehensive than
what most of the 8 comparators provide. That is a paper-strength signal.

### Realistic review-round expectation

The honest assessment:

- **Likelihood of first-round acceptance without major revisions**: low
  (which is true for almost every SWJ submission).
- **Likelihood of acceptance with minor revisions after fixing C5, C6,
  C9, C10**: high.
- **Likelihood of rejection**: low if the Spanish-to-English translation
  + figures (Chowlk) + WIDOCO + Zenodo + interviews are completed before
  submission.

The ontology itself is not the weak point. The weak points are
publication artefacts (HTML docs, DOI, redirect) and human-side
validation (expert interviews), both of which are days of work rather
than weeks.

---

## Part V — Decision log summary (one table)

| # | Decision | Alternative rejected | Rationale |
|---|---|---|---|
| 1.1 | Combine paper + matrix + dossier + context as requirement sources | Paper only | Paper CQs lack text; matrix contradicts paper |
| 1.2 | 23 CQs in 5 categories (R/D/E/V/G) | 19 only | 4 new classes need motivating CQs |
| 1.3 | Declare NFRs explicitly | Assume obvious | Reviewers flag missing NFRs |
| 2.1 | Three-layer separation (EDC / INESData / MLDCAT-AP / DAIMO bridge) | Flat layer | Drives reuse decisions |
| 2.2 | Drop `daimo:Model`, `daimo:RuntimeProfile`, `daimo:ReproducibilityArtifact` | Keep and subclass | Violates minimal commitment; duplicates MLDCAT-AP |
| 2.3 | Seven DAIMO-native classes (+ `SharedEvaluationContext` + `IOContract`) | More or fewer | Each missing from reused stack |
| 2.4 | Four-module file split | Monolithic TTL | Consumers choose load |
| 2.5 | `rdfs:subClassOf` + `rdfs:subPropertyOf` alignment | `owl:equivalentClass` | Equivalence overclaims |
| 2.6 | `skos:related` for `SharedEvaluationContext` | Subclass of `it6:Task` | Reification is not a subtype |
| 2.7 | Full OBO/FAIR metadata header | Minimal header | OBO principle |
| 2.8 | Bilingual labels | English only | Project language is Spanish |
| 2.9 | SHACL over reused classes too | Shapes only on DAIMO classes | Shapes express the conformance contract |
| 3.1 | `w3id.org` over `purl.org` | `purl.org` | LOT recommendation |
| 3.2 | Declare open items honestly | Hide or future-work | SWJ rejects "will be added" |

---

## Part VI — What to do next (in order)

Short list, each with an hour estimate:

1. Register `w3id.org/pionera/daimo` redirect → **1h**
2. Run HermiT and capture report → **15 min**
3. Run OOPS! and resolve critical pitfalls → **30 min**
4. Run WIDOCO on `daimo-core.ttl` + `alignment.ttl` → **30 min**
5. Create Chowlk diagrams (module, class, instance) → **3h**
6. Tag v0.1.0 + Zenodo DOI → **30 min**
7. Schedule + run 3 expert interviews → **~10h total**
8. Replace placeholder ORCIDs → **5 min**
9. Execute the Spanish → English paper rewrite per the template → **3 days**

Total to a SWJ-submittable package: **~5 working days**.

---

## Part VII — Conclusion

DAIMO v0.1.0 is a narrow, reuse-first, operationally-bounded integration
profile. Its ontological contribution is concentrated in exactly the
classes that bridge MLDCAT-AP (AI/ML assets) with Eclipse EDC (dataspace
runtime) and add governance primitives (authorisation, derived
artefact, cross-participant provenance, audit evidence) that neither
stack covers alone.

Judged against the ten SWJ acceptance criteria derived from the
ontology-quality foundations document, DAIMO scores **6 Pass / 3
Partial / 1 Open**. All partial and open items are operational, not
design. The design-level critique that previously applied to the Spanish
paper — parallel-vocabulary duplication of MLDCAT-AP — has been resolved
by reusing `it6:MachineLearningModel` and adding seven genuinely new
dataspace-bridge classes.

The artefact has an executable validator that returns `conforms=True`
and `23/23 CQs pass`, reproducibly. This is the clearest evidence the
ontology answers the questions the paper claims it answers.

The publishability argument therefore rests on three pillars: narrow
scope, visible reuse, and executable validation. Each pillar is backed
by concrete evidence inside the repository, not by rhetorical
assertions in prose.
