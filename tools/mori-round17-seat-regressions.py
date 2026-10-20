#!/usr/bin/env python3
"""mori-round17-seat-regressions.py — isolated fixture gate for the C1
seat terminal-status capability (`tools/mori-seat-terminal.py`).

The gate never reads a real sessions directory.  It walks one committed
fixture tree (synthetic transcripts only), runs the tool once per declared
case as a real subprocess with a minimal environment and a per-case working
directory, and grades the single stdout JSON document against the fixture
table.  stdout/stderr bytes are retained per run with SHA-256; the fixture
tree and the expected table are hashed before and after the run.

Fixture tree layout (--fixtures DIR):

    DIR/expected.json
    DIR/<pack>/...            venue for one case family (synthetic *.jsonl)

expected.json:

    {"schema": "mori-seat-terminal-expected-v1",   # optional string
     "pins": {"<fixture-relative path>": "<64 lowercase hex>"},
     "cases": [{
        "id": "unique-case-id",
        "pack": "<subdirectory name>",
        "args": ["--sessions-dir", "{pack}", "--now-ms", "<ms>", ...],
        "unreadable_files": ["locked.jsonl"],   # optional, pack-relative
        "fifo_files": ["pipe.jsonl"],            # optional, absent in source
        "unreadable_dirs": ["locked-dir"],       # optional, sandbox chmod
        "want": {"rc": 0 | 1 | 2,
                 "finding_id": "MORI_SEAT_TERMINAL_OK" |
                               "MORI_SEAT_TERMINAL_DEAD" |
                               "MORI_SEAT_TERMINAL_SETUP",
                 "totals": {<declared classes>: <int >= 0>},
                 "seats": {"<A1 relative key>": "<class>"},
                 "reason": "<exact top-level reason>",   # optional
                 "records": {"<A1 relative key>": {"<seat field>": <value>}},
                 "top": {"main_sessions" | "duplicate_stems": <value>}}
     }]}

`pins` is mandatory and is independent persisted evidence: every
non-directory fixture entry except expected.json must appear, and the map is
verified against the actual tree before any tool runs.  Regular file:
sha256 of the content bytes.  Symlink (including a link to a directory):
sha256 of the link target text (UTF-8, no newline).  FIFO: sha256(b"fifo").
A chmod-000 regular file is accepted only when empty and is pinned as
sha256(b"") (non-empty unreadable input is a setup error).  Other special
entries (sockets/devices) are ignored and unpinned.  Missing, extra or
mismatched pins yield verdict `snapshot_tampered` and rc2 before any run.

Argv support: the tokens `{pack}` and `{fixtures}` are replaced with
absolute paths; when no `--sessions-dir` / `--sessions-dir=...` token is
present the gate prepends one.  Case args are otherwise passed through
unchanged, including `--now-ms` and `--settle-seconds`.

Per-case sandbox: for every case whose pack exists, the gate copies the
source pack (regular files, symlinks recreated as symlinks, FIFOs via
`os.mkfifo`, other specials skipped) into `output/cases/<case-id>/sessions`
and points the tool's `--sessions-dir` there.  Paths listed in the case's
`unreadable_files` (pack-relative regular files, source kept readable) are
chmod 000 only in that copy, then the sandbox is discarded with the output
tree.  Paths listed in `fifo_files` must not exist in the source pack (a FIFO
is untrackable by Git/jj): the gate creates them with `os.mkfifo` only in the
sandbox, rejecting every symlink ancestor and escape before any mkdir and
creating missing components one at a time (never `mkdir -p` through a link).
`unreadable_dirs` names pack-relative real directories that are chmod 000 in
the sandbox after the copy and restored to 0700 after the run so output
cleanup cannot fail.  Pins exclude generated FIFOs and hash source bytes only;
`files_scanned` counts regular source `*.jsonl` files (files below an
unreadable dir use the documented loose bound).  An explicit
`--sessions-dir {pack}/subpath` (used for the tracked root-symlink case) is
rebased to `<sandbox>/subpath`; every other arg stays unchanged.  Git/jj
cannot preserve mode 000, so source fixtures and `pins` always stay on source
bytes.  A case whose pack is absent (rc2 unavailable-directory fixtures such
as MissingDir) gets no sandbox and the nonexistent source path is passed
unchanged.

Grading (both sides of every rc0/rc1 case, per contract Amendment A1):

    * rc and `finding_id` must equal the case want, and rc must agree with
      the finding_id (0 OK, 1 DEAD, 2 SETUP).
    * the tool's `totals` must carry exactly the eight classes
      (including `error_unsettled`) as non-bool ints >= 0 and must equal the
      class tally re-derived from the graded seats; a want may declare a
      subset of classes and every declared class is compared exactly.
    * the tool's `seats` may be the contract's list, or an equivalent
      key -> object map.  Every seat object carries the original nine
      contract fields plus `key` (required) and `prefix` (required; equal to
      the stem before the first `.`); it may add the A1 fields `kind`,
      `terminal_ms`, `reason`.  Ids are sorted by stem or by key.  Entries
      with `kind == "main"` are counted in `main_sessions` and excluded from
      totals, by_prefix, by_provider_model, retry_exhausted and want.seats
      grading, but still count in `files_scanned` and the seat list.
      want.seats keys must be A1 relative keys (a flat pack's key equals its
      stem); there is no stem fallback.
    * optional independent wants are compared exactly and type-strict:
      `want.reason` against the top-level `reason`; `want.top` only for
      `main_sessions` / `duplicate_stems` against those output fields; and
      `want.records` as `{A1 relative key: {seat field: value}}`, where only
      the listed fields are compared and the record must exist by exact key
      (again no stem fallback).  A record's declared `class` must agree with
      want.seats when both name the same key.
    * the A1 scan metadata `now_ms`, `settle_seconds`, `main_sessions` and
      `duplicate_stems` is validated when present (and `now_ms` /
      `settle_seconds` must echo a pinned `--now-ms` / `--settle-seconds`
      argument); a pre-A1 producer is not required to carry them.
    * `files_scanned` must equal the walked *.jsonl file count and len(seats)
      when no --prefix is passed and every fixture file is readable; a
      prefix-filtered pack, a pack holding an unreadable file, or a pack with
      an unreadable directory must stay within [len(seats), walked-file
      count].
    * stdout must be exactly one strict JSON object (duplicate keys and
      NaN/Infinity rejected); unknown top-level or seat keys fail; any
      forbidden transcript field (errorMessage, content, usage, raw
      message) fails.
    * errorMessage/content strings found in the fixture pack must not be
      echoed on stdout or stderr (bounded scan; strings contained in output
      keys, class tokens, seat ids/prefixes or provider/model values are
      exempt).

The contract does not pin the type of top-level `retry_exhausted`; the gate
accepts the count form (int equal to the number of flagged graded seats) or
the boolean aggregate, and rejects anything else.  `error_code` may be an
int or its digit string.  A rc2 document is graded leniently: schema,
finding_id and (when present) sessions_dir must be correct,
implementation-defined setup diagnostics are tolerated, forbidden transcript
fields are still rejected, and no totals/seats are required.

Exit codes:

    0  every case matched
    1  at least one mismatch, or the tool path is absent (every case is
       recorded `capability_absent`, never green)
    2  setup/tamper: bad arguments, unreadable/symlinked fixture root or
       expected table, missing pins or a `snapshot_tampered` tree,
       invalid case table, unsafe/non-empty --output, or fixture inputs
       changed during the run

Output safety: --output must be absent or an empty directory, must not be a
symlink, must not equal or contain the repository root, and must not sit
under the fixture tree, the tool file, `tools/`, `.git/`, `.jj/` or
`corpus/`.  It may sit under the repository's `.ufo/` tree.

Manifest `git` metadata records the resolved `branch`, its `branch_source`
(attached / origin-head / unique-master-main / unresolved), `receipt_ref`,
the receipt `branch_tip` = `rev-parse refs/heads/<branch>`, and `head` as a
diagnostic only.  Receipts are measured against `branch_tip`, never `head`.
Git metadata is collected with all GIT_* variables (including GIT_TRACE*
and GIT_CONFIG*) scrubbed and with `--no-optional-locks -c
core.fsmonitor=false`.

Every fixture entry is also hashed before and after the run (symlinks by
link text, never followed; FIFOs by type; unreadable empty files by their
known empty content hash), but those runtime hashes are a second signal:
the persisted `pins` are checked first.  `pack_before_sha256` and
`pack_after_sha256` use one definition in both branches:
`sha256(canonical(snapshot_tree(pack_dir)))`, or null when the pack is
absent/empty (so capability_absent and executed receipts are comparable).
The tool is run with HOME pointing
at the per-case directory so an implementation cannot reach a real user
profile by accident.

--selftest builds a tiny fake tool and fixture trees under $TMPDIR (which
must be set; /tmp and /var/tmp are refused) and exercises green,
capability_absent, mismatch, forbidden-key, seat-map, prefix, files-scanned,
unreadable, A1 main-session, persisted-pin tamper, fixture-drift and
output-guard arms.  It never touches the production tool, fixture tree or
lane.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import selectors
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

SCHEMA = "mori-round17-seat-regressions-manifest-v1"
EXPECTED_SCHEMA = "mori-seat-terminal-expected-v1"
TOOL_SCHEMA = "mori-seat-terminal-v1"

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TOOL = REPO / "tools/mori-seat-terminal.py"
DEFAULT_FIXTURES = REPO / ".ufo/waves/round-17/fixtures/seat"

CLASSES = (
    "completed",
    "aborted",
    "dead_rate_limit",
    "dead_quota",
    "dead_error_other",
    "error_unsettled",
    "incomplete",
    "unavailable",
)
DEAD_CLASSES = tuple(c for c in CLASSES if c.startswith("dead_"))
CLASS_SET = frozenset(CLASSES)

FINDING_OK = "MORI_SEAT_TERMINAL_OK"
FINDING_DEAD = "MORI_SEAT_TERMINAL_DEAD"
FINDING_SETUP = "MORI_SEAT_TERMINAL_SETUP"
FINDINGS = (FINDING_OK, FINDING_DEAD, FINDING_SETUP)
RC_FINDING_ID = {0: FINDING_OK, 1: FINDING_DEAD, 2: FINDING_SETUP}

MAIN_KIND = "main"
SEAT_REASONS = frozenset(("schema", "no-message", "unreadable",
                          "terminal-time"))

TOP_KEYS = {
    "schema", "sessions_dir", "files_scanned", "totals",
    "retry_exhausted", "by_prefix", "by_provider_model", "seats",
    "finding_id", "now_ms", "settle_seconds", "main_sessions",
    "duplicate_stems",
}
SEAT_KEYS = {
    "seat", "prefix", "class", "provider", "model",
    "error_status", "retry_exhausted", "retries", "error_code",
    "key", "kind", "terminal_ms", "reason",
}
# Amendment A1 adds the four trailing fields; a pre-A1 producer is graded on
# the original nine only.
REQUIRED_SEAT_KEYS = {
    "seat", "prefix", "class", "provider", "model",
    "error_status", "retry_exhausted", "retries", "error_code",
    "key",
}
FORBIDDEN_KEYS = {
    "errorMessage", "error_message", "content", "usage", "message",
    "message_text", "messages", "transcript", "raw", "text",
}
CASE_KEYS = {"id", "pack", "args", "want", "note", "unreadable_files",
             "fifo_files", "unreadable_dirs"}
WANT_KEYS = {"rc", "finding_id", "totals", "seats", "reason", "records",
             "top"}
WANT_TOP_KEYS = frozenset(("main_sessions", "duplicate_stems"))
UNSET = object()

CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")
PACK_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$")

RUN_TIMEOUT_S = 30
CAPTURE_CAP = 4 * 1024 * 1024
MAX_TEST_BYTES = 2 * 1024 * 1024
MAX_CANARIES = 256
MAX_REASONS = 40

BASE_ENV = {
    "PATH": "/usr/bin:/bin",
    "LC_ALL": "C",
    "TZ": "UTC",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONDONTWRITEBYTECODE": "1",
}


class SetupError(Exception):
    """Usage, fixture-table or output-guard failure: exit 2."""


# ---------------------------------------------------------------------------
# small utilities
# ---------------------------------------------------------------------------


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel_or_abs(path: Path) -> str:
    resolved = Path(path).resolve()
    try:
        return str(resolved.relative_to(REPO))
    except ValueError:
        return str(resolved)


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def one_line(text, limit: int = 520) -> str:
    cleaned = " ".join(str(text).split())
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 3] + "..."


def _reject_constant(token):
    raise ValueError("non-JSON constant %r" % token)


def _unique_pairs(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("duplicate JSON key %r" % key)
        seen[key] = value
    return seen


def strict_json(text):
    """Parse JSON, rejecting duplicate keys and NaN/Infinity constants."""
    return json.loads(text, object_pairs_hook=_unique_pairs,
                      parse_constant=_reject_constant)


def atomic_bytes(path: Path, data: bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(".%s.tmp-%d" % (path.name, os.getpid()))
    with open(tmp, "wb") as handle:
        handle.write(data)
    os.replace(tmp, path)


def atomic_json(path: Path, obj) -> None:
    atomic_bytes(Path(path), (canonical(obj) + "\n").encode("utf-8"))


def is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def strict_eq(actual, want) -> bool:
    """Type-strict equality: True != 1, "1" != 1."""
    return type(actual) is type(want) and actual == want


def is_scalar(value) -> bool:
    return value is None or type(value) in (str, int, bool)


def safe_relative(rel) -> bool:
    return (isinstance(rel, str) and bool(rel)
            and not rel.startswith("/") and "\\" not in rel
            and ".." not in rel.split("/")
            and all(ord(ch) >= 32 for ch in rel))


# ---------------------------------------------------------------------------
# fixture inputs: hashing and loading
# ---------------------------------------------------------------------------


def _walk_error(exc):
    raise SetupError("cannot walk fixture tree: %s" % exc)


def snapshot_tree(root: Path) -> dict:
    """Hash every entry under root without following symlinks.

    Symlinks hash their link text; directories record a presence marker;
    unreadable regular files hash a stat fingerprint.  Special files are a
    setup error.
    """
    root = Path(root)
    rows: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(
            root, followlinks=False, onerror=_walk_error):
        dirnames.sort()
        base = Path(dirpath)
        for name in list(dirnames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                rows[rel] = "link:" + os.readlink(path)
                dirnames.remove(name)
            else:
                rows[rel] = "dir"
        for name in sorted(filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                rows[rel] = "link:" + os.readlink(path)
                continue
            try:
                mode = path.lstat().st_mode
            except OSError as exc:
                raise SetupError("cannot stat fixture entry %s: %s"
                                 % (rel_or_abs(path), exc))
            if stat.S_ISFIFO(mode):
                rows[rel] = "fifo"
                continue
            if not stat.S_ISREG(mode):
                # Sockets/devices are ignored by the tool contract; they are
                # neither hashed nor pinned.
                continue
            try:
                rows[rel] = sha256_file(path)
            except OSError:
                info = path.lstat()
                meta = "%d:%d:%d:%d" % (info.st_mode, info.st_size,
                                        info.st_mtime_ns, info.st_ctime_ns)
                rows[rel] = "meta:" + sha256_bytes(meta.encode("utf-8"))
    return dict(sorted(rows.items()))


def pack_tree_digest(pack_dir: Path) -> str | None:
    """One definition for pack_before/after in every branch.

    sha256 of canonical(snapshot_tree(pack_dir)); None when the pack is
    absent or empty (including MissingDir, where both sides are null).
    """
    pack_dir = Path(pack_dir)
    if not pack_dir.is_dir() or pack_dir.is_symlink():
        return None
    snapshot = snapshot_tree(pack_dir)
    if not snapshot:
        return None
    return sha256_bytes(canonical(snapshot).encode("utf-8"))


PIN_RE = re.compile(r"^[0-9a-f]{64}$")
FIFO_PIN = sha256_bytes(b"fifo")
EMPTY_SHA256 = sha256_bytes(b"")


def _validate_pins(value) -> dict:
    """Persisted fixture digests: relative path -> 64 lowercase hex."""
    if value is None:
        raise SetupError("expected table must carry a top-level 'pins' "
                         "object (fixture-relative path -> sha256 hex)")
    if not isinstance(value, dict):
        raise SetupError("expected table 'pins' must be a JSON object")
    pins = {}
    for rel, digest in value.items():
        if not isinstance(rel, str) or not rel or rel.startswith("/") \
                or "\\" in rel or ".." in rel.split("/"):
            raise SetupError("pins key is not a fixture-relative path: %r"
                             % (rel,))
        if rel == "expected.json":
            raise SetupError("pins must not include expected.json itself")
        if not isinstance(digest, str) or not PIN_RE.match(digest):
            raise SetupError("pins[%s] must be 64 lowercase hex" % rel)
        pins[rel] = digest
    return pins


def compute_pins(fixtures_dir: Path) -> dict:
    """Hash every non-directory fixture entry except expected.json.

    Regular file: sha256 of content bytes.  Symlink (including a link to a
    directory): sha256 of the link target text (UTF-8, no newline).  FIFO:
    sha256(b"fifo").  An unreadable regular file is accepted only when it is
    empty, pinned as sha256(b"").  Directories are not entries.
    """
    root = Path(fixtures_dir)
    pins = {}
    for dirpath, dirnames, filenames in os.walk(
            root, followlinks=False, onerror=_walk_error):
        dirnames.sort()
        base = Path(dirpath)
        for name in list(dirnames):
            path = base / name
            if path.is_symlink():
                rel = path.relative_to(root).as_posix()
                pins[rel] = sha256_bytes(os.readlink(path).encode("utf-8"))
                dirnames.remove(name)
        for name in sorted(filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if rel == "expected.json":
                continue
            if path.is_symlink():
                pins[rel] = sha256_bytes(os.readlink(path).encode("utf-8"))
                continue
            try:
                info = path.lstat()
            except OSError as exc:
                raise SetupError("cannot stat fixture entry %s: %s"
                                 % (rel_or_abs(path), exc))
            if stat.S_ISFIFO(info.st_mode):
                pins[rel] = FIFO_PIN
                continue
            if not stat.S_ISREG(info.st_mode):
                # Sockets/devices are ignored and unpinned.
                continue
            try:
                pins[rel] = sha256_file(path)
            except OSError:
                if info.st_size == 0:
                    pins[rel] = EMPTY_SHA256
                else:
                    raise SetupError(
                        "pins_unverifiable: unreadable non-empty fixture "
                        "file %s" % rel)
    return dict(sorted(pins.items()))


def compare_pins(declared: dict, actual: dict) -> dict:
    missing = sorted(set(actual) - set(declared))
    extra = sorted(set(declared) - set(actual))
    mismatched = sorted(rel for rel in set(declared) & set(actual)
                        if declared[rel] != actual[rel])
    return {
        "ok": not (missing or extra or mismatched),
        "missing": missing,
        "extra": extra,
        "mismatched": mismatched,
    }


@dataclass(frozen=True)
class CaseSpec:
    cid: str
    pack: str
    args: tuple
    want_rc: int
    want_finding_id: str
    want_totals: dict
    want_seats: dict
    unreadable_files: tuple
    fifo_files: tuple
    unreadable_dirs: tuple
    want_reason: object
    want_records: dict
    want_top: dict


def _validate_want_totals(obj) -> dict:
    """Declared totals may be a subset; seats are re-derived exactly."""
    if not isinstance(obj, dict) or not obj:
        raise SetupError("want.totals must be a non-empty JSON object")
    unknown = set(obj) - CLASS_SET
    if unknown:
        raise SetupError("want.totals has non-contract class key(s): %s"
                         % ",".join(sorted(unknown)))
    for cls in CLASSES:
        if cls not in obj:
            continue
        value = obj[cls]
        if not is_int(value) or value < 0:
            raise SetupError("want.totals.%s must be a non-bool int >= 0"
                             % cls)
    return {cls: obj[cls] for cls in CLASSES if cls in obj}


def _validate_want_seats(obj) -> dict:
    if not isinstance(obj, dict):
        raise SetupError("want.seats must be a JSON object")
    out = {}
    for seat, cls in obj.items():
        if not isinstance(seat, str) or not seat or len(seat) > 1024 \
                or any(ord(ch) < 32 for ch in seat):
            raise SetupError("want.seats key is not a printable non-empty "
                             "seat id")
        if cls not in CLASS_SET:
            raise SetupError("want.seats[%s] is not a contract class" % seat)
        out[seat] = cls
    return out


def _validate_unreadable_files(value, cid: str, pack_dir: Path) -> tuple:
    """Pack-relative regular files to chmod 000 in the per-case sandbox.

    Source fixtures stay readable: pins hash source bytes and the mode change
    exists only in the copied sandbox (Git/jj do not preserve mode 000).
    """
    if value is None:
        return ()
    if not isinstance(value, list):
        raise SetupError("case %s: unreadable_files must be a list" % cid)
    paths = []
    for rel in value:
        if not isinstance(rel, str) or not rel or rel.startswith("/") \
                or "\\" in rel or ".." in rel.split("/") \
                or any(ord(ch) < 32 for ch in rel):
            raise SetupError("case %s: unreadable_files entries must be "
                             "pack-relative paths" % cid)
        if rel in paths:
            raise SetupError("case %s: duplicate unreadable_files entry %s"
                             % (cid, rel))
        paths.append(rel)
    if not paths:
        return ()
    if not pack_dir.is_dir() or pack_dir.is_symlink():
        raise SetupError("case %s: unreadable_files on a missing pack" % cid)
    root = pack_dir.resolve()
    for rel in paths:
        path = pack_dir / rel
        if path.is_symlink() or not path.is_file():
            raise SetupError("case %s: unreadable_files target is not a "
                             "regular source file: %s" % (cid, rel))
        try:
            path.resolve().relative_to(root)
        except ValueError:
            raise SetupError("case %s: unreadable_files target escapes the "
                             "pack: %s" % (cid, rel))
        if not os.access(path, os.R_OK):
            raise SetupError("case %s: unreadable_files source must stay "
                             "readable (pins hash source bytes): %s"
                             % (cid, rel))
    return tuple(paths)


def _validate_fifo_files(value, cid: str, pack_dir: Path,
                         unreadable: tuple) -> tuple:
    """Pack-relative paths to create as FIFOs in the per-case sandbox only.

    Git/jj cannot track a FIFO, so the source path must be absent; pins
    therefore exclude the generated entry and source hashing stays stable.
    """
    if value is None:
        return ()
    if not isinstance(value, list):
        raise SetupError("case %s: fifo_files must be a list" % cid)
    paths = []
    for rel in value:
        if not isinstance(rel, str) or not rel or rel.startswith("/") \
                or "\\" in rel or ".." in rel.split("/") \
                or any(ord(ch) < 32 for ch in rel):
            raise SetupError("case %s: fifo_files entries must be "
                             "pack-relative paths" % cid)
        if rel in paths:
            raise SetupError("case %s: duplicate fifo_files entry %s"
                             % (cid, rel))
        if rel in unreadable:
            raise SetupError("case %s: fifo_files overlaps unreadable_files "
                             "at %s" % (cid, rel))
        paths.append(rel)
    if not paths:
        return ()
    if not pack_dir.is_dir() or pack_dir.is_symlink():
        raise SetupError("case %s: fifo_files on a missing pack" % cid)
    for rel in paths:
        path = pack_dir / rel
        if path.exists() or path.is_symlink():
            raise SetupError(
                "case %s: fifo_files path must not exist in the source pack "
                "(FIFOs are untrackable; create them only via metadata): %s"
                % (cid, rel))
        current = pack_dir
        for part in rel.split("/")[:-1]:
            current = current / part
            try:
                info = current.lstat()
            except FileNotFoundError:
                break
            except OSError as exc:
                raise SetupError("case %s: cannot stat FIFO ancestor %s: %s"
                                 % (cid, rel, exc))
            if stat.S_ISLNK(info.st_mode):
                raise SetupError(
                    "case %s: fifo_files ancestor is a symlink (no "
                    "out-of-sandbox creation): %s" % (cid, rel))
            if not stat.S_ISDIR(info.st_mode):
                raise SetupError("case %s: fifo_files ancestor is not a "
                                 "directory: %s" % (cid, rel))
    return tuple(paths)


def _validate_unreadable_dirs(value, cid: str, pack_dir: Path,
                              unreadable: tuple, fifos: tuple) -> tuple:
    """Pack-relative real directories to chmod 000 in the sandbox copy."""
    if value is None:
        return ()
    if not isinstance(value, list):
        raise SetupError("case %s: unreadable_dirs must be a list" % cid)
    paths = []
    for rel in value:
        if not safe_relative(rel):
            raise SetupError("case %s: unreadable_dirs entries must be "
                             "pack-relative paths" % cid)
        if rel in paths:
            raise SetupError("case %s: duplicate unreadable_dirs entry %s"
                             % (cid, rel))
        paths.append(rel)
    if not paths:
        return ()
    if not pack_dir.is_dir() or pack_dir.is_symlink():
        raise SetupError("case %s: unreadable_dirs on a missing pack" % cid)
    root = pack_dir.resolve()
    for rel in paths:
        target = pack_dir / rel
        try:
            info = target.lstat()
        except OSError as exc:
            raise SetupError("case %s: unreadable_dirs target missing: %s "
                             "(%s)" % (cid, rel, exc))
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise SetupError("case %s: unreadable_dirs target is not a "
                             "real source directory: %s" % (cid, rel))
        try:
            target.resolve().relative_to(root)
        except ValueError:
            raise SetupError("case %s: unreadable_dirs escapes the pack: %s"
                             % (cid, rel))
        if not os.access(target, os.R_OK | os.X_OK):
            raise SetupError("case %s: unreadable_dirs source must stay "
                             "readable: %s" % (cid, rel))
        for other in unreadable + fifos:
            if other == rel or other.startswith(rel + "/"):
                raise SetupError("case %s: unreadable_dirs overlaps "
                                 "unreadable_files/fifo_files at %s"
                                 % (cid, rel))
    for index, rel in enumerate(paths):
        for other in paths[index + 1:]:
            if rel.startswith(other + "/") or other.startswith(rel + "/"):
                raise SetupError("case %s: nested unreadable_dirs entries "
                                 "are not supported: %s, %s"
                                 % (cid, rel, other))
    return tuple(paths)


def _validate_record_value(field: str, value) -> bool:
    if field == "class":
        return isinstance(value, str) and value in CLASS_SET
    if field in ("seat", "key", "prefix", "kind"):
        return (isinstance(value, str) and bool(value)
                and len(value) <= 4096
                and all(ord(ch) >= 32 for ch in value))
    if field in ("provider", "model"):
        return value is None or isinstance(value, str)
    if field == "retry_exhausted":
        return type(value) is bool
    if field == "reason":
        return value is None or value in SEAT_REASONS
    if field in ("error_status", "retries", "terminal_ms"):
        return value is None or (is_int(value) and value >= 0)
    if field == "error_code":
        return (value is None or (is_int(value) and value >= 0)
                or (isinstance(value, str) and value.isdigit()
                    and len(value) <= 64))
    return False


def _validate_want_records(value, cid: str) -> dict:
    if value is None:
        return {}
    if not isinstance(value, dict) or not value:
        raise SetupError("case %s: want.records must be a non-empty object"
                         % cid)
    records = {}
    for key, fields in value.items():
        if not safe_relative(key):
            raise SetupError("case %s: want.records key is not an A1 "
                             "relative key: %r" % (cid, key))
        if not isinstance(fields, dict) or not fields:
            raise SetupError("case %s: want.records[%s] must be a non-empty "
                             "field object" % (cid, key))
        unknown = set(fields) - SEAT_KEYS
        if unknown:
            raise SetupError("case %s: want.records[%s] unknown field(s): "
                             "%s" % (cid, key, ",".join(sorted(unknown))))
        checked = {}
        for field, expected in fields.items():
            if not is_scalar(expected) or not _validate_record_value(
                    field, expected):
                raise SetupError("case %s: want.records[%s].%s has an "
                                 "invalid value" % (cid, key, field))
            checked[field] = expected
        records[key] = checked
    return records


def _validate_want_top(value, cid: str) -> dict:
    if value is None:
        return {}
    if not isinstance(value, dict) or not value:
        raise SetupError("case %s: want.top must be a non-empty object"
                         % cid)
    unknown = set(value) - WANT_TOP_KEYS
    if unknown:
        raise SetupError("case %s: want.top unknown field(s): %s"
                         % (cid, ",".join(sorted(unknown))))
    top = {}
    for field, expected in value.items():
        if field == "main_sessions":
            if not is_int(expected) or expected < 0:
                raise SetupError("case %s: want.top.main_sessions must be a "
                                 "non-bool int >= 0" % cid)
        else:  # duplicate_stems
            ok = (is_int(expected) and expected >= 0) or (
                isinstance(expected, list)
                and all(isinstance(item, str) for item in expected))
            if not ok:
                raise SetupError("case %s: want.top.duplicate_stems must be "
                                 "an int >= 0 or a string list" % cid)
        top[field] = expected
    return top


def _validate_want_reason(value, cid: str):
    if value is UNSET:
        return UNSET
    if value is None:
        return None
    if not isinstance(value, str):
        raise SetupError("case %s: want.reason must be a string or null"
                         % cid)
    return value


def _analyze_case(fixtures_dir: Path, obj, index: int, seen: set) -> CaseSpec:
    if not isinstance(obj, dict):
        raise SetupError("case %d must be a JSON object" % index)
    unknown = set(obj) - CASE_KEYS
    if unknown:
        raise SetupError("case %d: unknown key(s): %s"
                         % (index, ",".join(sorted(unknown))))
    cid = obj.get("id")
    if not isinstance(cid, str) or not CASE_ID_RE.match(cid):
        raise SetupError("case %d: id must match %s"
                         % (index, CASE_ID_RE.pattern))
    if cid in seen:
        raise SetupError("duplicate case id %s" % cid)
    seen.add(cid)

    pack = obj.get("pack")
    if not isinstance(pack, str) or not PACK_RE.match(pack):
        raise SetupError("case %s: pack must be a simple subdirectory name"
                         % cid)
    pack_dir = fixtures_dir / pack
    if pack_dir.is_symlink():
        raise SetupError("case %s: pack directory must not be a symlink: %s"
                         % (cid, pack))
    if pack_dir.exists() and not pack_dir.is_dir():
        raise SetupError("case %s: pack path is not a directory: %s"
                         % (cid, pack))

    args = obj.get("args")
    if not isinstance(args, list) or len(args) > 64:
        raise SetupError("case %s: args must be a list of <=64 strings"
                         % cid)
    for token in args:
        if not isinstance(token, str) or len(token) > 4096:
            raise SetupError("case %s: args tokens must be strings <=4096 "
                             "bytes" % cid)
        if "\x00" in token or "\n" in token or "\r" in token:
            raise SetupError("case %s: args token carries a NUL or newline"
                             % cid)

    unreadable = _validate_unreadable_files(
        obj.get("unreadable_files"), cid, pack_dir)
    fifos = _validate_fifo_files(
        obj.get("fifo_files"), cid, pack_dir, unreadable)
    dirs = _validate_unreadable_dirs(
        obj.get("unreadable_dirs"), cid, pack_dir, unreadable, fifos)

    want = obj.get("want")
    if not isinstance(want, dict):
        raise SetupError("case %s: want must be a JSON object" % cid)
    unknown = set(want) - WANT_KEYS
    if unknown:
        raise SetupError("case %s: unknown want key(s): %s"
                         % (cid, ",".join(sorted(unknown))))
    want_reason = _validate_want_reason(want.get("reason", UNSET), cid)
    want_records = _validate_want_records(want.get("records"), cid)
    want_top = _validate_want_top(want.get("top"), cid)
    rc = want.get("rc")
    if not is_int(rc) or rc not in (0, 1, 2):
        raise SetupError("case %s: want.rc must be 0, 1 or 2" % cid)
    finding_id = want.get("finding_id")
    if finding_id not in FINDINGS:
        raise SetupError("case %s: want.finding_id is not a contract "
                         "finding_id" % cid)
    if RC_FINDING_ID[rc] != finding_id:
        raise SetupError("case %s: want.rc=%d requires finding_id=%s"
                         % (cid, rc, RC_FINDING_ID[rc]))

    if rc in (0, 1):
        if pack_dir.is_symlink() or not pack_dir.is_dir():
            raise SetupError("case %s: pack directory missing: %s"
                             % (cid, pack))
        if "totals" not in want or "seats" not in want:
            raise SetupError("case %s: rc%d want must carry totals and "
                             "seats" % (cid, rc))
        totals = _validate_want_totals(want["totals"])
        seats = _validate_want_seats(want["seats"])
        derived = {cls: 0 for cls in CLASSES}
        for cls in seats.values():
            derived[cls] += 1
        for cls, value in totals.items():
            if derived[cls] != value:
                raise SetupError("case %s: want.seats tally for %s is %d, "
                                 "want.totals says %d"
                                 % (cid, cls, derived[cls], value))
        dead_total = sum(derived[cls] for cls in DEAD_CLASSES)
        if rc == 0 and dead_total:
            raise SetupError("case %s: rc0 want carries dead_* seats" % cid)
        if rc == 1 and not dead_total:
            raise SetupError("case %s: rc1 want carries no dead_* seats"
                             % cid)
    else:
        totals = _validate_want_totals(want["totals"]) \
            if "totals" in want else {}
        seats = _validate_want_seats(want["seats"]) \
            if "seats" in want else {}
        if totals and seats:
            derived = {cls: 0 for cls in CLASSES}
            for cls in seats.values():
                derived[cls] += 1
            for cls, value in totals.items():
                if derived[cls] != value:
                    raise SetupError("case %s: want.seats tally for %s is "
                                     "%d, want.totals says %d"
                                     % (cid, cls, derived[cls], value))

    for key, fields in want_records.items():
        if "class" in fields and key in seats \
                and seats[key] != fields["class"]:
            raise SetupError("case %s: want.records[%s].class disagrees "
                             "with want.seats" % (cid, key))

    return CaseSpec(cid=cid, pack=pack, args=tuple(args), want_rc=rc,
                    want_finding_id=finding_id, want_totals=totals,
                    want_seats=seats, unreadable_files=unreadable,
                    fifo_files=fifos, unreadable_dirs=dirs,
                    want_reason=want_reason, want_records=want_records,
                    want_top=want_top)


def load_expected(fixtures_dir: Path):
    if fixtures_dir.is_symlink() or not fixtures_dir.is_dir():
        raise SetupError("fixtures directory not readable: %s"
                         % rel_or_abs(fixtures_dir))
    path = fixtures_dir / "expected.json"
    if path.is_symlink() or not path.is_file():
        raise SetupError("expected table missing: %s"
                         % rel_or_abs(path))
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SetupError("cannot read expected table %s: %s"
                         % (rel_or_abs(path), exc))
    try:
        doc = strict_json(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError("expected table is not strict UTF-8 JSON: %s"
                         % exc)
    if not isinstance(doc, dict):
        raise SetupError("expected table must be a JSON object")
    unknown = set(doc) - {"schema", "cases", "note", "pins"}
    if unknown:
        raise SetupError("expected table unknown key(s): %s"
                         % ",".join(sorted(unknown)))
    if "schema" in doc and not isinstance(doc["schema"], str):
        raise SetupError("expected table schema, when present, must be a "
                         "string")
    pins = _validate_pins(doc.get("pins"))
    cases = doc.get("cases")
    if not isinstance(cases, list) or not cases:
        raise SetupError("expected table must hold a non-empty 'cases' list")
    specs = []
    seen: set = set()
    for index, obj in enumerate(cases):
        specs.append(_analyze_case(fixtures_dir, obj, index, seen))
    return specs, raw, pins


# ---------------------------------------------------------------------------
# output guard
# ---------------------------------------------------------------------------


def guard_output(raw: Path, protected) -> None:
    raw = Path(raw)
    if raw.is_symlink():
        raise SetupError("--output must not be a symlink: %s" % raw)
    out = raw.resolve()
    if out.exists():
        if not out.is_dir():
            raise SetupError("--output exists and is not a directory: %s"
                             % out)
        if any(out.iterdir()):
            raise SetupError("--output directory must be empty: %s" % out)
    for path, label in protected:
        protected_path = Path(path).resolve()
        if out == protected_path or out.is_relative_to(protected_path) \
                or protected_path.is_relative_to(out):
            raise SetupError(
                "--output must not cover, equal or sit under %s (%s); "
                "declared inputs are never output"
                % (label, rel_or_abs(protected_path)))
    if out == REPO or REPO.is_relative_to(out):
        raise SetupError("--output must not equal or contain the repository "
                         "root")
    for protected_path in (REPO / "tools", REPO / ".git", REPO / ".jj",
                           REPO / "corpus"):
        if out == protected_path or out.is_relative_to(protected_path):
            raise SetupError("--output must not be inside protected tree %s"
                             % rel_or_abs(protected_path))


# ---------------------------------------------------------------------------
# argv expansion and bounded subprocess
# ---------------------------------------------------------------------------


def fixture_scan_bounds(pack_dir: Path, unreadable_dirs=()):
    """Count regular non-symlink *.jsonl files and unreadable ones.

    The tool contract walks regular files named *.jsonl and never follows
    symlinks; an unreadable regular file (or any file below an
    `unreadable_dirs` directory) still yields an `unavailable`/skipped
    result, but an implementation may or may not count it in
    `files_scanned`.
    """
    if not pack_dir.is_dir() or pack_dir.is_symlink():
        return 0, 0
    total = unreadable = 0
    for dirpath, dirnames, filenames in os.walk(
            pack_dir, followlinks=False, onerror=_walk_error):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".jsonl"):
                continue
            path = Path(dirpath) / name
            try:
                mode = path.lstat().st_mode
            except OSError:
                continue
            if not stat.S_ISREG(mode):
                continue
            total += 1
            rel = path.relative_to(pack_dir).as_posix()
            below = any(rel == directory or rel.startswith(directory + "/")
                        for directory in unreadable_dirs)
            if below or not os.access(path, os.R_OK):
                unreadable += 1
    return total, unreadable


def expand_args(spec: CaseSpec, fixtures_dir: Path) -> tuple:
    pack_dir = fixtures_dir / spec.pack
    tokens = [token.replace("{pack}", str(pack_dir))
              .replace("{fixtures}", str(fixtures_dir))
              for token in spec.args]
    found = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--sessions-dir":
            if index + 1 >= len(tokens):
                raise SetupError("case %s: --sessions-dir without a value"
                                 % spec.cid)
            found.append(tokens[index + 1])
            index += 2
            continue
        if token.startswith("--sessions-dir="):
            found.append(token.split("=", 1)[1])
        index += 1
    if len(found) > 1:
        raise SetupError("case %s: more than one --sessions-dir" % spec.cid)
    if not found:
        tokens = ["--sessions-dir", str(pack_dir)] + tokens
        found = [str(pack_dir)]
    if not found[0]:
        raise SetupError("case %s: empty --sessions-dir" % spec.cid)
    return tuple(tokens), Path(found[0])


def _arg_int(tokens, name: str):
    """Last integer value of a repeatable `--name N` / `--name=N` token."""
    value = None
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == name and index + 1 < len(tokens):
            value = tokens[index + 1]
            index += 2
            continue
        if token.startswith(name + "="):
            value = token.split("=", 1)[1]
        index += 1
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _copy_fixture_tree(source: Path, target: Path) -> None:
    """Copy a pack without following symlinks; FIFOs via os.mkfifo."""
    with os.scandir(source) as iterator:
        entries = sorted(iterator, key=lambda entry: entry.name)
    for entry in entries:
        src = Path(entry.path)
        dst = target / entry.name
        info = entry.stat(follow_symlinks=False)
        if stat.S_ISLNK(info.st_mode):
            os.symlink(os.readlink(src), dst)
        elif stat.S_ISDIR(info.st_mode):
            dst.mkdir()
            _copy_fixture_tree(src, dst)
        elif stat.S_ISFIFO(info.st_mode):
            try:
                os.mkfifo(dst)
            except OSError as exc:
                raise SetupError("cannot recreate FIFO in sandbox %s: %s"
                                 % (dst, exc))
        elif stat.S_ISREG(info.st_mode):
            try:
                shutil.copyfile(src, dst)
            except OSError as exc:
                raise SetupError("cannot copy fixture %s into the sandbox "
                                 "(source fixtures must stay readable): %s"
                                 % (src, exc))
        # sockets/devices are ignored, matching the tool contract


def _create_fifo_safely(root: Path, rel: str, cid: str) -> None:
    """Create one FIFO without ever following a symlink ancestor.

    Phase 1 lstat-scans every existing ancestor and rejects symlinks or
    escape before any mkdir.  Phase 2 creates missing components one at a
    time with os.mkdir (never mkdir -p through a link), checking each new
    component's type and containment again.
    """
    root = Path(root)
    root_resolved = root.resolve()
    parts = rel.split("/")
    current = root
    missing_index = None
    for index, part in enumerate(parts[:-1]):
        nxt = current / part
        try:
            info = nxt.lstat()
        except FileNotFoundError:
            missing_index = index
            break
        except OSError as exc:
            raise SetupError("case %s: cannot stat FIFO ancestor in sandbox "
                             "%s: %s" % (cid, rel, exc))
        if stat.S_ISLNK(info.st_mode):
            raise SetupError(
                "case %s: FIFO ancestor is a symlink in the sandbox "
                "(refused before mkdir): %s" % (cid, rel))
        if not stat.S_ISDIR(info.st_mode):
            raise SetupError("case %s: FIFO ancestor is not a directory: %s"
                             % (cid, rel))
        try:
            nxt.resolve().relative_to(root_resolved)
        except ValueError:
            raise SetupError("case %s: FIFO ancestor escapes the sandbox: %s"
                             % (cid, rel))
        current = nxt
    if missing_index is not None:
        for part in parts[missing_index:-1]:
            current = current / part
            try:
                os.mkdir(current, 0o700)
            except FileExistsError:
                pass
            except OSError as exc:
                raise SetupError("case %s: cannot create FIFO parent in "
                                 "sandbox %s: %s" % (cid, rel, exc))
            try:
                info = current.lstat()
            except OSError as exc:
                raise SetupError("case %s: cannot lstat new FIFO parent %s: "
                                 "%s" % (cid, rel, exc))
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise SetupError("case %s: FIFO parent became unsafe: %s"
                                 % (cid, rel))
            try:
                current.resolve().relative_to(root_resolved)
            except ValueError:
                raise SetupError("case %s: FIFO parent escapes the sandbox: "
                                 "%s" % (cid, rel))
    leaf = current / parts[-1]
    if leaf.is_symlink() or leaf.exists():
        raise SetupError("case %s: FIFO target already exists in the "
                         "sandbox: %s" % (cid, rel))
    try:
        os.mkfifo(leaf)
    except OSError as exc:
        raise SetupError("case %s: cannot create FIFO in sandbox %s: %s"
                         % (cid, rel, exc))


def materialize_sandbox(case_dir: Path, pack_dir: Path,
                        spec: CaseSpec) -> Path:
    """Copy the source pack per case and apply transient modes there.

    Source fixtures stay readable (pins hash source bytes); chmod 000 exists
    only inside the sandbox and disappears with the output tree.
    """
    sandbox = Path(case_dir) / "sessions"
    if sandbox.exists() or sandbox.is_symlink():
        raise SetupError("case %s: sandbox already exists: %s"
                         % (spec.cid, sandbox))
    sandbox.mkdir(parents=True)
    _copy_fixture_tree(pack_dir, sandbox)
    root = sandbox.resolve()
    for rel in spec.unreadable_files:
        target = sandbox / rel
        if target.is_symlink() or not target.is_file():
            raise SetupError("case %s: unreadable_files target missing from "
                             "sandbox: %s" % (spec.cid, rel))
        try:
            target.resolve().relative_to(root)
        except ValueError:
            raise SetupError("case %s: sandbox target escapes the sandbox: "
                             "%s" % (spec.cid, rel))
        os.chmod(target, 0)
    for rel in spec.fifo_files:
        _create_fifo_safely(sandbox, rel, spec.cid)
    for rel in sorted(spec.unreadable_dirs,
                      key=lambda item: item.count("/"), reverse=True):
        target = sandbox / rel
        try:
            info = target.lstat()
        except OSError as exc:
            raise SetupError("case %s: unreadable_dirs target missing from "
                             "sandbox: %s (%s)" % (spec.cid, rel, exc))
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise SetupError("case %s: unreadable_dirs target is not a real "
                             "sandbox directory: %s" % (spec.cid, rel))
        try:
            target.resolve().relative_to(root)
        except ValueError:
            raise SetupError("case %s: unreadable_dirs escapes the sandbox: "
                             "%s" % (spec.cid, rel))
        os.chmod(target, 0)
    return sandbox


def restore_sandbox_modes(sandbox, spec: CaseSpec) -> None:
    """Restore chmod-000 directories so output cleanup cannot fail."""
    if sandbox is None:
        return
    for rel in sorted(spec.unreadable_dirs,
                      key=lambda item: item.count("/"), reverse=True):
        target = Path(sandbox) / rel
        try:
            if target.is_symlink():
                continue
            info = target.lstat()
            if stat.S_ISDIR(info.st_mode):
                os.chmod(target, 0o700)
        except OSError:
            continue


def _rebase_sessions(tokens, sessions_source, pack_dir: Path,
                     sandbox: Path, cid: str) -> tuple:
    """Map an explicit pack/subpath sessions dir into the sandbox.

    `--sessions-dir {pack}/root-link` becomes `<sandbox>/root-link` so a
    tracked symlink root can be exercised without following it; the source
    tree is never the run root.
    """
    source = Path(sessions_source)
    if not source.is_absolute():
        raise SetupError("case %s: explicit --sessions-dir must be absolute "
                         "(use {pack}/...)" % cid)
    source = Path(os.path.abspath(source))
    pack = Path(os.path.abspath(pack_dir))
    try:
        relative = source.relative_to(pack)
    except ValueError:
        raise SetupError("case %s: --sessions-dir must be the pack root or "
                         "a subpath of it" % cid)
    target = sandbox if relative == Path(".") else sandbox / relative
    return _replace_sessions_dir(tokens, target), target


def _replace_sessions_dir(tokens, sessions_dir) -> tuple:
    """Point every --sessions-dir at the sandbox, leaving other args alone."""
    out = []
    replaced = False
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--sessions-dir":
            if index + 1 >= len(tokens):
                raise SetupError("--sessions-dir without a value")
            out.extend(["--sessions-dir", str(sessions_dir)])
            replaced = True
            index += 2
            continue
        if token.startswith("--sessions-dir="):
            out.append("--sessions-dir=" + str(sessions_dir))
            replaced = True
        else:
            out.append(token)
        index += 1
    if not replaced:
        out = ["--sessions-dir", str(sessions_dir)] + out
    return tuple(out)


def run_tool(argv, env, cwd, timeout_s: int, cap: int):
    """Run the tool with both streams byte-capped.  Never unbounded."""
    try:
        proc = subprocess.Popen(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=str(cwd), env=env,
            start_new_session=True)
    except OSError as exc:
        return b"", b"", None, False, False, exc.__class__.__name__

    selector = selectors.DefaultSelector()
    buffers = {"out": bytearray(), "err": bytearray()}
    for name, pipe in (("out", proc.stdout), ("err", proc.stderr)):
        os.set_blocking(pipe.fileno(), False)
        selector.register(pipe, selectors.EVENT_READ, name)
    deadline = time.monotonic() + timeout_s
    timed_out = capped = False
    while selector.get_map():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            break
        for key, _ in selector.select(min(remaining, 0.1)):
            try:
                chunk = os.read(key.fileobj.fileno(), 65536)
            except BlockingIOError:
                continue
            except OSError:
                chunk = b""
            if not chunk:
                selector.unregister(key.fileobj)
                key.fileobj.close()
                continue
            buffers[key.data] += chunk
            if len(buffers[key.data]) > cap:
                capped = True
                break
        if capped:
            break
    if timed_out or capped:
        try:
            os.killpg(os.getpgid(proc.pid), 9)
        except (ProcessLookupError, PermissionError):
            pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass
    selector.close()
    return (bytes(buffers["out"]), bytes(buffers["err"]), proc.returncode,
            timed_out, capped, None)


# ---------------------------------------------------------------------------
# grading helpers
# ---------------------------------------------------------------------------


def validate_totals(value):
    if not isinstance(value, dict):
        return None, "totals_not_object"
    if set(value) != CLASS_SET:
        return None, "totals_keys"
    for cls in CLASSES:
        item = value[cls]
        if not is_int(item) or item < 0:
            return None, "totals_value:" + cls
    return {cls: value[cls] for cls in CLASSES}, None


def _validate_seat_item(item, index: int, reasons):
    if not isinstance(item, dict):
        reasons.append("seat_%d_not_object" % index)
        return None
    unknown = sorted(set(item) - SEAT_KEYS)
    if unknown:
        reasons.append("seat_%d_unknown_key:%s" % (index, unknown[0]))
    missing = sorted(REQUIRED_SEAT_KEYS - set(item))
    if missing:
        reasons.append("seat_%d_missing_key:%s" % (index, missing[0]))
        return None
    seat = item["seat"]
    if not isinstance(seat, str) or not seat or len(seat) > 1024 \
            or any(ord(ch) < 32 for ch in seat):
        reasons.append("seat_%d_seat_id" % index)
        return None
    prefix = item["prefix"]
    if not isinstance(prefix, str):
        reasons.append("seat_%d_prefix" % index)
    elif prefix != seat.split(".", 1)[0]:
        reasons.append("seat_%d_prefix_not_derived" % index)
    if item["class"] not in CLASS_SET:
        reasons.append("seat_%d_class" % index)
    for key in ("provider", "model"):
        if not (item[key] is None or isinstance(item[key], str)):
            reasons.append("seat_%d_%s" % (index, key))
    status = item["error_status"]
    if not (status is None or is_int(status)):
        reasons.append("seat_%d_error_status" % index)
    if type(item["retry_exhausted"]) is not bool:
        reasons.append("seat_%d_retry_exhausted" % index)
    retries = item["retries"]
    if not (retries is None or (is_int(retries) and retries >= 0)):
        reasons.append("seat_%d_retries" % index)
    code = item["error_code"]
    code_ok = (code is None or (is_int(code) and code >= 0)
               or (isinstance(code, str) and code.isdigit()
                   and len(code) <= 64))
    if not code_ok:
        reasons.append("seat_%d_error_code" % index)

    key = item.get("key")
    if key is not None:
        key_ok = (isinstance(key, str) and 0 < len(key) <= 4096
                  and not key.startswith("/")
                  and ".." not in key.split("/")
                  and all(ord(ch) >= 32 for ch in key))
        if not key_ok:
            reasons.append("seat_%d_key" % index)
    kind = item.get("kind")
    if kind is not None and (not isinstance(kind, str) or not kind
                             or any(ord(ch) < 32 for ch in kind)):
        reasons.append("seat_%d_kind" % index)
    terminal_ms = item.get("terminal_ms")
    if terminal_ms is not None and (not is_int(terminal_ms)
                                    or terminal_ms < 0):
        reasons.append("seat_%d_terminal_ms" % index)
    reason = item.get("reason")
    if reason is not None and reason not in SEAT_REASONS:
        reasons.append("seat_%d_reason" % index)
    return item


def _rows_sorted(rows) -> bool:
    seat_ids = [row["seat"] for row in rows]
    if seat_ids == sorted(seat_ids):
        return True
    keys = [row.get("key") for row in rows]
    return all(isinstance(key, str) for key in keys) \
        and keys == sorted(keys)


def validate_seats(value):
    """Project the contract's list, or a seat/key -> object map, to rows."""
    reasons = []
    rows = []
    if isinstance(value, list):
        for index, item in enumerate(value):
            row = _validate_seat_item(item, index, reasons)
            if row is not None:
                rows.append(row)
    elif isinstance(value, dict):
        keys = list(value)
        if keys != sorted(keys):
            reasons.append("seats_not_sorted")
        for index, (key, item) in enumerate(value.items()):
            row = _validate_seat_item(item, index, reasons)
            if row is None:
                continue
            identity = row.get("key") if isinstance(row.get("key"), str) \
                else row["seat"]
            if key not in (row["seat"], identity):
                reasons.append("seat_%d_key_mismatch" % index)
            rows.append(row)
    else:
        return None, ["seats_not_list_or_object"]
    if not _rows_sorted(rows):
        reasons.append("seats_not_sorted")
    keys = [row["key"] for row in rows if isinstance(row.get("key"), str)]
    if len(keys) != len(set(keys)):
        reasons.append("duplicate_seat_key")
    return rows, reasons


