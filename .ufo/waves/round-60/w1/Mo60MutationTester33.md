# Mo60MutationTester33 — count-c1.py mutation probes (round 60, w1)

Role: mutation tester (single assignment, leaf seat, no dispatch). Detection only.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No production/corpus/SCORECARD/LOG edits,
no lane VCS writes, no fleet or sibling-repo writes. Scratch root
`/fast/scratch/hyaku/mori-r60/Mo60MutationTester33` was created explicitly and removed after
this report was written (`du -sh` 496M → `test -d` → `REMOVED`).

## Pinned object under test

| item | value |
|---|---|
| frozen contract | `.ufo/waves/round-60/contract.md` (freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`, entering `ddfb12fb0838b4307c445194a844f0c4b1950195`) |
| counter under test | `.ufo/waves/round-60/count-c1.py` |
| counter sha256 | `795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae` |
| sha at freeze `ac496c7c` | `795c1f31…ddbae` (identical) |
| sha at entering `ddfb12fb` | absent (blob sha `e3b0c442…b855`, i.e. `git show` returned nothing) |
| sha in lane working tree, before and after probes | `795c1f31…ddbae` (identical) |
| data revision R used for every target run | `b3c256138f00c704d5aa56eb0332d74506502ef2` (lane tip when the sandbox clone was cut; C1 data landed in `398d3225`) |

All repo reads were `git show` / `cat-file` / `rev-parse` / `status` only. Every mutated counter ran
from a scratch copy against a scratch **bare clone** of the lane (`git clone --bare --no-hardlinks`),
never against the lane. The counter itself is read-only (`git show`/`cat-file`); its receipt arm
re-executes the *revision-pinned* r59 counters, which are likewise `git show`/`ls-tree`/`cat-file`
only (checked in the r59 blobs before running).

## Baseline on pristine bytes (bounded detector, two modes)

```
$ python3 pristine/count-c1.py --selftest
C1_SELFTEST pass=6 fail=0                          # exit 0
$ python3 pristine/count-c1.py b3c25613… --repo <clone> --scratch <scratch>/run-base
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…   # exit 0
```

Baseline is green, so a met→unmet flip is attributable to the mutation.

## Probe results

| # | mutation (assigned) | mutated bytes | selftest | target at R | verdict |
|---|---|---|---|---|---|
| M1 | ignore the `r60-correction:` marker filter (skip no line) | `count-c1.py:81-82`: `if CORRECTION_MARKER in ln:` → `if False:` | `FAIL dead_corrected`; `C1_SELFTEST pass=5 fail=1`, exit 1 | `C1=unmet dead-uncorrected=2 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613… failed=dead=2`, exit 1 | **killed** (both detectors) |
| M2 | skip one receipt byte-compare (receipt idx 0 = `r59-c1-met.txt`) | `count-c1.py:138`: `if p.stdout != receipt_bytes:` → `if idx != 0 and p.stdout != receipt_bytes:` | `C1_SELFTEST pass=6 fail=0`, exit 0 | `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…`, exit 0 (byte-identical to baseline) | **survived** → coverage finding (below) |
| M3 | accept any 5-cell row (drop cell validation) | `count-c1.py:110-117` validation block deleted, `rows[cells[0]] = …` kept | `FAIL table_shape`; `C1_SELFTEST pass=5 fail=1`, exit 1 | `C1=met …` identical to baseline, exit 0 | **killed** by selftest (target blind, see note) |
| M4 | drop the lesson greps (existence only) | `count-c1.py:216-231` → `if lb is not None: lesson = "ok"` | `C1_SELFTEST pass=6 fail=0`, exit 0 | `C1=met …` identical to baseline, exit 0 | **survived** → coverage finding (below) |

Mutant shas: M1 `1df85c44febcf79535713cc3a64dda588e61aa36c44ce0d8ad8ddee3b903ac5b`,
M2 `1c14ea5acf048f930e06ea26846ac7a7bf523ef5e860f79e4c285229cd0104f9`,
M3 `fb38365be4e7b5a32034bed6828606aedfceb7ee61d1639950c4d943ef9e9867`,
M4 `70e30e09e9e2da8dc2db066c0e52f767fa3c95446779310fc426698075d13518`.
Line pointers are into the frozen `795c1f31` blob.

### M1 — flipped, as intended

Removing the marker exemption makes the two corrected SCORECARD lines count as dead; the frozen
predicate's `dead-uncorrected=0` term is exactly what the selftest case `dead_corrected` and the
real target both detect. Killed twice over.

### M3 — killed by selftest only

`parse_absent_table` returning a dict instead of `None` for a malformed table is caught by the
`table_shape` case (invalid disposition `wrong-supersedED`). At target level the mutant is not
verdict-bearing: a row with junk cells still fails the per-cell `present`/`absent` and
disposition comparisons in `measure()` (`absent_row:<name>` instead of `absent_table_shape`), so
the only target-level difference is the reason token, not met/unmet. No false-met path found
through the row-shape branch.

### M2 — survived; non-equivalent (predicate-breaking)

Shipped detectors cannot see it because the committed receipts genuinely byte-equal their re-runs.
Non-equivalence proved on a scratch fixture repo `D1.git` = clone of R whose tree is R's tree with
**only** `.ufo/waves/round-60/evidence/r59-c1-met.txt` replaced (blob
`75ff322c9925f9b0ba583d4821d3546b1e6df10e609bed3aa5063553bbc5c9a9`; `git diff --name-only HEAD^ HEAD`
lists that one path). Fixture commit `c89e60b9305eb5c50ce66807461d0e62ad04bcc5`:

```
pristine: C1=unmet dead-uncorrected=0 receipts=1/2 absent-set=5/5 lesson=ok rev=c89e60b9… failed=receipt:bytes_differ,receipts=1/2   exit 1
M2      : C1=met   dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=c89e60b9…                                            exit 0
```

The mutant converts a tampered receipt into `met`, and no selftest case exercises
`rerun_receipt` at all (selftest covers only `dead_*`, `corrected_*`, `table_*`).

### M4 — survived; non-equivalent (predicate-breaking)

Fixture `D2.git` = clone of R whose tree is R's tree with **only** `corpus/lessons/round-60.md`
replaced (blob `531a9e1d8025fad4e2041bd0f4d5f89248f3118ad4cbdc4305c21b28724b2c4b`, in which both
`supersedes round-59` literals read `supersedes round-58`). Fixture commit
`62258fbe6bfd1524e774d773219ba9dff410d930`:

```
pristine: C1=unmet dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=bad  rev=62258fbe… failed=lesson:no_supersedes   exit 1
M4      : C1=met   dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok   rev=62258fbe…                              exit 0
```

The mutant converts a lesson missing the frozen literal into `met`; the selftest has no lesson
case (teacher arm absent from `selftest()`), so only adversarial data distinguishes it.

## Coverage finding (not a contract change)

`count-c1.py --selftest` (`pass=6`) covers the dead-name arm (2 cases), the corrected-pointer arm
(2 cases) and the absent-table shape (2 cases). It has **zero** cases for (a) the receipts arm —
`rerun_receipt`'s exit-code and byte-equality tests — and (b) the lesson arm — the
`supersedes round-59` literal, the per-name `supersedes` requirement and the `f091bd77` landing
pointer. M2 and M4 therefore survive every shipped detector on shipped data while each flips the
frozen predicate on adversarial data (`met` reported for a tampered receipt / a lesson lacking the
marker). Mitigation that does exist, for the L1 to weigh: count-c3 pins count-c1
(`795c1f31…ddbae`), so an altered instrument is rejected at the C3 toolgate — that protects
instrument bytes, not predicate coverage of a counter admitted with a weakened arm. Suggest (proposal
only, post-freeze) two selftest cases: a `rerun_receipt` byte-mismatch case and a lesson-missing-
marker case, each asserting non-met.

## Restoration / bounds evidence

- Original bytes never touched: lane working-tree counter sha `795c1f31…ddbae` before and after all
  probes, equal to the freeze blob and to the clone's `R:.ufo/waves/round-60/count-c1.py`.
- "Restored bytes" re-run after all four probes: `C1_SELFTEST pass=6 fail=0` exit 0 and
  `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c25613…` exit 0 —
  identical to baseline.
- Git writes (clone, `read-tree`/`update-index`/`commit-tree`/`update-ref` in fixtures) happened
  only under the scratch root; each fixture asserted `rev-parse --is-bare-repository` →
  `true`/toplevel it owned before any commit. Lane tip unchanged at `b3c25613`; lane
  `git status --porcelain` shows only the orchestrator's/siblings' untracked entries
  (`evidence/c1-at-data.txt`, `w1.ready`, `w1.ready.dispatched`, `w1/`).
- Disk guard before and after heavy work: `ok` on `/tmp` 14%, `/var/tmp` 38%,
  `/fast/scratch/hyaku` 26→27%; exit 0. No pacman, no tool installs.

## Observation (not my artifact, no action taken)

At 13:16:28 the lane root contained an untracked `EXEC-MARKER` (92 B) reading
`executed /fast/scratch/hyaku/mori-r60/Mo60Executor58/full-old/real2/round-53/w1-results.json` —
i.e. a sibling seat's G1 marker PoC wrote outside its own scratch, into the lane working tree. My
probes ran only the frozen counter and its revision-pinned r59 counters, none of which executes a
repo-supplied tool blob, and the marker names another seat's path. I did not create, modify or
delete it; by my final check it was gone (lane status no longer lists it). Flagging for the L1 as
G1/§9 control hygiene: the marker control should land under `$HYAKU_SCRATCH`, not the lane root.

## Replay (exact)

```
S=/fast/scratch/hyaku/mori-r60/Mo60MutationTester33; mkdir -p $S; export TMPDIR=$S/tmp
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin; R=b3c256138f00c704d5aa56eb0332d74506502ef2
git clone --bare --no-hardlinks "$LANE" $S/lane.git
git -C $S/lane.git show $R:.ufo/waves/round-60/count-c1.py > $S/pristine/count-c1.py   # sha 795c1f31…ddbae
python3 $S/pristine/count-c1.py --selftest
python3 $S/pristine/count-c1.py $R --repo $S/lane.git --scratch $S/run-base
# mutant: edit the one line noted above, then
python3 $S/mN/count-c1.py --selftest
python3 $S/mN/count-c1.py $R --repo $S/lane.git --scratch $S/run-mN
# fixtures: clone --bare, hash-object -w the altered blob, read-tree $R, update-index --cacheinfo,
# write-tree, commit-tree -p $R, update-ref HEAD <new>
```
