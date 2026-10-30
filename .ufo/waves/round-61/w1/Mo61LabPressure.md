# Mo61LabPressure — C2 live-relevance probe

## Result

The falsifiable hypothesis is **consistent with these two host samples**, not established as a general equivalence: this host reports kernel `7.2.11-arch1-1`; for each observable active PSI line with a nonzero cumulative total, `total` advanced over the ~10 s interval, and each such line's `avg10` changed. No sampled line showed an `avg10` change while its `total` stayed fixed. The system CPU `full` line remained all-zero in both samples. This two-point observation cannot test the proposed condition (average changes while total is unchanged) because no changed average with unchanged total occurred.

## Exact evidence

Command executed from the fleet-root cwd (read-only; each `cat` reads `/proc/pressure/{cpu,memory,io,irq}`):

```sh
D=/fast/scratch/hyaku/mori-r61/Mo61LabPressure; mkdir -p "$D" && export TMPDIR="$D" && printf 'kernel=' && uname -r && printf 'sample1_utc=' && date -u +%Y-%m-%dT%H:%M:%SZ && for f in cpu memory io irq; do printf '%s\\n' "[$f]"; cat "/proc/pressure/$f"; done && sleep 10 && printf 'sample2_utc=' && date -u +%Y-%m-%dT%H:%M:%SZ && for f in cpu memory io irq; do printf '%s\\n' "[$f]"; cat "/proc/pressure/$f"; done
```

Captured output:

```text
kernel=7.2.11-arch1-1
sample1_utc=2026-10-30T05:35:24Z
[cpu]
some avg10=19.74 avg60=19.18 avg300=14.21 total=26948058846
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
[memory]
some avg10=4.74 avg60=3.80 avg300=2.94 total=1019171611
full avg10=4.55 avg60=3.62 avg300=2.82 total=950518771
[io]
some avg10=2.46 avg60=1.91 avg300=3.18 total=2298831527
full avg10=0.16 avg60=0.16 avg300=1.23 total=1044665862
[irq]
full avg10=2.09 avg60=1.79 avg300=1.51 total=1958272968
sample2_utc=2026-10-30T05:35:34Z
[cpu]
some avg10=19.00 avg60=19.11 avg300=14.37 total=26949966348
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
[memory]
some avg10=3.35 avg60=3.56 avg300=2.91 total=1019448069
full avg10=3.13 avg60=3.38 avg300=2.79 total=950789397
[io]
some avg10=1.90 avg60=1.81 avg300=3.11 total=2299021222
full avg10=0.06 avg60=0.14 avg300=1.19 total=1044705602
[irq]
full avg10=2.08 avg60=1.83 avg300=1.53 total=1958531533
```

Observed deltas (second minus first, totals in the kernel-emitted units): cpu some `+1,907,502` (`avg10` -0.74); memory some `+276,458` (-1.39), memory full `+270,626` (-1.42); io some `+189,695` (-0.56), io full `+39,740` (-0.10); irq full `+258,565` (-0.01). CPU full total and avg10 both remained zero. These are direct differences of the two captured outputs, not a rate or extrapolation.

## Interpretation and retained evidence

- The two observations are compatible with the R24 note's scoped v7.2 claims: reads collect totals and averages are refreshed on a read only when the next ~2 s update is due (`corpus/knowledge/system-pressure-r24.md:92-102`, especially corrected K5 at lines 99-102); a short event is counted in total and decayed into averages (`:19`, `:176`, `:190-193`).
- The stated monotonic accumulation claim is at `corpus/knowledge/system-pressure-r24.md:152-156`; the host samples do not independently prove kernel implementation semantics. The specified K4/K5 limits are explicitly at `:19-21`.
- No claim is made about what happened between samples, causality, host health, or behavior when a total is static. Two reads only; no interpolation.

No tools installed or updated. No production/counter/source files or VCS state changed. Disk guard status invocation returned scratch free space `369.4G` (status command itself timed out after printing the status table).