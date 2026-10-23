measured 2026-10-23T04:56:07Z

# CtlNoReset — partial no-decision control

- Sandbox: `/fast/scratch/hyaku/mori-r34/CtlNoReset/clone`
- Sandbox control commit: `9704ee4fcf87e14b1084cbf0c42fd39453587056` (retained on sandbox branch `master`).
- Frozen starting commit: `24603186b555dddb88ebd607e415e27bdea747b4`; the clone started exactly there, and the ancestry check exited 0.
- Axes: contract fidelity outside the assigned omissions; counter discrimination; sandbox containment; reproducible evidence and exact restoration.
- Expected detector: the frozen counter should report `C1=unmet` for the omitted reset and bad-line decisions.
- Control written from the contract, not copied from the counter. It preserves class precedence, device union, non-error states, valid rates, host aggregation, and offline/live interfaces. Lower counters become `ok` with a modulo-2**64 delta. Lines never become `bad-line`: every line with at least ten tokens supplies token ten without token-count or unsigned-token validation; a non-integer token ten becomes zero. Shorter named lines still contribute their name but no counter value.
- No tool installations or updates. No lane/fleet git writes. The report is the only file created in the lane; all implementation and git mutations were confined to the sandbox.

## Full control source

Committed path: `tools/mori-disk-rate.py`; SHA-256 `11a9c8191bbfe8a01e8957513d8e7fa37b7cac06e6c617c7ee7ab6d4b444e8ea`.

```python
#!/usr/bin/env python3
"""Two-sample disk rates with permissive lines and unsigned counter wrapping."""

import argparse
import json
import os
from pathlib import Path
import time


def read_sample(text):
    names = set()
    counts = {}
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 3:
            continue
        name = fields[2]
        names.add(name)
        counts.pop(name, None)
        if len(fields) >= 10:
            try:
                counts[name] = int(fields[9], 10)
            except ValueError:
                counts[name] = 0
    return names, counts


def device_class(block, name):
    entry = block / name
    if not entry.is_dir():
        return "unknown"
    if os.path.lexists(entry / "partition"):
        return "partition"
    slaves = entry / "slaves"
    if slaves.is_dir() and any(slaves.iterdir()):
        return "stacked"
    if os.path.lexists(entry / "device"):
        return "disk"
    return "virtual"


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
        sample = Path("/proc/diskstats")
        text_a = sample.read_text()
        time.sleep(args.interval_ms / 1000)
        text_b = sample.read_text()
    else:
        text_a = args.a.read_text()
        text_b = args.b.read_text()

    names_a, counts_a = read_sample(text_a)
    names_b, counts_b = read_sample(text_b)
    names = names_a | names_b
    block = args.sysfs / "class" / "block"
    if block.is_dir():
        names.update(entry.name for entry in block.iterdir())
    devices = {}
    for name in sorted(names):
        rate = None
        if name not in counts_a and name not in counts_b:
            state = "absent"
        elif name not in counts_b:
            state = "gone"
        elif name not in counts_a:
            state = "new"
        else:
            state = "ok"
            delta = counts_b[name] - counts_a[name]
            if delta < 0:
                delta %= 2**64
            rate = delta * 512 * 1000 // args.interval_ms
        devices[name] = {
            "class": device_class(block, name),
            "state": state,
            "write_Bps": rate,
        }
    basis = sorted(name for name in devices if devices[name]["class"] == "disk")
    total = None
    if basis and all(devices[name]["state"] == "ok" for name in basis):
        total = sum(devices[name]["write_Bps"] for name in basis)
    print(json.dumps({
        "interval_ms": args.interval_ms,
        "devices": devices,
        "host_basis": basis,
        "host_write_Bps": total,
    }))


if __name__ == "__main__":
    main()
```

## Bounded detector

All four invocations used this same command. `HEAD` referred to the pristine, control, control, and restored commits respectively. The two control invocations ran independently in parallel with distinct fresh seeds; the checkout stayed at the control commit until both exited.

```sh
timeout 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlNoReset/clone
```

### Pristine baseline — full output

```text
measured_at=2026-10-23T04:55:24Z repo=/fast/scratch/hyaku/mori-r34/CtlNoReset/clone rev=24603186b555dddb88ebd607e415e27bdea747b4
tool=absent C1=unmet
```

Exit code: `1`.

### Control run 1 — full output

```text
measured_at=2026-10-23T04:55:43Z repo=/fast/scratch/hyaku/mori-r34/CtlNoReset/clone rev=9704ee4fcf87e14b1084cbf0c42fd39453587056
tool=present guard=clean seed=13180992841630711749
fixed_pass=5/12 random_pass=90/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
```

Exit code: `1`.

### Control run 2 — full output

```text
measured_at=2026-10-23T04:55:43Z repo=/fast/scratch/hyaku/mori-r34/CtlNoReset/clone rev=9704ee4fcf87e14b1084cbf0c42fd39453587056
tool=present guard=clean seed=16662420109135030272
fixed_pass=5/12 random_pass=96/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=ok
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
```

Exit code: `1`.

### Restored baseline — full output

After both control runs exited, `git switch --detach 24603186b555dddb88ebd607e415e27bdea747b4` restored the original sandbox checkout, including the original absence of the tool. The control commit remains reachable through sandbox `master`.

```text
measured_at=2026-10-23T04:56:07Z repo=/fast/scratch/hyaku/mori-r34/CtlNoReset/clone rev=24603186b555dddb88ebd607e415e27bdea747b4
tool=absent C1=unmet
```

Exit code: `1`.

## Verdict and restoration evidence

The counter rejected this control twice through behavioral mismatches, not source-guard rejection or execution failure. Both live checks passed. The `states_seen` and `classes_seen` fields describe the counter's oracle coverage, not decisions emitted by the control.

Mutation-test classification: **inconclusive as a kill experiment**, because the pristine baseline already fails (`tool=absent`); not claimed as a killed mutant. As the assigned pre-data negative control, its observed result is `C1=unmet` in both fresh-seed runs.

| Bytes/reference | Before | Control | Restored |
|---|---|---|---|
| Sandbox HEAD | `24603186b555dddb88ebd607e415e27bdea747b4` | `9704ee4fcf87e14b1084cbf0c42fd39453587056` | `24603186b555dddb88ebd607e415e27bdea747b4` |
| Sandbox tree hash | `e644789b40f892b434f10eb731b5c919e0a1355a` | `94078224491de92cdd7548f9cedffbc52ce2f852` | `e644789b40f892b434f10eb731b5c919e0a1355a` |
| Tool bytes | absent | SHA-256 `11a9c8191bbfe8a01e8957513d8e7fa37b7cac06e6c617c7ee7ab6d4b444e8ea` | absent |

The original and restored tree hashes match exactly. Frozen lane inputs also have identical SHA-256 values before and after the probe:

```text
contract.md  f6c092fdca22a2041fa82f1c269e8805fbda3870572f5397300c6795dc61da9b
count-c1.py  0f0dd6d9114fa77d562a8ec1ddb811b4cd0eb3d32c71ea7551a37dd67826202e
```

All detector commands completed and exited; no probe service was started or left running.

control CtlNoReset: C1=unmet
