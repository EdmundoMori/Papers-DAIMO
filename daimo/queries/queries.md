# DAIMO SPARQL Query Suite

One query per CQ. Each query is runnable against the example KG in
`examples/flood-risk-scenario.ttl` with the DAIMO ontology + alignment loaded.

Standard PREFIX block (prepend to any individual query when splitting into .rq files):

```sparql
PREFIX daimo: <https://w3id.org/pionera/daimo#>
PREFIX dcat:  <http://www.w3.org/ns/dcat#>
PREFIX dct:   <http://purl.org/dc/terms/>
PREFIX it6:   <http://data.europa.eu/it6/>
PREFIX mls:   <http://www.w3.org/ns/mls#>
PREFIX odrl:  <http://www.w3.org/ns/odrl/2/>
PREFIX prov:  <http://www.w3.org/ns/prov#>
PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
PREFIX edc:   <https://w3id.org/edc/v0.0.1/ns/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:   <http://www.w3.org/2001/XMLSchema#>
```

---

## R — Registration and Publication

### CQ-R1 — Which AI models has a given provider published as governed catalog assets?

```sparql
SELECT ?model ?title WHERE {
  ?offering a daimo:AIAssetOffering ;
            daimo:offeredBy ?provider ;
            daimo:offersModel ?model .
  ?model dct:title ?title .
  FILTER (?provider = <https://example.org/daimo-scenario/upm>)
}
```

### CQ-R2 — For a given model, which catalog offering registered it, by which publisher, and when?

Exercises the subproperty entailment `daimo:offersModel ⊑ foaf:primaryTopic`,
letting the query reach the offering via the DCAT-native property without
knowing the DAIMO property. The offering agent is retrieved via the native
`daimo:offeredBy` because on a dcat:CatalogRecord `dct:publisher` denotes the
catalog maintainer (not the model author) — so we deliberately don't alias.

```sparql
SELECT ?offering ?provider ?issued WHERE {
  ?offering foaf:primaryTopic <https://example.org/daimo-scenario/flood-risk-v2> ;
            daimo:offeredBy ?provider ;
            dct:issued ?issued .
}
```

### CQ-R3 — Licence and usage policy of a model.

```sparql
SELECT ?model ?policy ?policyTitle WHERE {
  ?model a it6:MachineLearningModel ;
         odrl:hasPolicy ?policy .
  OPTIONAL { ?policy dct:title ?policyTitle }
  FILTER (?model = <https://example.org/daimo-scenario/flood-risk-v2>)
}
```

### CQ-R4 — I/O contract for the invocation interface of a published model.

Each I/O contract is resolved to the concrete service (interface) it applies to
via `daimo:forService`, so the result is one row per endpoint (REST, gRPC, …)
with the exact input/output format and authentication of that interface — never
a cartesian mix across interfaces.

```sparql
SELECT ?model ?service ?in ?out ?auth WHERE {
  ?deployment a daimo:ModelDeployment ;
              daimo:deploysModel ?model ;
              daimo:hasIOContract ?contract .
  ?contract daimo:forService ?service ;
            daimo:inputFormat ?in ;
            daimo:outputFormat ?out ;
            daimo:authMethod ?auth .
}
```

### CQ-R5 — For each offering, what concrete participant-role subclass does the providing agent hold?

Uses the class hierarchy (`rdfs:subClassOf*`) rather than a string-prefix filter, so the query
remains correct under any namespace change and under any future subclass of
`daimo:ParticipantRole`.

```sparql
SELECT DISTINCT ?agent ?roleClass WHERE {
  ?offering a daimo:AIAssetOffering ;
            daimo:offeredBy ?agent .
  ?agent daimo:hasRole ?role .
  ?role a ?roleClass .
  ?roleClass rdfs:subClassOf+ daimo:ParticipantRole .
}
```

---

## D — Discovery and Selection

### CQ-D1 — Which models solve a given task in a given application domain?

