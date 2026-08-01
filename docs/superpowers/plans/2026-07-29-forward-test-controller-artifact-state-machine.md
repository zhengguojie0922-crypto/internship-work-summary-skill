# Forward-Test Controller Artifact State Machine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the green controller's fixed four-turn progression with an auditable, artifact-driven state machine that retries the actual incomplete stage and stops early on workflow completion.

**Architecture:** Keep the baseline prompt path byte-for-byte unchanged. Add pure helpers that recognize exact canonical headings and choose the earliest incomplete stage, a single green continuation builder that repeats the original request and authorized decisions, and a dynamic run loop with an eight-turn ceiling and explicit controller-state records.

**Tech Stack:** Python 3.10+ standard library, `unittest`, subprocess JSONL fixtures, existing forward-test runner.

## Global Constraints

- Modify only `tests/forward_test_runner.py`, `tests/test_forward_test_runner.py`, and controller design/plan/audit records.
- Do not modify the Skill, grader, grading thresholds, scenarios, fixtures, required/forbidden claims, required questions, or rubrics.
- Controller state must not read grading-only scenario fields.
- Green continuations must retain the exact fixture binding, read-only policy, chat-only policy, original-request authority, and hidden-grading-data exclusions.
- Baseline initial and continuation prompt text must remain byte-for-byte unchanged and execute at most its four legacy prompts.
- Green maximum turns default to 8; fixture repositories remain read-only.
- The workspace is not a Git repository, so commit steps are recorded as unavailable rather than simulated.

---

### Task 1: Canonical Artifact Recognition And Stage Selection

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Produces: `_detect_canonical_artifacts(text_parts: Sequence[str]) -> tuple[str, ...]`
- Produces: `_next_workflow_stage(detected: Sequence[str]) -> str`
- Produces: `WORKFLOW_STAGE_ARTIFACTS`, ordered as evidence, facts, career

- [ ] **Step 1: Write the failing exact-heading and stage-order tests**

Add a focused test that obtains the new helpers through the loaded runner module,
so the initial RED is an assertion failure rather than an import error:

```python
def test_controller_detects_only_exact_canonical_headings_and_selects_first_incomplete_stage(self) -> None:
    runner = sys.modules[run_one.__module__]
    detector = getattr(runner, "_detect_canonical_artifacts", None)
    selector = getattr(runner, "_next_workflow_stage", None)
    self.assertIsNotNone(detector)
    self.assertIsNotNone(selector)

    text = [
        "Mention evidence-report.json in prose only.\n"
        "## evidence-report.json\n{}\n"
        "### EVIDENCE-REPORT.MD   \nbody\n"
        "`## fact-cards.json` is code, not a heading."
    ]
    self.assertEqual(
        ("evidence-report.json", "evidence-report.md"),
        detector(text),
    )
    self.assertEqual(
        (),
        detector(["```markdown\n## fact-cards.json\n```\n    ## resume-audit.json\n\t## career-package.md"]),
    )
    self.assertEqual(
        ("fact-cards.json", "fact-cards.md"),
        detector(["## fact-cards.json\r\n### FACT-CARDS.MD   \r\n"]),
    )
    self.assertEqual("facts", selector(detector(text)))
    self.assertEqual(
        "evidence",
        selector(("fact-cards.json", "fact-cards.md", "career-package.md", "resume-audit.json")),
    )
    self.assertEqual(
        "complete",
        selector((
            "evidence-report.json", "evidence-report.md",
            "fact-cards.json", "fact-cards.md",
            "career-package.md", "resume-audit.json",
        )),
    )
```

Add `import sys` to the test module.

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```powershell
python -m unittest tests.test_forward_test_runner.ForwardRunnerTests.test_controller_detects_only_exact_canonical_headings_and_selects_first_incomplete_stage -v
```

Expected: FAIL because `_detect_canonical_artifacts` and
`_next_workflow_stage` do not exist.

- [ ] **Step 3: Implement the minimal pure helpers**

Add ordered canonical constants and helpers near the existing artifact constants:

```python
MAX_TURNS = 8
BASELINE_MAX_TURNS = 4
CANONICAL_ARTIFACTS = (
    "session.json",
    "evidence-report.json",
    "evidence-report.md",
    "fact-cards.json",
    "fact-cards.md",
    "career-package.md",
    "resume-audit.json",
)
WORKFLOW_STAGE_ARTIFACTS = (
    ("evidence", ("evidence-report.json", "evidence-report.md")),
    ("facts", ("fact-cards.json", "fact-cards.md")),
    ("career", ("career-package.md", "resume-audit.json")),
)

