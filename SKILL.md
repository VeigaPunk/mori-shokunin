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
| silence oracle | gate | `bash tools/mori-silence-cases.sh` | 0 clean (all matched) · 1 failed · 2 could-not-evaluate | `bash tools/mori-silence-cases.sh --selftest` → `MORI_SILENCE_CASES_SELFTEST pass=24 fail=0` (round 45; the flag is consumed before the census-path positional, and the entropy re-exec carries it) | case table in-script | temp fixtures | mori |
| r13 regressions | gate | `python3 tools/mori-round13-regressions.py --output <dir>` (`--census`/`--oracle` default to the repo `tools/*.sh`; `--frozen-dir` default `.ufo/waves/round-13/frozen`) | 0 clean · 1 failed (claim mismatch) · 2 could-not-evaluate (usage/setup, unreadable target, `snapshot_tampered`, unbuildable requested mutation) | `python3 tools/mori-round13-regressions.py --selftest` — parser checks plus isolated real-gate subprocess cases asserting exit and stable finding ids; measured tally in round-14 evidence | in-script `FROZEN_PINS` and `FROZEN_BASE_COMMIT` independently pin the default frozen census/oracle/manifest; custom frozen directories are manifest-only and explicitly unpinned; expected claim ids/values are in-script; evidence names revision and dirty flag | `<dir>` evidence tree only; fixtures removed unless `--keep-fixtures` | mori |
| r14 regressions | gate | `python3 tools/mori-round14-regressions.py --output <dir>` (`--census` default `tools/mori-census.sh`; `--frozen` red control default `.ufo/waves/round-14/frozen/mori-census.sh`) | 0 clean · 1 failed (claim failed, or the frozen control did not reproduce the defect) · 2 could-not-evaluate (usage/setup/pin, `snapshot_tampered`, unexpected internal error) | `python3 tools/mori-round14-regressions.py --selftest` — 20 checks including real-gate red rc1 and tamper rc2 at 5601d12; the harness blob accepted at round 14 (git `5601d12`, sha256 prefix c39e5a73, since changed) is no longer the file on disk — the current `tools/mori-round14-regressions.py` is sha256 `533218a566030fda…` (re-pinned round 48 after the v3 pin check found the old truncated digest matched no file, `.ufo/waves/round-48/w1/ExecRealRegistryAudit.md`); `evidence/r14-selftest-accepted.json` under round-14 waves | in-script `PINNED_SHA256` for `.ufo/waves/round-14/frozen/mori-census.sh` (`39abda0a…`, the r13 delivered bytes) + expected claim ids/values | `<dir>` evidence tree only; fixtures removed unless `--keep-fixtures` | mori |
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
| r19 finite regressions | gate | `TMPDIR=<lane>/.scratch python3 tools/mori-round19-regressions.py --mode after --content-tool <absolute-content-tool> --freeze-tool <absolute-freeze-tool> --expected <lane>/.ufo/waves/round-19/frozen/expected.json --output <absent-output-file>` | 0 all frozen synthetic requirements match · 1 mismatch or capability-absence red · 2 setup, pin or moving-input error; before mode labels absent capability separately from production regressions | `python3 tools/mori-round19-regressions.py --selftest` → `R19_SELFTEST pass=26 fail=0`, added round 45; it builds the same C1/C2 fixtures as `--mode after` under `$TMPDIR` and asserts 26 predicates over them | Expected bytes must equal `5e393d20:.ufo/waves/round-19/frozen/expected.json`; extra binding refinements are separate | Explicit lane-local TMPDIR and output file only; never managed lane VCS | mori |
| r44 figure ledger (C1) | gate | `python3 .ufo/waves/round-44/count-c1.py <rev>` (`--ledger PATH`, `--repo PATH`, `--min-rows N`, `--min-classes N`, `--selftest`) | 0 `C1=met mismatches=0` · 1 `C1=unmet` (a row's recomputed value differs from its asserted value, or a row/class floor fails) · 2 `C1_SETUP` (usage, unresolvable revision, git timeout); a ledger whose rows are not single `git` pipelines naming `@REV@` is rejected, never scored | `python3 .ufo/waves/round-44/count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0` over isolated throwaway git repos: honest ledger, off-by-one row, junk producer, below-floor ledger, absent ledger, compound command | ledger bytes at the measured revision (default `.ufo/waves/round-44/figures.tsv`); witness fixture `.ufo/waves/round-44/fixtures/figures-r43.tsv`; mutant `.ufo/waves/round-44/fixtures/mutants/count-c1.py` | stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR | mori |
| r44 gate registry (C2) | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | 0 `REGISTRY=met` · 1 `REGISTRY=unmet` (unregistered path, a missing standard cell, an entry path that does not resolve at the revision, or no `--selftest` mode in the tool) · 2 `REGISTRY_SETUP` (usage, unresolvable revision, absent registry or gate table) | `python3 tools/mori-gate-registry.py --selftest` → measured `GATE_REGISTRY_SELFTEST pass=15 fail=0` at sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` (743 lines); v2 covers second-table registration, duplicate names, comment-only selftest, population mode and escape flags | in-script fixture registry rows; the audited surface is this SKILL.md `## Gates` table at `--rev` | stdout only; reads registry and audited paths at `--rev`; selftest fixtures use an isolated temporary tree | mori |
| r44 gate conformance (C2) | gate | `python3 .ufo/waves/round-44/count-c2.py <rev> --counter PATH [--counter PATH ...]` (`--mutants-dir PATH`, `--min-arms N`, `--selftest`) | 0 `C2=met` · 1 `C2=unmet` (absent counter, unregistered or thin row, no selftest tally, or a mutant its own selftest cannot catch) · 2 `C2_SETUP` (usage, unresolvable revision, git timeout) | `python3 .ufo/waves/round-44/count-c2.py --selftest` → `C2_SELFTEST pass=5 fail=0`: conformant counter, absent counter, unregistered counter, counter without `--selftest`, surviving mutant | `fixtures/mutants/<basename>` beside each counter; `MORI_GATE_REGISTRY` plumbs the auditor into fixture copies | stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written | mori |
| r44 corpus coverage (C3) | gate | `python3 .ufo/waves/round-44/count-c3.py <rev> --entry PATH --row S### [--row S### ...]` (`--coverage-map`, `--census PATH`, `--readme PATH`, `--selftest`) | 0 `C3=met` · 1 `C3=unmet` (entry absent or missing `verified-at`/`recheck`/`coverage-map`, a declared row absent or not `mined` or not naming the entry in `used-by`, a red census, or no README map row) · 2 `C3_SETUP` (usage, unresolvable revision, git timeout) | `python3 .ufo/waves/round-44/count-c3.py --selftest` → `C3_SELFTEST pass=6 fail=0`: registered entry, absent entry, row without `used-by`, red census, README without a row, missing coverage-map | `--census` default `<repo>/../scripts/sources-census.sh`; mutant `.ufo/waves/round-44/fixtures/mutants/count-c3.py` | stdout only; the registry copy handed to the census is materialized under the caller TMPDIR | mori |
| disk write rate (r34) | probe | `python3 tools/mori-disk-rate.py --interval-ms N` (live: read, wait N ms, read again; `--a FILE --b FILE` for two saved samples; `--sysfs DIR` default `/sys`) | 0 → one JSON report on stdout (`interval_ms`, `devices`, `host_basis`, `host_write_Bps`), every state other than `ok` carrying `write_Bps` null and never zero · 1 → a requested sample cannot be read (`mori-disk-rate.py: cannot read the sample(s) given`) · 2 → usage (`--interval-ms` not positive, or `--a` and `--b` given singly); the docstring's stdout sentence names only 0 and 2, so both the sample rc 1 and the selftest rc 1 are undeclared there — round-46 finding | `python3 tools/mori-disk-rate.py --selftest` → measured `MORI_DISK_RATE_SELFTEST pass=14 fail=0` rc 0, added round 45: it runs against synthetic samples and a synthetic sysfs root under the caller TMPDIR (no live `/proc` or `/sys` read) and exits 1 on a failing arm, 2 when the fixtures cannot be built; while it did not exist, the able-to-fail evidence was the offline pair (rc 0, sda state ok at 2048000 B/s), the unreadable sample (rc 1) and the two usage arms (rc 2) quoted in `.ufo/waves/round-45/w1/ScribeRegistryRows.md` | `SECTOR_BYTES = 512`; `VALID_TOKEN_COUNTS = (14, 18, 20)`; sectors-written is token 10 (`SECTORS_WRITTEN_INDEX = 9`); class and state order R1–R7 of `.ufo/waves/round-34/contract.md` §C1; sources S180–S198 | writes nothing: it creates no file, and `/proc/diskstats` (or the `--a` and `--b` files) plus `<sysfs>/class/block` are read only | mori |
| wave settlement (r20) | gate | `python3 tools/mori-wave-settlement.py scan --lane-root DIR [--fleet-root DIR] [--out PATH]`; `python3 tools/mori-wave-settlement.py --selftest` (accepted only as the sole argument, and absent from `--help`, whose only subcommand is `scan`) | 0 → every scanned wave is `settled` or `no-spawn` · 1 → any wave is `partial`, `unsettled` or `unavailable` (missing, empty, stub, unsafe or misrooted members) · 2 → the lane root is unreadable or not a directory, the fleet root is not a directory, or `--out` cannot be written; `ignored_json` and `unreadable_json` are counted and never flip the verdict | `python3 tools/mori-wave-settlement.py --selftest` → measured `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)` rc 0 = the 14 frozen cases in `.ufo/waves/round-20/frozen/c2-expected.json` plus the 9 in-script `REFINEMENT_CASES` (R1–R5, r6 missing taskCall, r7 `..` component, r8 symlinked parent), each case built under `tempfile.TemporaryDirectory(dir=$TMPDIR)` | `.ufo/waves/round-20/frozen/c2-expected.json` (the frozen 14, never edited); schema `mori-wave-settlement-v1` and dispatch `ufo-swarm-wave-dispatch-v1`; trailer regex `^Report: write your scoped findings to (\S+)$`; `STATUS_NAMES` = present, empty, stub, missing, misrooted, unsafe, unparsed | stdout is one JSON object; `--out PATH` writes exactly that file, creating its parent directories, and no other repo path is written; the selftest writes only under the caller TMPDIR; a `..` component or a symlinked parent on a report path is `unsafe` and never followed | mori |
| r41 calibration | probe (one dated self-assessment measurement, not a standing gate) | `python3 tools/mori-round41-calibration.py <revision> --repo DIR --reference-rev REV` (both options required; the reference gate is loaded byte-for-byte from `REV` and executed there) | 0 → `MORI_R41_CALIBRATION mismatches=0` with one `recorded_…/observed_…` line per record · 1 → `mismatches>0`: measured `mismatches=6 observed_as_of=37 extension_rows=19` at `554ff416` because the round-40 records moved after that round, so rc 1 reports the value of a dated reading, not a standing verdict · 2 → `MORI_R41_CALIBRATION_SETUP: <reason>` on stderr (git failure or timeout, reference-gate exit outside 0/1, missing summary or timing line, unparsable record) | `python3 tools/mori-round41-calibration.py --selftest` → measured `MORI_R41_CALIBRATION_SELFTEST pass=10 fail=0` rc 0, added round 45: it builds a synthetic git repository and synthetic record files under the caller TMPDIR and checks the old-record, correction-line and setup paths; while it did not exist, the able-to-fail evidence was the rc-1 run at `554ff416` and the four setup paths read in `main`, quoted in `.ufo/waves/round-45/w1/ScribeRegistryRows.md` | `GATE_PATH = tools/mori-sources-appendonly.py` read at `--reference-rev`; `RECORD_PATHS` = `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-40.md`; `CORRECTION_RE`, `SUMMARY_RE`, `TIMING_RE`; git timeout 120 s, reference-gate timeout 180 s | stdout only; it writes its reference-gate copy into a `mori-r41-gate-` `tempfile.TemporaryDirectory` under the caller TMPDIR and executes that committed program with the caller's privileges; the gate reads `--repo` and writes nothing outside its own selftest fixtures | mori |
| r45 ledger counter (C1) | gate | `python3 .ufo/waves/round-45/count-c1.py <rev>` (`--repo PATH`, `--ledger PATH` default `.ufo/waves/round-45/figures.tsv`, `--other-rev REV`, `--witness-dir DIR`, `--min-rows N`, `--min-classes N`, `--timeout S`, `--selftest`) | 0 → `C1=met mismatches=0` · 1 → `C1=unmet` (a rejected row grammar, a duplicate id or command, a HEAD-reading or revision-constant row, a value that does not recompute, a floor below 12 rows or 4 classes, or an accepted witness; `failed=` names the checks) · 2 → `C1_SETUP` (usage, `WORK`, unresolvable revision, git timeout); the floors clamp UP and the verdict line prints floors, revision, repo, other revision and `witnesses=<rejected>/<total>` | `python3 .ufo/waves/round-45/count-c1.py --selftest` → measured `C1_SELFTEST pass=16 fail=0` rc 0 at sha256 `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c1.py` disables duplicate-id detection (`if key in cmds:` to `if False:`) and its own run reads `C1_SELFTEST pass=15 fail=1` rc 1 | `.ufo/waves/round-45/figures.tsv` at the measured revision; `.ufo/waves/round-45/fixtures/witnesses/w-revconst.tsv`, `w-head.tsv`, `w-dup.tsv`; floors 12 rows and 4 classes; `GIT_VERBS` = show, grep, ls-tree, rev-list, cat-file, log | stdout only; the selftest writes only under a `c1st-` `tempfile.mkdtemp` in the caller TMPDIR, and child git runs with `GIT_*` scrubbed, `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`; there is no `bash -c` anywhere | mori |
| r45 gate conformance (C2) | gate | `python3 .ufo/waves/round-45/count-c2.py <rev>` (`--rev REV` is the alternate spelling and only one of the two may be given; `--repo PATH`, `--auditor PATH`, `--write-scope PATH` default `.ufo/waves/round-45/fixtures/write-scope.json`, `--mutants-dir DIR` default `.ufo/waves/round-45/fixtures/mutants`, `--timeout S`, `--selftest`) | 0 → `C2=met` with `tables= registered= unregistered= no_selftest= duplicate= wrong_row= writescope_mismatch= auditor_selftest=pass=/fail= mutant= rev= repo=` · 1 → `C2=unmet`, where `checks_failed=` names the failing checks (an absent or non-v2 auditor, a red auditor selftest, an unregistered or thin row, a duplicate, a surviving mutant, a write-scope mismatch) · 2 → `C2_SETUP` (usage or both revision spellings, not a git checkout, unresolvable revision, timeout) | `python3 .ufo/waves/round-45/count-c2.py --selftest` → measured `C2_SELFTEST pass=14 fail=0` rc 0 at sha256 `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93` (14 arms); the mutant `.ufo/waves/round-45/fixtures/mutants/count-c2.py` (sha256 `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703`) is a one-check byte-diff that disables the write-scope arm and its own selftest catches it | `AUDITOR_REL = tools/mori-gate-registry.py` (v2, sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, 743 lines); `WRITESCOPE_REL` and `MUTANTS_REL` above; `COUNTER_KEYS` = tables, registered, unregistered, no_selftest, duplicate, wrong_row plus writescope_mismatch; the write-scope fixture's `TRUE`/`FALSE`/`UNEXERCISED`/`UNAVAILABLE` map and its sorted-`sha256sum` tree digest | stdout only; it extracts its own copy with `git archive` into a `c2st-` `tempfile.mkdtemp` under the caller TMPDIR and runs the audited counters, the auditor and the write-scope arm from there; those children run with the caller's privileges, so their writes are bounded by what each child is told, not by this counter | mori |
| r45 corpus coverage (C3) | gate | `python3 .ufo/waves/round-45/count-c3.py <rev> --entry PATH --row S###` (`--entry`, `--row` and `--coverage-map` are each repeatable; `--root` defaults to the parent directory of `--repo`; `--census PATH` defaults to `<root>/scripts/sources-census.sh`; `--readme`, `--repo`, `--timeout S`, `--selftest`) | 0 → `C3=met rev=… entries=N rows=… census_sha256=…` · 1 → `C3=unmet` (an entry absent or missing `source:`/`verified-at:`/`recheck:`/`coverage-map:`, a declared row absent, not `mined`, or not naming the entry in `used-by`, a token collision such as S473 against S4731 or FR5 against FR12, a red census, or no README map row) · 2 → `C3_SETUP` (usage, a missing `--entry` or `--row`, unresolvable revision, census timeout) | `python3 .ufo/waves/round-45/count-c3.py --selftest` → measured `C3_SELFTEST pass=19 fail=0` rc 0 at sha256 `37fd7c24ff52…`; the mutant `.ufo/waves/round-45/fixtures/mutants/count-c3.py` (sha256 `69bf9b6eb29b…`) disables the census exit check (`proc.returncode == 0` to `True`) and its own run reads `C3_SELFTEST pass=17 fail=2` rc 1 | `--census` default `<root>/scripts/sources-census.sh`, whose sha256 the verdict line prints; the `corpus/README.md` map section; the declared entries and rows; lane `mori` | stdout only; fixtures are written under a `c3st-` `tempfile.mkdtemp` in the caller TMPDIR; the census arm executes `bash <root>/scripts/sources-census.sh validate --root <root> mori` with the caller's privileges, so that caller-named program is not sandboxed | mori |
| r44 figure ledger (C1) — write scope superseded | gate | `python3 .ufo/waves/round-44/count-c1.py <rev>` (`--ledger PATH`, `--repo PATH`, `--min-rows N`, `--min-classes N`, `--selftest`) | unchanged from row `r44 figure ledger (C1)` (SKILL.md:183), which remains the verdict-map authority for this instrument; this row supersedes that row's write-scope cell only | unchanged from row `r44 figure ledger (C1)`: `python3 .ufo/waves/round-44/count-c1.py --selftest` → measured `C1_SELFTEST pass=6 fail=0` rc 0 (re-run 2026-10-25) | unchanged from row `r44 figure ledger (C1)` (SKILL.md:183) | superseded: the cell at SKILL.md:183 reads "stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR", and that is false as written — the counter executes every ledger row through `bash -c` (`.ufo/waves/round-44/count-c1.py:113-114`) with the caller's cwd and environment, so a committed row writes anywhere the caller can; the round-45 arm's `TRUE` (`evidence/write-scope.txt:82`) covers only its `--selftest` run and not that production path. Superseded on the round-44 sentinel's F8 reading (`.ufo/waves/round-44/w1/SentTools.md` §F8), not re-measured by this row | mori |
| r44 gate registry (C2) — write scope superseded | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <repo-relative path> [--audit ...]` (`--registry PATH`, `--repo PATH`, `--selftest`) | unchanged from row `r44 gate registry (C2)` (SKILL.md:184), which remains the verdict-map authority; this row supersedes that row's write-scope cell only | `python3 tools/mori-gate-registry.py --selftest` → measured `GATE_REGISTRY_SELFTEST pass=15 fail=0` at sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`, 743 lines (re-run 2026-10-25) | unchanged from row `r44 gate registry (C2)` (SKILL.md:184) | superseded: the cell at SKILL.md:184 falsely described v1's write behavior under inherited GIT_DIR; v2 scrubs GIT_* in child_env; current source is the 743-line v2 auditor above | mori |
| r44 gate conformance (C2) — write scope superseded | gate | `python3 .ufo/waves/round-44/count-c2.py <rev> --counter PATH [--counter PATH ...]` (`--mutants-dir PATH`, `--min-arms N`, `--selftest`) | unchanged from row `r44 gate conformance (C2)` (SKILL.md:185), which remains the verdict-map authority; this row supersedes that row's write-scope cell only | unchanged from row `r44 gate conformance (C2)`: `python3 .ufo/waves/round-44/count-c2.py --selftest` → measured `C2_SELFTEST pass=5 fail=0` rc 0 (re-run 2026-10-25) | unchanged from row `r44 gate conformance (C2)` (SKILL.md:185) | superseded: the cell at SKILL.md:185 reads "stdout only; counter bytes materialize under the caller TMPDIR; nothing in the repo is written", and that is false for the bytes it described — `.ufo/waves/round-44/count-c2.py:111` builds `env = dict(os.environ)` and hands it to every audited counter, every mutant and the auditor, so a fixture commit lands wherever `GIT_DIR` says instead of only under the caller TMPDIR; the round-45 arm's `TRUE` (`evidence/write-scope.txt:96`) was taken with `GIT_*` removed, so it cannot see this. Superseded on the round-44 sentinel's F8 reading (`.ufo/waves/round-44/w1/SentTools.md` §F8), not re-measured by this row | mori |
| r44 corpus coverage (C3) — write scope superseded | gate | `python3 .ufo/waves/round-44/count-c3.py <rev> --entry PATH --row S### [--row S### ...]` (`--coverage-map`, `--census PATH`, `--readme PATH`, `--selftest`) | unchanged from row `r44 corpus coverage (C3)` (SKILL.md:186), which remains the verdict-map authority; this row supersedes that row's write-scope cell only | unchanged from row `r44 corpus coverage (C3)`: `python3 .ufo/waves/round-44/count-c3.py --selftest` → measured `C3_SELFTEST pass=6 fail=0` rc 0 (re-run 2026-10-25) | unchanged from row `r44 corpus coverage (C3)` (SKILL.md:186) | superseded: the cell at SKILL.md:186 reads "stdout only; the registry copy handed to the census is materialized under the caller TMPDIR", and that is false as a write-scope claim — it names where one copy goes and omits that the census arm executes a caller-named program (`.ufo/waves/round-44/count-c3.py:139`: `bash <census> validate --file <staged>`) unsandboxed, so that program writes anywhere; the round-45 arm's `TRUE` (`evidence/write-scope.txt:110`) covers only its `--selftest` run. Superseded on the round-44 sentinel's F8 reading (`.ufo/waves/round-44/w1/SentTools.md` §F8), not re-measured by this row | mori |

Round-45 registry refresh (2026-10-25): six rows were added — three tools that had none (`mori-disk-rate.py`,
`mori-wave-settlement.py`, `mori-round41-calibration.py`) and the round-45 counters `count-c1.py`, `count-c2.py`,
`count-c3.py` — plus four append-only superseding rows for the round-44 write-scope cells (183-186), whose claim
was true only for the observed `--selftest` run and false for the input the instrument executes. Four self-test
cells were updated in place to the branches landed this round: `silence oracle` (166, `MORI_SILENCE_CASES_SELFTEST
pass=24`), `r19 finite regressions` (182, `R19_SELFTEST pass=26`), `routed round-23 items (r24, C1)` (646,
`ROUTED_CHECK_SELFTEST pass=20`) and `routed round-24 items (r25, C1)` (721, `ROUTED_R24_SELFTEST pass=26`), each
measured 2026-10-25. None of these rows changes a tool's verdict map or a prior row's authority.

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

- Historical records include an `EDQUOT` write failure, not a complete current
  failure diagnosis. Capacity percentages cannot detect quota exhaustion;
  per-ID quota limits/usage remain unmeasured here. The rejected round23 quota
  attempt is evidence only under `.ufo/waves/round-23/rejected/`.
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

The historical schema-v1 registry is retained at
`da40bb20f81da125d798f73cd1653655be1255ca:SKILL.md`. Its old predicates are not
current API instructions; use the sole schema-v2 reconciliation row below.

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

## Round23 — current reconciliation API; quota attempt withdrawn

The round22 registry/field caveats above are historical v1. Current reconciliation
schema is `mori-retention-reconciliation-v2` on check/setup/selftest outputs.
`raw_unallowlisted` is REMOVED, not silently redefined or aliased. Use
`scanner_unallowlisted` for the policy-filtered in-scope count and
`raw_not_allowlisted` for the raw complement. The retained r21 control is4 versus9,
not two estimates of the same population. All original identity/exit/finding
semantics remain; `privacy_clearance` remains false. Frozen r22 oracles/real and
refinement checks that name the old key reproduce only in a checkout of their bound
revision, not by passing that revision to a changed working-tree driver.

The rows below supersede only the current-entry/pins of the round22 reconciliation
row; old evidence is not rewritten. `--repo` must be absolute (`"$PWD"`, not `.`).
Use an existing private scratch root for selftests; do not let an invalid TMPDIR
fall back to /tmp. New heavy scratch belongs under /fast/scratch/hyaku/mori-r23.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| retention reconciliation schema-v2 (r23) | gate, artifact accounting only | `python3 tools/mori-retention-reconcile.py check --repo "$PWD" --rev INPUT_COMMIT --receipt .ufo/waves/round-21/evidence/final/retention-floor.json --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` | 0 RETENTION_RECONCILED even when red; 1 RETENTION_RECONCILIATION_MISMATCH; 2 RETENTION_RECONCILIATION_SETUP | `TMPDIR=<existing-private-scratch> python3 tools/mori-retention-reconcile.py --selftest`; isolated actual CLI checks | `.ufo/waves/round-23/frozen/c1-requirements.json`, c1-source-delta.json, c1-expected-real.json, c1-expected-real-identities.json and oracle-rename.py; original26 separate from supplementary byte/output guards | read-only committed inputs; selftest private temporary fixtures | mori |

**C2 quota visibility is withdrawn, unadmitted evidence, not a supported tool.**
The deployed prototype and its knowledge note were removed after all96 pinned
readers settled; byte-exact copies and the failed observations remain under
`.ufo/waves/round-23/rejected/`. No quota command, registry entry or capability
is supported by those evidence files, and FR2 remains Frontier.

The original strict target remains **29/30, unprovable/not admitted**.
Frozen CaseEscapedSpace, its expected enabled row and the opposing pre-sealed
parent-ID rule all remain unchanged; there is no exception, exclusion or relabel.
An actual fully mocked permission-loss probe also produced false `disabled`
confidence after one UUID's device-list failure was dropped from the mapping
(`falsify/MutModeRead/permission-loss.json` under the round23 wave directory).
Primary kernel sources show that tmpfs active accounting tokens can persist
after runtime limit enforcement is disabled; the former `enforced` label was
not an observed enforcement flag. No kernel enforcement experiment was run.

C1 is separate: schema-v2 reconciliation and its original26/26 plus exact-source,
same-instance output, selftest and identity guards remain the supported work.
This grants no privacy, history, baseline, lifecycle or health clearance.
Four inherited retention hits, permission11/12red, two unknown dispositions and
blocked baseline acceptance remain. Configuration/diagnosis/remediation belong
to tsukuroi/operator; no census, threshold, Core or rank change follows withdrawal.

## Round24 — one-shot system pressure read (C2)

`python3 tools/mori-pressure.py` reads the **system** pressure files `/proc/pressure/{cpu,memory,io,irq}`
once (or twice with `--interval S`) and returns a verdict. It is detection and report only: it
never writes to `/proc`, `/sys` or a cgroup, never registers a PSI trigger, and never changes a
service. The resident trigger watcher and cgroup-scoped CPU/IO/IRQ pressure stay Frontier
(`PROVINCE.md:55`).

Sources: S090 (psi.rst), S091 (psi.c), S095 (psi_types.h), S145 (PSI_IRQ commit); knowledge entry `corpus/knowledge/system-pressure-r24.md`. System pressure is host-wide: a high reading is not evidence that the fleet caused it.

### Reading system pressure

| Condition | Report as | Never infer |
|---|---|---|
| system `/proc/pressure/cpu` shows `full avg10=0.00 … total=0` | `cpu.full` reported with `full_system_undefined: true`; the value is never a threshold input | that the CPU had no full stall — system CPU `full` is undefined and exported as zero for backward compatibility ([psi.rst:57-58](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst); [psi.c:1282-1288](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| `some avg10` ≥ `--warn-avg10` on `cpu`, `io` or `memory` | finding `PRESSURE_HIGH` naming the resource and the kind; the threshold is labeled local, not calibrated | that the fleet, a lane or a task caused the stall — `/proc/pressure/*` is system-wide ([psi.rst:37-38](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)); per-cgroup numbers live in the cgroup2 `*.pressure` files ([psi.rst:178-190](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)) |
| `full avg10` ≥ `--warn-avg10` on `memory`, `io` or `irq` | finding `PRESSURE_HIGH` on the `full` kind of that resource | that `full` means "all non-idle tasks stalled" for `irq` — that wording is the documented cpu/memory/io definition ([psi.rst:48-54](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)); the `irq` resource is exported only by the kernel code and is not described in `psi.rst` |
| the `irq` file carries no `some` line | `irq.some = null`, resource state `ok` | that irq "some" pressure is zero, or that a missing `some` line is malformed — the kernel prints only the `full` line for `PSI_IRQ` ([psi.c:1272-1276](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c), [psi.c:1289-1290](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| `/proc/pressure/irq` cannot be opened (ENOENT) | resource state `absent` | that there was no IRQ pressure — the file is created only under `CONFIG_IRQ_TIME_ACCOUNTING` ([psi.c:1717-1718](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| the read returns EOPNOTSUPP | resource state `unsupported`; no cause recorded (on v7.2 reachable through `/proc/pressure` only on `irq`, when IRQ time accounting is off — S091 `psi.c:1260-1263`; a boot-disabled PSI removes the files, so the `psi_disabled` branch is not reachable while they exist; see the knowledge entry's corrections section) | a zero reading, or which cause applied — kernel and boot diagnosis belongs to tsukuroi |
| the read returns EACCES/EPERM | resource state `unreadable` | a zero reading |
| any resource is `absent`, `unsupported` or `unreadable` | that resource is unavailable; verdict `PRESSURE_PARTIAL` (exit 0) unless every resource is unavailable → `PRESSURE_UNAVAILABLE` (exit 2) | that the resources that did read describe the whole system, or that partial coverage is a clean bill of health |
| the file breaks the line grammar (duplicate kinds, a missing required kind, a non-decimal avg, a non-integer or negative total) | resource state `malformed` | that the missing or unparsable value was low or zero — a malformed file is not a low-pressure reading; `total` is cumulative stall microseconds and `avg*` are percentages over 10/60/300 s windows ([psi.rst:40-43](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst), [psi.rst:60-63](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst), [psi.c:1290](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) |
| two reads with `--interval S` | `total_delta_us` and `stall_ratio` per kind; a decreasing total → resource state `counter_regressed` | that pressure fell because the counter decreased, or any stall duration from a single `total` without a delta |
| one-shot read (no `--interval`) | a point-in-time sample: system-wide stall percentages plus cumulative stall microseconds | that no stall happened between reads — a PSI trigger watcher stays Frontier (`PROVINCE.md:55`), and writing a trigger into `/proc/pressure/*` is a host write this lane never performs ([psi.rst:67-95](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst)) |

### Round24 registry additions

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| system pressure (r24, C2) | gate (host-surface verdict; not a census or fleet-admission gate) | `python3 tools/mori-pressure.py [--root DIR] [--warn-avg10 X] [--interval S] [--selftest [--cases FILE]]` (the selftest also prints `MATCHER: rejected n/n corrupted expectations` and fails if the matcher accepts one) — `--root` defaults to `/proc/pressure`; reads `cpu`, `memory`, `io`, `irq` | 0 → clean (`PRESSURE_OK`; `PRESSURE_PARTIAL` also exits 0 and means at least one resource was unavailable, malformed or `counter_regressed`; a threshold finding anywhere outranks it) · 1 → failed (`PRESSURE_HIGH`) · 2 → could-not-evaluate (every resource unavailable, or usage error) | `python3 tools/mori-pressure.py --selftest` → `MORI_PRESSURE_SELFTEST: PASS 12/12` over `tools/fixtures/mori-pressure/cases.json` (P01–P12, landed in a strict-ancestor commit before the tool; the tool seat read the cases while building, so the order is shown, not independence); error injection (EOPNOTSUPP, EACCES) uses an in-process open hook, documented as such | `tools/fixtures/mori-pressure/cases.json` (schema `mori-pressure-cases-v1`; each case pins exit, verdict, per-resource state, `some`/`full` subsets and `findings_include` pairs); `--warn-avg10` default 10.0 is labeled local, not calibrated | none live — stdout only; reads `/proc/pressure/{cpu,memory,io,irq}` (or `--root`); no `/proc`, `/sys` or cgroup write, no PSI trigger registration, no service or package change; selftest is in-process over the frozen cases | mori |
| routed round-23 items (r24, C1) | gate | `python3 -I tools/mori-routed-check.py --repo <repo> --rev <REV> [--round N]` (N defaults to 24) | 0 clean (`held` == `items` == 4) · 1 failed (any routed row red; R4 includes ledgers that are unclean, unbound, missing for a wave spec, or whose `at` precedes the commit that last changed the dispatch file) · 2 could-not-evaluate (repo, revision or base unreadable) | `python3 -I tools/mori-routed-check.py --selftest` → `ROUTED_CHECK_SELFTEST pass=20 fail=0`, added round 45; able-to-fail evidence remains the thirteen sandbox mutants in `.ufo/waves/round-24/w1/BuildRoutedCheck.md` | base `c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130` (fixed in the tool); `corpus/QUALITY.md` criteria 72-75 | read-only git object reads over the measured repo; runs `tools/mori-dispatch-ledger.py verify` as a subprocess | mori |

## Round25 — harness background-job cap (C2)

Grounded in `corpus/knowledge/harness-job-capacity-r25.md` (sources S098–S104, S112–S113; rows 2–3 also S134, S135, S136, added round 27 for routed R3). Upstream line
anchors below are at oh-my-pi tag `v18.12.6`.

### Harness background-job cap refusal (r25)

The fixed text `Background job limit reached (100). Wait for running jobs to finish or cancel one.`
is upstream's own message from the async job manager's registration path
(`job-manager.ts:371-373` at v18.12.6; installed `omp` byte 160033342), wrapped by the task tool as
`Failed to start background task job{s}: <agentId>: <message>` (`task/index.ts:1220-1230`).

| Condition | Report as | Never infer |
|---|---|---|
| the fixed sentence appears in a transcript or tool result | a harness **registration refusal** at the session's running-job cap; the number is the **effective** cap at that instant, `max(1, floor(min(100, async.maxJobs)))` — the clamp is compiled into the binary (`sdk.ts:2284`, byte 164406766), so `(100)` is the clamp, not the operator's configured value | that the operator configured 100 (the operator's OMP settings file sets a value above the clamp, and the clamp reduces it to 100; that file is one host's configuration, not a fleet fact — `corpus/knowledge/harness-job-capacity-r25.md` F12); that the cap is still 100 now — it is re-read at every check (`job-manager.ts:331-335`); that the refused work ran — `register()` throws before the job exists (`task/index.ts:1210-1219`, `results: []` at `:1229`) |
| an **auto-backgrounded** bash call, or the eval tool's auto-background branch, was made while the cap was full | nothing from that call — the auto-background branch checks `atCapacity` first and runs in the foreground instead (`tools/bash.ts:1220-1229`, `tools/eval.ts:536`) | that the cap was not reached; that the call was backgrounded; that every call at the cap is silent — eval `agent()`, `workpool()` and an explicit `async: true` bash reach `register()` with no `atCapacity` check and do raise the refusal (`docs/tools/eval.md:258`; `eval/agent-bridge.ts:210`; `task/workpool.ts:175,363`; `tools/bash.ts:1188-1209`) |
| a registration was refused — a `task` spawn, an eval `agent()` or `workpool()` batch, a vibe subagent, or an explicit `async: true` bash | one refused registration; a batch can partially start, so refusals and starts coexist in one result (`task/index.ts:1191-1219`, `:1233-1236`) | that the wave is dead — a refusal creates no job; that the count was this wave's own seats: the population is every **running, non-queued** job in the session tree — bash, task and eval alike (`job-manager.ts:343,367`, `:48`; `tools/bash.ts:882`) — and a parked (queued) task job counts only after `markRunning()` (`task/index.ts:1565,1490`); that the paths named here are the only ones that can refuse — of the twelve `register()` call sites in the shipped source only the bash and eval auto-background branches pre-check `atCapacity`, so ten sites refuse with no check of their own (`eval/agent-bridge.ts:210`; `eval/judgment-batch-bridge.ts:223`; `modes/controllers/tan-command-controller.ts:144`; `security/coordinator.ts:499`; `task/executor.ts:3272`; `task/index.ts:1407`; `task/restore.ts:85`; `task/workpool.ts:175,363`; `vibe/runtime.ts:1370`) |
| mori must state the cap | `python3 -I -B tools/mori-job-runway.py` → one JSON object (`schema: mori-job-runway-v1`) with `configured {state,value}`, `clamp {state,value,sites}`, `setting_default {state,value,sites}`, `effective`, and `verdict` ∈ `RUNWAY_CLAMPED` (exit 1) / `RUNWAY_AS_CONFIGURED` (exit 0) / `RUNWAY_DEFAULT` (exit 0) / `RUNWAY_UNKNOWN` (exit 2) | that the session was at capacity — the tool reports the **cap**, never a running-job count, and the live count is not readable from outside the session (`.ufo/waves/round-25/contract.md:83-85`); that an absent or unreadable clamp means "no clamp" (it is `RUNWAY_UNKNOWN`); that the file sets no `maxJobs` — `RUNWAY_DEFAULT` also reads a root flow mapping, a JSON file or a flow-mapped `maxJobs` child as absent, so the effective 100 is the schema default rather than a value read from the file (`corpus/knowledge/harness-job-capacity-r25.md` decision row `RUNWAY_DEFAULT`); that the file's `async.maxJobs` is the value the session resolved — the runtime settings stack has project and overlay layers the tool does not read (`corpus/knowledge/harness-job-capacity-r25.md` F13) |

**mori never acts on this text.** It does not edit the operator's OMP settings file or any other OMP
setting, it does not cancel or kill a running job, and it does not split, shrink or re-dispatch a
wave. mori is detection and report only (`SKILL.md:9`, `SKILL.md:139-147`, `PROVINCE.md:12-18`).
Dispatch and wave shape are kumitate's (`PROVINCE.md:65`); writes under `~/.omp` are the operator's
(`kama-shokunin/PROVINCE.md:45-47`); the harness-side remedy the message itself names — let running
jobs finish, or cancel one — is the operator's, and mori reports the refusal as evidence, not as a
work order.

**A refusal is not repairable by raising the setting.** `async.maxJobs` above 100 cannot lift this
cap: the clamp is compiled into the binary (`sdk.ts:2284`), so a configured 200 already means an
effective 100. Only the operator can change the installed binary or the harness build.


## Round26 — userspace OOM killers (C1/C2)

`python3 -I -B tools/mori-oom-killers.py` reads what this host's two **userspace** OOM killers
(earlyoom, `systemd-oomd`) are set to do and whether they have acted. It is detection and report
only: it starts, stops or configures nothing, and it never prints journal `MESSAGE` text, a process
name, a command line, a uid or an `--avoid`/`--prefer` expression. Host/unit diagnosis and any
killer tuning stay operator-owned (`PROVINCE.md:53`, FR10).

Grounded in `corpus/knowledge/userspace-oom-killers-r26.md` (the 2026-10-22 host record that
supersedes the 2026-10-19 reading in `corpus/knowledge/userspace-oom-killers-r12.md`) and in the
earlyoom v1.9.0 message grammar at tag `v1.9.0`. The tool is the Core surface; this table is the
reading rule.

### Did a userspace killer act?

| Condition | Report as | Never infer |
|---|---|---|
| earlyoom is `active` and its unit journal (current boot) holds a `sending SIGTERM to process ` or `sending SIGKILL to process ` line, or an `escalating to SIGKILL after ` line, **inside the current invocation's scope** | `KILLER_ACTED` (exit 1); `earlyoom.actions.sigterm` / `.sigkill` / `.escalations` counted | that a process died — the line is earlyoom's own log of a signal it sent ([kill.c:627](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c), [kill.c:318](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c)); that the count is a victim count (it is a count of log lines); that the killed process belonged to the fleet |
| earlyoom is `active` and reports `dryrun` mode (`dryrun mode enabled`, [main.c:295](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)) | `earlyoom.dryrun_send_lines` counts the send lines; `sigterm`/`sigkill` stay 0 and are never positive evidence | that nothing was signalled — dry-run sends no signal; that a dry-run line means a kill happened |
| earlyoom is `inactive` or its unit is `not-found` | `earlyoom.state` is `inactive` or `absent`; `earlyoom.actions` is **null** (unavailable), never zero counts | that the killer made no kills — an unavailable killer is not a killer that did nothing; that the host is healthy on the memory plane |
| earlyoom is in a non-steady state (`failed`, `activating`, `deactivating`, `reloading`, `maintenance`, `refreshing`) | `earlyoom.state` is `unavailable`; verdict `KILLERS_UNKNOWN` (exit 2) | that the unit is idle — an earlier invocation may have acted, so the state is not readable as active or inactive |
| earlyoom is `active` but its `ActiveEnterTimestampMonotonic` is missing or 0, or the invocation's version line is not in scope | `scope_complete: false`, verdict `KILLERS_UNKNOWN` (exit 2) | that the scope was empty because nothing happened — an unbounded scope is unknown, not quiet |
| an earlyoom `sending … to process` line falls **before** the current invocation's `ActiveEnterTimestampMonotonic` (an earlier invocation in the same boot) | `earlyoom.earlier_invocation_send_lines` reports the count; for an `active` unit it is not a verdict input (frozen case `c02`), for a unit that is not `active` it is positive evidence → `KILLER_ACTED` | that a restarted earlyoom never killed anything — the earlier invocation's sends are still sends; that `scope_complete: true` means the whole boot was checked |
| `systemd-oomd.service` notices with catalog `MESSAGE_ID` `d989611b15e44c9dbf31e3c81256e4ed` exist in the current boot | `oomd.notices_this_boot` > 0 → `KILLER_ACTED` (exit 1); the count is of journal **notices**, one per killed unit | that the notice names a unique victim — the catalog entry is "one or more processes in the unit @UNIT@" ([systemd.catalog.in:884-885](https://raw.githubusercontent.com/systemd/systemd/v262/catalog/systemd.catalog.in)); that oomd acted on the fleet |
| the kernel wrote an `oom-kill:constraint=` summary (system journal, `journalctl -k`) | kernel-side OOM evidence, reported by the existing kernel attribution path (`corpus/knowledge/kernel-oom-line-attribution-r12.md`) | that earlyoom or oomd caused it — earlyoom v1.9.0 has **no** `--kernel-oom` delegation option (its `-k` is ignored since v1.2, [main.c:245-246](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c); the option list at [main.c:180-192](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c) has no `kernel-oom`), so an earlyoom kill never produces a kernel OOM record |
| a needed read failed (unit show unreadable, journal unreadable, notice count unavailable) | the affected field is `null` / the state is `unavailable`; verdict `KILLERS_UNKNOWN` (exit 2) | that the killers were quiet — an unreadable surface is unknown, not zero |
| everything readable, no positive evidence anywhere | `KILLERS_QUIET` (exit 0) | that no memory kill happened in this boot — quiet means "no positive evidence from the killers that could be read", and it names the unavailable ones |

### Error patterns (userspace OOM killers)

| Observation | Reading |
|---|---|
| earlyoom's thresholds read from `/etc/default/earlyoom`, from the unit file, or from the upstream defaults | the thresholds in force are the ones earlyoom printed at startup: `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` ([main.c:414](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)) and `SIGKILL when mem avail <= <c>% and swap free <= <d>%` ([main.c:416](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c)), read from the unit's journal. The packaged default file is only the argument source (`EnvironmentFile=-/etc/default/earlyoom`, `ExecStart=/usr/bin/earlyoom $EARLYOOM_ARGS`, `/usr/lib/systemd/system/earlyoom.service:6-7`); the built-in defaults are 10 % with `PERCENT/2` for the kill threshold ([MANPAGE.md:31,45,56-57](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md)). **Never** treat the config file or the documented default as the running configuration — the running values are the printed ones; and never copy the file's values or the `--avoid`/`--prefer` expressions into a report |
| `oom_kill=0` (cgroup `memory.events` or `/proc/vmstat`) read as "no memory kills" while earlyoom is `active` | that counter moves only at the **kernel** victim site ([oom_kill.c:935-936 v7.2](https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c)); earlyoom signals in userspace and never increments it, and systemd-oomd kills through `cgroup.kill`/`kill()` and records `user.oomd_ooms`/`user.oomd_kill` xattrs instead ([oomd-util.c:269-306 v262](https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c)). With earlyoom active, `oom_kill=0` says only "no **kernel** OOM kills"; the userspace killers' own evidence is earlyoom's journal send lines and the `d989611b…` oomd notices. `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`, `userspace-oom-killers-r12.md` |
| earlyoom journal lines counted from a whole-boot query (`journalctl -b -u earlyoom.service` with no invocation bound) | earlyoom's log lines belong to **one invocation**; the scope is the lines whose `__MONOTONIC_TIMESTAMP` is at or after the unit's `ActiveEnterTimestampMonotonic`. A restart inside one boot gives a new `ActiveEnter`, so the previous invocation's send lines fall below the bound and a whole-boot count attributes an old kill to the running instance (`earlyoom.earlier_invocation_send_lines`; `.ufo/waves/round-26/w1/ReviewScopeClock.md:56-69`). The bound is comparable within a boot because both clocks are `CLOCK_MONOTONIC` |

### Round26 registry additions (three tools; the two round-25 rows answer routed R5)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| userspace OOM killers (r26, C2) | gate (host-surface verdict over two units; not a census or fleet-admission gate) | `python3 -I -B tools/mori-oom-killers.py [--inputs FILE \| --selftest \| --dump-inputs] [--cases FILE]` — no arguments collects the inputs live (`systemctl show` of the two units' `LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic`; the earlyoom unit journal of the current boot; the `d989611b15e44c9dbf31e3c81256e4ed` notice line count) and runs the same pure reader; `--inputs FILE` runs the reader on one JSON inputs object; `--dump-inputs` prints the live inputs with every non-version/threshold `MESSAGE` replaced by its grammar class | 0 → clean (`KILLERS_QUIET`) · 1 → failed (`KILLER_ACTED`) · 2 → could-not-evaluate (`KILLERS_UNKNOWN`: a needed read is null, an active earlyoom has an incomplete scope or an unverified grammar, a show text lacks `ActiveState`, or a setup/internal error — an uncaught exception never exits 1) | `python3 -I -B tools/mori-oom-killers.py --selftest` → `MORI_OOM_KILLERS_SELFTEST: PASS 32/32` over `tools/fixtures/mori-oom-killers/cases.json` (32 cases, `schema: mori-oom-killers-cases-v1`, frozen in `5b10649` before the tool's first commit `c2fdd92`; `count-c2.sh` reports `freeze_order=ok`, `cases_changed_since_freeze=0`) | result `schema: mori-oom-killers-v1`; `earlyoom` {`state` (`active`/`inactive`/`absent`/`unavailable`), `version`, `grammar` (`verified-1.9.0`/`unverified`), `thresholds`, `scope_complete`, `actions`, `dryrun`, `dryrun_send_lines`, `process_group_lines`, `earlier_invocation_send_lines`}, `oomd` {`state`, `notices_this_boot`}, `verdict`; the earlyoom grammar is pinned to tag `v1.9.0` (`main.c:161,295,414,416,519,523`; `kill.c:318,627,654`); `actions` is null for an inactive or absent killer, never zero counts | none live — stdout only; reads `systemctl show` and `journalctl` (two `journalctl` reads, one for the unit journal and one for the notice count); no unit, journal, package or network change; the output carries states, numbers, the version string and counts — never `MESSAGE` text, a process name, a command line, a uid or an `--avoid`/`--prefer` expression | mori |
| routed round-24 items (r25, C1) | gate (committed-bytes consistency gate over the lane's own round-24 evidence; not a fleet-admission gate) | `python3 -I -B tools/mori-routed-r24.py --repo REPO --rev REV [--rerun]` — every predicate reads git objects only (`cat-file`, `ls-tree`, `archive`, `merge-base`) at REV; the working tree is never consulted; `--rerun` additionally re-executes the named revision's `mori-pressure.py --selftest` from a temporary extract and reports byte equality | 0 → clean (`status: held`: all four counted items D1, D2, D3, D5 held **and** the D4 hygiene row held) · 1 → failed (any counted item red, or the D4 hygiene row red) · 2 → could-not-evaluate (the repository path is not a directory, the revision does not resolve to a commit, or a git call fails) | `python3 -I -B tools/mori-routed-r24.py --selftest` → `ROUTED_R24_SELFTEST pass=26 fail=0`, added round 45: the D1-D5 arms run over isolated throwaway git repos under `$TMPDIR`; able-to-fail evidence remains the round-25 wave-2 mutation reports (`.ufo/waves/round-25/w2/MutRoutedD1.md`, `MutRoutedD2.md`, `MutRoutedD3D5.md`, `MutRoutedHygiene.md`) | result `schema: mori-routed-r24-v1`; `items: 4`; per-item rows `{id, held, reasons[], detail}` for D1 (stale gate evidence), D2 (correction sweep in `corpus/knowledge/system-pressure-r24.md`), D3 (lesson count drift), D5 (`## Axes` table against the pinned base `28b79d3d`); D4 is a reported hygiene row, not a counted item; D3's case count is pinned to `4f05dd5a` (7 supplementary cases) | read-only git object reads over the measured repo; a temporary extract only for `--rerun`; **known limits**: D1 compares the recorded body with a constant, so only `--rerun` detects a forged PASS; D5 reads the Score and Last-change columns by position, never by header name; D2 does not scan heading lines for the stale phrases; D3 holds while the uncorrected `PASS 6/6` line remains; an unreadable pinned baseline exits 1, not 2; a promisor clone can have objects fetched into it (no `GIT_NO_LAZY_FETCH`); a `--repo` below the repository top level changes the result. `corpus/lessons/round-25-verifier-spotcheck.md:189-193` | mori |
| harness background-job runway (r25, C2) | gate (reads the operator's harness configuration and the installed binary; not a census or fleet-admission gate) | `python3 -I -B tools/mori-job-runway.py [--config PATH] [--binary PATH] [--selftest] [--cases PATH]` — `--config` defaults to `~/.omp/agent/config.yml`, `--binary` to the real path of `omp` on `PATH`; the tool reads one settings file and one binary and never runs `omp` | 0 → clean (`RUNWAY_AS_CONFIGURED` when the configured value equals the effective cap, `RUNWAY_DEFAULT` when no `maxJobs` is configured) · 1 → failed (`RUNWAY_CLAMPED`: the effective cap differs from the configured value) · 2 → could-not-evaluate (`RUNWAY_UNKNOWN`: the effective cap could not be derived, or a usage error) | `python3 -I -B tools/mori-job-runway.py --selftest` → `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` over `tools/fixtures/mori-job-runway/cases.json` (21 frozen cases); a co-evolved `tools/fixtures/mori-job-runway/supplementary-cases.json` (24 cases) is **not** counted; `--selftest --cases ""` silently runs the frozen cases instead of failing | result `schema: mori-job-runway-v1`; `configured {state,value}`, `clamp {state,value,sites}`, `setting_default {state,value,sites}`, `effective`, `verdict`; the clamp is `max(1, min(clamp, base))`; the configured value is read from a block-style `async:` → `maxJobs:` child only | read-only: one settings file and one binary are read; the only writes are the `--selftest` temporary files; the operator's settings file is never edited and its values are never printed in a report. **Known false-number limit (routed defect R1, still open)**: the rule-1 line grammar reads only the block-style `async:` → `maxJobs:` form, so a YAML/JSON form that omp's own parser reads as `maxJobs: 50` (a flow mapping `{async: {maxJobs: 50}}`, a JSON file, a flow or tagged child, an anchored or escaped `async` header, an indented root) is reported as `configured {absent, null}` → `effective 100` → `RUNWAY_DEFAULT`, exit 0 — a **false number**, and a file omp's parser refuses can still be reported as `set 50`, exit 0; `--selftest --cases ""` silently runs the frozen cases; an uncaught exception exits 1, the `RUNWAY_CLAMPED` code. `corpus/lessons/round-25-verifier-spotcheck.md:174-179`; `corpus/knowledge/harness-job-capacity-r25.md:211` | mori |

## Round27 — OOM victim selection (oom-victim-selection-r27.md)

Grounding for every row: `corpus/knowledge/oom-victim-selection-r27.md` (sources S003, S118, S148, S150, S130,
S132). Detection and report only: no row advises changing a setting, an `oom_score_adj` or an earlyoom option.

| Situation | What to conclude | What not to conclude | Grounding |
|---|---|---|---|
| a seat or lane died and the killer is unknown | check both journal event sources in the relevant boot and window: earlyoom-unit sends versus kernel OOM summaries and killed-process records; report each source separately | that earlyoom activity excludes a kernel kill, that kernel activity proves an earlyoom send, or that either class label identifies a seat or lane | `oom-victim-selection-r27.md` Fact 6 |
| earlyoom sent SIGTERM or SIGKILL and you must say which fleet process was most at risk | earlyoom takes the highest `oom_score` it computes: the kernel's exported score plus 300 for a `--prefer` name match, minus 300 for `--avoid`; in the 2026-10-22T15:56Z sample the session `omp` process ranked second on the host | that the largest process is chosen; the key is `oom_score` unless `--sort-by-rss` is set | `oom-victim-selection-r27.md` Facts 1 and 4; [kill.c:457-465](https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c) |
| a send line's `oom_score` exceeds `(2000 + oom_score_adj) * 2 / 3` (1466 at adjustment 200) | a `--prefer` match added 300 to that victim, if earlyoom runs without `--sort-by-rss` and no swapoff was in progress [INFERENCE: the ceiling assumes no page is counted twice in the resident set] | what the prefer expression says (it is never read or copied); that a line at or under the ceiling had no prefer match | `oom-victim-selection-r27.md` Facts 1, 2 and 5; [base.c:597](https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c) |
| a fleet process shows `oom_score_adj` 200 | it descends from a user unit of the unprivileged per-user manager (manager 100, children 100 more); the harness did not set it; it weighs as if the process held 20% more of RAM plus swap | that it was configured for the fleet, or that it cannot change: it can be raised, and lowered down to its floor of 100 | `oom-victim-selection-r27.md` Fact 3; [user@.service.in:35](https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in), [main.c:3063](https://raw.githubusercontent.com/systemd/systemd/v262/src/core/main.c) |
| an in-session seat died and the journal shows an earlyoom send to an `omp`-class process in that window | the session process may have been the victim, which ends every seat of that session at once (task seats run in-process, S142) | that the victim was the session process: the `omp` class also holds other sessions and the text-prediction daemon worker; which seat or lane the kill was for; the journal names a process class, never a seat | `oom-victim-selection-r27.md` Facts 4 and 6 |
| an earlyoom send to a `python`-class process in the same window as a dead seat | it establishes signalling of that selected process, not the session's survival or death; check separately for kernel OOM events and other earlyoom sends | that the process belonged to the fleet, that the signal proves exit, or that absence of an earlyoom send to the session excludes another cause | `oom-victim-selection-r27.md` Facts 5 and 6 |
| `memory.oom.group` is 1 on a cgroup | a kernel OOM kill whose victim sits below it takes the subtree of the highest ancestor with the flag set, up to the OOM domain (tasks at -1000 spared); an OOM confined to a cgroup below that ancestor ignores it | that earlyoom does the same; it signals one process | `oom-victim-selection-r27.md` Fact 2; [cgroup-v2.rst:1450-1466](https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst) |
| a lane is marked dead minutes into a new boot | the death was detected after a reboot | the time of death or its cause | `oom-victim-selection-r27.md` Fact 6 |

### Error patterns (OOM victim selection)

| Observation | Reading |
|---|---|
| "the +200 band is scanned first" (tsukuroi `oom-event-plane.md:116,349`, `kill-event-deep-r8.md:147,260`) | false: the kernel makes one pass and keeps the highest score, where the adjustment adds `adj * totalpages / 1000` pages; a tie goes to the later task (`oom-victim-selection-r27.md` Fact 2; [oom_kill.c:228-234,340-348,358-376](https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c)) |
| `oom_score` read as a 0–1000 badness, or the man page's "3% extra for root" applied | the exported file is `(1000 + badness * 1000 / totalpages) * 2 / 3`, range 0–2000, and v7.2 has no root bonus (`oom-victim-selection-r27.md` Fact 2) |
| "an unprivileged process can raise its `oom_score_adj` but never lower it" | false here: it can lower down to `oom_score_adj_min` (100 on this host); only the legacy `oom_adj` file ratchets (`oom-victim-selection-r27.md` Fact 3) |

## Round30 — earlyoom invocation scope (earlyoom-invocation-scope-r30.md)

Grounding for every row: `corpus/knowledge/earlyoom-invocation-scope-r30.md` (its decision table over frozen cases;
sources S156 and later). Every row is tagged `Round30`. Detection and report only: no row advises changing an
earlyoom option, a unit or `/etc/default/earlyoom`.

| Situation | What to conclude | What not to conclude | Grounding |
|---|---|---|---|
| earlyoom is `active` and `ActiveEnterTimestampMonotonic` is missing or `0` | the invocation is unbounded: `earlyoom.scope_complete=false`; every placeable boot line stays a candidate and the current invocation is taken from the last version line, so a send before that line is an earlier-invocation send; with no positive evidence the verdict is `KILLERS_UNKNOWN` (exit 2), and a send inside the last-version tail is still `KILLER_ACTED` (exit 1) | that an unbounded scope is an empty one (nothing happened); that the whole boot is attributed to the running instance; that `KILLERS_UNKNOWN` here is a read failure | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (unbounded-scope rows; cases `a2-05-monotonic-zero-active-quiet`, `a2-05-monotonic-zero-inactive-quiet`); rule A2-05 (`.ufo/waves/round-27/contract.md:53`); `58b61681:tools/mori-oom-killers.py:278-302`, `:424` |
| earlyoom is `active`, `ActiveEnterTimestampMonotonic` is missing or `0`, a real send line appears in the boot, then a plain restart (a later version line) — the disputed shape round 29 moved from `KILLER_ACTED` to `KILLERS_UNKNOWN` | `KILLERS_UNKNOWN` (exit 2): the send falls before the last version line and is counted only in `earlyoom.earlier_invocation_send_lines`, `earlyoom.actions.sigterm` stays 0 and `scope_complete` is false. This is the A2a limit: for an `active` unit an earlier-invocation send is reported but is not a verdict input, so the reader abstains — it neither claims the send acted now nor calls the unit quiet | that the restart erased the earlier send; that the earlier send proves the current invocation acted; that this `KILLERS_UNKNOWN` is a tool or read failure; that the same shape reads `KILLERS_QUIET`; that the rule text alone forces this reading (a literal scope reading gives `KILLER_ACTED`; wave-1 ReviewRuleTextShape F1) | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (disputed-shape section and A2a limit; the shape itself is pinned only by the blind frozen cases `tools/fixtures/mori-oom-killers/cases-a2-r30.json`; the A2a report-only rule is shown on a bounded scope by table case `a2-06-active-earlier-invocation-sends-quiet`, which is not the disputed shape); rules A2-05, A2-06, A2-07 (`.ufo/waves/round-27/contract.md:53-55`); A2a (`.ufo/waves/round-26/contract.md:171-172`, `:178-179`); `58b61681:tools/mori-oom-killers.py:293-302`, `:465-469`, `:487-489` |
| a send or escalation line of this boot sits outside the current invocation (before `ActiveEnterTimestampMonotonic`, or before the last version line under an unbounded scope) | it counts in `earlyoom.earlier_invocation_send_lines`; for an earlyoom that is not `active` a non-zero count is positive evidence → `KILLER_ACTED` (exit 1) with `earlyoom.actions=null`, so a stop or restart is not quiet; since round 30 a non-active unit with a readable show text and a retained non-zero stamp also counts a send inside its last invocation as positive evidence (`.ufo/waves/round-30/evidence/fix-tool.diff`) — that send is counted in no output field, so a non-active `KILLER_ACTED` can show every count at 0; for an `active` unit an earlier send is reported and is not itself a verdict input | that a restarted or stopped earlyoom never killed anything; that `scope_complete=true` means the whole boot was checked; that earlier sends belong to the current invocation's `earlyoom.actions`; that a non-active `KILLER_ACTED` always shows a non-zero count | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (earlier-invocation rows; cases `a2-06-inactive-earlier-invocation-sends-acted`, `a2-06-active-earlier-and-current-send-acted`); rule A2-06 (`.ufo/waves/round-27/contract.md:54`); `.ufo/waves/round-26/contract.md:175-179`; `58b61681:tools/mori-oom-killers.py:317-352`, `:465-469` |
| the journal holds `dryrun mode enabled` and send lines, or one invocation ran dry-run and another did not | dry-run is per invocation: the scan splits at each version line, so send lines inside a segment that logged `dryrun mode enabled` go to `earlyoom.dryrun_send_lines` while `actions.sigterm` and `.sigkill` stay 0 and are never positive evidence; a real send in another invocation is still counted — in `actions` when it is in the current invocation (`KILLER_ACTED`), in `earlier_invocation_send_lines` otherwise, which for an `active` unit is report-only (`a2-07-earlier-real-then-current-dryrun` reads `KILLERS_QUIET`); a dry-run invocation with no other evidence, a complete scope and a verified grammar reads `KILLERS_QUIET` | that a `sending SIG… to process` line inside a dry-run invocation sent a signal (earlyoom prints the same line and signals nothing); that the current invocation's dry-run flag applies to an earlier invocation or the reverse; that `KILLERS_QUIET` on a dry-run invocation means no send lines were logged (they are in `dryrun_send_lines`) | (Round30) `corpus/knowledge/earlyoom-invocation-scope-r30.md` (dry-run rows; cases `a2-07-earlier-real-then-current-dryrun`, `a2-07-three-invocations-dryrun-in-the-middle`); rules A2-04 and A2-07 (`.ufo/waves/round-27/contract.md:52,55`); `58b61681:tools/mori-oom-killers.py:333-381`, `:417-419` |

## Round31 — watchdog identity from a pid probe (watchdog-identity-r31.md)

Grounding for every row: `corpus/knowledge/watchdog-identity-r31.md` (its decision table; sources S161 and later).
Every row is tagged `Round31`. Detection and report only: no row advises starting, stopping, signalling or locking a
process, or changing the census probe.

| Situation | What to conclude | What not to conclude | Grounding |
|---|---|---|---|
| `pgrep -af shokunin-watchdog` (the census probe) prints a line | a candidate only: `-f` matches any command line that mentions the name (pager, editor, `exec -a` decoy), and the census counts lines, not processes | that the fleet watchdog is running | Round31 `corpus/knowledge/watchdog-identity-r31.md` rows 1–2; S161, S162 |
| `pgrep shokunin-watchdog` without `-f` finds nothing | the probe is blind: the name is at most 15 bytes and procps returns zero matches for a longer pattern; the watchdog's `#!/usr/bin/env bash` shebang makes its name `bash` anyway | that the watchdog is absent | Round31 `corpus/knowledge/watchdog-identity-r31.md` rows 3–5; S161, S162, S163, S164, S165 |
| a process's name or comm equals `shokunin-watchd` | nothing about identity: any thread can set its own 16-byte name with PR_SET_NAME, and a forged process matched `pgrep -x` on this host | that the process is the fleet watchdog | Round31 `corpus/knowledge/watchdog-identity-r31.md` row 6; S169, S172 |
| `pgrep` exits 1, or exits 2 or 3, or the binary is missing | exit 1 is absence for that one query; exit 2 or 3 and a missing binary are `unavailable`, never absence | that a failed or blind probe proves the watchdog is gone | Round31 `corpus/knowledge/watchdog-identity-r31.md` rows 12–13; S161 |
| a pid is seen again later, or its `/proc/<pid>/stat` start time changed | record pid plus start_time (field 22) as the identity pair within one boot; a changed start time is a different process under a reused pid | that a pid number alone names the same process over time | Round31 `corpus/knowledge/watchdog-identity-r31.md` rows 10–11; S167, S171, S173 |
| `/proc/locks` shows a FLOCK on the inode of `.ufo/.watchdog.lock` | a candidate only: some process holding the lock file descriptor is alive (the watchdog or an orphaned child of it); the PID field names the `flock` helper that took the lock, not the watchdog | that the watchdog is alive, that the listed pid is the watchdog, or that a `flock -n` test is a safe probe (it contends) | Round31 `corpus/knowledge/watchdog-identity-r31.md` row 14; S174 |

## Round31 — blind-writer gate (`tools/mori-blind-check.sh`)

Run `bash tools/mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>` inside the lane to
check committed writer briefs before a blind freeze: it prints `scanned=N`, `blind_violations=M` and one
`path:line:rule` per hit (exit 0 none, 1 hits, 2 input error); `--selftest` prints `PASS`. The files-opened rule it
implements is `.ufo/waves/round-31/rule-text.md`; every forbidden list entry is reported at its own line and prose after
the list is never an entry (round-30 D1). Known limits (round-31 residual CriticC2Tip): only `#` headings at
column 0 open or close a block (setext or indented headings do not), CRLF line endings make allowed paths fail, a tab
after `-` is not a list marker, allow globs are not path-normalized (`../` passes), and a `#` line inside a code fence still opens a block
(residual ReviewC2Tool F1). Its two other detectors are the round-30 gate's, with the false positives and
negatives named in `corpus/lessons/round-31.md` (Carried). Detection only: it judges no case.

## Round32 — blind-writer gate registry row and frozen run (round-31 routed defect 2)

The round-31 section above describes the gate in prose. This row gives it every PROTOCOL §Gate standard field. The
frozen-run arm runs the pinned tool bytes over the round-30 writer briefs and the allow file. Their digests are pinned
in `expected.json`, and a changed input is `snapshot_tampered` (exit 2) before any run. The arm runs the pinned copy,
not `tools/mori-blind-check.sh`, so a later tool edit shows only as a digest difference against `expected.json`
(exit 1). Receipts: `.ufo/waves/round-32/evidence/blind-baseline/`.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| blind-writer gate (r31) | gate | `bash tools/mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>` inside the lane; frozen-run arm `bash .ufo/waves/round-32/frozen/blind-check/verify.sh` | 0 clean (`scanned=N`, `blind_violations=0`) · 1 failed (`blind_violations>0`, one `path:line:rule` per hit; frozen arm: `frozen_run: differ`, also when the pinned tool bytes changed) · 2 could-not-evaluate (usage, invalid lane revision, report directory absent at that revision, unreadable allow file; frozen arm: `snapshot_tampered`) | `bash tools/mori-blind-check.sh --selftest` → prints `PASS`, exit 0; spelling is `--selftest` (no `--self-test` alias); 14 synthetic briefs, expected `scanned=14`/`blind_violations=13` plus 13 exact hit lines pinned in `selftest()` | `.ufo/waves/round-32/frozen/blind-check/expected.json` — sha256 of the 4 round-30 briefs and the round-30 allow file, gate blob sha256 `79b774f7…` (`3c26ef69…`), expected stdout and exit 1 | read-only over the lane tree at the named revision; frozen arm writes only a throwaway git repo under `$TMPDIR`, removed on exit; `--selftest` uses its own `mktemp` tree; never writes the lane | mori |

## Round32 — live recheck of mutable-URL sources (freshness)

Before relying on a `SOURCES.md` row whose URL is not pinned to a tag or commit (a `latest` man page, a docs site, an
API listing), re-open it live and check that the passage it was admitted for is still on the page. Round 32 did this
for the 34 such `mined` rows. 33 still carry their passages and S056 (pnas.org) is behind a bot challenge
(`corpus/lessons/round-32.md` `## Recheck`; method and limits in `corpus/evidence/recheck-r32/README.md`, sources
S175–S177). Tool for the counted check: `python3 .ufo/waves/round-32/count-c1.py <rev>`.

| Situation | What to conclude | What not to conclude | Grounding |
|---|---|---|---|
| a recheck quote is found on the live page and shares words with the row's teaches cell | a candidate only, until a non-author reader confirms the quote supports the teaches cell | that the source still supports the fact: an on-topic sentence or a quote cut inside a word (`protected` out of `unprotected`) passes a token test | Round32 `.ufo/waves/round-32/evidence/c1-controls.txt`; S176, S177 |
| `curl --fail` exits 22, or the server answers 403 with a challenge | the fetch failed for this method: record `unreachable` with the transcript | that the source changed or vanished, or that passing the challenge is an option | Round32 `corpus/evidence/recheck-r32/S056.fetch.txt`; S175 |
| the population URL redirects (S041, S062 to `rfc-editor.org/info/…`) | `--location` saved the final page; the url cell stays the row's URL | that a redirect is drift | Round32 `corpus/evidence/recheck-r32/README.md`; S175 |
| a row's anchor line numbers no longer index the live HTML (S002, S045) | the locator went stale while the passage stayed | that the fact drifted; line anchors into rendered pages are not stable identifiers | Round32 `.ufo/waves/round-32/w1/Recheck002.md`, `Recheck045.md` |

## Round33 — disk write rate from /proc/diskstats (FR6; corpus/knowledge/disk-write-rate-r33.md)

Detection and report only: these rules read counters and never touch a block device setting. Sources S180–S190.

- Round33 rule: read sectors written as field 10 of a /proc/diskstats line of 14, 18 or 20 fields, and convert its delta to bytes by multiplying by 512, never by a device block size (corpus/knowledge/disk-write-rate-r33.md rows 1 and 8).
- Round33 rule: a rate needs two readings and counts completed writes only; a counter lower in the newer reading marks that interval unavailable, and the since-boot average is never the current rate (corpus/knowledge/disk-write-rate-r33.md rows 2, 4 and 13).
- Round33 rule: total a host's writes over whole-disk lines or over partition lines but never both; a dm-N line repeats its backing device's writes on this host (observed, unsourced), so leave stacked devices out of a host total too (corpus/knowledge/disk-write-rate-r33.md row 3 and Host observation).
- Round33 rule: report the in-flight value (field 12) as the queue depth at the read and never subtract two readings of it; report the io_ticks delta over elapsed time as busy share, never as throughput; never present write ticks over elapsed time as a percentage (corpus/knowledge/disk-write-rate-r33.md rows 5, 6 and 7).
- Round33 rule: leave discarded sectors out of a write rate, read flush counts from whole-disk lines only and never add them to sectors written (corpus/knowledge/disk-write-rate-r33.md rows 10 and 11).
- Round33 rule: a missing partition line, a missing discard or flush field, or an iostat 0.0 is unavailable or unknown, never a zero write rate; parse /sys/block/<dev>/stat and /proc/diskstats with one routine over the 17 statistics (corpus/knowledge/disk-write-rate-r33.md rows 8, 9, 12 and 14).

Round33 correction to the Round32 section above: under the round-32 frozen definition (one page, the whole teaches
cell) five of the 33 `current` rows are not current on their population page alone (S058, S117, S128, S149, S137);
the clause-level recheck is in `corpus/lessons/round-33.md` (Round-32 repair).

## Round34 — two-sample disk write rate tool (FR6; tools/mori-disk-rate.py)

Detection and report only: the tool reads two `/proc/diskstats` samples and `/sys/class/block`, and writes nothing.
Sources S180–S198; the frozen rules R1–R7 are in `.ufo/waves/round-34/contract.md` §C1.

- Round34 rule: for a current write rate run `python3 tools/mori-disk-rate.py --interval-ms N` (live: read, wait N ms, read again) or add `--a FILE --b FILE` for two saved samples; never report the census's since-boot average as that rate (corpus/knowledge/disk-write-rate-r33.md row 13r).
- Round34 rule: classify a device from `/sys/class/block/<name>` in this order: no directory → unknown; a `partition` entry → partition (S191); a non-empty `slaves` directory → stacked (S192); a `device` entry → disk (S193); otherwise virtual, as a zram disk registered without a parent (S194; sysstat also calls a device without a `device` link virtual, S195).
- Round34 rule: a device's state is bad-line, absent, gone, new, reset or ok, in that precedence; only an ok device has a rate, `(B − A) × 512 × 1000 // interval_ms` bytes per second, and every other state reports null, never zero (corpus/knowledge/disk-write-rate-r33.md rows 4 and 9).
- Round34 rule: the host total sums the disk class only and is null unless every disk is ok; partitions are already inside their disk (row 3r) and a stacked device maps onto devices already counted (S192).

Round34 correction to the Round33 section above (append-only; round-33 spot-check §8 items 2 and 4): the Round33 rules
that cite rows 3, 6, 7 and 13 rest on the revised rows 3r, 6r, 7r and 13r (`corpus/knowledge/disk-write-rate-r33.md`
§Round-34 revision), which cite every source they need. The iostat clause of the last Round33 rule is narrowed to row
14: an iostat extended-statistics write-sector value of 0.0 does not by itself show an unchanged counter, because
iostat prints 0.0 when the newer sectors-written count is below the older one; read the raw counters before reading
that 0.0 as anything. An idle device also shows 0.0 [INFERENCE, closure §8 item 4], so 0.0 alone is neither a zero
rate nor an unavailable one.

Round35 corrections to the Round34 section above (append-only; `corpus/lessons/round-34-verifier-spotcheck.md` §6 items 2
and 4):
- Round35 correction: the class rule's `device` entry (S193) now rests on S202, which supersedes S193 append-only: on add
  and on delete the link exists only when the device has a parent and the device itself is not a partition, and a
  reparent moves it with no partition check. The `__add_disk` lines round 34 added to S182 in place now rest on S201, which supersedes S182.
- Round35 correction: the host-total clause "a stacked device maps onto devices already counted (S192)" is miscited.
  S192 supplies only the `slaves` classification. The clause is observed on this host, not sourced: a dm-0 write-sector
  delta equalled its slave partition's and its disk's (219728 sectors over 30 s,
  `.ufo/waves/round-34/wb/ExecStackedRemeasure.md`). Round 35 opened seventeen files and none states it; S203 and
  S204 are kept as rejected rows (sweep: `corpus/lessons/round-35.md` Gate). Do not sum a stacked device with its
  slaves; why the backing line also moves stays FR6 frontier.

## Round36 — source drift probe, SOURCES append-only gate, index check

- To see whether a source row's committed copy still matches its URL, run `python3 tools/mori-source-drift.py --root .`
  (network, read-only). Read `drifted` as "the copy is not reproducible from today's body", never as a changed
  source: annotated excerpts (round 30, S156–S160), rebuilt doc pages (S176, S177), post-copy line changes that miss
  the taught passage (S210, stylesheet/script-integrity line), and fetch-varying pages (S211, csrf meta — never
  `fresh`) all classify `drifted` with the source's taught claim unchanged; the dated nine-row enumeration with
  commands and open-time shas is in `corpus/knowledge/source-drift-r36.md`. The action per state is there.
- Before landing any `corpus/SOURCES.md` change, run `python3 tools/mori-sources-appendonly.py <tip> --round-base
  <entering tip>` and land only with `round_changed=[]` (exit 0). It lists in-place edits (`ids`), deleted rows
  (`deleted`) and superseders; a superseder is a disposition, not a discharge (QUALITY 102, 104). The
  `supersede_timing superseded_as_of=[...] stale_supersede=[...]` line (round 38) separates a disposition that
  postdates the edit from one that predates it; a stale entry is a gate finding, not a discharge (QUALITY 110).
  Round 39 makes "postdates" the reachability relation — `git merge-base --is-ancestor` between the id's last
  first-parent-derived edit and the superseding row's landing commit, on a `--full-history` walk that carries
  parent hashes (P-C9, QUALITY 112, S227); `round_changed` derives from first-parent edit detection. It
  replaces the round-35 wave script `.ufo/waves/round-35/check-sources-appendonly.py` as the active check.
- After every lane helper commit, run `bash tools/mori-index-clean.sh <lane>`: exit 1 means a staged path or an
  intent-to-add entry (`git add -N`) is in the lane index (QUALITY 103). `git diff --cached` does not list
  intent-to-add entries; the tool reads porcelain v1 and v2 and refuses a verdict when they disagree.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| source drift (r36) | probe | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` (rows may be `unavailable` or `no-copy`; not proof every URL was reachable) · 1 `drifted>0` · 2 could-not-evaluate (SOURCES.md missing or unreadable) | `python3 tools/mori-source-drift.py --selftest` (offline 127.0.0.1 fixture) | newest copy `corpus/evidence/sources-r<N>/<id>.<ext>` per row; live URL bodies | none (read-only; self-test temp dir removed) | mori |
| SOURCES append-only (r36) | gate | `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]` | with `--round-base`: 0 `round_changed=[]` · 1 non-empty; without: 0 no `ids` and no `deleted` · 1 otherwise; 2 git or parse error | `python3 tools/mori-sources-appendonly.py --selftest` (9 sandbox histories through the CLI, incl. supersede-before-edit) | git history of `corpus/SOURCES.md`; immutable = every column but status, recheck, used-by | none (read-only git; self-test temp dir removed) | mori |
| index clean (r36) | gate | `bash tools/mori-index-clean.sh <repo>` | 0 `staged=0 intent_to_add=0` · 1 staged or intent-to-add entries (≤20 paths listed) · 2 usage, not a repo, git error, or porcelain v1/v2 disagreement | `bash tools/mori-index-clean.sh --selftest` (clean, `add -N`, `add`, not-a-repo) | the repo's git index | none (`--no-optional-locks`; self-test temp dir removed) | mori |
| source drift (r37) | probe | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` · 1 `drifted>0` · 2 setup error; `unavailable` covers a refused redirect and an over-cap body (never `drifted`) | `--selftest` → `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` incl. named arms `huge_cap`, `redirect_private_refused` | `FETCH_MAX_BYTES = 4 * 1024 * 1024` (read +1); `if not _public_redirect_target(final):`; mutants `1<<40` and `if False:`; entry S221–S225 + commit `1caa242`; receipts `c2-after*.txt`, `drift-live-r37*.txt`; pin `freeze-r37-v3.txt` | none (read-only) | mori |
| C1 counter challenge arm (r37) | probe | `python3 .ufo/waves/round-37/count-c1.py <rev> [--repo DIR] [--tool FILE] [--negatives DIR] [--seed N]` | 0 `C1=met` · 1 `C1=unmet` (incl. `tool_timeout`) · 2 setup error | none (the three negative fixtures are the able-to-fail evidence) | `PREDICATE` as printed; `REAL_REV=6bd57097`, `REAL_BASE=f10a320d`; challenge title = the lane title; drawn-rev arm; fixture blobs; pin `freeze-r37-v3.txt` | scratch inside the lane tree (`.ufo/waves/round-37/scratch`) | mori |
| content-anchor check (r38) | probe | `python3 .ufo/waves/round-38/count-c4.py <rev> [--repo DIR]` | 0 `C4=met` · 1 `C4=unmet` · 2 setup error | none (the three fabricated witnesses under `.ufo/waves/round-38/fixtures/` are the able-to-fail evidence; the mutation arm `drift_kill` is a check) | `anchor:` entry lines resolved in `tools/mori-source-drift.py`; repo-relative capability paths; `row_states` arm; `return "drifted"` mutated to `return "excerpt"` | none (read-only; scratch under `.ufo/waves/round-38/scratch`) | mori |
| counter conformance (r38) | gate | `python3 .ufo/waves/round-38/conform.py <rev> [--counter PATH]... [--selftest]` | 0 `CONFORM=met` · 1 unmet · 2 setup error | `--selftest` (six mutations, each flips exactly its own check) | contract P-C1 bytes; `head_at_measurement`; lane-relative `--tool`; bounded reads; `tool_timeout` state; lane scratch parent | read-only (runs the counter under test) | mori |
| fabricated-content check v2 (r39) | probe | `python3 .ufo/waves/round-39/count-c7.py <rev> [--repo DIR] [--seed N]` | 0 `C7=met` · 1 `C7=unmet` · 2 setup error | none (the four fabricated witnesses under `.ufo/waves/round-39/fixtures/` are the able-to-fail evidence; `drift_kill_v2` uses a run-time-drawn post-state) | `anchor:` lines ≥8 chars at non-comment positions in `tools/mori-source-drift.py`; capability paths resolve to blobs; receipt rows have committed `sources-r<N>` copies; got-vs-want table diff | none (read-only; scratch under `.ufo/waves/round-39/scratch`) | mori |
| counter conformance v2 (r39) | gate | `python3 .ufo/waves/round-39/conform.py <rev> [--counter PATH]... [--selftest]` | 0 `CONFORM=met` · 1 unmet · 2 setup error | `--selftest` (nine mutations, each flips exactly its own check) | contract P-C7 bytes; `head_at_measurement`; lane-relative `--tool`; bounded child runs; folded timeout values; used-`communicate` drains; `tool_timeout` state; lane scratch parent; communicate-timeout conjunct | read-only (runs the counter under test) | mori |
| counter conformance v3 (r40) | gate | `python3 .ufo/waves/round-40/conform.py <rev> [--counter PATH]... [--selftest]` | 0 `CONFORM=met` · 1 unmet · 2 setup error | `--selftest` → `CONFORM_SELFTEST pass=11 fail=0` (eleven mutations; `timeout_scope_shadow`, `drain_bind_decoy` and the checker's own-mutation-table `selftest_conjunct` added; per-counter `comm_violations`) | contract P-C10 bytes; scope-aware timeout resolution (function-local shadow, `global`, conditional rebind, finite-positive fold); per-Popen `communicate` drain binding with consumed result | read-only (runs the counter under test) | mori |
| SOURCES append-only timing (r38) | gate | `python3 tools/mori-sources-appendonly.py <rev> --round-base REV` | summary exit as before; the extra line `supersede_timing superseded_as_of=[...] stale_supersede=[...]` is the finding | `--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` (re-measured round 47 by `tools/mori-pin-check.py`: the round-40 bytes at `265a955c` print `pass=15`, the round-41 freeze `d72ac167` added seven arms and the pin was not updated; round-40 v3: P-C11 — eligible set is every superseded id present at R, never-edited ids test as-of against their first-sighting commit; an edit compares against the first parent's own state only, so a first-parent-lacks-path merge contributes no edits and a linear delete-then-re-add contributes no changed event; r39 closure routed defects 1–4 and lesson findings 2/5) | latest-superseder landing vs last immutable-edit (or first-sighting) commit reachability over the `corpus/SOURCES.md` history | none (read-only git) | mori |

## Round47 — registry pin reconciler and the OOM tracepoint catalogue counter

`tools/mori-pin-check.py` replaces round 46's row-wide substring counter
(`.ufo/waves/round-46/count-repins.py`, retired as a calibration proof: it turned green when a
stale receipt string moved to another cell, `corpus/lessons/round-46.md` M1). It reads pins only
from each gate table's `self-test` cell, re-runs the bound `--selftest` command inside a
`git archive` export of the measured revision, and checks full sha256 pins against the files the
row names. Run it before landing any round that edits a registry row or a registered tool.

v2 (landed the same round, after wave-1 seats turned the frozen v1 green on junk edits —
`.ufo/waves/round-47/w1/CritC1Predicate.md` v2/v3/v7/v8, `w1/SentPinExec.md`): a bound command
must be `<interpreter> [-I] [-B] <tools/… or .ufo/waves/round-N/… path> [<rev>] --selftest`
(no inline `-c`, no `.scratch/`, no `..`), a pin's bound command may not differ from the
`--baseline-rev` binding (`rebound`), the pinned text must equal the observed text on the lines
that start with the prefix (all such lines must agree, so a `compat:` echo of an old tally is
ignored), row names are unique, a short row naming `selftest` in any case is `unparsed`, fenced
example tables are not read, the entry column comes from the header, and digest paths stay
inside the measured tree (w1 `RevPinCheckCode.md` M1/M3/L1 closed the same round). The seven
junk variants score unmet under v2 and the honest repair met (`.ufo/waves/round-47/evidence/v2/`).
The round-47 claim itself is scored with the frozen v1 bytes
(`git show 63eecf27:tools/mori-pin-check.py`).

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| registry pin reconciler (r47, C1) | gate | `python3 tools/mori-pin-check.py --rev <rev> [--repo DIR] [--min-tally-pins N] [--baseline-rev REV] [--skill PATH] [--timeout S] [--scratch DIR]` (`--root DIR` measures a directory as-is; v5, round 51: the `--rev` tree is a `git clone --shared` with `master` at the revision, under `--scratch`, else $TMPDIR, else /var/tmp — never under the repo: a `--scratch` inside it exits 2) | 0 → `PIN_CHECK=met` (mismatches=0, unparsed=0, no_command=0, dropped=0, rebound=0, duplicate=0, hidden=0, misattributed=0, env_unexpanded=0, tally pins ≥ N) · 1 → `PIN_CHECK=unmet`, one `pin … state=mismatch\|unparsed\|no_command\|dropped\|rebound\|duplicate\|hidden\|misattributed\|env_unexpanded` line per finding; every mismatch line ends `class=env` (no tally line, or the pinned tally then a timeout: the instrument could not run here) or `class=stale` (a different tally, disagreeing tally lines, an absent instrument file, a contradicting exit code, a digest or line-count pin), and the summary ends `env=N stale=N` (v5/v5.1, round 51) · 2 → `PIN_CHECK_SETUP` (no `--rev`/`--root`, unresolvable revision or baseline, unreadable SKILL) | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=125 fail=0` | round-47 floor `--min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53` (`.ufo/waves/round-47/contract.md` P-C1); v3 (round 48, section below) reads line-count pins and truncated digests in self-test cells, accepts the `selftest` and `self test` header spellings, counts hidden rows, rejects non-ASCII prefixes, rebinding to another argv for a baseline prefix and a digest decoy file named elsewhere in the row (`.ufo/waves/round-48/v3-spec.md`); v4 (round 49, section `Round49` below) reads a row as a reader sees it (F1-F5), binds a pin to the instrument its own cells claim (R11), applies env prefixes (K2/K8), and counts deleted line-count and truncated-digest pins and an unpinned reconciler (R12-R14) | its own export and TMPDIR under `<repo>/.scratch` (removed on exit); runs the registered selftests, which write only their own temp dirs | mori |
| r47 tracepoint catalogue (C2) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met events=8 rows=8 …` · 1 → `C2=unmet … failed=<checks>` (entry absent, provenance, table, name/field/call-site mismatch, pin mismatch, source row) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | sha256 of the four v7.2 copies under `corpus/evidence/sources-r47/` (in-script `PINS`); `ROW_ID = "S475"`; entry `corpus/knowledge/oom-tracepoints-r47.md` | none (read-only `git show`) | mori |

## Round48 — pin reconciler v3, the junk-variant counter, the quota entry and the unlanded check

`tools/mori-pin-check.py` is v3. After round 47's closure found that a v2 `met` could still be produced
by structural junk (`.ufo/waves/round-47/w2/CritV2Junk.md` FG1–FG5, O1), the claim is scored by a counter
that carries the junk next to honest edits: `.ufo/waves/round-48/count-c1.py` rewrites the measured
revision's SKILL.md with eight frozen junk edits (J1 header spelled `selftest`, J2/J3 fullwidth and
Cyrillic tally prefixes, J4 a stale tally rebound to an archived copy, J5 the gate rows moved into a fence,
J6 a blank line under the header, J7 a line-count pin off by one, J8 a truncated digest off by one) and four
honest edits, runs the tool under test on each and on the real registry, and wants `unmet` on every junk
edit and `met` on every honest edit. A tool that rejects too much fails the honest edits.

v3 rules (`.ufo/waves/round-48/v3-spec.md` R1–R8, plus R9/R10 from the wave-1 critic
`w1/CritJunkClasses.md`): the self-test header is recognised case-insensitively (`self-test`, `selftest`,
`self test`); a row-shaped line outside a parsed table that carries an ASCII `*SELFTEST` token or
`--selftest` is `hidden`, fenced or not; a tally-looking token in another cell of a parsed row or on a
continuation line under a row is `hidden`; a backticked span with a non-ASCII first token or a casefolded
`selftest` prefix, or a tally outside backticks, is `unparsed`; a baseline prefix bound to another argv is
`rebound`; `(N lines)` pins and truncated digests `hex{8,63}…` are read in self-test cells; every digest
binds to the nearest preceding in-tree path of its own cell, so a decoy file named elsewhere in the row no
longer matches. Known survivor, not closed: a row that names instrument A in its entry cell while its
self-test cell runs instrument B (`w1/CritJunkClasses.md` D7); closing it as a rule turns three legitimate
mutant-command rows (190, 191, 192) red, so it is a limit.

`tools/mori-unlanded-check.py` lists every file under `.ufo/waves/round-N/`, `corpus/`, `tools/` or at the
top level that is untracked, modified or staged, so a late seat result cannot sit off the record at report
time (round-47 routed defect 1). Run it before filing a report:
`python3 tools/mori-unlanded-check.py --repo . --round N`.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r48 junk-variant counter (C1) | gate | `python3 .ufo/waves/round-48/count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] [--min-tally N] [--jobs N] [--scratch DIR]` | 0 → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` · 1 → `C1=unmet …` with one `variant name=… expect=… got=… rc=…` line each · 2 → `C1_SETUP` (usage, unresolvable revision, SKILL.md unreadable, a variant anchor absent at R) | `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` | `BASELINE` 2d85e33d…, `MIN_TALLY` 26, variants J1–J8/H1–H4 as functions in the counter; controls `.ufo/waves/round-48/controls/` | the tool under test writes only under `--scratch` | mori |
| r48 quota entry counter (C2) | gate | `python3 .ufo/waves/round-48/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S …` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-48/count-c2.py --selftest` → `C2_SELFTEST pass=22 fail=0` | sha256 of the four copies under `corpus/evidence/sources-r48/` (in-script `COPIES`); `OPENED` 2026-10-25; quote 6–25 words; limit: a located quote does not prove the claim follows from it | none (read-only `git show`) | mori |
| unlanded check (r48) | gate | `python3 tools/mori-unlanded-check.py --repo DIR --round N` | 0 → `UNLANDED=clean round=N` · 1 → `UNLANDED=dirty round=N paths=K` and one `unlanded XY path` line per path (≤50) · 2 → `UNLANDED_SETUP` (usage, not a repository top level) | `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=17 fail=0` | scope `.ufo/waves/round-N/`, `corpus/`, `tools/`, top-level `*.md`; `.scratch/` and ignored files are outside it; `--repo` must be a top level | none (`git status --no-optional-locks` only) | mori |

### Decision row — FR2 filesystem quota (round 48)

| situation | do | do not | source |
|---|---|---|---|
| a workload reports `Disk quota exceeded` or errno EDQUOT | read it as a per-id limit; read accounting and enforcement separately (`xfs_quota -x -c state` on XFS), treat `ESRCH` as quotas off, not zero | read `df` capacity as the cause; copy errno 122 into a probe (MIPS 1133, SPARC 69) | `corpus/knowledge/quota-observability-r48.md` (S479–S484) |

## Round49 — the opaque-handle junk-variant counter, reconciler v4 and the journal-reach entry

Round 48's counter could be passed by a tool that keyed on the harness's variant file names
(`corpus/lessons/round-48-verifier-spotcheck.md` §5 item 3; round-48 `w1/CritC1Counter.md` F1).
`.ufo/waves/round-49/count-c1.py` hands every variant to the tool under an opaque name: the SKILL.md copy and
its scratch directory are named by a sha256 prefix of their bytes, the run order follows that hash, and the two
edits that change a second tracked file (N10 a stale pin, H5 a pin moved with its instrument) are built in a
throwaway fixture repository. It scores eighteen junk edits (round 48's J1–J8 and the new N1–N10), seven honest
edits (H1–H7) and the real registry read twice, every run with `--min-tally-pins 26 --baseline-rev 2d85e33d…`.
Its limits are named, not closed: the handle is a function of the variant bytes, so a tool that recomputes it
(or stats the sibling copies) can still read the order — `w1/CritC1Counter.md`; the counter's selftest runs a
text-only twin of `plan()`, not the production staging path — `w1/MutC1Counter.md` F1.

`tools/mori-pin-check.py` is v4. It keeps R1–R11 and adds: F1 a claim split from its row by a blank line is
still `hidden`; F2 the self-test header and the verdict-map column are matched after NFKC and zero-width
deletion; F3 any indentation is a row shape for the hidden scan; F4 `<tr`/`<td` markup is a row shape; F5 two
rows binding one `(prefix, argv)` must agree on their stated exit-code contract; K2 `VAR=value` prefixes are
applied (`env_unexpanded` when a value cannot be); K8 a PASS-form pin is checked against the exit code; K5 a
`C1/C2/C3_SELFTEST` namespace join is limited to the instrument's own family; X1 a vanished baseline binding is a
`no_command` finding, not a traceback; R12 a deleted line-count or truncated-digest pin is `dropped`; R13 a tree
that ships the reconciler must pin it; R14 a line-count pin binds the instrument the row runs. Still open:
K4 (pins outside the self-test cell), the `fixtures/mutants` carve-out of R11, and a content-keyed digest check
(`tools/mori-pin-check.py` docstring, R12–R14). Run it before landing any round that edits a registry row or a
registered tool; edit the reconciler's own row (the `PIN_CHECK_SELFTEST pass=N` pin above) in the same commit
as the tool.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r49 opaque-handle junk-variant counter (C1) | gate | `python3 .ufo/waves/round-49/count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] [--min-tally N] [--jobs N] [--scratch DIR]` | 0 → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` · 1 → `C1=unmet …` with one `variant name=… expect=… got=… rc=…` line each · 2 → `C1_SETUP` (usage, unresolvable revision, SKILL.md unreadable, a variant anchor absent at R) | `python3 .ufo/waves/round-49/count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0` | `BASELINE` 2d85e33d…, `MIN_TALLY` 26; variants J1–J8 (imported from round 48), N1–N10, H1–H7 as functions in the counter; controls `.ufo/waves/round-49/controls/` | the tool under test writes only under `--scratch` and the fixture repository it is pointed at | mori |
| r49 journal-reach entry counter (C2) | gate | `python3 .ufo/waves/round-49/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok provenance=ok` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-49/count-c2.py --selftest` → `C2_SELFTEST pass=26 fail=0` | sha256 of the four copies under `corpus/evidence/sources-r49/` (in-script `COPIES`); `OPENED` 2026-10-25; quote 6–25 words; limit: a located quote proves the words occur in the copy, not that the claim follows from them | none (read-only `git show`) | mori |

### Decision row — journal reach (round 49)

| situation | do | do not | source |
|---|---|---|---|
| a journal query's window starts before the oldest retained record (`journalctl --list-boots` first entry, or a `--since` older than it) | read the window as **not retained** and state the reach: the oldest retained boot entry, the configured ceilings from `systemd-analyze cat-config systemd/journald.conf`, and `journalctl --disk-usage` as a dated total | read the silence as host quiet or a failed probe; read a `--disk-usage` total as an event count or a per-journal share; read an empty `/run/log/journal` as "no journal" (a flush moves the boot's records to the persistent store); vacuum or rotate to widen the reach | `corpus/knowledge/journal-reach-r49.md` (S485–S488) |

## Round50 — the calibration counter and the memcg report-block entry (attempt 2)

Round 49's spot-check routed defect 2 — the 114/114 and 17/17 tallies were prose only — and the lane's K4 class
(a pin outside the registry's self-test cell), and round 50 puts both claims on a lowest axis (depth, freshness and
calibration tied at 5; freshness is untouched). Attempt 1 froze the predicates and counters at `950e99be…` and died
in a host crash; attempt 2 landed the data at `487941b9…`. The counters stay frozen: a counter weakness found after
scoring is a named limit, never a repair.

`.ufo/waves/round-50/count-c1.py` (calibration) scores the lane's self-assessment against the fleet record and the
instruments. For each of the six `SCORECARD.md` `## Axes` rows the Last change cell's first `round N` must be the
highest admitted mori round at or before 49 that the fleet `MANIFEST.json` at `e0144996…` grades `improved` or
`harmed` on that axis, the text from that `round N` to the next `;` must name that round's verdict word, and the
Evidence cell must cite that round's spot-check when the file exists at R, else `MANIFEST.json`. Every `SHONEN.md`
tally pin must be a backticked `python3 <path> --selftest` span followed by `(N/M)` or `-> PREFIX pass=N fail=K`,
re-run at R with `git archive`, matching its tally, with a receipt under `.ufo/waves/round-50/evidence/selftests/`
and no stray tally token elsewhere in the file; the floors are 2 pins and 4 boxes. Entering `7197160b` it read `mismatches=6`
(`.ufo/waves/round-50/evidence/control-c1-do-nothing.txt`); at `487941b9…` it reads
`C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d`. Eight controls carry
the reason classes: do-nothing 6, blanket all-latest 6, pins deleted `pins_floor`, corrected number without a
receipt 6, axes-only 2, SHONEN-only 4, box dropped `boxes_floor`, and a witness that is feasibility only. Named
limits: the Score column is not checked (the MANIFEST holds verdicts, not scores); the MANIFEST is trusted, not
re-judged; the hidden-tally scan enumerates `SHONEN.md` only; and a matching tally proves the instrument prints it
at R, not that its arms are good.

`.ufo/waves/round-50/count-c2.py` (depth) scores `corpus/knowledge/oom-memcg-stat-r50.md` against the three frozen
copies under `corpus/evidence/sources-r50/`: at least 10 claim rows, each claim cell 6+ words, unique, carrying 3
words its own quote does not; one mined `SOURCES.md` row per claim, opened 2026-10-26, naming its URL among the
three copies and citing the entry; one backticked 6–25-word quote per row located in that row's copy; all three
copies drawn on and every copy sha256-pinned. At `487941b9…` it reads
`C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok`; entering
`7197160b` it failed with `entry_absent`. Named limits: a located quote proves the words occur in the copy, not
that the claim cell follows from them; the beyond-quote word floor is a floor, not entailment; v7.2 says nothing
about later kernels or cgroup v1; and no host OOM block was read (the no-MESSAGE-grep lane rule), so the entry
states what the kernel prints, not what a past kill on this host printed. Both selftests re-run 2026-10-26:
`C1_SELFTEST pass=34 fail=0` and `C2_SELFTEST pass=31 fail=0`.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r50 calibration counter (C1) | gate | `python3 .ufo/waves/round-50/count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] [--scratch DIR] [--timeout S]` | 0 → `C1=met items=N axes=6 pins=P boxes=B mismatches=0 errors=0 hidden=0 manifest=<sha12> rev=R` · 1 → `C1=unmet … failed=<reasons>` with one `item` line per axis and pin (expect/got/state) · 2 → `C1_SETUP` (usage, a missing option value, an unresolvable revision on the lane or the fleet repo) | `python3 .ufo/waves/round-50/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` | `FLEET_REV` e0144996…, `THROUGH` 49, `MIN_BOXES` 4, `MIN_PINS` 2, `RECEIPT_DIR` `.ufo/waves/round-50/evidence/selftests/`; limit: the Score column is unchecked and the fleet MANIFEST is trusted | none (read-only `git show` / `git cat-file` / `git archive`; the archive is extracted under `--scratch` and removed) | mori |
| r50 memcg report-block entry counter (C2) | gate | `python3 .ufo/waves/round-50/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-50/count-c2.py --selftest` → `C2_SELFTEST pass=31 fail=0` | sha256 of the three copies under `corpus/evidence/sources-r50/` (in-script `COPIES`); `ENTRY` `corpus/knowledge/oom-memcg-stat-r50.md`; `OPENED` 2026-10-26; claims floor 10; quote 6–25 words with 3 words beyond it | none (read-only `git show` / `git rev-parse`) | mori |

### Decision row — memcg OOM block (round 50)

| situation | do | do not | source |
|---|---|---|---|
| a burst carries a usage line, a `Memory cgroup stats for <path>:` block and `Killed process` lines, and their numbers are compared | convert first: the usage and swap lines and the `Killed process` fields are kB, the `Tasks state (memory values in pages)` table is pages except `pgtables_bytes` in bytes, the block prints its charge amounts (`anon`, `file`, `shmem`, `kernel`) in bytes and its `workingset_*`, `pgscan*`, `pgsteal*` keys as counts | compare a block key with a victim-line figure as if both were kB, or read a `workingset_*` count as a byte amount | `corpus/knowledge/oom-memcg-stat-r50.md` (S489–S491) |
| the stats block is read | look keys up by name; read a missing `zswap`, `zswap_incomp`, `anon_thp` or `hugetlb` as not printed under this build's CONFIG (`hugetlb` also at run time), never as zero | index the block by line position, or read a short block as a low charge | `corpus/knowledge/oom-memcg-stat-r50.md` (S489–S490) |
| the block's bytes are totalled | keep `anon`, `file` and `shmem` distinct, and count `kernel_stack`, `pagetables`, `percpu`, `vmalloc` and `slab` once, inside `kernel` as the documentation defines it | add `file` to `shmem` (shmem is the swap-backed part of file), or add the five sub-keys to `kernel` a second time | `corpus/knowledge/oom-memcg-stat-r50.md` (S489) |
| the kill is attributed to a cgroup | read the block as the charged cgroup's charge, aggregated over the cgroup and its descendants, and the `Killed process` counters as the victim's own; read `oom_memcg=` and `task_memcg=` as two labels that can differ when hierarchy is enabled | infer the victim's usage from the block, or read the victim's own cgroup as the cgroup whose limit was hit | `corpus/knowledge/oom-memcg-stat-r50.md` (S490–S491) |
| victim lines print with no stats block, or a group kill is read | read the summary as rate-limited and the victim line as not; order a group kill as the selected victim's line, then `Tasks in <path> are going to be killed due to memory.oom.group set`, then a line per further kill, and keep `oom_kill` (processes) apart from `oom_group_kill` (group events) | read a missing block as proof the kill was global, or expect a line for a process that only shared a victim's mm | `corpus/knowledge/oom-memcg-stat-r50.md` (S491) |

## Round51 — the operability counter, the MemAvailable entry and the pin mismatch classes

Round 50's spot-check routed two defects into round 51: §5 item 1 / D-d — `tools/mori-pin-check.py` exported its
`--rev` tree under `<repo>/.scratch`, so a SIGKILLed run left 12547 paths in the repo it reads, and
`.ufo/waves/round-40/conform.py:69` hardcoded the lane path, so a re-execution off-host died as a setup error — and
§5 item 4 — a depth counter that scored where a quote sits and not what it says. Round 51 works operability and
depth on both, freezes its counters at `4677910e…` and lands the data at `87e0c374…`. Pin-check v5 measures a
`git clone --shared` checked out at the revision under `--scratch` (else a TMPDIR outside the repo, else /var/tmp) instead of a `git archive` under the repo
(the scratch-only control reads `reloc_mismatch=3` in `evidence/control-c1-scratch-only.txt`: the export cannot
simply leave the tree — the lane's relocation witness found two pinned instruments and `conform.py` read git
objects from the tree they run in), and it tags every mismatch line `class=env` or `class=stale`; `conform.py`
derives the lane from its own path and takes its selftest scratch from TMPDIR. At the data commit `87e0c374`
`.ufo/waves/round-51/count-c1.py` read `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok
selftest=pass=119,fail=0 failed=-` (after the wave, v5.1 adds six selftest arms — 125 — and the landed-tip line
is in `.ufo/waves/round-51/evidence/c1-at-landed.txt`); entering `aa3af1ec` the same counter read `C1=unmet kill_residue=12547
relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0
failed=kill_residue,relocated,classified`. The counters, predicates, controls and kill rules stay frozen: a
counter weakness found after scoring is a named limit, never a repair.

`.ufo/waves/round-51/count-c1.py` (operability) runs four arms at R. A: a `--rev` run in a fresh `--no-local` clone
is SIGKILLed 3 s after that run starts writing, and the clone it read must show 0 lines in
`git status --porcelain --ignored --untracked-files=all`. B: a second fresh clone runs pin-check under bubblewrap
with the lane working-tree path on a `--tmpfs`, and the run must exit 0 with a last line starting `PIN_CHECK=met`.
C: R's pin-check over a frozen five-row fixture registry must class the two no-tally pins `env`, the different-tally
pin and the rc-contradicting pin `stale`, leave the matching pin unclassed, and end ` env=2 stale=2`. D: R's own
pin-check selftest must exit 0 with at least 114 arms. The counter has no selftest of its own — `--selftest` is an
argparse usage error (exit 2) — so its controls carry that job: the five under `.ufo/waves/round-51/controls/`
(receipts `evidence/control-c1-<name>.txt`). The always-env control is the one that keeps the classifier honest:
a tool that says env for everything reads `failed=relocated,classified,selftest`.

`.ufo/waves/round-51/count-c2.py` (depth) scores `corpus/knowledge/memavailable-estimate-r51.md` against the five
frozen copies under `corpus/evidence/sources-r51/`: at least 12 claim rows, each claim cell 6+ words, unique, and
carrying 3 words its own quote does not; one mined `SOURCES.md` row per claim, opened 2026-10-26, naming its URL
among the five copies and citing the entry; one backticked 6–25-word quote per row located in that row's copy; all
five copies drawn on and sha256-pinned; and — the entailment arm that closes §5 item 4 — for every row a non-L1
wave report under `.ufo/waves/round-51/w1/` records the judgment for that exact claim text, with no dissent. At the
data commit it reads `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok
provenance=ok entailed=0 dissent=0 failed=entailment`: every quote is located and no seat has judged them yet. Its
selftest carries the entry-level controls plus the arm's eight (no votes, one row unreviewed, dissent, L1-authored
vote, vote in another directory, vote on other text, non-markdown file, whitespace folding).

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r51 operability counter (C1) | gate | `python3 .ufo/waves/round-51/count-c1.py <rev> [--repo DIR] [--hide PATH] [--scratch DIR] [--keep]` (`--hide` is the path bubblewrap hides, default the lane; `--scratch` must lie outside the source repo) | 0 → `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=N,fail=0 rev=<full> failed=-` · 1 → `C1=unmet … failed=<arms>` (kill_residue, relocated, classified, selftest), plus a `kill_residue_first:` line and the classifier's `prefix=` lines and summary echoed as `classified:` lines · 2 → argparse usage error, or `C1_SETUP <reason>` (unresolvable revision, scratch inside the source repo) | no mode of its own: `--selftest` is an argparse usage error (exit 2); the arms are exercised by the five controls in `.ufo/waves/round-51/controls/` (receipts `evidence/control-c1-<name>.txt`), and arm D pins R's pin-check selftest at ≥ 114 arms | `ENTERING_SELFTEST` 114; the five-row fixture registry (`enva`/`envb` → env, `stla`/`stlb` → stale, `okay` → match) and the ` env=2 stale=2` summary are in-script; the kill lands 3 s after the first write; limits: one kill moment, one hidden path (the lane), five fixture rows, and a tool that prints a tally then fails for an environmental reason is classed stale | scratch only: `--scratch DIR` (default a `mkdtemp` under TMPDIR) is refused inside the source repo and removed on exit unless `--keep`; each arm clones the repo fresh with `--no-local` and writes nothing into the tree it reads | mori |
| r51 MemAvailable entry counter (C2) | gate | `python3 .ufo/waves/round-51/count-c2.py <rev> [--repo DIR] [--entry PATH]`; `--hashes <rev>` prints each row's 12-hex claim handle | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=N dissent=0 rev=R` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance, entailment) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-51/count-c2.py --selftest` → `C2_SELFTEST pass=34 fail=0` (re-run 2026-10-26; receipt `evidence/selftest-c2.txt`) | sha256 of the five copies under `corpus/evidence/sources-r51/` (in-script `COPIES`); `ENTRY` `corpus/knowledge/memavailable-estimate-r51.md`; `OPENED` 2026-10-26; claims floor 12; quote 6–25 words with 3 words beyond it; the entailment arm reads `.ufo/waves/round-51/w1/` reports whose names do not start `MoriR51` and needs one `ENTAIL <h> entailed` line per row and no dissent; limits: a located quote proves the words occur, a vote proves a wave seat recorded that judgment — neither proves the judgment right — and v7.2 says nothing about other kernels | none (read-only `git show` / `git ls-tree` / `git rev-parse`) | mori |

### Decision row — runway reading (round 51)

| situation | do | do not | source |
|---|---|---|---|
| a seat spawn, a census or a pressure probe wants the host's runway | read the `MemAvailable` line itself and compare it with the dispatcher's floor; read a `MemAvailable/MemTotal` ratio as unit-free | rebuild the figure as `MemFree + Cached`: that sum counts tmpfs and shmem pages, which sit on anon LRU lists and which the estimate does not add | `corpus/knowledge/memavailable-estimate-r51.md` (S492–S495, rows 4, 7, 17, 20) |
| a meminfo figure is converted, or compared with a figure from another surface | read the figures through row 14's helper: a page count shifted by `PAGE_SHIFT - 10` prints kB, and a ratio is unit-free | mix a kB line with a cgroup block's byte amounts or a `Tasks state` page count (the round-50 conversion rule) | `corpus/knowledge/memavailable-estimate-r51.md` (S494, row 14; S489–S491) |
| `MemAvailable` reads 0, or small, while swap is free | read 0 as the formula's clamp, and the figure as having no swap term | read 0 as an exact zero or as proof a kill is imminent; read free swap as counted in the estimate | `corpus/knowledge/memavailable-estimate-r51.md` (S493, rows 1, 12) |
| `Cached` is large while `MemAvailable` is small | compare `Shmem`: tmpfs and shared memory raise `Cached` without raising the estimate | read the gap as cache the host can hand to a new seat, or as headroom the estimate has already counted | `corpus/knowledge/memavailable-estimate-r51.md` (S492–S496, rows 4, 5, 7, 17) |
| a runway threshold goes into a receipt, a report or a gate | report it as local: the estimate withholds min(half the term, the summed low watermarks) from both the file cache and the reclaimable kernel term, and the proc document says its accuracy varies from system to system | state the threshold as a property of `MemAvailable` in general, or recompute the estimate from `/proc/meminfo` alone (`totalreserve_pages` is not exported) | `corpus/knowledge/memavailable-estimate-r51.md` (S492–S493, rows 3, 8, 10, 13; Boundaries) |

### Pin mismatch classes (round 51)

`tools/mori-pin-check.py` v5 (round 51) tags a mismatch with why the pin failed, so an off-host re-execution reads
as what it is: "can't run here" or "the row and the instrument disagree". The rule is the tool docstring's (v5) and
the shape arm C of the round-51 operability counter scores over its fixture registry. The summary line ends
`env=N stale=N`, env + stale = mismatches, and any mismatch leaves `PIN_CHECK=unmet`. The class is a property of
the run, not of the registry: `unparsed`, `no_command`, `dropped`, `rebound`, `duplicate`, `hidden`,
`misattributed` and `env_unexpanded` findings carry no class.

| class | what it means | what the lane does |
|---|---|---|
| `class=env` | the pinned command printed no line starting with its prefix at all — a setup error, a missing path, a timeout, an OS error — or printed the pinned tally and then timed out (v5.1), so the instrument could not run here and the pin says nothing about the measured revision | read it as "can't run here": fix the environment or the instrument's own lane assumption (path, TMPDIR, interpreter, git objects) and rerun there; leave the row's pinned tally as it is — an env mismatch never justifies a re-pin, and rewriting the row to silence env is the false green the class exists to prevent |
| `class=stale` | the command ran and printed a different tally for its prefix, printed disagreeing tally lines (v5.1), its instrument file is absent from the tree (v5.1), printed the pinned tally with an exit code that contradicts it, or a digest or line-count pin does not match the file — the row and the instrument disagree at the measured revision | read it as a disagreement to settle, not a run to retry: either the pin is out of date, and the row and its receipt are edited in the same commit as the tool change (reconcile before landing a round), or the tool regressed, and the tool is fixed; say which in the receipt |

Named limits of the classes, frozen with the counter: a tool that prints a tally and then fails for an
environmental reason is classed stale; a row that binds no command is a `no_command` registry defect rather than
either class; and the class says why the pin failed, never whether the revision is good.
