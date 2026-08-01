# Forward-Test Controller Artifact State Machine Design

## 1. Problem

Codex final-8 completed 35/35 sessions without fixture writes, but only 1/35
passed. The controller used a fixed four-turn prompt sequence and advanced from
scope to evidence, facts, and career according to turn number. It did not check
whether the assistant had actually completed the preceding stage.

The final-8 transcripts show the architectural failure directly:

- 30/35 runs emitted `evidence-report.json` and `evidence-report.md` in turn 2,
  then emitted no new canonical artifact in turns 3 or 4.
- The assistant repeatedly reopened evidence confirmation, target role,
  collaborator/document inclusion, runtime evidence, identity, or scope
  decisions after the controller had answered them.
- All five algorithm runs treated the claim target as missing even though the
  original request stated the assessment to perform.
- Four fast-mode DevOps runs emitted all canonical artifacts in turn 2, but the
  fixed controller still sent later stage prompts.

Therefore, sending a continuation is not evidence that a stage advanced. The
assistant's canonical chat artifacts must be the source of truth for controller
progress.

## 2. Scope

This change is controller-only. It may modify:

- `tests/forward_test_runner.py`
- `tests/test_forward_test_runner.py`
- controller design, plan, and audit records under `docs/superpowers/` and
  `.superpowers/`

It must not modify:

- the installed or repository Skill
- the grader or grading thresholds
- scenario files, fixtures, required claims, forbidden claims, required
  questions, or rubric text
- the baseline controller's prompt text or fixed legacy sequence

The controller must not inspect grading-only scenario fields when choosing a
prompt or deciding whether the workflow is complete.

## 3. Considered Approaches

### 3.1 Longer fixed sequence

Increasing the fixed sequence from four to eight turns is simple, but preserves
the failed assumption that a sent prompt advances the assistant. It cannot
recover reliably from repeated questions or out-of-order artifacts.

### 3.2 Natural-language question parsing

Parsing pending questions and generating individual answers is flexible, but
depends on model-specific phrasing and language. It would create a large,
fragile policy surface and increase the risk of coupling the controller to
grading data.

### 3.3 Artifact-driven deterministic state machine

The selected approach recognizes exact canonical artifact headings in each
assistant turn, accumulates them across the session, and chooses the next prompt
from the first incomplete workflow stage. The prompt for a stage is idempotent:
repeating it repeats the same user-authorized decisions and requests only the
currently missing stage artifacts.

This approach is deterministic, language-independent, auditable, and directly
addresses the final-8 failure mode without reading grading fields.

## 4. Artifact Recognition

The recognizer examines assistant text only. A canonical artifact is present
when a line is a Markdown heading whose heading text is exactly one of:

- `session.json`
- `evidence-report.json`
- `evidence-report.md`
- `fact-cards.json`
- `fact-cards.md`
- `career-package.md`
- `resume-audit.json`

Recognition is case-insensitive, accepts Markdown heading levels 1 through 6,
accepts zero through three leading spaces, ignores trailing horizontal
whitespace, and handles LF or CRLF input. Headings inside backtick or tilde
fenced code blocks, four-space or tab-indented code, filename mentions in
prose, controller prompts, tool output, and files in the working directory do
not advance the state machine.

Artifact state is cumulative across completed assistant turns. Out-of-order
artifacts remain recorded, but the controller still requests the earliest
incomplete stage.

## 5. Workflow State

The green controller uses these stage completion sets:

| Stage | Completion artifacts |
|---|---|
| evidence | `evidence-report.json`, `evidence-report.md` |
| facts | `fact-cards.json`, `fact-cards.md` |
| career | `career-package.md`, `resume-audit.json` |

`session.json` is requested with the first strict-mode continuation and in every
fast-mode completion request, but it does not block terminal completion. This
keeps the controller aligned with the Skill's scope artifact without turning a
scenario-independent bookkeeping artifact into a new acceptance gate.

Strict mode selects the next action after every assistant turn:

1. If evidence is incomplete, confirm scope and request `session.json` plus the
   missing evidence artifacts.
2. If evidence is complete and facts are incomplete, close all evidence-stage
   decisions and request the missing facts artifacts.
3. If evidence and facts are complete and career is incomplete, confirm the
   facts-stage decisions and request the missing career artifacts.
