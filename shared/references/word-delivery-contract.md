> **Actualizacion 1.4.0 (prevalente):** consultar `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Las Notas de Edicion se generan desde el contrato JSON y el QA exige prueba de busqueda real cuando corresponde. El plan visual y el log de stock son obligatorios para todos los recursos, aun si registran no-stock con motivo.

# CONTRATO DE SALIDA — Word de diseño instruccional (v1.3)

Este contrato es **obligatorio** para Producción, Orquestación, Formato y QA Final; sustituye prácticas anteriores que mezclaban fuente/QA con el Word para edición.

## 1. Lo que recibe el equipo de edición

Cada recurso se entrega como **un solo `.docx`** elaborado a partir de la plantilla del equipo. **Solo** se permite:

- Una cabecera **única y visible al inicio**, dentro del cuerpo del documento, con los campos del recurso aprobados: Tipo de Recurso, Duración, Estilo/Edición, Descripción/Objetivo y, cuando esté incluido en la plantilla, su título.
- Debajo de ella, **Notas de Edición** (incluidas las recomendaciones concretas de realización, ritmo, visual, stock, animaciones, bloques y recursos) y **Contenido del Recurso** (textos, diálogos, narración, reactivos, retroalimentación, etiquetas para pantallas cuando correspondan).
- Hipervínculos reales a material de stock cuando los vaya a usar el editor, enlaces que sean **parte del recurso** y notas técnicas de implementación como `Enlazar al acceso oficial proporcionado por el cliente` si falta esa URL.

No agregar portada decorativa, sección introductoria fuera de la cabecera, segundo encabezado de metadatos, resumen de QA, tabla de procedencia ni bibliografía de producción.

## 2. Estructura y paginación

- **Orientación predeterminada A4 vertical (portrait)** por solicitud del equipo. Si la plantilla binaria heredada está en horizontal, prevalece esta definición actual para **nuevos entregables**. Cambiar a horizontal **solo por instrucción explícita y documentada**; no imponerla porque el asset antiguo sea horizontal.
- La cabecera aparece **una sola vez**, al comienzo del Word; ni `w:header` de Word ni filas de tabla `w:tblHeader` deben hacerla repetir en páginas posteriores. No copiar el bloque de metadatos al empezar una página.
- Los saltos de página **continúan** el texto o la tabla de notas/contenido; no reinician el recurso. No duplicar títulos ni rótulos de columnas en nuevas páginas, a menos que el equipo lo solicite de forma explícita.
- Conservar tipografías, colores, bordes, proporciones y datos aprobados de la plantilla en la medida compatible con el formato vertical. Si la conversión a vertical no permite preservar la legibilidad, **rediseñar proporcionalmente, renderizar y validar visualmente**; nunca comprimir el contenido hasta hacerlo ilegible.
- Inspeccionar **cada página renderizada**. Ninguna tabla rota, corte, solapamiento, imagen recortada, hoja en blanco o encabezado reiterado pasa a QA verde.

## 3. Información PROHIBIDA dentro del Word final

- `Material base: ...`, `Slides de referencia: ...`, `Fuente: presentación ...`, nombres de archivos fuente, páginas/diapositivas/minutos de los que se extrajo una afirmación, IDs F1/F2 u otras marcas de procedencia.
- Matriz de cobertura, citas de validación, trazabilidad factual, decisiones entre fuentes, niveles de confianza, reportes de revisores y hallazgos QA, justificación técnica de cada afirmación.
- Notas internas sobre por qué se eligió una fuente o se descartó otra; esos razonamientos no son instrucciones para el equipo de edición.

**Excepción semántica:** no eliminar datos/documentos citados *como contenido del aprendizaje* (p. ej., normas legales, avisos que el participante debe consultar). La prohibición es sobre referencias **internas de producción**.

## 4. Archivos separados de control interno

Mantener **fuera del Word** y preferentemente bajo `qa/`:

- `R##_trazabilidad.md`: tabla `Bloque/contenido | Fuente ID | ubicación en fuente (página/slide/minuto) | nivel de uso | estado de validación | observaciones`.
- `R##.manifest.json`: metadatos internos, URLs del stock y demás decisiones auditables; no entregarlo como parte del documento de edición.
- `R##_qa.json`/`R##_qa.md`: hallazgos y evidencias de revisores.
- Mapa de Fuentes y Matriz de Cobertura del curso (a nivel proyecto).

El revisor de Fidelidad consulta dichos archivos y compara **el contenido real del Word** contra las fuentes, sin pedir que la prueba aparezca en el Word. Afirmaciones no rastreables siguen siendo un error de Fidelidad, pero la solución es añadir/actualizar la trazabilidad **fuera** del documento.

## 5. Secuencia de producción

1. Construir documento en la plantilla; orientar en vertical y ajustar el ancho de las columnas sin degradar la legibilidad.
2. Mantener **solo la cabecera inicial**; añadir nuevas filas de contenido sin `w:tblHeader` ni nuevos metadatos.
3. Redactar texto y notas de edición con los activos necesarios. Registrar fuente/ubicación en `qa/R##_trazabilidad.md`, no en el Word.
4. Ejecutar normalización estructural (orientación/filas repetibles) cuando sea seguro.
5. Ejecutar `template-format-reviewer/scripts/audit_docx_structure.py archivo.docx --orientation portrait --traceability qa/R##_trazabilidad.md --strict` y **corregir todos los códigos de fallo**.
6. Renderizar a PNG y revisar **todas** las páginas; solo después se solicita aprobación del QA Final.

