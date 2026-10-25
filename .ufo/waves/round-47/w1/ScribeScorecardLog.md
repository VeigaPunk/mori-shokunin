# ScribeScorecardLog — round 47 wave w1 report

Seat: ScribeScorecardLog (leaf scribe). Assignment: draft the `SCORECARD.md` "## Round
47" section and the `LOG.md` round-47 entry for the mori-shokunin lane, from the frozen
contract, before the control receipts, at freeze commit
`63eecf2738db96f46b0bd02b1b2dfd66787493d0`, with a capabilities-table row for the
"registry pin reconciler" (`tools/mori-pin-check.py`) marked pending demonstration, and
`<TIP>` placeholders for the landed hash. No score change is claimed by the lane.

## Behavior (observed evidence)

All reads were read-only; no lane tool was executed (no scratch dir was needed), no
production file was edited, no install/update was performed (no tooling authorization
event).

- Lane HEAD at drafting time: `63eecf27` = freeze commit `63eecf2738db96f46b0bd02b1b2dfd66787493d0`
  (`git rev-parse HEAD`; `git log --oneline -8` shows the freeze commit
  "round-47: freeze — contract P-C1/P-C2, mori-pin-check.py, count-c2.py, controls,
  v7.2 OOM source copies, collision/quarantine scratch", parent entering tip
  `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`). The landed tip is not yet known; `<TIP>`
  is used as instructed.
- Contract read: `.ufo/waves/round-47/contract.md` (C1: `python3 tools/mori-pin-check.py
  --rev R --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`
  → `PIN_CHECK=met`, exit 0; C2: `python3 .ufo/waves/round-47/count-c2.py R` →
  `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0
  pin_mismatch=0 source_row=ok provenance=ok`; controls; kill rules; separability; round
  shape).
- Evidence receipts present under `.ufo/waves/round-47/evidence/` and read verbatim:
  - `control-c1-donothing.txt` — at entering tip: `PIN_CHECK=unmet tally_pins=26
    digest_pins=5 mismatches=1 unparsed=0 no_command=0 dropped=0`, rc=1; the sole
    mismatch is SKILL.md line 912 `MORI_SOURCES_APPENDONLY_SELFTEST` pinned
    `pass=15 fail=0` vs observed `pass=22 fail=0`.
  - `control-c1-deleted.txt` — `PIN_CHECK=unmet tally_pins=25 dropped=1`, rc=1.
  - `control-c1-moved.txt` — `PIN_CHECK=unmet mismatches=1`, rc=1 (stale tally kept in
    self-test cell).
  - `control-c1-truncated.txt` — `PIN_CHECK=unmet mismatches=1`, rc=1 (pin weakened to
    `pass=2`).
  - `control-c2-donothing.txt` — at entering tip: `C2=unmet events=0 rows=0
    name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=4 source_row=bad
    provenance=bad failed=entry_absent,pins,source_row`, rc=1.
  - `control-c2-staged.txt` — same `failed=entry_absent,pins,source_row`, rc=1.
  - `control-c2-three.txt` — same `failed=entry_absent,pins,source_row`, rc=1.
  - `control-c2-donothing-at-freeze.txt` — at freeze `63eecf27`:
    `C2=unmet events=8 rows=0 failed=entry_absent,source_row`, rc=1 (the eight
    TRACE_EVENTs resolve from the committed copies; the failure isolates to the entry).
  - `selftest-pin-check.txt` — `PIN_CHECK_SELFTEST pass=22 fail=0`, rc=0.
  - `selftest-c2.txt` — `C2_SELFTEST pass=13 fail=0`, rc=0.
  - `host-tracefs.txt` — read-only host tracefs oom reading (sudo -n ls/cat only): 8
    events listed (`compact_retry`, `finish_task_reaping`, `mark_victim`,
    `oom_score_adj_update`, `reclaim_retry_zone`, `skip_task_reaping`,
    `start_task_reaping`, `wake_reaper`), `enable` = 0, rc=0; user read denied (rc=2).
  - `census-start.txt` — sources census `mori ok`, rc=0, 23 W04 duplicate-url warnings
    only.
- Committed v7.2 source copies present under `corpus/evidence/sources-r47/`:
  `fs_proc_base.c`, `mm_page_alloc.c`, `mm_oom_kill.c`, `include_trace_events_oom.h`.
- SOURCES.md at freeze already carries S475 (Linux include/trace/events/oom.h at v7.2),
  S476 (mm/oom_kill.c, mm/page_alloc.c, fs/proc/base.c at v7.2) and S477 (host tracefs
  own-work receipt); S475 cites `TRACE_EVENT at lines 12, 34, 76, 118, 134, 150, 166,
  183` and the copy sha256.
- Staged assimilation entry (read-only, `/home/vgpnk/Projects/shokuknow/merge/mori/`):
  `knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` claims "The OOM lifecycle
  an observer can hook has exactly three named tracepoints" (`mark_victim`,
  `start_task_reaping`, `finish_task_reaping`), citing S507 (IEEE paper), vs the eight
  TRACE_EVENTs of the committed v7.2 oom.h copy — the C2 falsification target.

