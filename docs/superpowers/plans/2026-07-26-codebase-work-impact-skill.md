# Codebase Work Impact Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish an installable `analyzing-codebase-work-impact` Agent Skill that collects traceable Git evidence and guides evidence-backed career material generation.

**Architecture:** A portable Skill directory contains concise orchestration instructions, deterministic Python standard-library collectors and validators, JSON Schemas, and role/output references. Repository-level tests build deterministic temporary Git repositories and validate scripts, schemas, static Skill contracts, packaging documentation, and cross-platform CI configuration.

**Tech Stack:** Python 3.10+ standard library, Git 2.30+, JSON Schema Draft 2020-12 documents, `unittest`, GitHub Actions, Markdown, YAML.

## Global Constraints

- Repository name: `codebase-work-impact-skill`; installable unit: `skills/analyzing-codebase-work-impact`.
- Skill name: `analyzing-codebase-work-impact`; version source: `VERSION` containing `0.1.0`.
- `SKILL.md` frontmatter contains only `name` and `description`, uses imperative instructions, links every reference directly, and remains below 500 lines.
- Runtime floor is Python 3.10 and Git 2.30; Python scripts use only the standard library.
- Scripts never execute target-repository code, hooks, builds, tests, installers, generators, network calls, pulls, credential inspection, secret stores, or environment-variable values.
- JSON goes to stdout and diagnostics to stderr; output files are atomically replaced and their parent directories must already exist.
- Exit codes are exactly 0 success, 2 argument error, 3 Git unavailable/not a repository, 4 Git query failure, 5 I/O or encoding failure, and 6 schema validation failure.
- Machine artifacts use `schema_version: "1.0"`; repository paths use relative POSIX separators.
- Default output language is Chinese, with English and bilingual output supported; English career content is rewritten for the target market rather than mechanically translated.
- License is MIT with `Copyright (c) 2026 codebase-work-impact-skill contributors`.
- Model forward-test results must not be fabricated; unavailable runs are explicitly reported as incomplete.

---

### Task 1: Schemas, Fixture Manifests, and Scenario RED Baseline

**Files:** Create the six schema files under `skills/analyzing-codebase-work-impact/references/schemas/`, `tests/fixture_builder.py`, three fixture manifests, seven scenario files, and schema/static test modules.

**Interfaces:** Produces Draft 2020-12 schemas selected by `artifact_type`, deterministic `build_fixture(manifest_path, destination)` output, and test inputs used by all later tasks.

- [ ] Write schemas, manifests, scenarios, and failing tests before Skill behavioral instructions or production scripts.
- [ ] Run `python -m unittest discover -s tests -v`; verify failures identify missing collector, validator, and Skill contracts.
- [ ] Record that fresh-model RED runs are unavailable rather than creating synthetic baseline records.

### Task 2: Git Evidence Collector

**Files:** Create `skills/analyzing-codebase-work-impact/scripts/collect_git_evidence.py`; extend `tests/test_collect_git_evidence.py`.

**Interfaces:** Implements `contributors` and `collect` commands exactly as specified; emits deterministic evidence-report JSON except `generated_at`, reads `VERSION`, and applies sensitivity/redaction rules.

- [ ] Add one focused failing test for each command contract, filtering rule, Git edge case, output rule, stable ordering requirement, and secret-redaction requirement.
- [ ] Run the focused test after each addition and confirm the expected behavioral failure.
- [ ] Add minimal standard-library implementation and rerun the focused test to green.
- [ ] Run the complete collector test module and retain stdout/stderr separation.

### Task 3: Artifact Validator

**Files:** Create `skills/analyzing-codebase-work-impact/scripts/validate_artifact.py`; extend `tests/test_validate_artifact.py`.

**Interfaces:** Selects bundled schema from top-level `artifact_type`, supports a constrained Draft 2020-12 keyword subset for explicit schemas, prints a JSON summary unless quiet, and returns exit code 6 for validation failures.

- [ ] Add failing tests for valid and invalid examples of all six bundled schemas, explicit schemas, quiet mode, and I/O/argument failures.
- [ ] Implement only the validator features exercised by bundled schemas and documented explicit-schema keywords.
- [ ] Run validator tests, then validate every checked-in fixture and scenario through the CLI.

### Task 4: Skill Workflow and Domain References

**Files:** Create `SKILL.md`, `VERSION`, `agents/openai.yaml`, analysis/evidence/role/achievement/resume/interview references, and static behavior tests.

**Interfaces:** Guides scope → evidence → facts → career with strict and fast modes, resumable session semantics, feature-chain tracing, attribution, privacy, role classification, and auditable career outputs.

- [ ] Use the scenario/static RED evidence from Task 1 to write the minimum behavioral guidance.
- [ ] Link every reference directly from `SKILL.md`; keep detailed role and output material in references.
- [ ] Run static tests and `quick_validate.py`; fix only observed contract failures.
- [ ] Mark model-based GREEN validation incomplete when fresh Codex and Claude sessions are unavailable.

### Task 5: Publishing Surface and Full Verification

**Files:** Create `README.md`, `LICENSE`, `CONTRIBUTING.md`, `.github/workflows/test.yml`, `docs/artifact-schemas.md`, and `docs/examples/` artifacts.

**Interfaces:** Documents POSIX/PowerShell installation, upgrade, uninstall, explicit invocation, supported runtime status, schema usage, and safe contribution workflow.

- [ ] Add failing packaging/static assertions for required install targets, commands, license text, CI matrix, and forward-test status wording.
- [ ] Add the minimum publishing files and examples to satisfy those assertions.
- [ ] Run `python -m unittest discover -s tests -v` and the Skill creator `quick_validate.py`.
- [ ] Re-read the design specification section by section, verify every acceptance criterion, and report any unavailable forward-test gate precisely.

