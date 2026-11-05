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
   reads sudo command lines in `journalctl -o short-iso` or default `-o short` text
   (only lines carrying `sudo[` and ` COMMAND=`; other text that merely mentions
   /proc/sys is ignored) and prints one line per kernel-tunable write:
     SYSCTL_WRITE ts=T pid=N key=K value=V via=sysctl|sysctl-load|sh-echo|sh-redirect|tee
   then
     SYSCTL_WRITES n=N keys=K userns_zero=Z
   Writes: `sysctl [-w] key=value ...` (one per key=value), `sysctl -p[FILE]` /
   `-p FILE` / `-f` / `--load[=FILE]` / `--system` (key file:<path> or system,
   value -), each also behind NAME=value or `env` prefixes; inside a shell `-c`
   script (tokenized round 99: quotes, comments, `;` `&&` `||` `|` and newlines
   as in POSIX XCU 2.2/2.3) any command whose output redirection `>`/`>>` targets
   /proc/sys/... (via sh-echo for echo/printf, value = its first argument, else
   sh-redirect, value -), `tee [-a] /proc/sys/...` (value piped from echo/printf),
   and nested `sysctl` or shell `-c` commands. Reads (`sysctl -a`, `sysctl key`,
   `sysctl -r/--pattern PATTERN`, `cat /proc/sys/...`) are not writes, nor is
   /proc/sys text inside quotes or a comment. userns_zero counts writes setting
   user.max_user_namespaces to 0.
   Output carries fields only: no user name, PWD or command text (redaction
   posture); a value outside [A-Za-z0-9._:/-] or longer than 32 chars prints `?`.
   Exit 0 no write · 1 at least one write · 2 setup (unreadable input,
   journalctl failure, or `SYSCTL_WRITES_SETUP unparsed=U` after the summary when
   U sudo COMMAND lines had an unknown timestamp shape or untokenizable quoting:
   the scan fails closed rather than reading them as "no write").

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
import shutil
import subprocess
import sys
import tempfile

INIT_USER_INO = 4026531837  # PROC_USER_INIT_INO = 0xEFFFFFFD (include/linux/proc_ns.h)
LINK_RE = re.compile(r"^user:\[(\d+)\]$")
SAFE_VALUE = re.compile(r"^[A-Za-z0-9._:/-]{1,32}$")
SHELLS = {"sh", "bash", "dash", "zsh", "ksh", "busybox"}
ECHOES = {"echo", "printf"}
# journalctl -o short-iso: `2026-11-05T05:14:52-03:00 host sudo[12]:`
TS_PID_RE = re.compile(r"^(\S+)\s+\S+\s+sudo\[(\d+)\]:")
# journalctl -o short (the default, classic syslog shape): `Nov 05 05:14:52 host sudo[12]:`
TS_SHORT_RE = re.compile(r"^([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d\d:\d\d:\d\d)\s+\S+\s+sudo\[(\d+)\]:")
OPS = ("&&", "||", ">>", ";", "&", "|", ">", "<", "\n")
SEPARATORS = {";", "&&", "||", "&", "\n"}


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

class Unparsed(Exception):
    """A sudo COMMAND whose logged argv or shell script cannot be tokenized."""


EXIT_SUFFIX_RE = re.compile(r" ; (?:SIGNAL|EXIT)=\S*(?: ; (?:SIGNAL|EXIT)=\S*)*$")


def unescape_cntrl(s):
    """Invert sudo's control-character escape `#0n` / `#0nn` / `#0nnn` (lib/util/lbuf.c
    escape(): 3 chars below 010, 4 below 0100, else 5). Only control values decode: sudo
    escapes nothing printable, so `#071` is a literal (limit: a literal `#0` followed by a
    digit in the original argument is indistinguishable from an escape and decodes)."""
    out, i, n = [], 0, len(s)
    while i < n:
        if s.startswith("#0", i):
            d = s[i + 2:i + 5]
            if d == "177":
                out.append("\x7f")
                i += 5
                continue
            if len(d) >= 2 and d[0] in "123" and d[1] in "01234567" and 0o10 <= int(d[:2], 8) < 0o40:
                out.append(chr(int(d[:2], 8)))
                i += 4
                continue
            if d[:1] and d[0] in "01234567":
                out.append(chr(int(d[0], 8)))
                i += 3
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def split_cmd(cmd):
    """Invert sudo's COMMAND= rendering (lib/eventlog/eventlog.c, sudo 1.9.17p2): the command
    path, then one space per argument; an argument containing a space is wrapped in single
    quotes, and `'` and `\\` are backslash-escaped in every argument; control characters are
    `#0nn` escapes. A trailing ` ; SIGNAL=..`/` ; EXIT=..` (exit events) is not argv."""
    cmd = EXIT_SUFFIX_RE.sub("", cmd)
    argv, i, n = [], 0, len(cmd)
    while i < n:
        if cmd[i] == " ":
            i += 1
            continue
        buf, quoted = [], cmd[i] == "'"
        if quoted:
            i += 1
        while i < n:
            c = cmd[i]
            if c == "\\" and i + 1 < n and cmd[i + 1] in "'\\":
                buf.append(cmd[i + 1])
                i += 2
                continue
            if quoted and c == "'":
                quoted = None
                i += 1
                break
            if not quoted and c == " ":
                break
            buf.append(c)
            i += 1
        if quoted:
            raise Unparsed("unterminated quoted argument")
        argv.append(unescape_cntrl("".join(buf)))
    return argv


