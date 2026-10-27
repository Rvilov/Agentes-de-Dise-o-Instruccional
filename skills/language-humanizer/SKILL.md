---
name: language-humanizer
description: 'Corrige ortografía, gramática, puntuación, consistencia de tú/usted y naturalidad de recursos e-learning en español. Usar en la pasada editorial conjunta, despues de pedagogia y ANTES de la revision final de fidelidad. Aplica primero el glosario y tono del cliente, luego la guía interna Content QA x DI empaquetada en `.course-agent-suite/shared/references/content-qa-control-register.json`, y finalmente las reglas generales del español. Humaniza patrones de IA sin cambiar hechos, requisitos legales ni significado técnico y revisa continuidad gramatical entre pantallas.'
---

# Language and humanization reviewer (shared editorial pass)

Review Spanish tone, cohesion, punctuation, spelling, natural phrasing and consistent `tu/usted` according to audience. Share the **editorial pass** with Visual and Format, not a separate full-document reload. Remove artificial ellipses, theatrical fragments, repetitive formulas and odd connectors without changing facts, qualifications, procedures or client terminology.

Apply Content QA controls filtered from `shared/references/content-qa-control-register.json`. Open a relevant PPT slide only for ambiguity. Read `shared/references/general-spanish-supplement.md` for standard punctuation not addressed by the PPT (e.g. semicolon). Preserve concise and actionable Notes; avoid creating new source material during rewriting. Finish this pass **before** Fidelity so the reviewer assesses the definitive Word. A later edit invalidates its approval.

Report targeted changes and errors only; no repeated copy of the resource in QA output. If the host supports model tiers, basic form checks can use a lighter model, but ambiguity and meaning must be escalated.
