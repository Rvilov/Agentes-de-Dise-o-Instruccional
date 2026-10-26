---
name: accessibility-reviewer
description: 'Revisa requisitos de accesibilidad en guiones, Word y especificaciones de e-learning antes de implementación final. Usar para verificar texto alternativo de imágenes, subtítulos/transcripción de video, contraste indicado, instrucciones claras, dependencia exclusiva del color, lenguaje comprensible y alternativas para interacciones. Distingue entre revisión de diseño y conformidad técnica real: si no tiene acceso al curso implementado, no afirma cumplimiento WCAG completo.'
---

# Revisor de Accesibilidad

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Simplificar texto alternativo sin inventar detalles factuales o instrucciones inexistentes. Si cambia el contenido informativo se reabre Fidelidad.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Examinar las imagenes que efectivamente se insertaron, textos alternativos y legibilidad; una imagen de stock sugerida sin asset real no se considera implementada.


## Alcance

Revisar lo que puede verificarse en los entregables de diseño y producción. No afirmar conformidad técnica de Rise/Storyline/Genially sin probar la implementación real.

## Checklist

- Imágenes informativas con alt text o instrucción de alt text; decorativas identificadas como tales.
- Videos con subtítulos y, cuando corresponda, transcripción.
- No depender solo de color para indicar correcto/incorrecto, prioridad o estado.
- Contraste suficiente indicado para textos y gráficos; si no puede medirse, marcar para validación de implementación.
- Texto legible y lenguaje claro para la audiencia.
- Links con texto descriptivo; evitar “haz clic aquí” aislado.
- Instrucciones de interacción no dependientes solo de gesto, posición o color.
- Tablas y secuencias comprensibles en lectura lineal.
- Evitar texto esencial incrustado dentro de imágenes cuando pueda ser texto real.

Ejecutar `scripts/audit_docx_accessibility.py` como pre-chequeo de imágenes en Word. Complementar con inspección humana/visual.

Usar `references/review-contract.md`.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Entrega editorial

Poner instrucciones de accesibilidad que deba implementar el editor (texto alternativo, subtítulos, interacción) en Notas de Edición, pero el checklist/evidencia de revisión en `qa/` y nunca como apéndice dentro del Word. Seguir `.course-agent-suite/shared/references/word-delivery-contract.md`.


**Consulta contextual de Rise (v1.3.2):** Si revisas o produces un interactivo Rise, consultar `../../../.course-agent-suite/shared/references/rise-editorial-reference.md` para distinguir las instrucciones breves de edición (izquierda) del contenido e imágenes incrustadas (derecha); trazabilidad y decisiones técnicas en `qa/`. No copiar el contenido factual del documento de ejemplo.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
