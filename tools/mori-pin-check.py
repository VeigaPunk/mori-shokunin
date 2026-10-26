#!/usr/bin/env python3
"""mori-pin-check — re-measure the self-test pins of SKILL.md's gate registry.

Round 47 (C1, calibration). Replaces round 46's row-wide substring counter
(`count-repins.py`), which turned green when a stale receipt string was moved
to another cell of the same row (`corpus/lessons/round-46.md` M1;
`corpus/lessons/round-46-verifier-spotcheck.md` routed defect 1).

v2 (round 47, after wave-1 seats CritC1Predicate and SentPinExec turned the
frozen v1 — freeze `63eecf27`, sha256 `e3ef425a…` — green on junk edits):
bound commands are restricted, a pin's command may not change from the
baseline, the pinned text must equal the observed text, rows are unique, a
short row naming `selftest` in any case is unparsed, and digest paths stay
inside the measured tree. The round-47 claim P-C1 is scored with the frozen
v1 bytes; v2 is the lane's standing tool.

v3 (round 48, wave w1): adds, per the v3-spec R1-R8: case-insensitive
header recognition (`self-test` | `selftest` | `self test`); hidden-row
accounting (a row-shaped line outside a parsed self-test table — including
inside fences — carrying an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token or the text
`--selftest` is `hidden`, fatal); ASCII-strict span checks (a span whose first
token is non-ASCII, or whose first token casefolds to a tally-prefix shape, or
that carries an ASCII tally token not at its start, is `unparsed`); rebound by
instrument prefix (a row using a baseline prefix with an argv outside that
prefix's baseline set); line-count pins (`(\\d+) lines` binds to the nearest
preceding path in the same cell that resolves inside the tree); truncated-digest
pins (`hex{8,63}…` must prefix the sha256 of that same nearest preceding in-tree
path); setup failures exit 2 with one line, never a traceback. Also, after the
wave-1 critic `CritJunkClasses`: full digests bind to the nearest preceding
in-tree path of their own cell (R10, a decoy file named elsewhere in the row no
longer matches); a tally-looking token in another cell of a parsed row, or on a
continuation line directly under a row, is `hidden` (R9a/R9b); a tally written
outside backticks in a self-test cell is `unparsed` (R9c).

R11 (round-48 wave-2 proposal, `w2/R48ExecD7.md`, closes D7): a tally pin's
bound argv must run the row's claimed instrument — the first file path named in
the row's entry cell — or a mutant of it: a path with a `fixtures` or `mutants`
directory segment whose basename equals the claimed instrument's basename (the
lane's `fixtures/mutants/<basename>` convention, SKILL.md:185). Any other
instrument is `misattributed` (fatal). A row that claims instrument A in its
entry cell while its self-test cell runs instrument B is no longer green.

v4 (round 49, scored by the opaque-handle counter `.ufo/waves/round-49/count-c1.py`): a row is what a reader
sees. F1 — R9b's "directly under a row" is the nearest preceding non-blank line; F2 — the self-test header
(and F5's `verdict map` column) is matched after NFKC and zero-width deletion; F3 — any indentation (spaces
or a tab) is a row shape for the hidden scan; F4 — `<tr`/`<td` HTML markup is a row shape too; F5 — two rows
binding one `(prefix, argv)` must agree on their stated exit-code → outcome contract, else `duplicate`; K2 — a
leading `VAR=value` word is applied, and an unexpandable value is `env_unexpanded`; K8 — a PASS-form pin is
checked against the exit code; K5 — a `C1/C2/C3_SELFTEST` namespace join is limited to the instrument's own
family; X1 — a baseline binding that disappears is a `no_command` finding, never a traceback. Round-48 classes
K3, K6 and K7 are R12-R14 below; K4 (pins outside the self-test cell) stays open, and a row's claimed instrument
is compared by path only (a fixtures/mutants carve-out keeps three landed rows green). The self-test pin
`PIN_CHECK_SELFTEST pass=N` lives in SKILL.md row `registry pin reconciler (r47, C1)`.

R12-R14 (round 49, wave 1 — closes the round-48 wave-2 classes K3, K6 and K7 of
`w2/R48CritV3Junk2.md`; no new required flag, every rule is on by default):
  R12 (K3) the presence counter in `pin_keys` reads every pin kind a row can
  carry — a tally prefix, a digest, and a line count — not just tally prefixes
  and full digests. A full 64-hex digest and a truncated `<hex>…` digest are one
  kind (`digest`), so repairing a truncated pin to a full one is not a deletion,
  while deleting either one is `dropped` against `--baseline-rev`.
  R13 (K6) a measured tree that ships this instrument (`tools/mori-pin-check.py`)
  must pin it: at least one tally pin's bound argv must run that path, else
  `dropped`. The registry floor cannot see the row that pins the reconciler,
  because that row is new since the baseline.
  R14 (K7) a line-count pin must bind the instrument the row runs: its nearest
  preceding in-tree path must be a bound argv path of one of the row's tally
  pins, or the row's claimed entry path. A decoy path in the same cell is
  `mismatch` even when the count is true of the decoy.

What it reads
  Every Markdown table in SKILL.md whose header row has a cell named
  `self-test`. Cells are split on unescaped `|`; a data row whose cell count
  differs from its header's and that names `selftest` (any case) is
  `unparsed`; two parsed rows with one name are `duplicate`.
  Only the self-test cell is read for pins (the semantic cell):
    tally pin  — a backticked span that starts with `<PREFIX>SELFTEST`
                 (PREFIX = [A-Z0-9_]*), e.g. `C1_SELFTEST pass=16 fail=0`,
                 `X_SELFTEST: PASS (6 cases)`, `X_SELFTEST: PASS 12/12`.
                 The text after the prefix must carry a digit, else `unparsed`.
    digest pin — a full 64-hex token in the self-test cell; it must equal the
                 sha256 of at least one file path named anywhere in the row
                 that resolves inside the measured tree.

How it measures
  Each tally pin binds to the nearest preceding executable span in the same
  self-test cell: a span containing `--selftest` that starts with an
  interpreter (`python3`, `bash`, `sh`; leading `VAR=value` words are the
  environment the row writes and are applied — K2), or a bare `.py`/`.sh`
  path (e.g. a named mutant), run as
  `<interpreter> <path> --selftest`. A bound argv must be exactly
  `<python3|python|bash|sh> [-I] [-B] <path> [<rev>] --selftest` with
  `<path>` under `tools/` or `.ufo/waves/round-N/`, no `..`, no `.scratch/`;
  anything else (inline `-c` code, extra arguments) binds nothing.
  If the span is the bare `--selftest`,
  the command is the entry cell's first backticked span cut at its first `[`
  or `-` word, `<rev>`/`<REV>`/`<revision>` replaced by the measured
  revision, plus `--selftest`. No preceding span → `no_command`.
  The command runs (no shell) in the measured tree with TMPDIR set to a fresh
  directory under `<measured tree>/.scratch` (lane tools refuse a TMPDIR
  outside their own lane root); a leading `VAR=value` word of the span (or of
  the entry cell, for the bare `--selftest` form) is applied to the child's
  environment, `$PWD` meaning the measured root as a shell would mean it — an
  assignment that cannot be reproduced without a shell (`${OTHER}`, `~`,
  backticks, `<placeholder>`) is `env_unexpanded` (fatal, never silently
  dropped). The output lines that START with the prefix
  must all carry one text after it, that text must equal the pinned text
  exactly, and the exit code must be 0 unless the pinned text itself asserts a
  nonzero `fail=N` (a PASS-form pin such as `: PASS 12/12` claims success and
  is exit-checked — K8). Lines inside
  ``` / ~~~ fences are not read; the entry column is found by its header name.

Modes
  --rev REV [--repo DIR]   export REV with `git archive` and measure it there
                           (SKILL.md read from REV unless --skill is given)
  --root DIR               measure DIR as-is (selftest and fixtures)
  --skill PATH             read the registry from PATH instead
  --min-tally-pins N       floor on tally pins found (a deleted pin is not a fix)
  --baseline-rev REV       every (row name, pin prefix | sha256) key present in
                           SKILL.md at REV must still be present (`dropped=0`),
                           and each pin's bound argv must equal its argv at REV
                           (`rebound=0`); rows new since REV are not compared.

Output: one `pin line=… kind=… prefix=… state=… …` line per pin, then
  `PIN_CHECK=met|unmet tally_pins=N digest_pins=N mismatches=N unparsed=N
  no_command=N dropped=N rebound=N duplicate=N hidden=N misattributed=N
  env_unexpanded=N min_tally_pins=N rev=… baseline=yes|no`
Exit: 0 met · 1 unmet · 2 setup (usage, unresolvable revision, unreadable SKILL).
Read-only over committed bytes: with --rev it writes only its own export
under `<repo>/.scratch` (removed on exit); with --root it writes temp dirs
under `<root>/.scratch`. `--selftest` builds synthetic trees under TMPDIR.
"""
import argparse
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unicodedata

TIMEOUT_S = 600
HEX_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
PATH_RE = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.(?:py|sh|json|md|txt|tsv)")
SPAN_RE = re.compile(r"`([^`]*)`")
REV_WORDS = ("<rev>", "<REV>", "<revision>", "REV")
INTERPRETERS = ("python3", "python", "bash", "sh")
# v2 (round 47, after w1 CritC1Predicate/SentPinExec): a bound command must run a
# registered instrument path — `tools/…` or `.ufo/waves/round-N/…` — never `.scratch/`,
# never `..`, never inline code (`-c`), and carry no argument beyond an optional
# revision and `--selftest`.
SAFE_PATH = re.compile(r"(?:tools|\.ufo/waves/round-[0-9]+)/[A-Za-z0-9_./-]+\.(?:py|sh)")
PY_FLAGS = ("-I", "-B")

