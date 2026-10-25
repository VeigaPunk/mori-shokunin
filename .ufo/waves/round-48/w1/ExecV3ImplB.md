# ExecV3ImplB — w1 build report (mori round 48, C1 v3 candidate)

Seat: ExecV3ImplB (leaf executor; no subagent dispatched). Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured revision R = entering tip
`e5dbac05459887d9597ea5d1da0d8e3d024e0d17`; baseline `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.
Frozen counter `.ufo/waves/round-48/count-c1.py`; no tools installed (python3 only);
all lane-tool runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-ExecV3ImplB/tmp`.

## 1. Candidate artifact

- Base: `tools/mori-pin-check.py` at R (v2, sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`).
- Candidate: `.scratch/r48-ExecV3ImplB/mori-pin-check.py` (never in `tools/`).
- sha256 (candidate): `4eb06936c1838de41692656583bb5253997dc3679d714cded8859826d9021395`
- Line count: 858. Production tool bytes untouched (sha re-verified after work).

## 2. Implementation

Structural design as instructed: one tokenizer pass `scan_lines()` over SKILL.md
classifies every line (fence_open / fence_close / fence_body / header /
separator / row / candidate / other); `parse_registry()` (R1 header
recognition: `self-test` | `selftest` | `self test`, case-insensitive, exact
cell match) and `hidden_rows()` (R2) consume the same pass. New counters:
`hidden` (fatal) appended after `duplicate=` on the verdict line.

- R1 header: recognised cell set `HEADER_CELLS`; J1's `selftest`-headed gate
  table is parsed and its corrupt pins fail.
- R2 visibility: a row-shaped line (`^ {0,3}\|`) outside any parsed self-test
  table — including lines inside fences — carrying an ASCII
  `[A-Z][A-Z0-9_]*SELFTEST` token or the text `--selftest` counts `hidden`
  (fatal). Covers J5 (fenced block) and J6 (blank line between separator and
  first row breaks the table; the orphan row becomes hidden).
- R3 ASCII: inside a self-test cell, a backticked span that is neither a full
  digest, a truncated digest, an ASCII tally pin, nor a bound command is
  `unparsed` when (a) its first whitespace-delimited token contains a non-ASCII
  character, or (b) its first token NFKC-casefolds to a tally-prefix shape
  (`[A-Z][A-Z0-9_]*SELFTEST` fullmatch, case-insensitive), or (c) it carries an
  ASCII `...SELFTEST` token not at span start (R7 L4). Kills J2/J3 and
  lower/mixed-case prefix obfuscations.
- R4 rebound: v2 per-(row,prefix,ordinal) binding retained for existing rows; a
  NEW row that binds a prefix whose baseline bindings name exactly one distinct
  argv (a single canonical instrument) is `rebound` when its argv is outside
  that set. A prefix already shared by several baseline instruments is treated
  as a namespace (new genuine instruments may join it) — this is what keeps the
  honest H4 row and real row 939 green while J4 (archived copy of the single
  canonical `MORI_SOURCES_APPENDONLY` instrument) is caught. Baseline argv sets
  are resolved with a placeholder revision and normalised back to `<REV>`
  because a literal `<REV>` word is rejected by `derive_command`.
- R5 line-count pins: `(\d+) lines` binds to the nearest preceding path in the
  same cell that resolves to an in-tree file; newline count must equal it,
  else `mismatch`; no resolving path → `unparsed`. Kills J7 (742 vs 743).
- R6 truncated digests: `[0-9a-f]{8,63}…` is a digest pin that must prefix the
  sha256 of a path named in the row that resolves inside the tree; counts in
  `digest_pins`; else `mismatch`. Kills J8.
- R7 residuals: L2 escaped `\|` kept in cell (unchanged `split_cells`); L4
  token-not-at-span-start → `unparsed` (part of R3); L5 setup failures exit 2
  with one line — `main()` body wrapped so any exception prints
  `PIN_CHECK_SETUP …` and exits 2, never a traceback.
- R8 selftest: 53 arms (34 v2 + 19 new), one per rule/clause (see below); each
  new arm is killed by the mutation removing its rule (verified individually by
  construction: baseline/current texts chosen so the arm is green only with the
  rule present).

## 3. Selftest (tail = full output)

```
PASS honest  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS stale_tally  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS stale_in_cell_true_elsewhere  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS pin_moved_out_of_cell  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digest_ok  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digest_stale  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS malformed_row  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=0 rev=deadbeef baseline=no
PASS no_command  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS digitless_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS timeout  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS bare_flag_rev_entry  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS escaped_pipe_cell  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS below_floor  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS mutant_pin_bound_to_mutant  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS mutant_pin_wrong  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=2 rev=deadbeef baseline=no
PASS tmpdir_inside_measured_tree  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS token_boundary_truncated_pin  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS baseline_row_deleted  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=1 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS baseline_all_present  PIN_CHECK=met tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_inline_code_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_scratch_path_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_weakened_pin_exact  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_rebound_to_other_tool  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_entry_rebound  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_hidden_row_and_duplicate  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=1 hidden=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS v2_duplicate_name  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=1 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_digest_path_traversal  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_stale_echo_line_ignored  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_disagreeing_tally_lines  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_fenced_example_not_counted  PIN_CHECK=unmet tally_pins=0 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 min_tally_pins=1 rev=deadbeef baseline=no
PASS v2_entry_column_from_header  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r1_header_selftest_spelling  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r1_header_self_test_spelling  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_row_outside_table  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_fenced  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 min_tally_pins=1 rev=deadbeef baseline=no
PASS r2_hidden_selftest_arg  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=1 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_fullwidth_prefix  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_lowercase_prefix  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r3_mixedcase_prefix  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r4_rebound_new_row_same_prefix  PIN_CHECK=unmet tally_pins=2 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=1 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=yes
PASS r5_line_count_match  PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r5_line_count_no_path  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r6_trunc_digest_match  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r6_trunc_digest_mismatch  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_token_not_at_span_start  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_symlink_digest_not_inside  PIN_CHECK=unmet tally_pins=1 digest_pins=1 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_shape_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_dotdot_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS r7_argv_trailing_args_rejected  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 no_command=1 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS nonzero_rc_with_fail0  PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=1 rev=deadbeef baseline=no
PASS cli_met_rc0  rc=0
PASS cli_bad_rev_rc2  rc=2
PIN_CHECK_SELFTEST pass=53 fail=0
```

## 4. Full `diff -u` v2 → candidate

```
--- tools/mori-pin-check.py	2026-10-25 18:36:50.824795541 -0300
+++ .scratch/r48-ExecV3ImplB/mori-pin-check.py	2026-10-25 19:03:28.016270102 -0300
@@ -14,6 +14,19 @@
 inside the measured tree. The round-47 claim P-C1 is scored with the frozen
 v1 bytes; v2 is the lane's standing tool.
 
+v3 (round 48, wave w1): adds, per the v3-spec R1-R8: case-insensitive
+header recognition (`self-test` | `selftest` | `self test`); hidden-row
+accounting (a row-shaped line outside a parsed self-test table — including
+inside fences — carrying an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token or the text
+`--selftest` is `hidden`, fatal); ASCII-strict span checks (a span whose first
+token is non-ASCII, or whose first token casefolds to a tally-prefix shape, or
+that carries an ASCII tally token not at its start, is `unparsed`); rebound by
+instrument prefix (a row using a baseline prefix with an argv outside that
+rprefix's baseline set); line-count pins (`(\\d+) lines` binds to the nearest
+preceding path in the same cell that resolves inside the tree); truncated-digest
+pins (`hex{8,63}…` must prefix a named in-tree file's sha256); setup failures
+exit 2 with one line, never a traceback.
+
 What it reads
   Every Markdown table in SKILL.md whose header row has a cell named
   `self-test`. Cells are split on unescaped `|`; a data row whose cell count
@@ -77,6 +90,7 @@
 import sys
 import tarfile
 import tempfile
+import unicodedata
 
 TIMEOUT_S = 600
 HEX_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
@@ -91,6 +105,13 @@
 SAFE_PATH = re.compile(r"(?:tools|\.ufo/waves/round-[0-9]+)/[A-Za-z0-9_./-]+\.(?:py|sh)")
 PY_FLAGS = ("-I", "-B")
 
+HEADER_CELLS = ("self-test", "selftest", "self test")
+HIDDEN_TOKEN_RE = re.compile(r"[A-Z][A-Z0-9_]*SELFTEST")
+TRUNC_DIGEST_RE = re.compile(r"[0-9a-f]{8,63}\u2026")
+TALLY_PIN_RE = re.compile(r"([A-Z][A-Z0-9_]*SELFTEST)(.*)$", re.S)
+PINLIKE_T0_RE = re.compile(r"[A-Z][A-Z0-9_]*SELFTEST", re.I)
+LINE_COUNT_RE = re.compile(r"(\d+) lines")
+
 
 def argv_ok(argv, rev):
     if not argv or argv[0] not in INTERPRETERS:
@@ -124,44 +145,152 @@
     return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells) if cells else False
 
 
-def parse_registry(text):
-    """Rows of every self-test table: line, cells, header, idx (self-test),
-    eidx (entry), state ('ok'|'unparsed'). Lines inside ``` / ~~~ fences are
-    ignored, and a row followed by a separator row starts a new table."""
-    rows = []
+def scan_lines(text):
+    """Classify every line of SKILL.md — one tokenizer pass shared by header
+    recognition (R1), row parsing and hidden-row accounting (R2).
+
+    Kinds: fence_open/fence_close/fence_body (inside ``` / ~~~ blocks),
+    header (row with a recognised self-test header cell), separator,
+    row (data row of a parsed self-test table), candidate (row-shaped
+    line outside any parsed self-test table), other."""
+    lines = text.split("\n")
     header = None
-    idx = eidx = None
     fence = None
-    lines = text.split("\n")
     for n, line in enumerate(lines, 1):
         mark = line.lstrip()[:3]
         if mark in ("```", "~~~"):
-            fence = None if fence == mark else (fence or mark)
-            header = None
+            if fence == mark:
+                fence = None
+                header = None
+                yield n, "fence_close", {"raw": line}
+            else:
+                fence = fence or mark
+                yield n, "fence_open", {"raw": line}
             continue
         if fence:
+            yield n, "fence_body", {"raw": line}
             continue
         cells = split_cells(line)
         if cells is None:
             header = None
+            yield n, "other", {"raw": line}
             continue
         low = [c.lower() for c in cells]
-        if "self-test" in low:
-            header, idx = cells, low.index("self-test")
+        if any(c in HEADER_CELLS for c in low):
+            idx = next(i for i, c in enumerate(low) if c in HEADER_CELLS)
             eidx = low.index("entry") if "entry" in low else 2
+            header = (cells, idx, eidx)
+            yield n, "header", {"raw": line, "cells": cells, "idx": idx,
+                                 "eidx": eidx}
+            continue
+        if header is None:
+            yield n, "candidate", {"raw": line, "cells": cells}
             continue
-        if header is None or is_separator(cells):
+        if is_separator(cells):
+            yield n, "separator", {"raw": line, "cells": cells}
             continue
         nxt = split_cells(lines[n]) if n < len(lines) else None
         if nxt is not None and is_separator(nxt):
-            header = None  # another table's header row
+            header = None
+            yield n, "candidate", {"raw": line, "cells": cells}
+            continue
+        yield n, "row", {"raw": line, "cells": cells, "header": header[0],
+                         "idx": header[1], "eidx": header[2]}
+
+
+def parse_registry(text):
+    """Rows of every self-test table: line, cells, header, idx (self-test),
+    eidx (entry), state ('ok'|'unparsed'). Built from scan_lines; lines inside
+    ``` / ~~~ fences are ignored, and a row followed by a separator row starts
+    a new table."""
+    rows = []
+    for n, kind, payload in scan_lines(text):
+        if kind != "row":
             continue
-        state = "ok" if len(cells) == len(header) else "unparsed"
-        rows.append({"line": n, "cells": cells, "header": header, "idx": idx,
-                     "eidx": eidx, "state": state, "raw": line})
+        state = "ok" if len(payload["cells"]) == len(payload["header"]) else "unparsed"
+        rows.append({"line": n, "cells": payload["cells"], "header": payload["header"],
+                     "idx": payload["idx"], "eidx": payload["eidx"], "state": state,
+                     "raw": payload["raw"]})
     return rows
 
 
+def hidden_rows(text):
+    """R2: row-shaped lines (up to three leading spaces, then `|`) that are not
+    part of a parsed self-test table — including lines inside fences — and that
+    carry an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token or the text `--selftest`
+    are hidden pins (fatal)."""
+    found = []
+    for n, kind, payload in scan_lines(text):
+        if kind not in ("candidate", "fence_body"):
+            continue
+        raw = payload["raw"]
+        if not re.match(r"^ {0,3}\|", raw):
+            continue
+        if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:
+            found.append((n, raw))
+    return found
+
+
+def inside_tree(root, path):
+    rel = os.path.normpath(path)
+    if os.path.isabs(rel) or rel == ".." or rel.startswith(".." + os.sep):
+        return False
+    fp = os.path.join(root, rel)
+    return (os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)
+            and os.path.isfile(fp))
+
+
+def span_kind(span, cells, rev, eidx):
+    """Classify one backticked span of a self-test cell (R3, R7 L4):
+    ('tally'|'digest'|'trunc'|'command'|'unparsed'/reason|'ignore')."""
+    if HEX_RE.search(span):
+        return "digest", None
+    if TRUNC_DIGEST_RE.search(span):
+        return "trunc", None
+    if TALLY_PIN_RE.match(span):
+        return "tally", None
+    if command_from_span(span, cells, rev, eidx) is not None:
+        return "command", None
+    tok0 = span.split()[0] if span.split() else ""
+    if any(ord(c) > 127 for c in tok0):
+        return "unparsed", "non-ascii-token"
+    if PINLIKE_T0_RE.fullmatch(unicodedata.normalize("NFKC", tok0)):
+        return "unparsed", "casefold-selftest-prefix"
+    if HIDDEN_TOKEN_RE.search(span):
+        return "unparsed", "token-not-at-span-start"
+    return "ignore", None
+
+
+def _nearest_in_tree_path(prefix, root):
+    for pm in reversed(list(PATH_RE.finditer(prefix))):
+        if inside_tree(root, pm.group(0)):
+            return pm.group(0)
+    return None
+
+
+def line_count_pins(st, root):
+    """R5: `(\\d+) lines` binds to the nearest preceding path in the same cell
+    that resolves to an in-tree file; returns [(num, relpath_or_None)]."""
+    return [(int(m.group(1)), _nearest_in_tree_path(st[:m.start()], root))
+            for m in LINE_COUNT_RE.finditer(st)]
+
+
+def trunc_digest_pins(st, raw, root):
+    """R6: `[0-9a-f]{8,63}…` must be a prefix of the sha256 of some path named
+    in the row that resolves inside the tree; returns [(prefix, relpath|None)]."""
+    paths = sorted(set(PATH_RE.findall(raw)))
+    pins = []
+    for m in TRUNC_DIGEST_RE.finditer(st):
+        pfx = m.group(0)[:-1]
+        hit = None
+        for p in paths:
+            if inside_tree(root, p) and sha256_file(os.path.join(root, p)).startswith(pfx):
+                hit = p
+                break
+        pins.append((pfx, hit))
+    return pins
+
+
 def command_from_span(span, cells, rev, eidx=2):
     """Return argv for one backticked self-test-cell span, or None (v2: only
     argv that passes argv_ok)."""
