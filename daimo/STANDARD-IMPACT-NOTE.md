# DAIMO Standards Impact Note

This note records the standards that must be checked before the final SWJ
submission. It does not change DAIMO by itself.

Sources checked on 2026-07-06:

- MLDCAT-AP 3.1.0: https://semiceu.github.io/MLDCAT-AP/releases/3.1.0/
- MLDCAT-AP repository: https://github.com/SEMICeu/MLDCAT-AP
- Dataspace Protocol 2025-1: https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/2025-1/
- Dataspace Protocol repository: https://github.com/eclipse-dataspace-protocol-base/DataspaceProtocol

## MLDCAT-AP 3.1.0

Status observed: SEMIC Candidate Recommendation, published 2026-05-13.

Impact on DAIMO:

- DAIMO v0.1.6 is validated against MLDCAT-AP 3.0.0.
- The paper now explicitly states that MLDCAT-AP 3.1.0 must be checked before final submission.
- No ontology change has been made solely for 3.1.0 yet.

Required final action:

1. Compare the MLDCAT-AP 3.0.0 and 3.1.0 classes/properties used by DAIMO.
2. Confirm whether `it6:MachineLearningModel`, `it6:Run`, `it6:Flow`, `it6:Task`, `it6:Evaluation`, `it6:EvaluationMeasure`, `it6:Benchmark`, `it6:ComputerInfrastructure`, `it6:Hardware`, `it6:Library`, `it6:HarmRisk`, `it6:Modality`, `it6:trainedOn`, and `it6:testedOn` remain semantically compatible.
3. If compatible, state "no DAIMO changes required" in the paper.
4. If not compatible, update `alignment.ttl`, examples, shapes if needed, and rerun the full validation suite.

## Dataspace Protocol 2025-1

Status observed: stable release of the Eclipse Dataspace Protocol.

Impact on DAIMO:

- DAIMO uses DSP as an informative protocol layer, mainly around catalog, contract negotiation, transfer process, and ODRL agreements.
- DAIMO does not attempt to model the full DSP message schema.
- The paper now cites DSP 2025-1 and treats it as the final standard to check before submission.

Required final action:

1. Verify whether the `dspace:` namespace currently used in `alignment.ttl` remains acceptable for the target release.
2. Confirm that `ContractOffer`, `ContractNegotiation`, and `TransferProcess` remain valid informative mapping targets.
3. If DSP 2025-1 uses different canonical IRIs, update informative mappings only; rerun reasoner and CQ checks.

## Submission Decision

These checks are not blockers for the internal v4 master. They are blockers for
claiming final standards alignment in the SWJ submission.

