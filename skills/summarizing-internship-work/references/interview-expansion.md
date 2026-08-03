# Interview Expansion

Populate the `Interview Introduction` and `Interview Questions` sections of the final document from evidence-backed major outputs.

## Evidence-First Preparation

Before drafting either section, use the shared role framework to build an in-memory evidence matrix for every major output. Follow the feature from its business or system boundary through concrete files, symbols, callers, callees, data and state transitions, branches, dependencies, failures, configuration, tests, and applicable Git history. Keep this matrix in context; do not write an intermediate artifact.

Every project-specific question needs at least one concrete evidence anchor such as a file and symbol, a proved call-path segment, a branch, a test, a configuration item, or an applicable commit. A search hit, filename, framework convention, or plausible production outcome is not enough by itself.

## Interview Introductions

Write three introductions:

- `30-second`: problem or context, personal action, and supported result.
- `1-minute`: scope, constraints, code path, decisions, collaboration boundary, and validation.
- `3-minute`: alternatives, data and error paths, tests, trade-offs, evidence limits, and reflection.

The introductions and detailed answers must agree on scope, ownership, technical mechanism, validation, and impact boundaries. Use first-person ownership only when the selected feature or Git route supports it.

## Core Question Coverage

For each major output, prepare about 20 core interview questions. Plan them from distinct rows and relationships in the evidence matrix. Cover the supported parts of business context, personal scope, architecture, entry points, UI or API boundary, business rules, data flow, state and persistence, dependencies, configuration, failure handling, testing, performance, security, debugging, collaboration, maintenance, alternatives, and improvements.

Always merge duplicate questions when their evidence anchors, central conclusion, and answer path substantially overlap. Replace a duplicate only with a distinct evidence-backed angle. Do not paraphrase one implementation detail into several questions or use generic textbook material to satisfy the approximate count.

## Complete Core Question Unit

Write every core question with all of these elements:

1. **Detailed question**: establish the business scenario, implementation boundary, relevant constraint, and exact technical problem. Make the question specific enough that its answer cannot be copied unchanged to an unrelated project.
2. **Interview intent**: explain which engineering abilities and judgments the interviewer is evaluating and which weak shortcuts the question is designed to expose.
3. **Code evidence**: name the relevant files, symbols, entry point, callers, callees, data flow, state changes, and important branches. Explain what each anchor proves rather than listing paths without relationships.
4. **Reasoning process**: reconstruct the analysis from requirement to entry point, through the implementation and validation boundary. Show how the evidence supports each conclusion and where inference begins.
5. **Detailed first-person answer**: provide an interview-ready response that covers context, personal action under the applicable attribution route, implementation, difficulty, decision, validation, supported result, and explicit limits.
6. **Design trade-offs**: compare the implemented approach with evidence-supported alternatives. Explain benefits, costs, operational consequences, and the conditions under which another choice would be preferable. Do not invent rejected designs or decision authorship.
7. **Failure and validation analysis**: cover edge conditions, error propagation, degradation or recovery, concurrency or security concerns when relevant, tests, logs or observability, and remaining runtime validation gaps.
8. **2-4 deep follow-up questions**: derive follow-ups from concrete claims, branches, trade-offs, or gaps in the main answer. At least one should test the implementation chain and at least one should test a changed constraint or failure mode when the evidence supports it.
9. **Complete follow-up answers**: answer every follow-up in full. Each answer must reconnect to project evidence, reason through the changed premise, state the decision or diagnosis, and preserve the same evidence and attribution boundaries as the main answer.
10. **Evidence boundary**: close the unit by distinguishing source-confirmed facts, Git-confirmed facts, test evidence, user-provided attribution, static interpretation, and information that still needs user or runtime evidence.

A complete unit is a connected analysis, not ten disconnected labels. The reasoning, answer, trade-offs, failures, and follow-ups must refer to the same concrete code path and must not contradict one another.

## Scenario Questions

After the core questions, add a separate set of 3-5 scenario questions that test judgment under changed constraints. For each scenario, state the changed premise and assumptions, identify the affected code path and evidence anchors, analyze diagnosis or decision steps, give a concrete first-person response, compare trade-offs, define validation and escalation, and add evidence-derived follow-ups with complete answers. Make clear which parts describe the current implementation and which parts are a proposed response to the hypothetical scenario.

## Degradation And Final Audit

Produce fewer than 20 core questions when evidence is insufficient; never pad or fabricate to meet a quota. State unknowns plainly and explain what evidence or user input would verify them. Do not present inferred intent, runtime behavior, impact, metrics, ownership, or collaboration as fact.

Before the single final document write, run a final quality audit in memory:

- every core question contains the complete ten-element unit;
- every follow-up has a corresponding complete answer;
- every project-specific claim maps to a concrete evidence anchor or an explicit evidence boundary;
- the question set covers distinct technical dimensions without rephrased duplicates;
- introductions, resume claims, main answers, and follow-up answers use consistent attribution and facts;
- scenario answers distinguish current evidence from proposed actions;
- no answer hint, outline placeholder, or generic advice substitutes for the requested analysis.

If an item fails, return to the evidence matrix or question plan, inspect the relevant code path more deeply, and repair the draft in memory before writing `career-output/实习产出与面试准备.md`.
