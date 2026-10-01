# Scientific method and reporting rules

## Intended use

This workbench supports prospective scenario definition and calculation orchestration. It does not confer ISO conformity and does not replace AWAM’s scientific review.

## Minimum real-pilot record

Every real study should state:

- goal, intended use, decision context, and audience;
- functional unit and reference flow;
- system boundary and excluded stages;
- attributional/consequential/hybrid choice;
- allocation, substitution, recycling, and end-of-life treatment;
- baseline year, target year(s), geography, technology maturity, and pathway narratives;
- foreground measurements/assumptions and scale-up rule;
- background database/version/system model and any prospective transformation;
- LCIA method/version/categories;
- data-quality/representativeness limits;
- sensitivity and scenario uncertainty treatment;
- reviewer, approval state, and permitted communication status.

## Scenario design

A scenario is not just a year. It is:

```text
scenario = year + pathway + geography + technology maturity
           + foreground ID + background ID + narrative
           + explicit assumptions + approved transformations
```

Two scenarios may be compared only when the comparison basis is compatible. If a functional unit, boundary, method, system model, or critical modelling rule differs, the report should warn or refuse a like-for-like comparison.

## Scale-up

The tool should distinguish:

- measured pilot/lab values;
- engineering-design values;
- literature values;
- expert elicitation;
- scenario assumptions;
- unknowns.

Any learning curve, yield improvement, energy reduction, capacity change, or substitution must store the formula, evidence, applicable scenario, uncertainty/range, and reviewer.

## Uncertainty sequence

Phase 1: deterministic comparison. Phase 2: reviewer-selected one-at-a-time sensitivity and ranges. Phase 3: optional Monte Carlo only if distributions and correlations are scientifically justified. Scenario uncertainty must not be hidden inside a single probability distribution.

## Interpretation

Results are conditional. A lower number in the ambitious synthetic scenario means only that the illustrative transformations produce a lower arithmetic total under the illustrative factors. It does not mean the pathway is feasible, likely, or environmentally preferable across omitted categories.

