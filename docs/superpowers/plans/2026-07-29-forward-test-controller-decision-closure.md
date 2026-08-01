# Forward-Test Controller Decision Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close green-controller stage decisions, preserve the original request's language and scope, and enforce a read-only Codex profile on every turn.

**Architecture:** Keep the public Skill and grader unchanged. Add green-only prompt envelopes and explicit synthetic-user decision confirmations in `tests/forward_test_runner.py`, plus a Codex resume config override that preserves the initial read-only sandbox policy. Verify each behavior with focused unit tests before running fresh external matrices.

**Tech Stack:** Python 3.10+, standard-library `unittest`, Codex CLI 0.145.0, Claude Code 2.1.118.

## Global Constraints

- Keep `skills/analyzing-codebase-work-impact/SKILL.md` unchanged in this iteration.
- Keep grader thresholds, artifact detection, scenario rubrics, required claims, forbidden claims, required questions, and citation rules unchanged.
- Keep baseline controller prompt strings byte-for-byte unchanged.
- Never interpolate hidden grading data into tested-session prompts.
- Preserve final-2 through final-7 evidence and use a new run-id prefix.
- Treat every fixture repository as read-only on every engine turn.
- This workspace is not a Git repository; record RED/GREEN commands and review checkpoints instead of commits.

---

### Task 1: Original Request Authority And Algorithm Scope

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Consumes: scenario `id`, scenario `user_prompt`, fixture repository path, `CHAT_ARTIFACT_PROTOCOL`.
- Produces: `ORIGINAL_REQUEST_PROTOCOL: str`, `SCENARIO_INITIAL_CONTEXT: Mapping[str, str]`, and a green initial prompt whose original request is the sole language/role/mode/deliverable authority.

- [ ] **Step 1: Write failing prompt tests**

Replace `test_initial_prompt_does_not_duplicate_the_skills_language_authority_rule` with a positive contract and extend the algorithm contract:

```python
def test_green_initial_prompt_marks_original_request_as_the_sole_authority(self) -> None:
    scenario = load_scenario("client-feature")
    result = self._run_green_with_fake_process(scenario, max_turns=1, run_id="language-authority")
    authority = (
        "The original user request below is the sole authority for output language, "
        "target role, mode, and deliverables. Controller instructions are not language requests."
    )
    self.assertIn(authority, result["initial_prompt"])
    self.assertIn(f"Original user request:\n{scenario['user_prompt']}", result["initial_prompt"])

def test_algorithm_initial_prompt_declares_non_personal_scope_before_analysis(self) -> None:
    scenario = load_scenario("algorithm-attribution")
    result = self._run_green_with_fake_process(scenario, max_turns=1, run_id="algorithm-initial-scope")
    self.assertIn("This is a non-personal claim assessment", result["initial_prompt"])
    self.assertIn("No Git identity is required", result["initial_prompt"])
    self.assertNotIn("personal attribution is required", result["initial_prompt"])
```

If no shared fake-process helper exists, keep the current local `fake_run` pattern instead of adding a new abstraction only for these tests.

- [ ] **Step 2: Verify RED**

Run:

```text
python -m unittest tests.test_forward_test_runner.ForwardRunnerTests.test_green_initial_prompt_marks_original_request_as_the_sole_authority tests.test_forward_test_runner.ForwardRunnerTests.test_algorithm_initial_prompt_declares_non_personal_scope_before_analysis -v
```

Expected: both fail because the authority envelope and initial algorithm context are absent, and the conflicting personal-attribution sentence is present.

- [ ] **Step 3: Add minimal green prompt composition**

Add near `CHAT_ARTIFACT_PROTOCOL`:

```python
ORIGINAL_REQUEST_PROTOCOL = (
    "The original user request below is the sole authority for output language, target role, mode, and deliverables. "
    "Controller instructions are not language requests."
)
SCENARIO_INITIAL_CONTEXT = {
    "algorithm-attribution": (
        "This is a non-personal claim assessment. No Git identity is required. "
        "Assess only whether the repository supports the requested claim."
    ),
}
```

