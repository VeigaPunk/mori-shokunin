# JournalKnowledge — structured journal scopes (round 13, C1)

## Axes
- **Coverage:** new knowledge note gives source-grounded, MESSAGE-free structured journal classes with independent user/system scope labels, exact boot context, and the systemd-observed signal-9 exit path.
- **Operability:** denies invented counts; `unavailable` is not `0`; a zero oomd notice is a record count with `activity=unmeasured` and no unit-state probe; query mechanics are ready for CensusFix.

## Files changed
- `corpus/knowledge/structured-journal-scopes-r13.md` — new, 68 lines / 20,078 bytes; provenance trio + Claim / Evidence / Observed / [INFERENCE] / [UNKNOWN] / expected C1 implementation / limits / Fills.
- `.ufo/waves/round-13/build/JournalKnowledge.md` — this report.

No source registry, census script, SKILL, LOG, MANIFEST or sibling file edited. No commits. `SKILL.md:17` and `:30` already carry the structured, MESSAGE-free row and cite this note (observed current state); this seat did not edit SKILL.

## Behavior
Source-open only. S013, S014, S015 were re-fetched this round; S035 is the same pinned catalog bytes under a new scope; S036 is the pinned `unit.c` emitter. No live journal query was run, no `MESSAGE` value was read or emitted, and no C1 count is asserted as observed. The note marks every expected C1 number `pending measurement`; the current census probe (`tools/mori-census.sh:847-914`, text classes at `:881-885`) is described as the pre-C1 state at lane base `6531ac6`, not as the delivered implementation. Boot boundary D2 (named in `CensusFix.md` §9): C1 rows are current-boot only, `-b` with each record's `_BOOT_ID` normalized against `/proc/sys/kernel/random/boot_id` (`MORI_BOOT_ID` override); no `-b all`; the round-12 7/9 sample is retained-boot evidence and is not presented as a current-boot count.

