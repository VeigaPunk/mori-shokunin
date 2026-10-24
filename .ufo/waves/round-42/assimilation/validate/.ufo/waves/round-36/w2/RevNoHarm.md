# Round 36 wave 2 — no-harm audit

**Item attacked:** full diff `6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151`; lane-locality, deletions, SOURCES append-only behavior, protected-document bytes, remediation, and census/oracle/silence surfaces.

## Findings by severity

### Medium — added remediation instructions conflict with detection/report-only scope

`corpus/knowledge/source-drift-r36.md:27-28` adds reader actions to “save a byte copy under `corpus/evidence/...`” and “Restore `DIR/corpus/SOURCES.md`”. These instruct filesystem writes/restoration rather than detection/reporting only. The latter is an explicit repair instruction. Evidence: reading lines 27–28 returned those exact instructions.

### Medium — added counter can issue SIGKILL

`.ufo/waves/round-36/count-c2.py:70-82` starts a subprocess with `start_new_session=True`, then on timeout calls `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` to terminate its process group. This is scoped to the counter's own child process group, not a host service, but it is still an added kill operation and violates the stated no-kills boundary literally. Evidence: reading lines 70–83 showed the launch and timeout handler.

## Audit measurements

- Command: `git diff-tree -r --no-commit-id --name-status 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151`.
  Observed summary: **115 A, 3 M**; every path below is relative to the lane root. No absolute, parent (`..`), fleet-root, or sibling-repository path is changed.
- Command: `git diff --diff-filter=D --name-only 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151`.
  Observed output: empty; **0 deletions**.
- Command: `git diff --numstat 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- corpus/SOURCES.md`.
  Observed output: `16  0  corpus/SOURCES.md`. The corresponding diff contains only 16 added registry rows S205–S220; no existing row was edited or removed.
- Command: `git diff --quiet 6bd57097..bf0df77fee4b6ef54a90aea09335c7617f125151 -- SCORECARD.md SHONEN.md PROVINCE.md`.
  Observed output: exit 0 (byte-identical at the two endpoints).
- Full changed-path inventory below shows no existing census, oracle, or silence runtime/data surface changed. Round evidence additions include `evidence/census-start.txt` and the two new counter reference files under `evidence/refs/`; the only corpus registry change is the documented SOURCES append.
- No tools were installed or updated. The mounted tool list has no `lsp` device (`read xd://lsp` returned “No such tool”); this path/content audit did not perform caller/definition/diagnostic checks.

## Every changed path and classification

**Round-36 control-wave record/program additions**

- `.ufo/waves/round-36/c0-dispatch.json` — dispatch metadata.
- `.ufo/waves/round-36/c0/CtlJ1.md`
- `.ufo/waves/round-36/c0/CtlJ10.md`
- `.ufo/waves/round-36/c0/CtlJ11.md`
- `.ufo/waves/round-36/c0/CtlJ12.md`
- `.ufo/waves/round-36/c0/CtlJ13.md`
- `.ufo/waves/round-36/c0/CtlJ2.md`
- `.ufo/waves/round-36/c0/CtlJ3.md`
- `.ufo/waves/round-36/c0/CtlJ4.md`
- `.ufo/waves/round-36/c0/CtlJ5.md`
- `.ufo/waves/round-36/c0/CtlJ6.md`
- `.ufo/waves/round-36/c0/CtlJ7.md`
- `.ufo/waves/round-36/c0/CtlJ8.md`
- `.ufo/waves/round-36/c0/CtlJ9.md`
- `.ufo/waves/round-36/c0/CtlK1.md`
- `.ufo/waves/round-36/c0/CtlK10.md`
- `.ufo/waves/round-36/c0/CtlK11.md`
- `.ufo/waves/round-36/c0/CtlK13.md`
- `.ufo/waves/round-36/c0/CtlK2.md`
- `.ufo/waves/round-36/c0/CtlK3.md`
- `.ufo/waves/round-36/c0/CtlK4.md`
- `.ufo/waves/round-36/c0/CtlK5.md`
- `.ufo/waves/round-36/c0/CtlK6.md`
- `.ufo/waves/round-36/c0/CtlK7.md`
- `.ufo/waves/round-36/c0/CtlK8.md`
- `.ufo/waves/round-36/c0/CtlK9.md`
- `.ufo/waves/round-36/c0/controls/J1.py`
- `.ufo/waves/round-36/c0/controls/J10.py`
- `.ufo/waves/round-36/c0/controls/J11.py`
- `.ufo/waves/round-36/c0/controls/J12.py`
- `.ufo/waves/round-36/c0/controls/J13.py`
- `.ufo/waves/round-36/c0/controls/J2.py`
- `.ufo/waves/round-36/c0/controls/J3.py`
- `.ufo/waves/round-36/c0/controls/J4.py`
- `.ufo/waves/round-36/c0/controls/J5.py`
- `.ufo/waves/round-36/c0/controls/J6.py`
- `.ufo/waves/round-36/c0/controls/J7.py`
- `.ufo/waves/round-36/c0/controls/J8.py`
- `.ufo/waves/round-36/c0/controls/J9.py`
- `.ufo/waves/round-36/c0/controls/K1.py`
- `.ufo/waves/round-36/c0/controls/K10.py`
- `.ufo/waves/round-36/c0/controls/K11.py`
- `.ufo/waves/round-36/c0/controls/K13.py`
- `.ufo/waves/round-36/c0/controls/K2.py`
- `.ufo/waves/round-36/c0/controls/K3.py`
- `.ufo/waves/round-36/c0/controls/K4.py`
- `.ufo/waves/round-36/c0/controls/K5.py`
- `.ufo/waves/round-36/c0/controls/K6.py`
- `.ufo/waves/round-36/c0/controls/K7.py`
- `.ufo/waves/round-36/c0/controls/K8.py`
- `.ufo/waves/round-36/c0/controls/K9.py`

