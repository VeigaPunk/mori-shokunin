#!/usr/bin/env python3
"""Round-36 C2 counter: does tools/mori-sources-appendonly.py print the truth?

Usage:
    count-c2.py <rev> [--repo DIR] [--tool FILE] [--seed N]

<rev> is the revision that must carry tools/mori-sources-appendonly.py.
Without --tool the tool is taken from `git show <rev>:tools/mori-sources-appendonly.py`
(written to a temp file); with --tool FILE that file is used instead (controls).
--seed makes the blind arm replayable; a scored run draws its seed from os.urandom.

Arms:
  blind  24 sandbox git histories drawn at run time. The hidden truth comes from the
         counter's own op log (row dicts per commit), never from git and never from a
         file the tool can read.
  real   the lane's own history (rev 6bd57097, round base f10a320d) against the
         counter's independent git walk.

Exit: 0 met, 1 unmet, 2 counter setup error.
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
    "P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's "
    "hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox "
    "SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, "
    "round base f10a320d) it prints exactly the counter's independent oracle, which lists "
    "at least one id."
)

DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"
TOOL_REL = "tools/mori-sources-appendonly.py"
SCRATCH_ROOT = "/fast/scratch/hyaku/mori-r36"

REAL_REV = "6bd57097"
REAL_BASE = "f10a320d"
N_SANDBOX = 24

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


def run(cmd, cwd=None, timeout=120, env=None):
    """Run a command in its own process group; kill the whole tree on timeout."""
    proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass
        out, err = proc.communicate()
        raise
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


def render(rows):
    out = [
        "# SOURCES - sandbox registry",
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

    def __init__(self, root, index, rng):
        self.index = index
        self.rng = rng
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
        text = render(self.rows)
        if self.last_text is not None and text == self.last_text:
            self.op_cosmetic()
            text = render(self.rows)
        self.last_text = text
        self.states.append([list(cells) for cells in self.rows])
        with open(os.path.join(self.path, PATH), "w", encoding="utf-8") as handle:
            handle.write(text)
        git(self.path, "add", PATH)
        git(self.path, "commit", "-q", "-m", "c%d" % len(self.states))
        # first-held cells are the cells of the commit that first carried the row
        for cells in self.rows:
            self.first.setdefault(cells[0].strip(), list(cells))


def build_sandbox(root, index, rng):
    """Create one sandbox repo; return (path, truth, base_sha, flags)."""
    sandbox = Sandbox(root, index, rng)
    os.makedirs(os.path.join(sandbox.path, "corpus"))
    git(sandbox.path, "init", "-q")
    git(sandbox.path, "config", "user.name", "mori counter")
    git(sandbox.path, "config", "user.email", "counter@example.invalid")
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
    cmd = ["timeout", "120", sys.executable, tool] + list(args)
    return run(cmd, cwd=cwd, timeout=180, env=clean_env())


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

def blind_arm(tool, root, rng):
    results = []
    coverage = {"delete": 0, "changed_back": 0, "supersede": 0}
    for index in range(N_SANDBOX):
        path, truth, base_sha, flags = build_sandbox(root, index, rng)
        if truth["deleted"]:
            coverage["delete"] += 1
        if truth["changed_back"]:
            coverage["changed_back"] += 1
        if truth["superseded"]:
            coverage["supersede"] += 1
        proc = run_tool(tool, ["HEAD", "--repo", path, "--round-base", base_sha])
        got = parse_summary(proc.stdout)
        expected_exit = 1 if truth["round_changed"] else 0
        if got is None:
            tail = (proc.stdout + proc.stderr).strip().splitlines()
            ok = False
            reason = "no summary line (exit %d): %s" % (proc.returncode, tail[-1] if tail else "")
        elif not same_lists(got, truth):
            ok = False
            reason = ("lists differ\n      want: %s\n      got:  %s"
                      % (format_summary(truth), got["line"]))
        elif proc.returncode != expected_exit:
            ok = False
            reason = "exit %d, expected %d (round_changed=%s)" % (
                proc.returncode, expected_exit, truth["round_changed"])
        else:
            ok = True
            reason = ""
        results.append({"index": index, "ok": ok, "reason": reason, "truth": truth,
                        "got": got, "exit": proc.returncode})
    return results, coverage


def real_arm(tool, repo, scratch):
    # v2 (round-36 C0: J11 met because the v1 real arm ran on a clone under
    # /fast/scratch, which a harness-keyed program could detect): the tool and the
    # oracle read the repository itself, read-only git only; no clone.
    clone = os.path.abspath(repo)
    proc = run_tool(tool, [REAL_REV, "--repo", clone, "--round-base", REAL_BASE])
    got = parse_summary(proc.stdout)
    expected = oracle(clone, REAL_REV, REAL_BASE)
    ok = got is not None and same_lists(got, expected) and bool(expected["ids"])
    diffs = []
    if got is None:
        diffs.append("no summary line (exit %d)" % proc.returncode)
    else:
        for key in ("ids", "deleted", "superseded", "round_changed"):
            if got[key] != expected[key]:
                diffs.append("%s: want=%s got=%s" % (key, expected[key], got[key]))
        if got["violations"] != expected["violations"]:
            diffs.append("violations: want=%d got=%d"
                         % (expected["violations"], got["violations"]))
    return ok, got, expected, diffs, proc


# ------------------------------------------------------------------------- main

def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("rev")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--tool", default=None)
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

    tool_dir = tempfile.mkdtemp(prefix="mori-c2-")
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
                print("C2=unmet")
                print("seed=%d" % seed)
                return 1
            tool = os.path.join(tool_dir, "mori-sources-appendonly.py")
            with open(tool, "w", encoding="utf-8") as handle:
                handle.write(proc.stdout)
        print("tool: %s" % tool)

        scratch = os.path.join(SCRATCH_ROOT, "c2-%08x" % rng.randrange(1 << 32))
        os.makedirs(scratch, exist_ok=True)
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
            print("  tool exit=%d" % proc.returncode)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    finally:
        shutil.rmtree(tool_dir, ignore_errors=True)

    met = passed == N_SANDBOX and real_ok
    print("C2=%s" % ("met" if met else "unmet"))
    print("seed=%d" % seed)
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # counter setup error
        print("counter setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
