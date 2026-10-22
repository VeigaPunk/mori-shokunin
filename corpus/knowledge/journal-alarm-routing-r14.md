source: S013 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in — pinned commit cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af; `fe6faa94…` :604-616, `d989611b…` :884-894, coredump :66-75, loss :58-64; S015 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — systemd 262 page, Last-Modified 2026-09-22; User Journal Fields `MESSAGE=`/`MESSAGE_ID=`, Trusted Journal Fields; S035 — same pinned catalog, unit-result :561-566 and process-exit :568-575; S036 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c — `unit_log_failure` :6333-6342, `unit_log_process_exit` :6355-6392, `unit_log_field` :6995-6997; S037 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — subject-unit `UNIT=`/`USER_UNIT=` and emitter `_SYSTEMD_*` fields (L1-registered this round); S038 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c — `service_result_table:6598` `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` (L1-registered this round); S002 — https://docs.kernel.org/admin-guide/cgroup-v2.html — `memory.events.local` and `memory.events` `oom_kill` (opened 2026-10-20).
verified-at: 2026-10-20 — all source pages and pinned code re-opened 2026-10-20; lane base `dbe8500`; no census, journal query, fixture or gate run by this seat.
recheck: `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | grep -nE '^-- (fe6faa94|d9b373ed|98e32220)'`; `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c | grep -nE 'UNIT_RESULT=%s|EXIT_STATUS=%i|unit_log_field'`; `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c | grep -nF '[SERVICE_FAILURE_OOM_KILL]'`; `curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | grep -o 'Used by the system and user managers when logging about specific units.'`; `curl -fsSL https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | grep -o 'not supposed to be parsed for metadata.'`; `curl -fsSL https://docs.kernel.org/admin-guide/cgroup-v2.html | grep -o 'Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical.'`

# Journal alarm and subject routing — round 14

## Claim

A structured OOM *alarm* and a *victim count* are different claims. The `fe6faa94…` catalog
record is a unit-scoped service-manager notice that something in a unit was killed by the kernel
OOM killer; it carries neither victim identity nor a per-victim count. Mori must still alarm on
it. Round 14's ruling is one global `OOM_KILL_JOURNAL` critical finding per census, with separate
`user_notice`, `system_notice`, `user_unit_oom` and `system_unit_oom` counters that are never
summed into a record total. The `d9b373ed…` unit-failure record with `UNIT_RESULT=oom-kill` is a
second, independent OOM alarm path; it must alarm even when subject metadata is missing.

The r14 target restores the historical `KILL_SIGNAL_JOURNAL` warning from two structured arms:
user-scope `98e32220…` process SIGKILL 9, and user-scope `d9b373ed…` with
`UNIT_RESULT=signal`. The two
counts are separate and never summed; the result-signal arm establishes neither signal 9 nor a
sender. The structured OOM alarm is a sourced replacement *plus* an explicit operator-required
extension (system-scope notices and unit-result OOM records); it is not claimed to be
byte-equivalent to the retired user-journal text class.

Fleet/non-fleet ownership is read from the record's *subject* unit in `UNIT=`/`USER_UNIT=`. Those
are non-underscore, client-supplied fields; no authentication is claimed. The trusted
`_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT` fields describe the process the entry originates from — the
emitter — not the failed subject. A record whose subject metadata is missing, malformed,
unreadable, or ambiguous (either absent or dual presence of both fields) is an explicit
unattributed unknown, not fleet and not non-fleet. Journal scope is a query boundary, never a
field selector. The fleet split is an explicit unit-name-token heuristic
(`classification_rule=unit-name-token`): it improves subject selection but does not prove fleet
membership or causation.

A cgroup-local `memory.events.local` counter covers only the selected cgroup and cannot substitute
for the journal alarm; the notice class is not a cgroup counter either. Signal and GPF coverage
must distinguish three different limits: structured-but-unimplemented classes, classes with no
structured anchor, and delivery paths with no retained record at all.

Adjacent: `structured-journal-scopes-r13.md` owns the delivered six-class per-scope counter
schema; `kill-classes-by-message-id-r12.md` owns the notice-versus-victim unit boundary and the
historical 5/7/9 sample; `userspace-oom-killers-r12.md` owns oomd/earlyoom event planes;
`oom-kill-counter-kernel-only-r12.md` owns the kernel counter-only update path. This note adds the
round-14 alarm/routing frame and its limits; it does not modify implemented schema or re-measure.

