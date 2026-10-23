source: S157 (systemd v262 `src/core/unit.c:2773-2776` — the active-enter stamp is assigned only on a transition into active-or-reloading, and leaving that set stamps active-exit instead); S156 (systemd v262 `src/shared/bus-print-properties.c:19-24,194` — `ActiveEnterTimestampMonotonic` fails the `Timestamp`-suffix test, so `systemctl show` prints it as a bare decimal, `=0` when unset); S158 (systemd v262 `src/journal/journald-manager.c:1291-1295` — `Suppressed %i messages from %s`, emitted by journald, with the unit name); S159 (earlyoom commit `edd3d943` patch `:6-7`, `:34-36` — `Restart=always`, so a killed or crashed earlyoom starts again and prints a new version line); S160 (systemd v262 `src/journal/journalctl.c:512-517,543-546` — `-b` with no argument selects the current boot, `-u` adds the unit match); older rows re-used: S119 (earlyoom v1.9.0 `main.c:161` version line, `:295` dry-run line), S118 (`kill.c:627` send line, `:318` escalation), S122 (`org.freedesktop.systemd1.xml:2783-2790`: the stamps are 0 when the transition was not recorded this boot), S155 (dry-run is a send-site no-op), S154 (entry-object monotonic stamp); S120 (earlyoom `earlyoom.service.in` at v1.9.0 `:17` — `Restart=always` in the shipped file; added round 31, D4)
verified-at: 2026-10-22 — S156–S160 opened this round (access times and sha256 in `corpus/lessons/round-30.md` `## Gate`; excerpts in `corpus/evidence/sources-r30/`; all five re-fetched byte-identical by wave-2 seats `w2/ReopenS156.md`…`ReopenS160.md`); every decision-table row copies its case's frozen `expect` values, which the entering-tip tool blob `58b61681:tools/mori-oom-killers.py` and the tip tool both print (`.ufo/waves/round-30/count-c1.sh`; wave-2 CriticC1Admission F4); no host unit, journal, setting or signal touched
recheck: on an earlyoom release re-open `main.c` at the version and dry-run prints and the shipped unit's `Restart=`; on a systemd release re-open `unit.c` `unit_notify()`, `bus-print-properties.c` and `journald-manager.c` at the cited lines; after any change to `tools/mori-oom-killers.py` run its `--selftest --cases` on `cases.json`, `cases-supplementary.json`, `cases-a2.json` and `cases-a2-r30.json` and `--inputs` on each table row's case (the C1 counter pins the round-30 entering-tip blob and cannot test a new tool)
author: MoriR30 (L1); prose drafted by wave-1 seat DraftEntryC1 (`.ufo/waves/round-30/w1/DraftEntryC1.md`); source ids and decision-table rows bound by the L1

# Which earlyoom invocation a send line belongs to — scope, the restart split and the A2a limit (round 30)

## Why this entry

Round 26 recorded earlyoom 1.9.0 as this host's userspace OOM killer and counted its send lines
(`corpus/knowledge/userspace-oom-killers-r26.md`); round 27 read which process it picks
(`corpus/knowledge/oom-victim-selection-r27.md`). Neither says which run of earlyoom a send line belongs to, and the
round-29 closure routed exactly that question twice (R4, R6: `corpus/lessons/round-29-verifier-spotcheck.md:160-165`).
The reader `tools/mori-oom-killers.py` answers `KILLER_ACTED` (exit 1), `KILLERS_UNKNOWN` (exit 2) or `KILLERS_QUIET`
(exit 0).

## Facts

### 1. One invocation, as the reader sees it

- earlyoom prints `earlyoom <version>` once at startup (S119 `main.c:161`); each occurrence opens an invocation, and a
  line belongs to the segment opened by the latest version line before it (`.ufo/waves/round-30/rule-text.md:89-90`).
