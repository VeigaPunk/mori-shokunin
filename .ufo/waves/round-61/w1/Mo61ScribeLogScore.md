# Mo61ScribeLogScore — round-61 LOG/SCORECARD drafts

## Scope, axes and limits

Axes: C1 calibration (5), C2 freshness (5), C3 operability (7); entering scores otherwise coverage 6, depth 5, adjacency 6. Frozen contract read first. Drafts follow the r58–r60 pattern: revision/score paragraph, claim account or five-column table, wave/frontier account. After-cells remain **AT-DATA pending**. No admission, scalar change, completed settlement or provider-death inference is asserted.

Only this report was written in the lane. LOG.md, SCORECARD.md, SKILL.md, corpus, tools, registry and frozen instruments were not edited. Additional counter/selftest/fixture execution exceeded this seat's draft-only remit; its observed outputs are disclosed below, not substituted for canonical judgment. Fixture Git mutations occurred only under the seat scratch directory; no lane/fleet Git mutation was performed. One empty-owner fixture did not record the required pre-mutation toplevel assertion. No tools installed or updated; no pacman invocation.

## Evidence and provenance

Absolute lane prefix for references below: `/home/vgpnk/Projects/shokunin/mori-shokunin/`. Template surfaces: LOG.md:2975–3065 and SCORECARD.md:2923–3006. Contract: `.ufo/waves/round-61/contract.md:14–24,32–112`. Before receipts: `.ufo/waves/round-61/evidence/control-c{1,2,3}-do-nothing.txt:1–2`.

Entering revision: `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`. Freeze: `7370a731abcafc4c803111de7c22cd6264d63be1`. At observation HEAD was the freeze; dispatch artifacts were untracked. No data revision was observed.

Disk guard command: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`; first reading scratch free 356.3G (56% used), later 349.3G (57%). Scratch: `/fast/scratch/hyaku/mori-r61/Mo61ScribeLogScore/`; TMPDIR was set under it for most runs, but not explicitly set in every fixture command. Scratch is removed after recording this report.

Counting-command executions used the absolute script paths below, `--repo /home/vgpnk/Projects/shokunin/mori-shokunin`, and `--scratch /fast/scratch/hyaku/mori-r61/Mo61ScribeLogScore/<run>`:

- `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py REV --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r61/Mo61ScribeLogScore/c1def`
- Corresponding count-c2.py/count-c3.py commands used the same repo and scratch convention.
- For C1 entering-control reproduction, additionally: `--manifest /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/gate-manifest.json`.

Observed results:

| Measurement | Outcome |
|---|---|
| C1 entering, explicit absolute manifest | Byte-equal to committed control, rc 1 |
| C1 entering, default manifest | `C1=unmet gates=0 registered=0 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=manifest_unreadable rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc 1 |
| C2 entering | Byte-equal to committed control, rc 1 |
| C3 entering, explicit lane repo | Byte-equal to committed control, rc 1 |
| C1 freeze | `C1=unmet gates=25 registered=0 missing=25 thin=0 dup=0 unres=0 noselftest=0 noowner=0 …`, rc 1 |
| C2 freeze | `C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=7370a731abcafc4c803111de7c22cd6264d63be1`, rc 1 |
| C3 freeze, explicit lane repo | `C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=none rev=7370a731abcafc4c803111de7c22cd6264d63be1`, rc 0 |
| C1/C3 `--selftest --scratch <seat-run>` | Receipts byte-equal: 6/0 and 8/0, rc 0 |
| C2 `--selftest --scratch <seat-run>` (default floor 40) | `case good: ok=False want=True FAIL failed=['pointer_floor:6<40']`; `C2_SELFTEST pass=9 fail=1`, rc 1 explicitly captured |
| C2 `--selftest --floor 0` and `--floor 6` | Both byte-equal to committed 10/0 receipt, rc 0 |

Some exploratory pipelines printed the downstream `tail`/`cut` exit status as `rc=0`. These do **not** establish the Python process status. The table uses direct or file-captured statuses; default C2 selftest rc 1 was separately captured without a pipeline.

Receipt SHA256s:

```text
3b4555bc943d10bfc715af578985d2b82bab1d4fbe1862d4a07c9a64f3f7dfa8 control-c1-do-nothing.txt
59152a3f4e6da238d498dba6f423789e881b7cffe91a51e07aa5e15550e5abc0 control-c2-do-nothing.txt
0f5c112bf671bc1ae313d964698b9ee10faf838cc24b0b8618e3a182ce395e4e control-c3-do-nothing.txt
cbc4d29bb548f22facf7693e2c056637d714c85a38783dc978d88f1358578bf9 selftest-c1.txt
6cc5e04fcd153a8bdcf1719ebff2ed0c04cd0e7ace56a83cfe3b81c7b7efd1aa selftest-c2.txt
e01d3f23fca4864ae5fd88324998843ee99a49968af0dcc26bc0954a1fb3522e selftest-c3.txt
```

## LOG.md draft

```markdown
## Round 61 — Mori (L1 MoriR61): C1 calibration gate registry, C2 freshness PSI v7.3 recheck, C3 operability boundary v2 (AT-DATA pending)

Entering `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`; freeze
`7370a731abcafc4c803111de7c22cd6264d63be1` (two pre-seat amendments recorded in
the contract). Dispatch revision and data revision: AT-DATA pending. Scores
entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired tie depth/freshness/calibration at 5. C1 targets
calibration, C2 freshness, C3 operability; no scalar score change claimed.

Frozen claims (the contract records fresh-start review of r58–r60 rejected closures;
controls committed before seats scored):
- C1 calibration: 25 manifest paths from rounds 52–60 receive exactly one
  non-superseded, eight-cell gate-registry row in SKILL.md, including self-test and
  owner cells and a resolving entry path. Entering control: `C1=unmet gates=25
  registered=0 missing=25 thin=0 dup=0 unres=0 noselftest=0 noowner=0 …`, rc 1
  (`.ufo/waves/round-61/evidence/control-c1-do-nothing.txt`). After: AT-DATA pending.
- C2 freshness: `psi-v73-recheck-r61.md` rechecks the enumerated PSI pointers against
  six pinned v7.3 copies; floor 40, quotes distinct and located, ≥4 copies cited,
  mined SOURCES rows bound to the ledger. Entering control: `C2=unmet pointers=47
  rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0
  failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc 1
  (`.ufo/waves/round-61/evidence/control-c2-do-nothing.txt`). After: AT-DATA pending.
- C3 operability: boundary v2 checks the pinned r60 hole, r61 repair, unpinned-blob
  refusal, expect-table pin and live r61 counter pins. Entering control:
  `C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL
  cases=5 failed=r61 counters absent or sha pin mismatch at rev
  rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc 1
  (`.ufo/waves/round-61/evidence/control-c3-do-nothing.txt`). After: AT-DATA pending.

Control reproduction notes: C1's 25-path receipt reproduces with an explicit
absolute `--manifest` because the manifest is absent from the entering tree.
C2/C3 controls reproduce with explicit lane `--repo`. C1/C3 selftest receipts
reproduce 6/0 and 8/0. C2's 10/0 receipt reproduces at `--floor 0`/`--floor 6`;
default-floor selftest instead reports 9/1, rc 1. This discrepancy is reported,
not amended. Freeze-time observations are not after-cells: C1 registered=0,
C2 entry_absent, C3 measured met with explicit lane `--repo`.

Admission and capability-row decision: AT-DATA pending; no admission asserted.

Wave w1: one v2 wave, 64 dispatch entries; reviewer 9, critic 7, mutation-tester 8,
sentinel 3, executor 12, scribe 13, scout 5, connector 2, revenger 3, simplifier 2.
Reviewer/critic/mutation-tester/sentinel share 27/64 = 42.2%. Directive markers
observed in 64/64 task strings. Final settlement/report/empty-output counts:
AT-DATA pending; a dispatch entry is not evidence of completed execution.

SOURCES count at observation: 337 rows. The census executor report records validator
success; end census, source-row disposition, lesson Gate/Mistakes, assimilation,
capability admission and final wave findings: AT-DATA pending. No scalar movement
or completed frontier movement is inferred from the frozen contract alone.
```

## SCORECARD.md draft

