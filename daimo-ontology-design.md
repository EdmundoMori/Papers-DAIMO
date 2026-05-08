# DAIMO Ontology Design

Date: 2026-04-21
Status: Design draft ready for implementation
Methodology: LOT (phases 2a Conceptualisation and 2b Reuse)
Inputs synthesised in this doc:
- [daimo-paper-es.pdf](daimo-paper-es.pdf) — current paper (Spanish)
- [daimo-requirements-matrix.md](daimo-requirements-matrix.md) — what to reuse vs extend
- [mldcat-ap-3.0.0-dossier.md](mldcat-ap-3.0.0-dossier.md) — MLDCAT-AP analysis
- [dataspace-context-edc-inesdata.md](dataspace-context-edc-inesdata.md) — EDC + INESData layering
- [daimo-rewrite-template.md](daimo-rewrite-template.md) — paper rewrite scaffold
- [daimo-lot-methodology-mapping.md](daimo-lot-methodology-mapping.md) — LOT activity map

---

## 1. Core diagnosis

The paper and the matrix contradict each other on three core classes:

| Concept | Matrix verdict | Paper behaviour | Action |
|---|---|---|---|
| AI model | `Reuse directly` (`it6:MachineLearningModel` from MLDCAT-AP) | Defines parallel `daimo:Model ⊑ dcat:Dataset` | **Drop `daimo:Model`, reuse `it6:MachineLearningModel`** |
| Compute environment | `Reuse directly` (`it6:ComputerInfrastructure`) | Defines parallel `daimo:RuntimeProfile` | **Drop `daimo:RuntimeProfile`, reuse `it6:ComputerInfrastructure` + `it6:Hardware` + `it6:Library`** |
| Task / run / evaluation | `Reuse directly` (`it6:Task`, `it6:Run`, `it6:Evaluation`) | Defines `daimo:EvaluationContext` with dataset/version/protocol/seed | **Justify EvaluationContext as a reified grouping over existing MLDCAT-AP terms, or drop it** |

At the same time, the matrix identifies **seven concepts that a defensible DAIMO ontology needs but that the current paper does not have**:

- `AIAssetOffering` — bridge between model asset and dataspace offer
- `ParticipantRole` — dataspace roles (Provider, Consumer, PlatformOperator, Evaluator, GovernanceActor)
- `ModelDeployment` — hosted/serving instance distinct from model file or data service
- `ExecutionAuthorization` — binds `edc:ContractAgreement` to `it6:Run`
- `DerivedArtifact` — governed output of a model run exchanged across parties
- `CrossParticipantProvenanceRecord` — audit-ready, dataspace-scoped provenance aggregate
- `AuditEvidence` — compliance-oriented, signed/hashed/timestamped evidence

Net effect: the current paper builds the **wrong extension**. It duplicates MLDCAT-AP and misses the dataspace-bridge layer that is the only thing DAIMO is actually entitled to add.

This design doc realigns DAIMO to what the matrix and the MLDCAT-AP dossier already imply.

## 2. Design principles

1. **Reuse-first.** DAIMO adds a term only if no existing W3C/SEMIC/EDC vocabulary covers the semantics.
2. **Three-layer separation** (from [dataspace-context-edc-inesdata.md](dataspace-context-edc-inesdata.md)):
   - Layer A — dataspace runtime (EDC)
   - Layer B — dataspace platform/governance (EDC + INESData)
   - Layer C — AI/ML assets (MLDCAT-AP / DCAT / DCAT-AP)
   - DAIMO is the **integration profile connecting A, B, C**; it is not a fourth parallel layer.
3. **No parallel vocabulary.** Every DAIMO class must justify why it is not a `skos:exactMatch` or `rdfs:subClassOf` something that already exists.
4. **Do not inherit MLDCAT-AP release bugs.** The dossier flags `hasInputModalitity` typo, `hasOutput` drift, and EOSC context pointing to 2.1.0. DAIMO must pin canonical spellings.
5. **OWL 2 DL.** Keep decidable. No punning unless strictly needed.
6. **Bilingual labels (en + es).** DAIMO originates in a Spanish project.
7. **SHACL-validated.** Every DAIMO class carries at least one shape.

## 3. Namespace and module structure

