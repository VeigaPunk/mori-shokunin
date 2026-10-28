# Mo60Reviewer16 — wave-shape conformance (mori round 60, wave w1)

Verdict: **CONFORMS**. One v2 wave, 64 seats (64 spawn / 0 resume), policy v2
band 64–128 applies, attack share **32/64 = 50.0%**, no duplicate seat name, no
unknown role. No blocking finding; three low-severity evidence notes (N1–N3)
and one definitional divergence (N4) follow.

## Pins (every number below is read from these bytes)

| object | pin |
|---|---|
| lane tip at review | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| dispatch blob | `HEAD:.ufo/waves/round-60/w1-dispatch.json` = `80170e9b06d46ceafb62db6afc2e9c0cf65e4627` |
| dispatch bytes | sha256 `cac7b022f451a2beb7cc1d4bf30ad76be78c52a7d68e2196b7b2b00dbae35277`, 63355 B, mtime 2026-10-28 12:53:03 −0300 |
| frozen contract | `HEAD:.ufo/waves/round-60/contract.md` = `b4bb16c833c21b805fec4939e13653eac88bf155` (sha256 `a444e270957b957875b667b3cd226b965234deda242db12a81df597e2c15441d`) |
| spec blob | `HEAD:.ufo/waves/round-60/w1-spec.json` = `960129c50e5eefefb593e1015e806632a82fba27` |
| entered | `ddfb12fb0838b4307c445194a844f0c4b1950195`, freeze amendment `ac496c7cde8cad965079858accae3bedfe4a73f2` (both ancestors of HEAD) |
| dispatch landed | commit `76904b21` ("validated w1 dispatch payload (64 seats, v2)"); blob `80170e9b…` is identical at `76904b21`, `398d3225`, `b3c25613` → the dispatch has not moved since it was validated, and working-tree bytes == HEAD bytes |

`w1-dispatch.json` is tracked (not `git check-ignore`d); working-tree sha256 ==
`git cat-file -p HEAD:…w1-dispatch.json | sha256sum`, so this is a pinned read,
not an unpinned tree read.

## Seat count and per-role counts

`counts` block, `w1-dispatch.json:16-20`:

```
{"spawn": 64, "resume": 0, "total": 64}
```

64 `taskCall.tasks` entries (`w1-dispatch.json:422-744`), matching
`counts.spawn` exactly; `resumeSends` is `[]`, matching `resume: 0`; no w2
dispatch exists in the wave dir (`ls .ufo/waves/round-60/*dispatch*` →
`w1-dispatch.json` only), so the round total is 64 in one wave, as
`contract.md:135-137` ("One v2 wave `w1`, 64 seats") requires.

| role | seats |
|---|---|
| reviewer | 16 |
| executor | 12 |
| critic | 8 |
| scribe | 6 |
| mutation-tester | 5 |
| scout | 4 |
| revenger | 4 |
| simplifier | 4 |
| sentinel | 3 |
| connector | 2 |
| **total** | **64** |

Rows sum to 64. Role set is exactly the ten proposal roles of
`ufo-wave-policy-v2.json` `nativeProfiles.omp-native-v1.proposalRoles` and of
`SWARM_ROLES` in `~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:263-276`
(independent authorities, identical set). No `planner` / `distiller` / `labrat`
/ `main` lane — correct: the validator rejects those as frozen-topology seats
(`ufo-swarm-wave.mjs:263-264`), and `lane-addendum.md:236-239` puts the §3
planner seat on the L1, which matches `contract.md:138`.

## Attack share

Contract formula (`contract.md:137-138`): reviewer + critic + mutation-tester +
sentinel over total.

```
16 + 8 + 5 + 3 = 32 ; 32 / 64 = 50.0%   ≥ 25%  PASS
```

Under the `lane-addendum.md:206-209` v2 wording instead (reviewer, critic,
mutation-tester, **labrat**), the result is `16+8+5+0 = 29 / 64 = 45.3%` — also
≥ 25%. Both definitions pass; see N4 for the wording divergence.

## Policy v2 band 64–128 applies

