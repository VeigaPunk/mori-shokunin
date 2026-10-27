# Mo53ExecCensusCounts — frontier-step census, entering tip vs data commit

Seat: Mo53ExecCensusCounts (executor, leaf). Scope: count the SOURCES Registry by status and tier at the
frozen entering tip `20edafa5` and at the landed data commit `2a4213bf`, and run the frozen fleet census
validator, against `.ufo/waves/round-53/evidence/census-start.txt`. Read-only on the lane: no git/jj mutation,
no writes outside this report and `/fast/scratch/hyaku/mori-r53/Mo53ExecCensusCounts/` (removed at exit).

Machine: MACHINE_ID. No tools installed this seat. No network fetched this seat (both revisions read from the
lane's own object store).

## 1. Revisions and what was measured

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
95cf78eef71979f9b740ef6bc3c5299b6beff86e
exit=0
$ git -C ... log --oneline -3
95cf78ee round-53: wave w1 spec (67 seats, policy v2, validated), dispatch payload, receipts at data
2a4213bf round-53: data — v7.3 recheck ledger (C1), mori-commit-runway tool + fixtures + SKILL Round53 registry row and band entry (C2), rows S502-S513, S499 used-by
f4da3fd4 round-53: freeze — contract, C1/C2 counters with selftests, controls and receipts, census-start, sweeps, v7.3 and band source copies
exit=0
```

The wave-spec tip `95cf78ee` carries the same `SOURCES.md` blob as the data commit, so the live worktree is the
landed data content (not a stale read):

```
$ git -C ... rev-parse 2a4213bf:corpus/SOURCES.md 95cf78ee:corpus/SOURCES.md
89dd8625ada2e74ff8194c517e8d1eb324a262bc
89dd8625ada2e74ff8194c517e8d1eb324a262bc
exit=0
$ git -C ... diff --stat 2a4213bf 95cf78ee -- corpus/SOURCES.md
(no output)
exit=0
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
3454e59393be091c96fce768858fa343b9d375e9b46403fa4bac8fa43eab3167  .../mori-shokunin/corpus/SOURCES.md
$ git -C ... show 20edafa5:corpus/SOURCES.md | sha256sum
c949999424ce88385e0a9118ab74478cbaec62f3dc992a6883722e47966fbca9  -
$ git -C ... show 2a4213bf:corpus/SOURCES.md | sha256sum
3454e59393be091c96fce768858fa343b9d375e9b46403fa4bac8fa43eab3167  -
exit=0
```

So: before = sha256 `c9499994…` (341 lines, 265710 bytes), after = sha256 `3454e593…` (355 lines, 274479 bytes).

## 2. Registry census by status and tier (awk, 0–3 leading spaces, Registry section only)

Awk used (identical for both revs; `NF!=13` rows are counted as `badrows` rather than silently dropped):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <rev>:corpus/SOURCES.md | awk '
function trim(s){ gsub(/^[ \t]+|[ \t]+$/,"",s); return s }
/^## /{ sec=$0; next }
sec=="## Registry" && /^ {0,3}\| *S[0-9]/ {
  n=split($0,a,"|"); if (n!=13) { bad++; next }
  tier=trim(a[5]); st=trim(a[9]); rows++
  ... tally tc[tier], sc[st], kc[tier "/" st] ...
}'
```

Output, before (`20edafa59b38dac1ca358893f0259b1f436372d3`):

```
rows=274 badrows=0
status totals: mined=224 queued=24 rejected=26
tier totals: A=243 B=14 C=17
tier x status:
  A/mined=214
  A/queued=22
  B/queued=2
  C/rejected=17
  B/mined=10
  A/rejected=7
  B/rejected=2
exit=0
```

Output, after (`2a4213bf8da72f7cd78189baa5bb9be825dca1df`):

```
rows=286 badrows=0
status totals: mined=236 queued=24 rejected=26
tier totals: A=255 B=14 C=17
tier x status:
  A/mined=226
  A/queued=22
  B/queued=2
  C/rejected=17
  B/mined=10
  A/rejected=7
  B/rejected=2
exit=0
```

Delta (row counts only; no other group moved):

| measure | before | after | delta |
|---|---|---|---|
| Registry rows | 274 | 286 | **+12** |
| tier A | 243 | 255 | **+12** |
| tier B | 14 | 14 | 0 |
| tier C | 17 | 17 | 0 |
| status mined | 224 | 236 | **+12** |
| status queued | 24 | 24 | 0 |
| status rejected | 26 | 26 | 0 |
| A/mined | 214 | 226 | **+12** |
| A/queued | 22 | 22 | 0 |
| A/rejected | 7 | 7 | 0 |
| B/mined | 10 | 10 | 0 |
| B/queued | 2 | 2 | 0 |
| B/rejected | 2 | 2 | 0 |
| C/rejected | 17 | 17 | 0 |
| id space | max S501 | max S513 | +12 contiguous ids |
| tier-A share | 243/274 = 88.7 % | 255/286 = 89.2 % | +0.5 pt |

Field-count sanity (no malformed rows at either rev, so the `badrows` guard never fired):

```
$ ... | awk '/^## /{sec=$0;next} sec=="## Registry" && /^ {0,3}\| *S[0-9]/{n=split($0,a,"|"); print n}' | sort | uniq -c
    274 13      # before
    286 13      # after
exit=0
```

Rows with 4+ leading spaces (which the maintained parser ignores as code) and row-shaped lines outside
`## Registry` — both zero, so the awk and the frozen parser see the same row universe:

```
$ git show <rev>:corpus/SOURCES.md | grep -cE '^ {4,}\| *S[0-9]'
0    # before
0    # after
$ awk '/^ {0,3}##[ \t]/{sec=$0;next} /^ {0,3}\| *S[0-9]/{if (sec !~ /## Registry/) print NR": "$0}' b.md
(no output)
exit=0
```

## 3. The added rows are exactly S502–S513, all tier A / mined / opened 2026-10-26

```
$ comm -13 ids-<before>.txt ids-<after>.txt      # ids in after, not before
S502 S503 S504 S505 S506 S507 S508 S509 S510 S511 S512 S513
$ comm -23 ids-<before>.txt ids-<after>.txt      # ids in before, not after
(no output)
exit=0
```

Per-row attributes from the landed blob (id, kind, tier, status, opened, recheck, and the used-by target):

```
S502 kind=docs tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/Documentation/filesystems/proc.rst?h=v7.3   -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S503 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/mm/show_mem.c?h=v7.3                        -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S504 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/fs/proc/meminfo.c?h=v7.3                    -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S505 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/include/linux/mm_inline.h?h=v7.3            -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S506 kind=docs tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/Documentation/mm/overcommit-accounting.rst?h=v7.3 -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S507 kind=docs tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/Documentation/admin-guide/sysctl/vm.rst?h=v7.3   -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S508 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/mm/util.c?h=v7.3                            -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S509 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/include/linux/mman.h?h=v7.3                  -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S510 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/mm/mmap.c?h=v7.3                            -> corpus/knowledge/kernel-v7.3-recheck-r53.md
S511 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/mm/mm_init.c?h=v7.2                          -> corpus/knowledge/commit-runway-read-r53.md
S512 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/lib/percpu_counter.c?h=v7.2                  -> corpus/knowledge/commit-runway-read-r53.md
S513 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release  git.kernel.org/…/include/linux/percpu_counter.h?h=v7.2        -> corpus/knowledge/commit-runway-read-r53.md
```

Composition: `docs/A/mined=3` (S502, S506, S507), `code/A/mined=9`. All 12 use git.kernel.org cgit (no
raw.githubusercontent.com), which is why the W04 duplicate-URL set did not grow (§5). Both used-by targets exist
in the landed tree (`git cat-file -e 2a4213bf:corpus/knowledge/kernel-v7.3-recheck-r53.md` and
`…commit-runway-read-r53.md` both exit 0).

## 4. Registry rows changed in place — exactly one (S499 used-by)

Row-level diff (id → row text with a leading `| Sxxx` stripped, `join`ed across the two revs):

```
$ join -t$'\t' rows-<before>.tsv rows-<after>.tsv | awk -F'\t' '$2!=$3{print $1}'
S499
$ ... | wc -l
1
exit=0
```

The change is a used-by append, not a status/tier move:

```
$ git show 20edafa5:corpus/SOURCES.md | grep -E '^ *\| *S499 ' | awk -F'|' '{print $12}'
 corpus/knowledge/overcommit-commit-limit-r52.md
$ git show 2a4213bf:corpus/SOURCES.md | grep -E '^ *\| *S499 ' | awk -F'|' '{print $12}'
 corpus/knowledge/overcommit-commit-limit-r52.md, corpus/knowledge/commit-runway-read-r53.md
exit=0
```

This is the cross-claim link C2 needs (the round-52 overcommit source now also feeds the round-53 band entry).
It also shows why a status/tier census alone cannot see claim drift: one pre-existing row changed and no counter
in §2 moved. The row-text diff above is what closes that gap.

Whole-file diff accounting — the 14-line file delta is 12 registry rows plus 2 lines outside the table:

```
$ diff a.md b.md | grep -vE '^[<>] \| *S(50[2-9]|51[0-3]) ' | cut -c1-140
278c278                                   # S499 modified (used-by)
280a281,292                               # 12 added rows
331a344   Round 53 bounded search — Question (C1): … v7.3 … (Search log)
337a351   - (round 53) panic_on_unrecoverable_memory_failure, new in v7.3 … vm.rst (S507 copy) … (Leads)
exit=0
```

Neither added line is row-shaped, so neither trips E12 (§5, exit 0).

## 5. Frozen validator at both ends

### 5a. Entering tip, run independently (not from the receipt)

`census-start.txt` records only the W04 lines, an `ok` line and `rc 0` — it carries no tier/status totals. So I
re-ran the frozen script against an extracted entering-tip tree (fixture root in my scratch; `git archive`
extract, no clone, no mutation of the lane), and cross-checked against the receipt's W04 set:

```
$ printf 'LANES="\nmori|mori-shokunin|mori lane fixture\n"\n' > root-before/shokunin.conf
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 20edafa59b38dac1ca358893f0259b1f436372d3 \
    | tar -x -C /fast/scratch/hyaku/mori-r53/Mo53ExecCensusCounts/root-before/mori-shokunin
exit=0
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /fast/scratch/hyaku/mori-r53/Mo53ExecCensusCounts/root-before mori
…(23 W04 lines, byte-identical to census-start.txt; see diff below)…
mori	ok	/fast/scratch/…/root-before/mori-shokunin/corpus/SOURCES.md
exit=0
$ grep -c W04 before-validate.txt
23
$ diff <(grep W04 before-validate.txt) <(grep W04 .../evidence/census-start.txt) && echo IDENTICAL_BEFORE
IDENTICAL_BEFORE
exit=0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root .../root-before mori
mori	rows	274
mori	tier.A	243
mori	tier.B	14
mori	tier.C	17
mori	status.mined	224
mori	status.queued	24
mori	status.rejected	26
FLEET	rows	274
FLEET	tier.A	243
FLEET	tier.B	14
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	24
FLEET	status.mined	224
FLEET	status.rejected	26
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

The frozen script's own totals and my awk agree exactly at the entering tip (274 / 243 / 14 / 17 / 224 / 24 / 26),
by two independent implementations.

### 5b. Landed tip (live fleet root, required round-end command)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc61…/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40…/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20…%20技术白皮书.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
$ grep -c W04 census-end.txt
23
$ wc -l < census-end.txt
24
$ diff <(grep W04 census-end.txt) <(grep W04 .../evidence/census-start.txt) && echo IDENTICAL_END
IDENTICAL_END
exit=0
$ grep -cE 'git\.kernel\.org|v7\.3' census-end.txt
0
```

Landed totals from the same frozen script in `census` mode (matches §2 exactly):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori
mori	rows	286
mori	tier.A	255
mori	tier.B	14
mori	tier.C	17
mori	status.mined	236
mori	status.queued	24
mori	status.rejected	26
FLEET	rows	286 … FLEET	status.invalid	0 … FLEET	missing	0
exit=0
```

### 5c. Independent re-implementation of the W04 rule

I re-derived W04 from the source rows with my own reading of the script's `url_of()` normalization (strip
fragment and trailing slash, drop scheme, lowercase host) and the "same URL, different scope" rule, without
calling the script:

```
rows 274 W04 23   # 20edafa5
rows 286 W04 23   # 2a4213bf   (identical id+URL list at both revs)
exit=0
```

The 23 `(id, url)` pairs are the same set and order as `census-start.txt` and as the landed run. Therefore the
data commit adds zero W04: the twelve new rows use distinct cgit URLs under distinct scopes, and none of them
collides with a pre-existing URL. Also checked: `unique_ids=286 dup=0` and no duplicate full URL among the 12 new
rows (all `h=v7.3`/`h=v7.2` paths differ).

## 6. Comparison with the receipt (required line)

| reading | census-start.txt (22:28, entering tip) | this seat, entering tip (re-run) | this seat, landed tip (2a4213bf) |
|---|---|---|---|
| exit code | 0 | 0 | 0 |
| W04 count | 23 | 23 (byte-identical lines) | 23 (byte-identical lines) |
| rows / tier A / tier B / tier C | not recorded in receipt | 274 / 243 / 14 / 17 | 286 / 255 / 14 / 17 |
| mined / queued / rejected | not recorded in receipt | 224 / 24 / 26 | 236 / 24 / 26 |

Round-end requirement ("same command, exit 0") is satisfied at the landed tip: exit 0, W04 unchanged at 23, no
new E-code (the script emits none), so no new structural defect entered the registry with S502–S513.

## 7. Expected delta vs observed

Expected per assignment: +12 rows S502–S513, tier A, mined. Observed: exactly that — +12 rows, +12 tier A,
+12 mined, ids contiguous from the previous maximum S501 to S513, all twelve `opened 2026-10-26`, all twelve
`recheck: on-release`, zero removals, one pre-existing row text change (S499 used-by), zero new W04, validate
exit 0. Expectation confirmed with no residual.

## Findings

- **LOW — `corpus/SOURCES.md` rows S511–S513 (landed in `2a4213bf`).** These three C2 rows are new in this round
  but pin `mm/mm_init.c`, `lib/percpu_counter.c` and `include/linux/percpu_counter.h` at tag **v7.2** with
  `recheck: on-release`, while v7.3 is already tagged and the release trigger that C1 answers has fired. Nothing
  in C1's scope D covers these three files (D is the nine v7.3 paths S502–S510), so round 53 leaves three brand
  new rows already exposed to the same release-trigger debt C1 exists to clear. The pins themselves are accurate
  and are correctly labelled v7.2; this is recheck debt created by the round, not a counting defect. Whether
  those three paths changed between v7.2 and v7.3 is UNVERIFIED by this seat (no v7.3 copies fetched). Routed
  item for round 54, not a round-53 counter change.
- **LOW — `corpus/SOURCES.md` (registry-wide), census blind spot.** The status/tier census is invariant under
  in-place row rewrites: S499's used-by column changed between the two revs and every status/tier total in §2 is
  identical. Any future round that leans on "the census did not move" as evidence of "the registry did not
  change" would be wrong; the row-text join of §4 (1 modified row) is the check that actually covers it. Worth
  one line in the census procedure for round 54.
- **LOW — `corpus/SOURCES.md` tier distribution.** All twelve new rows are tier A, lifting tier-A share from
  88.7 % to 89.2 % (243/274 → 255/286) with no tier downgrades anywhere. Consistent with the contract (nine
  primary kernel files at v7.3, three at v7.2), but it means the registry's tier mix is now even more
  A-heavy; the lane's tier-B/C (secondary/community) evidence has not moved in this round. Informational for
  the frontier axis, no action implied by the contract.
- **No defect found** in the required readings: +12 rows S502–S513, all tier A and mined (§2, §3), W04 held at
  23 with rc 0 at both ends (§5), and the frozen script's totals reproduce my independent awk exactly (§2, §5a).

## Hygiene

- Concurrency note: at report time `git status --porcelain` in the lane lists sibling in-flight edits to
  `SKILL.md`, `corpus/knowledge/commit-runway-read-r53.md`, `tools/mori-commit-runway.py` and
  `tools/fixtures/mori-commit-runway/cases.json`. `corpus/SOURCES.md` is **not** among them, so the live
  `validate`/`census` runs above measured the landed blob `3454e593…` and not a sibling's draft. Both census
  arms additionally read `git show <rev>:corpus/SOURCES.md`, which is immune to worktree churn.
- Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ExecCensusCounts/` (`tmp/` for TMPDIR, `root-before/` for the
  entering-tip extract, ~334 MB). `bash scripts/hyaku/disk-guard.sh status` → rc 0, `/fast/scratch/hyaku` 25 %
  used, 605.5 G free, before the extract. Scratch removed with `rm -rf` at exit; nothing cited here lives only in
  scratch.
- Writes: this report only. No git/jj mutation in `/home/vgpnk/Projects/shokunin/mori-shokunin` or the fleet root
  (reads used `git show` / `git rev-parse` / `git cat-file -e` / `git archive`); no file created inside the lane
  by any tool; no PATH-directory write; no service or host setting touched.
- This report casts no voter line: it contains no line beginning with the voter keywords the C1 counter scans for.
