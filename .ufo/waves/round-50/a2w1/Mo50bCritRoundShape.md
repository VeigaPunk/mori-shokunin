# Mo50bCritRoundShape — round-shape honesty (mori round 50, attempt 2, wave a2w1)

Seat: critic (round shape). Leaf seat, no subagents, no edits outside this file, no tool installs.
Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bCritRoundShape/` (created, `TMPDIR` set inside it, removed at exit).
Frozen contract read first: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/contract.md` (freeze `950e99be`),
round prompt §6 item 2 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-50.md`).

I attack only the honesty of the round's shape: how many seats this round spent, what each attempt-1 seat's status
is, whether the landed wave meets the 64–100 directive, and which sentences would overstate. I do not judge C1/C2,
the counters, the entry, or the counters' controls.

## 1. What I read (commands, outputs, exit codes)

All read-only. `S=/fast/scratch/hyaku/mori-r50/Mo50bCritRoundShape`.

1. Dispatcher spawn receipts (the only per-wave spawn record that exists):

       grep -n 'spawned mori 50\|done mori 50\|mori/w1' /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log
       → 1603: 2026-10-26T05:58:49 spawned mori 50 w1 40
       → 1686: 2026-10-26T06:22:15 drive ['MadoR43'] [… 'mori/w1: live 37/40' …]     (last pre-gap w1 tick)
       → 1687: 2026-10-26T08:29:36 adopted …/round-50/w1.ready                        (restart adoption)
       → 1786: 2026-10-26T09:50:39 spawned mori 50 a2w1 64
       → (latest at my read) 1802: 2026-10-26T09:55:56 drive [] ['mori/a2w1: live 24/64' …]
       grep -c 'done mori 50 w1' …  → 0
       grep -c 'spawned mori 50 w1 40' … → 1
       grep -c 'spawned mori 50 a2w1 64' … → 1

2. Wave payloads and registries:

       python3 (scratch) over .ufo/waves/round-50/{w1,a2w1}-dispatch.json
       w1:   dispatch=40 spawn=40 band=32-64  reports=5  results_json=no
       a2w1: dispatch=64 spawn=64 band=64-128 reports=45 results_json=no      (a2 snapshot 2026-10-26T09:56:00-03:00)
       round total dispatched seats: 104
       name intersection w1 × a2w1 = []   (all w1 names `Mo50*`, all a2w1 names `Mo50b*`)
       registry members: w1 40, agentId non-null 0; a2w1 64, agentId non-null 0.

3. Independent re-validation of both wave shapes, in scratch, nothing written under the lane:

       UFO_CONFIG_PATH=…/ufo-wave-policy-v2.json UFO_PROJECT_ROOT="$S/root" \
         node ~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs plan --spec "$S/a2w1-spec.json"   → rc=0
         counts {"spawn":64,"resume":0,"total":64}; policy waveMinLanes=64 waveMaxLanes=128
       same with ufo-wave-policy.json and w1-spec.json                                              → rc=0
         counts {"spawn":40,"resume":0,"total":40}; policy waveMinLanes=32 waveMaxLanes=64
       `find .ufo/waves/round-50 -printf '%p %T@' | sha256sum` identical before/after → lane untouched.
       Planner-seat probe (`{"role":"planner"}` item, policy v2): rc=1,
         {"code":"unknown_role","message":"items[0].role \"planner\" is not a swarm role"} — confirmed.
       Neither spec carries `model` or `modelAlias` (spec keys are exactly context/items/reportDir/wave).

4. Attempt-1 report artifacts (`stat -c '%y %n'`), 5 of 40, all written before the 06:15 host saturation:

       05:51:24 Mo50ScoutCoverageFR1.md   06:01:23 Mo50ScribeRowOomKill.md   06:02:48 Mo50ScribeEntryB.md
       06:06:31 Mo50ScribeRowMemcontrol.md   06:08:03 Mo50ScribeEntryA.md

   All five plus `swarm-registry.json`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready.dispatched` and `w1-validate.err`
   are committed (`git -C …/mori-shokunin ls-tree --name-only 487941b9 .ufo/waves/round-50/w1/` lists exactly those six;
   the round-50 top level lists the rest), so every number above is re-derivable from committed bytes plus the
   dispatcher log.

