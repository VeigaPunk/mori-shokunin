# Round 43 contract — frozen before any seat scores and before the lane after-score

Entering tip: `e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2` (round-42 verifier
spot-check; ancestor of the rejected closure tip `25200325`). Frozen r42
counter `.ufo/waves/round-42/count-c1.py` sha256
`105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6`
is not amended. Its `run()` takes `argv, timeout` and not `cwd`.

Lowest non-retired axes are tied at 5 (depth, freshness, calibration).
Calibration is the lowest-axis claim because the routed defects are
self-assessment mismatches. Operability is the successor measurement.
No third claim. No score move is pre-awarded. No retirement, waiver, or
exploratory claim.

## P-C1S (operability) — one sentence

`C1S=met` if and only if `python3 .ufo/waves/round-43/count-c1s.py <rev>`
exits 0 and its last line is `C1S=met`, which that counter prints only when
every check passes on bytes at `<rev>`: the running counter is byte-identical
to `<rev>:.ufo/waves/round-43/count-c1s.py`; the frozen r42 counter at `<rev>`
matches the sha above and its `run` parameters are exactly `argv, timeout`;
a re-execution of that frozen counter exits non-zero, stderr contains
`TypeError: run() got an unexpected keyword argument 'cwd'`, and stdout has
no `^C1=` line; the successor `run()` accepts `cwd` and a sandbox-clone
invocation of `tools/mori-sources-appendonly.py --selftest` records rc 0 and
`MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`; the r42 v5 checker
selftest is `pass=17 fail=0` rc 0 and each committed mutant
(`conform-mut-walrus-branch.py`, `conform-mut-tuple-extract.py`,
`conform-mut-sort-deletion.py`) prints `pass=16 fail=1` rc 1 failing exactly
its own arm.

A rev that lacks this counter, or whose copy is not byte-identical to the
running file, prints `C1S=unmet` and does not run the later checks. That is
the do-nothing result on the entering tip. A planted file that prints
`C1S=met` without those bytes is `C1S=unmet`.

## P-C2 (calibration) — one sentence

`C2=met` if and only if `python3 .ufo/waves/round-43/count-c2.py <rev>`
exits 0 and its last line is `C2=met mismatches=0`, which that counter prints
only when every check passes on bytes at `<rev>`: the S235 registry row is
byte-identical to sha256
`971df55e9e1ed8826e66dd31d12f9cbb5b2c727cf71201a2c0eabc7311e169a2`
(the entering-tip row, which still contains `a30cda99` and `byte-identical`);
some other registry row contains both `corrects S235` and `a30dca99` and does
not contain `a30cda99`; SCORECARD.md contains the exact line
`Round-43 calibration correction: r42-declaration-C1=met superseded; frozen counter printed no C1= line`
and still contains the unrewritten declaration fragment
`` `C1=met` exit 0 (`evidence/c1-after.txt`) ``;
sha256 of `corpus/evidence/sources-r42/S235.pdf` is
`9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`.

The entering tip fails the correction-row check and the SCORECARD-line check.
A row that still carries `a30cda99`, or an in-place rewrite of the S235 row,
is `C2=unmet`.

## Controls, before the lane after-score

- Do-nothing C1S: the counter against the entering tip prints `C1S=unmet`.
- Do-nothing C1S junk: a scratch rev whose `count-c1s.py` only prints
  `C1S=met` is scored `C1S=unmet` by this counter.
- Green C1S: a scratch clone of the entering tip with this counter committed
  byte-identical, scored with `--repo` pointing at that clone, prints
  `C1S=met`. If it does not, the counter is wrong and is fixed before any
  seat scores and before the lane after-score.
- Do-nothing C2: the counter against the entering tip prints `C2=unmet`.
- Green C2: a scratch repo carrying the unrewritten S235 row, a correction
  row, the SCORECARD line, the unrewritten declaration fragment, and the PDF,
  prints `C2=met`.

## Sourced claim

C1S rests on a SOURCES row opened this round for
`subprocess.run` (`cwd=None` in the documented signature). The row is not
part of the frozen predicate; landing it does not by itself print `C1S=met`.

## Not this round's claims

S268 stays refused unless a fetch this host can reproduce is committed
before any admit. The OpenAlex L0 `527fc8dd` is not re-filed. No host
service is mutated. Assimilation is frontier work inside the claim cap,
not a third claim.
