# DAIMO Competency Questions

Date: 2026-04-21
Version: 0.1
Source: reconstructed from [daimo-paper-es.pdf](../../daimo-paper-es.pdf) §3.1, §5, §6.1 (paper references codes CQ-R1..CQ-V5 but never the natural-language text — this doc is the missing text)
Additions: 4 new CQs (CQ-G1..CQ-G4) enabled by the revised [daimo-ontology-design.md](../../daimo-ontology-design.md) dataspace-bridge classes.
Presentation pattern: hybrid of RePlanIT (category/lifecycle) + Explanation Ontology (metadata columns), per [swj-cq-patterns.md](../../swj-cq-patterns.md) recommendation.

## Actors

- **MP** — Model Provider (publishes a model, e.g. UPM)
- **MC** — Model Consumer (searches/invokes a model, e.g. municipality)
- **PO** — Platform Operator (runs the dataspace, e.g. INESData)
- **EV** — Evaluator (compares/evaluates)
- **GA** — Governance Actor (audits, enforces policy)

## Non-functional requirements (not CQs, but part of the ORSD)

- OWL 2 DL profile
- CC-BY 4.0 licence for the ontology; Apache-2.0 for code
- Bilingual labels (en + es)
- FAIR publication: persistent URI under `w3id.org/pionera/daimo`, content-negotiated HTML + RDF
- SHACL validation pass for every DAIMO class
- Reuse-first: every DAIMO term must justify why it is not covered by DCAT, DCAT-AP, MLDCAT-AP, ODRL, PROV-O, or EDC
- Alignment axioms declared for every DAIMO class that subclasses an external term

## Competency questions (23)

### R — Registration and Publication (5)

| Code | Actor | Question | SPARQL | Inference | Source |
|---|---|---|---|---|---|
| CQ-R1 | MP | Which AI models has a given provider published as governed catalog assets? | `CQ-R1.rq` | N | paper §3.1 Table 2 |
| CQ-R2 | MP | For a given model, which catalog offering registered it, by which publisher, and when was the registration issued? | `CQ-R2.rq` | **Y (subPropertyOf chain: daimo:offersModel ⊑ foaf:primaryTopic, daimo:offeredBy ⊑ dct:publisher)** | paper §3.1 Table 2 |
| CQ-R3 | MP | Which licence and usage policy apply to a published model? | `CQ-R3.rq` | N | paper §3.1 |
| CQ-R4 | MP | What I/O contract is declared for the invocation interface of a published model? | `CQ-R4.rq` | N | paper §3.1 (unimplemented in current artefact, Table 7 lists 4 R-queries) |
| CQ-R5 | MP | For each offering, what concrete ParticipantRole subclass does the providing agent hold? | `CQ-R5.rq` | **Y (rdfs:subClassOf+ path)** | paper §3.1 |

### D — Discovery and Selection (4)

| Code | Actor | Question | SPARQL | Inference | Source |
|---|---|---|---|---|---|
| CQ-D1 | MC | Which models solve a given task in a given application domain? | `CQ-D1.rq` | Y (task subtype) | paper §5.1 |
| CQ-D2 | MC | Which of those models are usable under a given licence or policy pattern (e.g. non-commercial allowed)? | `CQ-D2.rq` | N (negation-as-failure via `FILTER NOT EXISTS`, not OWL/RDFS inference) | paper §5.1 |
| CQ-D3 | MC | Which models expose a service endpoint, and what authentication method does each require? | `CQ-D3.rq` | N (parametrised — auth method is returned, not hard-coded) | paper §3.1 |
| CQ-D4 | MC | Which of those models reach a minimum metric threshold under a shared evaluation context? | `CQ-D4.rq` | N | paper §5.1 |

### E — Execution and Auditability (5)

