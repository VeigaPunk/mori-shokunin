# Round 67 — mori (L1 MoriR67, the second vendor churn grammar and the receipt-driven standing step)

author: mori L1 (MoriR67)
round: 67
date: 2026-11-01
entering: `8470a025` (`8470a025f94f7449e881c3d8a8c997ed89aa7a9a`, r66 verifier spotcheck tip)

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop` (r66 closed admitted).
Spot-checks re-run this round with own receipts, not cited from r66
(`.ufo/waves/round-67/evidence/freshstart-spotchecks-r67.txt`): the frozen r61
counter re-derived at the r61 data tip (`python
.ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` rc 1 — the same
verdict the r61 closure, the r65 re-derivation and the r66 re-derivation
reached); r59/r60 cited evidence `git cat-file -e` PRESENT and both revisions
`merge-base --is-ancestor` of refs/heads/master, rc 0 each.

Ruled out as r67 claims, and why: (1) re-declaring the r59/r60
entry-claims-class instruments — their met-flip counterexamples stand on
frozen bytes; (2) scalar score moves — no closure states a new number and no
lane convention licenses an L1-authored scalar; (3) claims on the old Linux
host's live surfaces — absent here, honestly `unavailable`; (4) editing the
frozen sweep `tools/mori-source-drift.py` or the r65 adjudicator's committed
behavior — the SKILL:905 tally pin and the r65/r66 receipts bind those bytes;
the r67 work extends only the lane-owned r66 re-check, which pins no SKILL
tally; (5) teaching a third grammar for the instrument-UA bot-manager chrome
— it is per-response serving variance, not a build artifact (QUALITY 159
discloses it; a third grammar would generalize a per-response token);
(6) re-declaring the admitted r64–r66 sweep/disposition/re-check work. Both
declared claims are unreachable by a do-nothing round
(`.ufo/waves/round-67/evidence/controls-r67.txt`: `asset-churn` = 0 and
`from-sweep` = 0 in the entering tool bytes, rc 1 each; QUALITY `^159\.` = 0;
S578 row = 0).

## Carry-ins from the r66 non-author closure (both build items discharged)

1. The stamp grammar is vendor-scoped — discharged as C1: the second vendor
   class (learn.microsoft.com asset-build-id churn, S241) now has its own
   named grammar (`asset-churn`, class name
   `learn-microsoft-asset-build-id` on the header line) instead of the
   disclosed-boundary-only state; QUALITY 159 pins the vendor-scoping rule
   and an append-only erratum on 158 retires its "S241 stays content-drift"
   clause.
2. `--from-sweep <receipt>` — discharged as C2, with the parser enforcing
   the r65 M1 lesson (a summary token is never counted as a row) and a
   rows-vs-summary agreement check the r66 standing step did not have.
3. The r65 L0 (`python3` Store stub naming in SKILL:905) stays open for the
   operator — routed around: no frozen byte edited (both standing instruments
   absent from the round's diff; the tally pin true by construction).

## Gate

One source opened this round, fetched with `curl -sS -m 60 -L` into scratch,
pinned byte-identical into `corpus/evidence/sources-r67/` (S578 sha256
`5c02b66156cd308624a5c8e2f5d8a0a5702ac40c5c07231c3fad05ccf36d2a8b`);
duplicate sweeps before opening: `grep -c "web.dev"` → 0,
`grep -c "http-cache"` → 0, `grep -c "cache.busting"` → 0 at the pre-open
state.

- S578 Prevent unnecessary network requests with the HTTP Cache (web.dev) —
  https://web.dev/articles/http-cache — opened 2026-11-01 — quote
  (`S578.html:4647`, 15 words): "Versioned URLs are a good practice because
  they make it easier to invalidate cached responses."; section heading
  "Long-lived caching for versioned URLs" `:4638`; continuation `:4652`
  ("You can't, at least not without changing the URL of the resource");
  page `<title>` at `:76`.

The row lands `mined`, used-by this lesson. C1's asset-churn grammar rests
on S578 + the vendor's own observed signature: versioned asset URLs are the
deploy-time cache-invalidation mechanism, so a pin-vs-fresh delta confined
to the `/static/assets/<build-id>/` segment (the exact shape the r65 diff
receipt recorded for S241) is the vendor's build pipeline, not page-content
drift.

reject sample: none met — no source rejections this round; the fresh-start
rule-outs above are the round's reject-class decisions.

Census (validator): start receipt
`.ufo/waves/round-67/evidence/census-start-r67.txt` (this host, 2026-11-01,
rc 0, tolerated W04 duplicate-URL class, command + rc line embedded) → end
receipt `.ufo/waves/round-67/evidence/census-end-r67.txt` (rc 0). SOURCES row
count 350 → 351 (S578) counted by `grep -c "^| S" corpus/SOURCES.md`, the
lane's separate row-count instrument.

## Mistakes

1. class: an edit that removes a definition its replacement still calls —
   the r67 re-write of `run()`'s prologue dropped the `emit =` assignment
   while the new header-write still called `emit`; the first execution died
   rc 1 (`NameError: name 'emit' is not defined`). captured-by: the first
   execution of the edited file (a selftest run is cheap; there is no reason
   to batch edits before one). fix: definition restored; every tool edit is
   executed immediately after writing, before anything else is built on it.
2. class: a green selftest over a design gap — the first r67 version taught
   the churn grammars on the instrument-UA arm only, and its selftest passed
   10/10 because the fixtures had no case where the instrument UA is served
   a different variant while the pinning body is grammar-clean; the LIVE
   S241 run then classified `content-drift` at 2026-11-01T10:21:36Z against
   a pinning body whose only delta was the two asset-id lines (the
   pin-vs-live diff: 2 of 1499 lines). captured-by: the live run plus the
   manual pin-vs-live diff — a green selftest proves only the shapes it
   contains; a live surface can veto it the same day. fix: the second-UA arm
   attempts the churn grammars too (after the strict ua-serving equality
   check, so r66's ua-serving/gate semantics are preserved), the fixture
   registry grew to 8 rows with S914 replicating the S241 shape, and the
   whole run history is disclosed in the selftest receipt
   (`.ufo/waves/round-67/evidence/recheck-selftest-r67.txt` header, runs at
   the final bytes PASS (10 cases) ×3, and
   `…/s241-assetchurn-live-r67.txt` carries the pre-fix and post-fix live
   lines side by side).
3. class: the r66 M4 truncation class recurred — the SCORECARD round-67
   section was first appended from a long bash here-document whose delimiter
   was never recognized ("here-document delimited by end-of-file (wanted
   PYEOF)"), cutting the python input mid-string. captured-by: the command's
   own warning plus the SyntaxError before anything was written to
   SCORECARD.md (the r66 fix — landmark verification before staging — was in
   place, so nothing landed truncated). fix: long appends are no longer
   heredocs at all — the section is written to a scratch file first, then
   `cat file >> target`, then the landmark counts are taken (header ×1, both
   claim rows ×1 each, capability row ×1, Planned ×1 — all green before
   staging).

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62/round-65 L0 lines stand open, routed around, never treated as
answered). Round 67 ran L1-only over committed bytes and this host's network;
no wave-based evidence is claimed.

## Assimilation

considerthese mined (2026-10-19…2026-10-26, all eight files; no newer file
exists — checked this round): the 2026-10-26 suggestion 1 (split pin-check
mismatches into "can't run here" vs "stale") is a real still-unimplemented
proposal, but it changes a tally-cited instrument's reported behavior
(pin-check 125/125 is cited in SHONEN box 3), so it belongs behind the
operator's instrument-change ruling (the mori | round-65 L0 line) and is not
adopted this round; suggestion 3 (re-execute what closures only
evidence-verify) was executed again — the frozen r61 counter re-derived this
round in the fresh-start receipt. Assimilation: none — shokuknow unreachable.
