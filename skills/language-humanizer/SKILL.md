---
name: language-humanizer
description: 'Corrige ortografía, gramática, puntuación, consistencia de tú/usted y naturalidad de recursos e-learning en español. Usar después de validar fidelidad y pedagogía. Aplica primero el glosario y tono del cliente, luego la guía interna Content QA x DI empaquetada en `references/content-qa-guidelines.md`, y finalmente las reglas generales del español. Humaniza patrones de IA sin cambiar hechos, requisitos legales ni significado técnico y revisa continuidad gramatical entre pantallas.'
---

# Corrector y Humanizador

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Despues de toda reescritura, comprobar que ni un matiz de hechos, negaciones, actores, cifras o excepciones cambio; invalidar y volver a ejecutar Fidelidad con los hashes nuevos.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Pulir el texto de contenido y la accion de las notas dentro de su estructura fija. No agregar parrafos, excusas de acceso, opciones especulativas ni razonamientos de QA a las notas.


## Jerarquía lingüística

1. Glosario, restricciones y tono del cliente.
2. Guía interna del equipo: ver `references/writing-guide-source.md`.
3. Ficha Maestra: persona lingüística, audiencia, tono y narrativa.
4. Ortografía y gramática del español estándar.

Si una regla inferior contradice una superior, respetar la superior y reportar la tensión.

## Revisar

- Ortografía, tildes, concordancia, puntuación y mayúsculas.
- Tú/usted/nosotros consistente.
- Siglas y términos del cliente sin variantes accidentales.
- Frases naturales y directas, sin rigidez de IA.
- Repetición de aperturas, cierres o muletillas.
- Evitar exceso de “imagina”, “en este recurso”, “es importante destacar”, “a continuación”, conclusiones grandilocuentes o enumeraciones artificiales cuando no aportan.
- Mantener español neutro salvo indicación del cliente.

## Humanizar sin inventar

Puede simplificar sintaxis, variar ritmo y eliminar redundancias. No puede:

- cambiar una cifra, fecha, requisito, excepción o definición;
- introducir un ejemplo factual no autorizado;
- “corregir” terminología técnica que viene del cliente sin marcarla;
- alterar una cita o texto legal por estilo.

## Guía interna obligatoria

Aplicar `references/content-qa-guidelines.md`, derivada de la presentación interna **Content - Revisión QA x DI** y empaquetada con esta skill. `references/writing-guide-source.md` conserva la procedencia y la política de actualización.

Además de ortografía y gramática, revisar expresamente:
- patrones de copy-paste IA (puntos suspensivos artificiales, exceso de puntos, falta de conectores);
- integridad gramatical entre pantallas;
- comillas/puntuación final, dos puntos y coma según la guía;
- consistencia de tú/usted y evitar tanto el “usted” burocrático como el “tú” artificial.

La guía solo se considera **verificada íntegramente** si están disponibles el PPTX original y el índice completo, además del registro de controles. El resumen `content-qa-guidelines.md` no sustituye el documento: si faltan, registrar `CONTENT_QA_SOURCE_INCOMPLETE`; no dar por cumplidos controles no revisados.

Usar `references/review-contract.md`. Las correcciones puramente ortográficas pueden ser autocorregibles; cualquier cambio semántico debe escalarse.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Word destinado al equipo de edición

No insertar citas de validación, nombres de fuentes, números de slide, timestamps del material base o rutas de archivo en el guion o en Notas de Edición; trasladar ese material a `qa/R##_trazabilidad.md`. Preservar los **datos legales o fuentes citadas como parte del propio aprendizaje**, si están en el material base. Aplicar el contrato `.course-agent-suite/shared/references/word-delivery-contract.md`.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
