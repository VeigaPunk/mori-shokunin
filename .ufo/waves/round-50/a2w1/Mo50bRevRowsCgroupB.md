# Mo50bRevRowsCgroupB — entailment review of claims-table rows 5–7 (S489), mori round 50 wave a2w1

Seat: Mo50bRevRowsCgroupB (leaf reviewer, godspeed). Scope: rows 5–7 of the claims table of
`corpus/knowledge/oom-memcg-stat-r50.md` at 487941b9395e89678af0053cc443cdb49cdee6e3, each judged against
the committed copy `corpus/evidence/sources-r50/cgroup-v2.7.2.html` with 15+ lines of surrounding text read.
Host: MACHINE_ID. No tool was installed or upgraded (none needed). Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bRevRowsCgroupB/` was created for TMPDIR only and removed at the end.
No kernel log, journal or cgroup state was read; only repo files.

## Bytes verified before judging

- `git diff --stat 487941b9395e89678af0053cc443cdb49cdee6e3 HEAD -- corpus/evidence/sources-r50/cgroup-v2.7.2.html corpus/knowledge/oom-memcg-stat-r50.md` → empty output, exit 0. Working tree HEAD is 4548a34d, but both files are byte-identical to the landed revision, so the on-disk copy reviewed below is the landed copy.
- `sha256sum corpus/evidence/sources-r50/cgroup-v2.7.2.html` → `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34`, equal to the record in `.ufo/waves/round-50/evidence/freeze-sha256.txt`.
- Entry line map at 487941b (read via `git show`): table header line 19, separator 20, rows 1–22 at lines 21–42. Rows under review: row 5 = entry line 25, row 6 = entry line 26, row 7 = entry line 27. All three cite S489, as assigned.

## Row 5 — entry line 25: the `kernel` key

- Claim: "The kernel key aggregates kernel_stack, pagetables, percpu, vmalloc and slab, and each of those five is also printed under its own name."
- Quote: `kernel (npn) Amount of total kernel memory, including (kernel_stack, pagetables, percpu, vmalloc, slab) in addition to other kernel memory use cases.`
- Location: cgroup-v2.7.2.html lines 1415–1417, the `<dt>kernel (npn)</dt>` entry inside the `memory.stat` key list (section opens `<dt>memory.stat</dt>` at line 1393).
- Context read (1400–1432, plus the slab block 1471–1480): after the npn-tag note (1401–1403) the list runs anon, file, then `kernel (npn)` (the quote), then the five sub-keys as separate `<dt>` entries of the same list: `kernel_stack` 1419 ("Amount of memory allocated to kernel stacks."), `pagetables` 1421, `sec_pagetables` 1423, `percpu (npn)` 1427, `sock (npn)` 1430, `vmalloc` 1432 ("Amount of memory used for vmap backed memory."), and further down `slab_reclaimable` 1472, `slab_unreclaimable` 1475, `slab (npn)` 1478 ("Amount of memory used for storing in-kernel data structures.").
- Verdict: **SUPPORTED**.
- Reasoning: the quote says the kernel amount is "total kernel memory, including (the five) in addition to other kernel memory use cases" — the five are components inside a larger total, which is what "aggregates" asserts; the entry's own reading rule ("`kernel` already contains … summing every key double counts kernel memory") reads it the same way. The second assertion ("each of those five is also printed under its own name") is not carried by the quote alone but is proven by the surrounding list — all five exist as own `<dt>` keys in the same `memory.stat` list (1419, 1421, 1427, 1432, 1478). The assignment's standard is quote plus context, so it stands. No replacement cell needed.
- Nomenclature note: "aggregates" could be misread as "is the exact sum of"; the source's "in addition to other kernel memory use cases" makes it containment plus remainder (kernel ≥ the five). The claim does not say "sum", so there are no words to cut.

## Row 6 — entry line 26: parse by key, not position

- Claim: "A parser must match key names, because a newer kernel can insert a counter between existing lines."
- Quote: `Don’t rely on items remaining in a fixed position; use the keys to look up specific values!`
- Location: cgroup-v2.7.2.html lines 1399–1400 — first of two occurrences; this one is the `memory.stat` preamble (section dt at 1393), immediately preceded at line 1398 by "The entries are ordered to be human readable, and new entries can show up in the middle."
- Context read (1384–1414): `memory.events` list closes at 1392; `memory.stat` dt 1393; intro 1394–1396; "All memory amounts are in bytes." 1397; entries-ordered sentence 1398; the quote 1399–1400; npn tag note 1401–1403; the `<dl>` key list follows (anon, file precede the `kernel (npn)` entry at 1415).
- Verdict: **SUPPORTED**.
- Reasoning: "use the keys to look up specific values" prescribes key-based lookup over positional reading, i.e. a parser must match key names; the immediately preceding sentence "new entries can show up in the middle" is the source's own statement that entries can appear between existing ones, and in kernel documentation that is the newer-kernel case. The claim is that sentence plus the quote, not more than it. No replacement cell needed.
- Occurrence note: the same two sentences repeat at lines 1604–1606 inside the `memory.numa_stat` section (followed there by "The entries can refer to the memory.stat."). The row is anchored to `memory.stat` parsing and matches the first occurrence; quote uniqueness is a table-level requirement (no other row carries this quote), so the double occurrence does not touch any frozen predicate. Informational only.

## Row 7 — entry line 27: `oom_kill` semantics

- Claim: "A rising oom_kill count does not prove a kernel memcg OOM, because the field counts kills by any kind of OOM killer."
- Quote: `The number of processes belonging to this cgroup killed by any kind of OOM killer.`
- Location: cgroup-v2.7.2.html lines 1378–1379, the `<dt>oom_kill</dt>` entry of the `memory.events` list (section opens `<dt>memory.events</dt>` at line 1346).
- Context read (1363–1394): preamble 1346–1353 includes "Note that all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy."; the list runs low, high, max, `oom` (with its own not-raised caveat), `oom_kill` 1378–1379 (the quote), `oom_group_kill` 1381 ("The number of times a group OOM has occurred."), `sock_throttled` after.
- Verdict: **SUPPORTED**.
- Reasoning: the field's definition counts processes of the cgroup killed "by any kind of OOM killer", and its scope is process membership ("belonging to this cgroup"), not charge — so a global OOM kill, or a memcg OOM charged to a different cgroup, that takes a process of this cgroup raises the same counter. A rising count therefore does not prove the kill was a memcg OOM charged here, which is exactly what the claim says; "rising" adds nothing beyond an increment, since the field is a plain count. No replacement cell needed.
- Reinforcing context (not cited by the row): the section preamble (1350–1353) makes all `memory.events` fields hierarchical, so a kill in a descendant cgroup also raises this cgroup's `oom_kill` — one more reason the count is not memcg-OOM evidence for this cgroup. The claim stands without it.

## Floor check of the three claim cells (informational)

The frozen counter scored the table `C2=met claims=22 located=22` at 487941b, so all rows already pass the ≥6-word and ≥3-new-3+-letter-word floors; this seat changes no claim cell, so no replacement cell is proposed. Spot check by eye: row 5 carries many words absent from its quote (key, aggregates, five, also, printed, under, own, name …); row 6 (parser, must, match, names, newer, kernel, insert, counter, between, existing, lines); row 7 (rising, count, prove, memcg, because, field, counts). The floor is a floor, not entailment — the per-row verdicts above are the entailment check the counter cannot make.

## Findings

- LOW — `corpus/evidence/sources-r50/cgroup-v2.7.2.html` lines 1604–1606: row 6's quote is not source-unique (repeats in the `memory.numa_stat` section). No frozen predicate is affected (quote uniqueness is table-scoped); informational.
- LOW — `corpus/knowledge/oom-memcg-stat-r50.md` line 25: "aggregates" is containment-plus-remainder in the source's wording, not an exact sum; the row is SUPPORTED as worded and no words need cutting.
- LOW — `corpus/knowledge/oom-memcg-stat-r50.md` line 27: stronger supporting context exists than the row uses (`memory.events` fields are hierarchical, HTML lines 1350–1353); the row is SUPPORTED without it; optional strengthening only.
- No HIGH or MED findings. Rows 5, 6, 7: SUPPORTED, SUPPORTED, SUPPORTED. No replacement claim cells required; the landed data needs no correction from this seat.
