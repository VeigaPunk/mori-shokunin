source: S003 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — v7.2 `Killed process` line 945; S013 — https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in — catalog at commit cf8ebfc6 entries `fc2e22…` line 66, `fe6faa…` line 604, `d989611b…` line 884; S014 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — systemd 262 `--output-fields=` lines 489–494 and `-k` lines 341–343; S015 — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html — systemd 262 `MESSAGE` / `MESSAGE_ID` lines 34–46
verified-at: 2026-10-19 (lane base 20e2255; host kernel 7.2.3-arch1-3, systemd 261 (261.2-1-arch))
recheck: curl -fsSL https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | grep -nE 'fc2e22bc|fe6faa94|d989611b'; journalctl --list-catalog fe6faa94e7774663a0da52717891d8ef d989611b15e44c9dbf31e3c81256e4ed fc2e22bc6ee647b6b90729ab34a250b1 | wc -l; journalctl --user -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l; journalctl --system -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l; journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+' -o json --output-fields=_BOOT_ID | jq -r '._BOOT_ID' | sort | uniq -c → anchors 66, 604, 884; 3; 7; 9; 5 7bd93aee71144017b870212161a3dabf

## Claim
Use the catalog `MESSAGE_ID` as the journal class key, with `--output-fields` restricted to non-`MESSAGE` fields. A matching catalog notice is a notice for a unit, not a count of killed processes. On the retained host journals, five kernel `Killed process` records in boot `7bd93aee71144017b870212161a3dabf` coexist with seven user-journal and nine system-journal `fe6faa94…` notices; the scopes and units are not additive victim counts.

Adjacent: `tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:97,120–135` and `oom-event-plane.md:39–41` document that one kernel kill can yield multiple per-unit `fe6faa94…` notices. Those earlier observations are not merged with this retained-journal sample; mori reports scoped fleet-evidence notice counts, not an OS kill total.

## Evidence
- S013 catalog: `fe6faa94e7774663a0da52717891d8ef` at `:604–605` is “A process of @UNIT@ unit has been killed by the OOM killer.”; `d989611b15e44c9dbf31e3c81256e4ed` at `:884–885` is systemd-oomd's “one or more processes in unit”; `fc2e22bc6ee647b6b90729ab34a250b1` at `:66–67` is a core-dump notice, not an OOM-kill class.
- S015, `systemd.journal-fields:MESSAGE_ID=` (`:42–46`), defines a 128-bit message-type identifier; the `MESSAGE=` section says “not supposed to be parsed for metadata” (`:34–36`). S014, `journalctl:--output-fields=` (`:489–494`), limits JSON output fields and notes the always-present cursor/timestamp/boot fields. No journal `MESSAGE` value is emitted by the commands here.
- Catalog inventory: `journalctl --list-catalog fe6faa94e7774663a0da52717891d8ef d989611b15e44c9dbf31e3c81256e4ed fc2e22bc6ee647b6b90729ab34a250b1 | wc -l` → `3` catalog entries.
- Kernel unit: `journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+' -o json --output-fields=_BOOT_ID | wc -l` → `5` records; `journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+' -o json --output-fields=_BOOT_ID | jq -r '._BOOT_ID' | sort | uniq -c` → `5 7bd93aee71144017b870212161a3dabf`.
- User notice unit: `journalctl --user -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l` → `7`; grouped with `jq -r '._BOOT_ID' | sort | uniq -c` → `7 7bd93aee71144017b870212161a3dabf`.
- System notice unit: `journalctl --system -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID | wc -l` → `9`; grouped with `jq -r '._BOOT_ID' | sort | uniq -c` → `9 7bd93aee71144017b870212161a3dabf`.
- Timestamp context for the five kernel OOM summaries (L1's MESSAGE-free extraction): `journalctl -k -b all -q --grep='^oom-kill:constraint=' -o json --output-fields=_BOOT_ID | grep -oE '"__REALTIME_TIMESTAMP":"[0-9]+"'` → timestamps corresponding to `2026-10-18T17:46:17Z`, `18:06:07Z`, `19:07:45Z`, `22:53:10Z`, `23:57:18Z` (UTC-rendered from journal microseconds).
- OOMD notice counts: `journalctl --user -q MESSAGE_ID=d989611b15e44c9dbf31e3c81256e4ed -o json --output-fields=_BOOT_ID | wc -l` → `0`; the same command with `--system` → `0`. The counts are separately scoped and are not summed.

## Observed
All three catalog IDs are present on the host; the `fe6faa94…` counts above are record/notice counts from two journal scopes. The kernel victim count is the number of matching `Killed process` records in the retained kernel journal, not a sum of the user/system notices. The boot grouping is from `_BOOT_ID` only.

## [INFERENCE]
The per-unit `fe6faa94…` fan-out is not a one-notice-per-victim counter: one kill can be reflected at more than one unit/scope, and a unit notice can describe a kill event without identifying a unique victim. The observed 5 vs 7 vs 9 quantities cannot be converted into a per-kill mapping from these counts alone.

## [UNKNOWN]
Which ancestor units account for each notice, whether one kernel victim maps to multiple notices, and whether records outside the retained journals existed were not established. No broad negative sweep was used.

## What it changes for mori
For the SKILL.md `Did something get killed?` / journal-class decision row (`:17`), count stable `MESSAGE_ID` matches and label the unit as **notice** or **kernel victim record** plus journal scope. Never sum user and system scopes or equate unit notices with victims.

## Delivery paths this cannot see
Catalog counts cannot see kills that produced no retained journal record, entries unavailable to the caller, or delivery paths that use another class/no catalog ID. They do not attribute an individual victim or prove a fleet lane caused a host event. The `fc2e22…` coredump class is not an OOM-kill count.

## Fills (coverage-map ground; Frontier row)
Coverage-map ground: structured OOM-class counts and the notice-versus-victim unit boundary. Frontier F1/F2: userspace OOM notices and kernel OOM journal attribution.
