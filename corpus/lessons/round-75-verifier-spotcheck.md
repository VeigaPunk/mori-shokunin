# mori round 75 — verifier spotcheck

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Lane: mori · round 75 · entering `8ddf29dd9f59c14559a003d3b613f02d52bd0a4f` · head `32132cfbc78dfb3ff608af2ab77a273db8a76a1b` (branch tip, pushed) · this file is written by the closure judge and is NOT committed by the lane; the orchestrator commits it under the protocol identity.

## 1. Step-1 conformance

| Check | Command | Observed | Verdict |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet root> log --format='%an %ae %H' -1 -- .ufo/reports/round-75/mori.md` | `mori-shokunin mori@shokunin.local 50293aa862691816403fa02fc11344eca286a076` | ok |
| Committed report bytes carry the SHONEN heading | `git show 50293aa8:.ufo/reports/round-75/mori.md \| grep -c "^## SHONEN"` | 1; four `[~]` box lines with resolvable pointers | ok |
| Dispatch digest | `.ufo/watchdog.log` grep `mori round=75` | `2026-11-02T01:37:25-08:00 launch mori round=75 base=8ddf29dd9f59` / `2026-11-02T03:10:47-08:00 complete mori round=75 head=32132cfbc78d pushed=True` — matches the orchestrator digest | ok |
| Lane tip pushed | `rev-parse refs/heads/master` vs `ls-remote origin refs/heads/master` | both `32132cfbc78dfb3ff608af2ab77a273db8a76a1b` | ok |
| Round shape | `git log 8ddf29dd..32132cfb --format='%H %an'` + `rev-parse 32132cfb^` | exactly one commit `32132cfb`, author `mori-shokunin`, parent = entering `8ddf29dd`; all round work reachable from `8ddf29dd..32132cfb` | ok |
| Cited lane commits exist + ancestral | `cat-file -e` + `merge-base --is-ancestor <h> refs/heads/master` for `32132cfb`, `8ddf29dd`, `dc50c80b`, `986d4b46` | all four: EXISTS ANCESTOR | ok |
| Marker rule | report names real work, receipts, and checkable hashes | real report, not a marker | ok |
| Evidence predates commit | receipt internal stamps (`2026-11-02T10:02Z`–`10:40Z` = 02:0x–03:4x −08:00) vs commit time 03:10:47−08:00 | all receipts predate the landing commit | ok |

Report is a real report: conformance clean, no defects at step 1.

## 2. Claim re-checks (all re-measured by the closure judge at `32132cfb`; none evidence-only)

### C1 — calibration (the r74 closure carry-ins)

| Measurement | Command | Observed | Reported | Verdict |
|---|---|---|---|---|
| entering lines | `git show 8ddf29dd:SCORECARD.md \| wc -l` | 3758 | 3758 | match |
| entering lead cell | `git show 8ddf29dd:SCORECARD.md \| grep -cE '^\| Rotation-recurrence schedule instrument'` | 0 | 0 | match |
| entering tables | `git show 8ddf29dd:SCORECARD.md \| grep -c "Capability \| What it can now do"` | 25 | 25 | match |
| entering sha | `git show 8ddf29dd:SCORECARD.md \| sha256sum` | `043951b26b7ea13c74a06cd7abe7deacd43cc1cf4de2514cec18efa6271f9e27` | same | match |
| after lead cell | `git show 32132cfb:SCORECARD.md \| grep -cE '^\| Rotation-recurrence schedule instrument'` | 1 | 1 | match |
| after tables | `git show 32132cfb:SCORECARD.md \| grep -c "Capability \| What it can now do"` | 26 | 26 | match |
| append-only proof | `git show 32132cfb:SCORECARD.md \| head -3758 \| sha256sum` | `043951b2…` = the entering sha (every entering byte unchanged) | same | match |
| backfill row shape | row at SCORECARD:3762 (14-line `## Round 75 backfill` block, lines 3760–3773) | canonical 4 columns, first-working 74, evidence pointers to r74 selftest + live receipts | as reported | match |
| −8 decomposition | `git show dc50c80b --numstat` | SHONEN.md 4/4, SKILL.md 2/2, corpus/SOURCES.md 3/2 (deletions 4+2+2 = 8) | same | match |
| do-nothing control | committed `.ufo/waves/round-75/evidence/controls-r75.txt` + my own before-greps | lead cell 0 / tables 25 / receipts absent rc 128 / challenge-row 0 at entering | as reported | match |

