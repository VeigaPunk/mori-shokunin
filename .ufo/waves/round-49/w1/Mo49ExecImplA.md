# Mo49ExecImplA — an independent v4 candidate of the pin reconciler (round 49, w1, C1)

Seat `Mo49ExecImplA` (leaf, mori-shokunin). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
fleet root `/home/vgpnk/Projects/shokunin`, entering tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`,
freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`.

**Frozen contract read first:** `.ufo/waves/round-49/contract.md` (C1 P-C1, the 26-variant list, the
controls table, the "independently implemented, not copied" disclosure).

**Implemented from these sources, not from the merged witness:**

| source | what it gives |
|---|---|
| `controls/tool-v3-entering.py` (sha256 `85a89a3b…` = `tools/mori-pin-check.py` at `b3e3453d`) | base bytes |
| `.scratch/r48w2-R48CritV3Junk1/fixes/f1_adjacency.py`, `f2_nfkc_header.py`, `f3_rowshape_indent.py`, `f4_html_rows.py`, `f5_exit_contract.py` | the five surface rules F1-F5 |
| `.ufo/waves/round-48/w2/R48CritV3Junk1.md` (§1-§8, "the repair set") | the class each rule closes, the cost notes, the N1-N9 shapes |
| `.scratch/r48w2-R48ExecD7/r11.diff`, `.ufo/waves/round-48/w2/R48ExecD7.md` §3, §4, §7, §8, §9 | R11 (D7), the four legitimate rows, the carve-out, the self-referential-pin consequence |

`controls/tool-r48-merged-witness.py` was **not opened** until the candidate was implemented,
self-tested and scored (§8 below).

**Write scope respected:** the only lane file written is this report; everything else is under
`.scratch/r49-Mo49ExecImplA/`. `git status --porcelain -- SKILL.md tools corpus .ufo/waves/round-49`
prints no modified tracked file (its untracked lines are the L1's `w1-dispatch.json`, `w1-spec.json`,
`w1-validate.err`, `w1.ready*`, `w1/`). No subagent was spawned (the optional read-only labrat was not
needed); no `git add/commit/stash/checkout/reset/pull/push`; no mutating `jj` command; no host read;
no pacman.

## 1. Candidate

