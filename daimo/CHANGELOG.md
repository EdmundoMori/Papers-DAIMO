# Changelog

All notable changes to DAIMO are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and DAIMO adheres
to semantic versioning (`owl:versionInfo` mirrors this file).

## [Unreleased]

### Fixed — DAIMO-ISSUE-04: SHACL targets for reused classes
- `OfferInDAIMOShape`, `MachineLearningModelInDAIMOShape` and `RunInDAIMOShape`
  used `sh:targetClass` on `odrl:Offer`, `it6:MachineLearningModel` and
  `it6:Run`, so **every** instance in a graph received DAIMO profile
  obligations, including resources not linked by DAIMO. Documentation claimed
  the rules applied "in DAIMO's context"; the targets did not.

### Changed — DAIMO-ISSUE-04
- Replaced the three global `sh:targetClass` with SHACL Core
  `sh:targetObjectsOf`: `hasOfferPolicy` (Offer); `offersModel` **or**
  `deploysModel` (Model); `authorizesRun` **or** `derivedFromRun` (Run).
- The same leak applied to `AgreementInDAIMOShape` (`sh:targetClass
  odrl:Agreement`); it now targets objects of `daimo:derivedFromAgreement`.
  Internal obligations (assigner/target, title/identifier/policy, flow/
  algorithm/agent/start, permission/assignee) are unchanged.
- New harness `python tests/reused_class_scope_test.py` (9-cell matrix):
  external incomplete Offer/Model/Run are not selected; in-scope incomplete
  resources violate; in-scope complete resources conform.
- SHACL still validates RDF graphs only; it does not apply ODRL policies or
  control access.

### Fixed — DAIMO-ISSUE-03: optional random seed when applicable
- `SharedEvaluationContextShape` required `daimo:randomSeed` with `sh:minCount 1`,
  forcing a seed even for deterministic protocols. The approved CQs ask for
  "protocol and, when applicable, seed". The property is kept (functional,
  `xsd:integer`) but SHACL cardinality is now **0..1**. Applicability depends
  on the evaluation procedure; DAIMO does not maintain a universal list of
  stochastic protocols. Absence of a seed is not a claim of complete
  reproducibility.

### Changed — DAIMO-ISSUE-03
- `daimo:randomSeed` definition/comment: fixes stochastic components *when the
  protocol uses them*; still functional (one seed per context).
- `SharedEvaluationContext` definition no longer treats the seed as one of five
  always-required facets.
- CQ-V1 uses `OPTIONAL { ?ctx daimo:randomSeed ?seed }`. CQ-V2/CQ-V3 already
  joined only on the context individual and metric; documented as seed-independent.
- New harness `python tests/random_seed_test.py`: seedless context conforms and
  is recovered by CQ-V1 with `?seed` unbound; two seeds and a non-integer seed
  are rejected.
- Flood-risk example keeps seed 42 (holdout uses it). Benchmark generator still
  emits a seed for its synthetic holdout; it no longer treats the property as
  mandatory for conformance.

### Fixed — DAIMO-ISSUE-02: separation of execution authorization and ODRL agreement
- `daimo:ExecutionAuthorization` was a **subclass of `odrl:Agreement`** and the
  flood-risk example used a **single individual** as both the accepted agreement
  and the execution authorization. CQ-G3 asked for "the authorization and the
  agreement it derives from" but no property related the two, and the query only
  returned the authorization. This conflated two distinct governance resources.

### Added — DAIMO-ISSUE-02
- **`daimo:derivedFromAgreement`** object property
  (`ExecutionAuthorization → odrl:Agreement`), **functional** (each authorization
  derives from exactly one agreement) and **asymmetric**. Documented as **not
  aligned** to any external term in `alignment.ttl` (`prov:wasDerivedFrom` was
  considered and rejected — generic entity lineage that would force every
  agreement into `prov:Entity` and lose the governance meaning).
- **`daimo:AgreementInDAIMOShape`** conformance shape over `odrl:Agreement`
  (requires `odrl:permission` ≥1 and `odrl:assignee` ≥1).
- **INV-9** (`AuthorizationAgreementAssigneeInvariant`): the authorization's
  `daimo:grantedTo` grantee must be an `odrl:assignee` of the `odrl:Agreement`
  it `daimo:derivedFromAgreement`.