## Evidence

### 1. The OOM notice is a unit notice, not a victim record

- S013 `fe6faa94e7774663a0da52717891d8ef` `:604-605`: “A process of @UNIT@ unit has been killed
  by the OOM killer.” The body adds “Note that the memory pressure might or might not have been
  caused by @UNIT@.” (`:615-616`). The record is unit-scoped and the catalog does not define a
  victim field.
- The pinned emitter `src/core/cgroup.c:3055-3105` (same commit, supplementary unregistered
  anchor) reads the unit's cgroup `memory.events` `oom_kill`, or `memory.events.local`
  `oom_group_kill` when `memory.oom.group=1`, converts a counter increase into a boolean, and logs
  once at `LOG_NOTICE` with `fe6faa94…`. Its message is “The kernel OOM killer killed some
  processes in this unit.” (11 words). Consequences: a jump of several kills between checks yields
  one notice (under-count); multiple ancestor units can each observe the same kill (fan-out);
  units without a cgroup runtime, or where the memory controller and its `memory.events` file are
  unavailable, emit nothing from this path; the inotify watch additionally requires memory
  accounting. Slice units are not inotify-watched (`src/core/cgroup.c:2077-2078`), but
  `on_cgroup_empty_event` (`:2936-2961`) calls `unit_check_oom(u)` at `:2959` without a slice
  exclusion, so a slice can still emit a notice when its cgroup empties. Because the slice
  counter is cumulative and the runtime's last-seen value starts at zero, a slice notice can
  reflect an earlier counter increase rather than a kill at that moment [INFERENCE]. Version
  scope: this control flow is read at pinned main `cf8ebfc6`; equivalence with the host systemd (261 when read in round 14; 262 on 2026-10-22) is not
  established. The host count-only observation in Observed is a read-only count consistent with
  this path, not a universal statement about every host or every notice.
- The r12 measurement already separated the units: five kernel victim lines versus seven
  user-journal and nine system-journal `fe6faa94…` notices in one boot. The quantities are not
  additive and do not establish a one-to-one mapping.
- Therefore the alarm label must be `unit=notice`, `count=<records>` (when a count is shown) and
  `attribution=none`; it must not read `count=kills`, `unit=victim`, or a unique victim. The alarm
  may be raised from a notice without identifying any victim.

### 2. `UNIT_RESULT=oom-kill` is an independent structured OOM path

- S035 `d9b373ed55a64feb8242e02dbe79a49c` `:561-566`: “The unit @UNIT@ has entered the 'failed'
  state with result '@UNIT_RESULT@'.” S036 `unit_log_failure` `:6333-6342` emits that catalog ID
  with `LOG_ITEM("UNIT_RESULT=%s", result)`.
- S038 `src/core/service.c:6598`: `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` fixes the vocabulary
  that can appear in `UNIT_RESULT`. The same pinned file's `service_notify_cgroup_oom_event`
  (`:4704-4752`, supplementary unregistered anchor) shows the result is policy-mediated: under
  `OOM_CONTINUE` the service is not failed, so no unit-failure record follows.
- A validated unit-failure record whose `UNIT_RESULT` is exactly `oom-kill` must raise the OOM
  alarm even when `UNIT=`/`USER_UNIT=` is missing or unusable: the result field is sufficient
  for the alarm, though not for victim identity or ownership. It is a consequence record, not a
  victim count, and its absence does not prove no OOM occurred.

### 3. Subject metadata versus emitter metadata

- S037/S015, User Journal Fields → `UNIT=`, `USER_UNIT=` (added v251): “Used by the system and
  user managers when logging about specific units.” The same section places them among fields
  “directly passed from clients and stored in the journal”; S015 also says `MESSAGE` is “not
  supposed to be parsed for metadata.” They are therefore subject metadata supplied by the
  manager, not authenticated identity.
