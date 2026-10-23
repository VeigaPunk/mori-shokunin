#!/usr/bin/env python3
"""Round-35 C1 counter (calibration): SCORECARD capabilities register vs fleet MANIFEST.

Predicate P-C1 (frozen; the same sentence is in contract.md and the receipt label):
  At the measured lane revision, the last level-2 section of SCORECARD.md whose heading
  begins "## Capabilities" holds exactly one table row per capability that the fleet
  MANIFEST.json at fleet revision MANIFEST_REV records in `capabilities_added` of an
  admitted mori closure, keyed `rounds[i].capabilities_added[j]`, naming that closure's
  round, and citing one or two evidence paths, each of which exists at the measured
  revision (any cited line range inside the file), exists at that closure's commit,
  changed between the previous mori closure commit and that closure's commit, lies under
  tools/, corpus/knowledge/ or corpus/evidence/ or is corpus/SOURCES.md, equals a tools/
  or corpus/knowledge/ path the capability string names (when it names one), and appears
  as a whole path in that closure's record text (its MANIFEST verification object, its
  capabilities_added strings, the lane spot-check files that object names, and the fleet
  report its `report` field names, all at MANIFEST_REV); and it holds no other row.
  C1=met iff matched == oracle and missing == bad == extra == 0.

Every arm is two-sided: missing (lower bound: each oracle capability must be matched) and
extra/bad (upper bound: no row beyond the oracle, no unresolvable path, no wrong round).

Usage: count-c1.py <lane-rev> [--repo PATH] [--fleet PATH] [--json]
Exit: 0 met, 1 unmet, 2 error. Read-only: git show / diff / ls-tree only.
"""
import json
import re
import subprocess
import sys

