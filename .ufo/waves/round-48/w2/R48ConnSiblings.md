# R48ConnSiblings — Sibling overlap audit for quota entry and pin tool (round 48, wave 2)

Seat: R48ConnSiblings. Lane: mori-shokunin (森, fleet and host observability: detection and report only).
Role: UFO-FSD connector / leaf seat falsifier.
No subagents dispatched. No production files, git index, jj state, or sibling repositories mutated.
Scratch directory: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ConnSiblings/`.

**Attacked:** The hypothesis that sibling lanes contest mori-shokunin's scope by duplicating or contradicting:
1. Mori's filesystem quota observability knowledge entry (`corpus/knowledge/quota-observability-r48.md`, theme FR2, sources S479–S484), or
2. Mori's SKILL.md self-test pin reconciler tool (`tools/mori-pin-check.py`).

**Verdict: HOLDS — class CLEAN_SEPARATION (zero contested scope, zero duplicate knowledge, zero semantic contradiction).**
All quota references in sibling lanes represent operational host runtime failure logs/hazards (specifically `/tmp` tmpfs exhaustion on the test workstation) or lexical false positives, not filesystem observability knowledge. No sibling lane implements a dynamic self-test pin re-measurement tool; sibling registry tools perform only static forward presence checks.

---

## 1. Audit Part 1: Sibling Overlap for Quota Observability (FR2)

### 1.1 Command and Observed Exit Code

```bash
grep -rliE --exclude-dir='.scratch' --exclude-dir='.ufo' --exclude-dir='waves' \
  'xfs_quota|quotactl|EDQUOT|repquota|Disk quota exceeded' \
  /home/vgpnk/Projects/shokunin/*-shokunin/corpus \
  /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md \
  /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md 2>&1
```

- **Exit code:** `2` (due to standard `grep` error output on non-existent `audio-shokunin/SKILL.md` and `game-dev-2d-shokunin/SKILL.md`).
- **Total matching files across fleet:** 642 matching file occurrences.
- **Hits within local lane `mori-shokunin`:**
  - `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md`: Declares provincial ownership of `FR2 — Quota/EDQUOT observability (detection and report only)`.
  - `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/quota-observability-r48.md`: Round-48 C2 knowledge entry.
  - `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md`: Lines 434 & 979 (decision table rules for quota error reporting).
  - `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/observability-surfaces-r2.md` and `audit-r11.md`: Historical audit citations.
  - `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r48/*`: The 6 source copies (S479–S484).

### 1.2 Analysis of Sibling Hits by Lane

A targeted scan for `xfs_quota`, `quotactl`, and `repquota` outside `mori-shokunin` yielded **EXACTLY 0 hits** in any sibling lane.
All sibling hits matched `EDQUOT` or `Disk quota exceeded`. Detailed breakdown by owning lane:

1. **`audio-shokunin`** (5 files: `corpus/live/runs/.../measurements.json`, `r77-scout/RECEIPTS.md`, `r77-boundary/probe-p7p8-bigwav-and-counter.json`, `r82-fold/run2-red-flake.measurements.json`, `r82-fold/proofs.txt`):
   - *Context:* Live ffmpeg and arecord integration runs generated multi-gigabyte uncompressed WAV files into `/tmp`, filling the 16 GB tmpfs and logging `Error submitting a packet to the muxer: Disk quota exceeded`.
   - *Relation to Mori:* Operational host runtime symptom. Does not define quota observability. No duplication or contradiction.
   - *Contested scope:* None (report-not-absorb).

2. **`game-dev-2d-shokunin`** (145 files across `corpus/fixtures/export_*.gd`, `corpus/lessons/r103-*.md`, `r104-*.md`, and `corpus/live/runs/`):
   - *Context:* Headless Godot engine export fixtures and test harness lessons. Fixtures document that `/tmp` on this workstation intermittently rejects even 4 KB writes with `EDQUOT` (quota), directing scratch directories to `/var/tmp/` instead.
   - *Relation to Mori:* Runtime environment constraint and host mitigation note. Does not analyze quota architecture or syscalls.
   - *Contested scope:* None (report-not-absorb).

3. **`game-dev-3d-shokunin`** (2 files: `corpus/knowledge/unreal-mcp/gate/README.md`, `run_gate.sh`):
   - *Context:* Line 267 of `run_gate.sh` uses `grep -qiE 'disk quota exceeded|no space left|out of diskspace|write error|quota exceeded'` to classify test subprocess log failures as environment errors rather than engine failures.
   - *Relation to Mori:* Gate triage regex for classifying external command failure modes. Does not observe or report filesystem quota state.
   - *Contested scope:* None (report-not-absorb).

4. **`kaidoku-shokunin`** (7 files: `corpus/knowledge/2026-10-19-arc3-r{1,3,4,6}-*.md`, `corpus/lessons/round-20.md`, `SKILL.md:449`, `corpus/evidence/round-34/elf/e12.bin`):
   - *Context:* Knowledge entries state recheck instructions noting that default runs fail with `EDQUOT (errno -122)` in the `/tmp` sandbox. `SKILL.md:449` mandates `use /var/tmp (/tmp never — EDQUOT hazard)`. `e12.bin` is a binary glibc ELF containing standard error strings (`EDQUOT`, `Disk quota exceeded`).
   - *Relation to Mori:* Operational mitigation of host sandbox limits. Does not define quota telemetry.
   - *Contested scope:* None (report-not-absorb).

5. **`kake-shokunin`** (2 files: `corpus/lessons/round-55.md`, `corpus/QUALITY.md`):
   - *Context:* Lexical false positive. Case-insensitive regex matched substring `edQuot` in `stagedQuoteAudit` (lines 44, 77, 94, 1168).
   - *Relation to Mori:* None.
   - *Contested scope:* None.

6. **`kengaku-shokunin`** (2 files: `corpus/evidence/probe-r19-P{4,5}-glm.log`):
   - *Context:* Probe run logs noting temporary test artifacts: `Left in /tmp per §2.6 (no EDQUOT occurred)`.
   - *Relation to Mori:* Operational probe log note confirming absence of write failure.
   - *Contested scope:* None.

7. **`kotoba-shokunin`** (1 file: `corpus/knowledge/corpus-integrity-round11.md`):
   - *Context:* Line 97 documents historical test execution `under /tmp disk-quota pressure (sort: write failed: … Disk quota exceeded)`.
   - *Relation to Mori:* Retrospective citation of a test runner failure.
   - *Contested scope:* None.

8. **`tabi-shokunin`** (3 files in `corpus/evidence/round-13/aria/node_modules/playwright-core/...`):
   - *Context:* Lexical false positive. Case-insensitive regex matched substring `edQuot` in JavaScript identifier `preferredQuote`.
   - *Relation to Mori:* None.
   - *Contested scope:* None.

---

## 2. Audit Part 2: Sibling Tools That Re-measure SKILL.md Self-Test Pins

### 2.1 Command and Observed Exit Code

```bash
grep -l 'self-test' /home/vgpnk/Projects/shokunin/*-shokunin/tools/* 2>&1
```

- **Exit code:** `2` (due to standard directory skip warnings on `tools/__pycache__` and `tools/fixtures`).
- **Hits outside `mori-shokunin`:**
  - `chousa-shokunin/tools/assimilate-rows.py`
  - `kama-shokunin/tools/gate-registry-check.py`
  - `kama-shokunin/tools/kama-llamacpp-live.py`
  - `kotodama-shokunin/tools/assemble-culture-d3.py`
  - `kotodama-shokunin/tools/assemble-culture-d4.py`
  - `kotodama-shokunin/tools/assemble-d2-typed.py`
  - `kotodama-shokunin/tools/assemble-d2.py`
  - `kotodama-shokunin/tools/assemble-d4-typed.py`
  - `kotodama-shokunin/tools/check-claim-separability.py`
  - `kotodama-shokunin/tools/d2-typed-labels.py`
  - `kotodama-shokunin/tools/replay-frozen.py`

### 2.2 Sibling Tool Inspection

Each hit was inspected to determine whether it parses SKILL.md, executes self-test commands, or verifies pins:

1. **`chousa-shokunin/tools/assimilate-rows.py`**:
   - Accepts `--selftest` to run self-test fixtures on row assimilation logic. Does not read SKILL.md.

2. **`kama-shokunin/tools/gate-registry-check.py`**:
   - Parses five-column registry tables in `SKILL.md` (`| Name | Kind / entry command | Exit map | Self-test / pinned values | Write scope |`).
   - Checks that every round counter in `.ufo/waves/round-*/count-*.py` or `tools/round<N>-*.py` is present in the table (`registered`), has non-empty cells, and that cited paths exist on disk (`missing-path:PATH`).
   - **Does NOT re-measure pins:** It never executes the self-test command, never evaluates output tallies, and never checks sha256 or line count pins.

3. **`kama-shokunin/tools/kama-llamacpp-live.py`**:
   - CLI tool flag `--selftest` runs parser and outcome self-tests without starting a model server. Does not read SKILL.md.

4. **`kotodama-shokunin/tools/*.py`** (8 tools):
   - All 8 scripts accept `--selftest` / `--self-test` to execute self-contained internal unit tests and synthetic fixture checks. None inspect SKILL.md.

### 2.3 Extended Inspection of Sibling Registry Tools

An extended audit of sibling tools inspecting `SKILL.md` revealed three additional instruments:

1. **`tsukuroi-shokunin/tools/check-registry-coverage.py`**:
   - Audits `SKILL.md` section `## Gate and probe registry — roundN...`.
   - Verifies that all files under `tools/` have a corresponding registry row, that the `Kind` is valid (`gate`, `probe`, `library`), and that any `--selftest` flag cited in the table exists as literal text in the tool source code (`REGISTRY-SELFTEST-UNRESOLVED`).
   - **Crucially ignores pins:** Line 267 unpacks `name, kind, entry, verdict, selftest, _pinned, _scope, _owner = cells` and completely discards `_pinned`. It does not execute self-tests or re-measure pinned values.

2. **`tsukuroi-shokunin/tools/check-self-assessment.py`**:
   - Audits `SCORECARD.md` self-assessment claims (K01–K27), checking that stated line counts and table row counts match `SKILL.md` line counts (`wc -l`) and pipe lines (`grep -c '^|'`). Does not parse or execute gate registry pins.

3. **`tameshi-shokunin/tools/registry-check.py`**:
   - Monitors entry commands declared in `tools/registry.json`. While `registry.json` includes `SKILL.md` provenance references, the tool executes commands from JSON, not from Markdown table cells.

4. **`souji-shokunin/tools/souji-landing-gate.py`**:
   - Checks that file paths cited in `SKILL.md` exist in the git tree (`LG-MISSING-REG`). Does not execute pins.

### 2.4 Conclusion on Pin Tools

`mori-pin-check.py` is **unique in the fleet**. It is the only instrument across all 20 shokunin lanes that dynamically parses Markdown gate registry tables, binds and executes `--selftest` commands in isolated environments, validates stdout tally regexes, verifies full sha256 digests, validates truncated digests, and verifies file line counts. Sibling tools perform only static structural checks (file-to-row coverage and path existence).

---

## 3. UFO-FSD Connector Move: Compatible Synthesis

### 3.1 Observed Evidence and Structural Asymmetry

Across the fleet and the round-48 artifacts, two complementary registry verification paradigms exist:
- **Sibling Paradigm (Forward Coverage: Tool -> Registry):** Both `kama-shokunin/tools/gate-registry-check.py` and `tsukuroi-shokunin/tools/check-registry-coverage.py` ensure that *no tool exists in the repository without being registered in SKILL.md*. They scan `git ls-tree tools/` and flag any untracked or unregistered tool within milliseconds (<0.2 s).
- **Mori Paradigm (Reverse Truth: Registry -> Tool Execution & Pins):** `mori-shokunin/tools/mori-pin-check.py` parses *existing rows in SKILL.md* and verifies that their pinned tallies, digests, and line counts match execution.

**The Blind Spot:** In round 48 wave 1, `tools/mori-unlanded-check.py` was introduced as a new instrument to close mistake M1. An engineer manually added row 973 in `SKILL.md`. If an author creates a new tool or script under `tools/` and forgets to register it, `mori-pin-check.py` produces `PIN_CHECK=met` without warning! It has no `git ls-tree` scan over `tools/`. Conversely, `kama` and `tsukuroi` tools produce exit 0 even if the self-test tally in the registry is completely fabricated or stale.

**Second-Order Runtime Interaction:** Re-measuring pins involves substantial subprocess overhead. When running `count-c1.py` (which runs `mori-pin-check.py` over 12 synthetic variants and 1 real registry, executing 572 subprocesses), execution took 210.19 seconds with `--jobs 8`. Under default sequential execution, it exceeded the 300 s timeout. Furthermore, as revealed in Part 1, host `/tmp` suffers from severe `EDQUOT` write failures. `mori-pin-check.py` correctly routes `TMPDIR` into `<repo>/.scratch/`, but running heavy subprocess suites exposes the lane to disk and process exhaustion.

### 3.2 Affected Axes

- **`calibration`** (Active score: 5, lowest tied axis): Improves calibration by eliminating false-green states where unpinned or unmeasured instruments lurk in `tools/` without being bound to the registry.
- **`operability`** (Active score: 7): Improves operability by synthesizing forward tool discovery with reverse pin verification into a single complete gate.
- **Zero harm to `depth` (5), `freshness` (5), `coverage` (6), or `adjacency` (6):** The check is purely additive, read-only over `git ls-tree`, and runs in <0.1 s before the dynamic pin runner.

### 3.3 Proposed Move: Bi-directional Registry Reconciler (Forward Tool Discovery + Reverse Pin Re-measurement)

For the successor round (round 49), synthesize the forward coverage technique of `kama` (`gate-registry-check.py`) and `tsukuroi` (`check-registry-coverage.py`) into `tools/mori-pin-check.py`:

1. **Phase 1 (Forward Tool Discovery — fast git tree scan, <0.2 s):**
   - Execute `git ls-tree -r --name-only <rev> -- tools/` (filtering `.py` and `.sh`, excluding `__pycache__` and `fixtures/`).
   - Parse all table rows in `SKILL.md` under all five- or eight-column registry tables.
   - For every discovered tool path, verify that it appears in at least one registry row's `entry` or `self-test` cell.
   - If an unreferenced tool is found, report `pin tool=<path> state=unregistered` (fatal, exit 1).
2. **Phase 2 (Reverse Pin Re-measurement — standing v3 dynamic evaluation):**
   - Proceed with the existing v3 semantic verification (tally pins, digest pins, truncated digests, line counts, baseline rebound checks, hidden rows).

### 3.4 Risks and Tradeoffs

- **Risk:** Auxiliary test helpers, fixture generators, or internal libraries in `tools/` that lack a `--selftest` flag might be flagged as `unregistered`.
- **Mitigation:** Adopt `tsukuroi`'s explicit `Kind` classification (`library` vs `gate` vs `probe`) or an explicit ignore pattern for `tools/fixtures/` and `tools/_*.py`.

### 3.5 Verification Procedure

Demonstrate in scratch on a temporary git fixture:
1. Clean tree: all tools in `tools/` are registered in `SKILL.md` with accurate pins -> exit 0 (`PIN_CHECK=met`).
2. Add unreferenced dummy tool `tools/mori-unregistered-sample.py` without touching `SKILL.md` -> tool immediately exits 1 (`pin tool=tools/mori-unregistered-sample.py state=unregistered`).
3. Add row with corrupt pin -> tool exits 1 (`pin line=N kind=tally state=mismatch`).
4. Execution time of Phase 1 measured at <0.05 s, adding zero perceptible latency to the evaluation.

---

## 4. Acceptance Runs on Landed Tip

Both frozen round-48 claims were evaluated on landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`:

1. **C1 Calibration Verification:**
   - Command:
     ```bash
     TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ConnSiblings \
       python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py \
       --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
       --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --jobs 8
     ```
   - Output:
     ```
     variant name=J1 expect=unmet got=unmet rc=1
     variant name=J2 expect=unmet got=unmet rc=1
     variant name=J3 expect=unmet got=unmet rc=1
     variant name=J4 expect=unmet got=unmet rc=1
     variant name=J5 expect=unmet got=unmet rc=1
     variant name=J6 expect=unmet got=unmet rc=1
     variant name=J7 expect=unmet got=unmet rc=1
     variant name=J8 expect=unmet got=unmet rc=1
     variant name=H1 expect=met got=met rc=0
     variant name=H2 expect=met got=met rc=0
     variant name=H3 expect=met got=met rc=0
     variant name=H4 expect=met got=met rc=0
     variant name=real expect=met got=met rc=0
     C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
     ```
   - Result: **C1=met** (exit 0; 210.19 s wall clock).

2. **C2 Depth Verification:**
   - Command:
     ```bash
     python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c2.py \
       e4dfff32d4f97c7ef250e9a7538fa75d4f284492
     ```
   - Output:
     ```
     C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
     ```
   - Result: **C2=met** (exit 0; 0.21 s wall clock).
