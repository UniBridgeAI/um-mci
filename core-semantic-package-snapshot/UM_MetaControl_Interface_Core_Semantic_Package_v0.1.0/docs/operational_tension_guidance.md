# Operational tension guidance

Operational tensions are **route-level diagnostic pressures**. They do not redescribe the task in the abstract; they describe what is currently making the chosen route hard to specify, justify, execute, or revise.

## The clean separation

- **Context** is mostly exogenous: governance, permissions, budget, tools, and environmental drift.
- **Operational tension** is endogenous: pressure created by the current task-state **relative to the current methodological route**.

## The primary tension dimensions

UM-MCI keeps the primary route tensions at one conceptual level:

- **Ambiguity** — key goals, terms, bounds, or acceptance criteria remain under-specified.
- **Uncertainty** — important unknowns remain even with a clear specification.
- **Evidence gap** — the route wants to make claims that the current evidence base cannot yet support.
- **Consistency** — current artifacts, assumptions, models, or evidence do not fit together.
- **Tractability / feasibility pressure** — the current formulation or route is too costly, unstable, stiff, or unwieldy to carry forward reliably.
- **Horizon pressure** — the current route is carrying too much unresolved future coupling or staging burden.

These are intended to be **unique but collectively near-covering** route pressures for first-release use.

## Horizon pressure

Horizon pressure measures unresolved long-range coupling carried by the current route. A long task may have low horizon pressure after staging, milestones, receding-horizon planning, simulation support, or explicit intermediate artifacts have externalized the future dependencies.

## Why tractability belongs here

Tractability / feasibility pressure is not the same thing as external budget pressure. A route can be intractable even when budget is generous, and a route can become tractable through methodological moves such as:
- representation change,
- decomposition,
- surrogate/emulation,
- relaxation/recovery,
- scope reduction.

That makes tractability a genuine **route-design pressure**, not just a context parameter.

## Attribution policy

Record tension changes at stage boundaries. Keep trivial clarification, retrieval, or one-off search inside provenance. Create a standalone stage only when a nontrivial route commitment or locally auditable episode is introduced.

## Recommended use

Use tension beliefs sparsely at stage boundaries. In low-overhead use, track only the few tensions that are clearly route-relevant for the current stage. A practical minimal profile is often:
- ambiguity,
- evidence gap,
- tractability,
- horizon,
- and only add uncertainty/consistency when they are genuinely active.


## Belief status

Pre/post tension states in records are **assessed beliefs**, not ground-truth measurements. They should normally be recorded with confidence and evidence pointers, and may be produced by an agent, a human reviewer, or a hybrid judgment process.

## Tractability vs. Horizon

Use **Horizon** when the dominant burden is unresolved future coupling, staging dependency, or long-range interaction that has not yet been externalized into manageable stages or milestones.

Use **Tractability** when the dominant burden is the present route itself being hard to carry out: the formulation, search, computation, or execution path is currently too stiff, too expensive, too unstable, or too unwieldy to manage.


