# Mo61ScoutAnchorMap — C2 pointer enumeration checklist (bounded data walk)

Seat: Mo61ScoutAnchorMap-2 (leaf scout; read-only; no VCS mutation, no fleet/sibling writes). Date: 2026-10-30.
Deliverable: the 47 C2 anchors enumerated **exactly as frozen `count-c2.py` does**, one line each:
pointer | r24 claim it supports (≤15 words of the entry) | pinned-copy context at the anchor.
For the scribes drafting `psi-v73-recheck-r61.md`; I draft no rows.

## Method (all read-only; absolute paths)

- Enumeration semantics read from `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py`:
  `FILES = [psi.rst, psi.c, psi_types.h, cgroup-v2.rst, Kconfig, kernel-parameters.txt]`;
  `NAMES = re.compile("(" + "|".join(re.escape(f) for f in FILES) + "):(\\d+)(?:-(\\d+))?")`;
  `enumerate_pointers` = `NAMES.finditer` over the entry bytes, key `file:start` or `file:start-end`,
  deduped preserving first occurrence.
- Authoritative count: frozen counter run at the entering revision —
  `TMPDIR=<scratch> python3 .ufo/waves/round-61/count-c2.py 325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r61/Mo61ScoutAnchorMap-2`
  → `C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent` rc=1 (expected red-before; entry exists, ledger does not).
- Independent replication: extractor script in scratch (same regex, same `git show` bytes) → `pointers=47`. Agree.
- Entry bytes identical at entering rev, freeze rev, and worktree: sha256 `26b22ddf38cdd4da2d7846943089d0e4bf2a05db6a00f6556c41b046cf2976f5` (`git show 325f7e63…:corpus/knowledge/system-pressure-r24.md` == worktree file). Enumeration is revision-stable for this round.
- Pinned copies: all six on-disk files under `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r61/` match the frozen PINS in count-c2.py byte-for-byte (psi.rst 11c6b712…, psi.c c4edc1e7…, psi_types.h 483269b2…, cgroup-v2.rst 2750c11a…, Kconfig d37de2a1…, kernel-parameters.txt b5a13c03…). Pin sizes: psi.rst 188 ln, psi.c 1725 ln, psi_types.h 216 ln, cgroup-v2.rst 3581 ln, Kconfig 2368 ln, kernel-parameters.txt 8710 ln. Note: the copies are NOT in the entering rev (first committed by the freeze); read at freeze rev 7370a731abcafc4c803111de7c22cd6264d63be1.
- Disk guard: green (`/fast/scratch/hyaku 55% 368.3G free`). No tools installed (none needed). Scratch cleaned before yield; receipts copied into this report.

Column notes: "claim" = the entry's own words (entry line numbers refer to `system-pressure-r24.md` at sha 26b22ddf…). "context" = the pinned **v7.3** copy's content at the anchor lines — the bytes a row's quote is validated against — plus a same/moved hint. Hints are my [INFERENCE] from entry-prose vs pinned-byte comparison, not drafted rows.

## The 47-pointer checklist (first-occurrence order)

