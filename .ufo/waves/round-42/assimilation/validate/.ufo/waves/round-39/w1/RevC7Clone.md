# RevC7Clone — C1 red: independent rebuild of the M18 fabricated self-consistent clone

## Acceptance: PASS

I rebuilt the clone from scratch (my own builder, not run-c7-reds.py): stub entry with the
three real anchors, invented live receipt = the real ten drifted rows plus `S103 drifted` with
summary `drifted=11`, committed as a sandbox child of the scored tip.

- Sandbox: `git clone --shared` of the lane, checked out at
  `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`; commit
  `dbc92a84c92cfcd852c2f94c03eb87a9aa5d1249`; parent
  `13bfba23b7ca063c76d3504a2ff6eb7b6a294932` (verified). Two paths changed: the stub entry
  and `.ufo/waves/round-37/evidence/drift-live-r37.txt`.
- r38 counter = verbatim `git show 13f3db7e:.ufo/waves/round-38/count-c4.py`
  (sha256 `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1`, identical to
  the tip's frozen copy), r38 fixtures extracted beside it. Driver imports those bytes and
  redirects only `SCRATCH_ROOT` into my scratch (lane round-38 tree untouched):
  `python3 .ufo/waves/round-39/scratch/RevC7Clone/drv-r38.py dbc92a84c92cfcd852c2f94c03eb87a9aa5d1249 --repo .ufo/waves/round-39/scratch/RevC7Clone/sandbox`
  → `check live_rows PASS (named=11 summary_drifted=11 unknown=[] unique=True)`, **`C4=met`, exit 0**.
- count-c7 = lane bytes (sha256 `b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`,
  equals `evidence/freeze-r39.txt`):
  `python3 .ufo/waves/round-39/scratch/RevC7Clone/drv-c7.py dbc92a84c92cfcd852c2f94c03eb87a9aa5d1249 --repo .ufo/waves/round-39/scratch/RevC7Clone/sandbox --seed 20261024`
  → `check live_rows_v2 FAIL (named=11 summary_drifted=11 unknown=[] unique=True no_copy=['S103'])`;
  the other four checks PASS and all four negatives are rejected; **`C7=unmet`, exit 1**.
- Baselines on the real tip `13bfba2`: r38 `C4=met` exit 0; count-c7 `C7=met` exit 0
  (`live_rows_v2 PASS (… no_copy=[])`).
- Driver logs: `.ufo/waves/round-39/scratch/RevC7Clone/logs/{clone1-r38,clone1-c7,real-r38,real-c7}.log`.

So the counter rejects the clone exactly on the claimed discriminator, and S103 is the sole
named id without a committed copy (`git ls-tree -r --name-only 13bfba2 corpus/evidence | grep -c S103`
→ `0`; S103 is a registry row, `corpus/SOURCES.md:109`). Anchors independently verified at
non-comment offsets in `tools/mori-source-drift.py` lines 54, 158, 208 —
`check_anchors_v2` → `(True, 'anchors=3 short=[] not_in_code=[] unique=True')`.

## Findings

### F1 — MEDIUM — `live_rows_v2` is an existence check: one fabricated 62-byte blob flips `C7=met`
`count-c7.py:99` (`COPY_RE`) matches only a path shape; `evidence_tree` (`:216-217`) reads
`git ls-tree -r --name-only`; `copy_paths_at` (`:223-232`) builds id→path; `check_live_rows_v2`
(`:313-330`) tests membership only (`no_copy = [sid for sid in named if sid not in copies]`,
`:326`). No blob content is ever opened.
Demonstration: clone `3a2373fd396e9c4c5550f2342c1b6fe1615585ad` = clone1 + one file
`corpus/evidence/sources-r39/S103.md` (62 bytes: `fabricated copy: one blob, no body, never
read by the counter`) → `check live_rows_v2 PASS (… no_copy=[])`, **`C7=met`, exit 0**
(`logs/clone2-c7.log`) on a fabricated stub entry and invented receipt.
Why it matters: P-C7's word is "committed **source copy**"; the code proves "a blob whose path
matches". The contract's disclosed bound (`contract.md:61`) covers only a forgery that *copies
the real* entry/row/receipt verbatim — clone2 is a fabricated binding (stub entry, invented
receipt, fabricated copy) and is not that class. This is the same words-vs-code gap C3 fixes
for the gate, recurring in C1: the M18 "fabricated content" class is one cheap file deep. The
measured after-state and the four negatives are unaffected; severity is medium because the
counter is faithful to the literal predicate reading.

### F2 — LOW — contradictory/ill-balanced receipts pass `live_rows_v2`
- Clone2's receipt keeps the real `S103 no-copy` at line 104 and adds `S103 drifted` at line 227;
  `live_rows_v2` passes because it only matches `<id> drifted` lines and the summary count.
- Clone `ddaa6752c5dd16ed290d7fb8ed84016dd1f536ab` = clone1 + only the fabricated copy, summary
  left arithmetically impossible (`rows=225` vs `53+0+11+0+162=226`) → `live_rows_v2 PASS`,
  **`C7=met`, exit 0** (`logs/clone3-c7.log`).
No check relates `rows` to the five state columns, or requires one state per id. The r38 counter
has the same shape (`count-c4.py:198-211`). Separate from F1 because a content read would not
fix these.

## Verified pins (no finding)
- `evidence/freeze-r39.txt` hashes all match current bytes and are identical at freeze commit
  `97b826a` and tip `13bfba2`: contract `fc36841b…`, count-c7 `b92c65f2…`, conform `fe0be179…`,
  gate `62cd4132…`, and every fixture.
- `contract.md:44`'s P-C7 (minus the `> ` quote prefix) is byte-identical to `count-c7.py`'s
  `PREDICATE` (both 1064 chars) — the apparent `…` in a prior read was display truncation, not
  a truncated predicate.
- `tools/mori-source-drift.py` unchanged `13f3db7e`→`13bfba2` (sha256 `453c5d8e…`).
- Lane read-only: all writes under `.ufo/waves/round-39/scratch/RevC7Clone/`; no lane file
  edited, no git/jj mutation in the lane, no tools installed or upgraded.

## Residual risk and verification gaps
- Verdicts use seed `20261024`; the seed selects only the `drift_kill_v2` drawn state (here
  `fresh`), and `live_rows_v2` never consumes it, so the C7 verdict is seed-independent, but I
  did not enumerate seeds.
- Clone2/3 are sandbox commits in scratch only; the lane's own `c7-red-clone.txt` fixture uses
  seed 7 and its own scratch. My independent rebuild reproduces its two verdicts.
- I did not probe copy-path variants (other `sources-r<N>`, non-blob paths) beyond the code
  read; `COPY_RE` + `ls-tree -r` names admit any blob under any `sources-r<N>`, which is the
  same existence-only weakness as F1.
- No counter divergence found: F1/F2 are predicate-strength/disclosed-bound gaps, not a
  mismatch between measured output and the code that produced it.
