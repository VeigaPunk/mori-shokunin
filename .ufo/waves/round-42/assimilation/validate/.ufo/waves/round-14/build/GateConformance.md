# R14 GateConformance — PROTOCOL gate standard vs r13 harness vs planned r14 gate

Seat: `MoriR14.GateConformance` (reviewer, leaf). Judged on: coverage. Milestone: restore OOM alarm and structured fleet routing.
Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No tests, builds, lint, or gate/harness runs. No files edited outside this report.

## Sources read (path:line)

- Canonical standard: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:388-435` (§Gate standard: verdict 393-397, self-test 398-402, two evidences 403-410, registry 411-419, scope 420-424, closure 425-430, delivery 431-435); `:230-231` (closure gate reproduces statuses); `:356-386` (Evidence standard, referenced).
- Appendix rows: `PROTOCOL-APPENDIX.md:35` (Gate standard, 10/12), `:51` (Registry home, 14), `:45` (Frozen inputs, 12/13).
- Lane registry: `mori-shokunin/SKILL.md:58-68` (Gates; table lists census, drift pin, silence oracle only); `:132` (verdict contract).
- r13 harness: `mori-shokunin/tools/mori-round13-regressions.py` (HEAD `dbe8500`, last touched `c13df48`, file sha256 `02b5974244923fa9cf644ce0795de98f6843b95e43662a6522d6299d8b63e264`, `git status` clean).
- r13 frozen dir (git-tracked): `.ufo/waves/round-13/frozen/{inputs.json, mori-census.sh, mori-silence-cases.sh}`. No `expected.json` exists.
- r13 census selftest reference: `tools/mori-census.sh:2243-2255` (`run_selftest`, trap cleanup), `:2265-2347` (fixture dispatcher stub, `MORI_FIXTURE` guard exit 97), `:2355-2360` (`fx_hash`/`fx_no_mutation`), `:2422-2427` (`env -i` SUT env), `:2457-2513` (`check()`: rc, verdict regex, finding ids), `:3435-3436` (`--selftest` dispatch).
- Routed defects: `corpus/lessons/round-13-verifier-spotcheck.md:132-135` (routes 1-4), `:84-89`, `:108-111`; `.ufo/waves/round-13/build/` items M7/M8 (cited from `round-13.md:23-24`).
- Planned gate spec: `.ufo/waves/round-14/dispatch.json:367` (CensusRepair: "CLI rc0 clean 1 mismatch 2 setup, pin snapshot digest if frozen given; selftest must invoke real gate over isolated fixture"), `:372` (HarnessMigration), `:392` (SkillRegistry), `:457` (this seat).
- Digests (read-only `sha256sum`): `tools/mori-census.sh` = `39abda0a…3985` (= spotcheck H), `tools/mori-silence-cases.sh` = `34cd5770…abfa`, frozen `mori-census.sh` = `3da5b098…3164` (= spotcheck B production), frozen `mori-silence-cases.sh` = `448f7723…eeb5`, frozen `inputs.json` = `d91690dc0417aecd9bffd507b53cd4e2a32fc6614753c82ccbc0c5b590cfdc3f`.

## Axes named

- **coverage** (judged axis): the gate must exercise the alarm and routing semantics it claims, with a real exit code and finding id, not helper outputs.
- **adjacency** (named constraint): gate fixtures and self-invocation must not read the live journal or write outside a temp tree.
- **discernment** (named constraint): the gate's expected values must be committed independently of its own recomputation.

## Conformance matrix: PROTOCOL standard vs r13 harness

| # | PROTOCOL requirement | r13 harness state | Evidence | Verdict |
|---|---|---|---|---|
| G1 | Gate is a committed, re-runnable verdict script; a verdict-producing tool is a gate | Verdict-producing (exit 0/1/2/3, `FINDING` lines, evidence.json), but self-declared "EVIDENCE HARNESS, NOT A GATE" and "not registered" | `:2-8`, `:1799`, `:1813`, `:1958` | **FAIL** |
| G2 | Registry row with name, kind, entry, verdict map, self-test spelling, pinned path, write scope, owner | No row. `SKILL.md:64-68` lists census, drift pin, silence oracle only | `SKILL.md:64-68` | **FAIL** |
| G3 | Verdict: 0 clean, 1 failed, every other code declared in registry, undeclared reads could-not-evaluate | Exit 0/1/2/3. Code 3 (`mutation-unavailable`) undeclared anywhere | `:59-64`, `:1743-1747` | **FAIL** (no registry to declare 3 in) |
| G4 | Self-test = self-invocation mode over isolated fixtures asserting **exit code and stable finding id**, expected values committed and independent of recomputation | `--selftest` calls `selftest()`, which imports and calls pure helpers (`verdict_roll`, `findings`, `lane_row`, `surface_rows`, `pass_cases`, `count_value`, `oracle_summary`, `fail_reasons`, `Harness._shonen_diff`, `shlex.quote`). No subprocess, no temp tree, no rc or finding-id assertion against a gate run. Count `checks=N` is printed dynamically, not a committed expected value | `:1821-1907`, `:1906` | **FAIL** (PROTOCOL :402 says helper-only "does not satisfy this clause") |
| G5 | Two evidences, part 1: a run over a committed input snapshot with its committed expected verdict | Frozen run exists only as a `--baseline` mode. Expected defects live in an in-script table, not checked against a committed frozen-run verdict file | `:51-54`, `:1499-1511` | **PARTIAL** |
| G6 | Frozen `expected.json` pins digest of every snapshot input; gate verifies digests before comparing; edited snapshot = `snapshot_tampered` (could-not-evaluate); no digests = `unpinned (legacy)` | Digests come only from `inputs.json`, which lives in the same directory as the files it digests. Verification (`verify_inputs_file`) checks file-vs-inputs.json consistency, not against any independent pin. A coordinated edit of a frozen file and its `inputs.json` passes. `snapshot_tampered` path exists (rc2) | `:269-298`, `:709-732`, `:740`, `:1787-1789`, `:1951` | **PARTIAL / FAIL on independence** |
| G7 | Verdict names the revision it was measured against | Evidence records sha256 of targets, frozen files, SHONEN, and `inputs.json`. Records no git revision and no dirty-state | `:1772-1790` | **FAIL** |
| G8 | Scope: read-only over surfaces it does not own; no live-tree write | Strict mode reads live `tools/mori-census.sh`; evidence goes to explicit `--output`. Fixtures under `--output` tree (`:33-46` of docstring). Compliant | docstring `:44-46` | PASS |
| G9 | Subprocess isolation | `run_process` passes an explicit `env=` dict (not inherited), `census_env` sets `PATH`, `HOME`, `TZ`, `LC_ALL` only; `build_common` (`:581`) and `census_env` (`:615-622`) exist and are reusable | `:581`, `:615-622`, `:771` | PASS (reusable) |
| G10 | Closure: red gate is a conformance defect; integrator verifies committed evidence (self-test tally, frozen-run verdict, revision) | Registry absent, so closure cannot grade it conformant (`:425-435`). Retained selftest evidence `regression-selftest-final.json` is 24 checks at `80bd58a`, not the delivered revision (spotcheck :135) | spotcheck `:135` | **FAIL** |
| G11 | Docstring/CLI accuracy for mutation provenance | F01 transplants the whole frozen `grade_lane`, not membership lines only. F02 is a reconstructed shim (`frozen_source: null`, `reverted_by: pre_fix_prefix_presence_shim`). Docs do not say this (`:55-57`, `:1575-1620`) | `:1602-1620` | **FAIL** (routed, spotcheck :136) |

Summary: the r13 harness fails G1, G2, G3, G4, G7, G10, and G11 and partially fails G5 and G6. Its only conformant elements are isolation patterns (G8, G9). Its selftest is the largest gap: the standard explicitly forbids helper-only self-tests.

## Why the current selftest is not a gate self-test

- It never executes `tools/mori-round13-regressions.py` or any census. A broken `main()`, broken exit mapping, or broken `FINDING` schema passes `SELFTEST: pass`.
- Prior evidence: M7 (`round-13.md:23`) was a parser that accepted an invented schema and rejected real census output. The fix added another pure test of the same parser (spotcheck :135, M7). Pure tests of a parser repeated the same blind spot.
- Census precedent (what the standard means): `tools/mori-census.sh:2243-2513` runs the real script in a subprocess under `env -i`, with a stubbed dispatcher, and asserts rc plus verdict regex plus finding ids for each case, plus a fixture-unchanged hash. The census-selftest evidence (`.ufo/waves/round-13/evidence/census-selftest.json:8`) records `PASS drift: LANE_SILENT (exit 1 DRIFT)`, i.e. the exit+id form.

## Pinned frozen input: the gap, measured

- Digest facts above are correct and current. Each frozen file matches the spotcheck table.
- The only pin is `inputs.json`, beside the files. `inputs.json` is itself not pinned by any gate. Its digest (`d91690dc…`) appears only in retained receipts (`.ufo/waves/round-13/evidence/*/evidence.json`, six hits). No gate reads those receipts.
- Consequence: anyone who edits `frozen/mori-census.sh` and rewrites `frozen/inputs.json` passes `snapshot_verify` and gets a clean frozen run. PROTOCOL :404-410 requires the expected values to be persisted independent of the snapshot.
- Frozen semantics (for the new gate's oracle choice): `frozen/mori-census.sh` = `3da5…` = spotcheck's B production, which emits OOM critical (`oom_crit_emissions=1`) and keeps the fleet/non-fleet split. Current production `39abda0a…` = spotcheck's H, which emits 0 OOM critical and 0 nonfleet routing. The frozen file is therefore the pre-cutover oracle, and the current file is the red-before witness. Measurements of both are L1's to run.

## Implementable minimal design (no tests run; for CensusRepair / HarnessMigration / SkillRegistry / L1)

### 1. Single gate file: `tools/mori-round14-regressions.py` (new, owned by the r14 seat per dispatch :367)

Use the r13 harness only as a source of helpers (`build_common`, `census_env`, `write_exec`, `sha256_file`, `json_dump`, `one_line`, `redact`). Do not inherit its `GATE not-registered` wording, its exit 3, or its helper-only selftest. Migrate or retire `tools/mori-round13-regressions.py` in the same round (HarnessMigration).

CLI:

```
python3 tools/mori-round14-regressions.py --census PATH --output DIR [--frozen-dir DIR] [--keep-fixtures]
python3 tools/mori-round14-regressions.py --selftest
```

- `--census` default `tools/mori-census.sh`. `--output` required (explicit evidence dir). `--frozen-dir` optional.
- Exit codes (declare exactly these in the registry row):
  - `0` clean: every claim passes.
  - `1` failed: at least one claim is `fail`, or a selftest case mismatches.
  - `2` could-not-evaluate: usage, setup, census missing or not executable, `snapshot_tampered`, evidence write failure. No other codes.
- Stdout: one `FINDING <id> status=<pass|fail|unavailable> axis=<a> observed="…"` line per claim, plus a final `MORI_R14_REGRESSIONS: claims=N … exit=R` line. Stable ids use the `R14_` prefix. Redact `CANARY` (`:105`, `:314`, `:321`).

### 2. Pinned frozen input (G6 fix): committed expected values in the gate, not in the snapshot dir

```python
FROZEN_PINS = {  # committed expected values; independent of .ufo/waves/round-13/frozen/inputs.json
    "mori-census.sh": "3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164",
    "mori-silence-cases.sh": "448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5",
    "inputs.json": "d91690dc0417aecd9bffd507b53cd4e2a32fc6614753c82ccbc0c5b590cfdc3f",
}
FROZEN_BASE_COMMIT = "6531ac6029e200a6392bb76673b6a17d3c895c96"
```

Algorithm, run before any census subprocess and before any output write:

1. `sha256(inputs.json) == FROZEN_PINS["inputs.json"]`. Else `R14_SNAPSHOT_TAMPERED`, rc 2.
2. Parse `inputs.json`. Its `sha256` map keys must equal `{"mori-census.sh", "mori-silence-cases.sh"}`, and `base_commit == FROZEN_BASE_COMMIT`. Else tampered, rc 2.
3. For each key `k`: `sha256(frozen/k) == FROZEN_PINS[k] == inputs["sha256"][k]`. Else tampered, rc 2.
4. Only on success, the frozen census may be run. Record `frozen_pins: verified` in evidence. When `--frozen-dir` is not given, record `frozen: not-supplied` (the spec's "pin if frozen given").

Keep `.ufo/waves/round-13/frozen/` bytes unchanged. Do not add files there.

### 3. Revision naming (G7)

Before running, record in evidence:
- `git -C <repo> rev-parse HEAD` (`REVISION`) and `git -C <repo> status --porcelain` (`DIRTY=true|false`), run with explicit `env=` (`PATH=/usr/bin:/bin`, `HOME`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`).
- If git cannot answer, record `REVISION=unavailable` and exit 2 (could-not-evaluate). Do not emit a fake revision.
- The `--census` sha256 is already recorded (`:1772`); keep it.

### 4. Real self-invocation selftest (G4 fix)

`--selftest` creates `tempfile.mkdtemp(prefix="mori-r14-selftest.")`, runs each case through the gate's own `main` in a subprocess, and removes the tree in `finally`.

Per case:
1. Build a fixture tree with `build_common(base)` / `census_env(base)` (`:581`, `:615`). Write a stub `journalctl` that answers only from the fixture and exits 97 when `MORI_FIXTURE` is unset (census pattern `:2265-2302`). Write stub `git`, `df`, `pgrep`, `tmux` the same way.
2. Compute `fx_hash(base)` before (census pattern `:2355`).
3. `subprocess.run([sys.executable, str(Path(__file__).resolve()), "--census", str(stub_census), "--output", str(out)], env=ISOLATED_ENV, cwd=str(base), capture_output=True, text=True, timeout=120)` with `ISOLATED_ENV` as an explicit dict. No inherited `MORI_*` or `GIT_*`.
4. Parse stdout `FINDING` lines and rc. Assert:
   - `rc == expected_rc`;
   - every id in `expected_ids` appears as `FINDING <id> status=…`;
   - no id in `forbidden_ids` appears;
   - stdout contains no `CANARY` text and no `MESSAGE` key/value;
   - `fx_hash(base)` unchanged (`fx_no_mutation` pattern `:2356-2360`).
5. Emit `SELFTEST: case <id> ok|bad …`; final `SELFTEST: pass cases=N` (exit 0) or `SELFTEST: fail <ids>` (exit 1).

Expected values are literal constants, never derived from the gate's own functions:

```python
SELFTEST_CASES = (
  # (case id, expected rc, required finding ids, forbidden finding ids)
  ("oom-user-kernel-notice",   1, ("R14_OOM_KILL_JOURNAL",),           ()),                    # critical, DRIFT
  ("oom-system-kernel-notice", 1, ("R14_OOM_KILL_JOURNAL",),           ()),
  ("unit-result-oom-kill",     1, ("R14_OOM_KILL_JOURNAL",),           ()),                    # structured UNIT_RESULT=oom-kill
  ("fleet-unit-failure",       1, ("R14_UNIT_FAILURE_JOURNAL",),       ("R14_UNIT_FAILURE_OUT_OF_SCOPE",)),  # warn => DRIFT (see note)
  ("nonfleet-unit-failure",    0, ("R14_UNIT_FAILURE_OUT_OF_SCOPE",),  ("R14_UNIT_FAILURE_JOURNAL",)),       # info, owner tsukuroi
  ("empty-journal-control",    0, (),                                  ("R14_OOM_KILL_JOURNAL",)),
  ("query-error-unknown",      2, (),                                  ("R14_OOM_KILL_JOURNAL",)),  # rc must not be 0; see note
  ("message-canary-absent",    1, ("R14_OOM_KILL_JOURNAL",),           ()),                    # canary never printed
  ("frozen-tamper",            2, ("R14_SNAPSHOT_TAMPERED",),          ()),
  ("red-before-current-census",1, ("R14_OOM_KILL_JOURNAL",),           ()),                    # pinned 39abda0a…
)
```

Notes on the table:
- Stable finding ids above are proposals. OomAttack, ResultFixtures, and RoutingAttack seats own the final id spellings. The table is a committed constant once fixed.
- `fleet-unit-failure` rc 1 relies on the measured precedent that a `warn` finding maps to DRIFT: `census-selftest.json:8` shows `LANE_SILENT` (warn) → exit 1 DRIFT. Confirm against the census verdict rule before committing the value.
- `query-error-unknown` must not be rc 0. The census rule is `unavailable is not zero` (`SKILL.md:29-31`, `:72-79`). The exact rc is a measured value: L1 records it once and commits it. It is not inferred here.
- Keep the pure checks as an extra sub-list, but they do not replace the case table.

### 5. Registry row (SKILL.md Gates table, mori's registry home per PROTOCOL :411-419)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| regressions-r14 | gate | `python3 tools/mori-round14-regressions.py --census <path> --output <dir> [--frozen-dir .ufo/waves/round-13/frozen]` | 0 clean · 1 failed · 2 could-not-evaluate | `--selftest` (real gate subprocess, `SELFTEST_CASES`) | `FROZEN_PINS` + `SELFTEST_CASES` in script; frozen dir read-only | `--output` dir only | mori |
| regressions-r13 (migrated or retired) | gate or retire | `python3 tools/mori-round13-regressions.py …` | 0 · 1 · 2 (3 dropped or declared could-not-evaluate) | `--selftest` (rewritten to subprocess, same pattern) | `FROZEN_PINS` (same constants) | `--output` dir only | mori |

Also remove `SKILL.md` description references to the r13 harness as "unregistered"/"evidence harness" (SkillRegistry seat).

### 6. Harness migration checklist (HarnessMigration seat, `tools/mori-round13-regressions.py`)

- Docstring `:2-8` and `:4`: drop "NOT A GATE" and "deliberately not registered".
- `:1799`, `:1813`, `:1958`: replace `gate: not-registered` with the registry row name.
- `:1745-1747`: drop exit 3 or declare it in the registry as could-not-evaluate.
- `:1821-1907`: keep as an inner list of pure checks. Add the subprocess case table (section 4) as the authoritative selftest.
- `:269-298`, `:709-732`: add `FROZEN_PINS` check (section 2). Keep `inputs.json` as a secondary check.
- `:1772-1790`: add `REVISION`, `DIRTY` (section 3).
- `:1602-1620` and docstring `:55-57`: state F01 = whole-function transplant of frozen `grade_lane`; F02 = reconstructed shim with `frozen_source: null`. Do not describe either as original-byte restoration (spotcheck :136).
- Keep the frozen directory bytes unchanged.

### 7. Ordering and evidence (L1, once, after all edits)

- L1 runs `--selftest` and each committed run once. L1 commits the measured rc values for `query-error-unknown` and the frozen-current red-before witness, then pins them in `SELFTEST_CASES`. Those committed constants are the only expected values; they are not recomputed at selftest time.
- Evidence written under `.ufo/waves/round-14/evidence/`, with `REVISION`, `DIRTY`, census sha, frozen pins, rc, and finding ids.

## Findings by severity

1. **HIGH — Gate is unregistered and self-described as not a gate** (G1/G2/G10). `tools/mori-round13-regressions.py:2-8, :1799, :1813, :1958`; `SKILL.md:64-68`. Fix: section 5 registry row, docstring change.
2. **HIGH — Selftest is helper-only, not a self-invocation** (G4). `:1821-1907`. Fix: section 4 subprocess case table. Required by PROTOCOL :398-402.
3. **HIGH — Frozen input pin is self-referential** (G6). `:269-298` checks `inputs.json` against files beside it. The inputs digest is recorded at `:1787-1789`, `:1951` and never compared. Fix: section 2 `FROZEN_PINS` in the gate.
4. **MEDIUM — No revision named** (G7). `:1772-1790`. Fix: section 3.
5. **MEDIUM — Undeclared exit code 3** (G3). `:1745-1747`. Fix: drop or declare.
6. **MEDIUM — Selftest tally not committed; retained evidence on a different revision** (G10). `:1906` prints `checks=N` dynamically; `regression-selftest-final.json` is 24 checks at `80bd58a`, not delivered `c13df48`/`dbe8500` (spotcheck :135, routed item 4). Fix: committed `SELFTEST_CASES` count; re-run on the delivered revision (L1).
7. **LOW — Mutation provenance wording** (G11). `:55-57`, `:1602-1620`. Fix: section 6 wording.

## Residual risk and verification gaps

- No execution was done (assignment bound). Selftest pass, rc values, and the `query-error-unknown` rc are unmeasured and must be measured by L1.
- The fleet-unit-failure rc 1 mapping is a precedent-based inference (`census-selftest.json:8`). Confirm against the census verdict rule.
- Final finding-id spellings depend on OomAttack, ResultFixtures, and RoutingAttack seats; this report does not fix them.
- The frozen census (`3da5…`, pre-cutover) has not been measured here for OOM/fleet semantics. It is the intended oracle only if it passes the restored claims. That measurement is L1's.
- The `build_common` / `census_env` helpers exist (`:581`, `:615`) but were not executed. Their `journal_stub_body` was not read (`:661`); the exit-97 guard must be verified in the new gate's stubs.

## Tooling

No tools installed or updated. Read-only actions: `sha256sum`, `git rev-parse --short HEAD`, `git log -1`, `git status --porcelain` on the two paths.

## SHONEN

Not applicable to this seat (no shokunin SHONEN assessment is produced by a reviewer in a leaf seat; `ShonenScribe` owns it).
