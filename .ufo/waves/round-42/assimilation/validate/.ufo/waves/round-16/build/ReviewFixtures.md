# ReviewFixtures — round-16 fixture id / rc / stable-id consistency

Lane: MoriR16.ReviewFixtures (reviewer, leaf). Read-only except this report.
Target: /home/vgpnk/Projects/shokunin/mori-shokunin
Method: static reads only. No fixture, tool, harness, or selftest was executed. No subagents were spawned.
Tooling: none installed or updated.

## 0. Read-time state (explicit; changes may be in flight)

At read-time, against the working tree as found:

- `.ufo/waves/round-16/fixtures/` does NOT exist. Zero of the 16 spec-named packs
  (ExactAnchor, KernelUser, KernelSystem, UnitOom, UnitSignal, ProcessSignal,
  MissingAnchor, BootBoundary, CursorShape, RecordShape, MalformedCapture,
  ProducerFailure, Stderr, Bounds, TypedFields, AnchorValidation) are on disk.
- `tools/mori-journal-window.py` does NOT exist.
- `tools/mori-round16-regressions.py` does NOT exist.
- `tools/mori-round16-context-check.py` does NOT exist.
- `.ufo/waves/round-16/build/` contains only `swarm-registry.json` before this report.
- `tools/mori-census.sh` exists and is the catalog-ID source of truth for this review.

Consequence: I cannot verify any fixture case's id, `want_rc`, `want_id`, or `want`
fields. Everything below is spec-level and source-level consistency, not a
review of authored cases. Re-run this review once the packs land.

## 1. Findings by severity

### HIGH-1 — Wrong unit-failure catalog ID in two pack prompts

- Where: `.ufo/waves/round-16/wave1-spec.json` items `PackUnitOom` and `PackUnitSignal`
  (and the matching `wave1-dispatch.json` / `wave1-task-response.json` copies).
  The prompt says: "unit-failure `d9b373ed55a64e6c8e2e7d70a0fce472`".
- Ground truth: `tools/mori-census.sh:1036` defines
  `JOURNAL_ID_UNIT_FAILURE=d9b373ed55a64feb8242e02dbe79a49c`. The r15 fixture
  `.ufo/waves/round-15/fixtures/UnitUser.json` uses the same `...feb8242e02dbe79a49c`.
  The census doc `CensusFix.md` and `CountDesign.md` also use `...feb8242e02dbe79a49c`.
- `d9b373ed55a64e6c8e2e7d70a0fce472` appears nowhere in the repo except the round-16
  prompts (grep, whole tree, gitignore off).
- Why it matters: the r15 predicate `positive_unit_oom` is keyed on the unit_failure
  record set (census line ~977 "d9b373ed records with UNIT_RESULT exactly oom-kill").
  A fixture built from the prompt's ID is not a faithful unit-failure fixture:
  - If the new window tool matches the full 32-hex ID exactly, the case expecting
    `positive_unit_oom=1` FAILS for a non-bug reason.
  - If it matches an 8-char prefix, the case passes for the wrong reason.
  - A "wrong case" negative built from the bogus ID would test nothing.
- Fix: correct both prompts to `d9b373ed55a64feb8242e02dbe79a49c`. Require every
  authored case to use only IDs present in `tools/mori-census.sh` (add a harness
  check that each `MESSAGE_ID` used in the "exact" arm is in the
  `JOURNAL_ID_*` set).

### HIGH-2 — Expected rc/id for "record present but MESSAGE_ID non-scalar" is undefined

- Where: spec `Interface` says every later record must be "object, same boot and
  unique valid scalar cursor"; malformed capture → rc2 UNAVAILABLE. It does not say
  whether a *cursor-valid, same-boot* record whose `MESSAGE_ID` is an array, object,
  bool, or missing is (a) an UNAVAILABLE malformed capture, or (b) a valid record that
  simply contributes 0 to every positive counter.
- Affected packs: TypedFields ("array MESSAGE_ID ... never positive"), RecordShape
  ("primitive JSON neighbors and JSON arrays"), KernelSystem/KernelUser/UnitOom
  ("neighbor" arms), and any pack with a non-scalar neighbor.
- Why it matters: the two readings give different `want_rc` and `want_id` for the same
  stdout. The r15 precedent (`UnitUser.json`, `unituser_msgid_array_retains_valid_oom`)
  retains the valid positive and does NOT blank the class, but that is r15 census
  semantics, and the window spec says "no numeric positive totals" on malformed capture.
  An author cannot know which to pin.
