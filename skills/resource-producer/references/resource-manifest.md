# Prioridad v1.4.0

**Contrato visual y editorial obligatorio.** Antes de generar cualquier Word, crear `qa/R##.editorial-contract.json` y `qa/R##.stock-search-log.json` (aunque la busqueda no sea necesaria: `searches: []`), segun `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. La anterior frase "Plan visual opcional" no aplica desde v1.4.0. Para tabs/acordeones, decision visual por panel, justificacion por bloque y registro de busqueda en todos los stock seleccionados. Ejecutar `shared/scripts/editorial_contract.py apply/audit` y `shared/scripts/audit_stock_execution.py --strict` antes de entregar.

# Manifest y trazabilidad INTERNOS — no incluir en el Word de edición

Guardar ambos archivos en `qa/` o en otra carpeta de control **distinta de `outputs/`**.

Ejemplo: `qa/R5.manifest.json`:

```json
{
  "resource_id": "R5",
  "title": "...",
  "type": "video | lectura | evaluación | ...",
  "objective": "...",
  "source_refs": [{"source_id":"F1","location":"slides 19-23","use":"contenido"}],
  "narrative": {"characters": ["Alex","Daniela"], "continuity_note": "..."},
  "visuals": [{"kind":"stock_video","title":"...","url":"https://...","embedded":false}],
  "interactions": [{"kind":"tabs","purpose":"comparar"}],
  "evaluation_key": [],
  "output_docx": "outputs/M1_R5_....docx"
}
```

Crear además `qa/R5_trazabilidad.md` con una fila por bloque factual del recurso:

| Bloque del recurso | Fuente ID | Ubicación (página/slide/minuto) | Uso | Validación | Observaciones |
|---|---|---|---|---|---|
| R5-B1 | F1 | diapositivas 19-23 | contenido | Pendiente de revisar | |

No añadir al Word la lista de fuentes, ubicaciones, IDs, nombres de archivos base ni evidencia de QA. El Word solo contiene cabecera inicial, Notas de Edición, recomendaciones editoriales y Contenido del Recurso. La trazabilidad sigue siendo obligatoria, pero **externa**.

## Plan visual opcional por tipo de recurso (v1.3.1)

Incluir `visual_plan` en el manifest cuando haya Tabs/Accordion o escenas audiovisuales. Según `shared/references/visual-language-and-stock-policy.md`, registrar en `visual_plan.blocks[]` cada bloque interactivo y sus `items[].visual`, y en `visual_plan.video_scenes[]` cada escena con `cue` y `visuals[]`. Alternativa `visual.kind="none"` exige motivo y es excepción, no forma de evitar el diseño visual. `stock_video` concreto exige URL https real y enlace clicable en el DOCX; sin ella, usar `status="pending"`, `search_terms` y etiqueta `PENDIENTE_STOCK_VIDEO`, lo cual deja la implementación audiovisual pendiente. El JSON pertenece a `qa/`, **no** al Word.


## Evidencia factual al producir v1.4.1

Guardar en `qa/R#.fidelity-ledger.json` un inventario completo de parrafos de `Contenido del Recurso` y sus afirmaciones, en lugar de insertar fuentes al Word. Ejecutar `shared/scripts/fidelity_gate.py prepare` **después** de la última escritura del DOCX, completar clasificación + claims + ubicación/cita literal y enlazar temas de `qa/course-coverage-contract.json`. El Productor no declara aprobado el reporte semántico independiente; debe pedir revisión al `source-fidelity-reviewer`. Tras reescrituras o revisión de lenguaje, el SHA cambia: volver a preparar/revalidar la evidencia y solicitar evaluación independiente.
