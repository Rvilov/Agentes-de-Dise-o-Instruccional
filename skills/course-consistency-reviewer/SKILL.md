---
name: course-consistency-reviewer
description: 'Revisa un curso completo después de producir sus recursos individuales. Usar para detectar inconsistencias entre Word de distintos R: terminología, personajes, roles, ejemplos, narrativa, títulos, tono, secuencia, datos repetidos, contradicciones internas y continuidad entre cierres/aperturas. Compara contra Ficha Maestra, Mapa de Fuentes y Matriz de Cobertura, pero no sustituye al revisor de fidelidad factual. Entrega hallazgos cruzados con ubicación en todos los recursos afectados.'
---

# Course consistency reviewer

Run **once per course** when all resources have completed the learning and editorial passes, and **before** final source fidelity. Compare terminology, names, characters, promises, examples, sequencing, openings/closings, voice and repeated factual statements across all Word files. Resolve factual contradictions against the approved source hierarchy; do not invent a reconciliation.

Write `qa/course-consistency-review.json`, listing every resource and its exact DOCX SHA-256 and your per-course judgment. Run the mechanical freshness check with `shared/scripts/verify_review_passes.py` during final QA. If any resource changes after consistency, invalidate only the affected review state and re-run checks needed for release. Keep review records out of editorial Word. Consult `references/consistency-matrix.md` only for complex cross-resource conflicts.
