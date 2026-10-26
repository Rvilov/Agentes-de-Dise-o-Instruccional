---
name: final-qa
description: 'Integra los reportes de todos los revisores de un recurso o curso y decide si se aprueba, se aprueba con ajustes o regresa a producción. Usar al final del flujo para aplicar gates de fidelidad, formato, pedagogía, visual/stock, lenguaje, consistencia y accesibilidad. Coordina correcciones automáticas solo cuando son objetivas y verificables, vuelve a ejecutar revisores afectados y evita ciclos infinitos. No sube entregables a Drive salvo petición explícita.'
---

# QA Final

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Exigir qa/R#.fidelity-review.json y reejecutar fidelity_gate.py audit sobre el Word y fuentes ACTUALES; aggregate_reports.py tambien reejecuta el gate. Sin evidencia, sin revisor, omisiones o fuente alterada -> ROJO. El reporte visual/editorial nunca sustituye fidelidad.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Exigir el reporte qa/R##.preflight.json con pass_machine_gates true (incluye notas canonicas y evidencia stock). Ausencia de contrato/log o incongruencia = REGRESA_A_PRODUCCION. Access_blocked y no_match = AMARILLO_IMPLEMENTACION, sin declararlo listo para edicion visual. VERDE solo tras inspeccion del editor visual, enlaces y render.


## Entradas

Reportes JSON de los revisores y los Word finales. Preferir reportes que sigan `references/review-contract.md`.

## Gates obligatorios

1. **Fidelidad:** cualquier `critical` o conflicto de fuentes no resuelto => `REGRESA_A_PRODUCCION`.
2. **Plantilla/Formato:** Word ausente, plantilla rota, orientación distinta de A4 vertical sin aprobación, cabecera repetida (`w:tblHeader` o cabecera real de Word), citas internas/fuentes dentro del entregable, trazabilidad externa ausente, hipervínculos obligatorios ausentes o render con defectos => **REGRESA_A_PRODUCCION**. Exigir `audit_docx_structure.py --strict --traceability <archivo>` **y** render de todas las páginas; nunca aprobar por solo texto/XML.
3. **Pedagógico:** objetivo/contenido/evaluación desalineados de forma crítica => regresar.
4. **Visual/Stock:** afirmar que hay una imagen/stock que no existe, URL inventada o visual ilegible crítico => regresar.
5. **Consistencia:** contradicción interna que afecta el criterio => regresar.
6. **Lenguaje/QA DI:** exigir **fuente PPT original completa + índice + registro de 27 controles** de `../../../.course-agent-suite/shared/references/content-qa-policy.md`, no solo el resumen `references/content-qa-guidelines.md`. Exigir evidencia por regla aplicable; no aprobar 100 % con reglas omitidas. La ausencia de la fuente impide afirmar QA completo aunque se pueda entregar diagnóstico parcial.
7. **Accesibilidad:** distinguir fallas corregibles de requisitos que solo pueden validarse en implementación.

## Ciclo híbrido

- Aplicar automáticamente solo issues `auto_fixable=true` con `proposed_fix` exacto y sin conflicto con otro revisor.
- Después de corregir, volver a ejecutar el revisor que emitió el hallazgo y cualquier revisor afectado.
- Máximo **2 ciclos automáticos** por recurso. Si persiste un hallazgo o surge una decisión de criterio, escalar a humano.
- No aplicar una corrección de estilo que cambie un dato validado por Fidelidad.

## Activos técnicos no suministrados

Distinguir **calidad del contenido** de **implementación final**. Si las fuentes mencionan una liga, botón o acceso, pero no suministran la URL, no bloquear el contenido ni inventar el enlace. Registrar `implementation_pending` con la instrucción de enlazar el acceso oficial cuando el cliente lo entregue. Puede existir estado VERDE de contenido con activos técnicos pendientes, siempre que el Word sea un guion de producción y no se esté declarando el recurso publicado.

## Decisión

