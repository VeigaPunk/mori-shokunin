---
name: mori-shokunin
description: "Fleet & host observability (森) — detect and report fleet liveness, wave settlement, kill/OOM events and resource runway. Triggers: 'fleet health', 'did a wave die', 'why did the daemon vanish', 'watchdog liveness', 'OOM kill'. Anti-trigger: NOT dispatch/orchestration (kumitate), NOT OS package/systemd/driver state (tsukuroi), NOT endpoint health (kama). Rank: shonen."
---

# mori-shokunin — fleet & host observability (森)

Domain: observing whether the fleet and its host are ALIVE and progressing — and
reporting it. **Detection and report only. This lane never remediates.**

## Decision table

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| Is the shokunin fleet alive? | watchdog pid + log freshness + `.ufo/state/*.round` values (count, max, per-lane value vs the ledger's last launch round) | restarting a daemon; killing a pid | `liveness` rows: pid, start time, last tick, state; `WATCHDOG_STATE_LAG`/`_AHEAD` are info — visibility, not severity |
| Did a wave settle? | `.ufo/waves/*/swarm-registry.json` + dispatch/results pair | assuming an unsettled wave is a failed one | per-wave settled/unsettled with age |
| Did something get killed? | MESSAGE-free `journalctl --user/--system -b` catalog-ID records — kernel-OOM notice, oomd notice, coredump, unit-process SIGKILL, unit-failure with result — plus the validated `UNIT_RESULT=oom-kill` and user `UNIT_RESULT=signal` paths; cgroup event counters | remediating, renicing, killing; treating a client-set MESSAGE_ID as authenticated or a notice as a unique victim | independent `scope=user or scope=system` record counts and current-boot anchor; per-scope validated-positive tokens `positive_kernel_oom`/`positive_unit_oom`/`positive_unit_signal`/`positive_process_sigkill` survive an adjacent invalid record while every raw aggregate/split token stays `unavailable`; ONE global `OOM_KILL_JOURNAL` crit → DRIFT when any independently valid positive OOM record exists, carrying four separate raw counters (`user_notice`/`system_notice`/`user_unit_oom`/`system_unit_oom`, never summed); fleet `UNIT_FAILURE_JOURNAL` info vs non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` info `owner=tsukuroi`, subject from exactly one valid `UNIT`/`USER_UNIT`, unclassifiable `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` info `owner=unresolved` (owner partition aggregate-only); user SIGKILL/`UNIT_RESULT=signal` `KILL_SIGNAL_JOURNAL` warn from independently valid user records even when raw `count`/`process_sigkill` is `unavailable`; arbitrary unreported signal paths remain unmeasured; cgroup count with selected source path/scope and observation time, not an event timestamp |
| Did journal records arrive after a retained anchor? (r16 probe) | `python3 tools/mori-journal-window.py --anchor <PATH> --scope user\|system` — exact-anchor window, see "Window probe (r16)" below | advancing, creating or rewriting the anchor; treating a missing, vacuumed, mismatched or foreign-boot anchor as zero; printing raw cursors, record text or `MESSAGE`; summing scopes; reading the window as a victim count | one JSON object on stdout: `rc0 finding_id=MORI_JOURNAL_WINDOW_OK` with `records_after_anchor`, the four never-summed `positive_*` counts and `evidence_basis=validated-record-subsets`; otherwise `rc2` with `MORI_JOURNAL_WINDOW_UNAVAILABLE reason=<stable>` or `MORI_JOURNAL_WINDOW_SETUP` |
| Is there resource runway? | `df -P` on the fleet root and `/tmp`; since-boot write average per target device; memory pressure PSI + fill/avail against labeled-local thresholds; scope high-watermark `memory.peak` | deleting files; resizing; tuning a labeled-local threshold to fit one observation | runway rows with the measured value: `used_pct`, `io_basis=since-boot`, `psi_some_avg10`, `mem_fill_scope`, `mem_peak` + `mem_peak_anchor` |
| Is a tmux session fleet work? | `tmux ls` + `list-panes -a` pane current paths under the fleet root; per-relevant-session `display-message` activity under a per-call timeout bound | killing/attaching to/steering sessions; treating foreign, or idle past a labeled-local number, as unhealthy | `sessions=N relevant=R foreign=F unclassified=U`; relevance rows carry `freshness=ok probed=P idle=I freshness_unavailable=U`; `TMUX_FOREIGN_SESSION` info per foreign session (path-based rule); `TMUX_SESSION_IDLE` info (r8) |
| Was a lane silent? | roster = `shokunin.conf` lane ids (parsed, never sourced) ∪ `.ufo/state/*.round` names (r12; `MORI_ROSTER_LANES` overrides); launch epoch from `.ufo/watchdog.log` + post-launch authorship (commits/files) | declaring failure from commit sparsity; sourcing the conf | silent / progressing / progressing-weak / young / not-open / unavailable; `roster_source=` + `ROSTER_SET_MISMATCH` info naming conf-only / state-only ids |

## Error patterns

| Observation | Reading |
|---|---|
| watchdog pid gone, no `complete` line | daemon death — a fleet-liveness finding, not a lane failure |
| wave registry present, no results | wave dispatched but never settled — age it, do not call it failed |
| Positive cgroup `oom_kill` | cumulative counter for the named source; counters alone identify neither the killed PID, event time nor fleet membership, and cover only the selected cgroup — descendants and other scopes sit outside it, so it is not a substitute for the journal `OOM_KILL_JOURNAL` alarm |
| `oom_kill=0` (cgroup `memory.events` or `/proc/vmstat`) | no **kernel** OOM kills — not "no memory kills": both counters move only at the kernel victim site ([oom_kill.c:935-936 v7.2](https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c)); systemd-oomd kills via `cgroup.kill`/`kill()` and records `user.oomd_ooms`/`user.oomd_kill` xattrs instead ([oomd-util.c:269-306 v261](https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c)); an inactive oomd/earlyoom is `unavailable (inactive)`, never 0 — `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`, `userspace-oom-killers-r12.md` |
| journal class counts | count records carrying catalog `MESSAGE_ID` (`fe6faa94…` kernel-OOM unit notice, `d989611b…` oomd notice, `fc2e22bc…` coredump, `98e32220…` unit-process SIGKILL, `d9b373ed…` unit failed — [systemd.catalog.in](https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in)) with `-o json --output-fields=`, never `MESSAGE` text; `COREDUMP_SIGNAL=11` and `EXIT_CODE=killed`/`EXIT_STATUS=9` are separate validated-field classes. IDs are client-set ([journal-fields](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html)), not authenticated emitters. Scopes are never summed; nonzero query rc, stderr, timeout or malformed JSON makes both aggregate and positive evidence unavailable. A semantic record failure in a successfully parsed capture makes raw aggregate/split tokens `unavailable`, never zero, but may retain individually qualified r15 positive evidence (see below). `drift=` counts warning/critical FINDING lines, not notice records or killed processes — `corpus/knowledge/structured-journal-scopes-r13.md`, `corpus/knowledge/journal-alarm-routing-r14.md` |
| positive OOM notice (`fe6faa94…`) in either scope, a validated `UNIT_RESULT=oom-kill` record, or a `positive_kernel_oom`/`positive_unit_oom` token > 0 | ONE global `OOM_KILL_JOURNAL severity=crit` per census → DRIFT when any independently valid positive OOM record exists, with four separate raw counters `user_notice`/`system_notice`/`user_unit_oom`/`system_unit_oom` that are never summed; a raw counter may read `unavailable:<reason>` while the positive token is > 0 — an adjacent malformed, nonmatching or foreign-boot record invalidates the aggregate, not the individually valid record. A known positive arm alarms even when another arm is `unknown` (`user_unit_oom_result_unknown`/`system_unit_oom_result_unknown` stay explicit, never fabricated zeros). This restores the r13-demoted mint-critical alarm. The class reports an OOM **event**, not a unique victim or a complete total: it carries no pid/uid/cgroup/time and cannot choose between several notices; a client-set ID makes it a reportable notice, not authenticated causation. The crit grade is mint demand (a kill is worth a human look), not a trust or victim-attribution claim |
| fleet vs non-fleet unit failure | generic severity is `info` on both sides: fleet `UNIT_FAILURE_JOURNAL`, non-fleet `UNIT_FAILURE_OUT_OF_SCOPE owner=tsukuroi` (triage pointer, never an action this lane takes). Classification takes exactly one valid subject field — `UNIT` or `USER_UNIT`, independent of journal scope, shaped as a 1–255-char systemd unit name with a known suffix — with `classification_rule=unit-name-token` over the historical case-insensitive tokens `shokunin`, `ufo-sighting`, `tmux-spawn`, `the-tick`, `fleet` (frozen `probe_journal` r12); "non-fleet" means no marker, not proof of unrelatedness, and this is not a claim of exhaustive fleet membership. No fallback to `_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT` emitter metadata, and only a validated count leaves the parser (unit bytes are never echoed). The system-scope id previously counted **all** system unit failures; it now counts fleet-only — new semantics, not a silent reuse of the id |
| unit subject absent, malformed, or ambiguous | `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` in either scope, `severity=info count=N scope=user\|system owner=unresolved reason=subject-metadata-unknown` — never `non-fleet` and never a fake zero. Both subject fields present is `unknown` even when identical; a failed, malformed or multi-boot query makes that class and the whole owner partition `unavailable` — aggregate-only, with no positive salvage into the partition and no partial bucket — and the fleet split is only as good as the fields the query kept |
| user `UNIT_RESULT=signal` on a unit-failure record, or a user `positive_unit_signal`/`positive_process_sigkill` token > 0 | one user-scope `KILL_SIGNAL_JOURNAL severity=warn` line with separate never-summed raw counters `process_sigkill` (`EXIT_CODE=killed`/`EXIT_STATUS=9`) and `user_unit_signal` (`UNIT_RESULT=signal`), restoring the legacy text class `Failed with result 'signal'` through the structured result field. The warn fires when either independently valid current-boot positive record exists, even if the raw `count=`/`process_sigkill`/`user_unit_signal` fields read `unavailable:<reason>` because an adjacent record invalidated the class; those raw fields are never rewritten as positive counts. A signal result alone is DRIFT for that user unit; a generic `signal` result is **not** proof of signal 9 and is never counted as signal-9 evidence, and cause stays unknown (a kernel OOM can also deliver SIGKILL). The system scope keeps no such warn — its unit results stay `info` through the failure-routing ids. Signal numbers other than 9, and kills leaving no retained record, remain unknown/unmeasured — never zero |
| `JOURNAL_CLASSES_UNMEASURED` reasons | names why each remaining class is unmeasured instead of a fake zero: `kernel_victim_text`/`gpf_text`/`uncataloged_unit_failure` are retired text heuristics (never aliases, never counted), `other_signals` is a structured field this probe has not implemented (EXIT_CODE/EXIT_STATUS records exist; S036 — only `EXIT_STATUS=9` is counted here), and `absent_records=possible:no-retained-record-is-not-no-event` keeps a missing record distinct from a missing event. No categorical "no structured field exists" claim |
| a kill needs PID / uid / cgroup / time | the kernel `oom-kill:constraint=…,task_memcg=…,pid=…,uid=…` record in the system journal (`journalctl -k`, `__REALTIME_TIMESTAMP` always printed — [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html)) is event-time attribution; only shape-validated tokens may leave a probe; re-reading the victim's cgroup later is not attribution (`ENOENT`) — `kernel-oom-line-attribution-r12.md`; not yet a census probe (PROVINCE Frontier). `OOM_KILL_JOURNAL`, its r15 positive tokens and the `UNIT_RESULT=oom-kill` subtype are alarms, not this attribution — none names a unique victim |
| process alive, last tick stale | wedged, not dead — report the age |
| `state_lag=` / `state_ahead=` counters | per-lane round VALUE vs the ledger's last `launch <lane> round=N` line; both info — a state file can disagree without the fleet being unhealthy |
| `state_val_unread_reasons=file:N symlink:N dir:N other:N` | every `*.round` ENTRY is classified before any read; a symlink/directory/non-regular entry is counted with its `WATCHDOG_STATE_ENTRY_UNREADABLE` info instead of vanishing, and symlinks are never followed; `state_val_unreadable` totals them (unreadable values + non-regular entries) while `state_rounds` still counts regular files only |
| `psi_some_avg10` past `psi_warn_avg10`, or fill/avail past their floor | memory pressure graded against labeled-local thresholds (`MEM_PRESSURE_HIGH`/`MEM_FILL_HIGH`/`MEM_AVAIL_LOW` are warn — a local placeholder can flip the roll); `mem_fill_scope=` names the scope — `cgroup` with a numeric `memory.max`, else the `host-ram` fallback, `unavailable` when neither can be read |
| cgroup `mem_peak=` / `mem_peak_source=` / `mem_peak_anchor=` | the scope's kernel high-watermark, comparable only within one cgroup instance (the anchor is the scope dir's mtime); `shape-refused`/`absent`/`unreadable` when it cannot be read — never a fake zero, and it is not a threshold |
| disk row `io_avg_since_boot=` | a since-boot AVERAGE (sectors written × 512 ÷ uptime), never an instantaneous rate; `DISK_IO_UNMEASURED` info when no target device yielded one; the two-sample instantaneous rate stays deferred on measured grounds (the 0.2 s dwell costs ≈208–222 ms across three independent isolations, the extra reads alone 16 ms median); an operator-pinned writer-less FIFO for `MORI_DISKSTATS`/`MORI_UPTIME` is a named open hang, not the live default |
| tmux `foreign=` / `TMUX_FOREIGN_SESSION` | pane-cwd classification only; foreign is a relevance fact, never an unhealthy fleet; a session absent from pane data counts `unclassified`, and no pane data at all → `relevance=unavailable` — neither is foreign |
| tmux `freshness=` / `TMUX_SESSION_IDLE` | idle = now − `session_activity`, probed for fleet-relevant sessions only via one timeout-bounded client call each (default bound 2 s per call, so the freshness block's worst case scales with the relevant-session count); past `idle_warn_s` (default 3600, labeled local) it is info, never DRIFT; `freshness=unavailable` carries its reason (`rc-<N>` — `rc-124` when the bound fired, `rc-137` when the grace kill did, `unparseable` on the row / `unparseable-probe-output` on the finding, `no-timeout-bin` — the probe refuses to run unbounded, `mixed` when only some relevant sessions could be measured) and is never idleness |

## Positive evidence vs an unavailable aggregate (r15)

The r15 repair is deliberately narrow: it preserves an alarm from an individually
valid structured record when an adjacent record invalidates its class. It does
not make the class complete and does not repair malformed input.

- **Per-scope evidence tokens.** `positive_kernel_oom`, `positive_unit_oom`,
  `positive_unit_signal` and `positive_process_sigkill` count only object
  records with a scalar `MESSAGE_ID` equal to the class id and a scalar
  `_BOOT_ID` equal to the current boot. The unit-OOM/signal tokens require
  `UNIT_RESULT` to be exactly `oom-kill`/`signal`; the process token requires
  `EXIT_CODE` exactly `killed` and scalar `EXIT_STATUS` 9 (string `"9"` or
  number `9`; bool, array and null are rejected). Subject metadata is
  irrelevant to these predicates, so a valid positive does not need a usable
  `UNIT`/`USER_UNIT`. The tokens appear scope-local on each
  `journal.<scope>` surface row, followed by
  `positive_basis=validated-subset-lower-bound` and
  `positive_validation=scalar-id+current-boot`; the single OOM line carries the
  scope-prefixed `user_positive_kernel_oom`/`system_positive_kernel_oom` and
  `user_positive_unit_oom`/`system_positive_unit_oom` with the same two basis
  tokens; the user signal line carries
  `user_positive_process_sigkill`/`user_positive_unit_signal`
  (user-only; the system INFO path carries none),
  `positive_basis=validated-subset-lower-bound`,
  `positive_validation=scalar-id+current-boot+exact-fields`, and
  `alarm_basis=validated-positive-records` (or
  `scoped-record-count+validated-positive-records`) names the firing basis.
- **Raw counts stay aggregate-only.** When any record invalidates a class, its
  raw aggregate/split token — and the unit owner partition — stays
  `unavailable:<reason>`. A positive token is separate evidence, never spliced
  into that raw token and never a partial total. Scopes remain separate and are
  never summed.
- **Alarm rule.** One global `OOM_KILL_JOURNAL crit` fires once if any
  independently valid positive OOM record exists, even when every raw OOM
  counter is `unavailable`. The user `KILL_SIGNAL_JOURNAL warn` likewise fires
  from an independently valid user unit-signal or process-SIGKILL record even
  when raw `count`/`process_sigkill`/`user_unit_signal` is unavailable; the
  system scope keeps no signal warn.
- **Failure rule.** The positive pass consumes the same captured, stderr-free,
  valid JSON stream as the class counts — no second journal query. A nonzero
  query rc, timeout, stderr bytes, or unparseable JSON makes the positive
  tokens `unavailable:<reason>` (for example `unavailable:rc-1`,
  `unavailable:timeout`, `unavailable:stderr-nonempty`,
  `unavailable:malformed-json`), never numeric zero. Semantic aggregate statuses
  (`record-invalid`, `multi-boot`, `boot-mismatch`) alone do not invalidate an
  independently parsed positive subset. A
  parsed stream with no individually valid record is a real 0 for that positive
  token — not a class total; excluded records never become counts. Array/non-string
  `MESSAGE_ID`/`_BOOT_ID`, foreign boots, and array/null/wrong-case result
  fields are excluded per record.
- **Not claimed.** Positive evidence is not completeness, not a victim count,
  not a unique victim or authenticated emitter, and not fleet causation.
  Malformed JSON is still unknown, not repaired; owner routing stays
  aggregate-only, and no new route or actuation is added.

Ground and full decision table: `corpus/knowledge/journal-positive-evidence-r15.md`
(S014/S015/S037/S038; an interface reading, not a measured live positive).

## Window probe (r16) — exact retained anchor, no census change

`tools/mori-journal-window.py` acquires a bounded, MESSAGE-free observation of
journal records written after one retained anchor. It is a **probe**: the
production census (`tools/mori-census.sh`) does not call it, adds no `SURFACE`
or `FINDING` row, and changes no alarm, drift verdict or positive token. The r10
drift pin stays red and is not re-pinned by this change.

- **Precondition: an exact retained anchor.** The caller supplies a file whose
  JSON object has `schema` = `mori-journal-anchor-v1`, `scope` = `user` or
  `system`, `boot_id` (32 lowercase hex) and `cursor` (an opaque printable scalar,
  at most 4096 characters, no control characters). The probe only reads it. It
  never creates, rewrites or advances an anchor and writes no cursor state. An end
  cursor may be reported but is not written. Stdout carries at most a SHA-256
  digest of the anchor, never the raw cursor or record text.
- **Continuity or unavailable.** The window counts only records after the anchor
  when the first parsed record carries exactly the anchor cursor and boot; that
  record is dropped. Every later record must be a same-boot object with a unique,
  valid scalar cursor. A missing, vacuumed or mismatched anchor cursor, a foreign
  boot, a duplicate or malformed cursor, a nonzero rc, stderr, timeout or overflow
  returns `rc2 MORI_JOURNAL_WINDOW_UNAVAILABLE` with a stable reason. Unavailable
  is never zero and never a positive total.
- **Claims it does not make.** The success path is exact retained-anchor
  continuity only. FR11 (`PROVINCE.md:51`) is not closed by it: cursor rotation and
  vacuum behavior remain `[UNKNOWN]`. The counts are validated record subsets
  (`evidence_basis=validated-record-subsets`), not completeness, an authenticated
  emitter, a unique victim or fleet causation. The four counts
  (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`,
  `positive_process_sigkill`) reuse the r15 predicates and are never summed across
  scopes.
  The window `positive_*` is a separate after-anchor identity: it is not comparable with, and does not substitute for, the census whole-boot `positive_*` or the r15 alarm retention, because the window refuses the whole window on any invalid record, whereas the census keeps individually valid positives beside invalid siblings.
- **Setup is not a window.** An invalid anchor or argument returns
  `rc2 MORI_JOURNAL_WINDOW_SETUP`. Neither code is a DRIFT, severity or alarm.

## Boundaries (hard)

- **Refuses dispatch mechanism** — that is kumitate. mori observes the fleet, it
  does not start, steer, or reparent anything.
- **Refuses OS-package state** — pacman/systemd units/drivers/firmware/boot are
  tsukuroi. mori reads journal and cgroup counters as fleet-relevant events and
  reports them; it never claims OS-state ownership and never repairs.
- **Refuses endpoint/model health** — kama.
- Credentials, oauth, `server.token` and session material are SHAPE ONLY.

## Checklist (executable)

- [ ] Every observation names its command and the revision/date measured.
- [ ] A missing surface is reported as `unavailable`, never as unhealthy.
- [ ] No remediation is performed or recommended as an action this lane takes.
- [ ] Findings carry a stable id so a later run can compare.

## Gates

`tools/mori-census.sh` — read-only census over the fleet-liveness surfaces.
`verify` → `MORI_CENSUS: CLEAN|DRIFT` exit 0/1, `--selftest` over fixtures,
exit 2 for setup/usage. Registry (PROTOCOL.md §Gate standard fields):

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| census | gate | `bash tools/mori-census.sh` (`MORI_SHOKUNIN_ROOT=<fleet root>` outside the fleet tree) | 0 clean · 1 failed (DRIFT) · 2 could-not-evaluate; r17 `HEAD_BRANCH_MISMATCH`/`LANE_AUTHOR_MISMATCH` are warn findings | `bash tools/mori-census.sh --selftest`; r17 measured tally and hash in round-17 evidence | expected ids/exits in `run_selftest()` | none live; selftest temp tree | mori |
| drift pin | gate | `bash tools/mori-census.sh --drift <baseline>` | 0 clean (`none`) · 1 failed · 2 could-not-evaluate (baseline missing/unreadable/malformed) | `--selftest` pin/drift arms | `corpus/evidence/baseline-r10-20261015T2231Z.json` | none (`--pin` writes only its path) | mori |
| silence oracle | gate | `bash tools/mori-silence-cases.sh` | 0 clean (all matched) · 1 failed · 2 could-not-evaluate | itself (hermetic case table, 28 cases) | case table in-script | temp fixtures | mori |
| r13 regressions | gate | `python3 tools/mori-round13-regressions.py --output <dir>` (`--census`/`--oracle` default to the repo `tools/*.sh`; `--frozen-dir` default `.ufo/waves/round-13/frozen`) | 0 clean · 1 failed (claim mismatch) · 2 could-not-evaluate (usage/setup, unreadable target, `snapshot_tampered`, unbuildable requested mutation) | `python3 tools/mori-round13-regressions.py --selftest` — parser checks plus isolated real-gate subprocess cases asserting exit and stable finding ids; measured tally in round-14 evidence | in-script `FROZEN_PINS` and `FROZEN_BASE_COMMIT` independently pin the default frozen census/oracle/manifest; custom frozen directories are manifest-only and explicitly unpinned; expected claim ids/values are in-script; evidence names revision and dirty flag | `<dir>` evidence tree only; fixtures removed unless `--keep-fixtures` | mori |
| r14 regressions | gate | `python3 tools/mori-round14-regressions.py --output <dir>` (`--census` default `tools/mori-census.sh`; `--frozen` red control default `.ufo/waves/round-14/frozen/mori-census.sh`) | 0 clean · 1 failed (claim failed, or the frozen control did not reproduce the defect) · 2 could-not-evaluate (usage/setup/pin, `snapshot_tampered`, unexpected internal error) | `python3 tools/mori-round14-regressions.py --selftest` — 20 checks including real-gate red rc1 and tamper rc2 at 5601d12, harness SHA `c39e5a73…`; `evidence/r14-selftest-accepted.json` under round-14 waves | in-script `PINNED_SHA256` for `.ufo/waves/round-14/frozen/mori-census.sh` (`39abda0a…`, the r13 delivered bytes) + expected claim ids/values | `<dir>` evidence tree only; fixtures removed unless `--keep-fixtures` | mori |
| r15 regressions | gate | `python3 tools/mori-round15-regressions.py --output <dir>` (`--census` default `tools/mori-census.sh`; `--fixtures` default `.ufo/waves/round-15/fixtures`; `--expected` default `.ufo/waves/round-15/expected.json`; `--frozen` default `.ufo/waves/round-15/frozen/mori-census.sh`, else `git show 0fa5e0d:tools/mori-census.sh`; `--pin-fixtures <path>` regenerates the expected table after packs settle) | 0 clean (all SUT expectations pass and the frozen control reproduces the entering red state on red-relevant cases) · 1 failed (a SUT fixture expectation failed) · 2 could-not-evaluate (usage/setup/pin/fixture-schema/control error, digest or expected-table mismatch, `snapshot_tampered`, missing expected table, unexpected internal error) | `python3 tools/mori-round15-regressions.py --selftest` — actual isolated gate subprocesses with temp packs/wrappers, asserting exit and stable expected ids; tally is measured at L1 integration, not predicted here. The r15 CLI has no hidden flags: `--selftest-child` and `--no-frozen-control` were removed from it (the r14 harness's `--no-frozen-control` belongs to that other tool); any unknown argument is refused by argparse with rc2, and `--selftest` refuses `--output` and `--pin-fixtures` with rc2 | in-script `PINNED_FROZEN_SHA256` `0e41cb83…` and `PINNED_BASE_COMMIT` `0fa5e0d…` (never trusted from a manifest; digest mismatch exits 2); expected table `.ufo/waves/round-15/expected.json` pins each fixture pack SHA-256, static per-case expectations, and gate/r14-helper/frozen digests (any later gate or r14 edit requires re-pin); runs store `expected.json` + `run-manifest.json` (revision, dirty path scope) under `<dir>` | `<dir>` evidence tree only, and `--output` must not equal/cover the fixture directory, repository root, `tools/`, `.git/` or `corpus/`; fixture packs read-only, a `MESSAGE` key is a setup error | mori |
| r16 regressions | gate | `python3 tools/mori-round16-regressions.py --tool tools/mori-journal-window.py --fixtures .ufo/waves/round-16/fixtures --expected .ufo/waves/round-16/expected.json --output <dir>`; `--pin-fixtures <path>` persists the digest table after packs settle | 0 all cases match · 1 mismatch or `capability_absent` (missing-before capability, not a production bug) · 2 usage/setup, digest mismatch, tamper or moving inputs | `python3 tools/mori-round16-regressions.py --selftest` — isolated actual gate subprocess arms; L1 records observed results | `.ufo/waves/round-16/expected.json` pins every pack plus gate and probe SHA-256; missing/mismatched table is not green | `<dir>` evidence only: wrappers, synthetic streams and manifest with load/end hashes, actual HEAD and porcelain; selftest uses isolated temporary trees | mori |
| r16 context check | gate | `python3 tools/mori-round16-context-check.py --spec PATH` (`--selftest` for isolated subprocess arms) | 0 `CONTEXT_OK` · 1 `CONTEXT_MISSING` · 2 `CONTEXT_SETUP` (usage, unreadable or invalid JSON); eight required clauses include explicit live-journal and `/tmp`-output prohibitions | `python3 tools/mori-round16-context-check.py --selftest`; observed result is recorded by L1, not predicted | in-script clause patterns; `.ufo/waves/round-16/wave1-spec.json` and `wave1-context-corrected-not-dispatched.json` are committed red/green text snapshots | none live; reads only `--spec`; selftest uses an isolated temporary tree; static text validation is not runtime prevention | mori |
| journal window (r16) | probe | `python3 tools/mori-journal-window.py --anchor <PATH> --scope user\|system [--journalctl PATH] [--timeout SECONDS] [--max-bytes N]` (`--selftest`) | probe, not a gate: rc0 `MORI_JOURNAL_WINDOW_OK` · rc2 `MORI_JOURNAL_WINDOW_UNAVAILABLE reason=<stable>` (capture, parse, cursor-continuity or boot failure) · rc2 `MORI_JOURNAL_WINDOW_SETUP` (invalid anchor or arguments); no severity, no DRIFT, no victim count | `python3 tools/mori-journal-window.py --selftest` — the actual CLI as isolated subprocesses, asserting rc and stable finding id; no network, no live reads; tally measured at L1 integration, not predicted here | none; `--journalctl` overrides the binary path | none: stdout only, the anchor is read and never written; query `--cursor=<anchor> --no-tail --quiet --output=json --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`, never `MESSAGE`, never `--after-cursor` without a proven anchor | mori |
| seat terminal status (r17) | probe | `python3 tools/mori-seat-terminal.py --sessions-dir DIR [--prefix P ...] [--max-tail-bytes N] [--max-files N] [--settle-seconds N] [--now-ms MS]` | 0 no aged error found, not health · 1 `MORI_SEAT_TERMINAL_DEAD` (aged last-error observations, not permanent deaths/incidents) · 2 `MORI_SEAT_TERMINAL_SETUP`; inspect unavailable/incomplete/unsettled totals | `python3 tools/mori-seat-terminal.py --selftest` | none live; schema3 and classification controls in-script | stdout only; selftest isolated fixtures | mori |
| r17 seat regressions | gate | `python3 tools/mori-round17-seat-regressions.py --tool PATH --fixtures .ufo/waves/round-17/fixtures/seat --output DIR` | 0 all match · 1 mismatch/capability_absent · 2 setup/snapshot_tampered/moving inputs | `python3 tools/mori-round17-seat-regressions.py --selftest` (TMPDIR required, not /tmp) | fixture `expected.json` contains independent input pins; actual streams and hashes in run-manifest.json | DIR evidence and isolated per-case copies; never source fixtures | mori |
| r17 jj regressions | gate | `python3 tools/mori-round17-jj-regressions.py --census PATH --output DIR [--scratch DIR] [--keep-scratch]` | 0 all assertions hold · 1 failed assertion · 2 setup; output/scratch guards run before writes | `python3 tools/mori-round17-jj-regressions.py --selftest --scratch DIR` | in-script fixed case/assertion universe; frozen entering census under round-17/frozen | DIR evidence; fresh isolated git/jj sandbox, HOME/XDG_CONFIG_HOME redirected; default cleanup, opt-in forensic retention recorded in manifest; never live lane VCS | mori |
| misroot sweep (r17) | probe | `python3 tools/mori-misroot-sweep.py --fleet-root DIR --lane mori --round N` (`--legacy-pathspec` only reproduces the blind sweep) | 0 `MORI_MISROOT_CLEAN` · 1 `MORI_MISROOT_CANDIDATE` (review lead, not ownership proof) · 2 `MORI_MISROOT_SETUP` | `python3 tools/mori-misroot-sweep.py --selftest` | in-script exact r16 artifact and expected outcomes; retained `round-17/frozen/MoriR16.Lesson` | stdout only; selftest sandbox | mori |
| r17 context check | gate | `python3 tools/mori-round17-context-check.py --spec PATH` | 0 `CONTEXT_OK` · 1 `CONTEXT_MISSING` · 2 `CONTEXT_SETUP`; static text only, no runtime prevention | `python3 tools/mori-round17-context-check.py --selftest` | in-script twelve clauses and mutation controls; committed wave specs | none live; selftest isolated temporary tree | mori |
| r18 retention (C1) | gate | `python3 tools/mori-retention-gate.py scan --repo <repo> --rev <REV> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` (baseline: `--rev d005cdd --expect-population .ufo/waves/round-18/frozen/c1-population.json`, no allowlist); frozen run: `python3 tools/mori-retention-gate.py --frozen-run` (snapshot `.ufo/waves/round-18/gate-snapshots/retention/`) | 0 clean · 1 failed/findings (unallowlisted hits or forbidden allowlist; `allowlist_stale` is warning-only) · 2 could-not-evaluate (`snapshot_tampered` or bad/missing inputs) | `mkdir -p .scratch && TMPDIR=$PWD/.scratch python3 tools/mori-retention-gate.py --selftest` (TMPDIR must be `<repo>/.scratch`) | `.ufo/waves/round-18/frozen/c1-policy.json`; `.ufo/waves/round-18/frozen/c1-population.json`; `.ufo/waves/round-18/frozen/c1-population-cmd.py` (reproduction command) | read-only over the measured repo (git ls-tree/cat-file/rev-list/diff-tree); selftest creates and commits only to throwaway git sandboxes under the caller's `$TMPDIR` (GIT_CONFIG_GLOBAL=/dev/null); JSON stdout, never matched text | mori |
| r18 freeze-order (C2) | gate | `python3 tools/mori-freeze-order.py check --repo <repo> --register .ufo/waves/round-18/frozen/c2-register.json --corrections corpus/evidence/freeze-register.json --tip-for r18-C1=<REV> --tip-for r18-C2=<REV> --tip-for r18-C3=<REV>` (rows with a placeholder tip are could-not-evaluate without `--tip-for`) | 0 clean · 1 failed/findings (remaining overclaim or required oracle disagreement) · 2 could-not-evaluate (bad/missing input or revision) | `python3 tools/mori-freeze-order.py --selftest` | `.ufo/waves/round-18/frozen/c2-register.json`; `corpus/evidence/freeze-register.json` (appended corrections) | read-only over the measured repo (git ls-tree/cat-file/rev-list/diff-tree); selftest creates and commits only to throwaway git sandboxes under the caller's `$TMPDIR` (GIT_CONFIG_GLOBAL=/dev/null); JSON stdout, never matched text | mori |
| r18 dispatch ledger (C3) | gate | `python3 tools/mori-dispatch-ledger.py verify --repo <repo> --rev <REV> --ledger PATH` | 0 clean · 1 failed/findings (unbound/mismatched digest, non-contiguous or out-of-order attempts, invalid started-row placement/count) · 2 could-not-evaluate (bad/missing input or revision) | `python3 tools/mori-dispatch-ledger.py --selftest` | `.ufo/waves/round-18/frozen/c3-ledger-format.json`; measured `.ufo/waves/round-18/wave*-attempts.json` and each row's referenced `<wave>-dispatch.json` | read-only over the measured repo (git ls-tree/cat-file/rev-list/diff-tree); selftest creates and commits only to throwaway git sandboxes under the caller's `$TMPDIR` (GIT_CONFIG_GLOBAL=/dev/null); JSON stdout, never matched text | mori |
| r19 content review (C1) | gate | `python3 tools/mori-content-review.py check --repo <repo> --rev <REV> --population .ufo/waves/round-19/frozen/content-population.json --reviews .ufo/waves/round-19/content-reviews.json --expected-sha256 4a50e77a1f436d349a62100cbac59f4dd337c3f48e63b5a31519d1d2231d581b` | 0 `CONTENT_REVIEW_CLEAN` · 1 incomplete/stale/unresolved review · 2 invalid/unevaluable input; a clean result certifies bounded review coverage, not automatic privacy detection | `TMPDIR=$PWD/.scratch python3 tools/mori-content-review.py --selftest`; actual CLI subprocess arms | `.ufo/waves/round-19/frozen/content-population.json`, `frozen/expected.json`; explicit population digest checked before comparison | stdout only; selftest isolated synthetic Git sandbox below lane-local TMPDIR | mori |
| r19 finite regressions | gate | `TMPDIR=<lane>/.scratch python3 tools/mori-round19-regressions.py --mode after --content-tool <absolute-content-tool> --freeze-tool <absolute-freeze-tool> --expected <lane>/.ufo/waves/round-19/frozen/expected.json --output <absent-output-file>` | 0 all frozen synthetic requirements match · 1 mismatch or capability-absence red · 2 setup, pin or moving-input error; before mode labels absent capability separately from production regressions | Same CLI over isolated synthetic Git fixtures (`--mode after`); before mode is the independent missing-capability/metadata negative control | Expected bytes must equal `5e393d20:.ufo/waves/round-19/frozen/expected.json`; extra binding refinements are separate | Explicit lane-local TMPDIR and output file only; never managed lane VCS | mori |

Round19 freeze receipt entry supersedes the unbound invocation in the r18 row:
`python3 tools/mori-freeze-order.py check --repo <repo> --rev <INPUT_REV>
--register .ufo/waves/round-18/frozen/c2-register.json
--corrections corpus/evidence/freeze-register.json
--tip-for r18-C1=<TIP> --tip-for r18-C2=<TIP> --tip-for r18-C3=<TIP>`.
The explicit input revision must contain byte-identical register/correction
files; dirty, external, uncommitted or missing input is exit2, not clean.
The receipt carries exact loaded-byte hashes, resolved full commits, overrides,
argv and a separate executing-script digest. Legacy invocation without `--rev`
still evaluates labels but is explicitly **unbound**, not committed-input
evidence. The 0/1/2 map and selftest entry remain unchanged. This is mori's own
record calibration, never a fleet admission or orchestration ruling.

Round-17 A2 registry precision: colocated history requires the helper's
`lane.branch` mirror; unresolved jj refs are unavailable, not HEAD fallback.
The committer-author diagnostic runs before young/closed early returns.
Terminal input uses selective schema/status/timestamp/token projection, rejects
failed traversal/root symlink, and opens regular files descriptor-relatively.
Unknown terminal age is unavailable; generic exhaustion and unknown vendor codes
are not guessed rate-limit causes. Selftests that create Git state run from
an isolated verification clone, never the managed lane checkout.

Where mori learns — tiers, study paths, search log: `corpus/SOURCES.md`.

The journal arm needs `jq`, `timeout`, and `wc`; missing parser/timeout is
unavailable, never an unbounded or fake-zero scan. Each serial current-boot
class query (twelve in the r13 bytes) has a labeled-local 2-second bound plus
one-second kill grace (`MORI_JOURNAL_TIMEOUT_S`), not a whole-census deadline.
The r15 positive pass reuses each class capture; it adds no journal query.
Only known class fields and the validated boot identifier leave the parser;
stderr bytes are counted then discarded. `oomd_activity=unmeasured` prevents
interpreting zero notice records as active/healthy oomd. Full store access,
cursor dedup and authenticated emitters are not claimed; the restored
`OOM_KILL_JOURNAL` crit is one global alarm over reported notices or
independently valid positive records, with four separate never-summed raw arms
plus the r15 per-scope positive tokens, and is neither an authenticated nor a
unique-victim kill count. Positive tokens are `unavailable` on capture/parser
failure and are never a total when the class is invalid (see the r15 section
above).

**Regression gates (r14).** `tools/mori-round13-regressions.py` re-measures the
committed round-13 claims from frozen inputs — long-history exact-author
membership (F01), the complete final-roll grammar (F02), the `--baseline`
recorded expected defects and the `--mutation f01|f02|both` transplant
witnesses — into an isolated `--output` evidence tree; it is registered above
as `r13 regressions`, not described as an unregistered evidence harness.
`tools/mori-round14-regressions.py` (registered above as `r14 regressions`) is the
same-census before/after gate for the journal repair: the frozen r13 census
bytes (`.ufo/waves/round-14/frozen/mori-census.sh`, pinned `39abda0a…`) must
go red on actual journal failures (exit 1) while the repaired census goes green,
covering the single global critical `OOM_KILL_JOURNAL` with its four separate
never-summed counters, the user `UNIT_RESULT=signal` and process-exit
`KILL_SIGNAL_JOURNAL` warn paths, fleet/non-fleet/unattributed unit routing,
unchanged scoped-count gains, an empty-zero/CLEAN control, query-error and
missing-metadata `unknown` (never a fake zero), no MESSAGE canary output, no
scope summing, and generic SIGKILL warn preservation. Neither gate replaces the
production census and neither is a universal forgery or audit-closure proof;
L1 measured the delivered r13 gate selftest at 8d22d18 (33 checks, 2 isolated
cases) and r14 gate at 5601d12 (20 checks); receipts are under
`.ufo/waves/round-14/evidence/`. The accepted r14 suite is 43 cases plus one
frozen-red control, 44 assertions passing, not 44 separate domain claims.

An earlier r14 selftest receipt at `8d22d18` exited 1 (`real-gate-red-oom-id`,
`real-gate-red-unit-id`, `real-gate-red-evidence`); it is superseded by the
`5601d12` accepted receipt and is not reported as green.

**Regression gate (r15).** `tools/mori-round15-regressions.py` (registered above
as `r15 regressions`) consumes the fixture packs under
`.ufo/waves/round-15/fixtures/` and checks the narrow salvage from both sides:
a valid current-boot record next to an invalid sibling must keep the OOM crit
or user signal warn and the matching positive token while the raw class token
stays `unavailable:<reason>`; negative and clean controls must stay silent. The
frozen entering census (`0e41cb83…` at `0fa5e0d`, in-script pin) is the red
control: red-relevant cases — those whose expected alarm depends on a class the
case's `invalid_class` makes unavailable — must miss the alarm there, while
every other case passes. A normal run also requires the committed expected
table (`.ufo/waves/round-15/expected.json`); a missing or mismatched table is
could-not-evaluate (exit 2), never a pass. The gate does not parse a malformed
JSON stream and does not claim completeness, authenticated ids or unique
victims; no tally is predicted here, and L1
measures the delivered selftest and gate revisions once after integration.

**Regression gate and probe (r16).** `tools/mori-round16-regressions.py` (registered above
as `r16 regressions`) runs `tools/mori-journal-window.py` against the committed fixture
packs under `.ufo/waves/round-16/fixtures/` through real CLI subprocesses with per-case
`journalctl` wrappers. A normal run requires the expected digest table written by the
pin step; a missing or mismatched table is not a pass. `tools/mori-round16-context-check.py`
(registered above as `r16 context check`) is a static text check of the round context
and runs nothing it names; `CONTEXT_OK` is not runtime prevention. Neither gate
touches the production census. No selftest tally is predicted here; L1 measures the
delivered revisions once after integration.

The positive counters are declared count-magnitude measurements and join the
census's drift volatile list; the existing r10 baseline therefore reports
`volatile_fields` rather than hiding the schema change. No re-pin is performed
or claimed in r15 — the old red pin remains status-neutral debt (L1 decision).

**Drift pin (r10).** `--pin <path>` runs the census (live, read-only) and
writes its full output normalized against a declared VOLATILE FIELD LIST —
volatile values masked to `<V>` (timestamps/ages, gauges, since-boot rates,
counters, `script_sha256`); the list is recorded verbatim in the baseline
header and defined in the script header (`tools/mori-census.sh:145-188`).
The baseline names the census bytes' sha256 and the pin clock, both
informational: behavior, not revision, is compared (two SHAs with the same
normalized output stay `none`). `--drift <path>` re-runs and diffs:
`MORI_DRIFT: none` exit 0, or the changed non-volatile fields/lines named —
`key` (changed value), `-key`/`+key` (removed/added field),
`-FINDING:<id>`/`+FINDING:<id>` (removed/added line; `output-order` for a pure
reorder) — exit 1; a missing, unreadable or
malformed baseline is exit 2, never a verdict. Pinning a DRIFT host is still
a pin (the CLEAN/DRIFT roll never decides the pin's exit code) and `--drift`
writes nothing. Selftest coverage (56 → 66 cases, r10): pin→drift clean,
volatile churn staying clean, an injected one-field regression naming its
field, a removed finding, the missing-baseline exit 2, and the two arity
cases. The lane's own live baseline is `corpus/evidence/baseline-r10-20261015T2231Z.json`
(pinned 2026-10-15T22:26:29Z at census `d7710981…`; it read `MORI_DRIFT: none` at
r10 and reads red from 2026-10-19 — tokens classified in `corpus/lessons/round-12.md`)
with its re-run recipe in the r10 evidence set.

`tools/mori-silence-cases.sh` — behavioral gate over `mori-census.sh`'s
lane-silence grading: one `PASS <id> …` / `FAIL <id>: …` line per case over
hermetic fixtures, tally `MORI_SILENCE_CASES: matched=N total=M`, exit 0 iff
all matched (1 on failures, 2 for setup/usage). **r5 run-order + r6
backchannel contract:** cases execute in a seeded-shuffled order and every
case requires the current run's nonce token `nonce-<N>` in its census output —
a stale or missing token fails the case (`run-nonce missing: the current run's
token is absent (canned/replayed output?)`; failure texts never name the
token). The run header prints `SHUFFLE_SEED=`, `RUN_NONCE=` and
`CASE_ORDER=<id> <id> …` (the order executed) only AFTER the last case — a
census running mid-loop cannot read the seed or order from the oracle's stdout
or process environment (the live nonce stays in the census's own env by
design); the graded `PASS` lines carry `nonce=1` (the two check-style
cases, `shape-invariance` and `readonly-no-mutation`, print bare `PASS <id>`).
Fixture content is per-run: the nonce token and an unprinted run salt are
woven into fixture bodies, commit messages and per-run blob files, so a
content→grade table memorized from an earlier run no longer matches. Pin
`MORI_SHUFFLE_SEED=<int>` / `MORI_RUN_NONCE=<int>` at invocation for a
byte-identical rerun (same seed → same order; both pins are dropped from the
process tree before any case runs); unset, both are random per run, and the
salt is never pinnable or printed.

**Round 13 verdict contract (bounded D01/D02 repair).** Every oracle case,
including shape invariance and read-only mutation checks, requires exactly one
complete final census verdict with the documented tally fields and
`CLEAN`/exit 0 or `DRIFT`/exit 1 agreement. `BANANA`, missing/duplicate records
and opposite roll/rc combinations fail the case — audit F02's demonstrated
prefix-only acceptance. Production exact-author membership consumes captured
history without an early-exiting producer pipe (audit F01). Scope, stated to
prevent over-reading: only audit D01/D02's named long-history membership and
BANANA/final-roll mechanisms are repaired. Arbitrary tally corruption,
aggregate/registry-count vacuity and adaptive output forgery remain outside the
demonstrated repair, so this is neither a full audit closure nor
universal-forgery resistance. The F01 whole-function transplant and the
reconstructed F02 prefix shim are bounded mutation witnesses, not original-byte
restorations; the original frozen before-runs establish the historical failures.
See `corpus/knowledge/verdict-contract-r13.md` and the round-13 regression
receipt.

## Finding → owner routing (two tiers — a deadlock was measured here)

Routing a finding to `tsukuroi` or `kama` for *remediation* deadlocks: both
provinces explicitly refuse to act (`tsukuroi-shokunin/PROVINCE.md:19` "never restarts
services. Detection and report; the operator remediates."; `kama-shokunin/PROVINCE.md:45-47` "kama never writes
to `~/.config`, `~/.omp`, or systemd units ... the operator repoints them"). mori
never remediates either. So a finding carries **two** owners:

| Tier | Role | Who | Acts how |
|---|---|---|---|
| 1 — triage/diagnosis | read-only domain specialist | `tsukuroi` (OS substrate, units, drivers) · `kama` (loopback model ports, baseURL drift) · `kumitate` (wave settlement, dispatcher queue, watchdog state) · `mori` (census hygiene, fixtures) | re-probes with its own tool and produces a diagnosis |
| 2 — actuation | authorized actor | `kumitate` for **automated orchestration** actions (`ufo-swarm-wave.mjs`, `fleet-dispatcher.mjs repend`, `ufo-sighting complete`) · **operator** for **host** mutations (service restarts, pacman, cgroup limits, mounts, deletions) | performs the change |

**Never collapse all findings onto `operator`** — that drowns the human in raw
kernel stacks and counter deltas with no domain triage. mori's payload must carry
enough typed context (`pid`, `comm`, `cgroup`, `mount`, `use_pct`, `wave_dir`,
`schema`, `newest_file_age_s`) that Tier 1 can diagnose without re-probing.

**Journal routing payload (r14).** `UNIT_FAILURE_OUT_OF_SCOPE` is the Tier-1
pointer for a non-fleet unit failure: `severity=info`, `owner=tsukuroi`, and a
validated count — never echoed unit text and never a Tier-2 instruction. A
record whose subject metadata is absent, malformed or ambiguous is
`UNIT_FAILURE_UNATTRIBUTED_JOURNAL severity=info owner=unresolved
reason=subject-metadata-unknown`: neither fleet nor routed to tsukuroi until a
diagnosis exists (both subject fields present is unknown even when identical).
The restored `OOM_KILL_JOURNAL` crit row is the operator-visible alarm, not a
remediation order.

**Premature-settlement guard:** an `WAVE_UNSETTLED_AGE` finding must never trigger
an automated settle while lanes are still writing; require
`newest_file_age_s` past a conservative stall threshold first.

## Secret-exposure exclusions (measured by a sentinel audit)

The census is count-only over the journal and shape-only over host paths. Two forms
were ruled out and must stay out:

- **Never print journal `MESSAGE` content.** This boot's user journal carries 221
  `1password` lines and 2 `gnome-keyring-daemon` lines with opaque runs; the probe
  counts them and never echoes the text. Never run the gate under `set -x`, and
  never capture journal output into a variable that is later echoed.
- **Never read a cgroup counter outside `/sys/fs/cgroup/`.** `read_file` echoes the
  first line into the surface row, so an operator-pointed `MORI_CGROUP_CURRENT`
  would print another file's first line; the probe refuses out-of-tree paths
  shape-only (`refused:outside-sysfs-cgroup`). r7's PSI/limit readers and r8's
  `memory.peak` reader reach the same no-echo outcome by shape: only validated
  tokens (`is_decimal` avg10, `is_int` bytes, the literal `max`) can enter a row
  (`mem_peak_source=shape-refused` otherwise).

Also excluded: `ps e` / `/proc/<pid>/environ` (`omp` carries
`HL_INITIAL_WORKSPACE_TOKEN`), `cat /proc/<pid>/fd/*` (`omp` holds 51 readable fds
onto session JSONL), and any journal output mode that keeps `MESSAGE`.

The window probe follows the same rule: its query field list excludes `MESSAGE`, and its stdout never echoes a raw cursor or record text.

## Disk thresholds are a PROPOSAL, not a measurement

`DISK_WARN_PCT=85` / `DISK_CRIT_PCT=95` carry **no write-rate evidence** and are
labeled as such. (**r7/r8 update — `census-r4` → `census-r5`:** the census
measures a write rate, but only the **average since boot** —
`io_basis=since-boot`, `io_avg_since_boot=<dev>:<Bps>/<uptime>s`, sectors
written × 512 ÷ uptime from `/proc/diskstats`, no sampling interval added to
runtime. The instantaneous two-sample rate stays a deferral, and r8 paid its
named precondition — the 0.2 s-window variant measured ≈208–222 ms across three
independent 15–30× isolations (minimum 208 ms) over the two-read floor against a
50 ms budget; the dwell is the cost, the reads alone 16 ms median — so it stays
out of census runtime on measured grounds, not an estimate. The average is not a
licence to recalibrate 85/95.) Falsification results worth keeping:

- The fleet's *actually reported* disk failures are **quota** events (`EDQUOT`,
  "disk-quota pressure") — a capacity-percent probe cannot see them, and the quota
  numbers are unreadable on this host.
- **Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%**
  while `df -P` Capacity on the same device reads **10%**; a probe that used the
  chunk percent would fire `DISK_LOW` against every proposed default today. Keep
  the `df -P` parser.
- **Never OR a byte floor against `df -P`'s Available column** — it is in
  1024-blocks, so a bytes-denominated floor false-fires on a 10%-full filesystem.
- One pair only. A sibling note proposing 90 and another proposing 80 must not be
  described as the default beside 85/95, or a later diff cannot say which proposal
  was tested.
- The since-boot average counts **every** write to the device since boot (OS and
  desktop included) and smooths bursts; it is not attributable to the fleet and
  is not a distribution to threshold against.

## Lane-silence grading is launch-aware and authorship-aware (r2 contract)

**Revision marker r2 — round 3, 2026-10-15.** This section replaces the round-1
rolling-window description. The binding decision table (lifecycle rows, exact
identity policy, named preconditions) is `corpus/knowledge/silence-grading-r2.md`;
it implements `PROTOCOL.md:153-168`.

`probe_silence` grades each roster lane against the launch epoch of its current
round, read from `.ufo/watchdog.log` (never log mtime, never the `tick=` counter),
and emits a per-lane row `SURFACE lane.<id>: <state> (lane=<id> round=<N>
launch_epoch=<e> age_s=<s> basis=<row> …; ts=…)` with state in {`silent`,
`progressing`, `progressing-weak`, `young`, `not-open`, `unavailable`}; the
aggregate `SURFACE silence:` row keeps the per-state counters (`silent=` /
`progressing=` / `progressing_weak=` / `young=` / `not_open=` / `unavailable=` /
`skipped=`).

- **Only a still-open mission is graded — closed reads `not-open`.** A
  `complete`/`wrap` line for the same lane+round closes it, as does a committed
  report at HEAD whose newest path commit has `launch_epoch < ct ≤ now`; a later
  same-round `launch` reopens it and a state-round advance hands the grade to the
  new round. No matching launch line → `not-open`; unreadable ledger/repo/git
  input → `unavailable` — a missing surface is never unhealthy.
- **Strict age gate.** Only `now − launch_epoch > LANE_SILENCE_S` (default 7200)
  is gradeable-old; age at or below the gate, or a future launch → `young`.
- **Authorship decides open-and-old, matching both identity fields exactly** —
  `<lane>-shokunin <lane>@shokunin.local`, never substring, never `%cn`/`%ce` —
  over ALL post-launch commits: a lane-authored commit → `progressing`; no subject
  commits but unexplained untracked/dirty recent files in the lane's own scope →
  `progressing` (attribution inference disclosed); sibling-only activity with a
  clean checkout → `progressing-weak`; nothing attributed → `silent`.
- **`FINDING LANE_SILENT severity=warn` fires only for the row-D clean-old-silent
  case**, carrying lane/round/launch_epoch/age_s — replacing the r1
  `head_epoch=`/`newest_epoch=` pair. `unavailable`/`not-open`/`young` emit no
  finding and no DRIFT.

The two measured r1 divergences this contract closes: the aggregator was
over-credited `progressing` by sibling commits plus a gitignored `game-dev-3d`
`watch.log`; kasegi was graded while its round had wrapped
(`.ufo/watchdog.log:287`; `LOG.md:73-80`).

Cutover receipt: `census-r2` landed in `tools/mori-census.sh` — sha256
`fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9` — round
receipts `corpus/evidence/cutover-r3-*.log`.

## Wave settlement scan and drift re-pin (r20)

Detection only. The settlement scan is read-only; the re-pin is an L1 ritual. Neither starts, steers, retries or settles a seat.

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| When to run the settlement scan | `python3 tools/mori-wave-settlement.py scan --lane-root <lane> [--fleet-root <fleet>] [--out FILE]` (the `--out` parent must exist), before any closure note that says a wave settled; select your wave in `waves[]` by `dispatch_path`, because the exit code is lane-wide | treating a lane-wide exit as one wave's verdict; copying or moving reports to flip a member to `present` | per-wave `state`, per-member counts, sorted not-present names; `mori-wave-settlement-v1` JSON, byte-identical on re-run of an unchanged tree; commit it with the scan time as the settlement receipt (`corpus/QUALITY.md` 64) — the JSON itself has no timestamp |
| `settled` | every member `present` (regular, non-symlink, size > 0); exit 0 | reading it as "the work is correct" (it counts non-empty files only) | `missing=0` |
| `no-spawn` | dispatch with `taskCall: null`; exit 0 | treating it as an unsettled wave | `members=0` |
| `partial` | at least one `present`, at least one not; exit 1 | calling the missing seats dead, failed or killed; auto-re-dispatching | list `missing`; any re-dispatch decision belongs to kumitate |
| `unsettled` | zero `present`, at least one member; exit 1 | inferring a crash, or even a dispatch, from zero reports | re-scan later; check the lane's spawn/refusal records before calling it dispatched |
| `unavailable` | no member had a parseable, safe report path; exit 1 | reading an unsafe path, following a symlink, or reporting zero | `unsafe` / `unparsed` counts |
| `stub` | whole content is the seat start marker `STATUS: started` (≤16 bytes read, never emitted) | counting a marker as a delivered report | counts as not present (`corpus/QUALITY.md` 66) |
| `empty` / `misrooted` | `empty` = size 0; `misrooted` = report exists only under `--fleet-root` at the same relative path | counting either as `present` | both count as not present; fix routing, not counts |
| `unsafe` / `unparsed` | `unsafe` = absolute, `..`, escapes the lane root, or crosses a symlinked parent; `unparsed` = no trailer line | reading an `unsafe` target | counts only |

Exit map: 0 all discovered waves `settled` or `no-spawn`; 1 any other state (or an uncaught crash, e.g. a pathologically deep tree, which prints a traceback); 2 usage error, unreadable lane root or a `--fleet-root` that is not a directory. Exit 1 means *not settled*. **Exit 0 with `totals.waves` = 0 proves nothing** (missing or symlinked `.ufo/waves`, JSON-only discovery); exit 0 can also coexist with `unreadable_json > 0`: always read both. A dispatch file is not dispatch evidence (`name_hint`, `duplicate_of` are shape only). Knowledge: `corpus/knowledge/wave-settlement-r20.md`.

**Never conclude dead, failed or killed.** The tool's own keys and state words never use those words (oracle `no_vocab`); member names are echoed as dispatched and may contain them. A missing report only means no regular non-empty file sat at the trailer path at scan time. Closure evidence is the watchdog `complete`/`wrap` line or a committed report (silence grading, r2); this probe is neither.

**Round21 correction superseding the r20 re-pin ritual.** The round20 outside
closure rejected C1: deleted aggregator wave markers were unresolved evidence
loss, not nonblocking `live-state`. QUALITY69 supersedes67. The r10 baseline
stays authoritative historical comparison input; the r20 baseline stays
byte-unchanged for provenance but is **invalid for acceptance**. Historical
post-pin `none` proves only sameness in that window.

1. Preserve each disappeared required observation's identity and baseline,
   deletion and preservation provenance. `aggregator-r10` and
   `aggregator-r10-resume` remain unknown, never declared settled or dead.
2. Before considering any new pin, apply QUALITY69: missing required evidence
   without independently evidenced per-identity disposition is
   `census-regression`, a pin blocker even with unchanged census code.
3. A removal-actor's posthoc receipt and a `blind_spot` annotation do not
   satisfy independent accounting. New `w24` aging is separate live-state;
   it cannot offset either lost old identity.
4. No re-pin runs in round21. A later steward must resolve the blocker before
   any pin, classify every remaining drift token with semantic evidence,
   reject census-regressions, and report the stability window honestly.
   Never use key coverage alone as semantic classification (carried Q65).

Ground: `corpus/lessons/round-21.md`; retained provenance
`.ufo/waves/round-21/evidence/historical-provenance.json`; active QUALITY69.

Never edit `tools/mori-census.sh`. `--pin` writes only its path; `--drift` writes nothing.

## Round21 retained-loss observation and policy-test registry

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| retained-loss audit | probe (negative baseline-acceptance evidence, not independent-disposition authority) | `python3 tools/mori-evidence-loss.py audit --root . --required .ufo/waves/round-21/frozen/required.json --accounting corpus/evidence/loss-accounting-r21.json` | 1 blocked/failed acceptance (omission, invalidity, unknown or external-review-required); 2 could-not-evaluate input/setup; audit never emits0 because outside acceptance is not an input or capability of this probe | `TMPDIR=$PWD/.scratch python3 tools/mori-evidence-loss.py --selftest`; exact rc/finding IDs and isolated committed Git fixtures | required pair and original r10 baseline references in round21 frozen/required.json; each copy's full revision/SHA is checked against Git | none live; selftest isolated temporary root only | mori |
| evidence-loss rule comparison | gate (finite synthetic policy tests) | `python3 tools/mori-evidence-loss.py classify --rule .ufo/waves/round-21/frozen/after-rule.json --cases .ufo/waves/round-21/frozen/cases.json` | 0 all synthetic expectations match; 1 mismatch; 2 malformed/setup; **not** actual baseline authorization | same `--selftest`, including citation-free false-rule negative control | six cases and old/new rule objects frozen at3b792db; independent oracle binds actual inputs/code to measured commit | none live; selftest temp tree | mori |

The audit retains numeric counters and separate identity lists. Valid unresolved
rows are not invalid; their expected real outcome is omitted0, unresolved2,
invalid0, pin_allowed=false, exit1. A structurally valid disposed declaration
is still external-review-required and cannot authenticate its author or clear
the pin. The classifier's positive cases are conditional synthetic logic only.
This is a mandatory acceptance observation plus outside-review requirement,
not interception of the existing raw `mori-census.sh --pin` write path.
Bypassing the blocker violates QUALITY69; this round runs no pin.
Trust refinement: `.ufo/waves/round-21/trust-refinement.md`.

## Round22 retention receipt reconciliation (accounting agreement only)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| retention receipt reconciliation | gate (accounting agreement, not privacy clearance) | `python3 tools/mori-retention-reconcile.py check --repo . --rev INPUT_COMMIT --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` | 0 RETENTION_RECONCILED even when retention is red; 1 RETENTION_RECONCILIATION_MISMATCH; 2 RETENTION_RECONCILIATION_SETUP | `TMPDIR=$PWD/.scratch python3 tools/mori-retention-reconcile.py --selftest`; actual isolated CLI, exit/finding assertions | `.ufo/waves/round-22/frozen/requirements-v2.json`, corrected fixture-builder-v2.py and independent oracle-reconcile-v2.py; original freeze retained with denominator-correction.md | none live; stdout only; selftest isolated fixtures | mori |

Read the three inputs from the exact committed input revision; the recorded
measurement revision, command --rev and inner commit must agree. Recount
the measured tree independently, requiring unchanged policy/allowlist bytes.
Report raw population and excluded identities separately: `policy_excluded`
means the frozen policy's non-author globs, never exclusion of its own source
file. The retained r21 split is95raw/5non-author/90scanner, with4unallowlisted.
The exact source policy and its nested copy remain scanned normally.

`privacy_clearance` is always false. An agreement result cannot replace the
active r18 retention gate, authorize a pin, settle/reap a wave or establish
that the old receipt's working-tree inputs were authentic. Original permission
control11/12 remains red; both historical dispositions remain unknown and
baseline acceptance blocked. No earlier registry row is superseded.
Ground: `corpus/knowledge/retention-reconciliation-r22.md`, S064 at its
commit-resolution-only scope; `corpus/lessons/round-22.md`.

Field caveats (wave2 FinalR02/NoHarm): `raw_unallowlisted` and
`scanner_unallowlisted` are one existing gate metric reported twice (both
exclude non-author hits); `policy_excluded` equals `non_author` by design.
Membership evidence is the identity lists, not these aliases. Setup reasons are
distinct tokens: `receipt_revision` (unresolvable/non-commit measured
revision), `measured_not_ancestor`, `policy_changed`/`allowlist_changed`,
`receipt_path_binding`, `input_not_regular`, `unsafe_input_path`, `usage`
(including `-h`, which never exits 0). Output digests are unsalted provenance,
not secrecy; argv echoes caller paths, so pass only lane-relative inputs.
