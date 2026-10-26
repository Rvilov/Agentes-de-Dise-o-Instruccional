# Plantilla oficial: contrato de entrega Word

Aplicar **primero** `.course-agent-suite/shared/references/word-delivery-contract.md`.

El entregable conserva los rótulos/zonas semánticas **una sola vez al inicio**:

- Tipo de Recurso
- Duración
- Estilo/Edición
- Descripción/Objetivo
- Notas de Edición
- Contenido del Recurso

Los textos de edición y las recomendaciones visuales van en **Notas de Edición**; el guion, diálogo, preguntas y mensajes van en **Contenido del Recurso**.

La plantilla binaria `assets/resource_template.docx` es la referencia de estilos, aunque el asset heredado esté en A4 horizontal. **La regla actual del equipo exige A4 vertical para nuevas entregas.** Mantener una única cabecera en el cuerpo, desactivar encabezados de tabla repetibles (`w:tblHeader`) y no añadir `Fuente`, `Material base`, `Slides de referencia` ni evidencia QA dentro del Word.

La información de fuentes va en `qa/R##_trazabilidad.md` y el manifest fuera del entregable. Validar con `scripts/audit_docx_structure.py --orientation portrait --traceability <ruta> --strict` y revisar el render de todas las páginas.

## Dos columnas Rise (v1.3.2)

En interactivos Rise, las notas izquierda deben limitarse a título de bloque + tipo Rise + 1-2 instrucciones (objetivo 20-45 palabras, máximo 60). A la derecha van todo texto final del estudiante, opciones, retroalimentación, **imágenes reales incrustadas junto a cada panel** y créditos/enlaces de stock debajo. No imágenes en notas, timecodes arbitrarios, contingencias o metarrazonamiento. Ejecutar `scripts/audit_rise_editorial.py recurso.docx --strict` y revisar el resultado visual página por página. Fuente referencial: `shared/references/rise-editorial-reference.md` (estructura únicamente).

## Regla universal para TODOS los recursos (v1.3.3)

Además de Rise, las escenas de **video** y los apartados de **lecturas, evaluaciones y descargables** usan Notas de Edición cortas (20-45 palabras objetivo; 60 máximo por fila), sin imágenes incrustadas a la izquierda, sin razonamiento de QA ni fuentes internas. El texto final y las imágenes reales ocupan Contenido del Recurso, a la derecha. Los enlaces auténticos de video stock pueden figurar en Notas y los timecodes de video solo cuando son cues de sincronización. Ejecutar `scripts/audit_editorial_notes.py recurso.docx --strict` para **todos**, además de `audit_rise_editorial.py` para Rise, y revisar cada página renderizada.
