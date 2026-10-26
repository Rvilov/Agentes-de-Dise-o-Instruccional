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
