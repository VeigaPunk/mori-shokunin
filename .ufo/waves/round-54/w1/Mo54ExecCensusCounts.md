# Mo54ExecCensusCounts — frontier-step census before → after

Seat: Mo54ExecCensusCounts (leaf executor, round 54 w1). Not a voter; this report emits no vote line.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Before rev: `39dcf4d7e410d362781a47e8365ca23b5c807598` (entering tip). After rev: `78295c764093ff1f6cee08d7246679900bde7265` (data commit).
Lane HEAD observed during the run: `2d0347a32b6befd7fd946a83319e04f6d8f004b9` (SOURCES.md at HEAD is byte-identical to the data rev).

SOURCES.md sha256 (evidence anchors, `git show <rev>:corpus/SOURCES.md | sha256sum` and `sha256sum corpus/SOURCES.md`):

```
abe6ed025523e91cfadd078e3433938b7fdbfbcd0dfc82b327e8e30f17c6bd08  -    # 39dcf4d7
0bf47834efa86bd4b41af441e6a99a92930d67b3a7ef81933fd8788dd5a1bb61  -    # 78295c76
0bf47834efa86bd4b41af441e6a99a92930d67b3a7ef81933fd8788dd5a1bb61  -    # HEAD 2d0347a3
b75f76f60e08fc213047f862360a93971517b96b9db047117b1bb0a05a373411  corpus/SOURCES.md   # working tree
```

## 1. Registry rows by status and tier — awk, both revs

Row shape used: `^ {0,3}\|[ ]*S[0-9]{3,}[ ]*\|` with `-F'|'`, requiring `NF == 13` (11 columns), then trimming `$5` (tier) and `$9` (status). 0–3 leading spaces accepted; 4+ would be indented code and is ignored.

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git show 39dcf4d7e410d362781a47e8365ca23b5c807598:corpus/SOURCES.md | awk -F'|' -f /fast/scratch/hyaku/mori-r54/Mo54ExecCensusCounts/awk-census.awk
rows=287 malformed=0
tier.A=256 tier.B=14 tier.C=17
status.mined=237 status.queued=24 status.rejected=26
cell.A.mined=227 cell.A.queued=22 cell.A.rejected=7
cell.B.mined=10 cell.B.queued=2 cell.B.rejected=2
cell.C.mined=0 cell.C.queued=0 cell.C.rejected=17
rc=0

$ git show 78295c764093ff1f6cee08d7246679900bde7265:corpus/SOURCES.md | awk -F'|' -f /fast/scratch/hyaku/mori-r54/Mo54ExecCensusCounts/awk-census.awk
rows=297 malformed=0
tier.A=266 tier.B=14 tier.C=17
status.mined=247 status.queued=24 status.rejected=26
cell.A.mined=237 cell.A.queued=22 cell.A.rejected=7
cell.B.mined=10 cell.B.queued=2 cell.B.rejected=2
cell.C.mined=0 cell.C.queued=0 cell.C.rejected=17
rc=0
```

Indentation census at the after rev (`match($0,/^ *\|[ ]*S[0-9]+[ ]*\|/)` → `RSTART-1`):

```
leading_spaces=0 rows=297
```

i.e. every registry row is at column zero; the 0–3-space tolerance changed no count on these revs.

Duplicate-id check at the after rev (`grep -oE 'S[0-9]+' | sort | uniq -d`): no output (0 duplicates). Row-shaped lines matching the pattern: 297, equal to the awk and script row totals, so no row-shaped line sits outside `## Registry` (E12 also absent; see §3).

## 2. Delta (after − before)

