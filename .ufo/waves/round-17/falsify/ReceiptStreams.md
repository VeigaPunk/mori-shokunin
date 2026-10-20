# C1 retained stream digests and per-case rc/finding falsification

**Scope:** read-only falsification of C1 retained evidence only: `evidence/seat-before|seat-after/run-manifest.json`, the 108 retained after-run `runs/<case>.stdout|.stderr` files, and the four receipts `evidence/{c1-before,c1-after,count-c1,seat-live}.json`. No gate, tool, selftest, or live-session run; no VCS command; no files written except this report. Consolidation ran as a stdlib `python3 -c` subprocess over committed bytes (rc0). Nothing was installed or upgraded.

## Answer: digest matrix

| Evidence side | Stream slots | Files retained | SHA-256 + size matched | Absent | Present-but-mismatched |
|---|---|---|---|---|---|
| `seat-after` (54 cases) | 108 | 108 | **108/108** | 0 | 0 |
| `seat-before` (54 cases) | 108 | 0 | 0 | **108** | 0 |
| Totals | 216 | 108 | 108 | 108 | **0** |

- After: file set equals exactly `{<id>.stdout,<id>.stderr}` for the 54 case ids (no orphans, no missing). All 54 stdout digests are distinct; all 54 stderr are the empty digest `e3b0c442...b855` with `stderr_bytes=0`, matching `tools/mori-seat-terminal.py:35` (JSON-only stdout).
- Before: `runs/` is empty; both `stdout_sha256` and `stderr_sha256` are `null` and the `stdout_bytes`/`stderr_bytes` keys are absent, with `tool.present=false` and `status=capability_absent` for all 54. The 108 absent slots are declared absence, not zero/blank digests, so they are not mismatches.
- Receipts: `c1-before`, `c1-after`, `count-c1`, `seat-live` → 8/8 recorded stdout/stderr digests recompute exactly (rc 1, 0, 0, 1 respectively; byte lengths 195/71/14/147904, all stderr empty).

`count-c1`'s `[54,0]` recomputes exactly from the manifests: before `capability_absent 54 + mismatched 0`, after `0 + 0`; manifest statuses are `{capability_absent:54}` and `{match:54}` respectively.

## Exact rc/finding (not aggregate)

For each of the 54 after cases, from the retained stdout alone:

- `RC_MAP[finding_id] == observed.rc == want.rc` for all 54 (26 rc1 / 25 rc0 / 3 rc2); `finding_id == want.finding_id`; rc2 cases carry no `totals`/`seats` claims and their `want` pins only rc+finding.
- `totals` re-derived from `kind=="seat"` rows equals the stdout `totals` and `want.totals` for all 51 seat-bearing cases; dead-class sum > 0 ⇔ rc1 ⇔ `_DEAD` for all 54 (no incoherent case).
- Every graded row is claimed: 50/51 `want.seats` maps resolve by the A1 relative `key`; `nested_directories` resolves by stem only (see F2). Per-seat class matches in all 51.
- Top-level keys are a subset of the schema allowlist and per-seat keys a subset of the A1 seat fields; no `errorMessage`/`content`/`usage`/`text` key appears anywhere (independent of the gate's own check).
- Independent binding: for 53/53 applicable cases (all but the nonexistent `MissingDir` pack), stdout `files_scanned` equals a fresh count of regular `*.jsonl` in the retained pinned fixture pack, honoring `--prefix` and the `--max-files` abort. So the retained documents describe real walks of the pinned fixtures, not synthesized tallies.
- Provenance pins: gate (`21285c2b…`), tool (`5819c3c0…`) and `expected.json` (`b684c63b…`) recompute to `PINNED_INPUTS.json` values; the 132-entry fixture-wide before/after snapshot maps are identical within each run and across both runs; 81 pins verified with no `inputs_changed`.
- Live receipt `seat-live.json`: stdout digest ok, rc1 + `MORI_SEAT_TERMINAL_DEAD`, 469 graded seats, 94 aged `dead_rate_limit`, totals sum equals seat count, retry count 90 re-derived, exactly the three argv prefixes present; matches the lesson's live numbers.

## Witnessed defects and limits (none defeats the 54→0 stream/rc claim)

**F1 — `pack_before_sha256`/`pack_after_sha256` use two incompatible definitions across branches.** In the `capability_absent` branch both fields are `pack_digest(fixture-wide snapshot subset)` (`tools/mori-round17-seat-regressions.py:1684-1685` → `pack_digest` at :368-375). In the executed branch both are `sha256(canonical(snapshot_tree(pack_dir)))`, a whole-pack tree digest (:1719-1721). Recomputation: before matches the prefix-subset definition 54/54 and the whole-tree definition 0/54; after matches whole-tree 53/54 (54th is `MissingDir`, `null` both sides) and prefix-subset only 1/54. Consequently cross-manifest field equality holds for 1/54 (the `null` case): the same field name is not comparable between the two receipts, and an auditor diffing them sees 53 false fixture drifts. The fixture-wide `inputs_before`/`inputs_after` maps (132 entries, identical cross-run) remain the valid stability witness, and `capability_absent` also fills `pack_after` from `inputs_before`, making `pack_changed=false` tautological there. Claim not defeated; field naming/definition is the defect.

**F2 — `expected.json` does not pin seat identity spelling.** `want.seats` uses the relative key in 50/51 seat-bearing cases, the stem in `nested_directories` only, and the gate accepts either (`compare_want`, `tools/mori-round17-seat-regressions.py:1227-1259`). Class/totals still cannot pass falsely: every graded row must be claimed (`unexpected_seat`) and duplicate-stem classes are compared per key. But the relative-key convention of A1:114 is asserted for only 50 cases, not as a table-wide invariant.

**F3 — A1:119 says the JSON "adds `now_ms`, `settle_seconds`, `main_sessions`, `duplicate_stems`" without an rc scoping;** the 3 rc2 setup documents instead contain only `schema`/`finding_id`/`reason`/`sessions_dir` (+`files_seen`,`max_files`,`prefixes`,`files_scanned`) per `_setup` (`tools/mori-seat-terminal.py:167-175`), and the gate explicitly permits minimal rc2 output (`allowed=None`, `mori-round17-seat-regressions.py:1300`). Contract text and implementation diverge for rc2; `want` pins only rc+finding there, so this is not a false green but the A1 wording overstates the emitted shape.

**F4 — `kind` vs `class` reading hazard.** `main_session_excluded_from_totals` retains a `kind:"main"` row with `class:"dead_rate_limit"` inside `seats` while `finding_id` is OK and rc0 — correct per A1:114 (main sessions excluded from totals; `dead` is computed over seat records, `mori-seat-terminal.py:484-489`), but a consumer filtering on `class` alone would see a dead class under a clean finding. Live run had `main_sessions=0`, so no live impact.

## Retention and trust boundaries

- Per-case sandboxes were removed: all `seat-after/cases/*/sessions` are empty (0 `*.jsonl`, 0 symlinks, 0 FIFOs), so retained stdout `sessions_dir` paths no longer resolve. The fixture-pack `files_scanned` re-derivation above recovers the tree binding from the pinned packs.
- Digest equality proves the gate's in-memory `out` bytes equal the retained files, and `evaluate()` derives `finding_id` reasons from those same bytes; `rc` is the real child return code, recorded but not independently re-derivable without re-running the tool (out of scope). Nothing independently tees child stdout to disk, so "process emitted exactly these bytes" rests on the gate's own `subprocess.PIPE` read.
- The terminal classifier itself (ordering, settle boundary, schema gate) was not reimplemented: `expected.json` is the compared authority here. That correctness lane is outside this seat. Manifests carry no run timestamp fields.

Attacked scope: stream retention/digests, per-case rc↔finding↔totals↔seat-class against `expected.json`, fixture-pin provenance, and the live receipt. Within that scope the 54/54 match and 108/108 stream digests are internally consistent; F1 is the one observed manifest defect.

Evidence: `.ufo/waves/round-17/contract.md:109-120`; `.ufo/waves/round-17/PINNED_INPUTS.json:1-25`; `tools/mori-round17-seat-regressions.py:368-375,1215-1260,1263-1315,1684-1685,1719-1721,1746-1752`; `tools/mori-seat-terminal.py:35,167-175,484-489,1831`; `.ufo/waves/round-17/evidence/{seat-before,seat-after}/run-manifest.json`, `seat-after/runs/<case-id>.stdout|.stderr`, `evidence/{c1-before,c1-after,count-c1,seat-live}.json`.

Report: .ufo/waves/round-17/falsify/ReceiptStreams.md
