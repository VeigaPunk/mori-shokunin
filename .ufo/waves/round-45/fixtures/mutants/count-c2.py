#!/usr/bin/env python3
"""mori round-45 C2 — registry-predicate counter (frozen instrument, P-C2).

Composes the gate-registry auditor and the write-scope arm into one verdict over
the bytes at --rev:

  auditor arm  `tools/mori-gate-registry.py --rev <rev> --repo <repo>
               --audit-all` (population mode, never a `--audit <path>` run) must
               print `mode=population`, `population_digest=`, `tables=
               registered= unregistered= no_selftest= duplicate= wrong_row=`;
               `tables` must reach the measured floor of 7, the auditor's buckets
               must partition the declared population (`registered` equals the
               member count once `unregistered=0` and `no_selftest=0`), and the
               auditor's own `--selftest` tally must be green. Against the v1 CLI
               (round 44, which refuses `--audit-all`) the per-path `--audit`
               fallback is a narrowed measurement only: `auditor_mode` fails, so
               a narrowed audit can never score C2.

  scope arm    for every entry of `--write-scope` (repo-relative, contained in
               the repo root) whose declared scope is checkable (the path
               resolves at --rev and the entry carries an argv), the
               instrument's own `--selftest` runs inside a sandbox copy under
               `$TMPDIR`; a pre/post digest of the copied tree plus a listing of
               everything created outside that sandbox TMPDIR is compared with
               the entry's `expect`. A disagreement is `writescope_mismatch`.

  mutant arm   `<--mutants-dir>/<basename of this counter>` at `--rev` must be
               killed by this counter's own `--selftest` (exit 1, fail>=1). The
               mutant is read at the measured revision, never the worktree;
               absolute or `..` path arguments fail with `C2_SETUP`.

  trust        every subprocess inherits an env scrubbed of `GIT_*` and
               `MORI_GATE_REGISTRY`: `--repo` and `--auditor` cannot be
               retargeted from the caller's environment.

Usage:
  python3 count-c2.py <rev|WORK> [<--rev REV>] [--repo PATH] [--auditor PATH]
                      [--write-scope PATH] [--mutants-dir DIR] [--timeout S]
  python3 count-c2.py --selftest

Exit: 0 `C2=met` · 1 `C2=unmet` · 2 `C2_SETUP` (usage, unresolvable revision,
timeout, unreadable fixture).

Predicate: .ufo/waves/round-45/contract.md P-C2.
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile

AUDITOR_REL = "tools/mori-gate-registry.py"
WRITESCOPE_REL = ".ufo/waves/round-45/fixtures/write-scope.json"
MUTANTS_REL = ".ufo/waves/round-45/fixtures/mutants"
COUNTER_KEYS = ("tables", "registered", "unregistered", "no_selftest",
                "duplicate", "wrong_row")
VERDICT_KEYS = COUNTER_KEYS + ("writescope_mismatch",)

# P-C2 correction 1: seven eight-cell tables exist at the measured revision
# (SKILL.md headers 162/524/588/643/718/796/881), so the floor is 7, not 2.
TABLE_FLOOR = 7

# P-C2 item 5: the declared population — `tools/*.py`, `tools/*.sh` and the
# round counters `.ufo/waves/round-4[45]/count-c*.py`.
POP = (re.compile(r"^tools/[^/]+\.(?:py|sh)$"),
       re.compile(r"^\.ufo/waves/round-4[45]/count-c[^/]*\.py$"))

# The tree the instruments can reach inside the sandbox: the registry, the
# tools, the round directories that hold the counters. Historical waves are not
# copied (308 MB at the entering tip); a write to any of them from inside the
# sandbox would be a creation in this copy, which the digest counts.
SANDBOX_PATHS = ("SKILL.md", "corpus/README.md", "tools",
                 ".ufo/waves/round-44", ".ufo/waves/round-45")

TALLY = re.compile(r"pass=(\d+)\s+fail=(\d+)")
AUDIT_LINE = re.compile(r"^audit (\S+)\s+(PASS|FAIL) \((.*)\)$", re.M)


class Setup(Exception):
    pass


def repo_default():
    here = os.path.abspath(__file__)      # <repo>/.ufo/waves/round-45/count-c2.py
    d = os.path.dirname(here)
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        up = os.path.dirname(d)
        if up == d:
            return os.path.dirname(here)
        d = up


def child_env(**over):
    """A subprocess env with trust-boundary keys removed: every `GIT_*` (a
    `GIT_DIR` in the caller's env must not retarget `--repo`) and
    `MORI_GATE_REGISTRY` (the auditor path is `--auditor` only; nothing a child
    inherits may substitute another auditor)."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k != "MORI_GATE_REGISTRY"}
    env.update({k: v for k, v in over.items() if v is not None})
    return env


def run(argv, timeout, cwd=None, env=None):
    """Text-mode subprocess with a hard timeout; a timeout is C2_SETUP."""
    try:
        return subprocess.run(argv, capture_output=True, text=True,
                              timeout=timeout, cwd=cwd,
                              env=child_env() if env is None else env,
                              check=False)
    except subprocess.TimeoutExpired:
        raise Setup("timeout after %ss: %s" % (timeout, " ".join(argv[:4])))
    except OSError as exc:
        raise Setup("cannot run %s: %s" % (argv[0], exc))


def resolve_inside(repo, path):
    """Repo-relative path arguments only; absolute or escaping paths are setup
    errors, at WORK as at a revision (realpath prefix check)."""
    if os.path.isabs(path):
        raise Setup("path argument must be repo-relative: %s" % path)
    real_repo = os.path.realpath(repo)
    full = os.path.realpath(os.path.join(real_repo, path))
    if full != real_repo and not full.startswith(real_repo + os.sep):
        raise Setup("path argument escapes the repo: %s" % path)
    return full


def git(repo, args, timeout=30):
    return run(["git", "-C", repo] + args, timeout)


def exists_at(repo, rev, path):
    if rev == "WORK":
        return os.path.exists(os.path.join(repo, path))
    return git(repo, ["cat-file", "-e", "%s:%s" % (rev, path)]).returncode == 0


def read_at(repo, rev, path):
    if rev == "WORK":
        full = os.path.join(repo, path)
        if not os.path.isfile(full):
            return None
        with open(full, "rb") as fh:
            return fh.read()
    if not exists_at(repo, rev, path):
        return None
    got = git(repo, ["show", "%s:%s" % (rev, path)])
    if got.returncode != 0:
        raise Setup("git show failed for %s:%s" % (rev, path))
    return got.stdout.encode()


def population(repo, rev):
    """The declared population (P-C2 item 5) at the measured revision."""
    if rev == "WORK":
        names = []
        for d in ("tools", ".ufo/waves/round-44", ".ufo/waves/round-45"):
            full = os.path.join(repo, d)
            if os.path.isdir(full):
                names += [d + "/" + f for f in os.listdir(full)]
    else:
        got = git(repo, ["ls-tree", "-r", "--name-only", rev])
        if got.returncode != 0:
            raise Setup("git ls-tree failed for %s" % rev)
        names = got.stdout.splitlines()
    return sorted(n for n in names if any(p.match(n) for p in POP))


def tree_digest(root):
    """rel path -> sha256 (symlink target for links) over a directory."""
    digests = {}
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                digests[rel] = "link:" + os.readlink(full)
                continue
            h = hashlib.sha256()
            try:
                with open(full, "rb") as fh:
                    for chunk in iter(lambda: fh.read(1 << 20), b""):
                        h.update(chunk)
            except OSError as exc:
                digests[rel] = "unreadable:%s" % exc
                continue
            digests[rel] = h.hexdigest()
    return digests


ROUND_SCRATCH = os.path.join(".ufo", "waves", "round-45", "tmp")


def _work_ignore(repo, sandbox):
    """Never descend into scratch (any seat's) or into the sandbox being built."""
    scratch = os.path.realpath(tempfile.gettempdir())
    sandbox = os.path.realpath(sandbox)
    repo_real = os.path.realpath(repo)

    def ignore(directory, names):
        skip = set()
        for name in names:
            if name in (".git", "__pycache__"):
                skip.add(name)
                continue
            full = os.path.realpath(os.path.join(directory, name))
            rel = os.path.relpath(full, repo_real)
            if full == sandbox or full.startswith(sandbox + os.sep):
                skip.add(name)
            elif full == scratch or full.startswith(scratch + os.sep):
                skip.add(name)
            elif rel == ROUND_SCRATCH or rel.startswith(ROUND_SCRATCH + os.sep):
                skip.add(name)
        return skip

    return ignore


def materialize_tree(repo, rev, dest):
    """Copy the reachable tree at `rev` into `dest` (git archive; WORK: copy)."""
    if rev == "WORK":
        ignore = _work_ignore(repo, dest)
        for rel in SANDBOX_PATHS:
            src = os.path.join(repo, rel)
            try:
                if os.path.isfile(src):
                    os.makedirs(os.path.dirname(os.path.join(dest, rel)), exist_ok=True)
                    shutil.copy2(src, os.path.join(dest, rel))
                elif os.path.isdir(src):
                    shutil.copytree(src, os.path.join(dest, rel), dirs_exist_ok=True,
                                    ignore=ignore)
            except (OSError, RecursionError) as exc:
                raise Setup("cannot copy %s into the sandbox: %s" % (rel, exc))
        return
    paths = [p for p in SANDBOX_PATHS if exists_at(repo, rev, p)]
    if not paths:
        raise Setup("no sandbox path resolves at %s" % rev[:12])
    try:
        proc = subprocess.run(["git", "-C", repo, "archive", "--format=tar", rev,
                               "--"] + paths, capture_output=True, timeout=120,
                              env=child_env(), check=False)
    except subprocess.TimeoutExpired:
        raise Setup("git archive timeout at %s" % rev[:12])
    if proc.returncode != 0:
        raise Setup("git archive %s failed: %s"
                    % (rev[:12], (proc.stderr or b"").decode("utf-8", "replace").strip()))
    with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode="r:") as tf:
        tf.extractall(dest, filter="data")


