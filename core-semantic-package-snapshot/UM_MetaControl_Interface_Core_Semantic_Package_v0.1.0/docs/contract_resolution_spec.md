# Contract resolution specification (minimal)

This document defines the minimal resolution order assumed by the core package.

## Resolution order

1. Choose the **base paradigm** for the stage.
2. Load the selected **starter profile** for that paradigm, if one is used.
3. Apply any explicit **dimension selections** that override or refine the starter profile. These selections are expressed as **Compass option paths**, so they may stop at a stable option family or descend to a leaf bullet family when finer control is needed. In other words, defaults resolve against the Compass seed rather than against a separate runtime projection layer.
4. Apply **machine-control settings** such as validation strictness or provenance mode.
5. Apply any chosen **supporting edge families** and their local settings.
6. Apply **governance** and **affordance** escalations or restrictions.
7. Enforce any structural selection constraints carried by the active dimensions or defaults (for example, the requirement that a fusion route activates at least one fusion locus layer).
8. Record any explicit **waivers** or manual overrides.
9. Emit a `resolution_snapshot` for the stage record.

## Important interpretation rules

- Defaults are defeasible starters, not mandatory truth.
- Supporting paradigms are recorded through supporting edge families because edge families specify **how** the support enters the route.
- Supporting edges are optional and context-sensitive.
- A complex task may be represented as a graph of linked stage-routes rather than one flat route.
- The package does not prescribe a single planner or learning algorithm; it only standardizes the upper-level contract inputs and outputs.
