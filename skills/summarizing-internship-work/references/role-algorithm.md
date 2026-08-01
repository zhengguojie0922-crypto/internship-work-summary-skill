# Algorithm Role Guide

## Role Boundary and Subdomains

- Treat algorithm work as problem formulation, dataset and label design, preprocessing, feature pipelines, model or optimizer logic, training, evaluation, experimentation, inference integration, and monitoring.
- Set the evidence boundary from a stated decision problem through data and label provenance, method behavior, validated results, and observed serving or monitoring artifacts.
- Separate data collection and label definition from model training; a dataset file alone does not establish a training contribution or label quality.
- Separate training and evaluation evidence; a checkpoint or training configuration does not establish offline evaluation quality.
- Separate offline evaluation from online product effects; a benchmark is not evidence that users received or benefited from a model.
- Separate inference behavior from monitoring evidence; serving code establishes an integration path, while logs or alerts establish a recorded runtime observation.
- Include rule systems, ranking or retrieval, optimization, classical machine learning, deep learning, and feature engineering only when direct artifacts show their role.
- Treat API wiring, CRUD, feature flags, and downstream model consumption as adjacent integration work unless the contribution changes algorithm behavior or serving constraints.
- Attribute dataset ownership, annotation operations, model selection, experiment decisions, infrastructure ownership, and rollout approval independently.
- Route material evidence gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.

## Entry-Point Discovery

- Start from a product hypothesis, problem statement, training entry point, notebook, pipeline definition, model registry record, experiment artifact, or monitored incident.
- Locate target and label creation logic, source snapshots, joins, time boundaries, exclusion rules, annotation guidance, and label leakage controls.
- Inspect preprocessing, feature definitions, feature freshness, transformations, train/serve feature parity, and feature ownership boundaries.
- Find model architecture, loss function, objective, optimizer, hyperparameters, random seed, checkpoint policy, and dependency versions.
- Trace training orchestration, resource configuration, data split strategy, retries, artifact storage, and the code that selects a produced model.
- Locate offline evaluation reports, a baseline, metric definitions, cross-validation outputs, confusion or ranking diagnostics, and slice/error analysis.
- Read experiment configuration for population, assignment, exposure, holdout, guardrails, stopping policy, and any cited online experiment result.
- Inspect inference adapters, request validation, feature lookup, batching, model version resolution, timeout, fallback, and inference budget controls.
- Find monitoring for prediction distributions, feature health, model drift, latency, resource use, errors, alerts, and documented incident response.
- Preserve missing data lineage, label audits, training logs, evaluation artifacts, experiment records, and production observations as explicit unknowns.

## Typical Code Chains

- Supervised training: source snapshot -> target or label definition -> preprocessing -> feature pipeline -> split -> training -> checkpoint -> offline evaluation -> registry boundary.
- Ranking or retrieval: query and candidate data -> relevance labels -> candidate generation -> scorer or ranker -> ranking metric -> error analysis -> serving integration boundary.
- Rule or optimization method: constraints and objective -> rule set or solver configuration -> candidate solution -> feasibility checks -> objective comparison -> selected action boundary.
- Feature pipeline: raw event or entity -> validation -> transformation -> feature store or materialization -> train lookup and serve lookup -> parity check; mismatch -> block or fall back.
- Offline evaluation: fixed evaluation data -> baseline comparison -> candidate predictions -> metric calculation -> slice/error analysis -> report artifact; unsupported comparison -> limit the claim.
- Online experiment: eligible population -> assignment -> exposure logging -> outcome capture -> guardrail and effect analysis -> decision record; imbalance or contamination -> reject or qualify the result.
- Inference serving: request -> input validation -> feature retrieval -> versioned model -> prediction -> threshold or policy -> response -> latency and error telemetry.
- Inference failure branch: malformed input, unavailable feature, timeout, or resource breach -> documented safe fallback or explicit failure -> event record -> incident boundary.
- Monitoring path: production input and prediction telemetry -> quality or drift checks -> alert threshold -> investigation -> rollback, retraining, or accepted-risk record.
- These chains show algorithm behavior and evidence branches, not proof of novelty, product lift, dataset scale, or sole ownership.

## Technical Decision Matrix

