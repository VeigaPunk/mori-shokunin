# CtlPositive — round-35 C1 positive control (reachability)

## Control name
Positive control "oracle register": a register built from the fleet MANIFEST closure oracle, binding all
18 admitted mori capabilities to their closure key, round and one strong artifact. This is the *claimed*
work (not a skip); `C1=met` is expected and is not a counter defect.

## What work it does / does not skip
It does the full claimed work: reads the fleet MANIFEST at 37b51a24, extracts admitted mori closures and
their `capabilities_added`, and for each writes one 5-cell row with key, capability (no `|`), short what-cell,
ONE strong evidence path selected by the counter's rule, and round. It skips nothing: it picks real artifacts
that exist at the closure commit, changed in that round, lie under the allowed prefix, match any named path,
and appear whole in the closure's record text (verification + spot-check files + fleet report + caps) — exactly
the checks `count-c1.py` applies.

## How built (exact commands)
```
mkdir -p /fast/scratch/hyaku/mori-r35/CtlPositive
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
    /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlPositive/clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../clone checkout -q -b ctl-positive \
    f2d28711ee723c969b6c2008d32df498192f9e7b
# generator: /fast/scratch/hyaku/mori-r35/CtlPositive/gen-register.py (80 lines; inline below)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 .../gen-register.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../clone -c user.name=ctl \
    -c user.email=ctl@local commit -qam ctl
```

### Generator (80 lines, exact)
```python
#!/usr/bin/env python3
"""C1 positive control: build the SCORECARD capabilities register from the fleet MANIFEST closure oracle.
Each admitted mori capability gets one row keyed rounds[i].capabilities_added[j], one strong artifact
(named path first, else tools/, corpus/knowledge/, corpus/SOURCES.md, corpus/evidence/).
Usage: gen-register.py [--list]  (appends to $LANE/SCORECARD.md unless --list)."""
import json, re, subprocess, sys

LANE = "/fast/scratch/hyaku/mori-r35/CtlPositive/clone"; FLEET = "/home/vgpnk/Projects/shokunin"
REV = "37b51a243302e8009c7067431e8a47f9a722fd14"; FIRST_PREV = "20e2255"
ART = ("tools/", "corpus/knowledge/", "corpus/evidence/")
PREF = ("tools/", "corpus/knowledge/", "corpus/SOURCES.md", "corpus/evidence/")
NAMED_RE = re.compile(r"((?:tools|corpus/knowledge)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
SPOT_RE = re.compile(r"mori-shokunin/([A-Za-z0-9_./-]+)@([0-9a-f]{7,40})")

def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p

def show(repo, rev, path):
    p = git(repo, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None

def whole_path_in(path, text):
    pat = r"(?<![A-Za-z0-9_./-])(?:mori-shokunin/)?" + re.escape(path) + r"(?![A-Za-z0-9_/-])"
    return re.search(pat, text) is not None

def short(cap):
    s = re.sub(r"\s+", " ", re.split(r"\s*\(|\s*;\s*", cap.replace("|", "/"))[0]).strip()
    return s[:90] + ("..." if len(s) > 90 else "")

def rank(p, named):
    if p in named:
        return (0, named.index(p))
    for k, pref in enumerate(PREF):
        if p == pref or (pref.endswith("/") and p.startswith(pref)):
            return (1, k)
    return (2, 0)

def main():
    man = json.loads(git(FLEET, "show", REV + ":MANIFEST.json").stdout)
    prev = git(LANE, "rev-parse", "--verify", FIRST_PREV + "^{commit}").stdout.strip()
    rows = []
    for i, r in enumerate(man["rounds"]):
        if r.get("lane") != "mori":
            continue
        commit = git(LANE, "rev-parse", "--verify", r["commit"].split("@", 1)[1] + "^{commit}").stdout.strip()
        caps = (r.get("capabilities_added") or []) if r.get("admitted") is True else []
        if caps:
            changed = set(git(LANE, "diff", "--name-only", "--no-renames", prev, commit).stdout.splitlines())
            vtext = json.dumps(r.get("verification") or {})
            extra = [show(LANE, h, p) for p, h in SPOT_RE.findall(vtext)]
            rep = r.get("report")
            if rep:
                rp = git(FLEET, "show", "%s:%s" % (REV, rep), check=False)
                if rp.returncode == 0:
                    extra.append(rp.stdout)
            ctext = vtext + "\n" + "\n".join(x for x in extra if x) + "\n" + "\n".join(caps)
            at = set(git(LANE, "ls-tree", "-r", "--name-only", commit).stdout.splitlines())
            for j, cap in enumerate(caps):
                named = list(dict.fromkeys(NAMED_RE.findall(cap)))
                cand = sorted(p for p in changed if p in at and (p.startswith(ART) or p == "corpus/SOURCES.md")
                              and (not named or p in named) and whole_path_in(p, ctext))
                pick = min(cand, key=lambda p: rank(p, named))
                print("row rounds[%d].capabilities_added[%d] candidates=%s" % (i, j, cand))
                rows.append((i, j, r["round"], cap, pick))
        prev = commit
    if "--list" in sys.argv:
        return
    body = ["", "## Capabilities register (round 35 positive control)", "",
            "| Key | Capability | What it can now do | Evidence | First-working round |",
            "|---|---|---|---|---|"]
    for i, j, rnd, cap, pick in rows:
        body.append("| `rounds[%d].capabilities_added[%d]` | %s | %s | `%s` | %s |"
                    % (i, j, cap.replace("|", "/"), short(cap), pick, rnd))
    with open(LANE + "/SCORECARD.md", "a", encoding="utf-8") as fh:
        fh.write("\n".join(body) + "\n")

main()
```

