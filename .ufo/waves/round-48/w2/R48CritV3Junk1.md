# R48CritV3Junk1 — new false-green classes against the LANDED v3 (round 48, w2, C1)

**Attacked:** `tools/mori-pin-check.py` as landed at
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (sha256
`85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`, byte-identical to
`git show e4dfff32:tools/mori-pin-check.py`) reading `SKILL.md` at the same revision (979 lines,
sha256 `62602b2e438a2fe572b48055e7c62cf169d94f2fa5afb14bb8e3262212e3a77d`). Fourteen new junk
edits: eight primary probes, one per assigned class (`v1`, `v2`, `v3a`, `v4`, `v5`, `v6`, `v7`,
`v8`), and six sub-probes that isolate one mechanism each (`v1b`, `v2b`, `v2c`, `v3b`, `v4b`,
`v5b`). No file under `tools/`, `corpus/`, `SKILL.md`, `SOURCES.md`, `LOG.md`, `SCORECARD.md` or
the freeze was touched; every edit exists only as a scratch `SKILL.md` variant.

**Verdict: BREAKS.** Seven of the fourteen probes print `PIN_CHECK=met` and exit 0 while the
registry carries a claim the tool never reads — a false pin (`pass=999 fail=0`), a false observed
value (`fail=3` next to a green `fail=0`), or a second, contradictory exit contract for a pin that
is already registered. The class is **"claims outside the one row shape R2 recognises"**: v3's own
doctrine (R2: *a pin a checker would not see is `hidden`, fatal*, including inside fences) is
implemented for a row that starts with up to three spaces and a pipe, and for nothing else —
tabs, four-or-more spaces, a row inline in an HTML comment, and HTML table markup all keep their
claim. One survivor is a different class: **duplicate authority** (two rows, one command, one
prefix, two exit contracts; the `duplicate` counter keys on the row name and R4 keys on
`(name, prefix, ordinal)`, so a new name defeats both).

The frozen predicate P-C1 is **not** falsified by any of this: the tool is `met` at the tip either
way, so C1 cannot distinguish these registries. Per the contract's named limit I report the
survivors as **limits**, not as a re-scoring.

Seven probes are **caught** and their receipts are below, because they show which of v3's rules do
hold in their own channel: a comment *block* around a junk table (its header line is still a
header, so the row is parsed and the false pin mismatches), an ASCII token under a laundered header
(R2 `hidden`), a tab-separated row inside a table (cell-count `unparsed`), an NBSP between prefix
and count (the span is a tally and mismatches), a four-space row *inside* a table (parsed), and a
gate table under a list item at 2 and 4 spaces (parsed, false pin mismatches).

---

## Method (one CLI, identical to `count-c1.py`'s `run_tool`)

Every measurement is this command, run from the lane root with `TMPDIR` inside this seat's scratch:

```
TMPDIR=<scratch> python3 -I -B <tool> --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin --min-tally-pins 26 \
  --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill <variant.md>
```

Scratch: `.scratch/r48w2-R48CritV3Junk1/` (`base-SKILL.md`, `variants/`, `controls/`, `fixes/`,
`results/`; driver `run_one.sh`, generators `gen.py` and `gen_fixes.py`). Each variant is
`base-SKILL.md` plus exactly one edit; the diffs below are `diff -U0` against that file and apply
with `patch -p1` (`a/SKILL.md` → `b/SKILL.md`).

Unedited base, same command (exit 0) — the control every survivor must be compared against:

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

## Results

