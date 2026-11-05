#!/usr/bin/env python3
"""count-c1.py -- mori round 99, claim C1 (operability), frozen counter.

Predicate P1 (same sentence as .ufo/waves/round-99/contract.md section C1): on the tree DIR of
revision R, (a) `tools/mori-userns-runway.py --selftest` exits 0 with last line
`MORI_USERNS_RUNWAY_SELFTEST: PASS (<n> cases)`; (b) the tool answers every case of a battery
GENERATED AT MEASUREMENT TIME from a printed seed (16 journal families x 3 instances in sudo's
own COMMAND= rendering, 12 fake-/proc runway cases), each expected answer computed by this
counter from what it planted, never from the tool: journal cases must match rc, the
`SYSCTL_WRITES` summary and the multiset of (key, value) on `SYSCTL_WRITE` lines; runway cases
must match rc and the whole `USERNS_RUNWAY` line; (c) a live run agrees with this counter's own
read of /proc/sys/user/max_user_namespaces and of the distinct non-initial `ns/user` links in at
least one of 3 attempts (limit and used_lb both equal); (d) the round-99 full incident capture
(sha256 pinned) scores rc 1, `SYSCTL_WRITES n=6 keys=1 userns_zero=2`, the six pinned writes and
no `SYSCTL_WRITES_SETUP` line; (e) `tools/mori-gate-registry.py --rev WORK --repo DIR
--audit-all` prints `REGISTRY=met`; (f) `corpus/knowledge/sudo-log-grammar-r99.md` cites in a
`source:` line an S-id above S632 (a row opened this round) whose `corpus/SOURCES.md` row is
`mined` and lists that knowledge path in `used-by`.

Usage: python3 .ufo/waves/round-99/count-c1.py --root DIR [--seed N] [--work SCRATCH]
Output: one `case <name> ok|FAIL` line per failed case, then
  C1=met|unmet cases_ok=K/T seed=N selftest=.. live=.. incident=.. registry=.. sourced=.. checks_failed=..
Exit 0 met, 1 unmet, 2 C1_SETUP (DIR missing, incident capture missing or sha differs).
Scratch: --work, else tempfile under TMPDIR (honoured; /tmp is never hardcoded); removed on exit.
"""

import argparse
import collections
import hashlib
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-userns-runway.py"
KNOW = "corpus/knowledge/sudo-log-grammar-r99.md"
INCIDENT = ".ufo/waves/round-99/evidence/journal-incident-r99.txt"
INCIDENT_SHA = "7ec650c9d41085938793451b4404e66fdb4f2c6e960600f3b57bfbfcf2d6090d"
INCIDENT_WRITES = sorted([("user.max_user_namespaces", "0"), ("user.max_user_namespaces", "10000"),
                          ("user.max_user_namespaces", "15638"), ("user.max_user_namespaces", "15638"),
                          ("user.max_user_namespaces", "0"), ("user.max_user_namespaces", "122865")])
ENTERING_MAX_SID = 632
INIT = 4026531837
USERNS = "user/max_user_namespaces"
KEYS = [USERNS, USERNS, "kernel/pid_max", "vm/swappiness", "vm/overcommit_memory",
        "net/core/somaxconn", "fs/inotify/max_user_watches", "kernel/unprivileged_userns_clone"]
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def run(argv, timeout=120):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired) as e:
        return -1, "RUN_ERROR %s" % e.__class__.__name__


def fields(line):
    return dict(kv.split("=", 1) for kv in line.split()[1:] if "=" in kv)


class Gen:
    def __init__(self, rnd):
        self.r = rnd
        self.pid = rnd.randrange(100000, 900000)

    def ts(self):
        r = self.r
        return "2026-%02d-%02dT%02d:%02d:%02d-03:00" % (r.randrange(1, 13), r.randrange(1, 29),
                                                       r.randrange(24), r.randrange(60), r.randrange(60))

    def npid(self):
        self.pid += self.r.randrange(1, 997)
        return str(self.pid)

    def sudo(self, cmd, pid=None, ts=None):
        u = self.r.choice(["alice", "vgx", "op"])
        return "%s h%d sudo[%s]:    %s : PWD=/w ; USER=root ; COMMAND=%s" % (
            ts or self.ts(), self.r.randrange(9), pid or self.npid(), u, cmd)

    def kv(self):
        k = self.r.choice(KEYS)
        v = "0" if (k == USERNS and self.r.random() < 0.5) else str(self.r.randrange(1, 200000))
        return k, v

    def decoy(self):
        k, v = self.kv()
        return "%s h app[%s]: note COMMAND=/usr/bin/sh -c 'echo %s > /proc/sys/%s'" % (self.ts(), self.npid(), v, k)


