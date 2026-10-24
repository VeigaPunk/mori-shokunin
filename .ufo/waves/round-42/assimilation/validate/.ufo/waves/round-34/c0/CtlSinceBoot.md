measured 2026-10-23T05:02:18Z

# CtlSinceBoot — wrong-surface control (since-boot census average)

**Shape under test:** the contract's controls table row "wrong surface | C-sinceboot: rates from
sectors / uptime (the existing census average) | unmet".

**Sandbox:** `/fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone`
**Sandbox commit:** `b0d5c4633eaaca99314519864fa88156e8b6c37a` (parent `24603186b555dddb88ebd607e415e27bdea747b4`, the frozen lane tip)
**Base check:** `git -C <clone> rev-parse HEAD` = `24603186b555dddb88ebd607e415e27bdea747b4` before the control commit — the clone was made from the frozen lane tip and the control commit is a direct child of it.

## What the control does

It is the *claimed* operation's shape with the rate taken from the wrong surface: instead of the
two-sample delta `(B − A) * 512 * 1000 // interval_ms`, every device that has a usable line in
sample B gets the census's since-boot average `B10 * 512 // uptime_seconds` read from `/proc/uptime`
(the same arithmetic as `tools/mori-census.sh` `io_of`, line 1893: `printf '%sBps' "$((sectors * 512 / up_s))"`).

Everything else is implemented to the contract: R1/R2 parsing (device = 3rd token, valid only with
14/18/20 tokens and all tokens except the name an unsigned decimal, sectors written = token 10),
R3 class from `<sysfs>/class/block/<name>` in the contract's order (`partition` → `stacked` →
`disk` → `virtual`), R4 device set = A ∪ B ∪ `class/block` entries, R5 state precedence
(`bad-line` > `absent` > `gone` > `new` > `reset` > `ok`), R7 host total over the sorted `disk` basis.

The control never names the lane's `.ufo` tree and never names the counter (`guard=clean` on every run).

## Control source (`tools/mori-disk-rate.py` at `b0d5c46`, verbatim)

