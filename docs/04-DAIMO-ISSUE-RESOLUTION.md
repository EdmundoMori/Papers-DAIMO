# DAIMO Technical Issue Resolution Report

## Status summary
| ID | Issue | Status | Base commit | Main files changed | Validation | Residual risk |
|---|---|---|---|---|---|---|
| DAIMO-ISSUE-01 | Unambiguous DataService–IOContract association | **RESOLVED** | `c525c79` | ontology, shapes, example, negatives, queries, benchmark, reports, docs 00–03, ORSD, CHANGELOG, evidence-matrix | SHACL conforms=True; 23/23 CQs; CQ-D3/CQ-E1 = 2 rows; INV-7/INV-8 fire; HermiT consistent | WIDOCO site under `daimo/docs/` not regenerated |
| DAIMO-ISSUE-02 | Separation of execution authorization and ODRL agreement | **RESOLVED** | `2ae0c6d` | ontology, shapes, example, negatives, CQs, `validate.py`, `reasoner_check.py`, benchmark, reports, docs 00–04, ORSD, CHANGELOG, evidence-matrix, CHOWLK guide | SHACL conforms=True; 23/23 CQs; CQ-G3 = 1 distinct auth≠agreement row; 11/11 negative checks; HermiT consistent; 0 forbidden entailments; benchmark 100/1000 conform | OOPS! timed out; WIDOCO copies under `daimo/docs/` still show `⊑ odrl:Agreement` |
| DAIMO-ISSUE-03 | Optional random seed when applicable | **RESOLVED** | `2ae0c6d` (working tree also holds ISSUE-02) | `daimo-core.ttl`, `daimo-shapes.ttl`, `queries.md`, `random_seed_test.py` + seed graphs, ORSD, docs 00–04, CHANGELOG, evidence-matrix | SHACL 0 seed conforms; 2 seeds / non-integer rejected; CQ-V1 OPTIONAL unbound on seedless graph; 23/23 CQs; flood-risk still conforms with seed 42 | No universal stochastic-protocol list (by design); WIDOCO not regenerated; no commit/push |
| DAIMO-ISSUE-04 | Scope of SHACL rules over reused classes | **RESOLVED** | `2ae0c6d` (working tree holds 02–04) | `daimo-shapes.ttl`, `tests/reused_class_scope_test.py` + fixtures, docs 00–04, CHANGELOG, evidence-matrix | 9-cell matrix PASS (mixed complete graph); flood-risk conforms; 11/11 negatives; 23/23 CQs; HermiT 1.46 s | WIDOCO copies still use `sh:targetClass`; INV-2 still `targetClass it6:Run` (SPARQL self-scopes); OOPS! timeout; no commit/push |

---

## DAIMO-ISSUE-01 — Unambiguous DataService–IOContract association

- **Base commit:** `c525c79d19695230488fa3bd20c1c9707b3168dc`
- **Execution date:** 2026-08-24
- **Working environment:** WSL Ubuntu-22.04, `daimo/.venv` (rdflib 7.6.0, pyshacl 0.31.0, owlrl 7.6.1, owlready2 0.51, Java for HermiT)
- **Version policy:** no version bump, tag, release, commit, push or PR performed in this step. Change recorded under `CHANGELOG.md` → `## [Unreleased]`. `owl:versionInfo` stays `0.1.6`.

### Initial problem
A `daimo:ModelDeployment` could declare several `daimo:exposedAs` services and
several `daimo:hasIOContract` contracts, but nothing linked a specific contract
to a specific service. Consequences:

- The flood-risk example declared two services (REST, gRPC) and two contracts
  (JSON/OAuth2, protobuf/mTLS) with no pairing.
- CQ-D3 and CQ-E1 joined services and contracts independently, producing the
  **cartesian product** (2 services × 2 contracts = **4 rows**, including the two
  wrong pairings REST↔mTLS and gRPC↔OAuth2).
- It was therefore impossible to determine unambiguously which format and
  authentication method belong to each endpoint.

### Verified root cause
Confirmed empirically **before** any change by running `validate.py` on the base
graph: CQ-D3 returned **4 rows** and CQ-E1 returned **4 rows** over the
two-service/two-contract deployment — the cartesian join predicted above. The
model lacked a property connecting `daimo:IOContract` to the `dcat:DataService`
it describes.

### Modelling decision
Add a native object property:

- **`daimo:forService`** — domain `daimo:IOContract`, range `dcat:DataService`.
- **`owl:FunctionalProperty`**: each contract describes exactly one service.
  (Several contracts may still describe the same service if ever needed — the
  functional characteristic is on `forService`, not a max-1 on contracts per
  service — but a single contract targets one service.)
- **`owl:AsymmetricProperty`**: a contract and the service it describes are
  distinct individuals (consistent with `offersModel`/`deploysModel` style).
- No inverse property added (no real reverse-query need; the deployment reaches
  the service through `exposedAs`).
- `daimo:hasIOContract` was **not** replaced: the intended structure is
  *deployment `exposedAs` ≥1 service; deployment `hasIOContract` ≥1 contract;
  each contract `forService` exactly one exposed service*.

### Alternatives considered and rejected
- **Reuse `dcat:endpointDescription`** — rejected. It runs in the opposite
  direction (`dcat:DataService` → a description resource) and its value is an
  API-description document (e.g. an OpenAPI file), not a structured
  `daimo:IOContract`. Not a semantic match, so no alignment was declared.
- **No property in DCAT, MLDCAT-AP, ODRL, PROV-O or DSP** carries the exact
  meaning "the data service this I/O contract describes"; `forService` therefore
  remains native and **unaligned**, documented as such in `alignment.ttl`.
- **Encode the pairing only in queries / expected counts** — explicitly rejected
  by the task; it would not fix the model.

### OWL changes (`daimo/ontology/daimo-core.ttl`)
- Added `daimo:forService` (ObjectProperty, Functional, Asymmetric) with
  `rdfs:label`, `rdfs:domain`, `rdfs:range`, `rdfs:isDefinedBy`,
  `skos:definition`, `skos:example`, `rdfs:comment`.
