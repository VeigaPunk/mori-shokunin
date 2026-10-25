# CritC2Predicate — round 47 wave w1 — attack on P-C2

Seat: critic (leaf, no subagents). Target: **P-C2** (depth claim) as frozen in
`.ufo/waves/round-47/contract.md` and `count-c2.py` (sha256 `fc77b933…`).
Attacks: (a) reach `C2=met` with a junk entry — mechanical table from the header with
no prose; (b) wrong `emitted in` paths that still contain the string; (c) verdict on
"mechanically generated table" under `AXES.md` depth and addendum §9 (§do-nothing
control = lane-addendum §9 "Claim sizing", the do-nothing-control rule).

All counter runs below use the **frozen bytes** of `count-c2.py` (selftest 13/13
passes, rc=0). No tools installed (none needed; no pacman/uv/npx actions).
Scratch: `.scratch/r47-CritC2Predicate/` (created; fixture git repo inside). No
production file touched; only this report written.

## Method (how `--entry`/rev reading was tested)

`count-c2.py` reads every file with `git show <rev>:<path>` (`git_reader`), so an
uncommitted scratch entry is invisible to the CLI; the `--entry PATH` argument only
replaces the entry path, still resolved at a rev. Two equivalent harnesses were used:

1. **importlib dict reader** — load `count-c2.py` as a module, call
   `evaluate(read, PINS, rev)` with `read = lambda p: files.get(p)`, where `files`
   holds the pinned source blobs (working-tree bytes verified equal to the frozen
   sha256: `PIN_CHECK_working_tree True`), the real `corpus/SOURCES.md` (contains the
   committed S475 row), and the variant entry. This is the exact same code path the
   CLI takes after `git show`.
2. **CLI at a committed fixture rev** — fixture git repo `D` =
   `.scratch/r47-CritC2Predicate/tmp.6BV8BIYBoH` (`git init`, then verified
   `git -C "$D" rev-parse --show-toplevel` == `$D` before the first commit; local
   `user.name/email` set; no lane/jj state touched). Pinned v7.2 copies and
   SOURCES.md copied byte-exact into `D`, junk entry added, committed at
   `6424a1a…`; then `python3 count-c2.py <rev> --repo "$D" [--entry …]`
   (rc=0 met / 1 unmet / 2 setup).
## Attack battery — results (frozen counter)

All variants use the real v7.2 oom.h (8 events). "mech" = rows generated from the
header only: names + `TP_STRUCT__entry` field sets via the counter's own
`parse_events` (i.e., re-deriving the same sets), emitted-in = the single copy
containing `trace_<name>(` (substring grep). No prose anywhere; entry = provenance
block (source/verified-at/recheck, 3 lines) + table.

| # | variant | outcome (command-equiv) | exit |
|---|---|---|---|
| V1 | mechanical table, no prose (dict reader) | `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=scratch` | met |
| V1b | same bytes, CLI at fixture rev `6424a1a`, default ENTRY | `C2=met …` (identical line) | 0 |
| V1c | same, explicit `--entry corpus/knowledge/oom-tracepoints-r47.md` | `C2=met …` | 0 |
| V2 | staged "three tracepoints" claim as table | `C2=unmet … name_mismatch=5 … failed=name_mismatch` | 1 |
| V3 | one wrong emitted-in (`mark_victim`→`mm/page_alloc.c`; string absent there) | `… callsite_mismatch=1 failed=callsite_mismatch` | 1 |
| V4 | correct path **plus bogus citation** `` `mm/vmscan.c` `` in same cell | `C2=met …` (junk citation undetected) | met |
| V5 | two COPY_OF kernel paths in emitted-in cell | `… callsite_mismatch=8 failed=callsite_mismatch` | 1 |
| V6 | provenance only, no table | `… failed=table` | 1 |
| V7 | invented extra event row (`gamma`) | `… name_mismatch=1 failed=name_mismatch` | 1 |
| V8 | empty field cell for one event | `… field_mismatch=1 failed=field_mismatch` | 1 |
| V9 | name/fields columns swapped | `… name_mismatch=16 failed=name_mismatch` | 1 |
| V10 | extra decorative column (tracepoint\|fields\|emitted in\|note) | `C2=met …` (passed) | met |
| V11 | missing provenance keys | `… provenance=bad failed=provenance` | 1 |
| V12 | S475 row absent/queued | `… source_row=bad failed=source_row` | 1 |
| V13 | entry absent | `… failed=entry_absent` | 1 |
| — | pin tamper (selftest suite) | `failed=pins` | 1 |

The counter's own `--selftest` (13/13 PASS) independently reproduces the met and
unmet classes on its fake tree.

### Wrong "emitted in" path that still contains the string — analysis

The attack asks: claim file Y for event E where the *true* callsite is X, and Y
still contains `trace_E(`. For this to pass, the same `trace_<name>(` must appear
in two of the three committed copies. Scanned all 8 events × 3 copies:

```
callsites_each_event: oom_score_adj_update→[fs/proc/base.c]; reclaim_retry_zone→[mm/page_alloc.c];
mark_victim→[mm/oom_kill.c]; wake_reaper→[mm/oom_kill.c]; start_task_reaping→[mm/oom_kill.c];
finish_task_reaping→[mm/oom_kill.c]; skip_task_reaping→[mm/oom_kill.c]; compact_retry→[mm/page_alloc.c]
collision_wrong_path_still_matches: {event: [] for all 8}
```

Each call exists in **exactly one** of the three pinned copies → the wrong-path
attack is **not reachable with today's data** (V3 confirms rejection). The counter's
check is *presence of one matching call in the claimed copy*, so if two copies ever
contained the same call (e.g., a future kernel version emitting from two files), the
wrong attribution would pass — a latent structural point, not currently exploitable.
V5 shows listing two kernel paths in one cell is rejected (len(paths)!=1).

## Verdict: is a mechanically generated table a legitimate depth move or junk?

- **Under `AXES.md` depth** ("verifiable technical detail — decision tables with
  real thresholds, named error signatures, cited sources; a reader can act on
  SKILL.md alone; no filler"): the catalogue *table itself is the measured artifact*
  — names, per-event field sets, emitting call sites, all pinned to the committed
  v7.2 bytes. A mechanically generated table that carries exactly that data is
  verifiable technical detail and not filler: it equals the honest build entry's
  table byte-for-byte on the measured axes (build entry table verified identical:
  `build_entry_table_data_matches_header True rows=8`, differing only by ~5.9 KB of
  prose — lifecycle, the identity-bearing `mark_victim` point, boundaries, refusal of
  the staged "three" claim). So as *data* it is a legitimate depth move.
- **Under addendum §9 (do-nothing control)** ("A target must be one a do-nothing
  control cannot reach … build the cheapest control that skips the claimed work … if
  it meets the target, the counter or target is wrong"): the committed do-nothing
  controls are the *true* §9 probes, and both stay unmet with the frozen counter at
  the freeze commit `63eecf2`:
  - `controls/control-c2-staged.md` (staged entry byte-exact — no table):
    `C2=unmet events=8 rows=0 … failed=provenance,source_row,table` rc=1;
  - `controls/control-c2-three.md` (staged "three tracepoints" as table):
    `C2=unmet … name_mismatch=5 … failed=name_mismatch,source_row` rc=1.
  The mechanical generator (V1) does **not** skip the claimed work: it performs the
  exact extraction the claim defines (TRACE_EVENT names → TP_STRUCT__entry field sets
  → emitting call per event over the pinned copies). What it skips is only the
  unmeasured layer (prose/lifecycle/interpretation), which the frozen predicate's
  named limits explicitly exclude ("does not check prose"). V1 is therefore the
  *floor* of what passes, not a §9 violation.
- **What C2=met does and does not certify**: the counter certifies structural
  consistency with the committed header (8 names, 8 field sets, one emitting call per
  event, provenance block citing S475, S475 source row). It does not certify that a
  human read the header, nor that the entry has interpretive value. V4/V10 show
  junk payloads ride along (bogus extra citations, decorative columns) — noise, not
  false data. **No junk entry with false data reached `C2=met`** in any tested
  variant (V2–V3, V5–V9, V11–V13 all rejected on the expected axis). The counter
  separates fabricated events/fields/callsites reliably; it cannot separate a
  correct table without prose from a correct table with prose, which is the claim's
  declared limit. No counterexample against the frozen predicate surfaced; the
  smallest safe correction if stricter depth is wanted later: require a non-table
  prose section with the entry's claim (outside the current frozen predicate — would
  be a *new* rule, not a fix to this one).

## Observations on the lane state (read-only, evidence)

- Entering tip `2d85e33…` before-state, frozen counter, default entry:
  `C2=unmet events=0 rows=0 … pin_mismatch=4 … failed=entry_absent,pins,source_row`
  rc=1 — matches the contract's declared before-state.
- `refs/heads/master` = `63eecf2…` = freeze commit (origin/master same). Working
  tree (uncommitted, w1 build) holds the sources, `corpus/SOURCES.md` mods,
  `corpus/knowledge/oom-tracepoints-r47.md`, evidence receipts, and the control
  receipts; the counter at any committed rev cannot see them until the L1 lands the
  build commit (UNVERIFIED for the post-landing state).
- Selftest: `C2_SELFTEST pass=13 fail=0`, rc=0.

## Report trailer

Report paths relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`. This seat's
scratch: `.scratch/r47-CritC2Predicate/` (fixture repo
`tmp.6BV8BIYBoH`, revs `114c606d…` and `6424a1a…`). No production edits, no fleet
repo/sibling/jj/git mutations. No tool installs (no entry recorded).
