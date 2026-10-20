# SecurityPrivacy — round 15 C1 (validated positives), read-only sentinel

Scope: no MESSAGE, unit strings, host credentials or database bytes may leak into the new positive output or the fixture captures. Read: `tools/mori-census.sh` (tag DC7D, `:296-329`, `:399-416`, `:960-1389`), `tools/mori-round14-regressions.py` (`:314-317`, `:403-507`, `:637-682`, `:1659-1683`, `:2019-2074`), and all 11 packs under `.ufo/waves/round-15/fixtures/`. Not opened: auth/credential files, agent.db, or the host journal. No census, gate or harness was run. No edits outside this report. No tools were installed or updated, because none were needed (host-safety amendment acknowledged). The only things executed were local `jq` runs on synthetic literals, to ground jq's semantics (shown below).

State at read time: no `positive_*` token exists in `tools/` (grep returned no hits), and `tools/mori-round15-regressions.py` does not exist yet. The findings below are acceptance constraints on the code about to land, plus audits of the code already in the tree.

## Findings

### P1 HIGH (privacy): jq stderr carries record values. "Avoid arbitrary stderr suppression" must not reach the jq pass
- **Evidence:** the census runs jq as `parsed=$("$JQ_BIN" -s -r "$@" "$filter" <<< "$raw" 2>/dev/null)` (`mori-census.sh:1099`). jq 1.8.2 prints the offending value on a type error. On synthetic input:
  - `jq: error (at <stdin>:1): string ("CANARYSECRETTEXT") and number (1) cannot be added`
  - `Cannot index string with string ("MESSAGE_ID")`
- **Why it matters:** the CensusPositive prompt says "avoid … arbitrary stderr suppression". The new positive selectors are meant to run over exactly the mixed/malformed streams that trigger type errors. The unit query also holds UNIT/USER_UNIT/UNIT_RESULT values (`:1201`).
- **Exploit path:** the `2>/dev/null` is dropped, or the positive pass gets its own jq call without it. A record with a non-string field then hits a type mismatch. Its value (a unit name, or MESSAGE if a stub ignores `--output-fields`) reaches census stderr. The r14 harness keeps stderr on disk (`r14:2052-2058`) and redacts only its own canaries (`r14:314-317`). Live callers see the stderr directly.
- **Remediation (smallest):** keep `2>/dev/null` on every jq call that reads journal bytes. Alternatively, reuse the existing `wc -c` coproc pattern (`:1057-1082`) and expose only `parser_stderr=present`. A jq failure is `unavailable:malformed-json`.

### P2 HIGH (fabrication): stale positive state across classes and scopes
- **Evidence:** `journal_query` clears its outputs once at the top: `JQ_N=''; JQ_BOOTS=''; JQ_BOOT=''; JQ_STATUS=''; JQ_VEC=''` (`:1051`). It then returns early at `:1055` (no-timeout-bin), `:1089` (rc/timeout), `:1094` (stderr) and `:1102` (malformed). `probe_journal` copies the results into per-key arrays right after each query (`:1221`).
- **Exploit path:** a new `JQ_POS*` global that is not cleared at `:1051` keeps the value from the previous query. Example: the user unit query finds `positive_unit_oom=1`, then the system unit query times out. The system row would then report `positive_unit_oom=1` and fire OOM crit from evidence that never existed. The contract requires positives to be unavailable on capture failure.
- **Remediation:** clear every positive output at `:1051`. Set positives only after jq returns rc 0. On any early return, store `unavailable:<JQ_STATUS>` per key.

### P3 MEDIUM (output injection): never echo record-derived strings from an invalid stream
- **Evidence:** the only journal-derived string the census echoes is the boot id. It is checked against 32 lowercase hex characters only on the ok path (`:1128-1134`). `sboot` is set only when the status is ok (`:1228`). `BOOT_ID_EXPECTED` is validated separately as 32 hex characters (`:321-329`).
- **Exploit path:** the positive path is the first one that emits output when the raw class is `record-invalid`/`multi-boot`. Suppose it took a boot or label column from the filter output, e.g. `[.[]._BOOT_ID][0]`. Then a neighbouring record such as `_BOOT_ID:"x alarm=0 paths= MORI_CENSUS: CLEAN"` could add tokens to a finding. `@tsv` escapes tabs and newlines but leaves spaces, so the injected tokens survive.
- **Remediation:**
  - Positive columns are integers only, each checked with `is_int`, with a fixed column count.
  - Positive lines print `boot=$BOOT_ID_EXPECTED`.
  - No UNIT, USER_UNIT, UNIT_RESULT or EXIT_* value is ever printed.
  - The unit owner partition stays aggregate-only, as the contract says (`:1264-1291` unchanged).

