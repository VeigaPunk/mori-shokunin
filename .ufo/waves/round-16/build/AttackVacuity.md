# AttackVacuity — round 16 C1 (empty fixtures, digest pinning, no-op fake-green)

Role: critic, report-only. Read time: 2026-10-20T05:49–05:52-03:00. Inputs were still in flight.
At read time:
- 13 of 16 packs had landed. `Bounds`, `MalformedCapture` and `Stderr` were absent.
- `tools/mori-journal-window.py` and `tools/mori-round16-regressions.py` did not exist.
- Harness findings therefore attack the **contract** (wave1-spec context and the WindowHarness/WindowTool prompts) and the landed pack bytes, not harness code.

## Disclosure (per L1 clarification)
- No live journalctl, no SUT or harness execution, no tests, gates or builds, no installs, no /tmp output, no write outside this file.
- Reading aid: I loaded the landed fixture JSON read-only into my own eval kernel. I tallied `want` keys and compared each case's declared rc against a hand-written reading of the contract. This is static data analysis, **not verification**, and is inadmissible as evidence that any tool behaves a given way.
- Deviation: I started one `sleep 90; ls` wait. It auto-backgrounded as bg_2749, did no reads beyond `ls`, and I cancelled it as soon as the L1 "no background jobs" clarification arrived. Disclosed to MoriR16.Lesson.

## Axes
- Discrimination: does a wrong tool go red?
- Contract coverage: is each MUST asserted by at least one case?
- Pin integrity: does the pin bind what was reviewed?
- Provenance honesty: are before/after claims true?

## Read-time pack digests (independent reference for pin cross-check)
```
d41bf9577ff45d8f84221ecd3acaa391828d3233a1671168b0dd88223e9081b2  AnchorValidation.json
af6ed035d4bde0db6b8ad0fc8247f978061ea4fbc3749095ad5a4905a1f5a848  BootBoundary.json
b29a4a1d5820783f7519bf44a2f54b99b13765e9d80a3b6196ddb9b76c8436c6  CursorShape.json
193dc63cdc8334da067ba23792826c8ff42be38a86a8e2610f852ecf24b7cbd3  ExactAnchor.json
a12bc349c010b053e7e7360ec12f9dd8d7921c2e0849e128547d1c5648b73222  KernelSystem.json
a0db2726d3a04429f9d7e5ef25429d15f7af39d2c77881fa87023941a62851be  KernelUser.json
fca571e28ceeb7acf25afea9540b375fa2a071f5bb57e3f66e196cd51c1a7646  MissingAnchor.json
af911e7404bc7078977265a502a83be094cd249951133ae3e2855064a9f2f8c2  ProcessSignal.json
ffc9c0cccb77886d5bfe64fe76fa6f2ef177949c3718205f06950aa110d970fb  ProducerFailure.json
9764c4277412e2a5caec32f6f8225da2289a40dda9e53f2661dce5d252090594  RecordShape.json
f827bffef9328ae1584a34cb074b52f14a67161a6f3f1d9024c4e513495be001  TypedFields.json
b333347a8cf93207fcd21bc753ac0a62f779abc3b3d9dd90fd7b15c380ce0665  UnitOom.json
6c08238a05ae774d820f8961893231c55d02af40685aa1b46cd73af0aaf175d1  UnitSignal.json
```
These are SHA-256 values I captured with `sha256sum` at 2026-10-20T05:52:28-03:00. If a pin carries different bytes, the pack changed after this read: re-review it, don't just re-pin.

## V1 (HIGH) — no unavailable case asserts the "no numeric positive totals" MUST or a reason
- **Counterexample (salvage mutant).** On any refusal, the tool emits `{"finding_id":"MORI_JOURNAL_WINDOW_UNAVAILABLE","positive_kernel_oom":1,…}` with rc 2. It passes **all 20/20** landed UNAVAILABLE cases.
- **Evidence:**
  - `want` is `null` in MissingAnchor (4), RecordShape (4) and KernelSystem `kernsys_oom_foreign_boot_after_anchor_refuses`.
  - `want` is `{}` in CursorShape (4), BootBoundary (3) and ProducerFailure (4).
  - Zero cases pin `reason`. Zero cases can express absence: a subset `want` cannot say "key must not exist".
  - The traps are built and then disarmed:
    - `MissingAnchor/anchor_vacuumed_positive_trap` carries a kernel-OOM record after a non-anchor first cursor.
    - `CursorShape/…-later-cursor-array` and `…-duplicate` carry `fe6faa94…` before the bad cursor.
    - ProducerFailure `*-positive-stream` carries a positive under rc 5, 124 and 137.
  - The pack authors flagged this themselves (PackCursorShape.md:35, PackMissingAnchor.md:60).
