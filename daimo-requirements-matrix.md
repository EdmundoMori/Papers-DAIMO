# DAIMO Requirements Matrix

Date: 2026-04-20 (updated 2026-04-22)
Baseline sources:
- MLDCAT-AP 3.0.0
- Dataspace Protocol (DSP), operationalised by Eclipse EDC
- INESData platform

## Note on EDC vs DSP vs ODRL (added 2026-04-22)

**EDC (Eclipse Dataspace Components) is a runtime framework, not a
vocabulary.** Its internal Java entities (Asset, ContractDefinition,
ContractNegotiation, ContractAgreement, TransferProcess) are control-plane
data structures, not on-the-wire RDF terms. Where this matrix says
"owner = EDC", the precise statement is:

- **Protocol layer**: use the **Dataspace Protocol (DSP)** vocabulary at
  `https://w3id.org/dspace/v0.8/` — the W3C-track spec that EDC
  implements on the wire. Examples: `dspace:Catalog`, `dspace:Dataset`,
  `dspace:ContractOffer`, `dspace:ContractNegotiation`,
  `dspace:TransferProcess`.
- **Policy / offer / agreement**: use **ODRL** at
  `http://www.w3.org/ns/odrl/2/`. Both DSP and EDC reuse ODRL here.
  Examples: `odrl:Offer`, `odrl:Agreement`, `odrl:Permission`,
  `odrl:Prohibition`.
- **Catalog / dataset / service**: use **DCAT / DCAT-AP** at
  `http://www.w3.org/ns/dcat#`.
- **EDC-specific extensions** (not yet in DSP): use the informal EDC
  namespace `https://w3id.org/edc/v0.0.1/ns/`. Only four concepts need
  this namespace today: `edc:ParticipantContext`, `edc:DataPlaneInstance`,
  `edc:EndpointDataReferenceEntry`, and participant-bound Asset
  descriptors that carry participant-context IDs.

DAIMO alignment therefore uses ODRL / DCAT / DSP for wire semantics and
`edc:` only for the few genuinely EDC-specific extensions.

## Legend

- `Reuse directly`: use the external concept as the main representation
- `Reuse with DAIMO profile`: reuse the external concept, but add DAIMO constraints, interpretation rules, or mappings
- `New DAIMO extension`: define a DAIMO class/relation because the external stack does not cover the need well enough

## Design principle

DAIMO should not try to replace:
- `MLDCAT-AP` for AI/ML metadata
- `DCAT` for catalog publication
- `ODRL` for policy/agreement structure
- `EDC` for dataspace process semantics

DAIMO should mainly do three things:
- connect AI/ML assets to dataspace exchange semantics
- make cross-participant AI usage machine-actionable
- add the missing governance/provenance layer for AI assets in a dataspace

## Matrix

