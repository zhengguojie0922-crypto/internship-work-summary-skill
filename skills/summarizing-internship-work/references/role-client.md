# Client Role Guide

## Role Boundary and Subdomains

- Treat client work as mobile, desktop, native, or cross-platform UI behavior that users run on a device.
- Set the boundary from screen composition through navigation, local state, platform lifecycle, and rendered interaction.
- Include network, local storage, platform services, packaging, telemetry, accessibility, and device behavior when the source shows them.
- Separate client-owned presentation or platform code from shared API libraries, backend contracts, and release operations.
- Identify whether evidence concerns a native module, a cross-platform bridge, or a platform adaptation layer.
- Attribute a screen, view model, store, adapter, or device test only when a change or source link supports that ownership.
- Treat consumed API schemas as integration context unless the evidence also shows the contributor authored the client call site.
- Treat release notes and store metadata as release context unless they name the client's platform work.
- Keep platform-specific behavior distinct from a common UI flow even when the same feature exists on several platforms.
- Route material evidence gaps through the main consolidated confirmation process; this guide does not add confirmation rounds.

## Entry-Point Discovery

- Start at screen, route, activity, scene, window, or navigation registration associated with the feature.
- Locate the view model, presenter, controller, reducer, or store that owns visible state and user actions.
- Trace lifecycle callbacks for foregrounding, backgrounding, recreation, suspension, and teardown.
- Find the API client, request interceptor, serialization model, and error mapping used by the screen.
- Inspect persistence schemas, migration registration, cache repositories, and invalidation paths for local data.
- Find background task registration, scheduler constraints, and cancellation hooks before claiming sync behavior.
- Read permission manifests, entitlement configuration, and platform-service adapters for camera, notifications, location, or files.
- Follow push and deep-link handlers to the destination route, state restoration, and authentication boundary.
- Locate device, emulator, snapshot, integration, and crash-report tests that directly exercise the claimed behavior.
- Record the source path and entry-point relation before turning a discovery observation into a career claim.

## Typical Code Chains

- Screen-to-state: route registration -> screen creation -> view model or store action -> rendered loading, content, or error state -> UI test boundary.
- Online request: user action -> state transition -> API client request -> decoded response -> store update -> screen render -> integration test boundary.
- Online failure: user action -> API client error -> mapped retryable or terminal state -> visible recovery action -> UI or integration test boundary.
- Offline queue: mutation intent -> durable offline queue write -> optimistic local state -> connectivity observer -> replay scheduler -> server acknowledgement -> queue removal.
- Offline conflict: replay request -> conflict response -> conflict policy -> merged, replaced, or user-resolved state -> durable local update -> integration test boundary.
- Queue retry: replay failure marked transient -> bounded retry metadata -> later eligible scheduling; permanent failure -> actionable error state without duplicate replay.
- Local migration: app startup -> schema version check -> ordered migration -> validation read -> repository exposure; migration failure -> recovery or blocked startup evidence.
- Push/deep link: platform callback -> payload validation -> authentication and navigation guard -> destination state load -> rendered target screen -> device test boundary.
- Background sync: scheduler trigger -> cancellation and network constraint check -> sync worker -> persisted result; constraint failure -> deferred execution rather than a false success.
- Permission flow: feature request -> platform permission prompt -> granted service call or denied fallback state -> screen feedback -> device test boundary.
- Release packaging: platform build configuration -> signing or bundle artifact -> version metadata -> telemetry initialization -> release validation evidence.
- These chains establish evidence paths, not proof that every downstream production transition occurred.

## Technical Decision Matrix