```sparql
SELECT ?model ?title WHERE {
  ?model a it6:MachineLearningModel ;
         dct:title ?title ;
         it6:hasTask <https://example.org/daimo-scenario/flood-risk-task> .
}
```

### CQ-D2 — Which of those models are usable under a non-commercial policy pattern?

```sparql
SELECT ?model ?title WHERE {
  ?model a it6:MachineLearningModel ;
         dct:title ?title ;
         odrl:hasPolicy ?policy .
  FILTER NOT EXISTS {
    ?policy odrl:prohibition ?p .
    ?p odrl:action odrl:commercialize .
  }
}
```

### CQ-D3 — Which models expose a service endpoint, and what authentication method does each require?

Returns all (model, endpoint, auth-method) tuples so the consumer can filter
client-side. No hard-coded authentication string. The contract is bound to its
endpoint through `daimo:forService`, so each endpoint is paired only with *its
own* authentication method — a deployment exposing a REST and a gRPC endpoint
returns exactly two rows, not the four combinations produced by an independent
service × contract join.

```sparql
SELECT ?model ?endpoint ?auth WHERE {
  ?deployment daimo:deploysModel ?model ;
              daimo:exposedAs ?service ;
              daimo:hasIOContract ?contract .
  ?contract daimo:forService ?service ;
            daimo:authMethod ?auth .
  ?service dcat:endpointURL ?endpoint .
}
```

### CQ-D4 — Models reaching a minimum metric threshold under a shared evaluation context.

```sparql
SELECT ?model ?value WHERE {
  ?eval a it6:Evaluation ;
        it6:evaluates ?model ;
        daimo:usesEvaluationContext <https://example.org/daimo-scenario/evalctx-climatebench-v1-2026-1-holdout> ;
        it6:hasEvaluationMeasure ?m .
  ?m it6:hasValue ?value .
  FILTER (?value >= 0.85)
}
```

---

## E — Execution and Auditability

### CQ-E1 — For a given catalog offering, what service endpoint, authentication, and I/O contract apply to invoking the underlying model?

Starts from an `AIAssetOffering` and reaches the deployment via the entailed
`foaf:primaryTopic` link (from `daimo:offersModel ⊑ foaf:primaryTopic`). The query
therefore tests the *reuse* of DCAT semantics end-to-end. The contract is joined
to its endpoint through `daimo:forService`, so each row describes one real
endpoint with its correct format and authentication — no cartesian mix.

```sparql
SELECT ?endpoint ?auth ?in ?out WHERE {
  <https://example.org/daimo-scenario/offering-flood-v2>
      foaf:primaryTopic ?model .
  ?deployment daimo:deploysModel ?model ;
              daimo:exposedAs ?service ;
              daimo:hasIOContract ?contract .
  ?contract daimo:forService ?service ;
            daimo:authMethod ?auth ;
            daimo:inputFormat ?in ;
            daimo:outputFormat ?out .
  ?service dcat:endpointURL ?endpoint .
}
```

### CQ-E2 — For a given model deployment, which runs have been executed, by which agents, and under which execution authorization?

Parametrised on a specific deployment. Traverses deployment → model → run, plus joins to
the authorization that permitted each run. Unaffected by DAIMO-ISSUE-02: the query
reaches the authorization through `daimo:authorizesRun`/`daimo:grantedTo`, which still
live on `daimo:ExecutionAuthorization`; the accepted `odrl:Agreement` is now a separate
individual reachable via `daimo:derivedFromAgreement` (see CQ-G3) when needed.

```sparql
SELECT ?run ?agent ?auth WHERE {
  <https://example.org/daimo-scenario/deployment-flood-v2>
      daimo:deploysModel ?model .
  ?run a it6:Run ;
       mls:realizes ?algo ;
       prov:wasAssociatedWith ?agent .
  ?auth a daimo:ExecutionAuthorization ;
        daimo:authorizesRun ?run ;
        daimo:grantedTo ?agent .
}
```

