# Mo50bCritSeparability — causal separability of C1 and C2 at `487941b9`

Seat: critic, mori round 50 (attempt 2), wave a2w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Landing under test `487941b9395e89678af0053cc443cdb49cdee6e3` (attempt-2 L1, parent `9b8562a371dc916fdc0fc686619ea1e271a3e118`,
the orchestrator salvage of attempt 1). Freeze commit `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`.
Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bCritSeparability/` (removed after this report was written).

Task: build, in a shared clone, (a) a commit with C2's files reverted to `9b8562a3` and score C1 on it; (b) a commit
with `SCORECARD.md` and `SHONEN.md` reverted to `9b8562a3` and score C2 on it; paste both counter lines; argue whether
either claim could have been met by the other's work.

## 1. Setup and frozen bytes

- Counters run were the lane working-tree copies; sha256 equals the freeze list
  (`evidence/freeze-sha256.txt`, freeze commit `950e99be`), so frozen bytes were measured:
  - `2d5c3ee53198124ef001908cc5abba5c71a6fb63773c31ece211b7c6cdae4456  .ufo/waves/round-50/count-c1.py`
  - `533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d  .ufo/waves/round-50/count-c2.py`
- Disk guard status before the run: `/fast/scratch/hyaku 24% used 612.6G free` (no ENOSPC).
- Clone: `git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin <scratch>/clone`, then
  `git checkout --detach 487941b9`. `git rev-parse --show-toplevel` = `<scratch>/clone` (verified before the first
  fixture commit). Local identity `Mo50bCritSeparability <crit-separability@shokunin.invalid>` set **inside the clone
  only**. No git/jj mutation of the lane, the fleet repo, or any sibling; the fleet repo was only read via
  `git show e0144996:MANIFEST.json` (the counter's default `--fleet-rev`).
- Every counter call passed `--repo <scratch>/clone`; C1 also passed
  `--fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>/c1-*-scratch`. C1's default fleet repo is
  `dirname(repo)`, which is wrong for a scratch clone — the documented option was used, not a workaround.
- Ancestry (read-only `merge-base --is-ancestor`): `950e99be -> 9b8562a3` YES, `9b8562a3 -> 487941b9` YES,
  `487941b9 -> lane HEAD 4548a34d` YES. Lane HEAD is ahead of the scored revision; scoring was at `487941b9` only.

## 2. Fixtures

`487941b9`'s parent **is** `9b8562a3` (`git log -1 --format='%h %p %s' 487941b9` →
`487941b9 parents=9b8562a3 …`). The whole landing delta relative to that parent is:

```
$ git diff --name-status 9b8562a3 487941b9
A	.ufo/waves/round-50/assimilation/a2/append-block.md
A	.ufo/waves/round-50/assimilation/a2/live-sha-L1.txt
A	.ufo/waves/round-50/assimilation/a2/mirror-validate.txt
M	SCORECARD.md
M	SHONEN.md
M	corpus/SOURCES.md
```

| fixture | rev | construction | diff vs `487941b9` |
|---|---|---|---|
| **A** — C2 landing reverted | `f3a2f46842fa40cdba613869d58f76e1bf33487f` | `git checkout 9b8562a3 -- corpus/knowledge/oom-memcg-stat-r50.md corpus/SOURCES.md` on `487941b9` | `corpus/SOURCES.md 3 deletions` only |
| **B** — C1 landing reverted | `6df703bdc9e60a280daf5288751a9a045b06f13b` | `git checkout 9b8562a3 -- SCORECARD.md SHONEN.md` on `487941b9` | `SCORECARD.md 4+/10−, SHONEN.md 1+/1−` |
| **A0** — C2 surface fully absent (supplementary) | `08f8d07523edc03bf5c1a8a0ac79049983c66a21` | `git rm` the entry + the three `corpus/evidence/sources-r50/` copies, `git checkout 9b8562a3 -- corpus/SOURCES.md` | 5 files, 10669 deletions |

Facts that make **A** a smaller intervention than its label suggests (see Findings F2):

- `git show 9b8562a3:corpus/knowledge/oom-memcg-stat-r50.md | sha256sum` and
  `git show 487941b9:corpus/knowledge/oom-memcg-stat-r50.md | sha256sum` both print
  `0fac741cce21d76eda26b9b0a915509e34be499b52041cb7e6c3b1c8cb97c109`. The entry is **byte-identical** at the
  salvage commit and at the landing; `git log -- corpus/knowledge/oom-memcg-stat-r50.md` lists only `9b8562a3`
  (the entry is *absent* at freeze `950e99be`).
- The three source copies are present and pin-clean at `9b8562a3` (they were committed at the freeze `950e99be`;
  C2 at fixture A prints `pins=ok`). Reverting them to `9b8562a3` is likewise a no-op.
- Therefore fixture A's only effective change is removing rows S489–S491 from `corpus/SOURCES.md`. A0 was added to
  remove the entire C2 surface (entry + copies + rows), which is what "C2's work absent" would have to mean if one
  wanted to test C1 against an empty C2 surface.

## 3. Results — every cell of the 2×2 (+ the full-revert and pre-landing states)

| state | `count-c1.py` | `count-c2.py` |
|---|---|---|
| `487941b9` (both halves landed) | **met**, all 8 items `state=ok` | **met** |
| **A** (C2 landing reverted) | **met**, identical item text | **unmet** `bad_rows=22 … source_rows=bad sources_floor` |
| **B** (C1 landing reverted) | **unmet** `mismatches=6` | **met**, identical line | 
| **A0** (C2 surface absent) | **met**, identical item text | **unmet** `entry_absent,pins` |
| `9b8562a3` (neither half landed) | **unmet** `mismatches=6` | **unmet** `bad_rows=22` |

Exact lines (all runs with the frozen counters; exit codes: met → 0, unmet → 1):

**Required line (a) — C1 on the C2-reverted fixture A, `rc=0`:**
```
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=f3a2f46842fa40cdba613869d58f76e1bf33487f
```
Its eight items, all `state=ok` (per-axis `expect=… got=ok`, pins `(114/114)` and `(17/17)` with receipts):
identical, character for character, to the C1 line of the unmodified landing except for `rev=`:
`diff <(sed 's/ rev=.*//' c1-base.txt) <(sed 's/ rev=.*//' c1-a.txt)` → IDENTICAL.

**Required line (b) — C2 on the C1-reverted fixture B, `rc=0`:**
```
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=6df703bdc9e60a280daf5288751a9a045b06f13b
```
Identical to the unmodified-landing C2 line except `rev=`:
`diff <(sed 's/ rev=.*//' c2-base.txt) <(sed 's/ rev=.*//' c2-b.txt)` → IDENTICAL.

Counter-evidence cells:

```
C2=A  : C2=unmet claims=22 located=0 quote_missing=0 bad_rows=22 sources=0 source_rows=bad pins=ok provenance=ok rev=f3a2f46842fa40cdba613869d58f76e1bf33487f failed=bad_rows,source_rows,sources_floor
C2=A0 : C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=08f8d07523edc03bf5c1a8a0ac79049983c66a21 failed=entry_absent,pins
C2=9b : C2=unmet claims=22 located=0 quote_missing=0 bad_rows=22 sources=0 source_rows=bad pins=ok provenance=ok rev=9b8562a371dc916fdc0fc686619ea1e271a3e118 failed=bad_rows,source_rows,sources_floor
C1=B  : C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=6df703bdc9e60a280daf5288751a9a045b06f13b failed=mismatch
C1=9b : C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=9b8562a371dc916fdc0fc686619ea1e271a3e118 failed=mismatch
C1=A0 : C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=08f8d07523edc03bf5c1a8a0ac79049983c66a21
```

C1 on B / on `9b8562a3` (the six mismatches): coverage `round=26,evidence_missing:corpus/lessons/round-47-…`,
operability `round=31,evidence_missing:…round-47-…`, depth `round=31,evidence_missing:…round-49-…`,
calibration `round=25,evidence_missing:…round-49-…`, freshness `ok`, adjacency `ok`,
pins `(60/60)` vs observed `PIN_CHECK_SELFTEST pass=114 fail=0` and `(13/13)` vs `UNLANDED_SELFTEST pass=17 fail=0`.
The B line is character-identical to the `9b8562a3` line except `rev=` (same sed diff), i.e. B is exactly the
C1 do-nothing state.

## 4. Separability argument

Read sets, from the frozen counters (line numbers are the lane working-tree copies):

- `count-c1.py` reads, at R: `SCORECARD.md` (l.211), `SHONEN.md` (l.212), a receipt
  `.ufo/waves/round-50/evidence/selftests/<stem>.txt` per pin (l.195), `exists()` of
  `corpus/lessons/round-N-verifier-spotcheck.md` (l.135–136), and the fleet `MANIFEST.json` at the pinned fleet rev
  (l.275, outside the lane). It **runs** the two pinned tools from `git archive R` (l.290–310). No string
  `SOURCES.md`, `corpus/knowledge`, or `sources-r50` appears anywhere in it
  (`grep -nEi 'SOURCES\.md|corpus/knowledge|sources-r50' count-c1.py` → no match).
- `count-c2.py` reads, at R: the entry (`ENTRY` l.31, read l.124), `corpus/SOURCES.md` (l.142), and the three
  committed copies with their frozen sha256 (`COPIES` l.40, read l.118). `grep -nEi 'SCORECARD|SHONEN' count-c2.py`
  → no match.
- The pinned tools' `--selftest` bodies build their own fixtures under `tempfile.mkdtemp` (pin-check l.976 onward;
  unlanded-check l.86 onward, its `corpus/…` writes land in sandbox repos it creates). They do not read the lane
  tree's corpus. Empirically: C1 still `met` at A0, where the lane entry and all three copies are absent.

Answering the question in both directions, with counter lines rather than prose:

1. **Could C1 have been met by C2's work?** No. C2's whole landed surface is present in fixture B (entry, rows,
   copies) and C1's own two files are at the salvage bytes; C1 prints `unmet … mismatches=6` (see `C1=B` above).
   C2's files do not appear in any C1 item: the six mismatches are four Axis Last-change cells and the two SHONEN
   pins, all C1-surface objects.
2. **Could C2 have been met by C1's work?** No. C1's whole landed surface is present in fixture A (SCORECARD cells,
   SHONEN pins, receipts) and C2 prints `unmet … bad_rows=22 … source_rows=bad sources_floor` (`C2=A`). Every one
   of the 22 rows parses (`claims=22`), so the entry survives; `located=0` and `bad_rows=22` say the only broken
   link is the SOURCES row each row cites.
3. **Is either claim *sufficient* on its own, with the other's surface emptied?** Yes, each is: C1 `met` at A and at
   A0 (C2 rows / entry+copies+rows absent, item text byte-identical to the landing), C2 `met` at B (C1 cells
   reverted, line byte-identical). So the two predicates are causally orthogonal to each other's files; the only
   shared inputs are external to both surfaces (fleet `MANIFEST.json` for C1; the freeze-committed copies for C2's
   pins, which are present in every fixture by construction).

The 2×2 is therefore a clean factorial: `P_C1` follows the SCORECARD/SHONEN delta and nothing else; `P_C2` follows
the SOURCES-row delta (plus entry/copies presence) and nothing else. Neither claim is an alias of the other, and
neither can borrow the other's evidence.

## 5. Strongest counterexample I could build

The strongest attack on the *separability receipt as prescribed* is not against the conclusion but against the
fixture: because the entry and the three copies are inherited from `9b8562a3` (the entry's only commit is the
salvage; the copies were committed at the freeze `950e99be`), the prescribed fixture A reverts only three
`corpus/SOURCES.md` rows. A reviewer who read "C2's files reverted to `9b8562a3`" as "the entry is gone" would be
wrong about what was measured: A still contains the 83-line entry and the 10,669-line copy set, and C2's failure at
A is exactly one arm (`bad_rows/source_rows/sources_floor`), not `entry_absent,pins`. A0 (`08f8d075`, entry +
copies + rows removed) closes that gap for the C1 side: C1 is `met` with C2's surface *fully* absent, so the
contract's sentence "C1 reads no corpus entry" is confirmed end-to-end, not merely for the row linkage.

What the fixtures do **not** show: whether the claims would be met if the freeze itself (counters, controls,
receipts) were absent — not testable by design, since the counters are the measuring instrument. They also do not
test that a *real* C2 revert (a tree where the entry never existed) keeps C1 met under a different entry path; the
counter hard-codes its surface, so no such tree can change C1.

## 6. Landing-delta provenance (observation, not a defect)

The attempt-2 landing's predicate-bearing delta is small: `SCORECARD.md` (10 added / 4 removed lines, incl. the
round-50 correction paragraph), `SHONEN.md` (1 line: pins 60/60→114/114, 13/13→17/17 plus receipt paths), and 3
appended `corpus/SOURCES.md` rows (plus 31 non-predicate lines in three `assimilation/a2/` files). The heavy C2 artifacts (entry 83 lines; copies 10,669 lines) were committed by
the salvage commit `9b8562a3` (author `mori-shokunin <mori@shokunin.local>`, message "…orchestrator salvage of
unlanded attempt-1 wave state and knowledge draft…"), and the C1 receipts
(`.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt`, `…/mori-unlanded-check.txt`) are present already at
`9b8562a3`. P-C1/P-C2 only require the artifacts at R, which holds — but any narrative that credits attempt 2 with
authoring the entry, the copies or the receipts is attributing attempt-1/salvage work to the attempt-2 landing.

## 7. What I did not verify / limits

- This is a dispatched-seat review, not an independent judgment of either claim; I did not re-adjudicate the C1/C2
  predicates themselves (controls, floors, quote entailment), only their separation.
- Fixture commits are ephemeral (scratch removed). Rebuild recipe: clone `--shared` the lane at `487941b9`, then for
  A `git checkout 9b8562a3 -- corpus/knowledge/oom-memcg-stat-r50.md corpus/SOURCES.md`; for B
  `git checkout 9b8562a3 -- SCORECARD.md SHONEN.md`; for A0 additionally `git rm` the entry and the three
  `corpus/evidence/sources-r50/` copies. Score with `--repo <clone> --fleet-repo /home/vgpnk/Projects/shokunin`
  (C1) / `--repo <clone>` (C2).
- The clone is `--shared`, so object bytes are the lane's; fixture trees were verified by `git diff --stat` before
  scoring. C1's pinned-tool runs executed from `git archive` of the fixture revs with `TMPDIR` under scratch.
- No host state was touched: no kernel-log MESSAGE read, no cgroup change, no OOM trigger, no systemctl/journalctl,
  no pacman (transactions are paused host-wide), no tool installs. `/home/vgpnk/Projects/shokuknow` was not read.
- Independence is total, so neither counter would catch a cross-surface inconsistency that leaves its own surface
  intact (e.g. at fixture A the entry cites S489–S491 while SOURCES lacks them; C1 still prints `met`). That is
  separability working as specified, and C2 is the instrument that catches that class; it is a named limit of using
  C1 alone as a lane-wide health check.
- Read-only git only (`show`, `diff`, `log`, `cat-file`, `ls-tree`, `merge-base`, `archive` via the counter); no
  add/commit/checkout/reset outside the throwaway clone.

## Findings

- **LOW — F1 (no defect; conclusion): the separability sentence in `contract.md` §Separability holds.** C1=`met` at
  fixture A (`f3a2f46`) and at the full-C2-revert fixture A0 (`08f8d07`) with item text identical to the landing;
  C2=`met` at fixture B (`6df703b`) with its line identical to the landing; the counter-evidence cells (`C1=B`,
  `C2=A`) show neither claim can be satisfied by the other's surface. Concerns: no file; supports axes
  **calibration** (C1) and **depth** (C2).
- **MED — F2 (evidence-design, fixable in wording): the prescribed fixture (a) is not a C2 revert, only a
  three-row revert.** `corpus/knowledge/oom-memcg-stat-r50.md` is byte-identical at `9b8562a3` and `487941b9`
  (sha256 `0fac741c…c109`; the entry's only commit is `9b8562a3`) and the three `corpus/evidence/sources-r50/`
  copies are already pin-clean at `9b8562a3`, so fixture A's diff vs the landing is `corpus/SOURCES.md | 3 ---`.
  The round's separability receipt should say "SOURCES rows S489–S491 only" and/or cite A0 `08f8d075` for the
  empty-C2-surface test. Concerns `contract.md` §Separability (fixture definition) and the seat spec; impacted axis
  **depth**.
- **LOW — F3 (provenance note, no data change): the attempt-2 landing delta is 5 predicate-relevant lines; the C2
  entry/copies and the C1 receipts predate it.** `git diff --name-status 9b8562a3 487941b9` lists `SCORECARD.md`,
  `SHONEN.md`, `corpus/SOURCES.md` plus three `assimilation/a2/` files; `corpus/knowledge/oom-memcg-stat-r50.md`
  was introduced by the salvage `9b8562a3` (absent at freeze `950e99be`) and the selftest receipts are present at
  `9b8562a3`. P-C1/P-C2 are unaffected (artifacts exist at R), but attribution wording that credits attempt 2 with
  the entry, the copies or the receipts is wrong. Concerns `SCORECARD.md` round-50 correction paragraph and the
  attempt-2 landing commit message; impacted axes **calibration** and **depth**.
- **LOW — F4 (named limit, no defect): C1's independence means `C1=met` says nothing about C2's surface.** At
  fixture A (`f3a2f46`) the tree is internally inconsistent — the entry still cites S489–S491 that SOURCES no
  longer contains — and C1 prints `met` (8/8 items `state=ok`). C1 must not be read as a lane-wide consistency
  check; only C2 catches that class. Concerns `.ufo/waves/round-50/count-c1.py` read set (l.211–212, 195, 135–136)
  and the calibration axis.
