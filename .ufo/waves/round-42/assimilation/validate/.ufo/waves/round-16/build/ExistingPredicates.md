# ExistingPredicates — r15 production positive predicates and exact catalog IDs

Round 16, seat `MoriR16.ExistingPredicates`. Read-only lane. Report only; no edits to
`tools/`, `corpus/`, fixtures, or another seat's files.

**Question answered:** what exactly does r15 production count as
`positive_kernel_oom` / `positive_unit_oom` / `positive_unit_signal` /
`positive_process_sigkill`, which catalog IDs are exact, and what does that mean for
`tools/mori-journal-window.py` (WindowTool) and the r16 fixture packs.

Confidence: **high** for the predicate guards and IDs (production source lines plus
executive evaluation on both installed JSON parsers). **Medium** for r16 window
pre-gate details (tool is not written yet; contract text only). Unresolved items are
listed at the end.

---

## 1. Observed: exact catalog IDs

`tools/mori-census.sh:1032-1036` (canonical in-repo catalog; comment block `:902-1029`
carries the authority chain S013/S035/S038, QUALITY #15/#16):

| constant | id | meaning | counted by a positive? |
|---|---|---|---|
| `JOURNAL_ID_KERNEL_OOM` | `fe6faa94e7774663a0da52717891d8ef` | kernel-OOM unit notice (“a process of @UNIT@ … killed by the OOM killer”) | yes — `positive_kernel_oom` |
| `JOURNAL_ID_UNIT_FAILURE` | `d9b373ed55a64feb8242e02dbe79a49c` | “Unit failed … result '@UNIT_RESULT@'” | yes — `positive_unit_oom` / `positive_unit_signal` via `UNIT_RESULT` |
| `JOURNAL_ID_UNIT_SIGKILL` | `98e322203f7a4ed290d09fe03c09fe15` | “Unit process exited … EXIT_CODE/EXIT_STATUS” | yes — `positive_process_sigkill` via `EXIT_CODE=killed`, status 9 |
| `JOURNAL_ID_OOMD` | `d989611b15e44c9dbf31e3c81256e4ed` | systemd-oomd per-unit notice | **no** (INFO class only; no positive) |
| `JOURNAL_ID_COREDUMP` | `fc2e22bc6ee647b6b90729ab34a250b1` | coredump notice; also the `COREDUMP_SIGNAL=11` subset | **no** (no positive) |

Corpus cross-check: `corpus/knowledge/structured-journal-scopes-r13.md:42-47` and
`corpus/knowledge/journal-positive-evidence-r15.md:110-113` name the same five IDs.
A sixth catalog id, `1f4e0a44a88649939aaea34fc6da8c95` (“terminated abnormally”), is
documented at `structured-journal-scopes-r13.md:15` but is **not** in the census catalog
and must not be counted. All comparisons are exact 32-lowercase-hex scalar equality —
no prefix, case-fold, trim, or substring (`journal-positive-evidence-r15.md:90-96`).

---

## 2. Observed: the production predicates (r15, landed)

Fallback selectors, verbatim (`tools/mori-census.sh:1052-1055`):

```jq
JOURNAL_JQ_POS_BASE   = select(type == "object")
                      | select((._BOOT_ID | type) == "string")
                      | select(._BOOT_ID == $boot)
                      | select((.MESSAGE_ID | type) == "string")
                      | select(.MESSAGE_ID == $id)
JOURNAL_JQ_POS_KERNEL  = [.[] | BASE] | length
JOURNAL_JQ_POS_SIGKILL = [.[] | BASE
                          | select((.EXIT_CODE | type) == "string")
                          | select(.EXIT_CODE == "killed")
                          | select(((.EXIT_STATUS | type) == "string" and .EXIT_STATUS == "9")
                                or ((.EXIT_STATUS | type) == "number" and .EXIT_STATUS == 9))] | length
JOURNAL_JQ_POS_UNIT    = [ ([.[] | BASE | select((.UNIT_RESULT | type) == "string")
                                     | select(.UNIT_RESULT == "oom-kill")] | length),
                           ([.[] | BASE | select((.UNIT_RESULT | type) == "string")
                                     | select(.UNIT_RESULT == "signal")]   | length) ] | @tsv
```

How they are wired:

- `$boot` is `BOOT_ID_EXPECTED` (file `/proc/sys/kernel/random/boot_id`, dashes/newlines
  stripped, must be exactly 32 chars over `[0-9a-f]`, else empty and the whole journal
  surface is `boot_id=unavailable`; `mori-census.sh:328-336`, `:1348-1353`).
- `$id` is the **class's own** catalog id, passed per query (`:1362`, `:1366`, `:1373`).
- The fallback runs only after a **semantic** aggregate failure
  (`record-invalid|multi-boot|boot-mismatch`) over the same captured bytes
  (`journal_query`, `:1200-1270`; `journal_positive_scan`, `:1124-1146`). A failed
  capture (rc, stderr, timeout, no timeout bin) or an unparseable/structurally-invalid
  aggregate response leaves `JQ_POS_VEC` empty → token `unavailable:<reason>`.
- On a fully valid aggregate, `journal_pos` returns the raw count/split instead
  (`:1308-1327`): kernel ← `jn`, unit-oom ← `ucnt:oom`, unit-signal ← `ucnt:signal`,
  process ← `jn`. So on `js=ok` the positive **equals** the raw value by construction.
- Only three classes set a positive filter: kernel, unit-failure, unit-sigkill
  (`:1362`, `:1366`, `:1373`). oomd/coredump/segfault never set one, so they can never
  feed a positive.
- Emission: surface rows `:1621-1625` (bare, scope-local, plus
  `positive_basis=validated-subset-lower-bound positive_validation=scalar-id+current-boot`);
  OOM finding `:1534` (`user_/system_positive_kernel_oom|unit_oom`, `alarm_basis`, `raw_basis`);
  KILL finding `:1588` (`user_positive_process_sigkill`, `user_positive_unit_signal`);
  all positive keys are in `DRIFT_COUNTER_KEYS` (`:2516-2519`) and therefore magnitude-masked
  by `drift_normalize`.

The four tokens are **record/notice counts**, never victim counts, never summed across
scopes, and never copied into a raw slot. They are not a completeness or authentication
claim (`journal-positive-evidence-r15.md:156-193`).

---

## 3. Field guard truth table (for WindowTool and pack authors)

### 3.1 Identity gates — every captured record

Let `B` = expected boot for the observation (`BOOT_ID_EXPECTED` in r15;
`anchor.boot_id` in r16), `C` = the class id for the token under test.

| # | record state | kernel | unit_oom | unit_signal | proc_sigkill | r16 window effect |
|---|---|---|---|---|---|---|
| I1 | JSON object; `_BOOT_ID` JSON string; `_BOOT_ID == B`; `MESSAGE_ID` JSON string; `MESSAGE_ID == C` | gate passed | gate passed | gate passed | gate passed | valid record (+1 `records_after_anchor`) |
| I2 | not a JSON object (string, number, bool, null, array) | 0 | 0 | 0 | 0 | **rc2 UNAVAILABLE** (whole capture) |
| I3 | `_BOOT_ID` missing / null / number / bool / array / object | 0 | 0 | 0 | 0 | **rc2** (foreign/mismatched boot) |
| I4 | `_BOOT_ID` string but `!= B` (incl. uppercase 32-hex) | 0 | 0 | 0 | 0 | **rc2** |
| I5 | `MESSAGE_ID` missing / null / number / bool / array / object | 0 | 0 | 0 | 0 | valid record, +1, no positive |
| I6 | `MESSAGE_ID` string but a different id (known or unknown) | 0 | 0 | 0 | 0 | valid record, +1, no positive |
| I7 | malformed JSON line, or two objects concatenated on one line | — | — | — | — | **rc2** (malformed capture) |
| I8 | empty stdout | — | — | — | — | **rc2** (anchor unproven) |

`type` here is JSON type, not truthiness: `"9"` is not `9`, `null` is not missing for the
predicate but both fail `type == "string"`, and a JSON `null` value never satisfies the
string guards.

### 3.2 Class-field guards, per token (record already passes I1)

| `MESSAGE_ID` | class field state | kernel | unit_oom | unit_signal | proc_sigkill |
|---|---|---|---|---|---|
| `fe6faa94…` | any / absent / hostile types | **1** | 0 | 0 | 0 |
| `d9b373ed…` | `UNIT_RESULT` string exactly `oom-kill` | 0 | **1** | 0 | 0 |
| `d9b373ed…` | `UNIT_RESULT` string exactly `signal` | 0 | 0 | **1** | 0 |
| `d9b373ed…` | other string: `resources`, `exit-code`, `OOM-KILL`, `Oom-Kill`, `oom-kill `, `signals`, `SIGNAL`, … | 0 | 0 | 0 | 0 |
| `d9b373ed…` | `UNIT_RESULT` missing / null / number / bool / array / object | 0 | 0 | 0 | 0 |
| `98e32220…` | `EXIT_CODE` string `killed` **and** `EXIT_STATUS` string `"9"` | 0 | 0 | 0 | **1** |
| `98e32220…` | `EXIT_CODE` string `killed` **and** `EXIT_STATUS` number `9` | 0 | 0 | 0 | **1** |
| `98e32220…` | `EXIT_CODE` string `killed` **and** `EXIT_STATUS` number numerically `9` (`9.0`, `9e0`, `9.000`) | 0 | 0 | 0 | **1** — divergence, see §5.1 |
| `98e32220…` | `EXIT_STATUS` string `09`, `9.0`, `137`, `15`, `" 9"`; bool `true`/`false`; null; array; object; missing | 0 | 0 | 0 | 0 |
| `98e32220…` | `EXIT_CODE` `Killed`, `exited`, `dumped`, number, array, null, missing | 0 | 0 | 0 | 0 |
| any other string id (`d989611b…`, `fc2e22bc…`, unknown) | any | 0 | 0 | 0 | 0 |
| `MESSAGE_ID` absent or non-string | any | 0 | 0 | 0 | 0 |

Consequences that matter for packs:

- **Class locality is by id only.** A `98e32220…` record carrying `UNIT_RESULT=oom-kill`
  counts nothing; a `d9b373ed…` record carrying `EXIT_CODE=killed/9` counts nothing; a
  `fe6faa94…` record carrying `UNIT_RESULT=signal` counts nothing.
- **`UNIT_RESULT` is a JSON string or it is not evidence.** Numbers, arrays, objects,
  null and missing are excluded from both unit positives — but (r16) they do **not**
  invalidate the window.
- **Subject fields are never read.** `UNIT`, `USER_UNIT`, `_SYSTEMD_UNIT`,
  `_SYSTEMD_USER_UNIT` have no effect on any positive (`journal-positive-evidence-r15.md:186-193`).
- **`EXIT_STATUS` numeric 9 counts; string `"9"` counts; nothing else does** except the
  numeric-equality edge in §5.1.

### 3.3 The anchor-position record (r16 only)

| state | effect |
|---|---|
| first parsed line is an object with `__CURSOR` exactly equal to `anchor.cursor` and `_BOOT_ID` exactly equal to `anchor.boot_id` | accepted, then **dropped**: never counts in `records_after_anchor`, never counts in any positive, even if its `MESSAGE_ID`/class fields match |
| its `MESSAGE_ID` / `UNIT_RESULT` / `EXIT_CODE` / `EXIT_STATUS` absent or hostile | irrelevant — only cursor+boot are checked |
| first line different cursor or different boot | rc2 UNAVAILABLE (anchor unproven / boot boundary) |

Observed in the r16 packs: `ExactAnchor.json` `anchor-only-user-empty-window` and
`KernelUser.json` `kernuser_oom_before_anchor_only` prove the drop (anchor is a
`fe6faa94…` record, expected `positive_kernel_oom: 0`); `KernelSystem.json`
`kernsys_oom_fanout_after_anchor` proves the anchor line need not carry `MESSAGE_ID`.

---

## 4. What WindowTool must implement (predicate side)

1. **Per-record scan, not the r15 aggregate gate.** r16 has no whole-stream aggregate.
   A record that is a JSON object with the anchor boot and a valid unique cursor is a
   valid record regardless of its class fields or `MESSAGE_ID` shape. Class-field
   mismatches set that token's contribution to 0; they do not make the capture
   unavailable. If WindowTool ports the r15 *aggregate* `all(...)` validation instead of
   the fallback predicates, every mixed-stream success case in `TypedFields.json`,
   `UnitSignal.json`, `KernelUser/System.json`, and `UnitOom.json` fails.
2. **Non-string `MESSAGE_ID` does not invalidate.** `TypedFields.json`
   `typedfields_msgid_array_sigkill` / `typedfields_msgid_array_unit_oom` are rc0 cases
   with `records_after_anchor: 1` and all positives 0. Only the predicate's
   `MESSAGE_ID` string equality fails.
3. **Anchor record is dropped before counting.** Check its cursor+boot, then skip it.
   Do not run the positive predicates on it.
4. **Unknown/adjacent known IDs are valid non-counting records.** `d989611b…` and
   `fc2e22bc…` appear after the anchor in success cases and increment
   `records_after_anchor` only (`KernelUser.json` case 4, `KernelSystem.json` case 3,
   `ExactAnchor.json` cases 2-4). Do not require a catalog id on every line.
5. **Do not deduplicate identical bodies.** r15 counts each matching object once, order
   irrelevant, duplicates are separate records (`journal-positive-evidence-r15.md:211`).
   In r16, duplicate *cursors* are the only duplicate that aborts the window (rc2); two
   identical bodies with distinct cursors both count.
6. **Counts are per token and per record.** One record contributes to at most one of the
   four counters. Never sum the four, never reuse a positive as a raw count, never add a
   `total`, never label `positive_unit_signal` as SIGKILL. `positive_*` are notice/record
   counts, not victims, and not a completeness claim.
7. **Success shape.** rc0 + `finding_id=MORI_JOURNAL_WINDOW_OK` + `scope` +
   `records_after_anchor` + the four integer `positive_*` fields + 
   `evidence_basis=validated-record-subsets`. `records_after_anchor` counts every
   validated post-anchor record, so it is ≥ the sum of the four positives.
8. **Any failure is rc2 with no numeric totals.** Nonzero rc, any stderr byte, timeout,
   overflow, truncation, malformed JSON, missing/duplicate/mismatched cursor, foreign
   boot, empty capture → `MORI_JOURNAL_WINDOW_UNAVAILABLE` (or `SETUP` for bad anchor/args),
   `positive_*` absent, never a fabricated 0. This is stricter than r15: r15 excludes a
   foreign-boot sibling and keeps counting; r16 must refuse the entire window.
9. **Never read or echo `MESSAGE`,** and never echo a raw cursor or record. The query's
   `--output-fields` list is the whole field surface; unknown extra fields in a wrapper's
   JSON are ignored.

---

## 5. Traps, divergences, and pack-author guidance

### 5.1 Numeric `EXIT_STATUS: 9.0` — count it, and avoid it in packs

Observed by direct evaluation of the production expressions:

| parser | `9.0 == 9` | `9.0 | tostring` | aggregate `JOURNAL_JQ_SIGKILL` (`tostring == "9"`) | positive `JOURNAL_JQ_POS_SIGKILL` |
|---|---|---|---|---|---|
| `/usr/bin/jq` jq-1.8.2 | true | `"9.0"` | `record-invalid` | **1** (numeric branch) |
| jaq 3.1.1 (the `jq` shell function in this session) | true | `"9.0"` | `record-invalid` | **1** |

So the production positive predicate accepts any JSON number numerically equal to 9
(`9`, `9.0`, `9e0`) while the r15 aggregate rejects a float because of its `tostring`
guard. This is asymmetric by design of the two selectors, not a window bug.
The r15 **harness oracle** rejects floats (`tools/mori-round15-regressions.py:255-268`,
`status_is_9`: bool/float/array/null rejected), so an author reasoning with the r15
oracle would expect 0 where the production predicate gives 1.
**Guidance:** packs should use `"9"` or integer `9`. If a `9.0`/`9e0` case is added
deliberately, the expected `positive_process_sigkill` is **1** (production predicate),
not the oracle's 0.

### 5.2 Exact-match traps

- `MESSAGE_ID` array (`["98e32220…"]`), uppercase, prefix, or whitespace-padded → no
  positive. It is still a *valid* r16 record; only the count is 0.
- `_BOOT_ID` uppercase or 31/33 chars → never equals a valid anchor (which is validated
  as 32 lowercase hex). In r16 this is rc2, not a 0.
- `UNIT_RESULT` `"oom-kill "` (trailing space), `OOM-KILL`, `oom_kill`, `signals`,
  `SIGNAL` → 0. The vocabulary spelling is fixed by S038
  (`structured-journal-scopes-r13.md:42-47`; `journal-positive-evidence-r15.md:118-125`).
- `EXIT_CODE` must be the string `killed`; `EXIT_STATUS` `"09"`, `"9.0"`, `"137"`,
  `"15"` → 0.
- Missing and explicit `null` behave the same for class guards (both fail
  `type == "string"`). Do not rely on `null` to mean "absent" differently.
- Duplicate JSON keys in one line: JSON parsers keep the last occurrence; avoid.
- JSONL only: one object per line. A top-level JSON array, a blank line, or concatenated
  objects is malformed capture → rc2 in r16 (r15 would see a non-object/parse failure).

### 5.3 Pack recipe (aligned with the existing drafts)

- Anchor object exactly `{schema:"mori-journal-anchor-v1", scope:<same as case>,
  boot_id:32-lowercase-hex, cursor:printable scalar ≤4096, no controls}`. Wrong scope,
  uppercase or short boot → rc2 `SETUP` (`AnchorValidation.json`).
- `stdout` line 1: the anchor record, `__CURSOR` byte-equal to `anchor.cursor`,
  `_BOOT_ID` equal to `anchor.boot_id`; other fields optional (`KernelSystem.json`
  fanout anchor has only cursor+boot).
- Lines 2..N: JSON objects, each `_BOOT_ID` equal to the anchor boot, each `__CURSOR`
  a unique valid scalar — never the anchor cursor and never repeated
  (`CursorShape.json`, `MissingAnchor.json`, `BootBoundary.json`, `RecordShape.json`).
- Do not include `MESSAGE` in fixture records (r15 harness bans it, `:252-260`; the r16
  goal is MESSAGE-free).
- For rc0 cases, set `want.records_after_anchor` = number of validated post-anchor lines
  and each `positive_*` per §3.2; `evidence_basis` is `validated-record-subsets`.
- For rc2 cases, omit numeric wants; `want_id` is `MORI_JOURNAL_WINDOW_UNAVAILABLE`
  (or `..._SETUP` for anchor/argument problems).
- Keep each case single-scope. A user-scope window may hold records with no
  `USER_UNIT`; subject fields are irrelevant to every positive.

### 5.4 Consistency of the drafts that exist now (static review only)

Every predicate-sensitive success case currently in `round-16/fixtures/` matches the
table in §3.2. Spot checks: `ProcessSignal.json` case 1 (killed/"9" counts; "15",
exited/"9", killed/"137" do not) → 1; case 2 (numeric 9 counts; `["9"]`, null do not)
→ 1; `TypedFields.json` (MESSAGE_ID array, `EXIT_STATUS:true` → 0; false + `"9"` → 1);
`UnitOom.json` (exact `oom-kill` vs `OOM-KILL`/`Oom-kill`/missing/`resources`);
`UnitSignal.json` (`signal` vs `9`/`["signal"]`/`signals`/`SIGNAL`);
`KernelUser/System.json` (adjacent ids and anchor-position class matches → 0).
No pack currently uses a float status, so §5.1 is latent, not active.

---

## 6. Remaining unknowns / ownership

- **Missing at read time (explicit).** `tools/mori-journal-window.py` and
  `tools/mori-round16-regressions.py` do not exist yet; no delivered code was reviewed
  here. This report is source/contract evidence and a predicate truth table only; the
  r16 harness and window tool behavior remain unverified until wave2 reviews delivered
  code. No tool existence was awaited or polled.
- **Window query match words are not pinned in the interface.** It is unknown whether
  WindowTool will query only the three positive ids, all five catalog ids, or an
  unfiltered cursor range. The predicate table is valid either way, but the tool must
  tolerate adjacent known ids in the stream (packs already require it). Owner:
  WindowTool; reviewer: ReviewCLI.
- **Record-cursor validity beyond “valid scalar”.** The anchor constraint is explicit
  (printable scalar ≤4096, no controls); the per-record cursor rule is only
  “valid scalar … unique”. [INFERENCE] the same shape is intended. Pack authors should
  use realistic `s=…;i=…;…` or plain printable tokens and avoid empty strings, controls,
  and repeats.
- **Duplicate-key JSON and 9.0** are producer-defect edges, not realistic journalctl
  emissions; they are trap fixtures only.
- r15's positive tokens are in `DRIFT_COUNTER_KEYS` (`:2516-2519`), so census drift masks
  their magnitudes. The r16 window is a separate observable; its output must not be
  normalized or pinned against the old census drift baseline. [INFERENCE] L1 owns the
  drift/re-pin decision; this seat makes no pin claim.

---

## 7. Disclosure (per L1 no-checks clarification)

- No live `journalctl` call, no journal read, no measurement loop, no test/gate/build/
  formatter/smoke run, no tool install, no `/tmp` use, no commit.
- Static review only: `tools/mori-census.sh`, `tools/mori-round15-regressions.py`,
  `corpus/knowledge/journal-positive-evidence-r15.md`,
  `corpus/knowledge/structured-journal-scopes-r13.md`, `corpus/knowledge/kill-classes-by-message-id-r12.md`,
  and the current `round-16/fixtures/*.json` drafts.
- Two local JSON-parser evaluations were run to confirm guard semantics on literal
  JSON (no journal access, no file writes): the production jq expressions under
  `/usr/bin/jq` 1.8.2 and under `jaq` 3.1.1 (the session's `jq` shell function). These
  are **not** SUT verification and are inadmissible as tool behavior evidence; they only
  ground §3.2/§5.1. Also disclosed: one `sed` read of `mori-round15-regressions.py` was
  auto-backgrounded by the harness during an interjection and then killed — repo static
  read only, no live data.

Report: .ufo/waves/round-16/build/ExistingPredicates.md
