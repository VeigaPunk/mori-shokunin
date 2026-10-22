#!/usr/bin/env python3
"""Read-only check of the round-24 routed defect items D1..D4 against committed bytes.

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

Hygiene row (reported, not counted):

  D4  ``.gitignore`` at REV has a line that is exactly one of
      ``__pycache__/``, ``__pycache__``, ``**/__pycache__/``,
      ``tools/__pycache__/``, ``*.pyc``, ``*.py[cod]``; no ``.gitignore`` in the
      REV tree has a ``!`` line mentioning ``pycache`` or ``.py``; and no
      tracked path under ``tools/`` contains ``__pycache__`` or ends ``.pyc``.

Output: one JSON object, ``schema: mori-routed-r24-v1``, ``items: 3``, ``held``,
``mismatches``, one row per counted item ``{id, held, reasons[], detail}`` and
``hygiene: {id: D4, held, reasons[]}``.  Exit 0 only when ``mismatches`` is 0
and the hygiene row holds, 1 otherwise, and 2 when the repository or the
revision cannot be read.

Python 3 standard library only; read-only; safe under ``python3 -I -B``.
"""

from __future__ import annotations

import argparse
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
            "items": 3,
            "held": None,
            "mismatches": None,
            "rows": [],
            "hygiene": {"id": "D4", "held": None, "reasons": [error]},
        },
        RC_UNAVAILABLE,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check the round-24 routed defect items D1..D4 against committed bytes.",
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
        d4_held, d4_reasons, d4_detail = _check_d4(repo, rev_commit)
    except (GitUnavailable, GitError) as exc:
        return _cannot_evaluate(repo, rev, str(exc))

    rows = [
        {"id": "D1", "held": d1_held, "reasons": d1_reasons, "detail": d1_detail},
        {"id": "D2", "held": d2_held, "reasons": d2_reasons, "detail": d2_detail},
        {"id": "D3", "held": d3_held, "reasons": d3_reasons, "detail": d3_detail},
    ]
    held = sum(1 for row in rows if row["held"])
    mismatches = len(rows) - held
    payload = {
        "schema": SCHEMA,
        "status": "held" if mismatches == 0 and d4_held else "failed",
        "repo": repo,
        "rev": rev,
        "rev_commit": rev_commit,
        "items": len(rows),
        "held": held,
        "mismatches": mismatches,
        "rows": rows,
        "hygiene": {"id": "D4", "held": d4_held, "reasons": d4_reasons, "detail": d4_detail},
    }
    ok = mismatches == 0 and d4_held
    return _emit(payload, RC_HELD if ok else RC_FAILED)


if __name__ == "__main__":
    sys.exit(main())
