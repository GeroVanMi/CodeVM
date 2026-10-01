#!/usr/bin/env python3
"""Step 3 driver: run headless `claude -p` once per source, inside CodeVM.

For each ID (from sources/sources.csv) without sources/extractions/<ID>.yaml:
  1. Skip and flag on manual_check.md if clean.md is over --max-tokens (chars/4).
  2. Copy clean.md into a fresh, empty temp workdir and run `claude -p` there
     with only the Read and Write tools (restricted mode, no Bash, no web, no
     MCP, no user/project settings). The prompt names one input and one output.
  3. Stamp extracted_by/extracted_at, then validate with
     scripts/validate_extractions.py. On failure re-extract once (with the
     errors in the prompt); on a second failure keep the record under
     sources/extractions/failed/ and append the ID to manual_check.md.

Stdlib only. Validation needs pyyaml + jsonschema in --python (default:
isolation_research/.venv/bin/python, else python3).

Examples:
  scripts/extract_driver.py --model claude-opus-5-5 --ids P-002 R-007
  scripts/extract_driver.py --model claude-sonnet-5 --dry-run
"""
import argparse, csv, datetime as dt, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
EXTRACTIONS = SOURCES / "extractions"
FAILED = EXTRACTIONS / "failed"
LOGS = EXTRACTIONS / "_logs"
MANUAL = SOURCES / "manual_check.md"
PROMPT = ROOT / "extraction" / "prompt.md"
VOCAB = ROOT / "extraction" / "vocabulary.yaml"
VALIDATOR = ROOT / "scripts" / "validate_extractions.py"
MANUAL_HEADER = ("\n## Extraction (Step 3)\n\nFlagged by `scripts/extract_driver.py`.\n\n"
                 "| ID | Date | Model | Reason |\n| --- | --- | --- | --- |\n")


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def flag(rid, model, reason):
    text = MANUAL.read_text() if MANUAL.exists() else "# Manual Check\n"
    if "## Extraction (Step 3)" not in text:
        text = text.rstrip("\n") + "\n" + MANUAL_HEADER
    reason = reason.replace("|", "\\|").replace("\n", " ")[:400]
    text = text.rstrip("\n") + f"\n| {rid} | {now()} | {model} | {reason} |\n"
    MANUAL.write_text(text)
    print(f"  flagged on manual_check.md: {reason}")


def build_prompt(row, model, inp, out, errors=None):
    body = PROMPT.read_text().split("\n---\n", 1)[1]
    retry = ""
    if errors:
        retry = ("## Retry\n\nA previous attempt was rejected by the validator with these errors. "
                 "Fix them (especially: quotes must be exact copies from the input file):\n\n"
                 + "\n".join(f"- {e}" for e in errors[:40]))
    subs = {"INPUT": inp, "OUTPUT": out, "MODEL": model, "ID": row["id"], "TITLE": row["title"],
            "AUTHOR_ORG": row["author_org"], "DATE": row["date"], "STREAM": row["stream"],
            "SUB_STREAM": row["sub_stream"], "HARNESS": row["harness"], "URL": row["url"],
            "VOCABULARY": VOCAB.read_text().strip(), "RETRY_NOTE": retry}
    for k, v in subs.items():
        body = body.replace("{{" + k + "}}", v)
    return body


def claude_cmd(args, prompt):
    return [args.claude, "-p", prompt,
            "--model", args.model,
            "--restricted", "--strict-mcp-config",
            "--tools", "Read,Write",
            "--allowedTools", "Read", "Write",
            "--disallowedTools", "Bash", "Edit", "WebFetch", "WebSearch", "NotebookEdit", "Agent",
            "--permission-mode", "dontAsk",
            "--max-turns", str(args.max_turns),
            "--output-format", "json"]


def stamp(path, model):
    """Force extracted_by/extracted_at to the driver's values (text-level, stdlib only)."""
    lines = [l for l in path.read_text().splitlines()
             if not l.startswith(("extracted_by:", "extracted_at:"))]
    i = next((n + 1 for n, l in enumerate(lines) if l.startswith("id:")), 0)
    lines[i:i] = [f"extracted_by: {model}", f"extracted_at: \"{now()}\""]
    path.write_text("\n".join(lines) + "\n")


def validate(args, record, clean):
    r = subprocess.run([args.python, str(VALIDATOR), "--record", str(record), "--clean", str(clean)],
                       capture_output=True, text=True)
    errs = [l.strip()[2:] for l in r.stdout.splitlines() if l.strip().startswith("- ")]
    if r.returncode != 0 and not errs:
        errs = [(r.stderr or r.stdout).strip()[-400:] or "validator failed"]
    return r.returncode == 0, errs


