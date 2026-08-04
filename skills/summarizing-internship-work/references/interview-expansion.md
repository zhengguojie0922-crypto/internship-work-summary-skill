# Interview Expansion

Populate the feature deep dives, interview introductions, natural interview Q&A, and scenario questions in the final document from evidence-backed major outputs.

## Evidence-First Preparation

Before drafting, use the shared role framework to build an in-memory evidence matrix and feature model for every fully expanded output. Follow the feature from its business or system boundary through concrete files, symbols, callers, callees, data and state transitions, branches, dependencies, failures, configuration, tests, and applicable Git history. Keep this analysis in context; do not write an intermediate artifact.

Every project-specific question needs at least one concrete evidence anchor such as a file and symbol, a proved call-path segment, a branch, a test, a configuration item, or an applicable commit. Explain the relationship among the evidence anchors. A path, line range, search hit, framework convention, or plausible production outcome is not enough by itself.

## Feature Deep Dive

Explain the feature as a coherent system before asking detailed interview questions. Use evidence-appropriate headings and cover the supported equivalents of:

1. Feature positioning, contribution boundary, and essential terminology.
2. Business or system background and the original problem.
3. A causal failure sequence showing how the problem occurs.
4. The feature's position in the wider architecture.
5. Goals, non-goals, invariants, authority, and trust boundaries.
6. Core data, state, protocol, algorithm, or lifecycle model.
7. End-to-end happy path, recovery path, and important branches.
8. Failure semantics, edge cases, degradation, and observability.
9. Alternatives, trade-offs, and reasons supported by evidence.
10. A code responsibility map connecting files, symbols, callers, callees, and tests.
11. A test and fault-scenario matrix.

Do not turn this list into empty boilerplate headings. Combine, rename, or omit sections when the target role or evidence calls for it, but complete the underlying explanation before Q&A. This shared chapter carries context that would otherwise be repeated or compressed inside every answer.

## Interview Introductions

Write three introductions from the feature model:

- `30-second`: problem or context, personal action, and supported result.
- `1-minute`: scope, constraints, code path, decisions, collaboration boundary, and validation.
- `3-minute`: architecture position, data and error paths, alternatives, tests, evidence limits, and reflection.

The introductions and detailed answers must agree on scope, ownership, mechanism, validation, and impact boundaries. Use first-person ownership only when the selected feature or Git route supports it.

## Natural Interview Q&A

Treat the version 1.2 depth dimensions as an internal quality rubric, not a visible form. Do not emit `Detailed question`, `Interview intent`, `Code evidence`, `Reasoning process`, `Detailed first-person answer`, `Design trade-offs`, and similar peer labels for every question.

Render each core question in the requested output language using this natural shape:

```markdown
### Q1: [Project-specific question]

**Answer:**

[One coherent interview-ready answer in connected paragraphs.]

**Follow-up 1: [Question derived from a concrete claim]**

[A complete standalone answer.]

**Follow-up 2: [Question derived from a trade-off, failure, or changed constraint]**

[A complete standalone answer.]

**Evidence and boundary:**

[The anchors and uncertainty needed to keep the answer honest.]
```

Start the main answer with a direct conclusion that answers the question without preamble. Continue in connected paragraphs through the relevant business or system invariant, end-to-end implementation mechanism, state or data changes, error and recovery behavior, alternatives and trade-offs, validation, and personal contribution boundary. Select what the question needs; do not print those dimensions as a checklist.

The answer must teach the system directly. Connect files and symbols through control flow, data flow, state transitions, or protocol frames and explain what each relationship proves. Do not replace analysis with a citation such as `service.go:812-871`.

Derive follow-ups from concrete claims, mechanisms, trade-offs, failures, or evidence gaps in the main answer. Every follow-up must be shown and answered separately. Each answer must stand on its own, reconnect to project evidence, reason through the premise, and preserve attribution and evidence boundaries. Never place several follow-up questions on one line and answer them with one compressed paragraph.

Plan distinct questions from the feature model. Always merge duplicate questions when their evidence anchors, central conclusion, and answer path substantially overlap. Do not paraphrase one implementation detail into several questions or use generic textbook material to fill breadth.

## Scenario Questions

Add 3-5 scenario questions for every fully expanded output. Use the same natural presentation. Each scenario changes a constraint grounded in the feature, gives a complete diagnosis or decision answer, identifies affected code and state, compares trade-offs, defines validation and escalation, and includes separately displayed follow-ups with complete standalone answers. Distinguish current implementation evidence from proposed action under the hypothetical premise.

