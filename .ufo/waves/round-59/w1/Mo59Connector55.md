# Mo59Connector55 — sibling-overlap walk: wave settlement (kumitate) vs mori round 59 C2

Scope: read-only planning data-walk. No edits, no VCS mutation, no fleet/sibling writes, no scratch used.
Frozen inputs read: `.ufo/waves/round-59/contract.md#FC7E`, `count-c1.py#CAC3`, `count-c2.py#ED2B` (freeze 60b3a76a; entering 2b9f0397).

## 1. Who owns what (evidence)

| Surface | Owner per sources | Evidence |
|---|---|---|
| `ufo-swarm-results-v1` input, `collect` join, `ufo-mission-result-v1` envelope | kumitate doc claims ownership | `kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:98-140` (`## scripts/ufo-swarm-collect.mjs`): RESULTS_SCHEMA = `ufo-swarm-results-v1`; join requires one results row per dispatch member (`unmapped_member` / `unexpected_member`, cited at `collect.mjs:549/576` in the doc); "never a judge input and never a handoff path" |
| Wave CLI `plan`/`run`/`record`; `SWARM_ROLES` | kumitate doc | `swarm-wave-lifecycle.md:47-93`; `settle` verb explicitly removed by round-32 errata (`:37-45`, `:85-87`) |
| `WAVE_*` census signals (`WAVE_RESULTS_SCHEMA_DRIFT`, `WAVE_SETTLED_PARTIAL`, ...) | kumitate in OwnerMap | `.ufo/waves/shokunin12h-20261014-p4-mori-r1/members/OwnerMap.md:76-82` — a historical 2026-10-14 member report copy in mori's tree, not a live owner table. Its `settle` instructions (`:77`, `:78`) are stale per the round-32 errata. |
| Live hub implementation | sibling repo, not kumitate's tree | `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs`, `ufo-swarm-collect.mjs` (HEAD `fb7157fc`). `git -C kumitate-shokunin ls-files | grep ufo-swarm` → empty; no `scripts/ufo-swarm-*` in fleet `scripts/`. |
| mori C2 results family `*-results.json` | mori (orchestrator inline handoff) | `mori-settlement-scan.py:2-13` ("written beside `<wave>-dispatch.json` ... per the round-59 contract") |

## 2. Shape facts (exact)

