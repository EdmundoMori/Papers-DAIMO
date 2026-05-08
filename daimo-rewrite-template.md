# DAIMO Rewrite Template

This document turns the review into a concrete rewrite scaffold for `daimo-paper-es.pdf`.

The goal is not to make the paper longer. The goal is to make the paper easier to defend in an ontology venue by making four things more visible:

- the task DAIMO supports
- the ontology engineering method
- the ontology design choices
- the validation and reuse story

This template is written in English because the most likely target venue is an international ontology journal. You can still use the structure if you draft in Spanish first.

## Recommended title options

Pick one narrow title and keep the scope operational.

1. `DAIMO: An Ontology for Governed AI Model Assets in Data Spaces`
2. `DAIMO: An Ontology for Publishing, Discovering, and Evaluating AI Models in Data Spaces`
3. `DAIMO: A Semantic Model for Governed AI Model Lifecycle Management in Data Spaces`

Avoid titles that sound broader than the paper proves, such as "ontology of AI models" or "general ontology for AI governance".

## Suggested paper structure

1. Introduction
2. Requirements and Competency Questions
3. Related Work and Reuse Boundary
4. Ontology Engineering Method
5. DAIMO Ontology Design
6. Case Study: Governed Model Exchange in a Data Space
7. Validation
8. Discussion and Limitations
9. Availability and Reuse
10. Conclusion

## Running scenario to use throughout the paper

Use one scenario from the introduction onward and keep returning to it:

- A model provider publishes an AI model in a data space.
- A model consumer searches for models satisfying task, policy, and quality constraints.
- A platform operator invokes a selected model through a service endpoint.
- An evaluator or governance actor audits the execution and compares model results under a shared evaluation context.

If possible, name the actors and the setting. Even if the data is synthetic, the scenario should read like a real decision process rather than a toy graph walkthrough.

## Section 1. Introduction

### What this section must do

- Establish why AI models in data spaces are different from plain downloadable artifacts.
- Introduce the running scenario.
- State the research gap in one precise sentence.
- State the contributions in a form reviewers can test.

### What to avoid

- Repeating the same "fragmentation" claim in multiple paragraphs.
- Spending too much space on broad data-space background before the actual problem appears.
- Claiming end-to-end support before the paper shows it.

### Starter opening paragraph

`AI models exchanged in data spaces are not merely downloadable artifacts. They are governed assets that must be published with persistent identity and access conditions, discovered under policy and quality constraints, invoked through operational interfaces, traced across executions, and compared using evaluation evidence. Existing resources support parts of this lifecycle, but they do not provide a unified semantic model for governed model exchange in data-space settings.`

### Starter scenario paragraph

`Consider a simple but representative data-space scenario. A model provider publishes a flood-risk prediction model together with licensing conditions, an invocation interface, and evaluation metadata. A consumer searches for a model that satisfies a target task, acceptable access conditions, and a minimum performance threshold. A platform operator then invokes the selected model through a governed service endpoint, while an evaluator later inspects execution traces and compares results against other models under the same evaluation context. Supporting this sequence requires more than descriptive documentation: it requires machine-actionable links between publication metadata, policy, execution, provenance, and evaluation evidence.`

### Starter contribution paragraph

`This paper presents DAIMO, an ontology for governed AI model assets in data spaces. DAIMO integrates catalog, policy, provenance, and machine-learning vocabularies with ontology terms for interface contracts, runtime requirements, evaluation contexts, audit artifacts, and reproducibility artifacts. The paper makes four contributions. First, it defines a semantic model for publishing, discovering, invoking, and comparing AI models in data spaces. Second, it specifies how DAIMO reuses and extends existing vocabularies rather than replacing them. Third, it provides an executable validation package including SHACL constraints, competency-question queries, and reproducibility artifacts. Fourth, it demonstrates the ontology in a governed model-exchange case study.`

### End-of-introduction paragraph

`The remainder of the paper is structured as follows. Section 2 derives requirements and competency questions. Section 3 positions DAIMO with respect to related work and clarifies the ontology's novelty boundary. Section 4 describes the ontology engineering method. Section 5 presents the ontology design. Section 6 demonstrates DAIMO through a running case study. Section 7 reports validation results. Section 8 discusses limitations. Section 9 describes artifact availability and reuse. Section 10 concludes.`

## Section 2. Requirements and Competency Questions

### What this section must do

- Show where the requirements came from.
- Make competency questions look elicited, not invented after implementation.
- Connect actors, tasks, and ontology modules.

### Minimum defensible requirement sources