- Revised `rdfs:comment` of `ModelDeployment`, `IOContract`, `exposedAs`,
  `hasIOContract` and the `IOContract` `skos:definition` to describe the
  per-endpoint contract/service pairing.

### Alignment changes (`daimo/ontology/alignment.ttl`)
- Added a documented **non-alignment** note for `daimo:forService` (no external
  superproperty; `dcat:endpointDescription` considered and rejected).

### SHACL changes (`daimo/shapes/daimo-shapes.ttl`)
- `IOContractShape`: `daimo:forService` now required (`sh:minCount 1`,
  `sh:maxCount 1`, `sh:class dcat:DataService`).
- **INV-7** `DeploymentContractServiceInvariant` (target `ModelDeployment`):
  every `hasIOContract` contract must `forService` a service the same deployment
  `exposedAs`.
- **INV-8** `DeploymentServiceContractInvariant` (target `ModelDeployment`):
  every `exposedAs` service must have ≥1 `forService` contract.
- Both are SHACL-SPARQL constraints. To avoid a **pySHACL false positive** (its
  federated-query regex flags the token `forService ` followed by whitespace),
  the two `sh:select` bodies reference the property by full IRI
  `<https://w3id.org/pionera/daimo#forService>`.
- Module `dct:description` / `rdfs:comment` updated: **8** invariants
  (INV-1..INV-8).

### Example and query changes
- `daimo/examples/flood-risk-scenario.ttl`: REST contract
  `ex:flood-risk-iocontract` → `forService ex:flood-risk-service`; gRPC contract
  `ex:flood-risk-iocontract-grpc` → `forService ex:flood-risk-service-grpc`.
  Two endpoints, formats and auth preserved.
- `daimo/queries/queries.md`: CQ-R4, CQ-D3, CQ-E1, CQ-G2 rewritten to join each
  contract to its service via `daimo:forService`, removing the
  `exposedAs × hasIOContract` cartesian join.

### Tests added or updated
- `daimo/tests/negative-examples.ttl`: added `bad:INV7-deployment` (contract
  `forService` a non-exposed service) and `bad:INV8-deployment` (exposed service
  with no contract). Header updated to INV-1..INV-8.
- `daimo/tests/negative_test.py`: `EXPECTED` extended with INV-7/INV-8.
- `daimo/scalability_benchmark.py`: generator now links every synthetic contract
  to its service via `forService`; the `invocation_contracts` control query uses
  the corrected relation.

### Commands executed
```bash
git status --short
git rev-parse HEAD                                   # c525c79...
.venv/bin/python validate.py
.venv/bin/python tests/negative_test.py
.venv/bin/python reasoner_check.py
.venv/bin/python scalability_benchmark.py --sizes 100 1000
.venv/bin/python validate.py           > reports/validation-results.md
.venv/bin/python tests/negative_test.py > reports/negative-test-results.md
git diff --check
```

### Exact results
- **validate.py:** ontology 608 / shapes 364 / data 227 triples; **SHACL
  conforms = True**; OWL-RL closure 2018 triples; **23/23 CQs ≥1 row**;
  **CQ-D3 = 2, CQ-E1 = 2, CQ-R4 = 2, CQ-G2 = 2**.
- **negative_test.py:** conforms = False; negative graph 163 triples;
  **8/8 invariants FOUND** (INV-1..INV-8) → `PASS: all 8 invariants fired`.
- **reasoner_check.py:** merged 835 triples; **HermiT consistent = True**, 0
  unsatisfiable; **OWL-RL** 835 → 2018 (1183 materialised), 0 `owl:Nothing`, 0
  unsatisfiable subclasses; **entailment check** 14 classes, **0** forbidden
  entailments.
- **scalability_benchmark.py --sizes 100 1000:** 100 units → 8153 data triples,
  **conforms**; 1000 units → 81053 data triples, **conforms**; `invocation
  contracts` count = 100 / 1000 (one endpoint per unit, no inflation).
- **git diff --check:** the only warnings are pre-existing trailing-whitespace /
  line-ending (CRLF) reports on the `docs/*.md` files (see residual risks); no
  whitespace defects were introduced by the ontology/shape/query/test edits.
- **OOPS!:** not executed — the external service `oops.linkeddata.es` was not
  reachable from the environment. No prior result reused. Expected effect of the
  change: `+1` on OOPS! P13 (undeclared inverse), correctness unaffected.

### Before/after CQ behaviour
| CQ | Before | After | Meaning |
|---|---|---|---|
| CQ-D3 | 4 rows | **2 rows** | each endpoint paired with its own auth method |
| CQ-E1 | 4 rows | **2 rows** | each endpoint with its own format + auth |
| CQ-R4 | 2 rows (interface not identified) | **2 rows** (service identified) | contract resolved to its `dcat:DataService` |
| CQ-G2 | 2 rows (no service) | **2 rows** (service reported) | deployment→infra→service→contract kept intact |
| all others | unchanged | unchanged | no regression |

### Documentation and reports updated
- `docs/00-DAIMO-OVERVIEW.md`, `docs/01-DAIMO-DESIGN.md`,
  `docs/02-DAIMO-IMPLEMENTATION.md`, `docs/03-DAIMO-EVALUATION.md` — counts,
  invariant list, `forService` reference, non-alignment row, evaluation numbers.
- `daimo/ORSD/daimo-cqs.md` — CQ-R4/D3/E1/G2 notes + endpoint-disambiguation note.
- `daimo/CHANGELOG.md` — `## [Unreleased]` section.
- `paper/evidence-matrix.md` — affected counts and figures.
- `daimo/reports/validation-results.md`, `negative-test-results.md`,
  `reasoner-report.md`, `scalability-benchmark.md` — regenerated from this run.

**Count changes (technical information only):** object properties 29 → **30**;
total native properties 37 → **38**; functional 28 → **29**; asymmetric 5 →
**6**; SHACL node shapes 18 → **20**; cross-class invariants 6 → **8**; positive
graph 225 → **227** triples; negative graph 118 → **163** triples; OWL-RL closure
1988 → **2018** triples.

### Remaining limitations or risks
1. **OOPS!** could not be re-run (service unreachable). Re-run before the next
   release and refresh `reports/oops-report.md` and evaluation §3.