## Gates

Read-only (git rev-parse/log); no mutation of lane jj state, git index, fleet repo, or
production files. No tool installed.

## Touched surfaces

Only this report (`Report:` trailer below). No edits to SKILL.md, SOURCES.md, corpus/,
tools/, LOG.md, SCORECARD.md or any other production file.

## Findings

1. The C1 before-state receipt matches the contract byte-for-byte (SKILL.md:912 pin vs
   observed `pass=22 fail=0`; `PIN_CHECK=unmet` rc=1); all three C1 controls are red as
   frozen, and the deleted control exercises the `dropped=1` baseline class.
2. The C2 do-nothing control at the entering tip is red on `entry_absent,pins,source_row`
   (pins red because the entry is absent); the freeze-time re-score isolates the failure
   to `entry_absent,source_row` — the committed v7.2 copies already yield `events=8`.
3. The two frozen counters' selftests pass (22/22 and 13/13), and the selftest receipts
   exercise the falsification classes (stale tally, stale in cell, moved pin, tomb
   boundary, three-of-eight missing event, invented event, missing field, wrong
   callsite, pin tamper, no source row, no provenance, no table, duplicate row, queued
   source row).
4. Freeze commit confirmed; entering tip is its parent (so the "before" receipts at
   `2d85e33d` are the pre-freeze state per contract).
5. The capabilities register (SCORECARD.md "## Capabilities", round-35 register) admits
   rows only through a demonstrated run (S199); the new row is therefore drafted as
   **pending demonstration** below, per the assignment.

## Draft 1 — SCORECARD.md "## Round 47" section (fenced, ready for L1 integration)

```markdown
## Round 47 — registry pin reconciler (C1) and OOM tracepoint catalogue (C2) (freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`; measured landing `<TIP>`)

Contract: `.ufo/waves/round-47/contract.md` (frozen with the counters and controls at
`63eecf27`; entering tip `2d85e33d`). Claims: C1 calibration (held 5) and C2 depth
(held 5) — both lowest non-retired axes. No score change is claimed by the lane.

Counting commands (from the contract):