| Need | Primary owner | Reuse basis | DAIMO action |
|---|---|---|---|
| Participant identity | DSP + EDC | DSP defines participant identity on the wire; EDC control plane binds it to offers, agreements, and transfers | `Reuse directly` for participant identity (DSP wire terms); add DAIMO guidance on how participant IDs identify model providers, consumers, evaluators, and operators |
| Participant context / multi-tenant runtime context | EDC extension | EDC 2025-08 decision record introduces `edc:ParticipantContext` and `participantContextId` as a first-class runtime concept. Not yet standardised in DSP. | `Reuse with DAIMO profile` via `edc:` extension namespace; DAIMO references participant context where AI assets, agreements, or runs are scoped to a specific participant context |
| Participant registration and participant directory | INESData | INESData adds a registration service and participant catalog federation | `New DAIMO extension` if this must be represented semantically; likely classes like `ParticipantRegistryEntry` or `RegisteredParticipant` |
| Participant roles | INESData + DAIMO need | INESData operationally distinguishes admin, user, connector actors; MLDCAT-AP models provider/registered user but not dataspace platform roles comprehensively | `New DAIMO extension`; define role concepts such as provider, consumer, evaluator, platform operator, registry admin |
| Catalog publication of AI assets | DCAT + DSP + MLDCAT-AP | DCAT publishes datasets/distributions/services; DSP extends DCAT for dataspace catalogs; MLDCAT-AP already profiles ML assets into this publication model | `Reuse directly`; DAIMO should not redefine catalog mechanics |
| Internal asset descriptor vs published dataset | EDC (internal) vs DCAT (wire) | EDC's internal `Asset` Java entity is distinct from the externally published `dcat:Dataset`. The internal descriptor is an implementation concern, not an ontology concern. | `Reuse with DAIMO profile`; DAIMO describes published datasets (DCAT / MLDCAT-AP), not the internal connector Asset |
| Machine learning model as core asset | MLDCAT-AP | `it6:MachineLearningModel` is the main ML concept and already links files, datasets, benchmarks, policies, risks, repositories, and modalities | `Reuse directly` as the main model class |
| Model file / package artifact | MLDCAT-AP | `it6:File` plus checksum and format are already modeled | `Reuse directly` |
| Model repository links | MLDCAT-AP | `hasRepository` and Linked Papers with Code repository classes already exist | `Reuse directly` |
| Model service / API exposure | MLDCAT-AP + DCAT | MLDCAT-AP gives `dcat:DataService` with `servesModel`; DSP uses `dcat:DataService` and distribution endpoints for access/negotiation | `Reuse with DAIMO profile`; DAIMO should clearly distinguish model service, access service, and runtime deployment |
| Model deployment instance | None strong | MLDCAT-AP is still weak on deployment-instance semantics; EDC is transfer-oriented, not model-serving-architecture oriented | `New DAIMO extension`; likely `ModelDeployment` or `ModelServingInstance` |
| Training / testing / validation datasets | MLDCAT-AP | `trainedOn`, `testedOn`, `validatedOn`, plus dataset metadata and distributions are already modeled | `Reuse directly` |
| Dataset provenance and curation metadata | MLDCAT-AP | `biasMethod`, `curationMethod`, `dataProvenance`, `unsuitabilityMethod`, `collectionMethod` already exist on datasets | `Reuse directly` |
| Dataset distributions / concrete files | DCAT + MLDCAT-AP | `dcat:Distribution` plus feature, quality, policy, and data-category enrichments already exist | `Reuse directly` |
| Model task / task type | MLDCAT-AP | `Task`, `TaskType`, `TaskCollection` provide richer semantics than flat task tags | `Reuse directly` |
| Input/output modality | MLDCAT-AP | `Modality` is first-class, though release artifacts contain naming inconsistencies | `Reuse with DAIMO profile`; DAIMO should pin one canonical interpretation and avoid inheriting MLDCAT-AP artifact typos |
| Benchmark linkage | MLDCAT-AP | `Benchmark` and model-to-benchmark links already exist | `Reuse directly` |
| Evaluation metrics and evaluation results | MLDCAT-AP | `Evaluation`, `EvaluationMeasure`, `QualityMeasurement`, and run/evaluation structure already exist | `Reuse directly` |
| Run / execution record | MLDCAT-AP | `Run`, `Flow`, `Parameter`, `OutputFileDescription`, `OutputFilePrediction`, infrastructure, and environmental impact are present | `Reuse directly` for ML execution semantics |
| Dataspace transfer process | DSP | DSP's `dspace:TransferProcess` models transfer separately from contract negotiation and supports finite/non-finite flows; EDC implements this on the wire | `Reuse directly` for dataspace transfer semantics |
| AI inference invocation across participants | None fully | MLDCAT-AP models runs, EDC models transfers, but neither fully captures cross-participant AI invocation authorization and evidence as one concept | `New DAIMO extension`; likely `InferenceInvocation` or `ExecutionAuthorization` as the bridge between agreement and run |
| Ongoing service access / non-finite AI service usage | DSP | DSP (via EDC) explicitly supports non-finite transfers and policy monitoring for ongoing access | `Reuse with DAIMO profile`; DAIMO should adapt this to AI service subscriptions, API sessions, or long-lived model access |
| Usage policy / offer policy | ODRL + MLDCAT-AP | DSP and EDC use ODRL offers and agreements; MLDCAT-AP attaches `odrl:hasPolicy` to models/distributions | `Reuse directly` for policy objects; DAIMO should not define a parallel policy language |
| Access policy hidden from catalog vs public offer policy | EDC (implementation concern) | EDC distinguishes access policy from contract policy in its control-plane selectors; this is a runtime implementation concern, not an on-the-wire RDF distinction | `Not ontologised` by default; DAIMO can note the distinction if a scenario requires it, but the canonical policy language remains ODRL |
| Contract definition linking policies to assets | EDC (internal) | EDC's `ContractDefinition` binds assets to access and contract policies through selectors at runtime. It is a Java entity, not an on-the-wire term. | `Not ontologised` directly; DAIMO reifies the publication event as `daimo:AIAssetOffering` (⊑ `odrl:Offer`) which carries the wire-visible policy |
| Contract negotiation | DSP | DSP's `dspace:ContractNegotiation` defines asynchronous negotiation semantics on the wire; EDC implements them | `Reuse directly` |
| Contract agreement | ODRL (DSP profile) | Agreement is the token/artifact granting access. DSP uses `odrl:Agreement`; EDC implements it. | `Reuse directly`; DAIMO specialises it as `daimo:ExecutionAuthorization` (⊑ `odrl:Agreement`) with AI-specific grantee and run-binding semantics |
| AI-specific agreement semantics | DAIMO need | ODRL gives structure, but not AI-specific meaning such as permitted inference, evaluation, fine-tuning, redistribution of derived outputs | `New DAIMO extension`; define controlled AI usage terms aligned to ODRL actions/constraints |
| Endpoint data reference / access coordinates | EDC extension | EDC models `edc:EndpointDataReferenceEntry` as the coordinates enabling pull access; this is an EDC-specific extension not yet in DSP | `Reuse` via EDC extension namespace when needed; otherwise use `dcat:DataService` + `dcat:endpointURL` |
| Provenance of cross-participant generation / derivation | None strong | MLDCAT-AP has rich metadata but weak PROV-style cross-party derivation; EDC tracks processes but not full artifact provenance semantics | `New DAIMO extension`; likely align with PROV-O later for derived outputs, who ran what, and under which agreement |
| Derived artifact from model use | None strong | MLDCAT-AP has output file concepts and predictions, but not a clean dataspace-governed notion of derived artifact exchanged across parties | `New DAIMO extension`; define `DerivedArtifact` or `ExecutionResultArtifact` |
| Audit / evidence record for compliance | None strong | EDC has events and policy monitoring; MLDCAT-AP has transparency/risk metadata; neither fully models audit evidence as a reusable semantic artifact | `New DAIMO extension` |
| Risk, harm, limitations, intended use | MLDCAT-AP | `HarmRisk`, `limitations`, `intendedUse`, `designSpecifications`, `testingDescription`, `totalNumberOfParameters` already exist | `Reuse directly` |
| Infrastructure / hardware / libraries | MLDCAT-AP | `ComputerInfrastructure`, `Hardware`, `Library` already exist | `Reuse directly` |
| Shared vocabularies across connectors | INESData | INESData exposes shared connector vocabularies and vocabulary management as platform services | `New DAIMO extension` if vocabulary governance is important to the target scenario |
| Federated catalog aggregation | DSP + INESData | DSP has federated-catalog behavior; INESData operationalises it with specific endpoints and participant crawling | `Reuse with DAIMO profile`; DAIMO may need `FederatedCatalogEntry` only if the scenario reasons over aggregated entries as first-class objects |
| Public portal publication context | INESData | INESData adds CMS/public-portal visibility beyond connector publication | `New DAIMO extension` only if DAIMO needs to model public dissemination, discoverability layers, or publication channels |
| Domain application / connector specialization | INESData | INESData shows language-space connectors, ELG integration, mobility AI services, and mapping applications | `New DAIMO extension` only if a target domain requires it; otherwise keep this out of the core ontology |

