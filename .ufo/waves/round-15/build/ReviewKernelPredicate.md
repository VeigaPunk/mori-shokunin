# ReviewKernelPredicate: positive kernel/unit/process selectors (round 15, C1)

Scope: read-only audit of `tools/mori-census.sh` against the round-15 contract for
`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`.
No code edited. No gates, builds, tests, or journal queries run. No installs performed (the
parent's host-safety directive was received; nothing needed installing for a read-only audit).

## Godspeed posture
- **Axes:** coverage (judged). Operability is a constraint: no new journal query, no new route.
- **Moves kept:** a second `jq` pass over the already-captured `$raw` (no journalctl), which
  improves coverage and harms no axis.

## Current target state (observed)
- `grep positive_` over the lane returns **zero hits** in `tools/mori-census.sh`. None of the four
  tokens exists yet. Every OOM/KILL predicate is still aggregate-gated.
- Aggregate gating is the root cause of the coverage loss. `JOURNAL_JQ_TAIL` (`:973`),
  `JOURNAL_JQ_MSGID` (`:974`), `JOURNAL_JQ_SIGKILL` (`:975`) and the unit filter `:1019-1037` all
  start with `if all(.[]; <every record valid for $boot and $id>) then ... else <one bare token>`.
  One foreign-boot, array-valued, or nonmatching record collapses the whole class to
  `record-invalid` / `boot-mismatch` / `multi-boot`. No per-record count survives.

## Verified-correct anchors (keep as is)
- Boot anchor is shape-validated, so the earlier concern is withdrawn: `:322-329` (32 lowercase hex
  via `case` plus length check). The selftest at `:3250-3254` (`MORI_BOOT_ID=not-a-boot-id` →
  both scopes unavailable) pins it.
- Type guards already present on the aggregate: `type == "object"` before any `._BOOT_ID` access
  (`:973`, `:1019`). `and` short-circuits, so a bare string/number element cannot raise a jq error
  there. A positive pass must keep the same ordering.
- Array/null `_BOOT_ID` and `MESSAGE_ID` never equal a scalar string in jq, so `==` against `$boot`
  and `$id` is already scalar-exact. Explicit `(x|type)=="string"` guards are still recommended
  for readability and to make the contract visible.
- `UNIT_RESULT` oom/signal (`:1016-1017`) is type-guarded and independent of subject (`:1001-1014`).
  Subject validity does not gate it. The positive unit counters must reuse those `oom`/`sig`
  definitions, not a new one.
- Alarm firing is confined to `:1303-1332` (OOM) and `:1340-1354` (KILL). Both currently read raw
  counts only.

## Findings (by severity)

### F1 (high, coverage): positives are not computed when the aggregate is invalid
- `journal_query` (`:1046-1136`) returns at `:1103-1105` (`record-invalid|multi-boot|boot-mismatch`)
  before any count parsing. The filter emits no positive columns in those branches.
- **Fix:** after the successful capture and `jrc==0` (after `:1100`, before the status `case` at
  `:1103`), run a second `"$JQ_BIN" -s -r --arg boot ... "$POS_FILTER"` on `"$raw"`. Its output is
  a fixed-width integer row. Store it in `JQ_POS` (or `JQ_POS_OOM`/`JQ_POS_SIG` per class). Use
  the same `$raw`. No journalctl call is added.
- Set the positive state on every early exit so it can never be stale:
  `:1054` (no-timeout-bin), `:1083-1089` (rc/timeout), `:1091-1095` (stderr-nonempty),
  `:1102` (malformed-json) → positive = `unavailable:<JQ_STATUS>`.
- Reset `JQ_POS*` at `:1051` alongside the other `JQ_*` resets.

### F2 (high, correctness): positive filter must be per record, not `all()`
Positive filter shape, per scope and per class:
```
[ .[] | select(
    type == "object"
    and ((._BOOT_ID | type) == "string") and ._BOOT_ID == $boot
    and ((.MESSAGE_ID | type) == "string") and .MESSAGE_ID == $id
    <class extras>
) ] | length
```
Class extras:
- `kernel_oom` (`fe6faa94…`): none beyond the above.
- `unit_failure` (`d9b373ed…`): two counts from the same stream.
  - `positive_unit_oom`: `(.UNIT_RESULT|type)=="string" and .UNIT_RESULT=="oom-kill"`
  - `positive_unit_signal`: `(.UNIT_RESULT|type)=="string" and .UNIT_RESULT=="signal"`
  - Neither clause consults UNIT/USER_UNIT. Subject is irrelevant to a positive.
- `unit_sigkill` (`98e32220…`): `(.EXIT_CODE|type)=="string" and .EXIT_CODE=="killed"` and
  `EXIT_STATUS` scalar `9`. The existing `(.EXIT_STATUS|tostring)=="9"` accepts string `"9"` and
  number `9`, and rejects arrays and objects. Keep that, but make the scalar guard explicit:
  `((.EXIT_STATUS|type) | IN("string","number")) and ((.EXIT_STATUS|tostring)=="9")`.
  (Decision for main: the contract says "scalar status 9". Accepting number 9 follows that literally.
  Tell me if string-only is wanted.)

### F3 (high, coverage): OOM alarm must fire on positives; path token must exist
- `:1303-1321` sets `oom_fire` only from raw `ko`/`uo`. Add: fire if
  `positive_kernel_oom(scope) > 0` or `positive_unit_oom(scope) > 0`, for either scope, regardless
  of raw status. An unavailable positive never fires.
- `:1328-1329` builds `oom_paths` only from the raw flags `oom_path_k`/`oom_path_u`. A positive-only
  fire yields `paths=` empty. Set `oom_path_k`/`oom_path_u` from the positive counts too, or add
  `positive_kernel_oom` / `positive_unit_oom` path names. Without this the finding line carries no
  reason.
- `:1323-1325`: append the positive tokens to `oom_fields` per scope, with their unavailable form.
- Keep "EXACTLY ONE" (`:1330-1332`). Do not add a second OOM line.

### F4 (high, coverage): user KILL warn must use positive user unit-signal and process-sigkill
- `:1340-1351`: `kill_fire` is raw-only. Add: fire if user `positive_process_sigkill > 0` or user
  `positive_unit_signal > 0`. Set `kill_paths` from the positive source when the raw one is
  unavailable.
- Only the user scope warns. System positives are evidence fields only (`:1356-1388` surface rows).
- `:1353` already states "counters are separate and never summed". Keep that wording.

### F5 (medium, contract): per-scope token naming is ambiguous. Decision needed
- The spec names the tokens `positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`,
  `positive_process_sigkill` and calls them "per-scope". The existing finding style is scope-prefixed
  (`user_notice=`, `system_unit_oom=`, `:1323-1325`).
- Recommendation: in each `SURFACE journal.<scope>` row (`:1384-1387`), emit the literal
  `positive_kernel_oom=N|unavailable:<reason>` (scope is implicit in the row). In the
  `OOM_KILL_JOURNAL` and `KILL_SIGNAL_JOURNAL` lines, emit `user_positive_*` / `system_positive_*`
  (matching `user_unit_oom=`). The literal-name grep in the harness must then match per row, not
  per line.
- Caution: `\bpositive_kernel_oom` does not match `user_positive_kernel_oom`, because `_` is a
  word character. Harness regexes must pick one form deliberately.

### F6 (medium, drift): decide whether new counters are masked
- `DRIFT_COUNTER_KEYS` (`:2254-2260`) does not list `kernel_oom_notice`, `user_unit_oom`, or
  `process_sigkill`. Raw counts are therefore unmasked, and drift stays visible. Keep the new
  positive counters unmasked too, to match. Adding them would be a counter mask that hides
  changes, which is out of scope this round (no repin, no mask widening). Flag for L1 / DriftScope.

### F7 (medium, contract): positive finding must stay client-supplied
- Positive tokens count client-supplied `MESSAGE_ID` (`:1331` already says `trust=client-supplied`).
  Keep that marker on the OOM and KILL lines. Do not add "authenticated", "victim", or "kill total"
  wording.

### F8 (low, residual, not a defect): syntax-malformed JSON still voids positives
- A single non-JSON line makes `jq -s` exit nonzero (`:1099-1102`). The contract says positives
  are unavailable on parser failure, so this is compliant. It is the real limit of "preserve
  positives from adjacent malformed records": it covers schema-invalid records (wrong types,
  array fields, foreign boot, nonmatching ID), not syntactically broken lines. Name this in the
  finding limits. Do not try to repair JSON.