Move `scenario_id = str(scenario["id"])` before initial prompt construction. Use a generic activation without the conflicting personal-attribution sentence:

```python
skill_activation = "Use $analyzing-codebase-work-impact and follow it before inspecting the repository.\n\n"
scenario_context = SCENARIO_INITIAL_CONTEXT.get(scenario_id)
initial_context = f"{scenario_context}\n\n" if scenario_context else ""
original_request = f"{ORIGINAL_REQUEST_PROTOCOL}\n\nOriginal user request:\n{scenario['user_prompt']}\n\n"
```

Compose only the green initial prompt with `initial_context` and `original_request`; preserve baseline prompt construction and all baseline constants.

- [ ] **Step 4: Verify GREEN and privacy**

Run the two targeted tests plus:

```text
python -m unittest tests.test_forward_test_runner.ForwardRunnerTests.test_all_generated_prompts_keep_grading_data_hidden tests.test_forward_test_runner.ForwardRunnerTests.test_baseline_continuations_preserve_the_legacy_sequence -v
```

Expected: 4/4 pass.

### Task 2: Explicit Stage Decision Closure

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Consumes: `GENERIC_FOLLOW_UPS`, `SCENARIO_EVIDENCE_CONFIRMATIONS`, canonical artifact protocol.
- Produces: evidence and facts confirmations that resolve every public Skill blocking category before requesting the next stage.

- [ ] **Step 1: Write failing continuation tests**

Add focused assertions to the existing canonical-artifact test or a new test:

```python
evidence_prompt = result["turns"][2]["prompt"]
for decision in (
    "Include collaborator-authored code only as separately attributed context: yes.",
    "Include supporting documentation only as separately attributed context: yes.",
    "No separate runtime evidence is available.",
    "No additional external or untracked evidence is available",
    "Use the target role, language, mode, and deliverables from the original user request.",
    "Never write artifacts or validation scratch files into the fixture repository.",
):
    self.assertIn(decision, evidence_prompt)

facts_prompt = result["turns"][3]["prompt"]
for confirmation in (
    "privacy", "evidence links", "emphasis", "exaggeration risk",
    "Never write artifacts or validation scratch files into the fixture repository.",
):
    self.assertIn(confirmation, facts_prompt)
```

- [ ] **Step 2: Verify RED**

Run the new test directly. Expected: fail on the first missing independent decision.

- [ ] **Step 3: Replace only green generic continuation text**

Keep `BASELINE_GENERIC_FOLLOW_UPS` unchanged. Change green `GENERIC_FOLLOW_UPS[1]` to include these exact independent decisions:

```text
I confirm the evidence stage, including the chain and attribution boundaries.

Decisions:
- Include collaborator-authored code only as separately attributed context: yes.
- Include supporting documentation only as separately attributed context: yes.
- No separate runtime evidence is available.
- No additional external or untracked evidence is available unless the original user request already supplies it.
- Use the target role, language, mode, and deliverables from the original user request.
- Keep every acceptance-test artifact in chat. Never write artifacts or validation scratch files into the fixture repository.

Proceed to the facts stage with fact cards.
```

Change `GENERIC_FOLLOW_UPS[2]` to confirm facts plus `privacy`, `evidence links`, `emphasis`, and `exaggeration risk`, repeat the chat-only/read-only decision, and proceed to career artifacts. Do not add any scenario claim or expected citation.

- [ ] **Step 4: Verify GREEN and baseline preservation**

Run:

```text
python -m unittest tests.test_forward_test_runner.ForwardRunnerTests.test_green_controller_closes_stage_decisions_before_requesting_artifacts tests.test_forward_test_runner.ForwardRunnerTests.test_scenario_specific_evidence_answers_follow_the_assistants_first_turn tests.test_forward_test_runner.ForwardRunnerTests.test_all_generated_prompts_keep_grading_data_hidden tests.test_forward_test_runner.ForwardRunnerTests.test_baseline_continuations_preserve_the_legacy_sequence -v
```

