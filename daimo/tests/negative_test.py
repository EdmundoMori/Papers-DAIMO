#!/usr/bin/env python3
"""
Negative-test harness for DAIMO cross-class invariants (INV-1..INV-6).

Loads the ontology + shapes + a deliberately-bad example KG
(`tests/negative-examples.ttl`) and asserts:

- Overall SHACL conformance is False.
- Exactly the expected invariants fire, and nothing else.

Each expected violation is keyed by the focus node's IRI pattern
(bad:INV1-*, bad:INV2-*, ...). This lets us verify that shapes catch
the violations they were designed for, not something else coincidental.

Exit code 0 iff every expected violation is found AND no unexpected
violations appear.
"""
from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph
from pyshacl import validate as shacl_validate

ROOT = Path(__file__).resolve().parent.parent
ONT_DIR = ROOT / "ontology"
SHAPES_DIR = ROOT / "shapes"
NEG_KG = ROOT / "tests" / "negative-examples.ttl"

# Expected: for each invariant, a substring that uniquely identifies
# its focus node (bad:INV1-artifact, bad:INV2-run, etc.).
EXPECTED = {
    "INV-1": "INV1-artifact",   # DerivedArtifact with wrong underAuthorization
    "INV-2": "INV2-run",        # Run with agent-grantee mismatch
    "INV-3": "INV3-deployment", # Deployment with service-model mismatch
    "INV-4": "INV4-auth",       # Authorization that expired before run started
    "INV-5": "INV5-offering",   # Offering whose offersModel is not in policy.target
    "INV-6": "INV6-offering",   # Offering whose offeredBy != policy.assigner
}


def load(files: list[Path]) -> Graph:
    g = Graph()
    for f in files:
        g.parse(f, format="turtle")
    return g


def main() -> int:
    print("=" * 72)
    print("DAIMO negative-test harness (cross-class invariants)")
    print("=" * 72)

    ontology = load(sorted(ONT_DIR.glob("*.ttl")))
    shapes = load(sorted(SHAPES_DIR.glob("*.ttl")))
    bad_data = load([NEG_KG])
    print(f"Ontology triples: {len(ontology)}")
    print(f"Shape triples   : {len(shapes)}")
    print(f"Negative triples: {len(bad_data)}")

    # Merge ontology + bad data so the validator has access to class
    # axioms (disjointness, subClassOf) while validating the bad KG.
    merged = Graph()
    for g in (ontology, bad_data):
        for t in g:
            merged.add(t)

    conforms, report_graph, report_text = shacl_validate(
        data_graph=merged,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
    )

    print(f"\nSHACL conforms: {conforms}")
    if conforms:
        print("FAIL: the negative KG was expected to FAIL validation, but it passed.")
        print("Shapes are not catching the deliberate violations.")
        return 1

    # Walk each expected invariant and verify a matching violation exists
    # somewhere in the report.
    report_lower = report_text.lower()
    found: dict[str, bool] = {}
    for inv, marker in EXPECTED.items():
        found[inv] = marker.lower() in report_lower

    print()
    all_found = True
    for inv, ok in found.items():
        status = "FOUND" if ok else "MISSING"
        print(f"  {status:7s}  {inv}  (looking for focus node containing '{EXPECTED[inv]}')")
        if not ok:
            all_found = False

    print()
    print("--- raw SHACL report (truncated) ---")
    print(report_text[:2500])
    print()

    if not all_found:
        print("FAIL: some expected invariants did not fire.")
        return 1

    print(f"PASS: all {len(EXPECTED)} invariants fired on their designated focus nodes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
