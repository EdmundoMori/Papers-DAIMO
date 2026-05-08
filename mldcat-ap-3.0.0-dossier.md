# MLDCAT-AP 3.0.0 Dossier

Date: 2026-04-20
Version pinned: MLDCAT-AP 3.0.0
Status in spec: SEMIC Candidate Recommendation, published 2025-09-30

## 1. What It Is

MLDCAT-AP 3.0.0 is an application profile that extends DCAT-AP for machine learning resources.
It is not a standalone ontology that replaces DCAT. Its design assumes catalog publication, exchange, and validation in a DCAT-AP ecosystem.

The official abstract says it aims to describe machine learning models together with their datasets, quality measured on those datasets, and citing papers. The spec also says AI Act and AI Code of Practice concepts were added over time.

Official sources:
- HTML spec: https://semiceu.github.io/MLDCAT-AP/releases/3.0.0/
- Changelog: https://github.com/SEMICeu/MLDCAT-AP/blob/main/releases/3.0.0/html/Changelog.md
- JSON-LD context: https://github.com/SEMICeu/MLDCAT-AP/blob/main/releases/3.0.0/context/mldcat-ap.jsonld
- SHACL: https://github.com/SEMICeu/MLDCAT-AP/blob/main/releases/3.0.0/shacl/mldcat-ap-SHACL.ttl

## 2. What It Reuses

The release page lists these prefixes and reused assets:
- `dcat`, `dct`, `foaf`, `adms`: catalog and metadata backbone from DCAT-AP / DCAT
- `odrl`: policies and rights constraints
- `dqv`, `qb`: quality measurement modeling
- `mls`: algorithm and execution relation (`mls:Algorithm`, `mls:realizes`)
- `mlso`: algorithm typing
- `dpv`: data categories on distributions
- `skos`: controlled concepts and task type lexicalization
- `spdx`: checksums and checksum algorithms
- `lpwc`, `lpwcc`: Linked Papers with Code paper/repository relations
- `frapo`: funding relation

Practical ownership by layer:
- DCAT/DCAT-AP owns catalog, dataset, distribution, data service, catalog record, common metadata.
- MLDCAT-AP adds the machine-learning-specific layer mostly in the `it6:` namespace.
- ODRL owns policy objects.
- DQV/QB own quality measurement patterns.
- MLS/MLSO own algorithm typing and one execution relation.
- LPWC owns paper and repository linking.

## 3. Core Semantic Architecture

### 3.1 Catalog layer

This is still a DCAT-AP profile first.

Main DCAT-facing classes:
- `dcat:Catalog`
- `dcat:CatalogRecord`
- `dcat:Dataset`
- `dcat:Distribution`
- `dcat:DataService`

Important MLDCAT-AP extensions at this layer:
- `dcat:Dataset` gets AI-dataset documentation fields like `it6:biasMethod`, `it6:collectionDate`, `it6:collectionMethod`, `it6:curationMethod`, `it6:dataProvenance`, `it6:unsuitabilityMethod`.
- `dcat:Distribution` gets data-specific operational fields like `it6:hasFeature`, `it6:defaultTargetAttribute`, `it6:ignoreAttribute`, `dqv:hasQualityMeasurement`, `dpv:hasData`.
- `dcat:DataService` gets `it6:servesModel` in addition to `dcat:servesDataset`.

Interpretation:
MLDCAT-AP does not abandon the DCAT publication model. It treats ML resources as catalog resources that can still be distributed, served, recorded, and validated like other data assets.

### 3.2 Model layer

The central ML class is `it6:MachineLearningModel`.

Its role is broader than a simple model card. It connects:
- data provenance: `trainedOn`, `testedOn`, `validatedOn`, `runnedOn`
- files and repositories: `hasFile`, `hasRepository`
- governance: `hasPolicy`, `hasRisk`, `hasProvider`, `hasRegisteredUser`
- transparency: `limitations`, `intendedUse`, `bias`, `shortDescription`, `designSpecifications`, `howToUse`
- publication/versioning: `created`, `modified`, `releaseDate`, `placedOnMarketDate`, `version`
- evaluation context: `hasBenchmark`, `evaluationResults`, `evaluationStrategy`
- architecture traits: `modelArchitecture`, `totalNumberOfParameters`, `methodOfDistribution`
- lineage: `fineTunedFrom`, `hasVariation`
- modality: `hasInputModality`, `hasOutputModality`

Associated model-side classes:
- `it6:File`
- `it6:Benchmark`
- `it6:HarmRisk`
- `it6:Modality`
- `lpwcc:paper`
- `lpwcc:repository`
- `spdx:Checksum`

Interpretation:
This is not just a model-card vocabulary. It tries to unify discoverability, transparency, risk, publication, artifacts, and some operational/evaluation metadata under one model-centric profile.

### 3.3 Experiment and evaluation layer

MLDCAT-AP has a more operational side than a plain model catalog.

