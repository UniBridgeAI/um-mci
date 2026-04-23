# Logging and overhead policy

The practical companion is intentionally designed so that UM-MCI logging does **not** need to run at every microstep.

## Default low-overhead policy

- Log tension beliefs at **stage boundaries**, not after every tiny action.
- Recompute only the tensions that are clearly active for the current route.
- Run all **must** validators by default.
- Escalate **should** and **may** validators only when stakes, budget, or failure signals justify it.
- Keep trivial clarification, one-off retrieval, and tiny tool calls in provenance unless they become substantial local episodes.

## Minimal tension subset

A low-overhead deployment will often track only:
- ambiguity,
- evidence gap,
- tractability,
- horizon,
- and sometimes uncertainty or consistency.


## Practical implication

UM-MCI is most useful when it helps an agent make **better global route decisions** without forcing the agent to narrate every tiny move. The point is to preserve learning where route design matters, not to inflate token or latency cost everywhere.
