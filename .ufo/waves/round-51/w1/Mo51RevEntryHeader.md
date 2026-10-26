# Mo51RevEntryHeader — wave w1: review of memavailable-estimate-r51.md parts that no counter checks

Seat: Mo51RevEntryHeader (reviewer, leaf; no subagents). Lane: mori-shokunin.
Target: `corpus/knowledge/memavailable-estimate-r51.md` at data commit
`87e0c374537557754bf71dd68036ded3ddc6699c`. The reviewed files are unchanged in the working tree
(HEAD `b504cb1701568a0038aab9d98ec13d28eff801da`; `git diff 87e0c374 --stat -- corpus/knowledge/memavailable-estimate-r51.md corpus/SOURCES.md corpus/evidence/sources-r51/` empty), so the landed bytes are the bytes reviewed.
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51RevEntryHeader` (removed on completion; `TMPDIR` pointed into it for the curl run).
No tool installs (existing git/curl/grep/sed/awk/sha256sum used).

Report: .ufo/waves/round-51/w1/Mo51RevEntryHeader.md

## Scope

Parts reviewed (entry line numbers from the commit bytes): title (line 1); the five
`source:` lines (lines 3–7) vs SOURCES rows S492–S496; `verified-at:` (line 8); the
`recheck:` command and its stated digests (line 9); `coverage-map:` (line 10); the intro
paragraph, lines 12–16 (dispatcher/census sentences, lines 13–14; the estimate sentence,
lines 14–16). Quote location, claim-text constraints, pins and copy-hash checks are P-C2
territory and were not re-audited here.

## Verdicts

### 1. Title (line 1) — accurate

Title: *"MemAvailable is the kernel's estimate of startable memory, not a count of free pages"*.
Committed S492 copy `proc.rst.v7.2` lines 1124–1135 read:

```
MemAvailable
              An estimate of how much memory is available for starting new
              applications, without swapping. Calculated from MemFree,
              SReclaimable, the size of the file LRU lists, and the low
              watermarks in each zone.