- S036 `unit_log_field` `:6995-6997` (same pinned file, outside S036's registered anchor range)
  returns `UNIT=` for a system manager and `USER_UNIT=` for a user manager. In
  `unit_log_failure` `:6337` and `unit_log_process_exit` `:6379` the value is the record's
  subject unit. The field *name* therefore encodes the manager kind; it does not encode the
  journal scope, and both scopes can carry `USER_UNIT`.
- S015 Trusted Journal Fields: “Fields prefixed with an underscore are trusted fields, i.e.
  fields that are implicitly added by the journal and cannot be altered by client code.”
  `_SYSTEMD_UNIT=`/`_SYSTEMD_USER_UNIT=` describe “the process the journal entry originates
  from”: the emitter, which need not be the failed subject. Q30 forbids classifying the subject
  from those fields.
- Round-14 routing ruling, applied to validated unit-failure records:
  * Raw total first: every record with `d9b373ed…` and a validated boot counts in the valid
    failure-record total, including records whose subject or result metadata is unusable.
    Metadata defects move a record between classification buckets; they never erase it from the
    raw total.
  * Fleet: exactly one of `UNIT=`/`USER_UNIT=` present and readable, and its value matching the
    historical case-insensitive predicate `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` →
    `UNIT_FAILURE_JOURNAL`, INFO (the historical fleet severity, not WARN), labelled
    `classification_rule=unit-name-token`. This is a lane ownership heuristic, not proof of fleet
    membership or causation: fleet-related units that lack a token (current arc2/run units are
    named by RoutingAttack as a live example) can land in the non-fleet bucket. The bucket means
    “name-token non-match”, not “proven non-fleet”.
  * Non-fleet: exactly one subject field present and readable with no predicate match →
    `UNIT_FAILURE_OUT_OF_SCOPE`, INFO, naming tsukuroi as owner, same
    `classification_rule=unit-name-token` label.
  * Unattributed: both fields absent, malformed, unreadable, or both present (dual presence is
    ambiguous even if the values agree) → `UNIT_FAILURE_UNATTRIBUTED_JOURNAL`, INFO,
    `owner=unresolved`, `reason=subject-metadata-unknown`, with scope and count. It is never
    counted as fleet or non-fleet and is never treated as zero. Subject fields are selected by
    presence, not by the query scope; no arbitrary subject payload is echoed.
  * Result axis: valid `oom-kill` → the global OOM alarm; another valid `UNIT_RESULT` → a
    non-OOM failure result; missing/malformed `UNIT_RESULT` → unknown result aggregate. The raw
    failure total is preserved in every case.
  * Scope is a query boundary, not a selector: `--user`/`--system` neither implies nor selects
    `USER_UNIT=`/`UNIT=`.

### 4. Cgroup-local coverage is not a substitute

- S002, `memory.events.local`: “Similar to memory.events but the fields in the file are local to
  the cgroup i.e. not hierarchical.” The `memory.events` `oom_kill` field is “The number of
  processes belonging to this cgroup killed by any kind of OOM killer.”
- The lane cgroup surface reads `memory.events.local` of the selected cgroup
  (`tools/mori-census.sh:1152-1164` at base `dbe8500`), with a user-session-service fallback. It
  cannot see kills of other cgroups, descendants, or other units, and the counter is cumulative
  across the cgroup's lifetime, so a positive value can predate the current wave.
- The journal notice class is boot-scoped, unit-scoped and manager-emitted for the units the
  manager checks: inotify-watched non-slice units with memory accounting, plus units checked on
  cgroup-empty (including slices), within the queried journal scope. The inotify watch excludes
  slices; the notice class does not. It is not computed from the selected cgroup counter.
  Userspace oomd kills do not increment kernel counters (see `userspace-oom-killers-r12.md`), so
  a zero cgroup `oom_kill` can coexist with userspace OOM kills and with notices for other
  units.
- Consequently: a critical `CGROUP_OOM_KILL` does not make the journal alarm unnecessary; a zero
  local counter cannot suppress `OOM_KILL_JOURNAL`; and neither surface replaces the other when
  one is unavailable.

### 5. Signal and GPF limits: three statements, not one

| class | structured anchor | limit |
|---|---|---|
| Signal 9 on a manager-observed unit process | `98e32220…` + `EXIT_CODE=killed` + `EXIT_STATUS=9` (S035 :575; S036 :6379-6391) | Implemented (r13 `unit_sigkill_record`) |
| Unit failed with result `signal` | `d9b373ed…` `UNIT_RESULT=signal` (S035 :561-566; S038 :6593) | Target user-scope WARN arm; it establishes that a signal ended the unit, not signal 9, the sender, or the cause |
| Other signals on manager-observed unit processes | same `98e32220…` record with `EXIT_STATUS=<signal>`; `unit_log_process_exit` logs WARNING for non-`CLD_EXITED` (S036 :6372-6377) | Implementable, **unimplemented**: the field exists; the filter does not |
| `UNIT_RESULT` values other than a counted bucket | `UNIT_RESULT=%s` (S035/S036) | Implementable, currently unpartitioned |
| GPF-specific identity | none; retired text heuristic matched `segfault\|general protection fault` in `MESSAGE` | **No structured anchor**; only a coredump record with `COREDUMP_SIGNAL=11` or kernel text may survive |
| Kernel OOM victim PID/UID/`task_memcg` | only the kernel `MESSAGE` line (`kernel-oom-line-attribution-r12.md`); the catalog notice has no such field | No structured anchor in the notice path |
| Signal sender/cause | `98e32220…` carries `EXIT_CODE`/`EXIT_STATUS` only; `COMMAND=` is also present but not requested | Unrecorded in this class |
| Rate-limited/lost records | loss notice `e9bf28e6…` (S013 :58-64); rate-limit text (:50-56) | **No retained record** may exist |
| Processes outside manager observation, inaccessible journal, vacuumed files | none | No retained record |

The three limits must stay separate:

1. **Implementable but unimplemented** — a structured field exists and a filter could be added
   (non-9 signals, result-value partitions). Do not describe these as having no structured field.
2. **No structured anchor** — a record or text may exist, but no metadata field identifies the
   class (GPF-specific identity, kernel victim detail). MESSAGE text is not an acceptable
   substitute.
3. **No retained record** — the event was never emitted, was lost, rate-limited, inaccessible, or
   vacuumed. Nothing can be counted, and absence is not evidence of zero events.

No live GPF regression is claimed. A GPF that surfaces only as SIGSEGV coredump is covered, if at
all, by the existing `segfault_signal11` class; a GPF that leaves no coredump/record is
unrecorded.

### 6. Alarm and routing contract (round-14 ruling; awaiting L1 measurement)

These are required behaviors, not a claim that the current HEAD implements them. At base
`dbe8500`, `tools/mori-census.sh:1085-1106` still assigns INFO to every journal class except
`user:unit_sigkill_record`, and no `UNIT_FAILURE_OUT_OF_SCOPE` or unattributed emission exists.

- **One global OOM alarm per census.** A positive validated count from either OOM source
  (`fe6faa94…` notice in user or system scope; `d9b373ed…` with `UNIT_RESULT=oom-kill` in either
  scope) raises one `OOM_KILL_JOURNAL` finding at `crit`, and the census rolls DRIFT once. The
  finding carries separate counters `user_notice`, `system_notice`, `user_unit_oom` and
  `system_unit_oom`. The four counters are evidence fields derived from the raw notice and
  unit-failure class totals; they are never summed into a record total and never presented as
  victims. A second positive source does not create a second alarm. A known
  positive arm still alarms when another arm is unavailable; an unavailable arm never suppresses
  or creates an alarm by itself.
- **Raw totals stay measurable.** The six per-scope class counters remain the raw record totals
  even when failed-subject metadata is missing; fleet/non-fleet/unattributed classification is a
  separate count over those raw totals, not a replacement for them.
- **Finding tally.** The census roll and drift count are counts of warning/critical finding
  lines, not notice records, process counts or killed processes.
- **Signal warn restoration.** Retain `KILL_SIGNAL_JOURNAL` as one user-scope WARN finding when
  either arm is positive: `98e32220…` with `EXIT_CODE=killed`/`EXIT_STATUS=9`, or
  `d9b373ed…` with `UNIT_RESULT=signal`. The process-9 and result-signal counters are reported
  separately and never summed; neither arm is a count of signals or victims.
  `UNIT_RESULT=signal` establishes only that the unit failed with result `signal` (S038 :6593); it
  does not establish signal 9, the signal number, the sender, or the cause. A system-scope
  result-signal record adds no new warning; the existing system-scope severity rules are
  unchanged. The process-9 arm covers only manager-observed unit process exits; the retired text
  pattern could match other status lines, so its coverage is not identical.
- **OOM alarm provenance is restoration plus extension, not old-text parity.** The frozen text
  class selected user-journal MESSAGE text (`Out of memory|oom-kill|oom_reaper|Killed process`).
  The structured alarm selects `fe6faa94…` notices in both scopes and `UNIT_RESULT=oom-kill`
  records in both scopes. The system-scope notice arm and the unit-result OOM arm are an explicit
  operator-required extension, not a byte-equivalent restoration of the old text class; do not
  claim old-notice parity or identical coverage/cardinality. The stable finding id, critical
  severity and DRIFT effect are retained.
- **Unavailable is not an alarm.** A malformed record field, malformed JSON, nonzero journalctl
  exit, stderr bytes, wrong boot, or timeout makes that scoped class unavailable. No positive
  alarm is inferred from an unavailable class, and unavailability does not by itself force DRIFT;
  it is a named unavailable surface. The alarm is fail-loud on positive validated records, not a
  claim to be comprehensive or unspoofable.
- **Fleet routing (name-token heuristic).** Valid fleet-name-token subject records →
  `UNIT_FAILURE_JOURNAL` INFO (`classification_rule=unit-name-token`); valid subjects with no
  token → `UNIT_FAILURE_OUT_OF_SCOPE` INFO with the tsukuroi owner route; unusable, absent or
  dual-presence subject metadata → `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` INFO with
  `owner=unresolved` and `reason=subject-metadata-unknown`. The tokens are a historical lane
  ownership convention, not a fleet-membership or causation guarantee: real fleet-related units
  without a token (arc2/run units are the named live example) can land in the non-fleet bucket.
  The valid raw failure-record total is preserved independently of these buckets.
- **Independence.** The OOM result alarm does not depend on subject metadata; the subject
  partition does not depend on the OOM result. Each axis is reported separately.
- **Trust.** `MESSAGE_ID`, `UNIT=`, `USER_UNIT=`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS` and
  `COREDUMP_SIGNAL` are client-supplied. Any process able to write the journal can forge a
  positive alarm or an ownership label. This is a fail-loud exposure, not authenticity; no
  emitter-authentication claim is made. `_BOOT_ID` is the only trusted scope anchor requested and
  validated.
- **Measurement bar (L1).** Frozen entering bytes must fail the restored positive fixtures; the
  delivered bytes must pass each positive and negative fixture on the revision actually
  delivered; the cgroup finding stays separate; no fixture may sum scopes or treat unavailable as
  zero. Live measurements are L1-owned.

## Observed

- S013/S035 catalog re-opened at the pinned commit: entries at `:58`, `:66`, `:561`, `:568`,
  `:604`, `:870`, `:884`; 1054 lines; SHA-256
  `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592`.
- S015/S037 page re-opened: systemd 262, `Last-Modified: Tue, 22 Sep 2026 13:31:36 GMT`;
  `UNIT=`/`USER_UNIT=` in User Journal Fields, added v251; trusted underscore fields in the
  following section.
- S036 `src/core/unit.c` re-opened: SHA-256
  `4833056a6313b250ad6b53de3121a51e8dee602733e1aedf4a7d3d2687d547ed`; `unit_log_failure`
  `:6333-6342`, `unit_log_process_exit` `:6355-6392`, `unit_log_field` `:6995-6997`.
- S038 `src/core/service.c` grep located `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` at `:6598`.
- S002 `memory.events.local` and `oom_kill` definitions re-opened 2026-10-20.
- Counter-evidence reported by `MoriR14.ScopedFixtures` (2026-10-20; report still pending at this
  write): a count-only host query grouping `fe6faa94…` records by subject suffix found slice
  subjects — user 7 total (slice 3 / service 2 / scope 2) and system 9 total (slice 4 / service
  5). This seat did not rerun that query; the pinned `on_cgroup_empty_event` path above shows how
  a slice can emit.
- No host journal query, census run, fixture run, or live measurement was performed by this seat.
  The historical 5/7/9 sample is cited from r12, not re-measured.

## [INFERENCE]

- A notice can describe a fleet-caused kill, a kill of a fleet unit, or a desktop kill; the record
  cannot distinguish them. A critical OOM alarm therefore does not establish fleet harm, and a
  fleet unit failure does not establish an OOM cause.
- A subject-unit predicate is a lane ownership convention, not authenticated membership. A forged
  `UNIT=` can move a record between the fleet and non-fleet buckets; the raw total and the OOM
  result axis remain. This is consistent with the lane's fail-loud exposure.
- Typed subject metadata improves *which unit the record is about*; it does not close fleet
  correlation. A real fleet-related unit whose name lacks a token is reported as name-token
  non-fleet, and a token-bearing name is not proof of fleet cause. FR1 remains frontier.
- A non-fleet bucket means “unit-name-token non-match”, not “proven non-fleet”: the live arc2/run
  units named by RoutingAttack are the expected false-negative class.
- A slice notice can fire at cgroup-empty from a cumulative counter increase that predates the
  empty event; its journal timestamp is the check time, not necessarily the kill time. A slice
  notice also does not identify the descendant unit or process, so it is weaker than a service
  notice for victim attribution.
- A positive notice count with zero local cgroup kills is consistent (another cgroup, ancestor
  fan-out, cumulative window). A zero notice count with a positive local counter is consistent
  (notice not emitted, unit not watched, journal loss). Neither pattern alone proves a defect.
- The `UNIT_RESULT=oom-kill` path and the notice path can both fire for one event; that is why
  the ruling uses one global alarm with separate counters rather than a summed total.

## [UNKNOWN]

- Per-notice victim cardinality and per-kill notice fan-out; whether the pinned main behavior
  matches the host systemd (261 when read in round 14; 262 on 2026-10-22); whether `UNIT=`/`USER_UNIT=` is present on every relevant host record;
  whether every OOM event yields a `UNIT_RESULT=oom-kill` record under this host's OOMPolicy;
  retention/rate-limit completeness; partial journal access; cross-scope duplicate identity.
- Whether any retained record on this host currently carries invalid or ambiguous subject
  metadata; the unattributed bucket's live size is unmeasured.
- Which signal produced a `UNIT_RESULT=signal` record, and who sent it; that arm carries no
  signal number and no sender identity.
- Which live fleet-related units lack a name token and therefore fall into the non-fleet bucket;
  the composition of both name-token buckets is unmeasured, and membership is not proven.
- No claim about a live GPF regression, fleet causation, or a unique victim.

## What it changes for mori

- Restore the OOM alarm as one global `OOM_KILL_JOURNAL` critical/DRIFT finding fed by structured
  notice and `UNIT_RESULT=oom-kill` record counts, with the four separate counters and no sum.
- Add `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` INFO for unusable or ambiguous subject metadata,
  `owner=unresolved`, while preserving the valid raw failure-record total.
- Keep fleet `UNIT_FAILURE_JOURNAL` and non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` (INFO, tsukuroi
  owner) as separate buckets selected by subject `UNIT=`/`USER_UNIT=` only, labelled
  `classification_rule=unit-name-token`; do not present the non-fleet bucket as proven fleet
  non-membership.
- Keep the cgroup-local `CGROUP_OOM_KILL` finding separate; it neither suppresses nor substitutes
  for the journal alarm.
- Replace the categorical `no-anchored-structured-field` wording with the three-way signal/GPF
  limit table, and keep unavailable classes explicitly unavailable rather than alarm or zero.
- Restore `KILL_SIGNAL_JOURNAL` as one user-scope WARN fed by two separate counters (process
  SIGKILL 9 and `UNIT_RESULT=signal`), never summed; system-scope result signal adds no warning.
- Preserve the r13 gains: six independent scoped counters, MESSAGE/COMMAND exclusion, validated
  `_BOOT_ID`, never summing user and system scopes, and the existing user-scope
  `unit_sigkill_record` `KILL_SIGNAL_JOURNAL` WARN path.

## Delivery paths this cannot see

Catalog notice counts cannot see: kernel OOM victims whose notice was not emitted or retained;
units without memory accounting or cgroup runtime; slice-level notices are included but name a
slice, not the descendant unit or process killed; processes outside a systemd manager; signals
the manager did not observe; non-unit process exits the manager did not reap;
signal sender or cause; OOM kills under
`OOM_CONTINUE` (no failure result); non-catalog failure texts; journal rate limiting or loss
(`e9bf28e6…`); records outside the queried boot, retention window or readable scope; and any
event whose record is forged. `fc2e22bc…` and `1f4e0a44…` are crash notices, not OOM kills;
`d989611b…` is an oomd notice for one or more processes.

## Fills (coverage-map ground; Frontier row)

Coverage-map ground: structured OOM alarm without victim overclaim, subject-unit fleet/non-fleet
routing with an explicit unattributed bucket, and three-way signal/GPF coverage limits. Frontier
FR1 remains partial: kernel victim attribution, per-process roll-up, signal-sender identity and
fleet causation remain frontier. The cgroup-local plane remains its own surface.

## Provenance limits

- Anchors are pinned systemd main `cf8ebfc6…`; host systemd was 261 in round 14 and is 262 on 2026-10-22 (`.ufo/waves/round-26/capture/capture.txt`). No version-equivalence claim.
- Supplementary unregistered code anchors: `src/core/cgroup.c:3055-3105`, `src/core/service.c:4704-4752`,
  `src/core/unit.h:1133,1177`. They are flagged as supporting code, not registered SOURCES rows;
  this note does not invent S ids for them. S036 covers `src/core/unit.c` but its registered
  anchor range is `:6333-6392`; `unit_log_field` `:6995-6997` lies outside it.
- S037 and S038 are L1-registered rows (`corpus/SOURCES.md` S037/S038, both mined and used-by
  this note). If a final row scope differs, adjust its used-by cell without rewriting this note's
  source claim.

## Measured implementation — L1, round 14

This supersedes the candidate/awaiting-measurement status of the target contract
above, not its source/version/trust limits. Census SHA-256
`0e41cb83fce2e8c5c711171e1cde2e6fa2809dcfce630eccabe52bcbe41516d9`
was measured at 8d22d18 (104/104 selftest) and 5601d12 (same census bytes).
The latter changes only the new gate's setup formatting and error map.

Commands `python3 tools/mori-round14-regressions.py --census
.ufo/waves/round-14/frozen/mori-census.sh --output
.ufo/waves/round-14/evidence/red-before-accepted` and the same command with
`--census tools/mori-census.sh --output
.ufo/waves/round-14/evidence/green-after-accepted` used the same committed
gate SHA `c39e5a7352666d09dc662293e1ea7be47ee3523b53247a5a6ae02e7dda19288d`.
Before: exit 1 with actual missing OOM critical alarms, signal-result warning
and fleet/non-fleet routing. After: exit 0, 43 cases plus the frozen-red control
pass (44 assertions). Six named behavioral acceptance arms fail **6 → 0**,
counted by the recorded jq command in `evidence/c1-measurement.json` under
`.ufo/waves/round-14/`. Frozen controls also fail new metadata-completeness
requirements; **43 failed assertions is not 43 production defects**.

Independent positive fixture counters, in class order kernel notice, oomd,
coredump, signal11, process SIGKILL, unit failure, are identical before/after:
user **3/0/2/1/2/1**, system **2/1/4/3/0/2**. Current-boot live bracketing
queries match all **12/12** cells, all zero; this is not live positive-load or
service-health proof (`evidence/live-measurement.json`, including reproducer).
The typed failed-subject partition, OOM result subset and source/error canaries
are fixture-proved, not authenticated fleet membership.

System fleet/non-fleet finding ids carry `_SYSTEM` suffixes; user ids retain
`UNIT_FAILURE_JOURNAL` / `UNIT_FAILURE_OUT_OF_SCOPE`. The unattributed id is
the same literal in both scopes, distinguished by `scope=`. Signal-only WARN
may carry `count=0` because that legacy field counts process SIGKILL records;
the positive `user_unit_signal` count is separate and is never summed.

The restored alarm is bounded: malformed class metadata, query denial or
timeout still yields explicit unavailable, not zero or DRIFT. A mixed stream
with a malformed MESSAGE_ID can hide an otherwise valid OOM indication
(`R14_SEC_DUP_MSGID_MIXED`); this inherited residual is disclosed, not certified
safe. Environment-selected binaries/timeout overrides, full store access,
retention and exhaustive fleet-name matching remain outside the guarantee.
