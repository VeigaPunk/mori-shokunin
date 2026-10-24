# AttackRow06 — io_ticks busy-time review

Scope: critic findings only for `corpus/knowledge/disk-write-rate-r33.md:24`, at revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. No admission, integration, or C1 judgment.

Axes: source entailment and FR6 depth; calibration of the reported quantity; version precision; A1 lexical independence. The claim targets depth and names calibration among its low axes (`.ufo/waves/round-33/contract.md:12-15`); R-J requires every asserted fact and a verdict requiring no further fact (`contract.md:44-50`), and A1 prohibits six-word Gate copying (`contract.md:119-123`).

## Atomic facts

The row cites S184, S181 and S182. Their Gate rows are `corpus/lessons/round-33.md:19,16,17`, respectively. Quotes below are from their committed copies, including surrounding text rather than treating the short Gate excerpts as exhaustive evidence.

| Fact | Quote or NOT STATED | File:line |
|---|---|---|
| O1: the observation concerns iostats.rst field 10, an I/O-time statistic | "Field 10 -- # of milliseconds spent doing I/Os (unsigned int)" | `corpus/evidence/sources-r33/S181.src:75` |
| O2: the line's exported value is io_ticks | `seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));` follows the in-flight field | `corpus/evidence/sources-r33/S182.src:1394-1395` |
| R1: the increment has magnitude now minus stamp | `__part_stat_add(part, io_ticks, now - stamp);` | `corpus/evidence/sources-r33/S184.src:1068` |
| R2: an ending I/O invokes that update | `update_io_ticks(bdev, now, true);` in `bdev_end_io_acct` | `corpus/evidence/sources-r33/S184.src:1100-1108` |
| R3: a counted in-flight I/O also permits the increment | `(end \|\| bdev_count_inflight(part)))` | `corpus/evidence/sources-r33/S184.src:1067-1068` |
| R2/R3 limit: ending or in-flight is, by itself, sufficient for an increment | **NOT STATED unconditionally.** The surrounding guard also requires `time_after(now, stamp)` and successful `try_cmpxchg(&part->bd_stamp, &stamp, now)`. The first sentence is defensible only as a description of a conditional update, not continuous accrual. | `corpus/evidence/sources-r33/S184.src:1065-1068` |
| R4: this is time, not a request count | "# of milliseconds spent doing I/Os"; the code adds the timestamp difference, not one | `corpus/evidence/sources-r33/S181.src:75`; `S184.src:1068` |
| R5: this is time, not request size | The same milliseconds heading and timestamp arithmetic; sectors are emitted separately from `stat.io_ticks` | `corpus/evidence/sources-r33/S181.src:75`; `S184.src:1068`; `S182.src:1391-1395` |
| R6: iostats.rst relates growth to nonzero field 9 | "This field increases so long as field 9 is nonzero." | `corpus/evidence/sources-r33/S181.src:76` |
| R7: the accumulated timestamps are jiffies | `unsigned long now = READ_ONCE(jiffies);` feeds `update_io_ticks(bdev, now, true);`, whose increment is `now - stamp` | `corpus/evidence/sources-r33/S184.src:1104-1108,1064-1068` |
| R8: the exported counter is converted with jiffies_to_msecs | `seq_put_decimal_ull(seqf, " ", jiffies_to_msecs(stat.io_ticks));` | `corpus/evidence/sources-r33/S182.src:1395` |
| Extra premise needed by verdict: the delta equals all and only busy milliseconds inside the sampling window | **NOT STATED.** The field description expressly warns of unaccounted time; the snapshot path can also use an earlier in-flight count, as shown below. | `corpus/evidence/sources-r33/S181.src:78-80`; `S182.src:1374-1380`; `S184.src:1065-1068,1108-1112` |

## Finding 1 — major: exact busy-share reporting is not established

Attack: `corpus/knowledge/disk-write-rate-r33.md:24`, especially "as the share of the window with I/O in progress".

**Verdict-follows: no, as written.** The time-versus-throughput distinction follows from the reading. The busy-window identity does not: the reading describes updates and units, not exact interval coverage. Calling the quotient a *recorded I/O-time ratio* would avoid that extra premise. R-J does not allow accepting the existing wording only after silently adding "approximately" (`.ufo/waves/round-33/contract.md:47-50`).

Direct narrowing in the same cited copy:

> Since 5.0 this field counts jiffies when at least one request was
> started or completed. If request runs more than 2 jiffies then some
> I/O time might be not accounted in case of concurrent requests.

Evidence: `corpus/evidence/sources-r33/S181.src:78-80`. The Gate quotes only the preceding nonzero-field-9 sentence (`corpus/lessons/round-33.md:16`); its surroundings are materially less absolute.

### Stronger code-level counterexample: cached in-flight sample counts idle time

[INFERENCE] The following interleaving is permitted by the cited code; it is not a measured host occurrence:

1. At jiffy 100 a first sample has io_ticks 0, stamp 100, and one accounted I/O in flight.
2. At jiffy 101 the next `diskstats_show` reads `inflight = 1`, then pauses before `part_stat_lock`. The count is saved before the lock (`S182.src:1374-1376`).
3. At jiffy 102 that I/O completes: `bdev_end_io_acct` advances stamp to 102, adds two ticks, and decrements in-flight to zero (`S184.src:1104-1112`).
4. At jiffy 110 the reader resumes. Its saved nonzero count enters the branch and calls `update_io_ticks(hd, jiffies, true)` (`S182.src:1375-1377`). The `end=true` argument bypasses a fresh in-flight test, so a successful stamp exchange adds eight **idle** ticks (`S184.src:1065-1068`).

Paths in that sequence abbreviate `corpus/evidence/sources-r33/`. The same snapshot-refresh pattern occurs in sysfs (`corpus/evidence/sources-r33/S182.src:1065-1071`), so switching interfaces does not remove this counterexample.

Tested the arithmetic with a source-equivalent guard model, assuming successful stamp exchanges and no wrap. Executed via Python eval as `timeout 10s prlimit --as=134217728 --cpu=5 -- python3 -c trace_script`; the model's operative code and schedule were:

```python
stamp, ticks, inflight = 100, 0, 1
def update(now, end):
    global stamp, ticks
    old = stamp
    if now > old:                 # time_after, no wrap; CAS succeeds
        stamp = now
        if end or inflight:
            ticks += now - old
cached_inflight = inflight        # reader pauses
update(102, True)                 # completion
inflight -= 1
if cached_inflight:
    update(110, True)             # reader resumes
```

Observed model output (exit 0):

```text
completion at j=102: stamp=102 ticks=2 live_inflight=0
reader resumes at j=110: stamp=110 ticks=10 live_inflight=0
window_ticks=10 recorded_io_ticks_delta=10 actual_inflight_ticks=2
reported_fraction=1.0 actual_fraction=0.2
```

This tests the counterexample's arithmetic, not live-kernel reproducibility. It needs neither concurrent outstanding requests nor a historical implementation to make exact busy-share reporting unsafe [INFERENCE from the cited interleaving].

### Version boundary

No separate version error established: row 6 names no introduction/fix version (`corpus/knowledge/disk-write-rate-r33.md:24`). Do not turn the documentation's "Since 5.0" paragraph into proof of a particular v7.2 undercount mechanism: the current helper visibly accumulates elapsed stamp differences (`corpus/evidence/sources-r33/S184.src:1065-1068`). The cached-reader counterexample uses those current bytes. No historical fix boundary was measured.

## A1 lexical check — none found

Compared the current reading against all 11 Gate quotes of its three cited IDs, using the counter's lowercase `[a-z0-9_]+` normalization and six-token windows (`.ufo/waves/round-33/count-c1-a1.py:59,82-87,268-275`). The probe read only the entry, lesson and three copies with `timeout 10s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8:<path>`; its Python process was bounded by `timeout 30s prlimit --as=536870912 --cpu=20`. Observed output, exit 0:

```text
row=6 reading_words=48 sixgrams=43
S184 quotes=3 matching_sixgrams=[] longest_matching_run=2
S181 quotes=4 matching_sixgrams=[] longest_matching_run=2
S182 quotes=4 matching_sixgrams=[] longest_matching_run=1
```

The same probe on the proposed reading below found no matching six-grams: longest matching runs S184=1, S181=1, S182=0 (48 normalized words; exit 0). These are scoped lexical checks, not a counter run or an admission.

## Smallest safe correction

Keep the observation and source cell. Replace only row 6's reading and verdict:

- **Reading:** The update helper conditionally accumulates the gap between its current and saved timestamps after the time-order, stamp-exchange and completion-or-in-flight checks. The printed value is converted from jiffies to milliseconds; the field description also warns of I/O time left uncounted with concurrent requests.
- **Verdict:** Treat this as recorded I/O-time accounting, not throughput or an exact busy-time fraction.

Support: `corpus/evidence/sources-r33/S184.src:1064-1068`, `S182.src:1395`, and `S181.src:75-80`. This is a fixable reporting/entailment defect, not a proposed change to R-J or the claim threshold.

Checks performed: read row 6, all cited Gate quotes and their committed surroundings; inspect both snapshot-refresh paths and bio/request accounting; compare current and proposed reading six-grams; run the bounded arithmetic model. Related source-seat cautions were read at `.ufo/waves/round-33/w1/SrcBlkCore.md:27-41`, `SrcIostatsRst.md:40-48`, and `SrcGenhd.md:45-59`. No source was live-refetched, no host I/O was generated, and no build, C1 counter, judge or UFO runtime was run. No tools were installed or updated; all spawned commands completed without background jobs. Only this report was written.
