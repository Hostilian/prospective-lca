# Reproduce and deploy the review package

## Local review

```bash
python -m app.cli demo --out exports/demo
python tools/build_report_previews.py --package exports/demo
python tools/verify_review_package.py --package exports/demo
python -m app.cli serve --dir exports/demo
```

The study brief is served at `/` and `/customer/`; the technical report is at `/reviewer/`. The original engine report remains at `/report.html`.

## Container

```bash
docker compose up --build
```

The image generates both report routes and verifies their calculation/document fingerprints during construction. Runtime needs no network or licensed database. The static server is a demonstration endpoint, not an authenticated researcher system.

## GitHub

The `quality-and-pages` workflow tests Python 3.11–3.13, compiles application/tests/tools, generates and verifies the export package, and checks that production validation returns the expected blocking exit code. It bundles the exports with the exact source revision and checksums, then retains the Python 3.12 package as the `technical-review-package` artifact for 30 days. Known database filename patterns are rejected; this is not a general data-confidentiality classifier.

The Docker job builds the image and checks the study brief, technical route and diagnostic JSON over HTTP. Pages deploys from `main` only after quality and Docker jobs pass; its package is also verified before upload and published as `technical-review-package.zip`.

Each standalone HTML is offline-readable without JavaScript. File downloads and variant switching work when the full package is retained. SHA-256 fingerprints cover the listed HTML/diagnostic artifacts and canonical calculation inputs/results. They do not establish scientific validation or institutional acceptance.
