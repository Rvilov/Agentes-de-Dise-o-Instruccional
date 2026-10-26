> **Actualizacion 1.4.0 (prevalente):** consultar `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Las Notas de Edicion se generan desde el contrato JSON y el QA exige prueba de busqueda real cuando corresponde. El plan visual y el log de stock son obligatorios para todos los recursos, aun si registran no-stock con motivo.

# Política visual contextual: Rise y video (v1.3.1)

## Regla principal

Seleccionar el apoyo visual por su **valor didáctico, exactitud, ritmo y editabilidad**, no por cuotas. Ningún recurso necesita obligatoriamente stock ni todos los recursos usan las mismas herramientas. La política se aplica si se **elige** un tipo de bloque o plano; explicar `NO_APLICA` cuando corresponda. Respetar los materiales base para hechos, marcas e interfaces. No crear afirmaciones o diagramas con relaciones inventadas.

## 1. Rise: pestañas, acordeones y otros bloques

- En **Tabs / pestañas** y **Accordion / acordeones** seleccionados, planear **un visual propio por ítem o panel** como criterio preferente de edición. Priorizar una imagen contextual distinta cuando ayude a identificar el concepto, objeto, acción o resultado que corresponde a ese ítem; no repetir una misma foto genérica.
- **No volcar el plan visual en Notas de Edición**: estas describen en 1-3 líneas el tipo de bloque Rise y una instrucción de montaje concreta. Las imágenes de cada panel van **incrustadas en la columna `Contenido del Recurso`**, junto al texto del panel al que pertenecen; debajo de la imagen, crédito/título y enlace real clicable cuando se disponga del asset. Motivo pedagógico, búsqueda de stock y estados de implementación van exclusivamente al manifest interno de `qa/`. No poner miniaturas, fotos ni listas de URLs de imagen en la columna de Notas de Edición.
- **Excepción justificable:** un panel puede prescindir de fotografía si se entiende mejor con un ícono, captura real autorizada de interfaz, diagrama o solo texto. Registrar la alternativa y razón concreta, ítem por ítem. No exigir imagen decorativa si contradice accesibilidad, claridad o naturaleza del bloque.
- En tarjetas, sliders, flip cards, pasos, procesos, comparativos, escenarios y bloques interactivos, decidir caso por caso; el hecho de ser interactivos no implica stock. Mantener una secuencia variada y pertinente, sin llenar todas las pantallas con fotos o iconos repetidos.
- **Referente editorial obligatorio para Rise**: si el diseño selecciona una imagen y el asset se encuentra disponible, **incrustar la imagen real en `Contenido del Recurso`** y colocarla junto al texto que ilustra. Una descripción en Notas de Edición **no sustituye** la imagen. Si el asset no está disponible, no simular una inserción terminada: registrar `PENDIENTE_STOCK_IMAGEN` y búsqueda en `qa/` y dejar el recurso **pendiente de implementación visual**, con una nota editorial breve solo si el montador la necesita. Excepciones sin fotografía (diagrama/ícono/captura/texto) deben planificarse y justificarse internamente, sin argumentaciones largas en el Word.

## 2. Video: gramática audiovisual (no solo stock)

Para cada escena o cambio importante de idea, escoger la solución adecuada y describirla en **Notas de Edición**, ligada al fragmento exacto de narración o momento de entrada. Opciones:

- `talent_only`: experto/talento en cámara cuando el discurso puede sostenerse sin apoyos; no imponer adornos.
- `lower_third`: pleca / lower third para concepto, nombre, definición corta; escribir **texto exacto en pantalla**, ubicación/entrada aproximada y motivo.
- `pop_up`: palabra clave, tip, cifra, recordatorio, llamada de atención; redactar texto exacto y cuándo aparece/desaparece. Evitar duplicación mecánica del audio.
- `big_caption`: énfasis breve o conclusión visual. No convertir todo el guion en captions.
- `stock_video`: B-roll que represente fielmente la acción o contexto; **enlace real y clicable obligatorio en el Word** cada vez que se recomiende una pieza concreta; incluir título/proveedor cuando exista, plano/acción y entrada narrativa.
- `stock_image`: imagen fija pertinente si aporta al concepto; incluir enlace real cuando se sugiera un stock específico o `PENDIENTE_STOCK_IMAGEN` y términos de búsqueda cuando no sea accesible, registrado solo en `qa/`.
- `mind_map`, `pyramid`, `flowchart`, `timeline`, `process`, `comparison`, `hierarchy`, `table`: gráficos didácticos, cada uno elegido por la relación que se comunica. Especificar componentes, etiquetas, orden, transiciones y vínculo con narración. Ejemplo: pirámide solo para niveles jerárquicos reales; flujo para decisiones o procedimientos; mapa mental para familias de ideas relacionadas.
- `interface`: captura o mockup autorizado, zoom/resaltado de botón o zona, con indicación precisa del elemento y el propósito de la toma.

**Regla de enlaces de video:** si una nota recomienda un video de stock concreto, agregar título hipervinculado o URL https real que apunte al asset en el Word. Enlazar una página genérica de búsqueda no satisface el requisito. Si no está localizado, usar `PENDIENTE_STOCK_VIDEO` más criterios de búsqueda en lugar de inventar enlaces o declarar la escena lista para editar; la evaluación de contenido puede ser positiva, pero la preparación audiovisual sigue **pendiente**.

## 3. Registro interno visual y verificación

El manifest `qa/R##.manifest.json` puede incluir `visual_plan` con `blocks` (Rise) y `video_scenes` (video). Los campos `purpose` y `description` especifican por qué se eligió la solución; cada escena identifica un `cue` ligado a la narración. **No trasladar el plan JSON ni la procedencia de fuentes al Word.** El Word contiene solo contenido + instrucciones visuales de edición y enlaces útiles.

