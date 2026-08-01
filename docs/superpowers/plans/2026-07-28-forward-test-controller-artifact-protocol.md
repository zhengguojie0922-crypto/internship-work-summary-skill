# Forward-Test Controller Artifact Protocol Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make file and chat-only Skill delivery use the same canonical artifact filenames, and make the green forward-test controller request that public contract without leaking scoring data.

**Architecture:** Add a format rule to the Skill's existing four-stage state machine and a generic chat artifact envelope to green controller prompts. Keep baseline prompts and exact filesystem artifact detection unchanged. Verify the change with static Skill contracts, generated-prompt tests, then fresh Claude and Codex matrices.

**Tech Stack:** Python 3.10+, standard-library `unittest`, Markdown Agent Skill, Claude Code 2.1.118, Codex CLI 0.145.0.

## Global Constraints

- Preserve every `final-2` through `final-6` run and audit; never overwrite failed evidence.
- Do not expose scenario rubric, required claims, forbidden claims, fixture conclusions, or expected citations to tested sessions.
- Keep fixture repositories read-only and network-disabled except for the explicitly authorized model API calls.
- Treat exact canonical filenames as the only artifact namespace in files and chat.
- Keep baseline controller prompts unchanged.
- This workspace is not a Git repository, so commit steps are unavailable; record test checkpoints instead.

---

### Task 1: Skill Chat Artifact Contract

**Files:**
- Modify: `tests/test_skill_contract.py`
- Modify: `skills/analyzing-codebase-work-impact/SKILL.md`

**Interfaces:**
- Consumes: the existing `Run Four Resumable Stages` artifact table.
- Produces: a canonical chat heading contract covering all seven filenames.

- [ ] **Step 1: Write the failing contract test**

Add a test that extracts `Run Four Resumable Stages` and requires these exact rules:

```python
def test_skill_uses_canonical_artifact_filenames_for_file_and_chat_delivery(self) -> None:
    stages = section(self.body, "Run Four Resumable Stages")
    for contract in (
        "Use the exact canonical filename for every file artifact and every chat-only artifact heading",
        "In chat-only mode, write `## <canonical filename>` before the complete artifact body",
        "Never replace a canonical filename with a translated or friendly-only heading",
        "Keep canonical filenames unchanged in Chinese, English, and bilingual output",
    ):
        self.assertIn(contract, stages)