HEADER_CELLS = ("self-test", "selftest", "self test")
HIDDEN_TOKEN_RE = re.compile(r"[A-Z][A-Z0-9_]*SELFTEST")
TRUNC_DIGEST_RE = re.compile(r"[0-9a-f]{8,63}\u2026")
TALLY_PIN_RE = re.compile(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", re.S)
PINLIKE_T0_RE = re.compile(r"[A-Z][A-Z0-9_]*SELFTEST", re.I)
LINE_COUNT_RE = re.compile(r"(\d+) lines")
# R13 (round-49 K6): the instrument this file is registered as (SKILL.md's entry
# cell for its row). A tree that ships it must pin it; `check(..., self_instrument=…)`
# lets the selftest prove both directions without touching the registry.
SELF_INSTRUMENT = "tools/mori-pin-check.py"


TALLY_TEXT_RE = re.compile(r"[A-Z][A-Z0-9_]*SELFTEST[:=]?\s*(?:pass=\d+|PASS)")


def argv_ok(argv, rev):
    if not argv or argv[0] not in INTERPRETERS:
        return False
    i = 1
    while i < len(argv) and argv[0].startswith("python") and argv[i] in PY_FLAGS:
        i += 1
    if i >= len(argv):
        return False
    path = argv[i]
    if (not SAFE_PATH.fullmatch(path) or ".." in path.split("/")
            or "/.scratch/" in "/" + path):
        return False
    rest = argv[i + 1:]
    return rest == ["--selftest"] or (rev is not None and rest == [rev, "--selftest"])


def split_cells(line):
    """Split a GFM table row on unescaped `|`: a pipe is a separator unless an odd number of
    backslashes precedes it (`\\|` stays in the cell; `\\\\|` is a literal backslash and a
    real separator — v2's one-character lookbehind mis-split such rows, round-47 L2)."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    parts, cur = [], []
    for i, c in enumerate(s):
        if c == "|":
            j, bs = i - 1, 0
            while j >= 0 and s[j] == "\\":
                bs += 1
                j -= 1
            if bs % 2 == 0:
                parts.append("".join(cur))
                cur = []
                continue
        cur.append(c)
    parts.append("".join(cur))
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def is_separator(cells):
    return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells) if cells else False


def _header_key(cell):
    """A header cell as a reader sees it: NFKC, zero-width characters removed, case folded (F2).
    The verdict-map column of the exit-contract rule (F5) is looked up the same way, so a
    non-breaking space in `verdict map` cannot hide the column (round-49 Mo49ExecImplA D1)."""
    return (unicodedata.normalize("NFKC", cell)
            .replace("\u200b", "").replace("\u200c", "")
            .replace("\u200d", "").replace("\ufeff", "").lower())


def scan_lines(text):
    """Classify every line of SKILL.md — one tokenizer pass shared by header
    recognition (R1), row parsing and hidden-row accounting (R2).

    Kinds: fence_open/fence_close/fence_body (inside ``` / ~~~ blocks),
    header (row with a recognised self-test header cell), separator,
    row (data row of a parsed self-test table), candidate (row-shaped
    line outside any parsed self-test table), other."""
    lines = text.split("\n")
    header = None
    fence = None
    for n, line in enumerate(lines, 1):
        mark = line.lstrip()[:3]
        if mark in ("```", "~~~"):
            if fence == mark:
                fence = None
                header = None
                yield n, "fence_close", {"raw": line}
            else:
                fence = fence or mark
                yield n, "fence_open", {"raw": line}
            continue
        if fence:
            yield n, "fence_body", {"raw": line}
            continue
        cells = split_cells(line)
        if cells is None:
            header = None
            yield n, "other", {"raw": line}
            continue
        low = [_header_key(c) for c in cells]
        if any(c in HEADER_CELLS for c in low):
            idx = next(i for i, c in enumerate(low) if c in HEADER_CELLS)
            eidx = low.index("entry") if "entry" in low else 2
            header = (cells, idx, eidx)
            yield n, "header", {"raw": line, "cells": cells, "idx": idx,
                                 "eidx": eidx}
            continue
        if header is None:
            yield n, "candidate", {"raw": line, "cells": cells}
            continue
        if is_separator(cells):
            yield n, "separator", {"raw": line, "cells": cells}
            continue
        nxt = split_cells(lines[n]) if n < len(lines) else None
        if nxt is not None and is_separator(nxt):
            header = None
            yield n, "candidate", {"raw": line, "cells": cells}
            continue
        yield n, "row", {"raw": line, "cells": cells, "header": header[0],
                         "idx": header[1], "eidx": header[2]}


def parse_registry(text):
    """Rows of every self-test table: line, cells, header, idx (self-test),
    eidx (entry), state ('ok'|'unparsed'). Built from scan_lines; lines inside
    ``` / ~~~ fences are ignored, and a row followed by a separator row starts
    a new table."""
    rows = []
    for n, kind, payload in scan_lines(text):
        if kind != "row":
            continue
        state = "ok" if len(payload["cells"]) == len(payload["header"]) else "unparsed"
        rows.append({"line": n, "cells": payload["cells"], "header": payload["header"],
                     "idx": payload["idx"], "eidx": payload["eidx"], "state": state,
                     "raw": payload["raw"]})
    return rows


def hidden_rows(text):
    """R2 + R9: pins that a checker would not see are `hidden` (fatal):
    (R2) row-shaped lines (up to three leading spaces, then `|`) outside a parsed
    self-test table — including lines inside fences — carrying an ASCII
    `[A-Z][A-Z0-9_]*SELFTEST` token or the text `--selftest`;
    (R9a, CritJunkClasses D5) a tally-looking token in a cell of a parsed row other
    than its self-test cell;
    (R9b, D2) a continuation line, directly under a table row and not itself a row,
    carrying a tally-looking token or `--selftest`."""
    found = []
    prev_raw = ""
    for n, kind, payload in scan_lines(text):
        raw = payload["raw"]
        row_shaped = bool(re.match(r"^\s*\|", raw))
        html_row = bool(re.match(r"^\s*<t[rd][\s>]", raw, re.I))
        if kind in ("candidate", "fence_body", "other") and (row_shaped or html_row):
            if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:
                found.append((n, raw))
        elif kind == "row" and len(payload["cells"]) == len(payload["header"]):
            for ci, c in enumerate(payload["cells"]):
                if ci != payload["idx"] and TALLY_TEXT_RE.search(c):
                    found.append((n, raw))
                    break
        elif kind == "other" and re.match(r"^\s*\|", prev_raw):
            if TALLY_TEXT_RE.search(raw) or "--selftest" in raw:
                found.append((n, raw))
        if raw.strip():
            prev_raw = raw
    return found


def inside_tree(root, path):
    rel = os.path.normpath(path)
    if os.path.isabs(rel) or rel == ".." or rel.startswith(".." + os.sep):
        return False
    fp = os.path.join(root, rel)
    return (os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)
            and os.path.isfile(fp))


def instrument_of(argv):
    """R11: the file path a bound argv runs — the word after the interpreter and
    its flags."""
    i = 1
    while i < len(argv) and argv[0].startswith("python") and argv[i] in PY_FLAGS:
        i += 1
    return argv[i] if i < len(argv) else None


def mutant_of(path, claimed):
    """R11 carve-out: `path` is a mutant of `claimed` — under a `fixtures` or
    `mutants` directory and carrying the claimed instrument's basename (the lane's
    `fixtures/mutants/<basename>` convention, SKILL.md:185)."""
    if not path or not claimed:
        return False
    segs = path.split("/")
    return (("fixtures" in segs or "mutants" in segs)
            and os.path.basename(path) == os.path.basename(claimed))


def span_kind(span, cells, rev, eidx):
    """Classify one backticked span of a self-test cell (R3, R7 L4):
    ('tally'|'digest'|'trunc'|'command'|'unparsed'/reason|'ignore')."""
    if HEX_RE.search(span):
        return "digest", None
    if TRUNC_DIGEST_RE.search(span):
        return "trunc", None
    if TALLY_PIN_RE.match(span):
        return "tally", None
    if command_from_span(span, cells, rev, eidx) is not None:
        return "command", None
    tok0 = span.split()[0] if span.split() else ""
    if any(ord(c) > 127 for c in tok0):
        return "unparsed", "non-ascii-token"
    if PINLIKE_T0_RE.fullmatch(unicodedata.normalize("NFKC", tok0)):
        return "unparsed", "casefold-selftest-prefix"
    if HIDDEN_TOKEN_RE.search(span):
        return "unparsed", "token-not-at-span-start"
    return "ignore", None


def _nearest_in_tree_path(prefix, root):
    for pm in reversed(list(PATH_RE.finditer(prefix))):
        if inside_tree(root, pm.group(0)):
            return pm.group(0)
    return None


def line_count_pins(st, root, allowed=None):
    """R5: `(\\d+) lines` binds to the nearest preceding path in the same cell
    that resolves to an in-tree file.

    R14 (round-49 K7): a line count is true of one file, and the row's file is the
    instrument it runs — the nearest preceding path must be in `allowed` (the
    row's bound argv paths plus its claimed entry path), so a decoy path in the
    same cell is `mismatch`. `allowed=None` measures R5 alone.
    Returns [(num, relpath_or_None, bound_ok)]."""
    out = []
    for m in LINE_COUNT_RE.finditer(st):
        p = _nearest_in_tree_path(st[:m.start()], root)
        out.append((int(m.group(1)), p,
                    allowed is None or (p is not None and p in allowed)))
    return out


def trunc_digest_pins(st, raw, root):
    """R6/R10: `[0-9a-f]{8,63}…` must be a prefix of the sha256 of the nearest
    preceding in-tree path of the same cell; returns [(prefix, relpath|None)]."""
    pins = []
    for m in TRUNC_DIGEST_RE.finditer(st):
        pfx = m.group(0)[:-1]
        p = _nearest_in_tree_path(st[:m.start()], root)
        hit = p if p is not None and sha256_file(os.path.join(root, p)).startswith(pfx) else None
        pins.append((pfx, hit))
    return pins


def command_from_span(span, cells, rev, eidx=2):
    """Return (argv, env) for one backticked self-test-cell span, or None (v2: only
    argv that passes argv_ok); env is the leading `VAR=value` environment (K2)."""
    if "--selftest" not in span:
        argv = None
        if re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.py", span):
            argv = ["python3", span, "--selftest"]
        elif re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.sh", span):
            argv = ["bash", span, "--selftest"]
        return (argv, {}) if argv is not None and argv_ok(argv, rev) else None
    got = derive_command(span, cells, rev, eidx)
    if got is None:
        return None
    argv, env = got
    return (argv, env) if argv_ok(argv, rev) else None


def pin_commands(cells, idx, rev, eidx=2):
    """Bind each tally pin in the self-test cell to the nearest preceding
    executable span: a `--selftest` command, or a bare `.py`/`.sh` path (a
    mutant named after the main command is run as `<interp> <path> --selftest`).
    Each binding is (prefix, pinned text, argv|None, env)."""
    st = cells[idx]
    bound = []
    current, current_env = None, {}
    for m in SPAN_RE.finditer(st):
        span = m.group(1)
        pm = re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span, re.S)
        if pm:
            bound.append((pm.group(1), pm.group(2), current, current_env))
            continue
        got = command_from_span(span, cells, rev, eidx)
        if got is not None:
            current, current_env = got
    return bound


