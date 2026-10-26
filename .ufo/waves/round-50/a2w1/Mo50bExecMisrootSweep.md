# Mo50bExecMisrootSweep — misroot pre-sweep (round 50, attempt 2, wave a2w1)

Seat: `Mo50bExecMisrootSweep`, executor, leaf (no subagents used, no labrat spent).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (MORI). Fleet root: `/home/vgpnk/Projects/shokunin`.
Data revision R = `487941b9395e89678af0053cc443cdb49cdee6e3`; entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`;
lane tip at the time of this sweep = `4548a34dc8b4072abaa4335c1f54a9efcfcc314a` (see §2.1). Contract read first:
`.ufo/waves/round-50/contract.md` (12818 bytes, frozen at `950e99be`).
Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecMisrootSweep/` — created, no temp file was needed, removed at exit.
Disk guard before work: `/fast/scratch/hyaku 24% used, 613.1G free` (`scripts/hyaku/disk-guard.sh status`, rc 0).
Tools installed/upgraded: **none** (no pacman, no uv tool, no npx).
Read-only throughout: no `git add/commit/stash/checkout/reset`, no jj command, no write to `.ufo/state/`, no write to
`.scratch/`, no kernel-log MESSAGE read, no cgroup or service change. Every read/write below is a stat, a read, or a
lane-external scratch listing; **no file outside this report was modified**.

## 1. Assignment and what was measured

1. `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and the untracked enumeration at the fleet
   root and under `/home/vgpnk/Projects/shokunin/.ufo`, filtered for anything that could belong to mori round 50
   (content or name naming mori, round 50, `Mo50`, or this lane's paths).
2. `ls`/`git status` on `/home/vgpnk/Projects/shokunin/mori-shokunin` for stray files any seat wrote outside
   `.ufo/waves/round-50/`.
3. For every candidate: the path, the evidence that it is mori's, and the `cmp`/`cp` command that would move it into
   the lane.

## 2. Fleet root

### 2.1 Porcelain categories (exact)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | awk '{print substr($0,1,2)}' | sort | uniq -c
      1 ??
    153  A
     17  M
```
rc 0. The 153 staged adds are 152 `.tower/comms|missions|reviews|quarantine|state…` paths plus
`.ufo/state/inline-dispatcher.log` — tower/orchestrator material, not this lane's. The 17 modified are 16
`.ufo/state/<lane>.report-baseline` files and `.ufo/watchdog.log` — `.ufo/state/`, out of bounds for this seat and
not mori round 50's to own. The single untracked file is `?? .ufo/state/disk-guard.log` (guard bookkeeping, in
`.ufo/state/`, not mori's).

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all | grep '^??'
?? .ufo/state/disk-guard.log
```
rc 0 — **one untracked file at the whole fleet root, and it is not mori round 50.**

### 2.2 Name scan for mori round 50 outside the lane

```
$ find /home/vgpnk/Projects/shokunin -maxdepth 3 \( -name '*Mo50*' -o -name '*mo50*' -o -name '*r50*' -o -name '*round-50*' \) \
    -not -path './mori-shokunin/*' -printf '%TY-%Tm-%TdT%TH:%TM %y %p\n' | sort
