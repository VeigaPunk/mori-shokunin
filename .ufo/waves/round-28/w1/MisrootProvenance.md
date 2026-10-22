# MisrootProvenance — round 28 wave 1: the seven fleet-root files (read-only)

Seat: `MoriR28.MisrootProvenance` (leaf scout, read-only). Task: hash, size, mtime, identity and
upstream equality for the seven untracked files that stood at the fleet root `/home/vgpnk/Projects/shokunin`,
the mori round-27 seat report(s) that name each source or hash, whether any OTHER lane's report names
them, and a per-file verdict. Nothing was moved, edited or deleted by this seat.

Tools: none installed or upgraded (`~/.omp/agent/RULES.md`, 14 lines, read); no pacman, no `jj`, no git
writes, read-only `git status` only. Skill `godspeed` read at `/home/vgpnk/.agents/skills/godspeed/SKILL.md`.
Upstream bytes were fetched with `curl` into my own scratch
`/fast/scratch/hyaku/mori-r28/MisrootProvenance/` (ordinary public raw URLs, no challenge bypass).

## 0. State change during this seat (L1 acted at 18:01Z)

Per the L1 note, the seven files were copied byte-exact into the lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin/` and deleted from the fleet root. This seat verified both ends:

- Every lane-root file has the same sha256, size and mtime to the nanosecond as the fleet-root copy I
  measured before the move (`stat -c '%s|%y'`, `sha256sum`, command in §2 table).
- `git -C /home/vgpnk/Projects/shokunin status --porcelain` (23 lines) contains no entry matching any of
  the seven names (grep for `(^|/)(base\.c|oom_kill\.c|MANPAGE\.md|main\.c|meminfo\.c|sd-main\.c|user@\.service\.in)$`
  printed nothing). The fleet root is clean of them.

## 1. What the seven are — identity, size, mtime, upstream equality

All seven carried mtimes inside one 70 ms window, `2026-10-22 14:08:55.279…` to `.349… −03:00`
(= `17:08:55Z`), i.e. one write batch, not edits. Upstream comparison is sha256 of the bytes I fetched.

| Fleet-root name | size | mtime (−03:00) | sha256 | First lines that identify it | Byte-for-byte upstream URL (my fetch sha256 = file sha256) |
|---|---|---|---|---|---|
| `base.c` | 98196 | 14:08:55.322125789 | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | `:1` `// SPDX-License-Identifier: GPL-2.0`; `:3` `*  linux/fs/proc/base.c`; `:8` `*  proc base directory handling functions` | `https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c` — HTTP 200, 98,196 B, sha equal |
| `oom_kill.c` | 34311 | 14:08:55.302125721 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | `:1` `// SPDX-License-Identifier: GPL-2.0-only`; `:3` `*  linux/mm/oom_kill.c`; `:5` `*  Copyright (C)  1998,2000  Rik van Riel` | `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` — HTTP 200, 34,311 B, sha equal |
| `MANPAGE.md` | 10114 | 14:08:55.279125643 | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | `:1` `% earlyoom(1) | General Commands Manual`; `:3` `# NAME`; `:5` `earlyoom - Early OOM Daemon` | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md` — HTTP 200, 10,114 B, sha equal |
| `main.c` | 21053 | 14:08:55.311125751 | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | `:1` `// SPDX-License-Identifier: MIT`; `:3` `/* Check available memory and swap in a loop and start killing`; `:4` ` * processes if they get too low */` | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` — HTTP 200, 21,053 B, sha equal |
| `meminfo.c` | 8344 | 14:08:55.286494373 | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` | `:1` `// SPDX-License-Identifier: MIT`; `:3` `/* Parse /proc/meminfo`; `:4` ` * Returned values are in kiB */` | `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c` — HTTP 200, 8,344 B, sha equal; **also equal at v1.8.2** (same sha, same size), so the tag is not pinned by bytes alone |
| `sd-main.c` | 180617 | 14:08:55.349125880 | `5ecdca43a8e0ed088758b228b54c72df311c0b9dc3855721ed02c5b169d3aae3` | `:1` `/* SPDX-License-Identifier: LGPL-2.1-or-later */`; `:3` `#include <fcntl.h>`; `:4` `#include <linux/oom.h>`; `:5` `#include <linux/vt.h>` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/main.c` — HTTP 200, 180,617 B, sha equal (v261 differs: `17316de7…`, 174,797 B) |
| `user@.service.in` | 1315 | 14:08:55.315557133 | `72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c` | `:1` `#  SPDX-License-Identifier: LGPL-2.1-or-later`; `:3` `#  This file is part of systemd.`; `:5` `#  systemd is free software; you can redistribute it and/or modify it` | `https://raw.githubusercontent.com/systemd/systemd/v262/units/user@.service.in` — HTTP 200, 1,315 B, sha equal; **also equal at v261** (unchanged file), so tag slack exists here too |

