# Round 16 — ClaimRubric: proposed finite C1 metric and no-harm rubric

Seat: `MoriR16.ClaimRubric` (leaf author-lane member; no subagent dispatch; no outside verification claimed).
Claim under rubric: **C1 coverage** — bounded, MESSAGE-free, same-boot new-since-anchor journal window (`tools/mori-journal-window.py`), FR11 advanced only for exact retained cursor continuity.
Entering revision: `b83edc6ee3db6822382ab673d7e6e984e420f22f` (HEAD, verified). Working tree at read time had uncommitted sibling edits to `LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/SOURCES.md` (round-16 text, S039 row); those are cited as in-flight, not as committed evidence. Nothing in the tree was modified by this seat.
Scores: **none pre-awarded**. Held entering scores per `SCORECARD.md` round-15 row: coverage **6** (owned, lowest), operability **7** (owned), depth 5, freshness 5, calibration 5, adjacency 6.

Tooling: no install or update by this seat. Used pre-existing `curl`, `sha256sum`, `git`, `grep`; no `/tmp` files written; no journal, cursor, census, selftest or gate executed.

---

## 1. Axes named

| Axis | Entering | Role in this claim | What may move it | What may not |
|---|---|---|---|---|
| coverage | 6 (owned, lowest) | the claim axis | fixture-proven, measured FR11 continuity capability with refusal coverage | a fixture count alone; live zero read as absence; victim/emitter/completeness language |
| operability | 7 (owned) | must not drop | none claimed | any census/selftest/oracle/regression count change, new census finding ids, cursor-state writes |
| depth | 5 | held | primary-source grounding of cursor/field predicates | new depth claim |
| freshness | 5 | held; old r10 drift pin **stays red** | none | re-pinning the r10 baseline; reporting drift exit 1 as green |
| calibration | 5 | held | explicit unavailable-versus-zero and subset-versus-total labels | pre-awarded points; "outside verified" wording from author seats |
| adjacency | 6 | held | read-only, no dispatch/OS actuation | `--rotate`, `--vacuum-*`, `--flush`, `systemctl`, `pacman`, `--cursor-file`, `--after-cursor` |

Move rule applied: keep a move only if it raises coverage and leaves every other axis at its entering value by a measured check (§5).

---

## 2. Primary sources opened this round

Opened 2026-10-20. Byte digests were taken with `curl -fsSL <url> | sha256sum` (piped, nothing written to disk).

| Source | Digest (raw bytes, this round) | Fact used | Matches r15 note? |
|---|---|---|---|
| S014 journalctl(1), systemd 262 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | `75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722` | `--cursor=` "Start showing entries from the location in the journal specified by the passed cursor"; `--after-cursor=` (not used here); `--cursor-file=` writes the last cursor to FILE at exit (**forbidden**: a cursor-state write); `--show-cursor` "format of the cursor is private and subject to change"; `--output-fields=`: `__CURSOR` and `_BOOT_ID` always printed for json; `--quiet`, `--no-tail`; `--vacuum-*` removes archived files; `--rotate` archives active files; json: "Journal entries permit non-unique fields…" arrays, >4096-byte fields → null, non-UTF-8 → numeric arrays | yes (digest identical to `corpus/knowledge/journal-positive-evidence-r15.md:1`) |
| S015 systemd.journal-fields(7) — https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | `906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7` | `MESSAGE_ID=` lowercase 128-bit hex typed key; `UNIT=`/`USER_UNIT=` client-supplied subject metadata; `_BOOT_ID=` trusted; "`__CURSOR`: a cursor is an opaque text string" | yes |
| S039 (uncommitted sibling row) sd_journal_test_cursor(3) / sd_journal_seek_cursor(3) — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html ; …/sd_journal_seek_cursor.html | test page `5ada44c28aa31dc7495276e2bf6a11a3370e33ae71277051736641882e5e9980`; seek page `b13d9928c1ea07a6a75dfe80d2227405c1f3ea6ac5b708219bef44fe15f6cd7b` | **Verified quotes:** "the same entry might be referred to by multiple different cursor strings" (test page, Description); "The cursor string should be considered opaque and not be parsed by clients" (get/test pages); "If no entry exists that matches exactly the specified seek address, the next closest is sought to." (seek page) | new this round |
| S038 service.c `service_result_table` at `cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af` — raw GitHub | (grep recheck, not digested) | lines 6594 `[SERVICE_FAILURE_SIGNAL] = "signal",` and 6598 `[SERVICE_FAILURE_OOM_KILL] = "oom-kill",` reproduced | yes |

