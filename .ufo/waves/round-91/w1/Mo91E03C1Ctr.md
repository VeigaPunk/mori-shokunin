# Mo91E03C1Ctr — C1 counter (calibration)

Seat: Mo91E03C1Ctr. Lane: mori-shokunin @ entering 79eaa8cf (contract frozen at e02b8a39).

## Deliverable

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/count-c1.py`
sha256 `cc599626bb09851bf07eed82886aa725a3fe5815483e3d5ba255b5e12ebce1f9` (473 lines,
`python3 -I`, stdlib only).

Implements frozen P-C1 exactly:

- Subject `.ufo/waves/round-87/count-c2.py` read via `git show <rev>:<path>` only.
- `--p1`/`--p2` default to `<clone>/.ufo/waves/round-91/mutants-c1.json` and
  `mutants-c1-independent.json` from the working tree; absent P1 = zero mutants, absent P2 =
  exit 2.
- Per mutant: `anchor_old` must occur exactly once (else `unanchored`); `anchor_new`
  producing identical bytes reads `empty`; the mutated copy runs `python3 <copy> --selftest`
  with a 120 s timeout (timeout -> rc 124 -> red, no FAIL labels -> `unattributed`).
- Frozen kill rule: `killed` iff red (rc!=0 or fail>0) AND nonempty FAIL-label set AND every
  FAIL label `startswith(family)`; any outside label -> `isolated`; red with no FAIL label
  -> `unattributed`; green -> `survived`; red/absent pristine -> every mutant `pristine`.
- `pins` = last `COUNTER_SELFTEST pass=N` tally of the pristine subject (prints `?` when no
  tally). `unarmed` = count of the four named families with no P1 mutant.
- Summary line matches the frozen format byte-for-byte; `C1=met` only when unarmed=0, all
  survivors/unattributed/isolated/unanchored are 0, both populations have >=1 kill, pins>0.
- Exit 0 met / 1 unmet / 2 setup (bad rev, missing repo, unreadable population, red own
  selftest).
- `--selftest`: 14 arms (kill_attributed, canary_unattributed, canary_isolated,
  empty_replacement, red_pristine, correct_fixture, unanchored_both, survivor_green,
  classify_boundary, unarmed_count, loader_absent, loader_bad_json, marker_literal,
  own_arms_pinned). Prints `C1_COUNTER_SELFTEST pass=14 fail=0`.

## Selftest output (exit 0)

```
PASS kill_attributed MUTANT p1 m-kill c2-absent killed rc=1 labels=c2-absent
PASS canary_unattributed MUTANT p1 m-canary-unattr c2-absent unattributed rc=1 labels=-
PASS canary_isolated MUTANT p1 m-canary-isolated c2-absent isolated rc=1 labels=unrelated-clause
PASS empty_replacement MUTANT p1 m-e c2-absent empty rc=-1 labels=-
PASS red_pristine pristine pristine
PASS correct_fixture killed=1 survivors=1 pins=2
PASS unanchored_both 2 unanchored
PASS survivor_green MUTANT p1 m-surv c2-absent survived rc=0 labels=-
PASS classify_boundary killed/isolated/unattributed/survived
PASS unarmed_count 4/3/0
PASS loader_absent None
PASS loader_bad_json ValueError
PASS marker_literal label
PASS own_arms_pinned 14/14
C1_COUNTER_SELFTEST pass=14 fail=0
```

## Fixture run (scratch repo, 79eaa8cf subject bytes, pre-arm state)

Fixture `D=$S/fixture-ti0c` (git init, toplevel verified, subject committed at
`979c3c614df0d70772d73fe4e54e552264452639`), synthetic P1 with one mutant per family plus a
2-mutant P2:

```
MUTANT p1 p1-c2-replay-compare-off c2-replay-compare-off survived rc=0 labels=-
MUTANT p1 p1-c2-supersede c2-supersede isolated rc=1 labels=supersede_absent_target,supersede_requires_clean
MUTANT p1 p1-c2-absent c2-absent survived rc=0 labels=-
MUTANT p1 p1-c2-defeated-accounting c2-defeated-accounting survived rc=0 labels=-
MUTANT p2 p2-c2-absent c2-absent survived rc=0 labels=-
C1=unmet families=4 unarmed=0 p1_killed=0 p1_survivors=3 p2_killed=0 p2_survivors=1 unattributed=0 isolated=1 pins=26 rev=979c3c614df0
EXIT=1
```

As expected at the pre-arm state: clause mutants survive (no arms exist yet) and one reads
`isolated` because the existing `supersede_*` FAIL labels do not begin with the family
prefix — the frozen rule working as written. `pins=26` is the subject's real arm count at
79eaa8cf (selftest prints `C2_COUNTER_SELFTEST pass=26 fail=0`).

P1-absent variant on the same fixture (`--p1` pointed at a missing file):

```
MUTANT p2 p2-c2-absent c2-absent survived rc=0 labels=-
C1=unmet families=4 unarmed=4 p1_killed=0 p1_survivors=0 p2_killed=0 p2_survivors=1 unattributed=0 isolated=0 pins=26 rev=979c3c614df0
EXIT=1
```

## Do-nothing run (79eaa8cf, P1 absent, P2 supplied from scratch)

The frozen P2 file `.ufo/waves/round-91/mutants-c1-independent.json` is NOT yet committed
(Mo91M01Mut still in flight; contract ordering step 1 pending). I supplied a scratch P2 of
two mutants against the 79eaa8cf subject clause code (`$S/mutants-c1-independent.json`):

```
$ python3 -I count-c1.py 79eaa8cf --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --p2 $S/mutants-c1-independent.json --scratch $S
MUTANT p2 dn-p2-0 c2-absent survived rc=0 labels=-
MUTANT p2 dn-p2-1 c2-supersede isolated rc=1 labels=supersede_absent_target,supersede_requires_clean
C1=unmet families=4 unarmed=4 p1_killed=0 p1_survivors=0 p2_killed=0 p2_survivors=1 unattributed=0 isolated=1 pins=26 rev=79eaa8cfe5e0
EXIT=1
```

`C1=unmet families=4 unarmed=4` exit 1 as the contract requires. NOTE for L1: with the real
committed P2 the `isolated`/`survived` split may differ; the unmet verdict and unarmed=4 are
structural (no P1 file at 79eaa8cf).

## Setup-error checks (all exit 2)

- absent P2 file -> `C1_SETUP p2 population absent: <path>` exit 2
- unresolvable rev -> `C1_SETUP unresolvable revision deadbeef` exit 2
- missing args -> usage on stderr, exit 2

## Files written

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-91/w1/candidates/count-c1.py`
  sha256 cc599626bb09851bf07eed82886aa725a3fe5815483e3d5ba255b5e12ebce1f9
- this report `.ufo/waves/round-91/w1/Mo91E03C1Ctr.md`

Scratch `/fast/scratch/hyaku/mori-r91/Mo91E03C1Ctr/` deleted before yield (fixture repos,
synthetic P2, captured outputs were all under it; evidence pasted above).

## Limits / open defects

- The frozen P2 population was not yet committed at run time; the do-nothing run used a
  scratch P2 (documented above). Re-run with the committed file once Mo91M01Mut lands.
- `pins` is read as the LAST `COUNTER_SELFTEST pass=N` tally in the subject's selftest
  output; the subject prints exactly one tally line, so this is unambiguous at 79eaa8cf.
- `empty` (anchor_new == anchor_old after replacement) is bucketed under the `unanchored`
  counter in the summary (contract has no `empty` field; an empty mutation can never be a
  kill, so unmet either way).
- No tools installed; no pacman used.
