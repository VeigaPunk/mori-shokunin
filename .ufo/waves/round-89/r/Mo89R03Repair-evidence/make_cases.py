#!/usr/bin/env python3
"""Mo89R03Repair: NEW binding cases (disjoint from the Mo89R01C1 battery) -> cases.json.

Shape {name, cmd, expect, why[, reach]}; bound path tools/mori-record-sweep.py.
expect is decided from bash 5.3 / CPython 3.14 semantics (why); `reach: header-unreachable`
marks cmds containing a newline, which a single `# cmd:` header line cannot carry.
"""
import json
import os
import sys

P = "tools/mori-record-sweep.py"
A = "--root . --pins .ufo/waves/round-82/record-pins.json"
LINE = "RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0"
BODY = "printf '%%s\\n' '%s'" % LINE
FAKEPY = "printf '%%s\\n' \"print('%s')\"" % LINE
PROD = "/home/vgpnk/Projects/shokunin/mori-shokunin/" + P
G = "python3 -I %s %s" % (P, A)

C = []


def case(name, cmd, expect, why, reach=None):
    row = {"name": name, "cmd": cmd, "expect": expect, "why": why}
    if reach:
        row["reach"] = reach
    C.append(row)


# ---- valid equivalents: bash runs CPython on the bound file with the same argv/cwd
case("N-E01-IB-combined", "python3 -IB %s %s" % (P, A), "met", "-IB = -I -B (CPython short flags combine)")
case("N-E02-X-dev", "python3 -X dev -I %s %s" % (P, A), "met", "-X takes the next word as its value; dev mode only adds warnings (stderr)")
case("N-E03-W-error-category", "python3 -W error::DeprecationWarning -I %s %s" % (P, A), "met", "-W value is the next word")
case("N-E04-timeout", "timeout 60 %s" % G, "met", "coreutils timeout DURATION COMMAND execs COMMAND")
case("N-E05-env-i-PATH", "env -i PATH=$PATH %s" % G, "met", "env -i clears env, PATH assignment, then execs python3")
case("N-E06-cd-dot-and", "cd . && %s" % G, "met", "cd . keeps cwd; && runs python on success")
case("N-E07-double-slash", "python3 -I ./tools//mori-record-sweep.py %s" % A, "met", "POSIX: // inside a path = /")
case("N-E08-PWD-absolute", "python3 -I \"$PWD/%s\" %s" % (P, A), "met", "$PWD is the replay cwd: same file")
case("N-E09-stderr-merge", "%s 2>&1" % G, "met", "redirect only; script runs")
case("N-E10-pipe-amp-cat", "%s |& cat" % G, "met", "|& pipes stdout+stderr to cat; script runs")
case("N-E11-subshell", "( %s )" % G, "met", "( list ) runs in a subshell, same cwd")
case("N-E12-brace-group", "{ %s; }" % G, "met", "{ list; } is a group command in the current shell")
case("N-E13-sh-c-string", "sh -c \"%s\"" % G, "met", "sh -c runs the string")
case("N-E14-escaped-path-chars", "python3 -I tools/mori\\-record\\-sweep.py %s" % A, "met", "backslash quotes '-'; word = tools/mori-record-sweep.py")
case("N-E15-eval", "eval '%s'" % G, "met", "eval re-parses and runs the string")
case("N-E16-stdbuf", "stdbuf -oL %s" % G, "met", "stdbuf execs COMMAND with buffering env")
case("N-E17-env-C-dot", "env -C . %s" % G, "met", "env -C . chdirs to the same dir")
case("N-E18-env-S", "env -S '%s'" % G, "met", "env -S splits the string into argv and execs it")
case("N-E19-nice-dashdash", "nice -n 0 -- %s" % G, "met", "GNU getopt: -- ends nice options, then COMMAND")
case("N-E20-setsid", "setsid -w %s" % G, "met", "setsid -w runs COMMAND in a new session and waits")
case("N-E21-sh-c-dollar0", "sh -c 'python3 -I \"$0\" %s' %s" % (A, P), "met", "the trailing word is $0 of the -c string; \"$0\" expands to the bound path")
case("N-E22-escaped-space-hash", "printf '%%s' x\\ #y >/dev/null; %s" % G, "met", "bash: '\\ ' is a quoted space, so # is mid-word, not a comment; printf goes to /dev/null")
case("N-E23-stdin-redirect", "%s </dev/null" % G, "met", "stdin redirect only")
case("N-E24-command-prefix", "command %s" % G, "met", "command NAME runs NAME bypassing functions")
case("N-E25-time-p", "time -p %s" % G, "met", "bash time keyword times the pipeline; report on stderr")
case("N-E26-Xdev-glued", "python3 -Xdev -I %s %s" % (P, A), "met", "-Xdev: value glued")
case("N-E27-ionice", "ionice -c 3 %s" % G, "met", "ionice -c CLASS COMMAND execs COMMAND")
case("N-E28-newline-separated", "true\n%s" % G, "met", "newline is a command terminator", "header-unreachable")
case("N-E29-line-continuation", "python3 -I \\\n%s %s" % (P, A), "met", "backslash-newline is removed (line continuation)", "header-unreachable")

