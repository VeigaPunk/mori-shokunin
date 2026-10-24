# CriticC1Admission — round 24 wave 2, attack on C1 admission

Seat: `MoriR24.CriticC1Admission` (critic, leaf). Measured tip named in the assignment:
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`. Lane tip when I read it: `13208d2a533380e1231dc935b6c338db99f1ddae`
(wave-2 ledger commit). Scratch and sandbox clone: `/fast/scratch/hyaku/mori-r24-a2/w2/CriticC1Admission/`.
All tool runs below use the `a730ecf` bytes of `tools/mori-routed-check.py` (blob `3337232ba364d5d290e0cf7c93d1bcb816f75562`,
identical at `13208d2`), invoked as `python3 -I rc-a730.py --repo <repo> --rev <rev> --round <N>`.

## Verdict in one paragraph

R4 is a real repair of the **binding clause** of routed item 4 for the failure mode round 23 actually had
(an honest writer committing the dispatch file after the call): it is red on the round-23 defect and green
on both round-24 waves, and an honest late commit turns it red. It is **not** a repair of item 4 as a whole,
and "held 4 of 4" overstates it: three of the four rows are regression guards that also held at base, two
of item 4's four clauses are neither checked nor disclosed in any landed surface, and the ordering is
satisfiable after the fact by the writer (forged committer date, future-dated `at`, a weakened verifier
supplied by the checked revision, or a wave that is never recorded). Survivor with a narrowed statement,
not a confirmation of the claim as worded.

## What I ran (all read-only against the lane; mutants only in the sandbox clone)

| Run | Result |
|---|---|
| `--rev a730ecf --round 24` | exit 0, `held 4/4` |
| `--rev 13208d2 --round 24` | exit 0, `held 4/4`; R4 detail has two ledgers (`wave1-attempts.json`, `wave2-attempts.json`), each `LEDGER_CLEAN`, each row `bound_before_call`, both specs `started` |
| `--rev 753d227 --round 24` (wave-2 spec bound, ledger not yet committed) | exit 1, `held 3/4`, R4 `wave_spec_without_started_ledger` |
| `--rev c725aa37 --round 23` (the real defect) | exit 1, `held 3/4`; `round-23/wave1-ledger.json` verifies `LEDGER_CLEAN` alone, yet its eight rows (`at` 17:03:11Z–17:24:14Z) precede the last change of `round-23/wave1-run.json` in `22772c1` (18:10:59Z); `round-23/wave1-attempts.json` adds `AT_INVALID, LEGACY_ROW_UNBOUND, STARTED_MISSING` |
| `--rev c725aa37 --round 24` | exit 1, `held 3/4`, R4 `no_round_ledger` (construction-fixed, as A4 says) |
| `--rev a730ecf --round 23` | exit 1, `held 3/4` (history is not retroactively repaired, correctly) |
| Lane evidence `.ufo/waves/round-24/evidence/c1-after-13208d2.json` | `held 4`, `items 4`, `rev_commit 13208d2…`; matches my run |

Mutant battery: `/fast/scratch/hyaku/mori-r24-a2/w2/CriticC1Admission/battery.py`, output in `battery.out`
(clone of the lane at `a730ecf`, one reset per mutant, clone reset to `a730ecf` at the end). Real-clock
commits were made at about 06:01 -03:00.

| Mutant | Change | Result | Meaning |
|---|---|---|---|
| K0 | none | exit 0, held 4/4 | control |
| K1a | wave-3 spec and dispatch committed now; ledger row `at` 05:58:00 -03:00 (before that commit) | exit 1, R4 `dispatch_committed_after_dispatch` | an honest late commit is caught (the round-23 mode) |
| K1b | same, dispatch commit made with `GIT_COMMITTER_DATE=2026-10-22T05:57:30-03:00` | exit 0, held 4/4 | forged committer date passes |
| K1c | same late commit, honest dates, row `at` set to 2099-01-01Z | exit 0, held 4/4 | no upper bound on `at`; a writer can satisfy the order after the fact |
| K2a | `git rebase --force-rebase 29c1bf4` (no content change; committer dates become now) | exit 1, R4 `dispatch_committed_after_dispatch` | false red: any integration rewrite of the bind commits flips the after-value |
| K2b | same rebase with `--committer-date-is-author-date` | exit 0, held 4/4 | date-preserving rewrite keeps it green |
| K3 | add `round-24/w3/swarm-registry.json` and a seat report, no spec, no ledger | exit 0, held 4/4 | a dispatched but unrecorded wave is invisible to R4 |
| K4a | zero the `payload_sha256` of the wave-1 row | exit 1, R4 `PAYLOAD_SHA256_MISMATCH` | control for K4b |
| K4b | K4a plus `tools/mori-dispatch-ledger.py` at REV replaced by a stub printing a clean status | exit 0, held 4/4 | R4 runs the verifier supplied by the revision it judges; the verifier is not pinned |
| K5 | one ledger with rows [wave-3 `refused`, wave-1 `started`], plus a wave-3 spec | exit 0, held 4/4 | the "spec has a started ledger" test reads the file's last row, not the last row of that wave; a refused wave counts as started |
| K6 | add `tools/mori-qgroup-probe.py` (quota mechanism text, no `quota` in the path) and a SKILL capability row for quota detection | exit 0, held 4/4 | R1 guards path names only (`tools/mori-routed-check.py:84-85,387-394`), not capability content or SKILL rows |

I did not write any R2 mutant: my bounds forbid writing a line that sets a privacy-clearance key to true.
R2 findings below are static reading of `tools/mori-routed-check.py:50-52`, marked as unrun.

## Findings

### F1 (high) — "repair of item 4" covers one of its four clauses, and no landed surface says so

- Routed text, `corpus/lessons/round-23-verifier-spotcheck.md:65`: bind future dispatches before the call,
  **keep source writers in separate worktrees**, **report extra invocations/resource units accurately**, and
  no census, identity or model-role metric is universal no-harm proof.
- R4 (`tools/mori-routed-check.py:545-650`) tests only binding order, ledger cleanliness and spec pairing.
- Wave 1 already raised this (`.ufo/waves/round-24/w1/CriticC1Vacuity.md:142-144`;
  `.ufo/waves/round-24/w1/ReviewDeclarationSizing.md` F11 at about line 164). At `13208d2`,
  `git grep -i "worktree|extra invocation|resource unit|F11|clause"` over `corpus/QUALITY.md`,
  `corpus/lessons/round-24.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md` and the contract finds no disclosure
  (the only hits are unrelated older rows). QUALITY 75 (`corpus/QUALITY.md:327-331`) and the lesson
  (`corpus/lessons/round-24.md:9-11`) call R4 "the repair" of item 4 without the scope limit.
- Impacted axes: calibration (premature saturation: the item is counted as held while half of it is unchecked).

### F2 (high) — "held 4 of 4" counts three guards that held at base

- `--rev c725aa37 --round 23` and `--round 24` both give R1–R3 green. The only row that moves is R4.
  A4 relabels R1–R3 as guards and QUALITY 72–74 say "Regression guard", but the after-value still reads
  as four held routed items, and the SCORECARD declaration row (`SCORECARD.md:1501` at `13208d2`) still says
  "repair the four byte-checkable round-23 routed items" with the construction-fixed before ("3 of 4 …
  no round-24 pre-call ledger") and "no check exists", which A4 and A5 superseded in the contract.
- Impacted axes: calibration (identity change: guard rows presented with repair weight).

### F3 (medium, inherent tradeoff, partly fixable) — the ordering is self-attested and post-hoc satisfiable

- K1b and K1c pass a dispatch committed after the call. A4 and QUALITY 75 disclose "recorded ordering, not
  harness-observed ordering", which is correct and should stay; K1c shows an extra, cheap gap the
  disclosure does not mention: `at` has no upper bound, so the row can be written after a late commit.
- Corroboration I checked, and its limit: the planner registries bracket each `at` consistently.
  `createdAt` is stamped by `ufo-swarm-wave.mjs run` (payload generation) and `updatedAt` by `record`
  after the call returns (`/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:47-58,616-622`).
  Wave 1: run 05:13:51.297 < bind `06d4f4d` 05:13:57 < `at` 05:14:13.93 < record 05:14:34.622 < ledger
  commit `4059ffb` 05:14:40 (all -03:00). Wave 2: run 05:56:35.904 < bind `753d227` committer 05:56:36
  < `at` 05:56:44.92 < record 05:56:58.238 ≤ ledger commit `13208d2` 05:56:58. These are lane-run script
  times, not harness times. My own session header shows a spawn at 08:56 UTC (minute granularity): consistent,
  not discriminating. My received assignment text equals task 30 (`CriticC1Admission`) of the committed
  `wave2-run.json` at `13208d2`, which corroborates payload identity from the receiving side for one seat.
  No harness-side call record was found: `~/.omp/agent/agent.db` (opened read-only) holds auth and usage tables only.
- Impacted axes: calibration (false provenance if presented as verified ordering).

### F4 (medium, fixable) — the judged revision supplies its own ledger verifier

- `_run_ledger_verify` executes `tools/mori-dispatch-ledger.py` from REV (`tools/mori-routed-check.py:329-350`);
  no row pins that blob. K4b: a stub verifier turns a digest mismatch green. The tool is unchanged since
  base (`git diff --quiet c725aa37 13208d2 -- tools/mori-dispatch-ledger.py`; blob
  `b86525c6a9fe0d44e90127323ff291104dcfb5fd`), so pinning costs nothing today.
- The same applies one level up: the after-value command runs the routed check from the tip. A closure that
  runs the tip's copy instead of blob `3337232b…` inherits any later edit to the checker.
- Impacted axes: calibration (duplicate authority: the subject also provides the judge).

### F5 (medium, fixable) — unrecorded and mixed waves

- K3: R4 sees only `*-attempts.json`, `*-ledger.json` and `wave*-spec.json` directly under the round
  directory (`tools/mori-routed-check.py:477-489`). A wave with a registry and reports but no spec and no
  ledger passes. Each wave already leaves `round-24/w<N>/swarm-registry.json`, which R4 ignores.
- K5: `started` is decided by `rows[-1]` of the whole file (`tools/mori-routed-check.py:637-644`), so a
  ledger mixing waves can mark a refused wave as started.
- Impacted axes: calibration (premature saturation: absence of evidence counted as compliance).

### F6 (medium, integration hazard) — the last-changed rule is fragile under history rewrite

- K2a: a content-free rebase resets committer dates and turns R4 red. The lane uses jj (`.jj` present) and
  its history already shows rewritten commits (`29c1bf4`: author 2026-10-21T18:06:54, committer
  2026-10-22T05:10:55; `df4db54`, `a730ecf`, `753d227` also differ by 1–9 seconds). A rewrite cannot make a
  red row green without backdating, so this is a false-red risk, not a false-green one.
- The after-value is also tip-sensitive within a wave: `753d227` (spec bound, call made, ledger not yet
  committed) is red. `held 4` at `a730ecf` predates wave 2 and is not the landed-tip value.
- Impacted axes: calibration and operability (a non-author integration step can flip the declared value).

### F7 (low, guards) — R1 and R2 guard narrower than their QUALITY text implies

- R1 (run, K6): a quota mechanism added under a path without `quota`, or a SKILL capability row, passes.
  QUALITY 72's "the quota capability stays absent" is wider than the predicate.
- R2 (static, unrun): the regex requires the underscore spelling and the literal `true`; hyphen, space or
  camelCase spellings and other truthy values are not matched, and A1 deliberately excludes `.ufo/**` and
  `tools/**`. The pinned receipts and pinned retention tools are the strong part of R2.
- R3: the whole round-23 tree pin is strong; item 3's prose clause ("the final forensic archive is not
  retroactively claimed scanned") has no predicate. Static, unrun.
- Impacted axes: calibration (guards; no repair weight is lost, but the criterion text overclaims).

## What a non-author closure should accept

1. R4 red on the real round-23 defect (`--rev c725aa37 --round 23`: eight rows 47–68 minutes before
   `22772c1`) and green on both round-24 waves at `13208d2`, with K1a showing an honest late commit is caught.
   That is a measured repair of the binding clause under honest recording.
2. `held 4/4` at the **final landed tip**, re-run by the closure with the checker blob `3337232b…` and with
   `tools/mori-dispatch-ledger.py` still equal to `b86525c6…`, and only if no rewrite reset the bind
   commits' committer dates (if one did, R4 red is an integration artifact; measure the pre-rewrite tip).
3. R1–R3 as regression guards that held, with no repair weight.

## What it should not accept

1. "Repair of item 4" or "repair of the four routed items" as worded (F1, F2, `SCORECARD.md:1501`). The
   honest statement is: binding clause of item 4 repaired as recorded ordering; worktree and
   accurate-reporting clauses unchecked; R1–R3 guards.
2. R4 as harness-observed, tamper-evident ordering (K1b, K1c, K4b) or as proof that every dispatch was
   recorded (K3, K5).
3. `held 4` at `a730ecf` as the after-value; it predates the wave-2 ledger.
4. QUALITY 72's "capability stays absent" as checked beyond path names (K6).

## Smallest safe corrections (new declarations or disclosures, not retroactive target changes)

- Text only, now: in QUALITY 75 and the lesson, state that R4 covers the binding clause only and list the
  worktree and accurate-reporting clauses as unchecked why-nots; align the SCORECARD declaration row with A4/A5
  or mark it superseded.
- Pin the ledger verifier to blob `b86525c6…` (or base) instead of REV. Holds at `13208d2` unchanged.
- Bound `at` above by the committer time of the commit that first added the row. Holds at `13208d2`
  (05:14:13.93 ≤ `4059ffb` 05:14:40; 05:56:44.92 ≤ `13208d2` 05:56:58). Closes K1c, not K1b.
- Require every `round-N/w*/swarm-registry.json` to pair with a spec and a started ledger of the same `wave`.
  Holds at `13208d2` (registries `mori-r24-w1`, `mori-r24-w2` equal the spec `wave` values). Closes K3.
- Decide `started` from the last row carrying that wave, or reject ledgers with more than one `wave` value. Closes K5.
- K1b (forged committer date) cannot be closed inside the lane; it needs a harness-written call time. That
  is a tradeoff the judge must accept as the stated limit, not a defect the lane can repair.

## Tooling

No installs or upgrades. Used pre-existing git 2.56.0, Python 3.14.8 and `/usr/bin/sqlite3`
(one read-only `.tables` query on `~/.omp/agent/agent.db`). No lane git index, jj state, host, `/proc`,
`/sys` or cgroup writes. This report is the only file written in the lane repo.
