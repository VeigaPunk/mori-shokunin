# ReviewSources — round 13 source reopen (S013 / S014 / S015)

Seat: MoriR13.ReviewSources (reviewer, leaf). Axes judged: coverage, operability.
Scope: reopen the S013, S014, S015 source sample; check claim-vs-source and quote accuracy; state what the sources can and cannot prove about fleet-caused kills and unique kernel victim counts.
No builds, tests, lint, or journal queries were run. No remediation applied. No lane files edited.

## Method and receipts (read-only)

- Fetched each source and hashed it: `curl -fsSL <url> | sha256sum | cut -c1-16`.
  - S013 `raw.githubusercontent.com/systemd/systemd/cf8ebfc6…/catalog/systemd.catalog.in` → `e53707db7e6963b2`. Matches registry SOURCES row S013.
  - S014 `freedesktop.org/…/man/latest/journalctl.html` → `75440570fb1f7185`. Matches registry row S014.
  - S015 `freedesktop.org/…/man/latest/systemd.journal-fields.html` → `906e5d34b38913dd`. Matches registry row S015.
  - Caveat: S014 and S015 are `man/latest/` URLs, which move. The digests match today, but the recheck will break after the next systemd man release. See F-9.
- Line anchors for S013 were checked with `grep -n` against the fetched bytes (exact).
- S014 and S015 numeric anchors could not be reproduced exactly. The raw HTML is paragraph-merged (463 lines), and the reader renders a different line count (1078 lines). Quotes were checked as text. See F-9.
- S003 (`torvalds/linux` v7.2 `mm/oom_kill.c`) and S004 (commit `c03c1a14…` `mm/memcontrol.c`) were checked with `grep -n` and `sed -n`, because the kernel-victim claims depend on them.
- Tool installs or upgrades: none. Used only preinstalled `curl`, `sha256sum`, `grep`, `sed`, `cut`, `wc`.

## Claim-vs-source checks

