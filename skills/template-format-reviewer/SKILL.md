---
name: template-format-reviewer
description: 'Verifica que cada recurso e-learning se entregue como documento Word usando la plantilla oficial y respetando sus campos, secciones, duración, notas de edición y contenido. Usar antes del QA final para detectar estructura rota, campos faltantes, links que no son hipervínculos reales, imágenes fuera de lugar y defectos visibles tras renderizar. Mantiene el archivo local y no lo sube a Drive. Incluye auditoría estructural y un flujo de render visual cuando las herramientas del entorno lo permiten.'
---

# Revisor de Plantilla y Formato

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Mantener el rastro factual en qa/, nunca dentro del Word. Un DOCX formateado no esta aprobado si falta el ledger y la revision independiente de Fidelidad.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Ejecutar shared/scripts/editorial_contract.py audit por cada Word para comprobar correspondencia exacta con titulo, etiqueta, accion y stock link. No aprobar notas manuales fuera de plantilla aunque cumplan maximo de 60 palabras. Ejecutar audit_stock_execution.py para garantizar imagenes dentro de Contenido del Recurso.


## Gate de formato

Bloquear si:

- el entregable no es `.docx`;
- no usa la plantilla oficial o la plantilla aprobada del proyecto;
- faltan campos críticos;
- la tabla/estructura está rota o el diseño horizontal se entrega sin una autorización expresa;
- la cabecera informativa se repite tras saltos de página o aparece en una cabecera de Word;
- aparecen en el Word fuente, ubicación, timestamp de transcripción, IDs o trazabilidad/QA de producción;
- faltan los archivos de trazabilidad externos;
- un enlace obligatorio de stock no es hipervínculo real;
- el render muestra clipping, superposición, imágenes cortadas o texto ilegible.

## Revisar

1. Tipo de recurso, título del recurso, duración y estilo/edición **sin referencias a fuentes de producción**.
2. Descripción/Objetivo.
3. Sección de Notas de Edición y Contenido del Recurso.
4. Límites de palabras/duración definidos en la Ficha Maestra.
5. Hipervínculos externos reales.
6. Imágenes: presencia, tamaño y ubicación.
7. Nombres de archivo y un archivo Word por recurso.
8. Que no existan comentarios de trabajo, placeholders accidentales, `TODO`, `PENDIENTE` no autorizados o rutas internas visibles.
9. Que la arquitectura instruccional esté explícita cuando corresponda: botón, lista, pestaña, acordeón, esquema, proceso, tarjeta, etc., conforme a `references/content-qa-guidelines.md`.
10. En secuencias por pantalla/escena, revisar puntuación de cierre, mayúscula de inicio y ausencia de fragmentos huérfanos.

## Activo técnico pendiente no suministrado

Si el material base **menciona** una liga/acceso pero no incluye su URL, aceptar una nota explícita como `Enlazar al acceso oficial proporcionado por el cliente` siempre que el manifest la declare como activo de implementación. No tratarla como `TODO` accidental ni inventar una URL. Solo bloquear si la URL era parte del entregable final y sí fue suministrada pero quedó sin enlazar.

## Flujo de QA visual

1. Ejecutar `scripts/audit_docx_structure.py recurso.docx --orientation portrait --traceability qa/R##_trazabilidad.md --strict`. Solo permite horizontal cuando existe aprobación expresa, usando `--orientation landscape`. Si `pass_delivery=false`, bloquear; revisar `issues` para correcciones.
2. Renderizar el DOCX con la herramienta disponible. Si existe LibreOffice, `scripts/render_docx.py` puede exportar a PDF y PNG usando utilidades del sistema.
3. Inspeccionar **todas** las páginas a 100%.
4. Si el entorno no permite renderizar, marcar `RENDER_NO_VERIFICADO`; no declarar el formato totalmente aprobado.

Usar `references/review-contract.md`.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Contrato obligatorio del Word final (v1.3)

Antes de redactar, modificar, revisar o aprobar cualquier Word, leer `.course-agent-suite/shared/references/word-delivery-contract.md`. La cabecera informativa va **una vez al inicio** del cuerpo. Los recursos nuevos serán **A4 vertical** salvo instrucción explícita de orientación diferente, incluso si el asset heredado es horizontal. No repetir las filas de título o columnas al pasar de página (`w:tblHeader` desactivado); no insertar la cabecera en `w:header` de Word ni recrearla en otro bloque. Después de la cabecera entregar exclusivamente **Contenido del Recurso** y **Notas de Edición**, que incluyen recomendaciones editoriales y enlaces de stock de producción. Prohibido mostrar citas internas, nombre/ubicación del material base, IDs de fuente, matriz, evidencia de revisión o QA en el Word. Conservarlos únicamente en `qa/R##_trazabilidad.md`, manifest y reportes externos; nunca sacrificar fidelidad, solo separar su evidencia. Verificar estructura con el auditor y renderizar todas las páginas. Ante una orientación original contradictoria prevalece esta instrucción actual del equipo.

## Enlaces de stock en Notas de Edición (v1.3.1)

Cuando el Word de video recomiende un **clip de stock concreto**, comprobar en OOXML que el nombre o URL sea **hipervínculo externo real** a ese asset, no texto subrayado. Rechazar direcciones inventadas o páginas de búsqueda genérica como sustitutas. Si existe `PENDIENTE_STOCK_VIDEO`, registrarlo como activo pendiente, no como enlace verificado ni preparación audiovisual final. Las indicaciones de pleca, pop up, gráfico, mapa mental, pirámide o interfaz son Notas de Edición permitidas; no son fuente factual y no deben ocultarse en QA. Aplicar `.course-agent-suite/shared/references/visual-language-and-stock-policy.md`.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
