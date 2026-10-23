# CtlGlossaryA1 — no-rate glossary control

Axes: depth discrimination, faithful R-J evidence, and exact-byte restoration. This is one adversarial control, not an admission or the independent C1 judgment.

## Finding F1 — major: a definition-only glossary prints C1=met

Attacks: `.ufo/waves/round-33/contract.md:26-42,119-123` and `.ufo/waves/round-33/count-c1-a1.py:165-192,279-313`. The counter recognizes a decision table by its headers and checks supported spans, but accepts the following state with no write-rate decision in any verdict.

**Yes: the glossary meets the mechanical P-C1-A1 counter.** At sandbox commit `04c02aebac351ce47d08eb98f47d0da81521a7b1`, `corpus/knowledge/disk-write-rate-r33.md:13-23` contains 11 distinct, paraphrased definitions, one each from S180-S190, and every verdict is `Note it.` The title and original source/verified-at/recheck lines are unchanged (`:1-5`); the original decision-bearing body was replaced, not left below the glossary. The only other committed changes supply the requested dispatch and honest self-judgment.

R-J was copied verbatim into sandbox `.ufo/waves/round-33/judge/dispatch.json:6` and `JudgeC1Rows.md:4`:

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or through a source the row does not cite.

The receipt explicitly discloses self-judgment, judges only the glossary, binds its SHA-256, and supplies each row's located span and reasoning (`04c02ae:.ufo/waves/round-33/judge/JudgeC1Rows.md:1-22`). It is not an independent closure-valid judge receipt; no official judgment of the real entry was performed here. The finding is counter discrimination, not a claim that the real entry lacks decisions or that an official judge has accepted this control.

### Glossary source grounding

All locators below have prefix `corpus/evidence/sources-r33/`, at the measured revision and unchanged in the sandbox. The complete quoted spans are committed in the control receipt, rows 1-11 (`JudgeC1Rows.md:10-20`). Code rows define literal assignments or types only; they assert no device-accounting semantics. `Note it.` adds no factual premise or rate choice.

| Glossary row | One definition, honestly self-judged supported | Located source |
|---|---|---|
| 1 | stat text layout: one whitespace-separated line with 17 decimal values | S180.src:21-22 |
| 2 | the two files expose identical 17-statistic contents | S181.src:5-6,22 |
| 3 | inflight receives bdev_count_inflight(hd)'s result | S182.src:1374-1376 |
| 4 | sectors is an unsigned-long array member | S183.src:8-11 |
| 5 | bdev_end_io_acct's sectors argument is unsigned int | S184.src:1100-1101 |
| 6 | blk_account_io_completion's bytes argument is unsigned int | S185.src:856 |
| 7 | one sector's size is 512 = 2**9 bytes | S186.src:26-27 |
| 8 | diskstats field 10 means sectors written | S187.src:1,19-21 |
| 9 | the flush counter counts requests executed by disk | S188.src:72 |
| 10 | discard tracking uses four stats like reads/writes | S189.src:7-10 |
| 11 | ioi means current-sample statistics | S190.src:1151-1152 |

The spans for short code/parameter definitions include adjacent committed text to reach six words; no adjacent fact was added to their readings. The receipt documents this explicitly for rows 3 and 11 (`JudgeC1Rows.md:12,20`). This is not a receipt falsely labeling junk as sourced: each actual definition has a located supporting statement. Independent review of that self-assessment remains unrun.

### Same bounded detector: pristine, glossary, restored

Clone: `/fast/scratch/hyaku/mori-r33/CtlGlossaryA1/clone`. Base: `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. The clone was made with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks` and detached at that exact revision; Git writes occurred only in this clone.

The same command ran once at each state's HEAD (outer 600-second/2-GiB cap retains the requested inner counting command):

```sh
timeout 600 prlimit --as=2147483648 --cpu=540 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1-a1.py HEAD --repo /fast/scratch/hyaku/mori-r33/CtlGlossaryA1/clone
```

Actual pristine output, exit 1 (`/fast/scratch/hyaku/mori-r33/CtlGlossaryA1/pristine.out:1-23`):

```text
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 distinct_sources=yes
dispatch_rule=no judge=absent
unmet_conditions=judge
C1=unmet
```

Actual glossary output, exit 0 (`/fast/scratch/hyaku/mori-r33/CtlGlossaryA1/glossary.out:1-22`):

