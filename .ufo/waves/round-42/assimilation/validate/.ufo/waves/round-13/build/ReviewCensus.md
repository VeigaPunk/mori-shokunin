# ReviewCensus — round 13 structured journal scopes (C1) and F01 authorship (C2)

Seat: `MoriR13.ReviewCensus` (reviewer, leaf). Scope: read-only review of the baseline
census journal probe, the F01 authorship branch, and the proposed structured
MESSAGE_ID count architecture (CensusFix / JournalSource / FieldsSource / CatalogSource
inputs). No source edited, no tests, no census or oracle run, no live journal query, no
journal `MESSAGE` read.

Tool installs/updates this seat: none. Git: `git branch -a` shows only `master`
(`6531ac6`); there is no separate F01 branch — F01 is the live line on `master`.

Verdict on the proposed architecture as stated in the wave spec: **not acceptable as
written.** The direction (MESSAGE-free, boot-scoped, scope-separated, count-only) is
correct; the rc, empty-versus-denied, identity, label and coverage semantics below must
be settled first. Facts marked [INFERENCE] or [UNOBSERVED] were not measured by this seat.

---

## 1. Baseline anchors (master, `tools/mori-census.sh`, `census-r5`)

| Anchor | What it does today | Review note |
|---|---|---|
| `:854-912` `probe_journal` | `cap journalctl --user -b --no-pager`; rc gate `rc -gt 1 → unavailable`; text greps for four classes; findings `OOM_KILL_JOURNAL crit`, `KILL_SIGNAL_JOURNAL warn`, `SEGFAULT_JOURNAL info`, `UNIT_FAILURE_JOURNAL info`, `UNIT_FAILURE_OUT_OF_SCOPE info` | Text classes, user scope only, `cmd=` printed in the row |
| `:865-872` | rc `0` and `1` both accepted | rc 1 is treated as "empty"; a permission failure with rc 1 becomes a silent zero |
| `:874-875` | `grep -ciE 'Out of memory\|oom-kill\|oom_reaper\|Killed process'`; `grep -ciE 'status=9/KILL\|...\|SIGKILL'` | Text match on MESSAGE; the spec forbids this |
| `:881` | `grep -ciE 'segfault\|general protection fault'` | Text match on MESSAGE |
| `:882-886` | `c_seg_json=$(cap … -o json COREDUMP_SIGNAL=11 2>/dev/null; printf … \| grep -c 'COREDUMP_SIGNAL' \|\| true)` | **CAP_RC is never read on this path.** A failed `journalctl` yields `CAP_OUT` = error text, `grep -c` = 0, `c_seg_json = 0`: silent false zero. It also counts substring hits anywhere in the stream, including stderr |
| `:890-891` | unit failure text grep, then fleet-name filter | Structured replacement not in the spec (see B6) |
| `:893-909` | DRIFT on `oom_kill>0` (crit) and `kill_signal>0` (warn) | Changing the class changes the DRIFT trigger set |
| `:911` | `SURFACE journal … oom_kill= kill_signal= segfault= unit_failure= rc=` | Key names are in `DRIFT_COUNTER_KEYS` (`:1766`, `:1768`, `:1771`) |
| `:849-853` header comment | "DRIFT on oom_kill>0 or kill_signal>0 (mint demand)" | Must be rewritten with the new classes |
| `:1723` | `run_census` calls `probe_journal` between waves and cgroup | Order unchanged by the proposal |
| `:1763-1775` `DRIFT_COUNTER_KEYS` | includes `kill_signal oom oom_kill segfault unit_failure` | New keys must be added longest-first (see M3) |
| `:1490-1499` F01 | `inwin=$(… awk …)`; `sibn=$(… awk 'END{print NR}')`; `if printf '%s\n' "$inwin" \| sed -E … \| grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"; then subj=1 else sib=1` | **The defect.** See §2 |
| `:2041-2042` selftest dispatcher | `journalctl) out_of journal; exit "$(rc_of journal)"` | **Args-blind**: every journalctl call (text or JSON, any filter) returns the same `journal` fixture file |
| `:2475-2479` | fixture `kernel: Out of memory: Killed process 4242` → `DRIFT OOM_KILL_JOURNAL` | Text-only fixture; will stop matching under any structured design |
| `:2676-2679` | `journal-empty-ok` → `CLEAN`, `^SURFACE journal: ok` | Needs an empty structured reply and the measured empty-query rc |
| `:2562-2564` | only F01-adjacent case: short sibling-only → `progressing-weak` | No long-history subject-positive case exists anywhere in the census or oracle selftest |
| `tools/mori-silence-cases.sh:517,525` | `printf … \| grep -m1 …\|\| true` into a value | Not an F01 defect (grep prints before it exits; rc masked), but it is a producer pipe into an early-exit grep under criterion 7. Report to ReviewOracle/OracleFix |
| `:1494` in `probe_silence` only | the only live producer pipe into a match test in the census | Sole F01 site |

