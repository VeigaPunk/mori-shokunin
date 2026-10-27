# mori-shokunin — Scorecard

Axes owned by this lane: **coverage + operability** (fleet-2); all six are scored
here, the owned pair drives the round's axis-move.

## Axes

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| coverage | 6 | per-surface notes landed (`corpus/knowledge/observability-surfaces-r2.md`); silence roster over the declared lanes (round 12, score 5 → 6 then); one-shot system pressure read (round 24); round-24 closure "Score 6 → 6" (`corpus/lessons/round-24-verifier-spotcheck.md:88`); round-26 closure grades coverage improved and states no new number (`corpus/lessons/round-26-verifier-spotcheck.md:133`); latest admitted closure grades coverage improved (FR13 held as a full event set plus lifecycle) and states no new number (`corpus/lessons/round-47-verifier-spotcheck.md:68`) | round 47 (improved, score held); round 26 (improved, score held) before the round-50 correction |
| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); 7 was first set in round 13's table (6 → 7), which closed rejected-harmed; first held in round 14's admitted table and kept since (round 14's closure grades operability unchanged and states the scores, `corpus/lessons/round-14-verifier-spotcheck.md:87`); round-28 closure grades operability improved (ten A2 rules pinned by 30 frozen cases) (`corpus/lessons/round-28-verifier-spotcheck.md:93`); round-31 closure grades operability improved (blind-writer gate `tools/mori-blind-check.sh`, C2 verified) and states the score stays 7 (`corpus/lessons/round-31-verifier-spotcheck.md:155`); round-35 correction: this cell said round 28; round-37 C2 verified the probe's hardening as named, mutation-killable arms and re-attributed that claim here (SCORECARD round-37 post-data correction; round-38 axes-cell correction); latest admitted closure grades operability improved (new reconciler `tools/mori-pin-check.py`, evidence-verified) and states no new number (`corpus/lessons/round-47-verifier-spotcheck.md:67`); round-51 closure grades operability improved (C1: a `--rev` pin re-execution is hermetic and classes mismatches) and states the score 7 (`corpus/lessons/round-51-verifier-spotcheck.md:130`) | round 51 (improved, score held); round 47 (improved, score held); round 31 (improved, score held) before the round-50 correction; round-37 C2 re-attributed here (score held, 7) |
| depth | 5 | source-linked knowledge entries with `source:`/`verified-at:`/`recheck:` lines (round 12 claim 1); the round-12 closure states the move (`corpus/lessons/round-12-verifier-spotcheck.md:17`); round-31 closure grades depth improved (watchdog identity decision table, C1 re-measured) and states the score stays 5 (`corpus/lessons/round-31-verifier-spotcheck.md:154`); round 27's depth improvement was verified under a rejected-honest-stop closure and is not counted; round-35 correction: this cell said round 12 (4 → 5), the last score move; latest admitted closure grades depth improved (C2 re-measured 21/21) and states the score 5 (`corpus/lessons/round-49-verifier-spotcheck.md:76`); round-50 closure grades depth improved (C2 re-measured 22/22) and states no score change (`corpus/lessons/round-50-verifier-spotcheck.md:126`); round-51 closure grades depth improved (C2 re-measured 21/21, the MemAvailable entry) and states the score 5 (`corpus/lessons/round-51-verifier-spotcheck.md:131`) | round 51 (improved, score held); round 50 (improved, score held); round 49 (improved, score held); round 31 (improved, score held) before the round-50 correction |
| freshness | 5 | round-10 drift pin still red; the round-20 re-pin was rejected (`corpus/README.md` Round21 correction); latest admitted closure grades freshness improved and states no new number (`corpus/lessons/round-28-verifier-spotcheck.md:92`); round 28's measured outcome proposed 5 → 6 (`SCORECARD.md:1781`), not adopted because no closure states it; the score itself is stated at `corpus/lessons/round-14-verifier-spotcheck.md:87` | round 28 (improved, score held); round-37 C2 is re-attributed to operability (round-38 axes-cell correction below) and round 38 claims no freshness move |
| calibration | 5 | round 12's self-assessed 5 → 6 was not re-derived by the outside reviewer and held at 5; round-24 closure "Score 5 → 5" (`corpus/lessons/round-24-verifier-spotcheck.md:68`); round-25 closure grades calibration improved and states no new number (`corpus/lessons/round-25-verifier-spotcheck.md:124`); latest admitted closure grades calibration improved (C1 verified, no score change claimed) and states the score 5 (`corpus/lessons/round-49-verifier-spotcheck.md:75`); round-50 closure grades calibration improved (C1 verified, no score change claimed) (`corpus/lessons/round-50-verifier-spotcheck.md:125`) | round 50 (improved, score held); round 49 (improved, score held); round 25 (improved, score held) before the round-50 correction; round-37 claim C1 closed the r36 measurement-discrimination defect and states no new number |
| adjacency | 6 | refuses dispatch (kumitate), OS state (tsukuroi) and harness configuration (operator) in PROVINCE and in its tools; score stated at `corpus/lessons/round-14-verifier-spotcheck.md:87`; latest admitted closure grading adjacency improved has no lane spot-check file: MANIFEST.json@63729047 mori round 19 (fleet MANIFEST.json rounds[398], verdicts.adjacency improved) | round 19 (improved, score held) |

Round-25 correction (C1 item D5): until round 25 this table still showed the round-1 scores (coverage 5,
operability 6, depth 4) with "round 1" in every row, while the round tables below held 6, 7 and 5. The scores
above are the ones the closure-admitted round-24 section records (`SCORECARD.md:1499-1506` at `28b79d3d`).

Round-50 correction (C1, calibration): the Last change cells of coverage, operability, depth and calibration named
rounds 26, 31, 31 and 25 while the fleet `MANIFEST.json` at `e014499613f63f8a467821219b0296121119ca53` records the
latest admitted mori round grading each axis improved as 47, 47, 49 and 49; the cells had skipped admitted
improvements in coverage (47), operability (36, 37, 38, 39, 41, 43, 44, 47), depth (38, 39, 41, 44, 47, 48, 49) and
calibration (37, 38, 39, 41, 43, 44, 46, 47, 48, 49) (`.ufo/waves/round-50/a2w1/Mo50bScribeMistakes.md` §3 item 2).
Each cell now leads with the latest round and keeps the older history after a `;`; scores are unchanged because no
closure states a new number. "Last change" here means the latest admitted closure grading the axis improved or
harmed, not the latest score move (a named limit of this convention:
`.ufo/waves/round-50/a2w1/Mo50bCritAxesSemantics.md`). Checked by `python3 .ufo/waves/round-50/count-c1.py <rev>`.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 1 | coverage + operability | no gate, empty corpus | `tools/mori-census.sh` landed; `--selftest` 14/14 PASS; live `MORI_CENSUS: DRIFT (findings=10 drift=9 unavailable=0 surfaces=7)` exit 1 | `corpus/knowledge/observability-census-r1.md` |

## Planned

Round 2: land one note per surface family and the first watch receipts, and add the
`progressing-weak` authorship proof.

## Retired

None.

## Round 2 — interactive cutover attempt (blocked, not completed)

The fleet's read-only `MANIFEST.json` round-1 closure records mori `ok` at
`7ca17b1`; the current lane baseline is
`0715198ed683445768944cec2db75bce12a1d202`. **Verified lane rounds remain 1.**
The old driver's launch counter 2 is not a second verified round. This attempt
does not change the legacy scalar scores above or claim native judgment.

The following plan supersedes the broad round-2 paragraph under **Planned**:
one coverage move, launch-aware and authorship-aware silence grading. Coverage
is the lower owned LIVE axis; operability remains LIVE. Other axes are observed
for regression, not selected by their legacy numbers.

| Axis | State | Attempt verdict | Evidence / limitation |
|---|---|---|---|
| coverage | LIVE — selected | unchanged | `probe_silence` remains the rolling-window implementation; no production cutover admitted |
| operability | LIVE | unchanged | baseline selftest PASS 14/14 exit 0; inherited round-2 driver exits 1 before any case verdict |
| depth | observed | unchanged | inherited silence note preserved as a candidate, not admitted domain knowledge |
| freshness | observed | unchanged | current CLI re-measured; no new drift detector or frozen behavioral baseline landed |
| calibration | observed | unchanged | route/fixture limits recorded; no outside admit/reject spot-check or promotion attestation |
| adjacency | observed | unchanged | detection/report boundary preserved; routing/host remediation remains outside lane scope |

| Learning trend | Attempt verdict | Evidence / limitation |
|---|---|---|
| expansion | unchanged | no new knowledge entry admitted |
| quality | unchanged | candidate note and harness withheld rather than represented as a verified cutover |
| discernment | unchanged | genuinely outside spot-check absent; L1 decisions are not outside verification |

Re-measured commands at baseline script SHA-256
`e3073a2b5e89bf717c1955e7a3d7bd995bf1096d61b6887af98b4517ee92f3f2`:

- `bash tools/mori-census.sh --selftest`:
  `MORI_CENSUS_SELFTEST: PASS (14 cases, 14 passed, 0 failed)` exit 0.
- `env MORI_ROSTER_LANES=mori MORI_LANE_SILENCE_S=900 bash tools/mori-census.sh`:
  `MORI_CENSUS: DRIFT (findings=14 drift=11 unavailable=0 surfaces=7)` exit 1.
  Mutable live observation, not a causal before/after comparison.
- `bash tools/mori-silence-cases.sh`: exit 1 during fixture setup; no
  `MORI_SILENCE_CASES` line, so no scenario tally is claimed.

Full argv, times, stdout/stderr and exit codes:
`.ufo/round-2/interactive-cutover/checks/`. WWKD plan, inherited byte snapshots
and route evidence are under the same root. Canonical wave `plan
--route-families` validates 32 distinct scopes, exit 0, but its routes are
unprobed and do not satisfy the operator's role bindings. **Dispatched: 0.**

Named debt and concrete unblock:

1. **Role routing:** existing content roles must bind `@m_composer`, audit
   roles `@m_grok`, connector `@m_antigravity` with `@m_zfl` fallback. Actual
   used roles resolve to `@m_mid` / `@m_strong` / `@m_fast`. Operator/integrator
   supplies an already authorized binding surface; mori does not change config.
2. **Candidate harness:** reconcile fixture Git setup at
   `tools/mori-silence-cases.sh:188-215`, real versus synthetic timeline grammar,
   and report-path assumptions before using it as a behavioral oracle.
3. **Admission:** after routing is supplied, a fresh round-2 L1 revalidates and
   dispatches one complete rendered 32-seat batch, integrates one coverage move,
   runs acceptance and records outside spot-check status.
4. **Receipt:** directly launched Sighting metadata has no authoritative task
   key/expected receipt bag. Integrator supplies that binding before an
   applicable receipt is minted/validated or the mission is completed.

This is one blocked attempt, not three blocked rounds and not saturation.
Next actual round remains **2**; the operator's minimum 100 verified-round goal
is unchanged. No shared ledger or historical report was rewritten.

## Round 2 verdict — 2026-10-15 (goal wave; the blocked attempt above remains the prior record)

Selected axis: **coverage** (the lower owned LIVE axis; operability live). One
falsifiable claim: before — `bash tools/mori-silence-cases.sh` exits 1 in
fixture setup with no `MORI_SILENCE_CASES` tally, no per-surface notes exist,
no watch receipts, `progressing-weak` unproven; after — the harness runs
end-to-end emitting an honest tally, seven per-surface notes + first dated watch
receipts land under `corpus/`, and the authorship proof is landed or explicitly
deferred with named precondition. Wave: one batched 13-seat flash call; report
`.ufo/reports/round-2/mori-goalwave.md`; integration commit under the mori lane
identity; acceptance re-run by the parent.

| axis | verdict | before → after evidence |
|---|---|---|
| coverage | **improved** | Before `e30b2e3`: exit 1 in fixture setup, no tally (blocked-attempt records). After: `bash tools/mori-silence-cases.sh` (sha `505a7504…`) → all 27 cases run, `MORI_SILENCE_CASES: matched=10 total=27`, exit 1, two reruns byte-identical; seven per-surface sections: `grep -cE '^## [1-7]\.' corpus/knowledge/observability-surfaces-r2.md` → 7; receipts `corpus/evidence/watch-r2-20261015T15{2746,2855,3003}Z.log` + index; authorship check `MORI_AUTHORSHIP_CHECK: matched=10 total=10` exit 0 (extract sha `9c91e0a0…`). The 17 FAILs = 16 r2-contract gap vs the still-r1 census + 1 measured r1 defect (`tools/mori-census.sh:517` pipefail crash) — reported as-is, not weakened. |
| operability | **improved** | Harness now operational end-to-end with exit-code contract (0 all-pass / 1 case-failures + tally / 2 setup+diagnostic); before: exit 1 with no diagnostic and no tally. Census `bash tools/mori-census.sh --selftest` → `PASS (14 cases, 14 passed, 0 failed)` exit 0 both before and after (census sha `e3073a2b…` unchanged). |
| depth | **improved** | Root-cause mechanism pinned and independently reproduced by two seats (`(A||B)&&C` precedence + `--allow-empty` empty root commit; `core.autocrlf` typo in the dead branch); census `:517` pipefail crash isolated with minimal chmod-000 repro; six census defects with path:line in the surfaces note. |
| freshness | **improved narrowly** | Three dated, hash-pinned, re-runnable watch receipts + index README; method limitation stated (repeated spaced censuses — the census has no watch mode); a drift pin is still absent, disclosed. |
| calibration | **improved narrowly** | Every grading rule labeled `proven`/`proposed` with named preconditions (`silence-grading-r2.md`); expected gradient pre-registered and mutant-census probes executed (falsifier/critic seats — no-op → `matched=1`, all-zero → `matched=4`, mutator → caught); byte-defective identity recipe (missing `>`) caught and fixed at integration. No threshold tuning claimed. |
| adjacency | **unchanged** | Scope-sentinel: zero remediation/kill/config content in any artifact; fleet root read-only for all seats; out-of-province findings (unit failures, parent-slice OOM counter) reported, not absorbed. |

Admission: five axes improved, adjacency unchanged, **none harmed → ADMIT**. No
scalar score. Learning trends: expansion **improved** (three knowledge notes +
one lesson), quality **improved** (honest failure counting; defects at path:line;
receipt hashes verified), discernment **unchanged** (no outside spot-check — the
wave's seats are the lane per protocol).

SHONEN (all four remain `[ ]`: no named non-author verifier yet; wave seats are
the lane): [ ] decision tables · [ ] end-to-end task logged · [ ] executable
without oral context · [ ] no cross-domain bleed.

Named debt for round 3: the r2 `probe_silence` census cutover (preconditions in
`corpus/knowledge/silence-grading-r2.md`; passing tally `matched=N total=M,
N=M` registered as the claim), the census `:517` (and `:283`) pipefail crash →
`unavailable` semantics, and the frozen-behavioral drift pin.

## Round 3 verdict — 2026-10-15 (goal wave; evidence commit `1439c47`)

Selected axis: **coverage** — the registered round-2 debt (above): land the r2
`probe_silence` in `tools/mori-census.sh` implementing the
`corpus/knowledge/silence-grading-r2.md` contract, harden `:517`/`:283`, add
selftest cases, re-baseline the frozen oracle per-case, never branch on
`MORI_FIXTURE`/fixture paths. Wave: one 32-seat flash AgentSwarm call (24
completed; 8 seats lost to a provider content-filter false positive —
alibaba-token-plan `data_inspection_failed` — and re-dispatched as an 8-seat
backfill, 8/8 completed; the cascade shim was fixed to fall through that class
of 400). Report: `.ufo/reports/round-3/mori-goalwave.md`.

**Before** (r1 census `e3073a2b…`; receipt
`corpus/evidence/cutover-r3-20261015T164140Z-before.log`): oracle `matched=10
total=27` exit 1 (16 contract gaps + 1 crash); selftest 14/14; live
aggregate-only silence row with 7 × `LANE_SILENT` (`head_epoch=`/`newest_epoch=`);
`:283` crash repro header-only.

**After** (r2 census `fe22a14f…`, `VERSION=census-r2`; receipts
`cutover-r3-20261015T165712Z-{selftest,oracle,live,oracle-counterfactual}.log`;
parent acceptance re-run 2026-10-15T17:24Z, all matching the receipts): selftest
`PASS (25 cases, 25 passed, 0 failed)` exit 0; oracle `matched=25 total=27`
exit 1 — 15 FAIL→PASS, 10 held; the 2 residual FAILs
(`ledger-missing-not-silent`, `report-future-no-close`) are the **frozen
oracle's matcher defect** — `case "$obs" in $want)` takes the expansion-introduced
`|` literally (`tools/mori-silence-cases.sh:362-365`); the observed states sit
inside the intended want-sets, proven by the counterfactual one-block matcher
patch: `matched=27 total=27` exit 0, independently reproduced byte-identical
(scratch sha `ae95b601…`) by four seats; live census r2: 9/9 per-lane rows all
`progressing` (8 × `row-A`; aggregator `row-B` with `attribution=inference`),
`SURFACE silence: ok (silent=0 progressing=9 …)`, zero `LANE_SILENT`,
`MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` (parent
run; receipt had findings=14 — the +1 is a mutable `SEGFAULT_JOURNAL` info
count; the 1 unavailable is tmux, never DRIFT).

| axis | verdict | before → after evidence |
|---|---|---|
| coverage | **improved** | r1 rolling mtime window, no launch/closure/authorship → every spec element implemented (26-row spec map, `silence-cutover-r3.md` §1, all rows `implemented`/`verified`); per-lane rows with the six states on the live fleet; 15 of 17 oracle fails flipped with per-case justification (§5). The literal `N=M` is arithmetically unattainable under the frozen matcher (max 25/27) — reported as-is; 27/27 proven at identical census bytes via the counterfactual. |
| operability | **improved** | census crash on unreadable repos (rc 1, no verdict) → `:517` construct deleted and `:283` rc-gated (`age_unreadable=`); `unreadable-git-unavailable` now grades `unavailable` with a full verdict; selftest 14 → 25; live census runs to a full verdict; perf ~5.7× faster live with linear parser scaling (perf seat, median of 3). Residual named: `:227` `state_n` is the same bare-pipeline shape (critic re-measured the crash) — carried to round 4. |
| depth | **improved** | `silence-cutover-r3.md` maps every spec row to file:line with seven named divergences D-a–D-g (none affects findings/DRIFT); the crash class pinned as a lesson with canaries (`corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`); closure predicate verified branch-by-branch (13 fixture cases incl. ct==NOW inclusive, ct==launch strict, closure-over-authorship precedence, relaunch reopening). |
| freshness | **improved narrowly** | five dated, hash-pinned receipts at the new SHA (before/selftest/oracle/live/counterfactual), indexed with re-run recipes (`corpus/evidence/README.md:110-173`); drift pin still absent — carried debt. |
| calibration | **improved** | strict age gate proven at the equality boundary; `LANE_SILENT` fires only for row D across every probe (critic's adversarial fixtures included); `unavailable` not over-broad (empty repo + old launch → `silent`, not `unavailable`); no fixture branching in the silence path (26/26 differential fixture probes byte-identical; zero `MORI_FIXTURE` refs in `:503-845`); mutant censuses grade honestly (no-op → `matched=1`, all-zero → `matched=4`) — with the disclosed caveat that a no-logic case-id *sniffer* can fake a tally, which is why the honesty case rests on source + differential evidence (named round-4 hardening). |
| adjacency | **unchanged** | scope-sentinel: detection/report only; frozen oracle byte-unchanged; fleet root read-only for seats; out-of-province observations (other surfaces' findings, `:227`) reported, not absorbed. |

Admission: five axes improved, adjacency unchanged, **none harmed → ADMIT**.
No scalar score. Learning trends: expansion **improved** (cutover note, lesson,
SKILL r2 contract section, receipt index, README updates); quality **improved**
(honest 25/27; matcher defect diagnosed by a bash-semantics probe + patch +
counterfactual, not asserted; per-case justification for all 27); discernment
**unchanged** (no outside spot-check; the counterfactual is a same-wave
experiment).

Named debt for round 4 (registered claim): the frozen-oracle matcher fix (one
block; witness `ae95b601…`) **plus** oracle anti-sniff hardening (opaque per-case
dirs, stop exporting `MORI_FIXTURE`, shape-invariance case — per the falsifier
seat) **plus** the census `:227` pipefail hardening and the critic's per-round
close-tracking fix; end-goal: `MORI_SILENCE_CASES: matched=27 total=27` exit 0
at pinned oracle+census SHAs, selftest green, live census honest. Carried
unchanged: the drift pin, the row-6 presence-only residual, the receipt-binding
and role-routing debts from the blocked attempt.

## Round 4 verdict — 2026-10-15 (goal wave; evidence commit `5b62c897`)

Selected axis: **operability** — the registered round-3 debt: make the verdict
machine trustworthy end-to-end (oracle matcher, fixture-signal leak, census
`:227` crash, per-round close tracking). Wave: one 32-seat flash AgentSwarm
call, 32/32 completed (the cascade content-filter fix held — zero dispatch
losses). Report: `.ufo/reports/round-4/mori-goalwave.md`.

**Before** (oracle `505a7504…`, census `fe22a14f…`): oracle capped at
`matched=25 total=27` by its own matcher (`case "$obs" in $want)` literal `|`);
case-id-sniffer census faked `27/27` exit 0 via fixture-path signal; `:227`
chmod-000 `.ufo/state` crashed the whole census (rc 1, header only, 0
verdicts); `complete r7; complete r5` misgraded a closed r7 anchor.

**After** (oracle `be0e28b8…` — matcher `want_match` exact-string alternation,
opaque `mktemp -d` per-case dirs, no `MORI_FIXTURE` export, new case 28
`shape-invariance`; census `af2d4e79…` — `:227` rc-gated, per-anchor-round
close tracking, selftest 25 → 30; parent acceptance 2026-10-15T17:55Z):
selftest `PASS (30 cases, 30 passed, 0 failed)` exit 0; oracle
`matched=28 total=28` exit 0, ×2 byte-identical (parent runs), all 27
pre-registered ids PASS + shape-invariance; live census honest
(`DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`, 9/9 lanes
progressing, 0 `LANE_SILENT`); sniffers: case-id channel closed (v1
reconstruction scores 1–2/28), path-shape sniffer caught at 27/28 by the
shape-invariance case.

| axis | verdict | before → after evidence |
|---|---|---|
| operability | **improved** | matcher defect (25/27 cap) → `want_match` alternation-safe, 28/28 at pinned SHAs ×3 deterministic; `:227` crash → rc-gated + 3 new selftest cases; close-anywhere → per-anchor-round tracking + 2 new cases (12 monotone + adversarial close sequences held); selftest 25 → 30; full regression batteries green (young/not-open, unavailable, root-lane, exit-contract, waves-hardening, close-reopen, journal arm untouched). |
| coverage | **unchanged** | No new measured domain surface; the case registry grew by exactly the disclosed shape-invariance case (28 total). |
| depth | **improved** | `corpus/knowledge/verdict-machine-r4.md`: matcher mechanism (bash case-pattern semantics), the three sniffer channels and what closed them, `:227` and close-tracking fixes, canaries; lesson `corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md`. |
| freshness | **unchanged** | five r4 receipts (`verdict-r4-20261015T173551Z-*.log`) at the new SHAs; drift pin still absent — carried. |
| calibration | **improved narrowly** | attack-class measurements now receipt-backed: sniffer v1/v2 logs, canary-227 before/after; the honest scoping correction below. |
| adjacency | **unchanged** | scope-sentinel clean; fixtures `/tmp` only; fleet root read-only; no remediation content. |

**Correction folded same-round (honest scoping):** the claim's clause "a
sniffer-v2 attempt cannot fake a pass" is **true only for the case-id/path
channel**. A run-order sniffer (canned grades keyed on deterministic invocation
order, no fixture bytes read) still reaches `matched=28 total=28` exit 0
(critic's sniffer-v3, reproduced by the admission seat). The channel and its
unblock (per-run case-order shuffle / run nonce) are named in
`verdict-machine-r4.md` and registered as round 5's claim. ADMIT-with-correction:
five-axis read — operability/depth/calibration improved, coverage/freshness/
adjacency unchanged, **none harmed → ADMIT**. No scalar score. Learning trends:
expansion/quality **improved**, discernment **unchanged** (same-wave
verification only).

## Round 5 verdict — 2026-10-15 (goal wave; evidence commit `a420deb7`)

Selected axis: **operability** — close the run-order spoofing channel (the
round-4 correction's named residual). Wave: one 32-seat flash call, 32/32.
Report: `.ufo/reports/round-5/mori-goalwave.md`.

**Before** (oracle `be0e28b8…`): fixed registry case order, no per-run secret —
a zero-logic census counting its own invocations replayed canned grades for
`matched=28 total=28` exit 0 (sniffer-v3 class, reproduced at r4 bytes by five
seats).

**After** (oracle `7143ccc2…`: seeded Fisher–Yates case order (xorshift32;
`SHUFFLE_SEED`/`CASE_ORDER` logged; seed never exported to the census;
`MORI_SHUFFLE_SEED` pins for repro) + per-run `RUN_NONCE` delivered three ways
(env, fixture file, and the disk-target dir name `nonce-<N>` which the frozen
census echoes in its disk row; every case requires the literal token —
stale/missing fails as `canned/replayed output?`); census `af2d4e79…` frozen;
parent acceptance 2026-10-15T18:30Z: selftest `PASS (30 cases…)` exit 0; oracle
`matched=28 total=28` exit 0 across runs with **different orders** (parent seeds
3335873357 / 1612830277); attack battery all exit 1 (invocation-count canned
`0/28`, stale-nonce `0/28`, adaptive positional `8/28`, env-reading v4 `10/28`);
grade tuples byte-identical across shuffles; order-pair probes (4 groups) show
no inter-case state leakage; live census honest.

**Correction folded same-round:** "zero-logic cannot fake" holds for the four
enumerated classes; two residuals remain, reproduced at `7143ccc2`: (R1)
**stdout-backchannel** — the census reads `CASE_ORDER`/`RUN_NONCE` from the
oracle's own stdout via `/proc/<ppid>/fd/1` (or `environ` on pinned runs) and
replays by position → 28/28 exit 0 (fix direction: print the run header AFTER
the case loop); (R2) **content-keyed forgery** — a memorized content→state
table still passes because the nonce binds no fixture content (fix: embed the
nonce in fixture content). Both named in `verdict-machine-r5.md`, registered as
round 6's claim.

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | fixed-order/no-secret execution → seeded shuffle + triple-channel nonce; four attack classes closed with receipt-backed tallies (`order-r5-20261015T180431Z-sniffer.log`); cross-shuffle grade stability + in-run determinism proven; registry byte-identical (28 ids/wants). |
| coverage | **unchanged** | registry unchanged; no new measured surface. |
| depth | **improved** | `corpus/knowledge/verdict-machine-r5.md` (design, seed contract, R1/R2 mechanisms); lesson `corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`. |
| freshness | **unchanged** | six r5 receipts at pinned SHAs incl. per-run seeds/orders; drift pin still carried. |
| calibration | **improved narrowly** | attack classes enumerated, tested, honestly scoped; residuals named with repro SHAs, not dropped. |
| adjacency | **unchanged** | scope-sentinel clean; census frozen and verified unchanged; no remediation content. |

Admission: ADMIT-with-correction (R1/R2 named, none harmed). No scalar score.
Learning trends: expansion/quality **improved**, discernment **unchanged**.

## Round 6 verdict — 2026-10-15 (goal wave; evidence commit `92b2e42`)

Selected axis: **operability** — close the round-5 residuals R1 (stdout
backchannel) and R2 (content-keyed forgery). Wave: one 32-seat flash call,
33/33 reports. Report: `.ufo/reports/round-6/mori-goalwave.md`.

**Before** (`7143ccc2…`): run header printed secrets before the case loop —
a census reading `/proc/<ppid>/fd/1` replayed by position for 28/28 exit 0
(R1); fixture content was nonce-free and run-invariant — memorized
content→state tables passed (R2).

**After** (oracle `3307761a…`: header moved after the case loop — parent
acceptance shows `SHUFFLE_SEED` at line 29 of 32, after all case lines;
`redact()` strips the token from echoed fragments; pinned-seed re-exec drops
env pins before any census exists (environ/fd probe 29/29 zero hits vs r5
positive control 2/1); R2: per-run `RUN_SALT_HEX` in every committed body +
random `blob-*` payloads outside graded trees; registry (28 ids/wants)
byte-identical; census `af2d4e79…` frozen). Parent acceptance 2026-10-15T19:20Z:
selftest 30/30 exit 0; oracle 28/28 exit 0 ×2 byte-identical, distinct orders;
live census honest (`DRIFT findings=15 drift=14 unavailable=1`); R1 attacker
0–1/28 (the 1 is shape-invariance self-agreement, not a grading pass); R2
memorizer fails at the salt-discriminating cases.

**Corrections / boundaries named (not claimed away):** (a) the impl iterated
mid-wave (`7143ccc2` → `9ce164ec` → `3307761a`) — at the first revision the
claim did NOT hold (R1 attacker still read the header); the re-exec revision
closed it, and the admission battery pins the FINAL bytes only; (b) residual
class: a **full-grammar normalizer** (strips nonce/salt shapes AND excludes
`salt-*`/`blob-*` names from its keys) still memorizes 28/28 — the honest
boundary: finite fixtures + deterministic grades are memorizable in principle;
anti-forgery here is depth, not impossibility (`verdict-machine-r6.md`); (c)
operator-invocation hygiene: a surviving ANCESTOR's environ can still carry
`MORI_SHUFFLE_SEED` — outside the oracle's control, named.

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | fd/environ backchannel → header-after-loop + re-exec scrub (probe 0 hits); content memorization → per-run salt + random blobs (memorizer caught); 28/28 honest held ×10 (impl) ×2 (parent). |
| coverage | **unchanged** | registry byte-identical. |
| depth | **improved** | `corpus/knowledge/verdict-machine-r6.md`; lesson `corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`. |
| freshness | **unchanged** | seven r6 receipts at pinned SHAs; drift pin carried. |
| calibration | **improved narrowly** | the mid-wave revision history admitted; the normalizer-class boundary measured (not asserted); attacker tallies receipt-backed (`backchannel-r6-20261015T191216Z-attack-r1/r2.log`). |
| adjacency | **unchanged** | scope-sentinel clean; census frozen and diff-verified; no remediation content. |

Admission: ADMIT-with-correction (normalizer-class boundary + ancestor-pin
caveat named; none harmed). No scalar score. Learning trends:
expansion/quality **improved**, discernment **unchanged**. The verdict-machine
arc (r3–r6) is complete: the oracle+census pair is now hardened against six
attack classes with two honest boundary classes named. Round 7 pivots to
**coverage**: the surface gaps measured in round 2 (`observability-surfaces-r2.md`:
tmux session relevance, memory-pressure threshold, disk write-rate,
`state_rounds` count-only) — registered as the round-7 claim.

## Round 7 verdict — 2026-10-15 (goal wave; evidence commit `d30b4e4`)

Selected axis: **coverage** — the round-2 pivot: close the four measured
surface gaps. Wave: one 31-seat flash call, 31/31. Report:
`.ufo/reports/round-7/mori-goalwave.md`.

**Before** (census `af2d4e79…`, selftest 30): tmux counted but never
classified; memory pressure never measured; disk rows point-in-time only;
`state_rounds` counted files, never read values (all receipt-backed in
`observability-surfaces-r2.md`).

**After** (census r4 `c7c3569b…`, oracle rebased `448f7723…`; parent
acceptance 2026-10-15T20:10Z): selftest `PASS (45 cases, 45 passed, 0 failed)`
(+15, none removed/renamed); oracle `matched=28 total=28` exit 0 ×2 at the new
SHAs (re-baseline additive-only — every case's state/finding/rc semantics
unchanged); live census shows all four new probes: `SURFACE tmux …
rule=pane_cwd_under_fleet_root` (unavailable rc=1 handled when no server),
cgroup row with `psi_some_avg10=/psi_full_avg10=/mem_fill_pct=/local_oom_kill=`,
disk row with `io_basis=since-boot io_avg_since_boot=dm-0:9433966Bps/12427s`
+ honest `io_avg_unavailable=tmpfs:not-a-block-device`, watchdog row with
`state_rounds_max=/state_lag=/state_ahead=/state_cmp=` and info findings
`WATCHDOG_STATE_LAG`/`WATCHDOG_STATE_AHEAD`.

Gap dispositions: **tmux relevance** — implemented (pane-cwd-under-fleet-root
rule, `TMUX_FOREIGN_SESSION`/`TMUX_RELEVANCE_UNAVAILABLE` info findings);
**memory pressure** — implemented (PSI avg10 some/full + cgroup fill % + host
avail %, thresholds labeled local, `MEM_PRESSURE_HIGH`/`MEM_FILL_HIGH`/
`MEM_AVAIL_LOW` warn); **disk write-rate** — since-boot average implemented
+ instantaneous two-sample explicitly deferred with named precondition
(`tools/mori-census.sh:48-52`, `surfaces-r7.md`); **state_rounds values** —
implemented (per-value read, lag/ahead vs ledger, info-severity so an
inconsistency is visible but cannot flip the roll).

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | four receipt-backed gaps closed (three fully, one honestly partially); +15 selftest cases with positive/negative fixtures; per-gap tester seats verified live rows against independent recomputation (diskstats arithmetic, state-file values). |
| operability | **unchanged** | selftest 30 → 45 all green; oracle 28/28 held through an additive-only re-baseline; pipefail-auditor found two new bare pipelines mid-wave — fixed by census-impl before close (receipt-backed). |
| depth | **improved** | `corpus/knowledge/surfaces-r7.md` (probe designs, labeled-local thresholds, deferral precondition); `observability-surfaces-r2.md` gap sections updated with pointers; lesson `2026-10-15-free-lunch-measurements-counter-baselines.md`. |
| freshness | **improved narrowly** | seven r7 receipts at the new SHAs (incl. per-gap live receipts); the drift pin remains the one carried item. |
| calibration | **unchanged** | thresholds labeled local, never tuned as universal; info-vs-warn severities assigned so visibility ≠ DRIFT. |
| adjacency | **unchanged** | unit-failure counts stay out-of-scope-flagged (tsukuroi's province); scope-sentinel clean; no remediation content. |

Honest residuals (named in `surfaces-r7.md`): instantaneous write-rate
(deferral); tmux per-session freshness (not claimed); `*.round` symlink/dir
invisibility; memory-tester's three residual items. Admission: **ADMIT** (one
axis improved, none harmed). No scalar score. Learning trends:
expansion/quality **improved**, discernment **unchanged**.

## Round 8 verdict — 2026-10-15 (goal wave; evidence commit `9738f1a`)

Selected axis: coverage/operability residual closure — the four `surfaces-r7.md`
residuals. Wave: one 31-seat flash call, 31/31. Report:
`.ufo/reports/round-8/mori-goalwave.md`.

**Before** (`c7c3569b…`, selftest 45): instantaneous write-rate deferred
without a cost number; tmux per-session freshness unmeasured; `*.round`
symlink/dir cases silently invisible; memory-probe residuals open.

**After** (census r5 `390ab9cd…`, selftest 56 = +11; oracle `448f7723…`
**not** rebased — the census delta was additive-only and the oracle fixtures
see the new probes as `unavailable`, so 28/28 held unmodified; parent
acceptance 2026-10-15T21:05Z): (1) write-rate: **deferral upgraded to measured
numbers** — isolated micro n=30/arm: 0.2 s two-sample adds +213 ms median (min
210 ms = 4.2× the 50 ms budget) → the admission rule says defer, so it defers
ON THE NUMBER, recorded in the header + `surfaces-r8.md`; (2) tmux per-session
freshness implemented (timeout-bounded, rc-gated, `freshness/probed/idle/
idle_warn_s` fields, 4 canaries incl. a frozen-tmux no-hang proof); (3)
roundfile diagnosis implemented (`state_val_unread_reasons=file/symlink/dir/
other` with per-reason counts; symlink target never read); (4) memory residuals
disposed per the note. Live rows carry the new fields (`state_rounds_max=18
state_lag=0`, `mem_peak/mem_peak_anchor`, `io_avg_since_boot=dm-0:8625212Bps/
15821s`); additive-only proven by a pinned-fixture field diff (exactly the 4
new names, none lost).

**Defect folded at admission (measured, not asserted):** the selftest harness
has a flaky-failure class — a grep-over-pipe SIGPIPE race at
`tools/mori-census.sh:1783/:1809`: admission seat ~25% false-FAIL in one
battery; parent determinism battery 1/8 (55/56, "missing match" on a silence
case); parent main acceptance 5/5 green. Root-caused to the harness pipe race,
NOT to probe logic (every false-FAIL is a different case, all green on rerun).
Verdict: **ADMIT-with-correction** — the four residual dispositions are
receipt-backed and additive-only holds, but "selftest all-pass" is currently
~87-100% deterministic; the flake is the registered round-9 top debt (fix the
race; add a determinism gate to admission).

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | three residuals closed with measured probes (freshness, roundfile reasons, memory) + one closed-by-measurement (write-rate deferral with numbers); +11 selftest cases; per-gap testers verified live rows against independent recomputation. |
| operability | **improved narrowly** | selftest 45 → 56; oracle 28/28 held WITHOUT a rebase (additive-only proof by pinned-fixture field diff); hang-guard bounded the new probe's worst case. Correction: the harness flake (:1783/:1809) measured at 1/8–25% — named, top r9 debt. |
| depth | **improved** | `corpus/knowledge/surfaces-r8.md` (dispositions, the cost-adjudication numbers from two independent measures, open items); lesson `2026-10-15-probe-pricing-dwell-bounds-filter-drop.md`. |
| freshness | **improved narrowly** | eight r8 receipts at pinned SHAs; drift pin still carried. |
| calibration | **unchanged** | the 50 ms budget rule was applied as written (defer won on the number); thresholds remain labeled local. |
| adjacency | **unchanged** | scope-sentinel clean; stub binaries slept only inside /tmp fixtures; no remediation content. |

Admission: ADMIT-with-correction (flake named; none harmed on the substance).
No scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 9 registered: eliminate the selftest flake class
(`:1783/:1809` SIGPIPE/grep race) — receipt-backed 0-flake over a ≥20-run
battery, selftest 56 green, oracle 28/28, zero probe-behavior change.

## Round 9 verdict — 2026-10-15 (goal wave; evidence commit `cffb37e`)

Selected axis: **operability** — the round-8 correction's named top debt: the
selftest harness flake. Wave: one 28-seat flash call, 28/28. Report:
`.ufo/reports/round-9/mori-goalwave.md`.

**Before** (`390ab9cd…`): selftest false-failed at 1/8–25% on a random case —
a grep-over-live-pipe SIGPIPE race (`grep -q` matches and exits while the
writer is still writing; pipefail turns the writer's SIGPIPE (rc 141) into a
scored "missing match"). The impl measured the class directly: 15/8000
non-zero rcs, all rc=141, concentrated when the match sits early in the
stream; 12–15/10000 false misses by payload size.

**After** (census `1c49238a…`, diff 21/7 **all inside `run_selftest()`** —
VERSION stays `census-r5` so production output is byte-identical; six
live-pipe-grep sites converted to capture-once-then-grep-file; zero pipelines
added; the two deliberately-kept pipes are read-all with no early-exiting
consumer, outside the class): race rate 0/60000 in the impl's micro-bench;
battery A 20/20 green (4-way concurrent); battery B 20/20 green **under 4 CPU
hogs**; parent battery 10/10 green; oracle `448f7723…` byte-frozen and 28/28
exit 0 (production path untouched — proven by the unchanged oracle wants);
live census honest (`DRIFT findings=15 drift=14 unavailable=1`). Git
archaeology (two seats, independent): the race predates r8 — reproducible at
the r7 bytes — r8's additions only widened the exposure.

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | 1/8–25% flake → 0 across 70+ post-fix runs incl. load (races measured 15/8000 → 0/60000 at the mechanism level); the selftest is now deterministic; production census byte-identical (oracle frozen, wants unchanged). |
| coverage | **unchanged** | 56 selftest cases, names byte-identical; no surface change. |
| depth | **improved** | `corpus/knowledge/selftest-flake-r9.md` (mechanism, rc=141 SIGPIPE anatomy, the capture-then-grep pattern, archaeology); lesson folded there + the pipefail lesson lineage. |
| freshness | **unchanged** | receipts at the new SHA; the drift pin remains the carried item — round 10's registered claim. |
| calibration | **unchanged** | the determinism bar (two independent ≥20-run batteries, one loaded) was met as written. |
| adjacency | **unchanged** | scope-sentinel clean; oracle byte-frozen; CPU hogs killed by their seats; no remediation content. |

Admission: **ADMIT** (operability/depth improved, none harmed). No scalar
score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 10 registered: the long-carried **drift pin** (freshness)
— a committed behavioral baseline plus a `--drift` mode with a declared
volatile-fields list, so census behavioral drift is itself detected; selftest
cases + receipts; oracle held green.

## Round 10 verdict — 2026-10-15 (goal wave; evidence commit `5be8943`)

Selected axis: coverage-of-self — the drift pin, carried since round 2.
Wave: one 29-seat flash call, 29/29. Report:
`.ufo/reports/round-10/mori-goalwave.md`.

**Before** (`1c49238a…`): no behavioral baseline; census regressions were
catchable only by humans reading receipts (rounds 2–9 relied on seat
discipline; the r8 flake existed for rounds before detection).

**After** (census `d7710981…`, selftest 66 = +10; oracle `448f7723…` frozen,
28/28; parent acceptance 2026-10-15T22:40Z): `--pin` writes a normalized
baseline with a declared volatile contract (`ts/age_s/*_epoch/counters/psi/
io_avg/script_sha256` masked to `<V>`, the list recorded in the baseline
header); `--drift` reports `MORI_DRIFT: none` (exit 0) or names the changed
non-volatile fields / `-key`/`+key` / `-FINDING:<id>` / line ids / `VERDICT`
(exit 1); missing/unreadable/malformed baseline → exit 2. The lane committed
its own live baseline (`corpus/evidence/baseline-r10-20261015T2231Z.json`) and
the parent re-ran `--drift` against it: clean, exit 0. Independent verifiers:
pin→drift roundtrip ×5 deterministic; injected regressions name exactly the
field (`warn_pct`, `+tester_extra`, `-SURFACE:disk`, `+state_lag_sec
-state_lag`, `VERDICT` on tampering); the overmask hunter could NOT hide a
dropped row, a rename, or a threshold change; live churn over 70 s stays
`none` (mask exercised, not trivial). Default-mode output byte-identical
(stamp-normalized hash equal both bytes).

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the census's own behavior over time is now a measured surface: baseline + drift contract + 10 new selftest cases + committed lane baseline + re-run recipe in the evidence index. |
| operability | **unchanged** | 66/66 green ×4; oracle 28/28; drift runs add no sampling delay (perf seat). |
| depth | **improved** | `corpus/knowledge/drift-pin-r10.md` (design, volatile rationale, over/under-masking risks, re-pin policy); lesson `2026-10-15-volatile-contract-behavioral-baselines.md`. |
| freshness | **improved** | the round-2-carried drift pin is LANDED; seven receipts + the baseline at pinned SHAs. Named: unmasked state words (`rc=`, `log=`, surface states) legitimately flip with host state — a future red drift may be baseline aging; the re-pin policy is documented, not hidden. |
| calibration | **unchanged** | the volatile contract was measured (three live runs, field-by-field diff) before being declared; under-masking risks are named with examples. |
| adjacency | **unchanged** | scope-sentinel clean; oracle byte-frozen; no remediation content. |

Admission: **ADMIT** (coverage/depth/freshness improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 11 registered (capstone, operator-directed strong model):
a full-lane deep audit on `openai-codex/gpt-6.1-sol` — every admitted round's
evidence chain re-verified, carried debts adjudicated, SHONEN readiness
assessed without self-attestation, and the four most load-bearing historical
claims re-executed at today's bytes.

## Round 11 verdict — 2026-10-15 (capstone audit, operator-directed strong
model `openai-codex/gpt-6.1-sol`; evidence commit `e4855e8`)

Selected axis: **calibration** — deep discernment: an independent-quality audit
of the whole lane corpus (the operator directed the strong model for this
round). Wave: one 32-seat call on `gpt-6.1-sol` (max effort), 34/34 reports.
Report: `.ufo/reports/round-11/mori-goalwave.md`; consolidated findings:
`corpus/knowledge/audit-r11.md`.

**What the audit confirmed (measured coverage, not vibes):** all 50 r2–r10
receipts exist and hash-verify; the evidence README indexes them completely;
every cited commit resolves and is ancestral; the cumulative tools/ diff equals
the sum of the rounds' claimed changes (no silent hunks); every round's
per-axis table satisfies the admission rule with verdict vocabulary only; the
correction-disposition ledger shows every named correction/residual either
dispositioned or still open — no silent drops; the four load-bearing
historical claims re-executed at today's bytes (r3 counterfactual class: 136
case evaluations; r4/r5 sniffer class: 195 case results, attackers in the
0–2/28 class; r9 flake battery: 0 flakes; r10 drift: clean + tamper named the
field). Parent battery at acceptance: selftest 66/66, oracle 28/28,
`MORI_DRIFT: none` exit 0 against the committed baseline (baseline byte-
unchanged since `5be8943`), live honest.

**What the audit corrected (folded at admission):** (1) **SHONEN: hold
promotion — 0/4 boxes gate-ready**: box 2 is `ready-for-named-non-author-
review`; boxes 1/3/4 are blocked-by-X (source-linkage; dead baseline recipe +
inconsistent instructions; external-shim attribution). Same-wave seats are the
lane per protocol; the gate needs a named non-author verifier. (2) **140/275
historical fixture fingerprints are not independently recomputable** from
durable artifacts (they live in /tmp scratch from their rounds) — a scratch-
evidence class; the audit could verify the receipts but not re-derive every
fixture tree. (3) **Three independently established defect categories** (per
the admission seat) with the register in `audit-r11.md`. (4) Report-format
nit: rounds 5–10 reports collapse the four SHONEN box lines into one physical
line. (5) Parent hygiene fold: the r10 acceptance's drift line was measured
through a pipe with a wrong-glob (`.txt` vs `.json`) — conclusion correct
(verified now with a direct run: `none`, exit 0), method sloppy; the r11
admission ritual gains an exit-code discipline line.

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | the lane now knows, with measured coverage, WHAT is verified (50/50 receipts, resolved commits, re-executed claims) and WHAT is not (scratch fixtures, universal correctness, promotion gates) — discernment at depth, strong-model seats per operator directive. |
| depth | **improved** | `corpus/knowledge/audit-r11.md`: findings table, final debt register, SHONEN readiness, operator recommendations; lesson `2026-10-15-settle-evidence-references-with-artifacts.md`. |
| coverage | **unchanged** | no new measured surface (the audit measured the measuring). |
| operability | **unchanged** | battery green at today's pins; the audit changed no tool bytes. |
| freshness | **unchanged** | baseline still clean (aging risk named, not realized). |
| adjacency | **unchanged** | audit seats wrote only their assigned artifacts; tools/ untouched (scope-sentinel verified). |

Admission: **ADMIT-with-correction** (calibration/depth improved; corrections
named; none harmed). No scalar score. Learning trends: expansion/quality
**improved**, discernment **improved** (the audit itself is the first round
whose core product is discernment; it was externally probed by the critic-of-
the-audit seat and still ships named limits).

**mori rounds 2–11 complete: ten admitted rounds.** Carried forward to the
operator (not lane debts): named-non-author SHONEN verification, the receipt-
binding and role-routing debts (blocked-attempt, operator/integrator
surfaces), and the promotion decision itself.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| — none yet — | | | |

Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.

## Saturation

The lane's saturation line + stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

## Round 12 — kaika campaign: sources, mistakes, roster (2026-10-19)

Steered round 12 (orchestrator steer table; lane LOG and MANIFEST agree on 11). Base
`20e2255`; measured at the round-12 commit (hash in the round-12 LOG entry and
`.ufo/reports/round-12/mori.md`). Commands run from the lane root; the census needs
`MORI_SHOKUNIN_ROOT=<fleet root>` when run from a worktree.

| # | claim (type) | axis | before → after | counting command | evidence |
|---|---|---|---|---|---|
| 1 | source-linked depth (capability acquisition: source registry) | depth | SKILL URLs 0 → 5, unregistered or non-A/non-mined 0 → 0; knowledge entries with `source:`/`verified-at:`/`recheck:` on lines 1–3 citing an A/mined row 0 → 4; SOURCES rows 0 → 33 with a clean contract-v1 census | `grep -oE 'https?://[^ )>\|`]+' SKILL.md \| sort -u \| wc -l`; the planner's A/mined linkage counter (`corpus/lessons/round-12.md` §Gate cites it); SOURCES-CONTRACT-v1 census block | `corpus/SOURCES.md`; `corpus/knowledge/*-r12.md`; `SKILL.md` error-pattern rows |
| 2 | mistakes → lesson-cited criteria | calibration | QUALITY criteria citing a lesson 0 → 20; `## Mistakes` rows 0 → 26 (captured-by `none` 5, each with a reason) | `grep -cE '^[0-9]+\. .*lessons/' corpus/QUALITY.md`; `grep -cE '^\| M[0-9]+ \|' corpus/lessons/round-12.md`; `grep -cE '^\| M[0-9]+ \|.*\| none \|' corpus/lessons/round-12.md` | `corpus/QUALITY.md` §Criteria added round 12; `corpus/lessons/round-12.md` |
| 3 | silence roster = declared lanes ∪ driver counters | coverage | live `SURFACE lane.*` rows 9 → 23 (`roster_source=conf+state`, `ROSTER_SET_MISMATCH` info: conf-only kotodama,souji; state-only audio,game-dev-2d,game-dev-3d); selftest 66 → 77 PASS; oracle 28/28 at unchanged sha `448f7723…` | `MORI_SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/mori-census.sh \| grep -c '^SURFACE lane\.'`; `bash tools/mori-census.sh --selftest`; `bash tools/mori-silence-cases.sh` | `corpus/evidence/roster-r12-20261019T220912Z-*.log`; `corpus/knowledge/roster-truth-r12.md`; census `d7710981…` → `3da5b098…` |

| axis | verdict (lane self-assessment, pending non-author verification) | score | evidence |
|---|---|---|---|
| depth | **improved** | 4 → 5 | claim 1; every SKILL URL resolves to an A/mined row; four knowledge rechecks re-executed by the L1 (line numbers 935/936/447/452/945/1820/1825/4966/269/306/66/604/884 and counts 7/9/5 reproduced) |
| calibration | **improved** | 5 → 6 | claim 2; discernment *trend* stays unjudged until the outside spot-check (`LEARNING.md` §Discernment) |
| coverage | **improved** | 5 → 6 | claim 3; 14 lanes graded that were invisible (incl. mori itself) |
| operability | **unchanged** | 6 | gates green at new bytes; cost named, not hidden: live census wall time 1884/1830/1930 ms → 4345/4339/4278 ms (`evidence/roster-r12-20261019T220912Z-walltime.log`), linear in roster size (≈0.17 s per graded lane), no declared runtime budget exists to breach — the critic seat disputes "unchanged" for want of a budget; operator to rule |
| freshness | **unchanged** | 5 | r10 pin was red before the round (aging, every token classified: `evidence/drift-r12-20261019T2204Z-classification.md`); after the roster change it additionally names exactly the 14 new lane rows and the roster fields (`evidence/drift-r12-20261019T2230Z-after-roster.log`) — detection working, no re-pin this round |
| adjacency | **improved** | 6 (held) | unclaimed contract repair, not one of the round's three claims, so no counting command and no score move: souji added to PROVINCE `## Adjacent` (siblings named 4 → 5); inbound TSUKUROI-F1-MEM-01 answered in PROVINCE (no retained kill record overlaps 2026-10-15T04:53:46Z; all 5 are dated 2026-10-18); tsukuroi's `oom-event-plane.md`/`kill-event-deep-r8.md` cited from each kill entry |

Correction to the score table at the top of this file (frozen at round 1; 4 of 6 pointers stale —
STATE dossier §2): the table is left as filed; this section's scores supersede it. Stale pointers:
coverage ("per-surface notes still owed" — landed r2), operability ("14/14" — 76 at r12),
freshness ("no drift pin yet" — landed r10), calibration ("`progressing-weak` deferred" — landed r3).

Capability rows (below) enter through this round's demonstrations.

## Capabilities (round 12 demonstrations)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| source registry | curate where mori learns: 33 opened, tiered, anchored rows with paths and a search log; contract-v1 census clean (malformed 0, duplicates/enums/tier-inflation/missing used-by empty) | `corpus/SOURCES.md` + contract census commands | 12 |
| live census | read-only census of watchdog, waves, journal, cgroup, disk, tmux and lane silence, now over the declared lane universe (23 lanes) | `corpus/evidence/roster-r12-20261019T220912Z-live.log` | 1 |
| census self-test | hermetic fixture self-test asserting exit code + finding id | `corpus/evidence/roster-r12-20261019T220912Z-selftest.log` (77/77) | 1 |
| silence oracle | behavioral gate with seeded shuffle + per-run nonce over the silence grading | `corpus/evidence/roster-r12-20261019T220912Z-oracle.log` (28/28) | 2 |
| drift pin | behavioral baseline compare naming every changed non-volatile field | `corpus/evidence/drift-r12-20261019T2230Z-after-roster.log` (names the 14 new lane rows) | 10 |

## Saturation (declared round 12)

Saturation line: **8/10** on each owned axis (coverage, operability). Stagnation window **N = 3**
admitted rounds without a capability entering the table. Reason: owned axes sit at 6 and 6; 8
leaves headroom, and 3 rounds avoids firing the nudge on a one-round plateau.

## Planned (round 13)

1. **freshness** — re-pin after classification: before `--drift baseline-r10-20261015T2231Z.json`
   exit 1 (classified tokens); after a new baseline file pinned with a recorded reason, old file
   kept, `--drift <new>` → `MORI_DRIFT: none` exit 0. Falsified by any unclassified token.
2. **operability** — close audit F01/F02: before, the long-history fixture grades
   `progressing-weak` despite a lane commit and the BANANA verdict wrapper scores 28/28; after,
   the fixture grades `progressing` and the wrapper fails while the honest oracle stays 28/28.
3. **coverage (frontier → core)** — FR1: a MESSAGE-free system-journal kernel-OOM count probe
   with its own finding id; before 0 kernel-OOM records visible to the census, after the 5
   retained records counted with `unavailable` when the system journal is unreadable.

## Round 12 post-review corrections (appended 2026-10-19)

- **Expansion:** four admitted knowledge entries qualify on uncovered ground; `corpus/knowledge/roster-truth-r12.md` is local measured census evidence, not a fifth expansion entry. This supersedes any reading of the trend count that includes it.
- **Calibration:** verdict **improved** under the kaika campaign binding (mistake mining into lesson-grounded QUALITY criteria is calibration work); scalar score **held at 5**, not 6, because the non-author reviewer could not re-derive 6.
- **Adjacency:** verdict **unchanged**, score **6 held**. The contract repair was unclaimed and had no counting command or score move; this supersedes the round-12 row's unsupported “improved” verdict.
- **Mutation coverage:** on round-head census SHA-256 `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164`, baseline selftest 77/77 and the re-run battery killed 12/12 mutants (0 survived, 0 inconclusive); receipt `corpus/evidence/roster-r12-20261019T220912Z-mutation.md` post-review section.

## Round 13 — structured journal scopes and verdict-contract repair

Steered round 13, attempt 1, 2026-10-20. Exactly **two** causally separable
claims: C1 coverage (capability acquisition), C2 operability. Both owned axes
entered at 6; the lowest-owned-axis obligation is met. The planned freshness
re-pin is not claimed. The prior FR1 plan's “five kernel records” is corrected:
those historical `--grep` matches were MESSAGE-selected and belonged to a
prior boot. This round advances structured notice/result coverage only.

Measured revision: **c13df48**, census SHA-256
`39abda0a67028575d888d9157b8548dec0b4944c3d8c165691e88ab657fc3985`,
oracle SHA-256
`34cd5770889ec6e7521b477aa9976cece7a64e07b83774c12ce2aea73161abfa`.
Before inputs: frozen r12 census/oracle from `6531ac6`, pinned by
`.ufo/waves/round-13/frozen/inputs.json`; the before measurement's harness
revision is 80bd58a. Two harness-only expectation corrections are recorded in
LOG.md and retained red receipts; production bytes did not change for them.

| claim | axis | before → after | counting command (lane root) | evidence |
|---|---|---|---|---|
| C1 dual-scope structured journal records | coverage | explicit scoped surfaces **0 → 2**; source-counter parity **12/12**; five C1 behavioral checks pass | `jq '[.result.baseline.stdout,.result.delivered.stdout] \| map(split("\n") \| map(select(startswith("SURFACE journal."))) \| length)' .ufo/waves/round-13/evidence/live-measurement.json` → `[0,2]` | `live-measurement.json` includes executable Python reproducer, full censuses and bracketing field-only queries; `regressions-accepted/evidence.json`; sourced by S013/S014/S015/S035/S036 |
| C2 exact-author and final-verdict correctness | operability | demonstrated named defects **2 → 0**; subject-first history row-C → row-A; BANANA oracle 28/28 accepted → 0/28 rejected; honest oracle 28/28 held | `jq -s '[.[] \| [.claims[] \| select(.id == "R13_F01_EXACT_AUTHOR_LONG_HISTORY" or .id == "R13_F02_REJECT_BANANA") \| select(.status == "expected-defect" or .status == "fail")] \| length]' .ufo/waves/round-13/evidence/regressions-before-final/evidence.json .ufo/waves/round-13/evidence/regressions-accepted/evidence.json` → `[2,0]` | frozen before + accepted after receipts; 19 contract checks pass, 2 exact-locus mutation-red witnesses, exit 0; S031 and audit-r11 F01/F02 |

Local score rubric (not a fleet scalar): retain the entering 6; add one point
for C1 only when the two scoped surfaces exist, all five C1 behavioral checks
pass, and all twelve live cells match; add one operability point only when the
two named defects are absent, honest oracle/control cases hold, and both
exact-locus negative witnesses reproduce the old failure. The commands and
receipts above re-derive both conditions. No score is awarded for row volume,
test volume, unclaimed repairs, or the raw fact that a baseline-mode run exits 0.

| axis | verdict (lane assessment; outside closure pending) | active score | evidence / limitation |
|---|---|---|---|
| coverage | improved | **6 → 7** | C1 rubric met; user SIGKILL WARN path retained through structured result metadata, not a silent deletion; system notice/result plane only, kernel attribution remains FR1 |
| operability | improved | **6 → 7** | C2 rubric met; census selftest **91/91**, harness pure checks **24/24**, honest oracle **28/28**, 19 behavior checks plus 2 mutation-red; audit D02's arbitrary tally/aggregate weaknesses remain outside this demonstrated fix |
| depth | unchanged | **5 held** | new sourced notes support the two claims; no independent depth claim or score |
| freshness | unchanged | **5 held** | r10 baseline retained; current compare exits 1; 42 tokens classified into intentional journal schema, carried r12 roster schema, and explicitly inferred live-state families; not a regression-free proof and no re-pin |
| calibration | unchanged | **5 held** | honors round-12 non-author score correction; Q26–Q28 and harness-error lesson are unclaimed contract/learning work, not scalar credit |
| adjacency | unchanged | **6 held** | tsukuroi owns OS diagnosis, kumitate orchestration; no remediation, publishing, sibling edits or assumed handoff closure |

Costs: one interleaved live pair took **3.025310 s → 2.960516 s**, not a
distribution or a speedup claim. The honest hermetic oracle took 1.881 s
before / 3.132 s after in the recorded suite. Journal producers are now bounded
at 2 s + 1 s grace per query (12 queries); parsing and other surfaces are not
covered by that producer bound. No existing declared budget was tuned.

### Capabilities demonstrated round 13

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| dual-scope journal records | report six boot-anchored class counters separately for user/system, unavailable on unsafe reads, never MESSAGE or summed kill totals | `.ufo/waves/round-13/evidence/live-measurement.json` (12/12); `corpus/knowledge/structured-journal-scopes-r13.md` | 13 |
| strict census verdict validation | reject malformed/duplicate/nonterminal/rc-inconsistent final rolls while retaining honest lane cases | `.ufo/waves/round-13/evidence/regressions-accepted/evidence.json` (BANANA 0/28; honest 28/28) | 13 |

### Frontier, trends and remaining limits

FR1 notice/result plane advances to Core; kernel victim-token attribution and
fleet correlation remain Frontier. FR11 cursor semantics remain unknown.
SOURCES 34 → 36 (A31 → A33, B2/C1 held), mined12 → 15, queued21 → 20,
rejected1 held; validation exits 0 with informational W04 for S013/S035's
same URL across different scopes. Mistakes and all mutable source-cell
old→new changes are in `corpus/lessons/round-13.md`.

Trends: expansion improved (new working dual-scope capability); quality improved
(F01/F02 repairs, stronger structured selection and marked historical
`--grep` overclaims); discernment improved through a lesson-backed Q28 response
to the previous outside review, not through calling this round's own seats
independent. Current non-author admit/reject verification remains pending.

Named residuals: client-set journal identifiers, duplicate records,
fail-closed array values, silent partial-store access, kernel-token parsing,
unvalidated roster overrides, oracle aggregate/registry-count vacuity and
arbitrary finding-tally corruption. No broad “cannot fake” claim is made.
Next steered work starts from these residuals and the deferred, reasoned
drift re-pin; no next round was started.

## Round 14 — outside correction and declared repair

Entering revision `dbe85009253c092fe50e4e93056fceeae273ec31`. Outside closure
`corpus/lessons/round-13-verifier-spotcheck.md` rejected round 13 as harmed:
coverage and adjacency harmed, operability improved; depth/freshness/
calibration unchanged. This supersedes the author no-harm/admission rows above.
The unrestricted coverage point is withdrawn: active coverage **6**, not 7.
Operability's independently verified F01/F02 improvement remains **7**;
depth/freshness/calibration/adjacency remain **5/5/5/6**. Historical scores and
receipts remain unchanged. The prior 24-check harness selftest was at
80bd58a, not the finally delivered c13df48 revision.

**One claim, C1 coverage:** restore structured OOM critical/DRIFT alarms,
fleet-only UNIT_FAILURE_JOURNAL and non-fleet UNIT_FAILURE_OUT_OF_SCOPE with
tsukuroi diagnosis routing, preserving six class counters in each independent
scope. Same regression command over pinned entering and delivered bytes
must show failed requirements before and zero failures after. Missing failed
subject metadata is unknown, not non-fleet. This works the lowest owned
non-retired axis, coverage (6 versus operability 7).

No new scalar point is pre-awarded for repairing a prior harm; coverage stays
6 unless an explicitly measured rubric warrants otherwise. Gate registration,
fresh delivered-selftest evidence, provenance and index corrections are
unclaimed conformance/learning work. Original frozen-byte failures remain
primary for F01/F02; their mutations are whole-function F01 and reconstructed
F02-prefix-shim witnesses, not byte-exact membership-line restorations.

### Round-14 measured result

**C1 verified (coverage improved; score 6 held).** The measured acceptance
counter is six named behavioral arms, not six independent production defects.
Against frozen entering census `39abda0a…`, the arms fail **6 → 0** after the
repair, using the same gate SHA `c39e5a73…`. Measured commit:
**5601d1201926124f7884bc694568abac2ead6d5c**. Census and migrated r13 gate
were already measured at 8d22d18 and did not change in 5601d12.

Counting command (lane root), executed exit 0, output `[6,0]`:

```sh
jq -s '[.[] | [.claims[] | select(.id == "R14_OOM_ALARM_USER" or .id == "R14_OOM_ALARM_SYSTEM" or .id == "R14_UNIT_OOM_KILL" or .id == "R14_UNIT_FAILED_FLEET" or .id == "R14_UNIT_FAILED_NONFLEET" or .id == "R14_UNIT_SIGNAL_WARN") | select(.status == "fail")] | length]' .ufo/waves/round-14/evidence/red-before-accepted/evidence.json .ufo/waves/round-14/evidence/green-after-accepted/evidence.json
```

The full strict before run exits 1 (43 failed assertions, including new
metadata requirements absent even from frozen controls); after exits 0
(43 cases + one required frozen-red control = **44 pass**). This is not a
claim of 43 historical bugs. Inspected named reasons show CLEAN/no critical
OOM → DRIFT/one critical alarm; missing non-fleet route → INFO owner=tsukuroi;
legacy generic signal-result warning is also restored. Raw positive counters
hold user `3/0/2/1/2/1`, system `2/1/4/3/0/2`, in six-class order. Both live
scoped rows remain (2 → 2), **12/12** bracketing cells match, all zero.
Evidence/counts: `.ufo/waves/round-14/evidence/c1-measurement.json`,
`live-measurement.json`.

| axis | verdict | score | evidence / limitation |
|---|---|---|---|
| coverage | improved | **6 held** | C1 restores prior harm and acquires typed subject/result handling; no extra point for repairing a rejected cutover |
| operability | unchanged | **7 held** | F01/F02 preserved: r13 suite 24 pass + 2 mutation-red, honest 28/28/BANANA 0/28; census 104/104; new gate setup defect caught and repaired, not counted as successful red evidence |
| depth | unchanged | **5 held** | S037/S038 support the C1 subject/result semantics; no independent depth claim |
| freshness | unchanged | **5 held** | old r10 baseline still exits 1 at 5601d12 (`evidence/drift-current.json`); no re-pin or clean-current-drift claim |
| calibration | unchanged | **5 held** | Q29–Q32 and explicit unknown/mutation qualifications are lesson-backed repairs, not scalar credit or outside self-certification |
| adjacency | improved | **6 held** | collateral restoration within C1: `R14_UNIT_FAILED_NONFLEET` fails before, passes after with owner=tsukuroi; diagnosis only, no sibling/OS mutations or new ownership claim |

Capability acquired through C1, not a second claim:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| typed journal alarm and subject triage | restore OOM/legacy signal alarms and partition failed-unit subjects fleet/non-fleet/unknown using structured fields, independently of scoped totals | `evidence/green-after-accepted/evidence.json` under `.ufo/waves/round-14/`; `corpus/knowledge/journal-alarm-routing-r14.md` | 14 |

SOURCES **36 → 38**, A33 → A35/B2/C1, mined15 → 17/queued20/rejected1;
both validator invocations exit 0 (informational duplicate-URL W04 only).
Trends: expansion **improved** (typed subject/result-plane knowledge), quality
**improved** (repaired rejected entry, live counter recheck and actual gate
self-invocations), discernment **improved** (outside disagreement learned as
Q29–Q32 with failing witnesses). This round's non-author admit/reject
spot-check remains pending; our 32 dispatched seats do not satisfy it.

Residuals remain explicit: client-set labels, name-token routing not exhaustive
membership, all-or-nothing malformed class handling (can hide an alarm),
unavailable does not imply DRIFT, unvalidated environment overrides, partial
store access/retention, old drift pin redness and broader oracle tally/forgery
debt. No SHONEN mark or rank is changed.

## Round 15 — declared coverage claim

Entering revision: `0fa5e0d` (the round-14 non-author spot-check).
Active owned axes remain coverage **6**, operability **7**; the former is
the lowest owned non-retired axis. Other scores remain depth/freshness/
calibration **5/5/5**, adjacency **6**. No stagnation waiver is used.

**C1 coverage:** preserve an OOM critical/DRIFT or user signal WARN/DRIFT
from an individually valid current-boot structured record when another
record invalidates the aggregate class. Existing raw totals and subject
partitions remain unavailable; additive `positive_*` tokens are validated
evidence subsets, not replacement complete totals. No malformed-JSON salvage,
extra journal query, authenticated membership or unique-victim claim.

Falsifiable metric: the same committed fixture packs and gate run against
pinned entering and delivered census bytes; count failed C1 case assertions
before → after. Mixed-positive failures must become zero, negative controls
must stay clean, and homogeneous scoped counts/owner routes must survive.
This repairs the explicitly disclosed suppression gap, not every event path.
Scores are held rather than awarding a point for fixture quantity.

### Planned (supersedes prior next-round intentions)

Only steered round 15 is executed here. Work the FR1 malformed-class
failure-mode boundary within C1; retain the old red drift pin as declared debt
without re-pinning. Dirty-path capture and active wording clarifications from
`corpus/lessons/round-14-verifier-spotcheck.md:134–140` are unclaimed
conformance/learning work. Independent outside closure remains required.

### Round-15 measured result

**C1 verified by the lane, pending non-author closure.** Measured gate/input
commit **1822145d95682709069bbc8f4e1b947ddbe20078**. The same final gate
SHA `6a55c33cc13e2cd862ebd44db66e8af635a35d7cd2a85168360569c886d62ffe`
grades pinned entering census `0e41cb83…` and delivered census `f1f8d1b6…`
against the same 63 committed cases. **Behavioral failures 34 → 0**; strict
run exits **1 → 0**, after **63/63 pass**. Full-schema failures are
63→0 because the old implementation also lacks the new fields; neither 34
nor 63 is a count of distinct production bugs.

Counting command, executed exit0, output `[34,0]`:

```sh
/usr/bin/jq -s '[.[].summary.sut_behavior_fail]' .ufo/waves/round-15/evidence/red-before-final/run-manifest.json .ufo/waves/round-15/evidence/green-after-final/run-manifest.json
```

Both runs reproduce **34/34** specifically missing-alarm frozen controls,
with zero inconclusive or unexpected controls; the other 29 legacy controls
pass. Seven separate capture-boundary cases pass, including valid-looking
bytes from failed rc124/137/5, stderr and malformed capture, plus a surviving
other-scope alarm. Evidence: `evidence/c1-measurement.json`,
`capture-boundary/run-manifest.json` under `.ufo/waves/round-15/`.

| Axis | Verdict | Active score | Evidence / limitation |
|---|---|---|---|
| coverage | improved | **6 held** | C1 finite mixed-record failure modes 34→0; raw unavailable preserved; not full event coverage |
| operability | unchanged | **7 held** | census113/113, oracle28/28, r13 24pass+2mutation-red, r14 44/44; delivered r15 selftest and full controls pass; capture-oracle setup error retained and repaired |
| depth | unchanged | **5 held** | S014/S015/S037/S038 ground predicates; no separate depth claim |
| freshness | unchanged | **5 held** | live recheck has two scoped zero rows; old r10 drift remains red exit1, no re-pin |
| calibration | unchanged | **5 held** | complete totals vs subset evidence explicit; procedural violations and actual setup failure disclosed, outside closure pending |
| adjacency | unchanged | **6 held** | aggregate-only owner partition and tsukuroi route preserved; no dispatch/OS actuation or membership takeover |

The preserved gates/census were measured at `26f6589dfa2a07e41a6dcfda99c2998bce2c0932`;
their verdict-driving bytes are unchanged in 1822145. Final r15 receipts name
real HEAD plus exact dirty paths and input hashes; `stable=true` and unchanged
input digests refer to measured scope, never every host surface.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| partial positive journal alarms | retain critical OOM/user-signal WARN from qualified current-boot records while invalid aggregate totals remain unavailable | `.ufo/waves/round-15/evidence/green-after-final/run-manifest.json`; `corpus/knowledge/journal-positive-evidence-r15.md` | 15 |

SOURCES **38→38**, A35/B2/C1 and mined17/queued20/rejected1 held; four used-by
cells extend to the new knowledge note, no immutable changes or new rows.
Trends: expansion improved (FR1 failure-mode ground); quality improved
(stronger measured alarm contract); discernment improved through prior
outside findings learned as Q33–Q36, not through calling our own seats outside.
Round execution carries procedural conformance debt M4–M6; no blanket
conformance or independent admission is self-certified.

Next steered-round plan, not executed here: coverage/FR11 cursor-bounded
new-since-pin observation; retain the reasoned drift re-pin as separate
freshness debt until an actual semantic review is assigned.

## Round 16 — declared cursor-window capability

Entering revision `b83edc6ee3db6822382ab673d7e6e984e420f22f`.
The round-15 outside closure admitted bounded C1 with procedural and active
registry correction debt; its finding is preserved in
`corpus/lessons/round-15-verifier-spotcheck.md`.

**C1 coverage (capability acquisition):** acquire a bounded, read-only,
MESSAGE-free new-since-anchor journal observation for one explicitly named
scope and boot. The first retained record must reproduce the exact anchor
cursor bytes and boot; only subsequent same-boot records are observed.
Nearest seeks, missing anchors, boot boundaries and failed/truncated captures
remain unavailable, never a zero-event conclusion. No automatic cursor-state
mutation and no production census cutover are part of this claim.

Coverage **6** is the lowest owned non-retired axis versus operability **7**;
no stagnation waiver or score increase is claimed. The falsifiable metric is
the same finite committed CLI cases, capability absent at entering revision
versus delivered implementation: failed cases before → after, with actual
subprocess receipts and independently persisted input hashes. Absence is
capability red, not a historical production bug. A live field-limited
read-only observation demonstrates the accessible surface, not complete
retention, authenticated emitters, unique victims or universal ordering.

The old r10 drift baseline is preserved without re-pin; its existing red
status is not made green by this separate capability. Routed round-15
corrections are unclaimed conformance/learning work. L1 holds the canonical
planner seat; dispatched author-lane seats are not outside verification.

### Append-only corrections carried into round 16

- The round-14 vectors at the historical row above
  (`3/0/2/1/2/1` user and `2/1/4/3/0/2` system) are **fixture vectors**,
  not live positive load. This explicitly supplies the SCORECARD correction
  referred to by round-15 lesson M3; the original row remains unchanged.
- Round-15's author wording “pending non-author closure” is superseded by
  `corpus/lessons/round-15-verifier-spotcheck.md` at entering `b83edc6`:
  status ok/admitted true at its finite fixture scope, with procedural and
  active-registry debt. Admission did not authorize the prohibited checks.
- The r16 window binds records to its **anchor boot**, not necessarily the
  current host boot. Historical same-boot windows are permitted; no claim to
  cover the current boot, all entries to now, or complete journal access is
  made. A proposed current-boot pre-gate is rejected as a different scope.
- Static context checks verify instruction text, not runtime compliance.
  Repeated unauthorized seat probes/outside-lane writes and the
  ReviewCounts overwrite of the lesson are recorded in the round-16 lesson
  and excluded from acceptance evidence. No execution-conformance pass is
  inferred from a green static instruction check.

### Round-16 measured result

**C1 verified by L1 at its finite capability scope; outside closure pending.**
Measured committed inputs:
`87a57c13dbb1fc2d3e049bba98aca1739822b8c9`.
Before: the entering commit has no window tool (`frozen/entering-capability.json`
under round-16 waves). The gate records64 `capability_absent`, not64
historical production failures. After: **64/64 matched**, zero mismatches,
with30 OK/31 unavailable/3 setup cases. No distinct-bug count is inferred.

Executed counting command, exit0:

```sh
jq -s '[.[] | {verdict,total:.summary.total,matched:.summary.matched,capability_absent:.summary.capability_absent,mismatched:.summary.mismatched,unmet:(.summary.capability_absent + .summary.mismatched)}]' .ufo/waves/round-16/evidence/capability-before/run-manifest.json .ufo/waves/round-16/evidence/capability-after/run-manifest.json
```

Observed unmet capability requirements64→0; strict gate exits1→0.
Window selftest16/16, regression-gate selftest6 named arms, context
selftest15 arms all pass. Initial gate-setup failures and their same-command
repairs are retained, not hidden or counted as production red.
The original context check exits1 for the missing explicit live-journal ban;
the context-only corrected, **never dispatched** fixture exits0.

Both live scopes return `MORI_JOURNAL_WINDOW_OK` from one bounded read each,
with `records_after_anchor=0` and all four positive subsets0. These
anchor-only captures establish host-path reachability, not absence of events,
full store access or positive live load. Receipts, exact argv, input digests,
real HEAD and porcelain: `.ufo/waves/round-16/evidence/`.
Unchanged verdict-driving inputs, not a clean whole working tree, are claimed.

| Axis | Verdict | Active score | Evidence / limit |
|---|---|---|---|
| coverage | improved | 6 held | new exact-retained anchor-boot window capability; finite64/64 and live2/2 OK |
| operability | unchanged | 7 held | new gate selftests pass after actual setup repairs; prior production bytes unchanged |
| depth | unchanged | 5 held | S014/S015/S039/S040 support narrow mechanics, not a separate depth claim |
| freshness | unchanged | 5 held | old r10 pin and census bytes preserved; prior recorded red remains debt, no re-pin |
| calibration | unchanged | 5 held | capability absence versus defect red and fixture/live scopes separated; procedural nonconformance disclosed |
| adjacency | unchanged | 6 held | no census integration, orchestration or host remediation; unauthorized seat staging remains a violation, not expanded ownership |

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| exact-start journal record window | read one explicit scope after a byte-equal retained anchor, refusing unsafe captures without advancing state | `evidence/capability-after/run-manifest.json`, `evidence/live-window-{user,system}.json` under round-16 waves | 16 |

SOURCES38→40, A35→37/B2/C1 held, mined17→19/queued20/rejected1 held;
new rows S039/S040 and only S014/S015 used-by extensions. Both census
invocations exit0 with the existing W04 notices. Expansion improves through
the demonstrated FR11 capability; quality improves through corrected active
registry/source wording. Discernment stays unchanged: outside verification
is pending and repeated seat instruction breaches earn no improvement credit.

Operator wrap-up: wave1=64, wave2 skipped before validation/dispatch,
round total64. All64 reports are retained after relocating2 misrooted
reports byte-exact with cmp. No workers were spawned after wrap-up.
No next round is started; any further plan requires a fresh operator steer.

## Round 17 — declared claims and first-wave refinement

Entering branch tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb` (not bare HEAD).
Outside r16 closure admitted the bounded window with routed procedural defects;
`corpus/lessons/round-16-verifier-spotcheck.md` supersedes the pending language
above. No round beyond17 is executed here.

| Claim | Axis / score | Falsifiable before→after |
|---|---|---|
| C1 terminal-at-scan capability | coverage6 held | absent tool fails every committed synthetic requirement; delivered field-limited classifier must match them all, then run against actual transcripts with temporal/identity qualifications |
| C2 jj branch provenance | operability7 held | same real colocated sandbox assertions against entering versus delivered census; off-branch HEAD and ambient-author failures must disappear while controls remain green |
| C3 blind-sweep correction | calibration5 held | same retained `MoriR16.Lesson` artifact is missed by legacy pathspec sweep and found by no-pathspec filename-or-content sweep; missed known-artifact assertions1→0 |

Initial wave1 declared C1/C2 under the historical “lowest owned” reading.
`build/ScorecardAxisCheck.md` identified the literal all-six obligation. Before
L1 claim measurements, C3 was declared in `.ufo/waves/round-17/contract.md` using
the already-dispatched MisrootSweep item. Calibration5 satisfies the lowest
non-retired axis without a waiver. Depth5/freshness5/adjacency6 remain observed;
no scores are raised for fixture volume.

The claims are independent files/instruments: transcript tool, census, misroot
detector. The context checker and routed stale-wording fixes support learning,
not a fourth axis claim. S043 drives vendor429 cause precedence in C1; S046
drives status1-versus-error handling in C2. Finite fixtures do not certify
permanent seat death, universal jj behavior, current journal completeness or
remote publication. All admission measurements are recorded below after L1
execution on settled committed inputs.

### Round-17 measured claims (L1, before fresh falsification)

Measured committed branch input:
**273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7**. The branch-tip/input digest
ledger is `.ufo/waves/round-17/PINNED_INPUTS.json`; exact counting argv, rc and
stdout are `evidence/count-c{1,2,3}.json` under that round root.

| Claim | Before→after | Score delta | Verdict at measured finite scope |
|---|---|---|---|
| C1 coverage | unmet synthetic capability cases54→0; gates1→0; delivered54/54 match | 6→6 | improved; absent capability is not54 production bugs; live469 observations with94 aged rate-limit errors, not permanent deaths/incidents |
| C2 operability | failed real git/jj sandbox assertions21→0; matching cases7/12→12/12; gates1→0 | 7→7 | improved; local branch identity only, no remote publication or universal jj proof |
| C3 calibration | missed known exact root artifact assertions1→0; legacy false-clean0→candidate1 | 5→5 | improved; filename-only archived artifact found without a pathspec; candidate is not ownership proof |

Reproduction commands (lane root):

```sh
jq -s '[.[] | (.summary.capability_absent + .summary.mismatched)]' .ufo/waves/round-17/evidence/seat-before/run-manifest.json .ufo/waves/round-17/evidence/seat-after/run-manifest.json
jq -s '[.[].totals.failed_assertions]' .ufo/waves/round-17/evidence/jj-before/run-manifest.json .ufo/waves/round-17/evidence/jj-after/run-manifest.json
jq -s '[.[] | (.stdout|fromjson) | 1 - ([.candidates[]|select(.path=="MoriR16.Lesson")]|length)]' .ufo/waves/round-17/evidence/c3-before.json .ufo/waves/round-17/evidence/c3-after.json
```

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| terminal-at-scan seat observation | passively classify supported bounded transcript tails, distinguish aged errors/quotas/settle states and retain relative-path/prefix qualifications without content emission | `.ufo/waves/round-17/evidence/seat-after/run-manifest.json` (54/54); `evidence/seat-live.json`; `corpus/knowledge/seat-terminal-status-r17.md` | 17 |
| no-pathspec misroot witness | detect filename-only prior own-lane root artifacts while leaving sibling controls unclaimed | `evidence/c3-{before,after}.json`, `frozen/c3-expected.json` under round-17 waves | 17 |

Depth5/freshness5/adjacency6 held unchanged. Existing census125/125,
oracle28/28, r13 24/24, r14 44/44 and r15 63/63 with frozen red34/34 pass;
seven historical instruments/pin bytes unchanged. No re-pin makes r10 green.
Selftests and counts are L1 runs on settled committed inputs, not seat attestations.
Procedural violations remain disclosed in the lesson; static context checks are
not prevention. Fresh wave2 falsification and independent outside closure are
separate; neither is self-certified here.

### Current axis register (round17 supersedes frozen historical headers)

| Axis | Active score | Round17 role | Evidence |
|---|---:|---|---|
| coverage | 6 | C1 selected | finite transcript observation, source-linked FR14 advance |
| operability | 7 | C2 selected | branch-authority and real sandbox regression measure |
| calibration | 5 | C3 selected; lowest score | known false-clean misroot witness and grounded outside-r16 corrections |
| depth | 5 | observed, unchanged | S041–S048 and scoped knowledge notes |
| freshness | 5 | observed, unchanged | r10 red remains carried, no re-pin |
| adjacency | 6 | observed, unchanged | detection/report only, sibling ownership retained |

The top round1 table and original coverage+operability-only header are historical,
not the active score/selection register. Selecting calibration here adds no new
functional province. No axis is retired and no stagnation waiver is used.
Fresh wave2's three killed implementation mutants and one context survivor are
recorded honestly; A2 corrects the survivor and concrete source/guard/oracle
findings before final measurement. Initial54/21/1 counters are retained as
first-measurement evidence, not silently treated as final A2 instrument results.

### Round-17 final measured verdicts (supersede the weaker first instrument)

Final input ledger: `.ufo/waves/round-17/FINAL-PINNED_INPUTS.json`.
C1/C3 measured code commit **91940fa339e38006f8db5bd7d78bb6f037f4d016**.
C2 measured commit **fe9fa9083db998ead1554459d656568c4173f288**; its three
own input hashes are byte-identical at the final C1/C3 commit. Causal separation
is measured, not assumed. `final-measurements.json` records each pin and unit.

| Claim | Final before→after | Score delta | Counting receipt |
|---|---|---|---|
| C1 coverage | unmet synthetic requirements **66→0**, delivered **66/66**; same expected table, **96** source-file pins; entering `24526ea` has no tool (cat-file rc128) | 6→6 | `evidence/final/count-c1.json` rc0; gate exits 1→0 |
| C2 operability | failed assertions **60→0** over the same **204** assertions; matched cases **7/17→17/17** | 7→7 | `evidence/final/count-c2.json` rc0; gate exits 1→0 |
| C3 calibration | missed exact archived artifact **1→0**, unexpected candidates **0→0**; tracked token-bearing and sibling controls unclaimed | 5→5 | `evidence/final/count-c3.json` rc0; strict pinned controls all match |

```sh
jq -s '[.[] | (.summary.capability_absent + .summary.mismatched)]' .ufo/waves/round-17/evidence/final/seat-before/run-manifest.json .ufo/waves/round-17/evidence/final/seat-after-fixed/run-manifest.json
jq -s '[.[].totals.failed_assertions]' .ufo/waves/round-17/evidence/final/jj-before/run-manifest.json .ufo/waves/round-17/evidence/final/jj-after/run-manifest.json
jq -c '.missed_unexpected' .ufo/waves/round-17/evidence/final/c3-assertions.json
```

C1 absence is capability red, not 66 historical production defects. The
implemented prototype fails eight stronger expectations; the delivered tool
matches all 66 after an independent 65/66 metadata failure was repaired without
changing the fixture. C2's earlier 21/0 counts used a weaker conditional
denominator; 60/0 under a constant 204 is the final comparable measure.
C3 after rc1 means the probe correctly found its known candidate, not a failed gate.

| Axis | Final L1 verdict | Active score | Evidence / qualification |
|---|---|---:|---|
| coverage | improved | 6 held | finite C1 66/66 and 469 actual transcript observations; no permanent-death, complete-retention or incident-count claim |
| operability | improved | 7 held | C2 17/17 with young/sidebranch/unresolved-mirror controls; fixed guard/context/oracle failures retained |
| calibration | improved | 5 held | C3 independent precommitted witness/control pins and exact candidate sets; r16 disagreements learned as Q43–Q50 |
| depth | unchanged | 5 held | primary sources support bounded claims, no separate depth score |
| freshness | unchanged | 5 held | stale pending/version wording superseded; old r10 red retained, no re-pin |
| adjacency | unchanged | 6 held | detection/report only; OS/routing/cleanup ownership preserved; procedural deviations disclosed, not compliance credit |

Final demonstration pointers for the round-17 capability rows:
`evidence/final/seat-after-fixed/run-manifest.json`, canonical-redacted
`evidence/final/seat-live-final.json`, and `evidence/final/c3-assertions.json`.
They supersede earlier round-17 demonstration pointers, not their retained bytes.
Census selftest 134/134, terminal 49 arms, other named selftests, oracle 28/28,
r13 24/24, r14 44/44 and r15 63/63 (frozen red 34/34) pass. The two actual L1
failures remain in the lesson and receipts. Source census final rc0; all 134
reports delivered, 0 reported dead, no replacements or new L0 question.

No promotion or non-author admission is self-certified. Planned work is only
the completed steered round-17 scope; any next claims require a new external steer.

## Round 18 — recovery attempt 2: repair the round-17 privacy harm, freeze-order, dispatch binding

Entering `d005cdd` (r17 closure rejected-harmed, adjacency). Requirement freeze `29b0dc7`
precedes first implementation `b8f5c6c`. Measured commit **3127c3a0aec48f41bbae3700b6bbaa13b759797a**.
Waves: w1 68 seats (15 dead on provider capacity), w2 67 seats (0 dead); round total 135.

| Claim | Axis | Before (rev) | After (3127c3a) | Counting command | L1 verdict |
|---|---|---|---|---|---|
| C1 retention (sourced S049–S052) | adjacency | 116 unallowlisted, routed 40 (`d005cdd`, population_match true) | 0, routed 0, 86 allowlisted name-only rows, 0 forbidden | `python3 tools/mori-retention-gate.py scan --repo . --rev <rev> --policy .ufo/waves/round-18/frozen/c1-policy.json [--allowlist corpus/evidence/retention-allowlist.json]` | metric improved; axis-level adjacency **not self-certified** (wave-2 critics: residual out-of-metric context; see `.ufo/waves/round-18/out-of-metric-triage.md`) |
| C2 freeze-order | calibration | r17 overclaims 1 (+3 r18 no-implementation at `29b0dc7`) | 0; r17 3/3 `co-evolved` = closure; r18-C1..C3 `pre-build` | `python3 tools/mori-freeze-order.py check --repo . --register .ufo/waves/round-18/frozen/c2-register.json --corrections corpus/evidence/freeze-register.json --tip-for r18-C{1,2,3}=<rev>` | improved narrowly (historical relabel + prospective pre-build) |
| C3 dispatch ledger | operability (capability) | r17 legacy 9/9 unbound | r18 w1 1/1, w2 2/2, residual 7/7 bound (residual ledger `STARTED_MISSING`) | `python3 tools/mori-dispatch-ledger.py verify --repo . --rev <rev> --ledger <file>` | capability acquired; not a same-population improvement |

| Axis | Verdict | Score | Note |
|---|---|---:|---|
| adjacency | improved at frozen-class scope; residue contested | 6 held | outside closure decides harm |
| calibration | improved narrowly | 5 held | |
| operability | improved (capability) | 7 held | selftests 21/21, 12/12, 14/14 |
| coverage, depth, freshness | unchanged | 6/5/5 held | r10 drift red carried, no repin |

Capabilities: retention gate (C1), freeze-order check (C2), dispatch-attempt ledger verify (C3) —
evidence `.ufo/waves/round-18/evidence/{c1-after,c2-after,c3-after-*}.json`, first working round 18.

## Round 19 — declaration and round18 outside-closure correction

Author `mori19attempt2`; entering tip `b3602869dadd4016675aeba8db2adf3fa1e1b531`.
Frozen requirements/oracle `5e393d20daa628a0b4ca9aa6a1626aa54285b3f0`.
C1 adjacency6 held: acquire a bounded content-review coverage gate; C2
calibration5 held (lowest tie): intrinsically bind freeze receipts to exact inputs.
No axis retirement or stagnation waiver. Missing capability/metadata is not a
historical production defect. Other active scores remain coverage6, operability7,
depth5 and freshness5; r10 drift red is carried without re-pin.

The round18 outside closure supersedes the preceding author qualification cells:
adjacency **improved** (r17 harm cured at committed tip), calibration **improved**
(one historical relabel plus three prospective verifications), operability
**improved** (dispatch-binding capability); all other axes unchanged.
Its trends are **unchanged / unchanged / improved** (expansion / quality /
discernment). Census additions were A9/B1/C5. These are corrections, not
round19 growth. Evidence: `corpus/lessons/round-18-verifier-spotcheck.md:39–181`.

### capabilities: round18 table-shape repair

| Name | What it can now do | Evidence pointer | First-working round |
|---|---|---|---:|
| Retained-context class gate | Scan every committed blob against frozen R1–R9 with explicit non-author/allowlist qualification; never emit matched text | `.ufo/waves/round-18/evidence/c1-after.json`, selftests in `evidence/final-selftests.txt`; independent closure C1 | 18 |
| Freeze-order labels | Distinguish pre-build, co-evolved, absent and no-implementation from Git order, with appended effective-label corrections | `.ufo/waves/round-18/evidence/c2-after.json`; independent closure C2 | 18 |
| Dispatch-attempt binding | Verify exact payload bytes/digests separately from whole-ledger sequencing and started-row requirements | `.ufo/waves/round-18/evidence/c3-after-wave1-attempts.json`, `c3-after-wave2-attempts.json`; refused-only residual failure retained | 18 |

### Round19 measured claims — bounded capability, not privacy clearance

Final same-instrument measurement:
**11795ac0e0a44db6549534eb1239e26353446370**.
The six-script final suite ran at
`c0fe0b230769ffba7168955f87985ec3ce08f41d`; all six tested script blobs
are byte-identical at the final measurement (`evidence/final-stability-coda.json`).
The corrected harness was actually exercised in both modes at the final revision.

| Claim | Axis / held score | Observed before→after | L1 verdict / qualification |
|---|---|---|---|
| C1 content-review coverage capability | adjacency6→6 | 10 absent-tool requirements→0 unmet; 10/10 matched after | improved, capability scope only. Actual194-path review fails closed: 43 content-reviewed,151 provenance-only,155 unresolved dispositions; exit1, not clearance. |
| C2 intrinsic freeze receipt provenance, sourced S064 | calibration5→5 (lowest tie) | 10 missing metadata assertions→0; matched2/12→12/12, plus4/4 binding controls | improved. Before failures derive from actual CLI responses, not a mode assumption. Existing six historical verdicts remain equal. |

Actual counting commands, lane root:

```sh
jq -s '[.[].c1.counts.capability_absent]' .ufo/waves/round-19/evidence/finite-before-observed.json .ufo/waves/round-19/evidence/finite-after-observed.json
# [10,0]
jq -s '[.[].c2.counts.capability_absent]' .ufo/waves/round-19/evidence/finite-before-observed.json .ufo/waves/round-19/evidence/finite-after-observed.json
# [10,0]
jq -s '[.[].c2.counts.pass]' .ufo/waves/round-19/evidence/finite-before-observed.json .ufo/waves/round-19/evidence/finite-after-observed.json
# [2,12]
```

Receipts are `evidence/count-C1-command.json`, `count-C2-command.json`,
`count-C2-matched-command.json`; every named round19 evidence path is beneath
`.ufo/waves/round-19/`. A missing capability is not ten prior production bugs.
The r18 replay's raw4→0 remains one historical correction plus three prospective
labels, not a new round19 four-defect improvement. Intrinsic replay metadata and
original semantic parity are in `evidence/c2-historical-binding-wrapper.json`.

| Axis | Score held | Round19 verdict | Evidence / boundary |
|---|---:|---|---|
| adjacency | 6 | improved | C1 capability passes its finite requirements; actual unresolved review remains red; no history/privacy-completeness claim |
| calibration | 5 | improved | C2 exact input/script/revision receipts and actual before counter; outside admit/reject sample agrees |
| coverage | 6 | unchanged | retrospective index repair, no newly covered observability ground |
| operability | 7 | unchanged | existing census134/134; new tools credited only to their declared axes |
| depth | 5 | unchanged | bounded Git-resolution source support, no separate depth score |
| freshness | 5 | unchanged | recorded r10 red retained, not re-pinned or re-evaluated as green |

### capabilities: first demonstrated round19

| Name | What it can now do | Evidence pointer | First-working round |
|---|---|---|---:|
| Bounded content-review coverage gate | Bind every declared population blob to exact review evidence and reject missing, stale, unresolved or provenance-only clearance | `evidence/finite-after-observed.json` C1 10/10; `content-population-final-command.json` real194-path negative result | 19 |
| Input-revision-bound freeze receipts | Match loaded register/correction bytes to an explicit commit, retain full resolved claim identities and executing-code provenance | `evidence/finite-after-observed.json` C2 12/12 plus4/4; `c2-{before,after}-replay.json` | 19 |

Trends: expansion **unchanged**, quality **unchanged**, discernment **improved**.
Repair/index/source-row volume is not new covered-ground knowledge. Main's
non-author S064-admit/S065-reject agreement and lesson-backed criteria support
discernment; author-side falsifiers do not replace that check.
No subsequent round is initiated or claimed; this planned scope is round19 only.

## Round 20 — classified drift re-pin (freshness) and per-seat wave settlement (coverage)

Author L1 MoriR20; entering tip `2061780117e6ca637725004897bd288d3ba7e988` (round 19 admitted).
Frozen contract/cases `e4d9384` precede the first implementation `2eeae04`. Active scores entering:
coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. Lowest non-retired tie
depth/freshness/calibration at 5; freshness selected (calibration chosen rounds 17–19; freshness
last moved round 10). No retirement, no stagnation waiver. Sourced claims: C1 S066/S067, C2
S068/S073/S074 (S073/S074 supersede S069/S071). Measured commit: the round-20 final lane tip named in the
report (tool and register bytes are unchanged after it).

| Claim | Axis / score | Before → after | Counting command (lane root) | L1 verdict |
|---|---|---|---|---|
| C1 classified re-pin | freshness 5 held | unclassified r10-drift tokens **8 → 0** of 50 (entering) and 7 → 0 of 49 (pre-pin 10:51Z); 0 census-regression; new baseline `corpus/evidence/baseline-r20-20261021T1051Z.json`, post-pin drift `none` rc 0 | `export LC_ALL=C; comm -23 <(tr ' ' '\n' < DRIFT \| grep -v '^MORI_DRIFT:$' \| grep . \| sort -u) <(/usr/bin/jq -r '.tokens\|keys[]' REG \| sort -u) \| wc -l` → `.ufo/waves/round-20/evidence/c1-count.json` | improved; two disappearance tokens carry recorded dissent (`blind_spot`) |
| C2 wave-settlement scan | coverage 6 held | independent oracle `capability_absent` **14 → 0**, matched 0 → 14; live r19 W1 16/64 partial | `/usr/bin/jq -s '[.[].counts.capability_absent]' .ufo/waves/round-20/evidence/c2-before.json .ufo/waves/round-20/evidence/c2-after.json` → `[14,0]` | improved (capability; not 14 historical defects) |

The frozen contract's C1 command set `LC_ALL=C` on `comm` only and miscounts under
`en_US.UTF-8` (37/33; wave-2 DraftLog/DraftScorecard); the corrected command exports it for the
whole pipeline. Frozen bytes unchanged.

| Axis | Verdict | Score | Evidence / boundary |
|---|---|---:|---|
| freshness | improved | 5 held | first re-verification of every drift token since r10 with evidence, stale baseline replaced; stability window of a live pin is minutes–hours (`corpus/knowledge/drift-repin-r20.md` §4) |
| coverage | improved | 6 held | per-seat settlement over 21 lanes / 196 dispatch files; FR3 partially to Core; dispatch authenticity and hygiene stay Frontier |
| operability | unchanged | 7 held | census selftest 134/134, silence oracle 28/28, census bytes unchanged; new tool credited to coverage only |
| calibration | unchanged | 5 held | dissent recorded rather than resolved by the author; QUALITY 64–68 are lesson-backed, no scalar credit |
| depth | unchanged | 5 held | sourced notes support the two claims; no separate depth claim |
| adjacency | unchanged | 6 held | kumitate result semantics and souji cleanup untouched; seat scope breaches disclosed, no credit |

### capabilities: first demonstrated round 20

| Name | What it can now do | Evidence pointer | First-working round |
|---|---|---|---:|
| Per-seat wave settlement scan | Count declared members vs non-empty report files (stub/misrooted/unsafe distinguished) for every dispatch file of a lane or the fleet, without emitting report bytes or calling a seat dead | `.ufo/waves/round-20/evidence/c2-after.json` (14/14), `c2-live-mori.json`, `c2-live-fleet.json`; `tools/mori-wave-settlement.py --selftest` 22/22 | 20 |

Trends (author proposal; outside closure decides): expansion improved (two admitted knowledge
entries citing mined rows; the settlement note is uncovered FR3 ground), quality improved (the
stale r10 behavioral reference re-verified token-by-token and superseded by a stronger classified
pin), discernment improved (Main non-author agree S068 admit / S072 reject; S069 corrected by S073).
No promotion or subsequent round is claimed.

Wave-2 corrections folded before landing (`.ufo/waves/round-20/falsify/`): register classes are now
26 schema / 19 live-state / 5 roster / 0 regression (FamRosterLanes); tool refinements R7 (in-lane `..`)
and R8 (symlinked parent) plus a vocabulary guard on every selftest case kill the surviving mutants
(MutTraversalAllowed, VocabFleet mutant A); final tool selftest 23/23, oracle 14/14
(`evidence/c2-final-selftest.txt`, `c2-after.json`, `c2-live-mori-final.json`, `c2-live-fleet-final.json`).
Sources S073–S076 supersede over-reaching S069/S071/S070/S067 teaches. Open disagreement for the
outside closure: WATCHDOG_STALE / WAVE_UNSETTLED_AGE class (K2/K3 dissent, AdjudicateWaves BROKEN).

## Round21 — repair the round20 rejection, not a silent re-pin

Entering branch e9f340ce986f82a60baad1b8e5ead655ab818a1c.
CloseMori20's non-author closure supersedes the preceding round20 author
verdicts: freshness **harmed**, calibration **harmed**, coverage improved;
operability/depth/adjacency unchanged. Round20 admission false. Trends:
expansion improved, quality unprovable-but-better, discernment harmed.
The r20 baseline and register remain historical bytes, **invalid for
baseline acceptance**. QUALITY69 supersedes67; this is not a re-pin.

### planned: steered round21 only

| Claim | Axis / held score | Falsifiable move | Frozen evidence |
|---|---|---|---|
| C1 retained disappearance accounting | freshness5→5 (lowest tie) | 2 omitted historical observation identities→0 omitted, explicitly retaining2 unresolved; no disposition invented and pin remains blocked | `.ufo/waves/round-21/contract.md`, `frozen/required.json`, baseline:26-27; requirements3b792db |
| C2 evidence-loss-first permission | calibration5→5 (lowest tie) | same evaluator reads old/new rules against unchanged six cases; old cause-only permission mismatches2, new must mismatch0 | `frozen/cases.json`, `frozen/before-rule.json`, `frozen/after-rule.json` under round21 waves; freeze3b792db |

Those are target expectations, not measured verdicts; exercised outcomes are
appended after integration. Other active scores coverage6, operability7,
depth5, adjacency6 held. No retirement, no stagnation waiver, no promotion.
Author expansion is not claimed for historical repair/source-row volume.
The round20 capability cell's22/22 is stale; actual final selftest was23/23
(round20 evidence/c2-final-selftest.txt and non-author C2_remeasurement).

Round21 provenance clarification (2026-10-21): C1's declaration was frozen
at3b792db; `frozen/required.json` and the actual retained accounting first
landed at8fed329636f53455ae2f53930c171c6186aff1fd, not3b792db. Only the
six policy cases and old/new rule objects carry the earlier freeze.
The empty before accounting is an explicit later reconstruction of the
absent representation at e9f340c, not bytes claimed to exist there.

### Round21 exercised outcomes — measured9fb1f911cfdd6061005c300795f44b1b45523897

| Claim | Axis / delta | Before→after | Verdict / boundary |
|---|---|---|---|
| C1 retained disappearance accounting | freshness5→5 held | omitted2→0 of exactly2 required identities; retained0→2, unresolved0→2, invalid0 both, pin_allowed=false both; audit rc1 both | improved evidence assurance, not settlement or positive authorization. Before is the explicit absent-representation reconstruction; actual entering path absence rc128 is retained. |
| C2 evidence-loss-first correction | calibration5→5 held | frozen synthetic mismatches2→0 of6; separately outside-adjudicated real loss/w24 sample mismatches1→0 of2 | improved bounded calibration: matches CloseMori20's outside ruling. Six synthetic cases establish consistency only; no raw-event discovery/authentication claim. |

Counting instrument (lane root; full argv and resolved input/code digests in
`.ufo/waves/round-21/evidence/final/measure-claims.json` and `claims-observed.json`):

```sh
python3 .ufo/waves/round-21/oracle-loss.py --tool "$PWD/tools/mori-evidence-loss.py" --root "$PWD" --required "$PWD/.ufo/waves/round-21/frozen/required.json" --before-accounting "$PWD/.ufo/waves/round-21/frozen/before-accounting.json" --after-accounting "$PWD/corpus/evidence/loss-accounting-r21.json" --before-rule "$PWD/.ufo/waves/round-21/frozen/before-rule.json" --after-rule "$PWD/.ufo/waves/round-21/frozen/after-rule.json" --cases "$PWD/.ufo/waves/round-21/frozen/cases.json" --revision 9fb1f911cfdd6061005c300795f44b1b45523897 --out OBSERVED.json
python3 tools/mori-evidence-loss.py classify --rule .ufo/waves/round-21/frozen/before-rule.json --cases .ufo/waves/round-21/outside-cases.json
python3 tools/mori-evidence-loss.py classify --rule .ufo/waves/round-21/frozen/after-rule.json --cases .ufo/waves/round-21/outside-cases.json
```

Outside runs exit1/mismatched1 then exit0/mismatched0 (`outside-before.json`,
`outside-after.json` under final evidence). CLI selftest114 assertions passes;
independent fixture original control11/12 rc1 intentionally rejects its
superseded positive permission, explicit trust-refinement12/12 rc0. Five
mutants in four probe families killed,0 survived/inconclusive; full synthetic
workspaces were archived and every member compared before cleanup.

| Name | What it can now do | Evidence | First-working round |
|---|---|---|---:|
| Retained-loss observation | Retain required disappeared identities, verify committed copy hashes and report missing/invalid/unknown states without authorizing a pin | final/claims-observed.json C1; selftest114; omission mutant; all under round21 waves | 21 |

Other axes coverage6/operability7/depth5/adjacency6 unchanged. No score
increase, promotion, independent settlement, positive-authorization capability
or privacy clearance. Retention floor4→4 identical inherited policy-copy
hits, rc1 both; still red. Final sources76→76, A62/B6/C8, mined42/queued25/
rejected9, validator rc0 both. Trends: expansion unchanged; quality improved
by explicit invalidation/retained evidence; discernment improved by learning
the outside disagreement and agreed source sample. Outside closure decides
admission. Planned scope remains the completed steered round21 only.

## Round22 declaration — receipt reconciliation, not clearance

L1 MoriR22; entering77a5bbe8a0b41dfbfd2546d024d36e294b814bd0.
R21 admitted by outside closure, without privacy clearance: retained raw95,
policy non-author-excluded5, scanner90, unallowlisted4 and0new. Original
permission control RED11/12 and both unknown dispositions remain debt.

One C1 **calibration capability**, score5→5 held (lowest non-retired tie
with depth/freshness); no saturation waiver or retirement. All other active
scores held coverage6/operability7/depth5/freshness5/adjacency6.
Before is capability absent at the entering revision, not24 production
defects. Target after:24 frozen requirements match, independently recounted
real95/5/90/4 receipt agrees while privacy_clearance=false.
Original declaration/source-file-exclusion mistake remains at df880b4;
corrected policy-membership meaning and independent v2 freeze landed
e2f549befaffa1c1301928191e1eecb6142c0dad before implementation.
Expected real input digests and values are frozen in
`.ufo/waves/round-22/frozen/expected-real.json`.

This is a declaration, not an exercised capability row or a result.
Actual counting commands, measured commit and verdict follow integration.
Sourced claim: S064 reopened only for commit-resolution semantics, with
Gate quote and source change log in `corpus/lessons/round-22.md`.
No frontier closure, promotion, privacy improvement or subsequent round.

### Round22 exercised outcome — measured da40bb20f81da125d798f73cd1653655be1255ca

Correction to the declaration above: `frozen/expected-real.json` was committed
with the implementation (8cb4afb), not pre-build; only the contract, correction,
v2 builder/oracle and requirements-v2 are freeze-bound (e2f549b, checked by the
driver against that commit).

| Claim | Axis / delta | Before→after | Verdict / boundary |
|---|---|---|---|
| C1 retention receipt reconciliation (capability, sourced S064) | calibration5→5 held | frozen24 capability_absent24→0, pass0→24 (same oracle, same inputs) | improved bounded calibration capability. Real r21 receipt reconciles exactly (exit0, receipt_match) as raw95 / policy non-author-excluded5 / scanner90 / unallowlisted4 (raw_not_allowlisted9), retention red, privacy_clearance=false; identity digests match, swapped twin rejected; contradictory entering receipt rejected (receipt_revision_conflict). |

Counting command (lane root):

```sh
python3 .ufo/waves/round-22/measure-round22.py --revision <REV> --output <ABSENT_DIR>
jq -c '[.before.capability_absent,.after.capability_absent,.after.pass,.all_claim_checks_pass]' <ABSENT_DIR>/summary.json
# measure3 at da40bb2: [24,0,24,true]
```

Exercised at da40bb2 (`.ufo/waves/round-22/evidence/measure3/`): CLI selftest
4/4; co-evolved refinement controls 52/52; 22 targeted mutants each killed on
their named rows, unmutated frozen+refinement controls green; all-arm output
safety true; current retention floor rc1, unallowlisted4, 0 new/0 missing,
same inherited identities; carried inputs byte-unchanged (census, retention
gate, evidence-loss tool, allowlist, loss accounting, r21 fixture runner and
original control, r20 baseline). Frozen R13–R21 are exit-level only; their
reasons rest on the co-evolved controls.

| Name | What it can now do | Evidence pointer | First-working round |
|---|---|---|---:|
| Retention receipt reconciliation | Recount a committed retention receipt's measured tree independently and report exact identity agreement, policy-membership exclusions and red state, never clearance | `.ufo/waves/round-22/evidence/measure3/summary.json`; `tools/mori-retention-reconcile.py --selftest` | 22 |

Other axes coverage6/operability7/depth5/freshness5/adjacency6 unchanged.
No score increase, privacy/history clearance, pin, disposition or promotion.
Open debt carried: four unallowlisted retention hits (policy copy under
round-20 falsify), original permission control RED11/12, two unknown
historical dispositions with baseline acceptance blocked. Trends (author
proposal; outside closure decides): expansion unchanged, quality improved,
discernment improved. No subsequent round.

## Round23 declaration — misleading-field cutover and quota-surface coverage

L1 MadoR22-2 (reused agent as mori L1); entering `1bfe708a170c877db3319060d0ab38771efe03ac`.
R22 admitted (MANIFEST rounds[427]): one bounded calibration capability at held score.
Full pre-registration: `.ufo/waves/round-23/contract.md`; frozen requirements and real
controls in `.ufo/waves/round-23/frozen/`, all landed before any implementation.

| Claim | Axis / held score | Falsifiable move | Frozen evidence |
|---|---|---|---|
| C1 remove misleading `raw_unallowlisted` (routed by r22 closure) | calibration 5→5 (lowest tie with depth/freshness) | `misleading_alias_runs` >0 → 0 and r23 oracle 25/26 → 26/26 (R01–R24 re-expressed, R25 schema v2/no alias, R26 raw complement) | `frozen/c1-requirements.json`, `oracle-rename.py`, `frozen/c1-expected-real.json` |
| C2 FR2 quota-surface probe (capability; sourced S077–S084) | coverage 6→6 | sealed independent fixture cases capability_absent → all match; real host exit0 `QUOTA_DISABLED` as frozen | `contract.md` §C2, `frozen/c2-expected-real.json`; cases/oracle sealed after wave 1, before implementation |

Targets, not results. Other scores held operability7/depth5/freshness5/adjacency6.
Open debt carried: 4 unallowlisted retention hits, permission control RED 11/12, two
unknown historical dispositions, baseline acceptance blocked, no privacy clearance.
No retirement, waiver, exploratory claim, promotion or subsequent round.

### Round23 measured disposition — C1 independent; C2 withdrawn/not admitted

| Claim | Measured before → deployed pinf3dc07c0 | Final disposition / held score |
|---|---|---|
| C1 calibration | original25/26→26/26; alias-bearing outputs8/18→0/18; schema-v2 outputs0/18→18/18 | retain exact two-change cutover, calibration5→5; supplementary guards are separate evidence, not extra original cases |
| C2 FR2 coverage | absent at1bfe708a; strict29/30 atf3dc07c0 (26/27 primary+3/3 supplemental);274/274 supplementary output predicates; direct real control matches | withdrawn from production/admitted surfaces after pinned96 completed; current capability absent, strict target unprovable/not admitted; coverage6→6, no Core/repertoire advance |

Original CaseEscapedSpace expected row and pre-sealed parent-ID rule remain unchanged
and contradictory; no narrowed denominator, exclusion, relabel or special-case.
Mocked permission-loss disproves the prototype's negative-association confidence;
primary sources disprove reading active-accounting tokens as enforcement evidence.
The former tool/note and all red measurements are byte-exact rejected evidence,
not a supported quota capability. Parent ordered withdrawal, not another experiment.

C1's exact source delta, same-instance replay, selftest4/4, and real r21 identities
are independent. The real accounting remains95raw/86allowlisted/5non-author/
90scanner/4in-scope-unallowlisted/9raw-complement, red, privacy_clearance=false.
R01–R26 are26 requirement IDs over18 cached invocations, not26 independent detections.
C22's supplementary comparison is tautological, not an exercised guard mutation;
W2's actual isolated alias-return mutation supplies separate sensitivity evidence.

No numeric score, promotion, lifecycle/health/baseline authority or subsequent round
is claimed. Operability7/depth5/freshness5/adjacency6 held. Original permission11/12red,
two historical unknown dispositions and blocked baseline acceptance remain. The
declaration's ordering means complete seal before production landing, not before
the explicitly permitted blind draft. Final withdrawal revision gets its own
measurement; neither a missing tool nor source-only correction is a C2 pass.

### Measured withdrawal revision

Pushed withdrawal `0d8f2d50eb85e0d4349b1045f01c04e57318cc1b` removes the production
quota tool/note/registry, not the frozen target. Exact exercised counting argv is in
`.ufo/waves/round-23/evidence/measure-withdrawal-invocation.json`:

```sh
TMPDIR=/fast/scratch/hyaku/mori-r23 /usr/bin/python -I .ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py --revision 0d8f2d50eb85e0d4349b1045f01c04e57318cc1b --seal 22772c10f6e3c1d8d3fe1b72083a6194e9f4e687 --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/evidence/measure-withdrawal
```

Executed once with an absent output directory and existing private TMPDIR. Reproduction
requires a fresh absent output/private scratch, not overwriting retained evidence.
Original C1 before25/26→after26/26; alias8→0, supplementary.pass=true,
real-control.match=true, identities exact, same source4599ee1a and mode100755.
C1 checks C16–C26/C35 pass independently. Full driver exit1 remains RED:
C07 expected quota addition, C15 quota presence, C34 strict C2 and C29/C30 real quota
control fail after withdrawal. Current C2 buckets are30capability_absent/0pass and
31capability_absent with real expectation; unmet0 is an absence bucket, NOT a pass.
No current quota real invocation was made; f3's earlier direct real match stays
historical. Source census exit0 at this revision; registry76→89, A62→75/B6/C8,
mined42→55/queued25/rejected9, only old S065 used-by changed.

Last retention-scanned evidence snapshot4994c0df54ee793c0c25c34d178729d42c045803:
`python3 -I tools/mori-retention-gate.py scan --repo "$PWD" --rev 4994c0df54ee793c0c25c34d178729d42c045803 --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`
actually exits1 RETENTION_FINDINGS, metric4, raw95/allowlisted86/non-author5.
Raw and unallowlisted identity multisets equal56ac3bad, new0/missing0; no permission
or unknown-loss control was rerun or cleared. Exact argv/streams are in
evidence/retention-floor-final.json; comparison is separate JSON. Later receipt/
forensic-packaging commits are not retroactively claimed scanned at this snapshot.

Capture limitation: frozen driver real-control filenames overwrite their own raw
command wrappers with parsed JSON. Semantic results/summary remain; exact original
stdout/stderr wrappers are unavailable for those controls. C1's original/supplementary
verdicts are not a claim of perfect evidence capture; see
evidence/harness-receipt-overwrite.json. No frozen fix or new C2 rescue run.

## Round 24 declaration (attempt 2, L1 MoriR24) — routed repair and system pressure

Entering tip `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130` (round 23 closure: rejected,
honest stop). Full contract: `.ufo/waves/round-24/contract.md`. Targets, not results.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 repair the four byte-checkable round-23 routed items | calibration 5 (lowest active, tied with depth and freshness) | no check exists; the new check at `c725aa37` is expected to report 3 of 4 held (no round-24 pre-call ledger) | `python3 -I tools/mori-routed-check.py --repo <lane> --rev <landed tip>` prints `"held": 4` of `"items": 4`, exit 0 |
| C2 system CPU, IO and IRQ pressure capability (FR12, sourced) | coverage 6 | `tools/mori-pressure.py` absent; no mori tool reads system CPU, IO or IRQ pressure | `python3 -I tools/mori-pressure.py --selftest` prints `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0, over cases landed before the tool |

Held and observed: operability 7, depth 5, freshness 5, adjacency 6. Routed item 5 is an
adjacency boundary without a byte predicate; it is reported, not counted. No retirement,
waiver, exploratory claim or promotion.


### Round 24 measured outcome (L1 MoriR24; measured at the landed tip named in the fleet report)

| Claim | Before | After (one command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 calibration, routed repair | `--round 23` at `c725aa37`: held 3 of 4, R4 red with 8 wave-1 ledger rows whose `at` precedes their dispatch commit (`evidence/c1-before-round23.json`); `--round 24` at `c725aa37`: held 3 of 4 (`no_round_ledger`) | `python3 -I tools/mori-routed-check.py --repo <lane> --rev <tip> --round 24` prints held 4 of items 4, exit 0 (compact JSON `"held":4`); timing mismatches 8 → 0 | improved, bounded: R4 repairs the binding clause of routed item 4 under lane-written times; R1–R3 are regression guards that held; calibration 5 → 5 |
| C2 coverage, system pressure capability | `tools/mori-pressure.py` absent at `c725aa37` (exit 128) | `python3 -I tools/mori-pressure.py --selftest` prints `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0, then `MATCHER: rejected 48/48 corrupted expectations` | improved: capability demonstrated; coverage 6 → 6 pending closure |

Supporting C2 evidence: cases landed at `f6a29702` before the tool at `6ee62487` (`tools/mori-freeze-order.py`
grades `pre-build`; the tool seat read the cases while building, so order is shown, not independence); live
bracket check 5 of 5 (`evidence/bracket-check-run.json`) plus wave-2 seat runs; wave-2 mutants on the frozen
cases: 10 killed, 6 survived (threshold edge, matcher, three grammar shapes, HIGH over PARTIAL); response landed
after the measurement and not counted toward the 12: matcher negative controls and a co-evolved
supplementary file (`PASS 7/7`). Sourced: S090–S096 opened this round; S097 rejected.
Census no-harm: `tools/mori-census.sh` byte-identical to `c725aa37`, selftest `PASS (134 cases, 134 passed,
0 failed)` before and after; all pre-existing `tools/*.py` blobs unchanged. Held: operability 7, depth 5,
freshness 5, adjacency 6. No retirement, waiver, exploratory claim or promotion.

### capabilities: first demonstrated round 24

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| one-shot system pressure read | read `/proc/pressure/{cpu,memory,io,irq}` once (or twice with `--interval`), report per-resource states, never zero for unavailable, system cpu `full` flagged undefined, irq `some` null, labeled-local threshold | `tools/mori-pressure.py --selftest` PASS 12/12; `.ufo/waves/round-24/evidence/bracket-check-run.json` 5/5; `.ufo/waves/round-24/w2/Mut*.md` | 24 |
| round-23 routed-item check | report whether the round-23 routed carry-forward items hold at a revision, and whether a round's dispatch payloads were committed before their recorded call times | `tools/mori-routed-check.py`; `.ufo/waves/round-24/evidence/c1-*.json`; `.ufo/waves/round-24/w1/BuildRoutedCheck.md` | 24 |


## Round 25 declaration (attempt 1, L1 MoriR25) — round-24 routed repair and harness job runway

Entering tip `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` (round 24 admitted). Full contract:
`.ufo/waves/round-25/contract.md` (landed `7634be75`). Targets, not results.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 repair round-24 routed defects D1–D4 | calibration 5 (lowest active, tied with depth and freshness) | `tools/mori-routed-r24.py` absent; expected `mismatches: 4` at `28b79d3d` | `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev <landed tip>` prints `"mismatches": 0` (`"held": 4` of `"items": 4`), exit 0 |
| C2 harness background-job runway capability (new ground, sourced) | coverage 6 | `tools/mori-job-runway.py` absent at `28b79d3d` (exit 128) | `python3 -I -B tools/mori-job-runway.py --selftest` prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0, over the 21 cases frozen at `7634be75` |

Held and observed: operability 7, depth 5, freshness 5, adjacency 6. No retirement, waiver,
exploratory claim or promotion.

### Round 25 measured outcome (L1 MoriR25; measured at the lane revisions named, before the report)

| Claim | Before | After (one command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 calibration, round-24 routed defects and the standing Axes table (A1–A5) | `python3 -I -B tools/mori-routed-r24.py --repo <lane> --rev 28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` prints `"items":4,"held":0,"mismatches":4`, hygiene red, exit 1 (`.ufo/waves/round-25/evidence/routed-r24-before-a5.txt`) | same command at `e06d4a02` (and at every later tip) prints `"items":4,"held":4,"mismatches":0`, hygiene held, exit 0 (`evidence/routed-r24-after-a5.txt`) | improved: four lane self-assessments that contradicted committed bytes (SCORECARD:1514 selftest output, the entry's "this section wins" banner, the lesson's `PASS 6/6` against SCORECARD:1521, the round-1 Axes table) now agree; calibration 5 → 5 pending closure |
| C2 coverage, harness background-job runway capability (sourced S098–S104, S112–S113) | `git cat-file -e 28b79d3d:tools/mori-job-runway.py` exits 128 | `python3 -I -B tools/mori-job-runway.py --selftest` prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0, over the 21 cases frozen at `7634be75` (blob `48df844a`) before the tool landed at `09f55b62` (`evidence/runway-selftest.txt` at `d3b7af2a`) | improved, bounded: capability shown running; live host run `RUNWAY_CLAMPED` (configured 200, clamp 100, effective 100, exit 1; `evidence/runway-live-run.txt`); coverage 6 → 6 pending closure |

Disclosed bounds on C2 (wave 2): the pre-A2 tool `09f55b62` also passes the frozen 21 while failing 14 of the
A2 forms, so the counted value measures agreement with the L1's 21 examples, not omp's YAML reading in general;
the A2 forms and the wave-2 mutant kills live in the co-evolved supplementary file (`PASS 24/24`, not counted).
The clamp is 100 in every upstream release that has the feature (wave-2 CriticC2Admission). The cases were written
by the L1 from the contract rules, not by a separate seat, and the tool seat read them while building.

### capabilities: first demonstrated round 25

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| harness background-job runway read | report the configured `async.maxJobs` from one settings file, the clamp and setting default compiled into the installed omp binary, the effective cap `max(1, min(clamp, base))`, and a verdict that never turns an unreadable, ambiguous or unparseable input into a number | `tools/mori-job-runway.py --selftest` PASS 21/21 (frozen) and PASS 24/24 (supplementary); `.ufo/waves/round-25/evidence/runway-live-run.txt`; `corpus/knowledge/harness-job-capacity-r25.md` | 25 |
| round-24 routed-defect and Axes-table check | report, from git objects only, whether the round-24 routed defects D1–D3 and the SCORECARD Axes table (D5) agree with committed bytes at a revision, plus a pycache hygiene row | `tools/mori-routed-r24.py`; `.ufo/waves/round-25/evidence/routed-r24-*-a5.txt`; `.ufo/waves/round-25/w1/BuildRoutedR24Tool.md` (41-case falsification battery) | 25 |

Held: operability 7, depth 5, freshness 5, adjacency 6. No retirement, waiver, exploratory claim or promotion.

Round-25 corrections from wave 2 (CriticC1Admission), appended before the report:
- The C1 count is two parts, not one 4 → 0 measurement: the A1 item set D1–D3 went 3 → 0
  (`evidence/routed-r24-before.txt`, `routed-r24-after.txt` at `e54b644b`), and D5, added by amendment A5 after that
  result was committed, went 1 → 0 (`routed-r24-after-a5.txt` at `e06d4a02`). D1 and D5 compare a SCORECARD row with
  repo state; D2 (a knowledge entry banner) and D3 (a lesson line; SCORECARD:1521 was already right) are lane
  self-records outside SCORECARD/SHONEN. SHONEN is not read.
- D5's pinned scores come from the lane's own round-24 declaration (`SCORECARD.md:1499-1506` at `28b79d3d`, "Targets,
  not results"). The round-24 closure states numbers only for calibration (5) and coverage (6); for operability, depth,
  freshness and adjacency it says "unchanged". The Axes-table note at lines 17–19 calls those lines
  "closure-admitted"; read it as "declared by the lane, with calibration and coverage confirmed by the closure". The
  round-1 table had also been declared historical in round 12 and round 17 (`SCORECARD.md:616-619`, `:1064-1077` at
  `28b79d3d`). D5 checks scores only, not evidence pointers or Last change text.
- The round-25 declaration above says "D1–D4"; after A1 and A5 the counted items are D1, D2, D3 and D5, with D4 a
  hygiene row.

## Round 26 declaration (attempt 1, L1 MoriR26) — FR10 userspace OOM killers

Entering tip `248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` (round 25 admitted, `MANIFEST.json` rounds[455]). Full
contract: `.ufo/waves/round-26/contract.md` (landed `28b04940`). Targets, not results. Rounds 23–25 each counted a
routed repair on calibration, so this round works a different frontier area (FR10, `PROVINCE.md:53`); the round-25
routed defects R1–R8 are hygiene or named debt, never a counted claim.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 supersede the stale FR10 host-state statements | freshness 5 (tied lowest active axis with depth and calibration) | contract C1 command at `248408f5` prints `stale_present=4`, `r26_entry=absent` (`.ufo/waves/round-26/evidence/c1-before.txt`) | same command at the landed tip prints `stale_present=0`, `r26_entry=present`; the r26 entry's `source:` line cites a SOURCES row opened in round 26 |
| C2 userspace OOM killer read capability (FR10, sourced) | coverage 6 | `git cat-file -e 248408f5:tools/mori-oom-killers.py` exits 128 (`evidence/c2-before.txt`) | `python3 -I -B tools/mori-oom-killers.py --selftest` prints `MORI_OOM_KILLERS_SELFTEST: PASS N/N`, exit 0, N = case count of `tools/fixtures/mori-oom-killers/cases.json` at its freeze commit, written by a seat other than the tool seat and committed before the tool |

Held and observed: operability 7, depth 5, calibration 5, adjacency 6. No retirement, waiver, exploratory claim
or promotion. No-harm check: lane retention scan 4 unallowlisted at `248408f5`
(`evidence/retention-scan-base.txt`); the landed tip must not exceed 4.

### Round 26 measured outcome (L1 MoriR26; measured at `327fbcca`, before wave 2)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 freshness, stale FR10 host-state statements | `bash .ufo/waves/round-26/count-c1.sh 248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` prints `stale_present=4`, `r26_entry=absent`, `r26_new_source_ids=0`, `r12_names_r26=0` | same script at `327fbcca` prints `stale_present=0`, `r26_entry=present`, `r26_new_source_ids=13`, `r12_names_r26=4` | improved, bounded to the four frozen phrases plus the superseding entry; freshness 5 → 5 held pending closure |
| C2 coverage, userspace OOM killer read (sourced S114–S126) | `bash .ufo/waves/round-26/count-c2.sh 248408f5…` prints `absent cases_commit=none tool_commit=none`, exit 2 | same script at `327fbcca` prints `freeze_order=ok`, `cases_changed_since_freeze=0`, `N=32`, `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, `exit=0` | improved, bounded: the count is agreement with 32 cases a separate seat wrote before the tool; coverage 6 → 6 held pending closure |

Uncounted, same change: r12 line 3 (recheck output dated), line 6 (`--kernel-oom` scoped to the master README; absent
from the installed 1.9.0), lines 14 and 18 (earlyoom unit state dated), README rows 34 and FR10. Not yet swept:
three `systemd 261` present-tense lines in `corpus/knowledge/journal-alarm-routing-r14.md:67-68,290,342` (wave-1
ScoutStaleSweep) — named debt.

### capabilities: first demonstrated round 26

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| userspace OOM killer read (earlyoom 1.9.0, systemd-oomd), bounded | from `systemctl show` and this boot's journal, report each killer's unit state, the earlyoom version string and its four startup thresholds, counts of earlyoom send, escalation, failed-kill, low-memory, process-group and dry-run send log lines for the current invocation, send lines of earlier invocations this boot, and the number of systemd-oomd kill notices this boot, with a `KILLER_ACTED` / `KILLERS_UNKNOWN` / `KILLERS_QUIET` verdict as in contract C2 and amendment A2. Counts are log lines, not processes killed. Known limits: for a running earlyoom, sends of an earlier invocation in the same boot are reported but do not change the verdict; counts with an incomplete scope are lower bounds; no logger-heartbeat check; previous boots are not read | `tools/mori-oom-killers.py --selftest` PASS 32/32 (frozen at `5b10649d`) and PASS 32/32 on `cases-supplementary.json`; `.ufo/waves/round-26/evidence/c2-live-run.txt`; `corpus/knowledge/userspace-oom-killers-r26.md` | 26 |

Held: operability 7, depth 5, calibration 5, adjacency 6 (retention scan 4 at `4dba9cc7`, equal to the entering
value). No retirement, waiver, exploratory claim or promotion.

## Round 26 corrections (routed R2 and R4 — hygiene, not a claim)

Append-only: the round-25 sections above are left as filed, and each statement corrected here is
named with its old text.

### R2 — the round-25 runway capability row is scoped, not absolute

Old text (`SCORECARD.md:1568`, round-25 capability row "harness background-job runway read", "What
it can now do" cell): "report the configured `async.maxJobs` from one settings file, the clamp and
setting default compiled into the installed omp binary, the effective cap `max(1, min(clamp,
base))`, and a verdict that never turns an unreadable, ambiguous or unparseable input into a number"

That clause is false as written and is withdrawn. What the tool does: it is a line grammar over ONE
block-style settings file, and it abstains (`RUNWAY_UNKNOWN`, exit 2) only on the malformed forms it
can name. On other spellings of the same setting it reports a number. Re-measured at the round-26
entering tip `248408f5` with the tool blob `239dd8be…` and the round-25 wave-2 differential probe
(307 generated configs, Bun 1.4.3 as the omp-side parser): 72 of 307 configs read a false 100
(`RUNWAY_DEFAULT`, exit 0) where omp's parser reads 50 — 62 from unrecognised `async` header
spellings (`&a async:` and `"\x61sync":`, 31 each) and 10 from child or root forms under plain
headers (`{maxJobs: 50}`, `!!str maxJobs: 50`, `&a maxJobs: 50`, `"max\u004aobs": 50`, the flow root
`{async: {maxJobs: 50}}` and the indented root); 12 more report a configured number omp's parser does
not read as that number, and 36 (21 + 15) report a number or the default for files omp's parser
rejects. The claim that holds: the tool reads a block-style single settings file — a column-0
`async:` key with a direct `maxJobs:` child — and abstains on the forms it can name. The defect is
routed (round-25 R1: make rule 1 abstain on any top-level form it cannot read the way omp does); the
fleet record already carries the scoped form (`MANIFEST.json` rounds[455] `capabilities_added[0]`:
"bounded to block-style configs (72 of 307 probe configs read a false 100, routed R1)"). Evidence:
`.ufo/waves/round-25/w2/ReviewRunwayCode.md` F1–F2; the entry
`corpus/knowledge/harness-job-capacity-r25.md` already marks the false number. The probe corpus and
script are not committed to the lane (round-25 R1 asks for that); the 72 figure was re-derived by
re-running the wave-2 seat's copy read-only against the tip tool blob.

### R4 — three residuals of the round-25 D5 rewrite

**R4a — the standing Axes table's operability row.** The row credited round 13 with the move to 7.
Round 13 closed `rejected-harmed` (`MANIFEST.json` rounds[13]: `admitted false`), so its
self-assessed 6 → 7 was never admitted, and 7 was first admitted in round 14 (rounds[14]:
`admitted true`, `verdicts.operability "unchanged"`; `SCORECARD.md:793` reads "7 held"). The row is
corrected in place (old and new text below).

Old (`SCORECARD.md:11`):

| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); held 7 in every round table since round 13 | round 13 (6 → 7) |

New:

| operability | 7 | census `--selftest` PASS (134 cases) before and after round 24 (`SCORECARD.md` round-24 measured outcome); held 7 in every round table since round 13, first admitted in round 14 (round 13 closed rejected-harmed) | round 14 (6 → 7; round 13's self-assessed 7 was not held) |

The score cell stays 7 (D5 pins it from `SCORECARD.md:1499-1506` at `28b79d3d`). The gate still
holds on this row text (replayed against the gate's own parser and predicates; the falsifier, Last
change `round 1`, turns D5 red with `axis_stale_round_1: operability`). If the standing table is
preferred to read "7 first admitted" rather than a move, the equivalent Last change cell is
"round 14 (7 first admitted; round 13's self-assessed 7 was not held)".

**R4b — the D5 note.** Old text (`SCORECARD.md:1584`, last line of the round-25 wave-2 corrections
bullet): "`28b79d3d`). D5 checks scores only, not evidence pointers or Last change text."

That sentence is wrong about the Last change cell. D5 checks two cells: the Score cell against the
pinned base scores, and the Last change cell for a stale `round 1` (round-25 contract A5: "no row's
Last change reads `round 1` unless its score equals its round-1 value"; `tools/mori-routed-r24.py:739-741`
implements it). It does not check the evidence-pointer cell. Corrected statement: "D5 checks the Score
cell and the Last change cell (no row's Last change may read `round 1` unless its score equals its
round-1 value); it does not check the evidence-pointer cell." This is why R4a lies inside the gate's
scope.

**R4c — the round-12 paragraph that describes the standing table.** Old text (`SCORECARD.md:620-621`,
round-12 section): "Correction to the score table at the top of this file (frozen at round 1; 4 of 6
pointers stale — STATE dossier §2): the table is left as filed; this section's scores supersede it.
Stale pointers:" (the pointer list continues at `:622-623`).

That paragraph is stale after the round-25 D5 rewrite (`e68855d5`), which replaced the standing
table: the table's scores are now the closure-admitted round-24 scores (`SCORECARD.md:1499-1506` at
`28b79d3d`; the note at `SCORECARD.md:17-19`), only three of the six Last change cells still read
`round 1`, and none of the four pointer strings it names at `:622-623` ("per-surface notes still
owed", "14/14", "no drift pin yet", "`progressing-weak` deferred") occurs in the standing table any
more. The scores it defers to are superseded too: that section's table (`:612-618`) reads
calibration 5 → 6 and operability unchanged 6, while the standing table holds calibration 5 and
operability 7. Superseding statement: the standing table is the round-25 D5 rewrite of the
closure-admitted round-24 scores; the round-1 pointer enumeration at `:622-623` is historical and no
longer describes that table.

### Round 26 wave-2 corrections to the capability row above (appended before the report)

- The `PASS 32/32` counted value certifies the pre-freeze behaviour only. The amendment-A2 behaviour
  (process-group, dry-run and earlier-invocation counts, suppressed lines, non-steady states, malformed timestamps,
  the journal readability probe) is pinned by no committed case file; it is shown by the committed detector inputs
  `.ufo/waves/round-26/evidence/a2-detectors/` and their outputs `a2-detectors.txt`.
- `KILLERS_QUIET` means no positive evidence in the killers readable in this boot; it is not zero kills. The
  committed live run shows the quiet path on one host only.
- Further limits found in wave 2: an inactive or never-started earlyoom with no send lines reads quiet; a journald
  suppression notice while earlyoom is stopped is not acted on; the unit-state and journal reads are not atomic;
  PID 1 records about the unit are skipped by the grammar, not filtered by the query.

## Round 27 declaration (attempt 1, L1 MoriR27) — OOM victim selection knowledge and the A2 case freeze

Entering tip `fc09f96c8036094bef06370dbb4b436edf96e6e3` (round 26 admitted, `MANIFEST.json` rounds[462]). Full
contract: `.ufo/waves/round-27/contract.md`. Targets, not results. No new tool this round (drift watch: a new
one-shot tool was the coverage claim in rounds 24–26).

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 how earlyoom and the kernel pick an OOM victim on this host, and the fleet's exposure (FR10, sourced) | depth 5 (tied lowest active axis with freshness and calibration) | `bash .ufo/waves/round-27/count-c1.sh fc09f96c…` prints `entry=absent new_rows_cited=0 skill_rows=0`, `C1=unmet`, exit 1 (`.ufo/waves/round-27/evidence/c1-before.txt`) | same command at the landed tip prints `C1=met`, exit 0: entry `corpus/knowledge/oom-victim-selection-r27.md` citing ≥3 mined rows S127+, and ≥3 `Round27` SKILL.md table rows citing it |
| C2 pin the ten round-26 amendment-A2 rules of `tools/mori-oom-killers.py` with frozen cases (routed D7) | operability 7 | `bash .ufo/waves/round-27/count-c2.sh fc09f96c…` prints `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | same command at the landed tip prints `C2=met`, exit 0: `cases-a2.json` (≥20 cases, all ten rule ids, written blind to the tool, unchanged since its freeze commit) `PASS N/N`, and the round-26 file still `PASS 32/32` |

Held and observed: freshness 5, calibration 5, coverage 6, adjacency 6. No retirement, waiver, exploratory claim or
promotion. No-harm check: lane retention scan 4 unallowlisted at `fc09f96c`; no landed tip may exceed 4.

Round-27 amendment W1 (before any C2 data): C2 is withdrawn, not narrowed. Its case-writer seat `WriteA2Cases` died at
spawn (`Error: No model selected.`), and the claim's substance is that seat's independence from the tool; dead seats
are never replaced. The round has one counted claim, C1. Routed D7 is carried as named debt
(`.ufo/waves/round-27/contract.md` "Amendment W1").

### Round 27 measured outcome (L1 MoriR27; measured at `0becc421`, before wave 2)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 depth, OOM victim selection on this host (FR10, sourced S127–S132) | `bash .ufo/waves/round-27/count-c1.sh fc09f96c…` prints `entry=absent new_rows_cited=0 skill_rows=0`, `C1=unmet`, exit 1 (`evidence/c1-before.txt`) | same command at `0becc4216f97e61f41a472bb6c66d2d781b9d9bb` prints `entry=present new_rows_cited=6 skill_rows=10`, `C1=met`, exit 0 (`evidence/c1-after.txt`) | improved, bounded: the counter checks shape only (wave-1 CriticC1Counter); the substance is the entry's six facts, each cited to a row opened this round or an existing row re-opened at identical bytes; depth 5 → 6 proposed, pending closure |
| C2 operability, A2 case freeze | `C2=unmet`, exit 1 | withdrawn before any data (amendment W1: the case-writer seat died at spawn) | none: not a counted claim |

Held: freshness 5, calibration 5, coverage 6, operability 7, adjacency 6. Retention scan 4 at every landed tip
(pre-commit scans of each batch; base 4 at `fc09f96c`). No retirement, waiver, exploratory claim or promotion.

## Round 28 declaration (attempt 1, L1 MoriR28) — carried row defects superseded and the A2 case freeze

Entering tip `6ebd518f10e53057da926353d99442d51267ccaf` (round 27 closed `rejected-honest-stop`: C1 depth verified, C2
withdrawn and so not verified). Full contract: `.ufo/waves/round-28/contract.md`. Targets, not results. A declared
claim is never withdrawn; a miss is reported as a miss.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 restore S096, S097, S101 to their first-published cells and supersede the eight carried row defects (S096, S097, S101, S127, S128, S129, S131, S140) with rows re-opened this round (routed 3, 4; sourced) | freshness 5 (tied lowest active axis with depth and calibration) | `bash .ufo/waves/round-28/count-c1.sh 6ebd518f` prints `row_identity=rows=144 changed=3 removed=0 bad=0`, `superseding=0/8`, `C1=unmet`, exit 1 (`.ufo/waves/round-28/evidence/c1-before.txt`) | same command at the landed tip prints `C1=met`, exit 0 |
| C2 pin the ten round-26 amendment-A2 rules of `tools/mori-oom-killers.py` with frozen blind cases (r26 D7, re-declared) | operability 7 | `bash .ufo/waves/round-27/count-c2.sh 6ebd518f` prints `a2_cases=0 a2_rules_covered=0/10`, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | `bash .ufo/waves/round-28/count-c2.sh <tip>` (hardened against r27 CriticC2Counter F1–F8, F11; committed before the cases) prints `C2=met`, exit 0 |

Held and observed: depth 5, calibration 5, coverage 6, adjacency 6. No retirement, waiver, exploratory claim or
promotion. No-harm check: the lane retention scan at the landed tip must not exceed its value at `6ebd518f`.

Round-28 amendment A1 (before any data; `.ufo/waves/round-28/contract.md` "Amendment A1"): the C1 counter was
hardened (teaches must differ, real `used-by` readers citing the new id, a Gate line per row, `readers_left=0`;
`rejected` accepted only for a row superseding a rejected row) and C1's scope widened to the live readers; the C2
field map pins `earlyoom.earlier_invocation_send_lines > 0` for A2-07. Amended C1 before at `6ebd518f`:
`superseding=0/8 readers_left=27`, `C1=unmet`, exit 1 (`evidence/c1-before-a1.txt`).

### Round 28 measured outcome (L1 MoriR28; measured at `6b695b02a28b5f7342b2cdaaa643c176839bf7db`, before wave-2 results)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 freshness, eight carried row defects superseded, three first-published rows restored, readers repointed (sourced S145–S152) | `count-c1.sh 6ebd518f` → `row_identity=rows=144 changed=3`, `superseding=0/8`, `readers_left=27`, `C1=unmet`, exit 1 (`evidence/c1-before-a1.txt`) | `count-c1.sh 6b695b02` → `row_identity=rows=152 changed=0 removed=0 bad=0`, `superseding=8/8`, `readers_left=0`, `C1=met`, exit 0 (`evidence/c1-after.txt`) | improved, pending closure: each new row re-opened against upstream bytes this round (Gate lines with sha256 in `corpus/lessons/round-28.md`); freshness 5 → 6 proposed |
| C2 operability, ten amendment-A2 rules pinned by 30 frozen blind cases | `count-c2.sh 6ebd518f` → `a2_schema=absent a2_cases=0`, `C2=unmet`, exit 1 (`evidence/c2-before-r28.txt`) | `count-c2.sh 6b695b02` → `freeze_commit=d21b8bd3`, `a2_cases=30 a2_rules_covered=10/10`, `a2_selftest=PASS 30/30`, `frozen32_selftest=PASS 32/32`, `C2=met`, exit 0 (`evidence/c2-after.txt`); first tool run after the freeze `evidence/c2-freeze-selftest.txt`; tool unchanged | improved, pending closure; operability held at 7 (case pinning strengthens an existing capability) |

Held: depth 5, calibration 5, coverage 6, adjacency 6. Retention scan at the landed tip in the last batch's receipts.
No retirement, waiver, exploratory claim or promotion. r25 R1/R5 carried (no landed change).

## Round 29 declaration (attempt 1, L1 MoriR29) — standing Axes table vs the closure record, and blind A2-07/A2-10 cases

Entering tip `7118f320a5ef18d20c1e361eff77db0e1a97b2d6` (round 28 admitted, MANIFEST `rounds[476]`). Full contract:
`.ufo/waves/round-29/contract.md` (amendments A1–A4 before data). Targets, not results. A declared claim is never
withdrawn; a miss is reported as a miss.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 the six `## Axes` rows agree with the admitted closure record (fleet MANIFEST `verdicts` at `63729047`) | calibration 5 (tied lowest with depth and freshness) | `bash .ufo/waves/round-29/count-c1.sh 7118f320 63729047` → `mismatches=11`, `C1=unmet`, exit 1 (`.ufo/waves/round-29/evidence/c1-before.txt`) | same command at the landed tip → `mismatches=0`, `C1=met`, exit 0 |
| C2 the A2-07 in-scope dry-run and A2-10 stamp-less shapes pinned by 24 frozen blind cases (round-28 routed defect 2; sourced S153–S155) | operability 7 | `bash .ufo/waves/round-29/count-c2.sh 7118f320` → file absent, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | same command at the landed tip → `C2=met`, exit 0 |

Held and observed: depth 5, freshness 5, coverage 6, adjacency 6. No retirement, waiver, exploratory claim or
promotion. No-harm check: lane retention scan metric at the landed tip not above 4 (base at `7118f320`, wave-1
RetentionBase).

### Round 29 measured outcome (L1 MoriR29; measured at `07b9a4b9045d178e833a5bc22eb278e299496dc4` and the tip receipts)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 calibration, Axes table vs closure record | `count-c1.sh 7118f320 63729047` → `mismatches=11`, `C1=unmet`, exit 1 (`evidence/c1-before.txt`) | `count-c1.sh 07b9a4b9 63729047` → `mismatches=0`, `C1=met`, exit 0 (tip receipt `evidence/tip-c1.txt`) | improved, bounded (counter holes carried: lesson M1); calibration held at 5 — no closure states 5 → 6 |
| C2 operability, blind A2-07/A2-10 cases | `count-c2.sh 7118f320` → file absent, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | `count-c2.sh <tip parent>` → `blind_violations=20`, `a2_r29_selftest=FAIL(exit=1)`, `C2=unmet`, exit 1 (tip receipt `evidence/tip-c2.txt`) | **miss** (Judge02 `unclear text`; Judge11–13 tool errors declined; A4 gate 20); the landed tool change fixes 10 judged cases fully, harm disputed (lesson) |

Held: depth 5, freshness 5, coverage 6, operability 7, adjacency 6, calibration 5. No retirement, waiver, exploratory
claim or promotion. Retention metric 4 (base 4).

## Round 30 declaration (attempt 1, L1 MoriR30) — invocation-scope decision table, round-29 residual and the disputed shape

Entering tip `58b61681a0e3f3b821a17d38a4e713ccd9921615` (round 29 closed `rejected-honest-stop`, MANIFEST
`rounds[483]`). Full contract: `.ufo/waves/round-30/contract.md` (`a66751b1`). Targets, not results. A declared claim is
never withdrawn; a miss is reported as a miss.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 how the oom-killers reader scopes an earlyoom invocation: a sourced decision table whose rows the tool reproduces (routed R6 knowledge half; sourced S156+) | depth 5 (tied lowest with freshness and calibration) | `bash .ufo/waves/round-30/count-c1.sh 58b61681` → entry absent, `C1=unmet`, exit 1 (`.ufo/waves/round-30/evidence/c1-before.txt`) | same command at the landed tip → `C1=met`, exit 0 |
| C2 round-29 residual cases pass (R4), the disputed active-unit shape pinned by blind frozen cases (R6), the blindness gate fixed with a self-test (R5) | operability 7 | `bash .ufo/waves/round-30/count-c2.sh 58b61681` → r29 file `FAIL 21/24`, new file absent, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | same command at the landed tip → `C2=met`, exit 0 |

Held and observed: freshness 5, calibration 5, coverage 6, adjacency 6. No retirement, waiver, exploratory claim or
promotion. No-harm check: lane retention scan metric at the landed tip not above its value at `58b61681`.

### Round 30 measured outcome (L1 MoriR30; measured before wave-2 results)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 depth, invocation-scope decision table (sourced S156–S160) | `count-c1.sh 58b61681` → entry absent, `C1=unmet`, exit 1 (`.ufo/waves/round-30/evidence/c1-before.txt`) | `count-c1.sh ee61010d` (blob `6c47dd03`) → `rows=13 rows_ok=13 new_ids=5 new_id_rows=13 excerpts_ok=5/5 skill_rows=4`, `C1=met`, exit 0 (`evidence/c1-after.txt`) | improved, pending closure; depth held at 5 (no closure states a move) |
| C2 operability, round-29 residual, disputed shape pinned blind, gate fixed | `count-c2.sh 58b61681` → r29 `FAIL 21/24`, file absent, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | `count-c2.sh 2ec25cc1` → r29 `PASS 24/24`, older `PASS 32/32 / 32/32 / 30/30`, `provenance=8/8 unselected=0`, `shape=8/4`, `r30_base_selftest=PASS 8/8`, `r30_selftest=PASS 8/8`, `gate_selftest=PASS`, `gate_mutants=4/4`, `scanned=4`, `blind_violations=1`, `C2=unmet`, exit 1 (`evidence/c2-after.txt`) | **miss**: the freeze gate flags `CaseR30a.md:105` (the brief's closing sentence parsed as a files-opened entry); the A2 version of the gate flagged the mandated godspeed skill path in all four writers (`evidence/gate-a2-prefreeze.txt`, amendment A3). Every other condition is met; lesson M5 |

Held: freshness 5, calibration 5, coverage 6, operability 7, adjacency 6, depth 5. No retirement, waiver, exploratory
claim or promotion. Retention metric 4 at the C1 batch (base 4). Tip receipts: `.ufo/waves/round-30/evidence/tip-c1.txt`,
`tip-c2.txt`, `tip-retention.txt` (receipts-only last batch).

## Round 31 declaration (attempt 1, L1 MoriR31) — watchdog identity decision table and the fixed blindness gate

Entering tip `a12c68ae81257fb6f918bb165bcb39c73f82d212` (round 30 closed `rejected-honest-stop`,
`corpus/lessons/round-30-verifier-spotcheck.md`). Full contract: `.ufo/waves/round-31/contract.md`, committed with both
counters, the C2 fixtures and the control scripts before any seat ran. Targets, not results. A declared claim is never
withdrawn, narrowed or amended after data; a miss is reported as a miss.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 how a pid probe can and cannot establish that the fleet watchdog is alive: a sourced decision table on FR5 ground (sourced S161+) | depth 5 (tied lowest with freshness and calibration) | `python3 .ufo/waves/round-31/count-c1.py a12c68ae` → `entry=absent`, `C1=unmet`, exit 1 | same command at the landed tip → `C1=met`, exit 0 (predicate P-C1, contract) |
| C2 the blindness gate parses the files-opened list and reports every forbidden entry: new lane tool `tools/mori-blind-check.sh` (routed D1) | operability 7 | `python3 .ufo/waves/round-31/count-c2.py a12c68ae` → `tool=absent`, `C2=unmet`, exit 1 | same command at the landed tip → `exact=16/16`, `C2=met`, exit 0 (predicate P-C2, contract) |

Held and observed: freshness 5, calibration 5, coverage 6, adjacency 6. No retirement, waiver, exploratory claim or
promotion. Controls (do-nothing and shortcut) for both counters are scored and committed before any seat runs:
`.ufo/waves/round-31/evidence/c1-controls.txt`, `c2-controls.txt`.

### Round 31 appended corrections to the round-30 measured outcome (routed D8; wave-1 DraftLogScorecardD7D8)

- **C1 tip-receipt correction (append-only; the historical row above is retained):** the row at `SCORECARD.md:1820` records the earlier `ee61010d` measurement (`new_ids=5 new_id_rows=13 excerpts_ok=5/5`). The later tip receipt `.ufo/waves/round-30/evidence/tip-c1.txt:1-2,16-18` measures the counter at parent `926ac1460c0b9a542725257870f530f98e94e4b1` and reports `rows=13 rows_ok=13 new_ids=4 new_id_rows=12 excerpts_ok=4/4 skill_rows=4`, `C1=met`, exit 0. Use the receipt values when describing the round-30 tip outcome; the C1 verdict remains met.
- **Frozen-contract consistency note (not a contract amendment):** condition 4's parenthetical at `.ufo/waves/round-30/contract.md:76-78` says the round-29 writer-wave check “reports 0.” Amendment A2 instead requires comparison with an exact expected set and exclusion of the 20 adjudicated false positives (`contract.md:170-172`). The gate documents nine expected `(file, rule)` reports (`check-blind-wave.sh:172-180`) and its self-test requires `scanned=8`, `blind_violations=9`, each expected pair exactly once, and none of the known false-hit paths (`check-blind-wave.sh:215-229`). The unqualified zero-report parenthetical is stale against that nine-report expectation; this note records the inconsistency without editing the frozen contract or claiming a gate rerun.

Round-31 amendment A1 (before any entry or tool was scored; `.ufo/waves/round-31/contract.md` "Amendment A1"): wave-1
critics showed cheap shortcuts meeting both frozen counters, so both predicates are tightened (conditions added, none
removed) and judged as P-C1-A1 (`count-c1-a1.py`, adds a committed non-author row judge) and P-C2-A1 (`count-c2-a1.py`,
adds 11 fixtures, bwrap isolation, randomized order and nonces). The original counters are reported beside them.
Correction to the C2 before cell above: at `a12c68ae` the counter prints `fixtures absent at revision`, `C2=error`,
exit 2 (`evidence/c2-before-base.txt`), not `tool=absent`, `C2=unmet`, exit 1; the tool-absent unmet state (exit 1) is
first measurable at the freeze `2124cbcd` (`evidence/c2-controls.txt`). Lesson `corpus/lessons/round-31.md` M1.

### Round 31 measured outcome (L1 MoriR31; measured at `d0cac478ecafa1eae4e155fa79343ab29a7bd086`)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 depth, watchdog identity decision table (FR5; sourced S161–S165, S167, S169–S174) | `count-c1.py a12c68ae` → `entry=absent`, `C1=unmet`, exit 1 (`evidence/c1-before.txt`); A1 controls all unmet (`evidence/c1-a1-controls.txt`) | `count-c1-a1.py d0cac478` → `rows=14`, `new_ids=12`, `gates_ok=12/12 copies_ok=12/12 fetch_ok=12/12`, judge `supported=13 supported_new=13 unsupported=[9]`, `skill_rows=6`, `C1=met`, exit 0; original `count-c1.py` also `C1=met` (`evidence/c1-after.txt`) | improved, pending closure; depth held at 5 (no closure states a move) |
| C2 operability, `tools/mori-blind-check.sh` (routed D1) | `count-c2.py 2124cbcd` (fixtures frozen, tool absent) → `exact=0/16`, `C2=unmet`, exit 1 (`evidence/c2-controls.txt`); at `a12c68ae` the counter exits 2 (lesson M1) | `count-c2-a1.py d0cac478` → `exact=27/27` in both bwrap runs, `answer_key_strings=none`, `C2=met`, exit 0; original `count-c2.py` → `exact=16/16`, `C2=met`, exit 0 (`evidence/c2-tip.txt`) | improved, pending closure; operability held at 7; C2 met under both predicates (lesson M5: P-C2-A1 alone would not catch a last-line-dropping tool) |

Held: freshness 5, calibration 5, coverage 6, operability 7, adjacency 6, depth 5. No retirement, waiver, exploratory claim
or promotion. After the measured revision: entry row 9 marked [INFERENCE] (judged unsupported; still counted
unsupported). Tip receipts: `.ufo/waves/round-31/evidence/c1-after.txt`, `c2-tip.txt`, `census-end.txt`,
`tip-retention.txt`.

## Round 32 declaration (attempt 2, L1 MoriR32A2) — live recheck of the mutable-URL source rows

Entering tip `641a6e86ecc60634d215c0a47ab86c47661abf86` (round 31 admitted, MANIFEST rounds[495]). Attempt 1 landed
nothing. Full contract: `.ufo/waves/round-32/contract.md`. It was committed with the population and the counter at
`29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4` (01:10:09Z), before any seat ran. This SCORECARD section is appended at round
end. Its declared cells copy that frozen contract and add nothing to it. Targets, not results.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 the 34 `mined` SOURCES rows whose URL is not pinned to a tag or commit are re-opened live, each with a committed copy, located quotes, a verdict and a bound non-author judgment; method sourced S175+ | freshness 5 (tied lowest with depth and calibration) | `python3 .ufo/waves/round-32/count-c1.py 641a6e86` → `rows_ok=0/34`, `new_ok=0`, `C1=unmet exit=1` (`.ufo/waves/round-32/evidence/c1-before.txt`) | same command at the landed tip → `rows_ok=34/34`, `new_ok>=1`, `C1=met exit=0` (predicate P-C1, contract) |

Held and observed: depth 5, calibration 5, coverage 6, operability 7, adjacency 6. No retirement, waiver, exploratory claim
or promotion. Controls: 14 runs from 7 control seats, scored under the frozen counter before any data seat. No negative
control printed `C1=met` (`.ufo/waves/round-32/evidence/c1-controls.txt`, committed `8ab61aff`).

### Round 32 measured outcome (L1 MoriR32A2; measured at `7766732a98795467d0541630e9707a7acba518e1`)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 freshness, live recheck of the 34 mutable-URL rows (sourced S175–S177) | `count-c1.py 641a6e86` → `rows_ok=0/34`, `new_ok=0`, `C1=unmet exit=1` | `count-c1.py 7766732a` → `recheck_rows=34 header_ok=True judge_ok=True judge_agree=34`, `rows_ok=34/34 verdicts={'current': 33, 'unreachable': 1}`, `new_ok=3`, `C1=met exit=0` (`.ufo/waves/round-32/evidence/c1-after.txt`) | improved, pending closure; freshness held at 5 (no closure states a move). Open: on the five multi-source rows the judge read `current` as "the part the population URL carries"; under a strict reading those rows fail R4 (`corpus/lessons/round-32.md`, Attacks) |

Held: depth 5, calibration 5, coverage 6, operability 7, adjacency 6, freshness 5. Mistakes M1–M3 in
`corpus/lessons/round-32.md`. M1: the contract's "last opened when added" sentence is false. The predicate does not read it.

## Round 33 declaration (attempt 1, L1 MoriR33) — reading /proc/diskstats as a disk write rate (FR6)

Entering tip `7d382043016e8854e3be2ee523a095b409c3d8a1` (round 32 closed `rejected-honest-stop`, MANIFEST rounds[498],
`corpus/lessons/round-32-verifier-spotcheck.md`). Full contract: `.ufo/waves/round-33/contract.md`, committed with the
counter at `27969134d51ea15982db4f36c77e2decd2a22b07` before any seat ran; Amendment A1 (code made to match the frozen
sentence and tightened after the C0 control wave, before any data seat) at `fdf4371fb6d5f7c4e8b1f29f4735afaead5d45c9`.
This section is appended at round end; its declared cells copy the frozen contract. Targets, not results.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 how to turn /proc/diskstats into a disk write rate: a sourced decision table on FR6 ground (sourced S180+), judged under the frozen rule R-J | depth 5 (tied lowest with freshness and calibration) | `python3 .ufo/waves/round-33/count-c1.py 7d382043` → `entry=absent`, `C1=unmet`, exit 1 (`.ufo/waves/round-33/evidence/c1-before.txt`) | `python3 .ufo/waves/round-33/count-c1-a1.py <landed tip>` → `C1=met`, exit 0 (predicate P-C1-A1) |

Held and observed: freshness 5, calibration 5, coverage 6, operability 7, adjacency 6. No retirement, waiver, exploratory
claim or promotion. Controls: wave C0 (5 seats) scored under the frozen counter before data; four negative controls met
it, so A1 was cut before data and every C0 control commit was re-scored under A1 (`.ufo/waves/round-33/evidence/c1-controls.txt`).
Anti-loop: rounds 31 (FR5 depth, operability) and 32 (freshness of source rows) are not repeated; FR6 is new ground.

### Round 33 measured outcome (L1 MoriR33; measured at `a193627c0a89e6aaca54b4b750f7f82e7249912a`)

| Claim | Before | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|---|
| C1 depth, FR6 disk write-rate decision table (sourced S180–S190) | `count-c1.py 7d382043` → `entry=absent`, `C1=unmet`, exit 1 | `count-c1-a1.py a193627c` → `rows=14`, `new_ids=11`, `gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11`, judge `supported=10 supported_new=10 unsupported=[3, 6, 7, 13]`, `skill_rows=6`, `C1=met`, exit 0; frozen `count-c1.py` also `C1=met` (`.ufo/waves/round-33/evidence/c1-after.txt`) | improved, pending closure; depth held at 5. Met exactly at the floor (10 supported); post-data control CtlGlossaryA1 shows a definition-only glossary can also meet P-C1-A1 with an honest self-judge (lesson, Attacks) |

Held: freshness 5, calibration 5, coverage 6, operability 7, adjacency 6, depth 5. Census end `mori ok`, exit 0, the
same 12 W04 lines (`evidence/census-end.txt`). Retention metric 4 at `62db24c0` = 4 at base. Routed round-32 defects
1–6 handled in `corpus/lessons/round-33.md` (Round-32 repair), with a non-author repair judge (JudgeRepairR32).

## Round 34 declaration and measured outcome (attempts 1–3; L1 MoriR34 / MoriR34A2 / MoriR34A3) — FR6 two-sample disk write-rate tool, QUALITY 98

Entering tip `f10a320d9056d19a6d007420df49d7b16a3bf857` (round 33 closed `rejected-honest-stop`). Contract
`.ufo/waves/round-34/contract.md` and `count-c1.py` frozen at `24603186` before any seat; Amendment A1 (`count-c1-a1.py`,
P-C1-A1) and the C0 control receipts at `b9fb029e`, before any data seat. Attempts 1 and 2 died with the orchestrator;
this section is written in attempt 3 and copies the frozen declared cells.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 FR6's two-sample write-rate arm as the tool operation `tools/mori-disk-rate.py` (P-C1-A1) | coverage 6 | `python3 .ufo/waves/round-34/count-c1-a1.py f10a320d` → `tool=absent C1=unmet`, exit 1 (`evidence/c1-before.txt`) | the same command at the landed tip → `C1=met`, exit 0 |
| C2 (exploratory) QUALITY criterion 98, the pre-data shortcut battery | calibration 5 (tied lowest) | round 33's nine pre-data controls had no no-decision control | no counting command; `unprovable-but-better` only with a named non-author reviewer |

| Claim | After (measured) | Verdict proposed for the closure |
|---|---|---|
| C1 | `count-c1-a1.py <tip>` → `fixed_pass=12/12 random_pass=300/300 coverage=ok live=ok C1=met`, exit 0 (L1, 06:47:48Z, `evidence/c1-tip-a3.txt`; tool byte-identical to `ba525e1a`); ExecCloneRerun 4/4 `C1=met` | **not verified (honest stop, §9)**: the post-data probe `ef936fb4`, which skips the real two-sample read and rule R3, also prints `C1=met` (`evidence/ctl-postdata-shortcut/rescore-a3.txt`, `wb/CritShortcutRescore.md`); CritQ99Gap built two more skip programs that meet it |
| C2 | QUALITY 98 (`corpus/QUALITY.md`, landed `8d56809a`) | `unprovable-but-better`, reviewer ReviewC2Judge3 (`.ufo/waves/round-34/wb/ReviewC2Judge3.md`); against: §8 item 1's second clause unanswered, D1/D2/D4, and the after-data shortcut (M2) |

Held: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. No score change, retirement or
waiver. Routed round-33 defects 2–8 landed and re-judged in attempt 3 (`corpus/lessons/round-34.md`): row 3r failed and
was superseded by 3r2 (supported); items 7 and 8 carry one wrong detail each, corrected in the lesson. QUALITY 99 for
mistake M2. SOURCES 190 → 198 rows.

## Capabilities

Round 35 (claim C1, calibration). This is the lane's current capabilities register, the `capabilities` field of the
AXES.md SCORECARD contract (S199). It holds one row per capability that a non-author closure admitted, as fleet
`MANIFEST.json` at fleet commit `37b51a24` records it (S200). The key is that closure's `rounds[i].capabilities_added[j]`;
the first-working round is the closure's round; the evidence is the artifact that round landed and the closure names.
Rows enter only through a round that demonstrates the capability running (S199), so the three capabilities of round 17,
a rejected round, are not rows. As the current self-assessment this register supersedes the `— none yet —` table in the
first `## Capabilities` section (left as filed at `d677cf3`) and the per-round capability tables, none of which listed
the admitted set. Check: `python3 .ufo/waves/round-35/count-c1.py <rev>` (predicate P-C1,
`.ufo/waves/round-35/contract.md`).

Rows that predate MANIFEST are not register rows: live census and census self-test (round 1), silence oracle (round 2)
and drift pin (round 10), in `## Capabilities (round 12 demonstrations)` above. They were admitted before MANIFEST
carried any mori `capabilities_added` key (its first keyed mori entry is `rounds[313]`, round 12): round 1 by the fleet
closure `rounds[140]`, rounds 2 and 10 by goal-wave verdicts with no named non-author verifier (this file's Round 2
and Round 10 verdicts). Their evidence pointers resolve at `dd76eb79`.

| key | capability | what it can now do | evidence | first-working round |
|---|---|---|---|---|
| `rounds[313].capabilities_added[0]` | source registry | Curates where mori learns: opened, tiered, anchored source rows with a search log; 34 rows with a clean contract-v1 census at the round-12 closure (the registry has grown since). | `corpus/SOURCES.md` | 12 |
| `rounds[339].capabilities_added[0]` | typed journal alarm and subject triage | Classifies structured failed-unit subjects as fleet, tsukuroi-routed or unresolved and raises one critical OOM journal alarm; the six named fixture failures went 6 to 0; no live-positive or exhaustive coverage proof. | `tools/mori-round14-regressions.py` | 14 |
| `rounds[345].capabilities_added[0]` | partial positive journal alarms | On finite committed fixtures, keeps individually qualified current-boot OOM and user-signal alarms beside invalid aggregate records, whose raw totals stay unavailable; no live positive load is claimed. | `tools/mori-round15-regressions.py` | 15 |
| `rounds[353].capabilities_added[0]` | exact-start journal record window | Reads one user or system journal scope after a byte-equal retained anchor cursor on the anchor's boot, MESSAGE-free, refusing unsafe captures as unavailable without advancing cursor state; 64/64 fixtures; live runs were anchor-only. | `tools/mori-journal-window.py` | 16 |
| `rounds[386].capabilities_added[0]` | retention gate | Scans lane revisions under the retention policy and reports metric and routed counts; selftest 21/21; after-metric 0 and routed 0 at 3127c3a. | `tools/mori-retention-gate.py` | 18 |
| `rounds[386].capabilities_added[1]` | freeze-order check | Checks frozen claim inputs against implementation history and counts overclaims; selftest 12/12; overclaims 4 to 0 at 3127c3a. | `tools/mori-freeze-order.py` | 18 |
| `rounds[386].capabilities_added[2]` | dispatch-attempt ledger verify | Verifies that dispatch attempts bind their payloads: round-18 wave 1 1/1 and wave 2 2/2 bound clean, residual 7/7 bound with STARTED_MISSING; selftest 14/14. | `tools/mori-dispatch-ledger.py` | 18 |
| `rounds[398].capabilities_added[0]` | blob-bound content-review coverage gate | Passes 10/10 frozen finite requirements; on the actual 194-path population it exits 1 with 155 unresolved dispositions, so it is not privacy clearance. | `tools/mori-content-review.py` | 19 |
| `rounds[427].capabilities_added[0]` | retention receipt reconciliation | Independently recounts the measured tree of a committed retention receipt and reports identity agreement and policy exclusions; accounting agreement only, privacy clearance always false. | `tools/mori-retention-reconcile.py` | 22 |
| `rounds[443].capabilities_added[0]` | one-shot system pressure read | Reads /proc/pressure cpu, memory, io and irq once per resource; unavailable is never zero, system cpu full is flagged undefined and irq some is null; frozen selftest PASS 12/12, six wave-2 survivors disclosed. | `tools/mori-pressure.py` | 24 |
| `rounds[443].capabilities_added[1]` | round-23 routed-item check | Checks the R1-R3 regression pins and R4 dispatch-before-call ordering over lane-written times; held 3 to 4; round-23 wave-1 timing mismatches 8, round-24 0 of 2. | `tools/mori-routed-check.py` | 24 |
| `rounds[455].capabilities_added[0]` | harness background-job runway read | Reads the configured async.maxJobs from one settings file plus the binary clamp and default, and reports the effective cap and a verdict (not a live job count); frozen selftest PASS 21/21; bounded to block-style configs. | `tools/mori-job-runway.py` | 25 |
| `rounds[455].capabilities_added[1]` | round-24 routed-defect and Axes-table check | Checks round-24 defects D1-D3 and D5 from git objects plus D4 hygiene; 4 to 0, re-measured by the closure with plain git reads; no registry row or selftest. | `tools/mori-routed-r24.py` | 25 |
| `rounds[462].capabilities_added[0]` | userspace OOM killer one-shot read | Reads earlyoom and systemd-oomd unit state, earlyoom startup thresholds, counts of earlyoom send, escalation, failed-kill and low-memory lines this invocation and oomd kill notices this boot; KILLER_ACTED, KILLERS_UNKNOWN or KILLERS_QUIET; counts are log lines, not processes. | `tools/mori-oom-killers.py` | 26 |
| `rounds[476].capabilities_added[0]` | SOURCES freshness repair | Superseded eight carried SOURCES row defects with re-opened rows S145-S152, restored S096, S097 and S101 to their first-published cells, and repointed the live readers. | `corpus/SOURCES.md`, `corpus/knowledge/oom-victim-selection-r27.md` | 28 |
| `rounds[476].capabilities_added[1]` | amendment-A2 frozen cases | Pins ten round-26 amendment-A2 rules of the OOM killer read with 30 frozen cases (freeze d21b8bd3), PASS 30/30; fixture-only, not a live-host result. | `tools/fixtures/mori-oom-killers/cases-a2.json` | 28 |
| `rounds[495].capabilities_added[0]` | blind-writer gate | Blind-writer gate with a passing --selftest; on the round-30 inputs it reports three missing-list hits and no longer flags CaseR30a.md:105; supersedes the round-30 wave gate (routed D1). | `tools/mori-blind-check.sh` | 31 |
| `rounds[495].capabilities_added[1]` | watchdog identity decision table | A sourced FR5 table (S161-S174) on what pid probes can and cannot establish about watchdog liveness; measurements used throwaway processes and did not change the census probe. | `corpus/knowledge/watchdog-identity-r31.md` | 31 |

## Round 35 declaration and measured outcome (attempt 1, L1 MoriR35) — capabilities register vs the closure record

Entering tip `dd76eb79` (round 34 closed `rejected-honest-stop`, MANIFEST `rounds[524]`). Contract
`.ufo/waves/round-35/contract.md` and `count-c1.py` frozen at `f2d28711` before any seat; pre-data control receipts
(wave C0, 12 seats) at `913df22e`; register landed at `721040a9`. The declared cells copy the frozen contract.

| Claim | Axis / score | Before | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 the last `## Capabilities` section binds each capability fleet MANIFEST@37b51a24 records under an admitted mori closure (18) to its key, round and a strong artifact, and holds no other row (P-C1); sourced S199, S200 | calibration 5 (tied lowest with depth and freshness) | `python3 .ufo/waves/round-35/count-c1.py dd76eb79` → `rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet`, exit 1 (`evidence/c1-before.txt`) | the same command at the landed tip → `matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met`, exit 0 |

| Claim | After (measured) | Verdict proposed for the closure |
|---|---|---|
| C1 | `count-c1.py cedb0ec4` → `rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met`, exit 0 (`evidence/c1-after.txt`; ExecTipRerun reproduced it in two fresh clones) | **not verified (honest stop)**: before data, control 10c (empty capability and what cells) met P-C1 and the L1 ruled it a residual instead of re-designing, against QUALITY 98's content-free shape (lesson M1); after data, the word-bag control also meets P-C1 (`w2/CtlWordBag.md`). P-C1 checks the binding, not the self-assessment's content. CritC1Verdict agrees (`w2/CritC1Verdict.md`) |

Held: calibration 5, coverage 6, operability 7, depth 5, freshness 5, adjacency 6. No retirement, waiver, exploratory
claim or promotion. Not claims: the register's rows were judged one by one by non-author wave-2 reviewers (lesson,
Judges); the Axes table's operability and depth `Last change` cells now name round 31 (`SCORECARD.md:11-12`); SOURCES
198 → 204 rows (S199–S202 admitted, S203–S204 rejected); QUALITY 98 correction and 100–102.

## Round 36 declaration and measured outcome (attempt 2, L1 MoriR36) — SOURCES append-only gate (C2, measured) and source-drift byte probe (C1, exploratory)

Entering tip `6bd57097` (round 35 closed `rejected-honest-stop`, MANIFEST `rounds[531]`). Contract
`.ufo/waves/round-36/contract.md` and both counters frozen before any data seat (v1 `da12b37`; v2 re-design after
C0 met-controls `c1a026cb`; pin record `evidence/freeze-v3.txt`). Attempt 1 died with the phase-4 orchestrator
(~09:30 -03) after committing the freeze, C0 receipts and wave-1 reports; attempt 2 inherited per addendum §5
(lesson M3), built the never-delivered C1 tool, landed the data commit `bf0df77`, scored both claims at that clean
tip, and dispatched wave 2 (66 seats, orchestrator-inline) whose documentary findings were repaired in the
integration commit.

| Claim | Axis / surface | Before (one command over committed bytes) | After (one command over committed bytes) |
|---|---|---|---|
| C2 — SOURCES append-only gate with deleted-row detection (capability acquisition) | operability — new registered gate `tools/mori-sources-appendonly.py` + fixture self-test | `python3 .ufo/waves/round-36/count-c2.py 6bd57097` → `tool_absent C2=unmet`, exit 1 (`evidence/c2-before.txt`) | `python3 .ufo/waves/round-36/count-c2.py bf0df77` → blind 24/24, real arm pass (18 ids), `C2=met`, exit 0, seed 15440749816798970567 (`evidence/c2-after.txt`); re-scored clean on 7 fresh draws (`w2/ExecReC2A.md`) and independently re-derived without the counter (`w2/RevC2Oracle.md`) |
| C1 — source-drift byte probe (exploratory, declared before data at `5842dc0`) | freshness technique (no freshness verdict admitted) — new probe `tools/mori-source-drift.py` | `python3 .ufo/waves/round-36/count-c1.py 6bd57097` → `tool_absent C1=unmet`, exit 1 (`evidence/c1-before.txt`) | `python3 .ufo/waves/round-36/count-c1.py bf0df77` → blind 40/40 mismatches=0, real arm fetched=58 fresh=49 drifted=9 excluded=0 mismatches=0, `C1=met` as byte-behavior evidence, exit 0, seed 7388485190103051243 (`evidence/c1-after.txt`) |

| Claim | Measured verdict |
|---|---|
| C2 | **verified (measured)**: the frozen counter fails all 25 v2 controls and 3+ substitute programs (c0 + w2 falsification), passes the gate at two fixed seeds and seven fresh draws, and its real-arm oracle was re-derived byte-identical by a seat that never read the counter. Gate registered with self-test (r35 spotcheck §6 items 2–3 discharged; 18 in-place ids superseded by S205–S220, `round_changed=[]`). |
| C1 | **unprovable** (as declared before data): the byte predicate cannot carry a freshness verdict (w1 `CritAxisFit.md`; QUALITY 105). No named non-author reviewer exists inside the round; the hyaku closure session is the reviewer of record — its `unprovable-but-better` judgment would admit the technique, otherwise the honest `unprovable` stands. The probe, its byte evidence, the nine-row dated enumeration and the S210/S211 reader-action classes land regardless. |

Capabilities register — row added this round (demonstrated running above):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-36 C2 | sources append-only gate | Reports in-place immutable-cell edits, deleted rows, superseders and per-round changed ids of `corpus/SOURCES.md`; `python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>` exits 0 iff the round changed no immutable cell | `tools/mori-sources-appendonly.py`; `evidence/c2-after.txt`; `--selftest` 8/8 | 36 |

Planned round 37: (1) r37 debt from the disclosed residuals — restructure the frozen counters' timeout path to
avoid SIGKILL of the sandbox child (requires a counter re-freeze, so a new claim), and a C2 re-score with a fixture
exercising `oracle_excluded>0`; (2) the C1 follow-on the critic named: compare like representations and bind the
witness to the taught claim; (3) one claim on the lane's remaining lowest axes (depth or calibration) with a
counter that fails content-free controls.

Held: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. No axis score moves this
round; C2 moves the operability surface (new registered gate + capability), C1 moves coverage/technique ground
(README Round-36 rows). No retirement.

## Round 37 declaration (attempt 1, L1 MoriR37) — measurement discrimination (calibration) and the drift probe's hardening (freshness)

Entering tip `842a32074b5c7972e9728f3f629d83eb92f127c2` (round 36 admitted; MANIFEST closure `rounds[54x]`,
`corpus/lessons/round-36-verifier-spotcheck.md`). Contract and both counters are frozen before any data:
`.ufo/waves/round-37/contract.md` (P-C1, P-C2, kill rules) with `count-c1.py` and `count-c2.py` pinned by git
blob hash in `evidence/freeze-r37.txt`. The declared cells below copy the frozen contract; targets, not results.

| Claim | Axis / score | Before (one command over committed bytes) | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 the C2 measurement discriminates a real-arm memoizer and enforces the per-id grammar: an extended counter with a run-time-drawn challenge arm in real-arm clothing and `deleted <id>` line parsing (r36 w2/RevNgC2 N1 class; w2/MutC2Deleted limit 3) | calibration 5 (tied lowest with depth and freshness) | `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool .ufo/waves/round-37/fixtures/memo-n1.py --seed 11` → `C2=met`, exit 0 (a tool that never computes the real-arm answer passes; `evidence/c1-before-memo.txt`); same counter with `fixtures/summary-only.py` → `C2=met`, exit 0 (`evidence/c1-before-summary.txt`) | `python3 .ufo/waves/round-37/count-c1.py <landed tip>` → blind 24/24, real pass, challenge pass, `negative memo-n1.py rejected`, `negative const.py rejected`, `negative summary-only.py rejected`, `C1=met`, exit 0 (`evidence/c1-after.txt`) |
| C2 the drift probe's two fetch policies are named, mutation-killable and corpus-bound (r36 w2/SentCensus hardening at `8ff9bba`) | freshness 5 (tied lowest) | `python3 .ufo/waves/round-37/count-c2.py 842a320` → `selftest FAIL` (4 unnamed arms), `knowledge FAIL`, `capability FAIL`, `readme FAIL`, `live FAIL`, `C2=unmet`, exit 1 (`evidence/c2-before.txt`) | the same command at the landed tip → all checks PASS, `C2=met`, exit 0 (`evidence/c2-after.txt`) |

Held and observed: coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6. No retirement,
waiver, exploratory claim or promotion. Controls: the before receipts are the r36 counter's own pass on the two
negative fixtures (a do-nothing control cannot produce `C1=met`); the after counter must both accept the honest
tool and reject all three fixtures, so a counter that only documents cannot meet it. Anti-loop: rounds 35
(register binding) and 36 (C2 gate acquisition, drift technique) are not repeated; C1 is the measurement
discrimination the r36 closure routed, C2 the hardening verification it left open.

Capabilities register — rows demonstrated running this round (closure admits them; evidence is the receipts):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-37 C1 | real-arm challenge counter | Extends the C2 gate measurement with a run-time-drawn challenge history in real-arm clothing and per-id `deleted` line parsing, so a real-arm memoizer and a summary-only printer are both rejected while the honest gate passes | `.ufo/waves/round-37/count-c1.py`; `.ufo/waves/round-37/evidence/c1-after-v2.txt`; `.ufo/waves/round-37/fixtures/` | 37 |
| round-37 C2 | source-drift re-fetch probe | Re-fetches every registry row with a committed copy and classifies the copy against today's body under a 4 MiB bounded read and a post-redirect public-destination policy; round 37 added `--selftest` 6 cases with two named, mutation-killable arms (the probe's live run first worked in round 36) | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after-v3.txt`; `.ufo/waves/round-37/evidence/drift-live-r37.txt` | 36 |

### Round 37 measured outcome (L1 MoriR37; measured at `e57c58b5`, before the wave returns)

| Claim | After (one committed command over committed bytes) | Verdict proposed for the closure |
|---|---|---|
| C1 calibration — measurement discrimination + per-id grammar | `python3 .ufo/waves/round-37/count-c1.py e57c58b5` → blind 24/24, real arm pass, challenge arm pass, `negative memo-n1.py rejected`, `negative const.py rejected`, `negative summary-only.py rejected`, `C1=met`, exit 0, seed 13985344346805549517 (`evidence/c1-after.txt`) | **verified (measured)**: the round-36 counter admits the memoizer and the summary-only printer (`C2=met`, exit 0, `evidence/c1-before-memo.txt`, `c1-before-summary.txt`); the round-37 counter rejects both while the honest gate still passes all three arms. Two earlier fixture defects are mined as lesson M1/M2 and the fixed bytes are the ones scored. |
| C2 freshness — drift-probe hardening | `python3 .ufo/waves/round-37/count-c2.py e57c58b5` → `tool_present PASS`, `selftest PASS` (6 arms), `cap_kill PASS` (`huge_cap=FAIL` in the mutant), `redirect_kill PASS` (`redirect_private_refused=FAIL` in the mutant), `knowledge PASS` (S205, S221–S225, `8ff9bba`), `capability PASS`, `readme PASS`, `live PASS`, `C2=met`, exit 0 (`evidence/c2-after.txt`) | **verified (measured)**: each policy is load-bearing under its own mutation, and the corpus binding exists at the scored rev. The live sweep is a demonstration, not a freshness verdict (the nine drifted rows stay representation differences per QUALITY 105). |

Held: coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6 — no score move; the
calibration and freshness rows' evidence pointers now name round 37. No retirement, waiver, exploratory
claim or promotion. Census end `mori ok`, exit 0 (`evidence/census-end.txt`). Capabilities register rows:
`round-37 C1` (real-arm challenge counter) and `round-37 C2` (source-drift re-fetch probe), both demonstrated
running in the receipts named above. Routed round-36 debts (a)–(h): (a)–(c) are claims C2/C1, (d) fixed and
re-run green (`evidence/r17-jj-selftest-r37.txt`), (e)–(g) are properties of the new counters, (h)
re-verified in the round-36 note. Frozen round-36 bytes are untouched.

### Round 37 post-data corrections (wave 1, appended before the report lands)

Wave 1 returned 37 seat reports. Four document/attribution defects and one open obligation are corrected
here; the frozen predicate bytes (P-C1, P-C2) and both measured receipts are unchanged.

1. **C2's axis is operability, not freshness** (w1/CritC2Axis, FAIL). The round changes a runnable
   instrument's verification — two named arms, each killed by its own mutation, plus the corpus binding —
   not a re-verified claim against a live surface. The declared cell above stays as declared (the contract
   is frozen); this correction re-attributes the claim: **C2 = operability (7), held**, and freshness is
   **not claimed as moved** this round. C1 remains calibration (5, tied lowest), so the lowest-axis
   obligation is still met.
2. **Debt (f) is OPEN, not closed** (w1/CritDebtDisposition). Round 36's obligation was "restructure the
   timeout path to avoid SIGKILL of the sandbox child". Round 37 replaces the immediate SIGKILL with
   SIGTERM → 5 s grace → SIGKILL and reports `tool_timeout` as a distinct state, which is a disclosed
   trade, not the requested restructuring. Re-filed as **operator-owned policy tradeoff**: a probe that
   must not kill its own child cannot bound a hung tool at all; the canonical judge decides whether the
   grace-period kill stands. The claim that the boundary is "in the predicate output" was wrong — it is in
   the counter docstring (`count-c1.py:27-29`) and `run()` (`:92-114`), not the printed `PREDICATE`.
3. **Evidence path erratum** (w1/SentData, w1/ScoutSentData, w1/CritDebtDisposition): four receipts
   (`c1-before-memo.txt`, `c1-before-summary.txt`, `census-start.txt`, `census-end.txt`) carried absolute
   operator paths. Re-emitted with repo-relative paths and a `redacted:` line (same command, same measured
   output); debt (e) is closed by that erratum commit, not by the original commit it claimed.
4. **Wave-spec redundancy** (w1/ScoutWaveSpec, FAIL): `ExecC1Seed41/42/43` were the loop body
   `RevC1Predicate` already ran — three seats on one loop. Recorded as lesson M7; the seed values stay as
   the seats' independent receipts.
5. **Content-free bypass of P-C2's content half** (w1/CritC2ContentFree, FAIL): all three fabricated
   shapes — a token-satisfying entry with no located quote, a capability row pointing nowhere, and a live
   receipt carrying the summary sentence alone — meet the predicate, and their combination with a real
   tool passes `C2=met`. P-C2's content checks are token/genus checks; they do not prove the corpus work.
   The measured claim (P-C2 as frozen) stands, but it is reported as **verified on P-C2 with a disclosed
   content-discrimination gap**, and the tightening (a content-anchor arm: the hardened tool must detect a
   named row's drift under the two policies) is routed to round 38 as a new counter version — not applied
   post-data here. This is the same class as QUALITY 98 and is recorded as lesson M9.
- **Commit attribution (A3).** The hardening commit is `1caa242` (it touches `tools/mori-source-drift.py`),
  not `8ff9bba` (which touches no tool byte). Every artifact is corrected; the C2 counter v3 reconstructs
  the commit and requires it to touch the tool (w1/ExecKnowledgeCheck; lesson M10).
- **A2 (drift receipt).** `evidence/drift-live-r37.txt` is the 225-row tip sweep
  (`rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`); the entering 220-row sweep is
  `drift-live-r37-start.txt`. The ten drifted rows are the nine round-36 rows plus S223, whose page footer
  clock changes between fetches (w1/ExecDriftLive; lesson M9-class byte-unstable page).
7. **Smaller bounded findings from wave 1** (all disclosed, none changes a verdict):
   `w1/MutC2CapArm` — `cap_kill` passes vacuously on a rev whose tool already lost the 4 MiB anchor, but
   the aggregate still reads `C2=unmet` via `selftest` (fail-closed); `w1/SimpC2` — four removable bytes
   (a dead `body_at is not None` conjunct, the duplicate `cat-file -e` pre-check in `show()`, a discarded
   return whose docstring promises `probe_timeout`, a mid-expression comment) and one wart are routed to
   round 38, because editing them now would break the counter pins; `w1/ExecC1Seed41` +
   `w1/RevC1Negatives` — the real arm does not compare the tool's exit code (latent: the blind and
   challenge arms do, and P-C1 does not require it).
8. **Probe-timeout wording**: `count-c2.py`'s docstring says a timeout "reports `probe_timeout`", but the
   check prints `exit=None` in its detail. The timeout path itself (SIGTERM → 5 s → SIGKILL) is real; the
   label is not. Corrected here rather than in the frozen bytes (r38: surface the detail or trim the
   docstring).
9. **Security review** (w1/SentTools, FAIL): HIGH — the counters execute the tool under test by design
   (that is the measurement; the trust boundary is the caller's `--repo`/`--tool`), documented as an
   accepted boundary; MEDIUM — `count-c2.py`'s `show()` git reads have no timeout or size bound, and
   LOW — relative `--tool` paths validate and execute from different directories (carried from r36
   w2/RevNgC2 §1). Both need a counter re-freeze, so they are routed to round 38 with the exact fixes.

### Round 37 A1–A3 re-score (measured at `4bfa0490`, after the wave-1 amendments)

| claim | after (command over committed bytes) | verdict |
|---|---|---|
| C1 (counter v2: run-time-drawn real arm; challenge title = the lane title) | `python3 .ufo/waves/round-37/count-c1.py 4bfa0490 --seed 20261024` → blind 24/24, real pass, **drawn arm pass** (rev `842a32074b`, base `3c2fe8c3eb`), challenge pass, three negatives rejected, `C1=met`, exit 0 (`evidence/c1-after-v2.txt`) | **verified (measured, v2)**: a memoizer keyed on the sandbox identity or the challenge's clothing can no longer print the published constant, because the drawn rev's answer is not published. Disclosed residual: a tool keyed on the real arm's published rev literal cannot be distinguished on that one arm (the drawn arm is where the discrimination lives). |
| C2 (counter v3: tip live receipt + attribution check that the cited commit touches the tool) | `python3 .ufo/waves/round-37/count-c2.py 4bfa0490` → all eight checks PASS, `knowledge … cited_commit=True touches_tool=True`, `live PASS` (225-row sentence), `C2=met`, exit 0 (`evidence/c2-after-v3.txt`) | **verified (measured, v3)**: the v2/v1 receipts stand as history; v3 is the receipt of record. The content-half gap (w1/CritC2ContentFree) remains disclosed and is routed. |

Freeze of record: `evidence/freeze-r37-v3.txt` (count-c1 `3e15f9fd…` at v2, count-c2 `39d06e20…` at v3, drift tool
`162ee87b…`, contract `d2d61144…`).

## Round 38 declaration (attempt 1, L1 MoriR38) — the content half, instrument conformance, timed supersede

Entering tip `e33bb561` (round 37 admitted). Frozen before data: `.ufo/waves/round-38/contract.md` +
`count-c1.py` (v4) + `count-c4.py` + `conform.py` + fixtures, pins in `evidence/freeze-r38.txt` (v1) and `evidence/freeze-r38-v3.txt` (final instrument bytes).
Three claims, distinct axes; calibration and depth are the tied-lowest non-retired (5), so the
lowest-axis obligation is met by C1 and C3.

| # | claim (type) | axis | before → after (one value) | counting command | evidence |
|---|---|---|---|---|---|
| 1 | content-anchor discrimination: the drift-corpus binding must resolve, not just carry the r37 tokens (r37 M9) | calibration | fabricated binding `C2=met` (r37 counter) and `C4=unmet` → real binding `C4=met`, exit 0 | `python3 .ufo/waves/round-38/count-c4.py <rev>` | `.ufo/waves/round-38/evidence/c4-before.txt`, `.ufo/waves/round-38/evidence/c4-after.txt`, `.ufo/waves/round-38/evidence/v3-token-control.txt`, `.ufo/waves/round-38/evidence/c4-witness.txt` |
| 2 | instrument conformance and replayability (r37 R1/R2/R4, SentTools MEDIUM/LOW, LabTimeoutBoundary) | operability | `CONFORM=unmet` (6/6 checks FAIL on the r37 counters) → `CONFORM=met` (6/6) with `CONFORM_SELFTEST pass=6 fail=0` | `python3 .ufo/waves/round-38/conform.py <rev> --counter …` and `--selftest` | `.ufo/waves/round-38/evidence/c5-before.txt`, `.ufo/waves/round-38/evidence/c5-after.txt`, `.ufo/waves/round-38/evidence/c5-after-selftest.txt` |
| 3 | timed supersede semantics in the append-only gate; S069 disposed by a postdating row (r37 ExecGateRound D3) | depth | gate prints no timing field (0 occurrences) → `supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]` at the round-38 tip, `stale_supersede=[S069]` at `e37dcc6` (corrected round 38, see note) | `python3 tools/mori-sources-appendonly.py <rev> --round-base f10a320d` | `.ufo/waves/round-38/evidence/gate-before.txt`, `.ufo/waves/round-38/evidence/gate-after.txt`, `.ufo/waves/round-38/evidence/gate-selftest-after.txt` |

Kill rules: a do-nothing control cannot print `C4=met`, `CONFORM=met` or the timing line; the
r37 counter scores the fabricated binding `C2=met`; a gate whose timing field is presence-based
lists S069 in `superseded_as_of` at `e37dcc6` and its own `stale_supersede` selftest fixture fails.

### Round 38 capability rows (demonstrated running this round)

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-38 C1 | content-anchor corpus check | Requires a corpus binding to resolve: named `anchor:` code strings in the probe's bytes, capability paths resolving from the repo root, one named drifted row per summary count, and a named-row selftest arm killed by its own mutation; rejects three fabricated token witnesses | `.ufo/waves/round-38/count-c4.py`; `.ufo/waves/round-38/evidence/c4-after.txt`; fixtures under `.ufo/waves/round-38/fixtures/` | 38 |
| round-38 C2 | counter conformance checker | Audits an instrument's identity and bounds — predicate bytes, lane-tip pin, lane-relative tool resolution, bounded reads, timeout state, lane scratch — with six mutations each flipping exactly its own check | `.ufo/waves/round-38/conform.py`; `.ufo/waves/round-38/evidence/c5-after.txt`; `.ufo/waves/round-38/evidence/c5-after-selftest.txt` | 38 |
| round-38 C3 | timed supersede reading | Separates a supersede disposition that postdates the edit from one that predates it, on the same commit walk the append-only gate already performs | `tools/mori-sources-appendonly.py` (`supersede_timing`); `.ufo/waves/round-38/evidence/gate-after.txt` | 38 |

### Round 38 axes-cell correction (append-only note; names the superseded text)

The `freshness` axes cell read "round-37 claim C2 verified the probe's hardening as named,
mutation-killable arms and states no new number"; the round-37 closure re-attributed C2 to
operability, so that clause is superseded. The cell now reads "round-37 C2 is re-attributed to
operability (round-38 axes-cell correction below) and round 38 claims no freshness move"; the
`operability` cell gained the round-37 pointer. The `source-drift re-fetch probe` capability row's
first-working cell moved 37 → 36 (the live run worked in round 36; round 37 added the named arms)
and its two wave-directory paths became repo-relative.

### Round 38 claim-3 cell correction (append-only note; names the superseded text)

The round-38 claim-3 row's after cell read "`supersede_timing superseded_as_of=[S069,S182,S193]
stale_supersede=[]` at the round-38 tip". That literal is superseded: the gate prints **every**
superseded id whose latest superseder postdates its last immutable-cell edit — 18 ids at the tip
(`[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193]`),
as `evidence/gate-after.txt:22` records. The error was the L1's transcription of the r36 oracle's
`superseded=[S069,S182,S193]` field for a different tool; the w2/RevScorecardClaims seat re-derived
it. The cell now carries the observed line and this note. The claim's discriminator is unchanged:
`stale_supersede=[S069]` at `e37dcc6` and `stale_supersede=[]` at the tip.

## Round 39 declaration (attempt 1, L1 mori-r39) — fabricated-content discrimination v2 (C1, calibration), conformance timeout name-and-value (C2, operability), ancestry-based timed supersede (C3, depth)

Entering tip `13f3db7e` (round 38 admitted). Contract `.ufo/waves/round-39/contract.md` and all
instrument bytes frozen at `97b826a9` (pins `evidence/freeze-r39.txt`) before any data seat.
Lowest non-retired axes calibration 5 and depth 5 (tied) — C1 works calibration, C3 depth.

| Claim | Axis / score | Before (one command over committed bytes) | Declared after-value (one command over committed bytes) |
|---|---|---|---|
| C1 the drift-corpus binding's checks discriminate fabricated content: code-position anchors ≥8 chars, file-not-directory capability paths, committed copies for named drifted rows, and a structural got-vs-want drift kill with a run-time-drawn post-state (r38 M18) | calibration 5 | the r38 counter accepts every bypass: `evidence/c7-red-one-char.txt`, `c7-red-comment.txt`, `c7-red-classifier.txt`, `c7-red-clone.txt` each end "RED (bypass accepted)"; the clone receipt shows `C4=met` exit 0 on a fabricated binding | `python3 .ufo/waves/round-39/count-c7.py <landed tip>` → five checks PASS, four negatives rejected, `C7=met`, exit 0 (`evidence/c7-after.txt`); the same command on the fabricated clone prints `live_rows_v2 FAIL ... no_copy=['S103']`, `C7=unmet` (clone receipt's round-39 block) |
| C2 the conformance checker reads timeout values (folded constants) and drain shape, and its selftest exercises the communicate-timeout conjunct (r38 M19) | operability 7 | `python3 .ufo/waves/round-38/conform.py 13f3db7e --counter fixtures-derived/bypass-none.py` → `CONFORM=met` exit 0 (`evidence/c8-red-none.txt`); bypass-wait likewise (`evidence/c8-red-wait.txt`); the r38 selftest never mutates a communicate timeout (`evidence/m19-selftest-gap.txt`) | `python3 .ufo/waves/round-39/conform.py <landed tip>` → `CONFORM=met` exit 0 (`evidence/c8-after.txt`); `--selftest` → `CONFORM_SELFTEST pass=9 fail=0` (`evidence/c8-after-selftest.txt`); both bypass fixtures → `CONFORM=unmet` with `timeout_value`/`drain_shape` FAIL (`evidence/c8-after-none.txt`, `c8-after-wait.txt`) |
| C3 the append-only gate's timed supersede is ancestry: `merge-base --is-ancestor` between the last first-parent-derived edit and the landing, on a parent-carrying `--full-history` walk (r38 F1/F2; sourced S227) | depth 5 | the r38 gate bytes fabricate `round_changed=[S001]` on fixture C (exit 1) and print `stale_supersede=[S001]` on fixture D where the predicate's words read as-of (`evidence/c9-red-a.txt`); the lane walk under default simplification drops `6531ac60` (53 vs 52 commits) | `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0` (`evidence/gate-selftest-after.txt`); `run-c9-dags.py` with the v2 gate prints `stale_supersede=[S001]` on A, `round_changed=[]` exit 0 on C, `superseded_as_of=[S001]` on D (`evidence/c9-after-fixture-a.txt`, `c9-after-fixture-c.txt`); lane receipts byte-identical to round 38 at the tip and `e37dcc6` (`evidence/c9-after-lane.txt`) |

Capability rows (demonstrated running this round; closure admits them):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-39 C1 | fabricated-content discriminator v2 | Scores the drift-corpus binding with code-position anchors, file-only capability paths, committed-copy live rows, and a drawn-state structural drift kill; rejects the three round-38 witnesses plus a comment-parked entry, and rejects a fabricated clone via the copy rule | `.ufo/waves/round-39/count-c7.py`; `evidence/c7-after.txt`; `evidence/c7-red-*.txt` | 39 |
| round-39 C2 | counter conformance v2 | Nine checks (the r38 six plus timeout_value, drain_shape, selftest_conjunct) with a constant-folding resolver and a nine-mutation selftest, each mutation flipping exactly its own check; rejects both r38-M19 bypass fixtures | `.ufo/waves/round-39/conform.py`; `evidence/c8-after.txt`; `evidence/c8-after-selftest.txt` | 39 |
| round-39 C3 | ancestry supersede reading | Separates as-of from stale by reachability (`merge-base --is-ancestor`) on a parent-carrying full-history walk with first-parent edit detection; lane verdicts unchanged, fixture verdicts now match the predicate's words | `tools/mori-sources-appendonly.py` (`supersede_timing`, P-C9); `evidence/c9-after-lane.txt`; `evidence/c9-after-fixture-a.txt` | 39 |

Held: coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6 — no scalar score moves
this round; C1 moves the calibration surface (new counter + receipts), C2 the operability surface
(new checker version), C3 the depth surface (gate semantics + S227). Sourced claim: C3 rests on
S227 (opened this round; `corpus/knowledge/gate-ancestry-r39.md`). No retirement, waiver, exploratory
claim or promotion. Frontier: S227, S228 rows; census 226 → 228.

## Round 40 declaration (attempt 1 resumed, L1 mori-r40) — conformance v3 scope-aware timeouts + per-Popen drains (C1, operability), gate v3 P-C11 eligible set + first-parent reference (C2, depth)

Entering tip `bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3` (round 39 admitted; closure
`corpus/lessons/round-39-verifier-spotcheck.md`). Instruments landed at
`265a955cc67be4eae97d2dc5a9338a25f31eb29b` (T1); evidence + corpus records at the
round tip (T2, this commit's parent chain). Contract
`.ufo/waves/round-40/contract.md` (frozen by the prior launch; re-verified and
completed by this one — see lesson M23). Lowest non-retired axes calibration 5 and
depth 5 (tied) — C2 works depth; C1 works operability (routed defect 1/2 class).

| Claim | Axis / score | Before (one command over committed bytes) | After (measured at T1) |
|---|---|---|---|
| C1 conformance v3: `timeout_scope` resolves every `timeout=` at its read site (function-local shadow, `global`, conditional rebind fail closed; finite-positive fold), `drain_bind` requires a consumed `communicate(timeout=…)` bound to the same name as each `Popen(`, `selftest_conjunct` reads the checker's own mutation table with per-counter comm_violations (r39 w1 findings 4/8/12; routed defects 1–2) | operability 7 | the r39 checker bytes (`fixtures/extracted/conform-v2-r39.py`, sha fe0be179…) print `CONFORM=met` exit 0 on nine survivor fixtures + a two-counter audit, and a conjunct-gutted r39 copy selftests `pass=8 fail=0` (`evidence/c10-red-*.txt`) | `python3 .ufo/waves/round-40/conform.py 265a955cc…` → `CONFORM=met` exit 0 (`evidence/c10-after.txt`); `--selftest` → `CONFORM_SELFTEST pass=11 fail=0` (`c10-after-selftest.txt`); each survivor + the multicounter audit → `CONFORM=unmet` exit 1 with the named new check FAIL (`c10-after-<fixture>.txt`); conjunct-gutted v3 copy → `pass=0 fail=10`, `selftest_conjunct` in every failing list (`c10-after-conjunct.txt`) |
| C2 gate v3 (P-C11): the `supersede_timing` eligible set is every superseded id present at R (never-edited ids test as-of against their first-sighting commit); an edit compares against the first parent's own state only — a first-parent-lacks-path merge contributes no edits and a linear delete-then-re-add contributes no changed event (r39 w1 findings 2/5; routed defects 3–4) | depth 5 | the v2 gate bytes (`fixtures/extracted/gate-v2-bb1f2457.py`, sha 62cd4132…) print the lane line with 18 as-of ids, S226 absent (`evidence/c11-before-lane.txt`), omit the never-edited superseded row on dag-n, fabricate a changed line + stale verdict on dag-p, and the conjunct-gutted/red set as committed (`c11-red-*.txt`) | `python3 tools/mori-sources-appendonly.py --selftest` → `pass=15 fail=0` (`c11-after-selftest.txt`); lane at T1 → 34 as-of ids incl. S226, `stale_supersede=[]` (`c11-after-lane.txt`); at `e37dcc6` → `stale_supersede=[S069]` (`c11-after-e37dcc6.txt`); dag-n/dag-p/dag-r print the P-C11 verdicts (`c11-after-fixture-{n,p,r}.txt`) |

**Correction folded same-round (number-drift):** the contract's and P-C11's
parenthetical "(19 ids)" mis-predicted the eligible-set extension: 16 never-edited
superseded rows (S226 plus 15 earlier) reach the timing line, not only S226 — the
measured value is **34 as-of ids** at T1. The predicate's semantic sentence is the
claim; the parenthetical arithmetic is corrected here and in lesson M24. The
discriminator (S226 present; v2's edit-bounded set omits all 16) is unchanged.

Kill rules as frozen: a do-nothing control cannot print `CONFORM=met` (the r39
checker on the survivors is the committed control); a gate keeping the edit-bounded
eligible set prints 18 ids ≠ 34 with S226 absent; a gate with the second-parent
fall-through fabricates the dag-p edit; a gate keeping the re-add changed event
prints `stale=[S008]` on dag-r.

Capability rows (demonstrated running this round; closure admits them):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-40 C1 | counter conformance v3 | Audits every counter's `timeout=` keywords at their read sites (function-local shadow, `global`, conditional rebind, finite-positive fold), binds every `Popen(` drain to a consumed same-name `communicate(timeout=…)`, and reads its own mutation table for the communicate-timeout conjunct with per-counter comm_violations; eleven-mutation selftest | `.ufo/waves/round-40/conform.py`; `evidence/c10-after.txt`; `c10-after-selftest.txt` | 40 |
| round-40 C2 | ancestry supersede reading v3 | Separates as-of from stale over every superseded id present at R (never-edited ids test against their first-sighting commit), with edits measured against the first parent's own state only — no second-parent fall-through, no re-add changed event | `tools/mori-sources-appendonly.py` (P-C11); `evidence/c11-after-lane.txt`; `c11-after-fixture-n.txt` | 40 |

Held: coverage 6, operability 7 (C1 moves the surface; the v3 checker row enters
the registry; score held per the round's honest read — closure rules), depth 5 (C2
moves the surface; score held, same read), calibration 5, freshness 5, adjacency 6 —
no scalar score moves this round; both claims are checker-semantics moves whose
receipts are the improvement. Sourced claim: C1 rests on S229 (opened this round;
`corpus/knowledge/conform-scope-r40.md`). No retirement, waiver, exploratory claim
or promotion. Frontier: S229 row; census 228 → 229 (exit 0 both ends).
Round shape: ONE v2 wave, 66 seats (32 attack = 48.5%), validated under policy v2
(`evidence/wave-plan.txt`, `w1-spec.json`) — prepared-but-undispatched under the
accepted host mapping (orchestrator dispatches prepared waves between rounds).

## Round-41 calibration correction (2026-10-24, L1 mori-r41)

The round-40 v3 gate at `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` derives
**35 as-of ids** at T1 and a **17-row** never-edited extension (S226 plus 16
earlier); the round-40 after-cell above recorded 34 and 16. Round-41
calibration correction: observed_as_of=35; extension_rows=17. This appended
line supersedes the round-40 "34 as-of ids"/"16 never-edited" figures; the
original text stands unmodified above.

Round-41 calibration correction: observed_as_of=35; extension_rows=17.
(single-line record for the frozen counter `tools/mori-round41-calibration.py`;
the wrapped paragraph above states the same values).

## Round 41 declaration (L1 mori-r41, attempt 2 — inherits attempt-1 freeze at d72ac16, re-verified byte-exact)

Entering tip `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` (round 40 closed REJECTED
rejected-honest-stop; closure `corpus/lessons/round-40-verifier-spotcheck.md`).
Lowest non-retired axes depth 5, calibration 5, freshness 5 (tied) — C2 works
depth, C3 works calibration; C1 works operability (routed defect 1 class).
Contract `.ufo/waves/round-41/contract.md`; pins `.ufo/waves/round-41/evidence/freeze-r41.txt`
(19/19 re-verified at attempt 2, `evidence/freeze-verify.txt`); frozen no-op
control `evidence/control-before.txt` (v3 checker `CONFORM=met` on all three
routed survivors; v3 gate wrong on all five routed DAG classes; calibration
mismatches=6).

| Claim | Axis / score | Before (one command over committed bytes) | After (measured) |
|---|---|---|---|
| C1 conformance binding model v4 (P-C10 r41): source-ordered function-local inventory — `Assign`/`AnnAssign`, `NamedExpr`, tuple/list destructuring, for/with targets; unresolved targets, unsupported stores, `global`/`nonlocal` rebinding and disagreeing multi-bindings fail closed (routed defect 1; sourced S230) | operability 7 | extracted r40 v3 bytes `fixtures/extracted/conform-v3-r40.py` print `CONFORM=met` exit 0 on each routed survivor (walrus, tuple-unpack, dead-loop; `evidence/control-before.txt` §C1) | `python3 .ufo/waves/round-41/conform.py aa161e998…` → honest counter `CONFORM=met`; each survivor `CONFORM=unmet` with only `timeout_scope` FAIL; `--selftest` `pass=14 fail=0`; early-continue mutant fails `selftest_conjunct` (`evidence/control-after.txt`) |
| C2 gate P-C12: eligible pair = both rows present at R; per-commit header maps; ancestry-grounded landing selection (maximal candidates, superseder-id then hash tie-break); delete/re-add = new landing; never-edited edit = first-sighting commit (routed defects 2a–c) | depth 5 | v3 gate bytes `fixtures/extracted/gate-v3-r40.py` fabricate dag-h changes, miss dag-h2's pair, time dag-z/z2's absent superseder, flip dag-2l on commit date, miss dag-x's re-add landing (`control-before.txt` §C2) | `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`; lane line at aa161e998 lists **36 as-of ids** (S229 via S231) stale=[]; at `e37dcc6` stale=[S069]; all seven routed DAG fixtures print the P-C12 verdicts (`control-after.txt` §C2) |
| C3 calibration records: append-only corrections reconcile the r40 34/16 self-assessment to the frozen r40 gate's 35/17 (routed defect 3) | calibration 5 | `python3 tools/mori-round41-calibration.py 62a207f… --repo . --reference-rev 62a207f…` → `MORI_R41_CALIBRATION mismatches=6` (`control-before.txt` §C3) | same counter at `c5326c61…` → `mismatches=0` exit 0 (`evidence/calibration-after.txt`) |

Capability rows (demonstrated running this round; closure admits them):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-41 C1 | counter conformance binding inventory v4 | Rejects timeout reads whose function-local bindings are walrus/tuple-unpack/loop-with targets, unsupported stores, `global`/`nonlocal` rebinds, or disagreeing multi-bindings — the routed v3 survivor class — while keeping the nine-check honest-counter pass and a 14-arm selftest whose conjunct applies each arm | `.ufo/waves/round-41/conform.py`; `evidence/control-after.txt` §C1 | 41 |
| round-41 C2 | ancestry supersede reading P-C12 | Reports `supersede_timing` over pairs present at R only, per-commit header maps, ancestry-selected landings with deterministic tie-break, re-add landings, first-sighting edits; lane-history verdicts preserved (36 as-of; S069 stale at e37dcc6) | `tools/mori-sources-appendonly.py`; `evidence/control-after.txt` §C2 | 41 |
| round-41 C3 | correction-record reconciliation | A frozen counter (`tools/mori-round41-calibration.py`, reference `62a207f…`) reads single-line `Round-41 calibration correction:` records in the three r40 record files and reports mismatches=0 | `evidence/calibration-after.txt` | 41 |

Held: coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6 —
no scalar moves; the claims repair routed falsifications, their receipts are the
improvement. Sourced claims: C1 rests on S230 (+S231 locator correction), C3 on the
frozen r40 gate bytes (own-work evidence). No retirement, waiver, exploratory claim
or promotion. Frontier: S230, S231 rows; census 229 → 231 (exit 0 both ends,
`evidence/census-start.txt`/`census-end.txt`). Round shape: ONE v2 wave, 64 seats
(31 attack = 48.4%), prepared+validated by attempt 1 under policy v2
(`evidence/wave-plan.json` exit 0, `w1-spec.json`); dispatch status recorded in the
round report. Attempt 3 (2026-10-24): wave dispatched by attempt 2 (64 spawned;
19/64 seat reports returned, committed under `.ufo/waves/round-41/w1/`); all 19
freeze pins re-verified at `7450722e` (`evidence/freeze-verify-attempt3.txt`);
C1/C2/C3 counters re-run live at `7450722e` with frozen-target results; census
229 → 231 exit 0 both ends (`evidence/census-start.txt`, `census-end.txt` — end
receipt repaired with header + `ROWS=231`); `calibration-after.txt` re-issued
with measured-revision header; lesson M27/M28 appended with wave-draft M-id
adjudication + S230 quote erratum; fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/mori.md`.

## Round 42 declaration (L1 Kimi fresh mori-r42) — routed repairs + checker v5

Entering tip `9de7323de482699743619cfa2ee444e7418421e3` (round 41 admitted).
Lowest non-retired axes depth 5, calibration 5, freshness 5 (tied): C2 works
calibration, C3 depth; C1 works operability (routed defect 1/5 class).
Freeze `.ufo/waves/round-42/contract.md` + counters + controls, pins
`evidence/freeze-r42.txt`, committed before any seat ran (inherited
same-round attempt tree, re-verified byte-exact, reused).

| # | claim | axis / score | before | after (measured at the landed tip) |
|---|---|---|---|---|
| C1 | conform v5 closes the three surviving r41 checker-mutation lanes with three fixture arms (`timeout_scope_walrus_positive`, `timeout_scope_tupleunpack_positive`, `timeout_scope_source_order`), each killed by exactly its own frozen checker mutation; sourced S347 (opened this round) + S230 | operability 7 | v4 bytes selftest `pass=14 fail=0` and the three v4-derived mutants survive (`evidence/control-c1-v4.txt`) | `python3 .ufo/waves/round-42/count-c1.py <tip>` → `C1=met` exit 0 (`evidence/c1-after.txt`) |
| C2 | report-accuracy errata in append-only lane records | calibration 5 | `count-c2.py 9de7323d` → `C2=unmet` exit 1 (`evidence/control-c2-before.txt`) | same counter at the landed tip → `C2=met` exit 0 (`evidence/c2-after.txt`) |
| C3 | the 145 unnamed inherited `d72ac16` files named by category and provenance | depth 5 | `count-c3.py 9de7323d` → `C3=unmet` exit 1 (`evidence/control-c3-before.txt`) | same counter at the landed tip → `C3=met` exit 0 (`evidence/c3-after.txt`) |

Round-41 report errata recorded here (claim C2, same three corrections as
the round-42 LOG entry): "8/8 mutants killed" is **superseded by 5/8 killed,
3 SURVIVED** (MutC1Walrus/MutC1Tuple/MutC1DropSort); "34 attack seats
(53%)" is **superseded by 31 attack seats of 64 (48.4%)** (12 reviewer + 11
critic + 8 mutation-tester; executors are not attack roles); "2 scouts,
4 scribes" is **superseded by 1 scout, 5 scribes**, returned total 19
unchanged. These corrections are recorded so no lane-owned round-42 record
re-asserts a superseded value uncontradicted.

Held: coverage 6, freshness 5, adjacency 6. No retirement, waiver,
exploratory claim or promotion. Frontier: registry 231 → 238 (S232–S235,
S241, S262 admitted with the two assimilation entries; S347 mine); refused
entry and flip condition under `.ufo/waves/round-42/assimilation/`.

### Round 42 measured outcome (L1 Kimi fresh mori-r42, tip 34b9267)

| Claim | After (measured) | Verdict proposed for the closure |
|---|---|---|
| C1 | `count-c1.py 34b9267…` → 28 checks PASS then `TypeError … cwd` at its final no-harm check, rc 1, no `C1=` line (`evidence/c1-after.txt`) | **not verified (honest stop)**: the frozen counter's own defect; v5 substance (17/0 selftest, three mutants killed on exactly their arms, routed four unchanged) verified by the counter's 28 prior checks and the no-harm clause re-derived by hand (`evidence/c1-noharm-manual.txt`); the counter is pinned and not amended after data (fleet lesson, kumitate r42) |
| C2 | `count-c2.py 34b9267…` → `C2=met` exit 0 (`evidence/c2-after.txt`) | verified (measured) |
| C3 | `count-c3.py 34b9267…` → `C3=met` exit 0 (`evidence/c3-after.txt`) | verified (measured) |

Held: coverage 6, operability 7, depth 5, calibration 5, freshness 5,
adjacency 6 — no score move (C1's miss bars a move on operability; C2/C3
repair routed defects at held scores, the lane's established pattern).
Mistake M4 added to the lesson (counter never executed end-to-end
pre-freeze).

## Round 43 declaration (L1 Kimi fresh L1, mori-r43) — successor operability + calibration repair

Entering tip `e3a2b58f72ba3bd52a90646f7285fb85f0ee5dd2`. Frozen r42
`count-c1.py` is not amended. Lowest non-retired axes are tied at 5;
calibration is the lowest-axis claim. No score move is pre-awarded.

| # | claim | axis / score | before | after (one command) |
|---|---|---|---|---|
| C1S | successor measurement completes, including no-harm, and prints `C1S=` | operability 7 | `count-c1s.py e3a2b58` → `C1S=unmet` (counter absent at rev) | `python3 .ufo/waves/round-43/count-c1s.py <tip>` → `C1S=met` exit 0 |
| C2 | append-only corrections of the r42 `C1=met` declaration cell and the S235 transposed sha | calibration 5 | `count-c2.py e3a2b58` → `C2=unmet mismatches=2` | `python3 .ufo/waves/round-43/count-c2.py <tip>` → `C2=met mismatches=0` exit 0 |

Round-43 calibration correction: r42-declaration-C1=met superseded; frozen counter printed no C1= line

The round-42 declaration cell above is not rewritten. The measured-outcome section already contradicted it. This line is the append-only supersession the round-43 counter reads. The S235 row is not rewritten; S349 records the committed PDF sha256.

### Round 43 measured outcome (L1 Kimi fresh mori-r43, tip dde525ea4a7fca365e8ff2f3c486bccf28b94e52)

| Claim | After (measured) | Verdict proposed for the closure |
|---|---|---|
| C1S | `python3 .ufo/waves/round-43/count-c1s.py dde525ea…` → 15 checks PASS, then `C1S=met` exit 0 (`evidence/c1s-after.txt`) | **verified (measured), with a disclosed instrument-tamper limitation.** The successor completes the arm the frozen r42 counter never reached: the frozen counter still exits non-zero with `TypeError: run() got an unexpected keyword argument 'cwd'` and prints no `C1=` line, and the no-harm arm records `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` rc 0 in a sandbox clone. Controls re-executed by the L1: do-nothing at the entering tip → `C1S=unmet` exit 1; a counter whose body only prints `C1S=met` → `C1S=unmet` exit 1; green control on a scratch clone → `C1S=met` exit 0. **Limitation, disclosed:** the counter's verdict is not tamper-evident — a coordinated mutation applied to both the running copy and the rev copy (the no-harm arm removed, or a check loosened) still prints `C1S=met` with one check fewer; the counter's identity is therefore pinned by its sha256 `93482248b46def2a2cec7238732af1551ef315517e76833c3843875313b65dc5` at the landed tip, and a mutated copy is not the claim's counter. Routed to round 44 as a counter-hardening item. A stricter reading of the kill rule would grade this claim not verified; the ruling is the closure's. |
| C2 | `python3 .ufo/waves/round-43/count-c2.py dde525ea…` → `C2=met mismatches=0` exit 0 (`evidence/c2-after.txt`) | **verified (measured).** The round-42 declaration cell is still present and unmodified (the counter's `declaration_unrewritten` check counts it exactly once), the append-only correction line appears exactly once, the S235 row's bytes are unchanged (sha256 `971df55e…`), and a separate row carries the committed PDF's sha256 `9855a498…`. Controls re-executed by the L1: do-nothing at the entering tip → `C2=unmet mismatches=2` exit 1; green control on a scratch clone → `C2=met mismatches=0` exit 0. |

Held: coverage 6, operability 7, depth 5, calibration 5, freshness 5,
adjacency 6 — no score move (the claims repair two routed defects at held
scores, the lane's established pattern; the lowest-axis obligation is worked
by C2 on calibration, tied lowest with depth and freshness). Frontier:
registry 238 → 243 rows (S348, S349, S350, S351, S470); one admitted
assimilation entry on the `--disk-usage` theme, two refusals with reason and
flip. QUALITY 115 (frozen instruments must replay off-host) and QUALITY 116
(an unreachable verdict needs a GET probe, not a HEAD probe) added this
round. Mistakes M1–M5 in `corpus/lessons/round-43.md`.

## Round 44 declaration (L1 lane subagent, mori-r44) — figure reconciliation, gate standard, FR5 pid-probe ground

Entering tip `1429c791db5891c484684feef893799909d2d6a8` (round-43 closure
admitted). Instruments frozen at `7cb59c6891d4f5d0266fe062565f094da835dc84`
before the first data seat; pins `.ufo/waves/round-44/evidence/freeze-r44.txt`.
Lowest non-retired axes at the entering tip: calibration 5 tied with depth 5 and
freshness 5 — C1 works calibration, C2 operability, C3 coverage. Contract and
predicates: `.ufo/waves/round-44/contract.md` (P-C1, P-C2, P-C3).

Routed round-43 defects answered: item 3 (count slips) by C1, item 4 (no gate
registry row, no `--selftest`) by C2, item 5 (receipt revision vs verdict
revision) by the tip-run receipt and QUALITY 119. Items 1, 2 and 6 are durable
records or operator-side and are named in the report, not fixed.

| # | claim | axis / score | before (one command over committed bytes) | declared after-value (one command) |
|---|---|---|---|---|
| C1 | a committed figure ledger reconciles the round's reported counts: `git`-pipeline rows naming `@REV@`, re-derived at the measured revision, 12-row and 4-class floors | calibration 5 | `python3 .ufo/waves/round-44/count-c1.py 1429c791` → `check ledger_present FAIL (absent)` → `C1=unmet`, exit 1 (`evidence/control-c1-donothing.txt`) | `python3 .ufo/waves/round-44/count-c1.py <landed tip>` → `C1=met mismatches=0`, exit 0 |
| C2 | each of the round's counters is a registered gate: eight non-empty standard cells in `SKILL.md`'s gate table, resolvable entry, a `--selftest` over isolated fixtures whose tally is fail 0, and a committed mutant its own selftest catches | operability 7 | `python3 .ufo/waves/round-44/count-c2.py 1429c791 --counter …` → `check counters_present FAIL (absent)` → `C2=unmet`, exit 1 (`evidence/control-c2-donothing.txt`) | `python3 .ufo/waves/round-44/count-c2.py <landed tip> --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py --counter .ufo/waves/round-44/count-c3.py` → `C2=met`, exit 0 |
| C3 | FR5 ground the lane did not hold enters the corpus: the `Z`/`X` process-state alphabet and the three worlds a zero-character `/proc/<pid>/cmdline` read is consistent with, with mined rows whose `used-by` names the entry, a census-green registry and a README map row | coverage 6 | `git grep -l 'Z ゾンビ' 1429c791 -- corpus/` → 0 files; registry 243 rows (`evidence/control-c3-donothing.txt`) | `python3 .ufo/waves/round-44/count-c3.py <landed tip> --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472` → `C3=met`, exit 0 |

Witnesses (the classes the round-43 closure routed):
`count-c1.py <tip> --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv` →
`C1=unmet mismatches=2`, naming F03 (asserted 15, observed 14) and F04
(asserted 34, observed 8); `tools/mori-gate-registry.py --rev <tip> --audit
.ufo/waves/round-43/count-c1s.py --audit .ufo/waves/round-43/count-c2.py` →
`REGISTRY=unmet` (`evidence/witness-r43-gates.txt`).

Kill rules as frozen: a do-nothing control cannot print `C1=met`, `C2=met` or
`C3=met` (the three entering-tip receipts above); a ledger whose rows are not
single `git` pipelines naming `@REV@` is rejected, not scored; a row below the
floor is rejected; a registry row missing a standard cell, naming an
unresolvable path, or a counter without `--selftest` fails `C2`; a mutant a
counter's own selftest cannot catch fails `C2`; a token quoted by no opened
source fails the C3 Gate.

### Round 44 correction appended before the after-measurement — the C3 ground sentence's "three worlds"

Appended after the declaration above; the declaration's bytes are not rewritten
(the frozen contract's P-C3 sentence keeps its wording). Evidence: the opened
pages, `w1/ScoutSources490.md` §5–§6.2.

The declaration's C3 cell says "the three worlds a zero-character
`/proc/<pid>/cmdline` read is consistent with". That phrasing is **superseded**:
the two opened pages ground **two** worlds — the pid never existed, and the pid
exists and is a zombie (`Z`) or `X` dead — plus a third, "swapped out", that only
the Linux-1.3.11-era zh_TW translation states and that the focal ja page
contradicts on the adjacent `comm` field (「スワップアウトされているかどうかによらず、
見ることができる。」 vs 「該檔案是否可見取決於該檔案是否已被交換出記憶體」). The
admitted entry asserts the two grounded worlds, records the third as a retired
translation-level claim, and gains the `Z`/`X` state alphabet with its `X`
version qualifier. The measured predicate P-C3 is unchanged: the token
`Z ゾンビ`, the two `mined` rows whose `used-by` names the entry, a census-green
registry and a README map row.

### Round 44 post-data corrections (appended before the report lands; the declaration above is not rewritten)

Wave-1 seats falsified four things in the declaration and one in the round-43
record. All are append-only corrections; frozen instrument bytes stay unchanged.

1. **C3's axis is depth, not coverage** (`w1/CritPredicates.md`; the lane's own
   admitted ruling at `corpus/lessons/round-31-verifier-spotcheck.md:156` says
   "The frontier step (+14 SOURCES rows, README FR5/D5 map rows) is not an axis
   claim"). The round's C3 changes what the lane can *say and show* about a pid
   probe — a decision-grade knowledge move — not the fraction of domain surfaces
   governed. **C3 = depth (5, tied lowest)**, and coverage is **not claimed as
   moved**. C1 remains calibration (5) and C2 operability (7); the three claims
   keep distinct axes and the lowest-axis obligation is met by C1 and C3.
2. **C3's novelty is narrower than the declaration says.** The zero-character
   `cmdline` read and the `Z` state are already held
   (`corpus/knowledge/watchdog-identity-r31.md:27,29`, S170/S167/S171), and
   S171's scope already names `X`. The new ground the entry actually lands is the
   **measured mm-less world** — 1698 of 1931 `/proc` entries read a zero-length
   `cmdline` and every one was state `I` (1489) or `S` (209), so the state letter
   does **not** separate an mm-less kernel thread from a sleeping user process
   (`evidence/cmdline-empty-by-state.txt`) — plus the two translations'
   disagreement on `comm` under swap, and the `ENOENT` boundary for a pid that
   does not exist. The entry states the held/new split in its own Claim.
3. **The P-C3 after-figure "1 file" is wrong.** `git grep -l 'Z ゾンビ'` at the
   landed tip finds **3** files: the entry, the S471 `anchor` cell and the
   `corpus/README.md` map row (`w1/RevScorecardPlanned.md`). The measured
   after-value is 3, and the ledger carries it as `F03`.
4. **C2's declared after-command is incomplete.** The frozen counter's
   `--mutants-dir` default (`fixtures/mutants`, lane-relative) does not exist, so
   the declared form prints `C2=unmet` on `mutant_kill`. The runnable form — the
   one this round measured — is
   `python3 .ufo/waves/round-44/count-c2.py <tip> --counter .ufo/waves/round-44/count-c1.py
   --counter .ufo/waves/round-44/count-c2.py --counter .ufo/waves/round-44/count-c3.py
   --mutants-dir .ufo/waves/round-44/fixtures/mutants`. The `SKILL.md` row's entry
   cell carries the same gap; correcting it in place would break the freeze pin, so
   it is routed to round 45 and disclosed in the report.
5. **C2 was already met at the freeze commit**, before any data seat: the
   capability landed with the instruments. The honest before/after is therefore
   "entering tip → freeze commit", and the round-44 data wave added no part of it.
   Disclosed; the claim is still measured, but it is not a data-wave product.
6. **C3's frozen counter is satisfiable only under an environment override.**
   `count-c3.py` stages the registry at `$TMPDIR/c3-*/SOURCES.md` while
   `sources-census.sh --file` resolves `used-by` against `dirname(file)/..`, so
   every repo-relative `used-by` misses (279 `E11`, exit 1). The after-measurement
   runs with `TMPDIR=<lane>`; the defect and its fix are routed to round 45.
7. **Round-43 SCORECARD cells are superseded.** The round-43 measured-outcome
   section says `C1S` printed "15 checks PASS" and names `dde525ea` as the
   measured tip. Superseded: the counter prints **14** check lines
   (`git show 91cb221f:.ufo/waves/round-43/evidence/c1s-after.txt | grep -cE '^check'`
   → 14), and the receipt of record for this round is
   `evidence/c1s-tip-run.txt` at the round-44 tip (14 checks PASS, `C1S=met`,
   exit 0). The round-43 cells are not rewritten; this note supersedes their
   numbers.

## Planned (round 45)

1. **C1's vacuity, closed**: a revision-sensitivity arm — each ledger row's value
   must differ from its value at a second revision (or be declared a constant with
   a reason), plus distinct ids and distinct commands, no `WORK` mode for scoring,
   an absent path is a FAIL not a zero, and the floors non-overridable
   (`w1/MutC1.md`, `w1/CritC1Vacuity.md`, `w1/ExecJunkLedger.md`).
2. **C2's instrument honesty**: `selftest_tally` must read the parsed tally
   (`fail==0`, `pass>=min_arms`, rc 0) instead of `" pass=" in t`; each mutant must
   be a byte-diff of its counter that disables exactly one check; the auditor must
   read every standard-header table in `SKILL.md`, resolve the *row's* entry path,
   and reject duplicate rows; the registry cells' write-scope claims must be
   corrected by an append-only superseding row (`w1/CritSelftestHonesty.md`,
   `w1/MutRegistry.md`, `w1/SentTools.md`, `w1/ExecGateInventory.md`).
3. **C3's census arm**: mirror the registry at `<repo>/corpus/SOURCES.md` (or pass
   `--root`) so `used-by` resolves without `TMPDIR`; pin the census script in the
   freeze manifest; make `source:`/`coverage-map:` token-exact.
4. **Instruments' exit maps**: move `git rev-parse` inside the `try`, so a git
   timeout prints `*_SETUP` exit 2 instead of a traceback exit 1; scrub `GIT_*`
   from the child environment; give `count-c1.py`'s `bash -c` rows a
   producer-rc/pipefail gate and forbid command substitution
   (`w1/RevVerdictMap.md`, `w1/SentTools.md`).
5. **Carried**: `considerthese` P3 (repository growth from scratch output) is
   still unimplemented; the lane's 14 unregistered gates and 3 tools without a
   `--selftest` mode stay open (the inventory is in the round-44 report).

### Round 44 measured outcome (L1 lane subagent, mori-r44) — landing commit `5157cdda`

Measured at `5157cdda41ca711da280a85e7d3ec13da6ec85d3`; receipts under
`.ufo/waves/round-44/after/`.

| # | axis / score | after (one command over committed bytes) | verdict proposed for the closure |
|---|---|---|---|
| C1 | calibration 5 | `python3 .ufo/waves/round-44/count-c1.py 5157cdda…` → 16 rows, 5 classes, all checks PASS, `C1=met mismatches=0`, exit 0 (`after/c1-after.txt`); witness `fixtures/figures-r43.tsv` → `C1=unmet mismatches=2` (`evidence/witness-r43-figures.txt`); do-nothing at the entering tip → `C1=unmet` (`evidence/control-c1-donothing.txt`) | **verified (measured), with a disclosed vacuity limitation.** The predicate's measured half holds: a committed ledger is re-derived at the measured revision. The content half — that each row is a figure the report states — is **not** machine-checked: two seats reached `C1=met` with a twelve-row ledger of revision-constant figures (`w1/ExecJunkLedger.md`) and with HEAD-reading rows (`w1/MutC1.md`), and `C1=met` can coexist with the round-43 slips at one revision because the witness's asserted column was transcribed from prose (`w1/CritC1Vacuity.md`). QUALITY 117's "Not covered" carries this; the tightening is round-45 item 1 |
| C2 | operability 7 | `python3 .ufo/waves/round-44/count-c2.py 5157cdda… --counter …count-c1.py --counter …count-c2.py --counter …count-c3.py --mutants-dir .ufo/waves/round-44/fixtures/mutants` → five checks PASS, `C2=met`, exit 0 (`after/c2-after.txt`); the two round-43 counters audit `REGISTRY=unmet` (`evidence/witness-r43-gates.txt`); entering tip → `C2=unmet` (`evidence/control-c2-donothing.txt`) | **verified (measured), with disclosed instrument limits.** All three round counters are registered with eight cells, resolve, and their selftests catch a committed mutant of themselves. Limits: `--mutants-dir` is required (the default path does not exist); `selftest_tally` accepts a failure-shaped tally (`w1/CritSelftestHonesty.md`, `w1/RevRegistryRows.md` D3); the auditor reads only the first gate table and its row selection flips under duplicates (`w1/MutRegistry.md`, `w1/ExecGateInventory.md`); the registry write-scope cells are false as written for `--repo`/`bash -c` use (`w1/SentTools.md`) |
| C3 | depth 5 (re-attributed from coverage post-data) | `TMPDIR=<lane> python3 .ufo/waves/round-44/count-c3.py 5157cdda… --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472` → five checks PASS, `C3=met`, exit 0 (`after/c3-after.txt`); census `--root … mori` → `ok`, exit 0, 245 rows (`evidence/census-end.txt`); the `Z ゾンビ` sweep at the entering tip → 0 files (`evidence/control-c3-donothing.txt`) and 3 at the landing commit (ledger `F03`) | **verified (measured), narrower than declared.** The measured predicate holds; the novelty is narrower than the declaration's cell (correction 2 above): the zero-character read and `Z` were already held, and the new ground is the measured mm-less world, the translations' disagreement and the `ENOENT` boundary. The counter is satisfiable only with `TMPDIR=<lane>` (defect M3) |

Held: coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6 —
no scalar score moves; the three claims repair routed defects and add one measured
knowledge world at held scores, the lane's established pattern. Round shape: ONE
v1 wave, 32 seats (12 attack roles = 37.5%), 31 reports returned, 1 seat still
running at landing (`RevLedgerVsReport`); no wave 2 (fewer than 32 distinct attack
items on landed bytes by landing time — the residual surface is the round-45 plan
above). Round total: 32 seats.

## Round 45 — closure-reconciled claims (measured landing `baabc9929f0f272f3a99cd0a7816a2cb35fda835`)

Non-author closure: `corpus/lessons/round-45-verifier-spotcheck.md:42-72`. Score changes were not admitted; scores remain coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6.

| Claim | Axis | Before → after; measured outcome | Closure verdict |
|---|---|---|---|
| C1 ledger gate stops being vacuous | operability | Round-44 counter reports `C1=met` on 3/3 vacuity witnesses; round-45 counter rejects 3/3. | improved |
| C2 registry stops overstating | calibration | Unregistered members 14→0 and missing selftests 1→0; closure finds 4 stale registry cells at the landing commit. | harmed |
| C3 sourced cgroup-level naming entry | depth | Entry absent→present; S473 mined and used by the entry; census rc 0. | improved |

Round-45 closure reports quality harmed due to stale registry cells and the false 29/29 freeze-manifest tally; the latter was corrected append-only in `LOG.md` round 46. Evidence and re-derivation: round-45 verifier spot-check above. No score delta is claimed.

## Round 46 — calibration repair

Claim C1 (calibration, held score 5): four round-45 `SKILL.md` registry rows have measured pins. Frozen counter `python3 .ufo/waves/round-46/count-repins.py <SKILL.md>` printed `MORI_R45_REPINS mismatches=4 rows=4` (exit 1) for committed `control-skill.md` and `mismatches=0 rows=4` (exit 0) for repaired `SKILL.md`; counter SHA-256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`. However, CritControl/CritVerdict demonstrated that stale receipt strings placed in another cell of each row also yield zero mismatches, and the counter does not re-measure live tools. **Verdict: unprovable** for the frozen predicate; the corrected cells are independently corroborated but the counter is not a calibration-grade mismatch measure. No score delta is claimed. Evidence: `.ufo/waves/round-46/w1/CritControl.md`, `CritVerdict.md`, and `corpus/lessons/round-46.md`.

## Round 47 — registry pins re-measured from committed bytes (C1) and the v7.2 OOM tracepoint catalogue (C2)

L1 MoriR47, attempt 1. Entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`; freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`
(`.ufo/waves/round-47/contract.md`, both counters and the controls committed before any seat). Scores entering:
coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis.
No score change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before (entering `2d85e33`) | After (measured at `af2250d8`) | Verdict proposed for the closure |
|---|---|---|---|---|---|
| C1 SKILL.md registry self-test pins reproduce from committed bytes | calibration 5 | `python3 <git show 63eecf27:tools/mori-pin-check.py> --rev R --min-tally-pins 26 --baseline-rev 2d85e33d…` | `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1` (`SKILL.md:912` pinned `pass=15`, tool prints `pass=22`), rc 1 — `evidence/control-c1-donothing.txt` | `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0`, rc 0 — `evidence/after-c1-v1-frozen.txt` | **unprovable**: the frozen scorer prints `met`, but it is also green on five junk edits (`evidence/v1-junk/`, `w2/CritC1Verdict.md`); the landed change is honest (`w2/ExecDiffScope.md`) and passes the hardened v2 (`evidence/after-c1-v2.txt`), which scores every junk variant unmet (`evidence/v2/`) |
| C2 OOM tracepoint catalogue entry (FR13) | depth 5 | `python3 .ufo/waves/round-47/count-c2.py R` | `C2=unmet … failed=entry_absent,pins,source_row`, rc 1 — `evidence/control-c2-donothing.txt` | `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok`, rc 0 — `evidence/after-c2.txt` | met; limits: prose and lifecycle claims are not counted, and a used-by survivor / indented-row miss are recorded (`corpus/lessons/round-47.md` M5) |

Controls that skip the work stay unmet: C1 do-nothing, deleted row, moved-cell and truncated pin
(`evidence/control-c1-*.txt`); C2 do-nothing, the staged entry byte-exact and the staged "three tracepoints"
claim as a table (`evidence/control-c2-*-at-freeze.txt`).

### capabilities: first demonstrated round 47

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| registry pin reconciler (v2) | re-run every tally and digest pin in SKILL.md's self-test cells from a `git archive` export of a revision and refuse rebinding, inline code, `.scratch` paths, weakened pins, stale echoes, duplicate or hidden rows | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0`; `.ufo/waves/round-47/evidence/after-c1-v2.txt`; `evidence/v2/` vs `evidence/v1-junk/` | 47 |

## Round 48 — the pin reconciler cannot be turned green by structural junk (C1) and the filesystem-quota entry (C2)

L1 MoriR48, attempt 1. Entering tip `e5dbac05459887d9597ea5d1da0d8e3d024e0d17`; freeze `4387cf94b69ddce455051a1ff38e93795c2e6cde`
(`.ufo/waves/round-48/contract.md`; both counters, the controls and the four source copies committed before any seat).
Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest
(tied 5) axis. No score change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before (entering `e5dbac05`) | After |
|---|---|---|---|---|
| C1 the pin reconciler rejects eight frozen junk edits and accepts four honest edits and the real registry | calibration 5 | `python3 .ufo/waves/round-48/count-c1.py --tool tools/mori-pin-check.py --rev R` | entering tool: `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12`, rc 1 — `evidence/control-c1-tool-v2-entering.txt`; `stub-always-met`: `junk_met=8`; `stub-always-unmet`: `honest_unmet=4 real=unmet` | measured at the landed tip, appended below |
| C2 the FR2 filesystem-quota entry: ≥8 rows, each a located quote | depth 5 | `python3 .ufo/waves/round-48/count-c2.py R` | `C2=unmet claims=0 … failed=entry_absent,pins`, rc 1 — `evidence/control-c2-donothing.txt` | measured at the landed tip, appended below |

Controls that skip the work stay unmet: C1 entering tool, both stubs (`evidence/control-c1-*.txt`); C2 do-nothing and the
22 `C2_SELFTEST` arms (altered quote, wrong copy, short/long/duplicate quote, unmined row, other-day row, missing
`used-by`, digest mismatch).

Limits named before data (contract): the variants are eight junk classes found by round-47 seats, not the class of all
junk; the counter does not run the tool's own selftest; a located quote proves the words exist in the copy, not that the
claim follows from them. Wave 1 added two harness-level limits (`corpus/lessons/round-48.md` Wave 1): a tool keyed on the
harness's variant filename passes C1, and script/JSON text inside a copy passes C2's quote check.

### capabilities: demonstrated round 48

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| junk-variant calibration counter | score a registry checker against eight named junk edits and four honest edits plus the real registry, so a checker that rejects everything or accepts everything both fail | `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0`; controls `evidence/control-c1-*.txt` | 48 |
| unlanded-work check | list every uncommitted, modified or staged file under the round directory, `corpus/`, `tools/` and top-level `*.md` before a report is filed | `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0` | 48 |

### Round 48 measured outcome (appended after wave 2; the table above is the declaration)

| Claim | After (measured at `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`; the tool and counter bytes are unchanged at the final tip) | Verdict proposed for the closure |
|---|---|---|
| C1 | `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12`, rc 0 — `.ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt`; re-run `w2/R48ExecRerunC1.md`, clone replay `w2/R48ExecRerunC1Clone.md` | **verified (proposed) on the frozen counter, with named limits:** the counter is met by a tool keyed on the harness's filename (`w1/CritC1Counter.md` F1, `w2/R48CritFreeze.md`), and the landed v3 still scores `met` on seven of fourteen new junk probes (`w2/R48CritV3Junk1.md`). The landed tool holds no harness branch (`w2/R48RevHarnessLeak.md`). |
| C2 | `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok` — receipt `evidence/after-c2-final.txt` (re-measured after the one overclaim row of `w2/R48RevEntryXfs.md` was reworded) | **verified (proposed);** limits: a located quote does not prove the claim; script/JSON text in a page also passes (`w1/CritC2Counter.md`) — none of the 15 quotes sits in script text (`w2/R48RevC2Counter.md`, `w2/R48ScoutEntryContext.md`) |

No axis table cell changed and no score change is claimed. Capability rows above stand: the junk-variant counter and the
unlanded check ran and their selftests pass; the v3 reconciler is the tool the C1 run measured. Axis harm: `w2/R48RevSkillScore.md` found the
Axes table unchanged. Planned (round 49): close the seven v3 survivors of `R48CritV3Junk1` and rule R11 for D7 (`R48ExecD7`);
add the selftest arms the mutation seats named; a successor C1 counter that hides the variant identity from the tool and
includes an honest edit that updates a pin.

## Round 49 — the pin reconciler reads what a reader sees (C1) and the journal-reach entry (C2)

L1 MoriR49, attempt 1. Entering tip `b3e3453d`; freeze `0df17b7b` (`.ufo/waves/round-49/contract.md`). Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6; no score change is claimed by the lane.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 reconciler rejects 18 junk edits, accepts 7 honest edits and the real registry, variants handed over under opaque names | calibration 5 | `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev R` | entering v3: `C1=unmet junk_met=9 … variants=26`; stubs and the filename sniffer unmet | measured at the landed tip (see the report) |
| C2 journal-reach entry, ≥8 located quotes over ≥3 sources | depth 5 | `python3 .ufo/waves/round-49/count-c2.py R` | `C2=unmet … failed=entry_absent,pins` | `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=4 …` at `24ebc799` |

Controls (all unmet before data): do-nothing, `stub-always-met`, `stub-always-unmet`, `stub-filename-sniffer` (met under the round-48 counter), `tool-r48-surface-fixes` (`junk_met=1`), `tool-r48-r11-only` (`junk_met=7`). Feasibility witness disclosed: `tool-r48-merged-witness` meets the predicate.

### capabilities: demonstrated round 49

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| opaque-handle junk-variant counter | score a registry checker on 18 junk and 7 honest edits without handing it a variant name; the name-keyed stub fails | `python3 .ufo/waves/round-49/count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0`; sniffer pair in `evidence/` | 49 |
| flagged-versus-fixed count | count a round's critic flags against its landing diff | `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` → `flagged=45 fixed=18 unfixed=9` (round 48) | 49 |

Limits and planned round 50: the handle is content-derived and the selftest covers a twin of `plan()` (`w1/Mo49CritC1Counter.md`, `Mo49MutC1Counter.md`); C2 measures location, not depth (`Mo49CritC2Counter.md`); K4, the R11 carve-out and a randomised handle are routed; a wave 2 was not run this round.

## Round 50 — the self-assessment agrees with the fleet record (C1) and the memcg OOM report block (C2)

L1 MoriR50a2, attempt 2. Entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`; freeze
`950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (`.ufo/waves/round-50/contract.md`; both counters, the controls, the
receipts and the three source copies committed before any seat); data
`487941b9395e89678af0053cc443cdb49cdee6e3`. Attempt 1 dispatched wave w1 (40 seats, 5 reports on disk) and died in
an orchestrator host crash; the orchestrator salvaged its tree at `9b8562a3`. Scores entering: coverage 6,
operability 7, depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis. No score
change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the self-assessment agrees with the fleet `MANIFEST.json` and with the instruments | calibration 5 | `python3 .ufo/waves/round-50/count-c1.py R` | `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch`, rc 1 — `evidence/control-c1-do-nothing.txt` | `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3`, rc 0 — `evidence/a2-c1-at-data.txt` |
| C2 the memcg OOM report block and `memory.stat`, 22 located quotes over 3 sources (FR1) | depth 5 | `python3 .ufo/waves/round-50/count-c2.py R` | `C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=entry_absent,pins`, rc 1 — `evidence/control-c2-donothing-git.txt` | `C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3`, rc 0 — `evidence/a2-c2-at-data.txt` |

The C1 landing is in the `## Axes` table and `SHONEN.md`: the round-50 correction paragraph under the table
(`SCORECARD.md:21-29`) records the four lagging cells and states that scores are unchanged because
no closure states a new number; the four Last change cells now lead with rounds 47, 47, 49 and 49 and each Evidence
cell names the newer round's closure file; SHONEN's two tally pins read `(114/114)` and `(17/17)` and cite committed
receipts `evidence/selftests/mori-pin-check.txt` and `evidence/selftests/mori-unlanded-check.txt`. The C2 landing is
`corpus/knowledge/oom-memcg-stat-r50.md` with rows S489–S491 (opened 2026-10-26) and the three copies under
`corpus/evidence/sources-r50/`.

Controls that skip the work stay unmet (all receipts under `.ufo/waves/round-50/evidence/`): C1 do-nothing
`mismatches=6`, all-latest `mismatches=6`, pins-deleted `pins=0 … failed=mismatch,pins_floor`,
pins-updated-no-receipt `mismatches=6`, axes-only `mismatches=2`, shonen-only `mismatches=4`, box-dropped
`boxes=3 … failed=boxes_floor,mismatch,pins_floor`; C2 do-nothing `failed=entry_absent`, the git do-nothing
`failed=entry_absent,pins`, and the three byte-exact staged-entry controls
`failed=claims_floor,provenance,source_rows,sources_floor,table`. Feasibility witness disclosed:
`control-c1-witness.txt` (both halves plus receipts, built by the L1's script) meets the C1 predicate. Counter
selftests: `C1_SELFTEST pass=34 fail=0`, `C2_SELFTEST pass=31 fail=0` (`evidence/selftest-c1.txt`,
`evidence/selftest-c2.txt`).

No capability row is claimed this round: both counters and both self-testable tools predate round 50, and the
round's new artifacts are knowledge and receipts rather than instruments.

Limits named before data: the Score column is not checked (verdicts, not scores); the Last-change convention is
read, not judged; the hidden scan is SHONEN.md only; a matching tally proves the instrument prints the number, not
that its arms are good; the fleet MANIFEST is trusted, not re-judged; a located quote proves the words occur in the
committed copy, not that the claim follows from them; the three-new-words floor is a floor; the entry says what
v7.2 prints, not what this host printed (no kernel MESSAGE grep, S351/QUALITY 15). Wave a2w1 re-opened all 22 C2 rows
and the prose; its overclaims were corrected in the data before landing, and the counter weaknesses it found are named
limits (`corpus/lessons/round-50.md` `## Wave a2w1 — integrated findings`, M4). The after values at the landed tip are
in the round report and `.ufo/waves/round-50/evidence/a2-c{1,2}-at-landed.txt`.

Planned (round 51): the two live producers of lane `.scratch/` residue (`tools/mori-pin-check.py:884-887` exports a
full tree into the lane; `.ufo/waves/round-40/conform.py:69` hardcodes the lane path) as an instrument fix with its
own counter; K4 beyond `SHONEN.md` (tally pins in `QUALITY.md`, `README.md`, `LOG.md`); a successor C1 counter that
closes the named survivors (verdict-word substring, second `## Axes`, symlinked pin path, the `admitted` filter arm).

## Round 51 — hermetic pin re-execution with env/stale classes (C1) and MemAvailable as the kernel's estimate (C2)

L1 MoriR51, attempt 1. Entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`; freeze
`4677910eae6df3dabd38fe9a0daf1945146a1110` (`.ufo/waves/round-51/contract.md`); data
`87e0c374537557754bf71dd68036ded3ddc6699c`. Scores entering: coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6; C2 works a lowest (tied 5) axis. No score change is claimed by the lane; the non-author
closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 a `--rev` pin re-execution leaves nothing in the repo it reads when killed, holds with the lane path hidden, and classes every mismatch env or stale | operability 7 | `python3 .ufo/waves/round-51/count-c1.py R [--scratch DIR]` | `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 … failed=kill_residue,relocated,classified`, rc 1 — `evidence/control-c1-do-nothing.txt` | `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=125,fail=0`, rc 0 — `evidence/c1-at-landed.txt` |
| C2 what `/proc/meminfo`'s MemAvailable is at v7.2, 21 located quotes over 5 sources, each row with a non-L1 entailment vote | depth 5 | `python3 .ufo/waves/round-51/count-c2.py R` | `C2=unmet claims=0 … pins=bad … failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` | `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0`, rc 0 — `evidence/c2-at-landed.txt` |

Controls that skip the work stay unmet (receipts under `.ufo/waves/round-51/evidence/`): C1 do-nothing,
scratch-only (`reloc_mismatch=3`), conform-only (`kill_residue=12478`, `classified=bad`), class-only
(`kill_residue=1`), always-env (`classified=bad`); the witness (feasibility, built by the L1) met. C2 do-nothing
`failed=entry_absent,pins`, and the data commit before any vote `failed=entailment` (`evidence/c2-at-data.txt`).
Counter selftest `C2_SELFTEST pass=34 fail=0`; `count-c1.py` has no selftest (controls instead).

No capability row is claimed: the pin reconciler predates round 51 (v5/v5.1 change how it runs, not what it can do).

Limits named before data and found by the wave (`corpus/lessons/round-51.md` `## Wave w1 — integrated findings`):
arm A kills at one moment and runs the revision's code unsandboxed; arm B checks exit code and last line; arm D
parses a printed tally; arm C's fixture is five rows; the entailment arm accepts any non-`MoriR51` `.md` under `w1/`
and one vote per row; a vote records a seat's judgment, not its correctness; the entry claims v7.2 bytes only.

Planned (round 52): the successor calibration counter and K4 beyond `SHONEN.md` (round-50 §5 item 3, not taken this
round); the remaining in-lane writers (round-38/39/41/42 `conform.py`, round-48/49 `count-c1.py` scratch under the
lane) as a hermeticity sweep with its own counter.


## Round 52 — the self-assessment agrees with the fleet record, its instruments and its own pointers (C1) and CommitLimit/Committed_AS at v7.2 (C2)

L1 MoriR52, attempt 1. Entering tip `4f266ef2`; freeze `d3a8ea59` (`.ufo/waves/round-52/contract.md`; both
counters, C1 controls, receipts, source copies); data `8524904a`. Scores entering: coverage 6, operability 7,
depth 5, freshness 5, calibration 5, adjacency 6; both claims work a lowest (tied 5) axis. No score change is
claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the self-assessment agrees with the fleet MANIFEST, its instruments and its own pointers, with K4 taken beyond SHONEN to the living pins of QUALITY.md and README.md | calibration 5 | `python3 .ufo/waves/round-52/count-c1.py R` | `C1=unmet items=37 … living=4 superseded=1 locators=25 mismatches=8 errors=0 hidden=0 lane_writes=0 … failed=mismatch`, rc 1 — `evidence/control-c1-do-nothing.txt` | `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0`, rc 0 — `evidence/c1-at-landed.txt` |
| C2 what /proc/meminfo's CommitLimit and Committed_AS are at v7.2, 28 located quotes over 5 sources, each row with two non-author entailment votes | depth 5 | `python3 .ufo/waves/round-52/count-c2.py R` | `C2=unmet claims=0 … pins=bad … failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` | `C2=met claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=28 dissent=0`, rc 0 — `evidence/c2-at-landed.txt` |

Controls that skip the work stay unmet (receipts under `.ufo/waves/round-52/evidence/`): C1 do-nothing
(`mismatches=8`), axes-only (5), receipts-only (6), living-only (5), rewrite-in-place (`pin_removed_or_rewritten`
×3), delete-stale-pins (×3), repeat-stale-tally (×3); the witness (feasibility, built by the L1 with
`controls/c1-data.py`) met. Counter selftests `C1_SELFTEST pass=42 fail=0`, `C2_SELFTEST pass=45 fail=0`
(`evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`). The C2 data commit before any vote read
`failed=entailment` (`evidence/c2-at-data.txt`); rows 3, 27 and 28 were replaced in-round after overclaim votes
and re-voted by non-author voters.

No capability row is claimed: the K4 arm extends the round-50 calibration counter; the entailment arm extends the
round-51 depth counter.

Limits named before data and found by the wave (`corpus/lessons/round-52.md` `## Wave w1 — integrated findings`):
arm A's verdict comparison is pinned only to `admitted` (a `startswith` mutant survived); the `superseded()`
guard for the pin's own criterion survived; receipts are pure text (a handwritten receipt passes); the newest
closure file is trusted verbatim for scores; `lane_writes` measures working-tree churn (concurrent writers flip a
run to unmet — final runs therefore use a quiescent tree); a supersede line quoting a stale span requires no
replacement pin tied to the subject; the locator arm covers only the Axes rows and SHONEN boxes (QUALITY/README
hold 78 more pointers); C2's voter distinctness is by filename and a REPLACE line is the only authorship signal.

Planned (round 53): the in-lane writers' successor freeze (round-38/39/41/42 `conform.py`, round-48/49
`count-c1.py`); the locator sweep beyond the Axes rows; the C1 arm-isolating controls for M4/M8 and the
receipt/closure trust gaps; a commit-ledger census line (CommitLimit/Committed_AS) and a mode-2 error band; the
PROVINCE/SCORECARD present-tense tally pins (K4 scope).

**Round-52 correction:** the round-52 C1 row's After cell above carries the superseded tally `items=42 axes=6
pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0` and must be read as
`items=43 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0`. The
receipt that row cites (`.ufo/waves/round-52/evidence/c1-at-landed.txt:45`, measured
`e7e056b8a17e54516a3c17798221c30e9902c250`) prints the 43/28 form with `manifest=6209bdb8e400`, rc 0; the two
superseded tokens are verbatim the at-data tally (`.ufo/waves/round-52/evidence/c1-at-data.txt:44`, measured
`8524904adb25e44f24d9f25aac7eae909625c18c`), written before the landed receipt existed. Every other token, the
`C1=met` verdict and the exit code agree; the row above is retained as filed (append-only; round-52 closure D2,
routed defect 1; drafted by `.ufo/waves/round-53/w1/Mo53ScribeScorecard.md` Draft 1).

## Round 53 — the release-pinned quotes re-verified at Linux v7.3 (C1) and the commit ledger as a runway read (C2)

L1 MoriR53 (attempt 1: freeze, data, wave w1, data corrections) and MoriR53a2 (attempt 2, after the orchestrator
session exit killed attempt 1 at 2026-10-26 23:57:36 -03; salvage commit `0df803033fba2386b10f5dcc6aa96bdef65cba15`).
Entering tip `20edafa59b38dac1ca358893f0259b1f436372d3` (round-52 verifier spot-check); freeze
`f4da3fd400fa88a6db8ea544a4f7045c15d2410e` (`.ufo/waves/round-53/contract.md`; both counters, controls, receipts,
both counter selftests, census-start, sweeps, twelve source copies); data `2a4213bf8da72f7cd78189baa5bb9be825dca1df`;
data corrections after the wave `fd86307ad54c13edb8b6dd13182a2ad196f42fcd`. Scores entering: coverage 6, operability
7, depth 5, freshness 5, calibration 5, adjacency 6; C1 works a lowest (tied 5) axis and C2 is a coverage move with
a capability row. No score change is claimed by the lane; the non-author closure rules.

| Claim | Axis (held) | Counting command | Before | After |
|---|---|---|---|---|
| C1 the release-pinned located-quote claims of `memavailable-estimate-r51.md` and `overcommit-commit-limit-r52.md` re-verified at Linux v7.3: one ledger row per claim hash (46), each with a v7.3 source row, a located v7.3 quote and a `holds`/`changed` disposition, and two RECHECK voters per row whose final line carries that disposition, neither a proposer of the row's quote | freshness 5 | `python3 .ufo/waves/round-53/count-c1.py R` | `C1=unmet scope=46 rows=0 matched=0 status_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 … failed=ledger_absent,pins`, rc 1 — `evidence/control-c1-do-nothing.txt` (R = `20edafa5`) | `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0`, rc 0 — `evidence/c1-at-salvage.txt` (R = `0df80303`; the at-landed re-run is named in the round-53 report) |
| C2 the commit ledger (`CommitLimit` / `Committed_AS`) as a runway surface `tools/mori-commit-runway.py` reads by overcommit mode, with the mode-2 per-CPU error band and a `--selftest` over its own fixtures | coverage 6 | `python3 .ufo/waves/round-53/count-c2.py R [--scratch DIR]` | `C2=unmet tool=absent selftest=error n=0 fixtures=80 agree=0 disagree=0 registry=bad live=error failed=registry,tool_absent`, rc 1 — `evidence/control-c2-do-nothing.txt` (R = `20edafa5`) | `C2=met tool=present selftest=pass n=31 fixtures=80 agree=80 disagree=0 registry=ok live=ok`, rc 0 — `evidence/c2-at-salvage.txt` (R = `0df80303`; the data commit read `n=23`, `evidence/c2-at-data.txt`; the at-landed re-run is named in the round-53 report) |

The C1 landing is `corpus/knowledge/kernel-v7.3-recheck-r53.md` with rows S502–S510 and the nine pinned v7.3 copies
under `corpus/evidence/sources-r53/`; the ledger's 46 table rows are byte-identical between the voted data commit
`2a4213bf` and `0df80303` (`git diff 2a4213bf 0df80303 -- corpus/knowledge/kernel-v7.3-recheck-r53.md` touches no
`| <12 hex> |` row). The C2 landing is `tools/mori-commit-runway.py` with `tools/fixtures/mori-commit-runway/cases.json`
(26 cases; `--selftest` `PASS 31/31` with five built-in hostile checks), the `## Round53` registry row in `SKILL.md`,
the band entry `corpus/knowledge/commit-runway-read-r53.md` and rows S511–S514.

Controls that skip the work stay unmet (receipts under `.ufo/waves/round-53/evidence/`, readings in the table at the
end of the contract): C1 do-nothing `rows=0 … pins=bad … failed=ledger_absent,pins`; all-held
`status_ok=44 quote_ok=44 … voted=46 dissent=0`, `failed=quote,status` — labelling everything held fails exactly the
two MAP_NORESERVE rows; v72-copies `held=46 absent=0 … pins=bad`, `failed=pins,quote,status`; no-votes
`status_ok=46 quote_ok=46 … voted=0`, `failed=votes`; the witness (feasibility only, built by the L1 with
`controls/c1-data.py`) met. C2 do-nothing `tool=absent … failed=registry,tool_absent`; mode-blind
`agree=53 disagree=27`, `failed=fixtures`; no-band `agree=71 disagree=9`; memoriser `agree=71 disagree=9`, exact on
the frozen 16 and wrong on the seeded near-edge cases (the junk tools print a fake `PASS 12/12` selftest, so the
fixture arm is what separates them); the witness (the counter's REF wrapped as a tool, `n=12` at the floor) met,
disclosed. Counter selftests `C1_SELFTEST pass=37 fail=0` and `C2_SELFTEST pass=30 fail=0`
(`evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`).

### capabilities: first demonstrated round 53

Capability rows (demonstrated running this round; the closure admits them, and the register's `key` cell is filled
then — the round-41 shape):

| key | name | what it can now do | evidence | first working |
|---|---|---|---|---|
| round-53 C2 | commit runway read by overcommit mode | Reads `CommitLimit` and `Committed_AS` from `/proc/meminfo`, five `/proc/sys/vm` files, the present-CPU mask and the page size (bounded, non-blocking reads) and prints one `mori-commit-runway-v1` JSON object whose verdict follows the mode: `COMMIT_HEURISTIC` (mode 0, never LOW, `single_request_cap_kb`), `COMMIT_UNLIMITED` (mode 1, never LOW), `COMMIT_OK` / `COMMIT_LOW` (mode 2 — LOW, exit 1, iff `usable_kb` = limit − committed − `admin_reserve_kbytes` − `user_reserve_kbytes` is at or below `band_kb` = batch × present CPUs × page), `COMMIT_UNKNOWN` (exit 2) on a missing, unreadable or malformed input; on this host (mode 0) it prints `COMMIT_HEURISTIC`, exit 0, with the limit recomputed equal to the printed one | `python3 -I -B tools/mori-commit-runway.py --selftest` (`PASS 31/31`); `evidence/c2-at-salvage.txt`; `w1/Mo53ExecHostLive.md` | 53 |

Limits named before data (the wave's own findings land in `corpus/lessons/round-53.md` `## Wave w1 — integrated
findings`): `held` proves the v7.2 quote's words still occur somewhere in the v7.3 file, not at the same place nor
with the same meaning — the disposition and its two votes carry the meaning; the vote arm proves two lane seats
recorded a judgment, not outside verification; D covers the claim tables of the two entries only (46 rows); the
pins prove the bytes are what the L1 fetched (the wave re-fetched them by two independent channels and found them
equal); C2's REF function and the tool share one author, so a shared misreading of the kernel passes both (two
independent kernel-derived oracles agreed, `w1/Mo53ExecFixtureOracleA.md`, `w1/Mo53ExecFixtureOracleB.md`); the band
is an upper bound from the batch rule with present CPUs and totalram at read time, not a measured deviation; the
seeded fixtures are derivable from the commit id; the live leg compares stable fields only — this host reads mode
0, so the mode-2 band arm is exercised by fixtures, not live. Counter weaknesses the wave names are routed for round
54 and were not fixed in-round (frozen bytes).

Planned (round 54): the round-52 standing limits carried in as routed defect 3 — the locator arm's scope
(`QUALITY.md` and `README.md` hold 78 pointers it does not read), receipts that are pure text, and arm A's verdict
pinned only to `admitted`; the items `Planned (round 53)` named and this round did not take (the in-lane writers'
successor freeze including round-40 `conform.py`, the locator sweep beyond the Axes rows, the C1 arm-isolating
controls); the v7.3 trigger for what D does not cover (`oom-tracepoints-r47.md`, `oom-victim-selection-r27.md`,
`disk-write-rate-r33.md`, `watchdog-identity-r31.md`, the round-50 memcg entry, S511–S513); a row-vs-citation arm
for SCORECARD claim rows (lesson M1); the frozen-counter weaknesses routed from wave w1 (lesson `## Wave w1 —
integrated findings`: filename-keyed voter identity, the C2 exit-code arm, REF importable from the archive); FR8's
calibrated `COMMIT_LOW` threshold, which needs measured refusal behaviour and is not a counter change; the 30
round-52 flags dropped without an owner (lesson considerthese section).

**Round-53 correction:** the round-53 C1 and C2 After cells above cite the at-salvage receipts
`evidence/c1-at-salvage.txt` and `evidence/c2-at-salvage.txt` (R = `0df803033fba2386b10f5dcc6aa96bdef65cba15`);
the landed measurement of those rows is `.ufo/waves/round-53/evidence/c1-at-landed.txt` and
`.ufo/waves/round-53/evidence/c2-at-landed.txt` (R = `0b36d23e596276c70725873621fe15a28c87189f`, the revision the
round-53 report measures). The verdict lines are token-identical apart from `rev=` (`diff` of the `C1=`/`C2=` lines
with `rev=` removed prints nothing, round-54 L1), so no number in the cells changes; the rows are retained as filed
(append-only; round-53 closure D2, routed defect 1; lesson `corpus/lessons/round-54.md` M1).

**Round-50 correction:** the same pattern, found by the round-54 sweep (`.ufo/waves/round-54/checks/receipt-stage.py
39dcf4d7`): the round-50 C1 and C2 After cells cite `evidence/a2-c1-at-data.txt` and `evidence/a2-c2-at-data.txt`
(R = `487941b9395e89678af0053cc443cdb49cdee6e3`), while `.ufo/waves/round-50/evidence/a2-c1-at-landed.txt` and
`.ufo/waves/round-50/evidence/a2-c2-at-landed.txt` (R = `bae8656ea74a8ea3a4f2cf784e15cbeb91d9ad7d`) hold the landed
measurement; the `C1=`/`C2=` lines are token-identical apart from `rev=` (`manifest=a94551c5bc8d` in both C1 lines).
Rows retained as filed (lesson `corpus/lessons/round-54.md` M1).

## Round 54 — C1 freshness and C2 hardware memory-failure kills

Measured at `f111d4b0120a04ed1a0a2270a72ec0a343d20e29`. Entering `39dcf4d7`; freeze `6830f3af`; data `1116c092`; wave `2d0347a3`; data corrections `78295c76`, `782c6e7d`, `c71d088a`. Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. C1 freshness and C2 depth work tied-lowest axes; no scalar score delta.

| Claim | Axis | Counting command | Before | After |
|---|---|---|---|---|
| C1: all 31 remaining claim-table rows pinned to Linux v7.2 have a v7.3 copy, derived status, located quote, quote-start line and two-voter disposition | freshness 5 | `python3 .ufo/waves/round-54/count-c1.py R` | `C1=unmet scope=31 rows=0 … failed=ledger_absent,pins`, rc 1 — `evidence/control-c1-do-nothing.txt` | `C1=met scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=31 dissent=0`, rc 0 — `evidence/c1-at-landed.txt` |
| C2: a source-linked 21-row depth entry on hardware memory-failure kills outside the OOM-victim path, every quote located in its own v7.3 copy and two settled entailment votes per claim | depth 5 | `python3 .ufo/waves/round-54/count-c2.py R` | `C2=unmet claims=0 … failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` | `C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=6 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0`, rc 0 — `evidence/c2-at-landed.txt` |

Limits: all C1 rows are `held`; 31/31 v7.2 quotes already occur at v7.3, and ten rows use byte-identical tag copies, so those status/disposition arms do not discriminate. Four other release-triggered artefacts remain outside C1's exact table scope. C2's results-name binding does not prove report authorship; a fabricated results file could assert two voter names. C2 quote normalization can join source lines. No memory-failure event was observed live; host counters are zero. Ten control clone revisions were removed and could not be replayed independently; receipts are first-run observations, not durable revision proofs.

No capability row. No-harm reviewer found no axis harmed. Sources census 287→298 rows; end validator rc 0, 23 W04. Assimilation none; S262/S268 quarantine rows source-checked in the lesson, no package item adopted. considerthese suggestion 3 completed. No installs; L0 none. Stale-lane: respawn-per-round, no other mission open. Trend verdicts: expansion improved, quality improved, discernment unchanged pending non-author closure.

Planned (round 55): the four other release-triggered artefacts outside C1's claim-table scope; a C2 voter-authenticity control; append-only superseding rows for the S508/S520 anchor gaps; durable control-tree witnesses.

**Round-55 correction to the Round-54 limits paragraph above:** the captured control observation is 12/14 control-clone revisions unavailable, not “Ten”; the other two are not stated to be removed. The old sentence is preserved append-only, as routed by the round-54 verifier spot-check D3.

## Round 55 — C1 freshness (Linux v7.3 release recheck of out-of-ledger pointers) and C2 depth (ENOSPC runway beyond the df block column)

Measured at `a27ec48210b136d9f2fd1b71c5e64f65f5a30e22` (w1 settlement integration). Entering `ca52426e`; freeze `c9b908f0`; data `b8b7064c`; dispatch `b8a70adf`. Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. C1 freshness and C2 depth work tied-lowest axes; no scalar score delta. Both claims land **unmet** on their frozen vote arms, with every data arm green; verdicts and causes are measured receipts, not judgments.

| Claim | Axis | Counting command | Before | After |
|---|---|---|---|---|
| C1: all 78 out-of-ledger v7.2 line pointers from the four entries have a v7.3 row with counter-derived status, in-bounds lines, correct pins and 2+ output-bound agreeing RECHECK voters per row | freshness 5 | `python3 .ufo/waves/round-55/count-c1.py R` | `C1=unmet scope=78 rows=0 … failed=ledger_absent,pins`, rc 1 — `evidence/control-c1-do-nothing.txt` at `ca52426e` | `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 … failed=votes`, rc 1 — `evidence/c1-at-landed.txt` at `a27ec482` |
| C2: a source-linked 23-claim depth entry on block/inode ENOSPC runway across XFS/btrfs/tmpfs, every quote located, ≥16 claims/6 sources, and 2+ output-bound ENTAIL voters per row with no overclaim | depth 5 | `python3 .ufo/waves/round-55/count-c2.py R` | `C2=unmet claims=0 … failed=entry_absent,pins`, rc 1 — `evidence/control-c2-do-nothing.txt` at `ca52426e` | `C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9 source_rows=ok pins=ok provenance=ok entailed=15 dissent=8 … failed=entailment`, rc 1 — `evidence/c2-at-landed.txt` at `a27ec482` |

Limits (named before data, confirmed after): C1's data arms pass 78/78 (69 same / 7 moved / 2 changed, zero broken, all `holds`, pins and provenance ok). The vote arm fails on two recorded causes — (1) output-shape binding: the frozen C1 counter binds a vote only when the captured output carries the exact `RECHECK <h> <w>` line as a stripped text line, and all 15 reporting voters' outputs are structured JSON yields whose `vote_lines` arrays quote the lines, so `voted=0`; the same round's C2 counter implements "contains" as substring and binds the identical shape (`entailed=15`); (2) latent coverage: even under a substring reading the tally is 68/78 (0 dissent) because 10 rows were assigned to `Mo55Rc13`+`Mo55Rc14` and `Mo55Rc14` settled with no vote lines (`Mo55Rc14` output = malformed prose, no report file). C2: 15/23 rows carry two bound entailing votes; 8 rows (1, 2, 7, 11, 12, 14, 16, 23) carry at least one `overclaim` vote from the frozen ENTAIL voter set and the kill rule counts any overclaim as dissent — Mo55Rev02's adjudication (D1–D5) and the voter rationales are recorded in the round-55 lesson. Votes are lane seats, not outside verification; the results binding proves the orchestrator recorded a seat of that name whose output repeats the line, not who wrote the report bytes.

Wave: one v2 `w1`, 64 seats (reviewer 28 — the 16 Rc and 12 En voters, critic 12, mutation-tester 6, executor 4, scribe 4, scout 2, connector 2, sentinel 2, revenger 2, simplifier 2). All 64 settled with outputs; 63 report files (`Mo55Rc14` report absent). One lost seat: `Mo55Rc14` (malformed settlement, no vote lines, no report). Attack share ≥25%. `Mo55Mut05` settlement-arm probes 15/15 match the frozen predicate. Census 298→298 rows (18 anchor/scope cells corrected in place, no row added or dropped); end validator rc 0, 23 W04 (`evidence/census-end.txt`). Assimilation none; quarantine slice 3 rows adjudicated — S262/S268 PRESENT, S244 PRESENT at its arXiv companion with the publisher path still 403 (flip recorded append-only). considerthese checked. No installs; pacman paused; no L0 question. Stale-lane: respawn-per-round, no other mission open. Trend verdicts: expansion improved (18 source rows anchored + two knowledge entries landed), quality improved (registry locators, D6 prose reconciliation, receipts re-taken at the frozen data revision), discernment unchanged pending non-author closure.

Planned (round 56): voter final-output format rule (plain-text vote lines) or an operator ruling binding-semantics amendment; a dispatch validator cross-checking per-row voter coverage against settled vote-line shapes; the four other release-triggered artefacts outside C1's claim-table scope; the S508/S520 append-only superseding anchors; durable control-tree witnesses; C2 re-wording of the 8 dissenting rows with re-vote under whatever binding rule the operator rules.

## Round 56 — C1 coverage (FR5 driver-liveness probe) and C2 operability (dual-shape vote binder)

Measured at `3f494b49cde612d929e82887a48e1660c022c359` (freeze) and re-verified at the landed tip `097c342b6c7d71444c0d81c9615197dc87d59c50` (`evidence/c1-at-landed.txt`, `c2-at-landed.txt`). Entering `5b295eee`; data `c419fe6d` + `6ced9da9`; dispatch `acc62f54`. Scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6. C1 coverage (the lowest owned axis) and C2 operability work owned axes; no scalar score delta.

| Claim | Axis | Counting command | Before | After |
|---|---|---|---|---|
| C1: the FR5 driver-liveness probe is landed with frozen sha, 13-case selftest, 9 frozen fixtures at their frozen malformed counts, the S544-sourced entry, and no health-verdict string | coverage 6 | `python3 .ufo/waves/round-56/count-c1.py R` | `C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent`, rc 1 — `evidence/controls.txt` at `5b295eee` | `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359`, rc 0 — `evidence/c1-at-freeze.txt`; re-verified `rev=097c342b6c7d71444c0d81c9615197dc87d59c50`, rc 0 — `evidence/c1-at-landed.txt` |
| C2: the dual-shape seat-output vote binder is landed with frozen sha, 16-case selftest, and re-binds the round-55 RECHECK tally over committed bytes to the frozen line while the frozen r55 counter reads voted=0 on the same bytes | operability 7 | `python3 .ufo/waves/round-56/count-c2.py R` | `C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok failed=tool_absent`, rc 1 — `evidence/controls.txt` at `5b295eee` | `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49cde612d929e82887a48e1660c022c359`, rc 0 — `evidence/c2-at-freeze.txt`; re-verified `rev=097c342b…`, rc 0 — `evidence/c2-at-landed.txt` |


## Round 57 — current capability register continuation (append-only)

The active register is the last `## Capabilities` section: the round-35 contract explicitly says it supersedes the stale first-section table and per-round tables (`SCORECARD.md:1951-1961`). The r56 non-author closure admitted two capabilities in fleet `MANIFEST.json` `rounds[832].capabilities_added`; these rows were absent from the active register at the round-57 entering revision and are appended here under their exact closure keys. This is a register continuation, not a correction to the superseded first-section table.

| key | capability | what it can now do | evidence | first-working round |
|---|---|---|---|---|
| `rounds[832].capabilities_added[0]` | dual-shape seat-output vote binding | Binds final vote lines in plain-text and JSON string-scalar seat outputs; 16/16 selftest and round-55 tally re-bound 78/78 while the frozen r55 counter reads voted=0 on the same bytes. | `tools/mori-vote-bind.py`; `.ufo/waves/round-56/evidence/c2-at-landed.txt` | 56 |
| `rounds[832].capabilities_added[1]` | strict per-event driver-liveness probe | Parses inline watchdog log launch/complete/dead/wrap/fail events into per-lane log facts; 13/13 selftest; captured log 1728 lines, 0 malformed, 23 lanes; not a health verdict. | `tools/mori-driver-liveness.py`; `.ufo/waves/round-56/evidence/c1-at-landed.txt` | 56 |
