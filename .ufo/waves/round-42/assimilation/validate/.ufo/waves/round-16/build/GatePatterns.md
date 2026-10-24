# GatePatterns — reusable r15 manifest / provenance / setup patterns for the r16 harness

Seat: `MoriR16.GatePatterns` (scout, leaf). 2026-10-20.
Lane: read-only except this report. No production file, harness, tool, fixture,
expected table, registry or sibling report was written. No build, test, lint,
formatter, gate, selftest or smoke run was executed. No live journalctl query,
measurement/probe loop, background job, or `/tmp` output was created; no
outside-lane write or probe occurred, so there is nothing to disclose to
`MoriR16.Lesson`. No subagent was spawned.

Target: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Scope: `tools/mori-round15-regressions.py` (read at SHA-256
`6a55c33cc13e2cd862ebd44db66e8af635a35d7cd2a85168360569c886d62ffe`, which
equals its own expected-table pin), `.ufo/waves/round-15/expected.json`,
`.ufo/waves/round-15/build/HarnessBuild.md`,
`.ufo/waves/round-15/build/ProvenanceCapture.md`, and the live r16 packs.

Read-time state (observed, not a claim about later writes):

- `tools/mori-round16-regressions.py`: ABSENT.
- `tools/mori-journal-window.py`: ABSENT.
- `.ufo/waves/round-16/expected.json`: ABSENT.
- `.ufo/waves/round-16/fixtures/`: 13 of the 16 spec pack topics, 52 cases at
  read time (AnchorValidation, BootBoundary, CursorShape, ExactAnchor,
  KernelSystem, KernelUser, MissingAnchor, ProcessSignal, ProducerFailure,
  RecordShape, TypedFields, UnitOom, UnitSignal). The three spec topics not yet
  on disk were Bounds, MalformedCapture and Stderr; no present pack uses
  `timeout:true` or `overflow:true`.
- Git HEAD `b83edc6ee3db6822382ab673d7e6e984e420f22f`. Worktree already dirty
  at read time: modified `LOG.md`, `PROVINCE.md`, `SCORECARD.md`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, plus untracked r16 fixtures and
  reports. No commit was made or requested.

## Axes

1. **Pin authority** — every verdict-driving byte is identified by SHA-256 and
   compared, never trusted from a mutable manifest.
2. **Moving-input refusal** — the same bytes are re-hashed after the run; a
   mixed-revision verdict is refused, not averaged.
3. **Revision provenance** — real `rev-parse HEAD` plus exact porcelain paths,
   paths only, start and end, with the harness output scope named explicitly.
4. **Setup / refusal discipline** — guard before writes, atomic writes, strict
   fixture schema, stable rc/error labels, no auto-repair.
5. **Capability honesty (r16 addition)** — an absent tool is `capability_absent`,
   not a SUT mismatch and never a pass.
6. **Selftest isolation** — the harness exercises itself through real
   subprocesses on synthetic temp inputs; no live journal, no production tool.

## Reusable patterns (observed in r15)

Line numbers are from the read-time file above.