## Clone commit
`e1463e8b01d5fe2c68417a73d5c5ad75dfb83f77` (parent f2d28711; one commit `ctl` on branch `ctl-positive`), SCORECARD.md +23 lines.

## Counter sha256 run
`27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` (frozen `count-c1.py`, sha256sum verified before scoring).

## Full stdout of the counter run
```
row rounds[313].capabilities_added[0] matched
row rounds[339].capabilities_added[0] matched
row rounds[345].capabilities_added[0] matched
row rounds[353].capabilities_added[0] matched
row rounds[386].capabilities_added[0] matched
row rounds[386].capabilities_added[1] matched
row rounds[386].capabilities_added[2] matched
row rounds[398].capabilities_added[0] matched
row rounds[427].capabilities_added[0] matched
row rounds[443].capabilities_added[0] matched
row rounds[443].capabilities_added[1] matched
row rounds[455].capabilities_added[0] matched
row rounds[455].capabilities_added[1] matched
row rounds[462].capabilities_added[0] matched
row rounds[476].capabilities_added[0] matched
row rounds[476].capabilities_added[1] matched
row rounds[495].capabilities_added[0] matched
row rounds[495].capabilities_added[1] matched
label=P-C1 rev=e1463e8b01d5fe2c68417a73d5c5ad75dfb83f77 manifest_rev=37b51a243302 register='## Capabilities register (round 35 positive control)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```
Exit code: `0`.

## Per-row strong candidate sets (full choice set; `*` = row's chosen path)
| key | round | candidates |
|---|---|---|
| rounds[313].capabilities_added[0] | 12 | toolkit/mori-census.sh*, corpus/SOURCES.md, corpus/evidence/drift-r12-20261019T2204Z-classification.md, corpus/evidence/roster-r12-20261019T220912Z-live.log, corpus/evidence/roster-r12-20261019T220912Z-mutation.md, corpus/knowledge/oom-kill-counter-kernel-only-r12.md, corpus/knowledge/roster-truth-r12.md |
| rounds[339].capabilities_added[0] | 14 | tools/mori-census.sh*, corpus/SOURCES.md, corpus/knowledge/journal-alarm-routing-r14.md, tools/mori-round13-regressions.py, tools/mori-round14-regressions.py |
| rounds[345].capabilities_added[0] | 15 | tools/mori-census.sh*, corpus/SOURCES.md, corpus/knowledge/journal-positive-evidence-r15.md, tools/mori-round13-regressions.py, tools/mori-round14-regressions.py, tools/mori-round15-regressions.py |
| rounds[353].capabilities_added[0] | 16 | tools/mori-journal-window.py*, corpus/knowledge/journal-cursor-window-r16.md, tools/mori-round16-context-check.py, tools/mori-round16-regressions.py |
| rounds[386].capabilities_added[0] | 18 | tools/mori-retention-gate.py* (named) |
| rounds[386].capabilities_added[1] | 18 | tools/mori-freeze-order.py* (named) |
| rounds[386].capabilities_added[2] | 18 | tools/mori-dispatch-ledger.py* (named) |
| rounds[398].capabilities_added[0] | 19 | tools/mori-content-review.py*, tools/mori-freeze-order.py |
| rounds[427].capabilities_added[0] | 22 | tools/mori-retention-reconcile.py* (named) |
| rounds[443].capabilities_added[0] | 24 | tools/mori-pressure.py* (named) |
| rounds[443].capabilities_added[1] | 24 | tools/mori-routed-check.py* (named) |
| rounds[455].capabilities_added[0] | 25 | tools/mori-job-runway.py* (named) |
| rounds[455].capabilities_added[1] | 25 | tools/mori-routed-r24.py* (named) |
| rounds[462].capabilities_added[0] | 26 | tools/mori-oom-killers.py* (named) |
| rounds[476].capabilities_added[0] | 28 | tools/fixtures/mori-oom-killers/cases-a2.json*, corpus/SOURCES.md, corpus/knowledge/oom-victim-selection-r27.md |
| rounds[476].capabilities_added[1] | 28 | tools/mori-oom-killers.py* (first-named), tools/fixtures/mori-oom-killers/cases-a2.json |
| rounds[495].capabilities_added[0] | 31 | tools/mori-blind-check.sh* (named) |
| rounds[495].capabilities_added[1] | 31 | corpus/knowledge/watchdog-identity-r31.md* (named) |

## Verdict
**met** — `C1=met`, exit 0, all 18/18 rows matched, missing=0, bad=0, extra=0, mismatches=0. This is the
expected positive-control outcome (the target state is reachable); it is not a counter defect.

## Files
- register: `.ufo/waves/round-35/c0/CtlPositive-register.md` (the appended section only, 22 lines ≤ 200)
- this report: `.ufo/waves/round-35/c0/CtlPositive.md`