```markdown
## Round 61 — C1 gate-registry calibration, C2 PSI v7.3 freshness, C3 boundary v2 operability (AT-DATA pending)

Entering `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`; freeze
`7370a731abcafc4c803111de7c22cd6264d63be1` (two pre-seat amendments recorded in
the contract). Dispatch/data revisions: AT-DATA pending. Scores entering: coverage 6,
operability 7, depth 5, freshness 5, calibration 5, adjacency 6. Lowest tie
 depth/freshness/calibration at 5. C1 targets calibration, C2 freshness, C3 operability.
No scalar score delta claimed; after-grades await closure.

| Claim | Axis | Counting command | Before | After / verdict |
|---|---|---|---|---|
| C1: all 25 frozen manifest paths from r52–r60 carry exactly one non-superseded eight-cell SKILL.md gate-registry row, self-test/owner cells, and resolving entry paths | calibration 5 | `python3 .ufo/waves/round-61/count-c1.py R --repo LANE --scratch SCRATCH` (entering-control replay additionally uses `--manifest ABS_MANIFEST`) | Entering control: `C1=unmet gates=25 registered=0 missing=25 thin=0 dup=0 unres=0 noselftest=0 noowner=0 …`, rc 1 (`.ufo/waves/round-61/evidence/control-c1-do-nothing.txt`; displayed failed-list excerpt, full receipt retained) | AT-DATA pending |
| C2: PSI v7.3 recheck ledger covers the enumerated v7.2 pointers (floor 40), with distinct located quotes, ≥4 pinned copies and mined/used-by source-row binding | freshness 5 | `python3 .ufo/waves/round-61/count-c2.py R --repo LANE --scratch SCRATCH` (default floor 40 retained) | Entering control: `C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc 1 (`.ufo/waves/round-61/evidence/control-c2-do-nothing.txt`) | AT-DATA pending |
| C3: boundary v2 demonstrates the pinned r60 hole/r61 repair, unpinned-blob refusal, expect-table pin and live r61 count-c1/count-c2 pins, with conjunctive met | operability 7 | `python3 .ufo/waves/round-61/count-c3.py R --repo LANE --scratch SCRATCH` | Entering control: `C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc 1 (`.ufo/waves/round-61/evidence/control-c3-do-nothing.txt`) | AT-DATA pending |

Command notation: LANE is `/home/vgpnk/Projects/shokunin/mori-shokunin`;
ABS_MANIFEST is its `.ufo/waves/round-61/gate-manifest.json`; SCRATCH is the
executing seat's directory under `$HYAKU_SCRATCH/mori-r61/`. Before receipts remain
unchanged. Observed selftests: C1 6/0, C3 8/0; C2 10/0 receipt reproduces with floor
0 or 6, whereas default floor 40 yields 9/1 rc 1. The discrepancy is unresolved.

Wave w1: 64 dispatch entries, attack-role share 27/64 = 42.2%; completion and
settlement counts AT-DATA pending. Dispatch metadata is not completed-work evidence.

Admission, final axis observations, census-end and capability-row decisions:
AT-DATA pending. The contract permits a capability row only after a met run in
the round's report; none is inserted by this draft. No successor counter or
contract changes are proposed; frozen findings are reported separately.
```

## Findings and gate limitations

