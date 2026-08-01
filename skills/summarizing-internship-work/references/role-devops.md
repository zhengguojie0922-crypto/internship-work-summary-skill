# DevOps Role Guide

## Role Boundary and Subdomains

- Treat DevOps work as delivery automation, infrastructure operations, reliability controls, and the evidence connecting them.
- Trace a change through workflow triggers, build and test jobs, artifact provenance, infrastructure, configuration, and secrets references.
- Include deployment, health, rollback, observability, alerting, incident response, cost controls, and recovery only when sources identify them.
- Separate configured capability from an actual execution record and from an operational result seen after execution.
- Separate pipeline authorship from application authorship, release approval, service ownership, and incident command.
- Treat a workflow file as configuration evidence, not evidence that every job ran or every stage deployed.
- Treat infrastructure definitions as intended resource state, not proof that a provider accepted or applied the change.
- Treat secret references as integration boundaries; never expose secret values, tokens, private URLs, or sensitive configuration.
- Stop at a managed platform, external action, unobserved deployment, or undocumented run result unless direct evidence continues the chain.
- Route material evidence gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.

## Entry-Point Discovery

- Start with pull-request triggers, scheduled workflows, manual dispatches, release tags, infrastructure modules, or an incident record.
- Locate build commands, dependency locks, test jobs, cache keys, artifact upload steps, and the artifact digest or version.
- Find artifact provenance inputs: source revision, builder identity, dependency versions, signatures, and promotion metadata.
- Inspect infrastructure providers, modules, variables, state backends, plan outputs, policy checks, and approved change records.
- Read configuration templates, environment overlays, feature flags, secret references, and rotation mechanisms without reading secret values.
- Locate deployment manifests, release controllers, change windows, health checks, canary rules, and rollback commands.
- Find monitoring definitions, SLI/SLO configuration, alert routing, runbooks, dashboards, and incident timeline links.
- Compare development, CI, staging, and production-like definitions to identify environment parity evidence or drift boundaries.
- Record the trigger, owner, environment, artifact identity, validation record, and last observed result before writing career material.
- Preserve missing run logs, apply outputs, and incident records as unknowns rather than assuming successful execution.

## Typical Code Chains

- Pull-request validation: pull request -> workflow trigger -> build and test jobs -> status artifact -> merge policy boundary; job failure -> failed status and diagnostic artifacts.
- Artifact promotion: source revision -> reproducible build -> immutable artifact digest -> staging validation -> promotion record; validation failure -> retain digest and block promotion.
- Infrastructure change: reviewed module change -> plan or dry-run -> policy check -> approved apply -> provider result; plan failure -> correct configuration before apply.
- Configuration change: environment overlay -> rendered deployment configuration -> controlled rollout -> runtime configuration observation; mismatch -> halt and reconcile the declared source.
- Progressive delivery: immutable artifact -> canary or phased cohort -> health and SLI observation -> expand rollout; threshold breach -> rollback trigger and stop expansion.
- Rollback path: failed deployment signal -> select prior verified artifact -> controlled rollback -> health verification -> incident record; rollback failure -> escalate through runbook.
- Alert-to-runbook: alert condition -> deduplication and routing -> runbook diagnosis -> mitigation action -> timeline evidence; false alert -> tune rule with preserved rationale.
- Incident fix: incident symptom -> scoped telemetry and logs -> corrective change -> validation run -> monitored recovery evidence; unresolved symptom -> continue incident ownership.
- Secret rotation: rotation event -> update reference or credential version -> consumer validation -> revoke prior version; validation failure -> preserve access only through approved recovery procedure.
- These chains show possible evidence paths and branches, not proof of deployment success, uptime, prevention, or business impact without records.

## Technical Decision Matrix

| Decision | Evidence to inspect | Supported claim | Prohibited inference |
| --- | --- | --- | --- |
| Build cache versus reproducibility | lockfiles, cache keys, clean build records | cache policy and reproducible inputs | faster delivery without measured runs |
| environment parity | overlays, variables, image versions, controlled comparisons | declared differences and parity controls | identical runtime behavior everywhere |
| Immutable artifacts | digest, registry policy, promotion metadata | artifact identity across stages | deployment completion or safety outcome |
| progressive delivery | cohort rules, health thresholds, rollout records | configured rollout strategy | reduced incident rate or universal availability |
| rollback trigger | threshold, approval rule, controller events | defined rollback condition | rollback actually executed successfully |
| least privilege | policy, role binding, access review | scoped access design | absence of unauthorized access |
| Secret rotation | version references, expiry policy, validation record | rotation mechanism and tested consumer boundary | no secret leakage or compromise |
| SLI/SLO and recovery objective | indicator definitions, error budget, runbook | operational targets and recovery intent | achieved availability or recovery performance |

## Failure Modes and Risks

- Unpinned actions or base images can change a build outside the reviewed source revision and weaken artifact provenance.
- Mutable tags can point a promotion step at a different artifact than the one previously validated.
- Environment drift can change permissions, dependencies, configuration, network rules, or data assumptions between stages.
- Privilege expansion can make a deployer, workflow, or emergency path broader than the documented least privilege boundary.
- Secret leakage can occur through logs, command echoes, artifacts, copied configuration, or unredacted incident notes.
- Partial rollout can leave mixed versions or schema compatibility risks when expand and rollback branches are incomplete.
- False health checks can report ready while user traffic, dependencies, or critical transactions remain impaired.
- Alert fatigue can hide a meaningful signal when thresholds, routing, deduplication, or ownership are not maintained.
- Unrehearsed recovery can fail under provider, region, data, or access constraints despite a documented runbook.
- Cost controls can shift cost or reliability to another service; do not claim savings without scoped billing evidence.

