#!/usr/bin/env python3
"""mori-round16-context-check.py — static gate for wave-spec contract context.

WHAT THIS GATE IS

  A small advisory text gate. It reads one wave spec document (--spec PATH),
  collects every string value stored under a key literally named ``context``
  (a top-level string document is itself the context), and requires that each
  collected context explicitly carries the round-16 contract restrictions:

    no_broadcast_exact_id       the context forbids ``agent://all`` broadcast
                                and requires exact seat-id / L1 addressing
    lane_report_resolution      the context binds ``Report:`` trailers to a
                                resolved write location (relative-to-root or
                                absolute-path wording)
    no_verification_permission  the context denies verification authority
                                (skip-build/test wording or the
                                selftest-is-not-permission clause)
    pacman_pause                the context declares the host-wide pacman
                                pause
    credential_prohibition      the context prohibits reading/copying/
                                querying/changing credential, auth, agent.db,
                                token, or session-material files
    write_scope                 the context confines writes to the assigned
                                file plus the lane report path
    no_live_journal_queries     the context explicitly bans live journal /
                                journalctl queries, measurement, or probe
                                loops — the prohibition must bind ``live``
                                to ``journal``; a selftest-only "no
                                network/live reads" clause does NOT satisfy
                                this restriction
    no_tmp_probe_outputs        the context forbids deliberate /tmp probe,
                                output, or download writes

  Exit 0 prints {"finding_id": "CONTEXT_OK", ...}; every collected context
  satisfied every clause. Exit 1 prints {"finding_id": "CONTEXT_MISSING",
  "missing": [...]} with the clause identifiers absent from at least one
  context (or every clause when no context string exists at all, flagged by
  "context_absent": true). Exit 2 prints {"finding_id": "CONTEXT_SETUP"}
  when the spec cannot be read or parsed — a gate misconfiguration, never a
  spec verdict.

WHAT THIS GATE IS NOT

  This is a static presence check over spec text. It does NOT prevent
  anything at runtime: it cannot stop a seat from broadcasting, running
  verification, issuing live journal queries, writing probes to /tmp,
  touching credentials, or writing outside its lane. Output always carries
  "claims_runtime_prevention": false. It also does not detect a context that
  states a clause and then contradicts it; that is reviewer work, not this
  gate's.

OUTPUT DISCIPLINE

  stdout carries exactly one JSON object. Spec text is never echoed back —
  only clause identifiers, counts, and the spec SHA-256.

--selftest builds isolated spec documents under a fresh mkdtemp tree, runs
this CLI as a real subprocess for a positive, one negative per dropped
clause, absent-context and malformed-spec arms, and asserts exit code,
finding_id, and missing-clause identity. It never touches the repository or
network. Existence of --selftest is not permission to run it during a wave.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RC_OK = 0
RC_MISSING = 1
RC_SETUP = 2

# Each clause: (clause_id, [group, ...]). A clause is present when EVERY group
# has at least one matching alternative. Groups are ordered: a mention/target
# group precedes its binding-rule group where both are required.
_CLAUSES = (
    (
        "no_broadcast_exact_id",
        (
            (
                r"(?:never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|don't|no)\b"
                r"[^\n]{0,80}agent://all",
                r"agent://all[^\n]{0,80}\b(?:never|forbidden|prohibit(?:ed|s)?|banned)",
            ),
            (
                r"exact\s+(?:seat\s+)?id\b",
                r"only\s+exact\b",
                r"exact\s+id\b",
            ),
        ),
    ),
    (
        "lane_report_resolution",
        (
            (r"\breport\b",),
            (
                r"relative\s+to\b",
                r"absolute\s+(?:report\s+)?path\b",
                r"write\s+it\s+at\b",
                r"report\s*dir(?:ectory)?\b",
                r"under\s+/",
                r"\.ufo/",
            ),
        ),
    ),
    (
        "no_verification_permission",
        (
            (
                r"selftest[^\n]{0,80}not\s+permission",
                r"not\s+permission[^\n]{0,80}(?:execute|run|selftest)",
                r"skip[^\n]{0,60}(?:build|test|lint|format|gate|smoke|verif)",
                r"no\s+execution\b",
                r"never\s+execute\b",
                r"do\s+not\s+(?:execute|run|verify)\b",
                r"without\s+verif",
            ),
        ),
    ),
    (
        "pacman_pause",
        (
            (
                r"pacman[^\n]{0,60}paus",
                r"paus\w*[^\n]{0,60}pacman",
                r"no\s+pacman\b",
                r"pacman[^\n]{0,60}(?:forbidden|prohibit(?:ed|s)?|off[\s-]*limits)",
            ),
        ),
    ),
    (
        "credential_prohibition",
        (
            (
                r"credential",
                r"agent\.db",
                r"oauth",
                r"server\.token",
                r"session\s+material",
                r"auth(?:entication)?\s+file",
            ),
            (
                r"(?:never|do\s+not|don't|must\s+not|prohibit(?:ed|s)?|forbidden)\b"
                r"[^\n]{0,100}(?:read|copy|query|change|access|touch|exfiltrat\w*|"
                r"leak|dump)\b[^\n]{0,80}"
                r"(?:credential|auth|agent\.db|token|session\s+material)",
                r"(?:never|do\s+not|don't|must\s+not|prohibit(?:ed|s)?|forbidden)\b"
                r"[^\n]{0,80}"
                r"(?:credential|auth\s+file|agent\.db|oauth|server\.token|"
                r"session\s+material)",
            ),
        ),
    ),
    (
        "write_scope",
        (
            (
                r"writes?\s+only\b",
                r"own\s+only\b",
                r"only\s+inside\b",
                r"exact\s+assigned\b",
                r"assigned\s+(?:file|files|path|paths|lane|scope)\b",
                r"stay\s+within[^\n]{0,60}assign",
            ),
        ),
    ),
    (
        "no_live_journal_queries",
        (
            (r"journal",),
            (
                r"(?:no|never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|"
                r"don't|must\s+not)\b[^\n]{0,60}\blive\b[^\n]{0,20}journal",
                r"(?:no|never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|"
                r"don't|must\s+not)\b[^\n]{0,60}journal\w*[^\n]{0,20}\blive\b",
                r"\blive\b[^\n]{0,20}journal\w*[^\n]{0,60}"
                r"(?:forbidden|prohibit(?:ed|s)?|banned|never|"
                r"not\s+permitt\w+|disallow\w+|barred)",
            ),
        ),
    ),
    (
        "no_tmp_probe_outputs",
        (
            (r"/tmp",),
            (
                r"(?:no|never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|"
                r"don't|must\s+not)\b[^\n]{0,60}/tmp[^\n]{0,60}"
                r"(?:probe|output|write|download|scratch)",
                r"/tmp[^\n]{0,60}(?:probe|output|write|download|scratch)"
                r"[^\n]{0,60}"
                r"(?:forbidden|prohibit(?:ed|s)?|banned|never|"
                r"not\s+permitt\w+|disallow\w+|barred)",
            ),
        ),
    ),
)

_CLAUSE_IDS = tuple(cid for cid, _ in _CLAUSES)

_COMPILED = tuple(
    (
        cid,
        tuple(
            tuple(re.compile(alt, re.IGNORECASE) for alt in group)
            for group in groups
        ),
    )
    for cid, groups in _CLAUSES
)


def _emit(payload, rc):
    sys.stdout.write(json.dumps(payload, sort_keys=True) + "\n")
    return rc


def _iter_contexts(node):
    """Yield every string value stored under a key literally named 'context'."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "context" and isinstance(value, str):
                yield value
            else:
                yield from _iter_contexts(value)
    elif isinstance(node, (list, tuple)):
        for value in node:
            yield from _iter_contexts(value)


