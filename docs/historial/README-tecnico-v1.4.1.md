# Course Agent Suite v1.4.1: fidelidad factual verificable

**Compatible con Codex y Claude Code.** Esta version agrega una compuerta independiente de evidencia factual por recurso, una auditoria de temas obligatorios para el curso completo y bloqueos de QA cuando los reportes de Fidelidad estan incompletos o corresponden a una version anterior.

## Que se comprueba

- **Documentos fuente:** el catalogo `qa/source-catalog.json` contiene las fuentes locales aprobadas, su rol y prioridad. El validador detecta documentos de material base en `sources/` que no se registraron y rechaza fuentes factuales ilegibles, sin transcripcion o imposibles de verificar. El SHA-256 liga la revision al archivo exacto.
- **Afirmaciones del Word:** `qa/R1.fidelity-ledger.json` registra cada parrafo de **Contenido del Recurso**, su clasificacion, sus afirmaciones y cada cita original con ubicacion concreta (`slide`, `paragraph`, `page`, `line`). Se verifica que el fragmento existe en el archivo/ubicacion indicada. No se insertan referencias en el Word.
- **Temas obligatorios:** `qa/course-coverage-contract.json` registra T1/T2, origen, obligatoriedad y recursos. Una segunda comprobacion verifica que cada tema obligatorio asignado tenga claims de respaldo. Al finalizar, `audit_course_coverage.py` inspecciona todos los recursos registrados en `qa/course-resource-index.json`.
- **Revision semantica independiente:** `source-fidelity-reviewer` debe entregar `qa/R1.fidelity-review.json` con su evaluacion por afirmacion y tema. La existencia de una cita **no demuestra** por si sola que la cita respalde la afirmacion. Falta de juicio por claim, dato alterado o tema omitido => ROJO.
- **Versiones posteriores:** si el Word o una fuente cambia, sus SHA-256 ya no coinciden. El QA Final reabre el Word/fuentes y repite el gate; **no confia solo en reportes de color verde**. Tras una reescritura del Humanizador hay que repetir la revision factual.

## Instalacion/actualizacion sobre un proyecto existente

Descargar/descomprimir la suite completa y ejecutar desde su directorio:

```bash
python install_suite.py --platform codex --project-dir "/ruta/a/tu/proyecto"
# o para Claude Code:
python install_suite.py --platform claude --project-dir "/ruta/a/tu/proyecto"
```

La instalacion respalda skills e instrucciones anteriores; conserva `sources/`, `resources/`, `outputs/` y `qa/`. **No convierte automaticamente los Word antiguos en archivos aprobados:** deben tener registros nuevos, revision independiente y nueva auditoria.

## Migrar un curso a este control sin rehacer el contenido

1. Revisar `01_mapa_fuentes.md` y `02_matriz_cobertura.md`: asignar IDs estables F#/T# y localizar **todos** los archivos originales realmente entregados. No inferir su contenido si no estan disponibles.
2. Crear `qa/source-catalog.json`, `qa/course-coverage-contract.json` y `qa/course-resource-index.json`, consultando ejemplos en `shared/templates/`. El catálogo de fuentes debe reflejar el material de `sources/`; registrar la PPT de QA como `factual:false` si figura ahi.
3. Para cada recurso, ejecutar:

```bash
python .course-agent-suite/shared/scripts/fidelity_gate.py prepare --project-dir . --resource-id R1 --docx outputs/R1.docx
```

4. Completar las unidades, claims, fragmentos, ubicaciones y temas del JSON creado. El Productor no marca la revision como aprobada ni inventa citas. Solicitar al `source-fidelity-reviewer` la evaluacion semantica **por claim**, almacenada en `qa/R1.fidelity-review.json`.
5. Ejecutar el gate de Fidelidad y luego los controles integrados:

```bash
python .course-agent-suite/shared/scripts/fidelity_gate.py audit --project-dir . --resource-id R1 --docx outputs/R1.docx --report qa/R1.fidelity-preflight.json --strict
python .course-agent-suite/shared/scripts/run_quality_gates.py --project-dir . --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json
python .course-agent-suite/shared/scripts/audit_course_coverage.py --project-dir . --report qa/course-fidelity-preflight.json --strict
```

6. El `final-qa` exige los reportes JSON completos y `aggregate_reports.py ... --project-dir . --resource-id R1 --docx outputs/R1.docx`. Una revision parcial puede emitir diagnostico, pero **nunca aprobar integralmente**. Consultar `shared/references/source-fidelity-evidence-policy.md` para el contrato completo.

**Limite honesto:** los scripts comprueban el documento, los fragmentos, la cobertura declarada y la version. No descubren por si solos todas las afirmaciones omitidas ni determinan automaticamente si una cita implica semanticamente una afirmacion. La revision profesional de Fidelidad es una etapa obligatoria, separada del Productor. PDFs escaneados, contenido de imagen/video o fuentes remotas inaccesibles requieren inspeccion o una transcripcion aprobada; no se certifican en ausencia de esa evidencia.

---

# Importante: version 1.4.0 - notas uniformes y stock buscado realmente

La ultima version exige un **contrato editorial unico** por recurso y un **registro de busquedas de stock**. No es una sugerencia opcional: productor, revisores y QA final deben pasar tres scripts ejecutables. Ver `shared/references/editorial-stock-enforcement.md` y ejemplos en `shared/templates/`.

**Secuencia obligatoria por recurso:**

1. Crear `qa/R1.editorial-contract.json`, con filas/escenas en orden y `stock_decision` en cada una.
2. Evaluar si necesita stock. Si si, **ejecutar una busqueda en Magnific/Envato/Freepik o catalogo autorizado mediante herramienta disponible**, registrar resultados verificables en `qa/R1.stock-search-log.json`, seleccionar visual y colocarlo junto al contenido. Sin acceso real -> pendiente de implementacion, no verde. Si no necesita stock: registrar razon y `searches: []`; el revisor evaluara su pertinencia.
3. Redactar texto y colocar imagenes en la columna `Contenido del Recurso`. Compaginar todas las notas desde el JSON:

```bash
python .course-agent-suite/shared/scripts/editorial_contract.py apply --contract qa/R1.editorial-contract.json --docx resources/R1_borrador.docx --output outputs/R1.docx
```

4. Validar contrato y busqueda con un unico comando desde la raiz del proyecto:

```bash
python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json
```

5. Obtener revision real de relevancia/atribucion/licencia, revisar los links y **renderizar/inspeccionar cada pagina**; despues autorizar verde.

**Actualizar una suite instalada:** descomprimir v1.4.0 y ejecutar `python install_suite.py --platform codex --project-dir "<proyecto>"` (o `--platform claude`) en la misma carpeta de proyecto. Hace backup y conserva `sources`, `qa`, `outputs`, `resources`. La actualizacion no modifica Word historicos; para ellos generar el contrato y corregir las notas/visuales segun el nuevo gate.

---

# Course Agent Suite

Suite portable para automatizar construcción y QA de cursos e-learning a partir de uno o múltiples materiales base.

## Skills

- course-production-orchestrator
- resource-producer
- source-fidelity-reviewer
- pedagogical-reviewer
- dynamism-reviewer
- visual-stock-reviewer
- template-format-reviewer
- language-humanizer
- course-consistency-reviewer
- accessibility-reviewer
- final-qa

## Instalación

Si vas a crear o corregir Word por script, instala la dependencia `python -m pip install -r requirements.txt` (usa la carpeta descomprimida). El render exige LibreOffice y utilidades de PDF según el entorno.

Codex:

```bash
python install_suite.py --platform codex --project-dir /ruta/proyecto
```

Claude Code:

```bash
python install_suite.py --platform claude --project-dir /ruta/proyecto
```

