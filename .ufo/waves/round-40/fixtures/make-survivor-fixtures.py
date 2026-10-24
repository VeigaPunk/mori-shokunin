#!/usr/bin/env python3
"""Build the round-40 C1 survivor fixtures from the count-c8 counter bytes.

Each fixture is the honest counter of record with one r39-w1 finding class
re-applied (RevC8Value H1/H2/M3/L4, RevC8Drain F1/F2/F3). The round-39
checker bytes accept every one of them (before receipts); the round-40
checker must reject each with the named new check.

Usage: make-survivor-fixtures.py <counter.py> <outdir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def anchored(source, anchor, old, new, count=1):
    """Replace `old` with `new` at the first occurrence AFTER `anchor`."""
    index = source.find(anchor)
    if index < 0:
        raise SystemExit("anchor absent: %r" % anchor)
    head, tail = source[:index], source[index:]
    if tail.count(old) < count:
        raise SystemExit("edit target %r absent after anchor %r" % (old, anchor))
    return head + tail.replace(old, new, count)


RUN_DEF = "def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):"
RUN_COMM = "        out, err = proc.communicate(timeout=timeout)\n"
TOOL_DEF = "def run_tool(tool, args, timeout=TOOL_TIMEOUT_S):"
GIT_TIMEOUT = "GIT_TIMEOUT_S = 120\n"


def build(source):
    fixtures = {}

    # H1: function-local shadow, runtime None (RevC8Value counter-shadow-none)
    s = anchored(source, GIT_TIMEOUT, GIT_TIMEOUT,
                 GIT_TIMEOUT + "TIMEOUT = 120\n")
    s = anchored(s, RUN_DEF, RUN_COMM,
                 "        TIMEOUT = None\n"
                 "        out, err = proc.communicate(timeout=TIMEOUT)\n")
    fixtures["shadow-none"] = s

    # H1b: function-local shadow, runtime -1
    s = anchored(source, GIT_TIMEOUT, GIT_TIMEOUT,
                 GIT_TIMEOUT + "TIMEOUT = 120\n")
    s = anchored(s, RUN_DEF, RUN_COMM,
                 "        TIMEOUT = -1\n"
                 "        out, err = proc.communicate(timeout=TIMEOUT)\n")
    fixtures["shadow-neg"] = s

    # H2: module-level conditional rebind (RevC8Value counter-cond)
    s = anchored(source, GIT_TIMEOUT, GIT_TIMEOUT,
                 GIT_TIMEOUT + 'NAME = 120\n'
                 'if os.environ.get("MORI_TIMEOUT_UNBOUNDED"):\n'
                 "    NAME = None\n")
    s = anchored(s, RUN_DEF,
                 "def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):",
                 "def run(cmd, cwd=None, timeout=NAME, env=None):")
    fixtures["cond"] = s

    # M3: non-finite literal
    s = anchored(source, GIT_TIMEOUT, GIT_TIMEOUT,
                 GIT_TIMEOUT + "NAME = 1e400\n")
    s = anchored(s, RUN_DEF,
                 "def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):",
                 "def run(cmd, cwd=None, timeout=NAME, env=None):")
    fixtures["inf"] = s

    # L4: fold crash (ZeroDivisionError at fold time)
    s = anchored(source, GIT_TIMEOUT, GIT_TIMEOUT,
                 GIT_TIMEOUT + "NAME = 1/0\n")
    s = anchored(s, RUN_DEF,
                 "def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):",
                 "def run(cmd, cwd=None, timeout=NAME, env=None):")
    fixtures["divzero"] = s

    # F1: M19-B wait+read drain beside a decoy used communicate (RevC8Drain E2)
    s = anchored(source, TOOL_DEF, RUN_COMM,
                 "        dummy = subprocess.Popen([sys.executable, \"-c\", "
                 "\"pass\"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n"
                 "        dummy_out, dummy_err = dummy.communicate(timeout=timeout)\n"
                 "        proc.wait(timeout=timeout)\n"
                 "        out, err = proc.stdout.read(), proc.stderr.read()\n")
    fixtures["decoy"] = s

    # F2a: communicate result assigned to `_` (RevC8Drain C2)
    s = anchored(source, TOOL_DEF, RUN_COMM,
                 "        _ = proc.communicate(timeout=timeout)\n"
                 "        out, err = proc.stdout, proc.stderr\n")
    fixtures["underscore"] = s

    # F2b: communicate result wrapped in a discarded tuple (RevC8Drain C)
    s = anchored(source, TOOL_DEF, RUN_COMM,
                 "        (proc.communicate(timeout=timeout), None)\n"
                 "        out, err = proc.stdout, proc.stderr\n")
    fixtures["tuple"] = s

    # F3: an undrained second Popen in the same function (RevC8Drain E)
    s = anchored(source, TOOL_DEF,
                 "    proc = subprocess.Popen([sys.executable, tool] + list(args),",
                 "    leftover = subprocess.Popen([sys.executable, \"-c\", "
                 "\"import time; time.sleep(5)\"], stdout=subprocess.PIPE,"
                 " stderr=subprocess.PIPE)\n"
                 "    proc = subprocess.Popen([sys.executable, tool] + list(args),")
    fixtures["second-popen"] = s

    # multi-counter control: communicate without any timeout (conjunct probe)
    s = anchored(source, TOOL_DEF, RUN_COMM,
                 "        out, err = proc.communicate()\n")
    fixtures["barecomm"] = s

    return fixtures


def main(argv):
    counter, outdir = argv[1], argv[2]
    source = open(counter, encoding="utf-8").read()
    os.makedirs(outdir, exist_ok=True)
    for name, text in sorted(build(source).items()):
        path = os.path.join(outdir, "survivor-%s.py" % name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        print("wrote %s (%d bytes)" % (path, len(text)))


if __name__ == "__main__":
    main(sys.argv)
