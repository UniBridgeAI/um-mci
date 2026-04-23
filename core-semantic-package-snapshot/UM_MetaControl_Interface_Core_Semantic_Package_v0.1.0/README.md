# Universal Methodology Meta-Control Interface (UM-MCI) Core Semantic Package

UM-MCI Core Semantic Package is a compact, machine-readable semantic package for route-level methodological planning and meta-control. It is grounded in the Eight Universal Methodology Paradigms (UM8), the Paradigm Interaction Matrix, and the eight paradigm Compass modules.

The Core Semantic Package provides a shared language for methodological route representation, validation, comparison, diagnosis, and later route-level learning. It is designed for situations where methodological structure must be represented, validated, compared, or integrated into agent systems, workflow logs, or reproducible research infrastructure.

## Where to start

| Your purpose | Why this path matters | Start here |
|---|---|---|
| Understand how UM8 helps with complex problem-solving or method-route choice | UM8 helps compare high-level methodological routes before committing to a solver, tool, or domain default. | Start with the UM8 theoretical overview: https://doi.org/10.5281/zenodo.18790203. Then open the relevant Compass module linked from that record. Use this package only when you need the machine-readable layer. |
| Use UM-MCI in an agent, workflow, logger, or reproducible system | UM-MCI provides a stable methodological vocabulary for long-horizon planning, global planning, meta-control, route diagnosis, meta-policy learning, and reusable soft-prior accumulation. | Use this package as the stable semantic contract. For onboarding examples and workflow templates, use the UM-MCI Practical Companion when its GitHub release is available. |
| Contribute shared methodological experience | Experience from different domains, teams, or agents becomes more useful when it lands in the same public vocabulary and can be compared, audited, and reused. | Use the Practical Companion contribution workflow when available. Do not add replacement `UM.*` vocabulary directly to this core package. |
| Maintain or redistribute a controlled release | This path is for the package owner, release steward, or downstream integrator who pins and redistributes a controlled snapshot. | Use `docs/core_validation.md`, `docs/manifest_and_release_integrity.md`, and `docs/release_scope_and_governance.md`. Most users can skip this path. |

## Relationship to the theory and companion layers

- **UM8 theoretical records** explain the methodology framework, the eight paradigm anchors, the Paradigm Interaction Matrix, and the paradigm-specific Compass modules.
- **UM-MCI Core Semantic Package** translates that theory layer into a stable machine-readable vocabulary, schema contract, Compass-aligned seed layer, and release-integrity package.
- **UM-MCI Practical Companion** is the faster-moving GitHub layer for examples, templates, projection utilities, retrospective extraction workflows, signature seeds, candidate route-prior notes, and contribution scaffolding.

## What this package contains

- **Layer 1 ontology**: paradigms, Compass-aligned dimensions, machine controls, edge slots, artifact types, validation primitives, operational tensions, context vocabularies, and namespaces.
- **Layer 2 seeds**: full Compass seeds for each paradigm, starter defaults expressed against canonical dimensions and Compass option paths, and cross-paradigm edge-family seeds.
- **Schemas**: validation schemas for registries, seeds, context instances, tension-belief instances, stage records, meta-run records, and governance proposals.
- **Documentation**: theory-to-package mapping, terminology, defaults and validation usage, stage guidance, edge-family governance, ontology governance, and release integrity.
- **Release tools**: core semantic validator, manifest generator, and strict manifest verifier.

## Core self-validation

Run these commands from the unpacked package root.

```bash
python scripts/validate_core_package.py --core-root .
```

This validates the JSON files against their schemas and checks cross-file semantic consistency: registered IDs, selected option paths, edge-family references, defaults, and related package constraints.

```bash
python scripts/verify_manifest_hashes.py --core-root . --strict
```

This verifies the release inventory: every file listed in `MANIFEST.json` must match its recorded size and SHA256 hash, and strict mode checks that the release tree does not contain unexpected files such as generated caches.

If any file is edited after release preparation, regenerate the manifest before strict verification:

```bash
python scripts/generate_manifest.py --root . \
  --package-version 0.1.0 \
  --archive-root UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0
```

## Citation and license

This package is licensed under **Apache-2.0**. The full license text is in `LICENSE`.

For scholarly, research, or public-facing use, cite the specific package release using `CITATION.cff`.

Specific version DOI for this release:

```text
10.5281/zenodo.19676079
```

Human-oriented UM8 theory records and Compass descriptions are separate scholarly records and may have their own DOI-level licenses.

## Version

```text
0.1.0
```
