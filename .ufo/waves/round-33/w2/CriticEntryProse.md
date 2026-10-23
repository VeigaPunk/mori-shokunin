# CriticEntryProse — round 33, wave 2

Review target: `corpus/knowledge/disk-write-rate-r33.md`, measured revision `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8` (canonical assignment). Paths below are lane-relative unless absolute.
Axes: **depth**, **calibration**, **freshness** (verification provenance), **operability** (resolvable citations). This is a critique, not a C1 judgment or admission decision. Amendment A1 and R-J were read at `.ufo/waves/round-33/contract.md:103-134,44-50`.

## Findings

### 1. Major — three five-second windows, for every whole disk, were not demonstrated

Attack: entry `:36-40`, especially “in three 5-second windows each whole disk's field-10 delta equalled the sum of its partitions' deltas”.

Evidence:
- `.ufo/waves/round-33/w1/ExecHostDiskstats.md:95-110`: the first experiment is `cp; dd ... conv=fsync; cp`, with **no five-second dwell**. The displayed disk/partition comparison names only `nvme1n1` and its two partitions; `dd` reports `0.0362923 s` at `:100`.
- The same report `:111-126` explicitly describes **two** timed windows, `5.04 s` and `5.32 s`, and displays partition sums for the two NVMe disks. It does not display the `sda1`/`sda2` comparisons there.
- Its summary at `:175-177` says three windows, not three five-second windows; its timing limitation repeats the two durations at `:198-199`.

Impacted axes: calibration, depth.
Smallest safe correction: distinguish the two approximately five-second NVMe comparisons from the additional untimed `nvme1n1` write experiment. Do not generalize the displayed comparisons to every whole disk in every window.

### 2. Major — host uptime is silently substituted for counter lifetime

Attack: entry `:49`, “the value is a lifetime mean”; also the “same since-boot total” characterization at `:39-40`.

Evidence:
- `tools/mori-census.sh:1892-1894` computes `sectors * 512 / up_s`; `:1907-1908` obtains `up_s` from whole-second **host uptime**, not device age or time since a counter reset.
- `corpus/evidence/sources-r33/S181.src:33-37` explicitly permits counter resets on device reattachment, reinitialization and overflow, not just boot.
- `.ufo/waves/round-33/w1/ExecHostDiskstats.md:93-94` establishes equality of the two raw counts in one snapshot. Its `:186` explicitly says reset/device-re-add behavior was not tested.
- Constructed counterexample [INFERENCE from the cited reset semantics and arithmetic, not a measured run]: a counter reset one second ago contains 100 sectors while host uptime is 100 seconds. The census quotient is 512 B/s; the counter-lifetime mean is 51,200 B/s.

Impacted axes: depth, calibration.
Smallest safe correction: call the host values “equal cumulative sector counts in this snapshot”; describe the census literally as cumulative bytes divided by integer host uptime, labeled `since-boot`. A counter-lifetime/since-boot interpretation needs the missing counter-epoch condition.

### 3. Major — observed counter equality is promoted to filesystem-attributed triple counting

Attack: entry `:39-43`, especially “would count the root filesystem's writes three times” and “That stacked-device double count is observed”.

Evidence:
- `.ufo/waves/round-33/w1/ExecHostDiskstats.md:116-126` shows equal aggregate deltas for `dm-0`, `nvme0n1p2` and `nvme0n1` in the two displayed timed windows. That is genuine evidence of numerical equality.
- Its own conclusion at `:128-130` says “up to three times”. Its `:193-197` says the prescribed write was on `/fast`/`nvme1n1p2`, **not** `dm-0`, and that the dm evidence is background-traffic coincidence rather than an induced dm experiment.
- Mapping/mount evidence is at the same report `:48-58,65-66`; it identifies the stack, but does not trace individual writes or attribute the measured sector deltas to a particular filesystem workload.
- `.ufo/waves/round-33/w1/SrcDmCore.md:4,35-38` expressly does not establish backing-device re-accounting of the same write.

Impacted axes: calibration, depth.
Smallest safe correction: retain the observed equal counters and topology; mark the filesystem-level explanation and potential triple counting as **[INFERENCE]**, rather than calling that causal identity observed. Keep the source gap/frontier disclosure. This is an evidence-labeling defect, not a reason to discard the measurements.

### 4. Major — the blanket guarantee about verdict cells is too strong

Attack: entry `:15`, “It adds no fact beyond the row's reading.”

Counterexample/evidence:
- Entry `:24` (row 6) interprets the quotient as “the share of the window with I/O in progress”. Its reading states accounting conditions, not an exact correspondence between accounted time and all busy time.
- `corpus/evidence/sources-r33/S181.src:78-80` explicitly says that with concurrent requests some I/O time may not be accounted. This is a locally committed counterexample to an unconditional exact busy-time interpretation.

Impacted axes: depth, calibration.
Smallest safe correction: retain “verdict cells are the lane's reporting rules”, but remove the blanket factual guarantee; correct the technical interpretation before making that guarantee again. Whether any table row meets frozen R-J remains the assigned judge's decision, not this report's.

### 5. Minor — the latency citation names a nonexistent repo-relative path

Attack: entry `:50-51`, `knowledge/surfaces-r8.md:75-89`.

Evidence: the glob tool queried both exact paths. Output:
```
# mori-shokunin/corpus/knowledge/
surfaces-r8.md
Skipped missing paths: /home/vgpnk/Projects/shokunin/mori-shokunin/knowledge/surfaces-r8.md
```
The existing `corpus/knowledge/surfaces-r8.md:75-89` does record the deferral, the 50 ms budget and the tested 0.2 s variant. `.ufo/waves/round-33/w1/ScoutFR6Census.md:41-43` points to this same evidence.

