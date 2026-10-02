# Changelog

## 0.1.1 — 2026-10-02

- Convert `set_quantity` inputs to inventory units and record both units in transformation diffs.
- Block mismatched scale labels, malformed quantity targets, duplicate inventory IDs, missing or nonfinite impact factors, and duplicate scenario selections.
- Add focused regression tests for conversion and validation failures.

## 0.1.0 — 2026-09-29

- Recovered the unfinished AWAM/Fraunhofer prospective-LCA work.
- Added a dependency-light offline vertical slice.
- Added explicit approval states, validation gates, scenario transformations, deterministic calculation, run manifests, HTML/CSV/JSON exports, and a local server.
- Added openLCA IPC probe and premise/Brightway readiness boundaries.
- Added research brief, source register, Mara questions, method/governance docs, demo script, and handover checklist.
- Added offline unit, integration, contract, and end-to-end tests.
