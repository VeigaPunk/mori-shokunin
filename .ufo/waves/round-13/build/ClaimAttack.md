# ClaimAttack — round 13 critic (C1 coverage, C2 operability)

Seat: `MoriR13.ClaimAttack` (critic, leaf). Axes judged: coverage, operability.
Inspection only. No build, test or lint ran, and no journal query ran. The only host reads were
`/proc/sys/kernel/random/boot_id`, `systemctl is-active/is-enabled`, `id -nG`, `bash --version`,
`systemctl --version` and `core_pattern`. Systemd source came from the pinned commit `cf8ebfc6`
(raw GitHub, opened 2026-10-20). Baseline is HEAD `6531ac6`. At read time the working tree
showed the OracleFix diff to `tools/mori-silence-cases.sh`; `tools/mori-census.sh` was not yet
edited. Tool installs: none.

## Canonical source anchors (for L1/JournalKnowledge; S013 is the catalog, unit.c/cgroup.c are code at the same commit)

- Catalog `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in`
  - `:561-566`: `d9b373ed55a64feb8242e02dbe79a49c`, "Unit failed … with result '@UNIT_RESULT@'".
  - `:568-575`: `98e322203f7a4ed290d09fe03c09fe15`, "Unit process exited … exit code is '@EXIT_CODE@' and its exit status is @EXIT_STATUS@".
  - Existing rows: `:66` (coredump), `:604` (unit OOM), `:884` (oomd).
- `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/unit.c`
  - `unit_log_failure` `:6333-6342`: MESSAGE_ID `:6338`, `UNIT_RESULT=` `:6341`.
  - `unit_log_process_exit` `:6355-6392`: level rule `:6372-6377`, MESSAGE_ID `:6380`, `EXIT_CODE=` `:6388`, `EXIT_STATUS=` `:6389`, `COMMAND=` `:6390`.
- `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/core/cgroup.c`
  - `unit_check_oom` `:3055-3105`. It reads `memory.events` `oom_kill`, or `memory.events.local` `oom_group_kill`, at `:3071-3089`. It sets a boolean `increased` at `:3091-3095`. It logs fe6faa94 with "The kernel OOM killer killed some processes in this unit." at `:3097-3100`.
  - `unit_check_oomd_kill` `:3004-3053`: xattr `user.oomd_ooms` at `:3016`, d989611b at `:3040`/`:3046`.
- `https://raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/src/systemd/sd-messages.h`
  - `:41` COREDUMP, `:178-179` UNIT_FAILURE_RESULT, `:184-185` UNIT_PROCESS_EXIT, `:195-196` UNIT_OOMD_KILL, `:198-199` UNIT_OUT_OF_MEMORY.

Version caveat: these anchors are on systemd main. The host runs `systemd 261 (261.2-1-arch)`.
Whether v261 behaves the same is [INFERENCE]; re-anchor at tag `v261` if the claim depends on host behavior.

## Findings

### A1 — C1 does not deliver planned FR1, and the planned FR1 contradicted Q15 (scope narrowing; QUALITY 25)

- **Counterexample.** The planned item at `SCORECARD.md:647-649` promises a "system-journal kernel-OOM count probe … after the 5 retained records counted".
  - **Unit.** The 5 are kernel `_TRANSPORT=kernel` records, counted at `kernel-oom-line-attribution-r12.md:15-16` with `journalctl -k … --grep=`. Kernel records carry no MESSAGE_ID. fe6faa94 is something else: a service-manager unit notice (cgroup.c `:3097-3100`). C1 counts notices, so it cannot count those records.
  - **Window.** C1 is boot-scoped. The 5 kernel records and the 7/9 notices all sit in boot `7bd93aee…` (`kill-classes-by-message-id-r12.md:14-16`). The current boot is `430d3038-1859-49e6-82cf-5fc475d1b3d0`, and r12 measured `-b 0` → 0 (`kernel-oom-line-attribution-r12.md:15-16`). The live after-value of "5" is unreachable. A live current-boot delta is likely 0 → 0 [INFERENCE; unmeasured].
  - **Method.** The planned recipe used `--grep`, which matches the MESSAGE field. That is text classification, which QUALITY 15 (`corpus/QUALITY.md:29`) forbids. So the plan could not be admitted as written.
