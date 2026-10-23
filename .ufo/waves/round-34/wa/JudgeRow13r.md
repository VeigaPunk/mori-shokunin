measured 2026-10-23T05:39:13Z

# JudgeRow13r — row 13r, disk-write-rate-r33.md (§Round-34 revision) at 8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3

judged-sha256: ca489eb41140024e95641a53c7df0ae15f755a4e0a507b9f353bfec1b415f9f6
(sha256 of `git -C <lane> show 8d56809…:corpus/knowledge/disk-write-rate-r33.md`; recomputed twice, identical. HEAD has since moved to fd25213… "round-34: wave A spec/dispatch… before dispatch"; row judged at the assigned revision 8d56809…, which is an ancestor of HEAD.)

## Rule (quoted word for word from the round-33 contract, `.ufo/waves/round-33/contract.md:47-50`)

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its
> observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row
> any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or
> through a source the row does not cite.

## Row 13r (line 79 of the file at the revision; under `## Round-34 revision (append-only; routed by … §8 items 2 and 3)` at line 65)

- Observation: `Lane fact: `tools/mori-census.sh:1869-1871,1879-1894,1907-1908` labels its value an average since boot and computes field 10 (sectors written) × 512 / uptime seconds`
- Reading: `Sectors written is a cumulative counter (S181.src:33-34,64-65); counters other than field 9 reset at boot, on device reattachment or reinitialisation, or when the underlying counter overflows, and readers should detect and handle resets when comparing snapshots (S181.src:34-37)`
- Verdict: `Call the census value a since-boot average only if none of those resets happened after boot, and never report it as the current write rate`
- Sources cited: `S181; lane fact `tools/mori-census.sh``

Sources opened at the revision: `corpus/evidence/sources-r33/S181.src` (committed copy) and `tools/mori-census.sh` (lane file named by the row).

## Observation facts — located quotes from `tools/mori-census.sh` at 8d56809…

- Fact O1 "labels its value an average since boot":
  - `census.sh:1869`: "AVERAGE SINCE BOOT — reported with that name and never as an instantaneous" (contiguous, 13 words).
  - `census.sh:1870-1871`: "rate. No sampling interval is added to census runtime (bounded deferral / recorded in the header block)."
- Fact O2 "computes field 10 (sectors written) × 512 / uptime seconds":
  - `census.sh:1887-1889`: "field 10 of a diskstats line = sectors written (field 8 is writes completed); / 512 bytes per sector is the counter's unit, not an assumption about the / device's physical sector size." (contiguous, 25 words)
  - `census.sh:1892`: "sectors=$(printf '%s\n' "$line" | awk '{print $10}' || true)" (extracts field 10; contiguous, ≥6 words)
  - `census.sh:1894`: "printf '%sBps' "$((sectors * 512 / up_s))"" (multiplies field 10 by 512 and divides by uptime seconds `up_s`; contiguous)
  - `census.sh:1907-1908`: "up_raw=$(read_file "$UPTIME_FILE"); up_raw=${up_raw%% *}; up_raw=${up_raw%%.*} / if is_int "$up_raw" && [ "$up_raw" -gt 0 ]; then up_s=$up_raw; fi" (uptime seconds source; contiguous, ≥6 words)

No observation fact is `missing`; every fact is stated by the cited spans.

## Reading facts — located quotes from committed `corpus/evidence/sources-r33/S181.src`

- Fact R1 "Sectors written is a cumulative counter":
  - `S181.src:33-34`: "All fields are cumulative, monotonic counters, except for field 9, which / resets to zero as I/Os complete." (contiguous, ≥6 words)
  - `S181.src:64-65`: "Field  7 -- # of sectors written (unsigned long) / This is the total number of sectors written successfully." (identifies field 7 as sectors written; contiguous, ≥6 words)
- Fact R2 "counters other than field 9 reset at boot, on device reattachment or reinitialisation, or when the underlying counter overflows, and readers should detect and handle resets when comparing snapshots":
  - `S181.src:34-37`: "The remaining fields reset at boot, on / device reattachment or reinitialization, or when the underlying counter / overflows. Applications reading these counters should detect and handle / resets when comparing stat snapshots." (contiguous, 22 words; `reinitialization` vs the row's `reinitialisation` is a spelling variant, and "Applications reading these counters" vs "readers" is a synonym — same facts stated)

No reading fact is `missing`; every fact is stated by the cited spans.

## Verdict follows from the reading without any further fact

- The reading states sectors written is a cumulative counter and that counters other than field 9 reset at boot/reattachment/reinitialisation/overflow, with readers to detect/handle resets when comparing snapshots. The verdict's guard — call the census value a since-boot average *only if none of those resets happened after boot* — is exactly the consequence of that reset semantics over a cumulative counter, and its second clause (never report it as the current write rate) follows from the observation fact that the value is an average since boot (windowed over uptime), not an instantaneous rate. Both clauses follow from the cited reading plus the cited lane observation; no further source or fact is required.

## Routed defect check

- `corpus/lessons/round-33-verifier-spotcheck.md` §3.1 (row 13 unsupported: "the observation is a fact about `tools/mori-census.sh`; S181 has no census, uptime or average text") and §8 item 2 (rows 3/6/7/13: "Cite S182:1370,1472, S181:78-80, S181:22, or narrow the cells") — the new 13r row narrows the observation to the lane file it names (`tools/mori-census.sh`) with the exact line spans, and keeps S181 spans that do state what the reading asserts. The routed defect is repaired for row 13r.

- Tooling: no tool installed or updated (no install needed; git used read-only; commands capped with the provided policy).

## Verification gaps

- None blocking. I did not re-run the counter `count-c1-a1.py` (judge seat; not assigned). All quotes read from committed copies at 8d56809…; the row was read as a single line (line 79) from the git-show extract.

VERDICT: row 13r: supported
