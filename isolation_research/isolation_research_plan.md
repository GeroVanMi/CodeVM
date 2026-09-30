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

## Step 2: Extract each source with the same template

Record every source in a table with these fields:

| Field | Values |
| --- | --- |
| Source | Title, author, link, date |
| Stream | Practitioner, researcher, standard |
| Author role and incentives | For example, vendor selling a sandbox, independent researcher, academic |
| Harness | Claude Code, pi, other, general |
| Research questions covered | RQ1–RQ7 |
| Threat addressed | Secret leakage, injection-to-RCE, destructive action, etc. |
| Recommendation | What the source says to do, in one sentence |
| Evidence type | Opinion, anecdote, incident, experiment, formal analysis |
| Stated tradeoffs | Ergonomics, cost, performance, platform support |
| Known bypasses or limits | As stated by the source |

## Step 3: Derive the threat model from the sources

- Collect the threat models and frameworks the sources use, for example the lethal trifecta, OWASP categories, STRIDE-style models, and threat models from papers.
- List the assets, untrusted input channels, and failure modes that sources name repeatedly.
- Note which framework is used by which stream and whether they are compatible.
- Output: a threat model built from the sources, with each item cited.

## Step 4: Synthesize

For each research question, produce:

- **Consensus:** recommendations most sources share, with the strength of their evidence.
- **Contested points:** where sources disagree and the reasons each side gives. Candidates to check:
  - Is a shared-kernel boundary (container, OS sandbox) enough, or is a VM needed?
  - Is per-domain egress allowlisting enough?
  - Are prompt-injection classifiers worth deploying?
  - Is the harness's native permission system a security boundary or only a convenience?
- **Practice-vs-research gaps:** recommendations from research that practitioners don't follow, and practices with no research support.
- **Blind spots:** risks that few sources address, such as agent-written git hooks, `.envrc`, or IDE task files executed later on the host.

## Step 5: Verify contested claims (optional, small)

- Pick only claims that are contested or unverified and that matter for CodeVM.
- Reproduce them with the smallest possible test, for example a canary token and an injected README.
- Anything larger belongs in a separate hands-on plan.

## Step 6: Deliverables

1. **Annotated bibliography:** every source, tagged by stream, date, and evidence type.
2. **Recommendation matrix:** practices as rows, sources as columns; each cell is *recommends*, *rejects*, or *not mentioned*.
3. **Source-derived threat model** (Step 3).
4. **Synthesis report:** consensus, contested points, gaps, and blind spots per research question (Step 4).
5. **Implications for CodeVM:** compare the current setup (Lima VM, nftables egress allowlist, package set) with the consensus, and list changes worth considering.
6. **Re-check list:** open questions and sources to revisit.

## Stopping rules

- Stop searching a stream when the last ten new sources add no new recommendations.
- Re-run the searches every three months, since the field moves quickly.
