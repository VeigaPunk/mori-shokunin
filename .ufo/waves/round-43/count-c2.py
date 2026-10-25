#!/usr/bin/env python3
"""Round-43 calibration counter. P-C2 is the sentence in contract.md.

Usage: python3 .ufo/waves/round-43/count-c2.py <rev> [--repo LANE]
Prints one line per check, then C2=met mismatches=0 or C2=unmet mismatches=N.
Exit 0 on met, 1 on unmet, 2 on usage.
"""
import hashlib
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
S235_SHA = "971df55e9e1ed8826e66dd31d12f9cbb5b2c727cf71201a2c0eabc7311e169a2"
PDF_REL = "corpus/evidence/sources-r42/S235.pdf"
PDF_SHA = "9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020"
DECL = "`C1=met` exit 0 (`evidence/c1-after.txt`)"
CORR = ("Round-43 calibration correction: r42-declaration-C1=met superseded; "
        "frozen counter printed no C1= line")

failures = []


def check(name, ok, detail=""):
    print("check %-22s %s%s" % (
        name, "PASS" if ok else "FAIL", (" (%s)" % detail) if detail else ""))
    if not ok:
        failures.append(name)


def git_bytes(rev, path):
    proc = subprocess.run(
        ["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
        capture_output=True, timeout=120)
    return proc.stdout if proc.returncode == 0 else None


def rows(text):
    found = []
    for line in text.splitlines():
        m = re.match(r"^ {0,3}\|\s*(S[0-9]+)\s*\|", line)
        if m:
            found.append((m.group(1), line))
    return found


def main():
    global LANE
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print("usage: count-c2.py <rev> [--repo LANE]", file=sys.stderr)
        return 2
    rev = args[0]
    if "--repo" in args:
        LANE = args[args.index("--repo") + 1]

    sources = git_bytes(rev, "corpus/SOURCES.md")
    score = git_bytes(rev, "SCORECARD.md")
    pdf = git_bytes(rev, PDF_REL)
    check("sources_present", sources is not None, "corpus/SOURCES.md")
    check("scorecard_present", score is not None, "SCORECARD.md")
    check("pdf_present", pdf is not None, PDF_REL)
    if sources is None or score is None or pdf is None:
        print("C2=unmet mismatches=%d" % len(failures))
        return 1

    text = sources.decode()
    s235 = [line for sid, line in rows(text) if sid == "S235"]
    s235_ok = len(s235) == 1 and hashlib.sha256(s235[0].encode()).hexdigest() == S235_SHA
    check("s235_unrewritten", s235_ok, "rows=%d" % len(s235))

    others = []
    for sid, line in rows(text):
        if sid == "S235":
            continue
        if "corrects S235" in line and "a30dca99" in line and "a30cda99" not in line:
            others.append(sid)
    check("correction_row", len(others) == 1, "ids=%s" % others)

    card = score.decode()
    check("declaration_unrewritten", card.count(DECL) == 1, "count=%d" % card.count(DECL))
    check("scorecard_correction", card.count(CORR) == 1, "count=%d" % card.count(CORR))
    check("pdf_sha", hashlib.sha256(pdf).hexdigest() == PDF_SHA, PDF_SHA[:12])

    n = len(failures)
    print("C2=%s mismatches=%d" % ("met" if n == 0 else "unmet", n))
    return 0 if n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
