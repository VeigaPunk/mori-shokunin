author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mori round-71 verifier spot-check (closure, non-author)

Lane: mori-shokunin, round 71. Base `015787e6f5aa7eb2c3e11066bcef7bf0428c17b6` → tip
`3627fac03f00ee904b45c9a9511b842356b1b46b` (branch `master`). All commands below were run by
this closure at `C:/Users/jpvei/.zcode/workspace/95b1ba4d-5089-47a4-9fd8-54adebbce2ae/fleet/mori-shokunin`
unless stated. Redaction rule observed: counts and shapes only.

## 1. Step-1 conformance — PASS

- Report committed in the fleet repo by the lane identity:
  `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-71/mori.md`
  → `mori-shokunin <mori@shokunin.local> a85534c6deb60b0c5f4cd1e780745d5f4a397a42`.
- `## SHONEN` heading present in the COMMITTED report bytes, 4 boxes, all `[~]` with resolvable
  pointers (`git show a85534c6:.ufo/reports/round-71/mori.md`, lines 172–177).
- Cited lane hashes: `015787e6f5aa…` (entering) and `3627fac03f00…` (measured tip) both exist;
  `git merge-base --is-ancestor 015787e6… 3627fac0…` → yes; tip == `refs/heads/master`.
- Pushed: `git ls-remote origin refs/heads/master` → `3627fac03f00ee904b45c9a9511b842356b1b46b`
  == local master (ahead=0).
- Round work reachable in `015787e6..3627fac0`: `git diff-tree -r --stat` → 25 files,
  +3246/−4; the only − lines are SHONEN.md's four evidence lines; none of the six frozen bytes
  (SKILL.md, PROVINCE.md, AGENTS.md, corpus/README.md, mori-source-drift.py,
  mori-drift-adjudicate.py) appear in the diff. Matches the report's landed-changes list exactly.
- Watchdog digest consistency: local master == ls-remote == `3627fac0` matches the
  `complete mori round=71 head=3627fac0 pushed=True` digest line.

No conformance defects found.

## 2. Claim re-checks (all re-measured by this closure — none evidence-only)

### C1 — calibration (carried-in D1/D2 discharge): VERIFIED MET

Before, at `015787e6` (all four reproduce the report):

```
git cat-file -e 015787e6:.ufo/waves/round-71/evidence/s582-pointers-erratum-r71.txt  → rc 128
git show 015787e6:corpus/SOURCES.md | grep -c "supersedes S582"                      → 0
git show 015787e6:corpus/QUALITY.md | grep -c "^162\."                               → 0
git show 015787e6:corpus/evidence/sources-r70/S582.html | sed -n '833p' | grep -c "The number of milliseconds."  → 0
```

After, at `3627fac0` (all reproduce):

```
git show 3627fac0:corpus/SOURCES.md | grep -c "supersedes S582"   → 1   (S583, line 364, INSIDE ## Registry (3..366), directly after S582 at :363)
git show 3627fac0:corpus/QUALITY.md | grep -c "^162\."            → 1
# able-to-fail pair on the pinned S582 copy, re-run by closure:
sed -n '833p' pin | grep -c "The number of milliseconds."          → 0   (line 833 is <h2 id="return-value">…)
sed -n '834p' pin | grep -c "The number of milliseconds."          → 1
sed -n '841p' pin | grep -c "To obtain the time the system has spent in the working state…"  → 1  (recorded :842 → 0, alert div)
sed -n '842p' pin | grep -c "advanced by approximately 49 days"    → 1  (recorded :845 → 0, <h2 id="requirements">)
sed -n '829p' pin | grep -c "Retrieves the number of milliseconds…" → 1 ; :836 → 1 (confirmed-exact pointers)
```

Byte-identity of the S582 re-open re-proven by closure, not read from the receipt: committed pin
`corpus/evidence/sources-r70/S582.html` sha256 `580f1935fb47b5c992a48d22299f7452aaeb00099f2ac96ba74c92002a18277f`
(52661 bytes) == receipt's recorded value, and a fresh closure `curl` of the live GetTickCount64
URL today returns the SAME sha256 and byte count — the corrected pointers bind the live body.

QUALITY 162 able-to-fail shape confirmed: criterion 162 (QUALITY.md:1704) requires "a grep of the
exact sentence against that one line returns 1" — it fails on every drifted pointer above, and
below (§5, defect routed) it fails on the round's own new S584 row, which is the demonstration
working. D2 disposition verified: round-71 lesson Gate lines 88–96 carry the old→new correction
(r70 lesson said `sysinfoapi` sweep 0; r70 receipt records `sysinfoapi rows=1` = the S574 row;
page-identifying `gettickcount64` sweep was and is 0; admit decision stands; r70 lesson bytes
untouched — SOURCES.md committed diff is exactly 2 insertions, the S583+S584 rows, 0 deletions).

