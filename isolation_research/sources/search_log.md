# Search Log

Step 1 source collection for the [research plan](../isolation_research_plan.md).
All queries ran on 2026-09-30.

## Method

- WebSearch returns about ten results per query. "Hits" is the number of results
  returned; "Kept" is the number of candidates kept at query time. Later
  deduplication and exclusion reduced the 82 kept candidates to the 57 sources
  in the source list (now [sources.csv](sources.csv)); see [excluded.md](excluded.md).
  P-058 was added in a later session and P-045 was removed in Step 2, so
  the practitioner stream now has 57 sources (102 in total).
- Sources found by following a link from a kept source are logged as "(direct
  fetch)" rows.
- Each kept source was opened with WebFetch to confirm title, author, and date
  unless the `verification` column of [sources.csv](sources.csv) says otherwise.
- The first session was stopped on request after the practitioner stream. A
  second session on the same date searched the researcher and standards
  streams and stopped at its 60-call budget.

## Practitioner Queries

| #   | Query                                                                                                               | Tool / mode                 | Hits        | Kept                               |
| --- | ------------------------------------------------------------------------------------------------------------------- | --------------------------- | ----------- | ---------------------------------- |
| 1   | Claude Code sandboxing documentation bubblewrap seatbelt network proxy                                              | WebSearch/standard          | 10          | 2                                  |
| 2   | Claude Code security documentation prompt injection devcontainer                                                    | WebSearch/standard          | 9           | 3                                  |
| 3   | OpenAI Codex CLI sandbox security documentation network access approval modes                                       | WebSearch/standard          | 9           | 2                                  |
| 4   | Gemini CLI sandbox documentation docker seatbelt                                                                    | WebSearch/standard          | 9           | 1                                  |
| 5   | anthropic engineering blog Claude Code sandboxing beyond permission prompts                                         | WebSearch/standard          | 9           | 1                                  |
| 6   | Anthropic Claude Code auto mode classifier prompt injection engineering blog 2026                                   | WebSearch/standard          | 9           | 2                                  |
| 7   | pi coding agent Mario Zechner security sandbox YOLO                                                                 | WebSearch/standard          | 9           | 1                                  |
| 8   | Cursor agent security sandbox terminal commands documentation 2026                                                  | WebSearch/standard          | 9           | 2                                  |
| 9   | mariozechner.at "opinionated and minimal coding agent" pi                                                           | WebSearch/standard          | 10          | 1                                  |
| 10  | github badlogic pi-mono coding-agent README security permissions containers                                         | WebSearch/standard          | 10          | 1                                  |
| 11  | Gondolin micro-VM agent sandbox earendil                                                                            | WebSearch/standard          | 9           | 1                                  |
| 12  | NVIDIA OpenShell agent sandbox policy                                                                               | WebSearch/standard          | 9           | 1                                  |
| 13  | open source sandbox for running Claude Code Codex agents safely microVM github 2026                                 | WebSearch/extended          | 9           | 2                                  |
| 14  | anthropic-experimental sandbox-runtime github issues escape bypass                                                  | WebSearch/standard          | 9           | 0                                  |
| 15  | agent-safehouse macOS sandbox coding agents                                                                         | WebSearch/standard          | 10          | 1                                  |
| 16  | Claude Code network sandbox bypass SOCKS5 null byte disclosure Guan                                                 | WebSearch/standard          | 10          | 0                                  |
| 17  | Aonan Guan Claude Code sandbox bypass blog original writeup                                                         | WebSearch/extended          | 9           | 3                                  |
| 18  | Trail of Bits coding agent security sandbox prompt injection 2026 blog                                              | WebSearch/standard          | 9           | 1                                  |
| 19  | NVIDIA AI Red Team practical security guidance sandboxing agentic workflows code execution                          | WebSearch/standard          | 9           | 2                                  |
| 20  | NCC Group coding agent security research Claude Code Cursor 2026                                                    | WebSearch/standard          | 9           | 0                                  |
| 21  | Pillar Security sandbox escape Cursor Codex Gemini CLI Antigravity host tools execute files research                | WebSearch/standard          | 9           | 0                                  |
| 22  | blog.trailofbits.com prompt injection to RCE AI agents argument injection                                           | WebSearch/standard          | 9           | 1                                  |
| 23  | pillar.security blog sandbox escapes coding agents seven bypasses                                                   | WebSearch/standard          | 10          | 1                                  |
| 24  | embracethered.com 2026 coding agent prompt injection Claude Code Codex exfiltration                                 | WebSearch/standard          | 9           | 0                                  |
| 25  | Simon Willison lethal trifecta coding agents sandbox 2026                                                           | WebSearch/standard          | 10          | 2                                  |
| 26  | Invariant Labs toxic flow analysis MCP coding agent GitHub exploit                                                  | WebSearch/standard          | 9           | 1                                  |
| 27  | Johann Rehberger embrace the red 2026 agent                                                                         | WebSearch/extended          | 10          | 0                                  |
| 28  | Joy Heron INNOQ blog sandbox coding agents Lima VM network                                                          | WebSearch/standard          | 9           | 3                                  |
| 29  | embracethered.com blog posts 2026 Claude Code auto mode remote code execution                                       | WebSearch/extended          | 10          | 1                                  |
| 30  | (direct fetch) Codex agent-approvals-security, Claude Code security/devcontainer/permissions/hooks pages            | WebFetch                    | 5           | 5                                  |
| 31  | CVE 2026 Claude Code vulnerability remote code execution project settings hooks trust dialog                        | WebSearch/standard          | 10          | 0                                  |
| 32  | Check Point Research Claude Code CVE-2025-59536 hooks MCP API key exfiltration ANTHROPIC_BASE_URL                   | WebSearch/standard          | 9           | 1                                  |
| 33  | Codex CLI CVE vulnerability 2026 command injection sandbox                                                          | WebSearch/standard          | 9           | 0                                  |
| 34  | CVE-2026-19592 Codex fsmonitor git config advisory researcher                                                       | WebSearch/standard          | 9           | 1                                  |
| 35  | Check Point Research OpenAI Codex CLI CVE-2025-61260 command injection project config                               | WebSearch/standard          | 9           | 1                                  |
| 36  | "Comment and Control" prompt injection GitHub Actions Claude Code Gemini CLI Copilot credential theft               | WebSearch/standard          | 9           | 0                                  |
| 37  | oddguan.com comment and control prompt injection credential theft Claude Code Gemini CLI GitHub Copilot agent       | WebSearch/standard          | 9           | 1                                  |
| 38  | Gemini CLI security trusted folders documentation prompt injection Tracebit vulnerability                           | WebSearch/standard          | 9           | 2                                  |
| 39  | GitHub Copilot coding agent firewall security documentation network allowlist                                       | WebSearch/standard          | 10          | 1                                  |
| 40  | GitHub Agentic Workflows security architecture safe outputs threat model                                            | WebSearch/standard          | 9           | 1                                  |
| 41  | how we run coding agents securely internally engineering blog sandbox credentials egress 2026                       | WebSearch/extended          | 9           | 2                                  |
| 42  | Stripe Minions background coding agents devbox isolation security blog                                              | WebSearch/standard          | 9           | 0                                  |
| 43  | company blog "coding agents" production credentials "egress proxy" isolated VM per task lessons learned             | WebSearch/extended          | 10          | 1                                  |
| 44  | Black Hat USA 2026 coding agents talk prompt injection sandbox                                                      | WebSearch/standard          | 9           | 2                                  |
| 45  | "Caging the Agent" Roblox Claude Code sandboxes Black Hat                                                           | WebSearch/standard          | 9           | 1                                  |
| 46  | DEF CON 34 AI Village 2026 coding agent talk sandbox prompt injection                                               | WebSearch/standard          | 9           | 0                                  |
| 47  | "The Sandbox Is a Suggestion" Elad Meged Novee Security DEF CON                                                     | WebSearch/standard          | 10          | 0                                  |
| 48  | Stripe engineering blog minions one-shot end-to-end coding agents devbox (allowed_domains stripe.dev, stripe.com)   | WebSearch/standard          | 10          | 1                                  |
| 49  | news.ycombinator.com sandbox coding agents VM container dangerously-skip-permissions 2026                           | WebSearch/standard          | 9           | 2                                  |
| 50  | lobste.rs sandboxing coding agents                                                                                  | WebSearch/standard          | 9           | 1                                  |
| 51  | HN Algolia API: "sandbox coding agent" (stories, created>=2026-01-01, comments>30)                                  | HN Algolia API              | 17          | 1                                  |
| 52  | HN Algolia API: "claude code sandbox" (same filters)                                                                | HN Algolia API              | 14          | 0                                  |
| 53  | HN Algolia API: "agent sandbox" (same filters)                                                                      | HN Algolia API              | 43          | 4                                  |
| 54  | HN Algolia API: "lethal trifecta" (same filters)                                                                    | HN Algolia API              | 0           | 0                                  |
| 55  | HN Algolia API: "prompt injection coding agent" (same filters)                                                      | HN Algolia API              | 2           | 1                                  |
| 56  | HN Algolia API: "dangerously-skip-permissions" (same filters)                                                       | HN Algolia API              | 1           | 0                                  |
| 57  | HN Algolia API: "YOLO mode agent" (same filters)                                                                    | HN Algolia API              | 1           | 1                                  |
| 58  | HN Algolia API: "microVM agents" (same filters)                                                                     | HN Algolia API              | 3           | 1                                  |
| 59  | HN Algolia API: "Claude Code security" (same filters)                                                               | HN Algolia API              | 13          | 0                                  |
| 60  | HN Algolia API: "exfiltrate" (same filters)                                                                         | HN Algolia API              | 12          | 2                                  |
| 61  | HN Algolia API: "egress" (same filters)                                                                             | HN Algolia API              | 15          | 0                                  |
| 62  | HN Algolia API: "sandboxing" (same filters)                                                                         | HN Algolia API              | 13          | 1                                  |
| 63  | HN Algolia API: "prompt injection" (same filters)                                                                   | HN Algolia API              | 14          | 0                                  |
| 64  | HN Algolia API: "Codex sandbox" (same filters)                                                                      | HN Algolia API              | 28          | 0                                  |
| 65  | HN Algolia API: "devcontainer agent" (same filters)                                                                 | HN Algolia API              | 1           | 0                                  |
| 66  | HN Algolia API: "auto mode" (same filters)                                                                          | HN Algolia API              | 30          | 1                                  |
| 67  | reddit r/ClaudeAI how do you sandbox Claude Code dangerously-skip-permissions VM container                          | WebSearch/standard          | 9           | 0                                  |
| 68  | reddit r/netsec coding agent prompt injection sandbox escape 2026                                                   | WebSearch/standard          | 9           | 0                                  |
| 69  | Reddit search.json API: "sandbox claude code", "dangerously-skip-permissions VM", "coding agent prompt injection"   | curl reddit.com/search.json | 0 (blocked) | 0                                  |
| 70  | site:reddit.com Claude Code sandbox VM isolation secrets setup                                                      | WebSearch/extended          | 9           | 0                                  |
| 71  | Mitchell Hashimoto OR Armin Ronacher OR Thorsten Ball agent sandbox VM blog 2026                                    | WebSearch/standard          | 10          | 0                                  |
| 72  | lucumr.pocoo.org gondolin sandbox agents                                                                            | WebSearch/standard          | 9           | 0                                  |
| 73  | github dotfiles claude settings.json sandbox permissions deny "Read(~/.ssh" observed agent configs                  | WebSearch/standard          | 9           | 0                                  |
| 74  | (direct fetch) simonwillison.net tags sandboxing, lethal-trifecta; day pages 2026-03-18, 2026-07-22, 2026-07-30     | WebFetch                    | 5           | 4                                  |
| 75  | OpenAI GPT-5.6 Sol sandbox escape Hugging Face package registry proxy incident report July 2026                     | WebSearch/extended          | 9           | 0                                  |
| 76  | PromptArmor Snowflake Cortex Code CLI sandbox escape malware process substitution                                   | WebSearch/standard          | 9           | 1                                  |
| 77  | openai.com joint postmortem Hugging Face ExploitGym evaluation sandbox (allowed_domains openai.com, huggingface.co) | WebSearch/standard          | 9           | 2                                  |
| 78  | (direct fetch) anthropic.com/engineering/claude-code-sandboxing; simonwillison.net lethal trifecta 2025-06-16       | WebFetch                    | 2           | 2                                  |
| 79  | Nx s1ngularity supply chain attack weaponized Claude Code Gemini CLI dangerously-skip-permissions steal secrets     | WebSearch/standard          | 9           | 1                                  |
| 80  | IDEsaster vulnerabilities AI IDEs Ari Marzouk                                                                       | WebSearch/standard          | 10          | 0                                  |
| 81  | malicious agent skills ClawHub OpenClaw supply chain 2026 research credential theft                                 | WebSearch/standard          | 9           | 0                                  |
| 82  | IDEsaster original research blog maccarita                                                                          | WebSearch/standard          | 9           | 0 (original found by direct fetch) |
| 83  | Koi Security ClawHavoc malicious skills ClawHub blog                                                                | WebSearch/standard          | 9           | 1                                  |
| 84  | coding agent deleted home directory rm -rf incident Claude Code Antigravity wiped drive destructive action          | WebSearch/standard          | 9           | 0                                  |

