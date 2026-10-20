# Round 15 — ScribeReportContract (report-only)

Seat: `ScribeReportContract` (role `scribe`, axes `coverage`, milestone "retain validated positives without fabricated totals"). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Scope: report-only evidence. No production, harness, fixture, or sibling edits. No builds, tests, linters, formatters, or smoke runs. No installations. No commits.

## Behavior

The round-15 claim (C1, coverage, lowest owned axis 6 vs operability 7) is: preserve critical OOM and user signal alarms from individually valid current-boot structured records, even when an adjacent malformed, nonmatching, or foreign-boot record invalidates the aggregate class. Raw aggregate and split counts stay unavailable when invalid.

This report does not verify behavior. It records what the wave's files and the lane's current production bytes say, as of this check.

Observed current production behavior (`tools/mori-census.sh`, 3842 lines), which is the gap C1 targets:

- Each journal class is graded by one all-or-nothing jq filter. `JOURNAL_JQ_MSGID` (line 974), `JOURNAL_JQ_SIGKILL` (line 975), `JOURNAL_JQ_SIGSEGV` (line 976), and the unit-record filter (line 1019) all begin with `if all(.[]; ...)`. One record that fails the `_BOOT_ID`/`MESSAGE_ID` predicate sends the whole class to the invalid branch.
- The invalid branch (line 1037) returns `record-invalid`, `boot-mismatch`, or `multi-boot`. Those tokens make the class `unavailable:<reason>`. The per-record positive evidence that C1 needs is not currently retained when the aggregate is invalid.
- The OOM alarm emits exactly one `OOM_KILL_JOURNAL crit` line (line 1331). The user `KILL_SIGNAL_JOURNAL` warn is keyed on `user:unit_sigkill_record` (line 1340).
- Census selftest cases for the journal path (lines 3224–3254) cover foreign boot, multi-boot, and invalid anchor as whole-class `unavailable`. A grep for mixed or valid-plus-invalid journal fixtures found none.

Corroborating history: the round-13 outside spot-check (`corpus/lessons/round-13-verifier-spotcheck.md`, lines 84–89 and 132) rejected the round-13 closure as harmed. The OOM alarm and the fleet/non-fleet unit distinction were lost in the cutover. Routed item 1 (line 132) requires the OOM warning and DRIFT behavior to return through structured metadata with committed positive and negative evidence.

## Gates

No lane gate was run; per instruction, none was run here.

Gate-relevant facts observed from files:

- `spec.json` context: C1 is sourced to reopened S014, S015, S037, and S038. L1 holds the planner. Other debt is unclaimed conformance.
- `spec.json` items: 64 seats. Role counts: executor 24, scout 8, reviewer 8, critic 8, connector 6, scribe 6, sentinel 2, revenger 2. The `ScribeReportContract` prompt is the seat's full assignment (read in full from `spec.json`).
- Required positive-evidence tokens (from the spec, not yet in production): `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`. Counting rule: object records with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID`. Unit result must be exactly `oom-kill` or `signal`. Process must be exactly `killed` with scalar status `9`.
- Fixture pack schema (from the spec): JSON list of `{id, user, system, want_oom, want_signal, invalid_class}`, boot id `11111111111111111111111111111111`, and the four fixed MESSAGE_IDs. Packs go under `.ufo/waves/round-15/fixtures/*.json`.

## HEAD sequencing

Measured at this check, with git read-only:

- Local branch `master`, HEAD `0fa5e0d`. Upstream `origin/master` is also `0fa5e0d`. Ahead 0, behind 0. Pushed HEAD equals local HEAD.
- Last twelve commits, newest first: `0fa5e0d` protocol-shokunin round-14 verifier spot-check; `52512ae` round-14 red-green repair evidence; `5601d12` round-14 tripwire formatting; `8d22d18` round-14 restore structured OOM alarms and subject-unit triage; `a5cc313` round-14 pin rejected cutover; `dbe8500` round-13 verifier spot-check; `2e57647` round-13 frontier evidence; `c13df48` round-13 expectations; `80bd58a` round-13 parser; `18d7d55` round-13 structured journal scopes; `6531ac6` protocol-shokunin remote documentation; `bf7cdc4` round-12 verifier spot-check.
- Round 15 has no commit yet. The only uncommitted change is the untracked directory `.ufo/waves/round-15/` (`git status --short` printed `?? .ufo/waves/round-15/`). No tracked file changed.

Sequencing implication: round-15 work starts from pushed HEAD `0fa5e0d`. The round-14 commit `8d22d18` is the one whose subject says it restored structured OOM alarms; the census header (line 16–18) describes that restoration as aggregate-gated. C1 changes grading from aggregate-gated to per-record-validated, so its commit must sit after `8d22d18` in the lane history. Whether `0fa5e0d` was itself a round-14 admission is not established by these files.

## Planner mapping

- `spec.json` context states: "L1 holds planner." No planner member is assigned to a scribe or executor seat. The planner is held at L1, not by this seat.
- The nearest connector seat in `assignments.json` is `ConnectPlannerWalk` (`MoriR15.ConnectPlannerWalk`, line 34). Its output is not present in the wave directory at this check.
- Seat-to-id mapping: `assignments.json` maps all 64 seat names to `MoriR15.<Seat>` ids. `build/swarm-registry.json` has 64 members with the same names. `spec.json` has 64 items with the same names. Checked by set comparison: no seat is missing from any of the three lists, and `spec.json` has no duplicate names.
- The registry lists every member with `axes: ["coverage"]` and the round-15 milestone. The spec's `axes` is `["coverage"]` only, so the spec and registry agree.

## Touched surfaces

Current state of surfaces named by the round-15 assignments, as observed at this check:

- `tools/mori-census.sh`: not changed by this seat. Still the r14 production file (3842 lines). No `positive_*` token exists under `tools/`. A lane-root search for the four tokens matched only wave metadata (`dispatch.json`, `spec.json`, `task-response.json`), not production code.
- `tools/mori-round15-regressions.py`: not present (glob returned no match). The HarnessBuild seat owns it.
- `.ufo/waves/round-15/fixtures/`: not present (glob returned "Path not found"). No fixture pack has landed.
- `corpus/SOURCES.md`: pre-wave source census at revision `0fa5e0d6` is recorded in `sources-before.json`. Command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`, exit 0. Informational W04 duplicate-url notes for S035 and S037 across scopes. Lane root `ok`.
- `.ufo/waves/round-15/`: untracked directory. Contains `spec.json`, `dispatch.json`, `task-response.json`, `assignments.json`, `host-safety-amendment.txt`, `sources-before.json`, and `build/swarm-registry.json`.

This seat wrote only `.ufo/waves/round-15/build/ScribeReportContract.md`.

## Out-of-scope items

Not claimed by this seat or by C1:

- Completeness of any journal count. Positive evidence means "at least one individually valid record," not a total.
- Authenticated `MESSAGE_ID` or `_BOOT_ID` (client-supplied; `trust=client-supplied` in the census output).
- Unique victim, unique kill count, or fleet-cause attribution. The systemd catalog describes unit notices, not a unique-victim counter (round-13 lesson, lines 107–111).
- Repair of arbitrary malformed JSON.
- Restoring raw MESSAGE parsing.
- Other conformance debt (`JOURNAL_CLASSES_UNMEASURED`, `other_signals`, cgroup counters, etc.). Named in the spec as "unclaimed conformance."
- Installations, host upgrades, and service restarts. No host action was taken by this seat.

## Findings

1. C1 is not yet implemented in production. The `positive_*` tokens are absent from `tools/`. The current aggregate gate (`if all(.[]; ...)`, lines 974–976 and 1019) still discards individually valid OOM and signal records when one adjacent record is invalid.
2. The round-13 closure's harm finding (corpus lesson lines 84–89, 132) is the source for C1's OOM and user-signal scope. C1 must restore those alarms; it must not restore MESSAGE parsing.
3. The wave's artifact set is partial at this check: `fixtures/` absent, harness absent, no executor reports or planner output. Those are unresolved facts for the main agent to check at integration, not defects found here.
4. The host-safety amendment (`host-safety-amendment.txt`) supersedes earlier installation permission: pacman installs only after `pacman -Sp --print-format '%n %v'` shows every package is uninstalled; never `-Sy`/`-Syu`/`-U`/`-R`; record installations. This seat installed nothing; the only pacman call was `pacman -Q pacman` (read-only). No install is pending.
5. Counts, grounded in file data: 64 seats in all three lists (assignments, registry, spec); 0 duplicates; 3842 census lines; 12 commits listed above; 1 untracked wave directory; 0 tracked modifications; 0 `positive_*` tokens in `tools/`; 0 fixture packs.

Unresolved facts, named honestly:

- Whether the executor seats have produced any production edit or fixture. Not visible in the wave directory at this check.
- The contents of `task-response.json` beyond the seat's own pending entry. Not reconciled here.
- Whether `ConnectPlannerWalk` produced its output. Not visible.
- Whether `0fa5e0d` was a round-14 admission. Not established by these files.

6. Routed from AttackProvenance (`.ufo/waves/round-15/build/AttackProvenance.md`), addressed to the ProvenanceCapture and HarnessBuild owners; this seat takes no action on them. Points: CE1 a dirty-file porcelain line does not change with content, so `moving:false` is false provenance and `harness.sha256` must be hashed at load and end, not emit time; CE2 the `MORI_EVIDENCE_REVISION` pin makes the HEAD comparison vacuous, so use the real `rev-parse HEAD`; CE3 excluding by output prefix can swallow fixtures or the frozen dir; CE4 `dirty` is always true when output is in-repo, so add `dirty_outside_output`; CE6 r15 must hash the importlib-loaded r14 module bytes and the fixture pack bytes as read. Unverified here: whether those owners adopt them.

## Artifact paths

- Report (this file): `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/build/ScribeReportContract.md`
- Inputs read: `.ufo/waves/round-15/spec.json`, `dispatch.json`, `task-response.json`, `assignments.json`, `host-safety-amendment.txt`, `sources-before.json`, `build/swarm-registry.json`; `tools/mori-census.sh`; `corpus/lessons/round-13-verifier-spotcheck.md`.

## Installations and tool changes

None. No `pacman -S`, `uv tool install`, or other install or update was run by this seat. The only package query was `pacman -Q pacman`, which is read-only.