| Decision | Evidence to inspect | Supported claim | Prohibited inference |
|---|---|---|---|
| State ownership | Screen-local state, feature stores, shared repositories, restoration paths, and sharing tests | The named layer owns the demonstrated state scope and restoration behavior | The contributor designed the whole client architecture or every screen uses the same ownership model |
| Lifecycle transition handling | Foreground, background, recreation, suspension, teardown callbacks, cancellation hooks, and lifecycle tests | Durable work survives and ephemeral work stops at the evidenced transitions | All operating systems and lifecycle sequences are handled correctly in production |
| Cache source of truth | Repository interfaces, local schemas, server responses, invalidation code, and cache tests | The evidenced source is authoritative while named caches are disposable or durable as implemented | Cache presence proves freshness, offline reliability, or server ownership |
| Offline conflict strategy | Replay code, conflict responses, merge rules, persisted queue state, and conflict tests | The implementation uses the recorded last-write, merge, server-authoritative, or user-resolution policy | The policy prevents every duplicate, data-loss case, or cross-device conflict |
| weak-network retry | Error classification, retry bounds, backoff, cancellation, user feedback, and network-condition tests | The named failures receive bounded retry or terminal handling under tested conditions | Retry code proves successful recovery, continuous connectivity, or production reliability |
| thread confinement | Executor annotations, dispatch points, UI mutation sites, blocking work, and concurrency tests | UI state and blocking work stay on the evidenced executors | Async syntax alone proves responsiveness, race freedom, or safe teardown |
| Resource cleanup | Subscription ownership, listener removal, handle closure, background cancellation, and pressure tests | The named resources are released at the demonstrated lifecycle boundary | Cleanup code proves no leaks, low memory use, or battery improvement across devices |
| Platform abstraction | Shared interfaces, native adapters, permission and lifecycle branches, and platform tests | A stable feature contract delegates the evidenced platform-specific behavior | One adapter proves parity, portability, or ownership of every supported platform |
| Navigation restoration | Persisted identifiers, state decoding, authorization revalidation, current-data reload, and restore tests | The named route restores only the state and guards demonstrated by evidence | A registered route proves safe restoration for stale sessions or every deep link |
| Telemetry design | Event definitions, emission sites, consent guards, tests, dashboards, and alert records | The client emits the named instrumentation under the evidenced conditions | Event code proves collection, monitoring, metric movement, or product impact |

## Failure Modes and Risks

- Stale screen state can render an obsolete result after an out-of-order response or lifecycle restore.
- Duplicate replay can submit the same queued mutation twice when acknowledgement and durable queue deletion are not coordinated.
- Data loss can occur when an optimistic edit is neither persisted nor recoverable after process death.
- Main-thread blocking can cause visible hangs, ANR risk, delayed input, or poor startup without proving a measured incident.
- resource pressure can evict caches, terminate background work, or expose cleanup defects on memory-constrained devices.
- Permission denial needs a functional fallback, explanation, or disabled state rather than assuming access exists.
- Background suspension can interrupt sync and requires resumable work rather than a claim of continuous execution.
- Version migration can corrupt or strand persisted data if version ordering, rollback, and validation are missing.
- Platform divergence can produce unequal behavior when adapters hide different lifecycle, notification, or storage rules.
- Weak connectivity can leave a request indeterminate; distinguish timeout, offline, cancellation, and server rejection states.

## Validation Evidence

- Unit evidence can show reducer, view model, serializer, conflict policy, or retry classification behavior in isolation.
- Integration evidence can connect the client repository or API client to a controlled server contract and persistence boundary.
- Device or emulator evidence can show rendering, platform callback, permission, navigation, and package behavior on the tested configuration.
- Lifecycle evidence should exercise foreground, background, recreation, cancellation, and state restoration paths relevant to the claim.
- weak-network evidence should model timeout, loss, slow transfer, and recovery rather than only a generic failed request.
- Migration evidence should start from an older stored schema and verify readable intended data after the ordered upgrade.
- Crash evidence can show a reported exception or automated crash test, not a crash-rate reduction unless cited records establish it.
- Release evidence can show a validated build, signing configuration, or artifact; it does not prove store publication or user reach alone.
- State the proof boundary for every result: static implementation, automated test, device execution, or cited operational record.
- Preserve failed or incomplete validation as a limitation rather than converting it into a resilience claim.

