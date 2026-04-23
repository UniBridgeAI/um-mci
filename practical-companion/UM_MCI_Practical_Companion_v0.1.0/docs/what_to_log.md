# What to log, and what not to log

UM-MCI works best when logging is selective.


## When to use UM-MCI at all

Use UM-MCI logging selectively. A task is worth entering the UM-MCI layer when route choice itself matters: multiple methodological routes are plausible, the route will change artifacts or validators, the task cannot be reduced to one ordinary tool call, or the resulting trace should teach future route selection.

Do not use UM-MCI as a wrapper around every small task. If the goal can be completed by one clarification, one lookup, one small code edit, or one ordinary tool call without a meaningful methodological commitment, keep it as a normal execution trace instead of creating a stage or meta-run.

## Log as a stage when
- a local route is chosen or revised,
- artifacts or validators change materially,
- support edges are added or removed,
- a meaningful route-level burden is being relieved,
- the step has its own local goal and can be validated or diagnosed locally.

## Do not create a new stage when
- the agent only asked one clarifying question,
- the agent only fetched one fact or document,
- the agent only ran a tiny tool step inside the current stage,
- the agent only ran a validator subcheck already implied by the active stage.

Keep those events in provenance or execution traces unless they become substantial local episodes.

## What UM-MCI is mainly trying to learn

UM-MCI logging is mainly meant to learn from **route-level commitments and revisions**: which paradigms, option paths, support edges, artifacts, and validators tend to work under which tensions and contexts.

It is not mainly meant to relearn trivial micro-facts such as “one clarification question can reduce ambiguity.” Those effects are real, but they should usually remain inside provenance rather than becoming standalone learning units.

## Low-overhead tension profile

If you want to minimize logging burden, do not rescore every tension every time. A practical minimal profile is to track only the tensions that are clearly route-relevant for the current stage—often ambiguity, evidence gap, tractability, horizon, and sometimes uncertainty or consistency—and leave the others unchanged unless they become salient.



## Tension beliefs are assessments

Pre/post tension states are route-level assessments, not objective truths. Use confidence and evidence pointers, and do not over-log trivial micro-actions that do not introduce nontrivial route commitments.
