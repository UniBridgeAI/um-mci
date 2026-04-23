# Core validation

This package includes `scripts/validate_core_package.py`.

## What it checks

The validator performs two classes of checks:

1. **Schema checks**
   - validates included Layer-1 registries against their schemas,
   - validates included Layer-2 seeds against their schemas.

2. **Cross-file semantic checks**
   - confirms that default `dimension_id` values resolve to registered dimensions,
   - confirms that default `selected_option_paths` resolve inside the Compass seed,
   - confirms that machine controls, control values, artifact IDs, validation primitive IDs, edge-slot IDs, and support edge IDs referenced by defaults or edge families exist,
   - confirms that release-governed `selection_constraints` are actually satisfied by starter defaults,
   - confirms that the top-level paradigm anchors in `um_paradigms_ontology` and `um_paradigm_compass_seed` remain aligned.

## Why this matters

The Core Semantic Package is a semantic package. JSON Schema validates structure, but some semantic integrity checks are necessarily cross-file. This helper is included so the core can validate itself without depending on companion tooling.

## Usage

Install the minimal validation dependency if needed:

```bash
pip install -r requirements-minimal.txt
```

Then run:

```bash
python scripts/validate_core_package.py --core-root .
```