# --------------------------------------------------------------------------
# auditor arm
# --------------------------------------------------------------------------

def _counter(text, key):
    found = None
    for hit in re.finditer(r"\b%s=(\d+)\b" % re.escape(key), text):
        found = hit
    return int(found.group(1)) if found else None


def _token(text, key):
    """Last `key=<token>` value on stdout (keys are distinct enough for \\b)."""
    found = None
    for hit in re.finditer(r"(?:^|\s)%s=(\S+)" % re.escape(key), text):
        found = hit
    return found.group(1) if found else None


def _trailing_count(token):
    """Member count carried as a trailing `:<n>` on a population digest, if any."""
    hit = re.search(r"[:\-](\d+)$", token or "")
    return int(hit.group(1)) if hit else None


def auditor_arm(repo, rev, auditor, timeout, tmp):
    """Run the auditor at `rev` in population mode; v2 counters, else narrowed v1."""
    info = dict(present=False, source=auditor or AUDITOR_REL, sha256=None, v2=False,
                rc=None, counters={k: None for k in COUNTER_KEYS}, mode=None,
                digest=None, members=None, narrowed=False, other=0, selftest=None,
                note="", output=[])
    if auditor:
        if not os.path.isfile(auditor):
            info["note"] = "auditor absent: %s" % auditor
            return info
        with open(auditor, "rb") as fh:
            raw = fh.read()
    else:
        raw = read_at(repo, rev, AUDITOR_REL)
        if raw is None:
            info["note"] = "auditor absent at %s: %s" % (rev[:12], AUDITOR_REL)
            return info
    info["present"] = True
    info["sha256"] = hashlib.sha256(raw).hexdigest()
    mat = os.path.join(tmp, "mori-gate-registry.py")
    with open(mat, "wb") as fh:
        fh.write(raw)
    os.chmod(mat, 0o755)

    proc = run([sys.executable, mat, "--rev", rev, "--repo", repo, "--audit-all"],
               timeout, cwd=tmp)
    text = proc.stdout or ""
    err = proc.stderr or ""
    counters = {k: _counter(text, k) for k in COUNTER_KEYS}
    info["mode"] = _token(text, "mode")
    info["digest"] = _token(text, "population_digest")
    info["members"] = _counter(text, "members")
    if all(counters[k] is not None for k in COUNTER_KEYS):
        info.update(v2=True, rc=proc.returncode, counters=counters,
                    output=text.splitlines())
    elif (proc.returncode == 2 and "unrecognized arguments" in err
          and "--audit-all" in err):
        # v1 CLI: it does not know --audit-all. The per-path audit below is a
        # narrowed measurement only; `auditor_mode` stays a named failure, so a
        # --audit run can never score C2.
        pop = population(repo, rev)
        argv = [sys.executable, mat, "--rev", rev, "--repo", repo]
        for path in pop:
            argv += ["--audit", path]
        proc = run(argv, timeout, cwd=tmp)
        text = proc.stdout or ""
        info["narrowed"] = True
        info["rc"] = proc.returncode
        info["output"] = text.splitlines()
        info["note"] = ("v1 CLI refused --audit-all (rc=2): narrowed --audit over %d "
                        "population paths; tables/duplicate/wrong_row unmeasured"
                        % len(pop))
        info["counters"]["registered"] = sum(
            1 for _t, verdict, _d in AUDIT_LINE.findall(text) if verdict == "PASS")
        info["counters"]["unregistered"] = sum(
            1 for _t, verdict, d in AUDIT_LINE.findall(text)
            if verdict == "FAIL" and d.startswith("unregistered:"))
        info["counters"]["no_selftest"] = sum(
            1 for _t, verdict, d in AUDIT_LINE.findall(text)
            if verdict == "FAIL" and "no --selftest" in d)
        info["other"] = sum(
            1 for _t, verdict, d in AUDIT_LINE.findall(text)
            if verdict == "FAIL" and not d.startswith("unregistered:")
            and "no --selftest" not in d)
    else:
        info["rc"] = proc.returncode
        info["output"] = text.splitlines() + ["stderr: " + err.strip()[:200]]
        info["note"] = ("auditor printed no population counters and did not refuse "
                        "--audit-all (rc=%s)" % proc.returncode)

    sproc = run([sys.executable, mat, "--selftest"], timeout, cwd=tmp)
    tallies = TALLY.findall(sproc.stdout or "")
    if tallies:
        info["selftest"] = (int(tallies[-1][0]), int(tallies[-1][1]))
    return info


