# Contrato editorial y búsqueda de stock verificable (v1.4.0)

**Obligatorio para TODOS los recursos y TODOS los agentes.** Esta política tiene prioridad sobre instrucciones anteriores de v1.3.x que describan el plan visual como opcional, o que permitan declarar un recurso listo con una imagen seleccionada sin buscar. No impone stock a cada pieza: impone **decidir y demostrar** qué visual conviene a cada bloque.

## Problema que resuelve

1. Notas de Edición variables entre cursos, aunque tengan menos de 60 palabras.
2. Recomendaciones de stock escritas sin una búsqueda real, o imágenes elegidas no insertadas.
3. Agentes que evitan la búsqueda poniendo `PENDIENTE_STOCK` o `NO_APLICA` sin evidencia.

## Contrato de producción de dos archivos QA (jamás dentro del Word)

Cada recurso R## requiere antes de redactar el Word:

- `qa/R##.editorial-contract.json`: **fuente única** de notas e inventario de bloques. Cada bloque declara `id`, `title`, `format`, `direction`, `stock_decision` (`needed` true/false y `reason` especifica), `visuals[]` con tipo y propósito, y `stock_assets[]` si selecciona stock. Cada pestaña/acordeón registra `panels[]` con una decisión visual por panel (puede ser imagen, captura, ícono, diagrama o texto justificado). Todo video incluye indicaciones por escena y puede incluir timecode útil.
- `qa/R##.stock-search-log.json`: **evidencia de ejecución**, con una fila por `asset_id`: proveedor/herramienta, consulta concreta, fecha, ID de resultado, candidatos encontrados y asset seleccionado; o resultado sin coincidencias tras dos búsquedas, o error técnico real de acceso. Una lista de enlaces inventados o una intención de búsqueda **no sirve**.

El Word final tiene solo la cabecera inicial, **Notas de Edición (izquierda)** y **Contenido del Recurso (derecha)**; trazabilidad y log permanecen en `qa/`.

## Estructura fija, sin variaciones de estilo entre cursos

Cada nota debe construirse exactamente desde el JSON con tres líneas y, **solo para video stock seleccionado**, un hipervínculo adicional:

```
1. Nombre del bloque
Rise: pestañas + imágenes.
Mostrar una imagen pertinente en cada pestaña y destacar los nombres de los casos.
```

```
2. Concepto clave (00:20-00:37)
Video: talento + pleca.
Mostrar la pleca "Tres decisiones" cuando inicie la explicación.
Stock: <título del clip, enlace real si se seleccionó stock-video>
```

Las **tres líneas** contienen: 1) índice+título, 2) etiqueta fija por tipo de recurso y mecanismo visual seleccionado, 3) instrucción accionable. No escribir 4-8 recomendaciones largas o historias de contingencias. Mantener objetivo 20-45 palabras y máximo 60 por fila; si una escena requiere más, **dividir la escena**, nunca ocultar instrucciones en texto del participante. Permitir timecodes solo para video sincronizado.

**Acción obligatoria antes de entregar:** ejecutar `python .course-agent-suite/shared/scripts/editorial_contract.py apply --contract qa/R1.editorial-contract.json --docx resources/R1_borrador.docx --output outputs/R1.docx`, tras crear filas y contenido; esto rellena las notas de forma determinista y conserva la columna derecha. Después, ejecutar `... editorial_contract.py audit --contract ... --docx outputs/R1.docx --strict`. Una nota redactada manualmente que se aleje de ese contrato **no pasa QA**, aunque tenga 20 palabras.

## Búsqueda real cuando el visual requiere stock

1. Antes de producir, **evaluar cada bloque/panel/escena**, incluyendo los que NO llevarán stock. Decidir entre stock imagen, stock video, fotografía provista, captura de interfaz autorizada, icono, diagrama (mapa mental, pirámide, flujo, etc.), talento a cámara o texto sin imagen cuando sea pedagógicamente válido. Escribir una razón específica en el JSON. Decir `NO_APLICA` no es razón suficiente.
2. Cuando se elija stock, **ejecutar la búsqueda de verdad** en Magnific/Freepik, Envato o proveedor autorizado. Si no hay conector, utilizar búsqueda web disponible orientada al catálogo del proveedor. El acceso es una capacidad del entorno; **la skill sola no habilita Magnific/Envato**. No asegurar que se buscó si no se llamó la herramienta o sitio.
3. Buscar por acción, contexto, personas/objetos y estilo, no por títulos abstractos como `productividad` sin más. Revisar resultados concretos y guardar referencia exacta (`result_ref`, ID de asset o URL de respuesta, proveedor, fecha, consulta y 1-3 candidatos pertinentes). Usar filtro sin IA si la Ficha Maestra lo exige; si el proveedor no permite verificarlo, marcar pendiente.
4. Elegir el asset que **represente el texto**, sin licencias inferidas. En Rise y lecturas, insertar la imagen realmente disponible en **Contenido del Recurso** junto al panel y enlazar la ficha del asset bajo ella; si se elige video stock, dejar un **hipervínculo real al clip** en Notas de Edición. Un enlace a resultados de búsqueda no es enlace de asset seleccionado.
5. Si el proveedor está inaccesible, guardar `status: access_blocked`, nombre de herramienta y error concreto. Si las búsquedas no devuelven material válido, registrar 2 consultas y `status: no_match` con evidencia. **No declarar listo** hasta localizar el activo o aprobar una solución visual alternativa que sí pueda montarse.
6. Si el recurso no necesita stock, `stock_decision.needed=false` con una razón por bloque. El revisor visual debe cuestionar decisiones sistemáticas de evitar stock en recursos largos o cuando el contenido se entendería mejor con una escena contextual. **No hay cuota de stock.**

