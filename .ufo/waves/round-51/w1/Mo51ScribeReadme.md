# Mo51ScribeReadme — round-51 w1, build seat (drafting the corpus/README.md round-51 block)

Role: build seat of wave `w1`. Deliverable: a fenced draft of the `## Round-51 coverage additions` block for
`corpus/README.md` — one coverage-map row for `corpus/knowledge/memavailable-estimate-r51.md` on resource-runway
ground, plus a dated append-only Frontier note. The L1 integrates; this seat edited no corpus file.

Read first: `/home/vgpnk/.agents/skills/godspeed/SKILL.md` (via `skill://godspeed`); the frozen contract
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/contract.md`; the house shape from
`corpus/README.md:685-696` read with `:raw` (round 50 block complete) and `:677-684` (round 49 block) for the
count-line convention; the entry `corpus/knowledge/memavailable-estimate-r51.md`; `corpus/SOURCES.md:271-275`
(S492–S496) and `:88` (S082); `.ufo/waves/round-51/evidence/sweep-memavailable.txt`;
`.ufo/waves/round-51/evidence/c2-at-data.txt`; `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` (21 lines).

## Behavior (commands, output, exit code)

All reads absolute or from the lane root; scratch created and removed (see Gates).

1. Shape source — the round-50 block verbatim:
   `read corpus/README.md:685-696:raw` rc=0, ends at line 696
   (`Still frontier: no host OOM block was read …`). Columns of the block:
   `| coverage-map row | entry | ground | sweep |`, then a `Count: …` paragraph, then
   `Dated note (append-only, 2026-10-26): … no frontier row is rewritten. Still frontier: …`.
   Round 49 (`:677-684`) confirms the same four columns and a `Dated note (append-only):` paragraph.

2. Append point — `grep -n '^## Round-50 coverage additions' corpus/README.md` rc=0 → `685:`; `wc -l` rc=0 → `696`.
   So the draft appends after the current last line, separated by one blank line.

3. README untouched by the data commit —
   `git diff --stat aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd 87e0c374537557754bf71dd68036ded3ddc6699c -- corpus/README.md | wc -l`
   → `0` (no diff line): the round-51 block is not in the file yet, so the draft is new text, not a correction.

4. Claim-row count and source coverage (independent of the C2 counter):
   `awk '/^## Claims/{f=1;next} /^## Reading rules/{f=0} f' corpus/knowledge/memavailable-estimate-r51.md` rc=0,
   rows matching `| S49[2-6] |` → `claim_rows=21`; per-source `grep -o 'S49[0-9]' | sort | uniq -c` →
   `5 S492`, `8 S493`, `3 S494`, `2 S495`, `3 S496` — all five sources drawn on, 21 rows.

5. At-data C2 reading (receipt read, not re-executed by this seat — the counter rerun is another seat's item):
   `.ufo/waves/round-51/evidence/c2-at-data.txt` →
   `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment`, `exit=1`.
   `.ufo/waves/round-51/evidence/c2-hashes-at-data.txt` → 21 `row=` lines rc=0.

6. Sweep receipt read: `.ufo/waves/round-51/evidence/sweep-memavailable.txt` —
   `git grep -c -F` for the seven patterns at `aa3af1ec` over `corpus/SOURCES.md corpus/knowledge SKILL.md`:
   `MemAvailable` hits 7 files, one occurrence each (`corpus/SOURCES.md`, `corpus/knowledge/audit-r11.md`,
   `harness-job-capacity-r25.md`, `observability-surfaces-r2.md`, `surfaces-r7.md`, `surfaces-r8.md`,
   `userspace-oom-killers-r26.md`); `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`,
   `34e431b0`, `show_mem.c` → 0 each; the `merge/mori` read-only check → `rc=1 (1 = no file)`.

7. Contexts of the seven `MemAvailable` hits, verified so the draft's sweep cell does not overstate them:
   `grep -n 'MemAvailable' <the seven files>` rc=0 →
   `surfaces-r7.md:83` host `MemAvailable/MemTotal` ratio on the row; `observability-surfaces-r2.md:234` the
   `memory.max`-numeric-else-host-ratio floor; `harness-job-capacity-r25.md:178` the harness acquire gate
   (`MemAvailable ≥ 6144 MB`); `userspace-oom-killers-r26.md:58` earlyoom's own
   `MemAvailableKiB * 100 / UserMemTotalKiB`; `audit-r11.md:342` a fixture meminfo written by a test
   (`'MemTotal: 100000 kB\nMemAvailable: 90000 kB\n'`); `surfaces-r8.md:171` host ratio 49–53%; `corpus/SOURCES.md`
   one row mention. None of the seven defines the number.

8. Dispatcher floor cited in the ground cell, verified before naming it:
   `grep -n 'MEM_MIN_GB' /home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run9.md` rc=0 →
   `60:  MemAvailable < 4 GiB (`MEM_MIN_GB`). A 128-seat wave fills in tranches.` and
   `98: … MEM_MIN_GB stays 4.`

9. S082 disclosure checked: `grep -n '^| S082 ' corpus/SOURCES.md` rc=0 → scope `textual mountinfo field layout only`,
   `sha256 e760f716f8278dee…` — the same bytes as S492, which is what the entry cell says.

10. Source copies match their recorded digests: `cd corpus/evidence/sources-r51 && sha256sum *` rc=0 →
    `34e431b0.patch 9f571a04…`, `meminfo.c.v7.2 d6c58074…`, `mm_inline.h.v7.2 2d4accbb…`,
    `proc.rst.v7.2 e760f716…`, `show_mem.c.v7.2 dba76b26…` — each equal to the sha256 in its SOURCES row
    (S492–S496) and in the entry's `recheck:` list (first four read; the fifth is elided in the entry line and
    confirmed from S496).

11. Disk guard before work: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` rc=0 →
    `/tmp 4% 124.0G`, `/var/tmp 35% 584.8G`, `/fast/scratch/hyaku 25% 605.3G`.

