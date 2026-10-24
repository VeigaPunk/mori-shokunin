# W2 ReviewCorrectionsR2R3 — attack of the routed R2/R3 corrections (round-30 lesson, SOURCES note)

**Verdict: agree with defect found — both corrections are substantively exact and complete; two minor prose/citation defects sit inside the correction text itself (R2's "one prototype" is false; R3 cites `round-29-verifier-spotcheck.md:163` where the routed pair is at `:159`).**

## Method

Re-derived from bytes, not receipts. Tooling directive: **no installs** (used preexisting curl, sha256sum, grep, wc, sed). Fetches went to `/fast/scratch/hyaku/mori-r30-w2/ReviewCorrectionsR2R3/`; no lane writes except this report; no git/jj writes anywhere.

- Re-fetched at the row's exact URLs (root paths; `src/kill.h` and `src/testsuite_cli_test.go` are HTTP 404 at v1.9.0):
  `curl https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.h` → HTTP 200, 1 440 B, sha256
  `abf8577b434096e1eb980bacc24508e8421af9edbefb0d78cf5b8b5f28160bfb`; `.../v1.9.0/testsuite_cli_test.go` →
  HTTP 200, 9 317 B, sha256 `1dc876421c856bde48ab4a63304dab838c585f79c68a807d52b0741d366eb795`.
  Both digests and sizes equal the row's recorded cells (`corpus/lessons/round-29.md:65`) and R2's claims
  (`corpus/lessons/round-30.md:158-168`).
- Re-ran the greps on the fetched bytes: `grep -in -e dryrun -e version kill.h` → exactly
  `36:    /* Flag --dryrun was passed */` and `37:    bool dryrun;`, exit 0. Same command on
  `testsuite_cli_test.go` → no output, exit 1. Isolated `grep -in version` on each → exit 1 (no match);
  isolated `grep -in dryrun testsuite_cli_test.go` → exit 1. So R2's replacement facts are all true and the
  round-29 row's reason ("no line in either file", `round-29.md:65`) is indeed false for kill.h.
- Recounted every label at `round-29.md:55-65` by piping each quoted string, extracted verbatim from the
  committed bytes, to literal `wc -w` (16 labels / 18 strings; two-string labels summed).

## R2 — exact and complete in substance

- Digests, sizes, grep outputs, exit codes, 44-line count (`wc -l kill.h` = 44), and the located quote
  `kill.h:36-37` (8 words = 6+2 by `wc -w`) all verified as stated (`round-30.md:158-168`).
- `kill.h:36-37` really are field declarations of `poll_loop_args_t` (struct closes at `kill.h:38` with
  `} poll_loop_args_t;`); the reject decision ("declares the flag, no send-site behaviour") stands — none of
  the file's declarations sends a signal. The correction's target defect is real and correctly described.
- **F1 (minor, exactness of the correction itself): R2's own reason sentence is false.**
  `corpus/lessons/round-30.md:167` says "the file has 44 lines and one prototype (`void kill_process(...)`,
  `kill.h:40`)". The fetched kill.h (sha `abf8577b…`) carries **three** prototypes: `kill_process` `:40`,
  `find_largest_process` `:41`, `is_larger` `:42`. Same defect class R2 corrects (a reason sentence stating
  something the named file contradicts); the conclusion survives (no prototype sends a signal), but the count
  is wrong. It also propagates: round-30 M1 (`round-30.md`, Mistakes M1, "one prototype … kill.h:40") repeats it.
- **F3 (cosmetic, ambiguity):** `round-30.md:166-167` "field declarations inside `poll_loop_args_t`
  (`kill.h:30-38`)" — `:36-37` do lie inside `:30-38`, but the struct actually spans `kill.h:10-38`
  (`typedef struct {` at `:10`). True as a neighborhood range, wrong if read as the struct's span.
- R2's fetch timestamp `2026-10-22T21:12:35Z` is not verifiable post hoc [INFERENCE — unobservable]; the
  digests are the binding fact and they match.

## R3 — exact and complete; one citation pointer wrong

Full recount (label → `wc -w` on verbatim committed bytes):

| line | label | wc -w | |
|---|---|---|---|
| :55 | 22 | 22 | OK |
| :55 | 24 | 24 | OK |
| :56 | 3 | 3 | OK |
| :57 | 2 | 2 | OK |
| :57 | 8 | 8 | OK |
| :57 | 3 | 3 | OK |
| :57 | 11 | **10** | wrong — correction confirmed |
| :57 | 4 | 4 | OK |
| :59 | 3 | 3 | OK |
| :60 | 11 | **10** | wrong — correction confirmed |
| :61 | 4 | 4 | OK |
| :61 | 5 | **4** | wrong — correction confirmed |
| :62 | 17 | **16** | wrong — correction confirmed |
| :63 | 8 | **6** | wrong — correction confirmed |
| :64 | 9 | 9 (2+7) | OK |
| :65 | 8 | 8 (6+2) | OK |

- Exactly 5 of 16 labels wrong, and R3's five corrections are the right five with the right values
  (`round-30.md:169-178`): completeness and exactness confirmed — no sixth wrong label exists.
- "Largest true quote is 24 words, so the 25-word quote bound holds either way" — verified (max 24).
- Provenance verified: `.ufo/waves/round-29/w1/SourceJournalExport.md:81` labels 2,8,3,11,4 and `:85`
  labels 4,5; `.ufo/waves/round-29/w1/SourceEarlyoomDryrun.md:72-73` labels 17,8 — all as R3 states.
- **F2 (minor, reference-drift): `round-30.md:178` cites `round-29-verifier-spotcheck.md:163` as "the routed
  pair … names 11 vs 10 and 17 vs 16".** That text is at `round-29-verifier-spotcheck.md:159`; `:163` is the
  R5 bullet's continuation ("separate writer vocabulary from tool leakage; fix and self-test it…"). Spotcheck
  cross-references `:126`, `:130` and `:157-158` elsewhere in M1/M2 are correct.

## SOURCES note — accurate

`corpus/SOURCES.md:213` (before `## Leads` at `:215`): five true values match my recount one-for-one;
"S153-S155 cells in this file carry no word-count label" verified (`grep -c 'words)'` on SOURCES `:159-161`
prints 0); the drafting-seat pointers are the verified ones above; "the corrected counts are also appended to
`corpus/lessons/round-30.md`" is true (R3 bullet at `round-30.md:169`). M2's side claim also reproduces:
`grep -ci word` over SOURCES `:160-161` prints 1 and the match is "wording".

## Findings by severity

- F1 minor — `round-30.md:167` (and M1's restatement): kill.h has three prototypes (`:40-42`), not one.
- F2 minor — `round-30.md:178`: spotcheck pointer should be `:159`, not `:163`.
- F3 cosmetic — `round-30.md:166-167`: `kill.h:30-38` is a neighborhood, the struct spans `:10-38`.

## Residual risk / verification gaps

- Systemd-side quotes/locations/digests of S153-S155 (`round-30.md:170` "every quoted string, location and
  digest is right") were not re-fetched here — my re-fetch scope was the two earlyoom files; those cells were
  verified by the round-29 outside check (`round-29-verifier-spotcheck.md:122-131`) and I did not contradict them.
- Fetch timestamps and "access time" cells are unobservable after the fact; digest/size equality is the
  verifiable residue and it holds everywhere I checked.
