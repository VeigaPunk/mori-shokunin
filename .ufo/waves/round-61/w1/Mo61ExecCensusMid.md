# Mo61ExecCensusMid — census-before receipt

Scope: read-only freeze census; no production, registry, VCS, or fleet writes.

Command run at the freeze:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Full captured output (tool reported successful completion; expected exit 0):

```text
mori\tW04\tS035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori\tW04\tS037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori\tW04\tS073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori\tW04\tS074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori\tW04\tS075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori\tW04\tS076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori\tW04\tS147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori\tW04\tS148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori\tW04\tS149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori\tW04\tS150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori\tW04\tS166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori\tW04\tS168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori\tW04\tS201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori\tW04\tS218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori\tW04\tS220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori\tW04\tS228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori\tW04\tS349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori\tW04\tS351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori\tW04\tS470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori\tW04\tS476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori\tW04\tS486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori\tW04\tS491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori\tW04\tS492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori\tW04\tS546 duplicate url www.rfc-editor.org/rfc/rfc8259.txt across scopes
mori\tW04\tS552 duplicate url doi.org/10.1109/TSC.2026.3698682 across scopes
mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

```sh
grep -c '^| S[0-9]' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```
Output: `337`.

Interpretation limited to the request: validator output lists the standing W04 duplicate-URL findings and concludes `mori ok` for SOURCES.md. No fixes or scope expansion performed. Scratch root created: `/fast/scratch/hyaku/mori-r61/Mo61ExecCensusMid` (TMPDIR pointed there); no additional tools installed.
