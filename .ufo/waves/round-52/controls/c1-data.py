#!/usr/bin/env python3
"""Round 52 C1 data applier — the L1's edits for the calibration claim, split into parts so the frozen controls
can apply a subset. Usage: c1-data.py <tree> <part>[,<part>...]   parts: axes, receipts, living, locator,
rewrite (control only: edits the stale pins in place), delete (control only: deletes them), repeat (control
only: supersedes them with the stale tally repeated). <tree> is a checkout of the lane (the lane itself at
data time, or a throwaway clone for a control). The receipts part runs the two SHONEN tools in <tree> with
TMPDIR=$TMPDIR and writes their output under .ufo/waves/round-52/evidence/selftests/.
"""
import os
import subprocess
import sys

R51 = "corpus/lessons/round-51-verifier-spotcheck.md"
STALE_Q = "`python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`"
STALE_R9 = "`--selftest` → `pass=9 fail=0`"
GOOD_SA = "`python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`"
GOOD_C39 = ("`python3 .ufo/waves/round-39/conform.py 4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d --selftest` → "
            "`CONFORM_SELFTEST pass=9 fail=0`")

QUALITY_ADD = """
## Criteria added round 52 — a living pin is current or superseded, and a self-assessment pointer lands on its words

141. **A command-tally pin in a living document (`corpus/QUALITY.md`, `corpus/README.md`) prints its tally when run
    today, or a later line supersedes it; the stale pin itself is never rewritten.** This row supersedes 112's check
    cell only; 112's criterion stands. Rationale: 112's check pinned the gate's selftest at the round-39 count while
    the committed tool has printed 22 since the round-41 freeze `d72ac167` (QUALITY 128). Check:
    """ + GOOD_SA + """, exit 0, run in a `git archive` of the tip with `TMPDIR` in scratch. Counter:
    `python3 .ufo/waves/round-52/count-c1.py <rev>` arm (C) lists every single-line pin in both files as good,
    superseded or a mismatch. Shown able to fail: at the entering tip `4f266ef2` the arm read three mismatches
    (`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`); rewriting a stale pin in place reads
    `pin_removed_or_rewritten`. Not covered: a pin split across lines or carrying a placeholder is not enumerated
    as a pin when it spans lines.
142. **A self-assessment pointer lands on the words it reports.** In `SCORECARD.md` `## Axes` and in the
    `SHONEN.md` boxes, a `path:N` pointer after a quoted string or a `proposed A → B` phrase names lines that hold
    that string or pair; every pointer names lines that exist. Rationale: the freshness cell pointed round 28's
    proposed `5 → 6` at `SCORECARD.md:1771`, which holds the amendment A1 paragraph; the pair is at `:1781`.
    Check: `python3 .ufo/waves/round-52/count-c1.py <rev>` arm (D), `item locator … state=` lines. Shown able to
    fail: the entering tip reads `item locator SCORECARD.md:1771 expect=pair:5_→_6 got=absent state=mismatch`.
    Not covered: prose before a pointer other than a quoted string or a `proposed A → B` pair is checked for range
    only.
"""

README_ADD = """
## Round-52 corrections (living pins)

Dated note (append-only, 2026-10-26): two command-tally pins in the coverage tables above no longer print what
they say, and neither row is rewritten.

- Round-39 row "Ancestry-based timed supersede": this note supersedes """ + STALE_Q + """ (the round-39 count); the committed gate has printed 22 since the round-41 freeze `d72ac167`: """ + GOOD_SA + """.
- Round-39 row "Counter conformance v2": this note supersedes """ + STALE_R9 + """, which names no command; the runnable form takes a revision: """ + GOOD_C39 + """.

Each bullet is one line on purpose: the counter reads a quoted stale pin as a quotation only when its replacement
pin stands on the same line.

Counter: `python3 .ufo/waves/round-52/count-c1.py <rev>` arm (C) (QUALITY 141).
"""


