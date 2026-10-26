# Mo51ScribeWhatChanges — `## What this changes for mori` draft for `corpus/knowledge/memavailable-estimate-r51.md`

Seat: Mo51ScribeWhatChanges (scribe, leaf, no subagents). Round 51 wave `w1`, lane `mori-shokunin`.
Item: draft a `## What this changes for mori` section (<= 8 lines, fenced) for the r51 entry, opening the five
linked entries and naming, per link, what the entry adds to how mori reads a runway number, with the line relied on.
Report path (this file): `.ufo/waves/round-51/w1/Mo51ScribeWhatChanges.md` — relative to
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

This seat wrote **no** line beginning with the wave's entailment token, cast no vote, and edited no file but this
one. The draft below is text for the L1 to place; nothing was inserted into the entry.

## Bytes read (hashes at read time, 2026-10-26)

`sha256sum` over the six files, exit 0:

```
b04f030d450b5a2f32de9efc84b9862e411a4ef56547307e2c3fec05846d4803  corpus/knowledge/memavailable-estimate-r51.md
2e2f926180c2ce0880a36cab2afd954266c9acb5194377911d8a7c35066d6491  corpus/knowledge/surfaces-r7.md
0b201bd7d9dbacf8b74efa9348914b2f670eb80886231f28d6e2603042c04fbb  corpus/knowledge/observability-surfaces-r2.md
26b22ddf38cdd4da2d7846943089d0e4bf2a05db6a00f6556c41b046cf2976f5  corpus/knowledge/system-pressure-r24.md
94efb7cf6da5e3d1e8ec19ec83135da1d09d76b073f2d68dd166c6b3f31ee93d  corpus/knowledge/userspace-oom-killers-r26.md
9b8453c859d3649b6414cf7dae834ba38d50324319caeb90baeb1067d790fed1  corpus/knowledge/harness-job-capacity-r25.md
```

These are read-time bytes of a working tree the L1 may still edit; they are not the freeze commit's bytes and
are not offered as a freeze receipt. The r51 entry as read is 65 lines (`awk 'NR>=50 && NR<=66'` printed lines
50-65 with 66 empty); the claims table is lines 20-42, claims row 1 at line 22 and row 21 at line 42.

## Draft (8 lines including the heading; append after `## Boundaries`, i.e. after line 65)

```markdown
## What this changes for mori
- `surfaces-r7.md:83-85`, `observability-surfaces-r2.md:234-235`: the census grades `host_mem_avail_pct` against a
  local 10 % floor; rows 1, 6, 8, 13 make that value a model, so a low row is not by itself pressure [INFERENCE].
- `system-pressure-r24.md:176`: PSI `avg10` is decayed stall time, not startable bytes — `PRESSURE_OK` is no runway.
- `userspace-oom-killers-r26.md:57-60`: earlyoom's "mem avail %" divides by `MemAvailable + AnonPages`, not `MemTotal`,
  so it is not the census figure; at `MemAvailable = 0` no earlyoom kill follows while swap is free (`:53`).
- `harness-job-capacity-r25.md:178`: the gate's absolute floor and the census's 10 % are one estimate in two units;
  neither is calibrated off this host (row 3), so a grant is not a runway claim.
```

