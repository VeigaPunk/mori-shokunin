#!/usr/bin/env python3
"""Read-only check of the round-24 routed defect items D1..D5 against committed bytes.

One command re-derives the round-24 routed items named in
``corpus/lessons/round-24-verifier-spotcheck.md`` (the "Routed defects" list,
D1..D4) at a committed revision, per claim contract C1 as amended by A1.

Every predicate reads git objects only (``cat-file``, ``ls-tree``, ``archive``,
``merge-base``) with a clean environment; the working tree is never consulted
and nothing is written.  No code from REV is ever executed; the optional
``--rerun`` flag re-executes the *named* revision R's own tool from a temporary
extract and only reports whether the recorded body is byte-equal to it.

Counted items (C1/A1):

  D1  stale gate evidence.  ``.ufo/waves/round-25/evidence/pressure-selftest.txt``
      exists at REV with header lines, in order: ``revision: <40 hex>`` naming a
      commit R that is REV or an ancestor of REV; ``command: python3 -I -B
      tools/mori-pressure.py --selftest``; ``tool_blob: <oid>`` equal to the
      blob of ``tools/mori-pressure.py`` at R and at REV; ``fixtures_tree:
      <oid>`` equal to the tree ``tools/fixtures/mori-pressure`` at R and at
      REV; ``exit: 0``.  The body after the header contains the line
      ``MORI_PRESSURE_SELFTEST: PASS 12/12`` and a line starting
      ``MATCHER: rejected 48/48``.
  D2  incomplete correction sweep in ``corpus/knowledge/system-pressure-r24.md``.
      Over the entry text with ``*``, ``_`` and backticks removed, case folded
      and all whitespace runs folded to one space: exactly one heading starting
      ``## corrections``; headings ``## facts`` and ``## decision table`` both
      present; the decision table has at least as many data rows as at
      ``28b79d3d``; outside the corrections section, no match of
      ``refreshed on (each|every) read``, of
      ``spike[^|.]{0,60}(is|are|can be|may be) invisible`` and of
      ``null[^|.]{0,15}means[^|.]{0,15}undefined``; outside it, both ``only when
      the next`` and ``not tracked`` occur; inside it, a line contains ``(k4)``
      and ``total``.
  D3  lesson count drift in ``corpus/lessons/round-24.md``.  With n = the number
      of cases in ``tools/fixtures/mori-pressure/supplementary-cases.json`` at
      ``4f05dd5a`` (7): the lesson at REV has one line containing ``Correction``,
      ``S07``, ``PASS n/n`` not followed by a digit, and a 7-40 hex token naming
      a commit at which that file has n cases.

Counted item added by A5:

  D5  the `## Axes` table of `SCORECARD.md` against the closure-admitted
      scores.  Held at REV when the table has exactly one row per axis
      (coverage, operability, depth, freshness, calibration, adjacency); each
      row's Score equals the score parsed from `SCORECARD.md` lines 1499-1506
      at `28b79d3d` (the pinned observed state, parsed with a regex over that
      line range; the parse fails closed when it does not yield all six
      axes); and no row whose score differs from its round-1 value says
      `round 1` in Last change.

Hygiene row (reported, not counted):

  D4  ``.gitignore`` at REV has a line that is exactly one of
      ``__pycache__/``, ``__pycache__``, ``**/__pycache__/``,
      ``tools/__pycache__/``, ``*.pyc``, ``*.py[cod]``; no ``.gitignore`` in the
      REV tree has a ``!`` line mentioning ``pycache`` or ``.py``; and no
      tracked path under ``tools/`` contains ``__pycache__`` or ends ``.pyc``.

Output: one JSON object, ``schema: mori-routed-r24-v1``, ``items: 4``, ``held``,
``mismatches``, one row per counted item ``{id, held, reasons[], detail}`` and
``hygiene: {id: D4, held, reasons[]}``.  Exit 0 only when ``mismatches`` is 0
and the hygiene row holds, 1 otherwise, and 2 when the repository or the
revision cannot be read.

Self-check: ``--selftest`` runs a bounded self-check of this tool's own parsing
and verdict arms against a throwaway git repository built under ``$TMPDIR`` --
its own fixtures, no host repository, no network.  It prints
``ROUTED_R24_SELFTEST pass=<n> fail=<n>`` and exits 0 when every arm passes, 1
when an arm fails and 2 when the fixture cannot be set up.  The all-held exit-0
verdict is out of its reach by construction: D2, D3 and D5 are pinned to fixed
base commits, so the self-check asserts the verdict mapping directly and the
synthetic repository exercises the held, failed and could-not-evaluate reads.

Python 3 standard library only; read-only; safe under ``python3 -I -B``.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile

SCHEMA = "mori-routed-r24-v1"

RC_HELD = 0
RC_FAILED = 1
RC_UNAVAILABLE = 2

GIT_TIMEOUT_SECONDS = 120
RUN_TIMEOUT_SECONDS = 120

# D1: the round-25 evidence file that must carry the measured revision.
EVIDENCE_PATH = ".ufo/waves/round-25/evidence/pressure-selftest.txt"
PRESSURE_TOOL_PATH = "tools/mori-pressure.py"
PRESSURE_FIXTURES_PATH = "tools/fixtures/mori-pressure"
EVIDENCE_COMMAND = "python3 -I -B tools/mori-pressure.py --selftest"
# A3: the body after the five header lines must be byte-equal to this.
EXPECTED_BODY = (
    b"MORI_PRESSURE_SELFTEST: PASS 12/12\n"
    b"MATCHER: rejected 48/48 corrupted expectations\n"
)

# D2: the knowledge entry and its hardening constants.
KNOWLEDGE_PATH = "corpus/knowledge/system-pressure-r24.md"
KNOWLEDGE_BASE_REV = "28b79d3d1b76824f0c825aabe6cb6c5dc49961bf"
D2_CORRECTIONS_HEADING = "## corrections"
D2_FACTS_HEADING = "## facts"
D2_TABLE_HEADING = "## decision table"
D2_NEGATIVE_PATTERNS = (
    r"refreshed on (each|every) read",
    r"spike[^|.]{0,60}(is|are|can be|may be) invisible",
    r"null[^|.]{0,15}means[^|.]{0,15}undefined",
)
D2_POSITIVE_PHRASES = ("only when the next", "not tracked")
# A3: the "this section wins" precedence banner must be gone from the body.
D2_BANNER_PHRASE = "this section wins"
D2_CORRECTIONS_TOKEN = "(k4)"
D2_CORRECTIONS_WORD = "total"

# D3: the lesson, and the pinned revision the case count is measured at.
LESSON_PATH = "corpus/lessons/round-24.md"
SUPPLEMENTARY_CASES_PATH = "tools/fixtures/mori-pressure/supplementary-cases.json"
SUPPLEMENTARY_CASES_BASE_REV = "4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e"
D3_TOKEN_CORRECTION = "Correction"
D3_TOKEN_CASE = "S07"

# D4: the accepted ignore rules and the hygiene exclusions.
GITIGNORE_PATH = ".gitignore"
D4_IGNORE_LINES = (
    "__pycache__/",
    "__pycache__",
    "**/__pycache__/",
    "tools/__pycache__/",
    "*.pyc",
    "*.py[cod]",
)
D4_NEGATION_MARKERS = ("pycache", ".py")
TOOLS_PREFIX = "tools/"

# D5: the SCORECARD `## Axes` table against the closure-admitted scores.
# The pinned observed state is parsed from the SCORECARD.md lines 1499-1506
# at 28b79d3d (the round-24 tip); the round-1 values are the scores the same
# table carried before any round moved them.
SCORECARD_PATH = "SCORECARD.md"
SCORECARD_BASE_REV = "28b79d3d1b76824f0c825aabe6cb6c5dc49961bf"
SCORECARD_BASE_LINE_START = 1499
SCORECARD_BASE_LINE_END = 1506
D5_AXES_HEADING = "## Axes"
D5_AXES = ("coverage", "operability", "depth", "freshness", "calibration", "adjacency")
# The round-1 value of each axis, from the same `## Axes` table at 28b79d3d.
D5_ROUND1_SCORES = {
    "coverage": 5,
    "operability": 6,
    "depth": 4,
    "freshness": 5,
    "calibration": 5,
    "adjacency": 6,
}
# The pinned observed score of each axis, parsed from the base lines.
D5_PINNED_SCORE_RE = re.compile(
    r"\b(%s)\s+(\d+)\b" % "|".join(D5_AXES),
    re.IGNORECASE,
)
# "round 1" as a whole token: "round 12" and "round 13" must not match.
D5_ROUND1_RE = re.compile(r"\bround\s+1\b", re.IGNORECASE)

# Selftest: a throwaway repository built under $TMPDIR, with a pinned identity
# so the fixture commits are content-stable.  The entry, lesson and scorecard
# bodies are shaped so that every parse arm of D2, D3 and D5 accepts them; the
# three checks still fail closed on the pinned base revisions, which a
# synthetic repository cannot carry.
SELFTEST_TALLY_PREFIX = "ROUTED_R24_SELFTEST"
SELFTEST_GIT_IDENTITY = {
    "GIT_AUTHOR_NAME": "mori routed selftest",
    "GIT_AUTHOR_EMAIL": "selftest@example.invalid",
    "GIT_COMMITTER_NAME": "mori routed selftest",
    "GIT_COMMITTER_EMAIL": "selftest@example.invalid",
    "GIT_AUTHOR_DATE": "2001-02-03T04:05:06 +0000",
    "GIT_COMMITTER_DATE": "2001-02-03T04:05:06 +0000",
}
SELFTEST_PRESSURE_TOOL = b"# synthetic pressure tool; never executed\nprint('stub')\n"
SELFTEST_PRESSURE_CASES = b'{"cases": [1, 2, 3]}\n'
SELFTEST_GITIGNORE = b"__pycache__/\n*.pyc\n"
SELFTEST_GITIGNORE_NEGATION = b"__pycache__/\n*.pyc\n!tools/*.pyc\n"
SELFTEST_KNOWLEDGE_ENTRY = (
    "# system pressure re-derived\n"
    "\n"
    "## facts\n"
    "\n"
    "- Only when the next batch lands is the row written.\n"
    "- Untracked scratch state is not tracked by the gate.\n"
    "\n"
    "## decision table\n"
    "\n"
    "| case | expected |\n"
    "|---|---|\n"
    "| a | one |\n"
    "| b | two |\n"
    "\n"
    "## corrections\n"
    "\n"
    "- (k4) the total is seven supplementary cases.\n"
)
SELFTEST_LESSON = (
    "# round 24\n"
    "\n"
    "## Correction\n"
    "\n"
    "S07 PASS 7/7 at `abcdef1` with the corrected sweep.\n"
)
SELFTEST_SCORECARD = (
    "# scorecard\n"
    "\n"
    "## Axes\n"
    "\n"
    "| axis | score | last change |\n"
    "|---|---|---|\n"
    "| coverage | 7 | round 41 |\n"
    "| depth | 4 | round 24 |\n"
    "\n"
    "## Notes\n"
    "\n"
    "Synthetic fixture; unreachable while the base SCORECARD is unreadable.\n"
)

REVISION_LINE_RE = re.compile(r"^[0-9a-f]{40}$")
TOOL_BLOB_LINE_RE = re.compile(r"^[0-9a-f]{40}$")
FIXTURES_TREE_LINE_RE = re.compile(r"^[0-9a-f]{40}$")
EXIT_LINE_RE = re.compile(r"^\d+$")
HEADER_KEY_ORDER = ("revision", "command", "tool_blob", "fixtures_tree", "exit")
HEADING_RE = re.compile(r"^#{1,6}\s")
HEX_TOKEN_RE = re.compile(r"(?<![0-9A-Za-z])([0-9a-fA-F]{7,40})(?![0-9A-Za-z])")
MARKER_CHARS = ("*", "_", "`")


class GitUnavailable(Exception):
    """The repository, revision or a committed object could not be read."""


class GitError(Exception):
    """A git command failed for a reason other than a missing object."""


class SelftestSetupError(Exception):
    """A self-check fixture could not be built (temp dir, git, fixture commit)."""


def _git_env() -> dict[str, str]:
    return {
        "PATH": os.defpath,
        "LANG": "C",
        "LC_ALL": "C",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    }


def _run_env() -> dict[str, str]:
    return {
        "PATH": os.defpath,
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    }


def _git(repo: str, args: list[str], *, allow_failure: bool = False) -> tuple[int, bytes]:
    """Run one read-only git command; return (returncode, stdout bytes)."""
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", "-C", repo, *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=_git_env(),
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitUnavailable("git read failed") from exc
    if proc.returncode != 0 and not allow_failure:
        raise GitError("git read failed: " + " ".join(args))
    return proc.returncode, proc.stdout


def _batch_check(repo: str, revs: list[str]) -> dict[str, str | None]:
    """Resolve each rev to a commit id (or None) with one cat-file call."""
    if not revs:
        return {}
    payload = "".join("%s^{commit}\n" % rev for rev in revs).encode("utf-8")
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", "-C", repo, "cat-file", "--batch-check"],
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=_git_env(),
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitUnavailable("git read failed: cat-file --batch-check") from exc
    if proc.returncode != 0:
        raise GitUnavailable("git read failed: cat-file --batch-check")
    out = proc.stdout.decode("utf-8", "replace").splitlines()
    resolved: dict[str, str | None] = {}
    for rev, line in zip(revs, out):
        parts = line.split()
        resolved[rev] = parts[0] if len(parts) >= 2 and parts[1] == "commit" else None
    return resolved


def _resolve_commit(repo: str, rev: str) -> str | None:
    """Resolve `rev` to a commit id, or None when it does not resolve."""
    return _batch_check(repo, [rev]).get(rev)


def _ls_tree_entry(repo: str, rev: str, path: str) -> tuple[str, str, str] | None:
    """Return (mode, type, oid) for `path` at `rev`, or None when absent."""
    code, out = _git(repo, ["ls-tree", rev, "--", path], allow_failure=True)
    if code != 0:
        return None
    for raw in out.decode("utf-8", "replace").splitlines():
        if not raw.strip():
            continue
        head, _, _name = raw.partition("\t")
        fields = head.split()
        if len(fields) < 3:
            continue
        return fields[0], fields[1], fields[2]
    return None


def _list_paths(repo: str, rev: str, prefix: str = "") -> list[str]:
    """List every tracked path at `rev` (optionally under `prefix`)."""
    args = ["ls-tree", "-r", "-z", rev]
    if prefix:
        args += ["--", prefix]
    code, out = _git(repo, args, allow_failure=True)
    if code != 0:
        raise GitUnavailable("git ls-tree failed at %s" % rev)
    paths = []
    for record in out.split(b"\0"):
        if not record:
            continue
        _, _, raw = record.partition(b"\t")
        paths.append(raw.decode("utf-8", "replace"))
    return paths


def _blob_bytes(repo: str, rev: str, path: str) -> bytes | None:
    """Return the committed blob of `path` at `rev`, or None when absent."""
    code, out = _git(repo, ["cat-file", "blob", "%s:%s" % (rev, path)], allow_failure=True)
    if code != 0:
        return None
    return out


def _is_ancestor(repo: str, ancestor: str, descendant: str) -> bool:
    code, _ = _git(
        repo,
        ["merge-base", "--is-ancestor", ancestor, descendant],
        allow_failure=True,
    )
    return code == 0


def _normalize(text: str) -> str:
    """Remove the emphasis markers, case fold and fold whitespace runs."""
    for marker in MARKER_CHARS:
        text = text.replace(marker, "")
    text = text.casefold()
    return re.sub(r"\s+", " ", text).strip()


def _split_header(data: bytes) -> tuple[dict[str, str], bytes, list[str]]:
    """Split the evidence file into its header values and its body bytes.

    The header is the leading run of ``key: value`` lines whose keys are the
    expected ones, in the expected order.  The body is every byte after the
    header.  The third return value lists the expected keys that were absent.
    """
    header: dict[str, str] = {}
    missing: list[str] = []
    offset = 0
    for key in HEADER_KEY_ORDER:
        newline = data.find(b"\n", offset)
        if newline < 0:
            missing.append(key)
            break
        line = data[offset:newline].decode("utf-8", "replace")
        match = re.match(r"^%s: ?(.*)$" % re.escape(key), line)
        if not match:
            missing.append(key)
            break
        header[key] = match.group(1)
        offset = newline + 1
    return header, data[offset:], missing



def _blocks(lines: list[str]) -> list[tuple[str | None, list[str]]]:
    """Split markdown lines into (heading, body) blocks.

    A heading line starts a new block; the text before the first heading is a
    block with heading None.
    """
    blocks: list[tuple[str | None, list[str]]] = []
    heading: str | None = None
    body: list[str] = []
    started = False
    for line in lines:
        if HEADING_RE.match(line):
            if started:
                blocks.append((heading, body))
            heading = line.strip()
            body = []
            started = True
            continue
        body.append(line)
    blocks.append((heading, body) if started else (None, body))
    return blocks


def _heading_level(heading: str) -> int:
    match = re.match(r"^(#{1,6})\s", heading)
    return len(match.group(1)) if match else 0


def _section_span(
    blocks: list[tuple[str | None, list[str]]], index: int
) -> list[int]:
    """Return the indices of the blocks that belong to the section at `index`.

    A section owns the blocks that follow it until the next heading of the
    same or a higher level.
    """
    level = _heading_level(blocks[index][0] or "")
    span = [index]
    for position in range(index + 1, len(blocks)):
        heading = blocks[position][0]
        if heading is None:
            span.append(position)
            continue
        if _heading_level(heading) <= level:
            break
        span.append(position)
    return span



def _data_row_count(block_lines: list[str]) -> int:
    """Count the data rows of the markdown table inside a block."""
    pipe_lines = [line.strip() for line in block_lines if line.strip().startswith("|")]
    separators = [line for line in pipe_lines if re.fullmatch(r"\|[\s\-:|]+\|", line)]
    return max(0, len(pipe_lines) - len(separators) - 1)


def _run_pressure_selftest(repo: str, rev: str) -> tuple[bytes, int]:
    """Run R's tools/mori-pressure.py --selftest from a temporary extract of R.

    Returns (stdout bytes, exit code).  The extract lives in a temporary
    directory that is removed when the call returns.
    """
    code, archive = _git(
        repo,
        ["archive", "--format=tar", rev, "--", PRESSURE_TOOL_PATH, PRESSURE_FIXTURES_PATH],
        allow_failure=True,
    )
    if code != 0:
        raise GitUnavailable("git archive failed at %s" % rev)
    with tempfile.TemporaryDirectory(prefix="mori-routed-r24-") as tmp:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
            try:
                tar.extractall(tmp, filter="data")
            except TypeError:  # pragma: no cover - Python < 3.12
                tar.extractall(tmp)
        script = os.path.join(tmp, PRESSURE_TOOL_PATH)
        if not os.path.isfile(script):
            raise GitUnavailable("tools/mori-pressure.py missing from the extract of %s" % rev)
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-B", script, "--selftest"],
                cwd=tmp,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=_run_env(),
                timeout=RUN_TIMEOUT_SECONDS,
                check=False,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise GitUnavailable("pressure selftest could not be run") from exc
        return proc.stdout, proc.returncode


def _check_d1(repo: str, rev: str, rerun: bool) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {}
    data = _blob_bytes(repo, rev, EVIDENCE_PATH)
    if data is None:
        reasons.append("evidence_file_missing")
        detail["evidence_path"] = EVIDENCE_PATH
        return False, reasons, detail
    detail["evidence_path"] = EVIDENCE_PATH
    detail["evidence_sha256"] = hashlib.sha256(data).hexdigest()
    header, body_bytes, missing = _split_header(data)
    if missing:
        reasons.append("header_missing: " + ",".join(missing))
    body_lines = body_bytes.decode("utf-8", "replace").split("\n")

    revision: str | None = None
    revision_value = header.get("revision", "").strip()
    if not REVISION_LINE_RE.match(revision_value):
        reasons.append("revision_line_malformed")
    else:
        revision = revision_value
        detail["revision"] = revision
        resolved = _resolve_commit(repo, revision)
        if resolved != revision:
            reasons.append("revision_not_a_commit")
            revision = None
        elif not _is_ancestor(repo, revision, rev):
            reasons.append("revision_not_rev_or_ancestor")

    command = header.get("command", "").strip()
    if command != EVIDENCE_COMMAND:
        reasons.append("command_line_malformed")
    detail["command"] = command

    tool_blob_value = header.get("tool_blob", "").strip()
    if not TOOL_BLOB_LINE_RE.match(tool_blob_value):
        reasons.append("tool_blob_line_malformed")
    else:
        recorded = tool_blob_value
        detail["tool_blob"] = recorded
        at_revision = _ls_tree_entry(repo, revision, PRESSURE_TOOL_PATH) if revision else None
        at_rev = _ls_tree_entry(repo, rev, PRESSURE_TOOL_PATH)
        if at_revision is None or at_rev is None:
            reasons.append("pressure_tool_missing")
        elif recorded != at_revision[2]:
            reasons.append("tool_blob_mismatch_at_revision")
        elif recorded != at_rev[2]:
            reasons.append("tool_blob_mismatch_at_rev")

    fixtures_value = header.get("fixtures_tree", "").strip()
    if not FIXTURES_TREE_LINE_RE.match(fixtures_value):
        reasons.append("fixtures_tree_line_malformed")
    else:
        recorded = fixtures_value
        detail["fixtures_tree"] = recorded
        at_revision = _ls_tree_entry(repo, revision, PRESSURE_FIXTURES_PATH) if revision else None
        at_rev = _ls_tree_entry(repo, rev, PRESSURE_FIXTURES_PATH)
        if at_revision is None or at_rev is None:
            reasons.append("pressure_fixtures_missing")
        elif recorded != at_revision[2]:
            reasons.append("fixtures_tree_mismatch_at_revision")
        elif recorded != at_rev[2]:
            reasons.append("fixtures_tree_mismatch_at_rev")

    exit_value = header.get("exit", "").strip()
    if not EXIT_LINE_RE.match(exit_value):
        reasons.append("exit_line_malformed")
    elif exit_value != "0":
        reasons.append("exit_line_not_zero")

    # A3: the body is byte-equal, not merely contained in.
    detail["body_sha256"] = hashlib.sha256(body_bytes).hexdigest()
    if body_bytes != EXPECTED_BODY:
        reasons.append("body_not_byte_equal")

    # The rerun is reported only: it never decides whether D1 holds.
    if rerun and revision is not None:
        try:
            stdout, exit_code = _run_pressure_selftest(repo, revision)
        except GitUnavailable as exc:
            detail["rerun"] = {"ran": False, "error": str(exc)}
        else:
            detail["rerun"] = {
                "ran": True,
                "exit": exit_code,
                "body_byte_equal": stdout == body_bytes,
                "body_sha256": hashlib.sha256(body_bytes).hexdigest(),
                "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            }
    return not reasons, reasons, detail


def _check_d2(repo: str, rev: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {}
    raw = _blob_bytes(repo, rev, KNOWLEDGE_PATH)
    if raw is None:
        reasons.append("knowledge_entry_missing")
        detail["knowledge_path"] = KNOWLEDGE_PATH
        return False, reasons, detail
    detail["knowledge_path"] = KNOWLEDGE_PATH
    text = raw.decode("utf-8", "replace")
    blocks = _blocks(text.split("\n"))

    corrections_indices = [
        index
        for index, (heading, _body) in enumerate(blocks)
        if heading is not None and _normalize(heading).startswith(D2_CORRECTIONS_HEADING)
    ]
    facts_present = any(
        heading is not None and _normalize(heading) == D2_FACTS_HEADING
        for heading, _body in blocks
    )
    table_indices = [
        index
        for index, (heading, _body) in enumerate(blocks)
        if heading is not None and _normalize(heading) == D2_TABLE_HEADING
    ]
    detail["corrections_sections"] = len(corrections_indices)
    detail["facts_heading_present"] = facts_present
    detail["decision_table_heading_present"] = bool(table_indices)

    if len(corrections_indices) != 1:
        reasons.append("corrections_heading_count_not_one")
    if not facts_present:
        reasons.append("facts_heading_missing")
    if not table_indices:
        reasons.append("decision_table_heading_missing")

    table_rows = 0
    if table_indices:
        table_rows = _data_row_count(blocks[table_indices[0]][1])
    detail["decision_table_data_rows"] = table_rows

    base_raw = _blob_bytes(repo, KNOWLEDGE_BASE_REV, KNOWLEDGE_PATH)
    base_rows = None
    if base_raw is None:
        reasons.append("base_knowledge_entry_unreadable")
    else:
        base_blocks = _blocks(base_raw.decode("utf-8", "replace").split("\n"))
        for heading, body in base_blocks:
            if heading is not None and _normalize(heading) == D2_TABLE_HEADING:
                base_rows = _data_row_count(body)
                break
    detail["decision_table_data_rows_at_base"] = base_rows
    if base_rows is not None and table_rows < base_rows:
        reasons.append("decision_table_rows_fewer_than_base")

    inside: set[int] = set()
    if corrections_indices:
        inside = set(_section_span(blocks, corrections_indices[0]))
    outside_lines: list[str] = []
    inside_lines: list[str] = []
    for index, (_heading, body) in enumerate(blocks):
        if index in inside:
            inside_lines.extend(body)
        else:
            outside_lines.extend(body)

    outside_text = " ".join(_normalize(line) for line in outside_lines)
    whole_text = " ".join(_normalize(line) for line in text.split("\n"))
    for pattern in D2_NEGATIVE_PATTERNS:
        if re.search(pattern, outside_text):
            reasons.append("phrase_present_outside_corrections: " + pattern)
    for phrase in D2_POSITIVE_PHRASES:
        if phrase not in outside_text:
            reasons.append("phrase_missing_outside_corrections: " + phrase)
    # A3: the "this section wins" precedence banner must be gone from the
    # entry.  The gate is the whole normalized file, not only the part outside
    # the corrections section: the banner sits inside that section, so the
    # outside-only form cannot distinguish a fixed entry from an unfixed one.
    detail["banner_outside_corrections"] = D2_BANNER_PHRASE in outside_text
    detail["banner_in_whole_entry"] = D2_BANNER_PHRASE in whole_text
    if D2_BANNER_PHRASE in whole_text:
        reasons.append("banner_present_in_entry: " + D2_BANNER_PHRASE)

    normalized_inside = [_normalize(line) for line in inside_lines]
    if not any(
        D2_CORRECTIONS_TOKEN in line and D2_CORRECTIONS_WORD in line
        for line in normalized_inside
    ):
        reasons.append("corrections_section_lacks_k4_total_line")

    return not reasons, reasons, detail


def _axes_section_lines(text: str) -> list[str] | None:
    """Return the lines of the `## Axes` section of a SCORECARD.md body."""
    lines = text.split("\n")
    start = None
    for index, line in enumerate(lines):
        if line.strip() == D5_AXES_HEADING:
            start = index + 1
            break
    if start is None:
        return None
    section: list[str] = []
    for line in lines[start:]:
        if line.startswith("#"):
            break
        section.append(line)
    return section


def _axes_rows(text: str) -> list[tuple[str, str, str]] | None:
    """Return the (axis, score, last change) triples of the `## Axes` table.

    A cell may itself contain a pipe, so the axis is the second field, the
    score the third, and the last change the second-to-last: the row always
    starts and ends with a pipe.  The header and the separator row are
    skipped.
    """
    section = _axes_section_lines(text)
    if section is None:
        return None
    rows: list[tuple[str, str, str]] = []
    for line in section:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        parts = stripped.split("|")
        if len(parts) < 4:
            continue
        cells = [cell.strip() for cell in parts[1:-1]]
        if len(cells) < 3:
            continue
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if cells[0].casefold() == "axis":
            continue
        rows.append((cells[0].casefold(), cells[1], cells[-1]))
    return rows


def _parse_pinned_scores(text: str) -> dict[str, int] | None:
    """Parse the pinned observed scores from the base SCORECARD.md lines.

    The lines are read as committed bytes at the pinned base revision.  The
    parse fails closed: it returns None unless every axis carries exactly one
    score.
    """
    lines = text.split("\n")
    window = lines[SCORECARD_BASE_LINE_START - 1 : SCORECARD_BASE_LINE_END]
    scores: dict[str, int] = {}
    for match in D5_PINNED_SCORE_RE.finditer("\n".join(window)):
        axis = match.group(1).casefold()
        score = int(match.group(2))
        if axis in scores and scores[axis] != score:
            return None
        scores[axis] = score
    if set(scores) != set(D5_AXES):
        return None
    return scores


def _check_d5(repo: str, rev: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {}
    detail["scorecard_path"] = SCORECARD_PATH
    detail["scorecard_base_rev"] = SCORECARD_BASE_REV

    # The pinned observed state is parsed from the committed base lines.
    base_raw = _blob_bytes(repo, SCORECARD_BASE_REV, SCORECARD_PATH)
    if base_raw is None:
        reasons.append("base_scorecard_unreadable")
        return False, reasons, detail
    pinned = _parse_pinned_scores(base_raw.decode("utf-8", "replace"))
    if pinned is None:
        reasons.append("pinned_scores_unparseable")
        return False, reasons, detail
    detail["pinned_scores"] = pinned

    # The `## Axes` table at REV must have exactly one row per axis.
    raw = _blob_bytes(repo, rev, SCORECARD_PATH)
    if raw is None:
        reasons.append("scorecard_missing")
        return False, reasons, detail
    rows = _axes_rows(raw.decode("utf-8", "replace"))
    if rows is None:
        reasons.append("axes_section_missing")
        return False, reasons, detail
    seen: dict[str, list[tuple[str, str]]] = {}
    for axis, score, last_change in rows:
        seen.setdefault(axis, []).append((score, last_change))
    detail["axes_rows"] = {axis: [score for score, _ in entries] for axis, entries in seen.items()}

    for axis in D5_AXES:
        entries = seen.get(axis)
        if not entries:
            reasons.append("axis_row_missing: " + axis)
            continue
        if len(entries) > 1:
            reasons.append("axis_row_duplicated: " + axis)
            continue
        score_text, last_change = entries[0]
        if not re.fullmatch(r"\d+", score_text):
            reasons.append("axis_score_not_numeric: " + axis)
            continue
        score = int(score_text)
        expected = pinned[axis]
        if score != expected:
            reasons.append("axis_score_mismatch: %s %d!=%d" % (axis, score, expected))
            continue
        round1 = D5_ROUND1_SCORES[axis]
        if score != round1 and D5_ROUND1_RE.search(last_change):
            reasons.append("axis_stale_round_1: " + axis)
    return not reasons, reasons, detail


def _count_cases(raw: bytes) -> int | None:
    try:
        document = json.loads(raw.decode("utf-8", "replace"))
    except ValueError:
        return None
    if not isinstance(document, dict):
        return None
    cases = document.get("cases")
    if not isinstance(cases, list) or not cases:
        return None
    return len(cases)


def _check_d3(repo: str, rev: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {}
    raw = _blob_bytes(repo, SUPPLEMENTARY_CASES_BASE_REV, SUPPLEMENTARY_CASES_PATH)
    if raw is None:
        reasons.append("supplementary_cases_unreadable")
        detail["supplementary_cases_base_rev"] = SUPPLEMENTARY_CASES_BASE_REV
        return False, reasons, detail
    total = _count_cases(raw)
    if total is None:
        reasons.append("supplementary_cases_unparsable")
        return False, reasons, detail
    detail["supplementary_cases_base_rev"] = SUPPLEMENTARY_CASES_BASE_REV
    detail["supplementary_case_count"] = total
    marker = "PASS %d/%d" % (total, total)
    detail["pass_marker"] = marker
    marker_re = re.compile(re.escape(marker) + r"(?![0-9])")

    lesson = _blob_bytes(repo, rev, LESSON_PATH)
    if lesson is None:
        reasons.append("lesson_missing")
        detail["lesson_path"] = LESSON_PATH
        return False, reasons, detail
    detail["lesson_path"] = LESSON_PATH
    text = lesson.decode("utf-8", "replace")

    matching_lines: list[str] = []
    tokens: list[str] = []
    for line in text.split("\n"):
        if D3_TOKEN_CORRECTION not in line:
            continue
        if D3_TOKEN_CASE not in line:
            continue
        if not marker_re.search(line):
            continue
        line_tokens = HEX_TOKEN_RE.findall(line)
        if not line_tokens:
            continue
        matching_lines.append(line.strip())
        for token in line_tokens:
            if token not in tokens:
                tokens.append(token)
    detail["matching_lines"] = matching_lines
    if not matching_lines:
        reasons.append("no_line_with_correction_s07_and_pass_marker")
        return False, reasons, detail

    # The hex token must sit on the same line as the other three elements.
    resolved = _batch_check(repo, tokens)
    usable: list[str] = []
    for line in matching_lines:
        for token in HEX_TOKEN_RE.findall(line):
            commit = resolved.get(token)
            if not commit:
                continue
            blob = _blob_bytes(repo, commit, SUPPLEMENTARY_CASES_PATH)
            if blob is None:
                continue
            if _count_cases(blob) == total:
                usable.append(token)
    detail["hex_tokens"] = tokens
    detail["tokens_naming_a_commit_with_n_cases"] = usable
    if not usable:
        reasons.append("no_hex_token_naming_a_commit_with_n_cases")
    return not reasons, reasons, detail


def _check_d4(repo: str, rev: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {}
    raw = _blob_bytes(repo, rev, GITIGNORE_PATH)
    matched: list[str] = []
    if raw is None:
        reasons.append("gitignore_missing")
    else:
        lines = raw.decode("utf-8", "replace").split("\n")
        matched = [line for line in lines if line in D4_IGNORE_LINES]
    detail["gitignore_path"] = GITIGNORE_PATH
    detail["matching_ignore_lines"] = matched
    if not matched:
        reasons.append("no_pycache_ignore_rule")

    tracked = _list_paths(repo, rev)
    gitignore_paths = [path for path in tracked if os.path.basename(path) == ".gitignore"]
    detail["gitignore_files"] = gitignore_paths
    for path in gitignore_paths:
        blob = _blob_bytes(repo, rev, path)
        if blob is None:
            reasons.append("gitignore_unreadable: " + path)
            continue
        for line in blob.decode("utf-8", "replace").split("\n"):
            stripped = line.strip()
            if not stripped.startswith("!"):
                continue
            if any(marker in stripped for marker in D4_NEGATION_MARKERS):
                reasons.append("gitignore_negation_reinstates_bytecode: " + path)

    bytecode = [
        path
        for path in tracked
        if path.startswith(TOOLS_PREFIX)
        and ("__pycache__" in path or path.endswith(".pyc"))
    ]
    detail["tracked_bytecode_paths"] = bytecode
    if bytecode:
        reasons.append("tracked_bytecode_under_tools")

    return not reasons, reasons, detail


def _verdict(rows: list[dict], d4_held: bool) -> tuple[str, int, int, int]:
    """The exit verdict for the counted rows and the hygiene row.

    Returns (status, counted held, mismatches, return code): held only when no
    counted item is red and the D4 hygiene row holds.
    """
    held = sum(1 for row in rows if row["held"])
    mismatches = len(rows) - held
    ok = mismatches == 0 and d4_held
    return ("held" if ok else "failed"), held, mismatches, (RC_HELD if ok else RC_FAILED)


def _emit(payload: dict, rc: int) -> int:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    return rc


def _cannot_evaluate(repo: str, rev: str, error: str) -> int:
    return _emit(
        {
            "schema": SCHEMA,
            "status": "could-not-evaluate",
            "error": error,
            "repo": repo,
            "rev": rev,
            "items": 4,
            "held": None,
            "mismatches": None,
            "rows": [],
            "hygiene": {"id": "D4", "held": None, "reasons": [error]},
        },
        RC_UNAVAILABLE,
    )


# ---- selftest -------------------------------------------------------------


def _selftest_base_dir() -> str:
    """The $TMPDIR every fixture must live under."""
    base = os.environ.get("TMPDIR") or tempfile.gettempdir()
    if not os.path.isdir(base):
        raise SelftestSetupError("fixture base is not a directory: " + base)
    if not os.access(base, os.W_OK):
        raise SelftestSetupError("fixture base is not writable: " + base)
    return base


def _selftest_write(root: str, relpath: str, data: bytes) -> None:
    path = os.path.join(root, relpath)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def _selftest_git(repo: str, args: list[str]) -> str:
    """Run one fixture-building git command with a pinned identity."""
    env = _git_env()
    env.update(SELFTEST_GIT_IDENTITY)
    try:
        proc = subprocess.run(
            ["git", "-c", "commit.gpgsign=false", "-C", repo, *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise SelftestSetupError("git could not run for the fixture") from exc
    if proc.returncode != 0:
        raise SelftestSetupError("git %s failed for the fixture" % " ".join(args))
    return proc.stdout.decode("utf-8", "replace").strip()


def _selftest_fixture(root: str) -> dict[str, str]:
    """Build the throwaway repository; return its revisions and recorded oids."""
    repo = os.path.join(root, "fixture-repo")
    os.makedirs(repo, exist_ok=True)
    _selftest_git(repo, ["init", "--template=", "--quiet"])
    _selftest_write(repo, PRESSURE_TOOL_PATH, SELFTEST_PRESSURE_TOOL)
    _selftest_write(repo, PRESSURE_FIXTURES_PATH + "/cases.json", SELFTEST_PRESSURE_CASES)
    _selftest_write(repo, KNOWLEDGE_PATH, SELFTEST_KNOWLEDGE_ENTRY.encode("utf-8"))
    _selftest_write(repo, LESSON_PATH, SELFTEST_LESSON.encode("utf-8"))
    _selftest_write(repo, SCORECARD_PATH, SELFTEST_SCORECARD.encode("utf-8"))
    _selftest_write(repo, GITIGNORE_PATH, SELFTEST_GITIGNORE)
    _selftest_git(repo, ["add", "--all"])
    _selftest_git(repo, ["commit", "--quiet", "-m", "fixture base"])
    base_rev = _selftest_git(repo, ["rev-parse", "HEAD"])
    tool_blob = _selftest_git(repo, ["rev-parse", "HEAD:" + PRESSURE_TOOL_PATH])
    fixtures_tree = _selftest_git(repo, ["rev-parse", "HEAD:" + PRESSURE_FIXTURES_PATH])

    evidence = (
        "revision: %s\n" % base_rev
        + "command: %s\n" % EVIDENCE_COMMAND
        + "tool_blob: %s\n" % tool_blob
        + "fixtures_tree: %s\n" % fixtures_tree
        + "exit: 0\n"
    ).encode("utf-8") + EXPECTED_BODY
    _selftest_write(repo, EVIDENCE_PATH, evidence)
    _selftest_git(repo, ["add", "--all"])
    _selftest_git(repo, ["commit", "--quiet", "-m", "fixture evidence"])
    evidence_rev = _selftest_git(repo, ["rev-parse", "HEAD"])

    forged = evidence.replace(
        ("command: %s\n" % EVIDENCE_COMMAND).encode("utf-8"),
        b"command: python3 tools/mori-pressure.py --selftest\n",
    ) + b"MATCHER: rejected 48/48 corrupted expectations (replayed)\n"
    _selftest_write(repo, EVIDENCE_PATH, forged)
    _selftest_git(repo, ["add", "--all"])
    _selftest_git(repo, ["commit", "--quiet", "-m", "fixture forged evidence"])
    forged_rev = _selftest_git(repo, ["rev-parse", "HEAD"])

    _selftest_write(repo, GITIGNORE_PATH, SELFTEST_GITIGNORE_NEGATION)
    _selftest_git(repo, ["add", "--all"])
    _selftest_git(repo, ["commit", "--quiet", "-m", "fixture negation"])
    negation_rev = _selftest_git(repo, ["rev-parse", "HEAD"])

    return {
        "repo": repo,
        "base_rev": base_rev,
        "evidence_rev": evidence_rev,
        "forged_rev": forged_rev,
        "negation_rev": negation_rev,
        "tool_blob": tool_blob,
        "fixtures_tree": fixtures_tree,
        "evidence": evidence.decode("utf-8"),
    }


def _selftest_dispatch(raw: list[str]) -> int:
    """Reject companion arguments, then run the self-check."""
    extras = [arg for arg in raw if arg != "--selftest"]
    if extras:
        sys.stderr.write(
            "mori-routed-r24.py: --selftest takes no other argument: %s\n"
            % " ".join(extras)
        )
        return RC_UNAVAILABLE
    return selftest()


def selftest() -> int:
    """Bounded self-check over synthetic fixtures under $TMPDIR."""
    passed: list[str] = []
    failed: list[str] = []

    def arm(name: str, fn) -> None:
        try:
            fn()
        except AssertionError as exc:
            failed.append("%s: %s" % (name, str(exc) or "assertion failed"))
            return
        except Exception as exc:  # an arm failure is reported, never raised
            failed.append("%s: %s: %s" % (name, type(exc).__name__, exc))
            return
        passed.append(name)

    def capture(fn, *args) -> tuple[str, int]:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            rc = fn(*args)
        return buffer.getvalue(), rc

    def report() -> int:
        for name in passed:
            print("selftest PASS " + name)
        for failure in failed:
            print("selftest FAIL " + failure)
        print("%s pass=%d fail=%d" % (SELFTEST_TALLY_PREFIX, len(passed), len(failed)))
        return RC_HELD if not failed else RC_FAILED

    try:
        base = _selftest_base_dir()
        cleanup = tempfile.TemporaryDirectory(
            prefix="mori-routed-r24-selftest-", dir=base
        )
    except Exception as exc:  # setup failure exits 2, after the tally
        failed.append("setup: %s" % exc)
        report()
        return RC_UNAVAILABLE

    with cleanup as root:
        try:
            fixture = _selftest_fixture(root)
            if not os.path.realpath(fixture["repo"]).startswith(
                os.path.realpath(base) + os.sep
            ):
                raise SelftestSetupError("fixture escaped $TMPDIR")
        except Exception as exc:  # fixture build failure exits 2, after the tally
            failed.append("setup: %s" % exc)
            report()
            return RC_UNAVAILABLE

        header = (
            b"revision: " + b"a" * 40 + b"\n"
            b"command: " + EVIDENCE_COMMAND.encode("utf-8") + b"\n"
            b"tool_blob: " + b"b" * 40 + b"\n"
            b"fixtures_tree: " + b"c" * 40 + b"\n"
            b"exit: 0\n"
        )

        def normalize_arm() -> None:
            assert _normalize("  *Refreshed   on `each`\tREAD *") == "refreshed on each read"

        def header_ok_arm() -> None:
            values, body, missing = _split_header(header + EXPECTED_BODY)
            assert missing == [], missing
            assert body == EXPECTED_BODY, body
            assert list(values) == list(HEADER_KEY_ORDER), list(values)
            assert values["exit"] == "0", values

        def header_missing_arm() -> None:
            broken = header.replace(b"tool_blob: ", b"tool_bloc: ")
            values, _body, missing = _split_header(broken + EXPECTED_BODY)
            assert missing == ["tool_blob"], missing
            assert "tool_blob" not in values, values

        def body_anchor_arm() -> None:
            assert EXPECTED_BODY.endswith(b"\n"), EXPECTED_BODY
            assert not EXPECTED_BODY.endswith(b"\n\n"), EXPECTED_BODY
            _values, body, _missing = _split_header(header + EXPECTED_BODY + b"\n")
            assert body != EXPECTED_BODY, body

        def blocks_arm() -> None:
            text = (
                "## facts\n\n- a\n\n### note\n\n- b\n\n## corrections\n\n- (k4) total\n"
            )
            blocks = _blocks(text.split("\n"))
            facts = [
                index
                for index, (heading, _body) in enumerate(blocks)
                if heading is not None and _normalize(heading) == D2_FACTS_HEADING
            ]
            assert len(facts) == 1, facts
            span = _section_span(blocks, facts[0])
            assert span == [facts[0], facts[0] + 1], span

        def data_row_count_arm() -> None:
            block = ["", "| case | expected |", "|---|---|", "| a | one |", "| b | two |", ""]
            assert _data_row_count(block) == 2, _data_row_count(block)
            assert _data_row_count(["", "no table here", ""]) == 0

        def d2_partition_arm() -> None:
            blocks = _blocks(SELFTEST_KNOWLEDGE_ENTRY.split("\n"))
            corrections = [
                index
                for index, (heading, _body) in enumerate(blocks)
                if heading is not None
                and _normalize(heading).startswith(D2_CORRECTIONS_HEADING)
            ]
            assert len(corrections) == 1, corrections
            inside = set(_section_span(blocks, corrections[0]))
            outside_lines = [
                line
                for index, (_heading, body) in enumerate(blocks)
                if index not in inside
                for line in body
            ]
            inside_lines = [line for index in sorted(inside) for line in blocks[index][1]]
            outside_text = " ".join(_normalize(line) for line in outside_lines)
            for phrase in D2_POSITIVE_PHRASES:
                assert phrase in outside_text, phrase
            for pattern in D2_NEGATIVE_PATTERNS:
                assert not re.search(pattern, outside_text), pattern
            assert D2_BANNER_PHRASE not in outside_text, outside_text
            normalized_inside = [_normalize(line) for line in inside_lines]
            assert any(
                D2_CORRECTIONS_TOKEN in line and D2_CORRECTIONS_WORD in line
                for line in normalized_inside
            ), normalized_inside
            banner_variant = SELFTEST_KNOWLEDGE_ENTRY.replace(
                D2_CORRECTIONS_HEADING, D2_CORRECTIONS_HEADING + "\n\nThis section wins."
            )
            whole = " ".join(_normalize(line) for line in banner_variant.split("\n"))
            assert D2_BANNER_PHRASE in whole, whole

        def axes_rows_arm() -> None:
            rows = _axes_rows(SELFTEST_SCORECARD)
            assert rows == [
                ("coverage", "7", "round 41"),
                ("depth", "4", "round 24"),
            ], rows
            piped = _axes_rows(
                "## Axes\n\n| axis | score | last change |\n|---|---|---|\n"
                "| calibration | 5 | note \\| round 1 |\n"
            )
            assert piped == [("calibration", "5", "round 1")], piped
            assert _axes_rows("# scorecard\n\n## Other\n") is None
            assert _axes_rows("no headings at all") is None

        def pinned_scores_arm() -> None:
            filler = ["filler"] * (SCORECARD_BASE_LINE_START - 1)
            window = [
                "| coverage 7 |",
                "| operability 8 |",
                "| depth 5 |",
                "| freshness 6 |",
                "| calibration 5 |",
                "| adjacency 7 |",
                "| other 3 |",
                "",
            ]
            scores = _parse_pinned_scores("\n".join(filler + window))
            assert scores == {
                "coverage": 7,
                "operability": 8,
                "depth": 5,
                "freshness": 6,
                "calibration": 5,
                "adjacency": 7,
            }, scores
            assert _parse_pinned_scores("\n".join(filler + window[:5])) is None
            duplicated = window[:6] + ["| depth 9 |", ""]
            assert _parse_pinned_scores("\n".join(filler + duplicated)) is None

        def round1_arm() -> None:
            assert D5_ROUND1_RE.search("round 1"), "round 1"
            assert D5_ROUND1_RE.search("closed round 1 (start)"), "round 1"
            assert not D5_ROUND1_RE.search("round 12"), "round 12"
            assert not D5_ROUND1_RE.search("round 41"), "round 41"

        def pinned_contract_arm() -> None:
            assert EXPECTED_BODY == (
                b"MORI_PRESSURE_SELFTEST: PASS 12/12\n"
                b"MATCHER: rejected 48/48 corrupted expectations\n"
            ), EXPECTED_BODY
            assert EVIDENCE_COMMAND == (
                "python3 -I -B tools/mori-pressure.py --selftest"
            ), EVIDENCE_COMMAND
            assert HEADER_KEY_ORDER == (
                "revision", "command", "tool_blob", "fixtures_tree", "exit",
            ), HEADER_KEY_ORDER
            assert REVISION_LINE_RE.match("a" * 40), "40 hex must be accepted"
            assert not REVISION_LINE_RE.match("a" * 39), "39 hex must be rejected"
            assert not REVISION_LINE_RE.match("A" * 40), "uppercase hex must be rejected"

        def d2_negative_samples_arm() -> None:
            samples = {
                r"refreshed on (each|every) read": "the table is refreshed on each read",
                r"spike[^|.]{0,60}(is|are|can be|may be) invisible":
                    "a spike in load is invisible",
                r"null[^|.]{0,15}means[^|.]{0,15}undefined":
                    "a null in the cell means undefined",
            }
            assert set(samples) == set(D2_NEGATIVE_PATTERNS), sorted(samples)
            for pattern, sample in samples.items():
                assert re.search(pattern, _normalize(sample)), (pattern, sample)

        def count_cases_arm() -> None:
            assert _count_cases(b'{"cases": [1, 2, 3, 4, 5, 6, 7]}') == 7
            assert _count_cases(b'{"cases": []}') is None
            assert _count_cases(b"[]") is None
            assert _count_cases(b'{"cases": 7}') is None
            assert _count_cases(b"not json") is None

        def hex_token_arm() -> None:
            assert HEX_TOKEN_RE.findall("at `abcdef1`") == ["abcdef1"]
            assert HEX_TOKEN_RE.findall("`abcdef0`") == ["abcdef0"], "7 hex must be accepted"
            assert HEX_TOKEN_RE.findall("`abcdef`") == [], "6 hex must be rejected"
            assert HEX_TOKEN_RE.findall("`abcde`") == [], "5 hex must be rejected"
            assert HEX_TOKEN_RE.findall("f" * 41) == []
            assert HEX_TOKEN_RE.findall("zabcdef1") == []
            assert HEX_TOKEN_RE.findall("abcdef1g") == []

        def resolve_commit_arm() -> None:
            repo = fixture["repo"]
            assert _resolve_commit(repo, fixture["evidence_rev"]) == fixture["evidence_rev"]
            assert _resolve_commit(repo, fixture["evidence_rev"][:7]) == fixture["evidence_rev"]
            assert _resolve_commit(repo, "0" * 40) is None
            assert _is_ancestor(repo, fixture["base_rev"], fixture["evidence_rev"])
            assert not _is_ancestor(repo, fixture["evidence_rev"], fixture["base_rev"])

        def blob_tree_arm() -> None:
            repo, rev = fixture["repo"], fixture["evidence_rev"]
            tree = _ls_tree_entry(repo, rev, PRESSURE_FIXTURES_PATH)
            assert tree is not None and tree[1] == "tree", tree
            assert tree[2] == fixture["fixtures_tree"], tree
            tool = _ls_tree_entry(repo, rev, PRESSURE_TOOL_PATH)
            assert tool is not None and tool[1] == "blob", tool
            assert tool[2] == fixture["tool_blob"], tool
            assert _blob_bytes(repo, rev, PRESSURE_TOOL_PATH) == SELFTEST_PRESSURE_TOOL
            assert _blob_bytes(repo, rev, EVIDENCE_PATH).decode("utf-8") == fixture["evidence"]
            assert _blob_bytes(repo, rev, "absent/path") is None

        def d1_held_arm() -> None:
            held, reasons, detail = _check_d1(
                fixture["repo"], fixture["evidence_rev"], False
            )
            assert held and reasons == [], (held, reasons)
            assert detail["revision"] == fixture["base_rev"], detail
            assert detail["tool_blob"] == fixture["tool_blob"], detail
            assert detail["fixtures_tree"] == fixture["fixtures_tree"], detail
            assert detail["body_sha256"] == hashlib.sha256(EXPECTED_BODY).hexdigest(), detail

        def d1_forged_arm() -> None:
            held, reasons, detail = _check_d1(
                fixture["repo"], fixture["forged_rev"], False
            )
            assert not held, held
            assert "command_line_malformed" in reasons, reasons
            assert "body_not_byte_equal" in reasons, reasons
            assert "rerun" not in detail, detail

        def d4_arm() -> None:
            held, reasons, _detail = _check_d4(fixture["repo"], fixture["evidence_rev"])
            assert held and reasons == [], reasons
            held_negated, reasons_negated, _d = _check_d4(
                fixture["repo"], fixture["negation_rev"]
            )
            assert not held_negated, held_negated
            assert any(
                reason.startswith("gitignore_negation_reinstates_bytecode")
                for reason in reasons_negated
            ), reasons_negated

        def verdict_arm() -> None:
            assert (RC_HELD, RC_FAILED, RC_UNAVAILABLE) == (0, 1, 2)
            green = [{"held": True}] * 4
            assert _verdict(green, True) == ("held", 4, 0, RC_HELD), _verdict(green, True)
            assert _verdict(green, False) == ("failed", 4, 0, RC_FAILED), _verdict(green, False)
            mixed = [{"held": True}, {"held": False}, {"held": True}, {"held": False}]
            assert _verdict(mixed, True) == ("failed", 2, 2, RC_FAILED), _verdict(mixed, True)

        def emit_arm() -> None:
            out, rc = capture(_emit, {"schema": SCHEMA, "held": 4, "mismatches": 0}, RC_HELD)
            assert rc == RC_HELD, rc
            assert out.endswith("\n") and out.count("\n") == 1, out
            assert json.loads(out)["schema"] == SCHEMA, out

        def main_failed_arm() -> None:
            out, rc = capture(
                main, ["--repo", fixture["repo"], "--rev", fixture["evidence_rev"]]
            )
            assert rc == RC_FAILED, rc
            payload = json.loads(out)
            assert payload["schema"] == SCHEMA, payload["schema"]
            assert payload["rev_commit"] == fixture["evidence_rev"], payload
            assert payload["items"] == 4, payload
            assert payload["held"] == 1 and payload["mismatches"] == 3, payload
            assert payload["status"] == "failed", payload["status"]
            assert [row["id"] for row in payload["rows"]] == ["D1", "D2", "D3", "D5"], payload
            row_d1 = payload["rows"][0]
            assert row_d1["held"] is True and row_d1["reasons"] == [], row_d1
            assert payload["rows"][1]["reasons"] == ["base_knowledge_entry_unreadable"], payload
            assert payload["rows"][2]["reasons"] == ["supplementary_cases_unreadable"], payload
            assert payload["rows"][3]["reasons"] == ["base_scorecard_unreadable"], payload
            assert payload["hygiene"]["held"] is True, payload["hygiene"]

        def main_unreadable_repo_arm() -> None:
            out, rc = capture(
                main, ["--repo", os.path.join(fixture["repo"], "absent"), "--rev", "HEAD"]
            )
            assert rc == RC_UNAVAILABLE, rc
            payload = json.loads(out)
            assert payload["status"] == "could-not-evaluate", payload
            assert payload["error"] == "repository path is not a directory", payload
            assert payload["items"] == 4 and payload["held"] is None, payload

        def main_unresolvable_rev_arm() -> None:
            out, rc = capture(main, ["--repo", fixture["repo"], "--rev", "1" * 40])
            assert rc == RC_UNAVAILABLE, rc
            payload = json.loads(out)
            assert payload["error"] == "revision does not resolve to a commit", payload

        def argv_branch_arm() -> None:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = main(["--selftest", "--bogus"])
                assert rc == RC_UNAVAILABLE, rc
            assert out.getvalue() == "", out.getvalue()
            assert "--selftest" in err.getvalue(), err.getvalue()

        def usage_arm() -> None:
            err = io.StringIO()
            try:
                with contextlib.redirect_stderr(err):
                    main([])
            except SystemExit as exc:
                assert exc.code == RC_UNAVAILABLE, exc.code
            else:
                raise AssertionError("main([]) did not exit through argparse")
            assert "--repo" in err.getvalue() and "--rev" in err.getvalue(), err.getvalue()

        arm("normalize_folds_markers_case_whitespace", normalize_arm)
        arm("split_header_reads_five_keys_and_body", header_ok_arm)
        arm("split_header_reports_the_missing_key", header_missing_arm)
        arm("body_is_byte_anchored", body_anchor_arm)
        arm("blocks_and_section_span_partition", blocks_arm)
        arm("data_row_count_excludes_header_and_separator", data_row_count_arm)
        arm("d2_negatives_absent_positives_present_outside", d2_partition_arm)
        arm("axes_rows_read_score_and_last_change", axes_rows_arm)
        arm("pinned_scores_parse_window_and_fail_closed", pinned_scores_arm)
        arm("round1_token_regex", round1_arm)
        arm("pinned_contract_literals", pinned_contract_arm)
        arm("d2_negative_patterns_match_samples", d2_negative_samples_arm)
        arm("count_cases_json_arms", count_cases_arm)
        arm("hex_token_width_and_boundaries", hex_token_arm)
        arm("resolve_commit_and_ancestor", resolve_commit_arm)
        arm("ls_tree_entry_and_blob_bytes", blob_tree_arm)
        arm("check_d1_holds_on_synthetic_evidence", d1_held_arm)
        arm("check_d1_rejects_forged_evidence", d1_forged_arm)
        arm("check_d4_holds_and_rejects_negation", d4_arm)
        arm("verdict_maps_held_and_failed", verdict_arm)
        arm("emit_writes_one_json_line", emit_arm)
        arm("main_failed_verdict_exit_1", main_failed_arm)
        arm("main_unreadable_repo_exit_2", main_unreadable_repo_arm)
        arm("main_unresolvable_rev_exit_2", main_unresolvable_rev_arm)
        arm("selftest_flag_branch_rejects_companions", argv_branch_arm)
        arm("repo_and_rev_stay_required", usage_arm)

    return report()


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    # The self-check needs no repository, and the production usage error must
    # not move: dispatch on the flag before argparse enforces --repo/--rev.
    if "--selftest" in raw:
        return _selftest_dispatch(raw)

    parser = argparse.ArgumentParser(
        description="Check the round-24 routed defect items D1..D5 against committed bytes.",
        allow_abbrev=False,
    )
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument(
        "--rerun",
        action="store_true",
        help="also re-execute the named revision's pressure selftest and report byte equality",
    )
    args = parser.parse_args(list(sys.argv[1:] if argv is None else argv))

    repo = args.repo
    rev = args.rev

    if not os.path.isdir(repo):
        return _cannot_evaluate(repo, rev, "repository path is not a directory")
    try:
        rev_commit = _resolve_commit(repo, rev)
    except (GitUnavailable, GitError) as exc:
        return _cannot_evaluate(repo, rev, str(exc))
    if rev_commit is None:
        return _cannot_evaluate(repo, rev, "revision does not resolve to a commit")

    try:
        d1_held, d1_reasons, d1_detail = _check_d1(repo, rev_commit, args.rerun)
        d2_held, d2_reasons, d2_detail = _check_d2(repo, rev_commit)
        d3_held, d3_reasons, d3_detail = _check_d3(repo, rev_commit)
        d5_held, d5_reasons, d5_detail = _check_d5(repo, rev_commit)
        d4_held, d4_reasons, d4_detail = _check_d4(repo, rev_commit)
    except (GitUnavailable, GitError) as exc:
        return _cannot_evaluate(repo, rev, str(exc))

    rows = [
        {"id": "D1", "held": d1_held, "reasons": d1_reasons, "detail": d1_detail},
        {"id": "D2", "held": d2_held, "reasons": d2_reasons, "detail": d2_detail},
        {"id": "D3", "held": d3_held, "reasons": d3_reasons, "detail": d3_detail},
        {"id": "D5", "held": d5_held, "reasons": d5_reasons, "detail": d5_detail},
    ]
    status, held, mismatches, rc = _verdict(rows, d4_held)
    payload = {
        "schema": SCHEMA,
        "status": status,
        "repo": repo,
        "rev": rev,
        "rev_commit": rev_commit,
        "items": len(rows),
        "held": held,
        "mismatches": mismatches,
        "rows": rows,
        "hygiene": {"id": "D4", "held": d4_held, "reasons": d4_reasons, "detail": d4_detail},
    }
    return _emit(payload, rc)


if __name__ == "__main__":
    sys.exit(main())
