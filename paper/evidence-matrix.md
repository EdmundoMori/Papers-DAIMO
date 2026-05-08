# DAIMO Paper — Evidence Matrix

Esta matriz acopla cada afirmación del paper (`paper/daimo-paper-es-v3.tex`) a un artefacto verificable del repositorio. Cada fila contiene:

- **Sección § párrafo**: ubicación en el paper
- **Afirmación**: frase o hecho extraído del texto
- **Tipo**: `factual` (dato verificable), `interpretive` (argumento defendible), `pending` (requiere acción externa)
- **Evidencia**: ruta al artefacto que respalda la afirmación
- **Estado**: `verified` (verificado contra artefacto), `needs-check` (pendiente de auditar), `pending-external` (marcado `\TODO` en rojo)

---

## 0. Inventario de artefactos (snapshots al 2026-04-23)

| Artefacto | Ubicación | Líneas | Contenido verificado |
|---|---|---|---|
| Ontología núcleo | `daimo/ontology/daimo-core.ttl` | 423 | 14 clases nativas, 29 `owl:ObjectProperty`, 8 `owl:DatatypeProperty`, 28 `owl:FunctionalProperty`, 5 `owl:AsymmetricProperty`, 5 `owl:inverseOf` |
| Alineamientos | `daimo/ontology/alignment.ttl` | 403 | 7 `rdfs:subClassOf`, 6 `rdfs:subPropertyOf` |
| Shapes SHACL | `daimo/shapes/daimo-shapes.ttl` | 412 | 18 `sh:NodeShape` (9 completitud + 3 conformidad + 6 invariantes), 6 `sh:SPARQLConstraint` |
| Grafo positivo | `daimo/examples/flood-risk-scenario.ttl` | 322 | 225 tripletas de datos; cada clase nativa instanciada al menos una vez |
| Grafo negativo | `daimo/tests/negative-examples.ttl` | 174 | 118 tripletas; 6 nodos focalizados (`bad:INV1-artifact`…`bad:INV6-offering`) |
| Consultas CQ | `daimo/queries/queries.md` | 358 | 23 consultas SPARQL organizadas en 5 categorías (R, D, E, V, G) |
| Reporte razonador | `daimo/reports/reasoner-report.md` | — | HermiT consistent=True 0.72s, OWL-RL 817→1988 (1171 materialised) 0.27s, 14 clases inspeccionadas, 0 advertencias entailment |
| Reporte validación | `daimo/reports/validation-results.md` | — | SHACL conforms=True sobre positivo; 23/23 CQs con conteos por consulta |
| Reporte negativo | `daimo/reports/negative-test-results.md` | — | 6/6 invariantes disparadas |
| Reporte OOPS! | `daimo/reports/oops-report.md` | — | 0 Críticos, 0 Importantes, 2 Menores (P13 afecta 34 elementos, P04 afecta 7) |
| Scripts | `daimo/validate.py`, `reasoner_check.py`, `oops_check.py`, `tests/negative_test.py` | — | Suite reproducible |
| Referencia humana | `daimo/ONTOLOGY-REFERENCE.md` | 850+ | Clase por clase con OntoClean tags, identity criteria, design choices |
| Matriz requisitos | `daimo/VALIDATION-MATRIX.md` | — | Trazabilidad requisito-evidencia original |

---

## 1. Métricas clave (a citar en el paper)

