# AttackRow08 — field-count support and version boundary

Scope: decision-table row 8, `corpus/knowledge/disk-write-rate-r33.md:26`, at assigned revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` (working-tree copies read as authorized). Findings only; no C1 or admission judgment.

Axes: depth (technical accuracy and complete quotation support), calibration (documentation claims versus actual kernel output), operability (field selection). Constraints applied: R-J at `.ufo/waves/round-33/contract.md:44-50` and A1 at `:119-123`.

## Per-fact table

The row cites only S187. Its four Gate quotes are at `corpus/lessons/round-33.md:22`; I opened all of `corpus/evidence/sources-r33/S187.src:1-43`, including every quote's surroundings. Locators below are relative to the lane.

| Fact | Quote or NOT STATED | File:line |
|---|---|---|
| Observation: `/proc/diskstats` has lines containing fields | “The /proc/diskstats file displays the I/O statistics of block devices. Each line contains the following 14 fields:” | `corpus/evidence/sources-r33/S187.src:5-7` |
| Observation: those values are whitespace-separated | **NOT STATED.** The entire cited copy describes field names/counts, not their delimiter. Whitespace in the documentation's field-list formatting is not a statement of the exported line's encoding. | `corpus/evidence/sources-r33/S187.src:1-43` |
| Reading: the ABI describes a 14-field base | “Each line contains the following 14 fields:” | `corpus/evidence/sources-r33/S187.src:6-7` |
| Reading: sectors written is field 10 | “10 sectors written” | `corpus/evidence/sources-r33/S187.src:19` |
| Reading: kernels 4.18 and later append four discard fields | “Kernel 4.18+ appends four more fields for discard” — **stated, but contradicted by tagged kernel code below** | `corpus/evidence/sources-r33/S187.src:26` |
| Reading: those fields follow the base and total 18 | “tracking putting the total at 18:” and the numbered entries “15 discards completed successfully” through “18 time spent discarding” | `corpus/evidence/sources-r33/S187.src:27,30-33` |
| Reading: kernels 5.5 and later append two flush fields | “Kernel 5.5+ appends two more fields for flush requests:” | `corpus/evidence/sources-r33/S187.src:36` |
| Reading: the flush fields follow the discard fields | “19 flush requests completed successfully” and “20 time spent flushing”, following discard positions 15–18 | `corpus/evidence/sources-r33/S187.src:30-40` |

## Findings

### F1 — major: the quoted 4.18 boundary is an upstream documentation error

Attack: `corpus/knowledge/disk-write-rate-r33.md:26`, specifically “kernels 4.18 and later add four discard fields”. The same claim is propagated by `corpus/SOURCES.md:193` and the S187 Gate quote at `corpus/lessons/round-33.md:22`.

Strong counterexample: **mainline Linux v4.18 prints 14 fields, not 18**. Its actual `diskstats_show` format is:

```c
seq_printf(seqf, "%4d %7d %s %lu %lu %lu "
           "%u %lu %lu %lu %u %u %u %u\n",
```

Evidence: [v4.18 block/genhd.c, diskstats_show](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/genhd.c?h=v4.18), opened at lines 1330–1358. There are 14 conversions; the final arguments are `inflight[0]`, `io_ticks`, and `time_in_queue`, followed by the call's closing parenthesis. No discard values follow them.

The adjacent release changes this printer to 18 fields:

```c
seq_printf(seqf, "%4d %7d %s "
           "%lu %lu %lu %u "
           "%lu %lu %lu %u "
           "%u %u %u "
           "%lu %lu %lu %u\n",
```

Evidence: [v4.19 block/genhd.c, diskstats_show](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/genhd.c?h=v4.19), opened at lines 1330–1367. Its four final arguments read `STAT_DISCARD` ios, merges, sectors, and milliseconds. The committed introducing patch shows precisely the 14-to-18 conversion change at `corpus/evidence/sources-r33/S189.src:148-171`, while its documentation hunk incorrectly says “4.18+” at `:53-59`.

This is not merely a stale base-field sentence: [the v4.18 ABI file](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/ABI/testing/procfs-diskstats?h=v4.18) lists only 14 fields, whereas [the v4.19 ABI file](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/ABI/testing/procfs-diskstats?h=v4.19) introduces the erroneous “4.18+” text.

Impacted axes: depth and calibration. Literal quote support exists for the erroneous boundary, so this is a technical-truth defect, not a claim that S187 fails to contain those words. Documentation authority must not conceal the contradictory printer.

Smallest safe correction preserving release information: replace the 4.18 boundary with the observed v4.18/v4.19 distinction and commit/register/cite those tagged printer sources. **Do not merely change 4.18 to 4.19 while leaving S187 as sole support:** that would introduce a new R-J support gap.

### F2 — minor wording defect with a strict R-J consequence: delimiter claim lacks its own citation

Attack: `corpus/knowledge/disk-write-rate-r33.md:26`, observation “whitespace-separated values”. Evidence: the complete sole cited copy, `corpus/evidence/sources-r33/S187.src:1-43`, contains no delimiter statement; tool `grep(pattern="white|separat", case=false, path="corpus/evidence/sources-r33/S187.src")` returned `No matches found`.

The delimiter is real in the kernel printer: `seq_printf(seqf, " %pg", hd)` and the subsequent `seq_put_decimal_ull(seqf, " ", ...)` calls explicitly emit spaces (`corpus/evidence/sources-r33/S182.src:1381-1408`). But S182 is not a source row 8 cites. Importing that evidence to rescue the existing row would violate R-J's uncited-source exclusion (`.ufo/waves/round-33/contract.md:47-50`).

Impacted axis: depth/source completeness. Smallest correction: observation → **“The number of fields on a `/proc/diskstats` line”**. Alternatively, cite S182 and locate the emitter evidence, retaining the original observation.

## Does the verdict follow from the reading?

**Yes, as a layout-based reporting rule.** The described base and extensions give 14, 18, and 20 positions; appending values leaves position 10 unchanged (`S187.src:19,26-40`). A missing field supplies no numeric measurement, so reporting it as unexported rather than zero adds no measured-value fact. This does not cure the unsupported delimiter detail or the false release boundary.

No extra claim that absent counters mean the device cannot perform discard/flush should be inferred: the row says “not exported”, not “unsupported by the device” (`disk-write-rate-r33.md:26`).

## Other attempted breaks

- **Current kernel path:** v7.2 emits discard and flush positions unconditionally before the newline (`S182.src:1401-1409`); there is no per-device branch there omitting the tail. This is consistent with the layout rule, not an additional defect.
- **Flush boundary:** [v5.4 diskstats_show](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/genhd.c?h=v5.4), opened at 1350–1490, ends with four discard values (18 fields); [v5.5 diskstats_show](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/block/genhd.c?h=v5.5), same range, adds `STAT_FLUSH` ios and milliseconds (20 fields). No contradiction found for 5.5. The committed patch likewise adds those arguments at `S188.src:174-181`.
- **Ancient partitions:** `S181.src:135-150,165-166` describes four-statistic partitions before the full set returned in 2.6.25. Sysstat 12.8.0 still has `else if (i == 7)` and assigns the seventh total field to `wr_sectors` (`S190.src:852-860`). This defeats a claim that 14/18/20 cover every historical partition format, but the row makes no such exhaustiveness claim and the entry warns earlier kernels can differ (`disk-write-rate-r33.md:55-56`). No additional defect assigned.

## Minimal source-only rewrite

If release-boundary teaching is removed rather than repaired with new committed citations, the existing S187 alone supports this replacement:

- Observation: **The number of fields on a `/proc/diskstats` line**
- Reading: **The ABI documents a 14-field base layout, sectors written at position 10, a four-field discard extension at positions 15–18, and a further two-field flush extension at positions 19–20.**
- Verdict: unchanged.
- Sources: S187.

That is a source-only alternative, not a repaired version history. Preserving the latter requires the F1 correction and added printer evidence above.

## A1 six-word check (exercised)

Executed the following bounded command against the original row and all four S187 Gate quotes (same `[a-z0-9_]+`, lowercased token rule as `count-c1-a1.py:86-87`):

```sh
timeout 30s prlimit --as=268435456 --cpu=15 python3 -c 'import pathlib,re; root=pathlib.Path("/home/vgpnk/Projects/shokunin/mori-shokunin"); entry=(root/"corpus/knowledge/disk-write-rate-r33.md").read_text(); row=next(x for x in entry.splitlines() if x.startswith("| 8 |")); reading=row.split("|")[3].strip(); gate=next(x for x in (root/"corpus/lessons/round-33.md").read_text().splitlines() if x.startswith("| S187 |")); qs=re.findall(r"\(\d+ words\): \"([^\"]*)\"",gate); words=lambda x: re.findall(r"[a-z0-9_]+",x.lower()); grams=lambda x: {tuple(words(x)[i:i+6]) for i in range(len(words(x))-5)}; hits=sorted(grams(reading)&set().union(*(grams(q) for q in qs))); print("row=8 cited_ids=S187"); print("reading_words="+str(len(words(reading)))); print("gate_quotes="+str(len(qs))); print("six_word_matches="+str(len(hits))); [print(" ".join(h)) for h in hits]'
```

Observed output:

```text
row=8 cited_ids=S187
reading_words=37
gate_quotes=4
six_word_matches=0
```

Checks not claimed: no judge, C1 counter, build, test suite, or live-device probe was run. Initial raw.githubusercontent.com reads for the four historical ABI tags returned HTTP 429; ordinary git.kernel.org reads supplied the historical evidence above. No bot challenge was bypassed. No tools installed or updated; no background jobs started; no lane edits beyond this report.