### C2 — depth (capability `tools/mori-workstate-win.py`): VERIFIED MET

Executed by closure on the committed bytes, 2026-11-01:

```
python tools/mori-workstate-win.py --selftest   → WORKSTATE_WIN_SELFTEST: PASS (10 cases), rc=0, x3
python tools/mori-workstate-win.py              → WORKSTATE_WIN: AVAILABLE surfaces=1 ok=1, rc=0, x3
```

Live lines carry `conversion=unbiased_ms-floor(10000) read_model=two-separate-reads
count=biased+unbiased boot_identity=absent debug_build_caveat=carried`; closure observed deltas
−11/−4/−7 ms at biased_ms≈497.7e9 (same shape as the receipt's −7/−12/−11 at ≈493.6e9 — the
declared two-separate-reads skew). The unit-floor conversion is real code
(`unbiased_100ns // 10000`, named on the line); the failed-call arm is real
(`ok == 0 → WorkstateUnavailable("qunbiased_return_zero")`, never a zero count — S584:826-827);
`conversion_floor` and `zero_is_real` selftest arms present and passing. Entry
`corpus/knowledge/workstate-win-r71.md` K1–K6 present. S584 pin verified by closure: sha256
`d0bcbba945e7cf29d4664feb28a35aa31c1f80cadb5191644a33ab84464f9136` (54774 bytes) — and a fresh
closure `curl` of the live QueryUnbiasedInterruptTime URL returns the same sha256 (byte-identical
today). One located-line defect inside this claim's evidence trail — see §5 (status-neutral,
routed; the claim's substance and every quote text verify).

### C3 — operability (capability `tools/mori-events-context-win.py`): VERIFIED MET

Executed by closure on the committed bytes, 2026-11-01:

```
python tools/mori-events-context-win.py --selftest  → EVENTS_CONTEXT_SELFTEST: PASS (10 cases), rc=0, x3
python tools/mori-events-context-win.py             → EVENTS_CONTEXT_WIN: PAIRED events_ok=1 uptime_ok=1, rc=0, x3
```

Live receipts bind `matched=209 window=200 surfaces=4 ok=4` with `uptime_ms≈497.98e9
count=biased boot_identity=absent` on the same receipt and print `boot_binding=none
events_window=recent-200-not-boot-scoped` on every line — matching the committed
`events-context-live-r71.txt` (matched=209, uptime_ms≈494e9, boot_binding=none x3).
Redaction arm verified able-to-fail by code read + selftest case 7: fixture child output carrying
computer/user/path/token values is parsed for the summary line only; the selftest asserts none of
the planted values reach stdout; `render()` emits only derived counts and state words. Child runs
are read-only (`wevtutil qe` / uptime children, bounded rc mapping); a missing or unparseable
child summary maps to a leg-unavailable reason, never guessed (selftest cases 5–6).

## 3. Axis-harm check — NO AXIS HARMED

`git diff-tree -r --stat 015787e6 3627fac0 -- SCORECARD.md` → 54 insertions, 0 deletions
(append-only; axes table rows untouched — coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6 all hold). Frozen bytes absent from the round diff. Lowest-axis rule
satisfied: calibration 5 and depth 5 are joint-lowest non-retired and C1/C2 work them.

## 4. Discernment spot-check (≥1 admit, ≥1 reject, ≥1 new SOURCES row re-opened)

