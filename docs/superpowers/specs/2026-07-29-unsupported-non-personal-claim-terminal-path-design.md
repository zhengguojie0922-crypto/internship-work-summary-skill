# Unsupported Non-Personal Claim Terminal Path Design

## Context

The `algorithm-attribution` forward-test fixture contains account-settings backend and client changes but no algorithm implementation. The request is explicitly non-personal and asks whether the fixture supports an algorithm-work claim. After the user confirms that no untracked or external algorithm evidence exists, the current Skill still requires a target-role work item before producing facts and career artifacts. Codex therefore repeats evidence-gap questions and never reaches `resume-audit.json`.

Controller retries cannot resolve this conflict. The controller already preserves the original request, role, non-personal scope, fixture boundary, and the user's external-evidence answer. The missing behavior belongs in the Skill contract.

## Decision

Add a terminal workflow to `SKILL.md` that applies only when all three predicates are true:

1. The request explicitly asks for a non-personal claim assessment.
2. The confirmed inspected scope contains no implementation evidence for the target role.
3. The user confirms that no untracked or external evidence is available for that claim.

Treat the third predicate as resolving the Source-Only Hard Gate question. Do not ask for the same evidence again. Do not infer a contribution from absence or from adjacent work in another role.

## Artifact Contract

The facts stage remains real and schema-valid even though it contains no target-role work item:

- `fact-cards.json` uses `work_items: []`.
- `fact-cards.md` states that the inspected scope supports no target-role work item.
- The response preserves the inspected-scope boundary and states that absence in the fixture does not prove absence elsewhere.

The career stage completes the assessment without manufacturing a resume claim:

- `career-package.md` gives an unsupported-claim verdict and refusal.
- `resume-audit.json` uses `entries: []`.
- No resume bullet, achievement, interview narrative, low-confidence claim, or personal attribution is generated.

Existing schemas already permit empty arrays, so no schema or validator change is required. Canonical artifact filenames, requested language, path validation, strict-stage progression, and fast-mode behavior remain unchanged.

## Stage Behavior

In strict mode, the user's no-external-evidence answer closes the pending evidence question. The next facts response emits both fact-card artifacts and stops at the existing facts confirmation point. After confirmation, the career response emits both career artifacts and completes the workflow.

In fast mode, the same terminal artifacts may appear in the single four-stage draft response. The terminal path does not relax confirmation rules for other requests.

## Decision Intake Before Gates

The `final-9e-probe-01` forward test showed that defining the terminal artifacts is insufficient when the model does not first record supplied decisions. The model recorded the collaborator-context answer but treated the adjacent supporting-documentation answer and exact algorithm claim as unresolved. It also entered the identity gate despite the explicit non-personal declaration.

Add a decision-intake ledger before the identity and source-only gates. On every turn, scan the complete current user message and record these fields before asking any question: analysis kind, identity state, claim target, target role, collaborator-code decision, supporting-documentation decision, and external-evidence decision. Values explicitly supplied in the initial request, a labelled original-request block, or a continuation answer are resolved values. A resolved value cannot be reclassified as pending in the same turn.

Use the ledger as the sole input to the identity, evidence-gap, and terminal-path gates. An explicit non-personal declaration resolves identity as not applicable. An explicit role phrase inside the claim resolves the target role. Explicit include/exclude and available/unavailable answers resolve their corresponding decisions. This is a general intake rule, not a scenario-specific controller exception.

The green forward-test controller must exercise this interface directly. For the non-personal algorithm scenario, place a `Resolved current-turn decision ledger` before narrative continuation text in the initial prompt and every continuation. Use explicit `field: value` lines for the seven Skill fields plus current-stage confirmations. Values may only restate the scenario request and synthetic user decisions; never include rubric, required claims, forbidden claims, required questions, or grader conclusions. Baseline prompts remain unchanged.

The Skill frontmatter trigger must name non-personal claim assessment explicitly. A forced activation whose description only advertises personal-work discovery biases the task toward identity collection before the body-level exception can apply. Keep personal work discovery and non-personal evidence-supported claim assessment as peer triggers.

## Testing

Use TDD:

1. Add a structural Skill contract test for the three predicates, resolved-question behavior, empty arrays, refusal, scope boundary, and prohibited invented outputs.
2. Run the focused test and observe RED because the terminal section is absent.
3. Add the smallest Skill section that satisfies the contract.
4. Run focused and full local suites, artifact validation, and compilation.
5. Synchronize the source Skill to the Codex installation and green controller copy; verify identical SHA-256 hashes.
6. Run a fresh external Codex algorithm probe. Require all four artifact pairs, `resume-audit.json`, and `workflow_complete` before running the five-repetition scenario gate.

## Non-Goals

- Do not change the artifact detector or controller state-transition logic; the green prompt builder may serialize the Skill's decision-ledger interface.
- Do not create synthetic target-role evidence.
- Do not loosen evidence, attribution, language, or path-validation rules.
- Do not send any material to Anthropic Claude without separate authorization.

## Progressive-Disclosure Attribution Route

Repeated `final-9g`, `final-9h`, and `final-9i` Codex probes loaded the correct deployed Skill but still selected the personal identity question before honoring an explicit non-personal ledger. The failure is therefore behavioral salience in the monolithic prompt, not cache, deployment, or controller-state corruption.

Keep only a three-branch attribution router in the main `SKILL.md`, before every other gate: non-personal plus identity-not-applicable continues without loading identity instructions; already-resolved identity continues without reopening scope; personal plus missing identity loads `references/identity-gate.md`. Move the exact identity question and complete personal first-turn protocol into that directly linked reference. The exact question must not remain anywhere in the main Skill body.

This refactor does not change attribution semantics. It narrows when personal-only instructions enter context so the terminal non-personal path can be selected from the resolved current-turn ledger.

## Complete Request Before Activation Wrappers

`final-9j-micro-01` no longer emitted the exact identity question, but still claimed that analysis kind, claim, identity, and scope were unspecified. Its response explicitly described the first line as an activation without a request, even though the complete request and ledger appeared later in the same prompt.

For green initial prompts, place the complete labelled original user request first, followed by the original-request authority protocol and resolved scenario context. Place the Skill activation sentence only after those user inputs, then add repository binding and chat-artifact instructions. Keep baseline prompts unchanged. This ordering prevents activation wrappers from framing the complete synthetic user request as missing while preserving all hidden-grading-data prohibitions.

TDD evidence: the new ordering assertions first failed in two focused tests because activation remained at offset zero. After the minimal reorder, four focused prompt and leakage tests passed. The next full controller run passed 31/32; its sole failure was an older record-format assertion that still required activation at offset zero. Updating that assertion made the affected test pass. Independent review then found the authority sentence still said the request was "below"; changing its test to "above" produced the expected RED before this constant was corrected.

## Bind the Skill Artifact Under Test

`final-9k-micro-01` received the complete reordered prompt but still read only the unrelated global `using-superpowers` Skill and falsely reported that the original-request body was absent. Forward-test prompts must follow the Skill-authoring contract by naming both the Skill and its exact artifact path. For each green run, bind the copied controller path `.claude/skills/analyzing-codebase-work-impact/SKILL.md` before the activation sentence and require that exact file plus its direct references to be read. Do not expose rubric or expected conclusions. Baseline prompts remain unchanged.

The binding contract was added test-first: the focused test failed because no exact path existed, then passed together with authority and hidden-grading-data tests after the minimal controller change. `final-9l-config-micro-01`, which tested `--ignore-user-config`, is an inconclusive transport failure: it emitted no assistant text and exhausted connection retries, so it is not acceptance evidence.

## Transport Multiline Codex Prompts Through Stdin

`final-9m-micro-01` still claimed that request text was missing and did not read the bound Skill. Codex CLI 0.145.0 `debug prompt-input` then rendered the actual model-visible input for the equivalent run: the user message contained only `Original user request:`. The persisted runner command retained the full Python string, but the Windows `.cmd` wrapper truncated the multiline command-line argument before it reached Codex. Earlier prompt and Skill diagnoses therefore observed a controller transport defect rather than the complete intended prompt.

For Codex initial and resumed turns, pass `-` in the CLI prompt position and send the complete current prompt through UTF-8 process stdin, which both `codex exec` and `codex exec resume` document as supported. Keep prompt arguments and `input=None` for Claude. Continue persisting the complete logical prompt in each turn record; the command record should contain `-`, not a duplicate multiline argument.

This transport fix is test-driven. Command-shape and process-input assertions failed against the argument-based implementation. After the minimal change, the initial command, resumed command, full initial stdin, full continuation stdin, and existing JSONL extraction tests passed 3/3.