- Fix: pin the rule in the spec before authoring. Recommended: a non-scalar MESSAGE_ID
  or EXIT_STATUS on a valid-cursor, same-boot record is a non-positive record (counted in
  `records_after_anchor`, contributes 0 to positives), rc0 OK. Anything that breaks
  object shape, cursor scalar, or boot is rc2 UNAVAILABLE. Then the TypedFields and
  RecordShape `want` fields are determinable.

### MEDIUM-1 — Anchor fixture shape cannot express the anchor file

- Spec: CLI takes `--anchor PATH`. Fixture contract: `"anchor": {...}` is a JSON object.
- Gap: the harness must serialize the object to a file. It cannot express:
  - a non-object anchor (array, string, number);
  - invalid JSON bytes (truncated, trailing junk) — needed by AnchorValidation ("malformed anchor boot");
  - a missing anchor file (the MissingAnchor topic is actually journal-output, not the file).
- Pin: add an `anchor_raw` (string, written verbatim) alternative, or state that
  AnchorValidation may only use object-level malformations. Also pin the expected id for
  each: missing file, unreadable file, invalid JSON, non-object, bad schema, bad scope,
  bad boot, bad cursor. Spec says "setup invalid anchor/args -> SETUP", which covers
  these, but says nothing about the *missing file* explicitly.

### MEDIUM-2 — Scope duplicated between case and anchor; mismatch expectation implicit

- Each case has top-level `"scope"` and `anchor.scope`. The AnchorValidation topic
  "scope mismatch" needs an expected id. The spec implies SETUP ("invalid anchor/args")
  but never states it.
- Pin: `case.scope != anchor.scope` → rc2 `MORI_JOURNAL_WINDOW_SETUP`. Then harness rule:
  every case must have `want_id = SETUP` iff setup-invalid.

### MEDIUM-3 — "stderr-bearing success" wording contradicts the contract

- Where: PackStderr prompt: "stderr-bearing success including secret-shaped canary".
- Contract: "Malformed/empty capture, ..., nonzero rc, stderr, timeout, overflow -> rc2 unavailable".
- Risk: an author reads "success" and writes `want_id=OK`. Under the contract, a
  stderr-bearing run is `UNAVAILABLE`, rc2, with no positive totals.
- Fix: rewrite the PackStderr topic as "stderr-bearing refusal". Harness check: any case
  whose `stderr` is non-empty must have `want_rc=2` and `want_id=UNAVAILABLE`.

### MEDIUM-4 — Bounds fixtures depend on undefined defaults

- Spec: `--timeout SECONDS` and `--max-bytes N` have no stated defaults. `timeout:true`
  and `overflow:true` are "wrapper delay/overflow with expected rc2", but the byte or
  second threshold they must cross is not in the fixture schema.
- Fix: require each Bounds case to pass explicit `--timeout` / `--max-bytes` (add
  `args` to the case schema), or pin the defaults in the spec. Also specify that the
  overflow wrapper emits strictly more than `--max-bytes` on stdout.

### MEDIUM-5 — Success-case `want` is a subset; vacuous passes are possible

- Example: `"want":{"records_after_anchor":0}` and spec says "selected want fields".
  A success case that asserts only `records_after_anchor` leaves the four positive
  counters and `evidence_basis` unchecked, so a tool that always prints zeros passes.
- Fix: for `want_id=OK` cases the harness must require all of: `records_after_anchor`,
  the four `positive_*` counters, and `evidence_basis == "validated-record-subsets"`.
  Absent keys in OK cases = harness error (rc2), not a silent pass.

### MEDIUM-6 — Record-level MESSAGE leakage semantics undefined

- Spec: the query uses `--output-fields=...` with no MESSAGE. The wrapper ignores the
  query, so a fixture stdout record that *contains* a `MESSAGE` key is a leak test.
- Spec does not say whether such a record is (a) accepted with MESSAGE silently dropped,
  or (b) refused. The Stderr and AttackOutputLeak topics depend on this.
- Fix: pin it. Recommended: MESSAGE-bearing records are refused rc2 UNAVAILABLE with the
  stable reason, and MESSAGE is never echoed on any path.

### MEDIUM-7 — Case-id uniqueness scope

- Spec: each case `id` is "unique". Not stated whether unique per pack or globally.
  With 16 packs authored in parallel, cross-pack collisions are likely.
- Fix: harness checks global uniqueness across all packs in `--fixtures DIR`, and
  refuses (rc2 setup) on collision.

### LOW-1 — `returncode` vs `want_rc` naming is confusable

