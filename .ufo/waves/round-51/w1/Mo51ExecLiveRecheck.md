# Mo51ExecLiveRecheck — live recheck of the five C2 sources + fleet census validate

Seat: `Mo51ExecLiveRecheck` (executor, leaf; no subagents — none dispatched, no labrat used).
Lane: `mori-shokunin`. Round 51, wave `w1`. Item: replay the entry's `recheck:` command, compare the five live
sha256 against the committed copies under `corpus/evidence/sources-r51/` and the `COPIES` table in
`.ufo/waves/round-51/count-c2.py`; then run `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`,
report rc, the W04 lines, and whether S492 is W04 rather than E04.

Data under test: `87e0c374537557754bf71dd68036ded3ddc6699c` (lane HEAD at run time `b504cb1701568a0038aab9d98ec13d28eff801da`).
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck/` with `TMPDIR` inside it; removed at the end and
`ls` re-run to confirm absence (see §Scratch). Nothing outside this report was written; no git/jj mutation ran
(only `rev-parse`, `show`, `diff --stat` — read-only).

## 1. The `recheck:` line replayed verbatim

The entry line (`corpus/knowledge/memavailable-estimate-r51.md:9`, read raw):

```
recheck: on-release — `for u in https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch; do curl -fsSL "$u" | sha256sum; done` -> e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126, dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5, d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda, 2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6, 9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0 in that order (ran 2026-10-26; all five matched the committed copies under `corpus/evidence/sources-r51/`)
```

Executed (command text is the backticked loop, unchanged; `TMPDIR` exported into scratch, cwd = scratch):

```
$ cd /fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck && export TMPDIR=$PWD/tmp
$ for u in https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst \
      https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c \
      https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c \
      https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h \
      https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch
  do curl -fsSL "$u" | sha256sum; done
e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126  -
dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5  -
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  -
2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6  -
9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0  -
recheck_rc=0
```

The five live digests equal the five digests recorded in the entry, in the entry's order. No 429, no timeout,
no partial stream: `curl -f` fails (rc 22) on any 4xx/5xx, the loop printed five digests and the pipeline exit
was 0. To make the absence of a 429 explicit rather than inferred, the status codes were also read once:

```
$ for u in <same five>; do printf '%s ' "$(curl -fsSL -o /dev/null -w '%{http_code}' "$u")"; echo "$u"; done
200 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst
200 https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c
200 https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c
200 https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h
200 https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch
```

No retry was needed, so the single permitted retry was not spent.

## 2. Live vs committed copies vs `COPIES` in `count-c2.py` (four-way)

`COPIES` is `dict` of `SRC_DIR + "<file>" -> sha256` at `.ufo/waves/round-51/count-c2.py:46-57`, with
`SRC_DIR = "corpus/evidence/sources-r51/"` (line 36). The counter's pin arm reads those paths with
`git show <rev>:<path>` (`git_reader`, lines 251-256; used at lines 149-153), i.e. from the committed tree at R,
not the working tree. Four independent readings were compared:

1. live upstream bytes (curl, §1);
2. working-tree bytes of `corpus/evidence/sources-r51/` (`sha256sum`);
3. the same five blobs as committed at the data revision (`git show 87e0c37:<path> | sha256sum`);
4. the constants in `COPIES`.

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/*
9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0  .../34e431b0.patch
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  .../meminfo.c.v7.2
2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6  .../mm_inline.h.v7.2
e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126  .../proc.rst.v7.2
dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5  .../show_mem.c.v7.2

$ for f in proc.rst.v7.2 show_mem.c.v7.2 meminfo.c.v7.2 mm_inline.h.v7.2 34e431b0.patch; do
    git -C $LANE show 87e0c37:corpus/evidence/sources-r51/$f | sha256sum; done
e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126  -
dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5  -
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  -
2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6  -
9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0  -
```

`COPIES` as parsed from the counter source (five tuples, regex on `\(SRC_DIR \+ "([^"]+)",\s*"([0-9a-f]{64})"`):

