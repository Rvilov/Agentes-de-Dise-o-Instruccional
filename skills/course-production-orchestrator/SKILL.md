---
name: course-production-orchestrator
description: 'Orquesta la construcción automatizada de cursos instruccionales una vez que la estructura y el número de recursos están definidos. Usar cuando se deba trabajar con uno o varios materiales base (PPTX, PDF, DOCX, transcripciones u otras fuentes), crear la Ficha Maestra, jerarquizar fuentes, construir la Matriz de Cobertura y preparar la producción de recursos en Word con la plantilla oficial. Mantener los entregables locales por defecto; nunca subirlos a Drive u otros servicios salvo petición explícita. Diseñado para ser portable entre Codex y Claude Code.'
---

# Course production orchestrator

Own the project brief, source hierarchy, content coverage, resource assignments, QA gates and final release. Operate exclusively from approved source materials. Start with `references/ficha-maestra.md`, `references/source-governance.md`, `references/coverage-matrix.md` only when building intake; use `references/production-workflow.md` to coordinate the production.

**Workflow:** Read `.course-agent-suite/shared/references/lean-workflow.md` once at project start. After intake, create each independent Word resource; run deterministic draft checks; coordinate three reviewer passes (learning, editorial, final fidelity). Run course consistency **once after editorial changes on all resources and before final fidelity**. Final QA verifies latest Word/source hashes, semantic review, source coverage, and Content QA controls. A change to the final Word invalidates fidelity and potentially consistency; rerun only invalidated checks.

Do not present QA as complete when a gate is missing. No unapproved web facts, invented stock URLs, or upload to external services. Keep source citations and review records in `qa/`, never in editorial Word. Respect the single-header portrait DOCX contract.

**Cost discipline:** One compact context brief per resource, reused across reviewers. Do not reload entire source packets or 97-slide index for each review. Filter the 27 Content QA controls and open a slide only for interpretation ambiguity. Prefer script summaries with failure details rather than full verbose logs. For mechanical checks run `shared/scripts/run_quality_gates.py --phase draft` before editorial, `--phase final` after fidelity. If model routing is supported, assign lightweight models to formal checks; never downgrade semantic fidelity review automatically. Read `shared/references/review-pass-contract.md` only when orchestrating reviewer output.