| # | r15 pattern | Mechanism | r16 adaptation |
|---|---|---|---|
| P1 | `sha256_bytes` / `sha256_file` (`:196-206`) | streaming hash; bytes and files hashed the same way | hash expected, every pack, tool source, executed tool copy, wrapper, raw run streams |
| P2 | `atomic_json` / `atomic_bytes` (`:216-234`) | write `.tmp`, `os.replace`, sorted keys, optional `chmod` | expected table, `run-manifest.json`, executed tool copy (0755), wrapper copies |
| P3 | `canonical` (`:236`) | compact sorted JSON for exact equality | per-case expected rows and every load/end digest block |
| P4 | `rel_or_abs` (`:208`), `one_line` (`:240`) | repo-relative paths; single-line bounded diagnostics with no raw bytes | manifest paths; refusal messages must not echo cursors, stderr canaries or pack bodies |
| P5 | `SetupError` / `SnapshotTampered` (`:180-188`) and labels in `main` (`:2337-2344`) | tamper is a subclass of setup; both exit 2; distinct `PIN ERROR` vs `GATE ERROR` lines | keep two labels: `PIN ERROR` / `GATE ERROR`; exit 2 for setup, tamper, moving input |
| P6 | `load_packs` (`:672-716`) | sorted `*.json`, read bytes once, hash those bytes, parse the same bytes, require a nonempty list, reject duplicate case ids globally | r16 top level is `{"cases":[...]}`; keep read-once/hash-once/parse-same-bytes, global id uniqueness, nonempty cases |
| P7 | `analyze_case` + `REQUIRED_KEYS`/`ALLOWED_KEYS`/`CASE_ID_RE` (`:166-175`, `:522-538`) | exact key set (unknown key = setup error), safe id regex, typed booleans/lists | exact r16 key set; optional `timeout`/`overflow`; safe case-id and pack-filename regex |
| P8 | `build_expected` / `compare_expected` (`:876-941`) | pin schema + constants + gate digest + helper digest + pack set + pack digests + canonical case rows; any mismatch raises `SnapshotTampered` with the current and expected values and says re-run `--pin-fixtures` | pin gate digest, tool presence+digest, pack set+digests, canonical case rows; never auto-repin |
| P9 | `run_pin` (`:1358-1375`) | pin mode loads and validates but executes nothing; atomic write; prints counts; warns when a required control class is absent | pin must execute neither the tool nor a wrapper; warn if the whole fixture set has no OK, no UNAVAILABLE, or no SETUP case |
| P10 | `materialize_target` (`:944-959`) | executed copy under `output/targets/`, mode 0755, digest of source bytes must equal digest of executed copy | copy `--tool` to `output/targets/window.py`; hash source and executed copy; manifest records both |
| P11 | `guard_output` / `guard_output_subpaths` (`:1383-1437`) | refuse output that is a symlink, is a file, covers/equals/sits under fixtures, frozen file/dir, expected file, repo root, `tools/`, `.git/`, `corpus/`; guard `fixtures/`, `targets/`, `runs/` subpaths before writes | protect `--fixtures`, `--expected`, `--tool`, repo root, `tools/`, `.git/`, `corpus/`; guard `wrappers/`, `targets/`, `runs/`, `fixtures/` subpaths |
| P12 | `capture_revision` (`:805-856`) | real `rev-parse HEAD`; `status --porcelain=v1 -z --untracked-files=all`; parses rename/copy old paths; sorted dedupe; paths only; records only the output tree as excluded scope | same; exclude only the harness `--output` tree, never an input; paths/contents are never copied |
| P13 | `revision_compare_core` (`:858-870`) | stable compare = observed HEAD + dirty paths outside harness output; full paths retained separately | same, but see D2 on which changes are fatal |
| P14 | `execute_census` run receipt (`:1033-1054`) | raw stdout/stderr files under `runs/`, argv, cwd, rc, timeout flag, exec error, duration, stream SHA-256 | one raw stdout/stderr and one wrapper-argv log per case; manifest stores paths+hashes, never stream contents |
| P15 | `run_gate` moving-input block (`:1675-1704`) | re-parse packs after the run and compare canonical rows; re-hash gate/helper/expected/source/executed copies; refuse a mixed-revision verdict | same for gate, expected, packs, tool source, tool executed copy, wrappers |
| P16 | `run-manifest.json` (`:1723-1770`) | `gate`, `expected`, `census`/frozen, `revision` start/end, `inputs` at_load/at_end/unchanged, `cases`, `runs`, `summary` | replace census/frozen sections with `tool`; add `capability_absent` accounting and `gate_exit` |
| P17 | `_selftest_run` (`:2166-2198`) | runs the harness itself as a subprocess, scrubs `MORI_*`, sets `PYTHONDONTWRITEBYTECODE=1`, writes a transcript under a temp root, asserts rc and a marker | reuse verbatim; markers `GATE PASS`/`GATE FAIL`/`GATE ERROR`/`CAPABILITY_ABSENT` |
| P18 | `selftest` (`:2200-2299`) | `tempfile.mkdtemp`, synthetic pack, synthetic wrappers, pin, green/red/tampered-id/tampered-rc runs, expected-digest tamper, then inspects the manifest run records | synthetic packs + a synthetic tool stub (not the production tool) under the temp root; explicit mismatch, setup, tamper, capability-absent and moving-input arms |

## Recommended r16 expected table

The r15 table is the right shape; r16 needs a `tool` block instead of
census/frozen blocks.

