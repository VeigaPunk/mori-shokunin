# Mo52ScribeLog — LOG.md `## Round 52` entry draft

Seat: `Mo52ScribeLog` (scribe, round 52 wave `w1`). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`; freeze `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`; data
`8524904adb25e44f24d9f25aac7eae909625c18c`; HEAD while drafting `075436b1346ca659afb8be7a46f0e67e4170aa83` (wave
spec/dispatch only). Output: this report; the entry draft is fenced in §2 and nothing outside it. No lane file was
edited; `LOG.md` was read only.

Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ScribeLog/` created and removed (`rmdir`; it stayed empty) — no clone,
no work tree, no fixture and no temp file was needed, because every read below is `git show`/`git diff`/`git log`
plus file reads. No heavy run, so `scripts/hyaku/disk-guard.sh` was not consulted. No tool installed or upgraded.
No host read beyond the reports' citations.

Reading cut for the vote tallies in the draft: **2026-10-27T00:20:09Z**, at which `w1/` held 46 reports, all 12
ENTAILMENT seats had landed, and the wave was still running. Every number that can still move is marked
`[L1 fills]` in the draft; the counts that were only partial at my first cut (00:18Z: 40 reports, 11 voters) were
re-taken at 00:20Z.

## 1. What I read (evidence for the draft)

```
$ git -C <lane> log --oneline -8
075436b1 round-52: wave w1 spec (68 seats, v2 validated; copy-on-change amend for the refused labrat role), dispatch, receipts at data
8524904a round-52: data — …                                             # the data commit
d3a8ea59 round-52: freeze — contract, C1/C2 counters with selftests, C1 controls and receipts, census-start, sweep, five v7.2 source copies
4f266ef2 round-51 verifier spot-check (integrator, hyaku): non-author admit/reject

$ cat .ufo/waves/round-52/evidence/{c1-at-data,c2-at-data,c2-hashes-at-data,control-c1-do-nothing,control-c2-do-nothing,census-start,freeze-sha256}.txt
$ tail -3 .ufo/waves/round-52/evidence/selftest-c1.txt   ->  C1_SELFTEST pass=42 fail=0 / exit=0
$ tail -3 .ufo/waves/round-52/evidence/selftest-c2.txt   ->  C2_SELFTEST pass=45 fail=0 / exit=0
$ git diff --stat d3a8ea59 8524904a -- .ufo/waves/round-52/{contract.md,count-c1.py,count-c2.py,controls,evidence} corpus/evidence/sources-r52
  …/evidence/selftests/mori-pin-check.txt      | 128 +++++
  …/evidence/selftests/mori-unlanded-check.txt |  20 ++
  2 files changed, 148 insertions(+)                    # frozen bytes untouched; only receipts added
$ git diff --stat 4f266ef2 8524904a -- .ufo/waves/round-51   -> (empty)  rc=0
$ git show --stat --oneline 8524904a                      -> 7 files: 2 receipts, SCORECARD, QUALITY, README, SOURCES, entry
$ git show 8524904a -- SHONEN.md                          -> (empty)  # SHONEN.md byte-identical; receipts are the new files
$ git show 8524904a:corpus/QUALITY.md | tail -26          -> criteria 141, 142
$ git show 8524904a:corpus/README.md   | tail -16         -> "## Round-52 corrections (living pins)", bullets at :727, :728
$ git show 8524904a:SCORECARD.md | sed -n '1,20p'         -> axes 6/7/5/5/5/6 unchanged at data
$ git ls-tree --name-only d3a8ea59 .ufo/waves/round-52/evidence/   -> 8 C1 controls incl. witness, C2 do-nothing, selftests, census, sweep
$ grep -n 'VOTERS' .ufo/waves/round-52/count-c2.py        -> :44 VOTERS = ["Mo52Ent%02d" % i for i in range(1, 13)]
$ git status --porcelain | grep -v 'round-52/w1/'         -> round-39/scratch/, check-history-rows.py, evidence/m2-history-rows.txt, w1.ready*, corpus/lessons/round-52.md
$ cat .ufo/waves/round-52/evidence/w1-validate-refused.txt ; cat .ufo/waves/round-52/build-w1-spec-amend.py
$ cat .ufo/waves/round-52/evidence/m2-history-rows.txt   -> HISTORY_ROWS changed=6 … ; changed=0 at 8524904a
$ ls -la .ufo/waves/round-39/scratch/mori-conform-selftest-afzrnaq4   -> 7 counter-*.py, ~22 KB each, mtime 21:16-21:17
$ w1 reports: 40 read/grepped by name; vote lines counted with
  grep -hE '^ENTAIL [0-9a-f]{12} (entailed|overclaim)' w1/*.md   -> 77 lines, 28 distinct hashes, all >=2 voters
```

