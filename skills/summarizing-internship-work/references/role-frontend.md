# Frontend Role Guide

Use this guide after the shared role analysis framework identifies frontend as the primary role.
Trace a user-visible behavior through source and tests before drafting career material.

## Role Boundary and Subdomains

- Treat browser UI, routes, and page composition as frontend evidence.
- Include design-system components, client state, data fetching, and browser performance.
- Include accessibility and analytics when source connects them to the selected user flow.
- Attribute API ownership only when server definitions or Git attribution directly support it.
- Attribute visual-design ownership only when design artifacts or user evidence support authorship.
- A frontend consumer can describe a contract boundary without claiming API implementation.
- A component change can describe implementation without claiming the full product surface.

## Entry-Point Discovery

- Start from route registration, page registration, or a visible string in the target flow.
- Follow component imports from the page toward behavior-specific child components.
- Locate state stores, query hooks, mutation hooks, and selectors that control the view.
- Search CSS modules, theme tokens, and design-system primitives for rendered appearance.
- Trace event handlers from clicks, input changes, submit actions, and keyboard actions.
- Locate analytics events only when their payload and triggering interaction are connected.
- Find browser tests, component tests, and fixtures that name the same workflow.
- Compare route-level composition with shared layout ownership before expanding attribution.
- Record feature flags, locale providers, and experiment wrappers as conditional boundaries.
- Record each source path, caller, boundary, and last supported node in the evidence chain.

## Typical Code Chains

- Page flow: route -> page registration -> component tree -> query hook -> API boundary.
- Confirm the page's loading, empty, error, and success branches before claiming coverage.
- Form mutation: input -> validation -> submit handler -> mutation -> API or browser-test boundary.
- Record disabled states, duplicate-submission protection, and response-to-UI mapping.
- List/detail cache: list query -> cache key -> detail mutation -> invalidation -> API boundary.
- Permission-gated UI: identity state -> authorization check -> rendered branch -> browser-test boundary.
- Design-system component: consumer -> shared primitive -> token or style -> visual-test boundary.
- Analytics event: user action -> handler -> event payload -> analytics API boundary.
- Call a flow end-to-end only when browser E2E or direct evidence spans its user boundary.
- Stop the chain at an opaque SDK, untested browser interaction, or undocumented API response.
- Mark inferred runtime sequencing as unknown instead of converting it into a behavior claim.

## Technical Decision Matrix

| Decision | Evidence to inspect | Supported claim | Prohibited inference |
|---|---|---|---|
| Local, shared, or server state | owner, store, query hook, consumers | state placement and scope | team-wide architecture intent |
| Controlled or uncontrolled input | value, defaultValue, handlers, validation | input behavior and trade-off | accessibility compliance by itself |
| Optimistic or pessimistic update | mutation callbacks, rollback, disabled state | visible consistency behavior | production reliability outcome |
| rendering boundary | server/client annotations, data boundary, hydration path | where rendering occurs | overall rendering strategy ownership |
| Request cancellation | abort signal, cleanup, query lifecycle | cancellation handling | absence of request race |
| Component reuse | imports, props, tokens, test consumers | shared implementation use | design-system authorship |

## Failure Modes and Risks

- Inspect a request race when route changes or repeated input can reorder responses.
- Inspect stale closure risk in callbacks, effects, delayed handlers, and mutation completions.
- Inspect duplicate submission through disabled controls, pending state, and idempotent UI behavior.
- Inspect hydration mismatch at the rendering boundary between server output and browser state.
- Inspect focus loss after rerender, modal transitions, validation errors, and list replacement.
- Inspect inaccessible label connections, error announcements, keyboard order, and accessibility tree output.
- Inspect layout shift from images, async content, font loading, and skeleton replacement.
- Inspect partial loading when independently fetched regions resolve or fail at different times.
- Inspect stale cache after mutations, navigation, and optimistic rollback.
- Inspect localization overflow in controls, tables, error text, and responsive layouts.

## Validation Evidence

- Component tests can prove isolated rendering, interaction, and state transitions in a controlled setup.
- Component tests cannot prove deployed routing, real network timing, or complete user journeys.
- Integration tests can prove connected components and mocked or local contract behavior.
- Browser E2E can support an end-to-end user flow when it exercises the visible path and assertions.
- Browser E2E cannot prove production conversion, browser population coverage, or API ownership.
- accessibility tree assertions can prove exposed names, roles, and selected relationships at test time.
- Visual regression can reveal intended render differences but cannot establish visual-design authorship.
- A performance trace can show measured browser work; preserve environment and metric details.
- Cite exact test names, trace files, commit context, and boundaries in the evidence record.
- Treat test setup, feature flags, and mocked responses as limits on what a test demonstrates.
- Prefer a narrowly named test assertion over a broad claim that the entire screen is correct.

## Impact and Metrics Evidence

- Core Web Vitals require a cited report, trace, or user confirmation with collection context.
- Task completion requires product analytics, study evidence, or explicit user-provided results.
- Error rate requires a cited monitoring query, report, or confirmed operational record.
- Accessibility audit results require the audit output, scope, date, and unresolved finding boundary.
- Bundle size requires a comparable build report and a defined asset or route scope.
- Support feedback requires a cited issue, feedback summary, or user-confirmed interpretation.
- Without such evidence, describe capability, validation, and expected boundary rather than impact.

## Resume Mapping

- Conservative: implemented a named page, component, state transition, or validation behavior.
- Cite the route, components, and test boundary that support the implementation wording.
- Standard: delivered a user flow across UI state and API consumption with attributable validation.
- Use standard wording only when tests or source connect the relevant layers and ownership.
- Impact: improved a verified user, performance, or accessibility outcome with cited evidence.
- Keep metric source, baseline, timeframe, and ownership boundary available for the impact claim.
- Separate authored implementation from review, pairing, migration support, and adjacent fixes.
- Preserve the difference between a release candidate result and a production user outcome.

## Interview Question Tree

- Foundation: explain the user flow, route entry, component responsibilities, and API boundary.
- Rendering/state detail: explain state placement, rendering boundary, and loading/error transitions.
- Trade-off: compare local/shared/server state or controlled/uncontrolled input using code evidence.
- Race diagnosis: explain how a request race or stale cache would appear and be contained.
- Scale/design-system extension: explain token, prop, reuse, and compatibility effects of extension.
- Broken-network scenario: describe partial loading, retry state, cancellation, and user feedback.
- Accessibility scenario: describe focus, accessible names, error announcement, and test evidence.
- Answer only from the traced chain; label unknown runtime behavior as needing user input.

## Overclaim Guardrails

- Component presence is not end-to-end ownership without a connected user-flow boundary.
- Consuming an API is not backend ownership or evidence of server-side implementation.
- Do not infer conversion, compliance, production performance, or design authorship from source alone.
- Do not infer accessibility compliance from one label, one test, or a component library import.
- Do not turn a configured metric, analytics event, or performance code path into a measured result.
- Route material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
