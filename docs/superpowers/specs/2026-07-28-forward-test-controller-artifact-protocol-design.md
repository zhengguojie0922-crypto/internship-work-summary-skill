# Forward-Test Controller Artifact Protocol Design

## Context

The `final-6` Claude matrix completed all 35 runs, but 34 runs failed the required-artifact gate after schema files stopped counting as generated artifacts. Most responses used human-readable headings such as `Evidence Report` or `Career Package` without exposing the canonical artifact names required by the Skill. The controller also relied on generic continuation language, so chat-only delivery did not have a deterministic artifact boundary.

This is a protocol mismatch between the Skill's stage table, chat-only output, the controller, and the grader. It is not evidence that schema files should count as output, and it must not be addressed by weakening filesystem artifact detection.

## Decision

Use one canonical artifact namespace for both file and chat output.

- File output must use the exact artifact filenames defined by the Skill.
- Chat-only output must use the same exact filenames as visible Markdown headings.
- A heading may contain the filename plus a language-appropriate description, but the filename itself must remain unchanged.
- The controller must request the current stage's canonical artifacts without supplying scenario rubric, required claims, forbidden claims, or expected conclusions.
- The grader must continue accepting an exact canonical artifact token in assistant text or an exact supported artifact basename on disk. It must not infer artifacts from semantic aliases and must not count schema files.

Canonical names remain:

```text
session.json
evidence-report.json
evidence-report.md
fact-cards.json
fact-cards.md
career-package.md
resume-audit.json
```

## Alternatives Considered

### Semantic heading aliases

Treat headings such as `Evidence Report` as equivalent to `evidence-report.md`. This is convenient for models but makes artifact detection language-dependent and cannot distinguish the JSON and Markdown variants. Rejected because it weakens the resumable artifact contract.

### Controller-side artifact synthesis

Have the controller transform free-form assistant text into missing artifacts after each turn. This would make the controller part of the product behavior and could conceal Skill failures. Rejected because tested outputs must come from the tested session.

### Canonical filename headings

Require exact filenames in both file and chat delivery. This preserves one contract across runtimes and makes missing artifacts observable. Selected.

## Controller Protocol

The green controller keeps the existing four-stage sequence and adds a generic delivery envelope:

1. The initial prompt states that chat-only artifacts must use the exact canonical filenames defined by the installed Skill as headings.
2. Each strict-mode continuation confirms only the preceding stage and requests the next stage's complete canonical artifacts.
3. The controller never names scenario-specific required artifacts from the scenario JSON. Stage artifact names come only from the public Skill contract.
4. The controller never supplies required claims, forbidden claims, rubric text, fixture conclusions, or citation answers.
5. Fast mode remains a single-response draft flow and must emit all four stages under their canonical artifact headings before any later continuation.
6. Clarification answers remain scenario-specific user statements. Documentation and collaborator-code answers stay independent and may not substitute for the assistant's required questions.

The baseline controller remains unchanged so historical RED behavior is preserved.

## Skill Contract

Add one delivery rule near the stage table:

- Emit every stage artifact under its exact canonical filename.
- In chat-only mode, use `## <canonical filename>` headings and include the full artifact body below each heading.
- Do not replace filenames with translated or friendly-only headings.
- For bilingual output, translate descriptions and content but keep filenames unchanged.

This is a format contract, not a new behavioral exception.

## Grader Contract

Keep exact artifact detection:

- Chat: detect the canonical artifact token in assistant text.
- Filesystem: accept only exact names in the supported artifact basename set and reject `*.schema.json`.
- Do not award an artifact based only on a semantically similar heading.

Citation validity, forbidden claims, semantic scores, and required questions remain independent hard gates. Passing the artifact gate must not compensate for another failure.

## Testing

Follow TDD:

1. Add contract tests proving the Skill requires canonical filename headings for chat-only output.
2. Add runner tests proving green prompts request canonical stage artifacts without containing scenario rubric or required/forbidden claims.
3. Add a fast-mode test proving one prompt requests all four stages under canonical headings.
4. Preserve the regression test that rejects Skill schema files as generated artifacts.
5. Run the focused tests, then all Skill/runner tests.
6. Synchronize the validated Skill into both runtime controllers and verify SHA-256 equality.
7. Run new `final-7` matrices for Claude Sonnet and Codex using the same seven scenarios and five runs per scenario.
8. Independently audit every run. Preserve `final-6` and all earlier failures unchanged.

## Acceptance

The controller redesign is accepted only when both tested runtime/model combinations meet the original design gates:

- 35/35 runs complete without runtime failure;
- every required artifact is present;
- no forbidden claim appears;
- citation validity is 100%;
- average semantic score is at least 90;
- every semantic item is at least 80;
- every scenario passes 5/5 runs.

If `final-7` still fails non-format semantic gates, stop and diagnose that evidence path separately. Do not weaken artifact detection or add controller hints containing expected answers.
