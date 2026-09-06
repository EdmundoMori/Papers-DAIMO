# Execution provenance

This report records a local re-run of an existing DAIMO harness.

- Evaluated source commit (ontology, shapes, examples, queries, tests): `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- HEAD at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- `v0.1.7^{}` at execution: `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`
- Command: `sha256 of protected sources (before)`
- Started (UTC): 2026-09-06T11:52:34Z
- Finished (UTC): 2026-09-06T11:52:34Z
- Working-tree status (`git status -sb`): `## main...origin/main
?? daimo/reports/_eval_runner.py
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


## Protected-file checksums (before)

Files: 18

| SHA-256 | bytes | path |
|---|---:|---|
| `4a241f073ae3e3b231bb00081aad0159b75a6dcab3ae59044d94c2578f2613bc` | 14378 | `daimo/examples/flood-risk-scenario.ttl` |
| `9615fd4e3f371d9f8b680d6fe47307ec6781d4c33e7fae3bb1b28e3344e46b41` | 22719 | `daimo/ontology/alignment.ttl` |
| `e6ab04b21e7480e974f5deb21d3a85b77ecff13daaf68b330f08f67f52eb56be` | 37271 | `daimo/ontology/daimo-core.ttl` |
| `1f6338c7a96ef2e6143696348d75fe18d081eeb1b0246073b3939e30d25fcbf1` | 14060 | `daimo/queries/queries.md` |
| `6a7a2ef7ce2c13a081d4e0e4ecb3221e183e9188520ba0b00bb4809974cbac7c` | 26804 | `daimo/shapes/daimo-shapes.ttl` |
| `d38930a32ecfbcf4805bbd16538b0a8a634fbff481c7744d15429bbfabad49d0` | 14682 | `daimo/tests/negative-examples.ttl` |
| `0aa1edd12813020aac985f06c20a8ca6f4dfc6126a831a06ad916be649102373` | 4246 | `daimo/tests/negative_test.py` |
| `2f7e411614aece16e080e0be66e3054477baecc5f34730da09e37dbb801fbee4` | 777 | `daimo/tests/random-seed-badtype.ttl` |
| `dbba1b40f9a21808682437dd4a6f191031cdcad844894be8e77a7c3217dd02ac` | 793 | `daimo/tests/random-seed-two.ttl` |
| `12fe2372fc8c569a921d8318c0648845b33768fa7985058ab02694aa080edfac` | 5417 | `daimo/tests/random_seed_test.py` |
| `4969a9e3758ce02993c2a81696ea24dd4d072d49fa2019564a94b2225254c5ef` | 2239 | `daimo/tests/reused-class-scope/daimo-complete.ttl` |
| `e06ab71d8b3f2d404e2fb0a8f59b62c5c58694e472dbad51b3cc672becf5392d` | 996 | `daimo/tests/reused-class-scope/daimo-model-incomplete.ttl` |
| `f11508044e8c7e75510ffd8a5c7e944af08f46bc0b86c9cad580d4a3a9ca1dee` | 1190 | `daimo/tests/reused-class-scope/daimo-offer-incomplete.ttl` |
| `1bc3bb231212e96e35665b188ceda20fccab10478642500098d7e591996b0f70` | 1095 | `daimo/tests/reused-class-scope/daimo-run-incomplete.ttl` |
| `39aaf0b446986a85a8b3b1fdc84655bd1e34afcea6195aabdb89a7c57539d000` | 1039 | `daimo/tests/reused-class-scope/external-incomplete.ttl` |
| `9269de6add4318db5651914dde7f96f4f362e5124bedf7e100c03892409d7d04` | 6314 | `daimo/tests/reused_class_scope_test.py` |
| `df2d1ec660c6478c3e6028168b3a90bfaf1ff00d08da87a6181efbdd1e4a522f` | 2089 | `daimo/tests/seedless-eval-context.ttl` |
| `058e3befd4c63eccf82e7e56f48180b9dd899133a803f8e34871ce1ff334f8f4` | 1863 | `daimo/tests/serialization_test.py` |
