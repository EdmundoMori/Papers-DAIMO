#!/usr/bin/env python3
"""Export daimo-core.ttl to docs/ontology.{ttl,owl,jsonld,nt} and sync copies."""
from __future__ import annotations

import shutil
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "ontology" / "daimo-core.ttl"
DOCS = ROOT / "docs"


def main() -> None:
    g = Graph()
    g.parse(CORE, format="turtle")
    DOCS.mkdir(parents=True, exist_ok=True)
    g.serialize(DOCS / "ontology.ttl", format="turtle")
    g.serialize(DOCS / "ontology.owl", format="xml")
    g.serialize(DOCS / "ontology.jsonld", format="json-ld")
    g.serialize(DOCS / "ontology.nt", format="nt")
    shutil.copyfile(ROOT / "ontology" / "alignment.ttl", DOCS / "alignment.ttl")
    shutil.copyfile(ROOT / "shapes" / "daimo-shapes.ttl", DOCS / "daimo-shapes.ttl")
    print(f"exported {len(g)} core triples -> {DOCS}/ontology.{{ttl,owl,jsonld,nt}}")
    print("copied alignment.ttl and daimo-shapes.ttl into docs/")


if __name__ == "__main__":
    main()