5. Attempt context: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1507` (launch attempt 1), `:1518`
   (`lane-dead-no-report mori round=50 … attempt 1 L1 died in the orchestrator host crash 2026-10-26 ~08:50 -03
   (omp process exit); no report landed`), `:1519` (launch attempt 2);
   `/home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run8.md:85` ("~08:50: the omp process exited, which
   ended every live agent: L1s SoujiR32, TabiR31, TameshiR48 and MoriR50, plus their seats"), `:30`
   ("64–100 seats per round (lane-addendum §6), as in run 7").
   Neither `w1-results.json` nor `a2w1-results.json` exists (`ls` → No such file or directory, both).

## 2. How the report MUST count seats

**Count spawns, from the dispatcher receipts — never dispatch payloads, never the registries.** A dispatch file
proves an item was authored; the `spawned <lane> <round> <wave> N` line proves N seats started. Round 50 has exactly
two such lines for mori (log:1603, log:1786) → **104 seats dispatched in the round: attempt 1 `w1` 40, attempt 2
`a2w1` 64.**

**Do not count attempt-1 seats as dead, and do not count them as complete.** For the 40 `w1` seats the evidence is:

| evidence | value | what it proves |
|---|---|---|
| dispatcher spawn receipt (log:1603) | 40/40 | all 40 seats were spawned |
| report artifact on disk | 5 (listed §1.4) | those 5 seats ran and wrote a report; their items' completion is not recorded |
| `w1-results.json` | absent | no settle record for any seat |
| `done mori 50 w1` line | 0 occurrences | the wave was never finalized (adopted at log:1687, never re-accounted or re-spawned) |
| registry `agentId` | null × 40 | **nothing** — see caveat below |
| dispatcher live ledger, last tick (log:1686) | `live 37/40` | 3 jobs had ended at 06:22:15 while 5 report files already existed → this ledger is not an outcome ledger either |

Correct classification: **35 seats unknown** ("no report and no outcome record"), 5 seats "report artifact only",
0 seats "dead" and 0 "complete". "Dispatched-dead" is not available as a label: no per-seat death is recorded
anywhere the lane may read, and the wave was fully spawned. The wave-level cause is the host crash (watchdog:1518,
goal:85); that is why the settlement is missing, not a verdict on any seat.

**Registry caveat (blocking if ignored).** `swarm-registry.json`'s `agentId` is null for all 64 a2w1 seats as well —
the wave that demonstrably spawned 64/64 (log:1786) and has 45 reports on disk. The field is therefore the builder's
initial state, never bound; it is evidence neither of spawn nor of death. Any shape sentence that cites "null agent
ids" as the attempt-1 signal is unsound.

**Same caveat for the dispatcher live ledger.** At 09:55:56 a2w1 read `live 24/64` (40 settled) with 45 report files
on disk: seats write their report before they yield, so report-file count ≥ settled count. Report-file counts are
snapshots and must carry their timestamp; settled counts must come from `a2w1-results.json`.

**Attempt-2 settlement must be read from `a2w1-results.json` if the L1 has it at filing, else stated as unrecorded.**
At my read there is no results file; the report may say "N report files on disk at HH:MM", never "64/64 seats
reported" and never "the wave settled".

**Never merge the two ledgers.** Attempt-1 names are `Mo50*`, attempt-2 names are `Mo50b*`; the intersection is empty.
The attempt-2 wave did not replace or resume any attempt-1 seat (no seat name is re-used), so "no dead seat was
replaced" is true, while "no seat died" is unproven.

**Role mix is declared roles from the dispatch `agent` field, not models.** Neither spec passes a model; the route
table decides, and no seat's answering model is recorded. Report role counts and the two run-8 shares, with the
run-8 role lists (`m_flash` = executor, labrat, scribe, sonic, simplifier, critic, revenger, sentinel; attack =
reviewer, critic, mutation-tester, labrat):

    w1:   executor 11, scribe 12, critic 5, connector 3, reviewer 3, mutation-tester 2, scout 2,
          sentinel 1, simplifier 1  → m_flash 30/40 = 75 %, attack 10/40 = 25 %
    a2w1: executor 17, reviewer 15, critic 9, scribe 8, connector 4, scout 3, mutation-tester 3,
          simplifier 2, sentinel 2, revenger 1 → m_flash 39/64 = 61 %, attack 27/64 = 42 %

Both waves meet the §3 L2 floor in one batched wave (connector, ≥3 executor, scribe, scout, reviewer, critic all
present); the canonical planner seat is held by the L1 (planner is rejected as a swarm role, verified above), so no
planner seat appears in either mix — record that mapping.

## 3. Does one v2 wave meet the 64–100 directive?

**Two readings, and only one of them passes — the report must name which it is using and print both numbers.**

- Per landed wave: **yes.** A single v2 wave is the documented alternative shape (§6 item 2: one v2 wave 64–128 under
  `ufo-wave-policy-v2.json`; run 7's shape line: "one v2 wave of 64–100"). `a2w1` is 64 seats, exactly at both floors,
  and re-validates rc 0 under policy v2 (`counts.total 64`, band 64–128). No padding, no residual call.
- Per round, counting every seat the round spawned: **no.** 40 + 64 = 104, which is 4 over the run-8 ceiling
  ("Round size unchanged: 64–100 seats in total"). The excess is the crashed attempt's wave, not filler: it is the
  same 40-seat wave whose settlement is missing, and the retry legitimately re-ran its work under new identities.

The round-sum reading is the defensible one for a shape sentence (a seat spent is a seat spent, and last round's
sibling precedent counted a crashed predecessor's wave in the round total — `kotodama.md` round-50: "Total 139
dispatched seats"). Writing "round total 64" is therefore the one sentence this round cannot afford.

The contract's `## Round shape` line ("Two v1 waves … Total 64–100") was **not** followed: attempt 2 ran one v2 wave.
That is a disclosed deviation, not a rule change — no claim predicate, counter, floor or kill rule in `contract.md`
mentions wave shape — but the report must say so in the same paragraph, or the contract and the report disagree on
their face.