Consequences for the metric (these are grounded, not inferred):

- **Silent-seek risk [INFERENCE].** The seek-to-next-closest behavior is documented for the C API (S039), not for the `journalctl --cursor` CLI, whose manual is silent on an absent cursor. A cursor that was rotated or vacuumed away might therefore yield exit 0 starting at a *later* entry, or an exit-1 error, or empty output. The window must fail closed on all three; the metric must have one case for each.
- **Identity is byte-level only [OBSERVED in S039].** Different strings may name one entry, so exact-byte equality of the first record is a conservative gate: it can refuse a valid anchor (safe), and it does not prove the journal has not re-encoded the entry. No cursor deduplication or aliasing claim may be drawn.
- **Opacity.** Cursors must be compared as bytes and never parsed. The metric must include a case where the cursor bytes differ only cosmetically (e.g., trailing space) and must be refused.
- **Empty means ambiguous.** Because the anchor entry itself is returned as the first record, an rc 0 stream with zero records (or only the anchor) is the only valid zero. Empty stdout cannot distinguish "no new records" from "anchor vanished", so it is unavailable.

---

## 3. Proposed finite C1 metric

### 3.1 Unit and counting

Pack set: **N = 38 committed case families** (§3.2) under `.ufo/waves/round-16/fixtures/`, one JSON pack per topic, pinned with `--pin-fixtures` before any run and checked against the normal `--expected` path. Each case runs the production CLI as a subprocess with a per-case `journalctl` wrapper (`MORI_…`/`--journalctl PATH`), never a function stub.

Two counts, reported side by side:

- **F — failed cases:** number of the N cases with at least one failing assertion. **Primary.** Expected-zero at delivery.
- **A — failed assertions:** total failing assertions across all cases. **Diagnostic.** Expected-zero at delivery; prevents one case with many checks from hiding behind another.

Entering baseline (capability absent, per harness contract): every case is recorded `capability_absent`, so **F_entering = N = 38** and **A_entering = total assertions (recorded, not a production-bug count)**. This number is capability red, not a historical production defect count; it must never be written as "38 bugs fixed".

Claimed movement, if and only if measured: **F: 38 → 0** and **A: all → 0**, with the same pack digests, same expected table and same harness digest at both revisions.

### 3.2 Case families (fixed IDs; each is one pack case)

Positive/valid (`want_rc=0`, `want_id=MORI_JOURNAL_WINDOW_OK`):

| ID | Stream (conceptual) | Exact expectation |
|---|---|---|
| S01 | anchor record only, same boot | records_after_anchor 0; four positives 0; rc 0 (the only valid zero) |
| S02 | anchor + 3 ordinary same-boot records, no class match | records 3; positives 0 |
| S03 | kernel OOM notice `fe6faa94…`, valid identity, no UNIT fields | positive_kernel_oom 1; others 0 |
| S04 | unit OOM `d9b373ed…` with `UNIT_RESULT="oom-kill"`, UNIT/USER_UNIT absent | positive_unit_oom 1; unit_signal 0 |
| S05 | unit `d9b373ed…` with `UNIT_RESULT="signal"`, UNIT as array | positive_unit_signal 1; unit_oom 0 |
| S06 | process `98e32220…` with `EXIT_CODE="killed"`, `EXIT_STATUS="9"` | positive_process_sigkill 1 |
| S07 | same valid OOM record duplicated ×2 | positive_unit_oom 2; records 2 (duplicates not deduplicated) |
| S08 | S04 and S05 in reversed order | same counts as forward order |
| S09 | unit records with `oom_kill`, `OOM-KILL`, `resources`, `UNIT_RESULT` null/array | all four positives 0; records counted |
| S10 | system-scope kernel OOM, user scope empty | positive_kernel_oom 1 in system; user 0 |
| S11 | user-scope positives while system scope empty | scope isolation: system 0 |
| S12 | valid positive plus a same-boot object whose `MESSAGE_ID` is an array | **decision required (§4 A1)**; pin the chosen reading |
| S13 | producer emits extra `MESSAGE` field despite `--output-fields` | rc 0; stdout does not echo the field or any record bytes |
| S14 | `EXIT_STATUS` as JSON integer `9` rather than string `"9"` | **decision required (§4 A2)**; pin the chosen reading |

Refusal/setup (`want_id` per row):

