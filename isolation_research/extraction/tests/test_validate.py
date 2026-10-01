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
        self.assertEqual(v.normalize("allow-\nlists"), "allow-lists")
        self.assertEqual(v.normalize("per-domain"), "per-domain")
        self.assertTrue(v.quote_in("allow-lists", v.normalize("allow-\nlists")))
        self.assertTrue(v.quote_in("allowlists", v.normalize("allow-\nlists")))

    def test_hyphenated_compound_across_line_break(self):
        clean = v.normalize("clicking on AI- \n  generated links")
        self.assertTrue(v.quote_in("clicking on AI-generated links", clean))
        self.assertTrue(v._quote_in("clicking on AI-generated links", clean))  # exact, no fallback
        self.assertFalse(v.quote_in("clicking on AI generated links", clean))

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

    def test_new_optional_fields_absent_ok(self):
        r = copy.deepcopy(self.rec)
        for k in ("date_normalized", "contested_positions"):
            del r[k]
        for rec in r["recommendations"]:
            for k in ("qualifier", "claim_kind", "boundary_strength"):
                rec.pop(k, None)
        r["threat_model"]["framework"].pop("details")
        self.assertEqual(self.check(r), [])

    def test_bad_qualifier_and_fixed_lists_reject_other(self):
        r = copy.deepcopy(self.rec)
        r["recommendations"][0]["qualifier"] = "sometimes"
        r["recommendations"][1]["claim_kind"] = "other:anything"
        errs = self.check(r)
        self.assertTrue(any("recommendations/0/qualifier" in e for e in errs))
        self.assertTrue(any("recommendations/1/claim_kind" in e for e in errs))

    def test_bad_date_normalized(self):
        r = copy.deepcopy(self.rec); r["date_normalized"] = "living, accessed 2026-09-30"
        self.assertTrue(any("date_normalized" in e for e in self.check(r)))

    def test_empty_threats_ok(self):
        r = copy.deepcopy(self.rec); r["recommendations"][0]["threats"] = []
        self.assertEqual(self.check(r), [])

    def test_asset_and_channel_tags(self):
        r = copy.deepcopy(self.rec); del r["threat_model"]["assets"][0]["tag"]
        self.assertTrue(any("assets/0" in e and "tag" in e for e in self.check(r)))
        r = copy.deepcopy(self.rec); r["threat_model"]["input_channels"][0]["tag"] = "made-up"
        self.assertTrue(any("input_channels/0/tag" in e for e in self.check(r)))
        r["threat_model"]["input_channels"][0]["tag"] = "other:carrier-pigeon"
        self.assertEqual(self.check(r), [])

    def test_framework_value_short(self):
        r = copy.deepcopy(self.rec); r["threat_model"]["framework"]["value"] = "x" * 61
        self.assertTrue(any("framework" in e for e in self.check(r)))

    def test_contested_positions(self):
        r = copy.deepcopy(self.rec); r["contested_positions"][0]["topic"] = "made-up"
        self.assertTrue(any("contested_positions/0/topic" in e for e in self.check(r)))
        r = copy.deepcopy(self.rec); r["contested_positions"][1]["quote"] = "never said this"
        self.assertTrue(any("quote not found (contested_positions[1])" in e for e in self.check(r)))

    def test_broken_yaml(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write("id: [unclosed\n")
        self.assertTrue(v.validate_record(f.name, FIX / "clean.md", self.val)[0].startswith("YAML"))


if __name__ == "__main__":
    unittest.main()
