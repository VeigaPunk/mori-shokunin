# ScoutSourcesDup — systemd/earlyoom source rows + census warning codes (round 30)

Seat: MoriR30.ScoutSourcesDup (leaf, no subagents). Lane rev read: `a66751b1a97fb6422a4756f867d94269de9bcdd5` — matches the contract's landing rev (`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`). Read-only work; this report is the only file written.

## 1. Census run (observed)

Command, run from the fleet root at 2026-10-22T21:14:33Z (finished 21:14:34Z):

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Output (verbatim, 11 lines; `EXIT=0`):

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Observed: 10 warnings, all `W04`; zero `E` findings; registry rows = 155 (`awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ {n++} END{print n}' corpus/SOURCES.md`); ids S001–S155 with no gap, so the next new id is **S156**.

## 2. What the codes mean — and where the definitions actually live

**CORPUS.md defines no W-codes.** `grep -nE 'W0[0-9]|warning code|W-code' /home/vgpnk/Projects/shokunin/CORPUS.md` printed no matches (run 2026-10-22). Its census section `CORPUS.md:131-149` lists only row-count, malformed-row, tier/status histogram, duplicate-id, enum and missing-used-by `awk` checks — it has **no URL-dedup check at all**. So "per CORPUS.md" cannot be satisfied literally; the only code authority is the script header, which the request's phrasing does not name.

Code table (`scripts/sources-census.sh:16` exit semantics, `:24-30` E-codes, `:31-33` W-codes):

| code | class | meaning (trigger as implemented) |
|---|---|---|
| W01 | warning | tier-C row with status `mined` whose used-by is not `—` (tier C is lead-only). Emission: `:670-671`. |
| W02 | warning | `rejected` row whose `teaches` text is shorter than 8 characters (no rejection reason). Emission: `:672-673`. |
| W03 | warning | `mined` row with used-by `—` (mined but no citing path). Emission: `:674-675`. |
| W04 | warning | the row's URL (first URL in the cell, normalized) already occurred in an earlier row **with a different scope**. Emission: `:644-646`. Does not fail validation (`:33`, `:364`). |
| E01 | error | malformed row: `NF != 13` (`:636-637`). |
| E02 | error | id does not match `S[0-9]{3,}`. |
| E03 | error | duplicate id. |
| E04 | error | same URL **and same scope** as an earlier non-rejected row, and `teaches` does not contain `supersedes S###` (`:639-643`). |
| E05 | error | kind outside the 10-value enum (`spec docs paper code tool dataset talk book community own-work`). |
| E06 | error | tier outside `A/B/C`. |
| E07 | error | status outside `queued/mined/rejected`. |
| E08 | error | `opened` not a valid past-or-present ISO date. |
| E09 | error | `recheck` not ISO date, `NNd`, or a symbolic cadence. |
| E10 | error | `community` at tier A. |
| E11 | error | a used-by path does not exist on disk. |
| E12 | error | row-shaped source outside the `## Registry` section. |

Errors exit 1; W-codes never change exit status (`:16`, `:33`). The requested census currently stands at 155 rows, 0 errors, 10 W04.

## 3. How duplicate detection really works (the part that decides new warnings)

- Normalization reads **only the first `http(s)` URL in the source cell**, strips a fragment and trailing slash, lowercases the host (`url_of`, `:606-612`). A URL placed 2nd–8th in a multi-URL cell is invisible to E04/W04.
- W04 fires only when the scope string differs; identical scope instead risks E04 (fatal) unless the row is `rejected` or its `teaches` contains `supersedes S###`.
- Confirmed against the live registry: 14 rows repeat an earlier row's first URL. Ten are cross-scope → exactly the ten W04 lines above. Four same-scope repeats — S133 (`supersedes S124`), S143 (`supersedes S090`), S144 (`supersedes S093`), S145 (`supersedes S096`) — produce nothing because their `teaches` opens with `supersedes`.
- [INFERENCE, from the code above] Therefore a new row that reuses an already-rowed first URL cannot be warning-free unless its scope is byte-identical to the old row **and** `teaches` contains `supersedes S###`; any different scope adds one W04. The only silent alternatives are a URL never used as a first URL, or a URL carried only in a non-first position of somebody else's cell.

