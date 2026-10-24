# LiveBracketCheck: C2 live bracket check (amendment A2)

Seat: `MoriR24.LiveBracketCheck` (leaf, no subagents). Round 24, wave 2, falsify.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Host: `plazir27`, kernel `7.2.11-arch1-1`.
Lane HEAD during this check: `89849a7` (08:59Z to 09:02Z), then `6a344d2` (09:03:35Z) and `a536b18` (seen 09:08:52Z).
Scratch: `/fast/scratch/hyaku/mori-r24-a2/w2/LiveBracketCheck/` (raw reads, tool outputs, copies).
Writes: this report and the scratch directory only. Host and lane were read only.

## 1. Result

- **Required runs pass on both tool versions the lane held during this check.** Runs 1 to 3 and the `--interval 1` run used blob `f2e39df3` (HEAD `89849a7`). The tool file was last written at 09:03:07Z (commit `6a344d2` at 09:03:35Z), so I repeated the three bracket runs and the interval run on blob `01a6448c` (HEAD `a536b18`). In every run, all seven reported totals (cpu some, cpu full, memory some, memory full, io some, io full, irq full) lie between the raw totals read just before and just after the tool. All four resources are `ok`. `irq.some` is `null`. System `cpu.full` total is `0` in the tool output and in both raw reads. Verdict `PRESSURE_OK`, exit 0, stderr empty.
- **Extra checks pass.** Every average triple (avg10, avg60, avg300 of each of the seven rows) equals one of the two raw readings: 63 of 63 triples over nine runs. The interval deltas and ratios agree with the raw bracket.
- **The committed five-run record also passes.** `.ufo/waves/round-24/evidence/bracket-check-run.json` (added by `6a344d2`) records five runs at 09:03:27Z, all passing. My cross-check of its recorded totals agrees.
- **The new UTF-8 clause behaves as its commit says.** Non-UTF-8 content makes the resource `malformed`, with verdict `PRESSURE_PARTIAL` and exit 0 (section 9).
- **No high-severity defect.** The same results hold on the lane-tip blob (`a730ecf`, blob `852d1ea7`, supplementary run 4).
- **The check proves less than its use suggests.** It shows that the values lie inside the read window. It does not show which files were read. A probe that reads the cgroup-root copies of the same counters passes all seven rows (F3).
- **Evidence gaps.** The selftest evidence file predates both later blobs (F1). The committed record keeps totals only, and the knowledge recheck line still omits the bracket (F2).

## 2. Identity and environment

| item | value | how measured |
|---|---|---|
| host, user | `plazir27`, `vgpnk` | `hostname`, `id -un` |
| kernel | `7.2.11-arch1-1` | `uname -r` |
| interpreter | Python 3.14.8, run as `python3 -I` | `python3 --version` |
| lane HEAD, 08:59:19Z to 09:02:27Z | `89849a7` | `git rev-parse HEAD` |
| lane HEAD, 09:08:52Z | `a536b18` (after `6a344d2`, committed 09:03:35Z) | `git rev-parse HEAD`, `git log` |
| measured tip | `a730ecf`, an ancestor of both | `git merge-base --is-ancestor` |
| tool blob at the measured tip | sha256 `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5`, 569 lines | `git cat-file -p a730ecf:tools/mori-pressure.py` |
| tool blob at `89849a7` | sha256 `f2e39df3791c491f59b581b3110d026335fe6153f495c86bebeaacef3547e747`, 614 lines. Hash checked before and after runs 1 to 3 and the interval run, and again after the stale-root control (about 09:02Z). The file mtime was 08:58:40Z at 08:59Z and changed at 09:03:07Z | `sha256sum`; `stat`; `git cat-file -p 89849a7:tools/mori-pressure.py` |
| tool file at `a536b18` | sha256 `01a6448c69e44ed69b616ccbf03b109cfc479bf14d094b0a2794258241e2da26`, 617 lines, file mtime 09:03:07.686Z. Hash checked before and after runs 5 to 7 and the interval run. The cgroup-root and non-UTF-8 probes ran after that mtime and before any later write | `sha256sum`; `stat`; `git cat-file -p HEAD:tools/mori-pressure.py` |
| change from the tip to `89849a7` | six hunks in the `a730ecf` numbering, at lines 383, 493, 519, 527, 537 and 548: argument parser, selftest and `main`. None is on the live read path | `git diff a730ecf 89849a7 -- tools/mori-pressure.py` |
| change from `89849a7` to `a536b18` | one hunk, `@@ -159,6 +159,9 @@`: three added lines (162 to 164) in `_read_resource`. `except UnicodeDecodeError` returns `malformed`. This is on the live read path | `git diff 89849a7 a536b18 -- tools/mori-pressure.py` |

## 3. Commands run