| metric | 39dcf4d7 | 78295c76 | delta |
|---|---|---|---|
| rows | 287 | 297 | **+10** |
| tier.A | 256 | 266 | **+10** |
| tier.B | 14 | 14 | 0 |
| tier.C | 17 | 17 | 0 |
| status.mined | 237 | 247 | **+10** |
| status.queued | 24 | 24 | 0 |
| status.rejected | 26 | 26 | 0 |
| cell A/mined | 227 | 237 | **+10** |
| cell A/queued, A/rejected, B/*, C/* | — | — | all 0 |

Only the A/mined cell moved. Expected shape (+10 rows, tier A, mined) is met exactly.

## 3. `sources-census.sh validate` and census (`--root /home/vgpnk/Projects/shokunin mori`)

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status   # before the run
root  use%  free
/tmp 4% 123.7G ; /var/tmp 35% 589.5G ; /fast/scratch/hyaku 27% 593.2G
rc=0

$ cd /home/vgpnk/Projects/shokunin
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
W04=23   E-codes=0   lines=24
```

Comparison with `.ufo/waves/round-54/evidence/census-start.txt`:

```
$ diff .ufo/waves/round-54/evidence/census-start.txt <validate output>
25d24
< exit=0
diff rc=1
```

The 23 W04 lines and the final `mori ok …` line are byte-identical; the only differing line is the literal receipt trailer `exit=0` at the end of `census-start.txt`, which the script itself never prints. Round-start and round-end W04 counts therefore agree at 23, and the command exits 0 as the contract's round-end requirement asks. The 10 new rows (cgit `?h=v7.3` URLs, rendered page `docs.kernel.org/7.3/...`) introduced no new duplicate-URL warning and no E-code.

Independent script cross-check on the exact rev bytes (extracted to scratch, counted with the script rather than my awk):

```
$ git show 39dcf4d7…:corpus/SOURCES.md > $S/SOURCES.39dc.md
$ git show 78295c76…:corpus/SOURCES.md > $S/SOURCES.7829.md
$ sources-census.sh census --file $S/SOURCES.39dc.md
file	rows	287 / tier.A 256 / tier.B 14 / tier.C 17 / status.mined 237 / status.queued 24 / status.rejected 26
census rc=0
$ sources-census.sh census --file $S/SOURCES.7829.md
file	rows	297 / tier.A 266 / tier.B 14 / tier.C 17 / status.mined 247 / status.queued 24 / status.rejected 26
census rc=0
```

The freed `census` totals on the lane worktree agree: `mori rows 297, tier.A 266, tier.B 14, tier.C 17, status.queued 24, status.mined 247, status.rejected 26`, `FLEET` identical, rc=0.

`validate --file` on the scratch copies returns rc=1 with `E11=323` (before) and `E11=337` (after), plus `W04=23` in both. This is a mode artifact, not a lane finding: with `--file` the used-by paths are resolved relative to the copy's directory (`/fast/scratch/...`), so every mined row's used-by reads as missing. The canonical lane-dir run above is E11-free (rc 0). The E11 delta (+14) equals the used-by references on the ten new rows plus the four revised rows, consistent with the row-level diff in §4. No other E-code appears in either file-mode run.

## 4. Row-level diff `39dcf4d7..78295c76 -- corpus/SOURCES.md`

`git diff --unified=0` → 28 lines, rc=0.

Ten added rows, all `tier=A status=mined`:

```
S515 code  Linux mm/memcontrol.c at tag v7.3
S516 code  Linux mm/oom_kill.c at tag v7.3
S517 code  Linux lib/percpu_counter.c at tag v7.3
S518 code  Linux include/linux/percpu_counter.h at tag v7.3
S519 code  Linux include/uapi/asm-generic/errno.h at tag v7.3
S520 docs  Control Group v2 (v7.3) — rendered kernel documentation
S521 code  Linux mm/memory-failure.c at tag v7.3
S522 docs  Linux Documentation/mm/hwpoison.rst at tag v7.3
S523 docs  Linux Documentation/ABI/stable/sysfs-devices-node at tag v7.3
S524 code  Linux include/trace/events/memory-failure.h at tag v7.3
```

Four rows appear as a removed and an added line each; id, URL and tier/status are unchanged, only the trailing used-by cell changed:

```
- S502 used-by: corpus/knowledge/kernel-v7.3-recheck-r53.md
+ S502 used-by: corpus/knowledge/kernel-v7.3-recheck-r53.md, corpus/knowledge/memory-failure-kills-r54.md
- S507 used-by: corpus/knowledge/kernel-v7.3-recheck-r53.md
+ S507 used-by: corpus/knowledge/kernel-v7.3-recheck-r53.md, corpus/knowledge/memory-failure-kills-r54.md
- S508 used-by: corpus/knowledge/kernel-v7.3-recheck-r53.md
+ S508 used-by: corpus/knowledge/kernel-v7.3-recheck-r53.md, corpus/knowledge/kernel-v7.3-recheck-r54.md
- S514 used-by: corpus/knowledge/commit-runway-read-r53.md
+ S514 used-by: corpus/knowledge/commit-runway-read-r53.md, corpus/knowledge/kernel-v7.3-recheck-r54.md
```

Two non-row lines were added between the round-53 addendum and `## Leads (unopened)`:

```
+Round 54 bounded search 1 — Question: at Linux v7.3, do the claim rows the lane still pins to v7.2 hold, and where do their quotes now begin? Where: git.kernel.org cgit `plain/<path>?h=v7.3` … (C1)
+Round 54 bounded search 2 — Question: what does the kernel do, print and count when it kills a process for a hardware memory error … (C2)
```

S515–S524 are all present at the after rev and no id is duplicated; `S502/S507/S508/S514` are present exactly once each.

## 5. Working-tree state observed (read-only note)

`git -C mori-shokunin diff --stat HEAD -- corpus/SOURCES.md` → `1 file changed, 6 insertions(+), 2 deletions(-)`, and the worktree sha256 (`b75f76f6…`) differs from HEAD (`0bf47834…`, equal to the data rev). The uncommitted hunks are: S508's anchor/quote text (adds `vm_memory_committed 937`), S520's anchor wording (`sidebar blurb 7.3.0 at document line 42 (not the footer)`), and the two `Round 54 bounded search` prose blocks above `## Leads`. Row identities, tiers and statuses are untouched, which is why the worktree `census` still reports rows 297 / A 266 / mined 247 / W04 23 identically to the data rev.

Consequence for receipts: `sources-census.sh` parses the working-tree file, so the `validate` receipt above describes the worktree bytes, not the committed bytes at `78295c76`. Both agree on every census metric I measured; if the L1 wants the round-end census bound to a commit, those hunks must be part of that commit. I did not write, stage or revert any of them.

## 6. Limits (UNVERIFIED / not attempted)

- Counts are of the registry table only, as the script defines it; prose, `## Leads`, `## Paths` and per-round search blocks were not counted.
- W04 is a duplicate-URL-across-scopes warning; `23` unchanged means no new duplicate appeared among S515–S524, not that those URLs are unique fleet-wide (the fleet-wide `shared` mode was not run for this seat).
- E04/W-code semantics outside this lane were not examined; only the `mori` lane was validated.
- No network fetch, no clone, no fixture, no commit was made; nothing was written outside this report and `/fast/scratch/hyaku/mori-r54/Mo54ExecCensusCounts/` (removed after the run).
- Tooling: no install or upgrade performed (disk-guard only read). No pacman invocation.

## Findings

1. **LOW — expected frontier step confirmed.** 287 → 297 registry rows, +10 exactly, all in the A/mined cell (256→266 tier A, 237→247 mined); no other tier/status cell moved (`corpus/SOURCES.md`, revs `39dcf4d7` → `78295c76`). The ten added rows are S515–S520 (C1) and S521–S524 (C2), each `tier=A status=mined`, and the four used-by cells S502, S507, S508, S514 gained the round-54 knowledge entries as the contract states.
2. **LOW — round-end census is clean.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` exits 0 with 23 W04 and no E-code; the W04 set is byte-identical to `evidence/census-start.txt`, so the +10 rows added no duplicate-URL warning (`corpus/SOURCES.md`).
3. **LOW — `census-start.txt` carries a non-tool trailer.** Its last line is the literal `exit=0`, which `sources-census.sh` never emits; a strict output diff against a fresh run differs by that one line (`.ufo/waves/round-54/evidence/census-start.txt:25`). The start and end runs otherwise agree; recorded so a later receipt check does not read the trailer as output drift.
4. **LOW — census receipt measures worktree, not commit.** `corpus/SOURCES.md` has uncommitted hunks (S508 and S520 anchor text, two `Round 54 bounded search` prose blocks) that make the worktree sha256 `b75f76f6…` differ from the data rev/HEAD `0bf47834…`. Census metrics are unaffected today, but a round-end receipt bound to commits would not be reproducible from `78295c76` unless those hunks are committed (`corpus/SOURCES.md`, HEAD `2d0347a3`).
