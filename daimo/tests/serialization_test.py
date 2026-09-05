#!/usr/bin/env python3
"""Assert public serialisations match the canonical core Turtle graph."""
from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "ontology" / "daimo-core.ttl"
DOCS = ROOT / "docs"


def load(path: Path, fmt: str) -> Graph:
    g = Graph()
    g.parse(path, format=fmt)
    return g


def main() -> int:
    print("=" * 72)
    print("DAIMO serialisation isomorphism harness")
    print("=" * 72)
    core = load(CORE, "turtle")
    serial = {
        "ttl": load(DOCS / "ontology.ttl", "turtle"),
        "owl": load(DOCS / "ontology.owl", "xml"),
        "jsonld": load(DOCS / "ontology.jsonld", "json-ld"),
        "nt": load(DOCS / "ontology.nt", "nt"),
    }
    failures: list[str] = []
    print(f"  core triples = {len(core)}")
    for name, g in serial.items():
        print(f"  docs/ontology.{name} triples = {len(g)}")
        if not core.isomorphic(g):
            failures.append(f"ontology.{name} is not isomorphic to daimo-core.ttl")
    shapes_src = load(ROOT / "shapes" / "daimo-shapes.ttl", "turtle")
    shapes_docs = load(DOCS / "daimo-shapes.ttl", "turtle")
    if not shapes_src.isomorphic(shapes_docs):
        failures.append("docs/daimo-shapes.ttl is not isomorphic to shapes/daimo-shapes.ttl")
    align_src = load(ROOT / "ontology" / "alignment.ttl", "turtle")
    align_docs = load(DOCS / "alignment.ttl", "turtle")
    if not align_src.isomorphic(align_docs):
        failures.append("docs/alignment.ttl is not isomorphic to ontology/alignment.ttl")
    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        return 1
    print("PASS: core serialisations and docs copies are isomorphic to sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
