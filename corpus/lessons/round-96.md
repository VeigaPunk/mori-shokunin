# Round 96 — lesson (mori, L1 MoriR96, attempt 1)

Frozen contract: `.ufo/waves/round-96/contract.md` at `b88c8ae8` (freeze, before any wave output). Entering HEAD
`66c5518e239eeacd6070be26d78085ef702392cb`. Wave `w1`: 10 seats (executor ×2, scout ×2, connector, scribe, critic,
reviewer, mutation-tester, revenger-as-labrat-probe). Wave `w2` (residual attack, 2 seats) was NOT dispatched: the validator
refuses spawn waves under 8 lanes (`.ufo/waves/round-96/w2-validator.err` before its removal; `too_few_lanes`), so the
candidate counter received no post-build mutation sweep this round (Mistake 5).

## Claims (frozen; verdicts)

- **C1 calibration — met at the landing revision (predicate P1), counted.** Before: `C1=unmet mismatches=5` at
  `66c5518e` (`evidence/before-c1-count-c2-through95.txt`; new counter `w1/calib/base-run.txt`). After: see the report's
  before→after table, `tools/mori-scorecard-calibration.py <landing rev>`.
- **C2 freshness — unmet (honest stop).** Before: `unpinned=6`. After: `unpinned=3`, `ok=89`, `mismatch=0`,
  `prefix_only=31`. The frozen target `unpinned=0` is not reached; three rows are stale (below).

## Gate

Re-opened this round (URL · access date · located quote, ≤25 words; quote located in the pinned bytes, tags stripped):

| row | URL | access (UTC) | located quote | decision |
|---|---|---|---|---|
| S622 | https://git-scm.com/docs/git-log | 2026-11-05 12:21:59 | "Select only files that are Added ( A ), Copied ( C ), Deleted ( D ), Modified ( M ), Renamed ( R )" (`corpus/evidence/git-log-docs.html`) | **admit as pinned copy**: live bytes = recorded `f206647f…` |
| S612 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 2026-11-05 12:21:59 | "AND-OR list (see 2.9.3.1 Asynchronous AND-OR Lists ) executed from the current shell execution environment" (`corpus/evidence/posix-shell-v3-chap02.html`) | **admit as pinned copy**: live bytes = recorded `0889867a…` |
| S125 | https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md (receipts at `…/round-25/capture/capture.txt`, `capture-earlyoom.txt`) | 2026-11-05 12:21:59 | receipt head: "$ date -u +%Y-%m-%dT%H:%M:%SZ 2026-10-22T10:06:23Z [exit 0]" (`corpus/evidence/.ufo/waves/round-25/capture/capture.txt`) | **admit as pinned copy**: receipt sha256 = recorded `e60f1bbc…` and `7adbe069…`; both byte-identical to the sibling originals (`cmp`, read-only). Copied as evidence only; not absorbed knowledge (PROVINCE adjacency). |
| S615 | https://docs.python.org/3/library/ast.html | 2026-11-05 12:20:55 | live bytes 362,493 B, sha256 `5e531ef0…` ≠ recorded `7891c588…` | **reject for pin (stale)**: a one-line footer difference ("Last updated on Nov 05, 2026 (12:03 UTC).") against the round-90 copy; recorded digest not edited. Flip: a live fetch hashing to the recorded value, or a supersession row per CORPUS rule 2. |
| S616 | https://docs.python.org/3/library/tokenize.html | 2026-11-05 12:20:55 | live bytes 53,982 B, sha256 `91bea7a6…` ≠ recorded `6842ed0f…` | **reject for pin (stale)**: footer-only difference per DigestRev. Flip as S615. |
| S623 | https://docs.python.org/3/using/cmdline.html | 2026-11-05 12:20:55 | live bytes 171,073 B, sha256 `f0a03369…` ≠ recorded `90ac3b25…` (same byte count) | **reject for pin (stale)**: DigestRev reports a footer-only difference. Flip as S615. |

Spot-check (non-author, this lesson's Gate): the reviewer seat `DigestRev` re-fetched all six URLs independently at its own
time and reproduced the same verdict on every row (`w1/rev/DigestRev.md` §5); the critic `CritRound` judged both predicates
`needs-amend` and the C2 target unsatisfiable under the frozen rule, which this round recorded as an honest stop rather than
rescoping after data (`w1/crit/CritRound.md` §e). Result: **agree** with the gate on the three admits and the three rejects.
The closure's non-author spot-check remains pending.

No new `SOURCES.md` rows; no in-place row edits (`status`, `recheck`, `used-by` unchanged; CORPUS rule 2). Pinned copies
are evidence files under `corpus/evidence/`, not registry edits.

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| 1 | stale frozen self-check bound: the r79 calibration counter fixes `THROUGH = 78`, so it reads `met` while rounds 79–95 are unchecked | `evidence/before-c1-count-c2-default.txt` (rc 0, met) vs `evidence/before-c1-count-c2-through95.txt` (rc 1, `mismatches=5`) | none | new unbounded counter `tools/mori-scorecard-calibration.py` (C1); the frozen r79 counter is left unamended and its default-bound `met` is recorded as void for the landing revision |
| 2 | count stated without its command: the round-95 lesson said `unpinned=3`; measured `unpinned=6` at `66c5518e` | `evidence/before-c2-digest.txt`; `corpus/lessons/round-95.md` (digest debt) | CORPUS rule "A count carries its command" — not applied when the r95 lesson was written | this round's command receipt; both counts kept, and the r95 figure named as unmeasured |
| 3 | frozen r79 selftest lets three of six single-change mutants survive: M2 min-vs-max, M5 any verdict word, M6 skipped adjacency axis | `w1/mut/MutCalib.md` table (survivors: M2, M5, M6) | none — no criterion requires a mutation sweep of a calibration counter's selftest | carried to round 97 as a planned claim (mutation sweep of the new counter and of the frozen one); not applied to the frozen counter |
| 4 | contract trap: the frozen counter command pinned no bound, so a seat-authored counter with a default bound could print `met` on the unedited scorecard | `w1/crit/CritRound.md` §(b)(ii) | QUALITY 208 (do-nothing control scored before freeze) — scored only against the frozen counter | the unbounded counter plus a red-before measurement on the real subject (`mismatches=5` at `66c5518e`) |
| 5 | residual attack wave below the validator's band: a 2-seat residual was refused (`too_few_lanes`, floor 8), so the candidate counter got no post-build mutation attack | `.ufo/waves/round-96/w2-validator.err` (removed; text retained here) | the wave validator (band floor 8) and the round-size rule; no planning gate | none this round; carried to round 97 as a planned claim with its own 8-seat wave |

Additional classes checked: fleet-root misroot sweep is recorded in the report; the r95 closure's routed items (m8/m10/m11
survivors, the dormant `census_path` literal arm, the `## Gate` heading) were not in this round's claims and are carried.

## Frontier step

- Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0 (`mori ok`, 42
  W04 duplicate-URL warnings), `evidence/before-census.txt`. Census after: exit 0 at the landing revision (the report
  cites the command output; `corpus/SOURCES.md` bytes are unchanged this round).
- Sourced claim: C2's landed evidence (`corpus/evidence/git-log-docs.html`, `posix-shell-v3-chap02.html`,
  `corpus/evidence/.ufo/waves/round-25/capture/*`) cites `S622`, `S612`, `S125`, each opened this round (Gate above).
- Frontier rows advanced: none in `corpus/README.md ## Frontier`.
