#!/usr/bin/env python3
"""Round 53 C2 counter (coverage) — the commit ledger as a runway surface a mori tool reads, by overcommit mode.

Round 52 admitted what CommitLimit and Committed_AS are (corpus/knowledge/overcommit-commit-limit-r52.md); no
mori tool reads them. The round moves that surface from knowledge into a read-only tool,
tools/mori-commit-runway.py, whose verdict depends on the overcommit mode and, under mode 2, on the
approximation band of the per-CPU committed counter (mm/mm_init.c mm_compute_batch, lib/percpu_counter.c).

Frozen predicate P-C2 (same sentence in contract.md, this counter and the receipt label):
  At revision R, tools/mori-commit-runway.py is a regular file; run from a git archive of R with
  `python3 -I -B`, its `--selftest` exits 0 and its last line is `MORI_COMMIT_RUNWAY_SELFTEST: PASS n/n` with
  n >= 12; on each of the 16 frozen edge fixtures below and the 64 fixtures this counter generates from the
  seed sha256(<full commit id of R>), the tool run with --meminfo, --vm-dir, --cpu-present and --page-kb
  pointing at that fixture exits with the reference exit code and prints one JSON object whose 15 checked
  fields equal this counter's reference reading (REF below, written from mm/util.c, mm/mm_init.c and
  lib/percpu_counter.c at v7.2); SKILL.md at R carries a table row naming tools/mori-commit-runway.py and
  --selftest; and the tool run on this host's defaults exits 0 or 1 and reports the mode, CommitLimit, the
  recomputed limit and the present-CPU count this counter reads from the same files.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR]  |  count-c2.py --selftest  |  count-c2.py --fixtures <rev>
Output: `C2=met|unmet tool=present|absent selftest=pass|fail|error n=N fixtures=N agree=N disagree=N
  registry=ok|bad live=ok|bad|error rev=R` (+ `failed=` list, + one `disagree` line per failing fixture).
Exit 0 met, 1 unmet, 2 setup. Writes only under --scratch (default: a fresh directory under $TMPDIR), removed
on exit; reads the lane with `git archive` / `git ls-tree` / `git show` only.

Limits (named before data): REF and the tool may share the author's misreading of the kernel — the fixtures
check agreement with REF, not with the kernel; the band is an upper bound from the batch rule (present CPUs,
totalram at read time), not a measured deviation; the live leg compares stable fields only (Committed_AS moves
between reads) and depends on the host it runs on; the 64 seeded fixtures are reproducible by anyone holding R,
so a tool written after seeing R could memorise them — the seed changes with every commit.
"""
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-commit-runway.py"
SCHEMA = "mori-commit-runway-v1"
MIN_SELFTEST = 12
N_SEEDED = 64
INT_MAX = 2 ** 31 - 1
FIELDS = ["schema", "verdict", "mode", "enforced", "commit_limit_kb", "committed_as_kb", "headroom_kb",
          "reserve_kb", "usable_kb", "band_kb", "batch_pages", "cpus_present", "single_request_cap_kb",
          "limit_recomputed_kb", "limit_consistent"]
CODES = {"COMMIT_OK": 0, "COMMIT_HEURISTIC": 0, "COMMIT_UNLIMITED": 0, "COMMIT_LOW": 1, "COMMIT_UNKNOWN": 2}
MEMINFO_KEYS = ["MemTotal", "SwapTotal", "CommitLimit", "Committed_AS"]
VM_KEYS = ["overcommit_memory", "overcommit_ratio", "overcommit_kbytes", "admin_reserve_kbytes",
           "user_reserve_kbytes"]
SELFTEST_RE = re.compile(r"^MORI_COMMIT_RUNWAY_SELFTEST: PASS (\d+)/(\d+)$")


# ---------------------------------------------------------------- reference reading (REF)
def parse_meminfo(text):
    vals, seen = {}, set()
    for line in text.split("\n"):
        m = re.match(r"^([A-Za-z0-9_()]+):\s*(.*)$", line)
        if not m:
            continue
        key = m.group(1)
        if key in seen and key in MEMINFO_KEYS + ["Hugetlb"]:
            return None
        seen.add(key)
        if key in MEMINFO_KEYS + ["Hugetlb"]:
            v = re.fullmatch(r"(\d+) kB", m.group(2).strip())
            if not v:
                return None
            vals[key] = int(v.group(1))
    if any(k not in vals for k in MEMINFO_KEYS):
        return None
    vals.setdefault("Hugetlb", 0)
    return vals


