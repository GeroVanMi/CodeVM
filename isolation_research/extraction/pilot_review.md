# Step 3 pilot review

Review of the six pilot records (P-002, P-026, P-043, R-007, R-017, S-010) extracted by `claude-opus-5-5`. This file only proposes changes. `vocabulary.yaml`, `schema.json`, `prompt.md` and the records were left unchanged.

## Summary verdict

**The pilot passes, with fixes needed before the full run.** Quotes are verbatim, and they mostly support the claims they are attached to. Metadata is correct. No prompt-injection payloads were reported or seen. Coverage of the sources is good: no major recommendation was missed in the sections I checked. Three systematic problems would distort the Step 4 matrix if left alone:

1. **`rejects` is overloaded.** It is used both for "the practice is insufficient" and for "do not enable this weakening option of the practice". For example, P-002 #13 and #16 would show Anthropic as *rejecting* `os-sandbox`, and P-002 #14 as *rejecting* `filesystem-scoping`. This is the most important fix.
2. **Non-security content gets extracted, with threats forced onto it.** P-043 recs 4–6 are operational or functional design choices. After the retry the extractor attached made-up threats to them (`resource-abuse` for "sandboxes as cattle"), because `threats` has `minItems: 1`.
3. **Granularity varies.** Records range from 6 to 27 recommendations. S-010 splits governance advice into many `other:` tags, while R-007 has 7 `capability-policy-enforcement` entries that are partly one claim plus its measured results.

Opus is good enough, and I recommend it for the full run (see the model recommendation below): about $50 extra over Sonnet buys quality on the judgment-heavy fields.

## Per-record findings

I spot-checked about 5 recommendations per record against `clean.md` (grep and section reads). I read P-043 and P-026 almost completely, and P-002, S-010 and R-007 by section. For R-017 (3,836 lines) I only checked quotes and greps. A full scan for misses there was not possible.

### P-002 (Anthropic, sandboxed Bash tool docs), 23 recs

- **Metadata:** correct. The date "living, accessed 2026-09-30" is not an ISO date (see the schema proposals).
- **Correct:** #2 (states the sandbox is "not a complete isolation boundary"; good for RQ2/RQ7), #4 (default read allows `~/.aws/credentials`, `~/.ssh`), #5/#6 (protected paths incl. `.git/hooks`, `.vscode`, `.idea`; this is good evidence for the host-delayed-execution blind spot), #8 credential masking, #11 (hostname allowlist, no TLS inspection).
- **Wrong stance or tag:**
  - #13 `os-sandbox rejects` (Docker socket) and #16 `os-sandbox rejects` (`allowAppleEvents`): the source recommends the sandbox and warns against specific weakening options. These should be `recommends` with a caveat, or carry a new `qualifier` (see the schema proposals).
  - #14 `filesystem-scoping rejects`: same problem.
  - #15 `container evaluates`: this is about `enableWeakerNestedSandbox` (bubblewrap nested inside a container), so it belongs under `os-sandbox` (a limit). It says nothing about containers as a boundary.
  - #12 quote "you can implement a custom proxy to:" is a dangling list intro. It is valid, but weak support.
  - #19 quote describes the escape hatch existing, not the recommendation to disable it.
- **Misses:**
  - The troubleshooting section tells users to add `docker *` and Go CLIs (`gh`, `gcloud`, `terraform`) to `excludedCommands`, which means running them unsandboxed. This is a vendor-recommended weakening and relevant to RQ2/RQ7.
  - Line 156: with filesystem isolation off, network egress stays confined. This is minor.
  - The pointer to the "Sandbox environments" page (dev containers / VMs comparison) is mentioned only in notes. That is fine.
- **Threat model:** thin. It has 1 input channel ("project settings") and no prompt injection, which is accurate because the page does not discuss PI.

### P-026 (Aonan Guan, CVE-2025-66479), 8 recs

