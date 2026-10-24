# RevReportSections — report-contract readiness gap scan (wave 2)


Seat: `mori-r36-w2-RevReportSections-23` (reviewer leaf; no subagent dispatch).
Item attacked: **the report contract** — `mori-round-36.md` §4 (lines 99–125) + the wave instruction
"the report must open by naming C1 (exploratory, freshness) and C2 (measured, operability)", plus the
report extras (Stale-lane line, tool installs). For each required section I point at the committed
evidence that can fill it, or name the gap. FAIL nothing — gaps are reported as findings.

Canonical runtime: Python 3.14.8 / git backend; lane HEAD `bf0df77fee4b6ef54a90aea09335c7617f125151`
(data commit, pushed). All measurements below are read-only git (`git show`/`git status`/`git ls-tree`)
and `sha256sum`; no lane file edited except this report. No tools installed (nothing to record).

---

## 1. Required-section map (report contract §4 + wave extras)

| # | Required section | Contract source | Committed evidence that fills it | Gap |
|---|---|---|---|---|
| 1 | **Work performed** — opens naming C1 (exploratory, freshness) and C2 (measured, operability); one bullet per work item with an evidence pointer | §4, `mori-round-36.md:104-106`; wave instruction | C1/C2 table + P-C1/P-C2 + exploratory declaration: `.ufo/waves/round-36/contract.md` (committed at bf0df77; declaration section at `:114-125`, added in 5842dc0); freeze `evidence/freeze-v2.txt`; C0 re-score `evidence/c0-rescore-v2.txt`; wave-1 dispatch `w1-dispatch.json` (33 seats) + `w1/swarm-registry.json` + 28 w1 reports; wave-2 dispatch `w2-dispatch.json`/`w2-spec.json` (66 seats); L1 measurement log `dispatch-log.txt:19-34` | w2 dispatch records, `gen-w2-spec.py`, `w2-validate.log` — all still **untracked** (must land with the wave-evidence commit). Pushed-tip contract row 13 contradicts the declaration (see F3) |
| 2 | **Landed changes** — every change tied to a LOG.md entry and the commit that carries it | §4, `mori-round-36.md:107-108` | All changes are at bf0df77: `tools/mori-source-drift.py`, `tools/mori-sources-appendonly.py`, `tools/mori-index-clean.sh`; `corpus/SOURCES.md` rows S205–S220 + copies `corpus/evidence/sources-r36/S205.src…S220.src`; `corpus/QUALITY.md` 103–105 (+25 lines); `SKILL.md` gate-registry rows (+20); `corpus/knowledge/source-drift-r36.md` (re `git diff --stat 6bd57097..bf0df77`) | **LOG.md has no Round-36 entry at bf0df77** (grep → 0 hits; tail ends at Round 35). `SCORECARD.md` has no round-36 section (claim record: score delta / evidence pointer / counting command / measured commit / capability row; C1 exploratory verdict + reviewer pointer). Both are §2/§5 record requirements; see F1/F2 |
| 3 | **Before → after measurements** — one per claim, each with the counting command and the commit measured against | §4, `mori-round-36.md:109-110` | Before receipts committed: `evidence/c1-before.txt` (`tool_absent C1=unmet EXIT=1`), `evidence/c2-before.txt` (`tool_absent C2=unmet EXIT=1`). After receipts exist in the worktree: `evidence/c1-after.txt` (blind 40/40 mismatches=0; real rows=220 oracle_fetched=58 fresh=49 drifted=9 excluded=0 mismatches=0; seed 7388485190103051243), `evidence/c2-after.txt` (blind 24/24; real arm pass; ids=18; seed 15440749816798970567). Counting commands: `python3 .ufo/waves/round-36/count-c1.py bf0df77…` / `count-c2.py bf0df77…`; counter sha256 match freeze pins (verified below) | **After-receipts are untracked at bf0df77** (`git status` → `??` for all three: c1-after.txt, c2-after.txt, drift-live-r36.txt). Until they land in a commit, the report cannot cite them as committed evidence (see F1) |
| 4 | **Sources & frontier** — census before→after with counting command; rows added by tier; rows touched old→new; frontier rows advanced | §4, `mori-round-36.md:111-115`; prompt §2b | Census start committed: `evidence/census-start.txt` (mori ok, exit 0, 13 W04 dup-URL warnings). Rows: 204 at 6bd57097 → 220 at bf0df77 (+16, all new S205–S220; tier A; 15 mined + 1 rejected S211). 18 superseded ids discharged (C2 receipt ids list). Frontier advance: `tools/mori-source-drift.py` now re-fetches every row with a committed copy (live probe `evidence/drift-live-r36.txt`: rows=220 fresh=49 drifted=9 no-copy=162) — first programmatic whole-registry re-fetch; S205 used-by `tools/mori-source-drift.py` | **Census-end receipt not produced yet** (w2 seat ExecCensusEnd is the producer; run is `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` — exit 0 required). **`corpus/lessons/round-36.md` missing** at bf0df77 (mistake-mining + Gate quotes; `git ls-tree bf0df77 corpus/lessons/` shows only round-34/35). The before→after row census must also state the 18 touched ids (C2 receipt) |
| 5 | **Trend verdicts** — expansion / quality / discernment, each with evidence; no scalar | §4, `mori-round-36.md:116-117` | Expansion: 16 new SOURCES rows + knowledge note `corpus/knowledge/source-drift-r36.md` + three new tools. Quality: tool selftests + w2 findings (below). Discernment: C1 axis-fit defect caught before data (w1/CritAxisFit.md, w1/MineCopyFidelity.md; declaration contract.md:114-125) + C0 v2 re-design (`evidence/c0-rescore-v2.txt`) | Verdicts are the L1's writing task; pointers exist. Quality verdict must absorb the w2 findings (F4) — stale "seven drifted" tally repeated in `SKILL.md:858-861`, `corpus/QUALITY.md:841`, `corpus/knowledge/source-drift-r36.md:17`, `corpus/README.md:565` vs measured 9 (S210/S211) |
| 6 | **SHONEN** — one line per box; `[x]` only with named non-author verifier, `[~]` with resolvable pointer, `[ ]` if untouched | §4, `mori-round-36.md:118-119` | SHONEN.md has 4 boxes, all `[ ]`. Pointers exist for `[~]`: SKILL.md gate-registry rows (drift row `SKILL.md:858-861`, append-only row); tool `--selftest` suites; PROVINCE.md + RevNoHarm (no cross-domain bleed). No named non-author verifier exists anywhere | Box 2 ("end-to-end domain task executed and logged") cannot even be `[~]` until LOG.md gets its round-36 entry (F1). No box can be `[x]` |
| 7 | **Stale-lane line** (report extra) | chousa-round-25.md §6 / mori wave context | Dispatch records show one mori mission per attempt (w1-dispatch.json, w2-dispatch.json; orchestrator directive dispatch-log.txt:33-34) | MANIFEST.json / `.ufo/state/` are never-touch for seats — the line is the L1's assertion from its own vantage; seats cannot independently verify "no other mission open" |
| 8 | **Tool installs** (report extra) | tooling directive (operator 2026-10-19) | None recorded by any seat: ExecCensusEnd, ExecReC2A, ExecDriftLive, RevC1Receipt, RevC2Interface, RevC2Receipt, RevMisroot, RevNoHarm and others all state "no tools installed" | None — report records zero installs, verified at report time |

