# Internship Work Summary Rename Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the installable project from Codebase Work Impact to Internship Work Summary without changing either analysis route or the single-document runtime contract.

**Architecture:** Preserve the existing Skill contents and move the complete installable directory as one unit so references and scripts keep their relative layout. Treat the new directory, frontmatter name, OpenAI metadata, version, README installation surface, and publishing tests as one canonical identity; allow the retired identity only inside an explicitly delimited migration section.

**Tech Stack:** Agent Skills Markdown/YAML, Python 3.10+ standard-library `unittest`, Git 2.30+, GitHub Actions

## Global Constraints

- Canonical project display name: `Internship Work Summary Skill`.
- Canonical Skill display name: `Internship Work Summary`.
- Canonical Skill identifier: `summarizing-internship-work`.
- Canonical installable directory: `skills/summarizing-internship-work`.
- Canonical GitHub repository name: `internship-work-summary-skill`.
- Release version: `0.3.0`.
- Do not keep an alias Skill or duplicate directory for `analyzing-codebase-work-impact`.
- Preserve both request routes, all seven role guides, the two-round confirmation limit, read-only repository inspection, and the sole runtime output `career-output/实习产出与面试准备.md`.
- Historical files under `docs/superpowers/specs/` and `docs/superpowers/plans/` retain the names used by the versions they document.
- Do not modify a user's globally installed Skills during implementation or testing.

---

### Task 1: Rename the installable Skill package

**Files:**
- Move: `skills/analyzing-codebase-work-impact/` to `skills/summarizing-internship-work/`
- Modify: `skills/summarizing-internship-work/SKILL.md`
- Modify: `skills/summarizing-internship-work/agents/openai.yaml`
- Modify: `skills/summarizing-internship-work/VERSION`
- Modify: `README.md`
- Modify: `LICENSE`
- Modify: `tests/test_skill_contract.py`
- Modify: `tests/test_collect_git_evidence.py`
- Modify: `tests/test_packaging.py`

**Interfaces:**
- Consumes: the behavior contract and relative reference layout currently contained by `skills/analyzing-codebase-work-impact/`.
- Produces: one installable Skill rooted at `skills/summarizing-internship-work/`, named `summarizing-internship-work`, with version `0.3.0`.

- [ ] **Step 1: Change focused tests to require the new package identity**

In `tests/test_skill_contract.py`, change the path and identity expectations:

```python
SKILL_DIR = ROOT / "skills" / "summarizing-internship-work"

# In test_frontmatter_triggers_internship_resume_and_interview_requests:
self.assertEqual("summarizing-internship-work", self.frontmatter["name"])

# In test_metadata_supports_implicit_invocation_and_names_the_skill:
self.assertIn('display_name: "Internship Work Summary"', metadata)
self.assertIn("$summarizing-internship-work", metadata)
```

In `tests/test_collect_git_evidence.py`, resolve the collector from the new directory:

```python
COLLECTOR = ROOT / "skills" / "summarizing-internship-work" / "scripts" / "collect_git_evidence.py"
```

In `tests/test_packaging.py`, change `SKILL_DIR`, the expected MIT copyright line, OpenAI metadata, and release assertions:

```python
OLD_SKILL_DIR = ROOT / "skills" / "analyzing-codebase-work-impact"
SKILL_DIR = ROOT / "skills" / "summarizing-internship-work"

# MIT_TEXT
Copyright (c) 2026 internship-work-summary-skill contributors

# test_metadata_and_version_are_aligned_with_the_breaking_release
self.assertEqual(
    {
        "interface": {
            "display_name": "Internship Work Summary",
            "short_description": "从本地代码库证据总结可核验的实习产出、简历和面试材料。",
            "default_prompt": "使用 $summarizing-internship-work 基于本地代码库和 Git 证据生成可核验的实习产出、简历与面试准备文档。",
        },
        "policy": {"allow_implicit_invocation": True},
    },
    metadata,
)
self.assertEqual("0.3.0", read_utf8(VERSION).strip())
self.assertIn("0.3.0", read_utf8(README))
```

Add this package-boundary test to `PublishingSurfaceTests`:

```python
def test_only_the_renamed_skill_directory_is_installable(self) -> None:
    self.assertFalse(OLD_SKILL_DIR.exists())
    self.assertTrue(SKILL_DIR.is_dir())
    self.assertEqual([SKILL_DIR], sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir()))
```

- [ ] **Step 2: Run the renamed-path tests and record RED**

Run:

```text
python -m unittest tests.test_skill_contract tests.test_collect_git_evidence tests.test_packaging.PublishingSurfaceTests.test_required_publishing_files_exist tests.test_packaging.PublishingSurfaceTests.test_only_the_renamed_skill_directory_is_installable -v
```