Experiment-related classes:
- `it6:Task`
- `it6:TaskType`
- `it6:TaskCollection`
- `it6:EstimationProcedure`
- `it6:Split`
- `it6:Prediction`
- `it6:PredictionFeature`
- `it6:Run`
- `it6:RunCollection`
- `it6:Evaluation`
- `it6:EvaluationMeasure`
- `it6:Parameter`
- `it6:Flow`
- `it6:FlowParameter`
- `it6:ComputerInfrastructure`
- `it6:Hardware`
- `it6:Library`
- `it6:EnvironmentalImpact`

This is the rough intended flow:
1. A `Task` describes the problem over source data.
2. A `Task` points to an `EstimationProcedure`, output, target feature, and evaluation measure.
3. A `Run` executes an `Algorithm`, uses a `Flow`, may point to a `Task`, and records parameters and output files.
4. A `Run` may carry `Evaluation` instances and environmental impacts.
5. `Flow` captures the reproducible software/pipeline structure and dependencies.
6. `ComputerInfrastructure` captures hardware and libraries involved.

Interpretation:
MLDCAT-AP is trying to bridge catalog metadata and OpenML-like experiment structure. That is one of its most important design characteristics.

## 4. Most Important Classes and What They Mean

### `it6:MachineLearningModel`

Definition in spec: "A file that has been trained to recognize certain types of patterns."

Why it matters:
- It is the entry point most DAIMO work will align with.
- It is where AI transparency, policy, artifact, modality, benchmark, and dataset links converge.

Mandatory properties in the spec quick reference:
- `dct:created`
- `it6:hasFile`
- `dct:identifier`
- `dct:title` via "name"
- `it6:trainedOn`
- `it6:version`

### `dcat:Dataset`

MLDCAT-AP keeps datasets as first-class resources rather than burying them as literals.
This is especially important for training, testing, validation, execution context, and data quality.

Mandatory dataset properties in the quick reference include:
- `it6:collectionDate`
- `dct:description`
- `dct:title`

### `dcat:Distribution`

Distribution is where dataset embodiment, features, policies, quality measurements, and data categories are attached.
This is useful when the same conceptual dataset has multiple files or formats.

### `dcat:DataService`

The key extension is `it6:servesModel`.
This is highly relevant for DAIMO because it separates a published model from the service endpoint that distributes or exposes it.

Mandatory data service properties:
- `dcat:endpointURL`
- `dct:title`

### `it6:Task`

Task is where the problem definition lives.
It is richer than just a task tag.
It can bind:
- source data
- target feature
- output prediction
- estimation procedure
- evaluation measure
- task type

This is one of the stronger parts of the profile if we want machine-actionable evaluation semantics.

### `it6:Run`

Run is the operational execution unit.
Mandatory run properties in the quick reference include:
- `mls:realizes`
- `it6:hasFlow`
- `it6:hasOutputFileDescription`
- `it6:hasOutputFilePrediction`

This means MLDCAT-AP does not stop at publication metadata. It explicitly models executions and outputs.

### `it6:Flow`

Flow captures the software/pipeline architecture necessary to reproduce a model build or execution setup.
It links to libraries and flow parameters and has its own status/version metadata.

This is a strong reuse point if DAIMO needs reproducibility and deployability context.

### `it6:ComputerInfrastructure`

This class packages hardware plus libraries under one named environment.
It is an important clue that the profile aims to cover not just model artifacts, but the environment required to run or evaluate them.

### `it6:HarmRisk`

Risk is a first-class object with:
- description
- mitigation
- nature
- probability
- severity
- source
- type

That makes MLDCAT-AP more governance-ready than a plain catalog profile.

## 5. Strong Design Choices

### 5.1 It stays anchored in DCAT-AP

This is a practical strength.
It means ML models remain publishable in catalog ecosystems instead of becoming a separate metadata island.

### 5.2 It treats datasets as first-class linked resources

Training, testing, validation, and execution datasets are explicit relations, not strings.
This is very important for DAIMO.

### 5.3 It covers both publication and execution/evaluation

Many model metadata efforts stop at model cards.
MLDCAT-AP goes further into task, run, flow, evaluation, split, and infrastructure.

### 5.4 It includes governance and AI Act style concerns

Modality, harm risk, policies, design specifications, testing description, total parameters, and environmental impact make it much closer to a current European governance setting than older ML metadata profiles.

### 5.5 It is backed by SHACL

The spec explicitly says constraints are expressed in SHACL and provides released shapes plus an SEMIC validation service.
That is valuable if DAIMO later wants a profile with executable conformance checks instead of narrative-only guidance.

## 6. Limits and Modeling Tensions

### 6.1 It is still a profile, not a complete foundational ontology

MLDCAT-AP is very useful, but it is not trying to be a deep formal ontology of AI systems, data spaces, contracts, sovereignty, trust, or deployment governance.
DAIMO should not expect it to solve data-space semantics by itself.

### 6.2 Some definitions are thin or operationally vague

Several classes have no definition or very light definitions in the HTML spec, for example:
- `Evaluation`
- `CostMatrix`
- `FlowParameter`
- `Prediction`
- `PredictionFeature`

That makes the profile usable, but not always conceptually crisp.