| ID | Corpus claim (file:line) | Source fact (verified) | Verdict |
|---|---|---|---|
| S013-a | fe6faa94 is at catalog `:604`, subject “A process of @UNIT@ unit has been killed by the OOM killer.” `:605` (kill-classes:11) | grep: `604:-- fe6faa94…`, `605:Subject: A process of @UNIT@ unit has been killed by the OOM killer.` | Accurate |
| S013-b | d989611b at `:884–885`, “one or more processes in unit” (kill-classes:11) | grep: `884:-- d989611b…`, `885:Subject: systemd-oomd killed one or more processes in unit @UNIT@` | Accurate; the quoted phrase is a true substring |
| S013-c | fc2e22bc at `:66–67` is a core-dump notice (kill-classes:11) | grep: `66:-- fc2e22bc…`, `67:Subject: Process @COREDUMP_PID@ … dumped core` | Accurate |
| S013-d | Catalog gives “distinct stable MESSAGE_ID values to core dumps, kernel OOM notices and oomd notices” (registry S013) | Three distinct IDs confirmed. Body of fe6faa94 at `:609–615` says the kernel OOM killer forcibly terminated “A process associated with @UNIT@”. | Accurate as a catalog statement |
| S013-e | Kill-classes Claim: “A matching catalog notice is a notice for a unit, not a count of killed processes.” (kill-classes:6) | Body `:609–615` is singular: “A process of unit … has been killed”. Nothing in S013 states emission cardinality (one notice per kill, or per unit event). | Overreach. The unit-scoped part is supported. “Not a count of killed processes” is [INFERENCE], not source. |
| S013-f | Catalog says nothing about causation, yet kill-classes:33 correctly says the counts do not prove a fleet lane caused the event | fe6faa94 body `:615`: “Note that the memory pressure might or might not have been caused by @UNIT@.” | Supports the corpus. Quote this line directly. |
| S013-g | Kernel-loss mode is left as [UNKNOWN] (kernel-oom:26; kill-classes:33) | catalog `e9bf28e6e834481bb6f48f548ad13606` at `:58–63`: “Journal messages have been missed … Kernel messages have been lost as the journal system has been unable to process them quickly enough.” | Omitted source. A loss signal exists in S013 and is not cited. See F-5. |
| S014-a | `--after-cursor` quote: “Start showing entries from the location in the journal after the location specified by the passed cursor.” (registry S014) | Present verbatim in the fetched page. | Accurate |
| S014-b | `-k` adds `_TRANSPORT=kernel` (kernel-oom:14) | Verbatim: “Show only kernel messages. This adds the match "_TRANSPORT=kernel". This implies `--boot=0` unless explicitly specified otherwise.” | Quote accurate. The `--boot=0` implication is omitted from the corpus. See F-6. |
| S014-c | `--output-fields` limits JSON output; always-present `__REALTIME_TIMESTAMP` and boot fields (kill-classes:12; kernel-oom:14) | Paragraph exists: “`__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`”. Applies to verbose/export/json modes. | Substantially accurate. Anchor numbers not reproduced. |
| S014-d | `--grep` is not mentioned anywhere in the corpus as a MESSAGE match | Verbatim: “`-g, --grep=` Filter output to entries where the **MESSAGE=** field matches the specified regular expression.” | **Corpus omits that the kernel victim count is a MESSAGE text match.** See F-1. |
| S014-e | `--system` / `--user` scope (kill-classes:16–18; userspace:15) | Verbatim: the system journal is readable by root and by members of `systemd-journal`, `adm`, `wheel`; `--user` shows only the invoking user; `--user` needs persistent logging (`Storage=`). | Counts are only as complete as the reader's access. Not recorded in the corpus. See F-7. |
| S015-a | MESSAGE is display text, “not supposed to be parsed for metadata” (registry S015; kill-classes:12) | Verbatim: “is not supposed to be parsed for metadata.” | Accurate |
| S015-b | MESSAGE_ID is the typed key; underscore-prefixed fields are trusted (registry S015; kill-classes:6, :30) | MESSAGE_ID sits under “**User Journal Fields** … fields that are directly passed from clients”. Trusted fields are underscore-prefixed and “cannot be altered by client code”. | **Claim-vs-source conflict.** MESSAGE_ID is client-writable, not trusted. See F-2. |
| S015-c | Line anchors: MESSAGE `:32–39`, MESSAGE_ID `:41–44`, _TRANSPORT `:204` (registry S015) vs MESSAGE `:34–36`, MESSAGE_ID `:42–46` (kill-classes:12) vs `_TRANSPORT :204–246` (kernel-oom:14) | Two corpus files disagree with each other and with the registry. The numbers could not be reproduced from the fetched bytes. | Anchor drift. See F-9. |
| S003-a | `dump_oom_victim` writes `oom-kill:constraint=` and `task=,pid=,uid=` at `:447–453` (kernel-oom:11) | grep: `447 oom-kill:constraint=`, `452 ,task=%s,pid=%d,uid=%d` | Accurate |
| S003-b | Killed-process line at `:945`; `count_vm_event(OOM_KILL)` at `:935` (kernel-oom:12; registry S003) | grep: `935 count_vm_event(OOM_KILL);`, `945 pr_err("%s: Killed process %d (%s) …UID:%u…")` | Accurate, but see F-4 for what the site means. |
| S004-a | `task_memcg=` at `:1825`; `oom_memcg=` at `:1820` (kernel-oom:12) | grep on c03c1a14: `1820 pr_cont(",oom_memcg=")`, `1825 pr_cont(",task_memcg=")` | Accurate |

## Findings by severity

### F-1 (high, coverage, C1). The kernel victim class is counted by MESSAGE text, not by a structured field.

