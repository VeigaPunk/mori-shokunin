# Mo97CritC2 — falsification attack on C2 (freshness), mori round 97 w1

Attack performed on landing `e85ed91249953094b067554bfa79fcdc65791f8e` vs entering
`973b2af11f41bd362163d7e29ac08286832f546b`, frozen counter `count-c2.py`
(sha256 `957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91`, verified identical at
worktree, at freeze `dd1ae1150f53df54e7530311b2323368e3c0e5e9`, and at landing). All runs in scratch
`$HYAKU_SCRATCH/mori-r97/Mo97CritC2` (removed on exit); live legs fetched docs.python.org read-only.

## 0. Ground truth re-established independently

- `git diff --stat` entering..landing: ONLY wave artifacts, SKILL.md +17 (C1), `corpus/SOURCES.md` +1
  line (S628), the three pins `corpus/evidence/sources-r97/S6{15,16,23}.html`, `S628.md`, lesson. **No
  tool edited, no S615/S616/S623/S619 row edited, no recorded digest edited.** S619 present at entering
  (`git show 973b2af1:corpus/SOURCES.md | grep -c '| *S619'` → `1`).
- Pins verified: `sources-r97/S615.html` = `7891c588…42f5` (= S619's corrected digest), `S616.html` =
  `6842ed0f…cb72` (= recorded), `S623.html` = `90ac3b25…31ad0` (= recorded), `S628.md` = `0ae6b880…c618`.
- Provenance: `S615.html` is **byte-identical** (cmp) to the r90 archive copy
  `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`; `S616.html` byte-identical to
  `…/python-tokenize-3.15.2.html` (`6842ed0f…cb72`). Real archival bytes, not reconstructions.
- Baseline rerun (F0): `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass
  live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=-` exit=0 — matches landing-c2.txt.

## (a) Reconstruction vs re-verification; does leg (d) prove live content unchanged?

S623's pin is a **reconstruction**: today's live page with the build-stamp line restored
(lesson: live `57b7f76b…6811` → stamp `(08:02 UTC)` restored → `90ac3b25…31ad0` = recorded). As a file
provenance it is archival repair — disclosed as such in contract and lesson ("reconstructed bytes;
sha256 equality with the recorded digest proves them the recorded fetch"). But the sha equality is
against a digest recorded **pre-round** (S623's row is not in the landing diff), so it is not circular:
preimage resistance makes "today's live content, modulo one stamp line, equals the recorded bytes" a
genuine live-surface re-verification, exactly the AXES freshness row's "re-verified against live
surfaces; stale items flagged or fixed". The pin is both repair and proof.

Leg (d) is a real content check, not a stamp glance. `tools/mori-drift-recheck.py` classifies
`time-churn` only when `stamp_free(copy) == stamp_free(body)` — the **whole-body line sequence** after
dropping lines matching the strict stamp regex; any changed teaching line breaks equality →
`content-drift` → counter `failed.append("live")` → unmet. `excerpt` (substring) and `fresh` order
before it; LIVE_OK = {fresh, time-churn}. My F6 demonstrates detection live (below).

## (b) Forgeries built in a scratch archive of the landing (count-c2.py unchanged)

- F1 r98 decoy: junk 100 B at `sources-r98/S616.html` → `TARGET S616 ok copy_matches_tool=no …
  checks_failed=target_S616` → **unmet** (newest_copy hijack caught).
- F2 r98 decoy sized 362,493 B at `sources-r98/S615.html` → digest tool `unpinned` (ambiguous pinned
  copy: two 362,493-byte candidates) and counter `TARGET S615 unpinned … hole_guard=n/a` → **unmet**.
- F3 junk overwrites true `S616.html` → `TARGET S616 mismatch`, `mismatch=1` → **unmet**.
- F5 true `S623.html` + one appended stamp-format line → sha breaks the size/prefix pairing →
  `TARGET S623 unpinned`, `unpinned=1` → **unmet** (stamp window not abusable without breaking legs a–c).
- F6 URL swap (S616 row URL → another live docs page), correct pins → `LIVE S616 content-drift`,
  `checks_failed=live` → **unmet on the live leg alone** (mirrors pre-committed control c2-contentdrift).
- F4 coordinated forgery: pin = today's live bytes minus the stamp line, SOURCES S616 digest edited to
  its sha (`9206a43c…e28b`) → legs (a)–(c) green, live `time-churn` (stamp-free equal) → **`C2=met`**.
  **This is the one forgery that scores green**: the counter cannot distinguish a coordinated
  registry+pin rewrite. It is bounded: the forged pin is still live-true content (freshness vs live
  holds); what is lost is provenance ("bytes the recorded digest names"), and SOURCES.md integrity is
  not a counter property but a repo property — verified here by the entering→landing diff (only +S628)
  and by seat rules. Not a falsification of the frozen claim; an instrument boundary to record.

## (c) Operator L0 (stale digests) and S615 honesty

L0 `.ufo/l0-questions.md:355` (mori | round-96) offers (a) supersession rows per CORPUS rule 2, (b)
recheck cadence, (c) recorded debt. Round 97 respects it: no supersession row appended for S616/S623,
no digest edited (diff-proven), and the contract states the L0 is "not treated as answered". The
mechanism used for S615 rides the **pre-existing** S619 row (r91 correction C-1, present at entering),
whose text itself says "supersedes S615 — the registry should record this full digest; the ast facts
S615 teaches are unchanged". The digest tool's own selftest shows supersession fires only for an `ok`
successor of a `mismatch` predecessor, and the counter's hole_guard forces the S615 copy to hash to
S619's digest (control `random 362493-byte S615 copy` → `hole_guard=fail`). `superseded-by S619` is
honest. Wording caveat: contract sentence "pin … the exact bytes each row's recorded digest names" is
literally true only for S616/S623; for S615 the pin matches the correction row's digest — the contract
parenthetical discloses this, so no amendment needed, but the sentence should not be quoted without it.
The round also produces exactly the evidence the L0 asks for: all three rows live ≡ recorded modulo
one stamp line (S615 `d5d9d590…`/restored→`7891…42f5`; S616 `bce32489…`/restored→`6842…cb72`; S623
`57b7f76b…`/restored→`90ac…31ad0`), grounding the stamp-churn reading via new row S628.

## (d) Do-nothing control

before-c2.txt (entering tree): `C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a
live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,…` exit=1 — the entering state
**fails**, so the claim is not a do-nothing pass (r94/r95 root cause avoided). Positive control
(c2-positive) and all forgery controls ran pre-freeze with `CONTROLS_DONE unexpected=0`.

## Receipts cited (copied)

- before-c2.txt tail: `C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,target_S615,target_S616,target_S623,live … exit=1`
- landing-c2.txt tail: `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=- … exit=0`
- controls-r97.txt: `EXPECT rc=1 contains='hole_guard=fail'` → `C2=unmet … hole_guard=fail`; `EXPECT rc=1 contains='C2=unmet mismatch=1'` → met by `mismatch=1`; c2-contentdrift → `LIVE S623 content-drift`, `checks_failed=live`; c2-positive → `C2=met … exit` 0.

## Verdict

Every attack vector failed to break the claim as frozen: do-nothing fails at entering; byte pins
verified against recorded digests and (S615/S616) against r90 archival bytes; the live leg detects real
content change (F6); decoys, junk pins, stamp insertions, and random-size holes all score unmet. The
single green forgery (F4) requires editing the frozen registry itself and yields live-true content —
an instrument trust boundary, not a claim defect. C2 survives falsification.

VERDICT C2 holds: pins match recorded digests (S615/S616 = r90 archival bytes; S623 reconstruction
proved by sha equality with the pre-existing recorded digest), leg (d) is a full-content live
comparison (content-drift on F6), hole/decoy/junk forgeries all unmet; residual: counter green is
conditional on SOURCES.md integrity (F4), guaranteed by the entering→landing diff, not by the counter.
