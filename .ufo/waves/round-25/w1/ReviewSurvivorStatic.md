# ReviewSurvivorStatic — static classification of the six round-24 pressure survivors at the tip

Seat: `MoriR25.ReviewSurvivorStatic` (reviewer, leaf — no subagents, no background jobs).
Date: 2026-10-22. Lane tip at time of review: `129832e3e8a710d47ecd0425efb9fc67ecf59697`
(`git log -1` in the lane, read-only). Round-24 wave-2 reports were authored against
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`; classification below is against the tip bytes of
`tools/mori-pressure.py` (blob `5785c5b23233a5ed1d2116ab610f9aa0cf3b12ec`) and
`tools/fixtures/mori-pressure/supplementary-cases.json` (blob `4d00f164be8ea856da80e059a139a5e78c67d17e`).
Working tree is clean for both files (`git status --porcelain -- <both>` empty, exit 0).

Method: **static differential reasoning only** — for each survivor, derive the mutant's behavior on the
tip bytes and find the committed assertion whose evaluation must differ. No mutant was applied anywhere;
this is deliberately independent of SurvivorReplay's dynamic replay. As premise verification I did run the
pristine tip tool read-only (`python3 -I -B`, in-process hooks, no `/proc` access, no writes):

- `python3 -I -B tools/mori-pressure.py --selftest` → `MORI_PRESSURE_SELFTEST: PASS 12/12` /
  `MATCHER: rejected 48/48 corrupted expectations`, exit 0.
- `python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json`
  → `MORI_PRESSURE_SELFTEST: PASS 7/7` / `MATCHER: rejected 28/28 corrupted expectations`, exit 0.

Tooling record: no tool installed or upgraded (system `python3` 3.14.8 and `git` sufficed; nothing to
record under the operator directive). No pacman action, no jj command, no mutating git command in the
lane; the only lane file written by this seat is this report. All paths below are lane-relative.

## 1. The six survivors (from the 12 wave-2 verdict tables, run at a730ecf)

Killed at round 24 (not in scope): EnoentZero (P04), FieldSwap (P01/P02/P03/P06/P07), ErrnoMap A+B
(P05/P10), Ratio (P11), CpuFullDelta (P11), Regressed (P12), IrqSome (P03 et al.), CpuFullThreshold (P02),
plus VerdictOrder's secondary mutant (PARTIAL exits 2; killed by P04/P08/P09/P10/P12).

The six SURVIVED mutants (one file each: `.ufo/waves/round-24/w2/MutPsiGrammar.md`,
`MutPsiVerdictOrder.md`, `MutPsiMatcher.md`, `MutPsiThresholdEdge.md`):

| # | Survivor | Mutant (round-24 definition) |
|---|---|---|
| 1 | ThresholdEdge | `_findings` line: `avg10 >= warn_avg10` → `avg10 > warn_avg10` |
| 2 | Grammar A | `LINE_RE` … `total=([0-9]+)$` → `total=([0-9]+)(?: .*)?$` (extra trailing fields accepted) |
| 3 | Grammar B | duplicate-kind guard in `_parse_resource` deleted (second same-kind line overwrites) |
| 4 | Grammar C | `total=([0-9]+)$` → `total=(-?[0-9]+)$` (negative total accepted) |
| 5 | VerdictOrder | verdict `elif` blocks swapped: PARTIAL branch precedes HIGH branch |
| 6 | Matcher | `_case_failures` findings_include gate → `if False:` (missing-finding check disabled) |

Tip diff `git diff a730ecf..HEAD -- tools/mori-pressure.py` (read-only) shows the six mutant sites
byte-equivalent to round 24; the only tool changes are a UTF-8-decode→`malformed` branch
(`tools/mori-pressure.py:162-164`), thresholds tolerating `counter_regressed` second reads
(`:290-292`), the `--cases` option (`:391-392`, `:530`), and the `_corrupted_expectations` matcher
controls (`:503-525`, `:566-572`, `:581-588`). Survival at a730ecf therefore implies survival at the tip
absent the new supplementary cases and controls.

## 2. Classification at the tip: all six covered — five by S-cases, one by the matcher controls

### 2.1 ThresholdEdge — COVERED by S01

- Mutant site at tip: `tools/mori-pressure.py:302` (`if avg10 >= warn_avg10 and …`).
- S01 (`tools/fixtures/mori-pressure/supplementary-cases.json:6-34`): memory `some avg10=10.00 …` exactly
  at the default threshold (`:13`); `expect` exit `1` (`:21`), verdict `PRESSURE_HIGH` (`:22`),
  `findings_include [["PRESSURE_HIGH","memory"]]` (`:29-32`).
- Pristine: `10.00 >= 10.0` → finding (`:302-311`) → HIGH/exit 1 → S01 passes.
- Under the mutant (derived): `10.00 > 10.0` is false, no eligible finding anywhere (all other avg10
  values are below 10.0) → verdict `PRESSURE_OK`, exit 0. Killed assertions: "exit 0 != 1"
  (`tools/mori-pressure.py:464-465`), "verdict PRESSURE_OK != PRESSURE_HIGH" (`:466-467`), and
  "finding PRESSURE_HIGH on memory missing" (`:494-499`). Selftest FAIL ⇒ mutant killed. [INFERENCE on
  mutant behavior; derivation from committed bytes]

### 2.2 Grammar A (extra trailing field) — COVERED by S02

- Mutant site at tip: `tools/mori-pressure.py:121-124` (`LINE_RE`, `total=([0-9]+)$` at `:123`), applied
  via `.fullmatch` (`:175`).
- S02 (`supplementary-cases.json:37-60`): io file line `some avg10=3.21 … total=654321 junk=1` (`:45`);
  `expect` verdict `PRESSURE_PARTIAL` (`:53`), `io.state == "malformed"` (`:56`).
- Pristine: `fullmatch` fails on the trailing `junk=1` token → `malformed` (`:176-178`) → PARTIAL/exit 0
  → S02 passes.
- Under the mutant (derived): the loosened regex consumes ` junk=1`, io parses `ok` → "io.state is 'ok',
  expected 'malformed'" and "verdict PRESSURE_OK != PRESSURE_PARTIAL" (`:466-467`, state branch
  `:468-493`). Selftest FAIL ⇒ killed. [INFERENCE on mutant behavior]

### 2.3 Grammar B (duplicate kinds) — COVERED by S03

- Mutant site at tip: `tools/mori-pressure.py:180-182` (`if kind in kinds: return STATE_MALFORMED`).
- S03 (`supplementary-cases.json:63-86`): memory file carries `some` twice (`:70`, second line identical
  to the first); `expect` verdict `PRESSURE_PARTIAL` (`:79`), `memory.state == "malformed"` (`:82`).
- Pristine: duplicate `some` → `malformed` (`:180-182`) → PARTIAL/exit 0 → S03 passes.
- Under the mutant (derived: guard deleted, per MutPsiGrammar.md mutant B): the second `some` overwrites
  the first, memory parses `ok` → "memory.state is 'ok', expected 'malformed'" and "verdict PRESSURE_OK
  != PRESSURE_PARTIAL". Selftest FAIL ⇒ killed. [INFERENCE on mutant behavior]

### 2.4 Grammar C (negative total) — COVERED by S04

- Mutant site at tip: `tools/mori-pressure.py:123` (`total=([0-9]+)$`).
- S04 (`supplementary-cases.json:89-112`): cpu line `some avg10=1.23 … total=-5 …` (`:95`); `expect`
  verdict `PRESSURE_PARTIAL` (`:105`), `cpu.state == "malformed"` (`:108`).
- Pristine: `[0-9]+` cannot match `-5`, `fullmatch` fails → `malformed` (`:175-178`) → PARTIAL/exit 0 →
  S04 passes.
- Under the mutant (derived: `total=(-?[0-9]+)$` per MutPsiGrammar.md mutant C): `int("-5")` parses, cpu
  is `ok` → "cpu.state is 'ok', expected 'malformed'" and "verdict PRESSURE_OK != PRESSURE_PARTIAL".
  Selftest FAIL ⇒ killed. [INFERENCE on mutant behavior]

### 2.5 VerdictOrder (PARTIAL beats HIGH) — COVERED by S05

- Mutant site at tip: `tools/mori-pressure.py:344-350` — swap so the `any(s != STATE_OK …)` PARTIAL
  branch (`:347-348`) precedes the `elif findings:` HIGH branch (`:345-346`).
- S05 (`supplementary-cases.json:115-149`): memory `some avg10=25.00` (`:122`) plus irq injected ENOENT
  (`:126`) — the finding+non-ok combination whose absence MutPsiVerdictOrder.md names as the gap;
  `expect` exit `1` (`:131`), verdict `PRESSURE_HIGH` (`:132`), `irq.state "absent"` with null
  some/full (`:134-137`), `findings_include [["PRESSURE_HIGH","memory"]]` (`:145-147`).
- Pristine: findings computed first (`tools/mori-pressure.py:341`), non-empty → HIGH branch (`:345-346`)
  → exit 1 → S05 passes.
- Under the mutant (derived): irq `absent` makes `any(s != STATE_OK)` true, so PARTIAL wins → exit 0.
  `findings` are still emitted (computed at `:341`, before the verdict block), so the findings_include
  assertion alone would NOT catch it — the kill is exactly the pair "exit 0 != 1" (`:464-465`) and
  "verdict PRESSURE_PARTIAL != PRESSURE_HIGH" (`:466-467`). Selftest FAIL ⇒ killed. [INFERENCE on mutant
  behavior]

### 2.6 Matcher (findings_include gate disabled) — COVERED by the matcher controls, not by any case's content

- Mutant site at tip: `tools/mori-pressure.py:498` (`if not any(f.get("id") == fid …)` → `if False:`),
  i.e. a pure permissiveness increase in the selftest matcher.
- Structural fact: no suite in which every case passes can kill such a mutant — a disabled
  failure-emitting branch only shrinks the failure set, so `PASS n/n` is invariant under it. This is why
  S01–S07 cannot be the killer: S01/S05/S07's `findings_include` pairs are genuinely emitted on pristine
  bytes, so the gate is unobservable on them, exactly as MutPsiMatcher.md argued for P06/P07.
- The tip closes this structurally instead: `_corrupted_expectations`
  (`tools/mori-pressure.py:503-525`, docstring `:504-505` names the wave-2 finding) derives, for every
  passing case, four deliberately wrong expectation copies — wrong verdict (`:508-512`), wrong exit
  (`:513-515`), and the one that matters here: `findings_include` extended with the impossible pair
  `["PRESSURE_HIGH", "absent-resource"]` (`:516-518`). It is impossible because `_findings` only ever
  iterates `RESOURCE_NAMES` (`:286-288`), so no emitted finding can carry resource
  `"absent-resource"`; the pristine gate therefore rejects the copy. `_selftest` requires rejection of
  every control (`:566-572`); any accepted control prints `MATCHER: accepted …` and FAILs with exit 1
  (`:581-585`).
- Under the mutant (derived): the finding control is accepted (gate disabled → no problems), so the
  mutated tool fails its own DEFAULT frozen-12 selftest — the only one of the six whose kill does not
  require loading the supplementary file at all. Selftest FAIL ⇒ killed. [INFERENCE on mutant behavior]
- Premise check on the controls (observed): the two pristine runs above report `rejected 48/48` (12
  cases × 4 controls) and `rejected 28/28` (7 × 4) — the counts confirm every case yields all four
  controls and all are rejected (each case's `expect` pins at least one resource state, so the
  `state` control exists for each; `:519-525`).

Run-scope nuance (binding for any replay): kills 2.1–2.5 materialize only in a selftest run that loads
`tools/fixtures/mori-pressure/supplementary-cases.json`
(`python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json`);
the default frozen-12 run alone would still pass survivors 1–5 (they survived exactly that run at round
24). Survivor 6 is killed by the default run itself. Both runs are green on pristine tip bytes (§0).

## 3. No survivor left uncovered; adjacent gaps S06/S07 are not among the six

- S06 (`supplementary-cases.json:152-176`) pins EPERM → `unreadable`, never zero. This covers the mutant
  MutPsiErrnoMap.md only *predicted* would survive ("An EPERM->ok mutant would be expected to survive
  today") — that mutant was never applied in round 24 and is not one of the six run-verdict survivors.
- S07 (`supplementary-cases.json:181-220`) pins the A3/F1 rule that a regressed memory counter does not
  hide a second-read threshold breach (`expect` `counter_regressed` + `PRESSURE_HIGH`/exit 1,
  `:208-219`; made implementable by the tip's `:290-292` change) — a wave-2 ReviewPressureCode finding,
  not a wave-2 mutant survivor.
- Discrepancy worth recording: the supplementary note (`supplementary-cases.json:3`) lists the survivors
  as "threshold edge, grammar looseness, verdict precedence, EPERM" — it omits the Matcher survivor and
  counts the EPERM prediction. The run-verdict tally from the 12 reports is: Grammar×3 + VerdictOrder +
  Matcher + ThresholdEdge. Both the EPERM gap (S06) and the Matcher survivor (controls) are covered at
  the tip either way, so there is no coverage hole — but survivor counting should use run verdicts, not
  predictions.

## 4. Verdict

All six round-24 survivors are covered at the tip: 1 by S01, 2 by S02, 3 by S03, 4 by S04, 5 by S05, and
6 by the `_corrupted_expectations` matcher controls. None is "still uncovered", so under the contract's
replay clause none of the six should need an "explained" outcome; a dynamic replay that fails to kill any
of the six at the tip would contradict this derivation and should be re-examined on both sides.

## 5. Residual risk and verification gaps

1. Mutant behaviors in §2 are static derivations from the round-24 mutant definitions applied to tip
   bytes, marked [INFERENCE]; no mutant was executed (assignment mandates static classification). The
   pristine premises (all cases pass, all controls rejected) were observed, not assumed.
2. Cross-check with SurvivorReplay: their report had not landed in `.ufo/waves/round-25/w1/` at read time
   (only `PlanDataWalk.md`, `BuildJobRunwayTool.md`, `QualityCriteriaDraft.md`, `swarm-registry.json`
   present; the registry lists `SurvivorReplay` as a w1 member). Comparison is therefore pending, not
   contradicting.
3. The matcher `state` control flips only the first (sorted) resource that has a `"state"` key per case
   (`tools/mori-pressure.py:519-525`): resource-state equality is control-checked 1-of-N per case. Not a
   gap for the six survivors, noted as residual for future matcher mutations targeting the
   some/full field loops (`:472-493`).
4. The finding control's impossibility argument rests on `_findings` iterating only `RESOURCE_NAMES`
   (`:286-288`); a future change emitting findings for non-canonical resource names would silently
   weaken it.
5. Grammar kills (§2.2–2.4) rest on `.fullmatch` semantics at `tools/mori-pressure.py:175`, verified in
   tip bytes and consistent with MutPsiGrammar.md's own behavior probes.

Report: .ufo/waves/round-25/w1/ReviewSurvivorStatic.md
