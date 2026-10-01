# Download Status

Step 2 of the [research plan](../isolation_research_plan.md), run on 2026-10-01.
All 103 sources in `sources.csv` (P-001..P-058, R-001..R-034, S-001..S-011) were attempted once.

## Counts

- Fetched OK: 99
- Flagged (clean text below 1,500 chars): 4 (P-038, P-045, S-002, S-004). Details in `manual_check.md`.
- Flagged for other reasons (HTTP error, robots.txt, known-bad domain, PDF garbage): 0
- Excluded for licensing: 0 (every source has `license_status` `ok`)

## Notes

- `sources.csv` was generated once by `../scripts/md_to_csv.py`; it refuses to overwrite without `--force`. Edit the CSV directly from now on.
- S-004: the URL cell in `sources.md` held three URLs. The CSV keeps the CISA URL; the Canadian HTML and Australian PDF copies are in `license_note`. The CISA page yields only 607 chars.
- URL rewrites: arXiv URLs fetch the PDF, GitHub repo and blob URLs fetch the raw README or file, Hacker News items use the Algolia API (thread as JSON, comments flattened), the CVE record is stored as JSON.

## How to Re-run

From `isolation_research/`:

```sh
.venv/bin/python scripts/fetch_sources.py                 # fetch anything not yet in corpus/
.venv/bin/python scripts/fetch_sources.py --ids S-004     # only selected IDs
.venv/bin/python scripts/fetch_sources.py --normalize-only --ids P-038   # after placing corpus/P-038/raw.pdf or raw.html
```

To re-download a source, delete `corpus/<ID>/` first; the `changed` column in `manifest.csv` then shows whether its hash differs. Thresholds: `--min-chars`, `--min-word-ratio`, `--delay`, `--timeout`, `--retries`, `--bad-domains`.

## Unfinished

- Manual downloads for the 4 flagged sources (see `manual_check.md`).
- The venv is at `isolation_research/.venv` (gitignored); recreate with `python3 -m venv .venv && .venv/bin/pip install trafilatura pymupdf requests`.
