# Mo57MutationTester34 — round-56 receipt review

## Findings and independent recheck plan

1. **Short-form evidence pointers confirmed.** The fleet-root report `.ufo/reports/round-56/mori.md:21,26,54-61` cites `evidence/driver-liveness-live.txt`, `evidence/tally-r55.txt`, `evidence/controls.txt`, and `evidence/c{1,2}-at-landed.txt`. `SCORECARD.md:2899,2903-2904` and `LOG.md:2954` also use `evidence/...`. The report commit resolves in the fleet repo (`git -C /home/vgpnk/Projects/shokunin log --format='%an %H %s' -3 -- .ufo/reports/round-56/mori.md` → `mori-shokunin a1c32aa4344a448d6772744fa06b1632056ada0b round-56: mori report`). The pointers do not resolve at either repository root: `test -e /home/vgpnk/Projects/shokunin/mori-shokunin/evidence/driver-liveness-live.txt` → absent; the analogous fleet-root path is absent. The real file is `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/driver-liveness-live.txt`. This is a citation-precision defect; evidence contents themselves were found at the wave path.

2. **Receipt wording is ambiguous.** Report `:21` says the live receipt is “(1728 lines, 0 malformed, 23 lanes).” The receipt is 304 physical lines (`wc -l .ufo/waves/round-56/evidence/driver-liveness-live.txt` → `304`); its JSON says `"lines": 1728` at `driver-liveness-live.txt:282`, `"malformed": 0` at `:283`, and has 23 lane keys (counted from `lanes`). Thus 1728 is the parsed watchdog-log line count, not the receipt-file length. Recheck by running `wc -l` and parsing the JSON separately; phrase the claim as `log.lines=1728`, `log.malformed=0`, `lanes=23` and identify the receipt path.

3. **Round-56 C2 absent-tool labels confirmed cosmetic/misleading.** `count-c2.py:69` returns `['tool_absent']`; its printer at `:156-163` marks each arm `ok` unless that arm's individual failure token is present. The replay `python3 .ufo/waves/round-56/count-c2.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa` produced `C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok ... failed=tool_absent`, exit 1. The committed `evidence/controls.txt:2` matches. By contrast, `count-c1.py:188-190` maps its `tool_absent` early return to all `bad` labels; the same replay printed all C1 arms `bad`. Independent recheck: run both counters at the entering revision and inspect the early-return and output mapping; do not read C2's `ok` arm labels as executed successes.

## Mutation probe — round-57 C1 pointer predicate

Target: frozen `.ufo/waves/round-57/count-c1.py:12`. Mutant: replace the required `".ufo/waves/round-56/" in x` substring with the weaker `"evidence/" in x`, which accepts the routed short-form citation. The detector was the same counter invoked via `GIT_DIR=<scratch-fixture>/.git python3 <counter> <fixture-rev>`; all fixture commits and files were confined to my scratch directory.

Observed outputs:

- Pristine, full-form fixture: `C1=met rows=2 evidence=ok rev=full`, exit 0.
- Pristine, short-form fixture: `C1=unmet rows=2 evidence=bad rev=short`, exit 1.
- Mutant, short-form fixture: `C1=met rows=2 evidence=ok rev=short`, exit 0.
- Mutant, full-form fixture: `C1=met rows=2 evidence=ok rev=full`, exit 0.
- Restored, short-form fixture: `C1=unmet rows=2 evidence=bad rev=short`, exit 1.

**Contract-level verdict: INCONCLUSIVE due to a pristine-baseline false accept.** The full-form scratch fixture deliberately contained no evidence blobs, yet the pristine counter returned `C1=met`; the `count-c1.py` predicate checks only for the path prefix and `| 56 |`, not whether the referenced path resolves. This violates the frozen wording “resolvable round-56 evidence pointer.” The short-prefix mutant is killed by the narrower string-form detector, but that does not establish actual pointer resolution. Coverage finding only; no contract change or remediation made.

Hashes (SHA-256): pristine/before `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`; mutated `9414525e1ec077b60b5d5ce5ef80ff07feead9877b042ad35f12c8ec1b03faac`; restored `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`. The frozen-commit blob and lane working file had the pristine SHA-256; lane file hash after the probe remained the same. Restoration was an exact copy from the untouched pristine scratch copy, followed by the restored detector run above.

## Recheck plan

1. From both repo roots, test each cited `evidence/...` path and compare with the actual `.ufo/waves/round-56/evidence/...` location; preserve the report's fleet-root location distinction.
2. Check the receipt's physical line count separately from its `log.lines`, `log.malformed`, and lane-key fields.
3. Replay both round-56 counters at `5b295eee...`; distinguish `failed=tool_absent` from arm execution and confirm C2's labels are not evidence of successful arm evaluation.
4. At the frozen round-57 measurement revision, verify both C1 capability rows and independently resolve each cited evidence path in that revision. The frozen counter alone does not establish resolution, as the dangling full-form fixture demonstrated.

No production files, counters, contracts, or commits were changed.