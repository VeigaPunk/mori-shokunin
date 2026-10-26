# Mo51SentEntryScope — Scope and adjacency review: MemAvailable entry and its five copies (round 51, wave w1)

Seat: Mo51SentEntryScope (leaf sentinel; scope/adjacency of the C2 entry, not a row-level judge).
Date: 2026-10-26. Lane: mori-shokunin. Data revision under review: `87e0c374537557754bf71dd68036ded3ddc6699c`
(entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`). Working-tree lane HEAD when read:
`b504cb1701568a0038aab9d98ec13d28eff801da` (seats landed after data).

Scratch: `/fast/scratch/hyaku/mori-r51/Mo51SentEntryScope/` — **not created**: this seat wrote no clone, fixture
or temp file. Every command below is read-only against committed bytes; nothing to remove.
Tool installs: none. No pacman call, no git/jj mutation, no write outside this report file.
Disk guard before the work (`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`): `/fast/scratch/hyaku`
26 % used, 597.4 G free; `/tmp` 3 %, 124.1 G free.

Report: .ufo/waves/round-51/w1/Mo51SentEntryScope.md

## Assignment

1. Does any sentence of `corpus/knowledge/memavailable-estimate-r51.md`, or rows S492–S496 in `corpus/SOURCES.md`,
   advise changing host memory configuration (`min_free_kbytes`, `watermark_scale_factor`, swap, cgroup limits) —
   tsukuroi's province — or the dispatcher's floor (the orchestrator's)? Verdict per issue.
2. Credential material, private URLs, absolute host paths and file sizes in `corpus/evidence/sources-r51/` (the lane
   helper skips new files > 1 MiB inside a named dir).

## Evidence read (read-only; absolute paths)

- Contract: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/contract.md` (C2 surface, P-C2,
  named limits, round shape, frozen rule).
- Entry: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md` (65 lines;
  framing `:12-16`, claim table `:22-42`, reading rules `:44-57`, boundaries `:59-65`).
- Rows: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:271-275` (S492–S496, each with copy path and
  sha256).
- Copies: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/` — `proc.rst.v7.2`,
  `show_mem.c.v7.2`, `meminfo.c.v7.2`, `mm_inline.h.v7.2`, `34e431b0.patch`.
- Frozen byte list: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/evidence/freeze-sha256.txt`
  (`:1-5` = the five copies, by basename).
- Counter copy table: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/count-c2.py:45-52` (`COPIES`,
  same basenames).
- Provinces: `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md` (`:6-10` owns, `:12-16` refuses,
  `:26` resource-runway row, `:289` shared-evidence sentence);
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md` (`:8-14` owns, `:28` refuse/report sentence,
  `:30-33` host-memory-as-triage sentence, ADJ-04 row `:49`).
- Lane probes: `tools/mori-census.sh` (`:313` `MEMINFO`, `:646-647` `meminfo_field`, `:1791-1793` the read),
  `tools/mori-pressure.py` (`:87` `DEFAULT_ROOT = "/proc/pressure"`), `tools/mori-source-drift.py`
  (`:76-105` `find_copy`, `:224-236` classify loop).

Data bytes unchanged since landing: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat
87e0c374537557754bf71dd68036ded3ddc6699c -- corpus/knowledge/memavailable-estimate-r51.md
corpus/evidence/sources-r51 corpus/SOURCES.md` → empty output, exit 0. Every finding below therefore applies to the
bytes the counter measured.

## 1. Host memory configuration — does any sentence advise a change?

No. Verdict: **in scope, no advisory sentence**. Evidence:

```
$ grep -nE '\b(should|must|avoid|prefer|set|change|tune|raise|lower|increase|decrease|disable|enable|adjust|write|configure)\b|cgroup' \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/memavailable-estimate-r51.md
42:| The commit put the estimate into meminfo so that monitoring programs need not model reclaim internals themselves. | S496 | `user space really should not be expected to know kernel internals to come up with an estima
51:- When `Cached` is large but `MemAvailable` is small, compare `Shmem`: tmpfs and shared memory raise `Cached`
exit 0
```

Both hits are non-advisory: `:42`'s word "should" sits inside the quoted kernel commit text, and `:51`'s "raise" is
descriptive ("tmpfs and shared memory raise `Cached`"). `cgroup` occurs zero times in the entry, so no cgroup-limit
sentence exists to advise anything. The only imperative sentences address the lane's own instruments
(`:46` "Read `MemAvailable` itself … never rebuild it as `MemFree + Cached`"; `:54` "Report the threshold as local"),
which is mori's own measurement practice under `PROVINCE.md:26` (runway / `fill/avail`) and FR8.

The single sentence naming those settings is a refusal, `:59-61`:

> Detection and report only: this entry reads `/proc/meminfo`; it never changes `vm.min_free_kbytes`,
> `watermark_scale_factor`, swap or any limit (host configuration is tsukuroi's; the dispatcher's floor is the
> orchestrator's).

Verdict on the refusal: correct direction, two attribution defects — see Findings F3 (sibling assigned an action class
it declines; no pointer) and F5 (subject is the entry, which reads nothing).

## 2. Dispatcher floor — does any sentence advise a change?

No advisory sentence. Verdict: **no scope breach**; one durability defect and one ambiguity.

- `:12-13` asserts the gate: "The fleet's dispatcher stops spawning seats when `MemAvailable` drops below a floor".
  Descriptive, no advice — but the entry carries **no source** for it (`grep -n 'goal-2026\|MEM_MIN_GB\|host limits'`
  over the entry → no match, exit 1). The contract names the only source,
  `.scratch/goal-20261026-hyaku-run9.md` host limits (`MEM_MIN_GB`), and that path is untracked and absent at the data
  revision:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files --error-unmatch .scratch/goal-20261026-hyaku-run9.md
error: pathspec '.scratch/goal-20261026-hyaku-run9.md' did not match any file(s) known to git
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e \
    87e0c374537557754bf71dd68036ded3ddc6699c:.scratch/goal-20261026-hyaku-run9.md
fatal: path '.scratch/goal-20261026-hyaku-run9.md' does not exist in '87e0c374…'
rc=128
```

  Live value observed (`grep -n 'MemAvailable\|MEM_MIN_GB' /home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run9.md`):
  `:60  MemAvailable < 4 GiB (MEM_MIN_GB). A 128-seat wave fills in tranches.` — i.e. the statement is true of the
  live run file, but cannot be rechecked from the corpus. Finding F2.
- `:53-54` reading rule 5 is the only sentence about a runway threshold: "A runway threshold on `MemAvailable` is a
  threshold on a model whose holdbacks are min(half, low-watermark sum); … Report the threshold as local, as the lane
  already does for its other thresholds (FR8)." Its subject is generic ("a runway threshold"), so it can be read as
  covering the orchestrator's `MEM_MIN_GB`; the trailing clause scopes it to lane thresholds. Labeling advice, not a
  request to change a floor, and `:59-61` disclaims the floor. Finding F4 (LOW, ambiguity only).
- `:48-49` ("a host with free swap can keep running past `MemAvailable = 0`") is the one sentence whose content bears
  on how conservative a floor is. It draws no conclusion about any floor and advises nothing; it is a description, in
  scope for a runway entry. Its sourcing (rows 1, 12) is a wording matter routed to the entailment seats — F7.

## 3. Adjacency of the sibling attribution

`PROVINCE.md:12-16` refuses "OS package, systemd unit, driver/firmware and boot state (→ tsukuroi)"; the entry's
`:60` extends that to "host configuration". tsukuroi's declaration, read at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`:

- `:30` — "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused
  pressure…" (measurement, not configuration).
- `:28` — "never restarts services. Detection and report; the operator remediates."
- `:8-14` Core surfaces — pacman state, systemd units/timers, journal/boot triage, driver/firmware. No sysctl, swap or
  memory-configuration surface is declared.

So a reader following `:60` to tsukuroi finds no surface that configures host memory, and a refusal of remediation.
The claim is over-broad rather than wrong in domain terms (memory sysctls and swap are OS substrate, not fleet
evidence). No sibling pointer is given, unlike the lane's adjacency convention
(`PROVINCE.md:289`, and the adjacency table rows citing `../tsukuroi-shokunin/PROVINCE.md:…`). Finding F3.

`mori` reading `/proc/meminfo` is in province: `PROVINCE.md:26` names "memory PSI/fill/avail" on the resource-runway
row, and the fill arm reads it (`tools/mori-census.sh:1791-1793`). The entry's own headline ("mori reports resource
runway…") is a correct self-description, not an absorption of tsukuroi's OS diagnosis.

## 4. Hygiene of `corpus/evidence/sources-r51/`

```
$ ls -la /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/
-rw-r--r-- 1 vgpnk vgpnk   5199 34e431b0.patch
-rw-r--r-- 1 vgpnk vgpnk   6046 meminfo.c.v7.2
-rw-r--r-- 1 vgpnk vgpnk  19417 mm_inline.h.v7.2
-rw-r--r-- 1 vgpnk vgpnk 107560 proc.rst.v7.2
-rw-r--r-- 1 vgpnk vgpnk  13204 show_mem.c.v7.2
$ grep -rInE '/home/|/fast/|/tmp/|/scratch|BEGIN [A-Z ]*PRIVATE|api[_-]?key|token|password|secret|ssh-rsa|https?://[^ ]*(token|key|auth|@)' \
    /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/
proc.rst.v7.2:1155:              as mlocked pages, ramfs backing pages, secret memfd pages etc.
proc.rst.v7.2:1825:    test:/tmp # dd if=/dev/zero of=/tmp/test.dat &
proc.rst.v7.2:2467:	# strace -e mount mount -o hidepid=1 -t proc proc /tmp/proc
proc.rst.v7.2:2468:	mount("proc", "/tmp/proc", "proc", 0, "hidepid=1") = 0
proc.rst.v7.2:2473:	proc /tmp/proc proc rw,relatime,hidepid=2 0 0
proc.rst.v7.2:2478:	# mount -o remount,hidepid=1 -t proc proc /tmp/proc
proc.rst.v7.2:2482:	proc /tmp/proc proc rw,relatime,hidepid=1 0 0
proc.rst.v7.2:2492:	# mount -o remount,hidepid=noaccess -t proc proc /tmp/proc
proc.rst.v7.2:2495:	# mount -o remount,hidepid=noaccess -t proc proc /tmp/proc
```

- Credentials: none. The only "secret" hit is upstream prose ("secret memfd pages", `proc.rst.v7.2:1155`); no key,
  token, password, private-key block or `user@host` URL anywhere in the five copies.
- Private URLs: none. Two URLs inside the copies, both upstream and public — `proc.rst.v7.2:73`
  `https://www.kernel.org/doc/html/latest/filesystems/proc.html` and `proc.rst.v7.2:992`
  `https://github.com/libhugetlbfs/libhugetlbfs/`. The entry and rows S492–S496 carry only the five public
  `raw.githubusercontent.com/torvalds/linux/v7.2/…` and `github.com/torvalds/linux/commit/34e431b0…` URLs.
- Absolute host paths: none. Every `/tmp` hit is upstream documentation text (a `dd` example, `hidepid` mount
  examples), not a path on this host; no `/home/`, `/fast/`, `/scratch`, machine name, `127.0.0.1`, `localhost` or
  dotted-quad address occurs in the entry or the copies (`grep -rInE` over both → no match).
- File sizes: largest copy 107,560 B (105 KiB); all five are below 1 MiB and below
  `mori-source-drift.py:54` `FETCH_MAX_BYTES = 4 * 1024 * 1024`. No copy can be skipped by a size gate.
- Hashes: all five copies match the entry's `recheck:` line and `freeze-sha256.txt:1-5`:

```
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r51/*
9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0  34e431b0.patch
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  meminfo.c.v7.2
2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6  mm_inline.h.v7.2
e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126  proc.rst.v7.2
dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5  show_mem.c.v7.2
```

Verdict: **clean** on all four hygiene questions.

One durability defect found while checking sizes/naming — F6: the copies are not addressable by the lane's own copy
matcher.

## 5. Checks that came out clean (and what would falsify them)

| Check | Evidence | Verdict |
|---|---|---|
| Entry unchanged between `87e0c37` and the worktree | `git diff --stat 87e0c37 -- <entry> <copies> SOURCES.md` empty, rc 0 | findings apply to landed bytes |
| No advisory sentence on host memory config | config-verb grep, 2 non-advisory hits | clean |
| No cgroup sentence at all | `cgroup` 0 matches in the entry | clean (nothing to advise) |
| No advisory sentence on the dispatcher floor | `:53-54` label advice only; `:59-61` disclaims floor | clean |
| Dispatcher statement is true of the live run file | `.scratch/goal-20261026-hyaku-run9.md:60` `MEM_MIN_GB` 4 GiB | true live, unrecheckable from corpus (F2) |
| Entry's line pointers into the copies | `show_mem.c.v7.2:32` = `long si_mem_available(void)`; `meminfo.c.v7.2:62` = the `MemAvailable:` print | correct |
| `MemAvailable/MemTotal` read is the census fill arm | `tools/mori-census.sh:1791-1793` (`meminfo_field MemTotal/MemAvailable`, `avail_pct`) | true for the census only (F1) |
| Pressure probe reads no meminfo | `grep -c meminfo tools/mori-pressure.py` → `0`; `DEFAULT_ROOT = "/proc/pressure"` | F1 confirmed |
| Copies under 1 MiB | `du -b` max 107,560 | clean |

## Not this seat's surface (routed, no vote cast here)

- Row-level entailment judgment for the 21 claims belongs to the seats whose item says ENTAILMENT; this seat records
  no vote, and its report carries no vote line. The counter reads only such lines, so nothing here can move
  `entailed=`/`dissent=`.
- Counter, predicate, control and kill-rule weaknesses (e.g. the named limits in the contract) are report material
  only; none is proposed as a fix here.
- Whether the five copies equal today's upstream bodies (re-fetch) was not run by this seat: that is source
  re-opening, not scope review. UNVERIFIED here beyond the committed-sha equality above.

## Findings

1. **MED — `corpus/knowledge/memavailable-estimate-r51.md:13-14`** (with `corpus/SOURCES.md` unaffected): the framing
   sentence says "the lane's census and pressure probes print `MemAvailable/MemTotal`". False for the pressure probe:
   `tools/mori-pressure.py` reads `/proc/pressure/{cpu,memory,io,irq}` only (`:87`; `grep -c meminfo` → 0), and only
   the census fill arm reads the pair (`tools/mori-census.sh:1791-1793`, printed as `host_mem_avail_pct`). Not advice —
   a false statement about the lane's own probes in the new depth surface. Smallest remediation: "the lane's census
   fill arm prints `MemAvailable/MemTotal`", or name `tools/mori-census.sh:1791`. (The claim table is unaffected; no
   row cites this sentence, so no entailment vote is displaced.)

2. **MED — `corpus/knowledge/memavailable-estimate-r51.md:13`**: "The fleet's dispatcher stops spawning seats when
   `MemAvailable` drops below a floor" asserts another owner's mechanism with no source in the entry; the only source
   (contract, C2 surface) is `.scratch/goal-20261026-hyaku-run9.md`, untracked (`git ls-files --error-unmatch` failed)
   and absent at `87e0c37` (`git cat-file -e` rc 128). Not a scope breach (no advice), but an unrecheckable
   cross-province fact in the corpus, resting on the same ephemeral `.scratch` class this round's C1 treats as
   residue. Smallest remediation: attribute it inline ("per the run's host limits, `MEM_MIN_GB`") with a committed
   pointer, or drop the mechanism clause and keep only that the lane reports runway against a local floor.

3. **LOW — `corpus/knowledge/memavailable-estimate-r51.md:59-61`**: "host configuration is tsukuroi's" assigns an
   action class the sibling declines — `tsukuroi-shokunin/PROVINCE.md:28` "Detection and report; the operator
   remediates", and its Core surfaces (`:8-14`) name no sysctl, swap or memory-configuration surface (host memory
   appears only as triage measurement, `:30`). Direction of the refusal is right, wording over-broad, and no sibling
   pointer is given where mori's adjacency convention gives `file:line` (`PROVINCE.md:289`). Smallest remediation:
   "OS state is tsukuroi's to diagnose and the operator's to change; the dispatcher's floor is the orchestrator's",
   with one `../tsukuroi-shokunin/PROVINCE.md:8-14,28` pointer.

