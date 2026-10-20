# MoriR14.KnowledgeRepair — journal alarm and subject routing

Seat: `MoriR14.KnowledgeRepair` (executor, leaf). Milestone: restore OOM alarm and structured
fleet routing. Axis: coverage.
Scope: one new knowledge file plus this report. No production, SOURCES, LOG, lesson, README,
score or verifier edit by this seat. No build, test, lint, formatter, census, fixture or live
journal query ran here; L1 owns measurement.

## Files changed

- `corpus/knowledge/journal-alarm-routing-r14.md` — new knowledge note: structured OOM alarm
  frame, subject-unit fleet routing, cgroup non-substitution, three-way signal/GPF limits,
  unavailable semantics and the r14 target contract.
- `.ufo/waves/round-14/build/KnowledgeRepair.md` — this report.

## Sources opened this round (2026-10-20)

Source trio first: pinned catalog (S013/S035), current journal-fields page (S015), pinned
emitter (S036). Then the L1-registered subject/result rows (S037/S038) and the already-mined
S002. All source content was read as data.

| row | authority | access | located quote (≤25 words) | location |
|---|---|---|---|---|
| S013 | systemd catalog, pinned `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` | 2026-10-20 | “A process of @UNIT@ unit has been killed by the OOM killer.” | catalog :604–605, entry :604–616 |
| S013 | same | 2026-10-20 | “Note that the memory pressure might or might not have been caused by @UNIT@.” | catalog :615–616 |
| S013 | same | 2026-10-20 | “Kernel messages have been lost as the journal system has been unable to process them quickly enough.” | catalog :63–64, loss entry :58–64 |
| S015 | `systemd.journal-fields(7)`, systemd 262, Last-Modified 2026-09-22 | 2026-10-20 | “not supposed to be parsed for metadata.” | User Journal Fields → `MESSAGE=` |
| S015 | same | 2026-10-20 | “Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code.” | Trusted Journal Fields |
| S035 | same pinned catalog | 2026-10-20 | “The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'.” | catalog :561–566 |
| S035 | same pinned catalog | 2026-10-20 | “The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@.” | catalog :568–575 |
| S036 | `src/core/unit.c`, pinned | 2026-10-20 | `LOG_ITEM("UNIT_RESULT=%s", result));` | `unit_log_failure` :6333–6342 |
| S036 | same | 2026-10-20 | `LOG_ITEM("EXIT_STATUS=%i", status),` | `unit_log_process_exit` :6379–6391 |
| S037 | `systemd.journal-fields(7)`, registered row | 2026-10-20 | “Used by the system and user managers when logging about specific units.” | User Journal Fields → `UNIT=`, `USER_UNIT=` (added v251) |
| S038 | `src/core/service.c`, pinned, registered row | 2026-10-20 | `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` | `service_result_table` :6598 |
| S002 | cgroup-v2 docs | 2026-10-20 (first opened 2026-10-19) | “Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical.” | `memory.events.local` |
| S002 | same | 2026-10-20 | “The number of processes belonging to this cgroup killed by any kind of OOM killer.” | `memory.events` → `oom_kill` |

Observed fetch facts: catalog 1054 lines, SHA-256
`e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592`; pinned `src/core/unit.c`
SHA-256 `4833056a6313b250ad6b53de3121a51e8dee602733e1aedf4a7d3d2687d547ed`; docs footer
`systemd 262`, `Last-Modified: Tue, 22 Sep 2026 13:31:36 GMT`. `src/core/service.c:6598` was
located by grep; `[SERVICE_FAILURE_SIGNAL] = "signal",` is at `:6593` in the same table.
`corpus/SOURCES.md` now carries S037 (line 43) and S038 (line 44), both mined and used-by
`corpus/knowledge/journal-alarm-routing-r14.md`.

## What the note establishes

1. **Structured OOM alarm ≠ unique victim.** `fe6faa94…` is a unit-scoped manager notice. The
   pinned emitter turns a cgroup-counter increase into one NOTICE; its message says “some
   processes”, carries no victim identity or count, can under-count a jump of kills, and can
   fan out across ancestor units. The r12 5-victim-line vs 7+9-notice measurement is cited, not
   re-measured. Alarm labels must be `unit=notice`, `count=<records>`, `attribution=none`.
2. **Two independent OOM arms, one alarm.** `d9b373ed…` with `UNIT_RESULT=oom-kill` (S035, S038)
   must alarm even with missing subject metadata. The r14 ruling is one global
   `OOM_KILL_JOURNAL` `crit` per census with separate `user_notice`, `system_notice`,
   `user_unit_oom`, `system_unit_oom` counters, never summed; a known positive arm still alarms
   when another arm is unavailable.
3. **Signal restoration is two structured arms.** `KILL_SIGNAL_JOURNAL` user-scope WARN fires on
   user process `98e32220…` SIGKILL 9 or user `UNIT_RESULT=signal`; counters are separate and
   never summed. `UNIT_RESULT=signal` establishes neither signal 9, the signal number, nor the
   sender; system-scope result signal adds no warning.
4. **Fleet/non-fleet by subject metadata only.** `UNIT=`/`USER_UNIT=` (S037) are non-underscore,
   client-supplied subject-unit fields; trusted `_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT` describe the
   emitter. Selection is by field presence, independent of journal scope; dual presence or
   missing/malformed metadata is unknown. Fleet/non-fleet uses the historical case-insensitive
   `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` predicate over the subject, labelled
   `classification_rule=unit-name-token`; it is a heuristic, not fleet-membership proof, and
   arc2/run units can be false negatives. Unknown subject routes to
   `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` INFO, `owner=unresolved`,
   `reason=subject-metadata-unknown`; fleet and non-fleet stay INFO (tsukuroi owner for non-fleet);
   the valid raw failure-record total is preserved.
