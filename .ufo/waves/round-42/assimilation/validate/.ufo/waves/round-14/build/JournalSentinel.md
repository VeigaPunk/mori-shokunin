# JournalSentinel — security review of structured unit metadata handling (round 14)

Seat: `MoriR14.JournalSentinel` (sentinel, leaf). Axis: coverage. Milestone: restore the OOM alarm and structured fleet routing.

Surface reviewed (read only):
- `tools/mori-census.sh` working tree, sha256 `39abda0a…3fc985`. This equals r13 delivered H and `.ufo/waves/round-14/frozen/mori-census.sh` (`cmp` returned no difference).
- `git status` shows only `.ufo/waves/round-14/` untracked. So **no round-14 repair had landed** when I reviewed.
- Pre-r13 B `6531ac6:tools/mori-census.sh:847-912` (historical predicate).
- `corpus/lessons/round-13-verifier-spotcheck.md`.

I ran no checks, tests, census or selftest. Host fact queries were read-only: `jq --version`, `command -v`, `sha256sum`, `man journalctl`, `systemctl --user list-units`.

Tools installed or updated: **none**.

Early contract sent to `MoriR14.CensusRepair` (points 1–5 below map to J1, J2, J3/J4, J5, J10).

## Summary

| ID | Sev | Status | One line |
|---|---|---|---|
| J1 | HIGH (L1-accepted residual) | present now; applies to the restored crit | One forged malformed record makes a whole class `unavailable`. The row and the `unavailable=` count report it explicitly (it is not a silent zero), but ROLL stays CLEAN, so a real OOM/SIGKILL alarm in that scope does not fire. |
| J2 | HIGH | prospective (repair) | Echoing UNIT/USER_UNIT/UNIT_RESULT bytes allows token and newline injection: forged FINDING/SURFACE/verdict lines. |
| J3 | MED | prospective | Subject field shape: null (>4096 B), arrays (duplicate or non-UTF8), missing, or two conflicting subject fields. A jq type error grades the whole class unavailable (same effect as J1). |
| J4 | MED | prospective | Emitter `_SYSTEMD_UNIT`/`_SYSTEMD_USER_UNIT` is not the failed unit and is not a spoof-proof anchor in user scope. |
| J5 | MED | prospective, plus pre-existing glob | Fleet predicate built from env/roster puts injected text into the jq program. `$ROSTER_LANES` is expanded unquoted with globbing on. |
| J6 | MED | present | A timeout or journal flood makes an alarm class `unavailable`. It is visible on the row, but the exit is CLEAN. |
| J7 | LOW-MED (L1-retained residual) | present | Mutable env bytes (`MORI_JOURNALCTL_BIN`, `MORI_JQ_BIN`) are echoed raw into rows. `MORI_JOURNAL_TIMEOUT_S=0` removes the bound. |
| J8 | LOW | present (host) | The live `jq` resolves to user-writable `~/.local/bin/jq`, which shadows root-owned `/usr/bin/jq`. |
| J9 | LOW | present | jq output parse folds extra columns into the last variable. Adding columns needs an exact column count. |
| J10 | INFO | prospective | Token grammar: `unit=` already means notice\|record. New counters must join `DRIFT_COUNTER_KEYS`. |
| J11 | LOW | present | `CAP_OUT` (raw journal bytes) remains a global after parsing. |
| J12 | INFO | accepted residual | Positive spoofing (forged fe6faa94 / `UNIT_RESULT=oom-kill`) forces crit DRIFT. It fails loud, so it is a disclosure item, not a blocker. |

Retained and correct; do not regress:
- **stderr is never stored or echoed.** The `wc -c` coproc counts bytes only (`:946-984`). A nonzero count grades `stderr-nonempty`, checked only after rc (`:972-984`).
- **jq stderr goes to `/dev/null`** (`:987`).
- **No MESSAGE is requested**: `--output-fields` is fixed at every call site (`:1068-1072`).
- **The boot id is the only journal string echoed**, and it is validated as 32 lowercase hex (`:1004-1010`).
- **`set +o xtrace`** (`:253`).
- **No pager** (`--no-pager`). **The scan is bounded** by `timeout -k 1` (`:961`).

The repair must not route the new queries through `cap()` (`:535-540`). `cap()` merges stderr into stdout (`2>&1`), which would feed diagnostics into JSON parsing and lose the byte-count discipline.

---