- Three new negative-test cases: `bad:INV9-auth` (grantee ≠ agreement assignee),
  `bad:AUTH-no-agreement` (authorization without a source agreement), and
  `bad:AUTH-bad-agreement` (source agreement missing `odrl:permission`). The
  negative harness now asserts **all 11** invariant/completeness rules fire
  (INV-1..INV-9 + the two authorization/agreement per-class rules).
- `validate.py` now runs a structural check that at least one
  `ExecutionAuthorization`/`odrl:Agreement` pair exists with distinct IRIs
  (`FILTER(?auth != ?agreement)`).
- `reasoner_check.py` `FORBIDDEN_SUPERS` extended with `odrl:Agreement` and
  `odrl:Policy` so any regression that re-types the authorization as an ODRL
  policy/agreement is caught.

### Changed — DAIMO-ISSUE-02
- `daimo:ExecutionAuthorization` is now aligned to **`prov:Entity`** (a governed
  artefact), **not** to `odrl:Agreement`. Its definition/comment were rewritten.
- `daimo:grantedTo` is **no longer** `rdfs:subPropertyOf odrl:assignee`
  (odrl:assignee's domain `odrl:Policy` would re-type the authorization as a
  policy). The grantee = agreement-assignee equivalence is enforced by INV-9.
- `ExecutionAuthorizationShape` now requires `daimo:derivedFromAgreement`
  (1..1, `odrl:Agreement`) and no longer requires `odrl:permission` on the
  authorization; the ODRL permissions live on the agreement.
- Example KG: the accepted agreement (`ex:agreement-municipality-flood-v2`,
  `odrl:Agreement`) and the authorization (`ex:authorization-municipality-flood-v2`,
  `daimo:ExecutionAuthorization`) are now distinct individuals linked by
  `daimo:derivedFromAgreement`; the provenance chain is preserved.
- CQ-G3 rewritten to return `?auth`, `?agreement`, `?grantee`, `?expires`, prove
  the two resources differ, and check the grantee against the agreement assignee.
  CQ-E2/CQ-E5 reviewed — unaffected.
- `scalability_benchmark.py` generates a distinct `odrl:Agreement` per unit and
  links each synthetic authorization to it via `derivedFromAgreement`; added an
  `auth_agreements` control query. Re-ran sizes 100 and 1000 — both still conform.
- Counts updated as technical information: object properties 30 → **31**, total
  native properties 38 → **39**, functional **29** (21 object + 8 datatype
  declarations of `owl:FunctionalProperty`; a naïve grep hits 30 because a
  comment mentions the term), asymmetric 6 → **7**;
  SHACL conformance shapes 3 → **4**; cross-class invariants 8 → **9**; SHACL
  node shapes 20 → **22**.

### Fixed — DAIMO-ISSUE-01: unambiguous DataService–IOContract association
- A `daimo:ModelDeployment` could declare several `daimo:exposedAs` services and
  several `daimo:hasIOContract` contracts with **no link between a specific
  contract and a specific service**. Queries CQ-D3 and CQ-E1 joined services and
  contracts independently, producing a cartesian product (four combinations for
  the two-service / two-contract flood-risk example) and making it impossible to
  determine unambiguously which format and authentication apply to each endpoint.

### Added
- **`daimo:forService`** object property (`IOContract → dcat:DataService`),
  **functional** (a contract describes exactly one service) and **asymmetric**.
  Documented as **not aligned** to any external term in `alignment.ttl`
  (`dcat:endpointDescription` was considered and rejected — wrong direction and
  it points to an API-description document, not a structured I/O contract).
- **INV-7** (`DeploymentContractServiceInvariant`): every `hasIOContract`
  contract must `forService` a service the same deployment `exposedAs`.
- **INV-8** (`DeploymentServiceContractInvariant`): every `exposedAs` service
  must have at least one `forService` contract.
- `IOContractShape` now requires `forService` (1..1, `dcat:DataService`).
- Two new negative-test cases (`bad:INV7-deployment`, `bad:INV8-deployment`);
  the negative harness now asserts **all 8 invariants** fire.

### Changed
- Example KG: `ex:flood-risk-iocontract` → `forService ex:flood-risk-service`
  (REST); `ex:flood-risk-iocontract-grpc` → `forService
  ex:flood-risk-service-grpc` (gRPC). Two endpoints, formats and auth preserved.
- SPARQL queries CQ-R4, CQ-D3, CQ-E1, CQ-G2 rewritten to join each contract to
  its service via `daimo:forService`, eliminating the cartesian join. On the
  example, **CQ-D3 and CQ-E1 now return 2 rows instead of 4**.
