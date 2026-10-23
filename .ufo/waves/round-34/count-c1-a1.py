#!/usr/bin/env python3
"""mori round 34 — C1 counter, Amendment A1 (adds conditions to count-c1.py; removes none).

usage: count-c1-a1.py <rev> [--repo DIR] [--seed N] [--random N]

Predicate P-C1-A1 (the same sentence as contract.md Amendment A1 and the receipt label C1=met):
  P-C1, and the tool runs with /home and /fast hidden from it and every capability dropped, and its live JSON lists every entry of
  /sys/class/block and every device whose line is valid in both of the counter's outer readings, each
  such device whose counter did not fall being reported ok with an integer rate, and in a fed live run
  (the counter serves two generated samples through /proc/diskstats, real /sys) the tool reads the file
  twice at least 0.9 * interval_ms apart and its JSON matches the oracle exactly.

Predicate P-C1 (the same sentence as contract.md and the receipt label C1=met):
  At the measured revision, tools/mori-disk-rate.py exists, never names the lane's .ufo tree or this
  counter, matches this counter's oracle exactly on the 12 fixed-seed scenarios and on every one of
  300 scenarios drawn from a fresh random seed (the drawn set must exercise all six states and all
  five classes), and its live run exits 0 with JSON whose classes match /sys and whose ok rates are
  bounded by the counter's own outer /proc/diskstats readings.

The oracle is computed in memory after the tool has run; no expected output is ever written to disk.
Exit 0 = C1=met, exit 1 = C1=unmet, exit 2 = usage error.
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time

TOOL = "tools/mori-disk-rate.py"
STATES = ("ok", "reset", "gone", "new", "absent", "bad-line")
CLASSES = ("disk", "partition", "stacked", "virtual", "unknown")
FIXED_SEEDS = list(range(1, 13))
DIGITS = re.compile(r"[0-9]+")

# ---------------------------------------------------------------- oracle (frozen rules R1-R8)

def parse(text):
    """R1: a line names a device by its 3rd whitespace token; lines with fewer than 3 tokens are
    ignored. R2: a line is valid only with 14, 18 or 20 tokens, every token except the name being
    an unsigned decimal; sectors written is token 10 (1-based)."""
    out = {}
    for line in text.splitlines():
        tok = line.split()
        if len(tok) < 3:
            continue
        name = tok[2]
        ok = len(tok) in (14, 18, 20) and all(DIGITS.fullmatch(t) for t in tok[:2] + tok[3:])
        out[name] = ("ok", int(tok[9])) if ok else ("bad", None)
    return out


def classify(sysfs, name):
    """R3: classes from <sysfs>/class/block/<name>: no such directory -> unknown; a `partition`
    entry -> partition; a non-empty `slaves` directory -> stacked; a `device` entry -> disk;
    otherwise virtual (checked in this order)."""
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


def oracle(text_a, text_b, sysfs, interval_ms):
    """R4: devices = names in A, names in B, entries of <sysfs>/class/block. R5: state precedence
    bad-line (a bad line in either sample) > absent (no line in either) > gone (A only) > new
    (B only) > reset (B sectors < A sectors) > ok. R6: ok rate = (B - A) * 512 * 1000 // interval_ms,
    every other state has write_Bps null. R7: host_basis = sorted disk-class names; host_write_Bps =
    sum of their rates when the basis is non-empty and every basis device is ok, else null."""
    a, b = parse(text_a), parse(text_b)
    names = set(a) | set(b)
    cb = os.path.join(sysfs, "class", "block")
    if os.path.isdir(cb):
        names |= set(os.listdir(cb))
    devices = {}
    for n in sorted(names):
        cls = classify(sysfs, n)
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
            rate = (rb[1] - ra[1]) * 512 * 1000 // interval_ms
        devices[n] = {"class": cls, "state": st, "write_Bps": rate}
    basis = sorted(n for n, d in devices.items() if d["class"] == "disk")
    host = None
    if basis and all(devices[n]["state"] == "ok" for n in basis):
        host = sum(devices[n]["write_Bps"] for n in basis)
    return {"interval_ms": interval_ms, "devices": devices, "host_basis": basis, "host_write_Bps": host}

# ---------------------------------------------------------------- scenario generator

DISKS = ["sda", "sdb", "sdc", "vda", "xvda", "nvme0n1", "nvme1n1", "mmcblk0"]
VIRT = ["loop0", "loop1", "zram0", "ram0"]


def part_name(d, i):
    return f"{d}p{i}" if d[-1].isdigit() else f"{d}{i}"


def fields_line(rng, name, nfields, f10):
    vals = [str(rng.randint(0, 259)), str(rng.randint(0, 2 ** 20)), name]
    for k in range(4, nfields + 1):
        vals.append(str(f10) if k == 10 else str(rng.randint(0, 2 ** 40)))
    return vals


def render(rng, vals):
    lead = " " * rng.randint(0, 4)
    return lead + "".join(v + " " * rng.randint(1, 3) for v in vals[:-1]) + vals[-1]


def corrupt(rng, vals):
    kind = rng.randint(0, 2)
    if kind == 0:  # wrong token count
        target = rng.choice([3, 5, 10, 11, 13, 15, 16, 17, 19, 21])
        while len(vals) > target:
            vals.pop()
        while len(vals) < target:
            vals.append(str(rng.randint(0, 99)))
    else:  # a non-decimal token at a non-name position (keeps the count)
        pos = rng.choice([i for i in range(len(vals)) if i != 2])
        vals[pos] = rng.choice(["-1", "x", "1.5", "0x1f", "+3", ""]) or "?"
    return vals


def scenario(seed, root):
    rng = random.Random(seed)
    nf = rng.choice([14, 18, 20])
    cls = {}
    slaves = {}
    disks = rng.sample(DISKS, rng.randint(1, 3))
    parts = []
    for d in disks:
        cls[d] = "disk"
        for i in range(1, rng.randint(0, 3) + 1):
            p = part_name(d, i)
            cls[p] = "partition"
            parts.append(p)
    for i in range(rng.randint(0, 2)):
        s = rng.choice([f"dm-{i}", f"md{127 - i}"])
        if s in cls:
            continue
        cls[s] = "stacked"
        slaves[s] = rng.sample(disks + parts, rng.randint(1, min(2, len(disks + parts))))
    for v in rng.sample(VIRT, rng.randint(0, 2)):
        cls[v] = "virtual"
    unknown = ["xyz9"] if rng.random() < 0.3 else []
    sysfs = os.path.join(root, "sys")
    for n, c in cls.items():
        base = os.path.join(sysfs, "class", "block", n)
        os.makedirs(base)
        if c != "partition":
            os.makedirs(os.path.join(base, "slaves"))
        if c == "partition":
            open(os.path.join(base, "partition"), "w").write(f"{rng.randint(1, 9)}\n")
        if c == "disk":
            open(os.path.join(base, "device"), "w").close()
        for sl in slaves.get(n, []):
            open(os.path.join(base, "slaves", sl), "w").close()
    la, lb = [], []
    for n in list(cls) + unknown:
        r = rng.random()
        a10 = rng.choice([rng.randint(0, 10 ** 6), rng.randint(0, 2 ** 40), rng.randint(2 ** 63, 2 ** 64 - 1)])
        if r < 0.10 and a10 > 0:
            b10, ina, inb = rng.randint(0, a10 - 1), True, True  # reset
        elif r < 0.17:
            b10, ina, inb = a10, True, False  # gone
        elif r < 0.24:
            b10, ina, inb = a10, False, True  # new
        elif r < 0.30 and cls.get(n) == "partition":
            continue  # absent: listed in sysfs only
        else:
            b10, ina, inb = a10 + rng.choice([0, rng.randint(1, 1000), rng.randint(1, 2 ** 32)]), True, True
        va = fields_line(rng, n, nf, a10)
        vb = fields_line(rng, n, nf, b10)
        if r > 0.92:
            if rng.random() < 0.5 and ina:
                va = corrupt(rng, va)
            elif inb:
                vb = corrupt(rng, vb)
        if ina:
            la.append(render(rng, va))
        if inb:
            lb.append(render(rng, vb))
    rng.shuffle(la)
    rng.shuffle(lb)
    ms = rng.choice([rng.randint(1, 100), rng.randint(100, 10000), 1000])
    pa, pb = os.path.join(root, "a.diskstats"), os.path.join(root, "b.diskstats")
    open(pa, "w").write("\n".join(la) + ("\n" if la else ""))
    open(pb, "w").write("\n".join(lb) + ("\n" if lb else ""))
    return pa, pb, sysfs, ms

# ---------------------------------------------------------------- runner


def run_tool(tool, args, timeout=20):
    try:
        # A1 (C-echo): the tool cannot read the lane, this counter or any sandbox clone; capabilities are
        # dropped after the mounts so namespace root cannot umount the overlay (CtlEcho v3).
        hide = "mount -t tmpfs none /home && mount -t tmpfs none /fast && exec setpriv --bounding-set=-all --inh-caps=-all --ambient-caps=-all --no-new-privs -- \"$@\""
        p = subprocess.run(["unshare", "--user", "--map-root-user", "--mount", "--", "sh", "-c", hide, "sh",
                            sys.executable, tool] + args, capture_output=True, text=True,
                           timeout=timeout, cwd=tempfile.gettempdir())
    except subprocess.TimeoutExpired:
        return None, "timeout"
    if p.returncode != 0:
        return None, f"rc={p.returncode}"
    try:
        return json.loads(p.stdout), None
    except ValueError:
        return None, "not-json"


def same(out, exp):
    if not isinstance(out, dict):
        return False
    return (out.get("interval_ms") == exp["interval_ms"] and out.get("devices") == exp["devices"]
            and out.get("host_basis") == exp["host_basis"]
            and out.get("host_write_Bps") == exp["host_write_Bps"])


def score_seeds(tool, seeds, seen):
    fails = []
    for s in seeds:
        root = tempfile.mkdtemp(prefix="mori-r34-c1-")
        try:
            pa, pb, sysfs, ms = scenario(s, root)
            out, err = run_tool(tool, ["--a", pa, "--b", pb, "--sysfs", sysfs, "--interval-ms", str(ms)])
            exp = oracle(open(pa).read(), open(pb).read(), sysfs, ms)
            for d in exp["devices"].values():
                seen["state"].add(d["state"])
                seen["class"].add(d["class"])
            if err or not same(out, exp):
                fails.append((s, err or "mismatch"))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    return fails


def live(tool):
    s0 = parse(open("/proc/diskstats").read())
    out, err = run_tool(tool, ["--interval-ms", "300"])
    s3 = parse(open("/proc/diskstats").read())
    if err:
        return f"live-{err}"
    if not isinstance(out, dict) or not isinstance(out.get("devices"), dict):
        return "live-shape"
    sysnames = set(os.listdir("/sys/class/block"))
    for n, d in out["devices"].items():
        if n not in set(s0) | set(s3) | sysnames:
            return f"live-foreign:{n}"
        if not isinstance(d, dict) or d.get("class") != classify("/sys", n):
            return f"live-class:{n}"
        if d.get("state") == "ok":
            r = d.get("write_Bps")
            if not isinstance(r, int) or r < 0 or n not in s0 or n not in s3 or s0[n][0] != "ok" or s3[n][0] != "ok":
                return f"live-rate:{n}"
            if r * 300 > (s3[n][1] - s0[n][1]) * 512 * 1000:
                return f"live-bound:{n}"
    # A1 (live hole): every sysfs block device and every device valid in both outer readings is listed;
    # one whose counter did not fall is reported ok with an integer rate (bounded above).
    both = {n for n in set(s0) & set(s3) if s0[n][0] == "ok" and s3[n][0] == "ok"}
    for n in sorted(sysnames | both):
        if n not in out["devices"]:
            return f"live-missing:{n}"
    for n in sorted(both):
        if s3[n][1] >= s0[n][1]:
            d = out["devices"][n]
            if d.get("state") != "ok" or not isinstance(d.get("write_Bps"), int) or isinstance(d.get("write_Bps"), bool):
                return f"live-notok:{n}"
    disks = sorted(n for n in out["devices"] if classify("/sys", n) == "disk")
    if out.get("host_basis") != disks or out.get("interval_ms") != 300:
        return "live-basis"
    return None


def fed_live(tool, seed):
    """A1 (C-zero / single-read): serve two generated samples over the real host's device names through
    a FIFO bound on /proc/diskstats; the tool must read twice >= 0.9 * interval apart and match the oracle."""
    import errno
    import threading
    rng = random.Random(seed)
    names = sorted(os.listdir("/sys/class/block"))
    nf = rng.choice([14, 18, 20])
    reset = rng.choice(names) if names else None
    la, lb = [], []
    for n in names:
        a10 = rng.randint(1, 2 ** 40)
        b10 = rng.randint(0, a10 - 1) if n == reset else a10 + rng.randint(0, 2 ** 30)
        la.append(render(rng, fields_line(rng, n, nf, a10)))
        lb.append(render(rng, fields_line(rng, n, nf, b10)))
    text_a, text_b = "\n".join(la) + "\n", "\n".join(lb) + "\n"
    ms = 400
    d = tempfile.mkdtemp(prefix="mori-r34-fed-")
    fifo = os.path.join(d, "ds")
    os.mkfifo(fifo)
    marks = {}

    def feed():
        fd = os.open(fifo, os.O_WRONLY)
        os.write(fd, text_a.encode())
        os.close(fd)
        while True:  # wait until the reader has closed sample A (a non-blocking open then fails ENXIO)
            try:
                fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
                os.close(fd)
                time.sleep(0.002)
            except OSError as e:
                if e.errno != errno.ENXIO:
                    raise
                break
        marks["a_closed"] = time.monotonic()
        fd = os.open(fifo, os.O_WRONLY)
        marks["b_opened"] = time.monotonic()
        os.write(fd, text_b.encode())
        os.close(fd)

    th = threading.Thread(target=feed, daemon=True)
    th.start()
    hide = ("mount --bind \"$0\" /proc/diskstats && mount -t tmpfs none /home && mount -t tmpfs none /fast"
            " && exec setpriv --bounding-set=-all --inh-caps=-all --ambient-caps=-all --no-new-privs -- \"$@\"")
    try:
        p = subprocess.run(["unshare", "--user", "--map-root-user", "--mount", "--", "sh", "-c", hide, fifo,
                            sys.executable, tool, "--interval-ms", str(ms)], capture_output=True, text=True,
                           timeout=20, cwd=tempfile.gettempdir())
        rc, stdout = p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        rc, stdout = "timeout", ""
    try:  # release a feeder still blocked on an open
        os.close(os.open(fifo, os.O_RDONLY | os.O_NONBLOCK))
    except OSError:
        pass
    th.join(2)
    shutil.rmtree(d, ignore_errors=True)
    if rc != 0:
        return f"fed-rc={rc}"
    if "b_opened" not in marks:
        return "fed-single-read"
    if marks["b_opened"] - marks["a_closed"] < 0.9 * ms / 1000:
        return "fed-no-interval"
    try:
        out = json.loads(stdout)
    except ValueError:
        return "fed-not-json"
    if not same(out, oracle(text_a, text_b, "/sys", ms)):
        return "fed-mismatch"
    return None


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__, file=sys.stderr)
        return 2
    rev, repo, seed, nrand = argv[0], os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))), None, 300
    i = 1
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]
        elif argv[i] == "--seed":
            seed = int(argv[i + 1])
        elif argv[i] == "--random":
            nrand = int(argv[i + 1])
        else:
            print(f"unknown argument {argv[i]}", file=sys.stderr)
            return 2
        i += 2
    if nrand != 300:
        print("note: --random other than 300 is a diagnostic run, never the predicate", file=sys.stderr)
    full = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", rev + "^{commit}"],
                          capture_output=True, text=True).stdout.strip()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"measured_at={stamp} repo={repo} rev={full or rev}")
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:{TOOL}"], capture_output=True)
    if src.returncode != 0 or not full:
        print("tool=absent C1=unmet")
        return 1
    work = tempfile.mkdtemp(prefix="mori-r34-tool-")
    tool = os.path.join(work, "mori-disk-rate.py")
    open(tool, "wb").write(src.stdout)
    try:
        text = src.stdout.decode("utf-8", "replace")
        guard = [w for w in (".ufo", "count-c1") if w in text]
        if seed is None:
            seed = int.from_bytes(os.urandom(8), "big")
        seen = {"state": set(), "class": set()}
        ffix = score_seeds(tool, FIXED_SEEDS, {"state": set(), "class": set()})
        frand = score_seeds(tool, [seed * 1000 + k for k in range(nrand)], seen)
        lv = live(tool) or fed_live(tool, seed)
        cover = set(STATES) <= seen["state"] and set(CLASSES) <= seen["class"]
        met = not guard and not ffix and not frand and lv is None and cover and nrand == 300
        print(f"tool=present guard={guard or 'clean'} seed={seed}")
        print(f"fixed_pass={len(FIXED_SEEDS) - len(ffix)}/{len(FIXED_SEEDS)} "
              f"random_pass={nrand - len(frand)}/{nrand}")
        print(f"states_seen={sorted(seen['state'])} classes_seen={sorted(seen['class'])} coverage={'ok' if cover else 'short'}")
        print(f"live={lv or 'ok'}")
        if ffix or frand:
            print(f"first_fails={(ffix + frand)[:5]}")
        print("C1=met" if met else "C1=unmet")
        return 0 if met else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
