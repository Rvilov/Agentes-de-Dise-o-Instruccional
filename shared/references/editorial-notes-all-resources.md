> **Actualizacion 1.4.0 (prevalente):** consultar `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Las Notas de Edicion se generan desde el contrato JSON y el QA exige prueba de busqueda real cuando corresponde. El plan visual y el log de stock son obligatorios para todos los recursos, aun si registran no-stock con motivo.

# Política universal de Notas de Edición — todos los recursos (v1.3.3)

## Alcance y prioridad

**Obligatoria para los 11 agentes** en todo Word de diseño instruccional: video con talento o voz IA, tutorial, lectura, interactivo Rise, Articulate, juego, descargable, infografía, one-pager, evaluación y cualquier otro formato. Sustituye la interpretación de v1.3.2 que limitaba el criterio de brevedad a Rise. Se aplica junto con el contrato de entrega Word, la política visual y la presentación íntegra *Content - Revisión QA x DI*. No modifica las fuentes factuales, decisiones de contenido ni la voz del cliente.

La muestra `M1_R2_Imagen_por_elemento.docx` se utiliza **solo como referencia de estructura y economía editorial**; no copiar texto, tema, personas ni imágenes de ese ejemplo a nuevos recursos.

## Contrato de dos columnas y economía editorial

- **Izquierda — Notas de Edición:** título/número de bloque o escena, formato/bloque y 1-2 instrucciones concretas de montaje que el editor puede ejecutar. Decidir y expresar una solución, no narrar el razonamiento. Objetivo habitual **20-45 palabras**; **máximo 60 por fila/bloque**. Si la complejidad exige más, **dividir en dos escenas o bloques** con sus propios contenidos; una excepción superior a 60 requiere aprobación del equipo documentada en QA externo, no en el Word.
- **Derecha — Contenido del Recurso:** narración/voz en off, diálogos, textos para participante, prompts, preguntas, opciones y retroalimentación; textos literales de pantalla cuando sea útil y **miniaturas o imágenes reales incrustadas** junto al bloque al que pertenecen, con crédito e hipervínculo auténtico cuando corresponda.
- **Prohibido en las notas:** citas a fuentes de formación, ubicación en PPT/transcripción, decisiones de QA, razonamiento interno, contingencias del tipo «si aún no tienes acceso», listas de alternativas especulativas, repeticiones del texto narrado, descripción pedagógica extensa, manual técnico o párrafos explicativos.
- **Enlaces para edición** sí pueden aparecer como hipervínculos reales donde sean operativos. Los videos stock concretos deben llevar link directo y clicable en Notas de Edición. Si no existe URL verificada, no inventarla; registrar la búsqueda y el estado pendiente **en el manifest/QA externo** y no presentar la escena como totalmente lista.
- Los datos legales o técnicos que el participante debe aprender van en la **columna de contenido**. La trazabilidad a las fuentes, controles y excepciones se guarda en `qa/`.

## Reglas según el formato, sin excepción al principio común

| Formato | Nota correcta, breve y ejecutable | Contenido / audiovisual |
| --- | --- | --- |
| **Video** | «Escena 3. Talento a cámara. Pleca: “Tres pasos”. Mostrar un diagrama de flujo cuando se enumere el proceso; animar por etapa». | Guion hablado completo y textos exactos; si se sugiere B-roll/video stock, URL real clicable en la nota. Timecodes **solo si sincronizan** locución, clip, pleca o animación; no añadir tiempos por inercia. |
| **Rise: acordeón / pestañas** | «Rise: acordeón de tres apartados. Mostrar foto distinta en cada panel y destacar el nombre de cada documento». | Texto final de los paneles e imágenes incorporadas **en esta columna**, no en Notas. Sin timecodes salvo audio/video sincronizado expresamente. |
| **Lectura** | «Texto + imagen. Insertar foto del contexto laboral al inicio y destacar la frase clave». | Texto para lectura y fotografía integrada junto al párrafo pertinente. |
| **Evaluación / juego** | «Rise: opción múltiple. Mostrar retroalimentación después de responder; no revelar la respuesta antes». | Enunciado, opciones, retroalimentaciones y apoyos visuales cuando se determinen. |
| **Descargable / infografía** | «Diseño: guía rápida. Organizar los cinco pasos en tarjetas numeradas con íconos». | Contenido textual íntegro, etiquetas e imágenes/gráficos aprobados. |

Estos ejemplos son solo de **forma**, no instrucciones obligatorias para cada recurso. Elegir stock, plecas, pop-ups, big captions, mapas mentales, pirámides, flujos e interfaces cuando aporten comprensión o ritmo, **no como cuotas visuales**. Si una escena es clara sin stock, no forzarlo.

## QA operativo y decisiones prohibidas en Word

1. Antes de producir, preparar el plan visual completo en `qa/` y separar lo decidido de lo hipotético.
2. Para cada fila, revisar si responde «¿qué hace exactamente el editor?» en menos de 60 palabras; eliminar frases de justificación o contingencia.
3. Mantener **cualquier imagen incrustada fuera de Notas de Edición**. En Rise/lectura, insertar las imágenes seleccionadas en Contenido, no sustituirlas por texto «[Imagen]».
4. Comprobar con `template-format-reviewer/scripts/audit_editorial_notes.py <docx> --strict`: longitud, ubicación de imágenes, metarrazonamiento y tiempos. Para Rise ejecutar también `audit_rise_editorial.py`.
5. Revisar el render de **todas las páginas** y comprobar fidelidad del guion, ubicación de assets, links de stock, cabecera única y legibilidad.
6. El QA Final no dará VERDE editorial si el auditor universal falla, aun cuando la forma del Word y su contenido factual sean correctos.

**No transformar una nota demasiado larga en contenido del participante sin verificar su naturaleza:** si es instrucción editorial, sintetizarla; si es texto hablado/visible, moverla al contenido; si es explicación QA o contingencia, pasarla al archivo interno. Si es irrelevante, suprimirla sin tocar los hechos aprobados.
