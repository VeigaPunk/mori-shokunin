# Mo89E02ArmsC2 — r88 c2 subject: nine attributed arms (calibration)

Axis: calibration. Seat: `Mo89E02ArmsC2` (executor, leaf). Entering revision: `760428abf925d98025b34bf23f2cbf54cbeb3bca`. Production checkout, corpus and git/jj index not written; no commits; no subagents; no background jobs. Tooling: python3 stdlib only; no installs or upgrades performed.

## Inputs (digests)

| item | sha256 |
|---|---|
| frozen r89 counter `.ufo/waves/round-89/count-c2.py` (read-only, MUTANTS source) | `40eacccc89bd3b394a6ffb0d6a5fd604143c41ec4375d8a4399e749b65420a3c` |
| subject exported from `760428ab:.ufo/waves/round-88/count-c2.py` (pre-edit; SUBJECT_ARMS=26, TARGET arms=26 already present) | `391268f891d17b5ae44cb0538da6de8f5786b2338ad1db7020405d158b263c18` |

## Candidate (complete)

- Scratch: `/fast/scratch/hyaku/mori-r89/Mo89E02ArmsC2/count-c2.py`
- Candidate artifact: `.ufo/waves/round-89/w1/candidates/r88-count-c2.py`, 406 lines, sha256 `6c2ac8fd17c907b498f4de1c18cc5ee209dfa21fb4fc390239c389fbed4b20ed`
- Diff vs. entering subject: `.ufo/waves/round-89/w1/Mo89E02ArmsC2-r88-c2.diff` (sha256 `673e60e6fb44178008a4e390ced1b0a355d7b13f2bd21bff2260bc9ffd4788aa`)

Changes (all in the subject; no production edit):

1. Extracted pure helpers: `met_line(rev)` (main now `print(met_line(rev))`), `own_ok_of(rc, out)` (main `own_ok = own_ok_of(own.returncode, own_out)`, same predicate), `clone_root_ok(top_out, d)` (clone fixture uses it; same `strip() == realpath(d)` predicate).
2. Deleted the dead `want_met` assignment in `fixture_verdict`.
3. FX label for a good `clean` fixture now prints `ok`; a good refused/absent fixture still prints `refused`; a non-good fixture still prints `ACCEPTED` (unchanged wording, see defects).
4. Nine new selftest arms, appended after `arms_pinned`: `target_full`, `met_line_derived`, `clean_wrong_split`, `receipt_name_bound`, `clone_top_bound`, `own_ok_red`, `verdict_last_wins`, `absent_without_supersedes`, `vacuous_body_fabricated`. Old 17 arms kept; total 26.

## Selftest (candidate)

`python3 -I <cand> --selftest --scratch <S>/work-pristine` → rc=0, `C2_COUNTER_SELFTEST pass=26 fail=0`, 26 PASS lines. AST parse rc=0.

## Nine isolated frozen mutant copies

Each anchor taken from frozen `MUTANTS` (C2 entries), required `count==1` in the candidate (all nine: 1). Mutant copy run as `python3 -I <mut> --selftest --scratch <S>/work-mut-<label>`. Kill rule (frozen): `(rc≠0 ∨ fail>0) ∧ FAIL <declared arm>`.

| mutant label | declared arm | state | rc | mutant sha256 | FAIL line(s) |
|---|---|---|---|---|---|
| C2-target | target_full | KILLED | 1 | `1571f461ff9d496366bc0158028c693bb3881958b76161f412d80ab57736e95c` | `FAIL target_full real=unmet fx=4 clean=1 refused=2 absent=1 arms=26` |
| C2-printed-target | met_line_derived | KILLED | 1 | `d0ea23ac808f630e2c9f0bcab3f2c961d100e837eb7726812b870a0211d60972` | `FAIL met_line_derived C2=met real=unmet … rev=abcdef123456` |
| C2-fixture-clean | clean_wrong_split | KILLED | 1 | `7f63e7a531fef7568bfb0860e6ee843cd6abacf0fe5b63fccf96469434586271` | `FAIL clean_wrong_split receipts=6` |
| C2-receipt-name | receipt_name_bound | KILLED | 1 | `b93d76742995d51bce494335b19d1d94a0c4f88dd9d0d22b2699b67352d8f924` | `FAIL receipt_name_bound other receipt` |
| C2-clone-top | clone_top_bound | KILLED | 1 | `af95750ee67c3c33cc49178de5048446af5aab499c0404a61927faec20adbbb6` | `FAIL clone_top_bound root` |
| C2-own-ok | own_ok_red | KILLED | 1 | `4d8192c6843c0c60116e8d1fbc672bb292669694f8bb0430422db1524ef0d38b` | `FAIL own_ok_red rc and fail` |
| C2-verdict-first | verdict_last_wins | KILLED | 1 | `ea0da4dfc4aa0020838b87fd998dceade299fe55f3f5b5052ef3cd1e63373ddd` | `FAIL verdict_last_wins last line` |
| C2-no-supersedes | absent_without_supersedes | KILLED | 1 | `3d6d2beb36f969b5bbe4f04e6b985edfc3bd091ff65b6389428e712820781c40` | `FAIL absent_without_supersedes ValueError` |
| C2-vacuous-body | vacuous_body_fabricated | KILLED | 1 | `b5401017e345a67a5ab133081507fa4822d9b8af5b97265636385a57047ecc8b` | `FAIL vacuous_body_fabricated body` |

Each mutant run printed `C2_COUNTER_SELFTEST pass=25 fail=1` (exactly its one declared arm failing). KILLED 9/9; survivors 0; unattributed 0; unanchored 0.

## Defects and limits (stated plainly)

- **Process slip, repaired before any run:** one edit targeted the wrong line and overwrote `env = dict(os.environ)` in `clone_fixture`. Restored in a second edit; the final diff shows no net change in `clone_fixture` beyond the `clone_root_ok` call. Pristine and mutant runs were made after the repair.
- **Not exercised:** `main` and `clone_fixture` are not run end to end (no `count-c2.py <rev>` graded run). Only the selftest arms and the nine mutant selftests were run, as assigned. The changed `main` call sites (`own_ok_of`, `met_line`, `clone_root_ok`, FX label) are therefore verified by AST parse plus the arm predicates, not by a graded run. Main should run the graded counter once integrated.
- **Retained wording defect:** a *non-good* clean fixture still prints `ACCEPTED` (the same label is used for any failing fixture). Left unchanged because the assignment asked only for the good-clean `ok` label.
- **Scope:** this seat delivers the r88 c2 subject candidate only. It does not establish `C2=met`; that also needs the r88 c1 candidate (Mo89E01ArmsC1), the frozen `ARMS_BY_FILE` (count-c1 28, count-c2 26) and the integrated frozen-counter run.

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r89/Mo89E02ArmsC2/` removed after these receipts were saved. No lane, production or corpus file was written; no fleet-root file touched.
