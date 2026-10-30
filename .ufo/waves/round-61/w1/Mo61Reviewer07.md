# Mo61Reviewer07 — manifest completeness audit

Axes: inventory completeness, gate/probe classification accuracy, landing provenance, zero-mutation review.

Scope: entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`; manifest at frozen revision `7370a731abcafc4c803111de7c22cd6264d63be1`. Paths below are lane-relative unless absolute. This is a review recommendation, not an admission or a proposed amendment.

## Findings, by severity

### HIGH — F1: the 25-path manifest omits three landed gate/checker instruments

| Missing path | First landing commit | Exact evidence of gate/checker behavior |
|---|---|---|
| `.ufo/waves/round-52/check-history-rows.py` | `2f245af7d6dd6878de266f3436d12f47df900144` | `:2-7` declares the historical SCORECARD immutability check, `HISTORY_ROWS changed=N`, exit 0/1/2; `:44-53` computes differences and returns failure when changed. Committed receipt `.ufo/waves/round-52/evidence/m2-history-rows.txt:1-6` records both failing applier (`changed=6`, exit 1) and passing landed data (`changed=0`, exit 0). |
| `tools/mori-commit-runway.py` | `2a4213bf8da72f7cd78189baa5bb9be825dca1df` | `SKILL.md:1209` explicitly registers it as **gate (host-surface verdict; not a census or fleet-admission gate)**, with full verdict map, selftest and owner. Tool `:33-50` defines clean/low/unknown outcomes and `:56-61` its selftest. `LOG.md:2852-2857` names the landed tool and host measurement. |
| `.ufo/waves/round-54/checks/receipt-stage.py` | `f111d4b0120a04ed1a0a2270a72ec0a343d20e29` | `:2-10` declares QUALITY-148 receipt-stage check and exit 0 iff no flags; `:54-63` checks committed receipt existence, corrections, and returns failure for uncorrected intermediate citations. `LOG.md:2926-2927` records its use. Committed `.ufo/waves/round-54/evidence/receipt-stage-after.txt:1-3` records `flagged=0`, exit 0. |

The runway omission is especially unambiguous: the existing registry already calls it a gate, so this is not a new interpretation of a helper as a gate.

Impact: contract `:32` describes every gate landed in rounds 52–60, but its fixed 25-path target (`:34-40`) is narrower. Frozen `count-c1.py:82-90,113-120` derives its universe exclusively from manifest paths; it does not discover omitted instruments. A passing fixed-universe measurement therefore cannot establish the broader completeness claim. These findings do **not** establish failure of the separately frozen 25-path registration predicate. No counter or contract change was made or proposed.

### MEDIUM — F2: two manifest entries are not standalone gates under the existing gate/probe distinction

* Manifest `:107-110`, `tools/mori-driver-liveness.py`, landed `c419fe6dc051a5828fabd5f472f851e76dd54e8d`: tool `:9-10` expressly emits no wellness/failure verdict; `:32-40` supplies log-shape facts and `DRIVER_LIVENESS_OK` / `UNAVAILABLE`, rc 0/2. This is a probe, analogous to the existing `SKILL.md:172` journal-window row explicitly labeled “probe, not a gate” for OK/unavailable shape results. Its selftest is a gate over the probe; that does not make its ordinary observation command an admission check.
* Manifest `:102-105`, `tools/mori-vote-bind.py`, same landing commit: tool `:48-51` says a completed tally exits 0 **always** and the caller's counter interprets the line; `:437-441` prints the tally and unconditionally returns 0. It is an extraction/tally helper, not the standalone vote-acceptance gate. Its `--selftest` mode does have pass/fail behavior. Registering it as a helper/probe is defensible; describing the ordinary tally itself as a gate is not.

These are classification findings, not a claim that the files should be unregistered, nor a proposed frozen-universe change. The two round-56 counters are separately present and supply the claim-level predicates.

## Round-by-round inventory

All paths here were enumerated from committed trees/history, not inferred from reports. `M` = present in frozen manifest; `O` = omitted independent instrument; `A` = auxiliary implementation/test runner, not counted as a new independent gate.

| Round | Independent instrument inventory | First landing evidence |
|---|---|---|
| 52 | M `.ufo/waves/round-52/count-c1.py`, `count-c2.py`; O `check-history-rows.py` | counters `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`; checker `2f245af7d6dd6878de266f3436d12f47df900144`; LOG `2810-2815` |
| 53 | M `.ufo/waves/round-53/count-c1.py`, `count-c2.py`; O `tools/mori-commit-runway.py` | counters `f4da3fd400fa88a6db8ea544a4f7045c15d2410e`; tool `2a4213bf8da72f7cd78189baa5bb9be825dca1df`; LOG `2843,2848-2857` |
| 54 | M `.ufo/waves/round-54/count-c1.py`, `count-c2.py`; O `checks/receipt-stage.py` | counters `6830f3af992d906bfa1e17e3743e631ab834f67c`; checker `f111d4b0120a04ed1a0a2270a72ec0a343d20e29`; LOG `2895-2905,2926-2927` |
| 55 | M `.ufo/waves/round-55/count-c1.py`, `count-c2.py` | `c9b908f0bb89974f30b927776ce2450ae4198b10`; LOG `2940-2946` |
| 56 | M `.ufo/waves/round-56/count-c1.py`, `count-c2.py`; M `tools/mori-driver-liveness.py`, `tools/mori-vote-bind.py` (F2 classification caveat) | counters `3f494b49cde612d929e82887a48e1660c022c359`; tools `c419fe6dc051a5828fabd5f472f851e76dd54e8d`; LOG `2952-2954` |
| 57 | M `.ufo/waves/round-57/count-c1.py`, `count-c2.py`, `verify-c2-source.py` | counters `618562c72a03dc4d17386b715357f863fd327274`; verifier `6f3f84820911bafbb3f66cdcb080368c9242303f`; LOG `2964-2968` |
| 58 | M `.ufo/waves/round-58/count-c1.py`, `count-c2.py` | `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; LOG `2977-2981` |
| 59 | M `.ufo/waves/round-59/count-c1.py`, `count-c2.py`; M `tools/mori-register-check.py`, `tools/mori-settlement-scan.py` | `ccfd554e64084a0b4370806dd12a850e0a7bd7db`; LOG `2989-2993`; these are replacement/frozen attempt-2 artifacts, not the discarded attempt-1 bytes |
| 60 | M `.ufo/waves/round-60/count-c1.py`, `count-c2.py`, `count-c3.py`; M `tools/mori-entry-claims-check.py` | `4d036fb07207dbc9aa400617e57117b9857114e9`; LOG `3007-3035`; subsequent pre-data amendments do not change first-landing identity |

