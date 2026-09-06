# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `daimo/.venv/bin/python validate.py`
- Started (UTC): 2026-09-06T11:52:38Z
- Finished (UTC): 2026-09-06T11:52:40Z
- Working-tree status (`git status -sb`): `## main...origin/main
 M daimo/reports/reasoner-report.md
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

======================================================================
DAIMO validation runner
======================================================================

Ontology files : ['alignment.ttl', 'daimo-core.ttl']
Shape files    : ['daimo-shapes.ttl']
Example files  : ['flood-risk-scenario.ttl']

[1/3] Parsing Turtle files ...
  ontology triples : 620
  shape triples    : 386
  data triples     : 233

[2/3] Running SHACL validation ...
  conforms         : True

[3/3] Running CQ SPARQL queries ...
  found 23 CQ queries in queries.md
  materialised closure: 2048 triples
  PASS  CQ-R1     rows=3
  PASS  CQ-R2     rows=1
  PASS  CQ-R3     rows=1
  PASS  CQ-R4     rows=2
  PASS  CQ-R5     rows=2
  PASS  CQ-D1     rows=3
  PASS  CQ-D2     rows=2
  PASS  CQ-D3     rows=2
  PASS  CQ-D4     rows=1
  PASS  CQ-E1     rows=2
  PASS  CQ-E2     rows=1
  PASS  CQ-E3     rows=2
  PASS  CQ-E4     rows=1
  PASS  CQ-E5     rows=1
  PASS  CQ-V1     rows=1
  PASS  CQ-V2     rows=1
  PASS  CQ-V3     rows=2
  PASS  CQ-V4     rows=1
  PASS  CQ-V5     rows=4
  PASS  CQ-G1     rows=1
  PASS  CQ-G2     rows=2
  PASS  CQ-G3     rows=1
  PASS  CQ-G4     rows=1

[extra] DAIMO-ISSUE-02 authorization/agreement separation ...
  PASS  auths=1 distinct-pairs=1 collapsed=0 unlinked=0

======================================================================
Summary: 23/23 CQ queries return >=1 row; SHACL conforms=True; auth≠agreement separation=True
======================================================================