Ejemplo de Rise:

```json
{
  "resource_type": "rise_interactive",
  "blocks": [
    {"id": "tabs-1", "kind": "tabs", "purpose": "Comparar tres casos", "items": [
      {"id": "tab-1", "title": "Caso A", "visual": {"kind": "custom_image", "description": "Escena que muestra el caso A", "purpose": "Reconocer el caso"}},
      {"id": "tab-2", "title": "Caso B", "visual": {"kind": "diagram", "description": "Comparación específica del caso B", "purpose": "Distinguir variables"}}
    ]}
  ]
}
```

Ejemplo de video:

```json
{
  "resource_type": "video",
  "video_scenes": [
    {"id": "escena-1", "cue": "Al introducir el concepto", "visuals": [
      {"kind": "lower_third", "on_screen_text": "Concepto clave", "purpose": "Fijar el término"}
    ]},
    {"id": "escena-2", "cue": "Al enumerar los niveles", "visuals": [
      {"kind": "pyramid", "description": "Tres niveles del modelo, solo si constan en fuente", "purpose": "Mostrar jerarquía"}
    ]}
  ]
}
```

Ejecutar cuando exista manifest: `python .agents/skills/visual-stock-reviewer/scripts/audit_visual_plan.py qa/R1.manifest.json --docx outputs/R1.docx --strict` (sustituir `.agents` por `.claude` en Claude Code). El auditor detecta ausencia de plan por panel, descripciones vacías, inventos de URL evidentes y falta de vínculos de stock de video en Word. **No reemplaza** revisión de las imágenes, validación manual de URL, pertinencia didáctica ni render del Word. No usar el conteo de enlaces/fotos como sustituto de la calidad.

## 4. Clasificación QA

