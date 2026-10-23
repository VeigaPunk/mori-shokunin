measured 2026-10-23T12:05:31Z

VERDICT: mapped

Axes: copy completeness (id has exactly one committed `sources-r<N>` file); pin vs mutable (URL ref, not tag-object immutability); cadence due-date at 2026-10-23 under the census predicate.

## Population

42 rows. `git ls-tree -r --name-only HEAD corpus/evidence` at `c1a026cb156c5fe84d76dc79190f1885ad11abf4` lists exactly these 42 paths, one file per id, so highest-N is the only N. `recheck-r32/` and `recheck-r33/` are not `sources-r<N>` and are excluded. Registry is 204 rows (`corpus/SOURCES.md`, every data row splits to 13 `|`-fields, 11 cells). Ids S156–S204 with no `sources-r` copy: S166, S168, S178, S179, S200, S201, S202.

Dir counts: r30=5, r31=12, r32=3, r33=11, r34=8, r35=3.

URL = first `http(s)` in the source cell, trailing `.,;)` stripped (same rule as contract P-C1). Each of the 42 has exactly one URL.

## Pin rule

- commit: ref is a hex object id (`/<sha>/` or `/commit/<sha>.patch`).
- tag: ref is a version tag (`v262`, `v7.2`, `v4.0.7`, `v12.8.0`, `v2.42.4`, `v4.18`, `v4.19`, `4.3.20.3`) or cgit `?h=man-pages-6.20`.
- mutable: no tag or commit ref in the URL.

HEAD (2026-10-23, `-sI -L`, 5 of 5, no redirect, HTTP 200): S199 commit URL unchanged; S203 `4.3.20.3` unchanged; S169 `?h=man-pages-6.20` unchanged; S175 and S176 stayed on the unversioned URL. S177 not fetched; same `/3/` shape as S176.

## Counts

Pinned 39 (tag 35, commit 4). Mutable 3.

| host | n | pin |
|---|---|---|
| raw.githubusercontent.com | 29 | tag 28, commit 1 (S199) |
| git.kernel.org | 5 | tag 5 |
| github.com | 3 | commit 3 |
| gitlab.com | 2 | tag 2 |
| docs.python.org | 2 | mutable 2 |
| curl.se | 1 | mutable 1 |

Status of the 42: mined 40, rejected 2 (S203, S204). Both rejected rows still have copies.

## Table

