# Known limitations

## Scientific

- The demo uses original illustrative impact proxies, not an approved LCIA method.
- The grape-pomace/biogas framing is only a synthetic example; it is not an AWAM process or finding.
- The avoided fertiliser credit is intentionally exposed but has no scientifically approved allocation, substitution, market, or consequential interpretation.
- Scale-up factors, background factors, geography, years, and pathways are illustrative and not forecasts.
- Credit-exclusion and decomposition-order diagnostics are deterministic arithmetic checks; no evidence-based uncertainty distribution is inferred.
- The engine does not yet model uncertainty distributions, correlations, dynamic LCA, consequential market effects, biogenic carbon, land use, or multifunctionality beyond the visible synthetic credit.
- ISO 14040/14044 alignment is a design intention, not a conformity claim.

## Technical

- The unit registry is deliberately small and is not a full LCA flow/unit ontology.
- The openLCA adapter currently provides a harmless endpoint probe and JSON-RPC payload builder, not a complete descriptor/calculation/reconciliation implementation.
- The premise/Brightway adapter currently records readiness metadata and intentionally does not import licensed databases.
- There is no database migration layer, multi-user access control, authentication, or telemetry.
- The generated HTML is responsive and self-contained but is not a replacement for a full researcher workflow UI.
- PDF and XLSX exports are not implemented in Phase 1; HTML, CSV, and JSON are the canonical exports.
- Both review routes have desktop/mobile, light/dark, JavaScript-disabled and A4 print checks. This tests presentation and package integrity; an AWAM real-pilot review remains required.

## Scope blockers for the real pilot

Mara/AWAM must confirm the real process, functional unit, boundary, target years, pathways, foreground/background route, openLCA version, database/system model, LCIA method, access permissions, acceptance test, and formal arrangement before real data is connected.