def edit(tree, rel, fn):
    p = os.path.join(tree, rel)
    with open(p, encoding="utf-8") as f:
        t = f.read()
    n = fn(t)
    if n == t:
        raise SystemExit("c1-data: no change in %s" % rel)
    with open(p, "w", encoding="utf-8") as f:
        f.write(n)


def axes(t):
    lines = t.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("| operability | 7 |"):
            c = l.split(" | ")
            c[2] = c[2] + ("; round-51 closure grades operability improved (C1: a `--rev` pin re-execution is "
                           "hermetic and classes mismatches) and states the score 7 (`%s:130`)" % R51)
            c[3] = "round 51 (improved, score held); " + c[3]
            lines[i] = " | ".join(c)
        if l.startswith("| depth | 5 |"):
            c = l.split(" | ")
            c[2] = c[2] + ("; round-51 closure grades depth improved (C2 re-measured 21/21, the MemAvailable entry) "
                           "and states the score 5 (`%s:131`)" % R51)
            c[3] = "round 51 (improved, score held); " + c[3]
            lines[i] = " | ".join(c)
    return "\n".join(lines)


def locator(t):
    return t.replace("round 28's measured outcome proposed 5 → 6 (`SCORECARD.md:1771`)",
                     "round 28's measured outcome proposed 5 → 6 (`SCORECARD.md:1781`)", 1)


def receipts(tree):
    d = os.path.join(tree, ".ufo/waves/round-52/evidence/selftests")
    os.makedirs(d, exist_ok=True)
    rev = subprocess.run(["git", "-C", tree, "rev-parse", "HEAD"], stdout=subprocess.PIPE).stdout.decode().strip()
    for tool in ("tools/mori-pin-check.py", "tools/mori-unlanded-check.py"):
        q = subprocess.run([sys.executable, tool, "--selftest"], cwd=tree, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        with open(os.path.join(d, os.path.basename(tool)[:-3] + ".txt"), "w", encoding="utf-8") as f:
            f.write("$ cd <lane checkout at %s> && python3 %s --selftest\n" % (rev, tool))
            f.write(q.stdout.decode("utf-8", "replace"))
            f.write("rc=%d\n" % q.returncode)


def main(argv):
    tree, parts = argv[0], argv[1].split(",")
    for part in parts:
        if part == "axes":
            edit(tree, "SCORECARD.md", axes)
        elif part == "locator":
            edit(tree, "SCORECARD.md", locator)
        elif part == "receipts":
            receipts(tree)
        elif part == "living":
            edit(tree, "corpus/QUALITY.md", lambda t: t.rstrip("\n") + "\n" + QUALITY_ADD)
            edit(tree, "corpus/README.md", lambda t: t.rstrip("\n") + "\n" + README_ADD)
        elif part == "rewrite":
            edit(tree, "corpus/QUALITY.md", lambda t: t.replace(STALE_Q, GOOD_SA))
            edit(tree, "corpus/README.md", lambda t: t.replace(STALE_Q, GOOD_SA).replace(STALE_R9, GOOD_C39))
        elif part == "delete":
            edit(tree, "corpus/QUALITY.md", lambda t: t.replace(STALE_Q, "the gate's selftest"))
            edit(tree, "corpus/README.md", lambda t: t.replace(STALE_Q, "the gate's selftest")
                 .replace(STALE_R9, "its selftest"))
        elif part == "repeat":
            edit(tree, "corpus/QUALITY.md", lambda t: t.rstrip("\n") + "\n\n141. This row supersedes 112's check "
                 "cell. Check: " + STALE_Q + ".\n")
            edit(tree, "corpus/README.md", lambda t: t.rstrip("\n") + "\n\nThis note supersedes " + STALE_Q
                 + " and " + STALE_R9 + ".\n")
        else:
            raise SystemExit("c1-data: unknown part %s" % part)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
