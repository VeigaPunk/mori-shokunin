# Mo80S03Lesson — round 80 w1

## Behavior and affected surfaces

1. Read the frozen contract, entering controls, SCORECARD axes/capabilities/r79 row, SKILL registry row 13, QUALITY 90/154/159/161–164, province boundaries and the r79 spot-check's D79-1/D79-5. Axes: calibration, operability, coverage; no scalar scores changed.
2. Created `corpus/lessons/round-80.md`, with front matter, Gate S595 scaffold, one mined D79-1 correction-sweep mistake, census and refusals, in the requested order. It names commands but does not convert planned green output into execution evidence.
3. Ran the explicitly assigned census and row count below. Did not rerun product selftests or frozen claim counters; entering red evidence is attributed to the existing controls receipt.
4. Requested source provenance from Mo80Sc02Source. The peer supplied pin/quote/duplicate facts in a message, but its report path remained absent at the last read. The lesson therefore retains the explicitly authorized `PIN PENDING — filled by the L1`, rather than installing a digest unsupported by the requested report.

Only writes: `corpus/lessons/round-80.md` and this assigned report. No product code, registry, contract, counters, fleet-root file, MANIFEST, OS/unit state or PATH directory changed. No commits, runtime invocation, installs, fixture, clone or scratch directory created. No subagent dispatch.

## Commands and observed outcomes

### Required round-start census

Working directory: `/home/vgpnk/Projects/shokunin/mori-shokunin`; live registry, not a revision export. Command:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; printf '\nexit=%s\n' "$?"
```

Output (tab-separated tool output reproduced below):

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
mori	W04	S565 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3 across scopes
mori	W04	S566 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 across scopes
mori	W04	S567 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/include/linux/psi_types.h?h=v7.3 across scopes
mori	W04	S568 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3 across scopes
mori	W04	S570 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3 across scopes
mori	W04	S571 duplicate url git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 across scopes
mori	W04	S583 duplicate url learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 across scopes
mori	W04	S585 duplicate url learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-queryunbiasedinterrupttime across scopes
mori	W04	S586 duplicate url docs.aws.amazon.com/waf/latest/developerguide/waf-tokens-immunity-times.html across scopes
mori	W04	S587 duplicate url learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md

exit=0
```

### Required row count

```sh
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Observed stdout `367`; command succeeded (rc 0). This is the live before-value, not a count invented from the last source ID.

### Evidence reads and provenance

- `read` `.ufo/waves/round-80/contract.md` and `evidence/controls-r80.txt`: contract P-C1/P-C2/P-C3 and all inherited negative controls available.
- `read` `SCORECARD.md:6-20,4006-4020`: six axes 6/7/5/5/5/6; r79 capability row still states `selftest 18 in-memory cases`.
- `read` `SKILL.md:1354-1395`: registry row states `CONTROL_RECEIPT_SELFTEST pass=19 fail=0`.
- `read` `corpus/lessons/round-79-verifier-spotcheck.md:96-105`: D79-1 explicitly identifies sibling-carrier disagreement; D79-5 says `when the selftest is next touched`.
- `grep` pinned HTML for `Mutation|mutation|<title>|Abstract`: line 121 carries the abstract definition used in the lesson. Quote is the first full sentence, 22 whitespace-delimited words, preserving literal `&#39;` from the pin. This seat did not independently run word-count or anchor-check tools.
- `read` `.ufo/waves/round-80/w1/Mo80Sc02Source.md`: absent at each attempted read; not treated as a completed source report.
- Source peer message reports sha256 `28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884`, pin 613 lines/43884 bytes, duplicate searches rc 1, two HTTP-200 captures identical. These are peer-reported, not this seat's fetch/hash evidence. The L1 must reconcile to the durable source report before removing the pin placeholder.

## Findings and conflicts for the canonical judge

Contract C3 headline: `taking named instruments from 15 of 55 to 55 of 55`.
Contract P-C3: `C3=unmet named=14 present=55 missing=41 extra=0`.
Contract C2 headline: `from 3 of 6`.
Contract P-C2: `survivors=2 killed=4 total=6`.

The lesson discloses those disagreements and uses frozen P-C2/P-C3 as the measurement authority. No contract edits or substitute counters. Receipt guard's textual binding is not semantic command relevance. Census rc 0 retains W04 warnings. No final claim verdict or landed revision observed by this seat.

## L1 placeholders (all named)

1. **LANDING PENDING**: final revision, three frozen-counter commands/output/exit codes and receipt paths.
2. **PIN PENDING — filled by the L1**: source report-backed S595 pin sha256.
3. **DUPLICATE RECEIPT PENDING**: durable source receipt path and exact pre-fetch sweep commands/results.
4. **GREEN RECEIPT PENDING**: C1 after-revision red-to-green command/output/rc and receipt.
5. **AFTER CENSUS PENDING**: after row count, landed tree/revision, census command/output/rc and receipt path.

Gate verdict is explicitly scoped; planned S595 admission does not assert a committed source row. The L1 should run the frozen final counters and its normal located-quote/word-label/census checks after integration; this seat has not exercised them.

## Own defects and limits

- Initially attempted `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show d58889220d3c6a18d461f2d31b5ab162ffef1e4e:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`. Git reported `fatal: path 'corpus/SOURCES.md' exists on disk, but not in 'd58889220d3c6a18d461f2d31b5ab162ffef1e4e'`; grep printed `0`, pipeline rc 1. That 0 is NOT a registry count. Corrected by running the assigned direct live-file count, which produced 367.
- Initial directory discovery used shell `ls -la` instead of the required specialized read/glob. No mutations resulted. Tool normalized the first listing unexpectedly; filed that behavior through `xd://report_issue`; no permissions inferred from it.
- Initial narrative preamble was unnecessary; subsequent work used tools directly.
- Source report absent, hence explicit authorized placeholders; no fabricated hash or landed evidence. No scratch tree exists to clean because none was created.

## Self-evaluation

Accuracy 4/5: inherited receipts and peer observations explicitly distinguished; final pin verification remains L1-owned. Completeness 4/5: requested scaffold complete, five authorized integration fields remain. Clarity 4/5: all requested sections ordered, with necessarily repeated pending evidence. Actionability 4/5: exact pending fields and frozen commands named; no landed revision yet. Conciseness 4/5: full census warning transcript makes report long but preserves negative results. Overall 4.0/5. Highest-impact next action: L1 reconcile the source report, then fill final landed receipts without upgrading planned outcomes. The user should agree this is a scaffold, not a passing-claims report.