Knowledge anchors used: `corpus/knowledge/kill-classes-by-message-id-r12.md` lines 6, 9–18,
21–24, 30–33; `corpus/knowledge/userspace-oom-killers-r12.md` lines 14–18, 24, 30;
`corpus/knowledge/audit-r11.md` F01 `:156`, F02 `:157`, D01 `:196`, D02 `:197`,
D08 `:203` (system journal absent), D09 `:204`, D21 `:216`; `SKILL.md:17`, `:28-31`
(journal row and oomd-inactive rule), `:90-91` (baseline reads red from 2026-10-19).

---

## 2. F01 — mechanism and acceptance

**Mechanism (direct from `:1490-1499`).** The `if` tests the rc of a pipeline under
`set -o pipefail`. `grep -Fxq` exits at its first match. When the matching line is early
in `$inwin` and `$inwin` is larger than the kernel pipe buffer, `printf` (and `sed`) is
still writing when `grep` exits, takes SIGPIPE (141), and pipefail makes the pipeline
rc non-zero. The `if` then takes the `else` branch: `sib=1`, the lane is graded
`progressing-weak`, and `other_authored_commits` reports the full sibling count.

Trigger conditions (all required):
1. the exact `<lane>-shokunin <lane@shokunin.local>` line is among the post-launch
   commits and is the **newest** one (git log is newest-first, so it is line 1);
2. the rendered `$inwin` exceeds one pipe buffer (64 KiB default on Linux; do not depend
   on the number — the fix must not depend on it);
3. the run goes through the production `grade_lane` path (not a fixture that bypasses it).

Trigger-free cases stay correct: subject-newest with a short window (no SIGPIPE, the
pipeline succeeds); subject-oldest with a long window (grep reads to EOF, no SIGPIPE).
That explains why the 66-case selftest and the 28-case oracle both pass while F01 is live:
neither has a long-history subject-newest arm. The audit reproduction (subject line plus
12,000 sibling lines) matches the mechanism: `progressing-weak … other_authored_commits=12001`
(audit-r11 F01 `:156`).

**Acceptance conditions for any F01 repair (bounded; no test run this seat):**
- A1. No pipeline whose result feeds an `if`/`&&`/`||` match test is fed by a live
  producer. The match runs over a captured variable (`case`/`[[ ]]` on a newline-framed
  string, or `grep -Fxq -- pat <<<"$stripped"`). The rc of the stripping step is read
  separately (`|| true` only where the value is then re-validated).
- A2. The subject-newest long-history arm (≥ 65,537 bytes of `$inwin`, subject line first)
  returns `progressing` with `basis=row-A`, rc 0. The fixture must be generated by a
  committed generator (e.g. `git fast-import` with explicit committer times in the
  `(launch, NOW]` window), not a `/tmp` artifact (QUALITY criterion 23).
- A3. The subject-oldest long-history arm and the sibling-only long-history arm (12,000+
  lines) return the same states they return today (`progressing` and `progressing-weak`
  respectively), with `other_authored_commits` equal to the exact sibling count. Pinned
  numbers, not "≥".
- A4. Identity remains whole-line exact on both fields: `substring-name-mismatch` and
  `substring-email-mismatch` (`:853-871` of the oracle) still yield `progressing-weak`.
- A5. Row A/C attribution is unchanged for the short cases already in the census selftest
  (`:2562-2564`) and the oracle cases at `tools/mori-silence-cases.sh:822-871`.
- A6. The repair does not change `:1490-1493` window arithmetic (strict `%ct` bounds).
- A7. The repair states, in the row or the header, that the failure class was a pipeline
  rc consumed as a match result (criterion 7), and cites `:1494` as the increment site
  (criterion 14).