El instalador copia las skills a `.agents/skills/` o `.claude/skills/` y añade un bloque de reglas globales a `AGENTS.md` o `CLAUDE.md` sin borrar contenido existente.

## Política de archivos y salida editorial v1.3

Los recursos se producen como `.docx` en la plantilla oficial **adaptada a A4 vertical**. Una sola cabecera de metadatos al inicio, seguida de Notas de Edición/recomendaciones y Contenido del Recurso. No se repiten las cabeceras al cambiar de página y no aparecen referencias a fuente, slides, transcripción o QA en el Word.

**La trazabilidad no se elimina:** se guarda en `qa/R##_trazabilidad.md` y manifest/reportes externos. Consultar `shared/references/word-delivery-contract.md`. La auditoría `skills/template-format-reviewer/scripts/audit_docx_structure.py` debe pasar con `--orientation portrait --traceability ... --strict` y cada página debe renderizarse e inspeccionarse.

No se suben los archivos a Google Drive ni a otro servicio salvo instrucción explícita.

## Guía de redacción

La suite incorpora **toda la presentación de 97 diapositivas** como **fuente normativa canónica** en `shared/source-guides/Content - Revisión QA x DI.pptx`. La guía `shared/references/content-qa-policy.md` establece cómo aplicarla, `content-qa-full-slide-index.md` conserva el texto editable de todas las slides, y `content-qa-control-register.json` asigna cada regla a los agentes con número de slide. El resumen `content-qa-guidelines.md` sirve de navegación **pero no sustituye la PPT**. El instalador copia todo a `.course-agent-suite/shared/` para uso offline de Codex y Claude Code.

La guía controla uniformidad de guiones, arquitectura de bloques, patrones IA, evaluación, sincronía visual, integridad gramatical, puntuación y tú/usted. La suite distingue reglas de ejercicios y ejemplos. **Punto y coma:** la PPT solo lo menciona en slide 26, no explica sus usos generales; el suplemento de español de la suite está separado y no se presenta como contenido de la PPT.

Para afirmar QA completo, registrar evidencia contra los **27 controles** aplicables; no basta con haber abierto el resumen. La ausencia del PPT original/índice produce `CONTENT_QA_SOURCE_INCOMPLETE`.

## Activos técnicos pendientes

Si el material base menciona una URL/acceso pero no incluye la liga real, la suite no la inventa ni bloquea el contenido por ello. Registra la instrucción de enlazar el acceso oficial del cliente como pendiente de implementación.

## Lenguaje visual contextual v1.3.1

Aplicar `shared/references/visual-language-and-stock-policy.md`: si un recurso Rise usa pestañas o acordeones, definir propuesta visual por panel (imagen pertinente, captura autorizada o gráfico/alternativa justificada). **No imponer stock a todos los recursos**. En video, planificar apoyo audiovisual según escena: plecas/lower thirds, pop ups, big captions, video stock/B-roll, gráficos como mapas mentales, pirámides, diagramas, timelines, comparaciones o apoyo de interfaz, con cue narrativo y texto exacto en pantalla cuando aplique. **Stock-video recomendado = enlace real clicable en Notas de Edición**. Si aún no existe, `PENDIENTE_STOCK_VIDEO` y términos de búsqueda, sin falsa promesa de edición lista. Validar con `skills/visual-stock-reviewer/scripts/audit_visual_plan.py` cuando haya manifest.

## Notas de Edición concisas para TODOS los recursos (v1.3.3)

**Regla global, no solo Rise:** video (con talento, narrado o tutorial), Rise, lecturas, evaluaciones, descargables, infografías y cualquier Word. En la columna izquierda cada escena/apartado lleva nombre, tipo de bloque y 1-2 instrucciones ejecutables (objetivo 20-45 palabras; **máximo 60** por bloque). No escribir explicaciones largas, razonamiento pedagógico, QA, alternativas hipotéticas o fuentes. Imágenes reales y texto definitivo en **Contenido del Recurso** a la derecha. Los links de **clips de stock para video** sí aparecen como hipervínculos auténticos en las notas; los **timecodes de video** solo si son cues útiles de sincronización. Nunca colocar imágenes incrustadas en la columna Notas.