5. **Cgroup-local coverage is not a substitution.** S002 defines `memory.events.local` as
   non-hierarchical. The lane reads one selected cgroup's local `oom_kill`
   (`tools/mori-census.sh:1152–1164` at base `dbe8500`); it cannot see other cgroups,
   descendants, or other units, and it is cumulative. The journal notice class is boot-scoped,
   unit-scoped and scope-wide. Userspace oomd kills do not increment kernel counters. Neither
   plane implies the other; neither replaces the other when unavailable.
6. **Signal/GPF limits are three statements.** Implementable-but-unimplemented (non-9 signals via
   `EXIT_STATUS=<signal>`, result-value partitions); no structured anchor (GPF-specific identity,
   kernel victim PID/UID/`task_memcg`, sender/cause); no retained record (rate-limit/loss,
   outside manager observation, inaccessible/vacuumed journal). The r13 categorical
   `no-anchored-structured-field` wording must not cover the first class. No live GPF regression
   is claimed.
7. **Unavailable is not an alarm and not zero.** Malformed field/JSON/query error, stderr, wrong
   boot or timeout makes that scoped class unavailable; no positive alarm is inferred and
   unavailability does not by itself force DRIFT. The note claims no comprehensive or
   unspoofable alarm; all selection fields are client-supplied.
8. **OOM provenance is restoration plus extension.** The retired text class selected user
   journal MESSAGE text. The structured alarm adds system-scope notices and unit-result OOM
   records as an explicit operator-required extension; the note does not claim old-text parity.
9. **Candidate only.** The note states required behaviors, not delivered schema. At base
   `dbe8500`, `tools/mori-census.sh:1085–1106` still assigns INFO to every journal class except
   `user:unit_sigkill_record`, and no `UNIT_FAILURE_OUT_OF_SCOPE`/unattributed emission exists.
   L1 measurement remains the gate.

## Counter-evidence received and applied

`MoriR14.ScopedFixtures` reported that the initial note's “slice units emit nothing” claim was
wrong. Verified in the pinned source: `unit_watch_cgroup_memory` skips slices at
`src/core/cgroup.c:2077-2078`, but `on_cgroup_empty_event` (`:2936-2961`) calls
`unit_check_oom(u)` at `:2959` without a slice exclusion. The current note has no blanket slice
exclusion: it says slices are not inotify-watched but can emit via the cgroup-empty check, the
inotify watch (not the notice class) excludes slices, and delivery paths say slice notices are
included but name only a slice. It records the cumulative-counter timing inference and qualifies
the control flow at pinned main `cf8ebfc6`, with host systemd 261 equivalence not established.
ScopedFixtures' count-only host grouping (user 7 = slice 3/service 2/scope 2; system 9 = slice
4/service 5) is cited as their seat read-only observation, not universal behavior and not re-run
here. This does not weaken the cgroup non-substitution claim: a slice notice adds only a
slice-level subject and still identifies no descendant unit, process or victim.

## L1 rulings incorporated

The note reflects, verbatim in substance: one global `OOM_KILL_JOURNAL` crit with four separate
no-sum counters; generic fleet/non-fleet INFO; `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` INFO with
`owner=unresolved` and `reason=subject-metadata-unknown`; subject selection by exactly one valid
`UNIT`/`USER_UNIT`, dual presence unknown, no emitter fallback; `classification_rule=unit-name-token`
and no exhaustive-membership claim; user process9 OR user result-signal WARN, separate counts, no
signal-9/sender inference from result signal; system result signal no new warning; unavailable
classes neither alarm nor DRIFT; OOM alarm marked restoration-plus-extension rather than old-notice
parity.

## Retained evidence and limits

- Quotes and access dates are in the table above; the note's `source:` line carries URLs, anchors
  and the 2026-10-20 access date, and its `recheck:` line is copy-pastable.
- Supplementary pinned code beyond registered rows: `src/core/cgroup.c:3055-3105` (notice
  cardinality), `:2077-2078` (slice inotify skip), `:2936-2961` (cgroup-empty `unit_check_oom`
  call), `src/core/service.c:4704-4752` (OOMPolicy path), `src/core/unit.h:1133,1177`
  (`log_unit_struct` macro). They are flagged in the note as unregistered supporting anchors; no
  S ids are invented for them. `unit_log_field` (`src/core/unit.c:6995-6997`) is in S036's file
  but outside S036's registered anchor range.
- Host version caveat: anchors are systemd main `cf8ebfc6`; host runs systemd 261. No
  version-equivalence claim. No journal query, fixture or census was run by this seat.

## Residual actions owned by L1 (not applied here)

- **S002 used-by gap:** line 8 still lists only the two r12 notes. Append
  `corpus/knowledge/journal-alarm-routing-r14.md`. S013/S015/S035/S036/S037/S038 already list the
  note.
- LOG.md round-14 entry for the new knowledge note per lane AGENTS.md.
- INDEX row 39 (IndexCorrection) now carries these holds: one global OOM alarm with four no-sum
  counters; two-arm KILL_SIGNAL WARN; `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`; name-token heuristic;
  S037/S038 added to sources (IndexCorrection confirmed the row matches).
- If L1 wants every supplementary code anchor registered, file rows for `cgroup.c`/`service.c`
  policy path/`unit.h`; otherwise accept them as flagged support.

## Tooling

None installed or updated by this seat. Reads used `read`, `grep`, `curl`, `python3` text
extraction and `sha256sum`; no package manager action.
