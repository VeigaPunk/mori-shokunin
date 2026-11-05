# Round 92 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Lane: mori. Round: 92 (attempt 1). Report: `.ufo/reports/round-92/mori.md`.
Entering `f63d1ab030d4179576e494342f48ef8718e497a5`; landing `9dce2ca6f6510cbb8fa41c5c1b8d8a802169e9c1`;
after-bookkeeping `587c7dfe13a637c8a82515eed8233827f4d58a5f` (= master = origin/master at check time).
Re-checks were run by plain commands over committed bytes (`git show <rev>:<path>`, `git ls-tree`,
`git log --diff-filter=A`, `sha256sum`, `pdftotext`) and by reading external sources. The lane's gates
(`count-c1.py`, `count-c2.py`, `tools/mori-source-digest.py --selftest`) were NOT executed; their committed
receipts were read and cross-checked by the plain commands below.

## 1. Conformance (protocol step 1)

| Check | Command and observed output | Result |
|---|---|---|
| Report attribution | `git log --format='%an %H' -- .ufo/reports/round-92/mori.md` → `mori-shokunin 5238fc0105f998403f5ecfd1afba7d5e593de4c0 round-92: mori report` | ok (lane identity, fleet repo) |
| SHONEN heading | `grep -c '^## SHONEN'` on the report → 1; four lines `[~]` with pointers | ok (one line per box) |
| Section order | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, SHONEN | ok |
| Cited lane commits exist | `rev-parse --verify` on `f63d1ab0`, `587c7dfe`, `9dce2ca6`, `699f6276` → all resolve | ok |
| Ancestry vs branch ref | `git -C mori-shokunin merge-base --is-ancestor <h> master` → true for `699f6276`, `9dce2ca6`, `587c7dfe`, `f63d1ab0` | ok |
| Lane state | `jj-lane.sh state mori-shokunin` → `branch=master local=587c7dfe… remote=587c7dfe… ahead=0 behind=0 head=detached tracked=0 untracked=1`, rc 0 | ok |
| Lane porcelain | `git status --porcelain` → `?? .ufo/waves/round-92/w1.ready.dispatched` | defect, status-neutral (see D5) |
| Remote | `git ls-remote origin refs/heads/master` → `587c7dfe13a637c8a82515eed8233827f4d58a5f` | ok |
| Prompt template contract | `.ufo/prompts/mori-round-92.md` carries §1–§5 (MISSION/AXES binding, 1–3 claims, frontier step, L2 floor, report contract, commit/push/L0) | ok |
| Wave composition | report: 11 seats, executor 1, scribe 3, scout 1, reviewer 3, critic 1, mutation-tester 1, connector 1; prompt minimum split is 3 executors | defect, status-neutral (D4) |
| Attack share | reviewer 3 + critic 1 + mutation-tester 1 = 5 of 11 = 45 % (floor 25 %) | ok |
| Dispatch digest | `.ufo/watchdog.log:2767` `2026-11-05T04:30:21-03:00 launch mori round=92 pgid=2434994 driver=hyaku-inline attempt=1`; `:2777` `2026-11-05T05:25:31-03:00 complete mori round=92; hyaku-inline attempt=1` | ok (digest copied into closure notes) |
| Status | substantive report with evidence pointers, commits, measurements; not a marker | `ok` |

## 2. Claims (per-claim re-check)

### C1 — depth: provenance trio in the first 12 lines of every `corpus/knowledge/` entry

Re-measured by me (plain `git show` over committed bytes; the frozen counter was not run):

```
for f in $(git ls-tree -r --name-only <rev> corpus/knowledge/ | grep '\.md$'); do
  git show <rev>:$f | head -12 | grep -E '^(source|verified-at|recheck):' ...
```

