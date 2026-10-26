<!-- COURSE_AGENT_SUITE_START -->
## Course Agent Suite - reglas globales

- Tratar uno o múltiples materiales base como fuente de verdad operativa. No inventar ni completar con internet salvo autorización.
- Crear Ficha Maestra, Mapa de Fuentes y Matriz de Cobertura antes de producir.
- Generar cada recurso como Word independiente usando la plantilla oficial **adaptada a A4 vertical** (salvo otra orientación expresamente aprobada), con **una sola cabecera inicial** y sin repetirla en saltos de página; no usar `w:tblHeader`.
- Mantener entregables locales. No subir a Google Drive ni a otros servicios salvo petición explícita.
- Mantener el Word editorial limpio: solo cabecera inicial, Notas de Edición/recomendaciones y Contenido del Recurso. Prohibido insertar `Fuente:`, `Material base:`, `Slides de referencia:`, ubicaciones, IDs ni evidencia QA. Guardar estos datos **solo en `qa/`**, en manifest, trazabilidad y reportes.
- Aplicar `.course-agent-suite/shared/references/word-delivery-contract.md`. Ejecutar la auditoría estructural estricta + render visual antes de aprobar Word.
- Ejecutar el gate de Fidelidad antes de aprobar estilo o QA.
- Usar corrección híbrida: automático solo para errores objetivos; criterio/ambigüedad se escala.
- Lecturas: equilibrar stock, gráficos e interacción. No usar capturas de slides con puro texto como diseño.
- Verificar que enlaces de stock sean hipervínculos reales y que imágenes/gráficos declarados estén realmente presentes.
- Aplicar `.course-agent-suite/shared/references/visual-language-and-stock-policy.md`: si se eligen Tabs/Accordion en Rise, planear visual por panel o excepción razonada; en video elegir plecas, pop ups, big captions, B-roll/video stock, imágenes, mapas mentales, pirámides y otros gráficos según aporte didáctico, sin cuota obligatoria. Todo video-stock concreto sugerido exige URL real clicable en Notas de Edición; sin URL registrar `PENDIENTE_STOCK_VIDEO` únicamente en `qa/` y no declarar listo para edición audiovisual.
- Aplicar la PPT Content QA x DI **completa** desde producción y QA según `.course-agent-suite/shared/references/content-qa-policy.md`; usar `content-qa-control-register.json` (diapositiva+control+evidencia) e índice de las 97 diapositivas, no solo el resumen. Si falta PPTX o índice marcar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar QA total. En la PPT el punto y coma solo aparece mencionado en la diapositiva 26, sin regla general de uso; consultar complemento de español separado.
- Si la fuente menciona un acceso pero no suministra la URL, no inventarla ni bloquear Fidelidad; registrarla como activo técnico pendiente de implementación.
- Aplicar la guía interna de redacción definida en `language-humanizer`.
## Regla editorial universal v1.3.3 — TODOS los recursos

Usar `.course-agent-suite/shared/references/editorial-notes-all-resources.md` en **videos, Rise, lecturas, evaluaciones, descargables e infografías**. Notas de Edición = instrucciones breves de montaje (20-45 palabras recomendadas, 60 máximo por fila/escena); Contenido = narración/textos/reactivos e imágenes verdaderas a la derecha. No incrustar imágenes en Notas ni poner ahí razonamiento interno, fuentes, contingencias o planes alternativos. En video sí se admiten **cues temporales útiles** y URLs de stock-video real y clicable. En Rise, evitar marcas de tiempo salvo sincronización aprobada. Las decisiones extensas pertenecen a `qa/`. Gate de TODO Word: `template-format-reviewer/scripts/audit_editorial_notes.py --strict`; gate adicional Rise: `audit_rise_editorial.py --strict`, además del render.


## Guardarrailes de produccion v1.4.0 - PRIORIDAD ALTA

- Antes de hacer cada Word, crear `qa/R##.editorial-contract.json` y `qa/R##.stock-search-log.json` siguiendo `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Son obligatorios incluso cuando no se requiere stock (log con `searches: []`).
- **Nunca escribir Notas de Edicion libremente:** renderizar desde JSON con `shared/scripts/editorial_contract.py apply`. Estructura fija: titulo numerado; tipo + formato; 1 accion concreta. El codigo de video permite tiempo pertinente y enlace real de clip. Imagenes de stock en contenido del recurso.
- Cuando se elija stock, **buscar realmente** con proveedor/herramienta disponible, registrar consultas, resultado y candidatos. Si no hay acceso, usar `access_blocked` con error e impedir publicacion lista para edicion. `PENDIENTE_STOCK` por si solo no demuestra busqueda; no inventar URLs.
- Cuando se elija diagrama, icono, interfaz, talento o texto en vez de stock, justificar pertinencia en cada bloque/panel. No imponer stock por cuota. Revisor Visual debe cuestionar omision sistematica.
- Gate obligatorio en TODOS los recursos: `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`, mas revision humana de imagenes y PDF/PNG renderizado. Sin doble gate verde, NO declarar aprobado para edicion.

## Gate de fidelidad basado en evidencia v1.4.1 - NO NEGOCIABLE

- Toda fuente factual del curso requiere entrada verificable en `qa/source-catalog.json`; todos los temas obligatorios se registran en `qa/course-coverage-contract.json` y en la Matriz de Cobertura.
- Cada Word exige `qa/R#.fidelity-ledger.json` con TODAS las unidades de Contenido, claims verificables, evidencia real localizada (archivo, diapositiva/pagina/parrafo/minuto y fragmento) y coverage de temas.
- **No basta una cita para dar soporte semantico.** `source-fidelity-reviewer` debe comparar afirmacion y fuente, evaluar completitud, condiciones y excepciones, y documentar su juicio por claim y por tema en `qa/R#.fidelity-review.json`. No autofirmar aprobacion ficticia.
- Ejecutar `shared/scripts/fidelity_gate.py audit --strict` y `run_quality_gates.py` por recurso; `final-qa/scripts/aggregate_reports.py` REPITE la comprobacion y exige el reporte independiente. Para curso completo ejecutar `shared/scripts/audit_course_coverage.py --strict`.
- Hash cambiado de Word o fuente, evidencia inexistente, afirmacion sin soporte, tema obligatorio omitido o reporte de Fidelidad ausente => **ROJO para QA integral**. Repetir tras cualquier reescritura, resumen, ajuste de evaluacion o correccion editorial.
- Fuentes/ubicaciones/QA solo en `qa/`, nunca dentro de los Word. Las fuentes de estilo y catálogos stock no respaldan hechos del curso. No sustituir un video o PDF no legible por suposiciones.

<!-- COURSE_AGENT_SUITE_END -->