- `scalability_benchmark.py` generator links every synthetic contract to its
  service via `forService`; the `invocation_contracts` control query uses the
  corrected relation. Re-ran sizes 100 and 1000 — both still conform.
- Counts updated as technical information: object properties 29 → **30**, total
  native properties 37 → **38**; cross-class SHACL invariants 6 → **8**.
- Comments of `ModelDeployment`, `IOContract`, `exposedAs` and `hasIOContract`
  updated to reference the new per-endpoint contract/service pairing.

### Notes
- No version bump, tag, or release in this step. `owl:versionInfo` remains
  `0.1.6`. OOPS! was not re-run (external service unreachable from the execution
  environment); the scan in `reports/oops-report.md` predates `forService`.

## [0.1.6] — 2026-07-06

### Fixed
- Removed the invalid `daimo:datasetVersion rdfs:subPropertyOf dct:hasVersion`
  alignment. `daimo:datasetVersion` is a datatype property carrying a literal
  dataset-version token, while `dct:hasVersion` relates one resource to another
  version resource. Keeping the alignment caused `owlready2` to warn about mixed
  object/datatype-property typing.
- Documented the non-alignment rationale in `alignment.ttl` and the property
  comment in `daimo-core.ttl`.

### Changed
- Version bumped from 0.1.5 to 0.1.6.
- Updated the core and SHACL module metadata to version 0.1.6.
- Added an explicit `owl:versionIRI` and `owl:versionInfo` to the alignment
  module.

## [0.1.5] — 2026-04-23

### Fixed — sixth-pass final audit
- **R-1**: Rewrote the 14 `skos:example` annotations added in v0.1.4.
  The prior versions referenced specific IRIs from the example KG
  (`ex:upm-provider-role`, `flood-risk-v2`, etc.), coupling the class
  definitions to one scenario. Replaced with generic pattern
  descriptions that illustrate each class without naming specific
  individuals — best-practice SKOS use and better for reusers who
  don't care about the flood-risk case.
- **R-6**: Declared `daimo:hasOffering rdfs:subPropertyOf foaf:isPrimaryTopicOf`
  for symmetry with `daimo:offersModel ⊑ foaf:primaryTopic`. Added the
  missing `foaf:isPrimaryTopicOf` external-property declaration (with
  `rdfs:seeAlso` to the FOAF spec) in `alignment.ttl`.
- **R-4**: Verified the `https://w3id.org/dspace/v0.8/` namespace
  resolves via w3id.org to the Eclipse DSP specification repository;
  the `https://w3id.org/dspace/2024/1/` IRI is an alias to the same
  target. Both are valid; the v0.8/ form is preferred because Eclipse
  EDC and related tooling reference it in code. Documented the choice
  as a comment in `alignment.ttl`.

### Changed
- Version bumped from 0.1.4 to 0.1.5 (doc-only + SKOS-quality fixes;
  no TBox changes).

## [0.1.4] — 2026-04-23

### Added — fifth-pass polish pack
- **Ontology-header enrichment**: `dct:creator` with ORCID placeholders,
  `dct:contributor`, `dct:publisher`, `owl:priorVersion`,
  `dct:conformsTo` (OWL 2 DL profile), and `rdfs:seeAlso` links to the
  WIDOCO docs, shapes module, and alignment module.
- **Shapes module header**: `shapes/daimo-shapes.ttl` now declares itself
  as `owl:Ontology` with its own `owl:versionIRI`, creator, license,
  and metadata. Until v0.1.3 the SHACL file had no self-declaration.
- **skos:definition and skos:example** on every DAIMO-native class (14
  classes). Adds intensional definitions and concrete instance examples
  alongside the existing `rdfs:comment`.
- **Named disjointness axiom**: the pairwise-disjointness of the nine
  top-level DAIMO kinds is now named `daimo:TopLevelKindsDisjointness`
  (previously anonymous) with its own `rdfs:label` and `rdfs:comment`.
- **Four inverse properties**: `daimo:hasDeployment` (↔ deploysModel),
  `daimo:hasDerivedArtifact` (↔ derivedFromRun),
  `daimo:hasAuditEvidence` (↔ evidenceOf), `daimo:hasOffering`
  (↔ offersModel). Answers inverse queries natively; reduces
  OOPS! P13 count.
- **Asymmetric declarations**: `daimo:offersModel`, `daimo:deploysModel`,
  `daimo:authorizesRun`, `daimo:derivedFromRun`, and `daimo:evidenceOf`
  are now `owl:AsymmetricProperty`, formally capturing that the
  offering/deployment/authorisation/derivation/evidence relations are
  never reflexive.
