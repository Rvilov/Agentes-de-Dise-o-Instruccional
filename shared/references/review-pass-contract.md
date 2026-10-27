# Grouped reviewer contract: three passes, seven roles

To reduce model calls, perform a **single shared-context review per group**, but keep each specialist's independent findings explicit. Stage reports can be created directly; do not generate seven verbose Markdown documents for the same resource. The stage `fidelity` is an independent high-reasoning review and must occur last.

Stage order: `learning` -> `editorial` -> **course consistency once after all editorial work** -> `fidelity` -> Final QA. These stages must be sequential and final factual evidence tied to the final Word SHA. If the Word changes after fidelity, the old approval is invalid even if the edit appears cosmetic.

Each `qa/R#.pass-<stage>.json` is a JSON object:

```json
{
  "pass": "learning",
  "resource_id": "R1",
  "completed_at": "2026-10-27T13:00:00+00:00",
  "reviews": [
    {"agent": "pedagogical-reviewer", "resource_id": "R1", "status": "VERDE", "issues": [], "content_qa_checks": []},
    {"agent": "dynamism-reviewer", "resource_id": "R1", "status": "VERDE", "issues": [], "content_qa_checks": []},
    {"agent": "accessibility-reviewer", "resource_id": "R1", "status": "VERDE", "issues": [], "content_qa_checks": []}
  ]
}
```

Editorial `reviews` must include `visual-stock-reviewer`, `template-format-reviewer` and `language-humanizer`. The final `fidelity` group must contain a `source-fidelity-reviewer` report with `status: VERDE`, `decision: APROBADO`, and actual `qa/R#.fidelity-review.json` with individual factual and topic assessments. All 27 Content QA control IDs need a real status and a brief evidence or a reason for `NO_APLICA`; distribute IDs across the seven tagged reviews. Never invent a verified control.

One course-level `qa/course-consistency-review.json`:

```json
{"status":"VERDE","completed_at":"2026-10-27T13:30:00+00:00","resources":[{"id":"R1","docx":"outputs/R1.docx","sha256":"<actual sha256>"}],"issues":[],"review_notes":"Specific comparison of names and claims across resources."}
```

Final QA should pass the three stage JSON paths to `final-qa/scripts/aggregate_reports.py --enforce-three-passes --project-dir ... --resource-id ... --docx ...`. The code checks reviewer identity, stage order, consistency review freshness, and final factual evidence. Reports that indicate only `VERDE` but lack completed structured checks must fail.
