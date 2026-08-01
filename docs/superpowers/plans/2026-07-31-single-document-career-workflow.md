# Single-Document Career Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the staged artifact workflow with two direct analysis routes that create only `career-output/实习产出与面试准备.md` during Skill use.

**Architecture:** Keep routing, confirmation limits, evidence boundaries, and final-document assembly in `SKILL.md`. Keep role-specific guidance in existing references, rewrite resume and interview references to describe sections within the single final document, and remove obsolete JSON artifact machinery.

**Tech Stack:** Agent Skill Markdown, Git, ripgrep, Python 3.10 standard-library `unittest`, GitHub Actions.

## Global Constraints

- Skill runtime creates no intermediate files or directories other than the parent directory for the final document.
- Skill runtime performs at most two user-confirmation rounds.
- Named-feature tracing ignores commit authorship; Git discovery scopes commits by Git identity.
- Target role is required but inferred before asking.
- Repository inspection is read-only and never executes target code.
- Resume and interview claims never invent unsupported facts or metrics.

---

### Task 1: Lock The New Skill Contract

**Files:**
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: Approved workflow design.
- Produces: Executable assertions for discovery triggers, request routing, confirmation limits, final document content, output path, and safety.

- [x] **Step 1: Replace old staged-artifact assertions with the new behavioral contract.**
- [x] **Step 2: Run `python -m unittest tests.test_skill_contract -v`.**
- [x] **Step 3: Confirm failures name missing new sections and old output behavior.**

### Task 2: Rewrite The Installable Skill

**Files:**
- Modify: `skills/analyzing-codebase-work-impact/SKILL.md`
- Modify: `skills/analyzing-codebase-work-impact/references/resume-writing.md`
- Modify: `skills/analyzing-codebase-work-impact/references/interview-expansion.md`

**Interfaces:**
- Consumes: Natural-language career request plus local repository evidence.
- Produces: One in-memory analysis and one final Markdown file.

- [x] **Step 1: Replace frontmatter description with Chinese and English trigger coverage.**
- [x] **Step 2: Implement named-feature and Git-discovery routing.**
- [x] **Step 3: Implement one consolidated question and a hard maximum of two confirmation rounds.**
- [x] **Step 4: Define layer-by-layer feature tracing and commit clustering.**
- [x] **Step 5: Define the complete ordered final-document template.**
- [x] **Step 6: Rewrite resume and interview references to populate that template without separate artifacts.**
- [x] **Step 7: Run `python -m unittest tests.test_skill_contract -v` and expect all tests to pass.**

### Task 3: Update Discovery Metadata And Chinese README

**Files:**
- Modify: `skills/analyzing-codebase-work-impact/agents/openai.yaml`
- Modify: `skills/analyzing-codebase-work-impact/VERSION`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `tests/test_packaging.py`

**Interfaces:**
- Consumes: New Skill contract.
- Produces: Correct implicit invocation metadata, installation documentation, workflow explanation, and publishing checks.

- [x] **Step 1: Add packaging assertions for the two routes, single output path, and absence of legacy artifact claims.**
- [x] **Step 2: Run the focused packaging tests and observe failure against the old README.**
- [x] **Step 3: Update `openai.yaml` with valid Chinese text and an explicit Skill invocation prompt.**
- [x] **Step 4: Bump the breaking workflow version from `0.1.0` to `0.2.0`.**
- [x] **Step 5: Rewrite README feature, usage, workflow, output, and verification sections in Chinese; update CONTRIBUTING for the reduced test surface.**
- [x] **Step 6: Run `python -m unittest tests.test_packaging -v` and expect all tests to pass.**

### Task 4: Remove Obsolete Artifact Machinery

**Files:**
- Delete: `skills/analyzing-codebase-work-impact/references/schemas/`
- Delete: `skills/analyzing-codebase-work-impact/scripts/validate_artifact.py`
- Delete: `docs/artifact-schemas.md`
- Delete: `docs/examples/*.json`
- Delete: `tests/fixture_builder.py`
- Delete: `tests/forward_test_runner.py`
- Delete: `tests/fixtures/`
- Delete: `tests/scenarios/`
- Delete: old validator, controller, fixture, forward-runner, and final-review tests
- Modify: `skills/analyzing-codebase-work-impact/references/analysis-defaults.md`
- Modify: `skills/analyzing-codebase-work-impact/references/achievement-analysis.md`
- Modify: `tests/test_collect_git_evidence.py`

**Interfaces:**
- Consumes: Confirmation that the staged JSON workflow is retired.
- Produces: A smaller repository containing only the installable Skill, reusable references, Git collector, and focused deterministic tests.

- [x] **Step 1: Add failing assertions for obsolete-file removal and direct links to retained analysis/role references.**
- [x] **Step 2: Remove files used only by the retired artifact protocol.**
- [x] **Step 3: Rewrite retained analysis references so they no longer depend on staged artifacts or extra confirmations.**
- [x] **Step 4: Replace fixture/schema-dependent collector tests with direct temporary-Git-repository tests.**
- [x] **Step 5: Search the installable Skill and README for legacy artifact names and remove remaining runtime references.**
- [x] **Step 6: Keep `collect_git_evidence.py` and its focused tests because Git discovery still uses contributor and commit evidence.**

### Task 5: Verify The Release Surface

**Files:**
- Verify: all remaining tracked files

**Interfaces:**
- Consumes: Completed implementation.
- Produces: Evidence that the reduced repository and new behavior are internally consistent.

- [x] **Step 1: Run `python -m unittest discover -s tests -v`.**
- [x] **Step 2: Run limited Codex acceptance for both routes; verify the named-feature route skips Git identity, the Git-discovery route confirms Git identity and target role together, and both create only the final Markdown.**
- [x] **Step 3: Run `git diff --check`.**
- [x] **Step 4: Inspect `git status --short` and the complete diff for accidental or unrelated changes.**
- [x] **Step 5: Run `python -m compileall -q skills tests`.**

Forward-validation scope: one controlled Codex run per route on 2026-07-31. DS, Claude, and a full multi-model matrix were not run and are not claimed.