Precision nit (status-neutral): the claim's "SCORECARD 3758 → 3772 lines" describes the backfill-only intermediate state; the committed SCORECARD at `32132cfb` is **3819** lines (backfill block 3760–3773 + the Round 75 section 3774–3819; numstat SCORECARD +61/−0, single end-of-file hunk). The falsifiable core (prefix sha unchanged, tables 25→26, lead cell 0→1, first-working 74) verifies exactly; the landed-changes section names both blocks. Recorded as a mild number-drift-class wording nit, not a falsification.

### C2 — freshness (the pin-family standing arm, re-derived LIVE)

| Measurement | Command | Observed | Reported | Verdict |
|---|---|---|---|---|
| Standing instrument re-run (closure judge, read-only) | `python tools/mori-drift-recheck.py --root . --only S241` (lane repo root) | `S241 asset-churn as-of=2026-11-02T11:24:23Z`; `MORI_DRIFT_RECHECK rows=1 adjudicated=1 … asset-churn=1 …`; rc=0 | receipt lines `rows=1 adjudicated=1 … asset-churn=1`, rc 0, as-of 10:31:13Z | match (fresh adjudication reproduces) |
| S581 identity | committed receipt `pin-family-rotrec-r75.txt` | `S581: IDENTICAL pin=5e5b941e… live=5e5b941e…`, 16179 bytes | same | match |
| S241 drift + continuity | committed receipt + `pin-family-reverify-r74.txt` | `S241: DRIFTED pin=1168b2a6… live=ddb7ba17…`; r74 receipt shows the SAME live sha `ddb7ba17…` — equal-size churn state persists; diff = 2 asset-URL pairs (build ids 0.4.03574.8308-9505b1c8 → 0.4.03589.8339-b0a05127) | same | match |
| Teaching re-verified both methods | receipt counting block | pin lines=3 live lines=3; pin occurrences=6 live occurrences=6 | same | match |
| No supersedes owed | receipt disposition + S241 row unchanged this round | pin immutable, no registry correction manufactured | as reported | match |

The practice discriminates, as claimed: it re-found the S241 drift and re-adjudicated it `asset-churn` rc 0, and re-found S581 identical. C2 verified met (re-measured live by the closure judge).

### C3 — depth (the three-session rotation series; the notable item)

The window-by-window comparison receipt (`.ufo/waves/round-75/evidence/rotation-series-comparison-r75.txt`) was checked line-by-line against the three committed session receipts it quotes, re-derived independently:

| Session / receipt | 31s | 91s | 304s | Judge's re-derivation from the receipt bytes |
|---|---|---|---|---|
| r70 hand-run (`shortwin-a/b/c-r70.txt`) | no | YES | no | a: window-s=31, per-response=0, same-bytes=true, `e4bf924c…` both legs; b: window-s=91, per-response=4, same-bytes=false, `e4bf924c…`→`6e7b906d…`; c: window-s=304, per-response=0, same-bytes=true, `6e7b906d…` both legs |
| r74 instrument (`rotation-schedule-live-r74.txt`) | no | no | YES | 31s/91s: per-response=0, same-bytes=true, `3e0ece81…` both legs; 304s: per-response=4, same-bytes=false, `3e0ece81…`→`5d88b3cc6039`; SUMMARY `rotated_yes=1 rotated_no=2 window_s_computed=31,91,304 wall_s=429 rc=0` |
| r75 instrument (`rotation-schedule-live-r75.txt`) | no | no | no | three window lines per-response=0 same-bytes=true, all six capture legs `34353de6db05`; SUMMARY `rotated_yes=0 rotated_no=3 window_s_computed=31,91,304 wall_s=429 clock=monotonic rc=0` — the first single-state session |