### Namespace
- Ontology IRI: `https://w3id.org/pionera/daimo`
- Prefix: `daimo:`
- Recommendation: migrate from `purl.org/pionera/daimo#` to `w3id.org` (LOT-preferred, more stable, easier content negotiation).

### Modules
```
daimo:core          — the integration vocabulary (Layer bridge)
daimo:offer         — AIAssetOffering and participant roles
daimo:execution     — ModelDeployment, ExecutionAuthorization, IOContract
daimo:provenance    — DerivedArtifact, CrossParticipantProvenanceRecord, AuditEvidence
daimo:align         — external alignment axioms (separate file, importable)
daimo:shapes        — SHACL shapes (separate file)
```

Rationale for modularity: reviewers can load just the modules they need, and the SHACL/alignment files are kept out of the TBox for clean reasoning.

### Imported prefixes (full reuse backbone)

```turtle
@prefix daimo: <https://w3id.org/pionera/daimo#> .
@prefix dcat:  <http://www.w3.org/ns/dcat#> .
@prefix dct:   <http://purl.org/dc/terms/> .
@prefix dcatap:<http://data.europa.eu/r5r/> .
@prefix it6:   <http://data.europa.eu/it6/> .            # MLDCAT-AP
@prefix mls:   <http://www.w3.org/ns/mls#> .             # ML-Schema
@prefix odrl:  <http://www.w3.org/ns/odrl/2/> .
@prefix prov:  <http://www.w3.org/ns/prov#> .
@prefix dpv:   <https://w3id.org/dpv#> .
@prefix dqv:   <http://www.w3.org/ns/dqv#> .
@prefix spdx:  <http://spdx.org/rdf/terms#> .
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .
@prefix foaf:  <http://xmlns.com/foaf/0.1/> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix edc:   <https://w3id.org/edc/v0.0.1/ns/> .       # EDC informal namespace
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
```

## 4. Reused backbone (no DAIMO class needed)

This is the layer DAIMO explicitly does not redefine.

| Concern | Reused class/property | Source |
|---|---|---|
| The AI model itself | `it6:MachineLearningModel` | MLDCAT-AP |
| Model file/package | `it6:File`, `spdx:Checksum` | MLDCAT-AP + SPDX |
| Model repository / paper | `lpwcc:repository`, `lpwcc:paper` | Linked Papers with Code |
| Catalog publication | `dcat:Catalog`, `dcat:CatalogRecord`, `dcat:Dataset`, `dcat:Distribution`, `dcat:DataService` | DCAT |
| Training / testing / validation datasets | `it6:trainedOn`, `it6:testedOn`, `it6:validatedOn` | MLDCAT-AP |
| Task and evaluation semantics | `it6:Task`, `it6:TaskType`, `it6:Run`, `it6:Flow`, `it6:Evaluation`, `it6:EvaluationMeasure`, `it6:Split`, `it6:EstimationProcedure`, `it6:Benchmark` | MLDCAT-AP |
| Compute environment | `it6:ComputerInfrastructure`, `it6:Hardware`, `it6:Library` | MLDCAT-AP |
| Transparency, risk, intended use | `it6:HarmRisk`, `it6:Modality`, `dct:description`, `it6:intendedUse`, `it6:limitations` | MLDCAT-AP |
| Policy expression | `odrl:Policy`, `odrl:Permission`, `odrl:Prohibition`, `odrl:Duty`, `odrl:Constraint` | ODRL |
| Offer / agreement structure | `odrl:Offer`, `odrl:Agreement` | ODRL |
| Dataspace contract and transfer | `edc:Asset`, `edc:ContractDefinition`, `edc:ContractAgreement`, `edc:ContractNegotiation`, `edc:TransferProcess`, `edc:EndpointDataReference`, `edc:ParticipantContext` | EDC |
| Generic provenance | `prov:Activity`, `prov:Entity`, `prov:Agent`, `prov:wasDerivedFrom`, `prov:wasAssociatedWith`, `prov:used`, `prov:generated` | PROV-O |
| Quality measurement | `dqv:QualityMeasurement`, `dqv:hasQualityMeasurement` | DQV |
| Data categories on distribution | `dpv:hasData`, DPV data concepts | DPV |
| Agents and organisations | `foaf:Agent`, `foaf:Organization`, `dct:creator`, `dct:publisher` | FOAF + DCT |