- Live SWARM_ROLES: `ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:265-276` = scout, reviewer, critic, connector, sentinel, executor, mutation-tester, revenger, simplifier, scribe (10). Planner/distiller/labrat/Main excluded (`:263-264`).
- Mori scanner ROLES: `tools/mori-settlement-scan.py:39-40` = the same 10, **copied, not imported**. Set-equal today; no shared source, so drift is silent.
- kumitate's collect input is `ufo-swarm-results-v1` (`collect.mjs:66`; doc: members = `results.json` `members` array, name key). Mori's artifacts are a different family:
  - `.ufo/waves/round-54..58/w1-results.json`: top-level keys `lane, round, wave, seats, results`; **no `schema` key**; members under `results`; member keys exactly `{agent, name, note, output}`.
  - `.ufo/waves/round-53/w1-results.json`: keys `lane, note, outputs_recovered, results, round, seats, settled_by, spawned, wave`; 67 members, each with extra key `report_file`.
  - `.ufo/waves/round-58/evidence/w1-settlement.json`: `schema: mori-wave-settlement-v1` (mori's own per-seat scan, `tools/mori-wave-settlement.py:33`), a third shape.
  - Conclusion: no mori `*-results.json` is a `ufo-swarm-results-v1` payload. Collect would not accept them [INFERENCE from the doc's shape description; collect not executed — no scratch/run permitted for this walk].
- Read-only scan of committed artifacts (`python3 tools/mori-settlement-scan.py <files>`, no writes):
  - r54 74/74, r55 64/64, r56 64/64, r57 64/64, r58 64/64 → `SETTLEMENT_SCAN_OK`, failures=0, rc 0.
  - r53 → `SETTLEMENT_SCAN_FAIL`, rc 1; 67 failures of the form `member[i]:extra_keys=report_file`. Matches contract's expected drift arm.
- Role counts in r54–58: no `planner` in any row (consistent with the planner exclusion above).
- Tracked-ness: all seven artifact files are git-tracked in mori (`git ls-files`).

## 3. Overlap and contested scope

1. **Name overlap, shape divergence.** Both sides say "settlement results"; only the filename pattern and role vocabulary overlap. The C2 predicate ("members==seats", "role enum") is a self-consistency check, not kumitate's dispatch bijection. `members==seats` compares to the `seats` field (`mori-settlement-scan.py:61-63`), not to the dispatch registry. A results file with wrong names would still scan OK. The counter does not claim a join; the entry must not either.
2. **"Schema drift" label.** The frozen predicate and expected r53 arm say `report_file` is schema drift. That is drift only relative to mori's own shape (`mori-settlement-scan.py:41` MEMBER_KEYS). Relative to kumitate's vocabulary the r53 file is not a `ufo-swarm-results-v1` payload at all (no `schema`, no `members`). The lesson should say "mori-local shape drift" to avoid claiming kumitate's `WAVE_RESULTS_SCHEMA_DRIFT` semantics.
3. **Census blind spot (by design).** `tools/mori-census.sh` `probe_waves` (`:865-931`) iterates `$WAVES_DIR/*` and skips `round-*` dirs (`case "$base" in round-*|.*) continue`). Its settled tokens are `results.json | closeout.json | mission-result.json | closeout.md`, not `w1-results.json`. The round-N settlement artifacts are invisible to the census. C2 must not claim census coverage.
4. **Two mori settlement vocabularies.** `tools/mori-wave-settlement.py` (round 20) reads `ufo-swarm-wave-dispatch-v1` dispatch files (`:34`, `:346`) and emits `mori-wave-settlement-v1`. The C2 scanner reads results files with a mori-only shape and no schema key. Both claim "settlement" over `.ufo/waves/`. The round-59 entry should keep them distinct by name and not call either the other's verdict.
5. **Stale kumitate citations.** Doc line numbers do not match the live hub: doc says `ufo-swarm-wave.mjs:131` for SWARM_ROLES (live `:265`); `collect.mjs:54-58` for schemas (live `:66`). Doc's `settle` verb references are stale per its own round-32 errata. Treat kumitate's doc as a non-authoritative pointer. Do not cite its line numbers in the round-59 entry.
6. **Planner boundary (holds).** SWARM_ROLES excludes planner (`ufo-swarm-wave.mjs:263-264`; doc `:64-65`). Round-59 connector items carrying planning walks are consistent with that; the planner stays L1-held.
7. **Producer.** The C2 scanner docstring names "the inline spawn handoff's settlement artifact"; kumitate's `settle` verb does not exist (doc `:85-87`). The producer of `*-results.json` is mori's orchestrator, not kumitate collect. No kumitate-owned surface is written by this round. No cross-lane edit is implied.

## 4. Refusal and boundary summary

- Do not claim: a dispatch-bijection join, census coverage, collect acceptance, or kumitate schema drift for the r53 file.
- Do claim (grounded): mori-local shape validation (object, seats==len(results), member key-set, unique names, role enum from a copy of the 10-role set), read-only scan verdicts above.
- Drift risk to note in the lesson: the 10-role set is copied from `ufo-swarm-wave.mjs:265-276`; a future kumitate role addition would not reach the mori scanner.

## 5. Verification (read-only, exact commands)

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 60b3a76ad0524c8978cc51922940be1c8c388915:tools/mori-settlement-scan.py | sha256sum` → `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (matches frozen PIN).
- `python3 tools/mori-settlement-scan.py .ufo/waves/round-5{4,5,6,7,8}/w1-results.json` → SETTLEMENT_SCAN_OK, 0 failures.
- `python3 tools/mori-settlement-scan.py .ufo/waves/round-53/w1-results.json` → rc 1, `report_file` extra keys.
- `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-files | grep -i ufo-swarm` → no output.
- `find /home/vgpnk/Projects -maxdepth 6 -name 'ufo-swarm-*.mjs'` → only under `ufo-fsd-alpha/scripts/`.

Assimilation: none. Scratch: none created. Install/update: none.
