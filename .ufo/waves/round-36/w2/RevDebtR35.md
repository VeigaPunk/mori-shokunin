# RevDebtR35 — round-35 §6 final disposition

**Scope:** §6 items 1–5 against landed tip `bf0df77fee4b6ef54a90aea09335c7617f125151` (round base `6bd57097`). This review does not infer freshness admission from C1. No tools were installed.

## Finding — MEDIUM: item 4's required post-landing log is absent from the landed tip

QUALITY 103 requires the dispatch log to record the index check after each `landed` line (`corpus/QUALITY.md:822-828`). The criterion and tool are present, and the tool works, but the after-landing result is only in the modified worktree log, not in `bf0df77`. Thus item 4 is not fully evidenced on the requested landed bytes.

- `read corpus/QUALITY.md:822-828` → criterion 103 says the round dispatch log records the check after each `landed` line; it also says the check detects index state after the fact and does not prevent a forbidden git command.
- `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin` → `MORI_INDEX_CLEAN staged=0 intent_to_add=0` (exit 0; present-state check).
- `bash tools/mori-index-clean.sh --selftest` → `MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0`.
- `git show bf0df77fee4b6ef54a90aea09335c7617f125151:.ufo/waves/round-36/dispatch-log.txt` → committed log ends at line 26 with “selftest PASS 4 cases; data commit next, then counters at the landed tip”; it has no committed post-landing index-check entry.
- `git diff -- .ufo/waves/round-36/dispatch-log.txt` → `1 file changed, 8 insertions(+)`; the uncommitted additions include “data commit landed bf0df77…” and “round append-only gate: round_changed=[] exit 0; index clean staged=0 intent_to_add=0”. These additions cannot establish the record at the specified tip.

The tool and the QUALITY criterion landed; the required round-log evidence did not. This is an evidence gap, not a claim that the current index is dirty.

## Item checks

### 1. No calibration claim; C1 is not a freshness verdict — PASS

- `read .ufo/waves/round-36/contract.md:3-6,116-126` → contract states “no calibration claim this round”; C1 is declared exploratory before data and its P-C1 result is “evidence of the probe's byte behaviour, not as C1's verdict”; C2 is the measured claim.
- `read .ufo/waves/round-36/evidence/c1-after.txt:1-6` → P-C1 receipt: `blind_rows=40 ... mismatches=0`, `real_rows=220 ... oracle_drifted=9 ... mismatches=0`, `C1=met`.

The receipt's `C1=met` is only the frozen byte-behaviour predicate result; it does not admit a freshness verdict. This review does not assert freshness or `unprovable-but-better`.

### 2. Supersede dispositions — PASS

- `python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097` →

```text
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S073
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
```

All 18 changed IDs have a named superseder. Superseder row IDs are `S073`, `S201`, `S202`, and `S206`–`S220`; the corresponding targets are exactly the 18 IDs in the output. Source evidence: `corpus/SOURCES.md:79` (S073), `:207-208` (S201–S202), and `:212-226` (S206–S220). S205 is the contract row, not an additional superseder.

### 3. Gate registry and self-test — PASS

- `read SKILL.md:870-874` → Round36 registry lists `SOURCES append-only (r36)` as a gate and specifies `python3 tools/mori-sources-appendonly.py --selftest` (“8 sandbox histories through the CLI”); it also registers index clean as a gate with its self-test.
- `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0`.

### 4. M4/index-clean implementation — PARTIAL; overall FAIL

`corpus/QUALITY.md:822-828` defines the check and its limits; `SKILL.md:866-868,874` registers the tool. The live and self-test outputs above confirm the tool runs, but the required after-landing record is missing from the landed log (finding above). The uncommitted worktree addition is not evidence at `bf0df77`.

### 5. Operator-owned items — no lane debt; promotion remains operator-owned

- `git diff --name-status 6bd57097f7ab2b471b4593ed2019c980b1368c68 bf0df77fee4b6ef54a90aea09335c7617f125151 -- LOG.md SHONEN.md corpus/lessons/round-35-verifier-spotcheck.md` → no changed paths (`status=0`). `git show bf0df77:LOG.md | awk 'NR==1801 {print NR ":" $0}'` → `1801:run although the operator's OMP settings file sets async.maxJobs: 200; ...`. This is the operator setting item, not lane repair debt.
- `git show-ref --verify refs/jj/keep/3b19cacb0444e799b4685e4bb8e8d76fbb51104a` → `3b19cacb0444e799b4685e4bb8e8d76fbb51104a refs/jj/keep/3b19cacb0444e799b4685e4bb8e8d76fbb51104a`. The retained ref exists; it is operator-owned, not a lane-file repair.
- `git status --porcelain -- .scratch/` → `?? .scratch/`. `read .ufo/waves/round-36/dispatch-log.txt:2` → entering state recorded `.scratch/` as untracked, dated `2026-10-21`, and “not this round's”. Operator-owned, not round debt.
- `read SHONEN.md:1-8` → four checklist boxes remain `[ ]`. The diff above shows `SHONEN.md` unchanged across the round. The promotion decision for the prior report's four `[~]` assessments remains operator-owned; no lane promotion was made.

## Residual risk and verification gaps

- QUALITY 103 explicitly provides detection after the fact, not prevention of a forbidden git command.
- The `lsp` device is unavailable: `read xd://lsp` returned “No such tool: xd://lsp” (mounted devices: `ast_edit`, `debug`). No LSP references/definition/diagnostics were available; findings above rely on direct file evidence and read-only gate outputs, not grep as semantic proof.
- The keep ref is present at review time; Git history does not version historical `.git/refs` state.

VERDICT: FAIL — item 4's required post-landing index-clean record is absent from the requested landed tip.
