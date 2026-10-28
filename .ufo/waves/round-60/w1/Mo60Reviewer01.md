# Mo60Reviewer01 — C2 re-derivation review (round 60, wave w1)

Seat: reviewer, leaf (no dispatch). Read-only on the lane; every mutation ran in a
scratch clone under `/fast/scratch/hyaku/mori-r60/Mo60Reviewer01/clone`.

Freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`; lane tip observed during the review
`b3c256138f00c704d5aa56eb0332d74506502ef2`.

## Verdict

**C2 reproduces byte-exactly at the freeze, and does not drift at the lane tip.**
The met line is a genuine function of (repo, revision) under a fresh `--scratch`,
and every claim arm (pin gate, selftest, scan, drift attribution, hostile trees,
real entry, copy equality) was exercised and shown to be load-bearing — except one
reproducibility hazard in scratch reuse (F1 below).

## 1. Freeze re-derivation

Command (cwd = lane root, fresh scratch):

```
python3 .ufo/waves/round-60/count-c2.py ac496c7cde8cad965079858accae3bedfe4a73f2 --scratch <S>/c2f
```

Output (exit 0):

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7cde8cad965079858accae3bedfe4a73f2
```

Byte-compare against the committed receipt:

```
cmp <S>/c2-freeze.out .ufo/waves/round-60/evidence/c2-at-freeze.txt   -> BYTE_EQUAL=yes
sha256 both = 5890ace1c7d0713d5d1e0b952c1a80d985938053bfad80ec03a34f1348f90b80
```

This matches the contract's frozen target token-for-token. Determinism: two runs on
two independent fresh scratch dirs produced byte-identical output (`DETERMINISTIC=yes`).

## 2. Lane-tip re-run (drift check)

At `b3c256138f00c704d5aa56eb0332d74506502ef2`:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c256138f00c704d5aa56eb0332d74506502ef2
```

**No drift in the met line** — only `rev=` differs. Required inputs are byte-stable
across the range: `git diff --name-status ac496c7c..b3c25613` lists exactly one C2-input
change, `corpus/SOURCES.md` (the C1 data landing, +4 rows); `tools/mori-entry-claims-check.py`
(`cffe9f33…e6e69`), `tools/mori-settlement-scan.py` (`4c04bf21…c9a9`), `count-c2.py`
(`8c4814f5…df976`) and `contract.md` (`a444e270…441d`) are byte-identical at both revisions.
Registry growth does not produce a false negative: `entry=ok rows=ok` still holds at the tip.

## 3. Entering-revision control

`count-c2.py ddfb12fb…` → exit 1, and `cmp` against
`evidence/control-c2-do-nothing.txt` → **BYTE_EQUAL=yes**:

```
C2=unmet selftest=bad scan=ok drift=ok trees=bad entry=bad rows=bad pins=bad tree=ok claims=0 files=0 spans=0 rev=ddfb12fb0838b4307c445194a844f0c4b1950195 failed=entry,pins,rows,selftest,tool_absent,trees,trees_set
```

The claim could not have been met before the round's work.

## 4. Discrimination tests (sandbox clone, all commits inside `<S>/clone`)

| # | Mutation | Result |
|---|---|---|
| A | baseline in clone at freeze | `C2=met …` (identical line) |
| B | `h02/expect.txt` tampered | `unmet … failed=expect_tamper:h02-malformed-claim,trees` (G3 works) |
| C | `h02` entry replaced by good-control bytes | `unmet … failed=tree:h02-malformed-claim:verdict` |
| D | EC tool replaced by marker-writing blob | `unmet … failed=…,tool_sha,…`; **0 marker files** under scratch (G1: blob never executed) |
| E | EC tool weakened (`MIN_SPAN=1`) | `unmet … tool_sha` (pin gate refuses to run it at all) |
| F2 | duplicate claim line in real entry | `unmet … claims=14 spans=13 failed=entry` (spans==claims is load-bearing) |
| G | whitespace-only quote in real entry | `unmet … spans=12 failed=entry` (`span:blank`) |
| H | claims below MIN_CLAIMS | `unmet … claims=4 failed=entry` (`claims_min`) |
| I | claim-shaped line w/o Quote field | `unmet … failed=entry` (H1 `grammar:`) |

Direct tool outputs (materialized pinned blobs from run A, no lane access):

- real entry: `ok=True reasons=[] stats={'claims':13,'files':6,'spans':13,'min_span':12}` — `min_span=12 ≥ MIN_SPAN=8` (H2).
- r53 drift: `SETTLEMENT_SCAN_FAIL` with 67 × `member[i]:extra_keys=report_file` — the `:extra_keys=` member key-set reason (H5) is genuine, not a filename heuristic.
- r54 bytes at an r53-named path (`alias/round-53-alias/w1.json`): `SETTLEMENT_SCAN_OK` — renamed control holds.
- scan arm: 5 real files, `members == seats` for every one (74/74, 64/64 ×4), `SETTLEMENT_SCAN_OK`.
- all six copies byte-equal their `.ufo` artifacts at the freeze; all thirteen trees reproduce their frozen expect prefixes (e.g. `h03→distinct:dup_span`, `h05→span:short`, `h07→rows:binding`, `h08→rows:status`, `h09→rows:usedby`, `h10→pin:`, `h11→span:`, `h12→frontmatter`).
- selftests match the contract: `C2_SELFTEST pass=8 fail=0`, `ENTRYCLAIMS_SELFTEST pass=13 fail=0`.
- no absolute host path in any r60 instrument or tool (`grep '/home/\|/fast/\|/tmp/'` → no matches).

## Findings

### F1 — MEDIUM (reproducibility): scratch reuse can report `met` for a revision that is not met

`count-c2.py:157` does `scratch.mkdir(parents=True, exist_ok=True)` and only ever
*adds* bytes. `count-c2.py:367` evaluates `scratch/"trees"/<name>` without resetting it,
and `count-c2.py:369` materializes only the files `git ls-tree` returns at R. A file
deleted at R therefore survives from an earlier run at the same `--scratch` and is
still evaluated.

Reproduced in the sandbox clone:

```
scratch X fresh, at freeze      -> C2=met … (exit 0)
clone: delete trees-c2h/h02/corpus/knowledge/wave-settlement-artifacts-r59.md
                                 rev c3b949ce0ad1d9d72155c94e4f1f0ea963ed3626