2. **WIDOCO site** under `daimo/docs/` (generated HTML + copied `.ttl`/`.owl`) is
   a build artefact that predates `forService`; regenerate it at the next release.
3. **git line endings:** `git diff --check` flags trailing whitespace on the
   `docs/*.md` files. This is a pre-existing CRLF/LF condition (the docs already
   showed as modified before the content edits of this task), not introduced
   here. Before committing, run `git diff -w` to confirm only intended content
   changed, and consider a `.gitattributes` (`*.md text eol=lf`) to normalise.
4. **Commit/push deferred:** per the task, no commit/push/PR was made. The local
   repository and GitHub still need a commit + push once the changes are
   reviewed.

### Final status
**RESOLVED** — all ten acceptance criteria met locally:
1. explicit contract–service relation (`daimo:forService`) ✓;
2. each example contract identifies its service unambiguously ✓;
3. CQ-D3/CQ-E1 return only correct associations (2 rows) ✓;
4. SHACL (INV-7) detects a contract bound to a non-exposed service ✓;
5. SHACL (INV-8) detects an exposed service without a contract ✓;
6. positive graph conforms ✓;
7. all other CQs still work (23/23) ✓;
8. HermiT + OWL-RL consistent, no forbidden entailments ✓;
9. reports regenerated ✓;
10. documentation matches the implementation ✓.

---

## DAIMO-ISSUE-02 — Separation of execution authorization and ODRL agreement

- **Base commit:** `2ae0c6dd47b6b08e07b2f4b350340f5097c721e3` (`main`, DAIMO-ISSUE-01 already merged; those changes are preserved).
- **Execution date:** 2026-08-24
- **Working environment:** WSL Ubuntu-22.04, `daimo/.venv` (rdflib 7.6.0, pyshacl 0.31.0, owlrl 7.6.1, owlready2 0.51, Java for HermiT)
- **Version policy:** no version bump, tag, release, commit, push or PR in this step. Recorded under `CHANGELOG.md` → `## [Unreleased]`. `owl:versionInfo` stays `0.1.6`.

### Initial problem
`daimo:ExecutionAuthorization` was modelled as `rdfs:subClassOf odrl:Agreement`, and the flood-risk example used **one individual** as both the accepted ODRL agreement and the execution authorization. CQ-G3 is approved as asking for “the authorization **and the agreement it derives from**”, but:

- no property related an authorization to a *different* agreement;
- the SPARQL for CQ-G3 returned only `?auth`, the grantee and the expiry;
- the accepted contractual result and the operational authorization that binds that result to concrete runs were therefore the same resource.

### Verified root cause
Confirmed on the ISSUE-01 graph (`2ae0c6d`, before this change) by reading the artefacts, not by rewriting CQ-G3:

- `daimo-core.ttl` / `alignment.ttl` declared `ExecutionAuthorization ⊑ odrl:Agreement`.
- `daimo:grantedTo ⊑ odrl:assignee`. Because `odrl:assignee` has domain `odrl:Policy` and `odrl:Agreement ⊑ odrl:Policy`, that alignment was only harmless while the authorization *was* an agreement; it is exactly what would re-type a separated authorization as an `odrl:Policy`.
- `flood-risk-scenario.ttl` typed `ex:authorization-municipality-flood-v2` as both `daimo:ExecutionAuthorization` and (via subclass) `odrl:Agreement`, and placed `odrl:permission` / `odrl:assignee` on that same node.
- CQ-G3 in `queries.md` selected `?auth ?grantee ?expires` only.

The approved question therefore could not be answered literally: there was no second individual to return.

### Modelling decision
Keep two distinct resources and a native functional link:

```
odrl:Agreement
       ↑  daimo:derivedFromAgreement (functional, asymmetric)
daimo:ExecutionAuthorization  ⊑  prov:Entity
       ↓  daimo:authorizesRun
    it6:Run
```

- **`daimo:derivedFromAgreement`** — domain `ExecutionAuthorization`, range `odrl:Agreement`, `owl:FunctionalProperty` (one accepted set of terms per authorization), `owl:AsymmetricProperty` (authorization ≠ agreement).
- **`ExecutionAuthorization ⊑ prov:Entity`** — a governed artefact, consistent with `ModelDeployment`, `DerivedArtifact` and `AuditEvidence`. It is **not** an ODRL policy.
- **ODRL permissions and parties live on the `odrl:Agreement`**. The authorization carries `authorizesRun`, `grantedTo` and `expiresAt`.
- **`grantedTo` is no longer `⊑ odrl:assignee`**. Equivalence “authorization grantee = agreement assignee” is SHACL INV-9, not OWL subsumption.
- Informative `skos:related dspace:ContractNegotiation` is kept: the DSP negotiation produces the agreement; the authorization is the derived resource used to bind that agreement to runs.

### Alternatives considered and rejected
- **Rewrite only CQ-G3** so it no longer asks for the agreement — rejected by the issue (the approved question stands; the model was wrong).
- **Reuse `prov:wasDerivedFrom`** — rejected. Domain/range `prov:Entity`; generic entity lineage. It would force every `odrl:Agreement` into `prov:Entity` and lose the meaning “the accepted ODRL agreement this authorization enforces”. No ODRL/DCAT/MLDCAT-AP/PROV-O/DSP property carries that meaning, so the property stays native and unaligned.
- **Keep `ExecutionAuthorization ⊑ odrl:Agreement` and add `derivedFromAgreement` to self** — rejected: that is the original conflation; `FILTER(?auth != ?agreement)` would fail.
- **Keep `grantedTo ⊑ odrl:assignee`** — rejected: `odrl:assignee` domain `odrl:Policy` would re-type every authorization as a policy, undoing the separation.
- **Leave `ExecutionAuthorization` with no external superclass** — considered. Rejected in favour of `prov:Entity`: the authorization is a fixed digital/conceptual artefact in the provenance chain, and the other DAIMO governance artefacts already sit under `prov:Entity`. The `prov:Entity` alignment does **not** make it an `odrl:Agreement` or `odrl:Policy`.

