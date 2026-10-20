# ReconProtectedTeaching — Operator Lessons, Protected Files, Inherited State, and Primary Source Boundaries for C1 Positive Evidence

- **Seat:** `MoriR15.ReconProtectedTeaching` (scout, leaf)
- **Lane Root:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
- **Milestone:** Retain validated positives without fabricated totals
- **Judged on:** Coverage (lowest owned axis at 6 vs operability at 7)
- **Target Report:** `.ufo/waves/round-15/build/ReconProtectedTeaching.md` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-15/build/ReconProtectedTeaching.md`)
- **Authority / Grounding:** Sources S014, S015, S037, S038; `corpus/QUALITY.md`; `corpus/lessons/round-14-verifier-spotcheck.md`; `corpus/lessons/round-14.md`; `corpus/knowledge/journal-alarm-routing-r14.md`; `tools/mori-census.sh` (HEAD `52512ae` / `0e41cb83…`); `SKILL.md`; `/home/vgpnk/.omp/agent/RULES.md`.
- **Contract & Boundaries:** Read-only inspection; no subagent dispatch; no verification, build, test, lint, format, or smoke runs (L1-owned); zero edits to production code, fixtures, or verifier files; tools installed/updated: **none**.

---

## 1. Axes Named & Godspeed Posture

1. **coverage** (Primary Judged Axis): Advancing from 6 towards 7 by closing the inherited alarm-suppression gap: preserving critical `OOM_KILL_JOURNAL crit` and `KILL_SIGNAL_JOURNAL warn` alarms from individually valid current-boot structured records, even when an adjacent malformed, non-matching, or foreign-boot record invalidates the aggregate class.
2. **operability** (Held at 7, Harmless): Strictly preserving existing raw class tokens and unavailable semantics (`<cls>=unavailable:<reason>`). Reusing the identical successful `$raw` JSON stream without spawning extra journal queries. Refusing to crash parsers or fabricate fake numeric zeros.
3. **depth** (Held at 5, Harmless): Grounding positive evidence tokens (`positive_kernel_oom`, `positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill`) strictly in reopened Tier A primary authorities: S014 (`journalctl`), S015 (`systemd.journal-fields`), S037 (subject-unit metadata `UNIT=`/`USER_UNIT=`), and S038 (`service_result_table` in `service.c`).
4. **freshness** (Held at 5, Harmless): Preserving the legacy red drift baseline (`baseline-r10-20261015T2231Z.json`) without silent repinning; maintaining clean commit hashes and hash-pinned frozen controls.
5. **calibration** (Held at 5, Harmless): Strict boundary discipline: positive evidence tokens count ONLY valid scalar matching records; raw aggregate/split counts stay unavailable when invalid. Never claiming completeness, authenticated emitter IDs, unique victim counts, or arbitrary malformed JSON repair.
6. **adjacency** (Held at 6, Harmless): Preserving the lane province boundary: detection only, no remediation or actuation. Maintaining subject-based triage routing (`UNIT_FAILURE_JOURNAL` vs `UNIT_FAILURE_OUT_OF_SCOPE` routed to `tsukuroi`) on valid aggregate classes, without leaking into OS maintenance or sibling provinces.

---

## 2. Operator Lessons & Verifier Spot-Check Directives

### 2.1 Global Operator Directives & Host Safety

| Directive | Source / Authority | Operative Rule | Reflection & Compliance in Round 15 |
|---|---|---|---|
| **Host Safety Directive (2026-10-20)** | Parent IRC (`MoriR15`) | Sync DB ~413 packages ahead. Before any `pacman -S`, run `pacman -Sp --print-format '%n %v' <pkgs>`; proceed ONLY if EVERY package not installed (`pacman -Q` fails). Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade, or restart services. | Strictly observed. This seat is a read-only scout; zero package installations or updates were needed or performed. |
| **Tooling Directive (2026-10-19)** | `/home/vgpnk/.omp/agent/RULES.md` | Agents may install/update helpful tools without asking using passwordless `sudo`, following strict channel order (`pacman -S --needed --noconfirm` → `uv tool install` → official binary → `cargo install` / `npm -g`). Record tool, version, channel, reason. | Acknowledged. No tools installed or upgraded. Existing preinstalled bash, coreutils, jq, and git used exclusively. |
| **No-Harm Rule (RFC 2119)** | `PROTOCOL.md:120-135`, `round-13-verifier-spotcheck.md:6-8` | An improvement on one axis cannot offset harm on another axis. A cutover that sacrifices existing alarm severity, trigger conditions, or adjacent-owner routing is `rejected-harmed`. | Core driver of C1: Round 14 restored OOM alarms for clean classes, but left an inherited suppression defect on mixed streams. C1 fixes the suppression without altering raw aggregate unavailable semantics. |
| **Leaf Seat Boundaries** | `spec.json`, `dispatch.json`, AGENTS.md | Leaf members execute no delegation, no background jobs, no git commits, and skip all verification/builds/tests/lints/smoke runs. Verification is L1-owned post-integration. | Strictly observed. Only this report file is written. |

### 2.2 Integrator / Verifier Spot-Check Lessons

#### A. Round 14 Verifier Spot-Check (`corpus/lessons/round-14-verifier-spotcheck.md`)
Closure of round 14 admitted C1 at its bounded measured scope (status `ok`, admitted `true`), but identified key inherited limitations and routed defects:
1. **The Disclosed Inherited Limitation (`:98`)**:
   > "The source reviewer initially compared malformed-stream behavior with pre-r13 text matching. That is not a new B→H loss: B already invalidated the whole malformed class and lacked the OOM alarm. The reviewer withdrew the harm finding. Class-wide invalidation remains a serious, **disclosed inherited limitation**, not part of this bounded repair's guarantee."
   - *Direct C1 Relevance*: Round 15 directly tackles this exact inherited limitation. When a journal stream contains valid OOM or signal records alongside an invalid record, the alarm must not be suppressed.
2. **Routed Defect 2 — Wording Clarification (`:137`)**:
   - Qualify `corpus/knowledge/journal-alarm-routing-r14.md:221` "fail-loud on positive validated records" as **positive validated class counts**, cross-linking the mixed-malformed-class limitation at `:386-390`. A valid record inside an invalidated class was previously hidden; round 15 provides the structured evidence tokens to expose positive evidence without pretending aggregate counts are clean.
3. **Routed Defect 3 — Interface Clarity (`:138`)**:
   - Document that legacy `KILL_SIGNAL_JOURNAL` `count`/`process_sigkill` can be `unavailable:<reason>` while an independently available user-unit signal arm raises `WARN`; these are not fabricated numeric zeros. The production code preserves availability honestly.
4. **Routed Defect 4 — Carried Gate Debt (`:139`)**:
   - Old r10 drift pin (`baseline-r10-20261015T2231Z.json`) remains red at measured `5601d12`. Routed as status-neutral conformance debt; never re-pinned silently.
5. **Operator Note 6 — SHONEN Boxes Untouched (`:141`)**:
   - All four SHONEN boxes remain unchecked (`- [ ]`). Checkbox promotion is strictly operator-owned.

#### B. Round 13 Verifier Spot-Check (`corpus/lessons/round-13-verifier-spotcheck.md`)
- Closure ruled `rejected-harmed` because selector improvements silently suppressed OOM alarms and collapsed fleet vs non-fleet unit routing.
- Established that clean selector changes must prove behavioral alarm equivalence on before/after revisions (Defect 1 & Defect 2).

### 2.3 Quality Criteria Relevant to C1 (`corpus/QUALITY.md`)

- **Q6 (rc-gated pipelines)**: Crash exit code never equals a verdict code; producer failure yields `unavailable`, never a fake zero or false clean roll.
- **Q7 (no live producer pipe feeding early match)**: Capture once to variable/file before asserting; avoid SIGPIPE (141).
- **Q12 (cumulative counter baseline)**: Never read cumulative counters without baseline (current `_BOOT_ID`).
- **Q15 (structured counting)**: Journal counted by `MESSAGE_ID` or trusted structured field, never by message text.
- **Q16 (scope independence)**: Scopes are never summed; user and system scopes maintain separate counters.
- **Q29 (alarm preservation on cutover)**: Behavioral alarms keep equivalent finding ID, severity, and verdict effect.
- **Q30 (subject metadata classification)**: Classify from failed subject's own `UNIT`/`USER_UNIT`, never from emitter fields; missing/malformed subject is explicit UNKNOWN/unavailable, never non-fleet or zero.

---

## 3. Protected Non-Author Files Inventory

The following files and paths are **protected** across all non-author and leaf seats. Leaf seats have zero write privilege over them:

```
                           PROTECTED NON-AUTHOR INVENTORY
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 1. Promotion Checklist                                                           │
│    /home/vgpnk/Projects/shokunin/mori-shokunin/SHONEN.md                         │
│    All 4 checklist boxes remain unchecked (- [ ]). Leaf seats never edit boxes.  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 2. Historical Lessons & Verifier Spot-Checks                                     │
│    - corpus/lessons/round-12-verifier-spotcheck.md                               │
│    - corpus/lessons/round-13-verifier-spotcheck.md                               │
│    - corpus/lessons/round-14-verifier-spotcheck.md                               │
│    - corpus/lessons/round-12.md, round-13.md, round-14.md                        │
│    Append-only historical records; never rewritten or back-edited.               │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 3. Immutable Baselines & Frozen Fixtures                                         │
│    - corpus/evidence/baseline-r10-20261015T2231Z.json (Red drift baseline)       │
│    - .ufo/waves/round-13/frozen/mori-census.sh (SHA: 304cb223…)                 │
│    - .ufo/waves/round-14/frozen/mori-census.sh (SHA: 39abda0a…)                 │
│    - .ufo/waves/round-14/evidence/green-after-accepted/runs/*                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 4. Production Scripts & Registered Regression Gates                              │
│    - tools/mori-census.sh (Registered gate: census & drift pin)                  │
│    - tools/mori-silence-cases.sh (Registered gate: silence oracle)               │
│    - tools/mori-round13-regressions.py (Registered gate: r13 regressions)        │
│    - tools/mori-round14-regressions.py (Registered gate: r14 regressions)        │
│    (Production modifications owned strictly by designated executor seats).       │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 5. Fleet Governance & Orchestrator Level Files (Fleet root: /home/vgpnk/Projects)│
│    - MANIFEST.json, ROADMAP.md, MISSION.md, AXES.md, CORPUS.md                   │
│    - scripts/* (e.g. scripts/sources-census.sh, scripts/shokunin-watchdog.sh)   │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 6. Sibling Repositories (Province Refusal: Detection Only, Zero Bleed)           │
│    - ../tsukuroi-shokunin/ (Host OS, systemd units, packages, drivers, boot)     │
│    - ../kumitate-shokunin/ (OMP task/hub orchestration, wave lifecycle)          │
│    - ../kama-shokunin/ (Model serving, endpoint health)                          │
│    - ../kagi-shokunin/ (Secrets, credentials, vault ops)                         │
│    - ../souji-shokunin/ (Artifact cleanup)                                       │
│    - ../kimi-shokunin/ (Mint templates, protocol definitions)                    │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 7. Authentication & Host Agent Database Files (STRICTLY FORBIDDEN)               │
│    - ~/.omp/agent/agent.db* (Never opened, copied, queried, or modified)        │
│    - Credentials, OAuth tokens, session tokens (Shape only, never read)          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Inherited State Analysis: The All-or-Nothing Aggregate Trap

In `tools/mori-census.sh` (as delivered in round 14, commit `52512ae` / `0e41cb83…`), journal parsing relies on monolithic jq filters:
- `JOURNAL_JQ_TAIL` (`:973`)
- `JOURNAL_JQ_MSGID` (`:974`)
- `JOURNAL_JQ_SIGKILL` (`:975`)
- `JOURNAL_JQ_SIGSEGV` (`:976`)
- `JOURNAL_JQ_UNITS` (`:1001-1037`)

### 4.1 Root Cause of Suppression
Every aggregate filter begins with:
```jq
if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and (._BOOT_ID == $boot) and (.MESSAGE_ID == $id) ...)
```
If **even one** record in the slurped array fails this predicate (for example: a record from a previous boot `_BOOT_ID != $boot`, a non-unique field serialized as a JSON array per S014 `:598`, or a corrupted non-object token), the `all(.[]; ...)` condition evaluates to `false`.

The filter then falls back into the `else` branch of `JOURNAL_JQ_TAIL`:
```jq
else (
  if all(.[]; type == "object" and (._BOOT_ID | type) == "string" and ((._BOOT_ID | length) > 0)) then
    ([.[]._BOOT_ID] | unique | length) as $b |
    if $b > 1 then "multi-boot"
    elif all(.[]; ._BOOT_ID == $boot) then "record-invalid"
    else "boot-mismatch" end
  else "record-invalid" end
)
```
Consequently, `parsed` evaluates to `record-invalid`, `multi-boot`, or `boot-mismatch`. At lines 1103–1105:
```bash
case "$parsed" in
  record-invalid|multi-boot|boot-mismatch) JQ_STATUS=$parsed; return 0 ;;
esac
```
`JQ_STATUS` is set to the error token and returns without computing any counts.

### 4.2 Alarm Suppression in `probe_journal`
In `probe_journal` (lines 1303–1327 and 1340–1354):
```bash
# OOM alarm
if [ "${js[$key]}" = ok ]; then ko=${jn[$key]}; else ko="unavailable:${js[$key]}"; fi
case "$ko" in
  unavailable:*) ;;
  *) if [ "$ko" -gt 0 ]; then oom_fire=1; oom_path_k=1; fi ;;
esac

# User signal alarm
if [ "${js[$key]}" = ok ]; then ps=${jn[$key]}; else ps="unavailable:${js[$key]}"; fi
case "$ps" in
  unavailable:*) ;;
  *) if [ "$ps" -gt 0 ]; then kill_fire=1; kill_paths=process_sigkill; fi ;;
esac
```
Because `ko`, `uo`, `ps`, and `us` are prefixed with `unavailable:`, the `case` statement silently drops into `;;`. **Neither `oom_fire` nor `kill_fire` is asserted.**

Thus, a single malformed or foreign-boot record in the journal query completely suppresses critical host OOM alerts (`OOM_KILL_JOURNAL crit`) and user process termination alerts (`KILL_SIGNAL_JOURNAL warn`), even if valid current-boot records exist in that same stream.

---

## 5. Primary Sources Register (S014, S015, S037, S038)

All four primary authorities reopened this round are Tier A sources. Quotations are verified $\le 25$ words.

| Source ID | Canonical Reference | Exact Anchor / Locator | Located Verbatim Quote ($\le 25$ words) | Word Count | Scope Boundaries for C1 |
|---|---|---|---|---|---|
| **S014** | `journalctl(1)` man page (systemd 262) — `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html` | HTML `:209`, man `:572` (`-o json`) | *"formats entries as JSON objects, separated by newline characters"* | 9 | Establishes stream format. Each line is an independent JSON object. |
| **S014** | `journalctl(1)` man page (systemd 262) | HTML `:215`, man `:598` (non-unique fields) | *"if a non-unique field is encountered a JSON array is used as field value"* | 14 | Documents why duplicate keys produce arrays, causing naive scalar equality to fail. |
| **S014** | `journalctl(1)` man page (systemd 262) | HTML `:236`, man `:680` (`--output-fields=`) | *"the __CURSOR, __REALTIME_TIMESTAMP, __MONOTONIC_TIMESTAMP, and _BOOT_ID fields are always printed"* | 10 | Proves `_BOOT_ID` is always present in output even if omitted from requested fields. Eliminates `MESSAGE` display text. |
| **S014** | `journalctl(1)` man page (systemd 262) | HTML `:352`, man `:1107` (exit status) | *"On success, 0 is returned; otherwise, a non-zero failure code is returned."* | 12 | Exit `rc=0` means query completed; non-zero (`rc=1` permission denied) must yield `unavailable`. |
| **S015** | `systemd.journal-fields(7)` (systemd 262) — `https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html` | HTML `:33-35`, man `:32-35` (User Fields) | *"User fields are fields that are directly passed from clients and stored in the journal."* | 13 | Proves `MESSAGE_ID` is client-supplied, not kernel-trusted. Records are operational evidence, not authentication. |
| **S015** | `systemd.journal-fields(7)` (systemd 262) | HTML `:83-84`, man `:80-84` (Trusted Fields) | *"Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code."* | 24 | Proves `_BOOT_ID` cannot be spoofed by unprivileged clients. Validating `_BOOT_ID == $boot` anchors current-boot relevance. |
| **S015** | `systemd.journal-fields(7)` (systemd 262) | HTML `:37-39`, man `:36-39` (`MESSAGE=`) | *"is not supposed to be parsed for metadata."* | 8 | Grounds strict refusal to parse `MESSAGE` display strings for OOM or signal detection. |
| **S037** | `systemd.journal-fields(7)` subject metadata — same URL | User Journal Fields → `UNIT=, USER_UNIT=` | *"Used by the system and user managers when logging about specific units."* | 12 | Identifies the failed *subject* unit. Contrast with `_SYSTEMD_UNIT` (emitting process). Subject validity does not gate OOM result. |
| **S038** | `src/core/service.c` result table — commit `cf8ebfc6` `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/service.c` | Line 6598 (`service_result_table`) | `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` | 4 | Authoritative vocabulary string for service OOM failure. Grounds exact string matching for `positive_unit_oom`. |
| **S038** | `src/core/service.c` result table | Line 6593 (`service_result_table`) | `[SERVICE_FAILURE_SIGNAL] = "signal",` | 4 | Authoritative vocabulary string for service signal termination. Grounds exact string matching for `positive_unit_signal`. |

---

## 6. Concrete Counterexamples for C1

The following five counterexamples demonstrate the exact failure modes that C1 addresses and the boundaries it enforces:

### CX1: Suppressed OOM Alarm on Mixed Stream (The Baseline Defect)
- **Scenario**: System journal query for kernel OOM notices (`fe6faa94e7774663a0da52717891d8ef`) returns two records:
  1. Record A: Valid current-boot record (`_BOOT_ID="1111..."`, scalar `MESSAGE_ID="fe6faa94..."`).
  2. Record B: Non-matching or malformed record (e.g. duplicate field yielding `MESSAGE_ID=["fe6faa94...", "extra"]`, or foreign-boot `_BOOT_ID="2222..."`).
- **Round 14 Behavior**: `JOURNAL_JQ_MSGID` evaluates to `record-invalid` (or `multi-boot`). In `probe_journal`, `ko="unavailable:record-invalid"`. The OOM alarm check `case "$ko" in unavailable:*) ;;` suppresses `OOM_KILL_JOURNAL crit`. Host is silent despite an actual OOM kill occurring.
- **Round 15 Required Behavior**:
  - Raw aggregate counter on `SURFACE journal.system` remains: `kernel_oom_notice=unavailable:record-invalid`.
  - Positive evidence pass over the same stream finds Record A: `positive_kernel_oom=1`.
  - `OOM_KILL_JOURNAL crit` fires with `alarm=1 paths=kernel_oom_notice ... system_positive_kernel_oom=1`.

### CX2: Fabricated Zero Total on Capture or Parser Failure (The Fabrication Trap)
- **Scenario**: Querying `--system` as an unprivileged user returns exit code `rc=1` (permission denied), or `jq` encounters truncated invalid JSON (`malformed-json`).
- **Flawed Implementation**: An overzealous selector treats the failure as "found 0 matching positive records", emitting `positive_kernel_oom=0` and claiming clean liveness.
- **Operator Directive Violation**: Violates QUALITY 6 / 24 and the Milestone directive ("Positive fields unavailable on capture/parser failure; unsafe/nonmatching records excluded, never interpreted as numeric-zero total").
- **Round 15 Required Behavior**: On capture failure (`CAP_RC != 0`, `timeout`, `stderr-nonempty`) or parser crash (`malformed-json`), positive evidence tokens MUST be `unavailable:<reason>` (e.g. `positive_kernel_oom=unavailable:rc-1` or `positive_kernel_oom=unavailable:malformed-json`). Never a fabricated numeric zero.

### CX3: Leaking Malformed Records into Aggregate Counters (The Parity Trap)
- **Scenario**: An implementation attempts to solve CX1 by changing the aggregate filter `all(.[]; ...)` to count only valid records, omitting the malformed ones from the total.
- **Flawed Implementation**: The `SURFACE journal.system` line emits `kernel_oom_notice=1`.
- **Operator Directive Violation**: Violates the Round 15 contract ("Existing raw aggregate/split counts STAY unavailable when invalid") and breaks regression gate `R14_SCOPED_PARITY`.
- **Round 15 Required Behavior**: The raw aggregate count MUST remain `unavailable:record-invalid`. The positive count lives in its dedicated token `positive_kernel_oom=1`. The aggregate surface is protected against false claims of whole-class integrity.

### CX4: User Signal-Result Warning Suppressed by Foreign Boot
- **Scenario**: User journal contains 1 valid current-boot unit failure record with `UNIT_RESULT="signal"` (`d9b373ed...`), alongside 1 record from a previous boot (`_BOOT_ID="9999..."`).
- **Round 14 Behavior**: Class evaluates to `multi-boot`. `ucnt["user:signal"]` evaluates to `unavailable:multi-boot`. The user signal warning `KILL_SIGNAL_JOURNAL warn` is suppressed.
- **Round 15 Required Behavior**: Raw aggregate `unit_failure_record=unavailable:multi-boot`. Positive evidence `positive_unit_signal=1`. `KILL_SIGNAL_JOURNAL warn` fires with `paths=unit_result_signal user_unit_signal=1`.

### CX5: Falsely Claiming Kernel Victim Attribution or Unique Victims
- **Scenario**: Documentation or finding fields claim "5 kernel OOM kills" based on 5 `fe6faa94...` notices.
- **Operator Directive Violation**: Violates QUALITY 16 and `round-14-verifier-spotcheck.md:8` ("This does not admit exhaustive old-MESSAGE equivalence, authenticated membership, unique-victim counts, positive-load live behavior or comprehensive OOM coverage").
- **Round 15 Required Behavior**: Finding notes must explicitly maintain that `fe6faa94...` and `d9b373ed...` records are systemd unit notices and unit failure results, not unique victim counts or authenticated fleet kills.

---

## 7. Scope Boundaries & Interface Contracts for C1

### 7.1 Positive Evidence Tokens Specification
Four positive evidence tokens are added per scope (`user` and `system`):
1. `positive_kernel_oom`: Counts records matching:
   - `type == "object"`
   - `(._BOOT_ID | type) == "string"` and `._BOOT_ID == $boot`
   - `(.MESSAGE_ID | type) == "string"` and `.MESSAGE_ID == "fe6faa94e7774663a0da52717891d8ef"`
2. `positive_unit_oom`: Counts records matching:
   - `type == "object"`
   - `(._BOOT_ID | type) == "string"` and `._BOOT_ID == $boot`
   - `(.MESSAGE_ID | type) == "string"` and `.MESSAGE_ID == "d9b373ed55a64feb8242e02dbe79a49c"`
   - `(.UNIT_RESULT | type) == "string"` and `.UNIT_RESULT == "oom-kill"`
   *(Subject unit metadata `UNIT`/`USER_UNIT` is NOT inspected for positive OOM)*.
3. `positive_unit_signal`: Counts records matching:
   - `type == "object"`
   - `(._BOOT_ID | type) == "string"` and `._BOOT_ID == $boot`
   - `(.MESSAGE_ID | type) == "string"` and `.MESSAGE_ID == "d9b373ed55a64feb8242e02dbe79a49c"`
   - `(.UNIT_RESULT | type) == "string"` and `.UNIT_RESULT == "signal"`
4. `positive_process_sigkill`: Counts records matching:
   - `type == "object"`
   - `(._BOOT_ID | type) == "string"` and `._BOOT_ID == $boot`
   - `(.MESSAGE_ID | type) == "string"` and `.MESSAGE_ID == "98e322203f7a4ed290d09fe03c09fe15"`
   - `(.EXIT_CODE | type) == "string"` and `.EXIT_CODE == "killed"`
   - `((.EXIT_STATUS | type) | IN("string","number"))` and `((.EXIT_STATUS | tostring) == "9")`

### 7.2 Single-Stream Reuse Contract
- **No extra `journalctl` invocations**: Both the aggregate pass and the positive evidence pass MUST operate on the identical `$raw` stream captured in `CAP_OUT`.
- Positive evidence pass is executed immediately after `jrc == 0` (valid JSON check), using jq over `$raw`.

### 7.3 Availability & Error Propagation Contract
- If capture fails (`CAP_RC != 0`, `timeout`, `stderr-nonempty`): positive tokens = `unavailable:<reason>`.
- If JSON parser fails (`malformed-json`): positive tokens = `unavailable:malformed-json`.
- If JSON is valid, positive tokens are non-negative integers ($\ge 0$).
- If positive tokens are 0 and aggregate is `unavailable:<reason>`, the surface reports `unavailable:<reason>`.

### 7.4 Alarm Triggering Contract
- `OOM_KILL_JOURNAL crit` fires if:
  `user_positive_kernel_oom > 0` OR `system_positive_kernel_oom > 0` OR `user_positive_unit_oom > 0` OR `system_positive_unit_oom > 0`.
- `KILL_SIGNAL_JOURNAL warn` (user scope only) fires if:
  `user_positive_process_sigkill > 0` OR `user_positive_unit_signal > 0`.
- The existing finding fields preserve raw counts and add positive evidence fields; no new finding IDs or route names are introduced.

### 7.5 Aggregate Routing Boundary
- Fleet vs non-fleet vs unattributed triage (`UNIT_FAILURE_JOURNAL` vs `UNIT_FAILURE_OUT_OF_SCOPE`) applies **strictly to valid aggregate classes**.
- If a unit failure class is invalid, subject routing remains `unavailable:aggregate-invalid`. Positive evidence only triggers the OOM/signal alarm; it does not fabricate partial subject routes.

---

## 8. Unresolved Facts & Instructions for L1

1. **Delivered Gate Selftest Verification**: SKILL.md cites selftest tallies from earlier revisions (`104/104 at 8d22d18`, `20 checks at 5601d12`). L1 must run `--selftest` across all registered gates on the final delivered commit bytes and record the exact receipts.
2. **Finding Field Tolerances in r13/r14 Gates**: Adding new positive evidence tokens to finding detail strings must be verified by L1 to ensure `tools/mori-round13-regressions.py` and `tools/mori-round14-regressions.py` do not fail on unexpected key additions.
3. **Old Drift Baseline Carried Debt**: Baseline `corpus/evidence/baseline-r10-20261015T2231Z.json` remains red (status-neutral conformance debt). L1 must ensure no silent re-pin occurs during round 15.
4. **SHONEN Checklist Integrity**: All four SHONEN promotion boxes remain `- [ ]`. No lane agent may check these boxes.
5. **Tooling Record**: Zero tools installed or updated. Compliant with 2026-10-19 directive and 2026-10-20 parent host-safety rule.