4. **LOW — `corpus/knowledge/memavailable-estimate-r51.md:53-54`**: reading rule 5's subject "A runway threshold on
   `MemAvailable`" is generic enough to cover the orchestrator's `MEM_MIN_GB` floor, so "Report the threshold as
   local" can read as advice to the orchestrator. The tail ("as the lane already does for its other thresholds
   (FR8)") and `:59-61` scope it to the lane, so there is no breach — only ambiguity. Smallest remediation: "the
   lane's runway threshold".

5. **LOW — `corpus/knowledge/memavailable-estimate-r51.md:59`**: "this entry reads `/proc/meminfo`" — a document reads
   nothing; the read is `tools/mori-census.sh:1791-1792`. Same sentence as F3, so one edit covers both.

6. **MED — `corpus/evidence/sources-r51/` naming vs `tools/mori-source-drift.py:76-105`** (rows
   `corpus/SOURCES.md:271-275`): the copies are basenamed (`meminfo.c.v7.2`, …) but `find_copy` requires
   `<Sid>.<ext>` inside `sources-r<N>/`; measured `find_copy(root, 'S492'…'S496')` → `None` for all five, so the
   drift probe prints `no-copy` for these rows and the round's five sources are outside automated drift detection.
   Pre-existing pattern: rounds r47–r51 all have `sid_named=0` (`for d in corpus/evidence/sources-r*` survey). Not a
   claim defect — `count-c2.py:45-52` pins the same basenames and `freeze-sha256.txt:1-5` freezes them, and the
   entry's own `curl | sha256sum` recipe still detects drift by hand — and the names MUST NOT change this round
   (frozen bytes). Smallest remediation for a later round: teach `find_copy` to fall back to the row's `copy` cell
   (`tools/mori-source-drift.py` is not a frozen counter — `freeze-sha256.txt` lists only the C1 witness copies), or
   record the gap as a named limit of C2's provenance arm.

7. **LOW (outside this seat's surface; routed, no vote) — `corpus/knowledge/memavailable-estimate-r51.md:48-49`**:
   "a host with free swap can keep running past `MemAvailable = 0`" cites rows 1 and 12; row 1's quote supports
   "without swapping" and row 12 the zero clamp, but neither quote says a host keeps running past zero. Wording or
   sourcing of a reading rule; the row-level judgment is the entailment seats'. Smallest remediation if the L1
   agrees: mark the sentence as inference (as `:51-52` already does) or cite nothing beyond the exclusion.