```json
{
  "schema": "mori-round16-regressions-expected-v1",
  "gate": {"path": "tools/mori-round16-regressions.py", "sha256": "<hex>"},
  "tool": {"path": "tools/mori-journal-window.py",
           "present": true, "sha256": "<hex-or-null>"},
  "fixtures": [
    {"name": "ExactAnchor.json", "sha256": "<hex>",
     "cases": [
       {"id": "anchor-only-user-empty-window", "scope": "user",
        "want_rc": 0, "want_id": "MORI_JOURNAL_WINDOW_OK",
        "want": {"records_after_anchor": 0},
        "timeout": false, "overflow": false,
        "journal_rc": 0, "stderr_present": false,
        "anchor_sha256": "<hex>"}
     ]}
  ]
}
```

Rules:

- The pack SHA-256 is the authority for every byte of the pack. Case rows are a
  human-diffable summary and an exact re-derivation check (P8), not a second
  source of truth.
- Do **not** store raw cursors, raw stdout, raw stderr, or `MESSAGE` bodies in
  the expected table. `anchor_sha256` and `stderr_present` are enough. This
  matches r15's rule that fixture record bodies are never copied into the
  manifest or a report, and it keeps a Stderr canary out of committed JSON.
- `present:false` pins the entering baseline capability; `sha256` must then be
  `null`. `present:true` requires a digest.
- Comparison order: schema, gate digest, tool presence/digest, pack name set,
  each pack digest, each canonical case row. Any mismatch is
  `SnapshotTampered` -> rc2 with expected/current values and "re-run
  --pin-fixtures". Missing expected file is `SetupError` -> rc2 with the exact
  pin command. No silent repair (r15 `compare_expected`, P8).
- Pin timing belongs to L1, after packs and the tool settle. A pin made while
  the tool is absent is valid evidence; it simply records the absent capability.

### Capability semantics (r16-specific, [INFERENCE] but forced by the contract)

| Pinned tool | On-disk `--tool` | Result |
|---|---|---|
| present + digest | present, digest matches | run normally |
| present + digest | absent | `SnapshotTampered` rc2 (a pinned input vanished) |
| present + digest | present, digest differs | `SnapshotTampered` rc2 |
| absent (`present:false`) | absent | `capability_absent`: rc1, zero runs, every expected case `capability_absent`; never counted as mismatch, never a pass |
| absent (`present:false`) | present | `SnapshotTampered` rc2; re-pin needed |
| any | exists but is a directory/unreadable | `SetupError` rc2 (not capability_absent) |

The summary must state `capability_absent_is_not_mismatch: true` and must not
fold those cases into `sut_fail`. rc1 is still correct because the expected
finite cases were not demonstrated.

## Recommended manifest sections

Follow P16, with this substitution:

```json
{
  "schema": "mori-round16-regressions-v1",
  "generated_at": "<UTC>",
  "gate": {"path": "...", "sha256": "..."},
  "expected": {"path": "...", "sha256": "...", "stored_copy": "expected.json"},
  "tool": {"path": "...", "present": true,
           "source_sha256": "...", "executed_copy": "targets/window.py",
           "executed_sha256": "...", "capability": "present"},
  "fixtures": [{"name": "...", "sha256": "...", "cases": ["..."]}],
  "revision": {"start": {}, "end": {}, "stable": true,
               "head_changed": false, "status_changed": false,
               "asserted_revision_note": "annotation only; real HEAD is compared"},
  "inputs": {"at_load": {}, "at_end": {}, "unchanged": true},
  "cases": [{"id": "...", "pack": "...", "status": "pass|mismatch|capability_absent|run_error",
             "expected": {}, "observed": {}, "run": "..."}],
  "runs": [{"run": "...", "case": "...", "argv": [], "cwd": "...", "rc": 0,
            "timed_out": false, "duration_ms": 0,
            "stdout_path": "...", "stderr_path": "...",
            "stdout_sha256": "...", "stderr_sha256": "...",
            "wrapper_argv_path": "...", "wrapper_argv_sha256": "..."}],
  "summary": {"total": 0, "pass": 0, "mismatch": 0,
              "capability_absent": 0, "run_error": 0,
              "capability_absent_is_not_mismatch": true},
  "gate_exit": 0
}
```

- `observed` carries only parsed stable fields (`rc`, `finding_id`, `scope`,
  `records_after_anchor`, four positives, `evidence_basis`) or a stable parse
  error label. It never carries raw stdout, raw cursor or stderr text (P14).
- Raw stdout/stderr files under `runs/` are evidence and may contain fixture
  cursors; the manifest stores paths and hashes only. The tool's own stdout is
  separate and must remain cursor-free.
