# Mo50bScribeMistakes — round 50 attempt 2, wave a2w1 (mori, 森)

Leaf scribe seat. Deliverable: a drop-in `## Mistakes` section for
`corpus/lessons/round-50.md` (fenced in §2), with columns `id | class | evidence | captured-by | fix`
(the column set round 49's lesson uses, `corpus/lessons/round-49.md:192-194`).

- Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
- Frozen claims (read first): `.ufo/waves/round-50/contract.md`; attempt-1 freeze `950e99be…`, entering tip
  `7197160b…`; data revision `487941b9395e89678af0053cc443cdb49cdee6e3` (attempt 2, L1 `MoriR50a2`).
- Writes: this report only. No edit to `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`,
  `tools/`, `considerthese/`, or any other file under `.ufo/waves/round-50/`. No commit, no judge, no
  subagent, no other runtime.
- Reads: `git log/show/archive/ls-files/grep`, `ls`, `grep`, the two frozen counters at named revisions,
  `tools/mori-wave-settlement.py scan`, one read of the driver log `.ufo/watchdog.log` (not a kernel log; no
  MESSAGE text read). No cgroup limit touched, no OOM triggered, no service/config command.
- Tooling: nothing installed or upgraded; pacman not run (host-wide pause). Python 3 and git only.
- Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bScribeMistakes/` (created with `mkdir -p`, `TMPDIR` inside,
  removed on exit by `trap 'rm -rf -- "$S"' EXIT`; each `git archive` extraction ran there). Disk guard read
  before the runs: `/fast/scratch/hyaku` 23 % used, 619.2 G free.
- Machine: `MACHINE_ID` (not recorded).

## 1. Measurements behind the rows (command → output)

All outputs below are verbatim from this seat's runs on 2026-10-26.

1. Frozen C1 do-nothing at the entering tip (`cat .ufo/waves/round-50/evidence/control-c1-do-nothing.txt`):

   ```
   item axis coverage expect=round_47_improved got=round=26,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
   item axis operability expect=round_47_improved got=round=31,evidence_missing:corpus/lessons/round-47-verifier-spotcheck.md state=mismatch
   item axis depth expect=round_49_improved got=round=31,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
   item axis freshness expect=round_28_improved got=ok state=ok
   item axis calibration expect=round_49_improved got=round=25,evidence_missing:corpus/lessons/round-49-verifier-spotcheck.md state=mismatch
   item axis adjacency expect=round_19_improved got=ok state=ok
   item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch
   item pin python3_tools/mori-unlanded-check.py_--selftest expect=(13/13) got=UNLANDED_SELFTEST_pass=17_fail=0 state=mismatch
   C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch
   exit=1
   ```

2. SHONEN pin drift across revisions — for each rev, `git -C <lane> archive <rev> | tar -x -C <scratch>/t-<rev>`,
   then `python3 tools/mori-pin-check.py --selftest | tail -1`, `python3 tools/mori-unlanded-check.py --selftest | tail -1`,
   `grep -o '([0-9]*/[0-9]*)' SHONEN.md`:

   ```
   === 91fbbc2a ===            (round-48 wave 2, 2026-10-25T20:25:44; where the pins were written)
   pin: PIN_CHECK_SELFTEST pass=60 fail=0
   unlanded: UNLANDED_SELFTEST pass=13 fail=0
   shonen: (60/60) (13/13)
   === 64c2d5fc ===            (round-49 data commit, 2026-10-25T22:49:54)
   pin: PIN_CHECK_SELFTEST pass=114 fail=0
   unlanded: UNLANDED_SELFTEST pass=17 fail=0
   shonen: (60/60) (13/13)
   === 43d84666 ===            (round-49 landing tip)
   pin: PIN_CHECK_SELFTEST pass=114 fail=0
   unlanded: UNLANDED_SELFTEST pass=17 fail=0
   shonen: (60/60) (13/13)
   === 7197160b ===            (round-49 closure = round-50 entering tip)
   pin: PIN_CHECK_SELFTEST pass=114 fail=0
   unlanded: UNLANDED_SELFTEST pass=17 fail=0
   shonen: (60/60) (13/13)
   ```

   At `91fbbc2a` the tool file hashes are `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`
   (`mori-pin-check.py`) and `e6695e04026b3da93e0c6406737602a31265970cd5bdfa1ac1d44835ad6a2b85`
   (`mori-unlanded-check.py`); rc 0 for both selftests.
   Current SHONEN (`487941b9`) line 7: `… (114/114); python3 tools/mori-unlanded-check.py --selftest (17/17);
   receipts .ufo/waves/round-50/evidence/selftests/mori-pin-check.txt, …mori-unlanded-check.txt`.

3. Axes Last change cells at the entering tip (`git show 7197160b:SCORECARD.md`, `## Axes` table, first token of
   column 4): coverage `round 26 (improved, score held)`; operability `round 31 (improved, score held)`; depth
   `round 31 (improved, score held)`; freshness `round 28`; calibration `round 25 (improved, score held)`;
   adjacency `round 19`.