1. **Bracket run, three times on blob `f2e39df3`, and three times on blob `01a6448c`.** Each run was one shell command: UTC stamp and `sha256sum` of the tool; UTC stamp; `cat /proc/pressure/{cpu,memory,io,irq}` into scratch files `raw1_*.txt`; UTC stamp; `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pressure.py > tool.json 2> tool.err`, then the exit code; UTC stamp; `cat` of the same four files into `raw2_*.txt`; UTC stamp; `sha256sum` of the tool. Runs on `f2e39df3`: `run1` at 08:59:57Z, `run2` at 09:00:09Z, `run3` at 09:00:15Z. Runs on `01a6448c`: `run5_current` at 09:09:43Z, `run6_current` at 09:09:49Z, `run7_current` at 09:09:53Z.
2. **`--interval 1`, once per blob (required).** The same bracket around `python3 -I <tool> --interval 1`: `interval1` at 09:00:25Z (blob `f2e39df3`) and `interval2_current` at 09:09:58Z (blob `01a6448c`).
3. **Extra: lane-tip blob.** `git show a730ecf:tools/mori-pressure.py` into scratch, then the same bracket (`run4_a730ecf`, 09:00:57Z, blob `852d1ea7`).
4. **Extra: stale-root control.** `python3 -I <tool> --root <scratch directory holding copies of the run1 raw1 bytes>` (09:01:52Z, blob `f2e39df3`).
5. **Extra: cgroup-root probe.** Copies of `/sys/fs/cgroup/{cpu,memory,io,irq}.pressure`, taken between two `/proc/pressure` raw reads (copies at 09:04:04.046464Z to 09:04:04.047432Z), then `python3 -I <tool> --root <copy directory>`. Blob `01a6448c`, because the file's last write was 09:03:07Z.
6. **Extra: non-UTF-8 probe.** A scratch root whose `cpu` file is one valid line followed by bytes `\xff\xfe`, with copies of the run7 `memory`, `io` and `irq` files, then `python3 -I <tool> --root <that directory>`. Blob `01a6448c`.
7. **Checker.** A Python cell parses the raw files with the kernel line grammar, compares each read with the tool JSON, applies the A2 conditions and the extra checks, runs mutation controls, and cross-checks the committed record `evidence/bracket-check-run.json`.
8. **Lane and host reads, all read only.** `git --no-optional-locks` with `rev-parse`, `log`, `status`, `cat-file`, `diff`, `show` and `merge-base`; `stat`; `ls` of `.ufo/waves/round-24/evidence/` and `w2/`; literal grep of the tool for call sites; `cat /proc/cmdline`; `read` of the committed checker and record. The `lsp` device is not mounted for this seat (`xd://lsp` returned "Mounted devices: ast_edit, debug"), so call-site statements rest on literal text.

Tool invocations: twelve in total. Eight used the default root (`run1`, `run2`, `run3`, `interval1` on `f2e39df3`; `run5_current`, `run6_current`, `run7_current`, `interval2_current` on `01a6448c`). One ran the tip-blob copy (`run4_a730ecf`, blob `852d1ea7`). Three used `--root` into scratch: the stale-root control on `f2e39df3`, and the cgroup-root and non-UTF-8 probes on `01a6448c`.

## 4. UTC times and raw bytes

| run | blob and role | sha256 before | raw1 read | tool run (exit) | raw2 read | sha256 after |
|---|---|---|---|---|---|---|
| run1 | `f2e39df3`, bracket | 08:59:57.289053 | 08:59:57.289588 to 08:59:57.290455 | 08:59:57.290706 to 08:59:57.324140 (0) | 08:59:57.324389 to 08:59:57.325440 | 08:59:57.325613 |
| run2 | `f2e39df3`, bracket | 09:00:09.029957 | 09:00:09.030602 to 09:00:09.031650 | 09:00:09.031818 to 09:00:09.062803 (0) | 09:00:09.063023 to 09:00:09.064198 | 09:00:09.064379 |
| run3 | `f2e39df3`, bracket | 09:00:15.046017 | 09:00:15.046559 to 09:00:15.047343 | 09:00:15.047469 to 09:00:15.075070 (0) | 09:00:15.075201 to 09:00:15.076512 | 09:00:15.076732 |
| interval1 | `f2e39df3`, `--interval 1` | 09:00:25.036810 | 09:00:25.037411 to 09:00:25.038306 | 09:00:25.038451 to 09:00:26.068090 (0; `elapsed_us` 1000245; wall 1.04 s) | 09:00:26.068345 to 09:00:26.069772 | 09:00:26.069928 |
| run4_a730ecf | `852d1ea7` (tip copy), bracket | 09:00:57.037316 | 09:00:57.037736 to 09:00:57.038462 | 09:00:57.038567 to 09:00:57.066561 (0) | 09:00:57.066779 to 09:00:57.067626 | not taken (scratch copy) |
| stale root | `f2e39df3`, `--root` copy of run1 raw1 | not taken | not taken | start 09:01:52.182066 (0) | not taken | not taken |
| run5_current | `01a6448c`, bracket | 09:09:43.692502 | 09:09:43.693165 to 09:09:43.694484 | 09:09:43.694702 to 09:09:43.722391 (0) | 09:09:43.722859 to 09:09:43.723876 | 09:09:43.724068 |
| run6_current | `01a6448c`, bracket | 09:09:49.757572 | 09:09:49.758181 to 09:09:49.759161 | 09:09:49.759312 to 09:09:49.790063 (0) | 09:09:49.790340 to 09:09:49.791254 | 09:09:49.791381 |
| run7_current | `01a6448c`, bracket | 09:09:53.948204 | 09:09:53.948622 to 09:09:53.949475 | 09:09:53.949602 to 09:09:53.977976 (0) | 09:09:53.978192 to 09:09:53.979268 | 09:09:53.979383 |
| interval2_current | `01a6448c`, `--interval 1` | 09:09:58.475893 | 09:09:58.476428 to 09:09:58.477384 | 09:09:58.477717 to 09:09:59.506087 (0; `elapsed_us` 1000287; wall 1.04 s) | 09:09:59.506276 to 09:09:59.508546 | 09:09:59.508722 |
| cgroup root | `01a6448c`, `--root` copy of cgroup-root files | not taken | 09:04:04.045251 to 09:04:04.046270 | 09:04:04.047599 to 09:04:04.074343 (0) | 09:04:04.074543 to 09:04:04.075625 | not taken |
| non-UTF-8 probe | `01a6448c`, `--root` | not stamped | not stamped | not stamped (0) | not stamped | not stamped |
| committed record | `evidence/bracket-check-run.json`, five runs (commit `6a344d2`) | — | — | `at` stamps 09:03:27.397896Z to 09:03:27.505765Z | — | — |

