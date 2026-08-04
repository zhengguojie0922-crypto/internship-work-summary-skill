# Role Analysis Framework

Use this framework after target-role classification and before the selected role guide. It converts repository evidence into role-specific technical analysis and career material without replacing the evidence and safety rules in `SKILL.md`.

## Evidence Chain

Build a bounded chain through entry point, user or system boundary, core logic, data flow, state or persistence, dependencies, configuration, error handling, and validation evidence. For every link record the definition, caller or consumer, relationship proved by source, and last supported node. A filename or search hit starts investigation but does not prove behavior.

## Evidence Matrix

Before drafting career material, build one in-memory evidence matrix for each major output. Keep it in working context rather than writing a research artifact. Each matrix records:

- the business goal, user or system value, and bounded feature scope;
- entry points, externally visible contracts, files, symbols, callers, and callees;
- the end-to-end code path, data flow, state transitions, persistence, and dependencies;
- business rules, important branches, lifecycle behavior, and configuration;
- failure paths, edge cases, recovery or degradation, and security boundaries;
- tests, logs, observability, configuration checks, and other validation evidence;
- applicable Git attribution, user-provided attribution, and collaboration boundaries;
- observable design choices, evidence-supported alternatives, trade-offs, and evidence gaps.

Do not move to question drafting until the matrix follows the implementation beyond search hits and filenames. Each project-specific question must map to at least one concrete evidence anchor: a file and symbol, a proved call-path segment, a branch, a test, a configuration item, or an applicable commit. Record where the chain stops so later answers can distinguish facts from interpretation and missing runtime evidence.

## Feature Model

Turn the evidence matrix into one shared feature model before writing resume material or interview questions. This model supplies the common technical context that later answers reuse instead of compressing the same explanation into one-line fields. Include, when supported:

- a glossary and the system or user boundary;
- a causal problem narrative showing how the original failure occurs;
- an architecture and call-path map from entry point through state, data, dependencies, and validation;
- the relevant state, data, protocol, or lifecycle model and its invariants;
- happy, failure, recovery, and degradation paths;
- a code and test responsibility map that explains each file or symbol's role and relationships;
- observable constraints, alternatives, trade-offs, ownership boundaries, and evidence gaps.

A path or line range alone is not analysis. For each important anchor, record what the symbol does, who calls it, what it calls, which state or data crosses the boundary, how failures propagate, and what test, configuration, or adjacent code verifies the relationship. Stop at the last supported node rather than completing a familiar framework pattern from assumption.

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

Plan the question set from the completed feature model, not from isolated search hits. Distribute questions across the dimensions the repository actually supports: business context and scope; entry point and end-to-end call path; data, state, persistence, and lifecycle; algorithms and business rules; interfaces and module boundaries; failure handling, idempotency, concurrency, and security; performance and observability; testing and defect diagnosis; architecture and evolution; personal contribution and reflection; target-role depth; and scenario reasoning under changed constraints.

Each question must cite the relevant chain, state the attribution boundary, and separate observed behavior from production assumptions. Use the natural answer recipe in `interview-expansion.md`: give a coherent main answer and show and answer each follow-up separately with complete follow-up answers. If two candidates use substantially the same evidence anchors, central conclusion, and answer path, merge duplicate questions and replace them only with a distinct evidence-backed angle. Omit an unsupported dimension instead of filling it with a generic textbook question.

Run a final quality audit before the final document write: verify the shared feature model, distinct coverage, concrete relationships among anchors, coherent main answers, independently answered follow-ups, attribution consistency, and explicit evidence boundaries. Repair failed items in memory by returning to the evidence matrix, feature model, or question plan.

## Cross-Role Boundary

Load exactly one primary role guide. Load at most one secondary role guide only when direct cross-role evidence is necessary to explain a dependency, interface, or collaboration boundary. The target role remains the organizing perspective. Consuming another layer does not prove ownership of that layer.

## Degradation Rules

When a chain breaks, stop at the last supported node and record the missing relationship, confidence impact, and possible verification source. When decision authorship is unavailable, describe implementation or participation rather than leadership. When runtime metrics are absent, report capability and validation evidence without claiming production impact.