- `APROBADO`: todos los gates verdes; menores no bloqueantes resueltos o aceptados.
- `APROBADO_CON_AJUSTES`: no hay gates críticos, pero quedan ajustes explícitos no bloqueantes.
- `REGRESA_A_PRODUCCION`: al menos un gate crítico o conflicto pendiente.

## Resultado

Ejecutar `scripts/aggregate_reports.py` para crear resumen automático y luego revisar las excepciones. Entregar resumen ejecutivo con: decisión, issues críticos, autocorrecciones realizadas, temas para decisión humana y lista de archivos finales.

Entregar los Word limpios en `outputs/` para edición y mantener reportes, manifest y trazabilidad en `qa/`, separados. Los archivos permanecen locales. No sincronizar a Drive ni otro servicio salvo instrucción explícita.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Contrato obligatorio del Word final (v1.3)

Antes de redactar, modificar, revisar o aprobar cualquier Word, leer `.course-agent-suite/shared/references/word-delivery-contract.md`. La cabecera informativa va **una vez al inicio** del cuerpo. Los recursos nuevos serán **A4 vertical** salvo instrucción explícita de orientación diferente, incluso si el asset heredado es horizontal. No repetir las filas de título o columnas al pasar de página (`w:tblHeader` desactivado); no insertar la cabecera en `w:header` de Word ni recrearla en otro bloque. Después de la cabecera entregar exclusivamente **Contenido del Recurso** y **Notas de Edición**, que incluyen recomendaciones editoriales y enlaces de stock de producción. Prohibido mostrar citas internas, nombre/ubicación del material base, IDs de fuente, matriz, evidencia de revisión o QA en el Word. Conservarlos únicamente en `qa/R##_trazabilidad.md`, manifest y reportes externos; nunca sacrificar fidelidad, solo separar su evidencia. Verificar estructura con el auditor y renderizar todas las páginas. Ante una orientación original contradictoria prevalece esta instrucción actual del equipo.

## Gate visual contextual y enlaces (v1.3.1)

Leer `.course-agent-suite/shared/references/visual-language-and-stock-policy.md`. Exigir informe de visual-stock-reviewer que inspeccione los Tabs/Accordion **por ítem** solo cuando se hayan elegido, evalúe la gramática audiovisual del video y verifique URL real clicable en Word para cada **video stock concreto** recomendado. Pedir `visual_plan` en manifest cuando existan Tabs/Accordion o escenas con apoyos. Integrar resultado del auditor `visual-stock-reviewer/scripts/audit_visual_plan.py --docx <Word> --strict`; revisar falsos negativos o casos justificables. No imponer stock universal ni cantidad mínima de plecas/pop-ups; no aceptar links falsos o gráficos decorativos. `PENDIENTE_STOCK_VIDEO` sin URL: contenido podría aprobarse, pero **no estado «listo para edición audiovisual»**. Mantener trazabilidad y QA fuera del Word.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.

## Gate obligatorio de legibilidad editorial Rise (v1.3.2)

Si el recurso es un interactivo/lectura Rise, ejecutar **también** `template-format-reviewer/scripts/audit_rise_editorial.py outputs/R##.docx --strict` y guardar el reporte en `qa/`. Si falla por notas superiores a 60 palabras, timecodes improcedentes, imágenes en la columna de notas, imagen prometida pero ausente en la columna de contenido o metarrazonamiento en notas, `REGRESA_A_PRODUCCION`. Las imágenes elegidas e incorporadas deben verse en `Contenido del Recurso` asociadas a los textos de sus paneles. La evidencia de pertinencia, alternativas descartadas y enlaces pendientes queda en QA externo; no añadir largas instrucciones técnicas al Word. En video aplicar el **mismo máximo general de 60 palabras por escena**; conservar solo tiempos con función de sincronización y vínculos reales de stock cuando corresponda. La plantilla estructural de referencia no autoriza copiar hechos ni imágenes de otro curso.