| ID | Condition | Expected |
|---|---|---|
| R01 | anchor path missing | rc 2, MORI_JOURNAL_WINDOW_SETUP |
| R02 | anchor not JSON | SETUP |
| R03 | schema not `mori-journal-anchor-v1` | SETUP |
| R04 | anchor scope ≠ `--scope` | SETUP |
| R05 | boot_id 31 chars, uppercase, or non-hex | SETUP |
| R06 | cursor empty, >4096 bytes, or contains a control character | SETUP |
| R07 | cursor non-string (array/null/number) | SETUP |
| R08 | `--timeout` or `--max-bytes` non-numeric/negative | SETUP |
| R09 | `--journalctl` path absent | rc 2, MORI_JOURNAL_WINDOW_UNAVAILABLE, reason producer-missing |
| R10 | journalctl rc 1 (cursor not found, modeled) | UNAVAILABLE |
| R11 | journalctl rc 5 | UNAVAILABLE |
| R12 | journalctl rc 137 | UNAVAILABLE |
| R13 | journalctl rc 124 | UNAVAILABLE |
| R14 | wrapper delays past `--timeout` | UNAVAILABLE, bounded by timeout |
| R15 | rc 0, stderr bytes > 0 | UNAVAILABLE; stderr not echoed |
| R16 | rc 0, `--max-bytes` overflow | UNAVAILABLE |
| R17 | rc 0, empty stdout | UNAVAILABLE (no anchor seen) |
| R18 | rc 0, first record cursor ≠ anchor (silent seek to a later entry) | UNAVAILABLE, reason first-cursor-mismatch |
| R19 | first record exact cursor but foreign boot | UNAVAILABLE |
| R20 | later record foreign boot | UNAVAILABLE |
| R21 | later duplicate cursor (including a second copy of the anchor) | UNAVAILABLE |
| R22 | later non-object line | UNAVAILABLE |
| R23 | later record cursor missing or non-scalar | UNAVAILABLE |
| R24 | malformed JSONL line (truncated) | UNAVAILABLE |
| R25 | valid positive plus adjacent foreign-boot record | UNAVAILABLE; **no positive emitted** (no salvage in this round) |
| R26 | cursor differs from anchor only by trailing space | UNAVAILABLE (opacity: bytes, not normalized) |
| R27 | anchor-cursor byte-equal but `_BOOT_ID` array at the first record | UNAVAILABLE |
| R28 | `MESSAGE` present as an array in a *refusal* stream (rc 1 plus stderr) | UNAVAILABLE; MESSAGE not read |

Harness assertions applied to **every** case (counted in F and A):

- **H1 argv exact.** Argv contains `--cursor=<anchor>` (not `--after-cursor`), `--no-tail`, `--quiet`, `--output=json`, `--output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`, exactly one scope flag. Argv contains no `MESSAGE=` match, no `--cursor-file`, no `--after-cursor`, no `--rotate`, no `--vacuum-*`, no `--flush`, no `--boot`/`--since`/`--until`, no `--directory`/`--file`/`--merge`.
- **H2 no echo.** stdout parses as one JSON object; the anchor cursor string does not occur in stdout or the tool's stderr; no record key other than the safe SHA-256 of the anchor appears.
- **H3 finding id and reason.** rc 0 ⇒ `finding_id=MORI_JOURNAL_WINDOW_OK` and no unavailable reason; rc 2 ⇒ UNAVAILABLE or SETUP as listed, with a stable reason from a fixed enumerated set (pinned per case, not regex-matched).
- **H4 no state write.** Anchor file digest unchanged; the fixture directory listing unchanged; no `*.cursor`/state file created; anchor never advanced.

### 3.3 Required coverage (C1 eligibility, proposal only)

The point decision belongs to L1 and the outside closure, not this seat. Proposed necessary conditions, all measured:

1. F = 0 and A = 0 at delivered revision, same pack/expected/harness digests as entering.
2. Each positive family S03–S06 passes **with exact integer counts**, not only rc 0.
3. Each of the discriminating refusals R18, R19, R20, R25, R26 passes with its exact reason. These are the FR11 continuity discriminators; a cut-down suite without them does not count.
4. Entering run recorded `capability_absent` for every case with receipts; delivered run records `pass` with subprocess receipts.
5. Input digests (tool, every pack, expected table, journalctl wrapper per case) and actual git HEAD plus exact porcelain are persisted, and the harness refuses to run on moving inputs.
6. No-harm rubric (§5) holds.

Fixture-only success is **capability acquisition**, not live coverage. Any live read-only measurement (for example, `journalctl -n1 --show-cursor` as a read-only anchor source followed by two bracketed windows) is L1-owned, must be labeled separately, and cannot prove completeness, victims, emitters or ordering. The r13 precedent used live evidence for a coverage point; this rubric recommends L1 decide whether one bracketed live read is required before any point, and it must not be run by a seat.