| Métrica | Valor verificado | Fuente |
|---|---|---|
| Perfil DL declarado | OWL 2 DL | `daimo-core.ttl` cabecera |
| Clases nativas totales | 14 (9 top-level + 5 `ParticipantRole` subclases) | grep `^daimo:[A-Z][a-zA-Z]+\s+a\s+owl:Class` en `daimo-core.ttl` |
| `owl:ObjectProperty` | 29 | grep |
| `owl:DatatypeProperty` | 8 | grep |
| `owl:FunctionalProperty` | 28 | grep |
| `owl:AsymmetricProperty` | 5 | grep |
| Pares `owl:inverseOf` | 5 | grep |
| `rdfs:subClassOf` a vocabularios externos | 7 | grep `alignment.ttl` |
| `rdfs:subPropertyOf` a vocabularios externos | 6 | grep `alignment.ttl` |
| `sh:NodeShape` totales | 18 | grep `daimo-shapes.ttl` |
| Shapes de completitud | 9 (una por clase DAIMO) | `daimo-shapes.ttl` |
| Shapes de conformidad | 3 (`OfferInDAIMOShape`, `MachineLearningModelInDAIMOShape`, `RunInDAIMOShape`) | `daimo-shapes.ttl` |
| Invariantes `sh:SPARQLConstraint` | 6 (INV-1…INV-6) | `daimo-shapes.ttl` |
| Preguntas de competencia | 23 | `queries/queries.md` |
| Tripletas del grafo positivo | 225 | `validate.py` output |
| Tripletas del grafo negativo | 118 | `negative_test.py` output |
| HermiT consistencia | True, 0.72s, 0 insatisfactibles | `reasoner-report.md` |
| OWL-RL materialización | 817 pre → 1988 post (1171 derivadas), 0.27s, 0 `owl:Nothing` | `reasoner-report.md` |
| Entailment check | 14 clases inspeccionadas, 0 advertencias | `reasoner-report.md` |
| OOPS! Críticos / Importantes / Menores | 0 / 0 / 2 | `oops-report.md` |
| OOPS! Menor P13 | 34 elementos afectados (sin inversa semánticamente útil) | `oops-report.md` |
| OOPS! Menor P04 | 7 elementos (clases externas declaradas localmente) | `oops-report.md` |
| SHACL conformidad positivo | conforms=True, 225 tripletas | `validation-results.md` |
| SHACL conformidad negativo | conforms=False, 6/6 invariantes disparadas | `negative-test-results.md` |
| CQ ejecución | 23/23 devuelven ≥ 1 fila | `validation-results.md` |

### Conteos por CQ (verificados)

| CQ | Filas | CQ | Filas | CQ | Filas |
|---|---|---|---|---|---|
| CQ-R1 | 3 | CQ-D1 | 3 | CQ-E1 | 4 |
| CQ-R2 | 1 | CQ-D2 | 2 | CQ-E2 | 1 |
| CQ-R3 | 1 | CQ-D3 | 4 | CQ-E3 | 2 |
| CQ-R4 | 2 | CQ-D4 | 1 | CQ-E4 | 1 |
| CQ-R5 | 2 |  |  | CQ-E5 | 1 |
| CQ-V1 | 1 | CQ-G1 | 1 |  |  |
| CQ-V2 | 1 | CQ-G2 | 2 |  |  |
| CQ-V3 | 2 | CQ-G3 | 1 |  |  |
| CQ-V4 | 1 | CQ-G4 | 1 |  |  |
| CQ-V5 | 4 |  |  |  |  |

---

## 2. Alineamientos a defender en el paper

### 2.1 `rdfs:subClassOf` (7)

| Clase DAIMO | Padre | Evidencia |
|---|---|---|
| `daimo:AIAssetOffering` | `dcat:CatalogRecord` | `alignment.ttl:~40`; defensa en `ONTOLOGY-REFERENCE.md §2.1` |
| `daimo:ExecutionAuthorization` | `odrl:Agreement` | `alignment.ttl`; defensa pendiente en §4.4 del paper |
| `daimo:ModelDeployment` | `prov:Entity` | `alignment.ttl` |
| `daimo:DerivedArtifact` | `prov:Entity`, `dcat:Resource` | `alignment.ttl` (alineamiento doble) |
| `daimo:CrossParticipantProvenanceRecord` | `prov:Bundle` | `alignment.ttl` |
| `daimo:AuditEvidence` | `prov:Entity` | `alignment.ttl` |
| `daimo:ParticipantRole` | `prov:Role` | `alignment.ttl`; caveat en `ONTOLOGY-REFERENCE.md §2.2` (PROV-O Role es activity-scoped, DAIMO dataspace-scoped) |

### 2.2 `rdfs:subPropertyOf` (6)

