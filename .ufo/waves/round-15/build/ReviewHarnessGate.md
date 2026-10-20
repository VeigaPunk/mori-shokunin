# ReviewHarnessGate — round-15 C1 (positive OOM/signal evidence), read-only audit

Scope: `tools/mori-census.sh` (census + `--pin`/`--drift`/`--selftest` gate), its
cross-file harness contracts (`tools/mori-round14-regressions.py`), exit codes 0/1/2,
and isolated self-invocation. No builds, tests, gates, or installs were run. Nothing
was installed (parent host-safety rule noted; no `pacman` invoked). No production file
was edited.

## Status of C1 in the current target

- **Not implemented.** No `positive_kernel_oom`, `positive_unit_oom`,
  `positive_unit_signal`, or `positive_process_sigkill` token exists anywhere under
  the lane (grep over the repo: no hits).
- **Root cause of the coverage loss (verified by reading):** every journal class is
  gated by one all-or-nothing jq pass over the whole stream.
  - Class filters: `JOURNAL_JQ_MSGID` / `JOURNAL_JQ_SIGKILL` / `JOURNAL_JQ_SIGSEGV`
    at `tools/mori-census.sh:974-976`, and the unit filter at `:1019-1037`. Each begins
    `if all(.[]; … and ._BOOT_ID == $boot and .MESSAGE_ID == $id)`; any failing record
    falls to the `else` branch and yields `record-invalid` / `multi-boot` /
    `boot-mismatch` for the entire class.
  - Early returns in `journal_query` at `:1102-1105` drop the stream before any count
    is taken.
  - `probe_journal` reads counts only when `js == ok`: `:1243-1245` (class findings),
    `:1266` (unit routing), `:1305-1313` (OOM inputs), `:1341-1343` (KILL inputs).
  - Effect: one malformed MESSAGE_ID array or one foreign-boot record in an otherwise
    valid current-boot kernel stream silences `OOM_KILL_JOURNAL` (`:1316`, `:1320`
    cannot fire because `ko`/`uo` are `unavailable:*`). The same holds for
    `KILL_SIGNAL_JOURNAL` (`:1344-1351`).
- This is the exact residual the r14 harness names as an accepted limitation
  (`tools/mori-round14-regressions.py:106-109`).

## HIGH

### H1. Positive evidence must be computed before the aggregate gate (implementation anchor)
- Required behavior (spec): per-scope `positive_*` counts from individually valid
  current-boot records in the SAME captured, successful, stderr-free stream; no new
  journal query; capture/parser failure → `unavailable:<reason>`; raw aggregate tokens
  unchanged.
- Fix anchors:
  1. In `journal_query` (`:1046-1135`), after the capture checks (`:1083-1095`) and the
     successful whole-stream parse (`:1099-1102`), but BEFORE the early returns at
     `:1103-1105`, run a second jq pass over `$raw` (`JQ_POS`). Multi-boot and
     record-invalid streams must still yield positives; the current boot is the only
     admissible boot.
  2. The positive filter must short-circuit on type: `[.[] | select(type=="object")
     | select((._BOOT_ID|type)=="string" and ._BOOT_ID==$boot and (.MESSAGE_ID|type)=="string" and .MESSAGE_ID==$id) …] | length`.
     Field access on a non-object input is a jq error and would turn the whole
     positive into `malformed-json`; the `select` must come first.
  3. Field sets already requested need no new query: kernel stream requests
     `_BOOT_ID,MESSAGE_ID` (`:1219`); unit stream requests `UNIT_RESULT` (`:1201`);
     sigkill stream requests `EXIT_CODE,EXIT_STATUS` (`:1196`). Positive unit tokens
     come from the unit stream (`UNIT_RESULT` exact string `oom-kill` / `signal`);
     process positives from the sigkill stream (`EXIT_CODE` exact `killed`,
     `EXIT_STATUS` scalar `9`).
  4. Feed the positive counts into `oom_fire` (`:1316`, `:1320`) and `kill_fire`
     (`:1346`, `:1350`) independently of `js`. Keep raw `ko`/`uo`/`ps`/`us` as
     `unavailable:<reason>` when invalid. Add the four positive tokens to the
     `OOM_KILL_JOURNAL` (`:1331`) and `KILL_SIGNAL_JOURNAL` (`:1353`) fields, and to the
     per-scope surface rows.
  5. Parser-level failure (`JQ_STATUS=malformed-json`, `stderr-nonempty`, `rc-*`,
     `timeout`) must set positives to `unavailable:<JQ_STATUS>`, never 0.
