# Research brief

## Executive finding

The reusable product should be a **local-first prospective-LCA workbench** that manages study definitions, scenarios, evidence, transformations, validation, calculation adapters, comparison, and reviewer-ready exports around AWAM’s established LCA workflow. The first technical milestone can be delivered without licensed data. The first real scientific milestone cannot be completed until AWAM confirms the pilot process and modelling choices.

## Evidence categories

| Statement | Evidence class | Interpretation |
|---|---|---|
| AWAM works across water, energy, resource management, process technologies, and valorisation. | Official AWAM pages, S-01/S-02 | Strong public fit for a process/scenario tool, but not evidence of internal workflow details. |
| AWAM’s public LCA sheet names openLCA and ecoinvent. | Official AWAM sheet, S-03 | Strong reason to design an openLCA companion and keep databases external. |
| Mara wants a reusable prospective-LCA capability AWAM can use. | Eren’s post-interview report | Important user context; exact pilot still unresolved. |
| A winery/grape-pomace case is the real AWAM pilot. | Unresolved | It is only the synthetic demonstration chosen to exercise the architecture. |
| “Project LIFE” means the EU LIFE programme. | Unresolved | Do not assume this. Ask Mara. |

## What prospective LCA means here

The workbench treats prospective LCA as a forward-looking LCA in which the product system is represented at a future point relative to the study. The future is represented through conditional scenarios, not a guaranteed prediction. A scenario must therefore carry at least a target year, geography, technology maturity, pathway narrative, foreground assumptions, background source/pathway, and model/database metadata.

Future-oriented terminology is not interchangeable. “Prospective” points to temporal position relative to the study; “ex-ante” is often used for early-stage technology assessment; “dynamic” may refer to time-dependent flows or impacts; “consequential” concerns modelling consequences of a change and does not automatically mean future-oriented. The application stores these choices separately rather than treating a year label as a complete scenario.

## Method controls derived from the sources

The workbench makes the following controls visible:

1. **Goal and scope first:** functional unit, reference flow, boundary, geography, intended use, and modelling type must be stated.
2. **Temporal consistency:** foreground and background years must be compatible or an approved bridge must be documented.
3. **Scenario consistency:** a target year without a pathway narrative is invalid for a real run.
4. **Foreground/background separation:** contribution totals are stored separately when the adapter supplies the layer.
5. **Scale-up transparency:** pilot/lab observations and future engineering assumptions are separate ledger entries.
6. **Data representativeness:** source, time, geography, technology fit, reliability, and limitations are recorded.
7. **Comparability gates:** scenarios should not be compared as like-for-like if their functional units, boundaries, methods, or system models differ.
8. **Interpretation:** reports include hotspots, comparison deltas, warnings, and limitations—not only a single ranking.
9. **Uncertainty honesty:** parameter, scenario, model, variability, and data-quality uncertainty are distinct. Unknowns are not turned into arbitrary probability distributions.

## Software ecosystem

| Tool | Role | Strength | Constraint / decision |
|---|---|---|---|
| openLCA | Primary candidate calculation engine at AWAM | Public AWAM material names openLCA; IPC makes a companion possible. | Exact AWAM version, database, system model, method, and approved IPC calls must be confirmed. |
| `olca-ipc` | Python IPC client | Avoids inventing a protocol and supports JSON-RPC/REST routes. | Pin the exact compatible release after the openLCA version is known; test against a safe AWAM database. |
| Brightway | Alternative/optional calculation route | Flexible Python ecosystem and documented framework. | A second engine increases reconciliation burden; use only if AWAM approves it. |
| premise | Optional prospective-background generator | Connects IAM scenarios to LCA background data and publishes validation/change concepts. | Requires ecoinvent/source-data licensing, compatible versions, IAM/pathway/year metadata, and a decision whether results return to openLCA or stay in Brightway. |
| Activity Browser | Optional Brightway GUI | Useful if AWAM already uses it for Brightway-based review. | Not needed for Phase 1 and would add another interface. |
| ecoinvent | Licensed LCI background | Mature system models and broad coverage. | Never bundle or redistribute it; system model and developer/integration terms must be explicit. |

## Current-version observations (access date 2026-09-29)

- The official openLCA download page surfaced openLCA 2.7.0.
- The upstream `olca-ipc.py` repository metadata surfaced project version 2.6.3.
- The current premise documentation is labelled 2.5.2 and lists ecoinvent compatibility entries through 3.12.
- The premise repository/release page also surfaced a 2.4.9.1 release entry. This is a version-resolution warning, not a recommendation to install one blindly. For the pilot, pin a release from the project’s own package/release metadata after AWAM confirms the calculation route.

## Compatibility conclusion

The smallest credible architecture is:

```text
project files + assumption ledger
            ↓
scenario/validation/orchestration layer
       ↙              ↓                ↘
synthetic adapter   openLCA IPC      premise/Brightway adapter
       ↓              ↓                ↓
comparison, manifests, review package, audit trail
```

The offline vertical slice uses only the left adapter. It is useful now because its validation, manifests, scenario IDs, and report contract can remain stable when the real calculation adapter is added.

## What remains unknown

- Which AWAM project/process is first.
- Whether “Project LIFE” is an EU LIFE project name or a general project-life/prospective-LCA phrase.
- The decision the first comparison must support.
- Functional unit, reference flow, boundary, allocation, and modelling type.
- openLCA version/OS, database version, system model, LCIA method, categories.
- Target years, pathways, geography, and whether foreground/background/both change.
- Whether premise/IAM scenarios are wanted or AWAM-defined pathways are sufficient.
- Access, storage, IP, formal paid arrangement, publication/confidentiality, and acceptance owner.

## Source register

See [`SOURCE_REGISTER.md`](../SOURCE_REGISTER.md) for URLs, access dates, evidence classes, and claims.

