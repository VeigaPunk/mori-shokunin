# Mo50bScribeLogScorecard — drafts for `LOG.md` `## Round 50` and `SCORECARD.md` `## Round 50`

Seat: scribe, round 50 attempt 2 wave a2w1. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Assignment: draft (fenced, never applied) the `LOG.md` `## Round 50` entry and the `SCORECARD.md` `## Round 50`
section in the house shape of the existing tail entries, carrying the entering tip, the freeze, the salvage, the
data rev, the scores entering, both claims with counting commands, the before/after counter lines quoted from the
named receipts, controls, named limits, the round-49 routed defects 1–8 with `[L1 fills]` markers, and the
correction entry for the round-49 "48 of 49" report count.

I edited no lane file. I ran no counter, no census, no freeze check and no clone: every figure below is either read
from a committed receipt (path named) or measured with a read-only git/`ls`/`grep` command (command and output
quoted). Where I could not measure, the text says UNVERIFIED or leaves `[L1 fills]`.

Scratch: none created. The directive's scratch root `/fast/scratch/hyaku/mori-r50/Mo50bScribeLogScorecard/` was not
needed (no clone, no fixture, no temp tree); the two `/tmp` list files I used to diff report names were removed
(`rm -f /tmp/r49_closure.lst /tmp/r49_now.lst`) and are not evidence. Tooling: nothing installed or upgraded;
`pacman` not run; no drive-level maintenance. `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
was read (idle, no heavy run made).

## 1. Observed evidence (commands, output, exit codes)

All paths below are relative to the lane unless written absolute; every command was run with `cwd` = the lane.

1. Report count under the round-49 wave-1 directory, by revision:

```
$ for r in 0df17b7b 24ebc799 43d84666 7197160b 9b8562a3 487941b9 4548a34d; do n=$(git ls-tree -r --name-only $r -- .ufo/waves/round-49/w1/ 2>/dev/null | grep -c '\.md$'); echo "$r md=$n"; done
0df17b7b md=0
24ebc799 md=0
43d84666 md=47
7197160b md=48
9b8562a3 md=49
487941b9 md=49
4548a34d md=49
```

On disk today: `ls .ufo/waves/round-49/w1/ | wc -l` → `50`; `ls .ufo/waves/round-49/w1/*.md | wc -l` → `49`; the
one non-`.md` entry is `swarm-registry.json`. The difference between `43d84666` (47) and today (49) is exactly
`Mo49ExecCounterTiming.md` and `Mo49SimpCounters.md` (`diff` of the sorted name lists, rc 1, two `>` lines); both
files' mtimes are 2026-10-25 23:39 and 23:02, i.e. after the round-49 landing (`43d84666`, 22:57 committer date),
and both enter tracking at `7197160b` and `9b8562a3` respectively
(`git log --format='%h %ad %s' --date=short -- .ufo/waves/round-49/w1/Mo49ExecCounterTiming.md .ufo/waves/round-49/w1/Mo49SimpCounters.md`
→ `9b8562a3 …` and `7197160b …`).

2. The wrong number's location. Tracked lane markdown outside `.ufo/waves/` mentioning the figures:

```
$ git ls-files '*.md' | grep -v '^\.ufo/waves/' | xargs grep -n "48 of 49\|48 wave-1\|48 reports\|48 report files"
corpus/lessons/round-49-verifier-spotcheck.md:26: … "48 wave-1 reports" … The lesson and `LOG.md` still carry the wrong number. …
corpus/lessons/round-49.md:7: … (48 of 49 reports on disk when this lesson was written). …
corpus/lessons/round-49.md:212: - Seat accounting for wave 1: 49 seats dispatched; 48 reports on disk at writing; …
```

(`LOG.md:1356` also matches, but it is the round-19 wave-2 figure "wave2 retains48 reports" and is unrelated.)
`git ls-files '*.md' | grep -v '^\.ufo/waves/' | xargs grep -n "47 of 49\|47 reports\|47 report files"` → no match
(rc 123 from `xargs` on no-match).

3. `LOG.md` does not carry the wrong number:

```
$ git log --oneline 43d84666..HEAD -- LOG.md      # no output
$ grep -n '^## Round 49' LOG.md
2724:## Round 49 (L1 MoriR49, attempt 1)
$ sed -n '/^## Round 49 (L1 MoriR49/,/^## /p' LOG.md | grep -nE 'report|wave 1|seats'
3:Entering tip … ; freeze `0df17b7b` …
7:- Not done, stated: no wave 2 (round total 49 seats, below the 64 floor); … 
```

The round-49 section (`LOG.md:2724-2730`) carries no wave-1 report count; `git show 43d84666:LOG.md` shows the same
seven lines. The lesson file is byte-identical at `43d84666` and at HEAD (`sha256sum corpus/lessons/round-49.md` and
`git show 43d84666:corpus/lessons/round-49.md | sha256sum` both
`6e8d9f6a028bcbb6399ac18c23019c8a12b480929aa46359f44397b02f69870c`).

4. Counter receipts quoted below (verbatim last lines; `exit=` lines from the same files):

```
control-c1-do-nothing.txt        C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch   exit=1
a2-c1-at-data.txt                C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3            exit=0
control-c2-donothing-git.txt     C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=entry_absent,pins   exit=1
a2-c2-at-data.txt                C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3   exit=0
```

Per-item lines of `a2-c1-at-data.txt` (8 items, all `state=ok`): coverage/operability `expect=round_47_improved`,
depth/calibration `expect=round_49_improved`, freshness `expect=round_28_improved`, adjacency
`expect=round_19_improved`; pins `expect=(114/114) got=PIN_CHECK_SELFTEST_pass=114_fail=0` and
`expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0`.

Other control verdict lines read from `evidence/` (`grep -E '^(C1=|C2=)' | tail -1` per file):

```
control-c1-all-latest.txt              ... mismatches=6 … failed=mismatch
control-c1-axes-only.txt               ... mismatches=2 … failed=mismatch
control-c1-shonen-only.txt             ... mismatches=4 … failed=mismatch
control-c1-pins-deleted.txt            pins=0 boxes=4 mismatches=4 … failed=mismatch,pins_floor
control-c1-pins-updated-no-receipt.txt ... mismatches=6 … failed=mismatch
control-c1-box-dropped.txt             items=6 pins=0 boxes=3 mismatches=4 … failed=boxes_floor,mismatch,pins_floor
control-c1-witness.txt                 C1=met … mismatches=0 (feasibility witness)
control-c2-do-nothing.txt              source_rows=bad pins=ok provenance=bad … failed=entry_absent
control-c2-staged-r46.txt              failed=claims_floor,provenance,source_rows,sources_floor,table
control-c2-staged-r47.txt              failed=claims_floor,provenance,source_rows,sources_floor,table
control-c2-staged-rows.txt             failed=claims_floor,provenance,source_rows,sources_floor,table
```

5. Counter and tool selftest receipts:

```
$ tail -1 .ufo/waves/round-50/evidence/selftest-c1.txt   -> C1_SELFTEST pass=34 fail=0
$ tail -1 .ufo/waves/round-50/evidence/selftest-c2.txt   -> C2_SELFTEST pass=31 fail=0
$ sed -n '1p;$p' .ufo/waves/round-50/evidence/selftests/mori-pin-check.txt
$ python3 tools/mori-pin-check.py --selftest   (git archive of 950e99be…; TMPDIR=<scratch>; 2026-10-26T05:49:15-03:00)
exit=0
$ sed -n '1p;$p' .ufo/waves/round-50/evidence/selftests/mori-unlanded-check.txt
$ python3 tools/mori-unlanded-check.py --selftest   (git archive of 950e99be…; TMPDIR=<scratch>; 2026-10-26T05:49:22-03:00)
exit=0
$ sha256sum .ufo/waves/round-50/evidence/selftests/*.txt
406c0be203ff9c715165971172ee577ed1486194c782597210336956015f4af9  …/mori-pin-check.txt
392907ac94422e169119e0e0c249f5296c9c23deb01557a11f7d1eda62b1183a  …/mori-unlanded-check.txt
```

Line counts: `mori-pin-check.txt` 117 lines, `mori-unlanded-check.txt` 20 lines (`sed -n '1,4p;$p'` reads confirm the
first arm line and the closing `exit=0`). The `--selftest` last line inside those files was not re-read in full by me
(the C1 counter's `pins=2` re-runs them at R); the receipts' own `exit=0` plus the counter's pin lines are the
evidence I quote.

6. Data-rev diff surface (`git diff --stat 7197160b 487941b9`, tail): 58 files changed, 15507 insertions, 5
deletions; among them `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md` (+3), `corpus/knowledge/oom-memcg-stat-r50.md`
(+83), the three copies under `corpus/evidence/sources-r50/`, `considerthese/2026-10-26.md` (+60),
`evidence/selftests/`, `evidence/selftest-c1.txt`, `selftest-c2.txt`, `sweep-memcg-stat.txt`, `w1/` (5 reports) and
`a2w1/`. `git rev-parse HEAD` at my read: `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`.

7. Entry shape (`corpus/knowledge/oom-memcg-stat-r50.md`, 83 lines): header, three `source:` lines (S489, S490,
S491, each "opened 2026-10-26"), `verified-at: 2026-10-26`, `recheck: 90d` with three sha256 values, `coverage-map:
FR1`, a `| claim | source | quote |` table at lines 19–42 (1 header + 1 separator + 22 claim rows), and a
`## Boundaries` section (detection and report only; no remediation). SOURCES rows at `corpus/SOURCES.md:268-270`.

8. Freeze and census receipts: `evidence/freeze-sha256.txt` has 34 non-comment lines (`grep -vc '^#'`);
`evidence/census-start.txt` ends `mori ok …/corpus/SOURCES.md` then `census-rc=0`, with 21 `W04` duplicate-URL
lines (`grep -c W04` → 21).

9. Debris measured (read-only): `ls -d .scratch/*/ | wc -l` → `183`; `find . -maxdepth 4 -name
'mori-conform-selftest-*'` → 0 lines; `git ls-files | grep -c 'mori-conform-selftest'` → 0;
`ls .ufo/waves/round-40/scratch` → `mutconform-arms2`, `selftest-v3-draft.txt`, `selftest-v3-draft2.txt`;
`.ufo/waves/round-50/__pycache__` exists and is ignored by `.gitignore:3:__pycache__/` (0 tracked files).

10. Scores entering, read at the entering tip: `git show 7197160b:SCORECARD.md | sed -n '6,14p'` → coverage 6,
operability 7, depth 5, freshness 5, calibration 5, adjacency 6.

UNVERIFIED by me: the fleet `MANIFEST.json` at `e0144996…` (I did not open the fleet repo); the a2w1 seat
settlement (24 `.md` files present at my read of `ls .ufo/waves/round-50/a2w1/*.md | wc -l`, wave still settling);
the freeze sha256 contents (I counted lines, did not run `sha256sum -c`); any host kill record (lane rule).

---

## Draft A — `LOG.md` `## Round 50` entry (append after `LOG.md:2730`)

```md
## Round 50 (L1 MoriR50a2, attempt 2; entering `7197160b`, freeze `950e99be`, data `487941b9`)

Attempt 1 (L1 MoriR50) froze its contract, both counters, the controls, the receipts and the three source copies at
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` from entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`, ran
wave w1 (40 seats dispatched; 5 reports on disk at this read) and died in an orchestrator host crash. The
orchestrator salvaged its unlanded working tree at `9b8562a371dc916fdc0fc686619ea1e271a3e118`, which also carries a
late round-49 seat report. Attempt 2 attacked the landed data in one v2 wave, `a2w1` (64 seats dispatched,
`.ufo/waves/round-50/a2w1-dispatch.json`), and the data landed at
`487941b9395e89678af0053cc443cdb49cdee6e3`. Counter, predicate, control and kill-rule bytes are frozen
(`evidence/freeze-sha256.txt`, 34 non-comment lines) and no amendment was made after a seat had scored.

Scores entering (`SCORECARD.md` `## Axes`, read at `7197160b`): coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6. Both claims work a lowest (tied 5) axis — C1 calibration, C2 depth. No score change is
claimed by the lane; the non-author closure rules.

- **C1 (calibration): the self-assessment agrees with the fleet record and with the instruments.** Counting command
  `python3 .ufo/waves/round-50/count-c1.py <rev>` (run from the lane; the fleet repo is its parent, `--fleet-repo`
  overrides). Before, at the entering tip: `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0
  manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch`, exit 1
  (`evidence/control-c1-do-nothing.txt`). The six mismatches are the four lagging Last change cells (coverage round
  26 against MANIFEST 47, operability 31 against 47, depth 31 against 49, calibration 25 against 49) plus SHONEN's
  `(60/60)` and `(13/13)` against `PIN_CHECK_SELFTEST pass=114 fail=0` and `UNLANDED_SELFTEST pass=17 fail=0`;
  freshness (28) and adjacency (19) already agreed. After, at the data rev: `C1=met items=8 axes=6 pins=2 boxes=4
  mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3`, exit 0
  (`evidence/a2-c1-at-data.txt`). The four corrected cells lead with rounds 47, 47, 49 and 49, keep the older
  history after a `;`, and each Evidence cell names the newer round's closure file; SHONEN's two tally pins read
  `(114/114)` and `(17/17)` and cite committed receipts
  `evidence/selftests/mori-pin-check.txt` (117 lines, `exit=0`) and
  `evidence/selftests/mori-unlanded-check.txt` (20 lines, `exit=0`) — the round-49 routed defect 2. The counter's
  `manifest=` field is a content digest of the fleet `MANIFEST.json` it read; it is not the fleet revision
  `e0144996…` the contract pins.
- **C2 (depth): the memcg OOM report block and what `memory.stat` says about a killed cgroup's charge (FR1).**
  Counting command `python3 .ufo/waves/round-50/count-c2.py <rev>`. Before: `C2=unmet claims=0 located=0
  quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad
  rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=entry_absent,pins`, exit 1
  (`evidence/control-c2-donothing-git.txt`; this is the counter run against the real entering rev, where the three
  copies under `corpus/evidence/sources-r50/` are absent, so `pins` fails as well). After:
  `C2=met claims=22 located=22 quote_missing=0 bad_rows=0
  sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3`, exit 0
  (`evidence/a2-c2-at-data.txt`). The entry `corpus/knowledge/oom-memcg-stat-r50.md` (83 lines) carries 22 claim
  rows over the usage/limit/failcnt line, the
  `Memory cgroup stats for <path>:` block, the per-victim `Killed process` fields, the `memory.stat` keys and their
  units, and the memcg-versus-global split (`__show_mem`); it rests on S489 (cgroup-v2 v7.2), S490 (memcontrol.c
  v7.2) and S491 (oom_kill.c v7.2), all opened 2026-10-26, with committed copies under
  `corpus/evidence/sources-r50/`.
- Controls stay unmet before data (C1 `evidence/control-c1-*.txt`, C2 `evidence/control-c2-*.txt`): C1 do-nothing
  `mismatches=6`; all-latest `mismatches=6`; pins-deleted `pins=0 … failed=mismatch,pins_floor`;
  pins-updated-no-receipt `mismatches=6`; axes-only `mismatches=2`; shonen-only `mismatches=4`; box-dropped
  `boxes=3 … failed=boxes_floor,mismatch,pins_floor`. C2 do-nothing `failed=entry_absent`; the git do-nothing
  `failed=entry_absent,pins`; the staged r46 entry, the staged r47 entry, and the staged r46 entry plus row S533 —
  each byte-exact — `failed=claims_floor,provenance,source_rows,sources_floor,table`. Feasibility witness disclosed
  (`evidence/control-c1-witness.txt`): both halves plus receipts, built by the L1's script, meet the C1 predicate —
  feasibility only, not the claim's landing.
- Counter selftests, committed receipts: `evidence/selftest-c1.txt` → `C1_SELFTEST pass=34 fail=0`;
  `evidence/selftest-c2.txt` → `C2_SELFTEST pass=31 fail=0`.
- Frontier, assimilation, considerthese, mistake: census at round start `evidence/census-start.txt` (rc 0; 21 W04
  duplicate-URL warnings plus `ok`); one assimilation theme and one entry (`oom-memcg-stat-r50.md`), staged S533
  renumbered by document to S489 with staged S534/S539 not adopted, collision check
  `assimilation/{reg-ids,staged-ids,collisions}` (261 registry ids, 136 staged, 18 collisions S471–S488), guard
  proof `assimilation/guard-proof/`, quarantine slice S244/S262/S268 left closed ([L1 fills] the final census and
  collision figures); considerthese `2026-10-26.md` suggestion 2 (host-path portability count) → QUALITY
  [L1 fills]; mistake mined: the self-assessment drift C1 measures.
- Named limits, stated before data: the Score column is not checked (the MANIFEST holds verdicts, not scores); the
  counter reads the Last-change convention, not whether another convention would be better; the hidden scan covers
  SHONEN.md only; a matching tally proves the instrument prints it at R, not that its arms are good; the MANIFEST is
  fleet-written and the counter trusts it; a located quote proves the quoted words occur in the committed copy, not
  that the claim cell follows from them; the three-new-words floor is a floor; v7.2 code says nothing about other
  kernels or cgroup v1; no host OOM block is read (no kernel MESSAGE grep — S351/QUALITY 15), so the entry states
  what the kernel prints, not what a past kill on this host printed.
- Round-49 closure routed defects (`corpus/lessons/round-49-verifier-spotcheck.md` §5; each disposition is the L1's
  to state): 1 author date — the report is filed in two fleet commits so the last author date is after the lane tip
  [L1 fills]; 2 selftest output files — done at the data rev:
  `evidence/selftests/mori-pin-check.txt` (117 lines, `exit=0`, sha256 `406c0be203ff9c715165971172ee577ed1486194c782597210336956015f4af9`)
  and `evidence/selftests/mori-unlanded-check.txt` (20 lines, `exit=0`, sha256
  `392907ac94422e169119e0e0c249f5296c9c23deb01557a11f7d1eda62b1183a`), cited by SHONEN's pins and measured by C1's
  `pins=2` [L1 fills the disposition]; 3 the 48-vs-47 erratum — the correction entry below; 4 `.scratch/` and the
  round-40 scratch dirs — the seven `mori-conform-selftest-*` dirs are no longer on disk (`find . -maxdepth 4 -name
  'mori-conform-selftest-*'` → 0; `git ls-files` → 0), `.ufo/waves/round-40/scratch/` still holds
  `mutconform-arms2/` and two `selftest-v3-draft*.txt`, and `.scratch/*/` stands at 183, unchanged from the round-49
  closure [L1 fills the deletion]; 5 round shape and the report-less round-49 seats — attempt 2 ran one v2 wave of 64
  seats (`a2w1`, 24 reports on disk at this seat's read), and the round-49 late reports are on disk and committed
  (`9b8562a3`) [L1 fills the settlement and the ancestor count]; 6 the `variants=26` versus 27 lines [L1 fills];
  7 K4 (SHONEN.md tally pins measured) is closed by C1's pins with committed receipts, the R11 carve-out and the
  randomised handle stay routed [L1 fills]; 8 the D-g wording [L1 fills].
- Not done, stated: round-end census [L1 fills]; the a2w1 settlement and the dead-seat accounting [L1 fills];
  `.scratch/` deletion [L1 fills]; the round-49 lesson's two wrong sentences [L1 fills] (see the correction below).

### Correction — the round-49 "48 of 49" report count (routed D-c)

Append-only. `corpus/lessons/round-49.md` states "48 of 49 reports on disk" twice (`:7` and `:212`); the file is
byte-identical at `43d84666` and today (sha256
`6e8d9f6a028bcbb6399ac18c23019c8a12b480929aa46359f44397b02f69870c`). The measured count of report files under
`.ufo/waves/round-49/w1/` (`git ls-tree -r --name-only <rev> -- .ufo/waves/round-49/w1/ | grep -c '\.md$'`):
`43d84666` → 47; `7197160b` → 48; `9b8562a3` → 49; `487941b9` → 49. So the lesson's 48 matches no revision at or
before its own commit: at the round-49 landing 47 report files plus `swarm-registry.json` were tracked, which is
what the round-49 report itself says ("47 of 49 on disk at filing";
`.ufo/reports/round-49/mori.md:58`). The two seats that report named as missing — `Mo49ExecCounterTiming` and
`Mo49SimpCounters` — did return: their reports sit in `.ufo/waves/round-49/w1/` (mtimes 2026-10-25 23:39 and 23:02)
and entered tracking with the round-50 entering snapshot `7197160b` (`Mo49SimpCounters.md`) and the salvage
`9b8562a3` (`Mo49ExecCounterTiming.md`), taking the count to 49 of 49.

The spot-check's D-c sentence and the round-49 erratum both add that `LOG.md` carries the wrong number. It does not:
`LOG.md`'s round-49 section (`LOG.md:2724-2730`) never carried a wave-1 report count, and `git log 43d84666..HEAD
-- LOG.md` is empty. The swept figures are therefore: **47** report files at the round-49 landing, **49** on disk
after the two late reports landed (both now committed), **0** wrong in `LOG.md`, **2** wrong in
`corpus/lessons/round-49.md`. `corpus/lessons/round-49-verifier-spotcheck.md` is closure evidence and is left
unedited; the lesson's own two sentences are corrected by [L1 fills] (wording offered in this seat's report, Draft
C).
```