### 3.4 Counting commands (proposed; manifest schema is a harness deliverable, not existing)

Proposed run-manifest fields: `cases[].id`, `cases[].status` ∈ {`pass`,`fail`,`capability_absent`}, `cases[].assertions[]{name,expected,actual,pass}`.

```sh
# F (primary): cases with any failing assertion or absent capability
jq '[.cases[] | select(.status != "pass")] | length' .ufo/waves/round-16/evidence/<run>/run-manifest.json
# A (diagnostic): failing assertions
jq '[.cases[].assertions[] | select(.pass == false)] | length' .ufo/waves/round-16/evidence/<run>/run-manifest.json
```

Expected at delivery: `0` and `0`. Expected at entering: `38` and the recorded assertion total.

---

## 4. Spec ambiguities to resolve before fixtures are frozen

These are not closed by the shared contract or by the primary docs; each needs one pinned reading and one case per reading.

- **A1 — later same-boot record with array/missing `MESSAGE_ID`.** The contract's validity list for later records is object + same boot + unique scalar cursor; it does not invalidate the window on MESSAGE_ID shape. *Proposed reading:* counted in `records_after_anchor`, contributes to no positive, does not make the window unavailable. Alternative (stricter): unavailable. Pin one; S12 expects the chosen one.
- **A2 — `EXIT_STATUS` integer `9` versus string `"9"`.** S014 says json encodes fields as strings. r15 wording reads "scalar equal to 9 (journalctl's normal encoding is the string "9")". *Proposed reading:* exact JSON string `"9"` is the positive; integer `9` is not positive (conservative, avoids a type-coercion claim). Pin one; S14 expects it.
- **A3 — cursor inclusive or exclusive.** S014 wording ("Start showing entries from the location … specified by the passed cursor") supports inclusive, consistent with "drop the first record". Either way the first-record exact check fails closed; the fixture set must still include R18 so that a silent seek is seen as unavailable, whichever way the CLI behaves.
- **A4 — absent field representation.** S014 does not say whether a field absent from a record is omitted or null in json output. *Proposed:* treat omitted and null as absent for positive predicates; include one case with each (S04 variant) so the reading is pinned by fixture, not inferred.
- **A5 — missing journalctl binary versus missing cursor.** Both lead to unavailable with different reasons (R09 versus R10); the expected reason per case must be fixed, not matched by regex.

---

## 5. No-harm rubric (per axis, measured, not asserted)

Checks are *run by L1 after both waves settle*; this seat runs none. Expected values are the entering values.

| Axis | Check | Expected | Source of pin |
|---|---|---|---|
| operability | census SHA `tools/mori-census.sh` at delivery | `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7` (equal to entering) | verified now at HEAD |
| operability | `git diff --quiet b83edc6 -- tools/mori-census.sh` | exit 0 (census untouched; new CLI is not a census surface) | git |
| operability | census selftest | 113/113 (`census-selftest.json`) | r15 receipt |
| operability | silence oracle | 28/28 | r15 receipt |
| operability | r13 regressions | 24 pass + 2 mutation-red | r15 receipt |
| operability | r14 regressions | 44/44 | r15 receipt |
| operability | r15 regressions selftest | PASS (full) | r15 receipt; harness SHA `6a55c33c…` |
| operability | census FINDING ids | unchanged; no new `SURFACE` or `FINDING` id from the window tool | grep of census output keys |
| coverage (no-harm to its own axis) | positive families S03–S06 retain exact counts | pass | §3.2 |
| depth | new depth claims | none; sources S014/S015/S039 cited as predicates only | §2 |
| freshness | `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json` | **exit 1 (red), unchanged**; baseline bytes unchanged; no `--pin` invocation | r15 `drift-current.json` (exit 1) |
| freshness | live census exit | recorded; not promoted to green | r15 `live-census.json` (exit 1) |
| calibration | output language | every positive labeled "validated-record subset"; no total, victim, emitter or completeness wording in stdout | §3.2 H2 |
| adjacency | forbidden surfaces in new CLI | `grep -cE 'systemctl|pacman|--rotate|--vacuum|--flush|--cursor-file|--after-cursor|systemd-cat' tools/mori-journal-window.py` = 0 (comments exempt only if the grep excludes `#` lines, pinned in harness) | static |
| security/no-echo | raw cursor and records | absent from stdout/stderr in every case | H2 |
| state | cursor/anchor writes | none; anchor digest unchanged | H4 |

