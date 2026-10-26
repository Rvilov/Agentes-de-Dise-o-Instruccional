# Version 1.4.1 - Evidencia factual y bloqueo de QA integral

- `shared/scripts/fidelity_gate.py`: nuevo gate de evidencia por cada afirmacion, integridad SHA-256 del Word y fuentes, cita literal en ubicacion real, clasificacion de todos los parrafos de Contenido, cobertura de temas y revision semantica independiente por claim/tema.
- `shared/scripts/audit_course_coverage.py`: valida recursos y temas obligatorios del curso completo, no solo un Word.
- `shared/scripts/run_quality_gates.py`: incorpora `factual_fidelity` como paso obligatorio del preflight; archivo faltante o informe obsoleto = fallo.
- `skills/final-qa/scripts/aggregate_reports.py`: exige `source-fidelity-reviewer`, contexto del proyecto y Word, reejecuta la auditoria de fuentes y devuelve error de CLI en rojo. Una declaracion VERDE aislada ya no basta.
- `course-production-orchestrator`: scaffold con `qa/source-catalog.json`, `qa/course-coverage-contract.json`, `qa/course-resource-index.json` y Matriz de Cobertura con IDs de tema. Intake comprueba existencia, fuentes locales y cita por ubicacion.
- `source-fidelity-reviewer`: exige evaluacion independiente por afirmacion (`claim_assessments`) y tema (`topic_assessments`), que preserve condiciones, excepciones, nombres, cifras y prioridad de fuentes.
- `resource-producer` y restantes agentes: regla universal para no introducir hechos nuevos, no poner citas en el Word y repetir Fidelidad despues de cualquier reescritura.
- Se mantienen la PPT completa de QA, las notas editoriales uniformes, los controles de stock y el instalador de actualizacion segura de v1.4.0.
- **Limite:** la evidencia mecanica evita citas ficticias y revisiones obsoletas, pero no certifica entailment semantico ni hallazgos que el revisor humano omita.

---

## v1.4.0 - 2026-10-26

- Nuevo origen estructurado `qa/R##.editorial-contract.json` y generador `shared/scripts/editorial_contract.py`: Notas de Edicion con mismo patron en todos los cursos; auditor comprueba equivalencia literal con Word.
- Nuevo registro `qa/R##.stock-search-log.json` y validador `shared/scripts/audit_stock_execution.py`: cada busqueda de stock realmente realizada, con evidencia de herramienta, candidatos y colocacion/link en Word; no omitir busqueda con `PENDIENTE_STOCK`.
- Nuevo `shared/scripts/run_quality_gates.py` centraliza gates existentes y nuevos. Si recurso requiere stock no buscado, rechazar. Busqueda bloqueada o sin resultados = implementacion pendiente, no listo para edicion.
- Exigir decision contextual de stock en cada bloque/panel y revision visual independiente; **sin cuotas** de imagenes de stock.
- Integracion en 11 agentes, guia compartida, README, manifest y pruebas; conservada instalacion segura y la PPT QA original.

## 1.3.3 — Notas de Edición concisas en TODOS los recursos

- **Universaliza** el criterio de brevedad anterior de Rise: videos, lecturas, evaluaciones, descargables, juegos y demás entregables usan columna de notas breve (20-45 palabras objetivo, 60 máximo), sin metarrazonamiento ni contenido duplicado.
- Conserva enlaces reales de stock-video y timecodes útiles en videos; evita marcas de tiempo de video en Rise no sincronizado.
- Los gráficos, fotografías y capturas **incrustadas** van en Contenido del Recurso, no en la columna Notas de Edición, en cualquier tipo de recurso.
- Política transversal `shared/references/editorial-notes-all-resources.md`, leída por los 11 agentes.
- Auditor universal determinista `audit_editorial_notes.py` con gate en Formato y QA Final; para Rise sigue la auditoría complementaria `audit_rise_editorial.py`.
- Conserva PPT completa, política de fidelidad, A4 vertical, cabecera única e instalador de actualización segura.

## 1.3.2 — Rise editorial compacto e imágenes en columna de contenido

