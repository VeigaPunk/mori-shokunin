#!/usr/bin/env python3
"""mori round-17 C2 gate: jj-colocation correctness of tools/mori-census.sh.

Contract (round-17 contract.md, C2):
  * the census resolves the lane branch like scripts/hyaku/jj-lane.sh
    detect_branch (symbolic-ref HEAD -> refs/remotes/origin/HEAD -> the unique
    of refs/heads/master / refs/heads/main) and queries refs/heads/<branch>
    instead of HEAD for report closure (row 6) and authorship (row 9);
  * HEAD_BRANCH_MISMATCH (severity warn, global drift) when HEAD resolves and
    `merge-base --is-ancestor HEAD refs/heads/<branch>` fails;
  * LANE_AUTHOR_MISMATCH (severity warn, global drift) for a post-launch commit
    on the branch whose committer is <lane>-shokunin <lane>@shokunin.local while
    the author email does NOT end in @shokunin.local (the A1 amendment: a
    sibling-shokunin author such as kengaku@shokunin.local is legitimate and is
    a required negative control);
  * a missing branch-resolver input falls back to the unchanged HEAD behavior.

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
  mori-round17-jj-regressions.py --census PATH --output DIR [--scratch DIR]
  mori-round17-jj-regressions.py --selftest [--scratch DIR]

The 12 cases cover: plain git progress; detached at tip; detached ahead
(plain git commit); detached behind; report on-branch closure; report only
off-branch (not closed); foreign author+committer; helper-shaped jj commit
(metaedit --update-author, commit, bookmark set); jj commit without bookmark
move; ambient author + lane committer; sibling-shokunin author + lane
committer (negative control); and no-resolver-input HEAD fallback.

Writes DIR/run-manifest.json (per-case assertions, failed count) and
DIR/cases/<id>.out (the exact census stream). Exit 0 = every assertion held;
1 = at least one failed assertion or a capability gap; 2 = gate setup error.

--selftest needs no live census: it runs the gate over a dormant fixture census
(MODE=ok, the amended contract) and over a HEAD-only mutant (MODE=head), then
over a missing census, and asserts exit codes plus the stable finding ids
HEAD_BRANCH_MISMATCH / LANE_AUTHOR_MISMATCH. Its temp tree is created under
--scratch when given (never required to be /tmp).
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


def git_short(repo: Path, rev: str, env) -> str:
    res = git(repo, ["rev-parse", "--short", rev], env)
    return res["stdout"].strip() if res["rc"] == 0 else ""


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
        snap[label] = {
            "head": git_rev(repo, "HEAD", env),
            "branch": git_rev(repo, f"refs/heads/{BRANCH}", env),
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


def mismatch_requirement(sb: dict) -> dict:
    env = sb["tool_env"]
    head_short = git_short(sb["lane"], "HEAD", env)
    branch_short = git_short(sb["lane"], f"refs/heads/{BRANCH}", env)
    return {
        "id": FINDING_MISMATCH,
        "severity_exact": "warn",
        "obs_contains": [f"lane={LANE}", head_short, branch_short],
    }


def author_requirement() -> dict:
    return {
        "id": FINDING_AUTHOR,
        "severity_exact": "warn",
        "obs_contains": [f"lane={LANE}"],
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


def case_jj_sibling_author(sb, tools):
    """Kengaku-style negative control: committer lane, author a sibling lane.

    The amended A1 rule only fires when the author email does NOT end in
    @shokunin.local, so a legitimate sibling-shokunin author must stay quiet.
    """
    jj = tools["jj"]
    env = sb["tool_env"]
    lane = sb["lane"]
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
    ("jj-sibling-author", "sibling-shokunin author + lane committer -> no LANE_AUTHOR_MISMATCH (negative control)", case_jj_sibling_author),
    ("git-fallback-head", "no resolver input (branch trunk, detached) -> unchanged HEAD grading", case_git_fallback_head),
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
    check("refs_unchanged", refs_before == refs_after,
          f"before={json.dumps(refs_before, sort_keys=True)} after={json.dumps(refs_after, sort_keys=True)}")

    by_id = {}
    for finding in parsed["findings"]:
        by_id.setdefault(finding["id"], finding)

    for requirement in expect["require"]:
        fid = requirement["id"]
        present = fid in by_id
        check(f"finding:{fid}:present", present, f"findings={sorted(by_id)}")
        if not present:
            continue
        finding = by_id[fid]
        if requirement.get("severity_exact"):
            check(
                f"finding:{fid}:severity",
                finding["severity"] == requirement["severity_exact"],
                f"severity={finding['severity']} expected={requirement['severity_exact']}",
            )
        for needle in requirement.get("obs_contains", []):
            check(
                f"finding:{fid}:obs_contains:{needle}",
                needle in finding["obs"],
                f"obs={finding['obs']}",
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
# selftest (PROTOCOL gate standard: isolated fixtures, stable finding ids)
# ---------------------------------------------------------------------------
#
# Two dormant fixture censuses exercise the gate itself, never a live census:
#   MODE=ok    the amended C2 contract (branch-anchored rows 6/9, both warn
#              findings, sibling-author negative arm, HEAD fallback when the
#              resolver has no input);
#   MODE=head  the entering behavior (bare HEAD, no C2 findings), used as the
#              mutant: the gate MUST turn red and name the missing finding.
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

resolve_branch() {
  local dir=$1 b ref
  local -a c=()
  b=$(git -C "$dir" symbolic-ref -q HEAD 2>/dev/null || true)
  case $b in refs/heads/*) printf '%s\n' "${b#refs/heads/}"; return 0 ;; esac
  ref=$(git -C "$dir" symbolic-ref -q refs/remotes/origin/HEAD 2>/dev/null || true)
  case $ref in refs/remotes/origin/*) printf '%s\n' "${ref#refs/remotes/origin/}"; return 0 ;; esac
  git -C "$dir" show-ref -q --verify refs/heads/master 2>/dev/null && c+=(master)
  git -C "$dir" show-ref -q --verify refs/heads/main 2>/dev/null && c+=(main)
  [ "${#c[@]}" -eq 1 ] && { printf '%s\n' "${c[0]}"; return 0; }
  return 1
}

branch=$(resolve_branch "$REPO" || true)
[ "$MODE" = head ] && branch=''
head=$(git -C "$REPO" rev-parse --verify -q HEAD 2>/dev/null || true)
state=unavailable
basis=row-1
round='-'
launch_ep='-'
age='-'
anchor=$(grep -E " launch $LANE round=" "$LEDGER" 2>/dev/null | tail -n 1 || true)
if [ -z "$anchor" ]; then
  state=not-open
  basis=row-2
else
  round=$(printf '%s\n' "$anchor" | awk '{for (i = 1; i <= NF; i++) if ($i ~ /^round=/) { v = $i; sub(/^round=/, "", v); print v; exit }}')
  launch_ts=$(printf '%s\n' "$anchor" | awk '{print $1; exit}')
  launch_ep=$(date -u -d "$launch_ts" +%s 2>/dev/null || true)
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
      ref=HEAD
      [ -n "$branch" ] && ref="refs/heads/$branch"
      rpath=".ufo/reports/round-$round/$LANE.md"
      closed=0
      if git -C "$ROOT" cat-file -e "$ref:$rpath" 2>/dev/null; then
        ct=$(git -C "$ROOT" log -1 --format=%ct "$ref" -- "$rpath" 2>/dev/null || true)
        if [ -n "$ct" ] && [ "$ct" -gt "$launch_ep" ] && [ "$ct" -le "$NOW" ]; then closed=1; fi
      fi
      if [ "$closed" -eq 1 ]; then
        state=not-open
        basis=row-6
      else
        subj=0
        sib=0
        if [ -n "$head" ]; then
          lg=$(git -C "$REPO" log --since="@$launch_ep" --format='%ct %an <%ae>' "$ref" 2>/dev/null || true)
          inwin=$(awk -v lo="$launch_ep" -v hi="$NOW" '$1 ~ /^[0-9]+$/ && $1 + 0 > lo + 0 && $1 + 0 <= hi + 0' <<< "$lg")
          if [ -n "$inwin" ]; then
            authors=$(awk '{ sub(/^[0-9]+ /, ""); print }' <<< "$inwin")
            case $'\n'"$authors"$'\n' in
              *$'\n'"$LANE-shokunin <$LANE@shokunin.local>"$'\n'*) subj=1 ;;
              *) sib=1 ;;
            esac
          fi
          if [ -n "$branch" ]; then
            btip=$(git -C "$REPO" rev-parse --verify -q "refs/heads/$branch" 2>/dev/null || true)
            if [ -n "$btip" ] && ! git -C "$REPO" merge-base --is-ancestor "$head" "refs/heads/$branch" 2>/dev/null; then
              hshort=$(git -C "$REPO" rev-parse --short "$head" 2>/dev/null || true)
              bshort=$(git -C "$REPO" rev-parse --short "$btip" 2>/dev/null || true)
              emit_finding HEAD_BRANCH_MISMATCH "lane=$LANE head=$hshort branch=$branch branch_tip=$bshort"
            fi
          fi
          if [ "$MODE" = ok ]; then
            am=$(git -C "$REPO" log --since="@$launch_ep" --format='%ct|%an|%ae|%cn|%ce' "$ref" 2>/dev/null \
              | awk -F'|' -v lo="$launch_ep" -v hi="$NOW" \
                '$1 ~ /^[0-9]+$/ && $1 + 0 > lo + 0 && $1 + 0 <= hi + 0 && $4 == "alpha-shokunin" && $5 == "alpha@shokunin.local" && $3 !~ /@shokunin[.]local$/ { n++ } END { print n + 0 }')
            case $am in ''|*[!0-9]*) am=0 ;; esac
            if [ "$am" -gt 0 ]; then emit_finding LANE_AUTHOR_MISMATCH "lane=$LANE commits=$am"; fi
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


def _run_gate(gate: Path, census: Path, output: Path, scratch: Path):
    return subprocess.run(
        [sys.executable, str(gate),
         "--census", str(census),
         "--output", str(output),
         "--scratch", str(scratch)],
        capture_output=True, text=True, timeout=600,
    )


def _case(manifest: dict, case_id: str) -> dict:
    return next(c for c in manifest["cases"] if c["id"] == case_id)


def _assertion_ok(manifest: dict, case_id: str, assertion_id: str) -> bool:
    case = _case(manifest, case_id)
    return any(a["id"] == assertion_id and a["ok"] for a in case["assertions"])


def _assertion_failed(manifest: dict, case_id: str, assertion_id: str) -> bool:
    case = _case(manifest, case_id)
    return any(a["id"] == assertion_id and not a["ok"] for a in case["assertions"])


def run_selftest(scratch_parent: str) -> int:
    gate = Path(__file__).resolve()
    parent = Path(scratch_parent).expanduser().resolve() if scratch_parent else None
    if parent is not None:
        parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(
        prefix="mori-r17-jj-selftest-",
        dir=str(parent) if parent is not None else None,
    ))
    checks = []
    failures = []

    def expect(label, ok, detail=""):
        if ok:
            checks.append(label)
        else:
            failures.append(f"{label}{(': ' + detail) if detail else ''}")

    try:
        ok_census = write_fixture_census(work, "ok")
        head_census = write_fixture_census(work, "head")
        absent_census = work / "absent-census.sh"

        out_ok = work / "out-ok"
        proc = _run_gate(gate, ok_census, out_ok, work / "scratch-ok")
        manifest = json.loads((out_ok / "run-manifest.json").read_text(encoding="utf-8"))
        expect("ok_rc0", proc.returncode == 0, f"rc={proc.returncode} {proc.stdout.strip()} {proc.stderr.strip()}")
        expect("ok_cases", manifest["totals"]["cases"] == len(CASES), f"cases={manifest['totals']['cases']}")
        expect("ok_failed_zero", manifest["totals"]["failed_assertions"] == 0,
               f"failed={manifest['totals']['failed_assertions']}")
        expect("ok_mismatch_finding",
               _assertion_ok(manifest, "jj-commit-no-bookmark", f"finding:{FINDING_MISMATCH}:present"))
        expect("ok_mismatch_severity",
               _assertion_ok(manifest, "jj-commit-no-bookmark", f"finding:{FINDING_MISMATCH}:severity"))
        expect("ok_author_finding",
               _assertion_ok(manifest, "jj-ambient-author", f"finding:{FINDING_AUTHOR}:present"))
        expect("ok_sibling_negative",
               _assertion_ok(manifest, "jj-sibling-author", f"finding:{FINDING_AUTHOR}:absent"))
        expect("ok_fallback_head",
               _assertion_ok(manifest, "git-fallback-head", "lane_basis")
               and _assertion_ok(manifest, "git-fallback-head", f"finding:{FINDING_MISMATCH}:absent"))

        out_head = work / "out-head"
        proc = _run_gate(gate, head_census, out_head, work / "scratch-head")
        manifest = json.loads((out_head / "run-manifest.json").read_text(encoding="utf-8"))
        expect("head_rc1", proc.returncode == 1, f"rc={proc.returncode}")
        expect("head_names_missing_mismatch",
               _assertion_failed(manifest, "jj-commit-no-bookmark", f"finding:{FINDING_MISMATCH}:present"))
        expect("head_failed_assertions", manifest["totals"]["failed_assertions"] > 0,
               f"failed={manifest['totals']['failed_assertions']}")

        out_absent = work / "out-absent"
        proc = _run_gate(gate, absent_census, out_absent, work / "scratch-absent")
        manifest = json.loads((out_absent / "run-manifest.json").read_text(encoding="utf-8"))
        expect("absent_rc1", proc.returncode == 1, f"rc={proc.returncode}")
        expect("absent_capability_absent",
               all(c["status"] == "capability_absent" for c in manifest["cases"]))
    finally:
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
        help="sandbox tree (default: <output>/scratch; with --selftest, the selftest temp parent)",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="isolated fixture proof of this gate (dormant fixture census + HEAD mutant); no live census needed",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest(args.scratch)
    if not args.census:
        parser.error("--census is required unless --selftest")
    if not args.output:
        parser.error("--output is required unless --selftest")

    output = Path(args.output).expanduser().resolve()
    census = Path(args.census).expanduser().resolve()
    scratch = Path(args.scratch).expanduser().resolve() if args.scratch else output / "scratch"

    try:
        output.mkdir(parents=True, exist_ok=True)
        cases_out = output / "cases"
        cases_out.mkdir(parents=True, exist_ok=True)
        run_stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = scratch / f"run-{run_stamp}-{os.getpid()}"
        run_dir.mkdir(parents=True, exist_ok=False)
    except OSError as exc:
        print(f"mori-round17-jj-regressions: setup: {exc}", file=sys.stderr)
        return 2

    try:
        tools = resolve_tools(args)
    except RuntimeError as exc:
        print(f"mori-round17-jj-regressions: setup: {exc}", file=sys.stderr)
        return 2

    census_present = census.is_file() and os.access(census, os.R_OK)
    census_bytes = census.read_bytes() if census_present else b""
    census_sha = sha256_bytes(census_bytes) if census_present else ""

    now = int(time.time()) + 120

    try:
        gate_sha = sha256_bytes(Path(__file__).resolve().read_bytes())
    except OSError:
        gate_sha = "unavailable"

    manifest = {
        "schema": SCHEMA,
        "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gate": {"path": str(Path(__file__).resolve()), "sha256": gate_sha},
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

    for case_id, description, setup in CASES:
        case_dir = run_dir / case_id
        needs_jj = case_id.startswith("jj-")

        if not census_present:
            case_results.append(manifest_case(
                case_id, description, "capability_absent",
                [{"id": "census_present", "ok": False, "detail": f"missing or unreadable: {census}"}],
                sandbox=str(case_dir),
            ))
            continue

        if needs_jj and not tools["jj"]:
            case_results.append(manifest_case(
                case_id, description, "capability_absent",
                [{"id": "jj_present", "ok": False, "detail": "no executable jj at ~/.local/bin/jj or PATH"}],
                sandbox=str(case_dir),
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
                sandbox=str(case_dir),
            ))
            continue

        outcome = evaluate(sb, census, expect, refs_before)
        res = outcome["result"]
        text = outcome["text"]
        out_file = cases_out / f"{case_id}.out"
        write(out_file, text)

        refs_after = outcome["refs_after"]
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
            "refs": refs_after,
        }
        case_results.append(manifest_case(
            case_id,
            description,
            status,
            outcome["checks"],
            observed=observed,
            output_file=str(out_file.relative_to(output)),
            sandbox=str(case_dir),
            census_command=res["argv"],
            census_sha=sha256_text(text),
        ))

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

    manifest_path = output / "run-manifest.json"
    write(manifest_path, json.dumps(manifest, indent=2, sort_keys=False) + "\n")

    print(
        f"mori-round17-jj-regressions: cases={len(case_results)} "
        f"match={statuses.get('match', 0)} mismatch={statuses.get('mismatch', 0)} "
        f"capability_absent={statuses.get('capability_absent', 0)} "
        f"setup_failed={statuses.get('setup_failed', 0)} "
        f"assertions={total_assertions} failed={failed_assertions}"
    )
    print(f"manifest: {manifest_path}")

    return 0 if failed_assertions == 0 and failed_cases == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