- `VERDE`: hay decisión visual apropiada y ejecutable donde aplica; stock recomendado tiene URL real clicable en el Word.
- `AMARILLO_IMPLEMENTACION`: el contenido es correcto, pero una pieza de stock propuesta no está localizada: `PENDIENTE_STOCK_VIDEO/IMAGEN`. No marcar como listo para edición audiovisual.
- `ROJO_VISUAL`: se eligieron Tabs/Accordion con ítems sin solución visual ni excepción justificada; se declara un video concreto de stock sin URL y sin estado pendiente; stock genérico irrelevante, URL inventada, enlaces de texto no clicables, gráficos incorrectos o visuales cortados.
- `NO_APLICA`: los bloques o tipos no se usan o un recurso justifica no emplear elementos visuales; no exigir en todos los recursos.

## 5. Separación editorial

El Word conserva una sola cabecera inicial, contenido del recurso y **Notas de Edición** con los visuales sugeridos y enlaces reales para edición. Dejar nombres de fuentes, páginas, diapositivas, actas de QA y evidencia de validación únicamente en `qa/`, conforme a `word-delivery-contract.md`.

## 6. Economía y ubicación de las Notas de Edición para Rise (v1.3.2)

Regla de producción basada en el **patrón estructural** del ejemplo final `M1_R2_Imagen_por_elemento.docx` proporcionado por el equipo: una sola cabecera inicial y, debajo, una tabla editorial de **dos columnas**, `Notas de Edición` a la izquierda y `Contenido del Recurso` a la derecha. El ejemplo se usa únicamente como **referencia de distribución y brevedad**; nunca copiar el tema, personajes, afirmaciones, nombres comerciales, contenidos ni imágenes de ese curso a otro.

- **Nota editorial objetivo**: título numerado, `Rise: [bloque]` y máximo 1-2 frases imperativas sobre la presentación o énfasis. Apuntar a 20-45 palabras; hasta 60 cuando exista una razón editorial concreta. El resto es contenido de la columna derecha o QA interno. No escribir manuales, hipótesis, planes de contingencia, comprobaciones ni justificaciones largas.
- **Contenido del Recurso**: texto final que verá el participante, nombres de pestañas/apartados, instrucciones dirigidas al participante, opciones y retroalimentaciones, **imágenes incrustadas** correspondientes y una referencia breve enlazada bajo cada imagen real. El editor debe visualizar la intención sin tener que interpretar 200 palabras de instrucciones.
- **No usar timestamps** como `00:45–01:30` en interactivos Rise salvo que el recurso contenga audio/video sincronizado y el equipo lo solicite. La duración global pertenece a la cabecera.
- **No mostrar metarrazonamiento**: `si aún no tienes acceso`, `excepción visual justificada`, `plan de búsqueda`, `si no existe el bloque...`, `motivo QA`, `único panel de Copilot`, instrucciones de autoprotección del agente y listas de alternativas. Resolver internamente y trasladar al Word solo la decisión aprobada.
- **Video**: conservar timecodes si facilitan sincronización narrativa, con notas compactas por escena; si se propone B-roll/stock concreto, su enlace auténtico y clicable sí pertenece a las indicaciones audiovisuales. Usar el mismo criterio global de economía editorial en video (máximo 60 palabras por escena), admitiendo cues de sincronía y links de stock necesarios.
- **Gate**: usar `skills/template-format-reviewer/scripts/audit_rise_editorial.py` además de las verificaciones de Word e imágenes, y siempre renderizar/inspeccionar las páginas. No declarar verde editorial cuando haya notas densas, imágenes en la columna incorrecta o imagen prometida pero ausente.

## Forma editorial transversal v1.3.3

No confundir plan visual con Notas de Edición: el plan visual completo y excepciones van en `qa/`; el Word solo contiene **instrucciones de montaje concisas** en columna izquierda (20-45 palabras objetivo, 60 máximo) y contenido/visuales pertinentes a la derecha. Aplicar también a **todos los guiones de video**. Plecas, pop-ups, big captions, gráficos o B-roll se describen en la nota de su escena con **una decisión concreta**, sin justificación extensa. URL auténtica clicable si se propone stock-video. Ver `editorial-notes-all-resources.md` y `audit_editorial_notes.py`.