| Propiedad DAIMO | Padre | Justificación |
|---|---|---|
| `daimo:offersModel` | `foaf:primaryTopic` | Convención DCAT CatalogRecord → recurso descrito |
| `daimo:hasOfferPolicy` | `odrl:hasPolicy` | Herencia directa |
| `daimo:grantedTo` | `odrl:assignee` | Parte destinataria de la autorización |
| `daimo:derivedFromRun` | `prov:wasGeneratedBy` | Generación PROV |
| `daimo:contextTask` | `it6:hasTask` | Especialización sobre `SharedEvaluationContext` |
| `daimo:datasetVersion` | `dct:hasVersion` | Versionado de dataset en el contexto |

### 2.3 Subpropiedades deliberadamente NO declaradas (3)

Todas documentadas en `ONTOLOGY-REFERENCE.md` con razón:

- `daimo:authorizesRun` ⊄ `prov:used` — tiparía la autorización como actividad PROV
- `daimo:grantedTo` ⊄ `prov:qualifiedAssociation` — tiparía al agente como asociación reificada
- `daimo:evidenceOf` ⊄ `prov:hadActivity` — tiparía la evidencia como objeto de influencia

---

## 3. Matriz por sección del paper

### §1 Introducción

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §1 ¶1 | AI Act (UE 2024/1689) exige documentación, registro de ejecuciones, trazabilidad y evidencia de auditoría | factual | `aiact` ref; Art. 11 y Anexo IV del Reglamento | verified |
| §1 ¶1 | Eclipse EDC y DSP implementan el plano contractual de espacios de datos europeos | factual | `dsp`, `edc` refs | verified |
| §1 ¶2 | MLDCAT-AP 3.0.0 describe modelos ML como subclases de `dcat:Dataset` | factual | `mldcatap` ref; SEMIC 2025 | verified |
| §1 ¶2 | `odrl:Offer` no está anclada a un modelo concreto del catálogo | interpretive | razonamiento sobre ODRL 2.2 spec; no hay en ODRL una propiedad que conecte `Offer` → modelo de catálogo | verified |
| §1 ¶3 | Ninguna ontología reutilizable vincula hoy publicación + política + ejecución + auditoría + evaluación | interpretive | Tabla 1 del paper (matriz de reuso); §2 trabajo relacionado | verified |
| §1 ¶4 | DAIMO introduce 9 clases nativas de primer nivel más 5 subclases de rol | factual | `daimo-core.ttl` (grep verificado: 14 clases) | verified |
| §1 ¶5 | Verificación de implicación detecta alineamientos silenciosamente incorrectos | factual | `reasoner_check.py`; `reports/reasoner-report.md` §entailment-verification | verified |
| §1 ¶5 | Cada invariante SHACL-SPARQL va acompañada de caso de violación deliberado | factual | `tests/negative-examples.ttl`; `negative-test-results.md` | verified |

### §2 Trabajo relacionado

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §2.1 | Model cards / factsheets / datasheets son principalmente documentales | interpretive | `mitchell19`, `arnold19`, `gebru21` refs | verified |
| §2.2 | MLDCAT-AP reutiliza `it6:MachineLearningModel`, `it6:Run`, `it6:Flow`, `it6:Evaluation`, etc. | factual | MLDCAT-AP 3.0.0 spec; `daimo-core.ttl` (usa estas clases) | verified |
| §2.3 | DCAT, ODRL, PROV-O son agnósticos respecto al dominio IA | interpretive | especificaciones W3C | verified |
| §2.4 | EDC es framework Java, no vocabulario | factual | `edc` ref; repo Eclipse-EDC | verified |
| §2.4 | `edc:ParticipantContext` es la única extensión EDC referenciada | factual | `alignment.ttl` y `daimo-core.ttl` (grep `edc:`) | verified |
| §2.5 | RePlanIT, GloSIS, Woods et al. comparten compromiso con validación ejecutable | interpretive | `kurteva`, `palma`, `woods` refs | verified |
| Tabla 1 | Matriz de reuso comparando familias contra los cinco atributos operacionales | interpretive (sintético) | §2 del paper + tabla propia basada en análisis de las especificaciones | verified |

