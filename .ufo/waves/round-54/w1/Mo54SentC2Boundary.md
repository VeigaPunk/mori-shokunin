# Mo54SentC2Boundary — boundary review of the C2 entry and the C1 ledger (round 54, w1)

Seat: boundary review of `corpus/knowledge/memory-failure-kills-r54.md` and
`corpus/knowledge/kernel-v7.3-recheck-r54.md` at `78295c764093ff1f6cee08d7246679900bde7265`.
Assigned questions: (a) does any sentence advise or imply writing a sysctl, injecting or unpoisoning memory,
loading hwpoison-inject, or grepping kernel text as a count (QUALITY 15); (b) are the host reads in the entry and in
`.ufo/waves/round-54/evidence/sweeps.txt` read-only; (c) do the Boundaries hand host repair to tsukuroi/operator as
`PROVINCE.md` Adjacent requires. Detection and report only: I ran no host write, no module load, no counter, and no
git mutation.

## 1. Bytes reviewed (so the line numbers below resolve)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git log --oneline -6
2d0347a3 round-54: wave w1 spec (74 seats, v2 validated: 24 voters, 39 attack seats), dispatch payload, at-data receipts
78295c76 round-54: data correction before any seat — C2 row 1 reworded and decision-table counting note (QUALITY 15: ...)
1116c092 round-54: data — C1 ledger ... C2 entry ... ; D3 lane-root strays relocated under rounds 28/38
6830f3af round-54: freeze — contract, counters ...
```

```
$ git rev-parse 78295c76:corpus/knowledge/memory-failure-kills-r54.md 78295c76:corpus/knowledge/kernel-v7.3-recheck-r54.md
75fefb794fd3cd48e2f478aa60fbd5693f167804
6104f174a91ee3d2ba57a5401c8094e96ed15c15
$ git hash-object corpus/knowledge/memory-failure-kills-r54.md corpus/knowledge/kernel-v7.3-recheck-r54.md
75fefb794fd3cd48e2f478aa60fbd5693f167804
6104f174a91ee3d2ba57a5401c8094e96ed15c15          (exit 0)
$ git diff --stat 78295c76..HEAD -- corpus/knowledge | cat
(no output; exit 0)                                  # HEAD 2d0347a3 adds the wave spec only
```

Working-tree bytes of both files equal the data commit's bytes, so the line numbers below are the reviewed revision's
line numbers. Entry length 86 lines; ledger length 109 lines (`wc -l`, exit 0).

Source provenance cross-check the entry asserts at its line 3:

```
$ sha256sum corpus/evidence/sources-r54/memory-failure.c.v7.3
94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003   (exit 0)
```

Matches the entry's `sha256 94d24a605b61…`. The four knobs are one table registered under "vm"
(`corpus/evidence/sources-r54/memory-failure.c.v7.3:134-171`, registration at `:2710`
`register_sysctl_init("vm", memory_failure_table)`), all `mode = 0644`.

## 2. Question (a) — sysctl writes, injection, unpoisoning, module load, text counts

**Answer: no sentence in either file advises or implies a write, an injection, an unpoison, a module load, or a
text-based count.** The complete set of places either file touches a knob or a kernel line:

| location | text at issue | read as |
|---|---|---|
| entry:7 | `recheck: on-release — re-fetch the six files at the new tag and re-run count-c2.py; on this host, re-read …` | network read + file read; no write |
| entry:35 | `the panic switch … is off unless set` | describes the guard `if (!sysctl_panic_on_unrecoverable_mf) return false;`; no instruction |
| entry:38 | `With recovery switched off, no process is killed …` | restates the S522 sentence (quoted in the same row); describes behaviour |
| entry:63-67 | table header `sysctl (v7.3) \| value → behaviour` and three rows | value→behaviour description, not an operator recipe |
| entry:69-73 | `On this host (read-only, 2026-10-27)` plus five values | reads only |
| entry:76-80 | `Detection and report only. Mori never injects poison (madvise(MADV_HWPOISON)`, the hwpoison-inject debugfs files the documentation lists for testing), never unpoisons a page and never writes a memory-failure sysctl; those are host-repair actions (tsukuroi / operator ground).` | explicit prohibition; see F7 for its enumeration width |
| entry:49-51 | `The lines are kernel text with no MESSAGE_ID, so a tally of them is a text-selected record count, never a structured count (QUALITY 15).` | correct QUALITY 15 discipline |
| ledger:105-108 | `memory.pressure and io.pressure are now documented "read-write" … the files always accepted PSI trigger writes, round 24's F8` | documentation drift record; no instruction (F6) |

Command check for imperatives (advice verbs) in both files:

```
$ grep -nE "\b(set|enable|turn|switch|toggle|should|must|run|execute|invoke)\b" <entry> <ledger>
entry:7, entry:35, entry:38; ledger:26, ledger:28, ledger:43, ledger:51     (exit 0)
```

Every hit is either the `recheck:` recipe (a read), a quoted kernel string, or the word `set` inside a claim's
source quote. No hit is an operator instruction.

QUALITY 15 ground: `corpus/QUALITY.md:29` — "A journal class is counted by MESSAGE_ID or another trusted structured
field, never by message text." The entry states the same rule for this class at entry:49-51, and the three rows that
point at kernel lines (55, 57, 60) are attribution rows ("which process", "was 1", "the host went down"), not counts.
Row 32 ("a parser can classify every recovery line exactly") is classification; the counting instruction for the
same row is the counter column at entry:57 and the preamble at 49-51. Residual risk is F1.

The ledger performs no host read at all (`grep -n "host\|live\|read live\|on this host"` → no output, exit 1); its
only live-surface prose is the PSI documentation drift at 105-108. All 31 dispositions read `holds`, which is the
voters' ground, not mine.

## 3. Question (b) — are the host reads read-only

**Entry:** lines 69-73 read exactly five sysfs counters, `HardwareCorrupted`, and four `/proc/sys/vm` names. No
write path, no `sysctl -w`, no `echo >`, no `/sys/devices/system/memory` write, no `madvise`, no debugfs.

**sweeps.txt:** the host block is lines 19-30:

```
19:$ uname -r; host memory-failure surfaces (read-only)
20:7.2.11-arch1-1
21:/sys/devices/system/node/node0/memory_failure/delayed:0
...
25:/sys/devices/system/node/node0/memory_failure/total:0
26:HardwareCorrupted:     0 kB
27:memory_failure_early_kill: 0
28:memory_failure_recovery: 1
29:enable_soft_offline: 1
30:panic_on_unrecoverable_memory_failure: cat: /proc/sys/vm/panic_on_unrecoverable_memory_failure: No such file or directory
```

Every recorded value is a read result; line 30's `cat:` diagnostic is positive proof that read was a `cat`. A
mutating-token sweep over the whole 37-line file finds nothing:

```
$ grep -nE "echo *[^ ]* *>|tee |sysctl -w|dd |madvise|hwpoison-inject|insmod|modprobe|systemctl|mount" sweeps.txt
(none)    exit 1
```

Independent read-only re-read today (my own, no write) reproduces every recorded value:

```
$ for f in /sys/devices/system/node/node0/memory_failure/*; do printf '%s: ' "$f"; cat "$f"; done
.../delayed: 0  .../failed: 0  .../ignored: 0  .../recovered: 0  .../total: 0
$ grep -i HardwareCorrupted /proc/meminfo
HardwareCorrupted:     0 kB
$ cat /proc/sys/vm/memory_failure_recovery ; cat /proc/sys/vm/memory_failure_early_kill ; cat /proc/sys/vm/enable_soft_offline
1 / 0 / 1
$ cat /proc/sys/vm/panic_on_unrecoverable_memory_failure
cat: ...: No such file or directory
$ uname -r
7.2.11-arch1-1                      (exit 0 for the loop; the last cat exits 1 as recorded)
$ ls -l /proc/sys/vm/enable_soft_offline /proc/sys/vm/memory_failure_recovery /proc/sys/vm/memory_failure_early_kill
-rw-r--r-- 1 root root 0 ... (each)   (exit 0)
$ id -u
1000                                 # non-root; test -w on /proc/sys/vm/memory_failure_recovery → not-writable-by-this-uid
```

So the reads are read-only both by command shape and by permission: this uid can read the knobs and cannot write
them. The values are also still current, so nothing the sweep recorded was produced by a write. Provenance limit:
the host block records values, not the literal commands (F5).

## 4. Question (c) — host-repair handoff

**Correct, with one unnamed recipient (F4).**

- `PROVINCE.md:9` — "Detection and report only — never remediation."
- `PROVINCE.md:13` — "systemd unit, driver/firmware and boot state (→ tsukuroi)".
- `PROVINCE.md:66` (Adjacent, tsukuroi row) — "Owns host OS, package, systemd-unit, driver, firmware, and boot
  diagnosis."
- Entry:79-80 routes to "host-repair actions (tsukuroi / operator ground)" — the same split, same lanes.
- Entry:83-84 declares soft offline out of scope but does not fence its trigger (F7).
- Entry:81-82 routes corrected-error accounting to "hardware-health ground this entry does not hold" and names no
  lane, although the adjacent owner for driver/hardware diagnosis is tsukuroi (F4).

The L1's uncommitted round-54 PROVINCE note (`git diff --unified=1 78295c76 -- PROVINCE.md`, appended at
`PROVINCE.md:456-472`, `+456,21`) repeats the routing — "injecting or unpoisoning memory, loading hwpoison-inject and
writing `vm.memory_failure_*` or `vm.panic_on_unrecoverable_memory_failure` are host actions (operator; host repair →
tsukuroi)" — and repeats the QUALITY 15 discipline ("counts come from the counters, never from kernel text"). It also
leaves EDAC/rasdaemon/MCE without a named lane, so F4 applies to both texts. That note is not at the reviewed
revision; I report it as observed draft, not as landed bytes.