- literature on data spaces, catalog governance, and ML lifecycle metadata
- standards and reused vocabularies such as DCAT, ODRL, PROV-O, ML-Schema
- one or more representative operational scenarios

### Stronger version if you can support it

- interviews with model providers, platform operators, or governance actors
- expert feedback on which metadata can realistically be produced and maintained

### Starter first paragraph

`DAIMO was developed through a requirements-driven ontology engineering process. Requirements were derived from three complementary sources: prior work on data spaces and ML lifecycle management, analysis of existing semantic standards and reused vocabularies, and a running operational scenario involving model publication, governed discovery, invocation, auditability, and comparative evaluation. Rather than aiming to model AI systems in general, the requirements were scoped to the information needed to support governed model exchange in data-space environments.`

### Starter actor-to-task paragraph

`Four actor perspectives guided the requirements. Model providers need to publish models as governed assets with persistent identity, usage conditions, and invocation metadata. Model consumers need to discover models that satisfy task, domain, policy, and quality constraints. Platform operators need to invoke models and reconstruct execution evidence. Governance and evaluation actors need to compare results under shared evaluation conditions and inspect audit and reproducibility artifacts. These perspectives were translated into competency questions that define the minimum operational scope of the ontology.`

### Suggested table

Create a table with these columns:

- Actor
- Task
- Information need
- Competency question
- DAIMO module

### How to present the competency questions

- Keep 8-12 key CQs in the main text.
- Move the full list to the appendix.
- Group them by lifecycle stage.

### Short transition paragraph

`The competency questions serve two purposes in this paper. They define the ontology's intended scope and they provide the basis for executable validation. This is important because DAIMO is not proposed as a general conceptualization of AI systems, but as an operational ontology whose value depends on whether the targeted questions can be answered over usable graph data.`

## Section 3. Related Work and Reuse Boundary

### What this section must do

- Position DAIMO against adjacent resources.
- Explain why reuse alone is insufficient.
- Clarify what DAIMO contributes that is genuinely new.

### Recommended subsection flow

1. Documentation artifacts and model transparency resources
2. ML lifecycle and experiment ontologies
3. Governance vocabularies for catalog, policy, and provenance
4. Domain ontologies and operational ontology papers
5. The remaining gap

### Starter gap paragraph

`The gap addressed by DAIMO is not the absence of semantic resources for any one part of the problem. Catalog publication is well supported by DCAT, access conditions can be represented with ODRL, provenance with PROV-O, and parts of ML experimentation with ML-Schema and related work. The missing piece is an ontology-level integration pattern that makes AI models first-class governed assets in data spaces and connects publication metadata, interface contracts, runtime requirements, execution traces, evaluation context, and reproducibility evidence in a single operational model.`

### Starter novelty-boundary paragraph

`DAIMO therefore should not be read as a replacement for DCAT, ODRL, PROV-O, or ML-Schema. Its contribution is narrower and more specific: it provides the ontology terms and alignment pattern needed to operationalize governed model exchange in data-space settings. The novelty lies in this integration profile, in the explicit treatment of model invocation and evaluation artifacts as part of governed exchange, and in the executable validation package used to test whether the resulting model supports the targeted operational questions.`

### What to cut from the current draft

- Repeated descriptions of data spaces before the ontology problem appears.
- Long literature narration that does not directly sharpen the gap.
- Claims that a resource is insufficient without saying insufficient for which task.

## Section 4. Ontology Engineering Method

### What this section must do

- Make the paper read like ontology engineering.
- Show decisions, not just outcomes.
- Explain why the ontology has this shape.

### Recommended subsections

1. Scope and design principles
2. Reuse strategy
3. Conceptual modeling
4. Implementation choices
5. Iterative refinement

### Starter scope paragraph

`The ontology engineering process followed a requirements-driven and reuse-first strategy. The scope was intentionally limited to the lifecycle of governed model assets in data spaces: publication, discovery, invocation, execution traceability, and comparative evaluation. DAIMO does not attempt to model AI systems in general, nor to replace detailed MLOps or benchmarking frameworks. Instead, it captures the semantic links required to make model assets operable and governable across organizational boundaries.`

### Starter design-principles paragraph

`Four design principles guided the ontology. First, reuse existing standards whenever they already capture the intended semantics with sufficient precision. Second, introduce new ontology terms only where the targeted competency questions cannot be answered using reused vocabularies alone. Third, model operationally important distinctions explicitly, especially where publication, invocation, provenance, and evaluation intersect. Fourth, keep the ontology modular and adoption-oriented so that DAIMO can be used as an integration layer rather than a monolithic replacement of existing models.`

