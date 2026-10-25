# R48ExecD7 — D7 (misattributed verification): BREAKS v3 as landed, closed by the proposed R11

Seat: R48ExecD7 (leaf; one read-only labrat probe not used). Lane: `mori-shokunin` at
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Round 48, wave w2 (falsify). Landed tip under
attack: `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`. Proposal for round 49 — no tracked file was
edited by this seat.

**What I attacked.** `w1/CritJunkClasses.md` D7: a registry row whose entry cell and verdict map
describe instrument **A** while its self-test cell binds instrument **B** and pins B's *true*
tally. v3 (`tools/mori-pin-check.py` at the tip, sha256 `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`,
917 lines) has no rule relating the bound argv to the entry column; the v3-spec R1–R10 leave it
open (`v3-spec.md`; lesson M3 "Not closed: D7").

**Verdict.**
1. **D7 BREAKS v3 as landed** — class open, reproduced at the *landed tip* (not only at the
   entering tip the w1 critic measured): the tip tool scores the D7 registry `PIN_CHECK=met`, rc 0
   (§2).
2. **The class is closed by the proposed R11** — with R11 the D7 registry is
   `PIN_CHECK=unmet … misattributed=1` rc 1, the real registry at the same revision is
   `PIN_CHECK=met … misattributed=0` rc 0, the frozen acceptance counter prints
   `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` rc 0, and the tool's own
   selftest is `PIN_CHECK_SELFTEST pass=65 fail=0` rc 0 (§6).
3. **Bounded, not closed**: a misattribution whose B is a `fixtures`/`mutants` path carrying the
   claimed instrument's basename survives R11 by construction (§8). That carve-out is what keeps
   the four legitimate rows green; it is a limit, stated rather than hidden.

## 1. Target, base and scratch

`L` below is `/home/vgpnk/Projects/shokunin/mori-shokunin` (the lane root) and `S` is
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7` (this seat's scratch; every
run sets `TMPDIR=$S`).

- Tool under test (v3, unmodified): `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py`
  at `e4dfff32…`, sha256 `85a89a3b…`, 917 lines; working-tree bytes equal the tip blob
  (`git show e4dfff32:tools/mori-pin-check.py | sha256sum` → same).
- Registry: `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md` at `e4dfff32…`, sha256
  `62602b2e438a2fe572b48055e7c62cf169d94f2fa5afb14bb8e3262212e3a77d`, 979 lines; exported copy
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/skill-e4dfff32.md` (same sha256).
- Entering registry `e5dbac05…` exported for the predicate probe:
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/skill-e5dbac05.md`.
- Candidate tool:
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py`, sha256
  `8321a3104f3fc8187bcf2350bdfca26562a417ba42bfb90308563a04924cdcf6`; diff to the tip tool
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/r11.diff`, sha256 `476f8a6e…`.
  No tracked path was passed to an edit tool; `git status --porcelain` shows no modified tracked
  file from this seat.
- **Measurement base is the committed blob, not the working tree.** While this seat ran, the
  working tree changed outside it: `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md` and
  `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/quota-observability-r48.md` were
  modified at 2026-10-25 20:03:31 (the `SKILL.md` hunk rewrites the D7 sentence's "four legitimate
  mutant-command rows" to "three … (190, 191, 192)"). Every receipt below is independent of that
  drift: each tool run exports `--rev e4dfff32…` with `git archive`, and the D7 variant is built
  from `git show e4dfff32:SKILL.md`. At 19:52 the working-tree `SKILL.md` still hashed
  `62602b2e…` = the tip blob, so the parse-level probe (§3) and the tool runs measure the same
  bytes. Row counts in §3 depend on the rule's scope: under R11's bound-argv scope only 190 and
  192 need the mutant carve-out, while 191 and 912 need only the bound-argv scoping (they name
  another instrument without binding it).

## 2. The class at the landed tip (before)

D7 registry = tip `SKILL.md` + one row appended to the Round48 gate table
(`$S/skill-d7.md`, sha256 `54da8e17…`); the row's pin is updated from the
w1 text to the tip's real tally (`pass=60 fail=0`), so the row is **true about B** and false only
about its claimed instrument:

```diff
@@ -971,6 +971,7 @@
 | unlanded check (r48) | gate | `python3 tools/mori-unlanded-check.py --repo DIR --round N` | ... | ... | ... | ... | mori |
+| r48 junk misattributed | gate | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` · 1 `drifted>0` · 2 setup | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0` | none | none | mori |
 
 ### Decision row — FR2 filesystem quota (round 48)