---

## 2. Findings by severity

**F1 — HIGH: the measured "after" evidence is not committed.**
`git status --porcelain` at the lane root shows `??` for `evidence/c1-after.txt`, `evidence/c2-after.txt`,
`evidence/drift-live-r36.txt` (also `gen-w2-spec.py`, `w2-dispatch.json`, `w2-spec.json`,
`w2-taskcall.json`, `w2-validate.log`, `w2/`, `.scratch/`). `git ls-tree bf0df77` contains only the
before-receipts, freeze files, c0-rescore-v2.txt, and the w1 tree. The §4 "Before → after" section cites
after-receipts; those citations hold only after a wave-evidence commit includes them. The worktree bytes are
pinned (sha256 `bdf017cb…` per RevC1Receipt) but uncommitted.

**F2 — HIGH: LOG.md and SCORECARD.md carry no round-36 record at the data tip.**
Commands:
```
git show bf0df77:LOG.md | grep -c "Round 36"        → 0
git show bf0df77:SCORECARD.md | grep -n "Round 36" → (no matches)
```
Contract §4 "Landed changes" requires every change tied to a LOG.md entry, and prompt §2.4/2.6 requires
the per-claim SCORECARD record (score delta, evidence pointer, counting command, measured commit; capability
row for C2; C1 exploratory row with verdict + reviewer pointer). Both are absent at bf0df77. The data
commit's message ("round-36: C1/C2 data — …") is not a LOG.md entry.

**F3 — MED: the pushed tip's contract row 13 contradicts the exploratory declaration; the frozen whole-file
pin is stale.**
`git show bf0df77:.ufo/waves/round-36/contract.md | sed -n '13p'` still reads "freshness (lowest-scoring
non-retired axis …) | flags stale source rows" with an unqualified `C1=met` after-cell, while the same
file's declaration (`:114-125`) says no freshness verdict is admitted and C1 verifies only as
`unprovable-but-better` with a named non-author reviewer, else `unprovable`. `evidence/freeze-v2.txt`
pins contract.md `dbd3f6d7…`; the landed blob hashes `065a17b5…` (RevFreezeIntegrity FAIL) and the worktree
hashes `e0426b8c…`. The P-C1/P-C2 sentences are byte-identical pin→tip (freeze discipline broken, predicate
text intact). The worktree carries an uncommitted row-13 fix — the report must land with that fix so the
pushed artifacts match its opening line.