- The corpus uses `journalctl -k -b all -q --grep='(Out of memory|Memory cgroup out of memory): Killed process [0-9]+'` for the kernel victim count (kill-classes-by-message-id-r12.md:3, :14; kernel-oom-line-attribution-r12.md:3, :16).
- It also uses `--grep='^oom-kill:constraint='` for the summaries (kernel-oom-line-attribution-r12.md:3, :15, :17).
- S014 defines `--grep` as a match on the MESSAGE= field (see S014-d).
- The corpus's "No MESSAGE field is output" (kill-classes:19 and kernel-oom:16) is true of output only. The selection itself is a MESSAGE-text match.
- This violates QUALITY criterion 15 ("never by message text") and lesson round-12 M13. It also breaks the round-13 goal of replacing text classes with structured counts.
- The sources give no structured discriminator for these lines. S013 has no catalog ID for kernel printk victim lines. S015 defines no field for them. Criterion 15 allows structured fields "when one exists"; none is established here.
- Consequence: the kernel victim class cannot be made structured from S013–S015. It must be labelled as a MESSAGE-text-matched residual, not as a structured count. Otherwise it cannot satisfy criterion 15.

### F-2 (high, coverage, C1). MESSAGE_ID is client-writable, not a trusted key.

- S015 places MESSAGE_ID under "User Journal Fields … directly passed from clients". Trusted fields are the underscore-prefixed ones.
- Kill-classes:6 and :30 treat MESSAGE_ID as the "typed key" and the notice count as the notice count. Criterion 15 says "MESSAGE_ID or another trusted structured field".
- Any process can write an entry with MESSAGE_ID=fe6faa94…. The sources do not say which emitter writes these notices.
- The notice counts (7 user, 9 system) are therefore "records bearing this MESSAGE_ID in scope", not "systemd notices". Attribution to systemd needs trusted emitter fields (`_TRANSPORT`, `_PID`, `_COMM`, `_UID`, per S015's trusted section).

### F-3 (high, claim-vs-source). The sources cannot prove a fleet-caused kill.

- S013 `:609–615` says the kernel OOM killer forcibly terminated "a process associated with @UNIT@", and that the pressure "might or might not have been caused by @UNIT@".
- S014 and S015 define journal fields and scopes; they say nothing about fleet membership.
- S004 `task_memcg=` gives a cgroup path, but no source in S013–S015 maps a cgroup path to a lane. No lane↔cgroup mapping source exists in this sample.
- Kill-classes:8 says "mori reports scoped fleet-evidence notice counts". The counts are host journal scopes, not fleet evidence. The wording should change to "host-journal scoped counts" (F-10).

### F-4 (high, claim-vs-source). The sources cannot prove a unique kernel victim count.

What S003 v7.2 shows (`oom_kill.c`):
- `__oom_kill_process()` at `:912` emits the Killed-process line at `:945` (`pr_err`, not inside a ratelimit). It also increments `OOM_KILL` at `:935`.
- It is called once for the chosen victim (`:1042`), and once per member through `oom_kill_memcg_member()` (`:998–1004`, call at `:1003`) when the memcg has group-kill set. One OOM event can therefore produce several Killed-process records.
- `dump_oom_victim()` (the `oom-kill:constraint=` summary) is emitted only under `__ratelimit(&oom_rs)` at `:1030–1032`. The summary count is at most the event count and can be lower.
- The record carries PID, comm and UID (`:945`). It carries no start time and no unique victim ID. PIDs can be reused.

Corpus claims that overreach:
- kill-classes:21 "The kernel victim count is the number of matching `Killed process` records". This counts process-kill records, including group members. It is not an event count, and it is not a unique-victim count.
- kernel-oom:20 "five matching summaries and five matching victim records" treats two different things as one. Equal here, not by source.
- Unique-victim keying would need a composite (boot id, `__REALTIME_TIMESTAMP`, PID). That is still not proven, because of F-5.

### F-5 (medium, coverage). The loss signal in S013 is not cited.

- S013 `:58–63`, `e9bf28e6e834481bb6f48f548ad13606`: "Journal messages have been missed. Kernel messages have been lost as the journal system has been unable to process them quickly enough."
- The corpus leaves loss as [UNKNOWN] (kernel-oom:26; kill-classes:33). S013 supplies a catalog class for exactly this.
- Without a loss canary, every kernel count is a lower bound of unknown tightness.

### F-6 (medium, operability). `-k` implies `--boot=0`; the corpus does not say so.

- S014 (`-k` entry): "This implies `--boot=0` unless explicitly specified otherwise."
- The corpus passes `-b all` (correct), so the 5 records are found. A bare `journalctl -k --grep=…` would return 0 for the prior boot, a silent false negative. The recheck lines do not warn of this.

### F-7 (medium, coverage). Reader access and persistence are not recorded.

- S014: the system journal needs root or membership in `systemd-journal`, `adm` or `wheel`. `--user` shows only the invoking user and requires persistent logging.
- The corpus reports `--system → 9` and `--user → 7` without recording the reader's uid, groups, or `Storage=`. Those counts are only as complete as the reader's access.

### F-8 (medium, claim-vs-source). Notice cardinality is overstated.

- S013 `:605` and `:609` describe one process per notice. Emission cardinality is not stated.
- kill-classes:6 says the notice is "not a count of killed processes". That is [INFERENCE] and should be labelled as such. The supported statement is: unit-scoped, carries no victim identity, cardinality unspecified in S013.

### F-9 (low, quote and anchor accuracy).

- S013 anchors are exact (grep-verified). S013 quotes are exact.
- S014 and S015 numeric anchors cannot be reproduced. The raw HTML is paragraph-merged and the reader's line count differs. Affected: registry S014 `:187–190`, `:489–492`, `:341–343`; registry S015 `:32–39`, `:41–44`, `:204`; kill-classes:12 `:34–36`, `:42–46`; kernel-oom:14 `:204–246`, `:341–343`.
- The two corpus files disagree with each other on S015 anchors. Replace numeric anchors with section-heading anchors (e.g. "User Journal Fields > MESSAGE_ID="), which resolve on the page, per QUALITY 9.
- S014/S015 are mutable `latest` URLs. Pin to a versioned systemd 262 page or record the digest per access. Digests `75440570fb1f7185` and `906e5d34b38913dd` match today.

### F-10 (low, wording). "fleet-evidence" describes host-journal scopes.

- kill-classes:8 uses "fleet-evidence notice counts". The scopes are host user and system journals (S014 scope definitions). Use "host-journal scoped notice counts".

## Residual risk and verification gaps

- No journal query was run. The counts 5 / 7 / 9 / 0 are the corpus's measurements and were not re-measured here.
- S005 (`oom:mark_victim` tracepoint, status queued) is the event-time alternative to the printk line. It was not opened and is not used for any claim.
- S013 covers catalog IDs only. It says nothing about which emitter writes fe6faa94 or d989611b.
- S003 proves the code paths, not the runtime behaviour on this host (group-kill and ratelimit firing are unobserved).

## Proposed checks for L1 (not run)

1. Relabel kernel victim counts as MESSAGE-text-matched and remove them from any "structured" C1 claim. Confirm with `grep -nE -- '--grep' corpus/knowledge/*-r12.md` that every hit carries that label.
2. Emitter trust for notices: `journalctl --system -q MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef -o json --output-fields=_BOOT_ID,_PID,_COMM,_TRANSPORT,__REALTIME_TIMESTAMP`. Group by `_COMM` and `_TRANSPORT`. Report the distribution before any emitter claim.
3. Loss canary: count `MESSAGE_ID=e9bf28e6e834481bb6f48f548ad13606` in `--system` for boot `7bd93aee71144017b870212161a3dabf`, and report it next to every kernel count.
4. Victim key: for `-k -b all` Killed-process records, count distinct (`_BOOT_ID`, `__REALTIME_TIMESTAMP`, PID) and report that as a lower bound, alongside the raw line count.
5. Reader scope: record `id -u`, `id -Gn`, and the `Storage=` value next to every `--system` and `--user` count.
6. Pin S014 and S015 to versioned URLs, or add a digest-recheck line to each registry row.

## Blockers

None. The sources were reachable and read. The unverifiable items above are reported as anchor drift and residuals, not blockers.
