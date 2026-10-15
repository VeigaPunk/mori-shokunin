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
