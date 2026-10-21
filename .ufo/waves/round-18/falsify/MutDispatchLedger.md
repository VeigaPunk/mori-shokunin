# Dispatch-ledger mutation probe — round 18, wave 2

## Scope and axes

Advisory mutation evidence for C3 operability; not a round verdict or an integration decision.
Attacked revision: `e2bfbd6f8dccc51fc06455efc41f720301112dd4`.
All source citations below refer to that revision unless a wave reading is named.

Axes: **frozen-contract sensitivity**, **single-point isolation**, **exact-byte restoration**, and **bounded, clone-local execution**. Eight requested mutants were applied separately to the assigned `MutDispatchLedger` clone. None was retained. No subagents or other runtime were invoked.

**Observed result: 5 killed, 3 survived, 0 inconclusive.** Each mutant had its own pristine, mutated, and restored selftest invocation: 24 detector runs total. All eight pristine and all eight restored runs passed 11/11. Survivors are coverage findings; they do not change the frozen contract.

## Authority and attacked reading

- `.ufo/waves/round-18/contract.md:39-43,66-69`: C3 dispatch binding and failure-capable conditions; `:47-53` defines selftest and return-code behavior.
- `.ufo/waves/round-18/frozen/c3-ledger-format.json:4,19`: canonical UTF-8 JSON uses `ensure_ascii=False`, `sort_keys=True`, compact separators; digest, byte count and task count must match the dispatch **at the measured revision**. Attempts must be contiguous, a unique started/partial row must be final, and a started row's returned-id count must match the task count.
- Read the named C1 policy/population and C2 register for frozen context; no C1/C2 finding or measurement is claimed here.
- `.ufo/waves/round-18/draft-verdicts.md:10` provisionally calls the C3 capability verified while distinguishing attempt populations. This probe narrows what its selftest establishes; it does not remeasure those populations or contradict an observed ledger digest.
- `.ufo/waves/round-18/out-of-metric-triage.md:8-16` was read as required. This report introduces no privacy-triage disposition and retains no other-session material.

## Detector and execution record

