# Developer guide

## Local development

```bash
python3 -m compileall -q app
python3 -m unittest discover -s tests -v
python3 -m app.cli demo --out exports/dev-demo
```

The runtime package uses the Python standard library in Phase 1. If an optional dependency is added, pin it, record its licence, add an offline test path, and update `THIRD_PARTY_NOTICES.md`.

## Extension rules

- Add domain fields with backwards-compatible JSON handling where possible.
- Keep adapters behind a stable interface.
- Do not put scientific assumptions in code when they belong in the project ledger.
- Add a validation code and remediation whenever a new gate is introduced.
- Include scenario/year/pathway in every result and export.
- Keep deterministic fingerprints independent of wall-clock timestamps.
- Add a contract test for every adapter and a golden test for every report shape.
- Never add licensed data to fixtures.

## Synthetic transformation units

`set_quantity` takes a value in its declared unit and converts it to the inventory item's unit before calculation. Its diff records the input and result units. `scale_quantity` takes a dimensionless multiplier; an optional unit only labels the affected flow and must match the inventory unit. Inventory factors must be present and finite for every declared impact category. These rules are limited to the synthetic adapter and do not define openLCA flow mapping.

## OpenLCA next milestone

After AWAM confirms the exact version and safe test database:

1. implement descriptor discovery;
2. resolve product systems and impact methods by stable IDs, not ambiguous names;
3. run a baseline calculation;
4. reconcile one independently checked result;
5. apply one approved foreground parameter transformation;
6. export a manifest and diff;
7. test that the source database remains unmodified.

## Premise/Brightway next milestone

Only after license and route approval: pin premise/Brightway/ecoinvent/IAM versions, store checksums and metadata, generate two background scenarios, inspect change/validation reports, and prove compatibility with the chosen calculation route.
