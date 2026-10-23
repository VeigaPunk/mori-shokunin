#!/usr/bin/env python3
"""Round-37 C1 counter v2 (amendment A1): does the C2 measurement discriminate a real-arm memoizer?

Usage:
    count-c1.py <rev> [--repo DIR] [--tool FILE] [--negatives DIR] [--seed N]

<rev> is the revision that must carry tools/mori-sources-appendonly.py.
Without --tool the tool is taken from `git show <rev>:tools/mori-sources-appendonly.py`
(written to a temp file); with --tool FILE that file is used instead (controls).
--seed makes the blind arm replayable; a scored run draws its seed from os.urandom.

Arms:
  blind          24 sandbox git histories drawn at run time, hidden truth from the
                 counter's own op log; both the summary line and the per-id
                 `changed <id> ...` / `deleted <id>` lines must match.
  real           the lane's own history (rev 6bd57097, round base f10a320d) against the
                 counter's independent git walk; summary and per-id lines must match.
  real-challenge one run-time-drawn history presented in real-arm clothing: a path under
                 the lane repo's own .ufo/waves/round-37/scratch, the lane git identity,
                 the lane SOURCES title. Its truth is the counter's op log, never a
                 published constant (closes w2/RevNgC2 N1: a tool that gates on the
                 sandbox identity and prints the receipt's constant).
  negatives      three fixture tools must each be REJECTED by the same machinery:
                 memo-n1 (honest on sandboxes, constant elsewhere), const (constant
                 everywhere), summary-only (correct four lists, no `deleted <id>` lines).

Exit: 0 met, 1 unmet, 2 counter setup error. A tool timeout is reported as
`tool_timeout` and scored unmet-by-timeout, never as a list mismatch; the counter
SIGTERMs the child's process group first and SIGKILLs only after a grace period.
"""
import argparse
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

PREDICATE = (
    "P-C1: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's "
    "hidden truth for ids, deleted, superseded and round_changed, and exactly the truth's "
    "per-id `changed`/`deleted` lines, on each of 24 sandbox SOURCES.md histories drawn at "
    "run time, on the lane's own history (rev 6bd57097, round base f10a320d) where the "
    "independent oracle lists at least one id, and on one run-time-drawn challenge history "
    "presented in real-arm clothing (lane path, lane git identity, lane title); and the same "
    "counter rejects all three negative fixtures (a real-arm memoizer, a constant printer, a summary-only "
    "printer) and matches the standing truth on one run-time-drawn ancestor revision of the lane repository "
    "whose expected answer is not the published real-arm constant."
)

DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
TOOL_REL = "tools/mori-sources-appendonly.py"
SCRATCH_ROOT = "/fast/scratch/hyaku/mori-r37"
CHALLENGE_PARENT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-37", "scratch")
NEGATIVES_DIR = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-37", "fixtures")

REAL_REV = "6bd57097"
REAL_BASE = "f10a320d"
N_SANDBOX = 24
NEG_BLIND = 4          # blind histories drawn for each negative fixture
TOOL_TIMEOUT_S = 120
TOOL_GRACE_S = 5

PATH = "corpus/SOURCES.md"
COLUMNS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
           "status", "opened", "recheck", "used-by"]
MUTABLE = ("status", "recheck", "used-by")

SUMMARY_RE = re.compile(
    r"^appendonly_violations=(\d+)\s+ids=\[([^\]]*)\]\s+deleted=\[([^\]]*)\]\s+"
    r"superseded=\[([^\]]*)\]\s+round_changed=\[([^\]]*)\]$")
SUPERSEDES_RE = re.compile(r"^supersedes\s+(S\d{3})\b")
CELL_RE = re.compile(r"^:?-{3,}:?$")


# ------------------------------------------------------------------ process runs

def clean_env():
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(key, None)
    return env


class ToolTimeout(Exception):
    """The child's process group exceeded the tool budget."""


def run(cmd, cwd=None, timeout=120, env=None):
    """Run a command in its own process group; on timeout SIGTERM the group, wait
    TOOL_GRACE_S, then SIGKILL only that group. The child is never killed before it
    had a chance to flush; the boundary is disclosed in the predicate output."""
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except OSError:
            pass
        try:
            out, err = proc.communicate(timeout=TOOL_GRACE_S)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except OSError:
                pass
            out, err = proc.communicate()
        raise ToolTimeout("tool exceeded %ds (SIGTERM, then SIGKILL after %ds)"
                          % (timeout, TOOL_GRACE_S))
    return subprocess.CompletedProcess(cmd, proc.returncode, out, err)


