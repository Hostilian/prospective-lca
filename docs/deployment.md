# Reproducible deployment

The workbench has three supported execution paths:

1. **Local Python** for development and review.
2. **Docker** for a stable, isolated demo server.
3. **GitHub Pages** for the generated synthetic review package.

## Local

```bash
python3 -m app.cli demo --out exports/demo
python3 -m app.cli serve --dir exports/demo
```

## Docker

```bash
docker compose up --build
```

Open `http://localhost:8765/`. The image contains only the application, the original synthetic project, and the schemas. It does not contain openLCA databases, ecoinvent files, credentials, or confidential data.

## GitHub Pages

The workflow at `.github/workflows/ci.yml` regenerates the site from the synthetic project and deploys it when a commit reaches the repository’s `main` branch. The Pages source must be set to **GitHub Actions** once in the repository settings.

The generated root page is the self-contained report. The same deployment also exposes `run.json`, `manifest.json`, CSV exports, and `report.html` for review and reproducibility.

## Pipeline guarantees

- Python compilation and the full offline test suite run on every push and pull request.
- Demo generation is verified in CI.
- The production approval gate is tested to ensure unresolved synthetic choices remain blocked.
- Forbidden licensed or database files are rejected.
- A Docker image is built and started in CI, with an HTTP smoke check.
- GitHub Pages deploys only from `main`, after quality and Docker checks pass.

## Scientific boundary

The public site is a technical demonstration only. It must not be presented as an AWAM result, an approved LCIA study, or evidence for an external decision. The scientific choices remain explicitly proposed until the AWAM owner and reviewer approve a real pilot definition and data route.

