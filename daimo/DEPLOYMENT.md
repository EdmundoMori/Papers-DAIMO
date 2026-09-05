# DAIMO publication procedure

This file is the procedure referenced by `w3id-redirect/.htaccess`.

## Canonical sources

1. **Core ontology:** `ontology/daimo-core.ttl`
2. **Alignment:** `ontology/alignment.ttl`
3. **SHACL:** `shapes/daimo-shapes.ttl`

Public RDF serialisations under `docs/ontology.{ttl,owl,jsonld,nt}` are
**generated from the core module**. Do not edit those files by hand.

```bash
cd daimo
.venv/bin/python scripts/export_serializations.py
.venv/bin/python tests/serialization_test.py
```

The HTML site under `docs/` (WIDOCO) is published by
`.github/workflows/daimo-pages.yml` (`workflow_dispatch`). After a TBox
change, regenerate WIDOCO when possible; at minimum re-run the export
script and copy the current `alignment.ttl` / `daimo-shapes.ttl` into
`docs/`.

## w3id.org

1. Copy `w3id-redirect/.htaccess` to
   `https://github.com/perma-id/w3id.org/pionera/.htaccess` via pull request.
2. Confirm `https://w3id.org/pionera/daimo` and
   `https://w3id.org/pionera/daimo/0.1.7` resolve.
3. Until the PR is merged, the namespace remains **pending**.

## GitHub release and Zenodo

1. Tag `v0.1.7` on the commit whose `owl:versionInfo` is `0.1.7`.
2. Create the GitHub release from that tag.
3. Upload the same tree with `daimo/.zenodo.json` to obtain the archival DOI.
4. Put the DOI into `CITATION.cff` (`identifiers: type: doi`) when issued.

The previous public freeze is `v0.1.6-swj-submission`.