### Starter reuse-strategy paragraph

`The reuse strategy prioritized vocabularies already recognized in semantic publishing and governance infrastructures. DCAT was reused for publication and access services, ODRL for permissions and restrictions, PROV-O for activities and responsibility, and ML-Schema for implementations, runs, and evaluations. New DAIMO terms were introduced only where these resources did not adequately capture the semantics of governed model assets in data spaces, such as interface contracts, runtime profiles, audit artifacts, and reproducibility artifacts.`

### Starter key-modeling-choice paragraph

A central modeling decision was to represent `daimo:Model` as a specialization of `dcat:Dataset`. This choice treats a model as a catalog-publishable asset that can expose distributions and data services while remaining compatible with data-space discovery mechanisms. Alternative designs were considered, including modeling the model purely as an ML artifact disconnected from catalog publication. That alternative was rejected because it weakens the connection between discovery, access conditions, and operational reuse in data-space environments.

### Starter iteration paragraph

`The ontology evolved iteratively through repeated alignment, implementation, and validation cycles. During refinement, several issues were corrected, including namespace inconsistencies across ontology, example data, and SHACL shapes, as well as overly strong range declarations that introduced unintended inferences. Reporting these iterations is important because the final ontology emerged not only through adding semantic content, but also through removing fragile semantics that would reduce interoperability or make validation misleading.`

### Figure to add

Add one figure showing:

- reused vocabularies on the left
- DAIMO modules in the center
- supported lifecycle tasks on the right

## Section 5. DAIMO Ontology Design

### What this section must do

- Make the ontology itself visible.
- Explain the purpose of each core module.
- Show how the pieces fit together.

### Recommended subsections

1. Overview and modular structure
2. Core classes
3. Core object and data properties
4. Alignment with reused vocabularies
5. Worked example

### Starter overview paragraph

`DAIMO is organized around the representation of AI models as governed catalog assets. From this core, the ontology connects a model to its invocation interface, implementation and runtime requirements, execution evidence, evaluation context, and supporting artifacts for audit and reproducibility. This structure reflects the operational path through which a model is published, selected, invoked, and later assessed in a data-space setting.`

### How to write the class descriptions

For each class, use the same 3-sentence pattern:

- what the class represents
- why reused vocabularies alone were not enough
- how the class is used in the running scenario

### Starter class paragraph for `daimo:IOContract`

The class `daimo:IOContract` captures the minimum machine-actionable interface information required to invoke a model in a governed setting. While DCAT can describe access services and distributions, it does not by itself provide an ontology-level construct for expressing the expected input and output contract of a model as part of governed model exchange. In the running scenario, this contract allows a consumer or platform operator to determine whether a selected model can be invoked through the advertised endpoint and authentication method.

### Starter class paragraph for `daimo:EvaluationContext`

The class `daimo:EvaluationContext` groups the conditions under which model results are comparable, including dataset, dataset version, protocol, and random seed. This explicit context is necessary because metric values alone are not sufficient evidence for governed selection or ranking. In DAIMO, evaluation claims become comparable only when they are linked to a shared evaluation context rather than reported as isolated scores.

### Starter alignment paragraph

`DAIMO aligns with reused vocabularies at the points where existing standards already offer stable semantics, and introduces DAIMO-specific terms only where operational model exchange would otherwise remain underspecified. This balance is important for adoption. If DAIMO duplicated catalog, policy, or provenance semantics already available in widely recognized vocabularies, it would reduce rather than improve interoperability.`

### Figures to add

- one module diagram
- one instance-level graph example
- optionally one alignment figure showing `daimo:Model -> dcat:Dataset`, `hasPolicy -> ODRL`, `execution -> PROV-O / MLS`

### What to cut from the current draft

- relying on tables alone
- describing classes without explaining why they are needed
- presenting terms without a running instance

## Section 6. Case Study: Governed Model Exchange in a Data Space

### What this section must do

- Show how DAIMO is used in a realistic process.
- Make the ontology feel necessary.
- Connect the use case to the competency questions.

### Recommended subsection flow

1. Case setup
2. Publication and discovery
3. Invocation and execution traceability
4. Evaluation and comparison

### Starter case-setup paragraph

`To illustrate the ontology in use, we consider a governed model-exchange case in which three models are published for the same task and application domain. One model serves as a previously available baseline, while two models are candidates for selection and execution. Each model is described with publication metadata, usage conditions, an invocation interface, execution-related metadata, and evaluation evidence. The purpose of the case study is not to claim broad empirical coverage, but to demonstrate how DAIMO connects the information required across the publication-to-evaluation lifecycle.`

