# JSONAttack — round 13 critic: structured journal counting

Seat: MoriR13.JSONAttack (critic). Axes: **coverage**, **operability**. Read-only.
I did not run the census, its selftest, the oracle, or any journal content query.
I did not read MESSAGE or a process environment, and I made no remediation.

What I did run:
- Parser behaviour probes with jq on **synthetic strings only** (no journal bytes).
- Read-only host metadata: `getfacl`/`stat`/`getfattr` on journal and cgroup directories, `systemctl is-active systemd-oomd`, `type -a jq`.
- Upstream source reads, systemd tag v261 (the host runs `systemd 261 (261.2-1-arch)`).

The target is the in-flight `tools/mori-census.sh` at snapshot tag **B8B7** (3166 lines, being edited by CensusFix). Line anchors below refer to that snapshot and may shift.

Tool installs: none.

## Verdict summary

The structured direction is right. It already gets these right:
- `-q` is used.
- A nonzero rc is reported as unavailable.
- MESSAGE is not requested.
- Malformed JSON is reported as unavailable.
- Scopes are never summed.

**Six defects still let a false 0, a silent partial count, or a single-record denial of service get through.** Each one has a small fix.

| # | Severity | Class | Axis harmed |
|---|---|---|---|
| D1 | high | an empty scope or a system-uid run reads as a valid 0 (empty vs denied) | coverage |
| D2 | high | records are never checked against the *current* boot | coverage |
| D3 | high | stderr is merged into stdout, so partial-file warnings are mislabelled `malformed-json` | operability |
| D4 | high | unbounded: no timeout, full slurp, whole output held in a shell variable | operability |
| D5 | medium | one spoofed array/null `MESSAGE_ID` record makes the whole class `record-invalid` | operability, coverage |
| D6 | medium | MESSAGE_ID is a client field; no emitter pin, and the finding names imply the emitter | coverage (claim honesty) |
| D7 | low | `segfault_signal11` is claimed as a subset of coredump records but is not one by construction | coverage |
| D8 | low | parser identity is resolved through PATH: a user-writable `~/.local/bin/jq` shadows `/usr/bin/jq`, and the harness shell has a jaq builtin | operability (provenance) |
| D9 | low | the selftest journal stub ignores its arguments, so scope and class independence cannot be tested | coverage of tests |

---

## D1 — empty scope, missing scope or system uid reads as a valid 0

**Counterexample.** These cases all exit rc 0 with empty stdout under `-q`:
- `journalctl --user` on a host whose journal is volatile.
- `journalctl --user` with `SplitMode=none`.
- `journalctl --user` with no `user-UID*.journal` files at all.

The jq filter at `mori-census.sh:890` maps `[]` to `0 0 none` (comment at `:889`). Every user class is then reported as `ok` with value `0`.

**Evidence.**
- `src/shared/journal-util.c` (v261), `journal_access_check_and_warn`: when `j->errors` is empty and no files exist, the only output is `log_notice("No journal files were found.")`, gated by `!quiet`. It returns 0.
- journalctl(1), local man page lines 95-96: "Note that --user only works if persistent logging is enabled".
- **Partial permission.** When some files hit EACCES but at least one opened, the EACCES case is `continue` (no warning). The hint goes through `access_check_var_log_journal` only if `!quiet`. The error `"No journal files were opened due to insufficient permissions."` fires **only** when `ordered_hashmap_isempty(j->files)`. So partial access is rc 0 and fully silent under `-q`.
- **System uid.** `src/libsystemd/sd-journal/sd-journal.c:1534-1551` (v261): under `SD_JOURNAL_CURRENT_USER`, a system uid (root, or a system-unit/cron context) also gets `SD_JOURNAL_SYSTEM`. The **user row then silently reads system files**, so the two rows are no longer independent scopes.
- **Total denial is handled.** The census treats rc 1 as unavailable (`:900-903`). The baseline treated rc 1 as valid ("1 can mean empty", old `:868-869`). That was the original false-0 path, and the new code has removed it.

