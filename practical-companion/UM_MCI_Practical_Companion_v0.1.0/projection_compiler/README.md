# Projection compiler

This directory contains a small reference utility that compiles selected parts of the core Compass seed and default profiles into a task-facing projection.

It is intentionally not a full route-resolution engine. It does not resolve context, tensions, user confirmations, manual overrides, support-edge local settings, evidence, or validator escalation. Those belong to downstream runtime implementations.

The compiler traverses option trees recursively. It does not assume a fixed option-path depth.

## Minimal command

```bash
python projection_compiler/scripts/compile_projection.py \
  --core-root /path/to/UM_MetaControl_Interface_Core_Semantic_Package \
  --profile projection_compiler/profiles/planner_minimal.profile.json \
  --paradigm-id UM.PARADIGM.OPTIMIZATION \
  --output projection_compiler/compiled_examples/optimization.planner_minimal.json
```

## Inputs

- `--core-root`: path to the unpacked Core Semantic Package.
- `--profile`: projection profile JSON.
- `--paradigm-id`: paradigm to compile.
- `--output`: path for the compiled projection.

## Output

The output is an implementation-facing view derived from the core semantic seed. It is not a replacement for the core Compass seed or defaults.