HN Algolia API calls used `https://hn.algolia.com/api/v1/search` with
`tags=story`, `numericFilters=created_at_i>1767225600,num_comments>30` (stories
since 2026-01-01 with more than 30 comments), and `hitsPerPage=15`. Reddit's
search API returned no data (blocked), so Reddit is not covered.

## Observed Practice Snapshot

GitHub code search counts via `gh api -X GET search/code -f q="<query>"`, run
2026-09-30. Counts are GitHub's approximate totals over indexed default
branches, not unique repositories. They show adoption signals only; no files
were read.

| Query                                                          | Total count |
| -------------------------------------------------------------- | ----------- |
| filename:settings.json path:.claude                            | 67328       |
| filename:settings.json path:.claude "sandbox"                  | 1450        |
| filename:settings.json path:.claude "allowUnsandboxedCommands" | 260         |
| filename:settings.json path:.claude "allowedDomains"           | 121         |
| filename:settings.json path:.claude "bypassPermissions"        | 1224        |
| filename:settings.json path:.claude "~/.ssh"                   | 1150        |
| filename:settings.json path:.claude ".env"                     | 9024        |
| filename:settings.json path:.claude "hooks"                    | 33088       |
| filename:devcontainer.json "claude-code"                       | 5632        |
| filename:devcontainer.json "dangerously-skip-permissions"      | 69          |
| filename:init-firewall.sh                                      | 888         |
| filename:config.toml path:.codex                               | 10080       |
| filename:config.toml path:.codex "danger-full-access"          | 450         |
| filename:config.toml path:.codex "workspace-write"             | 1584        |
| filename:.srt-settings.json                                    | 12          |
| filename:AGENTS.md                                             | 1130496     |
| filename:AGENTS.md "prompt injection"                          | 4856        |
| filename:CLAUDE.md "prompt injection"                          | 3344        |

