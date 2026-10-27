# Mo52MutC2Entry — mutation test of round-52 C2 counter entry-level arms

Seat: `Mo52MutC2Entry` (mutation tester, wave w1). Date: 2026-10-26.
Assignment: >= 8 single-point mutations of `.ufo/waves/round-52/count-c2.py` covering the entry-level arms
(opened date, used-by, unique quote, sources floor, word bounds, words-beyond floor, pins, row status); run
`--selftest` as the detector; killed iff exit != 0; table + arm text for survivors.
Report path: `.ufo/waves/round-52/w1/Mo52MutC2Entry.md` (relative to lane root).

## Baseline and environment

- Frozen counter bytes: committed at data commit `8524904adb25e44f24d9f25aac7eae909625c18c` and working tree
  are identical — sha256 `0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a` for all three of
  `git show 8524904…:.ufo/waves/round-52/count-c2.py`, the lane working-tree file and the archived copy.
- Lane snapshot for testing: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 8524904… | tar -x -C
  /fast/scratch/hyaku/mori-r52/Mo52MutC2Entry/lane` (read-only git; one archive per seat).
- Detector baseline (pristine, from the archive):

```
$ python3 .ufo/waves/round-52/count-c2.py --selftest
PASS honest_met … PASS text_copy_keeps_angle_brackets
C2_SELFTEST pass=45 fail=0
$ echo $?
0
```

- Tools: Python 3.14.8, git 2.56.0 (no installs made; none needed). Disk guard before the heavy run:
  `/fast/scratch/hyaku` 24% used, 614.5G free, no ENOSPC.
- Scratch root: `/fast/scratch/hyaku/mori-r52/Mo52MutC2Entry/` (all runs under `runs/`, outputs under
  `outputs/`, harness `harness.py`, summary `mutant-results.txt`); `TMPDIR` set to scratch `tmp/`.

## Method

`harness.py` copies the pristine source, applies exactly one textual mutation (asserting the needle occurs the
expected number of times), writes the mutant to `<scratch>/runs/<mutant>/.ufo/waves/round-52/count-c2.py`,
symlinks `corpus` → the archived lane (the selftest reads the five `COPIES` files from disk), byte-compiles
(`py_compile`), then runs the identical detector `python3 count-c2.py --selftest` in that directory and records
rc, output, diff vs pristine and mutant sha256. Control: pristine bytes through the same plumbing →
`C2_SELFTEST pass=45 fail=0`, rc 0. Mutated files exist only under scratch `runs/`; the archived pristine lane
was never written (sha256 re-checked after all runs, `0a9ec2…` unchanged). No fleet-repo bytes were touched; the
only file written outside scratch is this report.

## Mutant table (15 single-point mutations)

| mutant | arm | mutation (one line) | verdict | rc | detector output | mut sha256 |
|---|---|---|---|---|---|---|
| m01_opened_date | opened date | `OPENED = "2026-10-26"` → `"2026-10-27"` | SURVIVED | 0 | pass=45 fail=0 | 8b682d8feeeb06bd |
| m02_used_by_column | used-by | `srow[10])]` → `srow[9])]` (reads `180d` column as used-by) | KILLED | 1 | pass=33 fail=12 | 09f0de88184f73bc |
| m03_unique_quote_gate | unique quote | drop `or q in seen_quotes` (duplicate quotes accepted) | KILLED | 1 | pass=44 fail=1 | 19ab9686eed77e3f |
| m04_sources_floor_min | sources floor | `MIN_SOURCES = 5` → `4` | KILLED | 1 | pass=44 fail=1 | 9bf7cfb5c488a847 |
| m05_word_bounds_min | word bounds | `MIN_WORDS, MAX_WORDS = 6, 25` → `5, 25` | SURVIVED | 0 | pass=45 fail=0 | 9640f267d8f02408 |
| m06_beyond_floor | words-beyond floor | `MIN_BEYOND = 3` → `2` | SURVIVED | 0 | pass=45 fail=0 | e0c9042e2d370925 |
| m07_pins_digest_eq | pins | `…hexdigest() != digest` → `== digest` | KILLED | 1 | pass=38 fail=7 | 3db9c8f6c4fc7cac |
| m08_row_status_queued | row status | `srow[7] == "mined"` → `== "queued"` | KILLED | 1 | pass=32 fail=13 | 62b893215a9c9fe8 |
| m09_claim_unique_gate | unique claim (extra) | drop `or ckey in seen_claims` | KILLED | 1 | pass=44 fail=1 | cf844fddd24111c5 |
| m10_min_votes_one | entailment votes (extra) | `MIN_VOTES = 2` → `1` | KILLED | 1 | pass=34 fail=11 | 2f9b1831f4c4b322 |
| m11_voters_range | voter list (extra) | `range(1, 13)]` → `range(2, 14)]` | KILLED | 1 | pass=35 fail=10 | e5c0e2534fc0ab12 |
| m12_fence_tilde_only | fence (extra) | parse_claims fence set `("```", "~~~")` → `("```",)` | SURVIVED | 0 | pass=45 fail=0 | bbe3b83a08db3322 |
| m13_claim_word_floor | claim word floor (extra) | `MIN_CLAIM_WORDS = 6` → `5` | SURVIVED | 0 | pass=45 fail=0 | b4117bc97787979a |
| m14_claims_floor | claims floor (extra) | `MIN_CLAIMS = 12` → `11` | KILLED | 1 | pass=44 fail=1 | b618e0070205c993 |
| m15_provenance_recheck_drop | provenance (extra) | drop `has("recheck")` from provenance condition | SURVIVED | 0 | pass=45 fail=0 | a7a9b23e9dc35a72 |

9 killed, 6 survived. Every required arm got at least one mutant.

## Survivors — arm text and what is not covered

Detector expected and observed for each survivor: `C2_SELFTEST pass=45 fail=0`, rc 0 (identical to baseline).
Full outputs: `/fast/scratch/hyaku/mori-r52/Mo52MutC2Entry/outputs/<mutant>.txt`.

1. **m01_opened_date** (`count-c2.py:46` constant). `OPENED` is both the acceptance value (`srow[8] == OPENED`)
   and the fixture builder default in the selftest; every fixture is built with `OPENED`, so any single date is
   self-consistent. The only negative fixture hardcodes `"2026-10-25"`, which differs from either value. The
   detector therefore cannot distinguish "opened 2026-10-26" from any other one fixed date: a counter that
   accepted a wrong single date (e.g. the day before) with matching rows would pass.
2. **m05_word_bounds_min** (`count-c2.py:49` constant). Lower word bound is only exercised by the 3-word fixture
   (`"available = 0;"`); no fixture has exactly 5 words, so a floor of 5 (accepting 5-word quotes) is
   undetected. Upper bound 25 is exercised (26-word fixture).
3. **m06_beyond_floor** (`count-c2.py:48` constant). The words-beyond floor is only exercised by the 1-word
   fixture (`claim_echoes_quote_unmet`); a floor of 2 (accepting claims with exactly 2 words beyond the quote)
   is undetected.
4. **m12_fence_tilde_only** (`count-c2.py:95` `parse_claims`). The fence toggle reacts only to ``` in the
   selftest; `~~~` fences are never exercised. With the `~~~` arm removed from the toggle, a `~~~`-fenced table
   would be parsed as content instead of skipped. The counterpart fence in `entail_votes` was not part of this
   mutation.
