# DAIMO External Expert Validation Protocol

This protocol is the minimum human validation package needed before claiming
external validation in the SWJ submission. It does not replace expert review;
it only makes the review structured and reproducible.

## Expert Profiles

Recruit three independent reviewers:

| Profile | Required expertise | Focus |
|---|---|---|
| E1 | Ontology engineering / Semantic Web | Modelling quality, reuse, OWL/SHACL choices, publication quality. |
| E2 | Dataspaces / EDC / DSP | Dataspace realism, contract and participant-context assumptions. |
| E3 | ML / MLOps / model governance | Model lifecycle, deployment, evaluation, auditability, comparability. |

## Materials Sent to Experts

- `paper/daimo-paper-es-v4.pdf` or `paper/daimo-paper-en-swj-v4.pdf`.
- `daimo/ONTOLOGY-REFERENCE.md`.
- `daimo/VALIDATION-MATRIX.md`.
- `daimo/REPRODUCIBILITY.md`.
- `daimo/examples/flood-risk-scenario.ttl`.
- `daimo/shapes/daimo-shapes.ttl`.
- `daimo/queries/queries.md`.

## Review Questions

Ask every expert to answer:

1. Are the DAIMO competency questions sufficient for governed AI-model exchange in dataspaces?
2. Are any DAIMO-native classes unnecessary or missing?
3. Are the alignments to MLDCAT-AP, DCAT, ODRL, PROV-O, DSP/EDC defensible?
4. Are the six SHACL-SPARQL invariants meaningful and operationally realistic?
5. Does the anonymised scenario cover a plausible exchange without overclaiming deployment validation?
6. What would block adoption in your domain?
7. What change would most improve the paper before SWJ submission?

## Recording Template

| Expert | Profile | Observation | Severity | Action | Impact on DAIMO | Status |
|---|---|---|---|---|---|---|
| E1 | Ontology/SW |  | Major/Minor/Editorial | Accepted/Rejected/Future work |  | Open |
| E2 | Dataspaces/EDC |  | Major/Minor/Editorial | Accepted/Rejected/Future work |  | Open |
| E3 | ML/MLOps |  | Major/Minor/Editorial | Accepted/Rejected/Future work |  | Open |

## Paper Integration Rule

Only report this as validation after the reviews have happened. Until then,
the paper should say that executable validation is complete and expert
validation is pending or planned.

