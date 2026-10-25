# R48MutC2Counter — mutation test of frozen `count-c2.py --selftest`

**Attacked:** the frozen C2 counter's self-test detector, `.ufo/waves/round-48/count-c2.py` @ e4dfff32d4f97c7ef250e9a7538fa75d4f284492, blob sha256 `0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561`. Ten one-point mutants of the guarded predicates (the seat named 9 defect classes; "word bounds" was split into min/max to reach 10), each run against the bounded behavioral detector `python3 count-c2.py --selftest` (exit code + `FAIL`/`C2_SELFTEST` lines).

**Verdict: BREAKS** — class: selftest mutation resistance. 4 of 10 single-point mutants **survive** (m04 sources-floor, m05 word-min, m06 word-max, m08 wrong-copy-acceptance). 6 of 10 killed. The C2 predicate itself was *not* falsified on honest input (pristine baseline: `C2=met claims=8 located=8 …`, selftest 22/22); the breaks are detector-coverage gaps, per-mutant classes below. Survivors are coverage findings, not contract changes.

## Method (bounded, scratch-only)

- All mutants are scratch copies under `.scratch/r48w2-R48MutC2Counter/`. The frozen file was never opened by an edit tool. Each mutant lives at `.scratch/r48w2-R48MutC2Counter/<name>/count-c2.py` — exactly three directory levels below the lane root, because `selftest()` anchors corpus files via `dirname³(script dir)`.
- Detector: `TMPDIR=<scratch> python3 <mutant>/count-c2.py --selftest`; killed = non-zero exit / `FAIL` lines, baseline gated.
- Survivor evidence: separate `-verify` copies (mutant + a print of each check's actual `evaluate` line). Verdicts were taken from the **un-instrumented** mutant runs; the instrumented copies reproduced `pass=22 fail=0` (instrumentation changed no verdict).
- Baseline placement observation (observed, twice): a copy at 2 or 4 levels of depth aborts with `FileNotFoundError: …/corpus/evidence/sources-r48/xfs_quota.8.html` (traceback from `selftest()` line 232, exit 1). Relevant to anyone re-running from scratch; not scored as a defect.

## Baseline (gate)

```
$ TMPDIR=$S python3 $S/pristine/count-c2.py --selftest
PASS honest_met … (22 lines) … PASS other_entry_path_unmet
C2_SELFTEST pass=22 fail=0
EXIT=0
```

## Mutants → verdicts

| # | Mutant (exact one-point diff vs pristine) | Detector result | Verdict |
|---|---|---|---|
| m01 | drop opened-date: remove `and srow[8] == OPENED` from `row_ok` (line 159) | `FAIL row_opened_other_day_unmet`, `pass=21 fail=1`, EXIT=1 | **killed** |
| m02 | drop used-by: `and entry_path in [u.strip() for u in re.split(r"[,;]", srow[10])])` → `)` (line 160) | `FAIL used_by_missing_unmet`, `pass=21 fail=1`, EXIT=1 | **killed** |
| m03 | drop unique-quote: `… or q in seen_quotes:` removed from bounds check (line 144) | `FAIL duplicate_quote_unmet`, `pass=21 fail=1`, EXIT=1 | **killed** |
| m04 | sources floor off: `if len(used_sources) < MIN_SOURCES:` → `if False and …` (line 173) | `pass=22 fail=0`, EXIT=0 | **SURVIVED** |
| m05 | word-min drop: `if not (MIN_WORDS <= len(words) <= MAX_WORDS) …` → `if not (len(words) <= MAX_WORDS) …` (line 144) | `pass=22 fail=0`, EXIT=0 | **SURVIVED** |
| m06 | word-max drop: same site → `if not (MIN_WORDS <= len(words)) …` (line 144) | `pass=22 fail=0`, EXIT=0 | **SURVIVED** |
| m07 | pin check off: `if b is None or hashlib.sha256(…).hexdigest() != digest:` → `if False:` (line 106) | `FAIL pin_mismatch_unmet`, `pass=21 fail=1`, EXIT=1 | **killed** |
| m08 | wrong-copy acceptance: `if q in norm[url]:` → `if any(q in t for t in norm.values()):` (line 164) | `pass=22 fail=0`, EXIT=0 | **SURVIVED** |
| m09 | status drop: `srow[7] == "mined"` → `srow[7] == srow[7]` (line 158) | `FAIL row_not_mined_unmet`, `pass=21 fail=1`, EXIT=1 | **killed** |
| m10 | claim-cell floor off: `len(cells[0].split()) < 5` → `< 0` (line 134) | `FAIL claim_cell_short_unmet`, `pass=21 fail=1`, EXIT=1 | **killed** |

All ten diffs verified with `diff pristine.py <mutant>`: exactly the intended one-point change each, no collateral bytes.

## Survivor mechanisms (output-level evidence from `-verify` copies)

- **m04 — shadowed guard (weak assertion).** The only <3-sources fixture (`sources_floor_unmet`) has 6 rows, so `claims_floor` also fires; the check asserts only `not met`:
  `CHK sources_floor_unmet PASS | C2=unmet claims=6 … sources=2 … failed=bad_rows,claims_floor,source_rows` — `sources_floor` is absent from `failed` (dropped) yet the check passes. No selftest case isolates the ≥3-distinct-sources floor with claims ≥ 8.
- **m05 / m06 — vacuous assertion.** `short_quote_unmet` / `long_quote_unmet` assert `… and "bad_rows" in line`, but the summary line always contains the field name (`bad_rows=0` matches too). With the bound dropped, the out-of-range quote is no longer a bad row but is still unlocated:
  `CHK short_quote_unmet PASS | C2=unmet claims=8 located=7 quote_missing=1 bad_rows=0 … failed=quote_missing` (m05),
  `CHK long_quote_unmet PASS | … quote_missing=1 bad_rows=0 … failed=quote_missing` (m06).
  The checks cannot distinguish "rejected as bad row" from "counted as missing quote", so min/max word bounds are unpinned.
- **m08 — fixture insensitivity.** The wrong-copy fixture appends `" x"` to a quote lifted from the xfs_quota copy while citing the quotactl source, making the quote a substring of **no** committed copy. Any-copy lookup therefore still reports it missing:
  `CHK quote_from_wrong_copy_unmet PASS | C2=unmet claims=8 located=7 quote_missing=1 bad_rows=0 … failed=quote_missing` (m08).
  The fixture cannot tell per-row-copy lookup from any-copy lookup; drop the `" x"` suffix and m08's mutant would fail this check.

## Killed-mutant detail

Each of m01/m02/m03/m07/m09/m10 died on exactly its targeted check (the only `FAIL` line in its run), i.e. each guarded predicate in `row_ok`/bounds/uniqueness/pins has a dedicated, non-vacuous killer except the four classes above.

## Integrity / restoration evidence

- Frozen original sha256 **before** first run: `0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561`; **after** all runs: `0055aed101bd60b1267d160520948b8f412753b38c72b6bda17da841734ee561` (unchanged; also matches the pristine scratch copy). Scratch `pristine.py` hash identical at copy time and at close.
- Pristine rerun at close: 22 `PASS`, exit 0.
- Mutants and `-verify` instrumented copies confined to `.scratch/r48w2-R48MutC2Counter/` (left in place as evidence; nothing outside scratch and this report file was written). No git/jj mutating command run; read-only `sha256sum`/`diff` only. No pacman, no tool installs (none needed).

## Scope notes

- Detector for all verdicts is `--selftest` only, per seat. I did not run the C2 claim command against rev e4dfff3 (out of my scope) — the honest-input `C2=met` line above is from the selftest fixture, not the live rev. UNVERIFIED: nothing else material; all verdicts above are from executed runs with recorded exit codes.
- A surviving mutant is a coverage finding; I did not touch the counter, contract, or selftest.
