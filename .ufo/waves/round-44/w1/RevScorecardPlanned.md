# RevScorecardPlanned — round 44, wave 1

Seat: `L1Mori44-4.RevScorecardPlanned` (leaf reviewer; no dispatch, no edits).
Scope: the round's own record-keeping obligations — `SCORECARD.md`'s round-43
declaration/outcome, its `## Planned` sections, its axes table — against the
round-44 declaration and the frozen instruments.

Measured state while I ran: lane `HEAD` = `7cb59c6891d4f5d0266fe062565f094da835dc84`
(freeze commit, committer time `2026-10-25 05:05:23 -0300`); `git status
--porcelain` shows six modified tracked files and the round's drafts uncommitted:
`LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`,
`corpus/SOURCES.md`, `corpus/lessons/round-43.md` (all `+`-only diffs), plus
untracked `corpus/knowledge/pid-probe-conclusion-r44.md`,
`.ufo/waves/round-44/w1-spec.json`, `.ufo/waves/round-44/w1/`,
`.ufo/waves/round-44/assimilation/`. `SCORECARD.md`'s round-44 section grew from
35 to 54 added lines *while I was reading it* (a C3 correction note appeared), so
the draft is a moving target; the findings below are against the state quoted
inline.

---

## (a) What round 43 planned or left planned for round 44, and whether this round's claims match

**No `## Planned` entry exists for round 44.** `grep -n 'Planned' SCORECARD.md`
(freeze bytes) returns exactly five hits: `:27` (round 2), `:44`, `:643` (round
13), `:840` (round 15), `:2025` (round 37). The round-43 declaration
(`:2362-2375`) and measured outcome (`:2377-2392`) contain no next-round plan and
no `## Planned` subsection; `corpus/lessons/round-43.md` and `LOG.md`'s round-43
section name none either (`grep -n -i 'round 44|round-44|next round' LOG.md` at
the freeze commit → no hit; the hit at working-tree `LOG.md:2597` is the
round-44 erratum, not a plan).

The only forward plan round 43 left is the closure's routed list,
`corpus/lessons/round-43-verifier-spotcheck.md` at `1429c791` (`:203-222`):
items 1–6. The round-44 contract (`contract.md` §"Routed defects") claims 3, 4, 5
and reports 1, 2, 6.

Match against the three claims:

| routed item | round-44 claim that answers it | match |
|---|---|---|
| 3 — count slips ("15 checks" observed 14; "34 seat logs" observed 8) | C1 (figure ledger) | yes — witness fixture reproduces both |
| 4 — no `SKILL.md` registry row, no `--selftest` on the two r43 counters | C2 (gate standard) | partial — see H5/M1: C2 certifies the **r44** counters; the two r43 counters stay `REGISTRY=unmet` (that is the witness, not the repair) |
| 5 — C1S receipt at `dde525ea` while the verdict says "landed tip" | none; the declaration says "answered by the tip-run receipt and QUALITY 119" | **no** — see H5 |
| 1, 2, 6 | reported, not fixed (declaration `:13-16`) | as declared |

