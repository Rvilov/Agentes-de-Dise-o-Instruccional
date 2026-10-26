# Patrón editorial Rise: referencia aprobada del equipo (v1.3.2)

## Origen y límites

Basado en la **estructura**, NO en el contenido factual, de `M1_R2_Imagen_por_elemento.docx` (6 páginas, 8 apartados). El ejemplo es de un curso automotriz independiente; **no copiar sus contenidos, personajes, decisiones legales, términos de stock ni imágenes a cursos futuros**. La plantilla del nuevo proyecto y las decisiones expresas del equipo tienen precedencia. Esta referencia original usa orientación horizontal y repite los títulos de columna en varias páginas; **la política vigente exige A4 vertical y cabecera de metadatos única sin repetición**.

## Hallazgos específicos del ejemplo

1. **Página 1**: cabecera con tipo de recurso, título, duración, estilo/edición y objetivo; debajo comienza una tabla de dos columnas.
2. **Páginas 1-6, columna izquierda**: `Notas de Edición` mantiene título de apartado, tipo de bloque (`Rise: texto + imagen`, `Rise: acordeón de tres apartados`, `Rise: pestañas`, `Rise: proceso de tres pasos`) y una indicación corta (en 8 filas observadas, ~25-46 palabras por nota).
3. **Página 2, columna derecha**: en el acordeón de tres apartados, cada entrada tiene imagen visible junto al texto y crédito abreviado debajo de la imagen.
4. **Página 3, columna derecha**: las pestañas `Persona física` y `Persona moral` tienen imágenes distintas incrustadas junto a sus textos. La pregunta incluye imagen y retroalimentaciones en el contenido, no dentro de Notas de Edición.
5. **Páginas 4 y 5**: otros acordeones y procesos conservan sus imágenes en la columna del contenido. Las notas de edición solo describen cómo montar/resaltar.
6. **Página 6**: actividad y cierre con notas de edición resumidas; el texto final se sitúa en la columna derecha.
7. El ejemplo incluye `Slides de referencia` en la cabecera por ser una entrega histórica; **no copiar ese campo**: en la suite actual toda procedencia interna va a `qa/`.

## Contrato de tabla de Rise

| Notas de Edición (izquierda) | Contenido del Recurso (derecha) |
| --- | --- |
| **2. Reconoce la información**. `Rise: acordeón de tres apartados.` Presentar listas breves y destacar las diferencias. | **¿Qué información necesitas?** Abre cada apartado. `[Imagen 1 incrustada]` **Apartado A**: texto final. `[Imagen 2 incrustada]` **Apartado B**: texto final. `[Imagen 3 incrustada]` **Apartado C**: texto final. |
| **3. Compara dos alternativas**. `Rise: pestañas.` Dos pestañas con imágenes diferentes; destacar el cambio principal. | **Compara ambas opciones.** `[Imagen incrustada]` **Pestaña A**: texto final. `[Imagen incrustada]` **Pestaña B**: texto final. |

En el Word verdadero, los corchetes del ejemplo **se sustituyen por imágenes reales**, no quedan como marcadores ni texto literal. Debajo de cada imagen real incluir crédito y, cuando corresponda, enlace válido al asset. Toda justificación didáctica ampliada se registra exclusivamente en `qa/`.

## Contraste con el antipatrón detectado

**No permitido en Rise**: nota de 150-200 palabras con marcas `00:45–01:30`, instrucciones sobre qué hacer si falta acceso, varias soluciones hipotéticas, motivos de QA y explicaciones de por qué no colocar un botón. Esa información no es instrucción editorial. 

**Forma esperada**: `2. Prepara el documento. Rise: texto + imagen. Mostrar la captura autorizada para reconocer el documento y añadir el botón de acceso correspondiente.` (descripción visual breve). La captura, el texto final y el botón aparecen en `Contenido del Recurso`.

## Verificación

- `python skills/template-format-reviewer/scripts/audit_rise_editorial.py RECURSO.docx --strict`
- `python skills/template-format-reviewer/scripts/audit_docx_structure.py RECURSO.docx --orientation portrait --traceability qa/R##_trazabilidad.md --strict`
- Renderizar y revisar **todas las páginas**, con tamaño de imagen apropiado y sin pérdida de contenidos.

## Complemento de la norma universal v1.3.3

La concisión de Notas de Edición (20-45 palabras objetivo, 60 máximo) ahora rige **todos** los recursos. Esta referencia aporta solo detalles **específicos de Rise**: paneles, pestañas, acordeones, imágenes junto al contenido y supresión de tiempos de video no sincronizados. La norma matriz es `editorial-notes-all-resources.md`; en Rise ejecutar ambos auditores.