def _missing_clauses(context):
    missing = []
    for cid, groups in _COMPILED:
        for group in groups:
            if not any(rx.search(context) for rx in group):
                missing.append(cid)
                break
    return missing


def _check_spec(spec_path):
    path = Path(spec_path)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return RC_SETUP, {
            "finding_id": "CONTEXT_SETUP",
            "reason": "spec_unreadable",
            "detail": "%s: %s" % (type(exc).__name__, exc),
            "claims_runtime_prevention": False,
            "static_only": True,
        }
    digest = hashlib.sha256(raw).hexdigest()
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return RC_SETUP, {
            "finding_id": "CONTEXT_SETUP",
            "reason": "spec_invalid_json",
            "detail": "%s: %s" % (type(exc).__name__, exc),
            "spec_sha256": digest,
            "claims_runtime_prevention": False,
            "static_only": True,
        }

    if isinstance(doc, str):
        contexts = [doc]
    else:
        contexts = list(_iter_contexts(doc))

    base = {
        "spec_sha256": digest,
        "contexts": len(contexts),
        "clauses_checked": len(_CLAUSE_IDS),
        "claims_runtime_prevention": False,
        "static_only": True,
    }

    if not contexts:
        base["finding_id"] = "CONTEXT_MISSING"
        base["context_absent"] = True
        base["missing"] = list(_CLAUSE_IDS)
        return RC_MISSING, base

    missing_union = []
    contexts_failing = 0
    for ctx in contexts:
        miss = _missing_clauses(ctx)
        if miss:
            contexts_failing += 1
            for cid in miss:
                if cid not in missing_union:
                    missing_union.append(cid)

    if missing_union:
        base["finding_id"] = "CONTEXT_MISSING"
        base["context_absent"] = False
        base["contexts_failing"] = contexts_failing
        base["missing"] = missing_union
        return RC_MISSING, base

    base["finding_id"] = "CONTEXT_OK"
    return RC_OK, base


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