This accounts for all 25 manifest entries plus three omitted independent instruments (28 candidate instruments, including the two F2 probe/helper classifications). All 25 manifest landing/path pairs resolve with `git cat-file -e <landing>:<path>`.

Auxiliary executable inventory, explicitly excluded from independent-gate counts:

* A `.ufo/waves/round-52/r39-conform-selftest.sh`, landed `2f245af7d6dd6878de266f3436d12f47df900144`: `:2-8,18-19` wraps the existing round-39 selftest in a clone/bind mount; it adds isolation, not a new correctness predicate.
* A `.ufo/waves/round-55/checks/selftest-c1.py`, `selftest-c2.py`, landed `c9b908f0bb89974f30b927776ce2450ae4198b10`: split implementation of the already-inventoried counters' `--selftest`; callers are `count-c1.py:447-451`, `count-c2.py:347-353`. Both expose `run(counter)`, not an independent CLI gate.
* A controls/data drivers: r52 `controls/{c1-controls,c1-data}.py`; r53 `controls/{c1-data,controls}.py`; r54 `controls/{c1data,c2data,controls}.py`; r55 `controls/{c1data,c2data}.py`; r56 `controls/controls.py` (10 files). These construct/run controls for the parent counters rather than introducing a separate production gate.
* A dispatch/fixture builders: r52 `build-w1-spec.py`, `build-w1-spec-amend.py`; r53/r54/r56/r57/r58/r59 `build-w1-spec.py`; r60 `build-w1-spec.py`, `build-fixtures-r60.py` (10 files).
* A r58 wave probes `w1/Mo58Connector59.attack.py`, `w1/Mo58Executor44.receipt.py`, landed `874cb413` per addition history: frozen-C1 fixture attacks/reproduction harnesses, not successor gates (`Mo58Executor44.receipt.py:2-10,27-40`; `Mo58Connector59.attack.py:25-43`). No attack harness was executed.
* r59 `fixtures-c1/*/tools/*.py` are copied fixture payloads, not additional lane tool definitions.

