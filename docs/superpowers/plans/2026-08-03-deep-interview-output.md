# Deep Interview Output Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development and execute this plan inline. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every core and scenario interview question a detailed, code-evidence-backed preparation unit that includes complete follow-up answers, without prescribing document length.

**Architecture:** Add a positive output contract to the main Skill and central interview reference. The role framework supplies an in-memory evidence matrix and question-planning rules, while contract tests prevent regression to concise answers, answer hints, generic padding, or hard length targets.

**Tech Stack:** Markdown Skill instructions, Python `unittest`, Python standard library.

## Global Constraints

- Runtime analysis creates only `career-output/实习产出与面试准备.md`; all evidence notes remain in memory.
- Do not specify a total line, word, character, page, or token target for the final document.
- Keep approximately 20 core questions per major output when evidence supports them; quality and evidence boundaries override the approximate count.
- Every core question includes the ten approved elements and two to four follow-ups with complete answers.
- Do not create a worktree, commit, push, or open a pull request.

---

### Task 1: Lock The Deep-Question Contract With Failing Tests

**Files:**
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: Markdown content from `SKILL.md`, `interview-expansion.md`, and `role-analysis-framework.md`.
- Produces: Regression assertions for the approved evidence-first and complete-question contracts.

- [x] **Step 1: Replace the old concise-answer assertions**

Update the final-document and interview-reference tests to require these observable phrases or equivalent exact contract markers:

```python
for phrase in (
    "in-memory evidence matrix",
    "Detailed question",
    "Interview intent",
    "Code evidence",
    "Reasoning process",
    "Detailed first-person answer",
    "Design trade-offs",
    "Failure and validation analysis",
    "2-4 deep follow-up questions",
    "Complete follow-up answers",
    "Evidence boundary",
    "at least one concrete evidence anchor",
    "merge duplicate questions",
    "final quality audit",
):
    self.assertIn(phrase, output_section)
```

Add assertions that `concise reference answer`, `follow-up answer direction`, and `scenario response framework` are absent from the active Skill and interview reference. Add a regex assertion that the active instructions do not prescribe a numeric line, word, character, page, or token total.

- [x] **Step 2: Require the shared role framework to drive evidence-first planning**

Extend `test_role_analysis_framework_maps_evidence_to_career_material` to require `## Evidence Matrix`, concrete evidence anchors, distinct coverage dimensions, duplicate-question merging, complete follow-up answers, and the final quality audit.

- [x] **Step 3: Run the focused tests and verify RED**

Run:

```powershell
python -m unittest tests.test_skill_contract.SkillContractTests.test_final_document_has_resume_narratives_and_question_sets tests.test_skill_contract.SkillContractTests.test_interview_reference_separates_core_and_scenario_questions tests.test_skill_contract.SkillContractTests.test_role_analysis_framework_maps_evidence_to_career_material -v
```

Expected: failures because the existing files still request a concise reference answer and do not contain the new structural contract.

### Task 2: Implement Evidence-First Interview Generation

**Files:**
- Modify: `skills/summarizing-internship-work/SKILL.md`
- Modify: `skills/summarizing-internship-work/references/interview-expansion.md`
- Modify: `skills/summarizing-internship-work/references/role-analysis-framework.md`

**Interfaces:**
- Consumes: Evidence and attribution rules already defined by the Skill and selected role guides.
- Produces: An in-memory evidence matrix, distinct question plan, complete question units, and a final quality audit.

- [x] **Step 1: Add the evidence matrix to the shared framework**

Add `## Evidence Matrix` after `## Evidence Chain`. Require one in-memory row per major output covering business scope, entry point, files and symbols, callers and callees, data and state, rules and branches, failures, validation, applicable Git evidence, decisions and alternatives, and evidence gaps.

- [x] **Step 2: Expand interview question planning in the shared framework**

Replace the short question-tree paragraph with evidence-driven coverage across business context, call path, state, rules, boundaries, reliability, performance, validation, architecture, contribution, and target-role depth. Require at least one concrete anchor per project-specific question and merge duplicates whose anchors, conclusion, and answer path substantially overlap.

- [x] **Step 3: Replace concise output wording in the main Skill**

Before the numbered output structure, require the in-memory evidence matrix and question coverage plan. Replace item 7 with the complete ten-element question unit, two to four follow-ups with complete answers, and three to five fully analyzed scenario questions. Preserve the existing evidence-insufficiency rule.

- [x] **Step 4: Rewrite the interview reference as the detailed template**

Keep the three introductions, then define:

```text
Detailed question -> Interview intent -> Code evidence -> Reasoning process
-> Detailed first-person answer -> Design trade-offs
-> Failure and validation analysis -> 2-4 deep follow-up questions
-> Complete follow-up answers -> Evidence boundary
```

Define scenario units with assumptions, diagnosis or decision steps, concrete response, trade-offs, project evidence, validation, and complete follow-up answers. Add a final quality audit and repair loop before the single final write.

- [x] **Step 5: Run the focused tests and verify GREEN**

Run the same focused unittest command from Task 1.

Expected: all three tests pass.

### Task 3: Align Public Documentation And Version

**Files:**
- Modify: `README.md`
- Modify: `skills/summarizing-internship-work/VERSION`
- Modify: `tests/test_packaging.py`

**Interfaces:**
- Consumes: The final behavior contract implemented in Task 2.
- Produces: Accurate installation-facing documentation and package version `1.2.0`.

- [x] **Step 1: Add a failing packaging assertion for version 1.2.0**

Update the existing version expectation in `tests/test_packaging.py` from `1.1.0` to `1.2.0` and run its exact test method.

Expected: failure because `VERSION` and README still contain `1.1.0`.

- [x] **Step 2: Update VERSION and README**

Set `VERSION` to `1.2.0`. Replace README references to concise answers and answer directions with the complete-question structure, code evidence anchors, design trade-offs, failure analysis, and complete follow-up answers. Update the model-validation note to `1.2.0` without claiming an external-model run.

- [x] **Step 3: Run the focused packaging test**

Expected: the updated version test passes.

### Task 4: Verify The Complete Repository

**Files:**
- Verify all modified files.

**Interfaces:**
- Consumes: All changes from Tasks 1-3.
- Produces: Fresh evidence that the package, tests, syntax, and diff are consistent.

- [x] **Step 1: Run the complete test suite**

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures and zero errors.

- [x] **Step 2: Compile Python sources**

```powershell
python -m compileall skills tests
```

Expected: exit code 0.

- [x] **Step 3: Check patch formatting**

```powershell
git diff --check
```

Expected: no output and exit code 0.

- [x] **Step 4: Audit the final diff and repository state**

```powershell
git status --short
git diff --stat
git diff -- skills/summarizing-internship-work/SKILL.md skills/summarizing-internship-work/references/interview-expansion.md skills/summarizing-internship-work/references/role-analysis-framework.md README.md skills/summarizing-internship-work/VERSION tests/test_skill_contract.py tests/test_packaging.py
```

Confirm that no worktree, commit, push, external model claim, intermediate runtime artifact, or hard output-length target was introduced.