- **Impacted axis:** coverage (claim scope); frontier honesty (`PROVINCE.md:31` FR1).
- **Smallest safe correction.**
  - Record in SCORECARD/LOG an explicit planned→delivered correction: "FR1 kernel-record count not delivered; replaced by structured notice counts. The planned recipe violated Q15."
  - FR1 stays frontier. Kernel record count, `task_memcg` attribution and fleet correlation remain residuals.
  - The C1 before→after must be fixture-proven presence and discrimination of the rows (count, 0, unavailable), not "5".
  - Do not write "frontier → core".

### A2 — Retiring the text classes loses a DRIFT path unless replaced structurally (parent asked this)

- **Assessment.** Retiring them is a legitimate correction.
  - Text classes are inadmissible under Q15.
  - FP-7/FP-8 in `.ufo/waves/shokunin12h-20261014-p4-mori-r1/members/FalsePositiveAudit.md:203-249` show desktop-scoped and narrative false positives.
- **Counterexample (harm).** Baseline `KILL_SIGNAL_JOURNAL warn` flipped DRIFT (`tools/mori-census.sh:897-899`). A SIGKILLed fleet unit would have flipped DRIFT before; with pure retirement it flips nothing.
  - A structured equivalent exists with a pinned anchor: catalog `:568-575`, fields from unit.c `:6388-6389`.
  - The parent's follow-up directs the replacement. If it lands, the remaining OOM side is fine: an OOM inside the user slice still flips DRIFT through `CGROUP_OOM_KILL` (the same `memory.events` counter that cgroup.c `:3084-3086` watches). No new CGROUP probe is needed.
- **Acceptance conditions for the replacement.**
  1. Match on `MESSAGE_ID=98e322203f7a4ed290d09fe03c09fe15 EXIT_CODE=killed EXIT_STATUS=9`. Different fields AND together; same-field repeats OR [INFERENCE from journalctl match semantics, S014].
  2. Use `--output-fields=_BOOT_ID` only. `COMMAND=` (`:6390`) and `MESSAGE` never appear in output.
  3. User scope is WARN, system scope is INFO, never summed.
  4. Name the delivery paths this cannot see (Q17): processes that are not a unit's main/control process, such as children inside a tmux scope; kills of units with no `crt`/runtime; manager-escalated stop SIGKILLs, which are not fleet-caused.
  5. OOM-killed main processes also produce `killed/9`, so 98e32220 overlaps fe6faa94. These are classes, not victims; never add them.

### A3 — The oomd zero reads as "no kills" (r12 knowledge contradiction)

- **Counterexample.** `systemctl is-active systemd-oomd.service` → `inactive`; `is-enabled` → `disabled` (re-read 2026-10-20). `userspace-oom-killers-r12.md:6,21` says a probe "must render `unavailable (inactive)`, never a zero-kill result". The CensusFix brief's "valid empty query ⇒ 0" emits `oomd=0` on this host.
- **Correction (parent's follow-up adopts it).** Emit `activity=unmeasured` next to the 0 notice count. Keep the wording "records carrying d989611b: 0", never "oomd kills: 0". With no systemctl probe, the evidence cell must say killer activity is unmeasured.
- **Same class for coredumps.** A 0 fc2e22 count means nothing if `core_pattern` does not pipe to systemd-coredump.
  - On this host it does: `|/usr/lib/systemd/systemd-coredump …`, and the socket is active.
  - Name it as an assumption of the row and do not probe it.
- **Axis:** coverage (unavailable ≠ healthy).

### A4 — fe6faa94 is not a "kernel OOM notice" (naming/identity)

- **Evidence.** cgroup.c `:3091-3100`.
  - One notice fires per detected increase of the unit's `memory.events` `oom_kill`, which is a hierarchical counter. A jump of several kills yields one notice (under-count). Each watched ancestor unit also notices (fan-out, matching r12's 5 vs 7 vs 9).
  - Units without cgroup runtime emit nothing (`:3060-3062`).
- **Problem.** The CensusFix brief and the S013 used-by text say "kernel OOM notices".
- **Correction.** Label the row "unit-OOM notice (service manager)" with unit `notice`. The finding id must not contain KERNEL. The r13 knowledge note cites cgroup.c `:3055-3105`.
- **Axis:** coverage (unit honesty; Q16).

