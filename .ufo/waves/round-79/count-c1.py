#!/usr/bin/env python3
"""mori round-79 C1 counter (operability, capability acquisition).

Frozen predicate P-C1 (contract `.ufo/waves/round-79/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R, `tools/mori-control-receipt.py` exists as a committed blob; run from that
  blob with `python -I`, `--selftest` prints `CONTROL_RECEIPT_SELFTEST pass=P fail=F` with
  P >= 10 and F = 0 at rc 0; a live run over the round-78 evidence dir exits 1 and its
  stdout names `controls-r78.txt` together with the key
  `correction_marker_in_LOG_at_entering` (the D78-1 witness); and a live run over the
  round-79 evidence dir exits 0 with `unbound=0`.

Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] [--timeout S]
       count-c1.py --selftest
Output: one `item ...` line per graded item, then
  `C1=met|unmet tool=<sha12> selftest=<P>/<F> witness=<yes|no> after_rc=<n> after_unbound=<n>`
Exit 0 met, 1 unmet, 2 setup. Read-only on the repo (`git show`, `git archive`); the blob
and the archived evidence dirs are materialized under --scratch (default
$HYAKU_SCRATCH/mori-r79/count-c1) and removed on exit.
"""
import argparse
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

TOOL = "tools/mori-control-receipt.py"
EV_A = ".ufo/waves/round-78/evidence"
EV_B = ".ufo/waves/round-79/evidence"
WITNESS_KEY = "correction_marker_in_LOG_at_entering"
WITNESS_FILE = "controls-r78.txt"
MIN_CASES = 10
SELFTEST = re.compile(r"^CONTROL_RECEIPT_SELFTEST pass=(\d+) fail=(\d+)$", re.M)
UNBOUND = re.compile(r"^CONTROL_RECEIPT_SUMMARY\b.*\bunbound=(\d+)", re.M)


