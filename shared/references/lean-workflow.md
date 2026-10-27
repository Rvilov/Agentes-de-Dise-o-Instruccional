# Optimized production and QA workflow

## Intent
Minimize duplicated context **without** weakening factual fidelity, Word editorial quality, stock searches, or source coverage. This policy is canonical for all 11 skills. Do not copy it into each SKILL.md or CLAUDE.md/AGENTS.md.

## Project initialization (once)
1. Intake all approved sources: `qa/source-catalog.json`, source precedence, Ficha Maestra and `qa/course-coverage-contract.json`. An unregistered file in `sources/` must block integral approval.
2. Cache a **compact resource brief** (objective, audience, content scope, factual source IDs/locators, decisions, visual requirements) as a small local file. Keep the full sources available for targeted reads, not reprinting them in each reviewer prompt. Never discard exceptions, numeric conditions or contradictory sources.
3. Content QA: read `shared/references/content-qa-control-register.json` (27 controls) and use `shared/scripts/select_content_qa_controls.py` to select the IDs for the intended reviewers. The 97-slide index and PPTX remain installed; open **only relevant slides if a check is unclear**. Machine integrity is validated from a file hash, not copied into model prompts.

## Resource stages (three shared review passes)
1. **Produce** `outputs/R#.docx` and QA/stock/editorial manifests. Run `shared/scripts/run_quality_gates.py --phase draft` for mechanical checks; this is a draft status, never integral-green.
2. **Learning pass**: one context load and one grouped call for `pedagogical-reviewer`, `dynamism-reviewer`, `accessibility-reviewer`; keep individual findings tagged inside `qa/R#.pass-learning.json`. Apply any editorial or instructional corrections.
3. **Editorial pass**: one context load for `visual-stock-reviewer`, `template-format-reviewer`, `language-humanizer`; keep individual findings in `qa/R#.pass-editorial.json`. Confirm real stock searches when selected, usable assets, links, Notes and visual render. Apply corrections. Stop changing this Word once completed.
4. **Consistency once per course**: after **all** resources have passed the two stages above and before final fidelity, compare the complete course, write `qa/course-consistency-review.json` with SHA-256 per Word. If a later edit invalidates a hash, re-evaluate only what changed; do not suppress inconsistency.
5. **Final Fidelity pass**: after editorial and consistency, create/update `qa/R#.fidelity-ledger.json`; independent `source-fidelity-reviewer` makes claim-by-claim semantic decisions and writes `qa/R#.fidelity-review.json` plus `qa/R#.pass-fidelity.json`. Run `fidelity_gate.py audit --strict`. This pass normally runs **once per final Word**. Any later Word change invalidates its source evidence and requires renewed review of that changed Word.
6. **Final QA**: run `run_quality_gates.py --phase final`, `final-qa/scripts/aggregate_reports.py --enforce-three-passes`, and `audit_course_coverage.py --strict`. Red gates block delivery; no self-declared pass. Keep reports, evidence, full stock details and traces outside Word.

## Compute vs semantic work
- **Scripts, no model context**: file existence, orientations, repeated headers, widths, image/link counts, URL presence, note format/length, hashes, claim/source quote location, stock log status, 27-control completeness and QA report schema.
- **Reviewers, brief shared context**: semantics of claims vs sources, relevance of stock, pedagogical effectiveness, accessibility of intended experience, suitability of tone, course-wide consistency and visual suitability.
- **Model routing if supported**: use a lightweight tier for repeatable editorial/formal reviews with short structured output; use a capable tier for source fidelity and unresolved instructional ambiguities. Never write unsupported routing flags or assume identical capabilities across Codex and Claude Code.

## Safety and release
One-resource/one-Word, A4 portrait and header only on first page; Notes left limited to clear production instructions, content/images right. Source citations only in QA. Search stock only where needed but actually execute those searches and retain candidate/selection evidence. A missing provider does not mean 'no stock needed'. No remote upload unless explicitly requested. Two automatic objective fix cycles max; subjective decisions return to the user. Render and inspect every page before final release.
