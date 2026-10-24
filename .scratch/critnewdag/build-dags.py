#!/usr/bin/env python3
"""CritNewDag probe: candidate fixture DAGs attacking P-C11 (gate v3).

Builds each fixture repo under .scratch/critnewdag/repos/, then runs the
landed v3 gate and the extracted v2 gate on each via real subprocesses.

Fixtures:
  dag-h   merge whose first parent permutes the registry HEADER (columns
          1<->6): no row cell changes, but the gate's single colmap/imm_idx/
          teaches_idx (fixed at the first walked commit) misreads the
          permuted commits -> fabricated `changed` events and a stale
          supersede verdict where P-C11's words predict as_of.
  dag-o   octopus merge with two side supersede rows (tasked candidate).
  dag-rm  linear delete-then-re-add of a superseded row with MODIFIED
          immutable cells (tasked candidate).
  dag-wr  --no-ff merge whose first parent is the walk root; merge tree
          differs from both parents (tasked candidate).
  dag-t   probe: merge resolved TREESAME to its second parent — does
          `git log --full-history` list the merge at all?
"""
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
GATE_V3 = os.path.join(LANE, "tools", "mori-sources-appendonly.py")
GATE_V2 = os.path.join(
    LANE, ".ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py")
ROOT = os.path.join(LANE, ".scratch", "critnewdag", "repos")

spec = importlib.util.spec_from_file_location("gate", GATE_V3)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

_row = gate._row
_render = gate._render
COL = gate.COLUMNS


def render_permuted(rows, swap=(1, 6)):
    """_render() with the header's columns `swap`ped, rows to match."""
    cols = list(COL)
    i, j = swap
    cols[i], cols[j] = cols[j], cols[i]
    out = ["# SOURCES — selftest registry", "", "## Registry", "",
           "| " + " | ".join(cols) + " |",
           "|" + "|".join(["---"] * len(cols)) + "|"]
    for cells in rows:
        perm = list(cells)
        perm[i], perm[j] = perm[j], perm[i]
        out.append("| " + " | ".join(perm) + " |")
    return "\n".join(out) + "\n"


