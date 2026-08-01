# Feature Tracing Without Attribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow a natural-language feature-tracing request to inspect and summarize a feature chain without requiring or inferring personal Git attribution.

**Architecture:** Keep contribution discovery as the only path that produces personal contribution conclusions. Add an explicit feature-tracing branch before the personal identity gate; it follows source relationships and may use history as chronology, but does not ask for author identity or emit ownership claims. Combined runs retain both policies in their respective outputs.

**Tech Stack:** Markdown Skill instructions, Markdown README, Python `unittest` contracts.

## Global Constraints

- Keep analyzed repositories read-only and never execute their code.
- Do not weaken the existing evidence, privacy, or runtime-impact boundaries.
- Do not run model forward tests; run only targeted deterministic contracts.

---

### Task 1: Lock the entry-point boundary

**Files:**
- Modify: `tests/test_skill_contract.py`
- Modify: `skills/analyzing-codebase-work-impact/SKILL.md`

- [ ] **Step 1: Write the failing test**

Assert that a feature-tracing request with no personal identity bypasses the identity gate and prohibits author/ownership conclusions.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest discover -s tests -p "test_skill_contract.py" -v`

- [ ] **Step 3: Write minimal implementation**

Add a feature-tracing route that records attribution as not applicable for the feature summary, follows source-visible relationships, and keeps Git history chronological only.

- [ ] **Step 4: Run the targeted contract suite**

Run: `python -m unittest discover -s tests -p "test_skill_contract.py" -v`

### Task 2: Align user documentation

**Files:**
- Modify: `README.md`
- Modify: `tests/test_packaging.py`

- [ ] **Step 1: Write the failing test**

Assert that README separates contribution discovery attribution from author-independent feature tracing.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_packaging -v`

- [ ] **Step 3: Write minimal implementation**

Replace the feature-tracing example and workflow description so it requests a feature chain rather than personal attribution or a career package.

- [ ] **Step 4: Run publishing contracts**

Run: `python -m unittest tests.test_packaging -v`

### Task 3: Verify the changed surface

- [ ] **Step 1: Run affected contracts**

Run: `python -m unittest discover -s tests -p "test_skill_contract.py" -v` and `python -m unittest tests.test_packaging -v`.

- [ ] **Step 2: Check whitespace and changed files**

Run: `git diff --check` and `git status --short`.
