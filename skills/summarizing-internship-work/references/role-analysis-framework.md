# Role Analysis Framework

Use this framework after target-role classification and before the selected role guide. It converts repository evidence into role-specific technical analysis and career material without replacing the evidence and safety rules in `SKILL.md`.

## Evidence Chain

Build a bounded chain through entry point, user or system boundary, core logic, data flow, state or persistence, dependencies, configuration, error handling, and validation evidence. For every link record the definition, caller or consumer, relationship proved by source, and last supported node. A filename or search hit starts investigation but does not prove behavior.

## Decision Reconstruction

For every material implementation identify the observable constraint, actual choice, available alternative only when repository or user evidence supports it, trade-off, failure mode, and validation evidence. Separate a choice visible in code from a decision attributable to the user. Do not invent rejected alternatives or design intent.

## Technical Depth

Classify depth only from direct evidence:

| Level | Required evidence |
|---|---|
| Basic implementation | A bounded behavior change with a traceable entry, logic, and validation path |
| Independent ownership | Attributable work across multiple connected layers with explicit boundary handling |
| Complex problem solving | Evidence of constraints, edge cases, failure analysis, trade-offs, and targeted validation |
| System-level improvement | Evidence spanning shared contracts or operational boundaries with verified system effects |

Use the highest fully supported level. Repository size, line count, framework popularity, or confident prose does not raise the level.

## Evidence Classification

Classify each claim as source fact, Git attribution, test evidence, user-provided evidence, static inference, or unknown. High confidence requires direct evidence for the exact claim. Medium confidence requires multiple consistent static observations and an explicit runtime or outcome boundary. Low confidence stays out of resume wording and is marked needs user input.

## Career Material Mapping

Map each supported output through this sequence:

```text
problem or constraint -> attributable action -> technical mechanism -> validation -> bounded effect
```

Use a conservative resume version for implementation evidence, a standard version when ownership and validation are supported, and an impact version only when verified system or business evidence exists. Convert unresolved metrics into `Metrics Needs User Input` rather than placeholders inside resume bullets.

## Interview Question Tree

Generate questions from actual evidence in six branches: foundation, implementation detail, design alternative and trade-off, failure diagnosis, scale or extension, and scenario response. Each answer must cite the relevant chain, state the attribution boundary, and separate observed behavior from production assumptions. Omit a branch when the repository provides no relevant evidence instead of fabricating a scenario.

## Cross-Role Boundary

Load exactly one primary role guide. Load at most one secondary role guide only when direct cross-role evidence is necessary to explain a dependency, interface, or collaboration boundary. The target role remains the organizing perspective. Consuming another layer does not prove ownership of that layer.

## Degradation Rules

When a chain breaks, stop at the last supported node and record the missing relationship, confidence impact, and possible verification source. When decision authorship is unavailable, describe implementation or participation rather than leadership. When runtime metrics are absent, report capability and validation evidence without claiming production impact.