def forbidden_paths(obj, prefix=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = "%s/%s" % (prefix, key) if prefix else str(key)
            if key in FORBIDDEN_KEYS:
                yield path
            yield from forbidden_paths(value, path)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from forbidden_paths(value, "%s/%d" % (prefix, index))


def collect_canaries(pack_dir: Path) -> set:
    """Bounded scan of fixture message records for leak canaries.

    Only `type == "message"` records with a dict message are read; a
    credential_pin or any other record type is skipped unread, mirroring the
    tool contract.  A canary that is a substring of an output key, a class
    token, a seat id/prefix, or a provider/model value is exempt: the tool
    may emit those legitimately, so an exact match would be a false leak.
    """
    if not pack_dir.is_dir() or pack_dir.is_symlink():
        return set()
    vocabulary = " ".join(CLASSES + FINDINGS) + " " + " ".join(
        sorted(TOP_KEYS | SEAT_KEYS)) + " unknown"
    permitted = set()
    found = set()
    for dirpath, dirnames, filenames in os.walk(pack_dir, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.endswith(".jsonl"):
                continue
            path = Path(dirpath) / name
            if path.is_symlink() or not path.is_file():
                continue
            seat = name[: -len(".jsonl")]
            permitted.add(seat)
            permitted.add(seat.split(".", 1)[0])
            try:
                with open(path, "rb") as handle:
                    data = handle.read(MAX_TEST_BYTES)
            except OSError:
                continue
            for line in data.split(b"\n"):
                try:
                    record = strict_json(line.decode("utf-8"))
                except (UnicodeDecodeError, ValueError):
                    continue
                if not isinstance(record, dict) \
                        or record.get("type") != "message":
                    continue
                message = record.get("message")
                if not isinstance(message, dict):
                    continue
                provider = message.get("provider")
                model = message.get("model")
                if isinstance(provider, str):
                    permitted.add(provider)
                if isinstance(model, str):
                    permitted.add(model)
                permitted.add("%s/%s" % (
                    provider if isinstance(provider, str) else "unknown",
                    model if isinstance(model, str) else "unknown"))
                for key in ("errorMessage", "content"):
                    value = message.get(key)
                    if not isinstance(value, str):
                        continue
                    probe = value[:512]
                    if len(probe) < 8 or probe in vocabulary:
                        continue
                    found.add(probe)
    canaries = set()
    for probe in found:
        if any(probe in value for value in permitted):
            continue
        canaries.add(probe)
        if len(canaries) >= MAX_CANARIES:
            break
    return canaries


def compare_want(spec: CaseSpec, totals_row, rows, reasons) -> None:
    strict = spec.want_rc in (0, 1)
    if totals_row is not None:
        for cls, want in spec.want_totals.items():
            got = totals_row[cls]
            if not is_int(got) or got != want:
                reasons.append("want.totals.%s=%r" % (cls, got))
    elif strict:
        for cls in spec.want_totals:
            reasons.append("want.totals.%s=None" % cls)
    if rows is None or not (strict or spec.want_seats):
        return
    by_key = {}
    for row in rows:
        cls = row.get("class")
        key = row.get("key")
        if cls in CLASS_SET and isinstance(key, str) and key not in by_key:
            by_key[key] = cls
    missing = []
    for key, want in spec.want_seats.items():
        if key not in by_key:
            missing.append(key)
        elif by_key[key] != want:
            reasons.append("want.seat_class:%s" % key)
    if missing:
        reasons.append("want.seat_missing:%s" % missing[0])
    for row in rows:
        cls = row.get("class")
        key = row.get("key")
        if cls in CLASS_SET and isinstance(key, str) \
                and spec.want_seats.get(key) == cls:
            continue
        reasons.append("unexpected_seat:%s"
                       % (key if isinstance(key, str) else row["seat"]))
        break


def compare_independent_want(spec: CaseSpec, parsed, rows, reasons) -> None:
    """Compare want.reason / want.top / want.records exactly (JSON-type).

    Uses strict_eq: JSON true never equals 1, and 1.0 never equals integer 1.
    """
    if spec.want_reason is not UNSET:
        if not isinstance(parsed, dict) or "reason" not in parsed:
            reasons.append("want.reason=missing")
        elif not strict_eq(parsed["reason"], spec.want_reason):
            reasons.append("want.reason=%r" % (parsed.get("reason"),))
    for field, want in spec.want_top.items():
        if not isinstance(parsed, dict) or field not in parsed:
            reasons.append("want.top.%s=missing" % field)
        elif not strict_eq(parsed[field], want):
            reasons.append("want.top.%s=%r" % (field, parsed.get(field)))
    if not spec.want_records:
        return
    by_key = {}
    for row in rows or ():
        key = row.get("key")
        if isinstance(key, str):
            by_key[key] = row
    for key, fields in spec.want_records.items():
        row = by_key.get(key)
        if row is None:
            reasons.append("want.record_missing:%s" % key)
            continue
        for field, want in fields.items():
            if field not in row:
                reasons.append("want.record_field_missing:%s.%s"
                               % (key, field))
            elif not strict_eq(row[field], want):
                reasons.append("want.record:%s.%s=%r"
                               % (key, field, row.get(field)))


def evaluate(spec: CaseSpec, out: bytes, err: bytes, rc, timed_out: bool,
             capped: bool, exec_error, sessions_expected: Path,
             canaries, fixture_files: int, fixture_unreadable: int,
             prefix_filtered: bool, now_arg, settle_arg) -> tuple:
    reasons = []
    if timed_out:
        reasons.append("harness_timeout")
    if capped:
        reasons.append("tool_output_cap_exceeded")
    if exec_error:
        reasons.append("exec_error")
    if rc != spec.want_rc:
        reasons.append("rc=%r want=%d" % (rc, spec.want_rc))

    text = None
    try:
        text = out.decode("utf-8")
    except UnicodeDecodeError:
        reasons.append("stdout_not_utf8")
    parsed = None
    if text is not None:
        stripped = text.strip()
        if not stripped:
            reasons.append("stdout_empty")
        else:
            try:
                parsed = strict_json(stripped)
            except ValueError:
                reasons.append("stdout_not_single_json_object")
            else:
                if not isinstance(parsed, dict):
                    reasons.append("stdout_not_json_object")
                    parsed = None

    finding_id = parsed.get("finding_id") if parsed is not None else None
    if parsed is not None:
        if parsed.get("schema") != TOOL_SCHEMA:
            reasons.append("schema=%r" % (parsed.get("schema"),))
        allowed = TOP_KEYS if spec.want_rc != 2 else None
        if allowed is not None:
            unknown = sorted(set(parsed) - allowed)
            if unknown:
                reasons.append("unknown_key:" + ",".join(unknown))
        found_forbidden = sorted(set(forbidden_paths(parsed)))
        if found_forbidden:
            reasons.append("forbidden_key:" + found_forbidden[0])
        if finding_id != spec.want_finding_id:
            reasons.append("finding_id=%r want=%s"
                           % (finding_id, spec.want_finding_id))
        if rc in RC_FINDING_ID and finding_id != RC_FINDING_ID[rc]:
            reasons.append("finding_id_inconsistent_with_rc")

        sessions_dir = parsed.get("sessions_dir")
        if sessions_dir is not None:
            if not isinstance(sessions_dir, str):
                reasons.append("sessions_dir_not_string")
            else:
                try:
                    got_dir = Path(sessions_dir).resolve()
                except OSError:
                    got_dir = None
                if got_dir != sessions_expected:
                    reasons.append("sessions_dir_mismatch")

        if "files_scanned" in parsed:
            scanned = parsed["files_scanned"]
            if not is_int(scanned) or scanned < 0:
                reasons.append("files_scanned_not_int")

        # Amendment A1 additive scan metadata.  Each is validated when
        # present; a pre-A1 producer is not required to carry it.
        now_ms = parsed.get("now_ms")
        if now_ms is not None:
            if not is_int(now_ms) or now_ms < 0:
                reasons.append("now_ms_type")
            elif now_arg is not None and now_ms != now_arg:
                reasons.append("now_ms_mismatch")
        settle = parsed.get("settle_seconds")
        if settle is not None:
            if not is_int(settle) or settle < 0:
                reasons.append("settle_seconds_type")
            elif settle_arg is not None and settle != settle_arg:
                reasons.append("settle_seconds_mismatch")
        duplicate_stems = parsed.get("duplicate_stems")
        if duplicate_stems is not None:
            duplicate_ok = (
                (is_int(duplicate_stems) and duplicate_stems >= 0)
                or (isinstance(duplicate_stems, list)
                    and all(isinstance(item, str)
                            for item in duplicate_stems)))
            if not duplicate_ok:
                reasons.append("duplicate_stems_type")
        main_sessions = parsed.get("main_sessions")
        if main_sessions is not None \
                and (not is_int(main_sessions) or main_sessions < 0):
            reasons.append("main_sessions_type")

    totals_row = None
    rows = None
    graded_rows = None
    main_rows = None
    if spec.want_rc in (0, 1):
        if parsed is not None:
            required = ("schema", "sessions_dir", "files_scanned", "totals",
                        "retry_exhausted", "by_prefix",
                        "by_provider_model", "seats", "finding_id")
            missing = [key for key in required if key not in parsed]
            if missing:
                reasons.append("missing_key:" + ",".join(missing))

            totals_row, totals_error = validate_totals(parsed.get("totals"))
            if totals_error:
                reasons.append(totals_error)

            rows, seat_reasons = validate_seats(parsed.get("seats"))
            reasons.extend(seat_reasons)
            if rows is not None:
                graded_rows = [row for row in rows
                               if row.get("kind") != MAIN_KIND]
                main_rows = [row for row in rows
                             if row.get("kind") == MAIN_KIND]

            by_prefix, prefix_error = validate_totals_map(
                parsed.get("by_prefix"), "by_prefix")
            if prefix_error:
                reasons.append(prefix_error)
            by_pm, pm_error = validate_totals_map(
                parsed.get("by_provider_model"), "by_provider_model")
            if pm_error:
                reasons.append(pm_error)

            retry = parsed.get("retry_exhausted")
            retry_ok = type(retry) is bool or (is_int(retry) and retry >= 0)
            if not retry_ok:
                reasons.append("retry_exhausted_type")

            if totals_row is not None and graded_rows is not None \
                    and not seat_reasons:
                derived = {cls: 0 for cls in CLASSES}
                for row in graded_rows:
                    derived[row["class"]] += 1
                if derived != totals_row:
                    reasons.append("totals_mismatch_seats")
                expected_retry = sum(1 for row in graded_rows
                                     if row["retry_exhausted"])
                if type(retry) is bool:
                    if retry != (expected_retry > 0):
                        reasons.append("retry_exhausted_bool_mismatch")
                elif is_int(retry) and retry != expected_retry:
                    reasons.append("retry_exhausted_count_mismatch")
                if by_prefix is not None:
                    derived_prefix = {}
                    for row in graded_rows:
                        row_totals = derived_prefix.setdefault(
                            row["prefix"], {cls: 0 for cls in CLASSES})
                        row_totals[row["class"]] += 1
                    if by_prefix != derived_prefix:
                        reasons.append("by_prefix_mismatch")
                if by_pm is not None:
                    summed = {cls: 0 for cls in CLASSES}
                    for row_totals in by_pm.values():
                        for cls in CLASSES:
                            summed[cls] += row_totals[cls]
                    if summed != totals_row:
                        reasons.append("by_provider_model_sum_mismatch")
                scanned = parsed.get("files_scanned")
                if is_int(scanned):
                    loose = prefix_filtered or fixture_unreadable > 0
                    if loose:
                        if not (len(rows) <= scanned <= fixture_files):
                            reasons.append("files_scanned_out_of_range")
                    elif scanned != fixture_files \
                            or len(rows) != fixture_files:
                        reasons.append("files_scanned_mismatch")
                if main_sessions is not None and is_int(main_sessions) \
                        and main_sessions != len(main_rows):
                    reasons.append("main_sessions_mismatch")

            if totals_row is not None:
                dead_total = sum(totals_row[cls] for cls in DEAD_CLASSES)
                if rc == 0 and dead_total:
                    reasons.append("rc0_with_dead_totals")
                if rc == 1 and not dead_total:
                    reasons.append("rc1_without_dead_totals")

            compare_want(spec, totals_row, graded_rows, reasons)
    else:
        if parsed is not None:
            if "totals" in parsed:
                totals_row, totals_error = validate_totals(parsed["totals"])
                if totals_error:
                    reasons.append(totals_error)
            if "seats" in parsed:
                rows, seat_reasons = validate_seats(parsed["seats"])
                reasons.extend(seat_reasons)
            compare_want(spec, totals_row, rows, reasons)

    compare_independent_want(spec, parsed, rows, reasons)

    if canaries and (text is not None or err):
        haystack = (text or "") + "\n" + err.decode("utf-8", "replace")
        for canary in sorted(canaries):
            if canary in haystack:
                reasons.append("fixture_text_echoed")
                break

    deduped = []
    for reason in reasons:
        if reason not in deduped:
            deduped.append(reason)
    deduped = [one_line(reason, 200) for reason in deduped[:MAX_REASONS]]

    observed = {
        "rc": rc,
        "finding_id": finding_id,
        "files_scanned": parsed.get("files_scanned")
        if isinstance(parsed, dict) else None,
        "seat_count": len(rows) if rows is not None else None,
        "main_sessions": parsed.get("main_sessions")
        if isinstance(parsed, dict) else None,
        "now_ms": parsed.get("now_ms") if isinstance(parsed, dict) else None,
        "totals": totals_row,
    }
    return (not deduped), deduped, observed


def validate_totals_map(value, label: str):
    if not isinstance(value, dict):
        return None, label + "_not_object"
    rows = {}
    for key, item in value.items():
        if not isinstance(key, str):
            return None, label + "_key"
        row, error = validate_totals(item)
        if error:
            return None, "%s:%s" % (label, error)
        rows[key] = row
    return rows, None


# ---------------------------------------------------------------------------
# manifest and gate mode
# ---------------------------------------------------------------------------


def write_manifest(output: Path, doc: dict) -> None:
    atomic_json(Path(output) / "run-manifest.json", doc)


def capture_revision() -> dict:
    """Branch-anchored revision metadata.

    Branch resolution: attached HEAD -> origin/HEAD -> unique
    refs/heads/master|main.  `branch_tip` is the receipt (rev-parse
    refs/heads/<branch>); `head` is diagnostic only and is never a receipt.
    GIT_* variables (including GIT_TRACE* and GIT_CONFIG*) are scrubbed and
    git runs with --no-optional-locks and core.fsmonitor=false so metadata
    collection cannot write or be redirected by an ambient repository.
    """
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("GIT_")}
    base = ["git", "--no-optional-locks", "-c", "core.fsmonitor=false"]

    def git(args):
        try:
            proc = subprocess.run(base + args, cwd=str(REPO),
                                  capture_output=True, text=True,
                                  timeout=10, env=env)
        except (OSError, subprocess.SubprocessError):
            return None
        if proc.returncode != 0:
            return None
        return proc.stdout.strip() or None

    def ref_exists(ref: str) -> bool:
        return git(["rev-parse", "--verify", "--quiet", ref]) is not None

    head = git(["rev-parse", "--verify", "HEAD"])
    branch = None
    branch_source = None

    attached = git(["symbolic-ref", "-q", "HEAD"])
    if attached and attached.startswith("refs/heads/"):
        candidate = attached[len("refs/heads/"):]
        if candidate and ref_exists("refs/heads/" + candidate):
            branch = candidate
            branch_source = "attached"

    if branch is None:
        origin = git(["symbolic-ref", "-q", "refs/remotes/origin/HEAD"])
        if origin and origin.startswith("refs/remotes/origin/"):
            candidate = origin[len("refs/remotes/origin/"):]
            if candidate and ref_exists("refs/heads/" + candidate):
                branch = candidate
                branch_source = "origin-head"

    if branch is None:
        present = [name for name in ("master", "main")
                   if ref_exists("refs/heads/" + name)]
        if len(present) == 1:
            branch = present[0]
            branch_source = "unique-master-main"

    branch_tip = git(["rev-parse", "--verify", "refs/heads/" + branch]) \
        if branch is not None else None
    return {
        "branch": branch,
        "branch_source": branch_source or "unresolved",
        "branch_tip": branch_tip,
        "receipt_ref": "refs/heads/" + branch if branch is not None else None,
        "head": head,
    }


def run_gate(args, gate_sha: str) -> int:
    if not args.output:
        raise SetupError("--output DIR is required unless --selftest")
    fixtures_raw = Path(args.fixtures)
    if fixtures_raw.is_symlink():
        raise SetupError("fixtures directory must not be a symlink: %s"
                         % fixtures_raw)
    fixtures_dir = fixtures_raw.resolve()
    tool_path = Path(args.tool).resolve()
    if fixtures_dir.is_symlink() or not fixtures_dir.is_dir():
        if fixtures_dir.exists():
            raise SetupError("fixtures directory not a plain directory: %s"
                             % rel_or_abs(fixtures_dir))
        raise SetupError("fixtures directory missing: %s"
                         % rel_or_abs(fixtures_dir))
    expected_path = fixtures_dir / "expected.json"
    guard_output(Path(args.output), [
        (fixtures_dir, "the fixture directory"),
        (expected_path, "the expected table"),
        (tool_path, "the tool under test"),
    ])

    specs, expected_raw, pins = load_expected(fixtures_dir)
    actual_pins = compute_pins(fixtures_dir)
    inputs_before = snapshot_tree(fixtures_dir)
    if inputs_before.get("expected.json") != sha256_bytes(expected_raw):
        raise SetupError("expected table changed while loading; rerun")

    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    for sub in ("runs", "cases"):
        (output / sub).mkdir(parents=True, exist_ok=True)
    atomic_bytes(output / "expected.json", expected_raw)

    tool_present = tool_path.is_file() and not tool_path.is_symlink()
    manifest = {
        "schema": SCHEMA,
        "gate": "tools/mori-round17-seat-regressions.py",
        "gate_sha256": gate_sha,
        "tool": {
            "path": rel_or_abs(tool_path),
            "present": tool_present,
            "sha256": sha256_file(tool_path) if tool_present else None,
        },
        "fixtures": {
            "dir": rel_or_abs(fixtures_dir),
            "expected": {
                "path": rel_or_abs(expected_path),
                "sha256": sha256_bytes(expected_raw),
            },
            "pins": {
                "declared": len(pins),
                "declared_sha256": sha256_bytes(canonical(pins)
                                                .encode("utf-8")),
                "verified": None,
                "missing": [],
                "extra": [],
                "mismatched": [],
            },
            "inputs_before": inputs_before,
            "inputs_after": None,
            "inputs_changed": None,
        },
        "git": capture_revision(),
        "cases": [],
        "summary": None,
        "verdict": None,
        "exit_code": None,
    }

    pin_check = compare_pins(pins, actual_pins)
    manifest["fixtures"]["pins"].update({
        "verified": pin_check["ok"],
        "missing": pin_check["missing"],
        "extra": pin_check["extra"],
        "mismatched": pin_check["mismatched"],
    })
    if not pin_check["ok"]:
        # Persisted pin evidence is checked before any tool run: a moved
        # fixture tree is setup tamper, never a tool mismatch.
        manifest["summary"] = {
            "total": len(specs), "matched": 0, "mismatched": 0,
            "capability_absent": 0, "pack_changed": 0,
        }
        manifest["verdict"] = "snapshot_tampered"
        manifest["exit_code"] = 2
        write_manifest(output, manifest)
        print("GATE snapshot_tampered: missing=%s extra=%s mismatched=%s"
              % (",".join(pin_check["missing"]) or "-",
                 ",".join(pin_check["extra"]) or "-",
                 ",".join(pin_check["mismatched"]) or "-"),
              file=sys.stderr)
        return 2

    if not tool_present:
        # Entering-capability baseline: fixtures validated above; every case
        # is recorded absent, never green and never a production bug claim.
        for spec in specs:
            tokens, sessions = expand_args(spec, fixtures_dir)
            sessions = Path(os.path.abspath(sessions))
            digest = pack_tree_digest(fixtures_dir / spec.pack)
            manifest["cases"].append({
                "id": spec.cid,
                "pack": spec.pack,
                "argv": list(tokens),
                "sessions_dir": str(sessions),
                "sessions_arg": str(sessions),
                "status": "capability_absent",
                "ok": False,
                "reasons": ["capability_absent"],
                "observed": None,
                "pack_before_sha256": digest,
                "pack_after_sha256": digest,
                "pack_changed": False,
                "sandbox": None,
                "unreadable_files": list(spec.unreadable_files),
                "fifo_files": list(spec.fifo_files),
                "unreadable_dirs": list(spec.unreadable_dirs),
                "stdout_sha256": None,
                "stderr_sha256": None,
            })
        inputs_after = snapshot_tree(fixtures_dir)
        manifest["fixtures"]["inputs_after"] = inputs_after
        manifest["fixtures"]["inputs_changed"] = diff_snapshots(
            inputs_before, inputs_after)
        manifest["summary"] = {
            "total": len(specs), "matched": 0, "mismatched": 0,
            "capability_absent": len(specs), "pack_changed": 0,
        }
        manifest["verdict"] = "capability_absent"
        manifest["exit_code"] = 1
        write_manifest(output, manifest)
        print("GATE capability_absent: --tool %s does not exist; %d cases "
              "recorded absent (rc1), fixture digests enforced"
              % (tool_path, len(specs)))
        return 1

    matched = mismatched = 0
    pack_changed_any = False
    for spec in specs:
        tokens, sessions_source = expand_args(spec, fixtures_dir)
        case_dir = output / "cases" / spec.cid
        case_dir.mkdir(parents=True, exist_ok=True)
        pack_dir = fixtures_dir / spec.pack
        pack_exists = pack_dir.is_dir() and not pack_dir.is_symlink()
        sandbox = materialize_sandbox(case_dir, pack_dir, spec) \
            if pack_exists else None
        if sandbox is not None:
            tokens, run_sessions = _rebase_sessions(
                tokens, sessions_source, pack_dir, sandbox, spec.cid)
        else:
            run_sessions = Path(os.path.abspath(sessions_source))
            tokens = _replace_sessions_dir(tokens, run_sessions)
        sessions = Path(run_sessions).resolve()
        pack_before = pack_tree_digest(pack_dir)
        canaries = collect_canaries(pack_dir)
        fixture_files, fixture_unreadable = fixture_scan_bounds(
            pack_dir, spec.unreadable_dirs)
        prefix_filtered = any(
            token == "--prefix" or token.startswith("--prefix=")
            for token in tokens)
        now_arg = _arg_int(tokens, "--now-ms")
        settle_arg = _arg_int(tokens, "--settle-seconds")

        env = dict(BASE_ENV)
        env["HOME"] = str(case_dir)
        argv = [sys.executable, str(tool_path)] + list(tokens)
        out, err, rc, timed_out, capped, exec_error = run_tool(
            argv, env, case_dir, args.run_timeout, args.capture_cap)
        restore_sandbox_modes(sandbox, spec)

        atomic_bytes(output / "runs" / ("%s.stdout" % spec.cid), out)
        atomic_bytes(output / "runs" / ("%s.stderr" % spec.cid), err)

        ok, reasons, observed = evaluate(
            spec, out, err, rc, timed_out, capped, exec_error, sessions,
            canaries, fixture_files, fixture_unreadable, prefix_filtered,
            now_arg, settle_arg)

        pack_after = pack_tree_digest(pack_dir)
        pack_changed = pack_after != pack_before
        pack_changed_any = pack_changed_any or pack_changed

        if ok:
            matched += 1
        else:
            mismatched += 1
        manifest["cases"].append({
            "id": spec.cid,
            "pack": spec.pack,
            "argv": list(tokens),
            "sessions_dir": str(sessions),
            "sessions_arg": str(run_sessions),
            "status": "match" if ok else "mismatch",
            "ok": ok,
            "reasons": reasons,
            "observed": observed,
            "pack_before_sha256": pack_before,
            "pack_after_sha256": pack_after,
            "pack_changed": pack_changed,
            "sandbox": rel_or_abs(sandbox) if sandbox is not None else None,
            "unreadable_files": list(spec.unreadable_files),
            "fifo_files": list(spec.fifo_files),
            "unreadable_dirs": list(spec.unreadable_dirs),
            "stdout_sha256": sha256_bytes(out),
            "stderr_sha256": sha256_bytes(err),
            "stdout_bytes": len(out),
            "stderr_bytes": len(err),
        })

    inputs_after = snapshot_tree(fixtures_dir)
    changed = diff_snapshots(inputs_before, inputs_after)
    manifest["fixtures"]["inputs_after"] = inputs_after
    manifest["fixtures"]["inputs_changed"] = changed
    manifest["summary"] = {
        "total": len(specs), "matched": matched, "mismatched": mismatched,
        "capability_absent": 0, "pack_changed": sum(
            1 for case in manifest["cases"] if case["pack_changed"]),
    }

    if changed or pack_changed_any:
        manifest["verdict"] = "tamper:inputs-changed"
        manifest["exit_code"] = 2
        write_manifest(output, manifest)
        detail = ",".join(changed) if changed else "per-case pack digest"
        print("GATE tamper: fixture inputs changed during run: %s" % detail,
              file=sys.stderr)
        return 2

    verdict = "ok" if mismatched == 0 else "mismatch"
    manifest["verdict"] = verdict
    manifest["exit_code"] = 0 if mismatched == 0 else 1
    write_manifest(output, manifest)
    print("GATE %s: %d/%d cases matched (%s)"
          % (verdict, matched, len(specs), rel_or_abs(output)))
    return manifest["exit_code"]


def diff_snapshots(before: dict, after: dict) -> list:
    changed = []
    for key in sorted(set(before) | set(after)):
        if before.get(key) != after.get(key):
            changed.append(key)
    return changed


# ---------------------------------------------------------------------------
# selftest — tiny fake tool and fixtures under $TMPDIR; never the production
# tool, production fixtures or the lane
# ---------------------------------------------------------------------------


_STUB_TOOL = r'''
import json
import os
import stat
import sys

SCHEMA = "mori-seat-terminal-v1"
CLASSES = (
    "completed", "aborted", "dead_rate_limit", "dead_quota",
    "dead_error_other", "error_unsettled", "incomplete", "unavailable",
)
FINDING_OK = "MORI_SEAT_TERMINAL_OK"
FINDING_DEAD = "MORI_SEAT_TERMINAL_DEAD"
FINDING_SETUP = "MORI_SEAT_TERMINAL_SETUP"
MAIN_KIND = "main"
DEFAULT_NOW_MS = 1700000000000


def emit(obj, rc):
    sys.stdout.write(json.dumps(obj, sort_keys=True) + "\n")
    sys.exit(rc)


def make_seat(name, cls, provider, model, **extra):
    row = {"seat": name, "prefix": name.split(".", 1)[0], "class": cls,
           "provider": provider, "model": model, "error_status": None,
           "retry_exhausted": False, "retries": None, "error_code": None,
           "key": name, "kind": "subagent", "terminal_ms": None,
           "reason": None}
    row.update(extra)
    return row


def totals(seats):
    row = {cls: 0 for cls in CLASSES}
    for seat in seats:
        row[seat["class"]] += 1
    return row


def main():
    args = sys.argv[1:]
    sessions = None
    source = None
    now_ms = DEFAULT_NOW_MS
    settle_seconds = 900
    index = 0
    while index < len(args):
        token = args[index]
        if token == "--sessions-dir" and index + 1 < len(args):
            sessions = args[index + 1]
            index += 2
            continue
        if token.startswith("--sessions-dir="):
            sessions = token.split("=", 1)[1]
        if token == "--source" and index + 1 < len(args):
            source = args[index + 1]
            index += 2
            continue
        if token.startswith("--source="):
            source = token.split("=", 1)[1]
        if token == "--now-ms" and index + 1 < len(args):
            now_ms = int(args[index + 1])
            index += 2
            continue
        if token.startswith("--now-ms="):
            now_ms = int(token.split("=", 1)[1])
        if token == "--settle-seconds" and index + 1 < len(args):
            settle_seconds = int(args[index + 1])
            index += 2
            continue
        if token.startswith("--settle-seconds="):
            settle_seconds = int(token.split("=", 1)[1])
        index += 1
    if not sessions:
        emit({"schema": SCHEMA, "finding_id": FINDING_SETUP,
              "reason": "sessions-dir-required"}, 2)
    if os.path.islink(sessions):
        emit({"schema": SCHEMA, "sessions_dir": sessions,
              "finding_id": FINDING_SETUP, "reason": "root-symlink"}, 2)
    if not os.path.isdir(sessions):
        emit({"schema": SCHEMA, "sessions_dir": sessions,
              "finding_id": FINDING_SETUP,
              "reason": "unavailable-dir"}, 2)
    if os.path.exists(os.path.join(sessions, "drift-arm.flag")):
        with open(os.path.join(source or sessions, "drift.jsonl"), "a",
                  encoding="utf-8") as handle:
            handle.write('{"type":"message","message":{"role":"assistant",'
                         '"stopReason":"stop"}}\n')
    if os.path.exists(os.path.join(sessions, "dir-arm.flag")):
        locked_dir = os.path.join(sessions, "locked-dir")
        try:
            mode_zero = (os.stat(locked_dir).st_mode & 0o777) == 0
        except OSError:
            mode_zero = False
        if mode_zero:
            emit({"schema": SCHEMA, "sessions_dir": sessions,
                  "finding_id": FINDING_SETUP,
                  "reason": "walk-error"}, 2)
        emit({"schema": SCHEMA, "sessions_dir": sessions,
              "finding_id": FINDING_SETUP,
              "reason": "dir-mode-not-applied"}, 2)
    if os.path.exists(os.path.join(sessions, "readability-arm.flag")):
        locked = os.path.join(sessions, "Zeta.six.jsonl")
        try:
            readable = (os.stat(locked).st_mode & 0o444) != 0
        except OSError:
            readable = False
        seats = [make_seat("Zeta.six",
                           "completed" if readable else "unavailable",
                           "anthropic", "m1")]
    elif os.path.exists(os.path.join(sessions, "fifo-arm.flag")):
        pipe = os.path.join(sessions, "pipe.jsonl")
        try:
            is_fifo = stat.S_ISFIFO(os.lstat(pipe).st_mode)
        except OSError:
            is_fifo = False
        if not is_fifo:
            emit({"schema": SCHEMA, "sessions_dir": sessions,
                  "finding_id": FINDING_SETUP,
                  "reason": "missing-generated-fifo"}, 2)
        seats = []
    elif os.path.exists(os.path.join(sessions, "main-arm.flag")):
        seats = [
            make_seat("2026-10-20T12-00-00Z_abc123", "completed",
                      "openai", "gpt-synthetic", kind=MAIN_KIND),
            make_seat("Alpha.one", "completed", "anthropic", "m1"),
        ]
    elif os.path.exists(os.path.join(sessions, "dead-arm.flag")) \
            or os.path.exists(os.path.join(sessions, "wrong-type-arm.flag")):
        seats = [make_seat("Beta.two", "dead_rate_limit", "zai", "glm",
                           error_status=429, retry_exhausted=True,
                           retries=10, error_code=1302)]
    else:
        seats = [make_seat("Alpha.one", "completed", "anthropic", "m1")]
    if os.path.exists(os.path.join(sessions, "leak-arm.flag")):
        seats[0]["errorMessage"] = "LEAK-CANARY"
    seats.sort(key=lambda row: row["key"])
    graded = [row for row in seats if row.get("kind") != MAIN_KIND]
    by_prefix = {}
    for seat in graded:
        same = [row for row in graded if row["prefix"] == seat["prefix"]]
        by_prefix.setdefault(seat["prefix"], totals(same))
    by_pm = {}
    for seat in graded:
        key = "%s/%s" % (seat["provider"], seat["model"])
        same = [row for row in graded
                if (row["provider"], row["model"]) ==
                (seat["provider"], seat["model"])]
        by_pm.setdefault(key, totals(same))
    dead = sum(1 for seat in graded if seat["class"].startswith("dead_"))
    wrong_type = os.path.exists(os.path.join(sessions,
                                              "wrong-type-arm.flag"))
    if wrong_type:
        seats[0]["error_status"] = True
    main_count = len(seats) - len(graded)
    shaped = seats
    if os.path.exists(os.path.join(sessions, "dict-arm.flag")):
        shaped = {seat["seat"]: seat for seat in seats}
    if os.path.exists(os.path.join(sessions, "no-key-arm.flag")):
        shaped = [{key: value for key, value in row.items()
                   if key not in ("key", "prefix")} for row in seats]
    emit({"schema": SCHEMA, "sessions_dir": sessions,
          "files_scanned": len(seats), "totals": totals(graded),
          "retry_exhausted": sum(1 for seat in graded
                                 if seat["retry_exhausted"]),
          "by_prefix": by_prefix, "by_provider_model": by_pm,
          "seats": shaped,
          "now_ms": now_ms, "settle_seconds": settle_seconds,
          "main_sessions": True if wrong_type else main_count,
          "duplicate_stems": 0,
          "finding_id": FINDING_DEAD if dead else FINDING_OK},
         1 if dead else 0)


main()
'''


_SELFTEST_NOW_MS = 1700000000000


def _totals(**overrides) -> dict:
    row = {cls: 0 for cls in CLASSES}
    row.update(overrides)
    return row


def _case_ok() -> dict:
    return {
        "id": "st-ok", "pack": "pack-ok",
        "args": ["--sessions-dir", "{pack}",
                 "--now-ms", str(_SELFTEST_NOW_MS)],
        "want": {"rc": 0, "finding_id": FINDING_OK,
                 "totals": _totals(completed=1),
                 "seats": {"Alpha.one": "completed"}},
    }


def _case_dead() -> dict:
    return {
        "id": "st-dead", "pack": "pack-dead",
        "args": ["--sessions-dir", "{pack}",
                 "--now-ms", str(_SELFTEST_NOW_MS)],
        "want": {"rc": 1, "finding_id": FINDING_DEAD,
                 "totals": _totals(dead_rate_limit=1),
                 "seats": {"Beta.two": "dead_rate_limit"},
                 "records": {"Beta.two": {
                     "key": "Beta.two", "prefix": "Beta",
                     "class": "dead_rate_limit", "error_status": 429,
                     "retries": 10, "error_code": 1302,
                     "retry_exhausted": True, "reason": None}}},
    }


def _case_setup() -> dict:
    return {
        "id": "st-setup", "pack": "pack-absent",
        "args": ["--sessions-dir", "{pack}",
                 "--now-ms", str(_SELFTEST_NOW_MS)],
        "want": {"rc": 2, "finding_id": FINDING_SETUP,
                 "reason": "unavailable-dir"},
    }


def _write_line(pack: Path, name: str, record: dict) -> None:
    (pack / name).write_text(
        json.dumps(record, separators=(",", ":")) + "\n", encoding="utf-8")


def _selftest_tree(root: Path, kind: str) -> Path:
    fixtures = root / ("fixtures-" + kind)
    fixtures.mkdir()
    message = {"type": "message",
               "message": {"role": "assistant", "stopReason": "stop"}}

    ok_pack = fixtures / "pack-ok"
    ok_pack.mkdir()
    _write_line(ok_pack, "Alpha.one.jsonl", message)
    (ok_pack / "Linked.jsonl").symlink_to("Alpha.one.jsonl")

    if kind in ("green", "mismatch", "absent", "guard", "nonempty",
                "pintamper"):
        dead_pack = fixtures / "pack-dead"
        dead_pack.mkdir()
        _write_line(dead_pack, "Beta.two.jsonl",
                    {"type": "message",
                     "message": {"role": "assistant", "stopReason": "error",
                                 "errorStatus": 429,
                                 "errorMessage": "429 rate_limit"}})
        (dead_pack / "dead-arm.flag").write_text("", encoding="utf-8")
        cases = [_case_ok(), _case_dead(), _case_setup()]
        if kind == "green":
            cases[0] = dict(cases[0], fifo_files=["Pipe.jsonl"])
    elif kind == "drift":
        drift_pack = fixtures / "pack-drift"
        drift_pack.mkdir()
        _write_line(drift_pack, "Gamma.three.jsonl", message)
        (drift_pack / "drift-arm.flag").write_text("", encoding="utf-8")
        drift_case = dict(_case_ok(), pack="pack-drift")
        # Selftest-only arg: the fake tool writes to the source pack, not the
        # sandbox, so runtime input-drift detection is exercised.
        drift_case["args"] = list(drift_case["args"]) + [
            "--source", "{pack}"]
        cases = [drift_case]
    elif kind == "leak":
        leak_pack = fixtures / "pack-leak"
        leak_pack.mkdir()
        _write_line(leak_pack, "Delta.four.jsonl", message)
        (leak_pack / "leak-arm.flag").write_text("", encoding="utf-8")
        cases = [dict(_case_ok(), pack="pack-leak", id="st-leak")]
    elif kind == "dict":
        dict_pack = fixtures / "pack-dict"
        dict_pack.mkdir()
        _write_line(dict_pack, "Epsilon.five.jsonl", message)
        (dict_pack / "dict-arm.flag").write_text("", encoding="utf-8")
        cases = [dict(_case_ok(), pack="pack-dict", id="st-dict")]
    elif kind == "prefix":
        prefix_pack = fixtures / "pack-prefix"
        prefix_pack.mkdir()
        _write_line(prefix_pack, "Alpha.one.jsonl", message)
        _write_line(prefix_pack, "Beta.two.jsonl", message)
        cases = [dict(_case_ok(), pack="pack-prefix", id="st-prefix",
                      args=["--now-ms", str(_SELFTEST_NOW_MS),
                            "--prefix", "Alpha"])]
    elif kind == "main":
        main_pack = fixtures / "pack-main"
        main_pack.mkdir()
        _write_line(main_pack, "Alpha.one.jsonl", message)
        _write_line(main_pack, "2026-10-20T12-00-00Z_abc123.jsonl", message)
        (main_pack / "main-arm.flag").write_text("", encoding="utf-8")
        main_case = dict(_case_ok(), pack="pack-main", id="st-main")
        main_case["want"] = dict(main_case["want"],
                                 top={"main_sessions": 1,
                                      "duplicate_stems": 0})
        cases = [main_case]
    elif kind == "scan":
        scan_pack = fixtures / "pack-scan"
        scan_pack.mkdir()
        _write_line(scan_pack, "Alpha.one.jsonl", message)
        _write_line(scan_pack, "Beta.two.jsonl", message)
        cases = [dict(_case_ok(), pack="pack-scan", id="st-scan")]
    elif kind == "fifo":
        fifo_pack = fixtures / "pack-fifo"
        fifo_pack.mkdir()
        (fifo_pack / "fifo-arm.flag").write_text("", encoding="utf-8")
        cases = [{
            "id": "st-fifo", "pack": "pack-fifo",
            "args": ["--now-ms", str(_SELFTEST_NOW_MS)],
            "fifo_files": ["pipe.jsonl"],
            "want": {"rc": 0, "finding_id": FINDING_OK,
                     "totals": _totals(), "seats": {}},
        }]
    elif kind == "unreadable":
        unreadable_pack = fixtures / "pack-unreadable"
        unreadable_pack.mkdir()
        (unreadable_pack / "Zeta.six.jsonl").write_text("", encoding="utf-8")
        (unreadable_pack / "readability-arm.flag").write_text(
            "", encoding="utf-8")
        cases = [dict(
            _case_ok(), pack="pack-unreadable", id="st-unreadable",
            args=["--now-ms", str(_SELFTEST_NOW_MS)],
            unreadable_files=["Zeta.six.jsonl"],
            want={"rc": 0, "finding_id": FINDING_OK,
                  "totals": _totals(unavailable=1),
                  "seats": {"Zeta.six": "unavailable"}})]
    elif kind == "trap":
        trap_pack = fixtures / "pack-trap"
        trap_pack.mkdir()
        escape_target = root / "escape-target"
        (trap_pack / "link").symlink_to(str(escape_target))
        cases = [{
            "id": "st-trap", "pack": "pack-trap", "args": [],
            "fifo_files": ["link/new/pipe.jsonl"],
            "want": {"rc": 2, "finding_id": FINDING_SETUP},
        }]
    elif kind == "dirs":
        dirs_pack = fixtures / "pack-dirs"
        dirs_pack.mkdir()
        locked_dir = dirs_pack / "locked-dir"
        locked_dir.mkdir()
        _write_line(locked_dir, "inner.jsonl", message)
        (dirs_pack / "dir-arm.flag").write_text("", encoding="utf-8")
        cases = [{
            "id": "st-dir", "pack": "pack-dirs",
            "args": ["--now-ms", str(_SELFTEST_NOW_MS)],
            "unreadable_dirs": ["locked-dir"],
            "want": {"rc": 2, "finding_id": FINDING_SETUP,
                     "reason": "walk-error"},
        }]
    elif kind == "rootlink":
        rootlink_pack = fixtures / "pack-rootlink"
        rootlink_pack.mkdir()
        real_dir = rootlink_pack / "real-dir"
        real_dir.mkdir()
        _write_line(real_dir, "completed.jsonl", message)
        (rootlink_pack / "root-link").symlink_to("real-dir")
        cases = [{
            "id": "st-rootlink", "pack": "pack-rootlink",
            "args": ["--sessions-dir", "{pack}/root-link",
                     "--now-ms", str(_SELFTEST_NOW_MS)],
            "want": {"rc": 2, "finding_id": FINDING_SETUP,
                     "reason": "root-symlink"},
        }]
    elif kind == "nokey":
        nokey_pack = fixtures / "pack-nokey"
        nokey_pack.mkdir()
        _write_line(nokey_pack, "Alpha.one.jsonl", message)
        (nokey_pack / "no-key-arm.flag").write_text("", encoding="utf-8")
        cases = [dict(_case_ok(), pack="pack-nokey", id="st-nokey")]
    elif kind == "wrongtype":
        wrong_pack = fixtures / "pack-wrongtype"
        wrong_pack.mkdir()
        _write_line(wrong_pack, "Beta.two.jsonl",
                    {"type": "message",
                     "message": {"role": "assistant", "stopReason": "error",
                                 "errorStatus": 429,
                                 "errorMessage": "429 rate_limit"}})
        (wrong_pack / "wrong-type-arm.flag").write_text(
            "", encoding="utf-8")
        cases = [{
            "id": "st-wrongtype", "pack": "pack-wrongtype",
            "args": ["--now-ms", str(_SELFTEST_NOW_MS)],
            "want": {"rc": 1, "finding_id": FINDING_DEAD,
                     "totals": _totals(dead_rate_limit=1),
                     "seats": {"Beta.two": "dead_rate_limit"},
                     "records": {"Beta.two": {"error_status": 429}},
                     "top": {"main_sessions": 0}},
        }]
    else:
        raise AssertionError("unknown selftest tree kind %s" % kind)

    if kind == "mismatch":
        # The fake tool answers contract-correctly (rc1 dead); this want is
        # internally coherent but factually wrong, producing a real rc1.
        cases[1] = {
            "id": "st-dead", "pack": "pack-dead",
            "args": ["--sessions-dir", "{pack}",
                     "--now-ms", str(_SELFTEST_NOW_MS)],
            "want": {"rc": 0, "finding_id": FINDING_OK,
                     "totals": _totals(completed=1),
                     "seats": {"Beta.two": "completed"}},
        }

    pins = compute_pins(fixtures)
    atomic_json(fixtures / "expected.json",
                {"schema": EXPECTED_SCHEMA, "cases": cases, "pins": pins})
    if kind == "pintamper":
        # Persisted pins were computed above; the tree now moves under them.
        with open(ok_pack / "Alpha.one.jsonl", "ab") as handle:
            handle.write(b"\n")
    return fixtures


def _gate_proc(gate: Path, argv: list):
    return subprocess.run([sys.executable, str(gate)] + argv,
                          capture_output=True, text=True, timeout=300,
                          env=dict(os.environ))


def _assert(condition, label: str, proc=None) -> None:
    if condition:
        return
    detail = ""
    if proc is not None:
        detail = "\nstdout: %s\nstderr: %s" % (one_line(proc.stdout),
                                               one_line(proc.stderr))
    raise AssertionError("%s%s" % (label, detail))


def _manifest(output: Path) -> dict:
    return strict_json((Path(output) / "run-manifest.json").read_text(
        encoding="utf-8"))


def _selftest_root() -> Path:
    raw = os.environ.get("TMPDIR")
    if not raw:
        raise SetupError("--selftest requires TMPDIR set to the seat clone "
                         "scratch directory; /tmp scratch is forbidden")
    root = Path(raw).resolve()
    if not root.is_dir():
        raise SetupError("TMPDIR is not a directory: %s" % root)
    if root in (Path("/tmp"), Path("/var/tmp")):
        raise SetupError("TMPDIR must not be /tmp or /var/tmp")
    return root


def selftest() -> int:
    gate = Path(__file__).resolve()
    tmp_root = _selftest_root()
    checks = []
    with tempfile.TemporaryDirectory(prefix="mori-r17-seat-gate-",
                                     dir=str(tmp_root)) as td:
        root = Path(td)
        stub = root / "stub-tool.py"
        stub.write_text(_STUB_TOOL, encoding="utf-8")

        # green: every case matches, rc0, manifest counts and run artifacts.
        green = _selftest_tree(root, "green")
        out_green = root / "out-green"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(green), "--output", str(out_green)])
        _assert(proc.returncode == 0, "green rc=%s" % proc.returncode, proc)
        man = _manifest(out_green)
        _assert(man["verdict"] == "ok", "green verdict %r" % man["verdict"])
        _assert(man["summary"]["total"] == 3, "green total", proc)
        _assert(man["summary"]["matched"] == 3, "green matched", proc)
        _assert(all(c["status"] == "match" for c in man["cases"]),
                "green statuses", proc)
        _assert((out_green / "runs/st-ok.stdout").is_file(),
                "green run stdout retained", proc)
        _assert(man["fixtures"]["inputs_before"]
                == man["fixtures"]["inputs_after"],
                "green inputs stable", proc)
        _assert(man["tool"]["sha256"] == sha256_file(stub),
                "green tool digest", proc)
        _assert(man["schema"] == SCHEMA, "green manifest schema", proc)
        _assert(man["gate_sha256"] == sha256_file(gate),
                "green gate digest", proc)
        first = man["cases"][0]
        _assert(first["stdout_sha256"]
                == sha256_file(out_green / "runs/st-ok.stdout"),
                "green stdout sha", proc)
        _assert((out_green / "runs/st-ok.stderr").is_file(),
                "green stderr retained", proc)
        _assert(first["observed"]["totals"]["completed"] == 1,
                "green observed totals", proc)
        _assert(man["fixtures"]["inputs_before"].get("expected.json")
                == man["fixtures"]["expected"]["sha256"],
                "green expected pin", proc)
        _assert(man["fixtures"]["pins"]["verified"] is True,
                "green persisted pins verified", proc)
        _assert(man["fixtures"]["pins"]["declared"] > 0,
                "green pin count", proc)
        git_meta = man["git"]
        _assert({"branch", "branch_source", "branch_tip", "receipt_ref",
                 "head"} <= set(git_meta), "git metadata keys", proc)
        if git_meta["branch"] is not None:
            _assert(git_meta["receipt_ref"]
                    == "refs/heads/" + git_meta["branch"],
                    "git receipt ref", proc)
            _assert(re.fullmatch(r"[0-9a-f]{40,64}",
                                 git_meta["branch_tip"] or "") is not None,
                    "git branch tip", proc)
        else:
            _assert(git_meta["receipt_ref"] is None, "git no receipt ref",
                    proc)
        green_ok = man["cases"][0]
        _assert(green_ok["fifo_files"] == ["Pipe.jsonl"],
                "green fifo metadata", proc)
        green_pipe = Path(green_ok["sandbox"]) / "Pipe.jsonl"
        _assert(stat.S_ISFIFO(os.lstat(green_pipe).st_mode),
                "green generated FIFO", proc)
        _assert(not (green / "pack-ok/Pipe.jsonl").exists()
                and not (green / "pack-ok/Pipe.jsonl").is_symlink(),
                "green source has no FIFO", proc)
        green_pack_before = green_ok["pack_before_sha256"]
        checks.append("green_rc0_and_manifest")

        # capability_absent: missing --tool path, rc1, every case absent.
        out_absent = root / "out-absent"
        proc = _gate_proc(gate, ["--tool", str(root / "no-such-tool.py"),
                                 "--fixtures", str(green),
                                 "--output", str(out_absent)])
        _assert(proc.returncode == 1, "absent rc=%s" % proc.returncode, proc)
        man = _manifest(out_absent)
        _assert(man["verdict"] == "capability_absent",
                "absent verdict %r" % man["verdict"])
        _assert(all(c["status"] == "capability_absent"
                    for c in man["cases"]), "absent statuses", proc)
        _assert(man["summary"]["capability_absent"] == 3,
                "absent summary", proc)
        absent_ok = man["cases"][0]
        _assert(absent_ok["pack_before_sha256"] == green_pack_before,
                "pack digest definition matches across branches", proc)
        _assert(absent_ok["pack_after_sha256"] == green_pack_before,
                "absent pack digest stable", proc)
        checks.append("capability_absent_rc1")

        # mismatch: a factually wrong but coherent want must go red.
        mismatch = _selftest_tree(root, "mismatch")
        out_mismatch = root / "out-mismatch"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(mismatch), "--output",
                                 str(out_mismatch)])
        _assert(proc.returncode == 1, "mismatch rc=%s" % proc.returncode,
                proc)
        man = _manifest(out_mismatch)
        _assert(man["verdict"] == "mismatch",
                "mismatch verdict %r" % man["verdict"])
        dead = [c for c in man["cases"] if c["id"] == "st-dead"][0]
        _assert(dead["status"] == "mismatch", "mismatch case status", proc)
        _assert(any(reason.startswith("want.")
                    for reason in dead["reasons"]),
                "mismatch want reasons: %r" % dead["reasons"][:3], proc)
        checks.append("mismatch_rc1")

        # forbidden key: a leaked transcript field must go red.
        leak = _selftest_tree(root, "leak")
        out_leak = root / "out-leak"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(leak), "--output", str(out_leak)])
        _assert(proc.returncode == 1, "leak rc=%s" % proc.returncode, proc)
        man = _manifest(out_leak)
        _assert(man["verdict"] == "mismatch", "leak verdict", proc)
        reasons = man["cases"][0]["reasons"]
        _assert(any(reason.startswith("forbidden_key:")
                    or "unknown_key:errorMessage" in reason
                    for reason in reasons),
                "leak reasons: %r" % reasons[:4], proc)
        checks.append("forbidden_key_rc1")

        # seats as a seat->object map must project cleanly to want.seats.
        dict_tree = _selftest_tree(root, "dict")
        out_dict = root / "out-dict"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(dict_tree), "--output", str(out_dict)])
        _assert(proc.returncode == 0, "dict rc=%s" % proc.returncode, proc)
        man = _manifest(out_dict)
        _assert(man["verdict"] == "ok", "dict verdict", proc)
        _assert(man["cases"][0]["observed"]["seat_count"] == 1,
                "dict seat projection", proc)
        checks.append("seats_map_projection_rc0")

        # Amendment A1: main sessions are counted but excluded from totals,
        # breakdowns and want.seats grading.
        main_tree = _selftest_tree(root, "main")
        out_main = root / "out-main"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(main_tree), "--output", str(out_main)])
        _assert(proc.returncode == 0, "main rc=%s" % proc.returncode, proc)
        man = _manifest(out_main)
        _assert(man["verdict"] == "ok", "main verdict", proc)
        _assert(man["cases"][0]["observed"]["main_sessions"] == 1,
                "main_sessions count", proc)
        _assert(man["cases"][0]["observed"]["seat_count"] == 2,
                "main seat count", proc)
        _assert(man["cases"][0]["observed"]["now_ms"]
                == _SELFTEST_NOW_MS, "now_ms echoed", proc)
        checks.append("a1_main_sessions_rc0")

        # Generated FIFO only in the sandbox: zero-seat ignored-FIFO result
        # must stay green and the source path must remain absent.
        fifo_tree = _selftest_tree(root, "fifo")
        out_fifo = root / "out-fifo"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(fifo_tree), "--output", str(out_fifo)])
        _assert(proc.returncode == 0, "fifo rc=%s" % proc.returncode, proc)
        man = _manifest(out_fifo)
        _assert(man["verdict"] == "ok", "fifo verdict", proc)
        fifo_case = man["cases"][0]
        _assert(fifo_case["fifo_files"] == ["pipe.jsonl"],
                "fifo metadata recorded", proc)
        fifo_sandbox = Path(fifo_case["sandbox"]) / "pipe.jsonl"
        _assert(stat.S_ISFIFO(os.lstat(fifo_sandbox).st_mode),
                "sandbox FIFO created", proc)
        _assert(fifo_case["observed"]["files_scanned"] == 0,
                "generated FIFO not scanned", proc)
        _assert(sum(fifo_case["observed"]["totals"].values()) == 0,
                "generated FIFO yields zero totals", proc)
        source_fifo = fifo_tree / "pack-fifo/pipe.jsonl"
        _assert(not source_fifo.exists() and not source_fifo.is_symlink(),
                "source FIFO absent", proc)
        checks.append("generated_fifo_rc0")

        # F1 trap: a symlinked FIFO ancestor must be rejected before any
        # mkdir; the external target must never be created.
        trap_tree = _selftest_tree(root, "trap")
        escape_target = root / "escape-target"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(trap_tree), "--output",
                                 str(root / "out-trap")])
        _assert(proc.returncode == 2, "trap rc=%s" % proc.returncode, proc)
        _assert("ancestor is a symlink" in proc.stderr,
                "trap symlink reason: %r" % one_line(proc.stderr), proc)
        _assert(not escape_target.exists()
                and not escape_target.is_symlink(),
                "trap created no out-of-sandbox dir", proc)
        checks.append("symlink_ancestor_fifo_trap_rc2")

        # unreadable_dirs: chmod 000 only in the sandbox copy; the tool sees
        # the walk error; modes are restored so cleanup works.
        dirs_tree = _selftest_tree(root, "dirs")
        out_dirs = root / "out-dirs"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(dirs_tree), "--output", str(out_dirs)])
        _assert(proc.returncode == 0, "dirs rc=%s" % proc.returncode, proc)
        man = _manifest(out_dirs)
        dir_case = man["cases"][0]
        _assert(dir_case["status"] == "match", "dirs reason match", proc)
        _assert(dir_case["unreadable_dirs"] == ["locked-dir"],
                "dirs metadata recorded", proc)
        sandbox_dir = Path(dir_case["sandbox"]) / "locked-dir"
        _assert((os.stat(sandbox_dir).st_mode & 0o700) == 0o700,
                "sandbox dir mode restored", proc)
        source_dir = dirs_tree / "pack-dirs/locked-dir"
        _assert(os.access(source_dir, os.R_OK | os.X_OK),
                "source dir stays readable", proc)
        checks.append("unreadable_dirs_sandbox_rc0")

        # tracked root symlink is rebased into the sandbox and rejected.
        rootlink_tree = _selftest_tree(root, "rootlink")
        out_rootlink = root / "out-rootlink"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(rootlink_tree), "--output",
                                 str(out_rootlink)])
        _assert(proc.returncode == 0, "rootlink rc=%s" % proc.returncode,
                proc)
        man = _manifest(out_rootlink)
        link_case = man["cases"][0]
        _assert(link_case["status"] == "match", "rootlink reason match",
                proc)
        _assert(link_case["sessions_arg"].endswith("/sessions/root-link"),
                "rootlink sessions arg: %r" % link_case["sessions_arg"],
                proc)
        checks.append("root_symlink_rebase_rc0")

        # Missing key/prefix metadata must go red (no stem fallback).
        nokey_tree = _selftest_tree(root, "nokey")
        out_nokey = root / "out-nokey"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(nokey_tree), "--output",
                                 str(out_nokey)])
        _assert(proc.returncode == 1, "nokey rc=%s" % proc.returncode, proc)
        man = _manifest(out_nokey)
        reasons = man["cases"][0]["reasons"]
        _assert(any("key" in reason for reason in reasons),
                "nokey reasons: %r" % reasons[:4], proc)
        checks.append("key_metadata_required_rc1")

        # JSON-type-exact metadata: the fake tool emits bool where the wish
        # is integer (True vs 1); strict_eq must reject it, not loose ==.
        wrong_tree = _selftest_tree(root, "wrongtype")
        out_wrong = root / "out-wrongtype"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(wrong_tree), "--output",
                                 str(out_wrong)])
        _assert(proc.returncode == 1, "wrongtype rc=%s" % proc.returncode,
                proc)
        man = _manifest(out_wrong)
        _assert(man["verdict"] == "mismatch", "wrongtype verdict", proc)
        reasons = man["cases"][0]["reasons"]
        _assert(any("want.record" in reason or "want.top" in reason
                    or "error_status" in reason for reason in reasons),
                "wrongtype reasons: %r" % reasons[:4], proc)
        checks.append("wrong_type_metadata_rc1")

        # Persisted pins are independent evidence: a tree moved after pinning
        # is rc2 snapshot_tampered before any tool run.
        pin_tree = _selftest_tree(root, "pintamper")
        out_pin = root / "out-pintamper"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(pin_tree), "--output", str(out_pin)])
        _assert(proc.returncode == 2, "pintamper rc=%s" % proc.returncode,
                proc)
        man = _manifest(out_pin)
        _assert(man["verdict"] == "snapshot_tampered",
                "pintamper verdict %r" % man["verdict"], proc)
        _assert(man["fixtures"]["pins"]["verified"] is False,
                "pintamper pins unverified", proc)
        _assert(any(rel.endswith("pack-ok/Alpha.one.jsonl")
                    for rel in man["fixtures"]["pins"]["mismatched"]),
                "pintamper mismatched path", proc)
        _assert(not any((out_pin / "runs").iterdir()),
                "pintamper ran no case", proc)
        checks.append("pinned_snapshot_tamper_rc2")

        # --prefix: walked-file count may exceed retained seats.
        prefix_tree = _selftest_tree(root, "prefix")
        out_prefix = root / "out-prefix"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(prefix_tree), "--output",
                                 str(out_prefix)])
        _assert(proc.returncode == 0, "prefix rc=%s" % proc.returncode,
                proc)
        checks.append("prefix_filter_rc0")

        # Two walked files but one emitted seat without --prefix must fail.
        scan_tree = _selftest_tree(root, "scan")
        out_scan = root / "out-scan"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(scan_tree), "--output", str(out_scan)])
        _assert(proc.returncode == 1, "scan rc=%s" % proc.returncode, proc)
        man = _manifest(out_scan)
        _assert(any("files_scanned" in reason
                    for reason in man["cases"][0]["reasons"]),
                "scan files_scanned reasons", proc)
        checks.append("files_scanned_falsifier_rc1")

        # A chmod-000 fixture file must not break input hashing (metadata
        # fingerprint) or the run.
        unreadable_tree = _selftest_tree(root, "unreadable")
        out_unreadable = root / "out-unreadable"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(unreadable_tree), "--output",
                                 str(out_unreadable)])
        _assert(proc.returncode == 0, "unreadable rc=%s" % proc.returncode,
                proc)
        man = _manifest(out_unreadable)
        _assert(man["verdict"] == "ok", "unreadable verdict", proc)
        source_locked = unreadable_tree / "pack-unreadable/Zeta.six.jsonl"
        _assert((os.stat(source_locked).st_mode & 0o444) != 0,
                "unreadable source stays readable", proc)
        _assert(source_locked.stat().st_size == 0,
                "unreadable source content unchanged", proc)
        case_row = man["cases"][0]
        _assert(case_row["unreadable_files"] == ["Zeta.six.jsonl"],
                "unreadable metadata recorded", proc)
        sandbox_locked = Path(case_row["sandbox"]) / "Zeta.six.jsonl"
        _assert((os.stat(sandbox_locked).st_mode & 0o777) == 0,
                "sandbox copy is chmod 000", proc)
        _assert(case_row["observed"]["totals"]["unavailable"] == 1,
                "sandbox unreadable classified", proc)
        checks.append("unreadable_fixture_rc0")

        # fixture drift: the fake tool mutates its pack mid-run; rc2.
        drift = _selftest_tree(root, "drift")
        out_drift = root / "out-drift"
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(drift), "--output", str(out_drift)])
        _assert(proc.returncode == 2, "drift rc=%s" % proc.returncode, proc)
        man = _manifest(out_drift)
        _assert(man["verdict"] == "tamper:inputs-changed",
                "drift verdict %r" % man["verdict"])
        _assert(man["fixtures"]["inputs_changed"],
                "drift changed list", proc)
        _assert(man["cases"][0]["pack_changed"]
                is True, "drift per-case pack flag", proc)
        checks.append("fixture_drift_rc2")

        # output guard: protected trees and declared inputs are refused
        # before any directory is created.
        guard_targets = [
            (REPO / "tools/.st-seat-gate-guard", False),
            (REPO / ".git/.st-seat-gate-guard", False),
            (REPO / ".jj/.st-seat-gate-guard", False),
            (REPO / "corpus/.st-seat-gate-guard", False),
            (green, True),
            (green / "pack-ok", True),
        ]
        for target, existing in guard_targets:
            proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                     str(green), "--output", str(target)])
            _assert(proc.returncode == 2,
                    "guard %s rc=%s" % (target, proc.returncode), proc)
            if not existing:
                _assert(not target.exists(),
                        "guard created %s" % target, proc)
        checks.append("output_guard_rc2")

        # non-empty output refused.
        nonempty = root / "out-nonempty"
        nonempty.mkdir()
        (nonempty / "junk").write_text("x", encoding="utf-8")
        proc = _gate_proc(gate, ["--tool", str(stub), "--fixtures",
                                 str(green), "--output", str(nonempty)])
        _assert(proc.returncode == 2, "nonempty rc=%s" % proc.returncode,
                proc)
        checks.append("nonempty_output_rc2")

    print("SELFTEST ok: %s" % ",".join(checks))
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="round-17 mori-seat-terminal fixture gate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "expected.json: {\"pins\":{<relpath>:<sha256hex>},"
            "\"cases\":[{\"id\",\"pack\",\"args\",\"unreadable_files\","
            "\"fifo_files\",\"unreadable_dirs\","
            "\"want\":{\"rc\",\"finding_id\",\"totals\",\"seats\","
            "\"reason\",\"records\",\"top\"}}]}\n"
            "pins: every non-directory fixture entry except expected.json; "
            "regular=file sha256, symlink=sha256(target text), "
            "FIFO=sha256(b\"fifo\"); verified before any run.\n"
            "args: {pack}/{fixtures} expand to absolute paths; "
            "--sessions-dir is prepended when absent; an explicit "
            "{pack}/subpath sessions dir is rebased into the sandbox; other "
            "args (--now-ms included) pass unchanged.\n"
            "sandbox: each existing pack is copied per case under "
            "output/cases/<id>/sessions; unreadable_files/unreadable_dirs are "
            "mode 000 only in the copy (dirs restored after the run), "
            "fifo_files are os.mkfifo-created only there with componentwise "
            "symlink-ancestor rejection, and must be absent from the "
            "source tree.\n"
            "grading: rc0/rc1 wants must carry a totals subset and a seats "
            "map; seats are keyed by A1 relative key (key+prefix required), "
            "totals are re-derived from the graded seats (main-kind "
            "excluded), and optional want.reason/top/records are compared "
            "exactly and type-strict.\n"
            "output: absent or empty directory; may sit under repo .ufo; "
            "refused under the fixture tree, tool file, tools/, .git/, "
            ".jj/ or corpus/, and never equal/contain the repo root.\n"
            "selftest: requires TMPDIR (not /tmp or /var/tmp)."))
    parser.add_argument("--tool", default=str(DEFAULT_TOOL),
                        help="tool under test (absent path records "
                             "capability_absent, never green)")
    parser.add_argument("--fixtures", default=str(DEFAULT_FIXTURES),
                        help="fixture tree holding expected.json and pack "
                             "directories")
    parser.add_argument("--output", help="run output directory (must be "
                                         "empty or absent)")
    parser.add_argument("--run-timeout", type=int, default=RUN_TIMEOUT_S,
                        help="per-run harness deadline seconds")
    parser.add_argument("--capture-cap", type=int, default=CAPTURE_CAP,
                        help="per-stream byte cap on tool output")
    parser.add_argument("--selftest", action="store_true",
                        help="run isolated fake-tool/fixture self-checks "
                             "under TMPDIR; never touches lane inputs")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.selftest:
        try:
            return selftest()
        except SetupError as exc:
            print("SELFTEST SETUP: %s" % one_line(exc), file=sys.stderr)
            return 2
        except (AssertionError, OSError) as exc:
            print("SELFTEST FAIL: %s" % one_line(exc), file=sys.stderr)
            return 1
    try:
        gate_sha = sha256_file(Path(__file__).resolve())
        return run_gate(args, gate_sha)
    except SetupError as exc:
        print("SETUP: %s" % one_line(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
