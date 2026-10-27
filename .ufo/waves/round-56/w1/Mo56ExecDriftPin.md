# Mo56ExecDriftPin — no-harm to the freshness instruments (drift pin, census, silence oracle)

Seat: Mo56ExecDriftPin (mori-shokunin, leaf executor). Lane repo:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root:
`/home/vgpnk/Projects/shokunin`. Range measured:
`5b295eeebd87ebd610d8d39bfe2035742f740cfa` (entering) →
`8be2717b0809281d07dffe83dad424a4859e0747` (freeze). Scratch
`/fast/scratch/hyaku/mori-r56/Mo56ExecDriftPin/` (removed at exit; every
cited byte is copied into this report). No fleet file, git index, jj state or
PATH directory was written; no tools installed or upgraded (nothing needed).
Machine id: MACHINE_ID. No votes carried by this report.

## Assignment as executed

1. Locate the pinned drift baseline `corpus/evidence/baseline-r10-*.json` and
   run `mori-census.sh --drift <baseline>` read-only; report exit code and
   verdict line.
2. Confirm the round-56 range did not touch the census, the baseline, or the
   silence oracle (`git diff --name-only <entering>..<freeze>`).
3. Any regression is a HIGH finding.

Because the lane re-pinned at round 20 (`corpus/knowledge/drift-repin-r20.md:3-13`,
`:59-62`), **both** baseline files were evaluated: the seat-spec target
`baseline-r10-20261015T2231Z.json` (historical, red by design since round 12)
and the operative pin `baseline-r20-20261021T1051Z.json`.

## Instruments located, with bytes at both tips

`sha256sum` of the committed blob at each tip (`git show <rev>:<path> | sha256sum`):

```
tools/mori-census.sh
  entering=87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28
  freeze  =87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  [SAME]
  worktree=87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28
tools/mori-silence-cases.sh
  entering=ff8b69757dea40e0a1aae4969acf633ee306269da100c594f6104e77809a4dcd
  freeze  =ff8b69757dea40e0a1aae4969acf633ee306269da100c594f6104e77809a4dcd  [SAME]
corpus/evidence/baseline-r10-20261015T2231Z.json
  entering=0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478
  freeze  =0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478  [SAME]
corpus/evidence/baseline-r20-20261021T1051Z.json
  entering=e528bc1549fd3f44abe01450db8146d596245fd85c94f98e6d450e84d3be8433
  freeze  =e528bc1549fd3f44abe01450db8146d596245fd85c94f98e6d450e84d3be8433  [SAME]
corpus/evidence/drift-classification-r20.json
  entering=e244d5b14f6d0d507e40c2209e2a6088a4fba1051a8e80135a9eaab23b082854
  freeze  =e244d5b14f6d0d507e40c2209e2a6088a4fba1051a8e80135a9eaab23b082854  [SAME]
```

The census's own header records `census_sha256=87b8d680…ab28` in the r20
baseline and in `drift-classification-r20.json:5-7`, so the pinned comparison
is anchored to the bytes that are still on disk.

## 1. The pin still evaluates (exit code + verdict line)

Command (read-only; `--drift` writes nothing per
`tools/mori-census.sh:213` and `corpus/knowledge/drift-pin-r10.md:50`):

```
bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh --drift \
  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/baseline-r10-20261015T2231Z.json
```

**exit 1**, verdict line (64 tokens, 1169 bytes). Token-per-line form, byte-faithful
to the run:

```
MORI_DRIFT:
+FINDING:CGROUP_OOM_KILL_CUMULATIVE
+FINDING:COREDUMP_NOTICE_JOURNAL_USER
+FINDING:JOURNAL_CLASSES_UNMEASURED
+FINDING:LANE_SILENT
+FINDING:OOM_KILL_JOURNAL
+FINDING:ROSTER_SET_MISMATCH
+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER
+FINDING:UNIT_FAILURE_OUT_OF_SCOPE
+FINDING:WATCHDOG_STATE_LAG
+SURFACE:journal.system
+SURFACE:journal.user
+SURFACE:lane.audio
+SURFACE:lane.chousa
+SURFACE:lane.game-dev-2d
+SURFACE:lane.game-dev-3d
+SURFACE:lane.kaidoku
+SURFACE:lane.kotodama
+SURFACE:lane.lore
+SURFACE:lane.mado
+SURFACE:lane.mori
+SURFACE:lane.revenger
+SURFACE:lane.souji
+SURFACE:lane.tabi
+SURFACE:lane.tameshi
+SURFACE:lane.tsukuroi
+alarm_basis
+attribution
+conf_dropped_n
+conf_n
+gate_s
+note
+paths
+positive_basis
+positive_validation
+process_sigkill
+raw_basis
+reason
+repo
+roster_n
+roster_source
+state_dropped_n
+state_n
+trust
+user_positive_process_sigkill
+user_positive_unit_signal
+user_unit_signal
-FINDING:SEGFAULT_JOURNAL
-FINDING:WATCHDOG_STALE
-FINDING:WAVE_UNSETTLED_AGE
-SURFACE:journal
-attribution
-example
-rowb_files
-subject_commits
-window
HEADER
age_s
basis
boot
io_avg_unavailable
launch_epoch
obs
round
volatile_fields
```