The receipt's table (`31s: no/no/no · 91s: YES/no/no · 304s: no/YES/no`) is **faithful to the committed receipts in every cell**. The three headline readings verify: no stated window classified yes in every session; the two YESes landed at different windows in different sessions (r70@91s, r74@304s); the 31s bound held ×3.

| Measurement | Command | Observed | Reported | Verdict |
|---|---|---|---|---|
| r75 window lines | `git show 32132cfb:.ufo/waves/round-75/evidence/rotation-schedule-live-r75.txt \| grep -c "ROTATION_SCHEDULE window="` | 3 | 3 | match |
| r74 anchored yes | `grep -c "ROTATION_SCHEDULE window=.*rotated=yes"` on the r74 receipt | 1 | 1 | match |
| r74 literal decomposition | `grep -c "rotated=yes"` on the r74 receipt | 2 (1 run-result + 1 prose reading line — decomposition named in the receipt) | 2 = 1+1 | match |
| r70 yes arm | `grep -c "per-response=4" .ufo/waves/round-70/evidence/shortwin-b-r70.txt` | 1 | 1 | match |
| S590 URL absent before | `git show 8ddf29dd:corpus/SOURCES.md \| grep -c "waf-captcha-and-challenge-actions"` | 0 | 0 | match |
| S590 URL present after | same grep at `32132cfb` | 1 | 1 | match |
| Series entry | `git cat-file -e` before/after | rc 128 → rc 0 | same | match |
| S590 pin | `git show 32132cfb:corpus/evidence/sources-r75/S590.html \| sha256sum` + `wc -c` | `8bff4311b27061c944059a4300564347a3c04c6870b88198fa0b4dd0755037fa`, 19812 bytes | same | match |
| Anchor machine check | committed `s590-anchor-check-r75.txt` | run A `ANCHOR_CHECK: PASS items=3` rc 0 (:138 9 words, :144 11 words, :78 9 words); able-to-fail run B mislocated FAIL rc 1 | same | match |
| Quotes located in pin | `sed -n '138p'`, `'144p'`, `'78p'` on the pin | all three quoted sentences present verbatim at the recorded lines, word counts 9/11/9 | same | match |
| Standing battery | `git show 32132cfb:.ufo/waves/round-75/evidence/selftests-battery-r75.txt \| grep -c "^rc=0$"` | 11 | 11 of 11 | match |

Mechanism grounding (S590) is correctly bounded: the knowledge entry (`corpus/knowledge/rotation-series-r75.md`, provenance trio present, S1–S5) decides no TTL and no vendor verdict; the S580/S581 boundary is restated. C3 verified met (re-measured from committed receipts by the closure judge).

## 3. Per-axis verdicts

| Axis | Score (unchanged rows verified: axes table at SCORECARD lines 10–15, byte-untouched by the single end-of-file hunk) | Verdict | Basis |
|---|---|---|---|
| calibration | 5 | **improved** | C1 re-measured (see §2) |
| freshness | 5 | **improved** | C2 re-measured live |
| depth | 5 | **improved** | C3 re-measured |
| coverage | 6 | unchanged | no row touched; no new surface claimed as governed |
| operability | 7 | unchanged | battery re-run passes at this round's bytes; no instrument edited |
| adjacency | 6 | unchanged | vendor mechanism cited not absorbed; PROVINCE.md absent from the diff |

All three claims are on 5-score axes — the lane's lowest non-retired tier; distinct axes; causally separable (each before→after independent). No exploratory claim declared, so no `unprovable-but-better` judgment is owed. No axis harmed.

