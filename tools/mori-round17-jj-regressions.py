#!/usr/bin/env python3
"""mori round-17 C2 gate: jj-colocation correctness of tools/mori-census.sh.

Contract (round-17 contract.md, C2, plus the CensusJj fail-closed amendment):
  * the census resolves the lane branch from the helper mirror
    `git config lane.branch` (scripts/hyaku/jj-lane.sh init writes it) before
    any guess, and queries refs/heads/<branch> instead of HEAD for report
    closure (row 6) and authorship (row 9);
  * a jj-colocated lane (`.jj` present) REQUIRES a valid, existing mirror:
    missing/invalid/missing-ref grades the lane `unavailable` row-1, with no
    HEAD fallback and no C2 finding (intentional fail-closed);
  * a non-jj lane resolves like detect_branch (symbolic-ref HEAD ->
    refs/remotes/origin/HEAD -> the unique of refs/heads/master /
    refs/heads/main), and an unresolved non-jj lane keeps the entering HEAD
    fallback unchanged;
  * HEAD_BRANCH_MISMATCH (severity warn, global drift) when HEAD resolves and
    `merge-base --is-ancestor HEAD refs/heads/<branch>` fails; the receipt is
    the census's exact `head=`/`branch_tip=` 12-hex-character fields (NOT
    `rev-parse --short`), plus `basis=merge-base-not-ancestor`;
  * LANE_AUTHOR_MISMATCH (severity warn, global drift) for a post-launch commit
    on the branch whose committer is <lane>-shokunin <lane>@shokunin.local while
    the author email does NOT end in @shokunin.local (the A1 amendment: a
    sibling-shokunin author such as kengaku@shokunin.local is legitimate and is
    a required negative control); the receipt is `count=` plus
    `basis=committer-lane-author-foreign-email`;
  * both diagnostics are observations about the branch anchor and are emitted
    BEFORE the row/young/report-closed early returns (CensusNewBranches): a
    young lane still reports LANE_AUTHOR_MISMATCH, and a jj fleet root with an
    unusable mirror skips row-6 closure instead of falling back to HEAD.

The gate builds one throw-away fleet root per case under --scratch:
  <root>/shokunin.conf            LANES row for exactly one lane (`alpha`)
  <root>/.ufo/state/alpha.round   round counter (1, equal to the ledger anchor)
  <root>/.ufo/watchdog.log        launch ledger for `alpha` (age > 7200 s)
  <root>/.ufo/reports/round-1/    report path root for the closure cases
  <root>/alpha-shokunin/          a real child lane repo (plain git or jj)

Every repo is created with real `git`; jj cases run the real
`~/.local/bin/jj git init --colocate <abs sandbox path>` with HOME,
XDG_CONFIG_HOME, JJ_CONFIG, GIT_CONFIG_GLOBAL (and GIT_CONFIG_SYSTEM) pointed
inside the case sandbox, so nothing is written to the operator's ~/.config/jj or
to the lane checkout. Because this gate's scratch may itself live under a
jj-colocated lane, the sandbox guard is enforced on every call:
  * every non-init jj call is `jj -R <sandbox> ...` after asserting
    `<sandbox>/.jj` exists (init is the one `--colocate <abs path>` exception);
  * every git call is `git -C <sandbox> ...` with GIT_CEILING_DIRECTORIES at the
    case sandbox and GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset;
  * no remote is created (the sandboxes have none, so the resolver's
    origin/HEAD arm is exercised only as an absent input).
The gate never invokes jj or git against the lane or the fleet root; all
sandbox fleet roots live under --scratch (default: <output>/scratch).

Write-root guards (falsify SandboxFinal F2 + residual): the RAW `--output`/
`--scratch` argument and every existing ancestor are checked for symlinks
BEFORE resolve()/mkdir (resolve() follows the link and would erase the
evidence), and `..` components are refused; only then is the canonical path
checked. `--output` must be absent or an empty non-symlink directory, and
neither path may be the repo root, an ancestor of it, or inside a protected
`tools/`, `corpus/`, `.git/`, `.jj/`, `.ufo/` (except `.ufo/waves/` evidence),
the census input, the gate source, the output artifacts, `/tmp`, or
`/var/tmp`. A fresh gate-owned `run-<stamp>-<pid>-<n>` child is created under
scratch. Retention (F4): that run tree is removed unless `--keep-scratch` is
given. Cleanup runs after the run body (including every caught error) and
BEFORE the manifest is written, so `retained`/`retention.cleanup` are
accurate; a BaseException escape (Ctrl-C) is the only path that can leave the
tree.

Hermeticity: the census is run with its own override environment, so no live
journal, systemd, tmux, cgroup, pgrep, df or boot-id query happens. Every
override below is read from the census header (tools/mori-census.sh:202-241)
and pinned to a sandbox path or stub:

  MORI_SHOKUNIN_ROOT, MORI_UFO_DIR, MORI_WATCHDOG_LOG, MORI_TIMELINE_FILE,
  MORI_STATE_DIR, MORI_WAVES_DIR, MORI_FLEET_CONF, MORI_ROSTER_LANES,
  MORI_CGROUP_EVENTS/CURRENT/PRESSURE/MAX/PEAK/LOCAL_EVENTS/SERVICE_EVENTS,
  MORI_DISKSTATS, MORI_UPTIME, MORI_MEMINFO, MORI_BOOT_ID_FILE,
  MORI_DF_BIN, MORI_PGREP_BIN, MORI_JOURNALCTL_BIN, MORI_JQ_BIN,
  MORI_TMUX_BIN, MORI_TIMEOUT_BIN, MORI_GIT_BIN, MORI_DISK_TARGETS,
  MORI_TMUX_SCOPE_ROOT, MORI_NOW_EPOCH.

MORI_CGROUP_CURRENT points outside /sys/fs/cgroup on purpose: the census
refuses to read such a path (`refused:outside-sysfs-cgroup`), which is the
provable "no live cgroup read" state, not a live query.

Usage:
  mori-round17-jj-regressions.py --census PATH --output DIR [--scratch DIR] [--keep-scratch]
  mori-round17-jj-regressions.py --selftest [--scratch DIR] [--keep-scratch]

The 17 cases cover: plain git progress; detached at tip; detached ahead
(plain git commit); detached behind; report on-branch closure; report only
off-branch (not closed); foreign author+committer; helper-shaped jj commit
(metaedit --update-author, commit, bookmark set, with the lane.branch mirror);
jj commit without bookmark move; ambient author + lane committer; a YOUNG jj
lane (age < 7200 s) whose ambient-author finding must still be emitted; and a
sibling-shokunin author + lane committer (negative control); recorded
lane.branch=master with an attached subject-authored side branch (master is
graded, mismatch, no side credit); jj-colocated unresolved mirror
(unavailable, no HEAD fallback); jj-colocated mirror naming a missing ref
(unavailable); a jj fleet root with an unresolved mirror whose row-6 closure
must skip HEAD; and the non-jj no-resolver-input HEAD fallback (unchanged).

Writes DIR/run-manifest.json (per-case assertions, failed count, retained) and
DIR/cases/<id>.out (the exact census stream). Exit 0 = every assertion held;
1 = at least one failed assertion or a capability gap; 2 = gate setup error.

--selftest needs no live census: it runs the gate over a dormant compliant
fixture census, a HEAD-only mutant, and a one-character-short branch_tip
mutant, then over a missing census, and asserts exit codes, the stable finding
ids HEAD_BRANCH_MISMATCH / LANE_AUTHOR_MISMATCH, the exact receipt fields, the
same assertion universe on every side, the output/scratch guard arms, and the
retention policy. Its temp tree is created under --scratch or TMPDIR, never
under /tmp or /var/tmp.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCHEMA = "mori-round17-jj-regressions-v1"
LANE = "alpha"
BRANCH = "master"
ROUND = 1
AMBIENT_NAME = "Ambient Op"
AMBIENT_EMAIL = "op@example.com"
LANE_NAME = f"{LANE}-shokunin"
LANE_EMAIL = f"{LANE}@shokunin.local"
CASE_TIMEOUT = 240

FINDING_MISMATCH = "HEAD_BRANCH_MISMATCH"
FINDING_AUTHOR = "LANE_AUTHOR_MISMATCH"


# ---------------------------------------------------------------------------
# process helpers
# ---------------------------------------------------------------------------

def _text(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value


def run(argv, *, cwd=None, env=None, timeout=60):
    argv = [str(a) for a in argv]
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd) if cwd is not None else None,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )
        return {
            "argv": argv,
            "rc": proc.returncode,
            "stdout": _text(proc.stdout),
            "stderr": _text(proc.stderr),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "argv": argv,
            "rc": 124,
            "stdout": _text(exc.stdout),
            "stderr": _text(exc.stderr) + f"\ntimeout after {timeout}s",
            "timeout": True,
        }
    except OSError as exc:
        return {"argv": argv, "rc": 127, "stdout": "", "stderr": str(exc)}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8", "replace"))


def write(path: Path, text: str, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if mode is not None:
        path.chmod(mode)


def sanitized_env() -> dict:
    env = {}
    for key in ("PATH", "LANG", "LC_ALL", "TZ", "TERM"):
        if key in os.environ:
            env[key] = os.environ[key]
    env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
    env["LC_ALL"] = "C.UTF-8"
    env["LANG"] = "C.UTF-8"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)
    return env


def sandbox_tool_env(home: Path) -> dict:
    env = sanitized_env()
    env.update(
        {
            # Repo discovery is confined to the case sandbox: the lane checkout
            # above this gate's scratch owns a .jj, and neither git nor jj may
            # ever discover it.
            "GIT_CEILING_DIRECTORIES": str(home.parent),
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_DATA_HOME": str(home / ".local" / "share"),
            "XDG_STATE_HOME": str(home / ".local" / "state"),
            "JJ_CONFIG": str(home / "jjconfig.toml"),
            "GIT_CONFIG_GLOBAL": str(home / "gitconfig"),
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
        }
    )
    return env


# ---------------------------------------------------------------------------
# git / jj primitives
# ---------------------------------------------------------------------------

def git(repo: Path, args, env, timeout=60):
    return run(["git", "-C", str(repo)] + [str(a) for a in args], cwd=repo, env=env, timeout=timeout)


def git_init(repo: Path, env) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    res = run(["git", "-C", str(repo.parent), "init", "-q", "-b", BRANCH, str(repo)],
              cwd=repo.parent, env=env)
    if res["rc"] != 0:
        raise RuntimeError(f"git init failed: {res['stderr'].strip()}")


def git_commit(repo: Path, env, message: str, *, author=(AMBIENT_NAME, AMBIENT_EMAIL),
               date_epoch: int | None = None, paths=()) -> None:
    if paths:
        res = git(repo, ["add", "--"] + [str(p) for p in paths], env)
        if res["rc"] != 0:
            raise RuntimeError(f"git add failed: {res['stderr'].strip()}")
    argv = [
        "git", "-C", str(repo),
        "-c", f"user.name={author[0]}", "-c", f"user.email={author[1]}",
        "commit", "-q", "-m", message,
    ]
    cenv = dict(env)
    if date_epoch is not None:
        stamp = f"@{int(date_epoch)} +0000"
        cenv["GIT_AUTHOR_DATE"] = stamp
        cenv["GIT_COMMITTER_DATE"] = stamp
    res = run(argv, cwd=repo, env=cenv)
    if res["rc"] != 0:
        raise RuntimeError(f"git commit failed: {res['stderr'].strip()}")


def git_rev(repo: Path, rev: str, env) -> str:
    res = git(repo, ["rev-parse", "--verify", "-q", rev], env)
    return res["stdout"].strip() if res["rc"] == 0 else ""


def _oid12(repo: Path, rev: str, env) -> str:
    """Full object name, sliced to the census's 12-char receipt field.

    The census emits `head=`/`branch_tip=` as the first 12 hex characters of
    the full OID (mori-census.sh:2443); `rev-parse --short` is a different
    grammar and is never used as the oracle here.
    """
    full = git_rev(repo, rev, env)
    if not re.fullmatch(r"[0-9a-f]{40,64}", full):
        raise RuntimeError(f"cannot resolve a full commit OID for {rev} in {repo}: {full!r}")
    return full[:12]


def set_lane_branch(sb: dict, branch: str = BRANCH) -> None:
    """Mirror scripts/hyaku/jj-lane.sh init: git config lane.branch <branch>.

    The helper writes this mirror at init (jj-lane.sh:439); the census resolver
    reads it as the only jj-colocated branch input.
    """
    res = git(sb["lane"], ["config", "lane.branch", branch], sb["tool_env"])
    if res["rc"] != 0:
        raise RuntimeError(f"git config lane.branch failed: {res['stderr'].strip()}")


def set_launch_age(sb: dict, age_seconds: int) -> None:
    """Rewrite the ledger launch anchor so the census sees a younger lane.

    Commit timestamps use the real clock; the anchor is therefore placed
    age_seconds before real now. The census pins NOW at real now + 120 s, so
    the observed age is age_seconds + 120 (still < 7200 for the young case).
    """
    launch = int(time.time()) - int(age_seconds)
    write(sb["ufo"] / "watchdog.log",
          f"{iso_utc(launch)} launch {LANE} round={ROUND} pid=4242\n")


def jj_run(jj: str, repo: Path, args, env, timeout=120):
    # The gate's scratch lives under the lane checkout, whose .jj is visible to
    # jj's upward discovery. Every non-init jj call names its workspace with -R
    # after the workspace .jj is proven to exist; discovery is never relied on.
    if not (repo / ".jj").is_dir():
        raise RuntimeError(f"no jj workspace at {repo} (.jj missing)")
    return run([jj, "-R", str(repo)] + [str(a) for a in args], cwd=repo, env=env, timeout=timeout)


def jj_ok(jj: str, repo: Path, args, env) -> dict:
    res = jj_run(jj, repo, args, env)
    if res["rc"] != 0:
        raise RuntimeError(
            "jj " + " ".join(str(a) for a in args) + " failed: " + res["stderr"].strip()
        )
    return res


def jj_colocate(jj: str, repo: Path, case_dir: Path, env) -> None:
    # The one exception the sandbox guard allows: an explicit absolute path, run
    # from the case directory (outside every repo), never from inside the lane.
    res = run([jj, "git", "init", "--colocate", str(repo)], cwd=case_dir, env=env)
    if res["rc"] != 0:
        raise RuntimeError(f"jj git init --colocate failed: {res['stderr'].strip()}")
    if not (repo / ".jj").is_dir():
        raise RuntimeError("jj git init --colocate did not create a sandbox .jj")


def jj_head_commit(jj: str, repo: Path, env) -> str:
    res = jj_ok(jj, repo, ["--ignore-working-copy", "log", "--no-graph", "-r", "@-", "-T", "commit_id"], env)
    value = res["stdout"].strip()
    if not re.fullmatch(r"[0-9a-f]{40,64}", value):
        raise RuntimeError(f"jj @- did not resolve to a commit id: {value!r}")
    return value


# ---------------------------------------------------------------------------
# stubs
# ---------------------------------------------------------------------------

STUB_DF = """#!/bin/sh
printf '%s\\n' 'Filesystem 1024-blocks Used Available Capacity Mounted on'
printf '%s\\n' '/dev/fake0 1000000 50000 950000 5% /'
exit 0
"""

STUB_PGREP = """#!/bin/sh
printf '%s\\n' '4242 bash /fleet/scripts/shokunin-watchdog.sh'
exit 0
"""

STUB_EMPTY = """#!/bin/sh
exit 0
"""

STUB_JQ_FAIL = """#!/bin/sh
exit 1
"""


def build_stubs(stub_dir: Path, jq_bin: str) -> dict:
    stub_dir.mkdir(parents=True, exist_ok=True)
    write(stub_dir / "df", STUB_DF, 0o755)
    write(stub_dir / "pgrep", STUB_PGREP, 0o755)
    write(stub_dir / "journalctl", STUB_EMPTY, 0o755)
    write(stub_dir / "tmux", STUB_EMPTY, 0o755)
    write(stub_dir / "jq-fail", STUB_JQ_FAIL, 0o755)
    jq = jq_bin if jq_bin else str(stub_dir / "jq-fail")
    return {
        "df": str(stub_dir / "df"),
        "pgrep": str(stub_dir / "pgrep"),
        "journalctl": str(stub_dir / "journalctl"),
        "tmux": str(stub_dir / "tmux"),
        "jq": jq,
    }


# ---------------------------------------------------------------------------
# sandbox
# ---------------------------------------------------------------------------

def iso_utc(epoch: int) -> str:
    return _dt.datetime.fromtimestamp(epoch, _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def build_sandbox(case_dir: Path, now: int, tools: dict) -> dict:
    root = case_dir / "root"
    ufo = root / ".ufo"
    state = ufo / "state"
    waves = ufo / "waves"
    reports = ufo / "reports" / f"round-{ROUND}"
    lane = root / f"{LANE}-shokunin"
    home = case_dir / "home"
    stub_dir = case_dir / "stub"
    fix = case_dir / "fix"

    for path in (state, waves, reports, home / ".config", home / ".cache", fix):
        path.mkdir(parents=True, exist_ok=True)

    write(root / "shokunin.conf", f'LANES="\n{LANE}|{LANE}-shokunin|axis\n"\n')
    write(state / f"{LANE}.round", f"{ROUND}\n")
    write(ufo / "watchdog.log", f"{iso_utc(now - 8000)} launch {LANE} round={ROUND} pid=4242\n")
    write(root / "README.md", "round-17 jj gate sandbox\n")

    write(home / "gitconfig",
          f"[user]\n\tname = {AMBIENT_NAME}\n\temail = {AMBIENT_EMAIL}\n"
          f"[init]\n\tdefaultBranch = {BRANCH}\n")
    write(home / "jjconfig.toml",
          f'[user]\nname = "{AMBIENT_NAME}"\nemail = "{AMBIENT_EMAIL}"\n')

    stubs = build_stubs(stub_dir, tools.get("jq") or "")

    cg = fix / "cgroup"
    cg.mkdir(parents=True, exist_ok=True)
    write(cg / "memory.events",
          "low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n")
    write(cg / "memory.events.local",
          "low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\n")
    write(cg / "memory.current", "123456\n")
    write(cg / "memory.max", "max\n")
    write(cg / "memory.peak", "123456\n")
    write(cg / "memory.pressure",
          "some avg10=0.00 avg60=0.00 avg300=0.00 total=100\n"
          "full avg10=0.00 avg60=0.00 avg300=0.00 total=50\n")
    write(fix / "meminfo", "MemTotal:       16000000 kB\nMemAvailable:   12000000 kB\nMemFree:         8000000 kB\n")
    write(fix / "diskstats", "8 0 fake0 100 0 5000 100 0 0 0 0 0 0 0 0 0 0 0 0\n")
    write(fix / "uptime", "12345.67 40000.00\n")
    write(fix / "boot_id", "11111111-2222-3333-4444-555555555555\n")

    tool_env = sandbox_tool_env(home)
    git_init(root, tool_env)
    git_commit(root, tool_env, "root base", date_epoch=now - 9000, paths=["README.md"])

    git_init(lane, tool_env)
    write(lane / "seed.txt", "seed\n")
    git_commit(lane, tool_env, "lane base", date_epoch=now - 9000, paths=["seed.txt"])

    census_env = sanitized_env()
    census_env.update(
        {
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "JJ_CONFIG": str(home / "jjconfig.toml"),
            "GIT_CONFIG_GLOBAL": str(home / "gitconfig"),
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CEILING_DIRECTORIES": str(case_dir),
            "PATH": str(stub_dir) + os.pathsep + census_env["PATH"],
            "MORI_SHOKUNIN_ROOT": str(root),
            "MORI_UFO_DIR": str(ufo),
            "MORI_WATCHDOG_LOG": str(ufo / "watchdog.log"),
            "MORI_TIMELINE_FILE": str(ufo / "watchdog.log"),
            "MORI_STATE_DIR": str(state),
            "MORI_WAVES_DIR": str(waves),
            "MORI_FLEET_CONF": str(root / "shokunin.conf"),
            "MORI_ROSTER_LANES": "",
            "MORI_CGROUP_EVENTS": str(cg / "memory.events"),
            "MORI_CGROUP_CURRENT": str(cg / "memory.current"),
            "MORI_CGROUP_PRESSURE": str(cg / "memory.pressure"),
            "MORI_CGROUP_MAX": str(cg / "memory.max"),
            "MORI_CGROUP_PEAK": str(cg / "memory.peak"),
            "MORI_CGROUP_LOCAL_EVENTS": str(cg / "memory.events.local"),
            "MORI_CGROUP_SERVICE_EVENTS": str(cg / "memory.events.local"),
            "MORI_DISKSTATS": str(fix / "diskstats"),
            "MORI_UPTIME": str(fix / "uptime"),
            "MORI_MEMINFO": str(fix / "meminfo"),
            "MORI_BOOT_ID_FILE": str(fix / "boot_id"),
            "MORI_DF_BIN": stubs["df"],
            "MORI_PGREP_BIN": stubs["pgrep"],
            "MORI_JOURNALCTL_BIN": stubs["journalctl"],
            "MORI_JQ_BIN": stubs["jq"],
            "MORI_TMUX_BIN": stubs["tmux"],
            "MORI_TIMEOUT_BIN": tools["timeout"],
            "MORI_GIT_BIN": tools["git"],
            "MORI_DISK_TARGETS": f"{root} {case_dir}",
            "MORI_TMUX_SCOPE_ROOT": str(root),
            "MORI_NOW_EPOCH": str(now),
            "MORI_TMUX_TIMEOUT_S": "2",
            "MORI_JOURNAL_TIMEOUT_S": "2",
        }
    )
    return {
        "case_dir": case_dir,
        "root": root,
        "ufo": ufo,
        "state": state,
        "waves": waves,
        "reports": reports,
        "lane": lane,
        "home": home,
        "stub": stub_dir,
        "fix": fix,
        "tool_env": tool_env,
        "census_env": census_env,
    }


def refs_snapshot(sb: dict) -> dict:
    env = sb["tool_env"]
    snap = {}
    for label, repo in (("root", sb["root"]), ("lane", sb["lane"])):
        head = git_rev(repo, "HEAD", env)
        branch = git_rev(repo, f"refs/heads/{BRANCH}", env)
        # Full OIDs state the revision measured; the 12-char slices are the
        # census receipt grammar, recorded so a reader can compare them without
        # re-deriving a `rev-parse --short`.
        snap[label] = {
            "head": head,
            "head12": head[:12],
            "branch": branch,
            "branch12": branch[:12],
        }
    return snap


# ---------------------------------------------------------------------------
# expectations
# ---------------------------------------------------------------------------

def expect_progressing(*forbid):
    return {
        "state": "progressing",
        "basis": "row-A",
        "roll": "CLEAN",
        "rc": 0,
        "require": [],
        "forbid": list(forbid) if forbid else [FINDING_MISMATCH, FINDING_AUTHOR],
    }


def expect_weak(*forbid):
    return {
        "state": "progressing-weak",
        "basis": "row-C",
        "roll": "CLEAN",
        "rc": 0,
        "require": [],
        "forbid": list(forbid) if forbid else [FINDING_MISMATCH, FINDING_AUTHOR],
    }


def expect_silent(*forbid):
    return {
        "state": "silent",
        "basis": "row-D",
        "roll": "DRIFT",
        "rc": 1,
        "require": [],
        "forbid": list(forbid) if forbid else [FINDING_MISMATCH, FINDING_AUTHOR],
    }


def expect_closed():
    return {
        "state": "not-open",
        "basis": "row-6",
        "roll": "CLEAN",
        "rc": 0,
        "require": [],
        "forbid": [FINDING_MISMATCH, FINDING_AUTHOR],
    }


def expect_unavailable():
    """Fail-closed resolver: no progress and no C2 finding, not a row grade."""
    return {
        "state": "unavailable",
        "basis": "row-1",
        "roll": "CLEAN",
        "rc": 0,
        "require": [],
        "forbid": [FINDING_MISMATCH, FINDING_AUTHOR],
        # CensusJj A2: every unusable mirror reports this exact reason.
        "detail_contains": ["reason=ref-unresolved"],
    }


def expect_young():
    """Row-8 young: the author diagnostic must still fire as a warn."""
    return {
        "state": "young",
        "basis": "row-8",
        "roll": "DRIFT",
        "rc": 1,
        "require": [],
        "forbid": [FINDING_MISMATCH],
    }


def mismatch_requirement(sb: dict) -> dict:
    env = sb["tool_env"]
    head12 = _oid12(sb["lane"], "HEAD", env)
    branch12 = _oid12(sb["lane"], f"refs/heads/{BRANCH}", env)
    return {
        "id": FINDING_MISMATCH,
        "severity_exact": "warn",
        # Exact whitespace tokens from the census's own receipt grammar
        # (mori-census.sh:2443): head= and branch_tip= are the first 12 hex
        # characters of the FULL OIDs, plus the fixed basis token.
        "obs_tokens": [
            f"head={head12}",
            f"branch_tip={branch12}",
            "basis=merge-base-not-ancestor",
        ],
        "obs_contains": [f"lane={LANE}"],
    }


def author_requirement() -> dict:
    return {
        "id": FINDING_AUTHOR,
        "severity_exact": "warn",
        # Exact tokens from mori-census.sh:2446: count= and the fixed basis.
        "obs_tokens": [
            f"lane={LANE}",
            "count=1",
            "basis=committer-lane-author-foreign-email",
        ],
        "obs_contains": [],
    }


# ---------------------------------------------------------------------------
# case setups
# ---------------------------------------------------------------------------

def case_git_plain_progress(sb, tools):
    env = sb["tool_env"]
    write(sb["lane"] / "work.txt", "lane work\n")
    git_commit(sb["lane"], env, "lane work", author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    return expect_progressing()


def case_git_detached_at_tip(sb, tools):
    env = sb["tool_env"]
    write(sb["lane"] / "work.txt", "lane work\n")
    git_commit(sb["lane"], env, "lane work", author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    tip = git_rev(sb["lane"], f"refs/heads/{BRANCH}", env)
    res = git(sb["lane"], ["checkout", "-q", "--detach", tip], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach failed: {res['stderr'].strip()}")
    return expect_progressing()


def case_git_detached_commit(sb, tools):
    """Plain git commit on a detached HEAD: HEAD is ahead of the branch."""
    env = sb["tool_env"]
    res = git(sb["lane"], ["checkout", "-q", "--detach", "HEAD"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach failed: {res['stderr'].strip()}")
    write(sb["lane"] / "offbranch.txt", "off branch\n")
    git_commit(sb["lane"], env, "off-branch work", author=(LANE_NAME, LANE_EMAIL), paths=["offbranch.txt"])
    expect = expect_silent(FINDING_AUTHOR)
    expect["require"] = [mismatch_requirement(sb)]
    return expect


def case_git_detached_behind(sb, tools):
    """Detached HEAD behind the branch: still an ancestor, so no mismatch."""
    env = sb["tool_env"]
    write(sb["lane"] / "work.txt", "lane work\n")
    git_commit(sb["lane"], env, "lane work", author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    res = git(sb["lane"], ["checkout", "-q", "--detach", "HEAD~1"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach HEAD~1 failed: {res['stderr'].strip()}")
    return expect_progressing()


def case_git_report_on_branch(sb, tools):
    env = sb["tool_env"]
    report = sb["reports"] / f"{LANE}.md"
    write(report, "# alpha report\n")
    git_commit(sb["root"], env, "committed report", paths=[report.relative_to(sb["root"])])
    return expect_closed()


def case_git_report_off_branch(sb, tools):
    """The report exists only on a detached HEAD; the branch does not have it."""
    env = sb["tool_env"]
    res = git(sb["root"], ["checkout", "-q", "--detach", "HEAD"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach failed: {res['stderr'].strip()}")
    report = sb["reports"] / f"{LANE}.md"
    write(report, "# alpha draft report (off branch)\n")
    git_commit(sb["root"], env, "draft report off branch", paths=[report.relative_to(sb["root"])])
    return expect_silent()


def case_git_foreign_author(sb, tools):
    env = sb["tool_env"]
    write(sb["lane"] / "foreign.txt", "foreign work\n")
    git_commit(sb["lane"], env, "foreign work", author=(AMBIENT_NAME, AMBIENT_EMAIL), paths=["foreign.txt"])
    return expect_weak()


def case_jj_helper_commit(sb, tools):
    """The helper shape: metaedit --update-author, commit, bookmark set."""
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)
    jj_colocate(jj, lane, sb["case_dir"], env)
    with (lane / "seed.txt").open("a", encoding="utf-8") as handle:
        handle.write("helper work\n")
    jj_ok(jj, lane, ["--config", f"user.name={LANE_NAME}",
                     "--config", f"user.email={LANE_EMAIL}",
                     "metaedit", "--update-author"], env)
    jj_ok(jj, lane, ["--config", f"user.name={LANE_NAME}",
                     "--config", f"user.email={LANE_EMAIL}",
                     "commit", "-m", "helper work"], env)
    commit = jj_head_commit(jj, lane, env)
    jj_ok(jj, lane, ["--ignore-working-copy", "bookmark", "set", BRANCH, "-r", commit], env)
    return expect_progressing()


def case_jj_commit_no_bookmark(sb, tools):
    """jj commit without the bookmark step: HEAD is ahead of the branch."""
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)
    jj_colocate(jj, lane, sb["case_dir"], env)
    with (lane / "seed.txt").open("a", encoding="utf-8") as handle:
        handle.write("off-branch jj work\n")
    jj_ok(jj, lane, ["--config", f"user.name={LANE_NAME}",
                     "--config", f"user.email={LANE_EMAIL}",
                     "commit", "-m", "off-branch jj work"], env)
    expect = expect_silent(FINDING_AUTHOR)
    expect["require"] = [mismatch_requirement(sb)]
    return expect


def case_jj_ambient_author(sb, tools):
    """Ambient author (stamped into @ at init) + lane committer, bookmark moved."""
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)
    jj_colocate(jj, lane, sb["case_dir"], env)
    with (lane / "seed.txt").open("a", encoding="utf-8") as handle:
        handle.write("ambient-authored work\n")
    # No metaedit: @ keeps the ambient author, the committer is the lane.
    jj_ok(jj, lane, ["--config", f"user.name={LANE_NAME}",
                     "--config", f"user.email={LANE_EMAIL}",
                     "commit", "-m", "ambient-authored work"], env)
    commit = jj_head_commit(jj, lane, env)
    jj_ok(jj, lane, ["--ignore-working-copy", "bookmark", "set", BRANCH, "-r", commit], env)
    expect = expect_weak(FINDING_MISMATCH)
    expect["roll"] = "DRIFT"
    expect["rc"] = 1
    expect["require"] = [author_requirement()]
    return expect


def case_jj_young_ambient_author(sb, tools):
    """Young jj lane (age < 7200 s): LANE_AUTHOR_MISMATCH still warns."""
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)
    jj_colocate(jj, lane, sb["case_dir"], env)
    with (lane / "seed.txt").open("a", encoding="utf-8") as handle:
        handle.write("young ambient work\n")
    jj_ok(jj, lane, ["--config", f"user.name={LANE_NAME}",
                     "--config", f"user.email={LANE_EMAIL}",
                     "commit", "-m", "young ambient work"], env)
    commit = jj_head_commit(jj, lane, env)
    jj_ok(jj, lane, ["--ignore-working-copy", "bookmark", "set", BRANCH, "-r", commit], env)
    set_launch_age(sb, 100)
    expect = expect_young()
    expect["require"] = [author_requirement()]
    return expect


def case_jj_sibling_author(sb, tools):
    """Kengaku-style negative control: committer lane, author a sibling lane.

    The amended A1 rule only fires when the author email does NOT end in
    @shokunin.local, so a legitimate sibling-shokunin author must stay quiet.
    """
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)
    jj_colocate(jj, lane, sb["case_dir"], env)
    with (lane / "seed.txt").open("a", encoding="utf-8") as handle:
        handle.write("sibling-authored work\n")
    jj_ok(jj, lane, ["--config", "user.name=kengaku-shokunin",
                     "--config", "user.email=kengaku@shokunin.local",
                     "metaedit", "--update-author"], env)
    jj_ok(jj, lane, ["--config", f"user.name={LANE_NAME}",
                     "--config", f"user.email={LANE_EMAIL}",
                     "commit", "-m", "sibling-authored work"], env)
    commit = jj_head_commit(jj, lane, env)
    jj_ok(jj, lane, ["--ignore-working-copy", "bookmark", "set", BRANCH, "-r", commit], env)
    # Author is kengaku (a lane identity), so grading is progressing-weak, and
    # the amended author rule must NOT emit LANE_AUTHOR_MISMATCH.
    return expect_weak()


def case_jj_sidebranch_mirror(sb, tools):
    """Recorded lane.branch=master wins over an attached `side` branch.

    The side commit is subject-authored but off the lane branch: master is the
    only graded ref, so it earns no progress credit; HEAD ahead of master is a
    HEAD_BRANCH_MISMATCH. A second base branch (`main`) keeps the entering
    census's unique-master/main fallback ambiguous, so its before behavior is
    the HEAD fallback deterministically.
    """
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)
    res = git(lane, ["branch", "main", BRANCH], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git branch main failed: {res['stderr'].strip()}")
    res = git(lane, ["checkout", "-q", "-b", "side"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout -b side failed: {res['stderr'].strip()}")
    write(lane / "side.txt", "side work\n")
    git_commit(lane, env, "side work", author=(LANE_NAME, LANE_EMAIL), paths=["side.txt"])
    jj_colocate(jj, lane, sb["case_dir"], env)
    expect = expect_silent(FINDING_AUTHOR)
    expect["require"] = [mismatch_requirement(sb)]
    return expect


def case_jj_unresolved_mirror(sb, tools):
    """.jj lane with no lane.branch mirror: unavailable, never HEAD-anchored."""
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    res = git(lane, ["branch", "-m", "master", "trunk"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git branch -m failed: {res['stderr'].strip()}")
    write(lane / "work.txt", "lane work\n")
    git_commit(lane, env, "lane work", author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    tip = git_rev(lane, "refs/heads/trunk", env)
    res = git(lane, ["checkout", "-q", "--detach", tip], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach failed: {res['stderr'].strip()}")
    jj_colocate(jj, lane, sb["case_dir"], env)
    return expect_unavailable()


def case_jj_missingref_mirror(sb, tools):
    """lane.branch names a ref that does not exist: unavailable, no attached fallback."""
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
    set_lane_branch(sb)  # lane.branch=master, then remove the master ref
    res = git(lane, ["branch", "-m", "master", "trunk"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git branch -m failed: {res['stderr'].strip()}")
    write(lane / "work.txt", "lane work\n")
    git_commit(lane, env, "lane work", author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    tip = git_rev(lane, "refs/heads/trunk", env)
    res = git(lane, ["checkout", "-q", "--detach", tip], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach failed: {res['stderr'].strip()}")
    jj_colocate(jj, lane, sb["case_dir"], env)
    return expect_unavailable()


def case_jj_root_unresolved_closure(sb, tools):
    """jj fleet root with no lane.branch mirror: row-6 never falls back to HEAD."""
    jj = tools["jj"]
    env = sb["tool_env"]
    report = sb["reports"] / f"{LANE}.md"
    write(report, "# alpha report on root HEAD\n")
    git_commit(sb["root"], env, "committed report",
               paths=[report.relative_to(sb["root"])])
    write(sb["lane"] / "work.txt", "lane work\n")
    git_commit(sb["lane"], env, "lane work",
               author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    jj_colocate(jj, sb["root"], sb["case_dir"], env)
    return expect_progressing()


def case_git_fallback_head(sb, tools):
    """No master/main/origin HEAD: the census must fall back to bare HEAD."""
    env = sb["tool_env"]
    res = git(sb["lane"], ["branch", "-m", "master", "trunk"], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git branch -m failed: {res['stderr'].strip()}")
    write(sb["lane"] / "work.txt", "lane work\n")
    git_commit(sb["lane"], env, "lane work", author=(LANE_NAME, LANE_EMAIL), paths=["work.txt"])
    tip = git_rev(sb["lane"], "refs/heads/trunk", env)
    res = git(sb["lane"], ["checkout", "-q", "--detach", tip], env)
    if res["rc"] != 0:
        raise RuntimeError(f"git checkout --detach failed: {res['stderr'].strip()}")
    return expect_progressing()


CASES = [
    ("git-plain-progress", "plain git lane: lane-authored commit on the branch", case_git_plain_progress),
    ("git-detached-at-tip", "detached HEAD exactly at the branch tip is not a mismatch", case_git_detached_at_tip),
    ("git-detached-commit", "plain git commit on a detached HEAD: HEAD ahead -> mismatch, no progress", case_git_detached_commit),
    ("git-detached-behind", "detached HEAD behind the branch: ancestor holds, no mismatch", case_git_detached_behind),
    ("git-report-on-branch", "report committed on the branch closes the lane (row 6)", case_git_report_on_branch),
    ("git-report-off-branch", "report only on a detached HEAD does not close the lane", case_git_report_off_branch),
    ("git-foreign-author", "foreign author+committer on the branch is progressing-weak, not LANE_AUTHOR_MISMATCH", case_git_foreign_author),
    ("jj-helper-commit", "helper-shaped jj commit (metaedit, commit, bookmark set) is progressing", case_jj_helper_commit),
    ("jj-commit-no-bookmark", "jj commit without bookmark move: mismatch + no progress credit", case_jj_commit_no_bookmark),
    ("jj-ambient-author", "ambient author + lane committer on the branch -> LANE_AUTHOR_MISMATCH", case_jj_ambient_author),
    ("jj-young-ambient-author", "young jj lane (age < 7200 s): LANE_AUTHOR_MISMATCH warn is still emitted", case_jj_young_ambient_author),
    ("jj-sibling-author", "sibling-shokunin author + lane committer -> no LANE_AUTHOR_MISMATCH (negative control)", case_jj_sibling_author),
    ("jj-sidebranch-mirror", "recorded lane.branch=master + attached side branch: master graded, mismatch, no side credit", case_jj_sidebranch_mirror),
    ("jj-unresolved-mirror", ".jj lane without a lane.branch mirror -> unavailable, no HEAD fallback", case_jj_unresolved_mirror),
    ("jj-missingref-mirror", ".jj lane whose lane.branch ref is missing -> unavailable, no attached fallback", case_jj_missingref_mirror),
    ("jj-root-unresolved-closure", "jj root without lane.branch mirror: row-6 skips closure (never HEAD), lane still graded", case_jj_root_unresolved_closure),
    ("git-fallback-head", "non-jj lane with no resolver input (branch trunk, detached) -> unchanged HEAD grading", case_git_fallback_head),
]


# ---------------------------------------------------------------------------
# census parsing / assertions
# ---------------------------------------------------------------------------

SURFACE_RE = re.compile(r"^SURFACE lane\." + re.escape(LANE) + r": (\S+) \((.*)\)$", re.M)
FINDING_RE = re.compile(r"^FINDING (\S+) severity=(\S+) obs=(.*)$", re.M)
VERDICT_RE = re.compile(
    r"^MORI_CENSUS: (\S+) \(findings=(\d+) drift=(\d+) unavailable=(\d+) surfaces=(\d+)\)$", re.M
)


def parse_census(text: str) -> dict:
    surfaces = SURFACE_RE.findall(text)
    findings = [
        {"id": fid, "severity": sev, "obs": obs}
        for fid, sev, obs in FINDING_RE.findall(text)
    ]
    verdicts = VERDICT_RE.findall(text)
    state = surfaces[0][0] if surfaces else None
    detail = surfaces[0][1] if surfaces else ""
    basis_match = re.search(r"\bbasis=(row-[A-Za-z0-9]+)", detail)
    return {
        "state": state,
        "detail": detail,
        "basis": basis_match.group(1) if basis_match else None,
        "findings": findings,
        "verdict": verdicts[0][0] if verdicts else None,
        "verdict_count": len(verdicts),
        "surface_count": len(surfaces),
        "verdict_fields": (
            {
                "findings": int(verdicts[0][1]),
                "drift": int(verdicts[0][2]),
                "unavailable": int(verdicts[0][3]),
                "surfaces": int(verdicts[0][4]),
            }
            if verdicts
            else None
        ),
    }


def evaluate(sb: dict, census_path: Path, expect: dict, refs_before: dict) -> dict:
    bash = shutil.which("bash") or "/bin/bash"
    res = run([bash, str(census_path)], cwd=sb["root"], env=sb["census_env"], timeout=CASE_TIMEOUT)
    refs_after = refs_snapshot(sb)
    text = res["stdout"] + res["stderr"]
    parsed = parse_census(text)

    checks = []

    def check(cid, ok, detail):
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    check("census_exit", res["rc"] == expect["rc"], f"rc={res['rc']} expected={expect['rc']}")
    check("verdict_present", parsed["verdict"] is not None, f"verdict={parsed['verdict']}")
    check("verdict_unique", parsed["verdict_count"] == 1, f"verdict_lines={parsed['verdict_count']}")
    check("verdict_roll", parsed["verdict"] == expect["roll"],
          f"roll={parsed['verdict']} expected={expect['roll']}")
    check("lane_surface_unique", parsed["surface_count"] == 1, f"lane_surface_rows={parsed['surface_count']}")
    check("lane_state", parsed["state"] == expect["state"],
          f"state={parsed['state']} expected={expect['state']}")
    check("lane_basis", parsed["basis"] == expect["basis"],
          f"basis={parsed['basis']} expected={expect['basis']}")
    for needle in expect.get("detail_contains", []):
        check(f"lane_detail_contains:{needle}", needle in parsed["detail"],
              f"detail={parsed['detail']}")
    check("refs_unchanged", refs_before == refs_after,
          f"before={json.dumps(refs_before, sort_keys=True)} after={json.dumps(refs_after, sort_keys=True)}")

    by_id = {}
    for finding in parsed["findings"]:
        by_id.setdefault(finding["id"], finding)

    for requirement in expect["require"]:
        fid = requirement["id"]
        finding = by_id.get(fid)
        present = finding is not None
        check(f"finding:{fid}:present", present, f"findings={sorted(by_id)}")
        # Fixed assertion universe (falsify ReceiptC2Controls Q1): severity and
        # every detail check are emitted even when the finding is absent, so the
        # before and after runs have the same denominator and a missing field
        # fails its own check instead of shrinking the universe.
        expected_sev = requirement.get("severity_exact")
        if expected_sev:
            check(
                f"finding:{fid}:severity",
                present and finding["severity"] == expected_sev,
                f"severity={finding['severity'] if present else 'absent'} expected={expected_sev}",
            )
        obs = finding["obs"] if present else ""
        obs_tokens = set(obs.split())
        for token in requirement.get("obs_tokens", []):
            check(
                f"finding:{fid}:obs_token:{token}",
                token in obs_tokens,
                f"token={token!r} present={present} obs={obs or 'absent'}",
            )
        for needle in requirement.get("obs_contains", []):
            check(
                f"finding:{fid}:obs_contains:{needle}",
                present and needle in obs,
                f"needle={needle!r} present={present} obs={obs or 'absent'}",
            )

    for fid in expect["forbid"]:
        check(f"finding:{fid}:absent", fid not in by_id, f"findings={sorted(by_id)}")

    if "jj" in sb and sb["jj"]:
        # The jj repo config is written under the redirected HOME, never under
        # the operator's ~/.config/jj. This is the positive redirect evidence.
        check(
            "jj_config_redirected",
            (sb["home"] / ".config" / "jj").exists(),
            f"path={sb['home'] / '.config' / 'jj'}",
        )

    failed = [c for c in checks if not c["ok"]]
    return {
        "checks": checks,
        "failed_assertions": len(failed),
        "result": res,
        "text": text,
        "parsed": parsed,
        "refs_after": refs_after,
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def manifest_case(case_id: str, description: str, status: str, checks, observed=None,
                  output_file: str | None = None, sandbox: str | None = None,
                  census_command=None, census_sha: str | None = None) -> dict:
    return {
        "id": case_id,
        "description": description,
        "status": status,
        "assertions": checks,
        "failed_assertions": sum(1 for c in checks if not c["ok"]),
        "observed": observed or {},
        "sandbox": sandbox,
        "census_command": census_command,
        "census_stdout_sha256": census_sha,
        "output_file": output_file,
    }


def resolve_tools(args) -> dict:
    git_bin = shutil.which("git")
    if not git_bin:
        raise RuntimeError("git not found on PATH")
    jj_override = os.environ.get("MORI_JJ_BIN", "").strip()
    candidates = []
    if jj_override:
        candidates.append(jj_override)
    candidates.append(str(Path.home() / ".local" / "bin" / "jj"))
    found = shutil.which("jj")
    if found:
        candidates.append(found)
    jj_bin = ""
    for candidate in candidates:
        if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            jj_bin = candidate
            break
    timeout_bin = shutil.which("timeout") or "/usr/bin/timeout"
    return {
        "git": git_bin,
        "jj": jj_bin,
        "timeout": timeout_bin,
        "jq": shutil.which("jq") or "",
        "bash": shutil.which("bash") or "/bin/bash",
    }


def tool_version(argv) -> str:
    if not argv or not argv[0]:
        return "absent"
    res = run(argv, timeout=20)
    line = (res["stdout"] or res["stderr"]).strip().splitlines()
    value = line[0] if line else f"rc={res['rc']}"
    return value


# ---------------------------------------------------------------------------
# output / scratch guards (falsify SandboxFinal F2/F4)
# ---------------------------------------------------------------------------
#
# The gate writes two things: the output directory (manifest + case streams)
# and a fresh run tree under scratch (real git/jj sandboxes). Both are validated
# BEFORE any write, must not overlap the gate/census checkouts, their protected
# subtrees, or the census input, and the scratch run tree is removed by default
# (--keep-scratch opts into forensic retention; the manifest records retained).

PROTECTED_DIRS = ("tools", "corpus", ".git", ".jj")
TMP_ROOTS = (Path("/tmp"), Path("/var/tmp"))


def _within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _repo_root_of(path: Path) -> Path | None:
    """Nearest ancestor carrying .git or .jj -- filesystem only, no git call."""
    try:
        current = path.resolve()
    except OSError:
        return None
    if not current.is_dir():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or (candidate / ".jj").exists():
            return candidate
    return None


def _repo_roots(paths) -> list:
    roots = []
    for path in paths:
        if path is None:
            continue
        root = _repo_root_of(Path(path))
        if root is not None and root not in roots:
            roots.append(root)
    return roots


def _protected_error(path: Path, label: str, roots, inputs, gate_file: Path) -> str | None:
    for root in roots:
        if _within(root, path):
            return f"{label} is the repo root or an ancestor of it: {path} (repo {root})"
        for name in PROTECTED_DIRS:
            if _within(path, root / name):
                return f"{label} is inside protected {name}/: {path}"
        ufo = root / ".ufo"
        if _within(path, ufo) and not _within(path, ufo / "waves"):
            return (
                f"{label} is inside protected .ufo/ "
                f"(only .ufo/waves evidence is allowed): {path}"
            )
    for input_path in inputs:
        if path == input_path or _within(input_path, path):
            return f"{label} overlaps the input path: {input_path}"
    if path == gate_file or _within(gate_file, path):
        return f"{label} overlaps the gate source: {gate_file}"
    return None


def _canonical(path: Path) -> Path:
    try:
        return path.resolve()
    except OSError:
        return path.absolute()


def _has_symlink_component(path: Path) -> bool:
    """True when the raw path or any existing ancestor is a symlink.

    This MUST run before resolve(): resolve() follows the link, so
    `path.is_symlink()` on the resolved path is false for a raw symlink arg.
    """
    current = path
    while True:
        if current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def check_output_path(path: Path, roots, inputs, gate_file: Path) -> str | None:
    """Raw-path checks first, then canonical containment; no write happens."""
    if ".." in path.parts:
        return f"--output may not contain '..': {path}"
    if _has_symlink_component(path):
        return f"--output or an existing ancestor is a symlink: {path}"
    if os.path.lexists(path) and not path.is_dir():
        return f"--output exists and is not a directory: {path}"
    if path.is_dir():
        try:
            if any(path.iterdir()):
                return f"--output is not empty: {path}"
        except OSError as exc:
            return f"--output is unreadable: {path}: {exc}"
    return _protected_error(_canonical(path), "--output", roots, inputs, gate_file)


def check_scratch_path(path: Path, roots, inputs, gate_file: Path, output: Path) -> str | None:
    """Validate the scratch parent before any mkdir/run-child creation."""
    if ".." in path.parts:
        return f"--scratch may not contain '..': {path}"
    if _has_symlink_component(path):
        return f"--scratch or an existing ancestor is a symlink: {path}"
    if os.path.lexists(path) and not path.is_dir():
        return f"--scratch exists and is not a directory: {path}"
    resolved = _canonical(path)
    output_resolved = _canonical(output)
    if resolved == Path("/"):
        return "--scratch may not be the filesystem root"
    for tmp in TMP_ROOTS:
        if _within(resolved, tmp):
            return f"--scratch may not live under {tmp}: {resolved}"
    if _within(resolved, output_resolved / "cases") or resolved == output_resolved / "run-manifest.json":
        return f"--scratch overlaps output artifacts: {resolved}"
    return _protected_error(resolved, "--scratch", roots, inputs, gate_file)


def make_run_dir(scratch: Path) -> Path:
    """Create a fresh, gate-owned child of scratch; never reuse an entry."""
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for attempt in range(1000):
        candidate = scratch / f"run-{stamp}-{os.getpid()}-{attempt}"
        try:
            os.mkdir(candidate, 0o700)
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError(f"cannot create a fresh run directory under {scratch}")


# ---------------------------------------------------------------------------
# selftest (PROTOCOL gate standard: isolated fixtures, stable finding ids)
# ---------------------------------------------------------------------------
#
# Three dormant fixture censuses exercise the gate itself, never a live census:
#   MODE=ok       the amended C2 contract (branch-anchored rows 6/9, both warn
#                 findings with the exact head=/branch_tip=/count= receipt
#                 grammar, sibling-author negative arm, HEAD fallback when the
#                 resolver has no input);
#   MODE=head     the entering behavior (bare HEAD, no C2 findings), used as the
#                 mutant: the gate MUST turn red and name the missing finding;
#   MODE=wrongtip the compliant fixture with branch_tip= one character short,
#                 used to prove the exact-field assertion is not a substring
#                 check.
# The fixture reproduces only what this gate parses (lane surface, findings,
# verdict); it is not a census implementation and is never installed.

FIXTURE_CENSUS = r'''#!/usr/bin/env bash
# Dormant round-17 C2 gate selftest fixture. Not production, never installed.
set -uo pipefail
MODE=__MODE__
LANE=alpha
ROOT=${MORI_SHOKUNIN_ROOT:?}
LEDGER=${MORI_TIMELINE_FILE:-$ROOT/.ufo/watchdog.log}
STATE=${MORI_STATE_DIR:-$ROOT/.ufo/state}
NOW=${MORI_NOW_EPOCH:-$(date +%s)}
GATE_S=${MORI_LANE_SILENCE_S:-7200}
REPO=$ROOT/$LANE-shokunin
N_FINDINGS=0
DRIFT=0

emit_finding() {
  printf 'FINDING %s severity=warn obs=%s ts=fixture\n' "$1" "$2"
  N_FINDINGS=$((N_FINDINGS + 1))
  DRIFT=1
}

valid_branch() { [[ $1 =~ ^[a-zA-Z0-9][a-zA-Z0-9._/-]*$ ]] && [[ $1 != jj/* && $1 != *..* ]] ; }

resolve_branch() {
  local dir=$1 b ref
  local -a c=()
  # The helper mirror (git config lane.branch, jj-lane.sh:439) is the only
  # jj-colocated input; attached/origin/unique guesses are not used there.
  b=$(git -C "$dir" config --get lane.branch 2>/dev/null || true)
  if [ -n "$b" ]; then
    if valid_branch "$b" && git -C "$dir" rev-parse --verify -q "refs/heads/$b" >/dev/null 2>&1; then
      printf '%s\n' "$b"
      return 0
    fi
    if [ -d "$dir/.jj" ]; then return 2; fi
    # Non-jj: an unusable mirror falls through to the ordinary detection.
  elif [ -d "$dir/.jj" ]; then
    return 2
  fi
  b=$(git -C "$dir" symbolic-ref -q HEAD 2>/dev/null || true)
  case $b in refs/heads/*) b=${b#refs/heads/}; if valid_branch "$b"; then printf '%s\n' "$b"; return 0; fi ;; esac
  ref=$(git -C "$dir" symbolic-ref -q refs/remotes/origin/HEAD 2>/dev/null || true)
  case $ref in refs/remotes/origin/*) ref=${ref#refs/remotes/origin/}; if valid_branch "$ref"; then printf '%s\n' "$ref"; return 0; fi ;; esac
  git -C "$dir" show-ref -q --verify refs/heads/master 2>/dev/null && c+=(master)
  git -C "$dir" show-ref -q --verify refs/heads/main 2>/dev/null && c+=(main)
  [ "${#c[@]}" -eq 1 ] && { printf '%s\n' "${c[0]}"; return 0; }
  return 1
}

branch=''
branch_rc=1
if [ "$MODE" != head ]; then
  branch=$(resolve_branch "$REPO")
  branch_rc=$?
fi
if [ "$branch_rc" -eq 2 ]; then
  # Fail-closed jj resolver: no branch input = unavailable, no progress and no
  # C2 finding (the entering behavior is NOT used for a .jj lane).
  printf 'SURFACE lane.%s: unavailable (lane=%s round=- launch_epoch=- age_s=- basis=row-1 reason=ref-unresolved; ts=fixture)\n' "$LANE" "$LANE"
  printf 'MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=1)\n'
  exit 0
fi
# The report repo has its own resolver result: a jj root with an unusable
# mirror skips row-6 closure instead of falling back to HEAD.
root_branch=''
root_rc=1
if [ "$MODE" != head ]; then
  root_branch=$(resolve_branch "$ROOT")
  root_rc=$?
fi
head=$(git -C "$REPO" rev-parse --verify -q HEAD 2>/dev/null || true)
lane_ref=HEAD
[ -n "$branch" ] && lane_ref="refs/heads/$branch"

round='-'
launch_ep=''
anchor=$(grep -E " launch $LANE round=" "$LEDGER" 2>/dev/null | tail -n 1 || true)
if [ -n "$anchor" ]; then
  round=$(printf '%s\n' "$anchor" | awk '{for (i = 1; i <= NF; i++) if ($i ~ /^round=/) { v = $i; sub(/^round=/, "", v); print v; exit }}')
  launch_ts=$(printf '%s\n' "$anchor" | awk '{print $1; exit}')
  launch_ep=$(date -u -d "$launch_ts" +%s 2>/dev/null || true)
fi

# C2 diagnostics are observations about the branch anchor and are emitted
# BEFORE any row/young/closure early return: the entering census lost the
# author scan on young and report-closed lanes (CensusNewBranches).
if [ "$MODE" != head ] && [ -n "$branch" ] && [ -n "$head" ] && [ -n "$launch_ep" ] && [ "$launch_ep" -le "$NOW" ]; then
  btip=$(git -C "$REPO" rev-parse --verify -q "refs/heads/$branch" 2>/dev/null || true)
  if [ -n "$btip" ] && ! git -C "$REPO" merge-base --is-ancestor "$head" "refs/heads/$branch" 2>/dev/null; then
    head12=${head:0:12}
    btip12=${btip:0:12}
    # wrongtip: one character short, the exact-field arm's red fixture.
    if [ "$MODE" = wrongtip ]; then btip12=${btip12:0:11}; fi
    emit_finding HEAD_BRANCH_MISMATCH "lane=$LANE head=$head12 branch=$branch branch_tip=$btip12 basis=merge-base-not-ancestor"
  fi
  am=$(git -C "$REPO" log --since="@$launch_ep" --format='%ct|%an|%ae|%cn|%ce' "$lane_ref" 2>/dev/null \
    | awk -F'|' -v lo="$launch_ep" -v hi="$NOW" \
      '$1 ~ /^[0-9]+$/ && $1 + 0 > lo + 0 && $1 + 0 <= hi + 0 && $4 == "alpha-shokunin" && $5 == "alpha@shokunin.local" && $3 !~ /@shokunin[.]local$/ { n++ } END { print n + 0 }')
  case $am in ''|*[!0-9]*) am=0 ;; esac
  if [ "$am" -gt 0 ]; then
    emit_finding LANE_AUTHOR_MISMATCH "lane=$LANE count=$am committer=$LANE-shokunin <$LANE@shokunin.local> window=launch..NOW basis=committer-lane-author-foreign-email"
  fi
fi

state=unavailable
basis=row-1
age='-'
if [ -z "$anchor" ]; then
  state=not-open
  basis=row-2
else
  if [ -z "$launch_ep" ]; then
    state=unavailable
    basis=row-1
  elif [ "$launch_ep" -gt "$NOW" ]; then
    state=young
    basis=row-3
  elif [ $((NOW - launch_ep)) -le "$GATE_S" ]; then
    state=young
    basis=row-8
    age=$((NOW - launch_ep))
  else
    age=$((NOW - launch_ep))
    state_round=$(head -n 1 -- "$STATE/$LANE.round" 2>/dev/null || true)
    advanced=0
    if [ -n "$state_round" ] && [ "$state_round" -gt "$round" ] 2>/dev/null; then advanced=1; fi
    if [ "$advanced" -eq 1 ]; then
      state=not-open
      basis=row-7
    else
      rpath=".ufo/reports/round-$round/$LANE.md"
      closed=0
      if [ "$root_rc" -ne 2 ]; then
        root_ref=HEAD
        [ -n "$root_branch" ] && root_ref="refs/heads/$root_branch"
        if git -C "$ROOT" cat-file -e "$root_ref:$rpath" 2>/dev/null; then
          ct=$(git -C "$ROOT" log -1 --format=%ct "$root_ref" -- "$rpath" 2>/dev/null || true)
          if [ -n "$ct" ] && [ "$ct" -gt "$launch_ep" ] && [ "$ct" -le "$NOW" ]; then closed=1; fi
        fi
      fi
      if [ "$closed" -eq 1 ]; then
        state=not-open
        basis=row-6
      else
        subj=0
        sib=0
        if [ -n "$head" ]; then
          lg=$(git -C "$REPO" log --since="@$launch_ep" --format='%ct %an <%ae>' "$lane_ref" 2>/dev/null || true)
          inwin=$(awk -v lo="$launch_ep" -v hi="$NOW" '$1 ~ /^[0-9]+$/ && $1 + 0 > lo + 0 && $1 + 0 <= hi + 0' <<< "$lg")
          if [ -n "$inwin" ]; then
            authors=$(awk '{ sub(/^[0-9]+ /, ""); print }' <<< "$inwin")
            case $'\n'"$authors"$'\n' in
              *$'\n'"$LANE-shokunin <$LANE@shokunin.local>"$'\n'*) subj=1 ;;
              *) sib=1 ;;
            esac
          fi
        fi
        if [ "$subj" -eq 1 ]; then
          state=progressing
          basis=row-A
        elif [ "$sib" -eq 1 ]; then
          state=progressing-weak
          basis=row-C
        else
          state=silent
          basis=row-D
          printf 'FINDING LANE_SILENT severity=warn obs=lane=%s round=%s basis=row-D ts=fixture\n' "$LANE" "$round"
          N_FINDINGS=$((N_FINDINGS + 1))
          DRIFT=1
        fi
      fi
    fi
  fi
fi

printf 'SURFACE lane.%s: %s (lane=%s round=%s launch_epoch=%s age_s=%s basis=%s; ts=fixture)\n' \
  "$LANE" "$state" "$LANE" "$round" "$launch_ep" "$age" "$basis"
if [ "$DRIFT" -eq 0 ]; then
  printf 'MORI_CENSUS: CLEAN (findings=%d drift=0 unavailable=0 surfaces=1)\n' "$N_FINDINGS"
  exit 0
fi
printf 'MORI_CENSUS: DRIFT (findings=%d drift=1 unavailable=0 surfaces=1)\n' "$N_FINDINGS"
exit 1
'''


def write_fixture_census(root: Path, mode: str) -> Path:
    path = root / f"fixture-census-{mode}.sh"
    write(path, FIXTURE_CENSUS.replace("__MODE__", mode), 0o755)
    return path


def _run_gate(gate: Path, census: Path, output: Path, scratch: Path, extra=()):
    return subprocess.run(
        [sys.executable, str(gate),
         "--census", str(census),
         "--output", str(output),
         "--scratch", str(scratch),
         *extra],
        capture_output=True, text=True, timeout=600,
    )


def _run_gate_argv(gate: Path, argv):
    return subprocess.run(
        [sys.executable, str(gate), *argv],
        capture_output=True, text=True, timeout=600,
    )


def _tree_state(root: Path):
    try:
        return sorted(str(p.relative_to(root)) for p in root.rglob("*"))
    except OSError:
        return ["<unreadable>"]


def _case(manifest: dict, case_id: str) -> dict:
    return next(c for c in manifest["cases"] if c["id"] == case_id)


def _assertion_ok(manifest: dict, case_id: str, assertion_id: str) -> bool:
    case = _case(manifest, case_id)
    return any(a["id"] == assertion_id and a["ok"] for a in case["assertions"])


def _assertion_failed(manifest: dict, case_id: str, assertion_id: str) -> bool:
    case = _case(manifest, case_id)
    return any(a["id"] == assertion_id and not a["ok"] for a in case["assertions"])


def _assertion_matching(manifest: dict, case_id: str, prefix: str, ok: bool) -> bool:
    case = _case(manifest, case_id)
    return any(a["id"].startswith(prefix) and a["ok"] == ok for a in case["assertions"])


def _selftest_parent(scratch_parent: str) -> tuple[Path | None, str | None]:
    if scratch_parent:
        parent = Path(scratch_parent).expanduser().resolve()
    else:
        tmp = os.environ.get("TMPDIR", "").strip()
        if not tmp:
            return None, "selftest needs --scratch DIR or TMPDIR (no /tmp fallback)"
        parent = Path(tmp).expanduser().resolve()
    for forbidden in TMP_ROOTS:
        if _within(parent, forbidden):
            return None, f"selftest temp parent may not live under {forbidden}: {parent}"
    return parent, None


def run_selftest(scratch_parent: str, keep_scratch: bool = False) -> int:
    gate = Path(__file__).resolve()
    parent, parent_err = _selftest_parent(scratch_parent)
    if parent_err:
        print(f"mori-round17-jj-regressions: setup: {parent_err}", file=sys.stderr)
        return 2
    roots = _repo_roots([gate.parent, Path.cwd()])
    overlap = _protected_error(parent, "--scratch", roots, [], gate)
    if overlap:
        print(f"mori-round17-jj-regressions: setup: {overlap}", file=sys.stderr)
        return 2
    parent.mkdir(parents=True, exist_ok=True)
    if parent.is_symlink() or not parent.is_dir():
        print(f"mori-round17-jj-regressions: setup: selftest parent is not a real directory: {parent}",
              file=sys.stderr)
        return 2
    work = Path(tempfile.mkdtemp(prefix="mori-r17-jj-selftest-", dir=str(parent)))
    checks = []
    failures = []

    def expect(label, ok, detail=""):
        if ok:
            checks.append(label)
        else:
            failures.append(f"{label}{(': ' + detail) if detail else ''}")

    try:
        # --- isolated guard arms: pure checks over a synthetic repo tree ---
        fake = work / "fake-repo"
        for name in ("tools", "corpus", ".git", ".jj", ".ufo/state", ".ufo/waves/evidence"):
            (fake / name).mkdir(parents=True, exist_ok=True)
        fake_census = fake / "tools" / "census.sh"
        write(fake_census, "#!/bin/sh\nexit 0\n", 0o755)
        fake_gate = fake / "tools" / "gate.py"
        write(fake_gate, "")
        fake_roots = [fake]
        fake_inputs = [fake_census]
        out_probe = work / "guard-out"

        expect("guard_output_repo_root",
               _protected_error(fake, "--output", fake_roots, [], fake_gate) is not None)
        for name in PROTECTED_DIRS:
            expect(f"guard_output_{name.strip('.')}",
                   check_output_path(fake / name / "out", fake_roots, fake_inputs, fake_gate) is not None)
        expect("guard_output_dotufo",
               check_output_path(fake / ".ufo" / "state" / "out",
                                 fake_roots, fake_inputs, fake_gate) is not None)
        expect("guard_output_waves_allowed",
               check_output_path(fake / ".ufo" / "waves" / "evidence" / "out",
                                 fake_roots, fake_inputs, fake_gate) is None)
        nonempty = work / "nonempty"
        nonempty.mkdir()
        write(nonempty / "artifact", "x")
        expect("guard_output_nonempty",
               check_output_path(nonempty, fake_roots, fake_inputs, fake_gate) is not None)
        link = work / "outlink"
        link.symlink_to(fake / ".ufo" / "waves")
        expect("guard_output_symlink",
               check_output_path(link, fake_roots, fake_inputs, fake_gate) is not None)
        linkdir = work / "linkdir"
        linkdir.symlink_to(fake / ".ufo" / "waves")
        expect("guard_output_ancestor_symlink",
               check_output_path(linkdir / "out", fake_roots, fake_inputs, fake_gate) is not None)
        expect("guard_scratch_ancestor_symlink",
               check_scratch_path(linkdir / "tmp", fake_roots, fake_inputs,
                                  fake_gate, out_probe) is not None)
        ancestor = work / "ancestor"
        ancestor.mkdir()
        ancestor_repo = ancestor / "repo"
        (ancestor_repo / ".git").mkdir(parents=True)
        expect("guard_output_ancestor",
               _protected_error(ancestor, "--output", [ancestor_repo], [], fake_gate) is not None)
        gate_src = work / "gate-src"
        gate_src.mkdir()
        gate_file = gate_src / "gate.py"
        write(gate_file, "")
        expect("guard_output_gate_source",
               _protected_error(gate_src, "--output", [], [], gate_file) is not None)
        expect("guard_scratch_tools",
               check_scratch_path(fake / "tools" / "tmp",
                                  fake_roots, fake_inputs, fake_gate, out_probe) is not None)
        expect("guard_scratch_input_file",
               check_scratch_path(fake_census,
                                  fake_roots, fake_inputs, fake_gate, out_probe) is not None)
        input_dir = work / "inputs"
        input_dir.mkdir()
        input_census = input_dir / "census.sh"
        write(input_census, "")
        expect("guard_scratch_input_ancestor",
               check_scratch_path(input_dir, [], [input_census], fake_gate, out_probe) is not None)
        expect("guard_scratch_tmp",
               check_scratch_path(Path("/tmp") / "jj-gate-selftest",
                                  fake_roots, fake_inputs, fake_gate, out_probe) is not None)
        expect("guard_scratch_ok",
               check_scratch_path(work / "scratch-ok",
                                  fake_roots, fake_inputs, fake_gate, out_probe) is None)

        # --- compliant fixture: green, exact receipt fields, cleaned scratch ---
        ok_census = write_fixture_census(work, "ok")
        head_census = write_fixture_census(work, "head")
        wrongtip_census = write_fixture_census(work, "wrongtip")
        absent_census = work / "absent-census.sh"

        # Raw --output/--scratch symlink arguments must be rejected BEFORE
        # resolve(), and the sentinel target must stay byte-identical (the
        # SandboxFinal residual: resolving first erased the symlink evidence).
        sentinel = work / "sentinel-empty"
        sentinel.mkdir()
        out_link = work / "out-link"
        out_link.symlink_to(sentinel)
        before = _tree_state(sentinel)
        proc = _run_gate_argv(gate, ["--census", str(ok_census),
                                     "--output", str(out_link)])
        expect("argv_output_symlink_rc2", proc.returncode == 2, f"rc={proc.returncode}")
        expect("argv_output_symlink_target_unchanged", _tree_state(sentinel) == before)

        nested_link = work / "nested-link"
        nested_link.symlink_to(sentinel)
        before = _tree_state(sentinel)
        proc = _run_gate_argv(gate, ["--census", str(ok_census),
                                     "--output", str(nested_link / "newout")])
        expect("argv_output_nested_symlink_rc2", proc.returncode == 2, f"rc={proc.returncode}")
        expect("argv_output_nested_symlink_target_unchanged", _tree_state(sentinel) == before)

        scratch_link = work / "scratch-link"
        scratch_link.symlink_to(sentinel)
        out_guard = work / "out-guard-scratch"
        before = _tree_state(sentinel)
        proc = _run_gate_argv(gate, ["--census", str(ok_census),
                                     "--output", str(out_guard),
                                     "--scratch", str(scratch_link)])
        expect("argv_scratch_symlink_rc2", proc.returncode == 2, f"rc={proc.returncode}")
        expect("argv_scratch_symlink_target_unchanged", _tree_state(sentinel) == before)
        expect("argv_scratch_symlink_output_untouched", not out_guard.exists())

        out_ok = work / "out-ok"
        proc = _run_gate(gate, ok_census, out_ok, work / "scratch-ok-run")
        manifest_ok = json.loads((out_ok / "run-manifest.json").read_text(encoding="utf-8"))
        expect("ok_rc0", proc.returncode == 0,
               f"rc={proc.returncode} {proc.stdout.strip()} {proc.stderr.strip()}")
        expect("ok_cases", manifest_ok["totals"]["cases"] == len(CASES),
               f"cases={manifest_ok['totals']['cases']}")
        expect("ok_failed_zero", manifest_ok["totals"]["failed_assertions"] == 0,
               f"failed={manifest_ok['totals']['failed_assertions']}")
        expect("ok_mismatch_finding",
               _assertion_ok(manifest_ok, "jj-commit-no-bookmark",
                             f"finding:{FINDING_MISMATCH}:present"))
        expect("ok_mismatch_severity",
               _assertion_ok(manifest_ok, "jj-commit-no-bookmark",
                             f"finding:{FINDING_MISMATCH}:severity"))
        expect("ok_exact_head",
               _assertion_matching(manifest_ok, "jj-commit-no-bookmark",
                                   f"finding:{FINDING_MISMATCH}:obs_token:head=", True))
        expect("ok_exact_branch_tip",
               _assertion_matching(manifest_ok, "jj-commit-no-bookmark",
                                   f"finding:{FINDING_MISMATCH}:obs_token:branch_tip=", True))
        expect("ok_mismatch_basis",
               _assertion_ok(manifest_ok, "jj-commit-no-bookmark",
                             f"finding:{FINDING_MISMATCH}:obs_token:basis=merge-base-not-ancestor"))
        expect("ok_author_finding",
               _assertion_ok(manifest_ok, "jj-ambient-author",
                             f"finding:{FINDING_AUTHOR}:present"))
        expect("ok_author_count",
               _assertion_ok(manifest_ok, "jj-ambient-author",
                             f"finding:{FINDING_AUTHOR}:obs_token:count=1"))
        expect("ok_sibling_negative",
               _assertion_ok(manifest_ok, "jj-sibling-author", f"finding:{FINDING_AUTHOR}:absent"))
        expect("ok_fallback_head",
               _assertion_ok(manifest_ok, "git-fallback-head", "lane_basis")
               and _assertion_ok(manifest_ok, "git-fallback-head",
                                 f"finding:{FINDING_MISMATCH}:absent"))
        expect("ok_retained_false", manifest_ok.get("retained") is False,
               f"retained={manifest_ok.get('retained')!r}")
        scratch_run_ok = manifest_ok.get("scratch_run") or ""
        expect("ok_scratch_removed",
               scratch_run_ok != "" and not os.path.lexists(scratch_run_ok))

        # --keep-scratch: forensic retention is opt-in and recorded.
        out_keep = work / "out-keep"
        proc = _run_gate(gate, ok_census, out_keep, work / "scratch-keep",
                         extra=["--keep-scratch"])
        manifest_keep = json.loads((out_keep / "run-manifest.json").read_text(encoding="utf-8"))
        expect("keep_rc0", proc.returncode == 0, f"rc={proc.returncode}")
        expect("keep_retained_true", manifest_keep.get("retained") is True,
               f"retained={manifest_keep.get('retained')!r}")
        expect("keep_scratch_present",
               bool(manifest_keep.get("scratch_run"))
               and os.path.isdir(manifest_keep["scratch_run"]))

        # --- exact-field mutant: branch_tip= one character short is red ---
        out_wrong = work / "out-wrongtip"
        proc = _run_gate(gate, wrongtip_census, out_wrong, work / "scratch-wrongtip")
        manifest_wrong = json.loads((out_wrong / "run-manifest.json").read_text(encoding="utf-8"))
        expect("wrongtip_rc1", proc.returncode == 1, f"rc={proc.returncode}")
        expect("wrongtip_names_branch_tip",
               _assertion_matching(manifest_wrong, "jj-commit-no-bookmark",
                                   f"finding:{FINDING_MISMATCH}:obs_token:branch_tip=", False))

        # --- entering mutant: same universe, red on the missing finding ---
        out_head = work / "out-head"
        proc = _run_gate(gate, head_census, out_head, work / "scratch-head")
        manifest_head = json.loads((out_head / "run-manifest.json").read_text(encoding="utf-8"))
        expect("head_rc1", proc.returncode == 1, f"rc={proc.returncode}")
        expect("head_names_missing_mismatch",
               _assertion_failed(manifest_head, "jj-commit-no-bookmark",
                                 f"finding:{FINDING_MISMATCH}:present"))
        expect("head_failed_assertions", manifest_head["totals"]["failed_assertions"] > 0,
               f"failed={manifest_head['totals']['failed_assertions']}")

        # The before/after denominator must be identical (ReceiptC2Controls Q1).
        expect("same_assertion_universe",
               manifest_ok["totals"]["assertions"] == manifest_head["totals"]["assertions"]
               == manifest_wrong["totals"]["assertions"],
               f"ok={manifest_ok['totals']['assertions']} "
               f"head={manifest_head['totals']['assertions']} "
               f"wrongtip={manifest_wrong['totals']['assertions']}")

        out_absent = work / "out-absent"
        proc = _run_gate(gate, absent_census, out_absent, work / "scratch-absent")
        manifest_absent = json.loads((out_absent / "run-manifest.json").read_text(encoding="utf-8"))
        expect("absent_rc1", proc.returncode == 1, f"rc={proc.returncode}")
        expect("absent_capability_absent",
               all(c["status"] == "capability_absent" for c in manifest_absent["cases"]))
    finally:
        if keep_scratch:
            print(f"SELFTEST kept: {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)

    if failures:
        print("SELFTEST FAIL: " + "; ".join(failures))
        return 1
    print("SELFTEST ok: " + ",".join(checks))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="mori-round17-jj-regressions.py",
        description="C2 jj-colocation regression gate for tools/mori-census.sh",
    )
    parser.add_argument("--census", help="path to mori-census.sh (required unless --selftest)")
    parser.add_argument("--output", help="directory for run-manifest.json and case outputs (required unless --selftest)")
    parser.add_argument(
        "--scratch",
        default="",
        help="sandbox tree (default: <output>/scratch; with --selftest, the selftest temp parent). "
             "Must not be /tmp, /var/tmp, or overlap a repo root, tools/, corpus/, .git/, .jj/, "
             "the census input, or the output artifacts.",
    )
    parser.add_argument(
        "--keep-scratch",
        action="store_true",
        help="retain the fresh per-run sandbox tree for forensics (manifest retained=true); "
             "the default removes only the run tree this invocation created",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="isolated fixture proof of this gate (compliant/HEAD/wrongtip fixture censuses, "
             "output/scratch guard arms); no live census needed",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest(args.scratch, args.keep_scratch)
    if not args.census:
        parser.error("--census is required unless --selftest")
    if not args.output:
        parser.error("--output is required unless --selftest")

    gate_path = Path(__file__).resolve()
    census = Path(args.census).expanduser().resolve()

    # RAW paths: no resolve() before the guard. resolve() follows a symlink and
    # would erase the evidence the no-symlink rule needs (SandboxFinal
    # residual). Relative args are anchored at cwd WITHOUT normalising '..'.
    raw_output = Path(args.output).expanduser()
    if not raw_output.is_absolute():
        raw_output = Path.cwd() / raw_output
    raw_scratch = Path(args.scratch).expanduser() if args.scratch else raw_output / "scratch"
    if not raw_scratch.is_absolute():
        raw_scratch = Path.cwd() / raw_scratch

    roots = _repo_roots([gate_path.parent, Path.cwd(), census.parent])
    inputs = [census]

    # Raw path + existing-ancestor symlink checks run BEFORE resolve/mkdir;
    # only then are the canonical containment guards applied.
    guard_err = check_output_path(raw_output, roots, inputs, gate_path)
    if guard_err:
        print(f"mori-round17-jj-regressions: setup: {guard_err}", file=sys.stderr)
        return 2
    guard_err = check_scratch_path(raw_scratch, roots, inputs, gate_path, raw_output)
    if guard_err:
        print(f"mori-round17-jj-regressions: setup: {guard_err}", file=sys.stderr)
        return 2

    output = _canonical(raw_output)
    scratch = _canonical(raw_scratch)

    try:
        tools = resolve_tools(args)
    except RuntimeError as exc:
        print(f"mori-round17-jj-regressions: setup: {exc}", file=sys.stderr)
        return 2

    try:
        output.mkdir(parents=True, exist_ok=True)
        if output.is_symlink() or not output.is_dir():
            raise RuntimeError(f"--output changed type during creation: {output}")
        cases_out = output / "cases"
        cases_out.mkdir(parents=True, exist_ok=True)
        scratch.mkdir(parents=True, exist_ok=True)
        if scratch.is_symlink() or not scratch.is_dir():
            raise RuntimeError(f"--scratch changed type during creation: {scratch}")
        run_dir = make_run_dir(scratch)
    except (OSError, RuntimeError) as exc:
        print(f"mori-round17-jj-regressions: setup: {exc}", file=sys.stderr)
        return 2

    census_present = census.is_file() and os.access(census, os.R_OK)
    census_bytes = census.read_bytes() if census_present else b""
    census_sha = sha256_bytes(census_bytes) if census_present else ""

    now = int(time.time()) + 120

    try:
        gate_sha = sha256_bytes(gate_path.read_bytes())
    except OSError:
        gate_sha = "unavailable"

    keep_scratch = bool(args.keep_scratch)
    manifest = {
        "schema": SCHEMA,
        "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gate": {"path": str(gate_path), "sha256": gate_sha},
        "census": {
            "path": str(census),
            "present": census_present,
            "sha256": census_sha,
        },
        "tools": {
            "git": {"path": tools["git"], "version": tool_version([tools["git"], "--version"])},
            "jj": {
                "path": tools["jj"] or None,
                "version": tool_version([tools["jj"], "--version"]) if tools["jj"] else "absent",
            },
            "bash": {"path": tools["bash"]},
            "jq": tools["jq"] or None,
            "timeout": tools["timeout"],
        },
        "scratch_run": str(run_dir),
        "retained": None,
        "retention": {},
        "environment": {
            "HOME": "redirected per case into <case>/home",
            "XDG_CONFIG_HOME": "redirected per case into <case>/home/.config",
            "JJ_CONFIG": "redirected per case into <case>/home/jjconfig.toml",
            "GIT_CONFIG_GLOBAL": "redirected per case into <case>/home/gitconfig",
            "census": "run with the census override environment; morphic stubs answer pgrep, df, journalctl and tmux; MORI_CGROUP_CURRENT is outside /sys/fs/cgroup and is refused unread",
        },
        "cases": [],
        "totals": {},
    }

    case_results = []
    run_error = None

    try:
        for case_id, description, setup in CASES:
            case_dir = run_dir / case_id
            needs_jj = case_id.startswith("jj-")
            # A non-retained run's sandbox paths are removed below, so the
            # manifest records them only when forensic retention was requested.
            sandbox_field = str(case_dir) if keep_scratch else None

            if not census_present:
                case_results.append(manifest_case(
                    case_id, description, "capability_absent",
                    [{"id": "census_present", "ok": False,
                      "detail": f"missing or unreadable: {census}"}],
                    sandbox=sandbox_field,
                ))
                continue

            if needs_jj and not tools["jj"]:
                case_results.append(manifest_case(
                    case_id, description, "capability_absent",
                    [{"id": "jj_present", "ok": False,
                      "detail": "no executable jj at ~/.local/bin/jj or PATH"}],
                    sandbox=sandbox_field,
                ))
                continue

            try:
                sb = build_sandbox(case_dir, now, tools)
                sb["jj"] = tools["jj"] if needs_jj else ""
                expect = setup(sb, tools)
                refs_before = refs_snapshot(sb)
            except Exception as exc:  # setup is our own fixture, never the census
                case_results.append(manifest_case(
                    case_id, description, "setup_failed",
                    [{"id": "sandbox_build", "ok": False, "detail": str(exc)}],
                    sandbox=sandbox_field,
                ))
                continue

            outcome = evaluate(sb, census, expect, refs_before)
            res = outcome["result"]
            text = outcome["text"]
            out_file = cases_out / f"{case_id}.out"
            write(out_file, text)

            parsed = outcome["parsed"]
            status = "match" if outcome["failed_assertions"] == 0 else "mismatch"
            observed = {
                "state": parsed["state"],
                "basis": parsed["basis"],
                "roll": parsed["verdict"],
                "rc": res["rc"],
                "findings": [
                    {"id": f["id"], "severity": f["severity"]} for f in parsed["findings"]
                ],
                "verdict_fields": parsed["verdict_fields"],
                "refs": outcome["refs_after"],
            }
            case_results.append(manifest_case(
                case_id,
                description,
                status,
                outcome["checks"],
                observed=observed,
                output_file=str(out_file.relative_to(output)),
                sandbox=sandbox_field,
                census_command=res["argv"],
                census_sha=sha256_text(text),
            ))
    except Exception as exc:
        run_error = f"{type(exc).__name__}: {exc}"

    manifest["cases"] = case_results
    total_assertions = sum(len(c["assertions"]) for c in case_results)
    failed_assertions = sum(c["failed_assertions"] for c in case_results)
    failed_cases = sum(1 for c in case_results if c["failed_assertions"] > 0)
    statuses = {}
    for case in case_results:
        statuses[case["status"]] = statuses.get(case["status"], 0) + 1
    manifest["totals"] = {
        "cases": len(case_results),
        "match": statuses.get("match", 0),
        "mismatch": statuses.get("mismatch", 0),
        "capability_absent": statuses.get("capability_absent", 0),
        "setup_failed": statuses.get("setup_failed", 0),
        "assertions": total_assertions,
        "failed_assertions": failed_assertions,
        "failed_cases": failed_cases,
    }
    manifest["failed"] = failed_assertions
    if run_error:
        manifest["error"] = run_error

    # F4 retention policy: the fresh run tree is removed unless forensics were
    # requested. Only the child created above is ever removed -- never output,
    # the scratch parent, or anything else.
    retained = keep_scratch
    cleanup = "kept" if retained else "removed"
    if not retained:
        shutil.rmtree(run_dir, ignore_errors=True)
        if os.path.lexists(run_dir):
            retained = True
            cleanup = "failed"
            manifest["cleanup_error"] = f"could not remove {run_dir}"
    manifest["retained"] = retained
    manifest["retention"] = {
        "policy": "keep" if keep_scratch else "cleanup",
        "cleanup": cleanup,
        "scratch_run": str(run_dir),
    }

    manifest_path = output / "run-manifest.json"
    try:
        write(manifest_path, json.dumps(manifest, indent=2, sort_keys=False) + "\n")
    except OSError as exc:
        print(f"mori-round17-jj-regressions: setup: cannot write manifest: {exc}",
              file=sys.stderr)
        return 2

    print(
        f"mori-round17-jj-regressions: cases={len(case_results)} "
        f"match={statuses.get('match', 0)} mismatch={statuses.get('mismatch', 0)} "
        f"capability_absent={statuses.get('capability_absent', 0)} "
        f"setup_failed={statuses.get('setup_failed', 0)} "
        f"assertions={total_assertions} failed={failed_assertions} "
        f"retained={retained}"
    )
    print(f"manifest: {manifest_path}")

    if run_error:
        return 2
    return 0 if failed_assertions == 0 and failed_cases == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
