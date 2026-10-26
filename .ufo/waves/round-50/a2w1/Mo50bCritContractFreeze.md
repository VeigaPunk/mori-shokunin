# Mo50bCritContractFreeze — attack on the round-50 frozen contract (a2w1)

Seat: critic, wave a2w1. Scope: `contract.md` (P-C1, P-C2, their before/target/control/limit blocks)
against `count-c1.py`, `count-c2.py`, `controls/`, `evidence/`. Read-only on the lane; every write below
is under `/fast/scratch/hyaku/mori-r50/Mo50bCritContractFreeze/`. No tool installed (nothing needed);
pacman not run. MACHINE_ID omitted per lane rule.

Verdict of the attack: **no HIGH finding; the freeze and both before-values hold byte-for-byte, both
counters reproduce, and all 12 committed controls reproduce. Three MED and six LOW findings were found,
all wording, attribution or label defects plus two under-described conditions; none of them changes a
met/unmet verdict at 487941b9395e89678af0053cc443cdb49cdee6e3.** Every measurement below reads git blobs at
R (`git show`), so the working tree's in-flight edit of `corpus/knowledge/oom-memcg-stat-r50.md` (another
seat) does not enter any number here.

## 1. What was verified (command, output, rc)

### 1.1 Frozen bytes (assignment check)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum -c .ufo/waves/round-50/evidence/freeze-sha256.txt
  (no non-OK line)                                 34 entries, 34 OK, 0 FAILED
$ git diff --stat 950e99be6757a52b00e9eb70ae1a1a7bbe2ea379 487941b9395e89678af0053cc443cdb49cdee6e3 \
    -- .ufo/waves/round-50/count-c1.py .ufo/waves/round-50/count-c2.py .ufo/waves/round-50/controls \
       .ufo/waves/round-50/contract.md .ufo/waves/round-50/evidence ...
  .../assimilation/a2/append-block.md   | 3 +
  .../assimilation/a2/live-sha-L1.txt   | 3 +
  .../assimilation/a2/mirror-validate.txt | 25 +++
  .../evidence/selftests/mori-pin-check.txt | 117 +++
  .../evidence/selftests/mori-unlanded-check.txt | 20 +++
  5 files changed, 168 insertions(+)
$ <per-path: git show 487941b9:<path> | sha256sum against freeze-sha256.txt>
  entries=34 bad=0
$ git diff --stat 487941b9 4548a34d -- <.ufo/waves/round-50 frozen set> 
  evidence/a2-c1-at-data.txt | 10 +   evidence/a2-c2-at-data.txt | 2 +
```

Every frozen path is unchanged freeze→data and data→spec tip; the only changes in that range are new,
unfrozen files. Freeze hash list, working tree and data blob all agree (34/34).

### 1.2 Counters at the landed data (487941b9)

```
$ python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 --scratch <scratch>/c1data
item axis coverage expect=round_47_improved got=ok state=ok
item axis operability expect=round_47_improved got=ok state=ok
item axis depth expect=round_49_improved got=ok state=ok
item axis freshness expect=round_28_improved got=ok state=ok
item axis calibration expect=round_49_improved got=ok state=ok
item axis adjacency expect=round_19_improved got=ok state=ok
item pin python3_tools/mori-pin-check.py_--selftest expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=ok
item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
rc=0
$ python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
rc=0
$ python3 count-c1.py --selftest | tail -1   -> C1_SELFTEST pass=34 fail=0
$ python3 count-c2.py --selftest | tail -1   -> C2_SELFTEST pass=31 fail=0
```

Both lines are identical to `evidence/a2-c1-at-data.txt` and `evidence/a2-c2-at-data.txt`; both selftest
counts equal `evidence/selftest-c1.txt` (`C1_SELFTEST pass=34 fail=0`) and `evidence/selftest-c2.txt`
(`C2_SELFTEST pass=31 fail=0`).

### 1.3 Before-values equal the receipts

```
$ python3 count-c1.py 7197160b927f04db294c9553fb48fadcc7a3f4e3
  (8 item lines byte-identical to evidence/control-c1-do-nothing.txt)