## Draft — `## Round-51 coverage additions` (append to `corpus/README.md` after line 696)

```markdown
## Round-51 coverage additions

| coverage-map row | entry | ground | sweep |
|---|---|---|---|
| resource runway — what the fleet dispatcher's `MemAvailable` floor and the census `MemAvailable/MemTotal` row actually read (the `si_mem_available()` estimate: free pages minus `totalreserve_pages`, plus the file-LRU pages and the reclaimable kernel memory, each less `min(half, the zones' summed low watermark)`, clamped at zero; printed in kB; no swap in the figure) and why `MemFree + Cached` is not that number (tmpfs folios sort onto anon LRU lists while MADV_FREE anonymous folios sort onto the file lists, and `Cached` counts all file pages minus swap cache and buffers) | `knowledge/memavailable-estimate-r51.md` (S492–S496, opened 2026-10-26; S492 shares its URL and bytes with S082 at a different scope) | new ground — no FR row held it; the map held `MemAvailable` only as a value read (`knowledge/surfaces-r7.md:83`, `knowledge/observability-surfaces-r2.md:234`, the dispatcher's `MEM_MIN_GB` floor). States the kernel's model at v7.2, never a host value as typical, and reports rather than configures (`vm.min_free_kbytes`, `watermark_scale_factor`, swap and every limit are tsukuroi's; the floor is the orchestrator's); FR8 stays open — a runway threshold on this figure is a labeled-local threshold on a model | `si_mem_available`, `totalreserve`, `wmark_low`, `folio_is_file_lru`, `34e431b0` and `show_mem.c` → 0 in `corpus/SOURCES.md`, `corpus/knowledge` and `SKILL.md` at `aa3af1ec`; `MemAvailable` occurs in 7 paths (`corpus/SOURCES.md`, `audit-r11.md`, `harness-job-capacity-r25.md`, `observability-surfaces-r2.md`, `surfaces-r7.md`, `surfaces-r8.md`, `userspace-oom-killers-r26.md`) and is never defined there, and read-only `merge/mori` holds no file on it (`.ufo/waves/round-51/evidence/sweep-memavailable.txt`) |

Count: 21 claim rows and 21 located quotes over the five sources — at the data commit `87e0c37`
`python3 .ufo/waves/round-51/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c` prints `C2=unmet claims=21
located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok … dissent=0
failed=entailment` (`.ufo/waves/round-51/evidence/c2-at-data.txt`): every quote resolves in its committed copy,
and the wave's recorded per-row entailment judgment is the one arm still open.