- On a moving-input refusal, write the manifest **before** returning rc2 with
  `"gate_exit": 2` and `"refusal": "moving-input"`. r15 raises before writing
  (P15), so the strongest evidence of what moved is lost. This is the one
  deliberate deviation recommended. [INFERENCE]

## Moving-input and revision policy

Sequence, adapted from P6/P8/P15:

1. Guard `--output` and the pin target before any read or write. r15 guards the
   run output but **not** the pin path (`run_pin`, `:1358-1375`); r16 should
   refuse a pin path inside or equal to the fixtures tree, the tool, the
   expected table, the repo root, `tools/`, `.git/` or `corpus/`.
2. Read expected once, hash it, keep the bytes and store a copy in the output.
3. Read every pack once, hash raw bytes, parse those bytes, build rows.
4. Read the tool once, hash source bytes, write the executed copy, verify the
   executed digest equals the source digest (P10).
5. Capture revision start and `inputs.at_load`.
6. Run cases.
7. Re-hash every input and the executed copies; re-parse packs; capture revision
   end; compare canonical blocks. Any verdict-driving change -> rc2, no verdict
   (P15).
8. HEAD change between start and end -> rc2 `mixed-revision` (no commits are
   allowed in this wave, so a HEAD change is always an external event).
9. Dirty-path churn outside the harness output is **advisory, not fatal**.
   Sibling seats write reports concurrently; failing on that would make every
   run rc2. r15 records `status_changed` and `stable` without failing
   (`:1701-1704`, `:1746-1754`). Keep that split.

## Fixture-pack setup validation (r16)

These checks are setup (rc2), not tool behaviour. They mirror r15's strict
`analyze_case` (`:522-670`), with one critical r16 divergence.

Structural checks:

- Top level exactly `{"cases": [...]}`, nonempty list, no unknown top-level key.
- Case object: exact required keys (`id`, `scope`, `anchor`, `stdout`,
  `stderr`, `returncode`, `want_rc`, `want_id`, `want`), optional `timeout`,
  `overflow`; unknown key = setup error.
- `id`: globally unique across the pack directory, `CASE_ID_RE`
  (`^[A-Za-z0-9][A-Za-z0-9_.-]{0,80}$`, r15 `:175`); pack basename should use
  the same safe shape because it names wrapper/diagnostic paths.
- `scope` in `{user, system}`.
- `anchor` must be a JSON object and is written verbatim as the anchor file.
- `stdout`/`stderr` strings; `returncode` integer 0..255, bool rejected.
- `want_rc` in `{0, 2}`; `want_id` in `{MORI_JOURNAL_WINDOW_OK,
  MORI_JOURNAL_WINDOW_UNAVAILABLE, MORI_JOURNAL_WINDOW_SETUP}`;
  `OK <=> rc0`, `UNAVAILABLE|SETUP <=> rc2`.
- `timeout`/`overflow` booleans; either true requires rc2 +
  `MORI_JOURNAL_WINDOW_UNAVAILABLE`.
- Nonempty `stderr` requires rc2 + `UNAVAILABLE` (contract: any stderr is
  unavailable). Current `ProducerFailure` cases (`returncode` 5/124/137,
  empty stderr) already satisfy the nonzero-rc side.
- `returncode != 0` requires rc2 + `UNAVAILABLE`.
- rc2 cases: `want` must be `{}` (no numeric totals may be pinned).
- rc0 cases: `want` must contain `records_after_anchor`; allowed keys are the
  four `positive_*` counters, `scope`, `evidence_basis`; counts are integers
  `>= 0` (bool rejected); unknown key = setup error. Requiring all four
  counters and `evidence_basis` is the stronger rule recommended by
  `ReviewFixtures.md` MEDIUM-5, but the task contract's example shows a minimal
  `want`; L1 should settle this before the pin. [INFERENCE]

Anchor semantics — **do not reuse r15's reject-at-setup rule naively**:

`AnchorValidation.json` deliberately contains a scope-mismatched anchor, an
uppercase 32-hex boot id and a short boot id, all with
`want_rc:2 / MORI_JOURNAL_WINDOW_SETUP` (observed). The harness must therefore:

- compute `anchor_semantically_valid` (schema exact, `anchor.scope == case.scope`,
  32 lowercase hex boot id, cursor nonempty printable scalar `<=4096`);
