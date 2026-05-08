# Guía para dibujar DAIMO en notación Chowlk

Documento de trabajo para la persona (autor o colaborador) que vaya a producir las tres figuras del paper DAIMO en notación Chowlk, siguiendo [https://chowlk.linkeddata.es/notation](https://chowlk.linkeddata.es/notation).

**Objetivo:** reemplazar las tres figuras TikZ actuales del paper (`daimo-paper-en-v1.tex`) por diagramas Chowlk auténticos exportados como PDF/SVG desde diagrams.net.

---

## 0. Alcance y archivos afectados

Hay que producir tres diagramas:

| Figura | Contenido | Archivo destino |
|---|---|---|
| **Fig 1** | Arquitectura modular (3 módulos DAIMO + 5 vocabularios reutilizados) | `paper/figures/fig1-architecture.pdf` |
| **Fig 2** | Vista general de las 14 clases DAIMO con sus alineamientos y propiedades | `paper/figures/fig2-classes.pdf` |
| **Fig 3** | Escenario instanciado (~20 individuos con rdf:type y property assertions) | `paper/figures/fig3-scenario.pdf` |

Una vez exportados, en el `.tex` se reemplaza cada bloque `\begin{tikzpicture}…\end{tikzpicture}` por `\includegraphics[width=\textwidth]{figures/figN-*.pdf}`.

---

## 1. Herramientas

| Herramienta | URL | Instalación |
|---|---|---|
| **diagrams.net** | <https://app.diagrams.net> (web) o [desktop app](https://github.com/jgraph/drawio-desktop/releases) | Web: sin instalación. Desktop: descargar binario. |
| **Chowlk shape library** | <https://chowlk.linkeddata.es/chowlk_library.xml> | Archivo XML a cargar en drawio. |
| **Chowlk converter** (opcional) | <https://chowlk.linkeddata.es/> | Sólo si quieres round-trip diagrama → TTL. Para las figuras del paper no hace falta. |

### Cargar la biblioteca Chowlk en drawio

En drawio: `File → Open Library from → URL` y pegar `https://chowlk.linkeddata.es/chowlk_library.xml`. El panel izquierdo mostrará los bloques Chowlk listos para arrastrar.

> ⚠️ También existe una versión "lightweight" con menos bloques. Usa la **Complete library**.

---

## 2. Notación Chowlk: chuleta rápida

Resumen operativo de las convenciones que vas a usar. Para el detalle completo consulta la [notación oficial](https://chowlk.linkeddata.es/notation).

### 2.1 Elementos básicos

| Elemento | Forma | Contenido del label | Observación |
|---|---|---|---|
| **Clase** | Rectángulo de bordes rectos, negro sobre blanco | `daimo:AIAssetOffering` | Una clase por caja. |
| **Individuo** (instancia) | Rectángulo idéntico al de clase, **texto subrayado** | `ex:upm-catalog` | El subrayado es el marcador. |
| **Datatype / data range** | Rectángulo con borde **punteado** | `xsd:string` o `xsd:dateTime` | Destino de datatype properties. |
| **Clase anónima / wrapper** | Rectángulo vacío pequeño | (sin texto) | Para envolver restricciones. |
| **Constructor (unión, intersección, complemento, equivalencia, disjuntos)** | **Elipse** con operador Unicode | `⊔`, `⊓`, `¬`, `≡`, `⊥` | Hub de clase-axioma. |
| **Hexágono** | Hexágono con etiqueta especial | `<<owl:oneOf>>`, `<<owl:AllDifferent>>`, `<<owl:AllDisjointProperties>>`, `<<owl:propertyChainAxiom>>` | Wrappers n-arios. |

### 2.2 Arrows (crítico: la diferencia entre ellas codifica la semántica)

| Semántica | Línea | Cabeza | Uso |
|---|---|---|---|
| `rdfs:subClassOf` | Sólida | Triángulo **hueco** (generalización UML) | Apunta al padre. |
| `owl:ObjectProperty` | Sólida | Triángulo **relleno** | Apunta a la clase del range. Label sobre la línea. |
| `rdf:type` (instancia → clase) | **Punteada** | Triángulo **relleno** | Label `<<rdf:type>>`. |
| Conector de axioma (equivalencia, disjoint, unión, intersección) | **Punteada** | Diamante **hueco fino** | Color label `#000099` azul oscuro. |
| `owl:imports`, axiomas de propiedad, property chain | Punteada | Flecha abierta | Labels `<<owl:imports>>`, `<<rdfs:subPropertyOf>>`, `<<owl:inverseOf>>`. |

### 2.3 Propiedades: representación

Para cada `owl:ObjectProperty` hay dos formas de dibujarla:

**(a) Modo edge:** flecha de la clase domain a la clase range, con el label en la línea:

```
[daimo:AIAssetOffering] -- offersModel --> [it6:MachineLearningModel]
```

**(b) Modo rhombus node:** la propiedad como un nodo romboidal con `<<owl:ObjectProperty>>` en el label. Úsalo cuando la propiedad participe en `owl:inverseOf`, `rdfs:subPropertyOf` o property chains — porque esos axiomas conectan dos *propiedades*, no dos clases.

```
<<owl:ObjectProperty>>
  daimo:offersModel         <<owl:inverseOf>>         <<owl:ObjectProperty>>
                      ──────────────────────────>     daimo:hasOffering
```

### 2.4 Características de propiedad (sufijos textuales en el label)

| Flag | Semántica |
|---|---|
| `(F)` | `owl:FunctionalProperty` |
| `(IF)` | `owl:InverseFunctionalProperty` |
| `(S)` | `owl:SymmetricProperty` |
| `(T)` | `owl:TransitiveProperty` |
| `(A)` | `owl:AsymmetricProperty` |
| `(R)` | `owl:ReflexiveProperty` |
| `(IR)` | `owl:IrreflexiveProperty` |

Ejemplo aplicado a DAIMO: la propiedad `daimo:offersModel` es funcional y asimétrica, por lo que su label en el edge es:

```
(F) (A) daimo:offersModel
```

### 2.5 Restricciones inline

Van en el label del edge de la propiedad, en paréntesis antes del nombre:

| Notación | Semántica OWL |
|---|---|
| `(some) prop` | `owl:someValuesFrom` |
| `(all) prop` | `owl:allValuesFrom` |
| `(value) prop` | `owl:hasValue` (target es un individuo) |
| `prop [N1..N2]` | Cardinalidad mín N1, máx N2 |
| `prop [N..N]` | `owl:cardinality N` (exacta) |
| `prop [0..N]` | Sólo max |
| `prop [N..]` | Sólo min |

Ejemplo DAIMO: `daimo:offersModel [1..1]` sobre el edge de `AIAssetOffering` significa cardinalidad exacta 1.

### 2.6 Datatype properties

Se dibujan como **atributos dentro de la caja de la clase** (no como cajas separadas). El formato dentro del rectángulo de la clase es:

```
daimo:AIAssetOffering
──────────────────────
dct:title: xsd:string
dct:issued: xsd:dateTime
```

### 2.7 Metadata block

Rectángulo amarillo (`#fff2cc` / `#d6b656`) con líneas tipo ontology header:

```
<<owl:Ontology>>  https://w3id.org/pionera/daimo
dcterms:title "Data-space AI Model Ontology"@en
dcterms:creator <https://orcid.org/…>
dcterms:license <https://creativecommons.org/licenses/by/4.0/>
owl:versionIRI <https://w3id.org/pionera/daimo/0.1.5>
vann:preferredNamespacePrefix "daimo"
```

### 2.8 Prefijos

Rectángulo separado con las declaraciones:

```
@prefix daimo: <https://w3id.org/pionera/daimo#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix it6: <http://data.europa.eu/it6/> .
...
```

### 2.9 Código de color

El color es **puramente decorativo para agrupar módulos**; Chowlk no le asigna semántica. Para DAIMO sugerimos (colores estándar de drawio):

| Módulo / vocabulario | Fill | Stroke |
|---|---|---|
| DAIMO-nativo | `#fff2cc` amarillo | `#d6b656` |
| DCAT / MLDCAT-AP | `#dae8fc` azul | `#6c8ebf` |
| ODRL | `#ffe6cc` naranja | `#d79b00` |
| PROV-O | `#d5e8d4` verde | `#82b366` |
| FOAF / DCMI | `#e1d5e7` morado | `#9673a6` |

---

## 3. Mapeo DAIMO → Chowlk (lo que tienes que dibujar)

### 3.1 Las 14 clases DAIMO-nativas

| Clase | Forma | Label dentro de la caja | Color fill |
|---|---|---|---|
| `daimo:AIAssetOffering` | Rectángulo | `daimo:AIAssetOffering` + datatype attrs: `dct:title: xsd:string`, `dct:issued: xsd:dateTime` | amarillo |
| `daimo:ExecutionAuthorization` | Rectángulo | `daimo:ExecutionAuthorization` + `daimo:expiresAt: xsd:dateTime` | amarillo |
| `daimo:ModelDeployment` | Rectángulo | `daimo:ModelDeployment` | amarillo |
| `daimo:IOContract` | Rectángulo | `daimo:IOContract` + `daimo:inputFormat: xsd:string`, `daimo:outputFormat: xsd:string`, `daimo:authMethod: xsd:string` | amarillo |
| `daimo:DerivedArtifact` | Rectángulo | `daimo:DerivedArtifact` | amarillo |
| `daimo:CrossParticipantProvenanceRecord` | Rectángulo | `daimo:CrossPart.ProvenanceRecord` (nombre abreviado por espacio) | amarillo |
| `daimo:AuditEvidence` | Rectángulo | `daimo:AuditEvidence` + `daimo:signer: xsd:string`, `daimo:timestamp: xsd:dateTime` | amarillo |
| `daimo:SharedEvaluationContext` | Rectángulo | `daimo:SharedEvaluationContext` + `daimo:protocol: xsd:string`, `daimo:randomSeed: xsd:integer` | amarillo |
| `daimo:ParticipantRole` | Rectángulo | `daimo:ParticipantRole` | amarillo |
| **Subclases de ParticipantRole (5)**: `ModelProvider`, `ModelConsumer`, `PlatformOperator`, `Evaluator`, `GovernanceActor` | Cada una un rectángulo | Su nombre `daimo:<Name>` | amarillo, más pequeñas |

### 3.2 Clases reutilizadas (padres externos) — 6 en Fig 2

| Padre externo | Label | Color fill |
|---|---|---|
| `dcat:CatalogRecord` | `dcat:CatalogRecord` | azul |
| `dcat:Resource` | `dcat:Resource` | azul |
| `odrl:Agreement` | `odrl:Agreement` | naranja |
| `prov:Role` | `prov:Role` | verde |
| `prov:Entity` | `prov:Entity` | verde |
| `prov:Bundle` | `prov:Bundle` | verde |

### 3.3 Alineamientos subClassOf (7)

Dibuja como **línea sólida + triángulo hueco** desde la clase DAIMO al padre:

```
daimo:AIAssetOffering             ▷──>  dcat:CatalogRecord
daimo:ExecutionAuthorization      ▷──>  odrl:Agreement
daimo:ModelDeployment             ▷──>  prov:Entity
daimo:DerivedArtifact             ▷──>  prov:Entity
daimo:DerivedArtifact             ▷──>  dcat:Resource       (doble parent)
daimo:CrossParticipantProvenanceRecord  ▷──>  prov:Bundle
daimo:AuditEvidence               ▷──>  prov:Entity
daimo:ParticipantRole             ▷──>  prov:Role
```

Plus las 5 subclases de ParticipantRole — cada una tiene un triángulo hueco a `daimo:ParticipantRole`.

### 3.4 Propiedades de objeto DAIMO-nativas (selección para Fig 2)

Las 8 más representativas para la figura. Para las 21 restantes basta con documentarlas en Table 3 del paper.

| Propiedad | Domain | Range | Flags | Label en el edge |
|---|---|---|---|---|
| `daimo:offersModel` | AIAssetOffering | it6:MachineLearningModel | F, A | `(F) (A) daimo:offersModel` |
| `daimo:offeredBy` | AIAssetOffering | ParticipantRole | F | `(F) daimo:offeredBy` |
| `daimo:hasOfferPolicy` | AIAssetOffering | odrl:Offer | F | `(F) daimo:hasOfferPolicy` |
| `daimo:deploysModel` | ModelDeployment | it6:MachineLearningModel | F, A | `(F) (A) daimo:deploysModel` |
| `daimo:exposedAs` | ModelDeployment | dcat:DataService | — | `daimo:exposedAs` |
| `daimo:hasIOContract` | ModelDeployment | IOContract | — | `daimo:hasIOContract` |
| `daimo:authorizesRun` | ExecutionAuthorization | it6:Run | A | `(A) daimo:authorizesRun` |
| `daimo:grantedTo` | ExecutionAuthorization | ParticipantRole | F | `(F) daimo:grantedTo` |
| `daimo:underAuthorization` | DerivedArtifact | ExecutionAuthorization | F | `(F) daimo:underAuthorization` |
| `daimo:derivedFromRun` | DerivedArtifact | it6:Run | F, A | `(F) (A) daimo:derivedFromRun` |
| `daimo:hasAuditEvidence` | DerivedArtifact | AuditEvidence | — | `daimo:hasAuditEvidence` |
| `daimo:evidenceOf` | AuditEvidence | it6:Run | F, A | `(F) (A) daimo:evidenceOf` |
| `daimo:records` | CrossParticipantProvenanceRecord | prov:Activity | — | `daimo:records` |

### 3.5 Pares inversos explícitos (5)

Cada par necesita **dos rombos `<<owl:ObjectProperty>>`** unidos por línea punteada con label `<<owl:inverseOf>>`. Para la Figura 2 podemos saltarlos (basta con mostrar una dirección); los 5 pares se documentan en el TTL.

| Par |
|---|
| `daimo:authorizesRun` ↔ `daimo:authorizedBy` |
| `daimo:deploysModel` ↔ `daimo:hasDeployment` |
| `daimo:derivedFromRun` ↔ `daimo:hasDerivedArtifact` |
| `daimo:evidenceOf` ↔ `daimo:hasAuditEvidence` |
| `daimo:offersModel` ↔ `daimo:hasOffering` |

### 3.6 Axioma de disyunción nombrado

`daimo:TopLevelKindsDisjointness` (instancia de `owl:AllDisjointClasses`) entre las 9 clases nativas de primer nivel. En Chowlk esto se dibuja como:

1. Una **elipse** con `⊥` en el centro.
2. Nueve conectores **punteados con diamante hueco** desde cada una de las 9 clases de primer nivel hasta la elipse.

Está bien no dibujarlo en la Fig 2 (sobrecargaría) pero sí mencionarlo en caption y mostrarlo en un Listado del paper.

---

## 4. Figura 1 — Arquitectura modular

**Propósito:** mostrar los tres módulos DAIMO (núcleo, alineamientos, shapes) y las cinco capas de vocabularios reutilizados, con las relaciones `owl:imports` entre ellos.

Este diagrama **no es Chowlk-TBox en sentido estricto** (no es sobre clases), pero usa convenciones Chowlk: rectángulos de módulo, flechas punteadas `<<owl:imports>>`.

### Elementos

**3 módulos DAIMO** (rectángulos amarillo):
- `daimo-core.ttl` — "DAIMO core"
- `alignment.ttl` — "Alignment module"
- `daimo-shapes.ttl` — "SHACL module"

**5 rectángulos de vocabularios reutilizados** (colores por módulo):
- `dcat:` — azul
- `it6:` (MLDCAT-AP) — azul
- `odrl:` — naranja
- `prov:` — verde
- `dspace:`, `edc:` — gris (dataspace layer)

### Relaciones

1. `core` → `alignment` con flecha punteada label `<<owl:imports>>`
2. Desde `alignment` a cada uno de los 5 vocabularios: flecha punteada con label que describa cuántos `rdfs:subClassOf`/`rdfs:subPropertyOf` hay hacia ese vocabulario (p. ej. "7 subClassOf, 6 subPropertyOf" agregado).
3. Desde `shapes` a `core`: flecha label `validates` (no es owl:imports, es referencia SHACL).

### Layout recomendado

Dos columnas verticales:

```
 [DAIMO profile]               [Reused vocabularies]
 ┌──────────────┐              ┌────────────────────┐
 │ Core         │─────imports──┤ DCAT               │
 │ Alignment ───┤ ────────────>│ MLDCAT-AP          │
 │ SHACL        │─validates    │ ODRL               │
 └──────────────┘              │ PROV-O             │
                               │ DSP / EDC          │
                               └────────────────────┘
```

Cada columna encerrada en un contenedor con título.

---

## 5. Figura 2 — Vista general de clases

**Propósito:** mostrar las 14 clases DAIMO-nativas con sus alineamientos axiomáticos y las propiedades nativas clave.

### Layout recomendado (3 filas)

```
Fila 1 (parents externos):
  dcat:CatalogRecord  odrl:Agreement  prov:Role  prov:Entity  dcat:Resource  prov:Bundle

Fila 2 (DAIMO top-level):
  AIAssetOffering  ExecutionAuthorization  ParticipantRole  ModelDeployment  DerivedArtifact  CrossPart.ProvenanceRecord

Fila 3 (DAIMO sin parent externo + AuditEvidence):
  IOContract  AuditEvidence  SharedEvaluationContext
```

Puedes usar la versión TikZ actual en `paper/daimo-paper-en-v1.tex` (líneas ~340-420) como **referencia de layout**: las coordenadas (x=0, 3.7, 7, 10.3, 13.4, 16.5) y (y=5, 2.6, 0.3) funcionan bien en A4 doble columna.

### Elementos a incluir

- **14 rectángulos** amarillos (9 top-level + 5 subclases de ParticipantRole — las subclases pueden agruparse visualmente o dibujarse como hijas pequeñas de ParticipantRole con 5 triángulos huecos).
- **6 rectángulos** azules/verdes/naranjas/morados para parents externos.
- **7 flechas sólidas + triángulo hueco** para los subClassOf (lista en §3.3).
- **5 triángulos huecos pequeños** desde las 5 subclases de rol a `daimo:ParticipantRole`.
- **Propiedades nativas principales** (§3.4): 8-10 edges sólidos con triángulo relleno entre clases DAIMO, con flags en paréntesis.

### Elementos opcionales (pueden omitirse sin perder fidelidad)

- Los 5 pares `owl:inverseOf` (como rombos separados; añaden clutter).
- La disyunción nombrada `TopLevelKindsDisjointness`.
- Datatype attributes dentro de cada caja (si incluyes, añade 2-3 por clase; aumentan altura de las cajas).

### Leyenda

Contenedor separado (Legend Container de Chowlk, que se ignora en el converter):
- Rectángulo amarillo `daimo:X` — "DAIMO-native class"
- Rectángulo azul `ext:Y` — "Reused class"
- Flecha con triángulo hueco — "rdfs:subClassOf"
- Flecha con triángulo relleno — "object property"
- Paréntesis de flags — "(F) functional, (A) asymmetric, (T) transitive, …"

---

## 6. Figura 3 — Escenario instanciado

**Propósito:** mostrar ~20 individuos del escenario de flood-risk con sus asserts de tipo y propiedades.

Este diagrama es **ABox**: la mayoría de nodos son individuos (rectángulos con texto subrayado).

### Instancias a dibujar

| Individuo (subrayado) | Tipo (`rdf:type`) | Comentario |
|---|---|---|
| `ex:upm` | `foaf:Organization` | Provider |
| `ex:leganes` | `foaf:Organization` | Consumer municipality |
| `ex:inesdata` | `foaf:Organization` | Platform |
| `ex:csic` | `foaf:Organization` | Evaluator |
| `ex:gaia-compliance` | `foaf:Organization` | Governance |
| `ex:upm-catalog` | `dcat:Catalog` | |
| `ex:offering-flood-v2` | `daimo:AIAssetOffering` | |
| `ex:offering-flood-v1` | `daimo:AIAssetOffering` | |
| `ex:offering-flood-v2-ro` | `daimo:AIAssetOffering` | |
| `ex:flood-risk-v2` | `it6:MachineLearningModel` | |
| `ex:flood-risk-v1` | `it6:MachineLearningModel` | |
| `ex:deployment-flood-v2` | `daimo:ModelDeployment` | |
| `ex:upm-gpu-cluster` | `it6:ComputerInfrastructure` | |
| `ex:rest-service` | `dcat:DataService` | |
| `ex:grpc-service` | `dcat:DataService` | |
| `ex:iocontract-rest` | `daimo:IOContract` | |
| `ex:iocontract-grpc` | `daimo:IOContract` | |
| `ex:execauth-legs` | `daimo:ExecutionAuthorization` | |
| `ex:run-2026-04-20-legs` | `it6:Run` | |
| `ex:derived-prediction` | `daimo:DerivedArtifact` | |
| `ex:audit-evidence-legs` | `daimo:AuditEvidence` | |
| `ex:audit-run-legs-checksum` | `spdx:Checksum` | |
| `ex:cross-part-bundle` | `daimo:CrossParticipantProvenanceRecord` | |
| `ex:eval-v2` | `it6:Evaluation` | accuracy 0.89 |
| `ex:eval-v1` | `it6:Evaluation` | accuracy 0.82 |
| `ex:shared-context-2026` | `daimo:SharedEvaluationContext` | ClimateBench-v1 v2026.1 |

### Relaciones principales a dibujar

Flechas sólidas con triángulo relleno (property assertions):

- `ex:offering-flood-v2 --daimo:offersModel-->  ex:flood-risk-v2`
- `ex:offering-flood-v2 --daimo:offeredBy-->  ex:upm` (provider role)
- `ex:deployment-flood-v2 --daimo:deploysModel-->  ex:flood-risk-v2`
- `ex:deployment-flood-v2 --daimo:exposedAs-->  ex:rest-service`
- `ex:deployment-flood-v2 --daimo:exposedAs-->  ex:grpc-service`
- `ex:deployment-flood-v2 --daimo:hasIOContract-->  ex:iocontract-rest`
- `ex:execauth-legs --daimo:authorizesRun-->  ex:run-2026-04-20-legs`
- `ex:execauth-legs --daimo:grantedTo-->  ex:leganes`
- `ex:run-2026-04-20-legs --prov:wasAssociatedWith-->  ex:leganes`
- `ex:derived-prediction --daimo:underAuthorization-->  ex:execauth-legs`
- `ex:derived-prediction --daimo:derivedFromRun-->  ex:run-2026-04-20-legs`
- `ex:audit-evidence-legs --daimo:evidenceOf-->  ex:run-2026-04-20-legs`
- `ex:audit-evidence-legs --daimo:integrityHash-->  ex:audit-run-legs-checksum`
- `ex:cross-part-bundle --daimo:records-->  ex:run-2026-04-20-legs`
- `ex:eval-v2 --daimo:evaluationContext-->  ex:shared-context-2026`
- `ex:eval-v1 --daimo:evaluationContext-->  ex:shared-context-2026`

### Agrupación visual

Para ~25 instancias, agrupa visualmente en 5 "carriles" (swim-lanes de Chowlk):

1. **Provider (UPM)** — catalog, 3 offerings, 2 models
2. **Platform (INESData)** — deployment, infrastructure, 2 services, 2 contracts
3. **Consumer (Leganés)** — authorization, run, derived, audit
4. **Evaluator (CSIC)** — 2 evaluations, shared context
5. **Bundle** — cross-participant bundle cruzando los carriles

### Literales

En vez de dibujar cajas para literales (`0.89`, `"ClimateBench-v1"`), lístalos como atributos internos dentro de la caja del individuo:

```
ex:eval-v2 (subrayado)
────────────────────
it6:metricValue: 0.89
it6:metricName: "accuracy"
```

---

## 7. Metadata block obligatorio

En la esquina de cada figura (o al menos en Fig 2 que es la principal), incluye el rectángulo amarillo de metadata:

```
<<owl:Ontology>>  https://w3id.org/pionera/daimo
dcterms:title "DAIMO v0.1.5: Data-space AI Model Ontology"@en
dcterms:creator <https://orcid.org/0000-0002-XXXX>
dcterms:license <https://creativecommons.org/licenses/by/4.0/>
dcterms:issued "2026-04-23"^^xsd:date
owl:versionIRI <https://w3id.org/pionera/daimo/0.1.5>
vann:preferredNamespacePrefix "daimo"
vann:preferredNamespaceUri "https://w3id.org/pionera/daimo#"
```

Y un rectángulo de prefijos:

```
@prefix daimo:  <https://w3id.org/pionera/daimo#> .
@prefix dcat:   <http://www.w3.org/ns/dcat#> .
@prefix it6:    <http://data.europa.eu/it6/> .
@prefix odrl:   <http://www.w3.org/ns/odrl/2/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/> .
@prefix spdx:   <http://spdx.org/rdf/terms#> .
@prefix dct:    <http://purl.org/dc/terms/> .
```

---

## 8. Export y integración en LaTeX

### En drawio

Para cada figura:

1. `File → Export as → PDF`
2. Opciones: "Crop" habilitado, "Embed fonts", "Include a copy of my diagram" desactivado si no quieres que el XML quede embebido en el PDF.
3. Guarda como `paper/figures/fig1-architecture.pdf` / `fig2-classes.pdf` / `fig3-scenario.pdf`.

Alternativa: exporta también como SVG para tener la fuente editable:
- `File → Export as → SVG` → `paper/figures/fig2-classes.svg`

### En el .tex

Reemplaza cada bloque `tikzpicture`:

```latex
\begin{figure*}[t]
\centering
\includegraphics[width=\textwidth]{figures/fig2-classes.pdf}
\caption{Overview of the DAIMO native classes …}
\label{fig:classes}
\end{figure*}
```

Los captions y labels actuales son reutilizables tal cual.

### Consistencia entre versiones

Hay cuatro `.tex`: EN Sage, EN 1col, ES Sage, ES 1col. El archivo PDF de la figura es el mismo en las cuatro; sólo cambian el caption y las menciones a "Figure" / "Figura".

---

## 9. Checklist antes de exportar

- [ ] Todos los prefijos usados están declarados en el bloque de prefijos.
- [ ] Todas las clases DAIMO y externas tienen el `prefix:LocalName` correcto.
- [ ] `rdfs:subClassOf` siempre usa línea sólida + triángulo hueco, nunca otra combinación.
- [ ] `rdf:type` (Fig 3) siempre usa línea punteada + triángulo relleno.
- [ ] Propiedades: línea sólida + triángulo relleno, con label prefijado.
- [ ] Characteristics `(F)`, `(A)`, `(IF)` etc. aparecen en paréntesis antes del nombre, no después.
- [ ] Individuos llevan el texto **subrayado**.
- [ ] Datatype ranges llevan borde **punteado**.
- [ ] La leyenda está dentro de un Legend Container (el converter Chowlk lo ignora).
- [ ] El texto no se sale de las cajas.
- [ ] Ningún edge cruza una caja.
- [ ] Labels sobre edges no solapan con otras líneas (usa fondo blanco si hace falta).

---

## 10. Gotchas habituales

| Error común | Síntoma | Fix |
|---|---|---|
| Triángulo relleno en subclassOf | Arrow no reconocida por Chowlk converter | Cambia a "Open Block" thin en el menú Edit Style |
| Línea sólida en rdf:type | Converter genera object property en vez de rdf:type | Línea a "Dashed" |
| Prefijo sin declarar | Error del converter | Añadir la línea `@prefix` |
| Texto de clase con espacios en vez de camelCase | Nombres TTL inválidos | Usar PascalCase: `daimo:AIAssetOffering`, no `daimo:AI Asset Offering` |
| Individuo sin subrayado | Converter lo trata como clase | Marca el texto y aplica formato de subrayado |
| Datatype como caja sólida | Se interpreta como clase | Borde **punteado** obligatorio |
| Múltiples `rdf:type` en una instancia | Chowlk acepta comma separation | `ex:derivedPred a daimo:DerivedArtifact, dcat:Resource` |
| `owl:inverseOf` con rectángulos de clase | Converter da error | Usa nodos **rombo** (`<<owl:ObjectProperty>>`) |

---

## 11. Referencias

- **Notación oficial**: <https://chowlk.linkeddata.es/notation>
- **Página principal de Chowlk**: <https://chowlk.linkeddata.es/>
- **Chowlk converter (web)**: <https://chowlk.linkeddata.es/>
- **Library XML**: <https://chowlk.linkeddata.es/chowlk_library.xml>
- **diagrams.net (drawio)**: <https://app.diagrams.net>
- **Ejemplo SWJ que usa Chowlk**: RePlanIT ontology paper~\cite{kurteva}, Figs. 2-9
- **⚠️ WIDOCO NO genera diagramas Chowlk automáticamente.** La integración Chowlk está abierta como issue pendiente desde 2021 ([dgarijo/Widoco#484](https://github.com/dgarijo/Widoco/issues/484)) y no está implementada en ninguna versión. Lo único que WIDOCO produce visualmente es **WebVOWL** (flag `-webVowl`), que es una visualización interactiva HTML/JS, no una imagen estática, y no es adecuada para incluirla directamente en LaTeX sin captura de pantalla manual.

- **No existe ruta automatizada TTL → Chowlk.** Chowlk va en la dirección opuesta (drawio → TTL). Para obtener diagramas Chowlk sobre DAIMO hay que dibujarlos manualmente en drawio con la biblioteca Chowlk cargada, siguiendo las secciones §4–§6 de esta guía.

---

## 12. Tiempos estimados

| Tarea | Tiempo |
|---|---|
| Instalar drawio + cargar library | 15 min |
| Familiarización con shapes | 30 min |
| Fig 1 (arquitectura) desde cero | 1 hora |
| Fig 2 (clases) desde cero | 2-3 horas |
| Fig 3 (escenario) desde cero | 3-4 horas |
| Export + integración LaTeX | 30 min |

**Total ruta completa manual:** 7-9 horas.

**Nota importante:** no existe ruta semi-automática TTL → Chowlk. WIDOCO (pese a ser la herramienta estándar de documentación de ontologías) no soporta generación Chowlk todavía (issue abierto [#484](https://github.com/dgarijo/Widoco/issues/484)). Sí genera WebVOWL si se le pasa `-webVowl`, pero es interactivo HTML/JS y no sirve para LaTeX.