### Starter discovery paragraph

`The first task is governed discovery. A consumer searches for models suitable for a target task and domain, but also needs to exclude models whose license or policy conditions make them unusable in the intended setting. DAIMO supports this by linking the published model asset to task and domain metadata, and to explicit policy information that can narrow the discovery space. If quality thresholds are also relevant, the ontology permits filtering by evaluation evidence under a shared evaluation context rather than by unqualified score claims.`

### Starter execution paragraph

`The second task is operational invocation and later auditability. Once a model is selected, a platform operator needs to know how to access the service, what authentication method applies, and what contract the interface expects. After execution, the operator or auditor may need to reconstruct who ran the model, when the run took place, which implementation was used, and what evidence remains available. DAIMO addresses this by connecting the model to service metadata, implementation metadata, execution traces, and audit artifacts.`

### Starter evaluation paragraph

`The third task is comparative evaluation. In DAIMO, model scores are only meaningful when linked to an explicit evaluation context specifying dataset, dataset version, protocol, and seed. This makes it possible to distinguish contextualized ranking from unsupported comparison. By linking evaluations to reproducibility artifacts such as notebooks and result tables, the ontology also supports inspection of how comparative claims are backed by executable evidence.`

### How to strengthen this section

- If possible, replace the synthetic domain with real metadata or a partially real case.
- If you must keep the current example, say clearly that it is a demonstrator case and not a user study.

## Section 7. Validation

### What this section must do

- Separate internal validity from external validity.
- Show what was checked, how, and with what result.
- Be honest about what is still missing.

### Recommended subsections

1. Validation strategy
2. Competency-question validation
3. SHACL validation
4. Artifact and structural validation
5. External validation or adoption-oriented assessment

### Starter validation-strategy paragraph

`Validation was designed as a multi-layer process because no single evaluation method is sufficient for an ontology intended for operational use. DAIMO was therefore assessed through executable competency-question queries, structural validation using SHACL, artifact-level checks for reproducibility support, and, where available, external feedback on adequacy and usability. This combination aims to distinguish internal consistency from task-level usefulness.`

### Starter CQ paragraph

`The competency questions were operationalized as SPARQL queries over the example knowledge graph. This serves as a direct test of whether the ontology supports the intended information needs. Rather than treating competency questions as an informal appendix, the paper uses them as executable validation targets linked to the requirements established earlier.`

### Starter SHACL paragraph

`SHACL provides the structural validation layer of the artifact. The shapes enforce minimum completeness requirements for the main resources used in the case study, including published models, access services, interface contracts, executions, evaluation contexts, and supporting artifacts. This matters because the case graph should not merely illustrate the ontology; it should also conform to the structural assumptions underlying the operational claims of the paper.`

### Starter external-validation paragraph

Use one of these depending on what you have.

If you only have a limited external signal:

`External validation is currently lighter than the executable validation layers and should be interpreted accordingly. At this stage, the main purpose of the paper is to establish the ontology's operational scope and internal adequacy. A fuller assessment with domain experts and infrastructure stakeholders remains an important next step, especially to test whether the modeled information can be produced and maintained in realistic data-space workflows.`

If you can add expert input:

`To complement executable validation, the ontology was also reviewed with domain and infrastructure stakeholders. The purpose of this assessment was not to replace formal validation, but to test whether the abstraction level of DAIMO is meaningful in practice and whether the required metadata is realistic for providers, platform operators, and governance actors.`

### Important revision point

You currently define 19 CQs but validate 14. In the rewrite, address this directly with a short paragraph:

`Not all competency questions are currently executable. The remaining questions concern richer notions of compatibility, deployment viability, variant lineage, and minimum publication evidence. These questions were retained because they define important parts of the intended scope, but they require either richer semantics or additional graph data beyond the current iteration of the artifact.`

### Suggested table

Columns:

- Validation layer
- Target
- Method
- Evidence
- Result
- Limitation

## Section 8. Discussion and Limitations

### What this section must do

- Say what DAIMO is good for.
- Say what DAIMO does not yet do.
- Prevent over-reading of your claims.

### Starter first paragraph

`DAIMO's main contribution is not a new standalone theory of AI models, but an ontology-level integration pattern for governed model exchange in data spaces. Its value is strongest where publication metadata, policy constraints, invocation details, execution evidence, and evaluation context must be connected across organizational boundaries. In such settings, DAIMO can serve as a semantic integration layer between existing catalog, provenance, and ML metadata resources.`

### Starter limitation paragraph

