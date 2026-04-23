# Design rationale

## Why the core and companion are separated

The archival core should stay compact, stable, and semantically disciplined. The companion should stay practical, extensible, and easy to revise.

## Why option-path defaults still matter

A core default is a route prior, not a full implementation. It identifies which methodological commitments matter first and, when needed, it can descend from a stable dimension into a more specific Compass option path. That is already useful for route initialization, route comparison, and route logging.

Fine-grained bullet-level method families remain available through the Compass seed. This companion provides utilities for compiling those deeper options into task-facing views.

## Why signature seeds live here rather than in the archival core

Recognizer signatures are useful, but they evolve quickly with local logging practices, task families, and runtime architectures. They therefore belong in GitHub rather than in the stable Core Semantic Package.

## Why public namespaces matter

The public namespaces in the core package make cross-domain accumulation possible. If one biology group and one physics group record similar methodological experience using different local IDs, their experience cannot be accumulated or reused cleanly. A shared public vocabulary solves that coordination problem.