def shell_tokens(script):
    """POSIX-shell token recognition, reduced to what the write classifier needs.

    Returns (kind, text, glued) triples: kind `w` (word, quotes removed) or `op`
    (one of OPS); glued is True when the token touches the previous one with no
    blank between (so `2>` is a file-descriptor redirection, not an argument 2).
    Quoted text is one word (XCU 2.2: single quotes keep every character
    literal), and `#` at the start of a word starts a comment that runs to the
    newline (XCU 2.3 token recognition, rule 9); inside a word it is literal.
    Raises Unparsed on an unterminated quote.
    """
    toks = []
    i, n = 0, len(script)
    word, in_word, glued = [], False, False

    def flush():
        nonlocal word, in_word
        if in_word:
            toks.append(("w", "".join(word), word_glued))
        word, in_word = [], False

    word_glued = False
    prev_blank = True
    while i < n:
        c = script[i]
        if c in " \t\r":
            flush()
            prev_blank = True
            i += 1
            continue
        op = next((o for o in OPS if script.startswith(o, i)), None)
        if op is not None:
            was_word = in_word
            flush()
            toks.append(("op", op, was_word or not prev_blank))
            prev_blank = op == "\n"
            i += len(op)
            continue
        if c == "#" and not in_word:
            j = script.find("\n", i)
            i = n if j < 0 else j
            continue
        if not in_word:
            in_word, word_glued = True, not prev_blank
        prev_blank = False
        if c == "'":
            j = script.find("'", i + 1)
            if j < 0:
                raise Unparsed("unterminated single quote")
            word.append(script[i + 1:j])
            i = j + 1
        elif c == '"':
            j = i + 1
            buf = []
            while j < n and script[j] != '"':
                if script[j] == "\\" and j + 1 < n and script[j + 1] in '"\\$`\n':
                    buf.append(script[j + 1])
                    j += 2
                    continue
                buf.append(script[j])
                j += 1
            if j >= n:
                raise Unparsed("unterminated double quote")
            word.append("".join(buf))
            i = j + 1
        elif c == "\\" and i + 1 < n:
            word.append(script[i + 1])
            i += 2
        else:
            word.append(c)
            i += 1
    flush()
    return toks


def unwrap(argv):
    """Drop leading NAME=value assignments and an `env [-opts] [NAME=value]...` prefix."""
    argv = list(argv)
    while True:
        while argv and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", argv[0]):
            argv.pop(0)
        if argv and os.path.basename(argv[0]) == "env":
            argv.pop(0)
            while argv and argv[0].startswith("-") and argv[0] != "-":
                argv.pop(0)
            continue
        return argv


def sysctl_writes(args):
    """procps sysctl(8): `-p[FILE]`/`--load[=FILE]` (`-f` alias) load a file, `--system`
    loads the system files, `-r PATTERN`/`--pattern PATTERN` is a filter argument (never a
    setting even when the regex holds `=`), a bare `key=value` is a write."""
    writes = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-r", "--pattern"):
            i += 2
            continue
        if a.startswith("--pattern="):
            i += 1
            continue
        if a in ("-p", "-f", "--load") or a.startswith("--load=") or (len(a) > 2 and a[:2] in ("-p", "-f")
                                                                      and not a.startswith("--")):
            if a.startswith("--load="):
                f = a.split("=", 1)[1]
            elif len(a) > 2 and not a.startswith("--"):
                f = a[2:]
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


def echo_value(argv):
    for a in argv[1:]:
        if os.path.basename(argv[0]) == "echo" and re.fullmatch(r"-[neE]+", a):
            continue
        return a
    return "-"


