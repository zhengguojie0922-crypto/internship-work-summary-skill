# Natural Deep Interview Output Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and execute this plan inline. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the visible ten-field interview form with evidence-backed feature deep dives and natural, systematic answers with independently answered follow-ups.

**Architecture:** The shared role framework turns the in-memory evidence matrix into a reusable feature model. The interview reference defines the user-facing deep-dive chapter, natural Q&A form, scenario form, and one positive shape example; the main Skill controls route scaling and the single-file output contract.

**Tech Stack:** Markdown Skill instructions, Python `unittest`, Python standard library.

## Global Constraints

- Runtime analysis writes only `career-output/实习产出与面试准备.md`.
- Evidence matrices, feature models, question plans, and audits stay in memory.
- Do not prescribe a numeric line, word, page, character, or token target.
- A file path or line range without symbol relationships is not sufficient code analysis.
- Main answers are connected interview narratives; follow-ups are shown and answered separately.
- Work on `codex/natural-deep-interview-output` without an extra worktree.
- Do not commit, push, or create a pull request without explicit user instruction.

---

### Task 1: Lock The Two-Layer Output Contract

**Files:**
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: active Markdown instructions in `SKILL.md`, `interview-expansion.md`, and `role-analysis-framework.md`.
- Produces: regression tests for the feature model, deep-dive chapter, natural answers, and independent follow-up answers.

- [x] **Step 1: Replace visible ten-field assertions**

Update the final-document test to require `Feature Deep Dive`, `Natural Interview Q&A`, `direct conclusion`, `connected paragraphs`, `shown and answered separately`, `strongest two outputs`, `15-20`, and `internal quality rubric`. Assert that the main Skill no longer requires every visible question to contain `Detailed question`, `Interview intent`, `Reasoning process`, or `Detailed first-person answer` fields.

- [x] **Step 2: Require the interview reference's positive recipe**

Update the interview-reference test to require these headings and markers:

```python
for phrase in (
    "## Feature Deep Dive",
    "## Natural Interview Q&A",
    "## Positive Shape Example",
    "direct conclusion",
    "connected paragraphs",
    "relationship among the evidence anchors",
    "shown and answered separately",
    "not a length template",
):
    self.assertIn(phrase, text)
```

Require a natural `**Answer:**`, `**Follow-up 1:**`, and `**Evidence and boundary:**` example. Reject the retired visible ten-field sequence and grouped follow-up answers.

- [x] **Step 3: Require feature-model generation in the role framework**

Add `## Feature Model` and require glossary, causal problem narrative, architecture and call-path map, state/data/protocol/lifecycle model, happy/failure/recovery/degradation paths, code/test responsibility map, and evidence gaps before question planning.

- [x] **Step 4: Run focused tests and verify RED**

```powershell
python -m unittest tests.test_skill_contract.SkillContractTests.test_final_document_has_resume_narratives_and_question_sets tests.test_skill_contract.SkillContractTests.test_interview_reference_separates_core_and_scenario_questions tests.test_skill_contract.SkillContractTests.test_role_analysis_framework_maps_evidence_to_career_material -v
```

Expected: failures because version 1.2.0 still exposes the ten-field form and lacks a feature model and positive natural-answer example.

### Task 2: Implement Feature Deep Dives And Natural Q&A

**Files:**
- Modify: `skills/summarizing-internship-work/SKILL.md`
- Modify: `skills/summarizing-internship-work/references/interview-expansion.md`
- Modify: `skills/summarizing-internship-work/references/role-analysis-framework.md`

**Interfaces:**
- Consumes: repository evidence, attribution route, evidence matrix, primary role guide, and optional evidence-supported secondary guide.
- Produces: a shared feature model, user-facing feature chapter, natural main answers, independent follow-up answers, and a final audit.

- [x] **Step 1: Make the framework produce a feature model**

Insert `## Feature Model` after `## Evidence Matrix`. Define the glossary, failure origin, architecture and call path, state/data/protocol/lifecycle model, happy/failure/recovery/degradation paths, responsibility map, alternatives, and evidence gaps. Require question planning to reuse this shared model.

- [x] **Step 2: Rewrite interview expansion around two layers**

Replace `## Complete Core Question Unit` with `## Feature Deep Dive` and `## Natural Interview Q&A`. Keep the ten dimensions only as an internal rubric. Require answers to start with a direct conclusion and continue in connected paragraphs through mechanism, failure semantics, trade-offs, validation, and personal boundary.

- [x] **Step 3: Add one complete positive shape example**

Use a generic registration-transaction example that demonstrates:

```markdown
### Q: Why must account initialization use one transaction?

**Answer:**

[Direct conclusion, invariant, call path, transaction boundary, failure semantics,
trade-off, validation, and boundary in a coherent answer.]

**Follow-up 1: Can an external service call stay inside the transaction?**

[Complete standalone answer.]

**Follow-up 2: What if the commit succeeds but the response is lost?**

[Complete standalone answer.]

**Evidence and boundary:**

[Explain what concrete repository evidence would be required.]
```

State that it demonstrates shape only, supplies no project facts, and is not a length template.

- [x] **Step 4: Update main Skill route scaling and output order**

For a named feature, generate one complete deep dive with approximately 15-20 questions and 3-5 scenarios. For Git discovery, fully expand the strongest two outputs by default and summarize remaining verified outputs. Replace the visible ten-field requirement with `Feature Deep Dive` and `Natural Interview Q&A` sections and the internal audit.

- [x] **Step 5: Run focused tests and verify GREEN**

Run the focused command from Task 1. Expected: all three tests pass.

### Task 3: Align README And Version 1.3.0

**Files:**
- Modify: `tests/test_packaging.py`
- Modify: `README.md`
- Modify: `skills/summarizing-internship-work/VERSION`

**Interfaces:**
- Consumes: implemented version 1.3 behavior.
- Produces: accurate public documentation and aligned package version.

- [x] **Step 1: Write failing public-surface assertions**

Require README phrases for `功能深挖章节`, `自然问答`, `完整独立回答`, `代码关系`, `最强的 2 项`, and version `1.3.0`. Reject the old visible ten-field description.

- [x] **Step 2: Run focused packaging tests and verify RED**

Run the four existing README/version tests. Expected: failure against version 1.2.0 and old copy.

- [x] **Step 3: Update README and VERSION**

Explain the two-layer output, named-feature and Git-discovery scaling, natural answers, evidence relationship requirement, and single-file boundary. Change `VERSION` and the no-forward-test statement to `1.3.0` without claiming model validation.

- [x] **Step 4: Run focused packaging tests and verify GREEN**

Expected: all focused README/version tests pass.

### Task 4: Verify And Audit The Repository

**Files:**
- Verify all changed files.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: fresh deterministic evidence for completion.

- [x] **Step 1: Run the full test suite**

```powershell
python -m unittest discover -s tests -v
```

Expected: zero failures and zero errors.

- [x] **Step 2: Compile Python sources**

```powershell
python -m compileall -q skills tests
```

Expected: exit code 0.

- [x] **Step 3: Check the patch**

```powershell
git diff --check
```

Expected: no whitespace errors.

- [x] **Step 4: Audit active instructions**

Verify that active Skill files contain the two-layer positive recipe, do not prescribe a hard length target, do not require the ten internal dimensions as visible fields, and preserve the single-final-file rule.

- [x] **Step 5: Inspect final Git state**

```powershell
git status --short
git diff --stat
git diff
```

Confirm that changes stay on `codex/natural-deep-interview-output` and are not committed or pushed.
