import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
sys.path.insert(0, str(ROOT / "scripts"))

import check_artifacts  # noqa: E402
VENDOR_TOOL_NAMES = ("AskUserQuestion", "ask_user", "TodoWrite")


def skill_text(name):
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class UsingGreenfieldTest(unittest.TestCase):
    def test_using_greenfield_has_shared_rules_and_routing(self):
        text = skill_text("using-greenfield")
        self.assertIn("## Shared interview rules", text)
        self.assertIn("## Stage detection", text)
        for name in (
            "greenfield-vision",
            "greenfield-roadmap",
            "greenfield-architecture",
            "greenfield-todo",
            "greenfield-change",
        ):
            self.assertIn(name, text)

    def test_no_vendor_tool_names(self):
        for path in SKILLS.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for tool in VENDOR_TOOL_NAMES:
                self.assertNotIn(tool, text, f"{path} mentions {tool}")


STAGE_SKILLS = ("greenfield-vision", "greenfield-roadmap", "greenfield-architecture", "greenfield-todo")
TEMPLATE_TARGETS = {
    "greenfield-vision/templates/vision.md": "vision.md",
    "greenfield-roadmap/templates/roadmap.md": "roadmap.md",
    "greenfield-architecture/templates/architecture.md": "architecture.md",
    "greenfield-architecture/templates/adr.md": "adr/ADR-001-example.md",
    "greenfield-todo/templates/todo.md": "todo/M1.md",
}


class StageSkillsTest(unittest.TestCase):
    def test_stage_skill_sections(self):
        for name in STAGE_SKILLS:
            text = skill_text(name)
            for heading in ("## Inputs", "## Interview", "## Output", "## Checklist"):
                with self.subTest(skill=name, heading=heading):
                    self.assertIn(heading, text)

    def test_stage_skill_defers_to_shared_rules(self):
        for name in STAGE_SKILLS:
            text = skill_text(name)
            with self.subTest(skill=name):
                self.assertIn("using-greenfield", text)
                self.assertNotIn("one question at a time", text.lower())

    def test_stage_skill_requires_approved_inputs(self):
        for name in ("greenfield-roadmap", "greenfield-architecture", "greenfield-todo"):
            with self.subTest(skill=name):
                self.assertIn("status: approved", skill_text(name))

    def test_templates_form_a_consistent_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            for src, dest in TEMPLATE_TARGETS.items():
                target = Path(tmp) / dest
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((SKILLS / src).read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(check_artifacts.check(Path(tmp)), [])


class ChangeSkillTest(unittest.TestCase):
    def test_change_skill_has_gate_and_conventions(self):
        text = skill_text("greenfield-change")
        for phrase in ("approval", "superseded_by", "[dropped]", "Changelog", "out of scope", "using-greenfield"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        for heading in ("## Inputs", "## Interview", "## Output", "## Checklist"):
            self.assertIn(heading, text)

    def test_impact_table_template_columns(self):
        text = (SKILLS / "greenfield-change/templates/impact-table.md").read_text(encoding="utf-8")
        header = next(line for line in text.splitlines() if line.startswith("|"))
        for word in ("keep", "rework", "discard"):
            self.assertIn(word, header.lower())


if __name__ == "__main__":
    unittest.main()
