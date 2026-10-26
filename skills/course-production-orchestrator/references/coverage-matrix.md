# Matriz de Cobertura

Construir una fila por tema o unidad verificable.

| Tema | Fuente ID | Ubicación | Recurso asignado | Tipo de uso | Obligatorio | Evaluable | Notas |
|---|---|---|---|---|---|---|---|
| Ejemplo | F1 | Slides 7 y 16 | R4 | Contenido | Sí | Sí | — |
| Ejemplo visual | F1 | Slides 8-15 | R4 | Referencia | No | No | No convertir detalles en evaluación |

## Tipos de uso permitidos

- **Contenido:** debe enseñarse.
- **Referencia:** puede mostrarse para contexto o reconocimiento; no convertir en aprendizaje obligatorio sin autorización.
- **Lineamiento:** gobierna cómo redactar/diseñar, no forma parte del contenido del curso.
- **Soporte:** evidencia o detalle usado para validar una afirmación.
- **Excluido:** no debe utilizarse.

## Reglas

1. Todo recurso debe tener fuentes asignadas.
2. Todo tema obligatorio debe estar asignado al menos a un recurso.
3. Evitar duplicación salvo que tenga función pedagógica clara.
4. No evaluar contenidos marcados como `Referencia`, `Lineamiento` o `No evaluable`.
5. Si una fila depende de fuentes en conflicto, marcarla como bloqueada hasta resolver.


## Contrato verificable por tema v1.4.1

Añadir ID estable `T1`, `T2` como primera columna del Markdown. Mantener `qa/course-coverage-contract.json` sincronizado (ID, fuente, `locator`, `quote` original, `required`, `usage`, `resource_ids`). Los temas de contenido obligatorio exigen evidencia por claim del Word; un listado vacío no equivale a cobertura. Una revisión humana debe comprobar que el catálogo de temas **incluye todo** lo obligatorio de los materiales, porque el script solo valida los temas registrados.
