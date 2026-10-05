# Prospective LCA workbench

Independent prototype prepared by Eren Ozturk for technical discussion with Fraunhofer Portugal AWAM. The review package demonstrates scenario transformations, an assumption ledger and reproducible exports around a fixed synthetic grape-pomace example.

**Start here:** [Technical report](https://hostilian.github.io/prospective-lca/reviewer/) · [Study brief](https://hostilian.github.io/prospective-lca/customer/) · [Technical review guide](docs/technical-review.md) · [Download review package](https://hostilian.github.io/prospective-lca/technical-review-package.zip) · [Automated checks](https://github.com/Hostilian/prospective-lca/actions/workflows/ci.yml)

The software review package is ready for inspection. Scientific acceptance remains open: no AWAM inventory, licensed database, approved LCIA calculation or real prospective background has been connected. The numerical example is synthetic and cannot support investment, technology-ranking or environmental-performance claims.

## Review in ten minutes

1. Read the scope and interpretation limits in the technical report.
2. Inspect the scenario transformations, signed fertiliser credit, credit-exclusion check and order-dependent quantity/factor decomposition.
3. Use the audit appendix to reconcile the exact supplied display values with the full-precision calculation exports.
4. Follow the [review guide](docs/technical-review.md) through the code, tests and package verification. Record findings against the [pilot acceptance gates](docs/mara_requirements_questions.md).

The [reviewer brief](docs/reviewer_brief.md) sets the requested review scope. The [professional context note](docs/reviewer-context.md) records the public research used to tailor it for Dr. Mara Silva; it does not attribute requirements or approval to her.

## Reproduce the package

Python 3.11 or later; no runtime packages or database required. From the repository root:

```bash
python -m unittest discover -s tests -v
python -m app.cli demo --out exports/demo
python tools/build_report_previews.py --package exports/demo
python tools/verify_review_package.py --package exports/demo
python -m app.cli serve --dir exports/demo
```

Open http://127.0.0.1:8765/. On Windows, `py -3` can replace `python`.

| Export | Purpose |
|---|---|
| `index.html`, `customer/index.html` | Self-contained study brief |
| `reviewer/index.html` | Self-contained technical report and arithmetic diagnostics |
| `report.html` | Original engine report, retained for reconciliation |
| `run.json`, `manifest.json` | Full-precision calculation, validation, provenance and fingerprints |
| `results.csv`, `contributions.csv`, `assumptions.csv` | Tabular review exports |
| `review-diagnostics.json` | Credit-exclusion and reverse-order checks |
| `preview-manifest.json` | Display-data, HTML and diagnostic fingerprints |

The two report routes preserve all supplied totals, percentages and contribution labels in the appendix. Main-table rounding and small percentage discrepancies are disclosed. The downloadable ZIP records its exact source revision and includes file checksums. Core content works offline without JavaScript or external assets. Optional file links require the complete export package.

## Container and CI

```bash
docker compose up --build
```

The container generates and verifies the same report routes before serving them. GitHub Actions tests Python 3.11–3.13, checks the production gate, verifies exports, builds and smoke-tests the container, retains a review artifact, and deploys Pages from `main`. See [deployment notes](docs/deployment.md).

## Implementation boundary

Implemented: serializable project/scenario models, unit conversion, validation, deterministic quantity × factor calculations, transformation diffs, stage/layer contributions, exports and package integrity checks.

Interface boundaries: the openLCA adapter performs an HTTP connectivity probe and builds JSON-RPC payloads; it does not identify or calculate an approved model. The premise/Brightway adapter records readiness metadata; it does not generate a future database. They must pass a supervised baseline reconciliation before real use.

## Scientific acceptance and rights

A real pilot requires an approved treatment service and FU, boundary and counterfactual, measured inventory, database/system model and LCIA method, coherent future pathways, justified co-product treatment, and agreed numerical acceptance tolerances. The eight demonstration choices remain proposed. Production validation blocks this synthetic project.

[Known limitations](KNOWN_LIMITATIONS.md) distinguish software checks from scientific evidence. No licensed inventory, credentials or confidential AWAM files are included. Copyright, software licence and institutional IP terms remain unresolved under the [internal-use notice](LICENSE-or-INTERNAL-USE-NOTICE.md); public visibility does not constitute AWAM endorsement or an open-source licence grant.
