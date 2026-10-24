# RoutingAttack — round 14 critic report (structured fleet routing)

Seat: `MoriR14.RoutingAttack` (critic, leaf). Axis: coverage. Milestone: restore OOM alarm and structured fleet routing.
Scope: attack the planned structured replacement for the historical fleet/non-fleet unit-failure split (`UNIT_FAILURE_JOURNAL` fleet vs `UNIT_FAILURE_OUT_OF_SCOPE` non-fleet, tsukuroi). Report only. No lane file except this report was written. No census, gate, selftest or lane tool was run.

State when reviewed: `git status` showed `tools/mori-census.sh` unmodified (r13 H bytes, probe_journal :1031–1130), and `tools/mori-round14-regressions.py` did not exist yet. Findings are therefore design hazards for CensusRepair/JournalRegression, checked against the frozen and current source, pinned systemd source, and the live journal. The hazards (items 1–6 of §3) went directly to `MoriR14.CensusRepair` (delivered), as the parent asked.

## 1. Exact historical semantics (what "restore" must mirror)

Source: `.ufo/waves/round-13/frozen/mori-census.sh` (spot-check verifies these bytes equal B `tools/mori-census.sh`, sha `3da5b098…`), lines 855–911:

| Aspect | Historical behavior | Line |
|---|---|---|
| Journal read | `journalctl --user -b --no-pager` (short text), **user scope only**; system journal never read | :855,865 |
| Universe | text lines matching `-iE 'Failed with result\|Unit entered failed state'` | :890 |
| Fleet predicate | same lines, then `grep -ciE 'shokunin\|ufo-sighting\|tmux-spawn\|the-tick\|fleet'`. This is a **case-insensitive unanchored substring match over the whole short-format line** (hostname, identifier[pid] and MESSAGE, which embeds the unit name) | :891 |
| Fleet finding | `UNIT_FAILURE_JOURNAL` **info**, `class=unit_failure count=N scope=fleet-units`; does **not** set `st=drift` | :904–906 |
| Non-fleet finding | `UNIT_FAILURE_OUT_OF_SCOPE` **info**, `count=total−fleet note=non-fleet units (desktop/OS) — tsukuroi owns these`; no `owner=` token; no drift | :907–909 |
| OOM | `OOM_KILL_JOURNAL` crit → `st=drift`, user scope only, text `Out of memory\|oom-kill\|oom_reaper\|Killed process` | :874,893–895 |

Note that the historical `oom-kill` text alternative also matched the `Failed with result 'oom-kill'` unit-failure line, so a unit OOM result raised the crit alarm before r13. That supports CensusRepair's "account UNIT_RESULT=oom-kill" requirement as a restoration and not new scope (that fallout is the OOM seat's to judge).

**Severity defect in the round-14 brief:** the JournalRegression prompt asks for "fleet UNIT_FAILURE_JOURNAL **warn**". History is **info** (frozen :905), and the parent confirms INFO. In the current census `warn|crit` flips ROLL to DRIFT (`tools/mori-census.sh:392–402`). So a warn expectation would either fail the repaired census or force a new DRIFT on every fleet unit failure. Either outcome is a semantics change, not a restoration. Gate expectations must be `UNIT_FAILURE_JOURNAL severity=info` and `UNIT_FAILURE_OUT_OF_SCOPE severity=info`, and neither may set DRIFT by itself.

## 2. Emitter schema (sourced)

Pinned systemd `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` (S036), fetched 2026-10-20:

- `src/core/unit.c:6995–6997`: `unit_log_field(u)` = `MANAGER_IS_SYSTEM ? "UNIT=" : "USER_UNIT="`. `unit_log_failure` (:6333–6342) writes `MESSAGE_ID=d9b373ed…`, `UNIT_RESULT=%s` and the unit message through `log_unit_struct`, which appends `LOG_UNIT_ID(u)` (`unit.h:1174,1194`).
- `unit.h:1170–1174`: `log_unit_struct_errno` does `LOG_CONTEXT_PUSH_IOV(_c->log_extra_fields…)`. A unit's own `LogExtraFields=` therefore travel on the manager's record **about** that unit.
- `src/shared/logs-show.c:1114–1128`: in `-o json`, a field seen twice becomes a JSON **array**. An unprintable value becomes a **byte-number array**. A value with name+1+size ≥ 4096 becomes **null**.
- `src/libsystemd/sd-journal/sd-journal.c:1580–1610`: `--user` selects **files** `user-<uid>*.journal`; it is not a field filter. `src/journal/journald-manager.c:509–545,1181–1192`: user records go to the user file only with persistent storage and split-by-uid, and only once no runtime journal is open. Otherwise they go to the system file. Uids below 1000 (system users) always go to the system journal.
- `logs-show.c:1721–1807`: journalctl's own `-u`/`--user-unit` match ORs subject **and** emitter fields (`_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT`, `UNIT`+`_SYSTEMD_CGROUP=/init.scope`, `USER_UNIT`+`_UID`, `OBJECT_SYSTEMD_*`, `COREDUMP_*`).