- C1: `python3 tools/mori-pin-check.py --rev R --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` → `PIN_CHECK=met`, exit 0 at the landed tip. At entering tip: `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1` (`evidence/control-c1-donothing.txt`; SKILL.md:912 pins `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, tool prints `pass=22 fail=0`).
- C2: `python3 .ufo/waves/round-47/count-c2.py R` → `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok` at the landed tip. At entering tip: `C2=unmet failed=entry_absent,pins,source_row` (`evidence/control-c2-donothing.txt`).

| Claim | Axis | Before → after; measured outcome | Verdict proposed for the closure |
|---|---|---|---|
| C1 — SKILL.md registry self-test pins reproduce from committed bytes (`tools/mori-pin-check.py`) | calibration 5 | entering tip `PIN_CHECK=unmet mismatches=1` (SKILL.md:912) → landed tip `<TIP>` `PIN_CHECK=met mismatches=0 unparsed=0 no_command=0 dropped=0`, tally_pins≥26, exit 0 (`evidence/control-c1-donothing.txt`; after receipt `<TIP>`) | `<TIP>` |
| C2 — OOM tracepoint catalogue, field by field, from the committed v7.2 oom.h copy, cited via S475 | depth 5 | entering tip `C2=unmet failed=entry_absent,pins,source_row`; at freeze `C2=unmet events=8 failed=entry_absent,source_row` → landed tip `<TIP>` `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok` (`evidence/control-c2-donothing-at-freeze.txt`; after receipt `<TIP>`) | `<TIP>` |

Controls (each scored with the frozen counter before data; each must stay unmet):
- C1: do-nothing (entering revision, `evidence/control-c1-donothing.txt`); `controls/control-c1-deleted.md` (stale row deleted — `dropped`, `evidence/control-c1-deleted.txt`); `controls/control-c1-moved.md` (true tally placed in another cell, stale tally kept in the self-test cell — `mismatch`, `evidence/control-c1-moved.txt`); `controls/control-c1-truncated.md` (pin weakened to `pass=2` — token-boundary `mismatch`, `evidence/control-c1-truncated.txt`).
- C2: do-nothing (entering revision, `evidence/control-c2-donothing.txt`); `controls/control-c2-staged.md` (staged entry byte-exact — no catalogue table, `evidence/control-c2-staged.txt`); `controls/control-c2-three.md` (the staged "three tracepoints" claim as a table — `name_mismatch`, `evidence/control-c2-three.txt`); re-scored at the freeze commit (`evidence/control-c2-donothing-at-freeze.txt`) so the failure isolates to the entry.

Kill rules: landed tip `PIN_CHECK=unmet` → C1 not verified; landed tip `C2=unmet` → C2 not verified; no re-scoring under a changed counter.

Selftests at freeze: `PIN_CHECK_SELFTEST pass=22 fail=0` rc 0 (`evidence/selftest-pin-check.txt`); `C2_SELFTEST pass=13 fail=0` rc 0 (`evidence/selftest-c2.txt`).

Held: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6 — no score move; the claims work the two lowest non-retired axes. No retirement, waiver, exploratory claim or promotion. Source census at wave start: `mori ok`, rc 0, W04 duplicate-url warnings only (`evidence/census-start.txt`). Named limits (contract): C1 checks no line-count pins (`743 lines`) or truncated digests (`37fd7c24ff52…`), a digest matches any file path named in its row, and each command runs once (no determinism proof); C2 checks names, field sets and one emitting call per event in the committed v7.2 copies — not prose, lifecycle ordering, or the host's running kernel (the host tracefs read `evidence/host-tracefs.txt` is separate own-work evidence, row S477).

Capabilities register — new row (this round), **pending demonstration**:

| key | name | what it can now do | evidence | first-working round |
|---|---|---|---|---|
| — pending (key assigned on admission) | registry pin reconciler | re-runs every self-test-cell pin — tally pins and full-sha256 digest pins — in every SKILL.md gate-registry table from the committed bytes of a revision, against the pinned tool commands, reporting mismatch/unparsed/no-command/dropped counts and a `PIN_CHECK=met|unmet` verdict with a minimum-tally-pins floor and an entering-baseline drop check | `tools/mori-pin-check.py`; `.ufo/waves/round-47/evidence/selftest-pin-check.txt` (22/22) and control receipts | `<TIP>` (if demonstrated and admitted; S199 — rows enter only through a round that demonstrates the capability running) |
```

## Draft 2 — LOG.md round-47 entry (fenced, ready for L1 integration)

```markdown
## Round 47 (L1 mori-r47) — registry pin reconciler + OOM tracepoint catalogue (wave w1 build)

Freeze commit `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (contract
`.ufo/waves/round-47/contract.md`, counters `tools/mori-pin-check.py` and
`.ufo/waves/round-47/count-c2.py`, controls, and the v7.2 source copies under
`corpus/evidence/sources-r47/`); entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`
(round 46, non-author closure). Landed tip: `<TIP>`.

Motivating evidence per claim:

- C1 (calibration, held 5): the round-46 closure routed defect 1 (replace
  `count-repins.py`, row-wide substring matching) and `considerthese/2026-10-25.md`
  suggestion 1; the entering-tip receipt `evidence/control-c1-donothing.txt` shows
  `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1` — SKILL.md:912 pins
  `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, the committed tool prints
  `pass=22 fail=0`.
- C2 (depth, held 5): the staged shokuknow entry
  `knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` claims "exactly three
  named tracepoints" (`mark_victim`, `start_task_reaping`, `finish_task_reaping`,
  citing S507), while the committed Linux v7.2 `include/trace/events/oom.h` copy
  (S475, TRACE_EVENT at lines 12, 34, 76, 118, 134, 150, 166, 183) defines eight; at
  the freeze the counter already resolves `events=8` with the entry absent
  (`evidence/control-c2-donothing-at-freeze.txt`: `C2=unmet failed=entry_absent,source_row`).

Measured at `<TIP>` (wave w2):

- `python3 tools/mori-pin-check.py --rev <TIP> --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` → `PIN_CHECK=met`, rc 0 (`evidence/control-c1-donothing.txt` before; after receipt replaced by <TIP>).
- `python3 .ufo/waves/round-47/count-c2.py <TIP>` → `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok`, rc 0 (before: `C2=unmet failed=entry_absent,pins,source_row`).
- Selftests at freeze: `PIN_CHECK_SELFTEST pass=22 fail=0`, `C2_SELFTEST pass=13 fail=0`, rc 0 both. Controls all unmet as frozen. Source census at wave start `mori ok`, rc 0 (W04 warnings only).

Wave record: two v1 waves (policy `scripts/hyaku/ufo-wave-policy.json`, band 32–64):
w1 build + first falsifiers, w2 falsify after landing. Per wave, `w1-spec.json` /
`w1-dispatch.json`; seat reports under `.ufo/waves/round-47/w1/`. Round total within
64–100.

Verdicts at `<TIP>`: C1 verified if `PIN_CHECK=met`; C2 verified if `C2=met`;
neither score changes — calibration 5 and depth 5 held. No score delta is claimed by
the lane. Boundaries held: detection and report only; host tracefs read is read-only
(`evidence/host-tracefs.txt`); no remediation, no host state change.
```

## Out-of-scope items

After-state numbers (landed-tip receipts, C1/C2 verdicts, capability admission) are
not knowable at w1 draft time; `<TIP>` carries that. The staged r42 entry itself and
the SOURCES/SKILL/corpus content are L1 integration surface, not this seat's.

## Artifact paths (Report: trailer — relative to /home/vgpnk/Projects/shokunin/mori-shokunin)

Report: .ufo/waves/round-47/w1/ScribeScorecardLog.md
