#!/usr/bin/env python3
"""
DAIMO scalability benchmark.

Generates synthetic DAIMO-conformant exchange graphs of increasing size and
measures four operations that matter for practical consumption:

1. Turtle parse time.
2. OWL-RL materialisation time.
3. SHACL validation time.
4. SPARQL query time over the materialised graph.

The benchmark scales the number of governed exchange units. Each unit contains
one model, offering, ODRL offer, deployment, service, I/O contract, execution
authorisation, run, derived artefact, audit-evidence record, evaluation, and
cross-participant provenance record. Shared actors, participant contexts, task,
dataset, infrastructure, flow, algorithm, and evaluation context are created
once per graph.

Run:
    python scalability_benchmark.py --sizes 100 1000
    python scalability_benchmark.py --sizes 100 1000 10000

The 10k case can be expensive on small laptops because SHACL-SPARQL invariants
are evaluated over the full graph.
"""
from __future__ import annotations

import argparse
import gc
import json
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import owlrl
    from pyshacl import validate as shacl_validate
    from rdflib import Graph, Literal, Namespace, RDF, URIRef
    from rdflib.namespace import DCTERMS, RDFS, XSD
except ImportError as e:
    print(f"Missing dependency: {e}", file=sys.stderr)
    print("Run: pip install rdflib pyshacl owlrl", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parent
ONT_DIR = ROOT / "ontology"
SHAPES_DIR = ROOT / "shapes"
REPORT = ROOT / "reports" / "scalability-benchmark.md"

EX = Namespace("https://example.org/daimo-scale/")
DAIMO = Namespace("https://w3id.org/pionera/daimo#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
IT6 = Namespace("http://data.europa.eu/it6/")
MLS = Namespace("http://www.w3.org/ns/mls#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
PROV = Namespace("http://www.w3.org/ns/prov#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
EDC = Namespace("https://w3id.org/edc/v0.0.1/ns/")
SPDX = Namespace("http://spdx.org/rdf/terms#")
SPDXALG = Namespace("http://spdx.org/rdf/terms#checksumAlgorithm_")


PREFIXES = {
    "ex": EX,
    "daimo": DAIMO,
    "dcat": DCAT,
    "dct": DCTERMS,
    "it6": IT6,
    "mls": MLS,
    "odrl": ODRL,
    "prov": PROV,
    "foaf": FOAF,
    "edc": EDC,
    "spdx": SPDX,
    "spdxalg": SPDXALG,
    "rdfs": RDFS,
    "xsd": XSD,
}


SPARQL_QUERIES = [
    (
        "offerings",
        """
        SELECT (COUNT(?offering) AS ?count) WHERE {
          ?offering a daimo:AIAssetOffering .
        }
        """,
    ),
    (
        "invocation_contracts",
        """
        SELECT (COUNT(?endpoint) AS ?count) WHERE {
          ?deployment a daimo:ModelDeployment ;
                      daimo:exposedAs ?service ;
                      daimo:hasIOContract ?contract .
          ?service dcat:endpointURL ?endpoint .
          ?contract daimo:authMethod ?auth .
        }
        """,
    ),
    (
        "authorised_outputs",
        """
        SELECT (COUNT(?artifact) AS ?count) WHERE {
          ?artifact a daimo:DerivedArtifact ;
                    daimo:derivedFromRun ?run ;
                    daimo:underAuthorization ?auth .
          ?auth daimo:authorizesRun ?run .
        }
        """,
    ),
    (
        "evaluation_ranking",
        """
        SELECT ?model ?value WHERE {
          ?eval a it6:Evaluation ;
                it6:evaluates ?model ;
                daimo:usesEvaluationContext ex:eval-context ;
                it6:hasEvaluationMeasure ?measure .
          ?measure it6:hasValue ?value .
        }
        ORDER BY DESC(?value)
        LIMIT 10
        """,
    ),
]


@dataclass
class BenchmarkResult:
    units: int
    data_triples: int
    merged_triples: int
    closure_triples: int
    parse_s: float
    owlrl_s: float
    shacl_s: float
    sparql_s: float
    shacl_conforms: bool
    query_counts: dict[str, int]


def timer() -> float:
    return time.perf_counter()


def elapsed(start: float) -> float:
    return round(time.perf_counter() - start, 3)


def bind_prefixes(g: Graph) -> None:
    for prefix, ns in PREFIXES.items():
        g.bind(prefix, ns)


def load_graph(files: Iterable[Path]) -> Graph:
    g = Graph()
    bind_prefixes(g)
    for path in files:
        g.parse(path, format="turtle")
    return g


def add_common(g: Graph) -> None:
    for agent in ("provider", "consumer", "operator", "evaluator", "governance"):
        g.add((EX[agent], RDF.type, FOAF.Agent))
        g.add((EX[agent], FOAF.name, Literal(agent)))

    for ctx in ("provider-context", "consumer-context", "operator-context"):
        g.add((EX[ctx], RDF.type, EDC.ParticipantContext))
        g.add((EX[ctx], RDFS.label, Literal(ctx)))

    roles = [
        ("provider-role", DAIMO.ModelProvider, "provider", "provider-context"),
        ("consumer-role", DAIMO.ModelConsumer, "consumer", "consumer-context"),
        ("operator-role", DAIMO.PlatformOperator, "operator", "operator-context"),
        ("evaluator-role", DAIMO.Evaluator, "evaluator", "operator-context"),
        ("governance-role", DAIMO.GovernanceActor, "governance", "operator-context"),
    ]
    for role_id, role_class, agent, ctx in roles:
        role = EX[role_id]
        g.add((role, RDF.type, role_class))
        g.add((role, DAIMO.inParticipantContext, EX[ctx]))
        g.add((EX[agent], DAIMO.hasRole, role))

    g.add((EX.catalog, RDF.type, DCAT.Catalog))
    g.add((EX.catalog, DCTERMS.title, Literal("Synthetic DAIMO benchmark catalog")))
    g.add((EX.catalog, DCTERMS.publisher, EX.provider))

    g.add((EX.task, RDF.type, IT6.Task))
    g.add((EX.task, DCTERMS.title, Literal("Synthetic risk prediction task")))

    g.add((EX.dataset, RDF.type, DCAT.Dataset))
    g.add((EX.dataset, DCTERMS.title, Literal("Synthetic benchmark dataset")))
    g.add((EX.dataset, DCTERMS.hasVersion, Literal("2026.1")))

    g.add((EX.infrastructure, RDF.type, IT6.ComputerInfrastructure))
    g.add((EX.infrastructure, RDFS.label, Literal("Synthetic GPU cluster")))

    g.add((EX.flow, RDF.type, IT6.Flow))
    g.add((EX.flow, RDFS.label, Literal("Synthetic inference flow")))

    g.add((EX.algorithm, RDF.type, MLS.Algorithm))
    g.add((EX.algorithm, RDFS.label, Literal("Synthetic model algorithm")))

    g.add((EX["eval-context"], RDF.type, DAIMO.SharedEvaluationContext))
    g.add((EX["eval-context"], RDFS.label, Literal("Shared benchmark context")))
    g.add((EX["eval-context"], DAIMO.contextTask, EX.task))
    g.add((EX["eval-context"], DAIMO.contextDataset, EX.dataset))
    g.add((EX["eval-context"], DAIMO.datasetVersion, Literal("2026.1")))
    g.add((EX["eval-context"], DAIMO.protocol, Literal("holdout")))
    g.add((EX["eval-context"], DAIMO.randomSeed, Literal(42, datatype=XSD.integer)))
    g.add((EX["eval-context"], DAIMO.contextFlow, EX.flow))


def checksum_value(i: int) -> str:
    # 64 hex characters, deterministic and SHACL-compliant.
    return f"{i:064x}"[-64:]


def add_unit(g: Graph, i: int) -> None:
    model = EX[f"model-{i}"]
    policy = EX[f"policy-{i}"]
    offering = EX[f"offering-{i}"]
    deployment = EX[f"deployment-{i}"]
    service = EX[f"service-{i}"]
    contract = EX[f"io-contract-{i}"]
    auth = EX[f"authorization-{i}"]
    run = EX[f"run-{i}"]
    artifact = EX[f"artifact-{i}"]
    evidence = EX[f"audit-evidence-{i}"]
    checksum = EX[f"checksum-{i}"]
    evaluation = EX[f"evaluation-{i}"]
    measure = EX[f"measure-{i}"]
    bundle = EX[f"provenance-bundle-{i}"]

    g.add((model, RDF.type, IT6.MachineLearningModel))
    g.add((model, DCTERMS.title, Literal(f"Synthetic model {i}")))
    g.add((model, DCTERMS.identifier, Literal(f"synthetic-model-{i}")))
    g.add((model, DCTERMS.creator, EX.provider))
    g.add((model, IT6.trainedOn, EX.dataset))
    g.add((model, IT6.hasTask, EX.task))
    g.add((model, ODRL.hasPolicy, policy))

    g.add((policy, RDF.type, ODRL.Offer))
    g.add((policy, ODRL.target, model))
    g.add((policy, ODRL.assigner, EX.provider))
    g.add((policy, ODRL.permission, EX[f"offer-permission-{i}"]))
    g.add((EX[f"offer-permission-{i}"], RDF.type, ODRL.Permission))
    g.add((EX[f"offer-permission-{i}"], ODRL.action, ODRL.use))
    g.add((policy, DCTERMS.title, Literal(f"Synthetic offer policy {i}")))

    g.add((offering, RDF.type, DAIMO.AIAssetOffering))
    g.add((offering, DCTERMS.title, Literal(f"Synthetic offering {i}")))
    g.add((offering, DCTERMS.issued, Literal("2026-07-06", datatype=XSD.date)))
    g.add((offering, DAIMO.offersModel, model))
    g.add((offering, DAIMO.offeredBy, EX.provider))
    g.add((offering, DAIMO.hasOfferPolicy, policy))
    g.add((EX.catalog, DCAT.record, offering))

    g.add((deployment, RDF.type, DAIMO.ModelDeployment))
    g.add((deployment, RDFS.label, Literal(f"Synthetic deployment {i}")))
    g.add((deployment, DAIMO.deploysModel, model))
    g.add((deployment, DAIMO.exposedAs, service))
    g.add((deployment, DAIMO.hasIOContract, contract))
    g.add((deployment, DAIMO.onInfrastructure, EX.infrastructure))
    g.add((deployment, PROV.wasAttributedTo, EX.operator))

    g.add((service, RDF.type, DCAT.DataService))
    g.add((service, DCTERMS.title, Literal(f"Synthetic service {i}")))
    g.add((service, DCAT.endpointURL, URIRef(f"https://api.example.org/daimo-scale/{i}")))
    g.add((service, IT6.servesModel, model))

    g.add((contract, RDF.type, DAIMO.IOContract))
    g.add((contract, DAIMO.inputFormat, Literal("application/json")))
    g.add((contract, DAIMO.outputFormat, Literal("application/json")))
    g.add((contract, DAIMO.authMethod, Literal("oauth2-bearer")))

    g.add((run, RDF.type, IT6.Run))
    g.add((run, RDF.type, PROV.Activity))
    g.add((run, RDFS.label, Literal(f"Synthetic run {i}")))
    g.add((run, MLS.realizes, EX.algorithm))
    g.add((run, IT6.hasFlow, EX.flow))
    g.add((run, IT6.runnedOn, EX.infrastructure))
    g.add((run, PROV.wasAssociatedWith, EX.consumer))
    g.add((run, PROV.startedAtTime, Literal("2026-07-06T10:00:00Z", datatype=XSD.dateTime)))
    g.add((run, PROV.endedAtTime, Literal("2026-07-06T10:01:00Z", datatype=XSD.dateTime)))

    g.add((auth, RDF.type, DAIMO.ExecutionAuthorization))
    g.add((auth, RDFS.label, Literal(f"Synthetic execution authorization {i}")))
    g.add((auth, DAIMO.grantedTo, EX.consumer))
    g.add((auth, DAIMO.authorizesRun, run))
    g.add((auth, DAIMO.expiresAt, Literal("2027-07-06T00:00:00Z", datatype=XSD.dateTime)))
    g.add((auth, ODRL.permission, EX[f"auth-permission-{i}"]))
    g.add((EX[f"auth-permission-{i}"], RDF.type, ODRL.Permission))
    g.add((EX[f"auth-permission-{i}"], ODRL.target, model))
    g.add((EX[f"auth-permission-{i}"], ODRL.assigner, EX.provider))
    g.add((EX[f"auth-permission-{i}"], ODRL.assignee, EX.consumer))
    g.add((EX[f"auth-permission-{i}"], ODRL.action, ODRL.use))

    g.add((artifact, RDF.type, DAIMO.DerivedArtifact))
    g.add((artifact, DCTERMS.title, Literal(f"Synthetic derived artifact {i}")))
    g.add((artifact, DAIMO.derivedFromRun, run))
    g.add((artifact, DAIMO.underAuthorization, auth))

    g.add((evidence, RDF.type, DAIMO.AuditEvidence))
    g.add((evidence, DAIMO.evidenceOf, run))
    g.add((evidence, DAIMO.integrityHash, checksum))
    g.add((evidence, DAIMO.signedBy, EX.operator))
    g.add((evidence, DAIMO.recordedAt, Literal("2026-07-06T10:02:00Z", datatype=XSD.dateTime)))
    g.add((checksum, RDF.type, SPDX.Checksum))
    g.add((checksum, SPDX.algorithm, SPDXALG.checksumAlgorithm_sha256))
    g.add((checksum, SPDX.checksumValue, Literal(checksum_value(i))))

    g.add((evaluation, RDF.type, IT6.Evaluation))
    g.add((evaluation, IT6.evaluates, model))
    g.add((evaluation, DAIMO.usesEvaluationContext, EX["eval-context"]))
    g.add((evaluation, IT6.hasEvaluationMeasure, measure))
    g.add((measure, RDF.type, IT6.EvaluationMeasure))
    g.add((measure, IT6.hasValue, Literal(f"0.{800000 + (i % 100000):06d}", datatype=XSD.decimal)))

    g.add((bundle, RDF.type, DAIMO.CrossParticipantProvenanceRecord))
    g.add((bundle, RDFS.label, Literal(f"Synthetic provenance bundle {i}")))
    g.add((bundle, DAIMO.spansParticipantContext, EX["provider-context"]))
    g.add((bundle, DAIMO.spansParticipantContext, EX["consumer-context"]))
    g.add((bundle, DAIMO.spansParticipantContext, EX["operator-context"]))
    g.add((bundle, DAIMO.records, run))


def generate_data(units: int) -> Graph:
    g = Graph()
    bind_prefixes(g)
    add_common(g)
    for i in range(1, units + 1):
        add_unit(g, i)
    return g


def merge_graphs(*graphs: Graph) -> Graph:
    merged = Graph()
    bind_prefixes(merged)
    for graph in graphs:
        for triple in graph:
            merged.add(triple)
    return merged


def run_sparql_suite(graph: Graph) -> tuple[float, dict[str, int]]:
    prefixes = "\n".join(f"PREFIX {p}: <{ns}>" for p, ns in PREFIXES.items()) + "\n"
    counts: dict[str, int] = {}
    t0 = timer()
    for name, body in SPARQL_QUERIES:
        rows = list(graph.query(prefixes + body))
        if name == "evaluation_ranking":
            counts[name] = len(rows)
        else:
            counts[name] = int(rows[0][0])
    return elapsed(t0), counts


def benchmark_size(units: int, ontology: Graph, shapes: Graph) -> BenchmarkResult:
    generated = generate_data(units)
    data_triples = len(generated)

    with tempfile.NamedTemporaryFile(suffix=".ttl", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        generated.serialize(destination=tmp_path, format="turtle")
        del generated
        gc.collect()

        parsed = Graph()
        bind_prefixes(parsed)
        t0 = timer()
        parsed.parse(tmp_path, format="turtle")
        parse_s = elapsed(t0)

        merged = merge_graphs(ontology, parsed)
        merged_triples = len(merged)

        closure = Graph()
        bind_prefixes(closure)
        for triple in merged:
            closure.add(triple)
        t0 = timer()
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(closure)
        owlrl_s = elapsed(t0)
        closure_triples = len(closure)

        t0 = timer()
        conforms, _, _ = shacl_validate(
            data_graph=merged,
            shacl_graph=shapes,
            inference="rdfs",
            abort_on_first=False,
            meta_shacl=False,
            advanced=True,
        )
        shacl_s = elapsed(t0)

        sparql_s, query_counts = run_sparql_suite(closure)

        return BenchmarkResult(
            units=units,
            data_triples=data_triples,
            merged_triples=merged_triples,
            closure_triples=closure_triples,
            parse_s=parse_s,
            owlrl_s=owlrl_s,
            shacl_s=shacl_s,
            sparql_s=sparql_s,
            shacl_conforms=bool(conforms),
            query_counts=query_counts,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def results_to_markdown(results: list[BenchmarkResult], sizes: list[int]) -> str:
    payload = {
        "sizes": sizes,
        "results": [r.__dict__ for r in results],
    }

    lines = [
        "# DAIMO Scalability Benchmark",
        "",
        "This report is generated by `scalability_benchmark.py`. It measures",
        "synthetic DAIMO-conformant governed exchange graphs where each unit",
        "contains one offering, model, deployment, service, I/O contract,",
        "execution authorisation, run, derived artefact, audit-evidence record,",
        "evaluation, and cross-participant provenance record.",
        "",
        "The benchmark is not a production throughput claim. It is a reproducible",
        "sanity check for the non-functional scalability requirement: DAIMO should",
        "remain tractable as the number of exchange instances grows while the core",
        "ontology remains small.",
        "",
        "The repository report executes 100 and 1,000 exchange units. Larger",
        "runs, for example 10,000 units, are supported through `--sizes` but",
        "should not be cited unless executed on the target machine.",
        "",
        "| Units | Data triples | Merged triples | OWL-RL closure triples | Parse (s) | OWL-RL (s) | SHACL (s) | SPARQL suite (s) | SHACL conforms |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|:---:|",
    ]
    for r in results:
        lines.append(
            f"| {r.units} | {r.data_triples} | {r.merged_triples} | "
            f"{r.closure_triples} | {r.parse_s:.3f} | {r.owlrl_s:.3f} | "
            f"{r.shacl_s:.3f} | {r.sparql_s:.3f} | {r.shacl_conforms} |"
        )
    lines += [
        "",
        "## Query Counts",
        "",
        "| Units | Offerings | Invocation contracts | Authorised outputs | Ranking rows |",
        "|---:|---:|---:|---:|---:|",
    ]
    for r in results:
        qc = r.query_counts
        lines.append(
            f"| {r.units} | {qc['offerings']} | {qc['invocation_contracts']} | "
            f"{qc['authorised_outputs']} | {qc['evaluation_ranking']} |"
        )
    lines += [
        "",
        "## Machine-Readable Result",
        "",
        "```json",
        json.dumps(payload, indent=2),
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=[100, 1000],
        help="Number of governed exchange units to generate for each run.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=REPORT,
        help="Markdown report path.",
    )
    args = parser.parse_args()

    ontology_files = sorted(ONT_DIR.glob("*.ttl"))
    shapes_files = sorted(SHAPES_DIR.glob("*.ttl"))
    ontology = load_graph(ontology_files)
    shapes = load_graph(shapes_files)

    print("=" * 72)
    print("DAIMO scalability benchmark")
    print("=" * 72)
    print(f"Ontology triples: {len(ontology)}")
    print(f"Shape triples   : {len(shapes)}")
    print(f"Sizes           : {args.sizes}")
    print()

    results: list[BenchmarkResult] = []
    exit_code = 0
    for units in args.sizes:
        print(f"[units={units}] running ...", flush=True)
        try:
            result = benchmark_size(units, ontology, shapes)
            results.append(result)
            status = "conforms" if result.shacl_conforms else "does NOT conform"
            print(
                f"  triples={result.data_triples}, parse={result.parse_s:.3f}s, "
                f"owlrl={result.owlrl_s:.3f}s, shacl={result.shacl_s:.3f}s, "
                f"sparql={result.sparql_s:.3f}s, {status}"
            )
            if not result.shacl_conforms:
                exit_code = 1
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            exit_code = 1
            break
        finally:
            gc.collect()

    if results:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(results_to_markdown(results, args.sizes), encoding="utf-8")
        print()
        print(f"Report saved to {args.report.relative_to(ROOT)}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