Fetch receipts (all in one batch, `curl -s -o`):

- Access time: the batch ran 2026-10-22T17:57Z–18:00Z; `date -u +%FT%TZ` printed `2026-10-22T17:59:28Z`
  at the end of the systemd call. The kernel `v7.2` fetches in the same batch returned HTTP 200 with the
  hashes above; rate-limited side fetches (`v7.1`/`v6.18`/`master` at `raw.githubusercontent.com`) returned
  HTTP 429 with a 313-byte error body — irrelevant, the `v7.2` bytes already matched exactly.
- The `earlyoom v1.9.0` fetches (`MANPAGE.md`, `main.c`, `meminfo.c`) and `systemd v262`
  (`src/core/main.c`, `units/user@.service.in`) returned HTTP 200 with the hashes above.
- One later re-fetch of `linux/v7.2/mm/oom_kill.c` (second batch, immediately after; unstamped) returned the
  same `452f1348…` and 34,311 B.

## 2. Which mori round-27 seat report names each source or hash

`grep -rIl` per file name under `mori-shokunin/.ufo/waves/round-27/` and `grep -rn` per full/truncated
sha256. Naming seats are wave-1 source seats plus wave-2 seats that re-fetched, and the wave-2 misroot
sweep that named all seven at once.

| File | r27 report(s) naming it, with line |
|---|---|
| `base.c` | `w1/SrcProcBaseOomScore.md:30` (URL, access 15:46:35Z, 98,196 B), `:126`, `:135` (row S127); `w1/CriticInheritProbe.md:99` (full sha); `w2/ReopenS127.md:29` (access 17:09:49Z, full sha); `w2/CriticSkillWrongTurn.md:21` (full sha); `w2/ScoutMisroot.md:37` (short sha + root name) |
| `oom_kill.c` | `w1/SrcKernelOomBadness.md:14` (full sha), `:98` (row S003 URL); `w1/SrcProcBaseOomScore.md:33`, `:142`; `w1/ConnSiblingOverlap.md:30` (short sha); `w2/CriticSkillWrongTurn.md:20` (full sha); `w2/ScoutMisroot.md:38` |
| `MANPAGE.md` | `w1/SrcEarlyoomManpageOptions.md:124` (URL + full sha); `w2/CriticSkillWrongTurn.md:19` (full sha); `w2/CriticC1Novelty.md:153` (short); `w2/CriticEntryOverclaim.md:10` (short); `w2/ScoutMisroot.md:39` |
| `main.c` | `w1/SrcEarlyoomMainCSelf.md:88` (full sha); `w1/HostUnitOomAdjust.md:171` (full sha); `w1/ReviewS117.md:27` (full sha); `w2/CriticC1Novelty.md:151` (short); `w2/CriticSkillWrongTurn.md:17` (full sha); `w2/ScoutMisroot.md:40` |
| `meminfo.c` | `w1/SrcKillCSelection.md:63,66,71-76,106` (file and line anchors, no whole-file hash); `w2/CriticC1Novelty.md:152` (short sha); `w1/ScoutDeadSeatCorrelation.md:210` (full sha); `w2/CriticSkillWrongTurn.md:18` (full sha); `w2/ScoutMisroot.md:41` |
| `sd-main.c` | **only** `w2/ScoutMisroot.md:42` carries the local name `sd-main.c`. The systemd bytes under it are named as `src/core/main.c`: `w1/HostUnitOomAdjust.md:172` (full sha), `w1/CriticInheritProbe.md:109` (full sha), `w2/CriticEntryOverclaim.md:11` (short), `w2/CriticC1Admission.md:54` (short) |
| `user@.service.in` | `w1/SrcSystemdUserService.md:21` (URL + full sha), `:129`; `w1/CriticInheritProbe.md:108` (URL + full sha); `w2/CriticC1Admission.md:54` (short); `w2/ScoutMisroot.md:43` |

