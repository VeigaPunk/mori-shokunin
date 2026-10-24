# ExeC2GateSelftest — append-only gate selftest at the measured revision

Seat: `L1-mori-r41-attempt2.ExeC2GateSelftest` (executor, leaf). Scope: run the append-only
gate selftest in an isolated sandbox at the measured revision, report every case outcome and
the final tally. The gate was not edited; no production file was written by this seat.

## Measured revision and sandbox identity

- Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin` (lane tip `7450722e5f3b4fc6df3d719386ed643af59630e3`, read only).
- Measured revision: `aa161e998eb22282e3d96ed2710bb0b39e5163de` — the revision recorded in
  `.ufo/waves/round-41/evidence/control-after.txt` (`mode=after revision=aa161e99...`).
- Sandbox: disposable detached clone `/tmp/mori-r41-c2-selftest-14cjym/repo`
  (`git clone --no-hardlinks`, then `checkout aa161e99`); `git rev-parse HEAD` in the clone
  returned `aa161e998eb22282e3d96ed2710bb0b39e5163de`; clone status clean before and after.
- Gate bytes are revision-invariant across the wave: `git rev-parse <rev>:tools/mori-sources-appendonly.py`
  is `887fd85d96fd97f99f1845090cda64cf5e084fa8` at `aa161e99`, at the freeze revision
  `d72ac167`, and at lane tip `7450722e`. Sandbox file `sha256 = 75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`.
  The measurement therefore holds for the frozen gate and for the lane tip alike.
- Interpreter: `/usr/bin/python3` = Python 3.14.8 (same binary family as the control receipts).
- Git identity: `_clean_env()`-protected read-only git calls only; the selftest's fixture repos
  live under `tempfile.mkdtemp(prefix="mori-sources-appendonly-selftest-")` and are removed by
  `shutil.rmtree` in `finally`. Nothing was written inside the clone or the lane.

## Exact command and output (unmodified gate)

```
$ cd /tmp/mori-r41-c2-selftest-14cjym/repo
$ /usr/bin/python3 tools/mori-sources-appendonly.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
EXIT=0
```

stdout is exactly the single tally line; stderr empty; zero `FAIL` lines; clone status after
the run: 0 modified paths.

## All case outcomes

The selftest prints only failures, so per-case attribution used an external, read-only harness
(`/tmp/r41-c2-percase.py`) that imports the sandbox gate, wraps its `_run_cli` to retain each
case's child-process `(code, stdout)`, and re-evaluates each observed output against that case's
own hand-written expectation using the gate's `SUMMARY_RE`/`TIMING_RE`. One CLI child per case,
22 distinct fixture repos (`case00..case08`, `dag00..dag05`, `r41dag00..r41dag06`); no case was
skipped. The harness's own selftest() call reproduced the same tally (`pass=22 fail=0`).

| # | fixture | case | exit | observed summary / timing |
|---|---------|------|------|---------------------------|
| 1 | case00 | clean history | 0 | `appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]` |
| 2 | case01 | mutable-only edit | 0 | `appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]` |
| 3 | case02 | immutable edit | 1 | `appendonly_violations=1 ids=[S001] ... round_changed=[S001]` |
| 4 | case03 | changed-back inside the round | 1 | `appendonly_violations=0 ids=[] ... round_changed=[S001]` |
| 5 | case04 | deleted row | 1 | `appendonly_violations=1 ids=[] deleted=[S002] ... round_changed=[S002]` |
| 6 | case05 | superseding row | 1 | `... superseded=[S001] ...`; `superseded_as_of=[S001] stale_supersede=[]` |
| 7 | case06 | supersede before edit | 1 | `... superseded=[S001] ...`; `superseded_as_of=[] stale_supersede=[S001]` |
| 8 | case07 | row reorder | 0 | `appendonly_violations=0` all lists empty |
| 9 | case08 | whitespace padding | 0 | `appendonly_violations=0` all lists empty |
| 10 | dag00 | side-branch superseder is stale | 1 | `... superseded=[S001] ...`; `superseded_as_of=[] stale_supersede=[S001]` |
| 11 | dag01 | merge does not fabricate an edit | 0 | `appendonly_violations=1 ids=[S001] ... superseded=[S001] round_changed=[]`; `superseded_as_of=[S001]` |
| 12 | dag02 | landing is the last edit commit | 1 | `... superseded=[S001] ... round_changed=[S001]`; `superseded_as_of=[S001]` |
| 13 | dag03 | never-edited superseded row is as-of | 0 | `... ids=[] ... superseded=[S001]`; `superseded_as_of=[S001] stale_supersede=[]` |
| 14 | dag04 | first-parent-lacks-path merge contributes no edits | 1 | `... ids=[S001] ... round_changed=[S001]`; `superseded_as_of=[S001]` |
| 15 | dag05 | linear delete-then-re-add is not an edit | 1 | `... superseded=[S008] ... round_changed=[S008]`; `superseded_as_of=[S008]` |
| 16 | r41dag00 | per-commit header map prevents fabricated changes | 0 | `appendonly_violations=0 ids=[] ... superseded=[S001]`; `superseded_as_of=[S001]` |
| 17 | r41dag01 | per-commit teaches map retains permuted superseder | 0 | `appendonly_violations=0 ids=[] ... superseded=[S001]`; `superseded_as_of=[S001]` |
| 18 | r41dag02 | discarded superseder is ineligible at R | 0 | `appendonly_violations=1 ids=[] deleted=[S002] superseded=[] round_changed=[]`; both timing lists empty |
| 19 | r41dag03 | discarded edit and superseder do not decide timing | 1 | `... ids=[] deleted=[S002] superseded=[] round_changed=[S001]`; both timing lists empty |
| 20 | r41dag04 | incomparable superseders, early date | 1 | `... ids=[S001] ... superseded=[S001] ...`; `superseded_as_of=[] stale_supersede=[S001]` |
| 21 | r41dag05 | incomparable superseders, late date | 1 | `... ids=[S001] ... superseded=[S001] ...`; `superseded_as_of=[] stale_supersede=[S001]` |
| 22 | r41dag06 | deleted/re-added superseder uses later ancestry landing | 1 | `... ids=[S001] ... round_changed=[S001,S002]`; `superseded_as_of=[S001] stale_supersede=[]` |

Per-case verdicts: 22 PASS, 0 FAIL. Every row also satisfied the expectation fields not shown
above (`deleted`, `superseded`, `round_changed`, `superseded_as_of`, `stale_supersede`,
`superseded_by` where declared), exit-code equality, one-summary-line/one-timing-line shape,
`violations == len(ids)+len(deleted)` arithmetic, and the per-id line grammar.

Harness tail: `AUDIT cases=22 pass=22 fail=0` (exit 0).

## Tally against the frozen target

- Observed: `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, exit 0.
- Contract C2 frozen target (line 25 of `.ufo/waves/round-41/contract.md`): `pass=22 fail=0`.
  **Met exactly**, and identical to the recorded after-receipt at `aa161e99`
  (`control-after.txt` line 100).