_SELFTEST_PREAMBLE = (
    "Round gate coverage: acquire bounded journal observation. "
    "L1 MoriR16 holds canonical planner."
)

# Each fragment is authored to satisfy exactly its own clause and to feed no
# other clause's groups, so dropping one fragment must fail exactly that
# clause.
_SELFTEST_FRAGMENTS = (
    (
        "no_broadcast_exact_id",
        "Never agent://all; message ONLY exact seat id or L1 "
        "agent://MoriR16, never orchestrator.",
    ),
    (
        "lane_report_resolution",
        "Every Report: trailer path is relative to the repository root and "
        "must be written at the resolved report location.",
    ),
    (
        "no_verification_permission",
        "Skip all builds, tests, and gates; implementing a selftest is NOT "
        "permission to execute it.",
    ),
    (
        "pacman_pause",
        "ALL pacman transactions PAUSED host-wide.",
    ),
    (
        "credential_prohibition",
        "Never read, copy, query, or change credential/auth files or "
        "agent.db under any lane.",
    ),
    (
        "write_scope",
        "All writes ONLY inside your exact assigned file plus your report "
        "path.",
    ),
    (
        "no_live_journal_queries",
        "No live journalctl queries and no live journal reads of any kind.",
    ),
    (
        "no_tmp_probe_outputs",
        "Never use /tmp for deliberate probes, outputs, or downloads.",
    ),
)


def _selftest_context(drop=None):
    parts = [_SELFTEST_PREAMBLE]
    for cid, fragment in _SELFTEST_FRAGMENTS:
        if cid != drop:
            parts.append(fragment)
    return "\n".join(parts)


