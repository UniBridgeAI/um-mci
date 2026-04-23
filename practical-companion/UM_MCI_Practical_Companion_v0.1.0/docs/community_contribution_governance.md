# Community contribution and governance

A shared GitHub repository can accumulate cross-domain practical experience **if contributors write against the same public vocabulary and the same governance rules**.

## Why shared accumulation is possible

The UM-MCI core provides shared IDs for:
- paradigms
- dimensions
- option paths
- edge families
- artifacts
- validation primitives
- tensions
- context dimensions

Because these IDs are shared, different teams can log experiences in biology, physics, policy, engineering, or software tasks and still describe them in a common comparative language.

## Recommended contribution types

1. **Retrospective cases**
   - back-map a finished task or paper into route structure
2. **Worked examples**
   - minimal end-to-end demonstrations for users
3. **Signature seeds**
   - practical recognizer hints for edge-family use
4. **Candidate route-prior notes**
   - provisional soft priors about trigger patterns, useful routes, or failure recovery
5. **Governance proposals**
   - when a recurring pattern appears stable enough to justify promotion

## Promotion discipline

Keep fast-changing practical material in the companion unless all three hold:
- it recurs across teams or domains,
- its meaning has stabilized,
- leaving it outside the core would now harm interoperability or auditability.

## Local extensions

Use `extensions` with a vendor/team namespace for any local additions. Do not add undocumented top-level fields to shared records.


## Recommended accumulation workflow

1. **Use the released core IDs first.** Shared cases, signatures, and prior notes should reference the pinned public vocabulary whenever possible.
2. **Keep local extras local.** If a team needs extra fields, keep them under `extensions` and namespace them.
3. **Let patterns grow in the companion first.** Recurrent ideas should first appear as examples, retrospective cases, signature seeds, or candidate route-prior notes.
4. **Promote through governance proposals, not silent rewrites.** If a pattern seems stable enough for Layer 2 or Layer 1, submit a promotion proposal with evidence.
5. **Only core maintainers update the public vocabulary.** This prevents the shared language from drifting into incompatible forks.

## Public vocabulary immutability between core releases

For shared accumulation to remain globally shareable, the released public vocabulary should be treated as **read-only between core releases**. Contributors may add local fields under `extensions`, or grow new practical objects in the companion, but they should not silently redefine or replace released `UM.*` identifiers.

## Promotion flow

A practical pattern should normally move through four stages:
1. **local experiment** under `extensions` or a project-private note,
2. **companion-level shared object** such as a retrospective case, signature seed, or candidate route-prior note,
3. **governance proposal** when the pattern recurs and appears semantically stable,
4. **maintainer-curated core release** if promotion into Layer 2 or Layer 1 is justified.

This keeps shared accumulation possible without letting the public vocabulary fragment into incompatible forks.


## Shared submission minima

The relaxed schemas are intentionally permissive enough for local exploration. Public companion submissions should satisfy a stricter practical minimum. As a rule of thumb:

- **candidate route-prior notes** should include a base paradigm, at least one concrete commitment (option path or supporting edge), and evidence references that directly support the claim;
- **signature seeds** should identify both the base and supporting paradigms and include at least one concrete hint (dimension, artifact, or validation);
- **governance proposals** should include explicit targets, a requested action, a rationale, and evidence pointers.

The workspace validators enforce these minima for the shared starter objects even when the relaxed schemas allow thinner local drafts.