C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b... failed=mismatch
$ python3 count-c2.py 7197160b927f04db294c9553fb48fadcc7a3f4e3
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=7197160b... failed=entry_absent,pins
$ git -C /home/vgpnk/Projects/shokunin show e0144996...:MANIFEST.json | sha256sum | cut -c1-12
a94551c5bc8d
```

Contract line 46 ("coverage (cell round 26, MANIFEST 47), operability (31 vs 47), depth (31 vs 49),
calibration (25 vs 49) … `(60/60)` and `(13/13)` … freshness (28) and adjacency (19) already agree")
is exactly what both receipts and my run print. Contract line 106 (`pins=bad … failed=entry_absent,pins`)
is exactly `evidence/control-c2-donothing-git.txt`.

### 1.4 N* targets recomputed independently from the fleet MANIFEST

Parsed `MANIFEST.json` at `e0144996` (750 rounds, key `verdict`, key `lane_round`) with the contract's rule
(mori, verdict `admitted`, round ≤ 49, axis `improved`/`harmed`):

```
coverage 47 improved | operability 47 improved | depth 49 improved
freshness 28 improved | calibration 49 improved | adjacency 19 improved
```

Identical to the counter's `expect=` fields. Note: **operability round 47 is graded `improved` in the
MANIFEST, not `harmed`** — the `harmed` value in `count-c1.py --selftest` belongs to a synthetic manifest
only. Contract text never claims a verdict word for operability (line 46 says "operability (31 vs 47)"), so
this is consistent, but a reader of the selftest could misread it.

### 1.5 The controls were re-run, into scratch (nothing written in the lane)

`controls/c1-controls.py` and `controls/c2-controls.py` were imported as modules, their `EVID`/`WAVE`
globals repointed into scratch, and `main()` run against the entering revision:

```
do-nothing               exit=1 C1=unmet items=8 pins=2 boxes=4 mismatches=6 failed=mismatch
all-latest               exit=1 C1=unmet items=8 pins=2 boxes=4 mismatches=6 failed=mismatch
pins-deleted             exit=1 C1=unmet items=6 pins=0 boxes=4 mismatches=4 failed=mismatch,pins_floor
pins-updated-no-receipt  exit=1 C1=unmet items=8 pins=2 boxes=4 mismatches=6 failed=mismatch
axes-only                exit=1 C1=unmet items=8 pins=2 boxes=4 mismatches=2 failed=mismatch
shonen-only              exit=1 C1=unmet items=8 pins=2 boxes=4 mismatches=4 failed=mismatch
box-dropped              exit=1 C1=unmet items=6 pins=0 boxes=3 mismatches=4 failed=boxes_floor,mismatch,pins_floor
witness                  exit=0 C1=met   items=8 pins=2 boxes=4 mismatches=0
controls rc=0
do-nothing   C2=unmet ... pins=ok failed=entry_absent
staged-r46   C2=unmet ... failed=claims_floor,provenance,source_rows,sources_floor,table
staged-r47   C2=unmet ... failed=claims_floor,provenance,source_rows,sources_floor,table
staged-rows  C2=unmet ... failed=claims_floor,provenance,source_rows,sources_floor,table
controls2 rc=0
```

Every control reproduces its frozen receipt in every field except the per-clone fixture `rev=` hashes
(a fresh `git clone --shared` yields new commit ids; the receipts' ids are therefore not re-derivable, but
the edits they encode are, and the results are identical).

### 1.6 Surface facts the contract asserts

- Entering Axes scores at `7197160b` (`SCORECARD.md` `## Axes`): coverage 6, operability 7, depth 5,
  freshness 5, calibration 5, adjacency 6 — matches contract lines 9–10; depth/freshness/calibration tied lowest at 5.
- The calibration definition quoted at contract line 15 is `/home/vgpnk/Projects/shokunin/AXES.md:15`
  ("SHONEN.md/SCORECARD entries match observed repo state").
- The routed item at contract lines 24–25 is `corpus/lessons/round-49-verifier-spotcheck.md:111` (§5 item 2,
  "Commit a selftest output file for the tools … the 114/114 and 17/17 tallies resolve at closure time").
  (It asks for `.ufo/waves/round-50/evidence/`; the receipts sit in `evidence/selftests/`, a subdirectory —
  satisfied in substance.)
- Assimilation census: `wc -l` reg-ids 261, staged-ids 136, collisions 18, quarantine-slice 3 (S244/S262/S268);
  `grep -cx S533 reg-ids` → 0, rc=1. Guard proof: `grep -cE '^ {0,3}\| *(S533|S534)' guard-proof/registry.md`
  → 2, rc=0; the column-0-only pattern `'^\\| *(S533|S534)'` → 0, rc=1. Both halves of contract lines 137–140 hold.
- `evidence/sweep-memcg-stat.txt` matches contract lines 75–80 (five terms at 0 with rc=1; `anon-rss`/`shmem-rss`
  once in `oom-tracepoints-r47.md`; `oom_kill.c` URL non-zero, disclosed).
