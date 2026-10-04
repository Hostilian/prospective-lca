# Phase 2 — Questions and path

The prior chat completed Phase 1 and asked for clarification. No answers or real data appear in the supplied history. Continue with Path A, as instructed: methodology preview and workflow demonstration. These are two presentations of the same synthetic evidence, not synthetic and real-data reports.

Unanswered questions, in priority order:
1. Who is the customer, and what type of organisation is it?
2. What specific decision and decision date will this work inform?
3. What currently happens to the pomace, and what is the comparison process?
4. Which measured operating records, yields and mass balances are available?
5. What are the feedstock moisture and product quality requirements?
6. What evidence supports mineral-fertiliser substitution and co-product treatment?
7. Who owns and approves the scientific choices?
8. Which life-cycle inventory database, system model and impact method are approved?
9. Which background scenarios, versions, geography and years should be used?
10. Which uncertainty ranges and sensitivity cases should be reviewed?
11. What is the customer's LCA literacy and required language?
12. Which author/contact details and branding should appear?

[ASSUMPTION] English; restrained unbranded presentation; customer identity and decision unspecified. Version 1 explains terms for a reader new to life-cycle assessment. Version 2 serves a technical reviewer. Author/contact remain explicit placeholders. All scientific choices remain proposed.

# Phase 3 — Specification, recorded before coding

## Two versions

**Customer report:** spacious editorial document with a desktop margin contents list, short explanations and a clear intake checklist. Main message: this demonstrates the process of asking a future-facing question; it does not establish a result for the customer's plant.

**Methods review:** denser editorial review document with a horizontal contents strip, numbered evidence notes and more visible arithmetic/reconciliation detail. Main message: trace the synthetic assumptions and distinguish presentation checks from scientific approval.

## Outline for both versions

1. **Title and status.** Date, document version and author/contact placeholders; synthetic and unapproved-method limitations visible in the first viewport.
2. **Three-sentence summary.** State what is demonstrated, what the values mean and what is needed before a decision study.
3. **Study and boundary.** Define one tonne of wet grape pomace, Portugal, 2025/2030/2040 and the narrow conversion boundary; flag missing counterfactual and outputs.
4. **Scenario conditions.** Explain conditional process and background changes directly from the existing project file, with no invented pathway names or forecasts.
5. **Comparisons.** Show a single grouped horizontal chart of percentage change from the supplied baseline and a three-significant-figure totals table. Preserve exact supplied totals and percentages in the appendix, and disclose discrepancies.
6. **Baseline contributions.** Show positive burdens and the negative fertiliser credit on a signed horizontal axis. Keep the tiny water contribution labelled exactly rather than exaggerating its bar.
7. **Process and background.** Use the repository's quantity/factor transformations for an explicitly ordered synthetic decomposition; state interaction/order dependence and keep this separate from the fixed supplied headline totals.
8. **Assumptions.** Rewrite labels as statements based on ledger values, show all eight as proposed, identify the source and leave responsible owner unresolved.
9. **Limitations.** Explain proxy indicators, missing comparison treatment, missing uncertainty and missing data-quality review.
10. **Data request and next steps.** Give specific records and approval tasks needed for a real pilot.
11. **Appendix.** Glossary; exact supplied figures and supplied/recomputed percentage reconciliation; project/scenario/choice IDs; inventory transformation details; source input/ledger/result fingerprints, run ID and software validation note; separate preview-data and HTML file fingerprints.

## Charts

- **Grouped horizontal change chart:** x axis -100% to 0%, four future cases on y; climate, water and primary energy distinguished by blue, graphite and light neutral fills plus direct labels. Use percentages recomputed from the supplied displayed totals; 2-decimal labels disclose rounding. No probability or uncertainty claim.
- **Signed baseline climate bars:** x axis in kg CO2e per tonne, positive burdens right and a hatched credit left. Individual baseline contributions remain exact; explain that their actual sum is 221.18084, while 221.18 is the supplied rounded sum and 221.2 the supplied headline total.
- **Boundary diagram:** inline SVG boxes/flows for incoming pomace, conversion, inputs and outputs/credit; accompanying text fully describes it. No fabricated product yield.
- **Decomposition table:** measured in synthetic climate-proxy units; quantity changes first, factor changes second. Repository item-layer tags are not interpreted as causal reduction attribution. Show baseline, process-only intermediate and full synthetic totals, then disclose differences against the fixed supplied rounded totals.

## Plain-language glossary

Life-cycle assessment (LCA): an assessment of environmental burdens across the defined stages of a product or process. Prospective: conditional future cases. Functional unit (FU): the common reference used to compare cases, here one tonne processed. Foreground: process quantities and operating choices. Background: supplying systems and their factors. Proxy: a demonstration indicator standing in for an approved assessment. Life-cycle impact assessment (LCIA): converting inventory flows into indicators with a specified method. Credit: a modelled subtraction for an avoided activity, requiring evidence. CO2e: carbon-dioxide-equivalent unit. kWh, MJ and m3: kilowatt-hours, megajoules and cubic metres. Counterfactual: what would happen without the proposed process.

## Removed or moved

Remove gradient hero, metric-card grids, red/green judgement colours, decorative animation and raw-UUID prominence. Move identifiers, hashes, software version details, exact source decimals and automated validation to the appendix. Replace positive-length credit bars with signed bars. Retain all limitations and evidence gaps.

## Evidence policy

The user's pasted totals and contributions are authoritative for preview tables and charts. The original repository project is the source for scenario conditions and the separately labelled decomposition. Do not change the calculation engine or represent the preview as a new scientific run. Hashes of calculation artifacts refer to those artifacts, not to the user-supplied rounded display values. The preview has its own data/file fingerprints.

# Phase 1 — Audit status

The prior audit's verdict remains **DO NOT SEND as a scientific results report**. The redesigned documents may only be shared as a clearly labelled demonstration after filling author/contact and customer details. No real data, approved method, critical review, ISO compliance or scientist approval is claimed.