### Changes to ExecutionAuthorization
- Removed `rdfs:subClassOf odrl:Agreement` from the alignment module.
- Declared `rdfs:subClassOf prov:Entity` in both `daimo-core.ttl` (class definition) and `alignment.ttl` (same pattern as `ModelDeployment`).
- Rewrote `skos:definition`, `skos:example` and `rdfs:comment`: the class binds one accepted agreement to runs, a grantee and an expiry; it is not the agreement.
- `authorizesRun` / `authorizedBy` / `grantedTo` / `expiresAt` remain on the authorization. Comments now justify non-alignment of `authorizesRun` against `prov:used` because the authorization is a `prov:Entity`, not because it used to be an `odrl:Agreement`.
- Pairwise disjointness of top-level kinds is unchanged; `ExecutionAuthorization` stays a member of `daimo:TopLevelKindsDisjointness`.

### New authorization–agreement relation
`daimo:derivedFromAgreement` (`owl:ObjectProperty`, `owl:FunctionalProperty`, `owl:AsymmetricProperty`) with `rdfs:label`, `rdfs:domain`, `rdfs:range`, `rdfs:isDefinedBy`, `skos:definition`, `skos:example`, `rdfs:comment`. Counted as native property #31 (object properties 30 → 31; total native properties 38 → 39; asymmetric 6 → 7). Functional-property *declarations* remain **29** (21 object + 8 datatype); a comment containing the token `owl:FunctionalProperty` makes a naïve grep read 30.

### Alignment and non-alignment changes
- Deleted `ExecutionAuthorization rdfs:subClassOf odrl:Agreement`.
- Added `ExecutionAuthorization rdfs:subClassOf prov:Entity`.
- Deleted `grantedTo rdfs:subPropertyOf odrl:assignee`. Documented as a non-alignment: the domain of `odrl:assignee` would infer `odrl:Policy`.
- Documented non-alignment of `derivedFromAgreement` (no external superproperty; `prov:wasDerivedFrom` considered and rejected).
- Revised the `skos:related dspace:ContractNegotiation` note: the negotiation yields the agreement; the authorization is derived from that agreement.
- `alignment.ttl` now has **4** `rdfs:subPropertyOf` axioms (`offersModel`, `hasOfferPolicy`, `derivedFromRun`, `contextTask`). `hasOffering ⊑ foaf:isPrimaryTopicOf` remains in the core module.

### SHACL and invariant changes
- `ExecutionAuthorizationShape`: requires `derivedFromAgreement` 1..1 (`sh:class odrl:Agreement`); still requires `authorizesRun` ≥1, `grantedTo` 1..1, `expiresAt` 1..1. `odrl:permission` is **not** required on the authorization.
- New conformance shape `AgreementInDAIMOShape` (`odrl:Agreement`): `odrl:permission` ≥1 and `odrl:assignee` ≥1.
- **INV-1** and **INV-2** unchanged in SPARQL (they already walk `underAuthorization` / `authorizesRun` / `grantedTo` / `prov:wasAssociatedWith`); negative cases now also carry a well-formed source agreement so they do not false-trigger INV-9.
- **INV-9** `AuthorizationAgreementAssigneeInvariant` (SHACL-SPARQL, not OWL): the `grantedTo` grantee must be an `odrl:assignee` of the `derivedFromAgreement` target.
- Cross-class invariants 8 → **9**; conformance shapes 3 → **4**; node shapes 20 → **22**.
- Module comment no longer claims DAIMO classes subclass ODRL types.

RDFS `rdfs:range odrl:Agreement` on `derivedFromAgreement` means that, under `inference="rdfs"`, `sh:class odrl:Agreement` cannot catch a missing type (the range materialises it). The “agreement that is not a well-formed Agreement” case is therefore caught by `AgreementInDAIMOShape` (`odrl:permission` missing), not by `sh:class`. This limitation is documented on the negative example.

### Example and CQ-G3 changes
- New individual `ex:agreement-municipality-flood-v2` (`odrl:Agreement`) holds `odrl:target`, `odrl:assigner`, `odrl:assignee` and `odrl:permission`.
- Existing `ex:authorization-municipality-flood-v2` (`daimo:ExecutionAuthorization`) is a **different IRI**, linked by `daimo:derivedFromAgreement`, still `grantedTo` the municipality, `authorizesRun` the scenario run, `expiresAt` 2027-04-20.
- Provenance chain (`DerivedArtifact` → run → authorization; audit evidence; cross-participant bundle) preserved.
- CQ-G3 rewritten to return `?auth ?agreement ?grantee ?expires` with `FILTER(?auth != ?agreement)` and `?agreement odrl:assignee ?grantee`.
- CQ-E2 and CQ-E5 reviewed: they still traverse the authorization; the agreement is reachable via `derivedFromAgreement` when needed. Row counts unchanged (1).

**Exact CQ-G3 result** on the positive graph (1 row):

| Variable | Value |
|---|---|
| `?auth` | `https://example.org/daimo-scenario/authorization-municipality-flood-v2` |
| `?agreement` | `https://example.org/daimo-scenario/agreement-municipality-flood-v2` |
| `?grantee` | `https://example.org/daimo-scenario/municipality` |
| `?expires` | `2027-04-20T00:00:00+00:00` |

`FILTER(?auth != ?agreement)` holds. `validate.py` additionally asserts every authorization has a distinct typed agreement (`auths=1 distinct-pairs=1 collapsed=0 unlinked=0`).

### Negative tests
Harness `EXPECTED` now has 11 keys (INV-1..INV-9 plus two per-class completeness cases). Previous INV-1..INV-8 cases were updated with a source agreement whose `odrl:assignee` matches `grantedTo`, so they still fire **only** their original invariant.

| Case | Focus | What it detects |
|---|---|---|
| INV-2 | `INV2-run` | run agent ≠ authorization grantee (pre-existing; still required) |
| INV-9 | `INV9-auth` | authorization grantee ≠ agreement `odrl:assignee` |
| AUTH-no-agreement | `AUTH-no-agreement` | authorization with no `derivedFromAgreement` |
| AUTH-bad-agreement | `AUTH-bad-agreement-notagreement` | source resource lacks `odrl:permission` (not a well-formed `odrl:Agreement` under RDFS range inference) |

