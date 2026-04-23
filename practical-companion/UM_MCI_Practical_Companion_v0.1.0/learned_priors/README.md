# Candidate route-prior notes

This directory is a **community-level scaffold** for accumulating candidate route-prior notes about route choice, option-path triggers, failure signals, and recovery hints.

These notes are not part of the stable Core Semantic Package. They are practical, revisable, and should be treated as **candidate route priors** unless they explicitly document stronger evidence. In v0.1.0, most shared notes should be read as heuristic or early empirical route suggestions, not as verified learned priors.

Typical uses:
- trigger cues for when a paradigm or option path is promising
- common failure signals and fallback actions
- recurring tension/context patterns associated with useful route choices
- retrospective summaries that later motivate edge-family or default revisions

You can validate starter and contributed route-prior notes with `scripts/validate_route_prior_notes.py`.

To remain globally shareable, prior notes should reference the released core IDs rather than local replacement vocabularies. Local-only annotations should go under `extensions`. Recurrent patterns that seem stable enough for wider adoption should be escalated through a governance proposal rather than by silently editing the public vocabulary.

## Evidence standard for status labels

Use prior-note status conservatively:

- `heuristic` — a plausible route suggestion based on one case, expert judgment, or early retrospective evidence. It is **not** a learned prior.
- `empirical` — a recurring association observed across multiple traceable and preferably independent cases. It supports a route suggestion, not a causal effect estimate.
- `learned` — reserved for priors produced by an explicit learning process. A learned note should identify the input corpus or logs, sample size, independence assumptions, training/retrieval/statistical method, validation or holdout procedure where applicable, failure or false-positive assessment, and confidence basis.
- `deprecated` — a prior retained for traceability after contradiction, replacement, scope failure, or a superseding prior.

A route-prior note may suggest what to try first. It should not be read as an effect estimate unless the evidence explicitly supports comparison against alternatives.

The status is a governance aid, not a claim of final truth.

## Confidence

For `heuristic` notes, `confidence` is author-assessed unless a calibration method is explicitly documented. It should not be interpreted as a calibrated probability.

For `empirical` notes, confidence should be linked to the number and independence of supporting cases, the presence of counterexamples, and the quality of retrospective extraction.

For `learned` notes, confidence should cite the learning or evaluation procedure that produced it. If no such procedure is documented, do not treat the value as a calibrated probability.

## Evidence kind

`case_based` means the prior is grounded in concrete case records, which may include stage records, meta-runs, and retrospective case objects from the same case family. Use `mixed` when evidence combines clearly different evidence families, such as case records plus learned-from-logs outputs.

Evidence refs should directly support the recommended commitment. If a prior note recommends a specific option path or supporting edge family, its cited evidence should point to cases, stage records, or meta-runs that actually instantiate that pattern.

## External DOI and URL refs

External evidence references may be written as `doi:10.xxxx/...`, `https://doi.org/10.xxxx/...`, another URL, or a bare DOI beginning with `10.` such as `10.5281/zenodo.xxxxx`. Bare DOI strings are treated as external evidence by the companion validators.

## Template caution

`templates/route_prior_note.template.json` is structurally valid and intentionally illustrative. Before submitting a new prior note, replace all UM IDs, option paths, trigger cues, evidence refs, confidence values, and notes so they describe your own case. If you want a purely local draft, keep it outside `starter_notes/` and `contributed_notes/` until it satisfies the shared-object minimums.

## Directory layout

- `starter_notes/` — maintainer-provided starter notes.
- `contributed_notes/` — community notes under review.
- `templates/` — blank or illustrative templates.

The workspace validator scans both `starter_notes/` and `contributed_notes/`.

## Scope values

Use the narrowest scope that fits the prior:

- `paradigm` — the prior concerns whether a paradigm is likely to be useful.
- `edge_family` — the prior concerns a supporting relation between paradigms.
- `option_path` — the prior concerns one specific Compass option path under one dimension.
- `route_pattern` — the prior concerns a recurring bundle of multiple dimension selections and/or supporting edge families.

Use `route_pattern` when the prior recommends a combination such as lookahead planning + simulation-based evaluation + receding horizon + Simulation → Optimization support.

## Evidence counts and weak alignment

For shared prior notes, distinguish evidence objects from independent cases:

- `evidence_object_count` counts the number of cited evidence objects, such as a stage record and a meta-run record. In this first companion release, it is expected to equal the number of listed `evidence_refs`; future releases may distinguish evidence references from the number of internal evidence objects contained in an aggregate corpus, benchmark, DOI record, or log bundle.
- `independent_case_count` estimates how many independent tasks, domains, teams, or case families are represented. For `case_based`, `retrospective`, or `mixed` evidence with local evidence references, it should be at least 1.
- Legacy `support_count`, if present in older notes, is optional and should not be read as an independent-case count unless explicitly stated. New notes should prefer `evidence_object_count` and `independent_case_count`.

The evidence-alignment check is a weak mechanical check. It verifies that at least one recommended option path or supporting edge family appears in local evidence. It does **not** certify evidential sufficiency, causality, or generalizability.

If evidence is external and cannot be mechanically parsed by the companion validators, mark that limitation in `notes` or `extensions` and expect maintainer review before promotion.

## External-only evidence

If a shared prior note cites only external evidence, such as a DOI, URL, external benchmark, or off-repository log bundle, the companion validator cannot mechanically parse that evidence for selected option paths or supporting edge families. In that case, explicitly mark the limitation in `notes` or in `extensions.evidence_review.external_evidence_unchecked = true`. Passing validation then means that the note is structurally and vocabulary-aligned, not that the external evidence has been independently checked by the validator.
