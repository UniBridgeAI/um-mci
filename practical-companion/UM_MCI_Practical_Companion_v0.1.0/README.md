# UM-MCI Practical Companion v0.1.0

The UM-MCI Practical Companion is the faster-moving GitHub layer around the **UM-MCI Core Semantic Package**. It provides examples, templates, validators, projection utilities, retrospective extraction scaffolds, signature seeds, candidate route-prior notes, and contribution workflows aligned to a pinned core release.

## Where to start

| Your purpose | Why this path matters | Start here |
|---|---|---|
| Understand how UM8 helps with complex problem-solving or method-route choice | UM8 helps compare high-level methodological routes before committing to a solver, tool, or domain default. | Start with the UM8 theoretical overview: https://doi.org/10.5281/zenodo.18790203. Then open the relevant Compass module linked from that record. You do not need this companion unless you need practical examples or workflow scaffolding. |
| Use UM-MCI in an agent, workflow, logger, or reproducible system | The companion helps connect the core vocabulary to practical workflows that support long-horizon planning, global planning, meta-control, route diagnosis, meta-policy learning, and reusable soft-prior accumulation. | Read `docs/start_here.md`, then `docs/quickstart.md`, then validate one example stage or meta-run. |
| Contribute shared methodological experience | Experience from different domains, teams, or agents becomes reusable when it is expressed through the same released public vocabulary rather than private local terminology. | Read `CONTRIBUTING.md`, then open the template for the contribution type you want to submit. |
| Maintain or redistribute a controlled release | This path is for the package owner, release steward, or downstream integrator who pins and redistributes a controlled snapshot. Most users can skip it. | Use `docs/release_checklist.md` and release validation mode. |

## Core and companion layers

- **Core Semantic Package**: stable public vocabulary, Compass-aligned seeds, schemas, edge-family seeds, starter defaults, and core validation.
- **Practical Companion**: examples, templates, projection utilities, retrospective extraction workflows, signature seeds, candidate route-prior notes, contribution workflows, and workspace validation.

The companion uses the released core vocabulary. It should not silently mint replacement `UM.*` IDs.

## First validation command

From the unpacked companion root, with the core package unpacked locally:

```bash
python scripts/validate_workspace.py --core-root /path/to/UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0 --companion-root .
```

By default, this runs semantic validation: the core validator plus the example, signature, prior-note, and governance-proposal validators. It skips MANIFEST hash checks so ordinary edits do not fail for release-integrity reasons. Add `--release` for maintainer release validation, including strict core and companion MANIFEST checks.

## Minimal starting objects

If you want the smallest possible starting point, open:

- `templates/minimal_stage_record.template.json`
- `templates/minimal_meta_run_record.template.json`

Then move to `examples/` once the structure is familiar.

## Citation and license

This companion is licensed under **Apache-2.0**. The full license text is in `LICENSE`.

For scholarly, research, or public-facing use, cite the UM-MCI Core Semantic Package release (DOI: 10.5281/zenodo.19676079). Cite the companion repository or release when your work depends on its examples, scripts, templates, or contributed practical objects.