## Provisional DAIMO core

If we keep DAIMO tight, the likely core DAIMO-native concepts are:
- `daimo:AIAssetOffering`
- `daimo:ParticipantRole`
- `daimo:ModelDeployment`
- `daimo:ExecutionAuthorization`
- `daimo:DerivedArtifact`
- `daimo:CrossParticipantProvenanceRecord`
- `daimo:AuditEvidence`

Possible optional DAIMO concepts depending on scope:
- `daimo:RegisteredParticipant`
- `daimo:SharedVocabulary`
- `daimo:FederatedCatalogEntry`
- `daimo:PublicationChannel`

## What DAIMO should explicitly avoid redefining

Do not redefine these if the goal is a defensible ontology:
- catalog
- dataset
- distribution
- data service
- policy
- offer
- agreement
- transfer process
- machine learning model
- benchmark
- evaluation
- run
- hardware/library/infrastructure

Instead, DAIMO should import or align them and describe:
- how they connect in a data-space AI scenario,
- what AI-specific usage rights mean,
- what provenance/evidence must be recorded,
- how participant roles and contexts affect access and execution.

## Recommended next modeling step

Turn this matrix into a `layered ontology draft` with:
1. `Reused backbone`
2. `DAIMO core extension`
3. `Optional platform extension`
4. `Example instance pattern`