def command_writes(argv, redirs, prev_value, depth):
    """Writes of one simple command: its argv, its output redirections, the echo value piped in."""
    argv = unwrap(argv)
    writes = []
    exe = os.path.basename(argv[0]) if argv else ""
    value = echo_value(argv) if exe in ECHOES else "-"
    for target in redirs:
        if target.startswith("/proc/sys/"):
            writes.append((proc_key(target[len("/proc/sys/"):]), value,
                           "sh-echo" if exe in ECHOES else "sh-redirect"))
    if exe == "sysctl":
        writes += sysctl_writes(argv[1:])
    elif exe == "tee":
        for a in argv[1:]:
            if a.startswith("/proc/sys/"):
                writes.append((proc_key(a[len("/proc/sys/"):]), prev_value or "-", "tee"))
    elif exe in SHELLS and depth < 3:
        for j, a in enumerate(argv[1:], 1):
            if a == "-c" and j + 1 < len(argv):
                writes += script_writes(argv[j + 1], depth + 1)
                break
    return writes


def script_writes(script, depth=0):
    toks = shell_tokens(script)
    writes = []
    argv, redirs, prev_value = [], [], None
    k = 0

    def end_command():
        nonlocal argv, redirs
        out = command_writes(argv, redirs, prev_value, depth) if argv or redirs else []
        exe = os.path.basename(unwrap(argv)[0]) if unwrap(argv) else ""
        val = echo_value(unwrap(argv)) if exe in ECHOES else None
        argv, redirs = [], []
        return out, val

    while k < len(toks):
        kind, text, glued = toks[k]
        if kind == "w":
            argv.append(text)
        elif text in (">", ">>", "<"):
            if glued and argv and argv[-1].isdigit():
                argv.pop()  # `2>`: the digits name a file descriptor
            if k + 1 < len(toks) and toks[k + 1][0] == "w":
                if text != "<":
                    redirs.append(toks[k + 1][1])
                k += 1
        elif text == "|":
            out, val = end_command()
            writes += out
            prev_value = val
        elif text in SEPARATORS:
            out, _ = end_command()
            writes += out
            prev_value = None
        k += 1
    out, _ = end_command()
    writes += out
    return writes


def classify(cmd):
    """Return a list of (key, value, via) writes for one sudo COMMAND string.
    Raises Unparsed when the command or its shell script cannot be tokenized."""
    argv = split_cmd(cmd)
    if not argv:
        return []
    return command_writes(argv, [], None, 0)


def line_ts_pid(line):
    m = TS_PID_RE.match(line)
    if m:
        return m.group(1), m.group(2)
    s = TS_SHORT_RE.match(line)
    if s:
        return "%s-%02d_%s" % (s.group(1), int(s.group(2)), s.group(3)), s.group(4)
    return None


def scan_journal(lines):
    """Return (events, unparsed). A sudo COMMAND line whose timestamp shape is neither
    short-iso nor short, or whose command cannot be tokenized, is counted as unparsed:
    the scan fails closed instead of reading it as `no write`. sudo splits a log line
    longer than syslog_maxlen at a space and logs the rest as `user : (command continued)
    REST` under the same pid (eventlog.c do_syslog_sudo); those parts are joined back with
    one space before the command is read. A command whose quoted argument is still open at
    the end (a capture that dropped its continuation lines) is unparsed."""
    cmds = []          # [ts, pid, text]
    open_by_pid = {}
    unparsed = 0
    for line in lines:
        if "sudo[" not in line:
            continue
        cont = " : (command continued) " in line
        if not cont and " COMMAND=" not in line:
            continue
        tp = line_ts_pid(line)
        if tp is None:
            unparsed += 1
            continue
        ts, pid = tp
        if cont:
            rest = line.split(" : (command continued) ", 1)[1].rstrip("\n")
            if pid in open_by_pid:
                open_by_pid[pid][2] += " " + rest
            else:
                unparsed += 1  # a continuation whose first part is not in the input
            continue
        entry = [ts, pid, line.split(" COMMAND=", 1)[1].rstrip("\n")]
        cmds.append(entry)
        open_by_pid[pid] = entry
    out = []
    for ts, pid, cmd in cmds:
        if EXIT_SUFFIX_RE.search(cmd):
            continue  # an exit event repeats a command its accept event already logged
        try:
            found = classify(cmd)
        except Unparsed:
            unparsed += 1
            continue
        for key, value, via in found:
            out.append({"ts": ts, "pid": pid, "key": key, "value": value, "via": via})
    return out, unparsed


