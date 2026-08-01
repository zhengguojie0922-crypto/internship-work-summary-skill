---
name: summarizing-internship-work
description: Use when a user asks for 实习产出, 实习总结, 项目经历, 简历包装, 简历优化, 写到简历, 工作成果, 面试准备, internship output, internship summary, project experience, resume writing, resume optimization, CV writing, work achievements, or interview preparation from a local codebase, Git history, commit range, or named feature.
---

# Internship Work Summary

Turn read-only repository evidence into one evidence-backed internship, resume, and interview document. Keep observations, user statements, and unknowns distinct; do not turn inference into fact.

## Route the Request

- When the request names a specific feature, trace the feature regardless of commit authorship. A request to trace the feature is a named-feature route.
- When there is no specific feature, use Git history to discover the user's contributions: identify the Git identity, inspect relevant history, cluster commits into business or engineering outcomes, and trace each major cluster.
- If both are supplied, trace the named feature first and use Git history only to enrich attributable change evidence.

## Resolve Inputs

Always infer supplied values before asking, including repository, feature, commit range, language, and target role. Target role is required. Inference may provide a proposed value, but it does not replace the Git-discovery confirmation required below.

Ask one consolidated question for all material missing values. It may request Git identity only for Git discovery, target role when it cannot be inferred, scope, language, and any required privacy boundary. Perform at most two confirmation rounds. After the second round, continue with explicit unknowns instead of blocking on optional details.

## Trace a Named Feature

Do not ask for a Git identity. Trace the entry point, UI/API boundary, business logic, data flow, persistence, dependencies, configuration, error handling, and tests. Follow imports, calls, routes, schemas, events, and test coverage in both directions until evidence ends. Record what each link proves and label missing links or runtime behavior as unknown.

## Discover Contributions From Git History

When the request does not explicitly supply both values, use the first consolidated question to confirm both the Git identity and target role before analyzing commits, even when candidate values can be inferred from the repository. Present inferred candidates in that question so the user can answer briefly. If either value remains unanswered after the second and final confirmation round, continue with the best candidate only when evidence is unambiguous, label it as user-unconfirmed, and state the resulting scope limitation.

Filter candidate commits to the resolved Git identity before clustering; only matching commits become personal candidate work. Read collaborator commits only as separately attributed context. Inspect the relevant Git history read-only, group related commits into business or engineering outcomes, then trace each major cluster through its entry point, boundary, logic, data flow, persistence, dependencies, configuration, error handling, and tests. Separate authored change evidence from collaboration context and never treat authorship as proof of sole ownership or impact.

## Evidence and Safety Rules

- Keep repository inspection read-only; use searches and Git inspection only.
- Never execute target-repository code, install dependencies, change branches, fetch, or modify the target repository.
- Link every claim to source, Git, test, or user-provided evidence; label unsupported statements as unknown or needs user input.
- Never invent metrics, users, scale, runtime behavior, outcomes, causality, ownership, or business value.
- Always redact secrets, credentials, personal data, private URLs, customer identifiers, and proprietary values from the final document.

## Confidence Levels

- high = direct source/Git/test evidence for the exact claim.
- medium = multiple consistent static observations with an explicit runtime/outcome boundary.
- low = tentative interpretation that stays out of resume wording and is marked needs user input.

## Supporting Analysis References

Use [analysis defaults](references/analysis-defaults.md) for read-only commands, skip rules, limits, and degradation behavior. Use [achievement analysis](references/achievement-analysis.md) to turn the supported evidence into major outputs. Use [role classification](references/role-classification.md) to select the applicable role guide:

| Role | Guide |
|---|---|
| Frontend | [frontend guide](references/role-frontend.md) |
| Backend | [backend guide](references/role-backend.md) |
| Client | [client guide](references/role-client.md) |
| Testing | [testing guide](references/role-testing.md) |
| DevOps | [DevOps guide](references/role-devops.md) |
| Data analytics | [data analytics guide](references/role-data-analytics.md) |
| Algorithm | [algorithm guide](references/role-algorithm.md) |

## Build the Final Document

Keep working notes in memory. The only runtime file is `<current writable workspace>/career-output/实习产出与面试准备.md`; create its parent directory only when necessary. This final document is the only file artifact and the only explicit allowed workspace write, including when the writable workspace is also the analyzed repository. Repository source and Git state remain read-only. Do not create intermediate files or directories.

Prioritize the strongest 3-5 major outputs by direct evidence, technical depth, and target-role relevance. Put lower-value verified work in a concise appendix rather than expanding it as a major output.

Write the document in this order for each major output:

1. `Internship Output Overview`: scope, role, attribution boundary, and evidence confidence.
2. `Business Function and User Value`: only evidence-backed function and value; list unverified value as needs user input.
3. `Code Path`: entry point, boundary, logic, data flow, persistence, dependencies, configuration, error handling, tests, and evidence locations.
4. `Personal Work`: attributable actions, collaboration boundary, decisions, technical difficulties, validation, and explicit unknowns.
5. `Resume Wording`: three role-appropriate variants from [resume writing](references/resume-writing.md).
6. `Interview Introduction`: `30-second`, `1-minute`, and `3-minute` versions from [interview expansion](references/interview-expansion.md).
7. `Interview Questions`: about 20 core interview questions per major output, each with a reference answer, likely follow-ups, follow-up answer direction, scenario questions, and a scenario response framework.
8. `Metrics Needs User Input`: metrics that would strengthen the claim, why they matter, and the owner or system that could verify them.
9. `Evidence Index`: evidence locations, commit identifiers when used, confidence, attribution, and redactions.

Use the resume and interview references to expand these sections. Keep every factual claim evidence-backed and every stronger unsupported claim in the explicit unknowns or metrics section.