Alignment axiom pattern (stored in `daimo:align`):
```turtle
daimo:AIAssetOffering rdfs:subClassOf edc:ContractDefinition .
daimo:ExecutionAuthorization rdfs:subClassOf edc:ContractAgreement .
daimo:ModelDeployment rdfs:subClassOf prov:Entity .
daimo:DerivedArtifact rdfs:subClassOf prov:Entity, dcat:Resource .
daimo:CrossParticipantProvenanceRecord rdfs:subClassOf prov:Bundle .
daimo:AuditEvidence rdfs:subClassOf prov:Entity .
```

## 5. DAIMO-native vocabulary (with justification per class)

Every class below exists because neither MLDCAT-AP, DCAT, ODRL, EDC, nor PROV-O covers the semantics on its own. Each entry follows LOT's 3-line class description pattern (what / why reused is not enough / where used in the scenario).

### 5.1 `daimo:AIAssetOffering`

- **What**: the reified event of publishing an `it6:MachineLearningModel` into a dataspace as a governed, negotiable offer.
- **Why reuse alone is not enough**: MLDCAT-AP publishes the model in a catalog but has no notion of a dataspace offer. EDC has `ContractDefinition` but it is asset-agnostic. DAIMO needs the link.
- **Where used**: in the running scenario, when a model provider publishes a flood-risk prediction model under specific access conditions.

```turtle
daimo:AIAssetOffering a owl:Class ;
    rdfs:subClassOf edc:ContractDefinition ;
    rdfs:label "AI asset offering"@en, "oferta de activo de IA"@es ;
    rdfs:comment "A dataspace offering of an AI model as a governed asset."@en .

daimo:offersModel a owl:ObjectProperty ;
    rdfs:domain daimo:AIAssetOffering ;
    rdfs:range  it6:MachineLearningModel .

daimo:offeredBy a owl:ObjectProperty ;
    rdfs:domain daimo:AIAssetOffering ;
    rdfs:range  foaf:Agent .

daimo:hasOfferPolicy a owl:ObjectProperty ;
    rdfs:subPropertyOf odrl:hasPolicy ;
    rdfs:domain daimo:AIAssetOffering ;
    rdfs:range  odrl:Offer .
```

### 5.2 `daimo:ParticipantRole`

- **What**: a dataspace-scoped role taken by a participant with respect to an AI asset.
- **Why reuse alone is not enough**: MLDCAT-AP has `hasProvider`/`hasRegisteredUser` but no role taxonomy; EDC treats participants operationally without semantic roles; INESData has admin/user roles operationally but not as semantic resources.
- **Where used**: labelling Ana Ruiz (UPM) as ModelProvider, the municipality as ModelConsumer, INESData operator as PlatformOperator, Gaia-X compliance actor as GovernanceActor.

```turtle
daimo:ParticipantRole a owl:Class ;
    rdfs:label "participant role"@en, "rol de participante"@es .

daimo:ModelProvider    a owl:Class ; rdfs:subClassOf daimo:ParticipantRole .
daimo:ModelConsumer    a owl:Class ; rdfs:subClassOf daimo:ParticipantRole .
daimo:PlatformOperator a owl:Class ; rdfs:subClassOf daimo:ParticipantRole .
daimo:Evaluator        a owl:Class ; rdfs:subClassOf daimo:ParticipantRole .
daimo:GovernanceActor  a owl:Class ; rdfs:subClassOf daimo:ParticipantRole .

daimo:hasRole a owl:ObjectProperty ;
    rdfs:domain foaf:Agent ;
    rdfs:range  daimo:ParticipantRole .

daimo:inParticipantContext a owl:ObjectProperty ;
    rdfs:domain daimo:ParticipantRole ;
    rdfs:range  edc:ParticipantContext .
```

### 5.3 `daimo:ModelDeployment`

- **What**: a running or hosted instance of an `it6:MachineLearningModel` exposed through a `dcat:DataService`, usable under an `edc:ContractAgreement`.
- **Why reuse alone is not enough**: MLDCAT-AP stops at `dcat:DataService servesModel`; EDC has `DataPlaneInstance` but that is infra-generic; there is no semantic object representing "this model is running here, with this config, for this tenant."
- **Where used**: when the platform operator deploys `flood-risk-v2` behind an authenticated REST endpoint.

