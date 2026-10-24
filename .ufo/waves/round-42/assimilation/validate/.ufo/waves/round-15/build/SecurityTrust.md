# SecurityTrust: client-supplied IDs, `_BOOT_ID` trust, authentication claims (r15 C1)

Seat `MoriR15.SecurityTrust`. Leaf, read-only. Axis: **coverage**. Milestone: retain validated positives without fabricated totals.

Inspected:
- `tools/mori-census.sh` at snapshot `#DC7D`, lines 211-329, 399-416 and 889-1389.
- r14 stub `tools/mori-round14-regressions.py:404-555, 669-697`.
- `SKILL.md:17,30-31,85-88`, `corpus/knowledge/journal-alarm-routing-r14.md:25-29,96-106,221-237,269-271` and `corpus/knowledge/structured-journal-scopes-r13.md:17-32`.
- Round-15 fixture packs `ForeignBoot.json` and `NegativeInvalid.json`, and the outline of `BootArray.json`.
- Local `journald.conf(5)` (systemd 261.2): `SplitMode=`, `Storage=` and `RateLimitBurst=`.

I ran no census, gate, journal query or probe. I did not read any host config or auth material, and I installed nothing.

**State of the target.** The r15 positive interface had **not landed** when I checked: grep for `positive_` in `tools/mori-census.sh` found nothing, twice. So the findings below cover two things: the current code paths the positive feature will reuse, and the contract in `spec.json:3`. Every anchor refers to `#DC7D`.

## Findings

### F1: Positive tokens can be forged by any writer to the queried journal. `_BOOT_ID` validation does not bind the emitter. (Medium; inherent; not a regression)

- **Exploit path, user scope.** Any process running as the same uid sends one entry with `MESSAGE_ID=fe6faa94…` through `logger`, `systemd-cat` or `sd_journal_send`. Other forgeable entries:
  - `MESSAGE_ID=d9b373ed… UNIT_RESULT=oom-kill` (also fires the OOM alarm);
  - `MESSAGE_ID=98e32220… EXIT_CODE=killed EXIT_STATUS=9` (fires the user WARN);
  - `MESSAGE_ID=d9b373ed… UNIT_RESULT=signal` (fires the user WARN).

  journald stamps the forged entry with the real current `_BOOT_ID`. The scalar-boot check therefore passes by construction. The record becomes `positive_kernel_oom ≥ 1`, which produces `OOM_KILL_JOURNAL crit` and DRIFT.
- **Exploit path, system scope.** According to `journald.conf(5)` `SplitMode=`, "system users will log to the system journal". The page also says "If journals are stored on volatile storage … only a single journal file is used", and `SplitMode=none` stores all messages in the system journal. So:
  - any daemon running under a system uid can always forge a system-scope positive;
  - with volatile storage or `SplitMode=none`, any local user can.
- **Evidence.**
  - The filters check only client fields plus `_BOOT_ID` (`:974-976`, `:1019`). Output fields are `_BOOT_ID,MESSAGE_ID[,…]` only (`:1194-1219`), so no emitter field (`_PID`, `_UID`, `_TRANSPORT`) is ever evaluated.
  - S015 says user fields are "directly passed from clients" (`structured-journal-scopes-r13.md:17`).
- **No new surface.** r14 already fired on a single forged valid record whenever the class aggregate was otherwise clean (`:1314-1321`, `:1344-1351`). The positive path counts the same predicate per record.
- **Impact.** A forged crit or warn is a false DRIFT, which costs alert fatigue. There is no actuation route: the spec allows no new route, and `SKILL.md:17` forbids remediation.
- **Smallest remediation, this round.** Keep `trust=client-supplied` on every line that carries a positive token (see F4). The positive tokens must not be described as "verified" or "authenticated" anywhere.
- **Frontier (not this round).** Request `_PID,_UID` in the same query and report an `emitter_bound=N` counter: system scope `_UID=0 _PID=1`; user scope `_PID` equal to the user manager's MainPID. Underscore fields "cannot be altered by client code" (S015, `journal-alarm-routing-r14.md:103-104`). This is emitter binding, not authentication. A same-uid process that ptraces the user manager still defeats it [INFERENCE].

### F2: Suppression by injection, which r15 closes only for the alarm; flood and stderr suppression remain. (Medium; partially remediated by design)