Wave roster read from `.ufo/waves/round-52/w1-spec.json` (68 items): 12 ENTAILMENT (`Mo52Ent01`-`Mo52Ent12`, three
per seven-row block), 7 executors on C2, 6 C2 attackers/reviewers, 2 connectors, 2 sentinels, 9 executors and 6
attackers on C1, 2 revengers, 5 scribes, 2 scouts, 6 reviewers/auditors, 1 simplifier, plus the lab-writes probe.

## 2. Draft — `LOG.md` `## Round 52` entry (append-only; fenced)

````markdown
## Round 52 (L1 MoriR52, attempt 1; C1 calibration, C2 depth)

Entering tip `4f266ef2`; freeze `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2` (contract, both counters with their
`--selftest`, the C1 data applier and control builder, eight C1 control receipts including the disclosed witness,
the C2 do-nothing receipt, census-start, the overcommit sweep, five v7.2 source copies pinned by sha256 in
`evidence/freeze-sha256.txt`); data `8524904adb25e44f24d9f25aac7eae909625c18c`; wave spec
`075436b1346ca659afb8be7a46f0e67e4170aa83` (68 seats, v2-validated; the frozen builder was amended
copy-on-change by `build-w1-spec-amend.py` after the validator refused `items[39].role "labrat"`,
`evidence/w1-validate-refused.txt`); integration `[L1 fills]`. One v2 wave `w1` ran after the data commit, as
frozen. Motivating evidence: round-51 closure `corpus/lessons/round-51-verifier-spotcheck.md` §5 items 1-8 and
round-50 closure §5 item 3 (carried).