### Reasoning checks
`reasoner_check.py` `FORBIDDEN_SUPERS` now includes `odrl:Agreement` and `odrl:Policy`. After OWL-RL:

- **Before (ISSUE-01 / v0.1.6 model):** `ExecutionAuthorization ⊑ Agreement` (and hence `Policy` via ODRL).
- **After:** `ExecutionAuthorization ⊑ Thing, Entity` only. No `Agreement`, no `Policy`, no `Activity`, no `Nothing`.

HermiT: consistent, 0 unsatisfiable classes.

### Commands executed
```bash
git status --short
git rev-parse HEAD          # 2ae0c6dd47b6b08e07b2f4b350340f5097c721e3
.venv/bin/python validate.py
.venv/bin/python tests/negative_test.py
.venv/bin/python reasoner_check.py
.venv/bin/python scalability_benchmark.py --sizes 100 1000
git diff --check
.venv/bin/python oops_check.py          # TimeoutError contacting oops.linkeddata.es
```

Reports regenerated by redirecting `validate.py` / `negative_test.py` and by the writers inside `reasoner_check.py` / `scalability_benchmark.py`.

### Exact results
- **validate.py:** ontology **617** / shapes **384** / data **233** triples; **SHACL conforms = True**; OWL-RL closure **2043**; **23/23 CQs ≥1 row**; CQ-G3 = **1**; CQ-D3 = 2; CQ-E1 = 2; CQ-E2 = 1; CQ-E5 = 1; ISSUE-02 separation **PASS** `auths=1 distinct-pairs=1 collapsed=0 unlinked=0`.
- **negative_test.py:** conforms = False; negative graph **209** triples; **11/11 FOUND** (INV-1..INV-9 + AUTH-no-agreement + AUTH-bad-agreement) → `PASS: all 11 invariants fired`.
- **reasoner_check.py:** merged **850** triples; **HermiT consistent = True**, 1.71 s, 0 unsatisfiable; **OWL-RL** 850 → 2043 (1193 materialised), 0.63 s, 0 `owl:Nothing`; entailment check **14** classes, **0** forbidden entailments; `ExecutionAuthorization ⊑ Thing, Entity`.
- **scalability_benchmark.py --sizes 100 1000:** 100 units → 8753 data triples, conforms, 100 auth→agreement pairs; 1000 units → 87053 data triples, conforms, 1000 pairs.
- **git diff --check:** only warning is pre-existing trailing whitespace in the truncated pySHACL dump inside `reports/negative-test-results.md`.
- **OOPS!:** submitted to `https://oops.linkeddata.es/rest`; **TimeoutError** after 120 s. Prior scan (0 Critical, 0 Important, 2 Minor) predates `forService` and `derivedFromAgreement`. Expected extra P13 (undeclared inverse) for `derivedFromAgreement`; not cited as a new result.

### Files and reports updated
- `daimo/ontology/daimo-core.ttl`, `daimo/ontology/alignment.ttl`
- `daimo/shapes/daimo-shapes.ttl`
- `daimo/examples/flood-risk-scenario.ttl`
- `daimo/tests/negative-examples.ttl`, `daimo/tests/negative_test.py`
- `daimo/queries/queries.md`, `daimo/ORSD/daimo-cqs.md`
- `daimo/validate.py`, `daimo/reasoner_check.py`, `daimo/scalability_benchmark.py`
- `daimo/reports/validation-results.md`, `negative-test-results.md`, `reasoner-report.md`, `scalability-benchmark.md`
- `daimo/CHANGELOG.md`
- `docs/00-DAIMO-OVERVIEW.md`, `01-DAIMO-DESIGN.md`, `02-DAIMO-IMPLEMENTATION.md`, `03-DAIMO-EVALUATION.md`, this file
- `paper/evidence-matrix.md`, `paper/CHOWLK-DRAWING-GUIDE.md`

**Count changes (technical information only):** object properties 30 → **31**; total native properties 38 → **39**; asymmetric 6 → **7**; functional declarations stay **29**; SHACL node shapes 20 → **22**; conformance shapes 3 → **4**; cross-class invariants 8 → **9**; positive graph 227 → **233** triples; negative graph 163 → **209** triples; OWL-RL closure 2018 → **2043**.

### Remaining limitations or risks
1. **OOPS!** could not be re-run (service timeout). Re-run before the next release.
2. **WIDOCO copies** under `daimo/docs/alignment.ttl` and `daimo/docs/daimo-shapes.ttl` still contain `ExecutionAuthorization ⊑ odrl:Agreement` and `grantedTo ⊑ odrl:assignee`. They are generated artefacts; regenerate at the next release. Runtime validation loads `daimo/ontology/` and `daimo/shapes/`, not those copies.
3. **RDFS range vs `sh:class`:** a target of `derivedFromAgreement` is always typed `odrl:Agreement` under RDFS inference, so “not an Agreement” is enforced as “not a well-formed Agreement” (`odrl:permission` missing).
4. **Commit/push deferred** per the task. Local `main` remains at `2ae0c6d` plus uncommitted ISSUE-02 work.
5. No version bump: still `0.1.6`.

### Final status
**RESOLVED** — all ten acceptance criteria met locally:
1. authorization and agreement are distinct individuals ✓;
2. `ExecutionAuthorization` is no longer a subclass of `odrl:Agreement` ✓;
3. explicit `daimo:derivedFromAgreement` relation ✓;
4. CQ-G3 returns both resources (and grantee, expiry) ✓;
5. positive graph conforms ✓;
6. negative tests detect missing agreement, malformed agreement, grantee≠assignee, and run-agent≠grantee (INV-2) ✓;
7. no OWL-RL/HermiT inference of `Agreement` or `Policy` on `ExecutionAuthorization` ✓;
8. run agent, authorization grantee and agreement assignee are kept coherent (INV-2 + INV-9) ✓;
9. unrelated CQs still return ≥1 row (23/23) ✓;
10. reports regenerated ✓.

---

## DAIMO-ISSUE-03 — Optional random seed when applicable

