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
  interpreter (`python3`, `bash`, `sh`; leading `VAR=value` words dropped),
  or a bare `.py`/`.sh` path (e.g. a named mutant), run as
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
  outside their own lane root); the output lines that START with the prefix
  must all carry one text after it, that text must equal the pinned text
  exactly, and when the pin says `fail=0` the exit code must be 0. Lines inside
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
  no_command=N dropped=N rebound=N duplicate=N min_tally_pins=N rev=… baseline=yes|no`
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
        low = [c.lower() for c in cells]
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
        row_shaped = bool(re.match(r"^ {0,3}\|", raw))
        if kind in ("candidate", "fence_body") and row_shaped:
            if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:
                found.append((n, raw))
        elif kind == "row" and len(payload["cells"]) == len(payload["header"]):
            for ci, c in enumerate(payload["cells"]):
                if ci != payload["idx"] and TALLY_TEXT_RE.search(c):
                    found.append((n, raw))
                    break
        elif kind == "other" and re.match(r"^ {0,3}\|", prev_raw):
            if TALLY_TEXT_RE.search(raw) or "--selftest" in raw:
                found.append((n, raw))
        prev_raw = raw
    return found


def inside_tree(root, path):
    rel = os.path.normpath(path)
    if os.path.isabs(rel) or rel == ".." or rel.startswith(".." + os.sep):
        return False
    fp = os.path.join(root, rel)
    return (os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)
            and os.path.isfile(fp))


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


def line_count_pins(st, root):
    """R5: `(\\d+) lines` binds to the nearest preceding path in the same cell
    that resolves to an in-tree file; returns [(num, relpath_or_None)]."""
    return [(int(m.group(1)), _nearest_in_tree_path(st[:m.start()], root))
            for m in LINE_COUNT_RE.finditer(st)]


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
    """Return argv for one backticked self-test-cell span, or None (v2: only
    argv that passes argv_ok)."""
    if "--selftest" not in span:
        argv = None
        if re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.py", span):
            argv = ["python3", span, "--selftest"]
        elif re.fullmatch(r"[A-Za-z0-9_.][A-Za-z0-9_./-]*\.sh", span):
            argv = ["bash", span, "--selftest"]
        return argv if argv is not None and argv_ok(argv, rev) else None
    argv = derive_command(span, cells, rev, eidx)
    return argv if argv is not None and argv_ok(argv, rev) else None


def pin_commands(cells, idx, rev, eidx=2):
    """Bind each tally pin in the self-test cell to the nearest preceding
    executable span: a `--selftest` command, or a bare `.py`/`.sh` path (a
    mutant named after the main command is run as `<interp> <path> --selftest`)."""
    st = cells[idx]
    bound = []
    current = None
    for m in SPAN_RE.finditer(st):
        span = m.group(1)
        pm = re.match(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", span, re.S)
        if pm:
            bound.append((pm.group(1), pm.group(2), current))
            continue
        cmd = command_from_span(span, cells, rev, eidx)
        if cmd is not None:
            current = cmd
    return bound


def strip_env(words):
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):
        words.pop(0)
    return words


def derive_command(span, cells, rev, eidx=2):
    """argv for a span containing `--selftest`; the bare flag borrows the entry cell."""
    try:
        words = strip_env(shlex.split(span))
    except ValueError:
        return None
    if words and words[0] in INTERPRETERS:
        return words
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
    ewords = strip_env(ewords)
    if not ewords or ewords[0] not in INTERPRETERS or any(w.startswith("<") for w in ewords):
        return None
    return ewords + ["--selftest"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(words, root, scratch, timeout):
    # TMPDIR lives inside the measured tree (<root>/.scratch): lane tools such as
    # mori-round19-regressions.py refuse a TMPDIR outside their own lane root.
    tmp_parent = os.path.join(root, ".scratch")
    os.makedirs(tmp_parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="pin-tmp-", dir=tmp_parent)
    env = dict(os.environ, TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")
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
    """Multiset {(row name, pin kind/prefix): count} over parsed rows — no commands run."""
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
        for _ in HEX_RE.findall(st):
            k = (name, "sha256")
            keys[k] = keys.get(k, 0) + 1
    return keys

def pin_bindings(text, rev):
    """{(row name, prefix, ordinal): bound argv with the revision as `<REV>`}."""
    out = {}
    for row in parse_registry(text):
        if row["state"] != "ok":
            continue
        seen = {}
        for prefix, _pinned, words in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
            n = seen.get(prefix, 0)
            seen[prefix] = n + 1
            norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
            out[(row["cells"][0], prefix, n)] = norm
    return out


def check(text, root, scratch, rev, timeout, min_tally, baseline_text=None):
    out = []
    counts = {"tally_pins": 0, "digest_pins": 0, "mismatches": 0,
              "unparsed": 0, "no_command": 0, "dropped": 0, "rebound": 0,
              "duplicate": 0, "hidden": 0}
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
    for n, raw in hidden_rows(text):
        counts["hidden"] += 1
        out.append("pin line=%d kind=row state=hidden row=%r" % (n, raw[:80]))
    cache = {}
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
        for num, relpath in line_count_pins(st, root):
            if relpath is None:
                counts["unparsed"] += 1
                out.append("pin line=%d kind=lines state=unparsed pinned='%d lines'" % (line, num))
                continue
            fp = os.path.join(root, relpath)
            with open(fp, "rb") as f:
                nl = f.read().count(b"\n")
            if nl != num:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=lines state=%s pinned='%d lines' file=%s observed=%d"
                       % (line, "match" if nl == num else "mismatch", num, relpath, nl))
        ordinal = {}
        for prefix, pinned, words in pin_commands(cells, idx, rev, row["eidx"]):
            n = ordinal.get(prefix, 0)
            ordinal[prefix] = n + 1
            norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
            bkey = (cells[0], prefix, n)
            rebound = False
            if bkey in base_bind and base_bind[bkey] is not None and norm != base_bind[bkey]:
                rebound = True  # existing row changed its bound argv
            elif (bkey not in base_bind and norm is not None and prefix in base_bind_prefix
                    and len(base_bind_prefix[prefix]) == 1
                    and norm not in base_bind_prefix[prefix]):
                rebound = True  # new row rebinds a single-instrument prefix
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
            key = tuple(words)
            if key not in cache:
                cache[key] = run_cmd(words, root, scratch, timeout)
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
            if ok and re.search(r"\bfail=0\b", want) and rc != 0:
                ok = False
            if not ok:
                counts["mismatches"] += 1
            out.append("pin line=%d kind=tally prefix=%s state=%s pinned=%r observed=%r rc=%s cmd=%r"
                       % (line, prefix, "match" if ok else "mismatch", want,
                          (observed or "").strip()[:80] if observed is not None else None,
                          rc, " ".join(words)))
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
    met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
           and counts["no_command"] == 0 and counts["dropped"] == 0
           and counts["rebound"] == 0 and counts["duplicate"] == 0
           and counts["hidden"] == 0 and counts["tally_pins"] >= min_tally)
    out.append("PIN_CHECK=%s tally_pins=%d digest_pins=%d mismatches=%d unparsed=%d "
               "no_command=%d dropped=%d rebound=%d duplicate=%d hidden=%d min_tally_pins=%d rev=%s baseline=%s"
               % ("met" if met else "unmet", counts["tally_pins"], counts["digest_pins"],
                  counts["mismatches"], counts["unparsed"], counts["no_command"],
                  counts["dropped"], counts["rebound"], counts["duplicate"], counts["hidden"],
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


def row(selftest_cell, entry="`python3 tools/foo.py`", pinned="none"):
    return "| foo | gate | %s | 0 ok | %s | %s | none | mori |\n" % (entry, selftest_cell, pinned)


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
        with open(os.path.join(root, "tools", "mut.py"), "w") as f:
            f.write(MUT)
        with open(os.path.join(root, "tools", "tmp.py"), "w") as f:
            f.write(TMPTOOL)
        digest = sha256_file(os.path.join(root, "tools", "foo.py"))
        good = "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`"
        mut_ok = good + "; the mutant `tools/mut.py` reads `FOO_SELFTEST pass=2 fail=1` rc 1"
        mut_bad = good + "; the mutant `tools/mut.py` reads `FOO_SELFTEST pass=3 fail=0`"
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
        # R7 L2: `\\|` is a literal backslash followed by a real separator; the row stays 8 cells.
        cases.append(("r7_escaped_double_backslash_pipe", HDR +
                      "| foo | gate | a\\\\| 0 ok | `python3 tools/foo.py --selftest` → "
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
