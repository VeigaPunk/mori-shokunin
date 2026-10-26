# Mo51RevPromptConformance — round-51 prompt conformance review (wave w1)

Seat: `Mo51RevPromptConformance` (reviewer, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope assigned: check the round so far against `mori-round-51.md` §2, §2b, §4, §5, §6 items 2–10, §7, the
frozen contract (`.ufo/waves/round-51/contract.md`, sha256 `e5b02168c7…`), and the data commit
`87e0c374537557754bf71dd68036ded3ddc6699c`; report what the round would still fail, with pointers.

Method (all read-only): READ prompt sections (lines 9–131, 265–624 of the prompt file), the contract, the lane
history `aa3af1ec… → 4677910e… → 87e0c37… → b504cb17…`, `evidence/` receipts, `w1-spec.json`,
`w1-dispatch.json`, `w1.ready(.dispatched)`, SCORECARD.md `## Axes`, `considerthese/2026-10-26.md`, the landed
entry and `SOURCES.md` rows S492–S496, and live process/scratch state. No file was modified; no counter/predicate
change proposed (frozen); no tool installed; no pacman transaction.

## 1. Claims — §2 (PASS)

- Two claims, distinct axes: C1 on **operability** (7), C2 on **depth** (5). Neither is exploratory; no
  stagnation waiver (contract: "No stagnation waiver; no exploratory claim"); no retirement.
- Lowest-axis claim: lowest non-retired axes are depth/freshness/calibration (all 5, SCORECARD.md:12-14
  `## Axes`); C2 works depth — the lowest-axis requirement holds.
- Each claim declares a falsifiable before→after with a counting command (`count-c1.py`, `count-c2.py`), each
  with a do-nothing control that stays red (control-c1-do-nothing.txt: `C1=unmet kill_residue=12547`;
  control-c2-do-nothing.txt: `C2=unmet … failed=entry_absent,pins`).
- Separability: contract `## Separability` asserts disjoint surfaces; counts confirm C1 diff touches
  `tools/mori-pin-check.py`, `.ufo/waves/round-40/conform.py`, `SKILL.md`, `SHONEN.md`; C2 touches corpus entry,
  SOURCES rows, source copies and `ENTAIL` votes only.

## 2. Controls before data — §9/contract (PASS)

- Commit chain (verified by `git log` and parent hashes):
  1. `aa3af1ec` entering tip (round-50 closure),
  2. `4677910e` **freeze** — contract, both counters, `controls/` (builder + witness bytes), all control
     receipts, `census-start.txt`, `sweep-memavailable.txt`, `freeze-sha256.txt`, five source copies under
     `corpus/evidence/sources-r51/`,
  3. `87e0c37` **data** — C1 tool/conform/SKILL/SHONEN changes, C2 entry + rows S492–S496, selftest receipts,
  4. `b504cb17` wave w1 spec/dispatch + at-data receipts.
  Freeze strictly precedes data; nothing was scored before the freeze.
- Control readings in `contract.md` match the receipts verbatim (spot-checked `do-nothing` and `witness` rows;
  `c1-at-data.txt` matches the target line `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
  selftest=pass=119,fail=0`; `c2-at-data.txt` reads exactly `failed=entailment`, the required pre-review state).
- Witness disclosed: `controls/witness/` committed in freeze, flagged "disclosed, not the claim's landing".

## 3. Frontier step — §2b (census PASS; lesson PENDING; sourced claim PASS)

- Census start: `evidence/census-start.txt` — same command as §2b, exit 0, 22 W04 + `ok` (counted 22 W04
  lines). Matches the contract's claim.
- Mined mistake: the round-51 lesson `corpus/lessons/round-51.md` does **not exist yet** (expected end-of-round;
  a scribe draft sits in `w1/Mo51ScribeMistakes.md` with rows M1/M2). Watch: must land with the report and must
  show the fix "able to fail" (the control table already demonstrates it: do-nothing red vs witness/target green).
- Sourced claim: C2 rests on S492–S496, all `mined`, opened 2026-10-26, URL among the five frozen sources,
  `used-by` listing `corpus/knowledge/memavailable-estimate-r51.md` (SOURCES.md:271-275) — the sourced-claim
  requirement holds.

## 4. Assimilation — §6 item 10 (PASS as stated; report line PENDING)

- Contract states `Assimilation: none — merge/mori/ holds no staged entry or row on MemAvailable`, backed by
  `sweep-memavailable.txt` tail (`grep -rl … /home/vgpnk/Projects/shokuknow/merge/mori` → rc=1, no file).
- The end report must still carry the literal `Assimilation: none` line in its Sources & frontier section
  (§6 item 10: "A round either assimilates or says `Assimilation: none`").

## 5. considerthese — §6 item 10 (PASS)

- `considerthese/2026-10-26.md` suggestion 1 ("Split pin-check mismatches into 'can't run here' and 'stale'")
  is implemented inside C1 arm C: v5 diff adds `class=env`/`class=stale` per mismatch line and the summary ends
  `env=N stale=N`; the classified fixture row in `c1-at-data.txt` shows `class=env` ×2 and `class=stale` ×2,
  `env=2 stale=2`. At most one unimplemented proposal per round is honored (suggestion 2 was already adopted as
  QUALITY 127 in a prior round, not re-claimed).

## 6. Round shape — §6 item 2 / contract (PASS)

- One v2 wave `w1`: spec and dispatch both carry **68 items** (w1-spec.json `items`=68; w1-dispatch.json
  `counts.spawn=68, resume=0, total=68`; `taskCall.tasks`=68 — one batched task call, payload unchanged).
- Band: policy v2 `waveMinLanes=64 ≤ 68 ≤ waveMaxLanes=128`; `maxLanes=256` hard ceiling untouched;
  `w1-validate.err` empty (validator rc 0).
- Attack share: reviewer 14 + critic 12 + mutation-tester 3 = **29/68 ≈ 42.6 % ≥ 25 %** (42 sentinel 4
  attack seats → 48.5 %). No labrat seats; residual calls 0.
- `w1.ready` was taken once (`w1.ready.dispatched` stamped 2026-10-26T19:48:42 with seat ids), after the data
  commit (19:37) — dispatch order correct.

## 7. Report sections — §4 (PENDING — end-of-round deliverable)

- The round report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-51/mori.md` does not exist yet; the wave is
  mid-flight. The required §4 sections, the `Stale-lane` line, the census-after run (exit 0 required), the
  lesson, and LOG.md/SCORECARD.md updates are all still outstanding. Nothing observed so far would block them.

## 8. Misroot sweep & lane hygiene — §3/§7 (one MED finding, below)

- No stray reports outside `w1/` were found: lane `git status` shows only `w1/`, `w1.ready`,
  `w1.ready.dispatched` and `.ufo/waves/round-39/scratch/` as untracked; the fleet root status (excluding w1)
  is clean; no tracked file is modified anywhere.
- However, see finding F1/F2: during this wave, committed old instruments were executed in place and re-created
  lane-anchored scratch under `.ufo/waves/round-39/scratch/` (untracked leftover).

## 9. Scratch discipline — §7 (partial; F1/F2)

- My seat scratch: `/fast/scratch/hyaku/mori-r51/Mo51RevPromptConformance/` created, used for TMPDIR, and
  removed at exit (reported). Disk guard at start: `/fast/scratch/hyaku` 26 % used, 597 GB free — no ENOSPC risk.
- Wave seats' scratch dirs are still present under `/fast/scratch/hyaku/mori-r51/` (36+ dirs, several with live
  processes) — expected mid-wave; §7.2 requires each to self-remove before yield.

## 10. ENTAIL vote status — P-C2 entailment arm (wave output check)

- All 21 claim rows currently have ≥ 1 vote (39 `entailed` votes).
- **4 rows are blocked by `overclaim` votes**: rows 6 (`5d06a2ae70cf`), 12 (`ec0f6c97eeba`), 14
  (`a06f1037d952`), 15 (`102feb3debfa`). Per the contract these rows must have their claim text replaced by the
  L1 (new hash) before P-C2 can pass; the dissent on the old text then matches no row. Five extra voted hashes
  (`0a908e8eb4f3`, `56b7a3309d66`, `d901a2d666fb`, `6c2327e19df1`, `7e14f1771092`) are candidate replacement
  texts, some already carrying `entailed` votes — expected pre-integration state, not failure.
- Only ENTAILMENT seats wrote vote lines; all vote lines parse (`ENTAIL <12 hex> entailed|overclaim — …`);
  zero nonconforming lines. `Mo51CritEntailArm.md` mentions ENTAILMENT only in prose (allowed).

## Findings

- **MED — F1** `.ufo/waves/round-39/conform.py` (committed, unmodified) hardcodes
  `SCRATCH_ROOT = <lane>/.ufo/waves/round-39/scratch` (line 54) and its `--selftest` creates/removes work dirs
  there (lines 491-492). Observed during this wave: at 19:50 the untracked `.ufo/waves/round-39/scratch/`
  held `mori-conform-selftest-4m82s7b4/` with per-case files (counter-predicate.py, counter-timeout_value.py,
  …), then emptied at 19:51:04 (dir mtime), leaving the container behind. This recreates the §7-item-4 defect
  class (instrument writing inside the lane) on an unclaimed surface and leaves an untracked leftover in the
  lane. The misroot/relocation sweep must cover round-38/39 conform.py (and counters) as residual host-path
  instruments; the round report should name them as a named limit of C1's scope.
- **MED — F2** Live processes observed executing committed instruments/fixtures directly from the lane tree
  during the wave: `python3 <lane>/.ufo/waves/round-39/fixtures/hang-after-flush.py --selftest` (PIDs
  889684, 1014547, 1042343), `python3 <lane>/.ufo/waves/round-38/fixtures/hang-after-flush.py 6bd57097 --repo
  <lane> --round-base f10a320d` (PID 906007), and `python3 .ufo/waves/round-40/conform.py
  87e0c374537557754bf71dd68036ded3ddc6699c --selftest` from the lane root (PIDs 1019696, 1034906). Read-only
  in-place execution is not itself a mutation, but it couples probes to lane bytes and (per F1) dirtyed lane
  scratch; the wave's own probes should run old instruments from scratch clones under
  `/fast/scratch/hyaku/mori-r51/<seat>/`.
- **LOW — F3** Only 4 of 36 submitted w1 reports carry the `Report:` trailer path prescribed by the seat spec
  (Mo51RevEntail10.md, Mo51RevEntryHeader.md, Mo51ScribeLogScorecard.md, Mo51SentEntryScope.md). Many seats are
  still landing; verify at wave end.
- **LOW — F4** C2 entailment is currently blocked on rows 6/12/14/15 by overclaim votes (hashes above);
  L1 text substitution is required — integration work, not a defect.
- **INFO** End-of-round deliverables still pending and required: the round report with all §4 sections, the
  `Assimilation: none` line, census-after (exit 0), `corpus/lessons/round-51.md` (`## Mistakes`), LOG.md and
  SCORECARD.md updates. Nothing observed blocks these.

## Verification notes

- Receipts read: `c1-at-data.txt`, `c2-at-data.txt`, `c2-hashes-at-data.txt`, `selftest-c2.txt`,
  `census-start.txt`, `sweep-memavailable.txt`, `freeze-sha256.txt`, all `control-c1-*.txt`.
- Wave artifacts read: `w1-spec.json`, `w1-dispatch.json`, `w1.ready`, `w1.ready.dispatched`,
  `w1-validate.err` (empty), `swarm-registry.json` (harness-generated; not seat output).
- Live evidence: `ps -eo pid,etimes,args` at 2026-10-26 ~19:55; `find`/`stat` over
  `.ufo/waves/round-{38,39,40,41}/scratch`.
- No tool install/upgrade performed (none needed); no pacman transaction; no counter, predicate, floor or kill
  rule touched.