## J1 — HIGH, L1-accepted residual: one malformed record makes an alarm class unavailable (reported, exit CLEAN)

**Exploit path**
1. Any process of the user writes one entry for the current boot with `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef` plus a second `MESSAGE_ID=<anything>`, using `sd_journal_send` or a native datagram.
   - Both values are client-supplied, non-underscore fields (S015; `.ufo/waves/round-13/build/FieldsSource.md:16-20,113-117`).
   - journalctl's `MESSAGE_ID=fe6f…` match selects the entry because one value matches.
   - `-o json` then serializes the field as an array. Source: `journalctl(1)`, systemd 261, `man` lines 442-446: "if a non-unique field is encountered a JSON array…"; non-UTF8 values become byte arrays.
2. `JOURNAL_JQ_MSGID` (`:927`) requires `all(.[]; … (.MESSAGE_ID == $id))`. The array fails, so the tail emits `record-invalid` (`:926`). `journal_query` returns `JQ_STATUS=record-invalid` (`:992`).
3. `probe_journal` skips non-ok classes before emitting findings (`:1091`).
4. `emit_surface … unavailable` only increments `N_UNAVAIL` (`:411-413`). ROLL changes only on warn/crit (`:399-404`), and the exit follows ROLL (`:1968-1971`).

**Result:** the genuine fe6faa94 notices in that scope are not counted and no alarm fires. The class is **explicitly reported** as `kernel_oom_notice=unavailable:record-invalid` on the `journal.<scope>` row and in the verdict's `unavailable=` count, so this is not a silent zero. The exit is still CLEAN (rc 0).

The same trick works on the other classes:
- `unit_sigkill_record`: a duplicated `EXIT_STATUS`/`EXIT_CODE` silences the only current warn (`KILL_SIGNAL_JOURNAL`, `:928`, `:1095`).
- Restored `UNIT_RESULT=oom-kill` and fleet `UNIT_FAILURE_JOURNAL`, if they are validated whole-class the same way.

**Impact:**
- r14 restores `OOM_KILL_JOURNAL` crit (spotcheck routed defect 1). Under the r13 validation shape, that alarm is suppressible by one forged line.
- The historical text probe could not be suppressed by adding a line. It counted matches (`B:874`, `B:893-895`).
- So the restoration would look green in fixtures but stay weaker than the pre-r13 behaviour. That is a hidden no-harm failure on coverage.

**Smallest remediation (fail-closed, no new spoof surface):**
- Split validation into a **per-record partition** for alarm classes.
- jq emits integer columns `matched valid invalid boots`:
  - `matched` = records journalctl returned, after the boot check.
  - `invalid` = records whose selector or subject fields are not scalar or are not the expected value.
- `OOM_KILL_JOURNAL` crit fires when `matched > 0`, with `valid=… invalid=…` disclosed.
- Whole-class `unavailable` is kept only for producer failures: rc, timeout, stderr, unparseable JSON, a non-object record, or missing, foreign or multiple `_BOOT_ID`.
- `_BOOT_ID` is journald-trusted (underscore). Forging the selector alone cannot reach those whole-class arms. Only a hostile stub or binary can (see J8).
- Counting malformed matches toward the alarm adds no attack power. A well-formed forgery can already raise crit (J12).

**Acceptance cases under the partition design** (deferred; not round-14 expectations, see the L1 ruling below):
- user scope: one valid fe6faa94 record plus one record with `"MESSAGE_ID":["fe6f…","x"]` → `OOM_KILL_JOURNAL` crit, DRIFT rc1, `invalid=1`.
- the same pattern for `UNIT_RESULT` as an array.
- the same pattern for `EXIT_STATUS` as an array → `KILL_SIGNAL_JOURNAL` warn still present.

**L1 ruling (MoriR14, round 14):** no change to malformed-class acceptance is planned. Strict whole-class validation is kept to preserve the guarantee that every count comes from fully validated records. Array-class fail-closed unavailability and the unvalidated env knobs (J7) are **retained, known residuals**. The repaired census makes no universal alarm-proof claim. This seat records the ruling and does not contest it. What remains:
- The suppression path above stands as a disclosed residual: an unavailable row, exit CLEAN.
- The partition design above is an option for a later round, not a round-14 requirement.
- The `R14_SEC_DUP_*` rows below should therefore expect `<class>=unavailable:record-invalid` on the row and `unavailable≥1` in the verdict, not crit or DRIFT. They pin the residual's disclosure so a future change cannot turn it into a silent `0`.