Placement is at the end of the file, so the header lines (`source:`/`verified-at:`/`recheck:`), the claims table
and the reading rules are byte-untouched: the per-row hashes `count-c2.py --hashes` prints do not change and no
existing vote on a row is invalidated. [INFERENCE] This rests on the P-C2 predicate hashing the *claim cell*, not
the whole file — I did not run `count-c2.py --hashes` (out of this item's scope; the counter seat owns it).

## Per-link evidence

Each row is one link in the draft: the line I rely on, quoted from the file as read, and what the entry adds.

| # | draft bullet | line relied on (file:line, quoted) | what the entry adds to reading a runway number |
|---|---|---|---|
| 1 | 1 | `surfaces-r7.md:83-85`: "the host's own `MemAvailable/MemTotal` ratio with the scope **named on the row** (`mem_fill_scope=host-ram host_mem_avail_pct=…`, `:750`) against `MORI_MEM_AVAIL_MIN_PCT` (default 10, `:175`) → `MEM_AVAIL_LOW` warn (`:717`)" | the graded quantity is the kernel's estimate, so the existing `threshold_label=local` now covers the model and not only the 10; a low row can be `totalreserve_pages` plus the two `min(half, wmark_low)` holdbacks rather than allocation pressure |
| 1 | 1 | `observability-surfaces-r2.md:234-235`: "else the host `MemAvailable/MemTotal` floor against `MORI_MEM_AVAIL_MIN_PCT` (default 10) → `MEM_AVAIL_LOW` warn (`:717`) with the scope named on the row" | same rule stated in the r2 note's in-place r7 update; the entry does not change it, it names what the number is |
| 2 | 2 | `system-pressure-r24.md:176`: "That there was no stall: `avg10` is a decayed 10-second trend resampled every ~2 s (F4)… That the host is healthy." | the two readings mori prints side by side (`psi_some_avg10`, `host_mem_avail_pct`) are different populations — decayed stall *time* versus an estimate of startable *bytes* — so a clean PSI row cannot stand in for runway, and this is the only link no peer report covers (see §Conflicts) |
| 3 | 3 | `userspace-oom-killers-r26.md:57-60`: "\"mem avail %\" is `MemAvailableKiB * 100 / UserMemTotalKiB`, where *user mem total* is `MemAvailable + AnonPages`" and `:53`: "both memory and swap must be below minimum for earlyoom to act" | the same quantity is divided differently by two readers on this host, and the kill consequence at `MemAvailable = 0` is not automatic: the swap half of earlyoom's conjunction must also be at or below its limit |
| 4 | 4 | `harness-job-capacity-r25.md:178`: "`acquire`, lines 68-96), also requiring `MemAvailable ≥ 6144 MB`" | the seat gate spends an absolute floor on the same estimate the census grades in percent; neither number is derived from the other and row 3 leaves the model's error machine-specific, so a grant is admission, not runway evidence |
| — | 2,3,4 | entry rows 1, 3, 12 and reading rules lines 48-49 | the entry's own support for the last clause of each bullet: row 1 ("An estimate … without swapping"), row 3 ("The impact of those factors will vary from system to system."), row 12 ("if (available < 0) available = 0"), rule at 48-49 ("a host with free swap can keep running past `MemAvailable = 0`, and a reading of 0 is a clamp, not an exact zero") |

Deliberately not in the draft: any restatement of "swaps or kills", any recommendation to change a threshold, and
any number for the model's error (none is measured on this host).

## Findings

1. **LOW — the census's percent floor fires below 11 %, and the row prints the truncated percent.**
   `tools/mori-census.sh:1794` computes `avail_pct=$((mavail * 100 / mtotal))` (bash integer division) and
   `:1795` compares `[ "$avail_pct" -le "$MEM_AVAIL_MIN_PCT" ]` with the default `10` at `:369`. So
   `MEM_AVAIL_LOW` fires for every true `MemAvailable/MemTotal` in `[0 %, 11 %)`, and a true 10.9 % reading is
   printed as `host_mem_avail_pct=10` next to `floor_pct=10`. The entry's rule at line 53-55 ("Report the
   threshold as local") does not mention that the ratio it calls unit-free is emitted as a truncated integer
   percent. No peer report in `w1/` carries this (`grep -n "truncat\|integer division\|mavail \* 100" *.md` —
   only unrelated hits at `Mo51ExecLiveRecheck.md:214`, `Mo51ScoutPriorMentions.md:27`). Concern:
   `corpus/knowledge/memavailable-estimate-r51.md:50` (units rule) and `tools/mori-census.sh:1794-1795`. Named
   limit, not a proposed fix: the census is out of scope for this seat and its floor is the lane's local
   placeholder.
2. **LOW (corroboration, not new) — the row-14 "every meminfo value" / "kB on every meminfo line" wording.**
   Independently reached before reading any peer report, from the frozen copy: `KernelStack`
   (`corpus/evidence/sources-r51/meminfo.c.v7.2:111`), `VmallocTotal` (`:127`) and `HardwareCorrupted`
   (`:137`) print through `seq_printf`, and the hugepage lines come from `hugetlb_report_meminfo(m)` (`:173`),
   so "every meminfo value goes through one helper" (entry line 35, claim row 14) is overbroad. The runway
   consequence is intact: `MemFree` (`:61`) and `MemAvailable` (`:62`) do go through `show_val_kb` (`:28-32`).
   **Already reported at HIGH by wave seat `Mo51CritReadingRules.md:39` with a wider line list** (it adds
   `Zswapped` and the four unit-free `HugePages_*` counts). This seat claims no priority and no severity of its
   own beyond LOW; the L1 should treat it as one finding, not two. Concern: entry line 35 and line 50.
3. **LOW — three memory floors with three denominators now sit in the lane's reading path, and the entry does not
   name the collision.** Census: percent of `MemTotal` (`surfaces-r7.md:83-85`). earlyoom: percent of
   `MemAvailable + AnonPages` (`userspace-oom-killers-r26.md:57-60`). Gate: absolute kB (r25:178; the code at
   `scripts/hyaku/wave-slot.sh:21,68` is `int($2/1024)`, i.e. MiB). My draft's bullets 1, 3 and 4 state the
   distinction but no reading rule does. Also raised by `Mo51ScoutPriorMentions.md:58-60` (LOW, denominator
   collision, and MB vs MiB in the r25 wording); this is corroboration. Concern: entry lines 46-55 (reading
   rules).
4. **No contradiction found between the entry and the five linked entries.** Specifically checked and *not*
   flagged: (a) the intro's "before it swaps or kills" (line 12) is a statement about the lane's runway concept,
   not a claim about what `MemAvailable` measures, and the kernel's own wording agrees ("without causing swapping
   or OOM", quoted in the entry's row 6 quote and `show_mem.c.v7.2`); the entry's rule at 48-49 narrows it later
   without contradicting it. (b) The census's `MemAvailable/MemTotal` percentage and the entry's "unit-free"
   rule (line 50) agree. (c) The gate's absolute floor and the census's percentage are both floors on the same
   estimate — different units, no disagreement. (d) No linked entry anywhere claims `MemFree + Cached` is a valid
   runway figure (`grep -n "MemFree\|free+cached\|Cached"` over the five files plus `SKILL.md` returned nothing),
   so the entry's first reading rule contradicts nothing in the lane's corpus.

## Conflicts to report verbatim (for the canonical judge)

Two peers reached opposite conclusions about the intro sentence (entry line 12); this seat's position is
finding 4(a) above, i.e. no contradiction, so the disagreement is recorded, not resolved here.

- `Mo51RevEntryHeader.md:108-113`: *"Sentence 1 (line 12), \"mori reports resource runway: how much memory the host
  can still give to a new seat before it swaps or kills.\" — a fair gloss of the fleet's runway concept; the
  kernel's own wording is \"without causing swapping or OOM\" (`show_mem.c.v7.2:43-46`; `proc.rst.v7.2`
  MemAvailable). The entry refines the naive reading later (Reading rules row 12: swap excluded by construction;
  0 is a clamp) — the intro does not contradict that. No change needed."*
