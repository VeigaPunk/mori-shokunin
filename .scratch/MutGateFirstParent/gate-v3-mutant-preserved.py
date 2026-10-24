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

Read-only: the only git commands used are `rev-parse`, `log`, `show` and
`merge-base --is-ancestor`. No writes, no network, no clone.
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
    "P-C11: at revision R, tools/mori-sources-appendonly.py reports, after its "
    "summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; "
    "the timing line's eligible set is every superseded id present at R — a "
    "never-edited superseded id's last immutable-cell edit is its first-sighting "
    "commit, so it reaches the as-of/stale test — and an edit at a commit is a "
    "change against its first parent's state only: when the first parent lacks "
    "the path the commit contributes no edits (a delete-then-re-add contributes "
    "no changed event; ids still compare tip cells against first-sighting "
    "cells), never a fall-through to another parent's state; the lane-history "
    "verdicts are unchanged except the eligible-set extension — S226 joins "
    "superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, "
    "S069 is stale at e37dcc6 — and the selftest carries committed fixtures for "
    "a never-edited superseded row (as-of), a merge whose first parent lacks "
    "the path (no fabricated edit), and a linear delete-then-re-add (no changed "
    "event)."
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


def nearest_path_commit(repo, commit, path):
    """Newest commit at-or-before <commit> whose tree carries <path>, or None.

    A commit's graph parent often does not touch the registry (spot-check and
    verifier commits land between registry commits), so the walk's reference
    state for a commit is its nearest path-carrying ancestor, resolved per
    parent.
    """
    out = git(repo, "log", "--format=%H", "-1", commit, "--", path).strip()
    return out or None