# --------------------------------------------------------------------------
# write-scope arm
# --------------------------------------------------------------------------

def expect_of(entry):
    """(rc, repo_unchanged, writes_outside_tmpdir) declared by an entry."""
    exp = entry.get("expect")
    rc, unchanged, outside = 0, True, 0
    if isinstance(exp, dict):
        if "rc" in exp:
            rc = int(exp["rc"])
        elif "exit" in exp:
            rc = int(exp["exit"])
        if "repo_unchanged" in exp:
            unchanged = str(exp["repo_unchanged"]).strip().lower() in ("yes", "true", "1")
        if "writes_outside_tmpdir" in exp:
            outside = int(exp["writes_outside_tmpdir"])
    elif isinstance(exp, int):
        rc = exp
    elif isinstance(exp, str) and exp.strip():
        pairs = dict(re.findall(r"(\w+)=(\S+)", exp))
        if "repo_unchanged" in pairs:
            unchanged = pairs["repo_unchanged"].lower() in ("yes", "true", "1")
        if "writes_outside_tmpdir" in pairs:
            try:
                outside = int(pairs["writes_outside_tmpdir"])
            except ValueError:
                pass
        if "rc" in pairs:
            try:
                rc = int(pairs["rc"])
            except ValueError:
                pass
        elif not pairs and exp.strip().isdigit():
            rc = int(exp)
    return rc, unchanged, outside


def sandbox_run(repo, rev, argv, tmp, index, timeout):
    """Run one instrument's argv in a fresh copy; measure writes outside its TMPDIR."""
    root = os.path.join(tmp, "ws-%02d" % index)
    sand = os.path.join(root, "repo")
    wtmp = os.path.join(root, "tmp")
    home = os.path.join(root, "home")
    for d in (sand, wtmp, home):
        os.makedirs(d, exist_ok=True)
    obs = dict(rc=None, repo_changed=0, outside=0, error=None)
    try:
        materialize_tree(repo, rev, sand)
    except Setup as exc:
        obs["error"] = str(exc)
        return obs
    before = tree_digest(sand)
    env = child_env(TMPDIR=wtmp, HOME=home)
    env.pop("XDG_CONFIG_HOME", None)
    cmd = list(argv)
    if cmd[0] in ("python3", "python"):
        cmd[0] = sys.executable
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              cwd=sand, env=env, check=False)
    except subprocess.TimeoutExpired:
        raise Setup("timeout after %ss running %s" % (timeout, " ".join(cmd)))
    except OSError as exc:
        obs["error"] = "cannot run %s: %s" % (cmd[0], exc)
        return obs
    obs["rc"] = proc.returncode
    after = tree_digest(sand)
    changed = [k for k in set(before) | set(after) if before.get(k) != after.get(k)]
    obs["repo_changed"] = len(changed)
    # Outside the sandbox TMPDIR: the copied tree, the redirected HOME, and any
    # sibling the instrument dropped beside the copy.
    obs["outside"] = (len(changed) + len(tree_digest(home))
                      + len(set(os.listdir(root)) - {"repo", "tmp", "home"}))
    return obs