**Raw bytes.** Each read set (one `raw1` or one `raw2`) is 373 bytes: `cpu` 101, `memory` 108, `io` 110, `irq` 54 (`wc -c`). The sizes were the same in every bracket run and in both reads. Full sha256 values are in Appendix A.

Raw text, run1 `raw1` (the four files, in order):

```
cpu:
some avg10=0.14 avg60=0.03 avg300=0.00 total=11402661
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
memory:
some avg10=0.38 avg60=0.21 avg300=0.19 total=20023132
full avg10=0.38 avg60=0.21 avg300=0.19 total=19783373
io:
some avg10=3.95 avg60=2.71 avg300=2.62 total=128316803
full avg10=3.75 avg60=2.63 avg300=2.52 total=122999879
irq:
full avg10=0.00 avg60=0.00 avg300=0.00 total=22857005
```

Run1 `raw2`, the same layout, with these totals: cpu some 11402701, cpu full 0, memory some 20023132, memory full 19783373, io some 128319552, io full 123002523, irq full 22857256.

## 5. Totals: raw1, tool, raw2

Each cell reads `raw1 / tool / raw2`. For the interval runs, the tool value is the second read.

### 5a. Blob `f2e39df3` (runs 1 to 3, interval1) and blob `852d1ea7` (run 4)

| row | run1 | run2 | run3 | run4_a730ecf | interval1 |
|---|---|---|---|---|---|
| cpu some | 11402661 / 11402694 / 11402701 | 11439488 / 11439603 / 11439605 | 11462137 / 11462158 / 11462164 | 11542258 / 11542280 / 11542283 | 11485124 / 11487023 / 11487028 |
| cpu full | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| memory some | 20023132 / 20023132 / 20023132 | 20198456 / 20200978 / 20201575 | 20306997 / 20307055 / 20307065 | 20673040 / 20673040 / 20673040 | 20456305 / 20493529 / 20493826 |
| memory full | 19783373 / 19783373 / 19783373 | 19956356 / 19958878 / 19959475 | 20061433 / 20061492 / 20061494 | 20421149 / 20421149 / 20421149 | 20209373 / 20245981 / 20246278 |
| io some | 128316803 / 128319064 / 128319552 | 128836255 / 128838956 / 128839390 | 129153418 / 129154552 / 129155311 | 131598592 / 131602369 / 131603140 | 129800556 / 129894692 / 129895727 |
| io full | 122999879 / 123002045 / 123002523 | 123500616 / 123503234 / 123503667 | 123806220 / 123807316 / 123808040 | 126201345 / 126205099 / 126205869 | 124438987 / 124531266 / 124532284 |
| irq some | no line / null / no line | no line / null / no line | no line / null / no line | no line / null / no line | no line / null / no line |
| irq full | 22857005 / 22857216 / 22857256 | 22933069 / 22933322 / 22933498 | 22978067 / 22978182 / 22978231 | 23251046 / 23251313 / 23251368 | 23058692 / 23070718 / 23070826 |

### 5b. Blob `01a6448c` (runs 5 to 7, interval2)

| row | run5_current | run6_current | run7_current | interval2_current |
|---|---|---|---|---|
| cpu some | 12540378 / 12540849 / 12540852 | 12551562 / 12551590 / 12551593 | 12558761 / 12558789 / 12558794 | 12574000 / 12585841 / 12585847 |
| cpu full | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| memory some | 24706680 / 24706680 / 24706680 | 24805751 / 24805751 / 24805751 | 24863083 / 24863083 / 24863083 | 25118152 / 25218304 / 25218304 |
| memory full | 24397799 / 24397799 / 24397799 | 24495244 / 24495244 / 24495244 | 24551480 / 24551480 / 24551480 | 24803556 / 24901337 / 24901337 |
| io some | 153786733 / 153788221 / 153788870 | 154166466 / 154169306 / 154170249 | 154401498 / 154405124 / 154405936 | 154655064 / 154711511 / 154712840 |
| io full | 148074740 / 148076149 / 148076794 | 148451233 / 148454059 / 148455002 | 148683137 / 148686732 / 148687544 | 148933885 / 148988388 / 148989710 |
| irq some | no line / null / no line | no line / null / no line | no line / null / no line | no line / null / no line |
| irq full | 26217465 / 26217644 / 26217688 | 26264259 / 26264527 / 26264586 | 26295023 / 26295232 / 26295282 | 26341215 / 26365231 / 26365300 |

## 6. A2 conditions and extra checks

| check | blob `f2e39df3` (runs 1 to 3, interval1) and `852d1ea7` (run 4) | blob `01a6448c` (runs 5 to 7, interval2) |
|---|---|---|
| A2: every reported total lies between raw1 and raw2 (7 per run) | pass in all 5 runs | pass in all 4 runs |
| A2: all four resources `ok` | pass | pass |
| A2: `irq.some` null in the tool, and no `some` line in raw | pass | pass |
| A2: system `cpu.full` total 0 in the tool and in both raw reads | pass | pass |
| extra: verdict `PRESSURE_OK`, `findings` empty | pass | pass |
| extra: exit 0, stderr 0 bytes | pass | pass |
| extra: each of the 7 average triples per run equals raw1 or raw2 | pass (35 of 35) | pass (28 of 28) |
| extra, interval runs: deltas in [0, raw2 minus raw1]; implied first read (total minus delta) in [raw1, raw2]; `stall_ratio` = delta / 1e6; cpu full delta and ratio null (A3) | pass (interval1) | pass (interval2) |