### §3 Metodología

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §3.1 | LOT estructura el desarrollo en 4 fases | factual | `lot22` ref | verified |
| §3.1 | 23 CQs organizadas en 5 categorías | factual | `queries/queries.md` (5 secciones H2, 23 H3) | verified |
| Tabla actores | 5 tipos de actor, 23 CQs | factual | `queries/queries.md` + §1.2 escenario | verified |
| §3.2 | Escenario UPM/Leganés/INESData | factual (marco) | §5 caso de estudio + `flood-risk-scenario.ttl` | verified |
| §3.3 | Tres decisiones de diseño (reuse-first, separación 3 capas, clase por hueco) | interpretive | `daimo-design-rationale.md`; `ONTOLOGY-REFERENCE.md` design choices | verified |

### §4 La ontología DAIMO

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §4.1 ¶1 | DAIMO modela publicación, descubrimiento, invocación, trazabilidad, evaluación | factual | 9 clases nativas del `daimo-core.ttl` cubren estas cinco tareas | verified |
| §4.1 ¶2 | Tres módulos: núcleo, alineamientos, shapes | factual | `daimo/ontology/daimo-core.ttl`, `alignment.ttl`, `shapes/daimo-shapes.ttl` existen separados | verified |
| §4.1 Fig 1 | Arquitectura modular Chowlk | pending | a generar | pending-external |
| Tabla métricas §4.2 | 14 clases, 29 OP, 8 DP, 28 Func, 5 Asym, 5 Inv, 7 subClassOf, 6 subPropertyOf, 9+3 shapes, 6 invariantes | factual | Sección 1 de esta matriz (todos verificados por grep o reporte) | verified |
| §4.3.1 | `AIAssetOffering` alineada a `dcat:CatalogRecord` | factual | `alignment.ttl` | verified |
| §4.3.1 | `AIAssetOffering` responde CQ-R1, R2, R5, G1 | factual | `ONTOLOGY-REFERENCE.md §2.1` + `queries.md` | verified |
| §4.3.2 | `ParticipantRole` con 5 subclases no disjuntas | factual | `daimo-core.ttl` (grep subClassOf) | verified |
| §4.3.2 | PROV-O Role es activity-scoped — caveat | interpretive | `ONTOLOGY-REFERENCE.md §2.2` | verified |
| §4.3.3 | `ModelDeployment` expone `dcat:DataService` sobre `it6:ComputerInfrastructure` | factual | `daimo-core.ttl` + ejemplo `flood-risk-scenario.ttl` | verified |
| §4.3.4 | `IOContract` sin alineamiento externo | factual | `alignment.ttl` no tiene entrada para IOContract | verified |
| §4.3.4 | IOContract captura formato E/S y método autenticación | factual | `daimo-core.ttl` propiedades `inputFormat`, `outputFormat`, `authMethod` | verified |
| §4.3.5 | `ExecutionAuthorization` ⊑ `odrl:Agreement` | factual | `alignment.ttl` | verified |
| §4.3.6 | `DerivedArtifact` alineada doble (`prov:Entity`, `dcat:Resource`) | factual | `alignment.ttl` | verified |
| §4.3.7 | `CrossParticipantProvenanceRecord` ⊑ `prov:Bundle` | factual | `alignment.ttl` | verified |
| §4.3.8 | `AuditEvidence` enlaza `spdx:Checksum` estructurado | factual | `daimo-core.ttl` + ejemplo `ex:audit-run-legs-checksum` | verified |
| §4.3.9 | `SharedEvaluationContext` reifica (tarea, dataset, versión, protocolo, semilla) | factual | `daimo-core.ttl` propiedades `contextTask`, `contextDataset`, `datasetVersion`, `protocol`, `randomSeed` | verified |
| §4.4 ¶1 | Defensa `AIAssetOffering ⊑ dcat:CatalogRecord` vs `dcat:Dataset` | interpretive | razonamiento DCAT spec + `ONTOLOGY-REFERENCE.md §2.1 design choices` | verified |
| §4.4 ¶2 | Defensa `ExecutionAuthorization ⊑ odrl:Agreement` vs `prov:wasDerivedFrom` | interpretive | ODRL 2.2 Agreement semantics; `ONTOLOGY-REFERENCE.md §2.5` | verified |
| §4.5 ¶1 | Axioma nombrado `daimo:TopLevelKindsDisjointness` | factual | `daimo-core.ttl` (grep `AllDisjointClasses`) | verified |
| §4.5 ¶2 | 28 propiedades funcionales, 5 asimétricas, 5 pares inversos | factual | matriz §1 | verified |
| §4.5 ¶3 | 3 subpropiedades deliberadamente NO declaradas | interpretive | `ONTOLOGY-REFERENCE.md` + `alignment.ttl` (su ausencia) | verified |
| §4.6 | Tabla de reuso de vocabularios | factual | `ONTOLOGY-REFERENCE.md §1` (tabla de prefijos) | verified |

