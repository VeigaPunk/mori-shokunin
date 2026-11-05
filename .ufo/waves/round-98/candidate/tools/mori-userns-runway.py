#!/usr/bin/env python3
"""mori-userns-runway — user-namespace runway read and sysctl-write event scan
(fleet and host observability lane; detection and report only).

Round 98 (C1, coverage + capability acquisition). Motivating incident
(prompt addendum, host incident 2026-11-05): wave seats set
`user.max_user_namespaces` to 0 via sudo (journal: `echo 0` at 05:14:52 and
05:22:02 -03, transient 10000/15638 writes); with the limit at 0 every bwrap
sandbox failed with ENOSPC until the orchestrator restored 122865. The lane
held no read of this resource and no detector for the writes.

Two read-only modes:

1. Runway read (default):
     python3 tools/mori-userns-runway.py [--proc DIR] [--low N] [--init-ino INO]
   reads DIR/sys/user/max_user_namespaces (the limit for the namespace the reader
   runs in) and the `ns/user` link of every numeric DIR/<pid> entry; prints
     USERNS_RUNWAY limit=L used_lb=U pids=P unreadable=X runway=R low=T state=S
   used_lb = distinct user namespaces other than the initial one (inode INO,
   default 4026531837 = PROC_USER_INIT_INO) seen on readable process links. It is
   a LOWER BOUND: namespaces held only by a bind mount or an open fd, and those
   behind unreadable links (other users' processes), are invisible here.
   runway = max(L - U, 0); state = exhausted when runway == 0 (a limit of 0
   included), low when runway < T (default 32), else ok.
   Exit 0 ok · 1 low/exhausted · 2 setup (limit file missing/unparsable, no
   numeric process entries).

2. Write-event scan:
     python3 tools/mori-userns-runway.py --journal FILE|-
     python3 tools/mori-userns-runway.py --journal-live --since TS --until TS
   reads sudo command lines in `journalctl -o short-iso` text (only lines carrying
   `sudo[` and ` COMMAND=`; other text that merely mentions /proc/sys is ignored)
   and prints one line per kernel-tunable write:
     SYSCTL_WRITE ts=T pid=N key=K value=V via=sysctl|sysctl-load|sh-echo|tee
   then
     SYSCTL_WRITES n=N keys=K userns_zero=Z
   Writes: `sysctl [-w] key=value ...` (one per key=value), `sysctl -p [FILE]` /
   `--load` / `--system` (key file:<path> or system, value -), a shell `-c` script
   with `echo V > /proc/sys/...` or `... | tee [-a] /proc/sys/...`, and a direct
   `tee /proc/sys/...`. Reads (`sysctl -a`, `sysctl key`, `cat /proc/sys/...`)
   are not writes. userns_zero counts writes setting user.max_user_namespaces to 0.
   Output carries fields only: no user name, PWD or command text (redaction
   posture); a value outside [A-Za-z0-9._:/-] or longer than 32 chars prints `?`.
   Exit 0 no write · 1 at least one write · 2 setup (unreadable input,
   journalctl failure).

  python3 tools/mori-userns-runway.py --selftest
   builds fixtures under a tempfile directory (honours TMPDIR; /tmp is never
   hardcoded), deletes them, prints `MORI_USERNS_RUNWAY_SELFTEST: PASS (N cases)`.

What it is NOT: never writes a sysctl, never creates a namespace, never
remediates (tsukuroi owns OS state, the operator owns host configuration).
Standard library only.
"""

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

INIT_USER_INO = 4026531837  # PROC_USER_INIT_INO = 0xEFFFFFFD (include/linux/proc_ns.h)
LINK_RE = re.compile(r"^user:\[(\d+)\]$")
SAFE_VALUE = re.compile(r"^[A-Za-z0-9._:/-]{1,32}$")
SHELLS = {"sh", "bash", "dash", "zsh", "ksh", "busybox"}
ECHO_RE = re.compile(r"echo\s+(?:-[ne]+\s+)?['\"]?([^\s'\"|;&>]+)['\"]?\s*>{1,2}\s*['\"]?/proc/sys/([^\s'\";&|]+)")
TEE_RE = re.compile(r"(?:echo\s+(?:-[ne]+\s+)?['\"]?([^\s'\"|;&>]+)['\"]?\s*\|\s*)?(?:\S*/)?tee\s+(?:-a\s+)?['\"]?/proc/sys/([^\s'\";&|]+)")
TS_PID_RE = re.compile(r"^(\S+)\s+\S+\s+sudo\[(\d+)\]:")


class Setup(Exception):
    pass


def clean_value(v):
    return v if SAFE_VALUE.match(v or "") else "?"


def proc_key(path):
    return path.strip("/").replace("/", ".")


# ---------------------------------------------------------------- runway