```
proc.rst.v7.2     e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126
show_mem.c.v7.2   dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5
meminfo.c.v7.2    d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda
mm_inline.h.v7.2  2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6
34e431b0.patch    9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0
```

Joined result (script output, exit 0):

```
proc.rst.v7.2      live=e760f716f8278dee committed=e760f716f8278dee COPIES=e760f716f8278dee match=yes
show_mem.c.v7.2    live=dba76b263bbdf933 committed=dba76b263bbdf933 COPIES=dba76b263bbdf933 match=yes
meminfo.c.v7.2     live=d6c5807421a69eac committed=d6c5807421a69eac COPIES=d6c5807421a69eac match=yes
mm_inline.h.v7.2   live=2d4accbbc1ec139b committed=2d4accbbc1ec139b COPIES=2d4accbbc1ec139b match=yes
34e431b0.patch     live=9f571a04fc365858 committed=9f571a04fc365858 COPIES=9f571a04fc365858 match=yes
ALL_FIVE_MATCH= yes
```

`match=yes` on all five means live == working-tree copy == blob at R == `COPIES` constant for every source; there
is no drift between the recorded expectations and what upstream serves today.

## 3. The C2 files are unchanged from the data commit to HEAD

The validate run in §4 reads the working tree, not revision R, so the working tree's identity with R was checked
first (`git diff --stat` printing nothing = identical; exit 0):

```
$ git -C $LANE rev-parse HEAD
b504cb1701568a0038aab9d98ec13d28eff801da
$ git -C $LANE diff --stat 87e0c37 -- corpus/SOURCES.md corpus/knowledge/memavailable-estimate-r51.md \
      corpus/evidence/sources-r51 .ufo/waves/round-51/count-c2.py .ufo/waves/round-51/contract.md
(no output)  diff_rc=0
$ git -C $LANE diff --stat 87e0c37 HEAD -- corpus/SOURCES.md corpus/evidence/sources-r51 \
      corpus/knowledge/memavailable-estimate-r51.md
(no output)  head_diff_rc=0
```

So the census result below is a statement about the landed bytes, not about some later edit.

## 4. Fleet census validate, lane `mori`

