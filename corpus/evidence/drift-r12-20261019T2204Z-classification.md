# Drift-pin token classification + kill-event host facts — round 12 receipt

- Author: R12Scout (lane L2 seat, read-only); committed by the lane L1. Census bytes: base `20e2255:tools/mori-census.sh` (sha256 d7710981…), baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` (pinned 2026-10-15T22:26:29Z). Measured 2026-10-19T21:59–22:04Z.
- Lane reading: no token is a census regression. 'Yes' rows below mean the *fleet evidence* weakened (souji sweep e20f4fa; aggregator row-B → row-C), not that the gate misbehaved.

**Observation time:** `2026-10-19T22:03:56Z`  
**Axes:** drift-report fidelity; count-only host-evidence coverage.

## A. Drift-pin freshness

I ran `--drift` and the plain census using a copy of `20e2255:tools/mori-census.sh`, not the concurrently edited LANE script. The baseline is pinned at `2026-10-15T22:26:29Z`.

```text
MORI_DRIFT: +FINDING:UNIT_FAILURE_OUT_OF_SCOPE +other_authored_commits -FINDING:KILL_SIGNAL_JOURNAL -FINDING:SEGFAULT_JOURNAL -FINDING:WAVE_UNSETTLED_AGE -attribution -example -rowb_files SURFACE:journal basis obs
```

Exit status: **1**.

Relevant exact lines from the plain census:

```text
SURFACE journal: ok (cmd=journalctl --user -b --no-pager; oom_kill=0 kill_signal=0 segfault=0 unit_failure=3 rc=0; ts=2026-10-19T21:59:45Z)
SURFACE lane.aggregator: progressing-weak (lane=aggregator round=10 launch_epoch=1792039857 age_s=407328 basis=row-C other_authored_commits=137; ts=2026-10-19T21:59:45Z)
MORI_CENSUS: DRIFT (findings=13 drift=12 unavailable=1 surfaces=7)
```

| Token | Cause | Evidence command → output | Regression? |
|---|---|---|---|
| `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE` | Current user-journal census found 3 non-fleet unit failures; the finding is informational and outside fleet scope. Exact event timing within the boot is unknown. | Base plain census → `unit_failure=3`; `FINDING UNIT_FAILURE_OUT_OF_SCOPE ... count=3` | No |
| `+other_authored_commits` | Aggregator evidence changed from row-B to row-C: the current census reports `progressing-weak`, with 137 other-authored commits. | `git -C /home/vgpnk/Projects/shokunin show --stat --format=%H%n%ci e20f4fa \| grep -c 'waves/aggregator-r10'` → `17`; commit `e20f4fa3fd3fc9550641af38da3eddcf3d35f528`, “souji: remove 96 pushed-receipt checkpoint artifacts (operator sweep 2026-10-18).” Its stat includes deletions under both aggregator-r10 wave directories. | Yes—evidence-strength downgrade; no code defect demonstrated |
| `-FINDING:KILL_SIGNAL_JOURNAL` | The pinned finding was boot-scoped. The current boot began after the pin, and the current census sees zero kill-signal matches. | `uptime -s` → `2026-10-19 08:11:44`; `journalctl --user -b -q -o json --output-fields=_BOOT_ID \| wc -l` → 87,486 initially; current census → `kill_signal=0` | No—expected boot-scope change |
| `-FINDING:SEGFAULT_JOURNAL` | Same new-boot scope; current census sees zero segfault matches. | `uptime -s` → `2026-10-19 08:11:44`; base plain census → `segfault=0` | No—expected boot-scope change |
| `-FINDING:WAVE_UNSETTLED_AGE` | The finding-ID set changed. Baseline had 11 IDs: `aggregator-r10`, `aggregator-r10-resume`, five `shokunin12h-20261014-*` IDs, and four `shokunin-train-20261013*` IDs. Live had 10: the same five and four non-aggregator IDs, plus `shokunin-train-20261016-w24`. The old aggregator directories no longer contain the registry/dispatch/run markers used by the probe; empty directories are not counted as unsettled. **Their disappearance does not prove settlement.** | Baseline JSON `:26-36` vs base plain census findings; `git show --stat ... e20f4fa` includes deleted aggregator wave files. Base probe `tools/mori-census.sh:706-716` treats directories without settlement or launch markers as empty. | Yes—coverage/evidence-loss regression; actual settlement is **[UNKNOWN]** |
| `-attribution` | Row-B’s attribution field disappeared with the row-B evidence. | Baseline line: `basis=row-B ... attribution=inference`; live aggregator line: `basis=row-C other_authored_commits=137` | Yes—evidence-strength downgrade |
| `-example` | Row-B’s example field disappeared with the row-B evidence. | Baseline `SURFACE lane.aggregator` line vs live line above | Yes—evidence-strength downgrade |
| `-rowb_files` | Row-B’s file-count field disappeared after the aggregator evidence change. | Baseline `rowb_files=<V>` vs live `basis=row-C other_authored_commits=137` | Yes—evidence-strength downgrade |
| `SURFACE:journal` | The journal surface status changed from baseline `drift` to current `ok`; its counters are volatile and the current boot has no OOM/kill-signal matches. | Baseline JSON line 10 → `SURFACE journal: drift`; base plain census → `SURFACE journal: ok ... kill_signal=0 ...` | No |
| `basis` | The aggregator basis changed row-B → row-C. | Baseline `basis=row-B`; live `basis=row-C` | Yes—evidence-strength downgrade |
| `obs` | A wave finding’s `obs` value changed because the wave-ID set changed. The current-only ID is `shokunin-train-20261016-w24`; the baseline-only IDs are the two aggregator waves. | Baseline JSON lines 26–36 vs live census findings | No comparator defect; the underlying loss of old-wave evidence is covered above |

**Did the drift tool mis-report?** No false change was observed. Its `obs` and generic `-FINDING:WAVE_UNSETTLED_AGE` tokens are lossy summaries of the changed wave IDs, but they match the underlying diff. The important caveat is in the census evidence: deleted wave markers make old waves disappear from the unsettled set without proving settlement.

## B. Kill-event host facts

All journal outputs below were count-only or restricted to non-`MESSAGE` fields. The requested unit-group query completed for both user and system journals; system-journal reads succeeded.

| Fact | Command → observed output |
|---|---|
| Kernel | `uname -r` → `7.2.3-arch1-3` |
| systemd | `systemctl --version` → `systemd 261 (261.2-1-arch)`; build includes `+PCRE2` |
| PSI files | `ls /proc/pressure \| wc -l` → `4` |
| Host OOM-counter entry present | `grep -c '^oom_kill ' /proc/vmstat` → `1` matching entry |
| Userspace OOM services | `systemctl is-active systemd-oomd.service earlyoom.service; systemctl is-enabled systemd-oomd.service` → `inactive`, `inactive`, `disabled` |
| Observability binaries | `for b in bpftrace bpftool earlyoom oomctl coredumpctl journalctl otelcol otel-cli below atop; do command -v "$b" \|\| echo absent; done` → `bpftrace`, `bpftool`, `earlyoom`, `otelcol`, `otel-cli`, `below`, `atop` absent; `oomctl`, `coredumpctl`, `journalctl` present under `/usr/bin` |
| Cgroup2 mount | `grep -E '^cgroup2 ' /proc/mounts` → `cgroup2 /sys/fs/cgroup cgroup2 rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot,memory_hugetlb_accounting 0 0` |
| Kill-class catalog entries | `journalctl --list-catalog fe6faa94e7774663a0da52717891d8ef d989611b15e44c9dbf31e3c81256e4ed fc2e22bc6ee647b6b90729ab34a250b1 \| wc -l` → `3` |
| Kernel OOM events | `journalctl -k -b 0 ... '^oom-kill:constraint=' ... \| wc -l` → `0`; same query with `-b all` → `5`; all-boots `Killed process` query → `5` |
| Kernel OOM events by boot | All-boots constraint and `Killed process` queries, restricted to `_BOOT_ID` → both `5 "_BOOT_ID":"7bd93aee` |
| `fe6faa94…` unit notices by boot | User scope → `7 "_BOOT_ID":"7bd93aee`; system scope → `9 "_BOOT_ID":"7bd93aee` |
| Requested unit grouping | `journalctl --{user,system} -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID,UNIT,USER_UNIT \| grep -oE '"(UNIT\|USER_UNIT)":"[^"]+"' \| sort \| uniq -c` → user: 2 `app.slice`; 1 each `arc2-r10-mid.service`, `arc2-r8-ctl.service`, `run-p2866091-i19650632.scope`, `run-p4175743-i29293759.scope`, `-.slice`. System: 1 each `systemd-coredump@11-53250-746392_17435969-0.service`, `system.slice`, `system-systemd\\x2dcoredump.slice`, `user-1000.slice`, `user.slice`; 4 `user@1000.service`. |
| `d989611b…` systemd-oomd notices | Same user/system journal ID queries piped to `wc -l` → `0` / `0` |
| Missed-journal markers | `journalctl -b all -q MESSAGE_ID=e9bf28e6e834481bb6f48f548ad13606 -o json --output-fields=_BOOT_ID \| wc -l` → `0` |
| Current boot / user-journal probe | `uptime -s` → `2026-10-19 08:11:44`; `journalctl --user -b -q -o json --output-fields=_BOOT_ID \| wc -l` → 87,486 initially, 87,488 on a later read |

The **5 kernel OOM records** and **16 `fe6faa94…` notices** are distinct counts: the notices are distributed across multiple unit contexts and both journal scopes, so they are not a one-notice-per-kernel-event count. Exact per-event mapping is **[UNKNOWN]** from the requested unit-group output.

The compact host-fact table was sent to `W2RoundMori.R12KnowledgeB`. The temporary scratch directory was removed; LANE was not modified.
---
L1 caveats (round 12, from the sentinel seat's audit):
- The census rows quoted above carry `cmd=journalctl --user -b --no-pager` — the census's published
  provenance string. Re-running *that* string prints journal MESSAGE text; the census itself only
  counts (`tools/mori-census.sh:239-240` comment). Do not run the `cmd=` string as a recheck; use the
  count-only forms (`-o json --output-fields=_BOOT_ID … | wc -l`). Routed: emit a count-only `cmd=`
  (planned with r13 operability work).
- The kernel-OOM recheck above is abbreviated with `...`; the full, re-runnable MESSAGE-free form is
  line 3 of `corpus/knowledge/kernel-oom-line-attribution-r12.md`.
