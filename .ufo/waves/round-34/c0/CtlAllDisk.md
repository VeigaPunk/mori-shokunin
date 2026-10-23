measured 2026-10-23T04:57:09Z

# CtlAllDisk — partial no-decision control

- Sandbox: `/fast/scratch/hyaku/mori-r34/CtlAllDisk/clone`.
- Control commit: `4fee7ce4c1093df927642df7661630b5ff63345f`.
- Pristine commit: `24603186b555dddb88ebd607e415e27bdea747b4` (clone HEAD exactly matched the required freeze; ancestry check exited 0).
- Restored sandbox HEAD: `c19c0ab2d3797028b27234a174db6b5b4642e2f4`. The control remains available at its recorded commit; the final tree is restored to pristine.
- Axes: fidelity to R1/R2/R4/R5/R6; discrimination against omitted R3; exact-byte restoration and containment.
- Mutation: assign every device `class: disk`, omitting R3 entirely. Compute R7 from those classes, including every device in the host basis. The program was written from the contract, not copied from the counter.
- Expected detector: the unchanged frozen P-C1 counter rejects scenarios containing partition, stacked, virtual or unknown devices, and rejects the live class mismatch. Disk-only scenarios can pass.
- Tool installs/updates: none. No other runtime was invoked; all command runs were bounded by `timeout`.

## Full control source

`tools/mori-disk-rate.py` at the control commit:

```python
#!/usr/bin/env python3
"""Two-sample write-rate control with every device deliberately treated as disk."""

import argparse
import json
from pathlib import Path
import time


def sample(text):
    names = set()
    sectors = {}
    bad = set()
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 3:
            continue
        name = fields[2]
        names.add(name)
        numeric = fields[:2] + fields[3:]
        if len(fields) not in (14, 18, 20) or not all(
            value.isascii() and value.isdecimal() for value in numeric
        ):
            bad.add(name)
        else:
            sectors[name] = int(fields[9])
    return names, sectors, bad


def report(text_a, text_b, sysfs, interval_ms):
    names_a, sectors_a, bad_a = sample(text_a)
    names_b, sectors_b, bad_b = sample(text_b)
    names = names_a | names_b
    block = Path(sysfs) / "class" / "block"
    if block.is_dir():
        names.update(entry.name for entry in block.iterdir())

    devices = {}
    for name in sorted(names):
        rate = None
        if name in bad_a or name in bad_b:
            state = "bad-line"
        elif name not in names_a and name not in names_b:
            state = "absent"
        elif name not in names_b:
            state = "gone"
        elif name not in names_a:
            state = "new"
        elif sectors_b[name] < sectors_a[name]:
            state = "reset"
        else:
            state = "ok"
            rate = (sectors_b[name] - sectors_a[name]) * 512 * 1000 // interval_ms
        devices[name] = {"class": "disk", "state": state, "write_Bps": rate}

    basis = sorted(devices)
    host_rate = None
    if basis and all(devices[name]["state"] == "ok" for name in basis):
        host_rate = sum(devices[name]["write_Bps"] for name in basis)
    return {
        "interval_ms": interval_ms,
        "devices": devices,
        "host_basis": basis,
        "host_write_Bps": host_rate,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a")
    parser.add_argument("--b")
    parser.add_argument("--sysfs", default="/sys")
    parser.add_argument("--interval-ms", required=True, type=int)
    args = parser.parse_args()
    if (args.a is None) != (args.b is None):
        parser.error("--a and --b must be supplied together")
    if args.a is not None:
        text_a = Path(args.a).read_text()
        text_b = Path(args.b).read_text()
    else:
        diskstats = Path("/proc/diskstats")
        text_a = diskstats.read_text()
        time.sleep(args.interval_ms / 1000)
        text_b = diskstats.read_text()
    print(json.dumps(report(text_a, text_b, args.sysfs, args.interval_ms)))


if __name__ == "__main__":
    main()
```

## Frozen counting command

The same command was run against pristine HEAD, the control HEAD twice with independent fresh seeds, and restored HEAD:

```text
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlAllDisk/clone
```

### Pristine baseline — full output

```text
measured_at=2026-10-23T04:55:06Z repo=/fast/scratch/hyaku/mori-r34/CtlAllDisk/clone rev=24603186b555dddb88ebd607e415e27bdea747b4
tool=absent C1=unmet
```

Exit code: `1`. The pre-operation baseline fails because the tool is absent; this is not a passing baseline for a killed-mutant claim.

### Control run 1 — full output

```text
measured_at=2026-10-23T04:55:53Z repo=/fast/scratch/hyaku/mori-r34/CtlAllDisk/clone rev=4fee7ce4c1093df927642df7661630b5ff63345f
tool=present guard=clean seed=10054706966862686483
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
```

Exit code: `1`. No stderr.

### Control run 2 — full output

