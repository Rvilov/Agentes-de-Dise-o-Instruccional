---
name: resource-producer
description: 'Genera recursos instruccionales individuales a partir de una Ficha Maestra aprobada, Matriz de Cobertura y uno o varios materiales base. Usar cuando ya estén definidos el número y tipo de recursos y se deba producir R1, R2, R3, etc. Entrega cada recurso como Word independiente con la plantilla oficial, conserva trazabilidad a fuentes en archivos externos al Word, incorpora narrativa, interacción y visuales según el proyecto, y nunca sube archivos a Drive salvo petición explícita.'
---

# Productor de Recursos

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Preparar el ledger para el Word FINAL, clasificar todas las unidades, dividir afirmaciones y adjuntar evidencia literal a cada una. NO autofirmar la revision independiente. La ultima edicion invalida hashes y exige reauditar.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Producir primero contrato JSON y evaluar visuales por bloque/panel. Si seleccionas stock, llamar realmente al proveedor/consulta autorizados y guardar ID de respuesta, candidatos, seleccion, credito y estado. Incrustar imagen elegida en contenido y enlazarla; enlazar clips en Notas. Generar Notas solo con el compaginador. Nunca inventar resultados ni usar la palabra pendiente como sustituto de busqueda.


## Entradas obligatorias

- Ficha Maestra aprobada.
- Mapa de Fuentes y jerarquía.
- Filas de Matriz de Cobertura asignadas al recurso.
- Especificación del recurso: ID, tipo, duración, objetivo y plataforma.
- Plantilla Word oficial (`assets/resource_template.docx`) o una plantilla del proyecto declarada como sustituta.

No producir si falta una entrada crítica o existe un conflicto de fuentes sin resolver sobre el tema del recurso.

## Flujo

1. Leer solo las fuentes y ubicaciones asignadas al recurso. No mezclar temas de otros recursos.
2. Preparar un mini-plan: propósito, secuencia, interacción, narrativa, visuales, stock y cierre.
3. Redactar con el tono, persona lingüística, audiencia, narrativa y nivel de adaptación de la Ficha Maestra. Aplicar además `references/content-qa-guidelines.md` desde la primera versión para reducir retrabajo.
4. Mantener cada afirmación factual trazable a una fuente **solo en el manifest y en `qa/R##_trazabilidad.md`**; el Word visible no contendrá nombres de fuentes, páginas, slides, citas, IDs ni notas de QA. No completar con internet o conocimiento general salvo nivel 4 y autorización expresa.
5. Diseñar visualmente según el tipo:
   - Lecturas/interactivos: combinar texto breve, stock pertinente, gráficos/diagramas e interacción con propósito. No convertir todo en diagramas ni todo en interacción. Marcar en el guion qué bloque es botón, lista, pestaña, acordeón, esquema, proceso, tarjeta u otro componente cuando aplique.
   - Video: mantener el talento o experto a cámara cuando el proyecto lo exija; usar stock/B-roll, plecas, pop-ups, captions y diagramas como apoyo. Cada visual debe sincronizarse con el concepto o acción narrada; evitar stock genérico sin función pedagógica.
   - No usar capturas de slides con puro texto como sustituto de diseño. Si una slide contiene un formato, ejemplo o evidencia visual relevante, puede usarse solo si la Matriz la autoriza.
6. Stock:
   - Respetar proveedor y política de IA de la Ficha Maestra. Si se usa Magnific, priorizar `ai_generated: excluded`.
   - Guardar título, ID y URL real. En Word, el título del stock debe ser hipervínculo clicable cuando sea referencia de producción.
   - Si no se puede acceder al proveedor, registrar `PENDIENTE_STOCK` con términos de búsqueda **en el manifest/QA interno, no en el Word de Rise**; nunca inventar una URL ni afirmar que una imagen fue insertada si no lo fue.
   - En lecturas y Rise, cuando se seleccione una imagen y se disponga del asset, insertar la imagen real en Word **dentro de Contenido del Recurso junto al panel**, con crédito/enlace; nunca dentro de Notas de Edición. Un link o placeholder no cuenta como imagen integrada. Si falta el activo, marcar implementación visual pendiente en `qa/`, no crear una nota extensa.
   - Si el material base menciona un acceso, botón o liga pero **no proporciona la URL**, no inventarla. En Notas de Edición indicar: `Enlazar al acceso oficial proporcionado por el cliente`. Registrar el activo como pendiente de implementación, no como error factual.