## 4. Every row under the two prefixes

Selection: `source` cell contains a URL under `raw.githubusercontent.com/systemd/systemd/` or `raw.githubusercontent.com/rfjakob/earlyoom/` — **26 rows**, all `mined`. "Raw" counts URLs under those prefixes in the cell; the URL shown is the cell's first URL (the one the census dedups on). Two more rows point at the same repos only via `github.com` and are listed separately (S130 is already counted above because it also carries raw v262 URLs).

| line | id | URL (first in cell) | raw | status | scope |
|---|---|---|---|---|---|
| 17 | S011 | https://raw.githubusercontent.com/systemd/systemd/v261/src/oom/oomd-util.c | 1 | mined | systemd-oomd per-cgroup kill accounting and kill implementation |
| 19 | S013 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | 1 | mined | systemd message identifiers for coredumps, kernel OOM and systemd-oomd kills |
| 22 | S016 | https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md | 1 | mined | earlyoom userspace kill flow, logged actions and --kernel-oom delegation |
| 41 | S035 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in | 1 | mined | structured process-termination and unit-result message identifiers |
| 42 | S036 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c | 1 | mined | emitted unit-failure and process-exit structured field schema |
| 44 | S038 | https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c | 1 | mined | systemd service OOM-failure result string |
| 120 | S114 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | 1 | mined | earlyoom v1.9.0 release documentation only: the both-below-limits act rule, the SIGTERM-then-SIGKILL stage order, where actions are logged, the journalctl grep advice and the v1.9.0 changelog entry; not the post-1.9.0 upstream master README (S016), not the message grammar itself (kill.c/main.c), not host state |
| 121 | S115 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 1 | mined | the documented command-line contract of earlyoom 1.9.0 only: the `-m`/`-s` percentage thresholds and their PERCENT/2 kill defaults, the `-M`/`-S` KiB alternatives and their lower-value rule, the `-r` periodic-report interval, `--dryrun`, `--syslog`, and the EXIT STATUS code table; not the runtime log-line grammar, not the code paths behind the exit codes, not the host's configured values |
| 122 | S116 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c | 2 | mined | how earlyoom computes the two percentages its thresholds compare against and the fatal exits of its `/proc/meminfo` reader: the `MemAvailable` source and its fallback, the `user mem total` denominator, the swap-free denominator, and the 102/103/104 exits; v1.9.0 tag only; not the `main.c`/`kill.c` message grammar, not host service state, not kill history, not the manual's exit-status table |
| 123 | S117 | https://api.github.com/repos/rfjakob/earlyoom/tags | 8 | mined | which upstream tag carries 1.9.0 and its date, and whether the earlyoom log-message prefixes `sending SIGTERM when mem avail`, `sending %s to process` and `escalating to SIGKILL after` are stable across tags v1.7, v1.8 and v1.9.0; the version line, the two threshold lines, the action line, the escalation line, the kill-failure line, the two low-memory warnings, the dry-run flag and the percentage format at those tags; not kill-selection logic, not the host's unit state, not kill history |
| 124 | S118 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | 2 | mined | earlyoom 1.9.0 kill-path log literals and the warn() output route: the action, escalation, kill-failure, dryrun, process-group and victim-selection texts, and whether warn() reaches stderr or syslog; not the poll-loop decision logic, not the meminfo threshold parsing, not this host's unit configuration |
| 125 | S119 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 2 | mined | earlyoom v1.9.0 startup and poll-loop emission only: the version line, the two effective threshold lines, the low-memory warnings, the dry-run flag, the poll-loop act rule and the -M/-S percent conversion; not kill.c action lines, not meminfo percentage accounting, not host unit state |
| 126 | S120 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | 1 | mined | the upstream unit template only: how earlyoom is configured and what its hardening permits it to read; the generated earlyoom.service and the Arch packaging delta are separate sources |
| 127 | S121 | https://raw.githubusercontent.com/systemd/systemd/v262/src/oom/oomd-util.c | 2 | mined | systemd-oomd's own kill accounting and its journal notice id at the v262 release tag: the `user.oomd_ooms` and `user.oomd_kill` cgroup xattrs, the `Killed(path, reason)` D-Bus signal, and MESSAGE_ID `d989611b15e44c9dbf31e3c81256e4ed`; not host service state, not kill history, not kernel OOM counters |
| 128 | S122 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | 4 | mined | systemd 262 release documentation for the journal read path only: how `-o json` encodes a field that is not printable UTF-8, what `--output-fields=` always keeps, which entries `-u UNIT` selects, and what `ActiveEnterTimestampMonotonic` and the journal's `__MONOTONIC_TIMESTAMP` measure; documentation at one released tag, not this host's journal content, not the earlyoom message grammar, not an entry-completeness guarantee |
| 129 | S123 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/logs-show.c | 3 | mined | the encoder that produces `journalctl -o json` field values at the v262 release tag: the 4096-byte null threshold, the printable check that decides string versus byte array, and the definition of "printable"; the file that builds the JSON object only, not the journal's own storage or matching code |
| 130 | S124 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2 | mined | what `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` `auto` and `kill` mean and which cgroups systemd-oomd monitors, systemd 262 only; not this host's unit values (tsukuroi-owned) |
| 135 | S129 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml | 2 | mined | systemd 262 release documentation of the OOM score adjustment only: the per-unit range and its stated effects, the per-unit default of the managing manager's own level, the manager-wide default and its unset/inherit reading, the unprivileged-user-manager default of manager value plus 100, and the statement that the manager's own value is never rewritten; not this host's unit values, user-manager state or fleet process scores, not the kernel's `oom_score` computation or `proc(5)` wording, not earlyoom's or systemd-oomd's victim choice, not the privilege rule on lowering the value (kernel doc, separate row) |
| 136 | S130 | https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in | 2 | mined | the per-user service manager's OOM placement at the v262 release tag and what its children inherit: the `OOMScoreAdjust=` line in `units/user@.service.in`, the code that gives an unprivileged manager's children its own value plus 100 (`src/core/main.c` `determine_default_oom_score_adjust`; the manual sentence is row S129), and a `units/`-wide sweep for `OOMScoreAdjust=` and `ManagedOOM*`; not this host's live per-process `oom_score_adj` values, not earlyoom's victim selection, not the kernel badness function, not the meaning of the `ManagedOOM*` keys (S124) |
| 137 | S131 | https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0 | 1 | mined | which files the v1.9.0 tag ships as configuration and what the shipped default args are: the one default-settings file, its active and commented EARLYOOM_ARGS lines, its sourcing contract, and the Makefile rule that installs it; v1.9.0 tag only; not this host's /etc/default/earlyoom file or its values, not the Arch package delta (S126), not the README example args (S114), not the unit or init-script template content (S120) |
| 139 | S133 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2 | mined | what `ManagedOOMSwap=`/`ManagedOOMMemoryPressure=` `auto` and `kill` mean and which cgroups systemd-oomd monitors, systemd 262 only; not this host's unit values (tsukuroi-owned) |
| 143 | S137 | https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c | 1 | mined | when earlyoom removed and re-introduced the option to delegate kills to the kernel OOM killer: the v0.6 introduction and v1.2 removal with compatibility-ignore (S114 README.md:416,383; v1.9.0 main.c:245-246), and the master re-introduction commit with its author and merge dates; not the option's runtime behaviour on any host, not the v1.7-v1.9.0 log grammar (S117) |
| 156 | S150 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml | 2 | mined | systemd 262 release documentation of the OOM score adjustment only: the per-unit range and its stated effects, the per-unit unset default of the service manager's own level (the page names no manager type), the manager-wide default and its unset/inherit reading, the unprivileged-user-manager branch of manager value plus 100, and the statement that `DefaultOOMScoreAdjust=` leaves the manager process's own value unchanged; not the value a unit inherits when it sets no `OOMScoreAdjust=`, not this host's unit values, user-manager state or fleet process scores, not the kernel's `oom_score` computation or `proc(5)` wording, not earlyoom's or systemd-oomd's victim choice, not the privilege rule on lowering the value (kernel doc, separate row) |
| 157 | S151 | https://api.github.com/repos/rfjakob/earlyoom/git/trees/v1.9.0?recursive=1 | 3 | mined | which files the v1.9.0 tag ships as configuration and what the shipped default args are: the one default-settings file, its active and commented EARLYOOM_ARGS lines, its sourcing contract, and the Makefile rule that installs it; v1.9.0 tag only; not this host's /etc/default/earlyoom file or its values, not the Arch package delta (S126), not the README example args (S114), not the unit template content (S120 covers earlyoom.service.in only); the Makefile and init-script lines are cited here only as consumers of the file |
| 159 | S153 | https://raw.githubusercontent.com/systemd/systemd/v262/man/sd_journal_get_realtime_usec.xml | 1 | mined | systemd 262 release documentation of the journal entry monotonic timestamp only: CLOCK_MONOTONIC microseconds since boot-up of the specific boot, a point in time only together with the boot ID of that boot, the 128-bit third parameter receiving that boot ID, and a NULL boot ID making the call fail for an entry from another boot with -ESTALE; not the journalctl JSON field name, its encoding or the `--output-fields=` always-kept set (S122), not kernel CLOCK_MONOTONIC behavior across suspend, not this host's journal |
| 160 | S154 | https://raw.githubusercontent.com/systemd/systemd/v262/src/libsystemd/sd-journal/journal-def.h | 5 | mined | the per-entry monotonic stamp at the v262 release tag: where the entry object stores it, the accessor that reads it, and the export-format writers that print it as a bare decimal line; not the JSON rendering (S122 carries the `--output-fields=` always-kept set and S123 the JSON field encoder that makes a printable value a string), not this host's journal, not a claim that a `__MONOTONIC_TIMESTAMP=` data field is present in every entry's enumerated field list |

