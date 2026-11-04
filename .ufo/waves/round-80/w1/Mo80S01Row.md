# Mo80S01Row — round 80 w1 source registry/index

Axes: calibration, operability, coverage. This seat supplies source provenance and discoverability for C2; it does not claim a C1/C2/C3 execution verdict or score change.

## 1. Behavior and touched surfaces

Appended the unused id **S595** as the final registry row, before `## Paths`, at `corpus/SOURCES.md:376`. Appended the round-80 three-column index at `corpus/README.md:867-871`. No product code or frozen counter edited.

Exact source row bytes (UTF-8, newline terminated):

```text
| S595 | Practical Mutation Testing at Scale — arXiv:2102.11378v2 — https://arxiv.org/abs/2102.11378v2 | paper | A | mutation analysis's own definition as a test-adequacy criterion, limited to what the abstract states | abstract sentence at :121 (`grep -n 'Mutation analysis assesses' corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html`); sha256 28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884; copy corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html; 43884 bytes, 613 lines | Measuring detection of systematically seeded artificial faults exposes test-suite adequacy gaps that a green unmutated run alone does not measure. | mined | 2026-11-04 | 365d | corpus/knowledge/mutation-adequacy-r80.md |
```

Exact index row bytes:

```text
| Mutation analysis as a test-adequacy criterion (r80, S595) | `knowledge/mutation-adequacy-r80.md` (S595; `corpus/knowledge/mutation-adequacy-r80.md`) | The paper's abstract defines adequacy through detection of systematically seeded artificial faults, grounding C2's frozen mutant-killing criterion; the source does not establish that a green selftest or killing six selected mutants proves general adequacy. |
```

## 2. Provenance commands and observed output

Commands below ran with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`; paths are absolute unless clearly shown as literal row content.

The regex-tool search `S595|2102\\.11378|Mutation Testing at Scale` over the entering `corpus/SOURCES.md` returned `No matches found`; S594 was the last row. No fallback id was needed. The scout reported an independent pre-fetch duplicate sweep; this seat does not claim to have fetched or independently reopened the live page.

```sh
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
28ea1f163860348979a3aa9e9ef8e00fc8eb3ecec2762782d639783003f1b884  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
$ wc -lc /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
  613 43884 /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
```

Both commands exited successfully. The hash was printed, not inferred or copied unseen.

```sh
$ grep -n 'Mutation analysis assesses' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r80/arXiv-2102.11378v2-abs.html
```

Successful output matched lines 28, 32, 39 (metadata) and 121 (the abstract). The tool display truncates long HTML lines, so no full-line output is invented here. A separate regex-tool read restricted to `:121-121` displayed this contiguous sentence on line 121:

```text
Mutation analysis assesses a test suite&#39;s adequacy by measuring its ability to detect small artificial faults, systematically seeded into the tested program.
```

The row points to the abstract occurrence, not the metadata copies. Evidence is pin-relative; no claim of current live-page identity or full-paper reading.

## 3. Required census commands

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
0
```

Exit 0. The added row has eleven cells, with no embedded literal pipe.

```sh
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

Initial run exited 1: the expected 35 W04 duplicate-URL/across-scope warning lines, followed by the exact error:

```text
mori	E11	S595 missing used-by corpus/knowledge/mutation-adequacy-r80.md
```

The dependency belongs to Mo80S02Entry; notified that owner without creating a placeholder or weakening used-by.

## 4. Limits, defects and out-of-scope

Own process defect: initial census ran before the sibling-owned knowledge entry existed. The honest E11 result exposed the ordering dependency; it was not a passing gate. Initial report/pin lookup also returned not found while the source scout was still working; this seat waited for observed pin bytes and measured them before editing.

Tier A is limited to the abstract's own definition, not empirical sufficiency of this counter, equivalent-mutant handling, or Python implementation correctness. No round mutation harness, claim sweep, inventory counter, build, general battery, commit, publication, deployment, OS change, or other agent runtime was invoked. No scratch directory or tool installation was created by this seat.

Self-evaluation: accuracy 4 (pin read, not live re-open); completeness 5 (both rows and required censuses delivered, dependency failure resolved below); clarity 4 (long row required by schema); actionability 4 (exact rows and commands supplied, integration judgment remains Main's); conciseness 4 (preserves initial failure rather than hiding it). Overall 4.2. Improvement applied: waited for the real used-by target, then ran the required census successfully. Would the user agree? Evidence is explicit; no round-level judgment is asserted.

Artifact: `.ufo/waves/round-80/w1/Mo80S01Row.md`.

## 5. Final census after the owned dependency landed

Mo80S02Entry reported the knowledge entry written; the required census then returned the following exact output (35 tolerated W04 warnings, no E11). This is a dependency-resolution run, not a rerun to decorate the report.

```sh
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; printf 'census_rc=%s\n' "$?"
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
census_rc=0
```

Gates: row-shape census 0 malformed rows, exit 0; final source census exit 0, 35 tolerated W04 warnings. No claim that these formatting/provenance checks prove C2's mutant-killing predicate. No known unresolved defect in this seat's owned rows.
