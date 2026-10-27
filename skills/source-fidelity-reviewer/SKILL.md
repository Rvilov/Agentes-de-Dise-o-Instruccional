---
name: source-fidelity-reviewer
description: 'Verifica que un recurso instruccional sea fiel a uno o varios materiales base y a la Matriz de Cobertura. Usar al final, despues de redaccion y formato, o cuando se deba confirmar que cifras, fechas, nombres, requisitos, excepciones, secuencias y afirmaciones estén respaldados por las fuentes correctas. Detecta contradicciones, alteraciones, omisiones y uso indebido de material de referencia. Es un gate crítico: no usa internet para reemplazar al cliente ni resuelve conflictos entre fuentes por cuenta propia.'
---

# Independent source fidelity reviewer

Perform the **final high-priority semantic gate**, exactly once on the final editorial DOCX, after learning/editorial passes, language humanization, formatting, and course consistency. If the Word changes afterward, its SHA invalidates approval; repeat only this affected resource's fidelity work. No token-saving measure may weaken this gate.

Use `shared/references/source-fidelity-evidence-policy.md` and `qa/source-catalog.json`, `qa/course-coverage-contract.json`. Verify every actual content unit and factual claim against source quotations and precise locations. Check exceptions, conditions, scope, contradictory priorities and omitted required topics. Never infer missing sources or mark factual claims as nonfactual to bypass review.

Generate an independent `qa/R#.fidelity-review.json` with individual claim and topic assessments, source/Word hashes and explanations, not merely a green label. Source evidence stays outside Word. Execute `shared/scripts/fidelity_gate.py audit --strict`; it checks structure, excerpts and freshness, not semantic entailment. Escalate unsupported or ambiguous claims. Use a capable reasoning model; lightweight formatting models are not interchangeable with this review.
