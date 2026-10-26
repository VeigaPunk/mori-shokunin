# Mo50bExecAuthorDate — routed defect 1: the filed report's author date

Seat: executor, wave a2w1, lane mori-shokunin (round 50, attempt 2). Assignment: routed defect 1 of
`contract.md:146-148` — "the report must be filed with an author date at or after the lane tip it cites".
Read-only work: no lane or fleet byte was written except this report; no subagent; no install (nothing was
needed, so no tool/version/channel entry). Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bExecAuthorDate/` was created, `disk-guard.sh status` was checked
(`/fast/scratch/hyaku` 24 % used, 617.4 G free), and the directory was removed at end
(`rm -rf -- …` → rc 0, `ls` → "No such file or directory"). Every command below is `git`/`jj` read-only
(`jj` always with `--ignore-working-copy`); no mutating jj or git call was made.

## 1. What author date a fleet commit gets

Not the time of the commit run. The author date is the creation time of the shared fleet working-copy
change that the commit captures, and in the fleet's normal flow that is **exactly the committer date of the
preceding fleet commit — whichever lane made it**.

Mechanism, `/home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh`:

- lines 56-58: `jw()` passes `--config user.name=<lane>-shokunin --config user.email=<lane>@shokunin.local`;
- line 85: `jw metaedit --update-author` — jj 0.45.1 (the installed `jj --version` is
  `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`) documents this flag as: *"This updates the author
  name and email. The author timestamp is not modified – use `--update-author-timestamp` to update the
  author timestamp."*
- line 86: `jw commit -m "$msg" -- "${existing[@]}"` — the committer timestamp is set now.

`jj commit` then opens a fresh working-copy change whose author timestamp is the instant of creation, i.e.
the end of that commit. The next fleet commit therefore inherits it. The script's own comment at line 84
("`jj commit <paths>` keeps @'s author: stamp it first so author == committer") is **false under jj 0.45.1**:
name/email are stamped, the timestamp is not.

Evidence:

```
$ git log -40 --format='%H %aI %cI %P' ...  (window 375f9514 .. 28ff97e3)
checked=40 same=39 diff=0 root/no-parent=0      # 39/39 comparable commits: commit.ai == parent.ci exactly
$ git log -1 --format='%h ai=%aI ci=%cI' e60eb167 43997ee4
e60eb167 ai=2026-10-25T20:22:17-03:00 ci=2026-10-25T20:27:04-03:00
43997ee4 ai=2026-10-25T20:21:54-03:00 ci=2026-10-25T20:22:17-03:00
$ git log -1 --format='%h ai=%aI ci=%cI' 8af5b0b6 14910790 435d3c62
8af5b0b6 ai=2026-10-25T22:54:10-03:00 ci=2026-10-25T22:57:47-03:00
14910790 ai=2026-10-25T22:53:39-03:00 ci=2026-10-25T22:54:10-03:00
435d3c62 ai=2026-10-25T22:57:47-03:00 ci=2026-10-25T22:58:26-03:00
```

Live check of the same rule at the time of writing (read-only):

```
$ jj --ignore-working-copy log --no-graph -r @ -T 'author.timestamp() ++ "\n"'
2026-10-26 09:50:34.000 -03:00
$ git -C /home/vgpnk/Projects/shokunin log -1 --format='%h ci=%cI'
67fabbe4 ci=2026-10-26T09:50:34-03:00
```

So: author date = fleet working-copy open time = predecessor fleet commit's committer date; committer date =
the `fleet-commit.sh` run time. Report write time (the file mtime) enters neither field — round-49's report
file mtime is `2026-10-25 22:57:46.59 -0300` while its commit's author date is `22:54:10`.

## 2. Rounds 48 and 49, measured

Command (per round; rc 0 both):

```
FLEET=/home/vgpnk/Projects/shokunin; LANE=$FLEET/mori-shokunin
a=$(git -C "$FLEET" log -1 --format=%aI -- .ufo/reports/round-<N>/mori.md)
t=$(git -C "$LANE"  log -1 --format=%cI <cited tip>)
ta=$(git -C "$LANE" log -1 --format=%aI <cited tip>)
[ "$(date -d "$a" +%s)" -ge "$(date -d "$t" +%s)" ] && v=PASS || v=FAIL
```

Output:

```
round-48 report_author=2026-10-25T20:22:17-03:00 tip_ci=2026-10-25T20:26:18-03:00 tip_ai=2026-10-25T20:26:17-03:00 verdict=FAIL
round-49 report_author=2026-10-25T22:54:10-03:00 tip_ci=2026-10-25T22:56:42-03:00 tip_ai=2026-10-25T22:56:42-03:00 verdict=FAIL
rc=0
```

| round | report (fleet path) | report commit ai / ci | cited lane tip | tip ai / ci | author vs tip |
|---|---|---|---|---|---|
| 48 | `.ufo/reports/round-48/mori.md` (line 3 cites `14c5110d…` as "Lane HEAD (pushed)") | `e60eb167` 20:22:17 / 20:27:04 | `14c5110d65a2f225e7316e1996e92090b9b8e7cb` | 20:26:17 / 20:26:18 | **FAIL**, author 4 m 01 s *before* the tip |
| 49 | `.ufo/reports/round-49/mori.md` (line 3 cites `43d84666…` and prints the tip's committer date) | `8af5b0b6` 22:54:10 / 22:57:47 | `43d846669efe5a2fcc2325006f165af4e7e7fda4` | 22:56:42 / 22:56:42 | **FAIL**, author 2 m 32 s *before* the tip |

Both reports were written and committed *after* their lane tip — their **committer** dates are 46 s and
65 s after it — and both still fail the routed criterion, because the author field is inherited from the
fleet's preceding commit (`43997ee4` at 20:22:17 for round 48; `14910790` at 22:54:10 for round 49), both
of which predate the lane tips. The routed defect is present in both rounds, not only round 49.

Note on the comparison field: the round-49 disposition measured against the tip's **author** date
(`%aI`, 20:26:17); the assignment's check uses the tip's **committer** date (`%cI`, 20:26:18). The two
differ by 1 s on round 48's tip and are equal on round 49's; the verdict is FAIL under either, but `%cI` is
the right instant — it is when the lane tip became a commit.

## 3. The exact check command

### 3a. After filing (authoritative)

```sh
FLEET=/home/vgpnk/Projects/shokunin
LANE=$FLEET/mori-shokunin
REPORT=.ufo/reports/round-50/mori.md
TIP=<the hash printed in the report's "Lane tip at filing" line>