- C1 (calibration): `count-c1.py <rev>` runs four arms — (A) the six `## Axes` rows against the fleet MANIFEST
  and the newest closure's per-axis scores, (B) the four SHONEN pins with their receipts, (C) every single-line
  command-tally pin in `corpus/QUALITY.md` and `corpus/README.md` (supersession, never rewrite), (D) `path:N`
  locators in the Axes rows and the SHONEN boxes. Entering `4f266ef2`: `C1=unmet items=37 axes=6 pins=2 boxes=4
  living=4 superseded=1 locators=25 mismatches=8 errors=0 hidden=0 lane_writes=0 failed=mismatch`, exit 1
  (`evidence/control-c1-do-nothing.txt`) — the eight named in the contract. At data `8524904a`: `C1=met items=42
  axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0`, exit 0
  (`evidence/c1-at-data.txt`): the Axes operability and depth `Last change` cells now lead with the round-51
  closure (scores unchanged at 6/7/5/5/5/6); the two SHONEN pins resolved by the round-52 selftest receipts added
  under `evidence/selftests/` (SHONEN.md's bytes are identical between entering tip and data); QUALITY 141-142 and
  the README `## Round-52 corrections` block supersede the two stale pins one line each instead of rewriting them
  (`pass=12` → `pass=22` for the append-only gate, and a runnable form for the bare `--selftest`); the freshness
  locator moves `SCORECARD.md:1771` → `:1781`. At the landed tip `[L1 fills]` (`evidence/c1-at-landed.txt`).
  Selftest `C1_SELFTEST pass=42 fail=0` (`evidence/selftest-c1.txt`). Controls: the seven isolating controls tabled
  in the contract plus the witness (`C1=met … mismatches=0`, `evidence/control-c1-witness.txt`), disclosed as the
  L1's feasibility build with the data applier, not the claim's landing. Named limits the wave added (frozen
  counter, routed to
  round 53): two stale README pins sit outside arm (C) — `corpus/README.md:579` pins `PASS 4 cases` where the
  drift tool now prints `PASS (6 cases)`, and `:580` pins `Self-test PASS 8 cases` where the gate prints
  `pass=22` (`w1/Mo52ExecC1Unenumerated.md`) — a hand-written receipt satisfies the receipt arm, the newest
  closure file is trusted verbatim, and a `supersedes` line needs no replacement pin
  (`w1/Mo52CritC1Junk.md`); the `lane_writes` arm is a working-tree diff that reads a concurrent sibling report as
  a write (`w1/Mo52RevC1Counter.md`).
- C2 (depth): `corpus/knowledge/overcommit-commit-limit-r52.md` — what `CommitLimit` and `Committed_AS` are at
  kernel v7.2: the commit ledger, enforced only under `vm.overcommit_memory=2`, `vm_commit_limit()`, the per-CPU
  batched `vm_committed_as` and its approximate read, `__vm_enough_memory`, the user and admin reserves, and
  `MAP_NORESERVE` — rows S497-S501 (`Documentation/mm/overcommit-accounting.rst`,
  `Documentation/admin-guide/sysctl/vm.rst`, `mm/util.c`, `include/linux/mman.h`, `mm/mmap.c`, copies under
  `corpus/evidence/sources-r52/`). Entering `4f266ef2`: `C2=unmet claims=0 … sources=0 source_rows=bad pins=bad
  provenance=bad failed=entry_absent,pins` (`evidence/control-c2-do-nothing.txt`). At data `8524904a`: `C2=unmet
  claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0
  dissent=0 failed=entailment` (`evidence/c2-at-data.txt`) — every row priced and located, unmet only because no
  ENTAILMENT vote existed yet, which is the designed reading at data. Votes: the twelve seats
  `Mo52Ent01`-`Mo52Ent12`, three per seven-row block; at this entry's draft cut (2026-10-27T00:20Z, 46 of 68
  reports, 12 of 12 voters) 84 vote lines covered all 28 rows at ≥2 voters each, with two `overclaim` votes and
  three replacement lines on one row (hash `93b4fe285dc7`), so C2 stood at `dissent>0` and the replacement still
  owes two non-author `entailed` votes on its new hash. Landed reading and the vote resolution `[L1 fills]`.
- Frontier: census start rc 0, 23 W04 + `ok` (`evidence/census-start.txt`); registry rows 269 → 274 at data
  (tier A 238 → 243, `mined` 219 → 224), exactly the five announced ids and no other row moved
  (`w1/Mo52ExecCensusCounts.md`); census end `[L1 fills]`; sourced claim C2 on S497-S501 (five rows opened
  2026-10-26); assimilation none (`merge/mori/` holds no overcommit entry or row; `evidence/sweep-overcommit.txt`);
  considerthese `2026-10-26.md` suggestion 3 (re-execute what closures only evidence-verified) ran and agreed —
  the round-51 frozen C1 counter at `70e68cdd` reads `C1=met kill_residue=0 relocated=met reloc_mismatch=0
  classified=ok selftest=pass=125,fail=0` with every field matching `c1-at-landed.txt`, and the round-51 C2
  counter reads `C2=met claims=21 located=21 entailed=21 dissent=0` at `70e68cdd`, identical at `4f266ef2`,
  `d3a8ea59`, `8524904a` and `075436b1` because it reads no round-52 surface (`w1/Mo52ExecR51C1Rerun.md`,
  `w1/Mo52ExecR51C2Rerun.md`); the old counter's one-voter arm is no support for the hardened one, and the
  closures' evidence-verified readings are now re-executed for both claims; mistakes
  M1-M4 below; QUALITY 141-142 and the README block landed at data; SKILL `## Round52` `[L1 fills]`, SCORECARD
  `## Round 52` `[L1 fills]`, SHONEN boxes `[L1 fills]`, lesson `corpus/lessons/round-52.md` `[L1 fills]` (an
  untracked draft existed at 21:12, not part of the data commit).