@@ -293,8 +422,9 @@
     out = []
     counts = {"tally_pins": 0, "digest_pins": 0, "mismatches": 0,
               "unparsed": 0, "no_command": 0, "dropped": 0, "rebound": 0,
-              "duplicate": 0}
+              "duplicate": 0, "hidden": 0}
     base_bind = {}
+    base_bind_prefix = {}
     if baseline_text is not None:
         now = pin_keys(text)
         for k, n in sorted(pin_keys(baseline_text).items()):
@@ -302,7 +432,21 @@
             if gone > 0:
                 counts["dropped"] += gone
                 out.append("pin kind=baseline state=dropped row=%r pin=%s count=%d" % (k[0], k[1], gone))
+        # R4: keep the v2 per-key binding for existing rows, and record the
+        # baseline prefix → set of bound argv (any row) for new rows. A new row
+        # that binds a prefix whose baseline bindings name exactly one distinct
+        # argv (a single canonical instrument) is `rebound` when its argv is not
+        # in that set (a prefix already shared by several instruments is a
+        # namespace; new genuine instruments may join it).
         base_bind = pin_bindings(baseline_text, "<REV>")
+        # A literal `<REV>` word is rejected by derive_command, so re-resolve the
+        # baseline bindings with a placeholder revision and normalise it back to
+        # `<REV>` so the sets stay comparable with the current text.
+        _REV_PLACEHOLDER = "__REV__"
+        for (_name, prefix, _ordinal), norm in pin_bindings(baseline_text, _REV_PLACEHOLDER).items():
+            if norm is not None:
+                norm = tuple("<REV>" if w == _REV_PLACEHOLDER else w for w in norm)
+                base_bind_prefix.setdefault(prefix, set()).add(norm)
     names = {}
     for row in parse_registry(text):
         if row["state"] == "ok":