## Impact and Metrics Evidence

- Cite crash-free sessions only from an identified telemetry or operational source with its time window and population.
- Cite ANR or hang outcomes only from platform reports or monitoring records, not from the presence of asynchronous code.
- Cite startup, memory, and battery measurements only when a benchmark, profiler capture, or recorded experiment supports them.
- Cite sync failure counts or rates only from logs, dashboards, reports, or a scoped test dataset that defines the denominator.
- Cite store feedback and adoption only from source records and distinguish qualitative feedback from aggregate usage.
- Link a client change to an observed metric only when the record establishes both the changed version and comparison basis.
- Report configuration, device class, network condition, and sample boundary when those conditions affect interpretation.
- Use qualitative impact language when the evidence shows a designed behavior but not a measured result.
- Do not infer store adoption, device reach, crash reduction, or production behavior from code, a package, or a test alone.
- Keep metrics outside resume wording when their source, scope, or attribution is uncertain.

## Resume Mapping

- Map a supported screen-to-state chain to a concise statement about implementing or improving a client workflow.
- Map lifecycle evidence to robust lifecycle behavior only when callbacks, state rules, and validation are traceable.
- Map offline conflict evidence to durable synchronization or conflict handling without claiming reliability outcomes that lack records.
- Map concurrency evidence to safe UI updates, background IO, or thread confinement at the demonstrated boundary.
- Map cleanup evidence to resource management when lifecycle ownership and released resources are visible in the implementation or tests.
- Map platform adaptation evidence to compatible platform behavior while naming the relevant adapter or platform constraint.
- Name tests or release validation as verification work, not as proof that users experienced the intended outcome.
- Keep shared API code as context unless the contributor's client call-site or UI integration ownership is supported.
- Prefer verbs such as implemented, traced, validated, or improved when they match the evidence classification.
- Attach an evidence note for every quantitative or production-facing clause before using it in a resume bullet.

## Interview Question Tree

- Lifecycle scenario: explain the lifecycle transition, state ownership, cancellation, restoration, and the evidence that validates it.
- Offline scenario: explain queue persistence, replay eligibility, acknowledgement handling, duplicate prevention, and conflict resolution.
- Weak-network scenario: distinguish retryable transport failure from cancellation, rejection, and an indeterminate request outcome.
- Concurrency scenario: explain which executor owns UI state, which work leaves it, and how returned results are guarded after teardown.
- Resource scenario: explain subscriptions, caches, background work, resource pressure, and cleanup at the relevant lifecycle boundary.
- Cross-platform scenario: explain the shared feature contract, platform adaptation points, and where behavior deliberately differs.
- Migration scenario: explain stored-version detection, migration ordering, failure recovery, and data validation after upgrade.
- Permission scenario: explain the prompt trigger, denial path, later grant path, and device-level validation evidence.
- Metrics scenario: name the source, scope, denominator, comparison period, and remaining attribution limits before stating impact.
- End each answer at the last supported evidence node when runtime or outcome evidence is unavailable.

## Overclaim Guardrails

- Shared API code is not client authorship without a supported client integration, state, or platform change.
- A navigation route does not prove device reach, release adoption, or successful production use.
- A device test does not prove every platform, OS version, form factor, or network condition is covered.
- An offline queue implementation does not prove no data loss or duplicate submission without tested or operational evidence.
- Asynchronous work does not prove startup, memory, battery, hang, or crash improvement without measured records.
- A telemetry event does not prove the event was collected, monitored, or acted upon in production.
- A release artifact does not prove store approval, rollout completion, adoption, or incident-free behavior.
- Separate client, API, backend, platform, test, review, and release authorship in every evidence chain.
- Preserve unknown platform behavior, unsupported devices, and missing metrics as explicit limitations.
- Route material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