| field | value |
|---|---|
| path | `.scratch/r49-Mo49ExecImplA/mori-pin-check.py` (absolute: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecImplA/mori-pin-check.py`) |
| sha256 | `c3f233f4f6089ea7c58bc5a71418d35efb807348fde254f65e9fd221bd7fbd9a` |
| lines | 1115 |
| base | `controls/tool-v3-entering.py`, sha256 `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`, 917 lines |
| selftest tally | `PIN_CHECK_SELFTEST pass=81 fail=0` (entering: `pass=60 fail=0`; +16 new arms, 0 removed) |

## 2. What v4 adds (rule → mechanism → source)

| rule | mechanism in the candidate | source |
|---|---|---|
| **F1** adjacency | `hidden_rows` updates `prev_raw` only on non-blank lines, so R9b's "directly under a row" is the nearest preceding **non-blank** row | `f1_adjacency.py`; `R48CritV3Junk1.md` §1, §7 |
| **F2** header normalisation | `header_key(cell)` = NFKC → delete U+200B/U+200C/U+200D/U+FEFF → strip → lower; used for header recognition (R1) and for the F5 column lookup | `f2_nfkc_header.py`; §2 |
| **F3** row shape | `ROW_SHAPE_RE = ^\s*\|` replaces `^ {0,3}\|` in both R2 (`candidate`/`fence_body`/`other`) and R9b's `prev_raw` test | `f3_rowshape_indent.py`; §3, §4 |
| **F4** HTML rows | `HTML_ROW_RE = ^\s*<t[rd][\s>]` (case-insensitive) makes an HTML table-markup line a row shape for R2, and `other` joins the scanned kinds | `f4_html_rows.py`; §8 |
| **F5** exit contracts | two rows binding one `(prefix, argv)` must state the same `verdict map` `code → token` pairs; a conflicting pair is `duplicate`; a cell with no pair ("unchanged from row …") is skipped | `f5_exit_contract.py`; §6 |
| **R11** misattribution | a tally pin's bound argv must run the row **entry** cell's first file path, or a `fixtures`/`mutants`-segment path with the same basename; a pin with no entry path is `misattributed` with `claimed=None`; the bound command is not run for a misattributed pin, which still counts toward the tally floor | `r11.diff`; `R48ExecD7.md` §4 |

The verdict line gains one counter, appended after `hidden=`:
`… hidden=%d misattributed=%d min_tally_pins=%d rev=%s baseline=%s`. `misattributed==0` is part of
`met`. `count-c1.py:run_tool` matches `^PIN_CHECK=(met|unmet)`, so the addition is compatible.

## 3. Acceptance (1) — the tool's own selftest

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=$PWD/.scratch/r49-Mo49ExecImplA python3 -I -B .scratch/r49-Mo49ExecImplA/mori-pin-check.py --selftest
```

The 65 inherited arms all `PASS` (no arm was removed, no inherited expectation changed except the two
relocated mutant fixtures and one entry cell, below). The 16 new arms (each rule: at least one red
arm and one honest green arm):

```
PASS f1_blankline_continuation_tally  PIN_CHECK=unmet … hidden=1 …
PASS f1_honest_prose_after_blank  PIN_CHECK=met … hidden=0 …
PASS f1_adjacency_is_nearest_nonblank  PIN_CHECK=met … hidden=0 …
PASS f2_laundered_header_row_measured  PIN_CHECK=unmet … mismatches=1 …
PASS f2_laundered_header_zwsp_token  PIN_CHECK=unmet … unparsed=1 …
PASS f2_laundered_header_honest_row  PIN_CHECK=met …
PASS f2_zwsp_in_header_cell  PIN_CHECK=met …
PASS f3_tab_indented_fenced_row  PIN_CHECK=unmet … hidden=1 …
PASS f3_four_space_row  PIN_CHECK=unmet … hidden=1 …
PASS f3_indented_examples_without_token  PIN_CHECK=met … hidden=0 …
PASS f4_html_row_with_pin  PIN_CHECK=unmet … hidden=1 …
PASS f4_html_without_pin  PIN_CHECK=met … hidden=0 …
PASS f5_conflicting_exit_contracts  PIN_CHECK=unmet … duplicate=1 …
PASS f5_agreeing_exit_contracts  PIN_CHECK=met … duplicate=0 …
PASS f5_unstated_contract_skipped  PIN_CHECK=met … duplicate=0 …
PASS r11_same_instrument_green  PIN_CHECK=met … misattributed=0 …
PIN_CHECK_SELFTEST pass=81 fail=0
exit=0
```

(`…` elides only counters that are zero in that arm; each arm's full line, the five inherited R11 red
arms and the inherited 60, are in `.scratch/r49-Mo49ExecImplA/selftest-final.txt`, 81 `PASS`, 0 `FAIL`.)

Two inherited expectations changed because R11 would otherwise reject them, exactly as `r11.diff`
states: the two mutant arms bind `.ufo/waves/round-9/fixtures/mutants/foo.py` (same basename as the
claimed `tools/foo.py`) instead of the former `tools/mut.py`, and `r7_escaped_double_backslash_pipe`'s
entry cell now names the instrument it runs (`python3 tools/foo.py --rev <rev>`); its purpose
(`\\|` splitting, 8 cells) is unchanged.

## 4. Acceptance (2) — the frozen C1 counter

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=$PWD/.scratch/r49-Mo49ExecImplA \
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/count-c1.py \
    --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecImplA/mori-pin-check.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 \
    --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecImplA/c1 --jobs 3
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=N1 expect=unmet got=unmet rc=1
variant name=N2 expect=unmet got=unmet rc=1
variant name=N3 expect=unmet got=unmet rc=1
variant name=N4 expect=unmet got=unmet rc=1
variant name=N5 expect=unmet got=unmet rc=1
variant name=N6 expect=unmet got=unmet rc=1
variant name=N7 expect=unmet got=unmet rc=1
variant name=N8 expect=unmet got=unmet rc=1
variant name=N9 expect=unmet got=unmet rc=1
variant name=H6 expect=met got=met rc=0
variant name=H7 expect=met got=met rc=0
variant name=N10 expect=unmet got=unmet rc=1
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86
exit=0
```

Wall time 1674 s (jobs 3); receipt `.scratch/r49-Mo49ExecImplA/c1-run.txt`. The run was made against
the frozen sha256 above (the file was not edited afterwards). One earlier run was cancelled when the
file changed (dead-fixture removal); its receipt is discarded, not merged.

## 5. Acceptance (3) — sha256 and the unified diff against the entering tool

sha256 of the copy: `c3f233f4f6089ea7c58bc5a71418d35efb807348fde254f65e9fd221bd7fbd9a`
(`.scratch/r49-Mo49ExecImplA/sha256.txt`).
`diff -u controls/tool-v3-entering.py .scratch/r49-Mo49ExecImplA/mori-pin-check.py` (372 lines,
`.scratch/r49-Mo49ExecImplA/v4-vs-entering.diff`):

````diff
--- .ufo/waves/round-49/controls/tool-v3-entering.py	2026-10-25 20:42:21.650511752 -0300
+++ .scratch/r49-Mo49ExecImplA/mori-pin-check.py	2026-10-25 21:50:24.441329534 -0300
@@ -32,6 +32,34 @@
 continuation line directly under a row, is `hidden` (R9a/R9b); a tally written
 outside backticks in a self-test cell is `unparsed` (R9c).
 
+v4 (round 49, wave w1 — an independent implementation of the round-48 wave-2
+proposals, not a copy of the merged witness). Six rules, each carried by its own
+selftest arms (a red arm and an honest green arm):
+  F1 adjacency (`w2/R48CritV3Junk1.md` §1, §7): R9b's "directly under a table
+     row" means the nearest preceding NON-BLANK line, so a claim on the first
+     line after a blank line still sits under the row it continues.
+  F2 header normalisation (§2): the header cell is matched after NFKC and
+     deletion of U+200B/U+200C/U+200D/U+FEFF, so an NBSP or a zero-width
+     character no longer launders a self-test header.
+  F3 row shape (§3, §4): R2's row shape is any indentation (`^\\s*\\|`), so a
+     tab-indented fenced row and a four-space-indented row keep their claim.
+  F4 HTML table markup (§8): a line opening with `<tr`/`<td` is a row shape for
+     R2's hidden scan, so a claim carried by HTML table markup is seen.
+  F5 exit contract (§6): two rows binding the same `(prefix, argv)` are two
+     authorities for one command; their `verdict map` exit-code → outcome
+     tokens must agree, otherwise `duplicate`.
+  R11 misattribution (`w2/R48ExecD7.md` §4, closes D7): a tally pin's bound argv
+     must run the row's claimed instrument — the first file path named in the
+     row's ENTRY cell — or a mutant of it: a path with a `fixtures` or `mutants`
+     directory segment whose basename equals the claimed instrument's basename
+     (the lane's `fixtures/mutants/<basename>` convention). Anything else, and a
+     pin whose entry cell names no path, is `misattributed` (fatal). The bound
+     command is not run for a misattributed pin; the pin still counts toward the
+     tally floor. R11 reads only the argv bound to each pin, never every path of
+     the self-test cell (row 912 names the reconciler in prose), and its mutant
+     carve-out keeps the legitimate mutant-command rows green.
+The `misattributed=` counter is appended to the verdict line after `hidden=`.
+
 What it reads
   Every Markdown table in SKILL.md whose header row has a cell named
   `self-test`. Cells are split on unescaped `|`; a data row whose cell count
@@ -119,6 +147,16 @@
 
 
 TALLY_TEXT_RE = re.compile(r"[A-Z][A-Z0-9_]*SELFTEST[:=]?\s*(?:pass=\d+|PASS)")
+# v4 F3/F4: what a reader sees as a table row is a row shape for R2, whatever
+# its indentation, and HTML table markup is a row shape too.
+ROW_SHAPE_RE = re.compile(r"^\s*\|")
+HTML_ROW_RE = re.compile(r"^\s*<t[rd][\s>]", re.I)
+# v4 F2: characters that render as nothing (or as a plain space, via NFKC) and
+# that must not launder a header cell.
+ZERO_WIDTH_CHARS = ("\u200b", "\u200c", "\u200d", "\ufeff")
+# v4 F5: an exit-code → outcome token pair inside a `verdict map` cell.
+VERDICT_PAIR_RE = re.compile(
+    r"\b([012])\s*\u2192\s*`?([A-Z][A-Z0-9_]*(?:=(?:met|unmet|clean|dirty))?)")
 
 
 def argv_ok(argv, rev):
@@ -168,6 +206,15 @@
     return all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells) if cells else False
 
 