a=$(git -C "$FLEET" log -1 --format=%aI -- "$REPORT")
t=$(git -C "$LANE"  log -1 --format=%cI "$TIP")
[ -n "$a" ] || { echo "FAIL: $REPORT has no commit in the fleet repo"; exit 1; }
printf 'report_author=%s\nlane_tip_ci=%s\n' "$a" "$t"
[ "$(date -d "$a" +%s)" -ge "$(date -d "$t" +%s)" ] \
  && echo PASS || echo "FAIL: report author date precedes the lane tip it cites"
```

The `[ -n "$a" ]` guard is required: the path currently prints empty with rc 0 (not yet filed) —
`git -C /home/vgpnk/Projects/shokunin log -1 --format=%aI -- .ufo/reports/round-50/mori.md` → `out=[] len=0
rc=0`.

Epoch-only variant (no `date` parsing, offset-independent):

```sh
[ "$(git -C "$FLEET" log -1 --format=%at -- "$REPORT")" \
  -ge "$(git -C "$LANE" log -1 --format=%ct "$TIP")" ]
```

### 3b. Before filing (predicts the author date a single commit will get)

The next fleet commit's author date is the current working-copy change's author timestamp; in the normal
flow that equals the fleet HEAD's committer date:

```sh
h=$(git -C "$FLEET" log -1 --format=%cI)          # == the next fleet commit's author date
t=$(git -C "$LANE"  log -1 --format=%cI "$TIP")
[ "$(date -d "$h" +%s)" -ge "$(date -d "$t" +%s)" ] \
  && echo "single commit OK" || echo "STALE: file the report in two fleet commits"
```

Exact (no inheritance assumption), read-only:

```sh
jj -R /home/vgpnk/Projects/shokunin --ignore-working-copy log --no-graph -r @ \
   -T 'author.timestamp() ++ "\n"'
