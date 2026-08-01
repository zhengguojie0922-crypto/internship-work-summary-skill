# Testing Role Guide

## Role Boundary and Subdomains

- Treat testing work as requirement risk analysis, test design, fixtures, automation, environment control, quality reporting, release gating, and defect diagnosis.
- Set the boundary from a stated behavior or defect through verification logic, execution conditions, results, and linked product changes.
- Include unit, integration, contract, API, UI, device, performance, and exploratory evidence only when the source identifies the test layer.
- Separate test authorship from product-code authorship, defect reporting, reviewing, release approval, and CI platform ownership.
- Distinguish a test suite's presence from demonstrated execution, failure detection, or a change in release outcome.
- Treat test data, mocks, fakes, and environment configuration as evidence-bearing dependencies rather than incidental setup.
- Attribute quality reporting only when the contributor changed the report, interpreted it, or linked it to a supported decision.
- Keep release gate configuration separate from evidence that a release was blocked, approved, or affected.
- Use production-issue reproduction as diagnosis evidence only when the failure conditions and result are traceable.
- Route material evidence gaps through the main consolidated confirmation process; this guide does not add confirmation rounds.

## Entry-Point Discovery

- Start from requirement identifiers, defect reports, acceptance criteria, or the changed product behavior under test.
- Locate test suites, test names, markers, tags, and selection commands that define the execution scope.
- Find fixture factories, builders, seeded data, cleanup hooks, and ownership of shared test resources.
- Inspect mocks, fakes, stubs, contract servers, and real dependency setup to identify each behavioral boundary.
- Read environment setup, container definitions, test configuration, feature flags, clocks, random seeds, and credentials handling.
- Locate CI jobs, matrix definitions, sharding, retry settings, artifact uploads, and the release gate that consumes results.
- Find coverage configuration, mutation testing reports, failure logs, quarantines, and flaky-test tracking records.
- Follow linked fixes from a defect or failing test to the product-code change and regression case.
- Record the test layer, environment, input data, oracle, and result before describing a quality contribution.
- Preserve missing execution records as a boundary rather than assuming a checked-in test ran in CI.

## Typical Code Chains

- Requirement-to-test: acceptance rule -> risk model -> selected test level -> fixture and input -> assertion -> CI result -> requirement trace evidence.
- Defect-to-regression: defect symptom -> minimal reproduction -> failing regression test -> product fix -> passing regression execution -> linked evidence boundary.
- Fixture setup: fixture factory -> isolated data creation -> dependency configuration -> test action -> assertion -> deterministic cleanup.
- API automation: test client -> authenticated request -> controlled service or contract boundary -> response assertion -> report artifact -> integration test boundary.
- UI automation: stable locator -> user action -> rendered state assertion -> controlled wait condition -> screenshot or log artifact -> UI test boundary.
- flaky-test diagnosis: intermittent failure -> collect timing, order, state, and environment evidence -> identify nondeterministic cause -> targeted fix -> repeated execution result.
- Flaky retry branch: transient infrastructure classification -> bounded retry with preserved failure artifact; product assertion failure -> fail without masking.
- Release gate: required suite selection -> environment matrix -> result aggregation -> pass or fail policy -> release decision record when available.
- Production reproduction: incident condition -> sanitized production-like data and configuration -> local or staged reproduction -> regression test -> linked fix evidence.
- Parallel execution: partitioned tests -> fixture isolation -> independent resources -> result merge; shared-state conflict -> fail or serialize rather than silently contaminate.
- These chains show verification paths and decision inputs, not proof that every defect was prevented or every release outcome changed.

## Technical Decision Matrix

