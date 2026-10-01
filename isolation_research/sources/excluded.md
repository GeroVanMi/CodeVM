# Excluded Candidates

Notable candidates seen during Step 1 and not kept in [sources.csv](sources.csv). P-045 was removed later, in Step 2.

## Reposts and Secondary Coverage

These report on a kept original, so the original is cited instead.

| Candidate                                                                                                                           | Reason                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| BleepingComputer, SecurityWeek, The Hacker News, CSO Online, Cybernews coverage of Pillar, Guan, Check Point, and GitSpawn findings | News coverage of P-026 to P-029 and P-050 to P-052.                     |
| Cloud Security Alliance research notes (Comment and Control, GuardFall, auto mode, sandbox escapes)                                 | Secondary summaries of kept originals.                                  |
| codex.danielvaughan.com posts on Codex CLI security                                                                                 | Aggregator commentary; cites the same disclosures.                      |
| penligent.ai, pasqualepillitteri.it, aiweekly.co, letsdatascience.com, hexnode.com                                                  | Rewrites of the Claude Code sandbox bypass and Pillar findings.         |
| Simon Willison link posts on Snowflake Cortex and Claude Cowork                                                                     | Link posts; PromptArmor originals kept as P-053 and P-054.              |
| Straiker Black Hat 2026 roundup                                                                                                     | Used only to locate P-044.                                              |
| NVD, SentinelOne, Debian tracker entries for CVE-2026-19592 and others                                                              | CVE records without recommendations; researcher write-ups kept instead. |

## Catalogs and Listicles

| Candidate                                                                              | Reason                                                                            |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| wincent, "List of coding agent sandboxes 2026-05" (gist)                               | Catalog by isolation primitive; no recommendation. Useful seed list for revisits. |
| fishman/awesome-agent-sandbox, bureado/awesome-agent-runtime-security                  | Curated lists; no recommendation. Seed lists.                                     |
| Blaxel, Mastra, Northflank, Bunnyshell sandbox comparisons                             | Vendor marketing listicles.                                                       |
| Launch HN and Show HN product threads (Freestyle, Hoplite, Tilde.run, Twill, machine0) | Product launches without a security recommendation.                               |

## Out of Scope

| Candidate                                                                                      | Reason                                                                                                          |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| PromptArmor reports on Notion AI, Atlassian Rovo, Google Sheets, Ramp Sheets                   | SaaS assistants that do not execute code or shell tools.                                                        |
| Oasis Security "Claudy Day"                                                                    | Targets claude.ai chat, not a coding agent.                                                                     |
| Trail of Bits, "Using threat modeling and prompt injection to audit Comet"                     | Browser assistant, not a coding agent.                                                                          |
| Check Point, "No Tools Required" (Black Hat USA 2026)                                          | Agent frameworks (LangChain, CrewAI), not coding agents. Borderline; revisit if RQ6 needs multi-agent material. |
| Palo Alto, "A Billion-User Blast Radius: Owning ChatGPT's Secure Sandbox" (Black Hat USA 2026) | ChatGPT code interpreter sandbox. Borderline; revisit for RQ2.                                                  |
| Wikipedia pages, StationX, Winbuzzer articles on the OpenAI incident                           | Secondary.                                                                                                      |

## Unverifiable

| Candidate                                                                                                               | Reason                                                                               |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| OpenAI, "OpenAI and Hugging Face partner to address security incident during model evaluation" and technical report PDF | Returned HTTP 403. Hugging Face timeline (P-057) kept instead. Revisit.              |
| Koi Security, "ClawHavoc: 341 malicious ClawdBot skills"                                                                | Original URL now redirects to a Palo Alto product page. Revisit via archive.         |
| Elad Meged, "The Sandbox Is a Suggestion" (DEF CON 34)                                                                  | Found only in a secondary roundup.                                                   |
| Trail of Bits June 2026 report on coding assistants forming zombie networks                                             | Mentioned only in an aggregator; no original found.                                  |
| Docker, "Coding agent horror stories: the rm -rf incident"                                                              | Vendor marketing post; the underlying Claude Code GitHub issue 12637 was not opened. |
| Stripe, "Minions part 2"                                                                                                | Not opened; part 1 kept as P-038.                                                    |

## Researcher and Standards Stream