| # | class (assigned) | probe | verdict | counter |
|---|---|---|---|---|
| 1 | HTML comments around rows | `v1_html_comment` — one row inline in `<!-- … -->`, after a blank line | **met, exit 0 — SURVIVOR** | `hidden=0` |
| 1 | " | `v1b_comment_block` — `<!--` on its own line, junk table, `-->` | unmet, exit 1 — caught | `mismatches=1`, `tally_pins=32` |
| 2 | zero-width / NBSP | `v2_zwsp_header_prefix` — U+00A0 in the header cell **and** U+200B inside the pin token | **met, exit 0 — SURVIVOR** | `hidden=0 unparsed=0` |
| 2 | " | `v2b_nbsp_header_only` — laundered header, ASCII token kept | unmet, exit 1 — caught | `hidden=1` |
| 2 | " | `v2c_nbsp_separator` — NBSP between prefix and `pass=` | unmet, exit 1 — caught | `mismatches=1`, `tally_pins=32` |
| 3 | tab-separated cells | `v3a_tab_cells` — cells separated by tabs inside the round-48 table | unmet, exit 1 — caught | `unparsed=1` (`cells=1 header=8`) |
| 3 | " | `v3b_tab_fence` — tab-indented pipe row inside a fence | **met, exit 0 — SURVIVOR** | `hidden=0` |
| 4 | rows with 4+ leading spaces | `v4_fourspace` — 4-space row after a blank line | **met, exit 0 — SURVIVOR** | `hidden=0` |
| 4 | " | `v4b_fourspace_in_table` — same row, header active | unmet, exit 1 — caught | `mismatches=1`, `tally_pins=32` |
| 5 | gate table under a list item | `v5_list_item` — table 2 spaces under `- item` | unmet, exit 1 — caught | `mismatches=1`, `tally_pins=32` |
| 5 | " | `v5b_list_item_deep` — table 4 spaces under `- item` | unmet, exit 1 — caught | `mismatches=1`, `tally_pins=32` |
| 6 | duplicate row, different name, same prefix | `v6_dup_authority` — second row for `PIN_CHECK_SELFTEST` + the same argv, new name, contradicting exit contract | **met, exit 0 — SURVIVOR** | `duplicate=0 rebound=0`, `tally_pins=32` |
| 7 | `fail=0` in prose, `fail=3` observed split across lines | `v7_split_tally` — command, no pin; prose `pass=60 fail=0` in a cell, blank line, continuation recording `pass=60` / `fail=3` | **met, exit 0 — SURVIVOR** | `hidden=0`, `tally_pins=31` |
| 8 | (free) HTML table markup | `v8_html_table` — the same row as `<tr><td>…` | **met, exit 0 — SURVIVOR** | `hidden=0` |

Seven survivors, seven caught. Nothing below repeats J1–J8 (`count-c1.py`), FG1–FG5/O1
(round-47 `w2/CritV2Junk.md`) or D1–D18 (round-48 `w1/CritJunkClasses.md`): every one of the seven
is a *new row shape or a new identity channel*, not a new spelling of an old one.

---

## 1 — HTML comment around a row (SURVIVOR)

Falsified claim: a raw-bytes reader of the registry sees a pin `PIN_CHECK_SELFTEST pass=999 fail=0`
that the tool never counts (`tally_pins` stays 31). Rendering hides the comment, so the harm is to
any reader of the source — which is the same harm class R2 already accepts as fatal for fenced
rows (`J5`, `D4`).

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,2 @@
+
+<!-- | r48 html comment | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `PIN_CHECK_SELFTEST pass=999 fail=0` | none | none | mori | -->
```

Measured (`results/v1_html_comment.out`, exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

Why it evades: `split_cells` returns `None` for a line that does not start with `|`, so the line is
`other`; R9b fires only when `prev_raw` matches `^ {0,3}\|`, and the blank line the comment follows
sets `prev_raw = ""`. R2's `candidate` branch never sees it either (it is not row-shaped).

The same class *with* the comment markers on their own lines is caught — `v1b_comment_block`,
exit 1, `mismatches=1`: the header line inside the comment is recognised, the row is parsed and the
false pin is compared. So the hole is exactly "one blank line between the row and the claim".

**Smallest rule that kills it** (`fixes/f1_adjacency.py`, 2 lines): R9b's "directly under a table
row" must mean the nearest **non-blank** line.

```diff
--- a/tools/mori-pin-check.py
+++ b/tools/mori-pin-check.py
@@ -262,7 +262,8 @@
         elif kind == "other" and re.match(r"^ {0,3}\|", prev_raw):
             if TALLY_TEXT_RE.search(raw) or "--selftest" in raw:
                 found.append((n, raw))
-        prev_raw = raw
+        if raw.strip():
+            prev_raw = raw
     return found