**Round-36 contract, counter, and evidence additions**

- `.ufo/waves/round-36/contract.md` — frozen contract.
- `.ufo/waves/round-36/count-c1.py` — frozen C1 counter.
- `.ufo/waves/round-36/count-c2.py` — frozen C2 counter.
- `.ufo/waves/round-36/dispatch-log.txt` — round dispatch/landing record.
- `.ufo/waves/round-36/evidence/c0-rescore-v2.txt` — control rescore receipt.
- `.ufo/waves/round-36/evidence/c1-before.txt` — pre-data C1 receipt.
- `.ufo/waves/round-36/evidence/c2-before.txt` — pre-data C2 receipt.
- `.ufo/waves/round-36/evidence/census-start.txt` — census baseline receipt.
- `.ufo/waves/round-36/evidence/freeze-v2.txt` — v2 freeze hashes/receipt.
- `.ufo/waves/round-36/evidence/freeze.txt` — v1 freeze record.
- `.ufo/waves/round-36/evidence/refs/ref-c1.py` — reference counter logic.
- `.ufo/waves/round-36/evidence/refs/ref-c2.py` — reference counter logic.
- `.ufo/waves/round-36/w1-dispatch.json` — wave dispatch metadata.
- `.ufo/waves/round-36/w1-spec.json` — wave specification.
- `.ufo/waves/round-36/w1/swarm-registry.json` — wave registry.

**Wave-1 reports/drafts**

- `.ufo/waves/round-36/w1/BuildAppendTool.md`
- `.ufo/waves/round-36/w1/BuildIndexCheck.md`
- `.ufo/waves/round-36/w1/ConnSiblings.md`
- `.ufo/waves/round-36/w1/CritAxisFit.md`
- `.ufo/waves/round-36/w1/DraftDriftKnowledge.md`
- `.ufo/waves/round-36/w1/DraftQuality103.md`
- `.ufo/waves/round-36/w1/DraftSkillRows.md`
- `.ufo/waves/round-36/w1/MineCopyFidelity.md`
- `.ufo/waves/round-36/w1/ReviewDebtList.md`
- `.ufo/waves/round-36/w1/ReviewPredicateIdentity.md`
- `.ufo/waves/round-36/w1/ScoutSurfaces.md`
- `.ufo/waves/round-36/w1/SentinelSafety.md`
- `.ufo/waves/round-36/w1/SrcCorpus.md`
- `.ufo/waves/round-36/w1/SupS041.md`
- `.ufo/waves/round-36/w1/SupS044.md`
- `.ufo/waves/round-36/w1/SupS051.md`
- `.ufo/waves/round-36/w1/SupS062.md`
- `.ufo/waves/round-36/w1/SupS064.md`
- `.ufo/waves/round-36/w1/SupS179.md`
- `.ufo/waves/round-36/w1/SupS180.md`
- `.ufo/waves/round-36/w1/SupS181.md`
- `.ufo/waves/round-36/w1/SupS183.md`
- `.ufo/waves/round-36/w1/SupS184.md`
- `.ufo/waves/round-36/w1/SupS185.md`
- `.ufo/waves/round-36/w1/SupS186.md`
- `.ufo/waves/round-36/w1/SupS188.md`
- `.ufo/waves/round-36/w1/SupS189.md`
- `.ufo/waves/round-36/w1/SupS190.md`

**Lane documentation and corpus additions/append-only changes**

- `SKILL.md` — modified; round-36 tool registry/usage rows appended.
- `considerthese/2026-10-23.md` — daily reflection added.
- `corpus/QUALITY.md` — modified; criteria 103–105 appended.
- `corpus/SOURCES.md` — modified; rows S205–S220 appended only.
- `corpus/evidence/sources-r36/S205.src`
- `corpus/evidence/sources-r36/S206.src`
- `corpus/evidence/sources-r36/S207.src`
- `corpus/evidence/sources-r36/S208.src`
- `corpus/evidence/sources-r36/S209.src`
- `corpus/evidence/sources-r36/S210.src`
- `corpus/evidence/sources-r36/S211.src`
- `corpus/evidence/sources-r36/S212.src`
- `corpus/evidence/sources-r36/S213.src`
- `corpus/evidence/sources-r36/S214.src`
- `corpus/evidence/sources-r36/S215.src`
- `corpus/evidence/sources-r36/S216.src`
- `corpus/evidence/sources-r36/S217.src`
- `corpus/evidence/sources-r36/S218.src`
- `corpus/evidence/sources-r36/S219.src`
- `corpus/evidence/sources-r36/S220.src`
- `corpus/knowledge/source-drift-r36.md` — new C1 knowledge entry.

**New lane tools**

- `tools/mori-index-clean.sh` — index cleanliness check.
- `tools/mori-source-drift.py` — source-copy drift probe.
- `tools/mori-sources-appendonly.py` — SOURCES history gate.

No other changed paths were present in the target range. The protected-document, deletion, lane-locality, and SOURCES append-only checks passed; the two scope violations above make this audit fail.

Report: `.ufo/waves/round-36/w2/RevNoHarm.md`
VERDICT: FAIL — remediation instructions and timeout SIGKILL logic are present in added text/code.