The checker found no problems in any of the nine runs. The unmodified run1 passed its own checker. The key sets of the blob `01a6448c` outputs match those of blob `f2e39df3` outputs (checked with a recursive key comparison).

## 7. Verbatim tool output: run1 and `--interval 1` on blob `f2e39df3`

Run1, `tools/mori-pressure.py` at the path (stdout, exit 0):

```json
{
  "findings": [],
  "resources": {
    "cpu": {
      "full": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.0,
        "total": 0
      },
      "full_system_undefined": true,
      "notes": [
        "parsed from the kernel PSI line grammar",
        "system cpu 'full' is undefined by the kernel: reported, never used for a threshold"
      ],
      "some": {
        "avg10": 0.14,
        "avg300": 0.0,
        "avg60": 0.03,
        "total": 11402694
      },
      "state": "ok"
    },
    "io": {
      "full": {
        "avg10": 3.75,
        "avg300": 2.52,
        "avg60": 2.63,
        "total": 123002045
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 3.95,
        "avg300": 2.62,
        "avg60": 2.71,
        "total": 128319064
      },
      "state": "ok"
    },
    "irq": {
      "full": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.0,
        "total": 22857216
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": null,
      "state": "ok"
    },
    "memory": {
      "full": {
        "avg10": 0.38,
        "avg300": 0.19,
        "avg60": 0.21,
        "total": 19783373
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 0.38,
        "avg300": 0.19,
        "avg60": 0.21,
        "total": 20023132
      },
      "state": "ok"
    }
  },
  "root": "/proc/pressure",
  "schema": "mori-pressure-v1",
  "threshold": {
    "label": "local (not calibrated)",
    "metric": "avg10",
    "value": 10.0
  },
  "verdict": "PRESSURE_OK"
}
```

`--interval 1` on blob `f2e39df3` (stdout, exit 0). The `some` and `full` totals are the second read. `total_delta_us` and `stall_ratio` are the difference from the first read:

```json
{
  "elapsed_us": 1000245,
  "findings": [],
  "interval_s": 1.0,
  "resources": {
    "cpu": {
      "full": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.0,
        "stall_ratio": null,
        "total": 0,
        "total_delta_us": null
      },
      "full_system_undefined": true,
      "notes": [
        "parsed from the kernel PSI line grammar",
        "system cpu 'full' is undefined by the kernel: reported, never used for a threshold"
      ],
      "some": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.01,
        "stall_ratio": 0.001873,
        "total": 11487023,
        "total_delta_us": 1873
      },
      "state": "ok"
    },
    "io": {
      "full": {
        "avg10": 5.27,
        "avg300": 2.72,
        "avg60": 3.42,
        "stall_ratio": 0.089388,
        "total": 124531266,
        "total_delta_us": 89388
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 5.42,
        "avg300": 2.82,
        "avg60": 3.53,
        "stall_ratio": 0.091208,
        "total": 129894692,
        "total_delta_us": 91208
      },
      "state": "ok"
    },
    "irq": {
      "full": {
        "avg10": 0.0,
        "avg300": 0.0,
        "avg60": 0.0,
        "stall_ratio": 0.011745,
        "total": 23070718,
        "total_delta_us": 11745
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": null,
      "state": "ok"
    },
    "memory": {
      "full": {
        "avg10": 1.06,
        "avg300": 0.27,
        "avg60": 0.54,
        "stall_ratio": 0.036608,
        "total": 20245981,
        "total_delta_us": 36608
      },
      "notes": [
        "parsed from the kernel PSI line grammar"
      ],
      "some": {
        "avg10": 1.06,
        "avg300": 0.28,
        "avg60": 0.54,
        "stall_ratio": 0.037224,
        "total": 20493529,
        "total_delta_us": 37224
      },
      "state": "ok"
    }
  },
  "root": "/proc/pressure",
  "schema": "mori-pressure-v1",
  "threshold": {
    "label": "local (not calibrated)",
    "metric": "avg10",
    "value": 10.0
  },
  "verdict": "PRESSURE_OK"
}
```

The outputs of runs 2, 3, 4, 5, 6, 7 and interval2 are stored in scratch with their sha256 values in Appendix A. Their totals are in section 5, and their states and verdicts match the rules in section 6.

## 8. Findings, by severity

### F1 (Medium): the selftest evidence predates both later blobs, and the measured tip is not HEAD

- The measured tip is `a730ecf` (blob `852d1ea7`). HEAD moved to `89849a7` (blob `f2e39df3`, committed 08:59:07Z), then to `a536b18` (blob `01a6448c`, the tool last written 09:03:07Z, commit `6a344d2` at 09:03:35Z).
- The one-line file `.ufo/waves/round-24/evidence/c2-selftest-after.txt` (`MORI_PRESSURE_SELFTEST: PASS 12/12`, 35 bytes, dated 08:57:19Z) predates both later blobs. `89849a7` added a second selftest output line, `MATCHER: rejected N/M corrupted expectations`, printed after PASS (diff hunk `@@ -537,7 +573,13 @@`). So the file is not the output of HEAD.
- The wave-2 mutation results in `corpus/lessons/round-24.md` (heading "Wave-2 mutation results on the C2 selftest") name tool `852d1ea7`, the measured tip. They do not cover `01a6448c`.
- I did not run `--selftest` on any blob.
- Action for the integration owner: name the blob the C2 after-value is measured on, re-run `--selftest` on it, and retain the output with the commit hash.