- Known semantics relied on (not executed here): jq `.field` on a non-object input
  errors; `tostring` on an array yields `"[9]"`, so the `"9"` comparison already
  rejects arrays.

### H2. Retained r14 regression case 28 forbids the behavior C1 requires
- `tools/mori-round14-regressions.py:1547-1564` (`R14_SEC_DUP_MSGID_MIXED`): stream =
  one valid kernel OOM + one `MESSAGE_ID=[…]` record; expects
  `kernel_oom_notice=unavailable:record-invalid` AND `forbid_ids=FORBID_OOM`
  (`OOM_KILL_JOURNAL`).
- Under C1 the raw token stays `unavailable:record-invalid` (correct) but the alarm
  MUST fire with `positive_kernel_oom=1`. As written, the harness will go RED after H1
  lands. Harness owner must invert `forbid_ids` for that case to an expected
  `OOM_KILL_JOURNAL` with a positive field, and keep the raw-unavailable assertion.
  This is a required harness edit, not a production defect.
- Cases that still hold under C1 (verified by reading, not execution):
  - `R14_IGNORE_FILTERS_INVALID` (`:1531-1545`): only an OOMD record; positives must
    be `positive_kernel_oom=0`, not unavailable; no alarm.
  - `R14_WRONG_BOOT_UNAVAILABLE` (`:1502-1514`) and `R14_MULTI_BOOT_UNAVAILABLE`
    (`:1516-1529`): all records foreign-boot; positives 0; no alarm. Stays valid only
    if the positive filter enforces `_BOOT_ID == $boot` (see H1.2).
  - `R14_MALFORMED_UNAVAILABLE` (`:1489-1500`): whole stream unparseable; positives
    unavailable; no alarm.

### H3. Boot-anchor mismatch between the fixture pack and the gate's pinned boot
- Spec fixtures use `_BOOT_ID='11111111111111111111111111111111'`. The bash selftest's
  `sut_env` pins `MORI_BOOT_ID=0123456789abcdef0123456789abcdef`
  (`tools/mori-census.sh:2712`), and the r14 Python stub uses the same `0123…` value
  (`mori-round14-regressions.py:670`, `JOURNAL_BOOT`).
- The value `1111…` is valid 32-lowercase-hex and passes the `*[!0-9a-f]` check
  (`:1131`), so it is not rejected for form; but a pack consumed without overriding
  `MORI_BOOT_ID` grades every record `boot-mismatch`. Positives then read 0 and the
  case fails for the wrong reason.
- Fix: the pack consumer must set `MORI_BOOT_ID=1111…` (in `sut_env` for the pack path)
  or the pack must use the harness's boot. Document the choice in the fixture README.

## MEDIUM

### M1. Drift masking registry does not include the new integer tokens
- `DRIFT_COUNTER_KEYS` (`tools/mori-census.sh:2254-2270`) masks integer counters to
  `<V>` in `drift_normalize` (`:2277-2293`). The new positive counts are live integer
  measurements and must join the list, or every `--pin` baseline drifts on every
  positive-count change.
- Add exactly: `positive_kernel_oom positive_unit_oom positive_unit_signal
  positive_process_sigkill`. Listing `unit_oom` does NOT mask `positive_unit_oom`
  (the `\b` boundary fails after `_`), so each literal must be listed.
- `unit_signal`, `user_unit_signal`, `process_sigkill` are already listed
  (`:2268-2269`), so the registry is partly pre-staged for this change.

### M2. `--drift` ignores the census's own verdict and rc (exit-2 contract)
- `run_drift` calls `cap_census` (`:2484`) and never reads `CENSUS_RC`. The header
  contract says exit 2 = setup/usage; a live census that aborts before its verdict
  (for example a `set -euo pipefail` abort, rc 1, or a partial capture with no
  `MORI_CENSUS:` line) is compared as text and reports `MORI_DRIFT: …` with exit 1.
- rc alone is ambiguous: `run_census` exits 1 for legitimate DRIFT and a crash under
  `set -e` also exits 1. The discriminator is the verdict line. Fix: after `:2484`,
  require `grep -qE '^MORI_CENSUS: (CLEAN|DRIFT) '` on `CENSUS_CAPTURE` and that
  `CENSUS_RC` matches (`CLEAN`↔0, `DRIFT`↔1); otherwise `printf` a diagnostic and
  `exit 2`.