- **Exploit path today.** Every filter uses `if all(.[]; …)` (`:974-976`, `:1019`). One record in the class stream that fails the predicate turns the whole class into `record-invalid`, `boot-mismatch` or `multi-boot` (`:973`, `:1037`). The alarm then cannot fire (`:1314-1321`).

  A same-uid writer can create such a record by sending `MESSAGE_ID` twice. S014 says "if a non-unique field is encountered a JSON array is used as field value" (`JournalKnowledge.md` S014 `:215`). That single injected record silences a genuine kernel-OOM crit [INFERENCE: journalctl returns a multi-valued entry when one of its values matches].
- **r15 effect.** If the positive selector is evaluated **per record and in both branches** of the filter, a genuine scalar record still fires the alarm. Contract: "OOM fires once if ANY independently valid positive OOM record exists".
- **Residual suppressions (positives are unavailable by contract, so no alarm):**
  - **Timeout flood.** `JOURNAL_TIMEOUT_S` defaults to 2 seconds (`:316`), and rc 124/137 grades the class `timeout` (`:1086`). Matching forged records all count toward that bound. The rate limit is per service, 10000 messages per 30 s times a log2 disk factor (`journald.conf(5)`), so a writer spread over several units can reach the volume within minutes [INFERENCE].
  - **Producer stderr or rc failure.** Any stderr byte gives `stderr-nonempty` (`:1091-1094`); a nonzero rc gives `rc-N` (`:1083-1089`).

  These cases fail visible: the surface row reads `unavailable:<reason>`. But per `round-4/report-draft.md:113`, unavailable never flips DRIFT, so the crit turns into a CLEAN verdict.
- **Remediation.** Make no claim that r15 "preserves alarms" against adversarial writers. Document that capture-failure suppression is the residual. The fixture and report language should state that the mixed-record cases close accidental or single-record poisoning only.

### F3: The boot anchor trusts the environment; a stale or pinned `MORI_BOOT_ID` turns real alarms into `positive_*=0`. (Low-Medium)

- **Exploit or failure path.**
  - `BOOT_ID_EXPECTED=${MORI_BOOT_ID:-}` takes precedence over `/proc/sys/kernel/random/boot_id` and is only shape-checked (`:321-329`).
  - `journalctl -b` selects the **kernel's** current boot regardless (`:1072`).
  - So if the env anchor differs from the real boot (for example an `Environment=` value surviving a reboot, or a copied fixture env), every genuine current-boot record is "foreign":
    - the raw aggregate becomes `unavailable:boot-mismatch`;
    - under the r15 contract ("unsafe/nonmatching records excluded"), each positive token prints a **numeric `0`**;
    - neither the OOM crit nor the user WARN fires.
- **Why this matters for r15.** With an unmodified journald, foreign, array or missing `_BOOT_ID` records cannot appear in real `journalctl -b` output: `_BOOT_ID` is journald-stamped and single-valued, and `-b` adds a `_BOOT_ID=` match. The `ForeignBoot.json` "valid current-boot + foreign-boot" mix therefore corresponds live to anchor drift, a non-default store, or tampering [INFERENCE]. In the anchor-drift case, all records are foreign, not one adjacent record. Those fixtures are parser-robustness tests, not live-threat coverage.
- **Evidence.** No production launcher sets `MORI_BOOT_ID`. Only the selftest sets it (`:2712`, `:3251`), as do the r13 and r14 harnesses (`mori-round14-regressions.py:670-671`).
- **Smallest remediation.**
  - Add a `boot_source=env|file` token to both journal rows and to the OOM and KILL lines.
  - When the anchor comes from env and `MORI_FIXTURE` is unset, compare it to `BOOT_ID_FILE`. On disagreement, take the existing invalid-anchor path (`:1180-1184`, `boot_id=unavailable`) so the positive tokens read `unavailable`, never `0`.
  - Alternatively, when the class status is `boot-mismatch` or `multi-boot` and zero current-boot records survived, emit the positive tokens as `unavailable:<status>` rather than `0`.

### F4: Missing `trust=client-supplied` on the WARN line that will carry positive evidence. (Low; authentication-by-omission)

- **Evidence.**
  - Lines that have the token: `OOM_KILL_JOURNAL` (`:1331`), the notice findings (`:1252`) and the surface rows (`:1170-1182`, `:1384`).
  - Lines that lack it:
    - `KILL_SIGNAL_JOURNAL warn` (`:1353`);
    - `unit_sigkill_record` system (`:1250`);
    - `segfault_signal11` (`:1248`);
    - all `UNIT_FAILURE_*` lines (`:1272-1288`).
  - Every one of those lines is decided by client fields (`EXIT_CODE`, `EXIT_STATUS`, `UNIT_RESULT`, `COREDUMP_SIGNAL`, `UNIT`/`USER_UNIT`).
  - `emit_finding` lines are the reusable observations (`:399-410`). The `SKILL.md:30` disclaimer is not carried on the line.