+def header_key(cell):
+    """v4 F2: the comparison key of a header cell — NFKC (a no-break space renders
+    as a space), zero-width format characters deleted, case folded."""
+    s = unicodedata.normalize("NFKC", cell)
+    for ch in ZERO_WIDTH_CHARS:
+        s = s.replace(ch, "")
+    return s.strip().lower()
+
+
 def scan_lines(text):
     """Classify every line of SKILL.md — one tokenizer pass shared by header
     recognition (R1), row parsing and hidden-row accounting (R2).
@@ -198,7 +245,7 @@
             header = None
             yield n, "other", {"raw": line}
             continue
-        low = [c.lower() for c in cells]
+        low = [header_key(c) for c in cells]
         if any(c in HEADER_CELLS for c in low):
             idx = next(i for i, c in enumerate(low) if c in HEADER_CELLS)
             eidx = low.index("entry") if "entry" in low else 2
@@ -238,20 +285,26 @@
 
 
 def hidden_rows(text):
-    """R2 + R9: pins that a checker would not see are `hidden` (fatal):
-    (R2) row-shaped lines (up to three leading spaces, then `|`) outside a parsed
-    self-test table — including lines inside fences — carrying an ASCII
-    `[A-Z][A-Z0-9_]*SELFTEST` token or the text `--selftest`;
+    """R2 + R9 + v4 F1/F3/F4: pins that a checker would not see are `hidden`
+    (fatal):
+    (R2) a row-shaped line outside a parsed self-test table — including lines
+    inside fences — carrying an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token or the
+    text `--selftest`; v4 F3 widens the row shape to any indentation (`^\\s*\\|`)
+    and v4 F4 accepts HTML table markup (`<tr`/`<td`) as a row shape;
     (R9a, CritJunkClasses D5) a tally-looking token in a cell of a parsed row other
     than its self-test cell;
     (R9b, D2) a continuation line, directly under a table row and not itself a row,
-    carrying a tally-looking token or `--selftest`."""
+    carrying a tally-looking token or `--selftest`; v4 F1 reads "directly under" as
+    the nearest preceding NON-BLANK line."""
     found = []
     prev_raw = ""
     for n, kind, payload in scan_lines(text):
         raw = payload["raw"]
-        row_shaped = bool(re.match(r"^ {0,3}\|", raw))
-        if kind in ("candidate", "fence_body") and row_shaped:
+        # v4 F3 (any indentation) and F4 (HTML table markup) define what a reader
+        # sees as a row; R9b's continuation test below stays pipe-shaped because
+        # its `prev_raw` is the row a line continues.
+        row_shaped = bool(ROW_SHAPE_RE.match(raw) or HTML_ROW_RE.match(raw))
+        if kind in ("candidate", "fence_body", "other") and row_shaped:
             if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:
                 found.append((n, raw))
         elif kind == "row" and len(payload["cells"]) == len(payload["header"]):
@@ -259,10 +312,11 @@
                 if ci != payload["idx"] and TALLY_TEXT_RE.search(c):
                     found.append((n, raw))
                     break
-        elif kind == "other" and re.match(r"^ {0,3}\|", prev_raw):
+        elif kind == "other" and ROW_SHAPE_RE.match(prev_raw):
             if TALLY_TEXT_RE.search(raw) or "--selftest" in raw:
                 found.append((n, raw))
-        prev_raw = raw
+        if raw.strip():
+            prev_raw = raw
     return found
 
 
@@ -275,6 +329,37 @@
             and os.path.isfile(fp))
 
 
+def instrument_of(argv):
+    """v4 R11: the file path a bound argv runs — the word after the interpreter and
+    its `-I`/`-B` flags (the same skip `argv_ok` applies)."""
+    i = 1
+    while i < len(argv) and argv[0].startswith("python") and argv[i] in PY_FLAGS:
+        i += 1
+    return argv[i] if i < len(argv) else None
+
+
+def mutant_of(path, claimed):
+    """v4 R11 carve-out: `path` is a mutant of `claimed` — under a `fixtures` or
+    `mutants` directory and carrying the claimed instrument's basename (the lane's
+    `fixtures/mutants/<basename>` convention)."""
+    if not path or not claimed:
+        return False
+    segs = path.split("/")
+    return (("fixtures" in segs or "mutants" in segs)
+            and os.path.basename(path) == os.path.basename(claimed))
+
+
+def exit_contracts(row):
+    """v4 F5: the {(exit code): outcome token} pairs a row's `verdict map` cell
+    states, or {} when the cell names no pair (e.g. "unchanged from row …")."""
+    try:
+        vi = [header_key(c) for c in row["header"]].index("verdict map")
+    except ValueError:
+        return {}
+    vmap = row["cells"][vi] if len(row["cells"]) > vi else ""
+    return {int(m.group(1)): m.group(2) for m in VERDICT_PAIR_RE.finditer(vmap)}
+
+
 def span_kind(span, cells, rev, eidx):
     """Classify one backticked span of a self-test cell (R3, R7 L4):
     ('tally'|'digest'|'trunc'|'command'|'unparsed'/reason|'ignore')."""
@@ -453,7 +538,7 @@
     out = []
     counts = {"tally_pins": 0, "digest_pins": 0, "mismatches": 0,
               "unparsed": 0, "no_command": 0, "dropped": 0, "rebound": 0,
-              "duplicate": 0, "hidden": 0}
+              "duplicate": 0, "hidden": 0, "misattributed": 0}
     base_bind = {}
     base_bind_prefix = {}
     if baseline_text is not None:
@@ -486,6 +571,27 @@
         if n > 1:
             counts["duplicate"] += n - 1
             out.append("pin kind=row state=duplicate row=%r count=%d" % (name, n))
+    # v4 F5 (`w2/R48CritV3Junk1.md` §6): two rows binding one (prefix, argv) are
+    # two authorities for one command; their exit-code contracts must agree. Rows
+    # whose verdict map states no `code → token` pair (e.g. "unchanged from row …")
+    # are skipped, which is what keeps the four legitimate write-scope rows green.
+    contracts = {}
+    for row in parse_registry(text):
+        if row["state"] != "ok":
+            continue
+        pairs = exit_contracts(row)
+        if not pairs:
+            continue
+        for prefix, _pinned, words in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
+            if not words:
+                continue
+            prev = contracts.setdefault((prefix, tuple(words)), {})
+            for code, token in sorted(pairs.items()):
+                if code in prev and prev[code] != token:
+                    counts["duplicate"] += 1
+                    out.append("pin line=%d kind=row state=duplicate row=%r conflict=exit%d %s!=%s"
+                               % (row["line"], row["cells"][0], code, token, prev[code]))
+                prev[code] = token
     for n, raw in hidden_rows(text):
         counts["hidden"] += 1
         out.append("pin line=%d kind=row state=hidden row=%r" % (n, raw[:80]))
@@ -500,6 +606,11 @@
             continue
         cells, idx = row["cells"], row["idx"]
         st = cells[idx]
+        # v4 R11: the row's claimed instrument — the first file path of its ENTRY
+        # cell; None when the entry cell names no path.
+        entry_cell = cells[row["eidx"]] if len(cells) > row["eidx"] else ""
+        entry_paths = PATH_RE.findall(entry_cell)
+        claimed = entry_paths[0] if entry_paths else None
         # R3 / R7 L4: ASCII-strict span checks (a tally digitless pin is still
         # counted by the tally branch below).
         for m in SPAN_RE.finditer(st):
@@ -560,6 +671,15 @@
                 counts["no_command"] += 1
                 out.append("pin line=%d kind=tally prefix=%s state=no_command" % (line, prefix))
                 continue
+            # v4 R11 (closes D7): the bound argv must run the row's claimed
+            # instrument or a mutant of it. The command is not run — the pin is
+            # already fatal — but it still counts toward `tally_pins` above.
+            inst = instrument_of(words)
+            if inst != claimed and not mutant_of(inst, claimed):
+                counts["misattributed"] += 1
+                out.append("pin line=%d kind=tally prefix=%s state=misattributed claimed=%s bound=%s"
+                           % (line, prefix, claimed, inst))
+                continue
             key = tuple(words)
             if key not in cache:
                 cache[key] = run_cmd(words, root, scratch, timeout)
@@ -595,13 +715,15 @@
     met = (counts["mismatches"] == 0 and counts["unparsed"] == 0
            and counts["no_command"] == 0 and counts["dropped"] == 0
            and counts["rebound"] == 0 and counts["duplicate"] == 0
-           and counts["hidden"] == 0 and counts["tally_pins"] >= min_tally)
+           and counts["hidden"] == 0 and counts["misattributed"] == 0
+           and counts["tally_pins"] >= min_tally)
     out.append("PIN_CHECK=%s tally_pins=%d digest_pins=%d mismatches=%d unparsed=%d "
-               "no_command=%d dropped=%d rebound=%d duplicate=%d hidden=%d min_tally_pins=%d rev=%s baseline=%s"
+               "no_command=%d dropped=%d rebound=%d duplicate=%d hidden=%d misattributed=%d "
+               "min_tally_pins=%d rev=%s baseline=%s"
                % ("met" if met else "unmet", counts["tally_pins"], counts["digest_pins"],
                   counts["mismatches"], counts["unparsed"], counts["no_command"],
                   counts["dropped"], counts["rebound"], counts["duplicate"], counts["hidden"],
-                  min_tally, rev or "-",
+                  counts["misattributed"], min_tally, rev or "-",
                   "yes" if baseline_text is not None else "no"))
     return met, out
 
@@ -710,8 +832,10 @@
            "    print('TMP_SELFTEST pass=%d fail=%d' % (1 if ok else 0, 0 if ok else 1)); sys.exit(0 if ok else 1)\n")
 
 
-def row(selftest_cell, entry="`python3 tools/foo.py`", pinned="none"):
-    return "| foo | gate | %s | 0 ok | %s | %s | none | mori |\n" % (entry, selftest_cell, pinned)
+def row(selftest_cell, entry="`python3 tools/foo.py`", pinned="none", name="foo",
+        verdict="0 ok"):
+    return "| %s | gate | %s | %s | %s | %s | none | mori |\n" % (name, entry, verdict,
+                                                               selftest_cell, pinned)
 
 
 def selftest():
@@ -726,14 +850,23 @@
             f.write(SLOW)
         with open(os.path.join(root, "tools", "rev.py"), "w") as f:
             f.write(REVTOOL)
-        with open(os.path.join(root, "tools", "mut.py"), "w") as f:
-            f.write(MUT)
         with open(os.path.join(root, "tools", "tmp.py"), "w") as f:
             f.write(TMPTOOL)
+        # v4 R11 carve-out fixtures: a mutant of the claimed instrument lives under
+        # `fixtures/mutants/<basename>`; another basename under `fixtures/mutants`,
+        # or the right basename outside such a directory, is not a mutant of it.
+        for rel in (".ufo/waves/round-9/fixtures/mutants/foo.py",
+                    ".ufo/waves/round-9/fixtures/mutants/bar.py",
+                    ".ufo/waves/round-9/foo.py"):
+            p = os.path.join(root, *rel.split("/"))
+            os.makedirs(os.path.dirname(p), exist_ok=True)
+            with open(p, "w") as f:
+                f.write(MUT)
         digest = sha256_file(os.path.join(root, "tools", "foo.py"))
         good = "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0`"
-        mut_ok = good + "; the mutant `tools/mut.py` reads `FOO_SELFTEST pass=2 fail=1` rc 1"
-        mut_bad = good + "; the mutant `tools/mut.py` reads `FOO_SELFTEST pass=3 fail=0`"
+        mutant_rel = ".ufo/waves/round-9/fixtures/mutants/foo.py"
+        mut_ok = good + "; the mutant `%s` reads `FOO_SELFTEST pass=2 fail=1` rc 1" % mutant_rel
+        mut_bad = good + "; the mutant `%s` reads `FOO_SELFTEST pass=3 fail=0`" % mutant_rel
         cases = [
             ("honest", HDR + row(good), 1, True, None),
             ("stale_tally", HDR + row("`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`"), 1, False, "mismatch"),
@@ -859,8 +992,10 @@
         cases.append(("r7_argv_trailing_args_rejected", HDR + row("`python3 tools/foo.py --selftest extra` → " + stale, entry="no command here"),
                       1, False, "no_command"))
         # R7 L2: `\\|` is a literal backslash followed by a real separator; the row stays 8 cells.
+        # v4 R11: the entry cell names the instrument the row runs.
         cases.append(("r7_escaped_double_backslash_pipe", HDR +
-                      "| foo | gate | a\\\\| 0 ok | `python3 tools/foo.py --selftest` → "
+                      "| foo | gate | `python3 tools/foo.py --rev <rev>` a\\\\| 0 ok | "
+                      "`python3 tools/foo.py --selftest` → "
                       "`FOO_SELFTEST pass=3 fail=0` | none | none | mori |\n", 1, True, None))
         # R10 (round-48 CritJunkClasses D1): a digest of another file named elsewhere in the row.
         slow_digest = sha256_file(os.path.join(root, "tools", "slow.py"))
@@ -881,6 +1016,69 @@
         # R9c (D18): a tally written outside backticks in the self-test cell.
         cases.append(("r9c_tally_outside_backticks", HDR + row(good + "; also FOO_SELFTEST pass=999 fail=0"),
                       1, False, "unparsed"))
+        # ---- v4 arms: each rule below carries a red arm and an honest green arm.
+        # F1 adjacency (R48CritV3Junk1 §1, §7): R9b's "directly under a row" is the
+        # nearest preceding NON-BLANK line.
+        cases.append(("f1_blankline_continuation_tally", HDR + row(good) +
+                      "\n\n\u2192 the observed text was `FOO_SELFTEST pass=999 fail=0`\n", 1, False, "hidden"))
+        cases.append(("f1_honest_prose_after_blank", HDR + row(good) +
+                      "\n\nA prose paragraph that pins nothing.\n", 1, True, None))
+        cases.append(("f1_adjacency_is_nearest_nonblank", HDR + row(good) +
+                      "\n\nA prose line.\n\nA later line quotes `FOO_SELFTEST pass=999 fail=0` in prose.\n",
+                      1, True, None))
+        # F2 header normalisation (§2): NFKC plus zero-width deletion.
+        nb = HDR.replace("self-test", "self\u00a0test", 1)
+        cases.append(("f2_laundered_header_row_measured", nb + row(
+            "`python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=2 fail=0`"), 1, False, "mismatch"))
+        cases.append(("f2_laundered_header_zwsp_token", nb + row(
+            "`python3 tools/foo.py --selftest` → `FOO_\u200bSELFTEST pass=999 fail=0`"), 1, False, "unparsed"))
+        cases.append(("f2_laundered_header_honest_row", nb + row(good), 1, True, None))
+        cases.append(("f2_zwsp_in_header_cell", HDR.replace("self-test", "self-\u200btest", 1) + row(good),
+                      1, True, None))
+        # F3 row shape (§3, §4): any indentation is a row shape.
+        cases.append(("f3_tab_indented_fenced_row", "```\n\t| foo | gate | `python3 tools/foo.py` | 0 ok | "
+                      "`FOO_SELFTEST pass=999 fail=0` | none | none | mori |\n```\n" + HDR + row(good),
+                      1, False, "hidden"))
+        cases.append(("f3_four_space_row", "    | foo | gate | `python3 tools/foo.py` | 0 ok | "
+                      "`FOO_SELFTEST pass=999 fail=0` | none | none | mori |\n" + HDR + row(good),
+                      1, False, "hidden"))
+        cases.append(("f3_indented_examples_without_token",
+                      "    | an | indented | example | row |\n\n```\n\t| a | tab | example | row |\n```\n"
+                      + HDR + row(good), 1, True, None))
+        # F4 HTML table markup (§8): a `<tr`/`<td` line is a row shape.
+        cases.append(("f4_html_row_with_pin", "<table>\n<tr><td>html</td><td>gate</td><td>"
+                      "<code>python3 tools/foo.py --selftest</code> \u2192 "
+                      "<code>FOO_SELFTEST pass=999 fail=0</code></td></tr>\n</table>\n" + HDR + row(good),
+                      1, False, "hidden"))
+        cases.append(("f4_html_without_pin", "<!-- an honest note: nothing pinned here -->\n\n<table>\n"
+                      "<tr><td>note</td><td>plain prose cell</td></tr>\n</table>\n" + HDR + row(good),
+                      1, True, None))
+        # F5 exit contracts (§6): one (prefix, argv), one contract.
+        f5_a = row(good, name="pn a", verdict="0 \u2192 `PN_RUN=met` \u00b7 1 \u2192 `PN_RUN=unmet`")
+        f5_b = row(good, name="pn b", verdict="0 \u2192 `PN_RUN=met` \u00b7 1 \u2192 `PN_SETUP`")
+        f5_c = row(good, name="pn c", verdict="0 \u2192 `PN_RUN=met` \u00b7 1 \u2192 `PN_RUN=unmet`")
+        cases.append(("f5_conflicting_exit_contracts", HDR + f5_a + f5_b, 2, False, "duplicate"))
+        cases.append(("f5_agreeing_exit_contracts", HDR + f5_a + f5_c, 2, True, None))
+        cases.append(("f5_unstated_contract_skipped",
+                      HDR + f5_a + row(good, name="pn d", verdict="unchanged from row `pn a`"),
+                      2, True, None))
+        # R11 misattribution (R48ExecD7 §4, closes D7).
+        cases.append(("r11_misattributed_instrument", HDR + row(
+            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`"), 1, False, "misattributed"))
+        cases.append(("r11_entry_cell_without_instrument", HDR + row(
+            good, entry="the drift probe (no path named)"), 1, False, "misattributed"))
+        cases.append(("r11_second_entry_path_not_claimed", HDR + row(
+            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`",
+            entry="`python3 tools/foo.py --rev <rev>` (`--tool` default `tools/lc.py`)"), 1, False, "misattributed"))
+        cases.append(("r11_mutant_other_basename_rejected", HDR + row(
+            good + "; the fixture `.ufo/waves/round-9/fixtures/mutants/bar.py` reads "
+            "`FOO_SELFTEST pass=2 fail=1` rc 1"), 2, False, "misattributed"))
+        cases.append(("r11_mutant_right_basename_wrong_directory", HDR + row(
+            good + "; the fixture `.ufo/waves/round-9/foo.py` reads `FOO_SELFTEST pass=2 fail=1` rc 1"),
+            2, False, "misattributed"))
+        cases.append(("r11_same_instrument_green", HDR + row(
+            good, entry="`python3 tools/foo.py --rev <rev>` (the audit reads `tools/slow.py` in prose)"),
+            1, True, None))
         for name, text, floor, want_met, want_state in cases:
             scratch = tempfile.mkdtemp(prefix="c-", dir=base)
             text, btext = text if isinstance(text, tuple) else (text, None)
````

## 6. Rule attribution on frozen variants (observed, not inferred)

Ran the candidate on three of the counter's variants (built with `count-c1.py`'s own functions from
`git show b3e3453d:SKILL.md`), so which rule rejects each one is read off the verdict:

```
$ TMPDIR=$PWD/.scratch/r49-Mo49ExecImplA python3 -I -B .scratch/r49-Mo49ExecImplA/probe-attribution.py
== N1 rc=1
   pin line=981 kind=row state=hidden row='<!-- | r49 html comment | gate | `python3 tools/mori-pin-check.py --rev <rev>` |'
   PIN_CHECK=unmet … hidden=1 misattributed=0 …
== N5 rc=1
   pin line=983 kind=row state=duplicate row='r49 pin reconciler second authority' conflict=exit1 PIN_CHECK_SETUP!=PIN_CHECK=unmet
   PIN_CHECK=unmet … duplicate=1 hidden=0 misattributed=0 …
== N9 rc=1
   pin line=983 kind=tally prefix=PIN_CHECK_SELFTEST state=misattributed claimed=tools/mori-gate-registry.py bound=tools/mori-pin-check.py
   PIN_CHECK=unmet … duplicate=0 hidden=0 misattributed=1 …
exit=0
```

So N1 is F1 (`hidden` on the comment line after a blank line), N5 is F5 (conflicting exit-1
contract for one `(prefix, argv)`), N9 is R11 (claimed registry instrument, bound reconciler). The
remaining variants are rejected by the shapes their sources name; their per-variant output is not
retained here (each needs a full-registry run) — the counter row `got=unmet rc=1` is the evidence.

## 7. Real registry at the entering tip

```
$ TMPDIR=$PWD/.scratch/r49-Mo49ExecImplA python3 -I -B .scratch/r49-Mo49ExecImplA/mori-pin-check.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --repo . --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 baseline=yes
exit=0
```

Same 31 tally pins and 8 digest pins as the entering tool, with all six v4 rules active: no false
red on the real registry (31 binds, incl. the two mutant binds of rows 190/192 at
`.ufo/waves/round-45/fixtures/mutants/…`, row 912's prose naming the reconciler, and the four
`… — write scope superseded` rows whose verdict maps state no `code → token` pair).
Receipt `.scratch/r49-Mo49ExecImplA/real-b3e3453d.out`.

The bind census behind that sentence (the candidate's own `parse_registry`/`pin_commands` over
`git show b3e3453d:SKILL.md`, R11 active, printing only binds whose instrument differs from the
entry cell's first path):

```
line=190 row='r45 ledger counter (C1)' prefix=C1_SELFTEST claimed=.ufo/waves/round-45/count-c1.py bound=.ufo/waves/round-45/fixtures/mutants/count-c1.py mutant=True
line=192 row='r45 corpus coverage (C3)' prefix=C3_SELFTEST claimed=.ufo/waves/round-45/count-c3.py bound=.ufo/waves/round-45/fixtures/mutants/count-c3.py mutant=True
binds=31 no_command=0 non_identical=2
```

So exactly two binds need the mutant carve-out and both are `fixtures/mutants/<basename>` of their
claimed instrument — R11 reds nothing the registry legitimately states.

## 8. Comparison with the merged witness (made only after the candidate was finished)

Witness: `controls/tool-r48-merged-witness.py`, sha256
`c30ab6232893d984d1440784b6ce962d7c987c6d5538db0ead2f458a8ea1c9f0`, 1020 lines, selftest
`PIN_CHECK_SELFTEST pass=65 fail=0` (exit 0). `diff -u` of the two is
`.scratch/r49-Mo49ExecImplA/v4-vs-witness.diff`; the equivalence probe is
`.scratch/r49-Mo49ExecImplA/probe-witness.py` → `probe-witness.out`.

| # | difference | kind | probe | result |
|---|---|---|---|---|
| D1 | F5's `verdict map` column lookup: v4 uses the F2-normalised header key (`header_key`), the witness uses `c.lower()` on the raw cell | **behavioural** | a table whose column header is `verdict\u00a0map` with two rows binding one `(prefix, argv)` and conflicting exit-1 tokens | v4 `PIN_CHECK=unmet … duplicate=1` rc 1 with `conflict=exit1 PN_SETUP!=PN=unmet`; witness `PIN_CHECK=met … duplicate=0` rc 0 (the row is skipped) |
| D2 | selftest arm set: 81 arms vs 65 (16 new F1/F2/F3/F4/F5/R11 arms, none removed) | behavioural only inside `--selftest` | `--selftest` on both | v4 `pass=81 fail=0` rc 0; witness `pass=65 fail=0` rc 0; arm-name diff: 16 added, 0 lost |
| D3 | helper extraction (`header_key`, `ROW_SHAPE_RE`/`HTML_ROW_RE`/`ZERO_WIDTH_CHARS`/`VERDICT_PAIR_RE`, `exit_contracts`, `instrument_of`, `mutant_of`), `row()` gains `name`/`verdict`, docstring wording, one-line vs two-line `out.append` format strings | cosmetic (identical output text) | the same synthetic registry per rule shape run through both `--root` | outputs byte-identical (`identical=True`) for f1 blank-line continuation, f2 NBSP header, f3 tab-fenced row, f4 HTML row, f5 conflicting contract, R11 misattributed; only the D1 fixture differs |
| D4 | fixtures: v4 keeps no `tools/mut.py` (unused after the mutant carve-out), witness keeps its own fixture layout | cosmetic (selftest temp tree only) | D2 above (same arm outcomes) | no arm outcome differs |

Probe output (`.scratch/r49-Mo49ExecImplA/probe-witness.out`):

```
== f1_blankline_continuation  identical=True  rc_candidate=1 rc_witness=1
== f2_nbsp_header  identical=True  rc_candidate=0 rc_witness=0
== f3_tab_fenced  identical=True  rc_candidate=1 rc_witness=1
== f4_html_row  identical=True  rc_candidate=1 rc_witness=1
== f5_conflict  identical=True  rc_candidate=1 rc_witness=1
== r11_misattributed  identical=True  rc_candidate=1 rc_witness=1
== d1_nbsp_verdict_map_header  identical=False  rc_candidate=1 rc_witness=0
--- candidate
pin line=4 kind=row state=duplicate row='pn b' conflict=exit1 PN_SETUP!=PN=unmet
…
PIN_CHECK=unmet … duplicate=1 hidden=0 misattributed=0 …
--- witness
…
PIN_CHECK=met … duplicate=0 hidden=0 misattributed=0 …
PROBE differ=1 cases=7
exit=0
```

So the candidate and the witness are behaviourally identical on every frozen variant shape and on
the real registry, and differ in exactly one reachable case (D1, where v4 reads the column header
through the same normalisation F2 applies to the row-recognition header).

## 9. Limits and risks (stated, not re-scored)

1. **Landing moves the self-referential pin (integration, HIGH).** v4 prints
   `PIN_CHECK_SELFTEST pass=81 fail=0`; `SKILL.md:938` pins `pass=60 fail=0`. Because the reconciler
   runs the **measured tree's** tool, landing the bytes without editing that pin in the same commit
   turns its own row `mismatch` (the same consequence `R48ExecD7.md` §9 states for `pass=65`).
2. **F1 cost.** Any non-blank line under a table row that quotes a tally token or `--selftest` is
   now `hidden` — including honest prose. Measured cost at the entering tip: 0 newly flagged lines
   (real registry `hidden=0`).
3. **F3 cost.** An indented or fenced example row carrying a token is fatal — R2's stated intent,
   but it now also covers examples a reader would call an example. Measured: 0 such lines at
   `b3e3453d` (`grep -nE '^[[:space:]]+\|'` → no match; `^\t` → no match).
4. **F4 cost.** A `<tr`/`<td` line carrying a token or `--selftest` is fatal. Measured: 0 HTML row
   lines at `b3e3453d`.
5. **F5 limit.** It compares *stated* contracts only: a junk row that restates the authority row's
   contract verbatim is consistent; a row that legitimately changes a contract for an
   already-registered command is red until it restates the old one (the intent, per
   `R48CritV3Junk1.md` §6).
6. **R11 limits** (`R48ExecD7.md` §8, all still open): a committed decoy at
   `fixtures/mutants/<claimed-basename>` passes by construction; only the *first* entry-cell path is
   the claim; a row with no pin is unverified; paths are compared, not bytes; a misattributed pin is
   not executed, so its tally is never measured (it is fatal on its own).
7. **Predicate limits** remain the contract's: the variants are the classes rounds 47-48 found, not
   the class of all junk; K2-K8 stay routed; the counter does not run the tool's own `--selftest`.
8. **UNVERIFIED:** the false-red audit of F1-F5/R11 against *earlier* SKILL.md revisions (the
   contract lists it as closure work, not this seat's brief). I measured `b3e3453d` only, plus the
   synthetic trees in the selftest and the probes. **UNVERIFIED:** the counter's own selftest
   (`C1_SELFTEST pass=44 fail=0` at the freeze) was not re-run by this seat; the frozen receipt is
   used as-is. No host-reading command (journalctl, systemctl, `/proc`, `/sys`) was run, so no host
   observation is claimed.

## 10. Tooling

Nothing installed or upgraded (no pacman, no uv tool, no binary fetch). Only `python3` 3.14.8 and
read-only `git show/rev-parse/status` were used.

## Findings

- **HIGH — integration, `SKILL.md:938`:** landing v4 without moving the reconciler's own pin from
  `PIN_CHECK_SELFTEST pass=60 fail=0` to `pass=81 fail=0` in the same commit makes the landed gate
  red on itself (measured tally `pass=81 fail=0`; mechanism is the measured tree's own tool, as
  `R48ExecD7.md` §9 states).
- **MED — `tools/mori-pin-check.py` (v4 `hidden_rows`, F1):** a non-blank prose line directly under a
  table row that quotes a tally token or `--selftest` is now fatal, so future registry prose must not
  sit under a table. Cost at `b3e3453d`: 0 lines (`hidden=0` in the real run), so this is a forward
  constraint, not a current defect.
- **MED — `tools/mori-pin-check.py` (F5, `exit_contracts`):** the rule sees only stated
  `code → token` pairs; a second authority that restates the registered contract verbatim passes,
  and a legitimate contract change is red until the old contract is restated. Shape inherited from
  `R48CritV3Junk1.md` §6 (limit), implemented as stated.
- **MED — `tools/mori-pin-check.py` (R11 `mutant_of`):** the carve-out accepts any
  `fixtures`/`mutants` path with the claimed basename, so a committed decoy instrument that echoes
  the pinned tally is green; R11 closes the registry-text class (D7) only. Inherited from
  `R48ExecD7.md` §8.1, unchanged.
- **LOW — `tools/mori-pin-check.py` (F4 `HTML_ROW_RE`):** HTML table markup is now a row shape for
  R2, so a *documentation* example in SKILL.md written as `<tr><td>…--selftest…</td></tr>` would be
  fatal; measured 0 such lines at `b3e3453d`.
- **LOW — candidate vs witness (D1, `exit_contracts`):** v4 enforces F5 on a table whose
  `verdict map` header is laundered with an NBSP (the witness skips it); reachable only by a variant
  outside the frozen counter, so it cannot change C1 either way. Deliberate: F2's normalisation is
  the header key everywhere the tool reads a column.

Report: .ufo/waves/round-49/w1/Mo49ExecImplA.md
