# RevR44Cell — r44 registry cell vs committed auditor bytes

Role: UFO-FSD reviewer (leaf, no subagents). Scope: the r44 registry cell
(`## Gates` rows `r44 gate registry (C2)` at SKILL.md:184 and `r44 gate registry
(C2) — write scope superseded` at SKILL.md:194) — its selftest tally, digest and
line-count claims against the committed auditor bytes. Read-only; no edits,
no installs, no pacman.

## Checks performed (all reproducible)

1. Committed auditor bytes (HEAD `9834fed4` and working tree are identical —
   `git status --porcelain` lists no modification for the file):
   - `sha256sum tools/mori-gate-registry.py` → `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`
   - `git show HEAD:tools/mori-gate-registry.py | sha256sum` → same digest
   - `wc -l tools/mori-gate-registry.py` → **743 lines** (31165 bytes)
2. Actual selftest of the committed bytes (worktree == HEAD bytes):
   - `python3 tools/mori-gate-registry.py --selftest` → 15 `selftest PASS` lines,
     `GATE_REGISTRY_SELFTEST pass=15 fail=0`, exit 0
3. Frozen predicate runs:
   - `python3 .ufo/waves/round-46/count-repins.py SKILL.md` (repaired worktree)
     → `MORI_R45_REPINS mismatches=0 rows=4`, exit 0
   - `python3 .ufo/waves/round-46/count-repins.py .ufo/waves/round-46/control-skill.md`
     → `MORI_R45_REPINS mismatches=4 rows=4`, exit 1
4. Control identity: `sha256sum .ufo/waves/round-46/control-skill.md` =
   `ed71e8f6…` = `git show HEAD:SKILL.md | sha256sum` (control is byte-identical
   to the committed SKILL snapshot).

## Findings

- **F1 (no substitution found — tally/digest/line-count all match committed bytes).**
  Both r44 cells in the repaired worktree SKILL.md carry, verbatim:
  `GATE_REGISTRY_SELFTEST pass=15 fail=0`, sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`,
  `743 lines`. Each was independently re-measured against the committed auditor
  bytes and matches exactly: selftest prints `pass=15 fail=0` (rc 0), file hash
  is `8b82ac99…`, line count is 743. There is no stale or substituted value in
  the r44 cells as repaired.
- **F2 (the prior committed snapshot — the do-nothing control — is stale, and
  red *because* of it).** The control (HEAD SKILL.md, `ed71e8f6…`) r44 cells
  assert different values than the committed auditor bytes:
  - SKILL.md:184 (control) claims `GATE_REGISTRY_SELFTEST pass=6 fail=0`
    (v1-era description, no digest, no line count) — the committed auditor is
    743 lines at `8b82ac99…` and prints `pass=15 fail=0`.
  - SKILL.md:194 (control) claims v2 = sha256 `64db765e…`, 622 lines,
    `pass=10 fail=0` — none of those describe the committed bytes.
  This reproduces the predicate's red state: count-repins on the control reports
  `mismatches=4 rows=4` (the r44 base row is missing the `pass=15` needle; the
  r44 superseded row is missing the `pass=15`, `8b82ac99…` and `743 lines`
  needles).
- **F3 (root cause of the staleness is inside the committed snapshot itself).**
  Commit `18fd68b0` ("round-45: SKILL.md registry refresh …") introduced both the
  auditor bytes `8b82ac99…` (743 lines) and the SKILL.md row text describing the
  v2 auditor as `64db765e…`/622 lines/`pass=10` — i.e., the snapshot committed a
  SKILL.md cell describing byte-states that were never the committed file bytes.
  `.ufo/waves/round-45/evidence/registry-audit-all.txt:7-12` corroborates the
  timeline: v2 went through transient byte-states `64db765e` @07:46:24,
  `3e1cec57` @07:48:47, `5f693651` @07:50:22, `a82c1fb5` @07:53:04, before
  `8b82ac99` was stable at run time (07:55:16–07:56:03). The committed row text
  froze the earlier `64db765e` description while the committed file carried
  `8b82ac99`. The repair (worktree SKILL.md, uncommitted `M SKILL.md`) aligns the
  cells to the committed bytes; nothing in the r44 cells claims a value that
  differs from what the committed auditor bytes produce.
- **F4 (cross-check against r44 freeze).** `.ufo/waves/round-44/evidence/freeze-r44.txt:9,20`
  pins the r44-era auditor v1 at sha256 `743996b1…` with `GATE_REGISTRY_SELFTEST pass=6 fail=0`.
  The current committed auditor is a different, expanded v2 (743 lines, 15 arms);
  the repaired cells correctly describe the current committed bytes, not the r44
  freeze bytes.

## Residual risk / verification gaps

- The selftest was executed from the working tree; worktree bytes are identical
  to HEAD bytes (same sha256), so the tally applies to the committed bytes. I did
  not run from a fresh `git archive` checkout; equivalence is by digest only.
- Tally validation is output-matching (15 PASS lines, rc 0). Whether each arm
  genuinely asserts (vs merely completing) was the r44 `CritSelftestHonesty`
  concern, not re-audited here: the row's claim that the *tally* equals the
  selftest output is true.
- The word "stale" applies to the control snapshot (F2/F3), not to the repaired
  cells (F1). No substitution, fabrication, or mismatch was found in the r44
  registry cell against the committed auditor bytes.

No tool was installed or upgraded; no git/jj mutation performed; no file other
than this report was written.
