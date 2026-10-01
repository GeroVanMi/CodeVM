#!/usr/bin/env python3
"""Download every source in sources/sources.csv once and normalize it to clean.md.

Layout: sources/corpus/<ID>/raw.<ext> + clean.md; writes sources/manifest.csv and
sources/manual_check.md. Run with isolation_research/.venv/bin/python.
"""
import argparse, csv, datetime as dt, hashlib, json, re, sys, time
import urllib.robotparser as robotparser
from pathlib import Path
from urllib.parse import urlparse

import pymupdf as fitz
import requests
import trafilatura

BASE = Path(__file__).resolve().parent.parent / "sources"
CORPUS = BASE / "corpus"
UA = ("CodeVM-isolation-research-fetcher/1.0 (one-time download of cited sources for a "
      "literature review; contact gerome.meyer@pm.me)")
BAD_DOMAINS = ["x.com", "twitter.com", "linkedin.com", "youtube.com", "youtu.be",
               "vimeo.com", "facebook.com", "instagram.com", "tiktok.com"]
LOGIN_HINTS = ["login", "signin", "sign-in", "sign_in", "auth", "paywall", "subscribe", "sso"]
MANIFEST_COLS = ["id", "url", "final_url", "fetch_date", "http_status", "sha256",
                 "extraction_method", "clean_length", "changed", "flag"]
RAW_EXTS = ["pdf", "html", "md", "txt", "json"]


def host_of(url):
    return (urlparse(url).hostname or "").lower()


def domain_match(host, domains):
    return any(host == d or host.endswith("." + d) for d in domains)


class Fetcher:
    def __init__(self, delay, timeout, retries):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.delay, self.timeout, self.retries = delay, timeout, retries
        self.last = {}
        self.robots = {}

    def allowed(self, url):
        p = urlparse(url)
        key = f"{p.scheme}://{p.netloc}"
        if key not in self.robots:
            rp = robotparser.RobotFileParser()
            try:
                self.wait(p.netloc)
                r = self.s.get(key + "/robots.txt", timeout=self.timeout)
                rp.parse(r.text.splitlines() if r.status_code == 200 else [])
            except requests.RequestException:
                rp.parse([])
            self.robots[key] = rp
        return self.robots[key].can_fetch(UA, url)

    def wait(self, netloc):
        t = self.last.get(netloc, 0) + self.delay - time.time()
        if t > 0:
            time.sleep(t)
        self.last[netloc] = time.time()

    def get(self, url):
        err = None
        for attempt in range(self.retries + 1):
            self.wait(urlparse(url).netloc)
            try:
                r = self.s.get(url, timeout=self.timeout, allow_redirects=True)
                if r.status_code in (429, 500, 502, 503, 504) and attempt < self.retries:
                    time.sleep(2 ** attempt * 2)
                    continue
                return r
            except requests.RequestException as e:
                err = e
                time.sleep(2 ** attempt * 2)
        raise err


def rewrite(url):
    """Return (fetch_url, kind) with full-text-friendly rewrites."""
    p = urlparse(url)
    h = host_of(url)
    if h == "arxiv.org":
        m = re.match(r"/(abs|pdf|html)/([^?#]+?)(\.pdf)?$", p.path)
        if m:
            return f"https://arxiv.org/pdf/{m.group(2)}", "pdf"
    if h == "github.com":
        parts = p.path.strip("/").split("/")
        if len(parts) >= 5 and parts[2] == "blob":
            return f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/{'/'.join(parts[3:])}", "text"
        if len(parts) == 2:
            return f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/HEAD/README.md", "text"
    if h == "news.ycombinator.com":
        m = re.search(r"id=(\d+)", p.query)
        if m:
            return f"https://hn.algolia.com/api/v1/items/{m.group(1)}", "hn"
    if h == "cveawg.mitre.org":
        return url, "json"
    return url, "auto"


def hn_to_md(data):
    out = []
    def walk(node, depth):
        if node.get("title"):
            out.append(f"# {node['title']}\n\n{node.get('url') or ''}\n")
        text = node.get("text")
        if text:
            plain = trafilatura.utils.sanitize(re.sub(r"<[^>]+>", " ", text.replace("<p>", "\n\n"))) or ""
            out.append(f"{'  ' * depth}- **{node.get('author')}**: {plain}")
        for c in node.get("children") or []:
            walk(c, depth + 1)
    walk(data, 0)
    return "\n".join(out)


