# ReviewRawTotals — round 15, claim C1 (read-only audit)

Scope: raw aggregates never salvaged into misleading zeros or totals; the planned
validated-positive tokens (`positive_kernel_oom`, `positive_unit_oom`,
`positive_unit_signal`, `positive_process_sigkill`) for C1. Target:
`tools/mori-census.sh` (script sha in `DC7D` tag). Read-only: no gates, builds,
tests, edits, or installs. No package installs were performed; the host safety
rule (pacman dry-run gate) was acknowledged and not triggered.

## Axes (godspeed)
- Coverage (judged): keep valid current-boot OOM/signal alarms when a sibling record is invalid.
- Honesty (guard): raw totals stay unavailable when invalid; no zero reads as "none".

## Current-state anchors (verified by reading)

| Anchor | What it does | Status for C1 |
|---|---|---|
| `tools/mori-census.sh:973-976` | `JOURNAL_JQ_TAIL`/`_MSGID`/`_SIGKILL`/`_SIGSEGV`: `if all(.[]; …) then ... else record-invalid/boot-mismatch/multi-boot end` | All-or-nothing. One bad record blanks the class. Root cause. |
| `:1000-1037` `JOURNAL_JQ_UNITS` | Same `all()` gate on the `d9b373ed` stream; subject validity and `UNIT_RESULT` are NOT in the gate (good) | Same all-or-nothing gate on identity/boot. |
| `:1046-1136` `journal_query` | Capture rc, stderr-nonempty, `jq -s` parse, then returns `record-invalid\|multi-boot\|boot-mismatch` at `:1103-1105` before any positive could be computed | Positive pass must be inserted before these returns. |
| `:1192-1229` `probe_journal` class loop | Per-class `JQ_N`/`JQ_STATUS` stored in `jn`/`js` | No positive storage yet. |
| `:1303-1332` OOM alarm | `oom_fire` set only from raw `ko`/`uo` numerics (`:1314-1321`) | Silences valid alarm when raw is unavailable. |
| `:1340-1353` user KILL_SIGNAL warn | `ps` / `us` raw numerics only (`:1344-1351`) | Same silencing for user signal/sigkill. |
| `:1380-1385` surface `rc=` | `rc_n=${src[$scope]:-0}`; `src` only set for `rc-*` at `:1223` | See finding F2. |

Confirmed in the round-14 regression pin, `tools/mori-round14-regressions.py`:
- `:105-109` names the limitation: "a valid OOM record plus a malformed MESSAGE_ID record … can silence a valid alarm; that residual limitation is named in the seat report for L1 routing."
- `:1552-1564` `R14_SEC_DUP_MSGID_MIXED` pins `kernel_oom_notice=unavailable:record-invalid` and `forbid_ids=FORBID_OOM` (`FORBID_OOM = (OOM_ID,)` at `:240`). Under C1 this stream must now fire `OOM_KILL_JOURNAL`, so this pin is a direct contract conflict.
- `R14_WRONG_BOOT_UNAVAILABLE` (`:1534`-ish, foreign-only) and `R14_IGNORE_FILTERS_INVALID` (MESSAGE_ID mismatch only) contain no current-boot valid positive, so they stay green under the planned design.

Grep confirmed: no `positive_` token exists in `tools/` or `corpus/`. Nothing is implemented yet.

## Findings

### F1 — HIGH (coverage). All-or-nothing gate silences valid alarms.
- Anchors: `mori-census.sh:973-976`, `:1037`, `:1103-1105`, `:1302-1332`, `:1340-1353`.
- Evidence: a stream of `[valid current-boot OOM record, malformed MESSAGE_ID array record]` makes `journal_query` set `JQ_STATUS=record-invalid`. The alarm checks `js=ok` and never sees the valid record. Result: no `OOM_KILL_JOURNAL`, no drift. This is exactly the residual the r14 pin names (`mori-round14-regressions.py:105-109`).
- Fix (planned C1 design, sketch, not applied): compute positives from the same `$raw` in `journal_query` before the `:1103` early return; store in `JQ_POS_*`.
  - Per-record filter, guarded so one bad row cannot error the pass:
    `[.[] | select(type=="object") | select((._BOOT_ID? | type)=="string" and ._BOOT_ID==$boot)] | …`
    then per class check `(.MESSAGE_ID? | type)=="string" and .MESSAGE_ID==$id`.
  - Unit OOM: `(.UNIT_RESULT? | type)=="string" and .UNIT_RESULT=="oom-kill"`, with NO subject-validity gate (matches `:1297-1298`).
  - Process SIGKILL: `(.EXIT_CODE? | type)=="string" and .EXIT_CODE=="killed"` and scalar status `(.EXIT_STATUS? | type) as $t | ($t=="string" or $t=="number") and (.EXIT_STATUS|tostring)=="9"`.
  - Output one integer per token; `is_int` each; on any capture/stderr/parse failure set `positive_*=unavailable:<same reason>`.
