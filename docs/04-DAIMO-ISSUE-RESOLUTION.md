# DAIMO Technical Issue Resolution Report

## Status summary
| ID | Issue | Status | Main files changed | Validation | Residual risk |
|---|---|---|---|---|---|
| DAIMO-ISSUE-01 | Unambiguous DataService–IOContract association | **RESOLVED** | `daimo-core.ttl`, `alignment.ttl`, `daimo-shapes.ttl`, `flood-risk-scenario.ttl`, `negative-examples.ttl`, `negative_test.py`, `queries.md`, `scalability_benchmark.py`, all `reports/*`, docs 00–03, `ORSD/daimo-cqs.md`, `CHANGELOG.md`, `paper/evidence-matrix.md` | SHACL conforms=True; 23/23 CQs; CQ-D3/CQ-E1 = 2 rows; 8/8 invariants fire; HermiT consistent; OWL-RL 0 `owl:Nothing`/0 forbidden entailments; benchmark 100/1000 conform | OOPS! not re-run (service unreachable); WIDOCO site under `daimo/docs/` not regenerated; git commit/push deferred to a separate step (per instructions) |

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
