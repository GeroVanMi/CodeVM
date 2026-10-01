"""Run: .venv/bin/python -m unittest discover -s extraction/tests -v (from isolation_research/)."""
import copy, sys, tempfile, unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import validate_extractions as v  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

FIX = HERE / "fixtures"


class Normalizer(unittest.TestCase):
    def test_quotes_dashes_ligatures_whitespace(self):
        self.assertEqual(v.normalize("“a”  ‘b’\n—ﬁ…"), "\"a\" 'b' -fi...")

    def test_pdf_hyphenation(self):
        self.assertEqual(v.normalize("allow-\nlists"), "allowlists")
        self.assertEqual(v.normalize("per-domain"), "per-domain")
        self.assertTrue(v.quote_in("allow-lists", v.normalize("allow-\nlists")))

    def test_soft_hyphen_and_nbsp(self):
        self.assertEqual(v.normalize("se­cu rity"), "secu rity")

    def test_ellipsis_fragments_in_order(self):
        clean = v.normalize("one two three four")
        self.assertTrue(v.quote_in("one ... four", clean))
        self.assertFalse(v.quote_in("four ... one", clean))
        self.assertFalse(v.quote_in("   ", clean))


class Validator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.val = Draft202012Validator(v.load_schema())
        cls.rec = yaml.safe_load((FIX / "valid.yaml").read_text())

    def check(self, rec):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump(rec, f, allow_unicode=True)
        return v.validate_record(f.name, FIX / "clean.md", self.val, expected_id="P-999")

    def test_valid_fixture(self):
        self.assertEqual(v.validate_record(FIX / "valid.yaml", FIX / "clean.md", self.val, "P-999"), [])

    def test_bad_tag(self):
        r = copy.deepcopy(self.rec); r["recommendations"][0]["practice"] = "made-up"
        self.assertTrue(any("practice" in e for e in self.check(r)))

    def test_other_tag_ok(self):
        r = copy.deepcopy(self.rec); r["recommendations"][0]["practice"] = "other:nix-sandbox"
        self.assertEqual(self.check(r), [])

    def test_bad_stance_and_missing_field(self):
        r = copy.deepcopy(self.rec); r["recommendations"][0]["stance"] = "likes"; del r["extracted_by"]
        errs = self.check(r)
        self.assertTrue(any("stance" in e for e in errs))
        self.assertTrue(any("extracted_by" in e for e in errs))

    def test_fabricated_quote(self):
        r = copy.deepcopy(self.rec); r["threat_model"]["failure_modes"][0]["quote"] = "never said this"
        self.assertTrue(any("quote not found" in e for e in self.check(r)))

    def test_id_mismatch(self):
        r = copy.deepcopy(self.rec); r["id"] = "P-998"
        self.assertTrue(any("id mismatch" in e for e in self.check(r)))

    def test_broken_yaml(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write("id: [unclosed\n")
        self.assertTrue(v.validate_record(f.name, FIX / "clean.md", self.val)[0].startswith("YAML"))


if __name__ == "__main__":
    unittest.main()
