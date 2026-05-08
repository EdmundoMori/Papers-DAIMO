#!/usr/bin/env python3
"""
DAIMO reasoner consistency check.

Runs two reasoners against DAIMO v0.1.x:

1. HermiT (via owlready2) over the merged (ontology + alignment + example KG)
   graph. Reports: consistency, unsatisfiable classes, reasoning time.

2. OWL-RL (pure Python) rule-based inference on the same merged graph as a
   cross-check. Reports: materialised-triple count and any OWL-RL consistency
   flags (e.g., disjoint-class violations).

Exit code 0 iff both reasoners find the ontology consistent.
"""
from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS
from rdflib.term import URIRef

DAIMO_NS = "https://w3id.org/pionera/daimo#"

# Superclasses whose entailment on a DAIMO class would indicate a bug.
# Keyed by IRI string; value is a human-readable reason.
FORBIDDEN_SUPERS = {
    "http://www.w3.org/ns/prov#Activity":
        "DAIMO classes are artefacts/entities/roles, not activities; "
        "inference into prov:Activity indicates a wrong subproperty "
        "alignment (historical bug: authorizesRun ⊑ prov:used).",
    "http://www.w3.org/ns/prov#Association":
        "prov:Association is the reified association OBJECT, not an agent; "
        "inference into it indicates a wrong alignment (historical bug: "
        "grantedTo ⊑ prov:qualifiedAssociation).",
    "http://www.w3.org/2002/07/owl#Nothing":
        "unsatisfiable — something is logically contradictory.",
    "http://data.europa.eu/it6/MachineLearningModel":
        "only it6:MachineLearningModel itself should be inferred as this "
        "class (historical bug: contextDataset ⊑ it6:trainedOn).",
    "http://data.europa.eu/it6/Run":
        "only it6:Run itself should be inferred as this class "
        "(historical bug: contextFlow ⊑ it6:hasFlow).",
}

import owlrl

ROOT = Path(__file__).resolve().parent
ONT_DIR = ROOT / "ontology"
EX_DIR = ROOT / "examples"


def load_merged() -> Graph:
    g = Graph()
    for f in sorted(ONT_DIR.glob("*.ttl")):
        g.parse(f, format="turtle")
    for f in sorted(EX_DIR.glob("*.ttl")):
        g.parse(f, format="turtle")
    return g


def hermit_check(merged: Graph) -> dict:
    """Run HermiT via owlready2 against the merged graph."""
    import owlready2

    result: dict = {"reasoner": "HermiT (owlready2)"}
    with tempfile.NamedTemporaryFile(
        suffix=".rdf", mode="wb", delete=False
    ) as tmp:
        merged.serialize(destination=tmp.name, format="xml")
        tmp_path = tmp.name

    try:
        onto = owlready2.get_ontology("file://" + tmp_path).load()
        t0 = time.time()
        with onto:
            try:
                owlready2.sync_reasoner(infer_property_values=True)
                result["consistent"] = True
            except owlready2.OwlReadyInconsistentOntologyError as e:
                result["consistent"] = False
                result["error"] = str(e)
        result["reasoning_time_s"] = round(time.time() - t0, 2)

        unsat = []
        try:
            for cls in list(onto.classes()):
                if cls == owlready2.Nothing:
                    continue
                if owlready2.Nothing in cls.is_a:
                    unsat.append(str(cls))
        except Exception:
            pass
        result["unsatisfiable_classes"] = unsat
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    return result


def owlrl_check(merged: Graph) -> dict:
    g = Graph()
    for t in merged:
        g.add(t)
    pre = len(g)
    t0 = time.time()
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    dt = round(time.time() - t0, 2)
    post = len(g)

    # Disjoint-class violations manifest as individuals typed as owl:Nothing.
    nothing_individuals = list(
        g.subjects(predicate=RDF.type, object=OWL.Nothing)
    )
    unsat_classes = [
        c for c in g.subjects(predicate=RDFS.subClassOf, object=OWL.Nothing)
        if c != OWL.Nothing  # exclude trivial reflexive owl:Nothing ⊑ owl:Nothing
    ]

    return {
        "reasoner": "OWL-RL (owlrl)",
        "pre_triples": pre,
        "post_triples": post,
        "materialised": post - pre,
        "reasoning_time_s": dt,
        "nothing_individuals": [str(x) for x in nothing_individuals],
        "unsat_subclasses": [str(x) for x in unsat_classes],
        "closure_graph": g,
    }


def entailment_check(closure: Graph) -> dict:
    """
    For every DAIMO-native class, enumerate its inferred superclass set and
    flag any entailment into a FORBIDDEN_SUPERS target. This catches
    silent inference bugs that neither HermiT consistency nor SHACL will
    surface, because the problematic axiom doesn't produce a contradiction
    unless the ontology also asserts disjointness with the wrong class.
    """
    daimo_classes = sorted(
        {
            s for s in closure.subjects(RDF.type, OWL.Class)
            if isinstance(s, URIRef) and str(s).startswith(DAIMO_NS)
        },
        key=str,
    )

    per_class: dict[str, list[str]] = {}
    warnings: list[str] = []
    for c in daimo_classes:
        supers = sorted(
            {
                str(s) for s in closure.objects(c, RDFS.subClassOf)
                if isinstance(s, URIRef) and str(s) != str(c)  # exclude reflexive
            }
        )
        per_class[str(c)] = supers
        for sup in supers:
            if sup in FORBIDDEN_SUPERS:
                warnings.append(
                    f"{c.split('#')[-1]} ⊑ {sup.rsplit('/', 1)[-1].split('#')[-1]} "
                    f"— {FORBIDDEN_SUPERS[sup]}"
                )

    return {"per_class": per_class, "warnings": warnings}


