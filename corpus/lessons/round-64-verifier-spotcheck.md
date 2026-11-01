author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# mori round 64 — verifier spotcheck (non-author closure)

date: 2026-11-01 (UTC) · lane: mori · round: 64 · entering `6e70931d8583…` · landed
`a313f05bd437ed62664103a7a484fe297892f3f3` (branch tip, pushed). All git reads index-free
(`rev-parse`/`cat-file`/`ls-tree`/`diff-tree`/`merge-base --is-ancestor`/`show`/`log`); no
mutating git anywhere. This file is written by the closure judge and is NOT committed by the
lane; the orchestrator commits it.

## 1. Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| Report committed in fleet repo by lane identity | PASS | `git -C <fleet> log --format='%an <%ae> %H %cI' -1 -- .ufo/reports/round-64/mori.md` → `mori-shokunin <mori@shokunin.local> 8c20625d9fd7… 2026-10-31T23:01:36-07:00`; matches the dispatch digest complete line (23:01:36, head=a313f05b, pushed=True) |
| `SHONEN` heading in report | PASS | `## SHONEN` present, 4/4 boxes, all `[~]` with resolvable pointers; no `[x]` anywhere |
| Cited lane commits exist and are ancestors | PASS | entering `6e70931d…` (commit, ancestor), landed `a313f05b…` (commit, ancestor, == refs/heads/master == `ls-remote origin`), plus cited `67efdb79`, `7370a731`, `1592f53d`, `986d4b46`, `b3c25613` — all `cat-file -t`=commit and `merge-base --is-ancestor … refs/heads/master` rc 0 |
| Branch tip pushed | PASS | local `refs/heads/master` = `ls-remote origin refs/heads/master` = `a313f05b…` (ahead=0) |
| Cited work reachable 6e70931d..a313f05b | PASS | `a313f05b`'s parent is `6e70931d` (single-commit round); `diff-tree -r --stat` = 23 files, +4991/−26 — exactly the report's "Landed changes" list |
| Commit-then-report ordering | PASS | lane commit 2026-11-01T05:57:31Z (22:57:31 −07:00) precedes report commit 23:01:36 −07:00 |
| Write scope | PASS | diff touches only lane-repo files; SKILL.md untouched (rule-out 4 respected); no sibling or fleet files |

## 2. Per-claim re-check

### C1 — freshness 5: drift instrument certified on this host + first on-host sweep (verdict: verified met)

Re-measured by closure (commands run by me; receipts read via `git show a313f05b:<path>`):

- **Before.** `git show 6e70931d:tools/mori-source-drift.py | sha256sum` →
  `453c5d8e260301df…` = the before-receipt's pinned input digest; committed receipt
  `evidence/drift-selftest-before-v1-win-r64.txt` shows `MORI_SOURCE_DRIFT_SELFTEST: FAIL
  (5/6)` rc 1 with `huge_cap` grading the transport (`len=None`, `over_cap=unavailable`).
  Sweep receipts at entering: `git ls-tree -r 6e70931d | grep -c drift-live-win` → `0`
  (re-run by me). Sweep state is therefore genuinely new this round.
- **After.** `git show a313f05b:tools/mori-source-drift.py | sha256sum` →
  `eb5affa188b53fd0…` = the after-receipt's disclosed bytes; receipt shows `PASS (6 cases)`
  rc 0 with the scaling disclosed on the PASS line (`transport_cap=65536`,
  `frozen_cap_literal=True`). Tool source greps confirm the frozen
  `FETCH_MAX_BYTES = 4 * 1024 * 1024` literal retained and folded into the arm's pass
  condition, `fetch()` gained `cap=None` defaulting to it, arm names and the rc-2
  `missing_sources_exit2` check unchanged.
- **Kill properties** (committed receipt `evidence/drift-v11-counter-properties-r64.txt`):
  cap-kill mutant → `huge_cap … FAIL` rc 1; redirect-kill mutant →
  `redirect_private_refused … FAIL` rc 1. Both r37/r38 properties re-proven on v1.1 bytes.
- **Sweep.** Receipt `evidence/drift-live-win-r64.txt` re-tallied by me:
  fresh=53 drifted=23 unavailable=2 no-copy=268 → rows=346, summary line
  `MORI_SOURCE_DRIFT rows=346 … drifted=23 …` rc 1. The honest findings state (rc 1) is
  kept.
- **No silent re-pins.** `diff-tree -p 6e70931d a313f05b -- corpus/SOURCES.md` adds exactly
  S574 and S575 and modifies no existing row; no pinned copy for any of the 23 flagged rows
  was added or rewritten this round (the only new files under `corpus/evidence/` are
  `sources-r64/S574.html` and `S575.html`). The class receipt ends: per-row re-adjudication
  is SCORECARD planned r65, "no row bytes were rewritten this round".