- Mistakes carried into the lesson (`w1/Mo52ScribeMistakes.md`, M1-M4): M1 a living pin pinned at one round's tally
  and never superseded (`corpus/QUALITY.md:909`, `corpus/README.md:608`: `pass=12` while the committed gate has
  printed 22 since the round-41 freeze `d72ac167`; `corpus/README.md:607` pins a `--selftest` that names no
  command), and K4 had been closed for SHONEN only — every earlier counter reads 0 pins in the two living
  documents; M2 a closure's locators drift and nothing re-greps them (round-51 D-c: four of the eight
  `show_mem.c` locators in `corpus/lessons/round-51.md:83-84` name spans that do not hold the construct; erratum
  draft `w1/Mo52ScribeErratum51.md`, landing `[L1 fills]`); M3 the self-assessment lagged the fleet record by one
  round — both Axes cells led with an earlier round at the entering tip while the MANIFEST had admitted round 51
  (arm A, `control-c1-do-nothing.txt`), the recurrence of the lag the table's own Round-50 correction paragraph
  records; M4 a frozen file edited in place stays undetected — `.ufo/waves/round-40/conform.py` still differs from
  its round-40 freeze digest (`5025b966…` vs `7f5174d5…`) and no later freeze pins that path, so round 52's
  "edits none" is a policy, not a detector.
- Routed defects (round-51 §5): 1 → both counters ship a real `--selftest` (`C1_SELFTEST pass=42 fail=0`,
  `C2_SELFTEST pass=45 fail=0`, frozen at `d3a8ea59`); 2 → P-C2's entailment arm hardened — the frozen `VOTERS`
  list (`count-c2.py:44`), ≥2 votes per row, no vote from a text's author, unfenced lines only; at data
  `entailed=0` over 28 located rows shows the arm bites; 3 → the round-51 C1 counter is frozen and untouched
  (`git diff 4f266ef2 8524904a -- .ufo/waves/round-51` empty) and the wave mutation seat killed 10 of 12
  single-point mutants, naming the ten arm-isolating controls it fired (verdict word-boundary and single
  `## Axes` heading and Score cell for arm A; regular-file pin path and receipt presence for arm B; `pin_removed`
  bytes, the same-line quotation-replacement rule and `rc==0` for arm C; locator quote/pair content and
  `lane_writes` for arm D), while two MED survivors (a `startswith` verdict comparison and a dropped
  `cur != crit` guard in `superseded`) are routed as round-53 checks (`w1/Mo52MutC1Arms.md`); 4 → C1, with K4 taken
  beyond SHONEN to the living pins of QUALITY and README, and LOG.md and the SCORECARD round sections ruled dated
  records before data — attacked in `w1/Mo52CritC1Scope.md`, which names `SCORECARD.md:1070` as a present-tense
  tally outside every arm: a named limit routed to round 53; 5 → appended erratum `[L1 fills]` (no
  `corpus/lessons/round-51-erratum.md` at `8524904a`: `git ls-tree 8524904a corpus/lessons/` has none); 6 → no
  frozen file edited in place: the freeze→data diff over the frozen paths adds only the two selftest receipts, and
  the refused wave spec was amended copy-on-change; 7 → receipts carry the literal command they ran
  (spot-checked; the sentinel inventory `Mo52SentReceipts` `[L1 fills]`); 8 → the read-only inventory
  `Mo52ExecWritersConform` and `Mo52ExecWritersCounters` `[L1 fills]`, and the class is demonstrated live by the
  residue below: the data's own `corpus/README.md:728` bullet runs the round-39 `conform.py`, whose absolute
  `LANE`/`SCRATCH_ROOT` put its `mkdtemp` work dirs inside the lane.
