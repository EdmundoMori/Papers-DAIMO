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
- Reasoning time: **1.7 s**

### OWL-RL materialisation (pure Python)
- Triples before: **818** → after: **1988** (**1170 inferred**)
- Reasoning time: **0.63 s**
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
`Evaluator ⊑ Role, ParticipantRole`; `ExecutionAuthorization ⊑ Agreement`;
`CrossParticipantProvenanceRecord ⊑ Bundle`; `IOContract ⊑ Thing` (stand-alone,
as intended); `SharedEvaluationContext ⊑ Thing` (stand-alone).

**Verdict: CONSISTENT.**

---

## 3. Ontology pitfalls: OOPS! (`oops-report.md`)

- Scan date **2026-07-08**, scope `daimo-core.ttl` + `alignment.ttl`, service
  `oops.linkeddata.es/rest`.
- **0 Critical, 0 Important, 2 Minor.**

| Pitfall | Elements | Interpretation |
|---|---|---|
| **P13** — inverse relationships not explicitly declared | 34 | **By design**: DAIMO declares inverses only for the four most-queried one-to-many relations; declaring inverses for every property would bloat the closure with no query benefit. |
| **P04** — unconnected ontology elements | 7 | **False positive**: the 7 elements (`prov:Bundle`, `dcat:Catalog`, `odrl:Permission`, `odrl:Agreement`, `dcat:CatalogRecord`, `dcat:Distribution`, `prov:Role`) are **external stubs** declared for reasoner resolution; they are connected in their source ontologies. |

Neither minor pitfall affects correctness; both have a documented rationale.

---

## 4. Structural validation + question answerability (`validation-results.md`)

Run over `alignment.ttl` + `daimo-core.ttl` + `daimo-shapes.ttl` +
`flood-risk-scenario.ttl`:

- Ontology triples: **593**; shape triples: **342**; example data triples:
  **225**.
- **SHACL conforms: True.**
- Materialised closure for CQ evaluation: **1988 triples**.
- **23 / 23 CQ SPARQL queries return ≥ 1 row.**

Per-CQ result (rows returned):

| CQ | rows | CQ | rows | CQ | rows | CQ | rows |
|---|---|---|---|---|---|---|---|
| CQ-R1 | 3 | CQ-D1 | 3 | CQ-E1 | 4 | CQ-V1 | 1 |
| CQ-R2 | 1 | CQ-D2 | 2 | CQ-E2 | 1 | CQ-V2 | 1 |
| CQ-R3 | 1 | CQ-D3 | 4 | CQ-E3 | 2 | CQ-V3 | 2 |
| CQ-R4 | 2 | CQ-D4 | 1 | CQ-E4 | 1 | CQ-V4 | 1 |
| CQ-R5 | 2 |  |  | CQ-E5 | 1 | CQ-V5 | 4 |
| CQ-G1 | 1 | CQ-G2 | 2 | CQ-G3 | 1 | CQ-G4 | 1 |

**Summary: 23/23 CQs answerable; SHACL conforms = True.**

---

## 5. Negative testing (`negative-test-results.md`)

A deliberately-violating graph (`daimo/tests/negative-examples.ttl`, **118
negative triples**) is validated to prove each invariant actually **fires**.

- **SHACL conforms: False** (expected).
- **6 / 6 invariants FOUND** on their designated focus nodes:
  INV-1 (`INV1-artifact`), INV-2 (`INV2-run`), INV-3 (`INV3-deployment`),
  INV-4 (`INV4-auth`), INV-5 (`INV5-offering`), INV-6 (`INV6-offering`).
- The harness prints `PASS: all 6 invariants fired on their designated focus
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
| 100 | 8 053 | 8 646 | 16 248 | 0.468 | 5.478 | 10.374 | 0.080 | True |
| 1 000 | 80 053 | 80 646 | 147 648 | 4.660 | 53.672 | 135.010 | 0.356 | True |

Query counts scale linearly (100/1000 offerings, invocation contracts and
authorised outputs; ranking capped at 10 by the query). **Observation:** the
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
| C7 SHACL conformance + invariants | Pass |
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
- **Comparability scope.** `SharedEvaluationContext` fixes task, dataset
  version, protocol and seed but does not normalise metric formulae or prove
  equivalence across benchmark protocols — that is left to metric/protocol
  profiles.
- **OOPS! minor pitfalls (P13, P04)** are retained deliberately (documented in
  §3); they are not defects.

---

## 10. One-paragraph summary (drop-in for the paper)

> DAIMO was evaluated with a reproducible pipeline covering logical consistency
> (HermiT: consistent, 0 unsatisfiable classes), entailment materialisation and
> verification (OWL-RL: 818→1988 triples, 0 `owl:Nothing`, 0 forbidden
> entailments over 14 classes), ontology pitfalls (OOPS!: 0 Critical, 0
> Important, 2 documented Minor), structural and cross-class constraint
> validation (SHACL: conforms on a 225-triple scenario graph via 9 completeness
> shapes, 3 conformance shapes and 6 governance invariants), question
> answerability (23/23 competency questions return results over the OWL-RL
> closure), negative testing (all 6 invariants fire on a purpose-built
> 118-triple violation graph), and bounded scalability (conformant at 100 and
> 1 000 synthetic exchange units, 80k data / 148k closure triples at 1 000
> units). The only partial criteria are external expert validation and the final
> FAIR publication steps (w3id redirect and Zenodo DOI).