`policy` block (`w1-dispatch.json:4-15`): `source: "config"`, `maxLanes 256`,
`minLanes 16`, `waveMinLanes 64`, `waveMaxLanes 128`, `declaredMaxLanes null`,
`hardCeiling 256`, `globalRunnerCeiling 1056`.

Value-identical to `scripts/hyaku/ufo-wave-policy-v2.json`
`sha256 f12e1d6dfeae81a4a1ff805f8de50ec8386b3a16ae7f40b171f54c5236812fff`
`sighting.dispatch.swarm` on every shared key
(`maxLanes,minLanes,waveMinLanes,waveMaxLanes,rampBatchSize,rampIntervalMs`); key
diff is only dispatch-derived `source / declaredMaxLanes / hardCeiling /
globalRunnerCeiling` vs config `note`. `waveMinLanes 64 / waveMaxLanes 128` is
the v2 discriminator — v1 (`ufo-wave-policy.json`) is `waveMinLanes 32 /
waveMaxLanes 64`.

Band predicate re-derived from the validator source, not asserted:
`ufo-swarm-wave.mjs:837-848` (`policyFloor = min(waveMinLanes, maxLanes)`,
`policyCeiling = min(waveMaxLanes, maxLanes)`), `:898-908` (`cap = policy.maxLanes`
= 256 because `w1-spec.json` carries no `maxLanes`), `:1067-1092`
(`laneCeiling = min(policyCeiling, cap)`; spawn wave needs
`laneFloor ≤ total ≤ laneCeiling`).

```
laneFloor = min(64, 256) = 64 ; laneCeiling = min(128, 256) = 128 ; total = 64
64 >= 64  PASS (floor)      64 <= 128 PASS (ceiling)      no impossible_band
```

## Duplicate names — none

* dispatch: 64 names, 64 distinct, `duplicate_name` (`ufo-swarm-wave.mjs:1200`)
  cannot fire.
* spec items ↔ dispatch tasks: name sets equal, per-name role equal (0
  mismatches).
* embedded `registry.members` ↔ on-disk `w1/swarm-registry.json`: byte-equal
  member maps, 64 keys.
* registry keys ↔ dispatch names: no extras, no missing, per-name role equal.
* `w1.ready.dispatched` (2026-10-28T13:14:25): 64 handles, 64 distinct values,
  identity mapping, no missing/extra name — the dispatcher spawned
  `label=t['name']`, `agent=t['agent']` unchanged
  (`scripts/hyaku/inline-dispatcher.py:254-257`).
* all 64 names satisfy the validator's `MEMBER_NAME_PATTERN`
  `^[A-Z][A-Za-z0-9]{1,31}$` (`ufo-swarm-registry.mjs:33`), max length 20.
* 64 pairwise-distinct task bodies (the validator's `duplicate_expansion` gate
  cannot fire); every body starts `/skill:godspeed` and contains its own
  `Report: … w1/<name>.md` line.

## Unknown roles — none

Dispatch role set = `{reviewer, executor, critic, scribe, mutation-tester,
scout, revenger, simplifier, sentinel, connector}`; set difference against
`SWARM_ROLES` (`ufo-swarm-wave.mjs:263-276`) and against policy v2
`proposalRoles` is empty in both directions.

## Findings (non-blocking) and residual risk

* **N1 (informational, evidence pin).** The dispatch records no policy path or
  digest — only `source: "config"`. Identification as v2 rests on the
  `waveMinLanes 64 / waveMaxLanes 128` values, and that is necessary: the *count*
  64 sits inside **both** bands (v1 32–64 upper edge, v2 64–128 lower edge), so a
  reader checking only `counts.total` cannot tell v1 from v2. Value-match to
  `ufo-wave-policy-v2.json` is exact and v1 is excluded by `waveMinLanes 64`, so
  the claim holds; a future round would harden this by recording the resolved
  config path/sha in the dispatch (the same gap revenger r69 reported:
  policy resolves from `UFO_CONFIG_PATH`, `ufo-swarm-wave.mjs:143`).
* **N2 (informational, floor margin).** 64 == `waveMinLanes`, i.e. the wave
  passes the band with zero headroom at the floor. Any post-acceptance reduction
  (dropping seats, splitting the wave) would fail `too_few_lanes`
  (`ufo-swarm-wave.mjs:1083-1087`). The contract's fixed 64 is consistent; a dead
  seat must stay dead per `lane-addendum.md:229` and `:247` and must not be replaced.
