# Work performed — round 40 (C1 operability, C2 depth)

Draft prose for the round-40 report's "Work performed" section. Every number is
quoted from a committed receipt under `.ufo/waves/round-40/evidence/` or from a
count this seat took over committed bytes (method stated where counted).
Commands are quoted from each receipt's own `command:` line. Where a receipt
disagrees with the frozen prose, both are quoted under **Conflicts** and no
verdict is given here — the canonical judge owns that call.

## C1 — operability (score 7): conformance checker v3, P-C10

**Built.** The round-40 conformance checker
`.ufo/waves/round-40/conform.py` (805 added lines against the entering tip,
`git diff --stat bb1f2457 265a955cc`) with the counter of record
`.ufo/waves/round-40/count-c8.py` (563 added lines; the round-39 `count-c7.py`
bytes minus the sixteen dead lines of SimpCounters D1–D4). The checker's list of
checks is readable straight out of `c10-after.txt`: `predicate`, `head_pin`,
`tool_resolve`, `bounded_reads`, `timeout_scope`, `drain_bind`, `timeout_state`,
`scratch`, `selftest_conjunct` — nine `check … PASS` lines.

**Instrument/fixture freeze held.** `evidence/freeze-r40.txt` pins six round-40
paths and three extracted before-instrument paths; this seat re-derived all nine
sha256 values from the worktree bytes and all nine matched the receipt
(`contract.md` `6514914885…`, `count-c8.py` `4e4d50eb…`, `conform.py`
`5025b966…`, `tools/mori-sources-appendonly.py` `bde5a9a…`, `make-survivor-fixtures.py`
`8ff91db7…`, `run-c11-dags.py` `0cd7f1d2…`, `conform-v2-r39.py` `fe0be179…`,
`count-c7-r39.py` `b92c65f2…`, `gate-v2-bb1f2457.py` `62cd4132…`). The checker's
`PREDICATE` literal and the contract's P-C10 blockquote are the same 1564
characters (whitespace-normalised equal).

**Before control (round-39 v2 bytes, measured at `bb1f2457`).** The extracted
instrument (`fixtures/extracted/conform-v2-r39.py`, `sha256 fe0be179…`) printed
`CONFORM=met` / `EXIT=0` on eight survivors — `c10-red-shadow-none.txt`,
`c10-red-shadow-neg.txt`, `c10-red-cond.txt`, `c10-red-inf.txt`,
`c10-red-decoy.txt`, `c10-red-underscore.txt`, `c10-red-second-popen.txt`,
`c10-red-tuple.txt` — and on the two-counter audit `c10-red-multicounter.txt`.
`c10-red-divzero.txt` shows the setup-error route instead:
`conformance setup error: division by zero` / `EXIT=2` with no `check` line.
The checker copy with its own `("selftest_conjunct", …)` entry gutted still
printed `CONFORM_SELFTEST pass=8 fail=0` / `EXIT=0` (`c10-red-conjunct.txt`).

**After (round-40 v3, measured at `265a955cc`).** `c10-after.txt` prints nine
`check … PASS` lines and ends `CONFORM=met` / `EXIT=0`. `c10-after-selftest.txt`
carries eleven arms, each of the form `-> only <check> failed`, and ends
`CONFORM_SELFTEST pass=11 fail=0` / `EXIT=0`. Each of the nine survivors plus
the two-counter audit prints `CONFORM=unmet` / `EXIT=1`, and the failing check is
the new one:

| receipt | failing line (quoted) |
|---|---|
| `c10-after-shadow-none.txt` | `check timeout_scope      FAIL (survivor-shadow-none.py: bounded=[] value=['line 115 (communicate): non-numeric constant'])` |
| `c10-after-shadow-neg.txt` | `… value=['line 115 (communicate): timeout value -1 is not positive']` |
| `c10-after-cond.txt` | `… value=['line 116 (communicate): non-numeric constant']` |
| `c10-after-inf.txt` | `… value=['line 114 (communicate): timeout value inf is not finite']` |
| `c10-after-divzero.txt` | `… value=['line 114 (communicate): fold error: division by zero']` |
| `c10-after-decoy.txt` | `check drain_bind         FAIL (survivor-decoy.py: violations=['Popen at line 143 not drained by a bound, consumed communicate in its function'])` |
| `c10-after-underscore.txt` | same `drain_bind` line for `survivor-underscore.py` |
| `c10-after-second-popen.txt` | same `drain_bind` line for `survivor-second-popen.py` |
| `c10-after-tuple.txt` | same `drain_bind` line for `survivor-tuple.py` |
| `c10-after-multicounter.txt` | `drain_bind` and `selftest_conjunct` both FAIL, the second on `survivor-barecomm.py: honest_comm=['communicate without timeout at line 147'] strips=5 detected=5` |

