# ScoutMisroot — round 26 wave 2 misroot sweep

Seat: MoriR26.ScoutMisroot. Lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`; audited tip
16935e24c93fa7e7567413d7ec091339a5df1474; on-disk lane tree read where stated, else git objects.
Read-only throughout: no file moved, deleted, staged, or committed; no jj at the fleet root; no
subagents, no background jobs. No tool installed or upgraded.

Commands run (abridged): `git -C /home/vgpnk/Projects/shokunin status --porcelain`;
`git -C … ls-files --others --exclude-standard`; `git -C … status --porcelain --ignored=matching -uall`;
`git -C mori-shokunin status --porcelain`; `git -C mori-shokunin ls-files --others --exclude-standard`;
`git ls-files --debug`, `git cat-file -s :<path>`, `git diff --cached --name-status`; targeted
`grep -c`/`grep -n` on the three root additions; `find` for stray trees.

## A. Fleet root /home/vgpnk/Projects/shokunin — untracked files

Direct answer to the assignment: **zero true untracked files** (`??`) at the fleet root.
`git status --porcelain` emits 18 lines, none starting `??`; `git ls-files --others
--exclude-standard` at the root is empty. What the root does carry is three *intent-to-add*
entries (porcelain worktree column ` A`), which hold empty index placeholders
(`git cat-file -s :<path>` = 0, index blob e69de29, `flags: 20004000`, and
`git diff --cached --name-status` empty), plus 13 tracked-worktree modifications.
Fleet `.git/index` mtime `2026-10-22 11:16:51 -0300`, so the intent-to-add marks were made
inside the round-26 window.

Intent-to-add files, each checked for mori round 26 / MoriR26 seat content:

| Path (fleet root) | Size / mtime | Content check | Names mori r26 or MoriR26? |
|---|---|---|---|
| `.scratch/goal-20261022-hyaku-12h.md` | 17367 B, 2026-10-22 04:54:00 | names mori only as lane B4 at `mori (r24)` (lines 101–102); `grep -cE 'r26\|round ?26\|MoriR26'` = 0 | no |
| `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` | 10738 B, 2026-10-22 05:01:42 | bytecode; `grep -ac mori` = 0 | no |
| `write` | 25 B, 2026-10-21 19:52:50 | regular file; one `agent://` URI to an opaque agent id (id not copied); no lane, round or seat token | no |

Tracked files modified in the worktree, same check:

- `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` — 57248 B, 708 lines, mtime
  `2026-10-22 11:07:17`. **This is the only uncommitted fleet-root file whose content names mori
  round 26**: line 700 `2026-10-22T10:05:13-03:00 launch mori round=26 pgid=1826598
  driver=hyaku-inline attempt=1`. Case-sensitive `MoriR26` count in the whole log = 0, so no
  wave-2 seat name appears there. Expected fleet state, not a defect.
- `/home/vgpnk/Projects/shokunin/.ufo/state/mori.report-baseline` — 68 B, mtime
  `2026-10-22 10:05:12` (one second before the round-26 launch on line 700). Contains the token
  `26` once; no `round`, `session`, `pgid` keys. Path only; values not copied (privacy).
- 10 further `.ufo/state/*.report-baseline` modifications (chousa, kagi, kaidoku, kake, kama,
  kengaku, kumitate, mado, tameshi, tsukuroi) and 3 additions (kotoba, kotodama, revenger) —
  fleet dispatch state, no mori-r26 content read.

Stray directories at the fleet root (invisible to `git status` because they hold no files, or
their one file is ignored by `.gitignore:1 *-shokunin/`):

- `bash: ` — a directory named with a trailing space containing one file whose entire name is the
  shell error string `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh:
  No such file or directory` (10139 B, mtime `2026-10-18 14:01:47`). First lines are a JSON seat
  payload belonging to another lane; `grep -cE 'mori|r26|round ?26'` = 0. Redirect-target
  misroot, three days older than round 26.
- `mori-shokukin/` — 0 files, only an empty `.ufo/`; a one-letter typo of this lane's directory
  name and the closest thing in this sweep to a path that could capture a mistyped target.
- `tameshi-shokukin/` — 0 files, empty skeleton `.ufo/waves/round-18/w1`,
  `.ufo/waves/round-19/w1`, `tameshi-shokunin/.ufo/waves/round-19/w1`.
- `kaidoku-sh2/` — empty directory.
- None of these names mori round 26 or a MoriR26 seat.

## B. Lane /home/vgpnk/Projects/shokunin/mori-shokunin — untracked files