Command against the operative pin:

```
bash /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh --drift \
  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/baseline-r20-20261021T1051Z.json
```

**exit 1**, verdict line verbatim (410 bytes, 28 tokens):

```
MORI_DRIFT: +FINDING:CGROUP_OOM_KILL_CUMULATIVE +FINDING:KILL_SIGNAL_JOURNAL +FINDING:LANE_SILENT +FINDING:OOM_KILL_JOURNAL +FINDING:WATCHDOG_STATE_LAG +attribution +example +gate_s +has_head +no_fresh_files +no_other_commits +no_subject_commits +reason +repo +rowb_files -FINDING:WATCHDOG_STALE -gate_s -path -reason -subject_commits -window SURFACE:disk SURFACE:silence age_s basis launch_epoch reason round
```

Both invocations **evaluate**: the verdict vocabulary is `MORI_DRIFT: <tokens>`,
not the exit-2 setup path (`baseline missing` / malformed). A pin that could no
longer evaluate would exit 2 with a diagnostic, which did not happen.

## 2. The round-56 range does not touch any freshness instrument

```
git diff --name-only 5b295eee..8be2717b   -> 34 files
grep -E 'mori-census\.sh|mori-silence-cases\.sh|baseline-r(10|20)-' over that list
  -> NONE of census/oracle/baseline appears in the range
git diff --stat 5b295eee..8be2717b -- tools/
  -> 2 files changed, 926 insertions(+), 0 deletions(-)
     tools/mori-driver-liveness.py | 479 +
     tools/mori-vote-bind.py       | 447 +
```

`git diff --name-status <range> -- tools/ corpus/evidence/` adds only
`corpus/evidence/sources-r56/rfc8259.txt` and
`corpus/evidence/sources-r56/watchdog-log-grammar.txt`. The full 34-file range
list is the contract/counters/controls/fixtures/receipts under
`.ufo/waves/round-56/`, the two new tools, two new source copies, two new
knowledge entries, and the `corpus/SOURCES.md` append (S544/S545). Everything
else in `tools/` is untouched: `git diff --stat -- tools/` reports 0 deletions.

## 3. Behavioural no-harm (instruments still behave identically)

All runs from scratch with `TMPDIR` inside the seat scratch; `MORI_SHOKUNIN_ROOT`
pinned to the fleet root so the census reads the real fleet, not the scratch tree.

| # | command | exit | captured line |
|---|---|---|---|
| 1 | `bash tools/mori-census.sh --selftest` (freeze tip) | 0 | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, stderr 0 B |
| 2 | `bash tools/mori-silence-cases.sh` (freeze tip) | 0 | `MORI_SILENCE_CASES: matched=28 total=28`, stderr 0 B |
| 3 | `bash <entering>/tools/mori-census.sh --selftest` | 0 | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` |
| 4 | `bash <entering>/tools/mori-silence-cases.sh` | 0 | `MORI_SILENCE_CASES: matched=28 total=28` |
| 5 | `mori-census.sh --drift baseline-r20` at the entering-tip tree | 1 | byte-identical to the freeze-tip run |
| 6 | `mori-census.sh --drift baseline-r10` at the entering-tip tree | 1 | byte-identical to the freeze-tip run |

A/B (rows 5–6, `cmp` on the two captured files):

```
A/B r10 identical: YES
A/B r20 identical: YES
```

The entering-tip census is a `git archive` extraction of `5b295eee`; its
`tools/mori-census.sh` is the same 87b8d680…ab28 blob. Round-56 therefore
moves the drift verdict by **zero tokens** against both baselines.

Instrument stability under its own control (pin round-trip, scratch target only):

```
bash tools/mori-census.sh --pin <scratch>/now-pin.json
  -> MORI_PIN: ok path=<scratch>/now-pin.json    exit 0   (18293 bytes)
