# CriticCeilingInference — attack on the Fact 5 ceiling inference (mori round 27, wave 2)

Seat: `MoriR27.CriticCeilingInference` (critic, leaf). Attacks the inference in
`corpus/knowledge/oom-victim-selection-r27.md:133-137` (Fact 5) at lane tip `5f00fd04` that a send-line `oom_score`
above `(2000 + oom_score_adj) * 2 / 3` can only come from earlyoom's +300 `--prefer` adjustment, and the claim
"matched at least 8 victims". Read-only on the lane; nothing written except this file. Scratch:
`/fast/scratch/hyaku/mori-r27/CriticCeilingInference/` (upstream bytes and the in-memory script `ceiling.py`).
Tools installed or updated: none. `~/.omp/agent/RULES.md` read (14 lines, the tooling directive). No `godspeed`
skill file exists on disk; only the hook `~/.omp/agent/hooks/pre/godspeed-always-on.js` was found (`find` over `/`).

## Verdict

**Holds, with conditions.** All 8 above-ceiling sends do need the +300. Read without it, each would need a kernel
footprint 4 to 13 GiB larger than RAM plus swap. Every alternative I was asked to test fails on the evidence below.
Two things must change:

- The entry's evidence that a prefer expression was armed is the boot-0 process (wave-1 HostUnitOomAdjust), not boot -1.
- Two conditions are unstated: earlyoom ran without `--sort-by-rss`, and the kernel counted no page twice.

The data also give an upper bound the entry lacks: at most 27 of the 39 sends can be prefer-matched. The other 12,
including the one `omp`-class send, cannot be.

## Upstream bytes opened (2026-10-22, curl)

| File | URL | Accessed | sha256 |
|---|---|---|---|
| `kill.c` v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | 17:09:32Z | `b32e0fad…0bf3` (= S118) |
| `main.c` v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 17:09:32Z | `08656b0b…d0e4` (= S119) |
| `meminfo.c` v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c | 17:09:32Z | `526e512c…edfeb` |
| `MANPAGE.md` v1.9.0 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 17:14:04Z | `cc48b02e…dfeda` (= S115) |
| `fs/proc/base.c` v7.2 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c | 17:09:32Z | `cef1a2cf…15c6` (= S127) |
| `mm/oom_kill.c` v7.2 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 17:09:32Z | `452f1348…6b4e` (= S003) |
| `mm/oom_kill.c` v7.2.11 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/mm/oom_kill.c?h=v7.2.11 | 17:11:58Z | `452f1348…6b4e` (identical) |
| `fs/proc/base.c` v7.2.11 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/proc/base.c?h=v7.2.11 | 17:11:59Z | `cef1a2cf…15c6` (identical) |
| `mm/swapfile.c` v7.2 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/swapfile.c | 17:15:01Z | `5c89f9c3…3cecb` |

Quotes (verbatim, line numbers by `grep -n` on the downloaded bytes):

- `oom_kill.c:228-229` "points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) + mm_pgtables_bytes(p->mm) / PAGE_SIZE;"
- `oom_kill.c:233` "adj *= totalpages / 1000;"
- `base.c:586` "unsigned long totalpages = totalram_pages() + total_swap_pages;"
- `base.c:597` "points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;" (no clamp follows; `:599` prints it)
- `kill.c:414` "cur->oom_score += OOM_SCORE_PREFER;"; `:410-412` under `args->sort_by_rss` "cur->VmRSSkiB += VMRSS_PREFER;"
- `kill.c:378-382` VmRSS from `/proc/<pid>/stat`; `:396-401` `oom_score`; `:471` "get_oom_score_adj(cur->pid, &cur->oom_score_adj);"
- `kill.c:627` the send line prints `victim->oom_score, victim->oom_score_adj, victim->VmRSSkiB / 1024`;
  `fill_informative_fields` (`:484-506`) fills only name, cmdline and uid afterwards.
- `main.c:379` "Preferring to kill process names that match regex '%s'\n"; `main.c:412` "mem total: %4lld MiB, user mem total: %4lld MiB, swap total: %4lld MiB\n"
- `swapfile.c:3117` "total_swap_pages -= p->pages;" comes before `:3124` "err = try_to_unuse(p->type);"
- `MANPAGE.md:275` "For processes matched by `--prefer`, negative `oom_score_adj` values are not" (it concerns negative adjustments, not 200)

