# Stage record guidance

A **stage** is the basic logging and learning unit in UM-MCI.

A good stage boundary should satisfy three conditions:

1. it has a coherent local goal,
2. it has a coherent local methodological organization,
3. it can be validated and diagnosed locally enough to support learning.


## When to use UM-MCI logging at all

Do not route every task through UM-MCI. Enable UM-MCI stage logging when the task has a real methodological decision to learn from. As a practical gate, use UM-MCI when at least two of the following are true:

- the task has substantive route ambiguity, not merely an information gap;
- different methodological routes would change the evidence handled, artifacts produced, validators used, or trade-offs accepted;
- a single tool call or ordinary retrieval step is insufficient to express the key decision;
- method organization is a material part of success or failure;
- the run should contribute reusable route-level learning for future tasks.

Do not enable full UM-MCI stage/meta-run logging when the task is essentially a single-step tool execution, a quick clarification, a simple lookup, or a routine implementation step with no meaningful route commitment. In those cases, keep any useful detail in an execution trace or provenance note rather than creating stage records.

## What a stage should capture

- the base paradigm for the local route,
- the selected dimension commitments as **Compass option paths**,
- any supporting edge families and how they enter the route,
- the artifact and validation requirements,
- the pre/post tension belief,
- the outcome and any failure localization.

## Complex tasks

Complex tasks should not be forced into a single flat route description. Instead, use a **meta-run** with multiple stage records and optional stage links. Each stage may have its own local route, while the overall task organization is represented by the linked structure across stages.


## When to create a stage record

Create a standalone stage record when **all three** are true:

1. the step has a coherent local goal,
2. the step involves a nontrivial methodological organization or route commitment,
3. the step can be validated or diagnosed locally enough to support later learning.

Typical reasons to create a new stage are:
- a new base paradigm is selected,
- a previous route is materially revised,
- a new artifact/validation contract becomes active,
- a meaningful tension shift needs to be attributed to a specific methodological move.

## When *not* to create a standalone stage

Do **not** create a standalone stage for every small action. Keep the following as substeps, traces, or provenance inside the current stage unless they become substantial enough to change the route:
- a single clarifying question,
- a quick web lookup or local retrieval,
- a one-off tool call that does not change the route design,
- a validator subcheck that is already part of the active stage contract.

If a clarification, retrieval, or evidence-acquisition episode becomes large enough to have its own goal, acceptance criteria, and tension effect, then it may be logged as a separate stage.

## Tension attribution

A drop in tension should be attributed to a stage only when the stage materially contributed to that change. For example, if ambiguity drops because the user clarified a requirement in one sentence, that should usually remain a trace inside the current stage rather than become a new methodological stage. If ambiguity drops because the agent restructured the specification, formalized constraints, and revalidated the route, then the reduction belongs to that stage record.


## What UM-MCI is mainly trying to learn

UM-MCI stage logging is mainly meant to learn from **route-level commitments and revisions**: which paradigms, option paths, support edges, artifacts, and validators tend to work under which tensions and contexts. It is not mainly meant to learn obvious micro-facts such as “asking one clarification question can reduce ambiguity.” Those trivial relief channels should usually remain inside provenance rather than becoming their own learning unit.


## Tension logging note

A stage should normally record only the tensions that are clearly route-relevant at that boundary.


## Tension beliefs and extensions

`tension_pre` and `tension_post` should be read as assessor beliefs about route pressure at the stage boundary, not as objective task truths.

If a team needs extra local metadata, place it under the top-level `extensions` object and namespace it by team, vendor, or project rather than adding ad hoc top-level keys.

## Nested extensions

If a team needs local additions inside artifacts, validations, edge instances, or outcomes, place them under the object-level `extensions` field rather than adding ad hoc sibling fields. This keeps shared records traversable across teams while still allowing local experimentation.


## Edge role in a stage

A supporting edge instance may be logged where a supporting paradigm enters the current base paradigm, or where the current stage prepares support for a downstream route. Use `edge_role_in_stage` to reduce ambiguity:

- `incoming_support` — the edge enters the current base stage.
- `outgoing_preparation` — the current stage prepares a downstream edge target.
- `internal_composition` — the stage internally composes multiple paradigms.
- `cross_stage_link` — the edge primarily explains a route-graph relation.

When the edge target differs from the current base paradigm, set `edge_role_in_stage` and use `scope` / `activation_reason` to make the local role explicit.


## `local_settings` versus `extensions`

Use `local_settings` only for edge-local runtime or configuration details, such as a rollout horizon, a calibration window, or a simulator setting used by that edge instance. Use namespaced `extensions` for project-specific semantic annotations or fields that may later require governance. This prevents `local_settings` from becoming an ungoverned alternative vocabulary.
