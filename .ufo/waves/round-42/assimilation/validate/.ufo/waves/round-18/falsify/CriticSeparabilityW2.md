# Round 18 separability falsification — target `e2bfbd6f8dccc51fc06455efc41f720301112dd4`

## Axes

- **Execution independence:** can a verifier run without invoking the other criterion's executable?
- **Evidence/population independence:** does the verifier's input or measured population include another criterion's artifacts?
- **Target-tip provenance:** is the claimed result actually recorded for the attacked revision, using the committed inputs?

## Verdict per pair

| Pair | Verdict | Basis |
|---|---|---|
| C1–C2 | **Separate executables; not fully outcome-independent.** C1's `scan` reads Git blobs and C1 inputs; it does not call the C2 checker. But the C2 register's `r18-C1` row explicitly names C1's frozen inputs and `tools/mori-retention-gate.py` as its implementation path. In addition, C1's contract scans every tracked blob, so the C2 tool is part of C1's measured population. | `contract.md:24-37,47-65`; `frozen/c1-policy.json:5`; `frozen/c2-register.json:30-37`; `tools/mori-retention-gate.py:177-204,310-324`; `tools/mori-freeze-order.py:200-263`. |
| C1–C3 | **Separate executables; C1's measured population is shared.** C3 verifies a committed ledger against the dispatch JSON; it does not need C1. C1's full-tree scan nevertheless includes the C3 implementation, ledger and dispatch when those are tracked at the measured revision. Removing those files from the measured tree would change the scan input; whether they contribute C1 hits at `e2bfbd6` was not established here. | `frozen/c1-policy.json:5,27-29`; `frozen/c3-ledger-format.json:4-21`; `tools/mori-dispatch-ledger.py:102-164,200-338`. |
| C2–C3 | **Separate executables; C2's full result is linked to C3 landing.** The C2 `r18-C3` row explicitly names `tools/mori-dispatch-ledger.py` as its implementation path. The C3 verifier itself reads the ledger and referenced dispatch from Git and does not invoke C2. | `frozen/c2-register.json:38-41`; `tools/mori-freeze-order.py:200-263`; `tools/mori-dispatch-ledger.py:200-338`. |

### Specific questions

- **Does a C2 round-18 row depend on C1 landing? Yes: `r18-C1`.** It tests whether the C1 frozen paths precede the first commit touching `tools/mori-retention-gate.py`; it does not test or consume C1's scan result. Path-history queries at the target show the C1 frozen paths last changed at `29b0dc79e193b9d67845e39850a091a84bad66bd`, while the C1 implementation path first changed at `b8f5c6c38e591fed20c1e121af187e58c959c1fe`; no later changes to either set appeared in that queried range. Thus the row is *intentionally cross-claim*, although the C2 executable can evaluate it without running C1. `r18-C2` does not depend on C1; `r18-C3` depends on C3's implementation path, not C1. The C2 register uses placeholder tips for these rows, so the exact target must be supplied with `--tip-for` to evaluate them (`frozen/c2-register.json:30-41`).
- **Does the C3 wave-1 ledger depend on C1/C2? No, not on their tools or results.** The frozen identity is over the whole dispatch `context` and `tasks` payload, and verification recomputes it from the committed dispatch referenced by each row. The target's `wave1-attempts.json:1-14` has one row with a payload digest, `tasks_count` 68, result `started`, and `started_ids` 68. This is a payload/receipt relationship, not proof that any task passed. [INFERENCE] Whether that task array contains C1/C2 assignments was not inspected; it is immaterial to verifier execution independence and the ledger's result semantics.

## Strongest counterexample: the target-tip verdicts are not demonstrated by the committed reports

The tool designs are separable, but the L1 drafts overstate what the recorded evidence establishes at `e2bfbd6`:

1. `draft-verdicts.md:8` claims C1 reaches zero at the final measured commit, while also describing 55 hits at `daceeec` as pending allowlist rows. The committed `build/RetentionGate.md:16-24,42` records scans at `d005cdd` and `29b0dc7`, not at `e2bfbd6`; the `29b0dc7` scan reports four new rows versus the frozen population and is explicitly called outstanding. `build/RetentionGate.md:30` records a selftest, not a scan of the attacked tip. In the C1 source, `--frozen-run` checks a pinned synthetic snapshot (`tools/mori-retention-gate.py:331-397`); only `scan --repo ... --rev ...` measures a Git revision (`:177-204,310-324`). Those are different checks. The target tree search found no committed C1 allowlist file/rows (the scan accepts an optional external `--allowlist`). Therefore C1 is **independently runnable** at the target, but a clean C1 result at that target is **not established by the committed record**. If the 55 name-only hits still exist, the absent committed allowlist is a reproducibility blocker; if later edits removed them, the missing target scan still leaves that claim unverified.
2. `draft-verdicts.md:9` claims C2's three round-18 rows are `pre-build` at tip. The C1/C2/C3 path chronology is consistent with that ordering, but `build/FreezeOrder.md:14-17` records a run with all three tips set to `29b0dc79...`, where all three rows were `no-implementation`; it is not a run at `e2bfbd6`. Also, `build/FreezeOrder.md:29` says `no-implementation` is excluded from overclaims, while the exact target C2 implementation computes `overclaim` as `effective_label == "pre-build" and verdict != "pre-build"` (`tools/mori-freeze-order.py:260`). Do not use that stale run/report as proof of the target implementation's output.
3. `draft-verdicts.md:10` claims C3 wave-1 is bound. The target has the wave-1 ledger row and dispatch, but the committed `build/DispatchLedger.md:19-21` records round-17 ledger checks and a round-17 bind, not a `verify` of the round-18 wave-1 ledger at `e2bfbd6`. The C3 implementation can verify it independently, but the recorded digest field alone is not a recomputation.

The frozen C1 policy also labels its regex classes a recall floor, with the reading sweep outside the metric (`frozen/c1-policy.json:27-29`; `out-of-metric-triage.md:3-6`). Thus even a clean C1 tool result would not establish the separate whole-round privacy disposition.

## Smallest safe correction

Record a target-pinned run of each verifier, with exact revision and input paths in the report: C1 `scan` at the measured tip (commit an allowlist input or its digest if needed, then remeasure the resulting final tip); C2 `check` with explicit `--tip-for r18-C1=e2bfbd6`, `r18-C2=e2bfbd6`, and `r18-C3=e2bfbd6` plus the correction file; and C3 `verify` for `.ufo/waves/round-18/wave1-attempts.json` at that same tip. Keep each finding/output separate and do not represent the C2 `r18-C1` row or the C1 whole-tree population as causally independent. No verifier or selftest was executed in this review.

## Read-only command/evidence log

All commands below used `git -C /home/vgpnk/Projects/shokunin/mori-shokunin` and were read-only.

- `log -1 --format=%H` → exit 0; the checkout's observed head was `95c615836c2cf74ee11539c4289a1ce06a81cfcb`, later than the attacked tip. `log -1 --format=%H e2bfbd6` → exit 0; resolved to the requested target `e2bfbd6f8dccc51fc06455efc41f720301112dd4`. Source, tree, and path-history findings above were pinned to that target using `show`, `ls-tree`, `log`, and `grep`, not inferred from the later checkout.
- `log --reverse --format=%H d005cdde0e009dea6c0cc29b37163de536528658..e2bfbd6` → exit 0; returned the five-commit range used for chronology. Separate path-limited `log` queries for C1, C2, and C3 frozen/implementation paths → exit 0; each showed the freeze commit then the first-implementation commit described above.
- `show e2bfbd6:<tool path>` for the three verifier scripts; `show --format= --name-only` for the freeze, first-implementation, and attacked commits; and targeted `grep -n` queries over the contract, C2 register, verifier sources, reports, and ledgers → exit 0.
- `grep -l '"line_sha256"' e2bfbd6` → exit 0; it found population/tool/report references, not a dedicated committed allowlist. An exploratory `ls-tree` query using unsupported `:(glob)` pathspec magic → exit 128; it made no changes. The subsequent `grep -l` check was the content-based fallback.
- No verifier, test, selftest, install/update, or VCS mutation was performed. No URLs were consulted.