| Decision | Evidence to inspect | Supported claim | Prohibited inference |
|---|---|---|---|
| risk model | Requirements, defect history, harm, likelihood, change surface, detectability, recovery, and prioritization records | Test effort targets the named risks using the evidenced ranking factors | The model is complete, prevents defects, or represents every stakeholder risk |
| test pyramid | Suite layout, selection commands, runtime records, dependency boundaries, and critical-journey coverage | The evidenced behaviors are placed at named unit, integration, contract, UI, or end-to-end layers | Pyramid shape proves optimal coverage, fast feedback, or production correctness |
| Boundary selection | Failure hypothesis, test layer, dependency setup, oracle, and linked product boundary | The selected layer can reveal the stated failure within its demonstrated boundary | One layer covers behavior owned by unexecuted dependencies or environments |
| fixture isolation | Factories, unique resource names, setup, cleanup, reordered runs, and parallel results | Test data and resources are isolated for the evidenced execution scope | Independent-looking fixtures prove order independence or safe parallelism everywhere |
| Real dependency versus double | Contract under test, fake or mock behavior, real-service setup, and comparison tests | The chosen dependency boundary controls or exercises the named behavior | A double reproduces all real behavior or a real dependency proves production parity |
| Deterministic time | Injected clocks, frozen time, timers, schedules, and repeated execution | Time-dependent branching is controlled for the tested cases | A frozen clock proves race freedom or correctness under real scheduling |
| Deterministic randomness | Seeds, generator injection, generated values, shrinking artifacts, and rerun commands | Random inputs are reproducible at the recorded seed and scope | One reproducible seed covers the input space or eliminates nondeterminism |
| Parallelism | Worker configuration, partitioning, ports, accounts, queues, cleanup, and concurrent run records | The suite executes independently under the evidenced worker and resource configuration | A passing parallel run proves unlimited concurrency or absence of shared-state leakage |
| Retry policy | Failure classification, retry bounds, preserved artifacts, quarantine records, and repeated outcomes | Only the named infrastructure failures receive bounded retry while product failures remain visible | A passing retry proves the flaky-test cause is fixed or the first failure was harmless |
| Release policy | Required suites, exceptions, quarantine rules, ownership, gate configuration, and decision records | The configured release gate applies the evidenced pass, fail, and exception rules | Gate configuration proves a release was blocked, approved, improved, or incident-free |

## Failure Modes and Risks

- False positives can block useful work when assertions, fixtures, or environment assumptions do not reflect the intended behavior.
- False negatives can pass while missing a relevant boundary, state transition, error condition, or observable user outcome.
- Shared-state leakage can make one test's data, cache, clock, or feature flag influence another test.
- Order dependency can produce a passing local run and failing reordered or parallel execution.
- flaky-test masking occurs when broad retries or quarantine hide nondeterminism without identifying the cause.
- Weak assertions can confirm that code ran without checking the specific contract, error, side effect, or state change at risk.
- Environment drift can change dependencies, permissions, configuration, or data shape between local, CI, staging, and production-like runs.
- Over-mocking can verify a test double's behavior while missing a broken real integration contract.
- Slow feedback can reduce diagnostic value when suite selection, setup, or artifacts obscure the first actionable failure.
- Unscoped coverage can create confidence claims without proving the chosen tests exercise the actual failure boundary.

## Validation Evidence

- Red-green regression evidence should show the targeted test failing for the intended defect or behavior before the supporting change, then passing afterward.
- mutation testing can show whether tests detect selected code changes, but its score needs mutation scope and surviving-mutant interpretation.
- Coverage can indicate executed lines or branches, not whether assertions adequately distinguish correct from incorrect behavior.
- Repeated execution evidence can expose intermittent behavior when the command, count, environment, and failure artifacts are retained.
- Parallel execution evidence can validate fixture isolation and concurrency assumptions only for the tested worker and resource configuration.
- CI matrix evidence should name operating systems, runtimes, browsers, devices, or dependency versions actually executed.
- Defect linkage should connect a report, reproduction, regression test, product fix, and result without assigning unsupported authorship.
- Test reports can prove a suite outcome for the recorded run, not universal quality or a production defect rate.
- Artifact evidence may include logs, screenshots, traces, coverage reports, mutation reports, and environment metadata.
- State the proof boundary as static test code, local execution, CI execution, controlled environment, or cited release record.