def parse_present(text):
    t = text.strip()
    if not re.fullmatch(r"\d+(-\d+)?(,\d+(-\d+)?)*", t):
        return None
    n = 0
    for part in t.split(","):
        a, _, b = part.partition("-")
        lo, hi = int(a), int(b) if b else int(a)
        if hi < lo:
            return None
        n += hi - lo + 1
    return n


def parse_int_file(text):
    t = (text or "").strip()
    return int(t) if re.fullmatch(r"\d+", t) else None


def unknown():
    out = {k: None for k in FIELDS}
    out.update(schema=SCHEMA, verdict="COMMIT_UNKNOWN", enforced=None, limit_consistent=None)
    return 2, out


def ref(meminfo_text, vm, present_text, page_kb):
    """vm: name -> text or None. Returns (exit code, dict of FIELDS)."""
    if meminfo_text is None or present_text is None or page_kb < 1 or page_kb & (page_kb - 1):
        return unknown()
    mi = parse_meminfo(meminfo_text)
    cpus = parse_present(present_text)
    vmv = {k: parse_int_file(vm.get(k)) for k in VM_KEYS}
    if mi is None or cpus is None or cpus < 1 or any(v is None for v in vmv.values()):
        return unknown()
    mode = vmv["overcommit_memory"]
    if mode not in (0, 1, 2):
        return unknown()
    ram_pages = mi["MemTotal"] // page_kb
    swap_pages = mi["SwapTotal"] // page_kb
    huge_pages = mi["Hugetlb"] // page_kb
    if vmv["overcommit_kbytes"]:
        allowed = vmv["overcommit_kbytes"] // page_kb
    else:
        allowed = (ram_pages - huge_pages) * vmv["overcommit_ratio"] // 100
    allowed += swap_pages
    out = {k: None for k in FIELDS}
    out.update(schema=SCHEMA, mode=mode, enforced=(mode == 2), commit_limit_kb=mi["CommitLimit"],
               committed_as_kb=mi["Committed_AS"], headroom_kb=mi["CommitLimit"] - mi["Committed_AS"],
               cpus_present=cpus, limit_recomputed_kb=allowed * page_kb,
               limit_consistent=(allowed * page_kb == mi["CommitLimit"]))
    if mode == 1:
        out["verdict"] = "COMMIT_UNLIMITED"
        return 0, out
    if mode == 0:
        out["single_request_cap_kb"] = (ram_pages + swap_pages) * page_kb
        out["verdict"] = "COMMIT_HEURISTIC"
        return 0, out
    batch = max(min(ram_pages // cpus // 256, INT_MAX), max(cpus * 2, 32))
    out["batch_pages"] = batch
    out["band_kb"] = batch * cpus * page_kb
    out["reserve_kb"] = vmv["admin_reserve_kbytes"] + vmv["user_reserve_kbytes"]
    out["usable_kb"] = out["headroom_kb"] - out["reserve_kb"]
    low = out["usable_kb"] <= out["band_kb"]
    out["verdict"] = "COMMIT_LOW" if low else "COMMIT_OK"
    return (1 if low else 0), out


# ---------------------------------------------------------------- fixtures
def meminfo_lines(memtotal, swap, limit, committed, hugetlb=0, extra=None, drop=None, dup=None, garble=None):
    rows = [("MemTotal", memtotal), ("MemFree", memtotal // 3), ("MemAvailable", memtotal // 2),
            ("SwapTotal", swap), ("SwapFree", swap), ("CommitLimit", limit), ("Committed_AS", committed),
            ("Hugetlb", hugetlb)]
    out = []
    for k, v in rows:
        if k == drop:
            continue
        val = "%d kB" % v
        if k == garble:
            val = "%d" % v
        out.append("%-16s%s" % (k + ":", val.rjust(12)))
        if k == dup:
            out.append("%-16s%s" % (k + ":", val.rjust(12)))
    out += ["HugePages_Total:       0", "Hugepagesize:       2048 kB"] + (extra or [])
    return "\n".join(out) + "\n"


def mk(name, memtotal, swap, committed, mode, ratio=50, kbytes=0, hugetlb=0, admin=8192, user=131072,
       present="0-31", page_kb=4, limit=None, **mods):
    pages = (memtotal // page_kb - hugetlb // page_kb) * ratio // 100 if not kbytes else kbytes // page_kb
    lim = (pages + swap // page_kb) * page_kb if limit is None else limit
    vm = {"overcommit_memory": "%s\n" % mode, "overcommit_ratio": "%d\n" % ratio,
          "overcommit_kbytes": "%d\n" % kbytes, "admin_reserve_kbytes": "%d\n" % admin,
          "user_reserve_kbytes": "%d\n" % user}
    for k in mods.pop("vm_drop", []):
        vm[k] = None
    mi = meminfo_lines(memtotal, swap, lim, committed, hugetlb, **mods)
    return {"name": name, "meminfo": mi, "vm": vm, "present": present, "page_kb": page_kb}


def frozen_fixtures():
    g = 31721796  # this host's MemTotal (kB) at freeze
    # band edge: 8 GiB, 32 CPUs, no swap -> limit 4194304, reserve 139264, band 32768 (selftest arithmetic);
    # committed 4022272 leaves usable == band exactly, which is LOW (<=).
    return [
        mk("host-mode0-over", g, 31722876, 60169456, 0),
        mk("mode1-over", g, 0, 90000000, 1),
        mk("mode2-ok", g, 31722876, 20000000, 2),
        mk("mode2-low-negative", g, 0, 17000000, 2),
        mk("mode2-band-edge-low", 8388608, 0, 4022272, 2),
        mk("mode2-band-edge-ok", 8388608, 0, 4022268, 2),
        mk("mode2-kbytes", g, 1048576, 1000000, 2, kbytes=4194304),
        mk("mode2-hugetlb", 16777216, 0, 3000000, 2, hugetlb=4194304, ratio=80, present="0-7"),
        mk("mode2-one-cpu", 2097152, 0, 600000, 2, present="0"),
        mk("mode2-sparse-cpus", 67108864, 0, 1000000, 2, present="0,2-5,8"),
        mk("mode2-page64", 67108864, 0, 1000000, 2, page_kb=64, present="0-63"),
        mk("mode0-limit-mismatch", g, 31722876, 1000, 0, limit=123456),
        mk("unknown-mode3", g, 0, 1000, 3),
        mk("unknown-missing-commitlimit", g, 0, 1000, 2, drop="CommitLimit"),
        mk("unknown-vm-missing", g, 0, 1000, 2, vm_drop=["user_reserve_kbytes"]),
        mk("unknown-bad-present", g, 0, 1000, 2, present="0-3,x"),
    ]


def seeded_fixtures(seed_hex, n=N_SEEDED):
    rng = random.Random(int(seed_hex, 16))
    out = []
    for i in range(n):
        page_kb = rng.choice([4, 4, 4, 4, 16, 64])
        ncpu = rng.choice([1, 2, 4, 8, 12, 16, 32, 48, 64, 96, 128, 256])
        present = rng.choice(["0-%d" % (ncpu - 1) if ncpu > 1 else "0", ",".join(str(c) for c in range(ncpu))])
        mem = rng.randrange(2 ** 18, 2 ** 28) // page_kb * page_kb
        swap = rng.choice([0, 0, rng.randrange(0, 2 ** 27) // page_kb * page_kb])
        huge = rng.choice([0, 0, 0, rng.randrange(0, mem // 2) // page_kb * page_kb])
        ratio = rng.choice([50, 50, rng.randrange(0, 101)])
        kbytes = rng.choice([0, 0, 0, rng.randrange(1, 2 ** 26)])
        mode = rng.choice([0, 1, 2, 2, 2])
        admin, user = rng.choice([(8192, 131072), (rng.randrange(0, 2 ** 18), rng.randrange(0, 2 ** 18))])
        pages = (mem // page_kb - huge // page_kb) * ratio // 100 if not kbytes else kbytes // page_kb
        lim = (pages + swap // page_kb) * page_kb
        ram_pages = mem // page_kb
        batch = max(ram_pages // ncpu // 256, max(ncpu * 2, 32))
        band = batch * ncpu * page_kb
        style = rng.random()
        if style < 0.35:  # near the band edge (mode 2 boundary)
            committed = max(0, lim - admin - user - band + rng.randrange(-3, 4) * page_kb)
        else:
            committed = rng.randrange(0, max(1, 2 * lim + 1))
        kw = {}
        bad = rng.random()
        if bad < 0.04:
            kw["drop"] = rng.choice(MEMINFO_KEYS)
        elif bad < 0.07:
            kw["dup"] = rng.choice(MEMINFO_KEYS)
        elif bad < 0.09:
            mode = rng.choice([3, 7])
        elif bad < 0.11:
            kw["vm_drop"] = [rng.choice(VM_KEYS)]
        elif bad < 0.13:
            present = "0-%d,a" % ncpu
        out.append(mk("seeded-%02d" % i, mem, swap, committed, mode, ratio=ratio, kbytes=kbytes, hugetlb=huge,
                      admin=admin, user=user, present=present, page_kb=page_kb,
                      limit=lim if rng.random() > 0.1 else lim + page_kb, **kw))
    return out


def ref_for(fx):
    return ref(fx["meminfo"], fx["vm"], fx["present"], fx["page_kb"])


def write_fixture(fx, root):
    d = os.path.join(root, fx["name"])
    os.makedirs(os.path.join(d, "vm"))
    with open(os.path.join(d, "meminfo"), "w") as f:
        f.write(fx["meminfo"])
    for k, v in fx["vm"].items():
        if v is not None:
            with open(os.path.join(d, "vm", k), "w") as f:
                f.write(v)
    with open(os.path.join(d, "present"), "w") as f:
        f.write(fx["present"] + "\n")
    return d


# ---------------------------------------------------------------- harness
def run_tool(tool, args, timeout=30):
    try:
        p = subprocess.run([sys.executable, "-I", "-B", tool] + args, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout, cwd=os.path.dirname(os.path.dirname(tool)))
    except (subprocess.SubprocessError, OSError) as exc:
        return None, "", str(exc)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def compare(fx, tool, root):
    d = write_fixture(fx, root)
    rc, out, _ = run_tool(tool, ["--meminfo", os.path.join(d, "meminfo"), "--vm-dir", os.path.join(d, "vm"),
                                 "--cpu-present", os.path.join(d, "present"), "--page-kb", str(fx["page_kb"])])
    code, want = ref_for(fx)
    try:
        got = json.loads(out)
    except ValueError:
        return "%s: no JSON (rc=%s)" % (fx["name"], rc)
    if not isinstance(got, dict):
        return "%s: not an object" % fx["name"]
    diffs = ["%s want=%r got=%r" % (k, want[k], got.get(k, "<missing>")) for k in FIELDS
             if k not in got or got[k] != want[k] or type(got[k]) is not type(want[k])]
    if rc != code:
        diffs.insert(0, "exit want=%d got=%s" % (code, rc))
    return ("%s: %s" % (fx["name"], "; ".join(diffs))) if diffs else None


def read_text(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return None


def live_check(tool):
    before = read_text("/proc/meminfo")
    rc, out, _ = run_tool(tool, [])
    after = read_text("/proc/meminfo")
    vm = {k: read_text("/proc/sys/vm/" + k) for k in VM_KEYS}
    present = read_text("/sys/devices/system/cpu/present")
    page_kb = os.sysconf("SC_PAGE_SIZE") // 1024
    if before is None or after is None:
        return "error"
    c1, w1 = ref(before, vm, present, page_kb)
    c2, w2 = ref(after, vm, present, page_kb)
    try:
        got = json.loads(out)
    except ValueError:
        return "bad"
    if rc not in (0, 1) or not isinstance(got, dict):
        return "bad"
    for k in ("mode", "commit_limit_kb", "limit_recomputed_kb", "cpus_present", "limit_consistent"):
        if w1[k] != w2[k] or got.get(k) != w1[k]:
            return "bad"
    return "ok"


def evaluate_tree(tree, seed_hex, skill_text, live=True):
    """tree: extracted archive root. Returns (met, line, disagreements)."""
    failed, dis = [], []
    tool = os.path.join(tree, TOOL)
    present = os.path.isfile(tool) and not os.path.islink(tool)
    st, n, agree, registry, live_s = "error", 0, 0, "bad", "error"
    fixtures = frozen_fixtures() + seeded_fixtures(seed_hex)
    if not present:
        failed.append("tool_absent")
    else:
        rc, out, _ = run_tool(tool, ["--selftest"], timeout=300)
        lines = [l for l in out.strip().split("\n") if l.strip()]
        m = SELFTEST_RE.match(lines[-1]) if lines else None
        if rc == 0 and m and m.group(1) == m.group(2) and int(m.group(1)) >= MIN_SELFTEST:
            st, n = "pass", int(m.group(1))
        else:
            st = "fail"
            failed.append("selftest")
        root = tempfile.mkdtemp(prefix="fixtures-", dir=os.path.dirname(tree))
        for fx in fixtures:
            r = compare(fx, tool, root)
            if r is None:
                agree += 1
            else:
                dis.append(r)
        if dis:
            failed.append("fixtures")
        live_s = live_check(tool) if live else "skip"
        if live_s != "ok" and live:
            failed.append("live")
    for line in (skill_text or "").split("\n"):
        if line.lstrip().startswith("|") and TOOL in line and "--selftest" in line:
            registry = "ok"
    if registry != "ok":
        failed.append("registry")
    met = not failed
    line = ("C2=%s tool=%s selftest=%s n=%d fixtures=%d agree=%d disagree=%d registry=%s live=%s"
            % ("met" if met else "unmet", "present" if present else "absent", st, n, len(fixtures), agree,
               len(dis), registry, live_s))
    if failed:
        line += " failed=" + ",".join(sorted(set(failed)))
    return met, line, dis


def lane_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    args = list(argv)
    repo, scratch = lane_root(), None
    while "--repo" in args:
        i = args.index("--repo")
        repo = args[i + 1]
        del args[i:i + 2]
    while "--scratch" in args:
        i = args.index("--scratch")
        scratch = args[i + 1]
        del args[i:i + 2]
    fixtures_only = False
    if args and args[0] == "--fixtures":
        fixtures_only = True
        args = args[1:]
    if len(args) != 1 or args[0].startswith("-"):
        print("C2_SETUP usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | --selftest | --fixtures <rev>",
              file=sys.stderr)
        return 2
    try:
        full = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", args[0] + "^{commit}"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
                              check=True).stdout.decode().strip()
    except (subprocess.SubprocessError, OSError):
        print("C2_SETUP unresolvable revision %s" % args[0], file=sys.stderr)
        return 2
    seed = hashlib.sha256(full.encode()).hexdigest()
    if fixtures_only:
        for fx in frozen_fixtures() + seeded_fixtures(seed):
            code, want = ref_for(fx)
            print("%s exit=%d %s" % (fx["name"], code, json.dumps(want, sort_keys=True)))
        return 0
    if scratch:
        os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2-", dir=scratch)
    try:
        tree = os.path.join(work, "tree")
        os.makedirs(tree)
        arch = subprocess.run(["git", "-C", repo, "archive", full], stdout=subprocess.PIPE, timeout=300)
        if arch.returncode != 0:
            print("C2_SETUP archive failed", file=sys.stderr)
            return 2
        subprocess.run(["tar", "-x", "-C", tree], input=arch.stdout, check=True, timeout=300)
        skill = subprocess.run(["git", "-C", repo, "show", "%s:SKILL.md" % full], stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, timeout=60).stdout.decode("utf-8", "replace")
        met, line, dis = evaluate_tree(tree, seed, skill)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(line + " rev=" + full)
    for d in dis:
        print("disagree " + d)
    return 0 if met else 1


# ---------------------------------------------------------------- selftest
REF_TOOL = r'''
import json, os, sys
sys.path.insert(0, os.environ["C2_COUNTER_DIR"])
import importlib.util
spec = importlib.util.spec_from_file_location("c2", os.path.join(os.environ["C2_COUNTER_DIR"], "count-c2.py"))
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
a = sys.argv[1:]
if a == ["--selftest"]:
    print("MORI_COMMIT_RUNWAY_SELFTEST: PASS %s" % os.environ.get("C2_FAKE_PASS", "12/12")); sys.exit(0)
o = dict(zip(a[::2], a[1::2]))
def rd(p):
    try:
        return open(p).read()
    except OSError:
        return None
vmd = o.get("--vm-dir", "/proc/sys/vm")
vm = {k: rd(os.path.join(vmd, k)) for k in c2.VM_KEYS}
code, out = c2.ref(rd(o.get("--meminfo", "/proc/meminfo")), vm, rd(o.get("--cpu-present", "/sys/devices/system/cpu/present")),
                   int(o.get("--page-kb", os.sysconf("SC_PAGE_SIZE") // 1024)))
MUT = os.environ.get("C2_MUTANT", "")
if MUT == "mode_blind" and out["mode"] in (0, 1):
    out["verdict"] = "COMMIT_LOW" if out["headroom_kb"] < 0 else "COMMIT_OK"; code = 1 if out["headroom_kb"] < 0 else 0
if MUT == "no_band" and out["mode"] == 2:
    out["verdict"] = "COMMIT_LOW" if out["usable_kb"] <= 0 else "COMMIT_OK"; code = 1 if out["usable_kb"] <= 0 else 0
if MUT == "no_hugetlb" and out["limit_recomputed_kb"] is not None:
    out["limit_consistent"] = True
if MUT == "string_numbers" and out["commit_limit_kb"] is not None:
    out["commit_limit_kb"] = str(out["commit_limit_kb"])
print(json.dumps(out)); sys.exit(code)
'''


def selftest():
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    # REF on hand-computed cases (arithmetic written out in the comments, independent of ref()).
    # This host at freeze: MemTotal 31721796 kB, SwapTotal 31722876 kB, ratio 50, page 4 kB:
    # (7930449 * 50 // 100 + 7930719) * 4 = (3965224 + 7930719) * 4 = 47583772 = the printed CommitLimit.
    code, o = ref_for(mk("h", 31721796, 31722876, 60169456, 0, limit=47583772))
    check("ref_host_limit", code == 0 and o["limit_recomputed_kb"] == 47583772 and o["limit_consistent"] is True
          and o["verdict"] == "COMMIT_HEURISTIC" and o["headroom_kb"] == 47583772 - 60169456
          and o["single_request_cap_kb"] == 31721796 + 31722876 and o["band_kb"] is None)
    # Mode 2, 8 GiB, 32 CPUs, no swap: ram 2097152 pages; batch = max(2097152//32//256=256, max(64,32)) = 256;
    # band = 256*32*4 = 32768 kB; limit = 1048576 pages*4 = 4194304 kB; reserve 139264; committed 4000000:
    # usable = 194304 - 139264 = 55040 > 32768 -> OK; committed 4030000 -> usable 25040 <= 32768 -> LOW.
    code, o = ref_for(mk("m2", 8388608, 0, 4000000, 2))
    check("ref_mode2_ok", code == 0 and o["batch_pages"] == 256 and o["band_kb"] == 32768
          and o["usable_kb"] == 55040 and o["verdict"] == "COMMIT_OK" and o["enforced"] is True)
    code, o = ref_for(mk("m2l", 8388608, 0, 4030000, 2))
    check("ref_mode2_low", code == 1 and o["usable_kb"] == 25040 and o["verdict"] == "COMMIT_LOW")
    # Small host, 4 CPUs, 1 GiB: 262144 pages; 262144//4//256 = 256; max(8,32)=32 -> batch 256 band 4096 kB.
    code, o = ref_for(mk("s", 1048576, 0, 1000, 2, present="0-3"))
    check("ref_small_batch", o["batch_pages"] == 256 and o["band_kb"] == 4096)
    # Floor: 64 CPUs, 1 GiB: 262144//64//256 = 16 < max(128,32)=128 -> batch 128.
    code, o = ref_for(mk("f", 1048576, 0, 1000, 2, present="0-63"))
    check("ref_batch_floor", o["batch_pages"] == 128 and o["band_kb"] == 128 * 64 * 4)
    # overcommit_kbytes 4194304 with page 4: 1048576 pages + swap 262144 pages = 5242880 kB.
    code, o = ref_for(mk("k", 31721796, 1048576, 1000, 2, kbytes=4194304))
    check("ref_kbytes", o["limit_recomputed_kb"] == 5242880 and o["limit_consistent"] is True)
    # Hugetlb 4 GiB of 16 GiB, ratio 80: (4194304-1048576)*80//100 = 2516582 pages -> 10066328 kB.
    code, o = ref_for(mk("hg", 16777216, 0, 1000, 2, hugetlb=4194304, ratio=80, present="0-7"))
    check("ref_hugetlb", o["limit_recomputed_kb"] == 10066328)
    check("ref_present_parse", parse_present("0,2-5,8") == 6 and parse_present("0-31") == 32
          and parse_present("3-1") is None and parse_present("0-3,x") is None)
    code, o = ref_for(mk("m1", 1048576, 0, 9999999, 1))
    check("ref_mode1", code == 0 and o["verdict"] == "COMMIT_UNLIMITED" and o["band_kb"] is None
          and o["usable_kb"] is None and o["headroom_kb"] < 0)
    for name, kw in [("mode3", {"mode": 3}), ("drop", {"drop": "Committed_AS"}), ("dup", {"dup": "MemTotal"}),
                     ("garble", {"garble": "CommitLimit"}), ("vmdrop", {"vm_drop": ["overcommit_ratio"]})]:
        mode = kw.pop("mode", 2)
        code, o = ref_for(mk(name, 1048576, 0, 1000, mode, **kw))
        check("ref_unknown_" + name, code == 2 and o["verdict"] == "COMMIT_UNKNOWN" and o["mode"] is None)
    code, o = ref_for(mk("lim", 31721796, 31722876, 1000, 0, limit=123456))
    check("ref_limit_mismatch", o["limit_consistent"] is False and o["commit_limit_kb"] == 123456)
    check("frozen_count", len(frozen_fixtures()) == 16)
    a, b = seeded_fixtures("ab" * 32), seeded_fixtures("ab" * 32)
    check("seeded_reproducible", [x["meminfo"] for x in a] == [x["meminfo"] for x in b] and len(a) == N_SEEDED)
    c = seeded_fixtures("cd" * 32)
    check("seeded_varies", [x["meminfo"] for x in a] != [x["meminfo"] for x in c])
    kinds = set(ref_for(fx)[1]["verdict"] for fx in a + frozen_fixtures())
    check("fixture_verdict_mix", kinds == set(CODES))

    # Harness against generated tools in a temp tree.
    base = tempfile.mkdtemp(prefix="c2-selftest-")
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        os.environ["C2_COUNTER_DIR"] = here

        def tree_with(src, name):
            t = os.path.join(base, name, "tree")
            os.makedirs(os.path.join(t, "tools"))
            if src is not None:
                with open(os.path.join(t, TOOL), "w") as f:
                    f.write(src)
            return t

        skill = "| commit runway | gate | `python3 -I -B tools/mori-commit-runway.py [--selftest]` |\n"
        t = tree_with(REF_TOOL, "witness")
        met, line, dis = evaluate_tree(t, "11" * 32, skill, live=False)
        check("harness_witness_met", met and "agree=80 disagree=0" in line)
        met, line, dis = evaluate_tree(tree_with(None, "absent"), "11" * 32, skill, live=False)
        check("harness_absent_unmet", (not met) and "tool_absent" in line)
        met, line, dis = evaluate_tree(t, "11" * 32, "no row here\n", live=False)
        check("harness_registry_unmet", (not met) and "registry" in line)
        for mut in ("mode_blind", "no_band", "no_hugetlb", "string_numbers"):
            os.environ["C2_MUTANT"] = mut
            met, line, dis = evaluate_tree(t, "11" * 32, skill, live=False)
            check("harness_mutant_%s_unmet" % mut, (not met) and "fixtures" in line)
        os.environ["C2_MUTANT"] = ""
        os.environ["C2_FAKE_PASS"] = "3/3"
        met, line, dis = evaluate_tree(t, "11" * 32, skill, live=False)
        check("harness_selftest_floor_unmet", (not met) and "selftest=fail" in line)
        os.environ["C2_FAKE_PASS"] = "12/13"
        met, line, dis = evaluate_tree(t, "11" * 32, skill, live=False)
        check("harness_selftest_partial_unmet", (not met) and "selftest=fail" in line)
        os.environ["C2_FAKE_PASS"] = "12/12"
        memo = os.path.join(base, "memo.json")
        with open(memo, "w") as f:
            json.dump({fx["name"]: ref_for(fx) for fx in frozen_fixtures()}, f)
        memo_src = REF_TOOL.replace("MUT = os.environ.get(\"C2_MUTANT\", \"\")",
                                    "MUT = 'no_band' if os.path.basename(os.path.dirname(o.get('--meminfo', '/x/y'))).startswith('seeded') else ''")
        met, line, dis = evaluate_tree(tree_with(memo_src, "memoriser"), "22" * 32, skill, live=False)
        check("harness_memoriser_unmet", (not met) and "fixtures" in line)
        live = live_check(os.path.join(t, TOOL))
        check("harness_live_witness", live in ("ok", "error"))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    failn = 0
    for name, ok in checks:
        print("%s %s" % ("ok  " if ok else "FAIL", name))
        failn += 0 if ok else 1
    print("C2_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
