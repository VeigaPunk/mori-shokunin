# Mo53ExecMisrootSweep — mori round 53, wave w1, misroot pre-sweep (read-only)

Seat: `Mo53ExecMisrootSweep` (executor, lane member; no subagent dispatched).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
Scratch (created, used, removed at finish): `/fast/scratch/hyaku/mori-r53/Mo53ExecMisrootSweep/`.
Snapshot time: 2026-10-26 23:20–23:30 -0300. Lane tip at the last read: `fd86307ad54c13edb8b6dd13182a2ad196f42fcd`.

**Verdict in one line: there is no mori round-53 misroot at the fleet root or under the fleet's `.ufo/` — the copy-in
table is empty; the two named lane-root oddities (`0`, `--repo`) are seat misroots of rounds 38 and 39/40 that were
already catalogued and relocated, and one NEW untracked lane-root artifact (`r53-data.tar`) appeared during this wave
and is the only path in scope that still needs an L1 decision.**

## 0. What I did, and what I did not do

Read-only throughout: `git status`, `git ls-files`, `git log`, `git show`, `git diff`, `git archive` (read-only form),
`git rev-parse`, `git check-ignore`, `git fsck --unreachable`, `find`, `grep`, `sha256sum`, `cmp`, `tar -t/-x`, and the
lane's own detection-only tool `tools/mori-misroot-sweep.py`.