4. Fleet MANIFEST at `e0144996…` (`git -C /home/vgpnk/Projects/shokunin show …:MANIFEST.json`, rows with
   `lane=mori`, `verdict=admitted`), latest `lane_round` grading each axis `improved`:
   coverage 47, operability 47, depth 49, freshness 28, calibration 49, adjacency 19.
   Improvements each stale cell skips:

   ```
   coverage     cell=26 | skipped: 47                                                          (1)
   operability  cell=31 | skipped: 36,37,38,39,41,43,44,47                                     (8)
   depth        cell=31 | skipped: 38,39,41,44,47,48,49                                        (7)
   calibration  cell=25 | skipped: 37,38,39,41,43,44,46,47,48,49                               (10)
   ```

   Rounds 36-39 are admitted mori closures in that MANIFEST (`36` operability improved; `37` calibration +
   operability; `38` operability, depth, calibration; `39` calibration, operability, depth).

5. Round-49 report count. `grep -c '48'` over the four files named by routed defect 3:
   `corpus/lessons/round-49.md` → 43; `LOG.md` → 48; `SCORECARD.md` → 52;
   `/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/mori.md` → 11.
   Of those, the report-count hits are exactly:

   | file:line | verbatim | status |
   |---|---|---|
   | `corpus/lessons/round-49.md:7` | `(48 of 49 reports on disk when this lesson was written)` | wrong: 47 report files |
   | `corpus/lessons/round-49.md:212` | `49 seats dispatched; 48 reports on disk at writing;` | wrong: 47 report files |
   | `.ufo/reports/round-49/mori.md:9` | `(47 of 49 on disk at filing; no report from Mo49ExecCounterTiming and Mo49SimpCounters …)` | correct |
   | `.ufo/reports/round-49/mori.md:58` | `Erratum to corpus/lessons/round-49.md and LOG.md: they say 48 wave-1 reports; 47 report files plus swarm-registry.json were on disk` | erratum itself; quotes the wrong number as the thing corrected |
   | `LOG.md` | — | **no report count exists** in the round-49 entry (`LOG.md:2724-2730`): `grep -n '48 reports\|48 of 49\|47 reports\|47 of 49' LOG.md` returns only `LOG.md:1356` (`wave2 retains48 reports`, an older round) |
   | `SCORECARD.md` | — | **no report count** in the round-49 section (`:2632-2650`, the last section); its two `48` hits are `:2641` (`round-48 counter`) and `:2648` (`round 48`) |

   Filesystem at the moment the lesson was committed (`64c2d5fc`, 2026-10-25T22:49:54): the two later reports
   carry mtimes after it — `Mo49SimpCounters.md` 23:02:40, `Mo49ExecCounterTiming.md` 23:39:03 — so the
   directory held 48 entries = 47 report files + `swarm-registry.json`.
   `git ls-files .ufo/waves/round-49/w1 | wc -l` → `50` (49 reports + registry).
   Landing commits of the two late reports: `Mo49SimpCounters.md` first added at `7197160b`
   (2026-10-25T23:04:10), `Mo49ExecCounterTiming.md` first added at the round-50 salvage `9b8562a3`
   (2026-10-26T09:05:31).
   `python3 tools/mori-wave-settlement.py scan --lane-root … --fleet-root …` today reports round-49 w1 as
   `members=49 present=49 missing=0`.