```

Ground truth that the row lies about A: `python3 tools/mori-source-drift.py --selftest` →
`MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, rc 0 (`selftest exit_code PASS … missing_sources_exit2 PASS`).
A never prints `PIN_CHECK_SELFTEST pass=60 fail=0`.

Tip tool on the D7 registry (`$S/run-tools-mori-pin-check.py-d7.txt`):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7 \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 \
    --skill /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/skill-d7.md
pin line=974 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned=' pass=60 fail=0' observed=' pass=60 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=met tally_pins=32 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
exit 0
```

Same tool, unedited registry (`$S/run-tools-mori-pin-check.py-real.txt`):
`PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0
rebound=0 duplicate=0 hidden=0 min_tally_pins=26 … baseline=yes`, exit 0 — so D7 is a real gap in
the landed bytes, not a measurement artefact.

## 3. The four legitimate rows — classification

Measured with the tip tool's own parser over the tip registry
(`$S/attrib.py` → `$S/attrib-real.txt`): **58 parsed rows, 31 tally binds**;
29 binds run the first path of their row's entry cell, 2 run a fixture. Row numbers are tip
`SKILL.md` lines.

| line | row | binds | why it must stay green |
|---|---|---|---|
| 190 | `r45 ledger counter (C1)` | (1) `.ufo/waves/round-45/count-c1.py` `pass=16 fail=0` = claimed instrument; (2) `.ufo/waves/round-45/fixtures/mutants/count-c1.py` `pass=15 fail=1` | bind 2 is a **mutant of the claimed instrument**: `fixtures/mutants/<basename>`, same basename `count-c1.py` (the lane's convention, `SKILL.md:185`) |
| 191 | `r45 gate conformance (C2)` | (1) `.ufo/waves/round-45/count-c2.py` `pass=14 fail=0` = claimed instrument | the self-test cell *names* the mutant `.ufo/waves/round-45/fixtures/mutants/count-c2.py` with its sha256 but **binds no tally to it**; a rule that compared every path in the cell to the entry would go red here |
| 192 | `r45 corpus coverage (C3)` | (1) `.ufo/waves/round-45/count-c3.py` `pass=19 fail=0`; (2) `.ufo/waves/round-45/fixtures/mutants/count-c3.py` `pass=17 fail=2` | same shape as 190 |
| 912 | `SOURCES append-only timing (r38)` | (1) `tools/mori-sources-appendonly.py <rev> --selftest` `pass=22 fail=0` = claimed instrument | the cell *names another tool* (`tools/mori-pin-check.py`, the instrument that re-measured it) in prose; the only bound argv is the claimed instrument — again, only a **bound-argv** rule is safe |

Two consequences fix the rule's shape: it must read **only the argv bound to each tally pin**
(not every path of the self-test cell), and it must allow a **mutant of the claimed instrument**
under `fixtures`/`mutants` with the same basename. The predicate probe
(`$S/r11probe.py`) on both registries:

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7 \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/r11probe.py \
    /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/skill-e4dfff32.md deadbeef
r11_red=0 no_argv=0 no_entry_path=0
$ … /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/skill-e5dbac05.md deadbeef
r11_red=0 no_argv=0 no_entry_path=0
```

(`no_entry_path=0`: no row at either revision binds a tally without naming a path in its entry
cell, so the "claimed instrument" is always defined.)

## 4. R11 — the rule (normative wording for round 49's v3-spec)

> **R11 misattribution** (closes D7). For each tally pin with a bound argv, let *claimed* be the
> first file path named in the row's **entry cell** and *bound* the file path its argv runs (the
> word after the interpreter and its `-I`/`-B` flags). The pin is `misattributed` (fatal) unless
> *bound* equals *claimed*, or *bound* is a mutant of *claimed*: a path with a `fixtures` or
> `mutants` directory segment whose basename equals the claimed instrument's basename (the lane's
> `fixtures/mutants/<basename>` convention, `SKILL.md:185`). A row that binds a tally with no
> path in its entry cell is `misattributed` with `claimed=None`. The counter `misattributed=` is
> appended to the verdict line after `hidden=` and is fatal; one
> `pin line=… kind=tally prefix=… state=misattributed claimed=… bound=…` line is printed per
> finding. Selftest arms: `r11_misattributed_instrument`,
> `r11_mutant_other_basename_rejected`, `r11_second_entry_path_not_claimed`,
> `r11_entry_cell_without_instrument`, `r11_mutant_right_basename_wrong_directory`; the existing
> `mutant_pin_bound_to_mutant`/`mutant_pin_wrong` arms move their mutant to
> `.ufo/waves/round-9/fixtures/mutants/foo.py`, and `r7_escaped_double_backslash_pipe`'s entry
> cell names the instrument it runs (its purpose, `\\|` splitting, is unchanged).