The only lines in `kill.c` that change a candidate's `oom_score` are `:401` (the kernel value), `:414` (+300) and `:421` (−300)
(`grep -n -E 'oom_score \+=|oom_score =' kill.c`).

## Host evidence (read-only, aggregates only; `python3 -I -B` in-memory scripts in scratch, 2026-10-22T17:10–17:15Z)

- `journalctl --list-boots`: 6 boots. Boot -1 ran from 2026-10-20T12:57:09Z to 2026-10-22T07:54:50Z.
- Kernel per boot, from the kernel's `Linux version` record (version token only): boot -1 `7.2.11-arch1-1` (1 record),
  boot 0 `7.2.11-arch1-1`. Boots -5 to -3 keep 0 kernel records. Boot -2 keeps 513 kernel records with no version
  line, so its kernel is unknown. No boot other than -1 holds a send line.
- Swap in boot -1: one kernel swap-activation record (a file, 31722876 kB = 30.25 GiB), no zram record, and one
  systemd `Deactivating swap` record, after the last send at 2026-10-22T06:16:05Z.
- earlyoom in boot -1: one invocation (one `earlyoom 1.9.0` version record). It logged one prefer startup line
  (`main.c:379`) and one avoid startup line, and its startup `mem total` was 30978 MiB. Every one of the 39 pre-kill
  `mem avail` records (`meminfo.c:279-284`) shows a swap total of 30979 MiB. So `totalpages` was about 60.5 GiB,
  unchanged across all sends.
- `/etc/default/earlyoom` mtime 2026-10-20T12:19:40Z (metadata only, no value read), before boot -1's first entry.
  `/etc/systemd/system/earlyoom.service.d` absent; `systemctl show earlyoom.service -p DropInPaths --value` → 0 words.
- `/sys/kernel/mm/ksm/run` → `0` and `pages_sharing` → `0` (boot 0). There are 0 files mentioning ksm under the
  tmpfiles.d, sysctl.d and `/etc/systemd/system` trees.

Per-send test (boot -1, 39 sends; T = (30978 + 30979) MiB in pages). For each send line I computed the kernel score
its VmRSS alone would give at adjustment 200 (`base.c:597`, `oom_kill.c:233`). The real kernel score can only be
higher, because swap entries and page tables add to it. The gap is the send-line score minus that floor. A prefer
match needs a gap of at least 300.

| Band | Sends | Gap (points) | VmRSS MiB min / median / max | Footprint beyond VmRSS needed if not adjusted |
|---|---|---|---|---|
| above 1466 | 8 | 523–565 | 18430 / 19892 / 23653 | 47.4–51.2 GiB (total 4–13 GiB over T) |
| below 1466, gap ≥ 300 | 19 (all in the 06Z burst) | 300–301 | 4 / 10 / 17 | 27.2–27.3 GiB each |
| below 1466, gap < 300 | 12 | 169–255 | 10232 / 21795 / 23501 | 15.3–23.1 GiB |

One point of score is about 0.09 GiB of footprint here (11.02 points per GiB).

## Alternatives tested

