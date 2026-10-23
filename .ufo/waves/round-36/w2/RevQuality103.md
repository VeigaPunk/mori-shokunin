# RevQuality103 — QUALITY 103 shown-able-to-fail audit (round 36, wave 2, attempt 2)

Seat: mori-r36-w2 / RevQuality103. Lane tip audited: `bf0df77fee4b6ef54a90aea09335c7617f125151`
(`git rev-parse HEAD` → `bf0df77fee4b6ef54a90aea09335c7617f125151`). Round base: `6bd57097`.
Attacks: criterion 103 (`corpus/QUALITY.md:822-828`) — its red arm (selftest `add -N` case), the
round-35 M4 blind spot (`git diff --cached --name-only` silent on intent-to-add), and the live
check command at the landed tip.

## What item 103 claims

`corpus/QUALITY.md:822-828`: after every lane helper commit the lane git index holds no staged
path and no intent-to-add entry; the round's dispatch log records the check after each `landed`
line. Check: `bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin` prints
`staged=0 intent_to_add=0`, exit 0. Lesson: `corpus/lessons/round-35.md` M4;
`corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4. Shown able to fail: the tool's selftest
runs `git add -N newfile` in a sandbox and gets exit 1 (`intent_to_add=1`); `git diff --cached
--name-only` alone prints nothing there, so a check built on it passes the round-35 mistake.

## 1. Red arm present — selftest re-run

Command (lane root):

```
$ bash tools/mori-index-clean.sh --selftest; echo "SELFTEST_RC=$?"
MORI_INDEX_CLEAN_SELFTEST pass=4 fail=0
SELFTEST_RC=0
```

The red arm exists: selftest case 2, `tools/mori-index-clean.sh:171-180` — creates `newfile`,
runs `g -C "$repo" add -N newfile` (line 173), and asserts `rc == 1` **and** output matching
`MORI_INDEX_CLEAN staged=0 intent_to_add=1` (line 175). It passed (fail=0), so the assertion held
on this run. The gate's `intent_to_add` count is cross-checked between porcelain v1 (`XY == " A"`,
`collect_status`, :56-72) and porcelain v2 (`^1 \.A ` records, `count_ita_v2`, :73-77); a
disagreement returns 2/refuses a verdict (:120-124). No defect.

## 2. M4 blind spot reproduced in an independent sandbox (git 2.56.0)

Sandbox `/fast/scratch/hyaku/mori-r36/RevQuality103/sandbox` (driver
`/fast/scratch/hyaku/mori-r36/RevQuality103/m4-demo.sh`; lane untouched, gate run read-only against
the sandbox). After `git add -N newfile` on a repo with one commit:

```
=== A: git diff --cached --name-only (expect empty)
(empty output)
byte_count=0
=== B: lane gate on sandbox
MORI_INDEX_CLEAN staged=0 intent_to_add=1
MORI_INDEX_CLEAN_PATH newfile
LANE_TOOL_RC=1
=== C: cross-signals
-- porcelain v1:  A newfile
-- porcelain v2 '.A' count: 1
-- ls-files -v: H newfile
=== D: control — after real `git add newfile`
diff --cached --name-only now: [newfile]
MORI_INDEX_CLEAN staged=1 intent_to_add=0
LANE_TOOL_RC=1
```

Confirmed: `git diff --cached --name-only` prints **0 bytes** on the same sandbox where the lane
gate exits 1 with `intent_to_add=1` — exactly the round-35 M4 blind spot (M4: L1 ran
`git add -N .` in the lane, `corpus/lessons/round-35.md:68`). `git ls-files -v` shows plain
`H newfile`, i.e. indistinguishable from a genuinely staged empty file, matching the script header
claim (:14-23); the porcelain v1/v2 records are the only discriminating signals. Arm D shows the
gate still fails (as `staged=1`) once a real `git add` lands.

Precision note (not a defect): the selftest's case-2 assertion keys on `staged=0
intent_to_add=1`, not on asserting emptiness of `diff --cached` output. The criterion's sentence
"`git diff --cached --name-only` alone prints nothing there" is a git-behavior claim; I verified it
directly above (byte_count=0) rather than through the selftest, so the criterion text is accurate
as written.

## 3. Live check at the landed tip — green

Command, verbatim from 103's Check (lane root):

```
$ bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin; echo "LIVE_RC=$?"
MORI_INDEX_CLEAN staged=0 intent_to_add=0
LIVE_RC=0
```

Matches 103's expected output substring `staged=0 intent_to_add=0` with exit 0.

Why this is a green **at bf0df77** and not just of the dirty worktree:
- HEAD is `bf0df77fee4b6ef54a90aea09335c7617f125151`.
- `git status --porcelain tools/mori-index-clean.sh corpus/QUALITY.md` → empty output, rc=0: the
  audited gate script and criterion text are byte-identical to the tip.
- Repo-wide dirty state is one unstaged worktree edit (`.ufo/waves/round-36/dispatch-log.txt`)
  plus untracked wave artifacts (`git status --porcelain`, 10 entries, no staged first-column
  entries). The gate's contract (:4-6) excludes unstaged worktree edits from index state, and
  staged=0 ∧ intent_to_add=0 means the index equals the HEAD (bf0df77) tree for tracked paths.
  Therefore the live green is the index state of bf0df77.

## 4. Second conjunct: dispatch log records the check after each `landed` line

`.ufo/waves/round-36/dispatch-log.txt` has exactly one `landed` line (line 27, 15:4xZ):
`data commit landed bf0df77fee4b6ef54a90aea09335c7617f125151 (helper push verified)`. The next
entry (15:5xZ, lines 28-30) records: `round append-only gate: round_changed=[] exit 0; index clean
staged=0 intent_to_add=0` — the check's result, recorded after the landed line. Meets "records the
check after each `landed` line" at the current tip; no later landed line exists this round. The
dispatch-log edit itself is unstaged worktree state, which the gate deliberately ignores — not a
103 violation.

## 5. Citation soundness of the row

- `corpus/lessons/round-35.md:68` — M4 row exists: `git add -N .` in the lane at 09:06Z put
  intent-to-add entries for every untracked file into the lane index; rule stated, nothing
  enforced it. Matches what 103 attributes to it.
- `corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4 exists: "M4 enforcement. Nothing shown
  able to fail prevents `git add` in the lane. A check that `git status --porcelain
  --untracked-files=no` is empty after each helper commit, recorded in the round mechanics, would
  make it detectable." 103 implements exactly this (with the stronger index-clean gate) plus the
  recording obligation.