- The shipped unit restarts earlyoom whenever it is killed or crashes: S159 is the commit that introduced the line
  ("Have systemd restart us should we get killed or crash for some reason", `Restart=always`) and S120 is the
  `earlyoom.service.in` file at v1.9.0 that carries it (`:17`). So one boot can hold several invocations, and a restart
  writes a new version line: "send, restart" and "send, no restart" are different shapes.
- The journal the reader gets is the current boot of the earlyoom unit: `-b` with no argument enables the boot filter
  for the current boot and `-u` appends the unit match (S160 `journalctl.c:514-517,543-544`). Nothing before this boot
  is visible.

### 2. Bounded and unbounded scope

- systemd stamps a unit's active-enter time only on a transition into the active-or-reloading set, and stamps
  active-exit on the way out (S157 `unit.c:2773-2776`): a stop keeps the last active-enter stamp, the next start
  overwrites it. The properties hold 0 when no such transition was recorded this boot (S122
  `org.freedesktop.systemd1.xml:2789-2790`).
- `systemctl show` prints `ActiveEnterTimestampMonotonic` as a bare decimal, because the name does not end in
  `Timestamp` and holds no `USec` (S156 `bus-print-properties.c:19-24`, `:194`); an unset stamp therefore reads
  literally `ActiveEnterTimestampMonotonic=0`.
- For an active unit a non-zero stamp bounds the scope inclusively (`rule-text.md:25-26`): a send at the stamp acts, a
  send one microsecond before it does not.
- Missing or `0`: unbounded (A2-05, `rule-text.md:82-83`); `scope_complete` is false, the current invocation is the
  segment after the last version line, and lines before it count as earlier-invocation lines.
- An active earlyoom with `scope_complete: false` is `KILLERS_UNKNOWN` unless positive evidence stands
  (`rule-text.md:44-52`).

### 3. Where earlier-invocation sends go

- Sends and escalations outside the current invocation go to `earlyoom.earlier_invocation_send_lines` (A2-06,
  `rule-text.md:84-88`); a record without a numeric stamp is not counted there either (A2-10, `rule-text.md:114`).
- It changes the verdict only when earlyoom is not `active` (`inactive`, `absent` for `LoadState=not-found`, or a
  non-steady state mapped to `unavailable`): then a non-zero count is `KILLER_ACTED` while `actions` stays `null`.
- Round-30 change (C2.1, the round-29 Judge11–13 `tool error` rulings): for a non-active unit with a readable show text
  and a retained non-zero stamp (S157), the reader scopes the last invocation from that stamp, reports the last version
  line inside that retained scope (`earlyoom.version` is `null` when no version line is at or after the stamp; round-31
  correction D4 below) and its zero line counters, keeps `actions: null`, and treats a send inside that last invocation
  as positive evidence too (`.ufo/waves/round-30/evidence/fix-tool.diff`; differential
  `.ufo/waves/round-30/evidence/c2-differential.txt`).
  Limit (wave-2 CriticC1Admission F3): such a last-invocation send is counted in no output field — the verdict is
  `KILLER_ACTED` while `earlier_invocation_send_lines` excludes it and `actions` stays `null`, so a non-active
  `KILLER_ACTED` can carry every count at 0. Routed to the tool as a named residual.
- For an `active` earlyoom the earlier count is report-only: `a2-06-active-earlier-invocation-sends-quiet` pins
  `KILLERS_QUIET` with `earlier_invocation_send_lines: 2` — the disclosed A2a limit (`rule-text.md:79-80`).

### 4. The disputed shape: active, stamp absent or 0, a real send, then a plain restart

- Shape: `ActiveState=active`, stamp absent or `0`, two or more version lines, a real (not dry-run) send or escalation
  before the last version line and none after it.
- Answer: `KILLERS_UNKNOWN`, exit 2, with `state: active`, `scope_complete: false`, `actions.sigterm: 0`,
  `actions.sigkill: 0`, and the send kept in `earlier_invocation_send_lines`, not moved into `actions`.
