# AttackRow10 — discard values separate

## Scope and result

- Target: `corpus/knowledge/disk-write-rate-r33.md:28`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`; working-tree files read as permitted by the assignment.
- **Severity: none — no defect found in the assigned row.** This is a falsification report, not a canonical judge receipt or an admission decision.
- Axes: **depth / FR6** (complete factual support), **calibration / provenance** (R-J and no uncited rescue), **freshness** (historical introduction versus v7.2 behavior). These are the named axes and frontier in `.ufo/waves/round-33/contract.md:12-15`.
- Applied R-J at `.ufo/waves/round-33/contract.md:44-50` and Amendment A1 at `:119-123`. Row 10 cites only S189 and S182 (`corpus/knowledge/disk-write-rate-r33.md:28`).

## Atomic facts

Quotes below come exclusively from the row's own committed S182/S189 copies. Some necessary surroundings extend beyond the short Gate fragments; no third source supplies a missing premise.

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: discard values appear in `/proc/diskstats`. | "append them to the various stat files in /sys as well as /proc/diskstats." | `corpus/evidence/sources-r33/S189.src:8-9`; actual per-line output at `corpus/evidence/sources-r33/S182.src:1353,1401-1409` |
| Reading: discards have four statistics. | "These are tracked with the same four stats as reads and writes:"; the following list names completed I/Os, merges, completed sectors, and milliseconds. | `corpus/evidence/sources-r33/S189.src:9-15`; v7.2 emits those four at `corpus/evidence/sources-r33/S182.src:1401-1405` |
| Reading: those statistics are their own discard group. | "This is done via adding a new STAT_DISCARD define to genhd.h and then using it to index that stat field for discard requests." | `corpus/evidence/sources-r33/S189.src:17-18`; separate enum entry and routing at `:207-227` |
| Reading: they are the same kinds of statistics kept for reads. | "These are tracked with the same four stats as reads and writes:" | `corpus/evidence/sources-r33/S189.src:9-10`; corresponding READ output at `corpus/evidence/sources-r33/S182.src:1384-1388` |
| Reading: they are the same kinds of statistics kept for writes. | "These are tracked with the same four stats as reads and writes:" | `corpus/evidence/sources-r33/S189.src:9-10`; corresponding WRITE output at `corpus/evidence/sources-r33/S182.src:1389-1393` |
| Reading: the discarded-sector count is printed. | `seq_put_decimal_ull(seqf, " ", stat.sectors[STAT_DISCARD]);` | `corpus/evidence/sources-r33/S182.src:1403` |
| Reading: that sector count uses the separate `STAT_DISCARD` group, rather than the write-sector counter. | `stat.sectors[STAT_WRITE]` and `stat.sectors[STAT_DISCARD]` are separate output expressions; the patch routes discard operations to `STAT_DISCARD` before its write/read fallback. | `corpus/evidence/sources-r33/S182.src:1391,1403`; `corpus/evidence/sources-r33/S189.src:207-227` |

No observation or reading fact was left **NOT STATED** by the row's cited copies. `STAT_DISCARD` is the group index of the counter expression, not an assertion that the enum constant itself stores a count (`corpus/evidence/sources-r33/S189.src:17-18,207-227`; `corpus/evidence/sources-r33/S182.src:1403`).

## Does the verdict follow?

**Yes.** The reading establishes a discard-sector counter distinct from the write-sector counter. Keeping discarded sectors separate instead of adding them into the write rate, and displaying them separately if desired, is a reporting choice directly following that separation. No additional factual premise is needed (`corpus/knowledge/disk-write-rate-r33.md:28`; `corpus/evidence/sources-r33/S182.src:1391,1403`; `corpus/evidence/sources-r33/S189.src:223-227`).

**Smallest safe correction: none. No minimal rewrite is required.**

## Counterexamples attempted

All attacks target `corpus/knowledge/disk-write-rate-r33.md:28`. S184/S185/S186 below were used to attack the row, never to rescue its factual support.

| attempted counterexample | evidence and outcome | severity / impacted axes / correction |
|---|---|---|
| Discard's opcode has the write bit: could a completion also increment write sectors? | v7.2 declares `REQ_OP_DISCARD = 3`, and `op_is_write` tests bit 0. However, `op_stat_group` checks discard first and returns `STAT_DISCARD` before the write/read fallback (`corpus/evidence/sources-r33/S186.src:354-355,459-461,484-486,506-510`). Both inspected accounting paths use that group: bio completion at `corpus/evidence/sources-r33/S184.src:1100-1111`, request completion at `corpus/evidence/sources-r33/S185.src:856-863`. The row's own historical patch also shows the overriding discard branch (`corpus/evidence/sources-r33/S189.src:218-227`). This attempted counterexample fails on the actual routing. | none; depth/calibration; none |
| Are all discard effects isolated from shared statistics? | No: the emitter also prints combined READ + WRITE + DISCARD + FLUSH time (`corpus/evidence/sources-r33/S182.src:1396-1400`). The introduction patch likewise adds discard to a generic accumulator (`corpus/evidence/sources-r33/S189.src:236-240`). These defeat a broader claim of complete statistical isolation, but row 10 only separates discarded sectors from a write rate; it makes no such broader claim (`corpus/knowledge/disk-write-rate-r33.md:28`). | none for this row; depth/calibration; none |
| Is a 2018 introduction patch being mistaken for current behavior? | S189 dates itself to 2018 and its ABI hunk says `Kernel 4.18+` (`corpus/evidence/sources-r33/S189.src:3,53-59`). S182 independently shows the four discard outputs in the v7.2 emitter (`corpus/evidence/sources-r33/S182.src:1401-1405`; pinned URL at `corpus/lessons/round-33.md:17`). Row 10 asserts no different introduction version (`corpus/knowledge/disk-write-rate-r33.md:28`). No version-boundary defect found. | none; freshness/provenance; none |

## Six-consecutive-word check

Read all four S182 Gate quotes and both S189 Gate quotes (`corpus/lessons/round-33.md:17,24`) and their committed-copy surroundings: S182 `:1369-1409`, S189 `:7-18`. The exact quoted S182 lines are `:1371-1372,1374,1395,1403`; the quoted S189 lines are `:9-10,14`.

Executed deterministic Python Eval over the exact reading and those six Gate quotes: tokenize with `re.findall(r'[a-z0-9_]+', text.lower())`, build each text's consecutive six-token tuples, and intersect the reading's tuples with each quote's tuples separately. This matches the A1 normalization and comparison at `.ufo/waves/round-33/count-c1-a1.py:86-87,268-275`.

Observed output:

```text
A1 normalization: lowercased runs matching [a-z0-9_]+
reading_words=29
reading_6grams=24
S182 gate_quotes=4 shared_6grams=0 matches=[]
S189 gate_quotes=2 shared_6grams=0 matches=[]
counter_invoked=False; judge_invoked=False
```

## Checks and limits

- Read the target row, R-J/A1, every cited Gate quote and its source surroundings; inspected both current output functions, the introduction patch, current opcode classification, and the two completion-accounting functions named above.
- Used targeted searches for `STAT_WRITE`, `STAT_DISCARD`, `op_stat_group`, and `op_is_write` in the inspected accounting sources; these are source inspections, not a claim of exhaustive driver coverage.
- Ran only the described six-word comparison. No C1 counter, canonical judge, build, test suite, live device operation, network fetch, shell/background job, or Git/jj mutation was run.
- No tools installed or updated. Only this report was written.
