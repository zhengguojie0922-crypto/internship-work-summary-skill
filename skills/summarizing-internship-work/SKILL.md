---
name: summarizing-internship-work
description: Use when a user asks for 实习产出, 实习总结, 项目经历, 简历包装, 简历优化, 写到简历, 工作成果, 面试准备, internship output, internship summary, project experience, resume writing, resume optimization, CV writing, work achievements, or interview preparation from a local codebase, Git history, commit range, or named feature.
---

# Internship Work Summary

Turn read-only repository evidence into one evidence-backed internship, resume, and interview document. Keep observations, user statements, and unknowns distinct; do not turn inference into fact.

## Route the Request

- When the request names a specific feature, trace the feature regardless of commit authorship. A request to trace the feature is a named-feature route.
- When there is no specific feature, use Git history to discover the user's contributions: identify the Git identity, inspect relevant history, cluster commits into business or engineering outcomes, and trace each major cluster.
- If a named feature is supplied with an explicit request for Git verification, trace the feature first and then use Git history to verify attribution. A personal-output request by itself does not require Git verification.

## Resolve Inputs

Always infer supplied values before asking, including repository, feature, commit range, language, and target role. Target role is required. Inference may provide a proposed value, but it does not replace the Git-discovery confirmation required below.

Ask one consolidated question for all material missing values. It may request Git identity only for Git discovery, target role when it cannot be inferred, scope, language, and any required privacy boundary. Perform at most two confirmation rounds. After the second round, continue with explicit unknowns instead of blocking on optional details.

## Trace a Named Feature

Do not ask for a Git identity. When the user names a feature for a personal resume, internship summary, or personal output, treat that feature as fully implemented by the user and record the attribution as user-provided evidence. Do not check commit authorship unless the user explicitly requests Git verification. Use repository evidence to reconstruct implementation, decisions, validation, and effect boundaries; it does not override the supplied personal attribution.

If the user only asks how the feature works, trace the implementation but do not infer personal ownership.

Trace the entry point, UI/API boundary, business logic, data flow, persistence, dependencies, configuration, error handling, and tests. Follow imports, calls, routes, schemas, events, and test coverage in both directions until evidence ends. Record what each link proves and label missing links or runtime behavior as unknown.

## Discover Contributions From Git History

When the request does not explicitly supply both values, use the first consolidated question to confirm both the Git identity and target role before analyzing commits, even when candidate values can be inferred from the repository. Present inferred candidates in that question so the user can answer briefly. If either value remains unanswered after the second and final confirmation round, continue with the best candidate only when evidence is unambiguous, label it as user-unconfirmed, and state the resulting scope limitation.

Use the bundled [Git evidence collector](scripts/collect_git_evidence.py) for identity discovery and commit selection. Always pass `--output -` and consume stdout in memory; never use a file output path or create intermediate JSON.

1. Before asking for identity confirmation, run `python <skill-directory>/scripts/collect_git_evidence.py contributors --repo <repository> --max-commits 500 --output -`. Add `--since` and `--until` when the request supplies a date range.
2. Present observed full names and emails in the consolidated confirmation question. Treat `aliases` as candidates, not proof that identities belong to one person. Resolve same-name ambiguity with a full email, confirm each applicable alias, and include `Co-authored-by` identities.
3. After confirmation, run `python <skill-directory>/scripts/collect_git_evidence.py collect --repo <repository> --author "<confirmed full name or email>" --max-commits 500 --sensitivity internal --output -`. Use a repeated --author argument for every confirmed alias. Add confirmed date and path filters. Use `--sensitivity public` instead of `--sensitivity internal` when the requested document is intended for public sharing.

Exit code 2 means invalid arguments or scope, exit code 3 means the repository or Git is unavailable, exit code 4 means a Git query failed, and exit code 5 means evidence could not be read or written. Report the applicable boundary and continue only when the remaining evidence is sufficient. When the report contains `commit_limit_reached`, narrow the date/path scope during the allowed confirmation rounds or explicitly retain the bounded result; raise `--max-commits` only when the larger scan is necessary.

Filter candidate commits to the resolved Git identity before clustering; exact full-name or full-email matches as primary author or `Co-authored-by` author become personal candidate work. Read collaborator commits only as separately attributed context. Inspect the relevant Git history read-only, group related commits into business or engineering outcomes, then trace each major cluster through its entry point, boundary, logic, data flow, persistence, dependencies, configuration, error handling, and tests. Separate authored change evidence from collaboration context and never treat authorship as proof of sole ownership or impact.

