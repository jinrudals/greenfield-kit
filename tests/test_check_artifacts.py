import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_artifacts  # noqa: E402


def doc(status="approved", version=1, inputs=None, body=""):
    fm = f"---\nversion: {version}\nstatus: {status}\n"
    if inputs is not None:
        fm += f"inputs: [{', '.join(inputs)}]\n"
    return fm + "---\n\n" + body


def adr(status="accepted", superseded_by=None):
    fm = f"---\nversion: 1\nstatus: {status}\n"
    if superseded_by:
        fm += f"superseded_by: {superseded_by}\n"
    return fm + "---\n\n# decision\n"


class CheckArtifactsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="")
        return p

    def valid_tree(self):
        self.write("vision.md", doc(body="- **V-1** solve it\n"))
        self.write("roadmap.md", doc(inputs=["vision"], body="- **R-M1-1** first flow; refs: V-1\n"))
        self.write("todo/M1.md", doc(inputs=["roadmap"], body="- **T-M1-1** [pending] build; refs: R-M1-1\n"))

    def errors(self):
        return check_artifacts.check(self.root)

    def test_valid_tree_has_no_errors(self):
        self.valid_tree()
        self.write("adr/ADR-001-db.md", adr())
        self.assertEqual(self.errors(), [])

    def test_missing_frontmatter_reports_not_crashes(self):
        self.write("vision.md", "\ufeff---\r\nversion: 1\r\nstatus: approved\r\n---\r\n- **V-1** ok\r\n")
        self.write("roadmap.md", "")
        self.write("todo/M1.md", "no frontmatter at all\n")
        errors = self.errors()
        self.assertEqual([e for e in errors if e.startswith("vision.md")], [])
        self.assertTrue(any(e.startswith("roadmap.md") and "frontmatter" in e for e in errors), errors)
        self.assertTrue(any(e.startswith("todo/M1.md") and "frontmatter" in e for e in errors), errors)

    def test_bad_version_or_status(self):
        self.write("vision.md", "---\nversion: one\nstatus: final\n---\n")
        errors = self.errors()
        self.assertTrue(any("version" in e for e in errors), errors)
        self.assertTrue(any("status" in e for e in errors), errors)

    def test_duplicate_id(self):
        self.write("vision.md", doc(body="- **V-1** a\n- **V-1** b\n"))
        self.assertTrue(any("duplicate" in e and "V-1" in e for e in self.errors()))

    def test_malformed_id(self):
        self.write("vision.md", doc(body="- **X-9** nope\n"))
        self.assertTrue(any("X-9" in e and "ID" in e for e in self.errors()))

    def test_dangling_ref(self):
        self.valid_tree()
        self.write("todo/M1.md", doc(inputs=["roadmap"], body="- **T-M1-1** build; refs: R-M1-9\n"))
        self.assertTrue(any("R-M1-9" in e and "unknown" in e for e in self.errors()))

    def test_approved_doc_with_draft_input(self):
        self.write("vision.md", doc(status="draft", body="- **V-1** a\n"))
        self.write("roadmap.md", doc(inputs=["vision"], body="- **R-M1-1** x; refs: V-1\n"))
        self.assertTrue(any(e.startswith("roadmap.md") and "vision" in e and "approved" in e for e in self.errors()))

    def test_approved_doc_with_missing_input(self):
        self.write("roadmap.md", doc(inputs=["vision"], body="- **R-M1-1** x\n"))
        self.assertTrue(any(e.startswith("roadmap.md") and "vision" in e and "missing" in e for e in self.errors()))

    def test_dropped_without_reason(self):
        self.write("vision.md", doc(body="- **V-1** [dropped] gone\n"))
        self.assertTrue(any("V-1" in e and "reason" in e for e in self.errors()))

    def test_dropped_with_reason_ok(self):
        self.write("vision.md", doc(body="- **V-1** [dropped] gone (reason: out of scope)\n"))
        self.assertEqual(self.errors(), [])

    def test_todo_references_dropped_roadmap_item(self):
        self.valid_tree()
        self.write("roadmap.md", doc(inputs=["vision"], body="- **R-M1-1** [dropped] first flow (reason: cut); refs: V-1\n"))
        errors = self.errors()
        self.assertTrue(any("T-M1-1" in e and "R-M1-1" in e and "dropped" in e for e in errors), errors)

    def test_dropped_todo_may_reference_dropped_roadmap_item(self):
        self.valid_tree()
        self.write("roadmap.md", doc(inputs=["vision"], body="- **R-M1-1** [dropped] f (reason: cut); refs: V-1\n"))
        self.write("todo/M1.md", doc(inputs=["roadmap"], body="- **T-M1-1** [dropped] b (reason: cut); refs: R-M1-1\n"))
        self.assertEqual(self.errors(), [])

    def test_superseded_adr_missing_target(self):
        self.write("adr/ADR-001-db.md", adr(status="superseded", superseded_by="ADR-002"))
        self.assertTrue(any("ADR-001" in e and "ADR-002" in e for e in self.errors()))

    def test_superseded_adr_without_target_field(self):
        self.write("adr/ADR-001-db.md", adr(status="superseded"))
        self.assertTrue(any("ADR-001" in e and "superseded_by" in e for e in self.errors()))

    def test_supersede_cycle(self):
        self.write("adr/ADR-001-a.md", adr(status="superseded", superseded_by="ADR-002"))
        self.write("adr/ADR-002-b.md", adr(status="superseded", superseded_by="ADR-001"))
        self.assertTrue(any("cycle" in e for e in self.errors()))

    def test_missing_or_empty_root_is_an_error(self):
        missing = check_artifacts.check(self.root / "nope")
        self.assertTrue(any("not a directory" in e for e in missing), missing)
        self.assertTrue(any("no Markdown" in e for e in self.errors()))

    def test_status_tag_typos_are_reported(self):
        for tag in ("[in-progress]", "[in progress]", "[droped]"):
            with self.subTest(tag=tag):
                self.write("vision.md", doc(body=f"- **V-1** {tag} text\n"))
                self.assertTrue(any("V-1" in e and "status" in e for e in self.errors()), tag)

    def test_double_space_before_dropped_still_requires_reason(self):
        self.write("vision.md", doc(body="- **V-1**  [dropped] gone\n"))
        self.assertTrue(any("V-1" in e and "reason" in e for e in self.errors()))

    def test_refs_tolerate_punctuation_and_still_resolve(self):
        self.valid_tree()
        for ref in ("R-M1-9.", "`R-M1-9`", "R-M1-9 - see note", "R-M1-1, R-M1-9"):
            with self.subTest(ref=ref):
                self.write("todo/M1.md", doc(inputs=["roadmap"], body=f"- **T-M1-1** build; refs: {ref}\n"))
                self.assertTrue(any("R-M1-9" in e and "unknown" in e for e in self.errors()), ref)

    def test_comma_between_refs_and_deps_checks_both(self):
        self.valid_tree()
        self.write("todo/M1.md", doc(inputs=["roadmap"], body="- **T-M1-1** build; refs: R-M1-8, deps: T-M1-9\n"))
        errors = self.errors()
        self.assertTrue(any("R-M1-8" in e for e in errors), errors)
        self.assertTrue(any("T-M1-9" in e for e in errors), errors)

    def test_refs_without_any_valid_id(self):
        self.valid_tree()
        self.write("todo/M1.md", doc(inputs=["roadmap"], body="- **T-M1-1** build; refs: R-M1\n"))
        self.assertTrue(any("T-M1-1" in e and "no valid ID" in e for e in self.errors()))

    def test_duplicate_adr_number(self):
        self.write("adr/ADR-003-cache.md", adr())
        self.write("adr/ADR-003-auth.md", adr())
        self.assertTrue(any("duplicate" in e and "ADR-003" in e for e in self.errors()))

    def test_adr_number_must_be_three_digits(self):
        self.write("adr/ADR-0001-x.md", adr())
        self.assertTrue(any("ADR-0001-x.md" in e for e in self.errors()))


if __name__ == "__main__":
    unittest.main()