6. Round-50 attempt 1 wave state.
   - `.ufo/waves/round-50/w1.ready.dispatched` → `2026-10-26T05:58:49`; `w1-dispatch.json` `counts` →
     `{"spawn": 40, "resume": 0, "total": 40}` (registry: 40 members).
   - `ls .ufo/waves/round-50/w1/` → `Mo50ScoutCoverageFR1.md`, `Mo50ScribeEntryA.md`, `Mo50ScribeEntryB.md`,
     `Mo50ScribeRowMemcontrol.md`, `Mo50ScribeRowOomKill.md`, `swarm-registry.json` (mtimes 05:51:24 →
     06:08:03).
   - `python3 tools/mori-wave-settlement.py scan` → `{"dispatch_path":".ufo/waves/round-50/w1-dispatch.json",
     "members":40, "counts":{"missing":35,"present":5,"stub":0,"unsafe":0,…}}`.
   - Frozen counters at attempt 1's freeze (dispatch revision, nothing else landed):
     `python3 .ufo/waves/round-50/count-c1.py 950e99be6757a52b00e9eb70ae1a1a7bbe2ea379 --scratch <scratch>`
     → `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=950e99be… failed=mismatch`, rc 1;
     `python3 .ufo/waves/round-50/count-c2.py 950e99be… --repo <lane>` →
     `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=950e99be… failed=entry_absent`, rc 1.
   - Driver record (read-only read of `.ufo/watchdog.log`, lines 1507-1519):
     `2026-10-26T05:31:49-03:00 launch mori round=50 pgid=998797 driver=hyaku-inline attempt=1`;
     `2026-10-26T09:23:50-03:00 lane-dead-no-report mori round=50; retry same round (hyaku-inline attempt=1:
     attempt 1 L1 died in the orchestrator host crash 2026-10-26 ~08:50 -03 (omp process exit); no report
     landed; work salvaged to the lane branch)`; `2026-10-26T09:23:52-03:00 launch mori round=50 pgid=1820734
     driver=hyaku-inline attempt=2`. The same crash produced `lane-dead-no-report` rows for `souji round=32`,
     `tabi round=31`, `tameshi round=48` (lines 1510-1517).
   - Salvage commit `9b8562a3` (author 2026-10-26T09:05:31, committer 09:05:33) message: `round-50: hyaku run-8
     orchestrator salvage of unlanded attempt-1 wave state and knowledge draft, plus a late round-49 seat
     report (L1 died in the orchestrator host crash 2026-10-26 ~08:50 -03; not a landed round)`; its stat
     carries `corpus/knowledge/oom-memcg-stat-r50.md`, the five `w1/*.md` reports, the dispatch/spec files and
     `.ufo/waves/round-49/w1/Mo49ExecCounterTiming.md`.
   - Attempt 2 order: data commit `487941b9` (author 2026-10-26T09:05:32, committer 09:27:40; files:
     `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`, `assimilation/a2/*`) precedes its wave artifacts
     (`a2w1-dispatch.json` 09:31:31, `a2w1.ready` 09:31:39; `a2w1.ready.dispatched` does not exist yet).
     Counters at the data revision: `evidence/a2-c1-at-data.txt` → `C1=met … mismatches=0` exit 0;
     `evidence/a2-c2-at-data.txt` → `C2=met claims=22 located=22 … sources=3` exit 0.

7. Instrument surfaces (for the captured-by column):
   - `grep -c 'SHONEN' tools/mori-pin-check.py` → `0`; `grep -c 'SCORECARD' tools/mori-pin-check.py` → `0`;
     `tools/mori-pin-check.py:2` → `"""mori-pin-check — re-measure the self-test pins of SKILL.md's gate registry.`
   - `tools/mori-routed-r24.py` is the only tool that parses the Axes Last change column (`grep -c 'Axes'` → 9,
     `grep -ci 'last change'` → 5); its D5 counted item (`:44-51`) reads that column only to reject a
     score-carrying row that still says `round 1` (`axis_stale_round_1`), and D5's check is the Score column
     against `SCORECARD.md:1499-1506` at `28b79d3d` (`:150-160`, `:760-800`).
   - `ls .ufo/waves/round-50/ | grep -c 'attempts\|ledger'` → `0`; round-49 and round-50 hold no
     wave-settlement receipt (`ls -R .ufo/waves/round-49 | grep -i 'settle\|results'` → empty; same for round
     50). QUALITY 64 (`corpus/QUALITY.md:227-232`) therefore has no receipt for either wave.
   - L1-death precedent in the lane: `corpus/lessons/round-32-verifier-spotcheck.md:16` (`… attempt 1 landed
     nothing: lane tip = base`) and `corpus/lessons/round-34-verifier-spotcheck.md:14,16`.

