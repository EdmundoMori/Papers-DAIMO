#!/usr/bin/env python3
"""
Submit DAIMO (core + alignment) to the OOPS! pitfall-scanner REST API.

OOPS! API: https://oops.linkeddata.es/rest
Docs     : https://oops.linkeddata.es/

Saves:
  reports/oops-report.xml   - raw OOPS! RDF/XML response
  reports/oops-report.md    - human-readable pitfall summary

Exit code 0 iff no Critical (Important) pitfalls are reported.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

from rdflib import Graph

ROOT = Path(__file__).resolve().parent
ONT_DIR = ROOT / "ontology"
REPORTS = ROOT / "reports"
OOPS_URL = "https://oops.linkeddata.es/rest"


def build_rdfxml() -> str:
    g = Graph()
    for f in sorted(ONT_DIR.glob("*.ttl")):
        g.parse(f, format="turtle")
    return g.serialize(format="xml")


def submit(rdfxml: str) -> str:
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<OOPSRequest>"
        "<OntologyURI></OntologyURI>"
        f"<OntologyContent><![CDATA[{rdfxml}]]></OntologyContent>"
        "<Pitfalls></Pitfalls>"
        "<OutputFormat>RDF/XML</OutputFormat>"
        "</OOPSRequest>"
    )
    req = urllib.request.Request(
        OOPS_URL,
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def parse_pitfalls(raw_xml: str) -> list[dict]:
    """Extract pitfall records from OOPS!' RDF/XML response."""
    ns = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "oops": "http://oops.linkeddata.es/def#",
    }
    root = ET.fromstring(raw_xml)
    pitfalls = []
    for desc in root.findall(".//rdf:Description", ns):
        name_el = desc.find("oops:hasName", ns)
        desc_el = desc.find("oops:hasDescription", ns)
        imp_el = desc.find("oops:hasImportanceLevel", ns)
        code_el = desc.find("oops:hasCode", ns)
        affected = [
            e.text for e in desc.findall("oops:hasAffectedElement", ns) if e.text
        ]
        naffected_el = desc.find("oops:hasNumberAffectedElements", ns)
        if name_el is None or imp_el is None:
            continue
        pitfalls.append(
            {
                "code": code_el.text if code_el is not None else "",
                "name": name_el.text,
                "importance": imp_el.text,
                "description": desc_el.text if desc_el is not None else "",
                "n_affected": naffected_el.text if naffected_el is not None else "",
                "affected": affected,
            }
        )
    return pitfalls


def write_markdown(pitfalls: list[dict]) -> None:
    by_imp = {"Critical": [], "Important": [], "Minor": []}
    for p in pitfalls:
        by_imp.setdefault(p["importance"], []).append(p)

    lines = ["# DAIMO OOPS! Pitfall Report", ""]
    lines.append(f"- Total pitfalls flagged: **{len(pitfalls)}**")
    for level in ("Critical", "Important", "Minor"):
        lines.append(f"- {level}: **{len(by_imp.get(level, []))}**")
    lines.append("")
    for level in ("Critical", "Important", "Minor"):
        items = by_imp.get(level, [])
        if not items:
            continue
        lines.append(f"## {level} pitfalls ({len(items)})")
        lines.append("")
        for p in items:
            lines.append(f"### {p['code']} — {p['name']}")
            if p.get("n_affected"):
                lines.append(f"- affected elements: {p['n_affected']}")
            if p.get("description"):
                lines.append(f"- description: {p['description'].strip()[:400]}")
            if p.get("affected"):
                lines.append("- affected:")
                for a in p["affected"][:20]:
                    lines.append(f"  - `{a}`")
                if len(p["affected"]) > 20:
                    lines.append(f"  - ... and {len(p['affected']) - 20} more")
            lines.append("")
    (REPORTS / "oops-report.md").write_text("\n".join(lines))


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    print("Building RDF/XML from ontology/*.ttl ...")
    rdfxml = build_rdfxml()
    print(f"  {len(rdfxml)} chars")
    print(f"Submitting to {OOPS_URL} ...")
    raw = submit(rdfxml)
    (REPORTS / "oops-report.xml").write_text(raw)
    print(f"  raw response: {len(raw)} chars -> reports/oops-report.xml")

    pitfalls = parse_pitfalls(raw)
    write_markdown(pitfalls)
    print(f"  {len(pitfalls)} pitfalls parsed -> reports/oops-report.md")

    critical = [p for p in pitfalls if p["importance"] == "Critical"]
    important = [p for p in pitfalls if p["importance"] == "Important"]
    minor = [p for p in pitfalls if p["importance"] == "Minor"]
    print()
    print(f"Critical:  {len(critical)}")
    print(f"Important: {len(important)}")
    print(f"Minor:     {len(minor)}")

    if critical:
        print("\nCritical pitfalls:")
        for p in critical:
            print(f"  - {p['code']} {p['name']}  ({p.get('n_affected', '?')} elements)")
    if important:
        print("\nImportant pitfalls:")
        for p in important:
            print(f"  - {p['code']} {p['name']}  ({p.get('n_affected', '?')} elements)")
    if minor:
        print("\nMinor pitfalls:")
        for p in minor:
            print(f"  - {p['code']} {p['name']}  ({p.get('n_affected', '?')} elements)")

    return 0 if not critical else 1


if __name__ == "__main__":
    sys.exit(main())
