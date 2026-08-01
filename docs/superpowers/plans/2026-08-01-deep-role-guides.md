# Deep Role Guides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the seven shallow role checklists with a shared evidence-to-career analysis framework and detailed, role-specific code-tracing, resume, and interview guidance.

**Architecture:** Keep `SKILL.md` as the compact router. After classifying the target role, load one shared `role-analysis-framework.md`, exactly one primary role guide, and at most one secondary guide when direct cross-role evidence requires it. Each role guide uses the same ten-section contract but contains distinct technical chains, decisions, failure modes, validation evidence, metrics, resume rules, and interview prompts.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3.10+ standard-library `unittest`, Git 2.30+

## Global Constraints

- Skill identifier remains `summarizing-internship-work`.
- Version remains `1.0.0`; this change does not create a new release tag.
- The named-feature route never asks for Git identity.
- The Git-discovery route confirms both Git identity and target role before commit analysis when either is not explicitly supplied.
- The complete workflow performs at most two confirmation rounds.
- Target-repository analysis remains read-only and never runs target code, installs dependencies, changes branches, fetches, or modifies Git state.
- The only runtime artifact remains `career-output/实习产出与面试准备.md`.
- Do not create runtime JSON, evidence, audit, session, cache, or other intermediate files or directories.
- Never invent metrics, business outcomes, ownership, causality, runtime behavior, scale, or production impact.
- Support exactly seven primary guides: frontend, backend, client, testing, DevOps, data analytics, and algorithm.
- Load one primary role guide and no more than one secondary role guide.
- Each role guide uses the exact ten-section heading contract defined below and contains role-specific rather than title-substituted content.
- Each role guide contains 120 to 180 lines of executable guidance and compact matrices rather than general technical exposition.
- Add no external dependency and do not change `collect_git_evidence.py` or its CLI.
- Use deterministic contract tests only; do not add model forward tests.

---

### Task 1: Add the shared role-analysis framework and routing contract

**Files:**
- Create: `skills/summarizing-internship-work/references/role-analysis-framework.md`
- Modify: `skills/summarizing-internship-work/SKILL.md`
- Modify: `skills/summarizing-internship-work/references/role-classification.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: the existing target-role classification and two-route workflow.
- Produces: a shared analysis reference with label `role analysis framework` and target `references/role-analysis-framework.md`, plus a loading rule of one primary and at most one secondary guide.

- [ ] **Step 1: Write failing routing and framework tests**

Add this path beside the existing path constants:

```python
ROLE_FRAMEWORK_PATH = SKILL_DIR / "references" / "role-analysis-framework.md"
```

Add this link to `REQUIRED_REFERENCE_LINKS` immediately after role classification:

```python
"[role analysis framework]" "(references/role-analysis-framework.md)",
```

Change the existing role-guide glob filter so the new framework is not counted as an eighth role:

```python
if path.name not in {"role-analysis-framework.md", "role-classification.md"}
```

Add these tests to `SkillContractTests`:

```python
def test_skill_loads_shared_role_framework_and_bounds_cross_role_context(self) -> None:
    section = self._section("Supporting Analysis References")
    for phrase in (
        "role analysis framework",
        "one primary role guide",
        "at most one secondary role guide",
        "direct cross-role evidence",
    ):
        self.assertIn(phrase, section)

def test_role_analysis_framework_maps_evidence_to_career_material(self) -> None:
    text = ROLE_FRAMEWORK_PATH.read_text(encoding="utf-8")
    for heading in (
        "## Evidence Chain",
        "## Decision Reconstruction",
        "## Technical Depth",
        "## Evidence Classification",
        "## Career Material Mapping",
        "## Interview Question Tree",
        "## Cross-Role Boundary",
        "## Degradation Rules",
    ):
        self.assertIn(heading, text)
    lowered = text.lower()
    for phrase in (
        "entry point",
        "alternative",
        "failure mode",
        "validation evidence",
        "basic implementation",
        "system-level improvement",
        "resume",
        "scenario",
        "one secondary role guide",
        "last supported node",
    ):
        self.assertIn(phrase, lowered)