---

## Draft B — `SCORECARD.md` `## Round 50` section (append after `SCORECARD.md:2650`)

Appending after line 2650 places it after the `## Round 49` section, which is the house position (`## Round 49` is
the current end of file). The Axes-table correction for this round is **already landed** at the data rev —
`SCORECARD.md:21-25`, "Round-50 correction (C1, calibration)" — so the section below points at it and does not
restate it as new.

```md
## Round 50 — the self-assessment agrees with the fleet record (C1) and the memcg OOM report block (C2)

L1 MoriR50a2, attempt 2. Entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`; freeze
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (`.ufo/waves/round-50/contract.md`; both counters, the controls, the
receipts and the three source copies committed before any seat); data
`487941b9395e89678af0053cc443cdb49cdee6e3`. Attempt 1 dispatched wave w1 (40 seats, 5 reports on disk) and died in
an orchestrator host crash; the orchestrator salvaged its tree at `9b8562a3`. Scores entering: coverage 6,
operability 7, depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis. No score
change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the self-assessment agrees with the fleet `MANIFEST.json` and with the instruments | calibration 5 | `python3 .ufo/waves/round-50/count-c1.py R` | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch`, rc 1 — `evidence/control-c1-do-nothing.txt` | `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3`, rc 0 — `evidence/a2-c1-at-data.txt` |
| C2 the memcg OOM report block and `memory.stat`, 22 located quotes over 3 sources (FR1) | depth 5 | `python3 .ufo/waves/round-50/count-c2.py R` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=entry_absent,pins`, rc 1 — `evidence/control-c2-donothing-git.txt` | `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3`, rc 0 — `evidence/a2-c2-at-data.txt` |

