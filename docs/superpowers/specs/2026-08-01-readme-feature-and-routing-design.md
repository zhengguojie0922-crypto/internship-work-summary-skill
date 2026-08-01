# README Feature And Routing Design

## Goal

Make the Chinese README explain the Skill's complete user-facing capability, distinguish its seven supported target roles, and make route selection understandable without reading `SKILL.md`.

## Scope

Change only README documentation and its publishing-contract tests. Do not change Skill behavior, metadata, version, installation commands, output path, safety rules, or model-validation claims.

## Information Architecture

Keep `快速安装` near the top. Add `详细功能` after installation and before routing so a new user first learns how to install, then what the Skill can produce, then how their request is routed.

The detailed feature section contains:

1. Named-feature code-path tracing.
2. Git-identity-scoped internship-output discovery.
3. Evidence and attribution boundaries.
4. Resume wording and interview preparation.
5. Single-document output without intermediate artifacts.
6. Read-only inspection, truthfulness, and redaction.

Add a seven-role table with one row each for frontend, backend, client, testing, DevOps, data analytics, and algorithm work. Each row states the evidence focus and the career-output emphasis. Keep the role descriptions concrete and avoid claiming runtime capabilities not present in the Skill.

## Trigger And Routing

Rewrite `触发与路由` in this order:

1. Explain implicit and explicit invocation and give representative Chinese trigger phrases.
2. Present a decision table with request signal, selected route, Git-identity behavior, and analysis focus.
3. Cover three cases: named feature, Git discovery, and a mixed request containing both a named feature and Git scope.
4. State the confirmation contract after the decision table: one consolidated question, at most two rounds, named-feature routing never asks for Git identity, and Git discovery confirms Git identity plus target role when either was not explicitly supplied.
5. Give short example requests for both primary routes.

## Testing

Extend `tests/test_packaging.py` before editing README. The new contract verifies:

- `详细功能` exists before `触发与路由`.
- The six common capability areas are documented.
- All seven roles have distinct evidence and output guidance.
- All three route cases and their Git-identity rules are explicit.
- Existing installation, single-output, safety, verification, and privacy documentation remains intact.

Run the focused packaging test first to observe RED, then update README to GREEN. Finish with the complete unit suite, compile check, and `git diff --check`.

## Non-Goals

- No Skill runtime changes.
- No new scripts or dependencies.
- No model forward-test rerun.
- No version bump.
