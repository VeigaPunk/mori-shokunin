measured 2026-10-23T04:56:50Z

# Control CtlAllNull (content-free shape) — round 34 wave C0

- Sandbox path: `/fast/scratch/hyaku/mori-r34/CtlAllNull/clone`
- Sandbox commit: `0d60f56d8b3083af786c6fc38823ff431221da3b` (parent `24603186b555dddb88ebd607e415e27bdea747b4`, the frozen lane tip — descendant check OK)
- Base tip check: `git -C <clone> rev-parse HEAD` before the commit = `24603186b555dddb88ebd607e415e27bdea747b4` ✓
- Tool install / update record: none. No package installed (no pacman, no uv, no new binary); the control uses only the Python 3 standard library already present. Nothing to record.

## Control source (`<clone>/tools/mori-disk-rate.py`)

```python
#!/usr/bin/env python3
"""mori-disk-rate.py -- control C-allnull (content-free shape).

This is a PRE-DATA CONTROL built to attack the round-34 C1 counter. It deliberately does NOT
compute write rates: it lists every device name it can find in both samples and in
<sysfs>/class/block, gives every device class `disk`, state `ok`, write_Bps null, sets
host_basis to all names sorted and host_write_Bps to null, and echoes interval_ms.

It is not the claimed operation: no sectors are read, no rate is computed, no state is decided.
"""
import argparse
import json
import os
import sys
import time


def names_in(text):
    """Every device name the sample mentions (3rd whitespace token of any line with >= 3 tokens)."""
    out = set()
    for line in text.splitlines():
        tok = line.split()
        if len(tok) >= 3:
            out.add(tok[2])
    return out


def sysfs_names(sysfs):
    base = os.path.join(sysfs, "class", "block")
    try:
        return set(os.listdir(base))
    except OSError:
        return set()


def read_sample(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--a")
    ap.add_argument("--b")
    ap.add_argument("--sysfs", default="/sys")
    ap.add_argument("--interval-ms", type=int, default=1000)
    args = ap.parse_args(argv)

    sysfs = args.sysfs
    if args.a and args.b:
        text_a = read_sample(args.a)
        text_b = read_sample(args.b)
    else:
        text_a = read_sample("/proc/diskstats")
        time.sleep(max(0, args.interval_ms) / 1000.0)
        text_b = read_sample("/proc/diskstats")

    names = names_in(text_a) | names_in(text_b) | sysfs_names(sysfs)

    devices = {}
    for n in sorted(names):
        devices[n] = {"class": "disk", "state": "ok", "write_Bps": None}

    result = {
        "interval_ms": args.interval_ms,
        "devices": devices,
        "host_basis": sorted(names),
        "host_write_Bps": None,
    }
    json.dump(result, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Counter run 1 (fresh random seed)

```
$ timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlAllNull/clone
measured_at=2026-10-23T04:55:43Z repo=/fast/scratch/hyaku/mori-r34/CtlAllNull/clone rev=0d60f56d8b3083af786c6fc38823ff431221da3b
tool=present guard=clean seed=4439370180801026664
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

## Counter run 2 (fresh random seed, second run)

```
$ timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlAllNull/clone
measured_at=2026-10-23T04:55:59Z repo=/fast/scratch/hyaku/mori-r34/CtlAllNull/clone rev=0d60f56d8b3083af786c6fc38823ff431221da3b
tool=present guard=clean seed=356766306691344153
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

## Reading

The counter behaved as the contract's controls table expects for the content-free shape: the tool is present, the
`.ufo`/`count-c1` guard is clean, the tool exits 0 and emits well-formed JSON with the required key set, and every
scenario mismatches the oracle (`fixed_pass=0/12`, `random_pass=0/300`). The live arm independently rejects it with
`live-class:dm-0` — the control assigns class `disk` to every device, so it cannot agree with the oracle's
`classify()` on any non-disk device (and `host_basis` is every name, not only disk-class names).

Note that the oracle's own coverage bookkeeping (`states_seen`, `classes_seen`, `coverage=ok`) reports the *oracle's*
states/classes, not the control's — the counter's coverage term is satisfied even when the tool never produces those
states. That term is therefore not what rejects this control; the exact-match comparison is.

## Verdict

control CtlAllNull: C1=unmet