```turtle
daimo:ModelDeployment a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:label "model deployment"@en, "despliegue de modelo"@es .

daimo:deploysModel a owl:ObjectProperty ;
    rdfs:domain daimo:ModelDeployment ;
    rdfs:range  it6:MachineLearningModel .

daimo:exposedAs a owl:ObjectProperty ;
    rdfs:domain daimo:ModelDeployment ;
    rdfs:range  dcat:DataService .

daimo:onInfrastructure a owl:ObjectProperty ;
    rdfs:domain daimo:ModelDeployment ;
    rdfs:range  it6:ComputerInfrastructure .

daimo:hasIOContract a owl:ObjectProperty ;
    rdfs:domain daimo:ModelDeployment ;
    rdfs:range  daimo:IOContract .
```

### 5.4 `daimo:IOContract`

- **What**: the minimum machine-actionable input/output contract of a deployment, beyond a raw endpoint URL.
- **Why reuse alone is not enough**: DCAT describes the service, not the expected payload. MLDCAT-AP models modality but not invocation contract. OpenAPI would be too heavy and out-of-band.
- **Where used**: the consumer checks `inputFormat=application/json`, `outputFormat=application/geo+json`, `authMethod=oauth2-bearer` before invoking.

```turtle
daimo:IOContract a owl:Class ;
    rdfs:label "I/O contract"@en, "contrato de entrada/salida"@es .

daimo:inputFormat     a owl:DatatypeProperty ; rdfs:range xsd:string .
daimo:outputFormat    a owl:DatatypeProperty ; rdfs:range xsd:string .
daimo:authMethod      a owl:DatatypeProperty ; rdfs:range xsd:string .
daimo:inputSchema     a owl:ObjectProperty   ; rdfs:range dcat:Resource .
daimo:outputSchema    a owl:ObjectProperty   ; rdfs:range dcat:Resource .
```

(This is the one class from the original paper that survives. It is genuinely new.)

### 5.5 `daimo:ExecutionAuthorization`

- **What**: the authorisation binding an `edc:ContractAgreement` to concrete `it6:Run` invocations it permits.
- **Why reuse alone is not enough**: ODRL gives structure; EDC gives agreement objects; neither encodes "this specific run was permitted by this specific agreement under these constraints".
- **Where used**: when the consumer invokes `flood-risk-v2`, the platform logs the authorisation pointer so auditors can trace back from run to agreement.

```turtle
daimo:ExecutionAuthorization a owl:Class ;
    rdfs:subClassOf edc:ContractAgreement ;
    rdfs:label "execution authorization"@en, "autorización de ejecución"@es .

daimo:authorizesRun a owl:ObjectProperty ;
    rdfs:domain daimo:ExecutionAuthorization ;
    rdfs:range  it6:Run .

daimo:grantedTo a owl:ObjectProperty ;
    rdfs:domain daimo:ExecutionAuthorization ;
    rdfs:range  foaf:Agent .

daimo:expiresAt a owl:DatatypeProperty ;
    rdfs:range xsd:dateTime .
```

### 5.6 `daimo:DerivedArtifact`

- **What**: a governed, catalog-describable output produced by an `it6:Run` in a dataspace context.
- **Why reuse alone is not enough**: MLDCAT-AP has `it6:OutputFilePrediction` and `it6:OutputFileDescription` but not a dataspace-facing, policy-bearing resource that can itself be offered back. PROV gives `wasGeneratedBy` but not the catalog wrapper.
- **Where used**: the flood-risk prediction for district 5 produced by `flood-risk-v2` is itself a dataspace artefact with its own provenance and policy.

```turtle
daimo:DerivedArtifact a owl:Class ;
    rdfs:subClassOf prov:Entity, dcat:Resource ;
    rdfs:label "derived artifact"@en, "artefacto derivado"@es .

daimo:derivedFromRun a owl:ObjectProperty ;
    rdfs:subPropertyOf prov:wasGeneratedBy ;
    rdfs:domain daimo:DerivedArtifact ;
    rdfs:range  it6:Run .

daimo:underAuthorization a owl:ObjectProperty ;
    rdfs:domain daimo:DerivedArtifact ;
    rdfs:range  daimo:ExecutionAuthorization .
```

### 5.7 `daimo:CrossParticipantProvenanceRecord`

