# RevQuality104 — Criterion 104 shown-able-to-fail audit

**Target:** `corpus/QUALITY.md:829-836` (criterion 104, "QUALITY 102's check runs the registered gate `tools/mori-sources-appendonly.py` (SKILL.md Round36 registry row), not the round-35 wave script, which stays round-35 evidence. The gate also lists rows held earlier and absent at `<rev>` (`deleted=[...]`) and counts them as violations, closing 102's 'Not covered: deleted rows'. Check: `python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>` exits 0 with `round_changed=[]`; `--selftest` exits 0. Lesson: `corpus/lessons/round-35-verifier-spotcheck.md` §6 items 2-3. Shown able to fail: the self-test's deletion history prints `deleted=[S###]` and exit 1; under count-c2.py the round-35 script and a no-deletion variant score `C2=unmet` (`.ufo/waves/round-36/evidence/c0-rescore-v2.txt`, J2 and J5).")

**Claims under attack:** (1) the round-35 wave script (J2) scores `C2=unmet` under the frozen counter; (2) a no-deletion variant (J5) scores `C2=unmet`; (3) the gate's selftest deletion history prints `deleted=[S###]` and exit 1; (4) criterion 104 names the lesson (`round-35-verifier-spotcheck.md` §6 items 2-3) and the supersession of the round-35 wave script; (5) the check binds the registered gate at SKILL.md Round36.

## Evidence

### 1. J2 = round-35 wave script (byte-exact)
`sha256sum`:
```
f34cdbdee5b4b1fa8d2c28d5a4b2b9ac621e3d4b97b38d07ef880424de3914c6  .ufo/waves/round-36/c0/controls/J2.py
f34cdbdee5b4b1fa8d2c28d5a4b2b9ac621e3d4b97b38d07ef880424de3914c6  .ufo/waves/round-35/check-sources-appendonly.py
```
Identical (`diff` empty). `c0-dispatch.json` CtlJ2 (line 84-87): "copy `git -C … show 6bd57097:.ufo/waves/round-35/check-sources-appendonly.py` byte-exact".


### 2. Both score C2=unmet under the frozen counter (`evidence/c0-rescore-v2.txt`)
- J2 section (`c0-rescore-v2.txt:317-352`): `counter=count-c2.py sha256=c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34` (matches `evidence/freeze-v2.txt:4`). Blind 0/24; real arm FAIL (no summary line, tool exit=1); `C2=unmet` (line 350), `EXIT=1`.
- J5 section (`c0-rescore-v2.txt:476-558`): same counter sha; blind 0/24; real arm FAIL (tool prints violations=18 with `deleted=[]`, oracle `deleted=[]`; tool exit=1); `C2=unmet` (line 556), `EXIT=1`.
- No J2/J5 entry in the evidence scores `C2=met` (the only met line is 1169 = REF2 builder reference).

### 3. Selftest deletion-arm red behavior
- Full CLI self-test: `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0`, exit 0 (writes only a `tempfile.mkdtemp` sandbox; cleaned in `finally`; no lane mutation).
- Deletion-arm replication (same fixture as the selftest's "deleted row" case, `mori-sources-appendonly.py:372-373`: history [S001,S002] → [S001], driven through the CLI by the gate's own `_make_repo`/`_run_cli` helpers):
```
EXIT=1
deleted S002
appendonly_violations=1 ids=[] deleted=[S002] superseded=[] round_changed=[S002]
```
This is exactly the `deleted=[S###]` + exit 1 form criterion 104 cites; the per-id `deleted S002` line is also the shape the selftest asserts (`mori-sources-appendonly.py:422,448-451`).

### 4. Lesson named and supersession stated
- `QUALITY.md:833` cites `corpus/lessons/round-35-verifier-spotcheck.md` §6 items 2-3. The file exists and §6 item 2 reads "**SOURCES append-only debt.** … QUALITY 102's 'Not covered: deleted rows' stays a declared gap until the checker also flags a row missing at the tip" (line 172-174); item 3 reads "**Gate registry.** `.ufo/waves/round-35/check-sources-appendonly.py` … has no registry row at `SKILL.md` … and no self-test (PROTOCOL §Gate standard). Register it as a gate with a fixture self-test, or as a probe" (line 175-178). Both deficits are precisely what 104 closes.
- `QUALITY.md:829-831`: "runs the registered gate `tools/mori-sources-appendonly.py` (SKILL.md Round36 registry row), not the round-35 wave script, which stays round-35 evidence."
- SKILL.md Round36 registry row exists (`SKILL.md:873`): `SOURCES append-only (r36) | gate | python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P] | … | python3 tools/mori-sources-appendonly.py --selftest` (8 sandbox histories through the CLI) | …`; and `SKILL.md:864-865` states the tool "replaces the round-35 wave script `.ufo/waves/round-35/check-sources-appendonly.py` as the active check."
- The gate is committed at tip `bf0df77` (`git log -1 -- tools/mori-sources-appendonly.py` = bf0df77; `git status --short` shows no modification to `tools/`; sha256 `915527a7…` = working tree = commit content).

## Findings by severity
- **None.** Every element of criterion 104's shown-able-to-fail record reproduced: J2 (round-35 script, byte-exact) `C2=unmet`, J5 (no-deletion variant) `C2=unmet`, deletion-history red arm `deleted=[S002]` + exit 1, lesson citation §6 items 2-3 present, supersession of the round-35 wave script stated in 104 and in the registry (SKILL.md:864-865). No missing red arm; no defect found.

## Residual risk / verification gaps
- The full `--selftest` suit pass output is a single summary line; the `deleted=[S###]` + exit-1 red arm was evidenced by replicating the exact "deleted row" fixture through the CLI (fixture identical to `_selftest_cases()` case 4), not by forcing a suite failure.
- J5 is a *modified* round-35 script (deletion arm removed), matching the dispatch spec; the round-35 script itself is J2. J5's real-arm `deleted=[]` side matches the oracle, so its unmet score rests on the blind 0/24 mismatch, as the counter defines.
- The "real arm pass" of the *gate* (C2=met) is not re-run here (read-only review; receipt `evidence/c2-after.txt` records it); 104's own claims concern the two controls and the selftest red arm, both verified.

## VERDICT: PASS (criterion 104 — shown-able-to-fail record intact; no defect found)