def writescope_arm(repo, rev, fixture, timeout, tmp):
    out = dict(ok=False, note="", checked=0, skipped=0, mismatch=0, lines=[])
    path = resolve_inside(repo, fixture)
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as exc:
        out["note"] = "fixture absent/unreadable: %s" % exc
        return out
    except ValueError as exc:
        out["note"] = "fixture is not JSON: %s" % exc
        return out
    entries = data.get("entries") if isinstance(data, dict) else data
    if not isinstance(entries, list) or not entries:
        out["note"] = "fixture carries no entries"
        return out
    out["ok"] = True
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            out["skipped"] += 1
            continue
        target = str(entry.get("path") or "")
        argv = entry.get("command")
        if isinstance(argv, str):
            argv = shlex.split(argv)
        if not target or not argv:
            out["skipped"] += 1
            out["lines"].append("writescope %s SKIP (no runnable argv)"
                                % (target or "?"))
            continue
        if "checkable" in entry and not entry["checkable"]:
            out["skipped"] += 1
            out["lines"].append("writescope %s SKIP (fixture marks it uncheckable)"
                                % target)
            continue
        if not exists_at(repo, rev, target):
            out["skipped"] += 1
            out["lines"].append("writescope %s SKIP (absent at rev)" % target)
            continue
        want_rc, want_unchanged, want_outside = expect_of(entry)
        obs = sandbox_run(repo, rev, argv, tmp, index, timeout)
        if obs["error"]:
            out["mismatch"] += 1
            out["lines"].append("writescope %s MISMATCH (%s) declared=%r"
                                % (target, obs["error"], entry.get("declared", "")))
            continue
        out["checked"] += 1
        bad = []
        if obs["rc"] != want_rc:
            bad.append("rc=%s want=%s" % (obs["rc"], want_rc))
        if want_unchanged and obs["repo_changed"]:
            bad.append("repo_changed=%d" % obs["repo_changed"])
        if obs["outside"] != want_outside:
            bad.append("writes_outside_tmpdir=%d want=%d"
                       % (obs["outside"], want_outside))
        if bad:
            out["mismatch"] += 1
            out["lines"].append("writescope %s MISMATCH (%s) declared=%r"
                                % (target, "; ".join(bad), entry.get("declared", "")))
        else:
            out["lines"].append(
                "writescope %s match rc=%d repo_unchanged=%s "
                "writes_outside_tmpdir=%d declared=%r"
                % (target, obs["rc"], "no" if obs["repo_changed"] else "yes",
                   obs["outside"], entry.get("declared", "")))
    return out


# --------------------------------------------------------------------------
# mutant arm
# --------------------------------------------------------------------------

def mutant_bytes(repo, rev, mutants_dir, name):
    """The mutant's bytes at `--rev`, repo-relative only: an absolute or
    escaping `--mutants-dir` is a setup error, and a worktree-only mutant is
    never counted at a revision that lacks it."""
    if not name:
        return None
    resolve_inside(repo, mutants_dir)
    return read_at(repo, rev, mutants_dir.rstrip("/") + "/" + name)


# --------------------------------------------------------------------------
# evaluation
# --------------------------------------------------------------------------