- `Mo51SimpEntry.md:166-167`: *"**The intro keeps the \"swaps or kills\" framing** even though rows 1 and 6 are the
  only support; that framing is lane context (runway), not a claim, so I did not touch it."*

Both are consistent with "lane context, not a claim"; the second records weaker support than the first ("rows 1
and 6 are the only support"), and neither seat calls it a contradiction.

## Not done / out of scope

- Ran neither counter (`count-c1.py`, `count-c2.py`) and neither `--hashes` mode: not this item's gate, and this
  seat is not a counter seat. UNVERIFIED here: whether the section, once placed, leaves `C2` at
  `failed=entailment` or otherwise — that is the L1's measurement.
- Wrote no entailment-token line and cast no vote; this seat is not an entailment seat.
- Edited no corpus file, no `SKILL.md`/`SHONEN.md`/`SCORECARD.md`/`LOG.md`, no `tools/`, no `corpus/`, and no
  other file under `.ufo/waves/round-51/` (peers' reports were read only).
- Read no kernel message text; no `/proc` write, no service, cgroup, sysctl or package action.
- Installed no tool and upgraded none.

## Scratch and tooling

- Scratch `/fast/scratch/hyaku/mori-r51/Mo51ScribeWhatChanges/` — created with `mkdir -p`, `TMPDIR` set to its
  `tmp/` for the one command that needed it; no clone, no fixture, no file written there; removed before yield
  (`rm -rf`). The largest output this seat produced was the `sha256sum` block above (~500 B).
- `bash scripts/hyaku/disk-guard.sh status` ran before any write-shaped command: no ENOSPC condition observed
  (it listed `/fast/scratch/hyaku` entries; nothing was allocated beyond a directory).
- git/jj: none — no `git` or `jj` command was run by this seat.
- Commands exercised, all read-only, all exit 0 unless noted: `sha256sum` over the six files; `awk`/
  `grep -n`/`sed -n` over the five linked entries, the r51 entry, `corpus/evidence/sources-r51/meminfo.c.v7.2`,
  `tools/mori-census.sh`, `scripts/hyaku/wave-slot.sh`, `PROVINCE.md`; `ls -la` on
  `.ufo/waves/round-51/w1/`; `bash scripts/hyaku/disk-guard.sh status`.