## 4. Wording that would overstate (each with its falsifier)

| overstating sentence | falsified by |
|---|---|
| "round total 64 seats" / "64 seats, within the 64–100 directive" | log:1603 + log:1786 → 40 + 64 = 104; overshoot 4 |
| "attempt 1's wave did not count" (unstated rule) | watchdog:1518 records attempt 1 of *this round*; its 40 seats were spawned and worked |
| "35 dead seats" | no per-seat death record: no results file, no `done` line, registry ids unpopulated for the **settled** a2 wave too |
| "0 dead seats" (kotodama-style "dead/report-less seats: 0") | 35 attempt-1 seats have no artifact and no outcome record — unknown, not zero |
| "5/40 seats completed" | the 5 are report artifacts only; no settle record ties them to item completion |
| "the wave settled" / "64/64 seats reported" for a2w1 | no `a2w1-results.json` at 09:56; 45 report files vs `live 24/64` |
| "w1 was a partial wave" | dispatch and spawn were complete (40/40, log:1603); what is missing is the settlement |
| "104 seats are inside the 64–128 band" | 64–128 is a **per-wave** validator band; the round rule is 64–100 |
| "the registry records the seats' agent ids" | 0 of 104 members carry an id, including the 64 that spawned |
| "no seat died this round" | kill/seat-death records are not readable by this lane (no kernel-MESSAGE grep); attempt-1 outcomes unknown |
| "24 reports on disk" as the a2 figure (from `Mo50bScribeLogScorecard.md:236`) | a moving snapshot: 34 at 09:44, 41 at 09:53, 45 at 09:56 — must be re-taken at filing with its time |

## 5. Proposed round-shape paragraph (paste-ready)