`Several limitations remain. The current interface-contract model is still relatively coarse and does not yet support rich semantic compatibility checking. Runtime requirements are sufficient for basic operational description but not for full deployment reasoning. Evaluation contexts support contextualized comparison, but not yet complex benchmarking regimes with heterogeneous protocols and composite measures. Most importantly, external validation with domain experts and real infrastructures is not yet as strong as the internal executable validation package.`

### What to avoid

- Repeating the whole contribution again.
- Treating future work as proof that the current ontology already solves those problems.

## Section 9. Availability and Reuse

### What this section must do

- Tell reviewers exactly what is available.
- Show that the ontology is a reusable artifact, not only a paper result.

### Starter paragraph

`DAIMO is released as a research artifact package containing the ontology specification, SHACL shapes, example knowledge graph, competency-question queries, and supporting reproducibility materials. Persistent namespace design is separated from local implementation details to support stable reuse. The artifact package is intended to make both the semantic model and its validation workflow inspectable and repeatable by other researchers and practitioners.`

### Add concrete details if you have them

- repository URL
- persistent namespace
- version number
- license
- HTML documentation URL
- example files
- query directory
- validation script entry point

### Important honesty rule

Only claim public reuse readiness if the artifact is actually public and documented.

## Section 10. Conclusion

### What this section must do

- Restate the contribution tightly.
- End with a realistic future-work statement.

### Starter conclusion paragraph

`This paper presented DAIMO, an ontology for governed AI model assets in data spaces. DAIMO connects catalog publication, policy-aware discovery, controlled invocation, execution traceability, and contextualized evaluation through a reuse-first semantic design. The paper contributes both the ontology and an executable validation package intended to test whether the targeted operational questions can be answered over graph data rather than asserted only conceptually.`

### Starter future-work paragraph

`Future work should focus on richer semantic compatibility modeling for interface contracts, stronger representation of deployment and benchmarking conditions, broader validation with domain and infrastructure stakeholders, and public release of mature documentation and long-term reusable artifacts. These extensions would strengthen DAIMO from a validated research prototype into a more deployable integration layer for governed model exchange.`

## Figures you should add

Add at least these three figures to the rewritten paper:

1. `Problem-to-ontology figure`
- actors
- lifecycle stages
- information handoffs
- where DAIMO intervenes

2. `Ontology module figure`
- core DAIMO classes
- reused vocabularies
- main relations

3. `Worked example graph`
- one model
- one access service
- one policy
- one run
- one evaluation context
- one audit artifact
- one reproducibility artifact

Without these, the paper risks reading like a list of tables.

## Tables you should keep or revise

- Keep a compact related-work gap table.
- Keep an actor-to-CQ table.
- Keep a core-classes table, but shorten it.
- Keep a validation summary table.

Do not let tables replace the actual explanation.

## Paragraphs to remove or compress from the current draft

- repeated claims that DAIMO "addresses the gap"
- repeated claims that the work is not only conceptual
- repeated summaries of the same contributions in introduction, discussion, and conclusion
- long prose around reproducibility if the artifact details can be stated more directly

## What reviewers are likely to ask unless you answer it first

- Why is this an ontology and not just a metadata profile or graph schema?
- Why is `daimo:Model` a subclass of `dcat:Dataset`?
- What exactly can DAIMO express that a DCAT + ODRL + PROV-O + ML-Schema combination cannot?
- Where did the requirements come from?
- Is the example realistic enough to support the claims?
- Who would adopt this ontology, and with what data source?
- What remains unvalidated externally?

Make the paper answer these questions before the reviewer has to ask them.

## Fast rewrite order

If you rewrite in phases, use this order:

1. Rewrite Introduction
2. Rewrite Requirements and CQs
3. Rewrite Method section
4. Expand Ontology Design with figures and worked example
5. Rebuild Case Study around the running scenario
6. Reframe Validation
7. Compress Discussion and Conclusion
8. Finalize Availability section

## Optional contribution statement for the end of the introduction

You can use this almost verbatim if it matches the final paper:

`In summary, the paper contributes a requirements-driven ontology for governed AI model assets in data spaces, an explicit reuse and alignment strategy across catalog, policy, provenance, and ML vocabularies, a case-study-based demonstration of publication-to-evaluation support, and an executable validation package combining SHACL constraints, competency-question queries, and reproducibility materials.`

## Final advice for the rewrite

The strongest version of this paper will read less like "here is our ontology and here are its terms" and more like "here is a concrete governed model-exchange problem, here is why existing vocabularies alone do not solve it, here is the ontology design that closes the gap, and here is the evidence that it works for the targeted tasks."