def is_ancestor(repo, older, newer):
    """True when <older> is an ancestor of (or equal to) <newer>."""
    try:
        proc = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor",
                               older, newer],
                              capture_output=True, timeout=120, env=_clean_env())
    except subprocess.TimeoutExpired:
        raise GateError("git merge-base --is-ancestor timed out")
    except OSError as exc:
        raise GateError("git merge-base failed to start: %s" % exc)
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    raise GateError("git merge-base --is-ancestor %s %s failed: %s"
                    % (older, newer, proc.stderr.decode("utf-8", "replace").strip()))


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
    """Walk the path's history and return the four lists plus the verdict.

    Version 3 (round 40, r39 w1 findings 2/5): the supersede_timing eligible
    set is every superseded id present at R — a never-edited superseded id's
    last immutable-cell edit is its first-sighting commit — and an edit at a
    commit is a change against its first parent's state only, read from the
    first parent's own tree: when the first parent lacks the path (or the
    row) the commit contributes no edits and never falls through to another
    parent's or ancestor's state, so a delete-then-re-add contributes no
    changed event (persistent drift still surfaces in `ids`, which compares
    tip cells against first-sighting cells). Version 2 semantics (round 39,
    r38 lesson F1/F2) are retained for everything else: the walk carries
    parent hashes and uses `--full-history`; the supersede-as-of test is
    `git merge-base --is-ancestor` between the id's last edit commit and the
    superseding row's landing commit (not walk index order).
    """
    rev_full = git(repo, "rev-parse", "--verify", rev + "^{commit}").strip()
    tip_text = git_blob(repo, "%s:%s" % (rev_full, path))
    if tip_text is None:
        raise GateError("%s is absent at %s" % (path, rev_full))
    tip_rows, tip_colmap = parse_registry(tip_text)
    if tip_colmap is None:
        raise GateError("no registry header in %s at %s" % (path, rev_full))

    walk = []
    for line in git(repo, "log", "--format=%H%x09%P", "--reverse",
                    "--full-history", rev_full, "--", path).splitlines():
        commit, _, parents = line.partition("\t")
        walk.append((commit, parents.split() if parents else []))
    commits = [commit for commit, _ in walk]
    parents_of = dict(walk)
    by_hash = {commit: index for index, commit in enumerate(commits)}

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
    first_commit = {}   # id -> commit of its first sighting in the walk
    changed_at = {}     # commit index -> ids whose immutable cells changed
    deleted_at = {}     # commit index -> ids that disappeared there
    supersede_rows = {}     # (superseded id, superseder id) -> first index it appears
    supersede_landing = {}  # superseded id -> (latest landing index, that superseder id)
    teaches_idx = (colmap or {}).get("teaches", COLUMNS.index("teaches"))
    for index, commit in enumerate(commits):
        rows = states[index]
        if rows is None:
            continue
        for cells in rows:
            if teaches_idx >= len(cells):
                continue
            m = SUPERSEDES_RE.match(cells[teaches_idx].strip())
            if m:
                supersede_rows.setdefault((m.group(1), cells[0].strip()), index)
        current = {cells[0]: cells for cells in rows}
        ref = None
        for parent in parents_of.get(commit, []):
            ref_commit = parent if parent in by_hash else \
                nearest_path_commit(repo, parent, path)
            if ref_commit is None:
                continue
            pidx = by_hash.get(ref_commit)
            if pidx is not None and states[pidx] is not None:
                ref = states[pidx]
                break
        if ref is None:
            for cid, cells in current.items():
                if cid not in first:
                    first[cid] = cells
                    first_commit[cid] = commit
            continue
        ref_cells = {cells[0]: cells for cells in ref}
        for cid, cells in current.items():
            if cid not in first:
                first[cid] = cells
                first_commit[cid] = commit
            elif cid in ref_cells:
                if imm_key(cells, imm_idx) != imm_key(ref_cells[cid], imm_idx):
                    changed_at.setdefault(index, set()).add(cid)
            # P-C11: no `elif not is_merge` re-add branch — a row whose first
            # parent lacks it is an addition, not an edit; persistent drift
            # still surfaces through the ids tip-vs-first-sighting comparison
            # (r39 w1 finding 5a).
        gone = set(ref_cells) - set(current)
        if gone:
            deleted_at.setdefault(index, set()).update(gone)

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
    # P-C11: the timing line's eligible set is every superseded id present at
    # R, not only the edit-bounded `ids` list — a never-edited superseded id
    # still reaches the as-of/stale test (r39 w1 finding 2).
    superseded = sorted(cid for cid in tip if cid in sup_map)
    last_edit = {}
    for index, changed in changed_at.items():
        for cid in changed:
            last_edit[cid] = commits[index]
    superseded_as_of = []
    stale_supersede = []
    for cid in superseded:
        landing_index = supersede_landing[cid][0]
        # a never-edited id's last immutable-cell edit is its first-sighting
        # commit (P-C11's plain words; the round-39 gate never reached it)
        edit_commit = last_edit.get(cid) or first_commit.get(cid)
        if edit_commit is not None and is_ancestor(
                repo, edit_commit, commits[landing_index]):
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


