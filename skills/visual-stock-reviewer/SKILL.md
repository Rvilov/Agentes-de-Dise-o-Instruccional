---
name: visual-stock-reviewer
description: 'Revisa la calidad visual y el uso real de stock en recursos instruccionales Word, Rise y video. Usar para confirmar que imágenes y gráficos representen el contenido, que haya una mezcla adecuada entre stock, diagramas e interacción, que no se usen capturas de slides textuales como recurso visual, que los gráficos sean legibles y que las referencias de stock tengan enlaces reales y clicables. Cuando el proyecto usa Magnific, valida la política no-AI y no inventa assets ni URLs.'
---

# Revisor Visual y de Stock

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Stock y graficos son visuales, no evidencia de hechos. No introducir textos o datos de stock que alteren la fuente. Reabrir Fidelidad si se generan nuevas afirmaciones en capturas, graficos o pop-ups.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Auditar independientemente la necesidad de stock por bloque y cuestionar NO_STOCK generalizado sin razon pedagogica. Verificar pruebas reales de consulta, resultado y relevancia; comparar seleccion, URL y figura insertada o link en Word. Si no hubo acceso, devolver implementacion pendiente, no verde. Emitir firma de revision visual fuera del Word.


## Revisar el resultado real, no la intención

Si una nota dice “agregar imagen” pero el Word no contiene la imagen cuando debía estar integrada, marcarla como faltante. Si un título de stock parece enlace pero no tiene relación de hipervínculo en el DOCX, marcarlo.

## Criterios

1. **Pertinencia:** la imagen ayuda a comprender el bloque; no es relleno genérico. Aplicar la sincronía de `references/content-qa-guidelines.md`: debe reforzar el concepto técnico, la acción, el contexto o el resultado exacto que se explica.
2. **Variedad equilibrada:** en lecturas, combinar stock + gráficos/diagramas + interacción cuando el contenido lo permita. No usar solo diagramas en todo el recurso.
3. **Fuente visual:** no pegar capturas de slides que solo contienen texto. Transformar ese contenido en diseño. Screenshots de formatos, ejemplos o interfaces solo si tienen valor visual y están autorizados.
4. **Calidad:** sin pixelación evidente, clipping, textos ilegibles, elementos deformados, bordes accidentales ni acentos incorrectos en gráficos.
5. **Stock real:** título, proveedor, URL e ID deben ser reales. No aceptar URLs inventadas.
6. **Magnific:** cuando sea el proveedor aprobado, buscar con IA excluida si la herramienta lo permite. Si no se puede comprobar el origen, marcar `PENDIENTE_VERIFICACION_STOCK`.
7. **Video:** referencias de stock en notas de edición deben estar hipervinculadas en el Word. No es necesario incrustar el video.
8. **Lecturas:** si la producción requiere imagen integrada, un link no sustituye la imagen.
9. **Gráficos:** preferir diagramas simples, comparaciones, procesos y tarjetas; evitar ilustraciones recargadas o demasiado textuales.
10. **Secuencia visual:** en recursos por pantallas/escenas, comprobar que visual y texto/audio evolucionen juntos y que no haya cambios de imagen sin relación con el mensaje.

## Herramientas

Ejecutar `scripts/audit_docx_assets.py` para contar imágenes e hipervínculos y listar URLs externas. Complementar con inspección visual de todas las páginas renderizadas. El script no reemplaza la revisión visual.

Usar `references/review-contract.md`.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Referencias que sí pertenecen a Notas de Edición

Las **URL reales de clips de video stock** pueden aparecer enlazadas en Notas de Edición. En **Rise**, las imágenes seleccionadas y los créditos/enlaces de stock de imagen se colocan **en Contenido del Recurso**, junto al bloque correspondiente, nunca en la columna de Notas de Edición. Diferenciar de las **citas internas del material base** (archivo, diapositiva, minuto, fuente ID), que van exclusivamente a `qa/R##_trazabilidad.md`. No agregar bibliografías ni evidencias de QA al Word. Consultar `.course-agent-suite/shared/references/word-delivery-contract.md`.

## Nuevo gate: Rise por panel y gramática audiovisual (v1.3.1)

Aplicar en cada recurso `.course-agent-suite/shared/references/visual-language-and-stock-policy.md` y `references/visual-checklist.md`. Cuando se elijan Tabs/Accordion en Rise, verificar propuesta visual **por panel** (foto adecuada, diagrama, interfaz o alternativa razonada); solicitar justificación concreta para `none`. No exigir imágenes de stock a recursos que no las necesitan. Para video, comprobar que el plan diferencia talento, plecas, pop ups, big captions, B-roll, imágenes, gráficos (mapa mental, pirámide, flujo, jerarquía, línea de tiempo...), y que cada propuesta tenga función didáctica, contenido visible definido y sincronía narrativa. **Si recomienda stock-video específico, el Word debe contener URL real como hipervínculo funcional**, no solo un nombre o página de búsqueda. Si no está disponible, marcar `PENDIENTE_STOCK_VIDEO` como implementación pendiente; no inventar asset. Revisar también imágenes de stock sugeridas y sus enlaces o estado pendiente. Cuando haya manifest, ejecutar `scripts/audit_visual_plan.py <manifest> --docx <Word> --strict`; registrar el diagnóstico separado del Word y realizar inspección visual manual.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
