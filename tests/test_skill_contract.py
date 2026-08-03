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
DECISION_MATRIX_HEADER = (
    "| Decision | Evidence to inspect | Supported claim | Prohibited inference |"
)
CONSOLIDATED_CONFIRMATION_SENTENCE = (
    "Route material gaps through the main consolidated confirmation process; this guide "
    "does not add confirmation rounds or request Git identity for a named-feature route."
)
ROLE_MARKERS = {
    "role-frontend.md": (
        "request race",
        "rendering boundary",
        "accessibility tree",
        "Core Web Vitals",
        "design-system",
        "end-to-end user flow",
    ),
    "role-backend.md": (
        "idempotency",
        "transaction boundary",
        "cache invalidation",
        "message delivery",
        "authorization policy",
        "observability",
    ),
    "role-client.md": (
        "lifecycle transition",
        "offline queue",
        "weak-network",
        "thread confinement",
        "resource pressure",
        "platform adaptation",
    ),
    "role-testing.md": (
        "risk model",
        "test pyramid",
        "fixture isolation",
        "flaky-test",
        "mutation testing",
        "release gate",
    ),
    "role-devops.md": (
        "artifact provenance",
        "environment parity",
        "progressive delivery",
        "rollback trigger",
        "least privilege",
        "recovery objective",
    ),
    "role-data-analytics.md": (
        "metric grain",
        "late-arriving data",
        "slowly changing dimension",
        "data lineage",
        "experiment bias",
        "dashboard consumer",
    ),
    "role-algorithm.md": (
        "label leakage",
        "baseline",
        "offline evaluation",
        "online experiment",
        "model drift",
        "inference budget",
    ),
}

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
    "[Git evidence collector](scripts/collect_git_evidence.py)",
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


def read_level_two_headings(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"(?m)^##[ \t].*$", text))