## 6. Gates automáticos mínimos

- `PAGE_ORIENTATION`: no es vertical sin permiso explícito de otro formato.
- `REPEATING_TABLE_HEADER` o `REPEATING_WORD_HEADER_PART`: cabecera se repite potencialmente.
- `HEADER_LABEL_COUNT`, `META_HEADER_NOT_FIRST_BODY_BLOCK`, `BODY_CONTENT_OUTSIDE_EDITORIAL_TABLE`: cabecera ausente, mal ubicada o duplicada, o notas/contenido fuera de las columnas autorizadas.
- `VISIBLE_SOURCE_TRACEABILITY`: procedencia/ID/documento fuente aparece en el Word.
- `TRACEABILITY_SIDECAR_MISSING` / `TRACEABILITY_SIDECAR_UNPOPULATED`: no existe o no está diligenciado el archivo externo de trazabilidad requerido.
- `TABLE_WIDTH_OVERFLOW` / `TABLE_GRID_OVERFLOW`: la tabla conserva un ancho que podría salirse del papel vertical y cortar texto.
- `UNRESOLVED_PLACEHOLDER`: marcador temporal de producción que no debería publicarse.

La auditoría XML detecta estructura y señales de fuga, **no sustituye la inspección visual ni demuestra cobertura de todas las fuentes**. Las notas permitidas de stock y accesos técnicos pendientes no se consideran fuga de fuentes.


## Recomendaciones visuales por escena o panel (v1.3.1)

El Word editorial mantiene la misma estructura y **solo incluye notas accionables para la edición**, no referencias de origen. Para video, las Notas de Edición pueden describir plecas/lower thirds, pop ups, big captions, gráficos de mapa mental/pirámide/flujo/timeline/comparación, interfaz, B-roll e imágenes según convenga. Vincular cada apoyo al fragmento narrado, con texto exacto en pantalla cuando corresponda. **Cada stock-video concreto sugerido debe tener el enlace real como hipervínculo Word**; si no existe, registrar `PENDIENTE_STOCK_VIDEO` y términos de búsqueda en **`qa/`**, sin presentarlo como enlace ni como recurso listo en Word. Para pestañas/acordeones de Rise, incluir por panel visual pertinente o alternativa justificada. No imponer stock a todos los recursos. La evidencia interna del plan va en `qa/` y el manual completo en `visual-language-and-stock-policy.md`.

## 7. Rise: columnas y concisión vinculantes (v1.3.2)

- **Izquierda / Notas de Edición**: nombre numerado de sección + bloque Rise + 1-2 frases accionables. Orientación recomendada 20-45 palabras por apartado; **máximo 60 palabras**, salvo excepción aprobada en QA interno. No añadir explicaciones de por qué el agente tomó decisiones, hipótesis de acceso, fallbacks de interfaz ni advertencias técnicas extensas. El Word se debe poder ejecutar de un vistazo.
- **Derecha / Contenido del Recurso**: texto final del estudiante, títulos de acordeón/pestañas, instrucciones, reactivos, retroalimentación y las **imágenes realmente incrustadas** junto a cada panel que ilustran. Créditos y enlaces reales de imágenes debajo de las miniaturas, sin ensanchar la columna de notas. Si se escoge icono, diagrama o captura, colocarlo también junto al contenido.
- **No poner imágenes en Notas de Edición** ni listas de búsqueda de fotos. No poner tiempo `00:45–01:30` en Rise salvo sincronización de audio/video requerida. La duración del recurso solo va en la cabecera.
- **Pendientes/decisiones técnicas**: estados, enlaces no encontrados, alternativas descartadas y justificaciones de excepciones visuales van a `qa/` o al manifest. Conservar en Notas solo una instrucción simple verdaderamente útil, como `Enlazar el botón al acceso oficial del cliente`, sin comentarios extensos de contingencia.
- **Referencia estructural del equipo**: `shared/references/rise-editorial-reference.md`, extraída de `M1_R2_Imagen_por_elemento.docx`. Usar solo distribución/estilo/brevedad; jamás transferir hechos o imágenes de ese proyecto. Se mantienen cabecera única y orientación vertical estipuladas por este contrato incluso si la referencia está en horizontal.
- **Validación específica**: ejecutar `template-format-reviewer/scripts/audit_rise_editorial.py` en Word de Rise y revisar densidad, timecodes, imagen en columna correcta y contenido separado. Mantener `audit_docx_structure.py`, auditoría visual y render de todas las páginas.

## 7. Notas de Edición para todo tipo de recurso (v1.3.3)

La brevedad y separación de columnas son un **contrato universal**, no exclusivo de Rise: consultar `editorial-notes-all-resources.md`. En video, lectura, interactivo, evaluación, descargable o cualquier otro recurso, la columna izquierda contiene instrucciones breves y ejecutables (objetivo 20-45 palabras, máximo 60 por fila/escena), sin metarrazonamiento ni QA. Toda imagen incorporada en el Word va en Contenido del Recurso, vinculada al texto final. Los links de stock-video se mantienen clicables dentro de la nota de edición pertinente; no convertirlos en citas de procedencia. Timecodes solo si corresponden a sincronización audiovisual. Ejecutar para **cada Word** `template-format-reviewer/scripts/audit_editorial_notes.py <docx> --strict` y, cuando sea Rise, también `audit_rise_editorial.py`. Un rojo editorial bloquea la aprobación de formato.
