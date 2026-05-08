# Ontology Quality Foundations

Date: 2026-04-22
Purpose: establish the theoretical bar that DAIMO must meet. This document is
the reference frame for [daimo-design-rationale.md](daimo-design-rationale.md),
which evaluates the DAIMO artefact against every criterion introduced here.

The document is organised around one question: **what makes an ontology good?**
Six sub-questions follow:

1. What is an ontology and what is it *for*?
2. What kinds of ontologies exist, and which kind is DAIMO?
3. What design principles are universally accepted?
4. What quality dimensions and pitfalls are measured in the literature?
5. What evaluation methods are recognised at venues such as the Semantic Web
   Journal?
6. What does the LOT methodology prescribe, and how does it relate to the
   above?

Every section ends with an *implication for DAIMO* line so the theory remains
connected to the artefact.

---

## 1. What an ontology is and what it is for

### 1.1 Definitions that shape the field

The operational definition used across the Semantic Web community descends
from three statements:

- **Gruber (1993)**: *"An ontology is an explicit specification of a
  conceptualization."* The emphasis is on being explicit (machine-readable)
  and on a shared conceptualisation (not a private data model).
- **Studer, Benjamins, Fensel (1998)**: *"An ontology is a formal, explicit
  specification of a shared conceptualization."* Adds *formal* (logically
  precise) and *shared* (community-validated).
- **Guarino (1998)**: distinguishes an ontology proper (the logical theory)
  from a conceptualisation (the set of intended meanings). An ontology is the
  theory that approximates a conceptualisation as precisely as possible.

### 1.2 What ontologies are actually for

In practice, ontologies carry four loads simultaneously:

- **Shared vocabulary** — terms that mean the same thing across systems.
- **Machine-actionable semantics** — structure a reasoner or SHACL engine can
  use, not only narrative text.
- **Integration contract** — a stable surface that several data sources,
  applications, or organisations can map onto.
- **Governance artefact** — a declarative record of what distinctions the
  community considers important.

Not every ontology needs to carry all four. A controlled vocabulary (SKOS)
carries the first, a lightweight ontology (OWL) adds the second, a reference
ontology (BFO, DOLCE) emphasises the third and fourth.

**Implication for DAIMO.** DAIMO is explicitly an *integration contract* for
governed AI-model exchange in data spaces. Its primary utility is the third
load. Expectations about expressiveness should be calibrated to that role,
not to foundational-ontology expectations.

---

## 2. Kinds of ontologies and where DAIMO sits

Two orthogonal classifications recur in the literature.

### 2.1 By level of generality (Guarino 1998)

- **Top-level / foundational ontology** — concepts independent of a domain
  (BFO, DOLCE, GFO, UFO). Provide ontological commitments about time, space,
  endurants vs perdurants, roles, parthood.
- **Core / upper-domain ontology** — concepts common to a broad family of
  domains (e.g., IOF Core for industrial engineering; BBO for business
  processes).
- **Domain ontology** — concepts of a specific domain (FoodOn for food,
  GloSIS for soils, MAINT for industrial maintenance).
- **Application / task ontology** — concepts of a task in a domain (e.g., an
  ontology for auditing an AI inference in a data space).

### 2.2 By purpose (Gómez-Pérez, Fernández-López, Corcho 2004)

- **Reference ontology** — intended for re-use and conceptual precision.
- **Application profile** — intended for operational use within a specific
  infrastructure (DCAT-AP, MLDCAT-AP, DAIMO).
- **Application ontology** — instantiated per application, often not
  reusable.

### 2.3 By formal expressiveness

From least to most expressive: controlled vocabularies → taxonomies →
thesauri (SKOS) → lightweight OWL → OWL 2 DL → OWL 2 Full → first-order
logic with SWRL rules.

**Implication for DAIMO.** DAIMO is a **domain-level application profile**,
OWL 2 DL, built as an integration layer over existing W3C/SEMIC/EDC
vocabularies. It is not a foundational ontology and should not claim to be.
This classification immediately constrains the critique: DAIMO does not have
to settle time semantics or role theory, but it does have to be conceptually
crisp about the small set of terms it introduces.

