# CritJunkClasses — wave w1 new false-green classes against v2 (round 48, C1)

Seat: CritJunkClasses (leaf, no subagents). Target: the **v2** standing tool
`tools/mori-pin-check.py` at the entering tip
`R = e5dbac05459887d9597ea5d1da0d8e3d024e0d17` (sha256
`9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`, == R blob).
Measured-tree base: byte-exact `SKILL.md` at R (939 lines, sha256
`2c9772fe5dc19d35bf6ee15a3ef698915384b11eda686e59aa5d0b9413d6005b`) exported via
`git archive`; each variant = base + one edit. Scratch:
`.scratch/r48-CritJunkClasses/` (`variants/`, `results/`), TMPDIR inside it.

Every measurement below uses the same CLI as the frozen counter
`count-c1.py`'s `run_tool`:
`python3 -I -B v2-copy.py --rev R --repo <lane> --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 --skill <variant>`.

Baseline (pristine R, exit 0):
```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

## Verdict: **eight new false-green classes verified** (all `PIN_CHECK=met`, exit 0)

None repeat FG1-FG5/O1/N1-N4 (round-47 `w2/CritV2Junk.md`) or the frozen junk set
J1-J8 (round-48 `count-c1.py`). Classes are numbered D1-D18 with gaps left for
attempted-but-unrealizable classes (D6, below). The edits all live in SKILL.md
(report-only seat); no production files were touched.

---

## D1 — digest pin satisfied by a decoy file named elsewhere in the row (full 64-hex)

The row claims `tools/mori-pin-check.py`'s bytes hash `H`, but `H` is the sha256 of
a *different* committed file also named in the row. v2's digest check answers "does
`H` equal the sha256 of **any** path named in the row that resolves inside the tree"
— it never checks that the digest belongs to the claimed instrument. The decoy
`corpus/SOURCES.md` (sha256 at R = `e0c4c39b2804a16d51979bff3ceb9f1ff277b14cabb39b17bca2164f20ca911a`)
is named in the row, so the pin matches and `PIN_CHECK=met`.

Unified diff (append after R line 939):
```diff
@@ -937,3 +937,4 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+| r48 junk decoy digest | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → e0c4c39b2804a16d51979bff3ceb9f1ff277b14cabb39b17bca2164f20ca911a | `corpus/SOURCES.md` | none | mori |
```

v2 output (exit 0):
```
pin line=940 kind=digest state=match digest=e0c4c39b2804 file=corpus/SOURCES.md
PIN_CHECK=met tally_pins=28 digest_pins=6 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: `check()` collects `PATH_RE` paths from the **whole raw row** and
matches the digest against any of them (`tools/mori-pin-check.py` and
`corpus/SOURCES.md` both resolve; the decoy wins by if). The claim about the
instrument's bytes is false; the pin is satisfied by a different file. This is the
"a pinned sha256 of a different file with the right path elsewhere in the row" class.

v3 rule evaluation: R1 no · R2 no (row is inside a parsed table) · R3 no · R4 no ·
R5 no · **R6 no** — R6 only addresses *truncated* digest pins
(`[0-9a-f]{8,63}…`, U+2026) and still checks "prefix of the sha256 of **some** path
named in the row", so a full-length decoy digest remains accepted · R7 no · R8 n/a.
**Survives v3 as specced.**

---

## D2 — tally pin on a second physical line of the row (continuation line, no pipe)

The row's parse line carries the command; the tally (false `pass=999`) sits on the
next physical line, which does not start with `|`. `parse_registry` treats that line
as prose, so the pin is never parsed, counted or checked. The false claim is visible
in the document and invisible to v2.

Unified diff:
```diff
@@ -937,3 +937,5 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+| r48 junk second line | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` | none | none | mori |
+→ `PIN_CHECK_SELFTEST pass=999 fail=0`
```

v2 output (exit 0):
```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: the pin never enters a cell; only `|`-leading lines are rows. The
tally stays 28 (nothing dropped), so the floor is untouched.

v3 rule evaluation: R1 no · R2 no (the continuation line is not a *table row* —
R2's definition is a line starting with up to three spaces then `|`) · R3 no (the
span is not inside a self-test cell) · R4-R8 no. **Survives v3 as specced.**