### 6.3 Some ranges feel pragmatic rather than ontologically sharp

Examples:
- `MachineLearningModel.hasPrediction` points to `dcat:Dataset`, while `Task.hasOutput` points to `it6:Prediction`.
- `Run.hasOutputFilePrediction` points to `it6:File`.

Interpretation:
There are at least three layers for "output":
- abstract prediction schema
- produced dataset
- produced file

That is workable, but DAIMO will need to be very explicit about which one it is using in each data-space step.

### 6.4 The model definition is still file-centric

The model definition says "A file that has been trained to recognize certain types of patterns."
That is probably too narrow for service-native, hosted, composite, or continuously updated ML assets.

For DAIMO, we may want to distinguish:
- model as intellectual artifact
- model file/package
- model service/API
- model deployment instance

MLDCAT-AP helps, but does not fully separate those four.

### 6.5 It has little explicit provenance beyond selected links

There is rich metadata, but no strong PROV-style account of:
- who performed a specific run
- which activity generated which artifact
- exact derivation chains across organizations

That is likely one area where DAIMO will still need additional modeling if data-space accountability matters.

## 7. Release-Specific Issues To Remember

These are important because we said we would use primary sources and note inconsistencies instead of smoothing them over.

### 7.1 `hasInputModality` inconsistency

The rendered quick reference lists:
- `http://data.europa.eu/it6/hasInputModality`

But the released JSON-LD context maps:
- `MachineLearningModel.hasInputModality` -> `http://data.europa.eu/it6/hasInputModalitity`

And repo search shows the typo also appears in:
- the 3.0.0 context
- the 3.0.0 SHACL TTL
- the `example-machinelearningmodel-hf-apertus.ttl` example

Interpretation:
There is a release inconsistency between the rendered spec and machine-readable artifacts. We should not blindly inherit this into DAIMO.

### 7.2 Output modality inconsistency in one released example

The rendered spec lists `has output modality`.
The JSON-LD Apertus example uses `MachineLearningModel.hasOutputModality`.
But the released Turtle example serializes:
- `it6:hasOutput ex:modality-output-1`

Interpretation:
At least one release example appears inconsistent with the published property name.

### 7.3 Helper context drift in the EOSC example context

The released `eosc-mldcat-ap-context.jsonld` imports the `2.1.0` context, not the `3.0.0` context.
It also mentions older modeling assumptions such as `it6:hasTaskType` and `it6:hasMachineLearningLibrary`, while the 3.0.0 changelog says direct model links of that kind were removed or remodeled.

Interpretation:
The helper context looks transitional and should not be treated as the canonical truth for 3.0.0.

### 7.4 Example data quality issues

In the released Apertus Turtle example:
- dataset version is written as `1.0.O` with letter `O`, not `1.0.0`

This is minor, but it reinforces that examples are useful guidance, not normative truth.

## 8. What This Means For DAIMO

### Reuse directly

Strong candidates to reuse without reinvention:
- `dcat:Catalog`, `dcat:CatalogRecord`, `dcat:Dataset`, `dcat:Distribution`, `dcat:DataService`
- `it6:MachineLearningModel`
- `it6:File`
- `it6:Task`, `it6:TaskType`, `it6:Run`, `it6:Flow`, `it6:Evaluation`, `it6:EvaluationMeasure`
- `it6:Benchmark`
- `it6:Modality`
- `it6:HarmRisk`
- `it6:ComputerInfrastructure`, `it6:Hardware`, `it6:Library`
- `odrl:Policy`
- `dqv:QualityMeasurement`
- `spdx:Checksum`

### Reuse carefully

These need explicit DAIMO guidance because the profile is less sharp or internally inconsistent:
- input/output modality
- output/prediction/result distinctions
- helper contexts and examples
- direct model-to-service semantics in operational settings
- task vs task tags vs business capability

### Likely DAIMO extension areas

If your target is a data-space-native ontology, likely additions are:
- participant roles in data-space interactions
- offer/contract/agreement semantics beyond plain ODRL attachment
- execution authorization and controlled access flow
- sovereignty/compliance obligations tied to exchange and use
- provenance of cross-party execution and derived artifacts
- deployment instance vs service vs model package separation
- trust/audit/evidence records across federated actors

## 9. Bottom Line

MLDCAT-AP 3.0.0 is the strongest public baseline we have found so far for DAIMO because it already combines:
- DCAT-style publication
- model metadata
- dataset links
- benchmark/evaluation structure
- service links
- policy links
- risk and transparency metadata
- executable SHACL validation

But it should be treated as:
- the base backbone for DAIMO,
- not the final DAIMO ontology,
- and not an artifact we can copy blindly without correcting release inconsistencies.

For the next DAIMO step, the cleanest strategy is:
1. take MLDCAT-AP 3.0.0 as the baseline profile,
2. define a stable DAIMO interpretation layer over the parts we actually want,
3. fix or isolate inconsistent MLDCAT-AP release artifacts in our implementation notes,
4. add only the genuinely data-space-specific layer on top.