- 103's declared "Not covered" (detection after the fact; no prevention of forbidden git commands)
  is consistent with the artifact: the gate is read-only (`--no-optional-locks`, `g()` wrapper
  :43-44; selftest writes only inside its mktemp sandbox).

## Verdict

VERDICT: PASS — no defect found in scope. The red arm is present and passing (selftest case 2,
pass=4 fail=0, rc=0); the M4 blind spot is real in git 2.56.0 and demonstrable (`diff --cached
--name-only` prints 0 bytes while the gate exits 1 with intent_to_add=1 in the same sandbox); the
live check runs green at bf0df77 (`staged=0 intent_to_add=0`, exit 0); the dispatch log records
the check after the round's single landed line; both lesson citations check out.

Residual risk / verification gaps (disclosed, none actionable in scope):
- `count_ita_v2` (:73-77) greps non-`-z` porcelain v2 output line-wise; a path containing a raw
  newline relies on `core.quotePath` escaping (default on). Not exercised here; the current repo
  holds no such path, so it cannot affect this green.
- The selftest does not itself assert emptiness of `git diff --cached --name-only`; 103's
  demonstrated git behavior was verified by this seat's independent sandbox run at git 2.56.0
  only. A future git listing ITA in `diff --cached` would keep the selftest green (v1/v2 counts
  stay authoritative) while silently weakening 103's explanatory sentence — noted for a future
  read of this row, not a current defect.
- Selftest executed as instructed by this seat's assignment (lane's own read-only tool; writes
  confined to its mktemp sandbox and my scratch dir).

Installs: none performed.

Scratch: `/fast/scratch/hyaku/mori-r36/RevQuality103/` (m4-demo.sh, sandbox/ — throwaway).
