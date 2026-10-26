---
name: course-consistency-reviewer
description: 'Revisa un curso completo después de producir sus recursos individuales. Usar para detectar inconsistencias entre Word de distintos R: terminología, personajes, roles, ejemplos, narrativa, títulos, tono, secuencia, datos repetidos, contradicciones internas y continuidad entre cierres/aperturas. Compara contra Ficha Maestra, Mapa de Fuentes y Matriz de Cobertura, pero no sustituye al revisor de fidelidad factual. Entrega hallazgos cruzados con ubicación en todos los recursos afectados.'
---

# Revisor de Consistencia del Curso

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Comparar hechos entre recursos contra la misma fuente prioritaria; conflictos de nomenclatura o requisitos no se resuelven inventando. Reabrir Fidelidad tras cambios.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Comprobar que formato de Notas de Edicion, titulos, etiquetas, longitud y ubicacion de stock son identicos en todos los recursos del curso y que se usa contrato por recurso.


## Revisar el conjunto, no recursos aislados

1. **Terminología:** mismo concepto, misma forma aprobada.
2. **Personajes:** nombres, roles, relación, personalidad funcional y conocimientos coherentes.
3. **Narrativa:** cronología y continuidad; un recurso no debe contradecir lo ocurrido en otro.
4. **Tono/persona:** no alternar tú/usted o niveles de formalidad sin razón. Aplicar los criterios de audiencia/objetivo/voz de `references/content-qa-guidelines.md` y evitar tuteo artificial o “usted” burocrático.
5. **Progresión:** evitar explicar desde cero un concepto que ya se consolidó, salvo repaso deliberado.
6. **Duplicación:** detectar contenido repetido sin función pedagógica.
7. **Ejemplos:** no cambiar datos de un mismo caso entre recursos.
8. **Títulos y nombres:** nombres de herramientas, áreas, marcas y formatos idénticos a los aprobados.
9. **Transiciones:** cierres y aperturas deben conectar con el recurso correcto.
10. **Integridad entre pantallas/recursos:** revisar que los cortes no dejen fragmentos gramaticales huérfanos y que la secuencia sea fluida.
11. **Evaluación:** usar terminología y reglas enseñadas durante el curso.

## Prioridad

Si la inconsistencia es factual, remitir al `source-fidelity-reviewer`. Si es de estilo, coordinar con `language-humanizer`. No elegir una variante por preferencia personal cuando la Ficha Maestra o el cliente ya la definen.

Usar `references/review-contract.md`.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Separación editorial / QA

En Word solo se permite la cabecera inicial, Notas de Edición y Contenido del Recurso. No repetir cabeceras ni incorporar referencias internas a fuentes. Comparar consistencia entre recursos utilizando el Mapa de Fuentes, la trazabilidad y los reportes guardados **fuera** del Word. Consultar `.course-agent-suite/shared/references/word-delivery-contract.md`.


**Consulta contextual de Rise (v1.3.2):** Si revisas o produces un interactivo Rise, consultar `../../../.course-agent-suite/shared/references/rise-editorial-reference.md` para distinguir las instrucciones breves de edición (izquierda) del contenido e imágenes incrustadas (derecha); trazabilidad y decisiones técnicas en `qa/`. No copiar el contenido factual del documento de ejemplo.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
