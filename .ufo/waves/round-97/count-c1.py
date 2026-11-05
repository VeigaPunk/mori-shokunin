#!/usr/bin/env python3
"""mori round 97 -- frozen C1 (operability) counter.

Predicate P1 (same sentence as .ufo/waves/round-97/contract.md, C1):
  On the tree DIR (a `git archive` of the measured revision),
  (a) `python3 tools/mori-gate-registry.py --rev WORK --repo DIR --audit-all` prints
      `REGISTRY=met` (registered=all, unregistered=0 no_selftest=0 duplicate=0 wrong_row=0);
  (b) for each of the four tools below, the registry row the auditor attributes to it has a
      `self-test` cell that contains, verbatim, the final stdout line the tool's own
      `--selftest` prints when run from DIR now, and that selftest exits 0 (a checklist item
      that runs and produces its stated outcome);
  (c) that row's `verdict map` cell contains the tool's frozen verdict token below.

Usage: count-c1.py --root DIR
Output: per-target lines, then
  C1=met|unmet unregistered=<u> registry=<met|unmet> targets_ok=<k>/4 checks_failed=<list|-> root=<DIR>
Exit 0 met, 1 unmet, 2 setup. Standard library only; selftests honour TMPDIR.
"""
import argparse
import os
import re
import subprocess
import sys

TARGETS = {
    "tools/mori-cgroup-pressure.py": "MORI_CGROUP_PRESSURE",
    "tools/mori-drift-recheck.py": "MORI_DRIFT_RECHECK",
    "tools/mori-scorecard-calibration.py": "C1=met",
    "tools/mori-source-digest.py": "DIGEST_CHECK",
}
HEADER = ["name", "kind", "entry", "verdict map", "self-test", "pinned values", "write scope", "owner"]


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [c.strip() for c in s[1:-1].split("|")]


def registry_rows(path):
    rows = {}
    in_table = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            c = cells(line)
            if c is None:
                in_table = False
                continue
            if c == HEADER:
                in_table = True
                continue
            if in_table and c and not set("".join(c)) <= set("-: "):
                rows.setdefault(c[0], []).append(c)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    aud = os.path.join(root, "tools", "mori-gate-registry.py")
    skill = os.path.join(root, "SKILL.md")
    for p in (aud, skill):
        if not os.path.isfile(p):
            print("C1_SETUP missing " + p)
            return 2
    r = subprocess.run([sys.executable, aud, "--rev", "WORK", "--repo", root, "--audit-all"],
                       capture_output=True, text=True, cwd=root, timeout=600)
    if r.returncode == 2:
        print("C1_SETUP auditor rc=2: " + (r.stdout + r.stderr).strip()[-300:])
        return 2
    out = r.stdout.splitlines()
    regline = [l for l in out if l.startswith("registered=")]
    if len(regline) != 1:
        print("C1_SETUP no counter line")
        return 2
    f = dict(kv.split("=", 1) for kv in regline[0].split())
    registry = "met" if "REGISTRY=met" in out else "unmet"
    failed = [] if registry == "met" else ["registry"]
    rows = registry_rows(skill)
    ok_n = 0
    for path, token in TARGETS.items():
        al = [l for l in out if re.match(r"^audit %s\s" % re.escape(path), l)]
        m = re.search(r"PASS row='(.*)' \(", al[0]) if len(al) == 1 else None
        if not m:
            print("TARGET %s unattributed" % path)
            failed.append("target_" + os.path.basename(path))
            continue
        name = m.group(1)
        cand = rows.get(name, [])
        if len(cand) != 1 or len(cand[0]) != 8:
            print("TARGET %s row=%r rows_found=%d" % (path, name, len(cand)))
            failed.append("target_" + os.path.basename(path))
            continue
        row = cand[0]
        st = subprocess.run([sys.executable, os.path.join(root, path), "--selftest"],
                            capture_output=True, text=True, cwd=root, timeout=900)
        last = [l for l in st.stdout.splitlines() if l.strip()]
        last = last[-1].strip() if last else ""
        stated = bool(last) and last in row[4]
        verdict = token in row[3]
        good = st.returncode == 0 and stated and verdict
        print("TARGET %s row=%r selftest_rc=%d selftest_line=%r stated_in_cell=%s token_in_verdict_map=%s" % (
            path, name, st.returncode, last, "yes" if stated else "no", "yes" if verdict else "no"))
        if good:
            ok_n += 1
        else:
            failed.append("target_" + os.path.basename(path))
    met = not failed
    print("C1=%s unregistered=%s registry=%s targets_ok=%d/4 checks_failed=%s root=%s" % (
        "met" if met else "unmet", f.get("unregistered", "?"), registry, ok_n,
        ",".join(failed) if failed else "-", root))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