Live host (`plazir27`, systemd 261.2, persistent, split uid: `/var/log/journal/<id>/user-1000*.journal` present), read-only `journalctl … MESSAGE_ID=d9b373ed55a64feb8242e02dbe79a49c`, all boots:

| Scope | Records | Subject field | Emitter fields |
|---|---|---|---|
| `--user` | 4609 (5 boots) | `USER_UNIT` string in all; `UNIT` absent in all | `_SYSTEMD_UNIT=user@1000.service`, `_SYSTEMD_USER_UNIT=init.scope`, `_COMM=systemd`, `_UID=1000` in all |
| `--system` | 1 | `UNIT` string; `USER_UNIT` absent | `_SYSTEMD_UNIT=init.scope`, `_COMM=systemd`, `_UID=0` |

The current boot holds 0 records in either scope. `journalctl --system -F USER_UNIT` and `journalctl --user -F UNIT` both returned empty on this host.

## 3. Counterexamples, evidence and smallest safe corrections

Synthetic adversarial records were evaluated with jq in `/tmp/rattack` (not lane code). Predicate: `P='shokunin|ufo-sighting|tmux-spawn|the-tick|fleet'`, applied as `test($p;"i")`.

### 3.1 Classifying the emitter instead of the subject → fleet bucket always empty
- **Counterexample:** keying on `_SYSTEMD_UNIT` (or `_SYSTEMD_USER_UNIT`). Every live user record reads `user@1000.service`/`init.scope`, and every system record reads `init.scope`. The synthetic set with 2 real fleet subjects gave `{"fleet":0,"n":9}`.
- **Impact:** coverage. Every fleet failure is silently routed to tsukuroi as OUT_OF_SCOPE, which repeats the r13 adjacency harm.
- **Correction:** the subject is `USER_UNIT` (user manager) or `UNIT` (system manager) only. Add both to `--output-fields`. Never read `_SYSTEMD_*` for classification, and never use `-u`/`--user-unit` globs, because those OR in emitter and `OBJECT_*` fields (logs-show.c:1729–1741, 1774–1786).

### 3.2 Scope ↔ field coupling
- **Counterexample A:** requiring `UNIT` in user scope makes all 4609 live user records unknown. Requiring `USER_UNIT` in system scope makes the system record unknown.
- **Counterexample B:** a hard "user→USER_UNIT, system→UNIT" binding rejects legitimate system-file `USER_UNIT` records: uid<1000 user managers, records written while a runtime journal is open, and the user-file-open fallback (journald-manager.c:524–544). None appear on this host now, but they are source-possible.
- **Correction:** in both scopes, the subject = the single present string among {`UNIT`,`USER_UNIT`}. Both present, or neither present, means unknown. Keep scopes as separate rows/counts; never sum them (current r13 contract).
- **Historical boundary:** history read the user scope only. Applying the fleet split to system-scope records is new semantics, not restoration. Label it as such. On this host the one system record (`systemd-coredump@….service`, oom-kill) routes non-fleet.

### 3.3 Arrays and stringification
- **Counterexample:** `"USER_UNIT":["pipewire.service","shokunin"]` (duplicate field from `LogExtraFields=USER_UNIT=…` or a forged client record). `(.USER_UNIT|tostring)|test(P;"i")` → **true**, a false fleet hit, observed. A raw `.USER_UNIT|test(...)` → `jq: Error: cannot use [...] as string`, rc 5, observed. Under current `journal_query` that turns the **whole class** into `malformed-json` unavailable, so one hostile record blanks every count. A byte array (unprintable) and a null (≥4096) are the same family.
- **Correction:** gate every subject on `type=="string"`. A non-string goes to the per-record `unknown` bucket. No `tostring`, `ascii_downcase` or `test` before the type check. The existing SIGKILL filter's `(.EXIT_STATUS|tostring)=="9"` pattern is safe only for equality and must not be copied into a substring test. Apply the same rule to `UNIT_RESULT`: only `type=="string" and .=="oom-kill"` counts as oom-kill. An injected array is unknown, not oom-kill.

