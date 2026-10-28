# Mo59Critic25 — attack on the C2 drift arm

**Question assigned:** does `exit-1-on-r53` prove discrimination, or just
extra-key intolerance? Verdict: **counterexample found** — the arm is
under-instrumented; it proves neither. It certifies "some r53-correlated
nonzero exit" and would pass mutants that discriminate on the wrong axis
entirely. The pinned tool itself *is* member-extra-key intolerant (proven
below), but the counter's `drift` token is weak evidence for that fact.

Scope: read-only probes; tool + counter bytes at entering `2b9f0397` /
freeze `60b3a76a` were copied into scratch and never modified.

## The arm under attack

`count-c2.py:251-263`: materializes `.ufo/waves/round-53/w1-results.json`
into `$scratch/real2/round-53/w1-results.json` (line 255), then
`drift_ok = p.returncode != 0` (line 260). stdout is never read; no verdict
or reason attribution; any nonzero code — including exit 2 usage/crash —
satisfies the arm. Contrast the scan arm (lines 235-246), which parses
stdout and asserts `verdict == SETTLEMENT_SCAN_OK`.

## Confounds: r53 differs from r54–r58 on ≥3 independent axes

```
r53 top keys: lane,note,outputs_recovered,results,round,seats,settled_by,spawned,wave
r54–r58:     lane,results,round,seats,wave
r53 members:  67x (agent,name,note,output,report_file); note = non-null str x67; seats=67
r54: 74x (agent,name,note,output); note=None x74
r55–r58: 64x same; note=None
```

The drift file carries (a) member extra key `report_file`, (b) four extra
top-level keys, (c) non-null string `note`s, (d) odd seat count, (e) the
substring `round-53` in its materialized path. A nonzero exit on this file
is attributable to any subset of these — the arm does not vary any factor.

## Decisive mutants — both pass the frozen arms

Mutants = pinned tool + one predicate; replayed through the counter's
verbatim arm logic (same materialization paths, same subprocess calls):

| tool | scan_arm (r54–58 → OK, members==seats) | drift_arm (r53 → rc≠0) |
|---|---|---|
| pinned `mori-settlement-scan.py` | True | True |
| **M1**: `+if "round-53" in str(path): return fail("drift_path")` | **True** | **True** |
| **M2**: `+if m["note"] is not None: fails.append("note_not_null")` | **True** | **True** |

M1 performs **zero schema discrimination** — a filename heuristic passes
`drift=ok`. The counter itself plants the confound at `count-c2.py:255`
(`real2/round-53/`). M2 discriminates on the wrong schema axis (note
nullability, not member key-set): r53's notes are non-null, r54–58's are
null, so it too satisfies both arms. A pure `exit 1` unconditional mutant
fails only because the scan arm kills it — the drift arm alone cannot.

(One candidate mutant is already dead: byte-grep `report_file` fails the
scan arm because r58 member[60].output contains `"report_files_written"`.
Incidental payload coverage, not designed discrimination.)

## What the pinned tool actually does (probes, all reproducible)

Copies of the r53/r58 artifacts mutated in scratch, run through the pinned
tool (`sha 4c04bf21…`):

| probe | result |
|---|---|
| r53 unmutated | rc=1, `SETTLEMENT_SCAN_FAIL`, 67 reasons — **all** `member[i]:extra_keys=report_file` |
| **A**: r53 minus member `report_file`, all 4 top-level extras kept | rc=0, `SETTLEMENT_SCAN_OK` |
| **B**: r58 + `report_file` on member[0] | rc=1, `extra_keys=report_file` |
| **C**: A + `seats=66` | rc=1, `seats_mismatch` |
| **D**: A + duplicated member name | rc=1, `duplicate_names=…` |

So: the tool **is** genuinely intolerant of member extra keys (A/B isolate
it) and localizes reasons well. But it **silently tolerates** the other
three real r53 drift axes — top-level extras, non-null notes — since
`scan_file` never enumerates top-level keys (`mori-settlement-scan.py:55-68`)
and only counts non-null notes (`:99-100`). The arm label "drift" overclaims:
what is measured is member-key-set equality on one file.

## Fixable defect vs tradeoff

Fixable defect, not a canonical-judge tradeoff. The arm can be made honest
without changing the tool or the claim.

**Smallest safe correction** — replace the single `returncode != 0` check
with a 3-fixture battery + reason attribution:

1. **P1 positive control** (kills M1 *and* M2): r53 minus member
   `report_file`, top-extras kept, materialized under a `round-53`-free
   filename → MUST exit 0. (M1 fails: path clean but it has nothing to
   reject on r54–58 → actually M1 *passes* P1; refine: materialize P1 under
   `round-53/` too — then M1 fails it, M2 fails it via non-null notes.)
2. **N1 cross-injection**: r58 + `report_file` → MUST exit 1 **and**
   `failures[].reasons` contains `extra_keys=report_file` (parses stdout;
   locks out exit-2 crashes and wrong-axis rejections that can't produce
   the reason string).
3. **N2 reason attribution on r53 itself**: require verdict
   `SETTLEMENT_SCAN_FAIL` plus ≥1 `extra_keys=report_file` reason — proves
   the nonzero exit on r53 is *the* extra-key check, not a co-traveling
   predicate.

P1-under-round-53-path + N1 + N2 together exclude every demonstrated
mutant class while leaving the pinned tool passing (verified: probes A/B
above are exactly P1/N1 and the pinned tool passes both).

## Evidence commands

- Probes/mutants: `python3` heredoc under
  `$HYAKU_SCRATCH/mori-r59/Mo59Critic25/` (tool.py = byte copy of
  `tools/mori-settlement-scan.py`; mutants = `str.replace` insertion, asserted
  non-identical).
- r53 reasons: `tool.py r53.json` → 67 × `member[i]:extra_keys=report_file`.
- Tool selftest via counter's invocation: `SETSCAN_SELFTEST pass=10 fail=0`.
- Scratch cleaned before yield; lane untouched (`git status` clean).

## Impacted axes

- **C2 depth**: `drift=ok` token certifies less than the contract's scan-arm
  sentence (contract:77-79) implies — "r53 MUST scan FAIL" holds, but the
  measurement is attribution-blind. The 12 hostile trees exercise
  `eval_entry` only; scanner discrimination has no hostile-tree coverage.
- **C1 calibration**: not implicated.

## Assimilation / other

Assimilation: none. Report only; no production, registry, or VCS writes.
