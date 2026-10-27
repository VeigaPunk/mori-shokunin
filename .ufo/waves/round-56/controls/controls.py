#!/usr/bin/env python3
"""Round 56 controls — do-nothing receipts at the entering tip and
mutation arms for the C2 vote binder.

Usage: controls.py <enter-rev> [--repo DIR]
Writes nothing into the repo; scratch under TMPDIR. Each mutant is a
single-point edit of a scratch copy of tools/mori-vote-bind.py; a mutant is
KILLED iff its --selftest exits nonzero (the selftest arm that targets the
mutated behaviour fails). A SURVIVOR is a C2 kill-rule finding (a mutant its
own selftest cannot catch) and must print SURVIVOR.
"""
import os
import re
import subprocess
import sys
import tempfile

TOOL = "tools/mori-vote-bind.py"
C1 = ".ufo/waves/round-56/count-c1.py"
C2 = ".ufo/waves/round-56/count-c2.py"

MUTANTS = [
    ("fence-toggle-dropped",
     "        if fence:\n            continue\n", "", "t_fenced_text_ignored"),
    ("substring-scalar-binding",
     'm = VOTE_RE.match(s.strip())',
     'm = re.search(r"(RECHECK|ENTAIL)\\s+([0-9a-f]{12})\\s+([A-Za-z][A-Za-z0-9_-]*)", s)',
     "t_json_prose_substring_rejected"),
    ("hash-length-opened",
     r"([0-9a-f]{12})", r"([0-9a-f]{12,})", "t_hash_len_drift_rejected"),
    ("first-wins",
     'last[(v["verb"], v["hash"])] = v',
     'last.setdefault((v["verb"], v["hash"]), v)',
     "t_last_wins_text"),
    ("text-channel-closed",
     "    fence = False\n", '    return [], "text"\n    fence = False\n',
     "t_plain_binds"),
    ("json-channel-closed",
     "for s in _walk_strings(doc, []):", "for s in []:", "t_json_array_binds"),
    ("roster-filter-dropped",
     "roster = voters if voters is not None else sorted(outputs)",
     "roster = sorted(outputs)", "t_roster_and_name_filter"),
    ("entail-verb-dropped",
     r"^(RECHECK|ENTAIL)\s+", r"^(RECHECK)\s+", "t_entailed_verb_parsed"),
]


def git_show(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def run(repo, rev, path, cwd):
    src = git_show(repo, rev, path)
    if src is None:
        return None, None
    p_ = os.path.join(cwd, os.path.basename(path))
    with open(p_, "w", encoding="utf-8") as f:
        f.write(src)
    p = subprocess.run([sys.executable, p_] + [], capture_output=True, text=True, cwd=cwd)
    return p, p_


def main():
    if len(sys.argv) < 2:
        print("usage: controls.py <enter-rev> [--repo DIR]", file=sys.stderr)
        return 2
    enter = sys.argv[1]
    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    if "--repo" in sys.argv:
        repo = sys.argv[sys.argv.index("--repo") + 1]
    cwd = tempfile.mkdtemp(prefix="mori-r56-controls-", dir=os.environ.get("TMPDIR") or None)
    out = []

    def line(name, verdict, detail=""):
        out.append("%-28s %s %s" % (name, verdict, detail))

    # do-nothing receipts at the entering tip (tools absent there)
    for name, path in (("do-nothing-c1", C1), ("do-nothing-c2", C2)):
        src = git_show(repo, "HEAD", path)
        if src is None:
            line(name, "SETUP", "counter absent from working tree")
            continue
        p_ = os.path.join(cwd, os.path.basename(path))
        with open(p_, "w", encoding="utf-8") as f:
            f.write(src)
        p = subprocess.run([sys.executable, p_, enter, "--repo", repo],
                           capture_output=True, text=True, cwd=cwd)
        verdict = p.stdout.strip()
        want = "unmet" in verdict and "tool_absent" in verdict
        line(name, "PASS" if (p.returncode == 1 and want) else "FAIL", verdict[:110])

    src = git_show(repo, "HEAD", TOOL)
    if src is None:
        line("mutants", "SETUP", "tool absent from working tree")
    else:
        for name, old, new, arm in MUTANTS:
            mut = src.replace(old, new, 1)
            if mut == src:
                line("mut:" + name, "ERROR", "substitution did not apply")
                continue
            p_ = os.path.join(cwd, "mutant.py")
            with open(p_, "w", encoding="utf-8") as f:
                f.write(mut)
            p = subprocess.run([sys.executable, p_, "--selftest"],
                               capture_output=True, text=True, cwd=cwd)
            killed = p.returncode != 0
            line("mut:" + name, "KILLED" if killed else "SURVIVOR",
                 "arm=" + arm + (" rc=%d" % p.returncode if not killed else ""))
    text = "\n".join(out)
    print(text)
    return 1 if ("SURVIVOR" in text or "FAIL" in text or "ERROR" in text or "SETUP" in text) else 0


if __name__ == "__main__":
    sys.exit(main())