## Sources opened (access date 2026-10-20)
| id | URL | anchor | SHA-256 |
|---|---|---|---|
| S013 | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in` | `:58-64`, `:66-75`, `:604-616`, `:870-881`, `:884-894` | `e53707db7e6963b284e504dc17f36a4d5a2bdb4bd8a9611b2cf95c075ad86592` |
| S035 | same URL and commit as S013; new scope “structured process-termination and unit-result identifiers” | `:561-566`, `:568-575` | same bytes as S013 |
| S036 | `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c` | `unit_log_failure` `:6333-6342`; `unit_log_process_exit` `:6355-6392`; level `:6372-6377`; fields `:6379-6391` | `4833056a6313b250ad6b53de3121a51e8dee602733e1aedf4a7d3d2687d547ed` |
| supporting | `.../src/systemd/sd-messages.h` | `:178-179`, `:185` | `fb613f71807344eb29b9353cad8c09cb644fff4a18b1651fda9b49e0a23064fc` |
| supporting | `.../src/basic/process-util.c` | `:2306-2315` (`CLD_KILLED` → “killed”) | `a749f285bf168bdbb74bc7021055e8f121ec7a0bbbcb6a40e40283f5f699a4fe` |
| S014 | `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html` | HTML `:57-58`, `:71-76`, `:121-124`, `:192-207`, `:209-217`, `:230-236`, `:257-258`, `:352-356` | `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` |
| S015 | `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` | HTML `:33-42`, `:83-84`, `:100-104`, `:106-129` (kernel `:128`), `:196-197` | `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` |

S014/S015 are the systemd 262 pages. Line anchors for them are HTML lines in the fetched bytes pinned by the digest; the option/field permalink names are the drift-resistant locator if `latest` changes.

## Quote and anchor register (every quote ≤25 words)
| source | anchor | exact quote | words |
|---|---|---|---|
| S013 | `:605` | “A process of @UNIT@ unit has been killed by the OOM killer.” | 12 |
| S013 | `:615` | “the memory pressure might or might not have been caused by @UNIT@” | 12 |
| S013 | `:885` | “systemd-oomd killed one or more processes in unit @UNIT@” | 9 |
| S013 | `:890` | “One or more processes in the @UNIT@ unit have been killed by systemd-oomd” | 13 |
| S035 | `:575` | “The process' exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@.” | 12 |
| S035 | `:566` | “The unit @UNIT@ has entered the 'failed' state with result '@UNIT_RESULT@'.” | 11 |
| S015 | HTML `:34-36` | “is not supposed to be parsed for metadata” | 8 |
| S015 | HTML `:83-84` | “Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code.” | 24 |
| S014 | HTML `:193` | “This adds the match _TRANSPORT=kernel.” | 5 |
| S014 | HTML `:193` | “This implies --boot=0 unless explicitly specified otherwise.” | 7 |
| S014 | HTML `:236` | “the __CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP, and _BOOT_ID fields are always printed” | 10 |
| S014 | HTML `:209` | “formats entries as JSON objects, separated by newline characters” | 9 |
| S014 | HTML `:215` | “if a non-unique field is encountered a JSON array is used as field value” | 14 |
| S014 | HTML `:258` | “any warning messages regarding inaccessible system journals when run as a normal user” | 13 |
| S014 | HTML `:352` | “On success, 0 is returned; otherwise, a non-zero failure code is returned.” | 12 |
| S014 | HTML `:73` | “all messages that the user can see” | 7 |
| S015 | HTML `:196` | “opaque text string that uniquely describes the position of an entry” | 11 |
| S013 | `:63-64` | “Kernel messages have been lost as the journal system has been unable to process them quickly enough.” | 17 |

S036 evidence is code, not prose: `LOG_MESSAGE_ID(SD_MESSAGE_UNIT_PROCESS_EXIT_STR)`, `LOG_ITEM("EXIT_CODE=%s", sigchld_code_to_string(code))`, `LOG_ITEM("EXIT_STATUS=%i", status)` at `:6380-6389`; `sd-messages.h:185` maps the macro to `98e322203f7a4ed290d09fe03c09fe15`; `:178-179` maps `SD_MESSAGE_UNIT_FAILURE_RESULT` to `d9b373ed55a64feb8242e02dbe79a49c`; `process-util.c:2308` maps `CLD_KILLED` to “killed”.

## Distinctions the note fixes
- **Kernel OOM notice vs kernel record:** `fe6faa94…` is a unit notice that the kernel OOM killer killed a process; it is not a `_TRANSPORT=kernel` victim record, not a unique-victim count, and the catalog says cause may or may not be the unit. Kernel victim records (`Killed process`, `oom-kill:constraint=`) remain separate and are not counted by these IDs.
- **Oomd notice vs kill/process count:** `d989611b…` says “one or more processes”; its count is a unit-notice record count. A zero is not service health: `activity=unmeasured`, no `systemctl is-active`/`is-enabled` probe.
- **Coredump notices vs kills:** `fc2e22bc…` (“dumped core”) and `1f4e0a44…` (“terminated abnormally”) are crash notices, never added to a kill class.
- **Unit process exit vs cause:** `98e32220…` plus `EXIT_CODE=killed` / `EXIT_STATUS=9` counts systemd-observed signal-9 exits; it names no sender, no OOM/oomd cause, and also counts ordinary service control. `d9b373ed…` is a unit-result record, not a kill count.
- **Loss notice:** `e9bf28e6…` exists because the journal itself can lose messages; no journal class count is a complete history.
- **Scopes never summed:** user and system scopes are separate rows; unscoped output interleaves accessible journals; no total row. `MESSAGE_ID`, `EXIT_CODE` and `EXIT_STATUS` are user fields; none is authenticated producer identity.

## Pending measurements (do not cite as observed)
Expected C1 rows are exactly:
```
scope=user|system class=<label> unit=notice boot=current count=pending measurement
scope=user|system class=oomd_notice unit=notice boot=current count=pending measurement activity=unmeasured
scope=user|system state=unavailable reason=<rc|permission|boot-mismatch|persistent-logging>
```
`boot=current` is anchored: each record's `_BOOT_ID` must equal the normalized current `/proc/sys/kernel/random/boot_id` (`MORI_BOOT_ID` override); a mismatch is `unavailable`/`boot-mismatch`, never a count. Class labels: `kernel_oom_notice` (`fe6faa94…`), `oomd_notice` (`d989611b…`), `coredump_notice` (`fc2e22bc…`), `coredump_abnormal_notice` (`1f4e0a44…`), `journal_loss_notice` (`e9bf28e6…`), `unit_process_exit_sigkill` (`98e32220…` + `EXIT_CODE=killed` `EXIT_STATUS=9`), `unit_failure` (`d9b373ed…`). Every count is `pending measurement`; L1 appends after code settles. The scoped journal counts cited in this note remain the round-12 ones (5 kernel victim records, 7 user notices, 9 system notices, same boot `7bd93aee…`), a retained-boot sample cited from `kill-classes-by-message-id-r12.md`, not re-run and not a current-boot count.

## Recheck commands (from the note header)
- `curl -fsSL <pinned catalog> | grep -nE '^-- (e9bf28e6|fc2e22bc|fe6faa94|1f4e0a44|d989611b|d9b373ed|98e32220)'` → `58,66,561,568,604,870,884`.
- `curl -fsSL <pinned unit.c> | grep -nF 'EXIT_CODE=%s'` → `6388`.
- `curl -fsSL <pinned sd-messages.h> | grep -nE 'UNIT_PROCESS_EXIT_STR|UNIT_FAILURE_RESULT_STR'` → `178,185`.
- `curl -fsSL <journalctl page> | grep -nF 'id="--output-fields="'` → `230`.
- `curl -fsSL <journalctl page> | grep -nF 'JSON array is used as field value'` → `215`.
- `curl -fsSL <journal-fields page> | grep -nF 'id="MESSAGE_ID="'` → `40`.
- `curl -fsSL <journal-fields page> | grep -nF 'cannot be altered by client code'` → `83`.

## Risks and limits
- S035/S036 are cited in the note but their SOURCES rows are L1-owned and were not present when this report was written; a landed registry row must keep the declared scopes and used-by.
- Man-page `latest` URLs drift; anchors are pinned to the recorded access date and digest, not to a moving line number. `--user` depending on `Storage=` and the exact permission-denied exit code were not measured; the recipe treats any nonzero rc or unreadable scope as `unavailable`.
- `MESSAGE_ID` and `EXIT_CODE`/`EXIT_STATUS` are user fields. Counts are self-declared class/field metadata, not authenticated producer identity, and the signal-9 class is cause-blind.
- No live journal queries, no census changes, no builds/tests/lint/formatters/smoke runs. Verification is L1's integrated step.
- No tool installs or upgrades; no credential, environment or raw `MESSAGE` material handled.

## Blockers
None.