- No selftest case covers a census that dies before its verdict. Add one.

### M3. Empty path argument silently runs a live census
- `main` (`tools/mori-census.sh:3819-3821`) checks only `[ $# -ge 2 ]`. `--pin ""` sets
  `pin_path=""`; the `[ -n … ]` guards at `:3831` and `:3835` are false, and control
  falls through to `run_census live` (`:3839`). Result: exit 0/1 from a live census
  where the usage contract demands exit 2.
- Same for `--drift ""`.
- Fix: `die_usage` when the argument is empty (`[ -n "${2:-}" ]`).
- Add two selftest cases: `--pin ""` and `--drift ""` both expect exit 2.

## LOW

### L1. `check_cli` is not isolated (violates the one-environment rule)
- `check_cli` runs `bash "$SELF"` with the caller's inherited environment
  (`tools/mori-census.sh:2785`), while `check()` (`:2739`) and `pd_run` (`:2809`) run
  `env -i "${SUT_ENV[@]}"`. The comment at `:2681-2685` says `sut_env` is "the ONE
  fixture environment every census invocation gets".
- Present cases (`--bogus`, `--help`, `--pin` and `--drift` with no path) exit before
  any probe, so there is no false result today. Any future `check_cli` case that
  reaches a probe would read the host journal and the caller's `MORI_*`.
- Fix: call `sut_env` and run `env -i "${SUT_ENV[@]}" bash "$SELF" "$@"`.

### L2. Conflicting mode flags are silently resolved by precedence
- `main` (`:3816-3838`) returns at the first matched mode: `--selftest` beats
  `--pin`, which beats `--drift`. `--pin a --drift b` runs pin only with exit 0.
- Fix: `die_usage` on more than one mode flag.

### L3. Host-dependent helpers inside the hermetic selftest
- `sut_env` sets `PATH="$bin:/usr/bin:/bin"` (`:2688`). `jq` and `timeout` resolve from
  the host, so journal and tmux-timeout cases depend on host binaries. Expected output
  is independent of the host version, but any positive-token case that relies on jq
  `tostring` semantics inherits that dependency. Pin `MORI_JQ_BIN` in the positive
  cases if that matters.

## Verified clean (read-only evidence)

- Exit-code mapping: `run_census` CLEAN→0, DRIFT→1, else→2 (`:2227-2231`); selftest
  exits `FAIL==0` (`:3811`) under `set -euo pipefail` (`:255`).
- `die_usage` exit 2 (`:396`); `--help` exit 0 (`:3822`); `--pin` write failure exit 2
  (`:2433-2435`); `--pin` exit 0 regardless of roll (`:2437-2438`, as documented).
- `--drift`: missing/unreadable/no-marker/no-volatile-contract/empty-block → exit 2
  (`:2445-2476`); volatile-list change → exit 1 (`:2482`, `:2492-2494`); no-diff → exit 0
  (`:2496-2497`); diff → exit 1 (`:2502-2503`).
- Selftest isolation: `check()` (`:2739`) and `pd_run` (`:2809`) use `env -i` with
  `sut_env`; `fx_no_mutation` hashes the fixture before and after (`:2617-2619`,
  `:2775`), so the read-only claim is checked, not asserted.
- Mutants (`:2776`, `:2786`) are guarded by `cmp -s` anchor checks before use.

## Required fixes (ordered)

1. H1 — `journal_query`: add the positive jq pass on `$raw` before the early returns
   (`:1102-1105`); guard with `select(type=="object")`; emit the four tokens per scope;
   feed `oom_fire` (`:1316/:1320`) and `kill_fire` (`:1346/:1350`) independently of `js`.
2. H1 — add the four tokens to `OOM_KILL_JOURNAL` (`:1331`), `KILL_SIGNAL_JOURNAL`
   (`:1353`), and the per-scope surface rows (`:1383-1387`). Raw tokens unchanged.
3. M1 — add the four keys to `DRIFT_COUNTER_KEYS` (`:2254-2270`).
4. H2 — harness owner: invert `R14_SEC_DUP_MSGID_MIXED` (`mori-round14-regressions.py:1547-1564`)
   to expect the alarm with `positive_kernel_oom=1` and raw `unavailable:record-invalid`.