def test_role_classification_selects_one_primary_and_at_most_one_secondary(self) -> None:
    text = (SKILL_DIR / "references" / "role-classification.md").read_text(
        encoding="utf-8"
    )
    self.assertIn("exactly one primary role guide", text)
    self.assertIn("at most one secondary role guide", text)
    self.assertIn("direct cross-role evidence", text)
    self.assertIn("target role remains the organizing perspective", text)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```text
python -m unittest tests.test_skill_contract.SkillContractTests.test_skill_loads_shared_role_framework_and_bounds_cross_role_context tests.test_skill_contract.SkillContractTests.test_role_analysis_framework_maps_evidence_to_career_material tests.test_skill_contract.SkillContractTests.test_role_classification_selects_one_primary_and_at_most_one_secondary -v
```

Expected: FAIL because the shared framework file and new loading phrases do not exist.

- [ ] **Step 3: Create the shared role-analysis framework**

Create `role-analysis-framework.md` with these exact sections and rules:

```markdown
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
```

- [ ] **Step 4: Update `SKILL.md` loading instructions**

In `## Supporting Analysis References`, replace the role-classification sentence with the paragraph below, followed by the existing role table. The backslashes before link parentheses exist only to keep this plan's public-link validator from resolving future SKILL-relative links against `docs/superpowers/plans`; omit those backslashes in `SKILL.md`.

```markdown
Use [role classification]\(references/role-classification.md) to select exactly one primary role guide. After classification, always use the [role analysis framework]\(references/role-analysis-framework.md) and the one primary role guide. Load at most one secondary role guide only when direct cross-role evidence is required to explain a dependency, interface, or collaboration boundary; keep the target role as the organizing perspective.
```

- [ ] **Step 5: Tighten role classification**

Replace the opening paragraph of `role-classification.md` with:

```markdown
Classify work from the dominant direct evidence chain and the confirmed target role. Select exactly one primary role guide. Select at most one secondary role guide only when direct cross-role evidence is necessary to explain a dependency, interface, or collaboration boundary. The target role remains the organizing perspective, and secondary evidence does not establish secondary ownership.
```

Replace its final paragraph with:

```markdown
Load the shared `role-analysis-framework.md` and exactly one primary role guide. Load at most one secondary role guide when direct cross-role evidence meets the boundary above. Use the primary role to order career material and the secondary role only to frame collaboration or breadth. For a target role outside the seven supported categories, choose the closest primary guide and state the mapping reason and unsupported boundary in the final document.
```

- [ ] **Step 6: Run focused and module tests**

Run:

```text
python -m unittest tests.test_skill_contract -v
```

Expected: all `SkillContractTests` pass.

- [ ] **Step 7: Commit the shared framework**

```text
git add tests/test_skill_contract.py skills/summarizing-internship-work/SKILL.md skills/summarizing-internship-work/references/role-classification.md skills/summarizing-internship-work/references/role-analysis-framework.md
git commit -m "Add shared role analysis framework"
```

### Task 2: Deepen frontend and backend guides

**Files:**
- Modify: `skills/summarizing-internship-work/references/role-frontend.md`
- Modify: `skills/summarizing-internship-work/references/role-backend.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: the ten-part analysis contract from Task 1.
- Produces: detailed frontend and backend guides using the exact required headings and distinct evidence markers.

- [ ] **Step 1: Add the reusable guide assertion and failing tests**

Add these constants near the other test constants:

```python
ROLE_REQUIRED_HEADINGS = (
    "## Role Boundary and Subdomains",
    "## Entry-Point Discovery",
    "## Typical Code Chains",
    "## Technical Decision Matrix",
    "## Failure Modes and Risks",
    "## Validation Evidence",
    "## Impact and Metrics Evidence",
    "## Resume Mapping",
    "## Interview Question Tree",
    "## Overclaim Guardrails",
)
```

Replace `test_role_guides_supply_topics_without_extra_question_gates` with this name and body so it validates the surviving confirmation contract without requiring the retired `Evidence Topics` heading:

```python
def test_role_guides_do_not_add_question_gates(self) -> None:
    role_guides = sorted(
        path
        for path in (SKILL_DIR / "references").glob("role-*.md")
        if path.name not in {"role-analysis-framework.md", "role-classification.md"}
    )
    self.assertEqual(7, len(role_guides))
    for guide in role_guides:
        text = guide.read_text(encoding="utf-8")
        self.assertIn("main consolidated confirmation process", text, guide.name)
        self.assertIn("does not add confirmation rounds", text, guide.name)
        self.assertNotRegex(text, r"(?im)^Ask\b", guide.name)
        self.assertNotRegex(text, r"(?i)ask[^.]*Git identity", guide.name)
