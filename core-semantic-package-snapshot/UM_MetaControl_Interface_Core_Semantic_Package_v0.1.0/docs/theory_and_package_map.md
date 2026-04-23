# Theory resources and package mapping

UM-MCI is easiest to understand when the **theoretical framework layer** and the **machine-readable package layer** are read together.

## Read order for a new theory reader

1. **UM8 overview framework** — always read this first to understand the eight paradigm anchors and the middle-level abstraction.
2. **One relevant Compass module** — read next when you are working within a candidate paradigm and need its internal design space.
3. **Paradigm Interaction Matrix** — open when one paradigm is insufficient, or when you need cross-paradigm composition.
4. **Core Semantic Package** — use when you need the machine-readable ontology, seeds, and record schemas.
5. **GitHub practical companion** — use when you need examples, projection, retrospective extraction, signatures, or shared priors.

## The nine theoretical framework resources

The links below are used as **navigation pointers** to the theoretical framework layer. They are not package-version citations. Where a stable concept DOI is curated, prefer it for family-level navigation; otherwise the current public theory landing reference is used until the concept-DOI map is finalized. For reproducibility claims about a specific theory snapshot, use the corresponding specific version DOI.


### Top-level overview
- **Eight Universal Methodology Paradigms (UM8)** — concept DOI / stable theory landing: https://doi.org/10.5281/zenodo.18790203
  - Human role: the top-level framework; introduces the eight paradigm anchors, their trigger cues, and the interaction matrix as the first composition layer.
  - Package mapping:
    - `layer1_ontology/um_paradigms_ontology.v1.json`
    - `layer1_ontology/um_dimensions_ontology.v1.json`
    - `layer1_ontology/um_edge_slots_ontology.v1.json`
    - `layer2_seed/um_edge_families_seed.v1.json`

### Paradigm-specific Compass modules
- **Optimization Compass** — https://doi.org/10.5281/zenodo.19451866
- **Transformation Compass** — https://doi.org/10.5281/zenodo.19351919
- **Evolutionary Compass** — https://doi.org/10.5281/zenodo.19250879
- **Rule Compass** — https://doi.org/10.5281/zenodo.19152305
- **Inversion Compass** — https://doi.org/10.5281/zenodo.19109098
- **Probabilistic Compass** — https://doi.org/10.5281/zenodo.19032968
- **Fusion Compass** — https://doi.org/10.5281/zenodo.18962806
- **Simulation Compass** — https://doi.org/10.5281/zenodo.18903246

For all eight Compass modules, the main machine-readable counterpart in this package is:
- `layer2_seed/um_paradigm_compass_seed.v1.json`

The corresponding starter-route layer is:
- `layer2_seed/um_paradigm_defaults_seed.v1.json`

## How the theory appears in the package

### 1. UM8 overview
The top-level human framework appears in the package as:
- the **paradigm registry**,
- the **stable dimension ontology**,
- the **namespace contract**,
- the **glossary and release docs**.

### 2. Paradigm Interaction Matrix
The interaction matrix appears in the package as:
- `um_edge_slots_ontology.v1.json` — the directed structural slot layer,
- `um_edge_families_seed.v1.json` — the governed starter operator-family layer.

### 3. Eight Compass modules
Each Compass appears as:
- a subtree in `um_paradigm_compass_seed.v1.json`,
- starter bundles in `um_paradigm_defaults_seed.v1.json`,
- dimension anchors in `um_dimensions_ontology.v1.json`.

## Why the PDFs are not embedded in this package

The theory resources live as separate Zenodo records with their own citation metadata. This package links to those records as the theory layer and keeps the machine-readable release compact.


## Where the theoretical framework should live

The canonical theoretical framework resources should remain on Zenodo, where they already have their own stable records and citation metadata. GitHub may host optional convenience mirrors or pointers, but the package should treat the Zenodo records as the authoritative theory source.


## DOI usage for theory references

When a theory record has both a **concept DOI** and a **specific version DOI**, use them for different purposes:
- use the **concept DOI** (or stable Zenodo landing page) for durable navigation across versions,
- use the **specific version DOI** when exact reproducibility matters.

This package treats the Zenodo theory records as the canonical theory source.

## Builder crosswalk / mapping shell

For builders who need to traverse the alignment rather than merely trust it, see `docs/mapping_shell.md`. It gives a one-page crosswalk from the theory layer to Layer-1 dimensions, Layer-2 option values, and record-level fields.

## Concept DOI / landing-page policy

In these theory maps, links are used as **navigation pointers** to the canonical theoretical framework layer. When a concept DOI or stable landing page is available and curated, prefer it for family-level navigation. When exact reproducibility of a theory snapshot matters, use the corresponding specific version DOI in the relevant publication or release note rather than treating this map as the citation source.
