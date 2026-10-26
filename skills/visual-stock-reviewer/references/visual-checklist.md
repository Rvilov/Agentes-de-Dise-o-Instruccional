> **Actualizacion 1.4.0 (prevalente):** consultar `.course-agent-suite/shared/references/editorial-stock-enforcement.md`. Las Notas de Edicion se generan desde el contrato JSON y el QA exige prueba de busqueda real cuando corresponde. El plan visual y el log de stock son obligatorios para todos los recursos, aun si registran no-stock con motivo.

# Checklist visual

- ¿El Word contiene las imágenes que afirma contener?
- ¿Cada stock referenciado tiene enlace real?
- ¿El link abre el asset correcto?
- ¿Las lecturas mezclan stock, gráficos e interacción?
- ¿Hay capturas de material base con puro texto? Si sí, rediseñar.
- ¿Los gráficos caben completos y son legibles al 100%?
- ¿Hay textos sin acentos o errores dentro de una imagen?
- ¿La imagen corresponde a la audiencia y contexto?
- ¿No se atribuye stock/IA sin evidencia?
- ¿El visual refuerza exactamente el concepto, acción o resultado del bloque en vez de ser stock genérico?
- ¿En video, el B-roll/stock aparece en el momento narrativo correcto?

## Checklist contextual v1.3.1

- Si hay **Tabs o Accordion**: ¿cada panel tiene propuesta visual distinta y pertinente o razón interna explícita para una alternativa sin foto? ¿el plan detallado está en `qa/` y las Notas de Edición son breves? ¿las imágenes elegidas están incrustadas **junto al texto de su panel en Contenido del Recurso**?
- Si hay otras interacciones: ¿se eligió visual por propósito y no por requisito de stock general?
- En video: ¿se evaluaron plecas/lower thirds, pop ups, big captions, stock-video, imágenes, pantallas y gráficos según el mensaje, sin obligarlos todos?
- En pleca/pop-up/caption: ¿se escribió el texto exacto en pantalla y el momento narrativo de entrada?
- En diagrama/mapa mental/pirámide/flujo: ¿es correcta la relación conceptual y están especificados etiquetas, secuencia y animación sugerida?
- En stock-video concreto: ¿está el URL real **clicable** dentro del Word y corresponde a ese clip, o se marcó explícitamente `PENDIENTE_STOCK_VIDEO` más términos de búsqueda? ¿evitó stock genérico por cumplir?
- ¿El `visual_plan` pasa `audit_visual_plan.py` y el Word final conserva solo notas editoriales, sin citar fuentes internas?
