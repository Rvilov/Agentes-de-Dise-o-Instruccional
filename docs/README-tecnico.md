# Course Agent Suite v1.5.0 - efficient instructional design

Portable 11-skill system for Claude Code and Codex. The suite generates **one editable Word per course resource**, keeps editorial notes uniform, records source evidence separately, searches stock when useful and gates final QA. It retains the original 97-slide Content QA presentation and its 27-control register.

## Install or update an existing project

From the unzipped `course-agent-suite` directory:

```sh
python install_suite.py --platform codex --project-dir "/path/to/existing-course"
# or
python install_suite.py --platform claude --project-dir "/path/to/existing-course"
```

This preserves `sources/`, `templates/`, `resources/`, `qa/`, `outputs/` and custom content outside the suite markers. It backs up old suite skills and instructions. Restart the agent session to load new skill definitions. Install the complete ZIP, not individual isolated agents, because all agents use `.course-agent-suite/shared/`.

## Start a course

Ask `course-production-orchestrator` to inspect approved sources, produce the Master Brief, Source Map and Coverage Matrix, and obtain signoff. Provide the resource list and official Word template. Then ask it to produce resources with the **v1.5.0 lean workflow**. Do not paste source documents or 97-slide indexes into every reviewer prompt.

The three reviewer stages are:

1. `learning`: pedagogical, dynamism and accessibility review, in one shared-context call.
2. `editorial`: visual/stock, template and language review, in one shared-context call.
3. `fidelity`: one independent final factual verification **after** all layout, language and course-consistency changes.

The course consistency reviewer runs once across all resource Word files after editorial and before Fidelity. A later change to a Word invalidates its final factual approval; rerun only the affected checks. QA source citations never appear in Word. See `shared/references/lean-workflow.md` and `shared/references/review-pass-contract.md`.

## Efficient commands

```sh
# Return reviewer-specific controls, not the full presentation:
python .course-agent-suite/shared/scripts/select_content_qa_controls.py --agents language-humanizer,template-format-reviewer

# Mechanical draft check: fidelity is intentionally postponed and no integral green is possible:
python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --phase draft --compact --report qa/R1.draft.json

# After editorial + consistency + final independent fidelity:
python .course-agent-suite/shared/scripts/run_quality_gates.py --resource-id R1 --docx outputs/R1.docx --phase final --compact --report qa/R1.preflight.json

# Full QA, using three shared-context reports:
python .agents/skills/final-qa/scripts/aggregate_reports.py qa/R1.pass-learning.json qa/R1.pass-editorial.json qa/R1.pass-fidelity.json --project-dir . --resource-id R1 --docx outputs/R1.docx --enforce-three-passes --compact --out qa/R1.final.json

# Course-wide factual topic coverage:
python .course-agent-suite/shared/scripts/audit_course_coverage.py --project-dir . --strict
```

For Claude Code, use `.claude/skills/final-qa/...` instead of `.agents/skills/final-qa/...`. Always run CLI commands from the course-project root. Scripts do not consume model inference tokens but **their output does**; `--compact` prints short statuses and failures while retaining detailed JSON in `qa/`.

## What must not disappear

- Client source precedence, exact factual quotations and exceptions, topic coverage and independent source fidelity (required gate).
- Verified editorial Word layout, one initial header, actual images in Content and concise notes; render every page.
- Real stock searches where appropriate and a logged selection; no fake URL or generic imagery just to fill quotas.
- Original 97-slide presentation unchanged and the 27-check index; inspect relevant slides when necessary.
- Explicit approval for remote uploads or any addition to client factual content.

## References, testing and limits

- `shared/references/lean-workflow.md`: canonical stage ordering and compute strategy.
- `shared/references/review-pass-contract.md`: schemas for the three reports and course consistency.
- `shared/references/content-qa-on-demand.md`: how to use the 27-control register efficiently.
- `shared/references/source-fidelity-evidence-policy.md`: detailed claim and source QA.
- `shared/references/editorial-stock-enforcement.md`: canonical notes, image decisions, real search logs.
- `QA_REPORT.md`: regression tests and measured static-text savings.

Optional model routing: use a less expensive model for routine language/format checks only where Codex/Claude settings support it. Do not add unsupported model flags. A faster model should not independently approve ambiguous source claims.

These changes reduce repeated instructions and invocations. **Actual API token savings** vary with the tokenizer, document size, cache behavior and the prompts used by the execution host; the suite does not promise a fixed percentage.
