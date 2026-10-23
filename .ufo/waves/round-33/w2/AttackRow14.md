# AttackRow14 — scoped critic report

Target: `corpus/knowledge/disk-write-rate-r33.md:32`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` (revision supplied by the assignment). This is a support review, not a canonical judgment or claim measurement.

Axes: depth (accurate branch-level semantics), calibration (no universal claim from a conditional branch), and freshness/version scope (the named tag must not conceal differences within that version). C1 explicitly works depth: `.ufo/waves/round-33/contract.md:12-15,24`.

## Atomic facts

Paths beginning `S181.src` or `S190.src` below mean `corpus/evidence/sources-r33/`.

| fact | quote or NOT STATED | file:line |
|---|---|---|
| Observation: this is iostat. | "iostat: report CPU and I/O statistics" | `S190.src:2` |
| Observation: the version is sysstat 12.8.0. | **NOT STATED in either committed source body.** The Gate URL contains `/sysstat/sysstat/v12.8.0/iostat.c`, which supplies tag provenance, not a quote in the committed copy. This is not evidence that the tag is wrong. | `corpus/lessons/round-33.md:25`; `S190.src:37,50-52` only include/reference `VERSION` |
| Observation: a device's write-sector-rate display can be zero. | `xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);` and `cprintf_f(..., xios->wsectors);` support that possibility in the extended, separate-write display. This is numerical zero; the displayed precision is a separate matter. | `S190.src:1516-1517,1243-1253` |
| Reading: ioi is named the current sample. | "@ioi Current sample statistics." | `S190.src:1151` (also `1456`) |
| Reading: ioj is named the previous sample. | "@ioj Previous sample statistics." The label is present, but the actual argument need not remain the previous read sample: `ioj = &iozero;`. | `S190.src:1152,1457,1887-1893` |
| Reading: comparing the function's supplied write-sector values and finding current smaller selects numeric zero. | `xios.wsectors = ioi->wr_sectors < ioj->wr_sectors ? 0.0 : S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);` | `S190.src:1516-1517` |
| Reading: whenever the current actual sample is below the actual previous sample, iostat prints zero. | **NOT STATED as an unconditional iostat behavior.** The quote belongs to `write_ext_stat`; its caller first may replace `ioj` with zeros, and basic output uses another path. | `S190.src:1444-1464,1804-1806,1887-1893,1941-1945,1613-1615` |
| Reading: the decreasing-count branch selects zero instead of deriving that value from the two supplied counters. | The local ternary bypasses `S_VALUE` when its comparison is true. **NOT STATED for every iostat output or for the two actual snapshots**, because the caller can substitute a baseline. | `S190.src:1516-1517,1887-1893,1941-1945` |

The two naming quotes and the ternary are exactly the S190 Gate material (`corpus/lessons/round-33.md:25`). The S181 Gate includes reset documentation: "The remaining fields reset at boot, on device reattachment or reinitialization, or when the underlying counter overflows" (`corpus/lessons/round-33.md:16`; `S181.src:34-36`). That establishes reset possibilities; it does not establish what every iostat output path does afterward.

## Finding 1 — major: a reset can bypass the quoted zero branch

Attacks the unconditional reading and reset explanation in `corpus/knowledge/disk-write-rate-r33.md:32`.

The surrounding source explicitly warns that preprocessing has already occurred: "We've already tried to determine if a device had been removed then added again (see write_stats() function)" (`S190.src:1508-1512`). The caller initially selects the actual snapshots (`S190.src:1870-1871`), but its reinsertion heuristic replaces the previous argument with an all-zero structure (`S190.src:1804-1806,1887-1893`). Both display paths receive that possibly replaced pointer (`S190.src:1941-1945`).

Strongest counterexample, **[INFERENCE: static walkthrough, not an executed iostat run]**:

- Previous snapshot: `wr_ios=100`, `wr_sectors=800`; current snapshot: `wr_ios=1`, `wr_sectors=8`. Read/discard/flush operation counts and read/discard sector counts are zero in both snapshots. Assume an existing displayed device and extended, non-short output.
- Current nonzero write activity avoids the unfiltered-device skip (`S190.src:1873-1875`). The operation totals fall from 100 to 1, the write-sector comparison is true, and the other sector tests succeed because their previous values are zero (`S190.src:1888-1892`). Therefore `ioj = &iozero` (`S190.src:1893`).
- The extended calculation now compares **8 against 0**, not 8 against 800, and takes `S_VALUE(0,8,itv)`, not `0.0` (`S190.src:1516-1517`). With `itv=100`, this is 8 sectors/s; with the kilobyte factor 2 it is 4 kB/s (`S190.src:1066-1068,1248-1253`).
- The arithmetic definition is `#define S_VALUE(m,n,p) (((double) ((n) - (m))) / (p) * 100)` in [sysstat v12.8.0 common.h](https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.h), opened through the `common.h` include in [iostat.h](https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.h). These extra pages support this counterexample, not the existing row's R-J support.

