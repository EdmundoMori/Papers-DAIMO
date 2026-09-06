# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `daimo/.venv/bin/python reasoner_check.py`
- First captured run (UTC): started 2026-09-06T11:52:35Z, finished 2026-09-06T11:52:37Z, exit 0, HermiT 1.38 s
- Native markdown body below: same command re-run on the same commit in this session so the file written by `reasoner_check.py` (superclass list included) is conserved. HermiT time in this body: 1.62 s
- Python: Python 3.10.12 (`daimo/.venv/bin/python`)
- Java: openjdk version "21.0.11" 2026-04-21 (HermiT via owlready2 0.51)
- Relevant Python packages: rdflib==7.6.0, owlrl==7.6.1, owlready2==0.51
- Process exit code: 0
- Harness verdict: **PASS**

Saving this file in a later git commit does **not** mean the tests evaluated
that later commit. The evaluated content is `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`.

---

# DAIMO Reasoner Report

## HermiT (owlready2)

- consistent: **True**
- reasoning time: 1.62 s
- unsatisfiable classes: 0

## OWL-RL (pure Python)

- pre triples: 853
- post triples: 2048
- materialised: 1195
- reasoning time: 0.57 s
- owl:Nothing individuals (disjoint-class violations): 0
- unsatisfiable subclasses: 0

## Entailment-verification check

For each DAIMO-native class, lists every superclass entailed after OWL-RL materialisation. Catches silent inference bugs that HermiT and SHACL both miss (they would only surface if the ontology also asserted disjointness with the wrong class).

- DAIMO classes inspected: 14
- forbidden-entailment warnings: **0**

### Inferred superclasses per DAIMO class

- `daimo:AIAssetOffering` ⊑ Thing, CatalogRecord
- `daimo:AuditEvidence` ⊑ Thing, Entity
- `daimo:CrossParticipantProvenanceRecord` ⊑ Thing, Bundle
- `daimo:DerivedArtifact` ⊑ Thing, Resource, Entity
- `daimo:Evaluator` ⊑ Thing, Role, ParticipantRole
- `daimo:ExecutionAuthorization` ⊑ Thing, Entity
- `daimo:GovernanceActor` ⊑ Thing, Role, ParticipantRole
- `daimo:IOContract` ⊑ Thing
- `daimo:ModelConsumer` ⊑ Thing, Role, ParticipantRole
- `daimo:ModelDeployment` ⊑ Thing, Entity
- `daimo:ModelProvider` ⊑ Thing, Role, ParticipantRole
- `daimo:ParticipantRole` ⊑ Thing, Role
- `daimo:PlatformOperator` ⊑ Thing, Role, ParticipantRole
- `daimo:SharedEvaluationContext` ⊑ Thing

## Verdict

**CONSISTENT**