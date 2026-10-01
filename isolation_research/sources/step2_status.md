# Step 2 Status

Date: 2026-10-01. Step 2 extraction table written to the Notion database
"Related Work" (data source collection://3eca10ae-0ad1-80b4-8971-000b53b6f3b8).

## Progress

- Rows written: 103 of 103 (P-001 to P-058, R-001 to R-034, S-001 to S-011).
- Last ID done: S-011. Nothing left to resume for the Step 2 extraction.
- The table was empty before writing; no duplicates were created.
- Notion calls used: about 9 (fetch, schema update, empty-check query, 6 batch creates, 1 failed create that wrote nothing).

## Schema changes (the database had only the title "Name")

Added properties: Source ID, Author / org, Link (url), Date (text, because
many sources are "living" or approximate), Stream (select), Sub-stream
(select), Author role and incentives, Harness (multi-select), RQs
(multi-select), Threat addressed (multi-select), Recommendation, Evidence
type (select), Stated tradeoffs, Known bypasses or limits, Verification
status (select), Verification note. "Name" holds the source title.
Select values containing commas are not allowed, so verification values are
"Fetched", "Fetched undated", "Fetched abstract only", "Partly verified",
"Index only", "Snippet only", "Not read or unparsed".

## Notes on data quality

- "Author role and incentives", "Evidence type", and "Threat addressed" are
  inferred from sources.md summaries, not from full reading. P-024 evidence
  type is inferred.
- "not stated" means sources.md gives nothing; "unverified" means the source
  was not read well enough to say (P-012, P-031, P-044 to P-046, P-051, P-053,
  R-019, R-034, S-010, S-011).
- Harnesses outside the select list (Antigravity, Amazon Q, Claude Cowork)
  are mapped to "Other" with the name in the limits column.
- The default view only shows Name; columns are not hidden but view display
  properties were not changed.