- Composition of the 22: 9 basic history cases + 6 r40 dag cases + 7 r41 dag cases
  (`_selftest_cases`, `_selftest_dag_cases`, `_selftest_r41_dag_cases`), enumerated and
  executed 22/22 as above.

## Discrepancy with the seat prompt

The seat text says "all 21 case outcomes". The measured gate has **22** cases at the measured
revision, the freeze revision and the lane tip (case-list lengths read from the gate module:
9 + 6 + 7 = 22; selftest tally `pass=22`). No case is conditional or skipped: 22 distinct
fixture repos were driven, one CLI child each. The prompt's 21 is a stale off-by-one in the
wave spec; the measured count and the frozen target both say 22, and the frozen target is the
binding value. No reconciliation edit was made (read-only seat).

## No-harm and retained evidence

- Gate file unmodified: blob `887fd85d...` before and after; sandbox clone `git status --porcelain`
  empty before and after; no file in the lane repo written by this seat other than this report.
- Selftest side effects confined to a `mkdtemp` root under `/tmp`, removed by the gate's own
  `finally`.
- Raw captures retained in the disposable sandbox: `selftest-raw.txt` (exact tally run),
  `percase-timing.txt` (full per-case rows incl. timing lines); harness source
  `/tmp/r41-c2-percase.py`. These are ephemeral `/tmp` paths; the durable record is the tables
  and quoted output above.
- Tool installs/updates: none (no package manager invoked).

## Risks / residual boundaries

- This run measures the gate's own fixture matrix, not the live lane line. The live lane-line
  claims (36 as-of ids, no stale ids, `stale=[S069]` at `e37dcc6`, the dag-* fixtures) are
  separate C2 control/executor items and are not asserted here.
- The selftest's expectations are hand-written inside the gate; this seat re-verified the
  observed outputs against those expectations but did not independently re-derive the expected
  values from the predicate text. Mutation seats cover the arm-sensitivity side.
- Interpreter-bound: Python 3.14.8 (`/usr/bin/python3`). Different interpreters were not tested.
- Residual named by the gate's own predicate (multiple incomparable edits walk-order) is not
  exercised by any of the 22 cases; that remains a documented residual, not a fixed property.

## Blockers

None. The assignment completed end-to-end in the isolated sandbox.