The round-27 sweep itself, `w2/ScoutMisroot.md:30-52`, lists all seven with short hashes, row ids and
byte-identical scratch copies (`cmp -s` on each), and states at `:51-52` that which seat left them is
**unresolved** under the bounds. It also dates them "14:08:55 −03:00" (`:32`).

## 3. Other lanes — do any of their reports name these files?

Method: all 20 sibling lanes, `find '*/.ufo/waves' -type f -newermt '@1792685335' ! -newermt '@1792692535'`
(the file mtime ± 1 h, i.e. 2026-10-22T16:08:55Z to 18:08:55Z), then a name grep over the 200 wave files that
fell in that window. Also a sha256-prefix grep over every sibling lane's `round-27` tree.

- Files in window (counted from the first 200 `find` lines, so a lower bound): tsukuroi 96, kumitate 45,
  kotoba 41, kaidoku 13, kake 4, fleet `.ufo` 1.
- The name grep over the window was uncut (`grep -rIl` then a per-path mtime filter); of the whole window,
  exactly two files name any of the seven:
  1. `tsukuroi-shokunin/.ufo/waves/round-27/w2a2/RevSeatScope.md:13` (mtime 17:59:00Z) lists
     `MANPAGE.md, base.c, main.c, meminfo.c, oom_kill.c, sd-main.c, user@.service.in` among 13 untracked
     fleet-root paths, and records that a grep of every untracked file for `tsukuroi|round.?27|r27`
     "returned no matches — zero misroots naming tsukuroi round 27". So the other lane **observed and
     disowned** them; it does not claim authorship.
  2. `tsukuroi-shokunin/.ufo/waves/round-27/w2a2/ConnMoriHeadDrift.md:20` matches only because it cites
     mori's own `main.c:245-…` anchor for the entry — not a fleet-root copy.
- Hash grep over sibling `round-27` trees: `cc48b02e/08656b0b/526e512c` appear only inside a vendored copy of
  mori's own corpus, `tsukuroi-shokunin/.ufo/waves/round-27/siblings/mori/corpus/knowledge/userspace-oom-killers-r26.md`
  (28,496 B, mtime 12:56:35 −03:00 = 15:56:35Z, before the batch) — i.e. mori's bytes seen through a
  recursive export, not an independent tsukuroi claim. `cef1a2cf/452f1348/5ecdca43/72c2f40d` appear in no
  sibling lane's round-27 tree.
- Wider full-tree hash scan (all lanes, all waves, name-and-hash, per-lane `timeout 25`): the same **public
  upstream** hashes are cited independently by tsukuroi's older rounds — `452f1348` (mm/oom_kill.c) in
  `tsukuroi-shokunin/.ufo/waves/round-25/w1/SrcKernelOomCounter.md` (07:23:37Z) and five more r25 files plus
  r26 `RevAppendOnly/SOURCES-*.md` (12:24:52Z); `08656b0b` (earlyoom main.c) and `526e512c` (meminfo.c) in
  tsukuroi r25/r26 source and review files 07:25–12:24Z; `72c2f40d` (user@.service.in) in
  `tsukuroi-shokunin/.ufo/waves/round-25/w1/CritC2Rows.md` (07:25:51Z). `5ecdca43` (systemd src/core/main.c)
  and `cef1a2cf` (fs/proc/base.c) appear in **no** sibling lane at all (whole-tree scans; every hit is mori's
  own r26/r27/r28). All of these are 4 h 44 min to 9 h 45 min before the 17:08:55Z batch, name public
  upstream sources rather than a fleet-root copy, and fall outside the ±1 h window — naming a public source's
  hash is not authorship of a local copy.