Dated note (append-only, 2026-10-26): round 51 supersedes the resource-runway ground's silence about what
`MemAvailable` is — the dispatcher floor and the census ratio read an estimate, not free memory:
`si_mem_available()` starts from free pages minus `totalreserve_pages`, adds the file LRU pages and the
reclaimable kernel memory each less `min(half, wmark_low)`, and clamps at zero, so the figure is neither
`MemFree + Cached` nor a count of free pages, and a reading of zero is a clamp
(`knowledge/memavailable-estimate-r51.md`, S492–S496); no frontier row is rewritten. Still frontier: no host
`MemAvailable` value is claimed as typical, `totalreserve_pages` is not exported to userspace so the estimate
cannot be recomputed from `/proc/meminfo` alone, the entry claims the v7.2 bytes only, and FR8's calibration
stays open — a floor on this figure is a labeled-local threshold on a model whose holdbacks are
`min(half, the low-watermark sum)` and whose accuracy the proc document says varies from system to system.
```

Integration notes for the L1 (not part of the block):

- The `Count:` paragraph deliberately carries the at-data reading (`C2=unmet … failed=entailment`). Once
  `count-c2.py` prints `C2=met … entailed=21 dissent=0` at the final tip, replace that clause with the printed
  line (round-48's `COUNTER → C2=met claims=15 …` convention). Do not paste a `C2=met` reading the counter has
  not printed.
- The sweep cell keeps the entering rev `aa3af1ec` (the sweep predates the entry), matching round 50's practice
  of naming the pre-data tip.
- The ground cell names the dispatcher floor without a `.scratch` path: scratch pointers are not durable
  evidence (FR9). The receipt for the floor line is item 8 above.

## Gates

- Writes: this report only. `corpus/README.md` was read, never written; no edit to SKILL.md, SHONEN.md,
  SCORECARD.md, LOG.md, `corpus/`, `tools/`, `considerthese/`, or any other file under
  `.ufo/waves/round-51/`.
- Git: read-only (`git diff --stat`, `git log --oneline`, `git rev-parse HEAD`). No add/commit/stash/checkout/
  reset/pull/push, no jj command, no fleet-repo write.
- No subagent dispatched (leaf seat).
- Tooling: nothing installed; no pacman transaction (host-wide pause respected).
- Host: `disk-guard.sh status` rc=0 before work; no `/tmp` evidence used; no journal or kernel-log read; no
  `/proc/meminfo` sample taken (the block quotes no host value).
- Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ScribeReadme/` created with `mkdir -p` (`scratch-ok`, rc=0) and
  removed at the end of this seat; no clone, no fixture repo was made.
- Report-line rule: this report starts no line with the word `ENTAIL` (verified by grep, recorded under
  Findings F5).

## Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/w1/Mo51ScribeReadme.md`.
- Scratch (created, then removed): `/fast/scratch/hyaku/mori-r51/Mo51ScribeReadme/`.
- Read: contract; `corpus/README.md`; the entry; `corpus/SOURCES.md` (S082, S492–S496);
  `corpus/evidence/sources-r51/*` (sha256 only); the sweep and C2 at-data receipts; the dispatcher goal file
  (single `grep`).

## Out of scope

- Integrating the block into `corpus/README.md`, resolving competing drafts, or touching any frontier row —
  the L1's.
- The C2 counter, its predicate, the claim text, entailment votes, both claims' scoring, C1 and its controls —
  other seats' items; the counters are frozen and were not re-executed here.

## Known limits

- The draft reports only what the lane's own receipts and rows show; the claim-row count (21) was re-derived
  independently of `count-c2.py`, but the located/provenance arms are quoted from the at-data receipt, not
  re-run by this seat.
- The sweep cell states the entering-tip absence only; it is not evidence about any other revision or kernel.
- No other w1 draft of this same README block was read (`w1/` held 25 files at write time, none named for a
  README block); if a sibling proposes the same block, the L1 chooses.

## Findings

- **MED — `corpus/README.md:696` (integration):** the at-data C2 reading is `C2=unmet … failed=entailment`
  (`evidence/c2-at-data.txt`, exit 1). A round-51 block that printed a `C2=met` count line today would state an
  unobserved result; the draft keeps the at-data line and marks the replacement step for the L1.
- **LOW — `.ufo/waves/round-51/evidence/sweep-memavailable.txt`:** the seven `MemAvailable` hits are not all
  "read values" — `corpus/knowledge/audit-r11.md:342` writes a fixture meminfo. The draft's sweep cell therefore
  says "occurs in 7 paths … never defined there" rather than "read value".
- **LOW — `corpus/knowledge/memavailable-estimate-r51.md:9` (`recheck:` line):** the line lists five digests in
  one backtick command and is longer than 768 bytes, so a plain read truncates the fifth; the fifth digest is
  confirmed from `corpus/SOURCES.md:275` (S496) and from `sha256sum` of the copy. No defect, but a reader who
  copies the truncated line gets four digests.
- **LOW — `corpus/SOURCES.md:271` (S492):** the row shares URL and bytes with S082 at a different scope; the
  draft discloses this in the entry cell, as round 50 did for S491, so the duplicate-bytes relationship is not
  read as a new source.
- **LOW — this report:** verified that no line starts with the word `ENTAIL` — `grep -c` on this file returns 0
  (run after the final write; the draft's only occurrence of the stem is mid-sentence, "per-row entailment
  judgment", inside the `Count:` paragraph).