- **Base commit:** `2ae0c6dd47b6b08e07b2f4b350340f5097c721e3` (`main`). Uncommitted DAIMO-ISSUE-01/02 working-tree changes are preserved.
- **Execution date:** 2026-08-24
- **Working environment:** WSL Ubuntu-22.04, `daimo/.venv`
- **Version policy:** no version bump, tag, release, commit, push or PR. Recorded under `CHANGELOG.md` → `## [Unreleased]`. `owl:versionInfo` stays `0.1.6`.

### Initial problem
`daimo:randomSeed` is a functional datatype property (`SharedEvaluationContext → xsd:integer`). `SharedEvaluationContextShape` required `sh:minCount 1` and `sh:maxCount 1`, so every context had to declare a seed — including deterministic protocols where a seed is not applicable. The approved competency questions ask for “protocol and, when applicable, seed”.

### Requirement–implementation discrepancy
Verified by reading the artefacts:

- OWL: property present and functional (correct to keep).
- SHACL: `minCount 1` on `randomSeed` (too strong).
- CQ-V1: required `?ctx daimo:randomSeed ?seed` as a mandatory triple, so a valid seedless context would yield **0 rows**.
- CQ-V2 and CQ-V3 already joined only on the context IRI and metric (they did not mention the seed), so they were not the source of the mismatch, but CQ-V1 was.

The property must stay; only its **obligation** was wrong.

### Modelling decision
- Keep `randomSeed` as a functional `xsd:integer` datatype property (one context must not declare two incompatible seeds).
- SHACL cardinality **0..1** (`maxCount 1`, no `minCount`).
- Applicability is a property of the **evaluation procedure**, not of a DAIMO-wide list of stochastic protocols. No such list was invented.
- Omitting the seed records that the declared protocol does not use one; it is **not** a claim of complete reproducibility. Comparability still requires the same metric and compatible conditions, not just task/dataset/version/protocol/seed.

### OWL changes
- `daimo:randomSeed` kept: domain, range, `owl:FunctionalProperty`. Added `skos:definition`, `skos:example`, `rdfs:isDefinedBy`; comment rewritten.
- `SharedEvaluationContext` definition/example/comment: “protocol and, when applicable, random seed”; no claim that five facets alone guarantee comparability.
- `daimo:protocol` comment notes that seed applicability follows the procedure.

### SHACL cardinality changes
- Removed `sh:minCount 1` on `randomSeed`.
- Kept `sh:maxCount 1` and `sh:datatype xsd:integer`.
- Added an English `sh:message` stating optionality and the two rejection cases.

### Query changes
- CQ-V1: `OPTIONAL { ?ctx daimo:randomSeed ?seed }`. On flood-risk (holdout, seed 42) still 1 row with seed bound. On the seedless leave-one-out graph, 1 row with `?seed` unbound.
- CQ-V2 / CQ-V3: pattern unchanged (context IRI + metric); documented as not excluding seedless contexts.
- ORSD CQ-V1 wording and the V-category benchmarking note updated.

### Positive seedless-context test
`daimo/tests/seedless-eval-context.ttl`: `SharedEvaluationContext` with `protocol "leave-one-out"` and **no** `randomSeed`, plus a minimal evaluation/model so the graph is otherwise SHACL-complete.

`python tests/random_seed_test.py`:
- SHACL conforms = **True**
- CQ-V1 OPTIONAL: **1 row**, `protocol='leave-one-out'`, `seed_bound=False`
- CQ-V2/V3-style ranking: **1 row**

### Negative cardinality and datatype tests
Same harness:

| Graph | Expected | Observed |
|---|---|---|
| 0 seeds (`seedless-eval-context.ttl`) | conforms | **True** |
| 1 seed (flood-risk holdout, seed 42) | conforms | **True** (via `validate.py`) |
| 2 seeds (`random-seed-two.ttl`) | does not conform (`maxCount`) | **conforms=False** |
| non-integer seed (`random-seed-badtype.ttl`, `"forty-two"`) | does not conform (`datatype`) | **conforms=False** |

The repository has no pytest suite; the harness follows `tests/negative_test.py`.

### Commands executed
```bash
git status --short
git rev-parse HEAD
.venv/bin/python tests/random_seed_test.py
.venv/bin/python validate.py
.venv/bin/python tests/negative_test.py
.venv/bin/python reasoner_check.py
.venv/bin/python scalability_benchmark.py --sizes 100 1000
git diff --check
```

### Exact results
- **random_seed_test.py:** PASS (0/1 allowed; 2 seeds and non-integer rejected; CQ-V1 unbound; CQ-V2/V3 independent of seed).
- **validate.py:** ontology **620** / shapes **384** / data **233**; SHACL **conforms=True**; closure **2048**; **23/23 CQs**; CQ-V1=1, CQ-V2=1, CQ-V3=2; ISSUE-02 separation still PASS.
- **negative_test.py:** **11/11** INV/completeness checks still fire (ISSUE-02 harness not weakened).
- **reasoner_check.py:** merged **853**; HermiT **consistent**, 1.46 s, 0 unsatisfiable; OWL-RL 853→2048 (1195), 0.06 s, 0 `owl:Nothing`; 0 forbidden entailments.
- **scalability_benchmark.py:** 100 units 8753 data triples, conforms; 1000 units 87053, conforms. Seed still emitted for the synthetic holdout; not treated as mandatory.
- **git diff --check:** only the pre-existing trailing-whitespace warning in the truncated pySHACL dump of `reports/negative-test-results.md`.

### Documentation and reports updated
- `docs/00`–`03`, this file; `daimo/ORSD/daimo-cqs.md`; `daimo/CHANGELOG.md`; `paper/evidence-matrix.md`; `paper/CHOWLK-DRAWING-GUIDE.md`
- `daimo/reports/validation-results.md`, `negative-test-results.md`, `reasoner-report.md`, `scalability-benchmark.md`, **`random-seed-test-results.md`** (new)

### Remaining limitations or risks
1. DAIMO still does **not** decide automatically when a seed is required (no invented protocol taxonomy). Publishers must omit or declare it according to their procedure.
2. OWL `owl:FunctionalProperty` and SHACL `maxCount 1` both police two seeds; a reasoner may additionally infer inconsistency, but the SHACL test does not depend on that.
3. WIDOCO copies under `daimo/docs/` are not regenerated.
4. No version bump / commit / push in this step.