LABEL = "P-C1"
MANIFEST_REV = "37b51a243302e8009c7067431e8a47f9a722fd14"  # fleet commit: mori r34 closure
FIRST_PREV = "20e2255"  # parent of the first round-12 commit (1f07f1d^); r12 is mori's first MANIFEST entry
ARTIFACT_PREFIXES = ("tools/", "corpus/knowledge/", "corpus/evidence/")
ARTIFACT_FILES = {"corpus/SOURCES.md"}
NAMED_RE = re.compile(r"((?:tools|corpus/knowledge)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
KEY_RE = re.compile(r"^`?rounds\[(\d+)\]\.capabilities_added\[(\d+)\]`?$")
TICK_RE = re.compile(r"`([^`]+)`")
PATHTOK_RE = re.compile(r"^([A-Za-z0-9_.][A-Za-z0-9_./-]*)(?::(\d+)(?:-(\d+))?)?$")
SPOT_RE = re.compile(r"mori-shokunin/([A-Za-z0-9_./-]+)@([0-9a-f]{7,40})")


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p


def show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def whole_path_in(p, text):
    """True when p occurs in text not preceded or followed by a path character, or as mori-shokunin/p."""
    pat = r"(?<![A-Za-z0-9_./-])(?:mori-shokunin/)?" + re.escape(p) + r"(?![A-Za-z0-9_/-])"
    return re.search(pat, text) is not None


def tree_paths(repo, rev):
    out = git(repo, "ls-tree", "-r", "--name-only", rev).stdout
    return set(out.splitlines())


def register_rows(text):
    lines = text.splitlines()
    starts = [i for i, l in enumerate(lines) if l.startswith("## ")]
    cap = [i for i in starts if lines[i].startswith("## Capabilities")]
    if not cap:
        return None, []
    s = cap[-1]
    nxt = [i for i in starts if i > s]
    e = nxt[0] if nxt else len(lines)
    rows = []
    for l in lines[s + 1:e]:
        t = l.strip()
        if not t.startswith("|"):
            continue
        cells = [c.strip() for c in t.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if rows and not KEY_RE.match(rows[0][0]):
        hdr = rows[0]
        if hdr and hdr[0].lower() in ("key", "capability"):
            rows = rows[1:]
    return lines[s], rows


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    rev = argv[0]
    repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
    fleet = "/home/vgpnk/Projects/shokunin"
    as_json = "--json" in argv
    if "--repo" in argv:
        repo = argv[argv.index("--repo") + 1]
    if "--fleet" in argv:
        fleet = argv[argv.index("--fleet") + 1]
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}").stdout.strip()
    manifest = json.loads(git(fleet, "show", MANIFEST_REV + ":MANIFEST.json").stdout)
    entries = [(i, r) for i, r in enumerate(manifest["rounds"]) if r.get("lane") == "mori"]
    oracle = {}
    prev = git(repo, "rev-parse", "--verify", FIRST_PREV + "^{commit}").stdout.strip()
    for i, r in entries:
        commit = git(repo, "rev-parse", "--verify",
                     r["commit"].split("@", 1)[1] + "^{commit}").stdout.strip()
        if r.get("admitted") is True:
            caps = r.get("capabilities_added") or []
            if caps:
                changed = set(git(repo, "diff", "--name-only", "--no-renames", prev, commit).stdout.splitlines())
                vtext = json.dumps(r.get("verification") or {}, ensure_ascii=False)
                extra = []
                for p, h in SPOT_RE.findall(vtext):
                    c = show(repo, h, p)
                    if c is not None:
                        extra.append(c)
                rep = r.get("report")
                if rep:
                    rp = git(fleet, "show", "%s:%s" % (MANIFEST_REV, rep), check=False)
                    if rp.returncode == 0:
                        extra.append(rp.stdout)
                ctext = vtext + "\n" + "\n".join(extra) + "\n" + "\n".join(caps)
                at_commit = tree_paths(repo, commit)
                for j, cap in enumerate(caps):
                    oracle["rounds[%d].capabilities_added[%d]" % (i, j)] = {
                        "round": r["round"], "commit": commit, "changed": changed,
                        "ctext": ctext, "at_commit": at_commit,
                        "named": set(NAMED_RE.findall(cap)), "cap": cap,
                    }
        prev = commit
    sc = show(repo, full, "SCORECARD.md")
    if sc is None:
        raise RuntimeError("SCORECARD.md absent at %s" % full)
    heading, rows = register_rows(sc)
    at_rev = tree_paths(repo, full)
    seen = {}
    bad, extra, details = [], [], []
    for cells in rows:
        m = KEY_RE.match(cells[0]) if cells else None
        key = "rounds[%s].capabilities_added[%s]" % (m.group(1), m.group(2)) if m else None
        if key is None or key not in oracle:
            extra.append(cells[0] if cells else "")
            details.append({"row": cells[0] if cells else "", "status": "extra"})
            continue
        if key in seen:
            extra.append(key)
            details.append({"row": key, "status": "extra-duplicate"})
            continue
        seen[key] = True
        o = oracle[key]
        why = []
        if len(cells) != 5:
            why.append("cells=%d" % len(cells))
        else:
            rnd = cells[4].strip("` ")
            if rnd != str(o["round"]):
                why.append("round=%s!=%s" % (rnd, o["round"]))
            toks = TICK_RE.findall(cells[3])
            paths = []
            for t in toks:
                pm = PATHTOK_RE.match(t.strip())
                if not pm:
                    why.append("not-a-path:%s" % t)
                    continue
                p, a, b = pm.group(1), pm.group(2), pm.group(3)
                if p not in at_rev:
                    why.append("absent-at-rev:%s" % p)
                    continue
                if a:
                    n = len((show(repo, full, p) or "").splitlines())
                    lo, hi = int(a), int(b or a)
                    if not (1 <= lo <= hi <= n):
                        why.append("line-out-of-range:%s" % t)
                        continue
                paths.append(p)
            if not 1 <= len(toks) <= 2:
                why.append("evidence-paths=%d" % len(toks))
            for p in paths:
                if not (p in o["at_commit"] and p in o["changed"]
                        and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
                        and (not o["named"] or p in o["named"])
                        and whole_path_in(p, o["ctext"])):
                    why.append("weak-path:%s" % p)
        if why:
            bad.append(key)
            details.append({"row": key, "status": "bad", "why": why})
        else:
            details.append({"row": key, "status": "matched"})
    missing = sorted(k for k in oracle if k not in seen)
    matched = sum(1 for d in details if d["status"] == "matched")
    met = matched == len(oracle) and not missing and not bad and not extra
    summary = ("label=%s rev=%s manifest_rev=%s register=%r oracle=%d rows=%d matched=%d missing=%d bad=%d "
               "extra=%d mismatches=%d C1=%s") % (
        LABEL, full, MANIFEST_REV[:12], heading, len(oracle), len(rows), matched, len(missing), len(bad),
        len(extra), len(missing) + len(bad) + len(extra), "met" if met else "unmet")
    if as_json:
        print(json.dumps({"details": details, "missing": missing}, indent=1))
    else:
        for d in details:
            print("row %s %s %s" % (d["row"], d["status"], ",".join(d.get("why", []))))
        for k in missing:
            print("row %s missing" % k)
    print(summary)
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # noqa: BLE001
        print("count-c1: error: %s" % exc)
        sys.exit(2)