```

"Startable memory" is a fair compression of "memory available for starting new applications";
"not a count of free pages" matches the estimate being derived (MemFree minus reserves, plus
cache and reclaimable terms) rather than equal to MemFree — also the motivation recorded in
S496. No change needed.

### 2. Five `source:` lines (lines 3–7) vs S492–S496 — consistent

Compared each entry line against the committed SOURCES row (lines 271–275 of the commit):

| entry source line | SOURCES row | check |
|---|---|---|
| S492 — `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst` — docs, tier A, "... (/proc/meminfo field definitions), opened 2026-10-26 | S492: same URL; type docs; tier A; scope "the /proc/meminfo field definitions at v7.2 …"; mined 2026-10-26; used-by lists the entry | match |
| S493 — `…/v7.2/mm/show_mem.c` — code, tier A, "(si_mem_available, the estimate)" | S493: same URL; code/A; "si_mem_available() at v7.2: …"; 2026-10-26; used-by lists the entry | match |
| S494 — `…/v7.2/fs/proc/meminfo.c` — code, tier A, "(how the meminfo lines are printed)" | S494: same URL; code/A; "how /proc/meminfo prints its lines at v7.2: …"; 2026-10-26; used-by lists the entry | match |
| S495 — `…/v7.2/include/linux/mm_inline.h` — code, tier A, "(which folios sit on the file LRU lists)" | S495: same URL; code/A; "which folios sit on the file LRU lists and which (anonymous, tmpfs, swap-backed) on the anon lists"; 2026-10-26; used-by lists the entry | match |
| S496 — `https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch` — code, tier A, "(the 2014 commit that added MemAvailable (its stated motivation))" | S496: same URL; code/A; "the 2014 commit that added MemAvailable: its stated motivation (free plus cached is wrong) and its original formula"; 2026-10-26; used-by lists the entry | match |

Entry lines abbreviate the row scopes but do not contradict them. No change needed.

### 3. `verified-at: 2026-10-26` (line 8) — consistent

All five SOURCES rows are opened 2026-10-26; the recheck parenthetical on the same line is
dated 2026-10-26; review date is 2026-10-26. The entry claims no host values (its Boundaries
state "No host value is claimed as typical"). No change needed.

### 4. `recheck:` command and digests (line 9) — verified by execution

Ran the command verbatim from scratch (`TMPDIR` inside scratch), 2026-10-26:

```
for u in https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/show_mem.c https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/meminfo.c https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mm_inline.h https://github.com/torvalds/linux/commit/34e431b0ae398fc54ea69ff85ec700722c9da773.patch; do curl -fsSL "$u" | sha256sum; done
```

Output (five lines, in URL order):

```
e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126  -
dba76b263bbdf93323a277a29c9281a892ff3fb35ddd6f0ddaf9ba1acb5b02f5  -
d6c5807421a69eac21efd737b39d099c711b3132b371dc34986d181746e3deda  -
2d4accbbc1ec139bfe11a356d4d17a55a2543769f3e10057a8a8584429c45ef6  -
9f571a04fc365858d8c82d31b309217a5e40f37877732da70416b0b1b42563d0  -
```

Exit code 0. These are exactly the five digests stated on the `recheck:` line. Separately,
the five committed copies under `corpus/evidence/sources-r51/` at `87e0c374` hash to the
same five digests in the same order (`git show 87e0c374:corpus/evidence/sources-r51/<f> |
sha256sum`). The line's parenthetical "(ran 2026-10-26; all five matched the committed copies
...)" is corroborated. No change needed.

### 5. `coverage-map:` (line 10) — "new ground; no FR row held it" is true

Swept `corpus/README.md` (coverage map rows 7–50; Frontier table FR1–FR15 at lines 341–354;
round-addition sections incl. Round-43 line 626, Round-49/50 tables) and `corpus/knowledge/*.md`
for `meminfo|memavailable|runway`:

- No coverage-map row holds the meaning of MemAvailable (rows: census surfaces, OOM/journal
  classes, drift, quota, harness-job capacity, etc.).
- No Frontier row holds it: FR1 (kernel OOM event-time attribution), FR8 (alert-threshold
  calibration — the entry only *practices* its "label thresholds local" rule, citing FR8),
  FR15 (harness background-job capacity runway — omp `async.maxJobs` clamp, not host memory),
  and the Round-43 resource-runway note (journal store size, S470) are all distinct ground.
- `knowledge/` uses MemAvailable only as a read value, never defines it: `surfaces-r7.md:83`
  and `observability-surfaces-r2.md:234` (census/pressure ratio), `harness-job-capacity-r25.md:178`
  (acquire gate "MemAvailable ≥ 6144 MB"), `userspace-oom-killers-r26.md:58` (earlyoom's
  formula), `audit-r11.md:342,349` (fixtures).

So "resource runway (new ground; no FR row held it)" is accurate. Note (not a defect): the
entry has no coverage-map row in README yet — that integration is the L1's post-review step
and is outside the counters.

### 6. Intro paragraph, lines 12–16 — all three sentences accurate

- Sentence 1 (line 12), *"mori reports resource runway: how much memory the host can still
  give to a new seat before it swaps or kills."* — a fair gloss of the fleet's runway concept;
  the kernel's own wording is "without causing swapping or OOM" (`show_mem.c.v7.2:43-46`;
  `proc.rst.v7.2` MemAvailable). The entry refines the naive reading later (Reading rules row
  12: swap excluded by construction; 0 is a clamp) — the intro does not contradict that. No
  change needed.
- Sentence 2 (lines 13–14), *"The fleet's dispatcher stops spawning seats when `MemAvailable`
  drops below a floor, and the lane's census and pressure probes print `MemAvailable/MemTotal`."*
  — verified:
  - `scripts/hyaku/inline-dispatcher.py:112` `MEM_MIN_GB` (default 4); `:129-139` `host_ok()`
    reads `/proc/meminfo` `MemAvailable:` and returns False (logs `host-pressure`) when
    `mem_gb < MEM_MIN_GB`, so seats are not spawned while below the floor.
  - `scripts/hyaku/wave-slot.sh:68` `mem_avail_mb()` reads `MemAvailable:`; `:79-89`
    `acquire` loops (sleep 20) and grants only when `mem_avail_mb >= MIN_AVAIL_MB`.
  - Census probe: `corpus/knowledge/surfaces-r7.md:83` — "host's own `MemAvailable/MemTotal`
    ratio with the scope **named on the row** (`mem_fill_scope=host-ram host_mem_avail_pct=…`)".
  - Pressure probe: `corpus/knowledge/observability-surfaces-r2.md:234` — "else the host
    `MemAvailable/MemTotal` floor against `MORI_MEM_AVAIL_MIN_PCT` … → `MEM_AVAIL_LOW` warn".
- Sentence 3 (lines 14–16), *"This entry says what that number is at kernel v7.2: an estimate
  computed by `si_mem_available()` (`show_mem.c.v7.2:32-72`) from free pages, the file LRU
  lists, reclaimable kernel memory and the zones' low watermarks, printed in kB by
  `meminfo.c.v7.2:62`."* — verified line-for-line against the committed copies:
  - `show_mem.c.v7.2`: `si_mem_available()` spans lines 32–72; input terms: `NR_FREE_PAGES`
    − `totalreserve_pages` (line 47), `NR_ACTIVE_FILE`+`NR_INACTIVE_FILE` (54–55),
    `NR_SLAB_RECLAIMABLE_B`+`NR_KERNEL_MISC_RECLAIMABLE` (64–65), `wmark_low` summed per
    zone via `low_wmark_pages(zone)` (40–41); zero clamp (69–70).
  - `meminfo.c.v7.2:62` is `show_val_kb(m, "MemAvailable:   ", available);`, adjacent to
    MemFree (line 61); the kB helper (`:27-31`) shifts by `PAGE_SHIFT - 10` and prints
    `" kB\n"`.

## Replacement wording

None needed — no sentence in scope required a fenced replacement.

## Findings

No HIGH/MED/LOW defect found in the scoped parts. Checks performed:

- [none] Title (line 1) — accurate vs `proc.rst.v7.2` MemAvailable definition.
- [none] Five `source:` lines (3–7) — match SOURCES S492–S496 (URL, type/tier, opened,
  used-by).
- [none] `verified-at:` (line 8) — consistent with row open dates and recheck date.
- [none] `recheck:` (line 9) — executed; exit 0; stated digests equal live fetches and the
  five committed copies under `corpus/evidence/sources-r51/`.
- [none] `coverage-map:` (line 10) — "new ground; no FR row held it" verified against README
  coverage map + Frontier FR1–FR15 and a `knowledge/` sweep.
- [none] Intro paragraph (12–16) — dispatcher/census sentence verified against
  `inline-dispatcher.py` (`MEM_MIN_GB`), `wave-slot.sh` (`MIN_AVAIL_MB`), `surfaces-r7.md:83`,
  `observability-surfaces-r2.md:234`; estimate sentence verified against `show_mem.c.v7.2:32-72`
  and `meminfo.c.v7.2:62`.

Residual: the entry is not yet in the README coverage map; that is L1 integration, not a
defect in the entry (see section 5 note).