### Final status
**RESOLVED** — all ten acceptance criteria met:
1. `randomSeed` still defined and functional ✓;
2. SHACL allows zero or one seed ✓;
3. SHACL rejects two seeds ✓;
4. SHACL rejects a non-integer seed ✓;
5. positive seedless-context test exists and is automatic ✓;
6. CQ-V1 answers without a seed (`OPTIONAL`, unbound) ✓;
7. CQ-V2 and CQ-V3 do not depend on the seed ✓;
8. remaining CQs 23/23 ✓;
9. flood-risk example still conforms (seed 42 kept for holdout) ✓;
10. reports regenerated, including `random-seed-test-results.md` ✓.

---

## DAIMO-ISSUE-04 — Scope of SHACL rules over reused classes

- **Base commit:** `2ae0c6dd47b6b08e07b2f4b350340f5097c721e3`. Working tree already contains ISSUE-01..03; those changes are preserved.
- **Execution date:** 2026-08-24
- **Version policy:** no version bump, tag, commit, push or PR. All four issues stay under `CHANGELOG.md` → `## [Unreleased]`. `owl:versionInfo` remains `0.1.6`.

### Initial problem
`OfferInDAIMOShape`, `MachineLearningModelInDAIMOShape` and `RunInDAIMOShape` used `sh:targetClass` on `odrl:Offer`, `it6:MachineLearningModel` and `it6:Run`. Every instance of those reused classes in a graph received DAIMO profile obligations, including resources that never participate in DAIMO relations. The documentation said the rules applied “in DAIMO’s context”; the targets did not.

### Verified root cause
Read from `daimo/shapes/daimo-shapes.ttl` before the change: each of the three shapes had a single `sh:targetClass` on the reused type. pySHACL therefore selected every typed individual. A foreign `odrl:Offer` without `odrl:assigner` in the same graph as a DAIMO offering would fail even if `daimo:hasOfferPolicy` never pointed at it.

`AgreementInDAIMOShape` (ISSUE-02) had the same pattern (`sh:targetClass odrl:Agreement`). It is the same leak on a fourth reused class, so it was scoped in the same step.

INV-2 still uses `sh:targetClass it6:Run`, but its SPARQL only matches runs that some `daimo:ExecutionAuthorization` `authorizesRun`; an unlinked run does not fire. That SPARQL self-scoping is kept; the three *conformance* shapes did not self-scope.

### Targeting strategy
SHACL Core `sh:targetObjectsOf` (union when repeated). No `sh:SPARQLTarget`, no extra Advanced Features beyond the existing INV SPARQL constraints (`advanced=True` already required for INV-1..INV-9).

| Shape | Target(s) | Not targeted |
|---|---|---|
| `OfferInDAIMOShape` | objects of `daimo:hasOfferPolicy` | any other `odrl:Offer` |
| `AgreementInDAIMOShape` | objects of `daimo:derivedFromAgreement` | any other `odrl:Agreement` |
| `MachineLearningModelInDAIMOShape` | objects of `daimo:offersModel` **or** `daimo:deploysModel` | models only evaluated, served, or stored without those links |
| `RunInDAIMOShape` | objects of `daimo:authorizesRun` **or** `daimo:derivedFromRun` | unrelated MLDCAT-AP runs (e.g. `ex:run-baseline` in the example) |

Other DAIMO properties (`it6:evaluates`, `it6:servesModel`, `daimo:evidenceOf`, `daimo:records`) were considered and **not** added: they are either not DAIMO properties or would widen the profile without a CQ requirement. Internal obligations (assigner/target, title/identifier/policy, flow/algorithm/agent/start, permission/assignee) are **unchanged**.

SHACL checks RDF graphs. It does not apply ODRL policies and does not control access.

### SHACL changes
Replaced the three `sh:targetClass` (and the Agreement one) with `sh:targetObjectsOf`. Comments in `daimo-shapes.ttl` name the linking property. Module `dct:description` / `rdfs:comment` state the scope. Shape triple count 384 → **386** (two extra `sh:targetObjectsOf` on Model and Run).

### External-resource isolation tests
`tests/reused-class-scope/external-incomplete.ttl`: incomplete `odrl:Offer`, `it6:MachineLearningModel`, `it6:Run` with **no** DAIMO links.

Result: **SHACL conforms=True**, focus nodes = **[]**. If `sh:targetClass` were still in force this graph would fail.

The complete fixture (`daimo-complete.ttl`) **also mixes** those three incomplete externals with in-scope complete Offer/Model/Run. Result: **conforms=True**, externals still not in `sh:focusNode`. Isolation holds in a mixed graph, not only in an empty-of-DAIMO graph.

### In-scope negative tests
| Fixture | Result | Focus |
|---|---|---|
| `daimo-offer-incomplete.ttl` (`hasOfferPolicy` → offer without assigner/target) | conforms=False | `offer-incomplete` (and the offering via INV-5, expected) |
| `daimo-model-incomplete.ttl` (`offersModel` → model without title/id/policy) | conforms=False | `model-incomplete` |
| `daimo-run-incomplete.ttl` (`authorizesRun` → run without flow/algo/agent/start) | conforms=False | `run-incomplete` |
| `daimo-complete.ttl` (offer+model+run complete and linked) | conforms=True | [] |

Harness: `python tests/reused_class_scope_test.py`. Asserts the three shapes (and `AgreementInDAIMOShape`) have **no** `sh:targetClass` on the reused types and declare the **exact** `sh:targetObjectsOf` properties: `hasOfferPolicy`; `offersModel`+`deploysModel`; `authorizesRun`+`derivedFromRun`; `derivedFromAgreement`.

### Commands executed
```bash
.venv/bin/python tests/reused_class_scope_test.py
.venv/bin/python tests/random_seed_test.py
.venv/bin/python tests/negative_test.py
.venv/bin/python validate.py
.venv/bin/python reasoner_check.py
.venv/bin/python scalability_benchmark.py --sizes 100 1000
git diff --check
.venv/bin/python oops_check.py
```