- **Classes cite their evidence** (`evidence/drift-findings-ua-vs-content-r64.txt`), and I
  re-opened the class A source myself: curl-UA fetch of S572 → `3f2fd8a26e9258…`
  byte-identical to the pinned r63 copy (re-hashed from the repo — match); tool-UA fetch →
  differs from pinned (and differs run-to-run from the lane's `b49921a4…`, consistent with
  the class's "unstable vendor rendering" reading). Class B pinned-side digests re-verified:
  S241 `1168b2a6…`, S156 `4c029994…` — both match the receipt.

### C2 — depth 5, capability acquisition, sourced: Windows resource-runway probe (verdict: verified met)

Re-executed by closure (not merely evidence-verified — the tool is read-only one-shot; source
reviewed before running):

- **Source review.** `tools/mori-runway-win.py` (committed bytes sha256 `474289d079cf…`,
  matches the live receipt's digest): read-only `GlobalMemoryStatusEx` + `GetDiskFreeSpaceExW`
  via ctypes, standard library only; no writes, no network, no child processes; selftest is
  offline fixtures in a temp dir with cleanup, binary-mode writes; output is counts,
  percentages and state words only (a redaction selftest arm asserts user/path values in a
  fixture never print). Redaction-rule consistent.
- **Selftest re-run by me** (committed copy, two consecutive runs): `RUNWAY_WIN_SELFTEST:
  PASS (9 cases)` rc 0 both — identical to the committed receipt's runs A and B.
- **Live re-run by me** (once, read-only): `RUNWAY_WIN: AVAILABLE surfaces=2 ok=2
  unavailable=0` rc 0; `commit_avail_pct=44`, `free_pct=80`,
  `free_to_caller==free_bytes` — same shape and percentages as the lane's receipt; `load_pct`
  71 vs the receipt's 68, exactly the one-shot volatility the entry discloses (K3, S574:846-847).
- **Sourcing.** SOURCES 346 → 348 re-counted at both revisions
  (`git show <rev>:corpus/SOURCES.md | grep -c "^| S"` → 346 / 348). S574/S575 rows: tier A
  docs, opened 2026-10-31, both pinned copies re-fetched by me byte-identical (`d52b00df…`,
  `0d3c8d30…`); quotes verified at the pinned lines (`S574.html:829` 13 words;
  `S575.html:854` 21 words — counted, ≤25). Knowledge entry
  `corpus/knowledge/runway-win-r64.md` carries the provenance trio; K1–K8 anchors spot-checked
  at the cited pinned lines (829, 844-845, 846-847, 848, 829-831/854, 846-847, 848) — all
  present verbatim. Pre-open duplicate sweep re-checked: 0/0 hits at the entering tip.
- **Capability row** entered SCORECARD with evidence pointer and first-working round 64, per
  AXES.md §Capabilities (demonstrated in-round, not pre-claimed).

### r63 carry-ins D1–D6 (each re-derived)

| Item | Result | Evidence |
|---|---|---|
| D1 mistake 5 relocated verbatim to `## Mistakes` | PASS | `diff-tree -p` on `corpus/lessons/round-63.md`: item text moved byte-identical, correction notes added at both the new site and the vacated `## Assimilation` tail, naming misfiling commit `1592f53d` (exists, ancestral) |
| D2 second after-state selftest run committed | PASS | one receipt `selftests-rerun-and-guard-argv-r64.txt` carries run A and run B: 12/10/16/125 pass, 0 fail, all rc 0, identical |
| D3 full argv in receipts incl. guard `--expect` | PASS | receipt header prints every invocation; guard line: `python tools/mori-receipt-complete.py … --expect 14` → `RECEIPT_COMPLETE=complete … anchors=14` rc 0 |
| D4 "first Microsoft Learn rows" correction | PASS | recorded in LOG Round 64, SCORECARD Round 64, round-64 lesson item 4, and the report; substance verified from the registry: S241 = learn.microsoft.com ja-jp Azure OOM page opened 2026-10-24, predates S572/S573 (opened 2026-10-31) |
| D5 100644 mode note | PASS | recorded in LOG/SCORECARD/lesson: treecommit pins mode 100644 for new blobs; working-tree exec bit cannot reach the index; immaterial on this host (`python tools/…`), POSIX-portability note |
| D6 census wording corrected (junctions, no lag clone) | PASS | LOG r63 entry and r63 lesson corrected with inline notes naming the superseded wording; host-inspection basis recorded; census validator re-run by me at closure → rc 0, consistent with the corrected reading |

## 3. Axis-harm check

`diff-tree -p 6e70931d a313f05b -- SCORECARD.md` is a pure append: the Round-64 section plus
the capabilities row; no prior axis row modified. Scores entering/after unchanged
(coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 — no scalar
claimed). Spot reads of prior sections intact. No axis harmed.

## 4. Discernment spot-check (outside view)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S574 GlobalMemoryStatusEx (docs, A, mined) | admit | URL re-fetched; digest byte-identical to pinned `d52b00df…`; quote at `:829` (13 words) | agree | Primary vendor doc, correctly tiered; grounds K1–K4; used-by the admitted entry |
| S575 GetDiskFreeSpaceExW (docs, A, mined) | admit | URL re-fetched; digest byte-identical to pinned `0d3c8d30…`; quote at `:854` (21 words, counted) | agree | Primary vendor doc; the quota caveat at `:854` is exactly the boundary the probe's free_pct-from-caller choice encodes (K6) |
| Class A drift reading for S572 (finding kept, not re-pinned) | classing | curl-UA and tool-UA re-fetches by me; pinned copy re-hashed | agree | curl-UA byte-identical to pinned → serving-side, not content drift; classing (not normalizing) is the right disposition pending r65 |
| Reject-class: fresh-start rule-out (3) old-Linux live surfaces unavailable | rule-out | `command -v journalctl` → not found; `/proc/pressure` absent | agree | Surfaces genuinely absent on this host; honest `unavailable` beats a fake probe |
| Reject-class: fresh-start rule-out (1) r59/r60 instruments not re-declared | rule-out | prompt §7 r59 digest (met-flip counterexamples on frozen bytes); freshstart receipt: frozen counter at `986d4b46…` → `C2=unmet`, 14 quote_words anchors, rc 1; `986d4b46`/`b3c25613` ancestral | agree | Re-declaring on decertified instruments would relitigate frozen counterexamples; rule-out correct |

The lesson's Gate records "reject sample: none met — no source rejections this round", naming
the fresh-start rule-outs as the round's reject-class decisions; that is honest (both new rows
were admits). Census validator re-run by me at closure: rc 0 (tolerated W04 duplicate-URL
class, unchanged) — matches `census-end-r64.txt`.

## 5. Per-axis verdicts and trend verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| freshness | improved | C1 verified met (instrument certified on this host, kill-properties re-proven, first on-host sweep with 23 findings classed and flagged — none re-pinned or dropped) |
| depth | improved | C2 verified met (capability re-executed by closure: selftest 9/9 ×2 + live AVAILABLE; sourced S574/S575; K1–K8 line-verified; capability row entered) |
| coverage | unchanged | no coverage claim; PROVINCE host note records the new Windows-host instrument (frontier recorded, not claimed) |
| operability | unchanged | no operability claim; existing instruments' selftest tallies re-committed (12/10/16/125) and drift/runway selftests pass — no regression |
| calibration | unchanged | no calibration claim; honest rc 1 sweep, disclosed load-condition retake, and the volatile one-shot reading are calibration-positive but unclaimed |
| adjacency | unchanged | no cross-domain work; sibling settlement collection untouched |

Trends: **expansion: improved** (capability row entered with passing demonstration; new
knowledge entry on Windows resource-runway ground, sourced to mined rows; SOURCES 346 → 348 —
re-counted). **quality: improved** (instrument certified with counter-properties re-proven;
findings classed with two-UA digest evidence rather than normalized; entry anchors
line-located against digest-matched pinned copies; no admitted entry failed a re-check — the
S241 drift is marked, receipted, and routed to r65 disposition, not left unmarked).
**discernment: improved** (honest findings state kept; near-misses mined including a caught
heredoc truncation and a self-caught quote miscount; per-row adjudication deferred rather than
silently greened; my spot-check agrees on both admits and both sampled rule-outs).

## 6. Routed defects (status-neutral; the lane fixes these next round)

1. **Number-drift, self-defect (route to r65).** LOG.md's Round-64 entry says "Mistakes
   mined: three" and lists three, but `corpus/lessons/round-64.md` `## Mistakes` carries four
   rows (the report and its Sources & frontier section say four; the fourth is the S575 quote
   word-count mistake). LOG.md is append-only: fix by appended correction entry, not a rewrite.
2. **Observation, no action forced.** D6 (and D1's vacated-slot note) applied in-place wording
   corrections inside LOG.md's r63 entry and the r63 lesson rather than appending new entries —
   disclosed inline at both edit sites, no measured value changed, grounded in the cited
   `67efdb79` precedent (commit exists, ancestral). The append-only letter prefers new
   entries; keep the precedent narrow.
3. **Standing (already SCORECARD planned r65):** per-row disposition of the 23 flagged drift
   rows (refetch-and-repin or supersede, settling the UA question per vendor), then a re-sweep
   to drifted=0 or an honest remainder.

Operator note: SHONEN boxes 2 and 3 now carry resolvable pointers that this closure
re-verified directly (LOG Round 64 entry + round-64 receipts; selftest tallies re-committed
and re-executed: 12/10/16/125, drift 6/6, runway 9/9 ×2 + live). On this round's evidence
those two boxes look checkable by a non-author; no `[x]` was written (closure duty bars it;
promotion review is operator-directed).