The C1 landing is in the `## Axes` table and `SHONEN.md`: the correction paragraph under the table
(`SCORECARD.md:21-25` at the data rev) records the four lagging cells and states that scores are unchanged because
no closure states a new number; the four Last change cells now lead with rounds 47, 47, 49 and 49 and each Evidence
cell names the newer round's closure file; SHONEN's two tally pins read `(114/114)` and `(17/17)` and cite committed
receipts `evidence/selftests/mori-pin-check.txt` and `evidence/selftests/mori-unlanded-check.txt`. The C2 landing is
`corpus/knowledge/oom-memcg-stat-r50.md` with rows S489–S491 (opened 2026-10-26) and the three copies under
`corpus/evidence/sources-r50/`.

Controls that skip the work stay unmet (all receipts under `.ufo/waves/round-50/evidence/`): C1 do-nothing
`mismatches=6`, all-latest `mismatches=6`, pins-deleted `pins=0 … failed=mismatch,pins_floor`,
pins-updated-no-receipt `mismatches=6`, axes-only `mismatches=2`, shonen-only `mismatches=4`, box-dropped
`boxes=3 … failed=boxes_floor,mismatch,pins_floor`; C2 do-nothing `failed=entry_absent`, the git do-nothing
`failed=entry_absent,pins`, and the three byte-exact staged-entry controls
`failed=claims_floor,provenance,source_rows,sources_floor,table`. Feasibility witness disclosed:
`control-c1-witness.txt` (both halves plus receipts, built by the L1's script) meets the C1 predicate. Counter
selftests: `C1_SELFTEST pass=34 fail=0`, `C2_SELFTEST pass=31 fail=0` (`evidence/selftest-c1.txt`,
`evidence/selftest-c2.txt`).

No capability row is claimed this round: both counters and both self-testable tools predate round 50, and the
round's new artifacts are knowledge and receipts rather than instruments. [L1 fills] if the closure counts the
committed selftest receipts as a capability.

Limits named before data: the Score column is not checked (verdicts, not scores); the Last-change convention is
read, not judged; the hidden scan is SHONEN.md only; a matching tally proves the instrument prints the number, not
that its arms are good; the fleet MANIFEST is trusted, not re-judged; a located quote proves the words occur in the
committed copy, not that the claim follows from them; the three-new-words floor is a floor; the entry says what
v7.2 prints, not what this host printed (no kernel MESSAGE grep, S351/QUALITY 15). Wave a2w1's row-by-row re-open of
the 22 C2 quotes, and any row it could not corroborate, are recorded in the round report and stand as limits.

Planned (round 51): [L1 fills].
```

---

## Draft C — correction sweep for `corpus/lessons/round-49.md` (routed D-c)

The lesson file is not mine to edit. If the L1 corrects in place, the two sentences become:

```md
:7  `.ufo/waves/round-49/w1/` (47 report files on disk at this landing; 49 after the two late reports
    `Mo49SimpCounters.md` and `Mo49ExecCounterTiming.md` landed, both committed in round 50). **No wave 2 ran** (see
    Wave 1 below).

:212 - Seat accounting for wave 1: 49 seats dispatched; 47 report files on disk at this landing, 49 after the two
     late reports named at `:7` arrived; no `w1-results.json` was delivered (no WAVE-DONE message reached the L1),
     so death beyond a missing report stays unknown. I held the planner seat.
```

If the lesson stays as filed, the equivalent append-only note belongs in `corpus/lessons/round-50.md` and must carry
the same four figures (`43d84666` → 47; `7197160b` → 48; `9b8562a3` → 49; 0 wrong in `LOG.md`; 2 wrong in
`corpus/lessons/round-49.md`). Either way the LOG entry's correction subsection above is the lane-facing record.

---

## 2. Notes for the L1 (why certain slots say `[L1 fills]`)

- Defect 1 (author date) is a fleet-commit property; I cannot read the fleet report commit graph without opening
  the fleet repo, which my seat does not do.
- Defect 5 (round shape) needs the a2w1 settlement (`w1-results.json` / `a2w1-results.json`), which does not exist
  while the wave is still settling; I measured 24 `.md` files at my read and the dispatch count 64 from
  `a2w1-dispatch.json` (`counts.spawn`), and 40 from `w1-dispatch.json` (`counts.spawn`).
- Defect 6 (`variants=26` vs 27) and defect 8 (D-g wording) are lesson-text dispositions only the L1 can make.
- Defect 7's random-handle item is a counter change, which this round is forbidden to make; the LOG text keeps it
  routed rather than claiming a closure.
- The `manifest=a94551c5bc8d` field in both C1 receipts is a content digest the counter prints; it is not the fleet
  revision `e0144996…` in the contract. The draft says so once so a later reader does not read one as the other.
- `evidence/control-c2-do-nothing.txt` (pins=ok) and `evidence/control-c2-donothing-git.txt` (pins=bad) both exist.
  The contract's "Before" line is the `-git` one; the draft quotes the `-git` file. Quoting the other one would
  understate the before state.

## Findings

1. **MED — `corpus/lessons/round-49.md:7` and `:212` carry the wrong report count ("48 of 49").** Measured counts
   under `.ufo/waves/round-49/w1/` are 47 at `43d84666` (the lesson's own commit), 48 at `7197160b`, 49 from
   `9b8562a3`. The round-49 report is right (47 at filing); the lesson is wrong in two places and unchanged through
   HEAD. Draft A carries the correction entry and Draft C the two replacement sentences.
2. **MED — `corpus/lessons/round-49-verifier-spotcheck.md:26` (D-c) and `.ufo/reports/round-49/mori.md:58` name
   `LOG.md` as carrying the wrong number; it does not.** `LOG.md:2724-2730` has no wave-1 report count and
   `git log 43d84666..HEAD -- LOG.md` is empty. A round-50 correction that repeats "LOG.md is wrong" would add a
   second wrong statement; the draft states 0 wrong in `LOG.md`.
3. **LOW — `.scratch/` debris unchanged (routed defect 4).** `ls -d .scratch/*/ | wc -l` → 183 at my read, the same
   figure the round-49 closure recorded; `find . -maxdepth 4 -name 'mori-conform-selftest-*'` → 0 and
   `git ls-files | grep -c mori-conform-selftest` → 0, so the seven `round-40/scratch/mori-conform-selftest-*`
   dirs are gone, but `.ufo/waves/round-40/scratch/` still holds `mutconform-arms2/`, `selftest-v3-draft.txt` and
   `selftest-v3-draft2.txt`.
4. **LOW — `SCORECARD.md:21-25` already holds the round-50 Axes correction at the data rev.** The `## Round 50`
   section must reference it (Draft B does) rather than restate it, or the file will carry two accounts of one
   change.
5. **LOW — two C2 do-nothing receipts with different `pins`.** `evidence/control-c2-do-nothing.txt` prints
   `pins=ok`; its own header says it is `evaluate() over entering 7197160b + frozen copies`, an in-process call that
   supplies the copies. `evidence/control-c2-donothing-git.txt` has no header, is the counter run against the real
   entering rev (0 copies under `corpus/evidence/sources-r50/` at `7197160b`), and prints `pins=bad`. Only the second
   matches the contract's stated before line, so a LOG/SCORECARD quote must name the `-git` file (Drafts A and B do).
6. **LOW — `.ufo/waves/round-50/__pycache__/` exists in the round directory** (untracked, matched by
   `.gitignore:3:__pycache__/`), a Python artifact from running the counters in place; it is not part of the frozen
   evidence set.
7. **LOW — round-50 wave accounting is not yet a record.** Attempt 1 dispatched 40 seats with 5 reports on disk;
   attempt 2 dispatched 64 seats with 24 `.md` files present at this seat's read. Neither settlement file exists,
   so the LOG entry leaves the figure to the L1 rather than freezing a number that will move.