`git status --porcelain` for the lane: `## HEAD (no branch)`, one ` M`, `?? .scratch/`,
`?? .ufo/waves/round-26/w2/`.
`git ls-files --others --exclude-standard` = 3640 entries: 3639 under `.scratch/`, 1 under
`.ufo/waves/round-26/w2/` (`swarm-registry.json`), and **0 outside those two paths** — so the
requested list (untracked, not under `.scratch/` or `.ufo/waves/round-26/w2/`) is empty.

Ignored-untracked in the lane, outside those two paths (lane `.gitignore:1-3` plus jj internals):
`.jj/.gitignore`, `.jj/repo/`, `.jj/working_copy/`, `.ufo/interactive-sessions/`,
`.ufo/worktrees/` (six worktrees, three at round-19 sparse branches), `tools/__pycache__/`.
No misrooted seat file among them.

## C. Verdicts

| # | What it attacks | Finding | Verdict |
|---|---|---|---|
| 1 | Assignment: untracked at the fleet root naming mori r26 / a MoriR26 seat | Only `.ufo/watchdog.log:700` names mori round 26, and it is a tracked modification, not untracked; zero `MoriR26` matches anywhere in the root additions; zero `??` entries at the root | holds (no mori misroot at root) / defect (low) for root hygiene, rows 3–5 |
| 2 | Lane tip under attack 16935e24 | HEAD is detached at `ee83a88` (`2026-10-22 11:31:43`, "wave-2 spec/run re-rendered at 16935e24…"); `git merge-base --is-ancestor 16935e24 HEAD` = YES, with `2a23fbd` between; local `master` = `origin/master` = `ee83a88`; the lane is jj-colocated (`.jj/` present), so a detached HEAD is the normal jj posture. The tree on disk is 2 commits newer than the audited tip, and 16935e24 is contained in it | holds (no misroot) |
| 3 | Lane worktree vs audited tip | `.ufo/waves/round-26/w1/SrcEarlyoomKillC.md` is modified in the worktree: `git diff --numstat` = 54 insertions / 65 deletions, and it changed under me between two reads (25199 B mtime 11:33:28 → 24935 B mtime 11:34:41), i.e. a live writer is rewriting a wave-1 report during wave 2, two minutes after the wave-2 commit. Added lines contain 0 hits for kotoba/kotodama/tsukuroi/kumitate/kaidoku/tameshi and one hit for `SrcEarlyoomKillC`, so no evidence of another lane's content. Any consumer reading the worktree instead of `16935e24`/`ee83a88` sees a different w1 report | defect (low): uncommitted drift on a tracked w1 report, actively growing |
| 4 | Fleet root hygiene | `write` at the fleet root: 25-byte regular file, mtime `2026-10-21 19:52:50` (before the mori round=26 launch at `2026-10-22T10:05:13`), content is a single `agent://` URI; the name matches the `write` tool's own name, consistent with a call whose `path` argument resolved to `write` relative to the fleet root. [INFERENCE] a misdirected message payload, not a round-26 seat artifact | defect (low): stray file, intent-to-add in the fleet index |
| 5 | Fleet root hygiene | `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` registered intent-to-add in the fleet index (plus `write` and the goal file). `git diff --cached` is empty today, so nothing is actually staged; a later broad `git add -A` at the root would commit bytecode and the stray `write` | defect (low): compiled artifact and stray file queued in the index |
| 6 | Fleet root hygiene | Stray trees `bash: ` (one file), `mori-shokukin/`, `tameshi-shokukin/`, `kaidoku-sh2/` (all 0 files). The `mori-shokukin` typo variant is the nearest match to this lane's directory name; none carries mori-r26 content | defect (low): empty misroot skeletons, path risk only |
| 7 | Lane untracked list | 0 untracked lane files outside `.scratch/` and `.ufo/waves/round-26/w2/`; 3640 total untracked, 3639 `.scratch/` + 1 `w2/swarm-registry.json` | holds |

## D. Remaining unknowns

- Who wrote the stray fleet-root `write` file and which session's `agent://` id it names: the file
  predates the mori round=26 launch by ~14 hours; no owning process inspected.
- Which live process owns `.ufo/waves/round-26/w1/SrcEarlyoomKillC.md` at 11:34:41: attribution is
  by mtime and diff signature only, not by process inspection.
- Whether the L1 intends to commit the fleet-root intent-to-add set (goal file, pyc, `write`);
  only the L1 can drop them, and I did not touch them.
- C1/C2 were not measured by this seat; this report attacks nothing in them beyond lane tree state.