- **Smallest correction:**
  - (a) The harness enforces a global rule, independent of fixtures: when `want_id` is UNAVAILABLE or SETUP, the stdout object MUST NOT contain any `positive_*`, `records_after_anchor` or `evidence_basis` key.
  - (b) L1 publishes a closed reason vocabulary. Every rc2 case pins `want.reason`. Candidates seen in peer reports: `anchor-not-first-record` (Knowledge.md:7), `anchor-missing` (ReviewCLI F4), distinct timeout and overflow (ReviewCapture C-3, item 8).
  - Without (b), the topic packs cannot tell their refusal apart from an unrelated one.

## V2 (HIGH) — whole packs are green under an always-UNAVAILABLE no-op
- **Counterexample.** `print('{"finding_id":"MORI_JOURNAL_WINDOW_UNAVAILABLE"}'); sys.exit(2)` passes these packs in full:
  - CursorShape 4/4
  - MissingAnchor 4/4
  - RecordShape 4/4
  - ProducerFailure 4/4
  - BootBoundary 3/4
  - KernelSystem 1/4
- The full gate still goes red, but only because *other* packs carry rc0 cases. Each of those packs alone proves nothing about its topic.
- Two packs already show the right pattern:
  - BootBoundary pairs its refusals with `same_boot_boundary_ok` (rc0).
  - AnchorValidation pairs its SETUP refusals with `ANCHORVAL_VALID_NEGATIVE_CONTROL`.
- **Counterexample (attribution).** `RecordShape/recordshape-leading-string-primitive-user` refuses because the first record is not the anchor (anchor-not-first), not because of record shape. A tool with no record-shape check still refuses it.
- **Smallest correction:**
  - The harness requires every pack to have at least one rc0 case and at least one rc2 case.
  - Each refusal gets a twin: identical stdout, stderr and rc except the single topic defect, expected rc0 with exact counts.
  - CursorShape, MissingAnchor, RecordShape and ProducerFailure each need one twin. For ProducerFailure, that is `positive-stream` with `returncode:0`.

## V3 (HIGH) — the per-case wrapper ignores argv, so the query contract is untested
- Wrappers replay fixed stdout whatever the argv. Under the landed schema, every one of these mutants is fully green:
  - the tool requests `MESSAGE` in `--output-fields`;
  - it uses `--after-cursor`;
  - it omits `--cursor=<anchor>`;
  - it queries `--system` for `--scope user`;
  - it shells out to PATH `journalctl`, which is a **live read**.
- **Scope-swap exposure.** Only 13/29 rc0 cases pin `want.scope`. ExactAnchor, KernelUser, UnitSignal and BootBoundary pin none.
- **Smallest correction.** Each wrapper appends its argv, NUL-separated, to a log under `--output`. The harness asserts:
  - exactly one invocation for non-SETUP cases, and zero for SETUP cases;
  - the scope flag matches the case;
  - `--cursor=` equals the anchor cursor;
  - `--output-fields=` equals the exact six-field string, and no `MESSAGE`;
  - no `--after-cursor`;
  - `--no-tail --quiet --output=json` are present.
- In addition, prepend a PATH directory whose `journalctl` is a tripwire that must stay unexecuted. r15 already had a PATH tripwire (`mori-round15-regressions.py:42-43`); keep it.

## V4 (MEDIUM) — `want: null` versus `want: {}` split the schema
- Nine cases use `null` and eleven rc2 cases use `{}`.
- A strict loader rejects MissingAnchor, RecordShape and KernelSystem as rc2 setup, so those packs never run.
- A lax loader treats null as "no assertion", which makes the vacuity in V1 permanent.
- **Correction:** `want` is a required object. Reject unknown case keys, so a typo like `timout`/`overfow` cannot silently turn a bounds case into a plain one.

## V5 (HIGH) — empty and absent coverage reads green
- **Counterexample 1.** `{"cases":[]}`, or a fixtures dir missing some packs. "rc0 all cases match" is `all([])`, which is True. At read time Bounds, MalformedCapture and Stderr were missing. A harness that globs `*.json` would gate green with **zero** timeout, overflow, stderr or malformed-JSON coverage.
- r15 rejected empty packs (`:691-692`); the r16 shared schema is new and has no such guard.
- **Correction:**
  - Hard-code the 16 assigned pack names from wave1-spec.
  - Refuse missing or extra packs and refuse `cases` lists shorter than 2 (the assignment said 2–4).
  - Require globally unique case ids, because wrapper directories are keyed by id.
  - Pin the case-id list per pack.

## V6 (HIGH) — the digest pin is self-referential, and the tool pin contradicts the baseline
- **Self-blessing.** `--pin-fixtures` hashes whatever bytes exist and writes them; the normal run then checks current == pin. That detects movement *between* pin and run, nothing else. Whoever re-pins blesses any tampered or emptied pack.
  - **Correction:** L1 records the pin file's own SHA-256 in its round record, outside the harness. L1 cross-checks the pin against seat-reported pack digests and the read-time table above (r15 AttackProvenance did this for pack seats). Any re-pin is logged as an event, mirroring "old drift pin remains red, no re-pin".
