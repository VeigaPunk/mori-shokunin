#!/usr/bin/env python3
"""Read-only check of the round-23 routed defect items against committed bytes.

One command re-derives the round-23 routed items R1..R4 at a committed
revision.  Every predicate reads git objects only (ls-tree, cat-file, rev-parse,
log, diff) with a clean environment; the working tree is never consulted and
nothing is written.

The base revision is fixed to the round-23 verifier spot-check tip
(c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130).  R4 dispatches the committed
tools/mori-dispatch-ledger.py bytes of the same revision as a subprocess and
requires a clean verification.

Items (contract C1, as amended by A1 and A4):

  R1  round-23 routed item 1 -- quota capability stays absent, the whole
      .ufo/waves/round-23 tree is pinned to base, no quota path was added
      under tools/ or corpus/knowledge/ since base, and no file under tools/
      names the historical case.
  R2  round-23 routed item 2 -- retention evidence bytes and the retention
      tools are pinned to base, and no added line on the lane's own
      self-assessment and knowledge surfaces claims privacy clearance.
  R3  round-23 routed item 3 -- capture limitations preserved; the whole
      .ufo/waves/round-23 tree is pinned to base.
  R4  round-23 routed item 4 -- future dispatches are bound before the call.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

SCHEMA = "mori-routed-check-v1"
BASE_REV = "c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130"
LEDGER_TOOL_PATH = "tools/mori-dispatch-ledger.py"

RC_HELD = 0
RC_FAILED = 1
RC_UNAVAILABLE = 2

GIT_TIMEOUT_SECONDS = 60
LEDGER_TIMEOUT_SECONDS = 60

# R2: a line that claims privacy clearance is a routed-item violation.
PRIVACY_CLEARANCE_TRUE_RE = re.compile(
    r"privacy_clearance\s*[\"']?\s*[=:]\s*[\"']?true", re.IGNORECASE
)

# R2 scan scope (amendment A1): the lane's own self-assessment and knowledge
# surfaces only.  Wave reports under .ufo/** and tool sources under tools/**
# are deliberately excluded: they quote the pattern rather than assert it.
R2_SCAN_SCOPE = (
    "SCORECARD.md",
    "PROVINCE.md",
    "SKILL.md",
    "LOG.md",
    "README.md",
    "corpus/",
)

# R1: the historical quota case name must not be special-cased anywhere under
# tools/.  The needle is assembled at run time so this source file never
# contains the literal it searches for, and the scan therefore covers every
# file under tools/ without excluding this tool.
HISTORICAL_CASE_NEEDLE = "Case" + "Escaped" + "Space"

# R1: the quota capability paths stay absent at the checked revision.
R1_ABSENT_PATHS = (
    "tools/mori-quota-surface.py",
    "corpus/knowledge/quota-surface-r23.md",
)

# R1: the round-23 frozen tree is pinned to base (subsumed by the whole-tree
# pin; reported for direct traceability of the original predicate).
R1_FROZEN_TREE_PATH = ".ufo/waves/round-23/frozen"

# R1: any path added under these roots since base must not carry the quota
# capability name.
R1_QUOTA_PATH_ROOTS = ("tools/", "corpus/knowledge/")
R1_QUOTA_PATH_MARKER = "quota"

# R1 and R3: the whole round-23 wave tree is pinned to base.
ROUND23_TREE_PATH = ".ufo/waves/round-23"

# R2: retention evidence blobs and the retention tools are pinned to base.
R2_BLOB_PATHS = (
    ".ufo/waves/round-23/evidence/retention-floor-final.json",
    ".ufo/waves/round-23/evidence/retention-floor-final-comparison.json",
    "tools/mori-retention-gate.py",
    "tools/mori-retention-reconcile.py",
)

# R3: capture limitation evidence is pinned to base.
R3_BLOB_PATHS = (
    ".ufo/waves/round-23/evidence/harness-receipt-overwrite.json",
    ".ufo/waves/round-23/evidence/tmpfs-source-provenance-erratum.json",
)
R3_REJECTED_TREE_PATH = ".ufo/waves/round-23/rejected"


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


def _git(repo: str, args: list[str], *, allow_failure: bool = False) -> bytes:
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
    if proc.returncode != 0:
        if allow_failure:
            return proc.stdout
        raise GitError("git read failed: " + " ".join(args))
    return proc.stdout


def _git_status(repo: str, args: list[str]) -> int:
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", "-C", repo, *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=_git_env(),
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitUnavailable("git read failed") from exc
    return proc.returncode


def _rev_parse(repo: str, rev: str) -> str:
    out = _git(repo, ["rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"], allow_failure=True)
    value = out.decode("utf-8", "replace").strip()
    if not value:
        raise GitUnavailable("revision does not resolve to a commit")
    return value


def _oid_at(repo: str, rev: str, path: str) -> str | None:
    """Return the object id of `path` at `rev`, or None when it is absent."""
    try:
        proc = subprocess.run(
            [
                "git",
                "--no-optional-locks",
                "-C",
                repo,
                "rev-parse",
                "--verify",
                "--quiet",
                f"{rev}:{path}",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=_git_env(),
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitUnavailable("git read failed") from exc
    if proc.returncode != 0:
        return None
    value = proc.stdout.decode("utf-8", "replace").strip()
    return value or None


def _object_type(repo: str, oid: str) -> str:
    return _git(repo, ["cat-file", "-t", oid]).decode("utf-8", "replace").strip()


def _blob_bytes(repo: str, rev: str, path: str) -> bytes:
    try:
        return _git(repo, ["cat-file", "blob", f"{rev}:{path}"])
    except GitError as exc:
        raise GitUnavailable("committed blob is unavailable") from exc


def _list_paths(repo: str, rev: str, prefix: str) -> list[str]:
    out = _git(repo, ["ls-tree", "-r", "-z", rev, "--", prefix])
    paths = []
    for record in out.split(b"\0"):
        if not record:
            continue
        _, _, raw = record.partition(b"\t")
        paths.append(raw.decode("utf-8", "replace"))
    return paths


def _added_lines(repo: str, base: str, rev: str) -> list[tuple[str, str]]:
    """Return (path, line) for every line added between `base` and `rev`.

    The scan is limited to R2_SCAN_SCOPE: the lane's own self-assessment and
    knowledge surfaces.  .ufo/** and tools/** are excluded by the pathspec, so
    wave reports and tool sources that quote the pattern are never read.
    """
    out = _git(
        repo,
        [
            "diff",
            "--no-color",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--unified=0",
            base,
            rev,
            "--",
            *R2_SCAN_SCOPE,
        ],
    )
    added: list[tuple[str, str]] = []
    current: str | None = None
    for raw in out.decode("utf-8", "replace").splitlines():
        if raw.startswith("diff --git "):
            current = None
            continue
        if raw.startswith("+++ "):
            target = raw[4:].strip()
            if target == "/dev/null":
                current = None
            else:
                if target.startswith("b/"):
                    target = target[2:]
                current = target
            continue
        if raw.startswith("---") or raw.startswith("index ") or raw.startswith("@@"):
            continue
        if raw.startswith("+"):
            added.append((current or "", raw[1:]))
    return added


def _added_paths(repo: str, base: str, rev: str, roots: tuple[str, ...]) -> list[str]:
    out = _git(
        repo,
        [
            "diff",
            "--no-color",
            "--no-ext-diff",
            "--no-textconv",
            "--no-renames",
            "--name-only",
            "--diff-filter=A",
            base,
            rev,
            "--",
            *roots,
        ],
    )
    return [line for line in out.decode("utf-8", "replace").splitlines() if line.strip()]


def _parse_timestamp(value: object) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value.strip()
    if normalized.endswith(("Z", "z")):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def _last_change_epoch(repo: str, rev: str, path: str) -> int | None:
    """Committer epoch of the commit that last changed the blob at `path`.

    Only commits reachable from `rev` are considered.  A path that was never
    committed at or before `rev` yields None.
    """
    out = _git(
        repo,
        ["log", "-1", "--format=%ct", rev, "--", path],
        allow_failure=True,
    )
    for raw in out.decode("utf-8", "replace").splitlines():
        raw = raw.strip()
        if raw.isdigit():
            return int(raw)
    return None


def _ledger_rows(repo: str, rev: str, path: str) -> list[dict]:
    raw = _blob_bytes(repo, rev, path)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitUnavailable("attempt ledger is not valid UTF-8 JSON") from exc
    if not isinstance(parsed, list):
        raise GitUnavailable("attempt ledger is not a JSON array")
    return [row for row in parsed if isinstance(row, dict)]


def _run_ledger_verify(repo: str, rev: str, ledger_path: str) -> tuple[int, dict | None]:
    """Run the committed ledger tool of `rev` against `ledger_path`."""
    tool_bytes = _blob_bytes(repo, rev, LEDGER_TOOL_PATH)
    env = _git_env()
    env["HOME"] = env.get("HOME", os.path.expanduser("~"))
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-", "verify", "--repo", repo, "--rev", rev, "--ledger", ledger_path],
            input=tool_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env,
            timeout=LEDGER_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise GitUnavailable("dispatch ledger verification could not run") from exc
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        payload = None
    return proc.returncode, payload if isinstance(payload, dict) else None


def _check_r1(repo: str, rev: str, base: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {
        "round23_tree": {},
        "frozen_tree": {},
        "quota_paths_absent": {},
        "quota_paths_added": [],
        "historical_case_hits": [],
    }

    base_tree = _oid_at(repo, base, ROUND23_TREE_PATH)
    rev_tree = _oid_at(repo, rev, ROUND23_TREE_PATH)
    detail["round23_tree"] = {"base": base_tree, "rev": rev_tree}  # type: ignore[assignment]
    if base_tree is None or rev_tree is None:
        reasons.append("round23_tree_unreadable")
    elif _object_type(repo, rev_tree) != "tree":
        reasons.append("round23_tree_not_a_tree")
    elif base_tree != rev_tree:
        reasons.append("round23_tree_changed")

    base_frozen = _oid_at(repo, base, R1_FROZEN_TREE_PATH)
    rev_frozen = _oid_at(repo, rev, R1_FROZEN_TREE_PATH)
    detail["frozen_tree"] = {"base": base_frozen, "rev": rev_frozen}  # type: ignore[assignment]
    if base_frozen is None or rev_frozen is None:
        reasons.append("frozen_tree_unreadable")
    elif base_frozen != rev_frozen:
        reasons.append("frozen_tree_changed")

    for path in R1_ABSENT_PATHS:
        oid = _oid_at(repo, rev, path)
        detail["quota_paths_absent"][path] = oid  # type: ignore[index]
        if oid is not None:
            reasons.append("quota_capability_present")

    quota_paths = [
        path
        for path in _added_paths(repo, base, rev, R1_QUOTA_PATH_ROOTS)
        if R1_QUOTA_PATH_MARKER in path.lower()
    ]
    detail["quota_paths_added"] = quota_paths
    if quota_paths:
        reasons.append("quota_path_added")

    hits: list[str] = []
    needle = HISTORICAL_CASE_NEEDLE.encode("utf-8")
    for path in _list_paths(repo, rev, "tools/"):
        try:
            blob = _blob_bytes(repo, rev, path)
        except GitUnavailable:
            continue
        if needle in blob:
            hits.append(path)
    detail["historical_case_hits"] = hits
    if hits:
        reasons.append("historical_case_named_in_tools")

    return not reasons, reasons, detail


def _check_r2(repo: str, rev: str, base: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {
        "blobs": {},
        "privacy_clearance_true_lines": [],
        "scan_scope": list(R2_SCAN_SCOPE),
        "scanned_paths": [],
    }
    for path in R2_BLOB_PATHS:
        base_oid = _oid_at(repo, base, path)
        rev_oid = _oid_at(repo, rev, path)
        detail["blobs"][path] = {"base": base_oid, "rev": rev_oid}  # type: ignore[index]
        if base_oid is None or rev_oid is None:
            reasons.append("retention_evidence_unreadable")
        elif base_oid != rev_oid:
            reasons.append("retention_evidence_changed")
    added = _added_lines(repo, base, rev)
    detail["scanned_paths"] = sorted({path for path, _line in added})
    offending = [
        {"path": path, "line": line}
        for path, line in added
        if PRIVACY_CLEARANCE_TRUE_RE.search(line)
    ]
    detail["privacy_clearance_true_lines"] = offending
    if offending:
        reasons.append("privacy_clearance_true_line_added")
    return not reasons, reasons, detail


def _check_r3(repo: str, rev: str, base: str) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {"blobs": {}, "rejected_tree": {}, "round23_tree": {}}

    base_tree = _oid_at(repo, base, ROUND23_TREE_PATH)
    rev_tree = _oid_at(repo, rev, ROUND23_TREE_PATH)
    detail["round23_tree"] = {"base": base_tree, "rev": rev_tree}  # type: ignore[assignment]
    if base_tree is None or rev_tree is None:
        reasons.append("round23_tree_unreadable")
    elif _object_type(repo, rev_tree) != "tree":
        reasons.append("round23_tree_not_a_tree")
    elif base_tree != rev_tree:
        reasons.append("round23_tree_changed")

    for path in R3_BLOB_PATHS:
        base_oid = _oid_at(repo, base, path)
        rev_oid = _oid_at(repo, rev, path)
        detail["blobs"][path] = {"base": base_oid, "rev": rev_oid}  # type: ignore[index]
        if base_oid is None or rev_oid is None:
            reasons.append("capture_evidence_unreadable")
        elif base_oid != rev_oid:
            reasons.append("capture_evidence_changed")

    base_rejected = _oid_at(repo, base, R3_REJECTED_TREE_PATH)
    rev_rejected = _oid_at(repo, rev, R3_REJECTED_TREE_PATH)
    detail["rejected_tree"] = {"base": base_rejected, "rev": rev_rejected}  # type: ignore[assignment]
    if base_rejected is None or rev_rejected is None:
        reasons.append("rejected_tree_unreadable")
    elif _object_type(repo, rev_rejected) != "tree":
        reasons.append("rejected_tree_not_a_tree")
    elif base_rejected != rev_rejected:
        reasons.append("rejected_tree_changed")

    return not reasons, reasons, detail


def _round_wave_files(repo: str, rev: str, round_number: int) -> tuple[list[str], list[str]]:
    """Return (ledger candidates, wave spec files) directly under the round tree."""
    prefix = f".ufo/waves/round-{round_number}/"
    ledger_re = re.compile(rf"^{re.escape(prefix)}[^/]+-(attempts|ledger)\.json$")
    spec_re = re.compile(rf"^{re.escape(prefix)}wave[^/]*-spec\.json$")
    ledgers: list[str] = []
    specs: list[str] = []
    for path in _list_paths(repo, rev, prefix):
        if ledger_re.match(path):
            ledgers.append(path)
        elif spec_re.match(path):
            specs.append(path)
    return sorted(ledgers), sorted(specs)


def _spec_wave(repo: str, rev: str, spec_path: str) -> str | None:
    """The `wave` field of a committed wave spec file."""
    raw = _blob_bytes(repo, rev, spec_path)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitUnavailable("wave spec is not valid UTF-8 JSON") from exc
    if not isinstance(parsed, dict):
        return None
    wave = parsed.get("wave")
    return wave if isinstance(wave, str) and wave else None


def _ledger_waves(rows: list[dict]) -> set[str]:
    """The set of `wave` values carried by the rows of a ledger."""
    waves = set()
    for row in rows:
        wave = row.get("wave")
        if isinstance(wave, str) and wave:
            waves.add(wave)
    return waves


def _wave_number(path: str) -> str | None:
    """The wave number in a wave file name, e.g. `wave1-spec.json` -> `1`."""
    match = re.search(r"wave(\d+)", path.rsplit("/", 1)[-1])
    return match.group(1) if match else None


def _ledger_is_for_spec(
    spec_path: str,
    spec_wave: str | None,
    ledger_path: str,
    ledger_wave_values: set[str],
) -> bool:
    """True when `ledger_path` is a ledger of the wave named by `spec_path`.

    The wave value carried by the ledger rows decides the match.  A ledger
    whose rows carry no wave value at all is matched by its file name instead,
    so a legacy ledger is not silently unpaired with its own spec.
    """
    if spec_wave is not None:
        if spec_wave in ledger_wave_values:
            return True
        if ledger_wave_values:
            return False
    spec_number = _wave_number(spec_path)
    ledger_number = _wave_number(ledger_path)
    if spec_number is None or ledger_number is None:
        return False
    return spec_number == ledger_number


def _check_r4(repo: str, rev: str, round_number: int) -> tuple[bool, list[str], dict]:
    reasons: list[str] = []
    detail: dict[str, object] = {"round": round_number, "ledgers": [], "specs": []}

    ledgers, specs = _round_wave_files(repo, rev, round_number)
    detail["ledgers_found"] = ledgers
    detail["specs_found"] = specs
    if not ledgers:
        reasons.append("no_round_ledger")
        return False, reasons, detail

    ledger_rows: dict[str, list[dict]] = {}
    ledger_waves: dict[str, set[str]] = {}
    for ledger_path in ledgers:
        entry: dict[str, object] = {"path": ledger_path}
        # A verify exit of 2 (a missing dispatch path or unreadable ledger) is
        # an R4 finding, not a tool-level failure.
        try:
            rc, payload = _run_ledger_verify(repo, rev, ledger_path)
        except GitUnavailable:
            entry["verify_exit"] = None
            entry["verify_status"] = None
            entry["verify_findings"] = []
            reasons.append("dispatch_ledger_tool_unavailable")
            detail["ledgers"].append(entry)  # type: ignore[union-attr]
            continue
        entry["verify_exit"] = rc
        entry["verify_status"] = None if payload is None else payload.get("status")
        entry["verify_findings"] = [] if payload is None else payload.get("finding_ids")
        if rc != 0 or payload is None or payload.get("status") != "clean":
            reasons.append("attempt_ledger_not_clean")
            for finding_id in entry["verify_findings"]:  # type: ignore[union-attr]
                if isinstance(finding_id, str) and finding_id != "LEDGER_CLEAN":
                    reasons.append("ledger_finding:" + finding_id)
        try:
            rows = _ledger_rows(repo, rev, ledger_path)
        except GitUnavailable:
            reasons.append("attempt_ledger_unreadable")
            detail["ledgers"].append(entry)  # type: ignore[union-attr]
            continue
        ledger_rows[ledger_path] = rows
        ledger_waves[ledger_path] = _ledger_waves(rows)

        row_reports = []
        for index, row in enumerate(rows, 1):
            report: dict[str, object] = {"row": index}
            dispatch_path = row.get("dispatch_path")
            at_value = row.get("at")
            at = _parse_timestamp(at_value)
            report["dispatch_path"] = dispatch_path
            report["at"] = at_value
            if not isinstance(dispatch_path, str) or not dispatch_path:
                report["status"] = "no_dispatch_path"
                reasons.append("dispatch_path_missing")
                row_reports.append(report)
                continue
            if at is None:
                report["status"] = "invalid_at"
                reasons.append("dispatch_at_invalid")
                row_reports.append(report)
                continue
            changed_epoch = _last_change_epoch(repo, rev, dispatch_path)
            report["dispatch_last_changed_epoch"] = changed_epoch
            report["at_epoch"] = int(at.timestamp())
            if changed_epoch is None:
                report["status"] = "dispatch_not_committed"
                reasons.append("dispatch_not_committed")
            elif changed_epoch > int(at.timestamp()):
                report["status"] = "dispatch_committed_after_dispatch"
                reasons.append("dispatch_committed_after_dispatch")
            else:
                report["status"] = "bound_before_call"
            row_reports.append(report)
        entry["rows"] = row_reports
        detail["ledgers"].append(entry)  # type: ignore[union-attr]

    # Every wave spec of the round needs a ledger of the same wave whose last
    # row says the wave actually started.
    for spec_path in specs:
        spec_wave = _spec_wave(repo, rev, spec_path)
        matching = [
            path
            for path in ledgers
            if path in ledger_rows
            and _ledger_is_for_spec(spec_path, spec_wave, path, ledger_waves.get(path, set()))
        ]
        report: dict[str, object] = {
            "spec": spec_path,
            "spec_wave": spec_wave,
            "candidate_ledgers": matching,
        }
        started = False
        for ledger_path in matching:
            rows = ledger_rows[ledger_path]
            if not rows:
                continue
            last_result = rows[-1].get("result")
            report.setdefault("last_row_results", {})[ledger_path] = last_result  # type: ignore[union-attr]
            if last_result in ("started", "partial"):
                started = True
        report["started"] = started
        detail["specs"].append(report)  # type: ignore[union-attr]
        if not started:
            reasons.append("wave_spec_without_started_ledger")

    return not reasons, reasons, detail


def _emit(payload: dict, rc: int) -> int:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
    return rc


def _cannot_evaluate(repo: str, rev: str, base: str, error: str) -> int:
    return _emit(
        {
            "schema": SCHEMA,
            "status": "could-not-evaluate",
            "error": error,
            "repo": repo,
            "rev": rev,
            "base": base,
        },
        RC_UNAVAILABLE,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check the round-23 routed defect items against committed bytes.",
        allow_abbrev=False,
    )
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--round", type=int, default=24, dest="round_number")
    args = parser.parse_args(list(sys.argv[1:] if argv is None else argv))

    repo = args.repo
    rev = args.rev
    base = BASE_REV
    round_number = args.round_number

    if round_number <= 0:
        return _cannot_evaluate(repo, rev, base, "round must be a positive integer")

    try:
        if not os.path.isdir(repo):
            raise GitUnavailable("repository path is not a directory")
        if _git_status(repo, ["rev-parse", "--git-dir"]) != 0:
            raise GitUnavailable("repository path is not a git repository")
        rev_commit = _rev_parse(repo, rev)
        base_commit = _rev_parse(repo, base)
    except (GitUnavailable, GitError) as exc:
        return _cannot_evaluate(repo, rev, base, str(exc))

    try:
        r1_held, r1_reasons, r1_detail = _check_r1(repo, rev_commit, base_commit)
        r2_held, r2_reasons, r2_detail = _check_r2(repo, rev_commit, base_commit)
        r3_held, r3_reasons, r3_detail = _check_r3(repo, rev_commit, base_commit)
        r4_held, r4_reasons, r4_detail = _check_r4(repo, rev_commit, round_number)
    except (GitUnavailable, GitError) as exc:
        return _cannot_evaluate(repo, rev, base, str(exc))

    rows = [
        {"id": "R1", "held": r1_held, "reasons": r1_reasons, "detail": r1_detail},
        {"id": "R2", "held": r2_held, "reasons": r2_reasons, "detail": r2_detail},
        {"id": "R3", "held": r3_held, "reasons": r3_reasons, "detail": r3_detail},
        {"id": "R4", "held": r4_held, "reasons": r4_reasons, "detail": r4_detail},
    ]
    held = sum(1 for row in rows if row["held"])
    payload = {
        "schema": SCHEMA,
        "status": "held" if held == len(rows) else "failed",
        "repo": repo,
        "rev": rev,
        "rev_commit": rev_commit,
        "base": base,
        "base_commit": base_commit,
        "round": round_number,
        "items": len(rows),
        "held": held,
        "rows": rows,
    }
    return _emit(payload, RC_HELD if held == len(rows) else RC_FAILED)


if __name__ == "__main__":
    sys.exit(main())