def split_env(words):
    """K2 (round-48 w2 R48CritV3Junk2): a leading `VAR=value` word sequence is the
    environment the row writes, not decoration to be dropped — dropping it ran a
    command the row never wrote. Returns ({VAR: value}, argv)."""
    env = {}
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):
        key, _, val = words.pop(0).partition("=")
        env[key] = val
    return env, words


def resolve_env(env, root):
    """K2: the assignments as the child must see them. `$PWD`/`${PWD}` is the one
    variable this runner defines (the measured root, which is also the command's
    cwd, so it means what a shell would mean). Any other shell reference or an
    angle-bracket placeholder cannot be reproduced without a shell; returns
    ({}, name) so the pin is reported `env_unexpanded` (fatal) instead of a
    different command than the row writes being run and called a match."""
    out = {}
    for key, val in env.items():
        val = re.sub(r"\$\{PWD\}|\$PWD(?![A-Za-z0-9_])", lambda _m: root, val)
        if re.search(r"[$`~]|<[^>]*>", val):
            return {}, key
        out[key] = val
    return out, None


def norm_cmd(words, env, rev):
    """Comparable form of a pinned command: its assignments, then argv with the
    measured revision collapsed to `<REV>` (a change of either is a rebound)."""
    if words is None:
        return None
    return tuple(["%s=%s" % (k, env[k]) for k in sorted(env)]
                 + ["<REV>" if w == rev else w for w in words])


def render_cmd(words, env):
    return " ".join(["%s=%s" % (k, env[k]) for k in sorted(env)] + list(words))