@@ -311,6 +455,9 @@
         if n > 1:
             counts["duplicate"] += n - 1
             out.append("pin kind=row state=duplicate row=%r count=%d" % (name, n))
+    for n, raw in hidden_rows(text):
+        counts["hidden"] += 1
+        out.append("pin line=%d kind=row state=hidden row=%r" % (n, raw[:80]))
     cache = {}
     for row in parse_registry(text):
         line = row["line"]
@@ -322,17 +469,51 @@
             continue
         cells, idx = row["cells"], row["idx"]
         st = cells[idx]
+        # R3 / R7 L4: ASCII-strict span checks (a tally digitless pin is still
+        # counted by the tally branch below).
+        for m in SPAN_RE.finditer(st):
+            kind, reason = span_kind(m.group(1), cells, rev, row["eidx"])
+            if kind == "unparsed":
+                counts["unparsed"] += 1
+                out.append("pin line=%d kind=span state=unparsed reason=%s span=%r"
+                           % (line, reason, m.group(1)[:60]))
+        # R6: truncated digest pins (`hex{8,63}…` must prefix a named in-tree file).
+        for pfx, hit in trunc_digest_pins(st, row["raw"], root):
+            counts["digest_pins"] += 1
+            if hit is None:
+                counts["mismatches"] += 1
+            out.append("pin line=%d kind=digest state=%s digest=%s… file=%s"
+                       % (line, "match" if hit else "mismatch", pfx, hit))
+        # R5: line-count pins (`(\d+) lines` binds to nearest preceding in-tree path).
+        for num, relpath in line_count_pins(st, root):
+            if relpath is None:
+                counts["unparsed"] += 1
+                out.append("pin line=%d kind=lines state=unparsed pinned='%d lines'" % (line, num))
+                continue
+            fp = os.path.join(root, relpath)
+            with open(fp, "rb") as f:
+                nl = f.read().count(b"\n")
+            if nl != num:
+                counts["mismatches"] += 1
+            out.append("pin line=%d kind=lines state=%s pinned='%d lines' file=%s observed=%d"
+                       % (line, "match" if nl == num else "mismatch", num, relpath, nl))
         ordinal = {}
         for prefix, pinned, words in pin_commands(cells, idx, rev, row["eidx"]):
             n = ordinal.get(prefix, 0)
             ordinal[prefix] = n + 1
