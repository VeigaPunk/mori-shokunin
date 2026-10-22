# ScoutMisroot — round-24 wave-2 falsify: write scope and /tmp misroots

Seat `MoriR24.ScoutMisroot`. Read-only: no clone made, no lane or fleet file changed, no git
add/commit/checkout/reset/stash, no jj command, no service touched, no tool installed.
Snapshot time 2026-10-22 06:01–06:08 -03. Lane tip context `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`.

## 1. Fleet-root git status (the requested command)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` returned exactly:

```
 A .scratch/goal-20261022-hyaku-12h.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 A .ufo/state/kotoba.report-baseline
 A .ufo/state/kotodama.report-baseline
 M .ufo/state/mori.report-baseline
 A .ufo/state/revenger.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 A scripts/hyaku/__pycache__/append-closure.cpython-314.pyc
 A write
```

- **No `??` untracked file exists at the fleet root.** `git ls-files --others --exclude-standard`
  is empty. The six new files are *intent-to-add* index entries (` A`, zero-blob `e69de29…`
  confirmed by `git ls-files -s`), not porcelain-untracked. Per-file facts (`stat` + content reads):
  - `.scratch/goal-20261022-hyaku-12h.md` — 17367 B, 2026-10-22 04:54:00. **Names mori round 24**:
    line 86 `mori r24` (retry list) and line 102 `| B4 | mori (r24) | Fleet and host observability …`.
    This is the only new fleet-root file whose content names mori round 24.
  - `write` — 25 B, 2026-10-21 19:52:50. Content is the single line `agent://U100N079H334f935b`.
    `history://U100N079H334f935b` answers `Unknown agent`, so this is a stale/unknown id, not a
    mori round-24 seat. It is a **misrooted `write` call** (content only, no destination path),
    same failure mode as section 2. It does not name mori round 24.
  - `.ufo/state/kotoba.report-baseline` — 68 B, content `48 e3b0c442…b855` (empty-blob sha256);
    `.ufo/state/kotodama.report-baseline` — 68 B, `51 e3b0c442…b855`;
    `.ufo/state/revenger.report-baseline` — 68 B, `62 e3b0c442…b855`. No mori round-24 mention.
    (Modified `mori.report-baseline` reads `24 e3b0c442…b855`.)
  - `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` — 10738 B; `strings -a` shows only
    append-closure error/format strings, **no** `mori` token.

## 2. Pre-existing misroot directories at the fleet root (ignored, not touched)

`git status --ignored=matching` plus `du`/`find` surfaced three path-shaped misroots:

| path | type | size | created | content |
|---|---|---|---|---|
| `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory` | directory tree + one file | 12 K | 2026-10-18 14:01 | a 10139 B JSON (souji seat S54, round 4) stored under a path literally built from a shell command and error text; 0 matches for mori/round 24 |
| `mori-shokukin/` | empty dir tree `.ufo/waves/round-21/build/` | 0 B | 2026-10-21 09:53 | mori-adjacent typo of `mori-shokunin`, round 21 — **not round 24** |
| `tameshi-shokukin/` | empty dir tree (incl. `.ufo/waves/round-18/w1`, nested `tameshi-shokunin/.ufo/waves/round-19`) | 0 B | 2026-10-20/21 | typo tree, not mori |

All three are hidden by `.gitignore:1` (`*-shokunin/`), so they never appear in `git status`.
They predate this wave; they show the "argument string became a path" failure already recurs in
the fleet root.

## 3. /tmp inventory — items pointing at mori round 24 seats

Method: `ls -la /tmp`, name filter, then `du -sh`/`find` for sizes; plus a text scan
`find /tmp -maxdepth 1 -type f | xargs grep -Iil -m1 -E 'mori|round-24|r24'` (58 files matched),
with each hit opened to classify it. Sizes below are `du -sh` (dirs) and `stat` bytes (files).

### 3.1 Directories named for mori round 24 (all mtimes 05:14–05:36, inside the wave-1 window)