> **Round shape.** Attempt 2 landed the round as **one v2 wave**, `a2w1`, **64 seats** (`a2w1-dispatch.json`,
> `counts.total 64`; re-validated rc 0 under `scripts/hyaku/ufo-wave-policy-v2.json`, band 64–128); this is the
> prompt's single-wave alternative at its floor and a disclosed deviation from `contract.md`'s "Two v1 waves" line —
> no claim predicate, counter, floor or kill rule depends on wave shape. Seats are counted from the dispatcher's
> spawn receipts, not from payloads or registries: `2026-10-26T05:58:49 spawned mori 50 w1 40`
> (`.ufo/state/inline-dispatcher.log:1603`) and `2026-10-26T09:50:39 spawned mori 50 a2w1 64` (`:1786`) →
> **104 seats dispatched in round 50**. The run-8 rule is 64–100 seats in total: the landed wave of 64 is at the
> floor; the cumulative 104 is **4 over the ceiling**, and the excess is the crashed first attempt, not padding — no
> seat was added to a wave, no residual call was made, no seat was replaced, and the two waves share no seat name
> (`Mo50*` vs `Mo50b*`). Attempt-1 accounting (`w1`, 40 seats, spawned 40/40): **5 seats left a report**
> (`Mo50ScoutCoverageFR1`, `Mo50ScribeRowOomKill`, `Mo50ScribeEntryB`, `Mo50ScribeRowMemcontrol`, `Mo50ScribeEntryA`;
> 05:51:24–06:08:03), and **35 seats have no report and no outcome record** — no `w1-results.json`, no
> `done mori 50 w1` line, registry `agentId` unpopulated for every seat of both waves (so it evidences neither spawn
> nor death), and the dispatcher's last pre-crash tick read `mori/w1: live 37/40` at 06:22:15 while five reports were
> already on disk. Their status is **unknown**, not dead: the wave was fully spawned and was ended by the host crash
> (`.ufo/watchdog.log:1518`; `goal-20261026-hyaku-run8.md:85`), after which its ready file was adopted at 08:29:36
> (`inline-dispatcher.log:1687`) and never re-accounted or re-spawned. **a2w1 settlement:** `[L1 fills — if
> a2w1-results.json exists: seat totals by status plus dead seats; if not: "settlement not recorded at filing: N report
> files on disk at HH:MM, no results file, remainder unknown"]`. Role mix (declared roles; the route table picks the
> model, no `model`/`modelAlias` in either spec): w1 executor 11, scribe 12, critic 5, connector 3, reviewer 3,
> mutation-tester 2, scout 2, sentinel 1, simplifier 1 (m_flash-role 30/40 = 75 %, attack 10/40 = 25 %); a2w1
> executor 17, reviewer 15, critic 9, scribe 8, connector 4, scout 3, mutation-tester 3, simplifier 2, sentinel 2,
> revenger 1 (m_flash-role 39/64 = 61 %, attack 27/64 = 42 %). The §3 planner seat is held by the L1 (the validator
> rejects `planner`: `unknown_role`). **Round total 104 seats; dead seats recorded: none; attempt-1 seats with unknown
> status: 35.**

Fill rules for the `[L1 fills]` slot: take every number from `a2w1-results.json`; if it is absent at filing, do not
estimate from `live N/64` and do not use a report-file count as settled — write the unrecorded form with the
timestamp. If a2w1 adds a residual call later, add its seats to the 104 and restate the overrun.

## 6. Counting command for the closure (verified, rc 0, read-only)

```sh
python3 - <<'PY'
import json,re,collections,glob,os
L='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50'
LOG='/home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log'
MFLASH={'executor','labrat','scribe','sonic','simplifier','critic','revenger','sentinel'}
ATTACK={'reviewer','critic','mutation-tester','labrat'}
tot=0
for w in ('w1','a2w1'):
    d=json.load(open(f'{L}/{w}-dispatch.json')); t=d['taskCall']['tasks']
    roles=collections.Counter(x['agent'] for x in t); n=len(t); tot+=n
    mf=sum(v for k,v in roles.items() if k in MFLASH); at=sum(v for k,v in roles.items() if k in ATTACK)
    print(f'{w}: dispatch={n} spawn={d["counts"]["spawn"]} band={d["policy"]["waveMinLanes"]}-{d["policy"]["waveMaxLanes"]}'
          f' roles={dict(sorted(roles.items()))} mflash={mf}/{n}={mf/n:.0%} attack={at}/{n}={at/n:.0%}')
    print(f'   reports={len(glob.glob(f"{L}/{w}/*.md"))} results_json={"yes" if os.path.exists(f"{L}/{w}-results.json") else "no"}')
print('round total dispatched seats:',tot)
for i,line in enumerate(open(LOG),1):
    if re.search(r'(spawned|done) mori 50 (w1|a2w1) ',line): print(f'log:{i}: {line.strip()}')
PY
```

