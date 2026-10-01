# Step 3 extraction

Files:

- `schema.json`: JSON Schema for `sources/extractions/<ID>.yaml`. Tag enums are
  generated from `vocabulary.yaml`; after editing the vocabulary run
  `scripts/validate_extractions.py --sync-schema` (the validator always uses the
  current vocabulary, the sync only keeps the file readable).
- `vocabulary.yaml`: seed tags. Anything else is written `other:<text>`.
- `prompt.md`: extractor prompt template, filled by the driver.
- `pilot.md`: pilot IDs, status, and re-run command.
- `pilot_review.md`: review of the first pilot (v1) and the changes it led to.
- `tests/`: validator unit tests and fixture.

## Setup inside CodeVM

The VM has no host mounts; code arrives by git, and `sources/corpus/` is
gitignored. So:

1. On the host, commit and push; in the VM, clone or pull into `~/projects/CodeVM`.
2. On the host, copy the clean texts into the VM checkout:
   `isolation_research/scripts/push_corpus_to_vm.sh` (argument: repo path under
   `/home/agent`, default `projects/CodeVM`).
3. In the VM, create a venv for validation (needs PyPI egress):
   ```sh
   cd ~/projects/CodeVM/isolation_research
   python3 -m venv .venv && .venv/bin/pip install pyyaml jsonschema
   .venv/bin/python -m unittest discover -s extraction/tests
   ```
   Without it, run the driver with `--no-validate` and validate on the host.
4. Log in to Claude Code in the VM (`claude` once, interactively).

## Pilot

See `pilot.md`. Check the commands first with `--dry-run`.

## Review

For each pilot record, compare against the source: missed recommendations,
wrong stances, tags forced into a poor fit, frequent `other:` values (promote
them into `vocabulary.yaml`), unhelpful fields. Revise `vocabulary.yaml`,
`schema.json`, and `prompt.md`, delete the pilot records, and re-run until
satisfied. To keep an earlier round for comparison, move its records into a
subfolder (as with `sources/extractions/pilot_v1/`); the driver and validator
only look at the top level of `sources/extractions/`. Full-run model: Opus
(`claude-opus-5-5`), per `pilot_review.md`.

## Record fields added after the pilot

- `qualifier` (optional): `weakening-option`, `default-config`, `as-sole-control`,
  `future-work`. A warning against a weakening option of an endorsed practice is
  `recommends` + `weakening-option`, not `rejects`.
- `claim_kind` (optional): `recommendation`, `limitation`, `measured-result`;
  lets Step 4 collapse several entries per practice.
- `boundary_strength` (optional, RQ2 entries): `security-boundary`,
  `defense-in-depth`, `convenience`, `unstated`.
- `threats` may be empty; non-security design choices are not extracted.
- `threat_model.framework`: short name in `value`, explanation in `details`.
- `threat_model.assets[].tag` and `input_channels[].tag` (required): from
  `asset_tags` / `channel_tags`, or `other:<text>`.
- `contested_positions[]` (optional): `topic` from `contested_topics` (the Step 5
  contested points plus host-delayed execution), `position`, `quote`, `location`.
- `date_normalized` (optional): `YYYY`, `YYYY-MM` or `YYYY-MM-DD`.

## Full run and resume

```sh
scripts/extract_driver.py --model claude-opus-5-5
```

The driver skips IDs that already have `sources/extractions/<ID>.yaml`, so
re-running resumes. Each run uses a fresh temp directory containing only
`corpus/<ID>/clean.md`, with `claude -p --restricted --tools Read,Write
--permission-mode dontAsk --strict-mcp-config`. A failing record is
re-extracted once with the validator errors in the prompt; a second failure
leaves the record in `sources/extractions/failed/` and a row in
`sources/manual_check.md`. Sources over ~150k tokens (chars/4) are flagged
there and not run. Raw `claude` output goes to `sources/extractions/_logs/`
(gitignored). Commit and push the records from the VM, then pull on the host.

## Validate

```sh
.venv/bin/python scripts/validate_extractions.py            # all records
.venv/bin/python scripts/validate_extractions.py --ids P-002
.venv/bin/python scripts/validate_extractions.py --dir sources/extractions/pilot_v1
.venv/bin/python -m unittest discover -s extraction/tests   # self-test
```

Works on the host (venv present) and in the VM (after step 3).