Not done (by rule): no `git add/commit/stash/checkout/reset/pull/push` in the lane or the fleet root, no mutating `jj`,
no write to any file under the lane other than this report, no write to `SKILL.md` / `SHONEN.md` / `SCORECARD.md` /
`LOG.md` / `PROVINCE.md` / `corpus/` / `tools/` / `considerthese/` / `.ufo/waves/round-53/` (other seats' files), no
`pacman`, nothing installed, no host configuration read or written.

Two files were created **by me inside the lane root** during the investigation and removed by me before finishing:
`head2.tar` and `mech-test.tar` (both `git archive -o` outputs of a relative path — see §5.3). Disclosed here in full;
both are gone (`rm` exit 0 each), and the lane's untracked set outside `.ufo/waves/round-53/` contains neither.

## 1. Fleet root — the primary scope of this seat

### 1.1 `git status --porcelain` (no pathspec)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
[END — empty output, exit 0]
```

No modified, no deleted, and no untracked path at the fleet root. Repeated at 23:20:13, 23:22:47 and 23:29:58 -0300 —
empty every time. (At 23:22:47 the fleet root briefly showed ` M scripts/hyaku/inline-dispatcher.py`; by 23:23:36 the
diff was empty again and porcelain was clean. That file is the hyaku dispatcher's, not mori's; the diff contained zero
matches for `mori|Mo53|round-53`.)

### 1.2 Untracked files at the fleet root (porcelain alone under-reports; `-uall` and content grep added)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all
[END — empty output, exit 0]
```

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all -- .ufo
[END — empty output, exit 0]
```

The fleet's `.ufo/` holds 4,147 tracked paths; the only untracked-and-ignored entries under it are
`.ufo/state/*` (the dispatcher's runtime state — excluded by the seat rules) and `.ufo/watchdog.log` (ignored).

### 1.3 The lane's own misroot sweep, pointed at the fleet root, for r53

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecMisrootSweep && TMPDIR=$PWD/tmp \
    python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-misroot-sweep.py \
      --fleet-root /home/vgpnk/Projects/shokunin --lane mori --round 53
{"candidate_count": 0, "candidates": [], "detection_only": true, "finding": "MORI_MISROOT_CLEAN",
 "fleet_root": "/home/vgpnk/Projects/shokunin", "lane": "mori", "moves_or_deletes": false, "round": 53,
 "scan": {"bytes_read": 0, "non_regular_skipped": 0, "read_cap": 65536, "regular_files": 0,
          "truncated_files": 0, "unreadable": 0, "untracked_entries": 0},
 "schema": "mori-misroot-sweep-v1"}
exit 0
```

`untracked_entries: 0` — the fleet root has nothing for the tool to read, by name or by content.

### 1.4 Content sweep of the fleet for r53 markers (the instrument's other blind spot)

`git status` only sees untracked non-ignored paths; the sweep below covers every file the fleet tracks plus the
ignored trees, looking for `Mo53` / `round-53` / `mori-shokunin/.ufo/waves/round-53`:

```
$ grep -rIl --exclude-dir=.git --exclude-dir=.jj --exclude-dir='*-shokunin' \
      --exclude-dir=.tower --exclude=MANIFEST.json -E 'Mo53' . 2>/dev/null
./.ufo/state/inline-dispatcher.log
```

```
$ grep -rl 'mori-shokunin/.ufo/waves/round-53' . --exclude-dir=.git --exclude-dir=.jj \
      --exclude-dir='*-shokunin' --exclude=MANIFEST.json 2>/dev/null
./.ufo/prompts/mori-round-53.md
./.ufo/state/inline-dispatcher.log
```

Two hits, both fleet-side infrastructure and neither a seat write:

* `.ufo/state/inline-dispatcher.log` — the dispatcher's runtime log; it names the r53 seats it spawned (e.g. lines
  3604–3734, `spawn-cap …/mori-shokunin/.ufo/waves/round-53/w1.ready Mo53Fr01 …`). Under `.ufo/state/`, which the
  seat rules exclude from my scope. Not a misroot: it is the launcher's own log, in the launcher's own directory.
* `.ufo/prompts/mori-round-53.md` — **tracked** (`git ls-files -- .ufo/prompts/mori-round-53.md` prints it), mtime
  2026-10-26 22:10 -0300. This is the fleet-side prompt the L1 was dispatched with, the counterpart of the
  lane-side `contract.md`. Tracked and in place, not a stray.

A filesystem sweep of the same tree for anything written during the r53 wave (22:08 onward) outside the lane
directories, `.git/`, `.jj/`, `.tower/` and `.ufo/state/` returned only: the fleet's own prompt files
(`.ufo/prompts/{mori,kake,chousa,mado,kengaku,tsukuroi}-round-*.md`), other lanes' fleet reports
(`.ufo/reports/round-44/tsukuroi.md`, `.ufo/reports/round-50/kama.md`), `scripts/hyaku/lane-addendum.md`,
`.scratch/goal-20261026-hyaku-run9.md`, `.ufo/watchdog.log` and `MANIFEST.json`. **No mori round-53 seat file among
them.**

### 1.5 The copy-in table — EMPTY

The seat's deliverable is "path, evidence it is mori's, the `cmp` command to copy it into the lane". Measured
answer:

| path (fleet root / fleet `.ufo/`) | evidence it is mori's | `cmp` command |
|---|---|---|
| *(none)* | — | — |

There is no untracked file at the fleet root or under the fleet's `.ufo/` at any point in the 23:20–23:30 window, and
no file of any age in those trees contains mori r53 seat output other than the dispatcher's own log and the tracked
prompt. **Nothing to copy; no `cmp` to run.** Had a candidate existed, the command would have been
`cmp <fleet-path> /home/vgpnk/Projects/shokunin/mori-shokunin/<same-relative-path>` (exit 0 = byte-identical),
followed by removing only the fleet copy.

## 2. The two named lane-root oddities — are they seat misroots of an earlier round?

### 2.1 `0`

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files --stage -- 0 '--repo'
100644 4225074ec63c8d7ea66463d31a44df2f437bc9f6 0	0

$ git -C …/mori-shokunin log --format='%h %s' -- 0
96f7f97e round-38: residual re-check (8 seats, reports in resid/), red receipts re-emitted full-output at
b6993744, lesson M16-M19 repairs, misroot relocations (0, m9), dispatch-log landing record, reproducers committed

$ stat -c '%n size=%s mtime=%y' …/mori-shokunin/0
/home/vgpnk/Projects/shokunin/mori-shokunin/0 31 2026-10-23 23:27:48 -0300
$ sha256sum …/mori-shokunin/0
b24122a0f0245c0aa6961fa234fb40adc4527bcd8e61c3c1e247ec8ba1c3a078  …/mori-shokunin/0
$ cat …/mori-shokunin/0
NF=13 cells=11 double_quotes=0
```

**Yes — it is a seat misroot, of round 38, not round 53, and it was already relocated and committed.**
`git show 96f7f97e -- 0` prints `new file mode 100644 … +NF=13 cells=11 double_quotes=0`; the commit subject names
the relocation ("misroot relocations (0, m9)"), and `git show --stat 96f7f97e` shows the same commit moving
`m9-misroot-mori-source-drift-f725f30.py` into `.ufo/waves/round-38/…`. The provenance is documented in
`corpus/lessons/round-38.md:48` (lesson M17): a round-38 wave-1 seat wrote a probe output to the fleet root; the L1
copied it byte-exact into the lane at the same relative path (`mori-shokunin/0`), `cmp`-verified it, and removed the
fleet copy. The bytes are the committed bytes, not a worktree drift:

```
$ git -C …/mori-shokunin show HEAD:0 | cmp - …/mori-shokunin/0
cmp exit=0
```

(`git show HEAD:0` is byte-identical to the file on disk; the sha256 above is the same value the round-38 lesson and
`Mo50bExecMisrootSweep.md:142` record.) Already catalogued by the round-50 sweep
(`.ufo/waves/round-50/a2w1/Mo50bExecMisrootSweep.md:142`), the round-52 sweep
(`.ufo/waves/round-52/w1/Mo52ExecMisrootSweep.md:157`) and this wave's `Mo53MutC1.md:246`. **No r53 action.**

### 2.2 `--repo` (a directory?)

```
$ git -C …/mori-shokunin ls-files --stage -- 0 '--repo'
100644 4225074ec63c8d7ea66463d31a44df2f437bc9f6 0	0      # '0' only; '--repo' is not a tracked path

$ git -C …/mori-shokunin log --format='%h %s' -- 0
96f7f97e round-38: …                                          # no commit touches '--repo'

$ stat -c '%n %F mtime=%y' …/mori-shokunin/--repo
/home/vgpnk/Projects/shokunin/mori-shokunin/--repo directory 2026-10-24 01:27:38 -0300
$ find …/mori-shokunin/--repo -mindepth 1 | wc -l
0
```

**It is a directory, it is empty, and it is porcelain-invisible** (git does not report empty directories, so
`git status` never names it) — the same blind spot this sweep measured at the fleet root for `ok/` (§3.1).
It is **not** round 53's: its mtime is 2026-10-24 01:27, one day before the r53 freeze, and the round-39 wave-1
closed at 01:23:54 on 2026-10-24 while the round-40 instrument commit landed at 01:31:20 — the directory was created in
that 8-minute gap, i.e. during the round-39/40 window, from a command that took `--repo` as a literal path
(a shell-quoting accident; the round-39/40 instruments all take `--repo <path>`, e.g.
`.ufo/waves/round-39/count-c7.py:389`, `.ufo/waves/round-39/conform.py:520`). Already catalogued by
`.ufo/waves/round-50/a2w1/Mo50bExecMisrootSweep.md:143` and `.ufo/waves/round-52/w1/Mo52ExecMisrootSweep.md:116`.
It holds **no bytes**, so there is nothing to `cmp` and nothing to copy:

```
$ find /home/vgpnk/Projects/shokunin/mori-shokunin/--repo -mindepth 1 | wc -l   → 0
```

Verdict: a seat misroot of the round-39/40 window, already recorded; empty; **no r53 action** (the L1 may `rmdir` it —
it is the L1's to remove, not a seat's).

## 3. Empty-directory blind spot (the instrument's own limit), measured

`git status` cannot see an empty directory, and the lane's sweep tool reads only what `git status` reports. The
measured count is `find -type d -empty`.

### 3.1 Fleet root

```
$ find /home/vgpnk/Projects/shokunin -maxdepth 1 -type d -empty ! -name '.git' ! -name '.jj' ! -name '.tower' \
      ! -name '*shokunin' -printf '%p birth=%w mtime=%TY-%Tm-%Td %TH:%TM\n'
./ok mtime=2026-10-25 16:43
```

`/home/vgpnk/Projects/shokunin/ok/` — 0 entries, birth 2026-10-25 16:43:05.478289356, **the identical nanosecond** as
`mori-shokunin/.scratch/r47-ScribeQuality/2echo/` recorded in `.ufo/waves/round-47/w2/ScoutMisroot.md:157-169` (the
`2echo` sibling no longer exists; the lane `.scratch/r47-ScribeQuality/` directory is gone). That sweep attributed it
to a round-47 wave-1 seat running a relative path from the fleet-root cwd, and marked the exact command UNVERIFIED;
`.ufo/waves/round-52/w1/Mo52ExecMisrootSweep.md:74-76` re-recorded it and left it alone. **Not round 53's** (born
2026-10-25, one day before r53's freeze), **empty**, and it names nothing mori. No bytes, nothing to copy, nothing to
`cmp`.

Also empty at the fleet root's `.ufo/` level: `.ufo/waves/round-25` (mtime 2026-10-25 09:50),
`.ufo/waves/round-62/w2` (10:37), `.ufo/waves/round-33/falsify` (15:08), `.ufo/waves/round-50/w2` (19:26),
`.ufo/waves/round-34/wave1` (2026-10-26 02:48) — all predate the r53 wave (22:08) except the last, which is 19 hours
earlier, and none is mori's.

### 3.2 Lane, outside `.ufo/waves/round-53/`

```
$ git -C …/mori-shokunin status --porcelain --ignored=matching --untracked-files=all \
    | grep -v -E '\.ufo/waves/round-53/'
?? r53-data.tar
!! .jj/.gitignore
!! .jj/repo/
!! .jj/working_copy/
!! .ufo/waves/round-20/falsify/NoHarmRun/rg/.scratch/
!! .ufo/waves/round-44/__pycache__/ … !! .ufo/waves/round-52/controls/__pycache__/
!! tools/__pycache__/
```

Every `!!` line is either the lane's own jj store, a `__pycache__` (gitignored by the lane's `.gitignore`), or the
round-20 falsify scratch — all pre-existing, none round 53's, none mori r53 seat output. `find -type d -empty` over
the lane outside `.ufo/waves/round-53/` returns only historical fixture directories (round-13/15/16/17 evidence trees,
mtimes 2026-10-20). **`--repo` is the only empty directory in the lane that is not part of a historical evidence tree,
and it is the round-39/40 artifact of §2.2.**

## 4. The one NEW in-scope path: `r53-data.tar` (lane root, untracked, appeared during this wave)

```
$ stat -c '%n size=%s mtime=%y' /home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar
/home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar 51200 2026-10-26 23:19:41 -0300
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar
e8f6f1c5865446514936883d611475766591f564a16d1b6e8567058f93255be4  …/r53-data.tar
$ tar -tvf …/r53-data.tar
drwxrwxr-x root/root         0 2026-10-26 22:37 tools/
drwxrwxr-x root/root         0 2026-10-26 22:37 tools/fixtures/
drwxrwxr-x root/root         0 2026-10-26 22:37 tools/fixtures/mori-commit-runway/
-rw-rw-r-- root/root     24910 2026-10-26 22:37 tools/fixtures/mori-commit-runway/cases.json
-rwxrwxr-x root/root     14785 2026-10-26 22:37 tools/mori-commit-runway.py
```

**Identity (byte-exact, reproduced in my scratch):** the file is the `git archive` of the **C2 data commit**
`2a4213bf8da72f7cd78189baa5bb9be825dca1df` restricted to the two C2 data paths:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 2a4213bf8da72f7cd78189baa5bb9be825dca1df \
      tools/mori-commit-runway.py tools/fixtures/mori-commit-runway/cases.json -o "$S/data.tar"
$ cmp /home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar "$S/data.tar"
cmp exit=0
$ cmp …/r53-data.tar "$S/mine.tar"      # the same archive at the later tip 95cf78ee
…/r53-data.tar …/mine.tar differ: char 145, line 1     # differs only in the member mtimes
cmp exit=1
```

So it is mori round-53 material (the C2 tool and its fixtures, as they stood at the data commit) that landed as a
**file in the lane root** instead of in the seat's scratch — exactly the class the operator's scratch rule exists to
prevent. It is untracked, so a `git add -A`-style integration would sweep it into the next commit. It is **not** in
`.ufo/waves/round-53/evidence/freeze-sha256.txt` (`grep -c r53-data` → 0) and no seat's report trailer names it.

Independently spotted by a sibling seat: `Mo53ExecC2Replay.md:318` (it appeared at 23:19:41, the minute that report
was being written) and reported as its finding 8, "not mine". My reading agrees on identity and adds the byte-exact
reproduction above.

**Who wrote it: UNVERIFIED.** What I could and could not establish:

* No process holds it open; `lsof` is unavailable on this host; no `r53-data` string appears in the fleet tree, the
  lane tree, the dispatcher's log or the wave spec (`grep -rln 'r53-data' …` → only the sibling report that spotted
  it). The name is not in any instruction, so it is a seat's own choice.
* The member mtimes (2026-10-26 22:37) are the **committer** date of `2a4213bf`, and the member set is exactly the
  path pair that three r53 seats document extracting: `Mo53CritC2Semantics.md:5`
  ("extracted by `git archive 2a4213bf … tools/mori-commit-runway.py tools/fixtures/mori-commit-runway/cases.json`
  into my scratch"), `Mo53ExecToolPortability.md:19-20` (the same two paths, piped to `tar -x -C .`), and
  `Mo53ExecHostLive.md:4` (the same rev, `| tar -x`). Their reports all show the archive landing in a scratch
  directory; the tar that should have been the intermediate of one of those extractions is here instead. Which seat
  is the author is UNVERIFIED.
* **Mechanism, proven in my scratch (§5.3):** `git -C <repo> archive <rev> <paths> -o <relative-name>` writes the
  output into the **repository root**, not into the shell's cwd. A seat that used `-o r53-data.tar` (a relative name)
  while running from its scratch directory therefore lands the file in the lane root, silently.

**Disposition for the L1:** it is a wave artifact, not content; the bytes are reproducible from the data commit with
the `cmp`-verified command above. The L1 should remove it before the integration commit (it is not in the freeze
list, and leaving it risks a stray blob landing in the next commit). I did **not** remove it: it is not my file, and
the seat rules give me detection and report only.

## 5. Supporting measurements

### 5.1 The frozen bytes are intact after the wave

The L1 committed a data correction during the wave (`fd86307a`, "round-53: data corrections from w1 — tool bounded
reads/strict parsing/case-id guard (+3 cases, 5 hostile checks), two-sided band reading, CPU-hotplug limit, S514
mm_init.c v7.3, dated host sentence"; it touches `SKILL.md`, `corpus/SOURCES.md`,
`corpus/evidence/sources-r53/mm_init.c.v7.3`, `corpus/knowledge/commit-runway-read-r53.md`,
`tools/fixtures/mori-commit-runway/cases.json`, `tools/mori-commit-runway.py` — none of them a frozen file). The freeze
list still verifies against the working tree:

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && \
  sha256sum -c .ufo/waves/round-53/evidence/freeze-sha256.txt | grep -v ': OK$'
(no output)
$ … | grep -c ': OK$'
32
```

All 32 frozen files (contract, both counters, both control builders, the receipts, the census-start, the sweeps, the
selftest receipts, the v7.3/v7.2 source copies) match their frozen sha256 — no frozen file was edited in place.

### 5.2 The C2 data tip moved during the wave — the counters must be re-read at the new tip

The claim's data was frozen at `2a4213bf`; the L1's correction commit `fd86307a` now carries the tool, the fixtures
(26 cases, sha256 `3a1aef20…`), the registry row (`PASS 31/31`) and the entry ("26 frozen cases and 5 hostile-input
checks"). The three numbers are now mutually consistent again, which fixes the inconsistency
`Mo53ExecC2Replay.md` (finding 7) and `Mo53CritC2Semantics.md` (evidence row 10) observed against the earlier
worktree state. What is now stale is the **receipt set**: `.ufo/waves/round-53/evidence/c2-at-data.txt` and
`selftest-c2.txt` were taken at `2a4213bf`, and the tool bytes they cover are not the bytes at `fd86307a`. The
contract's own rule ("the claim is measured with `git show <freeze>`" for frozen files, and the data may be corrected
by the L1) makes this an L1 bookkeeping matter, not a counter change: the C2 counter must be re-run at the new tip for
the receipts to describe the landed bytes. Noted here because the misroot sweep is the seat that re-reads the lane
status and would otherwise be the only witness that the tip moved mid-wave.

### 5.3 Mechanism proof for §4 (and my own two artifacts, disclosed)

```
$ cd /fast/scratch/hyaku/mori-r53/Mo53ExecMisrootSweep/tmp
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 2a4213bf tools/mori-commit-runway.py -o mech-test.tar
rc=0
$ ls -la /fast/scratch/hyaku/mori-r53/Mo53ExecMisrootSweep/tmp/mech-test.tar
ls: cannot access '…/tmp/mech-test.tar': No such file or directory
$ ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/mech-test.tar
-rw-r--r-- 1 vgpnk vgpnk 20480 Oct 26 23:25 /home/vgpnk/Projects/shokunin/mori-shokunin/mech-test.tar
$ rm -f /home/vgpnk/Projects/shokunin/mori-shokunin/mech-test.tar     # removed, exit 0
```

`git archive -o <relative-name>` under `git -C <repo>` writes into the **repo root**, not the cwd — the cwd is
irrelevant to the output path. The same mistake by me produced `head2.tar` at 23:20:57 (removed, exit 0). Both
artifacts are gone; the lane's untracked set outside `.ufo/waves/round-53/` now contains only `r53-data.tar`.

A mitigation for the wave, offered as an observation, not as a change to any frozen instrument: the C2 counter itself
is immune, because `count-c2.py:409` uses `git -C repo archive <rev>` **without** `-o` and pipes stdout into
`tar -x -C <scratch-tree>`. The exposure is only for seats that use the `-o` form.

### 5.4 Prior-round catalog (so this seat is not the first to say it)

* `.ufo/waves/round-47/w2/ScoutMisroot.md:157-169` — fleet-root `ok/` and the lane `.scratch/r47-ScribeQuality/2echo/`
  sibling, same birth nanosecond, author UNVERIFIED.
* `.ufo/waves/round-50/a2w1/Mo50bExecMisrootSweep.md:142-146` — lane-root `0` (tracked, round-38 relocation) and
  `--repo` (empty, porcelain-invisible, round-39/40 window).
* `.ufo/waves/round-52/w1/Mo52ExecMisrootSweep.md:74-76, 116, 157` — `ok/`, `--repo`, the eight tracked lane-root
  strays, and the "a porcelain-only misroot count under-reports; the measured count is `find -type d -empty`" limit.
* `.ufo/waves/round-53/w1/Mo53MutC1.md:246` and `Mo53ExecC2Replay.md:318, 377` — this round's own sightings of `0`
  and of `r53-data.tar`.

## 6. Scope discipline — what I did not judge

I did not score C1 or C2, did not re-count votes, did not read the RECHECK ballots, did not touch the counters,
the tool, the fixtures, the entry, `SKILL.md` or any corpus file, and did not propose any change to a frozen
predicate, counter, control or kill rule. §5.2 is a bookkeeping observation about receipts that cite a tip which has
moved; the decision on re-running the counter is the L1's.

No tool was installed or upgraded (nothing in this task needed one), so no tool/version/channel line is owed.
`scripts/hyaku/disk-guard.sh status` was read before the work: `/fast/scratch/hyaku` at 25 % with 606.9 G free — no
ENOSPC condition, no stop needed.

## 7. Cleanup

`/fast/scratch/hyaku/mori-r53/Mo53ExecMisrootSweep/` (196 K at its largest) removed at finish; the two lane-root
files I created (`head2.tar`, `mech-test.tar`) were removed as they were made. The lane's untracked set outside
`.ufo/waves/round-53/` is `r53-data.tar` alone — not mine, reported in §4. The fleet root is clean.

## Findings

1. **LOW — an untracked tarball at the lane root, created during this wave.**
   `/home/vgpnk/Projects/shokunin/mori-shokunin/r53-data.tar` (51,200 B, mtime 2026-10-26 23:19:41 -0300, sha256
   `e8f6f1c5865446514936883d611475766591f564a16d1b6e8567058f93255be4`, five members) is the byte-exact `git archive` of
   the C2 data commit `2a4213bf` over the two C2 data paths (`cmp` exit 0 against a scratch reproduction). It is
   untracked, absent from `evidence/freeze-sha256.txt`, and named by no report trailer. Author UNVERIFIED; the
   mechanism is `git -C <repo> archive … -o <relative-name>` writing into the repo root (proved in §5.3), and the
   path pair matches the archive three r53 seats document extracting. Untracked, so the next `git add -A`-style
   integration can sweep it in. L1 decision: remove before the integration commit. Independently reported by
   `Mo53ExecC2Replay.md:377` (its finding 8).
2. **LOW — the C2 data tip moved mid-wave, so the at-data receipts now describe superseded bytes.**
   The L1's correction commit `fd86307a` (tool, fixtures 26 cases sha256 `3a1aef20…`, registry row `PASS 31/31`,
   entry "26 frozen cases and 5 hostile-input checks") is the live tip; `.ufo/waves/round-53/evidence/c2-at-data.txt`
   and `selftest-c2.txt` were taken at `2a4213bf`, whose tool bytes differ. The three numbers are mutually consistent
   again (the earlier worktree mismatch, `Mo53ExecC2Replay.md` finding 7, is fixed), but the receipts need re-running
   at the new tip. The frozen counter is unchanged and stays frozen.
3. **INFO — no mori round-53 misroot exists at the fleet root or under the fleet's `.ufo/`; the copy-in table is
   empty.** `git status --porcelain` (no pathspec) and `--untracked-files=all` are both empty at the fleet root and
   under `.ufo/` (23:20, 23:22, 23:29 -0300); the lane's own `tools/mori-misroot-sweep.py --fleet-root … --lane mori
   --round 53` returns `MORI_MISROOT_CLEAN`, `candidate_count: 0`, `untracked_entries: 0`. The only r53 markers
   outside the lane are the dispatcher's own log `.ufo/state/inline-dispatcher.log` (out of scope) and the tracked
   fleet prompt `.ufo/prompts/mori-round-53.md` (in place, not a stray). No `cmp` command is owed.
4. **INFO — the two named lane-root oddities are earlier-round seat misroots, already catalogued and relocated.**
   `0` (31 B, sha256 `b24122a0…`, content `NF=13 cells=11 double_quotes=0`) is tracked and byte-identical to
   `HEAD:0` (`cmp` exit 0); it entered the lane at `96f7f97e` (round-38 "misroot relocations (0, m9)") and is
   documented at `corpus/lessons/round-38.md:48` (M17) — a round-38 wave-1 seat's probe output, relocated byte-exact,
   not round 53's. `--repo` is an **empty directory** (0 entries), porcelain-invisible, mtime 2026-10-24 01:27, created
   in the round-39-wave-close (01:23:54) → round-40-instrument (01:31:20) window from a `--repo` literal-path
   accident; catalogued at `.ufo/waves/round-50/a2w1/Mo50bExecMisrootSweep.md:143` and
   `.ufo/waves/round-52/w1/Mo52ExecMisrootSweep.md:116`. No bytes, nothing to `cmp`, nothing to copy; the L1 may
   `rmdir` it. Neither is r53's.
5. **INFO — the fleet root's empty `ok/` directory is a round-47 artifact, still there, still empty.** Birth
   2026-10-25 16:43:05.478289356 — the identical nanosecond as the lane's (now removed)
   `.scratch/r47-ScribeQuality/2echo/` sibling recorded at `.ufo/waves/round-47/w2/ScoutMisroot.md:157-169`; 0
   entries; invisible to porcelain. Not r53's; no bytes; left alone (as rounds 50 and 52 did). The general limit
   stands: a porcelain-only misroot count under-reports, and the measured count is `find -type d -empty`.
6. **LOW — the frozen bytes are intact.** `sha256sum -c .ufo/waves/round-53/evidence/freeze-sha256.txt` in the lane
   reports 32/32 `OK` and no mismatch, after the wave's data corrections — no frozen file was edited in place.
7. **LOW — a lane-root write hazard for any seat using `git archive -o <relative-name>` under `git -C <lane>`.**
   Proved in §5.3: the output lands in the **repository root**, not the cwd, so a seat running from its scratch
   directory silently deposits the archive in the lane. The C2 counter is immune (`count-c2.py:409` pipes stdout to
   `tar -x -C <scratch>`); the exposure is the `-o` form, which is what produced finding 1. (I hit it twice myself
   and removed both files.) Suggestion for the round-54 prompt, not a change to any frozen instrument: name the
   archive output path absolutely, under the seat's scratch.
8. **INFO — my own footprint, disclosed.** Two files I created inside the lane root during the investigation
   (`head2.tar` at 23:20:57, `mech-test.tar` at 23:25) were removed immediately (`rm` exit 0 each); the lane's
   untracked set outside `.ufo/waves/round-53/` is `r53-data.tar` alone. My scratch
   `/fast/scratch/hyaku/mori-r53/Mo53ExecMisrootSweep/` was removed at finish. No `git add/commit/stash/checkout/
   reset/pull/push` in the lane or the fleet root, no mutating `jj`, no pacman, no tool installed, no host setting
   read or written.

Report: .ufo/waves/round-53/w1/Mo53ExecMisrootSweep.md