Any single failing row is harm, regardless of the coverage metric. A new drift reason, a changed census byte, or a census selftest count change is harm, not a footnote.

---

## 6. Residuals (kept visible; not claimed away)

- **FR11 cursor rotation/vacuum:** [UNKNOWN] how `journalctl --cursor=` reports an absent cursor; not measured live. Fail-closed by R10/R17/R18 regardless of which behavior occurs.
- **Silent seek:** [INFERENCE] from S039's C API seek behavior; CLI behavior undocumented in S014.
- **Cursor aliasing (S039):** byte-equality is conservative; no equivalence, dedup or cross-boot ordering claim. Cross-boot ordering stays [UNKNOWN].
- **Field encoding:** absent versus null (A4); `>4096`-byte fields become null (S014), which can hide a positive field; treated as not positive.
- **Authenticity:** `MESSAGE_ID`, `UNIT_RESULT`, `EXIT_CODE`, `EXIT_STATUS`, `UNIT`, `USER_UNIT` are client-supplied (S015). Any process that can write the journal can forge a positive. No emitter authentication.
- **Victims and causation:** a positive is a record witness; kill counts are not victim counts; `positive_unit_signal` does not prove signal 9 or a sender; OOM_CONTINUE can leave no record.
- **Completeness:** retention, rate-limit loss, unreadable scopes and events without structured records remain outside every count.
- **Live behavior:** not measured by this seat; a fixture pass does not establish current-host retention or service health.
- **Drift:** `baseline-r10-20261015T2231Z.json` remains red (exit 1 at r15 and at the entering revision). Preserved, not re-pinned; no semantic review has justified a new baseline.
- **Stale active registry (routed from r15, still present):** `SKILL.md:134` (r15 gate row) says `--no-frozen-control` "is selftest-internal and requires the hidden `--selftest-child`". Delivered `tools/mori-round15-regressions.py` refuses that flag per r15 `control-bypass-refused.json` (exit 2). The active-registry sentence must be corrected in a lane-authored commit; `build/SkillInterface.md:88` is historical draft and must not be rewritten.

---

## 7. Round-15 non-author feedback that this round must carry (append-only)

From `corpus/lessons/round-15-verifier-spotcheck.md`, not rewritten here:

1. Append a correction to M4 assigning L1 responsibility for the omitted wave-context broadcast restriction; keep the violation recorded (zero `agent://` tokens in the r15 spec/dispatch).
2. Append the omitted outside-lane instance to procedural debt: `build/HarnessBuild.md:248–267` `--pin-fixtures /tmp/mori-r15-expected-probe-final.json` write (in addition to `RegistryFrontier:63–72`).
3. Append a correction to M6/mid-flight: implementing subprocess selftest arms is not permission to execute them; `report:301–307` justification was wrong; early seat results are not admissible verification.
4. Correct the active registry (`SKILL.md:134`, §6) in a lane-authored commit with a lesson-backed disposition.
5. Keep the r10 drift pin red and unreviewed; keep victim/authentication/access/retention qualifications on every positive.

This seat does not perform these edits (out of its write scope).

---

## 8. Findings summary (for L1)

- The metric is **F: 38 → 0** over fixed case families, with **A** as diagnostic, measured by the same committed packs and digests at entering and delivered revisions. Entering red is capability absence, not a production count.
- Four spec ambiguities (A1, A2, A4, A5) and one inclusive/exclusive reading (A3) need pinned decisions before fixture freeze. A1 and A2 change expected outputs of two success cases.
- Two refusals are the FR11 discriminators: silent seek (R18) and foreign-boot first record (R19). Without them, a window that drops the anchor check would still pass the other rows.
- The no-harm rubric is mechanical: census bytes, selftest counts, drift exit 1, forbidden-surface grep, and no state writes. Any single failed row is harm.
- Residuals: cursor vacuum/rotation behavior, cross-boot ordering, cursor aliasing, authenticity, victims, completeness, live behavior, r10 drift red.

Read/verified this round: S014, S015, S039 (uncommitted row), S038 line grep; census and harness SHA-256; SCORECARD round 15 and 16 text; `journal-positive-evidence-r15.md`; `round-15-verifier-spotcheck.md`; `SKILL.md:134`; `LOG.md` round-16 entry. Executed: `curl|sha256sum`, `git` read-only status/diff/rev-parse, `grep`/`sed`/`sha256sum` on repo files. Not executed: census, selftests, regression harnesses, journalctl queries, any builds, tests or formatters.