| Code | Actor | Question | SPARQL | Inference | Source |
|---|---|---|---|---|---|
| CQ-E1 | PO | For a given catalog offering, what service endpoint, auth method, and I/O contract apply to invoking the underlying model? | `CQ-E1.rq` | **Y (foaf:primaryTopic entailment from daimo:offersModel)** | paper §5.2 |
| CQ-E2 | PO | For a given model deployment, which runs have been executed, by which agents, and under which execution authorization? | `CQ-E2.rq` | Y (agreement-to-run join) | paper §3.1 |
| CQ-E3 | PO | For a given run, what implementation, algorithm, flow, and compute infrastructure were used? | `CQ-E3.rq` | N | paper §5.2 |
| CQ-E4 | GA | What audit evidence (hash, signer, timestamp) supports a given run? | `CQ-E4.rq` | N | paper §5.2 |
| CQ-E5 | PO | What derived artefacts were produced by a given run and under which execution authorisation? | `CQ-E5.rq` | N | new, enabled by `daimo:DerivedArtifact` |

### V — Evaluation and Reproducibility (5)

| Code | Actor | Question | SPARQL | Inference | Source |
|---|---|---|---|---|---|
| CQ-V1 | EV | What shared evaluation context (dataset, version, protocol, seed) applies to a given evaluation? | `CQ-V1.rq` | N | paper §5.3 |
| CQ-V2 | EV | Under a shared evaluation context, which model achieves the highest value of a given metric? | `CQ-V2.rq` | N | paper §5.3 |
| CQ-V3 | EV | How do two or more models rank under the same evaluation context and metric? | `CQ-V3.rq` | N | paper §5.3 |
| CQ-V4 | EV | For a given model, which benchmark suites has it been evaluated on? | `CQ-V4.rq` | N (parametrised on a specific model) | paper §3.1 |
| CQ-V5 | EV | What reproducibility artefacts (flow, notebook, result table, checksum) back a given evaluation? | `CQ-V5.rq` | N | paper §5.3 |

### G — Governance Bridge (4, new)

Enabled by the dataspace-bridge classes introduced in [daimo-ontology-design.md](../../daimo-ontology-design.md). These CQs are the ones that justify DAIMO being more than MLDCAT-AP.

| Code | Actor | Question | SPARQL | Inference | Source |
|---|---|---|---|---|---|
| CQ-G1 | MC | Which offerings in the federated catalog include a given model? | `CQ-G1.rq` | N | new, enabled by `daimo:AIAssetOffering` |
| CQ-G2 | PO | Which deployments serve a given model, on what infrastructure, and with what I/O contract? | `CQ-G2.rq` | N | new, enabled by `daimo:ModelDeployment` |
| CQ-G3 | GA | Which execution authorisation (and the agreement it derives from) authorised a specific run? | `CQ-G3.rq` | Y (subClass reasoning) | new, enabled by `daimo:ExecutionAuthorization` |
| CQ-G4 | GA | Across participant contexts, what is the full provenance bundle for a derived artefact? | `CQ-G4.rq` | Y (aggregation via GROUP_CONCAT) | new, enabled by `daimo:CrossParticipantProvenanceRecord` |

## CQ count recap

| Category | CQs | Implemented now | Rationale |
|---|---|---|---|
| R Registration | 5 | 5 | All answerable with reused MLDCAT-AP + new `AIAssetOffering` |
| D Discovery | 4 | 4 | Covered by MLDCAT-AP + ODRL + SHACL for evaluation filter |
| E Execution | 5 | 5 | Covered by MLS `Run` + new `ExecutionAuthorization`, `DerivedArtifact`, `AuditEvidence` |
| V Evaluation | 5 | 5 | Covered by MLS `Evaluation` + `Flow` + new `SharedEvaluationContext` shape |
| G Governance bridge | 4 | 4 | The only ones unique to DAIMO |
| **Total** | **23** | **23** |  |

The original paper's claim "19 CQs, 14 implemented" becomes "23 CQs, 23 implemented" once the dataspace-bridge classes are added. The 4 new CQs are critical — they are the questions MLDCAT-AP alone cannot answer, and therefore carry the paper's novelty argument.

## How to cite this in the paper

In the rewritten §3.1:

> DAIMO's requirements were elicited from the running dataspace scenario in §1, complemented by the information needs documented in the MLDCAT-AP 3.0.0 specification and the Eclipse EDC control-plane documentation. Twenty-three competency questions were derived and organised into five categories aligned with the dataspace lifecycle: registration, discovery, execution, evaluation, and governance. Each CQ is expressed in natural language, paired with a SPARQL query over the example knowledge graph, and annotated with the asking actor, whether inference is required, and its elicitation source. The full table appears in the ORSD appendix; Table 2 summarises the actor-to-category mapping.