| Item | Decision | Re-opened source (by closure) | Agree/disagree | Reason |
|---|---|---|---|---|
| S583 (supersedes-S582 correction row) | admit | live GetTickCount64 URL re-fetched by closure curl; sha256 == pin `580f1935…`; all six pointer greps re-run on the pin | agree | Quotes real, corrected locations (:834/:841/:842) each grep 1, recorded locations grep 0; correction landed as a new row per contract v1 rule 2; S582 row bytes untouched |
| S584 (QueryUnbiasedInterruptTime, new row) | admit | live URL re-fetched by closure curl; sha256 == pin `d0bcbba9…` (54774 bytes); :817 quote re-read (11 words, ≤25); :819-820, :826-827, :830, :833 re-read | agree, with one routed caveat | Page real, tier A apt, quotes real and the unit/failed-call/working-state grounds hold; BUT the zero-at-boot anchor is drifted — see §5 D71-1. The admit stands (the row's substance is sound); the pointer defect routes |
| Gate reject sample (C2/C3 boundary discipline) | reject (boundary held) | closure's own live runs of both tools + `render()` code read | agree | Negative deltas (−11/−4/−7 ms) print verbatim as the declared read model predicts, never smoothed into an episode story; `boot_binding=none events_window=recent-N-not-boot-scoped` on every line; render() emits counts and state words only; PROVINCE.md byte-frozen |

Census: `bash <fleet>/scripts/sources-census.sh validate --root <fleet> mori` → `mori ok`, rc 0;
32 W04 duplicate-URL warnings (the tolerated pre-existing class, including S583's legitimate
re-use of the S582 URL). The validated `corpus/SOURCES.md` (fleet-root mirror) is byte-identical
(sha256 `e67ab3cf…`) to the lane tip's committed SOURCES.md. SOURCES 355 → 357 re-counted by
closure (`grep -c "^| S"`: 355 at `015787e6`, 357 at tip).

FRESH-START duty spot-check (one, own receipt): closure re-ran
`python -I .ufo/waves/round-61/count-c2.py 986d4b46db6e67682ef84091f606d125f987ecbc`
→ `C2=unmet … rc=1`, byte-identical to the round's `freshstart-spotchecks-r71.txt` and the same
verdict the r61 closure recorded; `986d4b46…` and `7370a731…` verified present and ancestral of
master by closure. Do-nothing controls receipt spot-checked: entering-state greps reproduce
(355 rows, 0 `supersedes S582`, rc 128 on r71 paths).

## 5. Routed defects the lane must fix next round (status-neutral)

- **D71-1 (located-line drift in the round's own new row — the D1 class, again).** The S584
  zero-at-boot pointer is off by one: the sentence "The interrupt-time count begins at zero when
  the system starts…" is at `S584.html:829`; the row's anchor cell, the S584 opening receipt
  (located-facts), the round-71 lesson Gate, knowledge entry K4
  (`corpus/knowledge/workstate-win-r71.md`), and the `tools/mori-workstate-win.py` header comment
  all record `:828` — which is `<h2 id="remarks">Remarks</h2>` (grep of the quote against :828
  returns 0; against :829 returns 1; verified on the pin and on the closure's byte-identical live
  re-fetch). This violates the just-landed QUALITY 162 on the round's own bytes — and is
  simultaneously the proof that the new rule can fail. Fix per QUALITY 162's own procedure: a NEW
  supersedes/correction entry naming `:828→:829` old→new plus a pin-verified receipt, sweeping
  every mention (row anchor is immutable; K4, the Gate line, the receipt erratum note, and the
  tool comment take append-only correction blocks or a next-round change); never in-place anchor
  edits. Severity: citation hygiene only — quote, page, pin, tier, and every C2 behavior verify.
- **D71-2 (minor, same correction sweep).** Two quote word-counts in the S584 trail are misstated:
  the failed-call quote is 26 words (recorded 22), the :817 sleep/hibernation quote is 15 words
  (recorded 17). Counts carry commands per CORPUS.md; correct alongside D71-1.

## 6. Trend verdicts (closure, with evidence)

- **expansion: improved** — SOURCES 355→357 verified by closure count; both rows opened, pinned,
  live-re-fetched byte-identical today; two capability acquisitions demonstrated running by
  closure and entered the SCORECARD capabilities table (first-working round 71) in the same
  round; the r70 "unopened" working-state surface is now open with entry K1–K6 and a probe.
- **quality: improved** — C1's able-to-fail pair re-derived; QUALITY 162 landed and shown
  able-to-fail (by the lane against S582's drift carriers, and by this closure against S584's
  :828 — the routed defect); standing battery green on unchanged bytes per committed receipt;
  six mistakes mined with class/evidence/captured-by/fix (lesson §Mistakes read); the D71-1/D71-2
  defects are named and routed, not left unmarked — correction lands next round.
- **discernment: improved** — the boundary reject sample verified by closure's own runs (no
  episode attribution, no power diagnosis, boot_binding=none traveling); eight fresh-start
  rule-outs receipted with reasons; the L0 lines stay open and routed around; the outside
  spot-check agrees with both sampled admits and the reject.

## 7. SHONEN note for the operator

All four boxes are `[~]` asserted-by-author with resolvable pointers. This closure re-derived the
substance behind every box (selftests 10/10 x3 both tools + live rc 0 x3 each; end-to-end task in
LOG.md Round 71; QUALITY 162 beside the standing criteria; PROVINCE.md byte-frozen — absent from
the round diff). The boxes look fully checkable by a non-author; per the closure contract this
judge writes no `[x]` into SHONEN.md — the operator may treat this section as the reviewing
record.