1. **C2 default selftest differs from the green receipt.** `.ufo/waves/round-61/count-c2.py:38,183–184,201,276,291–297`: floor default 40 is passed into synthetic six-pointer tests. Direct default execution yields `pass=9 fail=1`, rc 1; floor 0 and 6 yield receipt-byte-equal 10/0. This does not establish which invocation originally produced the receipt. No counter amendment proposed.
2. **C1 entering-control replay needs external manifest bytes.** `count-c1.py:206–217`: absolute existing manifests are read from disk; otherwise manifest is read from measured revision. Default entering replay gives manifest_unreadable/gates=0; absolute current manifest gives committed-receipt-byte-equal gates=25. Record the invocation rather than treating these as the same command.
3. **C3 repo default explains an observed conflict.** `count-c3.py:271,281–283`: repo defaults to cwd. At freeze with explicit lane repo, C3 met rc 0; from fleet cwd without `--repo`, C3 unmet with r60hole/livepins FAIL rc 1. This establishes scope dependence, not a proof over every revision or a canonical judgment about either report.
4. **C1 superseded-only fallback.** `count-c1.py:96–103`: if no non-superseded hits remain, `hits[0]` is selected. A scratch single-path fixture whose sole row had name `superseded gate (r52)` and scope `superseded by r60` returned `C1=met gates=1 registered=1 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 failed=none`, rc 0. Contract:38 requires one non-superseded row. Fixture revision `797c693b772940935916a05ef1aa41a951492dee` was scratch-only and is deleted; output is preserved here.
5. **C1 substring entry match.** `count-c1.py:62–69`: a scratch row entry `tools/x.py.bak` registered manifest path `tools/x.py`, which independently existed. Result same met/counts as finding 4, rc 0; scratch revision `36addbd28a9210219ae0f4734372d04cb97a98e3`. Manifest-path resolution does not validate the decoy entry's executable.
6. **Self-test-cell text is not execution evidence.** `count-c1.py:108–113`: only `--selftest` substring is checked. The freeze bytes for round-57/count-c1.py, count-c2.py and verify-c2-source.py contain no `--selftest` token. Their positional CLIs read respectively one revision or two file arguments. A scratch row claiming a r57 count-c1 `--selftest` scored C1 met rc 0; running that purported selftest printed `C1=unmet rows=0 evidence=bad`. This shows the cell check is textual, not that every allowed cell must name that same executable. No change proposed.
7. **Owner field is checked through thin, not noowner.** `count-c1.py:75,104–107,127,214`: noowner initialized/printed but not incremented. Scratch empty-owner case yielded `thin=1 noowner=0 failed=thin:tools/x.py:owner`, rc 1. Owner rejection is observed; always-zero noowner is not independent owner evidence.
8. **C3 static self-audit limit, with an important kill qualification.** `count-c3.py:106–124,187–188`: static arm checks whether the matched met line contains `c1_ok`. Scratch-copy substitutions `met = c1_ok or True` and `met = True  # c1_ok computed but unused` each printed `C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e639916fcbc77fa2ec7475951a1b86bb1cb`, rc 0. **Neither is an all-tests-surviving mutant:** each mutant's selftest reported `C3_SELFTEST pass=5 fail=3`. Those pipelined selftest invocations did not capture Python exit status; only printed tallies are claimed. Frozen source itself computes `c1_ok = all(b.values()); met = c1_ok`. These probes show static-arm limits, not that frozen committed met is unconditional.
9. **Output shape differs from contract illustration.** Contract:71 names `rows_src=ok provenance=ok sources>=4`; count-c2 fmt:190–197 prints numeric sources and failure reasons, not those success tokens. C1/C3 fmt also include `failed=none`, absent from contract illustrative met lines. Whether exact equality or semantic token interpretation controls is left to the canonical judge.
10. **Manifest landing is not a freeze pin.** r60 manifest entries list initial landing `4d036fb0…`; r60 c3 SHA there is `546486571e13e151fdec240a32b85a5a4fb71c16440c81a38edb8da12829a5ba`, versus amended freeze `fabde06c…` at ac496c7c. Both can be true: initial landing and later freeze are different events. C1 counter does not inspect landing metadata. No contradiction is asserted solely from that distinction.
11. **Normal pin/format bounds.** All 25 manifest paths resolved at freeze; all six v7.3 copy hashes matched frozen PINS. A scratch commit adding `\n# trailing edit\n` to count-c1 changed livepins from ok to FAIL (not a one-byte edit). C3 cases=5 is a literal arm count, not a runtime test tally. C2 enforces 5–25 quote words and stated-location matching for moved/changed (`count-c2.py:137,148–159`), which must not be confused with broader prose allowances. These are observations, not new contract terms.

## Conflict preserved verbatim

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/w1/Mo61ExecC3Run.md` states:

> C3 does **not** meet on any requested revision. The freeze and entering outputs are byte-identical except for `rev`, and differ from the committed do-nothing control in the `r60hole` result and failure reason. Consequently, requested control equivalence and red-before behavior are falsified. Do not infer the C3 claim met.

This seat observed the explicit-lane-repo freeze met line and byte-equal entering receipt reported above, and reproduced the sibling's failure shape with fleet cwd/no `--repo`. The sibling's original cwd was not captured in its cited command; causation for that historical invocation remains [INFERENCE]. Preserve both reports for canonical judgment; no admission verdict is made here.

## Touched surfaces and artifacts

Artifact: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/w1/Mo61ScribeLogScore.md` (this file; drafts plus small receipts inline). Scratch cleanup follows writing; no fixture is durable evidence beyond the preserved outputs and transcript. Production integration, gate changes, canonical judging, commits/pushes/publication/deployment and final settlement are out of scope. No installs/updates to report.