Expected: ERROR or FAIL because `skills/summarizing-internship-work/` does not exist and the old directory still exists.

- [ ] **Step 3: Move the package and update its canonical metadata**

Move the complete directory with Git history preserved:

```text
git mv skills/analyzing-codebase-work-impact skills/summarizing-internship-work
```

Change only the frontmatter name and H1 in `skills/summarizing-internship-work/SKILL.md`; retain the body behavior verbatim:

```yaml
---
name: summarizing-internship-work
description: Use when a user asks for 实习产出, 实习总结, 项目经历, 简历包装, 简历优化, 写到简历, 工作成果, 面试准备, internship output, internship summary, project experience, resume writing, resume optimization, CV writing, work achievements, or interview preparation from a local codebase, Git history, commit range, or named feature.
---

# Internship Work Summary
```

Replace `skills/summarizing-internship-work/agents/openai.yaml` with:

```yaml
interface:
  display_name: "Internship Work Summary"
  short_description: "从本地代码库证据总结可核验的实习产出、简历和面试材料。"
  default_prompt: "使用 $summarizing-internship-work 基于本地代码库和 Git 证据生成可核验的实习产出、简历与面试准备文档。"
policy:
  allow_implicit_invocation: true
```

Set `skills/summarizing-internship-work/VERSION` to exactly:

```text
0.3.0
```

Change the README H1 and opening identity sentence now so the package-version assertion is coherent; leave installation and migration copy for Task 2:

```markdown
# Internship Work Summary Skill

`summarizing-internship-work` 从本地代码库和 Git 证据总结可核验的实习产出，并生成简历和面试准备文档。版本 `0.3.0` 是彻底更名后的破坏性更新，采用 MIT 许可证。
```

In `LICENSE`, change only the copyright line:

```text
Copyright (c) 2026 internship-work-summary-skill contributors
```

- [ ] **Step 4: Run the focused package tests and verify GREEN**

Run:

```text
python -m unittest tests.test_skill_contract tests.test_collect_git_evidence tests.test_packaging.PublishingSurfaceTests.test_required_publishing_files_exist tests.test_packaging.PublishingSurfaceTests.test_only_the_renamed_skill_directory_is_installable tests.test_packaging.PublishingSurfaceTests.test_metadata_and_version_are_aligned_with_the_breaking_release tests.test_packaging.PublishingSurfaceTests.test_license_is_exact_mit_text_across_line_endings -v
```

Expected: all selected tests PASS. No behavior assertion or role-reference assertion changes other than the canonical name and path.

- [ ] **Step 5: Commit the installable package rename**

```text
git add README.md LICENSE skills tests/test_skill_contract.py tests/test_collect_git_evidence.py tests/test_packaging.py
git commit -m "Rename skill to internship work summary"
```

### Task 2: Update installation, invocation, and migration documentation

**Files:**
- Modify: `README.md`
- Modify: `tests/test_packaging.py`

**Interfaces:**
- Consumes: the `summarizing-internship-work` package, version, and metadata established by Task 1.
- Produces: new-user installation guidance that uses only the new repository and Skill names, plus one concise `0.2.x` migration section where the retired identity may be mentioned.

- [ ] **Step 1: Write failing publishing-surface tests for the rename and migration**

Change the explicit invocation assertion in `test_readme_documents_single_document_workflow`:

```python
"$summarizing-internship-work",
```

Add these constants near the existing publishing constants:

```python
NEW_REPOSITORY = "zhengguojie0922-crypto/internship-work-summary-skill"
OLD_IDENTITY_PHRASES = (
    "Codebase Work Impact",
    "codebase-work-impact-skill",
    "analyzing-codebase-work-impact",
    "$analyzing-codebase-work-impact",
)
```

Add two tests to `PublishingSurfaceTests`:

```python
def test_readme_uses_the_new_installation_and_invocation_identity(self) -> None:
    text = read_utf8(README)
    migration_heading = "## 从 0.2.x 升级"
    active_guidance, separator, migration = text.partition(migration_heading)
    self.assertEqual(migration_heading, separator)
    self.assertIn(NEW_REPOSITORY, active_guidance)
    self.assertIn("--skill summarizing-internship-work", active_guidance)
    self.assertIn("$summarizing-internship-work", active_guidance)
    for phrase in OLD_IDENTITY_PHRASES:
        self.assertNotIn(phrase, active_guidance)
    self.assertIn("analyzing-codebase-work-impact", migration)
    self.assertIn("summarizing-internship-work", migration)

def test_nonhistorical_product_files_do_not_use_the_retired_identity(self) -> None:
    active_files = (
        CONTRIBUTING,
        LICENSE,
        WORKFLOW,
        SKILL_DIR / "SKILL.md",
        METADATA,
        VERSION,
    )
    for path in active_files:
        text = read_utf8(path)
        for phrase in OLD_IDENTITY_PHRASES:
            self.assertNotIn(phrase, text, path.relative_to(ROOT))
```

