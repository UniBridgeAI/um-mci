# Core–companion handshake

Use the Zenodo core as the **semantic contract** and the practical companion as the **working layer**.

## Core answers
- what the public IDs mean,
- what dimensions and option paths exist,
- what defaults, edge families, artifacts, validators, tensions, and contexts can be referenced.

## Practical companion answers
- how to validate examples against the core,
- how to derive task-facing projections,
- how to reconstruct retrospective cases,
- how to experiment with recognizer/signature seeds.

## Version handshake

A companion example should pin the core release it expects through `package_version_pin`.
The companion validator checks that the pinned core version matches the core release actually supplied at validation time.

## Recommended repository pattern

A single public GitHub repository may contain both:
- `core_snapshot/` — a pinned mirror of the released core,
- `companion/` — the faster-moving practical layer.

That gives users one workspace while preserving a clean citation boundary: cite the Zenodo core; use GitHub for practical workflows.


## Future learned triggers and recovery hints

The core does not try to hard-code fine-grained trigger rules or failure-policy priors. Those belong in the practical layer, where they can begin as route-prior notes and later mature into stronger empirical guidance.


For a builder-facing crosswalk from theory labels to dimension IDs, option paths, and record fields, see `docs/mapping_shell.md` inside the unpacked core release.
