# MutRoutedSpecLedger — C1 mutant probe: every-wave-spec-has-a-started-ledger rule removed

Seat: MoriR24.MutRoutedSpecLedger (mutation-tester leaf). Date: 2026-10-22. No subagent dispatch.
Task: mutate `tools/mori-routed-check.py` so the "every wave spec has a started ledger" rule is
removed; construct a round with a spec and no ledger in a scratch clone; run unmutated and mutated
tool on the relevant revisions and on committed tamper commits; report verdict and restoration.

## Setup (scratch only; lane never touched)

- Scratch root: `/fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedSpecLedger/`
  - `clone-pristine/` — `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin`,
    checked out at measured lane tip `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`, plus tamper
    commits below. Pristine tool bytes.
  - `clone-mutant/` — same checkout; tool mutated in working tree, then restored.
- Lane repo was only read (git reads from `/home/vgpnk/Projects/shokunin/mori-shokunin` to clone);
  no lane file was touched except this report. No push, no `git`/`jj` mutation in the lane.
- Tooling: system `python3 3.14.8` and `git 2.56.0`; no new tool installed (no installs or
  upgrades this session; pacman untouched).

## Mutant

Behavior-bearing point: `_check_r4`, the enforcement of the rule:

```
647:        if not started:
648:            reasons.append("wave_spec_without_started_ledger")
```

Mutated by deleting those two lines (the spec loop still runs and still records
`"started": false` in the detail payload; it just no longer turns R4 red). This is the smallest
change that removes the rule's effect on the verdict.

- Byte hashes of `tools/mori-routed-check.py` (sha256):
  - committed blob at a730ecf (and pristine worktree): `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14`
    (git blob oid `3337232ba364d5d290e0cf7c93d1bcb816f75562`; matches w1 BuildRoutedCheck.md:16)
  - mutated worktree: `9e4624f84cd3dcd98d3fb4cb393d1114a73d3b67d3e17d2e1bf875733daac459`
  - restored worktree: `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14`,
    `git diff --exit-code` vs HEAD clean (worktree == committed blob; blob oid matches).

## Tamper commits (committed in clone-pristine only)

- Tamper B, `829b05d313c441a0c2739f7d03380701c41edd41`: adds
  `.ufo/waves/round-24/wave3-spec.json` (wave `mori-r24-w3`) with **no** wave3 ledger; the round
  still has the committed wave1 spec + `wave1-attempts.json` (clean, started). Round-24 tree at
  a730ecf contains only wave1 (git ls-tree confirmed; wave2 files are not committed at this rev).
- Tamper A, `f500b290c6278afaee02696f5174f40c9cb5dede`: adds `.ufo/waves/round-25/wave1-spec.json`
  — a round with a spec and **no ledger at all**.

## Runs (all `python3 -I tools/mori-routed-check.py --repo <clone-pristine> --rev <REV> --round N`; repo = clone-pristine for every run so both tools read identical committed bytes)

| run | tool | rev / round | exit | status | held | R4 held | R4 reasons |
|---|---|---|---|---|---|---|---|
| 01 | pristine | a730ecf / 24 | 0 | held | 4/4 | true | [] |
| 02 | pristine | c725aa37 / 23 | 1 | failed | 3/4 | false | 20 reasons (ledger unclean/AT_INVALID/LEGACY_ROW_UNBOUND/STARTED_MISSING; 8 dispatch_path_missing; 8 dispatch_committed_after_dispatch) |
| 03 | pristine | tamper B / 24 | 1 | failed | 3/4 | false | `["wave_spec_without_started_ledger"]` |
| 04 | pristine | tamper A / 25 | 1 | failed | 3/4 | false | `["no_round_ledger"]` |
| 05 | mutant | a730ecf / 24 | 0 | held | 4/4 | true | [] |
| 06 | mutant | c725aa37 / 23 | 1 | failed | 3/4 | false | identical 20 reasons as run 02 |
| 07 | mutant | tamper B / 24 | 0 | held | 4/4 | true | [] |
| 08 | mutant | tamper A / 25 | 1 | failed | 3/4 | false | `["no_round_ledger"]` |