### CQ-E3 — Implementation, algorithm, flow, and compute infrastructure used in a run.

```sparql
SELECT ?run ?algo ?flow ?infra WHERE {
  ?run a it6:Run ;
       mls:realizes ?algo ;
       it6:hasFlow ?flow ;
       it6:runnedOn ?infra .
}
```

### CQ-E4 — Audit evidence (hash, signer, timestamp) supporting a given run.

```sparql
SELECT ?run ?hash ?signer ?ts WHERE {
  ?evidence a daimo:AuditEvidence ;
            daimo:evidenceOf ?run ;
            daimo:integrityHash ?hash ;
            daimo:signedBy ?signer ;
            daimo:recordedAt ?ts .
}
```

### CQ-E5 — Derived artifacts produced by a run, and under which authorization.

Unaffected by DAIMO-ISSUE-02: `daimo:underAuthorization` still points to a
`daimo:ExecutionAuthorization`; the accepted `odrl:Agreement` behind it is reachable
via `?auth daimo:derivedFromAgreement ?agreement` if the agreement is also required.

```sparql
SELECT ?artifact ?title ?auth WHERE {
  ?artifact a daimo:DerivedArtifact ;
            dct:title ?title ;
            daimo:derivedFromRun ?run ;
            daimo:underAuthorization ?auth .
}
```

---

## V — Evaluation and Reproducibility

### CQ-V1 — Shared evaluation context of a given evaluation.

Returns task, dataset, version, protocol and, when applicable, random seed.
`daimo:randomSeed` is `OPTIONAL`: a valid deterministic context (no seed) still
answers the question; `?seed` is then unbound. Presence of a seed is a property
of the evaluation procedure, not a DAIMO-wide obligation (DAIMO-ISSUE-03).

```sparql
SELECT ?task ?dataset ?version ?protocol ?seed WHERE {
  <https://example.org/daimo-scenario/eval-flood-v2>
      daimo:usesEvaluationContext ?ctx .
  ?ctx daimo:contextTask    ?task ;
       daimo:contextDataset ?dataset ;
       daimo:datasetVersion ?version ;
       daimo:protocol       ?protocol .
  OPTIONAL { ?ctx daimo:randomSeed ?seed }
}
```

### CQ-V2 — Under a shared evaluation context, highest-scoring model for a metric.

Joins evaluations that share the **same context individual** and a metric value.
Does **not** require `daimo:randomSeed`: a seedless (deterministic) context is
still a valid grouping for ranking. Comparability also requires the same metric
and compatible conditions; sharing a context IRI is not by itself a complete
reproducibility claim.

```sparql
SELECT ?model ?value WHERE {
  ?eval a it6:Evaluation ;
        it6:evaluates ?model ;
        daimo:usesEvaluationContext <https://example.org/daimo-scenario/evalctx-climatebench-v1-2026-1-holdout> ;
        it6:hasEvaluationMeasure ?m .
  ?m it6:hasValue ?value .
}
ORDER BY DESC(?value)
LIMIT 1
```

### CQ-V3 — Ranking of models under the same evaluation context and metric.

Same join as CQ-V2 without `LIMIT 1`. Seed is not in the pattern, so evaluations
under a seedless context are not excluded.

```sparql
SELECT ?model ?value WHERE {
  ?eval a it6:Evaluation ;
        it6:evaluates ?model ;
        daimo:usesEvaluationContext <https://example.org/daimo-scenario/evalctx-climatebench-v1-2026-1-holdout> ;
        it6:hasEvaluationMeasure ?m .
  ?m it6:hasValue ?value .
}
ORDER BY DESC(?value)
```

### CQ-V4 — For a given model, which benchmark suites has it been evaluated on?

Parametrised on a specific model (previously returned all model-benchmark pairs regardless).

