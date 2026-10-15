# mori-shokunin — Scorecard

Axes owned by this lane: **coverage + operability** (fleet-2); all six are scored
here, the owned pair drives the round's axis-move.

## Axes

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| coverage | 5 | six surfaces censed by one gate; the per-surface notes are still owed (`corpus/README.md` Known gaps) | round 1 |
| operability | 6 | `tools/mori-census.sh` runs live (exit 1 DRIFT on real findings) and `--selftest` passes 14/14 in a hermetic temp tree | round 1 |
| depth | 4 | finding-id vocabulary + per-surface semantics in `knowledge/observability-census-r1.md`; thresholds are stated, two are proposals | round 1 |
| freshness | 5 | the live receipt is dated and re-runnable; no drift pin yet | round 1 |
| calibration | 5 | unavailable ≠ unhealthy is enforced and fixture-proved; `progressing-weak` is declared deferred rather than faked | round 1 |
| adjacency | 6 | refuses dispatch (kumitate) and OS state (tsukuroi) in PROVINCE and in the gate | round 1 |

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
