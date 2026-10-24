# Round 14 — ShonenScribe: four SHONEN evidence lines (report only)

Seat: `MoriR14.ShonenScribe` (leaf scribe, read-only). Lane: mori-shokunin. Milestone: restore OOM alarm and structured fleet routing (C1 coverage repair of the r13 `rejected-harmed` cutover).

**Boxes: none checked.** `SHONEN.md:5-8` remains four `[ ]` boxes; this report changes no mark. This report claims no non-author seat independence: no named non-author verifier is identified or ruled here (PROTOCOL.md:63-68; audit-r11.md:215 D20).

## Scope and boundaries

- Wrote only this file. No edits to `SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `tools/`, `corpus/`, or any sibling's build file.
- No builds, tests, lint, census, oracle, harness, or smoke runs. Reads and `grep` only.
- No git subcommands run.
- Tools installed or updated by this seat: **none**.
- No commits, no fleet or sibling writes.

## Inputs read

- `SHONEN.md:1-8` (four unchecked boxes, column-0 canonical form).
- `PROVINCE.md:3-16` (domain, owns, refuses), `:18-57` (out-of-province rule, core, frontier, adjacent table), `:79-81` (round-12 corrections).
- `SKILL.md:1-70` (decision table, error patterns, executable checklist, gates registry).
- `corpus/lessons/round-13-verifier-spotcheck.md` (closure file; see prior-closure state below).
- `corpus/lessons/round-13.md` (declared claims, Gate, reopened authorities, live task, "No SHONEN checkbox was checked").
- `LOG.md:722-756` (round 13) and `LOG.md:758-781` (round 14, entry in progress).
- `.ufo/waves/round-13/build/ReviewPromotion.md:7-47` (F1–F3 findings and per-box residuals).
- `tools/mori-census.sh` by grep only: `:893-918`, `:1025-1027`, `:2736-2790`.
- `.ufo/waves/round-14/` at read time: `spec.json`, `dispatch.json`, `build/swarm-registry.json` exist. No round-14 evidence file existed in `build/` yet.

## Prior closure state (round 13, `rejected-harmed`)

From `corpus/lessons/round-13-verifier-spotcheck.md`:

- Closure: status `ok`, `admitted: false`, verdict `rejected-harmed`.
- Per-axis: coverage **harmed**; adjacency **harmed**; operability improved; depth, freshness, calibration unchanged.
- Harm cited: the OOM critical/DRIFT alarm for kernel-OOM classes was demoted to INFO (`:1085–1095` at the reviewed revision); `UNIT_FAILURE_JOURNAL` was reused for all user-unit results with no fleet/non-fleet split and no tsukuroi owner label (`:1101–1102`); the unknown reason `no-anchored-structured-field` overstated the gap.
- Routed defects 1–7 include: restore OOM warning/DRIFT with structured metadata (1); restore fleet/non-fleet distinction and OS-owner routing (2); register the r13 verdict harness in SKILL gates (4); finish the correction sweep (6).
- Round-14 LOG entry (`LOG.md:758-781`) starts from entering HEAD `dbe85009…` and declares one claim, C1 coverage.

## The four asserted evidence lines

Each line below is an assertion with pointers. None is verified by this seat. None is a checked box.

### Line 1 — SKILL.md contains real decision tables, error patterns, checklists, cited sources

- **Asserted:** `SKILL.md` has `## Decision table` (`:11`), `## Error patterns` (`:22`), `## Checklist (executable)` (`:51`), and `## Gates` (`:58`) with a registry table (`:64-68`). Cited sources appear inline (`SKILL.md:28-31`: kernel `oom_kill.c`, `oomd-util.c`, `systemd.catalog.in`, `journal-fields`, `journalctl(1)`) and in `corpus/SOURCES.md` (`SKILL.md:70`).
- **Residual:** no sources section inside `SKILL.md` (ReviewPromotion F3, Box 1). The gates registry at `:64-68` lists census, drift pin, and silence oracle only. The r13 verdict harness `tools/mori-round13-regressions.py` is not registered there (round-13 closure defect 4).
- **Verifier:** none named non-author. Not claimed.

### Line 2 — At least one end-to-end domain task executed and logged in LOG.md

- **Asserted:** round-13 C1 live domain task is logged at `LOG.md:746`. Trigger: user-only text probe and FR1 system-scope gap. Action: frozen and delivered censuses bracketed by independent field-restricted journal queries. Outcome: 0 → 2 explicitly scoped journal surfaces; 12/12 class/scope cells matched. Evidence: `.ufo/waves/round-13/evidence/live-measurement.json`. An earlier census run is logged at `LOG.md:643-713` (round 12).
- **Residual:** the logged round-13 outcome was judged `rejected-harmed` on coverage (`round-13-verifier-spotcheck.md`). Its 12/12 live result is all-zero (`LOG.md:746`, `round-13.md:82-84`), so it is not positive-load validation.
- **Verifier:** none named non-author. Not claimed.

### Line 3 — Instructions executable by an agent without oral context