-            bkey = (cells[0], prefix, n)
             norm = None if words is None else tuple("<REV>" if w == rev else w for w in words)
+            bkey = (cells[0], prefix, n)
+            rebound = False
             if bkey in base_bind and base_bind[bkey] is not None and norm != base_bind[bkey]:
+                rebound = True  # existing row changed its bound argv
+            elif (bkey not in base_bind and norm is not None and prefix in base_bind_prefix
+                    and len(base_bind_prefix[prefix]) == 1
+                    and norm not in base_bind_prefix[prefix]):
+                rebound = True  # new row rebinds a single-instrument prefix
+            if rebound:
                 counts["rebound"] += 1
-                out.append("pin line=%d kind=tally prefix=%s state=rebound baseline_cmd=%r cmd=%r"
-                           % (line, prefix, " ".join(base_bind[bkey]),
-                              " ".join(norm) if norm else None))
+                out.append("pin line=%d kind=tally prefix=%s state=rebound cmd=%r"
+                           % (line, prefix, " ".join(norm)))
             counts["tally_pins"] += 1
             if not re.search(r"\d", pinned):
                 counts["unparsed"] += 1
@@ -366,16 +547,10 @@
                           rc, " ".join(words)))
         for digest in HEX_RE.findall(st):
             counts["digest_pins"] += 1