```python
#!/usr/bin/env python3
"""mori disk write-rate: per-device write rates from two diskstats samples.

This is the lane's *since-boot* rate surface, the one the census already
reports (tools/mori-census.sh, io_of): the device's sectors-written counter
times 512 bytes per sector, divided by the host uptime in seconds.  The
device classes and the per-device states follow the disk-rate rules; only the
rate numerator/divisor come from the since-boot surface.

usage:
  mori-disk-rate.py --a FILE --b FILE [--sysfs DIR] --interval-ms N
  mori-disk-rate.py [--sysfs DIR] --interval-ms N

Reads /proc/diskstats and sysfs; writes nothing but stdout JSON.
"""
import argparse
import json
import os
import re
import sys
import time

DIGITS = re.compile(r"[0-9]+")
UPTIME = "/proc/uptime"
DISKSTATS = "/proc/diskstats"


def parse(text):
    """Map device name -> (line_ok, sectors_written).

    A line names a device by its 3rd whitespace token; lines with fewer than 3
    tokens are ignored.  A line is valid only with 14, 18 or 20 tokens and
    every token except the name an unsigned decimal; sectors written is
    token 10.
    """
    out = {}
    for line in text.splitlines():
        tok = line.split()
        if len(tok) < 3:
            continue
        name = tok[2]
        good = len(tok) in (14, 18, 20) and all(DIGITS.fullmatch(t) for t in tok[:2] + tok[3:])
        out[name] = (good, int(tok[9]) if good else None)
    return out


def classify(sysfs, name):
    """Class from <sysfs>/class/block/<name>."""
    base = os.path.join(sysfs, "class", "block", name)
    if not os.path.isdir(base):
        return "unknown"
    if os.path.lexists(os.path.join(base, "partition")):
        return "partition"
    slaves = os.path.join(base, "slaves")
    if os.path.isdir(slaves) and os.listdir(slaves):
        return "stacked"
    if os.path.lexists(os.path.join(base, "device")):
        return "disk"
    return "virtual"


def uptime_seconds():
    """Host uptime in whole seconds, as the census reads it."""
    try:
        with open(UPTIME) as fh:
            raw = fh.read().split()[0]
    except (OSError, IndexError):
        return None
    raw = raw.split(".")[0]
    if not raw.isdigit():
        return None
    up = int(raw)
    return up if up > 0 else None


def since_boot_rate(sectors):
    """The census surface: sectors written since boot * 512 / uptime."""
    up = uptime_seconds()
    if up is None:
        return None
    return (sectors * 512) // up


def build(text_a, text_b, sysfs, interval_ms):
    a = parse(text_a)
    b = parse(text_b)
    names = set(a) | set(b)
    class_root = os.path.join(sysfs, "class", "block")
    if os.path.isdir(class_root):
        names |= set(os.listdir(class_root))
    devices = {}
    for name in sorted(names):
        cls = classify(sysfs, name)
        ra = a.get(name)
        rb = b.get(name)
        rate = None
        if (ra is not None and not ra[0]) or (rb is not None and not rb[0]):
            state = "bad-line"
        elif ra is None and rb is None:
            state = "absent"
        elif rb is None:
            state = "gone"
        elif ra is None:
            state = "new"
        elif rb[1] < ra[1]:
            state = "reset"
        else:
            state = "ok"
        # the census surface: every device that has a usable line in sample B
        # gets a since-boot average rate, whatever its state.
        if rb is not None and rb[0] and rb[1] is not None:
            rate = since_boot_rate(rb[1])
        devices[name] = {"class": cls, "state": state, "write_Bps": rate}
    basis = sorted(n for n in devices if devices[n]["class"] == "disk")
    host = None
    if basis and all(devices[n]["state"] == "ok" for n in basis):
        host = sum(devices[n]["write_Bps"] for n in basis)
    return {
        "interval_ms": interval_ms,
        "devices": devices,
        "host_basis": basis,
        "host_write_Bps": host,
    }


def main(argv):
    ap = argparse.ArgumentParser(description="per-device disk write rates")
    ap.add_argument("--a", help="first diskstats sample")
    ap.add_argument("--b", help="second diskstats sample")
    ap.add_argument("--sysfs", default="/sys")
    ap.add_argument("--interval-ms", type=int, default=1000)
    args = ap.parse_args(argv)
    if args.a and args.b:
        with open(args.a) as fh:
            text_a = fh.read()
        with open(args.b) as fh:
            text_b = fh.read()
    else:
        with open(DISKSTATS) as fh:
            text_a = fh.read()
        time.sleep(max(args.interval_ms, 0) / 1000.0)
        with open(DISKSTATS) as fh:
            text_b = fh.read()
    json.dump(build(text_a, text_b, args.sysfs, args.interval_ms), sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Counter output — run 1 (fresh random seed)

```
$ timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone
measured_at=2026-10-23T05:01:34Z repo=/fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone rev=b0d5c4633eaaca99314519864fa88156e8b6c37a
tool=present guard=clean seed=4950270554719520321
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-bound:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

exit code **1** (`C1=unmet`).

## Counter output — run 2 (independent fresh random seed)

