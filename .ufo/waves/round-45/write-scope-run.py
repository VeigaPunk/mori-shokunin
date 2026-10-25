#!/usr/bin/env python3
"""mori round-45 write-scope arm — sandbox runner for P-C2 item 6.

Each audited instrument's SKILL.md write-scope cell claims something about
where the instrument writes.  This runner copies the lane repo at a revision
into a sandbox under the caller's $TMPDIR, digests the copied tree (sorted
`find -type f -exec sha256sum`), lists the sandbox parent, runs the named
instrument's own `--selftest` with TMPDIR inside the sandbox but outside the
copied tree, re-digests, and reports what the run actually left behind:

    repo_unchanged=yes|no
    writes_outside_tmpdir=<n>
    declared=<cell text>
    observed=<diff summary>

Verdicts: TRUE (claim held), FALSE (bytes contradict the cell), UNEXERCISED
(no write seen but the selftest did not reach its own tally), UNAVAILABLE (the
instrument or its committed cell is absent at the measured revision).

Exit: 0 all match · 1 mismatch · 2 setup.  Never a traceback exit 1.

A declaration is re-derived from SKILL.md at the measured revision: a row
attributes a path through its entry cell naming that exact repo-relative path,
and the last such row in document order supersedes earlier ones.  The
fixture's frozen `declared` is compared with the revision's cell and drift is
reported; the claim tested is always the revision's.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys

FIELDS = ["name", "kind", "entry", "verdict map", "self-test",
          "pinned values", "write scope", "owner"]
HEADER_CELLS = [f.strip().lower() for f in FIELDS]
SETUP = 2


def repo_default():
    here = os.path.abspath(__file__)                     # <repo>/.ufo/waves/round-45/write-scope-run.py
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(here))))


def fixture_default(repo):
    return os.path.join(repo, ".ufo", "waves", "round-45", "fixtures",
                        "write-scope.json")


def setup(reason, detail=""):
    print("WRITESCOPE_SETUP reason=%s%s" % (reason, (" " + detail) if detail else ""))
    return SETUP


# ---------------------------------------------------------------- git / copy

def git(repo, args, timeout=120):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True,
                          text=True, timeout=timeout, check=False)


def resolve_rev(repo, rev):
    if rev == "WORK":
        return "WORK"
    try:
        got = git(repo, ["rev-parse", "--verify", rev + "^{commit}"], timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if got.returncode != 0:
        return None
    return got.stdout.strip()


SCRATCH = re.compile(r"^\.ufo/waves/[^/]+/tmp/")


def copy_work(repo, dest):
    """Copy tracked + untracked-non-ignored files; wave scratch dirs are not source."""
    listing = git(repo, ["ls-files", "-z", "--cached", "--others",
                         "--exclude-standard"], timeout=300)
    if listing.returncode != 0:
        return False, listing.stderr.strip()[:200]
    paths = [p for p in listing.stdout.split("\0") if p]
    copied, scratch, unreadable = 0, 0, 0
    for rel in paths:
        if SCRATCH.match(rel):
            scratch += 1
            continue
        src = os.path.join(repo, rel)
        dst = os.path.join(dest, rel)
        if not os.path.isfile(src):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.copy2(src, dst)
            copied += 1
        except OSError:
            unreadable += 1
    return True, ("%d files (working tree) scratch_excluded=%d unreadable_skipped=%d"
                  % (copied, scratch, unreadable))


def copy_rev(repo, rev, dest):
    if rev == "WORK":
        return copy_work(repo, dest)
    arch = subprocess.Popen(["git", "-C", repo, "archive", "--format=tar", rev],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    untar = subprocess.Popen(["tar", "-xf", "-", "-C", dest],
                             stdin=arch.stdout, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    arch.stdout.close()
    _out, err_untar = untar.communicate(timeout=600)
    _o, err_arch = arch.communicate(timeout=600)
    if arch.returncode != 0:
        return False, "git archive rc=%d %s" % (arch.returncode,
                                                err_arch.decode("utf-8", "replace").strip()[:200])
    if untar.returncode != 0:
        return False, "tar rc=%d %s" % (untar.returncode,
                                        err_untar.decode("utf-8", "replace").strip()[:200])
    return True, "git archive %s" % rev


# ------------------------------------------------------------------ digests

def _find(root, args, timeout=600):
    return subprocess.run(["find"] + args, cwd=root, capture_output=True,
                          text=True, timeout=timeout, check=False)


def digest_files(root):
    """Sorted `find . -type f -exec sha256sum {} +` -> ({rel: sha}, [lines])."""
    got = _find(root, [".", "-type", "f", "-exec", "sha256sum", "{}", "+"])
    shas = {}
    lines = []
    if got.returncode != 0:
        raise RuntimeError("find/sha256sum rc=%d %s" % (got.returncode,
                                                        got.stderr.strip()[:200]))
    for line in got.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            continue
        sha, path = parts[0].strip(), parts[1]
        if path.startswith("./"):
            path = path[2:]
        shas[path] = sha
        lines.append("%s  %s" % (sha, path))
    lines.sort()
    return shas, lines


def snapshot(root):
    """Every path under root (any type) + file digests + symlink targets."""
    shas, lines = digest_files(root)
    paths = _find(root, [".", "-mindepth", "1", "-print"])
    links = _find(root, [".", "-type", "l", "-print"])
    if paths.returncode != 0 or links.returncode != 0:
        raise RuntimeError("find listing rc=%d/%d" % (paths.returncode, links.returncode))
    all_paths = set()
    for line in paths.stdout.splitlines():
        line = line.strip()
        if line.startswith("./"):
            line = line[2:]
        if line:
            all_paths.add(line)
    link_map = {}
    for line in links.stdout.splitlines():
        line = line.strip()
        if line.startswith("./"):
            line = line[2:]
        if not line:
            continue
        try:
            link_map[line] = os.readlink(os.path.join(root, line))
        except OSError:
            link_map[line] = "?"
    return {"paths": all_paths, "sha": shas, "link": link_map, "lines": lines}


def tree_digest(lines):
    h = hashlib.sha256()
    for line in lines:
        h.update(line.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def delta(before, after):
    created = sorted(after["paths"] - before["paths"])
    deleted = sorted(before["paths"] - after["paths"])
    both = after["paths"] & before["paths"]
    modified = []
    for path in both:
        if before["sha"].get(path) != after["sha"].get(path):
            modified.append(path)
        elif before["link"].get(path) != after["link"].get(path):
            modified.append(path)
    modified.sort()
    return created, modified, deleted


# ------------------------------------------------------------- declarations

def parse_gate_rows(text):
    """Rows (8 cells) of every table whose header is the eight standard cells."""
    rows = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
            if [c.lower() for c in cells] == HEADER_CELLS:
                j = i + 1
                while j < len(lines) and lines[j].strip().startswith("|"):
                    body = lines[j].strip()
                    row_cells = [c.strip() for c in re.split(r"(?<!\\)\|", body)[1:-1]]
                    if row_cells and not set("".join(row_cells)) <= set("-: "):
                        rows.append(row_cells)
                    j += 1
                i = j
                continue
        i += 1
    return rows


def derive_declared(gate_rows, path):
    """Last row whose entry cell names `path` -> (cells, row names)."""
    hits = []
    for cells in gate_rows:
        if len(cells) != 8:
            continue
        if path in cells[2]:
            hits.append(cells)
    if not hits:
        return None, []
    return hits[-1], [c[0] for c in hits]


# -------------------------------------------------------------- instrument

ENV_KEEP = ("PATH",)


def sandbox_env(runroot, tmpdir):
    env = {
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "HOME": os.path.join(runroot, "home"),
        "TMPDIR": tmpdir,
        "TMP": tmpdir,
        "TEMP": tmpdir,
        "XDG_CACHE_HOME": os.path.join(runroot, "xdg", "cache"),
        "XDG_CONFIG_HOME": os.path.join(runroot, "xdg", "config"),
        "XDG_DATA_HOME": os.path.join(runroot, "xdg", "data"),
        "XDG_STATE_HOME": os.path.join(runroot, "xdg", "state"),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "SHELL": "/bin/sh",
        # A git call inside a selftest must never discover (or write) the lane
        # repo above the sandbox.
        "GIT_CEILING_DIRECTORIES": runroot,
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_SYSTEM": "/dev/null",
        "GIT_AUTHOR_NAME": "mori-writescope",
        "GIT_AUTHOR_EMAIL": "mori@shokunin.local",
        "GIT_COMMITTER_NAME": "mori-writescope",
        "GIT_COMMITTER_EMAIL": "mori@shokunin.local",
        "GIT_TERMINAL_PROMPT": "0",
    }
    return env


def run_argv(argv, cwd, env, timeout):
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, errors="replace",
                            start_new_session=True)
    timed_out = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            proc.kill()
        out, err = proc.communicate()
    return proc.returncode, out, err, timed_out


def run_one(entry, lane, runroot, timeout, gate_rows, interp):
    ident = entry["id"]
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", ident)
    tmprel = os.path.join("tmp", safe)
    tmpdir = os.path.join(runroot, tmprel)
    os.makedirs(tmpdir, exist_ok=True)
    for sub in ("home", "xdg/cache", "xdg/config", "xdg/data", "xdg/state"):
        os.makedirs(os.path.join(runroot, sub), exist_ok=True)

    frozen = entry.get("declared")
    cells, names = derive_declared(gate_rows, entry["path"])
    if cells is not None:
        declared = cells[6]
        source = "SKILL.md entry-cell row '%s'" % cells[0]
        if frozen is None:
            drift = "n/a"
        else:
            drift = "no" if frozen.strip() == declared.strip() else "yes"
    else:
        declared = frozen
        source = "fixture" if frozen is not None else "none"
        drift = "no" if frozen is not None else "n/a"
    checkable = bool(entry.get("checkable")) or cells is not None

    before = snapshot(runroot)
    argv = list(entry["command"])
    if argv and argv[0] in ("python3", "python"):
        argv[0] = interp
    absent = not os.path.exists(os.path.join(lane, entry["path"]))
    if absent:
        rc, out, err, timed_out = "skipped", "", "", False
    else:
        rc, out, err, timed_out = run_argv(argv, lane, sandbox_env(runroot, tmpdir), timeout)
    after = snapshot(runroot)
    created, modified, deleted = delta(before, after)

    touch = created + modified + deleted
    under_tmp = tmprel + os.sep
    outside = [p for p in touch if p != tmprel and not p.startswith(under_tmp)]
    repo_changes = [p for p in touch if p == "lane" or p.startswith("lane" + os.sep)]
    tmp_files = len([p for p in after["sha"] if p.startswith(under_tmp)])

    expect = entry.get("expect") or {}
    tokens = expect.get("stdout_contains") or []
    missing = [t for t in tokens if t not in out]
    selftest_line = ""
    for line in out.splitlines():
        if "SELFTEST" in line:
            selftest_line = line.strip()[:200]

    if absent:
        verdict, reason = "UNAVAILABLE", "absent at the measured revision"
    elif declared is None:
        verdict = "UNAVAILABLE"
        reason = "no committed write-scope cell names the path"
        if outside or repo_changes:
            reason += ("; %d write(s) outside TMPDIR observed but no claim to "
                       "contradict" % len(outside))
    elif outside or repo_changes:
        verdict, reason = "FALSE", "the run left bytes outside its TMPDIR"
    elif timed_out or rc != expect.get("rc", 0) or missing:
        verdict = "UNEXERCISED"
        bits = []
        if timed_out:
            bits.append("timeout")
        if rc != expect.get("rc", 0):
            bits.append("rc=%s" % rc)
        if missing:
            bits.append("stdout missing %s" % ",".join(missing))
        reason = "; ".join(bits)
    else:
        verdict, reason = "TRUE", "no write outside TMPDIR and the selftest tallied"

    observed = ("created=%d modified=%d deleted=%d outside_tmpdir=%d tmp_files=%d rc=%s"
                % (len(created), len(modified), len(deleted), len(outside), tmp_files, rc))
    if outside:
        observed += " first_outside=%s" % outside[0]

    print("--- instrument %s" % ident)
    print("path=%s" % entry["path"])
    print("declared_source=%s declared_drift=%s" % (source, drift))
    print("declared=%s" % (declared if declared is not None else "<none>"))
    if drift == "yes" and frozen is not None:
        print("declared_frozen=%s" % frozen)
    print("command=%s" % " ".join(argv))
    print("checkable=%s rows_naming=%s" % ("yes" if checkable else "no", len(names)))
    print("rc=%s timed_out=%s" % (rc, "yes" if timed_out else "no"))
    if selftest_line:
        print("selftest=%s" % selftest_line)
    print("repo_unchanged=%s" % ("yes" if not repo_changes else "no"))
    print("writes_outside_tmpdir=%d" % len(outside))
    print("observed=%s" % observed)
    if repo_changes:
        print("repo_changes=%s" % " ".join(repo_changes[:5]))
    if err.strip():
        print("stderr=%s" % err.strip().splitlines()[-1][:200])
    print("verdict=%s reason=%s" % (verdict, reason))

    return {"id": ident, "verdict": verdict, "outside": len(outside),
            "repo_unchanged": not repo_changes, "rc": rc,
            "declared": declared, "checkable": checkable}


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", action="store_true")
    ap.add_argument("--repo", default=repo_default())
    ap.add_argument("--fixture", default=None)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--only", action="append", default=[])
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    fixture = os.path.abspath(args.fixture or fixture_default(repo))
    tmpbase = os.environ.get("TMPDIR", "")
    if not tmpbase:
        return setup("no_tmpdir", "TMPDIR must be set (the sandbox lives there)")
    tmpbase = os.path.abspath(tmpbase)
    if tmpbase == "/tmp" or tmpbase.startswith("/tmp" + os.sep):
        return setup("tmpdir_is_tmp", "TMPDIR=%s; use a lane-local scratch dir" % tmpbase)
    if not os.path.isdir(tmpbase):
        return setup("tmpdir_unreadable", "TMPDIR=%s is not a directory" % tmpbase)
    try:
        with open(fixture, encoding="utf-8") as fh:
            spec = json.load(fh)
        entries = spec["entries"]
    except (OSError, ValueError, KeyError) as exc:
        return setup("fixture_unreadable", "%s: %s" % (fixture, exc))
    if not entries:
        return setup("no_entries", fixture)

    rev = "WORK" if args.work else args.rev
    resolved = resolve_rev(repo, rev)
    if resolved is None:
        return setup("unresolvable_revision", rev)

    runroot = os.path.join(tmpbase, "mori-writescope-%d-%s"
                           % (os.getpid(), hashlib.sha1(os.urandom(8)).hexdigest()[:8]))
    lane = os.path.join(runroot, "lane")
    os.makedirs(lane)
    interp = sys.executable or shutil.which("python3")
    status = SETUP
    try:
        ok, detail = copy_rev(repo, rev, lane)
        if not ok:
            return setup("copy_failed", detail)
        shas, lines = digest_files(lane)
        listing0 = ",".join(sorted(os.listdir(runroot)))
        gate_rows = []
        try:
            with open(os.path.join(lane, "SKILL.md"), encoding="utf-8",
                      errors="replace") as fh:
                gate_rows = parse_gate_rows(fh.read())
        except OSError:
            gate_rows = []
        print("WRITESCOPE write-scope arm (P-C2 item 6)")
        print("fixture=%s" % fixture)
        print("repo=%s" % repo)
        print("mode=%s rev=%s" % ("work" if rev == "WORK" else "rev", resolved))
        print("copy=%s" % detail)
        print("sandbox=%s" % runroot)
        print("interpreter=%s python=%s" % (interp, sys.version.split()[0]))
        print("gate_rows=%d" % len(gate_rows))
        print("lane_files=%d tree_digest=%s" % (len(shas), tree_digest(lines)))
        print("sandbox_parent_listing=%s" % listing0)
        print("env=minimal(PATH HOME TMPDIR XDG_* LANG GIT_*)")
        print("")

        selected = [e for e in entries if not args.only or e["id"] in args.only]
        results = []
        for entry in selected:
            results.append(run_one(entry, lane, runroot, args.timeout, gate_rows, interp))
            print("parent_listing=%s" % ",".join(sorted(os.listdir(runroot))))
            print("")

        true = [r for r in results if r["verdict"] == "TRUE"]
        false = [r for r in results if r["verdict"] == "FALSE"]
        unex = [r for r in results if r["verdict"] == "UNEXERCISED"]
        unav = [r for r in results if r["verdict"] == "UNAVAILABLE"]
        print("TRUE: %s" % (", ".join(r["id"] for r in true) or "-"))
        print("FALSE: %s" % (", ".join(r["id"] for r in false) or "-"))
        print("UNEXERCISED: %s" % (", ".join(r["id"] for r in unex) or "-"))
        print("UNAVAILABLE: %s" % (", ".join(r["id"] for r in unav) or "-"))
        print("WRITESCOPE instruments=%d true=%d false=%d unexercised=%d "
              "unavailable=%d writescope_mismatch=%d rev=%s repo=%s"
              % (len(results), len(true), len(false), len(unex), len(unav),
                 len(false), resolved, repo))
        met = not false and not unex and bool(true)
        print("WRITESCOPE=%s" % ("met" if met else "unmet"))
        if not true and not false:
            status = SETUP
        else:
            status = 0 if met else 1
    except KeyboardInterrupt:
        return setup("interrupted")
    except Exception as exc:                                  # noqa: BLE001
        return setup("internal", "%s: %s" % (type(exc).__name__, exc))
    finally:
        if args.keep:
            print("sandbox_kept=%s" % runroot)
        else:
            shutil.rmtree(runroot, ignore_errors=True)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