bash tools/mori-census.sh --drift <scratch>/now-pin.json
  -> MORI_DRIFT: none                            exit 0
```

A clean pin→drift round-trip means the red against the committed baselines is
live-state accumulation since the pin clock, not an instrument defect.

Lane-grading A/B (does the round-56 *commit set* change the census's own view
of the mori lane?). Two synthetic fleet roots were built in scratch, each with
`mori-shokunin/` extracted at one tip and committed under a throwaway identity
inside the fixture only (`git rev-parse --show-toplevel` asserted equal to the
fixture dir before the first commit), `MORI_NOW_EPOCH=1793200000`,
`MORI_LANE_SILENCE_S=900`:

```
root-entering lane row: SURFACE lane.mori: young (lane=mori round=56 launch_epoch=1793199400
                        age_s=600 basis=row-8 reason=age_le_gate gate_s=900)
root-freeze   lane row: SURFACE lane.mori: young (lane=mori round=56 launch_epoch=1793199400
                        age_s=600 basis=row-8 reason=age_le_gate gate_s=900)
```

Only the root path, the two masked ages, and the live cgroup gauges differ
between those runs. With the real fleet root and the gate lowered to 900 s so
authorship is actually graded, the lane still grades healthy:

```
SURFACE lane.mori: progressing (lane=mori round=56 launch_epoch=1793106516 age_s=4518
                    basis=row-A subject_commits=yes window=launch..NOW)
window commits by author: 4  mori-shokunin <mori@shokunin.local>
```

The single `LANE_SILENT` finding in that run is `lane=chousa round=58`
(`age_s=10064 gate_s=900 basis=row-D`), not the mori lane.

## 4. The round-56 census of record (sources census) still exits 0

The contract's "start census receipt" is the fleet sources census
(`scripts/sources-census.sh`), not the mori census
(`.ufo/waves/round-56/contract.md:68-71`). Its committed receipt reproduces
byte-for-byte:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
     --root /home/vgpnk/Projects/shokunin mori        # output + "exit=0"
cmp reproduced vs evidence/census-start.txt -> IDENTICAL
receipt bytes=2580  repro bytes=2580
```

End-state measurement at the freeze registry (read-only, stdout only):

```
sources-census.sh validate --file <lane>/corpus/SOURCES.md   -> exit 0
  lines=24, W-codes=23 W04, E-codes=0, stderr 0 B
sources-census.sh census   --root <fleet> mori               -> exit 0
  mori rows 318 ; FLEET rows 318 ; tier.A 287 tier.B 14 tier.C 17
  status.mined 267 status.queued 24 status.rejected 27 ; FLEET missing 0
```

So "end census must exit 0" is satisfiable at the freeze tip, with 23 W04 and
no E-code. Registry rows move 316 → 318 (S544, S545 added by `c419fe6d`),
verified independently: at the entering tip
`git show 5b295eee:corpus/SOURCES.md | grep -cE '^\|? *S[0-9]{3} *\|'` → 316,
at the freeze tip → 318.

## Limits of this seat

- Live-state drift is not falsifiable from a single observation: the r10/r20
  red is attributed to host and fleet state, not to any census byte. The A/B
  over the same census bytes, plus the pin round-trip, is the whole argument.
- Baseline-r20's canonical block holds 63 lines, today's scratch pin 68: 23
  baseline lines are absent from the new run and 28 lines are new. Of those,
  20 are lane rows, one is the disk row and one the silence row (changed in
  place); one finding line (`WATCHDOG_STALE`) disappears and six appear
  (`WATCHDOG_STATE_LAG` ×2, `OOM_KILL_JOURNAL`, `KILL_SIGNAL_JOURNAL`,
  `CGROUP_OOM_KILL_CUMULATIVE`, `LANE_SILENT`). Every difference is a
  lane/host state change visible in the census rows, not a rule change,
  because the script bytes are identical.
- `drift-classification-r20.json` maps tokens against `baseline-r10`
  (`:6`), so it is a register for the r10 red, not for the r20 red.
- The counters, predicates, controls and kill rules are frozen; nothing here
  proposes changing them.

## Findings