### Exact results
- **reused_class_scope_test.py:** PASS (9-cell matrix).
- **random_seed_test.py:** PASS (ISSUE-03 regression).
- **negative_test.py:** 11/11 FOUND; negative graph 209 triples; shape triples 386. (Fewer incidental Offer/Model/Run hits on unlinked stubs — expected after scoping; INV-1..INV-9 and AUTH-* still fire.)
- **validate.py:** ontology 620 / shapes **386** / data 233; SHACL **conforms=True**; 23/23 CQs; CQ-D3=2, CQ-E1=2, CQ-G3=1; ISSUE-02 separation PASS.
- **reasoner_check.py:** merged 853; HermiT consistent **1.46 s**; OWL-RL 853→2048 (1195), **0.64 s**; 0 forbidden entailments; `ExecutionAuthorization ⊑ Thing, Entity`.
- **benchmark:** 100 units 8753 data, parse 0.462 / OWL-RL 5.997 / SHACL 13.516 / SPARQL 0.276, conforms; 1000 units 87053 data, parse 5.351 / OWL-RL 58.816 / SHACL 170.883 / SPARQL 20.041, conforms.
- **git diff --check:** no warnings on this run.
- **OOPS!:** TimeoutError (120 s) contacting `oops.linkeddata.es`.

### Documentation and reports updated
`daimo-shapes.ttl`, `CHANGELOG.md`, docs 00–04, `docs/02` §4.3, `reports/reused-class-scope-results.md`, plus regenerated validation/reasoner/negative/scalability reports.

### Remaining limitations or risks
1. WIDOCO copies under `daimo/docs/` still contain the old `sh:targetClass` axioms; runtime validation loads `daimo/shapes/`.
2. INV-2 remains `sh:targetClass it6:Run` but SPARQL-scoped; documented, not a conformance-shape leak.
3. A model that is only `it6:evaluates`’d under a `SharedEvaluationContext` is **not** selected by `MachineLearningModelInDAIMOShape` (by design: not offered/deployed).
4. OOPS! still unreachable.

### Final status
**RESOLVED** — acceptance criteria 1–9 met.

---

## Integrated audit of DAIMO-ISSUE-01..04

### Repository and base state
- Branch `main`, HEAD `2ae0c6dd47b6b08e07b2f4b350340f5097c721e3` (ISSUE-01 commit). ISSUE-02..04 are uncommitted working-tree changes on top of that commit. No tag, release, commit, push or PR was created for 02–04.
- `owl:versionInfo` **0.1.6** throughout.

### Final changed-file inventory
Ontology/shapes/example/tests/queries/scripts/docs/reports for issues 01–04, plus `paper/evidence-matrix.md` and `paper/CHOWLK-DRAWING-GUIDE.md`. Paper `.tex`/`.pdf` leftovers and `Zone.Identifier` are **not** part of this bundle.

### Final ontology inventory
- 14 native classes; **31** object properties; **8** datatype properties; **29** functional declarations; **7** asymmetric; 5 `owl:inverseOf`.
- Native additions in this bundle: `daimo:forService` (ISSUE-01), `daimo:derivedFromAgreement` (ISSUE-02).
- `ExecutionAuthorization ⊑ prov:Entity`, **not** `odrl:Agreement`. `grantedTo` **not** `⊑ odrl:assignee`. `randomSeed` still functional, now 0..1 in SHACL.

### Final SHACL inventory
- 9 completeness shapes (DAIMO classes; `randomSeed` 0..1).
- 4 conformance shapes, all `sh:targetObjectsOf` on DAIMO properties (Offer, Agreement, Model, Run).
- 9 SHACL-SPARQL invariants (INV-1..INV-9).
- Shape triples: **386**.

### CQ results
23/23 ≥1 row. CQ-D3=2, CQ-E1=2 (no cartesian product). CQ-G3=1 with distinct auth≠agreement. CQ-V1=1 (seed optional). CQ-V2=1, CQ-V3=2.

### Reasoner results
HermiT consistent, 0 unsatisfiable, 1.46 s. OWL-RL 853→2048 (1195), 0.64 s, 0 `owl:Nothing`, 0 forbidden entailments (no `Agreement`/`Policy` on `ExecutionAuthorization`). `ExecutionAuthorization ⊑ Thing, Entity`.

### Negative-test results
- INV-1..INV-9 + AUTH-no-agreement + AUTH-bad-agreement: **11/11**.
- ISSUE-01: INV-7/INV-8 fire.
- ISSUE-03: 0 seed OK; 2 seeds and bad type rejected (`random_seed_test.py`).
- ISSUE-04: 9-cell matrix PASS (`reused_class_scope_test.py`).

### Scalability results
100 units: 8753 data triples, 17198 closure, conforms, 100 auth→agreement pairs (parse 0.462 / OWL-RL 5.997 / SHACL 13.516 / SPARQL 0.276 s). 1000 units: 87053 data triples, 156698 closure, conforms, 1000 pairs (parse 5.351 / OWL-RL 58.816 / SHACL 170.883 / SPARQL 20.041 s).

### OOPS! status
Service timeout. Last stored scan (2026-07-08): 0 Critical, 0 Important, 2 Minor. Predates `forService` / `derivedFromAgreement`. Not cited as a new result.

### Documentation consistency check
docs 00–04, ORSD CQs, CHANGELOG Unreleased, evidence-matrix and CHOWLK guide updated for all four issues. WIDOCO `daimo/docs/` **not** regenerated.

### Unresolved warnings
- OOPS! unreachable.
- WIDOCO stale copies of alignment/shapes.
- Expert validation (SWJ C9) still pending (pre-existing).
- `git diff --check` clean on this audit run.

### Versioning recommendation
Keep **one** Unreleased bundle. After human review, a **single** version bump is recommended: **0.2.0** (new properties `forService` and `derivedFromAgreement`; breaking removal of `ExecutionAuthorization ⊑ odrl:Agreement`; SHACL target narrowing). If the SWJ freeze must remain on the 0.1 line, use **0.1.7** with the same Unreleased notes. Do **not** increment four times.

### Overall conclusion
ISSUE-01, ISSUE-02, ISSUE-03 and ISSUE-04 are **RESOLVED** on the local working tree. Specific harnesses and the shared validate/reasoner/negative/benchmark suite all passed. No commit, push, tag, release or PR was made.
