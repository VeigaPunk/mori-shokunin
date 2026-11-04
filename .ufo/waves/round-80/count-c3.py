#!/usr/bin/env python3
"""mori round-80 C3 counter (coverage): does PROVINCE name every committed instrument?

Frozen predicate P-C3 (contract `.ufo/waves/round-80/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R the set of `tools/*.py` and `tools/*.sh` basenames named in PROVINCE.md
  contains every path `git ls-tree -r --name-only R -- tools/` reports with that shape, and
  every named path exists at R; the counter prints `C3=met named=N present=M missing=0` and
  exits 0. At the entering revision `d5888922` it prints
  `C3=unmet named=14 present=55 missing=41 extra=0` rc 1 (measured; the earlier draft of this
  line said 15/40 before the sibling-lane exclusion landed).

`named` counts distinct tool basenames mentioned anywhere in PROVINCE.md (prose or table);
`present` counts distinct `tools/<name>.py|.sh` paths in the tree at R (fixtures and
directories are not instruments); `missing` = present − named; `extra` = named − present
(a named path that does not exist at R — also a mismatch).

Usage: count-c3.py <rev> [--repo DIR] [--scratch DIR] | count-c3.py --selftest
Output: `C3=met|unmet named=N present=M missing=K extra=E rev=<sha12>`
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git ls-tree`; files only under --scratch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOKEN = re.compile(
    r"(?<![\w./-])(?:([A-Za-z0-9_.-]+)/)?tools/"
    r"([A-Za-z0-9_.-]+\.(?:py|sh))(?![\w.-])")
TREE = re.compile(r"^tools/([A-Za-z0-9_.-]+\.(?:py|sh))$")


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def tree_sets(repo, rev):
    p = run(["git", "-C", repo, "ls-tree", "-r", "-t", rev, "--", "tools/"])
    if p.returncode != 0:
        return None
    present, directories = set(), set()
    for line in p.stdout.splitlines():
        metadata, path = line.split("\t", 1)
        m = TREE.match(path)
        if m:
            target = directories if metadata.split()[1] == "tree" else present
            target.add(m.group(1))
    return present, directories


def grade(text, present, directories, own):
    named = set()
    for m in TOKEN.finditer(text):
        if m.group(1) is not None and m.group(1) != own:
            continue          # only the lane's own prefix may qualify tools/
        if m.group(2) not in directories:
            named.add(m.group(2))
    missing = sorted(present - named)
    extra = sorted(named - present)
    met = not missing and not extra
    return {"met": met, "named": len(named), "present": len(present),
            "missing": missing, "extra": extra}


def selfcheck(scratch):
    cases = []
    tools = ["mori-census.sh", "mori-pressure.py", "mori-runway-win.py"]
    bodies = {
        "complete": "".join(f"- `tools/{t}` probe\n" for t in tools),
        "missing_one": "".join(f"- `tools/{t}` probe\n" for t in tools[:2]),
        "extra_stale": "".join(f"- `tools/{t}` probe\n" for t in tools) + "- `tools/gone.py`\n",
    }
    expects = {"complete": True, "missing_one": False, "extra_stale": False}
    for label, body in bodies.items():
        d = tempfile.mkdtemp(dir=scratch)
        os.makedirs(os.path.join(d, "tools"))
        for t in tools:
            open(os.path.join(d, "tools", t), "w").write("# x\n")
        open(os.path.join(d, "PROVINCE.md"), "w").write("# p\n\n" + body)
        env = ["-c", "user.name=t", "-c", "user.email=t@t"]
        run(["git"] + env + ["-C", d, "init", "-q"])
        assert run(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() == d
        run(["git"] + env + ["-C", d, "add", "-A"])
        run(["git"] + env + ["-C", d, "commit", "-qm", "f"])
        rev = run(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
        pres, directories = tree_sets(d, rev)
        text = run(["git", "-C", d, "show", f"{rev}:PROVINCE.md"]).stdout
        r = grade(text, pres, directories, os.path.basename(d))
        cases.append((label, r["met"] == expects[label],
                      f"named={r['named']} present={r['present']} "
                      f"missing={len(r['missing'])} extra={len(r['extra'])}"))
    # mutation-seat survivors (r80 M01): a sibling-lane path and a directory must not count
    d = tempfile.mkdtemp(dir=scratch)
    os.makedirs(os.path.join(d, "tools", "fake-dir.py"))
    open(os.path.join(d, "tools", "fake-dir.py", "child"), "w").write("# x\n")
    for tname in tools:
        open(os.path.join(d, "tools", tname), "w").write("# x\n")
    open(os.path.join(d, "PROVINCE.md"), "w").write(
        "# p\n\n" + "".join(f"- `tools/{t}` probe\n" for t in tools)
        + "- `tools/fake-dir.py` is a directory, not an instrument\n"
        + "- `../tsukuroi-shokunin/tools/tsukuroi-census.sh` reads the same file\n")
    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
    run(["git"] + env + ["-C", d, "init", "-q"])
    assert run(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() == d
    run(["git"] + env + ["-C", d, "add", "-A"])
    run(["git"] + env + ["-C", d, "commit", "-qm", "f"])
    rev = run(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
    pres, directories = tree_sets(d, rev)
    r = grade(run(["git", "-C", d, "show", f"{rev}:PROVINCE.md"]).stdout,
              pres, directories, os.path.basename(d))
    cases.append(("sibling_and_directory_ignored", r["met"],
                  f"named={r['named']} present={r['present']} extra={r['extra']}"))
    # r80 reviewer MEDIUM-6, LOW-11 and LOW-12: one arm per routed exposure.
    own = os.path.basename(os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..")))
    r = grade("`corpus/tools/mori-census.sh`", {"mori-census.sh"}, set(), own)
    cases.append(("subdir_path_not_naming",
                  not r["met"] and r["named"] == 0
                  and r["missing"] == ["mori-census.sh"] and not r["extra"],
                  f"named={r['named']} missing={r['missing']}"))
    r = grade(f"`{own}/tools/mori-census.sh` "
              "`kata-shokunin/tools/sibling.py`",
              {"mori-census.sh"}, set(), own)
    cases.append(("own_lane_prefix_allowed",
                  r["met"] and r["named"] == 1 and not r["extra"],
                  f"named={r['named']} extra={r['extra']}"))
    r = grade("`tools/mori-census.sh` `tools/pkg.py` `tools/gone.py`",
              {"mori-census.sh"}, {"pkg.py"}, own)
    cases.append(("named_directory_ignored",
                  not r["met"] and r["named"] == 2
                  and not r["missing"] and r["extra"] == ["gone.py"],
                  f"named={r['named']} extra={r['extra']}"))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print(f"{'PASS' if good else 'FAIL'} {label} {line}")
    print(f"C3_COUNTER_SELFTEST pass={ok} fail={len(cases) - ok}")
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c3-r80-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C3_SETUP usage: count-c3.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"C3_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        tree = tree_sets(repo, rev)
        if tree is None:
            print("C3_SETUP ls-tree failed", file=sys.stderr)
            return 2
        text = run(["git", "-C", repo, "show", f"{rev}:PROVINCE.md"]).stdout
        if not text:
            print("C3_SETUP PROVINCE.md unreadable at rev", file=sys.stderr)
            return 2
        pres, directories = tree
        r = grade(text, pres, directories, os.path.basename(os.path.realpath(repo)))
        print(f"C3={'met' if r['met'] else 'unmet'} named={r['named']} present={r['present']} "
              f"missing={len(r['missing'])} extra={len(r['extra'])} rev={rev[:12]}")
        if r["missing"]:
            print("missing_first=" + ",".join(r["missing"][:8]))
        if r["extra"]:
            print("extra_first=" + ",".join(r["extra"][:8]))
        return 0 if r["met"] else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