---

## J2 — HIGH (prospective): unit bytes reaching output give line/token injection

**Exploit path**
- `UNIT`/`USER_UNIT`/`UNIT_RESULT` are client-supplied (S015).
- In the user journal any same-user process can set `USER_UNIT=` to anything, including `\n`, spaces, `=`, `;` and `)`.
- The value travels as a JSON string. `jq -r` decodes `\n` into a raw newline, and bash keeps it.
- `emit_finding` concatenates `obs` verbatim (`:398`). `emit_surface` does the same with `detail` (`:410`). Both are printed with `printf '%s\n'` (`:1962-1963`).

**Impact:** a value such as `x.service\nMORI_CENSUS: CLEAN (findings=0 …)` or `\nFINDING …` forges whole output lines. Any of the following can be forged that way:
- the verdict (the F02 oracle work exists because verdict-line integrity matters)
- a finding id or severity token
- a `count=` token (`drift_scan` concatenates duplicate keys)
- the drift pairing id (`drift_line_id`, `:2045-2054`)

Even without a newline, spaces and `=` inject tokens such as `severity=info count=0`, and `)` closes a SURFACE detail early.

**Smallest remediation:**
- **Never emit subject bytes.** Classify inside jq and emit only integer columns, e.g. `fleet nonfleet unknown invalid` per class.
- Validate each column with `is_int` (`:1470`).
- Owner text (`owner=tsukuroi`) and class labels must be shell literals, never journal-derived.
- Do not rely on `@tsv` escaping as the defense. `@tsv` escapes control characters but not spaces or `=`, and escaping behaviour differs across jq implementations (J8).

**Acceptance case:** a fixture with `"USER_UNIT":"a.service\nMORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=0 surfaces=0)"` and the same with `"a b=c.service"`. Assert:
- exactly one `^MORI_CENSUS:` line;
- the canary substring is absent from stdout and stderr;
- the record is counted as `unknown` (fails the charset check in J3), not as nonfleet.

---

## J3 — MED (prospective): subject shape and jq type errors

**Evidence:** `journalctl(1)` `man` lines 436-446 (systemd 261):
1. Fields larger than 4096 bytes are encoded as `null`.
2. Non-unique fields are encoded as arrays.
3. Non-printable or non-UTF8 values are encoded as byte arrays.

**Failure modes:**
- In jq, `startswith`, `test`, `split` and `ascii_downcase` on `null`, an array or a number raise errors. jq then exits nonzero, giving `malformed-json` at `:990`, and the whole class goes `unavailable`. That is the J1 effect again, triggerable with an oversized or duplicated `USER_UNIT`.
- Treating "not a fleet match" as nonfleet would also route forged or garbled subjects to `UNIT_FAILURE_OUT_OF_SCOPE owner=tsukuroi`. That is a false ownership claim, and spotcheck defect 2 forbids it ("unknown … not falsely nonfleet").

**Smallest remediation:**
1. Subject field selection: **accept either valid subject field, independent of journal scope** (L1 ruling). `--system`-readable stores may contain user-manager `USER_UNIT` entries, so a fixed scope→field mapping would misclassify them; this supersedes my earlier scope-bound rule.
   - Exactly one of `UNIT`/`USER_UNIT` is a valid string → that is the subject.
   - Both `UNIT` and `USER_UNIT` present → `unknown`, **even when the two values are identical** (L1 final ruling). The pinned `unit_log_field` selects exactly one field per manager, so the source documents no record that carries both. The raw record total is still kept, so these records are not dropped from the class count.
   - Neither is a valid string → `unknown`.
   - `EmitterSource` owns the unit.c field-name anchor; I did not re-open the source in this seat.
2. Guard with `(.F | type) == "string"` **before** any string operation. L1 has explicitly instructed CensusRepair to add these type guards.
3. Require the unit-name charset `^[A-Za-z0-9:_.\\@-]{1,255}$`, compared as a string. Anything else is `unknown`.
4. Put `USER_UNIT,UNIT,UNIT_RESULT` in `--output-fields`, plus the existing `_BOOT_ID,MESSAGE_ID`. Never add `MESSAGE`.
5. Partition into three counts (`fleet`, `nonfleet`, `unknown`) plus `invalid`, and never sum across scopes.

---

## J4 — MED (prospective): emitter fields are neither the subject nor a trust anchor

