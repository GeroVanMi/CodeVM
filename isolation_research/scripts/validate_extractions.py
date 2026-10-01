#!/usr/bin/env python3
"""Validate Step 3 extraction records (sources/extractions/<ID>.yaml).

Checks each record against extraction/schema.json (with tag enums filled from
extraction/vocabulary.yaml) and confirms every `quote` appears in
sources/corpus/<ID>/clean.md after normalization (whitespace, quote characters,
dashes, ligatures, soft hyphens, PDF line-break hyphenation).

Usage:
  validate_extractions.py                     # all records
  validate_extractions.py --ids P-001 R-007   # selected records
  validate_extractions.py --record F --clean C  # one file pair (tests/driver)
  validate_extractions.py --sync-schema       # write vocabulary enums into schema.json

Exit status: 0 if all valid, 1 if any record failed, 2 on usage errors.
Requires: pyyaml, jsonschema.
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
EXTRACTION = ROOT / "extraction"
SOURCES = ROOT / "sources"
VOCAB_SECTIONS = {"practice_tag": "practice_tags", "threat_tag": "threat_tags",
                  "evidence_type": "evidence_types", "author_role": "author_roles"}

_CHAR_MAP = {
    **{c: '"' for c in "“”„‟«»″〝〞"},
    **{c: "'" for c in "‘’‚‛‹›′`´"},
    **{c: "-" for c in "‐‑‒–—―−⁃﹘﹣－"},
    "…": "...", " ": " ", " ": " ", " ": " ",
    "­": "", "​": "", "‌": "", "‍": "", "﻿": "",
}
_TRANS = str.maketrans(_CHAR_MAP)
_ELLIPSIS = re.compile(r"\s*(?:\.\.\.|\[\.\.\.\])\s*")


def normalize(text: str) -> str:
    """Normalize text so verbatim quotes survive PDF/HTML extraction quirks."""
    text = unicodedata.normalize("NFKC", text)  # ligatures (fi, fl), full-width forms
    text = text.translate(_TRANS)
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)  # "exam-\nple" -> "example"
    text = re.sub(r"[*_`]+", "", text)  # markdown emphasis/code markers
    text = re.sub(r"\s+", " ", text)
    return text.strip()


_HYPH = re.compile(r"(?<=\w)- ?(?=\w)")


def quote_in(quote: str, norm_clean: str) -> bool:
    """Exact normalized match, falling back to a hyphen-insensitive match
    (PDF line breaks make "allow-lists"/"allowlists" ambiguous)."""
    return _quote_in(quote, norm_clean) or _quote_in(_HYPH.sub("", quote), _HYPH.sub("", norm_clean))


def _quote_in(quote: str, norm_clean: str) -> bool:
    """True if quote occurs in normalized clean text. An ellipsis ("..." or
    "[...]") splits the quote into fragments that must appear in order."""
    q = normalize(quote)
    if not q:
        return False
    pos = 0
    for frag in (f.strip() for f in _ELLIPSIS.split(q)):
        if not frag:
            continue
        i = norm_clean.find(frag, pos)
        if i < 0:
            return False
        pos = i + len(frag)
    return True


def load_schema(schema_path=EXTRACTION / "schema.json", vocab_path=EXTRACTION / "vocabulary.yaml"):
    schema = json.loads(Path(schema_path).read_text())
    vocab = yaml.safe_load(Path(vocab_path).read_text())
    for d, section in VOCAB_SECTIONS.items():
        schema["$defs"][d]["anyOf"][0]["enum"] = sorted(vocab[section])
    return schema


def iter_quotes(rec):
    for i, r in enumerate(rec.get("recommendations") or []):
        if isinstance(r, dict) and "quote" in r:
            yield f"recommendations[{i}]", r["quote"]
    tm = rec.get("threat_model") or {}
    if isinstance(tm, dict):
        if isinstance(tm.get("framework"), dict):
            yield "threat_model.framework", tm["framework"].get("quote", "")
        for key in ("assets", "input_channels", "failure_modes"):
            for i, e in enumerate(tm.get(key) or []):
                if isinstance(e, dict) and "quote" in e:
                    yield f"threat_model.{key}[{i}]", e["quote"]


def validate_record(record_path, clean_path, validator, expected_id=None):
    """Return a list of error strings (empty if valid)."""
    try:
        rec = yaml.safe_load(Path(record_path).read_text())
    except Exception as e:  # noqa: BLE001
        return [f"YAML parse error: {e}"]
    if not isinstance(rec, dict):
        return ["record is not a mapping"]
    errors = [f"schema: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
              for e in sorted(validator.iter_errors(rec), key=lambda e: list(e.absolute_path))]
    if expected_id and rec.get("id") != expected_id:
        errors.append(f"id mismatch: record has {rec.get('id')!r}, expected {expected_id!r}")
    try:
        norm_clean = normalize(Path(clean_path).read_text(errors="replace"))
    except FileNotFoundError:
        return errors + [f"clean text missing: {clean_path}"]
    for where, q in iter_quotes(rec):
        if not isinstance(q, str) or not quote_in(q, norm_clean):
            errors.append(f"quote not found ({where}): {str(q)[:120]!r}")
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--record")
    ap.add_argument("--clean")
    ap.add_argument("--sync-schema", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    schema = load_schema()
    if a.sync_schema:
        (EXTRACTION / "schema.json").write_text(json.dumps(schema, indent=2) + "\n")
        print("schema.json enums synced from vocabulary.yaml")
        return 0
    validator = Draft202012Validator(schema)

    if a.record:
        if not a.clean:
            ap.error("--record needs --clean")
        pairs = [(Path(a.record).stem, Path(a.record), Path(a.clean))]
    else:
        recs = sorted((SOURCES / "extractions").glob("*.yaml"))
        if a.ids:
            recs = [p for p in recs if p.stem in set(a.ids)]
            missing = set(a.ids) - {p.stem for p in recs}
            for m in sorted(missing):
                print(f"{m}: no record")
        pairs = [(p.stem, p, SOURCES / "corpus" / p.stem / "clean.md") for p in recs]

    failed = 0
    for rid, rp, cp in pairs:
        errs = validate_record(rp, cp, validator, expected_id=None if a.record else rid)
        if errs:
            failed += 1
            print(f"{rid}: FAIL ({len(errs)})")
            for e in errs:
                print(f"  - {e}")
        elif not a.quiet:
            print(f"{rid}: ok")
    print(f"{len(pairs) - failed}/{len(pairs)} valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
