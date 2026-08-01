"""Behavior contract for the installable work-impact skill."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "summarizing-internship-work"
SKILL_PATH = SKILL_DIR / "SKILL.md"
METADATA_PATH = SKILL_DIR / "agents" / "openai.yaml"
ROLE_FRAMEWORK_PATH = SKILL_DIR / "references" / "role-analysis-framework.md"

ROLE_REQUIRED_HEADINGS = (
    "## Role Boundary and Subdomains",
    "## Entry-Point Discovery",
    "## Typical Code Chains",
    "## Technical Decision Matrix",
    "## Failure Modes and Risks",
    "## Validation Evidence",
    "## Impact and Metrics Evidence",
    "## Resume Mapping",
    "## Interview Question Tree",
    "## Overclaim Guardrails",
)

TRIGGERS = (
    "实习产出",
    "实习总结",
    "项目经历",
    "简历包装",
    "简历优化",
    "写到简历",
    "工作成果",
    "面试准备",
)
ENGLISH_TRIGGERS = (
    "internship output",
    "internship summary",
    "project experience",
    "resume writing",
    "resume optimization",
    "CV writing",
    "work achievements",
    "interview preparation",
)

LEGACY_ARTIFACTS = (
    "session.json",
    "evidence-report.json",
    "evidence-report.md",
    "fact-cards.json",
    "fact-cards.md",
    "career-package.md",
    "resume-audit.json",
)
REQUIRED_REFERENCE_LINKS = (
    "[analysis defaults](references/analysis-defaults.md)",
    "[achievement analysis](references/achievement-analysis.md)",
    "[role classification](references/role-classification.md)",
    "[role analysis framework](references/role-analysis-framework.md)",
    "[frontend guide](references/role-frontend.md)",
    "[backend guide](references/role-backend.md)",
    "[client guide](references/role-client.md)",
    "[testing guide](references/role-testing.md)",
    "[DevOps guide](references/role-devops.md)",
    "[data analytics guide](references/role-data-analytics.md)",
    "[algorithm guide](references/role-algorithm.md)",
)


def read_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.fullmatch(r"---\n(?P<header>.*?)\n---\n(?P<body>.*)", text, re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md must contain LF-delimited YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group("header").splitlines():
        key, separator, value = line.partition(": ")
        if not separator:
            raise AssertionError(f"invalid frontmatter line: {line!r}")
        fields[key] = value
    return fields, match.group("body")


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SKILL_PATH.read_text(encoding="utf-8")
        cls.frontmatter, cls.body = read_frontmatter(cls.text)

    def test_frontmatter_triggers_internship_resume_and_interview_requests(self) -> None:
        self.assertEqual("summarizing-internship-work", self.frontmatter["name"])
        self.assertEqual({"name", "description"}, set(self.frontmatter))
        description = self.frontmatter["description"]
        self.assertTrue(description.startswith("Use when "))
        for trigger in TRIGGERS:
            self.assertIn(trigger, description)
        for trigger in ENGLISH_TRIGGERS:
            self.assertIn(trigger, description)

    def test_request_routes_are_feature_or_git_discovery(self) -> None:
        for phrase in (
            "specific feature",
            "trace the feature",
            "regardless of commit authorship",
            "no specific feature",
            "Git history",
            "cluster commits",
        ):
            self.assertIn(phrase, self.body)

    def test_missing_information_is_batched_into_at_most_two_rounds(self) -> None:
        for phrase in (
            "at most two confirmation rounds",
            "one consolidated question",
            "Git identity",
            "target role",
            "infer supplied values",
            "continue with explicit unknowns",
        ):
            self.assertIn(phrase, self.body)

    def test_git_discovery_confirms_identity_and_target_role_before_analysis(self) -> None:
        discovery_section = self._section("Discover Contributions From Git History")
        for phrase in (
            "first consolidated question",
            "confirm both",
            "Git identity",
            "target role",
            "before analyzing commits",
            "even when candidate values can be inferred",
        ):
            self.assertIn(phrase, discovery_section)

    def test_named_feature_route_does_not_require_git_identity(self) -> None:
        feature_section = self._section("Trace a Named Feature")
        self.assertIn("Do not ask for a Git identity", feature_section)
        self.assertIn("entry point", feature_section)
        self.assertIn("data flow", feature_section)
        self.assertIn("error handling", feature_section)
        self.assertIn("tests", feature_section)

    def test_git_discovery_scopes_personal_work_to_resolved_identity(self) -> None:
        discovery_section = self._section("Discover Contributions From Git History")
        self.assertIn(
            "Filter candidate commits to the resolved Git identity before clustering",
            discovery_section,
        )
        self.assertIn("personal candidate work", discovery_section)
        self.assertIn("separately attributed context", discovery_section)

    def test_final_document_has_resume_narratives_and_question_sets(self) -> None:
        output_section = self._section("Build the Final Document")
        for phrase in (
            "Internship Output Overview",
            "Business Function and User Value",
            "Code Path",
            "technical difficulties",
            "Resume Wording",
            "30-second",
            "1-minute",
            "3-minute",
            "about 20 core interview questions",
            "reference answer",
            "likely follow-ups",
            "follow-up answer direction",
            "scenario questions",
            "scenario response framework",
            "strongest 3-5",
            "concise appendix",
            "Evidence Index",
        ):
            self.assertIn(phrase, output_section)

    def test_role_guides_do_not_add_question_gates(self) -> None:
        role_guides = sorted(
            path
            for path in (SKILL_DIR / "references").glob("role-*.md")
            if path.name not in {"role-analysis-framework.md", "role-classification.md"}
        )
        self.assertEqual(7, len(role_guides))
        for guide in role_guides:
            text = guide.read_text(encoding="utf-8")
            self.assertIn("main consolidated confirmation process", text, guide.name)
            self.assertIn("does not add confirmation rounds", text, guide.name)
            self.assertNotRegex(text, r"(?im)^Ask\b", guide.name)
            self.assertNotRegex(text, r"(?i)ask[^.]*Git identity", guide.name)

    def _assert_deep_role_guide(self, filename: str, markers: tuple[str, ...]) -> None:
        text = (SKILL_DIR / "references" / filename).read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        self.assertGreaterEqual(line_count, 120, filename)
        self.assertLessEqual(line_count, 180, filename)
        for heading in ROLE_REQUIRED_HEADINGS:
            self.assertIn(heading, text, filename)
        for marker in markers:
            self.assertIn(marker, text, filename)
        self.assertIn("main consolidated confirmation process", text, filename)
        self.assertIn("does not add confirmation rounds", text, filename)
        self.assertNotRegex(text, r"(?im)^Ask\b", filename)
        self.assertNotRegex(text, r"(?i)ask[^.]*Git identity", filename)

    def test_frontend_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-frontend.md",
            (
                "request race",
                "rendering boundary",
                "accessibility tree",
                "Core Web Vitals",
                "design-system",
                "end-to-end user flow",
            ),
        )
        text = (SKILL_DIR / "references" / "role-frontend.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Design-system component: consumer -> shared primitive -> token or style -> "
            "browser visual-regression test boundary.",
            text,
        )

    def test_backend_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-backend.md",
            (
                "idempotency",
                "transaction boundary",
                "cache invalidation",
                "message delivery",
                "authorization policy",
                "observability",
            ),
        )
        text = (SKILL_DIR / "references" / "role-backend.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Read/cache hit: cache hit -> response -> contract/integration test "
            "boundary.",
            text,
        )
        self.assertIn(
            "Read/cache miss: cache miss -> repository read -> optional cache fill -> "
            "response -> contract/integration test boundary.",
            text,
        )
        self.assertIn(
            "Repository failure: repository read -> mapped error response -> "
            "contract/integration test boundary.",
            text,
        )

    def test_client_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-client.md",
            (
                "lifecycle transition",
                "offline queue",
                "weak-network",
                "thread confinement",
                "resource pressure",
                "platform adaptation",
            ),
        )

    def test_testing_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-testing.md",
            (
                "risk model",
                "test pyramid",
                "fixture isolation",
                "flaky-test",
                "mutation testing",
                "release gate",
            ),
        )

    def test_role_classification_uses_the_main_confirmation_process(self) -> None:
        text = (SKILL_DIR / "references" / "role-classification.md").read_text(encoding="utf-8")
        self.assertIn("main consolidated confirmation process", text)
        self.assertIn("does not add confirmation rounds", text)
        self.assertNotRegex(text, r"(?im)^Ask\\b")

    def test_skill_loads_shared_role_framework_and_bounds_cross_role_context(self) -> None:
        section = self._section("Supporting Analysis References")
        for phrase in (
            "role analysis framework",
            "one primary role guide",
            "at most one secondary role guide",
            "direct cross-role evidence",
        ):
            self.assertIn(phrase, section)

    def test_role_analysis_framework_maps_evidence_to_career_material(self) -> None:
        text = ROLE_FRAMEWORK_PATH.read_text(encoding="utf-8")
        for heading in (
            "## Evidence Chain",
            "## Decision Reconstruction",
            "## Technical Depth",
            "## Evidence Classification",
            "## Career Material Mapping",
            "## Interview Question Tree",
            "## Cross-Role Boundary",
            "## Degradation Rules",
        ):
            self.assertIn(heading, text)
        lowered = text.lower()
        for phrase in (
            "entry point",
            "alternative",
            "failure mode",
            "validation evidence",
            "basic implementation",
            "system-level improvement",
            "resume",
            "scenario",
            "one secondary role guide",
            "last supported node",
        ):
            self.assertIn(phrase, lowered)

    def test_role_classification_selects_one_primary_and_at_most_one_secondary(self) -> None:
        text = (SKILL_DIR / "references" / "role-classification.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("exactly one primary role guide", text)
        self.assertIn("at most one secondary role guide", text)
        self.assertIn("direct cross-role evidence", text)
        self.assertIn("target role remains the organizing perspective", text)

    def test_output_is_the_single_explicit_workspace_write(self) -> None:
        for phrase in (
            "current writable workspace",
            "only explicit allowed workspace write",
            "Repository source and Git state remain read-only",
        ):
            self.assertIn(phrase, self.body)

    def test_confidence_levels_are_defined_without_the_retired_evidence_model(self) -> None:
        for phrase in (
            "high = direct source/Git/test evidence for the exact claim",
            "medium = multiple consistent static observations with an explicit runtime/outcome boundary",
            "low = tentative interpretation that stays out of resume wording and is marked needs user input",
        ):
            self.assertIn(phrase, self.body)

    def test_only_runtime_artifact_is_the_final_markdown(self) -> None:
        self.assertIn("career-output/实习产出与面试准备.md", self.body)
        self.assertIn("only file artifact", self.body)
        self.assertIn("Keep working notes in memory", self.body)
        for artifact in LEGACY_ARTIFACTS:
            self.assertNotIn(artifact, self.body)

    def test_evidence_rules_forbid_invented_metrics_and_unsafe_execution(self) -> None:
        safety = self._section("Evidence and Safety Rules")
        for phrase in (
            "read-only",
            "Never execute target-repository code",
            "Never invent metrics",
            "needs user input",
            "redact secrets",
        ):
            self.assertIn(phrase, safety)

    def test_skill_navigates_directly_to_retained_analysis_and_role_references(self) -> None:
        for link in REQUIRED_REFERENCE_LINKS:
            self.assertIn(link, self.body)

    def test_metadata_supports_implicit_invocation_and_names_the_skill(self) -> None:
        metadata = METADATA_PATH.read_text(encoding="utf-8")
        self.assertIn('display_name: "Internship Work Summary"', metadata)
        self.assertIn("$summarizing-internship-work", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertNotRegex(metadata, r"[锟鐠閻濞闁]")

    def _section(self, heading: str) -> str:
        match = re.search(
            rf"(?ms)^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
            self.body,
        )
        if not match:
            self.fail(f"missing section: {heading}")
        return match.group("body")


if __name__ == "__main__":
    unittest.main()
