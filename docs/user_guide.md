# User guide

## Five-step workflow

### 1. Define

Write the goal, decision context, functional unit, reference flow, boundary, geography, baseline year, target years, and impact method. Do not leave a year or category implicit.

### 2. Model

Create the baseline and named future pathways. Each transformation must identify the target, original/new value, formula, evidence, uncertainty, and approval state.

### 3. Validate

Run `validate`. Fix structural errors first. In a real pilot, unresolved critical choices and unapproved transformations must block a production-labelled run.

### 4. Run

Use the selected adapter. The offline demo uses the synthetic adapter. A future openLCA route must connect only to an approved local IPC endpoint and must record database/method metadata without copying protected data.

### 5. Interpret

Read the report as a conditional comparison. Check assumptions, validation, hotspots, foreground/background contributions, deltas, limitations, and manifest hashes before discussing results.

## Reading the demo

The report shows a baseline plus four future combinations. Negative differences are lower illustrative totals versus baseline; they are not proof of sustainability, feasibility, or future likelihood. The banner and limitations are part of the result package, not decoration.

