# mori round 67 — non-author verifier spotcheck

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
date: 2026-11-01
lane: mori-shokunin · entering `8470a025f94f7449e881c3d8a8c997ed89aa7a9a` · landed `eed7272fc17d8beea75a275b13d03542ae275446` (branch master, pushed, ahead=0)
report: `.ufo/reports/round-67/mori.md` (fleet repo)
method: index-free git only (`rev-parse`, `cat-file`/`show`, `diff-tree`, `merge-base --is-ancestor`, `ls-remote`); live re-runs are read-only fetches. Per the lane redaction rule: no settings-file values, session identifiers, session-store paths, or session-record fields are copied into this artifact — counts and shapes only.

## 1. Step-1 conformance

| Check | Command / evidence | Observed | Verdict |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-67/mori.md` (fleet repo) | `mori-shokunin <mori@shokunin.local> 14ac41123654392ebfcbec4dc69ab9fc89fae156`, subject `round-67: mori report (hyaku zcode run 14)`, 185 insertions | OK |
| Committed report bytes = filed bytes | `git show 'HEAD:.ufo/reports/round-67/mori.md'` diffed against the working-tree file | empty diff | OK |
| `SHONEN` heading | read of the report | `## SHONEN` present, one `[~]` line per box (4/4), no `[x]` | OK |
| Cited lane commits exist + ancestral | `merge-base --is-ancestor` of `8470a025f94f` and `eed7272f` against `refs/heads/master` | rc 0 both | OK |
| Lane tip pushed | `rev-parse refs/heads/master` vs `ls-remote origin refs/heads/master` | both `eed7272fc17d8beea75a275b13d03542ae275446` (ahead=0) | OK |
| Round work reachable in range | `git diff-tree -r --stat 8470a025f94f eed7272f` | 16 files, +6083/−44 — exactly as the report states | OK |
| Dispatch digest corroborated | `.ufo/watchdog.log` | `2026-11-01T01:50:00-08:00 launch mori round=67 base=8470a025f94f (zcode run14)`; `2026-11-01T03:21:08-08:00 complete mori round=67 head=eed7272fc17d pushed=True` — matches the orchestrator digest | OK |
| Frozen bytes untouched | `git diff-tree -r 8470a025f94f eed7272f -- SKILL.md tools/mori-source-drift.py tools/mori-drift-adjudicate.py PROVINCE.md AGENTS.md corpus/README.md` | empty (byte-identical); SKILL:905 `PASS (6 cases)` tally pin counts exactly 1 at the tip | OK |
| Census exit 0 at round end | committed `census-start-r67.txt` / `census-end-r67.txt` both carry `rc=0`; closure re-ran the validator itself | `mori ok`, tolerated W04 duplicate-URL class, `rc=0` at 2026-11-01T12:05Z | OK |

Conformance defects: none.

## 2. Claim re-checks

Re-measured by closure (commands run fresh on this host against committed bytes; the working tree was verified byte-identical to `eed7272f` for `tools/mori-drift-recheck.py`, `corpus/evidence/sources-r42/S241.html` and `corpus/evidence/sources-r67/S578.html` before any run). No sibling gate executed; the standing battery tallies are evidence-verified from the committed receipt.

### C1 (depth 5) — the second vendor churn grammar (`asset-churn`, class `learn-microsoft-asset-build-id`) — VERIFIED MET (re-measured)