Thus a raw counter set back between samples does **not necessarily yield zero even in extended output**. This is an internal v12.8.0 control-flow boundary, not an earlier/later-version objection (`S190.src:1508-1517,1887-1893`).

A second narrowing exists in the same committed file: the caller selects `write_basic_stat` when extended output is off (`S190.src:1941-1945`); basic plain output calculates `wsectors = S_VALUE(ioj->wr_sectors, ioi->wr_sectors, itv);` without the quoted zero ternary (`S190.src:1613-1615`), and basic JSON does the same (`S190.src:1704-1707`). Adding only “extended” would therefore fix one omission but leave the reset-baseline counterexample intact. The `-x` switch enables extended output (`S190.src:2301-2303`).

Impacted axes: depth and calibration. This is a fixable scope/control-flow defect, not a justified tradeoff for the canonical judge to waive. The S190 teaches cell repeats the broad claim and should be narrowed consistently if the integrator repairs it (`corpus/SOURCES.md:196`).

## Verdict-follows check

**Not as written.** The caution against treating a fallback zero as proof of an unchanged counter follows from the conditional assignment (`S190.src:1516-1517`). But “a counter set back between samples also yields zero” is not an unconditional consequence: the caller may substitute zeros first (`S190.src:1887-1893`). S181 states reset causes, not the missing iostat behavior (`S181.src:33-37`). Accepting the present row requires the forbidden caveats “extended output” and “the supplied comparison argument still has the larger value”; R-J disallows caveat-dependent support (`.ufo/waves/round-33/contract.md:44-50`).

## Finding 2 — minor: literal version support is metadata-only

Attack: the observation's `(sysstat 12.8.0)` at `corpus/knowledge/disk-write-rate-r33.md:32`. The source includes `version.h` and a symbolic `VERSION`, not the literal release number (`S190.src:37,50-52`). A grep-tool search of both cited copies for `12\.8\.0|sysstat|VERSION` returned only `S190.src:3,51,83`, none containing `12.8.0`. The version is grounded by the Gate URL (`corpus/lessons/round-33.md:25`), but under literal R-J it is not stated by a quote inside a cited committed copy. Impacted axis: calibration/provenance precision. Smallest correction: keep version scope in the existing entry metadata and omit this parenthesis from the row; no claim that a different version was fetched.

## Smallest safe row rewrite

Keep the directly evidenced fallback; remove universal output/reset implications and the now-unused S181 citation:

| # | observation | reading | verdict | sources |
|---|---|---|---|---|
| 14 | iostat's `write_ext_stat` write-sector fallback | For this extended-output function, the write-sector value supplied as `ioi` being smaller than the value supplied as `ioj` makes `xios.wsectors` zero | Do not interpret this fallback zero as an unchanged write-sector counter | S190 |

Support: the function's extended-output purpose (`S190.src:1444-1464`) and its exact assignment (`S190.src:1516-1517`). “Supplied” deliberately does not claim that `ioj` still points to the actual previous snapshot. The proposed verdict follows from the unequal inputs alone; it adds no reset claim. This is a proposed correction only; no lane content was edited.

## A1 six-word check — none found

Checked the existing reading against **all seven** cited Gate quotes, not only the three S190 quotes (`corpus/lessons/round-33.md:16,25`). A bounded text-only Python evaluation used `re.findall(r'[a-z0-9_]+', text.lower())` and intersections of consecutive six-token tuples, matching the counter's normalization/comparison (`.ufo/waves/round-33/count-c1-a1.py:86-87,268-275`). Output:

```text
S181 Q1: shared_six_word_runs=[]
S181 Q2: shared_six_word_runs=[]
S181 Q3: shared_six_word_runs=[]
S181 Q4: shared_six_word_runs=[]
S190 Q1: shared_six_word_runs=[]
S190 Q2: shared_six_word_runs=[]
S190 Q3: shared_six_word_runs=[]
reading_tokens=34
```

## Checks and containment

Read the assigned row, Amendment A1 and R-J, both complete Gate rows, and every quoted location with surrounding committed-source text: S181 `22,28-38,64-76`; S190 `1139-1263,1444-1523`. Traced both output modes, reset preprocessing, field formatting and option selection through S190 `1056-1136,1586-1755,1760-1950,2289-2305`. Opened the two upstream headers linked above only to substantiate the static arithmetic counterexample. Performed the version search and six-word computation described above. No claim counter, judge, build, test suite, iostat process, host/device change, Git write, background job, or tool installation/update was performed. Only this report was written.