### §5 Evaluación

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §5.1 | Escenario instancia UPM/Leganés/INESData/CSIC/Gaia-X | factual | `flood-risk-scenario.ttl` (grep instancias) | verified |
| §5.1 | Grafo de 225 tripletas | factual | `validate.py` output | verified |
| §5.1 | 3 `AIAssetOffering`s, uno con política comercial prohibida | factual | `flood-risk-scenario.ttl` | verified |
| §5.1 | Despliegue multi-endpoint REST + gRPC | factual | `flood-risk-scenario.ttl`; CQ-G2 devuelve 2 filas | verified |
| §5.1 | `spdx:Checksum` estructurado SHA-256 con digest explícito | factual | `flood-risk-scenario.ttl` `ex:audit-run-legs-checksum` | verified |
| §5.2 ¶1 | HermiT consistente 0.72s, 0 insatisfactibles | factual | `reasoner-report.md` | verified |
| §5.2 ¶1 | OWL-RL materializa 1171 tripletas, 0 `owl:Nothing` | factual | `reasoner-report.md` | verified |
| §5.2 ¶2 | Verificación implicación sobre 14 clases, 0 advertencias | factual | `reasoner-report.md` §entailment-verification | verified |
| §5.2 ¶3 | OOPS! 0/0/2, P13 afecta 34, P04 afecta 7 | factual | `oops-report.md` | verified |
| §5.3 ¶1 | SHACL conforma sobre grafo positivo | factual | `validation-results.md` | verified |
| §5.3 ¶2 | 6 invariantes INV-1…INV-6 detalladas | factual | `daimo-shapes.ttl` (grep SPARQLConstraint) + `ONTOLOGY-REFERENCE.md §8` | verified |
| §5.3 ¶3 | Listado INV-5 como `sh:SPARQLConstraint` | factual | `daimo-shapes.ttl` líneas de `OfferingPolicyTargetInvariant` | verified |
| §5.3 ¶4 | 6/6 invariantes disparadas sobre banco negativo | factual | `negative-test-results.md` | verified |
| §5.4 | 23/23 CQs devuelven filas, conteos específicos | factual | `validation-results.md` | verified |
| §5.4 | CQ-R2 y CQ-E1 dependen de `subPropertyOf` entailment | factual | `queries.md` consultas; razonamiento | verified |
| §5.5 | Reuso verificado: 7 subClassOf, 6 subPropertyOf a vocabularios externos | factual | sección §2 de esta matriz | verified |
| §5.6 | Validación con expertos pendiente | pending | —; 3 perfiles identificados | pending-external |

