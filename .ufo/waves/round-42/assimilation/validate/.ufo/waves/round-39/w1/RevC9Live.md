# RevC9Live — gate parity at 13bfba2 and e37dcc6 vs round-38 receipts

Verdict: **PASS** on both acceptance items. No non-header difference in either diff; the
S069 stale verdict sits at line 22 of `gate-after-e37dcc6.txt` as claimed.

## Method

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; scratch under
`.ufo/waves/round-39/scratch/RevC9Live/`). Executed gate blob is
`d2c9616090048dd60357f2550baea6d8a9ae13da` — identical at `13bfba2`, at `HEAD` (`5561819`)
and in the worktree (`git rev-parse <rev>:tools/mori-sources-appendonly.py` and
`git hash-object`), so both runs exercise the round-39 gate. The round-38 receipts were
produced by blob `c2c86f4d3ca1c6f9b6d46462fb6481dab543b967`; the diff is therefore
cross-version (v2 gate vs v1 bytes), which is the C9 claim itself.

Commands run (each redirected to scratch; `EXIT=$?` appended):

```
python3 tools/mori-sources-appendonly.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --round-base f10a320d
python3 tools/mori-sources-appendonly.py e37dcc6 --round-base f10a320d
```

Both exit `1` (violation present, matching the round-38 receipts' `EXIT=1`), both emit 23
lines: 1 `command:` line, 1 predicate line, 18 `changed …` lines, 1 summary line, 1
`supersede_timing` line, 1 `EXIT=` line.

## Diff results

| Comparison | Non-header lines | Difference |
|---|---|---|
| fresh `13bfba2` vs `round-38/evidence/gate-after.txt` | lines 3–22, md5 `5ef25ac61ea720f0f8925002d908cfd8` both | **none** |
| fresh `e37dcc6` vs `round-38/evidence/gate-after-e37dcc6.txt` | lines 3–22, md5 `68981e11dad0a7cb4aee25a92d91c7ad` both | **none** |

Full-file `diff`, limited output:

- `13bfba2` vs `gate-after.txt` — only lines 1–2 change: `command:` revision
  (`b699374…` → `13bfba23…`) and the predicate line (`P-C6:` → `P-C9:` text). Both are
  header lines excluded by the assignment.
- `e37dcc6` vs `gate-after-e37dcc6.txt` — only line 2 changes (`P-C6:` → `P-C9:`). The
  `command:` line is already identical (`e37dcc6 --round-base f10a320d`).

Both diffs are line-index stable (23 vs 23 lines), so the body comparison is not an
artifact of misaligned headers.

Revision scoping is real, not vacuous: the fresh `e37dcc6` run prints
`changed S069 superseded_by=S073` while the `13bfba2` run prints
`changed S069 superseded_by=S226`; the gate reads via `git show <rev>:<path>`
(`tools/mori-sources-appendonly.py:136,138`) and derives supersession from the `teaches`
cell (`SUPERSEDES_RE`, line 69; `superseders()`, line 229).

Why the tip body equals the r38 tip body despite round-39 adding S227/S228: only the 18
frozen ids are displayed, S069's direct superseder is still S226 (the `S228` row's
`teaches` cell opens `supersedes S226`), and S226 is one level above the frozen set.
Observed tip summary: `round_changed=[S182,S193]`,
`supersede_timing superseded_as_of=[18 ids] stale_supersede=[]`; observed `e37dcc6`:
`superseded_as_of=[17 ids] stale_supersede=[S069]`. Both reproduce the receipts exactly.

## Line-22 check

`round-38/evidence/gate-after-e37dcc6.txt` is 23 lines; absolute line 22 is:

```
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
```

The fresh `e37dcc6` run reproduces this line character-for-character at line 22 (covered by
the lines 3–22 md5 equality above). S069 is the sole `stale_supersede` entry and is absent
from `superseded_as_of`. Line 23 is `EXIT=1`.

Ambiguity check: S069 also appears at line 11 (`changed S069 superseded_by=S073`) and twice
inside line 21 (`ids=[…]`, `superseded=[…]`). The *timing verdict* value — the thing C9
predicates — is uniquely on line 22, which is what the assignment asserts. Correct line
number.

## Secondary observations (not part of this seat's acceptance)

- `contract.md:146` declares `MORI_SOURCES_APPENDONLY_SELFTEST pass=11 fail=0` as the
  "After (declared)" state; `evidence/gate-selftest-after.txt` states `pass=12 fail=0`, and I
  reproduced it independently in an isolated TMPDIR:
  `TMPDIR=$PWD/.ufo/waves/round-39/scratch/RevC9Live/tmp python3 tools/mori-sources-appendonly.py --selftest`
  → `MORI_SOURCES_APPENDONLY_SELFTEST pass=12 fail=0`, exit 0. `git status --porcelain`
  count was 3 before and 3 after, so the selftest did not mutate the lane. The contract's
  declared count is therefore the wrong number; reported independently by peer
  `CritC9Semantics`. The gate's own predicate line does not pin a count, so this does not
  affect the two items above.
- `contract.md:148` declares `superseded_as_of=[18 ids + S226 once S228 lands]`; the landed
  tip prints 18 ids and no S226. Direct-edge semantics (S228 supersedes S226, not S069;
  S226 is outside the frozen violation set) explains the observed 18. Peer
  `CritC9Semantics` has agreed not to elevate this as a gate defect; I did not verify the
  first-parent/linear-readd claims on their fixtures, which are outside this assignment.

## Residual risk

- The `13bfba2` comparison is against a receipt produced at `b699374` (r38 tip), not at
  `13bfba2`. The assignment names that file as the round-38 receipt, and body equality
  holds; but the diff does not prove that the r39 gate emits the same bytes at `b699374`
  itself. The r39 lane receipt `evidence/c9-after-lane.txt` asserts the diff was identical
  at `f920eaf7`; my independent run at the scored tip `13bfba2` agrees.
- `gate-after.txt`'s predicate text (P-C6) is not equivalent to the executed predicate
  (P-C9): the latter adds `git merge-base --is-ancestor`, first-parent edit semantics, and
  `--full-history`. Ignoring the predicate line is required by the assignment, but it means
  the parity demonstrates verdict stability only for the 18 frozen ids on two revisions,
  not equivalence of the two implementations.

## Verification gaps

- No `lsp` server applies: the artifacts under test are textual gate receipts and a
  standalone Python script run end-to-end; results are the executed output, not semantic
  index reads.
- The peer-reported mutation evidence (linear readd flips exit/timing, first-parent state
  violation) was not re-run here; it is cited as peer-reported only.
- No tool installs or upgrades were needed (no pacman transaction, per host pause).