- **`rdfs:seeAlso` to source specs** on all 18 externally-declared
  classes/properties in `alignment.ttl` (DCAT, MLDCAT-AP, ODRL, PROV-O,
  FOAF, SPDX). Each now links to the specific section of its home
  specification.

### Changed
- Version bumped from 0.1.3 to 0.1.4 with matching `owl:versionIRI`.

## [0.1.3] — 2026-04-23

### Added — fourth-pass critique fixes
- **MED-1**: controlled vocabularies for `daimo:authMethod` (via SHACL `sh:in`
  over nine common authentication tokens) and `daimo:protocol` (via SHACL
  `sh:pattern` matching `holdout`, `<n>-fold-cv`, `bootstrap-<n>`, etc.).
  Catches typos in KG data that silently passed before.
- **INV-5** (`OfferingPolicyTargetInvariant`): every
  `daimo:AIAssetOffering`'s `daimo:offersModel` must appear as
  `odrl:target` of its attached policy, at Policy level or on some
  Permission. Prevents catalog records whose policy doesn't actually
  govern the registered model.
- **INV-6** (`OfferingAssignerInvariant`): the offering's
  `daimo:offeredBy` must equal the `odrl:assigner` of its attached
  policy. Prevents governance-chain inconsistencies where the catalog
  record credits one agent and the ODRL offer is issued by another.
- Two new negative-test cases (`bad:INV5-offering`, `bad:INV6-offering`)
  verifying each new invariant fires on a deliberately bad KG.

### Changed
- **MED-4**: `ex:audit-run-legs-checksum` promoted from blank-node to
  named IRI in the example KG. Allows external references and keeps
  the checksum identifier stable across serialisations.
- **LOW-1**: `ex:deployment-flood-v2` now exposes two services
  (`ex:flood-risk-service` REST + `ex:flood-risk-service-grpc` gRPC)
  with distinct `daimo:IOContract`s, exercising the non-functional
  `daimo:exposedAs` / `daimo:hasIOContract` established in v0.1.2.
- Negative-test harness updated: `EXPECTED` dict now contains six
  entries; success message reads "all 6 invariants fired".

## [0.1.2] — 2026-04-23

### Fixed — senior-reviewer second-pass critique
- **C-NEW-1**: removed `daimo:offeredBy rdfs:subPropertyOf dct:publisher`.
  On a `dcat:CatalogRecord`, `dct:publisher` denotes the catalog
  maintainer (e.g., INESData), not the author of the registered asset
  (e.g., UPM). The prior alignment produced wrong attribution.
- **C-NEW-2**: added `odrl:target` and `odrl:assigner` to all Offer
  policies in the example KG; added `daimo:OfferInDAIMOShape` requiring
  both fields at either Policy or Permission level (ODRL 2.2 conformance).
- **C-NEW-3**: migrated `daimo:integrityHash` from `xsd:string` to
  `spdx:Checksum`. A digest without its algorithm is unverifiable;
  `spdx:Checksum` bundles `spdx:algorithm` + `spdx:checksumValue`. SHACL
  shape now enforces both fields with a minimum 32-hex-char digest.
- **C-NEW-4**: removed `owl:FunctionalProperty` on `daimo:exposedAs` and
  `daimo:hasIOContract` (and the corresponding `sh:maxCount 1` in
  SHACL). A real deployment can expose multiple endpoints (REST + gRPC,
  multi-region) with a distinct I/O contract per service.

### Changed
- CQ-R2 SPARQL rewritten to use `daimo:offeredBy` directly (the prior
  version relied on the dropped `dct:publisher` alignment).

### Added
- [ONTOLOGY-REFERENCE.md](ONTOLOGY-REFERENCE.md) — comprehensive
  human-readable reference covering every class, property, axiom, and
  SHACL shape, with OntoClean tags, identity criteria, rationale for
  each design choice, and CQ / example-KG traversal maps.
- [VALIDATION-MATRIX.md](VALIDATION-MATRIX.md) — requirements-to-evidence
  traceability matrix mapping each class, property, axiom, CQ, and
  invariant to the validation script, report file, and pass criterion
  that proves it.

## [0.1.1] — 2026-04-22

### Fixed — alignment axioms (senior-reviewer critique)
- Removed `daimo:authorizesRun rdfs:subPropertyOf prov:used`. The prior
  alignment silently typed every `ExecutionAuthorization` as a
  `prov:Activity`, conflicting with its `odrl:Agreement` nature.