def git(repo, *args, check=True, timeout=120):
    proc = run(["git", "-C", repo] + list(args), timeout=timeout, env=clean_env())
    if check and proc.returncode != 0:
        raise RuntimeError("git %s failed in %s: %s" % (" ".join(args), repo,
                                                        proc.stderr.strip()))
    return proc


def git_out(repo, *args):
    return git(repo, *args).stdout


# ------------------------------------------------------------------- registry io

def parse_registry(text):
    """Return (rows, colmap) for a SOURCES.md body.

    rows: list of cell lists (one per registry row, header order).
    colmap: header column name -> index, or None when no header was found.
    """
    lines = text.splitlines()
    header_at = None
    header = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if cells and cells[0].lower() == "id" and len(cells) >= 5:
            header, header_at = cells, i
            break
    if header is None:
        return [], None
    colmap = {}
    for i, name in enumerate(header):
        colmap.setdefault(name.strip().lower(), i)
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
        if not re.fullmatch(r"S\d{3}", cells[0]):
            continue
        rows.append(cells)
    return rows, colmap


def immutable_indices(colmap):
    if not colmap:
        colmap = {name: i for i, name in enumerate(COLUMNS)}
    return [colmap[name] for name in COLUMNS if name not in MUTABLE and name in colmap]


def imm_key(cells, imm_idx):
    """Immutable cell fingerprint; cells compare stripped."""
    return tuple(cells[i].strip() for i in imm_idx)


def superseders(rows, colmap):
    """superseded id -> superseding row id, for rows whose teaches opens `supersedes S###`."""
    teaches_idx = (colmap or {}).get("teaches", COLUMNS.index("teaches"))
    out = {}
    for cells in rows:
        match = SUPERSEDES_RE.match(cells[teaches_idx].strip())
        if match:
            out.setdefault(match.group(1), cells[0].strip())
    return out


def format_summary(truth):
    return ("appendonly_violations=%d ids=[%s] deleted=[%s] superseded=[%s] round_changed=[%s]"
            % (truth["violations"], ",".join(truth["ids"]), ",".join(truth["deleted"]),
               ",".join(truth["superseded"]), ",".join(truth["round_changed"])))


def truth_from_states(states, base_index, colmap):
    """Truth for a sequence of row states (one per commit).

    states[i] is the ordered list of row cell-lists held at commit i.
    base_index is the index of the round base commit; commits after it are in range.

    Change detection mirrors the contract: at each commit an id counts as changed
    when its immutable cells differ from the cells it last held in an earlier
    commit, and an id counts as deleted when it was present in the previous commit
    and is gone now.
    """
    imm_idx = immutable_indices(colmap)
    first = {}
    changed_at = {}
    deleted_at = {}
    last_seen = {}
    prev_ids = set()
    for index, rows in enumerate(states):
        current = {cells[0].strip(): cells for cells in rows}
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
    tip_rows = states[-1]
    tip = {cells[0].strip(): cells for cells in tip_rows}
    ids = sorted(cid for cid, cells in tip.items()
                 if imm_key(cells, imm_idx) != imm_key(first[cid], imm_idx))
    deleted = sorted(set(first) - set(tip))
    sup_map = superseders(tip_rows, colmap)
    superseded = sorted(cid for cid in ids if cid in sup_map)
    round_changed = set()
    for index in range(base_index + 1, len(states)):
        round_changed |= changed_at.get(index, set()) | deleted_at.get(index, set())
    # ids edited away and edited back to their first cells (history fact, not a list)
    changed_back = []
    for cid in sorted(tip):
        if cid in ids:
            continue
        first_key = imm_key(first[cid], imm_idx)
        for rows in states:
            current = {cells[0].strip(): cells for cells in rows}
            if cid not in current:
                continue
            if imm_key(current[cid], imm_idx) != first_key:
                changed_back.append(cid)
                break
    return {
        "ids": ids,
        "deleted": deleted,
        "superseded": superseded,
        "round_changed": sorted(round_changed),
        "violations": len(ids) + len(deleted),
        "changed_back": changed_back,
    }


# --------------------------------------------------------------- sandbox making

KINDS = ["docs", "code", "spec", "community", "tool"]
TIERS = ["A", "B", "C"]
STATUSES = ["mined", "queued", "reviewed"]
RECHECKES = ["on-release", "90d", "180d"]
IMMUTABLE_EDIT_COLS = [1, 2, 3, 4, 5, 6, 8]   # all but id, status, recheck, used-by
MUTABLE_EDIT_COLS = [7, 9, 10]


def make_row(rng, rid, serial, teaches=None):
    used_by = ("corpus/knowledge/k%02d.md" % serial) if serial % 3 else "n/a"
    return [
        rid,
        "Note %d - https://example.invalid/docs/%d" % (serial, serial),
        rng.choice(KINDS),
        rng.choice(TIERS),
        "scope of note %d" % serial,
        "anchor %d" % serial,
        teaches if teaches is not None else "teaches note %d" % serial,
        rng.choice(STATUSES),
        "2026-10-19",
        rng.choice(RECHECKES),
        used_by,
    ]


