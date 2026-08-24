#!/usr/bin/env python3
"""
DAIMO-ISSUE-03 — optional randomSeed regression harness.

Asserts, automatically (not by manual inspection):

1. A SharedEvaluationContext with no daimo:randomSeed SHACL-conforms.
2. CQ-V1-style OPTIONAL query recovers that context with ?seed unbound.
3. CQ-V2/CQ-V3-style ranking over that context still returns rows (seed
   is not in the join).
4. Two seeds on one context do NOT conform (sh:maxCount 1).
5. A non-xsd:integer seed does NOT conform (sh:datatype).

Exit 0 iff every assertion holds. Independent of pytest; follow
`python tests/random_seed_test.py` like `python tests/negative_test.py`.
"""
from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph
from pyshacl import validate as shacl_validate

ROOT = Path(__file__).resolve().parent.parent
ONT_DIR = ROOT / "ontology"
SHAPES_DIR = ROOT / "shapes"
TESTS = ROOT / "tests"

SEEDLESS = TESTS / "seedless-eval-context.ttl"
TWO = TESTS / "random-seed-two.ttl"
BADTYPE = TESTS / "random-seed-badtype.ttl"

CQ_V1 = """
PREFIX daimo: <https://w3id.org/pionera/daimo#>
PREFIX it6:   <http://data.europa.eu/it6/>
SELECT ?task ?dataset ?version ?protocol ?seed WHERE {
  <https://example.org/daimo-seedless/eval>
      daimo:usesEvaluationContext ?ctx .
  ?ctx daimo:contextTask    ?task ;
       daimo:contextDataset ?dataset ;
       daimo:datasetVersion ?version ;
       daimo:protocol       ?protocol .
  OPTIONAL { ?ctx daimo:randomSeed ?seed }
}
"""

CQ_V2V3 = """
PREFIX daimo: <https://w3id.org/pionera/daimo#>
PREFIX it6:   <http://data.europa.eu/it6/>
SELECT ?model ?value WHERE {
  ?eval a it6:Evaluation ;
        it6:evaluates ?model ;
        daimo:usesEvaluationContext <https://example.org/daimo-seedless/ctx> ;
        it6:hasEvaluationMeasure ?m .
  ?m it6:hasValue ?value .
}
ORDER BY DESC(?value)
"""


def load(files) -> Graph:
    g = Graph()
    for f in files:
        g.parse(f, format="turtle")
    return g


def shacl(data: Graph, shapes: Graph) -> tuple[bool, str]:
    conforms, _, report = shacl_validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
    )
    return conforms, report


def main() -> int:
    print("=" * 72)
    print("DAIMO-ISSUE-03 randomSeed optionality harness")
    print("=" * 72)
    ontology = load(sorted(ONT_DIR.glob("*.ttl")))
    shapes = load(sorted(SHAPES_DIR.glob("*.ttl")))
    failures: list[str] = []

    # 1–3. Seedless positive graph
    seedless = load([SEEDLESS])
    merged = Graph()
    for g in (ontology, seedless):
        for t in g:
            merged.add(t)
    conforms, report = shacl(merged, shapes)
    print(f"\n[1] seedless context SHACL conforms: {conforms}")
    if not conforms:
        failures.append("seedless context must conform")
        print(report[:1500])

    rows = list(merged.query(CQ_V1))
    print(f"[2] CQ-V1 OPTIONAL rows={len(rows)}")
    if len(rows) != 1:
        failures.append(f"CQ-V1 expected 1 row, got {len(rows)}")
    else:
        seed = rows[0]["seed"]
        protocol = str(rows[0]["protocol"])
        print(f"    protocol={protocol!r} seed_bound={seed is not None}")
        if seed is not None:
            failures.append("CQ-V1 ?seed must be unbound on a seedless context")
        if protocol != "leave-one-out":
            failures.append(f"unexpected protocol {protocol!r}")

    rank = list(merged.query(CQ_V2V3))
    print(f"[3] CQ-V2/V3-style ranking rows={len(rank)} (must not require seed)")
    if len(rank) < 1:
        failures.append("CQ-V2/V3-style query returned 0 rows on seedless context")

    # 4. Two seeds
    two = load([TWO])
    merged_two = Graph()
    for g in (ontology, two):
        for t in g:
            merged_two.add(t)
    conforms_two, report_two = shacl(merged_two, shapes)
    print(f"[4] two seeds SHACL conforms: {conforms_two} (expect False)")
    if conforms_two:
        failures.append("two seeds must NOT conform")
    elif "maxcount" not in report_two.lower() and "max count" not in report_two.lower():
        # pyshacl names MaxCountConstraintComponent
        if "MaxCountConstraintComponent" not in report_two:
            failures.append("two-seed violation was not a maxCount failure")
            print(report_two[:1200])

    # 5. Bad datatype
    bad = load([BADTYPE])
    merged_bad = Graph()
    for g in (ontology, bad):
        for t in g:
            merged_bad.add(t)
    conforms_bad, report_bad = shacl(merged_bad, shapes)
    print(f"[5] non-integer seed SHACL conforms: {conforms_bad} (expect False)")
    if conforms_bad:
        failures.append("non-integer seed must NOT conform")
    elif "DatatypeConstraintComponent" not in report_bad and "datatype" not in report_bad.lower():
        failures.append("bad-type violation was not a datatype failure")
        print(report_bad[:1200])

    print()
    if failures:
        print("FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS: 0/1 seed allowed; 2 seeds and non-integer seed rejected; "
          "CQ-V1 OPTIONAL unbound; CQ-V2/V3 independent of seed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
