# SimpCounters — round 48 w1

Scope: review of the frozen C1/C2 counters; no frozen or production files changed. Candidate changes below are for a successor counter only. No tools were installed.

## Deletion candidates

1. **C1 selftest no-op** — delete `text = text.replace("(743 lines)", "(743 lines)")` immediately below the variants comment in `count-c1.py`. The synthetic registry constructed immediately above already contains `(743 lines)` in its first data row; the replacement is identity and does not establish an anchor. This is the only candidate proven by the scratch edit.
2. **C1 unused import** — `import concurrent.futures` is not referenced: the code uses the qualified name `concurrent.futures.ThreadPoolExecutor` / `concurrent.futures.as_completed`, so it is used; retain it. AST name-use check reports no unused C1 imports other than this apparent false positive (the import binds the `concurrent` package name, which AST import alias analysis must account for).
3. **C2 dead branch** — in `selftest()` quote construction, `quote_from(urls[0], "Quota exceeded", 3) if False else ...` always chooses the `else` operand. Removing the unreachable `if False` arm is behavior-preserving and a plausible next-round cleanup, but was not applied/proved in scratch during this assignment.
4. No unused C2 imports or helper functions were identified. `normalise` is used for both quote extraction and evaluation; normalization is not duplicated as an identical second routine.

## Evidence / proof

Scratch directory: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48-SimpCounters/`. Frozen counter copies initially matched the frozen SHA-256 values: C1 `7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97`; C2 `0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561`.

Applied only deletion candidate 1 to scratch C1. `diff -u` against frozen C1 showed exactly that one-line deletion; scratch C2 diff was empty.

- `TMPDIR=<scratch> python3 <scratch>/count-c1.py --selftest` → exit 0; `C1_SELFTEST pass=34 fail=0` (all 34 named checks PASS).
- `python3 -I -B <lane>/.ufo/waves/round-48/count-c2.py --selftest` → exit 0; `C2_SELFTEST pass=22 fail=0` (all 22 named checks PASS).
- Scratch C2 selftest attempt → exit 1, because its computed lane path resolves to `/home/vgpnk/Projects/shokunin/`, so it cannot find `corpus/evidence/sources-r48/xfs_quota.8.html` there. This was a scratch-location limitation, not evidence of a C2 behavior change; C2 was unmodified.
- Entering tool copy extracted from frozen revision had SHA-256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`, matching the freeze receipt.

A real C1 comparison (frozen versus scratch candidate, same tool/revision) was started in scratch; at report preparation both commands were still running, so real-run output identity is **UNVERIFIED**. No claim is made that real-run proof is complete. Since the proposed deletion is a literal identity operation and the selftest tally is unchanged, its local effect is established, but the assignment's full real-run proof remains outstanding.

## Preserved contract and tradeoff

The frozen counters remain byte-identical and authoritative. The one proven candidate deletes no variant logic and changes neither the 34-arm selftest tally nor its observed output; the tradeoff is purely removal of misleading no-op code. Other cleanup remains a proposal until independently checked against unchanged selftest and real-run output in a successor.

Real-run pair completed: baseline command using frozen C1 and scratch entering-tool copy, then the same command using scratch C1 with the single deletion. Both exited 1 and produced byte-identical output: J1-J8 all `got=met rc=0`, H1-H4 and real `got=met rc=0`, and `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05459887d9597ea5d1da0d8e3d024e0d17`. Thus the candidate preserves the full measured output (though the entering tool itself fails the frozen calibration predicate as its receipt also records).
