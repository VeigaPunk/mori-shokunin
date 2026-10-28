# Mo60Executor59 — round-60 scratch/disk hygiene receipt

Seat: executor (hygiene receipt item). Mode: read-only — no commits, no VCS mutation, no
fleet/sibling writes, no production-file edits. Lane tip read at
`b3c256138f00c704d5aa56eb0332d74506502ef2` (`round-60: move S561-S564 rows into the Registry
table (census E12 fix)`, 2026-10-28 12:58:36 -0300).

Scratch used: `/fast/scratch/hyaku/mori-r60/Mo60Executor59/` (TMPDIR set there); cleaned before
yield. All timestamps UTC.

## Deliverable 1 — disk-guard status (exit 0 = green)

Command:

```
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
```

Output (verbatim, head — guard scratch consumers only):

```
root                             use%     free
/tmp                              14%   110.6G
/var/tmp                          38%   557.1G
/fast/scratch/hyaku               26%   596.6G
```

`status` exit code: **0**. Contract for `status` is "exit code as `check`"
(`scripts/hyaku/disk-guard.sh:11-12`).

Exit-code form, run twice (start and end of this seat):

```
$ disk-guard.sh check
ok root=/tmp use=14% soft=70%
ok root=/var/tmp use=38% soft=70%
ok root=/fast/scratch/hyaku use=26% soft=70%
check_exit=0
```

Thresholds in force (`disk-guard.sh:111-116`): roots `/tmp /var/tmp /fast/scratch/hyaku`;
`SOFT_PCT=70`, `TARGET_PCT=60`, `HARD_PCT=90`, `IDLE_MIN=45`, `MIN_AGE_MIN=10`.

`df` cross-check at 16:16:01Z:

| mount | size | used | avail | use% |
|---|---|---|---|---|
| `/tmp` (`/dev/nvme1n1p1`) | 128G | 17G | 112G | 14% |
| `/` (`/dev/mapper/root`) | 930G | 337G | 558G | 38% |
| `/fast` (`/dev/nvme1n1p2`) | 804G | 208G | 596G | 26% |

Verdict: **green**. `/fast/scratch/hyaku` carries 356 GB of headroom to the 70% soft line
(563 GB used-equivalent); 596 GB absolute free. No pressure on any root.

## Deliverable 2 — round-60 scratch dirs with sizes

Command: `cd /fast/scratch/hyaku/mori-r60 && du -sk -- * | sort -n`
(blocks, KB; snapshot @ 2026-10-28T16:15:48Z, 55 top-level dirs, 139,848 files,
single-pass total `3,888,192 KB` = 3.71 GiB).

| KB | dir | KB | dir |
|---:|---|---:|---|
| 0 | Mo60Connector92 | 6800 | Mo60Reviewer11 |
| 0 | Mo60Critic23 | 6800 | Mo60Scribe74 |
| 0 | Mo60Critic28 | 6816 | Mo60Executor55 |
| 0 | Mo60Executor60 | 7124 | Mo60Scribe76 |
| 0 | Mo60Revenger96 | 7544 | Mo60Critic27 |
| 0 | Mo60Revenger97 | 10376 | Mo60Reviewer07 |
| 0 | Mo60Reviewer16 | 11656 | Mo60Reviewer15 |
| 0 | Mo60Scout83 | 12800 | Mo60Scribe73 |
| 0 | Mo60Scribe75 | 16744 | Mo60Reviewer04 |
| 0 | Mo60Sentinel41 | 18216 | Mo60Reviewer13 |
| 0 | Mo60Sentinel42 | 18416 | Mo60Critic24 |
| 0 | Mo60SimplifierA1 | 24052 | Mo60Critic25 |
| 0 | Mo60SimplifierA3 | 27504 | Mo60Executor54 |
| 4 | Mo60SimplifierA2 | 27512 | Mo60Executor52 |
| 8 | Mo60Sentinel43 | 43036 | L1-build (non-seat) |
| 20 | Mo60Executor59 (this seat) | 49552 | Mo60Reviewer09 |
| 40 | Mo60Scout81 | 174736 | Mo60MutationTester33 |
| 68 | Mo60Executor61 | 362404 | Mo60MutationTester34 |
| 160 | Mo60Revenger98 | 403100 | Mo60Reviewer03 |
| 476 | Mo60SimplifierA4 | 485016 | Mo60Reviewer06 |
| 484 | Mo60Executor58 | 491984 | Mo60Critic26 |
| 492 | Mo60MutationTester35 | 557236 | Mo60Reviewer01 |
| 1308 | Mo60Reviewer02 | 1081564 | Mo60Executor62 |
| 1392 | Mo60Critic21 | | |
| 1736 | Mo60Critic22 | | |
| 3352 | Mo60Reviewer12 | | |
| 3920 | Mo60MutationTester32 | | |
| 4404 | Mo60Executor57 | | |
| 4476 | Mo60Reviewer08 | | |
| 5424 | Mo60Reviewer05 | | |
| 6252 | Mo60MutationTester31 | | |
| 6800 | Mo60Reviewer10 | | |

Shares of the round total, final sweep (total `4,601,736 KB` = 4.39 GiB at that pass):

```
1081564 KB  23.5%  Mo60Executor62      (ref + gen1 + gen2, ~360 MB each, 41,662 files, no .git)
 561152 KB  12.2%  Mo60Reviewer01      (clone/ 502 MB, full non-shallow clone, .git 142 MB)
 491984 KB  10.7%  Mo60Critic26        (clone/ 362 MB, .git only 2 MB)
 488932 KB  10.6%  Mo60Reviewer06      (repo/ 467 MB, full non-shallow clone)
 456092 KB   9.9%  Mo60MutationTester33
 410056 KB   8.9%  Mo60Reviewer03      (incl. tmp.wSPTINIu8l 362 MB = mktemp -d residue)
 369000 KB   8.0%  Mo60Reviewer10
 362404 KB   7.9%  Mo60MutationTester34
```

