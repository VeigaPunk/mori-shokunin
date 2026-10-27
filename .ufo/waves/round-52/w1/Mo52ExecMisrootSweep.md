# Mo52ExecMisrootSweep — misroot pre-sweep (read-only), mori round 52 w1

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`; fleet root `/home/vgpnk/Projects/shokunin`.
Lane HEAD at every read: `075436b1346ca659afb8be7a46f0e67e4170aa83` (wave spec, after data `8524904a`); fleet HEAD
`685f7b36e66e172bbeba039d8fb6a22e78c655e8`. Read-only throughout: no `git add/commit/stash/checkout/reset/pull/push`,
no jj command, no `pacman`, no tool install, nothing written under the fleet root or the lane except this file.
Scratch `/fast/scratch/hyaku/mori-r52/Mo52ExecMisrootSweep/` (`mkdir -p`, two status snapshots kept there while
writing, removed at the end; every number below is copied into this file). `/fast` free at start: 603G on 804G
(`df -h /fast`). Nothing in `/home/vgpnk/Projects/shokunin/mori-shokunin` was created by any command I ran.

All observations are instants; the tree moves while w1 runs, so each block is stamped. I did not open
`.ufo/state/`, `.scratch/` file contents, `/home/vgpnk/Projects/shokuknow`, or any other lane's files.

## 1. Fleet root, `git status --porcelain` with no pathspec

```
$ date -Is; git -C /home/vgpnk/Projects/shokunin status --porcelain
2026-10-26T21:12:50-03:00
?? .ufo/reports/round-44/kengaku.md
rc=0   lines=1

$ git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 --untracked-files=all
?? .ufo/reports/round-44/kengaku.md        (identical: default status already enumerates files, not dirs)

$ date -Is; git -C … status --porcelain
2026-10-26T21:18:58-03:00
?? .ufo/reports/round-44/kengaku.md

$ date -Is; git -C … status --porcelain
2026-10-26T21:20:01-03:00
(empty; rc=0)
```

The single fleet-root untracked file at 21:12–21:19 was **not mori's**:

| path | evidence against mori ownership | round-52? |
|---|---|---|
| `.ufo/reports/round-44/kengaku.md` | `:1` `# kengaku — round 44 report (hyaku run 9, 2026-10-26)`; `:3` reads "Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`"; `grep -cE 'Mo52'` → `0`; 13,878 B, mtime `2026-10-26 21:05:52 -03` | no |

It is the kengaku lane's own round-44 report written at the fleet root at 21:05:52; by 21:20:01 it is gone (that
lane removed it). I did not read, move or copy it.

**`cmp` command set for mori round 52: empty.** There is no fleet-root file whose content names mori, round 52, Mo52
or this lane's paths, so there is nothing to relocate. The command I would have used for a candidate (template, kept
for the record — then `rm` the fleet copy only after `cmp` prints nothing):

```
cmp -- '/home/vgpnk/Projects/shokunin/<path>' \
        '/home/vgpnk/Projects/shokunin/mori-shokunin/<path>' && echo BYTE-EQUAL
```

## 2. Under `/home/vgpnk/Projects/shokunin/.ufo`

Untracked: only the kengaku file above (§1). Ignored / non-mori, name-listed only (no content read):

- `!! .ufo/state/aggregator.* … kengaku.* …` — driver state, off-limits by the task rule; not opened.
- `!! .ufo/watchdog.log` — orchestrator log.
- `!! .ufo/waves/shokunin-train-*/{xconnector,xsentinel}-scratch/` — other waves' per-seat scratch.
- `.ufo/waves/hyaku/misroots/` — three parked artifacts from rounds 15–16 (`MoriR16.Lesson` 847 B, `SoujiR15`,
  `TameshiR15`); historical, not round 52.