```

Measured: `f1_adjacency` on base → `PIN_CHECK=met` exit 0; on `v1_html_comment` → `PIN_CHECK=unmet`
exit 1 with `pin line=981 kind=row state=hidden row='<!-- | r48 html comment | …'`. Cost: honest
prose that quotes a tally on the first line after a table would now be `hidden`. I simulated the
change over all 979 lines of the real registry: **0** lines newly flagged.

## 2 — zero-width space in the token + NBSP in the header (SURVIVOR)

Falsified claim: a rendered table whose header reads `self test` and whose row claims
`PIN_CHECK_SELFTEST pass=999 fail=0` (the U+200B between `CHECK_` and `SELFTEST` is invisible; the
header's U+00A0 renders as a space). The tool reads neither the header nor the token.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,4 @@
+
+| name | kind | entry | verdict map | self test | pinned values | write scope | owner |
+|---|---|---|---|---|---|---|---|
+| r48 zwsp | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `PIN_CHECK_​SELFTEST pass=999 fail=0` | none | none | mori |
```

The header cell is `self\u00a0test` (U+00A0, bytes `302 240`) and the pin token is
`PIN_CHECK_\u200bSELFTEST` (U+200B, bytes `342 200 213`) — verified with `od -c` on
`variants/v2_zwsp_header_prefix.md` lines 981 and 983. Measured (exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

Why it evades: `scan_lines` compares `c.lower()` against `HEADER_CELLS`, so `self\u00a0test` is not
a header; the row becomes a `candidate`. R2 then needs an ASCII `[A-Z][A-Z0-9_]*SELFTEST` token in
the raw line, and the U+200B breaks it — `HIDDEN_TOKEN_RE` cannot span the ZWSP, and the row
carries no `--selftest` text (the command lives in the entry cell without the flag). Both
launderings are required, and each is individually covered: `v2b_nbsp_header_only` (laundered
header, ASCII token) is caught, `hidden=1`, exit 1; a ZWSP token under a *recognised* header is
caught by R3 as `state=unparsed reason=non-ascii-token`.

**2c (sub-probe, measured)** `v2c_nbsp_separator` — `PIN_CHECK_SELFTEST\u00a0pass=999 fail=0`
inside an honest, recognised cell — is **caught**, exit 1, `mismatches=1`, `tally_pins=32`,
`unparsed=0`, with
`pin line=983 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=999 fail=0' observed='pass=60 fail=0' rc=0`.
So the NBSP there is *not* a laundering: `TALLY_PIN_RE` matches the prefix and takes `(.*)` across
the NBSP, the span binds to the preceding command, and the false count is compared. (My static
reading — that R3's `tok0` would return `unparsed` — was wrong: the tally branch runs first, which
is stronger, because the pin is then actually measured.) NBSP is therefore only safe *inside* the
token, where it is invisible and where R2 cannot see it either (§2).

**Smallest rule that kills it** (`fixes/f2_nfkc_header.py`): R1 recognises the header cell after
NFKC and deletion of the zero-width format characters — the same normalisation intent as R1's
"case-insensitively", one step further.

```diff
--- a/tools/mori-pin-check.py
+++ b/tools/mori-pin-check.py
@@ -198,7 +198,10 @@
             header = None
             yield n, "other", {"raw": line}
             continue
-        low = [c.lower() for c in cells]
+        low = [unicodedata.normalize("NFKC", c)
+               .replace("\u200b", "").replace("\u200c", "")
+               .replace("\u200d", "").replace("\ufeff", "").lower()
+               for c in cells]
         if any(c in HEADER_CELLS for c in low):
```

Measured: `f2_nfkc_header` on base → `met` exit 0; on `v2_zwsp_header_prefix` → `unmet` exit 1 with
`pin line=983 kind=span state=unparsed reason=non-ascii-token span='PIN_CHECK_\u200bSELFTEST pass=999 fail=0'`
(the header now parses, so R3's existing span rule sees the token). Cost on the real registry: none
— every header cell is ASCII.

## 3 — tab-separated cells / a tab-indented row (SURVIVOR: the tab-indented row)

`v3a_tab_cells` (cells separated by tabs, no pipes) is **caught**: `unparsed=1`, `cells=1 header=8`,
exit 1 — the row keeps its ASCII `SELFTEST` token, so the cell-count `unparsed` branch counts it.

The tab that survives is an *indent*: a pipe row whose first character is a tab, inside a fence.
R2's fence exemption is implemented as `^ {0,3}\|`, so a tab defeats it, while the unindented
fenced twin is caught (that is `J5`/`D4`'s class, via R2's `fence_body` branch).

````diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,4 @@
+
+```
+	| r48 tab fence | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `PIN_CHECK_SELFTEST pass=999 fail=0` | none | none | mori |
+```
````

Measured (exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

This is a visible claim: it renders as a literal code block inside the fence. Why it evades:
`hidden_rows` tests `re.match(r"^ {0,3}\|", raw)` for `fence_body` lines, and `\t|` does not match;
`parse_registry` skips fence bodies by design.

## 4 — four leading spaces (SURVIVOR outside a table; caught inside one)

Same mechanism as §3 without a fence. Outside a table the line is a `candidate` whose shape fails
`^ {0,3}\|`; inside a table `split_cells` strips the line, so the row is parsed and the false pin
mismatches (`v4b_fourspace_in_table`, `mismatches=1`, exit 1).

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,2 @@
+
+    | r48 four space | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `PIN_CHECK_SELFTEST pass=999 fail=0` | none | none | mori |
```

Measured (exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

It renders as an indented code block, i.e. as a receipt a reader can quote.

**Smallest rule that kills §3 and §4** (`fixes/f3_rowshape_indent.py`): R2's row shape is *any*
indentation, not 0–3 spaces (both occurrences, including R9b's `prev_raw` test).

```diff
--- a/tools/mori-pin-check.py
+++ b/tools/mori-pin-check.py
@@ -250,7 +250,7 @@
-        row_shaped = bool(re.match(r"^ {0,3}\|", raw))
+        row_shaped = bool(re.match(r"^\s*\|", raw))
@@ -259,7 +259,7 @@
-        elif kind == "other" and re.match(r"^ {0,3}\|", prev_raw):
+        elif kind == "other" and re.match(r"^\s*\|", prev_raw):
```

Measured: `f3_rowshape_indent` on base → `met` exit 0; on `v3b_tab_fence` → `unmet` exit 1
(`state=hidden`, `row='\t| r48 tab fence | …'`); on `v4_fourspace` → `unmet` exit 1
(`state=hidden`, `row='    | r48 four space | …'`). Cost: a fenced or indented example row that
carries a tally token or `--selftest` becomes fatal — which is R2's stated intent. The real
registry has no such line (`grep -nE '^[[:space:]]+\|[^\n]*(SELFTEST|--selftest)'` → no match;
`grep -nP '^\t+\|'` → no match).

## 5 — gate table under a list item (CAUGHT)

Both indentations are parsed and rejected: `mismatches=1`, `tally_pins=32`, exit 1, with

```
pin line=985 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=999 fail=0' observed='pass=60 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
```

`split_cells` strips the line before testing for `|`, so list nesting (2 or 4 spaces, the latter of
which renders as code inside the list item) is invisible to the parser and the claim is still
checked. **No rule needed.** This is the one assigned class that v3 closes outright.

## 6 — duplicate row, different name, same prefix (SURVIVOR)

Falsified claim: a *second authority* for a pin that is already registered — the row binds the same
command (`python3 tools/mori-pin-check.py --selftest`) and the same true text
(`PIN_CHECK_SELFTEST pass=60 fail=0`) as SKILL.md:938, but its verdict-map cell says exit 1 is
`PIN_CHECK_SETUP`, "a red run is an environment error, never a finding", where the registered row
says exit 1 is `PIN_CHECK=unmet`. A reader who takes the new row as the authority reads a
contradiction into the same instrument, and nothing in the tool objects.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,4 @@
+
+| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
+|---|---|---|---|---|---|---|---|
+| r48 pin reconciler second authority | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0 → `PIN_CHECK=met` · 1 → `PIN_CHECK_SETUP` (a red run is an environment error, never a finding) · 2 → `PIN_CHECK_SETUP` | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0` | none | none | mori |
```

Measured (exit 0):

```
PIN_CHECK=met tally_pins=32 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

Why it evades: `duplicate` counts **row names**; R4 keys on `(name, prefix, ordinal)` — a new name
is outside both. The pin itself is genuinely true, so no tally rule can see the contradiction: the
falsity lives in the verdict map, a cell no rule reads. (D7's known limit is the *entry-vs-bound*
mismatch; this is *two rows, one command, two contracts*.)

**Smallest rule that kills it** (`fixes/f5_exit_contract.py`): R11 — two rows that bind one
`(prefix, argv)` are two authorities for one command, and their exit-code contracts must agree
(exit-code → outcome token, parsed from the `verdict map` cell).

```diff
--- a/tools/mori-pin-check.py
+++ b/tools/mori-pin-check.py
@@ -486,6 +486,33 @@
         if n > 1:
             counts["duplicate"] += n - 1
             out.append("pin kind=row state=duplicate row=%r count=%d" % (name, n))
+    # R11 (round-48 w2 CritV3Junk1): two rows binding one (prefix, argv) are two
+    # authorities for one command; their exit-code contracts must agree.
+    contracts = {}
+    for row in parse_registry(text):
+        if row["state"] != "ok":
+            continue
+        try:
+            vi = [c.lower() for c in row["header"]].index("verdict map")
+        except ValueError:
+            continue
+        vmap = row["cells"][vi] if len(row["cells"]) > vi else ""
+        pairs = {int(m.group(1)): m.group(2) for m in re.finditer(
+            r"\b([012])\s*\u2192\s*`?([A-Z][A-Z0-9_]*(?:=(?:met|unmet|clean|dirty))?)", vmap)}
+        if not pairs:
+            continue
+        for prefix, _pinned, words in pin_commands(row["cells"], row["idx"], rev, row["eidx"]):
+            if not words:
+                continue
+            key = (prefix, tuple(words))
+            prev = contracts.setdefault(key, {})
+            for code, token in sorted(pairs.items()):
+                if code in prev and prev[code] != token:
+                    counts["duplicate"] += 1
+                    out.append("pin line=%d kind=row state=duplicate row=%r "
+                               "conflict=exit%d %s!=%s"
+                               % (row["line"], row["cells"][0], code, token, prev[code]))
+                prev[code] = token
```

Measured: `f5_exit_contract` on base → `met` exit 0 (the four legitimate shared
`(prefix, argv)` pairs at SKILL.md:183/193, 184/194, 185/195, 186/196 carry no `code → token`
pairs in their "unchanged from row …" cells, so they are skipped); on `v6_dup_authority` →
`unmet` exit 1 with
`pin line=983 kind=row state=duplicate row='r48 pin reconciler second authority' conflict=exit1 PIN_CHECK_SETUP!=PIN_CHECK=unmet`.
Cost: a row that legitimately *changes* an exit contract for an already-registered command is now
red until it restates the old contract — which is the intent. Limit: the rule compares the
*stated* contracts, so a junk row that restates the authority row's contract verbatim is not
distinguished from a restatement (it is, however, then consistent).

## 7 — `fail=0` in prose, `fail=3` observed split across lines (SURVIVOR)

Falsified claim: the row block presents a green reading (`pass=60 fail=0`, in a cell) and, one
blank line below, records the observed text as split across two lines with `fail=3`. A reader sees
a gate row whose own receipt admits three failures; the tool reads neither the prose nor the
continuation.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,6 @@
+
+| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
+|---|---|---|---|---|---|---|---|
+| r48 split tally | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0 → `PIN_CHECK=met` · 1 → `PIN_CHECK=unmet` · 2 → setup | `python3 tools/mori-pin-check.py --selftest` | the prose reading of the run is `pass=60 fail=0` | none | mori |
+
+→ the observed text at e4dfff was split across two lines: `PIN_CHECK_SELFTEST pass=60` then `fail=3` on the next, so the prose `fail=0` above is wrong and no pin in this row is checked.
```

Measured (exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

Why it evades: three independent reasons, all narrow. (a) the row's self-test cell binds a command
but carries no pin, so `tally_pins` is unchanged and nothing is compared; (b) R9a scans only the
*other cells of a parsed row* for `TALLY_TEXT_RE`, and a bare `pass=60 fail=0` with no prefix does
not match it; (c) R9b needs `prev_raw` to be row-shaped and the blank line clears it. Note the
instrument's real output at the tip is one line, `PIN_CHECK_SELFTEST pass=60 fail=0` — the `fail=3`
is the false claim, and it is exactly the claim a "split observed text" would hide.

A "a row with a command must carry a pin" rule does **not** work here: 21 legitimate rows bind a
command with no tally pin (e.g. SKILL.md:164 `census`, :545 `retained-loss audit`, :902
`source drift (r36)`), so that rule would red the registry — measured with the tool's own
`parse_registry`/`pin_commands`.

**Smallest rule that kills it:** the same 2-line adjacency change as §1
(`fixes/f1_adjacency.py`). Measured: on `v7_split_tally` → `unmet` exit 1 with
`pin line=985 kind=row state=hidden row='→ the observed text at e4dfff was split across two lines: …'`.
Cost and safety: identical to §1 (0 of the real registry's 979 lines newly flagged).

## 8 — HTML table markup (SURVIVOR; the free class)

Falsified claim: a row that renders as a real table (inline HTML is rendered by every Markdown
viewer) and claims `PIN_CHECK_SELFTEST pass=999 fail=0`, in a document whose own doctrine is that
"Every Markdown table in SKILL.md whose header row has a cell named `self-test`" is read.

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -979,0 +980,4 @@
+
+<table>
+<tr><td>r48 html table</td><td>gate</td><td><code>python3 tools/mori-pin-check.py --rev &lt;rev&gt;</code></td><td>0/1/2</td><td><code>python3 tools/mori-pin-check.py --selftest</code> → <code>PIN_CHECK_SELFTEST pass=999 fail=0</code></td><td>none</td><td>none</td><td>mori</td></tr>
+</table>
```

Measured (exit 0):

```
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

Why it evades: `split_cells` requires a leading `|`; the `<tr>` line is `other`, and R9b's
`prev_raw` is `<table>`, not a row.

**Smallest rule that kills it** (`fixes/f4_html_rows.py`): HTML table markup is a row shape for
R2's hidden scan.

```diff
--- a/tools/mori-pin-check.py
+++ b/tools/mori-pin-check.py
@@ -251,7 +251,8 @@
         row_shaped = bool(re.match(r"^ {0,3}\|", raw))
-        if kind in ("candidate", "fence_body") and row_shaped:
+        html_row = bool(re.match(r"^\s*<t[rd][\s>]", raw, re.I))
+        if kind in ("candidate", "fence_body", "other") and (row_shaped or html_row):
             if HIDDEN_TOKEN_RE.search(raw) or "--selftest" in raw:
                 found.append((n, raw))
```

Measured: `f4_html_rows` on base → `met` exit 0; on `v8_html_table` → `unmet` exit 1 with
`pin line=982 kind=row state=hidden row='<tr><td>r48 html table</td>…'`. Cost: none on the real
registry (`grep -cE '<t(able|r|d)[ >]'` → 0).

---

## The repair set, measured against the frozen predicate

Each rule was measured alone (`results/f*`), and then all five together
(`fixes/combined.py`, sha256 `dcecbe2c9636cffd449722164ac7c8100ec14a42ce562d59fd4ca958bdec598b`)
were scored with the **frozen counter**, unchanged, at the landed tip:

```
TMPDIR=<scratch> python3 .ufo/waves/round-48/count-c1.py --tool fixes/combined.py \
  --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --repo <lane> --jobs 4 --scratch <scratch>
```

```
variant name=J1 expect=unmet got=unmet rc=1
…   (J2–J7 elided; each printed `got=unmet rc=1`)
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
```

exit 0. So the five rules are additive with the frozen predicate: the eight J edits stay unmet, the
four honest edits and the real registry stay met. Per-rule receipts:

| rule | kills | on base | on the survivor |
|---|---|---|---|
| F1 adjacency (`fixes/f1_adjacency.py`) | §1, §7 | `met` rc 0 | `unmet` rc 1, `hidden=1` each |
| F2 NFKC header (`fixes/f2_nfkc_header.py`) | §2 | `met` rc 0 | `unmet` rc 1, `unparsed=1` |
| F3 row shape `^\s*\|` (`fixes/f3_rowshape_indent.py`) | §3, §4 | `met` rc 0 | `unmet` rc 1, `hidden=1` each |
| F4 HTML row shape (`fixes/f4_html_rows.py`) | §8 | `met` rc 0 | `unmet` rc 1, `hidden=1` |
| F5 exit contracts (`fixes/f5_exit_contract.py`) | §6 | `met` rc 0 | `unmet` rc 1, `duplicate=1` |

The cheapest complete statement of the class: **R2 must define a row by what a reader sees, not by
a leading space-and-pipe** — any line that renders as, or is quoted as, a table row (indented,
tabbed, fenced, commented, HTML) is a row for the hidden-pin scan, and R9b's adjacency must skip
blank lines. F1–F4 are one idea applied to four shapes; F5 is the separate identity rule.

## Limits of this report

- **P-C1 is untouched.** These seven survivors do not change `PIN_CHECK=met` at the tip, so the
  frozen counter cannot see them and C1 stays `met` with or without the repairs. I did not run
  `count-c1.py` against the *unpatched* tool (other w2 seats hold that receipt); my own tip control
  is the direct `--skill base-SKILL.md` run quoted at the top.
- **Rendering claims are from the Markdown rules, not from a renderer.** I did not render the
  variants with a Markdown implementation; "renders as a table / code block / comment" is the GFM
  rule as I read it (`[INFERENCE]` where I say *renders*, though the byte shapes are measured).
- The variants are byte receipts, not a review of intent: §1, §3, §4, §7, §8 place the claim
  outside the pipe-row channel, so a judge could rule them "not registry rows" — I argue they are
  in scope because R2 already makes a *fenced* row fatal on exactly that reasoning, and because
  §2 and §8 render indistinguishably from a registry row.
- §6's repair compares stated contracts only; a junk row that copies the authority row's contract
  verbatim is consistent by construction, and no rule here checks that the *pin text* still belongs
  to the row's entry instrument (D7 remains open, and closing it turns legitimate mutant-command
  rows red — the reason the landed SKILL.md gives at 959-961).
- I did not test: `--root` mode, timeout/OSError paths, or C2's entry. The patched tool's own
  selftest *was* run: `python3 -I -B fixes/combined.py --selftest` → `PIN_CHECK_SELFTEST pass=60
  fail=0`, exit 0 (`results/combined-selftest.out`; unpatched control `results/tool-selftest.out`,
  same line, exit 0) — the 60 arms, including the arms for R2/R9, still pass with the five rules
  added.
- The working tree changed under me while I measured: at 20:14 `git status` showed `M SKILL.md`
  (SKILL.md:958-961, the D7 sentence) and `M corpus/knowledge/quota-observability-r48.md`, neither
  written by this seat. Every measurement here is `--rev e4dfff32…` (an export), so nothing in this
  report reads the working tree; the base bytes are `git show e4dfff32:SKILL.md`.
- No subagents were spawned; no lane tool was run with a tracked path as an edit target; all
  measurements used `TMPDIR=.scratch/r48w2-R48CritV3Junk1/tmp`. Nothing was installed.

## Receipts

- Base: `results/baseline.out`; variants: `results/<variant>.out`; per-rule: `results/f*-*.out`;
  combined counter run: `tmp/c1-combined/`; selftests: `results/combined-selftest.out`,
  `results/tool-selftest.out`.
- Variant digests: v1 `ee6c89d0…`, v1b `8919fd04…`, v2 `dfc732a8…`, v2b `5bb59a5f…`,
  v2c `9d753c35…`, v3a `909497f2…`, v3b `732e3bcb…`, v4 `e9f2010f…`, v4b `d7d768b7…`,
  v5 `9a4d4591…`, v5b `81e7dc95…`, v6 `88849b05…`, v7 `76bf48c5…`, v8 `1d3fc4fb…`.
- Fix digests: f1 `709aa61b…`, f2 `6ad170a9…`, f3 `11270fe9…`, f4 `6835f84c…`, f5 `2fcfe4be…`,
  combined `dcecbe2c…`.