- Target or label definition: inspect outcome timing, annotation policy, exclusions, and provenance; state the supported target rather than assuming labels are correct.
- Split strategy: inspect temporal, group, random, or cross-validation split code and justify isolation from future information or correlated entities.
- baseline: compare the candidate against the named heuristic, prior model, or simple method on the same scoped data and metric.
- Metric choice: connect the metric to the stated objective, class distribution, ranking position, calibration need, error cost, and evaluation population.
- Threshold or policy: inspect the decision threshold, abstention rule, and error trade-off; do not equate a score with a product decision without integration evidence.
- Model complexity: compare capacity, explainability, training cost, latency, and available validation evidence instead of treating a larger model as an improvement.
- Robustness: inspect perturbation tests, rare slices, missing inputs, adversarial or edge conditions, and the documented behavior when assumptions fail.
- Reproducibility: retain data version, code revision, seed, environment, dependency versions, configuration, and the recorded rerun scope.
- Online experiment: select assignment, guardrails, duration, stopping rule, and interpretation boundaries before attributing an observed product effect.
- inference budget: define latency, memory, compute, batch size, timeout, availability, and fallback constraints from serving requirements or measured artifacts.

## Failure Modes and Risks

- label leakage can use a post-outcome field, target proxy, future observation, or preprocessing result that makes validation unrealistically favorable.
- Train/serve skew can arise when online features, defaults, transformations, versions, or schemas differ from the training path.
- Class imbalance can hide harmful minority-class behavior behind aggregate accuracy or a poorly chosen evaluation metric.
- Overfitting can select a method that adapts to training, tuning, or repeated evaluation data without generalizing to the intended population.
- Biased evaluation can result from selection, temporal contamination, an unrepresentative holdout, missing outcomes, or invalid experiment assignment.
- Irreproducibility can follow from mutable data, absent seeds, undeclared environments, nondeterministic operations, or incomplete artifact capture.
- model drift can change feature distributions, labels, user behavior, or outcome relationships after deployment and invalidate an old evaluation boundary.
- Latency or resource breaches can exhaust the inference budget, queue requests, increase errors, or force an unreviewed degradation path.
- Unsafe fallback can apply a stale model, unvalidated heuristic, default prediction, or silent retry when input or dependency failure requires a visible safety policy.
- A successful request, green pipeline, or model registry entry does not prove prediction quality, fairness, product impact, or production reliability.

## Validation Evidence

- Data checks should identify schema, range, missingness, duplicates, label distribution, temporal boundary, provenance, and recorded results for the evaluated snapshot.
- Baseline comparison should hold data, split, metric, threshold, and evaluation protocol constant so the observed difference has a stated scope.
- Ablation should remove or vary a feature, component, rule, or objective and report the controlled comparison without treating correlation as sole causation.
- Cross-validation should record fold construction, grouping or temporal treatment, tuning separation, metric aggregation, and variability.
- Slice and error analysis should name the population, denominator, error type, threshold, and limitations instead of claiming fair or universal performance.
- Reproducibility evidence should connect a code revision, data version, environment, seed, configuration, and rerun outcome at the recorded boundary.
- Load tests should measure inference latency, throughput, error rate, memory, or compute for the named model version, hardware, payload, and concurrency.
- An online experiment requires assignment, exposure, outcome, guardrail, statistical treatment, uncertainty, and decision evidence before stating a product effect.
- Monitoring evidence should name the signal, baseline period, alert threshold, model version, response action, and whether a drift event was actually observed.
- State whether proof is static code, dataset artifact, controlled training run, offline evaluation, load test, online experiment, or production monitoring record.

## Impact and Metrics Evidence

- Cite offline quality only from named evaluation artifacts that define data version, split, metric, population, threshold, comparison method, and uncertainty where available.
- Cite online product effect only from a cited online experiment or decision record with assignment, exposure, outcome, population, attribution limit, and guardrail status.
- Cite latency and throughput only from load tests, serving telemetry, or benchmark records with model version, hardware, payload, concurrency, and measurement window.
- Cite memory, accelerator, storage, or compute cost only from resource records that identify workload, environment, aggregation, and comparison scope.
- Keep offline quality separate from online product effect, because an improved validation metric is not a demonstrated user or business outcome.
- Keep serving latency and resource cost separate from model quality, because a faster or cheaper request does not establish predictive benefit.
- Cite calibration, recall, precision, ranking, loss, or optimization objective values with their denominator, threshold, dataset, and intended interpretation.
- Cite drift rates, alert counts, rollback counts, or incident duration only from monitoring records that name the signal, period, model version, and response boundary.
- Use qualitative wording for implemented evaluation, reproducibility, or safety controls when direct outcome or metric artifacts are unavailable.
- Keep unsupported novelty, lift, accuracy, dataset size, fairness, availability, cost saving, and business-impact claims out of resume wording and label them as needing user input.