## Impact and Metrics Evidence

- Cite failure detection counts only from test reports or issue records that define the test scope and time window.
- Cite flaky rate only from a tracked denominator, classification method, and the execution population it describes.
- Cite duration only from measured suite, shard, environment, and comparison records rather than from an estimate.
- Cite escaped defects only from linked production or release records with a defined ownership and detection boundary.
- Cite reruns and quarantine counts only from CI records, preserving whether they represent infrastructure or product failures.
- Cite release gate outcomes only from decision records, and distinguish an available gate from a gate that actually blocked or approved a release.
- Relate a test change to a metric only when dates, version scope, and a defensible attribution path are recorded.
- Use qualitative statements about diagnosability or risk reduction when the code shows the strategy but no measured outcome exists.
- Do not infer complete coverage, zero defects, prevention, or release impact from test presence, a badge, or a passing run alone.
- Keep unsupported operational metrics out of resume wording and label them as needing user input.

## Resume Mapping

- Map a documented risk model to prioritizing verification around user harm, likelihood, and change surface.
- Map targeted regression evidence to reproducing a defect and adding a focused guard against that demonstrated behavior.
- Map fixture isolation to building deterministic test data, cleanup, or dependency control with the observed suite boundary.
- Map a flaky-test investigation to improved diagnosability only when the cause, change, and repeated result are traceable.
- Map API or UI automation to the behavior and environment actually verified rather than claiming total end-to-end coverage.
- Map release gate work to defining or maintaining a quality check without claiming a release was blocked or saved unless recorded.
- Map mutation testing or coverage to evidence analysis, including the limitations of the signal and surviving boundaries.
- Separate test, product-code, defect, review, CI, and release-decision authorship in each accomplishment statement.
- Prefer verbs such as designed, reproduced, automated, isolated, diagnosed, validated, or analyzed when supported by evidence.
- Attach a source note for every rate, count, prevention claim, or production-facing outcome before publishing it.

## Interview Question Tree

- Risk prioritization scenario: explain the risk model, affected users, failure severity, likelihood, detectability, and selected test depth.
- Pyramid scenario: explain why a behavior belongs in a unit, integration, contract, UI, or end-to-end layer and what each alternative would miss.
- Nondeterminism scenario: explain the flaky-test signal, time, randomness, order, environment, or shared-state hypothesis, and the confirming evidence.
- Fixture scenario: explain data creation, fixture isolation, cleanup, and how parallel execution changes the design.
- Dependency scenario: explain why a real dependency or double was selected and how the untested boundary remains visible.
- Regression scenario: explain the defect reproduction, red-green evidence, product fix linkage, and limitations on prevention claims.
- Environment scenario: explain local, CI, staging, and production-like parity, including configuration and data differences.
- Release scenario: explain required suites, policy, exceptions, artifacts, and the distinction between a release gate and a recorded release decision.
- Metrics scenario: name metric source, denominator, period, scope, attribution, and remaining uncertainty before stating impact.
- End every answer at the last supported node when production behavior, escaped defects, or release outcomes are not evidenced.

## Overclaim Guardrails

- Test presence does not prove defect prevention, complete coverage, zero defects, or release impact.
- A passing test does not prove production parity, all configurations, all user data, or absence of future regressions.
- A coverage number does not prove assertion quality, risk completeness, or behavior correctness beyond its measured scope.
- A mutation testing score does not prove all faults are detectable or that unmutated integration boundaries are protected.
- A quarantined or retried test does not prove the underlying flaky-test cause is fixed.
- A release gate configuration does not prove any specific release was blocked, approved, or improved.
- Separate test author, product-code author, defect reporter, reviewer, CI operator, and release decision-maker in every evidence chain.
- Preserve unknown environments, missing defect links, unmeasured rates, and unsupported outcomes as explicit limitations.
- Never convert a test refactor, added suite, or green CI run into a prevention or business-impact claim without cited records.
- Route material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