def commit(path, body, msg, when, env, path_file="corpus/SOURCES.md"):
    os.makedirs(os.path.dirname(os.path.join(path, path_file)),
                exist_ok=True)
    with open(os.path.join(path, path_file), "w", encoding="utf-8") as fh:
        fh.write(body)
    gate._git_in(path, "add", path_file, env=env)
    dated = dict(env, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    gate._git_in(path, "commit", "-q", "--allow-empty", "-m", msg, env=dated)
    return gate._git_in(path, "rev-parse", "HEAD", env=env).strip()


def merge_resolve(path, sides, body, msg, when, env,
                  path_file="corpus/SOURCES.md"):
    """Merge `sides` (list) resolving the registry to `body` by hand."""
    dated = dict(env, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
    proc = subprocess.run(["git", "-C", path, "merge", "--no-edit",
                           "--no-ff", "-m", msg] + list(sides),
                          capture_output=True, text=True, timeout=120,
                          env=dated)
    target = os.path.join(path, path_file)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(body)
    gate._git_in(path, "add", path_file, env=env)
    gate._git_in(path, "commit", "-q", "-m", msg, "--no-edit", env=dated)
    return gate._git_in(path, "rev-parse", "HEAD", env=env).strip()


def init(path, env):
    gate._dag_init(path, env)


def build_dag_h(path, env):
    """Merge: first parent permutes the header; supersede row landed at b0."""
    init(path, env)
    s001 = _row("S001")
    s008 = _row("S008", source="https://example.invalid/e", anchor="anchor e",
                teaches="teaches e")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s003 = _row("S003", source="https://example.invalid/c", anchor="anchor c",
                teaches="teaches c")
    b0 = commit(path, _render([s001, s008, s002]), "b0",
                "2026-01-01T00:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "side", b0, env=env)
    s1 = commit(path, _render([s001, s008, s002, s003]), "s1",
                "2026-01-01T01:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    # h1: SAME rows, permuted header (columns 1 <-> 6: source <-> teaches)
    h1 = commit(path, render_permuted([s001, s008, s002]), "h1",
                "2026-01-01T02:00:00Z", env)
    m = merge_resolve(path, ["side"],
                      render_permuted([s001, s008, s002, s003]), "m",
                      "2026-01-01T03:00:00Z", env)
    return {"b0": b0, "s1": s1, "h1": h1, "m": m}


def build_dag_o(path, env):
    """True octopus (3 parents): e1 edits S001 on main; sidea lands the
    S001 supersede row; sideb lands an S004 supersede row — all three tips
    incomparable so git cannot reduce the merge."""
    init(path, env)
    s001 = _row("S001")
    s004 = _row("S004", source="https://example.invalid/d", anchor="anchor d",
                teaches="teaches d")
    s001v2 = _row("S001", anchor="anchor a v2")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s003 = _row("S003", source="https://example.invalid/c", anchor="anchor c",
                teaches="supersedes S004 — replacement")
    b0 = commit(path, _render([s001, s004]), "b0",
                "2026-01-01T00:00:00Z", env)
    e1 = commit(path, _render([s001v2, s004]), "e1",
                "2026-01-01T01:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "sidea", b0, env=env)
    a1 = commit(path, _render([s001, s004, s002]), "a1",
                "2026-01-01T02:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "sideb", b0, env=env)
    b1 = commit(path, _render([s001, s004, s003]), "b1",
                "2026-01-01T03:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    m = merge_resolve(path, ["sidea", "sideb"],
                      _render([s001v2, s004, s002, s003]), "m",
                      "2026-01-01T04:00:00Z", env)
    return {"b0": b0, "e1": e1, "a1": a1, "b1": b1, "m": m}


def build_dag_z2(path, env):
    """Dead branch lands the ONLY 'supersedes S001' row AND edits S001
    there; the merge discards all of it.  v3 reports S001 superseded and
    STALE — a verdict sourced entirely from content absent at R."""
    init(path, env)
    s001 = _row("S001")
    s001v2 = _row("S001", anchor="anchor a v2")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s005 = _row("S005", source="https://example.invalid/g", anchor="anchor g",
                teaches="teaches g")
    b0 = commit(path, _render([s001]), "b0", "2026-01-01T00:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "side", b0, env=env)
    s1 = commit(path, _render([s001v2, s002]), "s1",
                "2026-01-01T01:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    c1 = commit(path, _render([s001, s005]), "c1",
                "2026-01-01T02:00:00Z", env)
    m = merge_resolve(path, ["side"], _render([s001, s005]), "m",
                      "2026-01-01T03:00:00Z", env)
    return {"b0": b0, "s1": s1, "c1": c1, "m": m}

def build_dag_h2(path, env):
    """Permute the header FIRST, then land the supersede row permuted:
    the gate's fixed teaches_idx reads the wrong cell at s2, so the
    supersede pair is never recorded and the eligible set at R misses
    S001 even though the tip file's own text supersedes it."""
    init(path, env)
    s001 = _row("S001")
    s008 = _row("S008", source="https://example.invalid/e", anchor="anchor e",
                teaches="teaches e")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    b0 = commit(path, _render([s001, s008]), "b0",
                "2026-01-01T00:00:00Z", env)
    h1 = commit(path, render_permuted([s001, s008]), "h1",
                "2026-01-01T01:00:00Z", env)
    s2 = commit(path, render_permuted([s001, s008, s002]), "s2",
                "2026-01-01T02:00:00Z", env)
    return {"b0": b0, "h1": h1, "s2": s2}


def build_dag_z(path, env):
    """The only 'supersedes S001' row lives on a side branch whose content
    the merge discards entirely.  At R no row supersedes S001, yet the
    walked dead branch feeds sup_map: v3 lists S001 on the timing line."""
    init(path, env)
    s001 = _row("S001")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s005 = _row("S005", source="https://example.invalid/g", anchor="anchor g",
                teaches="teaches g")
    b0 = commit(path, _render([s001]), "b0", "2026-01-01T00:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "side", b0, env=env)
    s1 = commit(path, _render([s001, s002]), "s1",
                "2026-01-01T01:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    c1 = commit(path, _render([s001, s005]), "c1",
                "2026-01-01T02:00:00Z", env)
    # merge keeps MAIN content (plus S005): side's supersede row discarded
    m = merge_resolve(path, ["side"], _render([s001, s005]), "m",
                      "2026-01-01T03:00:00Z", env)
    return {"b0": b0, "s1": s1, "c1": c1, "m": m}


def build_dag_2l(path, env, side_date):
    """Two rows independently supersede S001 on incomparable branches:
    S002 lands on a side branch (incomparable with S001's edit, so
    is_ancestor fails) while S003 lands on main AFTER the edit
    (is_ancestor holds).  supersede_landing keeps the LATEST
    first-appearance walk index = commit-date order; identical DAG and
    contents with a different side commit date flips the verdict."""
    init(path, env)
    s001 = _row("S001")
    s001v2 = _row("S001", anchor="anchor a v2")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s003 = _row("S003", source="https://example.invalid/c", anchor="anchor c",
                teaches="supersedes S001 — replacement")
    b0 = commit(path, _render([s001]), "b0", "2026-01-01T00:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "side", b0, env=env)
    s1 = commit(path, _render([s001, s002]), "s1", side_date, env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    c1 = commit(path, _render([s001v2]), "c1", "2026-01-01T02:00:00Z", env)
    c2 = commit(path, _render([s001v2, s003]), "c2",
                "2026-01-01T03:00:00Z", env)
    m = merge_resolve(path, ["side"], _render([s001v2, s002, s003]), "m",
                      "2026-01-01T04:00:00Z", env)
    return {"b0": b0, "s1": s1, "c1": c1, "c2": c2, "m": m}


def build_dag_2l_early(path, env):
    # side supersede dated before the main-chain landings:
    # walk index s1 < c2 -> latest landing = c2 (descends from c1) -> as_of
    return build_dag_2l(path, env, "2026-01-01T01:00:00Z")


def build_dag_2l_late(path, env):
    # identical DAG/contents, side commit dated after c2:
    # walk index s1 > c2 -> latest landing = s1 (incomparable) -> stale
    return build_dag_2l(path, env, "2026-01-01T03:30:00Z")
def build_dag_x(path, env):
    """Superseding row deleted-then-re-added around an intervening edit:
    supersede_landing's latest-first-appearance index moves the landing
    from s1 to r2, flipping the ancestry test stale -> as_of."""
    init(path, env)
    s001 = _row("S001")
    s001v2 = _row("S001", anchor="anchor a v2")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    b0 = commit(path, _render([s001]), "b0", "2026-01-01T00:00:00Z", env)
    s1 = commit(path, _render([s001, s002]), "s1",
                "2026-01-01T01:00:00Z", env)
    d1 = commit(path, _render([s001]), "d1",
                "2026-01-01T02:00:00Z", env)
    e1 = commit(path, _render([s001v2]), "e1",
                "2026-01-01T03:00:00Z", env)
    r2 = commit(path, _render([s001v2, s002]), "r2",
                "2026-01-01T04:00:00Z", env)
    return {"b0": b0, "s1": s1, "d1": d1, "e1": e1, "r2": r2}


def build_dag_rm(path, env):
    """Linear delete-then-re-add of superseded S008 with MODIFIED cells."""
    init(path, env)
    s001 = _row("S001")
    s008 = _row("S008", source="https://example.invalid/e", anchor="anchor e",
                teaches="teaches e")
    s008m = _row("S008", source="https://example.invalid/e-EDITED",
                 anchor="anchor e EDITED", teaches="teaches e EDITED")
    s009 = _row("S009", source="https://example.invalid/f", anchor="anchor f",
                teaches="supersedes S008 — replacement")
    b0 = commit(path, _render([s001, s008]), "b0",
                "2026-01-01T00:00:00Z", env)
    s1 = commit(path, _render([s001, s008, s009]), "s1",
                "2026-01-01T01:00:00Z", env)
    r1 = commit(path, _render([s001, s009]), "r1",
                "2026-01-01T02:00:00Z", env)
    r2 = commit(path, _render([s001, s009, s008m]), "r2",
                "2026-01-01T03:00:00Z", env)
    return {"b0": b0, "s1": s1, "r1": r1, "r2": r2}


def build_dag_wr(path, env):
    """--no-ff merge whose first parent is the walk root; m differs from
    both parents (adds S003), carries the side's edit + supersede row."""
    init(path, env)
    s001 = _row("S001")
    s001v2 = _row("S001", anchor="anchor a v2")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s003 = _row("S003", source="https://example.invalid/c", anchor="anchor c",
                teaches="teaches c")
    b0 = commit(path, _render([s001]), "b0", "2026-01-01T00:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "side", b0, env=env)
    s1 = commit(path, _render([s001v2, s002]), "s1",
                "2026-01-01T01:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    m = merge_resolve(path, ["side"], _render([s001v2, s002, s003]), "m",
                      "2026-01-01T02:00:00Z", env)
    return {"b0": b0, "s1": s1, "m": m}


def build_dag_t(path, env):
    """Merge resolved TREESAME to second parent: is the merge walked?"""
    init(path, env)
    s001 = _row("S001")
    s001v2 = _row("S001", anchor="anchor a v2")
    s002 = _row("S002", source="https://example.invalid/b", anchor="anchor b",
                teaches="supersedes S001 — replacement")
    s005 = _row("S005", source="https://example.invalid/g", anchor="anchor g",
                teaches="teaches g")
    b0 = commit(path, _render([s001]), "b0", "2026-01-01T00:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "-b", "side", b0, env=env)
    s1 = commit(path, _render([s001v2, s002]), "s1",
                "2026-01-01T01:00:00Z", env)
    gate._git_in(path, "checkout", "-q", "main", env=env)
    c1 = commit(path, _render([s001, s005]), "c1",
                "2026-01-01T02:00:00Z", env)
    # merge resolving ENTIRELY to side's content: discards c1's S005
    m = merge_resolve(path, ["side"], _render([s001v2, s002]), "m",
                      "2026-01-01T03:00:00Z", env)
    return {"b0": b0, "s1": s1, "c1": c1, "m": m}


def run_gate(gate_script, repo, rev, base, env):
    proc = subprocess.run(
        [sys.executable, gate_script, rev, "--repo", repo,
         "--round-base", base],
        capture_output=True, text=True, timeout=180, env=env)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    env = gate._selftest_env()
    os.makedirs(ROOT, exist_ok=True)
    cases = [
        ("dag-h", build_dag_h, "m", "b0"),
        ("dag-o", build_dag_o, "m", "b0"),
        ("dag-rm", build_dag_rm, "r2", "b0"),
        ("dag-wr", build_dag_wr, "m", "b0"),
        ("dag-t", build_dag_t, "m", "b0"),
        ("dag-h2", build_dag_h2, "s2", "b0"),
        ("dag-z", build_dag_z, "m", "b0"),
        ("dag-z2", build_dag_z2, "m", "b0"),
        ("dag-x", build_dag_x, "r2", "b0"),
        ("dag-2l-early", build_dag_2l_early, "m", "b0"),
        ("dag-2l-late", build_dag_2l_late, "m", "b0"),
    ]
    for name, builder, tip_name, base_name in cases:
        repo = os.path.join(ROOT, name)
        if os.path.exists(repo):
            import shutil
            shutil.rmtree(repo)
        try:
            shas = builder(repo, env)
        except Exception as exc:  # noqa: BLE001
            print("## %s BUILD FAILED: %r" % (name, exc))
            continue
        print("## %s shas=%s" % (name,
              {k: v[:10] for k, v in shas.items()}))
        # show what the walk sees
        walk = subprocess.run(
            ["git", "-C", repo, "log", "--format=%H %P", "--reverse",
             "--full-history", shas[tip_name], "--",
             "corpus/SOURCES.md"],
            capture_output=True, text=True, env=env).stdout
        print("walk:\n" + walk.rstrip())
        for tag, script in (("v3", GATE_V3), ("v2", GATE_V2)):
            code, out, err = run_gate(script, repo, shas[tip_name],
                                      shas[base_name], env)
            print("-- %s gate=%s exit=%d" % (name, tag, code))
            for line in out.splitlines():
                if line.startswith("P-C"):
                    continue
                print("   " + line)
            if err.strip():
                print("   STDERR: " + err.strip()[:400])
        print()


if __name__ == "__main__":
    main()