---

## D3 — second table whose header cell reads `Self-test results`

`parse_registry` recognizes a header only when a cell lowercases to exactly
`self-test` (list membership). `Self-test results` is a different string, so the
whole second table is invisible and its corrupt pin (`pass=999`) passes unchecked. A
prose line before it clears the previous table's header so this table is not
absorbed into the round-47 table (which would parse the row and go red).

Unified diff:
```diff
@@ -937,3 +937,7 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+
+| name | kind | entry | verdict map | Self-test results | pinned values | write scope | owner |
+|---|---|---|---|---|---|---|---|
+| r48 junk stattest | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=999 fail=0` | none | none | mori |
```

v2 output (exit 0):
```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: same invisibility channel as FG1/J1 (`selftest` → `Self-test results`
is a new spelling; ~ header is *additional*, not a rename of the round-47 header).
The corrupt row is never parsed.

v3 rule evaluation: **R1 catches only if implemented as substring** — "recognised
case-insensitively as `self-test`, `selftest` or `self test`" reads as exact cell
equality today, under which `Self-test results` stays unrecognized and R1 alone does
not catch it. **R2 catches it regardless**: the data row is a table row that is not
part of a parsed self-test table and contains an ASCII `[A-Z][A-Z0-9_]*SELFTEST`
token and `--selftest` → `hidden` (fatal). R3-R8 no. **Caught by R2** (and by R1
iff R1 is substring-based).

---

## D4 — tilde-fenced replacement of the two round-47 gate rows (corrupt pins)

Mirror of J5/FG5 but with `~~~` fences instead of ` ``` `. The two real pins vanish
from the tally (28 → 26, still at the floor) and are replaced by corrupt `pass=1`
claims that are never read.

Unified diff:
```diff
@@ -935,5 +935,7 @@
 | name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
 |---|---|---|---|---|---|---|---|
-| registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
-| r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+~~~markdown
+| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=1 fail=0` | none | none | mori |
+| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev>` | 0/1/2 | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=1 fail=0` | none | none | mori |
+~~~
```

v2 output (exit 0):
```
PIN_CHECK=met tally_pins=26 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: fences (both delimiters) are skipped wholesale by `parse_registry`;
the floor 26 is exactly what survives the removal of the two round-47 pins. (A
fence block *added* rather than replacing rows leaves 28 pins, also green.)

v3 rule evaluation: R1 no · **R2 catches** ("Fenced blocks are not exempt for such
rows") · R3-R8 no. **Caught by R2.**

---

## D5 — new row with an empty self-test cell; the tally claim sits in pinned-values

The row asserts `PIN_CHECK_SELFTEST pass=999 fail=0` (in the `pinned values` cell)
but its self-test cell is empty. v2 scans only the self-test cell; the claim is
never checked. Nothing is dropped (tally stays 28), so the verdict stays green.

Unified diff:
```diff
@@ -937,3 +937,4 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+| r48 junk empty cell | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 |  | `PIN_CHECK_SELFTEST pass=999 fail=0` | none | mori |
```

v2 output (exit 0):
```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: the semantic cell is empty, so no command and no pin exist; the claim
moved to a cell that is never read. This is only possible for rows with no baseline
obligation (rows 938-939 and later names); emptying a baseline-keyed row's cell
would trip `dropped`.

v3 rule evaluation: R1 no · R2 no (the row *is* part of a parsed table; R2's
"hidden" only covers rows outside parsed tables) · R3 no (no span in the self-test
cell) · R4-R8 no. **Survives v3 as specced.**

---

## D7 — misattributed verification: the row claims instrument A, v2 verifies instrument B

The new row's entry cell and verdict map describe `tools/mori-source-drift.py`
(its real selftest line: `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` — measured for
this report), but the self-test cell binds `tools/mori-pin-check.py --selftest` and
pins `PIN_CHECK_SELFTEST pass=34 fail=0`. v2 runs the *bound* command (pin-check)
and validates the pin against pin-check's true output; the row's claim about the
drift tool is false but never checked. The bag is a fresh row so the baseline
guard has no obligation to compare the binding to the entry.

