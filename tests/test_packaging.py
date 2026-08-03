"""Focused publishing-surface contract tests."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
OLD_SKILL_DIR = ROOT / "skills" / "analyzing-codebase-work-impact"
SKILL_DIR = ROOT / "skills" / "summarizing-internship-work"
README = ROOT / "README.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"
LICENSE = ROOT / "LICENSE"
WORKFLOW = ROOT / ".github" / "workflows" / "test.yml"
METADATA = SKILL_DIR / "agents" / "openai.yaml"
VERSION = SKILL_DIR / "VERSION"
CAREER_WORKFLOW_DESIGN = (
    ROOT / "docs" / "superpowers" / "specs" / "2026-07-31-single-document-career-workflow-design.md"
)
CAREER_WORKFLOW_PLAN = (
    ROOT / "docs" / "superpowers" / "plans" / "2026-07-31-single-document-career-workflow.md"
)

PUBLISHING_FILES = (README, CONTRIBUTING, LICENSE, WORKFLOW, METADATA, VERSION)
NEW_REPOSITORY = "zhengguojie0922-crypto/internship-work-summary-skill"
OLD_IDENTITY_PHRASES = (
    "Codebase Work Impact",
    "codebase-work-impact",
    "codebase-work-impact-skill",
    "analyzing-codebase-work-impact",
    "$analyzing-codebase-work-impact",
)
RETIRED_ARTIFACTS = (
    "session.json",
    "evidence-report.json",
    "evidence-report.md",
    "fact-cards.json",
    "fact-cards.md",
    "career-package.md",
    "resume-audit.json",
)
OBSOLETE_RUNTIME_PATHS = (
    ROOT / "docs" / "artifact-schemas.md",
    ROOT / "docs" / "examples" / "evidence-report.minimal.json",
    ROOT / "docs" / "examples" / "fact-cards.minimal.json",
    ROOT / "docs" / "examples" / "resume-audit.minimal.json",
    ROOT / "docs" / "examples" / "session.minimal.json",
    SKILL_DIR / "references" / "evidence-model.md",
    SKILL_DIR / "references" / "identity-gate.md",
    SKILL_DIR / "scripts" / "validate_artifact.py",
    ROOT / "tests" / "fixture_builder.py",
    ROOT / "tests" / "forward_test_runner.py",
    ROOT / "tests" / "test_final_review_contracts.py",
    ROOT / "tests" / "test_fixture_builder_and_assets.py",
    ROOT / "tests" / "test_forward_test_runner.py",
    ROOT / "tests" / "test_production_baseline.py",
    ROOT / "tests" / "test_validate_artifact.py",
)
SENSITIVE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    re.compile(r"(?i)\b(?:password|passwd|secret|token|credential|api[_-]?key)\s*[:=]\s*\S+"),
)
ABSOLUTE_PATH_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_.:/~>-])(?:[A-Za-z]:[\\/]\S*|/(?!/)[A-Za-z0-9._-]\S*)"
)
MIT_TEXT = """MIT License

