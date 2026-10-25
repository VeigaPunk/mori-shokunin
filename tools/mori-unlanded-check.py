#!/usr/bin/env python3
"""mori-unlanded-check — list round work that exists on disk but is not committed.

Round 48 (operability; mistake M1 of `corpus/lessons/round-48.md`). Round 47 filed its report
while three late seat reports and `w2-results.json` sat untracked
(`corpus/lessons/round-47-verifier-spotcheck.md` §1 and §5 item 1). Nothing in the round
looked at the working tree between the last seat and the report, so the report's seat count
was not what the repository held.

  mori-unlanded-check.py --repo DIR --round N     one check
  mori-unlanded-check.py --selftest                sandbox arms

Scope: a path in `git status --porcelain=v1 -z --untracked-files=all` (untracked, modified,
deleted, renamed or staged) that sits under `.ufo/waves/round-N/`, `corpus/`, `tools/`, or is a
top-level `*.md` file. `.scratch/` and anything git ignores are outside the scope on purpose.
`--repo` must be the repository's own top level: a subdirectory, or a directory that is not a
repository (git would otherwise discover a parent repository), is a setup error.

Output: `UNLANDED=clean round=N` (exit 0), or `UNLANDED=dirty round=N paths=K` followed by one
`unlanded XY path` line per path, at most 50 (exit 1); `UNLANDED_SETUP …` on stderr (exit 2).
Read-only: `git rev-parse` and `git status --no-optional-locks` only.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

LIST_CAP = 50


class Setup(Exception):
    pass


def git(repo, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    p = subprocess.run(["git", "-C", repo, "--no-optional-locks"] + list(args), env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if p.returncode != 0:
        raise Setup(p.stderr.decode("utf-8", "replace").strip() or "git exited %d" % p.returncode)
    return p.stdout


def in_scope(path, round_number):
    return (path.startswith(".ufo/waves/round-%d/" % round_number)
            or path.startswith("corpus/") or path.startswith("tools/")
            or ("/" not in path and path.endswith(".md")))


def check(repo, round_number):
    if not os.path.isdir(repo):
        raise Setup("not a directory: %s" % repo)
    top = git(repo, "rev-parse", "--show-toplevel").decode("utf-8", "replace").strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise Setup("--repo is not a repository top level (git top level is %s)" % top)
    raw = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    fields = raw.split(b"\0")
    found = []
    i = 0
    while i < len(fields):
        rec = fields[i]
        i += 1
        if not rec:
            continue
        xy, path = rec[:2].decode("ascii", "replace"), rec[3:].decode("utf-8", "replace")
        if xy[0] in "RC":
            i += 1  # the rename/copy source follows as its own NUL field
        if in_scope(path, round_number):
            found.append((xy, path))
    return sorted(found, key=lambda t: t[1])


def run(repo, round_number):
    found = check(repo, round_number)
    if not found:
        return 0, ["UNLANDED=clean round=%d" % round_number]
    lines = ["UNLANDED=dirty round=%d paths=%d" % (round_number, len(found))]
    lines += ["unlanded %s %s" % (xy.replace(" ", "."), path) for xy, path in found[:LIST_CAP]]
    return 1, lines


def selftest():
    results = []
    base = tempfile.mkdtemp(prefix="unlanded-selftest-")
    ident = ["-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid"]

    def sandbox(name):
        d = os.path.join(base, name)
        os.mkdir(d)
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE,
                             check=True).stdout.decode().strip()
        assert os.path.realpath(top) == os.path.realpath(d), "sandbox is not its own repository"
        return d

    def write(d, rel, text="x\n"):
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)

    def commit(d, msg="c"):
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d] + ident + ["commit", "-q", "-m", msg], check=True)

    def arm(name, ok, detail):
        results.append((name, ok, detail))

    try:
        d = sandbox("clean")
        write(d, ".ufo/waves/round-8/w1/A.md")
        write(d, "SKILL.md")
        commit(d)
        rc, out = run(d, 8)
        arm("clean_tree_exit0", rc == 0 and out == ["UNLANDED=clean round=8"], "rc=%d %s" % (rc, out[0]))

        write(d, ".ufo/waves/round-8/w2/Late.md")
        rc, out = run(d, 8)
        arm("untracked_late_result_exit1_names_it",
            rc == 1 and any(l.endswith(".ufo/waves/round-8/w2/Late.md") for l in out), "rc=%d %s" % (rc, out))
        os.unlink(os.path.join(d, ".ufo/waves/round-8/w2/Late.md"))

        write(d, ".ufo/waves/round-8/w1/A.md", "changed\n")
        rc, out = run(d, 8)
        arm("modified_tracked_report_exit1", rc == 1 and any(" .M " in " " + l + " " or "A.md" in l for l in out[1:]),
            "rc=%d %s" % (rc, out))
        commit(d, "land")

        write(d, "notes/elsewhere.txt")
        write(d, ".scratch/seat/out.txt")
        rc, out = run(d, 8)
        arm("outside_scope_and_scratch_not_listed", rc == 0, "rc=%d %s" % (rc, out))

        write(d, ".ufo/waves/round-7/w1/Old.md")
        rc, out = run(d, 8)
        arm("other_round_not_listed", rc == 0, "rc=%d %s" % (rc, out))
        rc7, out7 = run(d, 7)
        arm("other_round_listed_for_that_round", rc7 == 1 and out7[-1].endswith("round-7/w1/Old.md"), "rc=%d" % rc7)

        write(d, "corpus/lessons/round-8.md")
        write(d, "tools/new tool.py")
        rc, out = run(d, 8)
        arm("lessons_and_space_in_path_listed",
            rc == 1 and any(l.endswith("corpus/lessons/round-8.md") for l in out)
            and any(l.endswith("tools/new tool.py") for l in out), "rc=%d %s" % (rc, out))

        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        rc, out = run(d, 8)
        arm("staged_but_uncommitted_listed", rc == 1 and any("round-8.md" in l for l in out), "rc=%d" % rc)

        sub = os.path.join(d, "corpus")
        try:
            run(sub, 8)
            arm("subdirectory_is_setup_error", False, "no error")
        except Setup as exc:
            arm("subdirectory_is_setup_error", "top level" in str(exc), str(exc)[:80])
        try:
            run(os.path.join(base, "missing"), 8)
            arm("missing_directory_is_setup_error", False, "no error")
        except Setup:
            arm("missing_directory_is_setup_error", True, "setup")

        cli = subprocess.run([sys.executable, os.path.abspath(__file__), "--repo", d, "--round", "8"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arm("cli_dirty_rc1", cli.returncode == 1 and b"UNLANDED=dirty" in cli.stdout, "rc=%d" % cli.returncode)
        cli2 = subprocess.run([sys.executable, os.path.abspath(__file__), "--repo", sub, "--round", "8"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arm("cli_setup_rc2", cli2.returncode == 2 and b"UNLANDED_SETUP" in cli2.stderr, "rc=%d" % cli2.returncode)
        cli3 = subprocess.run([sys.executable, os.path.abspath(__file__), "--repo", d],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arm("cli_usage_rc2", cli3.returncode == 2, "rc=%d" % cli3.returncode)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    fail = 0
    for name, ok, detail in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
        fail += 0 if ok else 1
    print("UNLANDED_SELFTEST pass=%d fail=%d" % (len(results) - fail, fail))
    return 0 if fail == 0 else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    args = list(argv)
    opts = {"--repo": None, "--round": None}
    for k in opts:
        if k in args:
            i = args.index(k)
            if i + 1 >= len(args):
                break
            opts[k] = args[i + 1]
            del args[i:i + 2]
    if args or opts["--repo"] is None or opts["--round"] is None or not re.fullmatch(r"[0-9]+", opts["--round"]):
        print("UNLANDED_SETUP usage: mori-unlanded-check.py --repo DIR --round N | --selftest", file=sys.stderr)
        return 2
    try:
        rc, lines = run(opts["--repo"], int(opts["--round"]))
    except (Setup, subprocess.SubprocessError, OSError) as exc:
        print("UNLANDED_SETUP %s" % exc, file=sys.stderr)
        return 2
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