def pdf_to_md(path):
    doc = fitz.open(path)
    return "\n\n".join(page.get_text("text") for page in doc)


def word_ratio(text):
    toks = text.split()
    if not toks:
        return 0.0
    good = sum(1 for t in toks if re.fullmatch(r"[A-Za-z][A-Za-z'\-]{1,}[.,;:)]?", t))
    return good / len(toks)


def normalize(d):
    """Normalize existing raw.* in dir d. Returns (method, clean_text, raw_path)."""
    raw = next((d / f"raw.{e}" for e in RAW_EXTS if (d / f"raw.{e}").exists()), None)
    if raw is None:
        return None, "", None
    ext = raw.suffix[1:]
    if ext == "pdf":
        return "pymupdf", pdf_to_md(raw), raw
    data = raw.read_text(errors="replace")
    if ext == "json":
        obj = json.loads(data)
        if isinstance(obj, dict) and "children" in obj and "author" in obj:
            return "hn-api", hn_to_md(obj), raw
        return "json", "```json\n" + json.dumps(obj, indent=2) + "\n```", raw
    if ext in ("md", "txt"):
        return "plain", data, raw
    text = trafilatura.extract(data, output_format="markdown", include_links=True,
                               include_tables=True, favor_recall=True) or ""
    if len(text) < FALLBACK_CHARS:
        alt = embedded_json_text(data)
        if alt and len(alt) > max(3 * len(text), 1000):
            return "embedded-json", alt, raw
    return "trafilatura", text, raw


FALLBACK_CHARS = 2000  # below this, try the embedded-JSON fallback


