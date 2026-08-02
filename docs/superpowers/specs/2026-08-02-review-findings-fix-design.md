# Review Findings Fix Design

## Goal

Resolve the remaining evidence-selection, workflow, output-size, overwrite, naming, and release-version issues without restoring retired test fixtures or runtime intermediate files.

## Attribution Routes

- A named feature requested as the user's resume, internship summary, or personal output is treated as fully implemented by the user. This is user-provided evidence. Git authorship is not checked unless the user explicitly requests Git verification.
- A named feature requested only as an implementation analysis does not imply personal ownership.
- A request without a named feature uses confirmed Git identities. Only commits matching a confirmed full name or full email, including `Co-authored-by` identities, become personal candidate work.
- A mixed request traces the feature first and uses Git only when attribution verification was explicitly requested.

## Git Evidence Collection

The Git-discovery route runs the bundled collector twice and consumes stdout in memory: `contributors` first, then `collect` after identity confirmation. It never writes an intermediate JSON file. Contributor aliases are candidates for confirmation, not automatically merged identities.

Author matching uses case-insensitive, trimmed equality against complete names and complete email addresses. It includes the primary author and parsed co-authors but excludes substring matching. Date, path, merge, and scan-limit filters are passed to `git log`; `max_commits + 1` records are requested so the collector can report a deterministic truncation boundary while limiting history work.

## Final Document

The only runtime artifact remains `career-output/实习产出与面试准备.md`. By default, select the strongest three outputs; expand to at most five only when the user explicitly requests a comprehensive summary. Each output gets about 20 concise evidence-backed core questions with reference answers and follow-ups, plus a separate set of 3-5 scenario questions. Evidence safety overrides quotas, so insufficient evidence produces fewer questions rather than fabricated content.

If the final document already exists, update matching outputs and preserve unrelated verified material. Replace the entire document only when the user explicitly requests a rebuild.

## Release Surface

Prepare the repository as version `1.1.0`, update active documentation, and remove the retired product name from the complete installable Skill directory. Do not create tags, releases, commits, pushes, or pull requests in this task.

## Verification

Use test-first regression coverage for exact author matching, co-author selection, bounded Git history, Skill routing, output shape, overwrite behavior, and release metadata. Finish with the complete unittest suite, compileall, `git diff --check`, and a clean review of the uncommitted diff.