def journal_report(events, unparsed=0):
    lines = []
    for e in events:
        lines.append("SYSCTL_WRITE ts=%s pid=%s key=%s value=%s via=%s" % (
            e["ts"], e["pid"], clean_value(e["key"]) if e["key"] != "system" else "system",
            clean_value(e["value"]) if e["value"] != "-" else "-", e["via"]))
    keys = len({e["key"] for e in events})
    zero = sum(1 for e in events if e["key"] == "user.max_user_namespaces" and e["value"] == "0")
    lines.append("SYSCTL_WRITES n=%d keys=%d userns_zero=%d" % (len(events), keys, zero))
    if unparsed:
        lines.append("SYSCTL_WRITES_SETUP unparsed=%d" % unparsed)
        return lines, 2
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
        lines, rc = journal_report(*scan_journal(text.splitlines()))
        summary = [l for l in lines if l.startswith("SYSCTL_WRITES ")][0]
        results.append((name, (summary, rc) == want, (summary, rc), want))

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
        # round 99: reads and quoted/commented text are not writes (sysctl -r PATTERN, XCU 2.2/2.3)
        J4 = ("T h sudo[1]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -a -r 'user.max_user_namespaces=0'\n"
              "T h sudo[2]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl --pattern=a=b -a\n"
              "T h sudo[3]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo \"echo 0 > /proc/sys/user/max_user_namespaces\" > /dev/null'\n"
              "T h sudo[4]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/bash -c '# echo 0 > /proc/sys/user/max_user_namespaces'\n")
        journal_case("journal-not-writes", J4, ("SYSCTL_WRITES n=0 keys=0 userns_zero=0", 0))
        # round 99: writes the round-98 regexes missed (sysctl inside sh -c, env prefix, printf, sh-redirect, -pFILE)
        J5 = ("T h sudo[1]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'sysctl -w user.max_user_namespaces=0'\n"
              "T h sudo[2]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/env LC_ALL=C sysctl kernel.pid_max=99999\n"
              "T h sudo[3]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/bash -c 'printf 0 >> /proc/sys/vm/swappiness 2>/dev/null'\n"
              "T h sudo[4]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'cat /x > /proc/sys/vm/drop_caches; echo 1 | tee -a /proc/sys/vm/overcommit_memory'\n"
              "T h sudo[5]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -p/etc/sysctl.d/y.conf\n")
        journal_case("journal-more-writes", J5, ("SYSCTL_WRITES n=6 keys=6 userns_zero=1", 1))
        # round 99: the default `journalctl -o short` shape parses; an unknown shape fails closed
        J6 = "Nov 05 05:22:02 h sudo[7]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'\n"
        journal_case("journal-short-format", J6, ("SYSCTL_WRITES n=1 keys=1 userns_zero=1", 1))
        # round 99: sudo's own COMMAND= quoting (\' and #012 escapes) and an exit-event suffix
        J8 = ("T h sudo[1]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'printf \\'0\\' > /proc/sys/user/max_user_namespaces#012echo \\'#\\' done'\n"
              "T h sudo[2]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -a ; EXIT=0\n")
        journal_case("journal-sudo-escapes", J8, ("SYSCTL_WRITES n=1 keys=1 userns_zero=1", 1))
        # round 99: sudo's syslog_maxlen split, joined by pid; an orphan continuation and a
        # first part whose continuation is missing both fail closed
        J9 = ("T h sudo[31]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 >\n"
              "T h sudo[32]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -a\n"
              "T h sudo[31]:    u : (command continued) /proc/sys/user/max_user_namespaces'\n")
        journal_case("journal-continued", J9, ("SYSCTL_WRITES n=1 keys=1 userns_zero=1", 1))
        J10 = ("T h sudo[41]:    u : (command continued) /proc/sys/user/max_user_namespaces'\n"
               "T h sudo[42]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 >\n")
        journal_case("journal-continued-broken", J10, ("SYSCTL_WRITES n=0 keys=0 userns_zero=0", 2))
        J7 = ("Nov 5 05:22 h sudo[7]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sysctl -a\n"
              "x y z sudo[8]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'\n"
              "T h sudo[9]:    u : PWD=/x ; USER=root ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces\n")
        journal_case("journal-unparsed", J7, ("SYSCTL_WRITES n=0 keys=0 userns_zero=0", 2))
        runway_case("used-over-limit", "1", [I, "user:[21]", "user:[22]", "user:[23]"], (1, 3, 0, 0, "exhausted"))
        # redaction: a planted marker in the command never reaches the output
        J3 = "T h sudo[9]:    secretuser : PWD=/home/MARKERX ; USER=root ; COMMAND=/usr/bin/sysctl -w a.b=MARKERX$(id)\n"
        lines, _ = journal_report(*scan_journal(J3.splitlines()))
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
        lines, rc = journal_report(*scan_journal(text.splitlines()))
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