```

Measured at the time of writing, against the current mori data tip
`487941b9395e89678af0053cc443cdb49cdee6e3` (ai 09:05:32, ci 09:27:40):

```
single-commit OK head_ci=2026-10-26T09:50:34-03:00 tip_ci=2026-10-26T09:27:40
jj @ author.timestamp() = 2026-10-26 09:50:34.000 -03:00        # == HEAD 67fabbe4.ci
rc=0
```

## 4. Does one fleet-commit satisfy it when the report is written after the last lane commit?

**No as a rule — only conditionally, and the condition is about the fleet repo, not about the report.**

- A single fleet-commit passes **iff** the fleet working-copy change it commits was opened at or after the
  lane tip's committer instant — in the normal flow, iff some fleet commit (any lane's) has landed at or
  after the cited lane tip. The report being written after the last lane commit does not enter the
  computation: the author timestamp belongs to the shared working-copy change, not to the file write or the
  commit run.
- Rounds 48 and 49 are exactly the failing case: report written and committed after the tip
  (ci 20:27:04 / 22:57:47) while no fleet commit had landed since the tip, so the single commit inherited a
  pre-tip author date (20:22:17 / 22:54:10).
- Today it happens to pass for round 50 (tabi's `67fabbe4` landed 09:50:34, after mori's `487941b9` at
  09:27:40), but the report will cite the **final** lane tip, which is at or after the data tip; one more
  mori commit after 09:50:34 flips a single-commit filing back to FAIL. The check must be run against the
  tip actually cited, after that tip exists.
- The two-commit filing in `contract.md:147` makes it deterministic: commit C1 (any lane path after the
  lane tip — wave-2 reports, or a preliminary report body) has committer date t1 > tip; jj opens the next
  working-copy change with author timestamp t1; commit C2 on `.ufo/reports/round-50/mori.md` then has
  author = t1 >= tip. If another lane's commit lands between C1 and C2, C2's author is that later commit's
  time — still >= tip. This is the contract's "(= the first one's commit time)" and it is fully inside the
  lane's control; no mutating jj and no fleet-helper change is needed.
- Caveat the check itself catches: C2 **must touch the report**. If the final commit does not modify the
  report path, `git log -1 -- <report>` returns C1's author (which is inherited from before the tip) and the
  check fails.
- One-line alternative at the helper level (reported, not landed — outside this seat's write scope and
  outside round-50's frozen set): adding `--update-author-timestamp` to the `metaedit` call at
  `fleet-commit.sh:85` would stamp author = committer for every lane commit and remove the class fleet-wide.
  The round-50 route (two commits) is the in-lane fix; the helper change is the fleet-owner's call.

## 5. Named limits

- The lane tip's `%cI` is the lane-side clock when the commit was created; it is not the push time and not
  the fleet's observation time. A report can pass this check while the tip was not yet pushed.
- The author date carries no information about when the report bytes were written; a PASS only proves a
  fleet commit landed at/after the lane tip.
- `git log -1 -- <report>` is path-based: a later commit that does not touch the report is invisible
  (caveat in §4).
- The identity "author = predecessor's committer date" was verified on 39 consecutive commits and the live
  working copy; a working copy opened by something other than a fleet commit (e.g. an orchestrator salvage)
  would break the `HEAD.cI` predictor — the `jj -r @` form in §3b has no such assumption and was used live.
- All observed timestamps are `-03:00`; the `date -d` form was used, and the `%at`/`%ct` variant removes the
  offset dependence, but host clock steps were not measured.
- This check lives in the fleet repo, which the lane does not write, so the lane cannot commit a receipt of
  it; the report's "Lane tip at filing" line is the lane-side record.

## Findings

- **HIGH — the routed defect is present in both prior rounds, structurally.** `.ufo/reports/round-48/mori.md`
  commit `e60eb167` author 2026-10-25T20:22:17-03:00 vs cited tip `14c5110d` committer 20:26:18 (4 m 01 s
  before); `.ufo/reports/round-49/mori.md` commit `8af5b0b6` author 22:54:10 vs cited tip `43d84666`
  committer 22:56:42 (2 m 32 s before). Committer dates are after both tips; only the author field fails.
- **MED — `scripts/hyaku/fleet-commit.sh:84` states an invariant the code does not produce.** The comment
  says "stamp it first so author == committer"; `--update-author` at line 85 does not touch the author
  timestamp under jj 0.45.1. Either the comment is wrong or the call should gain
  `--update-author-timestamp` (helper is fleet-owned; not changed here).
- **MED — a single fleet-commit is not sufficient; the L1's filing step needs the §3b pre-file gate.** The
  contract's two-commit route (`contract.md:147`) is correct and deterministic, but nothing in the round
  checks the author date after filing; without §3a the same stale filing is invisible again.
- **MED — `mori-shokunin/.ufo/waves/round-49/disposition.md:73-82` proposes a check that would have passed
  the failing report.** Its green criterion is the report file's mtime ≥ the cited tip's committer date;
  round-49's report mtime is 22:57:46 ≥ 22:56:42, yet its commit author date 22:54:10 < 22:56:42. mtime is
  not the git author date.
- **LOW — `mori-shokunin/.ufo/waves/round-49/disposition.md:84-86` overstates the gap.** It says the
  criterion is unsatisfiable from inside a lane and that "a concurrent fleet commit between the lane tip
  and the report will re-create the round-48 shape"; both are contradicted by the mechanism: the two-commit
  filing needs no fleet-helper change, and a concurrent post-tip fleet commit *guarantees* a pass (it opens
  the working copy after the tip). The round-50 contract already supersedes this with carrier 1.
- **LOW — comparison-field drift.** The round-49 disposition compared against the lane tip's author date
  (`%aI`, 20:26:17) rather than its committer date (`%cI`, 20:26:18). Verdicts are unchanged, but the
  prescribed check (`%cI`) should be the recorded one.
