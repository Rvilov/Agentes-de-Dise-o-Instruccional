# Compact grouped review output

Use the **current** `shared/references/review-pass-contract.md` for `qa/R#.pass-learning.json` and `qa/R#.pass-editorial.json`. Each reviewer is represented once within the grouped `reviews[]` array, with its own `agent` ID, status, issues and relevant Content QA controls; do not output seven redundant standalone Markdown reports. Fidelity is the independent third group. Reports live only in `qa/`.