**Why the emitter is the wrong subject:**
- Unit-failure (`d9b373ed…`) and process-exit (`98e32220…`) records are written by the **manager** (PID 1, or the `user@UID.service` manager).
- Their `_SYSTEMD_UNIT` and `_SYSTEMD_USER_UNIT` describe that emitter: `init.scope`, `user@1000.service`, etc. [INFERENCE from S015 trusted-field semantics; `JournalFields`/`EmitterSource` own the exact quotes].
- Routing on them would send every failure to the same bucket.

**Why it is not a trust anchor in user scope:**
- The user manager runs with cgroup delegation, so a same-user process may be able to move into the manager's own scope and inherit `_SYSTEMD_USER_UNIT=init.scope` [INFERENCE; unmeasured].
- Do not describe `_SYSTEMD_USER_UNIT` narrowing as anti-spoof.
- System-scope `_PID=1` narrowing is a sounder hardening step [INFERENCE].

**Remediation:** subject = `UNIT`/`USER_UNIT` only. Disclose `trust=client-supplied` on routed findings. Claim no emitter authentication.

---

## J5 — MED: fleet predicate injection; roster glob expansion (pre-existing)

**Historical predicate** (`B:891`): case-insensitive substring `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` over the failure line.
- A structured mirror must keep it a **fixed literal**. If it is built from `MORI_ROSTER_LANES`, `shokunin.conf` or any env and spliced into the jq program text, a value such as `") or true or ("`, a regex metachar or `.` rewrites the classifier.
- Effects: everything becomes fleet (warn flood) or nothing does (silencing fleet failures into tsukuroi info).
- Pass any variable data with `--arg`, compare as literal strings, and never build a regex from data.
- Raw substring matching also accepts look-alike names (`notfleet.service`, `fleetwood.service`). A forged `USER_UNIT` can pick either bucket. That is the `RoutingAttack` seat's semantic concern; the security requirement is only that the predicate is constant and literal.
- Live: `systemctl --user list-units --all` and `list-unit-files` returned no unit matching any of the five fragments on this host, so transient `tmux-spawn-*.scope` units are the only plausible live matches [INFERENCE]. Those are any tmux session, fleet or not.

**Pre-existing glob expansion:**
- `for id in $ROSTER_LANES` (`:432`) and `for lane in $ROSTER_LANES` (`:1780`) are unquoted with no `set -f`.
- A roster token `*` expands against the cwd.
- The r12 LOW item "MORI_ROSTER_LANES tokens not shape-validated" is still open.
- This matters to journal routing only if the repair reuses the roster. **Do not.**

---

## J6 — MED: unbounded journal flooding produces a silent CLEAN for an alarm class

**Exploit path:**
1. A same-user process floods the user journal for the current boot with records matching the class selector.
2. The field-filtered scan exceeds `JOURNAL_TIMEOUT_S` (default 2 s, `:310`; labelled a placeholder, not measured).
3. `timeout` kills it with rc 124/137 → `timeout` status (`:975`).
4. The class goes `unavailable` and the run exits CLEAN.

`jq -s` also slurps all matched records into memory.

This is a fail-open availability path for the restored crit. The historical probe was also unavailable on rc > 1 (`B:869-871`), but r14 multiplies the queries: 6 or more per scope, plus the new result and subject queries.

**Smallest remediation:**
- When an **alarm** class is unavailable for `timeout`, `malformed-json` or `stderr-nonempty`, emit a named finding (e.g. `JOURNAL_ALARM_UNAVAILABLE class=kernel_oom_notice scope=user status=timeout`). Then the gap is visible beyond a surface token.
- Severity is L1's call: `info` keeps CLEAN on hosts where the system scope is unreadable (rc-1). `warn` restricted to `timeout|malformed-json|stderr-nonempty` would be fail-closed.
- Keep `rc-*`/EACCES as `unavailable` without DRIFT so unreadable system scopes stay CLEAN.

---

## J7 — LOW-MED: mutable env echoed raw; timeout bound defeatable

**Raw echo:**
- `cmd=$JOURNALCTL_BIN …` (`:1032`, `:1044`, `:1112`) and `parser=missing bin=$JQ_BIN` (`:1050`) print env bytes verbatim.
- A value containing `\n` forges whole lines (mechanism as in J2).
- The exposure is same-user env. It is real when the census inherits a lane's environment, i.e. when an agent or harness invokes it.