* **N3 (informational, absolute paths).** The contract's considerthese item ("no
  r60 instrument carries an absolute host path") holds for the instruments:
  `grep -c /home/vgpnk` → `0` for `count-c1.py`, `count-c2.py`, `count-c3.py`,
  `build-fixtures-r60.py`. The *dispatch text* does carry them (72 occurrences:
  `taskCall.context` at `w1-dispatch.json:421` plus 49 seat bodies) — these are
  per-seat assignments, not instruments, and are also why the dispatch is
  host-specific. Recording it so the two surfaces are not conflated.
* **N4 (informational, wording divergence).** `lane-addendum.md:206-209` defines
  v2 attack roles as reviewer, critic, mutation-tester, **labrat**;
  `contract.md:137-138` and this seat spec use reviewer, critic,
  mutation-tester, **sentinel**. The wave contains 3 sentinels and 0 labrats. Both
  formulas clear 25% (50.0% / 45.3%), so no conformance failure — but the L1
  report should state which formula it quotes.
* **N5 (hygiene, out of scope).** `.ufo/waves/round-60/__pycache__/`
  (`count-c{1,2,3}.cpython-314.pyc`, mtime 13:15) was created inside the frozen
  wave dir by a seat importing the counters. It is gitignored
  (`.gitignore:3: __pycache__/`) so it cannot enter wave evidence, but it is
  scratch inside the frozen dir and should not be copied into a receipt sweep.
  `w1/`, `w1.ready`, `w1.ready.dispatched` are untracked at HEAD — expected
  mid-wave (their landing is the settlement sweep; `w1-dispatch.json:421` itself
  records that C1's data lands during this wave).

Residual risk / verification gaps:
* I did not execute the validator (it would resolve policy from
  `UFO_CONFIG_PATH` and write plan artifacts); the band verdict is a literal
  re-derivation of its predicate at `ufo-swarm-wave.mjs:837-848, 898-908,
  1067-1092` against the recorded policy values. If a future reader needs the
  validator's own emitted `policy` block, the L1 should attach the validated plan
  — the committed dispatch is the only record today.
* Role *mix* is a dispatch-record fact; delivered-seat mix must be read from
  `<wave>-results.json` at settlement (`lane-addendum.md:147-150`), which does not
  exist yet (`ls .ufo/waves/round-60/w1-*.json` → dispatch/spec only). Dead seats
  and any late-completion drift are outside this seat.
* Report-dir contents are in flight (21 seat reports present when checked); I
  verified names against the dispatch, not completeness.

## Reproduction (read-only, from the lane repo root)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin
git rev-parse HEAD                                   # b3c256138f00…
git rev-parse HEAD:.ufo/waves/round-60/w1-dispatch.json      # 80170e9b…
git cat-file -p HEAD:.ufo/waves/round-60/w1-dispatch.json | sha256sum
python3 - <<'PY'
import json, collections, re
d=json.load(open('.ufo/waves/round-60/w1-dispatch.json'))
tasks=d['taskCall']['tasks']; roles=collections.Counter(t['agent'] for t in tasks)
attack=sum(roles[r] for r in ('reviewer','critic','mutation-tester','sentinel'))
print(len(tasks), d['counts'], dict(roles), attack, attack/len(tasks))
print('band', d['policy']['waveMinLanes'], d['policy']['waveMaxLanes'],
      d['policy']['waveMinLanes'] <= d['counts']['total'] <= d['policy']['waveMaxLanes'])
print('dups', [n for n,c in collections.Counter(t['name'] for t in tasks).items() if c>1])
print('badnames', [t['name'] for t in tasks if not re.match(r'^[A-Z][A-Za-z0-9]{1,31}$', t['name'])])
PY
```

Scratch: `$HYAKU_SCRATCH/mori-r60/Mo60Reviewer16/` was created and left empty (no
clone, no counter run, no fixture); nothing to copy back and it is removed at
yield. Disk guard checked before work: all roots green (`/fast/scratch/hyaku`
26% used, 598.7 G free).