- **Asserted:** `SKILL.md:64-68` names entry commands and exit maps for census (`bash tools/mori-census.sh`), drift pin (`--drift <baseline>`), and silence oracle (`bash tools/mori-silence-cases.sh`). The round-13 harness command is pinned in `corpus/lessons/round-13.md:73-74` (`python3 tools/mori-round13-regressions.py --mutation both --jobs 1 --output .ufo/waves/round-13/evidence/regressions-accepted`).
- **Residuals:**
  1. The round-13 harness command is absent from the SKILL gates registry (closure defect 4).
  2. `SKILL.md:99-101` says the r10 drift baseline reads red from 2026-10-19; `LOG.md:754` records `--drift` exit 1 at `c13df48`. An agent following the registry gets red with no repair path stated. The baseline is not re-pinned.
  3. ReviewPromotion F3 Box 3 names the r11 "dead-baseline-recipe + inconsistent instructions" debt (`.ufo/reports/round-11/mori-goalwave.md:32-35`). Whether it is now executable is unverified; this seat did not re-execute it.
  4. The working-tree `SHONEN.md` indentation drift found in round 13 (`ReviewPromotion.md` F1) was restored per `LOG.md:735`. At read time `SHONEN.md:5-8` is column-0. Byte equality against HEAD was not measured here.
- **Verifier:** none named non-author. Not claimed.

### Line 4 — No cross-domain bleed; PROVINCE.md accurate

- **Asserted:** `PROVINCE.md:3-16` names the domain and the refusals (dispatch to kumitate; OS/systemd/driver/boot to tsukuroi; endpoint health to kama; credentials to kagi). `PROVINCE.md:46-57` is the adjacent table. `PROVINCE.md:79-81` records that the phrase "scratch roots" does not resolve to a measured target.
- **Residuals against this line:**
  1. **Adjacency harm at round-13 delivered bytes.** `UNIT_FAILURE_JOURNAL` is reused for all user-unit results and system-unit results lose the fleet split and tsukuroi owner label (closure, "No-harmed-axis check" item 3; adjacency harmed). At read time `tools/mori-census.sh:1026-1027` emits `UNIT_FAILURE_JOURNAL` (user) and `UNIT_FAILURE_JOURNAL_SYSTEM` (system). Grep finds no `UNIT_FAILURE_OUT_OF_SCOPE` emission. The working tree may be under edit by round-14 seats, so this is not a verified current state.
  2. **OOM alarm.** Grep at read time finds no `OOM_KILL_JOURNAL` emission in `tools/mori-census.sh`; its only occurrences are comments and the legacy-class guard at `:2788`. This matches the closure's "OOM critical alarm dropped" finding. It is a bleed concern only insofar as OS-owned unit state is routed through fleet findings.
  3. **"scratch roots" residual is stale at read time.** ReviewPromotion F3 Box 4 cited `PROVINCE.md:9` and `SKILL.md:18`. Grep at read time finds the phrase only at `PROVINCE.md:81`, as the correction itself. `PROVINCE.md:9` and `SKILL.md:18` no longer contain it. This is an observation, not a closure of the residual by a committed change.
- **Verifier:** none named non-author. Not claimed.

## Summary

| Box | Asserted pointer | Open residual at read time | Mark |
|---|---|---|---|
| 1 SKILL decision tables/error patterns/checklists/sources | `SKILL.md:11,22,51,58,64-68,28-31,70` | in-SKILL sources section absent; r13 harness unregistered | `[ ]` (unchanged) |
| 2 End-to-end domain task logged | `LOG.md:643-713`, `LOG.md:746`, `live-measurement.json` | r13 outcome `rejected-harmed`; live result all-zero | `[ ]` (unchanged) |
| 3 Executable without oral context | `SKILL.md:64-68,99-101`; `round-13.md:73-74`; `LOG.md:735,754` | harness command unregistered; red drift pin; r11 debt unverified | `[ ]` (unchanged) |
| 4 No cross-domain bleed; PROVINCE accurate | `PROVINCE.md:3-16,46-57,79-81`; `tools/mori-census.sh:1026-1027` | r13 unit-routing and OOM alarm loss at delivered bytes; "scratch roots" residual stale | `[ ]` (unchanged) |

Round-14 status: the repair is in flight. `LOG.md:758-781` declares C1 only. No round-14 evidence file existed in `build/` at read time. None of the four lines can be asserted as satisfied by round 14 yet.

## Checks for L1 (named, not run here)

1. `cmp SHONEN.md <(git show HEAD:SHONEN.md)` should be silent, with `git status --short -- SHONEN.md` empty (ReviewPromotion F1 check).
2. `SKILL.md` gates registry: confirm a row for `tools/mori-round13-regressions.py` (or its round-14 successor) exists, with entry command, verdict map, and pinned values.
3. After round-14 lands: grep `tools/mori-census.sh` for `OOM_KILL_JOURNAL` (expect a critical emission on the user path and DRIFT behavior per the round-14 claim) and for `UNIT_FAILURE_OUT_OF_SCOPE` (expect a non-fleet route with a tsukuroi owner label). Confirm the r13 frozen-vs-repaired regression command fails on frozen bytes and passes on repaired bytes (round-14 LOG entry).
4. Ruling on whether any sampling reviewer qualifies as non-author under D20 is for L1/lane. This seat makes no ruling.

## Findings in one line each

- No box is checked; none is satisfied by round 14 yet.
- The four lines are assertions with pointers and named residuals, not verified claims.
- Two residuals (`UNIT_FAILURE` routing, OOM alarm emission) remain open at read time; one residual ("scratch roots") is stale at read time.
- No non-author seat independence is claimed here.