def dot(k):
    return k.replace("/", ".")


def family(g, name):
    """Return (lines, expected writes [(dotted key, value)], expected rc)."""
    k, v = g.kv()
    d = dot(k)
    if name == "W1-sysctl":
        return [g.sudo("/usr/bin/sysctl -w %s=%s" % (d, v))], [(d, v)], 1
    if name == "W2-sh-echo":
        return [g.sudo("/usr/bin/sh -c 'echo %s > /proc/sys/%s'" % (v, k))], [(d, v)], 1
    if name == "W3-tee-a":
        return [g.sudo("/usr/bin/sh -c 'echo %s | tee -a /proc/sys/%s'" % (v, k))], [(d, v)], 1
    if name == "W4-sh-sysctl":
        return [g.sudo("/usr/bin/sh -c 'sysctl -w %s=%s'" % (d, v))], [(d, v)], 1
    if name == "W5-env-sysctl":
        return [g.sudo("/usr/bin/env LC_ALL=C sysctl %s=%s" % (d, v))], [(d, v)], 1
    if name == "W6-printf-fd":
        return [g.sudo("/usr/bin/bash -c 'printf %s >> /proc/sys/%s 2>/dev/null'" % (v, k))], [(d, v)], 1
    if name == "W7-sudo-escape":
        return [g.sudo("/usr/bin/sh -c 'printf \\'%s\\' > /proc/sys/%s#012true'" % (v, k))], [(d, v)], 1
    if name == "W8-continued":
        pid = g.npid()
        return ([g.sudo("/usr/bin/sh -c 'echo %s >" % v, pid=pid),
                 g.sudo("/usr/bin/sysctl -a"),
                 "%s h1 sudo[%s]:    op : (command continued) /proc/sys/%s'" % (g.ts(), pid, k)], [(d, v)], 1)
    if name == "R1-quoted":
        return [g.sudo("/usr/bin/sh -c 'echo \"echo %s > /proc/sys/%s\" > /dev/null'" % (v, k))], [], 0
    if name == "R2-comment":
        return [g.sudo("/usr/bin/bash -c '# echo %s > /proc/sys/%s'" % (v, k))], [], 0
    if name == "R3-pattern":
        return [g.sudo("/usr/bin/sysctl -a -r %s=%s" % (d, v))], [], 0
    if name == "R4-exit-event":
        pid = g.npid()
        return ([g.sudo("/usr/bin/sysctl -w %s=%s" % (d, v), pid=pid),
                 g.sudo("/usr/bin/sysctl -w %s=%s ; EXIT=0" % (d, v), pid=pid)], [(d, v)], 1)
    if name == "R5-reads":
        return [g.sudo("/usr/bin/cat /proc/sys/%s" % k), g.sudo("/usr/bin/sysctl %s" % d)], [], 0
    if name == "S1-short-format":
        ts = "%s %02d %02d:%02d:%02d" % (g.r.choice(MON), g.r.randrange(1, 29), g.r.randrange(24),
                                          g.r.randrange(60), g.r.randrange(60))
        return [g.sudo("/usr/bin/sh -c 'echo %s > /proc/sys/%s'" % (v, k), ts=ts)], [(d, v)], 1
    if name == "S2-unknown-ts":
        return [g.sudo("/usr/bin/sh -c 'echo %s > /proc/sys/%s'" % (v, k), ts="x y")], [], 2
    if name == "S3-truncated":
        k2, v2 = g.kv()
        return ([g.sudo("/usr/bin/sysctl -w %s=%s" % (dot(k2), v2)),
                 g.sudo("/usr/bin/sh -c 'echo %s > /proc/sys/%s" % (v, k))], [(dot(k2), v2)], 2)
    raise KeyError(name)