The committed wave trees contain 47 `.py`/`.sh` candidates excluding those fixture copies: 19 counters, one independent source verifier, two omitted independent checkers, one isolation wrapper, two split selftests, ten controls/data drivers, ten builders, two attack/reproduction harnesses. The separate lane-tool addition history identifies six tools in the interval; five are in the manifest and runway is missing.

## Commands and observed receipts

Read-only provenance commands used (absolute repo; no git mutation):

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %s' --name-status 4f266ef2..325f7e639916fcbc77fa2ec7475951a1b86bb1cb -- 'tools/*' '.ufo/waves/round-5*/*.py' '.ufo/waves/round-60/*.py'
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --diff-filter=A --format='%H %s' --name-only 4f266ef2..325f7e639916fcbc77fa2ec7475951a1b86bb1cb -- .ufo/waves/round-52/check-history-rows.py .ufo/waves/round-52/r39-conform-selftest.sh .ufo/waves/round-54/checks/receipt-stage.py .ufo/waves/round-55/checks/selftest-c1.py .ufo/waves/round-55/checks/selftest-c2.py tools/mori-commit-runway.py
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 325f7e639916fcbc77fa2ec7475951a1b86bb1cb .ufo/waves/round-52 .ufo/waves/round-53 .ufo/waves/round-54 .ufo/waves/round-55 .ufo/waves/round-56 .ufo/waves/round-57 .ufo/waves/round-58 .ufo/waves/round-59 .ufo/waves/round-60
```

Python in the tool kernel filtered the committed tree for `.py`/`.sh`, read the frozen manifest with `git show`, compared membership, and checked every manifest landing/path pair with `git cat-file -e`. Observed output:

```text
manifest_count 25 unique_paths 25
OMITTED .ufo/waves/round-52/check-history-rows.py in_manifest False worktree_equal True
OMITTED tools/mori-commit-runway.py in_manifest False worktree_equal True
OMITTED .ufo/waves/round-54/checks/receipt-stage.py in_manifest False worktree_equal True
FROZEN_MANIFEST_EQUALS_WORKTREE True
25/25 manifest landing/path pairs: landing_resolves True
```

Entering-revision sha256 receipts for the three omissions (working-tree bytes equal committed bytes):

```text
a7e7a3cca942b7f3dd2054492b7b1b689696da7f5ad7b7303bc880ce0d734a54  .ufo/waves/round-52/check-history-rows.py
b3c123400f41a8e8d62e678d81175956c68a9735643a8a3cd09975666be1ffe4  tools/mori-commit-runway.py
5eae299b12c096b2c98a8ee74ae9639dcaba0b2d7cb3fee8fd8559948b1bd3ac  .ufo/waves/round-54/checks/receipt-stage.py
```

## Residual risk and verification gaps

* LSP unavailable: requesting `xd://lsp` returned `No such tool` and its mounted-device inventory contained no LSP. References/caller/definition checks therefore used literal search plus direct source inspection; searches are not semantic proof. No diagnostic server result is claimed.
* No counter, selftest, host probe, fixture, clone, service or alternative runtime was invoked. Old pass/fail lines above are explicitly committed historical receipts, not new executions. This audit does not certify the instruments' implementation correctness or current claim measurements.
* Gate/probe terminology remains a classification boundary, particularly for tools with selftest-only pass/fail modes. F1 does not depend on F2: runway's existing gate label and the two independent checker predicates independently establish omissions.
* No claim is made about canonical runtime identity, rerouting, saturation, or resume continuity; these paths are outside this manifest-inventory assignment.
* Only this report and the seat scratch directory were written. TMPDIR was set in the kernel to `/fast/scratch/hyaku/mori-r61/Mo61Reviewer07`; no heavy work or temporary evidence files were created. No tools installed or updated; no production, registry, counter, contract or VCS state changed.

Self-evaluation: accuracy 4/5 (F2 is taxonomy-based, disclosed); completeness 4/5 (committed executable inventory complete for named wave trees/tool additions; no runtime diagnostics); clarity 4/5 (auxiliary enumeration adds length); actionability 5/5 (three exact missing paths, full landing IDs and source predicates); conciseness 4/5 (inventory retained for auditability). Overall 4.2/5. Highest-impact improvement would be an authoritative gate/probe taxonomy ruling for F2, not a frozen-contract amendment. Would the user agree: likely, because F1 is independently evidenced and interpretation limits are explicit.
