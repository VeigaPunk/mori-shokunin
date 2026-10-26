#!/usr/bin/env python3
"""Build the round-51 C1 controls as commits in a throwaway fixture repo and score each with the frozen
counter. Usage: c1-controls.py BASE_REV SCRATCH_DIR OUT_DIR

The fixture repo K is a `git clone --no-local` of the lane in SCRATCH_DIR; every git call names `-C K`, and
K's toplevel is asserted before the first commit. Controls (each one commit on BASE_REV):
  do-nothing   — BASE_REV itself (no commit)
  scratch-only — pin-check's --rev export moved to TMPDIR; nothing else
  conform-only — conform.py's LANE derived from its own path and its scratch under TMPDIR; nothing else
  class-only   — pin-check's env/stale classes (witness bytes), export still under <repo>/.scratch
  always-env   — witness bytes, but every tally mismatch is tagged env
  witness      — both witness files (feasibility only; built by the L1, not the claim's landing)
Every control that ships the witness pin-check also carries its SKILL.md self-test pin (114 -> 119), so a
control fails on its substance, not on the stale pin. Each control commit gets a branch `ctl-<name>` so a
clone of K carries it.
Receipts: OUT_DIR/control-c1-<name>.txt (counter stdout + exit code).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
COUNTER = os.path.join(os.path.dirname(HERE), "count-c1.py")
PC = "tools/mori-pin-check.py"
CF = ".ufo/waves/round-40/conform.py"
SCR_OLD = 'scratch_parent = os.path.join(repo, ".scratch")'
SCR_NEW_ENTERING = "scratch_parent = tempfile.gettempdir()"
SCR_NEW_WIT = "scratch_parent = os.path.abspath(args.scratch) if args.scratch else tempfile.gettempdir()"
CLS_OLD = 'kind = "env" if observed is None else "stale"'
SK = "SKILL.md"
PIN_OLD = "`PIN_CHECK_SELFTEST pass=114 fail=0`"
PIN_NEW = "`PIN_CHECK_SELFTEST pass=119 fail=0`"


def git(k, *args, check=True):
    return subprocess.run(["git", "-C", k] + list(args), check=check, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=600).stdout.decode()


def sub(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def main(base, scratch, out):
    k = os.path.join(scratch, "K")
    subprocess.run(["git", "clone", "-q", "--no-local", LANE, k], check=True, timeout=600)
    if os.path.realpath(git(k, "rev-parse", "--show-toplevel").strip()) != os.path.realpath(k):
        raise SystemExit("fixture toplevel mismatch")
    base = git(k, "rev-parse", "--verify", base + "^{commit}").strip()
    ent_pc = git(k, "show", "%s:%s" % (base, PC))
    ent_cf = git(k, "show", "%s:%s" % (base, CF))
    wit_pc = open(os.path.join(HERE, "witness", "mori-pin-check.py")).read()
    wit_cf = open(os.path.join(HERE, "witness", "conform.py")).read()
    ent_sk = git(k, "show", "%s:%s" % (base, SK))
    wit_sk = sub(ent_sk, PIN_OLD, PIN_NEW)
    variants = {
        "scratch-only": {PC: sub(ent_pc, SCR_OLD, SCR_NEW_ENTERING)},
        "conform-only": {CF: wit_cf},
        "class-only": {PC: sub(wit_pc, SCR_NEW_WIT, SCR_OLD), SK: wit_sk},
        "always-env": {PC: sub(wit_pc, CLS_OLD, 'kind = "env"'), CF: wit_cf, SK: wit_sk},
        "witness": {PC: wit_pc, CF: wit_cf, SK: wit_sk},
    }
    revs = {"do-nothing": (LANE, base)}
    for name, files in variants.items():
        git(k, "checkout", "-q", "--detach", base)
        for rel, text in files.items():
            with open(os.path.join(k, rel), "w") as f:
                f.write(text)
        git(k, "add", "--", *files.keys())
        git(k, "-c", "user.name=mori-r51-control", "-c", "user.email=control@invalid",
            "commit", "-q", "-m", "control " + name)
        git(k, "branch", "-f", "ctl-" + name, "HEAD")
        revs[name] = (k, git(k, "rev-parse", "HEAD").strip())
    os.makedirs(out, exist_ok=True)
    procs = {}
    for name, (repo, rev) in revs.items():
        sc = os.path.join(scratch, "s-" + name)
        os.makedirs(sc, exist_ok=True)
        f = open(os.path.join(out, "control-c1-%s.txt" % name), "w")
        f.write("$ python3 .ufo/waves/round-51/count-c1.py %s --repo %s --scratch %s\n" % (rev, repo, sc))
        f.flush()
        procs[name] = (subprocess.Popen([sys.executable, COUNTER, rev, "--repo", repo, "--scratch", sc],
                                        stdout=f, stderr=subprocess.STDOUT), f)
    for name, (p, f) in procs.items():
        rc = p.wait()
        f.write("exit=%d\n" % rc)
        f.close()
        print(name, rc)


if __name__ == "__main__":
    main(*sys.argv[1:4])
