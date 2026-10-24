#!/usr/bin/env python3
"""Round-42 C2 counter: grade the report-accuracy errata records at REV.

P-C2 (frozen, contract.md): At the landed tip, LOG.md's round-42 entry and
SCORECARD.md's round-42 declaration each record the three corrections — (a) the
round-41 fleet report's `8/8 mutants killed` is superseded by
`5/8 killed, 3 SURVIVED` naming .ufo/waves/round-41/w1/MutC1Walrus.md,
MutC1Tuple.md, MutC1DropSort.md; (b) `34 attack seats (53%)` is superseded by
`31 attack seats of 64 (48.4%)` under the spec definition 12 reviewer + 11 critic
+ 8 mutation-tester (executors are not attack roles); (c) `2 scouts, 4 scribes`
is superseded by `1 scout, 5 scribes` with the returned total 19 unchanged — and
no lane-owned round-42 record re-asserts a superseded value uncontradicted.

Usage: python3 .ufo/waves/round-42/count-c2.py <rev> [--repo LANE]
Prints one line per check, then `C2=met|unmet`; exit 0 on met, 1 on unmet.
"""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
REV = None
W1 = ".ufo/waves/round-41/w1"
SPEC = ".ufo/waves/round-41/w1-spec.json"

failures = []


def check(name, ok, detail=""):
    print("check %-22s %s%s" % (name, "PASS" if ok else "FAIL",
                                (" (%s)" % detail) if detail else ""))
    if not ok:
        failures.append(name)


def git_show(rev, path):
    proc = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                          capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return None
    return proc.stdout


def git_ls(rev, path):
    proc = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only",
                           rev, path], capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return []
    return [l for l in proc.stdout.splitlines() if l]


def main():
    global REV
    args = [a for a in sys.argv[1:]]
    if not args:
        print("usage: count-c2.py <rev> [--repo LANE]")
        return 2
    REV = args[0]
    repo_idx = args.index("--repo") if "--repo" in args else -1
    if repo_idx >= 0:
        global LANE
        LANE = args[repo_idx + 1]

    log = git_show(REV, "LOG.md") or ""
    score = git_show(REV, "SCORECARD.md") or ""
    if not log or not score:
        print("C2=unmet (LOG.md or SCORECARD.md unreadable at %s)" % REV)
        return 1

    # --- evidence basis, re-measured at REV -------------------------------
    reports = [os.path.basename(p) for p in git_ls(REV, W1)
               if p.endswith(".md")]
    n_scr = sum(1 for r in reports if r.startswith("Scr"))
    n_scout = sum(1 for r in reports if r.startswith("Scout"))
    n_total = len(reports)
    check("evidence_returned_total", n_total == 19,
          "w1 md reports=%d want 19" % n_total)
    check("evidence_roles", n_scr == 5 and n_scout == 1,
          "Scr=%d Scout=%d want 5/1" % (n_scr, n_scout))

    spec_src = git_show(REV, SPEC)
    role_counts = {}
    if spec_src:
        spec = json.loads(spec_src)
        for item in spec.get("items", []):
            role_counts[item.get("role", "?")] = \
                role_counts.get(item.get("role", "?"), 0) + 1
    attack = sum(role_counts.get(r, 0)
                 for r in ("reviewer", "critic", "mutation-tester"))
    total = sum(role_counts.values())
    check("evidence_attack_seats",
          attack == 31 and total == 64 and role_counts.get("executor") == 3,
          "attack=%d/%d reviewer=%s critic=%s mut=%s exec=%s"
          % (attack, total, role_counts.get("reviewer"), role_counts.get("critic"),
             role_counts.get("mutation-tester"), role_counts.get("executor")))

    survivors = 0
    for name in ("MutC1Walrus.md", "MutC1Tuple.md", "MutC1DropSort.md"):
        body = git_show(REV, os.path.join(W1, name))
        if body and "SURVIVED" in body:
            survivors += 1
    check("evidence_survivors", survivors == 3, "SURVIVED reports=%d want 3" % survivors)

    # --- correction records in LOG.md round-42 entry -----------------------
    r42_log = log[log.find("## Round 42"):] if "## Round 42" in log else ""
    if not r42_log:
        # an append-only entry not starting with that heading: fall back to the
        # tail after the round-41 entry
        r42_log = log[log.rfind("Round-42"):] if "Round-42" in log else ""
    need_log = [
        ("log_erratum_tally",
         lambda t: ("8/8" in t and "5/8" in t and "SURVIVED" in t)),
        ("log_erratum_attack",
         lambda t: ("34 attack" in t and "31 attack" in t and "48.4%" in t)),
        ("log_erratum_roles",
         lambda t: ("2 scouts" in t and "4 scribes" in t
                    and "1 scout" in t and "5 scribes" in t)),
    ]
    for name, pred in need_log:
        check(name, bool(r42_log) and pred(r42_log),
              "round-42 LOG entry present=%s" % bool(r42_log))

    # --- correction records in SCORECARD.md round-42 declaration -----------
    r42_score = score[score.find("Round 42"):] if "Round 42" in score else ""
    need_score = [
        ("score_erratum_tally",
         lambda t: ("8/8" in t and "5/8" in t and "SURVIVED" in t)),
        ("score_erratum_attack",
         lambda t: ("34 attack" in t and "31 attack" in t and "48.4%" in t)),
        ("score_erratum_roles",
         lambda t: ("2 scouts" in t and "4 scribes" in t
                    and "1 scout" in t and "5 scribes" in t)),
    ]
    for name, pred in need_score:
        check(name, bool(r42_score) and pred(r42_score),
              "round-42 SCORECARD section present=%s" % bool(r42_score))

    # --- sweep: no uncontradicted re-assertion in lane-owned r42 records ---
    def bad(text):
        hits = []
        for pat in (r"8/8 mutants killed", r"34 attack seats \(53%\)",
                    r"2 scouts, 4 scribes"):
            for m in re.finditer(pat, text):
                ctx = text[max(0, m.start() - 200):m.end() + 200]
                if "superseded" not in ctx and "correct" not in ctx.lower():
                    hits.append(pat)
                    break
        return hits

    check("sweep_log_clean", not bad(r42_log),
          "uncontradicted=false-claim hits: %s" % bad(r42_log))
    check("sweep_score_clean", not bad(r42_score),
          "uncontradicted=false-claim hits: %s" % bad(r42_score))

    print("C2=%s" % ("unmet" if failures else "met"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