Unified diff:
```diff
@@ -937,3 +937,4 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+| r48 junk misattributed | gate | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` · 1 `drifted>0` · 2 setup | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | none | none | mori |
```

v2 output (exit 0):
```
pin line=940 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
PIN_CHECK=met tally_pins=29 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: v2 never cross-checks the bound command against the row's entry /
verdict-map / name. It verifies *that some committed instrument prints the pinned
text*, not that the registered instrument does. FG4 pinned a stale copy of the
*same* instrument; D7 binds a *different* instrument entirely.

v3 rule evaluation: R1-R8 no (no rule relates the bound argv to the entry column's
instrument). **Survives v3 as specced.**

---

## D8 — all-ASCII lowercase obfuscated tally prefix

The prefix `pin_check_selftest` (lowercase) fails v2's tally regex
`[A-Z][A-Z0-9_]*SELFTEST`, and the span contains no `--selftest`/bare path, so it
binds nothing and is silently ignored. The false `pass=999` claim passes. This is
the ASCII counterpart of FG2/FG3 (which used homoglyphs); no non-ASCII character is
involved.

Unified diff:
```diff
@@ -937,3 +937,4 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+| r48 junk lowercase | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → `pin_check_selftest pass=999 fail=0` | none | none | mori |
```

v2 output (exit 0):
```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: same "span is neither a tally pin nor a bound command, so it
contributes nothing" channel as FG2/FG3, but with ASCII only — the parser's strict
uppercase shape is the only gate.

v3 rule evaluation: R1 no · R2 no · **R3 catches** (the span's NFKC-casefolded text
contains `selftest` and is not an ASCII tally pin → `unparsed`, fatal) · R4-R8 no.
**Caught by R3.**

---

## D18 — tally written as plain text inside a parsed cell (no backticks)

The self-test cell shows `→ PIN_CHECK_SELFTEST pass=999 fail=0` outside backticks.
v2 reads pins only from backticked spans (`SPAN_RE`); the plain-text tally is
invisible, so the row verifies its command but never the (false) count. Tally stays
28.

Unified diff:
```diff
@@ -937,3 +937,4 @@
 |---|---|---|---|---|---|---|---|
 | registry pin reconciler (r47, C1) | gate | ... | ... | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | ... | ... | mori |
 | r47 tracepoint catalogue (C2) | gate | ... | ... | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | ... | ... | mori |
