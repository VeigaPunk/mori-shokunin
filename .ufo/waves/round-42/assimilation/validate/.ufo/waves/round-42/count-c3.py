#!/usr/bin/env python3
"""Round-42 C3 counter: grade the d72ac16 inheritance manifest at REV.

P-C3 (frozen, contract.md): At the landed tip,
`corpus/knowledge/inheritance-d72ac16-r42.md` names every path added unnamed by
commit d72ac167535229d737b9fa844513431d9a12f5ea — exactly 145 paths in three
categories: 67 `.ufo/waves/round-40/w1/*.md` seat reports, 7
`.ufo/waves/round-40/` evidence/scratch files, and 71 `.scratch/*` files — each
with category and provenance, and the manifest names no path d72ac16 did not add.
The named-freeze set (20 paths) is enumerated in evidence/freeze-r42.txt.

Usage: python3 .ufo/waves/round-42/count-c3.py <rev> [--repo LANE]
Prints one line per check, then `C3=met|unmet`; exit 0 on met, 1 on unmet.
"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
D72 = "d72ac167535229d737b9fa844513431d9a12f5ea"
MANIFEST = "corpus/knowledge/inheritance-d72ac16-r42.md"
CATEGORIES = {
    "seat_reports": (".ufo/waves/round-40/w1/", 67, ".md"),
    "r40_evidence_scratch": (".ufo/waves/round-40/", 7, None),
    "scratch": (".scratch/", 71, None),
}

failures = []


def check(name, ok, detail=""):
    print("check %-22s %s%s" % (name, "PASS" if ok else "FAIL",
                                (" (%s)" % detail) if detail else ""))
    if not ok:
        failures.append(name)


def git(args, timeout=120):
    return subprocess.run(["git", "-C", LANE] + args, capture_output=True,
                          text=True, timeout=timeout)


def added_paths(rev):
    proc = git(["diff-tree", "--no-renames", "--no-commit-id", "--name-only",
                "-r", rev])
    if proc.returncode != 0:
        return None
    return sorted(l for l in proc.stdout.splitlines() if l)


def manifest_paths(rev):
    proc = git(["show", "%s:%s" % (rev, MANIFEST)])
    if proc.returncode != 0:
        return None
    body = proc.stdout
    # fenced code blocks carry the path lists; prose may mention paths freely
    paths = set()
    in_fence = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            s = line.strip()
            if re.fullmatch(r"[A-Za-z0-9_./+-]+", s) and "/" in s:
                paths.add(s)
    return paths, body


def categorize(path):
    for name, (prefix, _want, _suffix) in CATEGORIES.items():
        if path.startswith(prefix):
            if name == "seat_reports" and not path.endswith(".md"):
                return None
            if name == "r40_evidence_scratch" and path.startswith(
                    ".ufo/waves/round-40/w1/"):
                return None
            return name
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: count-c3.py <rev> [--repo LANE]")
        return 2
    rev = args[0]
    if "--repo" in args:
        global LANE
        LANE = args[args.index("--repo") + 1]

    anc = git(["merge-base", "--is-ancestor", D72, rev])
    check("d72_ancestor", anc.returncode == 0, "merge-base rc=%d" % anc.returncode)
    added = added_paths(D72)
    check("d72_enumerated", bool(added),
          "paths=%s" % len(added) if added else "diff-tree failed")

    freeze = added and [p for p in added if categorize(p) is None] or []
    inherited = added and [p for p in added if categorize(p) is not None] or []
    check("freeze_set_size", len(freeze) == 20, "named-freeze paths=%d want 20"
          % len(freeze))
    check("inherited_set_size", len(inherited) == 145,
          "inherited paths=%d want 145" % len(inherited))
    cat_counts = {n: 0 for n in CATEGORIES}
    for p in inherited:
        cat_counts[categorize(p)] += 1
    for name, (_prefix, want, _suffix) in CATEGORIES.items():
        check("set_%s" % name, cat_counts[name] == want,
              "%d want %d" % (cat_counts[name], want))

    got = manifest_paths(rev)
    if got is None:
        check("manifest_present", False, "%s unreadable at %s" % (MANIFEST, rev))
        print("C3=unmet (%d checks failed)" % len(failures))
        return 1
    mpaths, body = got
    check("manifest_present", True, "%d candidate path lines" % len(mpaths))

    missing = sorted(set(inherited) - mpaths)
    extra = sorted(mpaths - set(inherited))
    check("manifest_covers_all", not missing,
          "missing=%d %s" % (len(missing), missing[:3]))
    check("manifest_no_extras", not extra,
          "extras=%d %s" % (len(extra), extra[:3]))

    # per-category coverage table inside the manifest (fenced blocks only)
    for name, (_prefix, want, _suffix) in CATEGORIES.items():
        section = re.search(r"### %s\n(.*?)(?=###|\Z)" % name, body, re.S)
        listed = 0
        if section:
            in_fence = False
            for line in section.group(1).splitlines():
                if line.strip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    s = line.strip()
                    if re.fullmatch(r"[A-Za-z0-9_./+-]+", s) and "/" in s:
                        listed += 1
        check("manifest_%s_rows" % name, listed == want,
              "listed=%d want %d" % (listed, want))

    print("C3=%s" % ("unmet" if failures else "met"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
