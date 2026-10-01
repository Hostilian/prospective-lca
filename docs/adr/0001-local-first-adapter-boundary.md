# ADR 0001 — Local-first adapter boundary

## Context

AWAM’s public material names openLCA and ecoinvent, while the exact internal versions, database permissions, and prospective-background route are not yet confirmed. A student prototype should remain useful without pretending that an untested openLCA/premise combination is seamless.

## Decision

Use a local-first orchestration layer with three adapters: synthetic (implemented), openLCA IPC (probe boundary first), and optional premise/Brightway (metadata/readiness boundary first). Keep licensed/confidential data external.

## Consequences

- The offline demonstration and tests are reproducible now.
- Real calculations require a supervised adapter milestone.
- The project avoids copying or redistributing protected inventories.
- Adapter contracts and manifests can remain stable when the engine changes.

## Revisit when

AWAM confirms the first pilot, approved openLCA version/database/method, data location, and whether the future background belongs in openLCA, Brightway, or a reconciled route.

