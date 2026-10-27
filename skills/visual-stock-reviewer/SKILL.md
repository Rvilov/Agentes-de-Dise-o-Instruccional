---
name: visual-stock-reviewer
description: 'Revisa la calidad visual y el uso real de stock en recursos instruccionales Word, Rise y video. Usar para confirmar que imágenes y gráficos representen el contenido, que haya una mezcla adecuada entre stock, diagramas e interacción, que no se usen capturas de slides textuales como recurso visual, que los gráficos sean legibles y que las referencias de stock tengan enlaces reales y clicables. Cuando el proyecto usa Magnific, valida la política no-AI y no inventa assets ni URLs.'
---

# Visual and stock reviewer (shared editorial pass)

Share **one editorial pass** with template-format and language reviewers using a common resource brief. Independently check visual meaning, image quality, missing images, links, availability/licensing, stock-search evidence and relevance. No arbitrary stock quota; justify substitutes (diagram, icon, UI, talent or none). A selected stock item must come from a real search and its proper URL/asset evidence, not a search-result placeholder.

Use `shared/references/editorial-stock-enforcement.md` when decisions include stock and `shared/references/visual-language-and-stock-policy.md` for Rise tabs/accordions and audiovisual grammar (plecas, pop-ups, B-roll, pyramids, timelines, mental maps). Run `scripts/audit_docx_assets.py` and `scripts/audit_visual_plan.py` where applicable; deterministic counts do not replace viewing rendered pages. Stock images belong in Content; a concrete suggested stock video requires a clickable URL in Notes. Report blocked access as pending implementation.

Return your own concise `agent` assessment within the editorial group. Finish edits before final fidelity.
