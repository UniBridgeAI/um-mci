# Examples

These examples are **companion-level worked objects** that validate against a pinned UM-MCI core release.

Use them to learn: 
1. how stage and meta-run records are structured,
2. how core public IDs are used in practice,
3. how routes, support edges, artifacts, validations, tensions, and outcomes are logged.

## Example index

| File | What it shows | Paradigms involved | When to open it |
|---|---|---|---|
| `stage_records/01_transformation_stage.json` | Reformulating a problem into a tractable contract | Transformation | When you want the smallest single-paradigm example |
| `stage_records/02_simulation_stage_with_probabilistic_support.json` | Simulation with probabilistic uncertainty support | Simulation + Probabilistic | When you want uncertainty-aware scenario work |
| `stage_records/03_optimization_stage_with_simulation_support.json` | Optimization with simulation-in-the-loop evaluation | Optimization + Simulation | When you want a worked route with support edges |
| `meta_runs/01_multi_stage_route_graph.json` | A linked three-stage route graph | Transformation → Simulation → Optimization | When you want the main worked chain |
| `retrospective_cases/01_supply_network_vignette_retro_case.json` | Back-mapping the worked chain into retrospective form | Transformation / Simulation / Optimization | When you want to see audit/back-mapping |
| `governance_proposals/examples/01_companion_signature_seed_proposal.json` | A companion-level proposal grounded in the worked chain | Simulation → Optimization | When you want to see promotion/governance mechanics |

If you are new to the theory, open `docs/theory_and_package_map.md` inside the unpacked core release first.



Governance proposal examples now live under `governance_proposals/examples/` so that example proposals and community submissions share the same governance area.

## Edge-role note for the first stage

In `stage_records/01_transformation_stage.json`, the `Transformation -> Optimization` edge is logged with `edge_role_in_stage = outgoing_preparation`. The current stage is therefore a Transformation stage that prepares a downstream Optimization route; it is not claiming that Optimization supports the Transformation stage.