### §6 Discusión

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §6 ¶1 | DAIMO posicionada frente a RePlanIT, GloSIS, Woods | interpretive | refs + §2 del paper | verified |
| §6 ¶1 | 3 rasgos distintivos (implication check, INV + banco negativo, reuse axiomático) | interpretive | §5.2, §5.3, §5.5 del paper | verified |
| §6 ¶2 | Limitaciones: IOContract sin compatibilidad semántica fina | factual | `daimo-core.ttl` IOContract no tiene propiedades de esquema; `ONTOLOGY-REFERENCE.md §2.4` | verified |
| §6 ¶2 | SharedEvaluationContext sólo protocolo homogéneo | factual | `daimo-core.ttl` propiedades simples | verified |
| §6 ¶2 | Rol conflación tipo/asignación | interpretive | `ONTOLOGY-REFERENCE.md §2.2 design choices` | verified |
| §6 ¶3 | `daimo:records` tiene `rdfs:range prov:Activity` → tipados inferidos | factual | `daimo-core.ttl` (grep `daimo:records`) | verified |
| §6 ¶3 | Sin alineamiento a BFO/GFO/DOLCE/UFO | factual | `alignment.ttl` no contiene referencias a tales | verified |
| §6 ¶4 | CQ-R2 y CQ-E1 requieren razonamiento `subPropertyOf` | factual | ver §5.4 | verified |
| §6 ¶4 | Validación con expertos pendiente | pending | — | pending-external |
| §6 ¶5 | 4 CQ-G requieren semántica DAIMO-nativa | factual | `queries.md` CQ-G1..G4 usan `AIAssetOffering`, `ModelDeployment`, `ExecutionAuthorization`, `CrossParticipantProvenanceRecord` | verified |

### §7 Disponibilidad

| § ¶ | Afirmación | Tipo | Evidencia | Estado |
|---|---|---|---|---|
| §7 | Licencia CC-BY 4.0 ontología / Apache 2.0 scripts | factual | `daimo/LICENSE` y cabeceras | verified |
| §7 | Namespace `w3id.org/pionera/daimo` | pending | requires PR merge | pending-external |
| §7 | Repositorio GitHub público | pending | — | pending-external |
| §7 | Zenodo DOI | pending | — | pending-external |
| §7 | WIDOCO HTML documentation | factual | `docs/` + `widoco.jar` | verified |
| §7 | CONTRIBUTING.md + CHANGELOG.md + SemVer policy | factual | archivos existen | verified |

### §8 Conclusiones

Sólo sintetiza material ya evidenciado — toda afirmación redirige a secciones anteriores.

---

## 4. Items pendientes consolidados (todos marcados `\TODO` en rojo en el .tex)

1. **Fig 1 — Arquitectura modular DAIMO (Chowlk)**: 3 módulos + 5 capas de vocabularios reutilizados.
2. **Fig 2 — Vista general de clases DAIMO (Chowlk)**: 9+5 clases con alineamientos.
3. **Fig 3 — Diagrama del escenario de caso de uso**: UPM/Leganés/INESData/CSIC/Gaia-X con flujos.
4. **Merge del PR `perma-id/w3id.org`** para que `w3id.org/pionera/daimo` resuelva.
5. **Crear repositorio GitHub público** vía `DEPLOYMENT.md` e incluir URL.
6. **Archivar primera release en Zenodo** y minteado de DOI.
7. **Instanciar DAIMO sobre catálogo MLDCAT-AP real** o carta de compromiso UPM/INESData.
8. **Estudio con expertos del dominio**: 3 perfiles identificados (EDC/INESData, MLDCAT-AP/SEMIC, MLOps).

---

## 5. Política de auto-verificación

Antes de cerrar cualquier versión del paper:

1. Toda fila `factual` debe tener un artefacto verificable accesible (`verified` status).
2. Toda fila `interpretive` debe tener al menos una base documental citable.
3. Toda fila `pending-external` debe aparecer como `\TODO` rojo en el `.tex`; recíprocamente, todo `\TODO` del `.tex` debe aparecer en la matriz como `pending-external`.
4. Las métricas de la Tabla 1 (sección 1) son la única fuente de verdad para números citados en el cuerpo — no inventar números.
5. Si se modifica la ontología (`daimo-core.ttl`, `alignment.ttl`, `daimo-shapes.ttl`), re-ejecutar `validate.py`, `reasoner_check.py`, `oops_check.py`, `negative_test.py` y regenerar las métricas antes de tocar el paper.