Files under `.ufo` (state excluded) modified after 19:00 today and naming `Mo52`/`round-52`
(`find .ufo -path .ufo/state -prune -o -type f -newermt '2026-10-26 19:00' -print0 | xargs -0 grep -l -m1 -E 'Mo52|round-52'`):
`.ufo/prompts/mori-round-52.md` (orchestrator dispatch prompt, tracked), `.ufo/prompts/chousa-round-52.md`,
`.ufo/prompts/closure/chousa-round-52.md`, `.ufo/reports/round-52/chousa.md` (chousa lane's own round-52 report),
`.ufo/reports/round-43/tsukuroi.md`. That last one is committed (`ff846a48`, 2026-10-26) and git-clean. None of
these is a mori seat write; `mori-round-52.md` is the fleet-side prompt the L1 was dispatched with, not a report.

Two fleet-root hygiene facts recorded, not owned by mori round 52:

- `tsukuroi.md:196` in that tracked report reads: "two fleet-root files `p.out`/`p.err`, which a chousa round-52 seat
  wrote. I did not touch them". At my 21:19 check `ls -la p.out p.err` → `No such file or directory` for both, rc=2,
  and the fleet porcelain is clean, so those two already-misrooted files are gone; nothing left to relocate.
- `/home/vgpnk/Projects/shokunin/ok` is an **empty directory** (0 entries, mtime `2026-10-25 16:43:05 -03`), tracked
  by nothing and therefore invisible to every porcelain-based sweep. It predates round 52 (wave started 19:50) and
  names nothing mori; I left it alone.

## 3. Lane `status --porcelain --ignored`, strays outside `.ufo/waves/round-52/`

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --ignored | wc -l
40      (21:12:50)          72      (21:22:14)
$ … status --porcelain --ignored | grep -c '^??'   → 61 ;  | grep -c '^!!'  → 11   (21:22:14)
$ … status --porcelain --ignored   (the 11 `!!` lines, 21:22:14)
!! .jj/            !! .ufo/waves/{44,45,47,48,49,50}/__pycache__/   (6 lines)
!! .ufo/waves/round-50/controls/__pycache__/   !! .ufo/waves/round-52{,/controls}/__pycache__/   !! tools/__pycache__/
$ … status --porcelain --ignored --untracked-files=all | wc -l → 10,393 (the `.jj` tree alone expands to
  10,308 `!! .jj/repo` lines; -uall is unusable as a signal, default porcelain is not)

$ git status --porcelain=v1 --untracked-files=all   (lines outside .ufo/waves/round-52/)
21:18:19  17 lines   21:19:22  31 lines   21:20:01  9 lines
21:20:01  ?? corpus/lessons/round-52.md            1
21:20:01  ?? .ufo/waves/round-39/scratch/…         8
21:12:50  (collapsed form) only `?? .ufo/waves/round-39/scratch/` and `?? corpus/lessons/round-52.md` outside round-52
```

At 21:12:50 and 21:22:14 no tracked file was modified (`git status --porcelain | grep -E '^ ?M|^M'` → no line). At
21:22:53 a sibling wrote **`corpus/README.md`** (`git diff --stat` → `1 file changed, 1 insertion(+), 1 deletion(-)`;
mtime `21:22:53.147`): line 728's pin was replaced by
"`bash .ufo/waves/round-52/r39-conform-selftest.sh 4f266ef2… --selftest`", and that wrapper exists
(`.ufo/waves/round-52/r39-conform-selftest.sh`, 1,441 B, `-rwxr-xr-x`, 21:22) and describes cloning the lane under
`$TMPDIR` and bind-mounting the clone over the hardcoded `LANE` with `bwrap`. That edit is not mine and I did not run
the wrapper (read-only seat); whether it prevents the lane writes is UNVERIFIED here — the lane scratch kept growing
after it appeared (3 dirs / 19 files / 456K at 21:22:36 → 4 dirs / 32 files / 768K at 21:23:29), so either old-form
runs were still in flight or the new pin is not the only caller.

The moving part is live, and its writers are the frozen instruments' own scratch parents:

| stray | measured | creator / evidence | round-52? |
|---|---|---|---|
| `.ufo/waves/round-39/scratch/mori-conform-selftest-*/counter-*.py` | live and growing: 2 dirs / 15 files / 360K at 21:20; 3 dirs / 19 files / 456K at 21:22:36; 4 dirs / 32 files / 768K at 21:23:29; each file 22.2–22.5 KB, mtimes 21:17:26–21:18:44 | `.ufo/waves/round-39/conform.py:54` `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")` and `:492` `mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` | yes — this round's runs of the README living pin / `count-c1.py` arm (C) |
| `.ufo/waves/round-38/scratch/` | 19 dirs, **18 empty** (porcelain-invisible); 6 empty dirs created today in pairs — `c1-hqleifox`+`19:49`, `c1-5qq4uc08`+`19:55`, `mori-c1-tool-241f_hrt`+`c1-u6dazxwm`+`21:14`, `mori-c1-tool-hqkwfldz`+`c1-2ppq8tkj`+`21:17` | `.ufo/waves/round-38/count-c1.py:992` `mkdtemp(prefix="mori-c1-tool-", dir=_scratch_parent())`, `:1029` `mkdtemp(prefix="c1-", …)`; `.ufo/waves/round-38/conform.py:37` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` | yes (pairs dated today) |
| one round-38 selftest work dir with 5 `counter-*.py` | present at 21:18:19, gone at 21:19:22 (`finally: shutil.rmtree`) | `.ufo/waves/round-38/conform.py:239` | yes |
| `.ufo/waves/round-40/scratch/` | 8 files, **all mtime 2026-10-26 09:07** (round-50/51 era); directory mtime bumped to `21:15:45` = a child added and removed [INFERENCE from the mtime alone] | `.ufo/waves/round-40/conform.py:73` `SCRATCH_ROOT = tempfile.gettempdir()` | no (older files); today's run left no file |
| `corpus/lessons/round-52.md` | untracked, 4,690 B, mtime `2026-10-26 21:12:15 -03`; `:2-8` name entering tip `4f266ef2`, freeze `d3a8ea59`, data `8524904a`, wave spec `075436b1`, `L1 MoriR52, attempt 1` | round-52's own draft | yes, in-lane (not a misroot) |
| `--repo` (lane root) | empty directory, mtime `2026-10-24 01:27`, 0 entries | already catalogued by `.ufo/waves/round-50/a2w1/Mo50bExecMisrootSweep.md:146` | no |
| `__pycache__/` (ignored) | `tools/`: 4 `mori-*.pyc` (source-drift 19:45 today); `.ufo/waves/round-52/`: `count-c2` 20:58, `build-w1-spec` 21:09, `count-c1` 21:11; `controls/`: `c1-data` 21:07 | importers named in the bytes (`build-w1-spec-amend.py:12`, `check-history-rows.py:38`) | pycache provenance is `Mo52ExecLocatorSweep`; cross-referenced, not re-attacked |
| `.scratch` | 225 files **tracked at HEAD** although `.scratch/` is in the lane `.gitignore`; 13 top-level entries, 11 dirs, 29M on disk; no new ignored entry at snapshot | tracked-before-ignore residue | no |

Two consequences worth naming:

1. The mitigation in this wave's rules — "run frozen round-38..49 instruments only from an archive or clone" — does
   **not** stop these writes: `LANE` is a hardcoded absolute constant in `round-38/conform.py:37`,
   `round-39/conform.py:53` (and `round-41`:66, `round-42`:73 per `Mo52ScribeScorecard.md:142,196`), so an archived
   copy still resolves its scratch parent inside the lane [INFERENCE from the constant plus the observed dirs].
   The remaining mitigation is a mutated copy or an instrument that takes the scratch parent as an argument; the
   counters are frozen, so this is a named limit for round 53.
2. The round-38 dirs that survive are **empty** and therefore absent from `git status`; a porcelain-only misroot
   count under-reports them. The measured count is `find -type d -empty`.

The live round-39 writes are already carried as a HIGH by `Mo52SentBoundary` (F1) and a LOW by `Mo52RevQualityRows`;
this seat's contribution is the round-38 empty-dir singleton (six dirs today), the round-40 transient, and the
before/after counts above, not a second attack.

`corpus/lessons/round-52.md` is round 52's own draft and belongs where it is; the L1 lands it. Cited, not judged:
its `:11` reads "One v2 wave `w1` (68 seats) ran after the data commit, as the contract froze" while the wave was
still running at 21:21 (`ls .ufo/waves/round-52/w1/*.md | wc -l` → 53), which is a scribe/quality question, not
this seat's.

## 4. Lane-root tracked strays — provenance and verdict

`git ls-tree HEAD --name-only -- 0 MANPAGE.md base.c main.c meminfo.c oom_kill.c sd-main.c 'user@.service.in'` lists
**eight** (the seat's list of seven omits `MANPAGE.md`, which is the seventh of the round-28 seven). Each file:

| file | size | sha256 | added by | verdict |
|---|---|---|---|---|
| `0` | 31 | `b24122a0f0245c0a…` | `96f7f97e` round-38 "… misroot relocations (0, m9)" | seat misroot (round 38 w1), relocated |
| `MANPAGE.md` | 10,114 | `cc48b02e79255ae2…` | `763d3469` round-28 "… misroot sweep of seven r27 fetches with hash check" | seat misroot (round 27), relocated |
| `base.c` | 98,196 | `cef1a2cf3f34f683…` | `763d3469` | seat misroot (round 27), relocated |
| `main.c` | 21,053 | `08656b0bc90c85f2…` | `763d3469` | seat misroot (round 27), relocated |
| `meminfo.c` | 8,344 | `526e512c89c58cb0…` | `763d3469` | seat misroot (round 27), relocated |
| `oom_kill.c` | 34,311 | `452f1348e79c252e…` | `763d3469` | seat misroot (round 27), relocated |
| `sd-main.c` | 180,617 | `5ecdca43a8e0ed08…` | `763d3469` | seat misroot (round 27), relocated |
| `user@.service.in` | 1,315 | `72c2f40dcfced1d8…` | `763d3469` | seat misroot (round 27), relocated |

Commands: `git log --format='%h %ad %s' --date=short --diff-filter=A -- <file>` per file (all seven at `763d3469`,
`0` at `96f7f97e`); `git show --name-only --format='' 763d3469` lists `MANPAGE.md`, `base.c`, `main.c`, `meminfo.c`,
`oom_kill.c`, `sd-main.c`, `user@.service.in` among its 16 changed paths (and `git show --name-status --format='%h %s'`
prints `A MANPAGE.md`); `sha256sum` per file.

**Yes, they are seat misroots** — of rounds 27 and 38, not of round 52:

- `.ufo/waves/round-28/evidence/misroot-before.txt` lists all seven as untracked **fleet-root** files at rev
  `6ebd518f` (`misroot base.c sha=cef1a2cf3f34f683 cited-by=.ufo/waves/round-27/w1/CriticC1Novelty.md`, …,
  `misroot_hits=7 exit=1`); `.ufo/waves/round-28/w1/MisrootProvenance.md:30-37` maps each to its upstream URL and
  records the fetch sha256. My content hashes reproduce all seven 16-hex prefixes exactly, so **the committed lane
  bytes are the round-27 fleet copies, byte-exact** — a relocation, not a re-fetch.
- `corpus/lessons/round-28.md:31-34` (M2) and `.ufo/waves/round-28/w2/ReviewMisrootSweep.md` record the sweep and the
  placement; `.ufo/waves/round-28/w2/ReviewMisrootSweep.md:62` records `git diff 763d3469 f2de0ee -- <the seven>`
  empty.
- `0` is `corpus/lessons/round-38.md:48` (M17): a round-38 wave-1 seat's probe output (`NF=13 cells=11
  double_quotes=0`), copied "into the lane at the same relative path (`mori-shokunin/0`), `cmp`-verified".

Residue that is still true today, and why I did **not** propose deleting anything:

- the round-28 sweep's own criterion is "untracked at the fleet root" (`misroot-hash-check.sh` reads only `?? `
  porcelain entries), so moving a file into the lane root and committing it reads `misroot_hits=0` while creating a
  tracked lane-root stray — the blind spot survives in the lane;
- two of the eight are duplicates of held copies — `base.c` = `corpus/evidence/sources-r47/fs_proc_base.c` and
  `oom_kill.c` = `corpus/evidence/sources-r47/mm_oom_kill.c` = `corpus/evidence/sources-r50/oom_kill.c.v7.2`
  (sha256 equal, `cmp`-level identical) — but the earlyoom trio (`main.c`, `meminfo.c`, `MANPAGE.md`) and the systemd
  pair (`sd-main.c`, `user@.service.in`) have **no other committed copy** in the lane (`find corpus/evidence -type f
  \( -iname '*MANPAGE*' -o -iname '*main.c*' -o -iname '*meminfo*' -o -iname '*user@*' -o -iname '*base.c*' -o
  -iname '*oom_kill*' \)` → only the four r47/r50/r51 kernel files and the root copies), so deleting them would
  destroy the only lane-held bytes for rows S114/S115/S130;
- no tracked lane document names them at the lane root (`git grep -n -E 'mori-shokunin/(base|main|meminfo|oom_kill|
  sd-main)\.c|mori-shokunin/MANPAGE\.md'` → no line), i.e. nothing pins the current placement.

Routed, not executed (successor-freeze design, round-53 item; §5 item 6 forbids in-place edits): either relocate the
six round-27 bytes plus `0` to `corpus/evidence/sources-r28/` with a lesson line that records the second move, or add
the lane-root paths to a lane-level ledger so a future sweep stops re-listing them. Both need an L1 decision.

Wording defect observed while checking this (LOW): `.ufo/waves/round-28/w2/RetentionAtTip.md:44-46` says the root
files' "blobs differ from the round-27 fleet copies cited in `evidence/misroot-before.txt` (e.g. `main.c` tip blob
`780f8125` vs cited sha prefix `08656b0b`)". `780f8125` is the git blob id (`git rev-parse HEAD:main.c`), not a
sha256; the content sha256 is `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`, equal to the cited
prefix. The bytes do not differ.

## 5. Limits of this sweep

- Attribution of each live scratch dir to a *named* seat is UNVERIFIED: I did not sample `ps`/`lsof`, so the creators
  are named by instrument (`round-38/count-c1.py:992,1029`, `round-38/conform.py:239`, `round-39/conform.py:492`),
  which is proven, and by timing, which is [INFERENCE].
- The counts are taken at five instants (21:18:19, 21:19:22, 21:20:01 for the lane; 21:22:14 and 21:22:36 for the
  ignored counts and the round-39 re-measure); the round-39 scratch alone went 17→31→9 untracked lines within 102 s
  and then grew again to 3 dirs / 19 files. A file created and removed between samples is not in the record.
- Empty directories are invisible to every porcelain gate; my empty-dir scan is `find -type d -empty` at one instant.
- `.ufo/state/`, `.scratch/` contents, other lanes (`kengaku-shokunin`, `chousa-shokunin`, `tsukuroi-shokunin`, …) and
  `/home/vgpnk/Projects/shokuknow` were not read; the kengaku/p.out/p.err statements rest on the fleet porcelain
  plus the tracked `tsukuroi.md:196` sentence, not on those lanes' files.
- A misroot that is git-ignored at the fleet root is invisible to `git status` (the fleet `.gitignore` ignores
  `*-shokunin/`, `.ufo/state/*`, `.ufo/watchdog.log`, `.tower/`, `.ufo/waves/*/*-scratch/`); I checked names under
  `.ufo` and found none naming mori round 52 outside `state/`, but an ignored write under `.tower/` would not appear.
- The lane-root strays are frozen history; deciding where they belong is a freeze question, not a measurement.

## Findings

- **HIGH — live lane writes outside the round-52 tree, from a frozen pin.** `.ufo/waves/round-39/scratch/` gains
  `mori-conform-selftest-*/counter-*.py` (2 dirs / 15 files / 360K at 21:20, 3 dirs / 19 files / 456K at 21:22:36,
  4 dirs / 32 files / 768K at 21:23:29) whenever the README.md:728 pin runs
  `python3 .ufo/waves/round-39/conform.py <rev> --selftest`, including the L1's own `count-c1.py` arm (C); writer
  lines `.ufo/waves/round-39/conform.py:53,54,491,492`. Archive-based mitigation cannot help because `LANE` is a
  hardcoded absolute path. Same mechanism as `Mo52SentBoundary` F1; this seat confirms it from the misroot side. A
  sibling replaced that pin at 21:22:53 with a bwrap wrapper (`.ufo/waves/round-52/r39-conform-selftest.sh`) that
  bind-mounts a scratch clone over `LANE`; writes had not stopped at 21:23:29 and I did not run the wrapper, so its
  effect is UNVERIFIED (and the fix is data/wrapper, not a counter edit).
- **MED — empty-directory lane writes are invisible to the porcelain sweep.** `.ufo/waves/round-38/scratch/` holds 18
  empty dirs of 19, six created today in pairs (`mori-c1-tool-*` + `c1-*` at 19:49, 19:55, 21:14, 21:17) by
  `.ufo/waves/round-38/count-c1.py:992,1029`; `git status --porcelain` cannot see any of them. Any round-end misroot
  count that uses porcelain alone under-reports.
- **MED — eight tracked lane-root strays, five of them the only committed copy of their bytes.** `0`, `MANPAGE.md`,
  `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in` (lane root; `763d3469` and
  `96f7f97e`). They are byte-exact round-27/round-38 seat misroots relocated by L1 sweeps whose criterion
  (untracked-at-fleet-root) cannot see the new path. Deleting the earlyoom trio or the systemd pair would lose the
  only lane copy; route a successor-freeze relocation, never an in-place move under §5 item 6.
- **LOW — the seat's own file list was incomplete.** The dispatch text names seven lane-root strays; `MANPAGE.md` is
  the eighth and was added by the same `763d3469` commit (round-28 receipt `misroot-before.txt` lists seven files,
  `MANPAGE.md` among them).
- **LOW — `.ufo/waves/round-40/scratch/` carries a transient write with no receipt.** Directory mtime `21:15:45`
  today on a dir whose 8 files are all `09:07`, i.e. a child created and removed during w1 while no round-52 report
  records a round-40 run; the parent is `tempfile.gettempdir()` (`round-40/conform.py:73`), so the transient is in
  the lane's own dir, not `/fast`.
- **LOW — `corpus/lessons/round-52.md` (untracked, 4,690 B, 21:12:15) states the wave "ran" while it is running.**
  In-lane draft, no misroot; cited for the scribe.
- **LOW — `.scratch/` holds 225 files tracked at HEAD although `.scratch/` is in the lane `.gitignore`** (13
  top-level entries, 11 dirs, 29M). A tracked-ignored overlap defeats both "ignored means transient" and
  "status counts the tree" assumptions used by the lane's disk and misroot accounting.
- **LOW — `.ufo/waves/round-28/w2/RetentionAtTip.md:44-46` compares a git blob id with a sha256 prefix** and concludes
  the root copies differ from the cited fleet copies; the content sha256 equals the cited prefix for all seven.
- **INFO — fleet root clean at 21:20:01 and again at 21:22:53** (`git -C /home/vgpnk/Projects/shokunin status
  --porcelain` → empty, 0 lines), the only two empty readings of the sweep. The only untracked file in the window was
  another lane's round-44 report (`kengaku.md`, removed by 21:20:01), and the two files `tsukuroi.md:196` attributes
  to a chousa round-52 seat (`p.out`, `p.err`) are already absent. No mori round-52 misroot exists at the fleet root
  or under `/home/vgpnk/Projects/shokunin/.ufo`, so the `cmp` relocation set is empty.