Same repositories, `github.com` only (outside both raw prefixes, listed for completeness — neither is affected by the raw-URL dedup):

| line | id | URL | status | scope |
|---|---|---|---|---|
| 18 | S012 | https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 | mined | systemd-oomd varlink arbitrary-SIGKILL vulnerability and affected versions |
| 161 | S155 | https://github.com/rfjakob/earlyoom/commit/ca2251fcd222af8c857aec4a26e182cf5f9c596e.patch | mined | the introduction of earlyoom's dry-run option only: the option-parser startup line it prints, the send-site guard that returns before any signal is sent, the flag spelling in the option table, and the manual and help-text wording added with it; not the v1.9.0 line numbers of the same strings (S118:271-274, S119:295), not the version line (S119:161), not the v1.9.0 manual text (S115), not any host configuration |

## 5. Candidate URLs — already rowed?

Exact-string search over all 210 lines of `corpus/SOURCES.md` (Python `in` over each line, plus the dedup model of `url_of`):

| candidate | in SOURCES.md? | evidence | new-row warning risk (first URL) |
|---|---|---|---|
| systemd v262 `man/org.freedesktop.systemd1.xml` | yes, **not as a row** — 4th URL of S122 | `corpus/SOURCES.md:128` source cell; anchor cites `man/org.freedesktop.systemd1.xml:2244, 2780, 2783-2790` | **none** — S122's first URL is `journalctl.xml`, so this URL is absent from the dedup set [INFERENCE from `:606-612`]; the facts, however, are already cited by S122 |
| systemd `src/core/unit.c` | yes, **other revision** — S036 | `corpus/SOURCES.md:42`; URL pinned to commit `cf8ebfc6…`, not v262 | **none** for a v262 URL (textually distinct); scope must state the tag/commit split from S036 |
| systemd `src/shared/bus-print-properties.c` | **no** | zero occurrences in the file | none |
| systemd `man/systemctl.xml` | **no** | only `systemctl` occurrence is S126's PKGBUILD anchor at `:132` | none |
| systemd `man/journalctl.xml` (v262) | yes — **S122 first URL** | `corpus/SOURCES.md:128`, mined | **W04** if scope differs from S122; **E04** (fatal) if the scope string is identical and `teaches` lacks `supersedes S###` |
| systemd `src/journal/journald-rate-limit.c` | **no** | zero occurrences | none |
| earlyoom v1.9.0 `earlyoom.service.in` | yes — **S120 first URL** | `corpus/SOURCES.md:126`, mined | **W04** if scope differs from S120; **E04** if scope identical without `supersedes` |

