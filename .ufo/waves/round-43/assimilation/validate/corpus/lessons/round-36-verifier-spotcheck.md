# Round 36 verifier spot-check — mori (non-author)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-23
lane round: mori 36 (attempt 2); lane HEAD `4890c2d571c5275f6a5c214545f79e59e0f4afca`; report `.ufo/reports/round-36/mori.md` (fleet commit `1c7d0816`, author `mori-shokunin <mori@shokunin.local>`)

## Step-1 conformance

- Report committed by the lane identity: `git log --format='%an %ae %H' -- .ufo/reports/round-36/mori.md` → `mori-shokunin mori@shokunin.local 1c7d0816…` (plus two earlier lane-authored report commits; final is `1c7d081`). PASS.
- `SHONEN` heading present, one line per box, all `[~]` (author-asserted; no non-author `[x]` — lane-asserted marks count as `[~]` per PROTOCOL; not a promotion attestation). PASS as report contract.
- Every cited lane commit exists and is an ancestor of `master` (tested `git merge-base --is-ancestor <hash> master`): `da12b37 c1a026c 5842dc0 bf0df77 9ca8f2e 6827d6e 8ff9bba 5a2fe05d b7874b19 1caa2423 6bd57097 4890c2d5` — all PASS. Interloper commit `c081375` ("considerthese", operator personal) sits inside the round range; disclosed by the lane (LOG attribution anchors). Status-neutral defect, recorded.
- Lane state via `scripts/hyaku/jj-lane.sh state`: `branch=master local=4890c2d5… remote=4890c2d5… ahead=0 behind=0`. Pushed. PASS.
- Uncommitted path: `git status --porcelain` → `?? .scratch/` (one untracked dir). This is the named uncommitted lane path; it matches the disclosed operator-owned `.scratch/` item (report "Open L0 / carried operator items"). Left untouched; recorded as a defect.
- Dispatched prompt `.ufo/prompts/mori-round-36.md` carries the contract: report path (l.101), SHONEN heading requirement (l.118), commit-hash citation (l.107), L2 floor §3 (l.80-95), lowest-axis rule (l.15), commit-then-push via jj-lane helper (l.271-285), wave-policy + addendum §6 attempt inheritance (l.170). PASS.
- Watchdog digest (copied per closure duty): `2026-10-23T07:41:46-03:00 launch mori round=36 pgid=451829 driver=hyaku-inline attempt=1`; `2026-10-23T15:03:19-03:00 lane-dead-no-report mori round=36; retry same round (attempt=1 superseded at T0 2026-10-23T18:00Z: stale phase-4 author; fresh attempt)`; `2026-10-23T15:10:29-03:00 launch mori round=36 pgid=94896 driver=hyaku-inline attempt=2`; `2026-10-23T16:23:39-03:00 complete mori round=36; hyaku-inline attempt=2`.

## Per-claim re-check

### C2 — SOURCES append-only gate (measured; operability; capability acquisition)

- Before, re-measured: `python3 .ufo/waves/round-36/count-c2.py 6bd57097` → `tool_absent C2=unmet` exit 1 (observed this session; matches `evidence/c2-before.txt`).
- After, re-measured: `python3 .ufo/waves/round-36/count-c2.py bf0df77` → blind arm 24/24 sandbox histories match hidden truth; real arm pass, `appendonly_violations=18`, ids `[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193]`, `deleted=[]`, `superseded=[S069,S182,S193]`, `round_changed=[S182,S193]` — byte-identical to `evidence/c2-after.txt`; `C2=met`.
- Gate evidence verified (not executed): self-test tally `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0` (w2/ExecSelftests.md, with mutant arms showing the PASS lines discriminate); registry row present at registry home (SKILL.md Round36 table: gate kind, entry, verdict map, self-test, pinned values, write scope, owner); freeze pins verify — `git hash-object count-c2.py` = `d8c41d96…` == freeze-v3 pin; count-c1 `b5888afe…` == pin; contract.md `f505594b…` == the tip blob the report names. Re-scores at `8ff9bba`/`4890c2d5` (7 fresh draws + fixed seeds, independent oracle re-derivation by w2/RevC2Oracle) taken as committed evidence.
- Owned axis not harmed: SCORECARD diff `6bd57097..4890c2d5` appends only the Round-36 section + capability row; no axis score rewritten.
- Verdict: **improved**.

### C1 — source-drift byte probe (exploratory; freshness technique)

- Before, re-measured: `python3 .ufo/waves/round-36/count-c1.py 6bd57097` → `tool_absent C1=unmet` exit 1 (observed; matches `evidence/c1-before.txt`).
- After, evidence-verified (not re-executed; the real arm re-fetches live URLs): `evidence/c1-after.txt` and `c1-after-final.txt` — blind 40/40 mismatches=0; real arm `rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 mismatches=0`; live run `drift-live-r36.txt` `rows=220 fresh=49 drifted=9 unavailable=0 no-copy=162`. Post-sentinel hardening (4MiB read cap, post-redirect public-destination policy) committed at `1caa2423` with its own frozen-counter re-verification (seed 4886171876972216342).
- Reviewer of record ruling (this session is the named non-author reviewer): **unprovable-but-better**. Reasons: (1) the exploratory claim is bounded exactly — a byte-behavior predicate, never asserted as a freshness verdict, and the lane itself proved the bound (w1/CritAxisFit annotated-excerpt counterexample) and declared the claim exploratory *before* data at `5842dc0`; (2) everything checkable about the technique verifies — blind arm, live oracle agreement on 58 fetched rows, self-test 4/4 with mutation discrimination, and it survived 21 attack-seat FAILs whose repairs/hardening all landed; (3) the technique adds real, reusable ground — first whole-registry re-fetch with per-state classification, a dated nine-row enumeration carrying commands and open-time shas at four sites, reader-action classes (S210 post-copy asset rebuild, S211 fetch-varying page), mined into QUALITY 105; (4) residuals are disclosed with r37 repair paths, not waived. No axis harmed; SCORECARD records the row as exploratory with no score move.
- Verdict: **unprovable-but-better**.