def embedded_json_text(html):
    """Fallback for client-rendered pages (Next.js __NEXT_DATA__, JSON-LD articleBody, other
    application/json payloads) whose body text is not in the DOM. Returns the longest string
    found in any embedded JSON script, rendered to markdown if it is HTML, or ''."""
    best, title = "", ""
    for m in re.finditer(r'<script[^>]*type="application/(?:ld\+)?json"[^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            obj = json.loads(m.group(1))
        except ValueError:
            continue
        stack = [obj]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                t = o.get("title") or o.get("headline") or o.get("name")
                for v in o.values():
                    if isinstance(v, str) and len(v) > len(best):
                        best, title = v, t if isinstance(t, str) and t != v else ""
                    else:
                        stack.append(v)
            elif isinstance(o, list):
                stack.extend(o)
            elif isinstance(o, str) and len(o) > len(best):
                best = o
    if re.search(r"<(p|div|h[1-6])[\s>]", best):
        best = trafilatura.extract(f"<html><body><article>{best}</article></body></html>",
                                   output_format="markdown", include_links=True,
                                   include_tables=True, favor_recall=True) or ""
    best = best.strip()
    return (f"# {title}\n\n{best}" if title and best else best)


def load_manifest():
    p = BASE / "manifest.csv"
    if not p.exists():
        return {}
    return {r["id"]: r for r in csv.DictReader(p.open())}


def check_flags(row, clean, method, args):
    flags = []
    if row.get("http_status") not in ("", "200", None):
        flags.append(f"HTTP status {row['http_status']}")
    fu = row.get("final_url") or ""
    if fu and fu != row["url"] and any(h in urlparse(fu).path.lower() + host_of(fu) for h in LOGIN_HINTS):
        flags.append(f"redirected to possible login/paywall: {fu}")
    if len(clean) < args.min_chars:
        flags.append(f"clean text too short ({len(clean)} < {args.min_chars} chars)")
    if method == "pymupdf" and clean and word_ratio(clean) < args.min_word_ratio:
        flags.append(f"PDF text looks like garbage (word ratio {word_ratio(clean):.2f} < {args.min_word_ratio})")
    return flags


def process(src, f, prev, args):
    sid, url = src["id"], src["url"]
    d = CORPUS / sid
    old = prev.get(sid, {})
    row = {"id": sid, "url": url, "final_url": old.get("final_url", ""),
           "fetch_date": old.get("fetch_date", ""), "http_status": old.get("http_status", ""),
           "sha256": "", "extraction_method": "", "clean_length": 0, "changed": "", "flag": ""}
    if src.get("license_status", "ok") == "excluded":
        row["flag"] = "excluded: " + src.get("license_note", "")
        return row, []
    have_raw = any((d / f"raw.{e}").exists() for e in RAW_EXTS)
    if not args.normalize_only and not have_raw:
        if domain_match(host_of(url), args.bad_domains):
            row["flag"] = "known-bad domain"
            return row, [f"known-bad domain ({host_of(url)}); not fetched"]
        furl, kind = rewrite(url)
        if not f.allowed(furl):
            row["flag"] = "robots"
            return row, [f"robots.txt disallows {furl}; not fetched"]
        try:
            r = f.get(furl)
        except requests.RequestException as e:
            row["flag"] = "error"
            return row, [f"request failed: {e.__class__.__name__}: {e}"]
        row.update(final_url=r.url, http_status=str(r.status_code),
                   fetch_date=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        if r.status_code != 200:
            row["flag"] = "http"
            return row, check_flags(row, "x" * args.min_chars, "", args)
        ctype = r.headers.get("content-type", "").lower()
        if kind == "pdf" or "pdf" in ctype or r.content[:5] == b"%PDF-":
            ext = "pdf"
        elif kind in ("hn", "json") or "json" in ctype:
            ext = "json"
        elif kind == "text" or "text/plain" in ctype or "markdown" in ctype:
            ext = "md"
        else:
            ext = "html"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"raw.{ext}").write_bytes(r.content)
    elif not have_raw:
        return row, ["no raw file present (normalize-only)"]
    elif not args.normalize_only:
        # already downloaded: keep the previous manifest row unchanged
        if old:
            return dict(old), [x for x in [old.get("flag")] if x and old.get("flag") != ""]
    method, clean, raw = normalize(d)
    (d / "clean.md").write_text(clean)
    sha = hashlib.sha256(raw.read_bytes()).hexdigest()
    row.update(sha256=sha, extraction_method=method, clean_length=len(clean))
    if old.get("sha256"):
        row["changed"] = "yes" if old["sha256"] != sha else "no"
    else:
        row["changed"] = "new"
    if args.normalize_only and not row["http_status"]:
        row["http_status"] = "manual"
        row["final_url"] = "manual"
    flags = check_flags(row if row["http_status"] != "manual" else {**row, "http_status": "200"},
                        clean, method, args)
    row["flag"] = "; ".join(flags)
    return row, flags


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ids", help="comma-separated IDs to process (default: all)")
    ap.add_argument("--normalize-only", action="store_true",
                    help="re-run normalization on existing raw files; no network")
    ap.add_argument("--min-chars", type=int, default=1500)
    ap.add_argument("--min-word-ratio", type=float, default=0.5)
    ap.add_argument("--delay", type=float, default=3.0, help="seconds between requests per domain")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--bad-domains", default=",".join(BAD_DOMAINS))
    args = ap.parse_args()
    args.bad_domains = [x.strip() for x in args.bad_domains.split(",") if x.strip()]

    sources = list(csv.DictReader((BASE / "sources.csv").open()))
    want = set(args.ids.split(",")) if args.ids else None
    prev = load_manifest()
    rows = dict(prev)
    f = Fetcher(args.delay, args.timeout, args.retries)
    for src in sources:
        if want and src["id"] not in want:
            continue
        row, flags = process(src, f, prev, args)
        if flags:
            row["flag"] = "; ".join(flags)
        rows[src["id"]] = row
        print(f"{src['id']}: {row.get('extraction_method') or '-'} len={row.get('clean_length')} "
              f"{'FLAG: ' + '; '.join(flags) if flags else 'ok'}", flush=True)

    order = [s["id"] for s in sources]
    with (BASE / "manifest.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, MANIFEST_COLS, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for i in order:
            if i in rows:
                w.writerow(rows[i])
    by_id = {s["id"]: s for s in sources}
    lines = ["# Manual Check", "",
             "Sources flagged by `scripts/fetch_sources.py`. Place a manual copy at",
             "`corpus/<ID>/raw.pdf` (or `raw.html`) and re-run with `--normalize-only --ids <ID>`.", "",
             "| ID | URL | Reason |", "| --- | --- | --- |"]
    for i in order:
        r = rows.get(i)
        if r and r.get("flag"):
            reason = r["flag"]
            lines.append(f"| {i} | {by_id[i]['url']} | {reason.replace('|', '/')} |")
    (BASE / "manual_check.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
