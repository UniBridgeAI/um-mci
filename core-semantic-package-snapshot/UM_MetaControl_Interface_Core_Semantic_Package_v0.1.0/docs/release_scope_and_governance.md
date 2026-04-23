# Release scope and governance

This core package is the **slow-changing semantic core** of UM-MCI.

## Included in the Core Semantic Package

- Layer-1 ontology files that define the public semantic vocabulary.
- Layer-2 Compass seeds, paradigm defaults, and edge-family seeds.
- Schemas for all canonical Layer-1 registries, all included Layer-2 seeds, and the context / record objects needed for route logging.
- Minimal explanatory documentation needed to interpret the package consistently.
- A lightweight validation helper for checking the semantic integrity of the core release itself.

## Excluded from the Core Semantic Package

The following materials are intentionally excluded because they are expected to evolve faster, to be corpus-dependent, or to depend strongly on downstream implementation choices:

- runtime projections,
- recognizer/signature libraries,
- examples and notebooks,
- implementation references,
- training code and learned policies,
- internal revision logs,
- practical logging/overhead playbooks.

These belong in a GitHub practical companion repository or another faster-moving distribution layer.

## Governance principle

- **Layer 1** changes slowly and only when a stable semantic need is demonstrated.
- **Layer 2** is a governed seed layer: it may expand, be corrected, or be refined across releases.
- Downstream local additions that are not registered in the Layer-1 namespace file should be treated as provisional rather than canonical.
- Defaults and edge families are starter content. They are intentionally defeasible and may be revised by downstream users or later governed releases.

## Semantic source order

For core use, the intended semantic order is:

1. `um_paradigms_ontology` — top-level methodology anchors.
2. `um_dimensions_ontology` — stable methodological decision spaces.
3. `um_paradigm_compass_seed` — paradigm-internal value spaces, option families, and leaf bullet families.
4. `um_paradigm_defaults_seed` — conservative starter commitments expressed against those dimensions and option paths.
5. records — concrete realized route commitments, outcomes, and revisions.

This ordering is important because defaults do not replace the Compass; they are only one governed entry route into it.

## Core–companion validation split

The Core Semantic Package includes its own integrity validator for Layer-1 / Layer-2 structure and cross-file semantic consistency. The GitHub practical companion performs additional validation for examples, retrospective cases, and recognizer/signature seeds against a pinned core release.

Companion materials may evolve on a faster cadence than the Core Semantic Package. Users who combine them should pin the core release and the companion release separately rather than assume automatic synchronization.

See `docs/ontology_extension_governance.md` for the criteria used when deciding whether a new term belongs in Layer 1, Layer 2, or only in companion/local runtime layers.


## Local extensions

The core package is intentionally conservative. If downstream teams need local fields in records, they should place them under an `extensions` object and namespace them by team, vendor, or project. Local extensions should not be promoted into the Layer-1 ontology unless they become cross-team, semantically stable, and necessary for interoperability or audit.


## Shared public vocabulary rule

To keep cross-domain experience comparable, downstream users should treat the released Layer-1 / Layer-2 IDs as the **shared public vocabulary** for that core version. Between released core versions, this public vocabulary should be treated as **read-only**.

- Do **not** silently rewrite public IDs in local copies if the goal is later sharing.
- Put local, unreviewed additions under `extensions` or keep them in companion-level notes.
- Do not mint new `UM.*` identifiers in local companion work.
- Promote recurrent patterns only through governed proposals and a later maintainer-curated core release.