**Timeout bound:**
- `MORI_JOURNAL_TIMEOUT_S` is unvalidated (`:310`, used at `:961`). `timeout 0` disables the bound, giving an unbounded journal scan; a non-numeric value gives rc 125 and the class unavailable.
- Repair queries must not add new env knobs that are echoed or spliced, e.g. no `MORI_FLEET_PATTERN`.

**Smallest remediation:**
- Shape-gate the bins. Reject anything outside `[A-Za-z0-9/._+-]`, as `unavailable reason=bin-shape-refused`, before echoing.
- Require `is_int` and `≥1` for `JOURNAL_TIMEOUT_S`, falling back to 2.

---

## J8 — LOW: parser resolves through a user-writable PATH entry

Observed on this host (non-interactive bash, `env -i PATH="$PATH"`):

| bin | resolves to | owner | notes |
|---|---|---|---|
| `jq` | `/home/vgpnk/.local/bin/jq` | `vgpnk` | 2 267 912 B, sha256 `b1c22172dd30…5870f`, ahead of `/usr/bin/jq` (`root`, 30 800 B, sha256 `e815667571d0…f7806`); both report `jq-1.8.2` |
| `journalctl` | `/usr/bin/journalctl` | — | — |
| `timeout` | `/usr/bin/timeout` | — | — |

**Risk:** the live census executes whatever is at `~/.local/bin/jq`. Any same-user process can replace it and return `0\t0\tnone` for every class, silencing all journal alarms with no trace. Lane agents can do this, and the tooling directive explicitly sanctions installing into `~/.local/bin`. This is an integrity issue, not a privilege escalation.

**Evidence caveat:** this harness's interactive shell resolves `jq` to a **builtin** (`jaq 3.1.1`). An L1 evidence command run inside the harness (e.g. the spotcheck's `jq -Rs scan(...)`) may therefore be executed by jaq, not by the jq the census uses. Receipts should name the parser binary.

**Smallest remediation:** disclose the resolved parser path in the surface row (shape-gated). Optionally L1 pins `MORI_JQ_BIN=/usr/bin/jq` in the registered gate invocation. No code default change is required this round.

---

## J9 — LOW: parse shape when columns are added

- `IFS=$'\t' read -r n nb boot <<< "$parsed"` (`:996`) reads the first line only, and extra columns are absorbed into `boot`.
- Today `boot` is then rejected by the hex/32 check (`:1007-1010`), which fails safe.
- With added integer columns (`fleet nonfleet unknown invalid`), the last variable would absorb the tail silently.

**Remediation:**
- Read into an array.
- Require an exact column count and a single output line.
- Apply `is_int` to every numeric column.
- Keep the jq sentinels (`record-invalid` etc.) as literal outputs only.

## J10 — INFO: token grammar and drift masks

- `unit=` already means `notice|record` (`:1100-1104`, `:1126`). A routed finding must not add `unit=<subject>` or `unit=fleet`. Use, for example, `subject=user:USER_UNIT subject_class=fleet` with literal values, and `owner=tsukuroi`.
- New integer keys (`fleet`, `nonfleet`, `unknown`, `invalid`, `oom_kill_result`, …) must be added to `DRIFT_COUNTER_KEYS` (`:1995-2006`). Otherwise `--drift` reports value changes as semantic drift.
- Do **not** add any key that could carry non-integer journal bytes. The `boot=` mask `[^ ;)]*` (`:2023`) shows how a free-text value would be partially masked.

## J11 — LOW: raw journal bytes outlive the parse

- `CAP_OUT` is global. After `journal_query` it still holds the raw JSON, including any MESSAGE a hostile stub returns, until the next `cap` caller overwrites it.
- Nothing echoes it today. The `xtrace` guard (`:250-253`) is the only defense.
- **Remediation:** clear `CAP_OUT=''` (and `raw`) right after the jq call in `journal_query`.

## J12 — INFO: positive spoofing (accepted residual, disclose)

A forged well-formed `fe6faa94…`, `d9b373ed… UNIT_RESULT=oom-kill` or fleet-looking `USER_UNIT` record in the user scope raises crit or warn. This fails loud, and the pre-r13 text probe had the same exposure (`ClaimAttack.md` A7). The repaired findings should carry `trust=client-supplied attribution=none`. They must not claim unique victims or fleet cause.

---

## Acceptance additions for L1 / JournalRegression (no execution here)