- **Metadata:** correct. The date is not in the text, and notes say so.
- **Correct:** #1 (`allowedDomains: []` disabled restriction; exploit-demonstration) and #2 (config-semantics flaw, not a kernel escape) are both accurate. #4, #6 and #7 map one-to-one to the "Recommended Actions" list (lines 146–150). Verify-runtime-version is folded into #4. That is fine.
- **Wrong tag:**
  - #3 `egress-proxy-inspection`: this is the domain-filtering proxy, so it should be `egress-domain-allowlist` (or `egress-deny-all`). Nothing is inspected.
  - #8 "rotate credentials" tagged `scoped-short-lived-tokens`: this is incident response. A better fit is a new `incident-response` tag or `other:`.
  - #5 `other:transparent-vulnerability-disclosure` has `threats: [egress-bypass]`, which is forced.
- **Misses:** none important. One implicit lesson could be a rec: test that isolation actually holds, since the author found the bug by testing the config matrix. That maps to `red-teaming-evaluation` (evaluates), and it matters for the CodeVM implications.

### P-043 (Mendral, harness outside the sandbox), 6 recs

- **Metadata:** title, author and date are not in the text. Notes say so correctly.
- **Correct:** #1 `harness-outside-sandbox` and #2 `no-secrets-in-env` are the post's real security content. #3 (`harness-permissions rejects`: "no permission model to enforce") is a fair reading and useful for the contested point on whether harness permissions are a boundary.
- **Problems:**
  - #4 (sandboxes as cattle → `remote-ephemeral-env`, threat `resource-abuse`) and #5 (org-scoped memory DB → `multi-agent-trust-boundaries`) are operational or multi-user design, not security recommendations. The threats were forced after attempt 1 failed with empty `threats`.
  - #6 (bash bypasses the virtualization layer) is self-described as functional. Notes acknowledge this. It is OK as `evaluates`, but `permission-bypass` overstates it.
- **Misses:** none. The source is short.
- **Inclusion:** borderline but defensible. Keep it.

### R-007 (Progent, academic), 15 recs

- **Metadata:** correct. Notes add that v3 is dated 2026-05-14.
- **Correct:** #2 (ASB 70.3%→3.9%), #6 (PI detectors fail to generalize to AgentDojo, high FP; key evidence for the contested point on classifiers), #7 (prompt-level defenses ineffective), and #14 (proxy mode cannot protect built-in tools) all match the text. The limitation "users who incorrectly approve widening updates" is captured in #8 `bypasses_limits`.
- **Issues:**
  - Five of the 7 `capability-policy-enforcement` entries are the same practice with different evidence: design, results, formal guarantee, manual policies. That inflates the matrix count. A `claim_kind` / evidence grouping would help (see the schema proposals).
  - Quotes use ` ... ` across PDF line breaks a lot ("Progent also significantly ... reduces ASR"). They are valid, but the ellipses could hide context. Spot checks were fine.
- **Misses:** none important. The "Defense Scope" limitation (text-only attacks not covered) is not recorded but is minor.

### R-017 (Chu, systematic survey), 26 recs

- **Metadata:** author and affiliation are correct. CSV date 2026-04-25 vs text v2 2026-05-06 is noted.
- **Correct:** #4 (classifiers insufficient), #6 (per-call checks miss semantic privilege escalation), #11 (non-transferability), #17 (SBOM incomplete). The Maloyan coding-agent citation (line 1382) is captured as a failure mode.
- **Issues:**
  - #8 `other:tool-sandboxing-unspecified` and #9 `other:egress-restriction-unspecified` reflect a real vocabulary gap: there is no tag for an unspecified sandbox or unspecified egress restriction (see the vocabulary proposals).
  - Most recs are `design-rationale` or `citation`. That is right for a survey, but Step 5 needs to know they are second-hand.
- **Could not check:** a full scan for misses in this 3,836-line source. Greps for container, VM, Docker, egress, allowlist and secret found no isolation-technology content the record omitted, which is consistent with the notes.

### S-010 (ANSSI–BSI), 27 recs