- write the anchor object even when invalid;
- require `want_id = SETUP` iff anchor is semantically invalid;
- require `want_id != SETUP` when the anchor is semantically valid.

This is a check on fixture intent, not a refusal of the fixture. It is also how
the harness avoids a false setup error on the three intended SETUP cases. The
task contract's phrase "Anchor exactly schema..." conflicts with these authored
cases; L1 should record an append-only wording correction, not change the pack.

Optional stronger oracle (r15 `count_positives` / `derive_unavailable`,
`:420-511`), only for rc0 cases and only after typed-field semantics are pinned
(`ReviewFixtures.md` HIGH-2):

- every nonempty stdout line parses as a JSON object;
- first object's `__CURSOR` and `_BOOT_ID` equal the anchor's cursor and boot id;
- every later object has the same boot and a unique scalar `__CURSOR`;
- `records_after_anchor == objects - 1`;
- derive the four positives with the r15 predicates (kernel OOM id; unit-failure
  id with `UNIT_RESULT`; unit-sigkill id with `EXIT_CODE=="killed"` and scalar
  status `9`), compare to `want` when present;
- flag any `MESSAGE_ID` literal absent from `tools/mori-census.sh`'s
  `JOURNAL_ID_*` set (this catches the wrong unit-failure id recorded in
  `ReviewFixtures.md` HIGH-1).

Do not derive counts for refusal cases; there are no valid totals to compare.

## Per-case wrapper setup

Contract: "actual CLI subprocess using per-case executable journalctl
wrappers". r15's wrapper materialisation (`selftest` `write_wrapper`,
`:2210-2221`) is the reusable shape:

- `output/wrappers/<case>.py` (0755) emits the pack's literal `stdout` bytes,
  writes the pack's `stderr` bytes, exits `returncode`; `timeout:true` sleeps
  beyond the passed `--timeout`; `overflow:true` emits strictly more than the
  passed `--max-bytes`.
- Harness invokes `--journalctl output/wrappers/<case>.py` (the CLI must treat
  it as the journalctl binary).
- The wrapper appends its full argv to `output/wrappers/<case>.argv.jsonl`.
  The harness asserts: exactly one of `--user`/`--system` matching case scope,
  `--cursor=<anchor.cursor>`, `--no-tail`, `--quiet`, `--output=json`, the exact
  `--output-fields` list, no token `MESSAGE`, and no `--after-cursor`.
  `ReviewAnchor.md` and `ReviewCLI.md` F1 independently require an argv record.
- For timeout/overflow cases the harness must pass explicit small bounds (for
  example `--timeout 1`, `--max-bytes 1024`) because the pack schema has no
  per-case args (`ReviewFixtures.md` MEDIUM-4). Do not rely on undocumented
  defaults.
- Hash the wrapper before and after the run; a wrapper is a verdict-driving
  input (P15).

## Harness selftest arms (not executed here)

Use P17/P18; synthetic packs and a synthetic tool stub under
`tempfile.mkdtemp(prefix="mori-r16-selftest-")`, never the production tool, never
live journald:

1. pin synthetic packs -> rc0, expected exists, zero wrapper invocations
   (marker file absent), no tool execution.
2. green: expected-pinned tool stub, one OK and one UNAVAILABLE case -> rc0;
   manifest run records and input-hash blocks exist; `gate_exit:0`.
3. mismatch: stub returns rc2 where rc0 is pinned -> rc1, status `mismatch`,
   `capability_absent:0`.
4. capability absent: expected pins `present:false`, no tool file -> rc1,
   status `capability_absent`, zero runs, no wrapper invocation.
5. setup: missing expected -> rc2; missing/unreadable fixtures -> rc2.
6. tamper: flip a pack digest in expected -> rc2; run with a tool whose digest
   differs from the pin -> rc2.
7. output guard: `--output` equal to the fixtures directory -> rc2, nothing
   written there.
8. moving input: a synthetic wrapper rewrites its own synthetic pack mid-run ->
   rc2 + `refusal: "moving-input"` receipt (this arm is absent from r15 and is
   the only way to exercise P15). [INFERENCE]
9. `_selftest_run` discipline: `sys.executable`, scrubbed `MORI_*`,
   `PYTHONDONTWRITEBYTECODE=1`, bounded subprocess timeout, transcript under the
   temp root, assert rc + marker. Assert id strings, not reason strings, until
   the reason enum is pinned (`ReviewFixtures.md`).

