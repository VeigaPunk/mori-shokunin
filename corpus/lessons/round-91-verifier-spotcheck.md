# round-91 verifier spot-check — mori (hyaku closure, non-author)

author: hyaku closure (non-author integrator, @m_zfl)
Round: mori 91, honest stop. Entering `79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520`, landing
`bee9f21e18db79ca27493b1453a9543f1994d59f`. Report: `.ufo/reports/round-91/mori.md`
(fleet commit `db50dfb97b7c1afb10f76661f577505680c9be5e`, author `mori-shokunin <mori@shokunin.local>`).
This file is written by the closure judge, who did not author any round-91 work.

## Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | PASS — `git log --format='%an %H' -- .ufo/reports/round-91/mori.md` → `mori-shokunin <mori@shokunin.local> db50dfb9…` |
| `## SHONEN` heading, one line per box | PASS — 4 boxes, all `[~]` with pointers; no `[x]` written by the lane (correct: only a non-author may write `[x]`) |
| Cited lane commits exist and are ancestors of `master` | PASS — `git merge-base --is-ancestor e02b8a39 master` rc 0; `git merge-base --is-ancestor bee9f21e master` rc 0 (jj-colocated; tested against branch ref) |
| Lane pushed, no uncommitted round work | PASS — `jj-lane.sh state` → `branch=master local=bee9f21e… remote=bee9f21e… ahead=0 behind=0`; `git status --porcelain` empty |
| Prompt carries the template contract | PASS — mission/axes binding (§1), L2 floor ≥8 batched (§3), commit-then-push + push scope + L0 side channel (§5), report path (§4), `SHONEN` heading (§4), commit-hash citation (§4 evidence-pointer rule), lane write scope (§6: "write only inside …/mori-shokunin") |
| Dispatch evidence digest | PASS — `.ufo/watchdog.log` contains verbatim: `2026-11-05T02:12:15-03:00 launch mori round=91 pgid=1954018 driver=hyaku-inline attempt=1` and `2026-11-05T04:18:17-03:00 complete mori round=91; hyaku-inline attempt=1` |
| Marker predicate | Not a marker — real committed round work with checkable hashes (`e02b8a39`, `bee9f21e`) |

## Per-claim re-check (all measurements re-run by this judge at `bee9f21e` unless noted)

- **C1 — calibration (not admitted by lane). CONFIRMED not admitted.**
  Re-ran the candidate counter: `python3 -I .ufo/waves/round-91/w1/candidates/count-c1.py 79eaa8cf… --repo <lane> --scratch /tmp/mori91-vscratch` →
  `C1_SETUP p2 population absent: …/.ufo/waves/round-91/mutants-c1-independent.json`, exit 2 — reproduces the reported before-measurement.
  Absence at landing: `git ls-tree -r --name-only bee9f21e -- .ufo/waves/round-91/` lists no `mutants-c1-*` file (P1/P2 populations absent).
  The claimed improvement does not exist at `bee9f21e`; the lane's not-admitted verdict is correct.
- **C2 — freshness (not admitted by lane). CONFIRMED not admitted.**
  `git cat-file -e bee9f21e:corpus/evidence/value-census-2026-11-05.txt` → `fatal: path … does not exist in 'bee9f21e'` (absent; also absent at `79eaa8cf`).
  The claimed snapshot and counter seat never returned; the lane's not-admitted verdict is correct.
- **Digest-class instrument (landed work, not a claim). Re-measured.**
  `python3 -I tools/mori-source-digest.py corpus/SOURCES.md .ufo/waves/round-90/w1/Mo90S01Sources/sources/` at `bee9f21e` (read-only; tool writes nothing) →
  `DIGEST_CHECK rows=121 ok=87 mismatch=2 prefix_only=31 unpinned=1`, rc 1 — byte-identical to the reported line. Mismatches flagged: S235, S615, matching the lesson's C-1/C-2. `unpinned=1` is S125.
  Able-to-fail evidence (S490 one-character flip → `mismatch=3`, rc 1) verified from the committed receipt `.ufo/waves/round-91/evidence/controls-r91.txt` (evidence-verified, not re-executed — the flip run lives in a scratch copy by design).
- **Corrections of record C-1/C-2. Re-measured by this judge:**
  `sha256sum .ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` → `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` (= C-1 full digest; registry row recorded a corrupted variant).
  `sha256sum corpus/evidence/sources-r42/S235.pdf` → `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020` (= C-2 full digest).
  Registry rows are not rewritten (append-only rule); the supersession rows are correctly deferred to round 92 planning.
- **Registry census. Re-measured:** `git show 79eaa8cf…:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,}'` → 389; same at `bee9f21e` → 391. Matches the report.
- **Wave results. Re-measured:** `jq` over `.ufo/waves/round-91/w1-results.json` → 12 seats; exactly `Mo91E01Arms`, `Mo91E02Snap`, `Mo91M01Mut`, `Mo91K01Conn`, `Mo91C01Ctl` have zero-length output and null status — matches the report's dead-seat list.
- **No axis harmed.** `git diff 79eaa8cf bee9f21e -- SCORECARD.md` is additive only: the Round-91 honest-stop section, a capability row (`tools/mori-source-digest.py`), attack findings, planned round 92. No axis score moved; no existing row weakened. LOG.md carries the round-91 entries; knowledge entry and lesson carry their provenance.

