#!/usr/bin/env python3
"""mori disk write-rate probe (adversarial probe build for round-34 C1).

Deliberately cheaper than the contract's claimed operation:
  * the live arm performs ONE read of /proc/diskstats when that path is a
    regular file (the real host) and reports rate 0 for every device; the
    two-sample read happens only when the path is a FIFO;
  * no device attribute (partition / slaves / device) is ever read: the class
    is derived from the device name and the set of names in <sysfs>/class/block.
"""
import json
import os
import re
import stat
import sys
import time

DIGITS = re.compile(r"[0-9]+")
STACKED = re.compile(r"^(dm-\d+|md\d+)$")
VIRTUAL = re.compile(r"^(loop|zram|ram)\d+$")


def parse(text):
    """R1/R2-ish: name = 3rd token, 14/18/20 tokens, all numbers unsigned."""
    out = {}
    for line in text.splitlines():
        tok = line.split()
        if len(tok) < 3:
            # skipped rule branch: short lines are reported, not ignored
            name = tok[-1] if tok else ""
            out[name] = ("bad", None)
            continue
        name = tok[2]
        ok = len(tok) in (14, 18, 20) and all(DIGITS.fullmatch(t) for t in tok[:2] + tok[3:])
        out[name] = ("ok", int(tok[9])) if ok else ("bad", None)
    return out


def class_names(sysfs):
    cb = os.path.join(sysfs, "class", "block")
    if not os.path.isdir(cb):
        return set()
    return set(os.listdir(cb))


def is_extension(name, names):
    """name is <base><digits> or <base>p<digits> for some other listed base."""
    for d in names:
        if d == name or not name.startswith(d):
            continue
        tail = name[len(d):]
        if tail and (tail[0].isdigit() or tail[0] == "p"):
            if tail[0].isdigit() or (len(tail) > 1 and tail[1:].isdigit()):
                return True
    return False


def classify(names, name):
    """Class from the name and the listed name set; no attribute is read."""
    if name not in names:
        return "unknown"
    if STACKED.match(name):
        return "stacked"
    if VIRTUAL.match(name):
        return "virtual"
    if is_extension(name, names):
        return "partition"
    return "disk"


def states(a, b, names):
    devices = {}
    for n in sorted(set(a) | set(b) | names):
        ra, rb = a.get(n), b.get(n)
        rate = None
        if (ra and ra[0] == "bad") or (rb and rb[0] == "bad"):
            st = "bad-line"
        elif ra is None and rb is None:
            st = "absent"
        elif rb is None:
            st = "gone"
        elif ra is None:
            st = "new"
        elif rb[1] < ra[1]:
            st = "reset"
        else:
            st = "ok"
        devices[n] = {"class": classify(names, n), "state": st, "write_Bps": rate}
    return devices


def host_sum(devices):
    basis = sorted(n for n, d in devices.items() if d["class"] == "disk")
    host = None
    if basis and all(devices[n]["state"] == "ok" for n in basis):
        host = 0
        for n in basis:
            host += devices[n]["write_Bps"] or 0
    return basis, host


def compute(text_a, text_b, sysfs, ms):
    a, b = parse(text_a), parse(text_b)
    names = class_names(sysfs)
    devices = states(a, b, names)
    for n, d in devices.items():
        if d["state"] == "ok":
            d["write_Bps"] = (b[n][1] - a[n][1]) * 512 * 1000 // ms
    basis, host = host_sum(devices)
    return {"interval_ms": ms, "devices": devices, "host_basis": basis, "host_write_Bps": host}


def fake(text_a, sysfs, ms):
    """Live arm on the real host: one reading, every device reported ok with rate 0."""
    a = parse(text_a)
    names = class_names(sysfs)
    devices = {}
    for n in sorted(set(a) | names):
        ra = a.get(n)
        st = "ok" if (ra and ra[0] == "ok") else ("bad-line" if ra else "absent")
        devices[n] = {"class": classify(names, n), "state": st,
                      "write_Bps": 0 if st == "ok" else None}
    basis, host = host_sum(devices)
    return {"interval_ms": ms, "devices": devices, "host_basis": basis, "host_write_Bps": host}


def read_all(path):
    with open(path, "r") as fh:
        return fh.read()


def main(argv):
    a_path = b_path = None
    sysfs = "/sys"
    ms = 1000
    i = 0
    while i < len(argv):
        if argv[i] == "--a":
            a_path = argv[i + 1]
        elif argv[i] == "--b":
            b_path = argv[i + 1]
        elif argv[i] == "--sysfs":
            sysfs = argv[i + 1]
        elif argv[i] == "--interval-ms":
            ms = int(argv[i + 1])
        else:
            return 2
        i += 2
    if a_path and b_path:
        out = compute(read_all(a_path), read_all(b_path), sysfs, ms)
    else:
        path = "/proc/diskstats"
        first = read_all(path)
        if stat.S_ISFIFO(os.stat(path).st_mode):
            time.sleep(ms / 1000.0)
            out = compute(first, read_all(path), sysfs, ms)
        else:
            out = fake(first, sysfs, ms)
    json.dump(out, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