## Researcher Queries

Second session, 2026-09-30. 56 searches and fetches in total across both
streams (limit 60). Direct fetches are arXiv abstract pages only.

| #   | Query | Tool / mode | Hits | Kept |
| --- | ----- | ----------- | ---- | ---- |
| R1  | (direct fetch) arxiv.org/abs/2503.18813 CaMeL | WebFetch | 1 | 1 (R-001) |
| R2  | (direct fetch) arxiv.org/abs/2506.08837 Design Patterns | WebFetch | 1 | 1 (R-002) |
| R3  | (direct fetch) arxiv.org/abs/2406.13352 AgentDojo | WebFetch | 1 | 1 (R-003) |
| R4  | (direct fetch) arxiv.org/abs/2403.02691 InjecAgent | WebFetch | 1 | 1 (R-004) |
| R5  | (direct fetch) arxiv.org/abs/2403.14720 Spotlighting | WebFetch | 1 | 1 (R-005) |
| R6  | (direct fetch) arxiv.org/abs/2604.02837 seed | WebFetch | 1 | 1 (R-014) |
| R7  | (direct fetch) arxiv.org/abs/2607.25379 seed | WebFetch | 1 | 1 (R-025) |
| R8  | arXiv 2026 coding agent prompt injection benchmark sandbox security Claude Code | WebSearch/extended | 10 | 6 |
| R9  | survey LLM agent security prompt injection defenses 2026 arXiv | WebSearch/standard | 10 | 3 |
| R10 | (direct fetch) abs pages 2601.17548, 2608.23550, 2607.05743, 2607.20759, 2608.06984, 2606.10749, 2602.10453 | WebFetch x7 | 7 | 7 |
| R11 | "The Attacker Moves Second" adaptive attacks prompt injection defenses arXiv | WebSearch/standard | 10 | 1 |
| R12 | Progent privilege control LLM agents OR "MELON" ... OR "Systems Security Foundations for Agentic Computing" | WebSearch/standard | 9 | 1 |
| R13 | Meta "Agents Rule of Two" AI agent security | WebSearch/standard | 9 | 1 |
| R14 | (direct fetch) 2504.11703, 2510.09023, ai.meta.com practical-ai-agent-security | WebFetch x3 | 3 | 3 |
| R15 | arXiv benchmark LLM agent container sandbox escape evaluation 2026 | WebSearch/extended | 10 | 3 |
| R16 | information flow control LLM agents FIDES Microsoft arXiv prompt injection planner | WebSearch/standard | 10 | 1 |
| R17 | (direct fetch) 2603.02277, 2606.08433, 2606.22504, 2505.23643 | WebFetch x4 | 4 | 4 |
| R18 | 2026 arXiv CaMeL follow-up capability-based agent prompt injection coding agent defense evaluation | WebSearch/extended | 9 | 1 |
| R19 | (direct fetch) 2601.09923 | WebFetch | 1 | 1 |
| R20 | arXiv 2026 MCP tool poisoning attack defense evaluation coding agents | WebSearch/standard | 9 | 0 |
| R21 | arXiv 2026 coding agent secret exfiltration credentials environment variables egress study | WebSearch/extended | 10 | 4 |
| R22 | (direct fetch) 2604.16762, 2605.09721, 2604.03070, 2608.30686, 2604.23338 | WebFetch x5 | 5 | 5 |
| R23 | SoK prompt injection agentic coding assistants 42 attack techniques arXiv | WebSearch/standard | 9 | 1 |
| R24 | (direct fetch) 2605.25871 | WebFetch | 1 | 1 |

