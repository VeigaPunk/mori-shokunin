measured 2026-10-23T04:57:34Z

# CtlSysBlock — wrong sysfs root

Sandbox: `/fast/scratch/hyaku/mori-r34/CtlSysBlock/clone`.
Sandbox control commit: `0ca2a59d637c1930dd42a89a143ec585c3a94bca`.
The clone started at the exact required frozen commit, `24603186b555dddb88ebd607e415e27bdea747b4`; the ancestry check exited 0.
Pristine contract-correct implementation commit: `929f48e622a05f17d57a5e4a935092a0d831d40a`.
Restoration commit and final sandbox HEAD: `661ba91a908e42772ff3eeb7f81b42c66bf66bd0`.
The control remains available at its recorded commit; the final worktree has the exact pre-mutation bytes.

Axes: fidelity to R1–R7 except the assigned sysfs-root defect; detector discrimination; containment and reproducibility.

## Mutant and expected detector

The program was written from the contract, not copied from the counter. Its sole mutation changes line 93 from
`block_root = args.sysfs / "class" / "block"` to `block_root = args.sysfs / "block"`.
Both classification and sysfs-only device discovery share that root; parsing, state precedence, rates, host aggregation,
and offline/live interfaces are otherwise unchanged.

Expected detector: `C1=unmet`, because fixtures expose classes and sysfs-only names under `class/block`, not `block`;
the host's partition names should also be misclassified in the live arm. The same full bounded detector was run on
pristine, mutant, and restored bytes. The two mutant runs were concurrent, each with its own fresh random seed.

## Full control source at the control commit

```python
#!/usr/bin/env python3
"""Report write rates between two diskstats snapshots."""

import argparse
import json
import os
from pathlib import Path
import time


def read_snapshot(text):
    result = {}
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 3:
            continue
        numbers = fields[:2] + fields[3:]
        valid = len(fields) in (14, 18, 20) and all(
            number.isascii() and number.isdecimal() for number in numbers
        )
        result[fields[2]] = int(fields[9]) if valid else None
    return result


def device_class(block_root, name):
    directory = block_root / name
    if not directory.is_dir():
        return "unknown"
    if os.path.lexists(directory / "partition"):
        return "partition"
    slaves = directory / "slaves"
    if slaves.is_dir() and any(slaves.iterdir()):
        return "stacked"
    if os.path.lexists(directory / "device"):
        return "disk"
    return "virtual"


def report(first, second, block_root, interval_ms):
    names = set(first).union(second)
    if block_root.is_dir():
        names.update(entry.name for entry in block_root.iterdir())
    devices = {}
    for name in sorted(names):
        present_a, present_b = name in first, name in second
        rate = None
        if (present_a and first[name] is None) or (present_b and second[name] is None):
            state = "bad-line"
        elif not present_a and not present_b:
            state = "absent"
        elif not present_b:
            state = "gone"
        elif not present_a:
            state = "new"
        elif second[name] < first[name]:
            state = "reset"
        else:
            state = "ok"
            rate = (second[name] - first[name]) * 512 * 1000 // interval_ms
        devices[name] = {
            "class": device_class(block_root, name),
            "state": state,
            "write_Bps": rate,
        }
    basis = sorted(name for name in devices if devices[name]["class"] == "disk")
    total = None
    if basis and all(devices[name]["state"] == "ok" for name in basis):
        total = sum(devices[name]["write_Bps"] for name in basis)
    return {
        "interval_ms": interval_ms,
        "devices": devices,
        "host_basis": basis,
        "host_write_Bps": total,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", type=Path)
    parser.add_argument("--b", type=Path)
    parser.add_argument("--sysfs", type=Path, default=Path("/sys"))
    parser.add_argument("--interval-ms", type=int, required=True)
    args = parser.parse_args()
    if (args.a is None) != (args.b is None):
        parser.error("--a and --b must be supplied together")
    if args.a is None:
        source = Path("/proc/diskstats")
        first = source.read_text()
        time.sleep(args.interval_ms / 1000)
        second = source.read_text()
    else:
        first, second = args.a.read_text(), args.b.read_text()
    block_root = args.sysfs / "block"
    result = report(read_snapshot(first), read_snapshot(second), block_root, args.interval_ms)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
```

## Frozen counting command

Each invocation used this unchanged command, with inherited `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed:

```text
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlSysBlock/clone
```

All four invocations completed, and every stderr stream was empty.

## Mutant run 1 — full output

```text
measured_at=2026-10-23T04:56:34Z repo=/fast/scratch/hyaku/mori-r34/CtlSysBlock/clone rev=0ca2a59d637c1930dd42a89a143ec585c3a94bca
tool=present guard=clean seed=7423136563260544691
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:nvme0n1p1
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
exit_code=1
```

## Mutant run 2 — full output, fresh seed

```text
measured_at=2026-10-23T04:56:34Z repo=/fast/scratch/hyaku/mori-r34/CtlSysBlock/clone rev=0ca2a59d637c1930dd42a89a143ec585c3a94bca
tool=present guard=clean seed=16836972923348506565
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:nvme0n1p1
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
exit_code=1
```

## Pristine run — full output

```text
measured_at=2026-10-23T04:56:06Z repo=/fast/scratch/hyaku/mori-r34/CtlSysBlock/clone rev=929f48e622a05f17d57a5e4a935092a0d831d40a
tool=present guard=clean seed=2198428297553690251
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit_code=0
```

## Restored run — full output

```text
measured_at=2026-10-23T04:57:08Z repo=/fast/scratch/hyaku/mori-r34/CtlSysBlock/clone rev=661ba91a908e42772ff3eeb7f81b42c66bf66bd0
tool=present guard=clean seed=473339257939407884
fixed_pass=12/12 random_pass=300/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
C1=met
exit_code=0
```

## Restoration and containment evidence

Measured SHA-256 of `tools/mori-disk-rate.py`:

| stage | SHA-256 |
|---|---|
| before mutation | `69b39a51217fccbbaab5b2770cfba11f3436fb4af6507cf81005209036a77b17` |
| mutated | `4c66fcf78f384aa953345fbb352ecea6878d8b1b82946870403b54ba1fa47733` |
| restored | `69b39a51217fccbbaab5b2770cfba11f3436fb4af6507cf81005209036a77b17` |

The baseline and restored hashes are identical. Both passed the complete fixed/random/live detector; the mutant failed
both complete runs. Mutation verdict: **killed**, not inconclusive.

Frozen input hashes were measured before and after the probe and were unchanged:

- `contract.md`: `f6c092fdca22a2041fa82f1c269e8805fbda3870572f5397300c6795dc61da9b`.
- `count-c1.py`: `0f0dd6d9114fa77d562a8ec1ddb811b4cd0eb3d32c71ea7551a37dd67826202e`.

All git writes were confined to the sandbox clone. This report is the only file created inside the lane repo.
Every executed command was bounded by `timeout`; all started subprocesses completed, and no background service was started.
Tool installs/updates: none.

## Host check: does `/sys/block` list partitions?

No. Actual `timeout 15 ls /sys/block` output (exit 0):

```text
dm-0
nvme0n1
nvme1n1
sda
sr0
```

The host does have partition class entries: `sda1`, `sda2`, `nvme0n1p1`, `nvme0n1p2`, `nvme1n1p1`, and `nvme1n1p2`.
Listing their `/sys/class/block/<name>/partition` attributes succeeded (exit 0). None appears in `/sys/block`.
The live failure `live-class:nvme0n1p1` therefore exercises the assigned root defect on this host, not only synthetic fixtures.

control CtlSysBlock: C1=unmet
