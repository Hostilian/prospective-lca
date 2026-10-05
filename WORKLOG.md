# Work log

| Date | Task | Result | Blocker / decision needed | Next action |
|---|---|---|---|---|
| 2026-09-29 | Recover unfinished AWAM/Fraunhofer prospective-LCA conversation | Confirmed Mara wanted a reusable prospective-LCA capability/tool AWAM could keep and use, not only a one-off analysis. | Real pilot, meaning of “Project LIFE”, openLCA version, database, scenarios, and acceptance owner unresolved. | Build an offline vertical slice while preserving decision gates. |
| 2026-09-29 | Inspect workspace | Workspace was empty apart from Codex config. | None. | Scaffold repository. |
| 2026-09-29 | Research official sources | Recorded AWAM LCA/openLCA/ecoinvent context, ISO framework, JRC PLANET BIO, prospective-LCA terminology, openLCA IPC, premise/Brightway, and ecoinvent licensing sources. | Some current package/release pages expose different version labels; pin only after AWAM confirms route. | Add research brief and source register. |
| 2026-09-29 | Implement offline engine | Added project model, validation, scenario transformations, deterministic synthetic calculation, manifests, reports, CLI, and local server. | Synthetic output is not scientifically validated. | Add tests and verify output. |

| 2026-10-05 | Finish expert review package | Revised study/technical reports, public professional-context research, pilot decision sheet, credit/order checks, source recalculation and tamper rejection; 23 offline tests pass. Container and CI now build/verify the review routes. | Real model, methods, measured data, scientific acceptance and IP terms remain unresolved. | Review one baseline plus two approved future cases. |
