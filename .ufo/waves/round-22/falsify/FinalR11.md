# R11 static falsification

## Result

**R11 holds for the delivered implementation on the frozen `forbidden` fixture; the oracle does not isolate the branch that makes it hold.** This is a static source trace only; no commands, fixtures, tests, or production code were executed or changed.

## Observed source path

- The effective contract leaves R11 as “forbidden allowlist cannot become clean” ( `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/contract.md:19` ); the correction changes the R03/R04 population semantics, not R11 ( `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/denominator-correction.md:7-9` ). The v2 requirements file lists R11 among the frozen 24 IDs.
- In `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/frozen/fixture-builder-v2.py:38-46,49-75`, the `forbidden` variant sets `must_redact_paths` to `allowed.txt`. It contains five matching raw hits: one in the policy source, two on the allowed path, one ordinary unallowed hit, and one non-author hit. The two allowed-path hits share the same path/class/line-digest, so the fixture builder emits one corresponding allowlist row and one forbidden entry. It removes both matching allowed-path hits from `allowed_effective` and adds both to `unallowed`; thus `raw_unallowlisted` is three (two forbidden-path hits plus the ordinary unallowed hit). The non-author hit remains excluded by its configured glob.
- In `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-retention-reconcile.py:195-218`, the checker derives `forbidden` when an allowlist row's path is in `must` (lines 197-202); such a row is not added to `allowed_keys`. It partitions hits by the non-author glob (203-207), then sets `retention_code` from `unallowed or forbidden` and selects `allowlist_forbidden` when `forbidden` is nonempty (209-210). It compares the receipt's hit lists, counters, forbidden rows, finding, and wrapper exit code before accepting a match (211-218). On this fixture, both `unallowed` and `forbidden` are nonempty, so the matched receipt is red, retains the forbidden finding, and reconciliation succeeds without granting privacy clearance.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-22/oracle-reconcile-v2.py:40-46,52` runs the `forbidden` variant through the same `check` CLI used by the other arms and requires successful reconciliation plus `forbidden_allowlist == 1`, `raw_unallowlisted == 3`, red state, and `privacy_clearance is False`. These assertions are consistent with the branch trace above.

## Missing control and smallest counterexample to R11's coverage

R11's fixture already has three unallowlisted hits. Therefore the assertion that its state is red does not show that the `or forbidden` term in `retention_code` is necessary. A minimal surviving code mutant is `retention_code = int(bool(unallowed))`: on the frozen R11 fixture `unallowed` is still nonempty, so the result remains red and the R11 assertions still pass even though the forbidden-only red path is no longer enforced.

The smallest isolating input is one valid allowlist row whose path is listed in `must_redact_paths`, but whose identity has no hit in the measured tree; keep the class policy and allowlist valid, and make the measured tree produce zero hits. The current source marks the row forbidden before checking whether its identity occurs in the hit set, so the correct receipt is red solely because `forbidden` is nonempty. The mutant above would make it clean. Add this as an R11-specific red arm through the same `check` command, ideally paired with an otherwise equivalent no-forbidden clean control. R02 is not that control: it is a separate fixture whose ordinary unallowlisted hit independently makes it red. The oracle also constructs receipts itself; its `check` invocation does not execute the embedded retention-gate command recorded in each wrapper.

## Evidence limits

High confidence in the stated branch behavior and test gap from direct source inspection. No LSP device was exposed in the available tool inventory; grep was used only to locate sections, not as semantic proof. Dynamic behavior remains unverified by design.