- Removed `daimo:grantedTo rdfs:subPropertyOf prov:qualifiedAssociation`.
  `prov:qualifiedAssociation` ranges over reified association objects,
  not agents; the alignment was typing grantee agents as Associations.
- Removed `daimo:evidenceOf rdfs:subPropertyOf prov:hadActivity`.
  `prov:hadActivity` is used on qualified-influence objects, not on
  entities; PROV-O does not offer a clean entity-to-activity attestation
  property, so DAIMO now uses a native property.
- Removed `daimo:contextDataset rdfs:subPropertyOf it6:trainedOn` and
  `daimo:contextFlow rdfs:subPropertyOf it6:hasFlow`. The domains of the
  external properties re-typed `SharedEvaluationContext` as
  `MachineLearningModel` / `Run` via RDFS inference. Conceptual
  relation retained via `skos:related` in `alignment.ttl`.

### Added — verification, invariants, tests
- Entailment-verification check in `reasoner_check.py`: for every
  DAIMO-native class, enumerates every inferred superclass after
  OWL-RL materialisation and flags any entailment into a forbidden
  target class.
- Four SHACL-SPARQL cross-class invariants (INV-1..INV-4):
  derivation-authorization consistency, run-agent-grantee match,
  deployment-service model match, authorisation-expiry temporal check.
- `tests/negative-examples.ttl` + `tests/negative_test.py`:
  four-case negative-test harness that deliberately violates each
  invariant and asserts every shape catches its designated violation.
- Seven competency questions deepened to exercise real reasoning
  rather than pure property retrieval: CQ-R2, CQ-R5, CQ-D3, CQ-E1,
  CQ-E2, CQ-V4, CQ-G4.
- Validator now materialises OWL-RL closure before running CQ
  SPARQL so subProperty/subClass entailments are queryable.

### Changed
- `daimo:AIAssetOffering` re-aligned from `odrl:Offer` to
  `dcat:CatalogRecord`. The previous alignment conflated the
  catalog-record reification with the policy object it carries.
- `daimo:offersModel` now `rdfs:subPropertyOf foaf:primaryTopic`;
  `daimo:offeredBy` now `rdfs:subPropertyOf dct:publisher`.
- External classes referenced by DAIMO axioms are now locally
  declared (owl:Class / owl:ObjectProperty / owl:DatatypeProperty)
  with minimal domain/range and `rdfs:comment` to satisfy OOPS!
  P34/P35/P08 without requiring full vocabulary imports.
- Spanish `@es` labels dropped (project originates in Spanish but
  target venue is English-only; Spanish proper names remain in the
  example KG where they are real referents).

### Removed
- WIDOCO `index-es.html` generation (bilingual docs no longer
  produced).

## [0.1.0] — 2026-04-21

### Added — initial release
- 9 DAIMO-native classes + 5 ParticipantRole subclasses.
- Axiomatised alignment to DCAT, DCAT-AP, MLDCAT-AP 3.0.0, ODRL 2.2,
  PROV-O, FOAF, SPDX, Dublin Core, and (for extension terms only)
  the Eclipse EDC namespace. DSP (`dspace:`) used for informative
  close-matches.
- 10 SHACL shapes (minimum completeness + two conformance shapes
  over reused `it6:MachineLearningModel` and `it6:Run`).
- Running-scenario example KG (`examples/flood-risk-scenario.ttl`)
  naming UPM / Leganés / INESData / CSIC / Gaia-X.
- 23 competency questions in natural language (`ORSD/daimo-cqs.md`)
  organised in five actor categories (R/D/E/V/G).
- SPARQL suite with one query per CQ; all return ≥1 row against the
  example KG.
- End-to-end validator (`validate.py`) running SHACL + CQ SPARQL.
- WIDOCO-generated HTML documentation under `docs/`.
- OWL 2 DL profile, `owl:versionIRI`, `owl:AllDisjointClasses` over
  top-level kinds, 18 `owl:FunctionalProperty` declarations.

## Unreleased — planned

- Live `w3id.org/pionera/daimo` redirect (Phase 3 publication).
- Zenodo archival DOI (Phase 3 publication).
- Chowlk class-diagram figure for paper submission.
- Expert validation interviews (LOT Phase 1 requirement-validation
  + LOT Phase 3 release-candidate review).
- Integration against a real MLDCAT-AP 3.0.0 catalog instance
  (external validation / case-study hardening).
