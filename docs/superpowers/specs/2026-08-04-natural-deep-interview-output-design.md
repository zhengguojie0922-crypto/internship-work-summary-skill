# Natural Deep Interview Output Design

## Goal

Make the final internship and interview document read like a project-specific deep-dive handbook: first explain each important feature as a coherent system, then provide natural, directly usable interview answers and independent follow-up answers. Depth must come from evidence, causal explanation, and complete technical narratives rather than a document-length quota or a visible ten-field form.

## Observed Failure

Version 1.2.0 correctly required evidence, trade-offs, failures, validation, and follow-ups, but exposed all ten requirements as peer fields inside every question. Models can satisfy that shape by writing one short sentence per field. An output with about 20 questions then naturally becomes about 200 lines without ever giving a systematic spoken answer.

The total request also creates compression pressure. Three default outputs, about 20 questions per output, and multiple follow-ups per question can require dozens of long answer units. Under a finite response budget, models tend to preserve the requested headings while shortening the substance.

The supplied reference document demonstrates a better structure. Its depth comes primarily from shared feature chapters covering background, failure origin, architecture, state, flows, code boundaries, and tests. The interview section can then use a simple `Question -> Answer -> Follow-up -> Answer` form because the underlying system has already been reconstructed.

## Output Architecture

The final document uses two layers for every fully expanded major output.

### Layer 1: Feature Deep Dive

Build a coherent chapter with these evidence-driven sections when the repository supports them:

1. Feature positioning and personal contribution boundary.
2. Business or system background and essential terminology.
3. The original problem and the concrete failure sequence.
4. The feature's position in the wider architecture.
5. Goals, non-goals, invariants, and authority boundaries.
6. Core data model, state model, lifecycle, or protocol concepts.
7. End-to-end happy path and recovery path.
8. Important branches, failure semantics, edge cases, and degradation.
9. Design alternatives, trade-offs, and reasons visible in evidence.
10. Code responsibility map linking files, symbols, callers, callees, and tests.
11. Test and fault-scenario matrix.
12. Resume wording and short interview introductions.

This is not a fixed heading checklist. Select and name sections according to the feature and target role, but the chapter must answer the equivalent engineering questions before interview Q&A begins.

Code evidence must explain relationships. A path or line range alone is not analysis. The chapter states what a symbol does, who calls it, what it calls, which state or data crosses the boundary, how errors propagate, and what test or configuration verifies the conclusion.

### Layer 2: Natural Interview Q&A

The ten version 1.2 quality dimensions remain an internal planning and audit rubric. They are not emitted as ten visible fields.

Each core question is rendered naturally:

```markdown
### Q1: [Project-specific question]

**Answer:**

[A coherent, interview-ready answer in connected paragraphs.]

**Follow-up 1: [Question derived from a concrete claim]**

[A complete standalone answer.]

**Follow-up 2: [Question derived from a trade-off, failure, or changed constraint]**

[A complete standalone answer.]

**Evidence and boundary:**

[Only the evidence anchors and uncertainty needed to keep the answer honest.]
```

The main answer begins with a direct conclusion, then develops the relevant context or invariant, the end-to-end implementation mechanism, error or recovery behavior, alternatives and trade-offs, validation, and personal boundary. These are connected parts of one explanation, not separate one-line labels.

Every follow-up is printed separately and receives its own complete answer. A grouped line of several questions followed by one combined answer is not a valid question unit.

## Evidence Workflow

The agent first builds the existing evidence matrix in memory, then uses it to draft a feature model before drafting questions. The feature model includes:

- a glossary and system boundary;
- a causal problem narrative;
- an architecture and call-path map;
- state, data, protocol, or lifecycle models;
- happy, failure, recovery, and degradation paths;
- code and test responsibility maps;
- alternatives, constraints, and evidence gaps.

Questions are derived from claims, mechanisms, invariants, branches, and trade-offs in that feature model. The answer must explain the relationship among anchors rather than repeat a file list.

## Route Scaling

### Named Feature Route

Produce one complete feature deep dive, approximately 15-20 evidence-supported core questions, and 3-5 fully answered scenario questions.

### Git Discovery Route

Select the strongest two outputs for complete deep dives by default. Put other verified contributions into resume-ready summaries and a compact appendix. An explicit comprehensive request may expand more outputs, but the skill preserves answer completeness before increasing breadth.

The question count remains approximate and evidence-driven. There is no line, word, page, character, or token target.

## Scenario Questions

Scenario questions use the same natural presentation. Each starts from a changed constraint grounded in the analyzed feature, gives a complete diagnosis or decision answer, explains affected code and state, compares trade-offs, defines validation and escalation, and includes separately answered follow-ups.

## Positive Example

Add one generic, reusable example to the interview reference. It demonstrates how a transaction-boundary question becomes a direct, multi-paragraph answer with a concrete call path, failure semantics, alternatives, validation, and independent follow-ups. It must not copy project-specific content from the user's supplied document.

The example is a shape exemplar, not a minimum-length template and not a source of facts for future projects.

## Quality Audit

Before the single final write, audit in memory:

- the feature deep dive explains the system before asking detailed questions;
- code anchors are connected by proved relationships rather than listed alone;
- every main answer is a direct, coherent explanation rather than a field summary;
- each follow-up is displayed and answered independently;
- questions draw from distinct mechanisms or failure modes;
- answers remain consistent with the feature model, attribution route, and evidence boundaries;
- generic textbook content, answer hints, and visible ten-field forms are absent;
- no hard document-length target is used.

Failed items return to evidence collection or drafting before the final file is written.

## Runtime Artifact Boundary

The skill still writes only `career-output/实习产出与面试准备.md`. Evidence matrices, feature models, question plans, and audits remain in memory. The analyzed repository remains read-only.

## Files To Change

- `skills/summarizing-internship-work/SKILL.md`: replace the visible ten-field question contract, add the two-layer output and route scaling.
- `skills/summarizing-internship-work/references/interview-expansion.md`: define feature deep dives, natural Q&A, independent follow-ups, scenario answers, and one positive example.
- `skills/summarizing-internship-work/references/role-analysis-framework.md`: make the evidence matrix produce a shared feature model before question planning.
- `README.md`: describe the natural deep-dive output and updated route scaling.
- `skills/summarizing-internship-work/VERSION`: update to `1.3.0`.
- `tests/test_skill_contract.py` and `tests/test_packaging.py`: replace version 1.2 form assertions with version 1.3 structure and anti-regression assertions.

No large forward-test controller or intermediate test artifact is restored.

## Verification

Use TDD:

1. Add contract tests for the two-layer output, natural answer form, independent follow-up answers, code relationship requirements, route scaling, positive example, and absence of the visible ten-field form.
2. Observe the focused tests fail against version 1.2.0.
3. Implement the minimal Skill, references, README, and version changes.
4. Run focused tests, the complete unittest suite, Python compilation, `git diff --check`, and an output-shape audit of active instructions.

The deterministic tests verify the prompt and package contract. Do not claim external-model behavior unless a model is actually run.

## Git Constraints

Work on the ordinary local branch `codex/natural-deep-interview-output`. Do not create an extra worktree. Leave commit, push, and pull-request actions for explicit user instruction.
