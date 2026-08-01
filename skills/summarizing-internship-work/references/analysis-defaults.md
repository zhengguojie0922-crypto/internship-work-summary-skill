# Analysis Defaults

## Limits

Apply these exact defaults while inspecting a repository:

| Limit | Value |
|---|---:|
| `max_candidate_files` | `max_candidate_files=200` |
| `max_hops_per_direction` | `max_hops_per_direction=3` |
| `max_alternative_chains` | `max_alternative_chains=5` |
| `max_text_file_bytes` | `max_text_file_bytes=1048576` |

Stop before exceeding a limit. During the allowed confirmation rounds, ask the user to narrow the repository, subproject, date or commit range, author set, or feature terms. When the limit remains reached after those rounds, analyze the bounded evidence and report the boundary, rather than asking again.

## Skip and Content Rules

Match a skipped directory only when its basename is a complete path segment. Never use substring matching. Use these exact default directory basenames:

- Dependencies and vendors: `.git`, `node_modules`, `vendor`, `.venv`, `venv`, `Pods`, `DerivedData`.
- Build output and caches: `dist`, `build`, `target`, `out`, `.next`, `.nuxt`, `.gradle`, `.idea`, `.cache`, `__pycache__`.

Use these exact generated filename rules:

- Suffix patterns: `*.min.js`, `*.min.css`, `*.map`.
- Complete names: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Podfile.lock`, `Cargo.lock`.

Classify a file as binary when either Git `numstat` reports `-` in an additions or deletions column, or the first `8192` bytes contain NUL. Do not decode or quote binary content. Classify text as oversized only when its byte size is greater than `max_text_file_bytes=1048576`. Record every skipped tracked path and one of `excluded_directory`, `generated`, `binary`, or `oversized`; do not read skipped content.

Let the user add or remove skip rules during scope confirmation. Apply approved changes only to the current analysis and state them in the final document.

## Source Citation Rules

Give every repository observation a source citation containing repository identity, revision or worktree state, relative path, line range when available, command, and excerpt or structured result. Cite Git claims with commit SHA and relevant file evidence. Cite user claims as user-provided evidence. Never cite a search hit as proof of runtime behavior or business effect.

## Safe Read-Only Commands

Treat `<safe-git>` below as a required process contract, not a literal executable. Never run a bare Git query against the analyzed repository.

Before every Git process, remove inherited `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_*`, `GIT_CONFIG_VALUE_*`, `GIT_CONFIG_SYSTEM`, `GIT_CONFIG_GLOBAL`, `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_COMMON_DIR`, `GIT_EXTERNAL_DIFF`, `GIT_DIFF_OPTS`, and `GIT_PAGER`. Then set these environment values:

```text
GIT_CONFIG_NOSYSTEM=1
GIT_CONFIG_GLOBAL=<empty-config-file-or-platform-null-device>
GIT_OPTIONAL_LOCKS=0
GIT_TERMINAL_PROMPT=0
GIT_PAGER=cat
PAGER=cat
```

Construct `<safe-git>` with this exact argument prefix, using a selected nonexistent hooks path outside the analyzed repository. Do not create a hooks directory:

```text
git --no-pager --no-optional-locks -c core.fsmonitor=false -c core.hooksPath=<selected-nonexistent-hooks-path> -c core.untrackedCache=false -c diff.external= -c diff.trustExitCode=false -c log.showSignature=false -c color.ui=false -C <repo>
```

Append only fixed read-only subcommands. Add `--no-ext-diff --no-textconv` to `log`, `show`, and `diff`; add `--no-textconv` to `blame` and `grep`. Never pass `--ext-diff`, `--textconv`, signature-display options, pager options, aliases, or a command assembled from repository content. Add path limits and explicit revisions whenever possible. Do not fetch, install tools, run repository hooks, execute project code, alter the index/worktree, or contact external systems.

## Boundary and Degradation Behavior

Stop a chain at an external service, generated boundary, submodule not in scope, unavailable revision, unsupported relation, or duplicate-only frontier. Record the boundary, last supported node, missing evidence, and possible next question. Treat shallow history, dirty state, missing Git, inaccessible files, unavailable search tools, and reached limits as degradation, not permission to guess.