## Trend verdicts

- **expansion: improved** — re-measured: unique `| S###` ids in `corpus/SOURCES.md` 204 (`6bd57097`) → 220 (`4890c2d5`); S205–S220 = 16 new rows as reported. Capability row present in SCORECARD (sources append-only gate, first working round 36). Knowledge entry `corpus/knowledge/source-drift-r36.md` cites mined S205. README Round-36 rows present.
- **quality: improved** — the seven→nine drift count repair is real: `drift-live-r36.txt` measures 9 drifted ids (S156–S160, S176–S177, S210); all four cited sites (knowledge note, QUALITY 105 addendum, SKILL Round36, README) carry the dated nine-row enumeration with commands and open-time shas (grep-verified). Freeze integrity: v3 pins verify byte-identical counters. S205 used-by corrected old→new and logged in the lesson Gate.
- **discernment: improved** — all 21 w2 FAILs are repaired in `9ca8f2e`/`6827d6e`/`8ff9bba`/`1caa2423` or disclosed as frozen-byte residuals with r37 paths (per-report; the disposition wording names each). The exploratory claim is reported `unprovable` with the reviewer condition named rather than self-attested. My independent spot-check below agrees with every sampled gate decision.

## Discernment spot-check (LEARNING.md — from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S206 (RFC 6585) — admit | admitted, mined | `https://www.rfc-editor.org/rfc/rfc6585.txt` §4 (fetched this session) | **agree** | Quote "too many requests in a given amount of time" verbatim at §4, 9 words ≤25; row teaches accurate; Standards Track April 2012 correct. |
| S212 (v7.2 stat.rst) — admit | admitted, mined | committed copy `corpus/evidence/sources-r36/S212.src` :21-22, :71-73 | **agree** | Source: "a single line of text containing 17 decimal values" (:21-22) and "standard UNIX 512-byte sectors" (:72); teaches sentence is a faithful ≤25-word paraphrase at its anchor; quote located. |
| S211 (PMC mirror of Nosek et al. 2018) — reject | rejected row | `corpus/SOURCES.md` rows S056 (:62) and S211 (:217) | **agree** | S056's source cell already carries the identical `pmc.ncbi.nlm.nih.gov/articles/PMC5856500/` URL; a mirror row would duplicate the URL without adding a recheck surface. Rejection-is-evidence rule satisfied. |

Census (closure step 3): `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0, `mori ok … corpus/SOURCES.md`, W04 duplicate-URL lines only (matches the report's census-end receipt, including the two new S218/S220 lines).

## Routed defects and notes for the lane (fix next round)

1. **Freeze-pointer slip (documentary)**: the report says "counter sha `c7edaacf…` == `evidence/freeze-v3.txt`", but those sha256 pins live in `evidence/freeze-v2.txt`; v3 pins git blob hashes (which verify exactly). Correct the pointer in the next round's report or a lesson addendum — append-only.
2. **Uncommitted lane path**: untracked `.scratch/` still present at closure (disclosed operator item; named here as the one uncommitted path).
3. **Partial wave settlement**: 62/66 w2 reports on disk, 4 seats never returned; disclosed honestly in the report with coverage by landed seats — keep the 4 items on the r37 verification list until superseded.
4. **Frozen-byte residuals** (disclosed, routed to r37): count-c2 SIGKILL of its own sandbox child on timeout; count-c1 docstring still says v1; counters do not detect SOURCES.md delete+restore inside a round; no 429/4xx oracle path exercised (`oracle_excluded=0`).
5. **w2 registry null agent ids** (lane-noted lesson from the orchestrator-inline handoff): record the actual seat ids in the r37 dispatch log if the inline path is used again.
6. **Operator items remain operator-owned** (not lane debt, restated per closure duty): LOG.md:1801 setting value, `refs/jj/keep 3b19cac`, `.scratch/`, SHONEN promotion review.
7. **SHONEN observation for the operator** (promotion is operator-owned, never written by this closure): all four SHONEN boxes now carry `[~]` evidence pointers that a non-author reviewer can execute from committed bytes (decision tables + registry rows; end-to-end round in dispatch-log + LOG; commands re-runnable; PROVINCE untouched). The boxes look checkable by a named non-author verifier whenever the operator schedules the promotion review.
8. Absolute operator paths in four evidence files (SentData LOW, disclosed) — fix-forward already routed by the lane to r37 hygiene.

Closure ruling basis: every declared claim verified by direct re-measurement (C2 before/after, census, row counts, freeze pins) or committed-evidence verification (C1, self-test tally, frozen re-scores); no owned axis harmed; exploratory claim ruled `unprovable-but-better` by the named non-author reviewer of record (this session) with reasons above.