**Impact.** Coverage. A 0 is published for a scope that was never read (QUALITY #6: unreadable-input canary; QUALITY #16: scope must be named truthfully).

**Smallest correction.**
1. **Per-scope liveness canary**, run before the class queries:
   `journalctl <flag> -b -q --no-pager -o json --output-fields=_BOOT_ID -n 1`
   It must return exactly one object whose `_BOOT_ID` equals the current boot (D2). Otherwise every class in that scope is `unavailable:scope-empty`.
   A live login always has user-journal records for the current boot, and PID1 always writes system-journal records.
2. If `id -u` is a system uid (`< 1000`, matching `uid_for_system_journal`), the user scope is `unavailable:system-uid`. Print `uid=` in the user row.
3. **Optional access predicate**, the same one journalctl itself uses (journal-util.c `access_check_var_log_journal`): uid 0, or member of `systemd-journal`, or member of a group in the default ACL of `/run/log/journal` (else `/var/log/journal`). Emit it as `journal_access=root|group|acl-group|none`.
   Measured on this host: `getfacl /var/log/journal` shows `default:group:wheel:r-x`, `default:group:adm:r-x`, and `id -nG` includes `wheel`, so the value here is `acl-group`.
   **Residual:** one file with an inconsistent ACL is still silent. Name it; do not claim it is covered.

## D2 — boot identity is only checked for agreement between records, never against the current boot

**Counterexample.** A journalctl that ignores `-b` and returns records from a single other boot passes. The current selftest stub ignores all arguments (`:2164-2170`), and a future option change could do the same. Lines `:914-926` only require that all records share **one** boot of length ≤ 64.

There is a second problem: `JQ_BOOT` comes from the first record. An empty but healthy scope therefore prints `user_boot=unavailable:no-records` (`:1000`). That loses the counter anchor that QUALITY #12 requires.

**Smallest correction.**
- Read the current boot id once: `/proc/sys/kernel/random/boot_id` with dashes stripped, overridable by `MORI_BOOT_ID` for fixtures.
- Pass it as `--arg boot`.
- Require every record to satisfy `._BOOT_ID == $boot` and `test("^[0-9a-f]{32}$")`. A mismatch gives `unavailable:other-boot`.
- Print `boot=` from that source, never from the records.
- This removes the ad-hoc `${#boot} -gt 64` check at `:925` and the `boot-conflict` bookkeeping at `:972-978`.

## D3 — `cap` merges stderr into the parsed bytes

**Counterexample.** `journal_query` calls `cap` (`:899`), and `cap` runs `CAP_OUT=$("$@" 2>&1)` (`:508-513`). Under `-q`, journalctl still writes these warnings with **rc 0**:
- `"Journal file %s is truncated, ignoring file."`
- `"... corrupted, ignoring file."`
- `"... uses an unsupported feature, ignoring file."`
- `"Too many journal files (limit is at %u) in scope, ignoring file"`

These are warnings, not `log_notice`, so `quiet` does not gate them (journal-util.c, `journal_access_check_and_warn` switch). The merged text makes jq fail, and the class is reported as `malformed-json`. That is fail-closed, but the label is wrong: the real condition is that files were skipped, i.e. a partial count. An inherited `SYSTEMD_LOG_LEVEL=debug` produces the same symptom. An inherited `SYSTEMD_LOG_TARGET=journal` or `SYSTEMD_LOG_LEVEL=err` makes those warnings vanish, giving a **silent partial count**.

**Probe (synthetic).** One stderr line in front of a valid record:
- jq-1.8.2 (`/usr/bin/jq` and `~/.local/bin/jq`): rc 5, `Invalid numeric literal at line 1, column 5`.
- jaq 3.1.1: rc 5, `expected digit`.

**Smallest correction.**
- Capture stdout and stderr separately. Count stderr lines but never echo them; they contain journal file paths.
- stdout fails to parse → `malformed-json`.
- stdout parses but stderr is nonempty → `unavailable:partial-files stderr_lines=N`.
- Pin the child environment: `SYSTEMD_LOG_LEVEL=warning SYSTEMD_LOG_TARGET=console SYSTEMD_COLORS=0 LC_ALL=C`.
- Keep `-q` mandatory. Without it, journalctl prints `-- No entries --` on **stdout** for an empty result (`src/journal/journalctl-show.c:605-606`, v261), and that breaks the JSON.

## D4 — unbounded runtime and memory

**Counterexample.** Eight sequential journalctl calls run with no wall-clock bound. `run_timeout` exists (`:515-528`) but is unused here. Each call buffers its whole output in `CAP_OUT`, passes it through a here-string, and runs `jq -s` (slurp) over it (`:905-907`).

A same-uid process can append matching records:
- `MESSAGE_ID` is a client field (D6).
- journald drops only above `RateLimitBurst=10000` per `RateLimitIntervalSec=30s` **per service** (journald.conf(5), local man page :160-168).
- That allows about 1.2 M matching records per hour per unit.

**Recommended limits.** These are labeled-local placeholders, following the same convention as `:303-311`.
- **`JOURNAL_TIMEOUT_S=10` per query**, through `run_timeout`. rc 124 → `unavailable:timeout`; no timeout binary → `unavailable:no-timeout-bin` (the existing convention at `:519-520`).
- **`JOURNAL_MAX_RECORDS=10000` per class and scope**, enforced with `-n $((JOURNAL_MAX_RECORDS+1))`.
  - More than the maximum → `count=saturated>10000`, status `saturated`. It is not a number and must not be compared or masked as one.
  - Basis: the highest measured class is 656 signal-11 coredump records in one boot (`mori-census.sh` baseline comment, old `:877-878`; LOG.md round-1 correction 7), so 10000 is about 15× headroom.
- **Never pass `--all`.** Without it, any field larger than 4096 bytes is encoded as `null` (journalctl(1) local man page :436-438). With the restricted `--output-fields`, each record stays at a few hundred bytes. Worst case: 10001 records × (4 always-on fields + ≤2 fields, each ≤ 4096 B) ≈ ≤ 250 MB. Realistic: about 3 MB.
- Use `jq -n 'reduce inputs as $e (...)'` instead of `-s`. Memory then stays constant per record, and every record is still validated (probe below).
- QUALITY #7 compliance: capture once into a file (`mktemp` under one `0700` dir, removed by trap; see the existing EXIT-trap lesson at `:2135-2144`), then run jq over the file. Do not pipe the live producer into the parser.

## D5 — one malformed-shape record blinds a whole class

**Counterexample.** One record logged through `sd_journal_send` / `logger --journald` / `systemd-cat` with `MESSAGE_ID` given twice:
- journalctl's match `MESSAGE_ID=fe6f…` selects the entry if **any** value matches.
- `-o json` renders a repeated field as an **array** (journalctl(1) :440-443). Non-UTF-8 values become byte arrays (:445-447), and fields over 4096 B become null (:436-437).
- `all(.[]; … .MESSAGE_ID == $id)` (`:890`) is false, so the class becomes `record-invalid` for the rest of the boot.

Any uid-1000 process can do this, including a fleet test harness writing catalog ids into the real journal.

**Evidence that real emitters never produce these shapes.** Each emits exactly one string `MESSAGE_ID`:
- `src/core/cgroup.c:3040-3051` (`d989611b`) and `:3097-3101` (`fe6faa94`): `log_unit_struct(... LOG_MESSAGE_ID(...))` once each.
- `src/coredump/coredump-context.c:351`: `iovw_put_string_field(... "MESSAGE_ID=", SD_MESSAGE_COREDUMP_STR)`.

**Smallest correction.**
- Split the outcome per record:
  - non-object, parse failure or other boot → whole class unavailable (structural).
  - object whose `MESSAGE_ID` is not exactly the string `$id` → `rejected+=1`, not counted.
- Report `n=<valid> rejected=<K>`, plus INFO `JOURNAL_RECORD_REJECTED` when K > 0. This keeps QUALITY #5 (a rejection is kept, not dropped) without letting one record blind a class.

**Synthetic probe.** Filter:

```
reduce inputs as $e ({n,rejected,other_boot,total};
  nonobject→error; bad _BOOT_ID shape→error;
  _BOOT_ID≠$boot→other_boot; string MESSAGE_ID==$id→n; else rejected)
```

Identical rc and output for `/usr/bin/jq` jq-1.8.2 and `~/.local/bin/jq` jq-1.8.2:

| input | rc | output |
|---|---|---|
| empty | 0 | `n=0 … total=0` |
| two valid | 0 | `n=2` |
| truncated last line | 5 | none (`Unfinished string at EOF`) |
| truncated first line | 5 | none |
| `null` / `[]` / `"x"` / `1` line | 5 | none (`nonobject`) |
| `MESSAGE_ID` array, byte array or null | 0 | `n=0 rejected=1` |
| two objects on one line | 0 | `n=2` (object count, not line count) |
| other boot | 0 | `other_boot=1` |
| stderr hint merged | 5 | none |

**Probe of naive forms, which must not be used.**
- `jq -c 'select(.MESSAGE_ID==$id)' | wc -l` on a truncated last line: prints **1** match before failing with rc 5. A partial count leaks if rc is not checked.
- On a `null` line: rc **0**, skipped silently.
- On an array id: 0 matches, rc 0, so the record vanishes from the count.
- `jq -s 'map(select(...))|length'` on a `null` line: rc 0, silent.

## D6 — MESSAGE_ID is spoofable; the finding ids imply the emitter

**Evidence.**
- systemd.journal-fields(7) local man page :120-122: "Fields prefixed with an underscore are trusted fields … cannot be altered by client code." `MESSAGE_ID` (:37-43) is a user field.
- The code already labels counts `field=user:MESSAGE_ID unit=notice` (`:860-861`, `:1015`), which is honest. But the ids `KERNEL_OOM_NOTICE_JOURNAL_*` and `OOMD_NOTICE_JOURNAL_*` (`:931-938`) read as manager-emitted notices.

**Trusted-field pins** (request them in `--output-fields`; never request `_CMDLINE` or `MESSAGE`):

| class / scope | pin | strength | anchor |
|---|---|---|---|
| `fe6faa94`, `d989611b` / system | `_PID=="1" and _UID=="0"` | strong: a non-root user cannot be PID 1 or uid 0 | emitter is the manager: `src/core/cgroup.c:3040-3051,3097-3101` |
| `fe6faa94`, `d989611b` / user | `_UID==uid and _SYSTEMD_UNIT=="user@<uid>.service"` (+ `_SYSTEMD_USER_UNIT=="init.scope"` — [INFERENCE], confirm on one live record) | **weak**: the subtree is delegated to the same uid; observed account and unit-instance values withheld in round19 | same |
| `fc2e22bc` / both | `_SYSTEMD_SLICE=="system.slice" and (_SYSTEMD_UNIT\|startswith("systemd-coredump@"))` | strong: uid 1000 cannot join root-owned system.slice cgroups | `src/coredump/coredump-submit.c:675-683` drops to the **crashing user's uid** before `sd_journal_sendv` at `:793` ("credentials journald will see are the ones of the coredumping user"), so `_UID` cannot pin and the cgroup can |

Report `pinned=` and `unpinned=` separately, label the user-scope pin `pin=weak`, and keep `unpinned` visible (D5 style).

**Forgery through the real emitter: `d989611b` cannot be pinned by any field.** [INFERENCE, not executed — mutation is out of scope]
- The manager emits `d989611b` whenever the `user.oomd_ooms` xattr on the unit's cgroup has increased (`cgroup.c:3018-3031`). It reads this when the cgroup empties (`cgroup.c:2961-2962`).
- Delegation metadata was observed in the historical read; account identity, unit instance and observed attribute values are withheld in round19.
- So a uid-1000 process can raise `user.oomd_ooms` on a user unit it owns. The real user manager then writes a record that passes every pin. The same applies to PID1 and `user@1000.service` at logout.
- `systemd-oomd` is measured `inactive` on this host right now.

**Correction.** Print `oomd_state=<is-active>` next to the oomd class as a label. **Never** state that a `d989611b` record proves oomd ran. That fits the spec's "notice units, never fleet-caused kill counts".

## D7 — the segfault class is not a subset of coredump records by construction

**Counterexample.** `:966` matches only `COREDUMP_SIGNAL=11`, and the header claims "a RECORD subset of the coredump records" (`:870-871`). But `src/coredump/coredump-backtrace.c:33` replaces `MESSAGE_ID` with `SD_MESSAGE_BACKTRACE_STR` on backtrace records, and any client can also log `COREDUMP_SIGNAL=11` with no coredump id.

**Correction.**
- Query `MESSAGE_ID=fc2e22bc… COREDUMP_SIGNAL=11`. Different fields are ANDed by journalctl, so the subset holds by construction.
- Validate both fields in jq. `(.COREDUMP_SIGNAL|tostring)=="11"` turns an array into `"[\"11\",…]"`, which is fine as a rejection but should go to `rejected`, not `record-invalid` (D5).

## D8 — parser provenance

Measured with `type -a jq` in the tool shell: `jq is a shell builtin` (`jq --version` → `jaq 3.1.1`), then `/home/vgpnk/.local/bin/jq`, then `/usr/bin/jq` (`pacman -Qo` → `jq 1.8.2-1`). In `bash --noprofile --norc`: `command -v jq` → `/home/vgpnk/.local/bin/jq` (jq-1.8.2).

`JQ_BIN=${MORI_JQ_BIN:-jq}` (`:283`) therefore resolves to a user-writable binary that shadows the packaged one. All three agree on rc (5) for the probed failures; jaq's error text differs.

**Correction.**
- Put `parser=<resolved path> parser_version=<--version>` in the surface detail (QUALITY #2 provenance).
- The selftest asserts parser **behaviour** (rc and output on the D5 matrix), not the version string.

## D9 — the selftest stub ignores its arguments

The dispatcher has `out_of journal` / `rc_of journal` with no argument inspection (`:2164-2170`). Every one of the eight queries (and a canary, if added) receives identical bytes.
- A fixture containing one `fe6f` record makes the `d989`, `fc2e` and segfault queries see that record → `record-invalid`.
- Scope and class independence **cannot** be exercised.

**Correction.**
- Key the stub files by `<scope>.<match-token>` (for example `journal.user.fe6faa94`, `journal.system.canary`), each with its own `.rc` and `.err`.
- Append each argv to `journal.args`. Hermetic cases can then assert that every call contains `-q`, `-b`, `-o json`, and `--output-fields` without `MESSAGE`, and no `--all` or `-g`.

---

## Proposed checks (for L1 after integration; not run by this seat)

All are hermetic. Stubs are keyed per D9 and `MORI_BOOT_ID` is pinned.

1. **Empty vs denied.**
   - user canary returns `[]` at rc 0 → user classes `unavailable:scope-empty`, system classes unaffected.
   - system rc 1 → system classes `unavailable:rc-1`, user classes unaffected.
   - a valid empty class with a live canary → `0`, status ok.
2. **System uid.** Run with a uid shim, or with an `id` stub if the census reads uid via a `*_BIN`, set to 0 → user row `unavailable:system-uid`.
3. **Other boot.** One record with `_BOOT_ID≠MORI_BOOT_ID` → that class `unavailable:other-boot`; the other classes keep their values.
4. **Shape matrix (D5)**, per class. Arrays, byte arrays and null ids → `rejected=1`, count unchanged, status ok. The `null`, `[]`, `"x"` and `1` lines, and truncated first/last lines → `malformed-json`.
5. **stderr (D3).** Valid stdout plus a stub `.err` line at rc 0 → `unavailable:partial-files`, never `malformed-json`, and the stderr text is **absent** from the receipt.
6. **Saturation (D4).** Stub returns `MAX+1` records → `saturated`, no numeric value. A stub that sleeps past `JOURNAL_TIMEOUT_S` → `unavailable:timeout`.
7. **Spoof labels (D6).**
   - system `fe6f` record with `_PID=4242` → `unpinned=1 pinned=0`.
   - user `fc2e` record without `systemd-coredump@` / `system.slice` → `unpinned=1`.
8. **Subset (D7).** A `COREDUMP_SIGNAL=11` record without the `fc2e` id is not counted in `segfault_signal11`.
9. **Independence.** Only `journal.system.d989611b` is positive → only `system_oomd_notice_d989611b>0`; the other seven counters stay 0. Repeat for each of the 8 cells.
10. **No MESSAGE leak (regression).** A fixture record carrying a `MESSAGE` canary token anywhere in the stub output. The token must never appear in the census receipt or in stderr.

## Residuals (named, not covered)

- Partial EACCES on one file while others open is silent under `-q` (journal-util.c, EACCES `continue`). Group/ACL membership is a proxy, not a proof.
- Same-uid forgery of user-scope `fe6faa94` and `d989611b` (weak pin). Authentic-emitter forgery of `d989611b` via `user.oomd_ooms` (D6) [INFERENCE].
- Possible journald PID-reuse race between the sender's exit and journald's metadata lookup [INFERENCE; not verified against v261's pidfd usage].
- The `--user` scope is selected by file type, not by `_UID` (sd-journal.c:1524-1551). Under `SplitMode=none` the user scope is empty, which the canary catches but cannot repair.
- The PROVINCE.md:63-71 frontier recipes count records with `| wc -l`. That form prints 0 on a permission failure unless pipefail is set and rc is checked. It is outside this seat's ownership and is noted for FrontierConnection / L1.

## Sources opened (2026-10-20)

- systemd v261:
  - `src/shared/journal-util.c` (`journal_access_check_and_warn`, `access_check_var_log_journal`)
  - `src/journal/journalctl-util.c` (`acquire_journal`, `journal_acquire_boot`)
  - `src/journal/journalctl-show.c:525-619`
  - `src/libsystemd/sd-journal/sd-journal.c:1524-1554`
  - `src/core/cgroup.c:2945-2966,3006-3107`
  - `src/coredump/coredump-submit.c:578-595,675-683,793`
  - `src/coredump/coredump-context.c:351`
  - `src/coredump/coredump-backtrace.c:33`
  - `src/systemd/sd-messages.h:41-42,195-199`
- Local man pages (systemd 261.2): journalctl(1) :87-96, :431-447, :496-502, :570-574, :834-835; systemd.journal-fields(7) :37-43, :120-151; journald.conf(5) :160-168.
- Host metadata: read-only access, delegation, activity and configuration checks were disclosed historically; account/group membership and observed configuration values are withheld in round19. No host query was repeated.