## Standards Queries

| #   | Query | Tool / mode | Hits | Kept |
| --- | ----- | ----------- | ---- | ---- |
| S1  | OWASP Top 10 for Agentic Applications 2026 | WebSearch/standard | 10 | 1 |
| S2  | NIST AI agent security guidance 2026 agent hijacking CAISI | WebSearch/standard | 9 | 1 |
| S3  | (direct fetch) genai.owasp.org top 10 agentic applications 2026 | WebFetch | 1 | 1 (S-002) |
| S4  | NCSC CISA joint guidance AI agents agentic AI security 2026 | WebSearch/standard | 10 | 1 |
| S5  | OWASP agentic ASI01 agent goal hijack ASI05 unexpected code execution list | WebSearch/standard | 9 | 0 (names only) |
| S6  | CISA "Careful Adoption of Agentic Artificial Intelligence" cisa.gov | WebSearch/standard | 10 | 0 |
| S7  | NCSC blog prompt injection is not SQL injection | WebSearch/standard | 9 | 1 |
| S8  | (direct fetch) ncsc.gov.uk prompt-injection-is-not-sql-injection | WebFetch | 1 | 1 (S-003) |
| S9  | cisa.gov resources "Careful Adoption of Agentic AI Services" May 2026 joint guide | WebSearch/extended | 10 | 1 |
| S10 | (direct fetch) cisa.gov careful-adoption-agentic-ai-services | WebFetch | 1 | 1 (S-004) |
| S11 | OWASP Top 10 for LLM Applications 2025 LLM06 Excessive Agency genai.owasp.org llmrisk | WebSearch/standard | 9 | 0 |
| S12 | (direct fetch) genai.owasp.org llm062025-excessive-agency | WebFetch | 1 | 1 (S-001) |
| S13 | NIST CAISI technical blog AI agent hijacking evaluations AgentDojo | WebSearch/standard | 9 | 2 |
| S14 | OWASP "Securing Agentic Applications Guide" sandbox code execution recommendations | WebSearch/standard | 9 | 0 |
| S15 | (direct fetch) nist.gov CAISI red-teaming blog, nist.gov/node/1872381, govinfo FR-2026-01-08 | WebFetch x3 | 3 | 3 (S-005 to S-007) |