- `tools/` and `SKILL.md` are unchanged from 950e99be to 487941b9 (`git diff --stat` empty), so the selftest
  tallies at freeze and at data coincide.

## 2. Findings

### F1 — MED — P-C2 does not state the condition the counter measures (provenance clause)

Counterexample (the strongest locally available): delete the `source: S491 — …` line from the landed entry
and score it with the frozen `evaluate()` at R. Every sentence of P-C2 (contract lines 93–102) still holds —
header `claim|source|quote`, 22 rows, quotes unique and located in the three copies, 3 sources drawn, copies
pinned, `source:`/`verified-at:`/`recheck:` present — yet the counter returns:

```
C2=unmet claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=bad rev=487941b9... failed=provenance
```

Evidence: `count-c2.py:132-134` (`head = …[:14]`, `src_lines`, `has()`), `count-c2.py:193-198`
(`ids_in_table <= cited`), contract lines 93–94 ("opens with source: lines, verified-at: and recheck:").
The reverse direction also diverges: inserting 4, 5, 6 and 7 non-blank prose lines *before* `source:` still
scores `C2=met … provenance=ok`; 10 lines fail (the window is 14 non-blank lines). So the sentence is both
under- and over-specified: the code adds "the `source:` lines cite every table S-id" and replaces "opens
with" by a 14-line window.

