# Manual Check

Sources flagged by `scripts/fetch_sources.py`. Place a manual copy at
`corpus/<ID>/raw.pdf` (or `raw.html`) and re-run with `--normalize-only --ids <ID>`.

| ID | URL | Reason |
| --- | --- | --- |
| P-038 | https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents | clean text too short (235 < 1500 chars) |
| S-002 | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026 | clean text too short (1227 < 1500 chars) |
| S-004 | https://www.cisa.gov/resources-tools/resources/careful-adoption-agentic-ai-services | clean text too short (607 < 1500 chars) |
