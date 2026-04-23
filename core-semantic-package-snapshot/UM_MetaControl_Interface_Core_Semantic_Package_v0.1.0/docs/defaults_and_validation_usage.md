# Defaults and validation usage

The `um_paradigm_defaults_seed.v1.json` file is the **entry layer** into the Compass seed. It is not a replacement for the Compass.

## What a paradigm default contains

For each paradigm, the defaults file provides:
- `required_dimension_ids` — stable decisions that must be resolved for a minimally valid route,
- `user_must_confirm_dimension_ids` — decisions the user or downstream planner should explicitly confirm,
- optional `selection_constraints` — starter-level structural rules such as “at least one locus layer must be active”,
- one or more `starter_profiles` — defeasible starter bundles.

Each starter profile then provides:
- `dimension_selections` — the initial **Compass option paths** selected by the starter,
- `machine_control_settings` — execution/compilation controls such as validation strictness,
- `base_artifact_requirements` — artifact families that are typically needed,
- `base_validation_requirements` — validation primitives that are typically required,
- `default_support_edge_shortlist` — recurrent supporting edges worth considering first,
- `notes` — warnings and review reminders.


### What `required_dimension_ids` means

`required_dimension_ids` is a **starter-profile minimum**, not a universal theorem about the paradigm and not a claim that every major dimension must always be selected in every task. It means: this particular starter profile is not considered minimally specified until those dimensions have been resolved. Optional layers, task-specific branches, and downstream refinements may still remain inactive or undecided.

`user_must_confirm_dimension_ids` is narrower. It marks the subset of dimensions that the starter does **not** want to resolve silently on the user's behalf.

A good mental model is:
- Layer 1 tells you which decision spaces exist.
- The Compass seed tells you what values are available inside those spaces.
- The starter profile says which of those spaces it insists on resolving before this baseline route should be trusted.

## How defaults align with Layer 1 and the Compass

- Layer 1 gives the **stable public dimensions** and machine controls.
- The Compass seed gives the **full internal value space**, including option families and leaf bullet families.
- The defaults file picks conservative **option paths** inside that Compass value space.

So defaults are neither free-floating heuristics nor a separate ontology. They are starter commitments grounded in the Compass seed.

## How to use defaults in practice

A practical starter flow is:
1. choose the candidate base paradigm,
2. inspect the available starter profiles for that paradigm,
3. copy one starter profile as the initial route scaffold,
4. confirm the `required_dimension_ids` and `user_must_confirm_dimension_ids`,
5. keep the default option paths that still fit,
6. override the ones that clearly mismatch the task,
7. keep or waive validators explicitly rather than silently,
8. record later refinements in the stage record rather than rewriting the core default.

The `starter_baseline` profile is typically the most conservative entry point. It is meant to reduce first-move ambiguity, not to settle the route once and for all.


## What artifact requirements do **not** mean

`base_artifact_requirements` does **not** mean that every listed artifact is always a fresh input artifact handed to the stage at the start. It is a **stage-level contract burden**. Depending on the artifact type and the route, an artifact may be:
- already available and required at stage entry,
- produced by the stage as an output,
- updated or maintained across the stage as part of route state.

The defaults file only says that the route should account for those artifact families. Exact entry/exit direction is resolved in concrete stage planning, edge contracts, and runtime execution.

Likewise, `base_validation_requirements` names the validation burden that should normally be active for the starter route. It does **not** claim those checks are universally sufficient for every task.

## Interpreting `must`, `should`, `may`, and `waived`

- **must** = expected to be present for the starter profile unless explicitly waived,
- **should** = recommended when budget and stakes allow,
- **may** = optional strengthening checks or artifacts,
- **waived** = deliberately skipped with a reason.

These are starter-contract expectations, not claims of universal correctness. A downstream user may tighten, loosen, replace, or waive them when the task, context, or failure signals justify it.

## What defaults are *not*

Defaults are **not**:
- guaranteed optimal,
- universally correct,
- sufficient for every task,
- a substitute for reading the relevant Compass subtree.

Their role is to reduce first-move ambiguity, not to eliminate judgment.


## Starter-profile minima

`required_dimension_ids` express the **minimum semantic commitments for a given starter profile**, not eternal truths about the paradigm as a whole. Different starter profiles may require different minima.

## Artifact and validation requirements are obligations, not simple inputs

`base_artifact_requirements` and `base_validation_requirements` describe the default **stage-level contract burden** for a starter route. Some artifacts may already exist at stage entry, some may be created during the stage, and others may be maintained throughout the stage. They should not be read as a simple input checklist.