---

## 3. Design principles that are universally accepted

Four sources are most frequently cited when reviewers justify a design
comment.

### 3.1 Gruber's five design criteria (1995)

- **Clarity** — definitions should be objective and independent of the
  application context.
- **Coherence** — inferences must be consistent with definitions; no
  contradictions.
- **Extendibility** — new terms can be added without revising existing
  definitions.
- **Minimal encoding bias** — conceptualisation at the knowledge level, not
  the implementation level.
- **Minimal ontological commitment** — make the weakest theory consistent
  with intended use; do not impose commitments not needed by applications.

### 3.2 Noy and McGuinness's seven rules (2001)

The "Ontology Development 101" checklist that most engineering tutorials
still use:

- There is no single correct way; multiple viable alternatives exist.
- Development is iterative.
- Concepts should correspond to objects (physical or logical) and
  relationships in the domain of interest.
- Nouns form classes, verbs form relations.
- Subclasses should inherit *is-a* properly (not by meronymy or similarity).
- Sibling classes should be disjoint whenever the domain supports it.
- Start with a scope definition (competency questions).

### 3.3 OBO Foundry principles (Smith et al. 2007)

Fourteen operational principles for community ontologies. The ones DAIMO
cares about:

- **Open** licence that permits reuse (CC-BY most common).
- **Common shared format** (OWL + RDF serialisations).
- **Unique identifier** (IRIs under a stable namespace).
- **Versioning** (`owl:versionIRI`, `owl:versionInfo`).
- **Defined scope** (non-overlapping with sister ontologies).
- **Textual definitions** for every term.
- **Plurality of users** — real consumers, not synthetic ones.
- **Locus of authority** — one responsible maintainer group.

### 3.4 FAIR principles applied to ontologies (Poveda-Villalón et al. 2020)

Findable, Accessible, Interoperable, Reusable translated into ontology
practice:

- Persistent resolvable URIs (w3id, purl).
- Content negotiation: HTML for humans, RDF for machines.
- Imported terms declared, not copied.
- Machine-readable licence (`dct:license`) and ontology-level metadata
  (title, creator, versionIRI, issued, modified).
- Community standards for documentation (WIDOCO, pyLODE) and validation
  (SHACL).

**Implication for DAIMO.** The revised DAIMO class set was derived from a
strict application of Gruber's *minimal ontological commitment* (do not
redefine `it6:MachineLearningModel`), Gruber's *extendibility* (the seven
native classes are additive, not substitutive), and FAIR (persistent IRI,
versionIRI, licence, content negotiation are explicit acceptance criteria).

---

## 4. Quality dimensions and pitfalls

### 4.1 The quality-dimension literature

Gangemi et al. (2005) organise ontology quality into three families:

- **Structural** — topology, modularity, depth, breadth, fan-out, proper
  use of disjointness, correct use of OWL features. Measurable
  automatically.
- **Functional** — does the ontology answer the competency questions over
  realistic data? Measurable by executing SPARQL over an example KG.
- **Usability** — do humans understand, reuse, and maintain it? Measurable
  only through user studies or adoption signals.

Duque-Ramos et al. (2011) added OQuaRE, adapting ISO/IEC 25000 software
quality characteristics to ontology engineering.

### 4.2 The OOPS! pitfall catalogue (Poveda-Villalón et al. 2014)

Forty-one pitfalls grouped by severity. The most common critical ones at
SWJ:

- **P05** — Defining wrong inverse relationships.
- **P07** — Merging different concepts in the same class.
- **P08** — Missing annotations (rdfs:label, rdfs:comment).
- **P10** — Missing disjointness.
- **P11** — Missing domain or range on properties.
- **P13** — Inverse relationships not explicitly declared.
- **P19** — Defining multiple domains or ranges on one property.
- **P22** — Using different naming conventions.
- **P24** — Recursive definitions.
- **P30** — Missing equivalent properties.
- **P41** — No licence declared.

