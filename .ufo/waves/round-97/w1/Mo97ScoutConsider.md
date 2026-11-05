# Mo97ScoutConsider — round 97 w1, scout seat (proposals triage)

Lane: mori (fleet & host observability). Scope: read-only triage of the operator's
`considerthese/` proposals against this round's landing `e85ed91249953094b067554bfa79fcdc65791f8e`
and earlier revisions. No implementation, no remediation, no git/jj mutation, no writes outside
this report file and my scratch `$HYAKU_SCRATCH/mori-r97/Mo97ScoutConsider` (removed on exit).

## 0. What I read

```
$ cat -n /home/vgpnk/Projects/shokunin/mori-shokunin/considerthese/2026-11-05.md   # 5 proposals, lines 15-19
$ cat -n /home/vgpnk/Projects/shokunin/mori-shokunin/considerthese/2026-10-26.md   # 4 proposals, lines 47-60
$ cat -n /home/vgpnk/Projects/shokunin/mori-shokunin/considerthese/2026-10-25.md   # 5 proposals, lines 44-58
$ cat -n /home/vgpnk/Projects/shokunin/mori-shokunin/considerthese/2026-10-24.md   # 4 proposals, lines 21-24
```

The newest file is `2026-11-05.md` (read from `master` at `2dc476d7`, the round-95 freeze). The
prior file is `2026-10-26.md`; `2026-10-26.md:57-60` is itself the lane's own adoption status line
for the `2026-10-25.md` file. The lane's own record of adoption status:

```
$ grep -c -i "considerthese" corpus/lessons/round-9*.md
round-90: 1   round-91: 2   round-92: 4   round-93: 2   round-94: 2   round-95: 1   round-96: 0   round-97: 0
```

So r96 and r97 published **no** considerthese status: the r96 lesson has no such section, and
neither does the r97 lesson (`grep -n "^#" corpus/lessons/round-97.md` → Claims / Gate / Mistakes /
routed-defect disposition / Frontier step only). Nothing in the r97 landing (`git show --stat
e85ed912` → `SKILL.md`, `corpus/SOURCES.md`, 3 pinned copies, `S628.md`, `corpus/lessons/round-97.md`)
touches a proposal.

## 1. Proposal triage — 2026-11-05.md (the 5 proposals marked "nothing acted on")

| # | file:line | proposal (verbatim head) | implemented by landing e85ed912 or earlier? | evidence |
|---|---|---|---|---|
| 1 | `considerthese/2026-11-05.md:15` | "Track a 'met as frozen vs admitted' ledger per window." | **NO** | no artifact computes an admitted share. `git grep -rn -i "admitted_share\|admitted share\|share of rounds" -- .` → only the proposal line itself. The closest tool, `tools/mori-scorecard-calibration.py`, reads *`MANIFEST.json` rounds[] rows* (`load_expectations`, lines 70-95) and reconciles the SCORECARD `Last change` cell — it never reads `corpus/lessons/round-*-verifier-spotcheck.md` (grep: 6 tools mention the filename, all in docstrings) and never computes a share. Data needed exists but is unused: 13 spotcheck lessons carry "Not admitted" (20 occurrences). |
| 2 | `considerthese/2026-11-05.md:16` | "Ask João for a read-only fleet snapshot path." | **NO** (and not lane-actionable) | the counters still hardcode the fleet root: `.ufo/waves/round-93/count-c1.py:39` and `count-c2.py:39` → `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`; `round-94/count-c1v2.py:131` → `$SHOKUNIN_ROOT/scripts/sources-census.sh`. The r97 counters need no fleet root (grep for `SHOKUNIN_ROOT\|sources-census` in both → 0 hits), so r97 is unaffected, but the ask stands for the r93/r94 counters. The ask is addressed to the operator, so it is a lane *report*, not a lane task. |
| 3 | `considerthese/2026-11-05.md:17` | "Log selftest and pin-check runtimes." | **NO** | nothing records a gate's wall time. `grep -c -E "time\.monotonic\|perf_counter" tools/mori-pin-check.py` → **0**; pin-check has `TIMEOUT_S = 600` (`tools/mori-pin-check.py:176`) but no elapsed field. No wave evidence records a duration (`git grep -rn -E "elapsed_s\|runtime_s\|duration_s" -- '.ufo/waves/'` → only round-13 `elapsed_s` JSON from the census harness, never a gate runtime). Measured this round: `pin-check --selftest` = **14.10 s**; the four r97-registered tools' selftests = 0.02–0.55 s. The operator's own datapoint is `considerthese/2026-11-05.md:5`: "`mori-pin-check.py --rev HEAD` (timed out at 100 s)". |
| 4 | `considerthese/2026-11-05.md:18` | "Sweep sibling lanes for the host-path literal, report only." | **PARTLY — implemented as a recurring connector seat, not as a standing sweep** | sibling sweeps run every round: `.ufo/waves/round-93/w1/Mo93Conn01.md` ("10 of 20 sibling lanes affected; 188 files; 435 matching lines"), `round-95/w1/Mo95Conn01.md` ("9,381 matching files … 21 lane directories with hits"), `round-96/w1/conn/ConnRound.md`. So the *measurement* is implemented; the *proposal's own wording* ("a read-only grep **in my review**") is not — the operator's daily reflection still carries no such grep. |
| 5 | `considerthese/2026-11-05.md:19` | "Report a mutation-survivor trend." | **NO** | survivor counts exist only per-round inside individual lessons (`git grep -n -o "survivors=[0-9]*" -- 'corpus/lessons/round-9*.md'` → r90 `survivors=0`/`survivors=3`, r95 `survivors=0`/`survivors=4`/`survivors=0`); there is no ledger, counter or tool that aggregates them per round: `git grep -rn -i "survivor" -- tools/` → only `mori-pin-check.py` (a selftest arm name), `mori-round17-context-check.py` (a fixture name), `tools/fixtures/mori-pressure/supplementary-cases.json` (a note). The r97 counters carry **no** mutant arms at all (`grep -c -i "mutant\|survivor" .ufo/waves/round-97/count-c1.py .ufo/waves/round-97/count-c2.py` → 0 and 0), so r97 cannot contribute a survivor point even if the ledger existed. |

