# Review Findings Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix evidence attribution, bound Git scanning, make the collector part of the Skill workflow, and align the single-document output and release contract.

**Architecture:** Keep the existing standard-library collector and single installable Skill. Tighten selection at the collector boundary, then encode the route and output contracts in `SKILL.md` and focused references; verify public packaging through existing unittest modules.

**Tech Stack:** Python 3.10+ standard library, Git 2.30+, Markdown, unittest.

## Global Constraints

- Modify only the isolated `codex/fix-review-findings` worktree in the new repository.
- Do not commit, push, create a pull request, tag, or Release.
- Do not restore retired fixtures, forward-test controllers, or runtime intermediate artifacts.
- The only artifact produced while using the Skill is `career-output/实习产出与面试准备.md`.
- Keep target-repository inspection read-only.

---

### Task 1: Correct Git identity selection and history bounds

**Files:**
- Modify: `tests/test_collect_git_evidence.py`
- Modify: `skills/summarizing-internship-work/scripts/collect_git_evidence.py`

**Interfaces:**
- Consumes: `collect --author <full-name-or-email>`, `--since`, `--until`, `--path`, `--max-commits`, and `--include-merges`.
- Produces: exact primary-author/co-author selection and a bounded `git log` query with the existing JSON report shape.

- [x] Add regression tests proving substring filters do not match, co-authors do match, and Git receives date/path/merge/limit filters.
- [x] Run the focused tests and confirm they fail for the expected missing behavior.
- [x] Implement normalized equality matching across authors and co-authors and bound `_parse_history` at the Git query.
- [x] Run the focused tests and confirm they pass.

### Task 2: Make the Skill workflow and output contract explicit

**Files:**
- Modify: `tests/test_skill_contract.py`
- Modify: `skills/summarizing-internship-work/SKILL.md`
- Modify: `skills/summarizing-internship-work/references/interview-expansion.md`

**Interfaces:**
- Consumes: named-feature personal requests, implementation-only feature requests, Git-discovery requests, mixed verification requests, and existing final documents.
- Produces: deterministic route selection, stdout-only collector use, bounded question output, and update-in-place final-document behavior.

- [x] Add contract tests for user-provided ownership, non-personal analysis, collector commands and errors, default-three output selection, separate scenario sets, evidence-shortfall behavior, and existing-document updates.
- [x] Run the contract tests and confirm they fail for the expected missing language.
- [x] Update the Skill and interview reference with the minimum explicit rules needed to pass.
- [x] Run the contract tests and confirm they pass.

### Task 3: Align packaging and release metadata

**Files:**
- Modify: `tests/test_packaging.py`
- Modify: `skills/summarizing-internship-work/VERSION`
- Modify: `README.md`

**Interfaces:**
- Consumes: installable Skill files and public repository documentation.
- Produces: version `1.1.0`, current route/output documentation, and a full-directory retired-name guard.

- [x] Add failing packaging assertions for `1.1.0`, the refined route/output contract, and retired-name scanning across the complete Skill directory.
- [x] Run the packaging tests and confirm they fail for the expected missing behavior.
- [x] Update version and README, and rename the disabled-hooks path prefix.
- [x] Run the packaging tests and confirm they pass.

### Task 4: Verify the complete uncommitted change

**Files:**
- Verify: `skills/`, `tests/`, `README.md`, and the two new planning documents.

**Interfaces:**
- Consumes: all changes from Tasks 1-3.
- Produces: fresh verification evidence and an inspectable uncommitted diff.

- [x] Run `python -m unittest discover -s tests -v` and require zero failures.
- [x] Run `python -m compileall -q skills tests` and require exit code 0.
- [x] Run `git diff --check` and require exit code 0.
- [x] Inspect `git status --short --branch` and `git diff --stat`; do not commit.