- Example: `"returncode":0` (the journalctl wrapper exit) and `"want_rc":0` (the CLI
  exit). The timeout note "expected rc2" refers to the CLI. Authors may swap them.
- Fix: rename `returncode` → `journal_rc`, and state in the schema that `want_rc` is the
  CLI exit code.

### LOW-2 — Invariants the harness should enforce mechanically

Recommended pre-run validation for every case (fail as rc2 setup, not as a tool bug):

- `want_id ∈ {MORI_JOURNAL_WINDOW_OK, MORI_JOURNAL_WINDOW_UNAVAILABLE, MORI_JOURNAL_WINDOW_SETUP}`.
- `want_id = OK` ⇔ `want_rc = 0`. `UNAVAILABLE` or `SETUP` ⇒ `want_rc = 2`.
- `timeout: true` or `overflow: true` ⇒ `want_id = UNAVAILABLE` and `want_rc = 2`.
- Non-empty `stderr` ⇒ `UNAVAILABLE`, rc2.
- OK cases: first stdout record's `__CURSOR` equals `anchor.cursor` and `_BOOT_ID` equals
  `anchor.boot_id` (otherwise the case is not a true "exact anchor" case).
- Every `MESSAGE_ID` literal used in an "exact" arm is in the `JOURNAL_ID_*` set of
  `tools/mori-census.sh` (see HIGH-1).
- Unique case `id` across all packs (MEDIUM-7).

### LOW-3 — r15 fixture shape is different; do not share a loader

- r15 fixtures (`.ufo/waves/round-15/fixtures/*.json`) are top-level arrays with
  `id` / `user` / `system` / `want_oom` / `want_signal` / `invalid_class`.
- Round-16 is `{"cases":[...]}` with `stdout` / `want_rc` / `want_id`.
- Risk: someone reuses the r15 census loader for r16. Keep them separate.

## 2. Verified (static) — consistent

- Census IDs cited in the prompts exist in `tools/mori-census.sh` (lines 1032-1036):
  `fe6faa94e7774663a0da52717891d8ef` (kernel OOM, `JOURNAL_ID_KERNEL_OOM`),
  `98e322203f7a4ed290d09fe03c09fe15` (unit SIGKILL, `JOURNAL_ID_UNIT_SIGKILL`),
  `fc2e22bc6ee647b6b90729ab34a250b1` and `d989611b15e44c9dbf31e3c81256e4ed` (non-OOM).
  Only the unit-failure ID is wrong (HIGH-1).
- Predicate names and semantics match r15 census lines ~976-984:
  - `positive_kernel_oom`: fe6faa94 records.
  - `positive_unit_oom`: d9b373ed records with `UNIT_RESULT == "oom-kill"`.
  - `positive_unit_signal`: d9b373ed records with `UNIT_RESULT == "signal"`.
  - `positive_process_sigkill`: 98e32220 records with `EXIT_CODE == "killed"` and
    `EXIT_STATUS` scalar `"9"` or number `9`; bool/array/null rejected.
  The PackUnitOom / PackUnitSignal / PackProcessSignal / TypedFields topic wording is
  consistent with these predicates, once HIGH-1 is fixed.
- Finding-id set (`MORI_JOURNAL_WINDOW_OK` / `_UNAVAILABLE` / `_SETUP`) and rc mapping
  (0 / 2 / 2) are internally consistent in the spec.
- Spec example case (`want_rc 0`, `want_id OK`, `records_after_anchor 0`) satisfies the
  invariants in LOW-2.

## 3. Not checkable now (blocked by absence)

- Every case's id uniqueness, want_rc / want_id agreement, want-field names, and
  predicate-field values. (No fixture files.)
- Whether the wrapper arms (timeout, overflow, stderr, nonzero rc) are authored to the
  invariants in LOW-2. (No harness.)
- Whether `tools/mori-journal-window.py` emits `records_after_anchor`,
  `positive_*`, `evidence_basis` with the exact names in the spec. (No tool.)
- Reason strings: spec says "reason stable" but enumerates none, so no fixture can pin
  a reason. Do not let fixtures assert reasons until the spec names a closed list.

## 4. Recommended order for the main agent

1. Fix HIGH-1 in the spec and in the dispatch/task-response copies before any pack is
   authored. This is the only item that changes content, not just schema.
2. Pin HIGH-2, MEDIUM-1/2/4/6 in the spec (rule text, not code) before authoring.
3. After packs land, re-run this review on the on-disk fixtures and the tool, and
   record read-time again.

No execution, no tests, no builds were performed. Read-only static review.
