#!/usr/bin/env python3
"""mori-misroot-sweep.py — detection-only fleet-root misroot candidate sweep.

Round 16's mandatory sweep ran

    git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports

so a seat report written at the fleet root (``MoriR16.Lesson`` at the root
itself, later relocated under ``.ufo/waves/hyaku/misroots/``) was invisible to
it.  This tool repeats the same read-only status query with NO pathspec by
default, reads at most the first 64 KiB of every untracked regular file, and
reports a candidate when a file's path or head text names both the lane id and
the round (``R17`` / ``round-17`` / ``r17``).

It never moves, deletes, edits or commits anything.  It only runs
``git -C <fleet-root> status --porcelain=v1 -z --untracked-files=all`` (with
``GIT_OPTIONAL_LOCKS=0``) and reads the bytes of untracked regular files.

C3 calibration: the archived r16 artifact
(`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson`,
847 bytes) names neither its lane nor its round in its content -- only its
filename carries them.  ``--selftest`` therefore plants those exact bytes under
that exact name and asserts that the no-pathspec sweep finds the file by path
alone while the legacy pathspec still misses it.

Limits: a candidate is a *review lead*, not proof of seat ownership (read the
file header before acting); only the first 64 KiB of each file is inspected;
git-ignored files are invisible to ``git status``; a path in the status output
is relative to ``--fleet-root``; ``--legacy-pathspec`` reproduces the round-16
blind spot and is kept for comparison only.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

RC_CLEAN = 0
RC_CANDIDATE = 1
RC_SETUP = 2

SCHEMA = "mori-misroot-sweep-v1"
READ_CAP = 64 * 1024
STATUS_TIMEOUT = 120

FINDING_CLEAN = "MORI_MISROOT_CLEAN"
FINDING_CANDIDATE = "MORI_MISROOT_CANDIDATE"
FINDING_SETUP = "MORI_MISROOT_SETUP"


# ---------------------------------------------------------------------------
# git plumbing (read-only)
# ---------------------------------------------------------------------------


# Environment variables that relocate git's view of the repository.  If a
# parent process exports any of them, `-C <fleet-root>` would be redirected to
# another repo (the JjAudit F10 pattern), so they are scrubbed before every git
# call, including the selftest sandbox's writes.  GIT_CEILING_DIRECTORIES is
# deliberately kept: it only bounds upward discovery and is used to isolate the
# selftest sandbox from the enclosing clone.
_REDIRECT_ENV = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_COMMON_DIR",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE",
    "GIT_PREFIX",
)

# Global flags: no optional index locks, no fsmonitor subprocess.
_GIT_GLOBAL = ("--no-optional-locks", "-c", "core.fsmonitor=false")


def _git_env():
    env = dict(os.environ)
    for name in _REDIRECT_ENV:
        env.pop(name, None)
    # Belt and braces with --no-optional-locks: the sweep must not write.
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def _git_cmd(*args):
    return ["git"] + list(_GIT_GLOBAL) + list(args)


def _status_argv(fleet_root, pathspecs):
    argv = _git_cmd(
        "-C", fleet_root,
        "status", "--porcelain=v1", "-z", "--untracked-files=all",
    )
    if pathspecs:
        argv.append("--")
        argv.extend(pathspecs)
    return argv


def _run_git(argv, timeout=STATUS_TIMEOUT):
    return subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_git_env(),
        timeout=timeout,
    )


def _parse_status(raw):
    """Return untracked paths from ``--porcelain=v1 -z`` output.

    In -z mode a rename/copy record carries the source path as a second
    NUL-separated field, so it must be consumed without being read as a record
    of its own.
    """
    fields = raw.split(b"\0")
    untracked = []
    index = 0
    while index < len(fields):
        token = fields[index]
        index += 1
        if not token or len(token) < 4:
            continue
        status = token[:2]
        if status[:1] in (b"R", b"C"):
            if index < len(fields):
                index += 1
            continue
        if status != b"??":
            continue
        untracked.append(os.fsdecode(token[3:]))
    return untracked


# ---------------------------------------------------------------------------
# token matching
# ---------------------------------------------------------------------------


def _lane_pattern(lane):
    # Seat ids concatenate lane and round (``MoriR17.Lesson``), so only the
    # character *before* the id is guarded: a lane id embedded in another word
    # (``Memori``) must not match.
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(lane), re.IGNORECASE)


def _round_pattern(round_number):
    digits = str(round_number)
    # ``R17``, ``r17``, ``round-17``, ``round 17``, ``round_17``, ``round17``.
    # No left guard: the token follows the lane in every seat id.  The right
    # guard keeps ``R170`` / ``round-170`` from matching round 17.
    return re.compile(
        r"(?:[Rr](?![A-Za-z])|round[-_ ]?)" + digits + r"(?![0-9])",
        re.IGNORECASE,
    )


def _read_head(path, cap=READ_CAP):
    """Read at most ``cap`` bytes of a regular file without following links.

    Returns ``(data, read_bytes, truncated, size_bytes)`` or raises OSError.
    """
    flags = (
        os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    fd = os.open(path, flags)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, 0, False, int(st.st_size)
        chunks = []
        remaining = cap
        while remaining > 0:
            chunk = os.read(fd, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        return data, len(data), int(st.st_size) > len(data), int(st.st_size)
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# sweep
# ---------------------------------------------------------------------------


def _setup(reason, detail, **extra):
    payload = {
        "schema": SCHEMA,
        "finding": FINDING_SETUP,
        "reason": reason,
        "detail": detail,
        "detection_only": True,
        "moves_or_deletes": False,
    }
    payload.update(extra)
    return RC_SETUP, payload


def _scan(fleet_root, pathspecs, lane, round_number):
    lane_rx = _lane_pattern(lane)
    round_rx = _round_pattern(round_number)

    argv = _status_argv(fleet_root, pathspecs)
    try:
        proc = _run_git(argv)
    except FileNotFoundError:
        return _setup("git_missing", "git executable not found")
    except subprocess.TimeoutExpired:
        return _setup(
            "git_timeout", "git status exceeded %d seconds" % STATUS_TIMEOUT
        )

    if proc.returncode != 0:
        stderr = proc.stderr.decode("utf-8", "replace")[:400]
        return _setup(
            "git_status_failed",
            "git status exited %d: %s" % (proc.returncode, stderr.strip()),
            git_command=argv,
        )

    try:
        repo_root = _run_git(
            _git_cmd("-C", fleet_root, "rev-parse", "--show-toplevel")
        )
        repo_root_text = (
            repo_root.stdout.decode("utf-8", "replace").strip()
            if repo_root.returncode == 0
            else None
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        repo_root_text = None

    untracked = _parse_status(proc.stdout)
    scan = {
        "untracked_entries": len(untracked),
        "regular_files": 0,
        "non_regular_skipped": 0,
        "unreadable": 0,
        "truncated_files": 0,
        "bytes_read": 0,
        "read_cap": READ_CAP,
    }
    candidates = []

    for rel_path in sorted(untracked):
        full_path = os.path.join(fleet_root, rel_path)
        read_bytes = 0
        size_bytes = 0
        truncated = False
        try:
            lstat = os.lstat(full_path)
        except OSError:
            scan["unreadable"] += 1
            data = None
        else:
            if not stat.S_ISREG(lstat.st_mode):
                scan["non_regular_skipped"] += 1
                continue
            scan["regular_files"] += 1
            try:
                data, read_bytes, truncated, size_bytes = _read_head(full_path)
            except OSError:
                scan["unreadable"] += 1
                data = None
                size_bytes = int(lstat.st_size)
            scan["bytes_read"] += read_bytes
            if truncated:
                scan["truncated_files"] += 1
        read_ok = data is not None

        text = data.decode("utf-8", "replace") if data is not None else ""

        matched_in = []
        lane_hit = False
        round_hit = False
        if lane_rx.search(rel_path):
            lane_hit = True
            matched_in.append("path")
        if round_rx.search(rel_path):
            round_hit = True
            matched_in.append("path")
        if read_ok:
            if lane_rx.search(text):
                lane_hit = True
                matched_in.append("content")
            if round_rx.search(text):
                round_hit = True
                matched_in.append("content")

        if not (lane_hit and round_hit):
            continue

        candidates.append(
            {
                "class": "candidate_misroot",
                "path": rel_path,
                "size_bytes": size_bytes,
                "read_bytes": read_bytes,
                "truncated": bool(truncated),
                "read": "content" if read_ok else "path_only",
                "matched_in": sorted(set(matched_in)),
            }
        )

    candidates.sort(key=lambda item: item["path"])
    payload = {
        "schema": SCHEMA,
        "finding": FINDING_CANDIDATE if candidates else FINDING_CLEAN,
        "fleet_root": os.path.abspath(fleet_root),
        "repo_root": repo_root_text,
        "lane": lane,
        "round": round_number,
        "legacy_pathspec": list(pathspecs) if pathspecs else None,
        "git_command": argv,
        "scan": scan,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "detection_only": True,
        "moves_or_deletes": False,
    }
    return (RC_CANDIDATE if candidates else RC_CLEAN), payload


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

_PLANTED_NAME = "MoriR16.Lesson"
# Byte-exact witness for C3 calibration: the archived round-16 fleet-root
# misroot, read from
# /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson
# on 2026-10-20 (847 bytes, sha256 below).  Its content names neither the lane
# nor the round; only the file name does.  Pinned here so --selftest is
# hermetic and byte-identical, and self-verifying through the digest.
_ARCHIVE_SHA256 = (
    "15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e"
)
_ARCHIVE_B64 = (
    "Qm9vdENvbnRpbnVpdHkgZGlzY2xvc3VyZSAoaW5hZG1pc3NpYmxlLCBub3QgdmVyaWZpY2F0"
    "aW9uKTogKDEpIExpdmUgcmVhZC1vbmx5IGpvdXJuYWxjdGwgcHJvYmVzIHJhbiBvbiB0aGUg"
    "aG9zdDogYSBjdXJyZW50LWJvb3QgY3Vyc29yIGZldGNoIChyYyAwLCAyIHJlY29yZHMsIGN1"
    "cnNvci9ib290IGZpZWxkcyBvbmx5KSwgYW4gLS1jdXJzb3IgYW5jaG9yIHF1ZXJ5IChyYyAw"
    "LCByZWNvcmRzIG5vdCBjb3VudGVkKSwgYSBmYWJyaWNhdGVkLWN1cnNvciBxdWVyeSAocmMg"
    "MSwgZW1wdHkgc3Rkb3V0KSwgYW5kIGEgLS11c2VyIC1uIDEgcXVlcnkgKHJjIDAsIDMzNyBi"
    "eXRlcykuIE9uZSBvZiB0aGVzZSByYW4gYXMgYmFja2dyb3VuZCBqb2IgYmdfMjY2Nywgc3Rh"
    "cnRlZCBiZWZvcmUgdGhlIG5vLXJ1bnMgaW5zdHJ1Y3Rpb247IGl0IGNvbXBsZXRlZCBvbiBp"
    "dHMgb3duOyBJIGRpZCBub3QgcmUtcnVuIGl0LiAoMikgU2NyYXRjaCBmaWxlcyB3ZXJlIHdy"
    "aXR0ZW4gdG8gL3RtcCAoL3RtcC8ucHJvYmVfbnVsbCwgL3RtcC8ueCkgZHVyaW5nIHRoZSBw"
    "cm9iZSBhbmQgcmVtb3ZlZCBhZnRlcndhcmRzLiBSZXN1bHRzIGZyb20gKDEpIGFyZSBub3Qg"
    "dXNlZCBhcyBldmlkZW5jZSBpbiBCb290Q29udGludWl0eS5tZCBiZXlvbmQgdGhlIGRpc2Ns"
    "b3NlZCBvYnNlcnZhdGlvbiB0aGF0IHRoZSBmYWJyaWNhdGVkIGN1cnNvciByZWZ1c2VzIHdp"
    "dGggcmMgMTsgY3Vyc29yIGluY2x1c2l2aXR5IG9uIHRoaXMgaG9zdCBpcyB1bm9ic2VydmVk"
    "LiBGaW5kaW5ncyByZXN0IG9uIFMwMTQvUzAxNS9zZF9qb3VybmFsX3Rlc3RfY3Vyc29yIHN0"
    "YXRpYyB0ZXh0IG9ubHkuIE5vIGZ1cnRoZXIgZXhlY3V0aW9uLg=="
)
_SIBLING_NAME = "TabiNote.md"
_SIBLING_TEXT = "# TabiR17 notes\n\nSeat: TabiR17.ConnectTameshi.\n"
_NESTED_REL = ".ufo/waves/round-16/build/MoriNote.md"
_NESTED_TEXT = "# round-16 build note\n\nSeat: MoriR16.FieldDocs.\n"
_IGNORED_NAME = "ignored-MoriR16.Lesson"
_IGNORED_TEXT = "Mori round-16 (ignored, must stay invisible)\n"
_PATH_ONLY_NAME = "MoriR15.note"  # empty body: the path alone names lane+round
_BIG_NAME = "big-notes.txt"
_BIG_TEXT = "Mori " + ("x" * 70000) + " round-16\n"
_TRACKED_NAME = "tracked.txt"
_TRACKED_TEXT = "Mori round-16 tracked file (must never be scanned)\n"
_GITIGNORE_TEXT = "ignored-*\n"


def _archive_bytes():
    data = base64.b64decode("".join(_ARCHIVE_B64))
    digest = hashlib.sha256(data).hexdigest()
    if digest != _ARCHIVE_SHA256:
        raise RuntimeError(
            "pinned fixture digest %s != %s" % (digest, _ARCHIVE_SHA256)
        )
    return data


def _write(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def _write_bytes(path, data):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def _selftest_git(args):
    argv = _git_cmd(*args)
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_git_env(),
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "git %s exited %d: %s"
            % (
                " ".join(argv),
                proc.returncode,
                proc.stderr.decode("utf-8", "replace")[:300],
            )
        )
    return proc


def _snapshot(root):
    """{relative path: (size, sha256-free digest bytes marker)} for files."""
    entries = {}
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root)
            try:
                st = os.lstat(full)
            except OSError:
                entries[rel] = None
                continue
            with open(full, "rb") as handle:
                entries[rel] = (int(st.st_size), handle.read())
    return entries


def _selftest_invoke(tool, argv, extra_env=None):
    env = _git_env()
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [sys.executable, tool] + argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=STATUS_TIMEOUT,
    )
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        payload = None
    return proc.returncode, payload, proc.stderr.decode("utf-8", "replace")


def _selftest():
    tool = os.path.realpath(__file__)
    tmp_root = tempfile.mkdtemp(prefix="mori-misroot-selftest-")
    failures = []

    def fail(message):
        failures.append(message)

    try:
        repo = os.path.join(tmp_root, "fleet")
        decoy = os.path.join(tmp_root, "decoy")
        os.makedirs(repo)
        os.makedirs(decoy, exist_ok=True)
        hooks_dir = os.path.join(tmp_root, "no-hooks")

        try:
            archive = _archive_bytes()
            _selftest_git(["init", "-q", repo])
            _selftest_git(["init", "-q", decoy])
            _write(os.path.join(repo, ".gitignore"), _GITIGNORE_TEXT)
            _write(os.path.join(repo, _TRACKED_NAME), _TRACKED_TEXT)
            _selftest_git(["-C", repo, "add", ".gitignore", _TRACKED_NAME])
            _selftest_git(
                [
                    "-C", repo,
                    "-c", "user.name=mori-selftest",
                    "-c", "user.email=mori-selftest@invalid",
                    "-c", "commit.gpgsign=false",
                    "-c", "core.hooksPath=" + hooks_dir,
                    "commit", "-q", "-m", "base",
                ]
            )
        except (OSError, RuntimeError, FileNotFoundError) as exc:
            return _emit(
                {
                    "schema": SCHEMA,
                    "finding": "MORI_MISROOT_SELFTEST_SETUP",
                    "detail": "%s: %s" % (type(exc).__name__, exc),
                },
                RC_SETUP,
            )

        # Plant the round-16 misroot shape and its controls.
        planted = os.path.join(repo, _PLANTED_NAME)
        sibling = os.path.join(repo, _SIBLING_NAME)
        nested = os.path.join(repo, _NESTED_REL)
        ignored = os.path.join(repo, _IGNORED_NAME)
        path_only = os.path.join(repo, _PATH_ONLY_NAME)
        big = os.path.join(repo, _BIG_NAME)
        # Byte-exact archived r16 bytes: the name alone names lane and round.
        _write_bytes(planted, archive)
        _write(sibling, _SIBLING_TEXT)
        _write(nested, _NESTED_TEXT)
        _write(ignored, _IGNORED_TEXT)
        _write(path_only, "")
        _write(big, _BIG_TEXT)
        # Decoy repo for the poisoned-env arm: if the sweep honoured an
        # inherited GIT_DIR/GIT_WORK_TREE, this file would be reported instead
        # of the intended fleet.
        _write(os.path.join(decoy, "MoriR16.decoy.md"), "Mori round-16 decoy\n")

        before = _snapshot(repo)
        if _PLANTED_NAME not in before:
            fail("setup: planted file missing before sweep")
        elif before[_PLANTED_NAME][1] != archive:
            fail("setup: planted bytes differ from the archived fixture")

        base = ["--fleet-root", repo]
        arms = (
            (
                "no-pathspec-round16",
                base + ["--lane", "Mori", "--round", "16"],
                {
                    "rc": RC_CANDIDATE,
                    "finding": FINDING_CANDIDATE,
                    "paths": {_NESTED_REL, _PLANTED_NAME},
                    "absent": {_IGNORED_NAME, _BIG_NAME, _TRACKED_NAME,
                               _SIBLING_NAME},
                },
            ),
            (
                "legacy-pathspec-round16",
                base + [
                    "--lane", "Mori", "--round", "16",
                    "--legacy-pathspec", ".ufo/waves",
                    "--legacy-pathspec", ".ufo/reports",
                ],
                {
                    "rc": RC_CANDIDATE,
                    "finding": FINDING_CANDIDATE,
                    "paths": {_NESTED_REL},
                    "absent": {_PLANTED_NAME},
                },
            ),
            (
                "poisoned-env-scans-intended-fleet",
                base + ["--lane", "Mori", "--round", "16"],
                {
                    "rc": RC_CANDIDATE,
                    "finding": FINDING_CANDIDATE,
                    "paths": {_NESTED_REL, _PLANTED_NAME},
                    "absent": {"MoriR16.decoy.md"},
                    "fleet_root": repo,
                    "scan_untracked": 5,
                },
                {
                    "GIT_DIR": os.path.join(decoy, ".git"),
                    "GIT_WORK_TREE": decoy,
                    "GIT_INDEX_FILE": os.path.join(decoy, ".git", "index"),
                },
            ),
            (
                "other-lane-not-flagged",
                base + ["--lane", "Mori", "--round", "17"],
                {"rc": RC_CLEAN, "finding": FINDING_CLEAN, "paths": set(),
                 "absent": {_SIBLING_NAME, _PLANTED_NAME}},
            ),
            (
                "sibling-detected-for-own-lane",
                base + ["--lane", "Tabi", "--round", "17"],
                {"rc": RC_CANDIDATE, "finding": FINDING_CANDIDATE,
                 "paths": {_SIBLING_NAME}},
            ),
            (
                "unrelated-lane-round",
                base + ["--lane", "Tameshi", "--round", "16"],
                {"rc": RC_CLEAN, "finding": FINDING_CLEAN, "paths": set()},
            ),
            (
                "path-only-match",
                base + ["--lane", "Mori", "--round", "15"],
                {"rc": RC_CANDIDATE, "finding": FINDING_CANDIDATE,
                 "paths": {_PATH_ONLY_NAME}, "matched_in": ["path"]},
            ),
            (
                "round-normalization",
                base + ["--lane", "mori", "--round", "R16"],
                {"rc": RC_CANDIDATE, "finding": FINDING_CANDIDATE,
                 "paths": {_NESTED_REL, _PLANTED_NAME}},
            ),
            (
                "invalid-round",
                base + ["--lane", "Mori", "--round", "sixteen"],
                {"rc": RC_SETUP, "finding": FINDING_SETUP},
            ),
            (
                "fleet-root-missing",
                ["--fleet-root", os.path.join(tmp_root, "absent"),
                 "--lane", "Mori", "--round", "16"],
                {"rc": RC_SETUP, "finding": FINDING_SETUP},
            ),
            (
                "fleet-root-not-repo",
                ["--fleet-root", os.path.join(tmp_root, "notrepo"),
                 "--lane", "Mori", "--round", "16"],
                {"rc": RC_SETUP, "finding": FINDING_SETUP},
                # The sandbox lives inside the clone that runs the selftest;
                # the ceiling keeps git from adopting that enclosing repo.
                {"GIT_CEILING_DIRECTORIES": tmp_root},
            ),
        )
        os.makedirs(os.path.join(tmp_root, "notrepo"))

        results = {}
        planted_match = None
        for arm in arms:
            name, argv, want = arm[0], arm[1], arm[2]
            extra_env = arm[3] if len(arm) > 3 else None
            rc, payload, stderr = _selftest_invoke(tool, argv, extra_env)
            results[name] = {
                "rc": rc,
                "finding": None if payload is None else payload.get("finding"),
                "paths": sorted(
                    item.get("path")
                    for item in (payload or {}).get("candidates", [])
                ),
            }
            label = "arm %s" % name
            if rc != want["rc"]:
                fail("%s: rc=%d want=%d" % (label, rc, want["rc"]))
            if payload is None:
                fail("%s: stdout is not one JSON object (stderr=%r)"
                     % (label, stderr[:160]))
                continue
            if payload.get("finding") != want["finding"]:
                fail("%s: finding=%r want=%r"
                     % (label, payload.get("finding"), want["finding"]))
            if payload.get("schema") != SCHEMA:
                fail("%s: schema=%r" % (label, payload.get("schema")))
            if payload.get("moves_or_deletes") is not False:
                fail("%s: moves_or_deletes is not false" % label)
            cands = payload.get("candidates", [])
            got_paths = {item.get("path") for item in cands}
            if payload.get("finding") != FINDING_SETUP and payload.get(
                "candidate_count"
            ) != len(cands):
                fail("%s: candidate_count=%r != %d"
                     % (label, payload.get("candidate_count"), len(cands)))
            for item in cands:
                if item.get("class") != "candidate_misroot":
                    fail("%s: candidate %r class=%r"
                         % (label, item.get("path"), item.get("class")))
            want_paths = want.get("paths")
            if want_paths is not None and got_paths != want_paths:
                fail("%s: candidates=%r want=%r"
                     % (label, sorted(got_paths), sorted(want_paths)))
            for absent in want.get("absent", ()):
                if absent in got_paths:
                    fail("%s: unexpected candidate %r" % (label, absent))
            if "fleet_root" in want and payload.get("fleet_root") != want["fleet_root"]:
                fail("%s: fleet_root=%r want=%r"
                     % (label, payload.get("fleet_root"), want["fleet_root"]))
            if "scan_untracked" in want:
                got_untracked = int(
                    (payload.get("scan") or {}).get("untracked_entries") or 0
                )
                if got_untracked != want["scan_untracked"]:
                    fail("%s: untracked_entries=%r want=%r"
                         % (label, got_untracked, want["scan_untracked"]))
            if "matched_in" in want:
                matched = {
                    tuple(item.get("matched_in") or [])
                    for item in payload.get("candidates", [])
                }
                if matched != {tuple(want["matched_in"])}:
                    fail("%s: matched_in=%r want=%r"
                         % (label, sorted(matched), want["matched_in"]))
            if name == "no-pathspec-round16":
                planted_match = next(
                    (item for item in cands
                     if item.get("path") == _PLANTED_NAME),
                    None,
                )
                if planted_match is None:
                    fail("%s: byte-exact planted witness not detected" % label)
                else:
                    if planted_match.get("matched_in") != ["path"]:
                        fail("%s: planted matched_in=%r want=['path']"
                             % (label, planted_match.get("matched_in")))
                    if planted_match.get("read_bytes") != len(archive):
                        fail("%s: planted read_bytes=%r want=%d"
                             % (label, planted_match.get("read_bytes"),
                                len(archive)))
                    if planted_match.get("size_bytes") != len(archive):
                        fail("%s: planted size_bytes=%r want=%d"
                             % (label, planted_match.get("size_bytes"),
                                len(archive)))
                scan = payload.get("scan") or {}
                if int(scan.get("truncated_files") or 0) < 1:
                    fail("%s: truncation cap not exercised" % label)
                if int(scan.get("bytes_read") or 0) > int(
                    scan.get("regular_files") or 0
                ) * READ_CAP:
                    fail("%s: read more than cap per file" % label)
            if name == "legacy-pathspec-round16":
                if payload.get("legacy_pathspec") != [
                    ".ufo/waves", ".ufo/reports"
                ]:
                    fail("%s: legacy_pathspec not echoed" % label)

        after = _snapshot(repo)
        if after != before:
            changed = sorted(
                set(before).symmetric_difference(after)
            ) or [
                rel for rel in sorted(before)
                if before[rel] != after.get(rel)
            ]
            fail("sweep mutated the sandbox: %r" % changed)

        swept = results.get("no-pathspec-round16", {}).get("paths") or []
        legacy = results.get("legacy-pathspec-round16", {}).get("paths") or []
        planted_found = _PLANTED_NAME in swept
        planted_missed_legacy = _PLANTED_NAME not in legacy
        if not planted_found:
            fail("capability arm: planted root file not found without pathspec")
        if not planted_missed_legacy:
            fail("regression arm: planted root file found with legacy pathspec")

        if failures:
            return _emit(
                {
                    "schema": SCHEMA,
                    "finding": "MORI_MISROOT_SELFTEST_FAIL",
                    "arms": len(arms),
                    "failures": failures,
                    "fixture_sha256": _ARCHIVE_SHA256,
                    "fixture_bytes": len(archive),
                    "planted_matched_in": None
                    if planted_match is None
                    else planted_match.get("matched_in"),
                    "planted_found_without_pathspec": planted_found,
                    "planted_found_with_legacy_pathspec": not
                    planted_missed_legacy,
                    "sandbox_unchanged": after == before,
                },
                RC_CANDIDATE,
            )
        return _emit(
            {
                "schema": SCHEMA,
                "finding": "MORI_MISROOT_SELFTEST_OK",
                "arms": len(arms),
                "fixture_sha256": _ARCHIVE_SHA256,
                "fixture_bytes": len(archive),
                "planted_matched_in": None
                if planted_match is None
                else planted_match.get("matched_in"),
                "planted_found_without_pathspec": planted_found,
                "planted_found_with_legacy_pathspec": not
                planted_missed_legacy,
                "sandbox_unchanged": after == before,
            },
            RC_CLEAN,
        )
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_HELP_EPILOG = """\
limits:
  * a candidate is a review lead, not proof of seat ownership; read the file
    header before acting on it;
  * only the first 65536 bytes of each untracked regular file are inspected;
  * git-ignored files never reach `git status` and cannot be seen;
  * paths are reported relative to --fleet-root;
  * --legacy-pathspec reproduces the round-16 pathspec blind spot and is for
    comparison only;
  * detection only: the tool never moves, deletes, edits or commits anything.
