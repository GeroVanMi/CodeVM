#!/usr/bin/env python3
"""One-time conversion of sources/sources.md tables into sources/sources.csv."""
import csv, re, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "sources"
COLS = ["id", "title", "author_org", "url", "date", "stream", "sub_stream", "harness",
        "rqs", "recommendation", "verification", "license_status", "license_note"]

def main():
    rows, stream, sub = [], "", ""
    for line in (SRC / "sources.md").read_text().splitlines():
        if line.startswith("## "):
            stream, sub = line[3:].strip(), ""
        elif line.startswith("### "):
            sub = line[4:].strip()
        elif re.match(r"^\|\s*[PRS]-\d{3}\s*\|", line):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            assert len(c) == 9, line
            rows.append(dict(id=c[0], title=c[1], author_org=c[2], url=c[3], date=c[4],
                             stream=stream, sub_stream=sub, harness=c[5], rqs=c[6],
                             recommendation=c[7], verification=c[8],
                             license_status="ok", license_note=""))
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate IDs"
    out = SRC / "sources.csv"
    if out.exists() and "--force" not in sys.argv:
        sys.exit(f"{out} exists; it is the source of truth now. Use --force to overwrite.")
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(rows)
    print(len(rows), "rows;", {p: sum(i.startswith(p) for i in ids) for p in "PRS"})

if __name__ == "__main__":
    main()
