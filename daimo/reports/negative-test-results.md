# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `daimo/.venv/bin/python tests/negative_test.py`
- Started (UTC): 2026-09-06T11:52:40Z
- Finished (UTC): 2026-09-06T11:52:41Z
- Working-tree status (`git status -sb`): `## main...origin/main
 M daimo/reports/reasoner-report.md
 M daimo/reports/validation-results.md
?? daimo/reports/_eval_runner.py
?? daimo/reports/checksums-protected-before.json
?? daimo/reports/checksums-protected-before.md
?? paper/DAIMO_PAPER.pdf
?? paper/DAIMO_v1.pdf
?? "paper/daimo-paper-es-v4 - copia.pdf:Zone.Identifier"
?? paper/daimo-paper-es-v4-1col.pdf
?? paper/fix_vertical_spacing.py
?? paper/sync_sage_editorial.py`
- Python: Python 3.10.12 (`daimo/.venv/bin/python`)
- Java: openjdk version "21.0.11" 2026-04-21 (exit 0)
- Relevant Python packages:
- rdflib==7.6.0
- pyshacl==0.31.0
- owlrl==7.6.1
- owlready2==0.51
- Process exit code: 0
- Harness verdict: **PASS**

Saving this file in a later git commit does **not** mean the tests evaluated
that later commit. The evaluated content is `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`.

---

========================================================================
DAIMO negative-test harness (cross-class invariants)
========================================================================
Ontology triples: 620
Shape triples   : 386
Negative triples: 209

SHACL conforms: False

  FOUND    INV-1  (looking for focus node containing 'INV1-artifact')
  FOUND    INV-2  (looking for focus node containing 'INV2-run')
  FOUND    INV-3  (looking for focus node containing 'INV3-deployment')
  FOUND    INV-4  (looking for focus node containing 'INV4-auth')
  FOUND    INV-5  (looking for focus node containing 'INV5-offering')
  FOUND    INV-6  (looking for focus node containing 'INV6-offering')
  FOUND    INV-7  (looking for focus node containing 'INV7-deployment')
  FOUND    INV-8  (looking for focus node containing 'INV8-deployment')
  FOUND    INV-9  (looking for focus node containing 'INV9-auth')
  FOUND    AUTH-no-agreement  (looking for focus node containing 'AUTH-no-agreement')
  FOUND    AUTH-bad-agreement  (looking for focus node containing 'AUTH-bad-agreement')

--- raw SHACL report (truncated) ---
Validation Report
Conforms: False
Results (13):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:class dcat:DataService ; sh:maxCount Literal("1", datatype=xsd:integer) ; sh:message Literal("An I/O contract must identify exactly one dcat:DataService it applies to (daimo:forService).", lang=en) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path daimo:forService ]
	Focus Node: [ <https://w3id.org/pionera/daimo#authMethod> Literal("api-key") ; <https://w3id.org/pionera/daimo#inputFormat> Literal("application/json") ; <https://w3id.org/pionera/daimo#outputFormat> Literal("application/json") ; rdf:type <https://w3id.org/pionera/daimo#IOContract>, rdfs:Resource ]
	Result Path: daimo:forService
	Message: An I/O contract must identify exactly one dcat:DataService it applies to (daimo:forService).
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:class odrl:Agreement ; sh:maxCount Literal("1", datatype=xsd:integer) ; sh:message Literal("An ExecutionAuthorization must derive from exactly one odrl:Agreement (daimo:derivedFromAgreement).", lang=en) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path daimo:derivedFromAgreement ]
	Focus Node: <https://example.org/daimo-negative/AUTH-no-agreement>
	Result Path: daimo:derivedFromAgreement
	Message: An ExecutionAuthorization must derive from exactly one odrl:Agreement (daimo:derivedFromAgreement).
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: [ sh:message Literal("An odrl:Agreement used as daimo:derivedFromAgreement must carry at least one odrl:permission (ODRL policy model).", lang=en) ; sh:minCount Literal("1", datatype=xsd:integer) ; sh:path odrl:permission ]
	Focus Node: <https://example.org/daimo-negative/AUTH-bad-agreement-notagreement>
	Result Path: odrl:permission
	Message: An odrl:Agreement used as daimo:derivedFromAgreement must carry at least one odrl:permission (ODRL policy model).
Constraint Violation in SPARQLConstraintComponent (http://www.w3.org/ns/shacl#SPARQLConstraintComponent):
	Severity: sh:Violation
	Source Shape: daimo:AuthorizationAgreementAssigneeInvariant
	Focus Node: <https://example.org/daimo-negative/INV9-auth>
	Value Node: <https://example.org/daimo-negative/INV9-auth>
	So

PASS: all 11 invariants fired on their designated focus nodes.