### 3.4 Missing and malformed subjects
- **Counterexamples:** a record without either field (any same-uid process can `sd_journal_send MESSAGE_ID=d9b373ed…`), `USER_UNIT=""`, both fields present, or a byte array. All four must be unknown. Folding them into non-fleet would falsely route to tsukuroi with fake precision. Folding them into fleet would fabricate fleet failures.
- **Over-strict validation counterexample:** unit names legally contain `\` escapes, `:` and one `@` (`src/basic/unit-name.c:19–26,40–70`; length < 256, `UNIT_NAME_MAX` 256, suffix must be a unit type). Live desktop scope from fleet evidence: `app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope` (`.ufo/waves/shokunin12h-20261014-p4-mori-r1/members/CgroupMemoryEvents.md:281`). Rejecting backslash would mislabel ordinary desktop/OS units unknown.
- **Validated partition (observed):** fleet / nonfleet / unknown = **2 / 2 / 5**. Fleet: `mori-shokunin-tick.service` and the false positive `app-flatpak-com.jetbrains.Fleet-4242.scope`. Nonfleet: `pipewire-pulse.service` and the `\x2d` scope. Unknown: array, missing, empty, byte-array, both-fields.
- **Correction:** this is a *suggested* subject validator, not a full reimplementation of `unit_name_is_valid`: string, 1–255 bytes, `^[A-Za-z0-9:_.\\@-]+\.(service|socket|target|device|mount|automount|swap|timer|path|slice|scope)$`. Emit `total = fleet + nonfleet + unknown` as validated integers per scope. Report unknown>0 explicitly, for example `unit_class_unknown=K` on the row or an info finding. Never echo subject bytes.

### 3.5 Substring false positives and false negatives (honest boundary)
- **False positive (kept by an exact mirror):** a case-insensitive unanchored `fleet` matches desktop apps such as `…com.jetbrains.Fleet…` (synthetic). Any desktop unit containing `shokunin`/`fleet` routes to mori.
- **False negatives (live, decisive):** across all 4609 user and 1 system historical records, the subject partition is **fleet 0 / nonfleet 4609 / unknown 0** (user) and **0/1/0** (system). There are 5 oom-kill results in total: user `arc2-r8-ctl.service`, `arc2-r10-mid.service`, `run-p4175743-i29293759.scope`, `run-p2866091-i19650632.scope`, and system `systemd-coredump@11-…service`. `systemctl --user list-units --all` shows **no** unit matching any historical token. Fleet work launched from terminals lives in `app-Hyprland-…scope` (CgroupMemoryEvents.md:281–282). So the name rule can say "no token", never "proven non-fleet". `arc2-r8-ctl.service` origin is not found in the repo; whether it is fleet work is [INFERENCE] unresolved.
- **Hostname dependency in history:** the frozen grep matched the whole line, so a host whose name contains a token would have classified *every* failure as fleet. Subject-only matching equals the historical result for systemd-emitted records on host `plazir27`, and for result strings, since no `UNIT_RESULT` value contains a token. It intentionally drops two things: text lines from non-manager processes and the obsolete `Unit entered failed state` wording. Disclose this as "predicate mirrored on subject; universe now catalog record, not text line". Do not claim count equivalence.
- **Correction:** keep the exact tokens, `-i` and substring (mirror; any anchoring or tightening is a semantics change that needs its own evidence). Label `rule=historical-name-token`, and qualify non-fleet as `no-fleet-token`, not "desktop/OS proven". Make the `UNIT_RESULT=oom-kill` alarm **independent of the partition** so a misrouted fleet OOM still alarms (all 4 live user oom-kill units would otherwise go only to tsukuroi info).

### 3.6 Trust / authentication boundary
- `UNIT`, `USER_UNIT` and `UNIT_RESULT` are client fields. journalctl itself trusts a system `UNIT` only together with `_SYSTEMD_CGROUP=/init.scope`, and trusts a user `USER_UNIT` only together with `_UID=<uid>` (logs-show.c:1735–1736, 1779–1780). Any same-uid process can therefore forge a user-scope record that journalctl itself would attribute.
- **Correction:** keep `trust=client-supplied` on the routed counts, and claim no emitter authentication. An optional emitter cross-check (system `_SYSTEMD_UNIT=init.scope`; user `_SYSTEMD_USER_UNIT=init.scope`) may be *reported*, but it must not filter silently. Otherwise records from uid<1000 or fallback paths vanish instead of becoming unknown.

### 3.7 Counting hazards
- One OOM event can yield several records: kernel `fe6faa94` notice, `98e32220` process exit and `d9b373ed` oom-kill result. `arc2-r8-ctl.service` has all three live (one each). Keep the classes distinct and never sum them into a "kills" total; the r13 notice≠kill rule still applies.
- `UNIT_FAILURE_JOURNAL` must count only fleet-token subjects. It must not reuse the r13 meaning "all user-unit results" (spot-check routed defect 2).

## 4. Required gate assertions (for JournalRegression / HarnessMigration)

1. User fixture with `USER_UNIT` holding a token and emitter `user@1000.service` → `UNIT_FAILURE_JOURNAL severity=info`, no DRIFT from that finding alone.
2. User non-token `USER_UNIT` → `UNIT_FAILURE_OUT_OF_SCOPE severity=info` naming tsukuroi; no DRIFT.
3. Emitter-trap fixture: emitter fields contain a token, subject does not → non-fleet (and the reverse).
4. Array, missing, empty, both-fields and byte-array subjects → unknown count, never fleet or non-fleet, and the class stays available.
5. `\x2d`-escaped valid unit → classified, not unknown.
6. System-scope `UNIT` and system-file `USER_UNIT` fixtures, plus `UNIT_RESULT=oom-kill` with a non-token subject → OOM alarm still fires.
7. No subject bytes and no MESSAGE canary appear in the output.

## 5. Impacted axes
- **coverage:** primary; the fleet split exists only if subject fields are used correctly.
- **adjacency:** a false tsukuroi route via unknown→nonfleet or emitter keying.
- **calibration:** `warn` vs historical `info`, and "non-fleet" overstated as proven.

All are fixable defects, not tradeoffs, except one: the name-token predicate has inherent recall limits (zero live hits). The canonical judge should accept that only if it is labeled as such.

## 6. Tooling / provenance
- No tools installed or updated.
- Network: fetched pinned systemd files at `cf8ebfc6…` with curl into `/tmp/rattack`: `src/core/unit.c`, `unit.h`, `service.c`, `src/shared/logs-show.c`, `src/libsystemd/sd-journal/sd-journal.c`, `src/journal/journald-manager.c`, `journalctl*.c`, `src/basic/unit-name.c` (+ `.h`), `catalog/systemd.catalog.in`.
- Live reads: read-only `journalctl --user/--system -o json --output-fields=…`, `-F`, `systemctl --user list-units/list-unit-files`. MESSAGE was never requested.
- Scratch: `/tmp/rattack/recs.json`, outside the lane.

## 7. Addendum — CensusRepair settled-design check (source-only)

CensusRepair's settled message:
- **Subject:** taken from `UNIT` and `USER_UNIT` in both scopes. Exactly one present is the subject; both or neither is unknown; `_SYSTEMD_*` is never used.
- **Validation:** string of 1–255 characters, systemd charset including `@`, `:` and `\`, known unit suffix.
- **Partition:** disjoint, total = fleet + nonfleet + unknown; unknown is never folded into OUT_OF_SCOPE.
- **Predicate:** case-insensitive token substring over the subject only, labeled name-token; nonfleet means no token (a routing hint, not proof).
- **Findings:**
  - `UNIT_FAILURE_JOURNAL` info, owner mori (fleet).
  - `UNIT_FAILURE_OUT_OF_SCOPE` info, `owner=tsukuroi` (non-fleet).
  - `UNIT_ATTRIBUTION_UNKNOWN` info (unknown subject).
  - `_SYSTEM` variants of each for the system scope.
- **OOM:** `UNIT_RESULT_OOM_KILL_JOURNAL(_SYSTEM)` crit, independent of the partition. A non-string or missing result is `unit_oom_result_unknown`, not oom.

**Status:** `tools/mori-census.sh` was still the r13 bytes when checked (mtime 01:26:50, size 173544, no repair identifiers found by grep). Only the design was checked; the written code has not been reviewed.

The design closes §3.1–§3.6. Remaining items, sent to `MoriR14.CensusRepair`:

1. **Presence test.** Use `has("UNIT")`/`has("USER_UNIT")`, not `!= null`. A field of 4096 bytes or more is emitted as JSON null (logs-show.c:1114), so `{UNIT:null, USER_UNIT:"x.service"}` must be unknown (both fields present). The jq demo in §3.4 used `!= null` and understates this case.
2. **One pass.** Derive the oom-kill count and the partition from the same `d9b373ed` record set in one jq pass, so oom-kill ⊆ total. A second `UNIT_RESULT=oom-kill` journalctl query can race the first, and it also matches records whose duplicated `UNIT_RESULT` array contains `oom-kill`.
3. **ID universe change.** `UNIT_FAILURE_JOURNAL_SYSTEM` meant all system unit failures in r13 (current :1027) and becomes fleet-only. The pre-r13 history had no system scope at all, so the system fleet split is new semantics. Document both in the stable-id header (:239–241) and in the probe comment (:913–918, which still says "no fleet classification"). This is required by spot-check routed defect 2.
4. **Existing selftest lines.** :2769 expects `UNIT_FAILURE_JOURNAL info` from a fixture whose subject carries no token. :2788 fails on any `OOM_KILL_JOURNAL` or `UNIT_FAILURE_JOURNAL` finding. Both must migrate with the repair.
5. **Escaping witness.** Add a selftest fixture `app-Hyprland-xdg\x2dterminal\x2dexec-dd9e67bd.scope` → classified nonfleet, so a bash→jq backslash-quoting bug in the charset fails red.