## Resume Mapping

- Map a traceable target and label path to formalizing an algorithm problem, while stating the available provenance and leakage boundary.
- Map preprocessing or feature work to implementing a reproducible pipeline only when train and serve behavior, artifacts, or validation support that scope.
- Map model or optimizer changes to evaluating a candidate against a baseline, not to inventing a novel method or claiming sole model ownership.
- Map offline evaluation to measuring a named metric on a defined split and population without presenting it as an online product result.
- Map ranking, retrieval, rule, or optimization work to the objective, constraints, and tested behavior actually evidenced in the repository.
- Map inference integration to meeting a documented interface, safety, or inference budget boundary without claiming platform ownership from API wiring alone.
- Map monitoring changes to instrumenting or investigating a signal, and distinguish configuration from a recorded model drift or incident response.
- Use verbs such as formulated, labeled, transformed, trained, evaluated, compared, analyzed, integrated, monitored, or reproduced when direct evidence supports them.
- Attach a source note for every model metric, experiment conclusion, latency statement, resource claim, or business outcome in a resume bullet.
- Stop at the last supported node when a feature pipeline, model, experiment, or serving path lacks evaluation, runtime, or outcome evidence.

## Interview Question Tree

- Metric disagreement scenario: explain target definition, split, baseline, metric semantics, threshold, slice evidence, uncertainty, and why results may not be comparable.
- label leakage scenario: explain when each field becomes available, how the leakage path was detected, its effect on evaluation, the corrected split or pipeline, and the rerun evidence.
- Drift scenario: explain the monitored signal, baseline period, model drift hypothesis, affected population, alert threshold, investigation, and supported mitigation or rollback.
- Latency regression scenario: explain model version, inference budget, payload and concurrency, measured latency or resource evidence, bottleneck, and selected trade-off.
- Unfair slice scenario: explain population and denominator, metric disparity, label or sampling limitations, threshold effects, mitigation options, and the boundary on fairness claims.
- Rollback scenario: explain guardrail breach, signal, safe fallback, model or configuration version, decision authority, event record, and recovery validation.
- Online experiment scenario: explain hypothesis, assignment, exposure, outcome, guardrails, uncertainty, contamination checks, and why a result may remain inconclusive.
- Reproducibility scenario: explain data version, code revision, seed, environment, configuration, artifact retention, rerun result, and unresolved nondeterminism.
- Method selection scenario: compare a baseline and candidate using the same evaluation boundary, complexity, robustness, interpretability, serving cost, and rejected alternatives.
- End every answer at the last supported node when offline evaluation, online experiment, inference telemetry, or monitoring records are missing.

## Overclaim Guardrails

- A dataset, label file, feature table, or annotation guide does not prove label correctness, completeness, representativeness, or ownership of collection operations.
- Training code, a checkpoint, or a registry record does not prove that a model trained successfully, generalized, or was selected for production.
- An offline evaluation result does not prove online product effect, user value, business lift, safety, fairness, or durability under model drift.
- API wiring, CRUD, and downstream model consumption do not establish algorithm ownership unless direct artifacts show a change to the method, data, evaluation, or serving constraints.
- A serving endpoint does not prove measured latency, availability, resource efficiency, production traffic, or successful fallback behavior.
- A monitoring configuration does not prove a model drift event, alert response, rollback, or sustained production quality without observed records.
- A single metric does not prove broad performance, calibration, fairness, causal benefit, or robustness outside its data, split, threshold, and population.
- Never invent novelty, lift, accuracy, dataset scale, experiment results, production adoption, or sole ownership from repository structure or static code.
- Redact personal data, labels, credentials, model artifacts, private experiment details, proprietary features, and restricted telemetry in career material.
- Route unresolved material gaps through the main consolidated confirmation process; this guide does not add confirmation rounds or request Git identity for a named-feature route.