- **Impact.** r15 adds `positive_unit_signal` and `positive_process_sigkill` to the KILL line. A line saying "validated positive" with no trust marker reads as an authenticated SIGKILL.
- **Remediation.**
  - Add `trust=client-supplied` to `KILL_SIGNAL_JOURNAL` (and to the other four lines listed above, if the owner accepts the drift-key change).
  - On both alarm lines, describe positives as shape-plus-boot checked. Example token: `positive_basis=scalar-id+current-boot`. Never use bare `validated`, `verified` or `authenticated`.

### F5: Basis and count labels are wrong when an alarm fires from positives alone. (Low; adjacent to "fabricated totals")

- **Evidence.** `OOM_KILL_JOURNAL … basis=scoped-record-count` (`:1331`) and `KILL_SIGNAL_JOURNAL … count=$ps … basis=scoped-record-count` (`:1353`).
- **Failure mode.** Under r15 the line can fire while `ps` or `ko` is `unavailable:record-invalid`. The line would then print `count=unavailable:record-invalid` next to `basis=scoped-record-count`, which claims a basis that does not exist.
- **Remediation.**
  - Keep `count=` raw (contract).
  - Add per-path positive tokens.
  - Set the basis per firing path, for example `basis=positive-record` when the firing path's raw class is unavailable. Never sum positives into `count=`.

### F6: Output-injection and fail-closed guard for the new jq output. (Info; implementation constraint)

- **Current guard.**
  - The else-branch emits only fixed words (`:973`, `:1037`), whitelisted at `:1103-1105`.
  - The ok-branch vector is exact-width and `is_int`-checked (`:1111-1120`).
  - The boot is checked as 32 lowercase hex (`:1131-1134`).
- **Constraints for the new positive vector.**
  - Emit it as integers in **both** branches, with the status as a fixed word in column 0.
  - Parse it with the same exact-width and `is_int` checks.
  - Never let a record-derived string through. `.UNIT`, `.USER_UNIT` and `.UNIT_RESULT` are attacker-controlled (`:998-999`).
- **What happens otherwise.** If the implementation emits `record-invalid<TAB>N…`, the exact-word `case` at `:1103` no longer matches and the row falls through to `malformed-json` (`:1112`). That fails safe but silently drops every positive.
- **Predicates.** They must guard `type == "object"` before field access. Scalarity is already implied by `== $id` and `== $boot` against `--arg` strings, and `(.EXIT_STATUS|tostring)=="9"` rejects arrays (`:975`).

### F7: Fixture fidelity for the trust cases. (Info; peers partly cover this)

- **Array `MESSAGE_ID`.** In `honor` mode the r14 stub drops records whose `MESSAGE_ID` is an array (`str(rec.get(k)) != v`, `:523`). Real journalctl would return them [INFERENCE, F2]. So the duplicate-field poisoning vector is only exercised under `dup-kernel` or `ignore-filters`. PackKernelSystem.md:59-104 and PackProcessUser.md:45-78 already raise mode selection.
- **`-b` ignored.** The stub ignores `-b` (`:450`), so foreign, missing and array `_BOOT_ID` records (`ForeignBoot.json`, `NegativeInvalid.json:39-71`, `BootArray.json`) reach the parser in a way real `-b` output cannot (F3).
- **Remediation.** In reports and SKILL text, label these cases as parser robustness. They must not be cited as live-attack or completeness coverage.

### F8: Binaries are resolved from the environment. (Info; unchanged)

`MORI_JOURNALCTL_BIN`, `MORI_JQ_BIN` and `MORI_TIMEOUT_BIN` (`:296-299`) decide every positive token, so a substituted jq can fabricate positives. The trust boundary is the same as the invoker's. No change is needed for r15; just do not present the positives as stronger evidence than the invoker env.

## What holds (verified by reading)

- No query requests `MESSAGE`. The only journal-derived string echoed is the 32-hex boot (`:1128-1134`). Unit and result bytes are never printed (`:998-999`).
- The docs already disclaim authentication:
  - `SKILL.md:17` ("treating a client-set MESSAGE_ID as authenticated"), `:30` ("IDs are client-set … not authenticated emitters"), `:88`;
  - `journal-alarm-routing-r14.md:233-237` ("Any process able to write the journal can forge a positive alarm").
- The r15 docs must keep that wording for the positive tokens.

## Not applicable

- `resume_continuity_v1` zero-mutation rejection: this lane surface has no such code path.

## Tooling

None installed or updated. The host-safety amendment was received; no package operation was needed.