## Per-axis verdicts (learning vocabulary)

| Axis | Verdict | Reason |
|---|---|---|
| calibration | unprovable | C1 never landed (populations absent; counter exit 2 re-confirmed); claimed arms not measurable |
| freshness | unprovable | C2 never landed (snapshot absent at both revisions, re-confirmed) |
| depth | unchanged | No score moved; digest gate detects R8/S235 but no depth claim declared or measured |
| coverage | unchanged | Registry +2 rows (new ground, admitted to expansion), no coverage-map claim |
| operability | unchanged | Digest tool runs (re-measured) but was not declared as the operability claim; nonce guard carried, not landed |
| adjacency | unchanged | No cross-domain evidence routed |

Round verdict: **rejected-honest-stop** — both declared claims verify only as `unprovable`, no axis harmed, real landed work (digest-class gate, 2 source rows, knowledge entry, lesson, corrections of record).

## Trend verdicts (closure, with own evidence)

- **expansion — improved.** 389 → 391 registry rows (re-measured); S617 `mined` and cited by `corpus/knowledge/calibration-arming-r91.md` (provenance trio checked: `source: S617`, `verified-at: 2026-11-05`, `recheck: 90d`); S618 rejected with reason and flip; census validate exit 0 after.
- **quality — improved.** Digest gate fails on R8/S235 at the entering registry and detects a one-character flip (committed receipt); C-1/C-2 corrections re-measured by this judge on the pinned bytes; no admitted entry failed a re-check; no axis harmed.
- **discernment — unchanged.** The lane's grade stands: attack seats found forgers the frozen predicates accept (C1 3/4, C2 6/10), a real calibration input for round 92, but no claim was admitted or measured this round, so calibrated discernment is unchanged. This judge's spot-check agreed with both sampled gate decisions (below), which supports at-least-not-harmed.

## Discernment spot-check (LEARNING.md; ≥1 admit + ≥1 reject, sources re-opened by this judge)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S617 Jia & Harman, TSE 2011 (mutation-testing survey) | admit (tier A, mined) | `https://web.eecs.umich.edu/~weimerw/2022-481F/readings/mutation-testing.pdf` — downloaded fresh: sha256 `056ac9b99410321c7cb80a29284c4ca106456e1a0cf64b6f4d633ba83edff342`, 1181976 bytes (both exact match); `pdftotext` → `grep -c -F 'Mutation Testing is a fault-based testing technique which provides a testing criterion'` = 1, located at raw line 21 | **agree** | Quote real and ≤25 words; canonical peer-reviewed survey (primary) for the mutation-adequacy scope; grounds the knowledge entry's kill/score definitions |
| S618 Google SRE book ch. 6 (Monitoring Distributed Systems) | reject (tier A kept) | `https://sre.google/sre-book/monitoring-distributed-systems/` — fetched fresh: sha256 `3117d94aca6d7422db18b210a4142718388523a4ea2082df539ffe9a8c4c2a75`, 73467 bytes (both exact match); `grep -c -F 'Observational experiments conducted over a very long time horizon'` = 1 | **agree** | Quote real; the chapter gives sampling-cadence guidance for long horizons, not a dated-snapshot/drift/freshness test — the rejection reason is sound and the flip condition is recorded in the row |

Both newly written `corpus/SOURCES.md` rows re-opened (≥1 required). Census validator:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, exit 0
(41 `W04` warning lines; the one new is the S618 duplicate-url warning — a warning, not an error).

## Routed defects (the lane must fix next round; status-neutral)

1. **R-D1 (mori r92):** S615/S235 recorded digests in `corpus/SOURCES.md` are corrupted (mismatch re-confirmed by the digest gate at `bee9f21e`); corrections of record C-1/C-2 are in the lesson, but the registry repair must be appended supersession rows per CORPUS rule 2, never an in-place rewrite. Already in SCORECARD planned round 92 item 5 — keep it.
2. **R-D2 (mori r92):** S156, S158, S159 digest mismatches against id-named copies (C-3) remain unclassified; classify with the same gate next round.
3. **R-D3 (operator/L0):** five of twelve wave seats (`Mo91E01Arms`, `Mo91E02Snap`, `Mo91M01Mut`, `Mo91K01Conn`, `Mo91C01Ctl`) returned empty output with null status/note; the spawn/stop reason is unrecorded per seat. The lane filed the L0 question; this is an orchestrator-side defect, not lane debt.
4. **R-D4 (mori r92):** in-scope registry carries 31 `prefix-only` digest records and 1 `unpinned` (S125) surfaced by the new gate — decide (round-92 planned item 5) whether the census absorbs the gate and backfills full digests.

## Notes for the operator

- All four SHONEN boxes are asserted `[~]` with resolvable pointers and look fully checkable by a
  non-author (SKILL.md tables unchanged and present; end-to-end digest check logged; tool usage
  executable without oral context; no cross-domain bleed observed). Promotion review is
  operator-owned; this judge did not write any `[x]`.
- The digest gate self-test/re-derivation duty (Gate standard: self-test over fixtures with
  committed expected values) is not yet present for `tools/mori-source-digest.py`; the registry
  row for it lives in SCORECARD `## Round 91` but a SKILL.md registry row is owed before closure
  grades any gate conformant. Not a round-91 failure — the instrument is detection evidence this
  round, not a claimed gate verdict.
