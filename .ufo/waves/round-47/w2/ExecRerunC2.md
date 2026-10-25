# ExecRerunC2 — round 47 wave w2 report

Seat: ExecRerunC2 (leaf). Attack: C2 depth claim (P-C2) at landed tip T=68d66ca53d89be5c34a62f46af7c37449d9f9b63, re-run with the frozen counter `.ufo/waves/round-47/count-c2.py`, compared against receipt `evidence/after-c2.txt`; then counter-run at E=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 and freeze F=63eecf2738db96f46b0bd02b1b2dfd66787493d0 to confirm the before state is not reachable by doing nothing.

## Verdict

**C2 claim HOLDS at T, under the frozen counter bytes.** Selftest passes 13/13. Both do-nothing controls (E, F) stay unmet with the failure lists the contract predicts; the before state is not reachable by doing nothing.

## Setup / identity (observed)

- `git -C <lane> rev-parse HEAD` → `68d66ca53d89be5c34a62f46af7c37449d9f9b63` (HEAD = master = T).
- `git -C <lane> rev-parse 2d85e33d… 63eecf2738… 68d66ca…` → all three resolve (rc=0).
- `sha256sum <lane>/.ufo/waves/round-47/count-c2.py` → `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` — byte-identical to the frozen instrument digest in contract.md (line 15). No install/upgrade performed (no tools needed; nothing to record).
- Working tree: `git status --porcelain` shows only untracked `.ufo/waves/round-47/w2/` (this report dir); no other dirt.
- Receipt commit: `git rev-parse af2250d80033ded23ec34af328068eeb85007d1c^{commit}` resolves; `git diff T af2250d8 -- <C2 measured files>` (entry, corpus/SOURCES.md, corpus/evidence/sources-r47, counter) is **empty** — tree equality for every measured file confirmed. The only diff is `evidence/after-c2.txt` itself (present at T, absent at af2250d8), i.e. the receipt file was committed with the tip while measured at af2250d8 — consistent with the claim's "measured at af2250d8" wording.

## Run 1 — counter at T (landed tip)

Command (cwd = lane root, TMPDIR=<lane>/.scratch/r47w2-ExecRerunC2):

```
$ python3 .ufo/waves/round-47/count-c2.py 68d66ca53d89be5c34a62f46af7c37449d9f9b63
C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63
rc=0
```

Comparison with receipt `evidence/after-c2.txt` (measured at af2250d8):

```
$ python3 .ufo/waves/round-47/count-c2.py af2250d80033ded23ec34af328068eeb85007d1c
C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=af2250d80033ded23ec34af328068eeb85007d1c
rc=0
```

Identical on every metric token (`C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok`); the only differing token is `rev=`, which is the argument passed to the counter. Run reproduces the receipt. Target-after predicate satisfied.

## Run 2 — selftest

Command:

```
$ python3 .ufo/waves/round-47/count-c2.py --selftest
PASS honest  …
PASS missing_event_three_of_eight_class  …
PASS invented_event  …
PASS missing_field  …
PASS wrong_callsite  …
PASS pin_tamper  …
PASS no_source_row  …
PASS no_provenance  …
PASS no_table  …
PASS duplicate_row  …
PASS entry_absent_do_nothing  …
PASS source_row_queued  …
PASS cli_not_a_repo_rc2  rc=2
C2_SELFTEST pass=13 fail=0
rc=0
```

13/13 PASS, fail=0, rc=0. (Full per-case lines retained in the run transcript; all cases predicted unmet → unmet, and the honest fixture → met.)

## Run 3 — counter at E (entering tip, do-nothing control)

Command:

```
$ python3 .ufo/waves/round-47/count-c2.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
C2=unmet events=0 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=4 source_row=bad provenance=bad rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 failed=entry_absent,pins,source_row
rc=1
```

Matches the contract's Before state exactly: `C2=unmet … failed=entry_absent,pins,source_row`. All four source pins missing at E (pin_mismatch=4) because the sources-r47 copies are not committed there.

## Run 4 — counter at F (freeze commit)

Command:

```
$ python3 .ufo/waves/round-47/count-c2.py 63eecf2738db96f46b0bd02b1b2dfd66787493d0
C2=unmet events=8 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=bad rev=63eecf2738db96f46b0bd02b1b2dfd66787493d0 failed=entry_absent,source_row
rc=1
```

Unmet as expected. At F the source copies are committed (pins=0), so the failure isolates to the entry and the SOURCES row (`failed=entry_absent,source_row`) — precisely the isolation the contract predicts ("Re-scored at the freeze commit, where the source copies are committed, so the failure isolates to the entry").

## What was attacked and why it holds

- Claimed after-state at T: reproduced exactly (Run 1), with the counter's own selftest proving the instrument catches each named failure class (Run 2). Counter bytes at run time = frozen v1 bytes (sha256 match).
- Claimed before/control states: E fails with exactly the contract's `failed=entry_absent,pins,source_row`; F fails with entry/row absence only. Both rc=1. The before state cannot be reached "by doing nothing" — doing nothing leaves E's revision, which is unmet.
- No mutation of lane/fleet git state occurred (git use was `rev-parse`/`show`/`diff`/`status`/`ls-tree`, all read-only); no subagents; all scratch under `<lane>/.scratch/r47w2-ExecRerunC2` (TMPDIR for every run); host reads read-only.

## Retained evidence

- Transcripts above (command + output + exit code) for all four runs.
- Frozen counter sha256 `fc77b933…` vs working-tree file sha256 (identical).
- Receipt comparison: metric-for-metric identical; `rev=` token reflects the argument passed (receipt measured at af2250d8; this run at T).
- Tree equality between T and af2250d8 for all measured C2 files verified via empty `git diff`.

## Risks / blockers

- None blocking. Notes: (1) receipt file is tracked at T but absent at af2250d8, so the receipt captures a measurement at af2250d8 committed later with the tip — consistent with the claim text, verified by the empty diff on the measured content files. (2) As a delegated seat I am not an independent judge; this is a rerun of the same counter on the same revs, confirming the claim's stated after-state and control states.