Working directory for every command:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger`.

The following exact command, bounded to 45 seconds by the command tool, was executed three times per mutant in pristine → mutated → restored order. All runs completed within that bound; no background execution was requested.

```sh
/usr/bin/sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger/tools/mori-dispatch-ledger.py && /usr/bin/env TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger/.scratch GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 /usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger/tools/mori-dispatch-ledger.py --selftest
```

The tool's selftest creates throwaway Git fixture repositories under that TMPDIR and removes its temporary directory on exit (`tools/mori-dispatch-ledger.py:413-445,491-496`). Its Git setup uses `git -C <sandbox>` with isolated configuration (`:347-358,376-391,428-442`). Those selftest-internal sandbox writes are the authorized VCS exception; no mutating VCS command was issued against the clone, lane, or fleet.

Additional executed read-only identity commands, each exit 0:

```sh
/usr/bin/sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger/tools/mori-dispatch-ledger.py && /usr/bin/git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger cat-file -p HEAD^{commit}
/usr/bin/git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger rev-list --max-count=1 HEAD
```

The latter returned the full attacked revision above. The former returned the pristine SHA-256 below and the commit object; commit identity fields are not reproduced.

Each selftest arm checks a subprocess exit code and presence of its expected finding ID, rather than only searching for a failure-shaped message (`tools/mori-dispatch-ledger.py:394-410`). The observed stdout in the table below is the selftest's aggregate output, not a separately captured per-fixture verification result.

## Mutants, expected detectors, and actual outputs

`P` in the execution table means the exact stdout `SELFTEST mori-dispatch-ledger PASS 11/11`, exit **0**. Every pristine and restored column represents a distinct execution, not reuse of a neighboring mutant's run.

| ID | Single-point mutation in the assigned clone | Expected detector under the frozen rule | Pristine | Mutated stdout; exit | Restored | Verdict |
|---|---|---|---|---|---|---|
| M1 | `tools/mori-dispatch-ledger.py:154`: change `ensure_ascii=False` to `ensure_ascii=True` in payload serialization only | A non-ASCII payload with an independently frozen digest/UTF-8 byte count should expose the canonicalization change; no such current arm | P | `SELFTEST mori-dispatch-ledger PASS 11/11`; **0** | P | **Survived** |
| M2 | `:155`: delete only the payload serializer's `sort_keys=True` argument | An insertion-order-varied multi-key task with an independently frozen canonical digest should fail the unsorted implementation; no such current arm | P | `SELFTEST mori-dispatch-ledger PASS 11/11`; **0** | P | **Survived** |
| M3 | `:234-235`: delete the SHA-256 comparison and its mismatch reason; payload byte-length and task-count checks remain | `tampered-payload-byte` and `wrong-digest`, each exit 1 with `PAYLOAD_SHA256_MISMATCH` | P | `SELFTEST mori-dispatch-ledger FAIL 9/11 failed=tampered-payload-byte,wrong-digest`; **1** | P | **Killed** |
| M4 | `:288`: replace `index != len(ledger)` with `index > len(ledger)`, thereby accepting a started row before the last row | `started-not-last`: exit 1, `STARTED_NOT_LAST` | P | `SELFTEST mori-dispatch-ledger FAIL 10/11 failed=started-not-last`; **1** | P | **Killed** |
| M5 | `:295`: replace the predicate with `if not _valid_int(expected_count):`, ignoring the row's `started_ids` | `started-ids-mismatch`: exit 1, `STARTED_IDS_MISMATCH` | P | `SELFTEST mori-dispatch-ledger FAIL 10/11 failed=started-ids-mismatch`; **1** | P | **Killed** |
| M6 | `:266`: remove only `or observed_attempts != expected_attempts`, allowing integer attempt gaps | `non-contiguous-attempt`: exit 1, `ATTEMPTS_NONCONTIGUOUS` | P | `SELFTEST mori-dispatch-ledger FAIL 10/11 failed=non-contiguous-attempt`; **1** | P | **Killed** |
| M7 | `:224`: replace the missing-digest reason append with `pass`, treating a missing-digest row as bound | `legacy-row`: exit 1, `LEGACY_ROW_UNBOUND` | P | `SELFTEST mori-dispatch-ledger FAIL 10/11 failed=legacy-row`; **1** | P | **Killed** |
| M8 | `:231`: prefer the dispatch file in the working tree instead of its measured-revision blob; retain the original committed-read path when the working-tree file is absent | A committed-clean dispatch with a subsequently changed working-tree payload, verified at the unchanged revision, should remain clean; no such current arm | P | `SELFTEST mori-dispatch-ledger PASS 11/11`; **0** | P | **Survived** |

M8 replaced exactly one assignment expression with:

```python
dispatch = json.loads((Path(repo) / safe_path).read_text(encoding="utf-8")) if (Path(repo) / safe_path).is_file() else _read_committed_json(repo, rev, safe_path, "DISPATCH_PATH_UNAVAILABLE")
```

This is specifically a **working-tree-preference** mutant. The absent-file fallback preserves the existing missing-dispatch error arm, avoiding an unrelated uncaught-file-error kill. It does not claim to change `bind`; only verification's dispatch acquisition was mutated.

M3 is the requested byte-count-only payload comparison defect, with the independent task-count validation intentionally left intact. M7's aggregate output establishes that the named legacy arm detected the mutant; it does not by itself identify whether that arm's exit-code assertion, finding-ID assertion, or both failed.

## Hash and restoration evidence

Pristine source SHA-256, denoted **H0**:

```text
4d8c7bf55b142569750f909ab3e9f7ef261d6d99672c55413027746c02c427b4
```

For every row below, the hash was emitted by `sha256sum` immediately before that stage's detector. Every mutated hash differs from H0. Every restoration returned exactly to H0 before its successful restored detector.

| ID | Before mutation | Mutated source SHA-256 | After exact restoration |
|---|---|---|---|
| M1 | H0 | `47b4f2850602e2eb2f009e933966525fc9a85b323e6d35674e3037e1f6302ab0` | H0 |
| M2 | H0 | `bcdfefbe2bce079156253f27fb87c04fd502dcb73f2639807c2260e2c68d3a7a` | H0 |
| M3 | H0 | `391cc70579757360b4b80a9e98c44e5e7dc27fb67bfd4213d180c0c7b784361e` | H0 |
| M4 | H0 | `0c7962b18c0185d2f6e09d029a3e64d1f188f34848bae398ddad5ae97a4b797f` | H0 |
| M5 | H0 | `d19c55ea54c5b5a977ad36300e2b4f6aa3658779d36cfc417eefb48bd6d8c354` | H0 |
| M6 | H0 | `cf104fd672923192869c2b3f1077fe1108cb7a0e7b4469257d169668dab04062` | H0 |
| M7 | H0 | `578d28d7d5ce36a5246655d2605c1d1940e10557e2ee7f765ade09aaeea87d6c` | H0 |
| M8 | H0 | `f4c8c35e892bde0958ede1a9d33b077887f2cc6555e2816797d829565d9e39fd` | H0 |

All source edits and inverse restorations used the surgical edit tool on the assigned clone only. There were no detector setup failures, timeouts, or failing pristine runs. No source edits followed M8's restoration.

## Missing arms and limits of the evidence

1. **Independent canonical UTF-8 oracle — demonstrated survivor M1.** The selftest's source payload is ASCII and its expected identity comes from the implementation under test (`tools/mori-dispatch-ledger.py:447-449`). A non-ASCII fixture alone would still share that oracle unless its expected digest and byte length were fixed independently. The present 11/11 result does not protect the frozen `ensure_ascii=False` requirement.
2. **Independent recursive key-order oracle — demonstrated survivor M2.** The task object has only one key (`:447`), and fixture files are themselves serialized with sorted keys (`:379-385`). There is no noncanonical nested insertion-order fixture checked against an independent canonical digest. The current suite does not protect `sort_keys=True`.
3. **Revision versus working-tree isolation — demonstrated survivor M8.** Every fixture writes and commits its dispatch, then verifies `HEAD` without a later working-tree edit (`:376-391,394-397,491-495`). It therefore supplies the same payload through both sources. The missing-dispatch arm (`:487-489`) tests absence, not source authority. No current arm changes the worktree after committing, removes a still-committed worktree dispatch, or distinguishes an older measured revision from current worktree contents.
4. **Other visibly absent arms, not additional mutation results.** The 11-case enumeration (`:452-489`) has no dedicated `PAYLOAD_BYTES_MISMATCH` or `TASKS_COUNT_MISMATCH` case despite the independent checks at `:236-239`; it also has no successful final-partial case. `bind` is not exercised by the selftest subprocess command (`:397`). These are source-observed omissions only; no survival or failure is claimed for unrun mutations of those behaviors.

No production fix, test expansion, integration, C3 acceptance ruling, or change to the contract was made. The missing arms are coverage findings for the integration owner, not permission to weaken a requirement.

## Scope accounting

Actual execution was limited to the recorded source-identity commands and the assigned tool's 24 selftests. Relevant skills, frozen inputs, wave readings, and the assigned clone's source/agent instructions were read using file tools. Source was temporarily changed only in the assigned clone; the only persistent handoff write is this report. No lane checkout tool source or sibling clone was modified. No fleet scripts/templates, manifests, state, runtime/user configuration, transcripts, or credential files were opened or modified. No host-service or live-journal command, package transaction, install, or upgrade was performed. These statements describe the actions taken, not a claim that later clean state proves the absence of prohibited actions. Tool install/update record: **none**.
