---
name: course-production-orchestrator
description: 'Orquesta la construcción automatizada de cursos instruccionales una vez que la estructura y el número de recursos están definidos. Usar cuando se deba trabajar con uno o varios materiales base (PPTX, PDF, DOCX, transcripciones u otras fuentes), crear la Ficha Maestra, jerarquizar fuentes, construir la Matriz de Cobertura y preparar la producción de recursos en Word con la plantilla oficial. Mantener los entregables locales por defecto; nunca subirlos a Drive u otros servicios salvo petición explícita. Diseñado para ser portable entre Codex y Claude Code.'
---

# Orquestador de Producción de Cursos

## Gate de evidencia factual v1.4.1 (OBLIGATORIO)

Leer `.course-agent-suite/shared/references/source-fidelity-evidence-policy.md`. Cada afirmacion factual debe tener ubicacion y fragmento literal de un material base aprobado en `qa/R#.fidelity-ledger.json`; cada tema obligatorio debe estar cubierto. El Word editorial NO incluye citas. El revisor de Fidelidad hace una segunda lectura semantica independiente y documenta cada afirmacion en `qa/R#.fidelity-review.json`. El QA Final revalida hashes del Word y las fuentes y BLOQUEA entrega integral sin evidencia/revision, incluso si los demas agentes dan verde. Despues de cualquier cambio factual o estilístico al Word, rehacer la comprobacion de Fidelidad; no maquillar los JSON ni inventar citas para superar el gate.

**Responsabilidad especifica:** Establecer un inventario de fuentes de contenido y una matriz de temas obligatorios con IDs y extractos comprobables. No iniciar produccion si faltan registros de fuente o temas. Al final ejecutar la auditoria integral del curso.


## Contrato editorial + stock verificable v1.4.0 (OBLIGATORIO)

**Leer `.course-agent-suite/shared/references/editorial-stock-enforcement.md` antes de trabajar con cualquier recurso.** Cada Word debe proceder de `qa/R##.editorial-contract.json`: una estructura fija de tres lineas para las Notas de Edicion (titulo numerado, etiqueta por formato, instruccion accionable), nunca notas libres diferentes entre cursos. Construir el Word con `shared/scripts/editorial_contract.py apply` y comprobarlo con `audit --strict`. Mantener imagenes reales en Contenido del Recurso, enlaces de stock-video reales en Notas, todo lo interno en `qa/`. Antes de terminar, exigir `qa/R##.stock-search-log.json` con la busqueda ejecutada donde se haya seleccionado stock (proveedor, consulta, ID de resultado, candidatos y URL seleccionada); `PENDIENTE_STOCK` sin intento de busqueda ya no es valido. Si el proveedor no esta conectado, registrar acceso bloqueado y no dar el recurso como listo para edicion. No imponer stock en cada recurso: justificar cuando conviene otro visual. Ejecutar `python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --report qa/R1.preflight.json`; no declarar QA integral verde con gate fallido. Registrar revision humana de pertinencia/licencia/URL y render de todas las paginas. Esta regla v1.4.0 prevalece sobre pautas anteriores cuando sean mas laxas.

**Responsabilidad de este agente:** Exigir contrato editorial y log antes de delegar; programar etapa real de busqueda visual antes de generar DOCX. Solicitar doble validacion Productor y Revisor Visual cuando todo un recurso prescinde de stock. No aprobar faltantes con una etiqueta generica.


## Propósito

Convertir un brief aprobado y uno o varios materiales base en un proyecto de producción controlado, trazable y listo para generar recursos instruccionales en `.docx` con la plantilla oficial incluida en `assets/resource_template.docx`.

## Reglas no negociables

1. Tratar el material base como un **corpus de una o más fuentes**, no como un único archivo.
2. Considerar las fuentes del cliente como verdad operativa. No completar vacíos con conocimiento general o internet salvo solicitud explícita.
3. No iniciar producción si faltan: objetivo, audiencia, fuentes, jerarquía o regla de conflicto, tono, narrativa, plataforma, estructura/número de recursos y nivel de libertad de adaptación.
4. Generar **cada recurso como un archivo Word independiente** usando la plantilla oficial del equipo.
5. Mantener todos los archivos localmente por defecto. **No subir a Google Drive, OneDrive, Dropbox ni otros servicios** salvo instrucción explícita del usuario.
6. Leer desde Drive solo cuando el usuario proporcione una fuente o autorice el acceso. Leer una fuente remota nunca implica permiso para escribir o subir archivos.
7. Separar errores objetivos de decisiones de criterio:
   - Corregir automáticamente errores objetivos y verificables.
   - Escalar decisiones pedagógicas, narrativas o ambiguas a revisión humana.
