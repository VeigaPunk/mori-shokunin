# Mo98CritC2 — C2 calibration falsification attempt (mori round 98, wave w1)

Critic seat. Target claim: C2 — at landing 600deb7ed2695f54b289cf5b6c3931e0fa9c8bb3, every SCORECARD `## Axes`
Last-change cell leads with the highest admitted mori closure round grading the axis improved/harmed, Score and
Evidence cells unchanged; registered gate `tools/mori-scorecard-calibration.py` (entering bytes, sha
662fafde7ba446e13a30bc88c10a61d99f933be72902053b1e1e871fc5835113) prints `C1=met axes=6 mismatches=0
columns_unchanged=yes`. Entering b2a67ce562bbf2f0cc73f47d8e79f792badf5e63; freeze b75e26ccd771b872099ef7233a61e3e91d9f6f7a.
All commands read-only (`git -C`, python over `git show`/committed receipts). Scratch
/fast/scratch/hyaku/mori-r98/Mo98CritC2 removed after this report.

## Verdict

**C2 holds.** Attribution re-derived independently from MANIFEST.json matches the new cells exactly; the do-nothing
control fails at entering; the SCORECARD delta is exactly the two Last-change cells with the history prepended
byte-identically; no non-claimed cell moved. Ignored-surface mismatches exist (§5) but none is inside P2's
declared surface and each is either a named limit on record or pre-existing debt.

## 1. Do-nothing control at entering — fails, so P2 separates

`TMPDIR=$S python3 .ufo/waves/round-98/count-c2.py b2a67ce562bbf2f0cc73f47d8e79f792badf5e63 --work $S` (re-run today):

```
C2=unmet mismatches=2 columns_unchanged=yes tool=ok tool_rc=1 mismatched_axes=operability,freshness rev=b2a67ce562bb
exit=1
```

Byte-identical in outcome to the frozen receipt `evidence/before-c2.txt`. A do-nothing control does not reach P2.
Gate run directly at entering (its own per-axis lines): only
`axis operability cell=round_93_improved expect=round_97_improved state=mismatch` and
`axis freshness cell=round_82_improved expect=round_97_improved state=mismatch`; the other four axes `state=ok`.
Landing: `C2=met mismatches=0 columns_unchanged=yes tool=ok tool_rc=0 mismatched_axes=- rev=600deb7ed269` exit 0 —
matches `evidence/landing-c2.txt`.

## 2. Independent re-derivation from MANIFEST.json — attribution confirmed

Re-derived with python over /home/vgpnk/Projects/shokunin/MANIFEST.json (filter lane=mori, admitted is True,
verdicts[axis] in {improved, harmed}, max round), 1386 fleet rounds, 87 mori entries, 59 admitted mori closures,
max mori round 97:

| axis | derived highest admitted improved/harmed | landing cell lead | match |
|---|---|---|---|
| coverage | (80, improved) | round 80 (improved, score held) | ok |
| operability | (97, improved) | round 97 (improved, score held) | ok |
| depth | (86, improved) | round 86 (improved, score held) | ok |
| freshness | (97, improved) | round 97 (improved, score held) | ok |
| calibration | (93, improved) | round 93 (improved, score held) | ok |
| adjacency | (19, improved) | round 19 (improved, score held) | ok |

r94/r95/r96 are `rejected-honest-stop` (not admitted — correctly not counted); no admitted mori improvement in
operability between 93 and 97 nor in freshness between 82 and 97, so the entering cells were exact as of the
r93/r82 admissions and the fix is the minimal correct prepend. rounds[1384] is mori r97 (admitted;
verdicts.operability=improved, verdicts.freshness=improved, others unchanged, capabilities_added=[]) — the exact
closure the new cells attribute. rounds[1385] is kaidoku r98, filtered by the gate's lane=mori check. b6d03408
(r97 closure commit) is an ancestor of entering (`merge-base --is-ancestor` rc 0, 1 commit between).

## 3. Thin-bookkeeping attack — rejected

§9 (mori-round-98.md:547-569) requires a calibration claim to *count* mismatches between self-assessment and
observed state, not assert; and a target a do-nothing control cannot reach. Both hold: the mismatch count is the
metric (2 → 0, §1), the control fails, and the instrument is the registered gate whose `--selftest` on entering
bytes passes `CALIB_SELFTEST pass=11 fail=0` (11 arms including stale-cell, not-admitted-higher, verdict-word,
Score-cell and Evidence-cell mutations). AXES.md:15 calibration = "SHONEN.md/SCORECARD entries match observed
repo state". This is the same work class as the accepted r50 correction (4 cells) and r79 correction (5 cells);
two cells is smaller only because r97 graded exactly two axes improved. §9 "prefer 2 claims" is satisfied
(13 seats, C1+C2). Not thin.