Impacted axis: operability.
Smallest safe correction: add the missing `corpus/` prefix. The cited deferral itself is supported; no new sampling implementation is warranted by this citation defect.

### 6. Minor — the first Limits sentence misstates both provenance and where versions appear

Attack: entry `:55-56`, “Every fact rests on Linux v7.2 sources ... rows 8 and 11 name the versions the sources give.”

Evidence:
- Entry `:3` correctly distinguishes v7.2 tag files, two upstream commit patches, and sysstat. `corpus/evidence/sources-r33/S188.src:1-4` is the 2019 flush-introduction patch; `S189.src:1-5,20` is the 2018 discard patch, refreshed on v4.17. They are not v7.2-tag source files.
- Host and census statements cite own-work reports/code, not Linux v7.2 sources (entry `:36-51`; `.ufo/waves/round-33/w1/ExecHostDiskstats.md:2-5`).
- Entry `:26` (row 8) actually names 4.18 and 5.5. Entry `:29` (row 11) names no kernel version. `S187.src:26-27,36` supplies those versions; `S188.src:37` also supplies 5.5.

Impacted axes: freshness/provenance, calibration.
Smallest safe correction: scope the provenance statement to the relevant source IDs, retain the historical-patch and own-work distinctions, and say **row 8** names the introduction versions. This can be fixed without changing the evidence or claiming additional coverage.

### 7. Minor — “A rate needs two readings” erases the entry's own average/interval distinction

Attack: entry `:59`, “A rate needs two readings and an elapsed time”.

Evidence: entry `:47-50` describes a since-boot average separately from a future two-sample rate; the implementation at `tools/mori-census.sh:1879-1895,1907-1908,1950-1958` derives its reported quotient from a counter read and uptime, not a paired sampled delta. A rate over a known zero baseline does not require two newly obtained readings [INFERENCE from that arithmetic].

Impacted axes: calibration, depth.
Smallest safe correction: say “A measured **interval/current write rate** needs two counter samples and their elapsed time.” Keep the separate, conditional treatment of the boot-baseline quotient from finding 2. Likewise, `:50` is clearest as “does not compute a paired-sample delta”, not an absolute count of file reads: `tools/mori-census.sh:1910,1950` calls the helper per target.

## Checked support and retained boundaries

- **Header `:3-5`:** registry `corpus/SOURCES.md:186-196` and Gate `corpus/lessons/round-33.md:7-25` match the source inventory and access date. Recheck cadence is a declared policy, not evidence that another kernel/sysstat version was tested.
- **Repeated fetches:** matching pairs are recorded in `w1/SrcStatRst.md:9-11`, `SrcIostatsRst.md:13-14`, `SrcGenhd.md:15`, `SrcPartStat.md:10-12`, `SrcBlkCore.md:7-8`, `SrcBlkMq.md:11-13`, `SrcSectorSize.md:13-16`, `SrcFlushCommit.md:9-10`, `SrcDiscardCommit.md:7-9`, and `SrcSysstatIostat.md:13-18`, all under `.ufo/waves/round-33/`.
- For L1's S187, ran `timeout 30s prlimit --as=536870912 sha256sum /fast/scratch/hyaku/mori-r33/L1/src/procfs-diskstats.src /fast/scratch/hyaku/mori-r33/L1/src/procfs-diskstats.2.src /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r33/S187.src`. Output was `0f2ffdc724e0a666c54aa3b1f1e94f93ce6b76745827d301dd164d789bbdd3b7` for all three paths, matching Gate `:22`. This checks saved-byte identity, not a new upstream fetch.
- **Scope/numbering `:7-11`:** `S187.src:10-23` supplies the raw major/minor/name prefix and raw field 12; `S181.src:22-25,71-73` supplies the statistics-only numbering. The stated +3 offset is supported. No device-setting instruction occurs in the complete 59-line entry read.
- **Host `:36-43`:** time/kernel are recorded at `ExecHostDiskstats.md:5,15-18`; “every line had 20 fields” is supported by `:20-31` (`11 20`, then 11 total lines), not a defect. Slave topology and equal raw values are supported at `:55-58,81-94,116-126`; findings 1-3 concern the added generalizations/interpretations.
- **Every cited census code location was inspected:** `tools/mori-census.sh:1879-1895` selects raw field 10 and performs the stated 512 conversion; `:1958` appends device/rate/uptime; `:1974` emits `io_basis=since-boot` and `io_avg_since_boot`. Additional prerequisite locations `:311-314,1872-1877,1907-1908,1922-1927,1946` support the default inputs, integer divisor and df/readlink device resolution. These agree with `ScoutFR6Census.md:10-23`.
- **No round-33 census change:** ran `timeout 30s prlimit --as=536870912 git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --exit-code 7d382043016e8854e3be2ee523a095b409c3d8a1 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 -- tools/mori-census.sh`; output: none, successful tool result. The entry's “No census code changed” is supported at the measured revision.
- **Remaining Limits `:57-59`:** `S181.src:111-121` supports minor partition/disk discrepancies and per-CPU summation. `S183.src:23,34-41` additionally shows the counter-read macro's unlocked sum; the iostats wording itself says no locks while **modifying** counters. No decision-table comparison is conditioned on exact disk/partition sample equality (entry `:19-32`). The entry specifies no sampling interval/threshold; finding 7 concerns only the universal two-read claim.

## Execution boundaries

Read-only evidence review, targeted searches/glob, one evidence checksum command, and read-only Git diff/tree inventory. No counter, judge, runtime, build, test, census invocation, new live host measurement or upstream refetch was run. No tools were installed/updated. Only this assigned report was written; no background process was started.