- Why: the last segment cannot be bounded, so "quiet now" is unproven, and A2-06 makes an active unit's earlier sends
  report-only. The pre-round-29 answer was `KILLER_ACTED`; the round-29 closure ruled the change **not harmed**
  (`corpus/lessons/round-29-verifier-spotcheck.md:77-98`).
- Pinned this round by eight blind frozen cases (`tools/fixtures/mori-oom-killers/cases-a2-r30.json`, four writers who
  read only the rule text): all eight expect this answer and both the entering-tip and the changed tool print it.
  Disclosed: the rule text alone does not decide the shape uniquely — a literal reading of the scope line gives
  `KILLER_ACTED` (wave-1 `ReviewRuleTextShape` F1); the writers and the tool agree on the split reading.
- No older frozen case has this shape, so it has no row in the decision table below. It is a robustness input: every
  entry into active overwrites the stamp (S157), so an active unit that reads `0` or no stamp while its journal holds
  two or more version lines needs a transition systemd did not record this boot [INFERENCE].

### 5. Dry-run is per invocation

- `dryrun mode enabled` is logged at startup (S119 `main.c:295`) and a dry run returns before `kill()` (S155), so later
  sends in that segment are decisions, not deliveries: they go to `earlyoom.dryrun_send_lines`, `sigterm`/`sigkill`
  stay 0 and are never positive evidence (A2-04, A2-07).
- The split is at version lines, so one dry-run invocation does not zero another's real sends.

### 6. Stamp-less records and suppression notices