Sibling sites to report, not fix here: `tools/mori-silence-cases.sh:517,525` (see §1).

---

## 3. Structured count architecture — findings

### BLOCKING

**B1. rc semantics: the empty query's rc is unmeasured, and the spec's rc1 rule may make
every quiet host `unavailable`.** The current code's own comment says rc 1 "can mean empty
on some builds" (`:868`). The spec says "failure rc1/rc2 → unavailable" and "valid empty
query → 0" without defining the valid-empty rc. If a valid empty `MESSAGE_ID=` query
returns rc 1 on this systemd (261.2 on the host per the knowledge note header, 262 per S014),
then a quiet host reports `unavailable` for every class, and `journal-empty-ok` cannot pass.
If instead rc 1 is treated as empty, a real failure that exits 1 becomes a false zero.
- Acceptance: the design must pin, from a measured run recorded in the wave report, the
  rc **and** the stdout/stderr byte counts for (a) a valid empty match, (b) a permission
  failure on `--system` for a non-privileged account, and (c) a bad option. Until pinned,
  the implementation must not map rc 1 to 0 nor to unavailable by assumption.
  [UNOBSERVED here — owner JournalSource.]
- Rule, once pinned: valid zero = rc equal to the pinned empty rc **and** empty stderr
  **and** empty stdout. Any other rc, any stderr bytes → `unavailable reason=rc<N>` or
  `reason=stderr`. Never 0.

**B2. Empty-versus-denied hole (already present).** `:869` accepts rc 1, `cap` merges
stderr into `CAP_OUT` (`:505`), and `:883` ignores CAP_RC altogether. A permission
failure can therefore read as zero on the user path (rc 1) and on the segfault JSON path
(any rc). The new design must not inherit either.
- Acceptance: every structured query gates on rc and on the presence of stderr bytes
  before any count is printed. Stderr is captured separately (not `2>&1` into the parsed
  stream) so `reason=access` and `reason=malformed` remain distinguishable. Merging stderr
  into the JSON stream is fail-closed but mislabels the reason; prefer separate capture.

**B3. Identity: `MESSAGE_ID` is a client-set field; the count is "entries carrying a
catalog ID", not "events systemd emitted".** Any same-UID process can write a journal
entry with `MESSAGE_ID=fe6faa94…` (user journal). The spec's "trusted structured field"
language (QUALITY criterion 15) is accurate only for `_`-prefixed fields; `MESSAGE_ID`
is not one of them [FieldsSource to confirm against S015; this seat's reading is that it
is a user field]. Consequences:
- A spoofed entry can raise a crit DRIFT (false red). It cannot hide a real entry.
- The count is not an authenticated kill signal and must say `trust=client-supplied`
  on the row, and the knowledge note must list it under "Delivery paths this cannot see"
  (criterion 17). The existing note (`kill-classes-by-message-id-r12.md:32-33`) does not
  list spoofing; it must.
- Acceptance: row and knowledge note both name the residual. No row may describe the
  count as proof of a kill, a victim or a fleet cause (criterion 16).

**B4. Record identity checks are missing from the spec.** Required per-record checks
(all must hold; a failure of any one → the whole scope is `unavailable`, not a partial
count):
- each non-empty stdout line parses as one JSON object (validate with `jq -e` over the
  captured buffer via here-string; `command -v jq` is the presence check; absence →
  `unavailable reason=no-jq`);
- `MESSAGE_ID` is present, a JSON **string** (not array), and equal byte-for-byte to the
  requested 32-hex ID; **a non-matching record is an identity mismatch → unavailable,
  never silently skipped** (QUALITY criterion 5: keep the rejection; the stub that
  ignores filters must fail loudly, not pass quietly);
- `_BOOT_ID` is present, a JSON string, and equal to the current boot ID (see B5);
- no key named exactly `MESSAGE` appears in any record (defence in depth: the
  `--output-fields` restriction is the primary control; a leaked MESSAGE key → the scope
  is unavailable and nothing from that record is printed);
- `__CURSOR` values are unique within the scope's stream; a duplicate → unavailable
  (no double count from a repeated stream).
- Count = number of valid, identity-matching records. Printed as `count=N` only.