Design notes: the rule is text-only and adds no subprocess — one `PATH_RE.findall` per parsed row
and one comparison per tally pin; the bound command is **not** run when the pin is
`misattributed` (the verdict is already fatal, and the pin still counts toward `tally_pins`, so a
misattributed row cannot lower the floor). It reuses the existing `PATH_RE` and the existing
`PY_FLAGS` skip, so `python3 -I -B tools/x.py <rev> --selftest` normalises identically to the
`argv_ok` path.

## 5. Diff (candidate vs the landed tip)

`diff -u /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py
/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py`
(sha256 of the diff `476f8a6e…`; candidate `8321a310…`, 53,519 B):

```diff
--- /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py
+++ /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py
@@ -32,6 +32,14 @@
 continuation line directly under a row, is `hidden` (R9a/R9b); a tally written
 outside backticks in a self-test cell is `unparsed` (R9c).
 
+R11 (round-48 wave-2 proposal, `w2/R48ExecD7.md`, closes D7): a tally pin's
+bound argv must run the row's claimed instrument — the first file path named in
+the row's entry cell — or a mutant of it: a path with a `fixtures` or `mutants`
+directory segment whose basename equals the claimed instrument's basename (the
+lane's `fixtures/mutants/<basename>` convention, SKILL.md:185). Any other
+instrument is `misattributed` (fatal). A row that claims instrument A in its
+entry cell while its self-test cell runs instrument B is no longer green.
+
 What it reads
   Every Markdown table in SKILL.md whose header row has a cell named
   `self-test`. Cells are split on unescaped `|`; a data row whose cell count
@@ -275,6 +283,26 @@
             and os.path.isfile(fp))
 
 
+def instrument_of(argv):
+    """R11: the file path a bound argv runs — the word after the interpreter and
+    its flags."""
+    i = 1
+    while i < len(argv) and argv[0].startswith("python") and argv[i] in PY_FLAGS:
+        i += 1
+    return argv[i] if i < len(argv) else None
+
+
+def mutant_of(path, claimed):
+    """R11 carve-out: `path` is a mutant of `claimed` — under a `fixtures` or
+    `mutants` directory and carrying the claimed instrument's basename (the lane's
+    `fixtures/mutants/<basename>` convention, SKILL.md:185)."""
+    if not path or not claimed:
+        return False
+    segs = path.split("/")
+    return (("fixtures" in segs or "mutants" in segs)
+            and os.path.basename(path) == os.path.basename(claimed))
+
+
 def span_kind(span, cells, rev, eidx):
     """Classify one backticked span of a self-test cell (R3, R7 L4):
     ('tally'|'digest'|'trunc'|'command'|'unparsed'/reason|'ignore')."""
@@ -453,7 +481,7 @@
     out = []
     counts = {"tally_pins": 0, "digest_pins": 0, "mismatches": 0,
               "unparsed": 0, "no_command": 0, "dropped": 0, "rebound": 0,
-              "duplicate": 0, "hidden": 0}
+              "duplicate": 0, "hidden": 0, "misattributed": 0}
     base_bind = {}
     base_bind_prefix = {}
     if baseline_text is not None:
@@ -500,6 +528,10 @@
             continue
         cells, idx = row["cells"], row["idx"]
         st = cells[idx]
+        # R11: the row's claimed instrument — the first file path of its entry cell.
+        entry_cell = cells[row["eidx"]] if len(cells) > row["eidx"] else ""
+        entry_paths = PATH_RE.findall(entry_cell)
+        claimed = entry_paths[0] if entry_paths else None
         # R3 / R7 L4: ASCII-strict span checks (a tally digitless pin is still
         # counted by the tally branch below).
         for m in SPAN_RE.finditer(st):
@@ -560,6 +592,14 @@
                 counts["no_command"] += 1
                 out.append("pin line=%d kind=tally prefix=%s state=no_command" % (line, prefix))
                 continue
+            # R11 (D7): the bound argv must run the row's claimed instrument or a
+            # mutant of it, never a different instrument.
+            inst = instrument_of(words)
+            if inst != claimed and not mutant_of(inst, claimed):
+                counts["misattributed"] += 1
+                out.append("pin line=%d kind=tally prefix=%s state=misattributed claimed=%s bound=%s"
+                           % (line, prefix, claimed, inst))
+                continue
             key = tuple(words)
             if key not in cache:
                 cache[key] = run_cmd(words, root, scratch, timeout)
@@ -595,12 +635,15 @@
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
+                  counts["misattributed"],
                   min_tally, rev or "-",
                   "yes" if baseline_text is not None else "no"))
     return met, out
@@ -726,14 +769,24 @@
             f.write(SLOW)
         with open(os.path.join(root, "tools", "rev.py"), "w") as f:
             f.write(REVTOOL)
-        with open(os.path.join(root, "tools", "mut.py"), "w") as f:
-            f.write(MUT)
+        # R11 carve-out fixtures: a mutant of the claimed instrument lives under
+        # `.ufo/waves/round-N/fixtures/mutants/<basename>` (SKILL.md:185); a fixture with
+        # another basename, or the right basename outside a fixtures/mutants directory, is
+        # not a mutant of the claimed instrument.
+        for rel in (".ufo/waves/round-9/fixtures/mutants/foo.py",
+                    ".ufo/waves/round-9/fixtures/mutants/bar.py",
+                    ".ufo/waves/round-9/foo.py"):
+            p = os.path.join(root, *rel.split("/"))
+            os.makedirs(os.path.dirname(p), exist_ok=True)
+            with open(p, "w") as f:
+                f.write(MUT)
         with open(os.path.join(root, "tools", "tmp.py"), "w") as f:
             f.write(TMPTOOL)
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
@@ -858,9 +911,12 @@
                       1, False, "no_command"))
         cases.append(("r7_argv_trailing_args_rejected", HDR + row("`python3 tools/foo.py --selftest extra` → " + stale, entry="no command here"),
                       1, False, "no_command"))
-        # R7 L2: `\\|` is a literal backslash followed by a real separator; the row stays 8 cells.
+        # R7 L2: `\\|` is a literal backslash followed by a real separator; the row stays 8
+        # cells. The entry cell names the instrument the row runs (R11: a pin with no claimed
+        # instrument in its entry cell is `misattributed`, claimed=None).
         cases.append(("r7_escaped_double_backslash_pipe", HDR +
-                      "| foo | gate | a\\\\| 0 ok | `python3 tools/foo.py --selftest` → "
+                      "| foo | gate | `python3 tools/foo.py --rev <rev>` a\\\\| 0 ok | "
+                      "`python3 tools/foo.py --selftest` → "
                       "`FOO_SELFTEST pass=3 fail=0` | none | none | mori |\n", 1, True, None))
         # R10 (round-48 CritJunkClasses D1): a digest of another file named elsewhere in the row.
         slow_digest = sha256_file(os.path.join(root, "tools", "slow.py"))
@@ -881,6 +937,21 @@
         # R9c (D18): a tally written outside backticks in the self-test cell.
         cases.append(("r9c_tally_outside_backticks", HDR + row(good + "; also FOO_SELFTEST pass=999 fail=0"),
                       1, False, "unparsed"))
+        # R11 (round-48 wave-2 D7): the bound argv must run the claimed instrument.
+        cases.append(("r11_misattributed_instrument", HDR + row(
+            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`"), 1, False, "misattributed"))
+        cases.append(("r11_mutant_other_basename_rejected", HDR + row(
+            good + "; the fixture `.ufo/waves/round-9/fixtures/mutants/bar.py` reads "
+            "`FOO_SELFTEST pass=2 fail=1` rc 1"), 2, False, "misattributed"))
+        cases.append(("r11_second_entry_path_not_claimed", HDR + row(
+            "`python3 tools/lc.py --selftest` → `LC_SELFTEST pass=1 fail=0`",
+            entry="`python3 tools/foo.py --rev <rev>` (`--tool` default `tools/lc.py`)"),
+            1, False, "misattributed"))
+        cases.append(("r11_entry_cell_without_instrument", HDR + row(
+            good, entry="the drift probe (no path named)"), 1, False, "misattributed"))
+        cases.append(("r11_mutant_right_basename_wrong_directory", HDR + row(
+            good + "; the fixture `.ufo/waves/round-9/foo.py` reads `FOO_SELFTEST pass=2 fail=1` rc 1"),
+            2, False, "misattributed"))
         for name, text, floor, want_met, want_state in cases:
             scratch = tempfile.mkdtemp(prefix="c-", dir=base)
             text, btext = text if isinstance(text, tuple) else (text, None)
