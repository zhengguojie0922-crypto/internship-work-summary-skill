# Internship Work Summary Rename Design

## Goal

Rename the project and installable Skill so the primary identity communicates its current purpose: summarizing evidence-backed internship work from a local codebase and turning that summary into resume and interview preparation material.

This is a naming and packaging change. The two analysis routes, evidence rules, supported roles, confirmation limits, and single-document runtime behavior remain unchanged.

## Naming Decision

Use the following canonical names:

- Project display name: `Internship Work Summary Skill`
- Skill display name: `Internship Work Summary`
- Skill identifier: `summarizing-internship-work`
- Installable directory: `skills/summarizing-internship-work`
- Recommended GitHub repository name: `internship-work-summary-skill`
- Release version: `0.3.0`

The old `Codebase Work Impact` and `analyzing-codebase-work-impact` names are retired from active product, installation, and invocation surfaces. No compatibility Skill or duplicate directory remains because two overlapping Skills would create ambiguous triggering and duplicate maintenance.

## Preserved Behavior

The renamed Skill keeps the current behavior contract:

- A named feature request traces the complete code path without filtering by commit author.
- A general internship-output request uses the confirmed Git identity to discover personal candidate work, then traces the corresponding implementation.
- The target role is selected from frontend, backend, client, testing, DevOps, data analytics, and algorithm work.
- Repository inspection remains read-only and evidence-backed.
- A normal run creates only `career-output/实习产出与面试准备.md` and no intermediate documents.
- The final document contains internship outputs, three resume variants, interview introductions, approximately 20 core questions per major output, follow-ups, and scenario questions.

## Repository Changes

Move the installable Skill directory with Git-aware history preservation and update all active references to its new identifier and path. Active surfaces include:

- `README.md`
- `CONTRIBUTING.md`
- `skills/summarizing-internship-work/SKILL.md`
- `skills/summarizing-internship-work/agents/openai.yaml`
- `skills/summarizing-internship-work/VERSION`
- packaging, contract, and behavior tests
- current workflow or configuration files that resolve the installable Skill path

Update prompts, installation commands, explicit invocation examples, display metadata, and expected paths together. Historical specifications and implementation plans retain the names used by the versions they documented; they are historical records rather than active installation guidance.

## Migration Experience

Document the rename as a `0.3.0` breaking change. Existing users remove the installed `analyzing-codebase-work-impact` directory or uninstall that Skill, then install and invoke `summarizing-internship-work`. The README should keep this migration note concise and place it after the normal installation and usage instructions.

Do not install, delete, or modify a user's globally installed Skill as part of repository development or tests.

## GitHub Rename

After the code change is merged, rename the GitHub repository from `codebase-work-impact-skill` to `internship-work-summary-skill` in repository settings. Update the local `origin` URL afterward even though GitHub normally redirects the previous repository URL.

Repository settings cannot be completed by the code change itself. Until the website rename occurs, documentation that uses the new repository URL may briefly depend on GitHub-side coordination.

## Verification

Verification must confirm:

- the installable Skill validates under the new identifier and directory;
- deterministic unit and packaging tests pass;
- active README, contributing, workflow, Skill metadata, and tests contain no stale old identifier or old repository URL;
- historical plans and specifications are excluded from the stale-reference assertion;
- the runtime output path and single-document contract have not changed;
- `git diff --check` passes.

## Out of Scope

- Changing feature tracing, Git discovery, role-specific analysis, resume writing, or interview generation behavior
- Keeping an alias Skill for the old identifier
- Rewriting historical commits or historical design documents
- Automatically modifying GitHub repository settings or users' global Skill installations

## Acceptance Criteria

The rename is complete when a new user can install `summarizing-internship-work`, invoke `$summarizing-internship-work`, and receive the same evidence-backed `career-output/实习产出与面试准备.md` workflow without encountering an active instruction or test that requires the retired identifier.
