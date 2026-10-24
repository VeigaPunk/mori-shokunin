# WindowAlarmBoundary — round 16 C1 (same-boot journal window vs r15 census alarms)

Seat: `MoriR16.WindowAlarmBoundary` (author lane, leaf). Scope: boundary analysis only.
Write set: this file. No code, fixture, census, harness or SOURCES/PROVINCE edits. No journal
query, no build/test/lint, no selftest run. Tooling: no tool installed or updated; read-only
primary-source fetches and repo reads only. `~/.omp/agent/RULES.md` read before use.

## 1. Godspeed posture and named axes

- **Coverage (C1, FR11):** does the window claim exceed exact retained-cursor continuity?
- **Calibration:** are window outputs named and bounded so they cannot be read as alarms,
  totals, absence, or victims?
- **Operability:** bounded cost, fail-closed reasons, no silent shift of the window start.
- **Adjacency:** census alarm lines, exit codes, finding ids, and the drift pin stay unchanged.

Verdicts are qualitative (improved / unchanged / harmed / unmeasured). No numeric score is
assigned, per the r15 rubric rule.

Rules applied: name the axes; iterate cheap and parallel (repo reads and primary-source fetches
batched); keep only moves that improve one axis and harm none; do not aim at a target count.

## 2. Sources opened this round

| id | what was opened | what it establishes here |
|---|---|---|
| S014 | journalctl(1), systemd 262 (fetched 2026-10-20; sha256 not recomputed) | `--cursor=` "Start showing entries from the location in the journal specified by the passed cursor."; `--after-cursor=` excludes the cursor location; `-b` "will add a match for `_BOOT_ID=`"; matches filter output (same field = OR, different fields = AND); `--output-fields=` always prints `__CURSOR`, `__REALTIME_TIMESTAMP`, `__MONOTONIC_TIMESTAMP`, `_BOOT_ID` in json. |
| S015 | systemd.journal-fields(7), systemd 262 | `MESSAGE_ID` is a lowercase 128-bit hex string without dashes; `_BOOT_ID` is trusted; "User fields are fields that are directly passed from clients"; `UNIT=`/`USER_UNIT=` are manager-supplied user fields. |
| CUR-1 | sd_journal_seek_cursor(3), systemd 262 | "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." |
| CUR-2 | sd_journal_get_cursor(3) / sd_journal_test_cursor(3), systemd 262 | "cursor strings do not uniquely identify an entry: the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible." `sd_journal_test_cursor()` is the API's verification after a seek. |
| S038 | `service.c` `service_result_table` | Not re-opened this round. Cited from `corpus/knowledge/journal-positive-evidence-r15.md` (`"oom-kill"`, `"signal"`). [CITED] |
| repo | `PROVINCE.md:25,40,54`; `corpus/knowledge/journal-positive-evidence-r15.md` §3–§6; `corpus/lessons/round-15.md`; `tools/mori-census.sh:892–1007, 1119–1290, 1292–1633, 2516–2519` | Window definition and FR11 scope; r15 predicates, decision table, alarm contract; census OOM/KILL alarm code and positive surface fields; mask list. |

Sections not re-verified here: `-q` suppressing inaccessible-system-journal warnings
(`structured-journal-scopes-r13.md:23`, [CITED]). The S014 `--cursor` inclusion of the anchor
entry is not stated explicitly in S014 (see §6, U1).

## 3. The boundary, stated once

**The window is not an alarm source.** It is a separate, anchor-relative, operator-supplied
observation. The census is a pure function of the host at census time. Integrating window counts
into `OOM_KILL_JOURNAL` or `KILL_SIGNAL_JOURNAL` would make the alarm depend on which anchor an
operator happens to hold. The same host would then alarm, go silent, or re-alarm depending on
when the anchor was last set, and the anchor is never advanced automatically.

Specific reasons to reject any automatic integration:

1. **Anchor-dependent state.** A window count is a function of (anchor, now). A census alarm must
   be a function of (host, now). Mixing them breaks the census's reproducibility and its
   selftest/drift-pin determinism.
2. **Duplicate firing.** r15 requires "at most one OOM line and at most one user WARN" per census
   and says "Do not emit a second OOM line for a second positive source"
   (`journal-positive-evidence-r15.md` §5 row 9, §6). A window alarm would be a second source on
   the same boot's records.
