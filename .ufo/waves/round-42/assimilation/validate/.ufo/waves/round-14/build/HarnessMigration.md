# HarnessMigration — r13 regression gate: protocol conformance + restored C1 semantics

Seat: `MoriR14.HarnessMigration` (executor, leaf). Axis: **coverage** (C1 alarm/routing acceptance evidence). Milestone: restore OOM alarm and structured fleet routing.

Owned file: `tools/mori-round13-regressions.py` (only source file edited). Frozen r13 input bytes were **not** changed.

Report file sha256 of the owned source at authoring: `304cb22336da40c6d465b55f135ec9bb9bf53fdea4656c63c24c37963b6718f2` (3033 lines).

## Axes named

- **coverage (judged):** the gate must now require the restored structured OOM critical alarm and the fleet/non-fleet/unattributed unit partition, not the round-13 all-INFO/CLEAN contract.
- **operability (constraint):** exit map 0/1/2 only, real isolated self-invocation, truthful registry identity, independent frozen pins, named revision.
- **calibration (constraint):** fixtures are literal expected values; no unit bytes or MESSAGE text are echoed; unknown subject is explicit, never fleet/non-fleet/zero; no summed counters.

## Sources read (read-only)

- `corpus/lessons/round-13-verifier-spotcheck.md` (rejection: OOM crit loss, fleet/tsukuroi loss, gate-registry defect, mutation-provenance defect).
- `.ufo/waves/round-14/build/GateConformance.md` (G1/G3/G4/G6/G7/G11 checklist and migration section 6).
- `.ufo/waves/round-14/build/CounterAttack.md` (C1 claim flips, scope-leak blind spot, P01–P19 parity matrix).
- `.ufo/waves/round-14/build/MutationDesign.md`, `JournalFields.md` (structured subject/result fields).
- `corpus/lessons/round-14.md` (declared claim, M4/M5, source access).
- Landed `tools/mori-census.sh` journal probe (read after CensusRepair's edits): `FLEET_UNIT_TOKENS` at :1000, one unit query at :1201, unattributed routing at :1286–1288, single global OOM line at :1331, user KILL_SIGNAL split at :1353, added SURFACE unit tokens at :1373–1381.
- L1 IRC rulings (final schema, fleet severity INFO, user signal-result WARN, one unattributed literal id).

## Changes (single file)

### 1. Protocol conformance (routed defect 4 / GateConformance G1–G7, G11)

- Removed every false self-description: no “EVIDENCE HARNESS”, no “NOT A GATE”, no permanent “not-registered”. The docstring and CLI now describe a **registered gate** (registry home `SKILL.md`, row name `r13 regressions`) with the declared map **0 clean · 1 failed · 2 could-not-evaluate**.
- Exit 3 is gone. A mutation that cannot be built (or any unexpected harness exception) now returns **2** (could-not-evaluate), never a false failed verdict. Setup, usage and `snapshot_tampered` also return 2.
- `registry_status()` (with pure `registry_row_status(text)`) reads the lane `SKILL.md` and prints exactly one of:
  - `GATE registered name=r13 regressions registry=...` + `GATE-ROW <matched row>`, or
  - `GATE registration-missing ...`, or `GATE registry-unreadable ...`.
  It never asserts non-registration. Evidence `summary.gate` is a structured object with status, registry path, matched row and exit map.
- **Independent frozen pins.** `FROZEN_PINS` commits the three known digests and `FROZEN_BASE_COMMIT`; `verify_frozen_pins()` runs before any target subprocess or output write for the default `.ufo/waves/round-13/frozen`. A coordinated edit of a frozen file plus its sibling `inputs.json` now still raises `snapshot_tampered`; the manifest shape/base commit/entries are secondary checks. A custom `--frozen-dir` is honestly labelled `unpinned (custom frozen dir)` (manifest-verified only).
- **Named revision.** `record_revision()` uses `MORI_EVIDENCE_REVISION` first, else `git -C <repo> rev-parse HEAD` with an explicit git env (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`); a dirty flag is recorded, never hidden. Unavailable revision raises setup → exit 2. Evidence carries `revision.head`, `revision.dirty`, `revision.source`, `targets.frozen_pins`, and the committed `expectations` block (counts, severity map, six OOM counter names, fleet predicate, selftest case ids).
- Evidence schema bumped to `mori-round13-regressions-v2` (documented in the file; no in-repo consumer reads the string).

### 2. C1 migration to restored OOM critical + fleet-only semantics

The round-13 `R13_C1_CLEAN_VERDICT` (all notices INFO, CLEAN, forbidden kill rows, `unmeasured`/`field`/`unit` row-shape prerequisites) is removed. Its replacement measures the repaired production contract:

| claim id | fixture | literal expectation |
|---|---|---|
| `R13_C1_SYSTEM_NOTICE_COUNTS` | system kernel 2, oomd 1, coredump 3 (all signal 11), user 0 | six counts exactly 2/1/3/3/0/0; user six zeros; one global `OOM_KILL_JOURNAL crit`, `system_notice=2`, no routing finding; `DRIFT` rc1 |
| `R13_C1_USER_SCOPE_INDEPENDENT` | same primary run | user row six zeros, own boot, no summed token, no user-scoped finding; no `_USER` suffix heuristic (global OOM line has none) |
| `R13_C1_USER_SCOPE_NONZERO` | user kernel 3, coredump 1 (signal 11), system empty | user counts 3/0/1/1/0/0; system six zeros; global OOM `user_notice=3`; `DRIFT` rc1 |
| `R13_C1_NO_MESSAGE_TEXT` | primary + leak-forcing stub | raw pre-redaction canary flag false and no `MESSAGE`/`MESSAGE=` key in either run; leak run still reports exact structured counts |
| `R13_C1_OOM_ALARM_DRIFT` | primary | exactly one crit `OOM_KILL_JOURNAL`, `system_notice=2 user_notice=0`, no `count=`/`total`/`sum`, `DRIFT` rc1 |
| `R13_C1_NOTICE_CLEAN_CONTROL` | system oomd 1, coredump 2 (signal 11), kernel 0 | six counts 0/1/2/2/0/0; **no** OOM/routing/kill finding; `CLEAN` rc0 (severity-creep control) |
| `R13_C1_EMPTY_CLEAN_CONTROL` | no records | six zeros both scopes; no alarm/routing/kill; `CLEAN` rc0 (unconditional-DRIFT control) |
| `R13_C1_UNIT_OOM_KILL_ALARM` | system: fleet `UNIT_RESULT=oom-kill`, missing-subject `oom-kill`, fleet record with absent result | raw `unit_failure_record=3`; `unit_oom=2`, `unit_oom_fleet=1`, `unit_oom_subject_unknown=1`, `unit_oom_result_unknown=1`, `unit_missing=1`; global OOM `system_unit_oom=2`, `system_unit_oom_result_unknown=1`; `DRIFT` |
| `R13_C1_UNIT_FAILURE_ROUTING` | system: 2 fleet, 1 missing subject, 1 both UNIT+USER_UNIT; user: 1 non-fleet (`pipewire-pulse.service`) | system 4 = 2 fleet + 1 missing + 1 ambiguous, user 1 non-fleet; `UNIT_FAILURE_JOURNAL_SYSTEM info count=2 scope=system`; `UNIT_FAILURE_OUT_OF_SCOPE info count=1 scope=user owner=tsukuroi`; `UNIT_FAILURE_UNATTRIBUTED_JOURNAL info count=2 scope=system owner=unresolved reason=subject-metadata-unknown`; all INFO → `CLEAN` rc0 |
| `R13_C1_SIGKILL_WARN_PRESERVED` | user process-exit killed/9 ×1 | `KILL_SIGNAL_JOURNAL warn count=1 process_sigkill=1 user_unit_signal=0 scope=user`; no OOM; `DRIFT` rc1 |

Every ok SURFACE row must carry the six round-13 tokens (names/order unchanged) **and** the r14 added tokens `unit_fleet unit_nonfleet unit_missing unit_ambiguous unit_malformed unit_oom unit_oom_fleet unit_oom_nonfleet unit_oom_subject_unknown unit_oom_result_unknown unit_signal`; the harness checks `fleet+nonfleet+missing+ambiguous+malformed == unit_failure_record` and `oom_fleet+oom_nonfleet+oom_subject_unknown == unit_oom`, no `total`/`sum`, and boot either the validated anchor or the all-zero `unavailable:no-records`. `unit_unknown` is deliberately not asserted as an independent bucket (it is the derived unknown count in production); the concrete categories are.

F01/F02 claims and their original-frozen comparisons are untouched. `--baseline` still records pre-fix defects as `expected-defect` / `baseline-control`; the old baseline bug that forced `R13_C1_NO_MESSAGE_TEXT`/`R13_C1_CLEAN_VERDICT` to `baseline-deviation` is gone (baseline now checks only the MESSAGE-free observation, and the notice/empty controls check the roll).

### 3. Structured journal fixture (FixtureSentinel F2)

`journal_stub_body` was replaced: it is now a generic journalctl-shaped stub that (a) ANDs `FIELD=value` argv filters across fields and ORs within a repeated field, (b) honors `-o json` / `--output=json`, (c) projects exactly `--output-fields` including `UNIT`, `USER_UNIT`, `UNIT_RESULT`, `COREDUMP_SIGNAL`, `EXIT_CODE`, `EXIT_STATUS`, and (d) in leak mode forces `MESSAGE` even when the field list excludes it. Records are structured field maps carrying `_BOOT_ID`, `MESSAGE_ID`, and the canary MESSAGE; a query with no fixture match yields an empty stream at rc 0. Text mode emits only a header line, so the frozen text probe cannot observe the structured fixtures. Bash arrays used for parsing are explicitly `declare -A VALS` / `declare -a PAIRS`.

### 4. Real self-invocation selftest (GateConformance G4)

`--selftest` keeps every pure parser/constant check (verdict grammar, finding schema, scoped rows, `_token_int`, pass-case parser, oracle summary, fail reasons, SHONEN constants/diffs, shell quoting, registry matcher, frozen-pin shape, fleet predicate, committed case table) and adds a committed `SELFTEST_CASES` table executed as **subprocesses of the real script**:

| case | expected rc | required id |
|---|---|---|
| `isolated-stub-target-red` | 1 | `R13_C1_SYSTEM_NOTICE_COUNTS` |
| `isolated-frozen-manifest-tamper` | 2 | `R13_SNAPSHOT_TAMPERED` |

Each case builds a temp tree (canonical SHONEN copy, stub census, stub oracle, optional manifest-mismatch frozen dir), runs with an explicit env (no inherited `MORI_*`/`GIT_*`), and asserts: rc, required/forbidden `FINDING` ids, presence of a `GATE` line with no false `not-registered`, no canary/MESSAGE leak, and `evidence.json.summary.exit == expected rc`. The subprocess call never passes `--selftest`, so there is no recursion. The pure checks remain a separate list; the case table is authoritative.

### 5. Mutation provenance wording (GateConformance G11)

Docstring, CLI description/epilog, `--mutation` help, claim details and `mutations[].attribution` now state:

- F01 = **whole frozen `grade_lane` function transplant** (also carries the older environment-hardening/fsmonitor behavior); not a membership-lines-only or byte-exact one-line revert.
- F02 = **reconstructed prefix-presence `verdict_grade` shim** (`frozen_source=null`), not an original function body; proves single-locus sufficiency for BANANA acceptance, not original-byte restoration.
- Original frozen bytes under `--baseline` are named primary historical evidence.

### 6. Subprocess and leak hardening (FixtureSentinel F1/F3)

- `run_process` records a **raw pre-redaction `canary_present` flag**; the MESSAGE-free check uses that flag and the `<canary-redacted>` marker, so the canary arm can actually fail.
- Timeout teardown is now `SIGTERM` → 2 s grace → `SIGKILL` to the process group (a TERM-honoring oracle EXIT trap can clean its temp tree); any `BaseException` kills the group before re-raising. No orphaned `start_new_session` child.
- Fixture trees stay under the explicit `--output` tree (no `/tmp` evidence); the docstring says so. Fixture directory names are now neutral (`fx-a` … `fx-k`) so no case id reaches the census through the path it echoes (`cmd=$JOURNALCTL_BIN ...`); run ids remain descriptive in evidence only. FixtureSentinel's residuals are recorded as deliberate limits: the stub projection is stricter than real journalctl (`_BOOT_ID`/cursor emitted only when requested — a false-red-only risk), and newline/control-character unit-name injection cannot be represented in the 0x1f line format (it belongs in the census selftest or the r14 gate). Selftest cleanup remains `rmtree(ignore_errors)`; no case creates mode-000 trees.

## Facts retained (read-only measurements)

| item | value |
|---|---|
| owned source sha256 | `304cb22336da40c6d465b55f135ec9bb9bf53fdea4656c63c24c37963b6718f2` |
| frozen `mori-census.sh` | `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164` (unchanged, == `inputs.json`) |
| frozen `mori-silence-cases.sh` | `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` (unchanged, == `inputs.json`) |
| frozen `inputs.json` | `d91690dc0417aecd9bffd507b53cd4e2a32fc6614753c82ccbc0c5b590cfdc3f` (unchanged, == `FROZEN_PINS`) |
| static validation | one read-only `ast.parse` (no import, no gate/census/oracle execution) — OK, 3033 lines |

No gate, census, oracle, selftest or mutation was executed by this seat. L1 runs verification once after all seats land.

## Risks and limits

1. **Schema alignment is read-only, not executed.** The C1 expectations were pinned from L1's final ruling and the landed probe source (`:1000`, `:1201`, `:1286–1288`, `:1331`, `:1353`, `:1373–1381`). If production id/token spelling moves again, the strict suite goes red — which is the intended failure mode, not a silent pass.
2. **Default frozen pins are mandatory on every run.** A tree without `.ufo/waves/round-13/frozen` (or with edited bytes) returns 2 `snapshot_tampered`/`snapshot_missing`; custom frozen dirs are manifest-verified and labelled unpinned, not independently pinned.
3. **Registry row is owned by SkillRegistry.** Until the `SKILL.md` row lands, output says `GATE registration-missing` (truthful). It never says `not-registered`. GateConformance/closure should treat a missing row as a conformance defect, not a harness verdict.
4. **`--baseline` remains a defect-recording mode**, not a green baseline: expected statuses are in-script, so the “two evidences” frozen-run expected-verdict file for r14 is the new gate's job; this gate's frozen pins + recorded baseline are the migration, not a new expected.json.
5. **Selftest red case uses stub targets.** It proves main/claim/exit/evidence/GATE plumbing and the tamper path; it does not re-prove production semantics (the strict run and the r14 gate do that).
6. Production still contains the retired r13 structured ids only in comments/history; the harness no longer expects `KERNEL_OOM_NOTICE_JOURNAL_*`, `R13_C1_CLEAN_VERDICT`, or `unmeasured` row prerequisites.
7. **Structured fixture limits (false-red only):** the stub emits exactly `--output-fields` and therefore omits journalctl's always-present `__CURSOR`/timestamps when unrequested; it cannot represent newline/control-character unit names (0x1f line records, minimal JSON escaping). A missing core field can only fail a claim, never make one pass; adversarial newline injection is measured by the census selftest / r14 gate.

## Recommended commands (L1, after all seats land; exact)

```sh
cd /home/vgpnk/Projects/shokunin/mori-shokunin

# 1. Self-test: pure checks + two real isolated subprocess cases.
python3 tools/mori-round13-regressions.py --selftest
# expect exit 0, "SELFTEST: pass checks=<N> cases=2", and GATE registered (after SkillRegistry row lands)

# 2. Strict gate against the repaired production targets.
python3 tools/mori-round13-regressions.py \
  --output .ufo/waves/round-14/evidence/regressions-strict
# expect exit 0, 24 pass claims; evidence.json summary.exit=0, revision named, frozen_pins=verified

# 3. Original frozen bytes: record the pre-fix defects (kept primary over mutations).
python3 tools/mori-round13-regressions.py --baseline \
  --output .ufo/waves/round-14/evidence/regressions-baseline
# expect exit 0 with expected-defect/baseline-control statuses; no baseline-deviation

# 4. Function-locus mutations red under the fixed targets.
python3 tools/mori-round13-regressions.py --mutation both --jobs 1 \
  --output .ufo/waves/round-14/evidence/regressions-mutation
# expect exit 0, 24 pass + 2 mutation-red; no mutation-unavailable

# 5. Tamper negative control (custom frozen copy, manifest mismatch):
T=$(mktemp -d)
cp .ufo/waves/round-13/frozen/* "$T"/
printf '#\n' >> "$T/mori-census.sh"
python3 tools/mori-round13-regressions.py --baseline --frozen-dir "$T" \
  --output .ufo/waves/round-14/evidence/regressions-tamper
# expect exit 2 and "FINDING R13_SNAPSHOT_TAMPERED status=fail"

# 6. Explicit revision receipt (optional; otherwise git HEAD is recorded):
MORI_EVIDENCE_REVISION=$(git rev-parse HEAD) MORI_EVIDENCE_DIRTY=false \
  python3 tools/mori-round13-regressions.py --output <dir>

# 7. Registry check:
grep -nE 'mori-round13-regressions|r13 regressions' SKILL.md
```

Sequential, not parallel: the `--selftest` red case and the accepted `--mutation` run both create isolated trees under their own `--output`; no shared path.

## Tooling

No tools installed or updated. Read-only actions: `grep`, `sed` reads, `sha256sum`, Python `ast.parse` (syntax only), and `git diff --stat`.

## SHONEN

Not applicable to a leaf executor seat; no promotion box was touched and no SHONEN assessment is claimed.
