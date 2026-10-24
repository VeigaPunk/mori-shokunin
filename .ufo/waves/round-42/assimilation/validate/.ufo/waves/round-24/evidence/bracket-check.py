#!/usr/bin/env python3
"""Round-24 amendment A2 live bracket check for tools/mori-pressure.py (read-only).

Per run: read the raw /proc/pressure files, run the tool once, read the raw files again.
Pass when every reported total lies between the two raw totals of its kind, all four
resources are ok, irq some is null and system cpu full total is 0. Writes JSON to stdout.
"""
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = "/proc/pressure"
NAMES = ("cpu", "memory", "io", "irq")
LINE = re.compile(r"^(some|full) avg10=\S+ avg60=\S+ avg300=\S+ total=([0-9]+)$")


def raw():
    out = {}
    for name in NAMES:
        with open(os.path.join(ROOT, name), "r", encoding="utf-8") as fh:
            text = fh.read()
        kinds = {}
        for line in text.splitlines():
            m = LINE.match(line)
            if m:
                kinds[m.group(1)] = int(m.group(2))
        out[name] = {"text": text, "totals": kinds}
    return out


def one(tool):
    before = raw()
    proc = subprocess.run([sys.executable, "-I", tool], capture_output=True, text=True, timeout=30)
    after = raw()
    payload = json.loads(proc.stdout)
    problems = []
    for name in NAMES:
        res = payload["resources"][name]
        if res["state"] != "ok":
            problems.append("%s state %s" % (name, res["state"]))
            continue
        for kind in ("some", "full"):
            got = res.get(kind)
            lo = before[name]["totals"].get(kind)
            hi = after[name]["totals"].get(kind)
            if got is None:
                if lo is not None:
                    problems.append("%s.%s null but raw file has it" % (name, kind))
                continue
            if lo is None or hi is None or not (lo <= got["total"] <= hi):
                problems.append("%s.%s total %s outside [%s, %s]" % (name, kind, got["total"], lo, hi))
    if payload["resources"]["irq"].get("some") is not None:
        problems.append("irq some not null")
    if payload["resources"]["cpu"]["full"]["total"] != 0:
        problems.append("system cpu full total not 0")
    return {
        "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "tool_exit": proc.returncode,
        "verdict": payload.get("verdict"),
        "raw_before": {n: before[n]["totals"] for n in NAMES},
        "raw_after": {n: after[n]["totals"] for n in NAMES},
        "reported": {n: {k: (payload["resources"][n].get(k) or {}).get("total")
                         for k in ("some", "full")} for n in NAMES},
        "problems": problems,
        "pass": not problems,
    }


def main():
    tool = sys.argv[1]
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    results = [one(tool) for _ in range(runs)]
    passed = sum(1 for r in results if r["pass"])
    print(json.dumps({"schema": "mori-r24-bracket-check", "uname": os.uname().release,
                      "runs": runs, "passed": passed, "results": results}, indent=1))
    return 0 if passed == runs else 1


if __name__ == "__main__":
    sys.exit(main())
