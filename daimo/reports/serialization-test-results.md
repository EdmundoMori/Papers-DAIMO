# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `daimo/.venv/bin/python tests/serialization_test.py`
- Started (UTC): 2026-09-06T11:52:45Z
- Finished (UTC): 2026-09-06T11:52:46Z
- Working-tree status (`git status -sb`): `## main...origin/main
 M daimo/reports/negative-test-results.md
 M daimo/reports/random-seed-test-results.md
 M daimo/reports/reasoner-report.md
 M daimo/reports/reused-class-scope-results.md
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
DAIMO serialisation isomorphism harness
========================================================================
  core triples = 393
  docs/ontology.ttl triples = 393
  docs/ontology.owl triples = 393
  docs/ontology.jsonld triples = 393
  docs/ontology.nt triples = 393
PASS: core serialisations and docs copies are isomorphic to sources.
