# Round 14 — frozen fleet predicate and structured subject fields

**Scope:** read-only reconstruction for restoring the historical OOM alarm and fleet/non-fleet unit-failure routing. No production file was edited. No live command or test was run; no tool was installed.

## Finding

The pre-r13 behavior was an intentionally narrow, user-journal text heuristic: OOM- or kill-looking lines made the journal surface DRIFT; failed-unit-looking lines were split by a case-insensitive substring search for five fleet tokens, with unmatched lines explicitly routed to tsukuroi. It was not a trustworthy event counter or an exact unit-membership registry.

The smallest structured subject-field analogue is to keep the unit-failure catalog selector (`MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`) and project the failed **subject** unit (`USER_UNIT` for user-manager records; `UNIT` for system-manager records), then apply the same legacy token set to that subject value. `UNIT_RESULT` is additionally needed to recover the structured `oom-kill` result path. Do not substitute `_SYSTEMD_UNIT` / `_SYSTEMD_USER_UNIT`: those identify the emitting process's unit, not necessarily the failed subject. Missing or malformed subject metadata cannot safely be called non-fleet; it is unknown. `UNIT`, `USER_UNIT`, `UNIT_RESULT`, and `MESSAGE_ID` are user journal fields, so this is structured classification, not authenticated provenance.

**Retained-boot witness narrows B's actual OOM trigger.** The read-only `NoHarmReview.md` NH3 evidence reports that `Failed with result 'oom-kill'` matched B's OOM regex, while the pinned `fe6faa94…` kernel-OOM notice wording did not; the observed B OOM alarm was therefore `UNIT_RESULT=oom-kill`, not a kernel-notice count (`NoHarmReview.md:13–16,28–32`). The same evidence says B's `KILL_SIGNAL_JOURNAL` regex also matched `Failed with result 'signal'` (`:16`); that is broader than the later explicit SIGKILL record selector.

**Concrete routing limitation.** NH3 reports the five-token predicate classified all 4 retained user `UNIT_RESULT=oom-kill` records as non-fleet (user `USER_UNIT` nonfleet 4597/4597; system `UNIT` nonfleet 1/1). The four user records name `arc2-r*-*.service` / `run-p*-i*.scope` kaidoku workloads, documented as `systemd-run --user` scopes/transient services in `kaidoku-shokunin/corpus/lessons/2026-10-18-caller-independent-services.md:8–17`. This is B parity, not a complete fleet-unit taxonomy (`NoHarmReview.md:17–23,40–44`).

## Evidence chain

### 1. Pre-r13 frozen behavior

The before-state source is `.ufo/waves/round-13/frozen/mori-census.sh`, `probe_journal()` at lines 847–911. The outside r13 spotcheck independently compares that frozen source with the delivered source and records the rejected-harmed regression (`corpus/lessons/round-13-verifier-spotcheck.md:5–7,76–89`).

Exact historical predicates (`frozen/mori-census.sh:854–911`):

- One query: `journalctl --user -b --no-pager`; it examined the current user's journal only.
- `c_oom` was the count of output lines matching, case-insensitively, `Out of memory|oom-kill|oom_reaper|Killed process` (`:874`).
- `c_kill` was the count of lines matching `status=9/KILL|Failed with result .signal|SIGKILL` (`:875`).
- The function set the journal surface to DRIFT if `c_oom > 0` or `c_kill > 0`; it emitted `OOM_KILL_JOURNAL crit` when `c_oom > 0`, and `KILL_SIGNAL_JOURNAL warn` when `c_kill > 0` (`:893–900`).
- Unit routing first counted failed-unit-looking lines with `Failed with result|Unit entered failed state`; its fleet subset was those lines also matching, case-insensitively, `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` (`:887–892`). A positive fleet subset emitted `UNIT_FAILURE_JOURNAL info` with `scope=fleet-units` (`:904–906`). If total unit-failure lines exceeded that subset, the difference emitted `UNIT_FAILURE_OUT_OF_SCOPE info` and explicitly said `non-fleet units (desktop/OS) — tsukuroi owns these` (`:907–909`).
- The surface row exposed the total text-derived counters and command (`:911`). Segfault/unit-failure counts were informational; only the OOM and kill-signal conditions changed the journal surface to DRIFT (`:853,893–911`).

This is a line-count predicate, not a unique journal-record, failed-unit, killed-process, or victim count. The fleet test was unanchored against the whole rendered line, not against a parsed unit name.

### 2. Fleet root and naming convention observed statically

- The fleet configuration identifies `/home/vgpnk/Projects/shokunin` as `SHOKUNIN_ROOT` (`shokunin.conf:6–8`). Mori derives the parent of a `*-shokunin` lane checkout as its default root and reads `shokunin.conf` as its fleet configuration (`tools/mori-census.sh:191–227,261–269,344`).
- `shokunin.conf:16–17` defines each lane entry as `<lane-id>|<repo-relative-to-SHOKUNIN_ROOT>|<axes>`. Entries use repository names such as `mori-shokunin`, `tsukuroi-shokunin`, `kumitate-shokunin`, and `mado-shokunin` (`:45–64,71–83`); `protocol` and `aggregator` point at `.` (`:20–21`). The current directory inventory likewise shows sibling repositories named with the `*-shokunin` suffix.
- The config's launch command is `omp -p --cwd "%C" "@%P"` (`shokunin.conf:24–28`). It declares lane IDs and working directories, not a systemd-unit allowlist or a mapping from every lane/repository to a manager unit. Thus the repo-root naming convention alone does not establish all fleet systemd subject-unit names.

### 3. Structured fields and the minimum analogue

