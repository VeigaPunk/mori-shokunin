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