def run(cmd, cwd=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def read_blob(repo, rev, path):
    p = run(["git", "-C", repo, "show", f"{rev}:{path}"])
    return p.stdout if p.returncode == 0 else None


def archive(repo, rev, path, dest):
    p = subprocess.run(["git", "-C", repo, "archive", rev, "--", path],
                       capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return False
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
        tf.extractall(dest)
    return True


TOOL_TEMPLATE = '''\
import sys
CASES = %(cases)s
HOSTILE = %(hostile)s
AFTER_RC = %(after_rc)s
if "--selftest" in sys.argv:
    print("CONTROL_RECEIPT_SELFTEST pass=%%d fail=0" %% CASES); sys.exit(0)
d = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else ""
if "round-78" in d and HOSTILE:
    print("CONTROL_RECEIPT controls-r78.txt sections=7 claims=10 bound=0 unbound=7")
    print("unbound controls-r78.txt#4. claims=1 keys=correction_marker_in_LOG_at_entering")
    print("CONTROL_RECEIPT_SUMMARY files=1 sections=7 claims=10 unbound=7")
    sys.exit(1)
if "round-78" in d:
    print("CONTROL_RECEIPT_SUMMARY files=1 sections=7 claims=10 unbound=0")
    sys.exit(0)
print("CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=2 unbound=0")
sys.exit(AFTER_RC)
'''


def _tool_source(cases=10, hostile=True, after_rc=0):
    return TOOL_TEMPLATE % {"cases": cases, "hostile": hostile, "after_rc": after_rc}


def _selftest_cases():
    """Fixture arms: (label, tool_source, expect_met)."""
    return [("good_tool_met", _tool_source(), True),
            ("selftest_below_floor_unmet", _tool_source(cases=9), False),
            ("no_witness_unmet", _tool_source(hostile=False), False),
            ("after_run_red_unmet", _tool_source(after_rc=1), False)]


def selfcheck(scratch, timeout):
    ok = 0
    for label, src, expect in _selftest_cases():
        d = tempfile.mkdtemp(dir=scratch)
        repo = os.path.join(d, "repo")
        os.makedirs(os.path.join(repo, "tools"))
        os.makedirs(os.path.join(repo, EV_A))
        os.makedirs(os.path.join(repo, EV_B))
        open(os.path.join(repo, "tools", "mori-control-receipt.py"), "w").write(src)
        open(os.path.join(repo, EV_A, "controls-r78.txt"), "w").write("## 4.\nx=0\n")
        open(os.path.join(repo, EV_B, "receipt.txt"), "w").write("## 1.\n$ true\nx=0\n")
        env = ["-c", "user.name=t", "-c", "user.email=t@t"]
        run(["git"] + env + ["-C", repo, "init", "-q"])
        run(["git"] + env + ["-C", repo, "add", "-A"])
        p = run(["git"] + env + ["-C", repo, "commit", "-qm", "fixture"])
        if p.returncode != 0:
            print(f"FAIL {label} fixture-commit rc={p.returncode}")
            continue
        rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
        res = check(repo, rev, os.path.join(d, "s"), timeout)
        got = res["met"]
        if got == expect:
            ok += 1
            print(f"PASS {label} met={got}")
        else:
            print(f"FAIL {label} want_met={expect} got={got} {res.get('why','')}")
    print(f"C1_COUNTER_SELFTEST pass={ok} fail={len(_selftest_cases())-ok}")
    return 0 if ok == len(_selftest_cases()) else 1


def check(repo, rev, scratch, timeout):
    items = []
    text = read_blob(repo, rev, TOOL)
    if text is None:
        return {"met": False, "why": "tool_absent", "items": [("tool_absent", "missing")]}
    sha = hashlib.sha256(text.encode()).hexdigest()[:12]
    os.makedirs(scratch, exist_ok=True)
    src = os.path.join(scratch, "mori-control-receipt.py")
    open(src, "w").write(text)
    st = run([sys.executable, "-I", src, "--selftest"], cwd=scratch, timeout=timeout)
    m = SELFTEST.search((st.stdout or "") + (st.stderr or ""))
    cases = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    st_ok = bool(m) and st.returncode == 0 and cases[0] >= MIN_CASES and cases[1] == 0
    items.append(("selftest", f"pass={cases[0]} fail={cases[1]} rc={st.returncode}"))

    def live(ev, tag):
        d = os.path.join(scratch, "ev-" + tag)
        os.makedirs(d, exist_ok=True)
        if not archive(repo, rev, ev, d):
            return None, "", "archive_failed"
        p = run([sys.executable, "-I", src, "--dir", os.path.join(d, ev)], cwd=scratch,
                timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or ""), ""

    rc_a, out_a, err_a = live(EV_A, "a")
    witness = rc_a == 1 and WITNESS_FILE in out_a and WITNESS_KEY in out_a
    items.append(("witness", f"rc={rc_a} named={witness} {err_a}".strip()))
    rc_b, out_b, err_b = live(EV_B, "b")
    um = UNBOUND.search(out_b or "")
    after = int(um.group(1)) if um else -1
    after_ok = rc_b == 0 and after == 0
    items.append(("after", f"rc={rc_b} unbound={after} {err_b}".strip()))
    met = st_ok and witness and after_ok
    why = ",".join(k for k, ok in (("selftest", st_ok), ("witness", witness),
                                   ("after", after_ok)) if not ok)
    return {"met": met, "why": why, "sha": sha, "cases": cases,
            "witness": witness, "after": after, "rc_b": rc_b, "items": items}


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = tempfile.gettempdir()
    scratch = tempfile.mkdtemp(prefix="count-c1-r79-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch, a.timeout)
        if not a.rev:
            print("C1_SETUP usage: count-c1.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        if top.returncode == 0:
            a.repo = top.stdout.strip()
        rev = run(["git", "-C", a.repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if rev.returncode != 0:
            print(f"C1_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = rev.stdout.strip()
        r = check(a.repo, rev, scratch, a.timeout)
        for k, v in r.get("items", []):
            print(f"item {k} {v}")
        cases = r.get("cases", (0, 0))
        print(f"C1={'met' if r['met'] else 'unmet'} tool={r.get('sha','none')} "
              f"selftest={cases[0]}/{cases[1]} witness={'yes' if r.get('witness') else 'no'} "
              f"after_rc={r.get('rc_b','-')} after_unbound={r.get('after','-')} rev={rev[:12]}"
              + (f" failed={r['why']}" if not r["met"] else ""))
        return 0 if r["met"] else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