3. **Subset, not new evidence (usually).** Same predicates, same boot (§4). Any record the window
   counts is also a record the census positive query would count, if the census capture succeeded.
   Adding the window only adds evidence in the capture-failure case (§4, row C).
4. **Boot asymmetry.** The census is `-b` current-boot only. The window is anchor-boot-only and
   refuses across reboots (§5). The two surfaces disagree at every boot boundary by design.
5. **Zero is not absence.** A zero window count means "no validated record in this captured
   window". r15 forbids reading a zero as absence (§4 "No completeness"; §6 "No fabricated zero").
   An alarm keyed on "no positives since anchor" would turn that into a health claim.

**Verdict on alarm integration: rejected.** Adjacency, calibration, and coverage all stay
unchanged only if the window never feeds a census finding, exit code, or drift comparison.

## 4. Relation between window subset counts and census alarms

Predicates are identical in both surfaces (`tools/mori-census.sh:1292–1366` and the window's
contract): scalar `_BOOT_ID` equal to expected boot, scalar `MESSAGE_ID` equal to the catalog id,
and per class `UNIT_RESULT` exact `"oom-kill"`/`"signal"`, or `EXIT_CODE` exact `"killed"` with
`EXIT_STATUS` `"9"`/`9`.

| case | census (`-b`, census time) | window (anchor, window time) | relation | alarm effect |
|---|---|---|---|---|
| A | capture ok; aggregate ok or unavailable | capture ok, same boot | W ≤ C for each token [INFERENCE: holds unless journal vacuum or rate-limit removes records between the two captures] | census fires as r15 defines; window none |
| B | capture ok (positives survive aggregate invalidity, r15 row 3) | capture ok, same boot, clean | W ≤ C | none from window |
| C | capture fails (rc≠0, 124/137, stderr bytes, malformed JSON, missing tool) → positives `unavailable` | capture ok | W may be >0 while C has no value; this is a second observation, not a salvage | must not fire any census alarm; r15 row 8 ("no alarm is inferred from that capture") stays true for the census capture. A separate window output is the only place this appears. |
| D | capture ok, aggregate unavailable by an adjacent invalid record | window clean because the invalid record is before the anchor | census positives already present (r15 rows 3, 6) → census already fires | none from window |
| E | any | anchor vacuumed / not the first record / boot changed | window unavailable with stable reason | census unaffected |

Only case C gives the window something the census cannot give, and it is still not an alarm.

## 5. Specific design findings

**F1 (non-obvious) — a filter in the window query converts a fail-closed anchor check into a
silent false continuity.** The contract's first-record rule ("first parsed record must have
exact anchor cursor+boot; drop it") depends on journalctl's `--cursor` returning the anchor
entry first. CUR-1 says a missing cursor seeks to the next closest entry. With no match
filter, that becomes a visible mismatch and the window refuses. If the query adds
`MESSAGE_ID=` matches to bound volume, the first returned record is the first *matching* entry
at or after the cursor. S014 says matches filter the output, so the anchor entry itself may not
appear [INFERENCE]. A vacuumed anchor would then look like a window that starts later, with
no refusal. That is FR11 harm: continuity claimed without the retained cursor. Any filtered
design therefore requires a separate unfiltered anchor proof (e.g., `--cursor=<anchor> -n1
--output-fields=__CURSOR,_BOOT_ID`, exact match) before the filtered query is accepted.

**F2 — do not add `-b` to the window query.** S014: `-b` "will add a match for `_BOOT_ID=`". That
hides foreign-boot records, so a reboot inside the window would look like a clean same-boot
window. The contract needs the boundary to appear as a foreign record and fail closed. Keep the
single `--cursor` query with no boot match.

**F3 — field names collide with census tokens.** The window uses the same `positive_kernel_oom`,
`positive_unit_oom`, `positive_unit_signal`, `positive_process_sigkill` names as the census
(`tools/mori-census.sh:2516`, mask list; `:3506` selftest grep `[ ]positive_kernel_oom=1`).
Nothing mixes the outputs today, but a future grep, mask, or concatenation would let a window
token satisfy a census check. Use a `window_` prefix (e.g., `window_positive_kernel_oom`).
Also do not use the `FINDING` prefix for window output.

**F4 — the name `records_after_anchor` overclaims.** With no match filter, it counts every
journal entry in that scope after the anchor, not class records. A reader will take it as an
event count. Rename to `entries_after_anchor` (unfiltered) or `class_records_after_anchor`
(if filtered, see M2). Add `not_evidence_of_absence=true`.

