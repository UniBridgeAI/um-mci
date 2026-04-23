# Glossary

- **Paradigm**: One of the eight universal methodology anchors. A paradigm is a family of primary solution logic, not a discipline or research community.

- **Compass hierarchy**: The machine-readable organization of a paradigm into major axes, stable subdimensions, optional layer modules where applicable, and leaf option families.

- **Paradigm ontology**: The Layer-1 registry of the eight top-level paradigm anchors. Use this file when you need the stable public paradigm vocabulary.

- **Paradigm Compass seed**: The Layer-2 seed that mirrors the top-level paradigm anchors and then carries the internal Compass design space for each paradigm.

- **Dimension**: A stable methodological decision space inside a paradigm. Dimensions belong to the canonical ontology.

- **Option path**: A path through the Compass seed from a selected dimension to one or more option-family nodes and, when needed, to a leaf bullet family. Defaults and records use option paths when they need to commit below the stable dimension level.

- **Definition**: The main semantic sentence for a paradigm, dimension, or option. Definitions are the primary machine-readable meaning-bearing field.

- **Tag**: A short subtitle or mnemonic cue. Tags are expected for paradigms, dimensions, and stable option families when the human-facing framework supplies one. Leaf bullet options may omit tags when label plus definition is already sufficient.

- **Machine control**: A non-semantic execution or compilation control such as validation strictness or provenance mode. Machine controls are kept separate from the ontology itself.

- **Route**: The methodological organization of work at a chosen unit of analysis. In simple cases a route may be described by a base paradigm plus the relevant dimension commitments. Supporting paradigms remain paradigms; supporting **edge families** record how those paradigms concretely enter the machine-readable route at particular directed slots. In complex tasks the overall organization may be a **route graph** composed of linked stage-routes rather than a single flat route.

- **Stage**: The atomic unit of logging and learning in a meta-run. A stage is a local route instance together with its local goal, artifact/validation plan, stop conditions, tension transition, and outcome.

- **Edge slot**: A stable structural directed pair `row → column` derived from the Paradigm Interaction Matrix. The slot fixes the source paradigm, target paradigm, and direction; it does not by itself specify the mechanism.

- **Edge family**: The package-level governed interaction object attached to an edge slot. Records normally reference edge families, not raw theory phrases. Edge families are starter seeds, not a closed exhaustive set.

- **Relation role**: A coarse structural property of an edge family. Multiple edge families may share the same relation role because it names the broad class of cross-paradigm relation.

- **Operator family**: A finer mechanism property inside an edge family. It identifies the recurrent mechanism currently recognized at that directed slot.

- **Canonical operator pattern**: The theory-side recurrent pattern highlighted in Figure 2. In v0.1.0, many operator-family seeds are initialized from these theory-side patterns. Later releases may refine, split, merge, or add operator families through governance.

- **Operator family code**: A machine-stable uppercase token for the operator family. It is useful for indexing, lightweight feature construction, filenames, and rule tables when the human-readable `operator_family` string is too verbose.

- **Artifact type**: A coarse cross-paradigm category for work products or intermediate methodological outputs.

- **Validation primitive**: A cross-paradigm property-check vocabulary item such as preservation checking, admissibility checking, calibration checking, or provenance checking.

- **Operational tension**: An endogenous diagnostic belief about current pressure points in a run, such as ambiguity, uncertainty, evidence gap, inconsistency, tractability pressure, or horizon pressure. Operational tensions are assessed relative to the current route, artifacts, evidence, and context.

- **Governance context**: Normative or permission constraints such as risk, reversibility, audit requirements, and action permissions.

- **Affordance context**: Resource and environment conditions such as budget, tools, and non-stationarity. Affordance is distinct from governance.

- **Namespace registry**: The public naming contract for the Core Semantic Package. IDs registered there are part of the canonical shared vocabulary. Unregistered additions may still be locally useful, but they are provisional rather than public-core canonical.

- **Starter default**: A defeasible initial bundle for a paradigm. It is meant to reduce first-move ambiguity, not to fix the final route in advance.

- **Manifest**: The archive inventory for a release. It lists the files that belong to the release together with size and SHA256 checksum values so a downstream user can verify that the package was unpacked intact and has not been silently altered.

- **SHA256 checksum**: A file fingerprint used to verify release integrity.


## Container dimension vs selectable dimension

Some Layer-1 dimensions are composite container nodes whose main role is to preserve the human Compass structure. Downstream records usually resolve the selectable subdimensions beneath them. Use `hierarchy_role` and `parent_dimension_id` rather than label similarity to distinguish these layers.