```

(The `tools/mut.py` fixture of the old arm shape is deleted by the diff — no arm reads it any
more; the three `.ufo/waves/round-9/…` fixtures carry the tallies. The escaped-pipe arm keeps its
purpose (`\\|` splitting) and only gains an instrument in its entry cell.)

## 6. Evidence

### 6.1 Selftest — all arms, final bytes

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7 \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py --selftest
… 65 × "PASS <arm>  <verdict line>" …
PIN_CHECK_SELFTEST pass=65 fail=0
exit 0
```
(`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/selftest-r11.txt`; the tip
tool's own tally is `pass=60 fail=0` — 60 arms + 5 new = 65. The five R11 arms each print their own
verdict line, e.g. `PASS r11_misattributed_instrument  PIN_CHECK=unmet … misattributed=1 …`.)

### 6.2 Able to fail — five mutations of the rule, each killed by exactly its arms

| mutation (sed on a scratch copy) | selftest | arms that flip to FAIL |
|---|---|---|
| A: `if inst != claimed and not mutant_of(...)` → `if False:` (rule removed) | `pass=60 fail=5`, rc 1 | `r11_misattributed_instrument`, `r11_mutant_other_basename_rejected`, `r11_second_entry_path_not_claimed`, `r11_entry_cell_without_instrument`, `r11_mutant_right_basename_wrong_directory` |
| B: `mutant_of` returns `False` (carve-out removed) | `pass=63 fail=2`, rc 1 | `mutant_pin_bound_to_mutant`, `mutant_pin_wrong` |
| C: skip when `claimed is None` | `pass=64 fail=1`, rc 1 | `r11_entry_cell_without_instrument` |
| D: drop the `fixtures`/`mutants` directory condition | `pass=64 fail=1`, rc 1 | `r11_mutant_right_basename_wrong_directory` |
| E: drop the basename-equality condition | `pass=64 fail=1`, rc 1 | `r11_mutant_other_basename_rejected` |