- `f63d1ab0`: `knowledge=98 with-trio=79`; 19 files miss at least one key (matches the lane's control `missing=19`).
- `587c7dfe`: `knowledge=98 with-trio=98`. Presence re-derived: **met**, 98 of 98.
- Move-only check (removed non-blank lines of the 19 diffs, each required to reappear byte-identical among additions): `notreappear=0` for all 19 files. Removed blank lines: 1 in `drift-pin-r10.md`, 1 in `lane-silence-r2.md` (lane disclosed both). Body text is unchanged.
- Truth spot-check of the trio `verified-at` value against the contract's landing constraint (`.ufo/waves/round-92/contract.md` line 36: "`verified-at` names the admission commit of the file"), via `git log --diff-filter=A --format=%h -- <file> | tail -1`:
  - 7 of 19 name the admission commit (`audit-r11` e4855e8c; `progressing-weak-r2`, `silence-grading-r2` 3da84149; `silence-cutover-r3` 1439c473; `verdict-machine-r4` 5b62c897; `-r5` a420deb7; `-r6` 92b2e427).
  - 12 of 19 do not: they carry a verification date or round tag instead (for example `counter-semantics-r78` → `2026-11-02 (round 78 …)` against admission `2360cc3b`; `lane-silence-r2` → `2026-10-15T04:56Z` against `3da84149`; also `counter-win-r77`, `drift-pin-r10`, `execution-binding-r89`, `kernel-v7.3-recheck-r53`, `rotation-receipt-grammar-r76`, `rotation-schedule-r74`, `rotation-series-r75`, `selftest-flake-r9`, `surfaces-r8`, `workstate-win-r71`).
  - The lesson's `## Work` section (round-92.md lines 51–52) states "Each `verified-at` names the admission commit of its file". That sentence is false for 12 of 19 files. Routed as D1.
- The `source:` and `recheck:` lines were not re-opened one by one; the lane's own QUALITY 194 says the counter checks presence only and that truth is a non-author check. The `verified-at` sample above is the truth check performed here.

Re-measured vs evidence-verified: the C1 count (98/98, presence) is **re-measured**; the lane's control and after receipts (`evidence/controls-r92.txt:3`, `evidence/after-r92.txt:3-4`) are evidence-verified as consistent with that count.

Verdict on the claim: the frozen predicate (presence) verifies. The depth axis is not shown by presence-only metadata (the lane's attack `Mo92R01Atk` accepted three forgeries, and 12 of 19 `verified-at` lines break the contract's own rule). The claim verifies as a measured presence predicate and does not establish the depth move. See §3.

### C2 — freshness: registry digest gate reports zero unresolved mismatches

Not re-executed (sibling gate). Committed receipts read: `.ufo/waves/round-92/evidence/after-r92.txt:6` → `C2=unmet mismatch=0 superseded=2 superseded_ids=S235,S615 prefix_only=31 unpinned=1 negatives=0 selftest=pass checks_failed=run_rc,superseded_ids,negatives rev=9dce2ca6f651`, rc 1; `:9` → `DIGEST_CHECK rows=122 ok=88 mismatch=0 superseded=2 prefix_only=31 unpinned=1`.

Plain cross-checks of the two rows the claim turns on:
- S615 recorded digest (`corpus/SOURCES.md` line 397 at `587c7dfe`): `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0`. Pinned copy `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` at `587c7dfe`: `sha256sum` = `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`, 362493 bytes. The recorded digest is wrong at its tail, so the S615 mismatch is real; the S619 correction (`supersedes S615`) carries the full correct digest.
- S235 committed copy `corpus/evidence/sources-r42/S235.pdf` at `587c7dfe`: `sha256sum` = `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`. S235 row and the pre-existing S349 row (line 246 at `f63d1ab0`) both record this digest, so S349 is a valid successor of S235. The frozen successor map expected a new S620, which the lane did not write; the premise defect is real.

Verdict on the claim: unmet as frozen (`superseded_ids` names S620, actual successor is S349; `negatives` needs an S620 row; `run_rc` is the QUALITY 193 exit rule). Not admitted. The lane's honest stop is accepted.

Re-measured vs evidence-verified: the two row digests and the S349 successor are **re-measured**; the counter's `mismatch=0` and the negative fixtures are **evidence-verified** from committed receipts only.

## 3. Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| depth | `unprovable` | C1's frozen predicate (presence) is met and re-measured at 98/98, but presence-only provenance metadata does not establish the axis (verifiable technical detail). Attack showed forgeries pass; 12 of 19 `verified-at` lines break the contract's own admission-commit rule. Not `harmed`: body text is move-only. |
| freshness | `unchanged` | C2 unmet as frozen; not admitted. The registry mismatch count moved 2 → 0 by supersession (S349 pre-existing; S619 new and correct), but the frozen predicate's clauses are not met, so no axis move is credited. Not `harmed`. |
| coverage | `unchanged` | No claim; no score moved in `SCORECARD.md` diff. |
| operability | `unchanged` | No claim; the digest tool gained a selftest, which is a capability row, not an axis score change. |
| calibration | `unchanged` | No claim; no score moved. |
| adjacency | `unchanged` | No claim; no score moved. |

SCORECARD diff check: `git diff f63d1ab0 587c7dfe -- SCORECARD.md` → `@@ -4705,3 +4705,26 @@`, all lines additive (new `## Round 92` section, capability row, planned list). No score line changed. No owned axis harmed.

Admission: **false**. C2 unmet; C1 verifies only as presence.

## 4. Discernment spot-check (LEARNING.md; `corpus/lessons/round-92.md` `## Gate`)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S619 (`docs.python.org/3/library/ast.html`, pinned copy) | admit (mined) | pinned copy at `587c7dfe`: `sha256sum` 7891c588…42f5, 362493 bytes; quote "Recursively yield all descendant nodes in the tree starting at node" found 1× in the tag-stripped text; 11 words (≤ 25) | agree | Row digest matches pinned bytes; quote located; correction of record for S615's wrong digest is valid. |
| S620 (`supersedes S235`) | reject (not written) | `corpus/SOURCES.md` line 246 at `f63d1ab0` (S349); `corpus/evidence/sources-r42/S235.pdf` sha256 9855a498…8020 at `587c7dfe` | agree | S349 already supersedes S235 with the same full digest; a second successor row is redundant. The flip condition in the lesson (S349 invalid or different digest) is itself checkable and false today. |
| S621 (FIPS PUB 180-4, §6.2) | queued (opened, no knowledge entry cites it) | `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf`: 833315 bytes (= row), PDF page 26 (printed p. 21); pdftotext line-wrap joins "256-bit / message digest." → quote "The final result of SHA-256 is a 256-bit message digest." matches 1× after whitespace normalization; 10 words; my sha256 0455b406…deb82 | agree | Queued status is correct; quote is located. The row records no digest, so byte identity to the scout's copy rests on size only (D7). |
| New row re-open (≥1 required) | — | S619 and S621 re-opened above | agree | Quotes ≤ 25 words; both re-located. |
| Knowledge trio sample: `counter-semantics-r78.md`, `lane-silence-r2.md` (landed trio lines) | admitted by lane as presence fix | git admission commits `2360cc3b`, `3da84149` | disagree (with the lesson's rule, not with the file's body) | `verified-at` carries a round date, not the admission commit the contract requires. The file's own body header does state the round date, so the value is not false. Routed as D1. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok …/mori-shokunin/corpus/SOURCES.md`, rc 0, with W04 duplicate-URL warnings (S619 shares S615's URL, S349 shares S235's URL; pre-existing pattern). Row count `grep -cE '^\|?\s*S[0-9]{3}\s*\|'` at `587c7dfe` → 393; at `f63d1ab0` → 391 (matches the lane's census receipts).