def _dag_commit(path, body, msg, when, env):
    """One commit on the current branch with pinned author/committer dates."""
    os.makedirs(os.path.join(path, "corpus"), exist_ok=True)
    target = os.path.join(path, "corpus", "SOURCES.md")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(body)
    _git_in(path, "add", "corpus/SOURCES.md", env=env)
    dated = dict(env, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    proc = subprocess.run(["git", "-C", path, "commit", "-q", "-m", msg],
                          capture_output=True, text=True, timeout=120, env=dated)
    if proc.returncode != 0:
        raise GateError("selftest dag commit %s failed: %s"
                        % (msg, proc.stderr.strip()))
    return _git_in(path, "rev-parse", "HEAD", env=env).strip()


def _dag_init(path, env):
    os.makedirs(path, exist_ok=True)
    _git_in(path, "init", "-q", "-b", "main", env=env)
    _git_in(path, "config", "user.name", "mori selftest", env=env)
    _git_in(path, "config", "user.email", "selftest@example.invalid", env=env)
    _git_in(path, "config", "commit.gpgsign", "false", env=env)


def _dag_merge(path, side, msg, when, env):
    dated = dict(env, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    proc = subprocess.run(["git", "-C", path, "merge", "-q", "--no-edit",
                           "-m", msg, side],
                          capture_output=True, text=True, timeout=120, env=dated)
    if proc.returncode != 0:
        raise GateError("selftest dag merge %s failed: %s"
                        % (msg, proc.stderr.strip()))
    return _git_in(path, "rev-parse", "HEAD", env=env).strip()


def _selftest_dag_cases():
    """Round-39 ancestry fixtures (r38 F1/F2, resid/ResidGateTiming A and C).

    Returns (name, kind, expected_exit, expected, round_base_name) tuples; the
    repo is built by _make_dag_repo with the named shas the expectations rely
    on. Dates pin the default-order walk so the round-38 index-order gate
    demonstrably misclassifies both fixtures (red receipts in round-39
    evidence), while the ancestry gate classifies them as written here.
    """
    # the buffer row keeps the side branch's append off the edited line's merge
    # hunk (git conflicts when an append is adjacent to a modified line), so
    # the fixture merge is clean — a conflict would test git, not the gate
    buffer = _row("S008", source="https://example.invalid/e", anchor="anchor e",
                  teaches="teaches e")
    base = _render([_row("S001"), buffer])
    edited = _render([_row("S001", anchor="anchor a v2"), buffer])
    side_superseding = _render([
        _row("S001"), buffer,
        _row("S009", source="https://example.invalid/f", anchor="anchor f",
             teaches="teaches f"),
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    side_plain = _render([
        _row("S001"), buffer,
        _row("S009", source="https://example.invalid/f", anchor="anchor f",
             teaches="teaches f"),
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="teaches b")])
    merged_superseding = _render([
        _row("S001", anchor="anchor a v2"), buffer,
        _row("S009", source="https://example.invalid/f", anchor="anchor f",
             teaches="teaches f"),
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="teaches b"),
        _row("S003", source="https://example.invalid/c", anchor="anchor c",
             teaches="supersedes S001 — replacement")])
    # dag-d: both branches make the same S001 edit independently; the
    # supersede row rides the side branch, so the row's landing commit IS
    # the id's last edit commit (ancestry: as-of). The round-38 walk-order
    # gate prints stale there; the predicate's plain words read as-of.
    side_edit_superseding = _render([
        _row("S001", anchor="anchor a v2"), buffer,
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    merged_both_edited = _render([
        _row("S001", anchor="anchor a v2"), buffer,
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    # dag-n (P-C11 eligible set): a superseding row lands without any edit to
    # the superseded row — the never-edited id's last immutable-cell edit is
    # its first-sighting commit, so it must still reach the as-of/stale test
    supersede_only = _render([
        _row("S001"), buffer,
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    # dag-p (P-C11 first-parent reference): main deletes the registry, the
    # side branch edits S001 and lands the supersede row, and the merge
    # resolves to a third content — the merge's first parent lacks the path,
    # so the merge contributes no edits (v2 falls through to the side
    # parent's state and fabricates a changed event plus a stale verdict)
    edited_and_superseding = _render([
        _row("S001", anchor="anchor a v2"), buffer,
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    merge_resolved = _render([
        _row("S001", anchor="anchor a v3"), buffer,
        _row("S002", source="https://example.invalid/b", anchor="anchor b",
             teaches="supersedes S001 — replacement")])
    # dag-r (P-C11 re-add): S008 is superseded, then deleted, then re-added
    # with identical cells on a linear history — the re-add is an addition
    # against a parent that lacks the row, not an edit, so the never-edited
    # id's last edit stays its first-sighting commit (as-of, not stale). The
    # round-39 gate re-flags the re-add as the last edit and prints stale.
    supersede_s008 = _render([
        _row("S001"), buffer,
        _row("S009", source="https://example.invalid/f", anchor="anchor f",
             teaches="supersedes S008 — replacement")])
    without_s008 = _render([
        _row("S001"),
        _row("S009", source="https://example.invalid/f", anchor="anchor f",
             teaches="supersedes S008 — replacement")])
    return [
        ("side-branch superseder is stale", "dag-a", 1,
         {"ids": ["S001"], "deleted": [], "superseded": ["S001"],
          "round_changed": ["S001"], "superseded_by": {"S001": "S002"},
          "superseded_as_of": [], "stale_supersede": ["S001"]}, "b0"),
        ("merge does not fabricate an edit", "dag-c", 0,
         {"ids": ["S001"], "deleted": [], "superseded": ["S001"],
          "round_changed": [], "superseded_by": {"S001": "S003"},
          "superseded_as_of": ["S001"], "stale_supersede": []}, "c1"),
        ("landing is the last edit commit", "dag-d", 1,
         {"ids": ["S001"], "deleted": [], "superseded": ["S001"],
          "round_changed": ["S001"], "superseded_by": {"S001": "S002"},
          "superseded_as_of": ["S001"], "stale_supersede": []}, "b0"),
        ("never-edited superseded row is as-of", "dag-n", 0,
         {"ids": [], "deleted": [], "superseded": ["S001"],
          "round_changed": [],
          "superseded_as_of": ["S001"], "stale_supersede": []}, "b0"),
        ("first-parent-lacks-path merge contributes no edits", "dag-p", 1,
         {"ids": ["S001"], "deleted": [], "superseded": ["S001"],
          "round_changed": ["S001"], "superseded_by": {"S001": "S002"},
          "superseded_as_of": ["S001"], "stale_supersede": []}, "b0"),
        ("linear delete-then-re-add is not an edit", "dag-r", 1,
         {"ids": [], "deleted": [], "superseded": ["S008"],
          "round_changed": ["S008"],
          "superseded_as_of": ["S008"], "stale_supersede": []}, "b0"),
    ], (base, edited, side_superseding, side_plain, merged_superseding,
        side_edit_superseding, merged_both_edited, supersede_only,
        edited_and_superseding, merge_resolved, supersede_s008,
        without_s008)


def _make_dag_repo(path, kind, bodies, env):
    """Build fixture DAG A, C, D, N, P or R; returns {name: sha}."""
    (base, edited, side_superseding, side_plain, merged_superseding,
     side_edit_superseding, merged_both_edited, supersede_only,
     edited_and_superseding, merge_resolved, supersede_s008,
     without_s008) = bodies
    _dag_init(path, env)
    shas = {}
    if kind == "dag-a":
        shas["b0"] = _dag_commit(path, base, "b0", "2026-01-01T00:00:00Z", env)
        shas["e1"] = _dag_commit(path, edited, "e1", "2026-01-01T01:00:00Z", env)
        _git_in(path, "checkout", "-q", "-b", "side", shas["b0"], env=env)
        shas["s1"] = _dag_commit(path, side_superseding, "s1",
                                 "2026-01-01T02:00:00Z", env)
        _git_in(path, "checkout", "-q", "main", env=env)
        shas["m"] = _dag_merge(path, "side", "m", "2026-01-01T03:00:00Z", env)
    elif kind == "dag-d":
        shas["b0"] = _dag_commit(path, base, "b0", "2026-01-01T00:00:00Z", env)
        shas["e1"] = _dag_commit(path, edited, "e1", "2026-01-01T01:00:00Z", env)
        _git_in(path, "checkout", "-q", "-b", "side", shas["b0"], env=env)
        shas["s1"] = _dag_commit(path, side_edit_superseding, "s1",
                                 "2026-01-01T02:00:00Z", env)
        _git_in(path, "checkout", "-q", "main", env=env)
        shas["m"] = _dag_merge(path, "side", "m", "2026-01-01T03:00:00Z", env)
    elif kind == "dag-c":
        shas["b0"] = _dag_commit(path, base, "b0", "2026-01-01T00:00:00Z", env)
        shas["c1"] = _dag_commit(path, edited, "c1", "2026-01-01T01:00:00Z", env)
        _git_in(path, "checkout", "-q", "-b", "side", shas["b0"], env=env)
        shas["c2"] = _dag_commit(path, side_plain, "c2",
                                 "2026-01-01T02:00:00Z", env)
        _git_in(path, "checkout", "-q", "main", env=env)
        shas["m"] = _dag_merge(path, "side", "m", "2026-01-01T03:00:00Z", env)
        shas["t"] = _dag_commit(path, merged_superseding, "t",
                                "2026-01-01T04:00:00Z", env)
        shas["c1"] = shas["c1"]
    elif kind == "dag-n":
        shas["b0"] = _dag_commit(path, base, "b0", "2026-01-01T00:00:00Z", env)
        shas["n1"] = _dag_commit(path, supersede_only, "n1",
                                 "2026-01-01T01:00:00Z", env)
    elif kind == "dag-p":
        shas["b0"] = _dag_commit(path, base, "b0", "2026-01-01T00:00:00Z", env)
        _git_in(path, "checkout", "-q", "-b", "side", shas["b0"], env=env)
        shas["s1"] = _dag_commit(path, edited_and_superseding, "s1",
                                 "2026-01-01T01:00:00Z", env)
        _git_in(path, "checkout", "-q", "main", env=env)
        _git_in(path, "rm", "-q", "corpus/SOURCES.md", env=env)
        dated = dict(env, GIT_AUTHOR_DATE="2026-01-01T02:00:00Z",
                     GIT_COMMITTER_DATE="2026-01-01T02:00:00Z")
        _git_in(path, "commit", "-q", "-m", "d1", env=dated)
        shas["d1"] = _git_in(path, "rev-parse", "HEAD", env=env).strip()
        # modify/delete conflict: resolve to the third content and commit the
        # merge — the merge's first parent (d1) lacks the path
        dated = dict(env, GIT_AUTHOR_DATE="2026-01-01T03:00:00Z",
                     GIT_COMMITTER_DATE="2026-01-01T03:00:00Z")
        proc = subprocess.run(["git", "-C", path, "merge", "--no-edit",
                               "-m", "m", "side"],
                              capture_output=True, text=True, timeout=120,
                              env=dated)
        if proc.returncode == 0:
            raise GateError("selftest dag-p merge unexpectedly clean")
        target = os.path.join(path, "corpus", "SOURCES.md")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(merge_resolved)
        _git_in(path, "add", "corpus/SOURCES.md", env=env)
        _git_in(path, "commit", "-q", "-m", "m", "--no-edit", env=dated)
        shas["m"] = _git_in(path, "rev-parse", "HEAD", env=env).strip()
    elif kind == "dag-r":
        shas["b0"] = _dag_commit(path, base, "b0", "2026-01-01T00:00:00Z", env)
        shas["s1"] = _dag_commit(path, supersede_s008, "s1",
                                 "2026-01-01T01:00:00Z", env)
        shas["r1"] = _dag_commit(path, without_s008, "r1",
                                 "2026-01-01T02:00:00Z", env)
        shas["r2"] = _dag_commit(path, supersede_s008, "r2",
                                 "2026-01-01T03:00:00Z", env)
    else:
        raise GateError("unknown dag kind %r" % kind)
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

    def check_one(name, repo, base_sha, expected_exit, expected):
        nonlocal passed, failed
        try:
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
            nonlocal_failed_append(name, exc)

    def nonlocal_failed_append(name, exc):
        nonlocal failed
        failed += 1
        print("FAIL %s: %s" % (name, exc))

    try:
        for index, (name, snapshots, expected_exit, expected) in enumerate(
                _selftest_cases()):
            repo = os.path.join(root, "case%02d" % index)
            try:
                shas = _make_repo(repo, snapshots, env)
                check_one(name, repo, shas[0], expected_exit, expected)
            except Exception as exc:             # noqa: BLE001 - selftest reports
                failed += 1
                print("FAIL %s: %s" % (name, exc))
        dag_cases, dag_bodies = _selftest_dag_cases()
        for offset, (name, kind, expected_exit, expected, base_name) in enumerate(
                dag_cases):
            repo = os.path.join(root, "dag%02d" % offset)
            try:
                shas = _make_dag_repo(repo, kind, dag_bodies, env)
                check_one(name, repo, shas[base_name], expected_exit, expected)
            except Exception as exc:             # noqa: BLE001 - selftest reports
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
                        help="print the frozen P-C11 predicate and exit")
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
