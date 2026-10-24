# AttackFalsePositive — round 15, C1 positive salvage

Seat: `MoriR15.AttackFalsePositive` (report only; no production edits, nothing executed against the census, no builds or tests).
Axis judged: coverage. Milestone: keep validated positives without making up totals.
Target: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh` at snapshot `#DC7D`.

## Axes

- **Coverage (claimed):** a critical OOM alarm or user KILL_SIGNAL warn survives when its own record is valid, even if a neighbouring record makes the class aggregate invalid.
- **No-harm guards (must not regress):**
  - An array, null, numeric, nested, foreign-boot or cross-class record must never fire an alarm.
  - Raw counts stay `unavailable:<status>` when invalid.
  - Capture and parser failure stays fully unavailable.

## Attack surface (anchors)

| Anchor | What it does today | Salvage risk |
|---|---|---|
| `:322-329` | Boot anchor: lowercase hex, 32 chars, else `''` | none if positives stay behind the `:1180-1185` gate |
| `:973-976` | Aggregate `all(...)`; `_BOOT_ID` is type `string` and `== $boot`; `MESSAGE_ID == $id`; `(.EXIT_STATUS\|tostring)=="9"` | copying `tostring` onto `_BOOT_ID` (A4) |
| `:1001-1018` | `subject` uses `(.UNIT // .USER_UNIT)`; `oom`/`sig` check that the type is string and the value matches exactly | copying the `//` idiom onto `_BOOT_ID`/`MESSAGE_ID` (A3); `subject` calls `has()` on non-objects |
| `:1019`, `:1037` | The invalid branch emits one bare word: `record-invalid`/`multi-boot`/`boot-mismatch` | positives must ride in this same jq output |
| `:1083-1102` | rc≠0, timeout, nonempty stderr or jq failure return before any count | must stay ahead of every positive (A11) |
| `:1103-1105` | Early return on the bare invalid word | a new `word\tposcols` form bypasses this case and reaches the width/int checks (A12) |
| `:1111-1134` | Exact width, integer columns, shell checks on nb/n/boot | an inconsistent vector must not leak positives (A12) |
| `:1303-1331` | OOM fires on `ko>0` or `uo>0`, and only from raw `ok` classes | add a positive path; never put 0 into the raw slot (A14) |
| `:1340-1353` | KILL warn reads `user:` keys only | the system scope must stay excluded (A10) |

## Parser facts I checked (jq at `/usr/bin/jq` = `jq-1.8.2`; `JQ_BIN` default `jq` at `:297`)

These are the only commands I ran. All were throwaway `jq -n` / stdin probes; the census was not run.

- **Numeric boot id passes `tostring`.** Record `{"_BOOT_ID":11111111111111111111111111111111}` (a number) with `--arg boot 11111111111111111111111111111111`:
  - `(._BOOT_ID|tostring)==$boot` gives `true`, because 1.8 preserves the integer literal.
  - `._BOOT_ID==$boot` gives `false`.
  - The fixture boot id is all `1`s, so this counterexample works directly against the fixture contract.
- **`index` is truthy on arrays and substrings.**
  - `["a","fe"]|index("fe")` gives `1`.
  - `"fe6f"|index("fe6f")` gives `0`, which is truthy in jq.
- **`tonumber` and `tostring` disagree on status values.**
  - `"09"|tonumber` gives `9`.
  - `9.0|tostring` gives `"9.0"`, while `9e0|tostring` gives `"9"`.
  - `9.0==9` gives `true`; `"9"==9` gives `false`.
- **Non-object records.**
  - `null|has("U")` gives `false` (no error).
  - `[1]|._BOOT_ID` raises an error.
  - Under `-s`, a top-level array record makes `.[]._BOOT_ID` fail, so jq exits nonzero and the result is `malformed-json`.
- **Duplicate keys:** `{"a":1,"a":2}|.a` gives `2` (the last one wins).
- **Extra finding:** in this shell, plain `jq` resolves to `jaq 3.1.1` (`~/.local/bin/jq`, not owned by any package). `/usr/bin/jq` is 1.8.2. The census calls `jq` through `PATH`.
  - So the parser that actually runs depends on PATH. jaq semantics can differ (for example `null|has`).
  - I did not compare their outputs for the census filters. L1 should pin `MORI_JQ_BIN`, or record which binary verification ran under.

## Counterexamples

Notation:
- `B` = `11111111111111111111111111111111`, `F` = `ffffffffffffffffffffffffffffffff`
- `K` = kernel id, `U` = unit id, `P` = process id
- Every case shows the stream contents and what a correct salvage must produce.
- "Excluded" means the record adds 0 to every `positive_*` and its class raw count stays `unavailable:<status>`.

