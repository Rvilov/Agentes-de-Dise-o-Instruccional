> **Actualizacion 1.4.0 (prevalente):** consultar `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Las Notas de Edicion se generan desde el contrato JSON y el QA exige prueba de busqueda real cuando corresponde. El plan visual y el log de stock son obligatorios para todos los recursos, aun si registran no-stock con motivo.

# Política de gates

Orden recomendado:

`Fidelidad → Pedagógico → Dinamismo → Visual/Stock → Plantilla/Formato → Lenguaje → Consistencia → Accesibilidad → QA Final`

Un resultado verde posterior nunca anula un rojo de Fidelidad. QA debe preservar la evidencia de quién emitió cada hallazgo.

## Gate de la PPT íntegra

Previo a un VERDE integral, ejecutar `scripts/aggregate_reports.py` con los reportes de los revisores. Este script verifica la integridad de la fuente normativa `Content - Revisión QA x DI.pptx` y exige la cobertura de sus **27 controles** (incluidos `NO_APLICA` con justificación). No aceptar un reporte verde si faltan controles (`CONTENT_QA_COVERAGE_INCOMPLETE`) o falta el PPTX/índice (`CONTENT_QA_SOURCE_INCOMPLETE`). Consultar `.course-agent-suite/shared/references/content-qa-policy.md`.

## Gate de formato del Word y trazabilidad externa (v1.3)

No permitir VERDE si el Word final está en horizontal sin autorización, repite cabecera visible/tabla, muestra citas a materiales base, incorpora reportes internos o no tiene archivo externo de trazabilidad. Debe pasar `template-format-reviewer/scripts/audit_docx_structure.py <docx> --orientation portrait --traceability <qa/R##_trazabilidad.md> --strict`; más la inspección de todas las páginas renderizadas. Fuente faltante del material base se registra en QA externo, no dentro del Word. Consultar `.course-agent-suite/shared/references/word-delivery-contract.md`.

## Gate audiovisual y Rise v1.3.1

Aplicar `shared/references/visual-language-and-stock-policy.md`: cuando el recurso eligió pestañas/acordeones, exigir propuesta visual por panel o excepción razonada; cuando sea video, verificar diversidad funcional de propuestas sin cuotas obligatorias, textos on-screen definidos y stock-video concreto enlazado realmente en el Word. Si existe `PENDIENTE_STOCK_VIDEO`, registrar implementación audiovisual pendiente: no etiquetar como `LISTO_PARA_EDICION`, aunque el contenido pase. Consultar auditor `visual-stock-reviewer/scripts/audit_visual_plan.py` y revisión humana de pertinencia.

## Gate transversal de economía editorial (v1.3.3)

**Aplica sin excepción de tipo**: video, video plus, Rise, lecturas, descargables, evaluaciones y demás Word. Ejecutar `template-format-reviewer/scripts/audit_editorial_notes.py <docx> --strict`; agregar `audit_rise_editorial.py` si corresponde. Si aparece `NOTES_EXCESSIVE_ALL_RESOURCES`, `IMAGE_IN_EDITORIAL_NOTES`, `NOTES_INTERNAL_QA`, `NOTES_ACCESS_CONTINGENCY` o cualquier error universal, **no aprobar VERDE de entrega**, aunque la fuente factual esté correcta. Para video, conservar solo cues de tiempo útiles y URL clicable de stock/B-roll cuando se recomiende un clip. Mantener la separación Contenido vs Notas y archivo de QA externo conforme `shared/references/editorial-notes-all-resources.md`.


## Comp puerta factual de doble validación v1.4.1

**Bloqueo absoluto de QA integral:** faltar `qa/source-catalog.json`, `qa/course-coverage-contract.json`, `qa/R#.fidelity-ledger.json`, `qa/R#.fidelity-review.json`, el informe `source-fidelity-reviewer` en los reportes o no superar `fidelity_gate.py audit --strict`. Fallan también evidencia citada inexistente, fuente con SHA alterado, texto Word con SHA alterado, unidad sin clasificar, claim no respaldado, cita de lineamiento como fuente factual, tema obligatorio no cubierto o revisión semántica incompleta.

El agregador final exige `--project-dir --resource-id --docx` para VERDE integral y reabre material y Word. Para el curso completo exigir `audit_course_coverage.py --strict`. El archivo del revisor debe incorporar `claim_assessments` y `topic_assessments` con explicación individual, no solo estado verde. Si un documento se modifica tras Humanizador/Editor, invalidar revisión anterior, repetirla y regresar a QA. El paso automático NO garantiza entailment semántico: exigir juicio profesional independiente.
