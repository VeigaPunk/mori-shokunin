#!/usr/bin/env python3
"""Round 50 C2 controls, scored with the frozen count-c2.py evaluate() over an overlay reader:
the entering revision's bytes, with the frozen source copies taken from the working tree (they are
committed in the freeze commit) and, per control, one file replaced.

Usage: c2-controls.py <entering-rev>
  do-nothing      entering bytes + the copies                                       unmet (entry_absent)
  staged-r46      staged scope-charge-fields-r46.md byte-exact at the entry path     unmet
  staged-r47      staged scope-composition-in-the-block-r47.md byte-exact            unmet
  staged-rows     staged r46 entry plus the staged S533 row appended byte-exact      unmet
"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE = os.path.dirname(HERE)
LANE = os.path.dirname(os.path.dirname(os.path.dirname(WAVE)))
STAGED = "/home/vgpnk/Projects/shokuknow/merge/mori"
spec = importlib.util.spec_from_file_location("c2", os.path.join(WAVE, "count-c2.py"))
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)


def main(argv):
    rev = subprocess.run(["git", "-C", LANE, "rev-parse", argv[0] + "^{commit}"], check=True,
                         stdout=subprocess.PIPE).stdout.decode().strip()
    base = c2.git_reader(LANE, rev)
    copies = {p: open(os.path.join(LANE, p), "rb").read().decode("utf-8", "surrogateescape")
              for _, (p, _d, _k) in c2.COPIES.items()}
    st = lambda n: open(os.path.join(STAGED, "knowledge/corpus/knowledge", n), encoding="utf-8").read()
    s533 = [l for l in open(os.path.join(STAGED, "SOURCES.append.md"), encoding="utf-8").read().split("\n")
            if l.startswith("| S533 |")][0]
    controls = [
        ("do-nothing", {}),
        ("staged-r46", {c2.ENTRY: st("scope-charge-fields-r46.md")}),
        ("staged-r47", {c2.ENTRY: st("scope-composition-in-the-block-r47.md")}),
        ("staged-rows", {c2.ENTRY: st("scope-charge-fields-r46.md"),
                         "corpus/SOURCES.md": (base("corpus/SOURCES.md") or "").rstrip("\n") + "\n" + s533 + "\n"}),
    ]
    rc = 0
    for name, over in controls:
        def read(p, over=over):
            if p in over:
                return over[p]
            if p in copies:
                return copies[p]
            return base(p)
        met, line = c2.evaluate(read, rev)
        with open(os.path.join(WAVE, "evidence", "control-c2-%s.txt" % name), "w") as f:
            f.write("$ count-c2.py evaluate() over entering %s + frozen copies (control %s)\n%s\nexit=%d\n"
                    % (rev, name, line, 0 if met else 1))
        print("%-12s %s" % (name, line))
        rc |= int(met)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