### F2 (Medium): the committed live record keeps totals only, and the recheck line still omits the bracket

- Commit `6a344d2` added `.ufo/waves/round-24/evidence/bracket-check.py` (83 lines) and `.ufo/waves/round-24/evidence/bracket-check-run.json` (303 lines). The JSON records five runs, all `pass: true`, with `uname` `7.2.11-arch1-1`, verdict `PRESSURE_OK` and exit 0. Its `at` stamps run from 09:03:27.397896Z to 09:03:27.505765Z. The runs used blob `01a6448c`, which was written at 09:03:07Z.
- My cross-check of the recorded `raw_before`, `raw_after` and `reported` totals found no problems. The counters never run backwards from one run to the next.
- Gaps: the record keeps totals only. It holds no raw text, no resource states and no tool JSON, so a reader cannot re-derive the passes from bytes in the file. The checker reads the raw files with Python `open()`, not `cat`. That should give the same bytes; I did not test it separately. The five runs finished within 0.11 s, so they show one moment, not a spread in time.
- `corpus/knowledge/system-pressure-r24.md:3` is unchanged at `a536b18`. It still gives the recheck as `--selftest` plus "one live run", with no bracket step.
- Action: keep the raw text and resource states in the record, or cite Appendix A of this report by hash, and add the bracket step to the knowledge recheck line.

### F3 (Medium): the bracket proves values inside a window, not the source path

- Probe (`cgroup_root_probe/`, copies taken at 09:04:04Z, blob `01a6448c`): I copied `/sys/fs/cgroup/{cpu,memory,io,irq}.pressure` between two `/proc/pressure` reads and ran `python3 -I <tool> --root <copy>`. Checked against the `/proc` bracket, all seven rows are inside, with no problems.
- The cgroup copies equal the `/proc` raw1 bytes for every kind. Against raw2 they differ by 9 to 1978 µs (cpu some 16, memory some and full 9, io some 1978, io full 1949, irq 174). The counters are the same set and move together.
- This agrees with the wave-1 finding (`.ufo/waves/round-24/w1/LivePressureCapture.md` §4, lines 158 to 166): root-cgroup files are byte-identical to the system files in a same-process read.
- Consequence: a tool that read the wrong files would pass A2 on this host. The tool's `"root": "/proc/pressure"` field echoes the argument, so it is not evidence of the source. The committed checker has the same limit, because it compares values with `/proc` only.
- The shipped default path is correct: the default root is `/proc/pressure`, and the output says so. Nothing here shows a defect in the default. The point is that A2 cannot serve as a source-identity control. The owner should either state that the check proves values only, or add a path-identity assertion.

### Checked, no defect

- **Live reader.** The only file open on the live path is `open(path, "r", encoding="utf-8")` in `_read_resource` (line 157 on both blobs). The other `open` call (line 534) reads the selftest cases file. The hook variables are set only inside `_case_failures` and restored in `_selftest`. This is a literal grep result, not a semantic reference check.
- **New UTF-8 clause** (blob `01a6448c`, lines 162 to 164). Exercised by the non-UTF-8 probe (section 9). It returns `malformed` with a note, not zero, as the commit says.
- **Host facts.** `corpus/knowledge/system-pressure-r24.md:2` says PSI is on, irq carries one full line and system cpu full total is 0. My reads agree. `cat /proc/cmdline` has no `psi=` token.
- **Interval mode.** Follows A3. Cpu full delta and ratio are null. `elapsed_us` is 1000245 and 1000287 for a 1 s request, with wall time 1.04 s in both runs.
- **Averages.** Match the raw bytes in all 63 triples (section 6).

### Lane hygiene (outside this scope; for the integration owner)

- `tools/__pycache__/` is still untracked at 09:08:48Z. Its only file, `mori-dispatch-ledger.cpython-314.pyc`, is dated 05:19 local (08:19Z), before this session. My runs did not write it, because `python3 -I <script>` does not cache the script itself.

## 9. Negative controls

- **Mutations of the run1 output, checked by the checker.** Five mutations, all rejected: cpu some above raw2 (`cpu some: total 11402702 outside raw bracket [11402661, 11402701]`); irq some filled in (`irq some: tool reports a value but raw lacks the line`); memory state `absent` (`memory: state=absent`); cpu full total 5 (`cpu full: total 5 outside raw bracket [0, 0]`); io full below raw1 (`io full: total 122999878 outside raw bracket [122999879, 123002523]`). The unmodified run1 passes.
- **Stale root (blob `f2e39df3`).** The tool was run on copies of the run1 raw1 bytes. Checked against the run2, run3 and interval1 brackets, the output is rejected each time. Example, run2: `cpu some: total 11402661 outside raw bracket [11439488, 11439605]`. So the check does catch a stale read once the counters have moved.
- **Cgroup-root probe (blob `01a6448c`).** Passes all seven rows (F3). The check is not a source-path control.
- **Non-UTF-8 probe (blob `01a6448c`).** The `cpu` file was one valid line followed by bytes `\xff\xfe`. The tool reported `cpu` `malformed` with the note `file content is not UTF-8 text; resource malformed, never reported as zero`. The other three resources were `ok`, the verdict was `PRESSURE_PARTIAL`, exit 0, stderr empty and findings empty.

## 10. Residual risk and verification gaps

