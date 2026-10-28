# Mo60Executor53 — mid-round source census (round 60, w1)

Role: executor, leaf. Work mode: read-only (no VCS mutation, no production edits).
Host guard: `disk-guard.sh status` green before work (`/fast/scratch/hyaku` use 26%, 600.0G free;
`/tmp` 14%; `/var/tmp` 38%). No pacman, no installs.

## Pins (so every number below is re-derivable)

| Item | Value |
|---|---|
| Lane repo | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| Lane HEAD at measurement | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| Entering revision (contract) | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| `corpus/SOURCES.md` worktree vs HEAD | clean (`git status --porcelain -- corpus/SOURCES.md` → empty) |
| `corpus/SOURCES.md` sha256 | `e8bda4a85241e9cf2ae719afa790e1b2b61da5fb7ec36568335d8c618add9441` |
| `corpus/SOURCES.md` blob at HEAD | `c3a91a392dbdce026e07e3b54d2c980221985379` |
| `scripts/sources-census.sh` sha256 | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` |

## Command 1 — census validate

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Exit status: **0**. Output verbatim (26 lines = 25 × W04 + 1 × ok):

```text
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
mori	W04	S546 duplicate url www.rfc-editor.org/rfc/rfc8259.txt across scopes
mori	W04	S552 duplicate url doi.org/10.1109/TSC.2026.3698682 across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Reading: `mori ok <SOURCES.md>`; W04 = same URL across scopes, a warning class that does not
fail validation (script line 33: "warnings do not affect clean lanes"; line 364 selftest
`W04-does-not-fail-validation` expects exit 0). No E04 (within-scope duplicate) and no error
class appears. Last line is the `ok` verdict, so the lane is clean.

## Command 2 — row count

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Output: **`337`**, exit 0.

Cross-checks on the same file:

- unique ids = 337, duplicate ids = none.
- min id `S001`, max id `S564` (337 rows over a 564-wide id space ⇒ gaps exist by design; no
  id is reused).
- total `^|` lines = 339 = 337 data rows + 1 header + 1 separator row — the `S\d{3,}` pattern
  selects data rows only, not header/separator.
- committed blob count at HEAD is also 337, so the count is not a dirty-worktree artefact.

## Delta vs the frozen round-start receipt

Contract states round start: exit 0, 333 rows, standing W04 set. Mid-round:

| Metric | Round start (`.ufo/waves/round-60/evidence/census-start.txt`) | Mid-round (this seat) |
|---|---|---|
| Census exit | 0 | 0 |
| Census output | 26 lines, 25 W04 + ok | byte-identical (`diff` → empty) |
| W04 id set | 25 ids | identical set (`W04_SET_IDENTICAL`) |
| SOURCES rows | 333 | **337** |

The +4 rows are exactly the §2b sourced-claim rows the contract predicts, confirmed by
`git diff ddfb12fb… HEAD -- corpus/SOURCES.md` (`1 file changed, 4 insertions(+)`):

- `S561` — Mo59Critic22 (own-work, A)
- `S562` — Mo59Sentinel57 (own-work, A)
- `S563` — Mo59Critic25 (own-work, B)
- `S564` — Mo59Sentinel58, REJECTED as duplicate scope of S562 (own-work, B; partition flip recorded)

No URL-bearing rows were added, which is why the W04 set and the census bytes did not move while
the row count rose 333 → 337. This matches contract §Census ("new S rows raise the count") and
§2b without adding new warnings.

## Findings

1. Census validate is clean: exit 0, `mori ok`, standing 25-row W04 warning set, no E04/errors.
2. Row count 337 (= 333 + 4), all ids unique, committed and worktree agree at HEAD `b3c25613`.
3. Mid-round census output is byte-identical to the committed round-start receipt; the +4 rows
   are exactly the four predicted own-work rows. No defect to report.

## Scope / non-actions

Read-only. No commits, no VCS mutation, no writes outside this report and scratch
(`$HYAKU_SCRATCH/mori-r60/Mo60Executor53`). No production files, corpus registry, SCORECARD, LOG,
lane VCS, fleet or sibling repos touched. No subagents. No tool installs, so no
tool/version/channel record is owed.

## Blockers / risks

None. Residual observation only: the W04 warning set is unchanged and remains non-failing by
design; if round end requires a stricter duplicate policy that would be a contract change, not a
finding of this seat.