same scratch X, at that rev     -> C2=met … (exit 0)      <-- stale file masks the deletion
fresh scratch, at that rev      -> C2=unmet … failed=tree:h02-malformed-claim:reasons,trees (exit 1)
```

Impact: the frozen receipts are sound (they were produced with fresh scratch dirs and
my fresh-scratch re-derivations reproduce them exactly), but the counter is not the
deterministic function of R the predicate implies; a reviewer or adversary reusing a
scratch directory can obtain `C2=met` for a revision where a hostile-tree construction
was removed. Suggested fix (for a future non-frozen revision): `shutil.rmtree` the
per-arm subdirs (`trees/`, `root/`, `real/`, `drift/`, `alias/`) before materializing,
or require an empty `--scratch` and record that in the receipt.

### F2 — LOW (dead condition): the scan arm's gate is a no-op

`count-c2.py:209` — `if not (ec_ok is not None and scan_ok_sha) or not rfiles:`.
`ec_ok` is a `bool`, so `ec_ok is not None` is always true and the clause reduces to
`not scan_ok_sha or not rfiles`. No verdict changes (the scan arm is intentionally
independent of the entry-claims tool), but the expression states a dependency that
does not exist and will mislead the next reviser.

### F3 — LOW (token redundancy): `rows=` / `pins=` are not independent

`count-c2.py:333-334` derive `rows_ok`/`pins_ok` from reason prefixes, but `entry_ok`
already requires the tool's `ok is True`, which requires an empty reason list. So
`entry=ok` implies `rows=ok pins=ok`, and those tokens can never be the sole cause of
an `unmet`. The contract's target line includes them, so keep them — but they carry no
discriminating power, and a report should not cite them as separate evidence.

### F4 — INFO (not exploitable today): H4's `if binders and` guard

`tools/mori-entry-claims-check.py:237` skips per-copy binding when the registry yields
no binders. That state always co-occurs with `rows:missing` / `rows:usedby` /
`rows:no_source_ids`, so the entry still fails; it is redundancy, not a hole. Noted for
the record only.

## Residual risk

- The hostile-tree arm pins verdict + reason prefixes + `expect.txt` bytes, but not each
  tree's file *inventory* at R; a deletion is caught only because a fresh scratch is used
  (F1). An addition at R would be materialized and could only be caught by the tool's own
  reasons.
- Hostile-tree evaluation runs against the real `corpus/SOURCES.md`, so registry growth
  (the C1 data landing) is in the loop for every tree. It held here at both revisions.
- G1 was exercised through the EC blob; the scan blob shares `run_pinned` but was not
  separately substituted.

## Verification gaps

- I did not re-derive `count-c1.py` / `count-c3.py` (other seats' claims; C3's G1 uses the
  same `run_pinned` shape I verified structurally in count-c2).
- No pacman, no installs, no tool changes were needed (`disk-guard.sh status` green before work).
- Scratch receipts: `c2-freeze.out`, `c2-tip.out`, `drun/*.out`, clone at
  `/fast/scratch/hyaku/mori-r60/Mo60Reviewer01/` (removed on yield; key outputs are inlined above).

## Environment note (outside my claim surface, observed only)

The lane working tree carried untracked C1/C3 in-flight artifacts during the review
(`evidence/c1-at-data.txt`, `w1.ready`, `w1/`); every number above was taken from
committed bytes via `git show` at a named revision, never from the working tree.