def main() -> int:
    merged = load_merged()
    print("=" * 72)
    print("DAIMO reasoner consistency check")
    print("=" * 72)
    print(f"Merged graph: {len(merged)} triples")

    exit_code = 0
    lines: list[str] = ["# DAIMO Reasoner Report", ""]

    try:
        print("\n[1/2] HermiT via owlready2 ...")
        h = hermit_check(merged)
        print(f"  consistent           : {h.get('consistent')}")
        print(f"  reasoning time (s)   : {h.get('reasoning_time_s')}")
        print(f"  unsatisfiable classes: {len(h.get('unsatisfiable_classes', []))}")
        for c in h.get("unsatisfiable_classes", []):
            print(f"    - {c}")
        if h.get("consistent") is False:
            exit_code = 1
            print(f"  error                : {h.get('error')}")
        lines.append("## HermiT (owlready2)")
        lines.append("")
        lines.append(f"- consistent: **{h.get('consistent')}**")
        lines.append(f"- reasoning time: {h.get('reasoning_time_s')} s")
        lines.append(f"- unsatisfiable classes: {len(h.get('unsatisfiable_classes', []))}")
        if h.get("error"):
            lines.append(f"- error: `{h['error']}`")
        lines.append("")
    except Exception as e:
        print(f"  HermiT check failed: {e}")
        lines.append(f"## HermiT — FAILED: `{e}`\n")
        exit_code = 2

    print("\n[2/3] OWL-RL (pure Python) ...")
    o = owlrl_check(merged)
    print(f"  pre triples          : {o['pre_triples']}")
    print(f"  post triples         : {o['post_triples']}")
    print(f"  materialised         : {o['materialised']}")
    print(f"  reasoning time (s)   : {o['reasoning_time_s']}")
    print(f"  owl:Nothing individuals: {len(o['nothing_individuals'])}")
    print(f"  unsat subclasses       : {len(o['unsat_subclasses'])}")
    for x in o["nothing_individuals"]:
        print(f"    ! {x}")
    if o["nothing_individuals"] or o["unsat_subclasses"]:
        exit_code = 1
    lines.append("## OWL-RL (pure Python)")
    lines.append("")
    lines.append(f"- pre triples: {o['pre_triples']}")
    lines.append(f"- post triples: {o['post_triples']}")
    lines.append(f"- materialised: {o['materialised']}")
    lines.append(f"- reasoning time: {o['reasoning_time_s']} s")
    lines.append(f"- owl:Nothing individuals (disjoint-class violations): {len(o['nothing_individuals'])}")
    lines.append(f"- unsatisfiable subclasses: {len(o['unsat_subclasses'])}")
    lines.append("")

    print("\n[3/3] Entailment-verification check ...")
    e = entailment_check(o["closure_graph"])
    print(f"  DAIMO classes inspected: {len(e['per_class'])}")
    print(f"  forbidden-entailment warnings: {len(e['warnings'])}")
    if e["warnings"]:
        exit_code = 1
        for w in e["warnings"]:
            print(f"    ! {w}")
    lines.append("## Entailment-verification check")
    lines.append("")
    lines.append(
        "For each DAIMO-native class, lists every superclass entailed after "
        "OWL-RL materialisation. Catches silent inference bugs that HermiT "
        "and SHACL both miss (they would only surface if the ontology also "
        "asserted disjointness with the wrong class)."
    )
    lines.append("")
    lines.append(f"- DAIMO classes inspected: {len(e['per_class'])}")
    lines.append(f"- forbidden-entailment warnings: **{len(e['warnings'])}**")
    if e["warnings"]:
        lines.append("")
        lines.append("### Warnings")
        for w in e["warnings"]:
            lines.append(f"- {w}")
    lines.append("")
    lines.append("### Inferred superclasses per DAIMO class")
    lines.append("")
    for cls, supers in e["per_class"].items():
        short = cls.rsplit("#", 1)[-1]
        if not supers:
            lines.append(f"- `daimo:{short}` — no external superclasses (stand-alone)")
        else:
            supers_short = [s.rsplit("#", 1)[-1].rsplit("/", 1)[-1] for s in supers]
            lines.append(f"- `daimo:{short}` ⊑ {', '.join(supers_short)}")
    lines.append("")

    lines.append("## Verdict")
    lines.append("")
    lines.append(
        "**CONSISTENT**" if exit_code == 0 else "**INCONSISTENT — see details above**"
    )
    (ROOT / "reports" / "reasoner-report.md").write_text("\n".join(lines))

    print("\n" + "=" * 72)
    print("Report saved to reports/reasoner-report.md")
    print("Exit code:", exit_code)
    print("=" * 72)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
