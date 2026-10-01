# Facts, unknowns, and decision gates

| Area | Current status | Evidence | Gate / owner |
|---|---|---|---|
| AWAM domain | Water, energy, resource management, process engineering, valorisation, LCA are public fit areas. | S-01–S-03 | Confirm which internal process is first. Mara/AWAM. |
| Reusable capability | Mara reportedly wants a capability/tool AWAM can possess and use. | Eren post-interview report | Confirm desired user and acceptance test. Mara. |
| Real pilot | Not known. | Unresolved | Must answer before real data connection. Mara. |
| “Project LIFE” | Ambiguous. | Interview phrase/context only | Determine whether it is EU LIFE or general project life/prospective LCA. Mara. |
| Functional unit | Only synthetic demo value exists. | Demo file | Must approve real reference flow. Mara. |
| Boundary | Only synthetic demo boundary exists. | Demo file | Must approve included/excluded stages. Mara. |
| Modelling type | Demo is attributional. | Demo file | Choose attributional/consequential/hybrid intentionally. Mara. |
| Baseline data | No licensed or AWAM data included. | Repository audit | Supply approved openLCA model/database. AWAM. |
| Future background | No premise database generated. | Repository audit | Choose AWAM-defined factors or premise/Brightway route. Mara + data owner. |
| LCIA | Demo uses illustrative proxies. | Demo file | Approve method/categories/version. Mara. |
| Calculation engine | Synthetic arithmetic works; openLCA probe boundary exists. | Tests | Validate against an independently checked openLCA calculation. AWAM reviewer. |
| Governance | Critical choices and transformations are approval-gated. | `app/services/validation.py` | Name reviewer, IP owner, data location, and external-communication process. AWAM + Eren. |
| Funding/formal route | Not documented. | Interview context | Agree paid student/project arrangement before production work. Mara/AWAM. |

## Decision gates

### Gate A — Real pilot definition

Do not connect real data until the first process, decision question, functional unit, boundary, target years, and pathway labels are written.

### Gate B — Data/calculation route

Do not install or transform licensed data until AWAM names the openLCA version, database/system model, LCIA method, premise/Brightway route if any, and allowed local data directory.

### Gate C — Scientific approval

Do not label a run as production until a named scientific reviewer has approved the assumption ledger, transformation set, and result-comparison basis.

### Gate D — Acceptance and handover

The first real milestone is accepted only when another researcher can reproduce one baseline plus two future pathways, inspect every changed assumption, understand warnings, and verify the exported result package.