**F5 — contract contradictions to resolve before implementation.**
- "stdout MUST NOT echo raw cursor or records" conflicts with "End cursor optional reported".
  Resolution: report the end cursor only as `sha256` (the contract already allows a safe SHA256
  of the anchor). Do not print the raw end cursor.
- Exit code 2 is used for both `MORI_JOURNAL_WINDOW_UNAVAILABLE` and
  `MORI_JOURNAL_WINDOW_SETUP`. Consumers must disambiguate by `finding_id`, not `rc`.
- argparse exits with rc 2 and writes usage to stderr. The contract requires one JSON object on
  stdout with `MORI_JOURNAL_WINDOW_SETUP` for setup errors. Catch `SystemExit` and emit JSON.
- The query lacks `--no-pager`. Add it.
- `--cursor` must be passed as a single argv element (`--cursor=VALUE`) so a value beginning
  with `-` cannot become an option. No shell.

**F6 — typed predicates in Python.** Python's `9.0 == 9` and `True == 1` are traps.
- `EXIT_STATUS` accepted only as `type(x) is str and x == "9"` or `type(x) is int and x == 9`.
  Reject bool explicitly.
- `UNIT_RESULT` only `type(x) is str and x == "oom-kill"` (or `"signal"`).
- `_BOOT_ID`, `MESSAGE_ID`, `__CURSOR`: `type(x) is str`.
- Census (jq) and window (Python) must agree; census uses jq `==` which has the same `9.0`
  behaviour. Pin the window to the r15 wording (string `"9"` or number `9`), so `9.0` is
  refused in both. [INFERENCE: jq `9.0 == 9` is true; not re-measured.]

**F7 — bounds and kill semantics.** `--timeout` must kill the whole process group
(`start_new_session=True`, `os.killpg`). `--max-bytes` must stop reading at the cap, not after
buffering. Stderr must be drained with its own cap and never printed. Overflow, timeout, any
stderr byte, and nonzero rc are all `unavailable`. The harness "delay" and "overflow" wrappers
exercise exactly these paths. Without group kill, a delayed wrapper can outlive the tool.

**F8 — cursor API facts that bound FR11.**
- CUR-1: a missing anchor silently seeks to the next entry. Only the exact-first-record check
  detects this. Keep it.
- CUR-2: the API documents that string comparison of cursors is not a reliable identity test,
  and recommends `sd_journal_test_cursor()`. The CLI cannot call that. The window's exact-string
  rule is therefore a fail-closed approximation: equal strings are accepted; different strings
  for the same entry are refused (possible false unavailable). The doc's statement that the
  cursor "identifies a journal entry globally and in a stable way" is what makes equal strings
  acceptable [INFERENCE]. This is the FR11 "cursor-string aliasing" residual in PROVINCE.md:54.
  Record it there. Do not claim identity beyond string equality.

**F9 — trust and access basis.** `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS` are
client-supplied (S015). The window inherits the census trust label: "validated subsets of
client-supplied fields". `-q` may suppress inaccessible-system warnings [CITED], so an rc 0
system-scope window can be partial. The output must say so in `basis`, and must never say
"complete".

## 6. Proposed moves (one bounded proposal, plus rejected alternatives)

**M1 (recommended, admit to L1): standalone window, contract tightened.**
- No census integration. Window output is a separate JSON object with `finding_id`
  `MORI_JOURNAL_WINDOW_OK`/`_UNAVAILABLE`/`_SETUP`. Never `FINDING` lines.
- Rename fields with `window_` prefix (F3) and `entries_after_anchor` (F4).
- End cursor reported as `sha256` only (F5).
- Add `--no-pager`; `--cursor=VALUE` single argv; argparse errors emit JSON (F5).
- Pythonic typed predicates per F6; group kill and capped stderr per F7.
- Add `not_evidence_of_absence=true` and `scope_access=unverified-quiet` to the basis (F9).
- Axes: coverage unchanged (no new claim); calibration improved (names, basis, no absence);
  adjacency unchanged (census bytes unchanged); operability unchanged except fail-closed
  wording. **Harms none. Admit.**

**M2 (candidate, not admitted): bounded-volume filtered window with a separate anchor proof.**
- Add `MESSAGE_ID=fe6faa94…` `MESSAGE_ID=d9b373ed…` `MESSAGE_ID=98e32220…` (same-field OR).
- Add an unfiltered `--cursor=<anchor> -n1` anchor proof that must match exactly before the
  filtered query is trusted (F1).
