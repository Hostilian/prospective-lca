# Decisions

## D-001 — Build a companion, not a replacement

**Decision:** The application orchestrates scenario definitions, evidence, validation, reproducibility, comparison, and reporting around openLCA/Brightway/premise. It does not rebuild those engines.

**Reason:** AWAM already works with LCA tools and databases. A small companion is easier to review and less likely to introduce an opaque second calculation engine.

**Status:** Accepted for Phase 1; confirm during real-pilot scoping.

## D-002 — Local-first and no licensed data in the repository

**Decision:** Offline mode works without a cloud account. Licensed/confidential data stays on the approved local system and is represented in manifests by metadata only.

**Reason:** Reduces data-exfiltration and redistribution risk and supports a researcher’s local workflow.

## D-003 — Production gate requires scientist approval

**Decision:** Critical choices and transformations must be `scientist_approved` before a production-labelled run. Demo mode can run proposed synthetic assumptions but labels them clearly.

**Reason:** A form with fields is not scientific validation. AWAM owns modelling choices and interpretation.

## D-004 — Deterministic offline adapter first

**Decision:** The first runnable milestone uses original synthetic inventory data and deterministic arithmetic. openLCA/premise adapters are explicit, opt-in boundaries.

**Reason:** The real pilot details and licensing route were not available at implementation time. The independent engineering work can still proceed.

## D-005 — No automatic Monte Carlo in Phase 1

**Decision:** Start with deterministic scenario comparison and explicit ranges/sensitivity later.

**Reason:** Prospective scenario uncertainty and model uncertainty should not be disguised as arbitrary probability distributions.

