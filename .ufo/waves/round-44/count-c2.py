#!/usr/bin/env python3
"""mori round-44 C2 — gate-standard conformance counter (frozen instrument).

For every counter named with --counter, at the measured revision:
  * the path resolves;
  * `tools/mori-gate-registry.py --rev <rev> --audit <path>` prints REGISTRY=met
    (an eight-cell row whose entry names it, a resolvable entry and a
    `--selftest` mode);
  * its own `--selftest`, run from the bytes at that revision in an isolated
    temp dir, prints `pass=N fail=0` with N >= --min-arms;
  * a committed mutant at `fixtures/mutants/<same basename>` is caught by that
    counter's own selftest (`fail>=1`, exit 1).
Also requires `tools/mori-gate-registry.py --selftest` to print `fail=0`.

Usage:
  python3 count-c2.py <rev|WORK> [--repo PATH] --counter PATH [--counter PATH ...]
                      [--mutants-dir fixtures/mutants] [--min-arms N] [--timeout S]
  python3 count-c2.py --selftest

Exit: 0 C2=met · 1 C2=unmet · 2 C2_SETUP.

Predicate: .ufo/waves/round-44/contract.md P-C2.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TALLY = re.compile(r"pass=(\d+)\s+fail=(\d+)")

GOOD_ROW = ("| fixture counter | gate | `python3 tools/fx-one.py <rev>` | 0 met · 1 unmet · "
            "2 setup | `python3 tools/fx-one.py --selftest` | in-script cases | stdout only | "
            "mori |")
HEADER = "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |"


class Setup(Exception):
    pass


def repo_default():
    here = os.path.abspath(__file__)          # <repo>/.ufo/waves/round-44/count-c2.py
    d = os.path.dirname(here)
    while True:
        if os.path.isdir(os.path.join(d, ".git")) or os.path.isfile(
                os.path.join(d, "tools", "mori-gate-registry.py")):
            return d
        up = os.path.dirname(d)
        if up == d:
            return os.path.dirname(here)
        d = up


def git(repo, args, timeout=30):
    try:
        return subprocess.run(["git", "-C", repo] + args, capture_output=True,
                              text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise Setup("git timeout: %s" % " ".join(args))


def read_at(repo, rev, path):
    if rev == "WORK":
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            return fh.read()
    if git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)]).returncode != 0:
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)])
    if got.returncode != 0:
        raise Setup("git show failed for %s:%s" % (rev, path))
    return got.stdout.encode()


def materialize(repo, rev, path, tmp):
    body = read_at(repo, rev, path)
    if body is None:
        return None
    dest = os.path.join(tmp, os.path.basename(path))
    with open(dest, "wb") as fh:
        fh.write(body)
    os.chmod(dest, 0o755)
    return dest


def run_script(path, args, timeout, cwd=None, env=None):
    try:
        return subprocess.run([sys.executable, path] + args, capture_output=True,
                              text=True, timeout=timeout, check=False,
                              cwd=cwd or os.path.dirname(path), env=env)
    except subprocess.TimeoutExpired:
        return None


def tally_of(proc):
    if proc is None:
        return None
    m = None
    for m2 in TALLY.finditer(proc.stdout or ""):
        m = m2
    return (int(m.group(1)), int(m.group(2))) if m else None


def selftest_env(auditor_path):
    """Fixture plumbing: a counter copy run from a temp dir resolves the auditor."""
    env = dict(os.environ)
    if auditor_path:
        env["MORI_GATE_REGISTRY"] = auditor_path
    return env


def evaluate(repo, rev, counters, mutants_dir, min_arms, timeout):
    checks, fails = [], []

    def record(name, ok, detail=""):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    present = {c: read_at(repo, rev, c) is not None for c in counters}
    record("counters_present", all(present.values()),
           "absent=%s" % [c for c, ok in present.items() if not ok] if not all(present.values())
           else "%d counters" % len(counters))

    tmp = tempfile.mkdtemp(prefix="c2-")
    try:
        auditor = materialize(repo, rev, "tools/mori-gate-registry.py", tmp)
        if auditor is None:
            record("registry_rows", False, "tools/mori-gate-registry.py absent")
            record("tool_selftest", False, "tools/mori-gate-registry.py absent")
        else:
            args = ["--rev", rev, "--repo", repo]
            for c in counters:
                args += ["--audit", c]
            env = selftest_env(auditor)
            proc = run_script(auditor, args, timeout)
            out = (proc.stdout if proc else "") or ""
            ok = proc is not None and proc.returncode == 0 and "REGISTRY=met" in out
            detail = "REGISTRY=met" if ok else "; ".join(
                ln.strip() for ln in out.splitlines() if " FAIL " in ln)[:160] or "auditor failed"
            record("registry_rows", ok, detail)
            sproc = run_script(auditor, ["--selftest"], timeout, env=env)
            st = tally_of(sproc)
            record("tool_selftest", sproc is not None and sproc.returncode == 0
                   and st is not None and st[1] == 0 and st[0] >= 4,
                   "pass=%d fail=%d" % st if st else "no tally")

        tallies, mut_details = [], []
        for c in counters:
            path = materialize(repo, rev, c, tmp)
            if path is None:
                tallies.append("%s absent" % c)
                mut_details.append("%s absent" % c)
                continue
            proc = run_script(path, ["--selftest"], timeout, env=env)
            t = tally_of(proc)
            if proc is not None and proc.returncode == 0 and t and t[1] == 0 and t[0] >= min_arms:
                tallies.append("%s pass=%d" % (os.path.basename(c), t[0]))
            else:
                tallies.append("%s %s" % (os.path.basename(c),
                                          "pass=%d fail=%d" % t if t else "no tally"))

            mpath = "%s/%s" % (mutants_dir.rstrip("/"), os.path.basename(c))
            mraw = read_at(repo, rev, mpath)
            if mraw is None:
                mut_details.append("%s mutant absent" % os.path.basename(c))
                continue
            mfile = os.path.join(tmp, "mutant-" + os.path.basename(c))
            with open(mfile, "wb") as fh:
                fh.write(mraw)
            os.chmod(mfile, 0o755)
            mproc = run_script(mfile, ["--selftest"], timeout, env=env)
            mt = tally_of(mproc)
            if mproc is not None and mproc.returncode == 1 and mt and mt[1] >= 1:
                mut_details.append("%s killed (fail=%d)" % (os.path.basename(c), mt[1]))
            else:
                mut_details.append("%s SURVIVED (%s)" % (
                    os.path.basename(c),
                    "pass=%d fail=%d" % mt if mt else "no tally"))
        record("selftest_tally", all(" pass=" in t for t in tallies), "; ".join(tallies))
        record("mutant_kill", all("killed" in m for m in mut_details), "; ".join(mut_details))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return checks, fails


# --------------------------------------------------------------------------
# selftest — isolated throwaway repo with fixture counters and mutants
# --------------------------------------------------------------------------

COUNTER_OK = """#!/usr/bin/env python3
import sys
if "--selftest" in sys.argv:
    print("FIX_SELFTEST pass=2 fail=0")
    sys.exit(0)
