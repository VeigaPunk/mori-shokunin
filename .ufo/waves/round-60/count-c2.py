#!/usr/bin/env python3
"""Round 60 C2 counter (depth) — the hardened entry-claims verifier is landed
at its frozen SHA, resists the thirteen frozen hostile trees (the routed
round-59 met-flip constructions), accepts the real round-59 entry without a
false negative, and attributes the r53 drift to its member key-set reason
while a renamed r54 control scans OK.

Frozen predicate P-C2 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, tools/mori-entry-claims-check.py exists with sha256 equal
  to PIN_EC and --selftest prints `ENTRYCLAIMS_SELFTEST pass=13 fail=0`
  exit 0 (executed only when the pin matches — G1); the real entry arm:
  corpus/knowledge/wave-settlement-artifacts-r59.md plus corpus/SOURCES.md
  plus the six ARTIFACT copies are materialized from R and the tool returns
  ok with >= MIN_CLAIMS claims, >= MIN_FILES files, spans == claims (H2),
  no rows: and no pin: reasons (H4/pins); the scan arm: the pinned
  tools/mori-settlement-scan.py (PIN_SCAN, G1-gated) returns
  SETTLEMENT_SCAN_OK with members==seats over the five REAL_SCAN files; the
  drift arm (H5): the pinned scan over the r53 file exits 1 with verdict
  SETTLEMENT_SCAN_FAIL and at least one reason containing `:extra_keys=`,
  while the same tool over r54 bytes materialized at an r53-named scratch
  path returns verdict SETTLEMENT_SCAN_OK (kills the filename-heuristic
  mutant); the tree arm: every directory under trees-c2h/ materializes and
  evaluates with the verdict its FROZEN_EXPECTS entry demands, its
  committed expect.txt byte-equals the frozen table (else expect_tamper —
  G3), and its reasons cover the frozen prefixes; every copy byte-equals
  its named .ufo artifact at R (tree=ok).

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR]
       count-c2.py --selftest
Output: `C2=met|unmet selftest=.. scan=.. drift=.. trees=.. entry=..
  rows=.. pins=.. tree=.. claims=N files=F spans=S rev=R` (+ ` failed=`).
  Exit 0 met, 1 unmet, 2 setup.
Read-only on the lane: git show / ls-tree / cat-file only; materializes
only under --scratch/TMPDIR through the containment-asserted writer (G2).
Honors TMPDIR.  Carries no absolute host path (run from the lane root).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL_EC = "tools/mori-entry-claims-check.py"
PIN_EC = "cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69"
TOOL_SCAN = "tools/mori-settlement-scan.py"
PIN_SCAN = ("4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5a"
            "c9a9")
ENTRY = "corpus/knowledge/wave-settlement-artifacts-r59.md"
SOURCES = "corpus/SOURCES.md"
TREES = ".ufo/waves/round-60/trees-c2h"
EXPECT_SELFTEST = "ENTRYCLAIMS_SELFTEST pass=13 fail=0"
MIN_CLAIMS = 10
MIN_FILES = 3

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
DRIFT_SCAN = ".ufo/waves/round-53/w1-results.json"
DRIFT_REASON = ":extra_keys="  # member key-set class (H5 attribution)

FROZEN_EXPECTS = {
    "h00-good-control": [],
    "h01-semantically-empty": ["distinct:dup_span", "text:short"],
    "h02-malformed-claim": ["grammar"],
    "h03-line-offset-alias": ["distinct:dup_span"],
    "h04-blank-quote": ["span:blank"],
    "h05-short-quotes": ["span:short"],
    "h06-degenerate-text": ["text:short"],
    "h07-single-row": ["rows:binding"],
    "h08-row-not-mined": ["rows:status"],
    "h09-usedby-other": ["rows:usedby"],
    "h10-stale-pin": ["pin:"],
    "h11-wrong-line": ["span:"],
    "h12-no-frontmatter": ["frontmatter"],
}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, timeout=120)


def git_show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def contained(root, target):
    """G2: target (inside root) must not escape by symlink or relative walk."""
    root_r = Path(root).resolve()
    t = Path(target)
    cur = t
    while True:
        if cur.is_symlink():
            return False
        if cur == root or cur.parent == cur:
            break
        cur = cur.parent
    try:
        resolved = t.resolve(strict=False)
    except OSError:
        return False
    return resolved == root_r or resolved.is_relative_to(root_r)


def materialize(root, rel, blob):
    """Containment-asserted write of `blob` at root/rel. Returns None on
    refusal (caller records `containment:`)."""
    root = Path(root)
    t = root / rel
    if not contained(root, t):
        return False
    t.parent.mkdir(parents=True, exist_ok=True)
    t.write_bytes(blob)
    return True


def run_pinned(tool_path, args, expect_pin, blob, scratch, timeout=300):
    """G1: execute repo-supplied tool bytes ONLY when their sha equals the
    frozen pin.  Returns (proc, executed_bool)."""
    if blob is None or sha256(blob) != expect_pin:
        return None, False
    p = subprocess.run(["python3", str(tool_path)] + args,
                       capture_output=True, text=True, timeout=timeout,
                       env={**os.environ, "TMPDIR": str(scratch)})
    return p, True


def measure(repo, rev, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    failed = []
    detail = {"claims": 0, "files": 0, "spans": 0}

    ec_b = git_show(repo, rev, TOOL_EC)
    ec_ok = ec_b is not None and sha256(ec_b) == PIN_EC
    if ec_b is None:
        failed.append("tool_absent")
    elif not ec_ok:
        failed.append("tool_sha")
    ec_path = scratch / "ec-tool.py"
    if ec_b is not None and ec_ok:
        ec_path.write_bytes(ec_b)  # materialize only when pinned

    scan_b = git_show(repo, rev, TOOL_SCAN)
    scan_ok_sha = scan_b is not None and sha256(scan_b) == PIN_SCAN
    if scan_b is None:
        failed.append("scan_tool_absent")
    elif not scan_ok_sha:
        failed.append("scan_tool_sha")
    scan_path = scratch / "scan-tool.py"
    if scan_b is not None and scan_ok_sha:
        scan_path.write_bytes(scan_b)

    # selftest arm (G1-gated)
    st_ok = False
    if ec_ok:
        p, ran = run_pinned(ec_path, ["--selftest", "--scratch",
                                      str(scratch / "st")], PIN_EC, ec_b,
                            scratch)
        st_ok = ran and p.returncode == 0 and EXPECT_SELFTEST in p.stdout
    detail["selftest"] = st_ok
    if not st_ok:
        failed.append("selftest")

    # scan arm
    scan_ok = True
    rfiles = []
    for rel in REAL_SCAN:
        b = git_show(repo, rev, rel)
        if b is None:
            scan_ok = False
            failed.append("scan_absent:%s" % rel)
            continue
        f = scratch / "real" / Path(rel).parent.name / Path(rel).name
        if materialize(scratch / "real",
                       "%s/%s" % (Path(rel).parent.name, Path(rel).name),
                       b) is False:
            scan_ok = False
            failed.append("containment:scan")
            continue
        rfiles.append(f)
    if not (ec_ok is not None and scan_ok_sha) or not rfiles:
        scan_ok = False
    else:
        p, ran = run_pinned(scan_path, [str(f) for f in rfiles], PIN_SCAN,
                            scan_b, scratch)
        out = None
        if ran:
            try:
                out = json.loads(p.stdout)
            except ValueError:
                out = None
        if not (ran and p.returncode == 0 and out is not None
                and out.get("verdict") == "SETTLEMENT_SCAN_OK"
                and all(f.get("members") == f.get("seats")
                        for f in out.get("files", []))):
            scan_ok = False
    detail["scan"] = scan_ok
    if not scan_ok:
        failed.append("scan")

    # drift arm with reason attribution (H5) + renamed control (M1 killer)
    drift_ok = False
    if scan_ok_sha:
        db = git_show(repo, rev, DRIFT_SCAN)
        if db is not None:
            materialize(scratch / "drift", "round-53/w1-results.json", db)
            p, ran = run_pinned(scan_path,
                                [str(scratch / "drift" / "round-53"
                                     / "w1-results.json")],
                                PIN_SCAN, scan_b, scratch)
            out = None
            if ran:
                try:
                    out = json.loads(p.stdout)
                except ValueError:
                    out = None
            reasons = []
            if out is not None:
                reasons = [r for fr in out.get("failures", [])
                           for r in fr.get("reasons", [])]
            attributed = (ran and p.returncode != 0
                          and out is not None
                          and out.get("verdict") == "SETTLEMENT_SCAN_FAIL"
                          and any(DRIFT_REASON in r for r in reasons))
            # renamed control: r54 bytes at an r53-named path must scan OK
            r54 = git_show(repo, rev, REAL_SCAN[0])
            ctrl = False
            if r54 is not None:
                materialize(scratch / "alias", "round-53-alias/w1.json", r54)
                p2, ran2 = run_pinned(
                    scan_path, [str(scratch / "alias" / "round-53-alias"
                                    / "w1.json")],
                    PIN_SCAN, scan_b, scratch)
                out2 = None
                if ran2:
                    try:
                        out2 = json.loads(p2.stdout)
                    except ValueError:
                        out2 = None
                ctrl = (ran2 and p2.returncode == 0 and out2 is not None
                        and out2.get("verdict") == "SETTLEMENT_SCAN_OK")
            drift_ok = attributed and ctrl
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

    # entry arm on a materialized root (G2-materialized)
    root = scratch / "root"
    have_all = True
    for rel in [ENTRY, SOURCES] + sorted(ARTIFACTS):
        b = git_show(repo, rev, rel)
        if b is None:
            have_all = False
            continue
        if materialize(root, rel, b) is False:
            have_all = False
            failed.append("containment:entry")
    if git_show(repo, rev, ENTRY) is None:
        failed.append("entry_absent")
    entry_ok = rows_ok = pins_ok = False
    if have_all and ec_ok:
        aj = scratch / "artifacts.json"
        aj.write_text(json.dumps(ARTIFACTS))
        p, ran = run_pinned(ec_path,
                            ["--root", str(root), "--entry", ENTRY,
                             "--registry", SOURCES,
                             "--artifacts-json", str(aj),
                             "--min-claims", str(MIN_CLAIMS),
                             "--min-files", str(MIN_FILES)],
                            PIN_EC, ec_b, scratch)
        out = None
        if ran:
            try:
                out = json.loads(p.stdout)
            except ValueError:
                out = None
        if ran and out is not None:
            reasons = out.get("reasons", [])
            st = out.get("stats", {})
            detail["claims"] = st.get("claims", 0)
            detail["files"] = st.get("files", 0)
            detail["spans"] = st.get("spans", 0)
            entry_ok = (p.returncode == 0 and out.get("ok") is True
                        and st.get("claims", 0) >= MIN_CLAIMS
                        and st.get("files", 0) >= MIN_FILES
                        and st.get("spans", 0) == st.get("claims", 0))
            rows_ok = not any(r.startswith("rows") for r in reasons)
            pins_ok = not any(r.startswith("pin") for r in reasons)
    detail["entry"] = entry_ok
    detail["rows"] = rows_ok
    detail["pins"] = pins_ok
    for tok, okv in (("entry", entry_ok), ("rows", rows_ok),
                     ("pins", pins_ok)):
        if not okv:
            failed.append(tok)

    # hostile trees arm (G3: frozen expect table, tamper detection)
    trees_ok = True
    listing = git(repo, "ls-tree", "--name-only", "%s:%s" % (rev, TREES))
    tdirs = [n for n in listing.stdout.decode().splitlines()
             if n] if listing.returncode == 0 else []
    if sorted(tdirs) != sorted(FROZEN_EXPECTS):
        trees_ok = False
        failed.append("trees_set")
    for name in tdirs:
        base = "%s/%s" % (TREES, name)
        frozen = FROZEN_EXPECTS.get(name)
        if frozen is None:
            trees_ok = False
            failed.append("tree:%s:frozen" % name)
            continue
        exp_b = git_show(repo, rev, base + "/expect.txt")
        if exp_b is None:
            trees_ok = False
            failed.append("tree:%s:expect" % name)
            continue
        if exp_b.decode().strip() != ",".join(frozen):
            trees_ok = False
            failed.append("expect_tamper:%s" % name)
            continue
        tr = scratch / "trees" / name
        fl = git(repo, "ls-tree", "-r", "--name-only", rev, base + "/")
        for f in fl.stdout.decode().splitlines():
            rel = f[len(base) + 1:]
            if rel == "expect.txt":
                continue
            b = git_show(repo, rev, f)
            if b is not None:
                if materialize(tr, rel, b) is False:
                    trees_ok = False
                    failed.append("containment:tree:%s" % name)
        if not ec_ok:
            trees_ok = False
            failed.append("tree:%s:tool" % name)
            continue
        p, ran = run_pinned(ec_path,
                            ["--root", str(tr), "--entry", ENTRY,
                             "--registry", SOURCES,
                             "--artifacts-json",
                             str(scratch / "artifacts.json"),
                             "--min-claims", str(MIN_CLAIMS),
                             "--min-files", str(MIN_FILES)],
                            PIN_EC, ec_b, scratch)
        out = None
        if ran:
            try:
                out = json.loads(p.stdout)
            except ValueError:
                out = None
        reasons = [] if out is None else out.get("reasons", [])
        want_ok = not frozen
        if out is None or out.get("ok") != want_ok:
            trees_ok = False
            failed.append("tree:%s:verdict" % name)
            continue
        if frozen and not all(any(r.startswith(e) for r in reasons)
                              for e in frozen):
            trees_ok = False
            failed.append("tree:%s:reasons" % name)
    detail["trees"] = trees_ok
    if not trees_ok:
        failed.append("trees")

    met = (ec_ok and st_ok and scan_ok and drift_ok and tree_ok
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

    chk("frozen_trees", len(FROZEN_EXPECTS) == 13
        and "h00-good-control" in FROZEN_EXPECTS)
    chk("artifacts_map", all(v.startswith(".ufo/") for v in
                             ARTIFACTS.values()) and len(ARTIFACTS) == 6)
    chk("real_scan", len(REAL_SCAN) == 5)
    chk("pins_hex", len(PIN_EC) == 64 and len(PIN_SCAN) == 64)
    # G2: containment refusals
    base = Path(tempfile.mkdtemp(prefix="mori-r60-c2st-",
                                 dir=os.environ.get("TMPDIR") or None))
    try:
        (base / "in").mkdir()
        chk("contain_parent", materialize(base, "../escape.txt", b"x")
            is False)
        chk("contain_inside", materialize(base, "in/f.txt", b"x") is True)
        (base / "ln").symlink_to("nowhere-escape")
        chk("contain_symlink_dir",
            materialize(base, "ln/f2.txt", b"x") is False)
        chk("no_escape_written",
            not (base.parent / "escape.txt").exists()
            and not (base / "nowhere-escape" / "f2.txt").exists())
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
    repo = "."
    scratch = None
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]
        elif argv[i] == "--scratch":
            scratch = argv[i + 1]
        i += 2
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="mori-r60-c2-",
                                   dir=os.environ.get("TMPDIR") or None)
    met, failed, detail = measure(repo, rev, scratch)

    def tok(k):
        return "ok" if detail.get(k) else "bad"
    line = ("C2=%s selftest=%s scan=%s drift=%s trees=%s entry=%s rows=%s "
            "pins=%s tree=%s claims=%d files=%d spans=%d rev=%s"
            % ("met" if met else "unmet", tok("selftest"), tok("scan"),
               tok("drift"), tok("trees"), tok("entry"), tok("rows"),
               tok("pins"), tok("tree"), detail["claims"], detail["files"],
               detail["spans"], rev))
    if not met:
        line += " failed=" + ",".join(failed)
    print(line)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
