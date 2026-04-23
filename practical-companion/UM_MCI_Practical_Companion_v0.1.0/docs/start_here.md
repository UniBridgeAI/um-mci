# Start here: how the practical companion connects to the core

The **core** and the **practical companion** serve different roles.

## Core

The core is the stable semantic contract. It defines:
- paradigms,
- dimensions,
- Compass seeds,
- defaults,
- edge-family seeds,
- schemas for stage, meta-run, governance, context, and tension objects.

If you want to know what a route commitment **means**, the core is the source of truth.

## Practical companion

The practical companion is the working layer. It shows how to use the core through:
- valid examples,
- projection helpers,
- retrospective extraction templates,
- signature seeds,
- candidate route-prior notes,
- workspace validators.

If you want to know how to **work with** the core in practice, start here and then go to `docs/quickstart.md`.

## Minimal first-use path

1. In the unpacked core release, open `docs/theory_and_package_map.md` if you still need the theory-to-package bridge.
2. Unpack the pinned core release.
3. Run one command from the companion root:

```bash
python scripts/validate_workspace.py --core-root /path/to/UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0 --companion-root .
```

For ordinary contribution work, this command skips MANIFEST hash checks so changed local files do not fail validation for release-integrity reasons. For maintainer release checks, add `--release`.


4. Open one example stage record and one meta-run.
5. Only after that, move to projection, retrospective extraction, signatures, or candidate route priors.

## Dependency

```bash
pip install -r requirements-minimal.txt
```

For builders who need a one-page reversible bridge from theory labels to dimensions, option paths, and record fields, see `docs/mapping_shell.md` inside the unpacked core release.
