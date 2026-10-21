# No-harm checks at the measured commit

Review result: pre-registered commands and one blocking check-registration gap. **No selftest, oracle, or regression gate below was run**, per assignment. The only executed command was the read-only hash inventory recorded under source integrity.

Run from the lane root, at the final measured commit, in one shell. The output paths below are intended to be fresh; do not reuse existing output directories/files.

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
NH="$PWD/.ufo/waves/round-20/evidence/no-harm"
mkdir -p "$NH/tmp"
```

## C1: freshness and protected source bytes

The frozen C1 contract says the census source is not changed and retains the entering digest (`contract.md:46-47`). The exact census digest is in `evidence/c1-drift-entering.json:3`. At this review, the read-only command

```sh
sha256sum tools/mori-census.sh corpus/evidence/baseline-r10-20261015T2231Z.json
```

returned:

```text
87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28  tools/mori-census.sh
0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478  corpus/evidence/baseline-r10-20261015T2231Z.json
```

At the measured commit, require both protected files to remain byte-identical:

```sh
printf '%s  %s\n%s  %s\n' \
  '87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28' 'tools/mori-census.sh' \
  '0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478' 'corpus/evidence/baseline-r10-20261015T2231Z.json' \
  | sha256sum --check -
```

Expected: both `OK`. Also run the hermetic census selftest (the script documents `--selftest`, exit 0 pass, in `tools/mori-census.sh:397-407`):

```sh
TMPDIR="$NH/tmp" bash tools/mori-census.sh --selftest
```

Expected: exit 0 and `MORI_CENSUS_SELFTEST: PASS`. Do not substitute a live census run for this check.

## C2: settlement selftest and independent oracle

The frozen interface declares `mori-wave-settlement.py --selftest` (`contract.md:56-61`). Once integrated, run:

```sh
python3 tools/mori-wave-settlement.py --selftest
```

Expected: exit 0. This is only the tool selftest; it is **not** the independent 14-case oracle acceptance.

**Blocking registration gap:** the contract requires an oracle harness independent of the settlement implementation and 14/14 matches (`contract.md:90-94`), with `counts.matched == 14` and zero after-state `capability_absent` (`contract.md:100-104`). The frozen inputs are `.ufo/waves/round-20/frozen/c2-expected.json:1-21`. Neither the contract nor the current `tools/` inventory provides an executable oracle-harness path/argv; the current `.ufo/waves/round-20/build/OracleHarness.md` still contains only `STATUS: started`. Do **not** count the tool's own `--selftest` as this oracle. The exact independent-harness command therefore cannot be truthfully pre-registered from the available artifacts; L1 must add its concrete path and argv to this register before acceptance, then require exit 0, `matched=14`, and no `capability_absent`.

## Prior regression gates

These are full normal regression runs, not merely harness selftests. Run each once; require exit 0 and its gate's all-cases-passed result. The argv follows the scripts' documented examples/defaults: R13 `tools/mori-round13-regressions.py:173-174,3222-3247`; R14 `tools/mori-round14-regressions.py:157-164`; R15 `tools/mori-round15-regressions.py:105-110,129-136`; R16 defaults `tools/mori-round16-regressions.py:84-87,1726-1746`; R17 seat defaults `tools/mori-round17-seat-regressions.py:185-193,3023-3070`; R17 census/JJ usage `tools/mori-round17-jj-regressions.py:85-87`.

```sh
python3 tools/mori-round13-regressions.py --output "$NH/r13"
python3 tools/mori-round14-regressions.py --census tools/mori-census.sh --output "$NH/r14"
python3 tools/mori-round15-regressions.py \
  --census tools/mori-census.sh \
  --fixtures .ufo/waves/round-15/fixtures \
  --expected .ufo/waves/round-15/expected.json \
  --output "$NH/r15"
python3 tools/mori-round16-regressions.py \
  --tool tools/mori-journal-window.py \
  --fixtures .ufo/waves/round-16/fixtures \
  --expected .ufo/waves/round-16/expected.json \
  --output "$NH/r16"
python3 tools/mori-round17-seat-regressions.py \
  --tool tools/mori-seat-terminal.py \
  --fixtures .ufo/waves/round-17/fixtures/seat \
  --output "$NH/r17-seat"
python3 tools/mori-round17-jj-regressions.py \
  --census tools/mori-census.sh \
  --output "$NH/r17-jj"
```

There is no `mori-round18-regressions.py` in the current `tools/` inventory. The available R18 component selftests are the narrowest exact checks rather than a fabricated unified runner. Their CLIs are in `mori-dispatch-ledger.py:545-565`, `mori-freeze-order.py:676-704`, and `mori-retention-gate.py:707-738`. The first two require a lane-local non-system-temp scratch; retention requires `TMPDIR` to resolve exactly to the lane's `.scratch` (`mori-retention-gate.py:457-475`). Run:

```sh
TMPDIR="$NH/tmp" python3 tools/mori-dispatch-ledger.py --selftest
TMPDIR="$NH/tmp" python3 tools/mori-freeze-order.py --selftest
TMPDIR="$PWD/.scratch" python3 tools/mori-retention-gate.py --selftest
```

Expected: exit 0 for all three. `.scratch` was an existing empty directory when inspected; confirm it still exists at the measured commit.

R19 has no `--selftest`: `tools/mori-round19-regressions.py:1104-1111` requires both tools, expected file, output file, and mode. The harness requires absolute paths and `TMPDIR` to be an existing directory under the lane (`:877-890`); its pinned expected file is `.ufo/waves/round-19/frozen/expected.json` (`:25-27`). Run after-mode against the current tools:

```sh
TMPDIR="$NH/tmp" python3 tools/mori-round19-regressions.py \
  --content-tool "$PWD/tools/mori-content-review.py" \
  --freeze-tool "$PWD/tools/mori-freeze-order.py" \
  --expected "$PWD/.ufo/waves/round-19/frozen/expected.json" \
  --output "$NH/r19-after.json" \
  --mode after
```

Expected: exit 0 and status `pass` (not `capability_absent`, `failed`, or `setup-error`).

## Critique

- **Counterexample [INFERENCE]:** if the settlement selftest and implementation share a path-classification defect, both could agree that an unsafe traversal or symlink report is present; the independent harness would catch it via the frozen `traversal` and `symlink-report` cases (`c2-expected.json:14,16`). A selftest pass cannot establish the contract's independent 14-case result.
- **Evidence:** the contract explicitly calls for an independently written harness and 14/14 (`contract.md:90-94`); no such runnable command is registered in the current artifacts. R18 also has no unified round-18 regression script, so use only the three extant component selftests above rather than inventing one.
- **Impacted axes:** C2 coverage; calibration of the claimed oracle result. The source-hash and census-selftest checks separately protect C1 freshness.
- **Smallest safe correction:** retain the separate tool selftest, register the independent oracle harness's exact executable and full argv, then gate acceptance on its 14/14 matched result. Run the listed historical gates and protected-byte checks at the same measured commit; a nonzero result or an unavailable case is not a no-harm pass.
