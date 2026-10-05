# Technical review guide

5 October 2026 · Engine 0.1.1 · Report edition 1.1

Review target: a reproducible synthetic workflow and its interface boundaries. Scientific acceptance of a real prospective LCA remains outside the completed software package.

## Reproduce and inspect

```bash
python -m unittest discover -s tests -v
python -m app.cli demo --out exports/demo
python tools/build_report_previews.py --package exports/demo
python tools/verify_review_package.py --package exports/demo
python -m app.cli validate --mode production
```

The test suite and package verification should pass. The final command should return exit code 2 because the demonstration is synthetic and its critical choices remain proposed. This expected failure is an acceptance check for the production gate.

## Trace one scenario

| Step | Entry point | Reviewer check |
|---|---|---|
| Inputs | [Project JSON](../demo/sample_project/project.json), [models](../app/domain/models.py) | FU, boundary, inventory, factors, source statements and scenario IDs |
| Validation | [Validation service](../app/services/validation.py) | Structure, units, finite values, targets, years, provenance and approval state |
| Transformation | [Engine](../app/services/engine.py) | Ordered operations; compatible `set_quantity` conversion; before/after values |
| Calculation | `run_project` and `calculate_scenario` in the engine | Each contribution is quantity × factor; credits retain their sign |
| Comparison | `compare_results` in the engine | Absolute/relative change against the selected baseline; zero baseline has no percentage |
| Fingerprints | [Manifest builder](../app/services/manifests.py) | Canonical input, ledger and result fingerprints |
| Presentation | [Report builder](../tools/build_report_previews.py), [display fixture](../demo/report_preview_data.json) | Supplied display strings remain distinct from full-precision calculation values |
| Diagnostics | [Review diagnostics](../tools/review_diagnostics.py) | Credit denominator, quantity/factor interaction and identical combined totals |
| Integrity | [Package verifier](../tools/verify_review_package.py) | Recalculate the source model; reject changed exports, manifests or HTML |

Call `run_project` for the validated calculation route. The lower-level `calculate_scenario` function assumes valid inputs and does not apply the production gate itself. This distinction matters when adding an adapter or API.

## Numerical reconciliation

The engine uses Python binary floating-point arithmetic. Baseline climate proxy: 221.18084000000002 kg CO2e per tonne; its signed fertiliser credit is −17.5. The supplied display headline is 221.2. The six supplied contribution labels sum exactly, in decimal arithmetic, to 221.18084. The main table presents three significant figures; the audit appendix retains the exact supplied strings and percentages.

Percentages in the comparison chart are recomputed from supplied display totals. They can differ from percentages calculated before rounding. No displayed discrepancy is silently repaired and no source inventory is changed by report generation.

The technical report calculates diagnostics from the original model, not from the rounded display fixture:

- Credit exclusion subtracts the signed credit from each net total. Its percentage denominator is the reference with its credit removed. The 0%, 50% and 100% credit settings are arithmetic checks; they are not measured ranges, probabilities or alternative treatment systems.
- Quantity-first decomposition assigns the interaction to the subsequent factor step. Factor-first decomposition assigns it to the subsequent quantity step. Both reconcile to the same combined change.
- The interaction is `combined − quantity-only − factor-only + reference`. Foreground/background inventory labels alone do not prove which driver caused the reduction.

For example, central 2030 has a zero-credit climate proxy of 136.170756 against a zero-credit reference of 238.68084: a −42.9486% arithmetic change. Its quantity/factor interaction is +13.608. These numbers explain model behaviour; they add no scientific evidence.

## What package verification proves

The report builder first reproduces the full demonstration run and checks its calculation manifest. It refuses to attach source fingerprints to modified results. The verifier checks the same calculations, the supplied display-data fingerprint, three HTML hashes and the diagnostic JSON fingerprint/content.

Run UUID is deterministically derived from inputs; it is not a unique execution identifier. Timestamps and platform fields vary between executions. SHA-256 fingerprints detect changes relative to the included manifest; they are not signatures, independent validation or proof of scientific authorship. CSV exports and the retained original engine HTML are provided for inspection but are not covered by the preview HTML hashes.

## Tests and deployment

23 offline tests cover unit conversion, malformed/duplicate targets, finite factors, scenario selection, approval gates, deterministic reruns, exports, display precision, diagnostic arithmetic and tamper rejection. CI repeats them on Python 3.11–3.13, verifies the package and production gate, rejects known database artifact patterns, and builds/smoke-tests Docker before deploying Pages.

Known filename patterns are a packaging precaution, not a general confidential-data detector. The static server has no researcher authentication or approval workflow. No real data should be added to the public demonstration.

## Interface and scientific acceptance gaps

| Area | Current implementation | Acceptance evidence still needed |
|---|---|---|
| openLCA | Harmless HTTP probe and JSON-RPC payload construction | Approved version/model, descriptor mapping, calculation and baseline reconciliation |
| Future background | premise/Brightway availability and required-metadata boundary | Approved IAM/scenario/year/geography route, licensed data access and reproduced transformation |
| Functional equivalence | One declared tonne of wet pomace | Treatment service, moisture, outputs, quality and matched counterfactual |
| Process evidence | Synthetic activity quantities | Measured mass/energy balance, scale, yields and seasonal coverage |
| Co-products | Synthetic signed fertiliser credit | Displacement evidence, nutrient equivalence and approved allocation/substitution rule |
| Sensitivity/uncertainty | Deterministic credit/order checks | Study-specific ranges, dependencies and justified uncertainty treatment |
| Scientific approval | Proposed/approved metadata and production gate | Named reviewer and recorded institutional acceptance; approval authentication if required |
| Rights/handover | Internal-use notice and no licensed inventory | Software licence, IP, data location and permitted publication/claims |

A completed software review does not close these scientific gates. Use the [pilot decision sheet](mara_requirements_questions.md) to define the smallest next accepted milestone.