The gutted-conjunct v3 copy prints `CONFORM_SELFTEST pass=0 fail=10` / `EXIT=1`,
with `selftest_conjunct` in **every** arm's `failing=[…]` list
(`c10-after-conjunct.txt`), i.e. the mutation table now reads its own entry.

**Counter parity.** `c10-parity.txt` records `count-c7 sha256:
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520` (equal to the
extracted round-39 bytes), `c7_exit=0`, `c8_exit=0`, `PARITY: receipts
byte-identical` for the recorded seed — the sixteen deleted lines changed no
receipt in that run.

**Residual observation, quoted not judged.** In `c10-after-divzero.txt` the
survivor also flips `predicate`, `head_pin`, `tool_resolve` and `timeout_state`
to FAIL (the crashing counter is the instrument under behavioural test), so that
fixture's receipt shows five FAIL lines where the other eight show one. The
before/after discriminator the contract names is still visible: `EXIT=2` with no
FAIL line before, a `timeout_scope` value violation after.

## C2 — depth (score 5, tied lowest): append-only gate v3, P-C11

**Built.** `tools/mori-sources-appendonly.py` version 3 (197 changed lines in
`git diff --stat bb1f2457 265a955cc`); its `PREDICATE` literal and the contract's
P-C11 blockquote are the same 1036 characters (whitespace-normalised equal). The
output shape is unchanged: per-id lines, `appendonly_violations=…` summary line,
then `supersede_timing …`.

**Before control (v2 bytes, `bb1f2457`).** On the lane (`c11-before-lane.txt`,
`command: python3 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py
bb1f2457 --repo .`) the timing line lists 18 ids and no S226:
`supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]`,
with `appendonly_violations=18` and `EXIT=1`. On the three P-C11 DAG fixtures the
v2 bytes print: dag-n `supersede_timing superseded_as_of=[] stale_supersede=[]`
/ `EXIT=0` (`c11-red-neveredited.txt` — the never-edited superseded row is
omitted); dag-p `changed S001 superseded_by=S002` plus
`supersede_timing superseded_as_of=[] stale_supersede=[S001]` / `EXIT=1`
(`c11-red-firstparent.txt`); dag-r `superseded=[] … round_changed=[S008]` with an
empty timing line / `EXIT=1` (`c11-red-readd.txt`).

**After (v3, measured at `265a955cc`).** `c11-after-selftest.txt` prints
`MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` / `EXIT=0`. On the lane
(`c11-after-lane.txt`, `command: python3 tools/mori-sources-appendonly.py
265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .`) the timing line lists the
35 ids S041, S044, S051, S062, S064, S067, S069, S070, S071, S083, S084, S090,
S093, S096, S097, S101, S124, S127, S128, S129, S131, S140, S179, S180, S181,
S182, S183, S184, S185, S186, S188, S189, S190, S193, S226 with
`stale_supersede=[]` and `appendonly_violations=18` (the same eighteen `changed
… superseded_by=…` lines the v2 receipt prints) / `EXIT=1`. At `e37dcc6`
(`c11-after-e37dcc6.txt`) the timing line drops S226 and S069, lists 33 ids and
ends `stale_supersede=[S069]`. The three fixtures now print the P-C11 verdicts:
dag-n `superseded=[S001] … superseded_as_of=[S001] stale_supersede=[]` / `EXIT=0`
(`c11-after-fixture-n.txt`); dag-p the same `changed S001 superseded_by=S002`
line, `superseded_as_of=[S001] stale_supersede=[]` and `EXIT=1`
(`c11-after-fixture-p.txt`); dag-r `superseded=[S008] … round_changed=[S008]`,
`superseded_as_of=[S008] stale_supersede=[]`, no `changed` line, `EXIT=1`
(`c11-after-fixture-r.txt`).

**Eligible-set delta, counted from the before/after pair.** The after set is the
before set plus 17 ids and minus none: S067, S070, S071, S083, S084, S090, S093,
S096, S097, S101, S124, S127, S128, S129, S131, S140, S226. Static cross-check
over the committed registry: `git show 265a955cc:corpus/SOURCES.md | grep -oE
"supersedes S[0-9]+" | sort -u` yields 36 tokens of which one is the prose
literal `S0`, leaving 35 ids — the same 35 the receipt lists; `ede486b7` yields
the same 35.

## Frontier and surroundings the claims rest on