## Third Session Queries (2026-10-01)

A third session on 2026-10-01 continued the standards and researcher streams
with a budget of 60 searches and fetches. Same columns as above.

### Standards

| #   | Query | Tool/mode | Hits | Kept |
| --- | ----- | --------- | ---- | ---- |
| S16 | (direct fetch) genai.owasp.org S-002 landing page and cisa.gov S-004 landing page | WebFetch x2 | 2 | 0 (PDF links sought) |
| S17 | (direct fetch) cyber.gov.au S-004 HTML page | WebFetch | 0 (timeout) | 0 |
| S18 | "Top 10 for Agentic Applications" 2026 PDF ASI01 ASI02 ASI03 ASI04 ASI05 mitigations | WebSearch/standard | 9 | 0 (secondary) |
| S19 | "Careful adoption of agentic AI services" PDF cyber.gov.au recommendations privilege sandbox | WebSearch/standard | 10 | 0 (PDF link for S-004) |
| S20 | (direct fetch) cyber.gov.au S-004 PDF | WebFetch | 0 (timeout) | 0 |
| S21 | "careful adoption of agentic AI services" pdf site:cisa.gov OR site:media.defense.gov OR site:ncsc.gov.uk | WebSearch/standard | 9 | 0 (Canadian HTML version found) |
| S22 | (direct fetch) cyber.gc.ca careful-adoption-agentic-ai | WebFetch | 1 | 1 (S-004 upgraded) |
| S23 | genai.owasp.org wp-content uploads "Agentic-Applications" 2026 pdf | WebSearch/standard | 10 | 0 |
| S24 | (direct fetch) genai.owasp.org/owasp-top-10-for-agentic-applications, then download/52117 PDF | WebFetch x2 | 2 | 1 (S-002 upgraded; PDF text extracted locally) |
| S25 | (direct fetch) genai.owasp.org llm01-prompt-injection | WebFetch | 1 | 1 (S-009) |
| S26 | OWASP GenAI "Securing Agentic Applications Guide" sandbox code execution network egress recommendations | WebSearch/standard | 9 | 0 (guide itself not surfaced) |
| S27 | NIST CAISI "AI Agent Standards Initiative" 2026 agent security guidance publication | WebSearch/standard | 9 | 0 (no published guidance yet) |
| S28 | NIST AI 100-2 E2025 adversarial machine learning taxonomy agent hijacking indirect prompt injection mitigations | WebSearch/standard | 9 | 1 (S-011) |
| S29 | NCCoE concept paper AI agent identity and authorization 2026 | WebSearch/standard | 10 | 0 |
| S30 | BSI 2026 AI agents coding assistants security recommendations Bundesamt KI-Agenten | WebSearch/standard | 9 | 1 (S-010) |
| S31 | ANSSI 2026 recommandations sécurité agents IA OR "AI agents" ANSSI guidance | WebSearch/standard | 9 | 0 |
| S32 | MITRE ATLAS 2026 AI agent techniques mitigations tool invocation exfiltration agent | WebSearch/standard | 10 | 0 |
| S33 | (direct fetch) cyber.gouv.fr ANSSI-BSI news (404), nist.gov NCCoE news, cyber.gov.au cyber-defence news (timeout), atlas.mitre.org AML.T0086 (404) | WebFetch x4 | 1 | 0 |
| S34 | (direct fetch) cyber.gouv.fr AI coding assistants publication page, ctid.mitre.org Secure AI v2 post | WebFetch x2 | 2 | 1 (S-010) |
| S35 | "agentic AI in cyber defence" joint guidance July 2026 ASD recommendations sandbox privileges | WebSearch/standard | 10 | 0 |
| S36 | (direct fetch) ANSSI-BSI PDF at allianz-fuer-cybersicherheit.de | WebFetch | 1 | 0 (landing text only) |
| S37 | OWASP GenAI Security Project "Securing Agentic Applications Guide 1.0" genai.owasp.org resource | WebSearch/standard | 9 | 0 |
| S38 | UK AI Security Institute 2026 agent sandboxing containment guidance OR blog coding agents isolation | WebSearch/standard | 9 | 1 (S-008) |
| S39 | ENISA 2026 agentic AI security report recommendations AI agents | WebSearch/standard | 9 | 0 |
| S40 | (direct fetch) ncsc.gov.uk Managing-the-cyber-risk-of-agentic-AI.pdf (404), then _0.pdf | WebFetch x2 | 1 | 1 (S-008; text extracted locally) |