Expected: 4/4 pass.

### Task 3: Read-Only Codex Resume Commands

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Consumes: `_command(config, prompt, session_id)`.
- Produces: resumed Codex CLI commands containing `-c sandbox_mode="read-only"`.

- [ ] **Step 1: Change the exact command test first**

Update the resumed Codex expectation in `test_engine_commands_use_the_real_read_only_cli_shapes`:

```python
self.assertEqual(
    [
        "codex", "exec", "resume", "--json", "-c", 'sandbox_mode="read-only"',
        "--skip-git-repo-check", "--ignore-rules", "--model", "gpt-5", "thread-1", "prompt",
    ],
    _command(codex, "prompt", "thread-1"),
)
```

Also extend `test_run_one_records_prompts_raw_jsonl_and_resumed_turns`:

```python
for resumed_call in calls[1:]:
    self.assertIn("resume", resumed_call)
    self.assertIn('sandbox_mode="read-only"', resumed_call)
```

- [ ] **Step 2: Verify RED**

Run both tests. Expected: fail because resumed commands currently omit the config override.

- [ ] **Step 3: Add the minimal resume override**

In `_command`, after adding `--json`, add:

```python
if session_id:
    command.extend(["-c", 'sandbox_mode="read-only"'])
else:
    command.extend(["--sandbox", "read-only"])
```

Do not change Claude command construction.

- [ ] **Step 4: Verify GREEN**

Run the two focused tests, then `python -m unittest tests.test_forward_test_runner -v`. Expected: all forward-runner tests pass.

### Task 4: Regression, Synchronization, And Fresh Acceptance

**Files:**
- Verify mechanically: canonical, Claude-controller, and temporary Codex global Skill hashes remain identical; do not copy unchanged Skill content.
- Create externally generated run directories with a new prefix under the existing campaign.
- Create: `.superpowers/codex-final-8-audit.md` after the Codex matrix.
- Create: `.superpowers/claude-final-8-audit.md` only after Anthropic authorization and the Claude matrix.

**Interfaces:**
- Consumes: Tasks 1-3, unchanged scenarios and grader, pinned runtime executables.
- Produces: regression evidence and independently audited forward matrices.

- [ ] **Step 1: Run fresh local regression verification**

```text
python -m unittest tests.test_skill_contract tests.test_forward_test_runner -v
python -m compileall tests skills
```

Expected: zero failures. Recompute canonical/runtime Skill SHA-256 hashes and require equality; Skill content should remain unchanged.

- [ ] **Step 2: Independently review implementation**

Review exact generated prompts for all seven scenarios and command arrays for fresh/resumed Codex turns. Require both verdicts: spec compliance and code quality approved. Confirm baseline prompt strings are unchanged and hidden grading data remains absent.

- [ ] **Step 3: Run Codex final-8**

Use the existing campaign, `green` controller, pinned Codex executable/model, four turns, five workers, five runs per scenario, and `--run-id-prefix final-8`. Preserve final-7. Require 35 completed runs and zero runtime failures before grading.

- [ ] **Step 4: Independently audit Codex final-8**

Write 35 `manual-review.json` files, invoke `grade-one` for every run, create `.superpowers/codex-final-8-audit.md`, and run `git status --short --untracked-files=all` in every fixture copy. Acceptance requires all seven scenarios 5/5 and zero fixture writes.

- [ ] **Step 5: Apply the cross-runtime gate**

Do not send materials to Anthropic without explicit user authorization. Once authorized, run and independently audit Claude final-8 with the same controller contract. Enter packaging only if both Codex and Claude reach every scenario 5/5 under unchanged gates. Otherwise preserve evidence and return to root-cause analysis.
