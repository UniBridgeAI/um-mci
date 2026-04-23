# Retrospective extraction guidance

Retrospective extraction reconstructs a UM-MCI account of a past task, paper, or execution trace.

The goal is not perfect certainty. The goal is to make methodological experience:
- visible,
- comparable,
- accumulative,
- revisable.

Use the templates in `retrospective_extraction/templates/` to record:
- task summary,
- hypothesized stage decomposition,
- base paradigms by stage,
- dimension and edge-family hypotheses,
- artifact and validator evidence,
- tension and context hypotheses,
- unresolved ambiguities.

## Paper-based retrospective extraction is not execution replay

For published papers, retrospective extraction should be treated as an interpretive reconstruction of the public methodological route, not as a replay of the authors' actual execution history. Papers usually present a curated success narrative; failed route attempts, intermediate repairs, and local decisions are often omitted or reorganized for publication.

Use the lightest defensible granularity:

- Prefer a paper-level or route-level hypothesis when stage evidence is weak.
- Create stage hypotheses only when the paper provides enough evidence for a local goal, a route commitment, and a validation or diagnostic boundary.
- Do not force many stages merely to fit the template.
- Distinguish evidence that is author-stated, artifact-supported, and inferred.
- If stage-level reconstruction is not justified, keep `stage_hypotheses` as an empty array and place the main interpretation in route-level notes or summary fields available in the record.

A retrospective case should make uncertainty visible rather than hide it. The goal is to make route-level methodological structure inspectable and comparable, not to claim certainty about the original research process.