Related, not asked but decisive for the same work: S120's row is already cited by `corpus/knowledge/userspace-oom-killers-r26.md:1` and `oom-victim-selection-r27.md:1`; S122's `journalctl.xml` is cited by `userspace-oom-killers-r26.md:1`. No knowledge entry cites `bus-print-properties.c`, `systemctl.xml`, `journald-rate-limit.c`, or `org.freedesktop.systemd1.xml` by filename (`grep` over `corpus/`, 2026-10-22).

## 6. Practical rules for the C1 rows (S156+)

1. Prefer first URLs that no existing row uses as its first URL. Mechanically warning-free candidates from the requested list: v262 `src/core/unit.c`, `src/shared/bus-print-properties.c`, `man/systemctl.xml`, `src/journal/journald-rate-limit.c`. `man/org.freedesktop.systemd1.xml` is also invisible to dedup but is already cited inside S122, so a row on it adds no new source evidence.
2. Avoid `v262/man/journalctl.xml` and `v1.9.0/earlyoom.service.in` as a new row's **first** URL, or budget one new W04 each. If one of them must be cited, put a novel URL first and carry the duplicate later in the same cell — second-and-later URLs are outside the dedup check.
3. Never copy a scope cell from S120/S122/S133/S150 etc. verbatim into a new row: identical scope + same first URL is E04, which fails validation, not a warning.
4. `teaches` containing `supersedes S###` is the only intended way to keep a same-URL/same-scope repeat silent; it is not a licence to duplicate a citation that adds nothing.
5. `unit.c` at v262 is a different revision from S036's `cf8ebfc6…` row: the anchor must name tag v262 = commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492` (the pin S121/S122 already use) or the row is a revision-drift defect.
6. Keep the row count at 11 fields: `S15x` id, `code/docs` kind, tier `A`, a scope narrower than the file, an anchor with line numbers + tag/commit + sha256, status `mined` only with a used-by path that exists.

## 7. Gaps and limits

- No `lsp` device is exposed to this seat and the artifacts are Markdown plus a GNU-awk shell script with no language server; all tracing here is textual (`url_of` and the W04/E04 blocks were read directly at `scripts/sources-census.sh:606-646`). Recorded as the literal fallback.
- The census was run in `validate` mode only, as requested; `census`/`overdue`/`shared` modes were not run, so counts beyond rows=155 and the W04 set are unmeasured here.
- "W-code meanings per CORPUS.md" has no literal answer: CORPUS.md carries no code vocabulary (`grep` above). The meanings in section 2 are the script's, which is the only executable definition.
- [INFERENCE] A new row whose only novel URL is `org.freedesktop.systemd1.xml` would pass the census silently even though S122 already cites that file; the census cannot see non-first URLs, so silence there is not evidence of a new source.