| path | size | what it holds |
|---|---|---|
| `/tmp/cib` | 272 K | kernel pressure sources: `psi.c` 48859, `psi.rst` 6792, `kernel_sched_sched.h` 117341, `arch_x86_kernel_tsc.c` 41716, `kernel_sched_cputime.c` 33065, `kernel_sched_clock.c` 13155, `measure.py` 1471 |
| `/tmp/mori-psi-probe.Ijpo9J` | 8.0 K | `mktemp -d` probe: `nofull` 48, `ws` 102, `errdir/`, three 0-byte stderr files |
| `/tmp/mori-psi-rst` | 100 K | `psi.rst` 6792, `master-psi.rst` 6792, `psi-second.rst` 6792, `psi.c` 48859, `psi-docs.html` 19726, `psi-docs.txt` 7956 |
| `/tmp/mori-r24-draft` | 536 K | kernel headers/sources for the knowledge entry: `psi.c` 48859, `psi.rst` 6792, `include_linux_sched.h` 73653, `kernel_cgroup_cgroup.c` 202860, `include_linux_irq.h` 44325, `interrupt.h` 27921, `kernel_time_ntp.c` 32946, `kernel_time_time.c` 27270, `fs_proc_interrupts.c` 859, plus 6 more |
| `/tmp/mori-r24-src` | 23 M | `kernel-parameters.txt` 317993, `man5_index.html` 274644, `gh_man5_tree.html` 199097, `proc.5.html` 31125, `man-pages-6.20.tar.xz` 1914692 and extracted `man-pages-6.20/` tree, `headers_404.txt` 161, `body_404.html` 196, `psi_v72.rst` 6792 |
| `/tmp/mori-src-kconfig` | 124 K | `Kconfig.v72` 74156, `psi.c.v72` 48859 |
| `/tmp/mori-srcpsic-dup` | 2.1 M | fixture tree `mori-shokunin/{SKILL.md 68320, corpus/QUALITY.md 32331, README.md 47015, SOURCES.md 66402, knowledge/, lessons/, evidence/}` |
| `/tmp/mori-srcpsic-final` | 2.1 M | same shape, `SOURCES.md` 67099 |
| `/tmp/mori-srcpsic-full` | 8.3 M | four variants `queued/`, `placeholder/`, `mined-noexist/`, `mined-withlesson/`, each a `mori-shokunin/` fixture with `SKILL.md` 68320 |
| `/tmp/mori-srcpsic-test` | 272 K | four empty fixture trees `a-queued`, `b-placeholder`, `c-mined`, `d-mined2` |

No `.git` or `.jj` exists inside `mori-srcpsic-*`; they are copied fixture trees, not clones.

### 3.2 Files named for mori round 24

| path | size | mtime | content |
|---|---|---|---|
| `/tmp/psi.c` | 48859 | 05:14 | kernel PSI source |
| `/tmp/psi.rst` | 6792 | 05:14 | kernel PSI docs |
| `/tmp/cso-mori.txt` | 0 | 05:45 | empty |
| `/tmp/cso-us-mori.txt` | 41369 | 05:46 | `update-safety` grep dump over mori-shokunin; includes `.ufo/waves/round-24/w1/SrcPsiRst.md:379` |
| `/tmp/e-m24.txt` | 0 | 05:39 | empty expected-output file |
| `/tmp/e-r24.txt` | 0 | 05:39 | empty expected-output file |
| `/tmp/o-m24.json` | 2942 | 05:39 | routed-check JSON: `repo=/home/vgpnk/Projects/shokunin/mori-shokunin`, `round=24`, `rev=master@06a7686e`, `held=4`, `items=4` |
| `/tmp/o-r24.json` | 2342 | 05:39 | same repo, `round=24`, `rev=c725aa37`, `held=3`, `items=4` |
| `/tmp/freeze-cases-check.py` | 10409 | 05:20 | "Independent re-derivation check for the frozen mori-pressure cases fixture … not the tool under test and is not committed." |
| `/tmp/x.txt` | 68320 | 05:35 | mori `SKILL.md` dump (`name: mori-shokunin`); no `Round24`/`r24` marker found |
| `/tmp/scorecard_c725aa37.md` | 114627 | 05:15 | `# mori-shokunin — Scorecard`, named for red commit `c725aa37` |

### 3.3 Files whose content (not name) points at the mori lane / C1 routed check

All are `tools/mori-routed-check.py` output JSONs or copies of the mori tool and name the mori
repo. `round`/`held`/`rev` extracted with `grep -o`:

| path | size | round | held | rev |
|---|---|---|---|---|
| `/tmp/o.json` | 6424 | 23 | 3 | c725aa37 |
| `/tmp/o-23-c725aa37…json` | 6424 | 23 | 3 | c725aa37 |
| `/tmp/o-r23.json` | 6702 | 23 | 3 | c725aa37 |
| `/tmp/r23-full.json` | 6799 | 23 | 3 | c725aa37 |
| `/tmp/final-a.json` | 6799 | 23 | 3 | c725aa37 |
| `/tmp/final-b.json` | 2342 | 24 | 3 | c725aa37 |
| `/tmp/final-c.json` | 2942 | 24 | 4 | 06a7686e |
| `/tmp/final-d.json` | 2365 | 24 | 3 | 29c1bf45 |
| `/tmp/committed-run.json` | 2942 | 24 | 4 | 06a7686e |
| `/tmp/rc-c725aa37…json` | 1747 | – | 3 | c725aa37 |
| `/tmp/rc-29c1bf45…json` | 1770 | – | 3 | 29c1bf45 |
| `/tmp/rc-head.json` | 2035 | – | 4 | f299bd79 |
| `/tmp/committed-tool.py` | 26834 | – | – | content names `tools/mori-dispatch-ledger.py` bytes |
| `/tmp/pristine-routed.py` | 26834 | – | – | same derivation |

Observation for the C1 seats, not a verdict: these round-24 artifacts show `held=4` only at
`06a7686e` (master at 05:39–05:45), not at the declared measured tip `a730ecf`. `06a7686e` is an
ancestor of `a730ecf` (`git merge-base --is-ancestor` → exit 0).

### 3.4 /tmp churn and excluded hits

- **Vanished mid-check:** `/tmp/mori-silence-cases.jubYng` (dir, mode 700, 9 links, mtime 06:00)
  appeared in the first `ls -la /tmp`; `du -sh` and `find` at 06:01 returned
  `No such file or directory`. A live seat created and removed mori-named scratch during this
  check.
- Excluded after content read (other lanes or incidental text): `/tmp/skill.base` (tsukuroi
  SKILL.md), `/tmp/LOG.md.bak` (kotoba log), `/tmp/m.py` (tsukuroi promisor mutants), `/tmp/st2.json`,
  `/tmp/st3.json`, `/tmp/st4.json`, `/tmp/neg.json`, `/tmp/integ-pass2.json`, `/tmp/integ-pass3.json`,
  `/tmp/pg-real.json`, `/tmp/pause.real`, `/tmp/final-selftest.json`,
  `/tmp/r25-expred-*` (tsukuroi pause-gate r24),
  `/tmp/codex-*`, `/tmp/oc-npm.json`, `/tmp/sudo_all.txt`, `/tmp/sudo_day.txt`,
  `/tmp/noharmmonitor-r25-*.json`, `/tmp/renoharm-mon-*.json`, `/tmp/r21-*.json`,
  `/tmp/kama-r25-*.cpp`, `/tmp/frk-*.json`, `/tmp/frk-targets.txt`, `/tmp/fleet_validate.out`
  (mori W04 row but no round-24 C1/C2), and `/tmp/c2*` scratch dirs (grep found no
  mori/pressure marker; they belong to other seats).

## 4. Write-scope findings

1. **/tmp is the evidence store for nine wave-1 reports.** The wave-1 spec places its working
   clones under `/fast/scratch/hyaku/mori-r24-a2/{wt-pressure,wt-cases,wt-routed,census-baseline}`
   (`wave1-spec.json:10,15,20,30`), but these reports cite /tmp paths:
   `SrcKconfig.md:23,28` (`/tmp/mori-src-kconfig`), `SrcKernelParams.md:22,174`
   (`/tmp/mori-r24-src/kernel-parameters.txt`), `SrcPsiC.md:203,395` (`/tmp/mori-srcpsic-full/`),
   `SrcPsiRst.md:27,32` (`/tmp/mori-psi-rst/psi.rst`), `SrcProcPressureMan.md:212,221`
   (`/tmp/mori-r24-src/`), `DraftKnowledgeEntry.md:25` (`/tmp/mori-r24-draft`),
   `CriticIntervalBoundary.md:11,32` (`/tmp/cib/`, `/tmp/cib/measure.py`),
   `FreezePressureCases.md:118` (`/tmp/freeze-cases-check.py`), `ScoutToolConventions.md:75,76`
   (`/tmp/_sptest.py`). One cited path is **already gone**: `/tmp/_sptest.py` is MISSING (checked
   with `[ -e ]`), so that report's evidence cannot be re-read.
