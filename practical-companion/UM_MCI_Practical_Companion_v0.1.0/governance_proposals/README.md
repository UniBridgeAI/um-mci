# Governance proposals

This directory is the bridge between fast-changing companion material and slower-changing core releases.

Use a governance proposal when a recurring pattern seems stable enough to justify one of the following:
- promotion into a Layer-2 seed,
- promotion into the Layer-1 shared vocabulary,
- revision of an existing default, edge family, or validation expectation.

Do **not** edit the public core vocabulary directly in ad hoc downstream copies if the goal is cross-domain sharing. Instead:
1. accumulate evidence in examples, retrospectives, signatures, or candidate route-prior notes,
2. submit a proposal here,
3. let maintainers decide whether the change belongs in a future core release.


Evidence pointers should be directly relevant to the requested action. If a proposal argues for a signature seed or promotion step, its evidence should point to cases or objects that actually instantiate that pattern.

## Directory layout

- `templates/` — proposal templates.
- `examples/` — maintainer-provided illustrative proposals.
- `proposals/` — community or project proposals under review.

Workspace validation checks proposal JSON files in both `examples/` and `proposals/`.

## Example targets versus real proposals

Some illustrative examples may target an existing maintainer-provided starter seed to demonstrate the review workflow. Real community proposals should usually target a contributed seed, a proposed new object, or a promotion candidate rather than silently modifying `starter_seeds/`.


## Edge-family payload discipline

If a proposal uses `payload.edge_family_id`, it must be a released `UM.EDGE_FAMILY.*` ID from the pinned core. Companion-local or proposed edge families should be described in the proposal payload and evidence first; they should not be silently written as public UM IDs before promotion.