- Coverage: positive predicate set identical; the filtered stream is a superset of positives.
  Calibration: `class_records_after_anchor` naming required. Adjacency: unchanged.
- Operability: bounds volume, which should reduce overflow-driven unavailability on busy
  journals. Cost: a second journalctl process, which the contract forbids ("Query one scope").
- Harms operability on the cost side. **Not admitted until L1 measures** wall time, overflow
  rate, and anchor-proof reliability on the live host (U2).

**Rejected:**
- Any window→`OOM_KILL_JOURNAL`/`KILL_SIGNAL_JOURNAL` path, or window-driven DRIFT. §3.
- Adding `-b` to the window query (F2).
- Reusing census `positive_*` token names in window output (F3).
- A stored or auto-advanced anchor. Contract forbids it; it would also make window output stateful.
- Salvaging JSON or a failed capture in either surface. r15 rejects it.

## 7. Verification the main agent should run (not run by this seat)

1. `grep -n 'journal-window\|MORI_JOURNAL_WINDOW' tools/mori-census.sh` → must be empty. The
   census must not invoke or read the window.
2. Census selftest and drift comparison unchanged: no new FINDING id, no new census-output
   token, pinned drift red state unchanged, no re-pin.
3. Window selftest fixture cases (isolated CLI subprocess, fake `journalctl` via `--journalctl`):
   - anchor missing / next-closest first record → unavailable (exact-match refusal);
   - empty stdout → unavailable;
   - anchor-only → rc 0, `entries_after_anchor=0`, `not_evidence_of_absence=true`;
   - foreign boot after anchor → unavailable (`boot-mismatch`), not a partial count;
   - `EXIT_STATUS` `9.0`, `true`, `"09"` → not positive; `"9"` and `9` → positive;
   - `UNIT_RESULT` array/`OOM-KILL` → not positive;
   - stdout contains neither raw cursor nor record bytes; end cursor only as sha256;
   - overflow and timeout wrappers kill the child group and return unavailable;
   - argparse error returns JSON with `MORI_JOURNAL_WINDOW_SETUP` on stdout.
4. Harness pins: no window output file name collides with census expected-input digests.
5. Live (L1 only, after integration): one generated anchor from `journalctl -n1 --show-cursor`
   on the current boot, then the window; confirm the first record equals the anchor (U1).

## 8. Unknowns (not measured)

- **U1.** Does `journalctl --cursor` return the anchor entry as the first record on this
  host's journald? S014 does not state inclusion explicitly. If it does not, every window is
  unavailable. Measure once live; do not infer.
- **U2.** Wall time and entry volume for an unfiltered window since a typical anchor on this
  host. Overflow rate under the chosen `--max-bytes`. Not measured here.
- **U3.** Whether a filtered query hides the anchor entry (F1). [INFERENCE from S014 match
  semantics] Measure only if M2 is considered.
- **U4.** Whether vacuum or rate-limit between window and census captures can make W > C
  (case A caveat). Journal rate-limit catalog `e9bf28e6…` is cited in `structured-journal-scopes-r13.md`; not re-read.
- **U5.** Whether equal `__CURSOR` strings always denote the same entry (CUR-2). [INFERENCE]
- **U6.** Whether `jq` `9.0 == 9` behaves as described in F6. Not re-measured.

## 9. Source registration for L1 (not written to SOURCES.md by this seat)

Proposed rows (status `queued` until L1 records quotes and sha256 at its own read):
- `sd_journal_seek_cursor(3)` — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html — quote CUR-1.
- `sd_journal_get_cursor(3)` / `sd_journal_test_cursor(3)` — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_get_cursor.html — quote CUR-2.

Use S014 `--cursor`/`--after-cursor`/`-b`/`--output-fields` anchors already in SOURCES.md
(S014 row). The FR11 frontier line in PROVINCE.md:54 should add "string non-uniqueness (CUR-2)"
to its residual list.

## 10. Summary of this seat's position

- Reject alarm integration. Window counts are anchor-relative validated subsets; census alarms
  are host-at-census-time. The only case where the window adds positives is a failed census
  capture, and even then the output stays a separate observation.
- Admit M1 (standalone, renamed, contract contradictions fixed).
- Hold M2 until live measurement (U1–U3).
- The one non-obvious constraint: do not filter, and do not add `-b`, in the window query.
  Either one silently turns a vacuumed anchor or a reboot into a clean-looking window.