- `--selftest` was not run by me on any blob. The HEAD selftest behaviour is read from the diff only (F1).
- The live `PRESSURE_HIGH` path was not exercised. The values seen were avg10 0.00 to 5.42, far below the 10.0 threshold. The wave-1 capture recorded io some avg10 10.57 at 08:22:34Z, so the threshold path is reachable on this host.
- EOPNOTSUPP and EACCES were not exercised live. The wave-1 capture (`w1/LivePressureCapture.md` §6) reports them unreachable on this host. I did not re-test that.
- The tool process windows of the one-shot runs (default root and the tip copy) were 27.6 to 33.4 ms. Inside a window that short, the bracket cannot tell a read from another read taken moments earlier when the counter did not move, and it says nothing about slow drift.
- The `lsp` device is not available to this seat. Call-site statements rest on a literal grep of the file.
- System pressure is host-wide. Peer seats were running during these reads. The values say nothing about cause (A2).
- The tool's `root` field echoes the argument. It is not evidence of the source (F3).

## 11. Tooling record and writes

- **Installs or updates: none.** The tools used were already present: `python3` 3.14.8, coreutils (`cat`, `date`, `sha256sum`, `wc`, `tail`, `cp`, `mkdir`, `ls`, `stat`, `od`, `printf`), `git`, and the grep and read tools. No pacman transaction was attempted, and the pacman pause was not touched.
- **Lane writes: this report only.** Git was used with `--no-optional-locks` and read-only subcommands only (`rev-parse`, `log`, `status`, `cat-file`, `diff`, `show`, `merge-base`). No `jj` command was run.
- **Scratch writes:** `/fast/scratch/hyaku/mori-r24-a2/w2/LiveBracketCheck/`, containing `run1`, `run2`, `run3`, `interval1`, `run4_a730ecf`, `run5_current`, `run6_current`, `run7_current`, `interval2_current`, `stale_root_from_run1`, `cgroup_root_probe` and `utf8_probe`.

## Appendix A: sha256 of every raw read and tool output

Byte counts are from `wc -c` and file sizes. Paths are relative to the scratch directory.