| # | pointer | r24 claim (entry:NN) | pinned v7.3 context at anchor |
|---|---|---|---|
| 1 | psi.rst:60-65 | averages are ratios over ten/sixty/300 s windows; total stall in us (19,94) | "The ratios (in %) are tracked as recent trends…" / "total absolute stall time (in us)…" → same |
| 2 | psi.c:342-360 | averages are exponentially decayed (19,97) | calc_avgs() body: calc_load with EXP_10s/60s/300s → same |
| 3 | psi.c:1268-1270 | averages recomputed on a read only when next 2-second update due (21) | collect_percpu_times + `if (now >= group->avg_next_update)` guard → same |
| 4 | psi.c:1372-1373 | v7.2 code enforces only 0 < window ≤ 10 s (23,133) | `if (window_us == 0 \|\| window_us > WINDOW_MAX_US) return ERR_PTR(-EINVAL);` → same |
| 5 | psi.c:1379-1380 | unprivileged writers: window must be a multiple of 2 s (23) | `if (!privileged && window_us % 2000000) return ERR_PTR(-EINVAL);` → same |
| 6 | psi.c:1712 | psi_proc_init tests psi_enable directly (26) | 1712 = `if (psi_enable) {` — 3-word line; **same-row impossible** (T2), loc 1712-1713 |
| 7 | psi.c:1017 | code charges IRQ time only to a non-idle current task (32,177) | 1017 = `if (!curr->pid)` — 3-word line; **same-row impossible** (T2), loc 1016-1018 |
| 8 | psi.c:1540 | one of the four psi_show(m, &psi_system, …) readers (42,89,148,241) | `return psi_show(m, &psi_system, PSI_IO);` — exactly 5 words → same |
| 9 | psi.c:1686 | irq reader also passes psi_system (42) | `return psi_show(m, &psi_system, PSI_IRQ);` — exactly 5 words → same |
| 10 | psi.rst:36-38 | exactly three files named: cpu, memory, io under /proc/pressure/ (66) | 36 blank; 37-38 = "Pressure information for each resource is exported…" → same (quote from 37-38) |
| 11 | psi.c:1710-1721 | kernel creates a fourth file pressure/irq under CONFIG_IRQ_TIME_ACCOUNTING (68) | psi_proc_init body incl. `proc_create("pressure/irq", 0666, …)` in ifdef → same |
| 12 | Kconfig:730-731 | build option's help text likewise names only cpu, memory, io (70) | 730-731 = `bool "Pressure stall information tracking"` + `select KERNFS`; the cpu/memory/io help prose sits just below (~735-742, [INFERENCE]) — quote the bool line (exactly 5 tokens) for same, or moved loc below |
| 13 | psi.rst:40-43 | each file holds `some` and `full` lines in that exact format (75) | literal block: "some avg10=0.00 … total=0" / "full …" → same |
| 14 | psi.c:1290-1296 | one seq_printf emitter, two fraction digits, `some` then `full` (78) | seq_printf "%s avg10=%lu.%02lu … total=%llu\n" + args → same |
| 15 | psi.rst:45-56 | some = at least some tasks stalled; full = all non-idle simultaneously (81) | definitions verbatim at 45-55 (56 blank) → same |
| 16 | psi.rst:57-59 | CPU full undefined at system level, zeroed since 5.13 (85) | "CPU full is undefined at the system level, but has been reported since 5.13…" (59 blank) → same |
| 17 | psi.c:1282-1288 | kernel skips the read so system CPU full stays zero (87) | comment + `if (!(group == &psi_system && res == PSI_CPU && full))` guard → same |
| 18 | psi.c:1284-1288 | total exported in us via div_u64(…, NSEC_PER_USEC) (96) | same block's `total = div_u64(group->total[PSI_AVGS][…], NSEC_PER_USEC)` → same; quote distinct from row 17 |
| 19 | psi.c:160-164 | sampled at PSI_FREQ (2*HZ+1), i.e. 2-second intervals (98) | `#define PSI_FREQ	(2*HZ+1)	/* 2 sec intervals */` + EXP_ defines (TAB bytes) → same |
| 20 | psi.c:1268 | each read collects the per-CPU times feeding total (21,99) | 1268 = `collect_percpu_times(group, PSI_AVGS, NULL);` — 3 tokens; **same-row impossible** (T2), loc 1267-1269 |
| 21 | psi.c:1269-1270 | averages recomputed when the next 2-second update is due (100) | guard + `group->avg_next_update = update_averages(group, now);` → same; quote distinct from row 3 |
| 22 | psi.c:600-602 | averages also updated by the averages work item (101) | work item: update_triggers + update_averages under same guard → same |
| 23 | psi.c:1273-1296 | only_full for IRQ; print loop emits only a `full` line (106) | ifdef only_full + `for (full = 0; full < 2 - only_full; full++)` + seq_printf → same; quote distinct from rows 14/17/18 |
| 24 | psi.c:1032-1042 | IRQ accounting path adds only to PSI_IRQ_FULL (107) | `groupc->times[PSI_IRQ_FULL] += delta;` inside for_each_group → same |
| 25 | psi.c:1364-1367 | IRQ trigger naming `some` refused with -EINVAL (109) | ifdef + `if (res == PSI_IRQ && --state != PSI_IRQ_FULL) return ERR_PTR(-EINVAL);` → same |
| 26 | psi_types.h:41-49 | state enum has PSI_IRQ_FULL, no IRQ some, under ifdef (110) | enum psi_res 41-49 with `PSI_IRQ` inside `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` (PSI_IRQ_FULL is at 57-70, NOT enumerated — orphan trap T9) → same |
| 27 | psi.c:1717-1719 | pressure/irq created only under CONFIG_IRQ_TIME_ACCOUNTING (113) | ifdef + proc_create("pressure/irq", …) + endif → same |
| 28 | psi.c:1260-1263 | irq read returns -EOPNOTSUPP when IRQ time accounting off (116) | `if (!irqtime_enabled() && res == PSI_IRQ) return -EOPNOTSUPP;` → same |
| 29 | psi.c:1257-1258 | psi_disabled static key makes every read fail EOPNOTSUPP (120) | `if (static_branch_likely(&psi_disabled)) return -EOPNOTSUPP;` → same |
| 30 | psi.c:228-240 | key enabled at init when psi_enable is false (121) | psi_init: `static_branch_enable(&psi_disabled)` when !psi_enable → same |
| 31 | psi.c:149-158 | psi_enable false via CONFIG_PSI_DEFAULT_DISABLED or psi= param (123) | ifdef default + setup_psi + `__setup("psi=", setup_psi)` → same |
| 32 | psi.c:1553-1566 | open handlers are plain single_open; failure surfaces on read (124) | psi_io/memory/cpu_open = single_open(...) → same |
| 33 | psi.c:1711-1719 | proc files created only when psi_enable is true (126) | `if (psi_enable) {` + proc_create block → same; quote distinct from rows 6/11 |
| 34 | kernel-parameters.txt:5505-5507 | psi= documented: enable/disable pressure stall tracking, format \<bool\> (127) | **MOVED**: pinned 5505-5507 = `proc_mem.force_override=` block; `psi=` now at **5540-5542** (`psi=		[KNL] Enable or disable pressure stall information` / `tracking.` / `Format: <bool>`) → moved, loc kernel-parameters.txt:5540-5542 |
| 35 | Kconfig:743-760 | CONFIG_PSI_DEFAULT_DISABLED makes psi=1 the opt-in (127) | 743-760 = PSI help tail + `config PSI_DEFAULT_DISABLED` block ("enabled through passing psi=1") → same |
| 36 | psi.rst:67-88 | trigger registered by writing some/full amount window; poll the descriptor (132) | "Monitoring for pressure thresholds" section + format line → same; quote distinct from row 43 |
| 37 | psi.rst:102-104 | documentation states windows ranging from 500ms to 10s (133) | "The kernel accepts window sizes ranging from 500ms to 10s…" → same |
| 38 | psi.c:167 | WINDOW_MAX_US 10000000 caps window at 10 s (134) | `#define WINDOW_MAX_US 10000000	/* Max window size is 10s */` (TAB bytes) → same |
| 39 | psi.c:1596-1598 | second trigger on same descriptor fails EBUSY (136) | `mutex_unlock(&seq->lock); return -EBUSY;` → same |
| 40 | psi.rst:178-187 | cgroup2 tracks PSI per cgroup; same file format (142) | "Cgroup2 interface" section verbatim → same |
| 41 | cgroup-v2.rst:1066-1081 | cgroup.pressure: per-cgroup, non-hierarchical switch, default 1 (143,242) | cgroup.pressure section 1066-1081 verbatim ("This control attribute is not hierarchical…") → same |
| 42 | psi.c:408-410 | total accumulates monotonically; no decrement path (154) | `/* total= */` loop: `group->total[aggregator][s] += …` → same |
| 43 | psi.rst:70-88 | only thresholds in the docs are the user's trigger examples (160) | trigger registration + examples "100ms … 500ms window" / "some 150000 1000000" → same; quote distinct from row 36 |
| 44 | psi.c:845-857 | writing 0 stops psi_system recording via psi_group_change (225) | !group->enabled flush block ("On the first group change after disabling PSI…") → same |
| 45 | psi.c:551 | totals freeze; averages decay toward zero after the switch (225) | `sample = group->total[PSI_AVGS][s] - group->avg_total[s];` — exactly 5 tokens → same |
| 46 | psi.c:1538-1550 | holds two full readers and a signature, not four readers (241) | psi_io_show/psi_memory_show/psi_cpu_show + psi_show calls 1540/1545/1550 → same (as r27-corrected) |
| 47 | cgroup-v2.rst:1066-1087 | each controller pressure file has its own section; irq.pressure at 1083-1087 (242) | 1066-1081 cgroup.pressure; 1083-1087 `irq.pressure` "Shows pressure stall information for IRQ/SOFTIRQ" → same |