5. H3 — fixture consumer: set `MORI_BOOT_ID=1111…` for pack cases, or re-anchor the packs.
6. M2 — `run_drift`: require a verdict line and matching rc; exit 2 otherwise; add a
   selftest case.
7. M3 — `main`: reject empty `--pin`/`--drift` paths with exit 2; add two selftest cases.
8. L1 — `check_cli`: isolate with `env -i "${SUT_ENV[@]}"`.
9. L2 — `main`: reject conflicting mode flags with exit 2.
10. Docs (not edited here): header block `:893-965`, usage `:377-391`, and
    `drift` header `:154-193` need the r15 positive-token contract. The fixture
    directory `.ufo/waves/round-15/fixtures/` does not exist yet (checked by glob), so
    no pack is consumable until the pack seats land.

## Residual risk and verification gaps

- Nothing was executed. Positive-count, jq-semantics, and exit-code claims are from
  reading the code; each H/M item needs a selftest or harness case when implemented.
- The alarm-silencing limitation remains for malformed JSON (whole-stream parse fails):
  by spec this is out of scope and stays `unavailable`, so no alarm can fire for that
  class. The report makes no completeness claim.
- No authenticated IDs, unique-victim counts, or malformed-JSON repair are claimed.
- Tool installs: none. Parent host-safety rule received; no `pacman` run.

## Final bounded static re-review — tools/mori-round15-regressions.py

Pinned bytes checked: sha256 3f1cdcfd7c9a3486c0dd941a145a2cbbd31deaaa9db133445f40b12477e5627b (2154 lines), matches the SHA3f1cdcfd pin. Read-only static review of execution, expected pin, control verdict, capture-failure availability, and output guard. No tests, gates, smokes, or installs run. Author-lane internal review only; L1 holds final verification.

No catastrophic defect was found on the SUT verdict path. The only destructive call is `shutil.rmtree` at line 934, confined to `output/fixtures/<cid>`, and case ids are regex-confined (166, 518), so traversal is blocked. Output covering or containing the repo is refused (1363-1364). The two control-verdict defects below (F1, F2) are the items that make exit 0 untrustworthy and should block L1 sign-off.

### F1 HIGH — red-relevant control accepts any frozen failure (fabricated control confirmation)
- `run_gate` 1502-1509: `red_confirmed` is set whenever the frozen run is not `fok`. `fok` is any base-check failure, including `exec_error` (1036-1037), `harness_timeout` (1034-1035), `bare_journalctl_tripwire` (1046-1047), `missing_surface`, and script-sha mismatch.
- Consequence: if the frozen target cannot execute or times out on every red-relevant case, control reads `red_confirmed`, and the gate exits 0 when the SUT passes (1686-1691). The entering red state was never reproduced.
- Fix: confirm a red-relevant control only when the frozen run completed (not timed_out, no error, rc consistent with its verdict) AND the missing alarm is the failing reason: `oom_lines==0` for want_oom, or `kill_lines==0` for want_signal. Any other frozen failure is `control_inconclusive` and exits 2.
- Not covered by selftest: every selftest gate run passes `--no-frozen-control` (2044, 2069), so the 1502-1515 path never runs in selftest.

### F2 HIGH — control can be silently disabled by two suppressed flags, exit 0
- `parse_args` 2109-2112 hides `--no-frozen-control` and `--selftest-child` via `argparse.SUPPRESS`. `main` 2130-2134 accepts `--no-frozen-control` when `--selftest-child` is also present. `run_gate` 1678-1681 then prints `GATE PASS exit=0`.
- This contradicts the EXIT MAP (header 91-92: exit 0 requires the frozen control to reproduce) and the message at 2131-2133 ("a normal run must include the pinned frozen control").
- Fix: make the no-control path reachable only from the in-process `selftest()`, for example by passing a private argument object, not a CLI flag. Or refuse exit 0 whenever `frozen_skipped` is true outside selftest.

### F3 MEDIUM — capture rc expectation mismatches census mapping for 124/137 (false red, not false green)
- `normalize_capture` 398-399 sets `status="rc-%d"` for every rc 1..255. The census maps `124|137` to `JQ_STATUS=timeout` (`tools/mori-census.sh:1085-1087`).
- A pack using rc 124 or 137 would expect `unavailable:rc-124` and the SUT would correctly report `unavailable:timeout`, producing a red SUT result.
- Fix: mirror the census map (124/137 → `timeout`) or refuse those values in the schema.