- Referencia estructural del documento final del equipo `M1_R2_Imagen_por_elemento.docx`: **notas breves a la izquierda**, texto de participante e **imágenes reales en el contenido a la derecha**. Su material de curso no se reutiliza en otros proyectos.
- En Rise, notas de edición de 20-45 palabras por bloque como objetivo y máximo 60. Eliminar timecodes sin audio sincronizado, hipótesis de interfaz, listas de alternativas y explicaciones de QA.
- Si se indica imagen por panel de Rise y el asset está disponible, insertar la foto/diagrama junto al panel en Contenido del Recurso, con crédito/enlace real; no desplazarla a la columna de Notas.
- Plan visual detallado y activos pendientes únicamente en `qa/` fuera del Word. Mantener para videos stock/B-roll enlazado y apoyo de plecas, pop-ups y gráficos contextual.
- `audit_rise_editorial.py`: gate determinista que revisa longitud/tempos de notas, ubicación de imagen y separación editorial.
- Sin cambiar el contrato de A4 vertical/cabecera única, la PPT de 97 diapositivas ni el instalador con backups.

# Changelog

## 1.3.1 — Lenguaje visual de Rise y video + actualización segura

- Tabs/Accordion: planeación de apoyo visual por panel, con alternativa explícita cuando una foto no conviene. Sin obligación de stock en todos los recursos.
- Video: notas por escena para plecas/lower thirds, pop ups, big captions, B-roll/video stock, gráficos (mapas mentales, pirámides, flujos, procesos, comparativos, jerarquías), interfaces y talento.
- Todo clip stock de video sugerido requiere URL real e hipervínculo clicable en Word. Pendientes se identifican sin inventar URLs ni declarar «listo para edición».
- Política visual central `shared/references/visual-language-and-stock-policy.md`; auditor del `visual_plan` para notas de edición y manifest QA.
- Instalador seguro para actualización en el mismo proyecto: backup de skills compartidas/instrucciones, `--dry-run`, preserve documentos, QA, fuentes y otras skills.

## 1.2.0

- La guía de 97 diapositivas pasa a ser **norma canónica íntegra**, no solo referencia resumida.
- Índice textual por diapositiva, inventario, registro de 27 controles trazados a slides y política de cobertura.
- 11 agentes con instrucción para consultar PPT original y controles pertinentes.
- Verificación automatizada de hash, inventario/cobertura y accesibilidad en instalaciones Claude Code/Codex.
- Diferenciación explícita entre regla contenida en la PPT y complemento de español sobre punto y coma.
- Gate `CONTENT_QA_SOURCE_INCOMPLETE` para no aprobar como verificación íntegra cuando falta el material.

## 1.1.0

- Incorporación portable de **Content - Revisión QA x DI.pptx**.
- Guía operativa compartida de lenguaje, evaluación, visuales e integridad gramatical.
- Política no bloqueante para URLs/activos técnicos mencionados pero no suministrados por el material base.
- Instalación local de referencias compartidas para Codex y Claude Code.
- QA y empaquetado completo de las 11 skills.

## 1.3.0 — Contrato editorial de Word, cabecera única y evidencia externa

- Preferencia obligatoria **A4 vertical** en nuevos recursos, aunque la plantilla histórica suministrada esté en horizontal, salvo autorización expresa del equipo.
- Cabecera del recurso una vez al principio del cuerpo; sin repetición en saltos de página ni `w:tblHeader`.
- Word limpio: Contenido del Recurso y Notas de Edición/recomendaciones, sin fuentes, números de diapositiva, nombres de archivos de origen ni hallazgos QA.
- Evidencia factual y QA obligatoria, pero en `qa/R##_trazabilidad.md`, manifest y reportes separados.
- Nuevo contrato común `shared/references/word-delivery-contract.md` en 11 agentes.
- `prepare_resource.py` genera sidecars en `qa/` y prepara Word en vertical; `normalize_resource_docx.py` ajusta orientación/repetición de forma segura.
- `audit_docx_structure.py` bloquea orientación, cabeceras reiteradas, fugas de fuente y trazabilidad externa ausente. Test con documentos con defectos y documentos normalizados, más render visual multippágina.