7. Crear el `.docx` desde la plantilla, adaptar el formato a **A4 vertical**, preservar tipografía/bordes y mantener la cabecera informativa **solo al principio**, en el cuerpo. No repetir tabla ni encabezados en los saltos de página. Usar `scripts/prepare_resource.py` para preparar el Word y su archivo de trazabilidad, y `scripts/normalize_resource_docx.py` para ajustar orientación y eliminar `w:tblHeader` cuando sea seguro; luego revalidar el render.
8. Crear dos sidecars internos bajo `qa/`: `*.manifest.json` y `R##_trazabilidad.md`, siguiendo `references/resource-manifest.md`. No son parte del Word ni se entregan a edición salvo petición.
9. Guardar **solo los Word terminados** en `outputs/` y la evidencia/cobertura/QA en `qa/`. No subir ni sincronizar a Drive u otro servicio sin petición explícita.

## Evaluaciones

- Evaluar solo contenido marcado como evaluable.
- Evitar reactivos obvios y mantener una sola respuesta correcta en opción múltiple.
- Incluir retroalimentación correcta e incorrecta.
- Mantener opciones de longitud y estructura gramatical comparables para que la correcta no destaque visualmente.
- Usar distractores plausibles basados en errores reales; evitar distractores que sean solo el opuesto literal de la respuesta correcta.
- Distribuir las letras correctas para evitar patrones predecibles; rotar opciones sin alterar el significado.
- No evaluar detalles de ejemplos o material marcado como referencia.

## Salida

Entregar un Word por recurso y su manifest interno. El Word es el entregable oficial; el manifest sirve para QA.

## Límites de corrección

Corregir durante producción errores objetivos detectados. No resolver conflictos de fuentes, cambiar la narrativa aprobada ni agregar conocimiento externo sin autorización.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Contrato obligatorio del Word final (v1.3)

Antes de redactar, modificar, revisar o aprobar cualquier Word, leer `.course-agent-suite/shared/references/word-delivery-contract.md`. La cabecera informativa va **una vez al inicio** del cuerpo. Los recursos nuevos serán **A4 vertical** salvo instrucción explícita de orientación diferente, incluso si el asset heredado es horizontal. No repetir las filas de título o columnas al pasar de página (`w:tblHeader` desactivado); no insertar la cabecera en `w:header` de Word ni recrearla en otro bloque. Después de la cabecera entregar exclusivamente **Contenido del Recurso** y **Notas de Edición**, que incluyen recomendaciones editoriales y enlaces de stock de producción. Prohibido mostrar citas internas, nombre/ubicación del material base, IDs de fuente, matriz, evidencia de revisión o QA en el Word. Conservarlos únicamente en `qa/R##_trazabilidad.md`, manifest y reportes externos; nunca sacrificar fidelidad, solo separar su evidencia. Verificar estructura con el auditor y renderizar todas las páginas. Ante una orientación original contradictoria prevalece esta instrucción actual del equipo.

## Contrato visual contextual para Rise y video (v1.3.1)

Leer `.course-agent-suite/shared/references/visual-language-and-stock-policy.md` **antes** del mini-plan visual. Si se usan Tabs o Accordion en Rise, describir **por cada pestaña/panel** su imagen pertinente o recurso visual alternativo con justificación. No forzar fotos en otros tipos de bloques o recursos, pero tampoco permitir acordeones y pestañas diseñados como texto plano sin una decisión consciente. En cada video planear escenas con una **mezcla contextual** de talento, plecas/lower thirds, pop ups, big captions, pantallas, diagramas (mapas mentales, pirámides, flujos, comparativos, etc.), imágenes o B-roll; no exigir todas las categorías. Las Notas de Edición indicarán cue narrativo, recurso, texto exacto en pantalla cuando exista y montaje sugerido. **Toda recomendación de stock-video concreto lleva URL real hipervinculada en el Word**. Si aún no está localizada: `PENDIENTE_STOCK_VIDEO` + criterios de búsqueda; no inventar liga ni declararla lista de edición. Crear `visual_plan` en manifest interno según la política. Ejecutar auditor de plan visual y someterlo a visual-stock-reviewer y final-qa. Conservar el contrato editorial limpio de Word y fuentes en `qa/`.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