def find_marker_sections(
    text: str, markers: tuple[str, ...]
) -> dict[str, tuple[str, ...]]:
    heading_matches = list(re.finditer(r"(?m)^(##[ \t].*)$", text))
    sections: dict[str, str] = {}
    for index, match in enumerate(heading_matches):
        heading = match.group(1)
        if heading not in ROLE_REQUIRED_HEADINGS:
            continue
        end = (
            heading_matches[index + 1].start()
            if index + 1 < len(heading_matches)
            else len(text)
        )
        sections[heading] = text[match.end() : end]
    return {
        marker: tuple(
            heading for heading, body in sections.items() if marker in body
        )
        for marker in markers
    }


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SKILL_PATH.read_text(encoding="utf-8")
        cls.frontmatter, cls.body = read_frontmatter(cls.text)

    def test_level_two_heading_reader_accepts_space_and_tab_separators(self) -> None:
        text = "## Space heading\n##\tTab heading\n"
        self.assertEqual(
            ("## Space heading", "##\tTab heading"),
            read_level_two_headings(text),
        )

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

    def test_named_feature_personal_output_uses_user_provided_attribution(self) -> None:
        feature_section = self._section("Trace a Named Feature")
        for phrase in (
            "personal resume, internship summary, or personal output",
            "fully implemented by the user",
            "user-provided evidence",
            "Do not check commit authorship",
        ):
            self.assertIn(phrase, feature_section)

    def test_implementation_only_feature_analysis_does_not_claim_ownership(self) -> None:
        feature_section = self._section("Trace a Named Feature")
        self.assertIn("only asks how the feature works", feature_section)
        self.assertIn("do not infer personal ownership", feature_section)

    def test_git_discovery_uses_the_collector_through_stdout(self) -> None:
        discovery_section = self._section("Discover Contributions From Git History")
        for phrase in (
            "contributors",
            "collect",
            "--output -",
            "consume stdout in memory",
            "aliases",
            "Co-authored-by",
            "repeated --author",
            "--max-commits 500",
            "--sensitivity internal",
            "--sensitivity public",
            "exit code 2",
            "exit code 3",
            "exit code 4",
            "exit code 5",
        ):
            self.assertIn(phrase.casefold(), discovery_section.casefold())

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
            "in-memory evidence matrix",
            "Detailed question",
            "Interview intent",
            "Code evidence",
            "Reasoning process",
            "Detailed first-person answer",
            "Design trade-offs",
            "Failure and validation analysis",
            "2-4 deep follow-up questions",
            "Complete follow-up answers",
            "Evidence boundary",
            "at least one concrete evidence anchor",
            "merge duplicate questions",
            "final quality audit",
            "separate set of 3-5 scenario questions",
            "strongest 3 major outputs by default",
            "up to 5 only when the user explicitly requests a comprehensive summary",
            "fewer than 20",
            "evidence is insufficient",
            "never pad or fabricate",
            "concise appendix",
            "Evidence Index",
        ):
            self.assertIn(phrase, output_section)
        for retired_phrase in (
            "concise reference answer",
            "follow-up answer direction",
            "scenario response framework",
        ):
            self.assertNotIn(retired_phrase, output_section)
        self.assertNotRegex(
            output_section,
            r"(?i)\b\d[\d,]*\+?\s+(?:total\s+)?(?:lines?|words?|characters?|pages?|tokens?)\b",
        )

    def test_existing_final_document_is_updated_without_silent_replacement(self) -> None:
        output_section = self._section("Build the Final Document")
        for phrase in (
            "If the final document already exists",
            "update matching outputs",
            "preserve unrelated verified material",
            "Replace the entire document only when the user explicitly requests a rebuild",
        ):
            self.assertIn(phrase, output_section)

    def test_interview_reference_separates_core_and_scenario_questions(self) -> None:
        text = (SKILL_DIR / "references" / "interview-expansion.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "in-memory evidence matrix",
            "Detailed question",
            "Interview intent",
            "Code evidence",
            "Reasoning process",
            "Detailed first-person answer",
            "Design trade-offs",
            "Failure and validation analysis",
            "2-4 deep follow-up questions",
            "Complete follow-up answers",
            "Evidence boundary",
            "at least one concrete evidence anchor",
            "merge duplicate questions",
            "final quality audit",
            "separate set of 3-5 scenario questions",
            "fewer than 20",
            "evidence is insufficient",
            "never pad or fabricate",
        ):
            self.assertIn(phrase, text)
        for retired_phrase in (
            "concise reference answer",
            "follow-up answer direction",
            "scenario response framework",
        ):
            self.assertNotIn(retired_phrase, text)
        self.assertNotRegex(
            text,
            r"(?i)\b\d[\d,]*\+?\s+(?:total\s+)?(?:lines?|words?|characters?|pages?|tokens?)\b",
        )

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
            if guide.name in {"role-client.md", "role-testing.md"}:
                self.assertIn(CONSOLIDATED_CONFIRMATION_SENTENCE, text, guide.name)
            self.assertNotRegex(text, r"(?im)^Ask\b", guide.name)
            self.assertNotRegex(text, r"(?i)ask[^.]*Git identity", guide.name)

    def _assert_deep_role_guide(self, filename: str, markers: tuple[str, ...]) -> None:
        text = (SKILL_DIR / "references" / filename).read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        self.assertGreaterEqual(line_count, 120, filename)
        self.assertLessEqual(line_count, 180, filename)
        headings = read_level_two_headings(text)
        self.assertEqual(ROLE_REQUIRED_HEADINGS, headings, filename)
        self.assertIn(DECISION_MATRIX_HEADER, text, filename)
        for marker in markers:
            self.assertIn(marker, text, filename)
        marker_sections = find_marker_sections(text, markers)
        for marker, sections in marker_sections.items():
            self.assertTrue(
                sections,
                f"{filename}: {marker!r} is outside the required H2 sections",
            )
        covered_sections = {
            section for sections in marker_sections.values() for section in sections
        }
        self.assertGreaterEqual(
            len(covered_sections),
            4,
            f"{filename}: role markers must span at least four required H2 sections; "
            f"marker locations: {marker_sections!r}",
        )
        self.assertIn("main consolidated confirmation process", text, filename)
        self.assertIn("does not add confirmation rounds", text, filename)
        self.assertNotRegex(text, r"(?im)^Ask\b", filename)
        self.assertNotRegex(text, r"(?i)ask[^.]*Git identity", filename)

    def test_frontend_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-frontend.md",
            ROLE_MARKERS["role-frontend.md"],
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
            ROLE_MARKERS["role-backend.md"],
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
            ROLE_MARKERS["role-client.md"],
        )

    def test_testing_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-testing.md",
            ROLE_MARKERS["role-testing.md"],
        )

    def test_devops_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-devops.md",
            ROLE_MARKERS["role-devops.md"],
        )
        text = (SKILL_DIR / "references" / "role-devops.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "Configured capability, execution evidence, and operational outcome "
            "are separate evidence layers.",
            text,
        )

    def test_data_analytics_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-data-analytics.md",
            ROLE_MARKERS["role-data-analytics.md"],
        )
        text = (SKILL_DIR / "references" / "role-data-analytics.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "SQL behavior, metric semantics, data-quality evidence, and "
            "business-decision evidence are separate evidence layers.",
            text,
        )

    def test_algorithm_guide_has_role_specific_depth(self) -> None:
        self._assert_deep_role_guide(
            "role-algorithm.md",
            ROLE_MARKERS["role-algorithm.md"],
        )

    def test_exactly_seven_distinct_deep_role_guides_exist(self) -> None:
        role_guides = sorted(
            path
            for path in (SKILL_DIR / "references").glob("role-*.md")
            if path.name not in {"role-analysis-framework.md", "role-classification.md"}
        )
        self.assertEqual(7, len(role_guides))
        self.assertEqual(set(ROLE_MARKERS), {guide.name for guide in role_guides})
        for guide in role_guides:
            self._assert_deep_role_guide(guide.name, ROLE_MARKERS[guide.name])

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
            "## Evidence Matrix",
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
            "at least one concrete evidence anchor",
            "merge duplicate questions",
            "complete follow-up answers",
            "final quality audit",
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

    def test_user_attribution_has_priority_without_expanding_feature_scope(self) -> None:
        safety = self._section("Evidence and Safety Rules")
        self.assertIn(
            "User-provided attribution supports ownership only for the named feature scope",
            safety,
        )
        references = self._section("Supporting Analysis References")
        self.assertIn(
            "Role-guide ownership guardrails must accept that user-provided attribution",
            references,
        )
        self.assertIn("adjacent components, team outcomes, or business impact", references)

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