Outputs saved in scratch root as `run-01…run-08-*.json`. Diff checks:
- run 01 vs 05: byte-identical; run 02 vs 06: byte-identical (the mutant changes nothing on the
  real revisions; the round-24 tip still holds and round 23 at base still goes red with the same R4 reasons).
- run 03 vs 07 differ exactly in the R4 row: pristine reports `held:3`, reason
  `wave_spec_without_started_ledger`; mutant reports `held:4`, no reasons (R4 held).

## Verdict: SURVIVED (cover finding)

The discriminating tamper is B: one clean started ledger exists, and a second wave spec has no
ledger. Pristine: R4 red (`wave_spec_without_started_ledger`, exit 1). Mutant: R4 held, full tool
green, exit 0. No other predicate in the tool flags the missing wave3 ledger; R1–R3 stay green
(the tamper lives under `.ufo/waves/round-24/`, which R1/R3 do not pin, and the R2 added-line scan
excludes `.ufo/**` per amendment A1). So the removed rule is the only detector of a per-wave missing
ledger once at least one ledger exists.

The literal "round with a spec and no ledger at all" case (tamper A) is still caught by both the
pristine and the mutated tool via the separate early-return rule `no_round_ledger`
(`_check_r4` lines 552–554) — that rule is untouched by this mutant, so this case is inconclusive
for this mutant (not a kill).

## Existing controls

- No built-in automated test suite exercises `tools/mori-routed-check.py` (SKILL.md round-24 row:
  "none built in; able-to-fail evidence is thirteen sandbox mutants in .ufo/waves/round-24/w1/BuildRoutedCheck.md").
- The w1 battery (BuildRoutedCheck.md:194–210) does not kill this mutant:
  - M6 "remove the round-24 attempts ledger" is the `no_round_ledger` early-return path (still red
    under the mutant — run 08 pattern), not the spec-vs-ledger rule.
  - M7 "ledger last row refused" reddens R4 through ledger-verify findings
    (`attempt_ledger_not_clean`, `ledger_finding:STARTED_MISSING`) that are independent of the
    removed loop; `wave_spec_without_started_ledger` is only a secondary reason there.
  - No w1 mutant adds a spec without its own ledger while another ledger remains; none would turn red
    solely by the removed rule.
- w1's own limit statement (BuildRoutedCheck.md:233–235) asserts "A spec with no matching ledger is
  red" — the mutant contradicts that claim for the mixed-ledger case, which is exactly the gap.

## Restoration evidence

- `clone-mutant/tools/mori-routed-check.py` restored with the two deleted lines re-inserted at the
  same position; sha256 back to `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14`,
  `git diff --exit-code` clean vs HEAD (blob oid `3337232ba364d5d290e0cf7c93d1bcb816f75562`).
- `clone-pristine` retains the two tamper commits (B `829b05d…`, A `f500b290…`); its working tree
  is clean and its tool file is unmutated.

## Findings

1. Mutant survives: after removing the every-wave-spec-has-a-started-ledger rule, a round with a
   clean started ledger plus a spec with no ledger passes fully green (`held:4`, exit 0) where the
   pristine tool reports `wave_spec_without_started_ledger` (exit 1). Surrogate = coverage finding:
   this clause of R4 is the sole detector of a missing per-wave ledger when any other ledger exists.
2. The "no ledger at all" shape is still caught by a different rule (`no_round_ledger`), so the
   deleted clause's exact gap is the mixed case above.
3. Mutant changes no output on the real revisions (a730ecf/24 and c725aa37/23 byte-identical to
   pristine), so the C1 after-value and the "red on round 23" repair story are unaffected by this
   mutation.
