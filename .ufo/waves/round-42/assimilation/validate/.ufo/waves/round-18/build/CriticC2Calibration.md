# C2 calibration critique

## Verdict

- The `1 → 0` is a defensible **retrospective correction of the register**, but by itself it is not evidence that calibration behavior improved. It counts whether a known historical overclaim remains uncorrected, and the correction is specifically prompted by the already-available closure. Treat it as a record-accuracy result, not a prospective calibration gain.
- The closure is non-author evidence, so comparing the tool's historical verdict with it is not literally a circular oracle. However, the reported 3/3 concordance is not an independent calibration trial: L1's frozen register already contains those rulings and their source locations. It demonstrates agreement/reproduction against known rulings, not blinded prediction.
- Self-application is meaningful only at a measured tip that includes a later implementation commit. At the freeze commit itself, `r18-C2` has no implementation commit and the defined verdict is `no-implementation`, not `pre-build`. A requirement that it report `pre-build` when measured at 29b0 would contradict the verdict rule and make the test pass only by conflating absence of an implementation with demonstrated ordering.
- Yes: calibration is a lowest non-retired axis, **tied at 5** with depth and freshness, not uniquely lowest.

## Counterexample and evidence

The historical register says `r17-C3` was declared `pre-build` in five locations, while the cited non-author ruling is `co-evolved` (`.ufo/waves/round-18/frozen/c2-register.json:24-29`). The round-17 closure explains that the final evidence supports the actual repair but does not establish blanket pre-build preregistration (`corpus/lessons/round-17-verifier-spotcheck.md:207-213`), and explicitly directs that this round not be labeled pre-build (`:398-402`). The round-18 contract then defines the before count as one and the after count as zero by appending a correction row (`.ufo/waves/round-18/contract.md:31-37`). This makes the change causally clear: the historical claim is being corrected after the adjudication, with no new calibration decision or blinded case required. The append-only correction preserves provenance, but the count still measures current register state, not the author's ability to calibrate on unseen outcomes.

The register's author field identifies L1, and its r17 rows include each external ruling and `ruling_at` pointer (`.ufo/waves/round-18/frozen/c2-register.json:3, 15-29`); the contract itself routes the repair from the r17 closure (`.ufo/waves/round-18/contract.md:9-15`). **[INFERENCE]** The ruling was therefore known and embedded before the C2 score was computed. Keep 3/3 as retrospective oracle concordance only. For a calibration claim, freeze labels and the requirement universe before exposing the judge/author to a blinded, independent ruling, or use a later held-out round.

The frozen commit check confirms the self-application boundary: `git ls-tree -r --name-only 29b0dc79e193b9d67845e39850a091a84bad66bd -- .ufo/waves/round-18/frozen/c2-register.json tools/mori-freeze-order.py corpus/evidence/freeze-register.json` (exit 0) listed only `c2-register.json`; `git rev-list --reverse --topo-order d005cdde0e009dea6c0cc29b37163de536528658..29b0dc79e193b9d67845e39850a091a84bad66bd` (exit 0) listed only the freeze commit; and `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-status -r 29b0dc79e193b9d67845e39850a091a84bad66bd -- .ufo/waves/round-18/frozen/c2-register.json tools/mori-freeze-order.py corpus/evidence/freeze-register.json` (exit 0) showed that commit adding the register, not the tool or correction file. Thus for `r18-C2` with tip forced to 29b0, `I` is absent under the frozen rule (`contract.md:62-65`; `c2-register.json:4-14, 34-37`) and the result must be `no-implementation`. Since the row is labeled `pre-build`, the stated overclaim rule makes it a mismatch at that tip. **[INFERENCE]** At a later measured tip, it can validly verify `pre-build` if 29b0 remains the last frozen-path change and the first implementation commit is later.

## Falsifier L1 must run

At the completed measured tip, first run the exact C2 check with all r18 tips explicitly set to the freeze commit:

```sh
python3 tools/mori-freeze-order.py check \
  --repo "$R" \
  --register .ufo/waves/round-18/frozen/c2-register.json \
  --corrections corpus/evidence/freeze-register.json \
  --tip-for r18-C1=29b0dc79e193b9d67845e39850a091a84bad66bd \
  --tip-for r18-C2=29b0dc79e193b9d67845e39850a091a84bad66bd \
  --tip-for r18-C3=29b0dc79e193b9d67845e39850a091a84bad66bd
```

The required falsifying outcome is `r18-C2: verdict=no-implementation`, with its effective `pre-build` label reported as an overclaim and the check exiting 1. If the tool calls that `pre-build` or exits clean, it has hidden the `I=none` case and the self-application does not test the declared rule. Separately, for the required failure-capability arm, the executor must run its isolated `--selftest` under its assigned `.scratch/` and verify that a fixture which co-commits a frozen path and implementation yields `co-evolved`, `overclaim=true`, and a failing check invocation (exit 1 with the stable expected finding). The aggregate selftest should pass only after asserting that failing child result; a clean aggregate selftest is not itself evidence that the fixture check was clean.

Do not demand `pre-build` at tip 29b0. For the positive self-application, use the eventual measured tip while requiring the frozen-path last-change to be 29b0 and the first implementation commit to follow it. The contract already calls for a co-committed fixture (`.ufo/waves/round-18/contract.md:35-37`).

## Smallest safe correction

Keep the append-only C3 correction and the 1→0 count, but describe it narrowly as a corrected historical overclaim; do not present either that count change or the known-oracle 3/3 as evidence of prospective calibration improvement. Make the positive r18 assertion at the actual post-implementation measured tip, with 29b0 as the observed freeze point; preserve `no-implementation` as distinct from `pre-build` at the freeze tip. Require the co-commit fixture's child check to fail as specified above.

## Axis evidence

`SCORECARD.md:1064-1077` calls calibration the C3-selected axis at score 5, shows depth and freshness also at 5, and says no axis is retired. The final active register still records calibration at 5 (`SCORECARD.md:1110-1117`). Therefore calibration is tied for the lane's lowest non-retired score.