SANDBOX_TITLE = "# SOURCES - sandbox registry"
LANE_TITLE = "# SOURCES \u2014 where mori learns"  # the lane's real title, verbatim (w1/RevC1Challenge)
LANE_IDENTITY = ("mori-shokunin", "mori@shokunin.local")


def render(rows, title=SANDBOX_TITLE):
    out = [
        title,
        "",
        "## Registry",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    for cells in rows:
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


class Sandbox:
    """One sandbox repo: its rows, its op log, and the hidden truth."""

    def __init__(self, root, index, rng, identity=None, title=SANDBOX_TITLE):
        self.index = index
        self.rng = rng
        self.identity = identity or ("mori counter", "counter@example.invalid")
        self.title = title
        self.path = os.path.join(root, "repo%02d" % index)
        self.rows = []
        self.states = []
        self.first = {}
        self.used_ids = set()
        self.serial = 0
        self.last_text = None
        self.pad = 0
        self.protected = set()
        self.imm_idx = immutable_indices({name: i for i, name in enumerate(COLUMNS)})

    # -- rows -----------------------------------------------------------------
    def new_id(self):
        while True:
            rid = "S%03d" % self.rng.randint(1, 299)
            if rid not in self.used_ids:
                self.used_ids.add(rid)
                return rid

    def new_row(self, teaches=None):
        self.serial += 1
        cells = make_row(self.rng, self.new_id(), self.serial, teaches)
        self.rows.append(cells)
        return cells

    def edited_rows(self):
        """Present rows whose immutable cells differ from their first-held cells."""
        out = []
        for cells in self.rows:
            first = self.first.get(cells[0].strip())
            if first is not None and imm_key(cells, self.imm_idx) != imm_key(first, self.imm_idx):
                out.append(cells)
        return out

    # -- ops ------------------------------------------------------------------
    def op_append(self):
        self.new_row()

    def op_edit_mutable(self):
        cells = self.rng.choice(self.rows)
        col = self.rng.choice(MUTABLE_EDIT_COLS)
        self.serial += 1
        cells[col] = "%s rev%d" % (cells[col].strip(), self.serial)

    def op_edit_immutable(self, target=None):
        if target is None:
            candidates = [cells for cells in self.rows
                          if cells[0].strip() not in self.protected]
            if not candidates:
                candidates = self.rows
            target = self.rng.choice(candidates)
        cells = target
        col = self.rng.choice(IMMUTABLE_EDIT_COLS)
        self.serial += 1
        cells[col] = "%s rev%d" % (cells[col].strip(), self.serial)

    def op_revert(self, target):
        """Restore the row's immutable cells to the cells it first held."""
        first = self.first.get(target[0].strip())
        if first is None:
            return
        for i in self.imm_idx:
            target[i] = first[i]

    def op_delete(self, target=None):
        cells = target if target is not None else self.rng.choice(self.rows)
        if cells is None or len(self.rows) <= 2:
            return
        self.rows.remove(cells)

    def op_supersede(self, target):
        cells = self.new_row(teaches="supersedes %s — replacement text" % target[0].strip())
        self.protected.add(cells[0].strip())

    def op_reorder(self):
        if len(self.rows) > 1:
            self.rng.shuffle(self.rows)

    def op_cosmetic(self):
        """Padding-only change: cells compare stripped, so no cell value changes."""
        cells = self.rng.choice(self.rows)
        col = self.rng.choice([1, 2, 3, 4, 5, 6, 8, 9, 10])
        self.pad += 1
        cells[col] = " " * self.pad + cells[col].strip()

    # -- commits --------------------------------------------------------------
    def commit(self):
        text = render(self.rows, self.title)
        if self.last_text is not None and text == self.last_text:
            self.op_cosmetic()
            text = render(self.rows, self.title)
        self.last_text = text
        self.states.append([list(cells) for cells in self.rows])
        with open(os.path.join(self.path, PATH), "w", encoding="utf-8") as handle:
            handle.write(text)
        git(self.path, "add", PATH)
        git(self.path, "commit", "-q", "-m", "c%d" % len(self.states))
        # first-held cells are the cells of the commit that first carried the row
        for cells in self.rows:
            self.first.setdefault(cells[0].strip(), list(cells))


def build_sandbox(root, index, rng, identity=None, title=SANDBOX_TITLE):
    """Create one sandbox repo; return (path, truth, base_sha, flags)."""
    sandbox = Sandbox(root, index, rng, identity=identity, title=title)
    os.makedirs(os.path.join(sandbox.path, "corpus"))
    git(sandbox.path, "init", "-q")
    git(sandbox.path, "config", "user.name", sandbox.identity[0])
    git(sandbox.path, "config", "user.email", sandbox.identity[1])
    git(sandbox.path, "config", "commit.gpgsign", "false")

    want_delete = (index % 2 == 0)
    want_changed_back = (index % 2 == 1)
    want_supersede = (index % 4 == 0)

    for _ in range(rng.randint(6, 12)):
        sandbox.new_row()
    sandbox.commit()

    op_commits = rng.randint(4, 8)
    revert_target = None
    supersede_target = None
    if want_changed_back:
        revert_target = sandbox.rows[0]
    if want_supersede:
        supersede_target = sandbox.rows[1]
    if revert_target is not None:
        sandbox.protected.add(revert_target[0].strip())
    if supersede_target is not None:
        sandbox.protected.add(supersede_target[0].strip())

    def victim_pool():
        return [cells for cells in sandbox.rows
                if cells[0].strip() not in sandbox.protected]

    # the forced delete and the forced revert land at random commits, so that in
    # some histories every change predates the round base (round_changed empty)
    delete_at = rng.randint(1, op_commits - 1) if want_delete else None
    revert_at = rng.randint(1, op_commits - 1) if want_changed_back else None

    for commit_index in range(op_commits):
        forced = []
        if commit_index == 0:
            if revert_target is not None:
                forced.append(("edit_immutable", revert_target))
            if supersede_target is not None:
                forced.append(("edit_immutable", supersede_target))
        if commit_index == 1 and supersede_target is not None:
            forced.append(("supersede", supersede_target))
        if commit_index == revert_at and revert_target is not None:
            forced.append(("revert", revert_target))
        if commit_index == delete_at:
            pool = victim_pool()
            forced.append(("delete", pool[0] if pool else None))

        pool = ["append", "edit_mutable", "edit_immutable", "reorder", "cosmetic"]
        if victim_pool():
            pool.append("delete")
        if sandbox.edited_rows():
            pool.append("revert")
            pool.append("supersede")
        wanted = rng.randint(1, 3)
        extra = list(forced)
        rng.shuffle(pool)
        for op in pool:
            if len(extra) >= wanted:
                break
            if any(op == kind for kind, _ in extra):
                continue
            extra.append((op, None))

        for op, target in extra:
            if op == "append":
                sandbox.op_append()
            elif op == "edit_mutable":
                sandbox.op_edit_mutable()
            elif op == "edit_immutable":
                sandbox.op_edit_immutable(target)
            elif op == "revert":
                if target is not None:
                    sandbox.op_revert(target)
                    continue
                candidates = [cells for cells in sandbox.edited_rows()
                              if cells[0].strip() not in sandbox.protected]
                if candidates:
                    sandbox.op_revert(candidates[0])
            elif op == "delete":
                if target is not None:
                    sandbox.op_delete(target)
                else:
                    pool = victim_pool()
                    if pool:
                        sandbox.op_delete(pool[0])
            elif op == "supersede":
                if target is not None:
                    sandbox.op_supersede(target)
                    continue
                candidates = [cells for cells in sandbox.edited_rows()
                              if cells[0].strip() not in sandbox.protected]
                if candidates:
                    sandbox.op_supersede(candidates[0])
            elif op == "reorder":
                sandbox.op_reorder()
            elif op == "cosmetic":
                sandbox.op_cosmetic()
        sandbox.commit()

    base_index = rng.randint(0, op_commits - 1)
    commits = git_out(sandbox.path, "log", "--format=%H", "--reverse").split()
    base_sha = commits[base_index]
    truth = truth_from_states(sandbox.states, base_index, {n: i for i, n in enumerate(COLUMNS)})
    flags = {"delete": want_delete, "changed_back": want_changed_back,
             "supersede": want_supersede}
    return sandbox.path, truth, base_sha, flags


# ------------------------------------------------------------------ tool running

def run_tool(tool, args, cwd="/"):
    cmd = ["timeout", str(TOOL_TIMEOUT_S), sys.executable, tool] + list(args)
    try:
        return run(cmd, cwd=cwd, timeout=TOOL_TIMEOUT_S + 60, env=clean_env())
    except ToolTimeout as exc:
        return subprocess.CompletedProcess(cmd, None, "", str(exc))


ID_CHANGED_RE = re.compile(r"^changed (S\d{3}) superseded_by=(S\d{3}|-)$")
ID_DELETED_RE = re.compile(r"^deleted (S\d{3})$")


def parse_id_lines(stdout):
    """The per-id lines the contract's C2 tool interface requires.

    Returns (changed, deleted, malformed) where changed/deleted are id lists in
    print order and malformed counts `changed`/`deleted`-looking lines that do not
    match the grammar."""
    changed, deleted, malformed = [], [], 0
    for raw in stdout.splitlines():
        line = raw.strip()
        m = ID_CHANGED_RE.match(line)
        if m:
            changed.append(m.group(1))
            continue
        m = ID_DELETED_RE.match(line)
        if m:
            deleted.append(m.group(1))
            continue
        if line.startswith("changed ") or line.startswith("deleted "):
            malformed += 1
    return changed, deleted, malformed


def same_id_lines(got, want):
    changed, deleted, malformed = got
    return (malformed == 0
            and sorted(changed) == sorted(want["ids"])
            and sorted(deleted) == sorted(want["deleted"])
            and len(changed) == len(set(changed))
            and len(deleted) == len(set(deleted)))


def parse_summary(stdout):
    matches = [line.strip() for line in stdout.splitlines() if SUMMARY_RE.match(line.strip())]
    if len(matches) != 1:
        return None
    groups = SUMMARY_RE.match(matches[0]).groups()

    def split_list(text):
        return [part for part in text.split(",") if part]

    return {
        "violations": int(groups[0]),
        "ids": split_list(groups[1]),
        "deleted": split_list(groups[2]),
        "superseded": split_list(groups[3]),
        "round_changed": split_list(groups[4]),
        "line": matches[0],
    }


def same_lists(got, want):
    return (got["violations"] == want["violations"]
            and got["ids"] == want["ids"]
            and got["deleted"] == want["deleted"]
            and got["superseded"] == want["superseded"]
            and got["round_changed"] == want["round_changed"])


# --------------------------------------------------------------------- real arm

def oracle(repo, rev, base):
    """Independent git walk over the path: the same four lists the tool must print."""
    commits = git_out(repo, "log", "--format=%H", "--reverse", rev, "--", PATH).split()
    states = []
    colmap = None
    for commit in commits:
        spec = "%s:%s" % (commit, PATH)
        if git(repo, "cat-file", "-e", spec, check=False).returncode != 0:
            rows = None          # the path is absent at this commit (rename/delete)
        else:
            rows, cm = parse_registry(git_out(repo, "show", spec))
            if cm is not None and colmap is None:
                colmap = cm
        states.append(rows)
    tip_rows, cm = parse_registry(git_out(repo, "show", "%s:%s" % (rev, PATH)))
    if cm is not None and colmap is None:
        colmap = cm
    imm_idx = immutable_indices(colmap)

    first = {}
    changed_at = {}
    deleted_at = {}
    last_seen = {}
    prev_ids = set()
    for index, rows in enumerate(states):
        if rows is None:
            continue            # path absent here: no rows, nothing to compare
        current = {cells[0].strip(): cells for cells in rows}
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

    tip = {cells[0].strip(): cells for cells in tip_rows}
    ids = sorted(cid for cid, cells in tip.items()
                 if imm_key(cells, imm_idx) != imm_key(first[cid], imm_idx))
    deleted = sorted(set(first) - set(tip))
    sup_map = superseders(tip_rows, colmap)
    superseded = sorted(cid for cid in ids if cid in sup_map)

    in_range = set(git_out(repo, "rev-list", "%s..%s" % (base, rev)).split())
    round_changed = set()
    for index, commit in enumerate(commits):
        if commit in in_range:
            round_changed |= changed_at.get(index, set()) | deleted_at.get(index, set())

    return {
        "ids": ids,
        "deleted": deleted,
        "superseded": superseded,
        "round_changed": sorted(round_changed),
        "violations": len(ids) + len(deleted),
    }


# ------------------------------------------------------------------------- arms

def draw_blind(root, rng, start=0, count=N_SANDBOX):
    """Build `count` sandbox histories (draw only, no tool run)."""
    draws = []
    for index in range(start, start + count):
        path, truth, base_sha, flags = build_sandbox(root, index, rng)
        draws.append({"index": index, "path": path, "truth": truth, "base_sha": base_sha})
    return draws


def check_blind(tool, draws):
    """Run one tool on pre-drawn sandboxes; compare summary and per-id lines."""
    results = []
    coverage = {"delete": 0, "changed_back": 0, "supersede": 0}
    for draw in draws:
        path, truth, base_sha = draw["path"], draw["truth"], draw["base_sha"]
        if truth["deleted"]:
            coverage["delete"] += 1
        if truth["changed_back"]:
            coverage["changed_back"] += 1
        if truth["superseded"]:
            coverage["supersede"] += 1
        proc = run_tool(tool, ["HEAD", "--repo", path, "--round-base", base_sha])
        got = parse_summary(proc.stdout)
        ids = parse_id_lines(proc.stdout)
        expected_exit = 1 if truth["round_changed"] else 0
        if proc.returncode is None:
            ok = False
            reason = "tool_timeout: %s" % proc.stderr.strip()
        elif got is None:
            tail = (proc.stdout + proc.stderr).strip().splitlines()
            ok = False
            reason = "no summary line (exit %d): %s" % (proc.returncode, tail[-1] if tail else "")
        elif not same_lists(got, truth):
            ok = False
            reason = ("lists differ\n      want: %s\n      got:  %s"
                      % (format_summary(truth), got["line"]))
        elif not same_id_lines(ids, truth):
            ok = False
            reason = ("per-id lines differ (malformed=%d)\n      want: changed=%s deleted=%s"
                      "\n      got:  changed=%s deleted=%s"
                      % (ids[2], truth["ids"], truth["deleted"], ids[0], ids[1]))
        elif proc.returncode != expected_exit:
            ok = False
            reason = "exit %d, expected %d (round_changed=%s)" % (
                proc.returncode, expected_exit, truth["round_changed"])
        else:
            ok = True
            reason = ""
        results.append({"index": draw["index"], "ok": ok, "reason": reason,
                        "truth": truth, "got": got, "exit": proc.returncode})
    return results, coverage


def blind_arm(tool, root, rng):
    return check_blind(tool, draw_blind(root, rng))


def real_arm(tool, repo, scratch):
    # v2 (round-36 C0: J11 met because the v1 real arm ran on a clone under
    # /fast/scratch, which a harness-keyed program could detect): the tool and the
    # oracle read the repository itself, read-only git only; no clone.
    clone = os.path.abspath(repo)
    proc = run_tool(tool, [REAL_REV, "--repo", clone, "--round-base", REAL_BASE])
    got = parse_summary(proc.stdout)
    ids = parse_id_lines(proc.stdout)
    expected = oracle(clone, REAL_REV, REAL_BASE)
    ok = (got is not None and same_lists(got, expected) and bool(expected["ids"])
          and same_id_lines(ids, expected))
    diffs = []
    if proc.returncode is None:
        diffs.append("tool_timeout: %s" % proc.stderr.strip())
    if got is None:
        diffs.append("no summary line (exit %s)" % proc.returncode)
    else:
        for key in ("ids", "deleted", "superseded", "round_changed"):
            if got[key] != expected[key]:
                diffs.append("%s: want=%s got=%s" % (key, expected[key], got[key]))
        if got["violations"] != expected["violations"]:
            diffs.append("violations: want=%d got=%d"
                         % (expected["violations"], got["violations"]))
    if not same_id_lines(ids, expected):
        diffs.append("per-id lines: want changed=%s deleted=%s got changed=%s deleted=%s "
                     "(malformed=%d)"
                     % (expected["ids"], expected["deleted"], ids[0], ids[1], ids[2]))
    return ok, got, expected, diffs, proc


def draw_real_rev(repo, rng, published_line, limit=40):
    """A run-time-drawn ancestor rev of the lane repo whose truth is not published.

    w1/RevC1Challenge (HIGH): the fixed real arm's answer is in the receipt, so a tool
    keyed on any constant property of that arm can print it. A drawn rev defeats every
    such key except the arm's own rev literal, which is part of the declared interface
    (disclosed residual)."""
    revs = git_out(repo, "rev-list", "--max-count=%d" % limit, "HEAD").split()
    candidates = []
    for rev in revs:
        if git(repo, "cat-file", "-e", "%s:%s" % (rev, TOOL_REL), check=False).returncode != 0:
            continue
        parent = git_out(repo, "rev-parse", "--verify", rev + "^").strip()
        if not parent:
            continue
        expected = oracle(repo, rev, parent)
        if format_summary(expected) == published_line:
            continue
        if not expected["ids"] and not expected["deleted"]:
            continue
        candidates.append((rev, parent, expected))
    if not candidates:
        raise RuntimeError("no drawable real rev")
    return rng.choice(candidates)


def real_draw_arm(tool, repo, rng, published_line):
    """Run the tool at a run-time-drawn rev; the expected answer is computed, never printed."""
    rev, base, expected = draw_real_rev(repo, rng, published_line)
    clone = os.path.abspath(repo)
    proc = run_tool(tool, [rev[:10], "--repo", clone, "--round-base", base[:10]])
    got = parse_summary(proc.stdout)
    ids = parse_id_lines(proc.stdout)
    ok = got is not None and same_lists(got, expected) and same_id_lines(ids, expected)
    reason = ""
    if proc.returncode is None:
        ok, reason = False, "tool_timeout"
    elif got is None:
        ok, reason = False, "no summary line (exit %s)" % proc.returncode
    elif not same_lists(got, expected):
        ok, reason = False, "lists differ: want %s got %s" % (
            format_summary(expected), got["line"])
    elif not same_id_lines(ids, expected):
        ok, reason = False, "per-id lines differ"
    return ok, rev, base, expected, got, reason


def challenge_arm(tool, rng):
    """One run-time-drawn history presented in real-arm clothing (RevNgC2 N1).

    The repo lives under the lane repo's own `.ufo/waves/round-37/scratch` (not under
    /fast/scratch or /tmp), carries the lane git identity and the lane SOURCES title,
    so a tool that classifies "sandbox vs real" by path, git identity or title is
    fooled; its truth comes from this counter's op log, so the published real-arm
    constant is not an answer to it."""
    os.makedirs(CHALLENGE_PARENT, exist_ok=True)
    root = tempfile.mkdtemp(prefix="challenge-", dir=CHALLENGE_PARENT)
    try:
        # even index => build_sandbox forces a deletion witness (want_delete)
        index = 900 + 2 * rng.randrange(50)
        path, truth, base_sha, flags = build_sandbox(
            root, index, rng, identity=LANE_IDENTITY, title=LANE_TITLE)
        if not truth["deleted"]:
            raise RuntimeError("challenge draw carried no deletion witness")
        proc = run_tool(tool, ["HEAD", "--repo", path, "--round-base", base_sha])
        got = parse_summary(proc.stdout)
        ids = parse_id_lines(proc.stdout)
        expected_exit = 1 if truth["round_changed"] else 0
        if proc.returncode is None:
            return False, got, truth, "tool_timeout: %s" % proc.stderr.strip()
        if got is None:
            return False, got, truth, "no summary line (exit %s)" % proc.returncode
        if not same_lists(got, truth):
            return False, got, truth, "lists differ: want %s got %s" % (
                format_summary(truth), got["line"])
        if not same_id_lines(ids, truth):
            return False, got, truth, ("per-id lines differ: want changed=%s deleted=%s "
                                       "got changed=%s deleted=%s"
                                       % (truth["ids"], truth["deleted"], ids[0], ids[1]))
        if proc.returncode != expected_exit:
            return False, got, truth, "exit %s, expected %d" % (
                proc.returncode, expected_exit)
        return True, got, truth, ""
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run_negative(tool, draws, repo, rng):
    """Judge one fixture tool. Rejected when any of the three arms fails."""
    blind, _ = check_blind(tool, draws)
    blind_fail = [r for r in blind if not r["ok"]]
    real_ok, _, _, _, _ = real_arm(tool, repo, None)
    challenge_ok, _, _, challenge_reason = challenge_arm(tool, rng)
    if blind_fail:
        detail = "blind %d/%d (repo%02d: %s)" % (
            len(blind_fail), len(blind), blind_fail[0]["index"],
            blind_fail[0]["reason"].splitlines()[0])
    elif not real_ok:
        detail = "real arm fails"
    elif not challenge_ok:
        detail = "challenge: %s" % challenge_reason
    else:
        detail = "all three arms pass"
    return (bool(blind_fail) or (not real_ok) or (not challenge_ok)), detail


# ------------------------------------------------------------------------- main

def _scratch_parent():
    """A writable scratch parent. Each arm then uses mkdtemp: unique per run, so a
    replay of the same seed never collides with a concurrent seat (r36 ExecReC2B §5)."""
    for candidate in (SCRATCH_ROOT, os.environ.get("TMPDIR") or "", "/tmp"):
        if not candidate:
            continue
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = tempfile.mkdtemp(prefix=".probe-", dir=candidate)
            os.rmdir(probe)
            return candidate
        except OSError:
            continue
    raise RuntimeError("no writable scratch parent (tried %s)" % SCRATCH_ROOT)


def display_path(path, repo):
    """Repo-relative for lane paths (r36 SentData: evidence carries no absolute
    operator path), absolute only for a path outside the repository."""
    absolute = os.path.abspath(path)
    base = os.path.abspath(repo)
    if absolute == base or absolute.startswith(base + os.sep):
        return os.path.relpath(absolute, base)
    return absolute


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("rev")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--tool", default=None)
    parser.add_argument("--negatives", default=NEGATIVES_DIR)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args(argv)

    print(PREDICATE)
    seed = args.seed if args.seed is not None else int.from_bytes(os.urandom(8), "big")
    rng = random.Random(seed)

    try:
        full = git_out(args.repo, "rev-parse", "--verify", args.rev + "^{commit}").strip()
    except Exception as exc:
        print("counter setup error: %s" % exc, file=sys.stderr)
        return 2
    if not full:
        print("counter setup error: cannot resolve %s in %s" % (args.rev, args.repo),
              file=sys.stderr)
        return 2

    fixtures = []
    for name in ("memo-n1.py", "const.py", "summary-only.py"):
        path = os.path.join(args.negatives, name)
        if not os.path.isfile(path):
            print("counter setup error: missing negative fixture %s" % path, file=sys.stderr)
            return 2
        fixtures.append((name, path))

    tool_dir = tempfile.mkdtemp(prefix="mori-c1-tool-")
    try:
        if args.tool:
            tool = args.tool
            if not os.path.isfile(tool):
                print("counter setup error: no such tool file: %s" % tool, file=sys.stderr)
                return 2
        else:
            proc = git(args.repo, "show", "%s:%s" % (full, TOOL_REL), check=False)
            if proc.returncode != 0:
                print("tool_absent")
                print("C1=unmet")
                print("seed=%d" % seed)
                return 1
            tool = os.path.join(tool_dir, "mori-sources-appendonly.py")
            with open(tool, "w", encoding="utf-8") as handle:
                handle.write(proc.stdout)
        print("tool: %s" % display_path(tool, args.repo))

        parent = _scratch_parent()
        scratch = tempfile.mkdtemp(prefix="c1-", dir=parent)
        try:
            start = time.time()
            results, coverage = blind_arm(tool, scratch, rng)
            blind_seconds = time.time() - start
            passed = sum(1 for r in results if r["ok"])
            print("blind arm: %d/%d sandbox histories matched the hidden truth (%.1fs; "
                  "coverage: deletions=%d changed-back=%d superseded=%d)"
                  % (passed, N_SANDBOX, blind_seconds, coverage["delete"],
                     coverage["changed_back"], coverage["supersede"]))
            for r in results:
                if not r["ok"]:
                    print("  repo%02d FAIL: %s" % (r["index"], r["reason"]))
            if coverage["delete"] < 12 or coverage["changed_back"] < 12 or coverage["supersede"] < 1:
                print("counter setup error: blind coverage below the frozen minimum "
                      "(%s)" % coverage, file=sys.stderr)
                return 2

            start = time.time()
            real_ok, got, expected, diffs, proc = real_arm(tool, args.repo, scratch)
            real_seconds = time.time() - start
            print("real arm: %s (%.1fs)" % ("pass" if real_ok else "FAIL", real_seconds))
            print("  tool:   %s" % (got["line"] if got else "(no summary line)"))
            print("  oracle: %s" % format_summary(expected))
            for diff in diffs:
                print("  diff: %s" % diff)
            print("  tool exit=%s" % proc.returncode)

            start = time.time()
            published_line = format_summary(expected)
            draw_ok, draw_rev, draw_base, draw_expected, draw_got, draw_reason = \
                real_draw_arm(tool, args.repo, rng, published_line)
            draw_seconds = time.time() - start
            print("drawn arm: %s (%.1fs) rev=%s base=%s"
                  % ("pass" if draw_ok else "FAIL", draw_seconds, draw_rev[:10], draw_base[:10]))
            print("  truth:  %s" % format_summary(draw_expected))
            print("  tool:   %s" % (draw_got["line"] if draw_got else "(no summary line)"))
            if not draw_ok:
                print("  reason: %s" % draw_reason)

            start = time.time()
            challenge_ok, chall_got, chall_truth, chall_reason = challenge_arm(tool, rng)
            challenge_seconds = time.time() - start
            print("challenge arm (real-arm clothing): %s (%.1fs)"
                  % ("pass" if challenge_ok else "FAIL", challenge_seconds))
            print("  truth:  %s" % format_summary(chall_truth))
            print("  tool:   %s" % (chall_got["line"] if chall_got else "(no summary line)"))
            if not challenge_ok:
                print("  reason: %s" % chall_reason)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)

        neg_root = tempfile.mkdtemp(prefix="c1-neg-", dir=parent)
        rejected = []
        try:
            neg_rng = random.Random(rng.getrandbits(64))
            neg_draws = draw_blind(neg_root, neg_rng, start=200, count=NEG_BLIND)
            for i, (name, path) in enumerate(fixtures):
                ok_rejected, detail = run_negative(
                    path, neg_draws, args.repo,
                    random.Random((seed * 1000003) ^ (i + 7)))
                print("negative %-14s %s (%s)"
                      % (name, "rejected" if ok_rejected else "ACCEPTED", detail))
                rejected.append(ok_rejected)
        finally:
            shutil.rmtree(neg_root, ignore_errors=True)
    finally:
        shutil.rmtree(tool_dir, ignore_errors=True)

    met = (passed == N_SANDBOX and real_ok and draw_ok and challenge_ok and all(rejected))
    print("C1=%s" % ("met" if met else "unmet"))
    print("seed=%d" % seed)
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # counter setup error
        print("counter setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
