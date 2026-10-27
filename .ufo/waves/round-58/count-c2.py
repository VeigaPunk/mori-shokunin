#!/usr/bin/env python3
"""Round 58 C2 counter: quote-bound depth entry with pinned-copy identity.

Fixes round-57 routed defect 2 (quote predicate): the r57 depth counter never
read the source copy and accepted any backticked text, so a full false-green
fixture (junk quotes + a mined row) scored met. This counter requires:

  1. ENTRY: corpus/knowledge/driver-events-r58.md exists at R with frontmatter
     lines source: S550, verified-at: 2026-10-27, recheck: <cell>, and
     coverage-map: <cell>  (sources=ok).
  2. CLAIMS: >= 8 bullet lines '- **K<n>** ... (tools/mori-driver-liveness.py:L)'
     each carrying >= 1 backticked span that is a substring of pinned-copy
     line L  (located count; failed=quotes otherwise).
  3. COPY=TREE: sha256 of corpus/evidence/sources-r58/mori-driver-liveness.py
     at R equals sha256 of tools/mori-driver-liveness.py at R (copy=ok tree=ok).
  4. ROWS: SOURCES.md at R holds row S550, status mined, used-by naming the
     entry  (rows=ok).

Usage: count-c2.py R | --selftest.  Exit 0 met / 1 unmet / 2 setup.
Frozen at the round-58 freeze commit; the predicate sentence lives in
.ufo/waves/round-58/contract.md and changing either invalidates the claim.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ENTRY = "corpus/knowledge/driver-events-r58.md"
COPY = "corpus/evidence/sources-r58/mori-driver-liveness.py"
TOOL = "tools/mori-driver-liveness.py"
SOURCES = "corpus/SOURCES.md"
ROW_ID = "S550"
KLINE = re.compile(r"^- \*\*K(\d+)\*\*.*\((tools/mori-driver-liveness\.py):(\d+)\)")


def _git(*args, cwd=None):
    return subprocess.run(["git", "-C", str(cwd or LANE), *args], capture_output=True, text=True)


def _show(rev, path):
    p = _git("show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def _sha256(b):
    return hashlib.sha256(b.encode()).hexdigest()


def measure(rev):
    failed = []
    entry = _show(rev, ENTRY)
    if entry is None:
        print(f"C2=unmet entry=absent failed=entry rev={rev}")
        return 1
    # sources arm
    sources = "ok"
    for needle in ("source: S550", "verified-at: 2026-10-27", "recheck:", "coverage-map:"):
        if needle not in entry:
            sources = "bad"
            failed.append("sources")
            break
    # copy/tree arm
    copy = _show(rev, COPY)
    tool = _show(rev, TOOL)
    copy_arm = tree_arm = "ok"
    if copy is None or tool is None:
        copy_arm = tree_arm = "bad"
        failed.append("copy")
    elif _sha256(copy) != _sha256(tool):
        copy_arm = tree_arm = "bad"
        failed.append("copy")
    # claims/located arms
    claims = 0
    located = 0
    copy_lines = copy.splitlines() if copy is not None else []
    for ln in entry.splitlines():
        m = KLINE.match(ln.strip())
        if not m:
            continue
        claims += 1
        lineno = int(m.group(3))
        spans = re.findall(r"`([^`]+)`", ln)
        if 1 <= lineno <= len(copy_lines) and any(
                len(s) >= 12 and s in copy_lines[lineno - 1] for s in spans):
            located += 1
    if claims < 8:
        failed.append("claims")
    if located < claims:
        failed.append("quotes")
    # rows arm
    reg = _show(rev, SOURCES) or ""
    rows = "ok"
    row_lines = [ln for ln in reg.splitlines() if ln.startswith(f"| {ROW_ID} ")]
    if len(row_lines) != 1:
        rows = "bad"
        failed.append("rows")
    else:
        cells = [c.strip() for c in row_lines[0].split("|")]
        # cells[0] empty (leading |), then id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by
        if len(cells) < 12 or cells[8] != "mined" or ENTRY not in cells[11]:
            rows = "bad"
            failed.append("rows")
    ok = not failed
    state = "met" if ok else "unmet"
    print(f"C2={state} claims={claims} located={located} copy={copy_arm} tree={tree_arm} "
          f"rows={rows} sources={sources} failed={','.join(failed) or 'none'} rev={rev}")
    return 0 if ok else 1


# ---------------- selftest ----------------

TOOL_TEXT = "\n".join(
    f"line {i} def parse_log(text): open_launches bookkeeping #{i}" for i in range(1, 220)
) + "\n"

ENTRY_OK = """# fixture driver events

source: S550
verified-at: 2026-10-27
recheck: 90d
coverage-map: FR5 advance — fixture