## 4. Harm check — none on the C2 surface

`git diff --stat b2a67ce..600deb7e` = 24 files: C1 surface (tools/mori-userns-runway.py, SKILL.md +12,
PROVINCE.md +6, corpus/SOURCES.md +4, corpus/evidence/sources-r98/*, corpus/knowledge/userns-runway-r98.md), wave
artifacts (contract, counters, controls, receipts, candidate/, census, journal capture), and the two r97
late-seat reports the contract's entering sentence names as routed D1 (w1/Mo97ScoutLive.md, w1/Mo97ScribeLog.md).
SCORECARD.md is `4 +-` = exactly its two rewritten rows. Cell-by-cell (split on `|`): only cell 3 (Last change)
differs in each row; cells 0–2 (Axis, Score, Evidence) byte-identical; and the new cell is exactly
`round 97 (improved, score held); ` + the old cell (verified byte-exact for both axes — nothing dropped). The
gate itself pins Score/Evidence to base 66c5518e (`columns_unchanged=yes`), and
tools/mori-scorecard-calibration.py is absent from the diff; my `sha256sum` of the entering bytes equals the
counter's TOOL_SHA. count-c2.py at landing hashes d6fe755fff2e2805c6550ff9bfe0b53c369d5dd8c9799fe4e02bd1e5e73c01fd,
equal to the pin on line 1 of landing-c2.txt (the counter is absent at entering, as expected — committed with the
freeze). No duplicate authority, no identity change, no premature saturation introduced.

## 5. Other SCORECARD self-assessment vs record — mismatches I can show (none inside P2's surface)

1. **Evidence cells (all six axes) name stale "latest admitted closure" rounds.** Landing axes table, Evidence
   cells: operability "latest admitted closure grades operability improved (blind-writer gate …)" citing round-31;
   freshness citing round-28; coverage round-47; depth round-49/50; calibration round-49/50. MANIFEST's latest
   admitted are 97/97/80/86/93 (§2). Show: `python3` cell extraction of
   `git show 600deb7e:SCORECARD.md` + the §2 derivation. This is a **named limit** on record — SCORECARD's own
   round-79 correction paragraph: "Named limit: this predicate grades the `Last change` clause only, not the
   `Evidence` cell" — and the gate *enforces* Evidence-cell stasis via columns_unchanged, so the round could not
   fix these cells without breaking its own frozen predicate. Disclosed tension, not a hidden regression.
2. **Capabilities register (r35 `## Capabilities` section, "one row per capability that a non-author closure
   admitted") holds 20 keyed rows, last `rounds[832]` (lane round 56); MANIFEST records 79 admitted capabilities
   across the 59 closures.** 59 entries from rounds 36–53 and 62–93 have no keyed register row (post-r56
   capabilities entered per-round `### capabilities:` tables instead; the r35 section had superseded those tables
   as the canonical record). Pre-existing divergence, not touched by r97 (capabilities_added=[]) and not named in
   the contract's Not-claimed list. Candidate calibration work for a future round; demonstrate by comparing
   `[(r['round'],j) for admitted mori rounds for j,_ in enumerate(capabilities_added)]` (79) against the
   `` | `rounds[N].capabilities_added[j]` `` register rows (20).
3. **Stagnation window.** The r13 declaration sets "Stagnation window N = 3 admitted rounds without a capability
   entering the table"; 29 admitted mori closures have round > 56 (last keyed register row). Which table resets
   the clock (per-round tables gained rows through r87) is undefined on the record; the divergence in (2) makes
   the nudge unauditable from the register alone. Observation only.
4. **Live-MANIFEST dependency (robustness note, not a defect).** The gate reads the live
   /home/vgpnk/Projects/shokunin/MANIFEST.json, not a pinned copy; fleet commit 9d1a14f3 (kaidoku r98 ledger,
   18:29:58 -03) landed between freeze (b75e26cc, 18:19:03) and landing (600deb7e, 18:30:38), adding
   rounds[1385]. Output is unaffected only because the gate filters lane=mori; my re-runs today reproduce both
   frozen receipts, so no drift occurred. Stability is incidental, not enforced by the instrument.

## 6. Checks not run

- SHONEN.md calibration conformance (AXES.md names SHONEN.md too; C2's frozen surface is SCORECARD-only — out of
  scope for this verdict, not run).
- Live re-execution of the Evidence cells' cited lesson files (staleness shown from the cells vs MANIFEST only).
- Whether any admitted mori closure between r35 and r97 stated a new axis score that the Score cells ignore
  (scores are not recorded in MANIFEST verdicts; not derivable from the manifest alone — unrun).