Selftest temp trees are the only permitted temp use in this wave and only L1
executes them.

## Do-not-copy list (observed r15 defects / format traps)

- **D1 — git env hardening.** r15 `_git` (`:782-793`) sets
  `GIT_OPTIONAL_LOCKS=0`, `core.fsmonitor=false`, `--no-optional-locks` but not
  `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`. r14/r13 do set both
  (`tools/mori-round14-regressions.py:387-390`,
  `tools/mori-round13-regressions.py:1221-1223`). r16 should include all four.
- **D2 — do not make dirty churn fatal.** r15 records `stable` without failing
  and only refuses on input digests (`:1675-1704`). Sibling report writes are
  continuous in this wave.
- **D3 — pin path is unguarded.** `run_pin` (`:1358-1375`) writes wherever
  `--pin-fixtures` points, including a fixture pack. Guard it.
- **D4 — unbounded child capture.** `execute_census` calls
  `communicate(timeout=...)` without a byte cap and calls `communicate()` with
  no timeout after `killpg` (`:1023`, `:1031`). `ReviewCapture.md` already
  flags this. The r16 harness should bound its own capture (the tool under test
  is separately bounded); do not inherit this pattern.
- **D5 — fixture loader is not portable.** r15 packs are a top-level JSON list
  with `user`/`system`/`want_oom`; r16 is `{"cases":[...]}` with stdout strings
  (`ReviewFixtures.md` LOW-3). Keep loaders separate; share only the mechanics
  (read/hash once, duplicate id, atomic pin).
- **D6 — r15 semantic rejections are not r16 setup rejections.** r15 rejects an
  `invalid_class` that names no failing record; r16 must accept deliberately
  invalid anchors and pin their expected SETUP outcome. This is the single most
  likely false setup error if `analyze_case` is copied wholesale.
- **D7 — `has_message_key` does not transfer.** r15 rejects a `MESSAGE` key in
  parsed fixture records (`:245-253`, used at `:564-566`). r16 stdout is one
  escaped literal string and may deliberately contain hostile fields. Enforce
  "never MESSAGE" at the wrapper-argv layer, and pin the stdout-leak rule
  separately (`ReviewFixtures.md` MEDIUM-6). Do not scan raw stdout for the
  token and call it setup.
- **D8 — no census/frozen machinery.** r16 has no frozen census control; the
  entering state is `capability_absent`, evidenced by
  `.ufo/waves/round-16/frozen/entering-capability.json` (observed:
  `capability_present:false` at `b83edc6`). Pins are pack + gate + tool only.

## Remaining unknowns / L1 decisions

1. `tools/mori-round16-regressions.py` and `tools/mori-journal-window.py` were
   absent at read time; no pattern above was exercised against them.
2. No reason-string enum exists, so the harness can pin `rc` and finding id but
   not reason text yet.
3. Typed-field (non-scalar `MESSAGE_ID`/`EXIT_STATUS`) semantics is unpinned
   (`ReviewFixtures.md` HIGH-2), which limits the independent count oracle to
   cases whose records are all scalar-valid.
4. Bounds cases need per-case `--timeout`/`--max-bytes` (or defaults pinned in
   the spec) before the harness can construct `timeout`/`overflow` wrappers.
5. The anchor-file schema cannot express a non-object or malformed anchor file
   (`ReviewFixtures.md` MEDIUM-1). If `AnchorValidation` grows those cases, the
   pack schema needs `anchor_raw` or equivalent; the current three invalid
   anchors are object-level and are expressible.
6. The task contract says an anchor is "exactly schema mori-journal-anchor-v1",
   but `AnchorValidation.json` intentionally violates it to test SETUP
   refusals. Recommended resolution: treat semantic anchor validity as a
   fixture intent field (invalid => pinned SETUP), and record the wording
   contradiction as an append-only correction rather than changing the pack.
7. Whether rc0 `want` must carry all four positives plus `evidence_basis`
   (stronger, `ReviewFixtures.md` MEDIUM-5) or may stay minimal per the contract
   example is an L1 pin decision. At read time all 29 rc0 cases carried the five
   counts; 9 also carried `scope` and 12 carried `evidence_basis`.

## Tooling record

No tool was installed, upgraded or downgraded. No package transaction was
attempted. Reads were static (file reads plus `git rev-parse/status` and
`sha256sum` on declared inputs); no gate, selftest, journal query or production
tool was executed.
