# AWAM Prospective LCA Workbench

A local-first, auditable companion for prospective life-cycle assessment work. It is designed to sit around established tools such as openLCA, ecoinvent, Brightway, and premise rather than replace them.

**Review the prototype:** [Live synthetic demo](https://hostilian.github.io/prospective-lca/) · [Reviewer brief](docs/reviewer_brief.md) · [CI and Docker verification](https://github.com/Hostilian/prospective-lca/actions/workflows/ci.yml) · [Two-minute walkthrough](docs/demo_script.md)

This is a discussion prototype for Fraunhofer Portugal AWAM. Its winery example and impact factors are synthetic. It is ready to demonstrate the workflow, but no real AWAM model has been connected or scientifically validated.

For a quick review, open the demo, inspect its scenario comparison and assumption ledger, then read [the questions for a real pilot](docs/mara_requirements_questions.md) and [the known limitations](KNOWN_LIMITATIONS.md).

The repository currently contains a complete offline vertical slice:

- a typed, serializable project model;
- explicit scientific choices and approval states;
- scenario/year/pathway separation;
- reviewable foreground/background transformations;
- unit checks for the synthetic inventory;
- validation that blocks production-labelled runs with unresolved choices;
- deterministic synthetic calculations with foreground/background and stage contributions;
- reproducibility fingerprints and run manifests;
- HTML report/dashboard plus CSV and JSON exports;
- an openLCA IPC probe boundary;
- a premise/Brightway readiness boundary that does not import or redistribute licensed data;
- an offline test suite and a 2-minute demonstration script.

The demo is intentionally synthetic. It is not an AWAM result, not an approved LCIA method, and not evidence that any future pathway will occur.

## Quick start

From the repository root:

```bash
python3 -m app.cli demo --out exports/demo
python3 -m app.cli serve --dir exports/demo
```

Open `http://127.0.0.1:8765/` in a browser. The generated package contains:

```text
exports/demo/
  index.html          # local dashboard/report
  report.html         # same self-contained report
  run.json            # machine-readable results and validation
  manifest.json       # reproducibility metadata and hashes
  results.csv
  contributions.csv
  assumptions.csv
```

### Docker quick start

The same synthetic, offline demo can run in a reproducible container:

```bash
docker compose up --build
```

Open `http://127.0.0.1:8765/`. The container does not include licensed databases, credentials, or confidential AWAM data.

### GitHub Pages and CI

The repository pipeline is defined in `.github/workflows/ci.yml`. It runs the test suite on Python 3.11–3.13, checks that the production gate remains fail-closed, rejects licensed/database artifacts, builds and smoke-tests Docker, and deploys the generated synthetic report to GitHub Pages from `main`. See [docs/deployment.md](docs/deployment.md).

## Commands

```bash
# Run the offline synthetic demonstration.
python3 -m app.cli demo --out exports/demo

# Validate without calculating. Production mode intentionally blocks the demo.
python3 -m app.cli validate --mode production
python3 -m app.cli validate --mode demo

# Run a selected scenario set.
python3 -m app.cli run --mode demo \
  --scenarios baseline-2025,central-2030,ambitious-2040 \
  --out exports/selected

# Probe a locally started openLCA IPC endpoint without sending project data.
python3 -m app.cli probe-openlca --endpoint http://localhost:8080

# Serve an already exported package.
python3 -m app.cli serve --dir exports/demo
```

For Windows PowerShell, use `py -3` in place of `python3`.

## Scientific and governance position

The application treats prospective LCA as a conditional scenario exercise, not an automatic prediction. Goal and scope, functional unit, boundary, modelling type, database/system model, LCIA method, geography, years, pathway assumptions, scale-up, allocation, and external-communication status are explicit decision gates.

The real AWAM pilot must be based on:

1. one approved reference openLCA model;
2. one functional unit and boundary;
3. two coherent future years/pathways;
4. an approved foreground/background data route;
5. a reviewer-approved assumption ledger;
6. an independently checked calculation result.

The current demo intentionally leaves these choices `proposed` and uses original synthetic factors. It cannot pass a production validation gate until AWAM’s scientific owner resolves and approves them.

## Repository map

```text
app/
  domain/                 Serializable models and units
  services/               Validation, calculation, hashing, manifests
  adapters/               Synthetic, openLCA probe, premise/Brightway boundary
  reporting/              CSV and self-contained HTML exports
  ui/                     Local static server
demo/sample_project/      Original synthetic project definition
docs/                     Research, method, governance, questions, handover
tests/                    Offline unit, integration, contract, and end-to-end tests
```

## What is deliberately not included

No ecoinvent files, `.zolca` database, EcoSpold data, AWAM confidential data, credentials, external API keys, or real project results are present. Any future integration must respect AWAM’s data location, ecoinvent licensing, openLCA version, database/system model, and internal review process.

## Current status

This is a technically working Phase 1 offline vertical slice. The openLCA and prospective-background phases are intentionally gated until Mara/AWAM supplies the real pilot definition and approves the data/calculation route. See [docs/handover_checklist.md](docs/handover_checklist.md), [docs/mara_requirements_questions.md](docs/mara_requirements_questions.md), and [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).
