---
name: resource-producer
description: 'Genera recursos instruccionales individuales a partir de una Ficha Maestra aprobada, Matriz de Cobertura y uno o varios materiales base. Usar cuando ya estén definidos el número y tipo de recursos y se deba producir R1, R2, R3, etc. Entrega cada recurso como Word independiente con la plantilla oficial, conserva trazabilidad a fuentes en archivos externos al Word, incorpora narrativa, interacción y visuales según el proyecto, y nunca sube archivos a Drive salvo petición explícita.'
---

# Resource producer

Produce one editable Word per resource from the approved template, with a single initial metadata header, short standardized **Notas de Edicion**, and **Contenido del Recurso**. A4 portrait unless expressly authorized otherwise. Keep facts, instructions, dialogues and actual supporting images in Content; never insert internal source citations or QA into Word.

Use `shared/references/editorial-stock-enforcement.md` only to create `qa/R#.editorial-contract.json` and `qa/R#.stock-search-log.json`. Render notes from the editorial JSON using `shared/scripts/editorial_contract.py apply`; do not free-write inconsistent notes. Stock is optional where appropriate, but if chosen, perform a real provider search, inspect and log candidates; images belong with content, concrete video-stock needs a real clickable URL. On blocked searches, record a pending asset without inventing a link or claiming ready for editing.

Use `shared/references/word-delivery-contract.md` for DOCX generation and visual rendering. Consult `shared/references/rise-editorial-reference.md` only for Rise, `shared/references/visual-language-and-stock-policy.md` for videos/visual planning, and `shared/references/source-fidelity-evidence-policy.md` **after the last editorial modification** to prepare the independent factual review. Do not approve your own factual assertions.

Run draft mechanical preflight without fidelity. Maintain brief factual evidence notes while authoring so the final fidelity pass can locate evidence efficiently. Do not invent facts, access URLs or examples portrayed as client policy. Keep deliverables local.
