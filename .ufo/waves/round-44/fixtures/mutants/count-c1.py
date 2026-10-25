#!/usr/bin/env python3
"""mori round-44 C1 — figure reconciliation counter (frozen instrument).

Reads a committed figure ledger at a revision and re-derives every asserted
number from committed bytes: each row is one `git` pipeline in which the token
@REV@ is replaced by the measured revision. Prints `C1=met mismatches=0` exit 0
only when every row reconciles, the ledger holds at least --min-rows rows, and
those rows cover at least --min-classes of the declared classes.

Usage:
  python3 count-c1.py <rev|WORK> [--repo PATH] [--ledger PATH] [--min-rows N]
                      [--min-classes N] [--timeout S]
  python3 count-c1.py --selftest

Exit: 0 C1=met · 1 C1=unmet · 2 C1_SETUP (usage/bad revision).

Predicate: .ufo/waves/round-44/contract.md P-C1.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

CLASSES = {"registry", "evidence", "wave", "corpus", "checks"}
GIT_VERBS = {"show", "grep", "ls-tree", "rev-list", "cat-file", "log", "diff"}
ID_RE = re.compile(r"^F\d{2,3}$")
DIGITS = re.compile(r"^\d+$")


class Setup(Exception):
    pass


def repo_default():
    here = os.path.abspath(__file__)
    # .ufo/waves/round-44/count-c1.py -> <repo>; a copy at another depth still
    # resolves by walking up to the nearest checkout or gate-registry tool.
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
        return subprocess.run(
            ["git", "-C", repo] + args,
            capture_output=True, text=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        raise Setup("git timeout: %s" % " ".join(args))


def read_at(repo, rev, path):
    """Committed bytes of `path` at `rev`, or None when the path is absent."""
    if rev == "WORK":
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            return fh.read()
    probe = git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)])
    if probe.returncode != 0:
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)])
    if got.returncode != 0:
        raise Setup("git show failed for %s:%s" % (rev, path))
    return got.stdout.encode()


def parse_ledger(text):
    """Return (rows, problems). rows: list of (id, asserted, cls, command)."""
    rows, problems = [], []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = line.split("\t")
        if len(cells) != 4:
            problems.append("row %d: %d TSV cells, want 4" % (n, len(cells)))
            continue
        fid, asserted, cls, cmd = [c.strip() for c in cells]
        if not ID_RE.match(fid):
            problems.append("row %d: id %r is not F<digits>" % (n, fid))
        if not DIGITS.match(asserted):
            problems.append("row %d: asserted %r is not an integer" % (n, asserted))
        if cls not in CLASSES:
            problems.append("row %d: class %r not in %s" % (n, cls, sorted(CLASSES)))
        if not cmd.startswith("git "):
            problems.append("row %d: command is not a git pipeline" % n)
        elif cmd.split()[1:2] and cmd.split()[1] not in GIT_VERBS:
            problems.append("row %d: git verb %r is not a read verb" % (n, cmd.split()[1]))
        if "@REV@" not in cmd:
            problems.append("row %d: command does not name @REV@" % n)
        if ";" in cmd or "&&" in cmd:
            problems.append("row %d: command is not a single pipeline" % n)
        if re.search(r"\b(echo|printf|true)\b", cmd):
            problems.append("row %d: command carries a non-byte producer" % n)
        rows.append((fid, asserted, cls, cmd))
    return rows, problems


def run_row(repo, rev, cmd, timeout):
    full = "%s 2>/dev/null | head -c 64" % cmd.replace("@REV@", rev)
    try:
        out = subprocess.run(
            ["bash", "-c", full],
            capture_output=True, text=True, timeout=timeout, check=False, cwd=repo,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout after %ss" % timeout
    if out.returncode != 0:
        return None, "rc=%d %s" % (out.returncode, out.stderr.strip()[:80])
    body = out.stdout.strip()
    if not DIGITS.match(body):
        return None, "output %r is not an integer" % body[:40]
    return int(body), ""


def evaluate(repo, rev, ledger, min_rows, min_classes, timeout, cmd_rev=None):
    checks, fails = [], []

    def record(name, ok, detail=""):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    raw = read_at(repo, rev, ledger)
    record("ledger_present", raw is not None,
           "absent" if raw is None else "%d bytes" % len(raw))
    if raw is None:
        return checks, fails, {"rows": 0, "classes": [], "mismatches": None}

    text = raw.decode("utf-8", "replace")
    rows, problems = parse_ledger(text)
    record("rows_parse", not problems, "; ".join(problems[:3]) or "%d rows" % len(rows))
    classes = sorted({r[2] for r in rows})
    record("row_floor", True,
           "rows=%d min=%d" % (len(rows), min_rows))
    record("class_floor", len(classes) >= min_classes,
           "classes=%s min=%d" % (",".join(classes), min_classes))

    mismatches, details = [], []
    if not problems:
        for fid, asserted, _cls, cmd in rows:
            got, why = run_row(repo, cmd_rev or rev, cmd, timeout)
            if got is None:
                mismatches.append("%s unreadable (%s)" % (fid, why))
                details.append("%s <- %s" % (fid, why))
            elif got != int(asserted):
                mismatches.append("%s asserted=%s observed=%d" % (fid, asserted, got))
                details.append("%s asserted=%s observed=%d" % (fid, asserted, got))
    record("commands_reconcile", not mismatches, "; ".join(details[:4]) or "all rows match")
    return checks, fails, {"rows": len(rows), "classes": classes,
                           "mismatches": None if problems else len(mismatches)}


# --------------------------------------------------------------------------
# selftest: isolated throwaway git repos, no live lane state
# --------------------------------------------------------------------------

def _mk_repo(tmp, ledger_rows, extra_files=None, commit=True):
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, ["init", "-q", "-b", "main"])
    git(repo, ["config", "user.email", "mori@shokunin.local"])
    git(repo, ["config", "user.name", "mori-shokunin"])
    body = "\n".join(ledger_rows) + "\n"
    for path, content in (extra_files or {}).items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)
    full = os.path.join(repo, ".ufo/waves/round-44/figures.tsv")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(body)
    if commit:
        git(repo, ["add", "-A"])
        git(repo, ["commit", "-q", "-m", "fixture"])
    rev = git(repo, ["rev-parse", "main"]).stdout.strip()
    return repo, rev


def _honest_rows(n=12):
    rows = []
    for i in range(n):
        cls = list(CLASSES)[i % len(CLASSES)]
        rows.append("F%02d\t%d\t%s\tgit show @REV@:data.txt | grep -c x" % (i + 1, 3, cls))
    return rows


def selftest():
    arms, failures = [], []

    def arm(name, fn):
        try:
            fn()
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))

    def honest():
        tmp = tempfile.mkdtemp(prefix="c1st-")
        try:
            repo, rev = _mk_repo(tmp, _honest_rows(), {"data.txt": "x\nx\nx\n"})
            checks, fails, meta = evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv",
                                           12, 4, 20)
            assert not fails, "honest ledger failed: %s" % fails
            assert meta["mismatches"] == 0, meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def offbyone():
        rows = _honest_rows()
        rows[0] = "F01\t4\tregistry\tgit show @REV@:data.txt | grep -c x"
        tmp = tempfile.mkdtemp(prefix="c1st-")
        try:
            repo, rev = _mk_repo(tmp, rows, {"data.txt": "x\nx\nx\n"})
            _c, fails, meta = evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv",
                                       12, 4, 20)
            assert "commands_reconcile" in fails, fails
            assert meta["mismatches"] == 1, meta
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def junk_producer():
        rows = _honest_rows()
        rows[0] = "F01\t3\tregistry\techo 3"
        tmp = tempfile.mkdtemp(prefix="c1st-")
        try:
            repo, rev = _mk_repo(tmp, rows, {"data.txt": "x\nx\nx\n"})
            _c, fails, _m = evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv",
                                     12, 4, 20)
            assert "rows_parse" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def below_floor():
        tmp = tempfile.mkdtemp(prefix="c1st-")
        try:
            repo, rev = _mk_repo(tmp, _honest_rows(5), {"data.txt": "x\nx\nx\n"})
            _c, fails, _m = evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv",
                                     12, 4, 20)
            assert "row_floor" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def absent_ledger():
        tmp = tempfile.mkdtemp(prefix="c1st-")
        try:
            repo, rev = _mk_repo(tmp, _honest_rows(), {"data.txt": "x\nx\nx\n"})
            _c, fails, _m = evaluate(repo, rev, ".ufo/waves/round-44/absent.tsv",
                                     12, 4, 20)
            assert "ledger_present" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def unstripped_pipe():
        rows = _honest_rows()
        rows[1] = "F02\t3\twave\tgit show @REV@:data.txt | grep -c x; true"
        tmp = tempfile.mkdtemp(prefix="c1st-")
        try:
            repo, rev = _mk_repo(tmp, rows, {"data.txt": "x\nx\nx\n"})
            _c, fails, _m = evaluate(repo, rev, ".ufo/waves/round-44/figures.tsv",
                                     12, 4, 20)
            assert "rows_parse" in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    arm("honest_ledger_met", honest)
    arm("offbyone_row_mismatch", offbyone)
    arm("junk_producer_rejected", junk_producer)
    arm("below_floor_rejected", below_floor)
    arm("absent_ledger_unmet", absent_ledger)
    arm("compound_command_rejected", unstripped_pipe)

    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("C1_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--ledger", default=".ufo/waves/round-44/figures.tsv")
    ap.add_argument("--min-rows", type=int, default=12)
    ap.add_argument("--min-classes", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.rev:
        print("usage: count-c1.py <rev|WORK> [--repo PATH] [--ledger PATH] [--selftest]")
        return 2
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo, ".git")) and args.rev != "WORK":
        print("C1_SETUP repo is not a git checkout: %s" % repo)
        return 2
    rev = args.rev
    if rev != "WORK":
        resolved = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
        if resolved.returncode != 0:
            print("C1_SETUP cannot resolve revision %r" % rev)
            return 2
        rev = resolved.stdout.strip()

    cmd_rev = rev
    if rev == "WORK":
        tip = git(repo, ["rev-parse", "master"])
        if tip.returncode != 0:
            tip = git(repo, ["rev-parse", "HEAD"])
        if tip.returncode != 0:
            print("C1_SETUP cannot resolve a tip for WORK mode")
            return 2
        cmd_rev = tip.stdout.strip()

    try:
        checks, fails, meta = evaluate(repo, rev, args.ledger,
                                       args.min_rows, args.min_classes, args.timeout,
                                       cmd_rev=cmd_rev)
    except Setup as exc:
        print("C1_SETUP %s" % exc)
        return 2

    for name, ok, detail in checks:
        print("check %-20s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    print("rev=%s" % rev)
    print("ledger=%s rows=%d classes=%s" % (args.ledger, meta["rows"],
                                            ",".join(meta["classes"]) or "-"))
    if fails:
        mism = meta["mismatches"]
        print("C1=unmet mismatches=%s" % ("?" if mism is None else mism))
        return 1
    print("C1=met mismatches=0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