- Do-nothing control, before: `git show 8470a025f94f:tools/mori-drift-recheck.py | grep -c asset-churn` → `0`, rc 1 (matches `controls-r67.txt`).
- After: `git show eed7272f:tools/mori-drift-recheck.py | grep -c asset-churn` → `19`, rc 0 (matches report).
- Selftest at the final bytes: `python tools/mori-drift-recheck.py --selftest` → `MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)`, rc 0, re-run by closure (the committed receipt carries three consecutive runs plus the honest run history).
- QUALITY 159: `grep -c '^159\.' corpus/QUALITY.md` 0 → 1, re-derived; the append-only erratum on 158 retires the stale "S241 stays content-drift" clause in place (addition, no rewrite).
- Live A/B, re-run by closure (~1 h after the lane's runs, same pin):
  - `python tools/mori-drift-recheck.py --root . --only S241` → `S241 asset-churn as-of=2026-11-01T11:43:02Z`, rc 0 (header names `stamp-class=python-docs-page-stamp asset-class=learn-microsoft-asset-build-id`).
  - Pinning-UA body re-fetch (`curl -sS -m 60 -L -A curl/8.21.0`): 53963 bytes both sides, 1499 lines each (awk NR; `wc -l` says 1498 because the final line is unterminated — the report's "1499" is the true line count); pin sha256 `1168b2a6…`, live sha256 `ddb7ba17…`, both matching the receipt exactly.
  - Pin-vs-live diff: `grep -c "^[<>]"` = 4 (2 changed lines) — exactly the two `/static/assets/<build-id>/` references (`0.4.03574.8308-9505b1c8` → `0.4.03589.8339-b0a05127`), lines 163 and 211. The vendor has not redeployed since the lane's fetch; the delta shape is identical to what the receipt recorded.
- Before-state citation: r66 standing receipt line 20 re-read at the entering bytes → `S241 content-drift as-of=2026-11-01T08:40:58Z`. Confirmed.
- Honest disclosure check (the decisive one): the pre-fix live run (`content-drift` at 10:21:36Z, second-UA arm never attempting the churn grammars) is recorded in THREE places — `s241-assetchurn-live-r67.txt` (pre/post side by side), `corpus/lessons/round-67.md` `## Mistakes` item 2 (green selftest over a design gap, captured-by + fix), and the `recheck-selftest-r67.txt` run-history header (NameError death → first green version over the gap → final bytes ×3). Disclosed, not laundered.

### C2 (operability 7) — `--from-sweep <receipt>` — VERIFIED MET (re-measured)

- Controls: `grep -c from-sweep` on entering bytes → `0` rc 1; at tip → `17` rc 0. Re-derived.
- Closure re-ran the standing step itself: `python tools/mori-drift-recheck.py --root . --from-sweep .ufo/waves/round-66/evidence/sweep-live-r66.txt` → rc 0, header `findings=17`, 17 rows adjudicated — 8 time-churn, 1 asset-churn (S241, the single intended flip), 5 receipt-open, 2 ua-serving, 1 gate, 0 content-drift. Identical class distribution to the committed `fromsweep-standing-r67.txt`; `grep -cE '^S[0-9]{3} '` = 17.
- Integrity checks shown able to fail in the selftest closure re-ran: `parse_sweep_rows_not_summary` (summary token never counted as a row), `from_sweep_malformed_exit2` (not-a-sweep rc 2; rows-vs-summary disagreement rc 2), `missing_sources_exit2` (rc 2), `from_sweep_selects_drifted` — all PASS in the closure's own run.
- R66 sweep receipt inputs re-read: 349 rows, `drifted=17` — the mode selected exactly the 17 findings.
- No-harm battery: `selftests-battery-r67.txt` — register 12/12, settlement 10/10, vote-bind 16/16, pin-check 125/125, adjudicate 5/5, recheck 10/10, all rc 0, loopback-transport condition carried (evidence-verified from the committed receipt; the recheck case independently re-run green by closure).

Both claims are causally separable (C1 = grammar class + QUALITY 159; C2 = receipt-driven selection mode) and neither is reachable by a do-nothing round (controls receipt). No exploratory claim was declared, so no `unprovable-but-better` ruling is owed.

## 3. No axis harmed

- `SCORECARD.md` diff over the range: one hunk, pure append after the r66 content (claims table, capability-row r67 extension, rule-outs, controls, planned) — no axis row or score rewritten. Entering/after scalars identical (coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; no scalar claimed — consistent with the lane's stated convention).
- Frozen instruments byte-identical across the range (SKILL.md, `tools/mori-source-drift.py`, `tools/mori-drift-adjudicate.py`, PROVINCE.md, AGENTS.md, corpus/README.md).
- Census rc 0 both ends and at closure; standing battery green.

## 4. Discernment spot-check (non-author)

Sampled from `corpus/lessons/round-67.md` `## Gate`: 1 admit (S578) and 1 reject-class decision (fresh-start rule-out 5 — no third grammar for the instrument-UA bot-manager chrome; the Gate honestly records "reject sample: none met" for source rejections this round).

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S578 web.dev HTTP Cache (versioned URLs), tier A, mined | admit | Live re-fetch of `https://web.dev/articles/http-cache` (2026-11-01) + committed pin `corpus/evidence/sources-r67/S578.html` (sha256 `5c02b661…` matches the lesson; worktree == committed) | agree | Quote resolves at `S578.html:4647` and is exactly 15 words ("Versioned URLs are a good practice because they make it easier to invalidate cached responses."); heading `:4638`, continuation `:4652`, title `:76` all resolve; the quote is present in today's live page too (grep count 1); it genuinely grounds `teaches` — versioned asset URLs as deploy-time cache invalidation is the rationale for the `asset-churn` grammar. Duplicate sweeps before opening are receipted (0 hits ×3). |
| Fresh-start rule-out 5: no third churn grammar for the instrument-UA bot-manager chrome | reject-class decision | Closure's own A/B bytes: instrument-UA body = pinning-UA delta + one per-response injection line before `</head>` (per the receipt, shape confirmed by the two live fetches taken this closure) | agree | A per-response token is serving variance, not a build artifact; normalizing it as a grammar could mask real content deltas and would bake an unversioned vendor behavior into the instrument. Deciding on the pinning-UA body (as shipped) is the conservative resolution, and QUALITY 159 discloses the boundary. |
| Fresh-start rule-out 4: no edit to the frozen sweep / r65 adjudicator | reject-class decision | `git diff-tree` over the range for both files: empty; SKILL:905 tally pin counts 1 at tip | agree | The restraint held in the landed bytes, and the r67 work was correctly built as an extension of the lane-owned r66 re-check, which pins no SKILL tally. |

New `SOURCES.md` row re-opened: S578 (above) — quote ≤25 words, located, tier A justified for the vendor-docs scope. SOURCES 350 → 351 re-counted (`grep -cE '^\| S[0-9]{3,} '` at entering vs tip).

Census validator re-run by closure: `mori ok`, rc 0 (tolerated W04 duplicate-URL class) — matches both committed receipts.

## 5. Trend verdicts (closure)

- **expansion: improved** — capability row extends with a demonstrated r67 extension (grammar + mode; first-working stays 66); one tier-A source opened, pinned, mined (350 → 351, re-counted); PROVINCE unchanged.
- **quality: improved** — both claims re-measured met with able-to-fail evidence (pre-fix live run receipted beside post-fix; from-sweep rc 2 paths exercised in the selftest closure re-ran); QUALITY 159 + append-only erratum; standing battery green (no operational axis traded).
- **discernment: improved** — three mistakes mined with class · evidence · captured-by · fix; the green-selftest-over-design-gap disclosure recorded in three artifacts (receipt, lesson, report) and re-verified above; third-grammar temptation rejected; considerthese pin-check proposal routed behind the operator's open instrument-change ruling rather than adopted.

## 6. Per-axis verdicts (closure; agree with the report)

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured met (live S241 A/B reproduced by closure) |
| operability | improved | C2 re-measured met (from-sweep 17/17 re-run by closure) |
| freshness | unchanged | held — as-of convention continues; no freshness claim declared; standing receipts moment-bound |
| coverage | unchanged | 6; no new surface claimed; PROVINCE byte-identical |
| calibration | unchanged | 5; three mistakes mined honestly; gap disclosure verified recorded (consistent with the score: honest accounting, no overreach) |
| adjacency | unchanged | 6; write scope clean — only lane files plus read-only vendor fetches; no sibling surface touched |

## 7. Routed items and notes for the next round / operator

1. Status-neutral labeling nit (route: lane, next round): in `s241-assetchurn-live-r67.txt`, the heading "live run at the FINAL bytes 2026-11-01T10:30:24Z" sits above the output block of the reproduced run (`run-start=2026-11-01T10:36:28Z`); the 10:30:25Z first post-fix run is cited in the report and SCORECARD but its own raw output block is not separately quoted in the receipt. Evidence unaffected — both runs are corroborated by closure's independent reproduction — but a future receipt should label each block with its own run-start.
2. Carry-in, stays open for the operator (correctly routed around, never treated as answered): the r65 L0 (SKILL:905 `python3` naming; this host's `python3` is a Store stub, rc 49 — confirmed by closure), the mori | round-65 instrument-change L0, and the mori | round-62 dispatch-surface L0. considerthese 2026-10-26 suggestion 1 (split pin-check mismatches) correctly held behind the instrument-change ruling.
3. SHONEN.md: all four boxes are `[~]` with resolvable pointers; none is checkable-claim-free. A non-author verifier could resolve box 2 and box 3 from the committed receipts (this closure re-ran the underlying evidence); per protocol only a non-author promotion review may write `[x]` — left for the operator's promotion process.
4. Live-surface note for next round (no action owed): S241's live build id (`0.4.03589.8339-b0a05127`) matched the lane's r67 fetch at closure time (~1 h later). The grammar is moment-bound by design; a future redeploy will produce a third id and must classify `asset-churn` again, not `content-drift`.

## 8. Closure decision

Both declared claims verify (re-measured); no axis harmed; conformance clean; trends expansion/quality/discernment all improved with evidence. **Round admitted.**