def read_runway(proc, low, init_ino):
    lim_path = os.path.join(proc, "sys", "user", "max_user_namespaces")
    try:
        with open(lim_path) as fh:
            raw = fh.read().strip()
    except OSError as e:
        raise Setup("limit unreadable: %s" % e.__class__.__name__)
    if not re.fullmatch(r"\d+", raw):
        raise Setup("limit unparsable")
    limit = int(raw)
    try:
        entries = os.listdir(proc)
    except OSError as e:
        raise Setup("proc unreadable: %s" % e.__class__.__name__)
    pids = [e for e in entries if e.isdigit()]
    if not pids:
        raise Setup("no numeric process entries")
    seen = set()
    unreadable = 0
    for p in pids:
        try:
            target = os.readlink(os.path.join(proc, p, "ns", "user"))
        except OSError:
            unreadable += 1
            continue
        m = LINK_RE.match(target)
        if not m:
            unreadable += 1
            continue
        ino = int(m.group(1))
        if ino != init_ino:
            seen.add(ino)
    used = len(seen)
    runway = max(limit - used, 0)
    if runway == 0:
        state = "exhausted"
    elif runway < low:
        state = "low"
    else:
        state = "ok"
    return {"limit": limit, "used_lb": used, "pids": len(pids), "unreadable": unreadable,
            "runway": runway, "low": low, "state": state}


def runway_line(r):
    return ("USERNS_RUNWAY limit=%(limit)d used_lb=%(used_lb)d pids=%(pids)d unreadable=%(unreadable)d "
            "runway=%(runway)d low=%(low)d state=%(state)s" % r)


# ---------------------------------------------------------------- journal

def split_cmd(cmd):
    try:
        return shlex.split(cmd)
    except ValueError:
        return cmd.split()


def classify(cmd):
    """Return a list of (key, value, via) writes for one sudo COMMAND string."""
    argv = split_cmd(cmd)
    if not argv:
        return []
    exe = os.path.basename(argv[0])
    writes = []
    if exe == "sysctl":
        args = argv[1:]
        i = 0
        while i < len(args):
            a = args[i]
            if a in ("-p", "--load") or a.startswith("--load="):
                if a.startswith("--load="):
                    f = a.split("=", 1)[1]
                elif i + 1 < len(args) and not args[i + 1].startswith("-"):
                    f = args[i + 1]
                    i += 1
                else:
                    f = "/etc/sysctl.conf"
                writes.append(("file:" + f, "-", "sysctl-load"))
            elif a == "--system":
                writes.append(("system", "-", "sysctl-load"))
            elif not a.startswith("-") and "=" in a:
                k, v = a.split("=", 1)
                writes.append((k.replace("/", "."), v, "sysctl"))
            i += 1
        return writes
    if exe in SHELLS:
        script = None
        for j, a in enumerate(argv[1:], 1):
            if a == "-c" and j + 1 < len(argv):
                script = " ".join(argv[j + 1:])
                break
        if script is None:
            return []
        for m in ECHO_RE.finditer(script):
            writes.append((proc_key(m.group(2)), m.group(1), "sh-echo"))
        for m in TEE_RE.finditer(script):
            writes.append((proc_key(m.group(2)), m.group(1) or "-", "tee"))
        return writes
    if exe == "tee":
        for a in argv[1:]:
            if a.startswith("/proc/sys/"):
                writes.append((proc_key(a[len("/proc/sys/"):]), "-", "tee"))
        return writes
    return []


def scan_journal(lines):
    out = []
    for line in lines:
        if "sudo[" not in line or " COMMAND=" not in line:
            continue
        m = TS_PID_RE.match(line)
        if not m:
            continue
        cmd = line.split(" COMMAND=", 1)[1].rstrip("\n")
        for key, value, via in classify(cmd):
            out.append({"ts": m.group(1), "pid": m.group(2), "key": key, "value": value, "via": via})
    return out


def journal_report(events):
    lines = []
    for e in events:
        lines.append("SYSCTL_WRITE ts=%s pid=%s key=%s value=%s via=%s" % (
            e["ts"], e["pid"], clean_value(e["key"]) if e["key"] != "system" else "system",
            clean_value(e["value"]) if e["value"] != "-" else "-", e["via"]))
    keys = len({e["key"] for e in events})
    zero = sum(1 for e in events if e["key"] == "user.max_user_namespaces" and e["value"] == "0")
    lines.append("SYSCTL_WRITES n=%d keys=%d userns_zero=%d" % (len(events), keys, zero))
    return lines, (1 if events else 0)


# ---------------------------------------------------------------- selftest

def _fake_proc(root, limit, links):
    """links: list of link targets (None = pid dir without an ns/user link)."""
    os.makedirs(os.path.join(root, "sys", "user"), exist_ok=True)
    if limit is not None:
        with open(os.path.join(root, "sys", "user", "max_user_namespaces"), "w") as fh:
            fh.write(limit)
    os.makedirs(os.path.join(root, "self"), exist_ok=True)
    for n, t in enumerate(links, 1):
        d = os.path.join(root, str(n), "ns")
        os.makedirs(d, exist_ok=True)
        if t is not None:
            os.symlink(t, os.path.join(d, "user"))


