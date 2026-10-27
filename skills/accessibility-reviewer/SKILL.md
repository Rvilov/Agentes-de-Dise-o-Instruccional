---
name: accessibility-reviewer
description: 'Revisa requisitos de accesibilidad en guiones, Word y especificaciones de e-learning antes de implementación final. Usar para verificar texto alternativo de imágenes, subtítulos/transcripción de video, contraste indicado, instrucciones claras, dependencia exclusiva del color, lenguaje comprensible y alternativas para interacciones. Distingue entre revisión de diseño y conformidad técnica real: si no tiene acceso al curso implementado, no afirma cumplimiento WCAG completo.'
---

# Accessibility reviewer (shared learning pass)

Review accessibility together with pedagogical and dynamism agents in **one learning pass**. Verify usable alt-text or implementation notes for meaningful images, captions/transcripts for video, adequate contrast, readable text, non-color-only states, accessible instructions and descriptive links. Do not claim tested WCAG conformance for a course that has not been implemented.

Run `scripts/audit_docx_accessibility.py` for mechanical DOCX indicators; use a lighter model for routine formal screening when the host supports model routing. Flag visual/implementation-dependent checks as pending, not green. Put short actionable editor instructions in Notes and all audit reasoning in `qa/`. Factual changes to descriptions must be completed before final fidelity.