```text
rows=11 rows_ok=11 distinct_rows=11 distinct_observations=11 short_readings=0
new_id_rows=11 new_ids=11 (S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190)
gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 distinct_sources=yes
rows_without_quote_overlap=0
readings_copying_quotes=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=11 supported_new=11 spans_bad=[] unsupported=[]
skill_rows=5
C1=met
```

Actual restored output, exit 1 (`/fast/scratch/hyaku/mori-r33/CtlGlossaryA1/restored.out:1-23`):

```text
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 distinct_sources=yes
dispatch_rule=no judge=absent
unmet_conditions=judge
C1=unmet
```

**Mutation-test verdict: inconclusive, not killed and not a passing-baseline survivor**, because the pristine revision has no judge receipt. **Adversarial-control result: accepted (C1=met)** with the requested honest self-receipt. Thus A1's non-copying and span conditions do not discriminate these definitions from write-rate decisions; this does not amend the frozen predicate after data. Evidence: the three actual detector outputs above and control entry/receipt at `04c02ae`.

## The REAL entry: decision present row by row

Presence only, not a source-support or correctness judgment. All references below are to `corpus/knowledge/disk-write-rate-r33.md` at `62db24c`. Every listed choice is absent from the control's all-`Note it.` verdict column (`04c02ae`, same path:13-23).

| Real row | Carries a decision the glossary lacks? | Real verdict's choice | Location |
|---|---|---|---|
| 1 | Yes | Convert the sector delta with 512, not the device block size | :19 |
| 2 | Yes | Report completed-write throughput, not submitted data | :20 |
| 3 | Yes | Sum whole disks or partitions, never both together | :21 |
| 4 | Yes | Mark the regressing-counter interval unavailable, not negative/wrapped/zero-filled | :22 |
| 5 | Yes | Report a snapshot queue depth; do not difference it | :23 |
| 6 | Yes | Report io_ticks delta / elapsed milliseconds as a time share, not throughput | :24 |
| 7 | Yes | Do not present write-ticks / elapsed time as a percentage | :25 |
| 8 | Yes | Accept 14/18/20 fields; missing discard/flush fields are not exported, not zero | :26 |
| 9 | Yes | A missing device line is unavailable, not zero writes | :27 |
| 10 | Yes | Exclude discarded sectors from write rate; report separately | :28 |
| 11 | Yes | Read flush counts on whole disks only; do not add them to sectors | :29 |
| 12 | Yes | Choose one parser over the 17 statistics for both interfaces | :30 |
| 13 | Yes | Label the average, not a current rate; require two readings for current rate | :31 |
| 14 | Yes | Do not infer idle from iostat zero without raw counters | :32 |

Row 12 is a parser choice rather than a rate formula, but is still an operational verdict beyond noting a definition (`:30`). This control weakens what the counter certifies; it does not erase the genuine decision-bearing text in the real table.

## Exact restoration and retained evidence

Restoration commit: `4a3c2a38764c90055f8d5c5c2543697d48930e2d`. The original entry bytes were restored and the two newly created judge files removed. Control bytes remain inspectable in parent commit `04c02aebac351ce47d08eb98f47d0da81521a7b1`; no lane changes or commits were made except writing this report.

Actual `timeout 30 prlimit --as=1073741824 --cpu=20 -- sha256sum <clone>/corpus/knowledge/disk-write-rate-r33.md` outputs:

- Pristine: `8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15`.
- Glossary: `abfc008e29666bc10909a704d76c5b326d6d6290b6b996e4e852d74510de3873` (also the committed judged-sha256).
- Restored: `8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15`.

Actual bounded, clean-environment `git -C <clone> rev-parse HEAD HEAD^{tree} 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8^{tree}` after restoration:

```text
4a3c2a38764c90055f8d5c5c2543697d48930e2d
8da118da561d932335fbf11ad006fc90ca6b3060
8da118da561d932335fbf11ad006fc90ca6b3060
```

The entire committed tree, not just the entry, is therefore restored exactly. The external counter's SHA-256 before and after was `9ec4d87c4eee79b2ef27b60f3f2b7ae73ee8d5bf2d3f2a73b19526b04145eda6` (same bounded sha256sum command with its absolute lane path).

No tools installed or updated. No subagents, background jobs, omp or alternate agent-runtime launches, device changes, or host-service changes were made. All commands returned; only the assigned three-state detector and restoration/hash evidence were exercised.
