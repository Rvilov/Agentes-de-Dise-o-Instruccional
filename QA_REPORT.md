# QA Report - Course Agent Suite v1.5.0

## Result

**PASS (synthetic technical validation).** Eleven skills pass `quick_validate.py`; 48 Python regression tests pass (37 prior + 11 new). The full source Content QA guide still contains 97 pages/slides; its 27 control register, inventory SHA and the original PPTX are mutually consistent. Both full and fast source-integrity checks passed.

## Measured instruction footprint

Scope: literal text of the **eleven SKILL.md files plus the one global project instruction fragment**, comparing official v1.4.1 ZIP against v1.5.0 source. It **excludes** referenced source material, retrieved course content, model responses, OCR, cache behavior, API overhead and dynamic prompts.

| Measure | v1.4.1 | v1.5.0 | Reduction |
|---|---:|---:|---:|
| UTF-8 bytes of fixed skill/global text | 115,568 | 20,400 | **82.35%** |
| Whitespace-delimited words | 14,840 | 2,614 | **82.39%** |
| Planned reviewer invocations per resource | 7 | 3 | **57.14%** |
| Content QA indexes loaded by default into model context | 97-slide index | 27-control register | On-demand |

This is an actual **static-text** measurement, not measured billable tokens. Invocation savings are a workflow projection assuming the host executes each group as one shared-context review. They may differ in Claude Code and Codex. Reproduce the first two rows using `shared/scripts/benchmark_instruction_footprint.py --baseline-zip <v1.4.1.zip>`.

## Regression coverage

- Correct grouped stages and reviewer identities are required; missing reviewers, stage reordering or an editorial group that is not approved blocks integral green.
- Required course consistency is one course-wide report with all declared current Word SHA-256 hashes, completed after editorial and before final source fidelity.
- Final semantic fidelity report must have been completed after editorial and must match current final Word/source hashes. A Word edited after approval blocks release.
- Claims with fake quotes, invalid locations, unregistered sources, missing source topics or incomplete review explanations fail the previous source gate.
- All 27 style controls must be covered by an assigned reviewer with appropriate evidence; role mismatch fails strict grouped QA.
- Draft mechanical checks may run without expensive fidelity; their result explicitly indicates `integral_release_eligible = false`.
- Existing Word editorial, visual-stock and stock-search guardrails pass the earlier regressions; no new permissions to invent stock or to skip rendering were introduced.
- Installation update passed in **Codex and Claude Code**, preserving `sources/`, `templates/`, `resources/`, `qa/`, `outputs/` and custom AGENTS/CLAUDE instructions.

## QA source

- Canonical 97-slide Content QA PPTX remains fully bundled and hash-verified; the deep inventory audit passes during installation.
- Fast per-resource QA checks only the 27-control register and source checksum, **without reading the entire slide index into model context**.
- The raw client sources and factual evidence remain the only authoritative basis for course claims.

## Known limits

- The lightweight-model preference is declared only as optional: native model selection varies by host and may require user settings. The installer does not force a tier.
- Mechanical checks verify source quotation existence, document hashes and schema; they **cannot themselves determine semantic truth**. The independent Fidelity reviewer remains mandatory.
- This is a synthetic regression and installed-suite test, not a live model-token benchmark or a real-course production audit. To establish a billable-token reduction, compare usage logs from the same course/materials on the same model and caching settings before and after upgrading.
- QA logs remain local. No course deliverables were uploaded.
