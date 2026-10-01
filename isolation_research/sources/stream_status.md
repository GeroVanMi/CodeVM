# Stream Status

State of Step 1 on 2026-10-01 (third session appended below). Original state on 2026-09-30: A first session covered the practitioner stream.
A second session covered the researcher and standards streams and stopped at
its budget of 60 searches and fetches (56 used). No broken entries from the
first session were found.

| Stream        | Sources kept | Stopping rule reached | Status                                           |
| ------------- | ------------ | --------------------- | ------------------------------------------------ |
| Practitioners | 57           | No                    | Searched; incidents still add new bypass classes (P-058 added in session 3; P-045 removed in Step 2) |
| Researchers   | 34           | No                    | Stopped at call budget twice; 2026 papers still add new mechanisms |
| Standards     | 11           | No                    | S-002 and S-004 read in session 3; S-008 (NCSC) added new recommendations |

## Practitioner Stream

57 sources (P-001 to P-057) from 84 logged queries and direct fetches, plus a
GitHub code search snapshot in
[search_log.md](search_log.md#observed-practice-snapshot).

The stopping rule was not reached. Of the last ten sources added, four still
brought a new recommendation or bypass:

- P-054: an allowlisted model-provider domain carried exfiltration using the
  attacker's own API key.
- P-057: the package-registry cache proxy, a permitted egress channel, was the
  escape route.
- P-056: an "offline" sandbox had live internet through misconfiguration, so
  every egress path needs validation.
- P-020: egress proxies can scan request bodies for secret patterns, with
  admitted DNS and encoding bypasses.

Sub-streams that look close to saturation: vendor documentation and reference
setups. The last several sources there repeat the same set: OS sandbox or VM,
default-deny egress with a domain allowlist, and credentials injected by a proxy
outside the boundary.

### Practitioner Gaps

- Reddit: the search API was blocked and site-restricted web search returned no
  threads. Not covered.
- Lobsters: no threads found through web search. Not covered.
- Observed practice: only aggregate code-search counts. No individual
  settings.json, devcontainer, or AGENTS.md files were read.
- Security firms: nothing relevant found from NCC Group for 2026. Invariant Labs
  is represented only by a 2025 post seen as a snippet.
- DEF CON 34 AI Village: no talk verified.
- Destructive actions (RQ6): only secondary coverage of the Claude Code rm -rf
  home directory incidents was found.
- Credential gateways seen on HN but not opened: OneCLI, Infisical Agent Vault,
  Zerobox, nah.

### Practitioner Sources to Revisit

- P-008 sandbox-runtime repo and issue tracker, not opened directly.
- P-018, P-031, P-051, P-053: snippet-only verification.
- P-026, P-028, P-046: index-only verification.
- P-044 Roblox slides: the PDF could not be parsed. Needs a text extraction.
- OpenAI incident post and technical report (HTTP 403), Koi ClawHavoc original
  (redirects). See [excluded.md](excluded.md#unverifiable).
- Claude Code GitHub issue 12637 (rm -rf ~ incident).
- Pillar's per-finding posts in the Week of Sandbox Escapes series. Only the
  summary post was read.

## Researcher Stream

28 sources (R-001 to R-028). All verified from arXiv abstract pages (or the
Meta blog for R-009); no full papers were read.

The stopping rule was not reached. Of the last ten added (R-019 to R-028 by
date), at least five brought a new recommendation: engine-class and patch-lag
comparison of sandboxes (R-020), revoking capabilities at task end (R-022),
auditing persistent carriers such as memory and skills (R-026), natural-language
rules in CLAUDE.md are rarely enforced (R-027), and task type changing
repository-poisoning risk (R-028). CapSeal (R-016) adds broker-mediated secrets.

### Researcher Gaps

- MCP tool poisoning papers found but not opened (see excluded.md).
- No forward-citation search on the Design Patterns paper, Spotlighting, or
  AgentDojo beyond one CaMeL follow-up query.
- No venue-specific search of USENIX Security, IEEE S&P, CCS, NDSS 2026
  proceedings, or ML-venue workshops. Venue status of most 2026 papers is
  unknown (preprints).
- Full texts not read; recommendations come from abstracts.
- Egress control has almost no dedicated research beyond R-018 and R-022.

## Standards Stream

7 sources (S-001 to S-007). The stopping rule was not reached.

### Standards Gaps

- S-002 (OWASP Agentic Top 10) and S-004 (CISA and partners) PDFs not read;
  their per-risk mitigations still need extraction.
- Not searched: OWASP LLM01:2025 Prompt Injection page, OWASP "Securing Agentic
  Applications Guide" and Agentic Threats and Mitigations, NIST AI 100-2 E2025,
  NIST CAISI AI Agent Standards Initiative (2026-02-17), UK AISI, ENISA, BSI,
  ANSSI, MITRE ATLAS, NCSC guidelines for secure AI system development.

## Third Session (2026-10-01)

Stopped at 53 of 60 searches and fetches before starting a new chain.

- Standards: S-002 PDF read (ASI01 to ASI05 mitigations, leads); S-004 read
  through the Canadian Cyber Centre HTML version. Added S-008 (NCSC interim
  agentic AI guidance, 2026-08-20), S-009 (OWASP LLM01), S-010 (ANSSI-BSI, 2024,
  partly verified), S-011 (NIST AI 100-2 E2025, partly verified). Stopping rule
  not reached: S-008 brought network and compute isolation maturity levels,
  proxy-injected credentials, and attributable traffic; S-002 brought per-tool
  egress allowlists and hash pinning.
- Researchers: added R-029 to R-034. Stopping rule not reached: R-029 (utility
  cost of a proxy-enforced egress allowlist), R-031 (OS sandbox share of the
  ASR reduction, byte-bound one-shot approvals), and R-030 (recoverable IFC)
  are new.
- Egress research gap: partly closed by R-029 and P-058 (DNS bypass of an
  HTTP-only allowlist). Still no dedicated study of egress-control bypass
  classes.

### Remaining Standards Gaps

- OWASP Securing Agentic Applications Guide 1.0 not located.
- MITRE ATLAS agentic techniques not verified at the source.
- ENISA, BSI (2026), ANSSI (2026), UK AISI (as guidance), CAISI final
  guidance: nothing agent-specific found or not yet published.
- S-010 and S-011 recommendations not extracted.

## Where to Resume

1. Researchers: open the R-002 forward-citation titles listed in excluded.md
   (ROPE, Twin Agent, LACUNA, When Tool Outputs Become Commands, Janus), then
   the earlier deferred titles (LivePI, ClawGuard, MCP-ITP, 2605.24069,
   2606.04141, CaMeLoT).
2. Researchers: forward citations of R-003 (AgentDojo, arXiv 2406.13352) and
   Spotlighting (arXiv 2403.14720); reference lists of R-011 and R-023 (not
   done in session 3).
3. Egress: verify the BeyondTrust AgentCore DNS research (403) through another
   URL; search for DNS and covert-channel studies on agent sandboxes.
4. Venues: USENIX Security 2026 and CCS 2026 accepted-paper lists (only NDSS
   checked, via one search).
5. Standards: OWASP Securing Agentic Applications Guide; ATLAS data repository;
   extract S-010 recommendations from the PDF; S-002 ASI06 to ASI10 in detail.
6. Apply the stopping rule from R-034 and S-011 onwards.

## Central Sources for Citation Chaining

- P-021 (lethal trifecta): the threat model most practitioner sources cite.
- P-004 and P-003 (Anthropic secure deployment and sandbox environments): the
  most complete vendor comparison of boundaries, credential proxying, and egress
  limits.
- P-025 (NVIDIA AI Red Team): the clearest mandatory versus recommended control
  list, including a VM recommendation.
- P-029 (Pillar Security): the main source on host-side delayed execution, a
  planned blind spot in Step 4.
- P-030 against P-035 (Embrace The Red against Anthropic auto mode): the
  clearest contested point on classifiers as a defense.
- P-027 and P-054 (Guan, PromptArmor): concrete egress allowlist bypasses.
- P-036 (GitHub Agentic Workflows): the most detailed production architecture
  with zero secrets in the agent.
- R-001 (CaMeL), R-002 (Design Patterns), R-003 (AgentDojo): the hub of the
  research citation graph; most 2026 defense papers evaluate on AgentDojo.
- R-008 (Attacker Moves Second): the main evidence against classifier and
  prompt defenses; pairs with P-030.
- R-011 and R-023: the coding-agent-specific SoKs; best reference lists for
  further chaining.
- S-002 and S-004: the standards most likely to be cited by practitioners.
- S-008 (NCSC agentic AI guidance): the most concrete standards source on
  egress and isolation levels; maps directly onto the CodeVM design.
