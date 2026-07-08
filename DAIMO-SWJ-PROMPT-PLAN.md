# DAIMO SWJ Prompt Plan

Este archivo fija el plan de trabajo para continuar la revision del articulo DAIMO con ChatGPT/Codex sin perder las restricciones cientificas del proyecto.

## Rol permanente

Actuar como editor cientifico experto en articulos de ontologias para Semantic Web Journal. El objetivo principal es mejorar el articulo desde el punto de vista editorial, cientifico, argumental y visual, no tratar el repositorio como documentacion interna de GitHub.

Reglas permanentes:

- La version maestra es `paper/daimo-paper-es-v4.tex`.
- `paper/daimo-paper-en-swj-v4.tex` es derivada de la version espanola y debe orientarse a Semantic Web Journal.
- No cambiar resultados de validacion, numeros, metricas, conteos ni claims empiricos si no estan documentados en los reportes de validacion del proyecto.
- No inventar funcionalidades de DAIMO.
- No anadir clases nuevas al nucleo de la ontologia.
- No fusionar `ai-model-discovery` dentro del core.
- No afirmar despliegue productivo, validacion externa por expertos, cumplimiento automatico del AI Act, motor federado, TEE implementado, endpoints reales o adopcion institucional si no esta demostrado.
- Mantener separadas la validacion ejecutable del artefacto ontologico, la validacion externa por expertos y el despliegue productivo real.
- Mantener la tesis reuse-first: DAIMO reutiliza MLDCAT-AP, DCAT, ODRL, PROV-O, DSP/EDC, FOAF, SKOS y SPDX, y solo anade clases puente cuando los vocabularios existentes no cubren la relacion necesaria.
- DAIMO no redefine el modelo de IA: reutiliza `it6:MachineLearningModel` de MLDCAT-AP.
- Usar estilo cientifico, sobrio, claro y directo.
- Evitar rutas internas del proyecto en el cuerpo principal del paper; reservarlas para apendices o material suplementario cuando sean necesarias para reproducibilidad.
- Toda tabla y figura debe estar introducida inmediatamente antes de aparecer.
- Revisar impacto en referencias cruzadas, captions, labels y compilacion LaTeX antes de cerrar cada bloque.

## Prompts aplicados

### Prompt 1. Diagnostico editorial y visual

Estado: completado.

Resultado principal:

- Se identifico tono interno y promocional en varias secciones.
- Se detectaron claims de novedad demasiado absolutos.
- Se senalaron repeticiones sobre reuse-first, no redefinicion del modelo, ausencia de despliegue federado y tipo de validacion.
- Se identificaron tablas densas y figuras con problemas de narracion inmediata.
- Se detectaron riesgos de claims no soportadas por reportes, especialmente sobre FAIR, validacion externa y banco negativo.

### Prompt 2. Revision de la version maestra espanola

Estado: aplicado en `paper/daimo-paper-es-v4.tex`.

Cambios principales:

- Introduccion reescrita con secuencia cientifica: problema, fragmentacion, brecha relacional, contribucion reuse-first, evidencia reproducible y estructura del articulo.
- Contribuciones compactadas en tres: perfil reuse-first con clases puente, validacion reproducible del artefacto y demostrador multi-participante acotado.
- Eliminado lenguaje de checklist editorial del cuerpo principal.
- Suavizadas claims absolutas de novedad y disponibilidad.
- Preservados todos los resultados de validacion documentados.

## Proximos prompts recomendados

### Prompt 3. Sincronizacion de la version inglesa

Objetivo: actualizar `paper/daimo-paper-en-swj-v4.tex` como derivada de la version espanola, manteniendo orientacion SWJ y sin introducir claims nuevos.

Entregables:

- Archivo ingles actualizado.
- Resumen de diferencias frente a la version espanola.
- Riesgos de traduccion o terminologia.
- Resultado de compilacion LaTeX.

### Prompt 4. Introduccion inmediata de tablas y figuras

Objetivo: revisar `paper/daimo-paper-es-v4.tex` para asegurar que toda tabla y figura este introducida inmediatamente antes de aparecer mediante un parrafo breve de 2-4 lineas.

Restricciones:

- No cambiar resultados, conteos ni claims empiricos.
- No reordenar masivamente secciones sin revisar labels y referencias cruzadas.

### Prompt 5. Compactacion de tablas densas

Objetivo: compactar tablas excesivamente densas sin perder trazabilidad cientifica.

Prioridad:

- Tablas de trazabilidad de requisitos y CQs.
- Tabla de terminos de dominio.
- Tabla de perfiles futuros.
- Tablas de metricas o disponibilidad, si reaparecen en versiones derivadas.

### Prompt 6. Revision visual academica

Objetivo: homogeneizar figuras y captions con estilo formal de articulo SWJ.

Restricciones:

- No crear nuevas clases ni propiedades.
- No convertir diagramas en claims de despliegue real.
- Mantener las figuras como apoyo interpretativo, no como sustituto de la argumentacion textual.

### Prompt 7. Auditoria final de claims contra reportes

Objetivo: comparar el manuscrito final contra:

- `daimo/VALIDATION-MATRIX.md`
- `daimo/reports/validation-results.md`
- `daimo/reports/reasoner-report.md`
- `daimo/reports/oops-report.md`
- `daimo/reports/negative-test-results.md`
- `daimo/reports/scalability-benchmark.md`

Entregables:

- Claims soportadas.
- Claims a suavizar.
- Claims a mover a limitaciones o trabajo futuro.
- Inconsistencias documentales pendientes.

### Prompt 8. Cierre pre-envio SWJ

Objetivo: realizar una pasada final de consistencia editorial, referencias cruzadas, captions, bibliografia, compilacion y disponibilidad del artefacto.

Entregables:

- Lista final de archivos modificados.
- Estado de compilacion de las versiones espanola e inglesa.
- Riesgos pendientes.
- Cambios recomendados para una siguiente ronda.