| Alternative | Result | Evidence |
|---|---|---|
| Page tables counted on top of rss and swap | **rejected** | They are counted (`oom_kill.c:228-229`), but page tables live in RAM, so resident set plus page tables stays within `MemTotal` and swap entries within `SwapTotal`. Read without the +300, the 8 lines need 47–51 GiB beyond VmRSS while swap is 30.25 GiB. That leaves 17–21 GiB of page tables on top of 18–23 GiB resident, 35–44 GiB in all, against 30.25 GiB of RAM. |
| `totalpages` changing (swap added or removed, zram) | **rejected** | The ceiling `(2000 + adj) * 2 / 3` does not depend on `totalpages`; only a footprint larger than `totalpages` breaks it. That can happen during a `swapoff`, which lowers `total_swap_pages` before it brings pages back (`swapfile.c:3117,3124`). Boot -1 had no zram, one swap activation and no deactivation before the last send, and swap total read 30979 MiB at all 39 sends. zram was gone before boot -1, not removed during it. |
| Integer arithmetic | **rejected** | Every truncation lowers the value: `totalpages / 1000` (`oom_kill.c:233`), `/ (long)totalpages` and `* 2 / 3` (`base.c:597`). At adjustment 200 the exact maximum is 1466, which is the script's `(2000 + adj) * 2 // 3`. My re-run reproduced `above=8`. |
| A different kernel in boot -1 | **rejected** | Boot -1 ran `7.2.11-arch1-1`, the same as boot 0. The stable v7.2.11 `oom_kill.c` and `base.c` are byte-identical to the v7.2 tag. Arch's own patch set was not diffed (the entry's Limits line still stands for that). |
| earlyoom reading `oom_score` at a different time | **rejected as a source of error; residual** | Score, adjustment and VmRSS come from one `is_larger` pass and are printed without being read again (`kill.c:378-402,471,627`, `:484-506`). The one gap is that the adjustment is read after the score (`:396` before `:471`). A process that lowered its own adjustment between the two reads (allowed down to the floor of 100, Fact 3) would print 200 against a higher score; reaching 1619 that way needs an adjustment of at least 429 at the score read [INFERENCE: arithmetic]. No evidence of such writers; implausible for 8 sends. |
| `--sort-by-rss` on in boot -1 | **rejected [INFERENCE]** | Under `--sort-by-rss` a prefer match adds 3 GiB to VmRSS, not 300 to the score (`kill.c:410-416`), and the 8 lines would have no explanation. Boot 0's argv lacks the flag (wave-1 `HostUnitOomAdjust.md:51`); the args file is older than boot -1, and there is no drop-in and one invocation. The 19 sends with a 300-point gap printed VmRSS of 4–17 MiB, which fits a score-side +300, not a VmRSS-side one. |
| Resident set counting one page twice (KSM; the same file or shmem mapped twice in one process) | **not excluded; residual** | VmRSS is the same counter the kernel scores (`kill.c:378-382`; `oom_kill.c:228`). A page counted twice there can push a footprint past `totalpages`. Each of the 8 would need at least 4–13 GiB counted twice. KSM is off now with no configuration that turns it on; boot -1's KSM state cannot be observed. [INFERENCE] implausible, but it is the true remaining condition. |

## Statements

| # | Statement (entry line) | Verdict | Severity |
|---|---|---|---|
| 1 | `:133-134` 8 of 39 above the ceiling, 1466 at 200 | holds (reproduced 8) | — |
| 2 | `:134-135` "The ceiling assumes a process's resident set, swap entries and page tables together stay within RAM plus swap [INFERENCE]" | holds; the condition is narrower and testable: page tables live in RAM, and the only way past it is a page counted twice in the resident set, or a `swapoff` in progress | low |
| 3 | `:135` "Only earlyoom's +300 `--prefer` adjustment can produce that (Fact 1)" | holds with conditions: `--sort-by-rss` off, no page counted twice, no `swapoff` in progress | medium |
| 4 | `:135-136` "present in earlyoom's argument list, value not read (wave-1 HostUnitOomAdjust)" | wrong provenance for boot -1: HostUnitOomAdjust read the live boot-0 process. Boot -1's own evidence is its one invocation's prefer startup line (`main.c:379`) | medium |
| 5 | `:136-137` "matched at least 8 victims" | holds; missing its upper bound: 12 sends have a gap below 300 and cannot be prefer-matched, so at most 27 | medium |
| 6 | `:178-179` Limits "The prefer-match count is a lower bound" | holds; add the upper bound and the 19 sends whose gap is exactly 300–301 | low |
| 7 | `:165` and `SKILL.md:729` decision row "a `--prefer` match added 300 to that victim" | holds with the same conditions; a reader applying it to a `--sort-by-rss` earlyoom would conclude wrongly | medium |
| 8 | `:66` Fact 2 "The range is 0 to 2000." | holds only under the same condition: no clamp exists (`base.c:596-599`) | low |
| 9 | `corpus/lessons/round-27.md:20` "8 of its 39 send lines carry a score only a prefer match can produce" | holds with the same conditions | low |

The 19 sends with a gap of 300–301 are strong but unproven evidence of more prefer matches. Read without the +300,
19 processes with 4–17 MiB resident would each need 27.2–27.3 GiB of swap within 6 seconds, with total swap at
30.25 GiB. That is possible only through swap entries shared by forked processes, since `MM_SWAPENTS` is counted per
process [INFERENCE]. A constant 300-point offset is the +300 signature. The ceiling test cannot prove these sends,
so they belong in the bound, not in the count.

## Exact corrections (old → new)

**A. Entry `oom-victim-selection-r27.md:133-137`.** Old:

> - **8 of the 39 send lines carry a score above the kernel's ceiling for their adjustment** (`(1000 + 200 + 1000) * 2
>   / 3 = 1466` for 200; `above_kernel_ceiling_for_adj=8` in the committed output). The ceiling assumes a process's
>   resident set, swap entries and page tables together stay within RAM plus swap [INFERENCE]. Only earlyoom's +300 `--prefer` adjustment can produce that (Fact 1), so the host's prefer
>   expression — present in earlyoom's argument list, value not read (wave-1 HostUnitOomAdjust) — matched at least 8
>   victims. This is a count of send lines, not of how the expression reads.

New:

> - **8 of the 39 send lines carry a score above the kernel's ceiling for their adjustment** (`(1000 + 200 + 1000) * 2
>   / 3 = 1466` for 200; `above_kernel_ceiling_for_adj=8` in the committed output). The ceiling holds while a
>   process's counted resident set, swap entries and page tables stay within RAM plus swap. Page tables live in RAM,
>   so only a page counted twice in the resident set or a `swapoff` in progress can break it [INFERENCE]. Read
>   without a +300, each of the 8 would need 4 to 13 GiB more than the 60.5 GiB of RAM plus swap. Boot -1 had no
>   swap change before its last send and ran the same kernel as boot 0 (wave-2 CriticCeilingInference). With
>   `--sort-by-rss` off, only earlyoom's +300 `--prefer` adjustment can produce that (Fact 1). Under `--sort-by-rss`
>   the +300 goes to the resident set instead (S118 `kill.c:410-416`). So the prefer expression of boot -1's one
>   earlyoom invocation, whose startup logged its prefer line once (S119 `main.c:379`; value not read), matched at
>   least 8 victims. At most 27 sends can be prefer-matched: 12 score less than 300 above what their resident set
>   alone gives (wave-2 CriticCeilingInference). This is a count of send lines, not of how the expression reads.

**B. Entry decision table `:165` (and `SKILL.md:729`, same middle cell).** Old: `| a --prefer match added 300 to that victim |`
→ New: `| a --prefer match added 300 to that victim, if earlyoom runs without --sort-by-rss and no swapoff was in progress |`.

**C. Entry Limits `:178-179`.** Old: "The prefer-match count is a lower bound: a prefer-matched victim whose kernel
score plus 300 stays under the ceiling is not counted." → New: append "The upper bound is 27: a send whose score is
less than 300 above its resident-set-only kernel score cannot be prefer-matched. 19 of the 27 sit exactly 300–301
above that floor, which fits a +300 with almost no swap but does not prove it."

**D. Entry Fact 2 `:66` (low).** Old: "The range is 0 to 2000." → New: "The range is 0 to 2000 while the footprint
stays within `totalpages`; the code does not clamp it (S127 `base.c:596-599`)."

**E. Lesson `corpus/lessons/round-27.md:20` (low).** Old: "8 of its 39 send lines carry a score only a prefer match
can produce" → New: "8 of its 39 send lines carry a score only a prefer match can produce while `--sort-by-rss` is
off".

## Privacy note for the L1

Both of my process-class statements use only allowed classes and counts. They are: all 12 sends that cannot be
prefer-matched are `other` (11) or `omp` (1), and the 27 that can be are the 27 `python`-class sends. Together with
the published class totals, they show which class the prefer expression's matches fall in, but not its text. Wording
A states only the bounds, not the classes. Whether to also publish "the one `omp`-class send was not prefer-matched"
is the L1's call. It matters to the fleet, because the session process was chosen on its own kernel score, not
through a prefer match. No pid, uid number, command line, process name outside the class list, `MESSAGE` text or
expression value entered this report.

## Side observation (low, outside the claim)

The committed `boot-send-classes.txt` shows `unparsed_send_lines=1` for boots -2, -1 and 0. These are almost
certainly earlyoom's startup threshold line, `main.c:414` "sending SIGTERM when mem avail <= …", which starts with
`sending SIG` (`boot-send-classes.py:45-47`). There is one per invocation, and boots -2, -1 and 0 each had one
invocation. [INFERENCE: matched by prefix count, not by printing the line.] They are not missed sends.

## Checks for the main agent

- `python3 -I -B /fast/scratch/hyaku/mori-r27/CriticCeilingInference/ceiling.py` prints the per-boot kernel, swap and
  invocation aggregates and the band counts above (aggregates only).
- `bash .ufo/waves/round-27/count-c1.sh <tip>` after any edit to the entry or SKILL.md, and the lane retention scan
  (must stay at 4 or below).