# ---- counterfeits: the bound Python program is never run by CPython from the bound blob
case("N-A01-path-as-dollar0", "sh -c '%s' %s" % (BODY, P), "reject", "trailing word is only $0; the string prints the body")
case("N-A02-c-dashdash-data", "python3 -c \"print('%s')\" -- %s" % (LINE, P), "reject", "-c runs the string; later words are sys.argv")
case("N-A03-echo-path", "echo %s >/dev/null; %s" % (P, BODY), "reject", "echo prints the path")
case("N-A04-cat-path", "cat %s >/dev/null; %s" % (P, BODY), "reject", "cat reads, does not execute")
case("N-A05-m-runpy", "python3 -m runpy %s %s 2>/dev/null; %s" % (P, A, BODY), "reject", "runpy __main__ treats argv[1] as a MODULE name: 'tools/mori-record-sweep.py' -> ModuleNotFoundError")
case("N-A06-bash-n", "bash -n %s; %s" % (P, BODY), "reject", "-n: read commands, do not execute")
case("N-A07-bash-o-noexec", "bash -o noexec %s; %s" % (P, BODY), "reject", "-o noexec == -n: nothing executes")
case("N-A08-exit-before", "%s; exit; %s" % (BODY, G), "reject", "exit ends the shell before the python list member")
case("N-A09-or-short-circuit", "%s || %s" % (BODY, G), "reject", "|| runs the right side only when printf fails")
case("N-A10-false-and", "false && %s; %s" % (G, BODY), "reject", "&& after false skips python")
case("N-A11-function-shadow", "python3() { %s; }; %s" % (BODY, G), "reject", "a shell function named python3 shadows the binary: the body is printed, CPython never runs")
case("N-A12-hash-p", "hash -p /usr/bin/true python3; %s; %s" % (G, BODY), "reject", "hash -p binds the name python3 to /usr/bin/true")
case("N-A13-function-never-called", "f() ( %s ); %s" % (G, BODY), "reject", "f is defined, never called")
case("N-A14-set-n", "%s; set -n; %s" % (BODY, G), "reject", "set -n: subsequent commands are read, not executed")
case("N-A16-fake-python-PATH", "mkdir -p f && printf '#!/bin/sh\\n%s\\n' \"echo '%s'\" > f/python3 && chmod +x f/python3 && PATH=$PWD/f:$PATH %s" % ("%s", LINE, G), "reject", "PATH lookup finds f/python3, a sh script that echoes the body")
case("N-A17-fake-python-relative", "ln -s /usr/bin/true python3 && ./python3 -I %s %s && %s" % (P, A, BODY), "reject", "./python3 is a symlink to true")
case("N-A18-overwrite-bound", "%s > %s; %s" % (FAKEPY, P, G), "reject", "the bound path is overwritten before it runs: the executed file is not the bound blob")
case("N-A19-builtin-cd", "mkdir -p d/tools && %s > d/%s && builtin cd d && %s" % (FAKEPY, P, G), "reject", "builtin cd changes cwd; tools/... resolves to the fake d/tools/...")
case("N-A15-sitecustomize", "mkdir -p s && printf '%%s\\n' \"print('%s')\" 'import os, sys' 'sys.stdout.flush()' 'os._exit(0)' > s/sitecustomize.py && PYTHONPATH=s python3 %s %s" % (LINE, P, A), "reject", "without -I, site imports sitecustomize from PYTHONPATH, which prints the body and _exits 0 before the script runs")
case("N-A20-command-cd", "mkdir -p d/tools && %s > d/%s && command cd d && %s" % (FAKEPY, P, G), "reject", "command cd changes cwd")
case("N-A21-env-combined-C", "mkdir -p d/tools && %s > d/%s && env -iCd PATH=$PATH %s" % (FAKEPY, P, G), "reject", "GNU getopt: -iCd = -i -C d; python3 runs d/tools/... (fake)")
case("N-A22-env-combined-S", "env -iS\"python3 -c \\\"print('%s')\\\"\" %s" % (LINE, P), "reject", "-iS<string> = -i -S <string>: argv = python3 -c print(...) tools/...; the path is sys.argv data to -c")
case("N-A23-uv-run-module", "uv run --no-project -q -m %s %s 2>/dev/null; %s" % (P, A, BODY), "reject", "uv run -m X == python -m X: module-name lookup fails, the file never runs")
case("N-A24-uv-run-directory", "mkdir -p d/tools && %s > d/%s && uv run --no-project -q --directory d python3 -I %s %s" % (FAKEPY, P, P, A), "reject", "uv run --directory d changes cwd before running")
case("N-A25-prod-absolute", "python3 -I %s %s" % (PROD, A), "reject", "runs the production working tree file, outside the replay tree at <rev>; content is not tied to the bound blob")
case("N-A26-bash-runs-python-file", "bash %s 2>/dev/null; %s" % (P, BODY), "reject", "bash interprets the Python file as shell (arguable: not the bound program's semantics)")
case("N-A27-heredoc-data", "cat >/dev/null <<'X'\n;%s\nX\n%s" % (G, BODY), "reject", "heredoc lines are data", "header-unreachable")
case("N-A28-dollar-quoted-cd", "mkdir -p d/tools && %s > d/%s && $'cd' d && %s" % (FAKEPY, P, G), "reject", "$'cd' is ANSI-C quoting for cd")
case("N-A29-command-v", "command -v python3 %s >/dev/null; %s" % (P, BODY), "reject", "command -v only describes names")
case("N-A30-glued-hash", "%s '#'%s" % (BODY, P), "reject", "quoted '#' glued: data to printf")

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases.json")
names = [c["name"] for c in C]
assert len(names) == len(set(names))
json.dump(C, open(out, "w"), indent=1)
print("wrote %d cases (%d met, %d reject) -> %s" % (len(C), sum(c["expect"] == "met" for c in C),
                                                   sum(c["expect"] == "reject" for c in C), out))
