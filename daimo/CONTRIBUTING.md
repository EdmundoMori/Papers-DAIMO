# Contributing to DAIMO

DAIMO follows the [LOT methodology](https://lot.linkeddata.es/) Phase 4
(maintenance) practices. Contributions, corrections, and discussions are
welcome.

## Ways to contribute

| Channel | Use for |
|---|---|
| **GitHub Issues** | Bug reports, term-definition corrections, missing competency questions, new use-case requests, alignment suggestions |
| **Pull Requests** | Code, ontology, shape, query, and documentation changes |
| **Discussions** | Open-ended questions, design alternatives, adoption stories |

## Issue triage

Every issue is triaged into one of four labels:

- `bug` — the ontology entails something wrong, or a SHACL/SPARQL test fails
- `enhancement` — new terms, new CQs, new invariants
- `doc` — documentation-only change
- `reuse` — alignment with an external vocabulary needs revision

Maintainers assign a target version. Expect a first response within
one week.

## Pull request workflow

1. Fork the repo and create a topic branch.
2. Make changes in the appropriate files:
   - Ontology terms → `ontology/daimo-core.ttl`
   - External alignment → `ontology/alignment.ttl`
   - SHACL shapes → `shapes/daimo-shapes.ttl`
   - SPARQL CQs → `queries/queries.md` (keep NL text synchronised with
     `ORSD/daimo-cqs.md`)
   - Example data → `examples/flood-risk-scenario.ttl`
3. **Run all validators locally** before submitting:
   ```bash
   .venv/bin/python validate.py                 # SHACL + CQ SPARQL
   .venv/bin/python reasoner_check.py           # HermiT + OWL-RL + entailment check
   .venv/bin/python oops_check.py               # OOPS! pitfall scan
   .venv/bin/python tests/negative_test.py      # cross-class invariant negative tests
   ```
   All four must exit zero.
4. Add a `CHANGELOG.md` entry under `## Unreleased`.
5. Open a PR with a short description and a link to the issue being
   addressed.

## Versioning

DAIMO uses semantic versioning on `owl:versionInfo` in
[ontology/daimo-core.ttl](ontology/daimo-core.ttl):

- **PATCH** (`0.1.X`) — documentation, SHACL-shape refinement, CQ rewrites
  that preserve the set of inferred triples over any conformant KG.
- **MINOR** (`0.X.0`) — new classes, new properties, or additions that
  do not remove or change the meaning of existing terms.
- **MAJOR** (`X.0.0`) — class removal, property-range narrowing, or
  alignment-axiom changes that affect downstream reasoning.

Every release bumps `owl:versionIRI` to a resolvable
`https://w3id.org/pionera/daimo/<version>` URL and updates
`CHANGELOG.md`.

## Deprecation policy

Terms removed at a MAJOR boundary follow a two-step deprecation:

1. In the MINOR release preceding removal, mark the term with
   `owl:deprecated "true"^^xsd:boolean` and a `rdfs:comment` explaining
   the replacement.
2. In the next MAJOR release, the term is removed from `daimo-core.ttl`
   but its IRI remains listed in `CHANGELOG.md` under "Removed".

IRIs are never reused for a different concept.

## What the maintainers will not accept

- PRs that redefine a term already reused from DCAT, MLDCAT-AP,
  ODRL, PROV-O, or DSP. DAIMO's design principle is reuse-first;
  new alignment axioms are welcome, parallel redefinitions are not.
- PRs that remove a CQ without either adding an issue explaining why
  the competency has been withdrawn, or rewriting the CQ in a stronger
  form.
- PRs that add an `rdfs:subPropertyOf` or `rdfs:subClassOf` axiom
  without running `reasoner_check.py` and showing the entailment-check
  output is still clean.

## Code of conduct

Be constructive, be precise, and assume good faith. Ontology engineering
debates can be heated; the codebase is the record.