## Positive Shape Example

The following generic transaction example demonstrates answer shape only. It supplies no facts for another repository and is not a length template. Replace every mechanism and evidence statement with findings from the analyzed project.

### Q: Why must account initialization run in one database transaction?

**Answer:**

The transaction is needed because registration is not complete when only the user row exists. In this example, the usable-account invariant includes the user, initial entitlement, invitation consumption, default workspace membership, and onboarding answers. If any required row is missing, later requests can observe an account that exists but cannot behave as a valid account. The transaction makes that invariant atomic: either every required database change becomes visible, or none of them does.

The call path starts at `RegistrationController.register`, which validates request shape and calls `UserService.register`. The service performs non-transactional checks that do not need locks, then opens a transaction and passes the same transaction handle to `UserRepository.insert`, `EntitlementRepository.grantInitial`, `InvitationRepository.consume`, `WorkspaceRepository.addOwner`, and `OnboardingRepository.saveAnswers`. Each repository must execute through that handle. A transaction declared in the service is not sufficient if one repository silently uses the global connection pool.

Inside the transaction, each step returns an error to the service. Any error leaves the commit path and triggers rollback; commit occurs only after all required writes succeed. Unique constraints still protect concurrent registration or invitation reuse at the database boundary. The service maps those constraint failures to stable domain errors rather than treating them as an unexpected partial success.

The trade-off is a longer transaction touching several tables, which increases lock time and the number of ways the transaction can fail. I would therefore keep syntax checks, password-cost checks, and read-only invitation format validation outside it, while retaining writes and race-sensitive validation inside. I would not put email delivery or another remote service call inside the transaction because an external system cannot participate in the database rollback. A transactional outbox or post-commit job gives that side effect a retryable boundary.

I would validate the design with failure injection at every repository call and assert that no user, entitlement, invitation relation, workspace membership, or onboarding row remains. I would also test concurrent requests for the same identity and invitation, verify the relevant unique constraints, and confirm that every repository receives the same transaction handle. Those checks prove atomicity more directly than a happy-path registration test.

**Follow-up 1: Can the welcome-email API call stay inside the transaction?**

It should not. Holding database locks while waiting on a remote API increases transaction duration, and a database rollback cannot undo an email that the provider already accepted. The safer boundary is to write an outbox event in the same database transaction as account initialization, commit both together, and let a worker deliver the email with retries. The outbox record proves that every committed account has a durable delivery request without claiming the remote delivery itself is atomic with the database.

**Follow-up 2: What if commit succeeds but the HTTP response is lost?**

The client may retry even though the account already exists, so the operation needs a stable idempotency boundary. A unique identity constraint prevents duplicate users, but the service should also recognize the existing completed registration and return a deterministic result rather than exposing a generic conflict. If the API supports an idempotency key, store its result in the same transaction; otherwise query the completed account state after the uniqueness conflict and verify that the registration invariant is satisfied before returning success.

**Evidence and boundary:**

A real answer requires the controller and service symbols, proof that every repository uses the same transaction handle, database constraints, rollback behavior, and failure-path tests. Static code can prove the intended transaction boundary; it does not prove production lock duration, failure rate, or email delivery outcomes without runtime evidence.

## Degradation And Final Audit

When evidence is insufficient, inspect callers, callees, tests, configuration, documentation, and applicable Git history before reducing scope. Prefer fewer supported questions to compressed or invented ones; never pad or fabricate to meet a quota. State unknowns plainly and identify what evidence or user input would resolve them.

Before the single final document write, run a final quality audit in memory:

- the Feature Deep Dive explains the system before detailed questions begin;
- important code anchors are connected by proved relationships rather than listed alone;
- each main answer starts with a direct conclusion and continues as a coherent explanation in connected paragraphs;
- every follow-up is shown and answered separately with a complete standalone answer;
- questions cover distinct mechanisms, decisions, or failure modes;
- introductions, resume claims, main answers, and follow-ups use consistent facts and attribution;
- scenario answers distinguish current evidence from proposed actions;
- visible ten-field forms, answer hints, and generic advice are absent.

If an item fails the final quality audit, return to the evidence matrix, feature model, or question plan, inspect the relevant path more deeply, and repair the draft in memory before writing `career-output/实习产出与面试准备.md`.
