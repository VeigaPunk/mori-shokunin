#!/usr/bin/env python3
"""mori-round17-context-check.py — static gate for wave-spec contract context.

WHAT THIS GATE IS

  A small advisory text gate. It reads one wave spec document (--spec PATH),
  collects every string value stored under a key literally named ``context``
  (a top-level string document is itself the context), and requires that each
  collected context explicitly carries the round-17 contract restrictions.
  The round-16 restrictions are kept unchanged; round 17 adds four:

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

  Round-17 additions:

    no_fleet_root_writes        the context names the fleet root
                                (``/home/vgpnk/Projects/shokunin``, not the
                                lane path below it) AND forbids writing
                                there — naming alone or a bare write ban
                                does not satisfy the restriction
    no_background_jobs          the context names background jobs /
                                long-lived processes / host services AND
                                binds a prohibition to at least one of them
    no_vcs_mutation             the context names git and/or jj mutation
                                surfaces (``git add``, ``git commit``,
                                ``jj metaedit``, VCS mutation, ...) AND
                                forbids them; a mutating-command allowlist
                                without a prohibition does not satisfy it
    transcript_fields_only      transcript reads must be limited to named
                                record fields AND printing content /
                                errorMessage must be forbidden — the two
                                halves are separate groups, so a context
                                that only says "read transcripts" or only
                                says "never print secrets" fails

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
  touching credentials, writing to the fleet root, starting background
  jobs, mutating git/jj state, or printing transcript content. Output
  always carries "claims_runtime_prevention": false. It also does not
  detect a context that states a clause and then contradicts it; that is
  reviewer work, not this gate's.

OUTPUT DISCIPLINE

  stdout carries exactly one JSON object. Spec text is never echoed back —
  only clause identifiers, counts, and the spec SHA-256.

--selftest builds isolated spec documents under a fresh mkdtemp tree (the
caller's TMPDIR is honoured), runs this CLI as a real subprocess for a
positive, one negative per dropped clause, absent-context and
malformed-spec arms, and asserts exit code, finding_id, and missing-clause
identity. The four round-17 clauses also get near-miss arms (mention kept,
prohibition replaced by a permission) and single-line arms, because a
one-line context is where a plain same-line window would let the previous
sentence's ban bind to the next clause's mention. It never touches the
repository or network. Existence of --selftest is not permission to run it
during a wave.
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

# The fleet root itself, never the lane repository beneath it. A context that
# names only ``/home/vgpnk/Projects/shokunin/mori-shokunin`` has named the
# lane, not the fleet root.
_FLEET_ROOT = "/home/vgpnk/Projects/shokunin"


def _ss(n):
    """Same-line filler of at most n chars that cannot cross a sentence end.

    A bare ``[^\\n]{0,n}`` window lets a prohibition from the previous
    sentence bind to a mention in the next one — on a spec whose context is
    one long line (the round-17 spec is exactly that) a /tmp ban followed by
    "Background jobs are allowed" read as "background jobs are forbidden".
    Periods are still allowed when not followed by whitespace, so paths such
    as ``~/.omp`` and ``agent.db`` stay inside the window.
    """
    return r"(?:[^\n.]|\.(?=\S)){0,%d}" % n

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
    (
        "no_fleet_root_writes",
        (
            (
                r"fleet\s+root[^\n]{0,40}" + re.escape(_FLEET_ROOT)
                + r"(?!/mori)(?![\w-])",
                re.escape(_FLEET_ROOT) + r"(?!/mori)(?![\w-])"
                r"[^\n]{0,40}\bfleet\s+root\b",
            ),
            (
                r"(?:never|do\s+not|don't|must\s+not|forbidden|"
                r"prohibit(?:ed|s)?|banned|no)\b" + _ss(100) +
                r"(?:writ\w*|create|place|put|drop|emit)\b" + _ss(100) +
                r"(?:fleet\s+root\b|" + re.escape(_FLEET_ROOT) +
                r"(?!/mori)(?![\w-]))",
                r"fleet\s+root\b" + _ss(100) +
                r"(?:never|forbidden|prohibit(?:ed|s)?|banned|"
                r"no\s+writes?\b|misroot)",
            ),
        ),
    ),
    (
        "no_background_jobs",
        (
            (
                r"\bbackground\s+(?:jobs?|processes?)\b",
                r"\blong[- ]lived\s+(?:process|processes|jobs?|services?)\b",
                r"\bhost\s+services?\b",
            ),
            (
                r"(?:no|never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|"
                r"don't|must\s+not)\b" + _ss(60) +
                r"\bbackground\s+(?:jobs?|processes?)\b",
                r"\bbackground\s+(?:jobs?|processes?)\b" + _ss(60) +
                r"(?:forbidden|prohibit(?:ed|s)?|banned|never|"
                r"not\s+permitt\w+|disallow\w+|barred)",
                r"(?:no|never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|"
                r"don't|must\s+not)\b" + _ss(60) +
                r"\b(?:long[- ]lived\s+(?:process|processes|services?)|"
                r"host\s+services?)\b",
            ),
        ),
    ),
    (
        "no_vcs_mutation",
        (
            (
                r"\bgit\s+(?:add|commit|push|pull|reset|checkout|switch|"
                r"stash|rebase|merge|clean|tag|cherry-pick)\b",
                r"\bjj\s+(?:mutat\w*|metaedit|abandon|rebase|squash|"
                r"describe|commit|bookmark|new|edit|split|duplicate|"
                r"restore)\b",
                r"\bvcs\s+mutation\b",
                r"\bmutating\s+jj\b",
                r"\bgit/jj\s+writes?\b",
            ),
            (
                r"(?:no|never|forbidden|prohibit(?:ed|s)?|banned|do\s+not|"
                r"don't|must\s+not)\b" + _ss(80) +
                r"(?:git\s+(?:add|commit|push|pull|reset|checkout|switch|"
                r"stash|rebase)|jj\s+(?:mutat\w*|metaedit|abandon|rebase|"
                r"squash|commit)|mutating\s+jj|vcs\s+mutation)",
                r"(?:git\s+add/commit|mutating\s+jj\s+command|"
                r"vcs\s+mutation)" + _ss(80) +
                r"(?:never|forbidden|prohibit(?:ed|s)?|banned|"
                r"not\s+permitt\w+)",
                r"\bno\s+vcs\s+mutation\b",
            ),
        ),
    ),
    (
        "transcript_fields_only",
        (
            (
                r"\btranscripts?\b[^\n]{0,80}\bread\s+only\b[^\n]{0,80}"
                r"\bfields?\b",
                r"\bread\s+only\s+(?:the\s+)?(?:record\s+)?fields?\b",
                r"\bfield[- ]limited\b",
                r"\blimited\s+to\s+(?:the\s+)?(?:named\s+|listed\s+|"
                r"same\s+)?fields?\b",
                r"\bonly\s+(?:the\s+)?(?:record\s+)?fields?\b[^\n]{0,80}"
                r"\b(?:type|customType|message\.)",
            ),
            (
                r"(?:never|do\s+not|don't|must\s+not|forbidden|"
                r"prohibit(?:ed|s)?|banned)\b" + _ss(80) +
                r"(?:print|emit|echo|reveal|leak|dump|copy)\b" + _ss(80) +
                r"\b(?:content|errorMessage)\b",
                r"\b(?:content|errorMessage)\b" + _ss(40) +
                r"(?:never|forbidden|prohibit(?:ed|s)?|banned)",
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
        "clause_ids": list(_CLAUSE_IDS),
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
    "L1 MoriR17 holds canonical planner."
)

# Each fragment is authored to satisfy exactly its own clause and to feed no
# other clause's groups, so dropping one fragment must fail exactly that
# clause.
_SELFTEST_FRAGMENTS = (
    (
        "no_broadcast_exact_id",
        "Never agent://all; message ONLY exact seat id or L1 "
        "agent://MoriR17, never orchestrator.",
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
    (
        "no_fleet_root_writes",
        "The fleet root is /home/vgpnk/Projects/shokunin; never write "
        "anything under the fleet root.",
    ),
    (
        "no_background_jobs",
        "No background jobs, no long-lived processes, and no host services "
        "of any kind.",
    ),
    (
        "no_vcs_mutation",
        "No VCS mutation anywhere: never run git add, git commit, git push, "
        "or a mutating jj command in the lane or your clone.",
    ),
    (
        "transcript_fields_only",
        "Session transcript reads are field-limited to the named record "
        "fields; never print content, errorMessage text, usage or any other "
        "field.",
    ),
)

# Near-miss fragments for the round-17 clauses: each KEEPS the clause's
# mention half and replaces its prohibition half with a permission. A clause
# whose groups collapsed into one loose pattern would accept these, so the
# arm asserts the clause still reports missing.
_SELFTEST_NEAR_MISS = {
    "no_fleet_root_writes": (
        "The fleet root is /home/vgpnk/Projects/shokunin and seats may "
        "write scratch wherever they like."
    ),
    "no_background_jobs": (
        "Background jobs are permitted for long scans, and host services "
        "may run."
    ),
    "no_vcs_mutation": (
        "Git add, git commit and jj metaedit are permitted inside your "
        "clone."
    ),
    "transcript_fields_only": (
        "Session transcript reads are field-limited to the named record "
        "fields, and content may be printed freely."
    ),
}

_ECHO_SENTINEL = "SPEC-ECHO-SENTINEL-9f3c2b7a"


def _selftest_context(drop=None):
    parts = [_SELFTEST_PREAMBLE]
    for cid, fragment in _SELFTEST_FRAGMENTS:
        if cid != drop:
            parts.append(fragment)
    return "\n".join(parts)


def _selftest_context_replaced(cid, replacement):
    parts = [_SELFTEST_PREAMBLE]
    for frag_cid, fragment in _SELFTEST_FRAGMENTS:
        parts.append(replacement if frag_cid == cid else fragment)
    return "\n".join(parts)


def _selftest_context_single_line(near_miss_cid=None):
    """Same context on ONE line — the shape of the real round-17 spec.

    On a one-line context a prohibition from a previous sentence sits within
    any ``[^\\n]{0,n}`` window of the next clause's mention, so this arm is
    what catches cross-sentence leakage in the round-17 prohibition groups.
    """
    parts = [_SELFTEST_PREAMBLE]
    for cid, fragment in _SELFTEST_FRAGMENTS:
        parts.append(_SELFTEST_NEAR_MISS[cid] if cid == near_miss_cid
                     else fragment)
    return " ".join(parts)


def _selftest_invoke(tool, spec_file, cwd):
    proc = subprocess.run(
        [sys.executable, str(tool), "--spec", str(spec_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd),
        timeout=60,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "replace"),
        proc.stderr.decode("utf-8", "replace"),
    )


def _selftest():
    tool = Path(__file__).resolve()
    root = Path(tempfile.mkdtemp(prefix="mori-r17-ctxcheck-"))
    failures = []

    positive_ctx = _selftest_context()

    arms = []

    def add_spec_arm(name, doc, want_rc, want_id, want_missing=None,
                     forbid_missing=(), forbid_stdout=()):
        spec_file = root / ("%s.json" % name)
        if isinstance(doc, bytes):
            spec_file.write_bytes(doc)
        else:
            spec_file.write_text(json.dumps(doc), encoding="utf-8")
        arms.append(
            (
                name, spec_file, want_rc, want_id, want_missing,
                forbid_missing, forbid_stdout,
            )
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
    for cid, replacement in _SELFTEST_NEAR_MISS.items():
        add_spec_arm(
            "near-miss-%s" % cid,
            {"context": _selftest_context_replaced(cid, replacement)},
            RC_MISSING, "CONTEXT_MISSING",
            want_missing={cid},
            forbid_missing={x for x in _CLAUSE_IDS if x != cid},
        )
    add_spec_arm(
        "positive-single-line",
        {"context": _selftest_context_single_line()},
        RC_OK, "CONTEXT_OK",
    )
    for cid, replacement in _SELFTEST_NEAR_MISS.items():
        add_spec_arm(
            "single-line-near-miss-%s" % cid,
            {"context": _selftest_context_single_line(near_miss_cid=cid)},
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
        "no-spec-echo",
        {"context": positive_ctx + "\n" + _ECHO_SENTINEL},
        RC_OK, "CONTEXT_OK",
        forbid_stdout=(_ECHO_SENTINEL,),
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
            RC_SETUP, "CONTEXT_SETUP", None, (), (),
        )
    )

    for (name, spec_file, want_rc, want_id, want_missing, forbid_missing,
         forbid_stdout) in arms:
        rc, stdout, _stderr = _selftest_invoke(tool, spec_file, root)
        label = "arm %s" % name
        if rc != want_rc:
            failures.append("%s: rc=%d want=%d" % (label, rc, want_rc))
            continue
        try:
            payload = json.loads(stdout)
        except ValueError:
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
        if want_rc != RC_SETUP and payload.get("clauses_checked") != len(_CLAUSE_IDS):
            failures.append(
                "%s: clauses_checked=%r want=%d"
                % (label, payload.get("clauses_checked"), len(_CLAUSE_IDS))
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
        for token in forbid_stdout:
            if token in stdout:
                failures.append("%s: stdout echoed spec text" % label)

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
            "clauses_checked": len(_CLAUSE_IDS),
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
        description="static gate: wave-spec context carries the round-17 "
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