```

- [ ] **Step 2: Verify RED**

Run:

```text
python -m unittest tests.test_skill_contract.SkillContractTests.test_skill_uses_canonical_artifact_filenames_for_file_and_chat_delivery -v
```

Expected: FAIL because the four format rules are absent.

- [ ] **Step 3: Add the minimal Skill rule**

Add imperative prose immediately before the stage table:

```text
Use the exact canonical filename for every file artifact and every chat-only artifact heading. In chat-only mode, write `## <canonical filename>` before the complete artifact body. Never replace a canonical filename with a translated or friendly-only heading. Keep canonical filenames unchanged in Chinese, English, and bilingual output.
```

- [ ] **Step 4: Verify GREEN**

Run the targeted test and `test_workflow_instruction_sentences_use_imperative_voice`; expect both to pass.

### Task 2: Green Controller Delivery Envelope

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Consumes: `run_one(...)`, `GENERIC_FOLLOW_UPS`, and the installed Skill contract.
- Produces: `CHAT_ARTIFACT_PROTOCOL: str` and stage-specific green follow-up prompts.

- [ ] **Step 1: Write failing prompt tests**

Add tests that run a green scenario with a fake process runner and assert:

```python
canonical = (
    "session.json", "evidence-report.json", "evidence-report.md",
    "fact-cards.json", "fact-cards.md", "career-package.md", "resume-audit.json",
)
self.assertTrue(all(name in result["initial_prompt"] for name in canonical))
self.assertIn("exact canonical filenames as Markdown headings", result["initial_prompt"])
self.assertIn("evidence-report.json", result["turns"][1]["prompt"])
self.assertIn("fact-cards.json", result["turns"][2]["prompt"])
self.assertIn("resume-audit.json", result["turns"][3]["prompt"])
```

Add a fast-mode assertion that the initial prompt says to emit all four stages in one response. Re-run the existing hidden-grading-data test unchanged.

- [ ] **Step 2: Verify RED**

Run the new prompt tests; expect failures because the green controller has no canonical delivery envelope.

- [ ] **Step 3: Add the green-only protocol**

Define:

```python
CHAT_ARTIFACT_PROTOCOL = (
    "For chat-only delivery, use these exact canonical filenames as Markdown headings and include each complete artifact body: "
    "session.json, evidence-report.json, evidence-report.md, fact-cards.json, fact-cards.md, career-package.md, resume-audit.json. "
    "Do not replace canonical filenames with friendly or translated headings. "
    "In strict mode emit only the current stage artifacts; in fast mode emit all four stages in one response."
)
```

Append it only to the green initial prompt. Update green follow-ups to request:

```text
scope confirmation -> evidence-report.json and evidence-report.md
evidence confirmation -> fact-cards.json and fact-cards.md
facts confirmation -> career-package.md and resume-audit.json
```

Keep `BASELINE_GENERIC_FOLLOW_UPS` and `BASELINE_SCENARIO_CONFIRMATIONS` byte-for-byte unchanged.

- [ ] **Step 4: Verify GREEN**

Run the new prompt tests plus all existing forward-runner tests; expect no failures.

### Task 3: Regression Verification And Runtime Synchronization

**Files:**
- Modify mechanically: Claude green controller Skill copy.
- Modify mechanically: temporary Codex global Skill copy.

**Interfaces:**
- Consumes: canonical `skills/analyzing-codebase-work-impact/SKILL.md`.
- Produces: three byte-identical Skill installations.

- [ ] **Step 1: Run relevant tests**

```text
python -m unittest tests.test_skill_contract tests.test_forward_test_runner -v
```

Expected: all tests pass with zero failures.

- [ ] **Step 2: Synchronize and hash**

Copy canonical `SKILL.md` to the Claude green controller and temporary Codex global Skill directory. Run `Get-FileHash -Algorithm SHA256` on all three paths and require identical hashes.

- [ ] **Step 3: Preserve historical evidence**

Assert that `final-6` run counts and audit reports remain present before starting new tests.

### Task 4: Final-7 Forward Matrices And Independent Audit

**Files:**
- Create externally generated `final-7-*` run directories under the existing `fa2` campaign.
- Create: `.superpowers/claude-final-7-audit.md`
- Create: `.superpowers/codex-final-7-audit.md`

**Interfaces:**
- Consumes: synchronized green controllers and the existing seven scenarios.
- Produces: 70 new run records, 70 manual reviews, 70 final grades, and two audit reports.

- [ ] **Step 1: Run Claude matrix**

Run 7 scenarios x 5 runs with prefix `final-7`, four turns, five workers, and the approved elevated Claude session permissions. Require 35 completed runs and zero runtime failures.

- [ ] **Step 2: Run Codex matrix**

Run the identical matrix with the pinned project-local Codex executable and the user's explicit authorization to send synthetic Skill/controller prompts and fixture repositories to OpenAI. Require 35 completed runs and zero runtime failures.

- [ ] **Step 3: Independently audit all results**

For each run, write `manual-review.json`, invoke `grade-one`, and verify artifact, forbidden-claim, citation, question, average, and individual-score gates. Do not auto-award semantic scores.

- [ ] **Step 4: Apply the acceptance gate**

Proceed to packaging only if both runtime/model combinations pass every scenario 5/5. If either fails, preserve evidence and return to root-cause analysis without weakening the grader or adding expected answers to prompts.

### Task 5: Packaging And Final Verification

**Files:**
- Modify only after final-7 acceptance: `README.md`, `tests/test_packaging.py`, canonical baseline/result archives.

**Interfaces:**
- Consumes: accepted independent final-7 audits.
- Produces: release-ready documentation and packaged test evidence.

- [ ] **Step 1: Archive accepted evidence and update release documentation**

Record test date, exact runtime/model versions, authentic RED/GREEN rates, and unverified model variants. Keep earlier failed rounds.

- [ ] **Step 2: Remove the temporary Codex global Skill installation**

Remove only `<user-home>/.codex/skills/analyzing-codebase-work-impact` after all Codex tests finish and verify the exact target before deletion.

- [ ] **Step 3: Run fresh final verification**

```text
python -m unittest discover -s tests -v
python -m compileall skills tests
python <skill-creator-path>/quick_validate.py skills/analyzing-codebase-work-impact
```

Require zero failures and report that Git commit, merge, and PR operations are unavailable because the workspace is not a Git repository.