```text
measured_at=2026-10-23T04:55:53Z repo=/fast/scratch/hyaku/mori-r34/CtlAllDisk/clone rev=4fee7ce4c1093df927642df7661630b5ff63345f
tool=present guard=clean seed=17481521059238385385
fixed_pass=0/12 random_pass=3/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
```

Exit code: `1`. No stderr.

## Which scenario classes fail

A separate bounded diagnostic regenerated each run's 12 fixed and 300 random fixtures using the unchanged frozen generator, executed the same control, and compared its output with the frozen oracle. It did not modify the counter or the control. Its process exited `0` with no stderr.

Every scenario containing any non-disk device failed: `312/312` in run 1 and `309/309` in run 2. Run 1 contained no disk-only scenarios; all `3/3` disk-only scenarios in run 2 passed. The per-device class mismatches were:

| Expected class | Run 1 mismatches / devices | Run 2 mismatches / devices |
|---|---:|---:|
| disk | 0 / 653 | 0 / 626 |
| partition | 974 / 974 | 921 / 921 |
| stacked | 317 / 317 | 306 / 306 |
| unknown | 100 / 100 | 93 / 93 |
| virtual | 292 / 292 | 311 / 311 |

Device sets, intervals, states and per-device rates matched throughout both diagnostics. Host bases differed in `312` and `309` scenarios respectively; host rates differed in `144` and `139`. Thus the observed offline failures isolate the omitted class decision and its R7 consequence, rather than faulty state/rate handling. Both live probes were rejected at `live-class:dm-0`.

Full diagnostic stdout:

```text
{"class_comparisons": {"disk": {"class_mismatches": 0, "devices": 653}, "partition": {"class_mismatches": 974, "devices": 974}, "stacked": {"class_mismatches": 317, "devices": 317}, "unknown": {"class_mismatches": 100, "devices": 100}, "virtual": {"class_mismatches": 292, "devices": 292}}, "disk_only_passed": 0, "disk_only_scenarios": 0, "host_basis_mismatches": 312, "host_rate_mismatches": 144, "nondisk_failed": 312, "nondisk_scenarios": 312, "offline_pass": "0/312", "seed": 10054706966862686483, "shape_mismatches": 0, "state_rate_mismatches": 0}
{"class_comparisons": {"disk": {"class_mismatches": 0, "devices": 626}, "partition": {"class_mismatches": 921, "devices": 921}, "stacked": {"class_mismatches": 306, "devices": 306}, "unknown": {"class_mismatches": 93, "devices": 93}, "virtual": {"class_mismatches": 311, "devices": 311}}, "disk_only_passed": 3, "disk_only_scenarios": 3, "host_basis_mismatches": 309, "host_rate_mismatches": 139, "nondisk_failed": 309, "nondisk_scenarios": 309, "offline_pass": "3/312", "seed": 17481521059238385385, "shape_mismatches": 0, "state_rate_mismatches": 0}
```

## Restoration and before/after hashes

The added control file was removed and that removal committed only inside the sandbox. Pristine and restored Git tree hashes are identical, including file bytes and modes:

```text
pristine HEAD:       24603186b555dddb88ebd607e415e27bdea747b4
pristine tree:       e644789b40f892b434f10eb731b5c919e0a1355a
control HEAD:        4fee7ce4c1093df927642df7661630b5ff63345f
control source SHA256: 3e112fd17c2a378f79ddbdb89e4908093bb64b3573c893eac9375e539ae17914
restored HEAD:       c19c0ab2d3797028b27234a174db6b5b4642e2f4
restored tree:       e644789b40f892b434f10eb731b5c919e0a1355a
tools/mori-disk-rate.py: ABSENT -> recorded control bytes -> ABSENT
```

The frozen inputs had the same SHA256 before and after all scoring:

```text
contract.md  f6c092fdca22a2041fa82f1c269e8805fbda3870572f5397300c6795dc61da9b
count-c1.py 0f0dd6d9114fa77d562a8ec1ddb811b4cd0eb3d32c71ea7551a37dd67826202e
```

### Restored baseline — full output

```text
measured_at=2026-10-23T04:57:09Z repo=/fast/scratch/hyaku/mori-r34/CtlAllDisk/clone rev=c19c0ab2d3797028b27234a174db6b5b4642e2f4
tool=absent C1=unmet
```

Exit code: `1`. Restoration reproduces the pristine baseline's absent-tool result. All started command processes have exited; no service or background process was started. The only file created in the lane repo by this assignment is this receipt; all Git writes were confined to the sandbox clone.

## Verdict

The frozen counter rejected this partial no-decision control on both fresh seeds. A killed-mutant verdict is **inconclusive** because the pristine absent-tool baseline already fails; the directly measured negative-control verdict is unambiguous.

control CtlAllDisk: C1=unmet
