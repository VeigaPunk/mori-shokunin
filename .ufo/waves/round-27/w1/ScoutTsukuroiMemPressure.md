# Scout — tsukuroi `memory-pressure-r25.md` against C1 victim-selection ground

Seat: MoriR27.ScoutTsukuroiMemPressure (leaf). Question: does the sibling file teach
anything about OOM victim choice, `oom_score`, or earlyoom options, and does mori's S125
need a new anchor (used-by change) rather than a new SOURCES row for C1?

## Source pin (observed)

- Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 157ee255:corpus/knowledge/memory-pressure-r25.md`
- Result: blob `be3065ae512f3fefec115a23c0e8fee2cbca9fc4`, 392 lines, 27,828 bytes,
  sha256 `ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25`.
- These equal the three identifiers mori `corpus/SOURCES.md:131` (S125) records: blob
  `be3065ae…`, "entry bytes sha256 ecafdcdd… (27,828 B)". This re-reading produced no new
  bytes, so it is a re-opening of an already-registered file.

## Answer

**C1 needs neither a new SOURCES row nor a new anchor on S125.** The file contains no
statement about kernel or earlyoom victim choice and no `oom_score`/`oom_score_adj`
content at all. Its only named earlyoom option is `--kernel-oom` (line 382), and that
sentence itself attributes the fact to mori's own
`corpus/knowledge/oom-kill-counter-kernel-only-r12.md`. S125's declared scope also says
the file is "not a primary source for any systemd, earlyoom or kernel fact"
(`corpus/SOURCES.md:131`), so resting any C1 fact on it would both mis-anchor and
contradict the row's scope.

If the L1 nevertheless decides to cite the file, the only correct registry change is a
**used-by anchor** on S125 (append `corpus/knowledge/oom-victim-selection-r27.md` to its
used-by and, optionally, the cited line range to its anchor column) — never a new row.
It would not help C1's counter: `count-c1.sh` counts only ids with `num >= 127`
(`.ufo/waves/round-27/count-c1.sh`, `MIN_ROW=127`). Recommendation: leave S125 unchanged.

## Occurrence counts in the file (observed, `grep -cF`)

| term | count | note |
|---|---|---|
| `oom_score` | 0 | no occurrence |
| `OOMScoreAdjust` | 0 | no occurrence; every `Adj` hit is the province row name `ADJ-04` (lines 1, 39, 369) |
| `--prefer` | 0 | — |
| `--avoid` | 0 | — |
| `--ignore` | 0 | — |
| `sort-by-rss` | 0 | — |
| `memory.oom.group` | 0 | — |
| `victim` | 0 | the word does not occur |
| `earlyoom` | 10 lines | lines 1, 40, 41, 217, 324, 325, 326, 364, 382, 387; line 1 and part of 387 are the capture file name `capture-earlyoom.txt`, not statements about earlyoom |
| `kernel-oom` | 1 | line 382 only |

## Every statement that touches the killer (line numbers in the pinned file)

| lines | statement | bearing on C1 |
|---|---|---|
| 40-42 | "The frozen capture never read earlyoom. The supplementary read-only capture shows `earlyoom.service` active and enabled on this host." | Presence only. Matches mori's own held ground; no selection facts. |
| 202-203 | "an `auto` unit becomes a kill candidate only when an ancestor … systemd-oomd monitors only cgroups whose units carry `kill`." | systemd-oomd candidate semantics, not kernel/earlyoom victim choice; systemd-oomd is inactive here (line 204). |
| 204 | "On this host systemd-oomd is inactive and disabled" | Already cited by mori's round-26 material (S125 row teaches field); not a C1 fact. |
| 217 | "(earlyoom is active and enabled on this host)" | Presence only, inside an operator-action sentence. |
| 317-318 | "A userspace killer's SIGKILL moves neither counter, so the kernel counter reads zero even when a userspace killer has killed something." | Kill accounting, not victim choice. |
| 324-326 | "an earlyoom kill would not move the kernel counters" (with the same presence line at 325) | Accounting, not selection. |
| 364-365 | "earlyoom is active and enabled on this host (supplementary read-only capture, context only)" | Presence only. |
| 382 | "A userspace killer moves neither kernel counter unless it asks the kernel to kill: earlyoom with `--kernel-oom` does" … "The captures did not read earlyoom's arguments." | The only earlyoom option named; the fact is attributed to mori's `oom-kill-counter-kernel-only-r12.md`. Not a selection option. |
| 387 | "A monitored `kill` unit's leaf cgroups, not the unit itself, are the kill candidates" | systemd-oomd cgroup granularity, not per-process victim choice. |
| 389 | "the selected cgroup is killed with all its descendants (`oomd-util.c` line 366)" | systemd-oomd whole-cgroup kill; contrast with per-process choice at best, and not a C1 primary source. |
| 392 | "S127 supersedes S125 (mori facts F2, F9 system half, F10; blob `d4ccce42`)" | tsukuroi's own registry numbering; see disambiguation below. |

Nothing else in the file names a process, score, priority or selection rule.

## S125 registry row as it stands (observed)

- `corpus/SOURCES.md:131`: tier B, status `mined`, opened `2026-10-22`, recheck `90d`.
- used-by: `corpus/knowledge/userspace-oom-killers-r26.md` (the only entry).
- anchor column: MP4 "lines 196-232", "How to read this entry" > "Userspace killers"
  (lines 40-42), "What this entry does not claim" (lines 363-367), wave-2 corrections
  block line 387.
- scope column: "not a primary source for any systemd, earlyoom or kernel fact, not
  mori's own host capture, and not a host-wide unit census".
- URL in the row is the tsukuroi GitHub raw URL at commit 157ee255; the blob sha256 it
  records is the same blob read here, so the row's pin is intact.

### Anchor or new row

- New row: wrong under the contract's own rule. The file already has a row (S125) at the
  identical blob and bytes; re-opening it "adds an anchor to that row, not a new row".
- Anchor (used-by change): correct form if and only if the new entry cites the file. That
  means editing S125's used-by to add `corpus/knowledge/oom-victim-selection-r27.md`;
  no id, URL, digest or scope changes.
- C1 necessity: no. The claim needs (a) kernel/earlyoom victim-selection rules, (b) the
  host `oom_score_adj` of fleet processes, (c) attribution of earlier-boot sends. All
  three are absent from this file. The presence statement at lines 40-42/364-365 is
  already held by mori from its own rows and the round-26 entry, and the `--kernel-oom`
  fact at line 382 is explicitly mori's (`oom-kill-counter-kernel-only-r12.md`).

## Disambiguation: the "S127 supersedes S125" note at line 392 is not mori's S125

- Observed: blob `d4ccce42` in the tsukuroi repo hashes to mori's
  `corpus/knowledge/system-pressure-r24.md` at mori commit `4f05dd5a`
  (`git rev-parse 4f05dd5a:corpus/knowledge/system-pressure-r24.md` →
  `d4ccce4262d8224e362da65eb5ba4b851ad0fea2`; blob sha256 of `d4ccce42` =
  `5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5`).
- Therefore line 392 talks about tsukuroi's own registry ids for mori's PSI file; it does
  not supersede mori's S125 and does not change the pin on this file. [INFERENCE] tsukuroi's
  S125 was an earlier reading of mori's `system-pressure-r24.md`; only the S127 blob
  identity above was observed.
- Practical rule for C1: do not let the string "S127 supersedes S125" in the sibling file
  collide with mori's round-27 ids S127+. They are different registries.

## What C1 still needs from other seats (not this file)

- Kernel victim choice: `oom_score`/`oom_badness`, `oom_score_adj`, `memory.oom.group` —
  Linux v7.2 `mm/oom_kill.c`, `fs/proc/base.c`, cgroup-v2 docs.
- earlyoom choice: `--prefer`/`--avoid`/`--ignore`, `--sort-by-rss`, staged SIGTERM/SIGKILL
  — earlyoom v1.9.0 sources/MANPAGE at tag 202d4db0.
- Host values: fleet processes' `oom_score_adj`, and send attribution from earlier boots.

## Commands and evidence

```
git -C .../tsukuroi-shokunin show 157ee255:corpus/knowledge/memory-pressure-r25.md | sha256sum
  → ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25  -
git -C .../tsukuroi-shokunin rev-parse 157ee255:corpus/knowledge/memory-pressure-r25.md
  → be3065ae512f3fefec115a23c0e8fee2cbca9fc4
wc -c → 27828
grep -cF 'oom_score' / 'victim' / '--prefer' / '--avoid' / '--ignore' / 'sort-by-rss' /
  'memory.oom.group' / 'OOMScoreAdjust' → 0 each
git -C .../mori-shokunin rev-parse 4f05dd5a:corpus/knowledge/system-pressure-r24.md
  → d4ccce4262d8224e362da65eb5ba4b851ad0fea2
```

- Tooling: no install or upgrade was made by this seat.
- No lane write was made except this report; no jj, no git write, no service action.

## Remaining unknowns

- None blocking this question. The file was read in full (392 lines); the zero counts are
  exhaustive for the pinned bytes. Whether mori's S125 should gain an anchor later is a
  policy call for the L1, answered above: not needed for C1.