""" + "\n".join(
    f"- **K{i}** the parser keeps event class {i}. (`open_launches bookkeeping #{10 + i}`) (tools/mori-driver-liveness.py:{10 + i})"
    for i in range(1, 9)
) + "\n"

ENTRY_JUNK = """# fixture

source: S550
verified-at: 2026-10-27
recheck: 90d
coverage-map: fixture

- **K1** q (`a fabricated quote that is not in the copy at all`) (tools/mori-driver-liveness.py:20)
- **K2** q (`another fabricated quote not present`) (tools/mori-driver-liveness.py:21)
- **K3** q (`third fabricated quote not present`) (tools/mori-driver-liveness.py:22)
- **K4** q (`fourth fabricated quote not present`) (tools/mori-driver-liveness.py:23)
- **K5** q (`fifth fabricated quote not present`) (tools/mori-driver-liveness.py:24)
- **K6** q (`sixth fabricated quote not present`) (tools/mori-driver-liveness.py:25)
- **K7** q (`seventh fabricated quote not present`) (tools/mori-driver-liveness.py:26)
- **K8** q (`eighth fabricated quote not present`) (tools/mori-driver-liveness.py:27)
"""

ENTRY_NO_FM = "\n".join(
    f"- **K{i}** c (`open_launches bookkeeping #{10 + i}`) (tools/mori-driver-liveness.py:{10 + i})"
    for i in range(1, 9)
) + "\n"

ROW_OK = ("| S550 | mori driver-liveness event classes — `tools/mori-driver-liveness.py` | own-work | A | "
          "event-class semantics of the per-event parser | `parse_log` lines 77-174; source copy "
          "`corpus/evidence/sources-r58/mori-driver-liveness.py` | Grounds the launch/complete/dead/launch-fail/wrap classes | "
          "mined | 2026-10-27 | 90d | corpus/knowledge/driver-events-r58.md |\n")
ROW_NO_USEDBY = ROW_OK.replace("corpus/knowledge/driver-events-r58.md", "—")


def _mkrepo(tmp, entry=None, copy_text=None, tool_text=TOOL_TEXT, row=None):
    d = tempfile.mkdtemp(dir=tmp)
    subprocess.run(["git", "init", "-q", d], check=True)
    os.makedirs(os.path.join(d, "corpus/knowledge"), exist_ok=True)
    os.makedirs(os.path.join(d, "corpus/evidence/sources-r58"), exist_ok=True)
    os.makedirs(os.path.join(d, "tools"), exist_ok=True)
    open(os.path.join(d, "tools/mori-driver-liveness.py"), "w").write(tool_text)
    if copy_text is not None:
        open(os.path.join(d, COPY), "w").write(copy_text)
    if entry is not None:
        open(os.path.join(d, ENTRY), "w").write(entry)
    header = ("# SOURCES\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
              "|---|---|---|---|---|---|---|---|---|---|---|\n")
    open(os.path.join(d, SOURCES), "w").write(header + (row or ""))
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return d, rev


def _run_selftest():
    global LANE
    keep = LANE
    tmp = tempfile.mkdtemp(prefix="mori-r58-c2-")
    cases = [
        ("conformant", dict(entry=ENTRY_OK, copy_text=TOOL_TEXT, row=ROW_OK), 0, "C2=met"),
        ("junk_quotes", dict(entry=ENTRY_JUNK, copy_text=TOOL_TEXT, row=ROW_OK), 1, "failed=quotes"),
        ("copy_sha_mismatch", dict(entry=ENTRY_OK, copy_text=TOOL_TEXT + "# drift\n", row=ROW_OK), 1, "copy=bad"),
        ("missing_frontmatter", dict(entry=ENTRY_NO_FM, copy_text=TOOL_TEXT, row=ROW_OK), 1, "sources=bad"),
        ("row_not_usedby", dict(entry=ENTRY_OK, copy_text=TOOL_TEXT, row=ROW_NO_USEDBY), 1, "rows=bad"),
        ("entry_absent", dict(entry=None, copy_text=TOOL_TEXT, row=ROW_OK), 1, "entry=absent"),
    ]
    passed = failed = 0
    from io import StringIO
    try:
        for name, kw, want_rc, want_tok in cases:
            d, rev = _mkrepo(tmp, **kw)
            LANE = d
            buf = StringIO()
            old = sys.stdout
            sys.stdout = buf
            try:
                rc = measure(rev)
            finally:
                sys.stdout = old
            out = buf.getvalue()
            if rc == want_rc and want_tok in out:
                passed += 1
            else:
                failed += 1
                print(f"case {name}: rc={rc} want={want_rc} out={out.strip()!r}", file=sys.stderr)
    finally:
        LANE = keep
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"C2_SELFTEST pass={passed} fail={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        raise SystemExit(_run_selftest())
    if len(sys.argv) != 2:
        print("usage: count-c2.py REV | --selftest", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(measure(sys.argv[1]))