5. **m13_claim_word_floor** (`count-c2.py:47` constant). Claim-cell word floor is only exercised by the 2-word
   fixture (`"short claim"`); a floor of 5 (accepting 5-word claim cells) is undetected.
6. **m15_provenance_recheck_drop** (`count-c2.py:252`). No selftest case removes `recheck:` alone; the
   provenance arm only ever fails on missing `source:`/`verified-at:` or uncited ids. A counter that stopped
   requiring the `recheck:` header would pass the detector.

## Kills — arm evidence (failing checks)

- m02_used_by_column: `honest_met`, `altered_quote_unmet`, `indented_row_ok`, `breadcrumb_identical_claims_unmet`,
  and the entailment checks that require a valid row set (12 FAIL) — used-by column is load-bearing.
- m03_unique_quote_gate: `duplicate_quote_unmet` only.
- m04_sources_floor_min: `sources_floor_unmet` only.
- m07_pins_digest_eq: `honest_met`, `indented_row_ok`, plus entailment checks downstream of valid rows (7 FAIL) —
  pin comparison direction is exercised.
- m08_row_status_queued: `honest_met`, `row_not_mined_unmet`, `altered_quote_unmet`, `indented_row_ok`,
  `breadcrumb_identical_claims_unmet`, plus entailment checks (13 FAIL) — `mined` status is load-bearing.
- m09/m10/m11/m14 (extras): the single named check for each (`breadcrumb_identical_claims_unmet`,
  `entail_one_voter_unmet`, `voters_frozen`, `claims_floor_unmet`).

## Restoration evidence

- Mutated copies exist only under `/fast/scratch/hyaku/mori-r52/Mo52MutC2Entry/runs/<mutant>/`, generated by the
  committed harness and regenerable from `harness.py` + pristine bytes.
- Archived pristine counter re-hashed after all runs: `0a9ec2ffdd85dd1a2be13f359ad82c0f45f99b781d73f9bcf3fa098d7f3bb74a`
  (unchanged). No fleet-repo write, no `git add/commit/…` anywhere, no writes outside scratch + this report.

## Findings

1. **HIGH** — `count-c2.py:46` (opened date): the `OPENED` constant is self-referential in the selftest
   (fixtures are built from the same constant they are checked against); any single fixed date passes. The
   P-C2 claim "opened 2026-10-26" is not anchored to an independent expectation in the detector. Round-53 route:
   a selftest fixture with a hardcoded date different from `OPENED` that must fail (or assert the constant equals
   a literal), plus a positive fixture asserting the literal date.
2. **MED** — `count-c2.py:48` (words-beyond floor): floor 3 is only tested at 1 beyond-word; a floor of 2 is
   undetected. Round-53 route: add a fixture with exactly 2 words beyond the quote that must be rejected.
3. **MED** — `count-c2.py:49` (word bounds): lower bound tested only at 3 words; a floor of 5 is undetected.
   Round-53 route: add a 5-word quote fixture that must be rejected.
4. **MED** — `count-c2.py:252` (provenance): `has("recheck")` is never negatively exercised; dropping the
   recheck requirement passes the detector. Round-53 route: add a case removing `recheck:` alone that must fail.
5. **LOW** — `count-c2.py:95` (parse_claims fence): `~~~` fencing is untested; removing `~~~` from the toggle is
   undetected. Round-53 route: add a `~~~`-fenced table fixture that must be ignored.
6. **LOW** — `count-c2.py:47` (claim word floor): floor 6 is only tested at 2 words; a floor of 5 is
   undetected. Round-53 route: add a 5-word claim-cell fixture that must be rejected.

Killed arms (used-by, unique quote, sources floor, pins, row status, unique claim, min votes, voter list, claims
floor) show the detector exercises those arms; the six survivors above are the coverage gaps routed to round 53.
No counter change is proposed; these are named limits only.