def derive_command(span, cells, rev, eidx=2):
    """(argv, env) for a span containing `--selftest`; the bare flag borrows the
    entry cell (its leading assignments included — K2)."""
    try:
        env, words = split_env(shlex.split(span))
    except ValueError:
        return None
    if words and words[0] in INTERPRETERS:
        return words, env
    if span.strip() != "--selftest":
        return None
    entry_spans = SPAN_RE.findall(cells[eidx] if len(cells) > eidx else "")
    if not entry_spans:
        return None
    ewords = []
    try:
        entry_words = shlex.split(entry_spans[0].replace("\\|", "|"))
    except ValueError:
        return None
    for w in entry_words:
        if w.startswith("[") or w.startswith("-"):
            break
        ewords.append(rev if (w in REV_WORDS and rev) else w)
    penv, ewords = split_env(ewords)
    if not ewords or ewords[0] not in INTERPRETERS or any(w.startswith("<") for w in ewords):
        return None
    return ewords + ["--selftest"], penv


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(words, root, scratch, timeout, extra_env=None):
    # TMPDIR lives inside the measured tree (<root>/.scratch): lane tools such as
    # mori-round19-regressions.py refuse a TMPDIR outside their own lane root.
    tmp_parent = os.path.join(root, ".scratch")
    os.makedirs(tmp_parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="pin-tmp-", dir=tmp_parent)
    env = dict(os.environ, TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")
    if extra_env:
        # K2: the assignments the bound span writes are applied, so the run is the
        # command the row writes (a row TMPDIR wins over the private one).
        env.update(extra_env)
    try:
        proc = subprocess.run(words, cwd=root, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout)
        return proc.returncode, proc.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return None, "timeout"
    except OSError as exc:
        return None, "oserror: %s" % exc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def pin_keys(text):
    """Multiset {(row name, pin kind): count} over parsed rows — no commands run.

    R12 (round-49 K3): every pin kind a row can carry is counted, so a *deleted*
    pin is `dropped` against the baseline instead of vanishing. A full 64-hex
    digest and a truncated `<hex>…` digest are one kind (`digest`): the baseline's
    stale truncated pin repaired to a full digest is a repair, not a deletion."""
    keys = {}
    for row in parse_registry(text):
        if row["state"] != "ok":
            continue
        st = row["cells"][row["idx"]]
        name = row["cells"][0]
        for m in SPAN_RE.finditer(st):
            pm = re.match(r"([A-Z][A-Z0-9_]*SELFTEST)", m.group(1))
            if pm:
                k = (name, pm.group(1))
                keys[k] = keys.get(k, 0) + 1
        n_digest = len(HEX_RE.findall(st)) + len(TRUNC_DIGEST_RE.findall(st))
        if n_digest:
            k = (name, "digest")
            keys[k] = keys.get(k, 0) + n_digest
        n_lines = len(LINE_COUNT_RE.findall(st))
        if n_lines:
            k = (name, "lines")
            keys[k] = keys.get(k, 0) + n_lines
    return keys

def pin_bindings(text, rev):
    """{(row name, prefix, ordinal): bound argv with the revision as `<REV>`}."""
    out = {}
    for row in parse_registry(text):
        if row["state"] != "ok":
            continue
        seen = {}
        for prefix, _pinned, words, penv in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
            n = seen.get(prefix, 0)
            seen[prefix] = n + 1
            out[(row["cells"][0], prefix, n)] = norm_cmd(words, penv, rev)
    return out


def check(text, root, scratch, rev, timeout, min_tally, baseline_text=None,
          self_instrument=SELF_INSTRUMENT):
    out = []
    counts = {"tally_pins": 0, "digest_pins": 0, "mismatches": 0,
              "unparsed": 0, "no_command": 0, "dropped": 0, "rebound": 0,
              "duplicate": 0, "hidden": 0, "misattributed": 0, "env_unexpanded": 0}
    base_bind = {}
    base_bind_prefix = {}
    if baseline_text is not None:
        now = pin_keys(text)
        for k, n in sorted(pin_keys(baseline_text).items()):
            gone = n - now.get(k, 0)
            if gone > 0:
                counts["dropped"] += gone
                out.append("pin kind=baseline state=dropped row=%r pin=%s count=%d" % (k[0], k[1], gone))
        # R4: keep the v2 per-key binding for existing rows, and record the
        # baseline prefix → set of bound argv (any row) for new rows. A new row
        # that binds a prefix whose baseline bindings name exactly one distinct
        # argv (a single canonical instrument) is `rebound` when its argv is not
        # in that set (a prefix already shared by several instruments is a
        # namespace; new genuine instruments may join it).
        base_bind = pin_bindings(baseline_text, "<REV>")
        # A literal `<REV>` word is rejected by derive_command, so re-resolve the
        # baseline bindings with a placeholder revision and normalise it back to
        # `<REV>` so the sets stay comparable with the current text.
        _REV_PLACEHOLDER = "__REV__"
        for (_name, prefix, _ordinal), norm in pin_bindings(baseline_text, _REV_PLACEHOLDER).items():
            if norm is not None:
                norm = tuple("<REV>" if w == _REV_PLACEHOLDER else w for w in norm)
                base_bind_prefix.setdefault(prefix, set()).add(norm)
    names = {}
    for row in parse_registry(text):
        if row["state"] == "ok":
            names[row["cells"][0]] = names.get(row["cells"][0], 0) + 1
    for name, n in sorted(names.items()):
        if n > 1:
            counts["duplicate"] += n - 1
            out.append("pin kind=row state=duplicate row=%r count=%d" % (name, n))
    # R11 (round-48 w2 CritV3Junk1): two rows binding one (prefix, argv) are two
    # authorities for one command; their exit-code contracts must agree.
    contracts = {}
    for row in parse_registry(text):
        if row["state"] != "ok":
            continue
        try:
            vi = [_header_key(c) for c in row["header"]].index("verdict map")
        except ValueError:
            continue
        vmap = row["cells"][vi] if len(row["cells"]) > vi else ""
        pairs = {int(m.group(1)): m.group(2) for m in re.finditer(
            r"\b([012])\s*\u2192\s*`?([A-Z][A-Z0-9_]*(?:=(?:met|unmet|clean|dirty))?)", vmap)}
        if not pairs:
            continue
        for prefix, _pinned, words, penv in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
            if not words:
                continue
            key = (prefix, render_cmd(words, penv))
            prev = contracts.setdefault(key, {})
            for code, token in sorted(pairs.items()):
                if code in prev and prev[code] != token:
                    counts["duplicate"] += 1
                    out.append("pin line=%d kind=row state=duplicate row=%r "
                               "conflict=exit%d %s!=%s"
                               % (row["line"], row["cells"][0], code, token, prev[code]))
                prev[code] = token
    for n, raw in hidden_rows(text):
        counts["hidden"] += 1
        out.append("pin line=%d kind=row state=hidden row=%r" % (n, raw[:80]))
    cache = {}
    bound_instruments = set()
    for row in parse_registry(text):
        line = row["line"]
        if row["state"] == "unparsed":
            if re.search(r"(?i)selftest", row["raw"]):
                counts["unparsed"] += 1
                out.append("pin line=%d kind=row state=unparsed cells=%d header=%d"
                           % (line, len(row["cells"]), len(row["header"])))
            continue
        cells, idx = row["cells"], row["idx"]
        st = cells[idx]
        # R11: the row's claimed instrument — the first file path of its entry cell.
        entry_cell = cells[row["eidx"]] if len(cells) > row["eidx"] else ""
        entry_paths = PATH_RE.findall(entry_cell)
        claimed = entry_paths[0] if entry_paths else None
        # R14 (round-49 K7): the paths a line-count pin of this row may bind — the
        # instrument(s) its tally pins run and its claimed instrument. Bound once
        # here so the line-count and tally branches read the same argv.
        binds = pin_commands(cells, idx, rev, row["eidx"])
        allowed = {instrument_of(w) for _p, _t, w, _e in binds if w}
        if claimed:
            allowed.add(claimed)
        # R3 / R7 L4: ASCII-strict span checks (a tally digitless pin is still
        # counted by the tally branch below).
        for m in SPAN_RE.finditer(st):
            kind, reason = span_kind(m.group(1), cells, rev, row["eidx"])
            if kind == "unparsed":
                counts["unparsed"] += 1
                out.append("pin line=%d kind=span state=unparsed reason=%s span=%r"
                           % (line, reason, m.group(1)[:60]))
        # R6 + R10: truncated digest pins (`hex{8,63}…` must prefix the sha256 of the
        # nearest preceding in-tree path of the cell).
        for pfx, hit in trunc_digest_pins(st, row["raw"], root):
            counts["digest_pins"] += 1
            if hit is None:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=digest state=%s digest=%s… file=%s"
                       % (line, "match" if hit else "mismatch", pfx, hit))
        # R9c (CritJunkClasses D18): a tally written outside backticks in a self-test cell.
        if TALLY_TEXT_RE.search(SPAN_RE.sub(" ", st)):
            counts["unparsed"] += 1
            out.append("pin line=%d kind=span state=unparsed reason=tally-outside-backticks" % line)
        # R5: line-count pins (`(\d+) lines` binds to nearest preceding in-tree path).
        # R14: the bound path must be the instrument the row runs.
        for num, relpath, bound in line_count_pins(st, root, allowed):
            if relpath is None:
                counts["unparsed"] += 1
                out.append("pin line=%d kind=lines state=unparsed pinned='%d lines'" % (line, num))
                continue
            if not bound:
                counts["mismatches"] += 1
                out.append("pin line=%d kind=lines state=mismatch pinned='%d lines' file=%s "
                           "reason=path-not-row-instrument bound=%s"
                           % (line, num, relpath,
                              " ".join(sorted(a for a in allowed if a)) or "-"))
                continue
            fp = os.path.join(root, relpath)
            with open(fp, "rb") as f:
                nl = f.read().count(b"\n")
            if nl != num:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=lines state=%s pinned='%d lines' file=%s observed=%d"
                       % (line, "match" if nl == num else "mismatch", num, relpath, nl))
        ordinal = {}
        for prefix, pinned, words, penv in binds:
            n = ordinal.get(prefix, 0)
            ordinal[prefix] = n + 1
            norm = norm_cmd(words, penv, rev)
            bkey = (cells[0], prefix, n)
            rebound = False
            # X1 (round-48 w2 R48CritV3Junk2): a pin whose bound command is unresolvable
            # (norm is None) is a `no_command` finding below — never a rebound, whose
            # finding line names the bound argv. Formatting that None turned a registry
            # finding into a setup exit 2 (`can only join an iterable`).
            if norm is not None:
                if bkey in base_bind and base_bind[bkey] is not None and norm != base_bind[bkey]:
                    rebound = True  # existing row changed its bound argv
                elif (bkey not in base_bind and prefix in base_bind_prefix
                        and norm not in base_bind_prefix[prefix]
                        and (len(base_bind_prefix[prefix]) == 1
                             or os.path.basename(instrument_of(norm) or "")
                             not in {os.path.basename(instrument_of(v) or "")
                                     for v in base_bind_prefix[prefix]})):
                    # K5 (round-48 w2 R48CritV3Junk2): a prefix banked by several
                    # baseline instruments is a namespace only for its own family — a
                    # new round's copy of one of those instruments (same basename).
                    # Any other new instrument joining it is `rebound`.
                    rebound = True
            if rebound:
                counts["rebound"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=rebound cmd=%r"
                           % (line, prefix, " ".join(norm)))
            counts["tally_pins"] += 1
            if not re.search(r"\d", pinned):
                counts["unparsed"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=unparsed pinned=%r"
                           % (line, prefix, pinned))
                continue
            if words is None:
                counts["no_command"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=no_command" % (line, prefix))
                continue
            # R11 (D7): the bound argv must run the row's claimed instrument or a
            # mutant of it, never a different instrument.
            inst = instrument_of(words)
            bound_instruments.add(inst)
            if inst != claimed and not mutant_of(inst, claimed):
                counts["misattributed"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=misattributed claimed=%s bound=%s"
                           % (line, prefix, claimed, inst))
                continue
            # K2 (round-48 w2 R48CritV3Junk2): the run is the command the row writes.
            # An assignment that cannot be reproduced without a shell is fatal, never
            # silently dropped (dropping it was the false green).
            envr, bad_env = resolve_env(penv, root)
            if bad_env is not None:
                counts["env_unexpanded"] += 1
                out.append("pin line=%d kind=tally prefix=%s state=env_unexpanded variable=%s cmd=%r"
                           % (line, prefix, bad_env, render_cmd(words, penv)))
                continue
            key = (tuple(words), tuple(sorted(envr.items())))
            if key not in cache:
                cache[key] = run_cmd(words, root, scratch, timeout, envr)
            rc, text_out = cache[key]
            # v2: only lines that START with the prefix are tally lines (a `compat:`
            # echo of an old tally is not), and they must all agree.
            tails = {l.strip()[len(prefix):].strip() for l in text_out.splitlines()
                     if re.match(re.escape(prefix) + r"(?![A-Za-z0-9_])", l.strip())}
            observed = tails.pop() if len(tails) == 1 else None
            want = pinned.strip()
            # v2: the observed tail must equal the pinned text exactly (a weakened pin
            # such as `pass=22` for `pass=22 fail=0` is a mismatch).
            ok = observed is not None and observed.strip() == want
            # K8 (round-48 w2 R48CritV3Junk2): a PASS-form pin (`: PASS 12/12`,
            # `: PASS (6 cases)`) claims success but carries no `fail=0`, so keying the
            # exit check on that word left its exit code unconstrained. The exit code
            # must be 0 unless the pinned text itself asserts a nonzero failure count.
            if ok and rc != 0 and not re.search(r"\bfail=[1-9]\d*\b", want):
                ok = False
            if not ok:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=tally prefix=%s state=%s pinned=%r observed=%r rc=%s cmd=%r"
                       % (line, prefix, "match" if ok else "mismatch", want,
                          (observed or "").strip()[:80] if observed is not None else None,
                          rc, render_cmd(words, penv)))
        for dm in HEX_RE.finditer(st):
            digest = dm.group(0)
            counts["digest_pins"] += 1
            # R10 (round-48 CritJunkClasses D1): a full digest binds to the nearest
            # preceding in-tree path of its own cell, never to any path of the row.
            p = _nearest_in_tree_path(st[:dm.start()], root)
            hit = p if p is not None and sha256_file(os.path.join(root, p)) == digest else None
            if hit is None:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=digest state=%s digest=%s file=%s"
                       % (line, "match" if hit else "mismatch", digest[:12], p))
    # R13 (round-49 K6): a measured tree that ships this instrument must pin it. The
    # registry floor and `dropped` cannot see the reconciler's own row — the row is
    # new since the baseline — so deleting it left the registry green at 30 pins.
    if (self_instrument and os.path.isfile(os.path.join(root, self_instrument))
            and self_instrument not in bound_instruments):
        counts["dropped"] += 1
        out.append("pin kind=self state=dropped instrument=%s" % self_instrument)
    met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
           and counts["no_command"] == 0 and counts["dropped"] == 0
           and counts["rebound"] == 0 and counts["duplicate"] == 0
           and counts["hidden"] == 0 and counts["misattributed"] == 0
           and counts["env_unexpanded"] == 0
           and counts["tally_pins"] >= min_tally)
    out.append("PIN_CHECK=%s tally_pins=%d digest_pins=%d mismatches=%d unparsed=%d "
               "no_command=%d dropped=%d rebound=%d duplicate=%d hidden=%d misattributed=%d "
               "env_unexpanded=%d min_tally_pins=%d rev=%s baseline=%s"
               % ("met" if met else "unmet", counts["tally_pins"], counts["digest_pins"],
                  counts["mismatches"], counts["unparsed"], counts["no_command"],
                  counts["dropped"], counts["rebound"], counts["duplicate"], counts["hidden"],
                  counts["misattributed"], counts["env_unexpanded"],
                  min_tally, rev or "-",
                  "yes" if baseline_text is not None else "no"))
    return met, out


def export_rev(repo, rev, dest):
    try:
        full = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=60, check=True).stdout.decode().strip()
        arc = subprocess.run(["git", "-C", repo, "archive", "--format=tar", full],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=300, check=True).stdout
    except (subprocess.SubprocessError, OSError):
        return None
    tarpath = os.path.join(dest, "tree.tar")
    with open(tarpath, "wb") as f:
        f.write(arc)
    tree = os.path.join(dest, "tree")
    os.mkdir(tree)
    with tarfile.open(tarpath) as t:
        t.extractall(tree, filter="data")
    os.unlink(tarpath)
    return full, tree


