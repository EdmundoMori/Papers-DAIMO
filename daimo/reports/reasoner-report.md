# DAIMO Reasoner Report

## HermiT (owlready2)

- consistent: **True**
- reasoning time: 0.72 s
- unsatisfiable classes: 0

## OWL-RL (pure Python)

- pre triples: 817
- post triples: 1988
- materialised: 1171
- reasoning time: 0.27 s
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
- `daimo:ExecutionAuthorization` ⊑ Thing, Agreement
- `daimo:GovernanceActor` ⊑ Thing, Role, ParticipantRole
- `daimo:IOContract` ⊑ Thing
- `daimo:ModelConsumer` ⊑ Thing, Role, ParticipantRole
- `daimo:ModelDeployment` ⊑ Thing, Entity
- `daimo:ModelProvider` ⊑ Thing, Role, ParticipantRole
- `daimo:ParticipantRole` ⊑ Thing, Role
- `daimo:PlatformOperator` ⊑ Thing, Ro========================================================================
DAIMO reasoner consistency check
========================================================================
Merged graph: 817 triples

[1/2] HermiT via owlready2 ...
  consistent           : True
  reasoning time (s)   : 0.72
  unsatisfiable classes: 0

[2/3] OWL-RL (pure Python) ...
  pre triples          : 817
  post triples         : 1988
  materialised         : 1171
  reasoning time (s)   : 0.27
  owl:Nothing individuals: 0
  unsat subclasses       : 0

[3/3] Entailment-verification check ...
  DAIMO classes inspected: 14
  forbidden-entailment warnings: 0

========================================================================
Report saved to reports/reasoner-report.md
Exit code: 0
========================================================================
