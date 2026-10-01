# Research Plan: How Practitioners and Researchers Recommend Securing Coding Agents

**Harnesses in scope:** Claude Code, pi. Include sources about Codex CLI, Gemini CLI, Cursor, Aider, and similar tools when their recommendations generalize.

**Goal:** Find out what practitioners and researchers recommend for isolating coding agents from the host. The main concerns are secret leakage and prompt injection being turned into remote code execution. Record where the two groups agree, where they disagree, and where practice lags behind research.

**Non-goal:** Designing or building a setup. Implications for CodeVM come last, after the survey.

**Time box:** 2026-01 to 2026-09 material preferred; include older material only when it is foundational or widely cited.

---

## Research questions

- **RQ1 — Threat models:** Which threat models do practitioners and researchers use for coding agents? Do they agree on the main risks?
- **RQ2 — Isolation boundary:** Which boundary do they recommend (native harness sandbox, OS sandbox, container, microVM/VM, remote machine), for which threat level, and why?
- **RQ3 — Secrets:** How do they recommend handling credentials, including the model API key?
- **RQ4 — Network egress:** How do they recommend controlling egress, and which bypasses do they acknowledge?
- **RQ5 — Prompt injection:** Which defenses do researchers consider effective, and which do practitioners actually deploy?
- **RQ6 — Secondary risks:** Which other risks come up most often (host-side delayed execution, supply chain, destructive actions, code integrity, resource abuse, data governance, multi-agent trust)? Which are rarely addressed?
- **RQ7 — Gaps:** Where do practitioners and researchers disagree, and where does practice lag research?

## Step 1: Collect sources

Search each stream separately and log the queries, date, and number of hits so the search can be repeated.

### Practitioners

- **Vendor documentation:** Anthropic (Claude Code security, sandboxing, devcontainer, hooks, managed settings), OpenAI Codex, Google Gemini CLI, Cursor, pi's repo and docs.
- **Reference setups:** official devcontainers, sandbox runtimes, and open-source agent sandbox projects, including their READMEs and issue trackers.
- **Engineering blogs:** companies describing how they run agents internally.
- **Security firms and independent researchers:** Trail of Bits, NCC Group, NVIDIA AI Red Team, Invariant Labs, Embrace The Red (Johann Rehberger), Simon Willison.
- **Talks:** Black Hat, DEF CON AI Village, and similar events.
- **Community discussion:** Hacker News, Reddit, Lobsters, maintainer blogs.
- **Observed practice:** public dotfiles and agent configs (`settings.json`, `AGENTS.md`, devcontainer files), to see what people actually run as opposed to what they recommend.
- **Incidents and disclosures:** CVEs and write-ups against coding agents.

### Researchers

- **Venues:** arXiv, USENIX Security, IEEE S&P, CCS, NDSS, and security workshops at ML venues.
- **Benchmarks:** AgentDojo, InjecAgent, and any benchmarks specific to coding agents.
- **Surveys:** surveys of LLM agent security and prompt injection.
- **Citation chains:** follow references backwards and citations forwards from key papers (CaMeL, dual-LLM pattern, spotlighting, lethal trifecta).

### Standards and guidance

- OWASP Top 10 for LLM Applications and OWASP agentic AI guidance.
- NIST, CISA, NCSC, and similar guidance on AI agents.

### Inclusion criteria

- The source makes at least one concrete recommendation or evaluates one.
- The source is about agents that execute code or tools, not only chatbots.
- Duplicates and reposts count once; cite the original.

## Step 2: Download sources

Download every source once, so extraction agents never fetch anything and each site is hit only once.

- **Source list:** generate `sources/sources.csv` once from `sources/sources.md`, keyed by the existing IDs (P-001, R-001, S-001, ...). From then on, the CSV is the source of truth; new sources are added there.
- **Fetch script:** a Python script that runs on the host. It uses `trafilatura` for HTML and `pymupdf` for PDFs. It rate-limits requests, respects `robots.txt`, and skips sources that are already downloaded.
- **Layout:** for each source, `sources/corpus/<ID>/raw.*` (the original file) and `sources/corpus/<ID>/clean.md` (normalized text). The `corpus/` directory is gitignored.
- **Manifest:** `sources/manifest.csv` is committed. It records ID, URL, fetch date, HTTP status, content hash, extraction method, and clean-text length. On re-runs, compare hashes to see which sources changed.
- **Manual-check list:** the script writes `sources/manual_check.md`, listing each source it flags with the reason. A source is flagged when:
  - the HTTP status is not 200, or the request was redirected to a login or paywall;
  - the clean text is shorter than a threshold (default 1,500 characters), which usually means only an abstract or an empty JavaScript page;
  - the domain is known not to work (X/Twitter, LinkedIn, video sites);
  - PDF conversion produced garbage (a low share of real words).

  All thresholds are command-line flags.
