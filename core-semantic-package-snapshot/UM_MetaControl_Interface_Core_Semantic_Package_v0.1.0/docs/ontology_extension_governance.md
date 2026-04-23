# Ontology extension governance

Layer 1 is intentionally conservative. Not every useful local addition belongs in the core ontology.

## Promote to Layer 1 only when all of the following are true

1. the concept recurs across multiple tasks or domains,
2. it is semantically stable rather than highly implementation-specific,
3. it is not better represented as a Layer-2 seed, local field, or example-level convention,
4. lacking it would materially hurt interoperability, auditability, or cross-run accumulation.

## Typical destinations for new ideas

- **Layer 1** — stable shared vocabulary items that many users need to mean the same way.
- **Layer 2** — starter defaults, edge families, or other governed seeds that may still evolve.
- **Companion / local runtime** — signatures, projection logic, implementation helpers, and corpus-specific conventions.

## Evidence expected for a Layer-1 promotion proposal

A good promotion proposal should show at least one of the following:
- repeated occurrence across retrospective cases,
- repeated failure or ambiguity caused by the concept being missing,
- clear inability to represent the concept cleanly using the existing ontology.

## Default stance

When in doubt, do **not** promote immediately. Keep the addition local or companion-level until recurrence and stability are better established.


## Promotion lifecycle

A recommended path for new recurrent ideas is:
1. keep the idea local or companion-level first,
2. record repeated evidence through examples, retrospectives, signatures, or learned-prior notes,
3. submit a governance proposal that cites that evidence,
4. let maintainers decide whether it should stay local, become a Layer-2 seed, or be promoted into Layer 1 in a future core release.

This keeps the public vocabulary stable while still allowing practical growth.

## Public vocabulary rule

Between released core versions, the public UM-MCI vocabulary should be treated as **read-only**. New local concepts may be used under `extensions` or companion-side practical objects, but they should not silently redefine released `UM.*` identifiers. Promotion into Layer 2 or Layer 1 should happen only through a later maintainer-curated core release.