-            paths = sorted(set(PATH_RE.findall(row["raw"])))
             hit = None
-            for p in paths:
-                rel = os.path.normpath(p)
-                if os.path.isabs(rel) or rel == ".." or rel.startswith(".." + os.sep):
-                    continue
-                fp = os.path.join(root, rel)
-                if (os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)
-                        and os.path.isfile(fp) and sha256_file(fp) == digest):
-                    hit = rel
+            for p in sorted(set(PATH_RE.findall(row["raw"]))):
+                if inside_tree(root, p) and sha256_file(os.path.join(root, p)) == digest:
+                    hit = p
                     break
             if hit is None:
                 counts["mismatches"] += 1
@@ -384,12 +559,13 @@
     met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
            and counts["no_command"] == 0 and counts["dropped"] == 0
            and counts["rebound"] == 0 and counts["duplicate"] == 0
-           and counts["tally_pins"] >= min_tally)
+           and counts["hidden"] == 0 and counts["tally_pins"] >= min_tally)
     out.append("PIN_CHECK=%s tally_pins=%d digest_pins=%d mismatches=%d unparsed=%d "
-               "no_command=%d dropped=%d rebound=%d duplicate=%d min_tally_pins=%d rev=%s baseline=%s"
+               "no_command=%d dropped=%d rebound=%d duplicate=%d hidden=%d min_tally_pins=%d rev=%s baseline=%s"
                % ("met" if met else "unmet", counts["tally_pins"], counts["digest_pins"],
                   counts["mismatches"], counts["unparsed"], counts["no_command"],
-                  counts["dropped"], counts["rebound"], counts["duplicate"], min_tally, rev or "-",
+                  counts["dropped"], counts["rebound"], counts["duplicate"], counts["hidden"],
+                  min_tally, rev or "-",
                   "yes" if baseline_text is not None else "no"))
     return met, out
 
@@ -435,41 +611,46 @@
         return 2
     repo = os.path.abspath(args.repo)
     scratch_parent = os.path.join(repo, ".scratch")
-    os.makedirs(scratch_parent, exist_ok=True)
-    scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
     try:
-        rev = None
-        if args.rev:
-            got = export_rev(repo, args.rev, scratch)
-            if got is None:
-                print("PIN_CHECK_SETUP unresolvable revision %s" % args.rev, file=sys.stderr)
-                return 2
-            rev, root = got
-        else:
-            root = os.path.abspath(args.root)
-        skill = args.skill or os.path.join(root, "SKILL.md")
+        os.makedirs(scratch_parent, exist_ok=True)
+        scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
         try:
-            with open(skill, encoding="utf-8") as f:
-                text = f.read()
-        except OSError:
-            print("PIN_CHECK_SETUP unreadable %s" % skill, file=sys.stderr)
-            return 2
-        baseline_text = None
-        if args.baseline_rev:
+            rev = None
+            if args.rev:
+                got = export_rev(repo, args.rev, scratch)
+                if got is None:
+                    print("PIN_CHECK_SETUP unresolvable revision %s" % args.rev, file=sys.stderr)
+                    return 2
+                rev, root = got
+            else:
+                root = os.path.abspath(args.root)
+            skill = args.skill or os.path.join(root, "SKILL.md")
             try:
-                bp = subprocess.run(["git", "-C", repo, "show", args.baseline_rev + ":SKILL.md"],
-                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
-            except (subprocess.SubprocessError, OSError):
-                bp = None
-            if bp is None or bp.returncode != 0:
-                print("PIN_CHECK_SETUP unreadable baseline %s" % args.baseline_rev, file=sys.stderr)
+                with open(skill, encoding="utf-8") as f:
+                    text = f.read()
+            except OSError:
+                print("PIN_CHECK_SETUP unreadable %s" % skill, file=sys.stderr)
                 return 2
-            baseline_text = bp.stdout.decode("utf-8", "replace")
-        met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
-        print("\n".join(out))
-        return 0 if met else 1
-    finally:
-        shutil.rmtree(scratch, ignore_errors=True)
+            baseline_text = None
+            if args.baseline_rev:
+                try:
+                    bp = subprocess.run(["git", "-C", repo, "show", args.baseline_rev + ":SKILL.md"],
+                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
+                except (subprocess.SubprocessError, OSError):
+                    bp = None
+                if bp is None or bp.returncode != 0:
+                    print("PIN_CHECK_SETUP unreadable baseline %s" % args.baseline_rev, file=sys.stderr)
+                    return 2
+                baseline_text = bp.stdout.decode("utf-8", "replace")
+            met, out = check(text, root, scratch, rev, args.timeout, args.min_tally_pins, baseline_text)
+            print("\n".join(out))
+            return 0 if met else 1
+        finally:
+            shutil.rmtree(scratch, ignore_errors=True)
+    except Exception as exc:
+        # R7 L5: a setup failure exits 2 with one line, never a traceback.
+        print("PIN_CHECK_SETUP %s" % exc, file=sys.stderr)
+        return 2
 
 
 # ---------------------------------------------------------------- selftest
@@ -597,6 +778,50 @@
                       "| name | entry | self-test | owner |\n|---|---|---|---|\n"
                       "| foo | `python3 tools/rev.py <rev>` | `--selftest` → `REV_SELFTEST: PASS (2 cases)` | mori |\n",
                       1, True, None))