1. **HIGH — none.** No round-56 regression of the drift pin, the census, or the
   silence oracle was found. Census/oracle/baseline/register blobs are
   byte-identical at `5b295eee` and `8be2717b`; the drift verdict is
   byte-identical from the entering-tip tree and the freeze-tip tree against
   both baselines; selftest 134/134 and oracle 28/28 pass at both tips. The red
   drift is pre-existing live state, not introduced by this range.

2. **MED — the operative r20 pin is red (28 tokens) and has no register keyed
   to it.** `corpus/evidence/drift-classification-r20.json:6` names
   `baseline-r10-…json` as the baseline it classifies (50 token entries,
   `class_counts` 26/19/5), so today's r20 red is unclassified except where a
   token name happens to overlap: 9 of 28 named, 19 unnamed. The r10 red is
   likewise under-covered today: 46 of 64 tokens named, 18 unnamed.
   Files: `corpus/evidence/baseline-r20-20261021T1051Z.json`,
   `corpus/evidence/drift-classification-r20.json:1-8`,
   `tools/mori-census.sh` (`run_drift`).

3. **MED — the round-56 start census receipt does not carry the "316 rows"
   figure the contract attributes to it.** `validate` mode prints `W04` rows
   and an `ok` line but no row count (`grep -c rows` on the receipt → 0); the
   receipt is exactly reproducible (2580 B, identical), and the row count is
   only obtainable from `census` mode (316 at the entering tip, 318 at the
   freeze tip). This is the round-55 routed defect 1 class (QUALITY 152)
   recurring in the receipt, not in the registry.
   Files: `.ufo/waves/round-56/evidence/census-start.txt:1-25`,
   `.ufo/waves/round-56/contract.md:70-71`,
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (validate mode).

4. **MED (live coverage, not a round-56 regression) — 4 of 23 lanes grade
   `unavailable`, including both main-repo lanes.** At the freeze tip the live
   census emits
   `SURFACE lane.protocol: unavailable … reason=ref-unresolved repo=/home/vgpnk/Projects/shokunin`
   and the same for `aggregator`, `audio`, `game-dev-2d`. The fleet root and
   those lane repos are jj-colocated (`/home/vgpnk/Projects/shokunin/.jj` mtime
   `2026-10-25 21:12:01 -0300`) with no `lane.branch` mirror
   (`git config --get lane.branch` → unset, rc 1), which the r17 A2 rule grades
   `ref-unresolved` by design. At the r20 pin the same rows were
   `progressing (basis=row-A)`, so this is a real loss of main-repo lane
   coverage accumulated after 2026-10-21, not by this range.
   Files: `tools/mori-census.sh` (roster/ref resolution, A2 clause),
   `/home/vgpnk/Projects/shokunin/.jj`.

5. **LOW — the drift-pin ritual is unexercised: no drift-named receipt exists
   after round 15.** `corpus/knowledge/drift-pin-r10.md:241-245` requires a
   `--drift` measurement as the first measurement of each round. Measured over
   every `round-*/evidence` directory: rounds 13, 14 and 15 carry 1–2
   drift-named files each; rounds 16–56 carry none (round-56: 11 files, none
   drift-named). The r20 red therefore accumulated unobserved for six days.
   Files: `corpus/knowledge/drift-pin-r10.md:241-245`,
   `.ufo/waves/round-56/evidence/`.

6. **LOW — receipt scope labels differ by invocation, which breaks naive byte
   comparison.** `validate --root <fleet> mori` labels the scope `mori` (the
   committed receipt), `validate <lane-dir>` labels it `mori-shokunin`, and
   `validate --file <lane>/corpus/SOURCES.md` labels it `file`. The S-id/W04
   payload is the same in all three; only the first column differs.
   Files: `.ufo/waves/round-56/evidence/census-start.txt:1-23`,
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:480` (`lane=${rel%-shokunin}`).

### Routed to round 57 (named limits, not fixes proposed here)

- Extend or replace the drift register so it covers the operative
  `baseline-r20` token set, and re-pin with the round-56 census bytes if the
  next round wants a green pin. Counters and predicates are frozen; this is a
  round-57 routing, not a round-56 change.
- Capture a `--drift` receipt each round (the ritual at
  `drift-pin-r10.md:241-245`) so a red cannot accumulate unnoticed.
- Set `lane.branch` for the jj-colocated fleet root and the `audio` /
  `game-dev-2d` lane repos, or record the four lanes as knowingly ungradeable,
  so the census does not silently drop the two main-repo lanes.
