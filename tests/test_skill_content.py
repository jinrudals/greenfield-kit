import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
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


if __name__ == "__main__":
    unittest.main()