El patrón aprobado para la distribución de Rise sigue documentado en `shared/references/rise-editorial-reference.md`, a partir del Word final del equipo; **no reutilizar su tema o imágenes**. Ver contrato general `shared/references/editorial-notes-all-resources.md`.

Auditoría obligatoria de cada Word:

```bash
python .agents/skills/template-format-reviewer/scripts/audit_editorial_notes.py outputs/R1.docx --strict
```

En Claude Code cambiar `.agents` por `.claude`. **Para Rise, ejecutar además** `audit_rise_editorial.py`. El auditor comprueba forma, no reemplaza revisión humana de pertinencia ni render visual de cada página.

## Cómo actualizar una suite ya instalada (v1.3.3)

Descargar la nueva versión, **descomprimir en una carpeta distinta** de la anterior y ejecutar el instalador apuntando al **mismo directorio del proyecto**:

```bash
# Desde la carpeta course-agent-suite nueva
python install_suite.py --platform codex --project-dir "/ruta/a/mi-proyecto"
# O bien para Claude Code:
python install_suite.py --platform claude --project-dir "/ruta/a/mi-proyecto"
```

El instalador v1.3.3 **actualiza en sitio** los 11 directorios de skills con el mismo nombre, la carpeta compartida `.course-agent-suite/shared/` y el bloque marcado en `AGENTS.md` o `CLAUDE.md`; **no borra** `sources/`, `templates/`, `resources/`, `outputs/`, `qa/` ni otras skills instaladas. Crea una copia de seguridad del contenido anterior de suite e instrucciones en `.course-agent-suite/backups/<fecha>/`. Para revisar sin cambiar: añadir `--dry-run`. Si se personalizaron archivos **dentro de las 11 skills**, comparar con el backup porque se sobrescriben.

Cerrar y volver a abrir la sesión del agente tras instalar. Una actualización **no reescribe Word anteriores**: ejecutar nuevamente Producción + QA con el contrato v1.3.3. No hace falta crear otro proyecto.

## Paquetes individuales

`packages/<skill-name>/skill.zip` contiene cada skill validada por separado. `course-agent-suite-portable.zip` es el bundle para Codex/Claude Code y no debe subirse como una sola Skill a una interfaz que acepte únicamente un `SKILL.md` por ZIP.


## Comprobación de fuente QA

Tras instalar, ejecutar `python .course-agent-suite/shared/scripts/validate_content_qa_source.py --root .course-agent-suite/shared` para verificar integridad del PPTX, cobertura de slides, registros y acceso portable.

## Corregir un Word creado por una versión anterior

En la copia instalada del proyecto:

```bash
# Requisito para normalizar documentos Office (se instala una vez)
python -m pip install python-docx

# 1. Corregir orientación, anchos de tabla y desactivar filas de encabezado repetido
python .agents/skills/resource-producer/scripts/normalize_resource_docx.py \
  outputs/R1_Anterior.docx --output outputs/R1_Corregido.docx --orientation portrait

# 2. Mover citas internas "Fuente:", "Material base:" y "Slides de referencia:"
# desde el Word a qa/R1_trazabilidad.md. No suprimir la evidencia: trasladarla.

# 3. Validar estructura y existencia de trazabilidad separada
python .agents/skills/template-format-reviewer/scripts/audit_docx_structure.py \
  outputs/R1_Corregido.docx --orientation portrait \
  --traceability qa/R1_trazabilidad.md --strict
```

En Claude Code, sustituir `.agents/skills/` por `.claude/skills/`. **Después, renderizar y comprobar todas las páginas**; la auditoría estructural por sí sola no demuestra que el documento sea legible. Una actualización de la suite instalada **no reescribe retrospectivamente** los `.docx` que ya se habían generado.
