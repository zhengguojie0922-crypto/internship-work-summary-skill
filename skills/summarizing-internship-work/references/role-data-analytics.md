# Data Analytics Role Guide

## Role Boundary and Subdomains

- Treat data analytics work as source contracts, ingestion, staging, transformation, SQL models, semantic metrics, quality controls, scheduling, dashboards, and consumers.
- Set the evidence boundary from an identified source field through modeled data, metric definition, validated output, and a documented consumer decision.
- Separate SQL behavior from the metric meaning it implements, the quality evidence it has, and any business outcome attributed to it.
- Include source ownership, warehouse administration, dashboard design, experimentation, and stakeholder decisions only when direct evidence supports each role.
- Treat a dashboard consumer as evidence of an audience or access path, not proof that the dashboard changed a decision.
- Treat source contracts, schemas, and model definitions as declared structure rather than proof of fresh, complete, or accurate data.
- Treat a scheduled job as configured execution capability; use scheduler records to establish a particular successful or failed run.
- Keep sensitive rows, identifiers, credentials, private dashboard links, and restricted query text out of career material.
- Stop at an external source, opaque transformation, unobserved dashboard interaction, or unstated stakeholder decision unless evidence extends the chain.
- Route material evidence gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.

## Entry-Point Discovery

- Start from a business question, source contract, table, event schema, model, metric catalog entry, dashboard, or quality incident.
- Locate ingestion jobs, connector configuration, landing tables, staging models, and source-to-target ownership boundaries.
- Inspect SQL models, macros, materializations, dependencies, incremental filters, and warehouse query plans.
- Find semantic metric definitions, dimensions, metric grain, aggregation, filters, timezone, and attribution logic.
- Trace quality checks for schema, nulls, duplicates, uniqueness, completeness, freshness, reconciliation, and accepted exceptions.
- Locate schedules, orchestrator runs, backfills, retry policy, notifications, and run artifacts that show actual execution.
- Read data lineage, catalog descriptions, column documentation, ownership metadata, and downstream dashboard dependencies.
- Inspect dashboard queries, refresh settings, access scope, dashboard consumer descriptions, exports, and cited stakeholder context.
- Record source version, event time, processing time, model version, execution window, and last supported observed result.
- Preserve unavailable source samples, run records, experiment details, and stakeholder decisions as explicit unknowns.

## Typical Code Chains

- Source-to-model: source contract -> ingestion -> staging normalization -> SQL model -> quality checks -> catalog lineage -> dashboard boundary; contract failure -> quarantine or failed run evidence.
- Metric definition: modeled relation -> metric grain -> dimensions and filters -> semantic metric -> rendered value -> dashboard consumer boundary; ambiguity -> document and resolve definition before comparison.
- Incremental model: watermark or partition -> new and changed records -> merge or append logic -> reconciliation -> scheduler record; late-arriving data -> backfill or correction branch.
- Dimension history: source change -> slowly changing dimension policy -> versioned records -> as-of join -> metric output; unmatched history -> null or exception policy.
- Quality incident: failed schema, freshness, or uniqueness check -> affected model scope -> triage -> corrective transform or source fix -> rerun evidence; unresolved failure -> mark output unreliable.
- Dashboard path: curated model -> semantic query -> dashboard refresh -> access by dashboard consumer -> documented interpretation; stale refresh -> disclose data currency rather than infer current status.
- Experiment analysis: assignment data -> exposure and outcome definitions -> cohort filters -> statistical diagnostic -> reviewed interpretation; experiment bias -> limit or reject conclusion.
- Join path: fact table -> declared key and cardinality -> dimension join -> aggregation -> reconciliation; fan-out join -> stop result publication and correct grain.
- Backfill path: historical scope -> controlled replay -> partition validation -> lineage update -> consumer notice; partial backfill -> label affected periods and avoid comparison claims.
- These chains establish behavior and evidence branches, not automatic proof of revenue, decision quality, freshness, or accuracy.

## Technical Decision Matrix

| Decision | Evidence to inspect | Supported claim | Prohibited inference |
| --- | --- | --- | --- |
| metric grain | primary key, aggregation, semantic definition | unit of analysis and aggregation rule | correct business meaning by itself |
| Join cardinality | keys, uniqueness tests, query result samples | expected one-to-one, one-to-many, or many-to-many behavior | no fan-out without validation |
| Event time versus processing time | event schema, ingestion timestamps, timezone policy | selected temporal interpretation | real-time freshness or ordering |
| late-arriving data | watermark, correction window, backfill records | handling policy and bounded delay | complete historical accuracy |
| slowly changing dimension | version columns, effective dates, as-of joins | documented history strategy | all historical attributes are correct |
| Incremental strategy | partition logic, merge key, full-refresh comparison | modeled update behavior | no missed or duplicated rows |
| Null and duplicate policy | tests, source contract, exception rules | specified quality treatment | source completeness or validity |
| experiment bias | assignment, exposure, selection, sample diagnostics | analyzed bias risks and limits | causal business outcome |

## Failure Modes and Risks

- Fan-out joins can duplicate facts and inflate aggregates when key cardinality is assumed rather than tested.
- Data leakage can let a label, post-outcome field, or future observation enter a metric or experiment analysis.
- Survivorship or selection bias can omit users, entities, failures, or nonparticipants and distort comparisons.
- Timezone drift can move events across reporting boundaries when source, warehouse, metric, and dashboard use different conventions.
- Stale data can show a previous scheduler result or delayed source without a visible freshness boundary.
- Schema drift can remove, rename, retype, or reinterpret fields while leaving downstream SQL syntactically valid.
- Misleading aggregation can hide distribution, denominator, cohort composition, missing values, or changes in metric grain.
- Late-arriving data can revise previously published periods when correction windows and consumer expectations are undefined.
- Slowly changing dimension errors can join facts to the wrong historical attribute or duplicate version records.
- Dashboard filters, extracts, or permissions can show a limited view that users mistake for the governed metric.

