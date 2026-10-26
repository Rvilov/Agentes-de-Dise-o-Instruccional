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

## Cobertura obligatoria de Content QA x DI (v1.2.0)

Los revisores que tengan controles asignados en `.course-agent-suite/shared/references/content-qa-control-register.json` deben reportar cada control pertinente con su fuente:

```json
"content_qa_checks": [
  {
    "id": "CQ-03",
    "result": "CUMPLE",
    "slides": [7],
    "evidence": "En el guion R1, no hay suspensivos enfáticos ni secuencias artificiales de puntos"
  },
  {
    "id": "CQ-04",
    "result": "NO_APLICA",
    "slides": [9],
    "evidence": "Este recurso es un video sin reactivos de opción múltiple"
  }
]
```

Valores permitidos: `CUMPLE`, `INCUMPLE`, `NO_APLICA`, `PENDIENTE_CRITERIO`. `NO_APLICA` siempre requiere motivo concreto. El agregador deduplica por ID y exige los 27 IDs, considerando únicamente los controles pertinentes; los no pertinentes se registran explícitamente como `NO_APLICA`.

El comando de QA final por defecto es estricto y **regresa rojo** si faltan controles o falta la fuente original/índice. Para un diagnóstico no integral, usar la opción `--partial-review`, cuya salida no se considera una aprobación verde final. La PPT es referencia de calidad/forma, no fuente factual.


## Evidencia de fidelidad obligatoria v1.4.1

En QA integral incluir reporte `source-fidelity-reviewer` y `qa/R#.fidelity-review.json` firmado en la etapa de revisión, con hashes vigentes y valoración individual de TODOS los claims y temas. El agregador no admite verdes genéricos sin evidencia: `aggregate_reports.py <reportes...> --project-dir <proyecto> --resource-id R1 --docx outputs/R1.docx --out qa/R1.qa-final.json`. Para proyecto completo ejecutar `audit_course_coverage.py --project-dir <proyecto> --strict`. No insertar evidencias en el DOCX del editor.
