# Round 74 — mori (L1 MoriR74): C1 calibration verified met (the r73 closure's two status-neutral routed defects discharged — D73-1 the events-context registry row joined back into one physical row with the SKILL:905 tally pin and every earlier line byte-identical; D73-2 the battery-count precision correction of record — the literal `grep -c "rc=0"` output was 11 = 10 run-result lines + 1 embedded sample line, the '10/10 runs green' substance true); C2 depth verified met, sourced S589 (capability acquisition `tools/mori-rotation-schedule.py` — the r73 planned head (a) landed: the rotation-recurrence protocol as a designed multi-window schedule instrument composing the REGISTERED ua-variance probe, registered at landing as registry row 11, selftest 13/13 x3, first live run rc 0 re-running the r70 schedule under the pinned grammar with a DIFFERENT per-window classification); C3 freshness verified met (the standing pin-family re-verification extended to the rotation family — S581 byte-identical, S241 equal-size byte drift found and adjudicated `asset-churn` by the standing drift re-check rc 0)

author: mori L1 (MoriR74)
round: 74
date: 2026-11-02
entering: `a9c3abb7` (`a9c3abb70572e5be2eb3afd941b1993b7af8d0d8`, r73 verifier spotcheck tip)

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`. Spot-checks re-run
this round with own receipts (`.ufo/waves/round-74/evidence/freshstart-spotchecks-r74.txt`):
the frozen r61 counter re-derived at the r61 data tip (`python -I
.ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` rc 1, the same
verdict every closure and the r65–r73 re-derivations reached); the eight
r59/r60/r61 lane revs PRESENT and `merge-base --is-ancestor` of
refs/heads/master rc 0 each; the three fleet report commits (2807c6ab,
eeedfd53, 3bb9b8e7) PRESENT in the fleet repo. Do-nothing controls
(`.ufo/waves/round-74/evidence/controls-r74.txt`): the tool, the knowledge
entry and this round's pin receipt absent at entering rc 128 each; no
time-library row in SOURCES at entering; SKILL.md 1327 lines at entering
with the split row present (split-continuation=1, joined-cell=0); SOURCES
361 rows at entering; the r73 battery receipt's literal rc=0 count 11.

Ruled out as r74 claims, and why:

1. LANDING the boot-scoped events window in the registered pairing tool —
   the r73 SCORECARD planned (b) phrasing still pointed there, but the r73
   closure's own discernment verdict (§6) grades the refusal correctly
   calibrated while the mori | round-65 L0 (instrument-change class) is
   open, and a window change to a just-registered probe still needs its own
   able-to-fail design round. The S588 anchor candidate stays a candidate;
   the pairing tool byte is untouched this round.
2. The label-sweep instrument (the mori | round-73 L0 line) — re-verified
   unanswered this round; it stays operator-material, not lane-claimed.
3. The encoding-pin harness and the pin-check mismatch split (the
   considerthese suggestion 1) — behind the same open instrument-change
   ruling; routed around.
4. Scalar score moves — no closure states a new number and no lane
   convention licenses an L1-authored scalar; the axes table stays
   untouched (append-only SCORECARD, prefix sha-identical).
5. Claims on the old Linux host's live surfaces — absent here, honestly
   `unavailable` (the Round-62 host note stands).
6. L2 wave dispatch — no dispatch surface on this host (carried
   disclosure; the three open mori L0 lines re-verified unanswered). Round
   74 ran L1-only over committed bytes, this host's network and this
   host's own surfaces.

All declared claims are unreachable by a do-nothing round (controls receipt
above).

## Gate

One NEW source opened this round (no supersedes corrections were owed —
the S241 finding is asset churn on the live body, not a registry-row
defect; see Mistakes and the C3 receipt); fetched with `curl -sS -m 60
-L`, duplicate sweep run INTO the receipt BEFORE the fetch (the r69
lesson's rule):

- S589 — https://docs.python.org/3/library/time.html — opened 2026-11-02 —
  located quotes (13 words each, ≤25): "Return the value (in fractional
  seconds) of a monotonic clock, i.e. a clock" (`:524`) and "that cannot go
  backwards.  The clock is not affected by system clock updates." (`:525`);
  difference-only-validity `:526-527` and the Windows QueryPerformanceCounter
  note `:529` located unopened beyond the quotes; page `<title>` "time —
  Time access and conversions" (Python 3.15.2) in the pinned head `:20`;
  pinned copy `corpus/evidence/sources-r74/S589.html` sha256
  `c8cc430e04d232f9e67412eae254a2c67ad153b4bde78121f83f2389739e91c7`
  (129606 bytes). Pre-row URL sweep = 0, receipted with the interpretation
  INSIDE `.ufo/waves/round-74/evidence/source-s589-r74.txt` BEFORE the
  fetch. The row landed INSIDE the Registry immediately after S588
  (SOURCES.md:370); row count 361 → 362 counted by
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`;
  the 13-field shape check prints `badNF=0` over all 362 rows. Both
  word-count anchors machine-verified by the r72 anchor-checker (PASS
  items=2 rc 0; the able-to-fail mislocation arm FAIL rc 1) —
  `.ufo/waves/round-74/evidence/s589-anchor-check-r74.txt`. Knowledge entry
  `corpus/knowledge/rotation-schedule-r74.md` (K1–K5 + limits + boundaries)
  cites the row in its provenance trio.