## Gates automáticos y humanos obligatorios

**Siempre, todos los recursos:**

```
python .course-agent-suite/shared/scripts/editorial_contract.py audit --contract qa/R1.editorial-contract.json --docx outputs/R1.docx --strict
python .course-agent-suite/shared/scripts/audit_stock_execution.py --contract qa/R1.editorial-contract.json --search-log qa/R1.stock-search-log.json --docx outputs/R1.docx --strict
```

Añadir auditor universal (`audit_editorial_notes.py`), el auditor Rise cuando aplique, `audit_visual_plan.py`, auditor estructural, revisión de enlaces **y render de TODAS las páginas**. Si hay fallo, devolver al Productor y repetir (máximo 2 ciclos).

- `INVALID`: contrato distinto del Word; asset elegido sin búsqueda; link falso/no clicable; visual faltante; fila/panel sin decisión. **No hay VERDE.**
- `IMPLEMENTATION_PENDING`: búsqueda intentada sin resultado o acceso bloqueado. Puede aprobarse contenido factual, pero **no declararse listo para edición visual final**.
- `READY_FOR_VISUAL_REVIEW`: pruebas estructurales superadas. **No equivale a QA final verde**: el Revisor Visual tiene que inspeccionar la pertinencia, imagen real, licencia/condiciones de uso y apertura de URL en el proveedor.

Los dos auditores nuevos **no hacen búsquedas por sí mismos** y no pueden confirmar actividad remota. Exigen un registro respaldado por los resultados verdaderos. Nunca generar `result_ref` sintético para sortearlos.

## Responsabilidades

- Orquestador: exigir ambos JSON y reservar paso de búsqueda antes de escritura del Word.
- Productor: decidir, ejecutar búsqueda en herramienta autorizada, seleccionar, insertar, enlazar y usar compaginador de notas.
- Revisor Visual: comprobar evidencia de resultados, pertinencia, licencias, encuadre y accesibilidad visual.
- Revisor de Formato: ejecutar la prueba de equivalencia contrato/Word.
- QA Final: exigir ambos reportes, bloquear faltantes y distinguir contenido aprobado de visual pendiente.
- Demás revisores: aplicar el contrato sin agregar notas internas ni convertir recursos en catálogos de stock.

**Importante:** la información factual y el desarrollo del curso solo proceden del material base autorizado. Buscar stock externo es una búsqueda de **apoyos visuales**, no una licencia para introducir información nueva al contenido.

## Ruta operativa preferida: Magnific/Freepik cuando el conector este disponible

En Codex o Claude Code, el Productor debe **descubrir si el entorno dispone del proveedor**. Cuando Magnific/Freepik esta conectado y expone estas operaciones, ejecutarlas en este orden:

1. `mcp__Magnific__stock_search`: usar `query` concreto; `content_type="photo"` para imagen o `"video"` para B-roll. En la Ficha Maestra que prohibe imagenes IA, usar `ai_generated="excluded"`. Aplicar `orientation` solo si ayuda. Guardar `items[].id`, `title`, `previewUrl` y `relatedKeywords` de la respuesta real.
2. Evaluar varios candidatos visualmente y escoger el mas pertinente, no el primero sin inspeccion.
3. `mcp__Magnific__stock_get` con el **id exacto devuelto** y `type`; registrar URL persistente de la ficha, autor, orientacion y condiciones conocidas. **No inventar URL publica a partir de un id.** Si solo se obtiene URL efimera de preview/descarga, registrar enlace final pendiente.
4. `mcp__Magnific__stock_download` con id y tipo para obtener archivo de imagen aprobado, respetando permisos y licencia. Los enlaces de descarga firmados pueden caducar: **no utilizarlos como enlace estable en el Word**.
5. Insertar imagen autorizada en la columna `Contenido del Recurso` o, para video stock, enlazar el clip/asset con URL persistente en `Notas de Edicion`. Registrar el identificador de resultado verdadero en el log.

Si Magnific no esta configurado, buscar mediante las herramientas web accesibles en el catalogo autorizado (Freepik, Envato u otro). Registrar `provider`, nombre de herramienta, enlaces del resultado y hora. Si ninguna herramienta permite consultar stock, registrar `access_blocked` con el error real; **la falta de integracion no equivale a busqueda realizada ni justifica un verde visual**. Exigir que el usuario conecte el proveedor si los assets son obligatorios para concluir el recurso.

## Control contra omitir stock sistematicamente

Si un recurso de **tres o mas bloques** no elige ningun stock, el validador NO da preparacion visual terminada sin `all_no_stock_review` en el log interno, con `reviewer: visual-stock-reviewer`, `accepted: true` y `rationale` que justifique las alternativas. **No significa obligar imagenes**: permite un recurso completo de diagramas/capturas/talento cuando ello es mejor, pero exige una segunda decision independiente y verificable.
