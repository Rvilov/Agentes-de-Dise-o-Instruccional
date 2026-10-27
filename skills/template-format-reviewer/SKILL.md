---
name: template-format-reviewer
description: 'Verifica que cada recurso e-learning se entregue como documento Word usando la plantilla oficial y respetando sus campos, secciones, duración, notas de edición y contenido. Usar antes del QA final para detectar estructura rota, campos faltantes, links que no son hipervínculos reales, imágenes fuera de lugar y defectos visibles tras renderizar. Mantiene el archivo local y no lo sube a Drive. Incluye auditoría estructural y un flujo de render visual cuando las herramientas del entorno lo permiten.'
---

# Word template and format reviewer (shared editorial pass)

Share **one editorial pass** with Visual/Stock and Language; keep separate `agent` findings but use the same draft/context. Enforce the team's Word layout: A4 portrait by default, one initial header (no repeated table header), clean two-column editorial layout, brief uniform Notes left, Content and real images right. No source references or internal QA inside delivered Word.

Read `shared/references/word-delivery-contract.md` for structural problems and `shared/references/editorial-notes-all-resources.md` for note-style exceptions. Execute strict `scripts/audit_docx_structure.py`, `scripts/audit_editorial_notes.py`, and Rise-specific `scripts/audit_rise_editorial.py` when relevant. Also verify editorial JSON via `shared/scripts/editorial_contract.py audit`; render and visually inspect **all pages**. Never claim visual success from XML-only checks.

Perform layout corrections before final factual review. Use a lighter model for mechanical/linguistic checks when supported; return only findings and exact fixes.
