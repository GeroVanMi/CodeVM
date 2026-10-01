# Download Status

Step 2 of the [research plan](../isolation_research_plan.md), run on 2026-10-01.
All 102 sources in `sources.csv` (P-001..P-058 without P-045, R-001..R-034, S-001..S-011) were attempted once. P-045 was removed deliberately (talk without written source).

## Counts

- OK after normalization: 102 (`manual_check.md` is empty)
- Flagged (clean text below 1,500 chars): 0. Previously flagged: P-038 (fixed by the embedded-JSON fallback), S-002 and S-004 (manual copies placed by the user, `changed` = yes in `manifest.csv`).
- Flagged for other reasons (HTTP error, robots.txt, known-bad domain, PDF garbage): 0
- Excluded for licensing: 0 (every source has `license_status` `ok`)

## Notes

- `sources.csv` was generated once by `../scripts/md_to_csv.py`; it refuses to overwrite without `--force`. Edit the CSV directly from now on.
- S-004: the URL cell in the former `sources.md` held three URLs. The CSV keeps the CISA URL; the Canadian HTML and Australian PDF copies are in `license_note`. The automatic CISA fetch yielded only 607 chars; the user placed a saved copy at `corpus/S-004/raw.html` (the `raw_files/` folder beside it is ignored), now about 62,000 chars.
- Extraction fallback: if trafilatura yields under 2,000 chars, the script takes the longest string from the page's embedded JSON (`__NEXT_DATA__`, JSON-LD, other `application/json` scripts) when it is over 3 times longer, and records `embedded-json` as `extraction_method`. Only P-038 (stripe.dev, client-rendered Next.js) uses it.
- For manually placed files, `fetch_date`, `http_status` and `final_url` stay as recorded by the original automatic fetch.
- Thin but full-text pages (about 1,700 to 1,900 chars): P-016, P-018, P-046, P-049, S-010.
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

- The venv is at `isolation_research/.venv` (gitignored); recreate with `python3 -m venv .venv && .venv/bin/pip install trafilatura pymupdf requests`.
