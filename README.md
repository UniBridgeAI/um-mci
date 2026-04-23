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
UM8 is the human-readable theory layer. It provides the high-level methodology architecture for comparing, combining, and designing major ways of solving complex problems before work becomes tied to specific tools, models, or domain defaults.

- [UM8 overview DOI](https://doi.org/10.5281/zenodo.18790203)

### UM-MCI Core Semantic Package
UM-MCI Core is the stable machine-readable layer aligned to that theory. It provides the shared semantic contract needed to represent, validate, compare, and reuse the higher-level organization of complex tasks across runs, systems, and reviewers.

- [UM-MCI Core Semantic Package DOI](https://doi.org/10.5281/zenodo.19676079)

### UM-MCI Practical Companion
The Practical Companion is the practical layer built around the Core. It provides worked examples, templates, utilities, and evolving workflow guidance for real use and contribution.

## What this repository contains

This repository contains:

- a **snapshot of the Core Semantic Package**
- the **Practical Companion**

The human-readable UM8 theory is published separately through its Zenodo records.

## When this repository is useful

This repository is most useful when a task is not exhausted by a single tool call or a standard procedure.

It matters most when:

- different high-level approaches could organize the same problem in different ways
- the overall approach changes what evidence matters, how progress is judged, and where revision begins
- long-horizon work requires explicit planning, revision, and reusable memory across runs
- success and failure should contribute experience that remains useful for future tasks

Routine tasks with a clear standard workflow usually do not require this full layer of representation and validation.

## Entry paths by purpose

Most users do not need to go through the whole ecosystem at once. Choose the smallest entry path that matches your immediate goal.

### 1. Understand how UM8 helps with complex problem solving and high-level method choice
Use this path when your goal is to understand how major ways of solving a problem can be compared before work is locked into specific tools, solvers, or domain defaults.

Start with the **UM8 overview** and one relevant **Compass module**.  
Move to **UM-MCI Core** only when the higher-level task structure needs machine-readable representation, validation, or reuse.

### 2. Connect an agent, workflow, or logger
Use this path when your goal is to support long-horizon planning, global planning, diagnosis, and the accumulation of reusable experience across runs.

Begin with **UM-MCI Core** and one minimal worked example from the **Practical Companion**.  
Consult the **UM8 overview** or a relevant **Compass module** whenever the higher-level organization of the task becomes unclear, contested, or in need of redesign.

### 3. Contribute shared methodological experience
Use this path when your goal is to let experience from different domains, teams, or agents land in the same public vocabulary so that it can be compared, audited, and reused.

Begin with the **Practical Companion**.  
Move to **UM-MCI Core** when stable vocabulary, validation boundaries, or canonical machine-readable structure become important.  
Return to the **UM8 overview** or a **Compass module** when the practical task requires deeper interpretation or redesign.

### 4. Maintain a release or controlled mirror
This path is for maintainers, release stewards, and downstream integrators. Use it when the goal is to validate, pin, or redistribute a controlled snapshot. Most users can skip this path.

## How to cite

Different parts of this repository correspond to different citable artifacts.

- **If you use the human-readable theoretical framework**, cite the [UM8 overview](https://doi.org/10.5281/zenodo.18790203) and the relevant Compass module.
- **If you use the stable machine-readable layer**, cite the [UM-MCI Core Semantic Package](https://doi.org/10.5281/zenodo.19676079).
- **If you use worked examples, templates, utilities, or other practical materials from this repository**, cite this GitHub repository or the relevant GitHub release.
- **If your work depends on both the theoretical framework and the Core package**, cite both.

This repository is an umbrella entry point across these layers. The theory records, the Core package, and the Practical Companion play different roles and may need to be cited separately depending on use.

## License

This repository is released under Apache-2.0 unless otherwise stated.