## 2. Proposal triage — 2026-10-26.md (the 4 proposals in the immediately prior file)

Status per the lane's own record: `corpus/lessons/round-93.md:90-92` ("`considerthese/2026-10-26.md`
says of its four suggestions that 1 is adopted (QUALITY 123), 2 is adopted as a criterion (QUALITY 127),
and 3 is adopted (round 49 flagged-fixed count) — the file's own status line (suggestion 4). No proposal
is 'still unimplemented', so none was mined.") and `corpus/lessons/round-94.md:66-69` (suggestion 3
executed as `evidence/rerun-r93-counters-at-8edbb86d.txt`).

| # | file:line | proposal | status | evidence |
|---|---|---|---|---|
| 1 | `considerthese/2026-10-26.md:47` | Split pin-check mismatches into "can't run here" vs "stale" | **IMPLEMENTED** | `tools/mori-pin-check.py:141-151, 860-880` (`class=env` / `class=stale`, `env=N stale=N`); QUALITY 138 at `corpus/QUALITY.md:1283`. |
| 2 | `considerthese/2026-10-26.md:51` | Follow the unfixed critic flags forward (carry-over ledger) | **PARTLY** | a one-round counter exists (`git ls-files` → `.ufo/waves/round-49/flagged-fixed/count-flagged.py`, `defects.jsonl`), but no carry-over across rounds: `git ls-files '.ufo/waves/round-*/flagged-fixed/*'` → round-49 only. No round-95/96/97 artifact tracks flags forward. |
| 3 | `considerthese/2026-10-26.md:54` | Re-execute what closures only evidence-verified | **IMPLEMENTED** | `.ufo/waves/round-94/evidence/rerun-r93-counters-at-8edbb86d.txt` (head: "considerthese 2026-10-26 suggestion 3 (criterion 136) … C1=met trio=98 … rev=8edbb86d6384"); QUALITY 136. |
| 4 | `considerthese/2026-10-26.md:57` | Keep a suggestion-adoption status line | **IMPLEMENTED then LAPSED** | the line existed in r91–r95 lessons (grep counts above); it is absent from the r96 and r97 lessons, so the newest file (2026-11-05) currently has no lane-side status. |

Earlier files (`2026-10-25.md` lines 44-58, `2026-10-24.md` lines 21-24) are each marked adopted or
mined in the lane's own lessons (r92:70-89, r93:86-92, r94:63-69, r95:101) — items 1, 2, 3 and 4 of
`2026-10-25.md` map to QUALITY 123 / 127 / the r49 flagged-fixed count / the "where did my suggestions
go" status line. Item 5 of `2026-10-25.md` ("Track retries") is only partly realised:
`tools/mori-driver-liveness.py:23,55,60,151` parses `lane-dead-no-report` and `retry same round`
events, but no per-round retry count is committed anywhere (`git grep -rn -i "retry_count\|retries="
-- tools/ corpus/` → no lane ledger).

