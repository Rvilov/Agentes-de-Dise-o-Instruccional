# Contrato de reporte de revisión

Cada revisor debe producir un reporte JSON y un resumen Markdown. El JSON permite que `final-qa` automatice gates y correcciones.

## Esquema mínimo

```json
{
  "agent": "source-fidelity-reviewer",
  "resource": "R5",
  "status": "VERDE | AMARILLO | ROJO",
  "decision": "APROBADO | APROBADO_CON_AJUSTES | REGRESA_A_PRODUCCION",
  "issues": [
    {
      "id": "FID-001",
      "severity": "critical | major | minor",
      "category": "fidelidad",
      "location": "sección / párrafo / bloque",
      "finding": "hallazgo verificable",
      "evidence": "fuente, ubicación o evidencia de QA",
      "recommendation": "acción concreta",
      "auto_fixable": true,
      "proposed_fix": "cambio exacto cuando sea seguro"
    }
  ],
  "checks": [],
  "notes": []
}
```

## Semáforo

- **VERDE:** sin hallazgos que impidan entrega.
- **AMARILLO:** hay ajustes menores o mayores corregibles sin cambiar el criterio aprobado.
- **ROJO:** existe al menos un bloqueo crítico o un gate obligatorio incumplido.

## Regla de autocorrección

Marcar `auto_fixable=true` solo si la corrección es objetiva, local y verificable. Si la solución exige interpretar, crear contenido, resolver conflicto de fuentes o alterar narrativa/estrategia, usar `false`.


## Campos Content QA x DI

Al emitir el JSON añadir `content_qa_checks` para los IDs de `../../../.course-agent-suite/shared/references/content-qa-control-register.json` asignados a este agente. Cada elemento debe incluir `id`, `result` (`CUMPLE`, `INCUMPLE`, `NO_APLICA`, `PENDIENTE_CRITERIO`), `slides` y `evidence`. `NO_APLICA` siempre exige un motivo explícito. No afirmar cumplimiento íntegro si no existe el PPTX y su índice. El agente QA Final verifica los 27 controles del paquete.


## Informe independiente de fidelidad v1.4.1

Ademas del reporte habitual de issues, entregar **obligatoriamente** `qa/R#.fidelity-review.json` siguiendo `shared/templates/fidelity-review.example.json`. Debe reflejar los SHA del Word y las fuentes, `reviewed_unit_ids`, `reviewed_claim_ids`, `reviewed_topic_ids`, `claim_assessments` (uno por afirmación: `claim_id`, `verdict`, `explanation`) y `topic_assessments` (uno por tema obligatorio: `topic_id`, `covered`, `explanation`). `semantic_checks` confirma completitud, implicación semántica, condiciones, prioridad, conflictos y ausencia de hechos externos. La revisión no puede ser generada por el mismo agente productor ni quedar solo en un indicador verde genérico.

El script valida el cotejo literal de fragmentos/ubicaciones y frescura SHA, pero el Revisor debe justificar si cada cita respalda la afirmación y buscar omisiones, negaciones, salvedades y generalizaciones. Si la evidencia no basta, devolver ROJO y escalar. No redactar la evidencia en el Word.
