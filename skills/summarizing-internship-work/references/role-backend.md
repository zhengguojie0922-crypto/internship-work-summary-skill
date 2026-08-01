# Backend Role Guide

Use this guide after the shared role analysis framework identifies backend as the primary role.
Trace a request or background behavior through source, failure handling, and validation before drafting career material.

## Role Boundary and Subdomains

- Treat transport/API, application service, and domain logic as backend evidence.
- Include persistence, async worker behavior, integrations, authorization, and operability when traced.
- Distinguish client consumption from service implementation and contract ownership.
- Distinguish infrastructure configuration from ownership of deployment or platform operations.
- Trace explicit boundaries between handler, service, repository, worker, and external dependency.
- Attribute shared work only when source or Git evidence identifies the contribution boundary.
- A migration or configuration change supports a narrow implementation claim, not system ownership.

## Entry-Point Discovery

- Start from route registration, controller or handler, command consumer, or scheduled-job registration.
- Locate validators, middleware, authentication, and authorization policy before the service call.
- Follow service interfaces into domain operations, repositories, ORM queries, and migrations.
- Locate event producers, consumers, queue configuration, and retry or dead-letter behavior.
- Inspect application configuration only alongside the code path that consumes it.
- Find integration, database, contract, concurrency, and fault-injection tests for the same behavior.
- Compare public and internal routes so compatibility claims state their exact audience.
- Record feature flags, environment variables, and credentials as configuration boundaries.
- Record request input, response or side effect, failure boundary, and last supported node.

## Typical Code Chains

- Request/response: route -> middleware -> validator -> service -> repository -> response and test boundary.
- Record invalid input, authorization failure, timeout, and mapped error response in that chain.
- Write transaction: handler -> service -> transaction boundary -> persistence -> commit/rollback and test boundary.
- Read/cache: handler -> service -> repository/cache -> invalidation path -> response and test boundary.
- Async message: producer -> broker contract -> consumer -> retry/dead-letter path -> test boundary.
- Scheduled job: scheduler -> job handler -> dependency -> partial-failure handling -> test boundary.
- Authorization decision: identity -> authorization policy -> protected operation -> denial test boundary.
- Name every external API, queue, or database boundary instead of claiming unseen downstream behavior.
- Stop at an unobserved broker, database trigger, vendor service, or deployment boundary.
- Separate an event publication attempt from evidence that an independent consumer acted on it.

## Technical Decision Matrix

| Decision | Evidence to inspect | Supported claim | Prohibited inference |
|---|---|---|---|
| API compatibility | route, schema, versioning, consumers | contract behavior | client adoption or zero breakage |
| Validation placement | validator, middleware, service checks | validation layer and scope | complete security posture |
| transaction boundary | transaction wrapper, writes, rollback tests | atomicity boundary in code | production isolation outcome |
| idempotency key | key storage, lookup, duplicate tests | duplicate-request handling | universal duplicate prevention |
| Isolation/concurrency | locks, version fields, retry paths | observed consistency mechanism | absence of lost update |
| cache invalidation | cache key, write path, expiry, tests | invalidation behavior | guaranteed freshness |
| message delivery | producer, consumer, acknowledgement | delivery semantics in code | exactly-once production delivery |
| Retry/dead-letter | retry policy, delay, dead-letter route | configured failure handling | incident prevention |

## Failure Modes and Risks

- Inspect partial write when operations cross a transaction boundary or external side effect.
- Inspect duplicate request behavior through idempotency, retries, and client timeout recovery.
- Inspect lost update risk around read-modify-write, concurrency controls, and isolation settings.
- Inspect stale cache after writes, expiry, cache invalidation, and read fallback paths.
- Inspect poison message handling through retry count, message delivery acknowledgement, and quarantine.
- Inspect authorization bypass at route, middleware, service, and repository-facing boundaries.
- Inspect timeout amplification across fan-out calls, retry layers, queues, and connection pools.
- Inspect schema drift between migrations, ORM models, serializers, contracts, and consumers.
- Inspect retry storm risk when transient failures share synchronized retry behavior.

## Validation Evidence

- Unit tests can prove pure domain logic and isolated error mapping under specified inputs.
- Contract tests can prove a declared API or message shape, not external consumer deployment status.
- Integration/database tests can prove repository and transaction behavior in their test environment.
- Concurrency tests can support a specific interleaving or consistency claim, not all production load.
- Migration tests can prove upgrade or rollback behavior within their declared database setup.
- Fault-injection tests can show selected timeout, retry, or dependency-failure handling.
- observability evidence can show emitted logs, metrics, or traces, not that anyone monitored them.
- Distinguish configured behavior from production behavior in every validation-based conclusion.
- Preserve test database engine, transaction mode, and concurrency harness when reporting results.
- Record whether fault injection targets the client, network, broker, database, or worker layer.

## Impact and Metrics Evidence

- Latency percentiles require a cited measurement, environment, time range, and traffic scope.
- Error rate requires a cited monitoring query, report, or incident record with denominator context.
- Throughput requires a cited load result or operational metric with workload definition.
- Queue lag requires a cited dashboard, alert, or report linked to the relevant consumer group.
- Retry and dead-letter counts require cited operational records and a stated message scope.
- Incident evidence and data-correction records require source, date, and attribution boundaries.
- Without cited evidence, state operational capability and validation rather than measured impact.

## Resume Mapping

- Conservative: implemented a named endpoint, domain rule, persistence change, or worker behavior.
- Cite the handler, service, repository, migration, and test boundary that support the wording.
- Standard: delivered an end-to-end service behavior when attributable tests span request to persistence.
- State external integration and infrastructure as boundaries unless direct evidence proves ownership.
- Impact: improved verified operational or business outcomes only with cited measurements or records.
- Keep metric source, baseline, timeframe, and collaboration boundary for each impact statement.
- Separate implemented safeguards from evidence that they prevented a particular incident.
- Describe review and operational support as collaboration unless attribution proves authorship.
- Treat rollout status as unknown unless deployment records or user evidence establish it.

## Interview Question Tree

- Contract/domain foundation: explain request shape, domain rule, response, and error boundary.
- Transaction detail: explain the transaction boundary, rollback path, and partial-write containment.
- Alternative consistency: compare idempotency, isolation, cache invalidation, and delivery choices.
- Timeout diagnosis: trace propagation, retries, backpressure, and observability evidence.
- Scale/partition scenario: explain queue partitioning, hot keys, ordering, and consumer implications.
- Incident response: explain detection, containment, data correction, communication, and follow-up tests.
- Answer from the traced implementation; distinguish a possible design from an observed deployment.

## Overclaim Guardrails

- Do not infer traffic, uptime, latency gains, incident prevention, or sole service ownership from code.
- Configuration is not proof of deployment, enabled monitoring, or infrastructure ownership.
- A repository call is not proof that a migration ran, a cache was warm, or a message was delivered.
- A test environment result is not a production reliability or performance result.
- Do not claim security or authorization effectiveness without direct policy and validation evidence.
- Do not convert a schema definition into proof that historical data was reconciled correctly.
- Do not describe a retry configuration as evidence of a completed recovery run.
- Route material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