No mutation fails an arm outside its own rule (no collateral). Receipts
`$S/selftest-mut{A,B,C,D,E}-*.txt`; mutants
`mutA-rule-removed.py … mutE-basename-condition-dropped.py` in the same directory. This satisfies
v3-spec R8 ("every new arm is killed by the mutation that removes its rule") and shows the
carve-out itself is pinned in both directions.

### 6.3 D7 red under R11 (final bytes)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7 \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 \
    --skill /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/skill-d7.md
pin line=974 kind=tally prefix=PIN_CHECK_SELFTEST state=misattributed claimed=tools/mori-source-drift.py bound=tools/mori-pin-check.py
PIN_CHECK=unmet tally_pins=32 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=1 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
exit 1
```
(`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/run-d7-final.txt`.) The
finding names both sides of the misattribution; the same registry is `met` under the tip tool
(§2), so the flip is the rule and nothing else.

### 6.4 Real registry green under R11 (final bytes)

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7 \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --min-tally-pins 26 \
    --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
41 × "pin line=…" (all state=match)
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
exit 0
```
(`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/run-real-final.txt`.) Every
verdict counter except the new one is identical to the tip tool's run (§2): `tally_pins=31
digest_pins=8` and all fatals 0.

### 6.5 Frozen acceptance counter, unchanged, with R11 as the tool under test

```
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7 \
  python3 -I -B /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py \
    --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/pincheck-d7.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --baseline 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --min-tally 26 --jobs 4 \
    --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/c1scratch