```
$ timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone
measured_at=2026-10-23T05:02:02Z repo=/fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone rev=b0d5c4633eaaca99314519864fa88156e8b6c37a
tool=present guard=clean seed=12737764085934359238
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-bound:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

exit code **1** (`C1=unmet`).

## Additional scoring (Amendment A1 counter, `count-c1-a1.py`, for information only)

```
measured_at=2026-10-23T05:03:15Z repo=/fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone rev=b0d5c4633eaaca99314519864fa88156e8b6c37a
tool=present guard=clean seed=17636625866752238245
fixed_pass=0/12 random_pass=1/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-bound:dm-0
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
EXIT=1
```

## Verdict

control CtlSinceBoot: C1=unmet

The contract's expectation for this row ("wrong surface | C-sinceboot | unmet") holds. The counter
rejects the since-boot census average on two independent arms: the offline scenario comparison
(`fixed_pass=0/12`, `random_pass=0/300`) and the live bound (`live=live-bound:dm-0`).

## Attribution — the rejection is caused by the rate surface alone

A second, diagnostic variant was scored to remove any doubt that the rejection comes from the
*surface* rather than from some incidental defect of this control.

**Variant B** (`6178b765321b5922e83e71e93ab597395a3ab3cd`, kept in the sandbox under tag
`diag-variantB-r6nulls`) keeps R6 exactly — `write_Bps` is null for every non-`ok` state — and
changes **only** the numerator/divisor of the `ok` rate to the since-boot average. Under that
variant:

```
fixed_pass=0/12 random_pass=7/300
live=live-bound:dm-0
C1=unmet
```

A per-field diff against the oracle (variant B, fixed seeds 1–12) shows the **only** differing
fields are `write_Bps` and (as a consequence) `host_write_Bps`:

```
seed  1: ndiff= 8 kinds=['write_Bps']
seed  2: ndiff= 2 kinds=['write_Bps']
seed  3: ndiff= 6 kinds=['write_Bps']
seed  4: ndiff= 8 kinds=['host_write_Bps', 'write_Bps']
seed  5: ndiff= 5 kinds=['write_Bps']
seed  6: ndiff= 4 kinds=['host_write_Bps', 'write_Bps']
seed  7: ndiff= 4 kinds=['host_write_Bps', 'write_Bps']
seed  8: ndiff= 3 kinds=['write_Bps']
seed  9: ndiff=11 kinds=['host_write_Bps', 'write_Bps']
seed 10: ndiff= 8 kinds=['host_write_Bps', 'write_Bps']
seed 11: ndiff= 8 kinds=['write_Bps']
seed 12: ndiff= 9 kinds=['host_write_Bps', 'write_Bps']
distinct diff kinds across fixed seeds: ['host_write_Bps', 'write_Bps']
```

No `class`, `state`, `interval_ms` or `host_basis` mismatch occurs anywhere: the control's R3/R4/R5
machinery is exactly right, and the *only* thing wrong with it is where the rate comes from. Over the
70 `ok` devices across the 12 fixed seeds, **0** of the control's rates equal the oracle's.

## Surprise worth recording: a since-boot tool can coincide with the oracle on some scenarios

The scenario generator can produce a scenario in which **no device is in state `ok`**. In such a
scenario the oracle's rates are all null and the since-boot control's rates are all null too, so the
two agree by accident. Measured with the counter's own generator and oracle (read-only import of
`count-c1.py` from its path; the diagnostic scripts lived in `/tmp` only and were never committed
into the sandbox clone, and the committed control has no dependency on the counter):

```
A_spec_literal: base=13448842937476400456 pass=1/300 fail=299   (the 1 pass has no 'ok' device)
B_r6nulls:      base=13448842937476400456 pass=5/300 fail=295   (all 5 passes have no 'ok' device)
```

So a since-boot tool is not *always* distinguishable from the oracle on a single scenario; it is
distinguishable whenever at least one device is `ok`. This does not weaken the control's verdict
here — the fixed seeds always contain `ok` devices (2 to 10 per seed, measured), so `fixed_pass=0/12`
is stable across every seed tried — but it is a real property of the counter that the fixed seed set,
not the 300 drawn scenarios, is what guarantees the wrong surface is always caught. If the fixed
seed set were ever regenerated from a generator that could produce all-`ok`-less scenarios, the
counter's discrimination of this row would rest on the drawn set alone (a ~1.7%–3.3% per-scenario
false-pass rate would then need to be beaten by 300 draws, which it is not, but the margin would be
thinner than the fixed set provides today).

## Containment

- No git or jj write command was run in `/home/vgpnk/Projects/shokunin/mori-shokunin` or in
  `/home/vgpnk/Projects/shokunin`. The only sandbox git writes are in
  `/fast/scratch/hyaku/mori-r34/CtlSinceBoot/clone`.
- The frozen counter and contract were read only, never edited. `count-c1.py` is byte-identical to
  what the contract froze (the lane's `count-c1-a1.py` appeared mid-seat and is reported above
  separately; it was not authored or modified here).
- This report file is the only file created inside the lane repo.
- All counter invocations were wrapped in `timeout 600`. Diagnostic scripts were run from `/tmp`
  and were deleted after use; no long-lived process was started.

## Tooling

No tool was installed or updated for this seat (nothing was needed beyond the pre-existing
`python3` and `git`; the counter, the sandbox clone and the diagnostics all ran with them). No
`pacman`, `uv`, `cargo` or `npm` transaction was performed, so there is nothing to record under the
operator's tooling directive.