## Findings

1. **Green, but the round is the fastest-growing scratch of the fleet.** Round-60 grew
   60 MB → 1.96 GB → 3.47 GB → 3.89 GB → 4.40 GB across this seat's run (19 → 48 → 50 → 55
   dirs). Peak measured rate over a fixed 20 s window:
   `sample1_KB=2005732 sample2_KB=3390312 dt_s=20 delta_KB=1384580 rate_MB_per_s=67.61`.
   Guard's own top-consumer line at 16:16 reads `3.3G idle=0 /fast/scratch/hyaku/mori-r60`
   (idle=0 = written within the last minute). At 67.6 MB/s sustained, the 356 GB soft-line
   headroom on `/fast` would be consumed in ≈1.5 h and the 596 GB free in ≈2.5 h; observed
   growth is bursty clone materialisation, so treat that as an upper-bound slope, not a
   forecast. No action taken; recorded for guard tuning only.

2. **Growth is dominated by whole-lane copies, not fixtures.** Four seats hold full-size
   working trees: Executor62 (3 duplicate trees under `ref/ gen1/ gen2/`, `du -sk`: 360,012 KB
   each) = 23.5% of the round alone; Reviewer01/Reviewer06 clones are **not shallow**
   (`git -C … rev-parse --is-shallow-repository` → `false`; Reviewer01 `.git` = 142,696 KB).
   The round rule is "one lightweight clone/worktree per seat only if needed" — the clones are
   within the letter of the rule, but `--depth`/`--shared` would have cut ~500 MB here.

3. **No seat leaked into `/tmp` or `/var/tmp`** (rule: `/tmp` never as evidence):
   `ls -1d /tmp/*Mo60* /tmp/*mori-r60* /var/tmp/*Mo60* /var/tmp/*mori-r60*` → no matches.
   Guard's `/tmp` top consumers are other lanes/rounds (`/tmp/kasegi-r42-judge` 61.5G idle=30,
   `/tmp/verif-kasegi-r42` 3.6G idle=0). All round-60 bytes are under `$HYAKU_SCRATCH`.

4. **All `.git` under round-60 scratch are inside seat scratch**, so no lane mutation:
   `find /fast/scratch/hyaku/mori-r60 -maxdepth 3 -name .git -prune` →
   `Mo60Reviewer01/clone/.git`, `Mo60Critic27/c1fixture-qdazcx1t/.git`, `Mo60Critic26/clone/.git`.
   None are the lane repo's own `.git`.

5. **Symlinks are deliberate G2 containment fixtures, not escapes.** All hits are relative
   dangling links named to point nowhere:
   `find … -type l -printf '%p -> %l\n'` → `L1-build/c3-freeze{,2,3}/g2/ln`, `L1-build/c3-fr/g2/ln`,
   `Mo60Reviewer02/c3f/g2/ln`, `Mo60Reviewer15/c3freeze/g2/ln`, `Mo60Reviewer13/c3/g2/ln`, each
   `-> nowhere`. No link resolves outside its scratch root.

6. **Scratch cleaned before yield, as required.** Seats present at an early snapshot but absent
   from the final one (`Mo60Executor51`, `Mo60Executor53`, `Mo60Executor56`) have reports on
   disk (`w1/Mo60Executor51.md`, `w1/Mo60Executor53.md`, `w1/Mo60Executor56.md`) with no
   scratch dir left — compliant self-cleanup, not abandonment. 13 empty dirs remain at the
   final snapshot (created, nothing written yet), which is expected mid-wave.

7. **Coverage vs dispatch.** `w1-spec.json` dispatches 64 seats; the scratch root holds 55
   top-level dirs at final snapshot, of which 1 is `L1-build` (non-seat) → 54 seats have
   written something, 10 have not yet (no dir at all). Nothing to remediate; listed so the L1
   can tell "not started" from "started and cleaned".

8. **Guard would not have eaten a live wave.** `disk-guard.sh sweep` skips entries younger than
   `MIN_AGE_MIN=10` (`:504-505` `keep-young`) and re-checks `entry_live` right before `rm`
   (`:733-734` `keep-live`), and unknown liveness is treated as live (header `:59`). With
   `idle=0` on `mori-r60`, a sweep at this moment would have kept the whole round. Read-only
   assessment; no sweep was run.

## Measurement caveats

- The tree is being written concurrently by ~50 live seats. Every number above is a
  non-atomic `du` snapshot; per-dir sums therefore differ from single-pass totals (e.g. 3.89 GB
  single-pass vs 4.40 GB a minute later), and a seat's size can fall between two snapshots
  because it cleaned up. Both figures are reported rather than reconciled.
- `du -sk` counts blocks (dedup within a pass); `du --apparent-size` reads lower on sparse/small
  files. Blocks are used for the guard comparison, since that is what the filesystem charges.
- `L1-build` is the L1's own freeze/control scratch (43 MB) included for completeness; it is
  not a seat dir.

## Deliverables

- Report: `.ufo/waves/round-60/w1/Mo60Executor59.md` (this file).
- disk-guard `status`: exit 0, all three roots green (14% / 38% / 26%), verbatim above.
- round-60 scratch inventory: 55 dirs / 139,848 files / 3.71 GiB at 16:15:48Z, full table above.
- No files outside this report were created, modified or deleted; no commits; no VCS mutation;
  scratch `/fast/scratch/hyaku/mori-r60/Mo60Executor59/` removed before yield.