Summary hint distribution: 46 anchors carry claim-matching text at the pinned anchor (same-compatible); 1 anchor moved (row 34). Rows 6/7/20 are same-**incompatible** under the counter's quote floor even though content matches (see T2). All hints [INFERENCE] pending the scribes' own byte checks.

## Mechanical traps for the drafters (derived from count-c2.py measure(), lines 124-186)

- **T1 anchor exactness.** Exactly 47 row anchors, one each: duplicate anchor → `dup_anchor`; missing → `rows_missing:…`; extra → `rows_orphan:…`; and `len(rows) != len(pointers)` → `rows_ne_pointers`. Row order in the ledger is free (set comparison).
- **T2 five-word floor (hard).** Counter enforces `5 <= wordcount(q) <= 25` (code, not just the contract's ≤25). Three `same` anchors are 3-word single lines and can never pass as `same`: psi.c:1712 (`if (psi_enable) {`), psi.c:1017 (`if (!curr->pid)`), psi.c:1268 (`collect_percpu_times(group, PSI_AVGS, NULL);`). A `same` row's hay is the anchor range only — it cannot be widened. Fix: mark `moved` (or `changed`) with a loc spanning the neighbouring lines so the joined hay crosses a `\n` and yields ≥5 whitespace tokens; counter joins lines with `"\n"`, so a quote spanning the newline is one substring. Workable locs from the pinned bytes: psi.c:1712-1713 (adds `proc_mkdir("pressure", NULL);`), psi.c:1016-1018, psi.c:1267-1269 (adds `if (now >= group->avg_next_update)`).
- **T3 the one moved pointer.** Row 34: `kernel-parameters.txt:5505-5507` holds `proc_mem.force_override=` in v7.3; `psi=` sits at 5540-5542. Suggested shape: `| kernel-parameters.txt:5505-5507 | moved | kernel-parameters.txt:5540-5542 | ` + a ≥5-word byte substring of 5540-5542 (e.g. "Enable or disable pressure stall information", 7 words).
- **T4 byte-exactness.** Quotes must be substrings of `"\n".join(lines[lo-1:hi])` of the PINNED bytes. psi.c defines carry TABs (rows 19, 38); rst literal blocks carry leading spaces (row 36/43, line 83). Only leading/trailing whitespace of the whole quote is stripped before matching; interior bytes must be exact. Do not re-type quotes — copy from the pinned copies.
- **T5 pairwise-distinct quotes.** Overlapping anchor ranges (rows 3/21, 17/18, 14/23, 33/6/11, 36/43) still need globally distinct quote strings after strip (`quote_dup` otherwise).
- **T6 provenance.** Ledger head (first 2000 bytes) must carry line-anchored `source:`, `verified-at:`, `recheck:` — else `provenance`.
- **T7 SOURCES binding.** Rows must cite ≥4 of the six copies (`sources_floor`); each cited copy needs a `corpus/SOURCES.md` line containing `corpus/evidence/sources-r61/<f>` AND `| S` AND `| mined |` AND `psi-v73-recheck-r61.md` (used-by) — all in the same line (`rows_src:<f>`).
- **T8 row grammar.** `ROW` regex: anchor `file:digits[-digits]`, status ∈ {same,moved,changed}, loc cell same grammar or `-`, quote in backticks on one line. A markdown header row like `| anchor | status | loc | quote |` does not match the grammar (safe).
- **T9 comma-list trap.** `psi.c:1540,1545,1550` (entry:42) enumerates ONLY `psi.c:1540`; likewise entry:19's `psi.c:342-360,408-411,551,572` enumerates only `psi.c:342-360`, entry:110's `psi_types.h:41-49,57-70` only `psi_types.h:41-49`, entry:225's `psi.c:551,1269-1270` only `psi.c:551`. Rows for the un-enumerated elements (e.g. psi.c:1545, psi.c:572, psi_types.h:57-70) are orphans and fail the counter.
- **T10 distinct keys.** `psi.c:1268` and `psi.c:1268-1270` are separate anchors — both need rows.
- **T11 floor.** pointers=47 ≥ floor 40 — satisfied; no `--floor` argument needed for the live run (FLOOR_DEFAULT=40).

## Findings (report-only; no fixes applied)

- **F1 (moves).** The v7.2→v7.3 drift visible at the anchors is exactly one moved pointer (row 34, kernel-parameters +35 lines); every other anchor's pinned content still matches its r24 claim text. [INFERENCE from byte comparison above; scribes confirm per-row when picking quotes.]
- **F2 (counter strictness).** T2 makes three content-unchanged anchors structurally unable to be `same` rows — a drafter who marks them `same` gets `quote_words` failures with no honest same-row fix. This is counter behavior, not a defect finding per se; the honest row is `moved`/`changed` with the neighbouring-line loc (semantics: the ≥5-word quotable span now starts on the preceding/following line).
- **F3 (entry self-consistency).** Entry line 110 claims "psi_types.h:41-49,57-70" for the PSI_IRQ_FULL/enum claim, but only 41-49 (the resource enum) is enumerated; the state-enum half (57-70) is unverifiable through this counter. No action possible this round (amendments barred); noted for the lesson.
- No counter defeat attempted beyond the reads above; no pacman/tools installed; no host or service changes; no provider/liveness inference.

## Receipts (copied before scratch cleanup)

```
$ TMPDIR=/fast/scratch/hyaku/mori-r61/Mo61ScoutAnchorMap-2 python3 .ufo/waves/round-61/count-c2.py \
    325f7e639916fcbc77fa2ec7475951a1b86bb1cb --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --scratch /fast/scratch/hyaku/mori-r61/Mo61ScoutAnchorMap-2
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e63…   (rc=1)

$ sha256sum corpus/evidence/sources-r61/{psi.rst,psi.c,psi_types.h,cgroup-v2.rst,Kconfig,kernel-parameters.txt}
11c6b712…  psi.rst / c4edc1e7…  psi.c / 483269b2…  psi_types.h / 2750c11a…  cgroup-v2.rst / d37de2a1…  Kconfig / b5a13c03…  kernel-parameters.txt   (all == PINS)

$ git show 325f7e63…:corpus/knowledge/system-pressure-r24.md | sha256sum
26b22ddf38cdd4da2d7846943089d0e4bf2a05db6a00f6556c41b046cf2976f5   (== worktree file; enumeration revision-stable)

$ grep -n "psi[.=]" corpus/evidence/sources-r61/kernel-parameters.txt  (pinned v7.3)
5540:	psi=		[KNL] Enable or disable pressure stall information
5541:			tracking.
5542:			Format: <bool>
```

Scratch `/fast/scratch/hyaku/mori-r61/Mo61ScoutAnchorMap-2/` cleaned after this write.