- **Metadata:** correct. "Last updated: September 2024" vs CSV 2024-10-04 is noted. `harness: []` is correct.
- **Correct:** the key recommendations (lines 57–66, 4.1, 4.2) are all captured, including #20 sandboxing the dev environment (line 389) and #21 SBOM.
- **Issues:**
  - Granularity is too fine. #8 and #9 (provider responsible / ask provider) are one recommendation. #11 and #12 share `other:user-awareness-training`. #1–#4 and #7 are all `data-governance`.
  - #25 `human-in-the-loop` for "no substitute for experienced developers" is a loose fit. `code-review-integrity` or `other:` would be better.
  - The `other:` tags are many and ad hoc (see below).
- **Misses:** none found.

## Cross-record consistency

| Concept | Tagged as | Proposal |
|---|---|---|
| "Do not enable weakening option X" | `rejects` on the parent practice (P-002 #13, #14, #16) | `recommends` the parent practice plus `qualifier`, or a new stance (see the schema proposals) |
| Sandbox of unspecified type | `other:tool-sandboxing-unspecified` (R-017), `other:sandboxed-dev-environment` (S-010) | new tag `sandbox-unspecified` |
| Egress restriction of unspecified type | `other:egress-restriction-unspecified` (R-017) | new tag `egress-restriction-unspecified` |
| Domain-filtering proxy | `egress-proxy-inspection` (P-026 #3) vs `egress-domain-allowlist` (P-002 #10) | clarify the definition of `egress-proxy-inspection` (content inspection only) |
| Credential rotation after incident | `scoped-short-lived-tokens` (P-026) | new tag `incident-response` |
| Org memory / multi-user state | `multi-agent-trust-boundaries` (P-043) | the prompt should say not to extract non-security design choices |
| Training / guidelines / risk analysis | 5 different `other:` tags (S-010) | new tag `org-governance-training` |

**Granularity:** P-002 has 23 recs and P-043 has 6, which mostly reflects real source density. The problem is splitting inside one source: R-007 has 5 entries for one practice, and S-010 has 2 recs for one "provider responsibility" point. For the matrix (one cell per practice and source), duplicates are harmless if Step 4 collapses them by `(practice, stance)`. Collapsing does not work when one source has both `recommends` and `rejects` for the same practice, which is frequent because of problem 1 in the summary. Fixing the stance semantics solves most of this.

**Are the threat models useful for Step 4?** Partly.

- `framework` is null in 5 of 6 records. Only R-017 has one, and it is a long free-text string. Step 4 needs a short normalized name. Proposal: `framework.value` should be a short name, with details in a new optional `details` field.
- `assets` and `input_channels` are free text with no tags, so Step 4 cannot count them per stream without a second normalization pass. Proposal: optional controlled `asset_tags` and `channel_tags` (see below), or accept an LLM normalization step in Step 4.
- `failure_modes[].threat` is tagged and countable. This is the part that is most useful today.
- P-043 has an empty `input_channels`. That is honest, since the source has none.

## Proposed vocabulary diff

```diff
 practice_tags:
+  sandbox-unspecified: Source recommends sandboxing/isolating execution without naming a technology.
+  egress-restriction-unspecified: Source recommends restricting outbound network without specifying deny-all vs allowlist.
+  incident-response: Detect and respond after compromise (rotate credentials, review logs, audit what ran).
+  org-governance-training: Organizational policy, usage guidelines, risk analysis, user training/awareness.
+  vendor-disclosure-transparency: Vendors issuing CVEs/advisories; users obtaining vendor security commitments.
+  model-level-robustness: Model training/fine-tuning against prompt injection or insecure code (e.g. SecAlign).
+  memory-integrity-controls: Provenance/access control on persistent agent memory.
-  egress-proxy-inspection: Route egress via a proxy that inspects or filters requests.
+  egress-proxy-inspection: Route egress via a proxy that inspects request CONTENT (TLS termination, DLP). Plain hostname filtering is egress-domain-allowlist.
-  container: Container isolation (Docker, Podman, devcontainer) on a shared kernel.
+  container: Container isolation (Docker, Podman, devcontainer) on a shared kernel as the agent's boundary (not merely the place a nested sandbox runs).

 threat_tags:
+  lateral-movement: Reaching internal network/services from the agent environment.
+  memory-poisoning: Injected content persisted in agent memory and acting in later sessions.
```

- `other:` tags seen (17): managed-settings-enforcement, transparent-vulnerability-disclosure, bash-command-parsing-guard, model-level-pi-finetuning, tool-call-proxy-enforcement, tool-sandboxing-unspecified, egress-restriction-unspecified, defense-in-depth, memory-integrity-controls, runtime-attestation-tee, regulatory-mandates, systematic-risk-analysis, provider-responsibility-for-pi, ask-provider-about-pi-mitigations, restrict-image-rendering-to-trusted-sources, user-awareness-training (×2), automated-testing-and-vuln-scanning, security-hardening-of-code-models, flag-ai-generated-code, provider-training-data-security, usage-guidelines, adoption-evaluation-metrics. Threats: other:lateral-movement, other:cross-session-memory-poisoning.
- **Keep as `other:`:** `defense-in-depth` is a meta-claim, so it fits better in notes or a `qualifier`. `runtime-attestation-tee`, `regulatory-mandates` and `flag-ai-generated-code` are single-source items.
- **Map existing tags:** `managed-settings-enforcement` → `harness-permissions` (add "incl. admin-enforced/managed settings" to its definition). `tool-call-proxy-enforcement` → `capability-policy-enforcement`. `restrict-image-rendering` → `egress-domain-allowlist`/data exfil. Keep it as `other:` only if a second source uses it. `automated-testing-and-vuln-scanning` → `code-review-integrity` (widen its definition to "review or automated testing/scanning").
- **Removals:** none yet. `gvisor-userspace-kernel`, `resource-limits`, `egress-deny-all` (used once), `secret-scanning`, `prompt-injection-direct` and `sandbox-escape` are unused or rare in 6 sources but likely to appear in the full corpus. Revisit after the run.

## Proposed schema and prompt diff

**Schema**

1. **Allow empty `threats`** (`minItems: 0`), and have the prompt say "empty if the source ties it to no threat; do not invent one". Forced threats (P-043 #4, P-026 #5) are worse than none. Keep `rqs` at minItems 1.
2. **Add `qualifier` (optional string, enum-ish):** `default-config`, `weakening-option`, `as-sole-control`, `future-work`. Alternative: add a stance `warns-against-weakening`. Either option fixes the `rejects` overloading. My preference is the qualifier, because it keeps the stance enum at three values for the matrix.
3. **Add `claim_kind` (optional enum):** `recommendation`, `limitation`, `measured-result`. This lets Step 4 collapse R-007-style duplicates and lets Step 5 pull "limits" for contested points.
4. **Add `boundary_strength` (optional enum) for RQ2 recs:** `security-boundary`, `defense-in-depth`, `convenience`, `unstated`. This directly feeds the contested point "harness permissions: boundary or convenience?", and the shared-kernel vs VM question (P-002 #2, P-043 #3 have this information only in prose).
5. **`date`:** add an optional `date_normalized` matching `^\d{4}(-\d{2}(-\d{2})?)?$`, and keep `date` as-is. P-002's "living, accessed …" breaks sorting.
6. **`threat_model.framework`:** add optional `details`, and say `value` must be a short name.
7. **Optional, cheap for Step 4:** `contested_positions[]`. Each item has `topic` (enum of the 4 contested points + `host-delayed-execution`) plus `position` and `quote`. The prompt already asks for "special attention" to these, but nothing in the schema captures them, so they get spread across recs and notes.

**Validator**

- Normalize soft-hyphen line breaks (`"AI-\ngenerated"` → `"AI-generated"`) before quote matching. This was the S-010 attempt-1 failure. Also consider joining across PDF line breaks so fewer ` ... ` splices are needed.

**Prompt**

- Define the stances precisely: "`rejects` = the source says the practice itself is ineffective or insufficient. Warnings against weakening options of a practice the source otherwise endorses → `recommends` with `qualifier: weakening-option`."
- Add: "Extract only security-relevant recommendations. Skip operational, performance or UX design choices even if prominent. Mention them in notes if relevant."
- Add: "Merge restatements of the same recommendation within one source. Use separate entries only for different claims (e.g. a recommendation vs its measured result vs its limitation, tagged via `claim_kind`)."
- Add: "Prefer the quote sentence that states the recommendation, not one describing the mechanism, and avoid quotes ending in a dangling list intro." (P-002 #12, #19)
- Add tag-boundary hints: the `egress-proxy-inspection` vs `egress-domain-allowlist` distinction, and `container` only when the container is the boundary.
- Add: "Avoid quotes that span a hyphenated line break."

## Model recommendation

Run data from `_logs/*.json` (the logs record costs at Opus 5.5 rates of $4/$20 per MTok with 1h cache writes; this reproduces the logged cost):

| ID | chars | attempts | duration (s) | output tok | cost (USD) |
|---|---|---|---|---|---|
| P-026 | 9.4k | 1 | 37 | 4.2k | 0.19 |
| P-043 | 11.0k | 2 | 43 + 37 | 4.8k + 4.0k | 0.21 + 0.18 |
| S-010 | 46.7k | 2 | 83 + 100 | 10.3k + 12.4k | 0.47 + 0.52 |
| P-002 | 61.2k | 1 | 115 | 12.3k | 0.58 |
| R-007 | 97.7k | 1 | 102 | 11.3k | 0.72 |
| R-017 | 190.2k | 1 | 188 | 22.4k | 1.38 |
| **Total** | 416k | 8 runs | 705 s (11.8 min) | | **4.24** (3.53 first attempts) |

**Extrapolation:**

- **Cost model.** A linear fit of first attempts gives cost ≈ $0.13 + $0.66 per 100k chars.
- **Remaining corpus.** 96 sources, 4.81M chars (largest: R-001 362k and S-011 352k chars, ≈ 90k tokens each, under the 150k flag).
- **Opus, first attempts:** ≈ 96 × 0.13 + 48.1 × 0.66 ≈ **$44**.
- **Opus with retries.** The pilot retry rate was 2/6. Should the proposed validator and prompt fixes not reduce it, budget **≈ $50–55**.
- **Opus wall time:** ≈ 2–2.5 h sequential.
- **Sonnet 5.5** ($2/$10, half Opus 5.5 per token): ≈ **$25–30**, assuming similar token counts. That assumption is not measured.

**Recommendation: Opus 5.5 for the full run.**

- The saving is only about $25. The extracted fields that matter most need judgment: stance, tag choice, `boundary_strength`, contested positions. Even Opus got these wrong in systematic ways, so a weaker model would add review time worth far more than $25.
- Retries were caused by schema and validator issues, not by model weakness. Both failures are fixed by the proposals above, so they are not an argument for or against either model.
- Optional cheap check before committing: run Sonnet 5.5 on 2 pilot sources (e.g. P-002 and S-010) and diff stances and tags against Opus. Sonnet would be acceptable if it matches on more than ~85% of (practice, stance) pairs.
- Note on effort settings: Opus 5.5's default effort is `medium`, while Sonnet 5.5 defaults to `high`. Set the effort explicitly in the driver either way.

## Open questions for the user

1. Stance fix: should it be a new `qualifier` field (my preference) or a fourth stance value?
2. Should `threats` be allowed empty, or should non-threat-specific recs be dropped instead?
3. Do you want controlled tags for assets and input channels now, or an LLM normalization pass in Step 4?
4. Should `contested_positions[]` be added to the schema? It costs a little extraction effort and saves Step 5 work.
5. Should the pilot records be re-extracted after the schema and prompt changes, for consistency? Expected cost ≈ $4.
6. Should P-043 stay included? Its security content is one paragraph.
7. Should the Sonnet two-source comparison be run before the full run?