| Candidate | Reason |
| --------- | ------ |
| SecRepoBench (arXiv 2504.21205) | Secure code generation, not agent isolation or injection. |
| LivePI (2605.17986), ClawGuard (2604.11790) | Seen as titles only; not opened within budget. Revisit. |
| MCP-ITP (2601.07395), Tool Description Poisoning (2605.24069), MCPTox (2508.14925), MCP server survey (2508.12538) | Not opened; MCP tool poisoning sub-topic deferred. Revisit. |
| CaMeLoT (2609.18674), VeriGrey (2603.17639), 2606.18530, 2604.18248, 2603.07496 | Titles only from one search; not opened. |
| StepShield (2601.22136), StealthBench (2607.26314), DuMateBench (2608.26546) | Rogue-agent intervention, offensive-agent stealth, or workflow benchmarks; off-topic for isolation. |
| Caught in the Act(ivation) (2606.04141) | Title only; not opened. Revisit (credential exfiltration detection). |
| Open Challenges in Multi-Agent Security (2505.02077), 2509.22040 | Not opened. |
| VILA-Lab Dive-into-Claude-Code (GitHub) | Architecture analysis, not a security recommendation. |
| CSA research notes on CISA, NIST CAISI, MCP tool poisoning | Secondary summaries of kept originals. |
| Kiteworks, Mayer Brown, HSToday, MeriTalk, Industrial Cyber coverage of CISA guidance | News or vendor coverage of S-004. |
| Modulos, Speakeasy, Palo Alto, Cycode, Teleport, BleepingComputer OWASP agentic explainers | Secondary coverage of S-002. |
| Simon Willison, "New prompt injection papers" | Link post; originals kept as R-008 and R-009. |
| NIST AI 100-2 E2025 (adversarial ML taxonomy) | Mentioned in secondary sources only; not opened. Revisit. |
| NVIDIA sandboxing post, nhimg.org, stride.build, augmentcode guides | Practitioner or vendor material; NVIDIA already P-025. |

## Third Session (2026-10-01)

| Candidate | Reason |
| --------- | ------ |
| NCCoE concept paper "Accelerating the Adoption of Software and AI Agent Identity and Authorization" (2026-02-05) | Requests comment; proposes no controls of its own. Revisit if the project publishes a practice guide. |
| NIST CAISI AI Agent Standards Initiative (launched 2026-02-17) | No finalized guidance published as of search; covered by S-005 to S-007. |
| MITRE ATLAS agentic techniques (AML.T0080 to AML.T0086) and CTID Secure AI v2 post (2026-05-06) | Technique IDs from secondary sources; atlas.mitre.org technique page returned 404; the CTID post names no specific mitigations. Revisit through the ATLAS data repository. |
| ASD "Careful adoption of agentic AI in cyber defence" (2026-07-24) | Page timed out; secondary sources describe it as restating S-004. Unverified. |
| ENISA "ENISA's view on Cybersecurity in the Frontier AI Era" (2026-07-07) | Seen via secondary source only; about machine-speed threats, not agent isolation. Not opened. |
| OWASP "Securing Agentic Applications Guide 1.0" | Mentioned by news coverage; the guide page was not surfaced in two searches. Revisit. |
| Mayer Brown, CSA, aicybr.com, infosecurity-magazine coverage of S-004 and S-008 | Secondary coverage. |
| Back-Reveal, "Your LLM Agent Can Leak Your Data" (2604.05432, ACL 2026) | Backdoored fine-tuned models; the abstract gives no concrete defense. The egress-quota idea appears only in the body (snippet). |
| BeyondTrust Phantom Labs, AWS Bedrock AgentCore Code Interpreter DNS covert channel (2026-03-16) | HTTP 403; seen in snippets and CSA notes only. Unverifiable for now; strong RQ4 candidate. Revisit, also Aurascape "Silent Leak". |
| Forward citations of R-002 not opened: ROPE (2608.27496), When Tool Outputs Become Commands (2608.27146), Twin Agent (2607.19595), Prismata (2607.08147), GIF (2606.23277), LACUNA (2605.28617), Janus (2607.01510), STARS (2604.10286) | Titles only from the Semantic Scholar list; not opened within budget. Revisit. |
| Steerability via constraints (2607.02389) | Title and snippet only; not opened. |
| WebCloak (IEEE S&P 2026), ExpShield (NDSS 2026) | Web scraping defenses; off-topic. |
| Joy Heron (INNOQ), "I Sandboxed My Coding Agents. You Should Too." (P-045, talk, 2026-03) | Removed in Step 2: talk page only, no written source to extract. |
