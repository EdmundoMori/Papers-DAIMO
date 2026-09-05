# Papers-DAIMO

Public package for **DAIMO** (*Dataspace AI Model Ontology*), an OWL 2 DL
integration profile for governed AI model assets in dataspaces.

- **Current version:** 0.1.7 (`owl:versionIRI` `https://w3id.org/pionera/daimo/0.1.7`)
- **Ontology sources (canonical):** [`daimo/ontology/`](daimo/ontology/)
- **SHACL shapes:** [`daimo/shapes/daimo-shapes.ttl`](daimo/shapes/daimo-shapes.ttl)
- **Public serialisations + WIDOCO HTML:** [`daimo/docs/`](daimo/docs/)
- **Human docs:** [`docs/`](docs/)
- **Release procedure:** [`daimo/DEPLOYMENT.md`](daimo/DEPLOYMENT.md)

```bash
cd daimo
python3 -m venv .venv && .venv/bin/pip install rdflib pyshacl owlrl owlready2
.venv/bin/python validate.py
.venv/bin/python reasoner_check.py
.venv/bin/python tests/negative_test.py
.venv/bin/python tests/random_seed_test.py
.venv/bin/python tests/reused_class_scope_test.py
.venv/bin/python tests/serialization_test.py
```

Licence: CC-BY 4.0 (ontology and docs), Apache-2.0 (validation code).
