# Phase 5 — Self-QA

Date: 4 October 2026. Preview document version 1.0; calculation workbench remains 0.1.1.

## Verdict

**Demonstration only. Do not send as a scientific results report.** Both variants use the same synthetic data. They can demonstrate the proposed workflow after customer/author/contact details are filled; real results require a separate approved study.

## Requested checklist

| Check | Result | Evidence / fix |
|---|---|---|
| Every supplied number preserved | PASS | Exact source strings for all five totals, all supplied percentages and all six contributions remain in the appendix. Display data is stored separately from engine output. |
| Every chart percentage recomputed | PASS | Decimal arithmetic: (future − baseline) / baseline × 100, using the supplied displayed totals. Labels have two decimals. Original percentages remain in the reconciliation table. Central climate is −47.92% from the displayed totals, while the original supplied value is −47.93%; both are explicitly labelled. |
| No invented facts or sources | PASS | Scenario conditions and quantities come from the original synthetic project. Proposed status and “Synthetic demonstration design note” source are retained. Decomposition is labelled as newly derived arithmetic. Customer, owner and contact are unresolved. |
| Limitations visible above fold | PASS | Verified at 375 × 812 and 1440 × 1000, in light and dark. The mobile contents list was removed from the first screen, and the warning precedes secondary metadata on narrow screens. |
| Raw scenario IDs / hashes confined to appendix | PASS | Main results and narratives use readable names; technical identifiers, source fingerprints and run ID are in the appendix. |
| Charts readable at 375 px | PASS | Separate narrow SVG layouts; direct numerical labels; no horizontal overflow or clipped SVG text. Crowded mobile axis ticks were reduced to −100%, −50% and 0%. |
| Contrast | PASS for checked colours | All rendered text colour pairs met 4.5:1, or 3:1 for large text, in both colour schemes. The light energy bar was darkened so graphic marks meet 3:1 against the page. Direct labels and fixed bar order supplement colour. |
| A4 print | PASS | Both documents render to A4. Wide boundary diagram appears once, charts stay together, and detailed transformations use one smaller table per case. The initial duplicate diagram and stranded rounding paragraph were fixed. No text lies outside the checked page margins. Final printouts have 15 pages each, including the evidence appendix. |
| JavaScript disabled | PASS | All ten report sections and both visible narrow charts remain available. Switching between variants uses ordinary links. Only the optional print button requires JavaScript; browser print works without it. |
| Self-contained, no external requests | PASS | Inline CSS, SVG and print-button script. No font/image requests, framework, tracking, fetch call, or external resource element. Version navigation is an explicit user-initiated link. |
| Each HTML below 300 KB | PASS | Approximately 55 KB per standalone file. |

All **21 offline tests** pass, including two new preview tests covering original display precision, disclosed percentage differences, signed contribution sum, absence of external resources, unique HTML IDs, output fingerprints, preservation of source artifacts and independent quantity/factor reconciliation. The existing production-mode approval gate continues to block the synthetic project.

Browser evidence was captured at mobile and desktop widths, in light and dark, plus JavaScript-disabled navigation. There were no browser execution errors or initial external requests. PDF pages were rendered for visual inspection and checked with extracted text; no charts or core tables were split. The full transformation appendix uses four separate tables so each can remain on one page.

## Arithmetic and provenance

- Supplied contributions sum to **221.18084**. **221.18** is the brief's rounded contribution sum; **221.2** is its headline total. All three are explicitly distinguished.
- Three-significant-figure table values use nearest rounding, with ties away from zero: **166.5 → 167**, **1.800 → 1.80**, **2363 → 2360**. The exact source decimals remain visible in the appendix.
- Main chart percentage rounding does not replace the supplied percentage strings. The reconciliation appendix records the discrepancy in percentage points.
- The process/background table uses the original full-precision synthetic model. Process quantities change first, then supply factors; the interaction is assigned to the latter step. In the ambitious case, the factor step includes the proposed heat-factor change. Changing the order changes the split.
- The preview does not edit the inventory, scenario multipliers, validation rules or calculation engine. Original source exports remain available; `report.html` is the original engine report.
- Source input/assumption/result fingerprints apply to the calculation artifacts. `preview-manifest.json` separately fingerprints the display dataset and each HTML file, and records the derived decomposition. Hashes do not constitute scientific verification.

## Top five remaining weaknesses and actions before sending

1. **No measured plant data or mass balance.** Obtain dated electricity, heat, water, enzyme, throughput, moisture, transport and product-yield records, with units and uncertainty ranges. Replace synthetic inputs only in a separate approved study.
2. **No agreed comparison or justified fertiliser substitution.** Establish current pomace treatment and alternative products; document nutrient equivalence and actual displacement. Approve allocation and credit treatment.
3. **No approved inventory/impact/background methods.** Agree the database, system model, versions, impact method and future supplying-system scenarios. Review geography, years and data rights.
4. **No uncertainty, sensitivity or data-quality review.** Test scale-up, electricity/heat demand, yields and credits; quantify uncertainty and independently reconcile the result.
5. **No named customer decision or accountable scientific/communication owner.** Fill the customer, author and contact placeholders; agree the goal, decision and audience; obtain scientific review and permission for the intended claims. Keep the demonstration status until real evidence supports a different status.

## Assumptions

[ASSUMPTION] English and restrained unbranded design. No named customer, customer goal or real dataset was provided. Version 1 explains terms for a new reader; Version 2 addresses a technical reviewer. Neither is a real-data Path B report. All eight scientific ledger choices remain proposed.