def main(argv):
    ap = argparse.ArgumentParser(prog="mori-pin-check.py")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--rev")
    g.add_argument("--root")
    ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--skill")
    ap.add_argument("--min-tally-pins", type=int, default=1)
    ap.add_argument("--baseline-rev", help="every pin key (row name, prefix) in SKILL.md at this "
                    "revision must still be present (a deleted pin is not a fix)")
    ap.add_argument("--timeout", type=int, default=TIMEOUT_S)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev and not args.root:
        print("PIN_CHECK_SETUP need --rev or --root", file=sys.stderr)
        return 2
    repo = os.path.abspath(args.repo)
    scratch_parent = os.path.join(repo, ".scratch")
    try:
        os.makedirs(scratch_parent, exist_ok=True)
        scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
        try:
            rev = None
            if args.rev:
                got = export_rev(repo, args.rev, scratch)
                if got is None:
                    print("PIN_CHECK_SETUP unresolvable revision %s" % args.rev, file=sys.stderr)
                    return 2
                rev, root = got
            else:
                root = os.path.abspath(args.root)
            skill = args.skill or os.path.join(root, "SKILL.md")
            try:
                with open(skill, encoding="utf-8") as f:
                    text = f.read()
            except OSError:
                print("PIN_CHECK_SETUP unreadable %s" % skill, file=sys.stderr)
                return 2
            baseline_text = None
            if args.baseline_rev:
                try:
                    bp = subprocess.run(["git", "-C", repo, "show", args.baseline_rev + ":SKILL.md"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
                except (subprocess.SubprocessError, OSError):
                    bp = None
                if bp is None or bp.returncode != 0:
                    print("PIN_CHECK_SETUP unreadable baseline %s" % args.baseline_rev, file=sys.stderr)
                    return 2
                baseline_text = bp.stdout.decode("utf-8", "replace")
            met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
            print("\n".join(out))
            return 0 if met else 1
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    except Exception as exc:
        # R7 L5: a setup failure exits 2 with one line, never a traceback.
        print("PIN_CHECK_SETUP %s" % exc, file=sys.stderr)
        return 2


# ---------------------------------------------------------------- selftest
HDR = "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n|---|---|---|---|---|---|---|---|\n"
TOOL = ("import sys\n"
        "if '--selftest' in sys.argv:\n"
        "    print('noise line')\n"
        "    print('FOO_SELFTEST pass=3 fail=0')\n"
        "    sys.exit(int(open(__file__ + '.rc').read()) if __import__('os').path.exists(__file__ + '.rc') else 0)\n")
SLOW = "import time, sys\nif '--selftest' in sys.argv:\n    time.sleep(30)\n    print('SLOW_SELFTEST pass=1 fail=0')\n"
REVTOOL = ("import sys\n"
           "if len(sys.argv) == 3 and sys.argv[2] == '--selftest' and sys.argv[1] == 'deadbeef':\n"
           "    print('REV_SELFTEST: PASS (2 cases)')\n"
           "else:\n    print('REV_SELFTEST: FAIL'); sys.exit(1)\n")
MUT = "import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=1'); sys.exit(1)\n"
TMPTOOL = ("import os, sys\n"
           "root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))\n"
           "t = os.path.realpath(os.environ.get('TMPDIR', '/'))\n"
           "if '--selftest' in sys.argv:\n"
           "    ok = t.startswith(root + os.sep)\n"
           "    print('TMP_SELFTEST pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1)); sys.exit(0 if ok else 1)\n")
# K2 fixtures: an instrument whose answer depends on the environment the row writes,
# and one whose answer depends on a variable the pin is only true when it is set.
ENVSTRICT = ("import os, sys\n"
             "if '--selftest' in sys.argv:\n"
             "    if os.environ.get('MORI_STRICT') == '1':\n"
             "        print('E_SELFTEST pass=2 fail=1'); sys.exit(1)\n"
             "    print('E_SELFTEST pass=3 fail=0')\n")
ENVMODE = ("import os, sys\n"
           "if '--selftest' in sys.argv:\n"
           "    if os.environ.get('E_MODE') == 'full':\n"
           "        print('E2_SELFTEST pass=1 fail=0')\n"
           "    else:\n"
           "        print('E2_SELFTEST pass=0 fail=1'); sys.exit(1)\n")
# K8 fixtures: a PASS-form tally (no `fail=` word), exit code from a sidecar; and a pin
# that itself asserts a nonzero failure count.
PASSTOOL = ("import os, sys\n"
            "if '--selftest' in sys.argv:\n"
            "    print('P_PASS_SELFTEST: PASS (6 cases)')\n"
            "    p = __file__ + '.rc'\n"
            "    sys.exit(int(open(p).read()) if os.path.exists(p) else 0)\n")
FAIL2TOOL = ("import sys\n"
             "if '--selftest' in sys.argv:\n"
             "    print('F2_SELFTEST pass=0 fail=2'); sys.exit(1)\n")


def row(selftest_cell, entry="`python3 tools/foo.py`", pinned="none", name="foo", verdict="0 ok"):
    return "| %s | gate | %s | %s | %s | %s | none | mori |\n" % (name, entry, verdict, selftest_cell, pinned)


def selftest():
    base = tempfile.mkdtemp(prefix="pin-selftest-")
    results = []
    try:
        root = os.path.join(base, "tree")
        os.makedirs(os.path.join(root, "tools"))
        with open(os.path.join(root, "tools", "foo.py"), "w") as f:
            f.write(TOOL)
        with open(os.path.join(root, "tools", "slow.py"), "w") as f:
            f.write(SLOW)
        with open(os.path.join(root, "tools", "rev.py"), "w") as f:
            f.write(REVTOOL)
        # R11 carve-out fixtures: a mutant of the claimed instrument lives under
        # `.ufo/waves/round-N/fixtures/mutants/<basename>` (SKILL.md:185); a fixture with
        # another basename, or the right basename outside a fixtures/mutants directory, is
        # not a mutant of the claimed instrument.
        for rel in (".ufo/waves/round-9/fixtures/mutants/foo.py",
                    ".ufo/waves/round-9/fixtures/mutants/bar.py",
                    ".ufo/waves/round-9/foo.py"):
            p = os.path.join(root, *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write(MUT)
        with open(os.path.join(root, "tools", "tmp.py"), "w") as f:
            f.write(TMPTOOL)
        for rel, src in (("envstrict.py", ENVSTRICT), ("envmode.py", ENVMODE),
                         ("passtool.py", PASSTOOL), ("fail2.py", FAIL2TOOL)):
            with open(os.path.join(root, "tools", rel), "w") as f:
                f.write(src)
        digest = sha256_file(os.path.join(root, "tools", "foo.py"))
        good = "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`"
        mutant_rel = ".ufo/waves/round-9/fixtures/mutants/foo.py"
        mut_ok = good + "; the mutant `%s` reads `FOO_SELFTEST pass=2 fail=1` rc 1" % mutant_rel
        mut_bad = good + "; the mutant `%s` reads `FOO_SELFTEST pass=3 fail=0`" % mutant_rel
        cases = [
            ("honest", HDR + row(good), 1, True, None),
            ("stale_tally", HDR + row("`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`"), 1, False, "mismatch"),
            ("stale_in_cell_true_elsewhere", HDR + row(
                "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`",
                pinned="`FOO_SELFTEST pass=3 fail=0`"), 1, False, "mismatch"),
            ("pin_moved_out_of_cell", HDR + row("`python3 tools/foo.py --selftest`",
                                                pinned="`FOO_SELFTEST pass=3 fail=0`"), 1, False, None),
            ("digest_ok", HDR + row(good + " at sha256 `%s` of `tools/foo.py`" % digest), 1, True, None),
            ("digest_stale", HDR + row(good + " at sha256 `%s` of `tools/foo.py`" % ("0" * 64)), 1, False, "mismatch"),
            ("malformed_row", HDR + "| foo | gate | `python3 tools/foo.py` | %s | none | mori |\n" % good, 0, False, "unparsed"),
            ("no_command", HDR + row("`FOO_SELFTEST pass=3 fail=0`", entry="no command here"), 1, False, "no_command"),
            ("digitless_pin", HDR + row("`python3 tools/foo.py --selftest` → `FOO_SELFTEST: PASS`"), 1, False, "unparsed"),
            ("timeout", HDR + row("`python3 tools/slow.py --selftest` → `SLOW_SELFTEST pass=1 fail=0`",
                                  entry="`python3 tools/slow.py`"), 1, False, "mismatch"),
            ("bare_flag_rev_entry", HDR + row("`--selftest` → `REV_SELFTEST: PASS (2 cases)`",
                                              entry="`python3 tools/rev.py <rev> [--repo DIR]`"), 1, True, None),
            ("escaped_pipe_cell", HDR + row(good, entry="`python3 tools/foo.py --scope user\\|system`"), 1, True, None),
            ("below_floor", HDR + row(good), 2, False, None),
            ("mutant_pin_bound_to_mutant", HDR + row(mut_ok), 2, True, None),
            ("mutant_pin_wrong", HDR + row(mut_bad), 2, False, "mismatch"),
            ("tmpdir_inside_measured_tree", HDR + row("`python3 tools/tmp.py --selftest` → `TMP_SELFTEST pass=1 fail=0`",
                                                      entry="`python3 tools/tmp.py`"), 1, True, None),
        ]
        with open(os.path.join(root, "tools", "big.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('BIG_SELFTEST pass=33 fail=0')\n")
        cases.append(("token_boundary_truncated_pin", HDR + row(
            "`python3 tools/big.py --selftest` → `BIG_SELFTEST pass=3`", entry="`python3 tools/big.py`"),
            1, False, "mismatch"))
        two = HDR + row(good) + row(good).replace("| foo |", "| bar |", 1)
        cases.append(("baseline_row_deleted", (HDR + row(good), two), 1, False, "dropped"))
        cases.append(("baseline_all_present", (two, two), 1, True, None))
        # v2 arms — the w1 CritC1Predicate/SentPinExec false-green classes (each green under v1).
        stale = "`FOO_SELFTEST pass=2 fail=0`"
        os.makedirs(os.path.join(root, ".scratch", "old"))
        with open(os.path.join(root, ".scratch", "old", "foo.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=0')\n")
        with open(os.path.join(root, "tools", "old.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=0')\n")
        cases.append(("v2_inline_code_rejected", HDR + row(
            "`python3 -c \"print('FOO_SELFTEST pass=2 fail=0')\" --selftest` → " + stale,
            entry="no command here"), 1, False, "no_command"))
        cases.append(("v2_scratch_path_rejected", HDR + row(
            "`python3 .scratch/old/foo.py --selftest` → " + stale, entry="no command here"),
            1, False, "no_command"))
        cases.append(("v2_weakened_pin_exact", HDR + row(
            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3`"), 1, False, "mismatch"))
        cases.append(("v2_rebound_to_other_tool", (HDR + row("`python3 tools/old.py --selftest` → " + stale),
                                                   HDR + row(good)), 1, False, "rebound"))
        cases.append(("v2_entry_rebound", (HDR + row("`--selftest` → " + stale, entry="`python3 tools/old.py`"),
                                           HDR + row("`--selftest` → `FOO_SELFTEST pass=3 fail=0`")),
                      1, False, "rebound"))
        # X1 arms (round-48 w2 R48CritV3Junk2): an existing baseline row whose bound
        # command becomes unresolvable is a `no_command` finding, not a setup exception.
        cases.append(("x1_baseline_binding_disappears", (HDR + row(
            "`python3 ./tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            entry="`python3 tools/foo.py`"), HDR + row(good)), 1, False, "no_command"))
        cases.append(("x1_baseline_binding_inline_code", (HDR + row(
            "`python3 -c \"print('FOO_SELFTEST pass=3 fail=0')\" --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            entry="`python3 tools/foo.py`"), HDR + row(good)), 1, False, "no_command"))
        # K5 arms (round-48 w2 R48CritV3Junk2): a prefix banked by two baseline
        # instruments admits a new round copy of its own family, never a different
        # instrument.
        for rel, pin in ((".ufo/waves/round-1/ns.py", 1), (".ufo/waves/round-2/ns.py", 2),
                         (".ufo/waves/round-3/ns.py", 3)):
            p = os.path.join(root, *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write("import sys\nif '--selftest' in sys.argv:\n"
                        "    print('NS_SELFTEST pass=%d fail=0')\n" % pin)
        with open(os.path.join(root, "tools", "stub.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('NS_SELFTEST pass=3 fail=0')\n")

        def nsrow(name, path, pin):
            return ("| %s | gate | `python3 %s --rev <rev>` | 0 ok | `python3 %s --selftest` → "
                    "`NS_SELFTEST pass=%d fail=0` | none | none | mori |\n" % (name, path, path, pin))
        ns_base = HDR + nsrow("ns-a", ".ufo/waves/round-1/ns.py", 1) + nsrow("ns-b", ".ufo/waves/round-2/ns.py", 2)
        cases.append(("k5_namespace_new_instrument_rejected",
                      (ns_base + nsrow("ns-c", "tools/stub.py", 3), ns_base), 3, False, "rebound"))
        cases.append(("k5_namespace_family_join_admitted",
                      (ns_base + nsrow("ns-c", ".ufo/waves/round-3/ns.py", 3), ns_base), 3, True, None))
        hidden = ("| foo | gate | `python3 tools/foo.py` | 0 ok | `python3 tools/foo.py --selftest` → "
                  "`foo_selftest pass=2 fail=0` | none | mori |\n")
        cases.append(("v2_hidden_row_and_duplicate", (HDR + hidden + row(good) + row(good), HDR + row(good)),
                      1, False, "unparsed"))
        cases.append(("v2_duplicate_name", HDR + row(good) + row(good), 1, False, "duplicate"))
        with open(os.path.join(base, "outside.py"), "w") as f:
            f.write("x = 1\n")
        out_digest = sha256_file(os.path.join(base, "outside.py"))
        cases.append(("v2_digest_path_traversal", HDR + row(
            good + " at sha256 `%s` of `../outside.py`" % out_digest), 1, False, "mismatch"))
        # v2 arms — w1 RevPinCheckCode M1 (stale echo), M3 (fenced example), L1 (entry column).
        with open(os.path.join(root, "tools", "decoy.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=4 fail=0')\n"
                    "    print('compat: FOO_SELFTEST pass=3 fail=0')\n")
        with open(os.path.join(root, "tools", "twice.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=3 fail=0')\n"
                    "    print('FOO_SELFTEST pass=4 fail=0')\n")
        cases.append(("v2_stale_echo_line_ignored", HDR + row(
            "`python3 tools/decoy.py --selftest` → `FOO_SELFTEST pass=3 fail=0`", entry="`python3 tools/decoy.py`"),
            1, False, "mismatch"))
        cases.append(("v2_disagreeing_tally_lines", HDR + row(
            "`python3 tools/twice.py --selftest` → `FOO_SELFTEST pass=3 fail=0`", entry="`python3 tools/twice.py`"),
            1, False, "mismatch"))
        cases.append(("v2_fenced_example_not_counted", "```markdown\n" + HDR + row(good) + "```\n", 1, False, None))
        cases.append(("v2_entry_column_from_header",
                      "| name | entry | self-test | owner |\n|---|---|---|---|\n"
                      "| foo | `python3 tools/rev.py <rev>` | `--selftest` → `REV_SELFTEST: PASS (2 cases)` | mori |\n",
                      1, True, None))
        # v3 arms — R1-R8 (each arm is killed by the mutation that removes its rule).
        with open(os.path.join(root, "tools", "lc.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('LC_SELFTEST pass=1 fail=0')\n"
                    + "# filler\n" * 39)
        assert open(os.path.join(root, "tools", "lc.py"), "rb").read().count(b"\n") == 42
        os.makedirs(os.path.join(root, "src"))
        with open(os.path.join(root, "src", "foo.py"), "w") as f:
            f.write(TOOL)
        with open(os.path.join(root, "foo.py"), "w") as f:
            f.write(TOOL)
        os.symlink(os.path.join(base, "outside.py"), os.path.join(root, "tools", "evil.py"))
        hidrow = "| hidd | gate | `python3 tools/foo.py` | 0 ok | `PIN_CHECK_SELFTEST pass=1 fail=0` | none | none | mori |\n"
        hidarg = "| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `A_SELFTEST pass=3 fail=0` | none | none | mori |\n"
        cases.append(("r1_header_selftest_spelling", HDR.replace("self-test", "selftest", 1) + row(good), 1, True, None))
        cases.append(("r1_header_self_test_spelling", HDR.replace("self-test", "self test", 1) + row(good), 1, True, None))
        cases.append(("r2_hidden_row_outside_table", HDR + row(good) + "\n" + hidrow, 1, False, "hidden"))
        cases.append(("r2_hidden_fenced", "```markdown\n" + hidrow + "```\n" + HDR + row(good), 1, False, "hidden"))
        cases.append(("r2_hidden_selftest_arg", HDR + row(good) + "\n" + hidarg, 1, False, "hidden"))
        cases.append(("r3_fullwidth_prefix", HDR + row(good + "; `PIN_CHECK＿SELFTEST pass=999 fail=0`"), 1, False, "unparsed"))
        cases.append(("r3_lowercase_prefix", HDR + row(good + "; `foo_selftest pass=2 fail=0`"), 1, False, "unparsed"))
        cases.append(("r3_mixedcase_prefix", HDR + row(good + "; `FOO_Selftest pass=4 fail=0`"), 1, False, "unparsed"))
        cases.append(("r4_rebound_new_row_same_prefix",
                       (HDR + row(good) +
                        "| bar | gate | `python3 tools/old.py` | 0 ok | `python3 tools/old.py --selftest` → `FOO_SELFTEST pass=2 fail=0` | none | none | mori |\n",
                        HDR + row(good)),
                       1, False, "rebound"))
        cases.append(("r5_line_count_match", HDR + row("`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (42 lines)",
                                                      entry="`python3 tools/lc.py`"), 1, True, None))
        cases.append(("r5_line_count_mismatch", HDR + row("`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (41 lines)",
                                                          entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
        cases.append(("r5_line_count_no_path", HDR + row("(7 lines) `python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`",
                                                         entry="`python3 tools/lc.py`"), 1, False, "unparsed"))
        # round 49 (Mo49ExecArmsBindUnlanded): an over-pin is a mismatch too — every other
        # arm pins fewer lines than the file has, so `nl != num` flipped to `nl > num`
        # survived the 65-arm suite (round-48 w2 R48MutV3Bind m_r5a).
        cases.append(("r5_line_count_overpin_mismatch", HDR + row(
            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (43 lines)",
            entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
        cases.append(("r6_trunc_digest_match", HDR + row(good + " at sha256 `%s…` of `tools/foo.py`" % digest[:12]), 1, True, None))
        cases.append(("r6_trunc_digest_mismatch", HDR + row(good + " at sha256 `%s…` of `tools/foo.py`"
                                                            % (digest[:11] + ("0" if digest[11] != "0" else "1"))), 1, False, "mismatch"))
        cases.append(("r7_token_not_at_span_start", HDR + row(good + "; `run: FOO_SELFTEST pass=3 fail=0`"), 1, False, "unparsed"))
        cases.append(("r7_symlink_digest_not_inside", HDR + row(
            good + " at sha256 `%s` of `tools/evil.py`" % out_digest), 1, False, "mismatch"))
        cases.append(("r7_argv_shape_rejected", HDR + row("`python3 src/foo.py --selftest` → " + stale, entry="no command here"),
                      1, False, "no_command"))
        cases.append(("r7_argv_dotdot_rejected", HDR + row("`python3 tools/../foo.py --selftest` → " + stale, entry="no command here"),
                      1, False, "no_command"))
        cases.append(("r7_argv_trailing_args_rejected", HDR + row("`python3 tools/foo.py --selftest extra` → " + stale, entry="no command here"),
                      1, False, "no_command"))
        # R7 L2: `\\|` is a literal backslash followed by a real separator; the row stays 8
        # cells. The entry cell names the instrument the row runs (R11: a pin with no claimed
        # instrument in its entry cell is `misattributed`, claimed=None).
        cases.append(("r7_escaped_double_backslash_pipe", HDR +
                      "| foo | gate | `python3 tools/foo.py --rev <rev>` a\\\\| 0 ok | "
                      "`python3 tools/foo.py --selftest` → "
                      "`FOO_SELFTEST pass=3 fail=0` | none | none | mori |\n", 1, True, None))
        # R10 (round-48 CritJunkClasses D1): a digest of another file named elsewhere in the row.
        slow_digest = sha256_file(os.path.join(root, "tools", "slow.py"))
        cases.append(("r10_digest_decoy_file_in_other_cell", HDR + row(
            good + " at sha256 `%s`" % slow_digest, pinned="`tools/slow.py`"), 1, False, "mismatch"))
        cases.append(("r10_trunc_digest_decoy_file_in_other_cell", HDR + row(
            good + " at sha256 `%s…`" % slow_digest[:12], pinned="`tools/slow.py`"), 1, False, "mismatch"))
        cases.append(("r10_digest_binds_to_nearest_preceding_path", HDR + row(
            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` at sha256 `%s` of `tools/foo.py`"
            % digest), 1, True, None))
        # round 49 (Mo49ExecArmsBindUnlanded): the digest binds to the nearest *preceding*
        # path, never to one written after it — `st[:dm.start()]` flipped to `st[dm.end():]`
        # survived the 65-arm suite (round-48 w2 R48MutV3Bind m_r10b).
        cases.append(("r10_digest_binds_to_nearest_preceding_path_not_following", HDR + row(
            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`; sha256 `%s` of `tools/slow.py`"
            % slow_digest, entry="`python3 tools/foo.py`"), 1, False, "mismatch"))
        # R9a (D5): a tally-looking token in a cell other than the self-test cell.
        cases.append(("r9a_tally_in_pinned_values_cell", HDR + row(
            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`",
            pinned="`FOO_SELFTEST pass=999 fail=0`"), 1, False, "hidden"))
        # R9b (D2): a continuation line directly under a row carries a tally.
        cases.append(("r9b_continuation_line_tally", HDR + row(good) +
                      "→ `FOO_SELFTEST pass=999 fail=0`\n", 1, False, "hidden"))
        # R9c (D18): a tally written outside backticks in the self-test cell.
        cases.append(("r9c_tally_outside_backticks", HDR + row(good + "; also FOO_SELFTEST pass=999 fail=0"),
                      1, False, "unparsed"))
        # R11 (round-48 wave-2 D7): the bound argv must run the claimed instrument.
        cases.append(("r11_misattributed_instrument", HDR + row(
            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`"), 1, False, "misattributed"))
        cases.append(("r11_mutant_other_basename_rejected", HDR + row(
            good + "; the fixture `.ufo/waves/round-9/fixtures/mutants/bar.py` reads "
            "`FOO_SELFTEST pass=2 fail=1` rc 1"), 2, False, "misattributed"))
        cases.append(("r11_second_entry_path_not_claimed", HDR + row(
            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`",
            entry="`python3 tools/foo.py --rev <rev>` (`--tool` default `tools/lc.py`)"),
            1, False, "misattributed"))
        cases.append(("r11_entry_cell_without_instrument", HDR + row(
            good, entry="the drift probe (no path named)"), 1, False, "misattributed"))
        cases.append(("r11_mutant_right_basename_wrong_directory", HDR + row(
            good + "; the fixture `.ufo/waves/round-9/foo.py` reads `FOO_SELFTEST pass=2 fail=1` rc 1"),
            2, False, "misattributed"))
        # R12-R14 arms (round 49, wave 1 — each arm is killed by removing its rule).
        lc_pin = "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`"
        lc_entry = "`python3 tools/lc.py`"
        cases.append(("r12_line_count_pin_deleted",
                      (HDR + row(lc_pin, entry=lc_entry),
                       HDR + row(lc_pin + " (42 lines)", entry=lc_entry)),
                      1, False, "dropped"))
        cases.append(("r12_trunc_digest_pin_deleted",
                      (HDR + row(good),
                       HDR + row(good + " at sha256 `%s…` of `tools/foo.py`" % digest[:12])),
                      1, False, "dropped"))
        cases.append(("r12_trunc_digest_repaired_to_full",
                      (HDR + row(good + " at sha256 `%s` of `tools/foo.py`" % digest),
                       HDR + row(good + " at sha256 `%s…` of `tools/foo.py`" % digest[:12])),
                      1, True, None))
        cases.append(("r14_line_count_decoy_path",
                      HDR + row(lc_pin + " of `tools/old.py` (3 lines)", entry=lc_entry),
                      1, False, "mismatch"))
        # K2 (round-48 w2 R48CritV3Junk2): the `VAR=value` prefix is the command's
        # environment, applied — not stripped and ignored. The first arm is the
        # critic's reproducer: as written the command prints `pass=2 fail=1` rc 1 while
        # the row pins the run without the variable.
        cases.append(("k2_env_prefix_as_written", HDR + row(
            "`MORI_STRICT=1 python3 tools/envstrict.py --selftest` → `E_SELFTEST pass=3 fail=0`",
            entry="`python3 tools/envstrict.py`"), 1, False, "mismatch"))
        cases.append(("k2_env_applied_honest_pin", HDR + row(
            "`E_MODE=full python3 tools/envmode.py --selftest` → `E2_SELFTEST pass=1 fail=0`",
            entry="`python3 tools/envmode.py`"), 1, True, None))
        cases.append(("k2_env_pwd_expanded", HDR + row(
            "`TMPDIR=$PWD/.scratch python3 tools/tmp.py --selftest` → `TMP_SELFTEST pass=1 fail=0`",
            entry="`python3 tools/tmp.py`"), 1, True, None))
        cases.append(("k2_env_unexpanded", HDR + row(
            "`TMPDIR=<elsewhere> python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`"),
            1, False, "env_unexpanded"))
        cases.append(("k2_entry_cell_env", HDR + row(
            "`--selftest` → `E_SELFTEST pass=3 fail=0`",
            entry="`MORI_STRICT=1 python3 tools/envstrict.py`"), 1, False, "mismatch"))
        # K8 (round-48 w2 R48CritV3Junk2): a PASS-form pin carries no `fail=0` but still
        # claims success, so its exit code is checked; a pin that itself asserts a
        # nonzero failure count keeps its nonzero exit legitimate.
        cases.append(("k8_pass_form_rc0", HDR + row(
            "`python3 tools/passtool.py --selftest` → `P_PASS_SELFTEST: PASS (6 cases)`",
            entry="`python3 tools/passtool.py`"), 1, True, None))
        cases.append(("k8_failure_count_exception", HDR + row(
            "`python3 tools/fail2.py --selftest` → `F2_SELFTEST pass=0 fail=2`",
            entry="`python3 tools/fail2.py`"), 1, True, None))
        # ---- v4 arms (ported from round-49 w1 Mo49ExecImplA): each rule carries a red arm and an
        # honest green arm. F1 adjacency (R48CritV3Junk1 §1, §7): R9b's "directly under a row" is the
        # nearest preceding NON-BLANK line.
        cases.append(("f1_blankline_continuation_tally", HDR + row(good) +
                      "\n\n\u2192 the observed text was `FOO_SELFTEST pass=999 fail=0`\n", 1, False, "hidden"))
        cases.append(("f1_honest_prose_after_blank", HDR + row(good) +
                      "\n\nA prose paragraph that pins nothing.\n", 1, True, None))
        cases.append(("f1_adjacency_is_nearest_nonblank", HDR + row(good) +
                      "\n\nA prose line.\n\nA later line quotes `FOO_SELFTEST pass=999 fail=0` in prose.\n",
                      1, True, None))
        # F2 header normalisation (§2): NFKC plus zero-width deletion.
        nb = HDR.replace("self-test", "self\u00a0test", 1)
        cases.append(("f2_laundered_header_row_measured", nb + row(
            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`"), 1, False, "mismatch"))
        cases.append(("f2_laundered_header_zwsp_token", nb + row(
            "`python3 tools/foo.py --selftest` → `FOO_\u200bSELFTEST pass=999 fail=0`"), 1, False, "unparsed"))
        cases.append(("f2_laundered_header_honest_row", nb + row(good), 1, True, None))
        cases.append(("f2_zwsp_in_header_cell", HDR.replace("self-test", "self-\u200btest", 1) + row(good),
                      1, True, None))
        # F3 row shape (§3, §4): any indentation is a row shape.
        cases.append(("f3_tab_indented_fenced_row", "```\n\t| foo | gate | `python3 tools/foo.py` | 0 ok | "
                      "`FOO_SELFTEST pass=999 fail=0` | none | none | mori |\n```\n" + HDR + row(good),
                      1, False, "hidden"))
        cases.append(("f3_four_space_row", "    | foo | gate | `python3 tools/foo.py` | 0 ok | "
                      "`FOO_SELFTEST pass=999 fail=0` | none | none | mori |\n" + HDR + row(good),
                      1, False, "hidden"))
        cases.append(("f3_indented_examples_without_token",
                      "    | an | indented | example | row |\n\n```\n\t| a | tab | example | row |\n```\n"
                      + HDR + row(good), 1, True, None))
        # F4 HTML table markup (§8): a `<tr`/`<td` line is a row shape.
        cases.append(("f4_html_row_with_pin", "<table>\n<tr><td>html</td><td>gate</td><td>"
                      "<code>python3 tools/foo.py --selftest</code> \u2192 "
                      "<code>FOO_SELFTEST pass=999 fail=0</code></td></tr>\n</table>\n" + HDR + row(good),
                      1, False, "hidden"))
        cases.append(("f4_html_without_pin", "<!-- an honest note: nothing pinned here -->\n\n<table>\n"
                      "<tr><td>note</td><td>plain prose cell</td></tr>\n</table>\n" + HDR + row(good),
                      1, True, None))
        # F5 exit contracts (§6): one (prefix, argv), one contract; the verdict-map column is found
        # through the F2 header normalisation (Mo49ExecImplA D1).
        f5_a = row(good, name="pn a", verdict="0 \u2192 `PN_RUN=met` \u00b7 1 \u2192 `PN_RUN=unmet`")
        f5_b = row(good, name="pn b", verdict="0 \u2192 `PN_RUN=met` \u00b7 1 \u2192 `PN_SETUP`")
        f5_c = row(good, name="pn c", verdict="0 \u2192 `PN_RUN=met` \u00b7 1 \u2192 `PN_RUN=unmet`")
        cases.append(("f5_conflicting_exit_contracts", HDR + f5_a + f5_b, 2, False, "duplicate"))
        cases.append(("f5_agreeing_exit_contracts", HDR + f5_a + f5_c, 2, True, None))
        cases.append(("f5_unstated_contract_skipped",
                      HDR + f5_a + row(good, name="pn d", verdict="unchanged from row `pn a`"),
                      2, True, None))
        cases.append(("f5_nbsp_verdict_map_header_still_read",
                      HDR.replace("verdict map", "verdict\u00a0map", 1) + f5_a + f5_b, 2, False, "duplicate"))
        cases.append(("r11_same_instrument_green", HDR + row(
            good, entry="`python3 tools/foo.py --rev <rev>` (the audit reads `tools/slow.py` in prose)"),
            1, True, None))
        # ------------------------------------------------ round-49 w1 (Mo49ExecArmsHeader):
        # killing arms for the eleven single-point survivors the round-48 mutation seats
        # reported — w2/R48MutV3Header.md m2r1/m2r2/m2r3, w2/R48MutV3Hidden.md #2/#4/#6/#10/#11/#12
        # and w2/R48MutV3Bind.md m_r5a/m_r10b. Each arm FAILs on the mutant that removes or
        # weakens its rule and PASSes on the unmutated tool (receipts in
        # .ufo/waves/round-49/w1/Mo49ExecArmsHeader.md).
        os.makedirs(os.path.join(root, "tools", ".scratch", "old"))
        with open(os.path.join(root, "tools", ".scratch", "old", "foo.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n    print('FOO_SELFTEST pass=2 fail=0')\n")
        sibling = os.path.join(base, "treeext")
        os.makedirs(sibling)
        with open(os.path.join(sibling, "f.py"), "w") as f:
            f.write("receipt copy\n")
        os.symlink(os.path.join("..", "treeext"), os.path.join(root, "esc"))
        sibling_digest = sha256_file(os.path.join(sibling, "f.py"))
        # R1 alias spelling is matched case-insensitively (v3 m2r1 deleted `.lower()`).
        cases.append(("r1_header_case_insensitive", HDR.replace("self-test", "Self-Test", 1) + row(good),
                      1, True, None))
        # R2: a row-shaped hidden line carrying `--selftest` and no ASCII SELFTEST token (m2r2).
        cases.append(("r2_hidden_selftest_arg_no_token", HDR + row(good) + "\n"
                      "| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `clean` | none | none | mori |\n",
                      1, False, "hidden"))
        # R3: a decorative non-ASCII span that never folds to a SELFTEST prefix (m2r3).
        cases.append(("r3_nonascii_decorative_span", HDR + row(good + "; `caf\u00e9 \u2713`"), 1, False, "unparsed"))
        # R9a: another cell's tally written without `fail=` (m-r9a-wk, `pass=\d+\s+fail=\d+`).
        cases.append(("r9a_tally_in_pinned_cell_pass_only",
                      HDR + row(good, pinned="`FOO_SELFTEST pass=999`"), 1, False, "hidden"))
        # R9b: `--selftest` on a continuation line, no tally token (m-r9b-wk).
        cases.append(("r9b_continuation_line_selftest_flag",
                      HDR + row(good) + "fallback: `python3 tools/old.py --selftest`\n", 1, False, "hidden"))
        # R9c: the `NAME: PASS` tally shape outside backticks (m-r9c-wk).
        cases.append(("r9c_tally_PASS_form_outside_backticks",
                      HDR + row(good + "; also X_SELFTEST: PASS (6 cases)"), 1, False, "unparsed"))
        # argv_ok: a `tools/.scratch/…` command is rejected only by the `/.scratch/` sub-check
        # (m-av-scratch); SAFE_PATH itself accepts the shape.
        cases.append(("r7_argv_tools_scratch_rejected", HDR + row(
            "`python3 tools/.scratch/old/foo.py --selftest` \u2192 `FOO_SELFTEST pass=2 fail=0`",
            entry="`python3 tools/.scratch/old/foo.py`"), 1, False, "no_command"))
        # inside_tree: a symlink path placed before its digest is the nearest preceding path, so
        # realpath containment is what rejects it (m-sl-rm dropped containment to isfile).
        cases.append(("r7_symlink_digest_precedes_path_containment", HDR + row(
            good + "; receipt `tools/evil.py` at sha256 `%s`" % out_digest), 1, False, "mismatch"))
        # inside_tree: a realpath that carries realpath(root) only as a bare string prefix, a
        # sibling directory whose name extends the root's basename (m-sl-wk dropped `+ os.sep`).
        cases.append(("r7_symlink_digest_prefix_sibling", HDR + row(
            good + "; receipt `esc/f.py` at sha256 `%s`" % sibling_digest), 1, False, "mismatch"))
        # R5: a line-count pin claiming more lines than the file has (m_r5a flipped `!=` to `>`).
        cases.append(("r5_line_count_overpin_mismatch", HDR + row(
            "`python3 tools/lc.py --selftest` \u2192 `LC_SELFTEST pass=1 fail=0` (43 lines)",
            entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
        # R10: a full digest followed by its own matching path must not bind forward (m_r10b
        # flipped nearest-preceding to nearest-following).
        cases.append(("r10_digest_following_path_not_bound", HDR + row(
            good + "; sha256 `%s` of `tools/slow.py`" % slow_digest), 1, False, "mismatch"))
        for name, text, floor, want_met, want_state in cases:
            scratch = tempfile.mkdtemp(prefix="c-", dir=base)
            text, btext = text if isinstance(text, tuple) else (text, None)
            met, out = check(text, root, scratch, "deadbeef", 5, floor, btext)
            ok = met == want_met and (want_state is None or any("state=%s" % want_state in l for l in out))
            results.append((name, ok, out[-1]))
        # rc arm: tool prints the pinned tally but exits non-zero.
        with open(os.path.join(root, "tools", "foo.py.rc"), "w") as f:
            f.write("1")
        scratch = tempfile.mkdtemp(prefix="c-", dir=base)
        met, out = check(HDR + row(good), root, scratch, "deadbeef", 5, 1)
        results.append(("nonzero_rc_with_fail0", (not met) and any("state=mismatch" in l for l in out), out[-1]))
        os.unlink(os.path.join(root, "tools", "foo.py.rc"))
        # K8 arm: the PASS-form pin's command prints the pinned text and exits 1.
        with open(os.path.join(root, "tools", "passtool.py.rc"), "w") as f:
            f.write("1")
        scratch = tempfile.mkdtemp(prefix="c-", dir=base)
        met, out = check(HDR + row(
            "`python3 tools/passtool.py --selftest` → `P_PASS_SELFTEST: PASS (6 cases)`",
            entry="`python3 tools/passtool.py`"), root, scratch, "deadbeef", 5, 1)
        results.append(("k8_pass_form_rc1", (not met) and any("state=mismatch" in l for l in out), out[-1]))
        os.unlink(os.path.join(root, "tools", "passtool.py.rc"))
        # R13 arms (round-49 K6): the instrument under measurement must be pinned.
        with open(os.path.join(root, "tools", "selfpin.py"), "w") as f:
            f.write("import sys\nif '--selftest' in sys.argv:\n"
                    "    print('SELF_SELFTEST pass=1 fail=0')\n")
        self_row = row("`python3 tools/selfpin.py --selftest` → `SELF_SELFTEST pass=1 fail=0`",
                       entry="`python3 tools/selfpin.py`").replace("| foo |", "| selfpin |", 1)
        for arm_name, body, want_met, want_mark in (
                ("r13_self_row_deleted", HDR + row(good), False, "kind=self state=dropped"),
                ("r13_self_row_pinned", HDR + row(good) + self_row, True, None),
                ("r13_self_instrument_absent_no_obligation", HDR + row(good), True, None)):
            scratch = tempfile.mkdtemp(prefix="c-", dir=base)
            met, out = check(body, root, scratch, "deadbeef", 5, 1,
                             self_instrument=("tools/absent.py" if "absent" in arm_name
                                              else "tools/selfpin.py"))
            results.append((arm_name, met == want_met and
                            (want_mark is None or any(want_mark in l for l in out)), out[-1]))
        # CLI arm: --root through main(), exit codes.
        with open(os.path.join(root, "SKILL.md"), "w") as f:
            f.write(HDR + row(good))
        cli = subprocess.run([sys.executable, os.path.abspath(__file__), "--root", root, "--repo", base],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        results.append(("cli_met_rc0", cli.returncode == 0 and b"PIN_CHECK=met" in cli.stdout, "rc=%d" % cli.returncode))
        cli2 = subprocess.run([sys.executable, os.path.abspath(__file__), "--rev", "no-such-rev", "--repo", base],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        results.append(("cli_bad_rev_rc2", cli2.returncode == 2, "rc=%d" % cli2.returncode))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    fails = 0
    for name, ok, last in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, last))
        fails += 0 if ok else 1
    print("PIN_CHECK_SELFTEST pass=%d fail=%d" % (len(results) - fails, fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
