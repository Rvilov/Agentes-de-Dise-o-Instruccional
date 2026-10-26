# Política canónica y accesibilidad: Content - Revisión QA x DI

## Fuente única y rango de aplicación

Esta suite utiliza la **PPT original completa (97 diapositivas)** como norma interna transversal de diseño instruccional, redacción, puntuación, evaluación, sincronía visual y trato tú/usted.

- **Fuente primaria, sin abreviar:** `../source-guides/Content - Revisión QA x DI.pptx` (SHA-256 `ec8dc8025e76e2232951a099ad32e5a73890a5687ba8fbefd497c41271ddebe5`).
- **Índice fiel de 97 diapositivas:** `content-qa-full-slide-index.md` (bloques editables; preserva número de diapositiva).
- **Inventario automatizable:** `content-qa-slide-inventory.json` (texto y presencia de imágenes).
- **Registro verificable:** `content-qa-control-register.json` (27 controles con numeración exacta de la diapositiva y agentes responsables).
- **Resumen operativo:** `content-qa-guidelines.md`. **No usar el resumen como sustituto de la fuente completa.**
- **Suplemento general:** `general-spanish-supplement.md` (identificado como reglas generales del español que no proceden de la PPT).

Las ilustraciones, imágenes, memes, resultados de encuestas, juegos y actividades se conservan en el PPTX. Si es necesario interpretar una imagen o una tabla que el índice no exprese suficientemente, **abrir la PPTX**, no inferir a partir de la transcripción.

## Uso obligatorio en cada recurso

1. Antes de producir/revisar: localizar `content-qa-control-register.json` en la carpeta compartida e identificar controles asignados al agente.
2. Consultar `content-qa-full-slide-index.md` para las diapositivas originales correspondientes; abrir la fuente PPTX si hay ambigüedad o visual relevante.
3. Aplicar controles normativos pertinentes según tipo de recurso. No exigir reglas ajenas al tipo de recurso: por ejemplo, no auditar opciones múltiples si no hay evaluación.
4. En el reporte de QA registrar `{id_control, diapositiva, resultado, evidencia_del_recurso, acción}` para cada control aplicable. Resultados: `CUMPLE`, `INCUMPLE`, `NO_APLICA`, `PENDIENTE_CRITERIO`.
5. Si el PPTX original o el índice completo no está disponible, registrar `CONTENT_QA_SOURCE_INCOMPLETE` y **no declarar verificación 100% contra la PPT**. Puede continuarse con un diagnóstico parcial, sin fingir un verde integral.
6. Prioridad: fuentes del cliente gobiernan **hechos del curso**; esta guía gobierna **calidad/forma**. Si existe una contradicción con una instrucción explícita del cliente, prevalece el cliente y se documenta la excepción. No introducir información factual no sustentada.

## Diferenciar diapositivas normativas y de ejercicio

Usar las etiquetas del índice. `actividad / ejercicio`, `captura de resultados`, `portada / separador`, `agenda` y `ejemplo` no imponen por sí solos una regla de aplicación a cursos. Una diapositiva `repaso` remite a una regla ya cubierta.

## Punto y coma: precisión de procedencia

La diapositiva **26** menciona «punto y coma» en un listado asociado a puntuación y comillas. **La PPT no incluye una explicación independiente sobre cuándo utilizar punto y coma para separar oraciones o elementos complejos.** Las reglas generales de uso se consignan por separado en el suplemento de español estándar; no se les atribuirá origen en esta PPT.

## Rutas portables Codex y Claude Code

El instalador coloca la única copia canónica del PPTX y referencias en:

`.course-agent-suite/shared/source-guides/` y `.course-agent-suite/shared/references/`

Desde cualquiera de los agentes instalados en `.agents/skills/<agente>/` o `.claude/skills/<agente>/`, localizar los documentos con la ruta relativa:

`../../../.course-agent-suite/shared/references/content-qa-policy.md`

Este enfoque evita duplicar 8.6 MB en cada Skill. **Instalar la suite completa**, no solo una Skill aislada, para disponer del PPT original.
