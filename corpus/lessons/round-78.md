# Round 78 — mori (L1 MoriR78): the r77 recovery landed — C1 operability verified met (D77-1 `tools/mori-counter-win.py` committed as NEW commit `4ce9e438` at the receipted sha `e6c527db…`, selftest 12/12 + live AVAILABLE surfaces=4 ok=4 re-receipted AT THE LANDED BYTES; D77-2 the canonical capabilities row, headings 26 -> 27, first-working 77); C2 calibration verified met (D77-3 the correction of record: the r77 landing `6a230c4b` is 21 paths and does NOT contain the tool — append-only, no r77 artifact edited); C3 freshness verified met, sourced S593 opened this round (pin-family rows=7 rc 0: ua-serving x3, fresh x2, time-churn x1, asset-churn x1; the parse_registry paren-truncation caught, cause-receipted, and routed around by a byte-identical row-side URL re-point — no registered instrument byte edited)

author: mori L1 (MoriR78)
round: 78
date: 2026-11-02
entering: `ecb916ce` (`ecb916ce0105c37142aef08def00d95ec70cf503`, the r77 verifier-spotcheck tip)

## Fresh start (r59/r60/r61 rejected closures re-read and re-derived; what was ruled out)

The §7 digests name r60/r61/r77 `rejected-honest-stop` (r77 is this lane's immediate
predecessor; its spotcheck `corpus/lessons/round-77-verifier-spotcheck.md` was read
in full first and its three routed defects ARE this round's work). Spot-checks
re-run this round with own receipts
(`.ufo/waves/round-78/evidence/freshstart-spotchecks-r78.txt`): the frozen r61
counter re-derived at the r61 data tip (`python -I .ufo/waves/round-61/count-c2.py
986d4b46…` -> `C2=unmet` rc 1, the same verdict every closure and the r65-r77
re-derivations reached); ten r59/r60/r61 lane revs PRESENT and
`merge-base --is-ancestor` of refs/heads/master rc 0 each; the three fleet report
commits (2807c6ab, eeedfd53, 3bb9b8e7) PRESENT in the fleet repo.

Ruled out as r78 claims, and why:

1. Amending or rewriting `6a230c4b` to "fix" the r77 landing — the spotcheck's own
   instruction is a NEW commit; history stays frozen. Discharged as D77-1 (commit
   `4ce9e438`).
2. Editing the r77 report/LOG/SCORECARD/SHONEN clauses that carry the false
   landing wording — frozen history; the correction of record rides append-only
   (the r75/r76 corrections-of-record precedent). Discharged as D77-3.
3. Editing the drift re-check's parse_registry so it carries parenthesized URLs —
   a registered, tally-pinned instrument; the mori | round-65 instrument-change
   L0 stays open. Routed around with the row-side percent-encoded URL re-point
   (byte-identity to the pin proven by cmp rc 0 before the re-point landed).
4. The boot-scoped events window (the mori | round-65 L0) and the label-sweep
   instrument (the mori | round-73 L0) — both re-verified unanswered this round;
   routed around, never treated as answered.
5. The considerthese suggestion 1 (split pin-check mismatches "can't run here"
   vs "stale") — behind the same instrument-change ruling; stays proposal.
6. A fourth rotation-schedule session — the series waits for wall-clock distance
   (the r75 planned head (d)).
7. Manufacturing a supersedes row for the ua-serving classifications (S591 r77,
   S592 and S593 this round) — the pins are immutable, the anchor receipts hold,
   QUALITY 159's grammar adjudicates; no supersedes owed, no manual registry edit.
8. Re-trying the r59-r61 frozen-counter claims — the entries stay indexed with
   honest status notes; the r61 counter re-derived `C2=unmet` again this round.
9. Scalar score moves — no closure states a new number and no lane convention
   licenses an L1-authored scalar; the axes table untouched.
10. Linux-host live surfaces and L2 wave dispatch — absent on this host (carried
    disclosure; the three open mori L0 lines re-verified present and unanswered).

All declared claims are unreachable by a do-nothing round (controls receipt:
`.ufo/waves/round-78/evidence/controls-r78.txt`).

## Gate

One NEW source opened this round; the duplicate sweep ran INTO the receipt BEFORE
the fetch (the r69 lesson's rule), the resolved page `<title>` was checked before
the pin (the r75 lesson's rule), and word counts were wc -w-verified before the
pin (QUALITY 90):

- S593 — https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/aa965225(v=vs.85)
  ("Memory Performance Information", Windows desktop legacy archive, Microsoft
  Learn) — opened 2026-11-02 — located quotes (wc -w-verified, then
  machine-verified by the r72 anchor-checker): "This topic associates performance
  counters with the data returned by memory performance functions and the Windows
  Task Manager" (`S593.html:713`, 18 words); "The following table associates
  memory object performance counters with the data returned by the memory
  performance functions in the" (`:720`, 19 words — the sentence continues through
  three linked structure names on the same line, so the located contiguous span
  ends at "the", recorded as such); "Memory object counter (unless otherwise
  noted)" (`:730`, 6 words); "Committed Bytes" (`:750`, 2 words); "Commit Limit"
  (`:756`, 2 words). Pinned copy `corpus/evidence/sources-r78/S593.html` sha256
  `7eb834fc1450f8f93d94e11cd66c4c7a84049631ca1b1032ffbb3019ff6a9bac` (48532
  bytes). Pre-row duplicate sweep = 0 rows on the URL / "PerfOS" / the WMI class
  name, receipted INSIDE `.ufo/waves/round-78/evidence/source-s593-r78.txt` BEFORE
  the fetch, with the interpretation named (nearest held rows S572/S574/S592 are
  sibling surfaces, not this page). FOUR wrong-URL candidates were fetched first
  and rejected as 404s (the cimwin32prov, wmisdk and aa394346 paths) — recorded in
  the receipt; the located page was found via a search of the vendor's own tree.
  All five anchors machine-verified: PASS items=5 ok=5 rc 0 + the able-to-fail
  mislocation arm FAIL rc 1 (`.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt`).
  The row landed at SOURCES.md:374 INSIDE the Registry immediately after S592
  (:373); rows 365 -> 366 counted by
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; the
  13-field shape check reads badNF=0 over all 366 rows; prefix lines 1-373 and the
  suffix byte-proven in the insert script output. Used-by cells S572 (:352),
  S574 (:354) and S592 (:373) gained `corpus/knowledge/counter-semantics-r78.md`
  in place (old->new logged in LOG.md and the receipt). Knowledge entry
  `corpus/knowledge/counter-semantics-r78.md` (K1–K4 + the named Pages/sec
  absence + limits/boundaries); README knowledge-index row appended 858 -> 859
  with the entering 858 lines byte-identical.

Admitted: S593 (tier A for the counter-name association scope; official vendor
documentation of the Windows memory-performance surface, opened and pinned this
round). Rejected: none this round — the four 404 candidates were fetch failures,
not registry candidates. Post-opening instrument finding, receipted in the same
receipt: the row's parenthesized URL is truncated by the drift re-check's
parse_registry; the standing family arm first classified S593 `unavailable`; the
cause chain (isolated re-run, direct mod.fetch samples 5/5, the parse repr) is
receipted, and the row URL was re-pointed to the RFC-equivalent percent-encoded
form after cmp-proven byte-identity to the pin; the final family arm reads
rows=7 adjudicated=7 unavailable=0 rc 0 (`pin-family-r78.txt` first run +
`-s593-isolated.txt` + `-final.txt`).

## Mistakes

1. class: verification (a receipt header written with a PLACEHOLDER run stamp) —
   the round-start census was launched foreground, hit the harness's 120s tool
   timeout, was moved to the background mid-run (the r74 process-spawn budget
   rule applies to the census too), and the completed output was redirected into
   a receipt with no captured stamp; a header was then drafted with a guessed
   "17:5xZ" stamp — caught by the no-fabrication rule BEFORE it could land.
   captured-by: the rule that a receipt's stamp must be provable. fix: the
   census was RE-RUN with the stamp captured by the same command that writes the
   receipt (`census-start-r78.txt`, run-start=2026-11-02T17:53:14Z) and the
   headerless first attempt was DISCARDED, never patched up; standing — a
   receipt whose stamp cannot be proven is re-run, never back-filled, and the
   census joins the backgrounded set.
2. class: verification (a sweep-interpretation line written from memory,
   contradicting the file it summarized) — the S593 receipt's first draft said
   "the r64 probe's GlobalMemoryStatusEx page is not a registry row"; re-reading
   the sweep hits before the fetch showed it IS one — S574, mined r64.
   captured-by: re-reading the hits the interpretation names (the Gate's own
   sweep discipline). fix: corrected pre-landing with the correction noted in the
   receipt; standing — a receipt's interpretation lines are checked against the
   hits they name before the next Gate step consumes them.
3. class: verification (a counting check with the wrong constant) — the first
   badNF check tested `pipes != 13`; a 13-field row carries 12 pipes (awk NF==13),
   so the check flagged all 366 rows. captured-by: the flag pattern itself — a
   check that flags EVERY row is telling you the check is broken, not the data.
   fix: re-run with the awk NF form, badNF=0 over 366; standing — when a counting
   check flags 100% of its population, suspect the constant before the data.
4. class: landing (a generator's string escapes warning at runtime) — RECURRED
   TWICE this round: the D77-2 SCORECARD append generator emitted SyntaxWarning
   `invalid escape sequence '\M'` and the LOG/SCORECARD correction generator
   emitted `'\|'` — the r77 mistake 5 class, not applied at write time despite
   being recorded as a standing fix. captured-by: the warnings themselves.
   fix: landed bytes verified correct post-hoc both times (single-backslash
   counter paths x4, zero doubled leftovers in the capabilities row; the replaced
   strings found and corrected); standing is now explicit — backslash-bearing
   literals in ANY generator take raw strings or chr(92) assembly at WRITE time,
   because post-hoc byte verification is a net, not a fix.
5. class: landing (a receipt written in a format its own stated counting command
   cannot read) — the first battery run wrote per-tool results as
   `rc=0_marker_rc=0` lines, which the anchored `grep -c "^rc=0$"` counting form
   (the receipt's own documented method since r74) cannot count. captured-by:
   re-reading the receipt against the D73-2 counting-method rule before use.
   fix: the run was stopped and re-run with one `rc=<n>` line per tool — 12/12
   counted by the anchored form; standing — a receipt's format is chosen so its
   own stated counting command works on it.

## Foreign evidence found in the worktree (disclosure, not a claim)

The whole-worktree sweep (`git ls-tree -r HEAD` vs disk — the index on this host
reads stale, so `git ls-files` was not used; generator run from the round scratch
dir with `python -I`) found: the three r76 foreign receipt files still disk-only
and uncommitted (`.ufo/waves/round-76/evidence/source-s591-sweep-r76.txt`,
`s591-source-r76.txt`, `win-family-live-r76.txt`) — the leave-for-operator ruling
stands, NOT committed and NOT cited by this round; and 14 disk-only paths, ALL of
them this round's own artifacts (the round-78 evidence receipts, the S593 pin,
the knowledge entry), each scheduled into this round's landing commit. The
D77-3 class (an own artifact listed disk-only, then mis-filed as committed
without checking the actual commit) is closed by the post-landing `git ls-tree`
re-check receipted in the round report. The r76 closure's `tools/__pycache__`
note stands (interpreter bytecode, excluded from the walk; operator may sweep).
Receipt: `.ufo/waves/round-78/evidence/foreign-sweep-r78.txt`.

## Wave

None — no dispatch surface on this host (carried disclosure; the three open mori
L0 lines — round-62, round-65, round-73 — re-verified present and unanswered this
round, routed around, never treated as answered). Round 78 ran L1-only over
committed bytes, this host's network and this host's own surfaces; no wave-based
evidence is claimed.

## Assimilation

considerthese mined (all eight files re-listed this round; newest-named
2026-10-26.md): the 2026-10-26 suggestion 1 (split pin-check mismatches into
"can't run here" vs "stale") remains the one still-unimplemented proposal and
remains behind the operator's open instrument-change ruling (the mori | round-65
L0 line); suggestions 2–4 stay proposals (suggestion 3 is the standing
fresh-start spot-check practice, re-performed this round with own receipts).
Assimilation: none — shokuknow unreachable.