2. **Shared fleet index was mutated.** Six new files are staged intent-to-add in
   `/home/vgpnk/Projects/shokunin/.git/index` (`git ls-files -s` → `e69de29bb2d1…` for all six).
   The effect is visible in every consumer's `git status`. Which actor ran `git add -N` is not
   recorded; I ran no index-mutating command.
3. **Lane worktree received an untracked pyc.** `tools/__pycache__/mori-dispatch-ledger.cpython-314.pyc`
   (34711 B, 2026-10-22 05:19) sits untracked in the lane repo — a wave-1 seat ran the tool in the
   lane worktree rather than a clone. `.scratch/` in the lane is untracked round-22 residue
   (last touched 2026-10-21 17:05), not round 24.
4. **Misroot family.** Fleet root `write` (section 1) and `bash: /…: No such file or directory`
   (section 2) share the same cause: a tool/command argument became a filesystem path. Both are
   stale (Oct 21 19:52 and Oct 18 14:01), but they are still executable-looking artifacts inside
   the fleet repo tree.

## 5. Verdict

- Killed: the assumption that the fleet root holds a porcelain-untracked file naming mori round 24 —
  there are no `??` entries at all.
- Confirmed: `.scratch/goal-20261022-hyaku-12h.md` is a new fleet-root file naming `mori r24`
  (lines 86, 102); `/tmp` holds a large wave-1 mori evidence store (≈37 MB across the dirs above)
  that the w1 reports cite directly; one cited path (`/tmp/_sptest.py`) is already lost; and the
  fleet root carries at least one `write` misroot plus three path-shaped misroot directories.
- Confidence: high on every listed file's existence/size/status (commands shown above); medium on
  attributing /tmp artifacts to individual wave-1 seats (timestamps and content align with the
  05:14–05:54 wave-1 window, but no per-seat marker exists).

## 6. Remaining unknowns

- Who ran `git add -N` for the six fleet-root entries, and whether the harness or a seat did it.
- Owner/intent of the deleted `/tmp/mori-silence-cases.jubYng`; /tmp is live, so this list is a
  snapshot and later seats may add or remove more.
- Whether any wave-2 report cites /tmp (I sampled wave-1 only; my own wave's binding forbids it).
- Nested files inside every /tmp directory were not exhaustively content-grepped: dirs were matched
  by name, and only the `c2*` dirs plus the listed ones were content-checked. No LSP was used —
  this task resolves filesystem/git artifacts, not code symbols.

## 7. Exact commands run (read-only)

```
git -C /home/vgpnk/Projects/shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin ls-files --others --exclude-standard
git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 -uall
git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 -uall --ignored=matching
git -C /home/vgpnk/Projects/shokunin ls-files -s -- write .scratch/goal-20261022-hyaku-12h.md …
git -C /home/vgpnk/Projects/shokunin ls-files --debug -- write .scratch/goal-20261022-hyaku-12h.md
git -C /home/vgpnk/Projects/shokunin check-ignore -v "bash: /home/vgpnk/Projects/shokunin/souji-shokunin/"
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --oneline -3 a730ecf…
git -C /home/vgpnk/Projects/shokunin/mori-shokunin merge-base --is-ancestor 06a7686e a730ecf
ls -la /tmp; find /tmp -maxdepth 1 -newermt '2026-10-22 05:00' ! -newermt '2026-10-22 06:40' -printf …
du -sh /tmp/cib /tmp/mori-psi-probe.Ijpo9J /tmp/mori-psi-rst /tmp/mori-r24-draft /tmp/mori-r24-src \
        /tmp/mori-src-kconfig /tmp/mori-srcpsic-{dup,final,full,test}
find /tmp/{cib,mori-psi-rst,mori-r24-draft,mori-src-kconfig,mori-srcpsic-*,…} -maxdepth N -printf …
find /tmp -maxdepth 1 -type f -print0 | xargs -0 grep -Iil -m1 -E 'mori|round-24|r24'
grep -o '"rev_commit":…|"round":…|"held":…|"items":…' /tmp/{o,o-r23,o-r24,o-m24,rc-*,final-*,…}.json
grep -rln '/tmp/' .ufo/waves/round-24/w1/   (lane repo)
strings -a scripts/hyaku/__pycache__/append-closure.cpython-314.pyc | grep -iE 'mori|r24|round'
```

No installs or upgrades were needed or performed.
