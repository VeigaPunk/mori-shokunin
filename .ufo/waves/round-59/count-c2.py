#!/usr/bin/env python3
"""Round 59 C2 counter (depth) — the wave-settlement results scanner is landed
at its frozen SHA, the depth entry `wave-settlement-artifacts-r59.md` carries
>=10 byte-exact pin-bound claims over >=3 distinct committed artifacts, every
cited S### registry row is mined with exact used-by binding, and the counter's
own hostile trees each fail for the reason they were frozen to fail.

Frozen predicate P-C2 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, tools/mori-settlement-scan.py exists with sha256 equal to
  PIN; its --selftest prints `SETSCAN_SELFTEST pass=10 fail=0` exit 0; run
  over the five REAL wave-results files materialized from R it exits 0 with
  verdict SETTLEMENT_SCAN_OK and every file's members==seats, while the
  DRIFT file exits nonzero (schema drift observed, reported);
  corpus/knowledge/wave-settlement-artifacts-r59.md exists at R with the
  four frontmatter keys in its first ten lines, >=10 claims in the frozen
  grammar `- **K<d>** — <text>. Quote: `<q>` (<file>:line:<n>|offset:<n>;
  pin <sha64>)`, all K ids distinct, every cited file one of the ARTIFACTS
  copies, every pin equal to the copy's sha256 at R, every line-span quote
  byte-equal to that copy's line n and every offset-span quote byte-equal
  to the copy's bytes at offset n; every copy file byte-equals its named
  .ufo artifact at R (tree=ok); every S### the entry's source lines cite is
  a registry row with status mined whose used-by cell names exactly this
  entry (rows=ok); and every tree under .ufo/waves/round-59/trees-c2/
  evaluates with verdict false and reason prefixes covering its frozen
  expect file (trees=ok).

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR]
       count-c2.py --selftest
Output: `C2=met|unmet selftest=.. scan=.. drift=.. trees=.. entry=..
  rows=.. pins=.. tree=.. claims=N files=F rev=R` (+ ` failed=`).  Exit 0
  met, 1 unmet, 2 setup.
Read-only on the lane: git show / ls-tree / cat-file only; materializes under
--scratch/TMPDIR.  Honors TMPDIR.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = "tools/mori-settlement-scan.py"
ENTRY = "corpus/knowledge/wave-settlement-artifacts-r59.md"
SOURCES = "corpus/SOURCES.md"
COPY_DIR = "corpus/evidence/sources-r59/"
TREES = ".ufo/waves/round-59/trees-c2"
EXPECT_SELFTEST = "SETSCAN_SELFTEST pass=10 fail=0"
MIN_CLAIMS = 10
MIN_FILES = 3
PIN = "4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9"  # frozen at freeze commit

ARTIFACTS = {
    "corpus/evidence/sources-r59/w1-results-r54.json":
        ".ufo/waves/round-54/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r55.json":
        ".ufo/waves/round-55/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r56.json":
        ".ufo/waves/round-56/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r57.json":
        ".ufo/waves/round-57/w1-results.json",
    "corpus/evidence/sources-r59/w1-results-r58.json":
        ".ufo/waves/round-58/w1-results.json",
    "corpus/evidence/sources-r59/w1-settlement-r58.json":
        ".ufo/waves/round-58/evidence/w1-settlement.json",
}
REAL_SCAN = [
    ".ufo/waves/round-54/w1-results.json",
    ".ufo/waves/round-55/w1-results.json",
    ".ufo/waves/round-56/w1-results.json",
    ".ufo/waves/round-57/w1-results.json",
    ".ufo/waves/round-58/w1-results.json",
]
DRIFT_SCAN = [".ufo/waves/round-53/w1-results.json"]

CLAIM = re.compile(
    r"^- \*\*K(\d+)\*\* — .+? Quote: `([^`]+)` "
    r"\((\S+?):(line|offset):(\d+); pin ([0-9a-f]{64})\)\s*$")
FRONTMATTER = ("source:", "verified-at:", "recheck:", "coverage-map:")
SID = re.compile(r"source:\s*(S\d+)")
ROW = re.compile(r"^\s{0,3}\|\s*(S\d{3,})\s*\|")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, timeout=120)


def git_show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def eval_entry(root):
    """Evaluate the entry grammar + sources binding under directory root.
    Returns (ok, reasons, stats)."""
    root = Path(root)
    reasons = []
    stats = {"claims": 0, "files": 0}
    ep = root / ENTRY
    try:
        text = ep.read_text(encoding="utf-8")
    except OSError:
        return False, ["entry_absent"], stats
    lines = text.splitlines()
    head = lines[:10]
    for k in FRONTMATTER:
        if not any(l.startswith(k) for l in head):
            reasons.append("frontmatter:%s" % k.rstrip(":"))
    claims = []
    seen = {}
    for ln in lines:
        m = CLAIM.match(ln)
        if not m:
            if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln):
                reasons.append("grammar:%.40s" % ln.strip()[:40])
            continue
        kid, quote, cfile, kind, n, pin = m.groups()
        if kid in seen:
            reasons.append("distinct:dup=K%s" % kid)
        seen[kid] = True
        claims.append((kid, quote, cfile, kind, int(n), pin))
    stats["claims"] = len(claims)
    if len(claims) < MIN_CLAIMS:
        reasons.append("claims_min:%d" % len(claims))
    files = sorted({c[2] for c in claims})
    stats["files"] = len(files)
    if len(files) < MIN_FILES:
        reasons.append("files_min:%d" % len(files))
    for f in files:
        if f not in ARTIFACTS:
            reasons.append("files:outside=%s" % f)
    for kid, quote, cfile, kind, n, pin in claims:
        fb_path = root / cfile
        if cfile not in ARTIFACTS:
            continue
        try:
            fb = fb_path.read_bytes()
        except OSError:
            reasons.append("pin:copy_absent=%s" % cfile)
            continue
        if sha256(fb) != pin:
            reasons.append("pin:%s" % kid)
        q = quote.encode("utf-8")
        if len(q) < 3:
            reasons.append("span:short=%s" % kid)
            continue
        if kind == "line":
            flines = fb.split(b"\n")
            if not (1 <= n <= len(flines)) or flines[n - 1] != q:
                reasons.append("span:%s" % kid)
        else:
            if fb[n:n + len(q)] != q:
                reasons.append("span:%s" % kid)
    sids = set()
    for l in head:
        sids.update(SID.findall(l))
    if not sids:
        reasons.append("rows:no_source_ids")
    try:
        reg = (root / SOURCES).read_text(encoding="utf-8")
    except OSError:
        reg = None
        reasons.append("rows:sources_absent")
    if reg is not None:
        for sid in sorted(sids):
            hit = None
            for ln in reg.splitlines():
                m = ROW.match(ln)
                if m and m.group(1) == sid:
                    hit = ln
                    break
            if hit is None:
                reasons.append("rows:missing=%s" % sid)
                continue
            cells = [c.strip() for c in hit.strip().strip("|").split("|")]
            if len(cells) != 11:
                reasons.append("rows:bad_row=%s" % sid)
                continue
            if cells[7] != "mined":
                reasons.append("rows:status=%s" % sid)
            if cells[10] != ENTRY:
                reasons.append("rows:usedby=%s" % sid)
    return (len(reasons) == 0), reasons, stats


def measure(repo, rev, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    failed = []
    detail = {"claims": 0, "files": 0}
    tool_b = git_show(repo, rev, TOOL)
    tool_ok = tool_b is not None and sha256(tool_b) == PIN
    if tool_b is None:
        failed.append("tool_absent")
    elif not tool_ok:
        failed.append("tool_sha")
    tp = scratch / "tool2.py"
    if tool_b is not None:
        tp.write_bytes(tool_b)

    st_ok = False
    if tool_b is not None:
        p = subprocess.run(["python3", str(tp), "--selftest",
                            "--scratch", str(scratch / "st2")],
                           capture_output=True, text=True, timeout=300,
                           env={**os.environ, "TMPDIR": str(scratch)})
        st_ok = p.returncode == 0 and EXPECT_SELFTEST in p.stdout
    detail["selftest"] = st_ok
    if not st_ok:
        failed.append("selftest")

    # real scan arm
    scan_ok = True
    rfiles = []
    for rel in REAL_SCAN:
        b = git_show(repo, rev, rel)
        if b is None:
            scan_ok = False
            failed.append("scan_absent:%s" % rel)
            continue
        f = scratch / "real2" / Path(rel).parent.name / Path(rel).name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
        rfiles.append(f)
    if tool_b is None or not rfiles:
        scan_ok = False
    else:
        p = subprocess.run(["python3", str(tp)] + [str(f) for f in rfiles],
                           capture_output=True, text=True, timeout=120)
        try:
            out = json.loads(p.stdout)
        except ValueError:
            out = None
        if not (p.returncode == 0 and out is not None
                and out.get("verdict") == "SETTLEMENT_SCAN_OK"
                and all(f.get("members") == f.get("seats")
                        for f in out.get("files", []))):
            scan_ok = False
            failed.append("scan")
    detail["scan"] = scan_ok
    if not scan_ok:
        failed.append("scan")

    # drift arm: r53 file must be judged FAIL
    drift_ok = False
    db = git_show(repo, rev, DRIFT_SCAN[0])
    if db is not None and tool_b is not None:
        f = scratch / "real2" / "round-53" / "w1-results.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(db)
        p = subprocess.run(["python3", str(tp), str(f)],
                           capture_output=True, text=True, timeout=120)
        drift_ok = p.returncode != 0
    detail["drift"] = drift_ok
    if not drift_ok:
        failed.append("drift")

    # tree arm: copies byte-equal their .ufo artifacts at R
    tree_ok = True
    for copy_rel, art_rel in ARTIFACTS.items():
        cb = git_show(repo, rev, copy_rel)
        ab = git_show(repo, rev, art_rel)
        if cb is None:
            tree_ok = False
            failed.append("copy_absent:%s" % copy_rel)
        elif ab is None:
            tree_ok = False
            failed.append("artifact_absent:%s" % art_rel)
        elif sha256(cb) != sha256(ab):
            tree_ok = False
            failed.append("tree:%s" % copy_rel)
    detail["tree"] = tree_ok
    if not tree_ok:
        failed.append("tree")

    # entry arm on a materialized root
    root = scratch / "root2"
    paths = [ENTRY, SOURCES] + sorted(ARTIFACTS)
    have_all = True
    for rel in paths:
        b = git_show(repo, rev, rel)
        if b is None:
            have_all = False
            continue
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b)
    if not have_all:
        entry_ok = rows_ok = pins_ok = False
        if git_show(repo, rev, ENTRY) is None:
            failed.append("entry_absent")
    else:
        entry_ok_all, reasons, stats = eval_entry(root)
        detail["claims"] = stats["claims"]
        detail["files"] = stats["files"]
        entry_ok = not any(r.startswith(("frontmatter", "distinct", "claims_min",
                                         "files", "span", "entry_absent"))
                           for r in reasons)
        rows_ok = not any(r.startswith("rows") for r in reasons)
        pins_ok = not any(r.startswith("pin") for r in reasons)
        if not entry_ok:
            failed.append("entry")
        if not rows_ok:
            failed.append("rows")
        if not pins_ok:
            failed.append("pins")
    detail["entry"] = entry_ok
    detail["rows"] = rows_ok
    detail["pins"] = pins_ok

    # hostile trees arm
    trees_ok = True
    listing = git(repo, "ls-tree", "--name-only", "%s:%s" % (rev, TREES))
    tdirs = [n for n in listing.stdout.decode().splitlines()
             if n] if listing.returncode == 0 else []
    if not tdirs:
        trees_ok = False
        failed.append("trees_absent")
    for name in tdirs:
        base = "%s/%s" % (TREES, name)
        exp_b = git_show(repo, rev, base + "/expect.txt")
        if exp_b is None:
            trees_ok = False
            failed.append("tree:%s:expect" % name)
            continue
        expect = [e for e in exp_b.decode().strip().split(",") if e]
        tr = scratch / "trees" / name
        tr.mkdir(parents=True, exist_ok=True)
        fl = git(repo, "ls-tree", "-r", "--name-only", rev, base + "/")
        for f in fl.stdout.decode().splitlines():
            rel = f[len(base) + 1:]
            if rel == "expect.txt":
                continue
            b = git_show(repo, rev, f)
            if b is not None:
                fp = tr / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_bytes(b)
        ok, reasons, _st = eval_entry(tr)
        want_ok = not expect
        if ok != want_ok:
            trees_ok = False
            failed.append("tree:%s:verdict" % name)
            continue
        if expect and not all(any(r.startswith(e) for r in reasons)
                              for e in expect):
            trees_ok = False
            failed.append("tree:%s:reasons" % name)
    detail["trees"] = trees_ok
    if not trees_ok:
        failed.append("trees")

    met = (tool_ok and st_ok and scan_ok and drift_ok and tree_ok
           and entry_ok and rows_ok and pins_ok and trees_ok)
    return met, sorted(set(failed)), detail


def selftest():
    passed = failed = 0

    def chk(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAIL " + name, file=sys.stderr)

    line_ok = ('- **K3** — seats equals members. Quote: `  "seats": 64,` '
               '(corpus/evidence/sources-r59/w1-results-r56.json:line:5; pin '
               + "a" * 64 + ")")
    m = CLAIM.match(line_ok)
    chk("claim_grammar", m is not None and m.groups()[:1] == ("3",)
        and m.group(4) == "line" and m.group(5) == "5")
    chk("claim_grammar_offset", CLAIM.match(
        line_ok.replace(":line:5;", ":offset:120;")) is not None)
    chk("claim_grammar_nopin", CLAIM.match(line_ok.replace("; pin " + "a" * 64, "")) is None)
    chk("min_claims", MIN_CLAIMS == 10)
    chk("artifacts_inside", all(v.startswith(".ufo/") for v in ARTIFACTS.values()))
    chk("real_scan_count", len(REAL_SCAN) == 5)
    chk("row_re", ROW.match("| S123 | x |") is not None
        and ROW.match("   | S123 | x |") is not None)
    # functional: synthetic good tree passes, frontmatter-less fails
    import shutil
    base = Path(tempfile.mkdtemp(prefix="mori-r59-c2st-",
                                 dir=os.environ.get("TMPDIR") or None))
    try:
        art = base / COPY_DIR.rstrip("/")
        art.mkdir(parents=True)
        f1 = art / "w1-results-r54.json"
        f1.write_text('{\n "seats": 2,\n}\n')
        f2 = art / "w1-results-r55.json"
        f2.write_text('{\n "seats": 3,\n}\n')
        f3 = art / "w1-results-r56.json"
        f3.write_text('{\n "seats": 4,\n}\n')
        ent = base / ENTRY
        ent.parent.mkdir(parents=True)
        claims = []
        for i in range(MIN_CLAIMS):
            f = [f1, f2, f3][i % 3]
            sha = sha256(f.read_bytes())
            rel = str(f.relative_to(base))
            claims.append('- **K%d** — c%d. Quote: ` "seats": %d,` (%s:line:2; pin %s)'
                          % (i + 1, i, i % 3 + 2, rel, sha))
        ent.write_text("source: S901\nverified-at: 2026-10-28\nrecheck: x\ncoverage-map: y\n\n"
                       + "\n".join(claims) + "\n")
        src = base / SOURCES
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text("| S901 | t | own-work | A | s | a | t | mined | 2026-10-28 | 90d | %s |\n" % ENTRY)
        ok, reasons, stats = eval_entry(base)
        chk("synth_good", ok and stats["claims"] == MIN_CLAIMS)
        ent2 = base / ENTRY
        ent2.write_text("\n".join(ent2.read_text().splitlines()[4:]) + "\n")
        ok2, reasons2, _ = eval_entry(base)
        chk("synth_no_frontmatter", not ok2
            and any(r.startswith("frontmatter") for r in reasons2))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print("C2_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    rev = argv[0]
    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    scratch = None
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]
        elif argv[i] == "--scratch":
            scratch = argv[i + 1]
        i += 2
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="mori-r59-c2-",
                                   dir=os.environ.get("TMPDIR") or None)
    met, failed, detail = measure(repo, rev, scratch)
    def tok(k):
        return "ok" if detail.get(k) else "bad"
    line = ("C2=%s selftest=%s scan=%s drift=%s trees=%s entry=%s rows=%s "
            "pins=%s tree=%s claims=%d files=%d rev=%s"
            % ("met" if met else "unmet", tok("selftest"), tok("scan"),
               tok("drift"), tok("trees"), tok("entry"), tok("rows"),
               tok("pins"), tok("tree"), detail["claims"], detail["files"], rev))
    if not met:
        line += " failed=" + ",".join(failed)
    print(line)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
