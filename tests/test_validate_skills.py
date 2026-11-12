import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate_skills  # noqa: E402

GOOD = "---\nname: {name}\ndescription: does a thing\n---\n\n# body\n"


def make_skill(root, name, text=None, dirname=None):
    d = Path(root) / (dirname or name)
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(GOOD.format(name=name) if text is None else text, encoding="utf-8")
    return d


class ValidateSkillsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_valid_skill_passes(self):
        make_skill(self.root, "greenfield-vision")
        self.assertEqual(validate_skills.validate(self.root), [])

    def test_name_must_match_directory(self):
        make_skill(self.root, "greenfield-roadmap", dirname="greenfield-vision")
        errors = validate_skills.validate(self.root)
        self.assertTrue(any("does not match directory" in m for _, m in errors))

    def test_missing_description_fails(self):
        make_skill(self.root, "greenfield-vision", text="---\nname: greenfield-vision\n---\n")
        errors = validate_skills.validate(self.root)
        self.assertTrue(any("description" in m for _, m in errors))

    def test_disallowed_name_fails(self):
        for i, name in enumerate(["greenfield_vision", "greenfield", "Greenfield-Vision", "other-skill"]):
            with self.subTest(name=name):
                sub = self.root / str(i)
                sub.mkdir()
                make_skill(sub, name)
                errors = validate_skills.validate(sub)
                self.assertTrue(any("not allowed" in m or "lowercase" in m for _, m in errors), errors)

    def test_allowed_names_pass(self):
        for name in ["using-greenfield", "greenfield-vision"]:
            with self.subTest(name=name):
                sub = self.root / name
                sub.mkdir()
                make_skill(sub, name)
                self.assertEqual(validate_skills.validate(sub), [])

    def test_bom_and_crlf_frontmatter_parsed(self):
        text = "\ufeff---\r\nname: greenfield-vision\r\ndescription: ok\r\n---\r\nbody\r\n"
        fm = validate_skills.parse_frontmatter(text)
        self.assertEqual(fm["name"], "greenfield-vision")
        self.assertEqual(fm["description"], "ok")

    def test_template_requires_version_and_status(self):
        d = make_skill(self.root, "greenfield-vision")
        (d / "templates").mkdir()
        (d / "templates" / "x.md").write_text("---\nversion: 1\n---\n", encoding="utf-8")
        errors = validate_skills.validate(self.root)
        self.assertTrue(any("x.md" in str(p) and "status" in m for p, m in errors), errors)


if __name__ == "__main__":
    unittest.main()