- **The harness does not pin itself.** The spec pins "every pack digest and tool digest" but not the harness bytes. r15 pinned `gate_sha256` (`:899-905`).
  - Counterexample: loosen `compare()` to return True. Every pin still validates.
  - **Correction:** pin the harness SHA-256 too, and let L1 record it externally, because a self-check alone is circular.
- **Tool digest versus the missing-tool baseline.** "Validate every pack digest and tool digest before runs" contradicts "missing tool at entering baseline records capability_absent".
  - Either the baseline run has no bytes to validate (and is refused as tamper, rc2), or the pin must be regenerated once the tool exists. In the second case the pin binds whatever tool L1 chooses, which is circular.
  - **Correction:** split the pin. `inputs` (packs, harness, reason vocabulary) is pinned once. `tool_sha256` is recorded per run at start and end, with explicit `absent` for the baseline, and enforced only as a moving-input check.

## V7 (MEDIUM, provenance) — capability_absent red is non-discriminating
- With no tool, 100% of cases fail by construction. "Red before, green after" has zero power to show that any case catches any defect.
- Reporting it as "bug reproduced" or "regression fixed" would be false provenance. The honest label is "capability added".
- Discrimination has to come from mutants. Mutant scripts must be test-only, created by the harness `--selftest` in an isolated temp tree, and executed only by L1. These arms must each go red on at least one case **per pack topic** they target:
  - M_unavail: always UNAVAILABLE.
  - M_setup: always SETUP.
  - M_okzero: counts records, zero positives. It passes ExactAnchor 4/4, TypedFields 3/4, KernelUser 2/4, UnitOom 2/4, UnitSignal 2/4, ProcessSignal 1/4 and KernelSystem 1/4, so it is caught only by the positive cases.
  - M_salvage (V1).
  - M_no_anchor_drop: KernelUser `kernuser_oom_before_anchor_only` catches it. Keep that case.
  - M_skip_anchor_compare: MissingAnchor `nearest_cursor_not_anchor` catches it.
  - M_scope_swap and M_message_field (V3).
  - M_bool_counts (V8).
- An rc+id-only selftest (the WindowTool and WindowHarness prompts) passes M_salvage, M_okzero on benign cases, and M_bool_counts.

## V8 (MEDIUM) — Python equality makes typed assertions fake-green
- **Counterexample.** The tool prints `"positive_process_sigkill": true`.
  - `True == 1` in Python, so `typedfields_bool_status_mixed_valid` (want 1) passes.
  - `false`, and `0.0` where an int is wanted, pass any `0` want.
  - `1.0` passes a want of 1.
- Duplicate keys: `{"finding_id":"…UNAVAILABLE",…,"finding_id":"…OK"}` parses as OK under `json.loads`. NaN and Infinity are accepted by default.
- **Correction:**
  - Compare with `type(a) is type(b) and a == b`.
  - Parse with `object_pairs_hook` rejecting duplicate keys and `parse_constant` rejecting NaN.
  - stdout must be exactly one JSON object followed by an optional newline.
  - A key missing from the output is a mismatch, never `None == None`.
  - An unparseable tool stdout is **rc1 mismatch**, not rc2 setup. Otherwise a no-op that prints nothing gets read as "harness could not evaluate".

## V9 (LOW) — subset runs and harness-side timeout
- r15 lets `--case` subsets run as a normal gate (`:1538-1547`). In r16, a subset run must never emit gate rc0. Label it diagnostic and use a distinct rc or verdict.
- If the harness-side per-case timeout kills the tool, that case is a mismatch.
- Timeout and overflow cases must:
  - pass an explicit small `--timeout` / `--max-bytes`;
  - make the wrapper exceed it by a wide margin;
  - have an under-bound twin expecting rc0 (V2).
- The fixture schema does not say which stream `overflow:true` floods. WindowTool must bound **both** streams, so add `overflow_stream: stdout|stderr` or one case per stream.

## Fixable versus tradeoff
- V1–V6 and V8–V9 are fixable before L1 runs: harness rules plus one twin case per refusal pack.
- One item is a true tradeoff for the judge. Without a pre-existing implementation there is no red control. A mutant kill-matrix is the only discrimination evidence, and it proves only the mutants that were enumerated. Any coverage claim must say exactly that.

## Impacted axes
- C1 coverage: refusal packs currently prove rc+id only.
- Operability: argv contract and live-read tripwire.
- Provenance: self-pin, capability_absent delta.
- No-harm: the "no positive totals on unavailable" MUST is unasserted.