Gate decisions: 2 of 2 sampled decisions agree (admit S619, reject S620); S621 queued agrees. Depth ruling on C1 agrees with the lane's own "met as frozen; depth not established".

## 5. Trend verdicts (non-author)

- **expansion: unchanged.** One correction row (S619) and one queued source (S621); no knowledge entry admitted. Agrees with the lane.
- **quality: unchanged.** No admitted entry failed a re-check (the 19 trio edits are move-only). Quality gained presence metadata but not verified provenance: 12 of 19 `verified-at` lines break the contract rule. The S615 digest defect is corrected by a new row, which is a real quality move on a single row; net unchanged.
- **discernment: unchanged.** Admit and reject sampled decisions agree on re-open. The unlearned disagreement is the lesson's false sentence about `verified-at` (round-92.md lines 51–52), which is a self-description, not a gate decision. Read strictly under LEARNING.md this could be `harmed`; it is graded `unchanged` here and routed as D1 with a required fix in round 93. The operator may rule the other way.

## 6. Routed defects (for the mori lane, round 93)

- **D1** (lesson and landed trio lines): correct `corpus/lessons/round-92.md` lines 51–52 by appended correction entry (not in-place), and bring the 12 `verified-at` lines in line with the contract (admission commit) or record why not. Evidence: §2 C1 table above.
- **D2** (frozen predicate premise): already recorded as Mistake 1 and QUALITY 196. Confirmed here. Round 93 re-declaration must grep the premise before the freeze, as planned.
- **D3** (stale receipt): `.ufo/waves/round-92/w1/Mo92E01Digest.after-run.txt` is an executor-era run (tail shows `DIGEST S620 ok` and `DIGEST_CHECK rows=123`), which predates the landed registry (no S620). Cite the landing-revision evidence (`evidence/mutants-r92.txt` control line, `evidence/after-r92.txt`) for landed state, or re-run and commit a landed-state receipt.
- **D4** (wave composition): prompt §3 minimum is 3 executors; the wave had 1 executor and 3 scribes. Status-neutral; correct the role mix in the next wave.
- **D5** (lane tree): untracked `.ufo/waves/round-92/w1.ready.dispatched` (orchestrator marker) sits in the lane repo. Not lane work; keep out of lane commits or ask the orchestrator to move it. Status-neutral.
- **D6** (format): S619 row is written as `|S619|…` (no interior spaces) while the file uses `| S### |`. It parses (census rc 0, 393 rows); normalise on next touch.
- **D7** (source row): S621 records no pdf digest. Add the sha256 of the copy used to locate the quote if the row becomes `mined`, or state that the copy is not retained.

## 7. Notes on SHONEN and promotion

No box is `[x]` and none is signed by a non-author here. Box 3 (instructions executable without oral context) names a selftest command that a non-author could run; this check did not run it (sibling gate). Promotion is operator-owned. Nothing in this file writes `[x]` into `SHONEN.md`.

## 8. Verdict

- Round verdict per the lane: honest stop. Non-author verdict: **rejected-honest-stop** (admitted false; no axis harmed).
- Lane status for the ledger: `ok` (substantive report, real committed work).