def _detect_canonical_artifacts(text_parts: Sequence[str]) -> tuple[str, ...]:
    text = "\n".join(text_parts)
    detected: set[str] = set()
    fence: tuple[str, int] | None = None
    canonical_by_case = {name.casefold(): name for name in CANONICAL_ARTIFACTS}
    for line in text.splitlines():
        if fence is not None:
            marker, minimum_length = fence
            if re.fullmatch(rf" {{0,3}}{re.escape(marker)}{{{minimum_length},}}[ \t]*", line):
                fence = None
            continue
        opening_fence = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if opening_fence:
            marker = opening_fence.group(1)
            fence = (marker[0], len(marker))
            continue
        heading = re.fullmatch(r" {0,3}#{1,6}[ \t]+(.*?)[ \t]*", line)
        if heading:
            canonical = canonical_by_case.get(heading.group(1).casefold())
            if canonical:
                detected.add(canonical)
    return tuple(name for name in CANONICAL_ARTIFACTS if name in detected)

def _next_workflow_stage(detected: Sequence[str]) -> str:
    available = set(detected)
    for stage, required in WORKFLOW_STAGE_ARTIFACTS:
        if not set(required).issubset(available):
            return stage
    return "complete"
```

Keep `ARTIFACT_BASENAMES` for the unchanged grader path.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run the Step 2 command. Expected: 1 test, OK.

---

### Task 2: Idempotent Green Continuation Builder

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Consumes: `_next_workflow_stage`, `CANONICAL_ARTIFACTS`, scenario `id`, `mode`, and `user_prompt`
- Produces: `_green_continuation(scenario, repository, fixture_binding, stage, detected) -> str`

- [ ] **Step 1: Write failing prompt-contract tests**

Add one strict-mode test and one fast/algorithm test. The strict test must assert
that each continuation includes the verbatim original request, authority text,
fixture binding, chat-only policy, no-write policy, and only the current missing
stage artifacts. It must also assert that facts-stage retries contain every
existing decision-closure sentence.

The fast test must assert that all missing canonical artifacts are requested in
one response and that an algorithm evidence retry contains this source-derived
decision without either hidden claim:

```python
"The claim to assess is exactly the original user request: whether the account settings code can support an algorithm engineering contribution claim."
```

The algorithm facts prompt must begin with `I confirm the evidence report as
written.`, answer both inclusion choices with first-person `I choose yes`, and
state that the schema-valid unsupported-claim output is
`fact-cards.json` with `work_items: []`; it must forbid creating a contribution
fact from absence.

For every produced prompt, reuse the existing hidden-values loop over
`required_claims`, `forbidden_claims`, `required_questions`, and `rubric`.

- [ ] **Step 2: Run the new prompt tests and verify RED**

Run the two new tests by full unittest name. Expected: FAIL because
`_green_continuation` does not exist.

- [ ] **Step 3: Implement the continuation builder**

Extract the existing fixture continuation prefix and use deterministic stage
blocks:

```python
def _missing_artifacts(stage: str, detected: Sequence[str], *, fast: bool) -> tuple[str, ...]:
    available = set(detected)
    if fast:
        return tuple(name for name in CANONICAL_ARTIFACTS if name not in available)
    required = dict(WORKFLOW_STAGE_ARTIFACTS)[stage]
    if stage == "evidence" and "session.json" not in available:
        required = ("session.json", *required)
    return tuple(name for name in required if name not in available)

def _canonical_request(names: Sequence[str], *, fast: bool) -> str:
    joined = ", ".join(names)
    mode = "in one response" if fast else "for the current stage"
    return f"Under the exact canonical Markdown headings, complete {joined} {mode}."
