# Gobierno de Fuentes

## Objetivo

Gestionar uno o múltiples materiales base sin mezclar, inventar ni resolver contradicciones arbitrariamente.

## Registro por fuente

Para cada fuente registrar:

- ID estable: F1, F2, F3...
- Nombre del archivo o documento.
- Tipo: PPTX, PDF, DOCX, XLSX, video, transcripción, enlace conectado, etc.
- Rol: principal, complementaria, actualización, referencia visual, lineamiento, glosario.
- Fecha o versión, si existe.
- Temas que cubre.
- Prioridad declarada.
- Restricciones: solo referencia, no evaluar, no resumir, no alterar, etc.
- Estado de acceso: local, adjunto, conectado.

## Jerarquía por defecto

Aplicar solo cuando no exista una regla específica del proyecto:

1. Actualización/instrucción explícita del cliente.
2. Documento más reciente identificado como actualización.
3. Fuente principal.
4. Fuente complementaria.
5. Referencia visual/contextual.

## Conflictos

Si dos fuentes aplicables afirman cosas incompatibles:

1. Comprobar si la Ficha Maestra define prioridad.
2. Comprobar si una fuente está marcada como actualización de otra.
3. Si sigue ambiguo, registrar `CONFLICTO ENTRE FUENTES`.
4. No elegir por conocimiento general ni por internet.
5. Bloquear únicamente el tema afectado y solicitar decisión humana.

## Trazabilidad

Toda afirmación factual sensible en un recurso debe poder rastrearse a:

`Fuente → ubicación → fragmento/tema → recurso`.

Cuando un contenido sea solo ejemplo o referencia visual, marcarlo explícitamente para impedir que aparezca como conocimiento obligatorio o como reactivo de evaluación.

## Fuentes de contenido vs. lineamientos

No todas las fuentes cumplen la misma función:

- **Fuente de contenido:** respalda hechos, procesos, definiciones, cifras, ejemplos autorizados y conocimiento evaluable.
- **Lineamiento transversal:** controla tono, redacción, diseño, QA o formato, pero **no añade hechos al curso**.

La PPT original **Content - Revisión QA x DI.pptx**, registrada en `shared/references/content-qa-policy.md`, debe clasificarse como `lineamiento` y verificarse íntegramente (97 diapositivas); `content-qa-guidelines.md` es solo un resumen. Nunca usar la guía para llenar vacíos de hechos del material base ni convertir sus ejercicios y ejemplos en contenido del curso.

## Diferencia esencial entre trazabilidad y guion

La trazabilidad es obligatoria para QA **pero no es contenido del Word entregable**. Guardar evidencia (fuente, diapositiva, minuto, prioridad) en Mapa de Fuentes, Matriz de Cobertura y `qa/R##_trazabilidad.md`. El Word de edición solo lleva la cabecera única, notas/recomendaciones editoriales y el contenido. No añadir `Fuente:`, `Material base:`, `Slides de referencia:` ni apartados de QA en el Word.


## Registro verificable obligatorio v1.4.1

Además del mapa Markdown, crear `qa/source-catalog.json` con ID, ruta a copia local verificable, rol (`principal`, `complementaria`, `guideline`), prioridad, `factual` y SHA-256 de cada fuente disponible. Si falta la fuente original, no afirmar auditoría automática. La transcripción aprobada puede ser la fuente textual de video; no asumir que el video incluye solo lo transcrito.

Crear `qa/course-coverage-contract.json` con un ID T# por tema obligatorio, fuente exacta, fragmento original y ubicación comprobable (`slide:N`, `page:N`, `paragraph:N` o `line:N`). Registrar recursos asignados. Las guías DI y stock llevan `factual:false` y **nunca prueban hechos**. Validar tema/claim en ambas direcciones y ejecutar `audit_course_coverage.py` al terminar el curso. Ver `shared/references/source-fidelity-evidence-policy.md`.