```

Add this helper to `SkillContractTests`:

```python
def _assert_deep_role_guide(self, filename: str, markers: tuple[str, ...]) -> None:
    text = (SKILL_DIR / "references" / filename).read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    self.assertGreaterEqual(line_count, 120, filename)
    self.assertLessEqual(line_count, 180, filename)
    for heading in ROLE_REQUIRED_HEADINGS:
        self.assertIn(heading, text, filename)
    for marker in markers:
        self.assertIn(marker, text, filename)
    self.assertIn("main consolidated confirmation process", text, filename)
    self.assertIn("does not add confirmation rounds", text, filename)
    self.assertNotRegex(text, r"(?im)^Ask\b", filename)
    self.assertNotRegex(text, r"(?i)ask[^.]*Git identity", filename)
```

Add these tests:

```python
def test_frontend_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-frontend.md",
        (
            "request race",
            "rendering boundary",
            "accessibility tree",
            "Core Web Vitals",
            "design-system",
            "end-to-end user flow",
        ),
    )

def test_backend_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-backend.md",
        (
            "idempotency",
            "transaction boundary",
            "cache invalidation",
            "message delivery",
            "authorization policy",
            "observability",
        ),
    )
```

- [ ] **Step 2: Run the new tests and verify RED**

Run:

```text
python -m unittest tests.test_skill_contract.SkillContractTests.test_frontend_guide_has_role_specific_depth tests.test_skill_contract.SkillContractTests.test_backend_guide_has_role_specific_depth -v
```

Expected: both tests FAIL because the existing five-section guides lack the ten-section contract and required markers.

- [ ] **Step 3: Replace `role-frontend.md` with a detailed guide**

Use all ten exact headings. Include these required contents:

| Section | Required frontend content |
|---|---|
| Role Boundary and Subdomains | Browser UI, design-system components, client state, data fetching, accessibility, analytics, browser performance; distinguish API and visual-design ownership |
| Entry-Point Discovery | Routes, page registration, visible strings, component imports, state stores, query hooks, CSS/theme tokens, event handlers, analytics events, browser tests |
| Typical Code Chains | Page flow; form mutation; list/detail cache; permission-gated UI; design-system component; analytics event; each chain ends at API or browser-test boundary |
| Technical Decision Matrix | Local/shared/server state; controlled/uncontrolled input; optimistic/pessimistic update; render/client/server boundary; request cancellation; component reuse; evidence and prohibited inference columns |
| Failure Modes and Risks | Request race, stale closure, duplicate submission, hydration mismatch, focus loss, inaccessible label, layout shift, partial loading, stale cache, localization overflow |
| Validation Evidence | Component tests, integration tests, browser E2E, accessibility tree assertions, visual regression, performance trace; state what each can and cannot prove |
| Impact and Metrics Evidence | Core Web Vitals, task completion, error rate, accessibility audit, bundle size, support feedback; require cited reports or user confirmation |
| Resume Mapping | Conservative implementation wording; standard wording with attributable cross-layer validation; impact wording only with verified user/performance evidence |
| Interview Question Tree | Foundation, rendering/state detail, trade-off, race diagnosis, scale/design-system extension, and broken-network/accessibility scenarios |
| Overclaim Guardrails | Component presence is not end-to-end ownership; consuming an API is not backend ownership; do not infer conversion, compliance, production performance, or design authorship |

Retain the exact sentence: `Route material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.`

- [ ] **Step 4: Replace `role-backend.md` with a detailed guide**

Use all ten exact headings. Include these required contents:

| Section | Required backend content |
|---|---|
| Role Boundary and Subdomains | Transport/API, application service, domain logic, persistence, async worker, integration, authorization, operability; distinguish client and infrastructure ownership |
| Entry-Point Discovery | Route registration, controller/handler, validators, middleware, service interfaces, repository/ORM, migrations, event producers/consumers, configuration and tests |
| Typical Code Chains | Request/response; write transaction; read/cache; async message; scheduled job; authorization decision; each includes failure and test boundaries |
| Technical Decision Matrix | API compatibility, validation placement, transaction boundary, idempotency key, isolation/concurrency, cache invalidation, message delivery semantics, retry/dead-letter behavior |
| Failure Modes and Risks | Partial write, duplicate request, lost update, stale cache, poison message, authorization bypass, timeout amplification, schema drift, retry storm |
| Validation Evidence | Unit, contract, integration/database, concurrency, migration, fault-injection and observability evidence; distinguish configured behavior from production behavior |
| Impact and Metrics Evidence | Latency percentiles, error rate, throughput, queue lag, retry/dead-letter counts, incident evidence and data-correction records; require cited evidence |
| Resume Mapping | Conservative endpoint/logic wording; standard end-to-end service wording with tests; impact wording only with verified operational or business outcomes |
| Interview Question Tree | Contract/domain foundations, transaction detail, alternative consistency models, timeout diagnosis, scale/partition scenarios and incident response |
| Overclaim Guardrails | Do not infer traffic, uptime, latency gains, incident prevention or sole service ownership; configuration is not proof of deployment |

Retain the same consolidated-confirmation sentence required for frontend.

- [ ] **Step 5: Run focused and module tests**

Run:

```text
python -m unittest tests.test_skill_contract.SkillContractTests.test_frontend_guide_has_role_specific_depth tests.test_skill_contract.SkillContractTests.test_backend_guide_has_role_specific_depth -v
python -m unittest tests.test_skill_contract -v
```

Expected: all selected and module tests pass.

- [ ] **Step 6: Commit frontend and backend guidance**

```text
git add tests/test_skill_contract.py skills/summarizing-internship-work/references/role-frontend.md skills/summarizing-internship-work/references/role-backend.md
git commit -m "Deepen frontend and backend role guidance"
```

### Task 3: Deepen client and testing guides

**Files:**
- Modify: `skills/summarizing-internship-work/references/role-client.md`
- Modify: `skills/summarizing-internship-work/references/role-testing.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: the shared framework and `_assert_deep_role_guide` helper.
- Produces: detailed client and testing guides with distinct platform and quality-engineering evidence.