### P4 MEDIUM (silenced alarm, coverage): a non-object neighbour can fail the whole pass
- **Evidence:**
  - `printf '[1]\n{"MESSAGE_ID":"x"}' | jq -s '[.[]|select(type=="object" and .MESSAGE_ID=="x")]|length'` gives `1`. jq's `and` short-circuits, so the guard works.
  - Without the guard, `"str"|.MESSAGE_ID` is a jq error. jq exits nonzero, the status becomes `malformed-json`, and all positives go unavailable.
  - The existing aggregate filters already guard this way (`:974-976`, `:1019`).
  - In all 11 packs, every record is a JSON object. A query for non-object records returned nothing. Non-object `MESSAGE_ID` values do exist (`{"id":…}`, arrays).
- **Impact:** one valid-JSON line that is not an object (a string, number or array) would silence a valid OOM/KILL alarm. That is exactly the C1 failure mode.
- **Remediation:** every positive selector starts with `type=="object" and`, before any field access. Add one pack or harness case: a valid kernel OOM record next to a JSON string line gives `want_oom=true` and `positive_kernel_oom=1`. Sent to HarnessBuild.

### P5 LOW (predicate width): keep the exact-string `tostring` form, never `tonumber`
- **Evidence:** jq 1.8.2 results for `(.EXIT_STATUS|tostring)=="9"`:

  | `EXIT_STATUS` | Result |
  |---|---|
  | `9` | true |
  | `"9"` | true |
  | `9.0` | false |
  | `["9"]` | false |
  | `[9]` | false |
  | `"09"` | false |
  | `true` | false |

- **Remediation:** an explicit scalar type guard is harmless. Do not use `tonumber`: it would also accept `"09"` and `"9.0"`, which widens the predicate.

### P6 LOW (trust labelling): the forgery surface is not widened, but the label must travel
- `MESSAGE_ID`, `EXIT_CODE`, `EXIT_STATUS` and `UNIT_RESULT` are set by the client. `_BOOT_ID` is a trusted journald field.
- A same-user process could already forge a single valid record before C1, and one record was already enough to alarm. So C1 does not amplify forgery.
- jq keeps the last value of a duplicate key (`{"MESSAGE_ID":"a","MESSAGE_ID":"b"}` → `"b"`). Real journalctl emits arrays for repeated fields, never duplicate keys, so this only matters for a hostile stub.
- **Remediation:** the contract says "no authenticated ids", so positive tokens should carry `trust=client-supplied`. The surface row already has it (`:1384`); the `KILL_SIGNAL_JOURNAL` line (`:1353`) does not. Add it there when the positives are added.

### P7 LOW (harness isolation, privacy): the r15 harness must not inherit the host journal
- **Evidence:**
  - The census falls back to `JOURNALCTL_BIN=${MORI_JOURNALCTL_BIN:-journalctl}` (`:296`).
  - r14 `census_env` does not inherit host env. It pins `MORI_JOURNALCTL_BIN` to the stub and sets a synthetic `MORI_BOOT_ID` and `PATH=<base>/bin:/usr/bin:/bin` (`r14:637-682`).
  - Saved stdout is redacted only for canaries (`r14:2052`).
- **Exploit path:** an r15 `--selftest` wrapper or red/green run that skips `census_env` would call `/usr/bin/journalctl` against the real host journal. Host boot id and record counts would then be persisted in evidence.
- **Remediation:** run every r15 subprocess with `census_env`, plus `MORI_BOOT_ID=11111111111111111111111111111111` for the packs. Sent to HarnessBuild.

### P8 INFO (provenance capture): paths only, no content
- `capture_revision` stores `git status --porcelain --untracked-files=all`, paths only. `--ignored` is not used (`r14:377-380`, `:403-431`).
- Names of untracked files inside the lane do enter the evidence, but their contents do not. That is acceptable.
- Not checked: the git configuration (hooks/fsmonitor) in effect when the harness runs git.
- Scope of this verdict: privacy only. It says nothing about whether porcelain detects moving inputs. Content changes to an already-dirty file leave its porcelain line unchanged (AttackProvenance CE1, `.ufo/waves/round-15/build/AttackProvenance.md`). Detecting that needs content hashes at load and at end. The paths-only privacy property still holds with hashes, because a digest does not reveal content.

