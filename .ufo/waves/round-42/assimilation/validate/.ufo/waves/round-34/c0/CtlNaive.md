measured 2026-10-23T04:57:38Z

# Control C-naive — mori r34 wave C0 (no-decision shape)

Item: CtlNaive — "does the arithmetic, skips every decision": for each name present in both samples
compute `(B10-A10)*512*1000//interval_ms` with token 10, no line validation, no reset/gone/new/absent
handling (a missing side counts as 0), every class `disk`, `host_basis` = all names,
`host_write_Bps` = sum of all rates.

## Sandbox

- Sandbox path: `/fast/scratch/hyaku/mori-r34/CtlNaive/clone`
- Sandbox commit: `797ccf81942ad65fe0f57cc6fe171dfea8c52e78` (parent `24603186b555dddb88ebd607e415e27bdea747b4`,
  the frozen lane tip; verified `git -C <clone> rev-parse HEAD` = `24603186b555dddb88ebd607e415e27bdea747b4`
  before the control commit, so the clone is at-or-descendant of the frozen tip).
- Commit made in the clone only: `git -c user.name=ctl -c user.email=ctl@sandbox commit`. No git/jj write
  command was run in `/home/vgpnk/Projects/shokunin/mori-shokunin` or in `/home/vgpnk/Projects/shokunin`.
- Tool installs: none. No `pacman`, `uv tool`, `cargo`, or `npm` transaction was performed; the control uses
  only the stdlib, and the frozen counter needs only `python3`. Nothing to record beyond "no installs".

## Control source (`<clone>/tools/mori-disk-rate.py`)

```python
#!/usr/bin/env python3
"""Control C-naive: the no-decision shape.

Does the arithmetic and skips every decision:
  * one rate per device name taken from the two samples,
  * no line validation (no token-count or decimal checks),
  * no reset / gone / new / absent handling (a missing side counts as 0),
  * every device is reported with class "disk",
  * host_basis is every name seen and host_write_Bps is the sum of all rates.
"""
import argparse
import json
import sys
import time


def read_sample(path):
    """Name = 3rd whitespace token; sectors written = token 10. No validation."""
    out = {}
    try:
        with open(path, "r", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return out
    for line in text.splitlines():
        tok = line.split()
        if len(tok) < 3:
            continue
        name = tok[2]
        sectors = 0
        if len(tok) > 9:
            try:
                sectors = int(tok[9])
            except ValueError:
                sectors = 0
        out[name] = sectors
    return out


def rates(a, b, interval_ms):
    names = sorted(set(a) | set(b))
    devices = {}
    total = 0
    for n in names:
        b10 = b.get(n, 0)
        a10 = a.get(n, 0)
        r = (b10 - a10) * 512 * 1000 // interval_ms
        devices[n] = {"class": "disk", "state": "ok", "write_Bps": r}
        total += r
    return devices, names, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a")
    ap.add_argument("--b")
    ap.add_argument("--sysfs", default="/sys")
    ap.add_argument("--interval-ms", type=int, required=True)
    args = ap.parse_args()
    ms = args.interval_ms
    if args.a and args.b:
        a = read_sample(args.a)
        b = read_sample(args.b)
    else:
        a = read_sample("/proc/diskstats")
        time.sleep(ms / 1000.0)
        b = read_sample("/proc/diskstats")
    devices, names, total = rates(a, b, ms)
    json.dump({"interval_ms": ms, "devices": devices, "host_basis": names,
               "host_write_Bps": total}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Note: the control takes `--sysfs` but ignores it — class is hardcoded `disk` for every device, which is the
intended no-decision shape.

## Counter run 1 (fresh random seed)

```
$ cd /tmp && timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlNaive/clone
measured_at=2026-10-23T04:57:05Z repo=/fast/scratch/hyaku/mori-r34/CtlNaive/clone rev=797ccf81942ad65fe0f57cc6fe171dfea8c52e78
tool=present guard=clean seed=12286540221639901928
fixed_pass=0/12 random_pass=1/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

## Counter run 2 (fresh random seed)

```
$ cd /tmp && timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlNaive/clone
measured_at=2026-10-23T04:57:18Z repo=/fast/scratch/hyaku/mori-r34/CtlNaive/clone rev=797ccf81942ad65fe0f57cc6fe171dfea8c52e78
tool=present guard=clean seed=4718205726109844957
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-class:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

## Verdict

control CtlNaive: C1=unmet

The counter rejects the no-decision shape: 0/12 fixed-seed scenarios pass, 0–1/300 random scenarios pass
(the single random pass in run 1 is a scenario whose devices all happened to be class `disk` with `ok`
state and no reset/gone/new/absent/bad-line divergence). The live arm independently rejects it at
`live-class:dm-0` — the counter's own `classify("/sys", "dm-0")` is `stacked`, the control reports `disk`.
Guard is `clean` (the control names neither `.ufo` nor `count-c1`), so the rejection is behavioural, not a
pathological-artifact guard trip. No processes were left running.

Counter-observation (informational, not a change to the counter): the contract's control table row for this
shape ("C-naive: one rate per line, every class disk, no state handling, host = sum of all lines") is
faithfully implemented here. `host_basis` in the control is *all* names rather than the disk-class subset
the oracle uses — the `host_basis` mismatch alone would fail the comparison, but the per-device
`class`/`state`/`write_Bps` fields already fail independently, so the verdict does not hinge on that
difference.