**F4 — MED: no named non-author reviewer for C1's `unprovable-but-better` is on record.**
`grep -i "non-author\|unprovable-but-better" .ufo/waves/round-36/w1/*` → no matches; no w2 report names a
non-author reviewer. Contract.md:117-125 and the wave instruction require a named non-author reviewer for the
claim to verify as `unprovable-but-better`; otherwise it lands `unprovable` and the report must say so. If no
such reviewer appears before the report, the report must land C1 as **unprovable** (byte-behavior evidence
reported as P-C1 evidence only).

**F5 — MED: `corpus/lessons/round-36.md` is missing** (needed for §2b mistake-mining and §4 Sources &
frontier Gate quotes). `git ls-tree bf0df77 -- corpus/lessons/` lists only round-34/35 lessons.

**F6 — MED: census-end receipt pending.** `evidence/census-start.txt` is committed; the end-run
(ExecCensusEnd, `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`, exit 0 required) has
not landed. §4 requires both outputs.

**F7 — LOW: landed documentation repeats a stale seven-drifted-rows tally.** `SKILL.md:858-861`,
`corpus/QUALITY.md:841`, `corpus/knowledge/source-drift-r36.md:17`, `corpus/README.md:565` (the latter an
uncommitted worktree edit) say all drifted rows were representation differences and list seven ids; the
committed receipt (`evidence/c1-after.txt:3`, `oracle_drifted=9`) and the live probe measure nine, adding
S210/S211 (ExecDriftLive, ExecReC1A, RevQuality105). The report must not repeat the stale count; these are
round findings to carry.

---

## 3. Every measurement in this report

| Measurement | Command | Observed |
|---|---|---|
| Landed tip | `git rev-parse HEAD` | `bf0df77fee4b6ef54a90aea09335c7617f125151` |
| After-receipts committed? | `git status --porcelain` | `?? .ufo/waves/round-36/evidence/{c1-after,c2-after,drift-live-r36}.txt` |
| LOG round-36 entry | `git show bf0df77:LOG.md | grep -c "Round 36"` | `0` |
| SCORECARD round-36 | `git show bf0df77:SCORECARD.md | grep -n "Round 36"` | no matches |
| SOURCES before/after | `git show 6bd57097:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3}'` ; same at bf0df77 | `204` → `220` |
| Counter pins | `sha256sum .ufo/waves/round-36/count-c{1,2}.py` | `86dd3b7a…` (= freeze-v2 line for count-c1.py), `c7edaacfff…` (= pin for count-c2.py) |
| Contract pin vs worktree | `sha256sum .ufo/waves/round-36/contract.md` | `e0426b8c…` ≠ freeze-v2 pin `dbd3f6d7…` (landed blob `065a17b5…`) |
| Named non-author reviewer | `grep -i "non-author" .ufo/waves/round-36/w1/*` | no matches |
| Lesson file | `git ls-tree bf0df77 -- corpus/lessons/` | round-34/35 only |

---

## 4. Residual risk / verification gaps

- Wave 2 is still running (66 seats; ~23 reports landed at scan time). Trend-verdict evidence and the full
  attack corpus finalize when the wave completes; this scan names the evidence sources, not the final wording.
- No LSP device is mounted (`read xd://lsp` → "No such tool"); findings are grounded in cited file text and
  git commands, not semantic references.
- Seats cannot read MANIFEST.json / `.ufo/state/`; the Stale-lane line is verified only from dispatch records.
- The C1/C2 receipts were byte-audited by peer seats (RevC1Receipt PASS, RevC2Receipt PASS, RevC2Oracle PASS,
  ExecReC2A/B fresh-seed replays met); counter hashes match freeze pins. Freeze-discipline drift is
  RevFreezeIntegrity's FAIL and must appear in the report's findings.

## 5. VERDICT: FAIL — report-readiness gaps exist (F1–F7 above; no claim verdict implied). The report
can be made complete by: committing the after-receipts + wave-2 records (F1); adding the LOG.md round-36
entry and the SCORECARD round-36 claim section (F2); landing the contract row-13 fix (F3); either naming a
non-author reviewer or landing C1 unprovable (F4); writing `corpus/lessons/round-36.md` (F5); recording the
census-end receipt (F6); and using the measured nine-drifted-rows counts (F7).