### A5 — Reusing an id with new semantics is hidden by the drift count mask (identity change)

- **Counterexample.** The drift pin masks count-only changes behind the same finding id (`audit-r11.md:211` D16). If `OOM_KILL_JOURNAL` or `SEGFAULT_JOURNAL` kept its id but switched meaning (text → MESSAGE_ID notices, or signal 11 → all coredumps), `--drift` would show no semantic change.
- **Status.** The parent reports new labels with no aliases, and the signal-11 count keeps COREDUMP_SIGNAL semantics. That is acceptable only if `SEGFAULT_JOURNAL` now counts `COREDUMP_SIGNAL=11` alone. fc2e22 (all signals) needs a distinct id (D08, `audit-r11.md:203`).
- **Check for L1.** `grep -n 'SEGFAULT_JOURNAL' tools/mori-census.sh` must sit only beside the `COREDUMP_SIGNAL=11` count.
- **Axis:** coverage/freshness.

### A6 — rc semantics: an empty result may exit 1 (direct falsifier of "valid empty ⇒ 0")

- **Evidence.** On this host, `journalctl --user -b … -g '<no-such-token>'` exited **1** (`.ufo/waves/shokunin12h-20261014-p4-mori-r1/members/UnavailableVsUnhealthy.md:65`). Baseline therefore accepted rc 0 and 1 (`tools/mori-census.sh:868-869`).
- **Risk.** The new rule "nonzero ⇒ unavailable" is right only if a field-match query with no results exits 0. That was measured for `-g` only; for field matches it is [UNKNOWN]. If such queries exit 1, every quiet scope renders `unavailable` live while the fixtures stay green.
- **Proposed L1 check.** MESSAGE-free:
  ```
  journalctl --user -b -q -o json --output-fields=_BOOT_ID MESSAGE_ID=00000000000000000000000000000000; echo rc=$?
  ```
  Repeat with `--system`. Also count parsed objects whose `MESSAGE_ID` equals the ID, never `wc -l`; without `-q` journalctl may print `-- No entries --` [INFERENCE].
- **Axis:** coverage/operability.

### A7 — Partial readability and spoofing (named residuals, not blockers)

- **Partial permission.** The user is in `wheel`, so the system journal is readable live and the `unavailable` arm is fixture-only. A partially readable file set can exit 0 with incomplete counts [INFERENCE]. Disclose it as a residual.
- **Spoofing.** MESSAGE_ID carries no underscore, so the client supplies it (S015, `kill-classes…r12.md:12`). Any user process, including a lane, can write `MESSAGE_ID=98e32220… EXIT_CODE=killed EXIT_STATUS=9` and force user-scope WARN DRIFT. This fails loud, not silent, and baseline text had the same exposure. A system-scope `_PID=1` narrowing is possible [INFERENCE]. Name it under Q8 rather than claim "cannot fake".
- **Axis:** calibration of the claim.

### A8 — Cost is unpriced (QUALITY 11; operability)

- **Before.** 1 full `--user -b` text dump, plus 1 live-only JSON coredump query (`:865`, `:883`).
- **After.** Up to 5 classes × 2 scopes of indexed queries, or fewer with OR'd matches. The system journal is newly read. None of them has a timeout bound (same as baseline).
- **Prior dispute.** The r12 critic already disputed "unchanged" operability over 4.3 s wall time with no budget (`SCORECARD.md:612`). Marginal wall time is [UNMEASURED]; it could fall, since the full-text dump disappears.
- **Required.** L1 must price the change: found-ness, live census median of 3 before and after, the enforced bound (none), and the filter's drop set (A2 item 4). Without that, operability cannot be "harm none".

### A9 — Live-only branch: the selftest cannot see the structured path (QUALITY 8)

- **Evidence.** The baseline JSON coredump count ran only when `MORI_FIXTURE` was unset (`tools/mori-census.sh:882`), so the selftest never exercised it.
- **Acceptance.** The new structured counts must have no `MORI_FIXTURE` branch.
- **Check.** `grep -n 'MORI_FIXTURE' tools/mori-census.sh` must not appear inside `probe_journal`.

### A10 — F01: a here-string fix introduces a temp-file failure channel that fails open