| run | file | bytes | sha256 |
|---|---|---:|---|
| run1 | raw1_cpu | 101 | b3c62bfa5adc11fd62c07b0c31dee35d3f90eb2cdc984f4046780a31034b639f |
| run1 | raw1_memory | 108 | 579026bf0d1366b3c5828329da5ebe6bcabf2ce591bd4f7fa844ab1aa7b5ba91 |
| run1 | raw1_io | 110 | f1f2399fc163c1c0b1704fc053a26240c65eda36a4e0a4a482908522b15ee368 |
| run1 | raw1_irq | 54 | d7c5388891c9a606915a491e6f0b41f91f0555c8110a4b0ea89182a320f1b8ad |
| run1 | raw2_cpu | 101 | 352b92e07beed29d7ba9fbb439b3827d7ff1cf3b6607b9547fbca68e65b9ab15 |
| run1 | raw2_memory | 108 | 579026bf0d1366b3c5828329da5ebe6bcabf2ce591bd4f7fa844ab1aa7b5ba91 |
| run1 | raw2_io | 110 | 43c2de2b498817c6474ba7d39ce1d4c825f6a39343867853d7c60852298498f1 |
| run1 | raw2_irq | 54 | 8ee96dd8e7b2606bdb8e8930f2934575d8333fa8aebcb688bf08ba9b086d84c3 |
| run1 | tool.json | 1684 | 29be297bb6acf51ab44072d33ee0493e64ddea8be840774ed2311a65cd699533 |
| run2 | raw1_cpu | 101 | 7e4b0559896f8126e45b5ecdaf481a40a02983603729df94f944f41740a6daa8 |
| run2 | raw1_memory | 108 | e81441e21d63132375904704c9f22590f090bfffbccb64845324a75e7b8a0b0a |
| run2 | raw1_io | 110 | e3f3b22e03e78c048e152c4ad5f92883e6ca8374eb5c5a9dbaf87fe9e3c2fc86 |
| run2 | raw1_irq | 54 | b68deaf18cc6d2fed3fb108609fe5e6e7b0774a865ab6b7807424fead38388b4 |
| run2 | raw2_cpu | 101 | 87909cde74f4e4ee9d0729b6824b1e4ba30ab57404fc3344956bb185573d8ea1 |
| run2 | raw2_memory | 108 | 3b27791edf9c149e4a30c2142237bdd81541af8a359264f1c32f1269f7b63fc0 |
| run2 | raw2_io | 110 | b2e92510c13ab3bed0c74d6c2400d2fbb49243bded759735e8ba53d585607411 |
| run2 | raw2_irq | 54 | f03ef629bda856e1c6dcf20946252eed1e1be1e78a5d9da922f4034a4b03f2a8 |
| run2 | tool.json | 1681 | 5aa0d1e35e00cd4a55dff3b598859989ddb8cc9b117e95c14a4b59663992bb53 |
| run3 | raw1_cpu | 101 | 650373d7f5bc8651bd30b48666c09a7baaf0fbdfdf7ca8a2eff906237c0f1772 |
| run3 | raw1_memory | 108 | 3a17ed9e75dffce0d964830b32e4471d9c694d70bb3727f0482e02ef5e86124e |
| run3 | raw1_io | 110 | 19b5ccba5b92fa8768766bb84590fafce526c470824ed88522abedb0483550f1 |
| run3 | raw1_irq | 54 | 3276ca41f85ab067bf8e9dc6d53f4df801c566f818b6681c3bdd5d2e6462639c |
| run3 | raw2_cpu | 101 | 595e75c0eedbb8cab17d2dd2ceec9fcd852f6e45020f387d72de15f4842ae0ea |
| run3 | raw2_memory | 108 | 0e2c86bd87a77cdd3f7d1888816c8822d7462dfa9a865e1c10264dc8aab72ddb |
| run3 | raw2_io | 110 | 012d677eb42734b2e88f57ef47f2d9f096967b1df3ec64208c1a2d9ad5f6256f |
| run3 | raw2_irq | 54 | b9fb8bc2be569fa0f2c75082e4ac9d62125a41dc8336565a2ca9517ba80604b4 |
| run3 | tool.json | 1682 | b9a977b1bc1ca9b47259fc0e72402d0b4adf9840a7cd0566c52a500ed5565f01 |
| run4_a730ecf | raw1_cpu | 101 | 4008cb983e09ebea3418c344239ce2009ce455a8bba562b4206f8dc1b34f5d8e |
| run4_a730ecf | raw1_memory | 108 | 9835527daee1fab24f51cadc13404e3b4dd7b86c81a571316e8487d9e46fc0ef |
| run4_a730ecf | raw1_io | 110 | 5d9f13aa1f14666414615fcd2a2637b434d7d895dfc61840dc065c1edb415944 |
| run4_a730ecf | raw1_irq | 54 | f2cd079d430517e7efb676216bfa1b58941d00d4360d132e0e0ae16cd487cfeb |
| run4_a730ecf | raw2_cpu | 101 | ef5227cb816298d4f02ea07a1aa427e5119bc3fde1eff97b8afb3d7cd5675e47 |
| run4_a730ecf | raw2_memory | 108 | 9835527daee1fab24f51cadc13404e3b4dd7b86c81a571316e8487d9e46fc0ef |
| run4_a730ecf | raw2_io | 110 | 6195e8c1ece16f2ff03811981aac870230b98a6d1b2b759b2c6c1a99c3b7bb9f |
| run4_a730ecf | raw2_irq | 54 | d5c2ff669d31ea69bf3eae430d0a7daeda145f69478623da9406ced95a85d3c7 |
| run4_a730ecf | tool.json | 1682 | 7124556e3ab189ac523a16e36b64f8fb396b153fd11652d995fdbfac671226e6 |
| interval1 | raw1_cpu | 101 | 559c3551415b2e9e136d8e9cc76f7265c9960aa38f7517e3ae7e28b16f5a460d |
| interval1 | raw1_memory | 108 | cc75aae354079f099bc42112747785784ca2f2cdd5b00b24628041319a59d434 |
| interval1 | raw1_io | 110 | 9d2de6f10b6dc2320712641ef1cff720649d4f35eda9c145d8897c504c2c5183 |
| interval1 | raw1_irq | 54 | 136f52c3d610b9971f170b75b5277fd2e600d04e1b1090389feff06da1ffc9d9 |
| interval1 | raw2_cpu | 101 | a43c15ca0187e5a230873abfde7ffbf57c8794f266b4026da52bcfb591d4ea19 |
| interval1 | raw2_memory | 108 | 4e097d6a21d89bd07cc31aa07eef0ec0abd8a2dde9c41cee2654d309ced21f07 |
| interval1 | raw2_io | 110 | c8c59f5e9892dab27269c5dfc81b82fd2f5e169ab88c3fadf0be4ec18795e70c |
| interval1 | raw2_irq | 54 | ff478e4b011d4702b2467d9f4c14b2eedbf9b5146d8e46817097c2e1ecf74320 |
| interval1 | interval.json | 2185 | 78110b55d82960de37e538446d776d56f21d8b7fc833e4f48cd66d4428603e85 |
| stale_root_from_run1 | tool.json | 1742 | c345f36fdcbf014b46253df26d4c84bc4566c4ef8ea18ff74b008cd00f2b3471 |
| run5_current | raw1_cpu | 101 | b559d435fdbe4ecad32f1403243378d09ca4229dde3dad27d029716e527e0f6f |
| run5_current | raw1_memory | 108 | aa883ff7d9070c6230d071a34f344fc533f13c2d96c449ecdca14207c506780c |
| run5_current | raw1_io | 110 | e35e0c87d286ecb6b0ed2650cd912a3f4425be5dff48c422bdf51024235e2b13 |
| run5_current | raw1_irq | 54 | 2e7c4cafec4996d83e759e8b78aa4ee7108b8644277b68163b06fa1287050d30 |
| run5_current | raw2_cpu | 101 | ad747d135ace9d070addfbf5c4467290b273af056ec15f5b3e3428bf0cc30a7d |
| run5_current | raw2_memory | 108 | aa883ff7d9070c6230d071a34f344fc533f13c2d96c449ecdca14207c506780c |
| run5_current | raw2_io | 110 | 2a8295c4a3bfd1515f3d1282e329d0427cab5a9ef5c7076169021080d4d14e68 |
| run5_current | raw2_irq | 54 | ac0aa33ca6f56ed18a7faf35ca91013dc28538d3b777492aca4808cdd5277732 |
| run5_current | tool.json | 1685 | c509a1a31d7311806b725966bf07c157cae47e1d9e0d993ef479c5d874c36bc0 |
| run6_current | raw1_cpu | 101 | e12927a2a8bc1182eedc3031c4845c2fa16bafb9b53dc12435f067e2091921bd |
| run6_current | raw1_memory | 108 | 88fb33f2c32b82c7e9dbee03d4a8353db2d62db6a995f515ba1068739fd3178d |
| run6_current | raw1_io | 110 | a8898f472398e7e3a353970d911a9d15d41ff7ab00a6c04a4098f1b877beefc0 |
| run6_current | raw1_irq | 54 | 51a1d4a558bd77ef266899723e1a6da34bdb9eb375e01a6eb7ef42ab4314c2bb |
| run6_current | raw2_cpu | 101 | fe92e981b12cec0d2c80a20050ec65e4f3cf5170c0bd43b15b94a2834250e1f1 |
| run6_current | raw2_memory | 108 | 88fb33f2c32b82c7e9dbee03d4a8353db2d62db6a995f515ba1068739fd3178d |
| run6_current | raw2_io | 110 | 8203b2420b18ad25593f7a5e9f660765b7b55fdbbb68bb02a88bb49e5cafefe5 |
| run6_current | raw2_irq | 54 | fa09c04dbcbc1f5e1e2345d8a6bf988763c8f77d41f0966891cd380da61d9de2 |
| run6_current | tool.json | 1684 | 60e4e33bbb6a83c1c5cdb38a93dc40d3b7232a6e0a3ab34cf7bc7c478aa68db7 |
| run7_current | raw1_cpu | 101 | 70f6afbc1582ac5f3504f364f91861c13106a575b2b6473708bc62caaf4914c2 |
| run7_current | raw1_memory | 108 | 33f27930ebf7acde5961002f63e340673fa7c38ea425d54ba69a852b1695f13b |
| run7_current | raw1_io | 110 | c02fbfab36ba47a452bd2b9e6f18e15991501af9b61e0af1c44516bca4387898 |
| run7_current | raw1_irq | 54 | aaa47fd1cc72ec2469390b51e1da4776d29c3bdf09747250a38a99c9a5933de2 |
| run7_current | raw2_cpu | 101 | e106c4093e8534c573873219975aca9ed5481d414937d1706da6627722af7ceb |
| run7_current | raw2_memory | 108 | 33f27930ebf7acde5961002f63e340673fa7c38ea425d54ba69a852b1695f13b |
| run7_current | raw2_io | 110 | 7934be0b252335f43c97b75bfe49959715cccdc7aa87da8d6de1bc5299d709bf |
| run7_current | raw2_irq | 54 | e4340ce1d189651d162ab132470af2e16d85da21afaa1a6eeb94bb843e2e0597 |
| run7_current | tool.json | 1687 | 53e052f7a704af69f9b1025edb9c4c1fffc9287d181730cada54a94fe9fe4d15 |
| interval2_current | raw1_cpu | 101 | bb8f8548a69800ff61f35244d494b38a2660df777a0f6af99dcc48d73caa3d93 |
| interval2_current | raw1_memory | 108 | ecf69b7b864ce06d53a64236d2bea496c9b69a14c3005405db5fe92ddb3d15cc |
| interval2_current | raw1_io | 110 | 045b03b533a1a3ed3e065e5d915bd8033e5f38120e6db2a7d7b6c2350e14d8b3 |
| interval2_current | raw1_irq | 54 | 29b8bf8321538911f5c9c9763abdff3b9ff24541bbbeef0d7359bbd537ce72ba |
| interval2_current | raw2_cpu | 101 | e1b8f9b1beba622b09b9c451fb1edc735e102d7dc18f966039c688ff71cf374e |
| interval2_current | raw2_memory | 108 | 5f250fd09e90f9be6585b6791a095f6b96a2892a2105e1f1e19d72156db1ac92 |
| interval2_current | raw2_io | 110 | 9b413dc62a47610dd9c8264b883f319e705a4b5a4393829076f5bf90262c4b0f |
| interval2_current | raw2_irq | 54 | 659eb8b04e3408c3ae2e49831fe4d8f5cbc25d32d11a6f4a6ba3e2b0f651ab32 |
| interval2_current | interval.json | 2188 | c342fed0f91b83448ce280cf104e1c21423d91867548fde070b7284b9e503033 |
| cgroup_root_probe | root/cpu | 101 | 8a239621b250dcd96c3405ff5c9633074be0b9c408319c1350195977c4d318de |
| cgroup_root_probe | root/memory | 108 | 875eb26823d94e50b3d04de93a983e44dc3859456acabf4245893ccfb93181f9 |
| cgroup_root_probe | root/io | 110 | 65690d41abd41ab6184b4433493a9d53a0c0fe63cf85fc8811e1be68f92ab699 |
| cgroup_root_probe | root/irq | 54 | f54e7128017dabf7c1d6e72ec34df54552ba692e797dd4fc0c1184e945cc85e4 |
| cgroup_root_probe | tool.json | 1741 | 960a34e528122174c36212f0fda8c2ec76d04cd2963c5976d63830d0beaae9a0 |
| utf8_probe | cpu | 50 | a7ad615c62ead84d8519963c6660c2b79203b9bfaf1783a132a33d06bd91c3fa |
| utf8_probe | memory | 108 | 33f27930ebf7acde5961002f63e340673fa7c38ea425d54ba69a852b1695f13b |
| utf8_probe | io | 110 | c02fbfab36ba47a452bd2b9e6f18e15991501af9b61e0af1c44516bca4387898 |
| utf8_probe | irq | 54 | aaa47fd1cc72ec2469390b51e1da4776d29c3bdf09747250a38a99c9a5933de2 |
| utf8_probe | tool.json | 1497 | d2a8bed1b354104fcd29cac8e6a055ed3f3c44bcf4cee405fd12c13b36f41906 |
| committed | evidence/bracket-check-run.json | 4746 | 6f3de8446fc0cfb6318f04fb6b204ff0361568cbfdfa95ebbbdc32d98eea49c1 |
| committed | evidence/bracket-check.py | 3068 | 8772cf137bff3a1a46a5925ecfd9b43ac0359fa0a6f2a58900c2313d4bf6d5cd |