def attempt(args, row, clean, errors, n):
    rid = row["id"]
    with tempfile.TemporaryDirectory(prefix=f"extract-{rid}-") as tmp:
        tmp = Path(tmp)
        inp = tmp / "corpus" / rid / "clean.md"
        out = tmp / "extractions" / f"{rid}.yaml"
        inp.parent.mkdir(parents=True)
        out.parent.mkdir(parents=True)
        shutil.copyfile(clean, inp)
        cmd = claude_cmd(args, build_prompt(row, args.model, str(inp), str(out), errors))
        if args.dry_run:
            print("  cwd:", tmp)
            print("  cmd:", " ".join(repr(c) if " " in c else c for c in cmd[:2]),
                  "<prompt %d chars>" % len(cmd[2]), " ".join(cmd[3:]))
            return None
        env = {k: v for k, v in os.environ.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN")}
        try:
            r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=args.timeout, env=env)
            log, rc = r.stdout + ("\n--- stderr ---\n" + r.stderr if r.stderr else ""), r.returncode
        except subprocess.TimeoutExpired:
            log, rc = "timeout", -1
        LOGS.mkdir(parents=True, exist_ok=True)
        (LOGS / f"{rid}.attempt{n}.json").write_text(log)
        if not out.exists():
            return None, [f"no output file written (claude exit {rc})"]
        dest = tmp / "result.yaml"
        shutil.move(out, dest)
        stamp(dest, args.model)
        ok, errs = validate(args, dest, clean) if not args.no_validate else (True, [])
        final = (EXTRACTIONS / f"{rid}.yaml") if ok else (FAILED / f"{rid}.yaml")
        final.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dest, final)
        if ok:
            (FAILED / f"{rid}.yaml").unlink(missing_ok=True)
        return ok, errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="e.g. claude-opus-5-5")
    ap.add_argument("--ids", nargs="*", help="only these IDs (default: all in sources.csv)")
    ap.add_argument("--max-tokens", type=int, default=150_000, help="flag sources above this (chars/4)")
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per claude run")
    ap.add_argument("--claude", default="claude")
    default_py = ROOT / ".venv" / "bin" / "python"
    ap.add_argument("--python", default=str(default_py) if default_py.exists() else "python3")
    ap.add_argument("--no-validate", action="store_true", help="skip validation (validate later on the host)")
    ap.add_argument("--dry-run", action="store_true", help="print commands, run nothing")
    args = ap.parse_args()

    if not args.no_validate and not args.dry_run:
        if subprocess.run([args.python, "-c", "import yaml, jsonschema"]).returncode != 0:
            sys.exit(f"{args.python} lacks pyyaml/jsonschema; see extraction/README.md or pass --no-validate")

    rows = list(csv.DictReader((SOURCES / "sources.csv").open(newline="")))
    if args.ids:
        wanted = set(args.ids)
        unknown = wanted - {r["id"] for r in rows}
        if unknown:
            sys.exit(f"unknown IDs: {' '.join(sorted(unknown))}")
        rows = [r for r in rows if r["id"] in wanted]

    done = flagged = failed = skipped = 0
    for row in rows:
        rid = row["id"]
        clean = SOURCES / "corpus" / rid / "clean.md"
        if (EXTRACTIONS / f"{rid}.yaml").exists():
            skipped += 1
            continue
        print(f"{rid}: {row['title'][:70]}")
        if not clean.exists():
            print("  clean.md missing (corpus not copied into the VM?)")
            failed += 1
            continue
        tokens = len(clean.read_text(errors="replace")) // 4
        if tokens > args.max_tokens:
            if not args.dry_run:
                flag(rid, args.model, f"~{tokens} tokens (chars/4) > {args.max_tokens}; not extracted")
            flagged += 1
            continue
        res = attempt(args, row, clean, None, 1)
        if args.dry_run:
            continue
        ok, errs = res
        if not ok:
            print(f"  attempt 1 failed ({len(errs)} errors); re-extracting")
            ok, errs = attempt(args, row, clean, errs, 2)
        if ok:
            print("  ok")
            done += 1
        else:
            failed += 1
            flag(rid, args.model, f"validation failed twice: {'; '.join(errs[:3])}")
    print(f"done {done}, skipped (existing) {skipped}, flagged long {flagged}, failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