def selftest():
    base = tempfile.mkdtemp(prefix="mori-userns-selftest-")
    results = []
    I = "user:[4026531837]"

    def runway_case(name, limit, links, want, low=32):
        d = os.path.join(base, name)
        _fake_proc(d, limit, links)
        try:
            r = read_runway(d, low, INIT_USER_INO)
            got = (r["limit"], r["used_lb"], r["unreadable"], r["runway"], r["state"])
        except Setup:
            got = "setup"
        results.append((name, got == want, got, want))

    def journal_case(name, text, want):
        ev = scan_journal(text.splitlines())
        lines, rc = journal_report(ev)
        results.append((name, (lines[-1], rc) == want, (lines[-1], rc), want))

    try:
        runway_case("ok-distinct", "122865\n",
                    [I] * 4 + ["user:[4026533001]"] * 3 + ["user:[4026533002]", None, "net:[1]"],
                    (122865, 2, 2, 122863, "ok"))
        runway_case("limit-zero", "0\n", [I, I], (0, 0, 0, 0, "exhausted"))
        runway_case("full", "2", [I, "user:[11]", "user:[12]"], (2, 2, 0, 0, "exhausted"))
        runway_case("low", "40", [I] + ["user:[%d]" % (100 + k) for k in range(10)], (40, 10, 0, 30, "low"))
        runway_case("missing-limit", None, [I], "setup")
        runway_case("garbage-limit", "abc", [I], "setup")
        runway_case("no-pids", "10", [], "setup")
        J = ("2026-11-05T05:14:39-03:00 h sudo[11]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -a\n"
             "2026-11-05T05:14:52-03:00 h sudo[12]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'\n"
             "2026-11-05T05:14:54-03:00 h sudo[13]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=10000\n"
             "2026-11-05T05:15:00-03:00 h app[14]: note: COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'\n")
        journal_case("journal-incident", J, ("SYSCTL_WRITES n=2 keys=1 userns_zero=1", 1))
        J2 = ("T h sudo[1]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -w vm.swappiness=10 kernel.pid_max=4194304\n"
              "T h sudo[2]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 2 | tee /proc/sys/vm/overcommit_memory'\n"
              "T h sudo[3]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/cat /proc/sys/user/max_user_namespaces\n"
              "T h sudo[4]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl user.max_user_namespaces\n"
              "T h sudo[5]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -p /etc/sysctl.d/x.conf\n")
        journal_case("journal-forms", J2, ("SYSCTL_WRITES n=4 keys=4 userns_zero=0", 1))
        journal_case("journal-empty", "", ("SYSCTL_WRITES n=0 keys=0 userns_zero=0", 0))
        # redaction: a planted marker in the command never reaches the output
        J3 = "T h sudo[9]:    secretuser : PWD=/home/MARKERX ; USER=root ; COMMAND=/usr/bin/sysctl -w a.b=MARKERX$(id)\n"
        lines, _ = journal_report(scan_journal(J3.splitlines()))
        ok = all("MARKERX" not in l and "secretuser" not in l for l in lines) and "value=?" in lines[0]
        results.append(("redaction", ok, lines, "no marker"))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    fails = [r for r in results if not r[1]]
    for name, ok, got, want in results:
        print("case %s %s%s" % (name, "pass" if ok else "FAIL", "" if ok else " got=%r want=%r" % (got, want)))
    if fails:
        print("MORI_USERNS_RUNWAY_SELFTEST: FAIL (%d of %d cases)" % (len(fails), len(results)))
        return 1
    print("MORI_USERNS_RUNWAY_SELFTEST: PASS (%d cases)" % len(results))
    return 0


# ---------------------------------------------------------------- main

def main(argv):
    ap = argparse.ArgumentParser(description="user-namespace runway read and sysctl-write scan (read-only)")
    ap.add_argument("--proc", default="/proc")
    ap.add_argument("--low", type=int, default=32)
    ap.add_argument("--init-ino", type=int, default=INIT_USER_INO)
    ap.add_argument("--journal")
    ap.add_argument("--journal-live", action="store_true")
    ap.add_argument("--since")
    ap.add_argument("--until")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.journal or a.journal_live:
        try:
            if a.journal_live:
                if not (a.since and a.until):
                    raise Setup("--journal-live needs --since and --until")
                r = subprocess.run(["journalctl", "-o", "short-iso", "--no-pager", "--since", a.since,
                                    "--until", a.until], capture_output=True, text=True)
                if r.returncode != 0:
                    raise Setup("journalctl rc=%d" % r.returncode)
                text = r.stdout
            elif a.journal == "-":
                text = sys.stdin.read()
            else:
                with open(a.journal, errors="replace") as fh:
                    text = fh.read()
        except (OSError, Setup) as e:
            print("SYSCTL_WRITES_SETUP %s" % (e if isinstance(e, Setup) else e.__class__.__name__))
            return 2
        lines, rc = journal_report(scan_journal(text.splitlines()))
        print("\n".join(lines))
        return rc
    try:
        r = read_runway(a.proc, a.low, a.init_ino)
    except Setup as e:
        print("USERNS_RUNWAY_SETUP %s" % e)
        return 2
    print(runway_line(r))
    return 0 if r["state"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
