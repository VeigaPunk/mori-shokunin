# Round 50 verifier spot-check — mori

author: hyaku closure (non-author integrator, @m_opus)

Scope: mori lane-round 50. Lane HEAD before `7197160b927f04db294c9553fb48fadcc7a3f4e3`, after
`756d5b1a5679b131203663cbbbd2c4d96f7143ee`. Closure date 2026-10-26. I did not author the round. I edited no
lane-authored file and ran no lane gate.

Driver digest (`.ufo/watchdog.log`, mutable; copied here):
`2026-10-26T05:31:49-03:00 launch mori round=50 pgid=998797 driver=hyaku-inline attempt=1` /
`2026-10-26T09:23:50-03:00 lane-dead-no-report mori round=50; retry same round (attempt 1 L1 died in the orchestrator host crash 2026-10-26 ~08:50 -03; no report landed; work salvaged to the lane branch)` /
`2026-10-26T09:23:52-03:00 launch mori round=50 pgid=1820734 driver=hyaku-inline attempt=2` /
`2026-10-26T11:04:16-03:00 complete mori round=50; hyaku-inline attempt=2`.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H %aI' -- .ufo/reports/round-50/mori.md` | `mori-shokunin e9833c0f73b6fa7555b104e242484d3afdf03c70 2026-10-26T10:54:42-03:00`; `mori-shokunin 4a20abb16ee185d751ad9c8d4bec6b445810ab72 2026-10-26T10:15:47-03:00`. Both are on `origin/main` |
| `SHONEN` heading, one line per box | read the report | present. Four boxes, all `[~]`, each with a pointer. The pointers resolve: `SKILL.md:1018` is `## Round50 …`, `LOG.md:2732` is `## Round 50 …`, `corpus/QUALITY.md:1176` is the round-50 criteria heading, and `a2w1/Mo50bConnSiblings.md` exists |
| cited commits exist and are ancestors of the branch | `git merge-base --is-ancestor <h> master` for `7197160b…`, `950e99be`, `9b8562a3`, `487941b9…`, `4548a34d…`, `bae8656e…`, `756d5b1a…` | all seven resolve and hold (rc 0) |
| pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state …/mori-shokunin` | `branch=master local=remote=756d5b1a5679… ahead=0 behind=0 head=detached tracked=0 untracked=0` |
| remote tip | `git ls-remote origin refs/heads/master` | `756d5b1a5679b131203663cbbbd2c4d96f7143ee` |
| leftovers | `git status --porcelain` | empty. `--ignored` shows 9 lines: `.jj/` and `__pycache__` dirs only |
| prompt carries template contract | `.ufo/prompts/mori-round-50.md` headings | §1 MISSION/AXES, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract, §5 push scope, §6 hyaku addendum, §7 scratch discipline (599 lines) |
| real report, not a marker | named commits, evidence files, counters | real. Status `ok` |
| commits in range | `git log 7197160b..756d5b1a` | 7 commits: 950e99be freeze, 649e14cf operator `considerthese`, 9b8562a3 orchestrator salvage, 487941b9 data, 4548a34d wave spec, bae8656e integration, 756d5b1a receipts. All except the operator commit are `mori-shokunin` |

Conformance defects (status-neutral, recorded in notes only):
- **D-a. The first filing commit has an author date earlier than the lane tip.** `4a20abb1` was authored
  `10:15:47`, while the tip `756d5b1a` was authored `10:52:00` and committed `10:54:21`. The second filing
  `e9833c0f` was authored `10:54:42`, after the tip, so the report as it stands satisfies round-49 routed defect 1.
  The report gives the mechanism: `scripts/hyaku/fleet-commit.sh:84-85` runs `jj metaedit --update-author` and
  keeps the creation time of the working-copy change. That script belongs to the fleet, so I route the defect to
  the operator, not to the lane.
- **D-b. The round ran over the seat ceiling and did not run the contract's wave shape.** Attempt 1 dispatched 40
  seats in `w1`. Five reports landed and 35 outcomes are unknown. Attempt 2 dispatched 64 seats in `a2w1`, and all
  64 reported (`ls a2w1/*.md | wc -l` → 64; `a2w1-results.json` `.seats` length 64). That is 104 seats in total,
  above the 100 ceiling. The frozen contract planned "two v1 waves", but the round ran one wave after the data had
  landed. The report discloses both points.
- **D-c. The round did not take the considerthese suggestion its frozen contract named.** The contract named the
  2026-10-25 suggestion 2. The round took suggestion 3 from 2026-10-26 instead. The lesson records why: the newer
  reflection superseded the older one, and the baseline of suggestion 2 is not reproducible
  (`Mo50bSentHostPaths.md`).
- **D-d. One prior closure could not be re-executed hermetically.** In the round-47 re-execution, a run first
  diverged because `.ufo/waves/round-40/conform.py` exited 2 under load. A rerun reproduced the receipt. The script
  hardcodes the lane path and writes its selftest scratch inside the lane. The lane routed the fix to round 51.
- Round-49 routed defects 2 (selftest receipts) and 4 (`.scratch` residue) are closed, and I checked both.
  Defect 2: `evidence/selftests/mori-pin-check.txt` holds `PIN_CHECK_SELFTEST pass=114 fail=0`, and
  `mori-unlanded-check.txt` holds `UNLANDED_SELFTEST pass=17 fail=0`. Both ran on a `git archive` of `950e99be`.
  `git diff --stat 950e99be 756d5b1a -- tools` is empty, so the receipts hold for the tip. Defect 4: `git status
  --porcelain --ignored` now lists no `.scratch` entry (the receipt records 166 before), and 225 tracked files
  remain.

## 2. Claims

| claim | axis | method |
|---|---|---|
| C1: the self-assessment agrees with the fleet record and the instruments | calibration | **Axes half re-measured** with my own `jq` over `MANIFEST.json`. **Pins half evidence-verified**: committed selftest receipts plus the pin-check run at the landed rev. I did not run the frozen `count-c1.py` |
| C2: the memcg OOM report block, FR1 | depth | **Re-measured** with my own quote locator, independent of `count-c2.py`, plus a live re-fetch of all three sources |

Freeze integrity: `sha256sum -c .ufo/waves/round-50/evidence/freeze-sha256.txt` → 34 `OK`, 0 failed. `git diff
--stat 950e99be 756d5b1a -- count-c1.py count-c2.py contract.md controls` → empty. Counter selftests committed:
`C1_SELFTEST pass=34 fail=0`, `C2_SELFTEST pass=31 fail=0`.

### C1 (calibration, held 5)

Committed counter evidence: before `control-c1-do-nothing.txt` → `C1=unmet items=8 axes=6 pins=2 boxes=4
mismatches=6 … manifest=a94551c5bc8d rev=7197160b… failed=mismatch`, `exit=1`. After `a2-c1-at-landed.txt` →
`C1=met … mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=bae8656e…`, `exit=0`. All seven non-witness
controls stay unmet.

My re-measurement of the axes half: `jq '[.rounds[] | select(.lane=="mori" and .type=="closure" and
.admitted==true and (.verdicts[$a]|test("^(improved|harmed)$"))) | .lane_round] | max'` for each axis gives
coverage 47, operability 47, depth 49, freshness 28, calibration 49, adjacency 19. At the tip, the `## Axes`
Last-change cells lead with 47, 47, 49, 28, 49, 19, so all six agree. At `7197160b` the cells read 26, 31, 31, 28,
25, 19, so four disagreed. The manifest the counter pins is `git show e0144996:MANIFEST.json | sha256sum` →
`a94551c5bc8d…`, which matches the receipt's prefix. The cited closure lines resolve:
`round-47-verifier-spotcheck.md:67` reads operability improved and `:68` coverage improved;
`round-49-verifier-spotcheck.md:75` reads calibration improved and `:76` depth improved.

Pins half: SHONEN read `(60/60)` and `(13/13)` at `7197160b`. It now reads `(114/114)` and `(17/17)`, which match
the committed receipts. `a2-pin-check-at-landed.txt` → `PIN_CHECK=met tally_pins=35 … mismatches=0`, `exit=0`, and
its rows for `PIN_CHECK_SELFTEST pass=114` and `UNLANDED_SELFTEST pass=17` show `state=match`. That makes 4 axis
mismatches plus 2 pin mismatches, which equals the reported `mismatches=6` before.

No score changes. `git diff 7197160b 756d5b1a -- SCORECARD.md` touches four Axes cells (Score column unchanged:
6/7/5/5/5/6), adds a correction paragraph, and appends a Round 50 section.

Limits the lane names and I carry: the counter reads verdict words as substrings, does not read the Score column,
and has a vacuous `admitted`-filter arm. "Last change" now means the latest admitted closure that graded the axis
improved or harmed, not the latest score move.

Ruling: **verified**. The axes half is re-measured and the pins half is evidence-verified.

### C2 (depth, held 5)

My measurement: I parsed the `## Claims` table of `corpus/knowledge/oom-memcg-stat-r50.md` at `756d5b1a`. For the
HTML copy I stripped script and style blocks, comments, tags and entities. I collapsed whitespace and tested each
quote as a substring of the committed copy its row names, with a no-whitespace fallback for code that wraps across
lines. Result: `rows=22 located=22 missing=0`, by source S489 7, S490 8, S491 7. Reported: `C2=met claims=22
located=22 quote_missing=0 bad_rows=0 sources=3 …` (`a2-c2-at-landed.txt`). The two agree.

Live re-fetch on 2026-10-26: `curl -fsSL <url> | sha256sum` gives cgroup-v2 `2d716cb7…0bf34`, memcontrol.c
`8a28e0bc…41fd5e` (the first try returned 429; the retry succeeded) and oom_kill.c `452f1348…01f756b4e`. All three
equal the committed copies.

Absence sweep before the entry: `git grep -F -c` of `memory.stat`, `Memory cgroup stats` and `failcnt` at
`7197160b` over `corpus/SOURCES.md corpus/knowledge SKILL.md` → 0 files for each. Before:
`control-c2-donothing-git.txt` → `C2=unmet … failed=entry_absent,pins`.

Nuance: two of the 22 claims, the `oom_memcg=` and `task_memcg=` labels, cover ground the lane already held
through S004 (`corpus/SOURCES.md:10`, "memcg OOM report path labels" at a master commit). The new ground is the
stats block, the formatter it shares with `memory.stat`, the failcnt source and the key semantics. A located quote
shows that the words are present, not that the claim follows from them. Wave a2w1 found six overclaims that the
counter had passed (M4), and the lane corrected them before landing. I read claim rows 1, 8, 9, 11 and 16 against
their source context and found no remaining overclaim.

Ruling: **verified** (re-measured).

### Per-axis grades

| axis | entering | verdict | basis |
|---|---|---|---|
| calibration | 5 | improved | C1 verified: 6 mismatches before, 0 after, re-derived from the MANIFEST and the receipts. No score change claimed |
| depth | 5 | improved | C2 re-measured 22/22. The live sources equal the copies |
| coverage | 6 | unchanged | not claimed. The Score cell is unchanged and only the Last-change wording moved |
| operability | 7 | unchanged | not claimed. `git diff 950e99be 756d5b1a -- tools` is empty, and pin-check at the landed rev is met with 35 tally pins |
| freshness | 5 | unchanged | not claimed |
| adjacency | 6 | unchanged | not claimed. The entry's Boundaries section leaves `memory.max`, `memory.oom.group` and `oom_score_adj` configuration to tsukuroi |

No axis is harmed. `git diff 7197160b 756d5b1a -- corpus/SOURCES.md corpus/knowledge` has 0 removed lines, so
both stay append-only. No exploratory claim, so no `unprovable-but-better` ruling is owed.

## 3. Discernment spot-check (LEARNING.md)

Source: the `## Gate` section of `corpus/lessons/round-50.md`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| **S490** mm/memcontrol.c v7.2 | admit, mined, tier A | `corpus/evidence/sources-r50/memcontrol.c.v7.2` (sha256 = live); `corpus/SOURCES.md:269`, S004 at `:10` | **agree** | The anchors name what the scope cell says: `memory_stats[]` at 1546, `memcg_stat_format` at 1693, `memory_stat_format` at 1751, `mem_cgroup_print_oom_meminfo` at 1791, the usage `pr_info` at 1805, `Memory cgroup stats for` at 1824, `memory_stat_show` at 4905 with the formatter call at 4914. The Gate quote (`if (cgroup_subsys_on_dfl(...)) memory_failcnt = …MEMCG_MAX…`) is at lines 1800-1803. The scope differs from S004 (different revision, plus the formatter and failcnt) |
| **S489** cgroup-v2 docs at 7.2 | admit, mined, tier A | live `https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html` (sha256 `2d716cb7…` = copy); copy lines 1396-1400 | **agree** | The 17-word quote "The entries are ordered to be human readable, and new entries can show up in the middle." is at copy lines 1398-1399 under `memory.stat`. It grounds the "match by key" claim. Adopting staged S533 renumbered by document is sound |
| **S491** mm/oom_kill.c v7.2 | admit, mined, tier A (W04) | copy `oom_kill.c.v7.2` (sha256 = live) | **agree** | The `pr_err("%s: Killed process %d …oom_score_adj:%d\n",` format is at line 945, with its arguments at 946-951, and occurs once. Reusing the URL of S003 and S476 at a new scope makes W04 a warning, not an error |
| staged `scope-composition-in-the-block-r47.md` (S539) | reject | `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/scope-composition-in-the-block-r47.md`; `SOURCES.append.md:75`; the note `…/lanes/mori/round10/.deepresearch/notes/r10-oom-composition.txt` (3151 bytes) | **agree** | The entry's only `source:` is a `file://` note outside the lane, and its recheck is a host `journalctl` command with no committed receipt. `grep -rl S539 corpus/knowledge` → nothing, and `grep -cE '^ {0,3}\| *S(533\|534\|539) *\|' corpus/SOURCES.md` → 0. Rejecting on provenance follows the lane's S351 rule. The flip (re-capture read-only and pin it) is concrete, and the lesson does not say the reading is false |
| staged own-work row S534 | reject | `SOURCES.append.md:70` | **agree** | Its locator is `file:///…/round9/.deepresearch/notes/r9-oom-block-usage-limit.txt`, outside the lane. The admitted entry carries no host claim, so nothing depends on the row |

New SOURCES rows re-opened: S489, S490 and S491, all above. Each ≤25-word Gate quote (17, 9 and 12 words) is in
the committed copy, and each copy equals the live bytes I fetched on 2026-10-26.

Census, my run: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → 22 `W04` and one
`ok`, rc 0. The new warning is S491. `evidence/census-start.txt` holds 21 `W04` and `census-end.txt` holds 22, and
both match. Row count: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}'` → 261 at `7197160b`
and 264 at the tip, which matches the report.

## 4. Trend verdicts

- **expansion: improved.** One admitted entry, `oom-memcg-stat-r50.md`, covers ground the sweep shows the lane did
  not hold (0 hits for `memory.stat`, `Memory cgroup stats` and `failcnt` at `7197160b`). It cites three tier-A
  `mined` rows, S489–S491, and advances FR1. Caveat: the path-label claims overlap S004.
- **quality: improved, narrowly.** Admitted entries were re-verified and none failed. Seats re-ran the frozen C2
  counters of rounds 48 and 49 at their scored revisions, and every run agreed: `Mo50bExecReexecR48.md` rows
  10-13 and `Mo50bExecReexecR49.md` rows 12-14 report `located=15/15` and `21/21`. The lane did not touch those
  entries in this round (`git log 7197160b..756d5b1a` on the three knowledge files is empty). The stale
  self-assessment cells and pins were found and marked with a named correction, not left standing. The round-47
  re-run had one transient divergence, which is disclosed and was reproduced on rerun. I evidence-verified these
  re-executions and did not run them myself.
- **discernment: improved.** All five sampled decisions agree: three admits and two rejects. The lane's own wave
  caught six counter-passing overclaims (M4), and those became lesson-backed corrections. QUALITY 134–136 each
  cite a lesson.

## 5. Routed defects (lane must fix next round unless marked otherwise)

1. **`.scratch` producers.** Fix `tools/mori-pin-check.py:884-887` and `.ufo/waves/round-40/conform.py:69`
   (hardcoded lane path, selftest scratch inside the lane) so that re-executions are hermetic (D-d). The lane
   already plans this.
2. **Round shape.** Keep within the 100-seat ceiling across attempts, run the frozen contract's wave shape or
   record an amendment before data lands, and give a final disposition for the 35 attempt-1 seats with no report
   (D-b).
3. **Successor C1 counter.** Close the named survivors: verdict-word substring, a second `## Axes`, the unread Score
   column, the vacuous `admitted` arm, and a symlinked pin path. Also take K4 beyond SHONEN (tally pins in
   QUALITY, README and LOG).
4. **C2 entailment.** The counter passed six overclaims (M4). Give claim-to-quote entailment a committed reviewer
   step or a counter arm before a depth claim relies on location alone.
5. **Contract deviations in the record.** When a frozen contract item is not run, as with the considerthese
   suggestion (D-c), name the deviation in `LOG.md` as well as in the lesson.
6. **Operator, fleet-owned.** `scripts/hyaku/fleet-commit.sh:84-85` (`jj metaedit --update-author`) gives a filing
   commit the creation time of the working-copy change, which can precede the lane tip (D-a). The lane cannot fix
   this.

## 6. Notes for the operator

All four SHONEN boxes are `[~]`, and every pointer resolves. The "instructions executable without oral context" box
now rests on committed selftest receipts (114/114, 17/17) and a pin-check run at the landed rev, so a non-author can
check it from committed bytes. The other three boxes point to resolvable sections. Whether they meet the promotion
bar is the operator's decision. I wrote no `[x]`.
