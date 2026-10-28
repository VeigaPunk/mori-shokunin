#!/usr/bin/env python3
"""Round 60 C3 counter (operability) — the Sentinel57/58 execution-boundary
HIGHs are closed in the round-60 counters and the closure is demonstrated
by replaying the routed PoC constructions against both rounds' counters.

Frozen predicate P-C3 (same sentence in contract.md, this counter and the
receipt label):
  At revision R, this counter builds three PoC scenarios under --scratch
  (fixture git repos created with explicit `git -C`, `rev-parse
  --show-toplevel` verified, fixture identity per commit):

  G1 toolgate — a PoC repo supplies an UNPINNED
  tools/mori-entry-claims-check.py blob that writes an EXEC-MARKER under
  the scratch it is handed and prints the expected selftest line.  Running
  the pinned round-60 count-c2.py (sha PIN_C2, materialized from R) against
  that repo must print `tool_sha` in failed= and must NOT create any
  EXEC-MARKER under its scratch; running the round-59 count-c2.py
  (revision-pinned at R59_DATA, materialized from the lane repo) against
  the same PoC MUST create the marker (the old hole, reproduced as the
  do-nothing control).

  G2 containment — driving the pinned round-60 count-c2 module's
  materialize(): a `..` walk, an inside-root write, and a symlink-parent
  write must return refuse/accept/refuse with nothing written outside the
  scratch root.

  G3 expectgate — a PoC repo committing
  trees-c2h/h02-malformed-claim/expect.txt with bytes that disagree with
  the counter's frozen expect table must make the pinned round-60
  count-c2.py print `expect_tamper:h02-malformed-claim`.

  C3=met iff all three gates hold (the G1 old-counter arm must reproduce
  the marker — a control that cannot fail proves nothing).

Usage: count-c3.py <rev> [--repo DIR] [--scratch DIR]
       count-c3.py --selftest
Output: `C3=met|unmet toolgate=ok|bad containment=ok|bad expectgate=ok|bad
  cases=N rev=R` (+ ` failed=`).  Exit 0 met, 1 unmet, 2 setup.
Read-only on the lane repo; all writes inside --scratch/TMPDIR.  Honors
TMPDIR.  Carries no absolute host path (run from the lane root).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PIN_C1 = "795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae"
PIN_C2 = "8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976"
C1_REL = ".ufo/waves/round-60/count-c1.py"
C2_REL = ".ufo/waves/round-60/count-c2.py"
R59_DATA = "7b86704d7c0754a09958d131b64dbfa2a6d3eaed"
R59_C2 = ".ufo/waves/round-59/count-c2.py"
EVIL_REL = "tools/mori-entry-claims-check.py"
TAMPER_REL = "trees-c2h/h02-malformed-claim/expect.txt"
FROZEN_H02 = "grammar"

EVIL_BLOB = '''#!/usr/bin/env python3
import sys, pathlib
argv = sys.argv[1:]
sc = None
if "--scratch" in argv:
    sc = pathlib.Path(argv[argv.index("--scratch") + 1])
try:
    base = sc if sc is not None else pathlib.Path(".")
    (base / "EXEC-MARKER").parent.mkdir(parents=True, exist_ok=True)
    (base / "EXEC-MARKER").write_text("executed " + " ".join(argv[:3]))
except Exception:
    pass
print("ENTRYCLAIMS_SELFTEST pass=13 fail=0")
print("SETSCAN_SELFTEST pass=10 fail=0")
sys.exit(0)
'''


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, timeout=120)


def git_show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def make_fixture_repo(base, files, name):
    """Fixture git repo per the git-fixture rule: explicit -C, toplevel
    check, throwaway per-commit identity, everything inside base/name."""
    d = Path(base) / name
    d.mkdir(parents=True, exist_ok=True)
    if git(d, "rev-parse", "--show-toplevel").returncode == 0:
        shutil.rmtree(d)
        d.mkdir(parents=True)
    p = git(d, "init", "-q")
    if p.returncode != 0:
        return None, "init_failed"
    chk = git(d, "rev-parse", "--show-toplevel")
    if chk.returncode != 0 or Path(chk.stdout.decode().strip()).resolve() \
            != d.resolve():
        return None, "toplevel_mismatch"
    for rel, blob in files.items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(blob)
    git(d, "add", "-A")
    p = git(d, "-c", "user.name=fixture", "-c",
            "user.email=fixture@example.invalid", "commit", "-qm",
            "poc: %s" % name)
    if p.returncode != 0:
        return None, "commit_failed"
    rev = git(d, "rev-parse", "HEAD").stdout.decode().strip()
    return rev, ""


def run_counter(counter_bytes, args, scratch, name):
    tmp = Path(scratch) / name
    tmp.write_bytes(counter_bytes)
    return subprocess.run([sys.executable, str(tmp)] + args,
                          capture_output=True, timeout=900,
                          env={**os.environ, "TMPDIR": str(scratch)})


def markers_under(root):
    return [str(p) for p in Path(root).rglob("EXEC-MARKER")]


def measure(repo, rev, scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    failed = []
    cases = 0

    c2_b = git_show(repo, rev, C2_REL)
    c2_ok = c2_b is not None and sha256(c2_b) == PIN_C2
    if c2_b is None:
        failed.append("count_c2_absent")
    elif not c2_ok:
        failed.append("count_c2_sha")
    c1_b = git_show(repo, rev, C1_REL)
    if c1_b is None:
        failed.append("count_c1_absent")
    elif sha256(c1_b) != PIN_C1:
        failed.append("count_c1_sha")
    r59c2_b = git_show(repo, R59_DATA, R59_C2)
    if r59c2_b is None:
        failed.append("r59_counter_absent")

    poc_rev, why = make_fixture_repo(
        scratch, {EVIL_REL: EVIL_BLOB.encode(),
                  "tools/mori-settlement-scan.py": EVIL_BLOB.encode()},
        "poc-exec")
    if poc_rev is None:
        failed.append("poc:%s" % why)
        return False, sorted(set(failed)), {"cases": cases}

    # G1 new counter: no execution of the unpinned blob
    s_new = scratch / "g1-new"
    s_new.mkdir()
    toolgate = False
    if c2_ok:
        p = run_counter(c2_b, [poc_rev, "--repo",
                               str((scratch / "poc-exec").resolve()),
                               "--scratch", str(s_new)],
                        scratch, "c2-new.py")
        out = p.stdout.decode("utf-8", "replace")
        no_exec = len(markers_under(s_new)) == 0
        gated = "tool_sha" in out and "tool_absent" not in out
        toolgate = gated and no_exec
        cases += 1
        if not gated:
            failed.append("g1_new_no_tool_sha")
        if not no_exec:
            failed.append("g1_new_executed:%s" % ",".join(
                markers_under(s_new)))
    else:
        failed.append("g1_new_skipped")

    # G1 old counter control: the hole reproduces
    old_hole = False
    if r59c2_b is not None:
        s_old = scratch / "g1-old"
        s_old.mkdir()
        run_counter(r59c2_b, [poc_rev, "--repo",
                              str((scratch / "poc-exec").resolve()),
                              "--scratch", str(s_old)],
                    scratch, "c2-old.py")
        found = markers_under(s_old)
        old_hole = len(found) > 0
        cases += 1
        if not old_hole:
            failed.append("g1_old_control_did_not_reproduce")
    else:
        failed.append("g1_old_skipped")

    # G2 containment via the pinned module
    containment = False
    if c2_ok:
        import importlib.util
        tmp = scratch / "c2-mod.py"
        tmp.write_bytes(c2_b)
        spec = importlib.util.spec_from_file_location("c2mod", tmp)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        g2 = scratch / "g2"
        g2.mkdir()
        r1 = mod.materialize(g2, "../escape.txt", b"x")
        r2 = mod.materialize(g2, "inside/f.txt", b"x")
        (g2 / "ln").symlink_to("nowhere")
        r3 = mod.materialize(g2, "ln/f.txt", b"x")
        containment = (r1 is False and r2 is True and r3 is False
                       and not (g2.parent / "escape.txt").exists()
                       and not (g2 / "nowhere" / "f.txt").exists())
        cases += 3
        if r1 is not False:
            failed.append("g2_parent_escape")
        if r2 is not True:
            failed.append("g2_inside_rejected")
        if r3 is not False:
            failed.append("g2_symlink_escape")
        if (g2.parent / "escape.txt").exists():
            failed.append("g2_escape_written")
    else:
        failed.append("g2_skipped")

    # G3 expect tamper
    expectgate = False
    if c2_ok:
        tampered = ("%s\nTAMPERED-EXTRA\n" % FROZEN_H02).encode()
        poc2_rev, why2 = make_fixture_repo(scratch, {TAMPER_REL: tampered},
                                           "poc-expect")
        if poc2_rev is None:
            failed.append("poc2:%s" % why2)
        else:
            s_g3 = scratch / "g3"
            s_g3.mkdir()
            p = run_counter(c2_b, [poc2_rev, "--repo",
                                   str((scratch / "poc-expect").resolve()),
                                   "--scratch", str(s_g3)],
                            scratch, "c2-g3.py")
            out = p.stdout.decode("utf-8", "replace")
            expectgate = "expect_tamper:h02-malformed-claim" in out
            cases += 1
            if not expectgate:
                failed.append("g3_no_tamper_flag")
    else:
        failed.append("g3_skipped")

    met = (c2_ok and toolgate and old_hole and containment and expectgate)
    return met, sorted(set(failed)), {"cases": cases}


def selftest():
    passed = failed = 0

    def chk(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAIL " + name, file=sys.stderr)
    chk("pins", len(PIN_C1) == 64 and len(PIN_C2) == 64)
    chk("evil_blob_marker", "EXEC-MARKER" in EVIL_BLOB
        and "--scratch" in EVIL_BLOB)
    chk("frozen_tamper_rel", TAMPER_REL.endswith("h02-malformed-claim/"
                                                 "expect.txt"))
    print("C3_SELFTEST pass=%d fail=%d" % (passed, failed))
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
        scratch = tempfile.mkdtemp(prefix="mori-r60-c3-",
                                   dir=os.environ.get("TMPDIR") or None)
    met, failed, d = measure(repo, rev, scratch)
    line = ("C3=%s toolgate=%s containment=%s expectgate=%s cases=%d rev=%s"
            % ("met" if met else "unmet",
               "ok" if "toolgate" not in failed and "g1_new_skipped"
               not in failed else "bad",
               "ok" if "containment" not in failed and "g2_skipped"
               not in failed else "bad",
               "ok" if "expectgate" not in failed and "g3_skipped"
               not in failed else "bad",
               d["cases"], rev))
    if not met:
        line += " failed=" + ",".join(failed)
    print(line)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
