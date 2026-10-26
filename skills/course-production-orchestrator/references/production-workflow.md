> **Actualizacion 1.4.0 (prevalente):** consultar `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Las Notas de Edicion se generan desde el contrato JSON y el QA exige prueba de busqueda real cuando corresponde. El plan visual y el log de stock son obligatorios para todos los recursos, aun si registran no-stock con motivo.

# Flujo de Producción y QA

## Flujo completo

`Brief → Ficha Maestra → Mapa de Fuentes → Matriz de Cobertura → resource-producer → source-fidelity-reviewer → pedagogical-reviewer → dynamism-reviewer → visual-stock-reviewer → template-format-reviewer → language-humanizer → course-consistency-reviewer → accessibility-reviewer → final-qa → entrega`

## Reglas aprendidas incorporadas

- Cada recurso final es Word en la plantilla oficial.
- Los archivos se mantienen locales; no subir a Drive salvo petición explícita.
- Lecturas: combinar stock + gráficos/diagramas + interacción; no reemplazar todo por diagramas.
- No usar capturas de slides con puro texto como visual.
- Stock citado en Word debe tener hipervínculo real.
- Si una imagen debía estar integrada, un enlace no cuenta como imagen insertada.
- Los gráficos deben revisarse visualmente: clipping, legibilidad, acentos, calidad.
- Evaluaciones: evitar patrones previsibles en letras correctas y no evaluar material marcado como referencia.
- Aplicar la PPT **Content QA x DI** íntegra desde producción y QA según `.course-agent-suite/shared/references/content-qa-policy.md`; usar su registro de 27 controles trazados a las diapositivas, no únicamente la guía resumida. Los juegos/ejemplos no se convierten en reglas. Uniformidad, arquitectura, evaluación equilibrada, sincronía visual, integridad entre pantallas y tú/usted deben quedar evidenciados en QA.

## Corrección híbrida

Corregir automáticamente solo errores objetivos y verificables. Máximo 2 ciclos automáticos por recurso. Escalar narrativa, pedagogía, ambigüedad entre fuentes, contenido externo o cambios semánticos.

## Separación obligatoria del paquete de entrega (v1.3)

Aplicar `.course-agent-suite/shared/references/word-delivery-contract.md`: Word A4 vertical, cabecera de metadatos una sola vez al inicio, sin filas Word `tblHeader` repetidas, y debajo exclusivamente Contenido del Recurso y Notas de Edición (incluidas recomendaciones de realización). Separar fuente, páginas/slides/minutos, justificación y QA en `qa/R##_trazabilidad.md`, manifest y reportes. **No incluir** esos datos en el documento para edición. Ejecutar auditoría estructural (`--strict`) y render visual página por página antes de permitir verde de formato y QA final.

## Decisiones visuales v1.3.1

Consultar `.course-agent-suite/shared/references/visual-language-and-stock-policy.md`. Si el productor elige pestañas o acordeón, registrar cada ítem y su visual propuesto o excepción justificada. En video, elegir lenguaje audiovisual significativo (talento, pleca, pop up, big caption, B-roll, gráfico, mapa mental, pirámide, interfaz...) con textos en pantalla/cues. El revisor visual aplica `audit_visual_plan.py` cuando corresponda. Ningún recurso requiere stock por defecto; cuando se recomienda un clip de stock concreto, se requiere URL real y clicable dentro del Word. Si no se consigue, estado audiovisual pendiente, no enlace inventado.


## Ciclo factual obligatorio v1.4.1

1. Mapa de Fuentes + contrato JSON `qa/source-catalog.json`, matriz con IDs T# y `qa/course-coverage-contract.json`.
2. Productor termina el Word, ejecuta `fidelity_gate.py prepare` y completa todas las unidades con claims y evidencias reales.
3. Revisor de Fidelidad **independiente** entrega `qa/R#.fidelity-review.json` con evaluación individual de claims, temas, condiciones y contradicciones.
4. `fidelity_gate.py audit --strict` reabre archivos reales y compara SHA-256, excerpts y cobertura. `run_quality_gates.py` incorpora este gate como `factual_fidelity`.
5. Tras cualquier cambio del Word, actualizar solo con nueva revisión de fidelidad; un review anterior queda inválido por hash.
6. `aggregate_reports.py` exige contexto del proyecto/Word y rehace el gate; `audit_course_coverage.py --strict` cubre todos los recursos declarados.

No aprobar globalmente si un tema obligatorio no tiene evidencia. Fuentes y QA nunca aparecen dentro del Word.
