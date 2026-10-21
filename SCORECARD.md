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
