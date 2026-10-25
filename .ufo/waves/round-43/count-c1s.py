#!/usr/bin/env python3
"""Round-43 successor operability counter. Does not amend the frozen r42 counter.

P-C1S is the sentence in contract.md. This file implements that sentence and
no other verdict rule. Usage:

    python3 .ufo/waves/round-43/count-c1s.py <rev> [--repo LANE]

Prints one line per check, then C1S=met or C1S=unmet. Exit 0 on met, 1 on
unmet, 2 on usage. A rev that does not contain this file byte-identical to
the running file stops after that check.
"""
import ast
import hashlib
import os
import re
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SELF_REL = ".ufo/waves/round-43/count-c1s.py"
FROZEN_REL = ".ufo/waves/round-42/count-c1.py"
FROZEN_SHA = "105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6"
V5_REL = ".ufo/waves/round-42/conform.py"
C8_REL = ".ufo/waves/round-41/fixtures/c1/count-c8.py"
CONTRACT_REL = ".ufo/waves/round-39/contract.md"
V5_MUTANTS = [
    ("walrus-branch", "timeout_scope_walrus_positive"),
    ("tuple-extract", "timeout_scope_tupleunpack_positive"),
    ("sort-deletion", "timeout_scope_source_order"),
]
CRASH = "TypeError: run() got an unexpected keyword argument 'cwd'"

failures = []


def check(name, ok, detail=""):
    print("check %-22s %s%s" % (
        name, "PASS" if ok else "FAIL", (" (%s)" % detail) if detail else ""))
    if not ok:
        failures.append(name)


def sh256(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(rev, path):
    proc = subprocess.run(
        ["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
        capture_output=True, timeout=120)
    return proc.stdout if proc.returncode == 0 else None


def run(argv, timeout=900, cwd=None):
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    return proc.returncode, proc.stdout, proc.stderr


def finish(met):
    print("C1S=%s" % ("met" if met else "unmet"))
    return 0 if met else 1


def selftest(clone, checker_abs, rev):
    return run([
        sys.executable, checker_abs, rev, "--repo", clone,
        "--contract", os.path.join(clone, CONTRACT_REL),
        "--counter", os.path.join(clone, C8_REL), "--selftest",
    ])


def parse_selftest(out):
    m = re.search(r"CONFORM_SELFTEST pass=(\d+) fail=(\d+)", out)
    fails = re.findall(r"^FAIL (\S+)", out, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None), fails


def main():
    global LANE
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print("usage: count-c1s.py <rev> [--repo LANE]", file=sys.stderr)
        return 2
    rev = args[0]
    if "--repo" in args:
        LANE = args[args.index("--repo") + 1]

    running = open(os.path.abspath(__file__), "rb").read()
    at_rev = git_bytes(rev, SELF_REL)
    same = at_rev is not None and at_rev == running
    check("self_at_rev", same,
          "absent" if at_rev is None else ("match" if same else "bytes differ"))
    if not same:
        return finish(False)

    frozen = git_bytes(rev, FROZEN_REL)
    check("frozen_sha", frozen is not None and sh256(frozen) == FROZEN_SHA,
          FROZEN_SHA[:12])
    sig_ok = False
    if frozen is not None:
        try:
            tree = ast.parse(frozen.decode())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "run":
                    sig_ok = [a.arg for a in node.args.args] == ["argv", "timeout"]
                    break
        except SyntaxError:
            sig_ok = False
    check("frozen_sig", sig_ok, "run params argv, timeout")

    v5 = git_bytes(rev, V5_REL)
    check("v5_present", v5 is not None, V5_REL)
    if frozen is None or v5 is None or not sig_ok:
        return finish(False)

    sandbox = tempfile.mkdtemp(prefix="mori-r43-c1s-", dir="/tmp")
    clone = os.path.join(sandbox, "repo")
    rc, _o, err = run(["git", "clone", "-q", "--shared", LANE, clone], timeout=300)
    check("sandbox_clone", rc == 0, err.strip()[:80])
    if rc != 0:
        return finish(False)
    run(["git", "-C", clone, "checkout", "-q", "--detach", rev])

    rc, out, _e = run(
        [sys.executable, os.path.join(clone, "tools/mori-sources-appendonly.py"),
         "--selftest"],
        cwd=clone)
    m = re.search(r"MORI_SOURCES_APPENDONLY_SELFTEST pass=(\d+) fail=(\d+)", out)
    check("noharm_cwd",
          rc == 0 and m and (int(m.group(1)), int(m.group(2))) == (22, 0),
          "rc=%d %s" % (rc, m.group(0) if m else out.strip()[:80]))

    v5_abs = os.path.join(clone, V5_REL)
    rc, out, _e = selftest(clone, v5_abs, rev)
    (p, f), fails = parse_selftest(out)
    check("v5_selftest_17", (p, f) == (17, 0) and rc == 0 and not fails,
          "pass=%s fail=%s rc=%d" % (p, f, rc))
    v5_text = v5.decode()
    for name, arm in V5_MUTANTS:
        mut_rel = ".ufo/waves/round-42/fixtures/mutants/conform-mut-%s.py" % name
        committed = git_bytes(rev, mut_rel)
        check("mutant_present_%s" % name, committed is not None, mut_rel)
        if committed is None:
            continue
        with open(v5_abs, "wb") as fh:
            fh.write(committed)
        rc, out, _e = selftest(clone, v5_abs, rev)
        (p, f), fails = parse_selftest(out)
        check("mutant_kill_%s" % name,
              (p, f) == (16, 1) and rc == 1 and fails == [arm],
              "pass=%s fail=%s fails=%s" % (p, f, fails))
    with open(v5_abs, "wb") as fh:
        fh.write(v5)

    frozen_path = os.path.join(sandbox, "frozen-count-c1.py")
    with open(frozen_path, "wb") as fh:
        fh.write(frozen)
    rc, out, err = run(
        [sys.executable, frozen_path, rev, "--repo", LANE], timeout=1800)
    check("frozen_still_crashes",
          rc != 0 and CRASH in (err or "") and not re.search(r"^C1=", out or "", re.M),
          "rc=%d crash=%s C1_line=%s" % (
              rc, CRASH in (err or ""), bool(re.search(r"^C1=", out or "", re.M))))

    return finish(not failures)


if __name__ == "__main__":
    sys.exit(main())
