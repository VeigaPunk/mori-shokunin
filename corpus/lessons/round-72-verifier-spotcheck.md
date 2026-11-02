# mori round-72 — verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
date: 2026-11-02 (closure pass; lane tip `d2f55d8c9f03855d92c3ba7be8becb8d93f38e26`, entering `c5873f73d981`)
scope: step-1 conformance, per-claim re-derivation, per-axis verdicts, discernment spot-check, trend verdicts, routed defects.
Redaction posture: counts and shapes only; no settings-file values, session identifiers, session-store paths, or session-record fields appear in this file.

## 1. Step-1 conformance — all checks pass

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-72/mori.md` | `mori-shokunin <mori@shokunin.local> a0eaa890d9e8580b7b56257e3f3570221268d69e` | pass |
| Committed report bytes = filed bytes | `git show a0eaa890:.ufo/reports/round-72/mori.md` vs worktree file | byte-identical | pass |
| `SHONEN` heading + one line per box | grep on committed report | `## SHONEN` at :37; 4 `[~]` lines (asserted-by-author with pointers — correct form for a non-promoted lane; no `[x]` written by the author) | pass |
| Lane tip pushed | `git rev-parse refs/heads/master` vs `git ls-remote origin refs/heads/master` | both `d2f55d8c9f03855d92c3ba7be8becb8d93f38e26` (ahead=0) | pass |
| Cited lane commits exist + ancestral | `cat-file -e` + `merge-base --is-ancestor … refs/heads/master` | `d2f55d8c…` (= tip), `c5873f73d981` (sole parent of the round commit), `986d4b46` (r61 data tip) all present and ancestral | pass |
| Dispatch/complete digest | grep `.ufo/watchdog.log` | lines match the closure digest exactly: `2026-11-01T16:00:15-08:00 launch mori round=72 base=c5873f73d981 (zcode run14)`; `2026-11-01T18:10:25-08:00 complete mori round=72 head=d2f55d8c9f03 pushed=True` | pass |
| Round work reachable | range `c5873f73d981..d2f55d8c9f03…` | single round commit, exactly the cited work | pass |
| Report lands last | commit timestamps | lane commit `2026-11-02T02:04:07Z` < report commit `2026-11-01T18:10:26-08:00` (= 02:10:26Z) | pass |
| No future-dated evidence | evidence receipt timestamps vs landing commit | all receipt timestamps (`00:37:35Z`–`01:39:56Z`) precede the lane commit `02:04:07Z` | pass |

## 2. "No frozen byte edited" — verified (re-measured)

`git diff-tree -r --stat c5873f73d981 d2f55d8c9f03…` → exactly **20 paths, +1430/−6** as reported. Path list: 12 new wave receipts under `.ufo/waves/round-72/evidence/`, `LOG.md` (+114/−0), `SCORECARD.md` (+55/−0), `SHONEN.md` (+4/−4), `corpus/SOURCES.md` (+3/−0), `corpus/knowledge/workstate-win-r71.md` (+12/−0), `corpus/lessons/round-72.md` (new), `tools/mori-anchor-check.py` (new), `tools/mori-workstate-win.py` (+3/−2).

- The −6 = SHONEN's 4 re-asserted box lines (the licensed per-box evidence-line form) + the workstate tool's header-comment rewrite (3-line comment: 3 added/2 deleted continuation lines). Code untouched (verified by reading the hunks; selftest re-run green, below).
- Append-only discipline holds: `LOG.md`, `SOURCES.md`, `SCORECARD.md` have **0 deleted lines**; the S584 row anchor cell is untouched in place (S585 supersedes it); the r71 receipt (`.ufo/waves/round-71/evidence/source-s584-r71.txt`), the r71 lesson (`corpus/lessons/round-71.md`), the r70 lesson and r70 receipt are absent from the diff.
- SKILL.md, PROVINCE.md, corpus/QUALITY.md, corpus/README.md, AGENTS.md absent from the diff — the frozen set the round declared untouchable is untouched.
- The one in-place edit (tool header comment `S584:828` → `S584:829`) is licensed: `corpus/lessons/round-71-verifier-spotcheck.md:151` routes it as "tool comment take append-only correction blocks or a next-round change". Workstate selftest re-run by this closure at the new bytes: `WORKSTATE_WIN_SELFTEST: PASS (10 cases)` rc 0.

## 3. Per-claim re-checks

### C1 (calibration) — RE-MEASURED, verified met

Before (at `c5873f73d981`), all re-run by this closure:

```
git show c5873f73d981:corpus/SOURCES.md | grep -c "supersedes S584"  -> 0   (also S581: 0, S583: 0)
git cat-file -e c5873f73d981:.ufo/waves/round-72/evidence/s584-anchors-erratum-r72.txt -> rc 128
git show c5873f73d981:tools/mori-workstate-win.py | grep -c "S584:828" -> 1
```

After:

```
grep -c "supersedes S584|S581|S583" corpus/SOURCES.md -> 1 / 1 / 1   (S585:SOURCES.md:366, S586:367, S587:368, INSIDE the Registry)
grep -c "S584:828" tools/mori-workstate-win.py -> 0
sed -n '828p' corpus/evidence/sources-r71/S584.html | grep -c "The interrupt-time count begins at zero" -> 0
sed -n '829p' … | grep -c "The interrupt-time count begins at zero" -> 1    (able-to-fail pair)
```

Standing QUALITY 90 label check over the ENTERING rev, re-run by this closure from the criterion's own committed script (corpus/QUALITY.md §90 block, extracted; `@@LESSON`/`@@SOURCES` markers per the documented form; `python -I -B` per this host's disclosed interpreter posture):

```
word_labels=8 mismatched=3   rc=1
line=362 label=15 wc=14   (S581 :70-71 — the unflagged-since-r70 finding)
line=365 label=17 wc=15   (S584 sleep/hibernation — routed D71-2)
line=365 label=22 wc=26   (S584 failed-call — routed D71-2)
```

— exactly the reported able-to-fail result and finding set.

Label-audit re-derivation (one of the three, done independently by this closure): S582/S583 `:829` definition label 14→13 —

```
sed -n '829p' corpus/evidence/sources-r70/S582.html | grep -o "Retrieves the number of milliseconds that have elapsed since the system was started\." | wc -w  -> 13
sha256sum corpus/evidence/sources-r70/S582.html -> 580f1935fb47b5c992a48d22299f7452aaeb00099f2ac96ba74c92002a18277f (52661 bytes; matches the S587 row's recorded pin)
```

Agrees with S587's correction; the pin sha binds the row.

Seven S584 mention carriers — all dispositions verified: (1) S584 row anchor cell immutable (SOURCES.md diff has 0 deletions; corrected by supersedes row S585 per contract v1 rule 2); (2) r71 opening receipt untouched (absent from diff; the erratum is correction of record); (3) r71 lesson Gate untouched (absent from diff; r72 lesson carries old→new); (4) K4 append-only correction block (+12/−0 in `corpus/knowledge/workstate-win-r71.md`, read: names :829, S585, the erratum, and re-confirms K1/K2/K3/K5/K6); (5) tool header comment fixed in place — licensed next-round change (r71 spotcheck :151), code untouched, selftest green (re-run by this closure); (6) r71 LOG/SCORECARD records stand (0 deletions in both); (7) fleet r71 report orchestrator-owned, named in the erratum receipt §7. The erratum's sweep self-hits (round-17 unrelated `:828`, controls/erratum self-reference lines, `__pycache__` build artifact) are named and correctly excluded.

The S586/S587 discharge carries the same shape: S581/S582/S583 label cells immutable (0 deletions), r70 lesson :65/:69/:80 untouched (absent from diff), r70 receipt :20 untouched (absent from diff), fleet r70 report named, LOG/SCORECARD grep-clean (checked: no r70/r71-section label carriers), K1 verified count-free.

### C2 (freshness) — evidence-verified + one independent live re-fetch, verified met

Committed receipt `.ufo/waves/round-72/evidence/pin-family-reverify-r72.txt`: `grep -c "^verdict: byte-identical"` → 7; `grep -c "^verdict: DIFFERS"` → 0; seven distinct pages covering nine registry rows (S583 shares S582's pin, S585 shares S584's). Per-row sha256s match the row-recorded pins (spot-verified locally for S581, S582, S584). Independent re-fetch by this closure (same fetcher posture `curl -sS -m 60 -L`):

```
curl -sS -m 60 -L -o <scratch>/S581-closure.html https://docs.aws.amazon.com/waf/latest/developerguide/waf-tokens-immunity-times.html
sha256 -> 5e5b941e97c0aa6e2d7bd958bdc66a6fbb2a260508880e99becda543e71fc865 (16179 bytes) == pin sha
```

Byte-identical today. No churn class fired and none manufactured (the receipt records plain byte-identity; the drift grammar was not invoked on a no-delta result).

### C3 (operability, capability acquisition `tools/mori-anchor-check.py`) — RE-MEASURED, verified met

- Selftest run by this closure from the lane root: `python tools/mori-anchor-check.py --selftest` → `ANCHOR_CHECK_SELFTEST: PASS (11 cases)` rc 0, **×3** (matches the receipt).
- Able-to-fail run B re-derived with the r71-RECORDED pre-correction values against the S584 pin:

```
python tools/mori-anchor-check.py --pin corpus/evidence/sources-r71/S584.html \
  --check 'def|817|11|Gets the current unbiased interrupt-time count, in units of 100 nanoseconds.' \
  --check 'sleep|817|17|The unbiased interrupt-time count does not include time the system spends in sleep or hibernation.' \
  --check 'failed_call|826-827|22|If the function succeeds, the return value is nonzero. If the function fails because it is called with a null parameter, the return value is zero.' \
  --check 'zero_at_boot|828|24|The interrupt-time count begins at zero when the system starts and is incremented at each clock interrupt by the length of a clock tick.'
-> sleep verdict=wordcount_mismatch (15 vs 17); failed_call verdict=wordcount_mismatch (26 vs 22);
   zero_at_boot verdict=mislocated (occurrences=0 at :828)
ANCHOR_CHECK: FAIL items=4 ok=1 mislocated=1 wordcount_mismatch=2  rc=1   (exactly as receipted)
```

- Able-to-fail run E re-derived: `--pin S581 --check 'section|54|10|…'` → FAIL rc 1 wordcount_mismatch=1 (9 vs 10); `--pin S582 --check 'def|829|14|…'` → FAIL rc 1 wordcount_mismatch=1 (13 vs 14). Both exact.
- Corrected-anchor runs re-derived: run A → all 8 items locate, counts equal recorded (11/15/26/24), rc 0; run C → `def|829|13` ok (13=13), all items locate, rc 0; run D → `section|54|9` ok (9=9), `minimum|83|11` ok (11=11), all items locate, rc 0. (First attempts by this closure mislocated two items whose TEXT this closure had guessed rather than copied from the pin — resolved with pin-exact fragments; tool behavior consistent at every step. The tool's declared span limit — two-line sentences verify as fragment-locates — is what requires the fragment form; observed on the `signature|819-820` item.)
- Redaction arm observed: stdout carries counts/shapes only — no quote text reaches output in any run above.
- Capabilities row entered SCORECARD with evidence pointer and first-working round 72, demonstrated in the same round (AXES.md §Capabilities satisfied).
- Note (routed, §6 below): the tool has no row in the lane's registry home (SKILL.md `## Gates`) — C3 is graded here as a **capability** (verified), not as a conformant gate.

Re-measured vs evidence-verified: C1 and C3 re-measured (every command above run by this closure); C2 evidence-verified with one independent live re-fetch.

## 4. Per-axis verdicts (closure's own, agreeing with the report where claimed)

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 verified met (re-measured): the routed D71-1/D71-2 carry-ins discharged by correction-of-record, the same class self-found by the round's own standing instrument and discharged in-round, every mention dispositioned; self-verified and left re-derivable (this closure re-derived all of it) |
| freshness | improved | C2 verified met: 7/7 pin-family pages byte-identical on 2026-11-02, receipted; independently re-fetched by this closure (S581) byte-identical; nine rows re-bound to live bodies |
| operability | improved | C3 verified met: the QUALITY 162/90 check made runnable, able-to-fail demonstrated against the recorded drifted values themselves (re-derived), capabilities row entered with same-round demonstration |
| depth | unchanged | SKILL.md untouched (absent from diff); no depth claim made |
| coverage | unchanged | no new external surface opened (correction rows of already-opened pages — honestly named as not-new-surfaces in report and lesson) |
| adjacency | unchanged | boundary held: workstate correction block counts/anchors only; anchor-checker citation-hygiene-only; no sibling surface touched; PROVINCE.md byte-frozen |

No axis is harmed (SCORECARD diff is +55/−0; the axes table is untouched; all claims additive).

## 5. Discernment spot-check (outside this closure, non-author)

Census: `bash <fleet>/scripts/sources-census.sh validate --root <fleet> mori` → **`mori ok` rc 0**, 35 W04 warnings — the last three are S585/S586/S587 duplicate-URL warnings of their own (superseded) pages, the same tolerated class the round receipted (start 32 → end 35).

| Item | Decision | Re-opened source (by this closure) | Agree/disagree | Reason |
|---|---|---|---|---|
| S585 (supersedes S584) — Gate admit | admit | pin `corpus/evidence/sources-r71/S584.html` (sha `d0bcbba9…`, 54774 bytes) anchors re-verified by this closure: :828 greps 0 / :829 greps 1; failed-call 26 words; sleep 15 words; the committed live re-open receipt records byte-identity 2026-11-02T00:45:29Z | agree | The correction is real (every corrected value re-derived), the mechanism is contract-legal (new row, anchor cell immutable), and the pre-row URL-slug sweep result of 1 is correctly interpreted as the S584 row itself, receipted before the row landed |
| S586 (supersedes S581) — Gate admit | admit | LIVE re-fetch of the URL by this closure: sha `5e5b941e…` (16179 bytes) byte-identical to pin; ≤25-word Gate quote at `S581.html:54` — "This section explains how challenge and CAPTCHA timestamps expire." = 9 words (≤25, located); corrected labels 9 and 14 proven by anchor-check runs D/E1 and direct wc | agree | Quote real and located; the 10→9 and 15→14 corrections match wc -w of the quoted text per QUALITY 90; row shape valid (13 fields, census-clean) |
| Gate reject sample — the boundary held (no manufactured churn classification on a byte-identical re-fetch; Precise variant `:876` stays unopened; corrections stop at the audited family S574–S585, older rows not claimed clean) | reject(s) of overreach | `:876` located by this closure's own run A (occurrences=1) yet the row still claims it unopened — the restraint is verifiable; family audit names its pairing rule and its 3 pairing artifacts + 2 prose-phrase exclusions | agree | Withholding an unearned classification, keeping an unopened variant unopened, and scoping claims to what was actually audited are exactly the calibrated moves; each refusal is checkable in the committed bytes, and this closure checked them |

## 6. Routed defects for the lane (status-neutral; none bars admission)

1. **Registry drift at the lane's registry home (family-wide; route to the lane).** The new gate-shaped instrument `tools/mori-anchor-check.py` (verdict rc 0/1/2, committed selftest, pin-bound expected values) has no row in SKILL.md `## Gates` — and neither do the r68–r71 instruments (`mori-ua-variance.py`, `mori-uptime-win.py`, `mori-workstate-win.py`, `mori-events-context-win.py`; grep count 0 each). PROTOCOL.md §Gate standard: closure grades no gate conformant until its registry row exists at the registry home. C3 is therefore graded here as a verified **capability**, not a conformant gate. Next round: land registry rows for the anchor-checker (and ideally the r68–r71 set), or surface the registry-home question for the Windows-source instrument family to the operator via the open L0 channel.
2. **Receipt command shorthand (cosmetic).** `s581-s583-labels-erratum-r72.txt` §1 prints the QUALITY 90 invocation without the `@@LESSON`/`@@SOURCES` echo markers that its own output's line numbering (line=362/365, SOURCES-relative) presupposes; the documented form (corpus/QUALITY.md §90) includes them and reproduces the output exactly — this closure re-ran it (`word_labels=8 mismatched=3` rc 1, same three findings). Future receipts: print the runnable command verbatim.
3. **Carried disclosures (named, not new):** L2 wave dispatch — no dispatch surface on this host (mori round-62/round-65 L0 lines stand open, re-verified unanswered in `.ufo/waves/round-72/evidence/l0-considerthese-r72.txt`); the r65-gated planned items (encoding-pin harness, pin-check mismatch split) stayed unimplemented and are named. Correctly routed around, never treated as answered.
4. **SHONEN boxes checkable by a non-author (for the operator).** All four boxes carry resolvable pointers and this closure re-derived the box-2/box-3 evidence directly (LOG round-72 entry; selftests re-run green). A non-author verification pass could legitimately write `[x]` at promotion review — this closure does not write SHONEN.md (duty 6).

## 7. Trend verdicts (closure's own)

- **expansion: improved** — the anchor-checker capability entered the SCORECARD capabilities table with a same-round running demonstration (LEARNING.md names capability admission an expansion observable); SOURCES 357 → 360 with the three correction rows binding nine registry rows to same-day-live bodies (honestly named as not-new-surfaces); coverage unchanged and not claimed otherwise.
- **quality: improved** — freshness moved with receipted evidence; the citation-drift class is eliminated from the trail-of-record (six corrected values, every mention dispositioned); no admitted entry failed its re-check (all seven pins byte-identical); 4 mistakes mined with classes, evidence, captured-by and fixes; the standing battery is green (11 tools rc 0, receipted; workstate selftest re-run by this closure at the corrected bytes).
- **discernment: improved** — this closure's outside spot-check agrees with the Gate's admits (S585/S586/S587 re-opened and re-derived) and with the recorded rejections/boundary decisions (no manufactured churn, Precise stays unopened, corrections scoped to the audited family); the round caught its own instruments' failures before landing (vacuous shape-check pattern, from-memory fixture values, self-counting receipt greps — all mined with fixes); the L0-gated items stayed unimplemented and named.

Admission: every claim verifies and no axis is harmed → **admitted**.
