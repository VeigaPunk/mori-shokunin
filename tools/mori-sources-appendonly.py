#!/usr/bin/env python3
"""mori-sources-appendonly.py — CORPUS.md rule 2 gate for corpus/SOURCES.md.

Usage:
    mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]
    mori-sources-appendonly.py --selftest

Rule 2 of CORPUS.md: the registry rows of corpus/SOURCES.md are append-only.
Only the columns `status`, `recheck` and `used-by` may change in place; every
other column is immutable, and a rewritten row must land as a new row whose
`teaches` cell opens `supersedes S###`.

What the gate measures, at revision <rev>:

  ids            rows present at <rev> whose immutable cells differ from the
                 cells the same id held in the first ancestry commit that
                 carried that id (endpoint comparison, QUALITY 102).  Row
                 identity is the id, never the line position.
  deleted        ids carried by some ancestry commit of <rev> and absent at
                 <rev> (the round-35 gap: a deleted row is not a rewrite).
  superseded     ids in `ids` for which a row present at <rev> has a `teaches`
                 cell opening `supersedes S###`.
  round_changed  ids whose immutable cells changed, or which were deleted, in
                 any commit of REV..<rev> that touches the path.  An id edited
                 and then edited back inside the range is listed too: the
                 change is a fact of the round even when the endpoint matches.

  superseded_as_of  ids in `superseded` whose latest superseding row's landing commit
                 is a descendant of (strictly later than) the id's last immutable-cell
                 edit commit.  Presence alone does not discharge: a superseder that
                 landed before the edit leaves the id in `stale_supersede` (round 38,
                 ExecGateRound D3).
  stale_supersede  superseded ids whose latest superseder landed at or before the edit.

  appendonly_violations = len(ids) + len(deleted)

Columns are taken by header position (id source kind tier scope anchor teaches
status opened recheck used-by); cells are compared stripped, so whitespace
padding is not a change.  Rows are keyed by id.

Output (stdout):
    changed <id> superseded_by=<latest superseding row id, or ->
    deleted <id>
    appendonly_violations=N ids=[...] deleted=[...] superseded=[...] round_changed=[...]
    supersede_timing superseded_as_of=[...] stale_supersede=[...]

Exit codes:
    0   no violation (with --round-base: nothing changed in the round)
    1   violation(s); with --round-base: the round changed the registry
    2   error (git failure, unparsable registry)

Read-only: the only git commands used are `rev-parse`, `log` and `show`.
No writes, no network, no clone.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

DEFAULT_PATH = "corpus/SOURCES.md"
COLUMNS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
           "status", "opened", "recheck", "used-by"]
MUTABLE = ("status", "recheck", "used-by")
CELL_RE = re.compile(r"^:?-{3,}:?$")
ID_RE = re.compile(r"S\d{3}")
SUPERSEDES_RE = re.compile(r"^supersedes\s+(S\d{3})\b")
SUMMARY_RE = re.compile(
    r"^appendonly_violations=(\d+)\s+ids=\[([^\]]*)\]\s+deleted=\[([^\]]*)\]\s+"
    r"superseded=\[([^\]]*)\]\s+round_changed=\[([^\]]*)\]$")
TIMING_RE = re.compile(
    r"^supersede_timing superseded_as_of=\[([^\]]*)\] stale_supersede=\[([^\]]*)\]$")

PREDICATE = (
    "P-C6: at revision R, tools/mori-sources-appendonly.py reports, after its summary "
    "line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; an id is "
    "superseded-as-of only when its latest superseding row's landing commit is a "
    "descendant of the id's last immutable-cell edit commit, and is listed in "
    "stale_supersede otherwise; on the lane history S069 is stale before its round-38 "
    "supersede row lands and no id is stale after, and the selftest carries a "
    "supersede-before-edit fixture that lists the id in stale_supersede."
)


class GateError(Exception):
    """Any condition that must exit 2."""


def _clean_env():
    """The caller's environment without the git redirection variables.

    `git -C <repo>` must address the repository that was asked for, not one
    the caller's environment points at.
    """
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                "GIT_COMMON_DIR"):
        env.pop(key, None)
    return env


# --------------------------------------------------------------------- git io

def git(repo, *args):
    """Run a read-only git command; raise GateError on failure."""
    try:
        proc = subprocess.run(["git", "-C", repo] + list(args),
                              capture_output=True, text=True, timeout=120,
                              encoding="utf-8", errors="replace",
                              env=_clean_env())
    except subprocess.TimeoutExpired:
        raise GateError("git %s timed out" % " ".join(args))
    except OSError as exc:
        raise GateError("git %s failed to start: %s" % (" ".join(args), exc))
    if proc.returncode != 0:
        raise GateError("git %s failed: %s"
                        % (" ".join(args), proc.stderr.strip() or "exit %d" % proc.returncode))
    return proc.stdout


def git_blob(repo, spec):
    """Content of <spec> (rev:path), or None when the path is absent there."""
    try:
        proc = subprocess.run(["git", "-C", repo, "show", spec],
                              capture_output=True, text=True, timeout=120,
                              encoding="utf-8", errors="replace",
                              env=_clean_env())
    except subprocess.TimeoutExpired:
        raise GateError("git show %s timed out" % spec)
    except OSError as exc:
        raise GateError("git show %s failed to start: %s" % (spec, exc))
    if proc.returncode != 0:
        return None
    return proc.stdout


# --------------------------------------------------------------- registry io

def parse_registry(text):
    """Return (rows, colmap) for a SOURCES.md body.

    rows: one cell list per registry row, in header order.
    colmap: header column name (lower case) -> cell index, or None when the
            body carries no header.
    """
    lines = text.splitlines()
    header = None
    header_at = -1
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if cells and cells[0].lower() == "id" and len(cells) >= 5:
            header = cells
            header_at = index
            break
    if header is None:
        return [], None
    colmap = {}
    for index, name in enumerate(header):
        colmap.setdefault(name.strip().lower(), index)
    rows = []
    for line in lines[header_at + 1:]:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        if all(CELL_RE.match(c) for c in cells if c):
            continue
        if not ID_RE.fullmatch(cells[0]):
            continue
        rows.append(cells)
    return rows, colmap


def immutable_indices(colmap):
    """Cell indices of the immutable columns, by header position."""
    if not colmap:
        colmap = {name: index for index, name in enumerate(COLUMNS)}
    return [colmap[name] for name in COLUMNS
            if name not in MUTABLE and name in colmap]


def imm_key(cells, imm_idx):
    """Immutable fingerprint of a row; cells compare stripped."""
    return tuple(cells[i].strip() for i in imm_idx)


def superseders(rows, colmap):
    """superseded id -> id of the row that supersedes it (first one wins)."""
    teaches_idx = (colmap or {}).get("teaches", COLUMNS.index("teaches"))
    out = {}
    for cells in rows:
        if teaches_idx >= len(cells):
            continue
        match = SUPERSEDES_RE.match(cells[teaches_idx].strip())
        if match:
            out.setdefault(match.group(1), cells[0].strip())
    return out


# ------------------------------------------------------------------- analysis

def analyze(repo, rev, path, round_base=None):
    """Walk the path's history and return the four lists plus the verdict."""
    rev_full = git(repo, "rev-parse", "--verify", rev + "^{commit}").strip()
    tip_text = git_blob(repo, "%s:%s" % (rev_full, path))
    if tip_text is None:
        raise GateError("%s is absent at %s" % (path, rev_full))
    tip_rows, tip_colmap = parse_registry(tip_text)
    if tip_colmap is None:
        raise GateError("no registry header in %s at %s" % (path, rev_full))

    commits = git(repo, "log", "--format=%H", "--reverse", rev_full, "--",
                  path).split()

    states = []
    colmap = None
    for commit in commits:
        text = git_blob(repo, "%s:%s" % (commit, path))
        if text is None:
            states.append(None)          # path absent at that commit
            continue
        rows, commit_colmap = parse_registry(text)
        if commit_colmap is not None and colmap is None:
            colmap = commit_colmap
        states.append(rows)
    if colmap is None:
        colmap = tip_colmap
    imm_idx = immutable_indices(colmap)

    first = {}          # id -> cells in the first commit that carried it
    changed_at = {}     # commit index -> ids whose immutable cells changed
    deleted_at = {}     # commit index -> ids that disappeared there
    last_seen = {}      # id -> cells it last held
    supersede_rows = {}     # (superseded id, superseder id) -> first index it appears
    supersede_landing = {}  # superseded id -> (latest landing index, that superseder id)
    teaches_idx = (colmap or {}).get("teaches", COLUMNS.index("teaches"))
    prev_ids = set()
    for index, rows in enumerate(states):
        if rows is None:
            continue
        for cells in rows:
            if teaches_idx >= len(cells):
                continue
            m = SUPERSEDES_RE.match(cells[teaches_idx].strip())
            if m:
                supersede_rows.setdefault((m.group(1), cells[0].strip()), index)
        current = {cells[0]: cells for cells in rows}
        for cid, cells in current.items():
            if cid not in first:
                first[cid] = cells
            elif cid in last_seen and imm_key(cells, imm_idx) != imm_key(last_seen[cid], imm_idx):
                changed_at.setdefault(index, set()).add(cid)
            last_seen[cid] = cells
        gone = prev_ids - set(current)
        if gone:
            deleted_at.setdefault(index, set()).update(gone)
        prev_ids = set(current)

    tip = {cells[0]: cells for cells in tip_rows}
    ids = sorted(cid for cid, cells in tip.items()
                 if cid not in first
                 or imm_key(cells, imm_idx) != imm_key(first[cid], imm_idx))
    deleted = sorted(set(first) - set(tip))
    for (target, by), index in supersede_rows.items():
        previous = supersede_landing.get(target)
        if previous is None or index > previous[0]:
            supersede_landing[target] = (index, by)
    sup_map = {target: by for target, (_, by) in supersede_landing.items()}
    superseded = sorted(cid for cid in ids if cid in sup_map)
    last_edit = {}
    for index, changed in changed_at.items():
        for cid in changed:
            last_edit[cid] = index
    superseded_as_of = []
    stale_supersede = []
    for cid in superseded:
        landing = supersede_landing[cid][0]
        if cid in last_edit and landing > last_edit[cid]:
            superseded_as_of.append(cid)
        else:
            stale_supersede.append(cid)

    round_changed = set()
    if round_base:
        base_full = git(repo, "rev-parse", "--verify",
                        round_base + "^{commit}").strip()
        in_range = set(git(repo, "log", "--format=%H",
                           "%s..%s" % (base_full, rev_full)).split())
        for index, commit in enumerate(commits):
            if commit in in_range:
                round_changed |= changed_at.get(index, set())
                round_changed |= deleted_at.get(index, set())

    return {
        "rev": rev_full,
        "ids": ids,
        "deleted": deleted,
        "superseded": superseded,
        "round_changed": sorted(round_changed),
        "violations": len(ids) + len(deleted),
        "superseded_by": sup_map,
        "superseded_as_of": superseded_as_of,
        "stale_supersede": stale_supersede,
        "commits": commits,
        "rows": len(tip),
    }


