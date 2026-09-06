# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `daimo/.venv/bin/python tests/random_seed_test.py`
- Started (UTC): 2026-09-06T11:52:42Z
- Finished (UTC): 2026-09-06T11:52:43Z
- Working-tree status (`git status -sb`): `## main...origin/main
 M daimo/reports/negative-test-results.md
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
DAIMO-ISSUE-03 randomSeed optionality harness
========================================================================

[1] seedless context SHACL conforms: True
[2] CQ-V1 OPTIONAL rows=1
    protocol='leave-one-out' seed_bound=False
[3] CQ-V2/V3-style ranking rows=1 (must not require seed)
[4] two seeds SHACL conforms: False (expect False)
[5] non-integer seed SHACL conforms: False (expect False)

PASS: 0/1 seed allowed; 2 seeds and non-integer seed rejected; CQ-V1 OPTIONAL unbound; CQ-V2/V3 independent of seed.