## 2. Draft `## Mistakes` for `corpus/lessons/round-50.md` (drop-in; L1 integrates)

```markdown
## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | self-assessment drift (survivor) | `SHONEN.md`'s tally pins read `(60/60)` and `(13/13)` from round 48's wave-2 commit `91fbbc2a` (2026-10-25T20:25:44) through the round-49 closure `7197160b` and attempt 1's freeze `950e99be`; run from `git archive 91fbbc2a` both tools printed exactly those tallies (`PIN_CHECK_SELFTEST pass=60 fail=0`, `UNLANDED_SELFTEST pass=13 fail=0`, rc 0 each), so the pins were true when written and went stale at the round-49 data commit `64c2d5fc` (2026-10-25T22:49:54), where the same two tools print `pass=114` and `pass=17` while SHONEN still said 60/60 and 13/13 — the round-49 closure and attempt 1's freeze carried the stale pin (`evidence/control-c1-do-nothing.txt`: `item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch`, the `(13/13)`/`pass=17` line likewise, `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch`, exit 1). The `## Axes` Last change cells at `7197160b` read `round 26 (improved, score held)` (coverage), `round 31` (operability), `round 31` (depth) and `round 25` (calibration) against the fleet `MANIFEST.json` at `e014499613f63f8a467821219b0296121119ca53`, whose latest admitted mori closures grading those axes improved are 47, 47, 49 and 49; the improvements each cell skipped are coverage 47 (one), operability 36, 37, 38, 39, 41, 43, 44, 47 (eight), depth 38, 39, 41, 44, 47, 48, 49 (seven) and calibration 37, 38, 39, 41, 43, 44, 46, 47, 48, 49 (ten), so two of the four cells had been wrong since the round-36 and round-37 closures. | `corpus/QUALITY.md:1028-1040` criterion 123: "A registry pin is calibrated only when an instrument re-runs it from committed bytes and reads it from its own cell. … `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` from round 40 to round 47 while the committed tool printed `pass=22` from the round-41 freeze `d72ac167` on. Check: `python3 tools/mori-pin-check.py --rev <rev> --baseline-rev <entering>` exits 0 before a round that edits a registry row or a registered tool lands." That check runs `tools/mori-pin-check.py`, whose own docstring is "re-measure the self-test pins of SKILL.md's gate registry" (`tools/mori-pin-check.py:2`) — `grep -c 'SHONEN' tools/mori-pin-check.py` → `0` — so the criterion reads SKILL.md's registry and never SHONEN.md's tally pins; and the Axes Last change column's only reader, `tools/mori-routed-r24.py` D5, uses it solely to reject a score-carrying row that says `round 1` (`axis_stale_round_1`, `:44-51`, `:760-800`) and never compares it with the latest admitted closure. | The round froze `count-c1.py`, which re-runs every SHONEN tally pin at R (`git archive`, TMPDIR in scratch), requires the observed `PREFIX pass=P fail=F` line as a committed receipt under `.ufo/waves/round-50/evidence/selftests/`, and requires each Axes Last change cell's first `round N` to be the MANIFEST's latest admitted round grading the axis improved or harmed, with that round's closure named in the Evidence cell. **Shown able to fail**: do-nothing at the entering tip prints `C1=unmet … mismatches=6` exit 1 (`evidence/control-c1-do-nothing.txt`); all-latest `mismatches=6`, pins-updated-no-receipt `mismatches=6`, axes-only `mismatches=2`, shonen-only `mismatches=4`, pins-deleted `pins=0 … failed=mismatch,pins_floor`, box-dropped `boxes=3 … failed=boxes_floor,mismatch,pins_floor` — each exit 1 (`evidence/control-c1-*.txt`); the landed tip prints `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0` exit 0 (`evidence/a2-c1-at-data.txt`). Named limits (contract): the Score column is not checked, and the MANIFEST is fleet-written, so the counter inherits its verdicts. |
| M2 | number-drift | The round-49 lesson counted directory entries as reports: `corpus/lessons/round-49.md:7` "`(48 of 49 reports on disk when this lesson was written)`" and `:212` "49 seats dispatched; 48 reports on disk at writing". The lesson was committed as `64c2d5fc` (2026-10-25T22:49:54), when `.ufo/waves/round-49/w1/` held 47 report files plus `swarm-registry.json` (48 entries; the 48 is the entry count, not the report count); the fleet report filed 22:54-22:57 already said "47 of 49 on disk at filing" and carried a trailing erratum (`.ufo/reports/round-49/mori.md:9,58`). The two missing seats' reports landed later: `Mo49SimpCounters.md` first at `7197160b` (2026-10-25T23:04:10), `Mo49ExecCounterTiming.md` only at the round-50 salvage `9b8562a3` (2026-10-26T09:05:31) — `git ls-files .ufo/waves/round-49/w1 | wc -l` → 50 (49 reports + registry), and `tools/mori-wave-settlement.py scan` gives `members=49 present=49`. | none — no QUALITY criterion reads a seat count written in a lesson: QUALITY 64 covers only "the per-seat report presence … counted by `tools/mori-wave-settlement.py scan` and the receipt … committed before the round reports that wave's settlement" (`corpus/QUALITY.md:227-232`), and round 49 committed no such receipt (no settlement receipt under `.ufo/waves/round-49/`), so the prose number was never compared with the filesystem. | Corrected wording: `:7` → "(47 report files of 49 seats on disk when this lesson was written; the directory held 48 entries, the 48th being `swarm-registry.json`)"; `:212` → "49 seats dispatched; 47 report files on disk at writing (`Mo49SimpCounters.md` landed at `7197160b`, `Mo49ExecCounterTiming.md` only at the round-50 salvage, so the directory now holds 49 report files)". Sweep: `grep -rn '48'` over `corpus/lessons/round-49.md` (43 hits), `LOG.md` (48), `SCORECARD.md` (52) and `.ufo/reports/round-49/mori.md` (11) leaves only the two lesson lines to correct — `LOG.md`'s round-49 entry carries no report count at all (`grep -n '48 reports\|48 of 49\|47 reports\|47 of 49' LOG.md` → only `LOG.md:1356`, an older round), and `SCORECARD.md`'s round-49 section has none (its two hits, `:2641` `round-48 counter` and `:2648` `round 48`, are not counts). **Shown able to fail: not yet shown.** No instrument compares a lesson's prose count with a report directory; the number is checkable by `ls .ufo/waves/round-49/w1 | wc -l` (50 entries) or the settlement scan (present 49), but no control goes red on a wrong prose count — the natural carrier is QUALITY 64's settlement receipt, which round 49 did not commit. |
| M3 | landing (attempt died mid-round) | Attempt 1 (`MoriR50`) dispatched a 40-seat wave at `2026-10-26T05:58:49` (`.ufo/waves/round-50/w1.ready.dispatched`; `w1-dispatch.json` `counts={"spawn":40,…total":40}`) after landing only the freeze `950e99be` (2026-10-26T05:45:42), then died in the orchestrator host crash (~08:50 -03, driver record `.ufo/watchdog.log:1518`), leaving 5 reports: `w1/` holds `Mo50ScoutCoverageFR1.md`, `Mo50ScribeEntryA.md`, `Mo50ScribeEntryB.md`, `Mo50ScribeRowMemcontrol.md`, `Mo50ScribeRowOomKill.md` plus `swarm-registry.json`, and `python3 tools/mori-wave-settlement.py scan` prints `w1-dispatch.json members=40 … present=5, missing=35` (a missing report is not a dead seat — the tool reports filesystem shape only, `tools/mori-wave-settlement.py:18`). No data was landed: both frozen counters are unmet at the freeze/dispatch revision — `count-c1.py 950e99be` → `C1=unmet … mismatches=6` rc 1; `count-c2.py 950e99be` → `C2=unmet claims=0 located=0 … failed=entry_absent` rc 1 — so the attempt's only durable work was the freeze plus what the orchestrator salvaged into `9b8562a3` (the unlanded entry draft `corpus/knowledge/oom-memcg-stat-r50.md` and the wave state). Attempt 2 inverted the order: data commit `487941b9` (2026-10-26T09:05:32/09:27:40) precedes its wave artifacts (`a2w1-dispatch.json` 09:31:31, `a2w1.ready` 09:31:39). | none in the lane for this shape. The bare L1-death class is recorded twice as a driver digest — `corpus/lessons/round-32-verifier-spotcheck.md:16` ("attempt 1 landed nothing: lane tip = base") and `corpus/lessons/round-34-verifier-spotcheck.md:14,16` — but both cover a death with **no** wave dispatched, and neither says what a half-run wave leaves. No lesson row and no QUALITY criterion reads the landing-before-dispatch order for a wave: QUALITY 75 (`corpus/QUALITY.md:330-337`) compares attempt/ledger `at` with the commit that changed the dispatch file, and round 50 holds no `*-attempts.json` or `*-ledger.json` (`ls .ufo/waves/round-50 | grep -c 'attempts\|ledger'` → 0); QUALITY 64 would have recorded `present=5, missing=35` before settlement, and no receipt was committed. | Land the round's data before the dispatch marker is written, so a dead L1 leaves landed work: the observable is that both frozen counters print `met` at the dispatch revision. **Partly shown able to fail**: as a state observable, red at attempt 1's dispatch revision — `C1=unmet … mismatches=6` rc 1 and `C2=unmet … entry_absent` rc 1 at `950e99be` — and green at attempt 2's pre-dispatch data commit — `evidence/a2-c1-at-data.txt` `C1=met … mismatches=0` rc 0, `evidence/a2-c2-at-data.txt` `C2=met claims=22 located=22 … sources=3` rc 0. **Not yet shown as a rule**: nothing in `tools/` or `.ufo/waves/round-50/` reads the dispatch revision's counters, so no committed receipt fails a round because its data was unlanded at dispatch. |
```

## 3. Premise corrections (assignment or landed wording the bytes do not support)

1. **"SHONEN pinned (60/60) and (13/13) since round 48 while the tools printed 114 and 17."** Half true.
   The pins were *written* in round 48 (`91fbbc2a`) and were correct there: at that revision the tools print
   60 and 13 (measurement 2). The divergence starts at the round-49 data commit `64c2d5fc`. A row that says the
   pins were wrong "since round 48" would accuse round 48 of a defect it did not have; the drafted M1 says
   "true when written, stale from `64c2d5fc`".
2. **`SCORECARD.md:21-26`, round-50 correction paragraph: "the Last change cells … lagged four admitted
   closures".** The cells are four; the closures are not. Measured: the four cells skipped 26 admitted
   improvements spread over closures 36, 37, 38, 39, 41, 43, 44, 46, 47, 48, 49 (per axis 1 / 8 / 7 / 10).
   Proposed wording: "… the four cells named rounds 26, 31, 31 and 25 while the fleet `MANIFEST.json` at
   `e0144996…` records the latest admitted mori round grading each axis improved as 47, 47, 49 and 49; the
   skipped improvements were coverage 47 (one), operability 36, 37, 38, 39, 41, 43, 44, 47 (eight), depth 38,
   39, 41, 44, 47, 48, 49 (seven) and calibration 37, 38, 39, 41, 43, 44, 46, 47, 48, 49 (ten), so the
   operability and calibration cells had been wrong since rounds 36 and 37." The sentence's other claims (the
   four values 26/31/31/25, the MANIFEST readings 47/47/49/49, scores unchanged, the checking command) are
   correct as landed.
3. **Routed defect 3 (round-49 spot-check §5 item 3) and the fleet erratum: "The lesson and `LOG.md` still
   carry the wrong number."** `LOG.md` carries no report count for round 49. The correction entry the same
   defect asks for ("Named correction entry … in the round-50 lesson and `LOG.md`") is therefore a *new*
   LOG.md sentence, not a fix of an existing one; the drafted M2 records this and leaves the entry text to the
   L1's LOG scribe.

## 4. Untouched, and what this seat did not establish

- No file outside this report was written; no commit, no index or jj change; no cache or scratch file inside
  the lane (the counters ran with `--scratch` under the seat scratch dir or from a scratch cwd).
- The counters were run only as measurement, never edited, and no counter/predicate/control change is proposed.
- Not checked: whether the MANIFEST's own per-axis grades are right (fleet-written; the counter inherits
  them); whether a different Last-change convention would be better (contract's named limit); the Score column;
  the `.scratch` residue count and the two round-49 seats' terminal causes (other seats' scope); the round-50
  wave-shape floors.
- Not read: any kernel log MESSAGE text, any credential, any host cgroup limit.
- The `a2w1` wave is in flight: its settlement count (`present=26, missing=38` at scan time) is a live number,
  quoted only as the scan's output, not as a settled count.

## Findings

1. **MED — `SHONEN.md:7` pins were wrong for two closures and attempt 1's freeze; the assignment's "since
   round 48" overstates the window.** Pins `(60/60)`/`(13/13)` set at `91fbbc2a` matched the tools there
   (60/13) and went stale at `64c2d5fc` (tools 114/17). Fixed at `487941b9`. The lesson row must say "stale
   from `64c2d5fc`", not "since round 48".
2. **MED — `SCORECARD.md:21-26` says the four Last change cells "lagged four admitted closures"; measured, they
   skipped 26 admitted improvements (coverage 1, operability 8, depth 7, calibration 10), so operability and
   calibration had been wrong since the round-36 and round-37 closures.**
3. **MED — no instrument read either half of the drift before round 50.** `corpus/QUALITY.md:1028-1040`
   criterion 123's check runs `tools/mori-pin-check.py`, which reads `SKILL.md`'s registry only
   (`tools/mori-pin-check.py:2`; `grep -c 'SHONEN'` → 0); the Axes Last change column's only reader
   (`tools/mori-routed-r24.py` D5) rejects only a `round 1` cell. The round's C1 counter closes this for
   SHONEN.md and the Last change cells (shown red by seven controls, green at `487941b9`).
4. **MED — the "48 vs 47" report count is wrong in two lesson lines and, contrary to routed defect 3, in no
   `LOG.md` line.** `corpus/lessons/round-49.md:7,212` must read 47 report files (48 directory entries); `LOG.md`'s
   round-49 entry (`:2724-2730`) has no count, so the routed defect's LOG half needs a new correction entry
   rather than a repair; `SCORECARD.md`'s round-49 section (`:2632-2650`) has no count either. The fleet report's
   own line 9 is already correct.
5. **MED — round-50 attempt 1 is the lane's first L1 death with a dispatched wave, and nothing records that
   shape.** 40 seats dispatched 05:58:49, 5 reports (`present=5, missing=35` by the lane's own scan), 35 seats'
   status unknown, and the driver record says only "no report landed; work salvaged to the lane branch"
   (`.ufo/watchdog.log:1518`). The prior L1-death records (`corpus/lessons/round-32-verifier-spotcheck.md:16`,
   `round-34-verifier-spotcheck.md:14,16`) all read "landed nothing: lane tip = base". The lesson row M3 is the
   first in-lane capture; the fix's observable is shown red/green by counters at `950e99be` vs `487941b9`, but
   no gate enforces it.
6. **LOW — QUALITY 64 is unmet for both round-50 waves and for round 49.** No committed settlement-scan receipt
   exists under `.ufo/waves/round-49/` or `.ufo/waves/round-50/`, although the criterion
   (`corpus/QUALITY.md:227-232`) requires one before the round reports settlement. This round's scan output is
   available (`present=5/missing=35` for `w1`, `present=26/missing=38` for `a2w1` at scan time) but unlanded.
7. **LOW — provenance of the C2 entry is split across two commits.** `corpus/knowledge/oom-memcg-stat-r50.md`
   reached the lane in the orchestrator salvage `9b8562a3` (attempt 1's unlanded draft), while the data commit
   `487941b9` carries only `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md` and `assimilation/a2/*`. A landing
   table that credits the entry to `487941b9` alone would be imprecise.
8. **LOW — the 48 in `corpus/lessons/round-49.md:7` is [INFERENCE] the entry count of `ls …
   | wc -l` at the lesson's commit time** (47 reports + `swarm-registry.json`); the lesson names no command, so
   the mechanism is inferred from the count and the mtimes, not observed.