C3 answers no routed defect; it is the frontier/axis claim the contract declares
(coverage 6). The axis obligation in `templates/round-prompt.md:14-17` ("at least
one claim works the lowest-scoring non-retired axis") is met by C1 on calibration
5. But two of the three tied-lowest axes (depth 5, freshness 5) are untouched and
the draft has no sentence saying so — round 43 had one
(`SCORECARD.md:2386-2387`, "the lowest-axis obligation is worked by C2 on
calibration, tied lowest with depth and freshness"). The round-44 entry needs its
own honest version of that sentence.

The last live `## Planned` block (`SCORECARD.md:2025-2029`, "Planned round 37")
is dangling: it names work (counter timeout-path restructure, `oracle_excluded`
fixture, a lowest-axis claim) that later rounds took up ad hoc, and nothing marks
it executed or superseded. Rounds 38–43 each shipped without a `## Planned`
section. Round 44 should restore the practice with a `## Planned (round 45)`
block; otherwise the next round again has no SCORECARD-derivable mandate.

---

## (b) Do the axes cells' evidence pointers still resolve at the freeze commit?

Every cited path resolves; every quoted fragment is present at the cited line.
Commands run at `7cb59c68` (`git cat-file -e <rev>:<path>` and
`git show <rev>:<file> | awk 'NR==n'`):

| axis | pointer | resolves | fragment at the cited line |
|---|---|---|---|
| coverage | `corpus/knowledge/observability-surfaces-r2.md` | yes (395 lines) | n/a (path citation) |
| coverage | `corpus/lessons/round-24-verifier-spotcheck.md:88` | yes | "Score 6 → 6." |
| coverage | `corpus/lessons/round-26-verifier-spotcheck.md:133` | yes | "| coverage | improved | …" (no number) |
| operability | `SCORECARD.md` round-24 measured outcome ("134 cases") | yes | `:1526` "selftest `PASS (134 cases, 134 passed, 0 failed)`" |
| operability | `corpus/lessons/round-14-verifier-spotcheck.md:87` | yes | "holds coverage6/operability7/depth5/freshness5/calibration5/adjacency6" (the grading "operability | unchanged" is at `:92`, not `:87` — see L1) |
| operability | `corpus/lessons/round-28-verifier-spotcheck.md:93` | yes | "ten A2 rules pinned by 30 frozen cases, PASS 30/30" |
| operability | `corpus/lessons/round-31-verifier-spotcheck.md:155` | yes | "the score stays 7" |
| operability | `tools/mori-blind-check.sh` | yes (366 lines) | n/a |
| depth | `corpus/lessons/round-12-verifier-spotcheck.md:17` | yes | "…score 4→5…" |
| depth | `corpus/lessons/round-31-verifier-spotcheck.md:154` | yes | "score stays 5 unless a closure states the move" |
| freshness | `corpus/README.md` Round21 correction | yes (`:412`) | `:415-417` "CloseMori20 rejected the pin … invalid for acceptance"; `:434` "the invalid r20 baseline is not accepted or re-pinned" |
| freshness | `corpus/lessons/round-28-verifier-spotcheck.md:92` | yes | "| freshness | improved | C1 verified…" |
| freshness | `SCORECARD.md:1771` | yes | "freshness 5 → 6 proposed" |
| freshness | `corpus/lessons/round-14-verifier-spotcheck.md:87` | yes | states freshness5 |
| calibration | `corpus/lessons/round-24-verifier-spotcheck.md:68` | yes | "Score 5 → 5." |
| calibration | `corpus/lessons/round-25-verifier-spotcheck.md:124` | yes | "| calibration | improved | C1 4 → 0 re-measured…" |
| adjacency | `corpus/lessons/round-14-verifier-spotcheck.md:87` | yes | states adjacency6 |
| adjacency | `MANIFEST.json@63729047` rounds[398] | yes (fleet repo `git cat-file -e`) | `"round": 19 … "verdicts": {"adjacency": "improved", …}` |
| adjacency | "no lane spot-check file" | yes | `git cat-file -e 7cb59c68:corpus/lessons/round-19-verifier-spotcheck.md` → rc 128 |

The "round-10 drift pin still red" claim is also true today:
`bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`
→ rc 1, `MORI_DRIFT: +FINDING:CGROUP_OOM_KILL_CUMULATIVE …` (baseline path exists
at the freeze commit).

**Defect B1 (medium, wording, not a broken pointer).** Five cells say "latest
admitted closure grades <axis> improved", but the latest admitted closure at the
entering tip is round 43 (`1429c791`, verdict "Admit", `:226-228`), and its axes
table (`:157-164`) reads:

- operability — improved (`:159`) → the cell's `round-31:155` is 12 rounds stale;
- calibration — improved (`:160`) → the cell's `round-25:124` is 18 rounds stale;
- depth — improved (`:154` of round 42) → the cell's `round-31:154` is 11 rounds stale;
- coverage — **unchanged** (`:161`) → the cell's "latest admitted closure grades
  coverage improved" is false as written (round 26 was the last improvement);
- freshness — **unchanged** (`:163`) → same falsehood (round 28 was the last improvement).

Adjacency's cell is the one that is literally true (r19/MANIFEST is still the
last improvement; r43 grades adjacency unchanged, `:164`). These are durable-record
wording defects: a closure reviewer reading the cells at face value will believe
operability/calibration were last improved by rounds 31/25. Round 44's entry should
append a correction naming each superseded clause (the round-38 "axes-cell
correction" precedent at `SCORECARD.md:2169`), not silently rewrite the cells.

---

## (c) Does the round-43 measured outcome contradict anything round 44 will assert?

Yes — five concrete contradictions, all reproducible from committed bytes.

**C1 (high).** `SCORECARD.md:2381` (round-43 outcome, C1S cell) says
"15 checks PASS". The closure at the entering tip says 14
(`corpus/lessons/round-43-verifier-spotcheck.md:109-115`), and I re-derived it:
`git show 91cb221f:.ufo/waves/round-43/evidence/c1s-after.txt | grep -cE '^check'`
→ **14**. Round 44's witness asserts the same (F03 asserted 15, observed 14).
The round's own errata cover `LOG.md` (working tree, +11 lines) and
`corpus/lessons/round-43.md` (working tree, +21 lines, append-only, report
pointers `0c9e9999:.ufo/reports/round-43/mori.md:45,109,123` verified to carry
"15 checks PASS"/"15 PASS") — but **no erratum is appended under the SCORECARD
round-43 outcome cell**, which is the lane-owned record that still asserts 15.
Round 43's own precedent for this exact situation is the append-only line at
`SCORECARD.md:2373-2375`; round 44 must do the same for `:2381` or the closure
will read two contradictory lane-owned records.

**C2 (high).** `SCORECARD.md:2377` heads the round-43 outcome "tip
`dde525ea…`", while the closure measured the lane tip `91cb221f`
(`round-43-verifier-spotcheck.md:8`) and the round-44 entering tip is
`1429c791` (whose parent is `91cb221f`; verified with `git log --format='%h %p'`).
Round 44's declaration asserts entering tip `1429c791` — consistent with the
closure, contradictory with the lane's own round-43 heading, and routed defect 5
is exactly this. The declaration claims item 5 answered; the durable SCORECARD
heading still names `dde525ea` with no correction. Same remedy as C1.

**C3 (high).** The contract's P-C3 after-sentence — "the same sweep at the landed
tip → 1 file" — is falsified by the artifacts this round is about to commit. The
token `Z ゾンビ` appears in **three** files: the entry
(`corpus/knowledge/pid-probe-conclusion-r44.md`, `source:` line and Claim),
the S471 registry row's `anchor` cell (`corpus/SOURCES.md`, worktree `:250`), and
the new README row (`corpus/README.md`, `## Round-44 coverage additions`).
Measured: `git grep -l 'Z ゾンビ' -- corpus/` (tracked, worktree) → 2 files
(`README.md`, `SOURCES.md`); `grep -rl 'Z ゾンビ' corpus/` → 3 (adds the
untracked entry). At the landed tip the committed sweep is 3, not 1. The frozen
counter does not test this figure, so `C3=met` can print while the round's
declared figure is wrong — the exact class C1 exists to prevent, and
`w1/ExecLedger.md`'s proposed rows contain no row for this sweep, so it would go
unreconciled. The report and any measured-outcome cell must say "0 → 3 files"
(or narrow the path, e.g. `-- corpus/knowledge/` → 1) and the ledger needs a row
for whichever figure is cited.

**C4 (high).** C2's after-value is already met at the **freeze** commit, before
any data seat. Measured:

```
$ python3 .ufo/waves/round-44/count-c2.py 7cb59c68… --counter .ufo/waves/round-44/count-c1.py \
    --counter .ufo/waves/round-44/count-c2.py --counter .ufo/waves/round-44/count-c3.py \
    --mutants-dir .ufo/waves/round-44/fixtures/mutants
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C2=met
rc=0
```

So the transition the declaration presents (before `1429c791` unmet → after
landed tip met) happened inside the round's own freeze commit. The record must
name `7cb59c68` as C2's measured commit (the capability landed there), present the
tip run as a replay/no-harm, and not let a closure read C2 as data-seat work. The
draft's kill rule "a do-nothing control cannot print … `C2=met`" is true only of
the entering-tip control; the freeze state with the flag prints it.

**C5 (high).** The declaration's C2 after-command, **as written**, cannot print
`C2=met`: `--mutants-dir` defaults to the CWD-relative `fixtures/mutants`
(`count-c2.py:168,355`), so from the lane root the committed mutants under
`.ufo/waves/round-44/fixtures/mutants/` are invisible. Measured at the freeze
commit without the flag:

```
check mutant_kill  FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
C2=unmet
rc=1
```

This is the routed-defect-4 class ("the row's documented entry command must
produce the documented verdict") recurring in this round's own row:
`SKILL.md:185`'s entry cell is `python3 .ufo/waves/round-44/count-c2.py <rev>
--counter PATH [--counter PATH ...]` with `--mutants-dir` only in parentheses, and
its pinned-values cell says "`fixtures/mutants/<basename>` beside each counter",
which is not where the counter looks from the lane root. The frozen bytes must not
be patched (route to round 45), but the round-44 declaration/measured-outcome
command must carry `--mutants-dir .ufo/waves/round-44/fixtures/mutants` — otherwise
the entry's own counting command reproduces `C2=unmet` at the landed tip.

**C6 (high).** The C3 entry's `verified-at:` names the freeze tip
`7cb59c6891d4f5d0266fe062565f094da835dc84`, a revision at which the entry does not
exist (`git cat-file -e 7cb59c68:corpus/knowledge/pid-probe-conclusion-r44.md` →
absent; it is untracked). That is routed defect 5 / the round's own QUALITY 119
("a receipt names the revision it measured, and the verdict names that same
revision") violated by the artifact the claim ships. The line should name the
landed tip (or drop the revision and keep the date).

**C7 (medium).** The C3 before-cell cites "registry 243 rows
(`evidence/control-c3-donothing.txt`)", but that receipt contains only
`check entry_present FAIL (absent)` — no row count. The 243 is in
`evidence/census-start.txt` (`rows=243`, census rc 0). Wrong evidence pointer.

Consistent, verified: registry 243 at `1429c791` and 245 in the working tree
(`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 245; census
`validate --root … mori` → rc 0); before-values `C1=unmet`/`C2=unmet`/`C3=unmet`
each rc 1 at `1429c791` matching the three `control-*-donothing.txt` receipts; the
C1 witness `C1=unmet mismatches=2` naming F03 (15 vs 14) and F04 (34 vs 8); the
r43 counts behind it (14 check lines, 8 logs with `provider.rate_limit`, 39 logs
containing `429`, 72 seat logs); freeze pins all match current bytes
(`sha256sum` over the ten pinned paths equals `freeze-r44.txt`); selftest tallies
replay (`C1_SELFTEST pass=6 fail=0`, `C2_SELFTEST pass=5 fail=0`,
`C3_SELFTEST pass=6 fail=0`, `GATE_REGISTRY_SELFTEST pass=6 fail=0`); S471/S472
carry 11 cells each (`awk -F'|'` → NF=12) with no id collision (S470 is the
highest pre-existing id); the entry's `recheck:` counts reproduce live (3 for
`ゾンビ`, 2 for `僵死`).

---

## (d) What the round-44 entry must record per claim, and what is missing from the drafts

The obligation is explicit: `templates/round-prompt.md:20-23` — "run a counting
command you can paste into the report, before and after" and "Record per claim in
SCORECARD.md: the score delta, evidence pointer, counting command, and measured
commit"; `:109-110` — each before→after measurement carries the counting command
**and the commit it was measured against**.

Required values, with the current facts:

| claim | score delta to record | counting command (as it must be written) | evidence pointer | measured commit |
|---|---|---|---|---|
| C1 calibration | 5 → 5 held; verdict "improved, no move" or the honest equivalent; state no move pre-awarded | `python3 .ufo/waves/round-44/count-c1.py <tip>` (ledger default `.ufo/waves/round-44/figures.tsv`) + the witness run | `.ufo/waves/round-44/figures.tsv`, `evidence/c1-after.txt`, `evidence/witness-r43-gates.txt`/fixture run | the landed tip (full sha); every ledger row re-derived there |
| C2 operability | 7 → 7 held; and the capability landed at the **freeze** commit | `python3 .ufo/waves/round-44/count-c2.py <tip> --counter …×3 --mutants-dir .ufo/waves/round-44/fixtures/mutants` | `SKILL.md:183-186`, `evidence/freeze-r44.txt`, `evidence/c2-after.txt`, `evidence/witness-r43-gates.txt` | `7cb59c68…` for the capability; landed tip for the replay |
| C3 coverage | 6 → 6 held | `python3 .ufo/waves/round-44/count-c3.py <tip> --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472` | the entry, `corpus/SOURCES.md` S471/S472, `corpus/README.md` §Round-44, a committed census receipt with `rows=245`, `evidence/c3-after.txt` | the landed tip |

Missing from the drafts I can see (all of them working-tree-only):

1. **The declaration is not committed.** `git log --all -S 'Round 44 declaration'
   -- SCORECARD.md` → empty. Sixteen wave reports already exist under
   `.ufo/waves/round-44/w1/` (first at 05:16; the freeze commit is 05:05:23), so
   the claims are not committed bytes a closure reviewer can `git show`. The
   appended "Round 44 correction … the C3 ground sentence's 'three worlds'"
   (working tree, +19 lines) claims "the declaration's bytes are not rewritten" —
   but no revision holds the superseded bytes, so that supersession is
   unverifiable. Either commit the declaration before appending corrections, or
   drop the correction and commit the corrected claim once.
2. **No per-claim score delta, no Held line, no "no score move pre-awarded".**
   The table's "axis / score" cell gives only the current score; the round-43
   declaration carried the explicit sentence (`:2366`) and outcome carried the
   Held line (`:2384-2387`).
3. **No measured commit per claim** — the after cells say `<landed tip>`. C2's
   true measured commit is the freeze commit (C4).
4. **No after receipts and no ledger.** `evidence/` holds only the freeze,
   witness, census-start and three control receipts; `c1-after.txt`,
   `c2-after.txt`, `c3-after.txt` and `.ufo/waves/round-44/figures.tsv` are
   absent, so C1's after-value is unreachable today.
5. **The C2 after-command is wrong as written** (C5) and the C2 before-command is
   abbreviated (`--counter …`), so neither is pasteable.
6. **Item 5 is asserted answered with no claim and no receipt** (H5):
   `evidence/c1s-tip-run.txt` does not exist; nothing in P-C1/P-C2/P-C3 tests a
   tip-run C1S receipt. Either land and name the receipt under C2's evidence (and
   say it is reported, not scored) or drop the "answered" sentence.