+| r48 junk plaintext | gate | `python3 tools/mori-pin-check.py --rev <rev>` | 0/1/2 | `python3 tools/mori-pin-check.py --selftest` → PIN_CHECK_SELFTEST pass=999 fail=0 | none | none | mori |
```

v2 output (exit 0):
```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17 baseline=yes
```

Why it evades: pin discovery is span-based; a tally that is not backticked is not a
pin and not an unparsed row.

v3 rule evaluation: R1 no · R2 no (row is part of a parsed table) · R3 no (requires a
backticked span) · R4-R8 no. **Survives v3 as specced.**

---

## Attempted but unrealizable at R: D6 — unconditional `echo` tally via a committed tools/ script

The brief's example ("a command that prints the pinned text unconditionally via
`echo` inside a committed tools/ script") was investigated as its own class:

- The round-47 control `c1-junk/skill-v3-fakeecho.md` already covers inline
  `python3 -c "print(...)" ... --selftest`; v2 rejects it via `argv_ok` (no SAFE_PATH
  argument). That channel is closed and not repeated here.
- A committed script under `tools/` or `.ufo/waves/round-N/` that prints a tally
  unconditionally would pass v2 trivially (the check only compares output text and
  exit code). **No such script exists at R**: a sweep of every committed `.py`/`.sh`
  under the SAFE_PATH prefixes found tally lines only in tools that compute them from
  real checks (e.g. `mori-silence-cases.sh`, `mori-pin-check.py`), in archived
  earlier copies (already J4/FG4), or in fixtures that print summary lines without a
  `*_SELFTEST` prefix (`.ufo/waves/round-38/fixtures/const.py`, `memo-*.py`).
- So the class is not *observable* at the fixed measured revision without adding a
  committed file, which a SKILL.md-only variant cannot do. **UNVERIFIED as a
  concrete edit at R.** If such a stub were later committed, no v3 rule (R1-R8)
  inspects tool internals, so it would survive v3 too — record as a w2 limit, not a
  scored class.

## R-rule coverage matrix

| class | v2 verdict | R1 header | R2 visibility | R3 ASCII | R4 rebound | R5 line-count | R6 digest | R7 residuals | R8 selftest |
|---|---|---|---|---|---|---|---|---|---|
| D1 decoy digest | met | no | no | no | no | no | **no (survives)** | no | n/a |
| D2 continuation tally | met | no | no (not a row) | no | no | no | no | no | n/a |
| D3 `Self-test results` | met | no* | **yes** | no | no | no | no | no | n/a |
| D4 tilde fence | met | no | **yes** | no | no | no | no | no | n/a |
| D5 empty self-test cell | met | no | no | no | no | no | no | no | n/a |
| D7 misattributed | met | no | no | no | no | no | no | no | n/a |
| D8 lowercase prefix | met | no | no | **yes** | no | no | no | no | n/a |
| D18 plain-text tally | met | no | no | no | no | no | no | no | n/a |

*D3: caught by R1 too iff R1 is implemented as substring matching; under exact-equal
cell matching it is not (see D3 text).

**Survivors of v3 as specced (limits for w2): D1, D2, D5, D7, D18** — plus the
unrealizable D6 if ever committed.

## Impacted axis

- **calibration (C1)** — primary: P-C1's `PIN_CHECK=met` is emitted for registries
  whose digest pins verify a decoy file (D1), whose false tallies hang on
  continuation lines (D2) or as plain text (D18), whose verification is
  misattributed across instruments (D7), whose claims move out of the semantic cell
  (D5), and whose invisible tables/fences hide corrupt pins (D3, D4). These are the
  same class of "the registry lies while the tool is green" the round's C1 exists to
  kill.

## Smallest safe corrections

1. **Pin digest to the claim's own instrument path** (R6 extension): a digest pin
   must match the sha256 of the path named in the *entry* cell (or the self-test
   command's path), not *any* path in the row; a row whose digest matches a
   non-claimed path is `mismatch`. Kills D1.
2. **Scan the full row region for unparsed tally shapes**: treat a SELFTEST-prefixed
   token on a non-row line immediately following a parsed row (D2) and a
   non-backticked `[A-Z][A-Z0-9_]*SELFTEST` token inside a parsed self-test cell
   (D18) as `unparsed`/`hidden`.
3. **Require the bound command to be the row's entry instrument** (R4 extension):
   record the entry cell's first path; a tally whose bound argv names a different
   instrument path is `rebound`/`misattributed`. Kills D7.
4. **Verify the self-test cell is non-empty and the claim text is in it**: a row
   whose self-test cell is empty while any other cell carries a SELFTEST token is
   `unparsed` (kills D5). Note this must not break the frozen honest rows (H1-H4).
5. R2 already covers D3 (any unparsed table row with a SELFTEST token) and D4
   (fenced rows); keep R2's scope but make explicit that it also covers a second
   unrecognized header spelling (`Self-test results`) and both fence delimiters.

## Evidence

- Scratch: `.scratch/r48-CritJunkClasses/` — `variants/D1…D18.md` (+`000-pristine.md`),
  `results/D1…D18.txt` (full command + pin lines + verdict line per variant),
  `results/D1…D18.diff` (unified diffs), `gen_variants.py`, `v2-copy.py` (==
  `tools/mori-pin-check.py` at R, sha256 `9832e38c…`).
- Measured tree: `git archive` of R; base SKILL.md sha256
  `2c9772fe…` (939 lines). Baseline rev `2d85e33d…` resolves.
- D7 ground truth: `python3 tools/mori-source-drift.py --selftest` →
  `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` rc 0 (the row claims
  `PIN_CHECK_SELFTEST pass=34 fail=0` instead).
- D1 decoy ground truth: `git show R:corpus/SOURCES.md | sha256sum` →
  `e0c4c39b2804a16d51979bff3ceb9f1ff277b14cabb39b17bca2164f20ca911a`.
- Tool selftest receipts: `python3 v2-copy.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` rc 0.