## Validation Evidence

- CI run records can prove named jobs, inputs, outputs, and result status for the recorded execution only.
- Artifact digests, signatures, attestations, and registry metadata can connect an artifact to its recorded source and builder boundary.
- Infrastructure plan or dry-run evidence can validate intended changes, while apply output is required to claim a provider accepted them.
- Staging evidence should state the environment, version, dependencies, test data, and differences from production-like conditions.
- Health checks should name the endpoint, threshold, observation window, and what workload or dependency they exclude.
- Rollback exercises can validate a rehearsed path, artifact selection, and observed recovery in the tested environment.
- Alert tests should show the injected condition, delivery route, deduplication behavior, and resulting runbook or ticket boundary.
- Incident timelines can establish observed sequence and response actions without assigning unsupported root cause or individual ownership.
- Controlled failure injection can validate a narrow resilience hypothesis; preserve safeguards and avoid implying full disaster recovery coverage.
- State whether the proof is static configuration, CI execution, staging execution, production observation, or cited operational record.

## Impact and Metrics Evidence

- Cite lead time only from delivery records that define start event, end event, repository or service scope, and time window.
- Cite deployment frequency only from release or deployment records with a stated environment and counting rule.
- Cite change failure rate only from a defined denominator, failure classification, and period rather than from a pipeline configuration.
- Cite recovery time only from incident records that define detection, restoration, and the recovery objective used for interpretation.
- Cite availability only from an SLI measurement source, scope, exclusions, and time window; a configured SLO is not an achieved result.
- Cite cost only from billing or allocation records that identify service, account, comparison period, and attribution limits.
- Cite alert quality from acknowledged alerts, false-positive classification, paging records, or a defined review process.
- Link a configuration or pipeline change to an operational metric only when dates, rollout scope, and attribution evidence support the relation.
- Use qualitative wording for repeatability, safety controls, or observability when sources show implementation but no measured operations result.
- Keep unsupported uptime, savings, incident-prevention, and performance metrics out of resume wording and label them as needing user input.

## Resume Mapping

- Map a traced build and test chain to automating a reproducible delivery path with the recorded trigger and artifact boundary.
- Map artifact provenance evidence to strengthening source-to-artifact traceability without claiming all releases were secure or successful.
- Map infrastructure plan and review evidence to maintaining declarative infrastructure and change validation, not provider-wide ownership.
- Map environment parity work to aligning declared configuration across named environments while preserving unverified runtime differences.
- Map progressive delivery configuration to introducing controlled rollout and rollback criteria, not to preventing incidents without records.
- Map least privilege evidence to narrowing or reviewing a documented access boundary without claiming a security outcome.
- Map alert and runbook evidence to improving diagnosability or response guidance when alert tests or timelines support it.
- Map recovery exercises to validating a tested recovery path with its environment and scope explicitly named.
- Prefer verbs such as automated, configured, traced, validated, hardened, rehearsed, or analyzed when source evidence supports them.
- Attach a source note for every rate, cost, availability, successful deployment, or incident-related outcome in a resume bullet.

## Interview Question Tree

- Pipeline failure scenario: explain the trigger, failed job, artifact and log evidence, ownership boundary, and the corrective branch.
- Reproducibility scenario: explain artifact provenance, pinned inputs, cache trade-off, immutable digest, and the validation record.
- Secret exposure scenario: explain redaction, least privilege, rotation scope, remediation path, and why no leak claim exceeds evidence.
- Deployment scenario: explain environment parity, progressive delivery cohort, health signal, expansion criteria, and rollback trigger.
- Rollback scenario: explain prior artifact selection, compatibility check, controlled rollback, verification, and escalation if recovery fails.
- Regional failure scenario: explain the recovery objective, dependencies, data and access constraints, runbook, and exercised evidence boundary.
- Alert scenario: explain signal design, routing, deduplication, runbook action, false-positive handling, and alert quality measurement.
- Infrastructure scenario: explain plan, policy, approval, apply result, drift detection, and what static configuration cannot prove.
- Metrics scenario: name the operational record, period, denominator, environment, attribution path, and unresolved uncertainty before stating impact.
- End each answer at the last supported node when real execution, operational outcome, or user impact is not evidenced.

## Overclaim Guardrails

- A workflow, manifest, or infrastructure module demonstrates configured capability, not a successful deployment or provider-side change.
- An artifact digest demonstrates identity and traceability, not that a user received the artifact or that it behaved correctly.
- A progressive delivery rule does not prove a canary expanded, a rollback occurred, or an incident was prevented.
- A health check does not prove application availability, customer success, dependency health, or recovery beyond its recorded scope.
- An access policy does not prove no privilege misuse, no secret leakage, or complete least privilege in all surrounding systems.
- An SLO or recovery objective does not prove achieved availability, recovery time, or disaster readiness without measured records.
- A cost setting does not prove savings without billing evidence and a defensible comparison period.
- Separate configuration author, pipeline operator, approver, service owner, incident commander, and platform provider ownership.
- Preserve missing logs, unknown environments, untested rollback paths, and unmeasured operations outcomes as explicit limitations.
- Route unresolved material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