## Test/fixture notes (for harness owner; no execution by me)
- Existing checks that must still hold: foreign-boot unavailable (`:3224-3228`), multi-boot
  (`:3230+`), record identity mismatch (`:3221-3222`), stderr/rc unavailable (`:3186-3189`).
  Each now also needs `positive_*` with the **same** fixture, showing positives survive while raw
  stays unavailable.
- Stub dispatch (`:2540-2566`) keys on MESSAGE_ID prefix and returns the whole slot file. Mixed
  valid/invalid fixtures (foreign boot + valid current boot) fit one slot file, so no stub change
  is needed. The `jrec` helper (`:3008`) writes a `MESSAGE` canary. Fixture packs must not do that.
- Boot anchor for pack fixtures is `11111111111111111111111111111111`. The harness must set
  `MORI_BOOT_ID` to that value for the pack run; the selftest default `0123…cdef` will not match.

## Necessary fixes (ordered)
1. F1: second jq pass over `$raw` in `journal_query`; positive state on every early exit.
2. F2: per-record positive filters for kernel, unit (oom+signal), sigkill.
3. F3: OOM fire and path tokens from positives (`:1303-1332`).
4. F4: KILL fire and path tokens from user positives (`:1340-1354`).
5. F5: decide naming (per-row literal vs scope-prefixed) and record it.
6. F6/F7: keep positives unmasked; keep `trust=client-supplied`.

## Verification gaps
- Nothing executed. Every claim above is from reading the source at the cited lines.
- The positive filter, the stub behaviour under mixed fixtures, and the drift-mask outcome are
  unverified until L1 runs the gates once after integration.
- F5 and the EXIT_STATUS scalar policy (F2) are decisions for the main agent, not verified facts.