- Pin conflict: `R14_SEC_DUP_MSGID_MIXED` must be re-pinned by L1 (alarm fires; raw stays `unavailable:record-invalid`). Do not leave it green by weakening `FORBID_OOM`. Its comment at `:1547-1551` must be updated in the same change.

### F2 — MEDIUM (honesty). Surface `rc=` shows a misleading `0` on failed captures.
- Anchors: `:1189` (`src[$scope]=0`), `:1223` (only `rc-*` overwrites), `:1380` (`rc_n=${src[$scope]:-0}`), `:1387` (surface line prints `rc=$rc_n`).
- Evidence: a timed-out query (`CAP_RC` 124/137 → `JQ_STATUS=timeout`, `:1086`) or `stderr-nonempty` / `malformed-json` leaves `rc=0` beside `state=unavailable`. The count is correctly `unavailable:timeout`, but the rc field reads as success.
- Fix: record the real `CAP_RC` (or a non-zero sentinel such as `na:<status>`) for every non-`ok` status, not only `rc-*`. Check whether `R14_TIMEOUT_UNAVAILABLE` (`:1639`) pins `rc=0`; if so L1 re-pins.

### F3 — MEDIUM (honesty, C1 design risk). Positive `0` beside raw `unavailable` reads as reassurance.
- With raw invalid, `positive_kernel_oom=0` means "no valid positive found", not "no OOM". The planned surface must keep the raw token `unavailable:<reason>` visible on the same row and must never print a positive zero when the positive pass itself failed (print `unavailable:<reason>` instead).
- Also: the OOM finding must not carry a raw `count=` total when raw is unavailable. Existing `:1331` line already avoids `count=`; keep that when adding positive fields.

### F4 — LOW (correctness, design gap). Positive pass must not be inside the existing early returns.
- `:1103-1105` returns `record-invalid`/`multi-boot`/`boot-mismatch` before positives are evaluated. If the positive pass is placed after `:1135`, it is skipped exactly in the cases it exists to rescue. Insert it after capture + stderr checks (`:1091-1095`) and before the `parsed` path.
- The positive pass must set `positive_*=unavailable:<status>` on the `CAP_RC != 0`, `stderr-nonempty`, `no-timeout-bin` paths (`:1052-1055`, `:1083-1095`) too.

### F5 — LOW (robustness). `jq -s` is whole-stream; a line that is not JSON at all fails the positive pass.
- This matches the instruction not to repair arbitrary malformed JSON: report `unavailable:malformed-json`. Document it so the claim is not read as "any bad line is tolerated". Do not add a per-line parser.

## Interface checks against the spec (round-15 spec.json:3)
- "scalar matching MESSAGE_ID / scalar current _BOOT_ID": guard with `type` checks. Equality alone is scalar-safe for strings, but `.EXIT_STATUS|tostring` accepts a string `"9"` and a number `9`; state that explicitly in the finding.
- "OOM fires once if ANY independently valid positive OOM exists": the single `OOM_KILL_JOURNAL` line (`:1330-1332`) must gate on `oom_fire` set from `max(raw, positive)` per source, not raw alone.
- "User KILL_SIGNAL warn likewise": gate `:1344-1351` on positive `process_sigkill` (user) OR positive `unit_signal` (user). System scope remains info-only.
- Keep the six raw tokens and the `unit_*` split tokens byte-identical when valid; add positive tokens after them.

## Verification gaps (not run, per assignment)
- No jq run was performed on the proposed filter; behaviour above is from reading jq semantics and the existing filters.
- The selftest journal stub (`tools/mori-census.sh` dispatcher `journalctl) out_of journal`, cited as E13/D9) ignores arguments. Positive fixtures need the argument-aware r14 stub (`mori-round14-regressions.py` projects fields); confirm the round-15 fixture harness uses that stub before counting positive cases.
- Whether `R14_TIMEOUT_UNAVAILABLE` pins `rc=0` (F2) was not read to the assertion level.

## Installs / tools
None performed. No `pacman` run. No `-Sy/-Syu/-U/-R` run.

## Summary
- Raw totals are honest today: every invalid path grades `unavailable:<reason>` and no code path emits a numeric zero for a failed class (checked `:1122`, `:1228`, `:1243`, `:1305-1321`, `:1343-1347`, `:1362-1366`).
- The real defect is F1 (silenced valid alarms), which is the C1 target. F2 is the one misleading-zero token found (`rc=0` on failures).
- The C1 change requires L1 to re-pin `R14_SEC_DUP_MSGID_MIXED` and update its comment; leaving it green would contradict the planned behaviour.
