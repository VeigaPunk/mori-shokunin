# Round 71 — mori (L1 MoriR71): C1 calibration verified met (the r70 closure's D1/D2 carry-ins discharged: supersedes row S583 re-points the S582 located-line pointers old→new against the byte-identical re-open, the knowledge entry takes an append-only correction block, QUALITY 162 makes pin-verification procedural, able-to-fail against the drifted pointers themselves); C2 depth verified met, sourced S584 (capability acquisition `tools/mori-workstate-win.py` — the Windows working-state read, the 100-ns unit conversion the doc grounds, `count=biased+unbiased boot_identity=absent` on every line); C3 operability verified met (capability acquisition `tools/mori-events-context-win.py` — the r63-class event counts re-derived WITH the r70-class boot window in one bound receipt, `boot_binding=none` traveling on every line)

author: mori L1 (MoriR71)
round: 71
date: 2026-11-01
entering: `015787e6` (`015787e6f5aa7eb2c3e11066bcef7bf0428c17b6`, r70 verifier spotcheck tip)

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`. Spot-checks re-run
this round with own receipts (`.ufo/waves/round-71/evidence/freshstart-spotchecks-r71.txt`):
the frozen r61 counter re-derived at the r61 data tip (`python -I
.ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` rc 1, the same
verdict the r61 closure and the r65–r70 re-derivations reached); the eight
r59/r60/r61 lane revs `cat-file -e` PRESENT and `merge-base --is-ancestor`
of refs/heads/master rc 0 each; the three fleet report commits (2807c6ab,
eeedfd53, 3bb9b8e7) PRESENT in the fleet repo.

Ruled out as r71 claims, and why:

1. Re-declaring the r59/r60/r61 entry-claims-class instruments — their
   met-flip counterexamples stand on frozen bytes (re-derived unmet again
   this round, receipt above).
2. Scalar score moves — no closure states a new number and no lane convention
   licenses an L1-authored scalar; the head axes table stays untouched
   (append-only SCORECARD, the r69 closure's own check).
3. Claims on the old Linux host's live surfaces — absent here, honestly
   `unavailable` (the Round-62 host note stands).
4. Editing the frozen bytes (SKILL.md, `tools/mori-source-drift.py`,
   `tools/mori-drift-adjudicate.py`, PROVINCE.md, AGENTS.md,
   corpus/README.md) — the SKILL:905 tally pin (the r65 L0) and the r65–r70
   receipts bind those bytes; this round's diff contains none of them. The
   r65 L0 line stays open (re-verified unanswered this round,
   `l0-considerthese-r71.txt`) and was routed around, never treated as
   answered.
5. The rotation recurrence receipt (r70 planned note a) — the r70 closure's
   own re-run already receipts a second-session data point at the ~91 s
   scale (no rotation caught, served body moved on: spotcheck §2 C1); one
   further single-session pair would add a data point, not a finding, and
   the vendor's serving decides what it shows — a recurrence claim worth
   making needs a designed multi-window protocol (a bigger instrument than
   this round carries). Not declared.
6. The cross-check arm's inconsistent branch (r70 planned note c) — the
   vendor's serving arms decide that; the arm stays a standing one.
   Cannot be manufactured honestly, so not declared.
7. In-place edits to any drifted r70 artifact (the opening receipt, the
   fleet report, the lesson, the S582 row anchor) — corrections are new
   entries, never in-place rewrites (contract v1 rule 2; the closure's own
   routing §6). The D1 discharge obeys: supersedes row + erratum + append-only
   correction block; zero frozen or foreign bytes edited.
8. The Precise variant of the unbiased counter (S584:876 names
   QueryUnbiasedInterruptTimePrecise) — stays unopened; the plain count is
   this round's surface and one opening per surface is the rule the r70
   round applied to this same pair of pages.

All declared claims are unreachable by a do-nothing round
(`.ufo/waves/round-71/evidence/controls-r71.txt`: every r71 tool, entry,
pin, receipt and the lesson absent at entering rc 128; SOURCES 355 rows at
entering with zero `supersedes S582` rows and zero matches for the S584
URL; QUALITY `162.` absent at entering).

## Gate

Three source events this round, each fetched with `curl -sS -m 60 -L`,
duplicate sweeps run INTO the receipts first (the r69 lesson's rule):

- S583 (supersedes S582 — the D1 correction row): the SAME GetTickCount64
  page re-opened this round,
  https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64
  — opened 2026-11-01T21:5xZ — the live body is BYTE-IDENTICAL to the r70
  pin (sha256 `580f1935fb47b5c992a48d22299f7452aaeb00099f2ac96ba74c92002a18277f`,
  52661 bytes, receipt `.ufo/waves/round-71/evidence/source-s582-reopen-r71.txt`),
  so the erratum's pin-verified pointers (:834/:841/:842) bind the live body
  too. Quotes re-verified line-by-line in
  `.ufo/waves/round-71/evidence/s582-pointers-erratum-r71.txt`: "The number
  of milliseconds." at `:834` (recorded `:833`, which is the
  `<h2 id="return-value">` heading — `grep -c` returns 0 there and 1 at
  :834); the working-state boundary sentence at `:841` (recorded `:842`, the
  alert div); the ~49-day alert at `:842` (recorded `:845`, the
  `<h2 id="requirements">` heading). `:829`/`:831`/`:836` confirmed exact.
  Pre-row sweep: `nf-sysinfoapi-gettickcount64` = 1 (the S582 row itself —
  receipted as EXPECTED for a supersedes correction row, not a new surface).
  The row lands `mined`, used-by the correction block in
  `corpus/knowledge/uptime-win-r70.md`, `corpus/knowledge/workstate-win-r71.md`,
  and this lesson. S582's own row bytes are UNCHANGED (the anchor cell is
  immutable; contract v1 rule 2).

- D2 precision correction (old→new, status-neutral): the r70 lesson's Gate
  recorded the S582 pre-row sweeps as "`gettickcount64` 0, `sysinfoapi` 0";
  the r70 receipt (primary evidence, `source-s582-r70.txt:5-11`) records
  `gettickcount64 rows=0 rc=1` and `sysinfoapi rows=1 rc=0` — the 1 is the
  S574 row (GlobalMemoryStatusEx, same sysinfoapi tree, whose row text the
  keyword matches). The page-identifying `gettickcount64` sweep was and is
  0, so the no-duplicate admit decision stands; the r70 lesson prose
  mis-stated the receipt. Corrected here (the next lesson, per the closure's
  routing §6 D2); the r70 lesson bytes stay untouched.

- S584 QueryUnbiasedInterruptTime,
  https://learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-queryunbiasedinterrupttime
  — opened 2026-11-01T22:03:48Z — quotes (`S584.html:817`, 11 words): "Gets
  the current unbiased interrupt-time count, in units of 100 nanoseconds.";
  (`:817`, 17 words): "The unbiased interrupt-time count does not include
  time the system spends in sleep or hibernation."; signature (`:819-820`)
  `BOOL QueryUnbiasedInterruptTime(PULONGLONG UnbiasedTime)`; failed-call
  signature (`:826-827`, 22 words): "If the function succeeds, the return
  value is nonzero. If the function fails because it is called with a null
  parameter, the return value is zero."; zero-at-boot (`:828`, 24 words):
  "The interrupt-time count begins at zero when the system starts and is
  incremented at each clock interrupt by the length of a clock tick.";
  working-state semantics (`:830`): "reflects only the time that the system
  is in the working state"; debug-build alert `:833`; Precise variant `:876`
  unopened. Copy `corpus/evidence/sources-r71/S584.html` sha256
  `d0bcbba945e7cf29d4664feb28a35aa31c1f80cadb5191644a33ab84464f9136`
  (54774 bytes). Sweeps INTO `.ufo/waves/round-71/evidence/source-s584-r71.txt`
  BEFORE the fetch: the API-name keyword `queryunbiasedinterrupttime`
  (case-insensitive) = 1 — receipted with its interpretation BEFORE anything
  cited the row: the hit is the S582 row's own K4 quote text, not a row for
  this page; the page-identifying URL-slug sweep
  `nf-realtimeapiset-queryunbiasedinterrupttime` = 0 rc 1 (no duplicate).
  The row lands `mined`, used-by `corpus/knowledge/workstate-win-r71.md`
  (C2's entry) and this lesson.

Both rows appended INSIDE the Registry section immediately after S582
(position verified: S583 at SOURCES.md:364, S584 at :365). SOURCES row count
355 → 357 counted by `grep -c "^| S" corpus/SOURCES.md`; the 13-field check
`awk -F'|' '/^\| S[0-9]+\|/ && NF!=13'` prints badNF=0. QUALITY 162 landed
(pin-verification rule, able-to-fail against the drifted pointers
themselves).

reject sample: the boundary applied against the tempting-to-overreach
readings of C2 — the probe prints two counts and their derived delta and
nothing else: no sleep/hibernation episode attribution, no boot
decomposition, no power-state diagnosis (tsukuroi/operator ground; PROVINCE
refuses), no liveness verdict, and the delta's negative readings on this
host (-7/-12/-11 ms, receipt `workstate-live-r71.txt`) are reported AS the
declared read model predicts (two separate read instants), not smoothed into
a prettier story. Likewise the pairing claim (C3) prints
`boot_binding=none` — the events window is RECENT-N, not boot-scoped; the
pair shares the host, never a time window, and the receipt says so on every
line rather than implying a boot-scoped count.

## Mistakes

1. class: verification (a selftest fixture drafted with unit arithmetic
   from memory — twice) — the C2 selftest's good-case fixture first set
   `unbiased_100ns=977_184_000_000` (that is 97_718_400 ms, not the 977_184 ms
   the grammar arm expected: a 100x slip), and after fixing the magnitude the
   delta-equal case still read 976206816 because 977184000 ms equals
   9_771_840_000_000 100-ns units (x10000 exactly — another from-memory
   slip, caught by hand-diffing the rendered line), and the grammar arm's
   expected literal then still spelled the stale values for a third 9/10
   run. captured-by: the grammar arm itself, three consecutive FAIL receipts
   (`workstate-selftest-r71.txt` carries all three runs' history and the
   fix narrative; the 10000x trap is exactly what the `unit_math` arm
   exists to pin). fix: fixture values are DERIVED from the pinned
   sentence — ms x 10000 — never recalled; the fixture and its expected
   literal are edited in the same change; a 9/10 selftest is a landing
   stop, not a warn.
2. class: verification (a rc-masking pipe on battery output) — the first
   battery attempt piped each selftest through `tail -1` and captured
   `$?` of the PIPE (tail), so mori-register-check's UnicodeDecodeError
   crash printed with `rc=0` beside it. captured-by: cross-reading the
   receipt — a traceback and rc=0 on the same lines contradict each other
   (the r9 lesson's own subject: `pipefail`/PIPESTATUS; here the pipe was
   not even rc-gated). fix: receipt rc capture is unpiped (`> file;
   echo rc=$?`), the summary line extracted as a separate read; a receipt
   line never carries a verdict token produced by a different process than
   the one whose rc it prints.
3. class: calibration (an interpreter-posture change dressed as hygiene) —
   that first battery also ran `python -I` while the standing battery
   convention (r70 receipt) is plain `python`: isolated mode ignores the
   host's PYTHONUTF8=1, the fixture `write_text` fell back to cp1252, an
   em-dash became byte 0x97, and the utf-8 read-back crashed — an
   environment dependency of a standing instrument, exposed by a posture
   change that LOOKED like extra rigor. captured-by: the unpiped rerun
   (12/12 rc 0) plus the two-line env probe (preferred encoding utf-8
   without `-I`, cp1252 with it), receipted in the battery header. fix: a
   rerun that cites a prior receipt's numbers states its posture and keeps
   it identical; the encoding dependency is disclosed in the battery
   receipt (no tool edit this round — a versioned encoding pin is routed
   beside the open r65 L0 as operator material).
4. class: landing (a receipt header claimed a capture it did not hold) —
   the events-context selftest receipt's first header said the pre-fix
   TypeError traceback was "receipted below verbatim" while the corrected
   receipt had already replaced the bytes that held it. captured-by:
   re-reading the receipt before landing (the claim and the bytes
   disagreed — the same read-back rule that caught r70's placeholder
   digest). fix: rewritten as a NOT-CAPTURED disclosure naming the QUALITY
   160 convention (not-captured is disclosed, never approximated); a
   receipt asserts only captures it actually holds.
5. class: search (a duplicate sweep read without its page-identifying
   form) — the S584 pre-row API-name sweep returned 1, which in isolation
   reads as "duplicate present"; the hit is the S582 row's own QUOTE text
   (its K4 sentence names QueryUnbiasedInterruptTime), and the
   page-identifying URL-slug sweep is 0. captured-by: interpreting the
   sweep before landing the row — a rows=1 against a page that cannot
   already have a row demanded a look at WHAT matched (`source-s584-r71.txt`
   carries both sweeps and the interpretation, receipted before the fetch).
   fix: a duplicate sweep names its page-identifying form (the URL slug);
   a keyword that occurs inside another row's quote text is expected to hit
   and is not a duplicate signal. (QUALITY 19's inspect-before-citing,
   applied to the sweep itself.)
6. class: landing (a registry cell carried prose where a path was parsed) —
   the S583 used-by cell was written as
   `corpus/knowledge/uptime-win-r70.md (r71 correction block), …` and the
   census validator's used-by parser took the parenthetical along as path
   text: the round-end census returned rc 1 with E11 "S583 missing used-by"
   (`.ufo/waves/round-71/evidence/census-end-first-attempt-r71.txt`, the
   not-captured disclosure; the fix + the rc 0 rerun in
   `census-end-r71.txt`). captured-by: the round-end validator itself — the
   gate the round contract runs at round end; the row was fixed in place
   (used-by is mutable, contract rule 2) before anything cited it. fix: a
   used-by cell is exactly comma-separated repo-relative paths; prose about
   WHY a path cites the row belongs in the row's teaches cell or the
   lesson, never inside a parsed list.

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62/round-65 L0 lines stand open — re-verified unanswered this round in
`.ufo/waves/round-71/evidence/l0-considerthese-r71.txt` — routed around,
never treated as answered). Round 71 ran L1-only over committed bytes, this
host's network and this host's own surfaces; no wave-based evidence is
claimed.

## Assimilation

considerthese mined (all files re-listed this round; newest-named
2026-10-26.md — receipt `l0-considerthese-r71.txt`, which also carries the
disclosed correction of its own first newest-file line, an `ls -t` tie on
equal checkout mtimes): the 2026-10-26 suggestion 1 (split pin-check
mismatches into "can't run here" vs "stale") remains the one
still-unimplemented proposal and remains behind the operator's open
instrument-change ruling (the mori | round-65 L0 line); suggestions 2–4 stay
proposals (suggestion 3 is the standing fresh-start spot-check practice,
re-performed this round). Assimilation: none — shokuknow unreachable.
