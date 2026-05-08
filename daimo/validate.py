#!/usr/bin/env python3
"""
DAIMO validation runner.

Loads the ontology + alignment + SHACL shapes + example KG, then:
1. Parses all Turtle files and reports syntax errors.
2. Runs SHACL validation and reports conformance.
3. Extracts every fenced SPARQL block from queries/queries.md and runs it
   against the example KG.
4. Prints a per-CQ pass/fail report (pass = query returned >=1 row).

Run:
    pip install rdflib pyshacl
    python validate.py

Exit code 0 iff all shapes conform and all CQs return at least one row.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from rdflib import Graph
    from pyshacl import validate as shacl_validate
except ImportError as e:
    print(f"Missing dependency: {e}. Run: pip install rdflib pyshacl", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parent
ONT_DIR = ROOT / "ontology"
SHAPES_DIR = ROOT / "shapes"
EX_DIR = ROOT / "examples"
QUERIES_MD = ROOT / "queries" / "queries.md"


def load_graph(files: list[Path]) -> Graph:
    g = Graph()
    for f in files:
        g.parse(f, format="turtle")
    return g


def extract_cqs(md_path: Path) -> list[tuple[str, str]]:
    """Extract (CQ_code, sparql) pairs from the markdown file."""
    text = md_path.read_text(encoding="utf-8")
    prefix_match = re.search(r"```sparql\s*(PREFIX[\s\S]*?)```", text)
    if not prefix_match:
        print("ERROR: could not find the PREFIX block in queries.md", file=sys.stderr)
        sys.exit(2)
    prefixes = prefix_match.group(1).strip() + "\n\n"

    cqs: list[tuple[str, str]] = []
    # Walk through headings and pick each subsequent sparql block.
    pattern = re.compile(
        r"###\s+(CQ-[A-Z0-9\-]+)[^\n]*\n[\s\S]*?```sparql\s*([\s\S]*?)```",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        code = m.group(1).strip()
        body = m.group(2).strip()
        if body.startswith("PREFIX"):
            query = body
        else:
            query = prefixes + body
        cqs.append((code, query))
    return cqs


def main() -> int:
    print("=" * 70)
    print("DAIMO validation runner")
    print("=" * 70)

    ontology_files = sorted(ONT_DIR.glob("*.ttl"))
    shapes_files = sorted(SHAPES_DIR.glob("*.ttl"))
    example_files = sorted(EX_DIR.glob("*.ttl"))

    print(f"\nOntology files : {[f.name for f in ontology_files]}")
    print(f"Shape files    : {[f.name for f in shapes_files]}")
    print(f"Example files  : {[f.name for f in example_files]}")

    # 1. Parse
    print("\n[1/3] Parsing Turtle files ...")
    try:
        ont = load_graph(ontology_files)
        shapes = load_graph(shapes_files)
        data = load_graph(example_files)
    except Exception as e:
        print(f"  FAIL: {e}")
        return 1
    print(f"  ontology triples : {len(ont)}")
    print(f"  shape triples    : {len(shapes)}")
    print(f"  data triples     : {len(data)}")

    # 2. SHACL
    print("\n[2/3] Running SHACL validation ...")
    data_combined = Graph()
    for g in (ont, data):
        for t in g:
            data_combined.add(t)
    conforms, report_graph, report_text = shacl_validate(
        data_graph=data_combined,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
    )
    print(f"  conforms         : {conforms}")
    if not conforms:
        print("\n  --- SHACL report ---")
        print(report_text)

    # 3. CQs
    print("\n[3/3] Running CQ SPARQL queries ...")
    cqs = extract_cqs(QUERIES_MD)
    print(f"  found {len(cqs)} CQ queries in {QUERIES_MD.name}")

    # Materialise OWL-RL closure before running CQ queries so subPropertyOf
    # and subClassOf entailments are available (reasoning that a
    # reasoning-capable triplestore would perform on its own).
    query_graph = Graph()
    for g in (ont, data):
        for t in g:
            query_graph.add(t)
    try:
        import owlrl
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(query_graph)
        print(f"  materialised closure: {len(query_graph)} triples")
    except ImportError:
        print("  (owlrl not installed — CQs run without materialised entailment)")

    passes = 0
    failures: list[tuple[str, str]] = []
    for code, query in cqs:
        try:
            result = query_graph.query(query)
            rows = list(result)
            n = len(rows)
            status = "PASS" if n > 0 else "FAIL"
            if n > 0:
                passes += 1
            else:
                failures.append((code, "0 rows"))
            print(f"  {status:4s}  {code:8s}  rows={n}")
        except Exception as e:
            failures.append((code, str(e)))
            print(f"  ERR   {code:8s}  {e}")

    print()
    print("=" * 70)
    print(f"Summary: {passes}/{len(cqs)} CQ queries return >=1 row; "
          f"SHACL conforms={conforms}")
    print("=" * 70)

    if failures:
        print("\nFailures:")
        for code, reason in failures:
            print(f"  - {code}: {reason}")

    return 0 if (conforms and passes == len(cqs)) else 1


if __name__ == "__main__":
    sys.exit(main())
