# Clean v1.0 Republishing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the current Internship Work Summary Skill as a new public GitHub repository with one root commit, a `v1.0.0` tag and release, and no inherited contributor history.

**Architecture:** First make and verify the stable-version content changes on the source release branch. Export only tracked files into an ignored `.tmp-v1-clean` directory and initialize a separate Git repository there, preserving the current repository as a rollback source. Rename the current GitHub repository to a legacy name, create and validate the new repository, then place permanent legacy deletion behind a final destructive-action confirmation.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3.10+ standard-library `unittest`, Git 2.30+, GitHub Actions, GitHub web UI

## Global Constraints

- GitHub owner: `zhengguojie0922-crypto`.
- New repository: `internship-work-summary-skill`.
- Temporary legacy repository: `internship-work-summary-skill-legacy`.
- Skill identifier: `summarizing-internship-work`.
- Project display name: `Internship Work Summary Skill`.
- Skill display name: `Internship Work Summary`.
- Version file value: `1.0.0`.
- Git tag: `v1.0.0`.
- Root commit subject: `Initial release of Internship Work Summary Skill v1.0.0`.
- Commit author and committer: `zhengguojie0922-crypto <zhengguojie0922@gmail.com>`.
- Export tracked files only; never copy or rewrite the source `.git` directory.
- Preserve both request routes, seven role guides, read-only analysis, evidence rules, and the sole runtime output `career-output/实习产出与面试准备.md`.
- Do not use GitHub Fork, Importer, a mirror push, or preserved source commit objects for the new repository.
- Do not permanently delete the legacy repository until every remote verification gate passes and the user confirms the exact deletion at action time.

---

### Task 1: Prepare stable v1.0 product content

**Files:**
- Modify: `README.md`
- Modify: `skills/summarizing-internship-work/VERSION`
- Modify: `tests/test_packaging.py`

**Interfaces:**
- Consumes: the merged `0.3.0` package and its current publishing tests.
- Produces: verified `1.0.0` tracked content with no active pre-1.0 migration guidance.

- [ ] **Step 1: Change publishing tests to require the stable release**

Rename `test_readme_uses_the_new_installation_and_invocation_identity` to `test_readme_uses_the_stable_release_identity` and replace its body with:

```python
def test_readme_uses_the_stable_release_identity(self) -> None:
    text = read_utf8(README)
    self.assertIn(NEW_REPOSITORY, text)
    self.assertIn("--skill summarizing-internship-work", text)
    self.assertIn("$summarizing-internship-work", text)
    self.assertIn("1.0.0", text)
    self.assertNotIn("## 从 0.2.x 升级", text)
    for phrase in OLD_IDENTITY_PHRASES:
        self.assertNotIn(phrase, text)
```

Include `README` in `test_nonhistorical_product_files_do_not_use_the_retired_identity`:

```python
active_files = (
    README,
    CONTRIBUTING,
    LICENSE,
    WORKFLOW,
    SKILL_DIR / "SKILL.md",
    METADATA,
    VERSION,
)
```

Change the release assertions in `test_metadata_and_version_are_aligned_with_the_breaking_release`:

```python
self.assertEqual("1.0.0", read_utf8(VERSION).strip())
self.assertIn("1.0.0", read_utf8(README))
```

- [ ] **Step 2: Run focused tests and record RED**

Run:

```text
python -m unittest tests.test_packaging.PublishingSurfaceTests.test_readme_uses_the_stable_release_identity tests.test_packaging.PublishingSurfaceTests.test_nonhistorical_product_files_do_not_use_the_retired_identity tests.test_packaging.PublishingSurfaceTests.test_metadata_and_version_are_aligned_with_the_breaking_release -v
```

Expected: FAIL because README still contains the `0.2.x` migration section and `VERSION` still contains `0.3.0`.

- [ ] **Step 3: Update the stable release content**

Replace the README opening paragraph with:

```markdown
`summarizing-internship-work` 从本地代码库和 Git 证据总结可核验的实习产出，并生成简历和面试准备文档。`1.0.0` 是首个稳定版本，采用 MIT 许可证。
```

Remove the complete section beginning with `## 从 0.2.x 升级` and ending immediately before `## 详细功能`.

Set `skills/summarizing-internship-work/VERSION` to exactly:

```text
1.0.0
```

- [ ] **Step 4: Run focused and complete verification**

Run:

```text
python -m unittest tests.test_packaging -v
python -m unittest tests.test_skill_contract -v
python -m unittest tests.test_collect_git_evidence -v
python -m unittest discover -s tests -v
python -m compileall -q skills tests
git diff --check
```

Expected: all 43 tests PASS; `compileall` and `git diff --check` exit 0 with no output.

- [ ] **Step 5: Commit the stable product content**

```text
git add README.md skills/summarizing-internship-work/VERSION tests/test_packaging.py
git commit -m "Prepare Internship Work Summary v1.0.0"
```