8. Si dos fuentes se contradicen y no existe una prioridad declarada, marcar **CONFLICTO ENTRE FUENTES** y detener la producción del contenido afectado.
9. Conservar trazabilidad **fuera de los Word entregables**: todo contenido obligatorio debe vincularse a una fuente y ubicación en `qa/R##_trazabilidad.md`, el Mapa de Fuentes y la Matriz de Cobertura.
10. Aplicar la guía transversal `references/content-qa-guidelines.md` como norma de forma/QA. No tratarla como fuente factual del curso ni como contenido evaluable.

## Flujo obligatorio

1. **Preparar proyecto**
   - Si no existe la estructura de trabajo, ejecutar `scripts/init_course_project.py`.
   - Copiar la plantilla oficial al proyecto; no modificar el asset original.

2. **Construir Ficha Maestra**
   - Seguir `references/ficha-maestra.md`.
   - Definir objetivo, audiencia, contexto de uso, tono, persona lingüística, narrativa, personajes, rol del participante, plataforma, duración, tipos de recursos, evaluación, lineamientos visuales, reglas de redacción y política de correcciones.

3. **Construir Mapa de Fuentes**
   - Seguir `references/source-governance.md`.
   - Registrar todas las fuentes, su función, alcance, prioridad, fecha/versión si existe y restricciones de uso.
   - Separar **fuentes de contenido** de **lineamientos transversales**. La guía Content QA x DI se registra como `lineamiento`, nunca como fuente factual.
   - Detectar contradicciones antes de producir.

4. **Construir Matriz de Cobertura**
   - Seguir `references/coverage-matrix.md`.
   - Mapear tema → fuente → ubicación → recurso → tipo de uso.
   - Distinguir: contenido obligatorio, ejemplo/referencia, lineamiento y contenido no evaluable.

5. **Validar preparación**
   - Ejecutar `scripts/validate_course_intake.py <carpeta-proyecto>`.
   - Si devuelve errores críticos, detenerse y resolverlos antes de producir.

6. **Preparar producción**
   - Entregar a cada recurso solo las fuentes y fragmentos que le corresponden según la Matriz de Cobertura.
   - Usar la Ficha Maestra como contrato común para tono, narrativa, personajes, plataforma y límites.
   - Usar `references/production-workflow.md` como contrato de integración con productores y revisores.

7. **Salida**
   - Guardar cada recurso en `outputs/` como `.docx` independiente **limpio de fuentes/citas internas**. Guardar manifest, trazabilidad y QA en `qa/`.
   - No exportar ni sincronizar archivos fuera del entorno local sin instrucción explícita.

## Jerarquía de fuentes

Aplicar en este orden cuando esté declarado:

1. Instrucción o actualización explícita del cliente.
2. Documento identificado como actualización posterior.
3. Fuente principal.
4. Fuente complementaria.
5. Referencia visual o contextual.

Si el proyecto define otra jerarquía, usar la del proyecto. Si no hay forma segura de resolver una contradicción, escalarla.

## Nivel de libertad de adaptación

Registrar un nivel en la Ficha Maestra:

- **0 Literal:** conservar contenido prácticamente textual.
- **1 Sintetizar:** reducir sin cambiar significado.
- **2 Reorganizar:** cambiar orden para mejorar aprendizaje.
- **3 Contextualizar:** crear casos/ejemplos derivados sin añadir hechos externos.
- **4 Enriquecer:** se permite información externa, pero debe diferenciarse de la fuente.

Nunca asumir un nivel superior al aprobado.

## Word y plantilla

- Asset oficial: `assets/resource_template.docx`.
- Mantener estructura y estilos de la plantilla, pero **salida A4 vertical** de acuerdo con la especificación actual del equipo (el asset histórico suministrado está en horizontal). La cabecera solo aparece una vez al principio; no utilizar `tblHeader` de Word ni recrear portada o bloque de metadatos por página.
- Crear un archivo por recurso. El Word solo incluye cabecera única, contenido instruccional, notas y recomendaciones editoriales. La evidencia y las fuentes van en `qa/`.
- Los revisores posteriores deberán validar estructura, render visual e hipervínculos reales.
- Las referencias a stock deben convertirse en hipervínculos clicables cuando el entregable lo requiera.

## Portabilidad

Esta skill debe poder copiarse sin cambios de lógica a:

- Codex: `.agents/skills/course-production-orchestrator/`
- Claude Code: `.claude/skills/course-production-orchestrator/`

Usar `scripts/install.py` para instalación local en un proyecto. Ver `references/platform-installation.md`.

## Recursos incluidos

