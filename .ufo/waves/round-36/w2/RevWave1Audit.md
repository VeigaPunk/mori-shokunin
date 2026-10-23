measured 2026-10-23T18:54:19Z

# RevWave1Audit — mori r36 wave 2 — wave-1 seat accounting recount

Attacks: the wave-1 seat accounting — dispatch count (33), report count (28), the 2 dead /
2 refused-hold exclusions, and the identity + return status of the 1 unaccounted seat.
Seat: leaf member, no subagents. Lane untouched except this report. No tools installed
(nothing to record under the tooling authorization).

## 1. Dispatch task count = 33

Command: read `.ufo/waves/round-36/w1-dispatch.json` (jq `.counts`):
```
"counts": { "spawn": 33, "resume": 0, "total": 33 }   (w1-dispatch.json:16-20)
```
Command: read `w1-dispatch.json?q=[.taskCall.tasks[].name]` → 33 names:
BuildDriftTool, BuildAppendTool, BuildIndexCheck, SrcCorpus, SupS041, SupS044, SupS051,
SupS062, SupS064, SupS179, SupS180, SupS181, SupS183, SupS184, SupS185, SupS186, SupS188,
SupS189, SupS190, DraftDriftKnowledge, DraftSkillRows, DraftQuality103, MineCopyFidelity,
ConnSiblings, ScoutSurfaces, CritC1Counter, CritC2Counter, MutC1Novel, MutC2Novel,
ReviewPredicateIdentity, CritAxisFit, SentinelSafety, ReviewDebtList.
Cross-check — spawn source `w1-spec.json` (jq `{wave,n_items:(.items|length),names:[.items[].name]}`):
`wave: "mori-r36-w1"`, `n_items: 33`, names identical to the dispatch list.

## 2. Reports on disk = 28 (+ swarm-registry.json)

Command: glob `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/*`
(hidden, gitignore off, limit 200) → 29 entries, no truncation:
28 `.md` files + `swarm-registry.json`. The 28: BuildAppendTool, BuildIndexCheck,
ReviewDebtList, SupS062, SrcCorpus, SupS051, SupS184, SupS190, CritAxisFit, SentinelSafety,
SupS179, SupS064, SupS186, SupS189, SupS041, SupS181, DraftSkillRows, SupS044, SupS180,
SupS188, ScoutSurfaces, DraftQuality103, SupS185, MineCopyFidelity, SupS183,
DraftDriftKnowledge, ReviewPredicateIdentity, ConnSiblings.

