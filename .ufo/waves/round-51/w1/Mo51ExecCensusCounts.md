# Mo51ExecCensusCounts — frontier-step census before → after (round 51, w1)

Seat: Mo51ExecCensusCounts (executor, leaf). Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Item: count Registry rows by status and tier at `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` (entering) and
`87e0c374537557754bf71dd68036ded3ddc6699c` (data), plus `sources-census.sh validate` vs
`evidence/census-start.txt`. No drafts; census only. I am not an entailment seat, so this report carries no
judgment lines and starts no line with the vote keyword.

## Scratch and guards

```
$ mkdir -p /fast/scratch/hyaku/mori-r51/Mo51ExecCensusCounts/tmp
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                               4%   124.0G
/var/tmp                          35%   584.8G
/fast/scratch/hyaku               26%   601.8G
rc=0
```

Scratch used: `/fast/scratch/hyaku/mori-r51/Mo51ExecCensusCounts/` (TMPDIR at `…/tmp`). No clone, no fixture repo,
no git mutation; only `git show`/`git rev-parse`/`sha256sum` reads. Scratch removed at the end (see §Cleanup).
No tool installed or upgraded (nothing needed).

## Method

Rows are read from the committed registry blobs (never the working tree for the two revs):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <rev>:corpus/SOURCES.md | awk -F'|' '<counter>'
```

Counter (`/fast/scratch/hyaku/mori-r51/Mo51ExecCensusCounts/census.sh`, kept only as the paste below — deleted with
scratch):

```awk
# accept 0-3 leading spaces before the leading pipe; registry columns are
# $2 id | $3 source | $4 kind | $5 tier | $6 scope | $7 anchor | $8 teaches | $9 status | ...
/^ {0,3}\| *S[0-9][0-9][0-9] *\|/ {
  tier=$5; status=$9
  gsub(/^[ \t]+|[ \t]+$/,"",tier)
  gsub(/^[ \t]+|[ \t]+$/,"",status)
  n++
  by_tier[tier]++
  by_status[status]++
  by_pair[status "\t" tier]++
}
END {
  printf "rows=%d\n", n
  print "-- by tier";      for (t in by_tier)   print "tier=" t "\t" by_tier[t]
  print "-- by status";    for (s in by_status) print "status=" s "\t" by_status[s]
  print "-- by status x tier"; for (p in by_pair) { split(p,a,"\t"); print "pair=" a[1] "/" a[2] "\t" by_pair[p] }
}
```

(Output piped through `sort -u` only to make the associative-array order stable; headers therefore sort with their
values, counts are unchanged.)

## Before — `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`

```
$ ./census.sh /home/vgpnk/Projects/shokunin/mori-shokunin aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd before.txt; echo rc=$?
rc=0
== rev: aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd
-- by status
-- by status x tier
-- by tier
pair=mined/A	204
pair=mined/B	10
pair=queued/A	22
pair=queued/B	2
pair=rejected/A	7
pair=rejected/B	2
pair=rejected/C	17
rows=264
status=mined	214
status=queued	24
status=rejected	26
tier=A	233
tier=B	14
tier=C	17
```

## After — `87e0c374537557754bf71dd68036ded3ddc6699c`

```
$ ./census.sh /home/vgpnk/Projects/shokunin/mori-shokunin 87e0c374537557754bf71dd68036ded3ddc6699c after.txt; echo rc=$?
rc=0
== rev: 87e0c374537557754bf71dd68036ded3ddc6699c
-- by status
-- by status x tier
-- by tier
pair=mined/A	209
pair=mined/B	10
pair=queued/A	22
pair=queued/B	2
pair=rejected/A	7
pair=rejected/B	2
pair=rejected/C	17
rows=269
status=mined	219
status=queued	24
status=rejected	26
tier=A	238
tier=B	14
tier=C	17
```

## Delta

| cell | entering | data | delta |
|---|---|---|---|
| rows | 264 | 269 | **+5** |
| status mined | 214 | 219 | **+5** |
| status queued | 24 | 24 | 0 |
| status rejected | 26 | 26 | 0 |
| tier A | 233 | 238 | **+5** |
| tier B | 14 | 14 | 0 |
| tier C | 17 | 17 | 0 |
| mined/A | 204 | 209 | **+5** |
| queued/A | 22 | 22 | 0 |
| rejected/A | 7 | 7 | 0 |

Matches the item's expectation: +5 rows, all tier A, all mined; no other cell moves.

Row-level identity diff (`<id>\t<tier>\t<status>`, `comm` over the two sorted tables):

```
$ comm -13 rows-before.tsv rows-after.tsv     # added at data
S492	A	mined
S493	A	mined
S494	A	mined
S495	A	mined
S496	A	mined
$ comm -23 rows-before.tsv rows-after.tsv     # removed at data
(no lines)
$ join -t$'\t' -j 1 rows-before.tsv rows-after.tsv | awk -F'\t' '$2!=$4 || $3!=$5'
(no lines)                                    # every pre-existing id keeps its tier and status
```

So the +5 is exactly S492–S496; no existing row was retiered, re-statused or deleted. Their non-empty `used-by`
points at the C2 entry in all five cases:

```
$ git -C … show 87e0c37:corpus/SOURCES.md | awk -F'|' '… id ~ /^S49[2-6]$/ …'
S492 nf=13 tier=A status=mined used-by=[corpus/knowledge/memavailable-estimate-r51.md]
S493 nf=13 tier=A status=mined used-by=[corpus/knowledge/memavailable-estimate-r51.md]
S494 nf=13 tier=A status=mined used-by=[corpus/knowledge/memavailable-estimate-r51.md]
S495 nf=13 tier=A status=mined used-by=[corpus/knowledge/memavailable-estimate-r51.md]
S496 nf=13 tier=A status=mined used-by=[corpus/knowledge/memavailable-estimate-r51.md]
```

Parser coverage check (the 0–3-space rule loses nothing):

```
== aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd
raw '| S' occurrences: 264
awk-accepted rows:     264
4+-space-leading rows: 0
max id: 491
duplicate ids:         (none)
== 87e0c374537557754bf71dd68036ded3ddc6699c
raw '| S' occurrences: 269
awk-accepted rows:     269
4+-space-leading rows: 0
max id: 496
duplicate ids:         (none)
```

## `sources-census.sh validate`

```
$ cd /home/vgpnk/Projects/shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin mori > validate.txt 2>&1; echo "rc=$?"
rc=0
$ grep -c W04 validate.txt
23
```

Full output (24 lines, rc 0):

```
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
```

Comparison with `evidence/census-start.txt` (rc 0, 22 W04 + `ok`): count 22 → **23**, id-set diff by `comm`:

```
$ comm -13 w04-start.ids w04-now.ids   # added
S492
$ comm -23 w04-start.ids w04-now.ids   # removed
(no lines)
```

The single new warning is S492 `raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst
… across scopes` — the contract's declared proc.rst row sharing S082's URL at a different scope. The pre-existing
S168 W04 on the same URL is the earlier rejected same-scope duplicate named in S492's own scope cell, so the
proc.rst URL now carries three rows (S082 mined, S168 rejected, S492 mined-different-scope) and two W04 lines.
`ok` for the registry file is preserved: no duplicate ids, no parse failure.

Reading is at the data commit, not a drifted tree:

```
$ git -C … rev-parse HEAD
b504cb1701568a0038aab9d98ec13d28eff801da          # later wave commits on top of the data commit
$ sha256sum …/corpus/SOURCES.md
1584410b6abb888b6dea6867377de6ee1340f36ecd78194b01e8049a49f26d32
$ git -C … show HEAD:corpus/SOURCES.md | sha256sum
1584410b6abb888b6dea6867377de6ee1340f36ecd78194b01e8049a49f26d32
$ git -C … show 87e0c37:corpus/SOURCES.md | sha256sum
1584410b6abb888b6dea6867377de6ee1340f36ecd78194b01e8049a49f26d32
```

Working tree, lane HEAD and the data commit all carry the same registry bytes, so the validator read the data-commit
registry. `sources-census.sh validate` takes no revision argument (it reads the path under `--root`); I did not
invent one.

## Limits of this census

- `validate` was run once, at one tree state; it is not a regression series and says nothing about the five new
  source copies' bytes (the freeze sha256 list and C2's copy arm cover that, not this seat).
- The status/tier counts are the registry's own cells; they are not a re-judgment of whether each row deserves its
  `mined` status. S492–S496 are marked `mined` with `used-by` naming an entry that exists at the data commit; the
  entry's own quality is C2's business.
- The W04 rule compares URLs across scopes; a W04 line is a warning, not an error. I did not attempt to decide
  whether S492/S168/S082 should be merged — that is registry-policy work outside this item and outside lane
  authority for a dispatched seat.
- If the lane later adds rows or edits scopes, the after-census and the 23-W04 count are the data-commit reading and
  must be re-taken at whatever tip the L1 measures.

## Cleanup

```
$ rm -rf /fast/scratch/hyaku/mori-r51/Mo51ExecCensusCounts
```

Everything cited above is pasted in this report before removal. No file outside my report and scratch was written;
no fleet-root tracked file, no PATH directory, no `~/.local/bin`, nothing in `~/.local/bin`, nothing under
`mori-shokunin/` except this report.

## Findings

- **LOW** — `.ufo/waves/round-51/w1/Mo51ExecCensusCounts.md` (this census): the census agreement is exact
  (+5 rows, all tier A / mined, no other cell moved, rc 0 both census and validate), so nothing here contradicts
  the contract. The one item for the L1 to note is the expected growth of the W04 set: 22 → 23 W04 lines, all
  attributable to S492's declared same-URL/different-scope proc.rst row (`corpus/SOURCES.md` S492 vs S082/S168).
  If the round-end census is compared against `evidence/census-start.txt` without that expectation, the +1 W04
  reads as a regression when it is the pinned design.
- **LOW** — `scripts/sources-census.sh` (lane-external, read-only): `validate` offers no revision selector, so a
  census at a named commit is only exact when the working tree happens to equal that commit (true here; verified by
  three equal sha256 values). Named as a measurement limit, not a defect request.
