# Informe de generacion WIDOCO (DAIMO 0.1.7)

**Estado:** PASS

**Commit evaluado:** `cd3c1ae0f8ad262fbbe899dd9b8b95db128becad`

Guardar este informe en un commit posterior **no cambia** el commit evaluado. La generacion se ejecuto sobre ese HEAD; este fichero es evidencia posterior, no parte del commit evaluado.

## Herramientas

- WIDOCO: 1.4.25 (JAR JDK-17)
- JAR: `/tmp/widoco-1.4.25-jar-with-dependencies_JDK-17.jar`
- SHA256 del JAR: `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`
- Java:

```
openjdk version "21.0.11" 2026-04-21
OpenJDK Runtime Environment (build 21.0.11+10-1-22.04.2-Ubuntu)
OpenJDK 64-Bit Server VM (build 21.0.11+10-1-22.04.2-Ubuntu, mixed mode, sharing)
```

- `java -jar ... --version` exit code: 0 (imprime `Version: 1.4.25`)

## Comando exacto

```
java -jar /tmp/widoco-1.4.25-jar-with-dependencies_JDK-17.jar \
  -ontFile daimo/ontology/daimo-core.ttl \
  -outFolder /tmp/daimo-widoco-017 \
  -rewriteAll \
  -webVowl \
  -getOntologyMetadata \
  -lang en \
  -uniteSections \
  -noPlaceHolderText
```

Los flags `-uniteSections` y `-noPlaceHolderText` se aceptaron. No fue necesario reintentar sin ellos.

## Fechas UTC y exit code

- Inicio (wrapper): 2026-09-06T11:55:14Z
- Fin (dateReleased en el HTML generado): 2026-09-06T11:55:22Z (Sun Sep 06 13:55:22 CEST 2026)
- Duracion aproximada del comando (incluye arranque JVM): ~9.3 s
- Exit code del proceso WIDOCO: **0** (mensaje `Documentation generated successfully`)
- Nota: el eco interno del codigo de salida se perdio al pasar por PowerShell; el codigo de salida del invocador WSL fue 0 y WIDOCO confirmo exito por stdout.

## Resultado de la generacion

- Ontologia de entrada: `daimo/ontology/daimo-core.ttl` (no modificada)
- Salida: `/tmp/daimo-widoco-017`
- HTML `index-en.html`:
  - This version / Revision: **0.1.7** (`https://w3id.org/pionera/daimo/0.1.7`)
  - Previous version: **0.1.6** (`https://w3id.org/pionera/daimo/0.1.6`)
  - Modified on: **2026-09-05**
  - Issued on: 2026-04-22
- No se edito a mano el HTML para forzar 0.1.6.
- `-uniteSections` unio las secciones en `index-en.html`. **No** se genero `sections/` ni `overview-en.html` separado.
- Conteo de object properties en el overview embebido de `index-en.html` (bloque entre "Object Properties" y "Data Properties"): **31** (`li` / `href`).
- OOPS: no se genero carpeta `OOPSevaluation/` (el enlace queda comentado en el HTML).
- Changelog automatico: **no generado**. WIDOCO intento descargar `https://w3id.org/pionera/daimo/0.1.6` y fallo con `java.io.FileNotFoundException`. La documentacion principal se genero igualmente. Esto no se trata como BLOCKED.

## Fusion en daimo/docs/

Copiados desde `/tmp/daimo-widoco-017` sobre `daimo/docs/` (sin borrar `alignment.ttl` ni `daimo-shapes.ttl`):

- `docs/index-en.html`
- `docs/provenance/provenance-en.html`
- `docs/provenance/provenance-en.ttl`
- `docs/resources/dark-mode-toggle.mjs`
- `docs/resources/dark.css`
- `docs/resources/extra.css`
- `docs/resources/jquery.js`
- `docs/resources/light.css`
- `docs/resources/marked.min.js`
- `docs/resources/moon.svg`
- `docs/resources/owl.css`
- `docs/resources/primer.css`
- `docs/resources/rdf.icon`
- `docs/resources/rec.css`
- `docs/resources/slider.css`
- `docs/resources/sun.svg`
- `docs/webvowl/css/webvowl.app.css`
- `docs/webvowl/css/webvowl.css`
- `docs/webvowl/data/foaf.json`
- `docs/webvowl/data/ontology.json`
- `docs/webvowl/data/template.json`
- `docs/webvowl/favicon.ico`
- `docs/webvowl/index.html`
- `docs/webvowl/js/d3.min.js`
- `docs/webvowl/js/webvowl.app.js`
- `docs/webvowl/js/webvowl.js`
- `docs/webvowl/license.txt`

No se copiaron las serializaciones `ontology.{ttl,owl,jsonld,nt}` ni el `readme.md` genericos de WIDOCO.

`daimo/docs/sections/` no fue emitido por WIDOCO (efecto de `-uniteSections`). Los HTML residuales previos (`crossref-en.html`, `description-en.html`, `overview-en.html`) se eliminaron despues, porque esas secciones ya estan unidas en `index-en.html`.

## Serializaciones oficiales (DEPLOYMENT.md)

```
cd daimo
.venv/bin/python scripts/export_serializations.py
cp ontology/alignment.ttl docs/alignment.ttl
cp shapes/daimo-shapes.ttl docs/daimo-shapes.ttl
.venv/bin/python tests/serialization_test.py
```

Resultado de `serialization_test.py`: **PASS** (`core triples = 393`; copias en `docs/` isomorfas a las fuentes).

Fuentes no modificadas:

- `daimo/ontology/daimo-core.ttl`
- `daimo/ontology/alignment.ttl`
- `daimo/shapes/daimo-shapes.ttl`
- `examples/`, `queries/`, `tests/` (no editados)

No se ejecuto commit ni push. No se toco `paper/`.