That draft should then be tested against one concrete scenario, for example:
- a provider offers a model,
- a consumer negotiates access,
- the consumer invokes the model as a service,
- a derived artifact is produced,
- provenance and compliance evidence are recorded.

## Sources

- MLDCAT-AP 3.0.0: https://semiceu.github.io/MLDCAT-AP/releases/3.0.0/
- MLDCAT-AP changelog: https://github.com/SEMICeu/MLDCAT-AP/blob/main/releases/3.0.0/html/Changelog.md
- MLDCAT-AP context: https://github.com/SEMICeu/MLDCAT-AP/blob/main/releases/3.0.0/context/mldcat-ap.jsonld
- MLDCAT-AP SHACL: https://github.com/SEMICeu/MLDCAT-AP/blob/main/releases/3.0.0/shacl/mldcat-ap-SHACL.ttl
- EDC control-plane docs: https://github.com/eclipse-edc/eclipse-edc.github.io/blob/main/content/en/documentation/for-adopters/control-plane/_index.md
- EDC entity docs: https://github.com/eclipse-edc/eclipse-edc.github.io/blob/main/content/en/documentation/for-contributors/control-plane/entities/_index.md
- EDC participant context decision record: https://github.com/eclipse-edc/Connector/blob/main/docs/developer/decision-records/2025-08-26-participant-context/README.md
- INESData connector README: https://github.com/INESData/inesdata-connector/blob/develop/README.md
- INESData registration service README: https://github.com/INESData/inesdata-registration-service/blob/develop/README.md
- INESData local environment README: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/README.md
- INESData connector interface config: https://github.com/INESData/inesdata-connector-interface/blob/develop/src/assets/config/app.config.json
- INESData connector interface catalog browser: https://github.com/INESData/inesdata-connector-interface/blob/develop/src/app/shared/services/catalog-browser.service.ts
- INESData connector interface vocabulary service: https://github.com/INESData/inesdata-connector-interface/blob/develop/src/app/shared/services/vocabulary.service.ts
- INESData connector configuration `c1`: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/resources/configuration/connector-c1-configuration.properties
- INESData connector configuration `c2`: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/resources/configuration/connector-c2-configuration.properties
- INESData connector configuration `elg`: https://github.com/INESData/inesdata-espacio-linguistico/blob/master/resources/configuration/connector-elg-configuration.properties
