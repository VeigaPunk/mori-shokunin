# RevC4Negatives — wave 2 falsification, C1 (C4) negative witnesses

Seat: `MoriR38.RevC4Negatives` (L1 MoriR38, wave 2)
Scored tip: `f725f3076972e6e70595b5ac8279be524a111ff8`
Scope: which of the four content checks each fabricated witness fails when projected
onto the real other bytes, and whether `count-c4.py`'s three negative lines agree.

## Verdict: PASS — the negatives discriminate, one failed check each

No witness passes all four checks; each fails exactly one, and each failed check is
the one the witness was fabricated to break. The counter prints `rejected` for all
three, consistent with the per-check decomposition below.

## Commands run (this seat, this session)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8
... (P-C4 predicate line elided)
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
check anchors          PASS (anchors=3 missing=[])
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
check live_rows        PASS (named=10 summary_drifted=10 unknown=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill       PASS (exit=1 row_states=('FAIL', "got=[...('S103', 'excerpt')...] want=[...('S103', 'drifted')...]"))
C4=met
EXIT=0
```

The counter's negative lines only say `rejected`/`ACCEPTED`; they do not name the
failed check. To name it, each witness was re-projected independently by a scratch
harness (`.ufo/waves/round-38/scratch/RevC4Negatives/project.py`) that reuses the
counter's own `check_anchors` / `check_capability` / `resolves` / `check_live_rows` /
`paths_in` functions and substitutes exactly the input each witness replaces — the
same projection the counter encodes at `count-c4.py:305-323`:

- `witness-token-entry`  → substituted for `entry_text` (the r38 knowledge entry)
- `witness-dangling-row` → substituted for `scorecard_text` (whole SCORECARD.md; the
  fixture file is itself one capability row, so `paths_in(dangling_row)` equals
  `paths_in(capability_row(dangling_row))`)
- `witness-summary-only-live` → substituted for `live_text` (the r37 live receipt)

## Witness → failed-check table (harness output)

| witness | anchors | capability | live_rows | named_row_drift | drift_kill | verdict |
|---|---|---|---|---|---|---|
| `witness-token-entry.md` | **FAIL** `anchors=0 missing=[]` | PASS | PASS | n/a† | n/a† | rejected |
| `witness-dangling-row.md` | PASS | **FAIL** `missing=['evidence/no-such-receipt.txt']` | PASS | n/a† | n/a† | rejected |
| `witness-summary-only-live.txt` | PASS | PASS | **FAIL** `named=0 summary_drifted=10` | n/a† | n/a† | rejected |
| real bytes (control) | PASS `anchors=3` | PASS `missing=[]` | PASS `named=10/10` | PASS | PASS | ACCEPTED |

† `named_row_drift` and `drift_kill` are evaluated from `tool_text`
(`tools/mori-source-drift.py` at the rev) only — the counter's `negatives`
conjunction (`count-c4.py:305-323`) does not include them because no witness
substitutes the tool bytes. Of the contract's four content checks, only three
(`anchors`, `capability`, `live_rows`; the contract counts
`named_row_drift`+`drift_kill` as its fourth) are witness-dependent. Both tool
checks remain PASS in every projection; verified via the counter's own `check`
lines above, which run on the same real tool bytes the projections use.

### Why each fails

- `witness-token-entry` (fixture lines: tokens `huge_cap`, `redirect_private_refused`,
  `1caa242`, S221; zero `anchor:` lines): `check_anchors` requires
  `len(anchors) >= MIN_ANCHORS` (3) with no missing → `anchors=0` fails the count
  floor (`count-c4.py:169-173`). Passes the other two because it keeps the real
  scorecard and live receipt.
- `witness-dangling-row` (fixture: capability row citing `tools/mori-source-drift.py`
  and `evidence/no-such-receipt.txt`): `paths_in` extracts both backticked paths;
  `check_capability` itself returns True (row present, ≥1 path), but the
  `all(resolves(repo, rev, p))` conjunct fails on `evidence/no-such-receipt.txt`,
  which does not exist at `f725f30` (`count-c4.py:314-315`).
- `witness-summary-only-live` (fixture: `MORI_SOURCE_DRIFT rows=225 ... drifted=10 ...`
  + `EXIT=1`, no `S### drifted` lines): `check_live_rows` requires
  `len(named) == drifted` with `drifted >= 1` → `named=0 ≠ 10`
  (`count-c4.py:184-197`).

## Comparison vs the counter's three negative lines

| counter line | harness decomposition | agree? |
|---|---|---|
| `negative witness-token-entry        rejected` | anchors FAIL only | yes |
| `negative witness-dangling-row       rejected` | capability FAIL only | yes |
| `negative witness-summary-only-live  rejected` | live_rows FAIL only | yes |

The counter emits no per-witness reason, only the verdict; its conjunction is
`anchors ∧ capability∧resolves ∧ live_rows`, so `rejected` is consistent with — and
here is shown to be caused by — exactly one failed check per witness. No witness is
rejected by accident (e.g., a second, unrelated failure masking a non-discriminating
check): each witness passes the two checks it does not target.

## Residual risk / gaps

- The discrimination is only as strong as each witness being single-check-broken;
  verified: each is. A hypothetical "token entry" that *also* carried three
  resolvable `anchor:` lines would pass — but that is the honest positive case, not
  a defect.
- `MIN_ANCHORS=3` is a floor, not per-anchor necessity; the witnesses don't probe
  whether one fabricated-but-resolvable anchor would pass (it would, if ≥3 lines and
  all verbatim — again the honest case).
- `paths_in` skips tokens starting `http` and requires a `/` in the path; a
  fabricated row citing a nonexistent *top-level* file (no slash) would not be
  caught by `capability`. The committed fixture uses `evidence/no-such-receipt.txt`,
  which is caught. Not in scope of the assigned command, noted for the record.
- Harness reuses the counter's own check functions (correct projection by
  construction) rather than reimplementing the predicates; the projection semantics
  were verified line-by-line against `count-c4.py:305-323` before relying on it.

## Tooling

No installs performed or needed; stock `python3` + `git` sufficed.

Report: .ufo/waves/round-38/w2/RevC4Negatives.md