print("FIX=met")
sys.exit(0)
"""

COUNTER_NO_SELFTEST = "#!/usr/bin/env python3\nprint('FIX=met')\n"

MUTANT_KILLED = """#!/usr/bin/env python3
import sys
if "--selftest" in sys.argv:
    print("FIX_SELFTEST pass=1 fail=1")
    sys.exit(1)
sys.exit(0)
"""

MUTANT_SURVIVED = """#!/usr/bin/env python3
import sys
if "--selftest" in sys.argv:
    print("FIX_SELFTEST pass=2 fail=0")
    sys.exit(0)
sys.exit(0)
"""


def _registry(rows):
    return ("# SKILL\n\n## Gates\n\n" + HEADER + "\n"
            + "|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")


def _mk(tmp, rows, files):
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, ["init", "-q", "-b", "main"])
    git(repo, ["config", "user.email", "mori@shokunin.local"])
    git(repo, ["config", "user.name", "mori-shokunin"])
    with open(os.path.join(repo, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(_registry(rows))
    for path, body in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.chmod(full, 0o755)
    git(repo, ["add", "-A"])
    git(repo, ["commit", "-q", "-m", "fixture"])
    rev = git(repo, ["rev-parse", "main"]).stdout.strip()
    return repo, rev


def auditor_bytes():
    """The auditor's own bytes, for the selftest fixture repo."""
    override = os.environ.get("MORI_GATE_REGISTRY")
    for cand in ([override] if override else []) + [
            os.path.join(repo_default(), "tools", "mori-gate-registry.py")]:
        if cand and os.path.isfile(cand):
            with open(cand, encoding="utf-8") as fh:
                return fh.read()
    raise Setup("cannot locate tools/mori-gate-registry.py for the selftest fixture")