In-place changes (contract rule 2, each logged old→new): S241 used-by
`corpus/knowledge/oom-evidence-loss-r38.md` → + `, corpus/knowledge/rotation-schedule-r74.md`;
S581 used-by `corpus/lessons/round-70.md` → + `, corpus/knowledge/rotation-schedule-r74.md`.
Both cells otherwise byte-unchanged; no status or recheck cell touched.

SOURCES.md otherwise unchanged.

## Mistakes

1. class: verification (a receipt line written from two different counting
   methods, reading as a mismatch) — the C3 teaching re-verification first
   printed `診断 count pin=3 live=6`: the "3" was the anchor cell's recorded
   LINE-count (`grep -c`), the "6" an OCCURRENCE-count (`grep -o | wc -l`)
   from my own command — two methods in one comparison line, neither named.
   The r72 label lesson's exact class (a count must state its method), one
   step from landing a fabricated-looking drift into a receipt.
   captured-by: re-measuring BOTH methods on both bodies before committing
   the receipt (pin lines=3, live lines=3; pin occurrences=6, live
   occurrences=6 — agreement under each method, mismatch only across
   methods). fix: the receipt block now states both methods with their
   commands and the disclosure; every count a receipt quotes names its
   method (line-count vs occurrence-count at minimum).
2. class: landing (a child-spawning selftest costs ~40 s per run on this
   host) — the new tool's selftest arms invoke the fake child through
   `subprocess.run` ten-plus times per run; on this Windows host each
   process spawn is slow, so three consecutive selftest runs plus an
   eleven-tool battery silently exceed the 120 s foreground shell budget —
   the run was backgrounded mid-write twice. captured-by: the shell
   timeout hitting the selftest-x3 loop and the battery; both re-run as
   background tasks with the receipts verified complete afterwards
   (`rotation-schedule-selftest-r74.txt` three `PASS (13 cases)` + `rc=0`
   lines; `selftests-battery-r74.txt` eleven `^rc=0$` lines). fix: any
   loop that spawns processes per iteration goes to the background runner
   by default on this host, and a receipt built incrementally is only
   counted done when its expected line count checks green.
3. class: landing (the r73 heredoc-append truncation class RECURRED — this
   time caught before it could bite) — the LOG.md round entry went through
   a large quoted heredoc and bash reported `here-document delimited by
   end-of-file` with the python input unparsed; LOG.md stayed byte-untouched
   (verified by the completeness tail-grep BEFORE any append). The r73
   lesson's own fix was then applied as designed: the entry written to a
   scratch file, appended with `cat >>`, and verified by greps
   (`grep -c "^## Round 74" LOG.md` = 1; 4231 → 4336 lines; the tail ends
   on the assimilation line). captured-by: bash's own warning plus the
   pre-append and post-append completeness greps. fix: standing — no
   multi-KB heredoc into any repo byte on this host; scratch file + `cat`
   + completeness greps is the only append path (now exercised twice).

## Wave

None — no dispatch surface on this host (carried disclosure; the three
open mori L0 lines — round-62, round-65, round-73 — re-verified unanswered
this round, routed around, never treated as answered). Round 74 ran
L1-only over committed bytes, this host's network and this host's own
surfaces; no wave-based evidence is claimed.

## Assimilation

considerthese mined (all eight files re-listed this round; newest-named
2026-10-26.md): the 2026-10-26 suggestion 1 (split pin-check mismatches
into "can't run here" vs "stale") remains the one still-unimplemented
proposal and remains behind the operator's open instrument-change ruling
(the mori | round-65 L0 line); suggestions 2–4 stay proposals (suggestion 3
is the standing fresh-start spot-check practice, re-performed this round).
Assimilation: none — shokuknow unreachable.