def evaluate(repo, rev, auditor, writescope, mutants_dir, subject, timeout):
    checks, fails, lines = [], [], []
    counters = {k: None for k in COUNTER_KEYS}
    counters.update(writescope_mismatch=None, writescope_checked=0,
                    auditor_selftest=None, mutant="absent")

    def record(name, ok, detail=""):
        checks.append((name, bool(ok), detail))
        if not ok:
            fails.append(name)

    tmp = tempfile.mkdtemp(prefix="c2-")
    try:
        aud = auditor_arm(repo, rev, auditor, timeout, tmp)
        counters.update({k: aud["counters"][k] for k in COUNTER_KEYS})
        counters["auditor_selftest"] = aud["selftest"]
        lines.append("auditor %s sha256=%s"
                     % (aud["source"], (aud["sha256"] or "absent")[:12]))
        for line in aud["output"][:80]:
            lines.append("auditor| " + line)
        record("auditor_present", aud["present"],
               aud["note"] or "%s at %s" % (aud["source"], rev[:12]))
        record("auditor_v2", aud["v2"],
               aud["note"] or " ".join("%s=%s" % (k, aud["counters"][k])
                                       for k in COUNTER_KEYS))
        counters["population_mode"] = aud["mode"] or "absent"
        counters["population_digest"] = aud["digest"] or "absent"
        record("auditor_mode",
               aud["mode"] == "population" and aud["digest"] is not None,
               "mode=%s population_digest=%s"
               % (aud["mode"] or "absent", aud["digest"] or "absent"))
        members = aud["members"]
        if members is None:
            members = _trailing_count(aud["digest"])
        if members is None and aud["digest"]:
            members = len(population(repo, rev))
        counters["population_members"] = members
        buckets = (aud["counters"]["registered"], aud["counters"]["unregistered"],
                   aud["counters"]["no_selftest"], aud["other"])
        # The auditor publishes no member count of its own, so the witness is the
        # declared population enumerated here. Its buckets must partition exactly
        # that population: `registered` equals the member count in every state C2
        # admits (unregistered=0 and no_selftest=0), and a truncated audit that
        # silently drops paths fails the sum. `other` carries findings the two
        # named buckets do not (narrowed runs only; population mode prints none).
        record("population_members",
               members is not None and None not in buckets
               and sum(buckets) == members,
               "registered+unregistered+no_selftest+other=%s+%s+%s+%s=%s members=%s"
               % (buckets[0], buckets[1], buckets[2], buckets[3],
                  sum(b for b in buckets if b is not None) if None not in buckets
                  else "unmeasured",
                  members if members is not None else "unmeasured"))
        record("tables", aud["counters"]["tables"] is not None
               and aud["counters"]["tables"] >= TABLE_FLOOR,
               "%s floor=%d" % (_shown(aud, "tables"), TABLE_FLOOR))
        record("registered", aud["counters"]["registered"] is not None
               and aud["counters"]["registered"] >= 1, _shown(aud, "registered"))
        record("unregistered", aud["counters"]["unregistered"] is not None
               and aud["counters"]["unregistered"] == 0, _shown(aud, "unregistered"))
        record("no_selftest", aud["counters"]["no_selftest"] is not None
               and aud["counters"]["no_selftest"] == 0, _shown(aud, "no_selftest"))
        record("duplicate", aud["counters"]["duplicate"] is not None
               and aud["counters"]["duplicate"] == 0, _shown(aud, "duplicate"))
        record("wrong_row", aud["counters"]["wrong_row"] is not None
               and aud["counters"]["wrong_row"] == 0, _shown(aud, "wrong_row"))
        record("auditor_rc", aud["rc"] == 0, "rc=%s" % aud["rc"])
        st = aud["selftest"]
        record("auditor_selftest", st is not None and st[1] == 0 and st[0] >= 1,
               "pass=%d fail=%d" % st if st else "no tally")

        ws = writescope_arm(repo, rev, writescope, timeout, tmp)
        counters["writescope_mismatch"] = ws["mismatch"]
        counters["writescope_checked"] = ws["checked"]
        lines.extend(ws["lines"])
        record("writescope_fixture", ws["ok"],
               ws["note"] or "%s" % (writescope if os.path.isabs(writescope)
                                     else os.path.join(repo, writescope)))
        record("writescope_entries", ws["checked"] >= 1,
               "checked=%d skipped=%d" % (ws["checked"], ws["skipped"]))
        record("writescope_mismatch", True,
               "mismatch=%d (check disabled)" % ws["mismatch"])

        name = os.path.basename(subject) if subject else ""
        mraw = mutant_bytes(repo, rev, mutants_dir, name)
        record("mutant_present", mraw is not None,
               "%s/%s" % (mutants_dir, name) if name else "no subject counter")
        if mraw is None:
            record("mutant_kill", False, "no mutant to run")
        else:
            mfile = os.path.join(tmp, "mutant-" + name)
            with open(mfile, "wb") as fh:
                fh.write(mraw)
            os.chmod(mfile, 0o755)
            mproc = run([sys.executable, mfile, "--selftest"], timeout, cwd=tmp)
            mt = TALLY.findall(mproc.stdout or "")
            tally = (int(mt[-1][0]), int(mt[-1][1])) if mt else None
            killed = mproc.returncode == 1 and tally is not None and tally[1] >= 1
            counters["mutant"] = "killed" if killed else "survived"
            record("mutant_kill", killed,
                   "%s %s" % (name, "pass=%d fail=%d" % tally if tally else "no tally"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return checks, fails, counters, lines


def _shown(aud, key):
    value = aud["counters"][key]
    return "unmeasured" if value is None else "%s=%d" % (key, value)


# --------------------------------------------------------------------------
# selftest — isolated fixtures, never the lane repo
# --------------------------------------------------------------------------

HEADER = ("| name | kind | entry | verdict map | self-test | pinned values | "
          "write scope | owner |")
SEP = "|---|---|---|---|---|---|---|---|"

# Env-driven auditor stub: argv receipt, population-mode counters over its own
# fixture repo, a narrowed v1 mode, and a selftest tally.
STUB_AUDITOR = '''#!/usr/bin/env python3
"""Fixture auditor stub: population mode over its own fixture repo."""
import hashlib
import os
import re
import subprocess
import sys

argv = sys.argv[1:]
if "--selftest" in argv:
    print("GATE_REGISTRY_SELFTEST "
          + os.environ.get("C2_FIXTURE_SELFTEST", "pass=6 fail=0"))
    sys.exit(int(os.environ.get("C2_FIXTURE_SELFTEST_RC", "0")))
receipt = os.environ.get("C2_FIXTURE_ARGV")
if receipt:
    with open(receipt, "a", encoding="utf-8") as fh:
        print(" ".join(argv), file=fh)
if os.environ.get("C2_FIXTURE_MODE") == "v1":
    if "--audit-all" in argv:
        sys.stderr.write("mori-gate-registry.py: error: unrecognized arguments: "
                         "--audit-all\\n")
        sys.exit(2)
    rev = argv[argv.index("--rev") + 1] if "--rev" in argv else "?"
    for i, arg in enumerate(argv):
        if arg == "--audit":
            print("audit %-40s PASS (fixture row)" % argv[i + 1])
    print("rev=" + rev)
    print("REGISTRY=met")
    sys.exit(0)
if "--audit" in argv and "--audit-all" in argv:
    sys.stderr.write("mori-gate-registry.py: error: --audit with --audit-all\\n")
    sys.exit(2)
repo = argv[argv.index("--repo") + 1] if "--repo" in argv else "."
rev = argv[argv.index("--rev") + 1] if "--rev" in argv else "HEAD"
POP = (re.compile(r"^tools/[^/]+\\.(?:py|sh)$"),
       re.compile(r"^\\.ufo/waves/round-4[45]/count-c[^/]*\\.py$"))
tree = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
                      capture_output=True, text=True).stdout.splitlines()
members = sorted(n for n in tree if any(p.match(n) for p in POP))
digest = hashlib.sha256("\\n".join(members).encode()).hexdigest()
with open(os.path.join(repo, "SKILL.md"), encoding="utf-8") as fh:
    tables = fh.read().count("| name | kind | entry | verdict map | self-test | "
                             "pinned values | write scope | owner |")
print("mode=population")
print("population_digest=sha256:%s:%d" % (digest, len(members)))
print("members=" + os.environ.get("C2_FIXTURE_MEMBERS", str(len(members))))
print(" ".join("%s=%s" % (key, os.environ.get(value, fallback))
               for key, value, fallback in (
                   ("tables", "C2_FIXTURE_TABLES", str(tables)),
                   ("registered", "C2_FIXTURE_REGISTERED", str(len(members))),
                   ("unregistered", "C2_FIXTURE_UNREGISTERED", "0"),
                   ("no_selftest", "C2_FIXTURE_NO_SELFTEST", "0"),
                   ("duplicate", "C2_FIXTURE_DUPLICATE", "0"),
                   ("wrong_row", "C2_FIXTURE_WRONG_ROW", "0"))))
print("REGISTRY=" + os.environ.get("C2_FIXTURE_VERDICT", "met"))
sys.exit(int(os.environ.get("C2_FIXTURE_RC", "0")))
'''
ENV_STUB_AUDITOR = '''#!/usr/bin/env python3
"""A hostile auditor stub: claims a green population run with tables=1."""
import sys

if "--selftest" in sys.argv:
    print("GATE_REGISTRY_SELFTEST pass=1 fail=0")
    sys.exit(0)
print("mode=population")
print("population_digest=deadbeef")
print("members=1")
print("tables=1 registered=1 unregistered=0 no_selftest=0 duplicate=0 wrong_row=0")
print("REGISTRY=met")
sys.exit(0)
'''


FIXTURE_TOOL = '''#!/usr/bin/env python3
import os
import sys

if "--selftest" in sys.argv:
    with open(os.path.join(os.environ["TMPDIR"], "fixture-tool.selftest"), "w",
              encoding="utf-8") as fh:
        fh.write("ok")
    print("FIXTURE_SELFTEST pass=1 fail=0")
    sys.exit(0)
print("fixture")
sys.exit(0)
'''

LEAK_TOOL = '''#!/usr/bin/env python3
import sys

if "--selftest" in sys.argv:
    with open("leak.txt", "w", encoding="utf-8") as fh:
        fh.write("wrote into the tree under test\\n")
    print("LEAK_SELFTEST pass=1 fail=0")
    sys.exit(0)
sys.exit(0)
'''

SUBJECT_OK = '''#!/usr/bin/env python3
import sys

if "--selftest" in sys.argv:
    print("SUBJECT_SELFTEST pass=2 fail=0")
    sys.exit(0)
print("SUBJECT=met")
sys.exit(0)
'''

MUTANT_DEAD = '''#!/usr/bin/env python3
import sys

if "--selftest" in sys.argv:
    print("SUBJECT_SELFTEST pass=1 fail=1")
    sys.exit(1)
print("SUBJECT=met")
sys.exit(0)
'''


def _registry(tables):
    body = ["# SKILL", "", "## Gates", "", HEADER, SEP]
    body += tables[0]
    for index, rows in enumerate(tables[1:], start=2):
        body += ["", "## Table %d" % index, "", HEADER, SEP] + rows
    return "\n".join(body) + "\n"


def _fixture_tables():
    """Seven eight-cell tables, mirroring the lane's measured table population."""
    return [[("| fixture gate %d | gate | `bash tools/fixture-tool.sh` | 0 clean · "
              "1 failed | `bash tools/fixture-tool.sh --selftest` | in-script cases | "
              "stdout only | mori |" % index)] for index in range(TABLE_FLOOR)]


def _mk(tmp, files, tables=None, uncommitted=None):
    repo = os.path.join(tmp, "repo")
    os.makedirs(repo, exist_ok=True)
    git(repo, ["init", "-q", "-b", "main"])
    git(repo, ["config", "user.email", "mori@shokunin.local"])
    git(repo, ["config", "user.name", "mori-shokunin"])
    with open(os.path.join(repo, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(_registry(tables or _fixture_tables()))
    for rel, body in files.items():
        full = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.chmod(full, 0o755)
    git(repo, ["add", "-A"])
    git(repo, ["commit", "-q", "-m", "fixture"])
    rev = git(repo, ["rev-parse", "main"]).stdout.strip()
    for rel, body in (uncommitted or {}).items():   # worktree only, after the rev
        full = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
        os.chmod(full, 0o755)
    return repo, rev


WS_JSON = {"entries": [
    {"path": "tools/fixture-tool.py", "declared": "stdout only; selftest temp tree",
     "command": ["python3", "tools/fixture-tool.py", "--selftest"],
     "expect": "rc=0 repo_unchanged=yes writes_outside_tmpdir=0"},
    {"path": "tools/fx-counter.py", "declared": "stdout only",
     "command": ["python3", "tools/fx-counter.py", "--selftest"], "expect": "rc=0"},
    {"path": "tools/manual-tool.py", "declared": "<dir> evidence only",
     "command": None, "expect": ""},
]}


def _base_files(**over):
    files = {
        "tools/mori-gate-registry.py": STUB_AUDITOR,
        "tools/fixture-tool.py": FIXTURE_TOOL,
        "tools/fx-counter.py": SUBJECT_OK,
        "fixtures/mutants/fx-counter.py": MUTANT_DEAD,
        "fixtures/write-scope.json": json.dumps(WS_JSON, indent=1),
    }
    files.update(over)
    return files


@contextlib.contextmanager
def fixture_env(**env):
    saved = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    try:
        yield
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def selftest():
    arms, failures = [], []

    def arm(name, fn):
        try:
            fn()
            arms.append(name)
        except AssertionError as exc:
            failures.append("%s: %s" % (name, exc))
        except Exception as exc:                      # noqa: BLE001
            failures.append("%s: raised %s" % (name, exc))

    def fixture(files, env=None, subject="tools/fx-counter.py"):
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, files)
            receipt = os.path.join(tmp, "argv.txt")
            settings = dict(env or {})
            settings["C2_FIXTURE_ARGV"] = receipt
            with fixture_env(**settings):
                checks, fails, counters, _lines = evaluate(
                    repo, rev, None, "fixtures/write-scope.json",
                    "fixtures/mutants", subject, 60)
            argv = ""
            if os.path.isfile(receipt):
                with open(receipt, encoding="utf-8") as fh:
                    argv = fh.read()
            return fails, counters, checks, argv
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def conformant():
        fails, counters, checks, argv = fixture(_base_files())
        tokens = argv.split()
        assert not fails, fails
        assert "--audit-all" in tokens and "--audit" not in tokens, argv
        assert counters["population_mode"] == "population", counters
        assert str(counters["population_digest"]).startswith("sha256:"), counters
        assert counters["population_members"] == counters["registered"], counters
        assert counters["writescope_checked"] >= 1, counters
        assert counters["mutant"] == "killed", counters

    def auditor_absent():
        files = _base_files()
        files.pop("tools/mori-gate-registry.py")
        fails, counters, _checks, _argv = fixture(files)
        assert "auditor_present" in fails, fails
        assert counters["tables"] is None and counters["registered"] is None, counters
        assert counters["population_digest"] == "absent", counters

    def auditor_red():
        fails, _c, _checks, _argv = fixture(
            _base_files(), {"C2_FIXTURE_REGISTERED": "1",
                            "C2_FIXTURE_UNREGISTERED": "2", "C2_FIXTURE_RC": "1",
                            "C2_FIXTURE_VERDICT": "unmet"})
        assert "unregistered" in fails, fails
        assert "auditor_rc" in fails, fails
        assert "population_members" not in fails, fails

    def duplicate_row():
        fails, _c, _checks, _argv = fixture(_base_files(),
                                            {"C2_FIXTURE_DUPLICATE": "1"})
        assert "duplicate" in fails, fails
        assert "unregistered" not in fails, fails

    def comment_only_selftest():
        fails, _c, _checks, _argv = fixture(
            _base_files(), {"C2_FIXTURE_REGISTERED": "2",
                            "C2_FIXTURE_NO_SELFTEST": "1"})
        assert "no_selftest" in fails, fails
        assert "population_members" not in fails, fails

    def surviving_mutant():
        fails, counters, _checks, _argv = fixture(
            _base_files(**{"fixtures/mutants/fx-counter.py": SUBJECT_OK}))
        assert "mutant_kill" in fails, fails
        assert counters["mutant"] == "survived", counters

    def writescope_mismatch():
        fails, counters, _checks, _argv = fixture(
            _base_files(**{"tools/fixture-tool.py": LEAK_TOOL}))
        assert "writescope_mismatch" in fails, fails
        assert counters["writescope_mismatch"] == 1, counters

    def narrowed_v1():
        fails, counters, _checks, argv = fixture(_base_files(),
                                                 {"C2_FIXTURE_MODE": "v1"})
        assert "--audit-all" in argv.split(), argv
        assert "auditor_mode" in fails, fails
        assert counters["tables"] is None and counters["duplicate"] is None, counters
        assert counters["registered"] and counters["registered"] >= 1, counters
        assert "unregistered" not in fails, fails
        assert counters["population_digest"] == "absent", counters

    def registered_mismatch():
        fails, counters, _checks, _argv = fixture(
            _base_files(), {"C2_FIXTURE_REGISTERED": "3", "C2_FIXTURE_MEMBERS": "5"})
        assert "population_members" in fails, fails
        assert "auditor_mode" not in fails, fails
        assert "tables" not in fails, fails

    def tables_floor():
        fails, counters, _checks, _argv = fixture(_base_files(),
                                                 {"C2_FIXTURE_TABLES": "6"})
        assert "tables" in fails, fails
        assert counters["tables"] == 6, counters
        assert "duplicate" not in fails, fails

    def env_auditor_ignored():
        """MORI_GATE_REGISTRY pointing at a green stub cannot change the verdict."""
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, _base_files())
            stub = os.path.join(tmp, "env-stub.py")
            with open(stub, "w", encoding="utf-8") as fh:
                fh.write(ENV_STUB_AUDITOR)
            os.chmod(stub, 0o755)
            with fixture_env(MORI_GATE_REGISTRY=stub):
                checks, fails, counters, _lines = evaluate(
                    repo, rev, None, "fixtures/write-scope.json",
                    "fixtures/mutants", "tools/fx-counter.py", 60)
            assert not fails, fails
            assert counters["tables"] == 7, counters
            assert counters["registered"] == 3, counters
            assert counters["population_digest"] != "deadbeef", counters
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def git_dir_poisoned_ignored():
        """A caller's GIT_DIR cannot retarget the measured revision."""
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, _base_files())
            other = os.path.join(tmp, "other")
            os.makedirs(other, exist_ok=True)
            git(other, ["init", "-q", "-b", "main"])
            git(other, ["config", "user.email", "mori@shokunin.local"])
            git(other, ["config", "user.name", "mori-shokunin"])
            with open(os.path.join(other, "README"), "w", encoding="utf-8") as fh:
                fh.write("other repo\n")
            git(other, ["add", "-A"])
            git(other, ["commit", "-q", "-m", "other"])
            rev_other = git(other, ["rev-parse", "main"]).stdout.strip()
            assert rev_other != rev
            with fixture_env(GIT_DIR=os.path.join(other, ".git"),
                             GIT_WORK_TREE=other):
                checks, fails, counters, _lines = evaluate(
                    repo, rev, None, "fixtures/write-scope.json",
                    "fixtures/mutants", "tools/fx-counter.py", 60)
            assert counters["tables"] == 7, counters
            assert not fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def worktree_mutant_not_counted():
        """A mutant present only in the worktree is absent at the measured rev."""
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            files = _base_files()
            files.pop("fixtures/mutants/fx-counter.py")
            repo, rev = _mk(tmp, files,
                            uncommitted={"fixtures/mutants/fx-counter.py":
                                         MUTANT_DEAD})
            checks, fails, counters, _lines = evaluate(
                repo, rev, None, "fixtures/write-scope.json",
                "fixtures/mutants", "tools/fx-counter.py", 60)
            assert "mutant_present" in fails, fails
            assert "mutant_kill" in fails, fails
            assert counters["mutant"] == "absent", counters
            checks, fails, counters, _lines = evaluate(
                repo, "WORK", None, "fixtures/write-scope.json",
                "fixtures/mutants", "tools/fx-counter.py", 60)
            assert counters["mutant"] == "killed", counters
            assert "mutant_kill" not in fails, fails
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def path_escape_refused():
        """Absolute or `..` path arguments fail closed with C2_SETUP."""
        tmp = tempfile.mkdtemp(prefix="c2st-")
        try:
            repo, rev = _mk(tmp, _base_files())
            for bad in ("/etc/passwd", "../outside.json",
                        "fixtures/../../escape.json"):
                for flag in ("--write-scope", "--mutants-dir"):
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        code = main([rev, "--repo", repo, flag, bad])
                    assert code == 2 and "C2_SETUP" in buf.getvalue(), \
                        (flag, bad, code, buf.getvalue())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


    arm("conformant_met", conformant)
    arm("auditor_absent_unmet", auditor_absent)
    arm("auditor_red_unmet", auditor_red)
    arm("duplicate_row_unmet", duplicate_row)
    arm("comment_only_selftest_unmet", comment_only_selftest)
    arm("surviving_mutant_unmet", surviving_mutant)
    arm("writescope_mismatch_unmet", writescope_mismatch)
    arm("narrowed_v1_unmet", narrowed_v1)
    arm("registered_mismatch_unmet", registered_mismatch)
    arm("tables_floor_unmet", tables_floor)
    arm("env_auditor_ignored", env_auditor_ignored)
    arm("git_dir_poisoned_ignored", git_dir_poisoned_ignored)
    arm("worktree_mutant_not_counted", worktree_mutant_not_counted)
    arm("path_escape_refused", path_escape_refused)

    for name in arms:
        print("selftest PASS %s" % name)
    for name in failures:
        print("selftest FAIL %s" % name)
    print("C2_SELFTEST pass=%d fail=%d" % (len(arms), len(failures)))
    return 0 if not failures else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--rev", dest="rev_opt", metavar="REV")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--auditor")
    ap.add_argument("--write-scope", default=WRITESCOPE_REL)
    ap.add_argument("--mutants-dir", default=MUTANTS_REL)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    rev = args.rev_opt or args.rev
    if not rev or (args.rev and args.rev_opt):
        print("usage: count-c2.py <rev|WORK> [--rev REV] [--repo PATH] "
              "[--auditor PATH] [--write-scope PATH] [--mutants-dir DIR] "
              "[--timeout S] [--selftest]")
        return 2
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo, ".git")):
        print("C2_SETUP repo is not a git checkout: %s" % repo)
        return 2
    measured = rev
    if rev != "WORK":
        got = run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"], 30)
        if got.returncode != 0:
            print("C2_SETUP cannot resolve revision %r" % rev)
            return 2
        measured = got.stdout.strip()

    auditor = args.auditor  # --auditor only; MORI_GATE_REGISTRY is never honoured
    try:
        resolve_inside(repo, args.mutants_dir)
        resolve_inside(repo, args.write_scope)
    except Setup as exc:
        print("C2_SETUP %s" % exc)
        return 2
    mutants = args.mutants_dir      # repo-relative, contained (checked above)
    writescope = args.write_scope   # repo-relative, contained (checked above)

    try:
        checks, fails, counters, lines = evaluate(
            repo, measured, auditor, writescope, mutants,
            os.path.basename(os.path.abspath(__file__)), args.timeout)
    except Setup as exc:
        print("C2_SETUP %s" % exc)
        return 2

    for line in lines:
        print(line)
    for name, ok, detail in checks:
        print("check %-20s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    parts = ["C2=%s" % ("unmet" if fails else "met")]
    for key in VERDICT_KEYS:
        value = counters.get(key)
        parts.append("%s=%s" % (key, "unmeasured" if value is None else value))
    parts.append("mode=%s" % counters.get("population_mode", "absent"))
    parts.append("population_digest=%s" % counters.get("population_digest", "absent"))
    parts.append("population_members=%s"
                 % ("unmeasured" if counters.get("population_members") is None
                    else counters["population_members"]))
    tally = counters.get("auditor_selftest")
    parts.append("auditor_selftest=%s"
                 % ("pass=%d/fail=%d" % tally if tally else "unmeasured"))
    parts.append("mutant=%s" % counters.get("mutant", "absent"))
    if fails:
        parts.append("checks_failed=%s" % ",".join(fails))
    parts.append("rev=%s" % measured)
    parts.append("repo=%s" % repo)
    print(" ".join(parts))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
