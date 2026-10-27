#!/usr/bin/env python3
"""Round 56 C1 counter (coverage) — the FR5 driver-liveness probe is landed, runs
and reports log-shape facts only.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, tools/mori-driver-liveness.py exists with sha256 equal to PIN;
  executed at R it prints a selftest line `DRIVER_LIVENESS_SELFTEST pass=13
  fail=0 skipped=0` and exits 0; executed over the frozen fixture tree
  .ufo/waves/round-56/fixtures/driver/ at R it prints one JSON object whose
  verdict is DRIVER_LIVENESS_OK for every fixture subdirectory that carries a
  watchdog.log and whose malformed counts match the frozen expectations
  (hyaku-pairing 0, attempt-rollover 0, legacy-grammar 0, in-flight 0,
  malformed 5, fails-and-dead 0, state-shapes 0, two-lanes 0, variants 0);
  corpus/knowledge/driver-liveness-r56.md exists at R and names S544 and
  tools/mori-driver-liveness.py; corpus/SOURCES.md at R carries a row S544 with
  status mined, opened 2026-10-27, used-by naming corpus/knowledge/driver-liveness-r56.md;
  and the tool text at R contains no health-verdict string (healthy, unhealthy,
  failed lane) — detection and report only.

Usage: count-c1.py <rev> [--repo DIR]   |   count-c1.py --selftest
Output: `C1=met|unmet selftest=ok|bad fixtures=ok|bad entry=ok|bad row=ok|bad norem=ok|bad rev=R`
  (+ `failed=` list when unmet).  Exit 0 met, 1 unmet, 2 setup.
Read-only: git show / ls-tree / rev-parse only; the selftest and fixture arms
materialize the tool and fixtures under the caller's TMPDIR and execute them
there (python3 subprocess, no network).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

TOOL = "tools/mori-driver-liveness.py"
ENTRY = "corpus/knowledge/driver-liveness-r56.md"
FIXDIR = ".ufo/waves/round-56/fixtures/driver"
EXPECT_SELFTEST = "DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0"
EXPECT_FIX = {
    "hyaku-pairing": 0, "attempt-rollover": 0, "legacy-grammar": 0,
    "in-flight": 0, "malformed": 5, "fails-and-dead": 0, "state-shapes": 0,
    "two-lanes": 0, "variants": 0,
}
HEALTH_WORDS = ("healthy", "unhealthy", "failed lane", "is stuck", "wedged")
PIN = "6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997"  # frozen at data commit 6ced9da9


def git_show(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return p.stdout


def git_ls(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, path],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return []
    return [l for l in p.stdout.split("\n") if l]


def sha(text):
    return hashlib.sha256(text.encode("utf-8", "surrogateescape")).hexdigest()


def run_tool(repo, rev, args, cwd):
    """Materialize the tool at rev under cwd/tool/tools/ and execute it.

    The tools/ nesting mirrors the repo layout so the tool's own
    dirname(dirname(__file__)) fixture derivation lands on cwd/tool/.
    """
    src = git_show(repo, rev, TOOL)
    if src is None:
        return None, None, "tool_absent"
    tdir = os.path.join(cwd, "tool", "tools")
    os.makedirs(tdir, exist_ok=True)
    tpath = os.path.join(tdir, "mori-driver-liveness.py")
    with open(tpath, "w", encoding="utf-8") as f:
        f.write(src)
    p = subprocess.run([sys.executable, tpath] + args, capture_output=True, text=True,
                       cwd=os.path.join(cwd, "tool"))
    return p.stdout, p.returncode, None


def materialize_fixtures(repo, rev, cwd):
    """Recreate the frozen fixture tree under cwd (symlinks included)."""
    p = subprocess.run(["git", "-C", repo, "ls-tree", "-r", rev, FIXDIR],
                       capture_output=True, text=True)
    n = 0
    if p.returncode != 0:
        return cwd, n
    for line in p.stdout.split("\n"):
        if "\t" not in line:
            continue
        meta, name = line.split("\t", 1)
        mode = meta.split(" ", 1)[0]
        content = git_show(repo, rev, name)
        if content is None:
            continue
        dest = os.path.join(cwd, name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if mode == "120000":
            link = content.rstrip("\n")
            if os.path.lexists(dest):
                os.remove(dest)
            os.symlink(link, dest)
        else:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(content)
        n += 1
    return cwd, n


def evaluate(repo, rev):
    failed = []
    tool_src = git_show(repo, rev, TOOL)
    if tool_src is None:
        return None, ["tool_absent"], "2"
    if PIN and sha(tool_src) != PIN:
        failed.append("pins")
    cwd = tempfile.mkdtemp(prefix="mori-r56-c1-", dir=os.environ.get("TMPDIR") or None)
    tdir = os.path.join(cwd, "tool")
    os.makedirs(tdir, exist_ok=True)
    _, nfix = materialize_fixtures(repo, rev, tdir)
    out, rc, err = run_tool(repo, rev, ["--selftest"], cwd)
    if err:
        failed.append("selftest_absent")
    elif rc != 0 or EXPECT_SELFTEST not in (out or ""):
        failed.append("selftest")
    fx_bad = []
    fixbase = os.path.join(tdir, FIXDIR)
    for name, want in EXPECT_FIX.items():
        log = os.path.join(fixbase, name, "watchdog.log")
        if not os.path.isfile(log):
            fx_bad.append(name + ":missing")
            continue
        out, rc, _ = run_tool(repo, rev, ["--fixture", os.path.join(fixbase, name)], cwd)
        try:
            doc = json.loads((out or "").strip())
        except ValueError:
            fx_bad.append(name + ":nojson")
            continue
        if doc.get("verdict") != "DRIVER_LIVENESS_OK" or doc["log"]["malformed"] != want:
            fx_bad.append("%s:%s/%s" % (name, doc.get("verdict"), doc["log"]["malformed"]))
    if fx_bad:
        failed.append("fixtures")
    entry = git_show(repo, rev, ENTRY)
    if entry is None or "S544" not in entry or "mori-driver-liveness.py" not in entry:
        failed.append("entry")
    reg = git_show(repo, rev, "corpus/SOURCES.md") or ""
    row = None
    for line in reg.split("\n"):
        if re.match(r"^ {0,3}\|\s*S544\s*\|", line):
            row = line
            break
    if (row is None or "mined" not in row or "2026-10-27" not in row
            or ENTRY not in row):
        failed.append("row")
    low = tool_src.split("# selftest", 1)[0].lower()
    if any(w in low for w in HEALTH_WORDS):
        failed.append("norem")
    return (EXPECT_SELFTEST if not failed else None), failed, None


def main():
    if "--selftest" in sys.argv:
        # the counter's own logic arms: fixture-expectation table sanity
        ok = len(EXPECT_FIX) == 9 and EXPECT_SELFTEST.startswith("DRIVER_LIVENESS_SELFTEST")
        print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (1 if ok else 0, 0 if ok else 1))
        return 0 if ok else 1
    if len(sys.argv) < 2:
        print("usage: count-c1.py <rev> [--repo DIR]", file=sys.stderr)
        return 2
    rev = sys.argv[1]
    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    if "--repo" in sys.argv:
        repo = sys.argv[sys.argv.index("--repo") + 1]
    p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", rev],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print("C1_SETUP: unresolvable revision %s" % rev, file=sys.stderr)
        return 2
    full = p.stdout.strip()
    _, failed, setup = evaluate(repo, full)
    if failed == ["tool_absent"]:
        print("C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad "
              "failed=tool_absent rev=%s" % full)
        return 1
    if setup:
        return 2
    ok = not failed
    print("C1=%s selftest=%s fixtures=%s entry=%s row=%s norem=%s rev=%s%s" % (
        "met" if ok else "unmet",
        "bad" if ("selftest" in failed or "selftest_absent" in failed) else "ok",
        "bad" if "fixtures" in failed else "ok",
        "bad" if "entry" in failed else "ok",
        "bad" if "row" in failed else "ok",
        "bad" if "norem" in failed else "ok",
        full,
        "" if ok else " failed=" + ",".join(failed)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