| Case id (proposed) | Fixture (synthetic, current boot) | Expect |
|---|---|---|
| `R14_SEC_DUP_MSGID_OOM` | user: 1 valid fe6faa94 + 1 with `MESSAGE_ID` array | per the L1 ruling: `kernel_oom_notice=unavailable:record-invalid` on `journal.user`; `unavailable≥1` in the verdict; never `kernel_oom_notice=0` |
| `R14_SEC_DUP_RESULT` | system: `d9b373ed…` with `UNIT_RESULT:["oom-kill","x"]` | the class is reported `unavailable:record-invalid` (or `unknown`), never a fabricated `0` or nonfleet |
| `R14_SEC_SUBJECT_NEWLINE` | `USER_UNIT` containing `\nMORI_CENSUS: CLEAN (…)` | one verdict line; canary absent; `unknown=1` |
| `R14_SEC_SUBJECT_TOKENS` | `USER_UNIT":"a b=c.service"` | no `b=c` token in output; `unknown=1` |
| `R14_SEC_SUBJECT_NULL_ARRAY` | `USER_UNIT:null`; `USER_UNIT:[1,2]`; `UNIT` and `USER_UNIT` both present (conflicting **and** identical) | each goes to the per-record `unknown` bucket; the class stays ok and the raw total includes the record; never `UNIT_FAILURE_OUT_OF_SCOPE`; a valid single `USER_UNIT` in a system-scope record is classified, not `unknown` |
| `R14_SEC_EMITTER_IGNORED` | `_SYSTEMD_USER_UNIT` fleet-looking, `USER_UNIT` non-fleet | routes nonfleet; and the reverse case routes fleet |
| `R14_SEC_BIN_NEWLINE` | `MORI_JQ_BIN=$'/x\nMORI_CENSUS: CLEAN'` | one verdict line; `bin-shape-refused` |
| `R14_SEC_TIMEOUT_ZERO` | `MORI_JOURNAL_TIMEOUT_S=0` | bound falls back; no unbounded call |
| `R14_SEC_MESSAGE_CANARY` | every record also carries `"MESSAGE":"<canary>"` | canary absent from stdout and stderr (retain r13 check) |

`resume_continuity_v1` zero-mutation rejection: not applicable to this surface. The census is read-only in live mode, and no resume path was in scope.

## Limits

- The review is of r13 production bytes plus the stated r14 contract. CensusRepair's eventual diff was not available, so every "prospective" item is a requirement, not an observed defect.
- J1's array serialization is from `journalctl(1)` (systemd 261 man page). I did not exercise it against a live forged entry.
- The J4 delegation spoof is [INFERENCE].
- J6 flood cost is unmeasured.

## Disposition reported by `MoriR14.CensusRepair` (claimed by the executor; this seat has not verified it against the bytes)

| Item | Disposition |
|---|---|
| J2 | Adopted. Raw `UNIT`/`USER_UNIT`/`UNIT_RESULT` are never echoed, only integer aggregates. A newline-injection canary test on `UNIT` asserts no forged FINDING line. |
| J3 | Adopted per L1. Subject = the single `UNIT`/`USER_UNIT` present, independent of scope; both present → `unknown`. A malformed, array or missing subject or result goes to a per-record `unknown` bucket and the raw class count is kept, never counted as nonfleet. Type guards are instructed by L1. |
| J5 | Adopted. The fleet token set is fixed literal text passed via `--arg`, with no env or roster interpolation. |
| J9 | Adopted. Exact TSV column count, and `is_int` on every column. |
| J10 | Adopted. New integer keys added to `DRIFT_COUNTER_KEYS`; `unit=notice\|record` kept, with no `unit=<name>` token. |
| J11 | Partly. `CAP_OUT` is never printed. Clearing it after the parse is not confirmed; the residual stays LOW. |
| J1 | Not adopted (L1). Duplicated `MESSAGE_ID` or other selector arrays still grade the class `record-invalid` → unavailable. That is disclosed on the row, not a silent `0`, and the other scope still alarms independently. |
| J7 | Not adopted (L1-retained residual). |
| J4, J6, J8 | Not addressed in the CensusRepair message. |

"Accepted residual" here means documented, not a security guarantee. Neither this report nor the census makes any broad claim that alarms cannot be spoofed or suppressed. L1 should check the dispositions above against the landed `tools/mori-census.sh` diff in its single verification run, using the `R14_SEC_*` cases.