**B5. Boot scope is not anchored.** `-b` selects the current boot, but the row and the
drift mask never say which boot. QUALITY criterion 12 requires the baseline next to a
cumulative counter.
- Acceptance: read the boot ID once (`/proc/sys/kernel/random/boot_id`, overridable via an
  env var for fixtures, shape-validated as a UUID before use or print), compare every
  record's `_BOOT_ID` against it (B4), and print `boot=<id>` once on the scope row. Add
  `boot` (or the boot-ID field name chosen) to `DRIFT_VOLATILE_SPECIAL`, otherwise every
  reboot is a false DRIFT (criterion 10).

**B6. Coverage loss stated as a rename.** The spec replaces four text classes with three
MESSAGE_ID classes and does not name a replacement for two of them:
- `kill_signal` (`status=9/KILL`, `Failed with result 'signal'`, `SIGKILL`): no
  structured class in the spec. It is currently a **warn DRIFT trigger** (`:897-900`).
  Dropping it removes a DRIFT path. Either supply a catalog-verified ID for the class
  (look it up in S013 only; do not recall one), or record the drop as a named coverage
  loss in the row, header, knowledge note and PROVINCE/SKILL changelog.
- `unit_failure` (`Failed with result`, `Unit entered failed state`, fleet-name filter at
  `:891`): no structured class in the spec. It is info-level. Same two options.
- `segfault` (`COREDUMP_SIGNAL=11` JSON path, `:882-886`, measured as 656 entries
  in a 2026-10-15 run per the comment at `:876-878`): the spec replaces it with
  `fc2e22bc` (any core dump). That is a **widening** of the class, not a rename:
  `fc2e22bc` counts every core-dumping signal, not only SIGSEGV/11. Either keep a separate
  `COREDUMP_SIGNAL=11` structured count (it is a trusted-enough structured field, not MESSAGE)
  or rename the class to `coredump` and state that signal 11 is no longer isolated
  (D08 and audit `:203` warn against conflating them).
- The spec's "coverage" claim is therefore **not** demonstrably improved. On the user scope
  it may be flat or lower until B6's two options are decided. The lane's lowest axis is
  coverage; a move that drops classes is a harm on that axis unless the drop is replaced
  or explicitly accepted.

### MAJOR

**M1. System scope access must be graded, never assumed.** `--system` needs journal group
membership or root. A non-privileged read may return rc 0 with an access hint and no
entries; that is indistinguishable from "no notices" unless stderr or the hint is checked.
[UNOBSERVED here — JournalSource measures it.] The knowledge note's system counts (9 for
`fe6faa94`, 0 for `d989611b`, `kill-classes…:16,18`) show access works on this host; that
is one observation, not a guarantee.
- Acceptance: the system row is `unavailable reason=access` unless the query's rc and
  stderr pass (B1/B2). It is never `count=0` on an access-unproven read.

**M2. Class-to-scope mapping is unverified for `d989611b`.** systemd-oomd's notice is
written by the oomd service in the system manager [INFERENCE from
`userspace-oom-killers-r12.md:14-18,24`: oomd is inactive and disabled on this host, and
the note calls the user-scope count "not a historical-kill conclusion"]. If so, a
user-scope `d989611b` query is structurally blind. Both zero counts (`:18` of the oomd note)
are therefore not evidence of "no oomd kills", and the oomd note itself says an inactive
killer must render `unavailable (inactive)`, never a healthy zero (SKILL `:29`).
- Acceptance: the `d989611b` row carries `killer=oomd service=inactive|active|unknown`
  (read from the unit state, or `unknown` with a reason), and `count=0` with
  `service=inactive` prints as `unavailable (inactive)` in prose and does not count as healthy.
  The scope on which the class is read must be the one the catalog entry is emitted in,
  stated with the S013/S014 anchor.

**M3. Drift keys and baseline.** Renaming or re-typing `oom_kill`, `kill_signal`,
`segfault`, `unit_failure` and adding new keys changes the `SURFACE journal` row. The
persisted `baseline-r10-20261015T2231Z.json` will then show `-key/+key` drift on every such
field (intentional, but real). Requirements:
- New counter keys must be added to `DRIFT_COUNTER_KEYS` in longest-first order where one
  key is a prefix of another (the comment at `:1760-1762` says so; `oom` vs `oom_kill`
  already needs it). A fixture that renders each new key through `drift_normalize`
  must show it masked.
- `boot`/boot-ID field goes to `DRIFT_VOLATILE_SPECIAL` (B5).
- The baseline is **not** re-pinned in this round unless the reason is recorded
  (criterion 10). The round's own `--drift` run is expected to be red on the journal row;
  the report must say so and must not present the red as a regression.