| id | line | pin | recheck | opened | copy | URL |
|---|---|---|---|---|---|---|
| S156 | 162 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r30/S156.txt | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c |
| S157 | 163 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r30/S157.txt | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c |
| S158 | 164 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r30/S158.txt | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c |
| S159 | 165 | commit | 180d | 2026-10-22 | corpus/evidence/sources-r30/S159.txt | https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch |
| S160 | 166 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r30/S160.txt | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c |
| S161 | 167 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S161.src | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1 |
| S162 | 168 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S162.src | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/src/pgrep.c |
| S163 | 169 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S163.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/sched.h |
| S164 | 170 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S164.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/exec.c |
| S165 | 171 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S165.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/binfmt_script.c |
| S167 | 173 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S167.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/array.c |
| S169 | 175 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S169.src | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_comm.5?h=man-pages-6.20 |
| S170 | 176 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S170.src | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_cmdline.5?h=man-pages-6.20 |
| S171 | 177 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S171.src | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_pid_stat.5?h=man-pages-6.20 |
| S172 | 178 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S172.src | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man2const/PR_SET_NAME.2const?h=man-pages-6.20 |
| S173 | 179 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S173.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/kernel.rst |
| S174 | 180 | tag | on-release | 2026-10-22 | corpus/evidence/sources-r31/S174.src | https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man5/proc_locks.5?h=man-pages-6.20 |
| S175 | 181 | mutable | on-release | 2026-10-23 | corpus/evidence/sources-r32/S175.src | https://curl.se/docs/manpage.html |
| S176 | 182 | mutable | on-release | 2026-10-23 | corpus/evidence/sources-r32/S176.src | https://docs.python.org/3/library/unicodedata.html |
| S177 | 183 | mutable | on-release | 2026-10-23 | corpus/evidence/sources-r32/S177.src | https://docs.python.org/3/library/html.html |
| S180 | 186 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S180.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst |
| S181 | 187 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S181.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst |
| S182 | 188 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S182.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c |
| S183 | 189 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S183.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h |
| S184 | 190 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S184.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c |
| S185 | 191 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S185.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c |
| S186 | 192 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S186.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h |
| S187 | 193 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S187.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats |
| S188 | 194 | commit | on-release | 2026-10-23 | corpus/evidence/sources-r33/S188.src | https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch |
| S189 | 195 | commit | on-release | 2026-10-23 | corpus/evidence/sources-r33/S189.src | https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch |
| S190 | 196 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r33/S190.src | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c |
| S191 | 197 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S191.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/partitions/core.c |
| S192 | 198 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S192.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/holder.c |
| S193 | 199 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S193.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c |
| S194 | 200 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S194.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/block/zram/zram_drv.c |
| S195 | 201 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S195.src | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c |
| S196 | 202 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S196.src | https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/lib/sysfs.c |
| S197 | 203 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S197.src | https://raw.githubusercontent.com/torvalds/linux/v4.18/block/genhd.c |
| S198 | 204 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r34/S198.src | https://raw.githubusercontent.com/torvalds/linux/v4.19/block/genhd.c |
| S199 | 205 | commit | on-release | 2026-10-23 | corpus/evidence/sources-r35/S199.src | https://raw.githubusercontent.com/VeigaPunk/kimi-shokunin/b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b/skills/shokunin/protocol/AXES.md |
| S203 | 209 | tag | 180d | 2026-10-23 | corpus/evidence/sources-r35/S203.src | https://raw.githubusercontent.com/sharkcz/collectl/4.3.20.3/docs/Disks.html |
| S204 | 210 | tag | on-release | 2026-10-23 | corpus/evidence/sources-r35/S204.src | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c |

Line numbers are `corpus/SOURCES.md`.

## Cadence

Census operative rules (`scripts/sources-census.sh`):

- Valid recheck is an ISO date, `NNd`, or symbolic (`^[A-Za-z][A-Za-z0-9 _-]*$`). Else E09 (`:663-666`, `symbolic` at `:582`).
- `NNd`: due = opened UTC midnight + N×86400 (`epoch` uses `mktime(..., 1)` at `:587`). Overdue when due ≤ today (`:678-685`). Also emits a `cadence` line (`:676-677`).
- ISO date: overdue when that date ≤ today. No `cadence` line.
- Symbolic (`on-release`, and the one registry value `per-closure`): `cadence` line only; due forced invalid; never overdue (`:682`, header `:34-37`).
- Header `:36-37` describes the `cadence` line as symbolic-only. The code also prints it for `NNd`. Code is the predicate used below.

`365d` is ordinary `NNd`, not symbolic. CORPUS.md `:105-106` says recheck is an ISO date or a cadence and names only `90d`, `180d`, `on-release`. It does not name `365d` and does not say symbolic cadences are never overdue. That never-overdue rule is census-only.

Registry recheck values (204 rows): on-release 162, 365d 16, 90d 15, 180d 10, per-closure 1. None of the 16 `365d` rows has a `sources-r` copy. Earliest `365d` due is S029 opened 2026-10-19 (`SOURCES.md:35`) → 2027-10-19. The 42 themselves are on-release 40 and 180d 2 (S159, S203).

Knowledge-file `recheck:` (`CORPUS.md:18`, `:163-170`) is a different surface from the SOURCES column.

## Due at 2026-10-23

None of the 42. None of the 204 registry rows.

- 40 on-release rows: census never judges them overdue.
- S159 180d from 2026-10-22 → 2027-04-20 (`SOURCES.md:165`).
- S203 180d from 2026-10-23 → 2027-04-21 (`SOURCES.md:209`).

No tools installed. No lane writes except this report.
