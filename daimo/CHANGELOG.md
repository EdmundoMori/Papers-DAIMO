# Changelog

All notable changes to DAIMO are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and DAIMO adheres
to semantic versioning (`owl:versionInfo` mirrors this file).

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