… 2026-10-25T19:24 d ./.ufo/waves/round-50
… 2026-10-25T19:38 d ./.ufo/reports/round-50
… 2026-10-26T09:23 f ./.ufo/prompts/mori-round-50.md
   (plus audio-shokunin/reports/round-50, game-dev-2d/lore reports r50-*, kotoba/kotodama round-50 plans — other lanes' repos)
```
rc 0. Three fleet-root hits, assessed:

| path | content | mori evidence | verdict |
|---|---|---|---|
| `.ufo/prompts/mori-round-50.md` | 2026-10-26 09:23, **tracked** (`git ls-files --error-unmatch` rc 0; `git log -1` → `3e3c1a14 2026-10-26 09:23:50 round-50: mori dispatch evidence (hyaku inline attempt 2)`) | names mori round 50 by design | **correct location** (fleet prompt registry). Not a misroot. |
| `.ufo/waves/round-50/` and `.ufo/waves/round-50/w2/` | **both empty**: `find .ufo/waves/round-50 -type f \| wc -l` → `0`; `git ls-files .ufo/waves/round-50 \| wc -l` → `0`; mtimes `19:24` / `19:26` (2026-10-25) | **none**: zero bytes, so nothing names mori; fleet round 50 is a *shared* fleet round (`.ufo/reports/round-50/` holds `chousa.md` 19:38, `kake.md`, `kotoba.md`, `kotodama.md`, `kumitate.md` — `grep -ril mori` over that dir → rc 1, no hits) | **UNVERIFIED attribution — not claimed as mori's.** Empty dirs are invisible to `git status`; if the orchestrator confirms they are dead, `rmdir /home/vgpnk/Projects/shokunin/.ufo/waves/round-50/w2 /home/vgpnk/Projects/shokunin/.ufo/waves/round-50` (rc 0 only if still empty). No `cmp`/`cp` applies: **there are no bytes to copy into the lane.** |
| `.ufo/reports/round-50/` | 5 other-lane reports, no `mori.md` | none | other lanes'; leave alone. Mori has filed nothing at the fleet root for round 50, so nothing of mori's is stranded there. |

**Result: nothing belonging to mori round 50 exists at the fleet root, so no relocation into the lane is possible or
needed.** (`.ufo-scratch/` at the fleet root holds only `RevengerAuditorHistory` from 2026-10-25 07:41 — another
lane's, not mori round 50.)

## 3. Lane: stray files written outside `.ufo/waves/round-50/`

### 3.1 Tracked tree is clean — no seat wrote to a protected path

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain | grep -cE '^( M|M |MM)'
0
```
rc 0. **Zero modified tracked files**: `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`,
`considerthese/`, the counters/predicates/controls under `.ufo/waves/round-50/` and `corpus/evidence/sources-r50/` are
all at `4548a34d`, unmodified by any a2w1 seat so far. So the misroot risk for *claim* surfaces this wave is zero.

### 3.2 Every untracked path in the lane, outside `.ufo/waves/round-50/` — snapshot 2026-10-26T09:54:03-03

```
$ git status --porcelain --untracked-files=normal
?? .ufo/waves/round-40/scratch/mori-conform-selftest-0rxgpfar/     ?? …-dra5yrh3/   ?? …-tdpskkl4/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-15bddcj3/     ?? …-fct02t0z/   ?? …-v4mvkufb/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-19j6vvca/     ?? …-k4w8jodr/   ?? …-ve0mnp68/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-5fc15qrp/     ?? …-rg2rfuvr/   ?? …-ys1qenzp/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-5ukdmji0/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-7pie5l06/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-_s88sxyc/
?? .ufo/waves/round-40/scratch/mori-conform-selftest-asm8qien/
?? .ufo/waves/round-50/a2w1.ready
?? .ufo/waves/round-50/a2w1.ready.dispatched
?? .ufo/waves/round-50/a2w1/
```
rc 0 — 19 lines: 16 round-40 scratch dirs (the stray family) + the 3 expected round-50 wave-state entries.
Plus **empty** dirs that porcelain cannot show (git does not track directories), found by `find -type d -empty`:
`.ufo/waves/round-38/scratch/{c1-9wz4iqqu,mori-c1-tool-i5236vo8}` (created 09:41 today) and
`.ufo/waves/round-39/scratch` (created 09:43 today).

### 3.3 Evidence that the family is mori's, and the identity commands

| path | evidence it is mori's | `cmp`/`cp` command | disposition |
|---|---|---|---|
| `.ufo/waves/round-40/scratch/mori-conform-selftest-*/` (16 dirs, 117 files, 2.7M at 09:54:03; 4 dirs/552K at 09:51:57, 9 dirs at 09:53) | content is lane instruments under lane paths: each surviving dir holds 4–9 `counter-{predicate,head_pin,tool_resolve,bounded_reads,timeout_scope,timeout_scope_shadow,drain_bind,drain_bind_decoy,timeout_state}.py` mutants, sizes 22036–22529 vs `.ufo/waves/round-40/count-c8.py` = **22310** — mutants of round-40's counter; the creator is `.ufo/waves/round-40/conform.py:70` `SCRATCH_ROOT = <LANE>/.ufo/waves/round-40/scratch` with `:743 mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)`, `:765 rmtree(..., ignore_errors=True)`. Only a mori seat runs lane scripts under this LANE. | nothing to copy: these are derived fixtures. Prove the pristine source is already in the lane, `cmp -s .ufo/waves/round-40/scratch/mutconform-arms2/conform-pristine.py .ufo/waves/round-40/conform.py` → **rc 0**. | not mine to delete. The L1's `rm -rf` (already staged by peer `Mo50bExecScratchInventory` §4 as a dry-run-then-delete pair) is the disposition; the bytes are reproducible from `round-40/{conform.py,count-c8.py}` at any revision. |
| `.ufo/waves/round-40/scratch/mutconform-arms2/` + `selftest-v3-draft.txt` + `selftest-v3-draft2.txt` (fixed, all mtime 2026-10-26T09:07:15) | `cmp -s mutconform-arms2/conform-pristine.py .ufo/waves/round-40/conform.py` → **rc 0** (byte-identical to the tracked tool); the mutant pair differs by one line only: `diff` → `291c291 <     if name in conditional: --- >     if False and name in conditional:` (rc 1). The drafts carry `CONFORM_SELFTEST pass=9 fail=2` / `pass=11 fail=0` — arm text of the lane's conform tool. | `cmp -s` above proves no unique bytes; nothing to copy. | untracked, unignored, no round-50-only content. Safe to delete once no report cites them; peer `Mo50bExecRound49Seats` and `Mo50bScribeLogScorecard` cite them by *name* only (§3.4). |
| `.ufo/waves/round-38/scratch/{c1-9wz4iqqu,mori-c1-tool-i5236vo8}` (empty, 09:41) | names are the lane counter's own: `.ufo/waves/round-38/count-c1.py:992 tempfile.mkdtemp(prefix="mori-c1-tool-", dir=_scratch_parent())`, `:1029 mkdtemp(prefix="c1-", dir=_scratch_parent())`, and `:907 _scratch_parent()` returns the round-38 scratch root. | no bytes (`find … -type f \| wc -l` → `0`); nothing to copy. | `rmdir` only; invisible to `git status` (empty), so no count impact. |
| `.ufo/waves/round-39/scratch` (empty, 09:43) | the `scratch` arm of `round-40|41|42/conform.py` carries the literal `round-39` scratch root (`round-40/conform.py:470,732`), so a fixture run materialises this path. | no bytes; nothing to copy. | `rmdir` only. |

### 3.4 The residue is regenerating, not historical

Peer `Mo50bExecScratchInventory` measured **0** `mori-conform-selftest-*` dirs at 09:36 and 9 at 09:50 "from a
sibling running `.ufo/waves/round-40/conform.py --selftest`". This sweep, independently, on the same path:

```
09:51:57 →  4 dirs   (552K,  27 files)
09:53:19 →  9 dirs   (1.6M,  71 files)
09:54:03 → 16 dirs   (2.7M, 117 files)   # ~3.5 dirs / 20 s while sampled
```
Every new dir is world-unreadable-looking `drwx------` created by the run and removed by `shutil.rmtree(..., ignore_errors=True)`
only when the run finishes; the survivors are the arms that fail or are killed. They are **untracked but not ignored**
(`.gitignore` in the lane lists only `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `__pycache__/`, `*.pyc`,
`.scratch/`), so they inflate exactly the number the round-49 closure item 4 tells the L1 to record.

### 3.5 Live second sink: the lane `.scratch/` (gitignored)

```
09:54:54–58 → .scratch/pin-check-{31g_s535,dfbw9cde,dgt2c3zs,kmuiviav}   (4 new today)
today's additions under .scratch: 4    total top-level entries: 191    directories: 187    du -sh: 26G
```
A peer's pin-check selftest is writing there **now**. Metadata only (`find -printf`, `du -sh`, `ls -d …|wc -l`) was
read; no file inside `.scratch/` was opened. This is the D-e residue the closure names, being re-filled by this wave.

## 4. Lane root listing vs porcelain

`ls -la` of the lane root shows 28 entries; porcelain shows none of them untracked and none modified, so every one is
either tracked at `4548a34d` or ignored. Two entries deserve an explicit non-attribution so no later seat re-flags them:

| lane-root entry | stat | mx status | round-50? |
|---|---|---|---|
| `0` | 31 bytes, `NF=13 cells=11 double_quotes=0`, mtime 2026-10-23 23:27 | **tracked** (`git ls-tree -r HEAD` lists it; introduced by `96f7f97e round-38: … misroot relocations (0, m9)`) | **No** — a round-38 relocation, already committed. |
| `--repo` | empty directory, mtime 2026-10-24 01:27 | **empty → invisible to porcelain**, untracked | **No** — dated a day before this round; a shell-quoting accident from an earlier round. `rmdir '/home/vgpnk/Projects/shokunin/mori-shokunin/--repo'` if the L1 wants it gone; no bytes. |

Also `.ufo/waves/round-50/__pycache__/` (mtime 09:27, `count-c1.cpython-314.pyc`) and `tools/__pycache__/`
(2026-10-25 19:36): both gitignored, both inside allowed scope (round-50 dir / tools cache), no action.

## 5. Counts the round-end record will need (measured, not projected)

| metric (lane, 2026-10-26T09:54) | value | command |
|---|---|---|
| porcelain lines incl. ignored | 193 | `git status --porcelain --ignored \| wc -l` |
| of which `.scratch/` | 170 | `… \| grep -c '^!! \.scratch/'` |
| of which `round-40/scratch` | 12 | `… \| grep -c 'round-40/scratch'` |
| of which `round-38/scratch`, `round-39/scratch` | 0 and 0 (dirs empty ⇒ invisible) | `… \| grep -c 'round-38/scratch'` |
| tracked modified | 0 | `git status --porcelain \| grep -cE '^( M\|M \|MM)'` |
| untracked visible | 19 (16 stray + 3 wave-state) | `git status --porcelain --untracked-files=normal` |

These move minute to minute while the mutation sweep runs; the L1 must take the before/after pair **after** the sweep
is stopped (or with the peer's `TMPDIR` pinned), otherwise the "after" count can exceed the "before".

## 6. Limits

- The 16 `mori-conform-selftest-*` dirs are attributed to *a* round-50 seat, not to a named one: the creator is proven
  (`round-40/conform.py:743`), the timing coincides with a2w1, and no other lane writes under
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/` — but I could not see the invoking process (`ps` was not
  sampled for it). Marked [INFERENCE] where named.
- Empty directories are invisible to every porcelain-based gate; my empty-dir scan is `find -type d -empty` at one
  instant, so a dir created and removed between samples is simply not in the record.
- Attribution of the fleet-root `.ufo/waves/round-50/{,w2}` dirs is **UNVERIFIED**: fleet round 50 is shared with at
  least five other lanes, and the two dirs hold zero bytes.
- I did not audit other lanes' repos, `/home/vgpnk/Projects/shokuknow`, `.ufo/state/` contents, or `.scratch/` contents
  (metadata counts only, per the operator scratch directive).
- No `cmp` of a *relocated* file exists to report for the fleet root because there was nothing there to relocate; the
  only identity checks possible were the lane-internal pristine-fixture ones, and both are recorded with their rc.

## Findings

- **MED — the round-40 scratch debris is live and growing inside the lane, and it is counted by the very gate the
  closure uses.** `.ufo/waves/round-40/scratch/mori-conform-selftest-*/` — 4 dirs/552K at 09:51:57, 9 at 09:53:19,
  16 dirs/117 files/2.7M at 09:54:03; untracked and **not** ignored (lane `.gitignore` has no `round-40` rule), so it
  enters `git status --porcelain` and the closure-item-4 before/after count. Creator: `.ufo/waves/round-40/conform.py:70,743,765`.
- **MED — a second, older scratch root is being written too, so deleting only the round-40 family leaves two behind.**
  `.ufo/waves/round-38/scratch/{c1-9wz4iqqu,mori-c1-tool-i5236vo8}` (empty, created 09:41) and
  `.ufo/waves/round-39/scratch` (empty, created 09:43). Mechanisms: `.ufo/waves/round-38/count-c1.py:907,992,1029`
  (`_scratch_parent()` → round-38 scratch) and `round-40/conform.py:470,732` (the `scratch` arm's literal `round-39`
  root). Both are empty, so they cost no porcelain lines today — but they are silent write sinks.
- **MED — the lane `.scratch/` is being re-filled during this wave** (`pin-check-*` ×4 created 09:54:54–58; 191
  top-level entries, 187 dirs, 26G). Read-only metadata only. The round-end deletion has a moving target.
- **LOW — the round-50 wave run writes its fixtures under lane historical rounds, not under
  `/fast/scratch/hyaku/mori-r50/<seat>/`** as the operator directive requires (all three paths above are inside the
  lane repo). Nothing was written *outside* the lane; the violation is that lane `.ufo` and `.scratch` are being used
  as scratch at all.
- **LOW — fleet-root `.ufo/waves/round-50/` and `/w2` are empty dirs (2026-10-25 19:24/19:26) that no git command can
  see**, attribution unverifiable (fleet round 50 is shared; `.ufo/reports/round-50/` has five other-lane reports and
  no mori one). No bytes, no copy; `rmdir` only on the orchestrator's word.
- **LOW — lane root carries two pre-round-50 artifacts invisible to porcelain**: tracked file `0` (31 bytes, round-38
  relocation `96f7f97e`) and empty untracked dir `--repo` (2026-10-24 01:27). Neither is round 50's; recorded so a
  later sweep does not re-attribute them.
- **INFO — no misroot of claim surfaces**: `git status --porcelain` shows 0 modified tracked files in the lane, so no
  a2w1 seat has touched `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`, `considerthese/`, the
  frozen counters/controls, or any file outside `.ufo/waves/round-50/`; and there is no mori round-50 file at the fleet
  root needing salvage.