- **What**: a reusable semantic bundle that aggregates `prov:Activity` and `prov:Entity` across participant contexts to tell a single audit-ready story.
- **Why reuse alone is not enough**: PROV bundles exist but carry no dataspace-specific framing; EDC tracks `TransferProcess` states but not an artefact-level derivation chain.
- **Where used**: the governance actor pulls one bundle showing model → run → derived artifact with all involved participants and agreements.

```turtle
daimo:CrossParticipantProvenanceRecord a owl:Class ;
    rdfs:subClassOf prov:Bundle ;
    rdfs:label "cross-participant provenance record"@en .

daimo:spansParticipantContext a owl:ObjectProperty ;
    rdfs:domain daimo:CrossParticipantProvenanceRecord ;
    rdfs:range  edc:ParticipantContext .

daimo:records a owl:ObjectProperty ;
    rdfs:domain daimo:CrossParticipantProvenanceRecord ;
    rdfs:range  prov:Activity .
```

### 5.8 `daimo:AuditEvidence`

- **What**: a compliance-oriented evidence record attached to any governed event, with integrity guarantees.
- **Why reuse alone is not enough**: no vocabulary in the reused stack carries (hash + timestamp + signer + referent + policy-cited) as one first-class object; matrix confirms this is a native gap.
- **Where used**: when the consumer asks "prove my flood-risk prediction was produced under a valid agreement with the agreed model version", one `daimo:AuditEvidence` resolves the claim.

```turtle
daimo:AuditEvidence a owl:Class ;
    rdfs:subClassOf prov:Entity ;
    rdfs:label "audit evidence"@en, "evidencia de auditoría"@es .

daimo:evidenceOf a owl:ObjectProperty ;
    rdfs:domain daimo:AuditEvidence ;
    rdfs:range  prov:Activity .

daimo:integrityHash a owl:DatatypeProperty ;
    rdfs:subPropertyOf spdx:checksum ;
    rdfs:range xsd:string .

daimo:signedBy a owl:ObjectProperty ;
    rdfs:domain daimo:AuditEvidence ;
    rdfs:range  foaf:Agent .

daimo:recordedAt a owl:DatatypeProperty ;
    rdfs:range xsd:dateTime .
```

## 6. Classes from the current paper: decisions

| Paper class | Decision | Rationale |
|---|---|---|
| `daimo:Model` | **Drop.** Reuse `it6:MachineLearningModel`. | Matrix says reuse directly; no justifying delta over MLDCAT-AP. |
| `daimo:IOContract` | **Keep.** | Genuinely new; no existing vocab covers this. |
| `daimo:RuntimeProfile` | **Drop.** Reuse `it6:ComputerInfrastructure`. | Same fields already in MLDCAT-AP. |
| `daimo:EvaluationContext` | **Reframe** as `daimo:SharedEvaluationContext` with a `sh:NodeShape` that requires `it6:trainedOn`, `it6:hasTask`, dataset version, protocol, seed. | A reified grouping has value for comparability; but it should be a shape over reused terms, not a parallel class. |
| `daimo:Artifact` | **Drop.** Use `prov:Entity` or `dcat:Resource`. | Too generic to justify. |
| `daimo:AuditArtifact` | **Rename to `daimo:AuditEvidence`.** | Matches matrix terminology and PROV alignment. |
| `daimo:ReproducibilityArtifact` | **Drop.** Reuse `it6:Flow` + `it6:File` + `spdx:Checksum`. | MLDCAT-AP already covers reproducibility scaffolding. |

Net change: current paper has 7 DAIMO classes; revised design has **8 DAIMO classes** (AIAssetOffering, ParticipantRole + 5 subclasses, ModelDeployment, IOContract, ExecutionAuthorization, DerivedArtifact, CrossParticipantProvenanceRecord, AuditEvidence). Three paper classes are dropped in favour of MLDCAT-AP reuse; one is reframed as a SHACL shape; one is renamed; seven dataspace-bridge classes are added.

## 7. Running scenario (for paper and for tests)

A municipality in Spain is a `ModelConsumer` in an INESData-based dataspace.
UPM (Universidad Politécnica de Madrid) is a `ModelProvider` publishing `flood-risk-v2`, an `it6:MachineLearningModel` for the `it6:Task` of flood-risk prediction, `it6:trainedOn` ClimateBench-v1.

