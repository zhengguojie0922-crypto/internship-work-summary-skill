# Forward-Test Controller Decision Closure Design

## Goal

Make the green forward-test controller carry a strict Skill session through all required stages without changing the Skill's source-only safety gates, exposing grading data, or allowing tested sessions to write into fixture repositories.

## Context

Codex final-7 completed 35/35 runs with zero runtime failures but passed only 1/35. The independent audit found five controller-level failure classes:

1. Strict sessions stopped after evidence because continuation prompts did not explicitly resolve separate collaborator-code, supporting-documentation, runtime-evidence, external-evidence, and output-location decisions.
2. English controller wrappers displaced the language and identity already present in the original user request.
3. The universal personal-attribution activation contradicted the algorithm scenario's non-personal assessment.
4. Later turns requested artifact names but did not close the decisions that the Skill must resolve before producing those artifacts.
5. Seven Codex sessions wrote 29 untracked files under read-only fixture repositories. The initial Codex command selected a read-only sandbox, but resumed commands did not restate a read-only configuration and Windows mode-bit changes did not enforce the policy.

The final-7 run records, manual reviews, grades, and audit remain immutable failure evidence.

## Constraints

- Keep `skills/analyzing-codebase-work-impact/SKILL.md` unchanged in this iteration.
- Keep all grader thresholds, artifact detection, scenario rubrics, required claims, forbidden claims, required questions, and citation rules unchanged.
- Keep baseline controller prompt strings byte-for-byte unchanged.
- Do not send rubric fields, expected claims, forbidden claims, expected citations, or fixture conclusions to tested sessions.
- Controller additions may state only synthetic-user scope choices, continuation decisions, output location, language authority, and runtime safety policy.
- Preserve final-2 through final-7 evidence; use a new run-id prefix for every new matrix.
- Treat fixture repositories as read-only on every engine turn.

## Approaches Considered

### Static Decision Closure In The Green Controller

Add explicit, category-by-category synthetic-user decisions to green continuations, mark the original request as the sole language and deliverable authority, make the algorithm non-personal scope visible on the first turn, and enforce Codex read-only configuration on resumed turns.

This is the selected approach. It is deterministic, small, testable without model calls, and does not inspect grading fields.

### Dynamic Question Parsing

Parse each assistant response, classify pending questions, and synthesize answers from a controller policy. This would handle more model wording variants but introduces a new parser and risks silently misclassifying genuine unresolved questions. It is unnecessary for the fixed seven-scenario acceptance controller.

### Relax The Skill Gates

Make collaborator and documentation decisions non-blocking or infer defaults inside the Skill. This would reduce controller friction but weaken real-user safeguards and address the symptom in the wrong component. It is rejected.

## Architecture

### Original Request Envelope

The green initial prompt must label the scenario's `user_prompt` as the original user request and the sole authority for requested language, target role, mode, and deliverables. Controller wrappers remain operational instructions and must explicitly say they are not language requests.

The initial prompt order is:

1. Skill activation.
2. Scenario scope context, when needed.
3. Original request authority rule and verbatim original user request.
4. Exact fixture binding and read-only/chat-only policy.
5. Canonical artifact protocol.

For `algorithm-attribution`, the scope context says this is a non-personal claim assessment and no Git identity is required. The generic sentence that personal attribution is required must not appear in this scenario.

For other scenarios, the controller must not invent identity in the initial prompt. Identity supplied in the original request remains authoritative; identities absent from it are supplied by the existing first continuation.

### Explicit Stage Decision Closure

The evidence-to-facts continuation must express synthetic-user decisions as independent statements:

- The evidence stage is confirmed.
- Include collaborator-authored code only as separately attributed context: yes.
- Include supporting documentation only as separately attributed context: yes.
- No separate runtime evidence is available.
- No additional external or untracked evidence is available unless the original request already supplies it.
- Use the target role, language, mode, and deliverables from the original request.
- Keep artifacts in chat and never write into the fixture repository.

Scenario-specific evidence confirmations may narrow these choices but must not contradict them. The controller still requests only `fact-cards.json` and `fact-cards.md` on that turn.

The facts-to-career continuation confirms facts, role, result, metric limitations, privacy, evidence links, emphasis, and exaggeration risk; repeats the chat-only and fixture read-only decisions; and requests only `career-package.md` and `resume-audit.json`.

Fast mode retains the existing rule to emit all four stages in one response. Follow-up prompts may confirm the already emitted draft but must not change the original request's language or role.

### Codex Read-Only Resume Profile

Every Codex command, fresh or resumed, must include a read-only sandbox policy. Fresh commands retain `--sandbox read-only`. Resumed commands add the equivalent supported config override `-c sandbox_mode="read-only"` because `codex exec resume` does not expose the `--sandbox` option.

Command construction tests must assert the read-only policy on both fresh and resumed commands. A forward-test audit must independently run `git status --short --untracked-files=all` for every fixture copy and reject a matrix that creates fixture-local files.

### Prompt Privacy Boundary

Green prompt construction may consume only:

- scenario ID for controller routing;
- scenario `user_prompt`;
- fixture repository path;
- public Skill activation and canonical artifact protocol;
- controller-owned synthetic-user confirmations.

It must never read or interpolate `required_artifacts`, `required_claims`, `forbidden_claims`, `required_questions`, `rubric`, or expected citations. Existing hidden-grading-data regression tests remain unchanged and must pass.

## Testing Strategy

### RED

Add focused tests proving current behavior is insufficient:

- algorithm initial prompt contains the personal-attribution conflict or lacks first-turn non-personal context;
- original request is not explicitly marked as sole language authority before operational wrappers;
- evidence continuation lacks independent yes/no decisions for collaborator code and documentation and lacks explicit no-runtime/no-external answers;
- facts continuation lacks privacy/evidence/emphasis/exaggeration confirmation;
- resumed Codex command lacks a read-only sandbox configuration.

Each test must fail for the named missing behavior before implementation.

### GREEN

Implement only the prompt constants/composition and command arguments required to pass the new tests. Re-run the unchanged hidden-grading-data and baseline prompt-preservation tests.

### REFACTOR And Regression

Run all forward-runner and Skill contract tests. Review generated prompts for all seven scenarios, verify baseline prompt bytes are unchanged, and verify no grading field appears in tested-session prompts.

## Forward Acceptance

Use a new run-id prefix and preserve final-7. For Codex, require:

- 35/35 completed runs;
- zero runtime failures;
- zero fixture writes;
- 35 manual reviews and 35 grades;
- every scenario 5/5 under the unchanged gates.

Run Claude only after explicit authorization to send the same synthetic materials to Anthropic. Packaging remains blocked until both runtime/model matrices pass every scenario 5/5.

If a new round fails, preserve it and repeat root-cause analysis. Do not weaken the grader, relax the Skill's evidence gates, or inject expected scenario answers.

## Files

- Modify `tests/forward_test_runner.py` for green prompt composition and Codex resume safety.
- Modify `tests/test_forward_test_runner.py` for RED/GREEN controller and command contracts.
- Create a new audit report only after a new forward matrix completes.
- Do not modify `skills/analyzing-codebase-work-impact/SKILL.md`, scenario files, fixture sources, grader logic, README, or packaging tests in this iteration.

## Acceptance

The controller change is implementation-complete when focused and full regression tests pass and an independent review finds no grading leakage or baseline prompt drift. The project is release-ready only after the separate dual-runtime forward acceptance gate succeeds.