- **Mechanism.** The defect is at `tools/mori-census.sh:1494` (`printf | sed | grep -Fxq`).
  - Under the Appendix B fixture, 12,001 lines × ~55 B ≈ 660 KB, above the pipe capacity.
  - Bash 5.3.15 then backs the here-string with a temp file in `$TMPDIR` [INFERENCE from bash ≥5.1 here-doc behavior]. Without space or quota (the host's known D21/FR2 class), the here-string fails, grep sees no input, and the grade reverts to `progressing-weak` with rc 0. That is the original symptom, now via ENOSPC.
  - Contrast: the oracle's here-strings fail closed (`verdict_grade` → `missing`, `mori-silence-cases.sh:582-584`). The census side would fail open.
- **Smallest safe correction.** No temp file and no early-exit consumer. Either:
  - one awk pass that reads the whole input: `awk -v n="$needle" '{sub(/^[0-9]+ /,"")} $0==n{f=1} END{exit !f}'`; or
  - `grep -Fxc` (reads to EOF) on the captured value, with a numeric check.
  Pass the needle via `-v`, never the history, which avoids MAX_ARG_STRLEN.
- **Acceptance tests.**
  - Long-history positive: subject first plus 12,000 siblings → `progressing`.
  - Sibling-only negative: → `progressing-weak`, `other_authored_commits=12000`.
  - Subject last and in the middle.
  - Near-miss authors: `kagi-shokunin2 <…>`, trailing junk, case variant → not subject.
  - If a here-string is kept, an unwritable-`TMPDIR` variant must not grade `progressing-weak` silently.
- **LOW.** `psi_avg10` (`:575`) pipes into an early-exit awk. The input is tiny, and `|| true` masks rc. Note it under Q7 and leave it.
- **Axis:** operability.

### A11 — F02: C2 closes the word/cardinality/rc classes, not D02 (tally corruption remains)

- **Evidence.** `VERDICT_RE` (`mori-silence-cases.sh:579`) accepts any digits.
  - `MORI_CENSUS: CLEAN (findings=0 drift=7 …)` with rc 0 passes.
  - The census invariant is ROLL=DRIFT ⇔ N_DRIFT>0 (`tools/mori-census.sh:367-371`).
  - D02 explicitly requires "BANANA/roll-rc/**tally-corruption** mutants must fail" (`audit-r11.md:197`).
- **Further accepted shapes.** A roll that is not the last line, and output appended after it.
- **Criterion 7 wording.** `mori-silence-cases.sh:635` and the shape grade (HEAD `:1038`) still pipe `printf` into `grep -m1`. Captured content is unaffected and rc is masked, but the shape equality is a match test on live-pipe output.
- **Smallest correction (behavioral, no source inspection).**
  - Require `CLEAN ⇒ drift=0`, `DRIFT ⇒ drift≥1`, and `drift ≤ findings`.
  - Optionally require the roll to be the last non-empty line.
  - Otherwise, the C2 claim and the QUALITY 26 wording must say "word/cardinality/rc", and D02 stays open for tallies.
- **Axis:** operability (claim scope).

### A12 — Freshness side effect (unowned axis; disclose)

- **Mechanism.** C1 rewrites the `SURFACE journal` field set and finding ids. The r10 pin is already red, so exit 1 is unchanged. But r12's classification (`corpus/evidence/drift-r12-20261019T2204Z-classification.md`) will not cover the new tokens. That trips the planned r13 #1 falsifier "any unclassified token" (`SCORECARD.md:643`).
- **Correction.** LOG/SCORECARD name the new journal tokens as intentional C1 schema drift, carried to the deferred re-pin. The LOG already says the re-pin is not claimed; add the token list.

## Bounded verdict guidance (for L1; the Rust judge decides)

- **C1 coverage: improved** is defensible only if all of these hold:
  - A2 lands, or the lost DRIFT path is named in the evidence cell.
  - A3 `activity=unmeasured` is present.
  - A1's narrowing is recorded.
  - A6's empty-rc check passes.

  Otherwise the honest cell is "unchanged" with a residual list.
- **C2 operability: improved** is defensible for F01 (with A10's negatives) and for F02's word/cardinality/rc classes. The claim must not say D02 is closed while A11's tally class passes. A8's cost must be priced before "harm none".
