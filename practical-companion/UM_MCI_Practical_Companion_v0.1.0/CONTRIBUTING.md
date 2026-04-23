# Contributing to the UM-MCI Practical Companion

This repository is designed to accumulate **shared practical experience** around the UM-MCI core across domains, teams, and agent workflows.

## Contribution license and material restrictions

Unless explicitly stated otherwise before acceptance, all contributions to this repository are submitted under the **Apache License, Version 2.0**.

By contributing, you represent that you have the right to submit the contribution under Apache-2.0. Do **not** submit confidential, private, proprietary, personal, restricted, third-party, or non-redistributable material, including private logs, PII, internal company code, unauthorized datasets, or copied code that you are not entitled to license.

Contributed examples, retrospective cases, signature seeds, candidate route-prior notes, governance proposals, schemas, and code may be indexed, retrieved, aggregated, evaluated, and used for machine-assisted or automated analysis of methodological patterns and route priors, subject to the repository license and governance policy.

## What kinds of contributions belong here

- new worked examples
- retrospective extraction cases
- signature seeds and recognizer hints
- candidate route-prior notes (heuristic, empirical, or explicitly learned route suggestions)
- integration helpers and audit workflows
- documentation improvements for onboarding or logging discipline


Important wording discipline: `learned_priors/` is the directory name, but not every note in that directory is a learned prior. Most early contributions should be described as **candidate route-prior notes** or **heuristic / empirical route-prior notes** unless they meet the evidence standard for `learned` status.

## What does not belong here

- changes to the stable Layer-1 ontology without a governance proposal
- project-private secrets, proprietary datasets, or non-redistributable code
- ad hoc fields added directly to core-compatible records without namespaced extensions

## Extension rule

If you need local fields in records, place them under an `extensions` object and namespace them by team, vendor, or project.

## Review expectations

Contributors should explain:
1. what the contribution is,
2. which core release it targets,
3. what evidence supports it,
4. whether it is heuristic, empirical, or learned,
5. whether it should remain companion-only or motivate a future governance proposal.


## Do not fork the public vocabulary casually

If you want your contribution to remain globally shareable, do not create ad hoc replacements for released core IDs. Use the pinned core vocabulary and put project-specific additions under `extensions`. If a missing concept keeps recurring, open a governance proposal instead of silently redefining the public language.

## Local ID style

Use stable, readable local IDs for companion-only objects. A simple policy is:
- keep released `UM.*` IDs unchanged,
- use `companion.<object_type>.<slug>` for companion-local records such as candidate route-prior notes or proposals,
- keep signature IDs under a distinct local prefix such as `SIG.`.

Do not mint new `UM.*` IDs in the companion. If a missing concept seems recurrent, submit a governance proposal instead.


## Shared-object minimums

Shared companion objects are expected to be more specific than a local draft:

- **Candidate route-prior notes** should cite direct evidence, state a concrete recommended commitment, prefer `evidence_object_count` and `independent_case_count`, and treat legacy `support_count` as optional. Do not label a note as `learned` unless it documents the learning process, input corpus or logs, validation method, failure/false-positive assessment, and confidence basis.
- **Signature seeds** should identify both `stage_pattern.base_paradigm_id` and `stage_pattern.supporting_paradigm_id`, and include at least one dimension, artifact, or validation hint.
- **Governance proposals** should point to directly relevant evidence and state the requested action explicitly.
- **Shared stage records** with supporting edge instances should include `edge_role_in_stage` so readers can distinguish incoming support from outgoing preparation.