1. **Publication.** UPM creates a `daimo:AIAssetOffering` that `daimo:offersModel` `ex:flood-risk-v2`, carries an `odrl:Offer` with a CC-BY-NC restriction, and lives in its `dcat:Catalog`.
2. **Discovery.** The municipality queries the federated catalog (INESData), filters by task + domain + policy compatibility (ODRL) + accuracy ≥ 0.85 on the shared `daimo:SharedEvaluationContext` (ClimateBench-v1 v2026.1, holdout protocol, seed 42).
3. **Negotiation.** Standard EDC `ContractNegotiation` produces an `edc:ContractAgreement`; DAIMO lifts it as a `daimo:ExecutionAuthorization` bound to future `it6:Run`s.
4. **Deployment.** The platform operator creates a `daimo:ModelDeployment` of `flood-risk-v2` on UPM-GPU-cluster `it6:ComputerInfrastructure`, exposed via `dcat:DataService` at `https://api.example.org/flood-risk/v2`, with a `daimo:IOContract` (JSON in, GeoJSON out, OAuth2).
5. **Invocation.** The consumer runs the model → `it6:Run`, `prov:wasAssociatedWith` municipality, `daimo:authorizedBy` the agreement; output is `daimo:DerivedArtifact` (`daimo:underAuthorization` pointing back).
6. **Evaluation.** An `it6:Evaluation` of `Accuracy = 0.89` is attached to the run, linked to the shared evaluation context so it is comparable with the published baseline.
7. **Audit.** A `daimo:AuditEvidence` carries `integrityHash`, `signedBy` the platform, and `recordedAt`. A `daimo:CrossParticipantProvenanceRecord` bundles the chain.

This scenario supports **all 19 CQs** of the paper and adds four new ones that the revised vocabulary enables:

- CQ-NEW-1: *Which offerings in the catalog include this model?*
- CQ-NEW-2: *Which deployments serve this model, and on what infrastructure?*
- CQ-NEW-3: *Which agreement authorised this specific run?*
- CQ-NEW-4: *What derived artifacts resulted from runs under this agreement?*

## 8. SHACL sketch (excerpts)

```turtle
daimo:AIAssetOfferingShape a sh:NodeShape ;
    sh:targetClass daimo:AIAssetOffering ;
    sh:property [ sh:path daimo:offersModel ;
                  sh:class it6:MachineLearningModel ;
                  sh:minCount 1 ] ;
    sh:property [ sh:path daimo:offeredBy ;
                  sh:class foaf:Agent ;
                  sh:minCount 1 ] ;
    sh:property [ sh:path daimo:hasOfferPolicy ;
                  sh:class odrl:Offer ;
                  sh:minCount 1 ] .

daimo:SharedEvaluationContextShape a sh:NodeShape ;
    sh:targetClass daimo:SharedEvaluationContext ;
    sh:property [ sh:path it6:hasTask ;         sh:minCount 1 ] ;
    sh:property [ sh:path it6:trainedOn ;        sh:minCount 1 ] ;
    sh:property [ sh:path dct:hasVersion ;       sh:minCount 1 ] ;
    sh:property [ sh:path daimo:protocol ;       sh:minCount 1 ] ;
    sh:property [ sh:path daimo:randomSeed ;     sh:minCount 1 ] .

daimo:AuditEvidenceShape a sh:NodeShape ;
    sh:targetClass daimo:AuditEvidence ;
    sh:property [ sh:path daimo:integrityHash ;  sh:minCount 1 ; sh:datatype xsd:string ] ;
    sh:property [ sh:path daimo:signedBy ;       sh:minCount 1 ] ;
    sh:property [ sh:path daimo:recordedAt ;     sh:minCount 1 ; sh:datatype xsd:dateTime ] ;
    sh:property [ sh:path daimo:evidenceOf ;     sh:minCount 1 ] .
```

## 9. Repository layout (LOT-compliant)

