# Prospective LCA workbench: review brief

Prepared by Eren Ozturk · 5 October 2026 · Review document edition 1.1

Independent prototype for technical discussion with Fraunhofer Portugal AWAM. Requested review: whether the scenario and evidence workflow is a suitable basis for one supervised pilot.

[Technical report](https://hostilian.github.io/prospective-lca/reviewer/) · [Study brief](https://hostilian.github.io/prospective-lca/customer/) · [Code and verification guide](technical-review.md)

## Reviewable now

One synthetic reference inventory and four future year/pathway cases. The package exposes transformed quantities and factors, an eight-entry proposed assumption ledger, stage contributions, signed credits and full-precision exports. The technical report adds credit exclusion and a reverse-order decomposition to show how methodological choices affect interpretation.

The figures demonstrate bookkeeping and reproducibility. They are not AWAM results, validated LCIA or projections of Portuguese supplying systems. A lower proxy total does not establish functional equivalence, feasibility or environmental preference.

## Review questions

1. Does the model keep reference flow, treatment service, boundary, counterfactual and co-product treatment sufficiently visible?
2. Can a researcher trace each scenario from the source quantity/factor through its transformation and contribution to the exported comparison?
3. Are credits, quantity/factor interaction and numerical presentation differences explicit enough for review?
4. Which approved reference model, calculation route and numerical tolerances should define the first pilot acceptance test?

## Software boundary

The offline synthetic calculation and exports work. The openLCA adapter currently probes connectivity and constructs payloads; it does not execute or reconcile a real model. The premise/Brightway adapter is a readiness boundary. Production validation blocks the synthetic project and proposed critical choices. Recorded approval states are metadata, not authenticated institutional sign-off.

## Proposed first pilot

Select one approved model and decision question. Record FU/reference flow, moisture and outputs, boundary/counterfactual, allocation or substitution rule, software/database/system-model/LCIA versions and permitted data location. Reproduce the baseline through the approved local route; a second researcher reconciles results against tolerances set beforehand. Only then add two coherent future cases and review sensitivities.

Deliver the model identifiers, evidence ledger, contributions, exports, fingerprints and discrepancy explanations together. [Pilot decision sheet](mara_requirements_questions.md) · [Handover checklist](handover_checklist.md).
