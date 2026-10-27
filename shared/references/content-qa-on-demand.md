# Content QA controls - load minimally

Use `content-qa-control-register.json` (27 IDs and the source-slide locators) as the ordinary review input. Never send the entire 97-slide Markdown index or embedded PPTX as prompt context. Filter the register by reviewer agent and use only matching IDs. Use `python shared/scripts/select_content_qa_controls.py --agents language-humanizer,template-format-reviewer` to produce a concise list.

Only if a control is ambiguous, consult the corresponding **individual** slide in `source-guides/Content - Revision QA x DI.pptx` or its specific indexed section; then document the source slide and interpretation in `qa/`. The full PPTX and 97-slide index remain bundled and must pass integrity checks. The style guide is not evidence for factual course claims. The semicolon is mentioned but not taught as a standalone rule in the deck; apply the separate Spanish supplement for general use.