- [ ] **Step 1: Write failing client and testing tests**

Add:

```python
def test_client_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-client.md",
        (
            "lifecycle transition",
            "offline queue",
            "weak-network",
            "thread confinement",
            "resource pressure",
            "platform adaptation",
        ),
    )

def test_testing_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-testing.md",
        (
            "risk model",
            "test pyramid",
            "fixture isolation",
            "flaky-test",
            "mutation testing",
            "release gate",
        ),
    )
```

- [ ] **Step 2: Run the tests and verify RED**

Run the two fully qualified tests above. Expected: both FAIL on missing headings and markers.

- [ ] **Step 3: Expand the client guide**

Use the ten exact headings and cover:

- Boundaries: mobile, desktop, native or cross-platform UI; lifecycle, network, local storage, platform service, packaging and telemetry boundaries.
- Discovery: screen/navigation registration, view model or store, lifecycle callbacks, API client, persistence schema, background task, permission manifest, platform adapter and device tests.
- Chains: screen-to-state, online request, offline queue and replay, local migration, push/deep link, background sync, permission flow and release packaging.
- Decisions: state ownership, lifecycle transition handling, cache/source of truth, offline conflict strategy, weak-network retry, thread confinement, resource cleanup and platform abstraction.
- Risks: stale screen state, duplicate replay, data loss, main-thread blocking, resource pressure, permission denial, background suspension, version migration and platform divergence.
- Validation: unit, integration, device/emulator, lifecycle, weak-network, migration, crash and release evidence with explicit proof boundaries.
- Metrics: crash-free sessions, ANR/hang, startup, memory, battery, sync failure, store feedback and adoption only from cited sources.
- Resume/interview: map evidence to robust client behavior; include lifecycle, offline conflict, concurrency, resource and cross-platform scenarios.
- Guardrails: shared API code is not client authorship; do not infer store adoption, device reach, crash reduction or production behavior.

Retain the consolidated-confirmation sentence.

- [ ] **Step 4: Expand the testing guide**

Use the ten exact headings and cover:

- Boundaries: requirement risk analysis, test design, fixtures, automation, environment, quality reporting, release gate and defect diagnosis.
- Discovery: test suites, markers/tags, fixture factories, mocks/fakes, environment setup, CI jobs, coverage config, failure reports and linked fixes.
- Chains: requirement-to-test, defect-to-regression, fixture/data setup, API/UI automation, flaky-test diagnosis, release gate and production-issue reproduction.
- Decisions: risk model, test pyramid, boundary selection, fixture isolation, real dependency versus double, deterministic time/randomness, parallelism and retry policy.
- Risks: false positive/negative, shared-state leakage, order dependency, flaky-test masking, weak assertion, environment drift, over-mocking and slow feedback.
- Validation: red-green regression evidence, mutation testing, coverage with boundary interpretation, repeated/parallel execution, CI matrix and defect linkage.
- Metrics: failure detection, flaky rate, duration, escaped defects, reruns, quarantine and release gate outcomes only from cited records.
- Resume/interview: emphasize risk reduction and diagnosability; include nondeterminism, environment parity, prioritization and release-decision scenarios.
- Guardrails: test presence does not prove prevention, complete coverage, zero defects or release impact; separate test, product-code, defect and review authorship.

Retain the consolidated-confirmation sentence.

- [ ] **Step 5: Run tests and commit**

Run the two focused tests and `python -m unittest tests.test_skill_contract -v`. Expected: PASS.

```text
git add tests/test_skill_contract.py skills/summarizing-internship-work/references/role-client.md skills/summarizing-internship-work/references/role-testing.md
git commit -m "Deepen client and testing role guidance"
```

### Task 4: Deepen DevOps and data-analytics guides

**Files:**
- Modify: `skills/summarizing-internship-work/references/role-devops.md`
- Modify: `skills/summarizing-internship-work/references/role-data-analytics.md`
- Modify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: the shared framework and deep-guide assertion helper.
- Produces: detailed delivery/operations and analytics guides.

- [ ] **Step 1: Write failing DevOps and data-analytics tests**

Add:

```python
def test_devops_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-devops.md",
        (
            "artifact provenance",
            "environment parity",
            "progressive delivery",
            "rollback trigger",
            "least privilege",
            "recovery objective",
        ),
    )

def test_data_analytics_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-data-analytics.md",
        (
            "metric grain",
            "late-arriving data",
            "slowly changing dimension",
            "data lineage",
            "experiment bias",
            "dashboard consumer",
        ),
    )
```

- [ ] **Step 2: Run the tests and verify RED**

Run the two fully qualified tests. Expected: FAIL on missing headings and markers.

- [ ] **Step 3: Expand the DevOps guide**

Use the ten exact headings and cover:

- Boundaries and discovery across triggers, build/test, artifact provenance, infrastructure, configuration, secrets references, deployment, health, rollback, observability and incidents.
- Chains for pull-request validation, artifact promotion, infrastructure change, progressive delivery, rollback, alert-to-runbook and incident fix.
- Decisions for cache/reproducibility, environment parity, immutable artifacts, deployment strategy, rollback trigger, least privilege, secret rotation, SLI/SLO and recovery objective.
- Risks including unpinned actions, mutable artifacts, environment drift, privilege expansion, secret leakage, partial rollout, false health checks, alert fatigue and unrehearsed recovery.
- Validation through CI run records, artifact digests, plan/dry-run, staging, health checks, rollback exercises, alert tests and incident timelines.
- Metrics only from run or operational evidence: lead time, deployment frequency, failure rate, recovery time, availability, cost and alert quality.
- Resume/interview mappings and pipeline failure, secret exposure, regional failure and rollback scenarios.
- Guardrails against claiming deployment success, uptime, cost savings or incident prevention from configuration alone.

Retain the consolidated-confirmation sentence.

- [ ] **Step 4: Expand the data-analytics guide**

Use the ten exact headings and cover:

- Boundaries and discovery across source contracts, ingestion, staging, transformation, SQL models, semantic metrics, quality checks, scheduling, dashboards and consumers.
- Chains for source-to-model, metric definition, incremental model, dimension history, quality incident, dashboard and experiment analysis.
- Decisions for metric grain, join cardinality, event time, late-arriving data, slowly changing dimension, incremental strategy, null/duplicate policy and experiment bias.
- Risks including fan-out joins, leakage, survivorship/selection bias, timezone drift, stale data, schema drift and misleading aggregation.
- Validation through schema/contract tests, reconciliation, uniqueness/completeness, freshness, lineage, query-plan checks, peer review and experiment diagnostics.
- Metrics from catalog, scheduler, warehouse, experiment or confirmed stakeholder evidence; distinguish dashboard consumer from business outcome.
- Resume/interview mappings and broken metric, backfill, experiment disagreement and executive-dashboard scenarios.
- Guardrails against inferring revenue, decision quality, freshness or accuracy from query presence; redact sensitive data and private links.

Retain the consolidated-confirmation sentence.

