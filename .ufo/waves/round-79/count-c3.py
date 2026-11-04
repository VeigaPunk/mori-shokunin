#!/usr/bin/env python3
"""mori round-79 C3 counter (freshness, sourced): the RFC 9111 Vary row and its entry.

Frozen predicate P-C3 (contract `.ufo/waves/round-79/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R: `corpus/SOURCES.md` carries 367 registry rows (`^\\|\\s*S\\d{3,}\\s*\\|`),
  the new row `S594` reads status `mined`, its `source` cell names
  `https://www.rfc-editor.org/rfc/rfc9111.txt`, its anchor cell names
  `corpus/evidence/sources-r79/rfc9111.txt` and that blob's sha256 at R; its `used-by` cell
  names `corpus/knowledge/ua-serving-normative-r79.md`; the entry exists at R with
  `source:` naming S594, a `verified-at:` line and a `recheck:` line; and `corpus/README.md`
  carries a knowledge-index row naming the entry.

Usage: count-c3.py <rev> [--repo DIR] [--rows 367]
       count-c3.py --selftest
Output: one `item ...` line per graded item, then
  `C3=met|unmet rows=N row=<ok|bad> pin=<ok|bad> entry=<ok|bad> index=<ok|bad> rev=<sha12>`
Exit 0 met, 1 unmet, 2 setup. Read-only on the repo (`git show` only).
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

AXES_ROWS = 367
ROW = re.compile(r"^\s{0,3}\|\s*(S\d{3,})\s*\|")
SID = "S594"
URL = "https://www.rfc-editor.org/rfc/rfc9111.txt"
PIN = "corpus/evidence/sources-r79/rfc9111.txt"
ENTRY = "corpus/knowledge/ua-serving-normative-r79.md"


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def read_blob(repo, rev, path):
    p = run(["git", "-C", repo, "show", f"{rev}:{path}"])
    return p.stdout if p.returncode == 0 else None


def grade(repo, rev, want_rows):
    src = read_blob(repo, rev, "corpus/SOURCES.md") or ""
    readme = read_blob(repo, rev, "corpus/README.md") or ""
    entry = read_blob(repo, rev, ENTRY)
    pin = read_blob(repo, rev, PIN)
    rows = [m.group(1) for m in (ROW.match(l) for l in src.splitlines()) if m]
    items = [("rows", f"count={len(rows)} want={want_rows}")]
    row_ok = len(rows) == want_rows
    cells = None
    for line in src.splitlines():
        m = ROW.match(line)
        if m and m.group(1) == SID:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            break
    row_state = "missing"
    if cells and len(cells) >= 11:
        _, source, _kind, _tier, _scope, anchor, _teaches, status, _opened, _recheck, used = cells[:11]
        row_state = "ok"
        for name, cond in (("url", URL in source), ("status", status == "mined"),
                           ("anchor", PIN in anchor),
                           ("used_by", ENTRY in used)):
            if not cond:
                row_state = f"bad:{name}"
                break
    elif cells:
        row_state = "bad:columns"
    if row_ok and row_state != "ok":
        row_ok = False
    items.append(("row", row_state))

    pin_ok = False
    if pin is not None:
        blob_sha = hashlib.sha256(pin.encode()).hexdigest()
        declared = re.findall(r"\b[0-9a-f]{64}\b", (cells or ["", "", "", "", "", ""])[5]) \
            if cells else []
        declared_entry = re.findall(r"\b[0-9a-f]{64}\b", entry or "")
        pin_ok = blob_sha in declared or blob_sha in declared_entry
    items.append(("pin", "ok" if pin_ok else ("missing" if pin is None else "sha_mismatch")))

    entry_ok = bool(entry) and f"source:" in entry and SID in entry \
        and "verified-at:" in entry and "recheck:" in entry
    items.append(("entry", "ok" if entry_ok else ("missing" if entry is None else "bad")))
    index_ok = "ua-serving-normative-r79.md" in readme
    items.append(("index", "ok" if index_ok else "missing"))
    met = row_ok and pin_ok and entry_ok and index_ok
    return {"met": met, "items": items, "rows": len(rows), "row": row_state,
            "pin": items[2][1], "entry": items[3][1], "index": items[4][1]}


def _sources(rows, sid_row):
    head = ("# SOURCES\n\n## Registry\n\n| id | source | kind | tier | scope | anchor |"
            " teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    body = "".join(
        f"| S{100+i:03d} | t — https://example.invalid/{i} | docs | A | s | a:1 | t | mined |"
        f" 2026-11-04 | 180d | corpus/knowledge/x.md |\n" for i in range(rows - 1))
    return head + body + sid_row + "\n"


def selfcheck(scratch):
    pin_text = "RFC 9111 fixture body\nSection 4.1 Calculating Cache Keys\n"
    sha = hashlib.sha256(pin_text.encode()).hexdigest()
    good_row = (f"| S594 | HTTP Caching (RFC 9111) §4.1 — {URL} | spec | A | the Vary-selected"
                f" representation | §4.1:1-2; sha256 {sha}; copy {PIN} | a Vary-nominated request"
                f" header field selects among stored representations | mined | 2026-11-04 | 365d"
                f" | {ENTRY} |")
    entry = ("# entry\nsource: S594\nverified-at: 2026-11-04\nrecheck: 365d\n")
    cases = [
        ("conformant_met", good_row, entry, True),
        ("queued_status_unmet", good_row.replace("| mined |", "| queued |", 1), entry, False),
        ("pin_sha_unmet", good_row.replace(sha, "0" * 64), entry, False),
        ("entry_missing_unmet", good_row, None, False),
    ]
    ok = 0
    for label, row, ent, expect in cases:
        d = tempfile.mkdtemp(dir=scratch)
        repo = os.path.join(d, "repo")
        os.makedirs(os.path.join(repo, "corpus", "evidence", "sources-r79"))
        os.makedirs(os.path.join(repo, "corpus", "knowledge"))
        open(os.path.join(repo, "corpus", "SOURCES.md"), "w").write(_sources(367, row))
        open(os.path.join(repo, "corpus", "README.md"), "w").write(
            "# corpus\n\n| Note | Holds | Sources |\n|---|---|---|\n"
            "| `knowledge/ua-serving-normative-r79.md` | x | S594 |\n")
        open(os.path.join(repo, "corpus", "evidence", "sources-r79", "rfc9111.txt"), "w").write(pin_text)
        if ent is not None:
            open(os.path.join(repo, ENTRY), "w").write(ent)
        env = ["-c", "user.name=t", "-c", "user.email=t@t"]
        run(["git"] + env + ["-C", repo, "init", "-q"])
        run(["git"] + env + ["-C", repo, "add", "-A"])
        run(["git"] + env + ["-C", repo, "commit", "-qm", "fixture"])
        rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
        r = grade(repo, rev, AXES_ROWS)
        if r["met"] == expect:
            ok += 1
            print(f"PASS {label} met={r['met']}")
        else:
            print(f"FAIL {label} want_met={expect} got={r}")
    print(f"C3_COUNTER_SELFTEST pass={ok} fail={len(cases)-ok}")
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--rows", type=int, default=AXES_ROWS)
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = tempfile.gettempdir()
    scratch = tempfile.mkdtemp(prefix="count-c3-r79-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C3_SETUP usage: count-c3.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        if top.returncode == 0:
            a.repo = top.stdout.strip()
        p = run(["git", "-C", a.repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"C3_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        r = grade(a.repo, rev, a.rows)
        for k, v in r["items"]:
            print(f"item {k} {v}")
        print(f"C3={'met' if r['met'] else 'unmet'} rows={r['rows']} row={r['row']} "
              f"pin={r['pin']} entry={r['entry']} index={r['index']} rev={rev[:12]}")
        return 0 if r["met"] else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