## Evidence and Safety Rules

- Keep repository inspection read-only; use searches and Git inspection only.
- Never execute target-repository code, install dependencies, change branches, fetch, or modify the target repository.
- Link every claim to source, Git, test, or user-provided evidence; label unsupported statements as unknown or needs user input.
- User-provided attribution supports ownership only for the named feature scope; it does not verify adjacent work, runtime behavior, metrics, or outcomes.
- Never invent metrics, users, scale, runtime behavior, outcomes, causality, ownership, or business value.
- Always redact secrets, credentials, personal data, private URLs, customer identifiers, and proprietary values from the final document.

## Confidence Levels

- high = direct source/Git/test evidence for the exact claim.
- medium = multiple consistent static observations with an explicit runtime/outcome boundary.
- low = tentative interpretation that stays out of resume wording and is marked needs user input.

## Supporting Analysis References

Use [analysis defaults](references/analysis-defaults.md) for read-only commands, skip rules, limits, and degradation behavior. Use [achievement analysis](references/achievement-analysis.md) to turn the supported evidence into major outputs. Use [role classification](references/role-classification.md) to select exactly one primary role guide. After classification, always use the [role analysis framework](references/role-analysis-framework.md) and the one primary role guide. Load at most one secondary role guide only when direct cross-role evidence is required to explain a dependency, interface, or collaboration boundary; keep the target role as the organizing perspective. Role-guide ownership guardrails must accept that user-provided attribution for a named-feature personal-output route, while still rejecting unsupported ownership of adjacent components, team outcomes, or business impact.

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

If the final document already exists, update matching outputs and preserve unrelated verified material. Replace the entire document only when the user explicitly requests a rebuild.

Prioritize the strongest 3 major outputs by default using direct evidence, technical depth, and target-role relevance. Expand to up to 5 only when the user explicitly requests a comprehensive summary. Put lower-value verified work in a concise appendix rather than expanding it as a major output.

Before drafting career material, build an in-memory evidence matrix for each major output using the role analysis framework. Trace business scope, entry points, files and symbols, callers and callees, end-to-end code path, data and state, business rules, failures, configuration, tests, applicable Git evidence, design choices, alternatives, and evidence gaps. Use the matrix to plan distinct questions. Every project-specific question must cite at least one concrete evidence anchor. If candidate questions share substantially the same anchors, central conclusion, and answer path, merge duplicate questions and find a different evidence-backed angle.

Write the document in this order for each major output:

1. `Internship Output Overview`: scope, role, attribution boundary, and evidence confidence.
2. `Business Function and User Value`: only evidence-backed function and value; list unverified value as needs user input.
3. `Code Path`: entry point, boundary, logic, data flow, persistence, dependencies, configuration, error handling, tests, and evidence locations.
4. `Personal Work`: attributable actions, collaboration boundary, decisions, technical difficulties, validation, and explicit unknowns.
5. `Resume Wording`: three role-appropriate variants from [resume writing](references/resume-writing.md).
6. `Interview Introduction`: `30-second`, `1-minute`, and `3-minute` versions from [interview expansion](references/interview-expansion.md).
7. `Interview Questions`: about 20 core interview questions per major output. Every question must be a complete unit containing a `Detailed question`, `Interview intent`, `Code evidence`, `Reasoning process`, `Detailed first-person answer`, `Design trade-offs`, `Failure and validation analysis`, `2-4 deep follow-up questions`, `Complete follow-up answers` for every follow-up, and an `Evidence boundary`. Then add a separate set of 3-5 scenario questions; each scenario states its changed premise, affected code path, diagnosis or decision process, concrete response, trade-offs, validation, and evidence-derived follow-ups with complete answers. Produce fewer than 20 core questions when evidence is insufficient; never pad or fabricate to meet a quota.
8. `Metrics Needs User Input`: metrics that would strengthen the claim, why they matter, and the owner or system that could verify them.
9. `Evidence Index`: evidence locations, commit identifiers when used, confidence, attribution, and redactions.

Use the resume and interview references to expand these sections. Keep every factual claim evidence-backed and every stronger unsupported claim in the explicit unknowns or metrics section. Before the single final write, run a final quality audit in memory: confirm that every core question has all ten elements, every follow-up has a complete answer, evidence anchors are explained rather than merely listed, questions cover distinct technical dimensions, attribution is consistent across resume and interview material, and scenarios distinguish current implementation from proposed action. Return to the evidence matrix and repair any failed item before writing the document.