def _selftest_invoke(tool, spec_file, cwd):
    proc = subprocess.run(
        [sys.executable, str(tool), "--spec", str(spec_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd),
        timeout=60,
    )
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        payload = None
    return proc.returncode, payload, proc.stderr.decode("utf-8", "replace")


def _selftest():
    tool = Path(__file__).resolve()
    root = Path(tempfile.mkdtemp(prefix="mori-r16-ctxcheck-"))
    failures = []

    positive_ctx = _selftest_context()

    arms = []

    def add_spec_arm(name, doc, want_rc, want_id, want_missing=None,
                     forbid_missing=()):
        spec_file = root / ("%s.json" % name)
        if isinstance(doc, bytes):
            spec_file.write_bytes(doc)
        else:
            spec_file.write_text(json.dumps(doc), encoding="utf-8")
        arms.append(
            (name, spec_file, want_rc, want_id, want_missing, forbid_missing)
        )

    add_spec_arm(
        "positive",
        {"wave": "selftest", "context": positive_ctx},
        RC_OK, "CONTEXT_OK",
    )
    add_spec_arm(
        "positive-taskcall",
        {"taskCall": {"context": positive_ctx}},
        RC_OK, "CONTEXT_OK",
    )
    add_spec_arm(
        "positive-string-doc",
        positive_ctx,
        RC_OK, "CONTEXT_OK",
    )
    for cid, _fragment in _SELFTEST_FRAGMENTS:
        add_spec_arm(
            "drop-%s" % cid,
            {"context": _selftest_context(drop=cid)},
            RC_MISSING, "CONTEXT_MISSING",
            want_missing={cid},
            forbid_missing={x for x in _CLAUSE_IDS if x != cid},
        )
    add_spec_arm(
        "no-context-key",
        {"wave": "selftest", "items": []},
        RC_MISSING, "CONTEXT_MISSING",
        want_missing=set(_CLAUSE_IDS),
    )
    add_spec_arm(
        "partial-context-second",
        {
            "context": positive_ctx,
            "taskCall": {"context": _SELFTEST_PREAMBLE},
        },
        RC_MISSING, "CONTEXT_MISSING",
        want_missing=set(_CLAUSE_IDS),
    )
    add_spec_arm(
        "invalid-json",
        b'{ "context": ',
        RC_SETUP, "CONTEXT_SETUP",
    )

    # Missing file arm needs no written spec.
    arms.append(
        (
            "missing-file",
            root / "does-not-exist.json",
            RC_SETUP, "CONTEXT_SETUP", None, (),
        )
    )

    for name, spec_file, want_rc, want_id, want_missing, forbid_missing in arms:
        rc, payload, _stderr = _selftest_invoke(tool, spec_file, root)
        label = "arm %s" % name
        if rc != want_rc:
            failures.append("%s: rc=%d want=%d" % (label, rc, want_rc))
            continue
        if payload is None:
            failures.append("%s: stdout not a single JSON object" % label)
            continue
        if payload.get("finding_id") != want_id:
            failures.append(
                "%s: finding_id=%r want=%r"
                % (label, payload.get("finding_id"), want_id)
            )
        if payload.get("claims_runtime_prevention") is not False:
            failures.append(
                "%s: claims_runtime_prevention not false" % label
            )
        if want_missing is not None:
            missing = set(payload.get("missing") or [])
            if not want_missing.issubset(missing):
                failures.append(
                    "%s: missing=%r lacks %r"
                    % (label, sorted(missing), sorted(want_missing))
                )
            leaked = missing.intersection(forbid_missing)
            if leaked:
                failures.append(
                    "%s: unexpected missing clauses %r"
                    % (label, sorted(leaked))
                )

    if failures:
        return _emit(
            {
                "finding_id": "SELFTEST_FAIL",
                "failures": failures,
                "claims_runtime_prevention": False,
                "static_only": True,
            },
            RC_MISSING,
        )
    return _emit(
        {
            "finding_id": "SELFTEST_OK",
            "arms": len(arms),
            "claims_runtime_prevention": False,
            "static_only": True,
        },
        RC_OK,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="static gate: wave-spec context carries the round-16 "
        "contract restrictions (advisory; no runtime prevention)"
    )
    parser.add_argument("--spec", metavar="PATH",
                        help="wave spec JSON document to check")
    parser.add_argument("--selftest", action="store_true",
                        help="run isolated subprocess selftest; takes no "
                        "other flags")
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    if args.selftest:
        if args.spec:
            return _emit(
                {
                    "finding_id": "CONTEXT_SETUP",
                    "reason": "selftest_takes_no_spec",
                    "claims_runtime_prevention": False,
                    "static_only": True,
                },
                RC_SETUP,
            )
        return _selftest()
    if not args.spec:
        return _emit(
            {
                "finding_id": "CONTEXT_SETUP",
                "reason": "spec_required",
                "claims_runtime_prevention": False,
                "static_only": True,
            },
            RC_SETUP,
        )
    rc, payload = _check_spec(args.spec)
    return _emit(payload, rc)


if __name__ == "__main__":
    sys.exit(main())