### Task 2: Build the isolated one-commit repository

**Files:**
- Create ignored directory: `.tmp-v1-clean/`
- Create ignored archive: `.tmp-v1-clean-snapshot.tar`
- Do not modify tracked source files

**Interfaces:**
- Consumes: the verified tracked snapshot at the Task 1 commit.
- Produces: a separate Git repository at `.tmp-v1-clean` with exactly one `main` commit and the annotated `v1.0.0` tag.

- [ ] **Step 1: Verify the exact temporary targets before creation**

Run from the source repository root:

```powershell
Resolve-Path .
Test-Path -LiteralPath '.tmp-v1-clean'
Test-Path -LiteralPath '.tmp-v1-clean-snapshot.tar'
git check-ignore -v .tmp-v1-clean/probe
git status --short --branch
```

Expected: the resolved path matches the repository root returned by `git rev-parse --show-toplevel`; both `Test-Path` results are `False`; the root `.gitignore` rule for names beginning with `.tmp-` matches the probe; the source worktree is clean. Stop rather than delete or overwrite if either temporary target already exists.

- [ ] **Step 2: Export only tracked files**

Run:

```powershell
New-Item -ItemType Directory -Path '.tmp-v1-clean'
git archive --format=tar --output=.tmp-v1-clean-snapshot.tar HEAD
tar -xf .tmp-v1-clean-snapshot.tar -C .tmp-v1-clean
```

Verify that no source history or ignored state was copied:

```powershell
Test-Path -LiteralPath '.tmp-v1-clean\.git'
Test-Path -LiteralPath '.tmp-v1-clean\.superpowers'
Get-ChildItem -LiteralPath '.tmp-v1-clean' -Force
```

Expected: both `Test-Path` results are `False`; the listing contains only tracked project files.

- [ ] **Step 3: Initialize the clean repository and canonical identity**

Run:

```text
git -C .tmp-v1-clean init --initial-branch=main
git -C .tmp-v1-clean config user.name zhengguojie0922-crypto
git -C .tmp-v1-clean config user.email zhengguojie0922@gmail.com
git -C .tmp-v1-clean add --all
git -C .tmp-v1-clean commit -m "Initial release of Internship Work Summary Skill v1.0.0"
git -C .tmp-v1-clean tag -a v1.0.0 -m "Internship Work Summary Skill v1.0.0"
```

- [ ] **Step 4: Verify clean history and run tests inside the new repository**

Run:

```text
git -C .tmp-v1-clean rev-list --count main
git -C .tmp-v1-clean log -1 --format=fuller
git -C .tmp-v1-clean shortlog -sne --all
git -C .tmp-v1-clean status --short --branch
git -C .tmp-v1-clean rev-parse v1.0.0^{}
git -C .tmp-v1-clean rev-parse main
python -m unittest discover -s .tmp-v1-clean/tests -v
python -m compileall -q .tmp-v1-clean/skills .tmp-v1-clean/tests
git -C .tmp-v1-clean diff --check
```

Expected:

- commit count is `1`;
- author and committer are both `zhengguojie0922-crypto <zhengguojie0922@gmail.com>`;
- shortlog lists only that identity;
- worktree is clean on `main`;
- the peeled annotated tag SHA equals the `main` SHA;
- all 43 tests pass from the clean snapshot;
- compilation and diff checks exit 0.

### Task 3: Create and publish the new GitHub repository

**Files:**
- No tracked source-file changes
- Modify local Git remotes only after the corresponding GitHub repository operation succeeds

**Interfaces:**
- Consumes: the verified `.tmp-v1-clean` repository and current owner-authenticated GitHub session.
- Produces: a new public `zhengguojie0922-crypto/internship-work-summary-skill` repository containing the one-commit `main` branch and `v1.0.0` tag.

- [ ] **Step 1: Rename the current GitHub repository to the exact legacy name**

In the authenticated GitHub repository, open **Settings > General > Repository name**, change `internship-work-summary-skill` to `internship-work-summary-skill-legacy`, and confirm. Verify this exact URL loads before continuing:

```text
https://github.com/zhengguojie0922-crypto/internship-work-summary-skill-legacy
```

If browser automation cannot access an authenticated owner session, stop at this step and hand the exact rename to the user. Do not attempt to obtain or expose stored credentials.

- [ ] **Step 2: Separate the local legacy and new remotes safely**

After the GitHub rename succeeds, run in the source repository:

```text
git remote rename origin legacy
git remote set-url legacy https://github.com/zhengguojie0922-crypto/internship-work-summary-skill-legacy.git
git remote -v
```

Expected: only the `legacy` remote exists and both of its URLs use `internship-work-summary-skill-legacy.git`.

- [ ] **Step 3: Create the new empty public repository**

