# Step 3 extraction

Files:

- `schema.json`: JSON Schema for `sources/extractions/<ID>.yaml`. Tag enums are
  generated from `vocabulary.yaml`; after editing the vocabulary run
  `scripts/validate_extractions.py --sync-schema` (the validator always uses the
  current vocabulary, the sync only keeps the file readable).
- `vocabulary.yaml`: seed tags. Anything else is written `other:<text>`.
- `prompt.md`: extractor prompt template, filled by the driver.
- `pilot.md`: pilot IDs and command.
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
satisfied. Choose the full-run model by comparing a cheaper model on the same
IDs (`--model <model>` writes the same paths, so move the opus records aside first).

## Full run and resume

```sh
scripts/extract_driver.py --model <model>
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
.venv/bin/python -m unittest discover -s extraction/tests   # self-test
```

Works on the host (venv present) and in the VM (after step 3).
