# CriticC2 — attack on C2 (jj branch-anchored census probes)

Seat: MoriR17.CriticC2-5 (critic; advises, does not judge). Date 2026-10-20.
Inputs: `.ufo/waves/round-17/contract.md:16-20,80-94`; `tools/mori-census.sh` at 24526ea
(lines 1967-1974, 2092-2110, 2176-2273, 2275-2294); `scripts/hyaku/jj-lane.sh` (99-126, 155-165,
580-670); routed evidence `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md`
(F3, F4, F5, F7, rows 1/2/5/6) and `JjTrialMori.md` (H1, H4).
Executor clone `.ufo/worktrees/round-17/CensusJj` still sits at 24526ea with no census diff
(`git log --oneline -3` / `git diff --stat 24526ea`, rc 0, empty diff), so this attacks the
**contract**, not an implementation.

All live measurements were read-only git (`GIT_OPTIONAL_LOCKS=0`, `-c core.fsmonitor=false`,
`GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` unset) over the fleet root plus 21 `*-shokunin` repos; no jj
command, no sandbox, no census run, nothing written outside this file. No tools installed.

## Axes

- **operability (C2's owned axis 7):** census verdict correctness on a jj-colocated fleet, false
  findings, runtime.
- Regression guards: grade identity in steady state; no new false `LANE_SILENT`/drift; one branch
  authority (no duplicate resolver); no "landed" claim the probe cannot support.

## Q1 — Is HEAD≠branch real or synthetic only?

**Both, but the observed real case is not the one the contract motivates.**

1. *Now:* 22/22 repos have `merge-base --is-ancestor HEAD refs/heads/<b>` rc 0 and HEAD == branch tip
   (8 colocated: kaidoku kama mado mori souji tabi tameshi tsukuroi; 6 of them detached and resolving
   via `origin/HEAD`). Zero live mismatches.
2. *Helper failure window (jj-lane.sh:604 `jj commit` → :658 `bookmark set`):* **synthetic only.**
   Only evidence is the sandbox F3 measurement (JjAuditMori.md:62-77). HEAD-reflog scan (≤400
   entries) of the 8 colocated lanes: every HEAD commit that is not an ancestor of the current branch
   was **also** in the branch reflog (kaidoku 4, kama 1, tameshi 1, tsukuroi 1) — i.e. HEAD and the
   branch moved together (rebase drafts), never HEAD alone.
3. *Real, live, today — non-helper cause:* `tameshi-shokunin` HEAD reflog:
   `f8832ef/0559c60/e16adb7 HEAD@{2026-10-20 12:29:33 -0300} commit: selftest-fixture*` authored and
   committed by `tameshi <tameshi@selftest>`, absent from the `refs/heads/master` reflog, repaired at
   `HEAD@{2026-10-20 12:36:43 -0300} round-17 L1 repair: restore HEAD after R04 seat fixture commits
   (GIT_DIR leak)`. HEAD sat off-branch for **7 m 10 s**, inside tameshi's open round-17 window
   (ledger: `2026-10-20T12:07:33-03:00 launch tameshi round=17`). The fixture tree had 3 files;
   `f8832ef` is `1 A / 1296 D` against the lane tree (`git show --name-status`, rc 0).
   - Entering census in that window: `log` on HEAD sees 3 in-window commits by a non-lane author →
     **row C `progressing-weak` credited from selftest junk** (or row B first, see H3).
   - C2 census: branch has no in-window commits (98bea7d is pre-launch) and `HEAD_BRANCH_MISMATCH`
     fires on a real incident. **This is a genuine improvement and the strongest pro-C2 evidence;
     the contract should cite it instead of resting on the synthetic F3 window.**

Verdict: the defect is real (one observed incident, 7 min), but its live trigger was a GIT_DIR leak,
not the jj commit→bookmark gap. Detection is point-in-time: a census run must land inside the window
[INFERENCE: census cadence not measured].

## Q2 — Can branch anchoring hide work the old HEAD read showed?

Yes, in one shape, and the contract's "grading semantics otherwise unchanged" hides a mixed basis.

**H1 — mixed revision basis (fixable defect).** Rows A/C and row 6 move to `refs/heads/<b>`, but row
B (`ls-files -mo`, mori-census.sh:2180) still reads the git index, which under jj is HEAD-based
(JjAuditMori F7, :145-146; F5). When HEAD is ahead of the branch:
- Counterexample (helper guard exit): `metaedit` (jj-lane.sh:600) stamps the lane author, `jj commit`
  (:604) moves HEAD, then a sweep guard exits 1 (:614 parent, :628 out-of-scope path, :652 phantom
  deletion, :659 bookmark set) — "the bookmark stays put on any violation" (:609). Same shape: a seat's
  raw `jj commit` (the repo config already carries the lane identity, JjTrialMori.md:52-56).
  Old census: row A `progressing` (lane-authored commit at HEAD). C2 census: commit not on branch →
  not in log; committed paths are no longer dirty against the HEAD index → row B misses them →
  **row D `silent` + `LANE_SILENT`**. The lane is stuck, not silent; the verdict misnames it.
- Reverse (tameshi shape): index follows a foreign HEAD tree; with 1296 lane paths absent from it,
  `ls-files -mo` can list live files as untracked and row B can grade `progressing` from a
  contaminated index [INFERENCE: whether the leaked index file was the lane's was not observed].
- Consequence: under mismatch, A/C read the branch, B reads HEAD. The entering census was at least
  consistent.

**H2 — branch ≠ landed (claim boundary).** `bookmark set` precedes push (jj-lane.sh:658 then :669);
a rejected push leaves an unpushed commit on `refs/heads/<b>` with HEAD == branch → no mismatch,
same credit as before. Live: `kama` `master@{2026-10-20 10:50:42}` = `c0556c7`, rewritten 7 s later
(`rebase (finish)`), `merge-base --is-ancestor c0556c7 refs/remotes/origin/master` rc 1 — the branch
ref itself credited a never-pushed commit. C2 must not be described as "landed" anchoring
(JjAuditMori.md:257 motivates it with the "landed = committed AND pushed" spirit).

**H3 — steady state is unaffected.** Six detached colocated lanes have HEAD == branch; old and new
reads are identical there. No live lane today would change grade from the A/C/6 switch alone.

## Q3 — Harms to operability

**O1 — `LANE_AUTHOR_MISMATCH` false finding on today's fleet (real, measured).** Simulated row-9 scan
(branch log, `--since=@launch`, strict `ct > launch`, root-lane pathspec as mori-census.sh:2205) over
each lane's last ledger launch:
- `kengaku` (git-mode, no `.jj`; open round 13 since 2026-10-15T01:50:57-03:00, row 6 not closed:
  report last committed 2026-09-29): commit `6180e4f` — author `protocol-shokunin
  <protocol@shokunin.local>`, committer `kengaku-shokunin <kengaku@shokunin.local>`,
  "Integrate remote documentation; preserve local round log", ct 1792458318 in window. Matches the
  contract rule literally (contract.md:88-89) → **1 drift finding, flips census to exit 1**, for a lane
  integrating an operator/protocol commit — not the F4 mechanism (jj keeping an *ambient* author).
- True positives on live history: **0**. All 8 colocated lanes have 0 commits with lane committer and
  different author (helper metaedit works). Live precision of the rule as written: 0/1.
- If the implementation runs a separate unfiltered log instead of reusing `lg_args`, the root lane
  `protocol` adds **22 more** false hits: relay commits `"round-N report (<lane>) — lane-authored,
  committed by integrator"` (e.g. 930677e, 46e4403), each touching only `.ufo/reports/...`, which the
  row-9 pathspec excludes. Author = lane, committer = `protocol-shokunin`, so each matches the rule for
  root lane `protocol`. Measured: shared pathspec → 0 hits, unfiltered → 22.
- [INFERENCE] Approximate anchors: my ledger parse (last `launch`, closed by a later `complete` of the
  same round) is simpler than `ledger_anchor` (mori-census.sh:2009) and ignores `.round` state.

**O2 — row 6 must resolve the fleet root's branch, not the lane's.** Row 6 queries `$ROOT`
(mori-census.sh:2100-2102), not the lane repo. Seven lanes are on `main` (audio, game-dev-2d,
game-dev-3d, kaidoku, kotodama, lore, revenger); the fleet root has no `refs/heads/main`
(rev-parse rc≠0). Reusing the lane branch for `$ROOT` makes `cat-file -e refs/heads/main:...` fail →
row 6 never closes for those lanes → their closed rounds fall to row 9 (false `LANE_SILENT` once the
lane stops committing). The fleet root is not colocated (`.jj` absent; HEAD attached = master), so the
row-6 switch changes nothing live and only adds this risk.

**O3 — duplicate branch authority.** Contract resolver = symbolic-ref → `origin/HEAD` → unique
master/main (contract.md:82-83). The helper's own read path is `lane_branch_git` (`git config
lane.branch`, jj-lane.sh:99-102) **first**, then `detect_branch` (:162, :387); `detect_branch` is
documented "used ONLY by init for a first recording" (:113). Live: 4 colocated lanes record
`lane.branch` (kaidoku main, mado/mori/tabi/tsukuroi master), 3 do not (kama souji tameshi); today all
agree with `origin/HEAD`. A lane whose recorded branch differs from origin's default would be graded
against the wrong branch and raise a false `HEAD_BRANCH_MISMATCH` on every run.

**O4 — unresolved branch / missing ref degrades to `silent`.** The contract does not say what happens
when the resolver fails (detached, no `origin/HEAD`, both or neither master/main) or `refs/heads/<b>`
is absent. Swapping `rev-parse --verify -q HEAD` (mori-census.sh:2197) for the branch ref sets
`has_head=0`, skips the log, and falls to row B/D → **`silent`**. In the entering census `has_head=0`
meant "no history"; now it can mean "resolver mismatch" — a new false `LANE_SILENT`.

**O5 — `merge-base` rc conflation.** `--is-ancestor` returns 1 for "not ancestor" and ≥128 for errors.
"fails" (contract.md:86) implemented as `!= 0` turns a git error into a drift finding.

**O6 — transient in-flight positives (tradeoff, low).** A census sample inside the helper's
:604→:658 span (snapshot, guard loop over `jj diff --summary`) reports `HEAD_BRANCH_MISMATCH` on a
healthy lane. The census does not take the helper lock. No fleet consumer acts on census findings
(`grep LANE_SILENT|mori-census` over `/home/vgpnk/Projects/shokunin/scripts`: no matches; only
`emit_finding ... warn`, mori-census.sh:2291), so this is report noise, not automation harm.
Acceptable if the detail carries both short hashes (contract already requires it) so a rerun
disambiguates.

**O7 — runtime: negligible.** 5 extra git calls (symbolic-ref HEAD, config lane.branch, symbolic-ref
origin/HEAD, rev-parse branch, merge-base) × 22 repos × 3 reps: mean 0.51 ms, max 0.95 ms, ≈56 ms per
full fleet pass (python subprocess timing incl. spawn). Row-9 log on the branch: 0.6–5.7 ms per repo.
Reusing the row-9 log with `%cn <%ce>` appended makes `LANE_AUTHOR_MISMATCH` cost zero extra calls.

## Impacted axes

operability (O1 false drift today, O2/O4 false `LANE_SILENT` risk, H1 misnamed verdict), identity
(O3 duplicate branch authority), provenance (H2 "landed" overclaim). Coverage (C1) untouched — C2
edits only the census, separability holds.

## Smallest safe corrections (all fixable; none forces rejection)

1. **Author rule (O1):** fire `LANE_AUTHOR_MISMATCH` only when committer is the lane identity AND the
   author is **not** a fleet identity (`^[a-z0-9-]+-shokunin <[a-z0-9-]+@shokunin\.local>$`) — that is
   the F4 shape (ambient author). Compute it from the **same** row-9 log call (`lg_args` pathspec,
   strict awk window), adding `%cn <%ce>` to the format. Kills the kengaku hit and the 22 relay hits.
2. **Resolver (O3):** `git config --get lane.branch` → symbolic-ref → `origin/HEAD` → unique
   master/main, mirroring `cmd_state` (jj-lane.sh:162), not `detect_branch` alone.
3. **Row 6 (O2):** resolve `$ROOT`'s branch once per run, separately from lane branches.
4. **Failure paths (O4/O5):** resolver failure or missing `refs/heads/<b>` while HEAD resolves →
   `unavailable` row-1 (`reason=branch-unresolved` / `branch-ref-missing`), never `silent`; treat
   `merge-base` rc 1 as mismatch, rc ≥128 as unavailable/error.
5. **Mixed basis (H1):** compute `HEAD_BRANCH_MISMATCH` before row 6 so early returns (rows 6/7/8)
   still report it, and append `head_branch_mismatch=1` (plus count of in-window `refs/heads/<b>..HEAD`
   commits) to `GL_EXTRA` so a row-B or row-D verdict under mismatch is visibly HEAD-index-based.
6. **Claim wording (H2):** describe C2 as "graded on the local branch ref", not "landed"; cite the
   tameshi 2026-10-20 12:29–12:36 leak as the observed motivating incident.

## Falsifier cases the JjGate should carry (each from evidence above)

| case | setup | entering census | required C2 outcome |
|---|---|---|---|
| fixture-leak | 3 foreign-author commits on detached HEAD above branch, in window | row C/B credit | no A/C credit; `HEAD_BRANCH_MISMATCH` |
| guard-exit | lane-authored commit at HEAD, bookmark unmoved | row A | `HEAD_BRANCH_MISMATCH`; verdict annotated, not bare `silent` |
| integrate | git-mode lane, committer lane, author `protocol-shokunin` | — | **no** `LANE_AUTHOR_MISMATCH` |
| ambient | colocated lane, committer lane, author non-fleet | — | `LANE_AUTHOR_MISMATCH` |
| relay | root lane, committer protocol, author lane, `.ufo/reports` only | — | no finding |
| main-lane-row6 | lane on `main`, report committed on root `master` | row 6 closes | row 6 still closes |
| bad-origin-head | detached, `origin/HEAD` → absent local branch | log on HEAD | `unavailable`, never `silent` |
| steady | detached HEAD == branch tip | grade G | byte-identical grade G, no finding |

## Commands run (all read-only, rc 0 unless noted)

- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/.jj /home/vgpnk/Projects/shokunin/.jj` — rc 2
  (expected misses; 8 lanes colocated, fleet root not).
- Python `subprocess` over 22 repos: `symbolic-ref -q HEAD`, `config --get lane.branch`,
  `symbolic-ref -q refs/remotes/origin/HEAD`, `rev-parse -q --verify refs/heads/{master,main,<b>}`,
  `merge-base --is-ancestor HEAD refs/heads/<b>`, `reflog show -n 400 HEAD`, `reflog show refs/heads/<b>`,
  `log --format=%H|%ct|%an <%ae>|%cn <%ce>` (full branch and per-lane windows), `show --name-only`.
- `git -C CensusJj log --oneline -3 && git diff --stat 24526ea` — no diff.
- `grep` of `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` for launch/complete lines; `cat
  .ufo/state/<lane>.round` (souji absent, rc 1 on that cat).
- `git -C fleet cat-file -e HEAD:.ufo/reports/round-13/kengaku.md` rc 0; `log -1 --format='%ct %ci'`
  → 2026-09-29 (pre-launch).
- tameshi: `reflog show --date=iso -n 9 HEAD`; `show --name-status f8832ef` (1 A / 1296 D);
  `ls-tree -r --name-only` e16adb7 = 3, 98bea7d = 1296.
- kama: `reflog show refs/heads/master`; `merge-base --is-ancestor c0556c7 refs/remotes/origin/master`
  rc 1.