7. **No SCORECARD erratum for the round-43 outcome cell** (C1, C2) — the
   append-only supersession the lane's own round-43 entry demonstrates.
8. **No `## Planned (round 45)` section**, and the only Planned text in the file
   is round 37's dangling block (`:2025-2029`).
9. **QUALITY 117-119 cite `corpus/lessons/round-44.md` as their lesson; at my
   read that file did not exist** (`ls corpus/lessons/round-44.md` → no such
   file). It appeared untracked during this review (177 lines, `## Gate` /
   `## Mistakes` / `## Wave findings` / `## Resource runway`), so the pointer is
   no longer dangling but is still uncommitted, and the corpus additions and the
   lesson must land in the same commit or the pointer is transiently false in
   history.
10. **The C3 after-figure is wrong** (C3) and no ledger row covers it.
11. **C3's entry `verified-at:` names a revision where the entry is absent** (C6).

Also worth recording as scope, not defect: `freeze-r44.txt` pins `SKILL.md`
(`f9b1e2bf…`) although the contract's Freeze sentence pins only the counters,
`tools/mori-gate-registry.py`, the fixtures and the contract. Since C2's rows
already exist in `SKILL.md` at the freeze commit (`:183-186`, all eight cells
non-empty, all three entry paths resolve — `mori-gate-registry.py --rev 7cb59c68
--audit …` → `REGISTRY=met`), the round should state that the SKILL.md pin is a
baseline observation, not an amendment ban; otherwise any later SKILL.md edit
silently invalidates the freeze receipt.

---

## Residual risk and verification gaps

- I could not measure a landed tip (the round has no round-44 commit). C3's
  "3 files" is measured on the working tree (2 tracked + 1 untracked); the
  tip value is inferred from the three artifacts that will be committed
  (`[INFERENCE]`, stated as such).
- I re-ran the frozen counters and the auditor, the census, the drift gate, and
  the two page `recheck:` counts; I did not re-open the two source pages for
  content (that is `ScoutSources490`/`CritAssimilationGate`'s ground), so the
  entry's quotes are not re-verified here.
- The axes-cell staleness (B1) is a durable-record wording defect; it does not
  change any score, and I did not edit the file.
- The round-44 SCORECARD section was still being appended to during this review;
  line numbers for the draft are as of the quoted read (54 added lines).
