measured 2026-10-23T05:44:18Z
# MutLiveArm — five live-arm mutation probes

Axes: counter sensitivity, minimal behavioral changes, reproducible witnesses, exact restoration.

Citation prefixes: `S` = `/fast/scratch/hyaku/mori-r34/a2-MutLiveArm`; `L` = `/home/vgpnk/Projects/shokunin/mori-shokunin`. Every `S/...:line` or `L/...:line` below expands to that absolute path.

## Scope and detector

Target: `8d56809afccefe0ab80c8e73ac3e1ea57c25f5f3`, tool `tools/mori-disk-rate.py`; each before receipt records this revision (`S/reuse.before.txt:1-2`, `S/skip-sleep.before.txt:1-2`, `S/half-sleep.before.txt:1-2`, `S/measured-time.before.txt:1-2`, `S/mountinfo-path.before.txt:1-2`).

Isolation command: `timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r34/a2-MutLiveArm/clone`; output: `Cloning into '.../clone'... done.` Five detached worktrees under S hold independent mutants; their commits and hashes are in `S/mutants.json:2-30`.

Each of the 15 detector calls used the unchanged frozen counter with fresh default randomness, all 12 fixed and 300 random scenarios, a 600-second timeout and 1 GiB address-space bound. Exact commands, seeds and outputs are retained in each `<mutant>.before.txt`, `<mutant>.mutant.txt`, and `<mutant>.restored.txt` (`S/reuse.before.txt:1-10`; other receipts cited below). Calls within each stage ran concurrently; stages were pristine, mutant, exact-byte restoration, restored revision.

## Results

Witness numbers are `sda.write_Bps` and `host_write_Bps`, pristine → mutant, from the controlled-live witness described below. They are not offline CLI differences.

| Mutant / committed revision | Diff summary | Expected detector | Actual counter output line | Verdict | Witness |
|---|---|---|---|---|---|
| reuse / `7ce1a8f0f7fb60bfffcf0816506e338ddd47b52d` | Return `first, first`; keep nominal sleep (`S/reuse.mutant.py:182-184`). | Fed live requires two readings and exact output (`L/.ufo/waves/round-34/count-c1-a1.py:356-365`). | `live=fed-mismatch`; `C1=unmet`; exit 1 (`S/reuse.mutant.txt:6-7,21`). | killed | 5120 → 0; one read (`S/witnesses/reuse/result.json:17,37-49`). |
| skip-sleep / `b5b92adcb68b7286af7db8db5bb17019f9bab256` | Delete the sleep; retain two reads (`S/skip-sleep.mutant.py:182-183`). | Fed minimum separation, 0.9 × 400 ms (`L/.ufo/waves/round-34/count-c1-a1.py:312,358-359`). | `live=fed-no-interval`; `C1=unmet`; exit 1 (`S/skip-sleep.mutant.txt:6-7,21`). | killed | 5120 → 0; no sleep (`S/witnesses/skip-sleep/result.json:17,37-51`). |
| half-sleep / `f5bf84afbe8e7d54e4f7cf3b3a99decd42d9b720` | Divide requested milliseconds by 2000 instead of 1000 (`S/half-sleep.mutant.py:182-184`). | Same fed minimum separation. | `live=fed-no-interval`; `C1=unmet`; exit 1 (`S/half-sleep.mutant.txt:6-8`). | killed | 5120 → 0; sleep 0.2 s (`S/witnesses/half-sleep/result.json:17,37-53`). |
| measured-time / `8703c440eff9c5d5657e970b7db0e25b2b536b0e` | Divide live rates by integer measured elapsed milliseconds, retaining nominal `interval_ms` metadata; offline denominator unchanged (`S/measured-time.mutant.py:280-289,296-297`). | Fed exact oracle uses nominal milliseconds (`L/.ufo/waves/round-34/count-c1-a1.py:364-365`; `L/.ufo/waves/round-34/contract.md:46-47`). | `live=ok`; `C1=met`; exit 0 (`S/measured-time.mutant.txt:6-8`). | survived | 5120 → 4096 with 500 ms measured vs 400 ms nominal (`S/witnesses/measured-time/result.json:17,33,37,53`). |
| mountinfo-path / `8d8a8482aae9ea66a2ad30e9ab88a57613cd390d` | Read `/proc/self/mountinfo`; choose first procfs mountpoint, then its `diskstats`, instead of the fixed canonical path (`S/mountinfo-path.mutant.py:182-188`). | A path-dependent case needs an alternate proc-view challenge; the frozen fed test binds only `/proc/diskstats` (`L/.ufo/waves/round-34/count-c1-a1.py:339-344`). | `live=ok`; `C1=met`; exit 0 (`S/mountinfo-path.mutant.txt:6-8`). | survived | 5120 → 0 with a stale alternate proc view listed first (`S/witnesses/mountinfo-path/result.json:17,37-55`; `S/witness.py:63-79,101-103`). |

