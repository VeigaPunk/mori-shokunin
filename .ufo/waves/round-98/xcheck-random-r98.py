#!/usr/bin/env python3
"""xcheck-random-r98.py — POST-HOC supplementary check, written after the w1 critic Mo98CritC1 showed that a
fixture-shape lookup stub passes the frozen count-c1.py. NOT the C1 counter, not part of the frozen predicate;
it changes no claim. It generates fixtures the tool has never seen (seeded, seed printed) and computes the
expected answer independently, so a lookup keyed on the frozen fixtures cannot pass.

Usage: python3 xcheck-random-r98.py TOOL [--seed N] [--cases N] [--work DIR]
Prints `XCHECK seed=S proc_ok=a/n journal_ok=b/m` and exits 0 only when every case matches.
"""
import argparse, os, random, shutil, subprocess, sys, tempfile

INIT = 4026531837


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("tool"); ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--cases", type=int, default=40); ap.add_argument("--work")
    a = ap.parse_args(argv)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1 << 30)
    rnd = random.Random(seed)
    work = tempfile.mkdtemp(prefix="xcheck-r98-", dir=a.work)
    pok = jok = 0
    try:
        for i in range(a.cases):
            d = os.path.join(work, "p%d" % i)
            os.makedirs(os.path.join(d, "sys", "user"))
            limit = rnd.choice([0, rnd.randint(1, 60), rnd.randint(100, 300000)])
            open(os.path.join(d, "sys", "user", "max_user_namespaces"), "w").write("%d\n" % limit)
            pool = [rnd.randint(4026532000, 4026599999) for _ in range(rnd.randint(1, 40))]
            used, unread, n = set(), 0, rnd.randint(1, 80)
            for k in range(n):
                nd = os.path.join(d, str(rnd.randint(1, 10**6) * 100 + k), "ns"); os.makedirs(nd)
                c = rnd.random()
                if c < 0.3:
                    t = "user:[%d]" % INIT
                elif c < 0.85:
                    ino = rnd.choice(pool); used.add(ino); t = "user:[%d]" % ino
                elif c < 0.93:
                    t = None; unread += 1
                else:
                    t = "net:[%d]" % rnd.randint(1, 9999); unread += 1
                if t: os.symlink(t, os.path.join(nd, "user"))
            low = rnd.choice([32, rnd.randint(1, 100)])
            runway = max(limit - len(used), 0)
            state = "exhausted" if runway == 0 else ("low" if runway < low else "ok")
            want = "USERNS_RUNWAY limit=%d used_lb=%d pids=%d unreadable=%d runway=%d low=%d state=%s" % (
                limit, len(used), n, unread, runway, low, state)
            r = subprocess.run([sys.executable, a.tool, "--proc", d, "--low", str(low)], capture_output=True, text=True)
            if r.stdout.strip() == want and r.returncode == (0 if state == "ok" else 1):
                pok += 1
        for i in range(a.cases):
            lines, writes, zero, keys = [], 0, 0, set()
            for k in range(rnd.randint(0, 12)):
                key = rnd.choice(["user.max_user_namespaces", "vm.swappiness", "kernel.pid_max", "fs.file_max"])
                val = str(rnd.choice([0, rnd.randint(1, 999999)]))
                form = rnd.randint(0, 4)
                ts = "2026-11-%02dT%02d:%02d:00-03:00" % (rnd.randint(1, 28), rnd.randint(0, 23), rnd.randint(0, 59))
                pre = "%s h sudo[%d]:    u : PWD=/w ; USER=root ; COMMAND=" % (ts, rnd.randint(2, 99999))
                if form == 0:
                    lines.append(pre + "/usr/bin/sysctl -w %s=%s" % (key, val)); w = True
                elif form == 1:
                    lines.append(pre + "/usr/bin/sh -c 'echo %s > /proc/sys/%s'" % (val, key.replace(".", "/"))); w = True
                elif form == 2:
                    lines.append(pre + "/usr/bin/sysctl %s" % key); w = False
                elif form == 3:
                    lines.append(pre + "/usr/bin/cat /proc/sys/%s" % key.replace(".", "/")); w = False
                else:
                    lines.append("%s h app[7]: COMMAND=/usr/bin/sysctl -w %s=%s" % (ts, key, val)); w = False
                if w:
                    writes += 1; keys.add(key)
                    zero += key == "user.max_user_namespaces" and val == "0"
            want = "SYSCTL_WRITES n=%d keys=%d userns_zero=%d" % (writes, len(keys), zero)
            r = subprocess.run([sys.executable, a.tool, "--journal", "-"], input="\n".join(lines) + "\n",
                               capture_output=True, text=True)
            out = r.stdout.strip().splitlines()
            if out and out[-1] == want and len(out) == writes + 1 and r.returncode == (1 if writes else 0):
                jok += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("XCHECK seed=%d proc_ok=%d/%d journal_ok=%d/%d" % (seed, pok, a.cases, jok, a.cases))
    return 0 if pok == jok == a.cases else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
