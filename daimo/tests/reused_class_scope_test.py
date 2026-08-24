#!/usr/bin/env python3
"""
DAIMO-ISSUE-04 — reused-class SHACL target scope harness.

Matrix (automatic, not manual inspection):

  resource | DAIMO-linked | complete | expected
  Offer    | No           | No       | not selected (graph conforms)
  Offer    | Yes          | No       | violation, focus = in-scope offer
  Offer    | Yes          | Yes      | conforms
  Model    | No           | No       | not selected
  Model    | Yes          | No       | violation, focus = in-scope model
  Model    | Yes          | Yes      | conforms
  Run      | No           | No       | not selected
  Run      | Yes          | No       | violation, focus = in-scope run
  Run      | Yes          | Yes      | conforms

Also asserts the three conformance shapes no longer declare sh:targetClass
on odrl:Offer / it6:MachineLearningModel / it6:Run, and that they declare
the exact sh:targetObjectsOf properties.

Command: python tests/reused_class_scope_test.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from rdflib import Graph, URIRef, Namespace
from pyshacl import validate as shacl_validate

ROOT = Path(__file__).resolve().parent.parent
ONT_DIR = ROOT / "ontology"
SHAPES_DIR = ROOT / "shapes"
FIX = ROOT / "tests" / "reused-class-scope"
REPORT = ROOT / "reports" / "reused-class-scope-results.md"

SH = Namespace("http://www.w3.org/ns/shacl#")
DAIMO = Namespace("https://w3id.org/pionera/daimo#")
SC = Namespace("https://example.org/daimo-scope/")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
IT6 = Namespace("http://data.europa.eu/it6/")

OFFER_SHAPE = DAIMO.OfferInDAIMOShape
MODEL_SHAPE = DAIMO.MachineLearningModelInDAIMOShape
RUN_SHAPE = DAIMO.RunInDAIMOShape
AGREEMENT_SHAPE = DAIMO.AgreementInDAIMOShape

EXPECTED_OBJECTS = {
    OFFER_SHAPE: {DAIMO.hasOfferPolicy},
    MODEL_SHAPE: {DAIMO.offersModel, DAIMO.deploysModel},
    RUN_SHAPE: {DAIMO.authorizesRun, DAIMO.derivedFromRun},
    AGREEMENT_SHAPE: {DAIMO.derivedFromAgreement},
}
FORBIDDEN_CLASS = {
    OFFER_SHAPE: ODRL.Offer,
    MODEL_SHAPE: IT6.MachineLearningModel,
    RUN_SHAPE: IT6.Run,
    AGREEMENT_SHAPE: ODRL.Agreement,
}


def load(files) -> Graph:
    g = Graph()
    for f in files:
        g.parse(f, format="turtle")
    return g


def shacl(data: Graph, shapes: Graph):
    conforms, report_graph, report_text = shacl_validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
    )
    return conforms, report_graph, report_text


def focus_nodes(report: Graph) -> set[URIRef]:
    return {o for o in report.objects(None, SH.focusNode) if isinstance(o, URIRef)}


def merge(ontology: Graph, data: Graph) -> Graph:
    g = Graph()
    for src in (ontology, data):
        for t in src:
            g.add(t)
    return g


def main() -> int:
    buf = io.StringIO()

    def out(line: str = "") -> None:
        print(line)
        buf.write(line + "\n")

    out("=" * 72)
    out("DAIMO-ISSUE-04 reused-class SHACL target scope harness")
    out("=" * 72)
    ontology = load(sorted(ONT_DIR.glob("*.ttl")))
    shapes = load(sorted(SHAPES_DIR.glob("*.ttl")))
    failures: list[str] = []

    for shape, forbidden in FORBIDDEN_CLASS.items():
        name = str(shape).split("#")[-1]
        targets = set(shapes.objects(shape, SH.targetClass))
        objs = set(shapes.objects(shape, SH.targetObjectsOf))
        out(f"  {name} sh:targetClass = {sorted(str(t) for t in targets) or '(none)'}")
        out(f"  {name} sh:targetObjectsOf = {sorted(str(t).split('#')[-1] for t in objs)}")
        if forbidden in targets:
            failures.append(f"{shape} still has sh:targetClass {forbidden}")
        expected = EXPECTED_OBJECTS[shape]
        if objs != expected:
            failures.append(
                f"{shape} targetObjectsOf={sorted(str(x) for x in objs)} "
                f"expected={sorted(str(x) for x in expected)}"
            )

    def run_case(name: str, ttl: Path, expect_conforms: bool, must_focus=None, must_not_focus=None):
        data = load([ttl])
        conforms, report, text = shacl(merge(ontology, data), shapes)
        focus = focus_nodes(report)
        line = f"[{name}] conforms={conforms} focus={[str(f) for f in sorted(focus, key=str)]}"
        out("")
        out(line)
        if conforms != expect_conforms:
            failures.append(f"{name}: expected conforms={expect_conforms}, got {conforms}")
            if not expect_conforms:
                out(text[:800])
        if must_focus is not None:
            if must_focus not in focus:
                failures.append(f"{name}: expected focus node {must_focus}")
        if must_not_focus:
            hit = [n for n in must_not_focus if n in focus]
            if hit:
                failures.append(f"{name}: external node(s) selected as focus: {hit}")

    externals = [SC["external-offer"], SC["external-model"], SC["external-run"]]

    run_case(
        "external Offer/Model/Run incomplete",
        FIX / "external-incomplete.ttl",
        expect_conforms=True,
        must_not_focus=externals,
    )
    run_case(
        "DAIMO Offer incomplete",
        FIX / "daimo-offer-incomplete.ttl",
        expect_conforms=False,
        must_focus=SC["offer-incomplete"],
    )
    run_case(
        "DAIMO Model incomplete",
        FIX / "daimo-model-incomplete.ttl",
        expect_conforms=False,
        must_focus=SC["model-incomplete"],
    )
    run_case(
        "DAIMO Run incomplete",
        FIX / "daimo-run-incomplete.ttl",
        expect_conforms=False,
        must_focus=SC["run-incomplete"],
    )
    run_case(
        "DAIMO Offer/Model/Run complete (mixed with externals)",
        FIX / "daimo-complete.ttl",
        expect_conforms=True,
        must_not_focus=externals,
    )

    out("")
    if failures:
        out("FAIL:")
        for f in failures:
            out(f"  - {f}")
        REPORT.write_text(buf.getvalue(), encoding="utf-8", newline="\n")
        return 1
    out("PASS: 9-cell matrix — external incomplete ignored; "
        "in-scope incomplete rejected; in-scope complete conforms.")
    REPORT.write_text(buf.getvalue(), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
