# Fidelidad al material base v1.4.1: control de evidencia de doble direccion

**Norma obligatoria para todo recurso y todo agente.** La informacion factual se deriva exclusivamente de las fuentes de contenido aprobadas. Los documentos de estilo, las fotos de stock, los ejemplos ajenos y el conocimiento general no sustituyen al material base. No se inventan cifras, plazos, requisitos, excepciones, nombres, procesos ni afirmaciones sobre el cliente. El nivel de adaptacion aprobado determina la forma de explicar, no concede permiso para alterar hechos. Cuando se autorice informacion externa, separarla en un registro de fuente nuevo, con aprobacion explicita.

## Tres pruebas distintas, no intercambiables

1. **Evidencia documental:** existe el archivo fuente autentico; su SHA-256 coincide con el registrado; el fragmento citado existe en la diapositiva, parrafo, pagina o linea indicada. Verificable por script.
2. **Cobertura bidireccional:** todos los parrafos del campo `Contenido del Recurso` estan inventariados y clasificados; los que contienen afirmaciones verificables tienen claims; todo tema obligatorio asignado tiene claims vinculados. Verificable estructuralmente por script, pero la deteccion semantica de afirmaciones omitidas necesita revisor.
3. **Apoyo semantico real:** la fuente *realmente sustenta* la afirmacion generada, manteniendo negaciones, condiciones, limites, actores, cifras y excepciones. El revisor de fidelidad debe comparar ambas frases; **el script no prueba por si solo la implicacion semantica**.

Un archivo sin errores tipograficos NO equivale a fidelidad. Una referencia de fuente en un JSON NO equivale a una afirmacion sustentada. Un status verde escrito por el Productor NO equivale a aprobacion de Fidelidad.

## Archivos obligatorios (internos, nunca dentro del Word)

- `qa/source-catalog.json`: fuentes F1/F2, ruta local, rol y prioridad. Conservar una copia/export verificable de cada fuente conectada antes de aprobar, sin sustituirla por un enlace sin acceso. Las guias de estilo llevan `factual: false` y no se admiten como evidencia de hechos.
- `qa/course-coverage-contract.json`: temas T1/T2... relevantes, fragmento de fuente exacto, ubicacion, estado obligatorio, recursos responsables y tipo de uso (`content`, `reference`, `guideline`, `excluded`). Alinear con `01_mapa_fuentes.md` y `02_matriz_cobertura.md`. No inventar temas para rellenar.
- `qa/R#.fidelity-ledger.json`: SHA del Word y fuentes, inventario de *todos* los parrafos de la columna derecha, clasificacion (`factual`, `mixed`, `nonfactual`), claims verificables, referencias concretas y cruce de temas obligatorios.
- `qa/R#.fidelity-review.json`: decision **independiente** de `source-fidelity-reviewer`, referida al mismo Word y hashes, lista completa de unidades/claims/temas revisados, chequeos semanticos y observaciones. No generar una aprobacion simulada para el script.
- `qa/R#.fidelity-preflight.json`: salida automatizada de `fidelity_gate.py audit`. Falta de cualquiera de los anteriores es gate rojo; el PDF, el video o la captura sin texto accesible requieren evidencia manual adicional y no pueden aprobarse como fuente auto-verificada.

## Flujo por recurso

1. Registrar y leer **todas** las fuentes del tema; decidir prioridad y resolver conflictos con el cliente, no con conocimiento general.
2. Construir los temas obligatorios en la matriz con ID estable y fragmento original verificable. Un tema sin asignacion, aunque aparezca en el material base, impide cobertura integral.
3. Redactar `outputs/R1.docx` con la plantilla. Solo contenido y notas breves de edicion, sin citas ni trazabilidad visibles.
4. Ejecutar desde la raiz del proyecto:

```bash
python .course-agent-suite/shared/scripts/fidelity_gate.py prepare \
  --project-dir . --resource-id R1 --docx outputs/R1.docx
```

