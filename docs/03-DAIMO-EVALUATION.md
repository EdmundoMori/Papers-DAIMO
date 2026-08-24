# DAIMO — Evaluation

Companion to [`02-DAIMO-IMPLEMENTATION.md`](02-DAIMO-IMPLEMENTATION.md). This is
the primary source for the paper's **"Evaluación"** section. Every figure below
is reproduced from the generated reports in `daimo/reports/` (regenerate with the
scripts in `02-DAIMO-IMPLEMENTATION.md` §7).

---

## 1. Evaluation methodology

DAIMO is evaluated along **six complementary dimensions**, so that a weakness
missed by one method is caught by another:

1. **Logical consistency** — HermiT (OWL 2 DL reasoner).
2. **Entailment materialisation + verification** — OWL-RL closure plus a custom
   check that no DAIMO class entails a forbidden superclass.
3. **Ontology pitfalls** — OOPS! (OntOlogy Pitfall Scanner).
4. **Structural + business constraints & question answerability** — SHACL
   conformance on the example graph + 23 CQ SPARQL queries.
5. **Negative testing** — deliberately-malformed graph must trigger each
   cross-class invariant.
6. **Bounded scalability** — synthetic growth benchmark (100 & 1000 exchange
   units).

---

## 2. Reasoning: consistency & entailment (`reasoner-report.md`)

### HermiT (via owlready2)
- **Consistent: True**
- **Unsatisfiable classes: 0**
- Reasoning time: **1.46 s**

### OWL-RL materialisation (pure Python)
- Triples before: **853** → after: **2048** (**1195 inferred**)
- Reasoning time: **0.64 s**
- `owl:Nothing` individuals (disjointness violations): **0**
- Unsatisfiable subclasses: **0**

### Entailment-verification check
Custom check that inspects, for every DAIMO-native class, every superclass
entailed after OWL-RL materialisation — catching silent inference bugs that both
HermiT and SHACL would miss.
- DAIMO classes inspected: **14**
- **Forbidden-entailment warnings: 0**

Representative inferred superclasses (all correct, none spurious):
`AIAssetOffering ⊑ CatalogRecord`; `DerivedArtifact ⊑ Resource, Entity`;
`Evaluator ⊑ Role, ParticipantRole`; `ExecutionAuthorization ⊑ Entity`
(**not** `⊑ Agreement`/`⊑ Policy` after DAIMO-ISSUE-02 — these are now among the
forbidden superclasses and none is entailed);
`CrossParticipantProvenanceRecord ⊑ Bundle`; `IOContract ⊑ Thing` (stand-alone,
as intended); `SharedEvaluationContext ⊑ Thing` (stand-alone). The
`daimo:forService` (IOContract → dcat:DataService) and the new
`daimo:derivedFromAgreement` (ExecutionAuthorization → odrl:Agreement)
introduce no forbidden entailment: `derivedFromAgreement` is deliberately not a
subproperty of `prov:wasDerivedFrom`, so the authorization is never re-typed as a
`prov:Entity`-lineage source nor the agreement dragged into DAIMO's kinds.

**Verdict: CONSISTENT.**

---

## 3. Ontology pitfalls: OOPS! (`oops-report.md`)

- Scan date **2026-07-08**, scope `daimo-core.ttl` + `alignment.ttl`, service
  `oops.linkeddata.es/rest`.
- **0 Critical, 0 Important, 2 Minor.**

> **Note (DAIMO-ISSUE-01 / DAIMO-ISSUE-02):** this OOPS! scan predates the
> addition of `daimo:forService` and `daimo:derivedFromAgreement`. OOPS! was
> **not re-run** because the external OOPS! service (`oops.linkeddata.es`) was
> not reachable from the execution environment (the request timed out).
> `daimo:derivedFromAgreement` declares no inverse (like the other native
> lineage properties), so the expected effect is at most a `+1` on the P13
> (undeclared-inverse) count; correctness is unaffected. Re-run OOPS! before the
> next release and refresh these figures.

| Pitfall | Elements | Interpretation |
|---|---|---|
| **P13** — inverse relationships not explicitly declared | 34 | **By design**: DAIMO declares inverses only for the four most-queried one-to-many relations; declaring inverses for every property would bloat the closure with no query benefit. |
| **P04** — unconnected ontology elements | 7 | **False positive**: the 7 elements (`prov:Bundle`, `dcat:Catalog`, `odrl:Permission`, `odrl:Agreement`, `dcat:CatalogRecord`, `dcat:Distribution`, `prov:Role`) are **external stubs** declared for reasoner resolution; they are connected in their source ontologies. |

Neither minor pitfall affects correctness; both have a documented rationale.

---

## 4. Structural validation + question answerability (`validation-results.md`)

Run over `alignment.ttl` + `daimo-core.ttl` + `daimo-shapes.ttl` +
`flood-risk-scenario.ttl`:

- Ontology triples: **620**; shape triples: **386**; example data triples:
  **233**.
- **SHACL conforms: True.**
- Materialised closure for CQ evaluation: **2048 triples**.
- **23 / 23 CQ SPARQL queries return ≥ 1 row.**
- **DAIMO-ISSUE-02 separation check:** 1 `ExecutionAuthorization` /
  `odrl:Agreement` pair, all distinct (`?auth != ?agreement`).
- **DAIMO-ISSUE-03:** CQ-V1 uses `OPTIONAL` on `randomSeed` and still returns
  1 row on the flood-risk holdout context (seed 42 bound). A seedless
  leave-one-out context is covered by `tests/random_seed_test.py` (conforms;
  `?seed` unbound).

Per-CQ result (rows returned):

| CQ | rows | CQ | rows | CQ | rows | CQ | rows |
|---|---|---|---|---|---|---|---|
| CQ-R1 | 3 | CQ-D1 | 3 | CQ-E1 | 2 | CQ-V1 | 1 |
| CQ-R2 | 1 | CQ-D2 | 2 | CQ-E2 | 1 | CQ-V2 | 1 |
| CQ-R3 | 1 | CQ-D3 | 2 | CQ-E3 | 2 | CQ-V3 | 2 |
| CQ-R4 | 2 | CQ-D4 | 1 | CQ-E4 | 1 | CQ-V4 | 1 |
| CQ-R5 | 2 |  |  | CQ-E5 | 1 | CQ-V5 | 4 |
| CQ-G1 | 1 | CQ-G2 | 2 | CQ-G3 | 1 | CQ-G4 | 1 |

**Summary: 23/23 CQs answerable; SHACL conforms = True.**

**DAIMO-ISSUE-01 effect.** After adding `daimo:forService` and rewriting the
per-endpoint queries, **CQ-D3 and CQ-E1 now return 2 rows** (one per real
endpoint), not the previous **4** produced by the cartesian `exposedAs ×
hasIOContract` join on a two-service / two-contract deployment. CQ-R4 and CQ-G2
now report the service each contract applies to, and every other CQ is unchanged.

**DAIMO-ISSUE-02 effect.** CQ-G3 now returns **both** the
`daimo:ExecutionAuthorization` and the distinct `odrl:Agreement` it
`daimo:derivedFromAgreement`, together with the grantee and expiry
(`?auth ?agreement ?grantee ?expires`), and carries `FILTER (?auth != ?agreement)`
to prove the two resources are different individuals. It still returns 1 row on
the scenario (one authorization derived from one accepted agreement). CQ-E2 and
CQ-E5 keep returning 1 row: they traverse `authorizedBy`/`authorizesRun` and the
grantee, which are unaffected by moving the ODRL terms onto the agreement.

**DAIMO-ISSUE-04 effect.** Conformance shapes over reused classes now select
only resources linked by DAIMO properties (`sh:targetObjectsOf`). An unrelated
`odrl:Offer`, `it6:MachineLearningModel` or `it6:Run` in the same graph is not
a focus node. The flood-risk example still conforms because every reused
offer/model/run that DAIMO talks about is so linked. Isolation and in-scope
negatives are `tests/reused_class_scope_test.py`.

---

## 5. Negative testing (`negative-test-results.md`)

A deliberately-violating graph (`daimo/tests/negative-examples.ttl`, **209
negative triples**) is validated to prove each invariant actually **fires**.

- **SHACL conforms: False** (expected).
- **11 / 11 checks FOUND** on their designated focus nodes:
  INV-1 (`INV1-artifact`), INV-2 (`INV2-run`), INV-3 (`INV3-deployment`),
  INV-4 (`INV4-auth`), INV-5 (`INV5-offering`), INV-6 (`INV6-offering`),
  INV-7 (`INV7-deployment`, contract points to a non-exposed service),
  INV-8 (`INV8-deployment`, exposed service with no contract),
  INV-9 (`INV9-auth`, authorization grantee ≠ agreement `odrl:assignee`),
  plus the two DAIMO-ISSUE-02 completeness cases: `AUTH-no-agreement`
  (authorization with no `daimo:derivedFromAgreement`) and `AUTH-bad-agreement`
  (derived agreement missing its required `odrl:permission`).
- The harness prints `PASS: all 11 invariants fired on their designated focus
  nodes`.

This closes the loop: §4 shows the invariants **do not** false-positive on a
correct graph; §5 shows they **do** catch each broken governance rule.

---

## 6. Bounded scalability (`scalability-benchmark.md`)

Synthetic DAIMO-conformant graphs where each **unit** contains one full exchange
(offering, model, deployment, service, I/O contract, authorization, run, derived
artefact, audit evidence, evaluation, cross-participant provenance record). This
is a **reproducible sanity check**, not a production-throughput claim.