+        # v3 arms — R1-R8 (each arm is killed by the mutation that removes its rule).
+        with open(os.path.join(root, "tools", "lc.py"), "w") as f:
+            f.write("import sys\nif '--selftest' in sys.argv:\n    print('LC_SELFTEST pass=1 fail=0')\n"
+                    + "# filler\n" * 39)
+        assert open(os.path.join(root, "tools", "lc.py"), "rb").read().count(b"\n") == 42
+        os.makedirs(os.path.join(root, "src"))
+        with open(os.path.join(root, "src", "foo.py"), "w") as f:
+            f.write(TOOL)
+        with open(os.path.join(root, "foo.py"), "w") as f:
+            f.write(TOOL)
+        os.symlink(os.path.join(base, "outside.py"), os.path.join(root, "tools", "evil.py"))
+        hidrow = "| hidd | gate | `python3 tools/foo.py` | 0 ok | `PIN_CHECK_SELFTEST pass=1 fail=0` | none | none | mori |\n"
+        hidarg = "| hidd | gate | `bash tools/a.sh --selftest` | 0 ok | `A_SELFTEST pass=3 fail=0` | none | none | mori |\n"
+        cases.append(("r1_header_selftest_spelling", HDR.replace("self-test", "selftest", 1) + row(good), 1, True, None))
+        cases.append(("r1_header_self_test_spelling", HDR.replace("self-test", "self test", 1) + row(good), 1, True, None))
+        cases.append(("r2_hidden_row_outside_table", HDR + row(good) + "\n" + hidrow, 1, False, "hidden"))
+        cases.append(("r2_hidden_fenced", "```markdown\n" + hidrow + "```\n" + HDR + row(good), 1, False, "hidden"))
+        cases.append(("r2_hidden_selftest_arg", HDR + row(good) + "\n" + hidarg, 1, False, "hidden"))
+        cases.append(("r3_fullwidth_prefix", HDR + row(good + "; `PIN_CHECK＿SELFTEST pass=999 fail=0`"), 1, False, "unparsed"))
+        cases.append(("r3_lowercase_prefix", HDR + row(good + "; `foo_selftest pass=2 fail=0`"), 1, False, "unparsed"))
+        cases.append(("r3_mixedcase_prefix", HDR + row(good + "; `FOO_Selftest pass=4 fail=0`"), 1, False, "unparsed"))
+        cases.append(("r4_rebound_new_row_same_prefix",
+                       (HDR + row(good) +
+                        "| bar | gate | `python3 tools/old.py` | 0 ok | `python3 tools/old.py --selftest` → `FOO_SELFTEST pass=2 fail=0` | none | none | mori |\n",
+                        HDR + row(good)),
+                       1, False, "rebound"))
+        cases.append(("r5_line_count_match", HDR + row("`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (42 lines)",
+                                                      entry="`python3 tools/lc.py`"), 1, True, None))
+        cases.append(("r5_line_count_mismatch", HDR + row("`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0` (41 lines)",
+                                                          entry="`python3 tools/lc.py`"), 1, False, "mismatch"))
+        cases.append(("r5_line_count_no_path", HDR + row("(7 lines) `python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`",
+                                                         entry="`python3 tools/lc.py`"), 1, False, "unparsed"))
+        cases.append(("r6_trunc_digest_match", HDR + row(good + " at sha256 `%s…` of `tools/foo.py`" % digest[:12]), 1, True, None))
+        cases.append(("r6_trunc_digest_mismatch", HDR + row(good + " at sha256 `%s…` of `tools/foo.py`"
+                                                            % (digest[:11] + ("0" if digest[11] != "0" else "1"))), 1, False, "mismatch"))
+        cases.append(("r7_token_not_at_span_start", HDR + row(good + "; `run: FOO_SELFTEST pass=3 fail=0`"), 1, False, "unparsed"))
+        cases.append(("r7_symlink_digest_not_inside", HDR + row(
+            good + " at sha256 `%s` of `tools/evil.py`" % out_digest), 1, False, "mismatch"))
+        cases.append(("r7_argv_shape_rejected", HDR + row("`python3 src/foo.py --selftest` → " + stale, entry="no command here"),
+                      1, False, "no_command"))
+        cases.append(("r7_argv_dotdot_rejected", HDR + row("`python3 tools/../foo.py --selftest` → " + stale, entry="no command here"),
+                      1, False, "no_command"))
+        cases.append(("r7_argv_trailing_args_rejected", HDR + row("`python3 tools/foo.py --selftest extra` → " + stale, entry="no command here"),
+                      1, False, "no_command"))
         for name, text, floor, want_met, want_state in cases:
             scratch = tempfile.mkdtemp(prefix="c-", dir=base)
             text, btext = text if isinstance(text, tuple) else (text, None)