- Round-28 side: `mori-shokunin/.ufo/waves/round-28/evidence/misroot-before.txt` (18:01:16Z) carries all seven
  hashes — the L1's pre-move snapshot, which corroborates the set but is not a producer claim. This wave's
  `w1/ScoutSurfaceRecon.md` (18:02:26Z) names `cef1a2cf`, i.e. the round-28 recon seat, also after the batch.
- The generic lane-wide name grep (`base.c`, `main.c`, `meminfo.c`…) hits dozens of unrelated older rounds in
  chousa, kagi, mado, lore, etc.; none of those files falls in the ±1 h window and none names `sd-main.c`
  or `user@.service.in`. They are other projects' own `base.c`/`main.c`.

**No other lane's report claims these files.** The only sibling lane that names the fleet-root copies is
tsukuroi's `RevSeatScope.md:13`, and it disowns them; sibling lanes that cite the same public upstream hashes
(tsukuroi r25/r26, 4 h 44 min or more earlier) are citing upstream sources for their own rows, not a local copy.

## 4. Verdict per file, with the producer evidence

Producer evidence gathered here:

1. One batch at 17:08:55Z, seven files, 70 ms (mtimes in §1) — a copy loop, and the local names are the
   upstream basenames except the systemd pair. `sd-main.c` is a **local rename** (upstream
   `src/core/main.c`); the shared wave-1 scratch root already held
   `/fast/scratch/hyaku/mori-r27/sd-main.c` (180,617 B, mtime 15:53:01Z) and `/fast/scratch/hyaku/mori-r27/base.c`
   (98,196 B, 15:47:24Z). The fleet-root set reuses that rename, so it descends from the r27 scratch tree,
   not from an independent download.
2. The only seat scratch write inside the same millisecond window is
   `/fast/scratch/hyaku/mori-r27/CriticSkillWrongTurn/kill.c` (21,169 B, mtime `14:08:55.280125646 −03:00`,
   one millisecond after fleet-root `MANPAGE.md` at `.279125643`). That seat's scratch then received
   `main.c 17:09:02.979`, `MANPAGE.md .995`, `meminfo.c 17:09:03.010`, `base.c .031`, `oom_kill.c .048`,
   `sd-main.c 17:09:03.279`, `user@.service.in .293` — all seven hashes identical to the seven
   (`sha256sum` in that directory; e.g. `base.c cef1a2cf…`, `sd-main.c 5ecdca43…`). Its report
   `w2/CriticSkillWrongTurn.md:12` says "Sources opened (curl on public raw URLs, 2026-10-22T17:09:03Z,
   bytes under the seat scratch dir)" and lists those hashes at `:17-21`.
3. No other wave-2 seat scratch shows writes at 17:08:5x: `find /fast/scratch/hyaku/mori-r27 -type f
   -newermt '@1792688925' ! -newermt '@1792688945'` printed only
   `ReviewPrivacyLanded/changed-files.txt` (17:08:51Z) and `CriticSkillWrongTurn/kill.c` (17:08:55.280Z).
   The re-fetch batches of `CriticCeilingInference` (17:09:32Z) and `CriticC1Admission` (17:10:19Z, `f/`
   with `S127_base.c` etc.) are later and stayed in scratch.

[INFERENCE] The batch is a first attempt by `MoriR27.CriticSkillWrongTurn` that wrote to the fleet root (one
output, `kill.c`, resolved to its absolute scratch path), followed by its documented 17:09:02–03Z re-fetch
into scratch. The command line, pid and cwd are not observable to this seat (privacy bound; ScoutMisroot
recorded that no process held these files open at scan time, `w2/ScoutMisroot.md:50`).

