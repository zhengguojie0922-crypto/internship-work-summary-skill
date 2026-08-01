# Unsupported Non-Personal Claim Terminal Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow an evidence-backed non-personal claim assessment to finish with empty fact-card and resume-audit collections when the target-role claim is unsupported and no external evidence exists.

**Architecture:** Add one conditional terminal recipe to the Skill contract. Reuse the existing schemas, validators, stage machine, canonical filenames, and controller behavior; prove the contract with a structural test and then with an external Codex forward-test probe.

**Tech Stack:** Markdown Agent Skill, Python `unittest`, JSON Schema artifacts, OpenAI Codex CLI.

## Global Constraints

- Preserve strict and fast four-stage behavior.
- Preserve requested language, fixture binding, read-only analysis, and chat-only output rules.
- Do not infer personal contribution or target-role implementation from missing evidence.
- Do not send test material to Anthropic Claude without separate authorization.
- This workspace is not a Git repository; commit steps are not applicable.

---

### Task 1: Add the terminal-path Skill contract

**Files:**
- Modify: `tests/test_skill_contract.py`
- Modify: `skills/analyzing-codebase-work-impact/SKILL.md`

**Interfaces:**
- Consumes: `section(body, heading)` structural contract helper and existing Source-Only Hard Gate.
- Produces: a `Close Unsupported Non-Personal Claims` Skill section with a deterministic facts/career recipe.

- [ ] **Step 1: Write the failing structural test**

Add one test that requires the three activation predicates, treats the external-evidence answer as resolved, requires `work_items: []` and `entries: []`, requires an unsupported-claim refusal and inspected-scope boundary, and forbids generating contribution or resume facts from absence.

- [ ] **Step 2: Run the focused test to verify RED**

Run: `python -m unittest tests.test_skill_contract.SkillContractTests.test_skill_closes_unsupported_non_personal_claims -v`

Expected: FAIL because `Close Unsupported Non-Personal Claims` is absent.

- [ ] **Step 3: Add the minimal Skill recipe**

Insert the terminal section immediately after `Source-Only Hard Gate`. Key it to all three observable predicates and define the four canonical artifact outputs without changing schemas or controller code.

- [ ] **Step 4: Run focused and full Skill tests**

Run: `python -m unittest tests.test_skill_contract.SkillContractTests.test_skill_closes_unsupported_non_personal_claims -v`

Expected: PASS.

Run: `python -m unittest tests.test_skill_contract -v`

Expected: all tests pass.

### Task 2: Verify, synchronize, and review

**Files:**
- Update: `.superpowers/sdd/progress.md`
- Synchronize: green controller Skill copy
- Synchronize: installed Codex Skill copy

**Interfaces:**
- Consumes: the source Skill from Task 1.
- Produces: three byte-identical deployed Skill copies and fresh local verification evidence.

- [ ] **Step 1: Run regression and syntax suites**

Run: `python -m unittest tests.test_skill_contract tests.test_forward_test_runner -v`

Run: `python -m compileall tests skills`

Expected: exit code 0 for both.

- [ ] **Step 2: Validate the Skill folder**

Run the available `quick_validate.py` against `skills/analyzing-codebase-work-impact` and resolve any reported error.

- [ ] **Step 3: Synchronize deployed copies**

Copy the complete source Skill directory to the green controller installation and the local Codex skills installation without changing test fixtures or result records.

- [ ] **Step 4: Verify deployment hashes**

Compute SHA-256 for all three `SKILL.md` files and require exact equality.

- [ ] **Step 5: Request an independent review**

Review the diff against the design and original release contract. Resolve every Critical or Important finding before forward testing.

### Task 3: Forward-test and resume release gates

**Files:**
- Create: new immutable records under the configured forward-test runtime root
- Update: `.superpowers/sdd/progress.md`

**Interfaces:**
- Consumes: synchronized green Skill, algorithm scenario, feature-chain fixture, artifact-driven controller.
- Produces: a successful probe, then a five-run algorithm gate, followed by the remaining authorized Codex matrix when eligible.

- [ ] **Step 1: Run one external Codex algorithm probe**

Use a new run ID. Require runtime completion, `workflow_complete`, both fact-card artifacts, both career artifacts, and `resume-audit.json` with no unsupported algorithm entry.

- [ ] **Step 2: Diagnose any probe failure from raw artifacts**

If the probe fails, preserve its record, identify the first violated contract boundary, add a failing regression test, and repeat RED-GREEN before another probe.

- [ ] **Step 3: Run the five-repetition algorithm gate**

Only after the probe passes, run five fresh algorithm repetitions and grade all results. Require 5/5 before proceeding.

- [ ] **Step 4: Resume the remaining Codex scenarios and release audit**

Run the other six scenarios at five repetitions each, preserve immutable results, apply the existing grader/manual review, and check fixture cleanliness. Do not run Claude tests without separate authorization.

### Task 4: Isolate the personal identity protocol

**Files:**
- Modify: `tests/test_skill_contract.py`
- Modify: `skills/analyzing-codebase-work-impact/SKILL.md`
- Create: `skills/analyzing-codebase-work-impact/references/identity-gate.md`

- [x] **Step 1: Write routing and reference-placement tests, then observe RED**

Require the attribution route before every other gate, prevent the non-personal branch from loading the identity reference, load it only for personal missing-identity requests, and forbid the exact identity question in the main Skill body.

- [x] **Step 2: Move the personal identity protocol and observe GREEN**

Keep the three-branch router in `SKILL.md`; move the exact question and complete personal first-turn stop contract to the directly linked identity reference. The focused RED produced three expected failures; the resulting Skill contract suite passes 34/34.

- [ ] **Step 3: Re-run deployment, review, and forward-test gates**

Run all local verification, synchronize the complete Skill directory to both deployed copies, obtain a clean independent review, then run a one-turn Codex micro-probe before a full algorithm probe.