def format_list(items):
    return ",".join(items)


def report(result):
    """The lines the gate prints, in order."""
    lines = []
    for cid in result["ids"]:
        lines.append("changed %s superseded_by=%s"
                     % (cid, result["superseded_by"].get(cid, "-")))
    for cid in result["deleted"]:
        lines.append("deleted %s" % cid)
    lines.append("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] "
                 "round_changed=[%s]"
                 % (result["violations"], format_list(result["ids"]),
                    format_list(result["deleted"]),
                    format_list(result["superseded"]),
                    format_list(result["round_changed"])))
    lines.append("supersede_timing superseded_as_of=[%s] stale_supersede=[%s]"
                 % (format_list(result["superseded_as_of"]),
                    format_list(result["stale_supersede"])))
    return lines


# --------------------------------------------------------------------- selftest

def _selftest_env():
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                "GIT_COMMON_DIR"):
        env.pop(key, None)
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _row(rid, source="https://example.invalid/a", kind="docs", tier="A",
         scope="scope a", anchor="anchor a", teaches="teaches a",
         status="mined", opened="2026-01-01", recheck="on-release",
         used_by="n/a"):
    return [rid, source, kind, tier, scope, anchor, teaches, status, opened,
            recheck, used_by]


def _render(rows):
    out = ["# SOURCES — selftest registry", "", "## Registry", "",
           "| " + " | ".join(COLUMNS) + " |",
           "|" + "|".join(["---"] * len(COLUMNS)) + "|"]
    for cells in rows:
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def _git_in(path, *args, env):
    proc = subprocess.run(["git", "-C", path] + list(args), capture_output=True,
                          text=True, timeout=120, env=env)
    if proc.returncode != 0:
        raise GateError("selftest git %s failed: %s"
                        % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def _make_repo(path, snapshots, env):
    """Create a repo whose history is the given list of SOURCES.md bodies."""
    os.makedirs(os.path.join(path, "corpus"), exist_ok=True)
    _git_in(path, "init", "-q", env=env)
    _git_in(path, "config", "user.name", "mori selftest", env=env)
    _git_in(path, "config", "user.email", "selftest@example.invalid", env=env)
    _git_in(path, "config", "commit.gpgsign", "false", env=env)
    shas = []
    for index, body in enumerate(snapshots):
        target = os.path.join(path, "corpus", "SOURCES.md")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(body)
        _git_in(path, "add", "corpus/SOURCES.md", env=env)
        _git_in(path, "commit", "-q", "-m", "c%d" % index, env=env)
        shas.append(_git_in(path, "rev-parse", "HEAD", env=env).strip())
    return shas


def _selftest_cases():
    """(name, snapshots, expected dict) triples; expected holds the four lists."""
    base = _render([_row("S001")])
    mutable = _render([_row("S001", status="queued")])
    edited = _render([_row("S001", anchor="anchor a v2")])
    reverted = _render([_row("S001")])
    padded = _render([_row("S001", anchor="  anchor a  ", status=" mined ")])
    two_rows = _render([_row("S001"), _row("S002", source="https://example.invalid/b",
                                            anchor="anchor b", teaches="teaches b")])
    one_row = _render([_row("S001")])
    superseding = _render([_row("S001", anchor="anchor a v2"),
                            _row("S002", source="https://example.invalid/b",
                                 anchor="anchor b", teaches="supersedes S001 — replacement")])
    with_old_superseder = _render([_row("S001"),
                                   _row("S002", source="https://example.invalid/b",
                                        anchor="anchor b",
                                        teaches="supersedes S001 — replacement")])
    old_superseder_then_edit = _render([
        _row("S001", anchor="anchor a v3"),
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    reordered = _render([_row("S002", source="https://example.invalid/b",
                              anchor="anchor b", teaches="teaches b"), _row("S001")])
    return [
        ("clean history", [base, two_rows], 0,
         {"ids": [], "deleted": [], "superseded": [], "round_changed": [],
          "superseded_as_of": [], "stale_supersede": []}),
        ("mutable-only edit", [base, mutable], 0,
         {"ids": [], "deleted": [], "superseded": [], "round_changed": [],
          "superseded_as_of": [], "stale_supersede": []}),
        ("immutable edit", [base, edited], 1,
         {"ids": ["S001"], "deleted": [], "superseded": [], "round_changed": ["S001"],
          "superseded_as_of": [], "stale_supersede": []}),
        ("changed-back inside the round", [base, edited, reverted], 1,
         {"ids": [], "deleted": [], "superseded": [], "round_changed": ["S001"],
          "superseded_as_of": [], "stale_supersede": []}),
        ("deleted row", [two_rows, one_row], 1,
         {"ids": [], "deleted": ["S002"], "superseded": [], "round_changed": ["S002"],
          "superseded_as_of": [], "stale_supersede": []}),
        ("superseding row", [base, edited, superseding], 1,
         {"ids": ["S001"], "deleted": [], "superseded": ["S001"], "round_changed": ["S001"],
          "superseded_by": {"S001": "S002"}, "superseded_as_of": ["S001"],
          "stale_supersede": []}),
        ("supersede before edit", [with_old_superseder, old_superseder_then_edit], 1,
         {"ids": ["S001"], "deleted": [], "superseded": ["S001"],
          "round_changed": ["S001"], "superseded_by": {"S001": "S002"},
          "superseded_as_of": [], "stale_supersede": ["S001"]}),
        ("row reorder", [two_rows, reordered], 0,
         {"ids": [], "deleted": [], "superseded": [], "round_changed": [],
          "superseded_as_of": [], "stale_supersede": []}),
        ("whitespace padding", [base, padded], 0,
         {"ids": [], "deleted": [], "superseded": [], "round_changed": [],
          "superseded_as_of": [], "stale_supersede": []}),
    ]


def _run_cli(args, env):
    """Run this tool as a child process; returns (returncode, stdout)."""
    proc = subprocess.run([sys.executable, os.path.abspath(__file__)] + list(args),
                          capture_output=True, text=True, timeout=180, env=env)
    return proc.returncode, proc.stdout


def selftest():
    """Build small sandbox repos and check the gate's own verdict on each.

    The check drives the command line, exactly as the round-36 counter does:
    `HEAD --repo <sandbox> --round-base <sha>` in a repo whose history is a
    fixture.  Every expectation below is written by hand, not derived from
    the tool's own output.
    """
    env = _selftest_env()
    root = tempfile.mkdtemp(prefix="mori-sources-appendonly-selftest-")
    passed = 0
    failed = 0
    try:
        for index, (name, snapshots, expected_exit, expected) in enumerate(_selftest_cases()):
            repo = os.path.join(root, "case%02d" % index)
            try:
                shas = _make_repo(repo, snapshots, env)
                base_sha = shas[0]
                code, stdout = _run_cli(["HEAD", "--repo", repo,
                                         "--round-base", base_sha], env)
                lines = [l for l in stdout.splitlines()
                         if l.strip() and l.strip() != PREDICATE]
                summary_lines = [l for l in lines if SUMMARY_RE.match(l.strip())]
                problems = []
                if len(summary_lines) != 1:
                    problems.append("expected one summary line, got %d"
                                    % len(summary_lines))
                    summary = lines[-1] if lines else ""
                else:
                    summary = summary_lines[0].strip()
                got = {
                    "ids": [l.split()[1] for l in lines if l.startswith("changed ")],
                    "deleted": [l.split()[1] for l in lines if l.startswith("deleted ")],
                }
                if summary_lines:
                    groups = SUMMARY_RE.match(summary).groups()
                    got["superseded"] = [p for p in groups[3].split(",") if p]
                    got["round_changed"] = [p for p in groups[4].split(",") if p]
                    violations = int(groups[0])
                    if violations != len(got["ids"]) + len(got["deleted"]):
                        problems.append("violations %d != len(ids)+len(deleted)"
                                        % violations)
                else:
                    got["superseded"] = []
                    got["round_changed"] = []
                timing_lines = [l for l in lines if TIMING_RE.match(l.strip())]
                if len(timing_lines) != 1:
                    problems.append("expected one supersede_timing line, got %d"
                                    % len(timing_lines))
                    got["superseded_as_of"] = []
                    got["stale_supersede"] = []
                else:
                    tgroups = TIMING_RE.match(timing_lines[0].strip()).groups()
                    got["superseded_as_of"] = [p for p in tgroups[0].split(",") if p]
                    got["stale_supersede"] = [p for p in tgroups[1].split(",") if p]
                for key in ("ids", "deleted", "superseded", "round_changed",
                            "superseded_as_of", "stale_supersede"):
                    if got[key] != expected[key]:
                        problems.append("%s: want %s got %s"
                                        % (key, expected[key], got[key]))
                if code != expected_exit:
                    problems.append("exit: want %d got %d" % (expected_exit, code))
                want_by = expected.get("superseded_by", {})
                for cid, by in want_by.items():
                    match = [l for l in lines
                             if l.startswith("changed %s " % cid)]
                    if not match or not match[0].endswith("superseded_by=%s" % by):
                        problems.append("superseded_by[%s]: want %s got %r"
                                        % (cid, by, match[0] if match else None))
                for line in lines:
                    if SUMMARY_RE.match(line) or TIMING_RE.match(line):
                        continue
                    if not (re.match(r"^changed S\d{3} superseded_by=(\S+)$", line)
                            or re.match(r"^deleted S\d{3}$", line)):
                        problems.append("per-id line malformed: %r" % line)
                if problems:
                    failed += 1
                    print("FAIL %s: %s" % (name, "; ".join(problems)))
                else:
                    passed += 1
            except Exception as exc:                 # noqa: BLE001 - selftest reports
                failed += 1
                print("FAIL %s: %s" % (name, exc))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("MORI_SOURCES_APPENDONLY_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if failed == 0 else 1


# ----------------------------------------------------------------------- main

def main(argv):
    parser = argparse.ArgumentParser(
        description="CORPUS.md rule 2 gate for corpus/SOURCES.md")
    parser.add_argument("rev", nargs="?", help="revision to inspect")
    parser.add_argument("--repo", default=".", help="repository directory")
    parser.add_argument("--round-base", default=None,
                        help="start of the round (exclusive); enables round_changed")
    parser.add_argument("--path", default=DEFAULT_PATH, help="registry path")
    parser.add_argument("--selftest", action="store_true",
                        help="run the fixture self-test and exit")
    parser.add_argument("--print-predicate", action="store_true",
                        help="print the frozen P-C6 predicate and exit")
    args = parser.parse_args(argv)

    if args.print_predicate:
        print(PREDICATE)
        return 0
    if args.selftest:
        return selftest()
    if not args.rev:
        parser.error("a revision is required (or --selftest)")

    try:
        result = analyze(args.repo, args.rev, args.path,
                         round_base=args.round_base)
    except GateError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    print(PREDICATE)
    for line in report(result):
        print(line)
    if args.round_base:
        return 1 if result["round_changed"] else 0
    return 1 if (result["ids"] or result["deleted"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