### F4 MEDIUM — `revision.stable` is always false when output lies inside the repo
- `revision_core` (838-839) keeps the full `dirty_paths` list, including output-scope paths. Output files are created during the run (targets at start, runs and fixtures afterwards), so `stable` compares unequal (1576-1579).
- Not exit-driving, but the provenance field misreports, contrary to the CE3/CE4 intent that output scope is excluded.
- Fix: compare only `head` and `dirty_outside_harness_output_paths` across start and end.

### F5 MEDIUM — output guard does not protect frozen, expected, or pre-existing output subpaths
- `guard_output` (1352-1370) does not refuse output that covers `.ufo/waves/round-15/frozen/` or the `expected.json` path. With `--fixtures` elsewhere, `--output .ufo/waves/round-15` is allowed.
- In that case `capture_revision` excludes `frozen/` from the outside-dirty list (CE3). The `output_scope.note` at 832 claims "frozen inputs are never excluded", which the code does not enforce.
- `atomic_bytes(output/"expected.json", expected_raw)` (1431) writes the table read at 1398. If the pin is regenerated mid-run, the gate overwrites the new pin with the old bytes.
- `build_case_fixture` (933-934) `rmtree`s `output/fixtures/<cid>`. The guard checks only the resolved output root, so a pre-existing symlink at `output/fixtures` pointing into the declared fixtures would redirect the rmtree into inputs.
- Fix: refuse output that covers or links to the frozen dir, the expected file's directory, or fixtures; reject symlinked `output/{fixtures,targets,runs}` before writing; correct the note at 832 or enforce it.

### F6 LOW-MEDIUM — hashed bytes are not guaranteed to be executed bytes (CE6)
- `load_r14` (286) executes the module via `SourceFileLoader`. That loader can take bytecode from `__pycache__` validated only by mtime and size, while the gate hashes source bytes read separately (1386, 1388).
- The gate's own bytes have the same window: `gate_sha` is read at 1383 after Python has already loaded the file at startup.
- Fix: read each verdict-driving file once, hash those bytes, and execute `compile(data, path, "exec")` into the module dict. Do not reread for hashing.

### F7 LOW — silent fallback on git-blob tamper
- `resolve_frozen` (732-754) catches `SetupError`, which includes `SnapshotTampered`. A git blob that fails the pin falls back to the on-disk copy with the source reported as `path:` and no disclosure.
- The pin still holds (both candidates must equal the pinned digest), so the bytes used are correct. Only provenance and disclosure are lost.
- Fix: catch only git materialization failures; re-raise `SnapshotTampered`.

### F8 LOW — int/str boundary in status 9
- `status_is_9` (246-254) accepts float `9.0`. The r14 stub filter compares `str()` (`"9.0" != "9"`), so the delivered stream and the expected positive disagree for that input. jq `tostring` would accept it.
- No current pack is known to use it. Fix: accept only the string `"9"` and integer `9`, or align the stub.

### Verified clean (static)
- Expected-pin comparison covers gate, r14, frozen, fixture-pack sha, and canonical per-case expectations (862-906). Input hashes are taken at load and re-checked at end (1563-1575).
- Head uses real `git rev-parse HEAD` (786). The pinned revision is annotation only (1628-1631). Dirty accounting excludes output scope and reports `dirty_outside_harness_output` (827-829).
- Positives are derived from fixture records, not from the SUT (count_positives 473-493). `want_oom`/`want_signal` are cross-checked against derived triggers (570-580).
- Capture failures expect `unavailable:<reason>` on every positive token, never zero (551-556). Positive tokens stay unavailable on capture failure.
- MESSAGE-key rejection is recursive (236-243, 529-531). Fixtures cannot carry raw MESSAGE.
- Exit map (1675-1692) is correct except for F1 and F2.

### Recommended order
1. F1 and F2 before any exit-0 claim is relied on. F1 needs a selftest case that exercises the frozen path, using a frozen wrapper that exec-fails.
2. F3 through F5 before merge.
3. F6 through F8 as hardening.

Checks L1 should run once after integration: a normal run with a valid expected table (confirm control reproduces, not merely fails), a frozen-exec-failure case (must exit 2), the two-flag bypass (must refuse), an rc-124 pack, and an in-repo output run (confirm `stable` after F4).