Passing OOPS! with zero critical pitfalls is now the de-facto minimum for
SWJ ontology tracks.

### 4.3 OntoClean (Guarino & Welty 2002)

A method for cleaning taxonomic mistakes by tagging classes with four
metaproperties:

- **Rigidity (+R / -R / ~R)** — is instancehood necessary across all
  worlds?
- **Identity (+I / -I)** — does instancehood carry identity criteria?
- **Unity (+U / -U)** — do instances have a whole-part theory?
- **Dependence (+D / -D)** — does instancehood require another entity?

Rules: anti-rigid classes cannot subsume rigid ones; classes with
identity criteria must not subsume classes without them; dependent classes
must not subsume independent ones.

OntoClean is mostly applied to foundational and domain ontologies;
application profiles such as MLDCAT-AP and DAIMO rarely run a full
OntoClean audit but benefit from at least checking that role-like classes
(e.g., `daimo:ParticipantRole`) are modelled as anti-rigid roles rather
than natural kinds.

**Implication for DAIMO.** DAIMO inherits OOPS! compliance as an acceptance
criterion. OntoClean is applied informally to the `ParticipantRole`
hierarchy (roles are anti-rigid and dependent on the agents that play
them — this is why DAIMO uses `daimo:hasRole` rather than making agents
themselves subclasses of role classes).

---

## 5. Evaluation methods accepted at SWJ

Cross-paper evidence from the eight SWJ comparators (see
[swj-cq-patterns.md](swj-cq-patterns.md)) identifies five evaluation layers.
A paper typically needs at least three.

### 5.1 Syntactic and profile validation

Parse the Turtle/RDFXML, check OWL 2 DL profile membership with Protégé or
the OWL API profile checker. Zero-cost, non-negotiable.

### 5.2 Logical consistency

Run HermiT / Pellet / ELK. Report: reasoning time, unsatisfiable classes
(should be 0), entailment check of at least one domain-relevant inference.

### 5.3 Pitfall scanning

Run OOPS!. Report: scorecard, resolutions for each critical pitfall.

### 5.4 Functional validation — CQ answering

For each competency question, write a SPARQL query against a populated
example KG and verify the query returns the expected rows. The ratio
*CQs answered / CQs stated* is a quality signal reviewers explicitly look
at.

### 5.5 Structural validation — SHACL

Express minimum-completeness expectations as SHACL shapes. Validate the
example KG against them. Reviewers treat SHACL pass as a statement about
the KG, not only about the ontology; so SHACL validates that the KG used
to answer CQs is itself well-formed.

### 5.6 External validation

At least one of:

- Case study with real data (NutriLink, GloSIS, MAINT).
- Expert interviews with declared participants (ANNO).
- Adoption signal (FAO picked up GloSIS, EU DPP context picked up RePlanIT).

No published SWJ ontology paper has skipped external validation entirely
without severe review comments.

**Implication for DAIMO.** The DAIMO artefact built today covers layers
5.1, 5.2 (once HermiT run), 5.4, 5.5. OOPS! (5.3) and External validation
(5.6) remain open — these are the highest-leverage remaining items.

---

## 6. The LOT methodology as a synthesis

LOT (Poveda-Villalón, Fernández-Izquierdo, Fernández-López, García-Castro
2022) structures an engineering process that operationalises the theory
above. Four phases:

### 6.1 Phase 1 — Requirements specification

- Collaborate with users.
- Produce an **Ontology Requirements Specification Document (ORSD)**.
- Elicit competency questions in natural language.
- Elicit non-functional requirements (OWL profile, licence, multilingual,
  FAIRness, reuse commitments).

### 6.2 Phase 2 — Implementation

Four sub-activities, iterated:

- **2a Conceptualisation** — Chowlk diagrams, module structure, initial
  OWL.
