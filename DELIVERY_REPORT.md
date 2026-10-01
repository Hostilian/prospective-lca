# AWAM Prospective-LCA Workbench — delivery report

Date: 2026-09-29

## Outcome

The unfinished Fraunhofer Portugal AWAM prospective-LCA task has been completed as a runnable Phase 1 offline vertical slice. It is a reusable companion/workbench foundation, not a claim that the real AWAM pilot has been scientifically completed.

## Working outputs

- `app/`: domain model, validation, deterministic engine, adapters, reporting, CLI, and local server.
- `demo/sample_project/project.json`: original synthetic winery/pomace scenario set.
- `exports/demo/`: generated review package.
- `docs/research_brief.md`: AWAM/method/software research and compatibility decision.
- `docs/facts_unknowns_decision_gates.md`: facts, unknowns, and explicit blockers.
- `docs/mara_requirements_questions.md`: smallest real-pilot questions for Mara.
- `docs/scientific_method.md`: prospective-LCA controls and interpretation rules.
- `docs/data_governance.md`: local/licensed/confidential data rules.
- `docs/demo_script.md`: 2-minute walkthrough for Mara.
- `docs/handover_checklist.md`: delivered versus still scientifically blocked.
- `SOURCE_REGISTER.md`: primary/official sources and access dates.

## Demonstration contents

The synthetic project runs:

- baseline 2025;
- conservative 2030;
- central 2030;
- conservative 2040;
- ambitious 2040.

Each scenario has a named pathway, year, geography, foreground/background identifiers, narrative, transformations, formulas, evidence note, and approval state. The report separates impact proxies by scenario, stage, and foreground/background layer and includes the assumption ledger, validation findings, hotspots, limitations, and reproducibility hashes.

The climate-proxy totals are illustrative only: baseline 221.181, central 2030 115.171, conservative 2030 166.488, conservative 2040 130.201, ambitious 2040 39.030 kg CO2e proxy per synthetic functional unit. They must not be interpreted as AWAM findings or validated LCIA results.

## Commands

```bash
python3 -m app.cli demo --out exports/demo
python3 -m app.cli validate --mode demo
python3 -m app.cli validate --mode production   # expected to block the synthetic project
python3 -m app.cli serve --dir exports/demo
```

## Verification performed

- `compileall`: passed.
- Offline unittest suite: **15 tests passed**.
- Synthetic CLI run: passed; all five scenarios exported.
- Deterministic re-run test: passed; result fingerprint and run UUID remained stable.
- Change detection test: passed; changing one transformation changed results.
- Production gate: passed; unresolved/proposed synthetic assumptions were blocked with specific errors.
- Adapter contract tests: passed for JSON-RPC payload shape and premise/Brightway readiness boundary.
- Report end-to-end test: passed; scope, scenarios, validation, manifest, synthetic banner, and accessible SVG chart marker present.
- Local HTTP smoke test: passed; generated dashboard served successfully and contained the banner, chart, and validation sections.

## Scientifically validated versus technically validated

Technically validated now: serialization, scenario transformations, small unit registry, deterministic synthetic arithmetic, comparison, validation gates, manifests, HTML/CSV/JSON exports, and local serving.

Not scientifically validated now: the synthetic factors, the example process, the avoided fertiliser credit, scale-up assumptions, future background factors, pathway feasibility, any ISO-conformance claim, and any real AWAM result.

## Required decision from Mara/AWAM

The real pilot still needs the process, meaning of “Project LIFE”, decision context, functional unit, boundary, modelling type, openLCA version/OS, database/version/system model, LCIA method/categories, target years/pathways/geography, foreground/background route, data permissions, reviewer, acceptance test, formal arrangement, IP, confidentiality, and publication rules.

## Smallest next supervised milestone

Use one approved AWAM reference model and a safe small test export. Reproduce one baseline through the approved local calculation route, then add two coherent future pathways and deliver the same manifest/assumption-ledger/report package. Stop and review before expanding to a platform.

