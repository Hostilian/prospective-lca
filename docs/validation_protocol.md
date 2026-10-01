# Validation protocol

## Offline acceptance checks

1. `demo` imports the project.
2. Baseline plus four future combinations execute.
3. `validate --mode production` blocks synthetic unresolved assumptions.
4. Missing required study fields yield specific findings.
5. Year/background mismatch yields `TEMPORAL_MISMATCH`.
6. Unknown transformation targets yield `UNKNOWN_TRANSFORMATION_TARGET`.
7. Incompatible units yield `UNIT_INCOMPATIBLE`.
8. Every run has input, assumption, and result hashes.
9. Re-running unchanged input preserves the deterministic run UUID and result hash.
10. Changing a transformation changes the input/result fingerprints and the comparison.
11. Generated report contains synthetic banner, scope, scenarios, ledger, validation, hotspots, and limitations.
12. No licensed or confidential data appears in the repository.

## Real openLCA acceptance

To be run only with an approved local test database:

- detect offline server with an actionable message;
- resolve a named product system and method by stable descriptor;
- reproduce one independently checked calculation within a documented tolerance;
- apply one approved foreground parameter change;
- show the exact diff and preserve the source database;
- package the run without copying protected data.

## Real prospective-background acceptance

To be run only if AWAM approves premise/Brightway:

- build/load two approved target-year/pathway backgrounds;
- record premise, IAM, source database, system model, and checksums;
- produce validation/change reports;
- prove route compatibility;
- document unmapped sectors and scenario limitations;
- independently review a small reference case.