Copyright (c) 2026 internship-work-summary-skill contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def read_utf8(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AssertionError(f"{path.relative_to(ROOT)} has a UTF-8 BOM")
    return raw.decode("utf-8")


def public_markdown_files() -> tuple[Path, ...]:
    completed = subprocess.run(
        ["git", "ls-files", "--", "README.md", "CONTRIBUTING.md", "docs", "skills"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    paths = {
        path
        for relative in completed.stdout.splitlines()
        if relative.endswith(".md") and (path := ROOT / relative).is_file()
    }
    paths.update((CAREER_WORKFLOW_DESIGN, CAREER_WORKFLOW_PLAN))
    return tuple(sorted(path for path in paths if path.is_file()))


def assert_no_files(test_case: unittest.TestCase, root: Path, pattern: str) -> None:
    test_case.assertEqual([], list(root.rglob(pattern)))


def parse_openai_metadata(text: str) -> dict[str, dict[str, str | bool]]:
    expected_fields = {
        "interface": {"display_name", "short_description", "default_prompt"},
        "policy": {"allow_implicit_invocation"},
    }
    parsed: dict[str, dict[str, str | bool]] = {}
    section: str | None = None

    for number, line in enumerate(text.splitlines(), start=1):
        if not line:
            continue
        section_match = re.fullmatch(r"([a-z_]+):", line)
        if section_match:
            section = section_match.group(1)
            if section not in expected_fields or section in parsed:
                raise ValueError(f"line {number}: unexpected section")
            parsed[section] = {}
            continue

        field_match = re.fullmatch(r"  ([a-z_]+): (.+)", line)
        if section is None or field_match is None:
            raise ValueError(f"line {number}: expected a two-space field")
        key, raw_value = field_match.groups()
        if key not in expected_fields[section] or key in parsed[section]:
            raise ValueError(f"line {number}: unexpected field")
        if raw_value in {"true", "false"}:
            value: str | bool = raw_value == "true"
        else:
            if not (raw_value.startswith('"') and raw_value.endswith('"')):
                raise ValueError(f"line {number}: expected quoted string")
            value = json.loads(raw_value)
            if not isinstance(value, str):
                raise ValueError(f"line {number}: expected quoted string")
        parsed[section][key] = value

    if set(parsed) != set(expected_fields):
        raise ValueError("missing or unexpected sections")
    for name, fields in expected_fields.items():
        if set(parsed[name]) != fields:
            raise ValueError(f"missing or unexpected fields in {name}")
    return parsed


def assert_local_links_resolve(text: str, source: Path) -> None:
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        destination = match.group(1).strip().split(maxsplit=1)[0]
        if not destination or destination.startswith("#"):
            continue
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination):
            continue
        target = unquote(destination.strip("<>").split("#", 1)[0])
        if not (source.parent / target).resolve().exists():
            raise AssertionError(f"broken local Markdown link in {source.name}: {destination}")


class PublishingSurfaceTests(unittest.TestCase):
    def test_required_publishing_files_exist(self) -> None:
        for path in PUBLISHING_FILES:
            self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")

    def test_only_the_renamed_skill_directory_is_installable(self) -> None:
        self.assertFalse(OLD_SKILL_DIR.exists())
        self.assertTrue(SKILL_DIR.is_dir())
        self.assertEqual([SKILL_DIR], sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir()))

    def test_retired_artifact_publishing_and_runtime_files_are_absent(self) -> None:
        for path in OBSOLETE_RUNTIME_PATHS:
            self.assertFalse(path.exists(), f"retired runtime asset remains: {path.relative_to(ROOT)}")
        assert_no_files(self, SKILL_DIR / "references" / "schemas", "*.json")
        assert_no_files(self, ROOT / "docs" / "examples", "*.json")
        assert_no_files(self, ROOT / "tests" / "fixtures", "*")
        assert_no_files(self, ROOT / "tests" / "scenarios", "*")

    def test_obsolete_file_check_detects_nested_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            nested_file = root / "nested" / "artifact.json"
            nested_file.parent.mkdir()
            nested_file.write_text("{}", encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_no_files(self, root, "*.json")

    def test_readme_documents_single_document_workflow(self) -> None:
        text = read_utf8(README)
        for phrase in (
            "$skill-installer",
            "npx skills add",
            "$summarizing-internship-work",
            "\u547d\u540d\u529f\u80fd",
            "Git",
            "\u76ee\u6807\u5c97\u4f4d",
            "Git \u8eab\u4efd",
            "\u6700\u591a\u4e24\u8f6e",
            "career-output/\u5b9e\u4e60\u4ea7\u51fa\u4e0e\u9762\u8bd5\u51c6\u5907.md",
            "\u4e1a\u52a1\u529f\u80fd",
            "\u4ee3\u7801\u8def\u5f84",
            "\u4e09\u79cd\u7b80\u5386",
            "30 \u79d2",
            "1 \u5206\u949f",
            "3 \u5206\u949f",
            "20 \u4e2a\u6838\u5fc3\u95ee\u9898",
            "\u53c2\u8003\u56de\u7b54",
            "\u8ffd\u95ee",
            "\u573a\u666f\u9898",
            "\u6307\u6807",
            "\u8bc1\u636e\u7d22\u5f15",
            "\u4e2d\u6587",
            "\u82f1\u6587",
            "\u53cc\u8bed",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("Code > Download ZIP", text)
        for artifact in RETIRED_ARTIFACTS:
            self.assertNotIn(artifact, text)
        for phrase in ("\u4e2d\u95f4 JSON", "evidence", "fact-card", "audit", "session"):
            self.assertIn(phrase, text)
        for phrase in ("\u53ea\u8bfb", "\u4e0d\u6267\u884c\u76ee\u6807\u4ed3\u5e93\u4ee3\u7801", "\u4e0d\u7f16\u9020\u6307\u6807", "\u8131\u654f"):
            self.assertIn(phrase, text)
        for role in ("frontend", "backend", "client", "testing", "DevOps", "data analytics", "algorithm"):
            self.assertIn(role, text)

    def test_readme_uses_the_stable_release_identity(self) -> None:
        text = read_utf8(README)
        self.assertIn(NEW_REPOSITORY, text)
        self.assertIn("--skill summarizing-internship-work", text)
        self.assertIn("$summarizing-internship-work", text)
        self.assertIn("1.2.0", text)
        self.assertNotIn("## \u4ece 0.2.x \u5347\u7ea7", text)
        for phrase in OLD_IDENTITY_PHRASES:
            self.assertNotIn(phrase, text)

    def test_nonhistorical_product_files_do_not_use_the_retired_identity(self) -> None:
        active_files = {
            README,
            CONTRIBUTING,
            LICENSE,
            WORKFLOW,
            *(
                path
                for path in SKILL_DIR.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            ),
        }
        for path in sorted(active_files):
            text = read_utf8(path)
            for phrase in OLD_IDENTITY_PHRASES:
                self.assertNotIn(phrase, text, path.relative_to(ROOT))

    def test_readme_explains_detailed_features_roles_and_routing(self) -> None:
        text = read_utf8(README)
        self.assertIn("## 详细功能", text)
        self.assertIn("## 触发与路由", text)
        self.assertLess(text.index("## 详细功能"), text.index("## 触发与路由"))
        for phrase in (
            "功能代码链路追踪",
            "Git 实习产出发现",
            "证据与归属边界",
            "简历表述",
            "面试准备",
            "单文档输出",
            "前端（`frontend`）",
            "后端（`backend`）",
            "客户端（`client`）",
            "测试（`testing`）",
            "DevOps",
            "数据分析（`data analytics`）",
            "算法（`algorithm`）",
            "命名功能路由",
            "Git 发现路由",
            "混合请求",
            "不询问 Git 身份",
            "同时确认 Git 身份和目标岗位",
            "默认该功能由用户完整实现",
            "不自动声明个人所有权",
            "只有用户明确要求 Git 校验时",
            "完整姓名或完整邮箱精确匹配",
            "共同作者",
            "默认选择证据最强的 3 项",
            "明确要求全面总结时才扩展到最多 5 项",
            "3-5 个独立场景题",
            "证据不足时少于 20 个",
            "代码证据锚点",
            "详细问题",
            "考察意图",
            "代码依据",
            "思考过程",
            "详细参考回答",
            "设计取舍",
            "异常与验证",
            "深入追问",
            "逐条完整回答",
            "保留无关的已验证内容",
            "明确要求重建",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("简洁参考回答", text)
        self.assertNotIn("回答方向", text)

    def test_metadata_and_version_are_aligned_with_the_current_release(self) -> None:
        metadata = parse_openai_metadata(read_utf8(METADATA))
        self.assertEqual(
            {
                "interface": {
                    "display_name": "Internship Work Summary",
                    "short_description": "\u4ece\u672c\u5730\u4ee3\u7801\u5e93\u8bc1\u636e\u603b\u7ed3\u53ef\u6838\u9a8c\u7684\u5b9e\u4e60\u4ea7\u51fa\u3001\u7b80\u5386\u548c\u9762\u8bd5\u6750\u6599\u3002",
                    "default_prompt": "\u4f7f\u7528 $summarizing-internship-work \u57fa\u4e8e\u672c\u5730\u4ee3\u7801\u5e93\u548c Git \u8bc1\u636e\u751f\u6210\u53ef\u6838\u9a8c\u7684\u5b9e\u4e60\u4ea7\u51fa\u3001\u7b80\u5386\u4e0e\u9762\u8bd5\u51c6\u5907\u6587\u6863\u3002",
                },
                "policy": {"allow_implicit_invocation": True},
            },
            metadata,
        )
        with self.assertRaisesRegex(ValueError, "quoted string"):
            parse_openai_metadata("interface:\n  display_name: Codebase Work Impact\n")
        self.assertEqual("1.2.0", read_utf8(VERSION).strip())
        self.assertIn("1.2.0", read_utf8(README))

    def test_readme_distinguishes_structural_verification_from_model_behavior(self) -> None:
        text = read_utf8(README)
        for phrase in (
            "## 验证",
            "python -m unittest discover -s tests -v",
            "python -m compileall -q skills tests",
            "git diff --check",
            "结构性测试",
            "模型层行为",
            "`1.2.0` 未执行独立模型前向验收",
            "不代表 DS、Claude",
            "不代表完整模型矩阵",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("截至 2026-07-31", text)

    def test_license_is_exact_mit_text_across_line_endings(self) -> None:
        actual = read_utf8(LICENSE).replace("\r\n", "\n")
        self.assertEqual(MIT_TEXT, actual)

    def test_public_markdown_has_resolved_links_and_no_local_paths_or_secrets(self) -> None:
        self.assertNotIn(ROOT / "docs" / "artifact-schemas.md", public_markdown_files())
        self.assertIn(ROOT / "docs" / "superpowers" / "plans" / "2026-07-30-chinese-readme.md", public_markdown_files())
        self.assertIn(CAREER_WORKFLOW_DESIGN, public_markdown_files())
        self.assertIn(CAREER_WORKFLOW_PLAN, public_markdown_files())
        self.assertIn(SKILL_DIR / "SKILL.md", public_markdown_files())
        self.assertTrue(SENSITIVE_PATTERNS[1].search("AKIA" + "A" * 16))
        self.assertTrue(SENSITIVE_PATTERNS[2].search("ghp_" + "a" * 36))
        for path in (r"D:\repo", r"C:\work", "/private/project", "/tmp/report", "/var/log/app.log"):
            self.assertRegex(path, ABSOLUTE_PATH_PATTERN)
        for non_path in ("https://example.test/path", "//server/share", "~/.codex/skills", "<user-home>/.codex/skills"):
            self.assertNotRegex(non_path, ABSOLUTE_PATH_PATTERN)
        for path in public_markdown_files():
            text = read_utf8(path)
            assert_local_links_resolve(text, path)
            self.assertNotRegex(text, ABSOLUTE_PATH_PATTERN)
            for pattern in SENSITIVE_PATTERNS:
                self.assertIsNone(pattern.search(text), f"sensitive text in {path.relative_to(ROOT)}")

    def test_contributing_covers_only_remaining_tests_and_tools(self) -> None:
        text = read_utf8(CONTRIBUTING)
        for phrase in (
            "Python 3.10",
            "Git 2.30",
            "python -m unittest tests.test_packaging -v",
            "python -m unittest tests.test_skill_contract -v",
            "python -m unittest tests.test_collect_git_evidence -v",
            "python -m unittest discover -s tests -v",
            "python -m compileall -q skills tests",
            "git diff --check",
            "三个聚焦测试模块",
            "RED",
            "GREEN",
            "\u53ea\u8bfb",
            "\u4e0d\u6267\u884c\u76ee\u6807\u4ed3\u5e93\u4ee3\u7801",
        ):
            self.assertIn(phrase, text)
        for retired in ("validator", "schema", "fixture", "scenario", "forward-runner", "model-forward-test"):
            self.assertNotIn(retired, text.lower())

    def test_implementation_plan_marks_completed_deterministic_work_factually(self) -> None:
        plan = read_utf8(ROOT / "docs" / "superpowers" / "plans" / "2026-07-31-single-document-career-workflow.md")
        task_four = plan.split("### Task 4:", 1)[1].split("### Task 5:", 1)[0]
        task_five = plan.split("### Task 5:", 1)[1]
        self.assertNotIn("- [ ]", task_four)
        for step in (
            "- [x] **Step 1: Run `python -m unittest discover -s tests -v`.**",
            "- [x] **Step 3: Run `git diff --check`.**",
            "- [x] **Step 4: Inspect `git status --short` and the complete diff for accidental or unrelated changes.**",
            "- [x] **Step 5: Run `python -m compileall -q skills tests`.**",
            "run limited codex acceptance for both routes",
            "ds, claude, and a full multi-model matrix were not run and are not claimed",
        ):
            self.assertIn(step.casefold(), task_five.casefold())

    def test_design_requires_git_discovery_confirmation_even_for_inferred_values(self) -> None:
        design = read_utf8(
            ROOT / "docs" / "superpowers" / "specs" / "2026-07-31-single-document-career-workflow-design.md"
        )
        self.assertIn("confirm both in the first consolidated question", design)
        self.assertIn("not as substitutes for confirmation in Git discovery", design)
        self.assertNotIn(
            "requires a Git identity only when it cannot be inferred",
            design,
        )

    def test_ci_matrix_covers_python_310_and_latest_on_all_platforms(self) -> None:
        workflow = json.loads(read_utf8(WORKFLOW))
        matrix = workflow["jobs"]["test"]["strategy"]["matrix"]
        self.assertEqual(["ubuntu-latest", "windows-latest", "macos-latest"], matrix["os"])
        self.assertEqual(["3.10", "3.x"], matrix["python-version"])


if __name__ == "__main__":
    unittest.main()