FAMILIES = ["W1-sysctl", "W2-sh-echo", "W3-tee-a", "W4-sh-sysctl", "W5-env-sysctl", "W6-printf-fd",
            "W7-sudo-escape", "W8-continued", "R1-quoted", "R2-comment", "R3-pattern", "R4-exit-event",
            "R5-reads", "S1-short-format", "S2-unknown-ts", "S3-truncated"]
INSTANCES = 3


def expected_summary(writes):
    keys = len({k for k, _ in writes})
    zero = sum(1 for k, v in writes if k == dot(USERNS) and v == "0")
    return "SYSCTL_WRITES n=%d keys=%d userns_zero=%d" % (len(writes), keys, zero)


def got_writes(out):
    res = []
    for line in out.splitlines():
        if line.startswith("SYSCTL_WRITE "):
            f = fields(line)
            res.append((f.get("key"), f.get("value")))
    return sorted(res)


def runway_case(g, root, idx, kind):
    r = g.r
    d = os.path.join(root, "rw%02d" % idx)
    os.makedirs(os.path.join(d, "sys", "user"))
    os.makedirs(os.path.join(d, "self"))
    k = r.randrange(0, 40)
    if kind == "over":
        limit = r.randrange(0, max(k, 1))
        k = max(k, limit + 1)
    elif kind == "zero":
        limit = 0
    else:
        limit = r.randrange(0, 80)
    nss = r.sample(range(4026532000, 4026599999), k)
    links = ["user:[%d]" % INIT] * r.randrange(1, 6)
    for ns in nss:
        links += ["user:[%d]" % ns] * r.randrange(1, 4)
    nones = r.randrange(0, 3)
    nets = r.randrange(0, 3)
    links += [None] * nones + ["net:[%d]" % r.randrange(4026531000, 4026539999) for _ in range(nets)]
    r.shuffle(links)
    with open(os.path.join(d, "sys", "user", "max_user_namespaces"), "w") as fh:
        fh.write("%d\n" % limit)
    for n, t in enumerate(links, 1):
        p = os.path.join(d, str(r.randrange(1, 10 ** 6) * 100 + n), "ns")
        os.makedirs(p)
        if t is not None:
            os.symlink(t, os.path.join(p, "user"))
    low = r.randrange(1, 40)
    runway = max(limit - k, 0)
    state = "exhausted" if runway == 0 else ("low" if runway < low else "ok")
    want = "USERNS_RUNWAY limit=%d used_lb=%d pids=%d unreadable=%d runway=%d low=%d state=%s" % (
        limit, k, len(links), nones + nets, runway, low, state)
    return d, low, want, (0 if state == "ok" else 1)


