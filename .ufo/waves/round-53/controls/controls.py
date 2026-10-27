#!/usr/bin/env python3
"""Round 53 controls (L1 MoriR53) — each control is a commit in a throwaway clone of the lane at the entering
tip plus the round-53 freeze files copied from this checkout; it is scored with the frozen counter and the
receipt (literal command, exit code, verdict line) is written to ../evidence/control-<claim>-<name>.txt.
Usage: controls.py <scratch-dir> [name...]   (names: c1-do-nothing c1-all-held c1-v72-copies c1-no-votes
c1-witness c2-do-nothing c2-mode-blind c2-no-band c2-memoriser c2-witness). Clones and scratch live under
<scratch-dir>, outside the lane, and are removed at the end.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(W)))
E = "20edafa59b38dac1ca358893f0259b1f436372d3"
C1 = {"c1-all-held": "ledger,allheld,rows,votes", "c1-v72-copies": "ledger,rows,votes,v72copies",
      "c1-no-votes": "ledger,rows", "c1-witness": "ledger,rows,votes"}
C2 = {"c2-mode-blind": "mode_blind", "c2-no-band": "no_band", "c2-memoriser": "memoriser", "c2-witness": ""}
FREEZE_COPY = ["corpus/evidence/sources-r53", ".ufo/waves/round-53/count-c1.py", ".ufo/waves/round-53/count-c2.py"]
WRAPPER = r'''#!/usr/bin/env python3
"""CONTROL TOOL (round-53 C2 control %(name)s; not lane data): the counter's reference reading%(what)s."""
import importlib.util, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c2", os.path.join(here, "..", ".ufo", "waves", "round-53", "count-c2.py"))
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
a = sys.argv[1:]
if a == ["--selftest"]:
    print("MORI_COMMIT_RUNWAY_SELFTEST: PASS 12/12"); sys.exit(0)
o = dict(zip(a[::2], a[1::2]))
def rd(p):
    try:
        return open(p).read()
    except OSError:
        return None
vmd = o.get("--vm-dir", "/proc/sys/vm")
vm = {k: rd(os.path.join(vmd, k)) for k in c2.VM_KEYS}
code, out = c2.ref(rd(o.get("--meminfo", "/proc/meminfo")), vm, rd(o.get("--cpu-present", "/sys/devices/system/cpu/present")),
                   int(o.get("--page-kb", os.sysconf("SC_PAGE_SIZE") // 1024)))
MUT = %(mut)r
if MUT == "memoriser":
    MUT = "no_band" if os.path.basename(os.path.dirname(o.get("--meminfo", "/x/y"))).startswith("seeded") else ""
if MUT == "mode_blind" and out["mode"] in (0, 1):
    out["verdict"] = "COMMIT_LOW" if out["headroom_kb"] < 0 else "COMMIT_OK"; code = 1 if out["headroom_kb"] < 0 else 0
if MUT == "no_band" and out["mode"] == 2:
    out["verdict"] = "COMMIT_LOW" if out["usable_kb"] <= 0 else "COMMIT_OK"; code = 1 if out["usable_kb"] <= 0 else 0
print(json.dumps(out)); sys.exit(code)
'''
WHAT = {"mode_blind": ", with a mode-blind verdict (LOW whenever Committed_AS exceeds CommitLimit)",
        "no_band": ", with no approximation band (LOW only below zero usable room)",
        "memoriser": ", exact on the frozen fixtures and band-blind on the seeded ones", "": " (feasibility witness)"}


def sh(*a, **k):
    return subprocess.run(list(a), check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **k)


def clone(base, name):
    d = os.path.join(base, "clone-" + name)
    shutil.rmtree(d, ignore_errors=True)
    sh("git", "clone", "-q", "--shared", "--no-checkout", LANE, d)
    if sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.decode().strip() != d:
        raise SystemExit("clone toplevel mismatch")
    sh("git", "-C", d, "checkout", "-q", "--detach", E)
    return d


def commit(d, msg):
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "-c", "user.name=mori-control", "-c", "user.email=control@mori.invalid",
       "commit", "-q", "--no-verify", "-m", msg)
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.decode().strip()


def receipt(name, parts, rev, cmd, shown_cmd):
    q = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = os.path.join(W, "evidence", "control-%s.txt" % name)
    with open(out, "w", encoding="utf-8") as f:
        f.write("# control %s (parts: %s); clone of the lane at %s%s, control commit %s\n"
                % (name, parts or "-", E, "" if rev == E else " + round-53 freeze files", rev))
        f.write("$ %s\n" % shown_cmd)
        f.write(q.stdout.decode("utf-8", "replace"))
        f.write("exit=%d\n" % q.returncode)
    print(name, q.returncode, q.stdout.decode().split("\n")[0][:200])


def main(argv):
    base = os.path.abspath(argv[0])
    names = argv[1:] or ["c1-do-nothing"] + list(C1) + ["c2-do-nothing"] + list(C2)
    os.makedirs(base, exist_ok=True)
    tmp = os.path.join(base, "tmp")
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ, TMPDIR=tmp)
    for name in names:
        d = clone(base, name)
        rev = E
        if name not in ("c1-do-nothing", "c2-do-nothing"):
            for p in FREEZE_COPY:
                src, dst = os.path.join(LANE, p), os.path.join(d, p)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
            commit(d, "control base: round-53 freeze files")
            if name in C1:
                sh(sys.executable, os.path.join(HERE, "c1-data.py"), d, C1[name], env=env)
            else:
                mut = C2[name]
                with open(os.path.join(d, "tools", "mori-commit-runway.py"), "w") as f:
                    f.write(WRAPPER % {"name": name, "what": WHAT[mut], "mut": mut})
                with open(os.path.join(d, "SKILL.md"), "a") as f:
                    f.write("\n| commit runway (control) | gate | `python3 -I -B tools/mori-commit-runway.py "
                            "[--selftest]` | control |\n")
            rev = commit(d, "control " + name)
        if name.startswith("c1-"):
            cmd = [sys.executable, os.path.join(W, "count-c1.py"), rev, "--repo", d]
            shown = "python3 .ufo/waves/round-53/count-c1.py %s --repo %s" % (rev, d)
            parts = C1.get(name)
        else:
            sc = os.path.join(base, "c2-" + name)
            cmd = [sys.executable, os.path.join(W, "count-c2.py"), rev, "--repo", d, "--scratch", sc]
            shown = "python3 .ufo/waves/round-53/count-c2.py %s --repo %s --scratch %s" % (rev, d, sc)
            parts = C2.get(name)
        receipt(name, parts, rev, cmd, shown)
        shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(base, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