## 4. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S590 admit (tier A, AWS WAF action-behavior docs) | admit | LIVE fetch of `docs.aws.amazon.com/waf/latest/developerguide/waf-captcha-and-challenge-actions.html` | **agree** | Live page is byte-identical to the pin (sha `8bff4311…`, 19812 bytes, equal), all three quoted sentences present (counts 1/1/1), anchor-check PASS + able-to-fail FAIL receipted; tier A for a vendor-docs scope is right |
| Three-slug reject (waf-challenge.html, challenge.html, waf-challenge-action.html) | reject | LIVE fetch of `…/waf-challenge.html` | **agree** | HTTP 200 but the resolved page `<title>` is `302 Found` — a redirect/frame, not the topic page; the reject reason ("resolves to the guide-index frame, teaches nothing about the action's behavior") holds; the flip condition is stated |
| S589 used-by in-place update | in-place change (contract rule 2) | committed SOURCES.md cell + lesson old→new log | **agree** | Only `used-by` changed (old 2 paths → new 3 paths, `corpus/knowledge/rotation-series-r75.md` appended); status/recheck untouched; old→new logged in the lesson and LOG — rule 2 compliant |

Census validator re-run by the closure judge: `mori ok`, 35 W04 (the tolerated duplicate-URL class), exit 0 — matches the round-end claim.

## 5. Trend verdicts (closure judge, from re-derived facts)

- **expansion: improved** — one new admitted knowledge entry (`corpus/knowledge/rotation-series-r75.md`) on ground the schedule family did not hold (the recurrence series + the mechanism layer), `source:` citing the new mined row S590; SOURCES 362 → 363 re-counted; the entry's S1–S5 all re-derived from committed receipts.
- **quality: improved** — both closure carry-ins discharged with re-derivable evidence (sha-proven append-only backfill; numstat-proven −8 decomposition); the standing arm demonstrated discriminating (drift re-found and re-adjudicated; S581 re-found identical — reproduced live by the judge); the series comparison reads entirely from committed bytes and is faithful cell-by-cell; battery 11/11; census rc 0 both ends; four mistakes mined with classes/evidence/captured-by/fixes.
- **discernment: improved** — the frozen r74 SCORECARD section NOT edited in place (proven by the unchanged entering sha, not just asserted); a same-day fourth schedule session refused; no TTL decided despite new mechanism ground; the vendor's bot management left the vendor's; three open mori L0 lines routed around; the D73-2 count-precision class caught in the round's own receipt before landing; the reject decisions survive re-opening.

## 6. Notes and routed items for the lane (status-neutral; none bars admission)

1. **Scorecard line-count wording nit.** C1's "SCORECARD 3758 → 3772 lines" is the backfill-only intermediate; the committed file at `32132cfb` is 3819 lines (numstat +61/−0). Next time, state both deltas ("backfill +14; round section +47; file 3758 → 3819") so the after-count is re-derivable at the cited commit without decomposition.
2. **Pre-existing corpus-index drift (routed, new observation by this closure).** `corpus/README.md`'s round-sections and knowledge index end at round 58; the r59–r75 knowledge entries (`wave-settlement-artifacts-r59`, `uptime-win-r70`, `workstate-win-r71`, `boot-anchor-win-r73`, `rotation-schedule-r74`, `rotation-series-r75`, and the r62–r69 Windows-instrument family) are not indexed there (83 knowledge files at HEAD; zero README rows naming any `win-r6x`/`win-r7x` entry). Not introduced this round (README was absent from the diffs of r62–r75 alike) and prior spotchecks only verified the README untouched, never flagged the index gap. A future round could land an index-repair move (the README's own "Round19 retrospective index repair" is the precedent) as a measured claim.
3. **SHONEN boxes.** All four remain `[~]` (asserted-by-author) with resolvable pointers; nothing in this round's evidence contradicts them. They look fully checkable by a non-author verifier — flagged for the operator's promotion review, per the standing instruction; this closure does not write `[x]`.
4. Dispatch-surface disclosure carried (no L2 wave on this host) — consistent with rounds 62–74, nothing new to route.

**Closure ruling: every claim re-measured and verified; no axis harmed; no conformance defect bars admission. mori round 75 is `ok`, admitted.**