### Researchers

| #   | Query | Tool/mode | Hits | Kept |
| --- | ----- | --------- | ---- | ---- |
| R25 | arXiv 2026 LLM agent network egress control exfiltration sandbox allowlist proxy evaluation | WebSearch/extended | 9 | 3 |
| R26 | (forward citations) Semantic Scholar API citations of arXiv:2506.08837 (R-002), filtered by title | WebFetch | 12 listed | 2 opened and kept |
| R27 | (direct fetch) arXiv 2608.02670, 2607.24625, 2604.05432, 2601.11893, 2609.38224, 2604.13630 | WebFetch x6 | 6 | 5 (R-029 to R-033) |
| R28 | arXiv 2026 coding agent DNS exfiltration covert channel sandbox network policy bypass study | WebSearch/standard | 9 | 1 (P-058) |
| R29 | USENIX Security 2026 OR IEEE S&P 2026 OR NDSS 2026 prompt injection agent defense paper isolation privilege | WebSearch/standard | 10 | 1 |
| R30 | (direct fetch) beyondtrust.com AgentCore post (403), cveawg CVE-2026-12039 | WebFetch x2 | 1 | 1 (P-058) |
| R31 | "ACE: A Security Architecture for LLM-Integrated App Systems" arXiv NDSS 2026 | WebSearch/standard | 9 | 1 (R-034) |

Third session total: 53 searches and fetches (40 standards, 13 researcher).
P-058 is a practitioner incident found during the egress search.
