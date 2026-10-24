# Round 36 W2 — claim-sizing audit

**Attack:** contract and round shape; C1 exploratory freshness technique and C2 measured operability.

## Medium — FAIL: C1's claim table still implies a freshness verdict

`contract.md:13` calls C1's axis “freshness” and says its capability “flags stale source rows.” That is a semantic freshness claim. The same contract says P-C1 cannot carry a freshness verdict: at `contract.md:118-125`, it explains the byte classifier detects representation differences rather than stale skill claims, declares C1 exploratory, and says P-C1 is evidence of byte behavior, “not as C1's verdict.” The frozen P-C1 in `count-c1.py:50-56` checks byte classifications, not freshness. The receipt's `C1=met` is consequently byte-evidence only, not evidence that stale sources were detected. The table's capability/axis remains oversized relative to the admitted evidence; do not treat the receipt as freshness admission.

**After-state command/output evidence** (recorded as scored at the data tip in `dispatch-log.txt:27-31`; default counter path retrieves the tool from the specified commit via `git show`, `count-c1.py:679-689` and `count-c2.py:677-686`):

- `python3 .ufo/waves/round-36/count-c1.py bf0df77fee4b6ef54a90aea09335c7617f125151` → `evidence/c1-after.txt:2-6`: `blind_rows=40 tool_exit=1 tool_rows=40 mismatches=0`; `real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0`; `C1=met`; seed `7388485190103051243`; `C1_EXIT=0`.
- `python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151` → `evidence/c2-after.txt:3-9`: blind `24/24`; real arm pass, tool/oracle both report 18 ids and identical lists; `C2=met`; seed `15440749816798970567`.

## Sizing and control checks

- **Predicates are bounded, not unbounded universals:** `contract.md:21-23` bounds the blind checks to 40 rows and 24 generated histories; C1's real arm is the finite registry at revision R. “Every row” is bounded by those fixtures/snapshot. No separate unbounded target found.
- **Predicate / counter / receipt labels:** P-C1 at `contract.md:21`, `count-c1.py:50-56`, and `c1-after.txt:1` is identical. P-C2 at `contract.md:23`, `count-c2.py:32-38`, and `c2-after.txt:1` is identical. The pin check `git show bf0df77fee4b6ef54a90aea09335c7617f125151:.ufo/waves/round-36/count-c1.py | sha256sum` produced `86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  -`; the corresponding C2 command produced `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  -`. Both equal `freeze-v2.txt:3-4` and the hashes shown in the C0 receipts. No kill-rule sentence/counter-hash/receipt-label mismatch found.
- **C0 predates data:** `git log --format='%h %cI %s' -15 bf0df77fee4b6ef54a90aea09335c7617f125151` showed C0/freeze-v2 commit `c1a026c` at `2026-10-23T09:03:05-03:00` and data commit `bf0df77` at `2026-10-23T15:20:10-03:00`.
- **Do-nothing controls cannot reach either target:** `evidence/c0-rescore-v2.txt:858-884` records K1 with the frozen C1 counter (`86dd…`): `blind_rows=40 tool_exit=0 tool_rows=0 mismatches=40`, `real_arm=skipped`, `C1=unmet`, `EXIT=1`. `:2-85` records J1 with the frozen C2 counter (`c7ed…`): its empty result fails the blind arm (1/24 histories match) and real arm (empty output versus oracle's 18 ids), then `C2=unmet`, `EXIT=1`. The receipt records the controls, selected counter, seeds, and outputs, but not their complete argv; exact C0 invocation lines are therefore unavailable in this checkout.

## Residual risk and verification gaps

- The after-receipt files are untracked at the inspected tip (`git status --short -- .../c1-after.txt .../c2-after.txt` → `??` for both); `dispatch-log.txt` records the post-commit scoring, but the receipts themselves are not contained in `bf0df77`.
- `freeze-v2.txt` pins contract.md as `dbd3f6d…`, while the inspected tip's contract hash is `065a17b…`; the contract's exploratory declaration was committed before data (`5842dc0`), and the dispatch log says the predicate sentences were unchanged. The predicate/counter/receipt identity check passes, but the whole-contract digest no longer authenticates the amended text.
- No LSP device/server is available: `read xd://lsp` returned “No such tool” (only `ast_edit` and `debug` were mounted). Findings are grounded in cited file text; no semantic references/diagnostics were available. No tools were installed.

VERDICT: FAIL (contract.md:13 overstates C1 as stale-source detection despite contract.md:118-125 explicitly limiting it to exploratory byte-behavior evidence).

Report: .ufo/waves/round-36/w2/RevContractSizing.md