- **S229** is registry row 235 of `corpus/SOURCES.md` (Python execution model —
  naming and binding; copy `corpus/evidence/sources-r40/S229.src`, 869 lines).
  The knowledge entry `corpus/knowledge/conform-scope-r40.md` carries
  `source:`/`verified-at: 2026-10-24`/`recheck: on-release` lines, quotes the
  15-word rule, and closes `Used by claim C1 of round 40
  (.ufo/waves/round-40/contract.md, P-C10)`. That is C1's sourced grounding, not
  execution evidence.
- **Census pair**: `census-start.txt` and `census-end.txt` are byte-identical
  (both `sha256 d823173352f740d3495cbf6ebcab456a775e22133d84ffad1661275318d14319`,
  re-derived here). Each lists the same 16 standing `W04` duplicate-URL rows
  (S035, S037, S073–S076, S147–S150, S166, S168, S201, S218, S220, S228) and
  closes `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`;
  no S229 row appears in either. **Limit:** the receipts carry no exit-status
  line, so "census exit 0" is the lesson's sentence, not receipt bytes.
- **Lesson**: `corpus/lessons/round-40.md` (59 lines, committed at `8d3badd`)
  mines two mistakes — M23 inherited-unverified-freeze and M24 number-drift — and
  records the re-add "honest-stop" disposition, so the round's ≥1-mistake
  requirement is met on paper (content unverified here).
- **Erratum**: `corpus/lessons/round-39-erratum.md` (28 lines) carries the
  finding-11 wording correction, the S227 18→17-word correction, the r39
  `pass=11`→12 correction and the nonexistent fixture-path correction.

## Conflicts — reported verbatim for the canonical judge

1. **C2 lane as-of count.** Frozen contract, C2 after-cell (`contract.md:137`)
   declares `supersede_timing superseded_as_of=[19 ids incl. S226]
   stale_supersede=[]`; its kill rule (`contract.md:145`) says "mismatches the
   declared 19 ids"; the wave context and the ExeGateLane routing entry say "34
   as-of ids"; `corpus/lessons/round-40.md` M24 and the SCORECARD after-cell say
   "the measured lane line at T1 lists **34** as-of ids" with the class "16 rows:
   S226 plus 15 earlier". The landed receipt `c11-after-lane.txt` lists **35**
   ids, and the delivery delta is 17 ids, not 1 and not 16. This seat counted the
   line; it did not rerun the gate.
2. **dag-p "no fabricated changed line".** The ExeDagP routing entry asks to
   "confirm the merge contributes no edit (no fabricated changed line)". Both
   receipts print `changed S001 superseded_by=S002` and
   `appendonly_violations=1`; the v2→v3 difference on this fixture is the stale
   verdict, `stale_supersede=[S001]` (red) → `[]` (after), plus
   `superseded_as_of=[]` → `[S001]`. The gate's own selftest row for dag-p
   (`tools/mori-sources-appendonly.py`, `("first-parent-lacks-path merge
   contributes no edits", "dag-p", 1, {…"round_changed": ["S001"]…})`) also
   expects that changed line.
3. **dag-r "no changed event".** The contract's before-cell says v2 "prints a
   `changed` event for the linear delete-then-re-add"; `c11-red-readd.txt` shows
   no `changed` line, only `round_changed=[S008]` / `EXIT=1`. The after receipt
   shows `round_changed=[S008]` / `EXIT=1` as well; the pair discriminates only
   on `superseded`/`superseded_as_of` (`[]` → `[S008]`).

## Replay bounds observed while drafting (no instrument was rerun here)

- `head_pin` compares the counter's `--pin-only` output — `git rev-parse HEAD` of
  the repo (`count-c8.py:404-409`) — against the checker's own `git rev-parse
  HEAD` (`conform.py:520-524`). The receipt's `pin=265a955cc… tip=265a955cc…`
  therefore records HEAD at measurement time; byte-replaying that line requires
  HEAD to still be `265a955cc`. Lane HEAD is now `ede486b7` (read with
  `git rev-parse HEAD`), so a replay prints different hex on both sides while
  still passing.
- `c11-after-selftest.txt` holds only the summary line (3 lines total): the 15
  arms are not individually evidenced in the landed receipt.
- Three receipts carry uncommitted worktree appends by sibling seats
  (`c10-after-selftest.txt` gains a `wall_seconds: 57.371` block and absolutised
  command paths; `c10-after-conjunct.txt`, `c10-red-conjunct.txt` gain absolute
  command paths). All quotes above are from the committed blobs
  (`git show HEAD:<path>`), not the worktree copies.
