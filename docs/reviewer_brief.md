# Prospective LCA workbench — prototype review brief

**Prepared by:** Eren Ozturk  
**Status:** technical prototype for discussion with Fraunhofer Portugal AWAM  
**Live demonstration:** https://hostilian.github.io/prospective-lca/

## Purpose

The prototype explores a reusable workflow for comparing a reference life-cycle assessment with conditional future scenarios. It keeps study choices, scenario changes, evidence, validation findings, and output fingerprints together so a researcher can review how each comparison was produced. It is intended to complement an approved LCA calculation workflow, not replace scientific modelling or openLCA.

## What can be reviewed now

- A synthetic reference case and four year/pathway combinations for 2030 and 2040.
- An assumption ledger that shows the foreground and background changes behind each scenario.
- Checks for missing scope, provenance, units, temporal consistency, and scientific approval state. A synthetic project cannot be labelled as a production run.
- A reproducible report with stage contributions, scenario comparisons, CSV/JSON exports, and a run manifest.
- Offline tests, a Docker smoke test, and an automated GitHub Pages deployment.

The example process and impact factors are original illustrations. The displayed numbers are **not AWAM results, validated LCIA, forecasts, or evidence that one pathway is preferable**.

## Five-minute review

1. Open the [live synthetic demonstration](https://hostilian.github.io/prospective-lca/) and read the banner and scope.
2. Compare the baseline with a future scenario and inspect the assumption ledger and validation findings.
3. Download the [run data](https://hostilian.github.io/prospective-lca/run.json) and [manifest](https://hostilian.github.io/prospective-lca/manifest.json) to see the review trail.
4. Check the [repository](https://github.com/Hostilian/prospective-lca), [automated checks](https://github.com/Hostilian/prospective-lca/actions/workflows/ci.yml), and [known limitations](../KNOWN_LIMITATIONS.md).

## Proposed first supervised pilot

Choose **one** AWAM-approved process and reference model. Agree its decision question, functional unit, reference flow, boundary, modelling type, geography, openLCA/database/system-model versions, LCIA method, and data-access rules. First reproduce the baseline through an approved local calculation route and reconcile it with the reference result. Only then add two reviewed future pathways and produce a comparison and assumption ledger.

The acceptance test and acceptable numerical differences should be set by AWAM's scientific owner before that work begins. The prototype currently has an openLCA connection probe and adapter boundary; it does **not** run a real openLCA calculation or generate a premise background database.

## Decisions requested from AWAM

1. Which process and decision should be the pilot? Does “Project LIFE” refer to a named EU LIFE project or to prospective assessment over a project's life?
2. Which model, method, target years, and future pathways are approved?
3. Who can provide a safe test model, review assumptions, and define the acceptance test?
4. What are the permitted data location, confidentiality, IP, publication, and formal collaboration terms?

The detailed [scoping questions](mara_requirements_questions.md) and [handover checklist](handover_checklist.md) support that discussion. No licensed database or confidential AWAM file is included in this public prototype.