```

## 5. count-c1 acceptance run (background; ~5 min)

Command:
`python3 -I -B .ufo/waves/round-48/count-c1.py --tool .scratch/r48-ExecV3ImplB/mori-pin-check.py --rev e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --repo <lane> --scratch .scratch/r48-ExecV3ImplB/c1`

```
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=unmet rc=1
variant name=H2 expect=met got=unmet rc=1
variant name=H3 expect=met got=unmet rc=1
variant name=H4 expect=met got=unmet rc=1
variant name=real expect=met got=unmet rc=1
C1=unmet junk_met=0 honest_unmet=4 real=unmet errors=0 variants=12 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17
```

Result: all eight junk edits J1-J8 are `unmet` (exit 1). H1-H4 and `real` are
`unmet` **only** because the entering registry itself carries one stale truncated
digest in row 168 (see §6); with that single registry repair they all become
`met`, giving `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12`
at the landed tip.

## 6. Real-registry output (candidate, `--rev e5dbac05 … --min-tally-pins 26 --baseline-rev 2d85e33d`)

```
pin line=166 kind=tally prefix=MORI_SILENCE_CASES_SELFTEST state=match pinned='pass=24 fail=0' observed='pass=24 fail=0' rc=0 cmd='bash tools/mori-silence-cases.sh --selftest'
pin line=168 kind=digest state=mismatch digest=c39e5a73… file=None
pin line=182 kind=tally prefix=R19_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 tools/mori-round19-regressions.py --selftest'
pin line=183 kind=tally prefix=C1_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c1.py --selftest'
pin line=184 kind=lines state=match pinned='743 lines' file=tools/mori-gate-registry.py observed=743
pin line=184 kind=tally prefix=GATE_REGISTRY_SELFTEST state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 tools/mori-gate-registry.py --selftest'
pin line=184 kind=digest state=match digest=8b82ac999091 file=tools/mori-gate-registry.py
pin line=185 kind=tally prefix=C2_SELFTEST state=match pinned='pass=5 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c2.py --selftest'
pin line=186 kind=tally prefix=C3_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c3.py --selftest'
pin line=187 kind=tally prefix=MORI_DISK_RATE_SELFTEST state=match pinned='pass=14 fail=0' observed='pass=14 fail=0' rc=0 cmd='python3 tools/mori-disk-rate.py --selftest'
pin line=188 kind=tally prefix=MORI_WAVE_SETTLEMENT_SELFTEST state=match pinned=': PASS (23 cases, 23 passed, 0 failed)' observed=': PASS (23 cases, 23 passed, 0 failed)' rc=0 cmd='python3 tools/mori-wave-settlement.py --selftest'
pin line=189 kind=tally prefix=MORI_R41_CALIBRATION_SELFTEST state=match pinned='pass=10 fail=0' observed='pass=10 fail=0' rc=0 cmd='python3 tools/mori-round41-calibration.py --selftest'
pin line=190 kind=tally prefix=C1_SELFTEST state=match pinned='pass=16 fail=0' observed='pass=16 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c1.py --selftest'
pin line=190 kind=tally prefix=C1_SELFTEST state=match pinned='pass=15 fail=1' observed='pass=15 fail=1' rc=1 cmd='python3 .ufo/waves/round-45/fixtures/mutants/count-c1.py --selftest'
pin line=190 kind=digest state=match digest=5f2deea0b35c file=.ufo/waves/round-45/count-c1.py
pin line=191 kind=tally prefix=C2_SELFTEST state=match pinned='pass=14 fail=0' observed='pass=14 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c2.py --selftest'
pin line=191 kind=digest state=match digest=153423c48ca9 file=.ufo/waves/round-45/count-c2.py
pin line=191 kind=digest state=match digest=9850b3fcc888 file=.ufo/waves/round-45/fixtures/mutants/count-c2.py
pin line=192 kind=digest state=match digest=37fd7c24ff52… file=.ufo/waves/round-45/count-c3.py
pin line=192 kind=digest state=match digest=69bf9b6eb29b… file=.ufo/waves/round-45/fixtures/mutants/count-c3.py
pin line=192 kind=tally prefix=C3_SELFTEST state=match pinned='pass=19 fail=0' observed='pass=19 fail=0' rc=0 cmd='python3 .ufo/waves/round-45/count-c3.py --selftest'
pin line=192 kind=tally prefix=C3_SELFTEST state=match pinned='pass=17 fail=2' observed='pass=17 fail=2' rc=1 cmd='python3 .ufo/waves/round-45/fixtures/mutants/count-c3.py --selftest'
pin line=193 kind=tally prefix=C1_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c1.py --selftest'
pin line=194 kind=lines state=match pinned='743 lines' file=tools/mori-gate-registry.py observed=743
pin line=194 kind=tally prefix=GATE_REGISTRY_SELFTEST state=match pinned='pass=15 fail=0' observed='pass=15 fail=0' rc=0 cmd='python3 tools/mori-gate-registry.py --selftest'
pin line=194 kind=digest state=match digest=8b82ac999091 file=tools/mori-gate-registry.py
pin line=195 kind=tally prefix=C2_SELFTEST state=match pinned='pass=5 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c2.py --selftest'
pin line=196 kind=tally prefix=C3_SELFTEST state=match pinned='pass=6 fail=0' observed='pass=6 fail=0' rc=0 cmd='python3 .ufo/waves/round-44/count-c3.py --selftest'
pin line=664 kind=tally prefix=MORI_PRESSURE_SELFTEST state=match pinned=': PASS 12/12' observed=': PASS 12/12' rc=0 cmd='python3 tools/mori-pressure.py --selftest'
pin line=665 kind=tally prefix=ROUTED_CHECK_SELFTEST state=match pinned='pass=20 fail=0' observed='pass=20 fail=0' rc=0 cmd='python3 -I tools/mori-routed-check.py --selftest'
pin line=739 kind=tally prefix=MORI_OOM_KILLERS_SELFTEST state=match pinned=': PASS 32/32' observed=': PASS 32/32' rc=0 cmd='python3 -I -B tools/mori-oom-killers.py --selftest'
pin line=740 kind=tally prefix=ROUTED_R24_SELFTEST state=match pinned='pass=26 fail=0' observed='pass=26 fail=0' rc=0 cmd='python3 -I -B tools/mori-routed-r24.py --selftest'
pin line=741 kind=tally prefix=MORI_JOB_RUNWAY_SELFTEST state=match pinned=': PASS 21/21' observed=': PASS 21/21' rc=0 cmd='python3 -I -B tools/mori-job-runway.py --selftest'
pin line=905 kind=tally prefix=MORI_SOURCE_DRIFT_SELFTEST state=match pinned=': PASS (6 cases)' observed=': PASS (6 cases)' rc=0 cmd='python3 tools/mori-source-drift.py --selftest'
pin line=911 kind=tally prefix=CONFORM_SELFTEST state=match pinned='pass=11 fail=0' observed='pass=11 fail=0' rc=0 cmd='python3 .ufo/waves/round-40/conform.py e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --selftest'
pin line=912 kind=tally prefix=MORI_SOURCES_APPENDONLY_SELFTEST state=match pinned='pass=22 fail=0' observed='pass=22 fail=0' rc=0 cmd='python3 tools/mori-sources-appendonly.py e5dbac05459887d9597ea5d1da0d8e3d024e0d17 --selftest'
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=939 kind=tally prefix=C2_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 .ufo/waves/round-47/count-c2.py --selftest'
PIN_CHECK=unmet tally_pins=28 digest_pins=8 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Findings (exactly one): `pin line=168 kind=digest state=mismatch digest=c39e5a73… file=None`
— row 168 (`r14 regressions`) self-test cell pins `harness SHA c39e5a73…`; no
path named in that row has a sha256 with that prefix in the measured tree (the
harness `tools/mori-round14-regressions.py` at R hashes to `533218a5…`; the
round-14 frozen census hashes to `39abda0a…`; `evidence/r14-selftest-accepted.json`
under round-14 waves hashes to `7c19bc08…`). This pin is stale (it referred to
the harness at rev `5601d12`).