5. El Productor clasifica **cada parrafo** de `qa/R1.fidelity-ledger.json`, divide en afirmaciones verificables y adjunta evidencia **literal y localizada**. Un texto pedagogico puro puede ser `nonfactual` solo con justificacion; un ejemplo que incluya un plazo o procedimiento factual no es exento. La fuente debe ser de contenido y la ubicacion concreta (`slide:5`, `paragraph:12`, `page:2`, `line:40`, `lines:40-43`). El fragmento debe ser verdadero, sin link inventado. El campo `rationale` explica por que la evidencia respalda esa afirmacion.
6. Vincular cada tema `required: true` del recurso a uno o mas claim IDs en `topic_coverage`. Usar `coverage_complete=true` solamente despues de revisar **todas** las unidades y temas, no antes.
7. El **Revisor de Fidelidad**, separado del Productor, comprueba nuevamente que el contenido preserve significado, condiciones, salvedades y prioridad de fuentes. Confirma todos los IDs en `qa/R1.fidelity-review.json` y registra los chequeos semanticos; los casos sin respaldo se marcan rojo, sin convertirlos en hechos por conveniencia.
8. Ejecutar:

```bash
python .course-agent-suite/shared/scripts/fidelity_gate.py audit \
  --project-dir . --resource-id R1 --docx outputs/R1.docx \
  --report qa/R1.fidelity-preflight.json --strict
python .course-agent-suite/shared/scripts/run_quality_gates.py \
  --project-dir . --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json
```

9. Antes de aprobar QA integral, ejecutar `final-qa/scripts/aggregate_reports.py` con reportes completos, `--project-dir`, `--resource-id` y `--docx`. Este agregador **repite** la comprobacion de hashes y evidencia; no confia solo en el JSON de preflight. En ausencia de evidencia o reporte de Fidelidad: rojo, o diagnostico parcial expresamente marcado.
10. **Despues de CADA modificacion del Word** (Productor, Humanizador, revision de evaluacion o montaje), el SHA cambia: regenerar ledger para la nueva version **conservando y revisando la trazabilidad anterior** y repetir Revisor de Fidelidad + gate. No copiar hashes nuevos sobre evidencia vieja sin revisarla. Maximo dos ciclos de correccion automatica objetiva.

## Clasificaciones y bloqueos

- `RESPALDADA`: misma afirmacion, alcance y condiciones que el material base.
- `ALTERADA`, `CONTRADICTORIA`, `NO_ENCONTRADA`, `OMISION_RELEVANTE`, `CONFLICTO`, `PENDIENTE`: **no verde**. No cambiar silenciosamente los hechos para salvar el gate.
- `ACTIVO_IMPLEMENTACION_PENDIENTE`: fuente menciona una URL/archivo/acceso pero no proporciona el enlace; marcar implementacion pendiente **fuera del Word**, no inventar URL ni declararlo un hecho inconsistente. Puede validarse fidelidad del contenido aunque no el recurso listo para publicar.
- Si un tema es solo `reference` o `guideline`, no convertirlo en requisito ni pregunta evaluable por defecto.

## Ejemplo de evidencia

La fuente F1 dice en `slide:3`: "Se requiere la aprobacion del responsable y completar la capacitacion." La unidad del Word afirma: "Solicita aprobacion de tu responsable y completa la capacitacion." Dos claims pueden ser respaldadas por ese mismo fragmento con justificacion; no agregues "activacion en 24 horas", porque esa afirmacion no esta en la fuente.

## Restricciones honestas

La extraccion de PPTX y DOCX es de texto del archivo, la de PDF necesita `pdftotext` y acceso al texto. Elementos incrustados en imagenes, interfaces o videos requieren inspeccion adicional o transcripcion aprobada. No declarar que un PDF escaneado, un video o un adjunto remoto sin bytes se verifico por este script. Tampoco se puede demostrar de forma determinista que el Productor identifico todas las afirmaciones factuales; esa completitud exige una **segunda lectura semantica independiente**. La estructura y los hashes sirven para impedir omisiones simples, citas falsas, reportes ausentes y aprobaciones de versiones distintas.