4. If all three stage sets are complete, stop immediately with
   `workflow_complete`.

Fast mode does not impose strict-stage pauses. After every incomplete assistant
turn it repeats the scope decision, evidence/facts decision closure, original
request, and all missing canonical artifacts in a single-response request. It
stops immediately when the three stage sets are complete.

## 6. Continuation Contract

Every green continuation includes:

- the exact read-only fixture path and binding
- the original user request verbatim
- a statement that the original request remains the sole authority for
  language, target role, mode, and deliverables
- the chat-only and no-fixture-write rules
- the deterministic decisions appropriate to the current stage
- only the canonical artifacts missing from the current stage, except fast mode
  which requests all missing canonical workflow artifacts together

Evidence decision closure remains comprehensive and idempotent:

- the user confirms the evidence report as written in first person
- the user answers `yes` in first person to include collaborators and supporting
  documentation only as separately attributed context
- the user confirms in first person that no separate runtime evidence is
  available
- the user confirms in first person that no external or untracked evidence is
  available unless supplied by the original request
- the user confirms that target role, language, mode, and deliverables come
  from the original request
- the user confirms that artifacts and validation scratch files must not be
  written to the fixture

The algorithm scenario also restates, using only the original request, that the
claim target is whether the account-settings code supports an algorithm
engineering contribution claim. It states that the assessment is non-personal,
requires no Git identity, and has no untracked algorithm artifact or external
evidence. This does not disclose the scenario's required or forbidden claims.
After algorithm evidence is confirmed, the controller states the schema-valid
unsupported-claim path explicitly: `fact-cards.json` may use `work_items: []`,
`fact-cards.md` explains that no supported algorithm work item exists, and no
contribution fact may be created from absence. At career stage, the empty fact
set is confirmed and `resume-audit.json` must contain no unsupported algorithm
resume entry.

The controller does not parse or echo assistant questions. Repeating the complete
decision set closes any matching pending question while keeping behavior stable
across languages and model wording.

## 7. Turn Budget And Termination

- The green controller supports a maximum of 8 turns.
- It stops early after any turn that completes the workflow.
- It stops on process failure or a missing session identifier, preserving
  existing behavior.
- If the turn budget is exhausted before completion, the run remains a completed
  runtime session but records `max_turns_exhausted` as the controller stop reason.
- The baseline controller remains limited by its existing four-prompt legacy
  sequence even when the CLI accepts a larger global maximum.

The CLI default becomes 8 so external green runs exercise the adaptive retry
budget without additional flags.

## 8. Auditability

Each green turn records a controller-state snapshot containing:

- canonical artifacts detected in that turn
- cumulative canonical artifacts
- the stage selected after that turn

The run record includes:

- `controller_stop_reason`
- final `controller_stage`
- final cumulative `detected_artifacts`

These fields are diagnostic only. The grader remains unchanged and does not use
them.

## 9. Testing

TDD must cover:

1. Exact-heading recognition with LF/CRLF input and rejection of prose-only,
   fenced-code, and indented-code filename headings.
2. Strict-mode retries that remain on evidence until evidence artifacts appear.
3. Advancement to facts only after both evidence artifacts appear.
4. Advancement to career only after both facts artifacts appear.
5. Early stop after all workflow stage artifacts appear.
6. Out-of-order and partial artifact output.
7. Fast-mode all-at-once retries and early stop.
8. Original-request, language authority, fixture binding, decision closure, and
   hidden-grading-data protections on every generated continuation.
9. Algorithm claim-target closure without required/forbidden-claim leakage.
10. Maximum-turn exhaustion and controller audit fields.
11. Byte-for-byte preservation of baseline prompts and four-turn behavior.

Focused controller tests must pass before the full Skill/runner suite. The final
verification must also compile `tests` and `skills` and confirm the three Skill
copies retain the same SHA-256 digest.

## 10. External Acceptance

The next retained Codex campaign prefix is `final-9`. It uses Codex CLI 0.145.0,
model `gpt-5.6-sol`, read-only sandbox mode, five runs per scenario, and the
adaptive maximum of eight turns.

Packaging remains blocked unless all seven Codex scenarios pass 5/5, all runs
complete without runtime failures, every fixture remains clean, and the existing
grader gates pass. Claude testing requires separate authorization to send the
synthetic materials to Anthropic; current authorization covers OpenAI Codex
only.
