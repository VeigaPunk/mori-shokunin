# mori round 47 — frozen contract (L1 MoriR47, attempt 1)

Entering lane tip: `2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (round 46; non-author closure
`corpus/lessons/round-46-verifier-spotcheck.md`). This file, both counters and the controls
under `controls/` are committed in one freeze commit before any wave seat runs. A predicate,
counter, floor or kill rule changed after any seat has scored is not the claim's rule.

Active scores entering (SCORECARD.md Axes table): coverage 6, operability 7, depth 5,
freshness 5, calibration 5, adjacency 6. Lowest non-retired axes: depth, freshness,
calibration (tied at 5). Both claims work a lowest axis; no stagnation waiver is used.

Frozen instrument bytes (sha256):

- `tools/mori-pin-check.py` — `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`
- `.ufo/waves/round-47/count-c2.py` — `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e`

If the working-tree bytes ever differ, the claim is measured with `git show <freeze>:<path>`.

## C1 — calibration: SKILL.md registry self-test pins reproduce from committed bytes

Surface: `SKILL.md` gate-registry tables (the lane's self-assessment of its own instruments).
Routed by the round-46 closure (defect 1: replace `count-repins.py`, which was row-wide
substring matching) and mined from `considerthese/2026-10-25.md` suggestion 1 ("Add a registry
pin check … compare the pinned sha256 and selftest tally against … a real `--selftest` run.
Then list any mismatch by line number").

**P-C1.** At revision R, `python3 tools/mori-pin-check.py --rev R --min-tally-pins 26
--baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` prints `PIN_CHECK=met` and exits 0:
every tally pin and full-sha256 digest pin in the self-test cell of every SKILL.md gate table
reproduces from the committed bytes of R (mismatches=0, unparsed=0, no_command=0), no pin key
present at the entering revision is dropped (dropped=0), and at least 26 tally pins are found.

- Before (entering `2d85e33`): `PIN_CHECK=unmet tally_pins=26 digest_pins=5 mismatches=1` —
  `SKILL.md:912` pins `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`, the committed tool
  prints `pass=22 fail=0` (receipt `evidence/control-c1-donothing.txt`).
- Target after: `PIN_CHECK=met` at the landed tip, same command.
- Controls (each scored with the frozen counter before data; each must stay unmet):
  do-nothing (entering revision); `controls/control-c1-deleted.md` (the stale row deleted —
  `dropped`); `controls/control-c1-moved.md` (round-46 false-green class: the true tally placed
  in another cell, stale tally kept in the self-test cell — `mismatch`);
  `controls/control-c1-truncated.md` (pin weakened to `pass=2` — token-boundary `mismatch`).
- Kill rule: if the landed tip prints `PIN_CHECK=unmet`, C1 is not verified; no re-scoring
  under a changed counter.
- Named limits: line-count pins (`743 lines`) and truncated digests (`37fd7c24ff52…`) are not
  checked; a digest pin matches if it equals the sha256 of any file path named in its row; the
  check runs each command once and does not prove a selftest is deterministic.

## C2 — depth: the OOM tracepoint catalogue, field by field, from the kernel's own header

Surface: `corpus/knowledge/` FR13 (eBPF kill/OOM tracing). Assimilation theme from
`/home/vgpnk/Projects/shokuknow/merge/mori/` — staged entry
`knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` claims "exactly three named
tracepoints"; the committed Linux v7.2 `include/trace/events/oom.h` copy defines eight
`TRACE_EVENT`s. Sourced claim: new row S475 (opened this round).

**P-C2.** At revision R, corpus/knowledge/oom-tracepoints-r47.md opens with source: (citing
S475), verified-at: and recheck:, and carries a table whose header's first cell is
`tracepoint` with one row per TRACE_EVENT in the committed copy of Linux v7.2
include/trace/events/oom.h — the row's backticked tracepoint name set equals the header's
event set, each row's backticked field set equals that event's TP_STRUCT__entry field set,
and each row's `emitted in` path is a committed v7.2 copy containing `trace_<name>(` — every
committed copy matching its frozen sha256; and corpus/SOURCES.md at R carries S475 as a mined
tier-A code row naming v7.2 and include/trace/events/oom.h whose used-by names the entry.

Counting command: `python3 .ufo/waves/round-47/count-c2.py R` → `C2=met|unmet …`.

- Before (entering `2d85e33`): `C2=unmet … failed=entry_absent,pins,source_row`.
- Target after: `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0
  pin_mismatch=0 source_row=ok provenance=ok` at the landed tip.
- Controls (unmet with the frozen counter): do-nothing (entering revision);
  `controls/control-c2-staged.md` (the staged entry byte-exact — no catalogue table);
  `controls/control-c2-three.md` (the staged "three tracepoints" claim as a table —
  `name_mismatch`). Re-scored at the freeze commit, where the source copies are committed, so
  the failure isolates to the entry.
- Kill rule: `C2=unmet` at the landed tip → C2 not verified.
- Named limits: the counter checks names, field sets and the presence of one emitting call per
  event in the committed v7.2 copies; it does not check prose, lifecycle ordering claims, or the
  host's running kernel (a host tracefs reading is separate own-work evidence).

## Separability

C1 touches only SKILL.md registry cells and `tools/mori-pin-check.py`; C2 touches only the
FR13 knowledge entry, its SOURCES rows and `corpus/evidence/sources-r47/`. Either counter can
be run with the other claim's changes reverted.

## Round shape

Two v1 waves (policy `scripts/hyaku/ufo-wave-policy.json`, band 32–64): w1 build + first
falsifiers, w2 falsify after landing. Total within 64–100.