**M4. Finding ids are a compare contract.** The header (`:223-234`) lists the ids as
stable. Keep an id only where its meaning is identical. `OOM_KILL_JOURNAL` (`crit`,
DRIFT) changes meaning from "text match" to "notice count" (criterion 14: cite the
increment site, `S013` `:604-605` for `fe6faa94`, not the old word list). Recommend renaming
to new ids (e.g. `OOM_NOTICE_JOURNAL`, `COREDUMP_NOTICE_JOURNAL`) so the diff shows removed
and added lines rather than a silently changed meaning. Each id's severity must match the
scope rule below.

**M5. Scope rule and severity asymmetry must be stated, not implied.** The spec says
system-specific ids are INFO only. That means a fleet-relevant unit-level OOM notice in the
system manager cannot raise DRIFT. That is an alerting-policy decision; it must be written
into the header and PROVINCE, with the reason (fleet units run in the user manager;
system notices are host observations under tsukuroi's triage per `SKILL.md:44-47`). Without
it the roll is silently blinder than the old text probe on the system side, which was
never read at all.

**M6. Kernel OOM is not in these classes.** `fe6faa94` is systemd's unit notice ("A
process of @UNIT@ unit has been killed by the OOM killer", `S013` `:604-605`, knowledge
`:10-11`), emitted by PID 1 for a unit, not a kernel record. The spec calls it "kernel OOM
notices", and `SKILL.md:30` says "unit hit by kernel OOM". The kernel victim record
(`oom-kill:constraint=…`, `journalctl -k`) is the only kernel-side class and it is **not**
counted by any proposed class. The FR1 claim must therefore not say "kernel OOM counted".
Label the class `unit-oom-notice (systemd, from a kernel OOM kill)` on the row, and keep
`kernel victim record` out of the count until a separate, reviewed probe exists.

**M7. Selftest stubs are args-blind, so the structured probe cannot be tested as written.**
`:2041-2042` returns the same `journal` file for every invocation. A JSON probe that
receives text fixture bytes gets a parse failure → `unavailable`. Scenario cases that
expect `DRIFT`/`FINDING` from text (`:2475-2479`) will flip to `unavailable` silently, and
`journal-empty-ok` (`:2676-2679`) needs a structured empty reply. Acceptance:
- the stub dispatches on the requested `MESSAGE_ID=` and `-o json` and returns the
  scope-specific fixture (or empty for quiet arms);
- the text `journal` fixture is retired for this probe (not kept as a second source);
- OracleFix's `tools/mori-silence-cases.sh` stub is coordinated (it currently has the same
  args-blind stub). This seat does not edit it.

### MINOR / PRESENTATION

**m1.** Header comment `:849-853` and the `:15` summary still describe kill/OOM text
classes and `DRIFT on oom_kill>0 or kill_signal>0`. Rewrite with the new semantics.
**m2.** `cmd=` string in the row (`:855`, `:911`) is fine (no MESSAGE), but the new row must
print the exact query shape (`--output-fields` list and the four IDs) so an auditor can
replay it without MESSAGE (criterion 9: the published command must resolve).
**m3.** `timeout`: each `journalctl` call should be bounded with `run_timeout` (`:516-523`).
The census's own rule is "never hang" for external reads (`:510-515`); the current journal
call is unbounded. Recommended, not blocking.
**m4.** The knowledge note `kill-classes-by-message-id-r12.md` is the right place for the
trust residual (B3), the scope mapping (M2) and the notice-versus-kernel label (M6). It
currently says "kernel victim count" in its Observed section; keep that phrase only for
the kernel record, which is not counted here.
**m5.** Do not present zero as "no kill" in any row. Zero is "no matching record in
this scope, this boot, with this access and this service state".

---

## 4. Proposed bounded acceptance conditions (for L1 and CensusFix; no tests run here)

Structured count (C1), each condition checkable from code and fixture definitions:

1. **rc pin.** The valid-empty rc and the denied-access rc/stream shape are recorded from
   a measured run in the wave report (B1). Until then no code path maps an unpinned rc to 0.
2. **Stream discipline.** Stdout and stderr are captured separately; any stderr bytes →
   unavailable with `reason=stderr`; rc ≥ 1 (after the pinned empty rc) → unavailable with
   `reason=rc<N>`; absent journalctl → unavailable (`reason=journalctl-missing`).
