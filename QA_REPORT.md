# QA de Course Agent Suite v1.4.1

## Resultado

**VALIDADA PARA INSTALACION Y PRUEBAS DE CURSO** en Codex y Claude Code. Se agrego una compuerta de fidelidad factual que impide verde integral sin evidencia verificable y revision semantica independiente. **No se ha probado todavia esta nueva version contra un curso completo real de usuario.**

## Guardarrailes nuevos (material base)

- `fidelity_gate.py prepare`: enumera TODAS las unidades de texto de la columna `Contenido del Recurso` en el Word real. Inicializa estatus `PENDIENTE` (no se autopresume respaldo).
- `fidelity_gate.py audit --strict`: coteja hashes de Word/fuentes; archivos reales en `sources/` versus catalogo; citas exactas con ubicaciones DOCX/PPTX/PDF/TXT; afirmaciones con fuente factual (no guia DI o stock); links unidad-claim; temas obligatorios-claims y su justificacion; y exige valoracion independiente por cada afirmacion/tema.
- `audit_course_coverage.py --strict`: comprueba todos los recursos declarados y la cobertura de todos los temas **registrados** como obligatorios en el contrato del curso.
- `run_quality_gates.py`: anade `factual_fidelity` a los gates existentes. El preflight falla ante ledger/revision incompleta o Word/fuente desactualizada.
- `aggregate_reports.py`: reejecuta la comprobacion sobre el Word/fuente actual, exige reporte JSON de `source-fidelity-reviewer` en el conjunto de informes y bloquea QA integral si falta evidencia. Estado ROJO devuelve codigo de salida distinto de cero.
- Orquestador y Productor ahora crean o requieren los registros `qa/source-catalog.json`, `qa/course-coverage-contract.json`, `qa/course-resource-index.json`, `qa/R#.fidelity-ledger.json`, `qa/R#.fidelity-review.json`. Se mantienen **fuera de los Word editoriales**.
- Toda edicion posterior de un Word cambia su SHA-256 y anula la revision anterior, incluso si solo fue una reescritura estilistica.

## Pruebas realmente ejecutadas

- **37/37 unitarias** APROBADAS: 13 de v1.4.0 para notas/stock y 24 nuevas para fidelidad (claim sin fuente, cita inventada, cita en ubicacion incorrecta, fuente alterada, Word alterado, tema omitido, revision generica verde, reporte ausente, archivo no registrado, fuente-guia usada como hecho, compatibilidad de locator TXT/DOCX/PPTX, auditoria de curso, intake incompleto y bloqueo de QA Final).
- **2/2 instalaciones y actualizaciones** sobre proyectos ya existentes: Codex y Claude Code, ejecutadas dos veces por entorno. Conservan `sources`, `qa`, `resources`, `outputs` e instrucciones fuera del bloque administrado; backup generado.
- **6/6 gates de preentrega** APROBADOS en cada entorno con un recurso/fuente **sintetico**: `notes_canonical`, `stock_execution`, `factual_fidelity`, `editorial_length`, `document_structure`, `visual_plan`.
- **2/2 gates de cobertura de curso** APROBADOS con matriz de temas sintetica en ambos entornos.
- **11/11 skills** validadas mediante `quick_validate.py`.
- **97/97 diapositivas** de la PPT normativa Content QA x DI indexadas, **27 controles** e integridad SHA-256 `ec8dc8025e76e2232951a099ad32e5a73890a5687ba8fbefd497c41271ddebe5` verificados.
- **Word de prueba** renderizado a PNG y revisado visualmente: una pagina A4 vertical, cabecera unica y columnas sin desbordes. No se entrega como recurso del usuario.
- Scripts Python compilados sin errores.

## Limitaciones importantes

1. Los tests utilizan material fuente **sintetico**; NO acreditan que los recursos actuales de Nestle, Grupo FAME u otro cliente esten aprobados.
2. Las comprobaciones literales y SHA-256 acreditan **existencia de fragmentos e integridad de version**, pero NO demuestran por si solas que un fragmento respalde semanticamente cada claim. Esa comprobacion requiere una segunda lectura por `source-fidelity-reviewer`, registrada de forma individual.
3. El script no descubre automaticamente TODO el conocimiento obligatorio en una fuente. Un agente/humano debe construir la matriz de temas completa y comprobar omisiones contra las fuentes; la auditoria verifica **todos los temas registrados** y detecta fuentes documentales no registradas.
4. PDF escaneado, texto en imagen, contenido audiovisual sin transcripcion y formatos de fuente no compatibles no se pueden considerar verificaciones automáticas; registrar necesidad de inspeccion manual o version textual aprobada. No usar OCR ni conocimiento general como sustituto silencioso.
5. Citas y reportes externos pueden escribirse incorrectamente por un agente; esta suite impide muchos errores verificables y exige juicio independiente, pero no garantiza que un modelo nunca produzca una falsedad.
6. Los Word existentes NO se actualizan automaticamente al instalar. Requieren migracion a los sidecars de evidencia, una revision independiente y nuevos QA gates.
7. Validacion de stock real y licencias depende de los conectores/proveedores disponibles; las pruebas de stock anteriores son simuladas.

## Entrega

Un Word editorial por recurso, **sin** citas, IDs ni fuentes en notas o contenido. Los detalles de trazabilidad y revision permanecen en `qa/`. Se conserva la regla de no subir recursos del cliente a servicios externos salvo peticion expresa; el ZIP de la herramienta se subira al Drive autorizado por el usuario.
