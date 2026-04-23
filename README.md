# UM-MCI

This package supports global planning and meta-control for AI agents tackling complex, long-horizon tasks, reducing costly strategic mistakes and blind trial-and-error search.

This repository is part of the broader **Universal Methodology ecosystem**. It brings together a snapshot of **UM-MCI Core Semantic Package** and the evolving **UM-MCI Practical Companion**. The human-readable **UM8** theory is published separately.

## The Universal Methodology ecosystem

The broader **Universal Methodology ecosystem** currently has three connected layers:

- **UM8**, the human-readable theoretical framework
- **UM-MCI Core Semantic Package**, the stable machine-readable semantic package
- **UM-MCI Practical Companion**, the practical layer of examples, templates, and workflow guidance

These layers serve different purposes.

### UM8 theoretical framework
UM8 is the human-readable theory layer. It provides the high-level methodology architecture for comparing, combining, and designing high-level methdological routes for complex problem solving before work becomes tied to specific tools, models, or domain defaults.

- [UM8 overview DOI](https://doi.org/10.5281/zenodo.18790203)

### UM-MCI Core Semantic Package
UM-MCI Core operationalizes the UM8 theoretical framework in machine-readable form. It provides the stable semantic contract needed to represent, validate, compare, and reuse methodological routes across runs, systems, and human review.

- [UM-MCI Core Semantic Package DOI](https://doi.org/10.5281/zenodo.19676079)

### UM-MCI Practical Companion
UM-MCI Practical Companion is the evolving practical layer built around the released Core package. It provides worked examples, templates, utilities, and contribution workflows that help users learn the core quickly, apply it in real tasks, and extend it through shared practical experience.

## What this repository contains

This repository contains:

- a **snapshot of the Core Semantic Package**
- the **Practical Companion**

The human-readable UM8 theory is published separately through its Zenodo records.

## When this repository is useful

Use this repository when a task contains a real methodological decision to learn from.

It is most useful when:

- the task has genuine route ambiguity, not merely an information gap
- different ways of organizing the work would change the evidence, artifacts, validators, or trade-offs involved
- the key decision cannot be reduced to a single tool call or an ordinary retrieval step
- the organization of the method is a material part of success or failure
- the run should contribute reusable experience for future tasks

Routine work with a clear standard procedure usually does not require this full layer of explicit representation and validation. In such cases, ordinary execution traces are often sufficient.

## Entry paths by purpose

The appropriate entry path depends on the user’s immediate objective. Most users do not need to traverse the whole ecosystem at once.

### 1. Theoretical understanding and high-level route design
Choose this path when the immediate goal is to understand how UM8 supports complex problem solving before work becomes tied to particular tools, solvers, or domain defaults.

Begin with the **UM8 overview** and one relevant **Compass module**.  
Move to **UM-MCI Core** only when the resulting task structure needs machine-readable representation, validation, or reuse.

### 2. Agent and workflow integration
Choose this path when the immediate goal is to incorporate route-aware planning, logging, validation, or review into an agentic system, workflow, or evaluation pipeline.

Begin with **UM-MCI Core** and one minimal worked example from the **Practical Companion**.  
Consult the **UM8 overview** or a relevant **Compass module** whenever the higher-level organization of the task becomes unclear, contested, or in need of redesign.

### 3. Contribution of reusable methodological experience
Choose this path when the immediate goal is to make experience from different domains, teams, or agents comparable and reusable within a shared public vocabulary.

Begin with the **Practical Companion**.  
Move to **UM-MCI Core** when stable vocabulary, validation boundaries, or canonical machine-readable structure become necessary.  
Return to the **UM8 overview** or a relevant **Compass module** when the practical case requires deeper interpretation or redesign.

## How to cite

Different parts of this repository correspond to different citable artifacts.

- **If you use the human-readable theoretical framework**, cite the [UM8 overview](https://doi.org/10.5281/zenodo.18790203) and the relevant Compass module.
- **If you use the stable machine-readable layer**, cite the [UM-MCI Core Semantic Package](https://doi.org/10.5281/zenodo.19676079).
- **If you use worked examples, templates, utilities, or other practical materials from this repository**, cite this GitHub repository or the relevant GitHub release.
- **If your work depends on both the theoretical framework and the Core package**, cite both.

This repository is an umbrella entry point across these layers. The theory records, the Core package, and the Practical Companion play different roles and may need to be cited separately depending on use.

## License

This repository is released under Apache-2.0 unless otherwise stated.