```

Build `_green_continuation` from:

1. exact repository continuation and fixture binding;
2. `ORIGINAL_REQUEST_PROTOCOL` and `Original user request:\n{scenario['user_prompt']}`;
3. scope, evidence, or facts confirmations selected by actual stage;
4. algorithm context/claim closure when applicable;
5. chat-only and no-fixture-write policy;
6. `_canonical_request` for current missing artifacts.

For fast mode, include scope plus evidence and facts closures together and pass
`fast=True`. Do not read any scenario field except `id`, `mode`, and
`user_prompt`.

- [ ] **Step 4: Run the prompt-contract tests and existing hidden-data tests**

Run:

```powershell
python -m unittest tests.test_forward_test_runner.ForwardRunnerTests.test_green_continuation_repeats_authority_and_requests_only_the_incomplete_stage tests.test_forward_test_runner.ForwardRunnerTests.test_fast_and_algorithm_continuations_close_decisions_without_grading_leak tests.test_forward_test_runner.ForwardRunnerTests.test_all_generated_prompts_keep_grading_data_hidden -v
```

Expected: 3 tests, OK after updating the existing hidden-data fake responses to
emit the canonical artifacts needed for deterministic stage traversal.

---

### Task 3: Adaptive Run Loop, Early Stop, And Audit State

**Files:**
- Modify: `tests/test_forward_test_runner.py`
- Modify: `tests/forward_test_runner.py`

**Interfaces:**
- Consumes: `_detect_canonical_artifacts`, `_next_workflow_stage`, `_green_continuation`
- Produces in each green turn: `controller_state.detected_artifacts`, `controller_state.cumulative_artifacts`, `controller_state.next_stage`
- Produces in each run: `controller_stop_reason`, `controller_stage`, `detected_artifacts`

- [ ] **Step 1: Write failing strict retry and early-stop tests**

Create a fake Codex process whose assistant outputs by call are:

```python
[
    "Scope only; evidence-report.json is mentioned in prose.",
    "## evidence-report.json\n{}\n## evidence-report.md\nbody",
    "Still asking for confirmation; no new artifact heading.",
    "## fact-cards.json\n{}\n## fact-cards.md\nbody",
    "## career-package.md\nbody\n## resume-audit.json\n{}",
]
```

Assert the generated stages are evidence, facts, facts, career; the controller
uses five turns, stops before eight, records `workflow_complete`, and preserves
cumulative artifacts in canonical order.

- [ ] **Step 2: Run the strict adaptive test and verify RED**

Expected: FAIL because the current runner still precomputes a fixed sequence.

- [ ] **Step 3: Write failing fast and exhaustion tests**

Fast test: turn 1 returns scope only, turn 2 returns all seven exact headings.
Assert exactly two calls and `workflow_complete`.

Exhaustion test: every turn returns only a question. Run with `max_turns=8` and
assert eight calls, stage `evidence`, and `max_turns_exhausted`.

- [ ] **Step 4: Run the new tests and verify RED**

Expected: both fail under fixed prompt generation and missing audit fields.

- [ ] **Step 5: Refactor `run_one` to generate green prompts after each turn**

Preserve initial prompt construction. Preserve baseline prompt construction in
its existing order and text. Replace the precomputed green follow-ups with a
loop that:

```python
detected_artifacts: set[str] = set()
controller_stage = "evidence"
controller_stop_reason: str | None = None
prompts = [initial_prompt]

while len(turns) < max_turns and len(turns) < len(prompts):
    # Execute the existing subprocess/JSONL capture block unchanged.
    turn_detected = _detect_canonical_artifacts(text_parts) if controller_name == "green" else ()
    detected_artifacts.update(turn_detected)
    controller_stage = _next_workflow_stage(tuple(detected_artifacts)) if controller_name == "green" else "legacy"
    if controller_name == "green":
        turn["controller_state"] = {
            "detected_artifacts": list(turn_detected),
            "cumulative_artifacts": [name for name in CANONICAL_ARTIFACTS if name in detected_artifacts],
            "next_stage": controller_stage,
        }

    if return_code != 0:
        controller_stop_reason = "process_failed"
        break
    if not session_id:
        controller_stop_reason = "missing_session_id"
        break
    if controller_name == "green" and controller_stage == "complete":
        controller_stop_reason = "workflow_complete"
        break
    if len(turns) >= max_turns:
        controller_stop_reason = "max_turns_exhausted"
        break
    if controller_name == "baseline":
        if len(turns) >= len(prompts):
            controller_stop_reason = "legacy_sequence_complete"
            break
    else:
        prompts.append(_green_continuation(
            scenario,
            Path(str(fixture["repository_path"])),
            fixture_binding,
            controller_stage,
            tuple(detected_artifacts),
        ))