```sparql
SELECT DISTINCT ?benchmark ?benchmarkTitle WHERE {
  <https://example.org/daimo-scenario/flood-risk-v2>
      it6:hasBenchmark ?benchmark .
  OPTIONAL { ?benchmark dct:title ?benchmarkTitle }
}
```

### CQ-V5 — Reproducibility artefacts backing an evaluation.

```sparql
SELECT ?eval ?flow ?flowVersion ?run ?runStart WHERE {
  ?eval a it6:Evaluation ;
        it6:evaluates ?model ;
        daimo:usesEvaluationContext ?ctx .
  ?ctx daimo:contextFlow ?flow .
  OPTIONAL { ?flow dct:hasVersion ?flowVersion }
  OPTIONAL {
    ?run a it6:Run ;
         mls:realizes ?algo ;
         prov:startedAtTime ?runStart .
  }
}
```

---

## G — Governance Bridge (new CQs enabled by DAIMO)

### CQ-G1 — Offerings that include a given model.

```sparql
SELECT ?offering ?title ?provider WHERE {
  ?offering a daimo:AIAssetOffering ;
            daimo:offersModel <https://example.org/daimo-scenario/flood-risk-v2> ;
            dct:title ?title ;
            daimo:offeredBy ?provider .
}
```

### CQ-G2 — Deployments serving a model, with infrastructure, service, and I/O contract.

Keeps the deployment → infrastructure → service → contract chain intact: each
contract is tied to its `dcat:DataService` through `daimo:forService`, so the
row reports the endpoint together with the format and authentication that apply
to *that* endpoint.

```sparql
SELECT ?deployment ?infra ?service ?in ?out ?auth WHERE {
  ?deployment a daimo:ModelDeployment ;
              daimo:deploysModel <https://example.org/daimo-scenario/flood-risk-v2> ;
              daimo:onInfrastructure ?infra ;
              daimo:hasIOContract ?contract .
  ?contract daimo:forService ?service ;
            daimo:inputFormat ?in ;
            daimo:outputFormat ?out ;
            daimo:authMethod ?auth .
}
```

### CQ-G3 — Which execution authorization, and the ODRL agreement it derives from, authorised a specific run?

DAIMO keeps the accepted `odrl:Agreement` and the `daimo:ExecutionAuthorization`
as two **distinct individuals** (DAIMO-ISSUE-02). The authorization records which
runs an accepted agreement covers, for which grantee, and until when. This query
returns **both** resources, proves they are different (`FILTER(?auth != ?agreement)`),
retrieves the grantee and expiry, and confirms the grantee is the agreement's
`odrl:assignee` — the coherence SHACL invariant INV-9 enforces.

```sparql
SELECT ?auth ?agreement ?grantee ?expires WHERE {
  ?auth a daimo:ExecutionAuthorization ;
        daimo:authorizesRun <https://example.org/daimo-scenario/run-2026-04-20-legs> ;
        daimo:derivedFromAgreement ?agreement ;
        daimo:grantedTo ?grantee ;
        daimo:expiresAt ?expires .
  ?agreement a odrl:Agreement ;
             odrl:assignee ?grantee .
  FILTER (?auth != ?agreement)
}
```

### CQ-G4 — Full provenance bundle for a derived artifact across participant contexts.

Aggregates per bundle with `GROUP_CONCAT` so one conceptual bundle returns one row,
not a cartesian product of `(context × activity)` combinations.

```sparql
SELECT ?bundle
       (GROUP_CONCAT(DISTINCT STR(?ctx); SEPARATOR=", ") AS ?contexts)
       (GROUP_CONCAT(DISTINCT STR(?activity); SEPARATOR=", ") AS ?activities)
WHERE {
  <https://example.org/daimo-scenario/prediction-legs-2026-04-20>
      daimo:derivedFromRun ?run .
  ?bundle a daimo:CrossParticipantProvenanceRecord ;
          daimo:records ?run ;
          daimo:records ?activity ;
          daimo:spansParticipantContext ?ctx .
}
GROUP BY ?bundle
```