## 5. Scratch and host discipline

Scratch root `/fast/scratch/hyaku/mori-r54/Mo54SentC2Boundary/` created with `mkdir -p`; it held only `tmp/` and no
cited file. No clone, no fixture, no network fetch. Disk guard read before start:
`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0, `/fast/scratch/hyaku` 26% used,
596.8G free. Read-only git only (`log`, `rev-parse`, `cat-file -t`, `hash-object` without `-w`, `diff --stat`); no
lane jj, no index write, no fleet-root write. No pacman transaction, no install, no forced-write probe. No credential
material, URL, session identity or machine id is reproduced here. Scratch removed before this report was finalised.

Limits: I did not re-fetch the six v7.3 copies (independent source re-fetch is another seat's surface), did not run
either counter, and did not judge any ledger disposition or claim row. A dispatched seat is not an independent
judge.

## Findings

| # | severity | file:line | finding |
|---|---|---|---|
| F1 | LOW | `corpus/knowledge/memory-failure-kills-r54.md:61` (with 49-51, 57) | The decision row's evidence cell opens with a text observation (`no line`) before the structured one (`all counters 0`), so a reader could implement "no `Memory failure:` line ⇒ nothing happened" — exactly the text-selected negative QUALITY 15 bars. The preamble at 49-51 forbids a tally, but not a text-derived *absence*. Smallest remediation: make the counters and `HardwareCorrupted: 0 kB` the stated evidence and label the absent line a corroborating observation, as row 57 already does for attribution. |
| F2 | LOW | `corpus/knowledge/memory-failure-kills-r54.md:7` | The on-release re-read glob `/proc/sys/vm/memory_failure_*` covers two of the four knobs the file reads (`memory_failure_recovery`, `memory_failure_early_kill`) and misses `vm.enable_soft_offline` (entry:72) and `vm.panic_on_unrecoverable_memory_failure` (entry:67,73) — so the recipe would skip the round's headline new switch and the soft-offline gate. Ground: `sources-r54/memory-failure.c.v7.3:134-171` (four entries, one `vm` table registered at `:2710`). Smallest remediation: name the four paths explicitly. |
| F3 | LOW | `corpus/knowledge/memory-failure-kills-r54.md:63-67` | The `sysctl (v7.3) \| value → behaviour` table lists three of the four memory-failure knobs; `vm.enable_soft_offline` is read at entry:72 and named as the soft-offline gate at entry:83 but has no behaviour row, although S521 documents the gate (`sources-r54/memory-failure.c.v7.3:2943-2949`, `:2985-2986` `disabled by /proc/sys/vm/enable_soft_offline`). Smallest remediation: add the fourth row (default 1; 0 disables soft offline). |
| F4 | LOW | `corpus/knowledge/memory-failure-kills-r54.md:81-82` | Corrected-error accounting is declared "hardware-health ground this entry does not hold" with no recipient lane, so a positive EDAC/`rasdaemon` observation has no route. `PROVINCE.md:66` makes tsukuroi the owner of driver/firmware diagnosis. Smallest remediation: name tsukuroi in that bullet (and in the round-54 PROVINCE draft bullet that repeats the phrase). |
| F5 | LOW | `.ufo/waves/round-54/evidence/sweeps.txt:19-30` | The host block asserts `(read-only)` in the section heading and then records only values; the literal read commands are absent, so read-only-ness is provable today by re-observation (this report §3) and by permission, not from the artifact. Qualifies as a disclosure gap against the lane's probe-disclosure rule, not a write. Smallest remediation: record the command list once (`cat` on the nine paths) next time this surface is swept. |
| F6 | LOW | `corpus/knowledge/kernel-v7.3-recheck-r54.md:105-108` | The drift paragraph is the only place in either file that names a write-capable surface ("the files always accepted PSI trigger writes"), and it carries neither a fence nor the pointer to `PROVINCE.md` FR12/round-24, where a PSI trigger write is explicitly outside the census. It states a documentation fact, not an instruction, but a reader keyed on the new "read-write" wording has nothing in this file telling them not to write a trigger. Smallest remediation: add "a trigger write stays outside mori's read-only probes (PROVINCE FR12)". |
| F7 | LOW | `corpus/knowledge/memory-failure-kills-r54.md:78-80` | The fence enumerates `madvise(MADV_HWPOISON)` and the hwpoison-inject *debugfs files*, but not loading the `hwpoison_inject` module — although S522:109-112 defines injection as "hwpoison-inject module through debugfs `/sys/kernel/debug/hwpoison/`", and the wave's host guard forbids loading it. It also does not fence the soft-offline trigger the entry declares out of scope at 83-84: `madvise(MADV_SOFT_OFFLINE)` (`/usr/include/asm-generic/mman-common.h:57`; reaches `soft_offline_page` via `sources-r54/memory-failure.c.v7.3:2691-2692`). Out of scope is not prohibited. Smallest remediation: extend the clause to the module load and to both madvise calls. |

No HIGH or MED boundary finding: every sentence that names a knob, an injection path or a kernel line is either
descriptive, a quoted claim, a read recipe, or an explicit prohibition, and neither file contains a write command,
a module load or a text-tally instruction.