- Lane residue: `.ufo/waves/round-39/scratch/` (`mori-conform-selftest-*`, up to four work dirs, ~450 KB) written
  by wave seats running the frozen round-39 instrument; deletion and its receipt `[L1 fills]`. Nothing else
  untracked outside `w1/` except the L1's own `check-history-rows.py`, `evidence/m2-history-rows.txt`,
  `w1.ready`, `w1.ready.partial`, and the untracked `corpus/lessons/round-52.md`.
- Not done, stated (deviations, routed defect 5): `[L1 fills]` for everything the integration owes — the landed
  C1/C2 readings, SHONEN/SCORECARD/SKILL/lesson integration, the erratum, the census end, the residue deletion,
  the lesson section the re-execution lands in, and the C2 row-3 vote resolution. Deviations observed at draft
  time: (a) the three `-at-data` receipts were written at 21:08 and land in `075436b1`, not in the data commit, so
  a seat reading them "at DATA" finds nothing at `8524904a`; (b) the contract's pre-freeze note records one edit
  of `controls/c1-data.py` before freeze with only the living-only and witness controls re-run; (c) the witness
  control is the L1's own feasibility build, disclosed in the contract table; (d) the data commit message names
  "SHONEN round-52 receipts" while SHONEN.md is byte-identical between `4f266ef2` and `8524904a` — the receipts are
  the new files under `evidence/selftests/`; (e) `corpus/README.md:728` publishes a command that writes into the
  lane (the residue above), a data correction the L1 may still take. Nothing beyond the data commit had landed
  when this entry was drafted: HEAD was `075436b1` (wave spec, dispatch, `-at-data` receipts) and every `w1`
  report was untracked.
````

Append arithmetic (asked by `Mo52ScribeShonen`): `LOG.md` is 2805 lines and ends with a newline; entries are
separated by one blank line (`:2764` blank, `:2765` the round-51 heading). Appended at EOF after one blank line, the
draft's heading line lands at **`LOG.md:2807`**; the existing `LOG.md:2765-2805` and `LOG.md:2732-2763` locators
stay valid, and `count-c1.py` arm (D) reads both ranges (`evidence/c1-at-data.txt`). Any other content appended to
`LOG.md` before this entry shifts it.

## 3. `[L1 fills]` checklist (each is a fact only the integration can supply)

1. Integration commit(s) and their SHAs (round-51 used two parts plus a final); the wave-results commit.
2. `evidence/c1-at-landed.txt` and `evidence/c2-at-landed.txt` readings at the landed tip (C2 must show
   `entailed=N dissent=0` with `N ≥ 12`, or the claim stays unverified under the frozen kill rule).
3. The C2 row-3 resolution: which of the two announced replacement texts was taken, and the two non-author
   `entailed` votes on its new hash.
4. The lesson section the considerthese re-execution lands in (the runs themselves are recorded in the entry: both
   round-51 counters agree, field by field).
5. Erratum landing (`corpus/lessons/round-51-erratum.md`, from `w1/Mo52ScribeErratum51.md` §4).
6. Census end receipt and its W04 count (start: rc 0, 23; registry 269 → 274 at data).
7. Residue deletion receipt for `.ufo/waves/round-39/scratch/mori-conform-selftest-*` and for the L1's untracked
   wave-dir files (`check-history-rows.py`, `evidence/m2-history-rows.txt`, `w1.ready*`).
8. Dispositions of routed defects 5, 7 and 8 after the pending seats land (`Mo52ScribeErratum51` §4,
   `Mo52SentReceipts`, `Mo52ExecWritersConform`, `Mo52ExecWritersCounters`, `Mo52ExecLogPinsHistory`,
   `Mo52ExecScorecardPinsHistory`, `Mo52ExecC1Unenumerated`, `Mo52ExecC1Controls`, `Mo52LabLaneWrites`,
   `Mo52ScribeMistakes`), and whether the two MED arm survivors from `Mo52MutC1Arms` are routed or fixed.