Observed at 2026-10-26T09:56:00-03:00 (output verbatim in §1.2, §1 summary): `w1 dispatch=40 … reports=5
results_json=no`, `a2w1 dispatch=64 … reports=45 results_json=no`, `round total dispatched seats: 104`, and the two
`spawned` lines. The report-file counts in that output move while a2w1 runs; the dispatch/spawn/round-total lines do
not.

## 7. Impacted axes and the smallest safe correction

- **calibration** (AXES: self-assessment quality, overreach caught): the round-shape sentence is the report's own
  self-assessment of scale, and 64-for-104 is exactly the overreach class the axis names. This is report-level, not a
  SCORECARD cell, so C1's counter is unaffected (it reads `SCORECARD.md`/`SHONEN.md` only) — the misstatement would
  still be caught by the closure as false evidence, not by C1.
- **operability** (commands that exist and produce the stated outcome): §6's command is runnable and read-only; it
  gives the closure a receipt for every number in the paragraph.
- Not touched: any claim predicate, counter, control, kill rule, target, source row, or the entry.

**Smallest safe correction:** paste §5's paragraph instead of any summary form, and replace the one `[L1 fills]` slot
under the fill rule. No counter, dataset or wave change is needed; nothing here asks the L1 to dispatch more seats
(that would widen the 4-seat overrun, not repair it).

## Findings

1. **HIGH — the round total is 104, not 64, and "64 seats within 64–100" is the sentence to block.**
   `.ufo/state/inline-dispatcher.log:1603` (`spawned mori 50 w1 40`) + `:1786` (`spawned mori 50 a2w1 64`).
   Concerns the report's round-shape line; proposal in §5.
2. **HIGH — 35 attempt-1 seats must be reported as unknown, not dead and not complete.**
   `.ufo/waves/round-50/w1/` (5 of 40 reports), no `w1-results.json`, `grep -c 'done mori 50 w1'` → 0,
   `.ufo/state/inline-dispatcher.log:1686` (`live 37/40`) vs five report files on disk. A "38 dead seats"-style or
   "0 dead seats" sentence is unsupported either way.
3. **MED — `swarm-registry.json` `agentId` is unpopulated for all 104 seats** (`.ufo/waves/round-50/w1/swarm-registry.json`
   40 nulls; `.ufo/waves/round-50/a2w1/swarm-registry.json` 64 nulls while that wave spawned 64/64 and has 45 reports).
   Citing null ids as spawn/death evidence in the report or in a future round-shape accounting is a false signal.
4. **MED — the dispatcher live ledger is not an outcome ledger.** `live 37/40` at `.ufo/state/inline-dispatcher.log:1686`
   (3 ended) coexists with 5 w1 report files; `live 24/64` at `:1802` coexists with 45 a2w1 report files. Neither
   number may stand in for a settlement count.
5. **MED — the sibling draft's moving snapshot.** `a2w1/Mo50bScribeLogScorecard.md:236` ("24 reports on disk at this
   seat's read") and `:350`: the L1 must re-take the count at filing with its timestamp (34 at 09:44, 41 at 09:53,
   45 at 09:56) and take settlement from `a2w1-results.json`, not from that number.
6. **LOW — the landed shape deviates from `contract.md`'s `## Round shape` line** ("Two v1 waves"). Not a rule change
   (no predicate references shape) but it must be stated in the report, else contract and report disagree on their face.
7. **LOW — planner-seat mapping must be recorded.** `planner` is rejected as a swarm role (`unknown_role`, rc 1,
   probe in §1.3), and no wave carries one; the L1 holds that seat. Omitting the mapping reads as a missing §3 role.
8. **UNVERIFIED — per-seat outcome of the 35 attempt-1 seats**, whether `w1-results.json` will ever be written (no
   line as of 09:56), and every seat's answering model (no `model`/`modelAlias` in either spec; routing is the route
   table's and is not recorded in the wave artifacts).
