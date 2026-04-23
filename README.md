# UM-MCI

UM-MCI supports global planning and meta-control for agents tackling complex, long-horizon tasks, reducing costly strategic mistakes and blind trial-and-error search.

This repository is part of the broader **Universal Methodology ecosystem**. It brings together a snapshot of **UM-MCI Core** and the evolving **UM-MCI Practical Companion**. The UM8 theoretical framework and the released Compass modules are published separately.

## The Universal Methodology ecosystem

The broader Universal Methodology ecosystem consists of four connected layers:

- the **UM8 theoretical framework**
- the **Paradigm Compass modules**
- the **UM-MCI Core Semantic Package**
- the **UM-MCI Practical Companion**

These layers serve different purposes.

### UM8 theoretical framework
UM8 supports higher-level planning and design in complex problem solving. It identifies and consolidates recurrent solution logics abstracted from lower-level methods across disciplines into a compact, stable space for comparison and design.

It organizes complex problem solving into eight recurrent methodological paradigms: **Transformation, Optimization, Probabilistic, Inversion, Rule, Fusion, Simulation, and Evolutionary**. The UM8 overview places these paradigms in a common comparative space and makes their interaction structure visible before work becomes tied to specific tools, models, or domain defaults.

- [UM8 overview DOI](https://doi.org/10.5281/zenodo.18790203)

### Paradigm Compass modules
The Compass modules open the internal design space of the UM8 paradigms. Each module makes explicit the major axes and design commitments that shape how one paradigm should be configured before implementation begins.

The full set of released Compass modules is linked from the UM8 overview record.

### UM-MCI Core Semantic Package
UM-MCI Core is the stable machine-readable layer aligned to the UM8 theoretical framework. It provides the shared semantic contract required to represent, validate, compare, and reuse the higher-level organization of complex tasks across runs, systems, and human review.

- [UM-MCI Core Semantic Package DOI](https://doi.org/10.5281/zenodo.19676079)

### UM-MCI Practical Companion
The Practical Companion is the evolving practical layer built around the Core. It provides worked examples, templates, utilities, and contribution workflows for practical use and shared experience accumulation.

## When this repository is useful

Use this repository when a task contains a real methodological decision to learn from.

It is most useful when:

- the task has genuine route ambiguity, not merely an information gap
- different ways of organizing the work would change the evidence, artifacts, validators, or trade-offs involved
- the key decision cannot be reduced to a single tool call or an ordinary retrieval step
- the organization of the method is a material part of success or failure
- success and failure should contribute reusable experience for future tasks

Routine work with a clear standard procedure usually requires only ordinary execution traces.

## Entry paths by purpose

Most users do not need to go through the whole ecosystem at once. Choose the smallest entry path that matches your immediate objective.

### 1. Understand how UM8 supports high-level methodological comparison and task design
Choose this path when the goal is to understand how complex problems can be framed, compared, and designed at a higher methodological level before lower-level implementation choices begin to dominate the work.

Begin with the **UM8 overview** and one relevant **Compass module**.  
Move to **UM-MCI Core** only when the resulting task structure needs machine-readable representation, validation, or reuse.

### 2. Connect an agentic system, workflow, or logger
Choose this path when the goal is to support long-horizon planning, route diagnosis, policy learning, and reusable experience across runs in an agentic system.

Begin with **UM-MCI Core** and one minimal worked example from the **Practical Companion**.  
Consult the **UM8 overview** or a relevant **Compass module** whenever the higher-level organization of the task becomes unclear, contested, or in need of redesign.

### 3. Contribute reusable methodological experience
Choose this path when the goal is to contribute methodological experience in a form that can be compared, audited, and reused across domains, teams, or agents.

Begin with the **Practical Companion**.  
Move to **UM-MCI Core** when stable vocabulary, validation boundaries, or canonical machine-readable structure become important.  
Return to the **UM8 overview** or a relevant **Compass module** when the practical case requires deeper interpretation or redesign.

## How to cite

Different parts of this repository correspond to different citable artifacts.

- **If you use the UM8 theoretical framework**, cite the [UM8 overview](https://doi.org/10.5281/zenodo.18790203).
- **If you use a Paradigm Compass module**, cite the relevant Compass module DOI. The released Compass modules are linked from the UM8 overview record.
- **If you use the stable machine-readable layer**, cite the [UM-MCI Core Semantic Package](https://doi.org/10.5281/zenodo.19676079).
- **If you use worked examples, templates, utilities, or other practical materials from this repository**, cite this GitHub repository or the relevant GitHub release.
- **If your work depends on both the theoretical framework and the Core package**, cite both.

This repository serves as an umbrella entry point across these layers. The theory, the Core package, and the Practical Companion play different roles and may need to be cited separately depending on use.

## License

This repository is released under Apache-2.0 unless otherwise stated.