Do not add historical plans or specifications to `active_files`.

- [ ] **Step 2: Run the publishing tests and record RED**

Run:

```text
python -m unittest tests.test_packaging.PublishingSurfaceTests.test_readme_documents_single_document_workflow tests.test_packaging.PublishingSurfaceTests.test_readme_uses_the_new_installation_and_invocation_identity tests.test_packaging.PublishingSurfaceTests.test_nonhistorical_product_files_do_not_use_the_retired_identity -v
```

Expected: FAIL because normal README installation and invocation guidance still contains the retired repository and Skill identifiers, and the migration section is absent.

- [ ] **Step 3: Replace normal README installation and invocation guidance**

Use the new canonical repository and Skill names in the Skill Installer prompt:

```text
使用 $skill-installer 从 https://github.com/zhengguojie0922-crypto/internship-work-summary-skill/tree/main/skills/summarizing-internship-work 安装这个 Skill。
```

Use the new names in both Skills CLI commands:

```sh
npx skills add zhengguojie0922-crypto/internship-work-summary-skill --skill summarizing-internship-work --agent codex --global --yes
npx skills add zhengguojie0922-crypto/internship-work-summary-skill --skill summarizing-internship-work --agent claude-code --global --yes
```

Change every normal explicit invocation example to:

```text
$summarizing-internship-work
```

Do not change the documented triggers, request routing, seven roles, output path, or verification claims.

- [ ] **Step 4: Add the concise breaking-change migration section**

Place this section after Quick Installation and before Detailed Features:

```markdown
## 从 0.2.x 升级

`0.3.0` 将 Skill 从 `analyzing-codebase-work-impact` 彻底更名为 `summarizing-internship-work`，不保留旧 Skill 副本。已有用户先从 Codex 或 Claude Code 的 Skills 目录中移除旧 Skill，再按照上面的快速安装命令安装新 Skill；不要同时保留两个版本，以免重复触发。
```

- [ ] **Step 5: Run focused and complete verification**

Run:

```text
python -m unittest tests.test_packaging -v
python -m unittest tests.test_skill_contract -v
python -m unittest tests.test_collect_git_evidence -v
python -m unittest discover -s tests -v
python -m compileall -q skills tests
git diff --check
```

Expected: all unit tests PASS; `compileall` and `git diff --check` exit 0 with no output. The unit-test count may increase only by the new package-boundary and publishing-surface tests.

- [ ] **Step 6: Inspect the final rename diff and commit**

Run:

```text
git status --short
git diff --stat HEAD
git diff HEAD -- README.md tests/test_packaging.py
```

Expected: only the planned README and publishing-test changes remain after Task 1's commit; the README migration section is the only active documentation location that mentions `analyzing-codebase-work-impact`.

Commit:

```text
git add README.md tests/test_packaging.py
git commit -m "Document internship work summary migration"
```

### Task 3: Complete the GitHub rename handoff

**Files:**
- No repository file changes

**Interfaces:**
- Consumes: the merged `0.3.0` rename commits and a repository owner session on GitHub.
- Produces: the public repository URL `https://github.com/zhengguojie0922-crypto/internship-work-summary-skill` and a matching local `origin` URL.

- [ ] **Step 1: Confirm the implementation branch is ready for review**

Run:

```text
git status --short --branch
git log --oneline origin/main..HEAD
```

Expected: a clean worktree and the design plus two implementation commits ahead of `origin/main`.

- [ ] **Step 2: Push the branch and merge it through a pull request**

Push the current branch, open a pull request, wait for the full GitHub Actions matrix, and merge only after all required checks pass. Do not push the implementation commits directly to `main`.

- [ ] **Step 3: Rename the GitHub repository after the implementation merge**

As repository owner, open **Settings > General > Repository name**, change `codebase-work-impact-skill` to `internship-work-summary-skill`, and confirm the rename. Verify that the new repository page loads and that the old URL redirects to it.

- [ ] **Step 4: Update and verify the local remote URL**

Run:

```text
git remote set-url origin https://github.com/zhengguojie0922-crypto/internship-work-summary-skill.git
git remote -v
```

Expected: both fetch and push URLs use `internship-work-summary-skill.git`.