def live_independent():
    limit = open("/proc/sys/user/max_user_namespaces").read().strip()
    seen = set()
    for e in os.listdir("/proc"):
        if e.isdigit():
            try:
                t = os.readlink("/proc/%s/ns/user" % e)
            except OSError:
                continue
            m = re.fullmatch(r"user:\[(\d+)\]", t)
            if m and int(m.group(1)) != INIT:
                seen.add(m.group(1))
    return limit, str(len(seen))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("C1_SETUP root missing")
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    inc = os.path.join(root, INCIDENT)
    if not os.path.isfile(inc):
        inc = os.path.join(here, "evidence", os.path.basename(INCIDENT))
    try:
        inc_bytes = open(inc, "rb").read()
    except OSError:
        print("C1_SETUP incident capture unreadable")
        return 2
    if hashlib.sha256(inc_bytes).hexdigest() != INCIDENT_SHA:
        print("C1_SETUP incident capture sha256 differs from the frozen pin")
        return 2
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
    g = Gen(random.Random(seed))
    if a.work:
        os.makedirs(a.work, exist_ok=True)
        work = tempfile.mkdtemp(prefix="mori-r99-c1-", dir=a.work)
    else:
        work = tempfile.mkdtemp(prefix="mori-r99-c1-")
    py = sys.executable
    tool = os.path.join(root, TOOL)
    have_tool = os.path.isfile(tool)
    fails = []
    ok_cases = total = 0
    try:
        # (a) selftest
        selftest = "absent"
        if have_tool:
            rc, out = run([py, tool, "--selftest"])
            last = (out.strip().splitlines() or [""])[-1]
            selftest = "ok" if rc == 0 and re.fullmatch(r"MORI_USERNS_RUNWAY_SELFTEST: PASS \(\d+ cases\)", last) else "fail"
        if selftest != "ok":
            fails.append("selftest")
        # (b) generated journal battery
        for fam in FAMILIES:
            for i in range(INSTANCES):
                lines, writes, want_rc = family(g, fam)
                body = list(lines)
                for _ in range(g.r.randrange(0, 3)):
                    body.insert(g.r.randrange(0, len(body) + 1), g.decoy())
                path = os.path.join(work, "j-%s-%d.txt" % (fam, i))
                with open(path, "w") as fh:
                    fh.write("\n".join(body) + "\n")
                total += 1
                good = False
                if have_tool:
                    rc, out = run([py, tool, "--journal", path])
                    summ = [l for l in out.splitlines() if l.startswith("SYSCTL_WRITES n=")]
                    good = (rc == want_rc and summ == [expected_summary(writes)]
                            and got_writes(out) == sorted(writes))
                if good:
                    ok_cases += 1
                else:
                    print("case %s-%d FAIL" % (fam, i))
        # (b) generated runway battery
        kinds = ["over", "over", "zero"] + ["any"] * 9
        for idx, kind in enumerate(kinds):
            d, low, want, want_rc = runway_case(g, work, idx, kind)
            total += 1
            good = False
            if have_tool:
                rc, out = run([py, tool, "--proc", d, "--low", str(low)])
                good = rc == want_rc and out.strip() == want
            if good:
                ok_cases += 1
            else:
                print("case runway-%02d-%s FAIL" % (idx, kind))
        if ok_cases != total:
            fails.append("battery")
        # (c) live cross-check
        live = "absent"
        if have_tool:
            live = "fail"
            for _ in range(3):
                rc, out = run([py, tool])
                lim, used = live_independent()
                ls = out.strip().splitlines()
                f = fields(ls[0]) if len(ls) == 1 and ls[0].startswith("USERNS_RUNWAY ") else {}
                if rc in (0, 1) and f.get("limit") == lim and f.get("used_lb") == used:
                    live = "ok(limit=%s,used_lb=%s,state=%s)" % (lim, used, f.get("state"))
                    break
        if not live.startswith("ok"):
            fails.append("live")
        # (d) incident capture
        incident = "absent"
        if have_tool:
            rc, out = run([py, tool, "--journal", inc])
            summ = [l for l in out.splitlines() if l.startswith("SYSCTL_WRITES n=")]
            incident = "ok" if (rc == 1 and summ == ["SYSCTL_WRITES n=6 keys=1 userns_zero=2"]
                                and got_writes(out) == INCIDENT_WRITES
                                and "SYSCTL_WRITES_SETUP" not in out) else "fail(rc=%d)" % rc
        if incident != "ok":
            fails.append("incident")
        # (e) registry
        aud = os.path.join(root, "tools", "mori-gate-registry.py")
        rc, out = run([py, aud, "--rev", "WORK", "--repo", root, "--audit-all"], timeout=600)
        registry = "met" if "REGISTRY=met" in out else "unmet"
        if registry != "met":
            fails.append("registry")
        # (f) sourced knowledge
        sourced = "unmet"
        kp = os.path.join(root, KNOW)
        if os.path.isfile(kp):
            ids = set()
            for line in open(kp, errors="replace"):
                if re.match(r"^[-* ]*source *:", line):
                    ids.update(re.findall(r"\bS\d{3,}\b", line))
            rows = {}
            try:
                for line in open(os.path.join(root, "corpus", "SOURCES.md"), errors="replace"):
                    m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
                    if m:
                        rows[m.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")]
            except OSError:
                rows = {}
            hits = [sid for sid in sorted(ids)
                    if int(sid[1:]) > ENTERING_MAX_SID and sid in rows and len(rows[sid]) == 11
                    and rows[sid][7] == "mined"
                    and KNOW in [p.strip() for p in re.split(r"[,;]", rows[sid][10])]]
            if hits:
                sourced = "met(%s)" % ",".join(hits)
        if not sourced.startswith("met"):
            fails.append("sourced")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    met = not fails
    print("C1=%s cases_ok=%d/%d seed=%d selftest=%s live=%s incident=%s registry=%s sourced=%s checks_failed=%s"
          % ("met" if met else "unmet", ok_cases, total, seed, selftest, live, incident, registry, sourced,
             ",".join(fails) or "-"))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