3. **Record gate.** Every stdout line is one JSON object; the whole buffer validates before
   any count is printed; a malformed line, array-valued `MESSAGE_ID`, non-string `_BOOT_ID`,
   duplicate `__CURSOR`, leaked `MESSAGE` key, or non-matching `MESSAGE_ID` → the scope is
   `unavailable reason=malformed|identity|dup-cursor|message-key` (B4).
4. **Boot.** `_BOOT_ID` equals the current boot ID (read once, shape-validated); `boot=` is on
   the row; boot ID is in the volatile list (B5).
5. **Scopes.** `scope=user` and `scope=system` rows are separate; no summed total in any
   row, finding, or drift key; `system` is `unavailable reason=access` unless access is
   proven by the gate above (M1).
6. **Units.** Each class row names its unit: `unit=notice` for `fe6faa94` and `d989611b`,
   `unit=coredump-notice` for `fc2e22bc`. No row says "kill" for a notice class (criterion 16).
7. **Trust.** Each row carries `trust=client-supplied`; the knowledge note lists spoofing
   under delivery paths it cannot see (B3, criterion 17).
8. **Killer state.** The `d989611b` row carries the oomd service state; `count=0` with
   service inactive is prose `unavailable (inactive)` and is never a healthy zero (M2).
9. **Coverage disclosure.** Either a structured replacement for `kill_signal` and
   `unit_failure` is supplied from S013 with its anchor, or both drops are named in the row
   header, knowledge note, and PROVINCE/SKILL changelog as coverage losses (B6). Signal-11
   is either kept as its own count or the segfault→coredump widening is named (B6).
10. **Ids and drift.** Renamed ids for changed meanings (M4); new keys in
    `DRIFT_COUNTER_KEYS` longest-first; boot in volatile list; the r10 baseline is not
    re-pinned without a recorded reason; the red `--drift` result of this round is reported
    as intentional schema drift (M3).
11. **Fixtures.** Selftest stub dispatches on arguments (M7); arms exist for: user-positive
    per class; system-positive per class; quiet both scopes → 0 with the pinned rc; rc
    failure; stderr with rc 0; malformed JSON line; text-only stub output (must not count and
    must not print as 0 — must be unavailable); MESSAGE_ID mismatch; boot mismatch; array
    `MESSAGE_ID`; duplicate cursor; long history with a subject-newest F01 arm. All
    fixtures generated by a committed generator, not `/tmp` artifacts.
12. **Honesty of the row.** No row prints MESSAGE, cursor, or a raw record. Only counts,
    unit label, scope label, trust label, boot ID, reason labels.

F01 (C2 part), see §2 A1–A7.

Oracle (for ReviewOracle / OracleFix, out of this seat's scope): the silence oracle needs a
subject-newest long-history case (its absence is why F01 passed), and its `printf | grep -m1`
extractions at `:517,:525` should move to captured-buffer matching.

---

## 5. Residual risk and verification gaps

- **Unmeasured (blocking for B1, M1, M2):** valid-empty rc; denied-access rc and stream
  shape for `--system` and `--user`; whether `d989611b` is written to the system journal
  only; whether `MESSAGE_ID` is accepted as a trusted field under S015. These are for
  JournalSource / FieldsSource / CatalogSource. This seat did not query the live journal.
- **Not measured here:** that `jq` is present on the host (spec says check binary only;
  presence is an operator/host fact, not verified by this seat).
- **Not claimed:** that any structured count equals kernel OOM kills, unique victims, or
  fleet-caused kills. The sources cannot show that (ReviewSources scope).
- **F01 reproduction:** mechanism is from code reading at `:1490-1499` and the
  pipefail/SIGPIPE semantics; the audit's measured instance (audit-r11 F01 `:156`) is cited,
  not re-run here (no verification this seat).
- **Scoring:** lowest owned axes are coverage and operability at 6. This review does not
  support a 7 on either: coverage is flat-or-lower until B6 is decided, and operability
  gains from the MESSAGE-free design are offset by the unmeasured rc and access
  semantics (B1, M1) and the args-blind selftest (M7). CountDesign owns any score mapping.

Installs/updates by this seat: none. Commits: none. Builds/tests/lint/format/smoke runs: none.