| File | Verdict | Confidence |
|---|---|---|
| `base.c` | mori round-27 seat (wave-2 batch, 17:08:55Z; same bytes as r27 S127 captures, named with full sha at `ReopenS127.md:29`, `CriticInheritProbe.md:99`, `SrcProcBaseOomScore.md:30`) | high for r27; producer seat CriticSkillWrongTurn medium-high |
| `oom_kill.c` | mori round-27 seat (r27 S003; full sha at `SrcKernelOomBadness.md:14`; scratch copy `SrcKernelOomBadness/oom_kill.c`) | high / medium-high |
| `MANPAGE.md` | mori round-27 seat (r27 S115; full sha at `SrcEarlyoomManpageOptions.md:124`; 1 ms from CriticSkillWrongTurn's kill.c) | high / medium-high |
| `main.c` | mori round-27 seat (r27 S119; full sha at `SrcEarlyoomMainCSelf.md:88`, `HostUnitOomAdjust.md:171`) | high / medium-high |
| `meminfo.c` | mori round-27 seat (r27 S116; full sha at `CriticC1Novelty.md:152`, `ScoutDeadSeatCorrelation.md:210`; 5+ wave-1 scratch dirs hold it) | high / medium-high |
| `sd-main.c` | mori round-27 seat (systemd v262 `src/core/main.c`, r27 S130; full sha at `HostUnitOomAdjust.md:172`, `CriticInheritProbe.md:109`; the local name appears only in `ScoutMisroot.md:42`) | high / medium-high |
| `user@.service.in` | mori round-27 seat (r27 S130; full sha at `SrcSystemdUserService.md:21`, `CriticInheritProbe.md:108`) | high / medium-high |

No file is attributable to another lane. None is "unknown" in the sense of an outside producer: all seven
are public upstream bytes captured by mori's own round-27 seats, and the r27 sweep plus this report pin the
batch to the wave-2 window.

## 5. Remaining unknowns

- Exact seat identity for the batch: **not observed**, only the millisecond fingerprint above. The r27 sweep
  itself left it unresolved (`ScoutMisroot.md:52`) for the same bound (no pid/command-line read-out).
- `meminfo.c` cannot be pinned to v1.8.2 vs v1.9.0 by bytes (identical); the r27 row S116 records v1.9.0.
  `user@.service.in` is identical in v261 and v262; S130 records v262.
- Whether the wave-2 seat still needs the copies: no; all seven are byte-identical to its own scratch copies.

## 6. Privacy and bounds

No uid, pid, `user-<digits>` slice/service name, unit name of this host, journal `MESSAGE` text, earlyoom
`/etc/default` or `--prefer/--avoid/--ignore` value is reproduced here. Only counts, states, versions,
hashes, sizes and mtimes. No fleet file was written except this report; scratch writes stayed in
`/fast/scratch/hyaku/mori-r28/MisrootProvenance/`.

## 7. Ready-to-paste summary for the round-28 record

```text
misroot r27, seven files at fleet root, batch mtime 2026-10-22T17:08:55Z (14:08:55 -03:00), moved by L1 at 18:01Z:
base.c cef1a2cf = linux v7.2 fs/proc/base.c
oom_kill.c 452f1348 = linux v7.2 mm/oom_kill.c
MANPAGE.md cc48b02e = earlyoom v1.9.0 MANPAGE.md
main.c 08656b0b = earlyoom v1.9.0 main.c
meminfo.c 526e512c = earlyoom v1.9.0 meminfo.c (identical at v1.8.2)
sd-main.c 5ecdca43 = systemd v262 src/core/main.c
user@.service.in 72c2f40d = systemd v262 units/user@.service.in (identical at v261)
producer: mori round-27 wave-2 seat; fingerprint ties it to MoriR27.CriticSkillWrongTurn (its kill.c, 1 ms away,
plus its 17:09:02-03Z scratch copies of all seven); exact seat not observed (bounds).
other lanes: none claim them; tsukuroi w2a2/RevSeatScope.md:13 lists all seven as untracked debris and disowns.
```