## Validation Evidence

- Schema and contract tests can prove expected columns, types, accepted values, and compatibility rules at the tested boundary.
- Reconciliation can compare counts, sums, hashes, or sampled records across sources when scope, time window, and transformation differences are stated.
- Uniqueness and completeness checks should name the key, null policy, accepted exceptions, and result for the recorded execution.
- Freshness checks require source, timestamp field, threshold, scheduler context, and observed delay; configuration alone is insufficient.
- Data lineage can establish modeled dependencies and ownership metadata, not the correctness of every upstream transformation.
- Query-plan checks can reveal execution strategy and cost risks for a specified warehouse, data volume, and query version.
- Peer review can support reviewed SQL or metric definitions, but it does not replace execution or semantic validation evidence.
- Experiment diagnostics should show assignment integrity, exposure, sample size, missingness, balance, and applicable experiment bias limits.
- Backfill validation should compare affected partitions and publication status without claiming all downstream consumers refreshed.
- State whether the proof is static SQL, controlled query result, scheduler run, warehouse record, experiment artifact, or confirmed stakeholder evidence.

## Impact and Metrics Evidence

- Cite model freshness from scheduler or warehouse records that define timestamp, threshold, affected model, and time window.
- Cite data quality counts or rates from named test results with denominator, exception policy, and execution scope.
- Cite query performance or cost only from query history, plan, billing, or benchmark records with comparable workload and period.
- Cite dashboard usage only from access, analytics, or stakeholder evidence and distinguish dashboard consumer access from interpretation or action.
- Cite revenue, conversion, retention, or operational outcomes only from confirmed business evidence with metric definition and attribution boundary.
- Cite experiment results only with assignment method, exposure definition, population, statistical treatment, uncertainty, and experiment bias assessment.
- Cite catalog or lineage coverage only from a scoped inventory and avoid converting documentation presence into correctness claims.
- Link a SQL or semantic change to a metric shift only when timing, affected population, baseline, and causal limitations are documented.
- Use qualitative wording for traceability, governed definitions, or validation controls when only implementation evidence exists.
- Keep unsupported accuracy, freshness, decision-quality, and business-impact metrics out of resume wording and label them as needing user input.

## Resume Mapping

- Map a source-to-model chain to building a traceable transformation with named source contract, staging, model, and validation boundaries.
- Map metric grain and semantic definition evidence to defining a reviewable metric rather than claiming its business interpretation was adopted.
- Map incremental model and late-arriving data handling to maintaining a documented update and correction path with its observed scope.
- Map slowly changing dimension logic to preserving historical attributes when effective dates, join behavior, and validation are traceable.
- Map quality tests and reconciliation to detecting or preventing a specific data issue only when the recorded result supports that scope.
- Map lineage and catalog evidence to improving discoverability or traceability without claiming comprehensive governance.
- Map dashboard work to enabling a dashboard consumer to access a defined view, not to a decision or revenue outcome without stakeholder evidence.
- Map experiment analysis to analyzing a stated hypothesis and bias limitations without overstating causal certainty.
- Prefer verbs such as modeled, defined, reconciled, validated, documented, traced, analyzed, or backfilled when source evidence supports them.
- Attach a source note for every metric, adoption statement, decision claim, quality rate, or business outcome in a resume bullet.

## Interview Question Tree

- Broken metric scenario: explain metric grain, denominator, joins, filters, semantic definition, reconciliation evidence, and correction boundary.
- Join scenario: explain expected cardinality, fan-out risk, uniqueness evidence, aggregation effect, and the rejected or selected alternative.
- Backfill scenario: explain late-arriving data, affected partitions, incremental strategy, validation, lineage update, and consumer communication limit.
- History scenario: explain slowly changing dimension policy, effective dates, as-of join, unmatched records, and validation evidence.
- Quality incident scenario: explain detection signal, affected scope, triage, correction, rerun, and whether consumers were notified.
- Experiment disagreement scenario: explain assignment, exposure, cohort selection, experiment bias, diagnostics, uncertainty, and why a conclusion may remain limited.
- Executive-dashboard scenario: explain source-to-model lineage, metric definition, refresh boundary, dashboard consumer, and confirmed decision evidence if any.
- Performance scenario: explain query-plan evidence, warehouse context, cost or duration measurement, and trade-offs without generalizing beyond the workload.
- Metrics scenario: name the catalog, scheduler, warehouse, experiment, or stakeholder source, period, population, denominator, and attribution limit.
- End each answer at the last supported node when a query, dashboard, or metric lacks runtime, consumer, or business-decision evidence.

## Overclaim Guardrails

- SQL presence does not prove that a model ran, a dashboard refreshed, data was fresh, or results were accurate.
- A source contract or schema test does not prove all source records are complete, timely, semantically correct, or historically stable.
- A metric definition does not prove that its metric grain, denominator, or business interpretation matches every consumer's use.
- A quality check does not prove no data quality issue exists outside its keys, thresholds, execution window, or accepted exceptions.
- Lineage does not prove upstream correctness, downstream dashboard refresh, or a stakeholder's decision quality.
- A dashboard consumer record does not prove the consumer viewed, understood, trusted, or acted on the dashboard.
- An experiment query does not prove causal impact without valid assignment, diagnostics, uncertainty, and experiment bias analysis.
- Never infer revenue, adoption, decision quality, freshness, accuracy, or cost savings from query presence alone.
- Redact sensitive data, credentials, customer identifiers, private dashboard links, and restricted source details in all evidence summaries.
- Route unresolved material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