"""


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="detection-only sweep for fleet-root files that name a "
        "lane and a round (misroot candidates)",
        epilog=_HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--fleet-root", metavar="R",
        help="git checkout to sweep (paths are reported relative to it)",
    )
    parser.add_argument(
        "--lane", metavar="ID",
        help="lane id to look for, case-insensitively (e.g. Mori)",
    )
    parser.add_argument(
        "--round", metavar="N", dest="round_number",
        help="round number or token (17, R17, round-17)",
    )
    parser.add_argument(
        "--legacy-pathspec", metavar="P", action="append", default=None,
        help="restrict git status to P (repeatable); reproduces the round-16 "
        "query for comparison; omit for the full sweep",
    )
    parser.add_argument(
        "--selftest", action="store_true",
        help="build an isolated sandbox git repo under TMPDIR with the "
        "byte-exact archived MoriR16.Lesson bytes at the root and prove the "
        "no-pathspec sweep finds it by name while the legacy pathspec misses "
        "it; takes no other flags",
    )
    return parser.parse_args(argv)


def _normalize_round(value):
    match = re.match(r"^\s*(?:(?:round)[-_ ]?|[Rr])?(\d{1,6})\s*$", value)
    if not match:
        return None
    return int(match.group(1))


def main(argv=None):
    args = _parse_args(argv)

    if args.selftest:
        if args.fleet_root or args.lane or args.round_number or args.legacy_pathspec:
            return _emit_payload(
                _setup(
                    "selftest_takes_no_sweep_flags",
                    "--selftest runs alone",
                )
            )
        return _selftest()

    if not args.fleet_root or not args.lane or not args.round_number:
        return _emit_payload(
            _setup(
                "arguments_required",
                "--fleet-root, --lane and --round are required",
            )
        )

    round_number = _normalize_round(args.round_number)
    if round_number is None:
        return _emit_payload(
            _setup(
                "invalid_round",
                "round must be a number or R<number>/round-<number>",
            )
        )

    if not os.path.isdir(args.fleet_root):
        return _emit_payload(
            _setup(
                "fleet_root_missing",
                "not a directory: %s" % args.fleet_root,
            )
        )

    rc, payload = _scan(
        args.fleet_root, args.legacy_pathspec, args.lane, round_number
    )
    return _emit(payload, rc)


def _emit_payload(result):
    rc, payload = result
    return _emit(payload, rc)


def _emit(payload, rc):
    sys.stdout.write(json.dumps(payload, sort_keys=True) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
