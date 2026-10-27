---
name: final-qa
description: 'Integra los reportes de todos los revisores de un recurso o curso y decide si se aprueba, se aprueba con ajustes o regresa a producción. Usar al final del flujo para aplicar gates de fidelidad, formato, pedagogía, visual/stock, lenguaje, consistencia y accesibilidad. Coordina correcciones automáticas solo cuando son objetivas y verificables, vuelve a ejecutar revisores afectados y evita ciclos infinitos. No sube entregables a Drive salvo petición explícita.'
---

# Final QA and release authority

Release only after the three grouped review passes complete and the **independent final Fidelity gate** confirms the final Word and source hashes. The shared passes are: `learning` (Pedagogy+Dynamism+Accessibility), `editorial` (Visual+Format+Language), `fidelity` (Source Fidelity). A separate consistency review happens **once per course before Fidelity**. See `shared/references/review-pass-contract.md` for report schema and order.

Execute deterministic gates through `shared/scripts/run_quality_gates.py --phase final`, then `scripts/aggregate_reports.py --enforce-three-passes` with the three compact JSON reports. Run course coverage check. The aggregator must independently confirm source evidence, 27 Content QA controls, group membership and report freshness; no generic `VERDE` can substitute for structural evidence. Inspect every Word page visually and verify stock relevance/licensing when possible. No unauthorized upload.

Return a short status summary and unresolved decisions; full machine logs stay in `qa/`. Fail closed if evidence, source, script, required stage or third-party search is missing. After the final fidelity stage, any Word change invalidates its SHA and requires a focused re-audit.