variant name=J1 expect=unmet got=unmet rc=1
… J2 … J8 all "expect=unmet got=unmet rc=1" …
variant name=H1 expect=met got=met rc=0
… H2, H3, H4 all "expect=met got=met rc=0" …
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
exit 0
```
(`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7/count-c1-r11.txt`.) This is
the predicate the round-49 claim would be scored with, at the same revision and baseline: R11 is
not narrower than the frozen junk and does not reject any honest edit. The counter was not
modified.

## 7. Cost and risk

- No new subprocess: the rule compares text already parsed; it *skips* the bound run for a
  misattributed pin (one `pin line=` instead of a command run), so a registry full of D7 rows
  gets cheaper, not slower.
- One new fatal counter appended after `hidden=`; the verdict line stays a single line. Consumers
  of the line in this lane grep `PIN_CHECK=(met|unmet)` (`count-c1.py:run_tool`), so the addition
  is compatible.
- The four legitimate rows need **no registry edit**; only the tool's own selftest fixtures change
  (§5, last two hunks).

## 8. Limits — what R11 does not close (state, do not re-score)

1. **A fixture-shaped decoy.** A row claiming `tools/foo.py` whose self-test binds
   `.ufo/waves/round-N/fixtures/mutants/foo.py` is allowed even if that fixture is not a mutant
   but an unconditional echo of the pinned tally. R11 cannot tell a mutant from a decoy with the
   same basename; the protection is that such a file must be committed, which is D6 (the w1
   critic found no such script at R; it becomes a *file* class, not a registry-text class).
2. **Claim moved into the entry cell's second path.** R11 compares the *first* path only, so a
   row may name B first (entry cell) and still describe A in its row *name* or verdict map. R11
   does not read the row name or the verdict-map prose; D7 as *worded* (entry cell claims A) is
   closed, a row that mislabels itself in the name column is not.
3. **No pin, no claim.** A row with no tally pin is invisible to R11 (nothing is verified); rows
   whose entry cell names no path *and* bind a tally are `misattributed` (`claimed=None`), but a
   row with neither a path nor a pin stays `met` by construction.
4. **Bytes are not read.** R11 compares paths, not tool contents: a registered instrument that
   prints another instrument's tally is out of scope (same as D6).
5. **Cross-revision staleness is not its subject.** R11 says nothing about a row whose claimed
   instrument's *tally* drifted; that is the existing tally/digest/line-count machinery.

## 9. Consequences for round 49 (the self-referential pin)

If R11 lands, the tool's selftest prints `PIN_CHECK_SELFTEST pass=65 fail=0` (measured, §6.1)
while the registry row `registry pin reconciler (r47, C1)` at `SKILL.md:938` pins
`PIN_CHECK_SELFTEST pass=60 fail=0`. Because the pin check runs the **measured tree's** tool, the
row must be repaired to `pass=65 fail=0` in the same commit; otherwise the tool's own row goes
`mismatch` on itself. (In the measurements above the export at `e4dfff32…` still contains the tip
tool, so the row legitimately stayed at 60.) The v3-spec section for round 49 should also state
that R11's `misattributed` counter is fatal, and add the rule to the docstring's rule list (done
in the diff).

## 10. Reproduction

```sh
S=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecD7
L=/home/vgpnk/Projects/shokunin/mori-shokunin
REV=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
BASE=2d85e33d14198d388fd3cda9cc15ec07e57e7a53
cd $L
git show $REV:SKILL.md > $S/skill-e4dfff32.md
python3 -I -B $S/make-d7.py $S/skill-e4dfff32.md $S/skill-d7.md      # D7 registry
TMPDIR=$S python3 -I -B $S/pincheck-d7.py --selftest                  # pass=65 fail=0
TMPDIR=$S python3 -I -B $S/pincheck-d7.py --rev $REV --repo . --min-tally-pins 26 \
    --baseline-rev $BASE --skill $S/skill-d7.md                      # unmet, misattributed=1, rc 1
TMPDIR=$S python3 -I -B $S/pincheck-d7.py --rev $REV --repo . --min-tally-pins 26 \
    --baseline-rev $BASE                                             # met, misattributed=0, rc 0
TMPDIR=$S python3 -I -B .ufo/waves/round-48/count-c1.py --tool $S/pincheck-d7.py --rev $REV \
    --repo . --baseline $BASE --min-tally 26 --jobs 4 --scratch $S/c1scratch   # C1=met, rc 0
TMPDIR=$S python3 -I -B $S/r11probe.py $S/skill-e4dfff32.md deadbeef # r11_red=0 …
```

## 11. Unverified

- Whether any *other* lane row outside this revision would be rejected by R11: only
  `e4dfff32…` and `e5dbac05…` were probed (`r11_red=0` on both); a future row that names its
  verified instrument second in the entry cell would be `misattributed` (see §8.2).
- The full 13-variant matrix was run once at the final bytes (`§6.5`); no repeat run, no seed or
  timing sensitivity is expected (the counter has none), but a second run was not taken.
- No labrat probe was dispatched: every claim above is a direct measurement of the lane's own
  bytes.
- The candidate deletes the selftest's `tools/mut.py` fixture (no arm reads it after the mutant
  moved under `fixtures/mutants/`); a variant that kept it would print the same
  `PIN_CHECK_SELFTEST pass=65 fail=0` — not measured separately.

Report: .ufo/waves/round-48/w2/R48ExecD7.md