## 3. The ONE still-unimplemented proposal I nominate

**`considerthese/2026-11-05.md:17`** — verbatim:

> "3. **Log selftest and pin-check runtimes.** `mori-pin-check.py --rev HEAD` took over 100 s today.
> Recording runtime per tool per day would show gates drifting toward timeouts before they fail."

Why this one, and why it fits this lane's PROVINCE:

- **Still unimplemented**, measured three ways: no timing call in the gate (`grep -c` → 0 in
  `mori-pin-check.py`), no runtime field in any gate output or receipt, no runtime artifact in any
  wave evidence file.
- **In province.** PROVINCE owns "lane counters", "`.ufo/waves/*` settlement state", watchdog
  liveness/log freshness and the lane's own evidence (`PROVINCE.md:6-10`, `:125`, `:132`), and the
  round-18 note places "own-evidence retention" and instrument-grade gates in Core. A gate's own
  runtime is lane observability: `mori-pin-check.py` is the lane's gate reconciler
  (`PROVINCE.md:572`, `SKILL.md:1317` registry row "registry pin reconciler (r47, C1)"). This is
  detection-and-report only: the lane would *record* a runtime, never tune a timeout or a service.
- **Converts into a QUALITY criterion/lesson next round, in the lane's existing idiom.** The natural
  criterion is the missing half of QUALITY 138: *"a gate timeout is classified, and the gate's
  measured runtime is recorded, so a drifting gate is reported before it fails."* Concretely,
  `tools/mori-pin-check.py:587-593` already classifies a timeout as `env` vs `stale` for *pins*, but
  the lane's own **frozen counters** do not: neither `count-c1.py` nor `count-c2.py` catches
  `subprocess.TimeoutExpired` (`grep -c TimeoutExpired` → 0 and 0) although both set
  `timeout=600`/`timeout=900` (`.ufo/waves/round-97/count-c1.py:70,99`; `count-c2.py:77,133`).
  I reproduced the resulting crash on a scratch copy of the frozen C1 counter (timeout patched
  900 → 2 s, tool made to hang): stdout is **0 bytes**, stderr ends
  `subprocess.TimeoutExpired: … timed out after 2 seconds`, rc=1. A receipt built on
  `grep '^C1='` therefore sees *nothing* and cannot distinguish "the instrument hung" from "the
  predicate is false" — precisely the env/stale ambiguity QUALITY 138 fixed for pins and never
  carried to the counters. The lesson candidate for r98 is therefore concrete and falsifiable: a
  counter that runs a gate under a timeout must print a *named* outcome (e.g. `C1=unmet
  … timeout=1`) and record the elapsed seconds, so a slow-but-green gate is visible as slow.
  This also protects the lane's own operability axis: the four tools this round registered in
  `SKILL.md` are exactly the class that a future reviewer would want timed.

I deliberately do **not** nominate proposal 4 (sibling host-path sweep): the measurement already
runs every round as a connector seat, so a new standing sweep would duplicate existing practice.
I do **not** nominate proposal 1 (admitted-share ledger): it is a lane-internal bookkeeping artifact
with no `PROVINCE.md` ownership surface (the fleet record is `MANIFEST.json`, owned by the operator),
and it is not on an operability/freshness axis. Proposal 2 is addressed to the operator, not the lane.

## 4. Incidental observations (reported, not acted on)