- A record whose `__MONOTONIC_TIMESTAMP` is absent or not a number is left uncounted in both counts and makes the scope
  incomplete (A2-10, `rule-text.md:95-98,114`; the entry-object stamp is S154's).
- journald itself writes the rate-limit notice, naming the unit: `Suppressed %i messages from %s` with the count
  `rl - 1` (S158 `journald-manager.c:1294`). An in-scope notice means earlyoom lines are missing, so `scope_complete`
  is false (A2-01, `rule-text.md:105`); the check is scope-local.

## Decision table

Every row's verdict and fields are the case's frozen `expect` values and are printed by the entering-tip tool on that
case's inputs (`bash .ufo/waves/round-30/count-c1.sh <rev>`).

| shape | verdict | fields | case | sources |
|---|---|---|---|---|
| bounded scope, an in-scope send with its process-group line | `KILLER_ACTED` | `earlyoom.scope_complete=true`, `earlyoom.actions.sigterm=1` | `a2-03-group-kill-one-with-sigterm-action` | S157 |
| bounded scope, suppression notice one microsecond before the stamp | `KILLERS_QUIET` | `earlyoom.scope_complete=true` | `a2-01-suppressed-before-scope-start` | S158, S157 |
| bounded scope, version line before the stamp, only an escalation after it | `KILLER_ACTED` | `earlyoom.scope_complete=false`, `earlyoom.actions.sigterm=0` | `c34-escalation-only-incomplete-scope` | S157, S118 |
| active, stamp `0`, no send line | `KILLERS_UNKNOWN` | `earlyoom.scope_complete=false` | `a2-05-monotonic-zero-active-quiet` | S156, S122 |
| inactive, stamp `0`, no send line | `KILLERS_QUIET` | `earlyoom.scope_complete=false`, `earlyoom.state="inactive"` | `a2-05-monotonic-zero-inactive-quiet` | S156, S157 |
| active, sends only in an earlier invocation | `KILLERS_QUIET` | `earlyoom.earlier_invocation_send_lines=2`, `earlyoom.scope_complete=true` | `a2-06-active-earlier-invocation-sends-quiet` | S159, S119 |
| stopped unit, sends in earlier invocations | `KILLER_ACTED` | `earlyoom.earlier_invocation_send_lines=3`, `earlyoom.state="inactive"` | `a2-06-inactive-earlier-invocation-sends-acted` | S157, S159 |
| active, an earlier send and a current send | `KILLER_ACTED` | `earlyoom.earlier_invocation_send_lines=1`, `earlyoom.actions.sigkill=1` | `a2-06-active-earlier-and-current-send-acted` | S159 |
| earlier real invocation, current dry-run invocation | `KILLERS_QUIET` | `earlyoom.earlier_invocation_send_lines=2`, `earlyoom.dryrun_send_lines=1` | `a2-07-earlier-real-then-current-dryrun` | S159, S155 |
| three invocations, dry-run in the middle | `KILLER_ACTED` | `earlyoom.earlier_invocation_send_lines=2`, `earlyoom.actions.sigterm=1` | `a2-07-three-invocations-dryrun-in-the-middle` | S159, S155 |
| removed unit, two invocations with sends | `KILLER_ACTED` | `earlyoom.scope_complete=false`, `earlyoom.state="absent"` | `a2-09-removed-unit-two-invocations-mixed-sends` | S159 |
| journald suppression notice inside the scope | `KILLERS_UNKNOWN` | `earlyoom.scope_complete=false` | `a2-01-suppressed-in-scope-active-quiet` | S158 |
| send record without a numeric monotonic stamp | `KILLERS_UNKNOWN` | `earlyoom.scope_complete=false`, `earlyoom.actions.sigterm=0` | `a2-10-malformed-action-line-uncounted` | S154 |

## Limits

- A2a: an active earlyoom's earlier sends never change the verdict; the disputed shape is `KILLERS_UNKNOWN` with the
  send reported, not `KILLER_ACTED`. Disclosed, not a gap to re-litigate.
- A1a: incomplete-scope counts are lower bounds printed as counts (frozen `c04`); A3: no logger-heartbeat check, so a
  bounded scope with only a version line reads quiet (`c19-version-line-only`).
- A2-10: an uncounted record makes the result abstain but says nothing about its content. Suppression is scope-local.
- Scope is the current boot only (S160); no cross-boot count. A stop keeps the last active-enter stamp (S157), so a
  stopped unit's last invocation is bounded by a stamp from its last start, not by its stop.
- No `MESSAGE` text, process names, command lines, uids or host prefer/avoid expressions in the output
  (`rule-text.md:54-55`); counts are log lines, not processes signalled or killed (A5).

## Not claimed

No host read; the shapes above are inputs, not observations. No claim that any restart happened on this host; no
tool, unit or journal change.

## Adjacent

`corpus/knowledge/userspace-oom-killers-r26.md` owns the grammar and live counts;
`corpus/knowledge/structured-journal-scopes-r13.md` owns the timestamp mechanics; the host's OOM configuration stays
with tsukuroi (`.ufo/waves/round-30/w1/ConnectorSiblings.md`); this entry owns the invocation boundary.

## Round-31 correction (routed D4; wave-1 FixEntryVersionD4; QUALITY 77: corrected in place above and recorded here)

- Old text at `a12c68ae`, lines 52-55: "for a non-active unit with a readable show text and a retained non-zero stamp (S157),
  the reader scopes the last invocation from that stamp, reports its version and its zero line counters, …". "Reports
  its version" held only for a version line at or after the retained stamp (round-30 wave-2 ReviewEntryProse LOW-2,
  `.ufo/waves/round-30/w2/ReviewEntryProse.md:27-43`; `corpus/lessons/round-30.md:231-232`). The tool sets
  `version = None` (`tools/mori-oom-killers.py:360`), assigns it only while iterating version lines inside the retained
  scope (`:389-396`, scope filter `stamp >= aetm` at `:305-322`) and emits it as `earlyoom.version` (`:518`), so it is
  `null` when no version line is at or after the stamp and the last such line otherwise. Corrected in place at lines
  53-58.
- Old text at `a12c68ae`, lines 23-25, cited S159 alone for `Restart=always` (round-30 ReviewEntryProse LOW-1). S159 is
  the commit that introduced the line (`corpus/SOURCES.md:165`); S120 is the `earlyoom.service.in` file at v1.9.0 that
  carries it at `:17` (`corpus/SOURCES.md:126`). Corrected in place at lines 23-26 to name both; no SOURCES cell changes.