Create `zhengguojie0922-crypto/internship-work-summary-skill` in GitHub. Select **Public** and do not initialize a README, `.gitignore`, license, template, or first commit. Verify the empty repository page resolves at:

```text
https://github.com/zhengguojie0922-crypto/internship-work-summary-skill
```

If repository creation fails, leave the legacy repository intact and restore its original name only after confirming the new-name target does not exist.

- [ ] **Step 4: Push the clean branch and annotated tag**

Run:

```text
git -C .tmp-v1-clean remote add origin https://github.com/zhengguojie0922-crypto/internship-work-summary-skill.git
git -C .tmp-v1-clean push -u origin main
git -C .tmp-v1-clean push origin v1.0.0
git -C .tmp-v1-clean remote -v
```

Expected: both pushes succeed without force; fetch and push URLs use the new repository.

Add a non-tracking convenience remote to the source repository without changing its legacy branch upstreams:

```text
git remote add origin https://github.com/zhengguojie0922-crypto/internship-work-summary-skill.git
git remote -v
```

Expected: `legacy` points to the legacy repository and `origin` points to the new repository.

- [ ] **Step 5: Publish the GitHub Release**

Prepare this exact release title and body:

```markdown
Title: Internship Work Summary Skill v1.0.0

Internship Work Summary Skill 的首个稳定版本。

- 支持从具体功能出发追踪完整代码链路。
- 支持按 Git 身份发现和总结个人实习产出。
- 支持前端、后端、客户端、测试、DevOps、数据分析和算法七类岗位。
- 仅生成 `career-output/实习产出与面试准备.md`，不创建中间文档。
- 提供简历表述、面试介绍、核心问题、追问和场景题。
- 保持只读仓库分析、证据约束和敏感信息脱敏。
```

Open **Releases > Draft a new release**, select existing tag `v1.0.0`, enter the title and body, and mark it as the latest release. Because publishing communicates publicly on the user's behalf, request action-time confirmation immediately before clicking **Publish release**.

### Task 4: Verify the new repository and gate legacy deletion

**Files:**
- Create ignored verification clone: `.tmp-v1-verify/`
- No tracked source-file changes

**Interfaces:**
- Consumes: the published new repository, tag, release, and completed GitHub Actions run.
- Produces: an evidence-based deletion decision for `zhengguojie0922-crypto/internship-work-summary-skill-legacy`.

- [ ] **Step 1: Verify remote refs, root history, and commit identity**

Before cloning, require `Test-Path -LiteralPath '.tmp-v1-verify'` to return `False`. Then run:

```text
git clone https://github.com/zhengguojie0922-crypto/internship-work-summary-skill.git .tmp-v1-verify
git -C .tmp-v1-verify rev-list --count main
git -C .tmp-v1-verify log -1 --format=fuller
git -C .tmp-v1-verify shortlog -sne --all
git -C .tmp-v1-verify rev-parse v1.0.0^{}
git -C .tmp-v1-verify rev-parse main
```

Expected: one commit; only the current account identity; tag and `main` resolve to the same commit.

- [ ] **Step 2: Verify public product and CI surfaces**

Verify on GitHub:

- the repository is public and `main` is the default branch;
- GitHub Actions for the root commit passes on Ubuntu, Windows, and macOS for Python 3.10 and 3.x;
- the README installation URL and Skills CLI commands refer to the new repository and `summarizing-internship-work`;
- the `v1.0.0` release is public and marked latest;
- `skills/summarizing-internship-work/SKILL.md` is reachable;
- `commits?author=zgjaaaaaa` shows no commit history;
- the Contributors graph has no source commit attributable to `zgjaaaaaa`, allowing for GitHub cache recomputation time.

Run from the verification clone:

```text
python -m unittest discover -s tests -v
python -m compileall -q skills tests
git diff --check
```

Expected: all 43 tests pass; compilation and diff checks exit 0.

- [ ] **Step 3: Present the exact destructive target and request confirmation**

Only after Steps 1 and 2 pass, present exactly:

```text
Permanent deletion target:
https://github.com/zhengguojie0922-crypto/internship-work-summary-skill-legacy

This permanently removes its Stars, Issues, pull requests, Actions history, settings, and redirect. Type `delete internship-work-summary-skill-legacy` to confirm.
```

Do not accept the earlier design approval as deletion confirmation. Stop until the exact confirmation is received.

- [ ] **Step 4: Delete only the confirmed legacy repository**

After exact confirmation, open the legacy repository's **Settings > General > Danger Zone > Delete this repository**, verify the owner and repository name are exactly `zhengguojie0922-crypto/internship-work-summary-skill-legacy`, enter GitHub's required confirmation text, and delete it. Do not delete the new `internship-work-summary-skill` repository.

Verify afterward that the legacy URL returns not found while the new repository, `main`, `v1.0.0` tag, release, and Actions remain accessible. Keep the local legacy refs until the user explicitly requests local cleanup.
