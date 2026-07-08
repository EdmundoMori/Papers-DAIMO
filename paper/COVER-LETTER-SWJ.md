# Cover letter — Semantic Web Journal (Description of ontology)

**Manuscript type:** Description of ontology  
**Title:** DAIMO: An Ontology for Governed AI Model Assets in Dataspaces  
**Authors:** Edmundo de Elvira Mori Orrillo, Jiayun Liu  
**Frozen artefact release:** https://github.com/EdmundoMori/Papers-DAIMO/releases/tag/v0.1.6-swj-submission

---

Dear Editors,

We submit **DAIMO (Dataspace AI Model Ontology)**, an OWL 2 DL integration
profile that connects DCAT-AP, MLDCAT-AP 3.0.0, ODRL 2.2, PROV-O, and the
Dataspace Protocol to treat AI models as first-class governed assets in
dataspaces.

## Contribution

DAIMO adds fourteen native classes (nine top-level bridge classes and five
participant-role subclasses) that neither MLDCAT-AP nor catalog/policy
vocabularies alone cover. The profile supports publication, discovery,
invocation, execution traceability, and contextualised evaluation across
participant boundaries. The paper reports **executable validation of the
ontology artefact** — not production deployment in a live dataspace
connector.

## Validation evidence (reproducible)

The submission package includes:

- OWL consistency (HermiT): 0 unsatisfiable classes
- OWL-RL materialisation and entailment verification
- SHACL conformance over the positive demonstrator graph
- Six cross-class SHACL-SPARQL invariants with a six-case negative test bench
- OOPS! scan (2026-07-08): 0 Critical, 0 Important, 2 Minor
- Twenty-three SPARQL-bound competency questions (23/23 pass on OWL-RL closure)
- Bounded synthetic scalability benchmark (100/1000 exchange units)

All scripts, reports, and replay instructions are in the repository directory
`daimo/` and frozen at tag `v0.1.6-swj-submission`.

## Relationship to related work

DAIMO is evaluated against **MLDCAT-AP 3.0.0**. MLDCAT-AP 3.1.0 is discussed
as a future evolution risk, not as an internal conformance checklist. The
requirements and demonstrator graph are anchored in a **bounded flood-risk
prediction scenario** inspired by PIONERA-style exchanges.

## FAIR publication status

For peer review, the **immutable GitHub release** is the authoritative
artefact snapshot. A w3id.org redirect configuration and Zenodo archival DOI
are prepared but require author credentials to activate; they will be completed
for the camera-ready version if accepted.

## Suggested reviewers

We suggest reviewers with expertise in:

- ontology engineering and LOT methodology;
- semantic web validation (OWL, SHACL, SPARQL);
- dataspace governance (DCAT, ODRL, DSP/EDC);
- ML metadata vocabularies (MLDCAT-AP, PROV-O).

## Declarations

- The manuscript is original and not under consideration elsewhere.
- All authors approve the submission.
- Validation evidence is reproducible from the frozen release without
  proprietary infrastructure.

Sincerely,

Edmundo de Elvira Mori Orrillo and Jiayun Liu  
Universidad Politécnica de Madrid
