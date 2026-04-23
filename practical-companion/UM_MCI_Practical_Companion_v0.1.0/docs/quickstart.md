# Quickstart

## Smallest practical path

1. Unpack the pinned core release locally.
2. Install the minimal validation dependency once if needed:

```bash
pip install -r requirements-minimal.txt
```

3. From the companion root, run:

```bash
python scripts/validate_workspace.py --core-root /path/to/UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0 --companion-root .
```

For ordinary contribution work, this command skips MANIFEST hash checks so changed local files do not fail validation for release-integrity reasons. For maintainer release checks, add `--release`.


4. Open:
- `examples/stage_records/03_optimization_stage_with_simulation_support.json`
- `examples/meta_runs/01_multi_stage_route_graph.json`

5. If you want the smallest possible authoring surface, start from:
- `templates/minimal_stage_record.template.json`
- `templates/minimal_meta_run_record.template.json`

6. Move to one of the companion workflows only when needed:
- `projection_compiler/` for task-facing projections
- `retrospective_extraction/` for back-mapping papers/projects/traces
- `signature_library/` for recognizer seeds
- `learned_priors/` for soft-prior accumulation

This document is command-first. For role explanations, read `docs/start_here.md`.


## Advanced repeated local checks

After the pinned core release has already been validated once, contributors who are only editing companion examples or notes may use `--skip-core-validator` for a faster local semantic check. Maintainers should not skip core validation in `--release` mode.