- The pinned systemd catalog records `d9b373ed…` as “Unit failed”, with the subject unit and `UNIT_RESULT`; `UNIT_RESULT` can describe non-signal failures too (`corpus/knowledge/structured-journal-scopes-r13.md:13–14`; `corpus/SOURCES.md:41–43`). `98e32220…` is a separate process-exit record requiring `EXIT_CODE=killed` and `EXIT_STATUS=9` to select its SIGKILL subset; that record does not provide sender or cause (`structured-journal-scopes-r13.md:13–14,42–47`).
- The systemd 262 `systemd.journal-fields(7)` entry for `UNIT=` and `USER_UNIT=` says they name units about which the system or user manager logs, and documents matching `UNIT=name.service` / `USER_UNIT=name.service` for `journalctl --unit` / `--user-unit`. The trusted `_SYSTEMD_UNIT=` and `_SYSTEMD_USER_UNIT=` fields instead describe the unit of the process the journal entry originates from. See the [official field reference](https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html#UNIT=).
- Minimum output projection for unit-failure routing is `_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT` for the selected failure records; add `UNIT_RESULT` for the OOM-result arm. For each manager scope, classify the corresponding subject field using the legacy case-insensitive token set `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet`. The rule is: matching subject → fleet route; present, well-formed subject with no match → non-fleet route to tsukuroi; absent/invalid/ambiguous subject → unknown, not a fabricated non-fleet result. The historic baseline only queried `--user`; system-scope routing would be an explicit coverage extension, not part of the old invariant. Keep user/system counts separate.
- `UNIT_RESULT=oom-kill` on the `d9b373ed…` unit-result record is a structured OOM signal. The `fe6faa94…` kernel-OOM catalog ID is a per-unit **notice**, not a unique-victim count; it can also say the memory pressure may or may not have been caused by that unit (`structured-journal-scopes-r13.md:10–14`). A structured alarm can preserve the old critical/DRIFT behavior without claiming a victim count or restoring MESSAGE parsing. If both notice and unit-result records describe one incident, do not add them and report the sum as a number of kills. **The fleet-token predicate is only a unit-failure routing label; it MUST NOT suppress or downgrade any positive OOM alarm.**

The same retained-boot evidence reports system `fe6faa94…` notices with `UNIT=user@N.service` four times (`NoHarmReview.md:17–23`). This broad user-manager envelope contains fleet work but is not a per-workload subject; the legacy tokens miss it, while treating the envelope itself as fleet would overstate event attribution. Thus the five-token projection is the smallest B-parity structured rule, not a fully accurate live fleet-membership classifier. Do not silently expand it to `arc2-*`, `run-*`, or the `user@N.service` envelope: those are semantic changes requiring an explicit owner/scope decision. Keep any such coverage claim bounded.

### 4. Current divergence

The current production `probe_journal()` projects only `_BOOT_ID,MESSAGE_ID` for the generic `unit_failure_record` query (`tools/mori-census.sh:1031–1073`), then emits one `UNIT_FAILURE_JOURNAL` / `_SYSTEM` finding with `no fleet classification` (`:1101–1102`). It does not query `UNIT`, `USER_UNIT`, or `UNIT_RESULT`, and the current class loop defaults journal findings to INFO; only the user `unit_sigkill_record` is WARN (`:1085–1106`). It therefore neither restores the critical OOM journal alarm nor preserves the former fleet/non-fleet owner split.

The r13 non-author spotcheck measured the old source as one OOM-critical and one non-fleet-route emission, versus zero of each in delivered source (`round-13-verifier-spotcheck.md:76–89`). It specifically rejects using the existing cgroup counter as a blanket replacement: the code prefers `memory.events.local` or a `user@UID.service` counter, while descendant or out-of-scope journal events are not guaranteed to appear in that selected counter (`round-13-verifier-spotcheck.md:84–85`; current cgroup selection `tools/mori-census.sh:1143–1165,1295–1300`).

The current `PROVINCE.md:24` already states the desired behavior—positive OOM notices and observed `UNIT_RESULT=oom-kill` retain critical `OOM_KILL_JOURNAL`/DRIFT, and failed-unit subject metadata restores fleet-only `UNIT_FAILURE_JOURNAL` versus non-fleet `UNIT_FAILURE_OUT_OF_SCOPE` with tsukuroi routing. That is contract prose; the production code above is the observed implementation and still diverges.

## Limits and confidence

- **Historical predicate — high confidence:** read directly from the frozen source and corroborated by the outside verifier's before/after source comparison. It was current-user-only, message-text-based, and substring-based; it did not prove fleet causation or count victims.
- **Structured field choice — high confidence for field semantics; moderate confidence for coverage:** the pinned catalog and primary docs support the result and subject-field choices. This seat did not query live records; the read-only retained-boot sample reported in `NoHarmReview.md:17–23` supplies concrete field-presence and naming evidence, not a complete inventory. `UNIT`/`USER_UNIT`, `UNIT_RESULT`, and `MESSAGE_ID` are user fields, not an authentication boundary.
- **Current fleet mapping — bounded and demonstrably incomplete:** current configuration exposes lane/repository names and an OMP working-directory launch convention, not a complete systemd-unit map. Reusing the five old tokens exactly preserves B's heuristic, but NH3 reports it misses all observed failed-unit records in the retained sample, including all four kaidoku OOM-result records. This is parity with B, not proof of fleet coverage. Keep missing subject metadata distinct from non-fleet, and do not silently replace the legacy tokens with new unit-name patterns.
- **No live state claim:** this seat ran no journal query, systemd unit inventory, test, or census. Retained-boot counts above are attributed to the read-only `NoHarmReview.md` evidence and were not re-executed here.
- **LSP unavailable:** `read xd://lsp` returned `No such tool`; no LSP endpoint was mounted. Grep was used only to locate source anchors; the predicate and divergence above are based on directly read source and the committed verifier report.
