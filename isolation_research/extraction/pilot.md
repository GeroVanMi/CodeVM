# Step 3 pilot

Six varied sources, extracted with the strongest model before the full run.

| ID | Type | Title | Size (chars) | Why |
| --- | --- | --- | --- | --- |
| R-007 | Paper | Progent: Securing AI Agents with Privilege Control | 95,584 | Research defense with empirical evaluation; PDF text (ligatures, hyphenation) stresses the quote check. |
| P-002 | Vendor docs | Configure the sandboxed Bash tool (Anthropic) | 61,024 | Dense vendor documentation with many settings; states its own bypasses (domain fronting, Unix sockets); vendor incentives. |
| P-043 | Blog post | The agent harness belongs outside the sandbox | 10,987 | Short opinionated practitioner post on the boundary question (RQ2, RQ3). |
| P-026 | CVE write-up | CVE-2025-66479: Anthropic's Silent Fix and the CVE That Claude Code Never Got | 9,375 | Exploit/disclosure; tests `evidence_type` and `rejects` stances and `bypasses_limits`. |
| S-010 | Standard | AI Coding Assistants (joint ANSSI-BSI recommendations) | 46,520 | Government guidance specific to coding assistants; many recommendations; manual PDF copy. |
| R-017 | Long survey | A Systematic Survey of Security Threats and Defenses in LLM-based agents | 189,198 (~47k tokens) | Long survey; tests whole-file reading, threat-model extraction, and record size. |

## Run (inside the VM, from the repo checkout)

```sh
cd ~/projects/CodeVM/isolation_research
scripts/extract_driver.py --model claude-opus-5-5 --ids R-007 P-002 P-043 P-026 S-010 R-017
```

Then review the records in `sources/extractions/` (and `sources/extractions/failed/`,
`sources/manual_check.md`) as described in `README.md`.