1. **The r96 landing re-introduced an absolute host path into `tools/`.** `tools/mori-scorecard-calibration.py`
   (added at `9bde9322`, r96 landing) hardcodes `/home/vgpnk/...` in four lines (14, 15, 42, 43:
   `MANIFEST_DEFAULT`, `REPO_DEFAULT`). The lane's own frozen r93 C2 counter reads it as a regression:
   ```
   $ python3 -I .ufo/waves/round-93/count-c2.py <rev> --repo <lane>
   1fc921cf -> C2=met home_literals=0 vgpnk_refs=0 tools=3 selftests=3/3 census=ok rev=1fc921cf75af
   2dc476d7 -> C2=met home_literals=0 vgpnk_refs=0 tools=3 selftests=3/3 census=ok rev=2dc476d7fdb6
   9bde9322 -> C2=unmet home_literals=4 vgpnk_refs=4 tools=3 selftests=3/3 census=ok checks_failed=home_literals,vgpnk_refs
   973b2af1 -> C2=unmet home_literals=4 vgpnk_refs=4 tools=3 selftests=3/3 census=ok checks_failed=home_literals,vgpnk_refs
   e85ed912 -> C2=unmet home_literals=4 vgpnk_refs=4 tools=3 selftests=3/3 census=ok checks_failed=home_literals,vgpnk_refs
   ```
   QUALITY 127 (`corpus/QUALITY.md:1070`) requires that "the count of those that do is stated with its
   scope"; no r96 or r97 record states it (`git grep -rn -E "home_literals\|vgpnk_refs" -- corpus/lessons/round-96.md
   corpus/lessons/round-97.md LOG.md SCORECARD.md` → no r96/r97 hit). The r97 SKILL.md row for that tool
   (`SKILL.md:1447`) states its write scope as "stdout only; selftest fixtures in a TMPDIR temp dir, removed"
   and does not disclose the host-path defaults. Consequence for off-host replay: with default args the tool
   reads the *author's* live checkout, not the tree it is invoked from —
   `python3 tools/mori-scorecard-calibration.py HEAD` inside an archive of `9bde9322` printed
   `C1=met … rev=e85ed9124995` (the live repo's HEAD), and with `--repo <that archive>` it exits 2 with
   "not a git repository". This is a lane-owned instrument, so it is the lane's own call; reported only.
2. **The r97 counters have no mutant arms** (`grep -c -i "mutant\|survivor"` → 0, 0), so r97 supplies no
   survivor data point for proposal 5's trend. `corpus/lessons/round-97.md:56-57` carries the mutation
   sweep as debt to round 98.

## 5. Round-97 claim replay (measurement only, for the record)

Frozen counters, `git archive` into scratch, `--root DIR`:

```
$ python3 .ufo/waves/round-97/count-c1.py --root $S/enter        # rev 973b2af1
C1=unmet unregistered=4 registry=unmet targets_ok=0/4 checks_failed=registry,target_mori-cgroup-pressure.py,target_mori-drift-recheck.py,target_mori-scorecard-calibration.py,target_mori-source-digest.py   rc=1
$ python3 .ufo/waves/round-97/count-c1.py --root $S/land         # rev e85ed912
C1=met unregistered=0 registry=met targets_ok=4/4 checks_failed=-   rc=0
$ python3 .ufo/waves/round-97/count-c2.py --root $S/enter        # rev 973b2af1
C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy   rc=1
$ python3 .ufo/waves/round-97/count-c2.py --root $S/land         # rev e85ed912 (live leg run)
LIVE S615 time-churn as-of=2026-11-05T21:02:35Z / LIVE S616 time-churn / LIVE S623 time-churn
C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=-   rc=0
```

Both match the frozen receipts (`.ufo/waves/round-97/evidence/before-c1.txt`, `before-c2.txt`,
`landing-c1.txt`, `landing-c2.txt`) byte-for-byte on the verdict tokens and counts; counter digests match
the receipts' pins (`sha256sum` → `78a09016…d2a95`, `957a7be6…1491`). Reproduced independently of the
L1's scratch paths.

## 6. Unrun checks (named, not run)

- `mori-pin-check.py --rev HEAD` — **not run** (the operator recorded a >100 s timeout on 2026-11-05;
  I ran only `--selftest`, 14.10 s). A `--rev` run would need a ~330 MB clone.
- `tools/mori-census.sh --selftest` (134/134), `mori-pin-check.py --selftest` tally (125/125),
  `mori-source-digest.py --selftest` (11/11), `mori-record-sweep.py` / `mori-claim-sweep.py` /
  `mori-control-receipt.py` / `mori-counter-win.py` selftests — **not run** (out of this seat's scope;
  the operator's own 2026-11-05 file records them at `2dc476d7`).
- The round-93/94 counters' off-host replay against a *fleet snapshot* — **not run** (needs the operator's
  snapshot path; proposal 2).
- `tools/mori-gate-registry.py --audit-all` on the entering tree — not run separately; its result is
  consumed and printed by the frozen C1 counter (`registered=… unregistered=4`).
- Sibling-lane host-literal sweep for r97 — **not run** (proposal 4 is implemented as a connector seat;
  the r95 sweep is the last committed map, and r96's connector seat scoped itself to counter overlap).

VERDICT proposals holds: of the five proposals in `considerthese/2026-11-05.md`, three are still
unimplemented (1 admitted-share ledger, 2 fleet snapshot path, 3 gate runtimes), one is partly implemented
(4 sibling host-path sweep), and one has no per-round trend artifact (5 mutation-survivor trend);
the lane's own `considerthese/2026-10-26.md` file had, by its own status line, no proposal still
unimplemented — except that the adoption status line itself (its suggestion 4) lapsed after r95.

Report: .ufo/waves/round-97/w1/Mo97ScoutConsider.md