```
daimo/
├── ontology/
│   ├── daimo-core.ttl
│   ├── daimo-offer.ttl
│   ├── daimo-execution.ttl
│   ├── daimo-provenance.ttl
│   └── alignment.ttl
├── shapes/
│   └── daimo-shapes.ttl
├── queries/
│   ├── CQ-R1.rq ... CQ-V5.rq
│   └── CQ-NEW-1.rq ... CQ-NEW-4.rq
├── examples/
│   └── flood-risk-scenario.ttl
├── docs/                   (WIDOCO)
│   └── index-en.html
├── diagrams/               (Chowlk)
│   ├── module-diagram.svg
│   ├── class-diagram.svg
│   └── instance-graph.svg
├── ORSD/
│   └── DAIMO-ORSD.pdf
├── reports/
│   ├── oops-report.html
│   ├── reasoner-report.txt
│   └── validation-results.md
├── LICENSE                 (CC-BY 4.0)
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

## 10. Migration path from current paper to this design

Four steps, ordered to minimise rework:

1. **Replace every occurrence of `daimo:Model` with `it6:MachineLearningModel`** in the ontology, shapes, examples, queries, and paper body. Same for `daimo:RuntimeProfile` → `it6:ComputerInfrastructure`.
2. **Drop `daimo:Artifact` and `daimo:ReproducibilityArtifact`.** Convert reproducibility links to `it6:Flow` and `it6:File`.
3. **Rename `daimo:AuditArtifact` → `daimo:AuditEvidence`** and add `integrityHash`, `signedBy`, `recordedAt`, `evidenceOf`.
4. **Add the seven dataspace-bridge classes** (AIAssetOffering, ParticipantRole hierarchy, ModelDeployment, ExecutionAuthorization, DerivedArtifact, CrossParticipantProvenanceRecord; IOContract already exists). Add matching SHACL shapes, example instances, and SPARQL queries.

After step 4, §4, §5 and §6 of the paper require moderate rewrite — Table 4 (core classes) shrinks on the MLDCAT-AP duplicates and grows on the dataspace-bridge side. Table 6 (reuse) remains but now shows actual alignment axioms, not just name lists.

## 11. Impact on the paper (cross-reference to rewrite template)

| Rewrite template section | What changes with this design |
|---|---|
| §1 Introduction, contributions | Contribution 1 now says "**integration profile** over MLDCAT-AP, EDC, ODRL, PROV-O" — honest and specific. |
| §3 Related work | Compulsory: MLDCAT-AP 3.0.0, EDC control plane, INESData. Gap paragraph sharpens: nobody provides the dataspace bridge. |
| §4 Method (LOT) | Phase 2b reuse is now concrete: 7 external vocabularies, alignment axioms shown. |
| §5 Ontology design | Tables 4, 5 shrink (fewer DAIMO classes); alignment figure becomes essential. |
| §6 Case study | Running scenario in §7 above drops in cleanly; 4 new CQs added. |
| §7 Validation | SHACL shapes now test actual reuse conformance, not just self-defined shapes. |
| §8 Discussion | Limitations section changes: the "IOContract still coarse" limit stands; "duplicates MLDCAT-AP" no longer applies. |

## 12. What this design does **not** solve

Honest limits of the revised design:

- **Fine-grained policy semantics.** ODRL gives structure, not AI-specific action taxonomies (e.g., "may fine-tune on derived data"). Out of scope for this iteration.
- **Deployment viability reasoning.** `ModelDeployment` + `ComputerInfrastructure` describe, but do not reason about, resource fit. A deployment viability CQ would need a deeper runtime ontology.
- **Federated identity and trust.** `ParticipantRole` references `edc:ParticipantContext`; trust/credential semantics (Verifiable Credentials, Gaia-X compliance tokens) are not modelled.
- **INESData shared vocabularies.** Platform vocabulary governance (Layer B) is noted but not ontologised. Can be a future extension.

## 13. Next concrete actions

In order:

1. Create the `ontology/` files above with the classes and axioms exactly as shown. (1 day)
2. Populate `examples/flood-risk-scenario.ttl` from §7. (0.5 day)
3. Write the 4 new CQs + SPARQL queries. (0.5 day)
4. Run OOPS! and HermiT; fix any issues. (0.5 day)
5. Generate WIDOCO docs and publish at `w3id.org/pionera/daimo`. (0.5 day)
6. Update the paper body to reflect the realignment (this drives the Spanish → English rewrite anyway). (3–4 days)
7. Schedule expert interviews with one EDC/INESData stakeholder and one MLDCAT-AP/MLOps stakeholder to validate the alignment decisions. (2 days including write-up)

Total: ~8 working days to a LOT-compliant, reuse-defensible DAIMO ready for SWJ submission.
