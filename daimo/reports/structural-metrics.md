# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `daimo/.venv/bin/python -c '<rdflib counts over core/examples/shapes>'`
- Started (UTC): 2026-09-06T11:52:46Z
- Finished (UTC): 2026-09-06T11:52:47Z
- Working-tree status (`git status -sb`): `## main...origin/main
 M daimo/reports/negative-test-results.md
 M daimo/reports/random-seed-test-results.md
 M daimo/reports/reasoner-report.md
 M daimo/reports/reused-class-scope-results.md
 M daimo/reports/validation-results.md
?? daimo/reports/_eval_runner.py
?? daimo/reports/checksums-protected-before.json
?? daimo/reports/checksums-protected-before.md
?? daimo/reports/serialization-test-results.md
?? paper/DAIMO_PAPER.pdf
?? paper/DAIMO_v1.pdf
?? "paper/daimo-paper-es-v4 - copia.pdf:Zone.Identifier"
?? paper/daimo-paper-es-v4-1col.pdf
?? paper/fix_vertical_spacing.py
?? paper/sync_sage_editorial.py`
- Python: Python 3.10.12 (`daimo/.venv/bin/python`)
- Java: openjdk version "21.0.11" 2026-04-21 (exit 0)
- Relevant Python packages:
- rdflib==7.6.0
- pyshacl==0.31.0
- owlrl==7.6.1
- owlready2==0.51
- Process exit code: 0
- Harness verdict: **PASS**

Saving this file in a later git commit does **not** mean the tests evaluated
that later commit. The evaluated content is `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`.

---

METHOD
rdflib parse of Turtle sources (same loader style as validate.py).
Class/property counts: subjects in daimo-core.ttl with the given owl: type
and IRI prefix https://w3id.org/pionera/daimo#
Native = object properties union datatype properties.
Example triples: len(examples/*.ttl). Shape triples: len(shapes/*.ttl).
validate.py ontology triples = core+alignment.
---
core_triples 393
align_triples 238
ontology_triples_core_plus_align 620
shape_triples 386
example_triples 233
daimo_classes 14
object_properties 31
datatype_properties 8
native_properties 39
functional_properties 29
asymmetric_properties 7
CLASS_IRIS
https://w3id.org/pionera/daimo#AIAssetOffering
https://w3id.org/pionera/daimo#AuditEvidence
https://w3id.org/pionera/daimo#CrossParticipantProvenanceRecord
https://w3id.org/pionera/daimo#DerivedArtifact
https://w3id.org/pionera/daimo#Evaluator
https://w3id.org/pionera/daimo#ExecutionAuthorization
https://w3id.org/pionera/daimo#GovernanceActor
https://w3id.org/pionera/daimo#IOContract
https://w3id.org/pionera/daimo#ModelConsumer
https://w3id.org/pionera/daimo#ModelDeployment
https://w3id.org/pionera/daimo#ModelProvider
https://w3id.org/pionera/daimo#ParticipantRole
https://w3id.org/pionera/daimo#PlatformOperator
https://w3id.org/pionera/daimo#SharedEvaluationContext
OP_IRIS
https://w3id.org/pionera/daimo#authorizedBy
https://w3id.org/pionera/daimo#authorizesRun
https://w3id.org/pionera/daimo#contextDataset
https://w3id.org/pionera/daimo#contextFlow
https://w3id.org/pionera/daimo#contextTask
https://w3id.org/pionera/daimo#deploysModel
https://w3id.org/pionera/daimo#derivedFromAgreement
https://w3id.org/pionera/daimo#derivedFromRun
https://w3id.org/pionera/daimo#evidenceOf
https://w3id.org/pionera/daimo#exposedAs
https://w3id.org/pionera/daimo#forService
https://w3id.org/pionera/daimo#grantedTo
https://w3id.org/pionera/daimo#hasAuditEvidence
https://w3id.org/pionera/daimo#hasDeployment
https://w3id.org/pionera/daimo#hasDerivedArtifact
https://w3id.org/pionera/daimo#hasIOContract
https://w3id.org/pionera/daimo#hasOfferPolicy
https://w3id.org/pionera/daimo#hasOffering
https://w3id.org/pionera/daimo#hasRole
https://w3id.org/pionera/daimo#inParticipantContext
https://w3id.org/pionera/daimo#inputSchema
https://w3id.org/pionera/daimo#integrityHash
https://w3id.org/pionera/daimo#offeredBy
https://w3id.org/pionera/daimo#offersModel
https://w3id.org/pionera/daimo#onInfrastructure
https://w3id.org/pionera/daimo#outputSchema
https://w3id.org/pionera/daimo#records
https://w3id.org/pionera/daimo#signedBy
https://w3id.org/pionera/daimo#spansParticipantContext
https://w3id.org/pionera/daimo#underAuthorization
https://w3id.org/pionera/daimo#usesEvaluationContext
DP_IRIS
https://w3id.org/pionera/daimo#authMethod
https://w3id.org/pionera/daimo#datasetVersion
https://w3id.org/pionera/daimo#expiresAt
https://w3id.org/pionera/daimo#inputFormat
https://w3id.org/pionera/daimo#outputFormat
https://w3id.org/pionera/daimo#protocol
https://w3id.org/pionera/daimo#randomSeed
https://w3id.org/pionera/daimo#recordedAt