```

Construct the full baseline prompt list before the loop, capped by
`BASELINE_MAX_TURNS`. Validate `max_turns` against `MAX_TURNS=8`; baseline still
has only four prompts.

Add run-level fields using canonical order:

```python
"controller_stop_reason": controller_stop_reason,
"controller_stage": controller_stage,
"detected_artifacts": [name for name in CANONICAL_ARTIFACTS if name in detected_artifacts],
```

- [ ] **Step 6: Run all adaptive focused tests and verify GREEN**

Run the Task 1-3 focused test names together. Expected: all OK.

- [ ] **Step 7: Update fixed-sequence tests to assert state-driven behavior**

Replace fake responses such as `turn 1` with exact stage artifacts where the
test expects progression. Keep prompt content assertions, but assert retries
remain on the same stage when the fake emits no artifact. Update the baseline
test to call `max_turns=8` and still expect exactly the existing four prompts.

- [ ] **Step 8: Run the complete runner unit suite**

Run:

```powershell
python -m unittest tests.test_forward_test_runner -v
```

Expected: all runner tests pass with no errors or warnings.

---

### Task 4: Regression Verification And Final-9 Campaign

**Files:**
- Modify only if failures expose a controller bug: `tests/forward_test_runner.py`, `tests/test_forward_test_runner.py`
- Create: `.superpowers/codex-final-9-audit.md`
- Modify: `.superpowers/sdd/progress.md`

**Interfaces:**
- Uses unchanged CLI commands `prepare`, `run-matrix`, `grade-one`, and `summarize`
- Retains prefix `final-9`; never overwrites final-8

- [ ] **Step 1: Run fresh local verification**

Run:

```powershell
python -m unittest tests.test_skill_contract tests.test_forward_test_runner -v
python -m compileall tests skills
```

Expected: all tests pass and compileall exits 0.

- [ ] **Step 2: Verify Skill copies remain byte-identical**

Calculate SHA-256 for the repository Skill, prepared green controller Skill,
and installed Skill used by the campaign. Expected: all three equal the retained
digest `CF0834A7BED54862AD6889D7CD4DAB4F935E7F1A6CD1D25B151EF93B437C7F48`.

- [ ] **Step 3: Run Codex final-9**

Use the existing prepared runtime root and executable:

```powershell
python tests/forward_test_runner.py run-matrix --runtime-root <existing-fa2-root> --controller green --engine codex --executable <repo-root>/.superpowers/forward-codex-cli/node_modules/.bin/codex.cmd --model gpt-5.6-sol --runtime-metadata '{"cli_version":"0.145.0"}' --timeout-seconds 600 --max-turns 8 --runs-per-scenario 5 --run-id-prefix final-9 --workers 5
```

Run scenarios sequentially if the complete matrix would exceed the host's
one-hour command limit. Preserve all run records.

- [ ] **Step 4: Audit every final-9 run**

For all 35 runs:

- confirm completion/runtime status and controller stop reason;
- create one manual review from the unchanged scenario rubric;
- run unchanged `grade-one`;
- verify exact fixture cleanliness with `git status --short --untracked-files=all`;
- summarize artifact, forbidden-claim, citation, semantic, question, and score
  gates in `.superpowers/codex-final-9-audit.md`.

- [ ] **Step 5: Apply the acceptance gate**

Proceed to packaging only if every scenario is 5/5, all 35 runs complete, all
fixtures are clean, and all grader gates pass. Otherwise retain final-9, record
the evidence-backed blocker, and do not claim GitHub release readiness.

Do not run Claude or send any material to Anthropic without separate explicit
authorization.
