# Single-Document Career Workflow Design

## Goal

Turn the Skill into a direct internship-output and interview-preparation workflow. A normal run creates no intermediate artifacts and writes exactly one final Markdown document to `career-output/实习产出与面试准备.md`.

## Trigger Surface

Implicitly invoke the Skill when a user mentions internship output, internship summary, project experience, resume packaging or optimization, putting a feature on a resume, work achievements, or interview preparation. Include the common Chinese phrases directly in frontmatter so Chinese requests activate reliably.

## Request Routing

Route every request into one of two paths:

1. **Named feature:** Start from the user's feature description and trace the implementation regardless of commit authorship. Inspect entry points, UI or API boundaries, business logic, data flow, persistence, configuration, dependencies, error handling, and tests.
2. **Git discovery:** When no feature is named, identify the user's commits, cluster them into business or engineering outcomes, and trace the implementation behind each material cluster.

The named-feature path never requires a Git identity. For Git discovery, inferred identity or role values may shorten the user's reply, but they do not replace confirmation when the request did not explicitly supply both values.

## Confirmation Contract

Use at most two confirmation rounds across the complete run.

- Infer repository, feature, Git identity, target role, time range, and language from supplied context before asking. Use inferred Git identity and target role as concise proposed values, not as substitutes for confirmation in Git discovery.
- For Git discovery, when the request does not explicitly provide both Git identity and target role, confirm both in the first consolidated question before analyzing commits. Time range is optional and defaults to all reachable history.
- Reserve a second round only for a material ambiguity or for business context that would substantially improve resume claims.
- Continue with explicit unknown markers when the user does not answer. An unambiguous inferred Git identity or target role may be used after the second round only when marked as user-unconfirmed. Do not introduce staged approval gates.

## Evidence Collection

Treat the target repository as read-only. Use `rg` and read-only Git queries. Do not run repository code, builds, tests, hooks, package managers, or generated commands. Keep search notes, candidate lists, and evidence relationships in conversation memory only.

For named features, Git history is chronology rather than an authorship filter. For Git discovery, Git identity scopes candidate commits, but adjacent collaborator code may be inspected to explain the chain without claiming it as the user's work.

## Final Document

Write one final file at `career-output/实习产出与面试准备.md`. Create the parent directory when necessary. The document contains:

1. Internship output overview
2. Business function and user value
3. Complete code path
4. Personal work, technical decisions, and difficulties
5. Resume wording in concise, standard, and strengthened variants
6. Interview introductions for 30 seconds, 1 minute, and 3 minutes
7. About 20 core interview questions per major output, each with a reference answer
8. Likely follow-ups and answer direction for each core area
9. Scenario questions and response frameworks
10. Quantifiable indicators and information that still needs user input
11. Evidence index containing relevant files and commits

When many Git clusters exist, prioritize the strongest three to five outputs so the final document remains usable. Preserve a short appendix for lower-value verified work.

## Truthfulness And Privacy

Separate source-visible facts, Git attribution, user-provided context, and interpretation. Never invent metrics, scale, production status, business impact, ownership, causality, or runtime behavior. Mark unsupported but useful resume inputs as `需要用户补充`. Redact secrets, personal data, internal URLs, customer identifiers, and unnecessary repository details.

## Repository Simplification

Remove the old staged-artifact contract, JSON schemas, minimal JSON examples, artifact validator, fixture controller, forward-test runner, and tests dedicated to those obsolete surfaces. Retain the deterministic Git evidence collector and its focused tests. Rewrite the Skill contract and packaging tests around the installable core, single output, README, license, links, and CI configuration.

## Verification

Use TDD for the new contract:

1. Run the new contract tests against the old Skill and observe failure.
2. Rewrite the Skill and supporting references.
3. Update metadata and README.
4. Remove obsolete runtime/test assets.
5. Run focused contract, packaging, and Git collector tests.
6. Run the complete remaining deterministic test suite and `git diff --check`.