```
$ export TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck/tmp
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

(stderr empty.) Line accounting over that stdout: 24 lines total = 23 `W04` + 1 `ok`; `grep -cE '\tE[0-9]{2}\t'`
= 0 E-codes; warning codes other than W04 = 0. `rc=0` is the script's "clean or warnings" exit
(`scripts/sources-census.sh:17-19`).

### Is S492 W04 and not E04?

Yes — W04, and the classification is the correct one by the script's own definitions
(`scripts/sources-census.sh:29-31`: `E04 duplicate URL+scope (no supersedes)`, `W04 same URL across scopes`).
S492's own scope field differs from the scope of every earlier row that shares its URL:

```
$ awk -F'|' '/^\| S492 /{...}' corpus/SOURCES.md
NF=13
[2] Linux Documentation/filesystems/proc.rst at tag v7.2, meminfo fields — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst
[3] docs   [4] A
[5] the /proc/meminfo field definitions at v7.2 (MemFree, MemAvailable, Cached, Shmem, KReclaimable, SReclaimable); same URL and bytes as S082 (mountinfo layout) with a different scope; S168 was the rej…
[6] proc.rst:1124-1135 (MemFree, MemAvailable), 1138-1141 (Cached), 1192-1201 (Shmem, KReclaimable, SReclaimable); tag v7.2; copy corpus/evidence/sources-r51/proc.rst.v7.2 sha256 e760f716…
[7] MemAvailable is documented as an estimate for starting applications without swapping, and Cached includes tmpfs and shmem.
[8] mined  [9] 2026-10-26  [10] on-release  [11] corpus/knowledge/memavailable-estimate-r51.md
```

- S082 (`corpus/SOURCES.md:88`) holds scope `textual mountinfo field layout only`, section `1965-2002` — the same
  URL and the same sha256 prefix (`e760f716f8278dee`) over a different part of the file. Different scope, so the
  pair is a W04, not an E04.
- S168 (`:172`) was the round-31 *same-scope* duplicate of S082 and is `rejected`; S492's scope text names that
  history explicitly, which is why the new row is not seeded as a second same-scope row.
- Row shape is valid: `NF=13`, id `S492` matches `S[0-9]{3,}`, kind `docs` and tier `A` are in the enums, status
  `mined`, `opened 2026-10-26` (today, not future), recheck `on-release` is a symbolic cadence (E09 allows it),
  used-by `corpus/knowledge/memavailable-estimate-r51.md` exists on disk (else E11), used-by is not `—` (else W03).
  None of E01-E12 fired for it.

Round-start receipt `evidence/census-start.txt` holds 22 W04 lines + `ok`, rc 0; this run holds 23, the extra one
being S492. The delta is exactly the new row and nothing else — the other 22 ids are the same ids this run reports.

## 5. Observations within this item's scope (named, not re-scored)

- The `recheck:` line records byte digests only. A digest proves the copy is what upstream served on the fetch
  date; it cannot prove the v7.2 tag will never be re-pointed or that a later fetch will not 404. The entry's
  cadence is `on-release`, so the check re-runs then.
- The entry line's five expectations are order-dependent prose; a reader who reorders the URLs silently mismatches.
  The command as written and the expectation list as written agree today (§1), so this is a readability limit.
- `COPIES` pin verification reads blobs at R through `git show` (`count-c2.py:149-153`), so `pins=ok` is a claim
  about the committed tree; the working tree is only used by the `--selftest` path (`count-c2.py:305-310`, which
  resolves the lane from `__file__`). Both agree here (§2, §3).
- `sources-census.sh validate` reads the working tree; §3 shows the working tree equals R for every C2 file, so
  the rc 0 above applies to the landed data.

## 6. Scratch lifecycle and hygiene

```
$ S=/fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck; mkdir -p "$S/tmp"; export TMPDIR="$S/tmp"   # before every run
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status ; echo rc=$?
root                             use%     free
/tmp                               3%   124.1G
/var/tmp                          35%   584.9G
/fast/scratch/hyaku               25%   602.8G
... (top consumers truncated; no ENOSPC condition)  rc=0
$ rm -rf -- /fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck
$ ls -d /fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck
ls: cannot access '/fast/scratch/hyaku/mori-r51/Mo51ExecLiveRecheck': No such file or directory
```

No clone, no work tree, no fixture repo; only `curl` pipes and two small local files (`cmp.py`, `validate-mori.txt`)
inside that scratch. No tool install or upgrade was needed (no pacman, no uv/npx). No kernel-log text was read, no
`/proc` pressure file was read, no limit or sysctl touched. Nothing under `~/.local/bin`, the fleet root, or the
lane's tracked files was written except this report.

## Findings

- **LOW — census W04 count rises 22 → 23; S492 is W04, correctly not E04** (`corpus/SOURCES.md:271`, against
  `corpus/evidence/census-start.txt` which records 22 W04 + `ok`). Anyone diffing round-end against round-start
  census must expect the extra line and must not read it as a new defect; the reason (same URL as S082 over a
  different, meminfo scope) is documented inside the row itself. `validate` rc 0, 0 E-codes.
- **LOW — the recheck expectation list is order-dependent prose** (`corpus/knowledge/memavailable-estimate-r51.md:9`).
  Today's replay reproduces it exactly in order, but a future re-reader has no machine anchor tying URL order to
  digest order; a reordered list would look like a mismatch rather than a reordering.
- **LOW — the recheck proves bytes, not tag immutability** (same line). A byte digest on a date says what upstream
  served that day; the `on-release` cadence is the only thing that re-tests it, and a re-pointed tag would be
  visible only as a changed digest, indistinguishable at a glance from a legitimate upstream edit.
- **INFO — no 429/timeout encountered**: all five fetches returned HTTP 200 and `recheck_rc=0`; the single
  permitted retry was not used, so this run says nothing about upstream rate-limit behavior under load.