| # | Stream (scope) | Record(s) | Raw status | Correct positive | want_oom / want_signal | Footgun that gets it wrong |
|---|---|---|---|---|---|---|
| A1 | user kernel | `{"_BOOT_ID":["B","F"],"MESSAGE_ID":"K"}` | record-invalid | kernel 0 | false / false | `any(._BOOT_ID[]?;.==$boot)`, `IN(...)`, `index($boot)`, `flatten`, `first` |
| A2 | system kernel | `{"_BOOT_ID":"B","MESSAGE_ID":["P","K"]}` (journalctl emits arrays for repeated fields; `MESSAGE_ID` can be set by the client) | record-invalid | kernel 0 | false / false | `.MESSAGE_ID\|index($id)` gives 1, truthy |
| A3 | user unit | `{"MESSAGE_ID":"U","UNIT_RESULT":"oom-kill","UNIT":"x.service"}` (no boot), plus the same with `"_BOOT_ID":null` and with `false` | record-invalid | unit_oom 0 | false / false | `(._BOOT_ID // $boot)==$boot`, copying the `.UNIT // .USER_UNIT` idiom at `:1006` |
| A4 | system kernel | `{"_BOOT_ID":11111111111111111111111111111111,"MESSAGE_ID":"K"}` (number) | record-invalid | kernel 0 | false / false | `(._BOOT_ID\|tostring)==$boot`, copying the `EXIT_STATUS` idiom at `:975`; **checked true on jq 1.8.2** |
| A5 | user kernel | `{"_BOOT_ID":"11111111-1111-1111-1111-111111111111","MESSAGE_ID":"K"}` plus valid `{"_BOOT_ID":"F","MESSAGE_ID":"K"}` | boot-mismatch | kernel 0 | false / false | `gsub("-";"")`, which copies the `tr -d -` at `:324` onto records; also `ascii_downcase` |
| A6 | user unit | `UNIT_RESULT` as `["oom-kill"]`, `null`, `"OOM-KILL"`, `"oom-kill "`, `"oom-kill-x"` (each with boot `B`, id `U`) next to one foreign-boot record | multi-boot | unit_oom 0 | false / false | `.UNIT_RESULT[]?`, `startswith`, `test("oom")`, `ascii_downcase`. Reuse `def oom`/`def sig` (`:1016-1017`) as they are. |
| A7 | user process | `EXIT_CODE ["killed"]`; `EXIT_STATUS` as `"09"`, `"9.0"`, `9.0`, `["9"]` (boot `B`, id `P`) | record-invalid | process_sigkill 0 | false / false | `tonumber==9` (`"09"`→9), `.EXIT_STATUS==9` (9.0→true), `[]?` |
| A8 | system kernel | `{"_BOOT_ID":"F","MESSAGE_ID":"K","X":{"_BOOT_ID":"B","MESSAGE_ID":"K"}}` | boot-mismatch | kernel 0 | false / false | `..\|objects`, `paths`, recursive descent |
| A8b | system kernel | top-level `[{"_BOOT_ID":"B","MESSAGE_ID":"K"}]` next to a valid-looking peer | jq error, so malformed-json | all positives **unavailable** | false / false | `.[]?\|.[]?`, `flatten`, `try` |
| A9 | user unit stream | `{"_BOOT_ID":"B","MESSAGE_ID":"K","UNIT_RESULT":"oom-kill","UNIT":"x.service"}` | record-invalid | unit_oom 0 **and** kernel 0 | false / false | testing positives against a set of all three ids instead of the stream's own `$id`; counting across streams |
| A10 | **system** process + **system** unit | valid `{"_BOOT_ID":"B","MESSAGE_ID":"P","EXIT_CODE":"killed","EXIT_STATUS":"9"}` and valid `{"_BOOT_ID":"B","MESSAGE_ID":"U","UNIT_RESULT":"signal","UNIT":"x.service"}`, each next to a foreign-boot record | multi-boot | system process_sigkill 1, system unit_signal 1 | **false / false** | firing the user warn from a positive of either scope (scope-blind `positive_*` lookup) |
| A11 | user kernel | valid `{"_BOOT_ID":"B","MESSAGE_ID":"K"}` with rc=1; same with rc=141; timeout 124; stderr 1 byte; same valid line followed by a truncated `{"_BOOT_ID":` | rc-1 / rc-141 / timeout / stderr-nonempty / malformed-json | all positives **unavailable** | false / false | parsing before the rc/stderr gate; line-wise `fromjson?` or `try` repair; `--seq` |
| A12 | user kernel | the filter's invalid branch emits `record-invalid\t<pos>` | — | positive accepted only if the width is exact and every column passes `is_int` | — | an unvalidated positive column after the `:1104` bypass; positives kept from an ok vector that fails `:1121-1134` (n>0 with nb=0, nb≠1, non-hex boot) |
| A13 | both | `MORI_BOOT_ID=not-a-boot-id`; record `{"_BOOT_ID":"","MESSAGE_ID":"K"}` | `boot_id=unavailable` (`:1180`) | positives unavailable; no query | false / false | computing positives with `--arg boot ""` before or outside the gate |
| A14 | user kernel | foreign-boot only, `{"_BOOT_ID":"F","MESSAGE_ID":"K"}` | boot-mismatch | `positive_kernel_oom=0` beside `user_notice=unavailable:boot-mismatch` | false / false | writing the positive into the `ko` raw slot (`:1305`), which turns the unavailable total into `user_notice=0`; a finding body showing `count=0` |

