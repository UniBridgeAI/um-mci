# Edge-family governance

Edge families are governed starter seeds for cross-paradigm interaction.

## Terminology policy

For most user-facing documentation, say **edge family**. The other terms explain properties or provenance of that object.

- **Edge slot** = the stable directed structural slot from the Paradigm Interaction Matrix, such as `Simulation → Optimization`. It fixes the two paradigms and direction, but not the mechanism.
- **Edge family** = the governed package-level interaction object attached to an edge slot. This is the object that records normally reference.
- **Relation role** = a coarse structural property of an edge family. Many edge families may share the same relation role, because it names the broad kind of cross-paradigm relation.
- **Operator family** = the finer mechanism property inside an edge family. It specifies the recurrent mechanism currently recognized for that directed slot.
- **Canonical operator pattern** = the theory-side recurrent pattern highlighted in Figure 2 of the UM8 theoretical overview / Paradigm Interaction Matrix. In v0.1.0, many operator-family seeds are initialized from these theory-side patterns; later releases may refine, split, merge, or add operator families through governance.

A compact example:

- edge slot: `Simulation → Optimization`
- edge family: the governed package object for that slot
- relation role: a broad class such as scenario evaluation
- operator family: a more specific mechanism such as simulation-in-the-loop evaluation for optimizing decisions
- canonical operator pattern: the corresponding theory-side pattern shown in the Interaction Matrix

In short: `relation_role` and `operator_family` are properties of the **edge family** object. `canonical operator pattern` records the theory-to-package mapping and seed provenance.

## What an edge family means

An edge family states a recurrent **cross-paradigm operator role** through which one paradigm can enter another at a directed edge slot.

Two levels should be kept distinct:

- `relation_role` = a **coarse structural class** for the interaction; it is governed and revisable across releases rather than a closed exhaustive inventory.
- `operator_family` = the more specific recurrent mechanism family at that slot; it is a seed-level recurrent pattern, not a closed complete catalog.

A simple way to read this distinction is:
- `relation_role` tells you the broad kind of cross-paradigm move,
- `operator_family` tells you the more specific recurrent mechanism seed currently recognized at that slot,
- `operator_family_code` provides a compact machine-stable token for indexing and rule tables.

It does **not** claim that:

- the family is exhaustive,
- the requires/provides artifact contract is universally sufficient,
- the default validation bundle is always adequate in every task.

Those fields are seed-level expectations intended to help downstream users start from a coherent contract.

## When a downstream user needs more

If a downstream user encounters a new interaction pattern that is not well captured by an existing family, they may:

1. record the local interaction in their own runtime layer,
2. keep the original edge slot,
3. define a provisional local family or operator,
4. submit a governance proposal for promotion in a later release.

## Why recognizer/signature libraries are excluded here

Recognizer libraries can grow quickly as tasks, corpora, and local implementation practices expand. They are useful in practice, but they are not necessary for publishing the stable Core Semantic Package. They belong more naturally in a GitHub practical companion layer.

## Release discipline

Later releases may revise `relation_role` or introduce new operator families when recurring interaction patterns justify it. Many edge families may share the same relation role. Such changes belong to release governance rather than runtime drift.