Required registry repairs (L1 integration; never excused in the tool):
1. Row 168: replace `` `c39e5a73…` `` with the current harness sha prefix
   `` `533218a5…` `` (or drop the truncated digest / re-word it) so the pin
   resolves. After this single edit, rows 168, H1-H4 and `real` all measure
   `met` (verified: J4/H4/real runs differ from the green state only by this
   one line).

All other new rules measure green on the real registry: `hidden=0`, `unparsed=0`,
`rebound=0`, `dropped=0`, `duplicate=0`, `tally_pins=28`, `digest_pins=8`
(5 full digests + 3 truncated: rows 184/190/191×2/192×2/194 all match).

## 7. Risks / limits / interpretation notes

- R3 clause (b) is implemented as a first-token casefold prefix-shape check, not
  a whole-span substring check: a literal "any span whose NFKC-casefolded text
  contains `selftest`" reading would flag benign registry prose spans
  (`evidence/r14-selftest-accepted.json`, `--selftest-child`,
  `--selftest --cases ""`, `selftest()`, bare unbindable `--selftest`) and
  make the real registry unrepairable without rewriting unrelated prose. The
  chosen reading still kills every ASCII obfuscation of a tally-prefix
  (lowercase / mixed-case / fullwidth / Cyrillic) while leaving commands,
  filenames and option names alone.
- R4 treats a prefix shared by multiple baseline instruments as a namespace.
  A future junk that rebinds a stale/archived argv under a *multi-instrument*
  prefix would not be caught by the new-row rule (per-key rule still covers old
  rows). This is the boundary of the class the frozen junk actually exercises.
- J1-J8 all exit 1 for the *reported* reason (rule mapping above); the sim
  evidence per variant is in `.scratch/r48-ExecV3ImplB/` (findings reprinted in
  §5/§6).
- UNVERIFIED: nothing about the C2 claim or the assimilation package was
  touched or checked by this seat.

## 8. Evidence files (scratch)

- `.scratch/r48-ExecV3ImplB/mori-pin-check.py` (candidate)
- `.scratch/r48-ExecV3ImplB/diff-v2-v3.txt`
- `.scratch/r48-ExecV3ImplB/selftest.out`
- `.scratch/r48-ExecV3ImplB/count-c1.out`
- `.scratch/r48-ExecV3ImplB/real.out`
- `.scratch/r48-ExecV3ImplB/tree-analysis/` (committed-tree export at R, read-only analysis)
