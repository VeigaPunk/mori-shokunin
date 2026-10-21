VERDICT: HOLDS. All 20 battery commands exit 0 with their gate's pass verdict. Protected census and baseline bytes are unchanged. Two lane-hygiene items (F1, F2) are not battery-caused and need lead review.

## Method
- Run once, sequentially, cwd = lane root. Outputs, TMPDIR and HOME are isolated under `.ufo/waves/round-20/falsify/NoHarmRun/` (S). MORI_* and GIT_* stripped; LANG/LC_ALL=C; TZ=UTC.
- No git or jj command run by me. No installs or updates. Toolchain used as found: Python 3.14.8, bash 5.3.20, jj 0.45.1 (`~/.local/bin/jj`, used by the R17-jj gate).
- Logs: `S/logs/NN-*.stdout|stderr`, `S/logs/summary.json` (exact argv, rc, seconds, last lines), `pre-hashes.json`, `post-hashes.json`.
- 20 watched files (tools under test, C2 oracle, frozen c2-expected, R19 expected): sha256 identical before and after the run.
- Start marker 08:05:08.584; battery ended 08:08:04; retention mirror ran after.

## Results (rc = exit code; last = final stdout line)
01 `bash tools/mori-census.sh --selftest` rc=0. last: `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`
02 `bash tools/mori-silence-cases.sh` rc=0. last: `MORI_SILENCE_CASES: matched=28 total=28`
03 `python3 tools/mori-round13-regressions.py --selftest` rc=0. last: `SELFTEST: pass checks=33 cases=2`
04 `python3 tools/mori-round13-regressions.py --output S/r13` rc=0. verdict: `MORI_R13_REGRESSIONS: claims=24 pass=24 exit=0`; last line is a GATE-ROW echo
05 `python3 tools/mori-round14-regressions.py --selftest` rc=0. last: `SELFTEST: pass checks=20 (parsers + real-gate red rc1/tamper rc2)`
06 `python3 tools/mori-round14-regressions.py --census tools/mori-census.sh --output S/r14` rc=0. verdict: `MORI_R14_REGRESSIONS: claims=44 pass=44 exit=0`; last line is a GATE header
07 `python3 tools/mori-round15-regressions.py --selftest` rc=0. last: `SELFTEST PASS selftest_root=.../tmp/mori-r15-selftest-bnbb222t`
08 `python3 tools/mori-round15-regressions.py --census tools/mori-census.sh --fixtures .ufo/waves/round-15/fixtures --expected .ufo/waves/round-15/expected.json --output S/r15` rc=0. last: `GATE PASS exit=0`
09 `python3 tools/mori-round16-regressions.py --selftest` rc=0. last: `SELFTEST ok: pin_rc0,green_rc0_verdict_ok,absent_rc1_capability_absent,tool_drift_rc2,bad_want_rc1_mismatch,pack_drift_rc2`
10 `python3 tools/mori-round16-regressions.py --tool tools/mori-journal-window.py --fixtures .ufo/waves/round-16/fixtures --expected .ufo/waves/round-16/expected.json --output S/r16` rc=0. last: `GATE ok: 64/64 cases matched`
11 `python3 tools/mori-round17-seat-regressions.py --selftest` rc=0. last: `SELFTEST ok: ...,nonempty_output_rc2` (19 checks)
12 `python3 tools/mori-round17-seat-regressions.py --tool tools/mori-seat-terminal.py --fixtures .ufo/waves/round-17/fixtures/seat --output S/r17-seat` rc=0. last: `GATE ok: 66/66 cases matched`
13 `python3 tools/mori-round17-jj-regressions.py --selftest` rc=0. last: `SELFTEST ok: ...,absent_capability_absent`
14 `python3 tools/mori-round17-jj-regressions.py --census tools/mori-census.sh --output S/r17-jj` rc=0. line 1: `cases=17 match=17 mismatch=0 capability_absent=0 setup_failed=0 assertions=204 failed=0 retained=False`; last: manifest path
15 `python3 tools/mori-round19-regressions.py --content-tool <lane>/tools/mori-content-review.py --freeze-tool <lane>/tools/mori-freeze-order.py --expected <lane>/.ufo/waves/round-19/frozen/expected.json --output S/r19-after.json --mode after` rc=0. stdout is a JSON receipt; `.status` = `"pass"`
16 `python3 tools/mori-dispatch-ledger.py --selftest` rc=0. last: `SELFTEST mori-dispatch-ledger PASS 14/14`
17 `python3 tools/mori-freeze-order.py --selftest` rc=0. last: `SELFTEST freeze-order PASS 12/12`
18 `python3 tools/mori-wave-settlement.py --selftest` rc=0. last: `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (22 cases, 22 passed, 0 failed)` (tool selftest, not the oracle)
19 `python3 .ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool tools/mori-wave-settlement.py --out S/c2-oracle.json` rc=0. no stdout; `counts` = matched 14, mismatched 0, capability_absent 0
20 `python3 tools/mori-retention-gate.py --selftest` rc=0, run on scratch mirror (F3). last: `SELFTEST retention-gate PASS 21/21`
Protected bytes (critic's literal `sha256sum --check`, run before and after): `tools/mori-census.sh: OK`, `corpus/evidence/baseline-r10-20261015T2231Z.json: OK`, rc=0.

## Findings
F1 (not battery-caused; lead action). New bytecode caches in protected dirs: `tools/__pycache__/mori-wave-settlement.cpython-314.pyc` (08:05:36.227) and `.ufo/waves/round-20/build/ImplSettlementAlt/tools/__pycache__/mori-wave-settlement.cpython-314.pyc` (08:05:36.230). The `tools/` mtime moved to the same instant, so an entry was created there. No battery code imports this module. Greps of the battery scripts found no importlib, spec_from_file_location, import_module, py_compile or `python -c`. R15 compiles in memory and sets PYTHONDONTWRITEBYTECODE for children. The settlement and oracle runs are script executions, which write no bytecode for the entry script. A concurrent importer outside the battery is the likely cause [INFERENCE]. Not deleted (lane is read-only to me). Recommend: identify the importer, remove the caches, run tests with PYTHONDONTWRITEBYTECODE=1.

F2 (not battery-caused). Corpus files newer than my start marker: `corpus/knowledge/drift-repin-r20.md` (08:05:15.410, during step 01). The census selftest, silence-cases and R13 contain no corpus write path, only citation comments (grep). `corpus/knowledge/wave-settlement-r20.md`, `corpus/lessons/round-20.md` and `corpus/SOURCES.md` (08:09:38.067) were written after the battery ended. Lead should confirm these edits are intended.

F3 (deviation, disclosed). The retention selftest requires TMPDIR to equal the lane's `.scratch`, which is a lane write outside the read-only bound. I ran it on `S/rg/`, a mirror holding byte-identical copies of `tools/mori-retention-gate.py` (sha256 cf0896a2ea36f169c9e900c58eefe7e2a900a4c9d67f849f753f4631d8ab829e), `.ufo/waves/round-18/frozen/c1-policy.json` and `gate-snapshots/retention/retention.json`. Copies were hash-verified. The tool uses its root only for `.scratch`, the policy and the snapshot. Lane `.scratch` is still empty.

F4 (C2 registration). The critic's blocking gap now has a runnable command: row 19. c2-oracle.py sha256 2a0da4c8acf20f5960302e3850992fff7a164003501bf73ca912532a0f8e6914; c2-expected.json sha256 0984806922da727a02a7944c00154df7a5aaff356c91c6fb36f47467c4f7d2af. Result 14/14 matched, 0 capability_absent. Caveats: the oracle lives in build/ and its header records an L1 repair (v0 kept as c2-oracle-v0.py), so this result holds only for those bytes. I did not assess oracle independence from the implementation (outside this item).

F5 (critic doc divergence). NoHarmCritic.md's pre-registered commands write to `.ufo/waves/round-20/evidence/no-harm`, which is lane evidence. All my outputs went to S instead; argv is otherwise as registered.

## Not run / gaps
- Live census (no flags), R19 `--mode before`, C1 post-pin drift and C2 counting commands are outside this item.
- No lane git state recorded (no git commands run). Bind these results to bytes via `pre-hashes.json`.