9. SKILL `## Round52`, SCORECARD `## Round 52`, SHONEN box lines and the lesson body.
10. Whether the data corrections flagged in §4 (README :728 text, S497/S499 anchors, entry row-3 wording,
    entry :14 citation) were taken before the landed measurement, and the new data revision if so.

## 4. Findings

- **HIGH — `corpus/README.md:728` (data, round-52 appended block) with `.ufo/waves/round-39/conform.py:53-54,491-492`.**
  The data publishes `python3 .ufo/waves/round-39/conform.py 4f266ef2… --selftest` as a runnable living pin. The
  instrument derives `LANE` and `SCRATCH_ROOT` from its own absolute path and passes `dir=` to `mkdtemp`, so
  neither `TMPDIR` nor a `git archive` of R moves the write: it writes `mori-conform-selftest-*` dirs inside the
  committed lane tree. Observed live during this wave: `.ufo/waves/round-39/scratch/mori-conform-selftest-afzrnaq4`
  holding seven ~22 KB `counter-*.py` files at 21:16-21:17, and (per `w1/Mo52SentBoundary.md` §5) up to four
  concurrent work dirs, 24 entries, 450137 bytes at 21:11-21:15. QUALITY 141's disclosure "run in a `git archive`
  of the tip with `TMPDIR` in scratch" is therefore false for this pin. Data correction (allowed) or an appended
  note naming the real write target, and a round-53 successor-freeze item (defect 8).
- **HIGH — `.ufo/waves/round-52/count-c1.py:527,534,562` (`lane_writes`), receipt
  `evidence/c1-at-data.txt` (`lane_writes=0`).** The guard samples `git status` once after evaluation: a write the
  instrument removes in its own `finally`, or one leaving only an empty directory, is invisible (independently
  reproduced in `w1/Mo52SentBoundary.md` F2), while an untracked sibling seat report reads as a lane write
  (`w1/Mo52RevC1Counter.md` F1 replayed the frozen counter at `8524904a` and got `C1=unmet … lane_writes=5` from
  five concurrent `w1/*.md` reports). `lane_writes=0` at data is therefore not evidence of a write-free run, and a
  re-run during a live wave cannot read `met`. Frozen counter: named limit, routed to round 53.
- **HIGH — C2 row 3 (hash `93b4fe285dc7`) is contested and not yet resolvable from the landed reports.** Two voters
  (`Mo52Ent01`, `Mo52Ent03`) vote `overclaim` and file replacement texts; three replacement lines carry two
  distinct texts, one of them filed twice at `w1/Mo52Ent01.md:64,133`. Under the frozen kill rule the row clears
  only when the replacement's new hash draws two non-author `entailed` votes; at the 00:20Z cut, with all 12 voters
  landed, the counter could still see only the 28 original hashes and no new-hash vote, so
  `C2=met … dissent=0` is not reachable without a residual dispatch. Two different texts for one hash also make
  "which replacement the counter takes" a reading the entry must state.
- **HIGH — `.ufo/waves/round-52/count-c1.py` `check_pins`/`closure_scores`/`check_living` (frozen counter).** The
  wave's junk-path critic demonstrated three edits that make the counter print `met` without measuring:
  a hand-written receipt in `evidence/selftests/*.txt` satisfies the receipt arm (nothing checks the receipt was
  produced by running the pinned command), a fabricated newest closure file sets every axis score, and a
  `supersedes` line needs no replacement pin (`w1/Mo52CritC1Junk.md:132-141`, variants A/B/C). Named limits for
  round 53; no counter change proposed.
