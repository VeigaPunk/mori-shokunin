#!/usr/bin/env python3
"""mori round-95 C1 counter (calibration): battery kill coverage of the round-94 admission counter.

Frozen predicate P-C1r95 (`.ufo/waves/round-95/contract.md` section C1; this docstring, the contract
and the receipt carry the same sentence):

  python3 -I .ufo/waves/round-95/count-c1.py <rev> --lane <lane-repo> --census <sources-census.sh>

  <rev> names a lane commit that holds the pristine round-94 counter `.ufo/waves/round-94/count-c1v2.py`
  whose sha256 MUST equal PRISTINE_SHA256 (else exit 2). The script clones the lane (no alternates) into
  $TMPDIR (default $HYAKU_SCRATCH/mori-r95, else /fast/scratch/hyaku), builds one fixture commit per row of
  FIXTURES on top of BASE 84b152308fa6, and scores the pristine counter and each mutant of MUTANTS on the
  fixture set through the counter's public path `count-c1v2.py <fixture-rev> --repo <clone> --census <CENSUS>`.

  Every fixture has an expected pristine verdict (checked; a mismatch is exit 2, so no fixture is vacuous).
  A mutant is KILLED iff at least one fixture's verdict (the `C1=` token plus the checks_failed list)
  differs from the pristine verdict on that fixture. A mutant whose run prints no `C1=` line counts as
  killed with `crash` (never as a silent pass). The one declared equivalent mutant (m5) is listed, not scored.

  Before (round-94 battery only) and after (round-94 battery plus the round-95 fixtures) are both printed:

    C1=met survivors=0 killed=7/7 before_r94_survivors=<n> r94_survivor_ids=<ids> pristine=green equiv=m5 ...

  exit 0 iff survivors == 0 and the pristine counter is green on BASE; exit 1 otherwise; exit 2 on setup failure.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "84b152308fa6c2f224ad75dff68e525dab9057ac"
ENTERING = "7b3fe9d540c98b8b0390a0f9bbe78de4341092a5"
COUNTER_PATH = ".ufo/waves/round-94/count-c1v2.py"
PRISTINE_SHA256 = "6eb7fa4cf0ecf86064bb2714a5b93b52bf3356dc6e38e5dc7ee51f7255a7b384"
FILE_R77 = "corpus/knowledge/counter-win-r77.md"
FILE_R73 = "corpus/knowledge/boot-anchor-win-r73.md"
VERIFIED = "verified-at:"

# Single exact-text edits of the pristine bytes. Each anchor must occur exactly once.
MUTANTS = {
    "m1": ("    return len(tok) >= 7 and ac.startswith(tok)", "    return ac[:7] in va"),
    "m1b": ("    return len(tok) >= 7 and ac.startswith(tok)", "    return ac in tok"),
    "m2": ("    return len(tok) >= 7 and ac.startswith(tok)", "    return ac.startswith(tok)"),
    "m3": ('        if not census_ok:\n            fails.append("census")\n', ""),
    "m4": ("        if trio < 98:", "        if trio < 0:"),
    "m6": ("        patched = sum(1 for rel in TWELVE\n"
           "                      if one_verified_at_change(args.repo, rev, os.path.join(KNOW, rel)))",
           "        patched = len(TWELVE)"),
    "m7": ("            if admission_token_ok(va, ac):", "            if ac and va and ac[:7] in va:"),
}
EQUIVALENT = {"m5": ("        if adm_fail != 0 or adm_ok != len(NINETEEN):",
                     "        if adm_fail != 0 or adm_ok < 1:")}
R94_FIXTURES = ["R94-L", "R94-R", "R94-M"]
R95_FIXTURES = ["R95-LEN", "R95-CEN", "R95-TRIO", "R95-PAT"]
EXPECTED = {  # pristine verdict per fixture: (C1 token, checks_failed)
    "R94-L": ("C1=unmet", "admission"), "R94-R": ("C1=unmet", "admission"),
    "R94-M": ("C1=unmet", "admission"), "R95-LEN": ("C1=unmet", "admission"),
    "R95-CEN": ("C1=unmet", "census"), "R95-TRIO": ("C1=unmet", "trio"),
    "R95-PAT": ("C1=unmet", "patched12"),
}


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), r.stderr.decode(errors="replace").strip()))
    return r


def admission(clone, rel):
    lines = [ln for ln in git(clone, "log", "--diff-filter=A", "--format=%h", ENTERING, "--", rel)
             .stdout.decode().split() if ln]
    if not lines:
        raise RuntimeError("no admission commit for %s" % rel)
    return lines[-1]


def verified_line_index(lines):
    idx = [i for i, ln in enumerate(lines) if ln.startswith(VERIFIED)]
    if len(idx) != 1:
        raise RuntimeError("verified-at line count %d" % len(idx))
    return idx[0]


def commit(clone, msg):
    git(clone, "add", "-A")
    git(clone, "-c", "user.name=mori-r95-fixture", "-c", "user.email=fixture@mori.invalid",
        "-c", "commit.gpgsign=false", "commit", "-q", "-m", msg)
    return git(clone, "rev-parse", "HEAD").stdout.decode().strip()


def build_fixtures(clone, ac_r77):
    """Return {fixture_id: (rev, census_override or None)}; every fixture starts from BASE."""
    fx = {}
    git(clone, "checkout", "-q", "--detach", BASE)
    orig77 = git(clone, "show", "%s:%s" % (BASE, FILE_R77)).stdout.decode()
    orig73 = git(clone, "show", "%s:%s" % (BASE, FILE_R73)).stdout.decode()
    path77 = os.path.join(clone, FILE_R77)
    path73 = os.path.join(clone, FILE_R73)

    def write(path, text):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def edit_verified(fn):
        lines = orig77.splitlines(keepends=True)
        i = verified_line_index(lines)
        lines[i] = fn(lines[i])
        return "".join(lines)

    for label, make in [("R94-L", lambda ln: ln.replace(ac_r77, "f" + ac_r77 + "0", 1)),
                        ("R94-R", lambda ln: ln.replace(ac_r77, ac_r77 + "9f", 1)),
                        ("R94-M", lambda ln: ln.replace(ac_r77, "a" + ac_r77 + "b", 1)),
                        ("R95-LEN", lambda ln: ln.replace(ac_r77, ac_r77[:5], 1))]:
        git(clone, "checkout", "-q", "--detach", BASE)
        write(path77, edit_verified(make))
        fx[label] = (commit(clone, "round-95 control fixture %s" % label), None)

    git(clone, "checkout", "-q", "--detach", BASE)
    fx["R95-CEN"] = (BASE, "FAILING")  # census override only; tree unchanged

    git(clone, "checkout", "-q", "--detach", BASE)
    lines73 = orig73.splitlines(keepends=True)
    kept = [ln for ln in lines73 if not ln.startswith("recheck:")]
    if len(kept) != len(lines73) - 1:
        raise RuntimeError("expected exactly one recheck: line in %s" % FILE_R73)
    write(path73, "".join(kept))
    fx["R95-TRIO"] = (commit(clone, "round-95 control fixture R95-TRIO"), None)

    git(clone, "checkout", "-q", "--detach", BASE)
    write(path77, orig77 + "\nRound-95 control: body-only line, no verified-at change.\n")
    fx["R95-PAT"] = (commit(clone, "round-95 control fixture R95-PAT"), None)
    return fx


def run_counter(src, rev, clone, census, scratch):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": scratch, "TMPDIR": scratch}
    r = subprocess.run(["python3", "-I", src, rev, "--repo", clone, "--census", census],
                       capture_output=True, text=True, env=env)
    out = (r.stdout or "").strip()
    m = re.search(r"C1=(met|unmet)", out)
    if not m:
        return ("crash", r.returncode, out.splitlines()[0] if out else "")
    c = re.search(r"checks_failed=(\S+)", out)
    return (m.group(0), r.returncode, c.group(1) if c else "")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev")
    ap.add_argument("--lane", required=True)
    ap.add_argument("--census", required=True)
    args = ap.parse_args(argv)
    lane = os.path.abspath(args.lane)
    census_real = os.path.abspath(args.census)
    if not os.path.isfile(census_real):
        print("C1_SETUP census not a file: %s" % census_real)
        return 2
    pristine_bytes = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (args.rev, COUNTER_PATH)],
                                    capture_output=True).stdout
    if hashlib.sha256(pristine_bytes).hexdigest() != PRISTINE_SHA256:
        print("C1_SETUP pristine counter sha256 mismatch at %s" % args.rev)
        return 2
    root = os.environ.get("TMPDIR") or os.path.join(os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku",
                                                    "mori-r95")
    os.makedirs(root, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="c1-", dir=root)
    try:
        clone = os.path.join(scratch, "clone")
        subprocess.run(["git", "clone", "-q", "--no-local", "--no-checkout", lane, clone],
                       check=True, capture_output=True)
        if git(clone, "rev-parse", "--show-toplevel").stdout.decode().strip() != clone:
            print("C1_SETUP clone toplevel mismatch")
            return 2
        ac_r77 = admission(clone, FILE_R77)
        fixtures = build_fixtures(clone, ac_r77)
        variants = {"pristine": pristine_bytes}
        for mid, (anchor, repl) in MUTANTS.items():
            if pristine_bytes.decode().count(anchor) != 1:
                print("C1_SETUP anchor for %s not unique" % mid)
                return 2
            variants[mid] = pristine_bytes.decode().replace(anchor, repl, 1).encode()
        results = {}  # (variant, fixture) -> verdict
        census_fail = os.path.join(scratch, "census-fail.sh")
        with open(census_fail, "w") as fh:
            fh.write("#!/usr/bin/env bash\nexit 1\n")
        for vname, data in variants.items():
            vdir = os.path.join(scratch, "v-" + vname)
            os.makedirs(vdir)
            src = os.path.join(vdir, "count-c1v2.py")
            with open(src, "wb") as fh:
                fh.write(data)
            for fid, (rev, cover) in fixtures.items():
                census = census_fail if cover == "FAILING" else census_real
                results[(vname, fid)] = run_counter(src, rev, clone, census, scratch)
        pristine_ok = results[("pristine", "R94-L")] is not None
        base_live = run_counter(os.path.join(scratch, "v-pristine", "count-c1v2.py"), BASE, clone,
                                census_real, scratch)
        green = base_live[0] == "C1=met" and base_live[1] == 0
        bad = [fid for fid in EXPECTED if results[("pristine", fid)][0] != EXPECTED[fid][0]
               or results[("pristine", fid)][2] != EXPECTED[fid][1]]
        if bad:
            print("C1_SETUP pristine fixture verdict unexpected: %s" % ",".join(
                "%s=%s" % (f, results[("pristine", f)]) for f in bad))
            return 2
        killers = {}
        for mid in MUTANTS:
            hits = [fid for fid in fixtures if results[(mid, fid)] != results[("pristine", fid)]]
            killers[mid] = hits
        survivors = sorted(m for m in MUTANTS if not killers[m])
        r94_only = sorted(m for m in MUTANTS
                          if not [f for f in R94_FIXTURES if results[(m, f)] != results[("pristine", f)]])
        crashes = sorted(m for m in MUTANTS for fid in fixtures if results[(m, fid)][0] == "crash")
        met = not survivors and green
        print("C1=%s survivors=%d killed=%d/%d before_r94_survivors=%d r94_survivor_ids=%s "
              "after_survivor_ids=%s pristine=%s equiv=m5(declared) crash_ids=%s"
              % ("met" if met else "unmet", len(survivors), len(MUTANTS) - len(survivors), len(MUTANTS),
                 len(r94_only), ",".join(r94_only) or "-", ",".join(survivors) or "-",
                 "green" if green else "red", ",".join(sorted(set(crashes))) or "-"))
        for mid in MUTANTS:
            print("KILL %s by=%s" % (mid, ",".join(killers[mid]) or "NONE"))
        for fid in fixtures:
            print("PRISTINE %s %s" % (fid, " ".join(map(str, results[("pristine", fid)]))))
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
