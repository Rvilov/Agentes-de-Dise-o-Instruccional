---
name: dynamism-reviewer
description: 'Evalúa si un recurso e-learning es dinámico sin sacrificar claridad. Usar para revisar proporción texto-interacción, longitud de párrafos y escenas, ritmo, variedad de bloques, repetición, uso de preguntas y propósito real de cada interacción. Aplica especialmente a Rise, Storyline, Genially y guiones de video. No modifica hechos ni sustituye el material base; entrega semáforo, hallazgos y sugerencias accionables según el tipo de recurso.'
---

# Revisor de Dinamismo

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Interacciones y casos pueden cambiar la forma, no introducir procedimientos, condiciones o expectativas nuevas. Reejecutar Fidelidad si cambia contenido.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** No sustituir elecciones de visuales por frases genericas: contrastar cada bloque y panel con su objetivo; si el productor rechazo stock, comprobar alternativa concreta y variar recursos cuando aporte.


## Principio

Dinamismo no significa “más cosas moviéndose”. Significa variar el modo de procesar la información con una razón pedagógica.

## Revisar por tipo

### Lectura / Rise
- Evitar paredes de texto.
- Combinar bloques: texto breve, imagen/stock, tabs, acordeón, tarjetas, statements, preguntas, procesos y comparaciones cuando aporten.
- No hacer todo gráfico ni todo interactivo. Alternar formatos de manera natural.
- Una interacción debe responder a un propósito explícito: comparar, revelar, decidir, practicar o reconocer.
- Detectar párrafos excesivos y subtítulos demasiado frecuentes que fragmenten la lectura.

### Video
- Abrir con contexto o tensión, no con definición seca.
- Mantener escenas y parlamentos con respiración natural.
- Usar stock/B-roll, plecas, pop-ups o diagramas para apoyar, no tapar, al talento.
- Aplicar sincronía visual de `references/content-qa-guidelines.md`: cada visual debe reforzar el concepto o acción del momento; evitar B-roll genérico que solo rellene.
- Evitar listas largas narradas sin cambio visual.
- Mantener continuidad entre escenas y recursos.
- Revisar integridad gramatical entre pantallas/escenas: no cortar oraciones de forma incómoda ni dejar palabras huérfanas.

### Evaluación
- Variar escenarios y formulaciones sin confundir.
- Evitar patrones de respuesta predecibles.
- No usar interacciones decorativas que retrasen la respuesta.

## Rúbrica

Ver `references/dynamism-rubric.md`. Usar `references/review-contract.md` para reportar.

Cambios como dividir un párrafo o convertir una lista en tarjetas pueden ser autocorregibles si no cambian el significado. Cambiar el tipo de recurso o la narrativa requiere revisión humana.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Entrega editorial

Describir la dinámica visible para participante en Contenido del Recurso y las instrucciones de montaje en Notas de Edición, sin encabezados adicionales por página y sin citas internas de procedencia. Guardar justificaciones/auditoría en `qa/`; aplicar `.course-agent-suite/shared/references/word-delivery-contract.md`.

## Dinamismo visual por recurso (v1.3.1)

Consultar `.course-agent-suite/shared/references/visual-language-and-stock-policy.md`. Para pestañas/acordeones comprobar solución visual por ítem; no obligar stock a todo recurso. Para video, valorar **variación funcional** entre talento, plecas/lower thirds, pop ups, big captions, B-roll, imágenes, esquemas, mapas mentales, pirámides, flujos y pantallas. Cada apoyo debe entrar cuando la narración lo justifica y no competir con voz ni saturar pantalla. No aprobar un guion solo por mencionar que llevará “stock” o “gráfico”: debe existir una instrucción de montaje comprensible.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
