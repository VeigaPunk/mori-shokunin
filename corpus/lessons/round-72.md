# Round 72 — mori (L1 MoriR72): C1 calibration verified met (the r71 closure's D71-1/D71-2 carry-ins discharged — supersedes row S585 re-points the S584 zero-at-boot anchor :828→:829 and corrects the two misstated word-counts 22→26 and 17→15 against the byte-identical re-open, with an every-mention sweep across all seven carriers; PLUS the same defect class self-found and discharged in the same round: supersedes row S586 corrects two S581 word-count labels 10→9 and 15→14, supersedes row S587 corrects the S582/S583 `:829` definition label 14→13 — all three found partly because the standing QUALITY 90 label check, run against the entering bytes for the first time since r71 landed them, fails rc 1 on them); C2 freshness verified met (the standing pin-family live re-verification: all seven pinned pages behind S574–S585 re-fetched byte-identical, receipts bound per row); C3 operability verified met (capability acquisition `tools/mori-anchor-check.py` — the QUALITY 162/90 located-line + word-count check made runnable, able-to-fail demonstrated against the recorded drifted values themselves)

author: mori L1 (MoriR72)
round: 72
date: 2026-11-02
entering: `c5873f73` (`c5873f73d9811b65e44b5edcdeea625e519ed984`, r71 verifier spotcheck tip)

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`. Spot-checks re-run
this round with own receipts (`.ufo/waves/round-72/evidence/freshstart-spotchecks-r72.txt`):
the frozen r61 counter re-derived at the r61 data tip (`python -I
.ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` rc 1, the same
verdict the r61 closure and the r65–r71 re-derivations reached); the eight
r59/r60/r61 lane revs `cat-file -e` PRESENT and `merge-base --is-ancestor`
of refs/heads/master rc 0 each; the three fleet report commits (2807c6ab,
eeedfd53, 3bb9b8e7) PRESENT in the fleet repo. Do-nothing controls
(`.ufo/waves/round-72/evidence/controls-r72.txt`): every r72 artifact absent
at entering rc 128 (both errata receipts, the re-open receipt, the re-verify
receipt, the anchor-check tool, this lesson); SOURCES 357 rows at entering
with zero `supersedes S584`/`S581`/`S583` rows; the drifted mentions
STANDING at entering (tool header `S584:828` count=1, K4 `S584.html:828`
count=1, r71 lesson `(:828` count=1, r71 receipt `:828` count=1, the 22/17
labels count=1 each).

Ruled out as r72 claims, and why:

1. Re-declaring the r59/r60/r61 entry-claims-class instruments — their
   met-flip counterexamples stand on frozen bytes (re-derived unmet again
   this round, receipt above).
2. Scalar score moves — no closure states a new number and no lane
   convention licenses an L1-authored scalar; the axes table stays
   untouched (append-only SCORECARD).
3. Claims on the old Linux host's live surfaces — absent here, honestly
   `unavailable` (the Round-62 host note stands).
4. Editing the frozen bytes (SKILL.md, `tools/mori-source-drift.py`,
   `tools/mori-drift-adjudicate.py`, PROVINCE.md, AGENTS.md,
   corpus/README.md) — the SKILL:905 tally pin (the r65 L0) and the
   r65–r71 receipts bind those bytes; this round's diff contains none of
   them. The r65 L0 line stays open (re-verified unanswered this round,
   `l0-considerthese-r72.txt`) and was routed around, never treated as
   answered.
5. The r71 planned item (a), the multi-window rotation-recurrence protocol —
   NOT declared, honest sizing: this round's landing budget went to the
   closure-routed D71 discharge plus the self-found same-class discharge
   (three correction rows, two errata receipts, seven carriers swept); a
   designed multi-window instrument needs its own protocol design and
   live multi-session wall clock, and a rushed one would violate the
   QUALITY 161 stated-window discipline. It stays the r73 planned head.
6. The r71 planned items (b)/(c) — the encoding-pin harness and the
   considerthese pin-check mismatch split — both sit behind the operator's
   open instrument-change ruling (the mori | round-65 L0 line, still
   unanswered, `l0-considerthese-r72.txt`); routed around, not implemented.
7. The Precise variant QueryUnbiasedInterruptTimePrecise (S584:876, the
   r71 planned note (d)) — the lane's own recorded rule keeps it unopened
   "unless a round needs sub-tick working-state resolution"; no such need
   arose this round. Stays unopened.
8. In-place edits to any drifted r71 artifact (the S584 row anchor cell,
   the r71 opening receipt, the r71 lesson, the fleet report) — corrections
   are new entries, never in-place rewrites (contract v1 rule 2; the
   closure's routing §5). The only in-place edit this round is the
   lane-owned, non-frozen `tools/mori-workstate-win.py` HEADER COMMENT,
   which the closure routing explicitly licenses as "a next-round change";
   its code is untouched and the selftest re-run is green at the new bytes
   (`workstate-r72-recheck.txt`, 10/10 x3, live rc 0 x3).
9. L2 wave dispatch — no dispatch surface on this host (carried
   disclosure; the mori round-62 L0 line stands open, re-verified
   unanswered in `l0-considerthese-r72.txt`). Round 72 ran L1-only over
   committed bytes, this host's network and this host's own surfaces.

All declared claims are unreachable by a do-nothing round (controls receipt
above).

## Gate

One source RE-open event for the correction rows (no new external surface
was needed; the round's three rows are supersedes corrections of
already-opened pages), fetched with `curl -sS -m 60 -L`, duplicate sweeps
run INTO the receipts first (the r69 lesson's rule):

- S585 (supersedes S584 — the routed D71-1/D71-2 correction row): the SAME
  QueryUnbiasedInterruptTime page re-opened this round,
  https://learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-queryunbiasedinterrupttime
  — opened 2026-11-02T00:45:29Z — the live body is BYTE-IDENTICAL to the
  r71 pin (sha256 `d0bcbba945e7cf29d4664feb28a35aa31c1f80cadb5191644a33ab84464f9136`,
  54774 bytes, receipt `.ufo/waves/round-72/evidence/source-s584-reopen-r72.txt`),
  so the erratum's anchors bind the live body too. Pre-row sweep INTO that
  receipt: the page-identifying URL-slug sweep
  `nf-realtimeapiset-queryunbiasedinterrupttime` = 1 — receipted with its
  interpretation BEFORE the row landed: the 1 is the S584 row itself,
  EXPECTED for a supersedes correction row, not a duplicate surface.
  Verified per D71-1: the zero-at-boot sentence "The interrupt-time count
  begins at zero when the system starts and is incremented at each clock
  interrupt by the length of a clock tick." greps 0 at the recorded `:828`
  (which is `<h2 id="remarks">Remarks</h2>`) and 1 at `:829`, on pin and
  live copy; per D71-2: the failed-call sentence is 26 words (recorded 22)
  and the :817 sleep/hibernation sentence is 15 words (recorded 17), by
  `grep -o | wc -w` on the located lines; all other S584 anchors re-checked
  exact (:817 def 11 words, :819-820 signature, :826-827 span with the
  sentence wholly on :827, :830, :833, :876). Erratum receipt
  `.ufo/waves/round-72/evidence/s584-anchors-erratum-r72.txt` carries the
  every-mention sweep: SEVEN carriers named with dispositions — the S584
  row anchor cell (immutable; corrected by S585), the r71 opening receipt
  (bytes untouched; the erratum is the correction of record), the r71
  lesson Gate (bytes untouched; corrected old→new HERE, the D2 precedent),
  knowledge entry K4 (append-only correction block landed this round in
  `corpus/knowledge/workstate-win-r71.md`), the `tools/mori-workstate-win.py`
  header comment (fixed in place, the licensed next-round change; selftest
  green at the new bytes), the r71 LOG/SCORECARD entries (historical
  append-only round records: they STAND as recorded, corrected-of-record by
  S585 — rewriting them would falsify what the r71 measurement cited), and
  the fleet r71 report (orchestrator-owned, named). S584's scope, teaches
  and standing untouched; SOURCES row bytes for S584 UNCHANGED.

- S586 (supersedes S581) and S587 (supersedes S583) — SELF-FOUND this
  round, same class as D71-2, discharged in the same round by the same
  mechanism. The standing QUALITY 90 label check, run against the entering
  bytes (c5873f73) — its first run against rows landed AFTER r29 — returns
  `word_labels=8 mismatched=3` rc 1: the two routed S584 labels AND one
  nobody had flagged (S581's `:70-71` label 15, actual 14). The checker's
  parser sees only quote-ADJACENT labels, so a family-wide audit (every
  "(N words)" label in rows S574–S585 paired with its nearest quote,
  wc -w arbiter) closed the blind spot and found three more misstatements:
  S581 `:54` label 10 (actual 9), S582 `:829` label 14 (actual 13), S583
  `:829` label 14 (actual 13). Machine verification, carrier sweeps and
  dispositions in `.ufo/waves/round-72/evidence/s581-s583-labels-erratum-r72.txt`:
  the S581/S582/S583 row label cells (immutable; corrected by S586/S587),
  the r70 lesson Gate :65/:69/:80 (bytes untouched; corrected old→new
  HERE), the r70 opening receipt `source-s582-r70.txt:20` (bytes untouched;
  the erratum is the correction of record), the fleet r70 report
  (orchestrator-owned, named), LOG/SCORECARD (grep-clean, no carriers),
  `uptime-win-r70.md` K1 (quotes the sentence WITHOUT a count — not a
  label carrier, verified). All of S583's located-line pointer corrections
  stand UNCHANGED and were re-confirmed on the pin (:833→:834, :842→:841,
  :845→:842); S587 supersedes the LABEL only. S581's :59-60/:83-84 labels
  (19/11) re-confirmed correct.

- Standing re-verification (C2): all seven distinct pinned pages behind
  S574/S575 (r64), S579/S580/S581 (r68–r70), S582+S583 (r70/r71),
  S584+S585 (r71/r72) re-fetched live 2026-11-02 with the rows' own
  fetcher posture — ALL SEVEN byte-identical (sha256_match=yes x7,
  receipt `.ufo/waves/round-72/evidence/pin-family-reverify-r72.txt`),
  covering nine registry rows (S583 and S585 share pins with S582/S584).

Rows appended INSIDE the Registry immediately after S584 (S585 at
SOURCES.md:366, S586 at :367, S587 at :368). SOURCES row count 357 → 360
counted by `grep -c "^| S" corpus/SOURCES.md`; the 13-field shape check
`awk -F'|' '/^\| S[0-9]+ \|/ {n++; if (NF!=13) bad++} END {print n+0, bad+0}'`
prints `360 0` (see Mistakes 1 for the vacuous-pattern version of this
check that this round retired). Census rc 0 at round start
(`census-start-r72.txt`, 32 W04 warnings — the tolerated pre-existing
class) and rc 0 at round end (`census-end-r72.txt`).

reject sample: the boundary held against the tempting-to-overreach reads of
this round's findings. The re-verify receipt records byte-identity, and
where the standing grammar's churn classes (time-churn/asset-churn) would
have fired on a delta, none fired — no churn classification was manufactured
to look thorough. The anchor-checker verifies locate+count only: it claims
nothing about a row's tier, scope or teaches cells, never fetches (the pin
is local; live byte-identity is the separate curl receipt), and prints
counts/shapes only (the selftest redaction arm plants a marker token in the
fixture and proves it cannot reach stdout). The self-found corrections stop
at the audited family (S574–S585): older rows were not audited this round
and none is claimed clean.

## Mistakes

1. class: verification (a shape check whose pattern matched nothing) — the
   first S585 NF check ran `awk -F'|' '/^\| S[0-9]+\|/ && NF!=13'` (the
   same command shape the r71 lesson's Gate records): the pattern requires
   a pipe directly after the digits, so it can never match the actual
   `| S585 | ` row shape — it printed `badNF=0` VACUOUSLY, a green count
   from a matcher that matched zero rows. captured-by: the row-specific
   awk `/^\| S585 \|/ {print "NF=" NF}` printed NOTHING, exposing that the
   earlier zero was vacuous; re-run with the span-corrected pattern
   `^\| S[0-9]+ \|` matched all 360 rows with bad=0. fix: a shape check
   prints its denominator beside the exception count (`rows_matched=360
   bad=0`) — a matcher that matches nothing is a vacuous pass, not a pass;
   the r71-recorded command shape is hereby corrected by this lesson (the
   authoritative NF gate remains the census validator's E01, which
   parses rows regardless of this pattern's span bug).
2. class: verification (fixture expected-values drafted from memory — the
   r71 lesson's own mistake-1 class, repeated) — the anchor-checker's
   first selftest run had 3 of its arms FAIL: I wrote 11 as the fixture
   sentence's word count from memory of the REAL S584 sentence while the
   fixture sentence carries 10 tokens, and the word-count arm counted
   whole-line tokens (skewed by any second sentence sharing the located
   line) instead of the matched occurrence. captured-by: the selftest
   arms themselves (first run rc 1; its output was captured in the
   session only and is NOT in any receipt — disclosed NOT-CAPTURED per
   QUALITY 160, never approximated; the committed run history starts at
   the final bytes, 11/11 x3 in `anchor-check-r72.txt`). fix: expected
   values are DERIVED (`len(text.split())` of the recorded text), never
   recalled; the count arm counts ONE occurrence of the recorded text, so
   a co-located sentence cannot skew it — which is also what makes the
   tool catch the D71-2 class on multi-sentence lines.
3. class: landing (a receipt's summary greps counted their own echoed
   command lines) — the re-verify receipt's first summary printed
   `byte-identical=8 / differs=1` for a 7-fetch receipt: each grep matched
   its own `$ grep -c …` echo line appended one line earlier.
   captured-by: reading the receipt before landing — 8 > 7 fetches
   contradicts the receipt's own body (the wrong-summary build existed
   only in the working tree and was rebuilt; the wrong bytes are
   disclosed here, NOT approximated). fix: receipt summary greps use
   line-anchored patterns (`^verdict:`) that an echoed command can never
   match, and a receipt's counts must be arithmetically consistent with
   its own body before it lands.
4. class: search (a label-pairing audit over-flags when the pairing is
   mechanical) — the family-wide label audit's first pass reported 8
   mismatches; reading each flagged pair against its row text showed 3
   were pairing artifacts (a label nearest-quoted to a section heading or
   an adjacent short quote, not to its own sentence) and 2 hits were prose
   phrases, not labels; the true set is 6 (4 self-found + the 2 routed).
   captured-by: the audit printing its pairing decision (side + gap +
   quote) beside every flag, making the artifacts readable before any
   correction landed. fix: corrections land only on pairs read against
   the row text, never on a pairing heuristic's raw output; an audit
   names its pairing rule. (The audit also stands as evidence that the
   STANDING QUALITY 90 parser cannot see location-token label shapes —
   `(`:829`, 14 words)` — a standing-instrument blind spot named for the
   operator, not worked around silently: this round's committed
   anchor-checker covers per-anchor (line, quote, count) verification and
   the label-blind-spot remains an operator-material note.)

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62/round-65 L0 lines stand open — re-verified unanswered this round
in `.ufo/waves/round-72/evidence/l0-considerthese-r72.txt` — routed around,
never treated as answered). Round 72 ran L1-only over committed bytes, this
host's network and this host's own surfaces; no wave-based evidence is
claimed.

## Assimilation

considerthese mined (all eight files re-listed this round; newest-named
2026-10-26.md — receipt `l0-considerthese-r72.txt`): the 2026-10-26
suggestion 1 (split pin-check mismatches into "can't run here" vs "stale")
remains the one still-unimplemented proposal and remains behind the
operator's open instrument-change ruling (the mori | round-65 L0 line);
suggestions 2–4 stay proposals (suggestion 3 is the standing fresh-start
spot-check practice, re-performed this round). Assimilation: none —
shokuknow unreachable.