- **2b Reuse** — for every term, decide reuse vs new; justify every
  addition.
- **2c Encoding** — OWL serialisation, full annotation (labels, comments,
  metadata).
- **2d Evaluation** — syntactic + logical + structural + functional +
  pitfall validation.

### 6.3 Phase 3 — Publication

- Generate HTML documentation with WIDOCO.
- Publish under content-negotiated persistent URI (w3id, purl).
- Deposit a tagged release with DOI (Zenodo).
- Release candidate review with stakeholders before publication.

### 6.4 Phase 4 — Maintenance

- Issue tracker, deprecation policy, versioning governance.
- Scheduled iterations for new requirements and errors.

LOT therefore synthesises:
- **Gruber/Noy-McGuinness** → phase 2a conceptualisation.
- **OBO/FAIR** → phase 3 publication.
- **Gangemi/OOPS!/OntoClean** → phase 2d evaluation.
- **NeOn 9 reuse scenarios** → phase 2b reuse (explicit reuse of terms and
  re-engineering of non-ontological resources).

**Implication for DAIMO.** LOT is the correct methodological anchor. DAIMO
v0.1.0 has executed phases 1 and 2 completely, and partially executed
phase 3 (namespace declared, licence, metadata) with the remaining parts
(WIDOCO, Zenodo DOI, live redirect) listed as next steps. Phase 4 is not
yet applicable.

---

## 7. Ten acceptance criteria distilled for DAIMO

From sections 1–6, the criteria any ontology paper must meet at SWJ:

| # | Criterion | Source |
|---|---|---|
| C1 | Scope is explicit and operationally bounded | §1.1, §2.2 |
| C2 | Engineering methodology is named and followed | §6 (LOT) |
| C3 | Competency questions are stated in natural language, numbered, and grouped | §5.4, SWJ evidence |
| C4 | Reuse of existing vocabularies is explicit and justified per term | §3.1 (Gruber minimal commitment), LOT 2b |
| C5 | OWL 2 DL profile, zero unsatisfiable classes, reasoner report | §5.1, §5.2 |
| C6 | OOPS! scan with zero critical pitfalls, results reported | §4.2 |
| C7 | SHACL shapes express minimum-completeness and validate against the example KG | §5.5 |
| C8 | Each CQ is answered by a SPARQL query that returns expected rows | §5.4 |
| C9 | External validation: case study with real or realistic data, plus expert or adoption signal | §5.6 |
| C10 | FAIR publication: persistent URI, CC-BY licence, HTML docs, DOI, versionIRI, ontology-level metadata | §3.4 (FAIR), OBO principles |

This ten-point list is the exact framework used to critique DAIMO in
[daimo-design-rationale.md](daimo-design-rationale.md).

---

## 8. Frequently misapplied ideas (traps)

### 8.1 "My ontology is DCAT-AP" — profile is not the same as ontology

An **application profile** reuses, constrains, and extends one or more
reference vocabularies. A profile is not a new ontology merely because it
adds local constraints. A profile becomes an ontology when it introduces
new classes or properties with novel semantics that cannot be expressed
by the reused vocabularies.

### 8.2 "I reused DCAT" — listing is not reuse

Reviewers distinguish *declarative reuse* (listing namespaces in a table)
from *axiomatic reuse* (writing `rdfs:subClassOf` / `rdfs:subPropertyOf` /
`skos:exactMatch` axioms). Only the latter is machine-checkable.

### 8.3 "I validated 14/19 CQs" — the ratio is treated as a quality signal

A ratio below 100% is not automatically bad, but must be *explained*: each
unimplemented CQ must be labelled as "requires richer semantics" or
"requires additional graph data", with a specific cause.

### 8.4 "SHACL shapes pass" — does not replace logical consistency

SHACL is structural, not deductive. A SHACL pass says nothing about
consistency under reasoning. Both checks are needed.

### 8.5 "My case study is illustrative" — needs a declaration