### P9 INFO (parser provenance)
- The live census uses `jq` from PATH (`:297`). On the host PATH, `~/.local/bin/jq` (a user-writable `jq-1.8.2` binary) comes before pacman's `/usr/bin/jq` (`jq 1.8.2-1`).
- The r14 harness PATH does not include `~/.local/bin`, so harness runs resolve `/usr/bin/jq`.
- Same-user write access, so no privilege boundary. Reported only for traceability.

## Fixture capture audit (11 packs): clean
Packs: BootArray, CleanControls, FanoutPositive, ForeignBoot, KernelSystem, KernelUser, NegativeInvalid, NegativeStatus, ProcessUser, SignalUser, UnitUser.
- **Record keys** are limited to `MESSAGE_ID, _BOOT_ID, EXIT_CODE, EXIT_STATUS, UNIT_RESULT, USER_UNIT, _TRANSPORT, __CURSOR, __MONOTONIC_TIMESTAMP, __REALTIME_TIMESTAMP`.
- **Absent:** a `MESSAGE` key, `/home` paths, usernames, canaries, secrets and tokens. The grep's only hit was `__MONOTONIC_TIMESTAMP:"1000"`.
- **Boot values:** only the synthetic `1111…`, `2222…`, arrays of those, `null`, and `[]`. None is the host boot id.
- **Synthetic metadata:** cursors are `s=r15-…`, realtime timestamps are `1700000000000xxx`, and `_TRANSPORT` is `journal`.
- **Unit names** are fleet-style and synthetic: `kagi-shokunin.service`, `shokunin-fixture.service`, `shokunin-worker.service`.
- **Case ids:** no duplicates across the packs.

## Checks for L1 after integration
- `grep -nE '2>/dev/null' tools/mori-census.sh` still covers every jq call that reads journal bytes (P1).
- `journal_query` clears every positive output at its top (P2).
- No new emitted token comes from a record string (P3).
- Run the r15 gate plus r14 leak mode (`R14_MESSAGE_CANARY`, `R14_SEC_UNIT_CANARY`) on the integrated census.
- Run the proposed case with a non-object neighbour (P4).

## Post-landing read (`mori-census.sh` tag 3F9A, read-only)
- **P1 fixed.** Both jq passes keep `2>/dev/null`: `journal_positive_scan` `:1135` and the aggregate `:1217`.
- **P2 fixed.** `JQ_POS_VEC` is cleared together with the other `JQ_*` outputs (`:1168`) and again on entry to the scan (`:1129`). The rc, stderr, timeout and parser-failure returns (`:1200-1220`) leave it empty. `journal_pos` (`:1307-1327`) prints `unavailable:<status>` when there is no vector.
- **P3 fixed.** The scan accepts only one line with an exact column count of `is_int` values (`:1139-1146`). The alarm lines print `boot=$BOOT_ID_EXPECTED` (`:1525`, `:1567`). No unit or record string is added.
- **P4 fixed.** Every positive selector starts with a `select(type=="object")` chain (`:1051`). The aggregate filters short-circuit with `and`, so non-object JSON neighbours grade `record-invalid` and the scan then runs. Verified on synthetic input with jq 1.8.2: a stream of `"str"`, `[1]`, `7`, `null` and valid records counted only the valid records. The `MESSAGE` canary key did not affect the count and was not printed.
- **P6 fixed.** `KILL_SIGNAL_JOURNAL` now carries `trust=client-supplied` (`:1567`).
- **P5: accepted as directed by L1 (INFO, no defect).** `JOURNAL_JQ_POS_SIGKILL` (`:1053`) matches EXIT_STATUS by type: the scalar string `"9"` or the scalar number `9`. Because jq evaluates `9.0 == 9` as true, number `9.0` also counts. Verified: the synthetic stream `[EXIT_STATUS 9.0, EXIT_STATUS "9"]` gives a positive count of 2. CensusPositive reports that L1's final r15 clarification requires exactly this. Remaining difference: the ok-path aggregate (`:975`, `tostring=="9"`) rejects a number `9.0`, which makes that record grade the class `record-invalid`, while the positive pass counts it. The raw count stays unavailable, so no total is fabricated. Real journalctl fields are strings, so there is no privacy or forgery impact. If L1 later wants both paths to agree, it is a one-line selector change.