- [ ] **Step 5: Run tests and commit**

Run the two focused tests and the complete skill-contract module. Expected: PASS.

```text
git add tests/test_skill_contract.py skills/summarizing-internship-work/references/role-devops.md skills/summarizing-internship-work/references/role-data-analytics.md
git commit -m "Deepen DevOps and analytics role guidance"
```

### Task 5: Deepen the algorithm guide and verify the complete role system

**Files:**
- Modify: `skills/summarizing-internship-work/references/role-algorithm.md`
- Modify: `tests/test_skill_contract.py`
- Verify: all Skill, packaging, and Git collector files

**Interfaces:**
- Consumes: the shared framework and six completed role guides.
- Produces: the seventh detailed guide and a complete seven-guide structural/uniqueness contract.

- [ ] **Step 1: Write failing algorithm and complete-system tests**

Add:

```python
def test_algorithm_guide_has_role_specific_depth(self) -> None:
    self._assert_deep_role_guide(
        "role-algorithm.md",
        (
            "label leakage",
            "baseline",
            "offline evaluation",
            "online experiment",
            "model drift",
            "inference budget",
        ),
    )

def test_exactly_seven_distinct_deep_role_guides_exist(self) -> None:
    role_guides = sorted(
        path
        for path in (SKILL_DIR / "references").glob("role-*.md")
        if path.name not in {"role-analysis-framework.md", "role-classification.md"}
    )
    self.assertEqual(7, len(role_guides))
    bodies = []
    for guide in role_guides:
        text = guide.read_text(encoding="utf-8")
        for heading in ROLE_REQUIRED_HEADINGS:
            self.assertIn(heading, text, guide.name)
        bodies.append(text)
    self.assertEqual(len(bodies), len(set(bodies)))
```

- [ ] **Step 2: Run the tests and verify RED**

Run the two new tests. Expected: the algorithm-depth test FAILS; the seven-guide structure test also FAILS until the algorithm guide is expanded.

- [ ] **Step 3: Expand the algorithm guide**

Use the ten exact headings and cover:

- Boundaries and discovery across problem formulation, dataset/labels, preprocessing, features, model or optimizer, training, evaluation, experiment, inference integration and monitoring.
- Chains for supervised training, ranking/retrieval, rule/optimization method, feature pipeline, offline evaluation, online experiment and inference serving.
- Decisions for target/label definition, split strategy, baseline, metric choice, threshold, model complexity, robustness, reproducibility, online experiment and inference budget.
- Risks including label leakage, train/serve skew, class imbalance, overfitting, biased evaluation, irreproducibility, model drift, latency/resource breach and unsafe fallback.
- Validation through data checks, baseline comparison, ablation, cross-validation, slice/error analysis, reproducibility, load tests, online experiment and monitoring.
- Metrics from cited evaluation or experiment artifacts only; separate offline quality, online product effect, latency and resource cost.
- Resume/interview mappings and metric disagreement, drift, latency regression, unfair slice and rollback scenarios.
- Guardrails against treating CRUD, API wiring or model consumption as algorithm ownership; do not invent novelty, lift, dataset scale or sole ownership.

Retain the consolidated-confirmation sentence.

- [ ] **Step 4: Run focused and module verification**

Run:

```text
python -m unittest tests.test_skill_contract -v
```

Expected: all `SkillContractTests` pass.

- [ ] **Step 5: Commit the completed role system**

```text
git add tests/test_skill_contract.py skills/summarizing-internship-work/references/role-algorithm.md
git commit -m "Deepen algorithm role guidance"
```

- [ ] **Step 6: Run complete deterministic verification and review the final diff**

Run:

```text
python -m unittest tests.test_skill_contract -v
python -m unittest tests.test_packaging -v
python -m unittest tests.test_collect_git_evidence -v
python -m unittest discover -s tests -v
python -m compileall -q skills tests
git diff --check
```

Expected: all 43 existing tests plus the new contract tests pass; `compileall` and `git diff --check` exit 0 with no output. Record the new total from `unittest discover` rather than assuming a fixed number.

Then verify directly:

```text
git diff --stat 857530b..HEAD
git diff --check 857530b..HEAD
git status --short --branch
```

Expected: only the design, plan, `SKILL.md`, role references, and `tests/test_skill_contract.py` changed; no runtime outputs or intermediate artifacts exist; the worktree is clean after the final commit.
