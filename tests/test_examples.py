import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_artifacts  # noqa: E402

EXAMPLE = ROOT / "examples" / "cli-notes"
BEFORE, AFTER = EXAMPLE / "before", EXAMPLE / "after"


def read(base, rel):
    return (base / rel).read_text(encoding="utf-8")


class ExamplesTest(unittest.TestCase):
    def test_examples_are_consistent(self):
        for tree in (BEFORE, AFTER):
            with self.subTest(tree=tree.name):
                self.assertTrue(tree.is_dir(), f"{tree} missing")
                self.assertEqual(check_artifacts.check(tree), [])

    def test_before_has_all_documents(self):
        for rel in ("vision.md", "roadmap.md", "architecture.md", "adr/ADR-001-storage.md", "todo/M1.md"):
            self.assertTrue((BEFORE / rel).is_file(), rel)
        self.assertIn("[done]", read(BEFORE, "todo/M1.md"))

    def test_after_contains_each_change_kind(self):
        self.assertNotIn("**V-4**", read(BEFORE, "vision.md"))
        self.assertIn("**V-4**", read(AFTER, "vision.md"))  # added
        self.assertIn("version: 2", read(AFTER, "roadmap.md"))  # changed
        self.assertIn("## Changelog", read(AFTER, "roadmap.md"))
        self.assertRegex(read(AFTER, "roadmap.md"), r"\*\*R-M1-3\*\* \[dropped\].*\(reason: ")  # removed
        self.assertRegex(read(AFTER, "todo/M1.md"), r"\*\*T-M1-3\*\* \[dropped\].*\(reason: ")
        self.assertIn("status: superseded", read(AFTER, "adr/ADR-001-storage.md"))  # superseded
        self.assertIn("superseded_by: ADR-002", read(AFTER, "adr/ADR-001-storage.md"))
        self.assertTrue((AFTER / "adr/ADR-002-sqlite.md").is_file())

    def test_superseded_adr_body_is_unchanged(self):
        def body(base):
            return read(base, "adr/ADR-001-storage.md").split("---", 2)[2]

        self.assertEqual(body(BEFORE), body(AFTER))

    def test_change_scenario_has_impact_table(self):
        text = read(EXAMPLE, "change-scenario.md")
        for word in ("keep", "rework", "discard"):
            self.assertRegex(text, rf"(?i)\b{word}\b")
        for item_id in ("V-4", "R-M1-2", "R-M1-3", "ADR-001"):
            self.assertIn(item_id, text)
        self.assertTrue(re.search(r"\|.*\|", text))


if __name__ == "__main__":
    unittest.main()
