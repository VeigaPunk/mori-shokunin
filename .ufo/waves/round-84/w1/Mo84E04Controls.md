# Mo84E04Controls — round 84 w1: independent control and no-harm receipt

Seat: Mo84E04Controls (leaf; no subagents used, no labrat needed — the assignment is read-only
re-execution). Milestone: round 84 w1: independent control and no-harm receipt.
Judged axes: operability, depth.

## Produced

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-84/evidence/controls-verify-r84.txt`
  — the independent receipt: all nine required commands with verbatim output and rc, the
  deviations section, and supplementary evidence (counter selftests + pre-A2 freeze-bytes run).

No counter, tool or record was edited. No commit, no scratch left behind (scratch dir
`/fast/scratch/hyaku/mori-r84/Mo84E04Controls/` removed at yield). No tools installed or
upgraded (none needed; python 3.14.8 already present).

## What I ran (all from `/home/vgpnk/Projects/shokunin/mori-shokunin`; full verbatim output in the receipt)

Round-84 counters at the freeze commit `daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4`:

| command | verdict line (verbatim) | rc | expected | deviation |
|---|---|---|---|---|
| `python3 -I .ufo/waves/round-84/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` | `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green detector=green rev=daa77bd5684c` (+4 MUTANT lines: M24a/M24b survived, M24c/M24d equivalent) | 1 | `C1=unmet mutants=4 killed=0 equivalent=2 survivors=2 ...` rc 1 | none |
| `python3 -I .ufo/waves/round-84/count-c2.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` | `C2=unmet arm=absent rev=daa77bd5684c` | 1 | `C2=unmet arm=absent` rc 1 | none |
| `python3 -I .ufo/waves/round-84/count-c3.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` | `C3=unmet delta=absent rev=daa77bd5684c` | 1 | `C3=unmet delta=absent` rc 1 | none |

No-harm battery — round-83 counters at the same freeze commit (recorded exactly, no expectation
imposed by the seat):

| command | verdict line (verbatim) | rc | reading |
|---|---|---|---|
| `python3 -I .ufo/waves/round-83/count-c1.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` | `C1=met mutants=23 killed=22 equivalent=1 survivors=0 total=23 pristine=green detector=green rev=daa77bd5684c` (+23 MUTANT lines) | 0 | met — no harm (27.89s) |
| `python3 -I .ufo/waves/round-83/count-c2.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` | `C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived live_tokens=64 live_agree=64 rev=daa77bd5684c` | 0 | met — no harm (5.00s) |
| `python3 -I .ufo/waves/round-83/count-c3.py daa77bd5684c8db75eec1e80c87ee4fa5c3a6bb4` | `C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40 rev=daa77bd5684c` | 0 | met — no harm |

Round-84 counters at the entering revision `5adf4337b6510dd246b247092c11cbaa97c930d3`:

| command | verdict line (verbatim) | rc | expected | deviation |
|---|---|---|---|---|
| `python3 -I .ufo/waves/round-84/count-c1.py 5adf4337b6510dd246b247092c11cbaa97c930d3` | `C1=unmet harness=absent rev=5adf4337b651` | 1 | unmet/absent rc 1 | none |
| `python3 -I .ufo/waves/round-84/count-c2.py 5adf4337b6510dd246b247092c11cbaa97c930d3` | `C2=unmet arm=absent rev=5adf4337b651` | 1 | unmet/absent rc 1 | none |
| `python3 -I .ufo/waves/round-84/count-c3.py 5adf4337b6510dd246b247092c11cbaa97c930d3` | `C3=unmet delta=absent rev=5adf4337b651` | 1 | unmet/absent rc 1 | none |

The three entering-revision verdict lines are byte-identical to the frozen do-nothing controls in
`.ufo/waves/round-84/evidence/controls-r84.txt`.

## Verified

1. **Frozen controls reproduce.** All three round-84 counters at the freeze commit print exactly
   the frozen population/entering-control lines with rc 1; the C1 population control matches the
   contract verbatim (`mutants=4 killed=0 equivalent=2 survivors=2 total=4 pristine=green
   detector=green`).
2. **Do-nothing controls reproduce.** All three entering-revision runs print `unmet ... absent`
   rc 1, byte-identical to `controls-r84.txt`.
3. **No harm.** All three round-83 counters still grade the freeze commit `met` rc 0 — the r84
   wave's freeze/spec/dispatch commits and in-flight sibling writes did not disturb the r83
   verdicts.
4. **Counter selftests (supplementary).** `count-c1.py --selftest` → `C1_COUNTER_SELFTEST
   pass=11 fail=0` rc 0; `count-c2.py --selftest` → `C2_COUNTER_SELFTEST pass=9 fail=0` rc 0;
   `count-c3.py --selftest` → `C3_COUNTER_SELFTEST pass=9 fail=0` rc 0.

## Context finding (pre-data amendment A2, not a seat defect)

While this seat was reading the tree, the lane HEAD moved from `dbdb1aaa` (A1) to `39190f8a`
("round-84: pre-data amendment A2 (M24b/M24c/M24d anchors corrected; population control now
mutants=4 survivors=2)"). Consequences, both recorded in the receipt:

- The executing `count-c1.py` bytes are blob `a5db2cc` (A2), not the freeze blob `b0b8bbf`;
  `count-c2.py`/`count-c3.py` are byte-identical between worktree and freeze.
- Supplementary run of the pre-A2 freeze bytes at the freeze commit shows why A2 was needed:
  the original anchors mis-anchored M24b (occurrences=2), M24c (0) and M24d (0), printing
  `C1=unmet mutants=1 killed=0 equivalent=0 survivors=1 total=1 ...` rc 1 instead of the
  contract's stated `mutants=4 killed=0 equivalent=2 survivors=2`. The A2 bytes reproduce the
  frozen population control exactly (section 1 of the receipt).

This is the L1's own pre-data amendment chain (A1, A2), committed before any after-value exists;
it is not a deviation of the required battery and not another seat's defect.

## Could not verify

- Nothing in the assigned scope was left unrun. Outside this seat's scope by design: the
  after-revision grading (integration tip does not exist yet at measurement time) and the r83
  counters' behavior at revisions other than the freeze commit.
- Stream separation: the invoking shell captured stdout/stderr combined; per the counters'
  source all verdict lines in sections 1–3 are stdout and no stderr output occurred (the only
  stderr emissions observed were the deliberate no-argument usage probe, rc 2).

## Defects in other seats' bytes

None found. No counter, record, or sibling file was modified by this seat (worktree counter
paths were clean before and after; `git status --porcelain` on the three r84 counter paths
showed 0 lines at close).
