# RevIndexClean — QUALITY 103 second-clause audit of round-38 dispatch log

**Result: FAIL (record coverage).** Of the five commits in
`e33bb561712b32f46861362a3fa43762fa70ae4f..f725f3076972e6e70595b5ac8279be524a111ff8`,
only the first has a `landed` line and an index-clean record. The other four commits have
no `landed` line, no index-clean record, and no disclosure of either omission anywhere in
`.ufo/waves/round-38/dispatch-log.txt`.

## Criterion text (read at the scored tip)

`corpus/QUALITY.md:822-828`, criterion 103: "After every lane helper commit, the lane git
index holds no staged path and no intent-to-add entry, and the round's dispatch log records
the check after each `landed` line." Debt-disposition row 9 of the frozen contract
(`contract.md:134`) disposes it as: "`dispatch-log.txt` records the index-clean check after
each `landed` line; the criterion's check is re-read against this round's log."

## Commit → record table

Commits from `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%H %ci %s' --reverse e33bb56..f725f30`:

| # | Commit | Landed | Subject | `landed` line | Index-clean record | Disclosed? |
|---|--------|--------|---------|---------------|--------------------|------------|
| 1 | `3501d4c21f70e2ec2659c37c3f960b55f60cfea6` | 17:49:42 | round-37 erratum + LOG amendment + inherited reports | `dispatch-log.txt:3` | `dispatch-log.txt:4` — `staged=0 intent_to_add=0 (exit 0)` | recorded |
| 2 | `1f1e9968f4746dc7ed46804d4e7d02693dfd1497` | 17:51:15 | freeze — contract, counters, fixtures, pins | none | none | no |
| 3 | `8d261508229901d69587b7b6c2726b1db0563617` | 17:55:19 | before receipts + witness-sandbox builder | none | none | no |
| 4 | `daa1d4d2501e1671e7b7ff1fd60a069564f178b0` | 17:55:25 | data: S226, timed supersede, scorecard rows | none | none | no |
| 5 | `f725f3076972e6e70595b5ac8279be524a111ff8` | 19:36:47 | counter v4.1, freeze v2, w1 spec/dispatch | none | none | no |

## Live index-clean output (run this wave)

```
$ bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin
MORI_INDEX_CLEAN staged=0 intent_to_add=0
EXIT=0
```

The first clause holds at measurement time: zero staged paths, zero intent-to-add entries.
(`git status --porcelain` shows only ` M`/untracked entries — unstaged worktree state,
which `tools/mori-index-clean.sh:5-6` explicitly excludes from index state.) The defect is
in the *record*, not the index.

## Missing records — all undisclosed

- **Commits 2–4 (`1f1e996`, `8d26150`, `daa1d4d`)**: no `landed` line, no clean-index
  record. Each had a successor commit in the range that could have committed the record —
  none did. `git show <commit>:.ufo/waves/round-38/dispatch-log.txt` at `1f1e996`,
  `8d26150`, and `daa1d4d` prints byte-identical content: the same 4 lines covering only
  `3501d4c`. The log file was created at `1f1e996` (per
  `git log -- .ufo/waves/round-38/dispatch-log.txt`) and never touched again.
- **Commit 5 (`f725f30`, the scored tip)**: no `landed` line, no record. A record for the
  tip is structurally deferred to a later commit, but the log also does not disclose that
  the three preceding commits went unrecorded — so even under the most charitable reading
  (record lands in the next commit), the log is already behind by three commits with no
  disclosure of the lag.
- No other file under `.ufo/waves/round-38/` (excluding seat scratch) records a
  `mori-index-clean` run for commits 2–5: `grep -rln 'mori-index-clean\|landed'
  .ufo/waves/round-38/` outside `scratch/` returns only `contract.md`, `dispatch-log.txt`,
  the w1 spec/dispatch/plan JSONs, and `w1/ExecIndexCleanLog.md` — the last being a
  wave-1 report (uncommitted at `f725f30`), not the dispatch log and not a clean-index
  receipt.

## Wave-1 corroboration

`w1/ExecIndexCleanLog.md` (present in the working tree, untracked) reports the identical
finding: "FAIL (commit coverage) … five commits, but dispatch-log.txt contains only one
`landed` entry … the other four commits in the scored-tip history have no corresponding
entry or recorded index state" (`ExecIndexCleanLog.md:3-13`). Wave 2 re-derived this
independently: the committed log at `f725f30` is byte-identical to the working-tree copy
(`git diff f725f30 -- dispatch-log.txt` → empty).

## Prior-round contrast

Round-37's log (`.ufo/waves/round-37/dispatch-log.txt:17-19`) records the index-clean
check after each landed commit and, for the late commits where in-order logging lapsed,
discloses them explicitly: "index clean after 5dff52a1 and after
0a05f7e6/52d636d5/5631efa9/1ae1d6d6/30dfe70f … re-run at 30dfe70f". Round-38's log does
neither — it records one pair and silently stops.

## Verdict

**FAIL.** Every commit after `3501d4c` lacks its QUALITY 103 record and the log does not
disclose the gaps. Because a `landed`-line-only reading makes the clause trivially
satisfiable by logging one commit and forgetting the rest — while commits 2–4 each had
committed successors that should have carried their `landed` + check pair — the honest
reading (round-37's own convention) is per-commit coverage, which fails 4-of-5.

## Tooling

No installs performed; `bash`, `git`, `grep` already present.

Report: .ufo/waves/round-38/w2/RevIndexClean.md