- **MED — arm (C) enumerates fewer pins than the contract's "every single-line pin" claim.**
  `corpus/README.md:579` pins `PASS 4 cases` where `tools/mori-source-drift.py --selftest` now prints `PASS (6
  cases)`, and `:580` pins `Self-test PASS 8 cases` where the gate prints `pass=22`; both are stale, unsuperseded
  and outside arm (C) (`w1/Mo52ExecC1Unenumerated.md` findings 1-2). Also `SCORECARD.md:2209,2238` pin a bare
  `--selftest` that the instrument cannot run without a revision (`w1/Mo52ExecScorecardPinsHistory.md` F1) — a
  diagnosed K4-class defect the scope decision excludes as history.
- **MED — a frozen file is still divergent from its freeze digest.**
  `.ufo/waves/round-40/conform.py` hashes `7f5174d5…` against `5025b966…` in
  `.ufo/waves/round-40/evidence/freeze-r40.txt`, and no later freeze pins that path. Round 52 edited no frozen file
  (verified) but detects nothing: M4 in the lesson is a policy, not a check.
- **MED — `evidence/c1-at-data.txt`, `evidence/c2-at-data.txt`, `evidence/c2-hashes-at-data.txt` are not in the
  data commit.** `git ls-tree 8524904a .ufo/waves/round-52/evidence/` lists the freeze receipts and the two
  selftests only; the three `-at-data` receipts were written at 21:08 and land in `075436b1`, while every wave
  seat is pointed at them "at DATA" (`w1/Mo52SentBoundary.md` F5). Provenance is genuine (first line is the
  literal command at `8524904a`), but the pointer is one commit early. Draft wording ("at data") is accurate; the
  deviation is recorded in the entry.
- **MED — S497/S499 anchor cells in `corpus/SOURCES.md:276,278`.** `45` should be `48` and `83-84` should be
  `83-85` (the only listed gap is line 85, which the entry's own ptrace claim quotes), and S499's `901-1006`
  overruns `__vm_enough_memory` into `get_cmdline()`'s kernel-doc ending at 1003
  (`w1/Mo52RevSourcesRows.md` §1, `w1/Mo52ExecAnchorCheck.md` §Findings 1-3). Data corrections the L1 may take.
- **MED — `corpus/knowledge/overcommit-commit-limit-r52.md` `## Boundaries` (71-72) asserts a numeric bound
  ("up to the batch size per CPU") that none of the five copies contains, and reading-rules row 2 (59) makes an
  unsourced ordering claim about `MemAvailable` (`w1/Mo52CritC2Prose.md` findings 1-2). The bound is derivable —
  `w1/Mo52ExecBatchDeviation.md` measures 968 pages/CPU under mode 2 and 61956 pages/CPU under modes 0/1 on this
  host — but the entry as landed cites no line for it.
- **LOW — `git show 8524904a -- SHONEN.md` is empty.** The data commit message names "SHONEN round-52 receipts"
  while the SHONEN pins' text still points at round-51 receipt paths; the pins resolve because `count-c1.py` looks
  the receipt up by basename in the round's `evidence/selftests/`. Accurate as a mechanism, misleading as a
  message.
- **LOW — untracked L1 artifacts in the lane.** `.ufo/waves/round-52/check-history-rows.py`,
  `.ufo/waves/round-52/evidence/m2-history-rows.txt`, `w1.ready`, `w1.ready.partial` and
  `corpus/lessons/round-52.md` exist at HEAD `075436b1` but in no commit. Not part of the data; the entry claims
  nothing for them beyond naming them as L1 drafts.
- **LOW — the data commit's own living-pin rule is narrower than the round-51 target.** Routed defect 4 asked for
  K4 beyond SHONEN including LOG; round 52 rules LOG.md and the SCORECARD round sections dated records and
  `w1/Mo52CritC1Scope.md` falsifies that rationale with `SCORECARD.md:1070` ("Existing census125/125" —
  present-tense, stale within its own round, outside every arm). The delivered arms are consistent on what they
  run; the scope is a named limit for round 53.

Report: `.ufo/waves/round-52/w1/Mo52ScribeLog.md`
