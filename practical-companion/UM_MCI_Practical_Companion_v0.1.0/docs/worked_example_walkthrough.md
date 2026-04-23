# One-page worked example walkthrough

This walkthrough shows the shortest useful path from theory to package use.

## Scenario

Suppose you have a design problem whose evaluation is expensive, partially model-based, and likely to require comparison across scenarios.

## Step 1 — theoretical framework

Read:
1. the UM8 overview to understand why this is not just “pick an algorithm”,
2. the interaction matrix to see that Optimization may use Simulation as a supporting paradigm,
3. the Optimization and Simulation Compass modules.

## Step 2 — semantic core

In the core package, inspect:
In the unpacked core release, open:
- `layer1_ontology/um_paradigms_ontology.v1.json`
- `layer2_seed/um_paradigm_compass_seed.v1.json`
- `layer2_seed/um_paradigm_defaults_seed.v1.json`

Start from the Optimization starter profile and inspect the selected option paths under the **children of** `UM.DIM.OPTIMIZATION.PROBLEM_ARCHITECTURE` (for example `OPTIMIZATION_STANCE`, `FEASIBILITY_STRUCTURE`, `DECISION_OBJECT`, `VARIABLE_TYPE`, `EVALUATION_ACCESS`, and `TEMPORAL_COMMITMENT`), then inspect `UM.DIM.OPTIMIZATION.SOLUTION_LOGIC`.

## Step 3 — practical companion

Now open:
- `examples/stage_records/03_optimization_stage_with_simulation_support.json`
- `examples/meta_runs/01_multi_stage_route_graph.json`

This shows how the abstract route becomes a machine-readable stage record with:
- dimension selections
- supporting edge instances
- artifacts
- validations
- pre/post tension beliefs

## Step 4 — if you want task-facing views

Use the projection compiler to generate a task-facing view for planning or diagnosis.

## Step 5 — if you want to accumulate experience

Use:
- `retrospective_extraction/templates/retrospective_case_template.json`
- `learned_priors/templates/route_prior_note.template.json`

The first captures what happened in a finished task; the second captures a reusable soft prior that may later become empirical.


For a builder-facing crosswalk from theory labels to dimension IDs, option paths, and record fields, see `docs/mapping_shell.md` inside the unpacked core release.


## Step 6 — follow the worked chain into shared accumulation

The same supply-network vignette now continues into three companion-level objects:
- `examples/retrospective_cases/01_supply_network_vignette_retro_case.json`
- `learned_priors/starter_notes/01_optimization_lookahead_with_simulation_support.json`
- `governance_proposals/examples/01_companion_signature_seed_proposal.json`

This is the intended public narrative: route record → retrospective case → candidate route-prior note → governance proposal.