- `references/ficha-maestra.md`: contrato inicial del curso.
- `references/content-qa-guidelines.md`: reglas transversales de QA/DI para forma, lenguaje, evaluaciones y sincronía visual.
- `references/source-governance.md`: inventario, jerarquía y conflictos de fuentes.
- `references/coverage-matrix.md`: trazabilidad tema-fuente-recurso.
- `references/production-workflow.md`: flujo y gates de producción.
- `references/platform-installation.md`: instalación en Codex y Claude Code.
- `scripts/init_course_project.py`: crea el scaffold de un curso.
- `scripts/validate_course_intake.py`: valida que el intake esté listo para producción.
- `scripts/install.py`: instala esta skill en un proyecto Codex o Claude Code.
- `assets/resource_template.docx`: plantilla Word oficial.

## Suite de agentes

Consultar `references/suite-integration.md` para invocar productores y revisores. Todos los revisores deben seguir `references/review-contract.md`. El flujo usa máximo dos ciclos automáticos de corrección por recurso.

## Integración obligatoria de la PPT completa Content QA x DI

La copia canónica completa de 97 diapositivas y su registro por reglas están en la carpeta compartida del proyecto instalado: `../../../.course-agent-suite/shared/references/content-qa-policy.md` y `../../../.course-agent-suite/shared/source-guides/Content - Revisión QA x DI.pptx`. Leer la política, filtrar los controles del propio agente en `content-qa-control-register.json`, consultar las diapositivas respectivas en `content-qa-full-slide-index.md` y comprobar en PPTX las imágenes o ambigüedades. La antigua `references/content-qa-guidelines.md` es **solo resumen**, nunca prueba de revisión completa. Registrar resultado por control aplicable con ID, diapositiva y evidencia. Si falta fuente íntegra o índice, reportar `CONTENT_QA_SOURCE_INCOMPLETE` y no afirmar que se auditó el 100 % de la PPT. Mantener ejemplos/actividades separados de reglas; la PPT no es fuente factual del curso.

## Contrato obligatorio del Word final (v1.3)

Antes de redactar, modificar, revisar o aprobar cualquier Word, leer `.course-agent-suite/shared/references/word-delivery-contract.md`. La cabecera informativa va **una vez al inicio** del cuerpo. Los recursos nuevos serán **A4 vertical** salvo instrucción explícita de orientación diferente, incluso si el asset heredado es horizontal. No repetir las filas de título o columnas al pasar de página (`w:tblHeader` desactivado); no insertar la cabecera en `w:header` de Word ni recrearla en otro bloque. Después de la cabecera entregar exclusivamente **Contenido del Recurso** y **Notas de Edición**, que incluyen recomendaciones editoriales y enlaces de stock de producción. Prohibido mostrar citas internas, nombre/ubicación del material base, IDs de fuente, matriz, evidencia de revisión o QA en el Word. Conservarlos únicamente en `qa/R##_trazabilidad.md`, manifest y reportes externos; nunca sacrificar fidelidad, solo separar su evidencia. Verificar estructura con el auditor y renderizar todas las páginas. Ante una orientación original contradictoria prevalece esta instrucción actual del equipo.

## Selección y QA del lenguaje visual (v1.3.1)

Añadir en Ficha Maestra una decisión por tipo de recurso y plataforma sobre apoyos visuales permitidos/prohibidos. Consultar `.course-agent-suite/shared/references/visual-language-and-stock-policy.md`; delegar a Producción, Revisor de Dinamismo y Revisor Visual el criterio contextual: imágenes por panel cuando se eligen Tabs/Accordion, excepto alternativa justificada; videos con plecas, pop ups, captions, stock-video enlazado, mapas mentales, pirámides u otros esquemas solo si aportan. No obligar visuales idénticos en todos los recursos. Requerir manifest `visual_plan` y revisión de URLs antes de aprobar recursos para edición. Registrar pendientes fuera del Word excepto la instrucción editorial accionable.

## Política universal de notas editoriales (v1.3.3)

**Para TODO recurso**, leer `.course-agent-suite/shared/references/editorial-notes-all-resources.md` antes de producir o revisar. **Notas de Edición** (izquierda): título/escena + bloque/formato y 1-2 acciones de montaje (objetivo 20-45 palabras; máximo 60 por fila/escena, salvo excepción autorizada documentada en QA externo). **Contenido del Recurso** (derecha): narración, diálogos, textos, reactivos y apoyos visuales reales vinculados a su bloque. No incrustar fotos/capturas en Notas ni convertirlas en manual de producción, reflexión pedagógica, contingencia técnica, lista de alternativas o reporte de QA. Mantener trazabilidad y plan detallado exclusivamente en `qa/`. Para video, sí permitir timecodes que sincronizan voz/animación y **links auténticos clicables de clips stock** en Notas. Para Rise no incluir tiempos de video salvo sincronización aprobada. Aplicar el **auditor universal** `template-format-reviewer/scripts/audit_editorial_notes.py <Word> --strict` a videos, Rise, lecturas, evaluaciones, descargables y demás recursos; en Rise ejecutar además `audit_rise_editorial.py`. Revisar visualmente todas las páginas; cualquier gate rojo impide VERDE editorial.