Landed record agrees: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C
/home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r bf0df77fee4b6ef54a90aea09335c7617f125151
--name-only -- .ufo/waves/round-36/w1/ .ufo/waves/round-36/dispatch-log.txt` → exactly the
28 `w1/*.md` + `w1/swarm-registry.json` + `dispatch-log.txt`.

## 3. Set difference: dispatch minus reports = 5 names

BuildDriftTool, CritC1Counter, CritC2Counter, MutC1Novel, MutC2Novel.
Command: `for n in BuildDriftTool CritC1Counter CritC2Counter MutC1Novel MutC2Novel; do
p=.ufo/waves/round-36/w1/$n.md; [ -e "$p" ] && echo "EXISTS $n" || echo "ABSENT $n"; done`
→ `ABSENT` for all five.

Declared exclusions verified against `dispatch-log.txt`:
- `dispatch-log.txt:15` — MutC1Novel, MutC2Novel dead (provider rate limit, 12:04Z), "dead, not replaced".
- `dispatch-log.txt:16` — CritC1Counter refused by provider (cyber_policy, 14 s), "hold, not retried".
- `dispatch-log.txt:17` — CritC2Counter refused by provider (cyber_policy, 29 s), "hold, not retried".

## 4. The 33rd task: BuildDriftTool — did NOT return

Every dispatch task carries a `Report:` trailer (jq
`[.taskCall.tasks[]|{name,report:(.task|(capture("(?m)^Report: (?<r>.+)$")|.r))}]`);
all 33 point at `.ufo/waves/round-36/w1/<TaskName>.md`. BuildDriftTool's trailer names
`.ufo/waves/round-36/w1/BuildDriftTool.md` — that file is ABSENT (§3), and a lane-wide
grep for `BuildDriftTool` in `.ufo/waves/round-36` finds it only in w1-dispatch.json:26,238,
w1-spec.json:8, and w1/swarm-registry.json:8 (registry/dispatch bookkeeping, no report).
Conclusion: BuildDriftTool did not return a report.

Reconciliation (truthful):
`33 = 28 reports + 2 dead (MutC1Novel, MutC2Novel) + 2 refused-hold (CritC1Counter,
CritC2Counter) + 1 (BuildDriftTool: no report, no return)`.

## 5. Findings

### F1 [moderate — committed seat-accounting record is false] dispatch-log.txt:21
`dispatch-log.txt:21` records "w1 reports (30/33; MutC1Novel, MutC2Novel dead rate-limited;
CritC1Counter, CritC2Counter provider cyber_policy hold)". 30 is arithmetically impossible
under any reading: 33 − 2 dead − 2 hold = 29 maximum seats that could have returned reports,
and the landed tree at the same tip (bf0df77) contains exactly 28. The line as written also
double-counts: 30 + the 4 named exclusions = 34 > 33. The true count is 28 (§2) and the
attempt-2 operator claim ("28 reports … 1 unaccounted") is correct; the committed log line is
not. Lane-wide grep for `30/33`: only occurrence is dispatch-log.txt:21 — no claim, contract,
or counter cites it, so this does not touch C1/C2 or the routed repairs; it is a false count
in the permanent round record (tracked at bf0df77, verified by the ls-tree in §2).

### F2 [minor — "never built" claim contradicted by seat-scratch artifact] dispatch-log.txt:25
`dispatch-log.txt:25` states "tools/mori-source-drift.py was never built by attempt 1 — L1
built it to the frozen interface". A build exists at
`/fast/scratch/hyaku/mori-r36/BuildDriftTool/tools/mori-source-drift.py`:
- `/usr/bin/stat -c '%y %s %n' <scratch> <lane-tool>` →
  `2026-10-23 09:26:50.552379884 -0300 17911 …/BuildDriftTool/tools/mori-source-drift.py`
  (= 12:26:50Z, inside the wave-1 window: dispatched ~12:03Z, settle deadline 12:50Z,
  dispatch-log.txt:13,20) and
  `2026-10-23 15:19:31.911643420 -0300 15189 …/lane/tools/mori-source-drift.py` (= 18:19Z,
  the attempt-2 L1 rebuild per dispatch-log.txt:25-26).
- `python3 -c "import ast,…ast.parse(f) for f in …"` → `both parse OK` (scratch build is a
  syntactically complete Python tool, not a truncated fragment).
- `sha256sum` → scratch `460c34a970b8acbc…`, lane `578667ca3ad0a3a8…`; `diff | wc -l` → 655.
  The landed lane tool is a different build from the one sitting in the seat's scratch dir.
As written ("never built"), dispatch-log.txt:25 is contradicted by this artifact; it is true
only under the charitable reading "never delivered/landed by attempt 1". Attribution of the
scratch build to the BuildDriftTool seat is [INFERENCE] from the seat-named directory and the
in-window timestamp; the writer is not directly witnessed.

### F3 [observation — registry is non-evidentiary] w1/swarm-registry.json
jq `[.members|to_entries[]|{n:.key,agentId:.value.agentId,item:.value.item}]` → all 33
members have `agentId: null, item: null` (members carry only kind/agentId/role/item). The
registry records no return for ANY seat, so report files on disk are the only return
evidence; bare `history://` lists no wave-1 seat agents in this session's registry (past-
session subagents are not persisted), so harness transcripts cannot corroborate either.

## 6. Residual risk and verification gaps

- Scratch mtime proves existence at 12:26:50Z, not completion or authorship (F2 inference).
- `agentId: null` for all members means I cannot distinguish "never spawned" from "spawned,
  lost" for any of the 5 non-reporting seats from lane records alone; dispatch-log.txt:15-17
  documents the 4, nothing documents BuildDriftTool's fate.
- Report contents were not audited (accounting scope only): the 28 files' internal quality,
  and whether CritC1Counter/CritC2Counter "findings none" (log:16) is fair, are other seats' items.
- No remediation performed (mori province: detection and report only).

## 7. Verdict basis

The item's FAIL trigger is "the arithmetic cannot be made truthful". It can, and is (§4):
28 + 2 + 2 + 1 = 33 with the 1 identified by name as BuildDriftTool, which did not return
(its report file is absent). The accounting claim under attack verifies true. F1/F2 are
defects in the dispatch-log working record (committed, but cited by no claim); F3 is an
observation limiting future audits.

VERDICT: PASS — assigned arithmetic truthful (33 = 28 + 2 + 2 + 1; 33rd = BuildDriftTool, no return); FAIL trigger does not fire. Defects F1 (dispatch-log.txt:21 false "30/33") and F2 (dispatch-log.txt:25 "never built" vs scratch artifact) reported above for the record owners.
