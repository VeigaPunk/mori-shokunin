# mori round 38 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
round: 38 (lane HEAD judged: 13f3db7e5c7163e7ef300259ff597a42a79f81f1; entering: f725f3076972e6e70595b5ac8279be524a111ff8)
report judged: .ufo/reports/round-38/mori.md (fleet commit a5015561, author mori-shokunin)

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-38/mori.md` (fleet) | `mori-shokunin a5015561d74eb0f30e7f546f4f21d0f05241c4e5` | PASS |
| SHONEN heading, one line per box | read report | 4 boxes, all `[ ]`, none pre-checked | PASS |
| cited commits exist + ancestor of branch | `git merge-base --is-ancestor <hash> refs/heads/master` for all 8 landed-table hashes + f725f30/13f3db7e/e37dcc6/e33bb561/f10a320d/71abd41/62db24c | all ancestor-OK | PASS |
| lane pushed, no pending work | `scripts/hyaku/jj-lane.sh state` / `git status --porcelain` | `ahead=0 behind=0`; porcelain shows only `?? .scratch/` (pre-round-23 evidence, named in report, intentionally untracked) | PASS |
| prompt carries template contract | read `.ufo/prompts/mori-round-38.md` | template contract + hyaku addendum present | PASS |

Marker test: real report with checkable work and landed commits — not a marker.

## Per-claim re-check

Gate-standard closure consequence binds: the three claims rest on lane-owned instruments
(`count-c4.py`, `conform.py`, `mori-sources-appendonly.py`), so their receipts/tallies were
verified as committed evidence and the frozen pins re-hashed; no sibling gate was executed.
Plain re-measurements over committed bytes were run where possible (git ancestry, row diffs,
receipt greps, census counts, sha256).

### C1 — calibration (content half of the drift-corpus binding) — evidence-verified — axis improved

- `evidence/c4-before.txt` (at e37dcc6): `check anchors FAIL (anchors=0)`, `check capability FAIL`
  (phantom missing path), `COUNTER_EXIT=1` — matches claimed `C4=unmet`.
- `evidence/c4-witness.txt` (fabricated binding d2ee0532 in sandbox): all three token witnesses
  `rejected`; capability FAIL on the dangling path — discrimination control consistent.
- `evidence/v3-token-control.txt`: round-37 counter all-PASS on the same fabricated clone —
  consistent with the claimed `C2=met` on token-satisfying bytes.
- `evidence/c4-after.txt` (at b6993744): four content checks PASS, `unique=True`, one capability
  row — matches claimed `C4=met`.
- Freeze pins re-measured: `sha256sum` of committed `count-c1.py`/`count-c4.py`/`conform.py`
  equals the entries in `evidence/freeze-r38-v3.txt` (5aa51556…, 8332341c…, 580a0bf1…).

### C2 — operability (instrument conformance) — evidence-verified — axis improved

- `evidence/c5-before.txt` (e37dcc6, r37 counters): 6/6 checks FAIL — matches `CONFORM=unmet`.
- `evidence/c5-after.txt` (b6993744, r38 counters): 6/6 PASS including `head_pin` equality and
  `bounded_reads` cap/mkdtemp/scratch — matches `CONFORM=met`.
- `evidence/c5-after-selftest.txt`: `CONFORM_SELFTEST pass=6 fail=0`, each mutation flipping
  exactly its own check.
- `evidence/m13-drain-unbounded.txt`: new checker FAILs the unbounded-drain mutant
  (`CONFORM=unmet` exit 1) — able-to-fail evidence for the M13 hardening.

### C3 — depth (timed supersede semantics + S226) — re-measured + evidence-verified — axis improved

Own re-measurements over committed bytes (no lane gate executed):
- `evidence/gate-before.txt`: full receipt read — no `supersede_timing` line (0 occurrences). PASS.
- `evidence/gate-after.txt:22`: `supersede_timing superseded_as_of=[18 ids] stale_supersede=[]`. PASS.
- `evidence/gate-after-e37dcc6.txt:22`: `stale_supersede=[S069]`. PASS (report and LOG cite
  line 2; the value is at line 22 — report-only citation offset, see defects).
- S069 in-place edit confirmed by row diff: `git show 71abd41:corpus/SOURCES.md` vs
  `62db24c:corpus/SOURCES.md`, row 75 differs in the teaches cell ("lane rule:" inserted).
- Ancestry re-derived: `git merge-base --is-ancestor 71abd41 62db24c` → S073's landing predates
  S069's last edit (stale case); `--is-ancestor 62db24c daa1d4d` → S226's row landing postdates
  the edit. Both hold.
- S226 row at `corpus/SOURCES.md:232` opens `supersedes S069`;
  `corpus/knowledge/containment-timed-supersede-r38.md` cites S226 with
  source/verified-at/recheck lines.
- Gate selftest evidence: `evidence/gate-selftest-after.txt` `pass=9 fail=0`.

### No axis harmed

- `git diff f725f30 13f3db7e -- SCORECARD.md`: only the round-38 declaration rows, capability
  rows, and two append-only correction notes naming superseded text (protocol-conformant).
  Axis-score rows (coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6)
  are identical before and after (grep-diff over both versions: empty).
- `QUALITY.md` +7 lines only: QUALITY 111, lesson M10-backed, append-only, able-to-fail shown.
- SKILL.md / corpus/README.md untouched in the round window.

## Decisive counters (re-derived)

- Seat reports: w1 13, w2 40, resid 8 (`ls w1/*.md w2/*.md resid/*.md`) — matches report.
- Dispatched: w1 65, w2 43 (`counts.total` in w{1,2}-dispatch.json) — matches report; total 116 ≤ 128.
- w2 missing reports: exactly `CritC4Gaming`, `CritC5Gaming`, `ConnReceipts` (43 registry names
  minus 40 report files) — matches the report's 3 never-spawned seats.
- Census rows: 225 at entering tip e33bb561 → 226 at f725f30 and 13f3db7e
  (`git show <rev>:corpus/SOURCES.md | grep -c '^| S'`) — matches the claimed +1 (S226), no
  other row additions; no existing row's status/recheck/used-by cell edited (append-only clean).
- `sources-census.sh validate --root … mori`: exit 0, benign W04 lines only (run by this verifier).

## Spot-check table (LEARNING.md §Discernment is checked from outside)

Round 38's `## Gate` recorded exactly one candidate (S226, admitted) and **zero rejects**
("Rejected: none new"; search log excluded 0), so the reject sample is drawn from the nearest
in-registry reject decisions (SOURCES.md REJECTED rows, corpus registry) and the zero-reject
fact itself is recorded.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S226 — Python os.path.realpath docs | admitted (mined) | live `https://docs.python.org/3/library/os.path.html` (curl, 2026-10-24) + committed copy `corpus/evidence/sources-r38/S226.src` | agree | Quote "Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)." is verbatim at lines 657–659 of both live page and committed copy; 24 words ≤ 25; the source genuinely grounds the canonical-path containment rule that S069's in-place edit restated; row landing postdates the edit (ancestry re-derived above). |
| S065 — Python hashlib docs (corpus reject, 2026-10-21) | rejected | live `https://docs.python.org/3/library/hashlib.html` (curl, 2026-10-24) | agree | Page matches its located description (module introduction; "Hash algorithms" and "Hash Objects" sections present). The rejection reason holds: a hash-API document describes byte digests, not which repository revision supplied bytes, so it cannot support revision-provenance claims. |
| S057 — Wagenmakers et al. 2012 (corpus reject, 2026-10-21) | rejected | DOI `10.1177/1745691612463078` (curl -L, 2026-10-24) | agree | Publisher page sits behind a JS challenge ("Just a moment…") — the reject reason itself records "body not opened; abstract only", so the unverifiable-stronger-claim rejection stands on its stated grounds. |

## Trend verdicts

- expansion — **improved (bounded)**: +1 admitted row (S226, measured 225→226), two knowledge
  entries (`source-drift-content-anchor-r38.md`, `containment-timed-supersede-r38.md`), the
  round-38 lesson; no deletions, no registry cell edits.
- quality — **improved (bounded)**: instruments conformance-checked with committed receipts
  (6/6 met, selftest 6/6), red receipts for M1/M3/M4/M5/M6 + M13 able-to-fail states committed
  with one-spot-mutation reproducers under `.ufo/waves/round-38/scratch/red-receipts/`, freeze
  pins byte-match; residual bypasses (M18/M19) bounded and routed, not hidden.
- discernment — **improved (bounded)**: the lane disclosed that in-round reviewers are all
  dispatched seats and left the outside check open; this non-author spot-check agrees with the
  admit and both sampled rejects; lesson M1–M19 mines nineteen mistakes with receipt-backed
  fixes (M16 backfills the missing able-to-fail receipts the w2 seat found).

## Routed defects for round 39 (minor, status-neutral)

1. `corpus/SOURCES.md` S226 row quote suffix reads `:657-658`; the sentence runs to 659 (lane
   already disclosed this; keep routed until landed).
2. Report/`LOG.md` cite `gate-after-e37dcc6.txt:2` for `stale_supersede=[S069]`; the value is at
   line 22. SCORECARD already cites :22 correctly.
3. `w2/swarm-registry.json` stores `agentId: null` for all 43 members, so "agentId null" is not
   discriminating evidence of never-spawned seats; the count claim itself verifies (43−40, names
   match) but the citation should name the missing-report comparison.
4. `.ufo/waves/round-38/w1-validate.log` is 0 bytes — no committed evidence of the wave-1
   policy-v2 band (64–128) validation the report asserts; claim-adjacent, not one of the three
   measured claims.

## SHONEN note for the operator

All four boxes are checkable by a non-author at this point (this closure session is the named
verifier of record for the report's assertions; seed fidelity was reviewed by the lane's w2 seat
with all boxes left `[ ]`). Whether any box flips to `[x]` and any promotion follows is
operator-owned; this verifier makes no promotion or mint call.

Dispatch/complete digest (from `.ufo/watchdog.log`, mutable): attempts 1–3 of this round died to
orchestrator freezes (19:47, 19:57, 20:17 relaunches; lane-dead-no-report), final attempt
launched 23:10:44, completed 23:52:57-03:00 (hyaku-inline attempt=1). No tool installs or
upgrades were needed or performed by this verifier (curl/git/sha256sum/python3 all present;
none installed).

Verdict: all three claims verify, no axis harmed — **admitted**.
