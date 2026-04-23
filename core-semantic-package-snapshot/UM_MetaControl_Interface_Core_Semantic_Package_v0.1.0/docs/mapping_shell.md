# Minimal mapping shell: from theory layer to machine layer

This builder-facing page shows how the UM8 theoretical framework layer maps into the machine-readable package.

## Why this matters

A minimal mapping shell provides three things:
- **trust** — the machine layer can be inspected against the theory layer,
- **reversibility** — humans can read machine logs back into Compass language,
- **shared accumulation** — route records, priors, and proposals remain legible across teams.

## Crosswalk at the smallest useful resolution

| Theory layer element | Core package layer | Primary file(s) | Typical record-level use |
|---|---|---|---|
| UM8 overview (Figure 1) | Top-level paradigm anchors | `layer1_ontology/um_paradigms_ontology.v1.json` | `base_paradigm_id` |
| Interaction Matrix (Figure 2) | Directed paradigm pair scaffold | `layer1_ontology/um_edge_slots_ontology.v1.json` | `supporting_edge_instances[*].edge_slot_id` |
| Canonical pairwise interaction family | Edge-family seed | `layer2_seed/um_edge_families_seed.v1.json` | `supporting_edge_instances[*].edge_family_id` |
| Compass major axis | Stable dimension anchor | `layer1_ontology/um_dimensions_ontology.v1.json` | `dimension_selections[*].dimension_id` |
| Stable subdimension / associated axis / layer module | Stable recordable decision space below the parent axis | `layer1_ontology/um_dimensions_ontology.v1.json` | usually the same `dimension_id` field, but now at the relevant sub-layer |
| Option family / bullet family | Paradigm-internal value space | `layer2_seed/um_paradigm_compass_seed.v1.json` | `selected_option_paths` |
| Starter entry package | Defeasible route prior | `layer2_seed/um_paradigm_defaults_seed.v1.json` | copied, confirmed, or overridden into a concrete stage route |
| Stage-level method episode | Machine-readable route record | `schemas/um_stage_record.schema.v1.json` | stage record |
| Multi-stage composition | Route graph / linked stage routes | `schemas/um_meta_run_record.schema.v1.json` | `stages[]`, `stage_links[]` |

## How to read composite parents correctly

Some theory labels are **grouping parents**, not the level at which records usually make final commitments.
Examples:
- `UM.DIM.OPTIMIZATION.PROBLEM_ARCHITECTURE` is a parent grouping layer; concrete records usually resolve its children such as `OPTIMIZATION_STANCE`, `FEASIBILITY_STRUCTURE`, `DECISION_OBJECT`, `VARIABLE_TYPE`, `EVALUATION_ACCESS`, and `TEMPORAL_COMMITMENT`.
- `UM.DIM.SIMULATION.WORLD_MODELING_APPROACH` is a parent grouping layer; concrete records usually resolve `PRIMARY_FORMALISMS`, and optionally `EMULATION_LAYER` and `COMPOSITION_LAYER`.
- `UM.DIM.INVERSION.INVERSION_OBJECTIVE` is a parent grouping layer; concrete records usually resolve `INVERSION_TARGET` and `SOLUTION_FORM`.

The theory therefore stays intact, while the machine layer becomes traversable at the level where concrete route commitments are actually logged.

## One minimal human → machine → human loop

1. A human reads the relevant Compass and chooses a route idea in Compass language.
2. The core records the same choice as `base_paradigm_id` + `dimension_selections` + `selected_option_paths` + optional `supporting_edge_instances`.
3. A later reader can inspect those fields and map them back to the corresponding Compass axes and option families.

That is the minimum reversible bridge this package is trying to preserve.

## Container layers vs selectable layers

Some Compass labels appear twice in the machine layer because the theory distinguishes a **container block** from the **record-level choice layer** beneath it. This is intentional, not duplicate ontology.

Examples:
- `UM.DIM.INVERSION.FORWARD_MODEL_CLASS` is the **container axis** for the whole forward-model block.
- `UM.DIM.INVERSION.FORWARD_CLASS` is the **selectable subdimension** under that container.
- `UM.DIM.SIMULATION.WORLD_MODELING_APPROACH` is the container axis, while `PRIMARY_FORMALISMS`, `EMULATION_LAYER`, and `COMPOSITION_LAYER` are the layers a record or UI will usually resolve.

Front-ends should surface `hierarchy_role` and render container layers as headings or grouping nodes rather than as duplicate choices. In practice, most route records select at the stable subdimension / associated-axis / layer-module level, not at every composite parent.
