# Deep Interview Output Design

## Goal

Increase the final career document's project-specific depth without setting a total line, word, or character target. Every core interview question must become a complete, evidence-backed interview preparation unit rather than a short prompt with a concise answer.

## Problem

The current skill requests about 20 core questions but describes each response as a `concise reference answer`. It does not require each question to reconstruct the relevant code path, explain trade-offs, cover failures and validation, or answer its follow-ups. A model can therefore satisfy the visible structure while producing a document of only a few hundred lines and relying on generic interview language.

This is an output-shape failure. The fix is a positive structural contract that defines what a complete analysis unit contains. It is not a request to "write more," and it must not introduce a hard document-length target.

## Evidence-First Generation Flow

For each selected internship output, the skill builds an in-memory evidence matrix before drafting career material. The matrix covers:

- business goal, user value, and feature boundary;
- entry points and externally visible contracts;
- files, symbols, callers, callees, and the end-to-end call path;
- data flow, state transitions, persistence, and external dependencies;
- important rules, branches, and lifecycle behavior;
- failure paths, boundary conditions, recovery, and degradation;
- tests, logs, configuration, and other validation evidence;
- Git evidence when the Git-discovery route applies;
- design choices, plausible alternatives, and evidence limitations.

The matrix remains in memory. Runtime behavior still creates only `career-output/实习产出与面试准备.md`; it does not create research notes, evidence files, prompts, or other intermediate artifacts.

Questions are planned from the matrix only after the evidence pass is complete. A project-specific question must cite at least one concrete evidence anchor such as a file, symbol, call-path segment, test, configuration item, or commit. Unsupported runtime outcomes and business metrics remain explicitly unknown.

## Complete Question Unit

Each of the approximately 20 core interview questions for an output uses the following complete structure:

1. Detailed question: establish the business scenario, implementation scope, and technical problem.
2. Interview intent: state the abilities and judgments the interviewer is testing.
3. Code evidence: identify relevant files, symbols, entry point, call chain, data flow, and important branches.
4. Reasoning process: reconstruct how to move from the requirement through the implementation and infer design intent from evidence.
5. Detailed first-person answer: provide an interview-ready account of context, implementation, difficulty, decisions, result, and limits.
6. Design trade-offs: compare the implemented approach with credible alternatives and explain the choice only to the extent supported by evidence.
7. Failure and validation analysis: cover edge cases, error paths, tests, observability, and remaining validation gaps.
8. Two to four deep follow-up questions: derive them from claims and decisions in the main answer.
9. Complete follow-up answers: answer every follow-up with project evidence and reasoning rather than an answer hint.
10. Evidence boundary: distinguish source-confirmed facts, Git-confirmed facts, reasoned interpretations, and information requiring user input.

All core questions use this structure. The final document also contains three to five scenario questions. Each scenario question includes assumptions, diagnosis or decision steps, a concrete response, trade-offs, evidence links back to the project, and follow-ups with full answers.

## Coverage And Deduplication

The question plan distributes coverage across the evidence actually present in the project. Relevant dimensions include:

- business requirement, value, and scope;
- entry points, end-to-end calls, and data flow;
- data structures, state, persistence, and lifecycle;
- algorithms and business rules;
- interfaces, module boundaries, and cross-system collaboration;
- errors, degradation, idempotency, concurrency, and edge cases;
- performance, resources, and observability;
- tests, validation, and defect diagnosis;
- architecture, alternatives, and evolution;
- personal contribution, technical difficulty, and retrospective improvement;
- technical depth expected for the target role.

Two questions are duplicates when their evidence anchors, central conclusion, and answer path are substantially the same. Duplicate questions are merged, and a different evidence-backed angle is selected. Generic textbook questions cannot be used to reach an approximate count.

If evidence is insufficient, the skill first expands its read-only investigation to callers, callees, tests, configuration, documentation, and applicable Git history. If the evidence still cannot support the normal breadth, the final document contains fewer high-quality questions and an explicit evidence-gap note. It never fabricates code, ownership, runtime outcomes, metrics, or business impact.

## Career Material

The feature explanation, resume wording, and 30-second, 1-minute, and 3-minute narratives also use the evidence matrix. They identify the business purpose, individual scope under the selected attribution route, implementation path, technical challenge, decision, validation, and honest impact boundary. The interview section receives most of the document's depth, but the earlier career sections must be internally consistent with it.

## Role Adaptation

The shared role-analysis framework defines the evidence matrix, technical-depth dimensions, question coverage, and complete-question contract. Exactly one primary role guide and at most one evidence-supported secondary guide continue to select role-specific emphasis. The seven role guides do not duplicate the shared output template; they provide the technical dimensions and decision patterns that populate it.

## Quality Gate

Before writing the final Markdown file, the skill audits the in-memory draft:

- every core question contains all ten complete-question elements;
- every follow-up has a corresponding complete answer;
- every project-specific claim maps to a concrete evidence anchor or an explicit evidence boundary;
- the set covers distinct technical dimensions and avoids rephrased duplicates;
- first-person claims follow the selected attribution route;
- resume wording, narratives, main answers, and follow-up answers do not contradict one another;
- no placeholder language such as "answer direction" substitutes for actual analysis;
- no total line, word, or character target is used as a quality proxy.

When an item fails the audit, the skill returns to the evidence matrix or question draft in memory and repairs that item before the single final write.

## Files To Change

- `skills/summarizing-internship-work/SKILL.md`: replace concise-answer language with the evidence-first flow, complete-question contract, and final quality gate.
- `skills/summarizing-internship-work/references/interview-expansion.md`: define detailed core and scenario question units, coverage, deduplication, and follow-up-answer requirements.
- `skills/summarizing-internship-work/references/role-analysis-framework.md`: connect the evidence chain and role-specific analysis to question planning and depth.
- `tests/test_skill_contract.py`: assert the new positive structural contract and the absence of retired concise-answer wording and length targets.
- `README.md`: explain that interview preparation is code-evidence-backed and includes complete follow-up answers.
- `skills/summarizing-internship-work/VERSION`: change `1.1.0` to `1.2.0`.

The seven role guides are changed only if implementation reveals a missing shared-framework navigation point. They are not duplicated mechanically.

## Verification

Use TDD for the contract change:

1. Add focused assertions for the evidence matrix, complete-question unit, follow-up answers, deduplication, quality gate, and absence of hard length targets.
2. Run the focused test and observe failure for the missing contract.
3. Implement the minimal Skill and reference changes.
4. Run the focused test until it passes.
5. Run the complete unittest suite, Python compilation checks, and `git diff --check`.

Do not restore the deleted forward-test controller or large synthetic test materials. No external model claim is made unless an external model is actually run.

## Release And Git Constraints

This is a behavior-level minor release, so the packaged version becomes `1.2.0`. Work remains on the ordinary local branch `codex/deepen-interview-output`. Do not create a worktree, commit, push, or open a pull request on the user's behalf.