Reviewers accept illustrative case studies only if the paper explicitly
declares them as demonstrators, not as adoption evidence. A synthetic
graph presented as "evaluation" is a red flag.

### 8.6 "Future work will add experts" — does not substitute current validation

External validation is a current-paper obligation, not a future-work item.

**Implication for DAIMO.** Sections 4–6 of the DAIMO paper rewrite must
explicitly navigate traps 8.1, 8.2, 8.5 (current paper fails on 8.1 and 8.2
because the draft lists reuse without axiomatising it; see the design
rationale document for the fix).

---

## 9. Summary — what a "good" ontology looks like at SWJ

- Narrow, operational scope.
- Named methodology, iterative evidence.
- Numbered competency questions in natural language.
- Reuse declared with alignment axioms, not prose.
- OWL 2 DL, reasoner-consistent, OOPS!-clean.
- SHACL shapes with a conforming example graph.
- SPARQL that answers every CQ.
- A case study readers recognise as realistic.
- At least one external validation signal.
- FAIR publication with persistent URI, licence, docs, DOI.

This list is the contract. The next document checks every line of the
contract against the DAIMO artefact built on 2026-04-22.

---

## References

- Gruber, T. R. (1993). A translation approach to portable ontology
  specifications. *Knowledge Acquisition* 5(2): 199–220.
- Gruber, T. R. (1995). Toward principles for the design of ontologies used
  for knowledge sharing. *International Journal of Human-Computer Studies*
  43(5–6): 907–928.
- Studer, R., Benjamins, V. R., Fensel, D. (1998). Knowledge engineering:
  Principles and methods. *Data & Knowledge Engineering* 25(1–2): 161–197.
- Guarino, N. (1998). Formal ontology and information systems. In:
  *Proceedings of FOIS'98.*
- Guarino, N., Welty, C. (2002). Evaluating ontological decisions with
  OntoClean. *Communications of the ACM* 45(2): 61–65.
- Gangemi, A., Catenacci, C., Ciaramita, M., Lehmann, J. (2005). A
  theoretical framework for ontology evaluation and validation. In:
  *Proceedings of SWAP'05.*
- Noy, N. F., McGuinness, D. L. (2001). Ontology Development 101: A Guide
  to Creating Your First Ontology. *Stanford Knowledge Systems Laboratory
  Technical Report KSL-01-05.*
- Smith, B., Ashburner, M., Rosse, C., et al. (2007). The OBO Foundry:
  coordinated evolution of ontologies to support biomedical data
  integration. *Nature Biotechnology* 25(11): 1251–1255.
- Wilkinson, M. D., Dumontier, M., Aalbersberg, Ij.J., et al. (2016). The
  FAIR Guiding Principles for scientific data management and stewardship.
  *Scientific Data* 3: 160018.
- Poveda-Villalón, M., Gómez-Pérez, A., Suárez-Figueroa, M. C. (2014).
  OOPS! (OntOlogy Pitfall Scanner!). *International Journal on Semantic
  Web and Information Systems* 10(2): 7–34.
- Poveda-Villalón, M., Espinoza-Arias, P., Garijo, D., Corcho, O. (2020).
  Coming to Terms with FAIR Ontologies. In: *Proceedings of EKAW'20.*
- Poveda-Villalón, M., Fernández-Izquierdo, A., Fernández-López, M.,
  García-Castro, R. (2022). LOT: An industrial oriented ontology
  engineering framework. *Engineering Applications of Artificial
  Intelligence* 111: 104755.
- Suárez-Figueroa, M. C., Gómez-Pérez, A., Fernández-López, M. (2012).
  The NeOn Methodology for Ontology Engineering. In: *Ontology Engineering
  in a Networked World*, Springer, 9–34.
- Duque-Ramos, A., Fernández-Breis, J. T., Stevens, R., Aussenac-Gilles, N.
  (2011). OQuaRE: A SQuaRE-based Approach for Evaluating the Quality of
  Ontologies. *Journal of Research and Practice in Information Technology*
  43(2): 159–176.