- **Manual downloads:** for flagged sources, for example paywalled papers, place the file at `sources/corpus/<ID>/raw.pdf` (or `raw.html`) and re-run the script in normalize-only mode. Manually downloaded files go through the same normalization as all others.
- **Licensing:** only include sources that may be given to an LLM. Mark excluded sources in `sources.csv` instead of downloading them.

## Step 3: Extract each source once

Read each source exactly once and extract everything that later steps need. Later steps work only on the extraction records and never re-read sources, except for spot checks.

- **Isolated extractor:** a driver script runs headless `claude -p` once per source inside CodeVM. Each run may use only the Read and Write tools. It gets one input path (`corpus/<ID>/clean.md`) and one output path, and has no web or shell access. Sources may contain prompt-injection payloads, so they are handled inside the sandbox being researched. The driver skips IDs that already have a record, so interrupted runs can be resumed.
- **Records:** one file per source at `sources/extractions/<ID>.yaml`, committed. Each record contains:
  - **Metadata:** ID, title, author or organization, date, stream, author role and incentives, harness, `extracted_by` (the model used).
  - **Inclusion:** `included` (true or false) and the reason, re-checked against the inclusion criteria on the full text.
  - **`recommendations[]`:** one entry per recommendation, with practice tag, stance (recommends, rejects, evaluates), threat addressed, research questions, evidence type, stated tradeoffs, known bypasses or limits, a verbatim quote, and its location.
  - **`threat_model`:** the framework the source names, plus lists of assets, untrusted input channels, and failure modes. Each element has a verbatim quote.
  - **`notes`:** free text for anything the schema does not cover.
- **Vocabulary:** practice and threat tags come from a controlled vocabulary. Values outside it are written as `other:<text>`. The seed vocabulary is written during the pilot.
- **Validation:** a script checks every record against a JSON Schema. It also confirms that every quote appears in `clean.md`, after normalizing whitespace and quote characters. A failing record is re-extracted once; if it fails again, the source goes on `manual_check.md`.
- **Long sources:** the extractor reads the whole text. Sources over about 150k tokens are flagged on `manual_check.md` for a decision; they are not chunked automatically.
- **Pilot first:** extract about six varied sources (a paper, vendor documentation, a blog post, a CVE write-up, a standard, a long survey) with the strongest available model. Review the records, revise the schema and vocabulary, and only then run all sources. Choose the model for the full run based on the pilot.

## Step 4: Aggregate and derive the threat model

- **Scripts** turn the records into:
  - `sources.bib`: one entry per included source, with author-year citation keys and the source ID in the `note` field. The entry type is guessed (`@article` when there is a DOI or arXiv ID, otherwise `@misc` with `url` and `urldate`). The script only adds missing entries and never overwrites existing ones, so manual fixes are kept.
  - The recommendation matrix (practices as rows, sources as columns).
  - Lists of threat-model elements (frameworks, assets, input channels, failure modes), with counts per stream and the record IDs that name them.
- **LLM draft:** an agent drafts the source-derived threat model from these lists only, citing record IDs. It notes which framework each stream uses and whether the frameworks are compatible. The draft is then reviewed by hand.

## Step 5: Synthesize (manual)

Done by hand from the extraction records and Step 4 outputs. For each research question, produce:

- **Consensus:** recommendations most sources share, with the strength of their evidence.
- **Contested points:** where sources disagree and the reasons each side gives. Candidates to check:
  - Is a shared-kernel boundary (container, OS sandbox) enough, or is a VM needed?
  - Is per-domain egress allowlisting enough?
  - Are prompt-injection classifiers worth deploying?
  - Is the harness's native permission system a security boundary or only a convenience?
- **Practice-vs-research gaps:** recommendations from research that practitioners don't follow, and practices with no research support.
- **Blind spots:** risks that few sources address, such as agent-written git hooks, `.envrc`, or IDE task files executed later on the host.

## Step 6: Verify contested claims (optional, small)

- Pick only claims that are contested or unverified and that matter for CodeVM.
- Reproduce them with the smallest possible test, for example a canary token and an injected README.
- Anything larger belongs in a separate hands-on plan.

## Step 7: Deliverables

1. **Bibliography:** `sources.bib`, plus the extraction records tagged by stream, date, and evidence type.
2. **Recommendation matrix:** practices as rows, sources as columns; each cell is *recommends*, *rejects*, or *not mentioned*.
3. **Source-derived threat model** (Step 4).
4. **Synthesis report:** consensus, contested points, gaps, and blind spots per research question (Step 5).
5. **Implications for CodeVM:** compare the current setup (Lima VM, nftables egress allowlist, package set) with the consensus, and list changes worth considering.
6. **Re-check list:** open questions and sources to revisit.

## Stopping rules

- Stop searching a stream when the last ten new sources add no new recommendations.
- Re-run the searches every three months, since the field moves quickly.