Impacted axes: depth (claim text vs measurement), calibration (the contract is the claim's rule).
Smallest safe correction: none to the data (it satisfies the stricter code) and none to the frozen counter;
carry the exact wording — "the first 14 non-blank lines carry `source:`, `verified-at:`, `recheck:`, and the
`source:` lines name every S-id used in the table" — as a round-50 named limit and as the round-51 sentence.

### F2 — MED — the counter's own predicate header asserts a false equivalence

`count-c1.py:3` says the text below is "the same sentence in contract.md, this counter and the receipt
label"; `count-c1.py:16` ends it with "Met iff mismatches=0 and errors=0." That clause exists in neither
`contract.md` (lines 29–41) nor any receipt, and it is false for the code: `evaluate()` gates on `hidden`,
`pins_floor`, `boxes_floor`, `axes` as well (`count-c1.py:214-231`, `met = not failed`).

Counterexample: drop SHONEN.md line 5 (the first checklist box — a line that carries no pin) from the data
revision and score the overlay:

```
C1=unmet items=8 axes=6 pins=2 boxes=3 mismatches=0 errors=0 hidden=0 … failed=boxes_floor
```

`mismatches=0 errors=0` and still unmet. (Dropping lines 5, 6 or 8 gives the same isolated `boxes_floor`.)

Impacted axes: calibration.
Smallest safe correction: the counter is frozen, so record in the round-50 limit list that the C1 predicate
is "met iff no condition of (a)/(b) and of the floors fails", and that `count-c1.py:16`'s iff is an erratum.
No data change: the landed tip is met under both readings.

### F3 — MED — the `box-dropped` control cannot isolate the floor it is cited for, and contract line 63 misstates it

`contract.md:63` reads "box-dropped | `boxes=3 … boxes_floor` unmet | deleting a box fails". The control
(`controls/c1-controls.py`, `box_idx[2]`) deletes SHONEN.md line 7, which is the *only* line carrying both
tally pins, so its receipt reads:

```
C1=unmet items=6 axes=6 pins=0 boxes=3 mismatches=4 errors=0 hidden=0 … failed=boxes_floor,mismatch,pins_floor
```

(reproduced in scratch: identical). The unmet verdict is fully explained by `pins_floor` + `mismatch`; the
control adds nothing to the box floor. contract line 63 also omits `pins=0`, `mismatch` and `pins_floor`
from a row that reads as a quoted result. A pure box-floor control does exist — drop line 5 with the pins
intact and the counter prints `mismatches=0 … failed=boxes_floor` (F2's probe) — and the selftest arm
`box_deleted_unmet` (`count-c1.py`, `shonen(boxes=3)`, pins kept) isolates it too.

Impacted axes: calibration (controls are the feasibility evidence for the self-assessment claim).
Smallest safe correction: keep the receipt, fix the row's attribution in the round-50 limit list (or the
round-51 contract), and make the next round's box control delete a pin-free box line. No data or counter change.

### F4 — LOW — the C1 pin predicate is broader than P-C1 states (`→` accepted)

`contract.md:37-38` lists exactly two pin forms: `` `(N/M)` `` or `` `-> `PREFIX pass=N fail=K`` ``.
`count-c1.py:49-51` accepts `(?:→|->)`. Counterexample: rewrite the landed SHONEN pin as
`` `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=114 fail=0` `` and score at R:

```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0
```

A form the contract does not list as a tally pin satisfies the ≥2 floor, and `PIN.sub` removes it before the
hidden scan (`count-c1.py:153-156`), so it is also invisible to "no other tally token".

Impacted axes: calibration. Smallest safe correction: limit-list note ("the counter also accepts the U+2192
arrow form"); no data change (SHONEN.md uses the fraction form).

### F5 — LOW — `axes=6` is a constant and the `axes` failure reason is dead code

`contract.md:30` presents `axes=6` as part of the printed measurement; `count-c1.py:229`
(`if sum(1 for i in axis_items) != len(AXES)`) can never fire, because `check_axes` emits exactly one item
per axis unconditionally; `axes=` is `len(axis_items)` = 6 always. Counterexample: append a seventh row
`| test | 1 | nothing | round 1 |` to the data Axes table → `C1=met … axes=6`. Extra non-axis rows are
ignored (`count-c1.py:123`), and `## Axes` is located by the first heading only (`count-c1.py:99-105`).

Impacted axes: calibration. Smallest safe correction: none to the data; note that "exactly one row for each
of the six axes" is enforced per-axis, not as a row-count, and that `axes=6` carries no signal.

### F6 — LOW — contract line 112 enumerates three C2 control reasons; the receipts list five, and all three controls stop at the first gate

`contract.md:111-113`: "each unmet (`table`, `claims_floor`, `source_rows`)". The receipts (reproduced exactly
in scratch) read `failed=claims_floor,provenance,source_rows,sources_floor,table`. Because the staged r46/r47
entries carry no `claim|source|quote` table, `claims=0` in all three, so `claims_floor`, `source_rows` and
`sources_floor` are consequences of the missing table; the S533 row that `staged-rows` appends to SOURCES.md
is never consulted (no row is parsed), so that control tests nothing about the row format. `controls/c2-controls.py`
is honest about this in its docstring; the contract row reads as three independent reasons.

Impacted axes: depth. Smallest safe correction: limit-list note with the five-reason receipt text; the
entry-level conditions themselves are isolated in `C2_SELFTEST` (31/31, arms `row_not_mined_unmet`,
`row_opened_other_day_unmet`, `used_by_missing_unmet`, `escaped_pipe_quote_located`), which I reproduced.

### F7 — LOW — the C1 receipts are freeze-time transcripts, not R-time transcripts, and are checked by string membership only

`evidence/selftests/mori-pin-check.txt:1` and `mori-unlanded-check.txt:1` are stamped
"git archive of 950e99be…", while `contract.md:39` says the pin command is "run at R (git archive of R…)".
The counter's check (`count-c1.py:196`) is `got in [l.strip() for l in receipt.split("\n")]` — any file
carrying the right line passes, with no command, revision or exit-code check. This is harmless here only
because `tools/` is unchanged between 950e99be and R and my R run prints exactly `PIN_CHECK_SELFTEST
pass=114 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`; the receipt's own provenance line contradicts the
"at R" wording, and none of the named limits (contract lines 67–70) names the membership-only check.

Impacted axes: calibration. Smallest safe correction: add "the receipt is a freeze-time transcript checked by
line presence, not an R-time execution record" to the round-50 limit list; no data change.

### F8 — LOW — `source_rows=ok` does not mean what the target line implies

`contract.md:108` uses `source_rows=ok` in the target line without a definition; `count-c2.py:199` defines it
as `"ok" if (ids_in_table and not bad) else "bad"` — i.e. "at least one table S-id was seen and no row failed
*any* check", which folds claim-cell, quote and SOURCES-row failures into the label. A row with a fine source
row and a short claim still prints `source_rows=bad`.

Impacted axes: depth, calibration. Smallest safe correction: define the label in the limit list; the data's
`source_rows=ok` is true under either reading (bad_rows=0), and I verified S489–S491 are 11-cell rows with
`status=mined`, `opened=2026-10-26`, used-by `corpus/knowledge/oom-memcg-stat-r50.md`, one row per id.

### F9 — LOW — the freeze sentence over-covers `assimilation/`

`contract.md:6-7` lists "the assimilation scratch under `assimilation/`" among what "are committed in one
freeze commit". `assimilation/a2/{append-block.md,live-sha-L1.txt,mirror-validate.txt}` were added in the data
commit 487941b9 and are not in `freeze-sha256.txt`. Nothing in the contract cites them, so no claim is
affected; the sentence should be read as "the 9 files listed in freeze-sha256.txt".

Impacted axes: none (housekeeping). Smallest safe correction: none required; note the scope.

## 3. Named limits this seat adds (for the round report)

1. Contract wording and counter code differ in the three places above (F1, F4, F5): the contract is the claim's
   rule but not a full description of the measurement.
2. The C1 pin receipts are freeze-time transcripts checked by line presence (F7); the control receipts' fixture
   commit ids cannot be re-derived (clone deleted), only their edits and results.
3. The fleet MANIFEST is trusted as written (the counter does not re-judge closures) — contract already names this.
4. Not this seat's remit and still open: the per-row re-opening of the 22 C2 claims against the text around each
   quote (contract lines 116–118 assign that to the wave-2 reviewers).

## 4. Kill rules at the landed tip

`C1=met` and `C2=met` at 487941b9395e89678af0053cc443cdb49cdee6e3 — neither kill rule fires. The freeze's own
promise ("if working-tree bytes ever differ, the claim is measured with `git show <freeze>:<path>`") holds:
the counters run from git at R, and all 34 frozen blobs match their listed sha256.

## Findings

| # | Severity | Finding | Concern |
|---|---|---|---|
| F1 | MED | P-C2 omits the provenance condition the counter enforces (every table S-id cited in the `source:` lines within the first 14 non-blank lines); the same evidence shows "opens with" is a 14-line window, not a prefix condition | `.ufo/waves/round-50/contract.md:93-94`; `.ufo/waves/round-50/count-c2.py:132-134,193-198`; `corpus/knowledge/oom-memcg-stat-r50.md:3-7` |
| F2 | MED | `count-c1.py:16` "Met iff mismatches=0 and errors=0" is false (floors and hidden also gate) and the file's "same sentence" header (line 3) is contradicted; probe prints `mismatches=0 errors=0 … failed=boxes_floor` | `.ufo/waves/round-50/count-c1.py:3,16,224-231`; `.ufo/waves/round-50/contract.md:29-41` |
| F3 | MED | `box-dropped` deletes the only pin-carrying SHONEN line, so it cannot isolate `boxes_floor`, and contract line 63 quotes an incomplete result (`pins=0`, `mismatch`, `pins_floor` omitted) | `.ufo/waves/round-50/contract.md:63`; `.ufo/waves/round-50/controls/c1-controls.py:108-109,121`; `.ufo/waves/round-50/evidence/control-c1-box-dropped.txt:8`; `SHONEN.md:7` |
| F4 | LOW | P-C1 lists two pin forms; the counter also accepts the `→` token form, which then satisfies the ≥2 pin floor and the hidden scan | `.ufo/waves/round-50/contract.md:37-38`; `.ufo/waves/round-50/count-c1.py:49-51` |
| F5 | LOW | `axes=6` in the printed line is a constant and the `axes` failure branch is unreachable; an extra non-axis row is ignored while "exactly one row for each of the six axes" is presented as a measurement | `.ufo/waves/round-50/contract.md:30`; `.ufo/waves/round-50/count-c1.py:123,229-230` |
| F6 | LOW | Contract gives three failure reasons for the staged C2 controls; the receipts list five, and all three controls fail at `table` (claims=0), so the appended S533 row is never parsed | `.ufo/waves/round-50/contract.md:111-113`; `.ufo/waves/round-50/evidence/control-c2-staged-*.txt:2` |
| F7 | LOW | The C1 receipts are stamped `git archive of 950e99be`, not R, and the counter checks them by line membership only; neither the "run at R" wording nor this weakness is in the named limits | `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt:1`, `mori-unlanded-check.txt:1`; `.ufo/waves/round-50/count-c1.py:196`; `.ufo/waves/round-50/contract.md:39,67-70` |
| F8 | LOW | `source_rows=ok` is defined as "some table S-id seen and no bad rows", not as the SOURCES rows' health, and the target line uses it undefined | `.ufo/waves/round-50/contract.md:108`; `.ufo/waves/round-50/count-c2.py:199` |
| F9 | LOW | The freeze sentence covers "the assimilation scratch under `assimilation/`", but `assimilation/a2/*` was added at the data commit and is not in `freeze-sha256.txt` (uncited by any claim) | `.ufo/waves/round-50/contract.md:6-7`; `.ufo/waves/round-50/evidence/freeze-sha256.txt`; `.ufo/waves/round-50/assimilation/a2/` |
