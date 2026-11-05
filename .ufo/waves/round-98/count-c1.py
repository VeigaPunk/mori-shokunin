#!/usr/bin/env python3
"""count-c1.py — mori round 98 C1 counter (coverage, capability acquisition).

Predicate P1 (same sentence as .ufo/waves/round-98/contract.md section C1): on the tree DIR of
revision R, (a) `tools/mori-userns-runway.py --selftest` exits 0 and its last line matches
`MORI_USERNS_RUNWAY_SELFTEST: PASS (<n> cases)`; (b) the tool answers every case of this
counter's frozen fixture battery (9 runway cases built here, 6 journal cases including the
committed incident capture) with the frozen exit code and summary fields; (c) a live run on
/proc exits 0 or 1 and reports the limit this counter reads itself from
/proc/sys/user/max_user_namespaces; (d) the lane's gate auditor
`tools/mori-gate-registry.py --rev WORK --repo DIR --audit-all` prints `REGISTRY=met`;
(e) `corpus/knowledge/userns-runway-r98.md` cites in a `source:` line at least one S-id whose
`corpus/SOURCES.md` row is `mined`, opened 2026-11-05 or later, and lists that knowledge path in
`used-by`; (f) one PROVINCE.md line names both `user namespace` and `tools/mori-userns-runway.py`.

Usage: python3 count-c1.py --root DIR [--work SCRATCH]
Label: C1=met (exit 0) / C1=unmet (exit 1); C1_SETUP (exit 2) when DIR or the pinned incident
capture is unusable. Standard library only; fixtures live under --work (default: a tempfile dir
honouring TMPDIR) and are deleted on exit.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/mori-userns-runway.py"
KNOW = "corpus/knowledge/userns-runway-r98.md"
INCIDENT = ".ufo/waves/round-98/evidence/journal-incident-r98.txt"
INCIDENT_SHA = "978504134c53a4a4b404bf5175b51aa31f5afd27ad62cd517e4a2fbc2cd79738"
I = "user:[4026531837]"

RUNWAY_CASES = [
    # name, limit file content (None = absent), link targets (None = pid dir without link), extra args,
    # expected rc, expected fields (None = setup line expected)
    ("F1-mixed", "122865\n", [I] * 6 + ["user:[4026533813]"] * 3 + ["user:[4026533741]"] * 2
     + ["user:[4026533750]", None, None, "mnt:[4026531841]"], [], 0,
     dict(limit="122865", used_lb="3", pids="15", unreadable="3", runway="122862", state="ok")),
    ("F2-limit-zero", "0\n", [I, I, I], [], 1,
     dict(limit="0", used_lb="0", runway="0", state="exhausted")),
    ("F3-full", "3\n", [I] + ["user:[%d]" % (500 + k) for k in range(3)], [], 1,
     dict(limit="3", used_lb="3", runway="0", state="exhausted")),
    ("F4-low", "50\n", [I] + ["user:[%d]" % (600 + k) for k in range(20)], [], 1,
     dict(limit="50", used_lb="20", runway="30", state="low")),
    ("F5-boundary", "50\n", [I] + ["user:[%d]" % (700 + k) for k in range(18)], [], 0,
     dict(limit="50", used_lb="18", runway="32", state="ok")),
    ("F6-missing-limit", None, [I], [], 2, None),
    ("F7-bad-limit", "-1\n", [I], [], 2, None),
    ("F8-low-flag", "10\n", [I] + ["user:[%d]" % (800 + k) for k in range(6)], ["--low", "5"], 1,
     dict(limit="10", used_lb="6", runway="4", low="5", state="low")),
    ("F9-nonpid", "100\n", [I, "user:[900]"], [], 0,
     dict(limit="100", used_lb="1", pids="2", runway="99", state="ok")),
]

J2 = (
    "2026-11-05T10:00:00-03:00 h sudo[101]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/sysctl --system\n"
    "2026-11-05T10:00:01-03:00 h sudo[102]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 1 >> /proc/sys/kernel/sysrq'\n"
    "2026-11-05T10:00:02-03:00 h sudo[103]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/bash -c 'echo 65536 | tee -a /proc/sys/fs/inotify/max_user_watches'\n"
    "2026-11-05T10:00:03-03:00 h sudo[104]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/tee /proc/sys/vm/drop_caches\n"
    "2026-11-05T10:00:04-03:00 h sudo[105]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/sysctl -n kernel.pid_max\n"
    "2026-11-05T10:00:05-03:00 h sudo[106]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/sysctl -a\n"
    "2026-11-05T10:00:06-03:00 h sudo[107]:    u : PWD=/w ; USER=root ; COMMAND=/usr/bin/cat /proc/sys/vm/overcommit_memory\n"
    "2026-11-05T10:00:07-03:00 h systemd[1]: Started sudo[108] COMMAND=/usr/bin/sysctl -w x.y=1\n"
)
J3 = ("2026-11-05T11:00:00-03:00 h sudo[201]:    u : PWD=/w ; USER=root ; "
      "COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=0 user.max_net_namespaces=0\n")
J6 = ("2026-11-05T12:00:00-03:00 h sudo[301]:    zzsecretuser : PWD=/home/QQMARKER ; USER=root ; "
      "COMMAND=/usr/bin/sysctl -w kernel.domainname=hostx\n")

INCIDENT_WRITES = [
    ("2026-11-05T05:14:52-03:00", "0"), ("2026-11-05T05:14:54-03:00", "10000"),
    ("2026-11-05T05:16:04-03:00", "15638"), ("2026-11-05T05:16:04-03:00", "15638"),
    ("2026-11-05T05:22:02-03:00", "0"), ("2026-11-05T05:42:18-03:00", "122865"),
]


def fields(line):
    return dict(kv.split("=", 1) for kv in line.split()[1:] if "=" in kv)


def run(argv, stdin=None, timeout=300):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, input=stdin, timeout=timeout)
        return r.returncode, r.stdout
    except (subprocess.TimeoutExpired, OSError) as e:
        return -1, "ERR %s" % e.__class__.__name__


def build_proc(d, limit, links):
    os.makedirs(os.path.join(d, "sys", "user"))
    if limit is not None:
        with open(os.path.join(d, "sys", "user", "max_user_namespaces"), "w") as fh:
            fh.write(limit)
    for extra in ("self", "net", "123abc"):
        os.makedirs(os.path.join(d, extra, "ns"))
    os.symlink("user:[4026533999]", os.path.join(d, "self", "ns", "user"))
    os.symlink("user:[4026533998]", os.path.join(d, "123abc", "ns", "user"))
    for n, t in enumerate(links, 1):
        nd = os.path.join(d, str(1000 + n), "ns")
        os.makedirs(nd)
        if t is not None:
            os.symlink(t, os.path.join(nd, "user"))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("C1_SETUP root not a directory")
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    inc = os.path.join(here, "evidence", "journal-incident-r98.txt")
    if not os.path.isfile(inc):
        inc = os.path.join(root, INCIDENT)
    try:
        inc_bytes = open(inc, "rb").read()
    except OSError:
        print("C1_SETUP incident capture unreadable")
        return 2
    if hashlib.sha256(inc_bytes).hexdigest() != INCIDENT_SHA:
        print("C1_SETUP incident capture sha256 differs from the frozen pin")
        return 2
    work = tempfile.mkdtemp(prefix="count-c1-r98-", dir=a.work)
    fails = []
    ok_cases = 0
    total = len(RUNWAY_CASES) + 6
    tool = os.path.join(root, TOOL)
    have_tool = os.path.isfile(tool)
    py = sys.executable
    try:
        # (a) selftest
        if have_tool:
            rc, out = run([py, tool, "--selftest"])
            last = out.strip().splitlines()[-1] if out.strip() else ""
            selftest = "ok" if rc == 0 and re.fullmatch(r"MORI_USERNS_RUNWAY_SELFTEST: PASS \(\d+ cases\)", last) else "fail"
        else:
            selftest = "absent"
        if selftest != "ok":
            fails.append("selftest")
        # (b) runway battery
        for name, limit, links, extra, want_rc, want in RUNWAY_CASES:
            if not have_tool:
                continue
            d = os.path.join(work, name)
            build_proc(d, limit, links)
            rc, out = run([py, tool, "--proc", d] + extra)
            lines = out.strip().splitlines()
            good = rc == want_rc and len(lines) == 1
            if good and want is None:
                good = lines[0].startswith("USERNS_RUNWAY_SETUP")
            elif good:
                f = fields(lines[0]) if lines[0].startswith("USERNS_RUNWAY ") else {}
                good = all(f.get(k) == v for k, v in want.items())
            if good:
                ok_cases += 1
            else:
                fails.append("case_" + name)
        # (b) journal battery
        jcases = []
        jcases.append(("J1-incident", ["--journal", inc], None, 1, "SYSCTL_WRITES n=6 keys=1 userns_zero=2"))
        p2 = os.path.join(work, "j2.txt"); open(p2, "w").write(J2)
        jcases.append(("J2-forms", ["--journal", p2], None, 1, "SYSCTL_WRITES n=4 keys=4 userns_zero=0"))
        jcases.append(("J3-two-keys", ["--journal", "-"], J3, 1, "SYSCTL_WRITES n=2 keys=2 userns_zero=1"))
        p4 = os.path.join(work, "j4.txt"); open(p4, "w").write("")
        jcases.append(("J4-empty", ["--journal", p4], None, 0, "SYSCTL_WRITES n=0 keys=0 userns_zero=0"))
        jcases.append(("J5-unreadable", ["--journal", os.path.join(work, "absent.txt")], None, 2, None))
        p6 = os.path.join(work, "j6.txt"); open(p6, "w").write(J6)
        jcases.append(("J6-redaction", ["--journal", p6], None, 1, "SYSCTL_WRITES n=1 keys=1 userns_zero=0"))
        for name, args, stdin, want_rc, want_last in jcases:
            if not have_tool:
                continue
            rc, out = run([py, tool] + args, stdin=stdin)
            lines = out.strip().splitlines()
            good = rc == want_rc and bool(lines)
            if good and want_last is None:
                good = len(lines) == 1 and lines[0].startswith("SYSCTL_WRITES_SETUP")
            elif good:
                good = lines[-1] == want_last
                if good and name == "J1-incident":
                    got = [(fields(l).get("ts"), fields(l).get("value")) for l in lines[:-1]]
                    good = (got == INCIDENT_WRITES and all(fields(l).get("key") == "user.max_user_namespaces"
                                                           for l in lines[:-1]))
                if good and name == "J6-redaction":
                    good = "QQMARKER" not in out and "zzsecretuser" not in out
            if good:
                ok_cases += 1
            else:
                fails.append("case_" + name)
        # (c) live
        live = "absent"
        if have_tool:
            try:
                host_limit = open("/proc/sys/user/max_user_namespaces").read().strip()
            except OSError:
                host_limit = None
            rc, out = run([py, tool])
            lines = out.strip().splitlines()
            f = fields(lines[0]) if len(lines) == 1 and lines[0].startswith("USERNS_RUNWAY ") else {}
            live = "ok" if (rc in (0, 1) and host_limit is not None and f.get("limit") == host_limit) else "fail"
            if live == "ok":
                live = "ok(limit=%s,used_lb=%s,state=%s)" % (f.get("limit"), f.get("used_lb"), f.get("state"))
        if not live.startswith("ok"):
            fails.append("live")
        # (d) registry
        aud = os.path.join(root, "tools", "mori-gate-registry.py")
        rc, out = run([py, aud, "--rev", "WORK", "--repo", root, "--audit-all"], timeout=600)
        registry = "met" if "REGISTRY=met" in out else "unmet"
        if registry != "met":
            fails.append("registry")
        # (e) sourced knowledge
        sourced = "unmet"
        kp = os.path.join(root, KNOW)
        if os.path.isfile(kp):
            text = open(kp, errors="replace").read()
            ids = set()
            for line in text.splitlines():
                if re.match(r"^[-* ]*source *:", line):
                    ids.update(re.findall(r"\bS\d{3,}\b", line))
            rows = {}
            try:
                for line in open(os.path.join(root, "corpus", "SOURCES.md"), errors="replace"):
                    m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
                    if m:
                        cells = [c.strip() for c in line.strip().strip("|").split("|")]
                        rows[m.group(1)] = cells
            except OSError:
                rows = {}
            hits = []
            for sid in sorted(ids):
                c = rows.get(sid)
                if c and len(c) == 11 and c[7] == "mined" and c[8] >= "2026-11-05" \
                        and KNOW in [p.strip() for p in re.split(r"[,;]", c[10])]:
                    hits.append(sid)
            if hits:
                sourced = "met(%s)" % ",".join(hits)
        if not sourced.startswith("met"):
            fails.append("sourced")
        # (f) province
        province = "unmet"
        try:
            for line in open(os.path.join(root, "PROVINCE.md"), errors="replace"):
                if "user namespace" in line.lower() and "tools/mori-userns-runway.py" in line:
                    province = "met"
                    break
        except OSError:
            pass
        if province != "met":
            fails.append("province")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    met = not fails
    print("C1=%s cases_ok=%d/%d selftest=%s live=%s registry=%s sourced=%s province=%s checks_failed=%s root=%s"
          % ("met" if met else "unmet", ok_cases, total, selftest, live, registry, sourced, province,
             ",".join(fails) or "-", root))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
