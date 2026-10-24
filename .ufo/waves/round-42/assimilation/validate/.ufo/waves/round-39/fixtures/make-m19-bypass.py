#!/usr/bin/env python3
"""Round-39 C8 fixtures: build the two r38-M19 bypass counters from the r38
count-c1 bytes (r38 lesson M19).

  bypass-none.py  every drain is `communicate(timeout=UNBOUNDED_DRAIN_S)` with
                  `UNBOUNDED_DRAIN_S = None` (keyword name present, value hangs)
  bypass-wait.py  the drain is `proc.wait(timeout=timeout)` +
                  `proc.stdout.read()` (timeout parked on wait, pipe drained
                  by a read that never bounds)

Usage: make-m19-bypass.py <rev> <lane-repo> <out-dir>
The out dir receives bypass-none.py and bypass-wait.py plus the source they were
derived from (count-c1-r38.py).
"""
import os
import shutil
import subprocess
import sys

SRC_REL = ".ufo/waves/round-38/count-c1.py"


def main(argv):
    rev, repo, out = argv[1], os.path.abspath(argv[2]), os.path.abspath(argv[3])
    os.makedirs(out, exist_ok=True)
    proc = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, SRC_REL)],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise SystemExit("git show failed: %s" % proc.stderr)
    source = proc.stdout
    src_path = os.path.join(out, "count-c1-r38.py")
    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(source)

    # bypass A: name-not-value (r38 M19 bypass A)
    if "TOOL_GRACE_S = 5" not in source:
        raise SystemExit("anchor TOOL_GRACE_S absent")
    none_src = source.replace(
        "TOOL_GRACE_S = 5",
        "TOOL_GRACE_S = 5\nUNBOUNDED_DRAIN_S = None", 1)
    n_drains = none_src.count("proc.communicate(timeout=TOOL_GRACE_S)")
    if n_drains == 0:
        raise SystemExit("no TOOL_GRACE_S drains found")
    none_src = none_src.replace("proc.communicate(timeout=TOOL_GRACE_S)",
                                "proc.communicate(timeout=UNBOUNDED_DRAIN_S)")
    with open(os.path.join(out, "bypass-none.py"), "w", encoding="utf-8") as fh:
        fh.write(none_src)

    # bypass B: wait+read drain (r38 M19 bypass B) — the whole timeout block
    start_anchor = ("        out, err = proc.communicate(timeout=timeout)\n"
                    "    except subprocess.TimeoutExpired:")
    si = source.find(start_anchor)
    end_anchor = ('        raise ToolTimeout("tool exceeded %ds (SIGTERM, then SIGKILL after %ds)"\n'
                  '                          % (timeout, TOOL_GRACE_S))\n')
    ei = source.find(end_anchor)
    if si < 0 or ei < si:
        raise SystemExit("run() timeout block anchors absent")
    ei += len(end_anchor)
    wait_src = source[:si] + (
        "        proc.wait(timeout=timeout)\n"
        "        out, err = proc.stdout.read(), proc.stderr.read()\n"
        "    except subprocess.TimeoutExpired:\n"
        "        try:\n"
        "            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)\n"
        "        except OSError:\n"
        "            pass\n"
        "        try:\n"
        "            proc.wait(timeout=TOOL_GRACE_S)\n"
        "        except subprocess.TimeoutExpired:\n"
        "            try:\n"
        "                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)\n"
        "            except OSError:\n"
        "                pass\n"
        "        out, err = proc.stdout.read(), proc.stderr.read()\n"
        "        raise ToolTimeout(\"tool exceeded %ds (SIGTERM, then SIGKILL after %ds)\"\n"
        "                          % (timeout, TOOL_GRACE_S))\n"
    ) + source[ei:]
    with open(os.path.join(out, "bypass-wait.py"), "w", encoding="utf-8") as fh:
        fh.write(wait_src)

    print("derived %d drain(s) into bypass-none.py; bypass-wait.py from the "
          "primary communicate drain" % n_drains)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