def _base_files(**over):
    files = {
        "tools/mori-gate-registry.py": auditor_bytes(),
        "tools/fx-one.py": COUNTER_OK,
        "fixtures/mutants/fx-one.py": MUTANT_KILLED,
    }
    files.update(over)
    return files


def selftest():
    arms, failures = [], []

    def arm(name, fn):
        try:
            fn()
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                      # noqa: BLE001
            failures.append("%s: raised %s" % (name, exc))

    def honest():
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW], _base_files())
            _c, fails = evaluate(repo, rev, ["tools/fx-one.py"],
                                 "fixtures/mutants", 2, 60)
            assert not fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def absent_counter():
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW], _base_files())
            _c, fails = evaluate(repo, rev, ["tools/fx-two.py"],
                                 "fixtures/mutants", 2, 60)
            assert "counters_present" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def unregistered():
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, ["| other | gate | `python3 tools/other.py` | 0 | "
                                  "`--selftest` | x | y | mori |"], _base_files())
            _c, fails = evaluate(repo, rev, ["tools/fx-one.py"],
                                 "fixtures/mutants", 2, 60)
            assert "registry_rows" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def no_selftest_mode():
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW],
                            _base_files(**{"tools/fx-one.py": COUNTER_NO_SELFTEST}))
            _c, fails = evaluate(repo, rev, ["tools/fx-one.py"],
                                 "fixtures/mutants", 2, 60)
            assert "registry_rows" in fails, fails
            assert "selftest_tally" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def mutant_survives():
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, [GOOD_ROW],
                            _base_files(**{"fixtures/mutants/fx-one.py": MUTANT_SURVIVED}))
            _c, fails = evaluate(repo, rev, ["tools/fx-one.py"],
                                 "fixtures/mutants", 2, 60)
            assert "mutant_kill" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    arm("registered_conformant_met", honest)
    arm("absent_counter_unmet", absent_counter)
    arm("unregistered_counter_unmet", unregistered)
    arm("no_selftest_mode_unmet", no_selftest_mode)
    arm("surviving_mutant_unmet", mutant_survives)

    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("C2_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--counter", action="append", default=[])
    ap.add_argument("--mutants-dir", default="fixtures/mutants")
    ap.add_argument("--min-arms", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.rev or not args.counter:
        print("usage: count-c2.py <rev|WORK> --counter PATH [--counter PATH ...] [--selftest]")
        return 2
    repo = os.path.abspath(args.repo)
    rev = args.rev
    if rev != "WORK":
        resolved = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
        if resolved.returncode != 0:
            print("C2_SETUP cannot resolve revision %r" % rev)
            return 2
        rev = resolved.stdout.strip()
    try:
        checks, fails = evaluate(repo, rev, args.counter, args.mutants_dir,
                                 args.min_arms, args.timeout)
    except Setup as exc:
        print("C2_SETUP %s" % exc)
        return 2
    for name, ok, detail in checks:
        print("check %-18s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    print("rev=%s" % rev)
    print("C2=%s" % ("unmet" if fails else "met"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