VERDICT: killed — reuse
VERDICT: killed — skip-sleep
VERDICT: killed — half-sleep
VERDICT: survived — measured-time
VERDICT: survived — mountinfo-path

All five mutant runs still reported `fixed_pass=12/12 random_pass=300/300` and `coverage=ok` (`S/reuse.mutant.txt:4-5`, `S/skip-sleep.mutant.txt:4-5`, `S/half-sleep.mutant.txt:4-5`, `S/measured-time.mutant.txt:4-5`, `S/mountinfo-path.mutant.txt:4-5`). Reuse and skip-sleep also emitted a feeder-thread `BrokenPipeError`; this is retained, not suppressed (`S/reuse.mutant.txt:8-19`, `S/skip-sleep.mutant.txt:8-19`).

## Pristine/restored brackets

Every before and restored call produced `live=ok`, `C1=met`, exit 0; therefore none of these outcomes is being called a kill on a failed baseline.

| Mutant | Pristine receipt | Restored receipt |
|---|---|---|
| reuse | `S/reuse.before.txt:6-10` | `S/reuse.restored.txt:6-10` |
| skip-sleep | `S/skip-sleep.before.txt:6-10` | `S/skip-sleep.restored.txt:6-10` |
| half-sleep | `S/half-sleep.before.txt:6-10` | `S/half-sleep.restored.txt:6-10` |
| measured-time | `S/measured-time.before.txt:6-10` | `S/measured-time.restored.txt:6-10` |
| mountinfo-path | `S/mountinfo-path.before.txt:6-10` | `S/mountinfo-path.restored.txt:6-10` |

## Witness inputs and the offline constraint

The requested offline-only output difference cannot be honestly supplied for isolated live-arm mutations: `--a` plus `--b` takes the saved-sample branch and does not call `read_live_samples` (`L/tools/mori-disk-rate.py:282-286`). Changing shared offline semantics merely to force that difference would introduce a second defect.

I exercised the requested offline command separately for every mutant. All ten CLI executions exited 0 and produced the same JSON: `sda` class `disk`, state `ok`, rate 5120, host basis `["sda"]`, host rate 5120, interval 400. Each receipt records `offline_equal: true`, not a fabricated differing witness (`S/witnesses/reuse/result.json:2-14`; `S/witnesses/skip-sleep/result.json:2-14`; `S/witnesses/half-sleep/result.json:2-14`; `S/witnesses/measured-time/result.json:2-14`; `S/witnesses/mountinfo-path/result.json:2-14`).

Each mutant has its own saved `a`, `b`, and `sys/class/block/sda/device` input under `S/witnesses/<mutant>/`. A has 100 sectors written, B has 104, and interval is 400 ms; the generator and exact offline CLI are `S/witness.py:27-38,95-106`.

Additional live witnesses are module-level controlled executions, not unmodified live CLI runs or a second counter. They execute the saved pristine/mutant source and actual `main`/classification/report logic, replacing that loaded module's sample reader, clock, and mountinfo read only. The clock charges 50 ms per sample read; canonical data advances to B at 450 ms; an alternate proc view remains at A (`S/witness.py:41-90`). This makes all five behavioral differences concrete without write load or additional mounts. Mountinfo is synthetic; it does not expose host mount records (`S/witness.py:101-103`).

