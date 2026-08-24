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