Control (salvage must fire), one per path:
- **Kernel OOM:** user kernel stream `[{"_BOOT_ID":"B","MESSAGE_ID":"K"}, {"_BOOT_ID":"F","MESSAGE_ID":"K"}]`.
  - Expected: multi-boot, `positive_kernel_oom=1`, `want_oom=true`, raw `user_notice=unavailable:multi-boot`.
- **User signal:** user unit stream `[{"_BOOT_ID":"B","MESSAGE_ID":"U","UNIT_RESULT":"signal","UNIT":"x.service"}, {"_BOOT_ID":["B"],"MESSAGE_ID":"U"}]`.
  - Expected: record-invalid, `positive_unit_signal=1`, `want_signal=true`.
  - Unit counts and owner partition stay unavailable; no `UNIT_FAILURE_*` route line.

## Smallest required behaviour

1. **One positive predicate per stream, inside the existing single jq pass.** Same `CAP_OUT`, no new query.
   - Shape: `[.[] | select(type=="object" and (._BOOT_ID|type)=="string" and ._BOOT_ID==$boot and (.MESSAGE_ID|type)=="string" and .MESSAGE_ID==$id)]`.
   - Then the class test on that list:
     - **kernel:** none.
     - **unit:** the existing `oom` / `sig` defs (`:1016-1017`).
     - **process:** `(.EXIT_CODE|type)=="string" and .EXIT_CODE=="killed" and ((.EXIT_STATUS|type)=="string" or (.EXIT_STATUS|type)=="number") and (.EXIT_STATUS|tostring)=="9"`. This keeps today's accepted forms `"9"`, `9` and `9e0`, and rejects `9.0`, `"09"` and arrays.
   - Use exactly one level of `.[]`.
   - Never use these on identity fields: `//`, `tostring`, `tonumber`, `index`, `IN`, `any(...[]?)`, `..`, `flatten`, `try`/`?`, `ascii_downcase`, `gsub`.
   - Never use the `tonumber` / `index` / `IN` forms on result or status fields either.
2. **Positives only on a validity verdict.**
   - Allowed when the status is `ok` or a jq-emitted `record-invalid|multi-boot|boot-mismatch`, and the emitted positive column passes `is_int` with an exact width check.
   - Unavailable for:
     - `no-timeout-bin`, `rc-*`, `timeout`, `stderr-nonempty`
     - `jrc≠0` (`malformed-json`), wrong width
     - the shell-side inconsistency checks at `:1121-1134`
     - the boot-anchor gate at `:1180`
3. **Echo only the boot id the shell validated.** Salvage output never prints any record-derived string (no `[.[]._BOOT_ID][0]` from a mixed stream). `boot=` stays `$BOOT_ID_EXPECTED`.
4. **Positives stay in their own stream and scope.**
   - `positive_kernel_oom` comes only from the kernel stream.
   - `positive_unit_*` comes only from the unit-failure stream with `$id`=U.
   - `positive_process_sigkill` comes only from the process stream with `$id`=P.
   - OOM fires once on any scope's kernel or unit-oom positive.
   - The KILL warn reads only `user:` positives (`:1340-1343`).
5. **Separate tokens, separate slots.** Raw `ko`, `uo`, `uou`, `ps` and `us` keep `unavailable:<status>`. Positive tokens sit beside them. A positive of 0 never replaces a raw slot, and is never printed as `count=`.
   - `KILL_SIGNAL_JOURNAL` at `:1353` currently prints `count=$ps`. When the raw count is unavailable, that must stay `count=unavailable:<status>`, not the positive.
6. **Path naming.** `paths=` must say whether an alarm came from a positive or from a raw count; reusing `kernel_oom_notice` / `unit_result_oom_kill` from raw-only logic is wrong.
   - The salvage path must set `oom_path_k`/`oom_path_u` from positives, not leave `paths=` empty.
   - Whether the path label changes is a contract question, not a safety one.

## Classification

- **Fixable defects** (implementation hazards; the rules above remove them): A1–A9, A11–A14.
- **A10 is not a defect today.** It becomes one only if salvage looks up positives without a scope.
- **Residual, not salvage-specific:** duplicate JSON keys (last wins). jq parses the stream identically for the aggregate and the positives, and journalctl never emits duplicate keys, so the canonical judge should not hold this against salvage.
- **jq vs jaq on PATH** is an operability and verification-provenance risk, not a coverage defect. L1 should pin the binary used for verification.

## Tooling

No installs or upgrades. The post-interjection host rule was observed: no `pacman` was invoked.