Witness command: `timeout --kill-after=3 120 prlimit --as=1073741824 -- python3 -B /fast/scratch/hyaku/mori-r34/a2-MutLiveArm/witness.py`. Output for every name: `offline_equal=True controlled_live_output_differs=True`; exact JSON and call traces are retained in the per-mutant `result.json` files cited above.

## Coverage findings, not contract changes

- Measured-time survived this fresh-seed frozen run while the controlled 500 ms witness changed the rate from the required nominal result. This is a counter gap for read-duration overhead. The actual elapsed denominator inside the frozen run was not instrumented; why that run matched is not directly observed (`S/measured-time.mutant.txt:3-8`; `S/witnesses/measured-time/result.json:17,37,53`).
- Mountinfo-path survived this frozen run while the controlled alternate-mount ordering changed which data it read. This is a counter gap for environment-dependent path discovery, not evidence that the real host has such an alternate view (`S/mountinfo-path.mutant.txt:3-8`; `S/witnesses/mountinfo-path/result.json:39-55`).
- These are single-run mutation outcomes, not a claim that either mutant survives every seed or host. No rule, counter, seed count, or landed source was changed.

## Exact restoration and hashes

Common pristine/before/restored SHA-256: `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b` (`S/mutants.json:5,11,17,23,29`; `S/restoration.json:4,10,16,22,28`). Each restored worktree was committed and the detector was run on that restored commit, not merely on the original base revision (`S/restoration.json:5-6,11-12,17-18,23-24,29-30`; restored receipts line 1).

| Mutant | Mutated SHA-256 | Restored revision |
|---|---|---|
| reuse | `74d94b40af23199f1bed153a5a21821e247d1179025e99d34c85d060eb408a85` | `2c92f1084fbe4cdd54a0102aded589f34924e3bf` (`S/restoration.json:3-6`) |
| skip-sleep | `7c940497c0f40e50986d562530b36dda9e3e7006f0ce18051f3c961c62362db0` | `ae8e89fae2455cc54242cee941f2f7864ff728de` (`S/restoration.json:9-12`) |
| half-sleep | `d5dfb3997eb169e95d242a7804888c544515d5666ac56364db02baca494c6252` | `96c7f9dae40725a54666071134b928b8094c11f2` (`S/restoration.json:15-18`) |
| measured-time | `55395c2dae82db0b584eec2e76dc56b0d319a2c75b256261cc29a0e7af1a8607` | `df807d95e4019ace052a835f18d3baf047ba178a` (`S/restoration.json:21-24`) |
| mountinfo-path | `c4dc0bb859913eadcb9323a2fdb319dc71364e57041d214e3db8ca550e60555c` | `cca677a1eaa75f23d4b85bd1d465d21dd96a85c8` (`S/restoration.json:27-30`) |

Before and after command: `timeout 10 prlimit --as=134217728 -- sha256sum <L/tools/mori-disk-rate.py> <L/.ufo/waves/round-34/count-c1-a1.py> <L/.ufo/waves/round-34/contract.md>` (angle brackets denote expanded paths, not literal shell syntax). Both outputs had these SHA-256 values (paths shown relative to L):

```
370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b  tools/mori-disk-rate.py
c14c3494d7356fa7c619a0e30c10cd9b71baa99eb0fb74cfd34c7f21b3b181e2  .ufo/waves/round-34/count-c1-a1.py
695c8412769da278932b44198649853c140d0eeda88e7591f71bc2950765cc11  .ufo/waves/round-34/contract.md
```

No tool installs or updates. No subagents, OMP/FSD runtime invocation, write load, or lane Git/JJ writes were used. All launched commands were bounded foreground subprocesses and returned; no background jobs were started. Only this report was authored in the lane; restored worktrees, committed mutants, snapshots, fixtures, diffs and raw receipts remain under S for the integration owner.
