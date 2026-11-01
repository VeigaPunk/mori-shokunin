# mori round 69 — verifier spot-check (closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
round: 69
lane: mori-shokunin (branch master)
entering: `c53dd7895b3e4a7391215972dc4e4d83f78b4b08` · landed: `dee4f67818c4a623c99276b522577a095c43f66a` (branch tip, pushed)
closed_at: 2026-11-01T19:06:47Z

All commands below were run by this verifier at closure time against the lane
repo working tree (byte-identical to `dee4f678` for every file checked:
`tools/mori-ua-variance.py` sha256 `5528b961…`, `corpus/SOURCES.md` sha256
`d4f97b48…` both equal their `git show dee4f678:…` hashes). Index-free git only.
Per the mori standing redaction rule this file carries counts, shapes, hashes
and public-URL facts only.

## 1. Step-1 conformance — CLEAN

| Check | Command | Observed | Verdict |
|---|---|---|---|
| Report committed in fleet repo by lane identity | `git -C <fleet> log --format='%an %ae %H' -1 -- .ufo/reports/round-69/mori.md` | `mori-shokunin mori@shokunin.local 154577d842733c25d2b9f0a41e5bc7d327e4826e` | PASS |
| `SHONEN` heading in committed report | `git show 154577d8:…mori.md \| grep -n "^## SHONEN"` | line 168 `## SHONEN`, 4 boxes, all `[~]` | PASS |
| Lane HEAD == cited landed hash | `git -C <lane> rev-parse refs/heads/master` | `dee4f67818c4a623c99276b522577a095c43f66a` | PASS |
| Branch tip pushed | `git -C <lane> ls-remote origin refs/heads/master` | equals local `refs/heads/master` | PASS |
| Entering hash ancestral | `merge-base --is-ancestor c53dd7895b3e refs/heads/master` | rc 0 | PASS |
| r61 data tip `986d4b46` exists + ancestral | `cat-file -t` / `merge-base --is-ancestor` | `commit`, rc 0 | PASS |
| r60 revision `b3c25613` (cited in the committed freshstart receipt) ancestral | `merge-base --is-ancestor` | rc 0 | PASS |
| Content digests resolve | `git show c53dd789:tools/mori-ua-variance.py \| sha256sum`; `git show dee4f678:corpus/evidence/sources-r69/S580.html \| sha256sum` + `wc -c` | `3f6eb7a625b5ab00…` (the report's r68-bytes digest); `238ec28d962bb58a…`, 15183 bytes | PASS |
| Round work reachable, scope clean | `git log --format='%H %an' c53dd789..dee4f678`; `diff --name-only` | one commit, authored `mori-shokunin`; 18 files +1022/−27 (report says exactly this); every path inside the lane repo | PASS |

Report is a real report (work, evidence pointers, LOG-tied changes, checkable
hashes), not a marker. Dispatch digest (launch 07:58:40-08:00, complete
10:10:09-08:00) brackets every receipt timestamp in the round (16:19Z–17:38Z =
08:19–09:38 -08:00). No conformance defects found.

## 2. Per-claim re-check

### C1 — calibration: the observation-window grammar (QUALITY 161) — RE-MEASURED, VERIFIED

- Before/after: `git show c53dd789:corpus/QUALITY.md | grep -c "^161\."` → `0` rc 1;
  at `dee4f678` → `1` rc 0. `^158\.`, `^159\.`, `^160\.` = 1 each after; the
  QUALITY.md diff is append-only (criterion 161 added, nothing rewritten).
- Able-to-fail re-run by this verifier:
  `git show dee4f678:.ufo/waves/round-68/evidence/s241-uavariance-r68.txt | grep -c "window-s="` → `0` rc 1
  (the rule fires on the r68 receipt — its as-of stamps 13:53:46Z→14:14:54Z are
  1268 s apart and its grammar carried no window token); over the r69 receipt →
  `4` hits, `window-s=4015` exactly 3. Matches the committed demonstration
  receipt `quality161-abletofail-r69.txt` line for line.
- Tool side at `dee4f678`: `--window-s` parsed; `WINDOW_S_RE = ^[0-9]+$`;
  non-integer → rc 2 setup error (selftest `window_rejects_non_integer` asserts
  rc 2 with empty stdout); omitted → `window-s=unavailable reason=not-stated`;
  docstring carries the window-dependency paragraph; selftest case names
  `window_stated_when_given` / `window_unstated_marked_unavailable` /
  `window_rejects_non_integer` present.
- Entering controls receipt (`controls-r69.txt`): `^161\.` = 0, `window-s=` = 0,
  `recheck-summary` = 0, r69 receipt absent rc 128 — a do-nothing round reaches
  none of this.

Verdict: **improved** (calibration 5, score held — consistent with the lane
convention that no closure states a new number).

### C2 — depth, sourced S580: the stated-window receipt — RE-MEASURED + INDEPENDENTLY RE-DERIVED, VERIFIED

- Receipt present at `dee4f678`; absent at entering (controls receipt, rc 128).
- Window math re-derived: capture A `as-of=2026-11-01T16:23:39Z`, capture B
  `as-of=2026-11-01T17:30:34Z` → 4015 s. Compare line re-read:
  `per-response=4 stable=1497 stable-not-in-pin=2 stable-in-pin=1495 lines-a=1499 lines-b=1499 lines-pin=1499 same-bytes=false window-s=4015 crosscheck=consistent` rc 0; sha-a/sha-b equal the two capture blocks' own shas.
- Helper byte-equality receipt independently re-derived two ways: (a) hashing
  the four helper function bodies (`fetch`, `capture`, `now_utc`, `sha256_hex`)
  extracted from `c53dd789` and `dee4f678` bytes — identical pairs; (b)
  diff-hunk placement — no hunk touches any of the four bodies (the nearest
  hunks insert constants before `now_utc` and insert two new functions after
  `capture` ends at its `return 0`). Capture A ran at the entering tool bytes
  (sha256 `3f6eb7a6…`), capture B at the final bytes (`5528b961…`); both digests
  re-computed and matching.
- Honest no-TTL-separation finding verified against both receipts: the r68
  receipt's diff positions are exactly lines 218 and 1498 (window 1268 s); the
  r69 receipt's diff positions are exactly lines 218 and 1498 (window 4015 s).
  Both positions rotate within BOTH windows, and the receipt states plainly
  that the two windows cannot separate the positions' rotation clocks, that TTL
  separation remains unmeasured, and that no TTL value is decided. This is an
  honest null result, correctly reported as metadata, not as a lifetime.
- `stable-not-in-pin=2` decomposition: a-lines not in pin = [163, 211, 218,
  1498]; asset-id segment at exactly [163, 211] — unchanged from r68; the r68
  planned item's growth arm did not materialize, as reported.
- Pin identity: `git show dee4f678:corpus/evidence/sources-r42/S241.html | sha256sum`
  → `1168b2a626ec4b69…` — the same pin digest the r68 compare line carries.
- S580 grounding: row re-opened live this closure (below) — byte-identical.

Verdict: **improved** (depth 5, score held; sourced on S580+S579 as claimed).

### C3 — operability: the standing cross-check arm (`--recheck-summary`) — RE-RUN LIVE BY THIS VERIFIER (read-only), VERIFIED

- Evidence-verified side: at entering `grep -c "recheck-summary"` = 0 (controls
  receipt); at `dee4f678` the tool carries `parse_recheck_summary`,
  `crosscheck_verdict`, and the `--recheck-summary` arg; the committed final
  selftest receipt shows five crosscheck arms (consistent / inconsistent-is-lead
  rc 0 / reverse-disagreement rc 0 / absent-arm unavailable / non-summary rc 2)
  inside `MORI_UA_VARIANCE_SELFTEST: PASS (14 cases)` x3 at the final bytes
  (`uavariance-selftest-final-r69.txt` carries the tally 3 times). Selftests
  were NOT re-executed by the verifier except through the live run below.
- Live re-run performed by this verifier (read-only network GETs, scratch-only
  writes), 2026-11-01T18:48–18:51Z, working bytes == `dee4f678`:
  1. Two same-UA captures 18:48:23Z — both `rc=0`, 54343 bytes, identical
     sha256 `8d113471…` (same-second pair; no rotation caught).
  2. `python tools/mori-drift-recheck.py --root . --only S241` → rc 0, stderr 0
     bytes, `asset-churn=1` (`MORI_DRIFT_RECHECK rows=1 adjudicated=1 …
     asset-churn=1 …`), same shape as the round's 17:30:35Z re-check.
  3. `python tools/mori-ua-variance.py --compare --label r69-closure-xcheck
     --pin corpus/evidence/sources-r42/S241.html --a … --b … --window-s 0
     --recheck-summary <recheck file>` → rc 0:
     `per-response=0 stable=1499 stable-not-in-pin=4 stable-in-pin=1495 lines-a=1499 lines-b=1499 lines-pin=1499 same-bytes=true window-s=0 crosscheck=consistent crosscheck-basis=stable-not-in-pin=4+recheck-asset-churn=1`.
- Reading: the arm runs live, stays rc 0 (a lead, not a failure), names both
  counts in its basis, and agrees (`consistent`). My 0-second window caught
  `per-response=0` where the round's 21/67-minute windows caught
  `per-response=4` at two positions — an independent corroboration of the
  window-dependency finding (C1/C2). My `stable-not-in-pin=4` = the 2 asset
  lines + the 2 token lines of a byte-stable pair, matching the receipt's own
  2+2=4 control decomposition. The receipted FIRST live agreement
  (`stable-not-in-pin=2` + `recheck-asset-churn=1` → `consistent`) is
  internally consistent across its compare line and recheck block.

Verdict: **improved** (operability 7, score held).

## 3. No axis harmed

- `git diff c53dd789 dee4f678 -- SCORECARD.md` is append-only (new round-69
  section from old line 3435); the axes table bytes are untouched — no score
  changed, no axis moved downward.
- Frozen set absent from the round diff (name-only path list contains no
  SKILL.md, PROVINCE.md, AGENTS.md, corpus/README.md, mori-source-drift.py,
  mori-drift-adjudicate.py) — the r65 L0 (SKILL:905 tally pin) stays true by
  construction and routed around, as claimed.
- Standing battery receipt (`selftests-battery-r69.txt`) matches the report
  exactly: register 12/12, settlement 10/10, vote-bind 16/16, pin-check 125/125,
  adjudicate 5/5, recheck 10/10 — all on unchanged bytes. Evidence-verified,
  not re-executed.
- LOG.md append-only (+106 lines, Round 69 entry); SHONEN.md marks confined to
  `[~]` + evidence-line updates (no `[x]` written, no box or seed text changed).

## 4. Discernment spot-check (non-author, outside)

| Item | Decision | Re-opened source / re-run | Agree/disagree | Reason |
|---|---|---|---|---|
| Admit: S580 AWS WAF token characteristics (the round's one new SOURCES row) | admit, tier A, mined | Live re-open `curl -sS -m 60 -L` of the row's URL: 15183 bytes, sha256 `238ec28d962bb58a…` — byte-identical to the committed pin `corpus/evidence/sources-r69/S580.html`; both quotes present at the cited lines (`:63-64` 16 words, `:70` 12 words); `<title>` matches | AGREE | The row's `teaches` (token content carries the timestamps of the client's latest successful challenge responses → an observation's window is load-bearing) is grounded in the pinned bytes and is exactly the fact C1/C2 rest on; position (line 361, immediately after S579, inside Registry before `## Paths`) honors the r68 sectioned-append rule; census validator rc 0 |
| Reject-class sample: not adopting considerthese 2026-10-26 suggestion 1 (split pin-check mismatches) | reject (defer) | Verified the ground: `considerthese/2026-10-26.md` exists and characterizes suggestion 1 correctly (the pin-check mismatch is "can't run here" vs "stale"); the mori \| round-65 L0 line (instrument-change ruling) is present and unanswered in the fleet `.ufo/l0-questions.md` (line 242); the pin-check tally pin is SKILL-cited | AGREE | The rejection is procedural, not evasive: the change alters a tally-cited instrument's reported behavior, which sits behind an open operator ruling — and the lane routed around it without editing any frozen byte |
| Census validator (contract step 3) | — | `bash <fleet>/scripts/sources-census.sh validate --root <fleet root> mori` → rc 0; only `W04 duplicate-url-across-scopes` warnings (the tolerated class the round's census receipts name); the validator resolves the lane through the fleet-root symlink to this same repo (SOURCES.md sha256 `d4f97b48…` == `dee4f678` bytes, 353 rows) | — | PASS; matches both census receipts (rc=0) |

Gate section honesty note: `## Gate` says "reject sample: none met — no source
rejections this round" and names the fresh-start rule-outs as the reject-class
decisions; this verifier sampled one of those and agrees (above).

## 5. Mined mistakes — all three real in the disclosed run history

1. Silent-StringIO scoping bug (testing): the pre-fix receipt
   (`uavariance-selftest-r69.txt`) shows three consecutive bare `rc=1` lines —
   zero diagnostics — at disclosed uncommitted working bytes; the final receipt
   shows `PASS (14 cases)` x3 at `5528b961…`; the committed tool's restore
   lines spell `sys.stderr` (the fix as described). REAL.
2. Negative sweep before its receipt (landing): `source-sweeps-r69.txt` marks
   the pre-row block attested-not-captured (16:31–16:33Z, un-receipted) and
   re-runs post-row where each hit IS the S580 row (1/1/0). This verifier
   re-ran the post-row counts (`waf-tokens-details` = 1; `^| S` rows = 353).
   REAL.
3. Near-write outside the lane root (landing): disclosed as a mistyped
   `…/website_fleet/` path beside the lane root, caught on the Write tool's own
   path report and deleted before any receipt cited it. The checkable residue
   is the claim itself: no `website_fleet` directory exists anywhere under the
   workspace (find, depth 3), and every receipt path the round cites resolves
   inside `fleet/mori-shokunin/`. REAL (residue-free by deletion; attested by
   the author, consistent with all committed paths).

## 6. Trend verdicts (this verifier's grades — they agree with the report)

- **expansion: improved** — SOURCES 352 (`c53dd789`, re-counted by this
  verifier) → 353 (`dee4f678`); the S580 row is opened, pinned byte-identical,
  and mined; a capability row entered the SCORECARD capabilities table
  (first-working round 69) with a demonstration this verifier re-ran live. No
  admitted entry failed its bar.
- **quality: improved** — the stated-window receipt answers the r68 planned
  question honestly (TTL separation reported unmeasured, no value decided);
  the standing battery is green on unchanged bytes; the one defect the round
  introduced was caught, fixed, selftest-proven 14/14 x3, and mined. No entry
  found false and left unmarked.
- **discernment: improved** — QUALITY 161 is procedural and demonstrated
  able-to-fail against the lane's own prior receipt; the claims name their own
  limits (window = metadata; crosscheck decides nothing; no row re-classed;
  QUALITY 159 untouched); the rejected alternatives are on record with reasons;
  this verifier's admit and reject samples both AGREE.

## 7. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 re-measured + able-to-fail re-run (above) |
| depth | improved | C2 receipt re-derived, helper byte-equality independently confirmed, sourced S580 re-opened live |
| operability | improved | C3 arm re-run live by this verifier: `crosscheck=consistent`, rc 0 |
| coverage | unchanged | no coverage claim; corpus surface set untouched |
| freshness | unchanged | no freshness claim; standing re-check run as C3's input, no re-pin claimed |
| adjacency | unchanged | no sibling surface touched; QUALITY 159 vendor scoping untouched |

## 8. Routed defects the lane must fix next round

None. No conformance defect, no red gate, no routed item arises from this
closure. Notes for the operator (status-neutral):

- All four SHONEN boxes now look fully checkable by a non-author: this verifier
  re-derived box 1's QUALITY 161 fact and demonstration receipt, box 2's Round-69
  LOG entry and receipts, box 3's selftest receipts (14/14 x3 at the committed
  bytes) plus a live run of the tool, and box 4's no-bleed diff check. Per the
  promotion gate, only a non-author may write `[x]`; this closure deliberately
  writes none — the operator decides whether to run the promotion review.
- Carried open items (unchanged, correctly routed around, never treated as
  answered): the mori | round-65 instrument-change L0 and the mori | round-62
  dispatch-surface L0 — both still open in the fleet `.ufo/l0-questions.md`.
- Round-70 planned items in SCORECARD are falsifiable and follow from this
  round's honest null (short repeated windows to bound each position's rotation
  from above; the crosscheck inconsistent branch has no live observation yet —
  selftest-proven only).