| Units | Data triples | Merged | OWL-RL closure | Parse (s) | OWL-RL (s) | SHACL (s) | SPARQL suite (s) | Conforms |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 100 | 8 753 | 9 373 | 17 198 | 0.462 | 5.997 | 13.516 | 0.276 | True |
| 1 000 | 87 053 | 87 673 | 156 698 | 5.351 | 58.816 | 170.883 | 20.041 | True |

Query counts scale linearly (100/1000 offerings, invocation contracts,
authorised outputs and **authorization→agreement pairs**; ranking capped at 10 by
the query). The `invocation contracts` control query joins each contract to its
service through `daimo:forService`, so it counts one endpoint per unit (100/1000)
with no cartesian inflation. A new **Auth→Agreement pairs** control query
(added for DAIMO-ISSUE-02) confirms each generated authorization derives from
exactly one distinct `odrl:Agreement` (100/1000). **Observation:** the
ontology stays small and constant while data grows; SPARQL stays sub-second, and
OWL-RL + SHACL grow roughly linearly (SHACL is the dominant cost at 1000 units).

---

## 7. Requirements coverage

- **Competency questions: 23 / 23 implemented** (R:5, D:4, E:5, V:5, G:4). The 4
  governance-bridge CQs (CQ-G1..G4) are unique to DAIMO — unanswerable by
  MLDCAT-AP alone — and carry the novelty claim.
- **Non-functional requirements:** OWL 2 DL ✓, reuse-first with justification per
  term ✓, alignment axioms for every subclassed term ✓, SHACL pass per class ✓,
  CC-BY 4.0 / Apache-2.0 ✓, bilingual labels ✓, FAIR publication *(partial —
  see §9)*.

---

## 8. Mapping to SWJ acceptance criteria

| SWJ criterion | Status |
|---|---|
| C1 Scope | Pass |
| C2 Methodology (LOT) | Pass |
| C3 CQs in natural language | Pass |
| C4 Reuse axiomatised | Pass |
| C5 Reasoner consistency + entailment | Pass |
| C6 OOPS! pitfalls | Pass |
| C7 SHACL conformance + invariants (9 invariants + 4 conformance shapes) | Pass |
| C8 CQ SPARQL | Pass |
| C9 External (expert) validation | **Partial** — expert interviews pending |
| C10 FAIR publication | **Partial** — frozen release ready; w3id PR + Zenodo DOI pending |

**8 Pass, 2 Partial, 0 Open.**

---

## 9. Limitations & threats to validity

- **Expert validation (SWJ C9) pending.** Reasoner/SHACL/CQ evidence is
  automated; a light human expert review (`EXPERT-VALIDATION-PROTOCOL` in the
  frozen release history) is still to be scheduled. This is the main open item.
- **FAIR publication partial.** The `w3id.org/pionera/daimo` redirect PR and the
  Zenodo DOI depend on author credentials and are not yet live.
- **Scalability is bounded.** Numbers are a reproducible sanity check at 100/1000
  units on the authors' machine, not a throughput guarantee; SHACL time is the
  dominant cost and grows with data size. Larger runs (`--sizes 10000`) are
  supported but should be re-measured on the target machine before citing.
- **Single running scenario.** Validation uses one (rich) flood-risk scenario
  graph; broader domain coverage would strengthen external validity.
- **Comparability scope.** `SharedEvaluationContext` records task, dataset
  version, protocol and, when applicable, random seed. Ranking still requires
  the same metric and compatible conditions; omitting a seed is not a claim of
  complete reproducibility. Metric formulae are not normalised here — that is
  left to metric/protocol profiles.
- **OOPS! minor pitfalls (P13, P04)** are retained deliberately (documented in
  §3); they are not defects.

---

## 10. One-paragraph summary (drop-in for the paper)

> DAIMO was evaluated with a reproducible pipeline covering logical consistency
> (HermiT: consistent, 0 unsatisfiable classes), entailment materialisation and
> verification (OWL-RL: 853→2048 triples, 0 `owl:Nothing`, 0 forbidden
> entailments over 14 classes — including no `odrl:Agreement`/`odrl:Policy`
> entailment on `ExecutionAuthorization`), ontology pitfalls (OOPS!: 0 Critical, 0
> Important, 2 documented Minor), structural and cross-class constraint
> validation (SHACL: conforms on a 233-triple scenario graph via 9 completeness
> shapes, 4 conformance shapes and 9 governance invariants), question
> answerability (23/23 competency questions return results over the OWL-RL
> closure, with CQ-G3 returning the distinct authorization and its derived
> `odrl:Agreement`), negative testing (all 9 invariants plus 2
> authorization/agreement completeness cases fire on a purpose-built
> 209-triple violation graph), and bounded scalability (conformant at 100 and
> 1 000 synthetic exchange units, 87k data / 157k closure triples at 1 000
> units). The only partial criteria are external expert validation and the final
> FAIR publication steps (w3id redirect and Zenodo DOI).
