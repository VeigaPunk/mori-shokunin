#!/usr/bin/env python3
"""mori round-91 C1 counter (calibration): the round-87 receipt gate's unarmed clause
families are armed, and every declared mutant dies attributed to its family.

Frozen predicate P-C1 (`.ufo/waves/round-91/contract.md` — this file, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-91/count-c1.py R --repo <clone>` prints
  `C1=met families=4 unarmed=0 p1_killed=<n> p1_survivors=0 p2_killed=<m> p2_survivors=0
  unattributed=0 isolated=0 pins=<a> rev=<12>` and exits 0, where `unarmed` counts the four
  named families (`c2-replay-compare-off`, `c2-supersede`, `c2-absent`,
  `c2-defeated-accounting`) with no P1 mutant at R; every P1 and P2 mutant is `killed` at R;
  and `pins` is the subject's selftest arm count at R (the counter prints it; the landing
  may change it, recorded as a supersession of the frozen round-89/90 pins, not as an edit
  of their receipts).

Populations (both frozen before data): **P1** `.ufo/waves/round-91/mutants-c1.json`,
lane-declared by `Mo91E01Arms`; **P2** `.ufo/waves/round-91/mutants-c1-independent.json`,
written by mutation-tester `Mo91M01Mut` without seeing P1. Both are read from the clone's
working tree at the given `--p1`/`--p2` paths (defaults are the two files above); an absent
P1 file means zero P1 mutants, an absent P2 file is a setup error (exit 2).

Kill rule (frozen before data): a mutant is `killed` iff `(rc!=0 or fail>0)`, its FAIL label
set is nonempty, and every FAIL label begins with the mutant's declared family name. A red
run with any label outside the family is `isolated`; a red run with no FAIL label is
`unattributed`; an absent or multiply-occurring anchor is `unanchored`; an anchor whose
replacement produces identical bytes is `empty`; a red pristine copy is `pristine`.

Per mutant line: `MUTANT <population> <id> <family> killed|isolated|unattributed|unanchored
|pristine|empty|survived rc=<n> labels=<comma list>`.

Usage: count-c1.py <rev> --repo <clone> [--p1 FILE] [--p2 FILE] [--scratch DIR]
       count-c1.py --selftest
Exit 0 met, 1 unmet, 2 setup. The subject is read with `git show <rev>:<path>` — never the
working tree. All scratch files live under --scratch (TMPDIR honoured); no /tmp literal.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SUBJECT = ".ufo/waves/round-87/count-c2.py"
P1_DEFAULT = ".ufo/waves/round-91/mutants-c1.json"
P2_DEFAULT = ".ufo/waves/round-91/mutants-c1-independent.json"

FAMILIES = ("c2-replay-compare-off", "c2-supersede", "c2-absent",
            "c2-defeated-accounting")

SELFTEST_TIMEOUT = 120
OWN_TIMEOUT = 300

SELFTEST_TALLY = re.compile(r"COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
FAIL_LABEL = re.compile(r"^FAIL\s+(\S+)", re.M)
EXPECTED_ARMS = 14


def run(cmd, cwd=None, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def clean_env(scratch):
    env = dict(os.environ)
    env.update(TMPDIR=scratch, GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull, PYTHONDONTWRITEBYTECODE="1")
    return env


def subject_selftest(path, scratch, timeout=SELFTEST_TIMEOUT):
    """Run one subject copy's own --selftest. Returns (rc, combined output)."""
    work = tempfile.mkdtemp(dir=scratch, prefix="st-")
    env = clean_env(work)
    try:
        try:
            p = run(["python3", "-I", path, "--selftest", "--scratch", work],
                    cwd=work, env=env, timeout=timeout)
        except subprocess.TimeoutExpired:
            return 124, "timeout"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def selftest_tally(out):
    """The last `COUNTER_SELFTEST pass=N fail=M` tally as (pass, fail), or (-1, -1)."""
    m = None
    for m in SELFTEST_TALLY.finditer(out):
        pass
    if m is None:
        return -1, -1
    return int(m.group(1)), int(m.group(2))


def fail_labels(out):
    """The distinct FAIL labels of one selftest run, in first-seen order."""
    seen, out_labels = set(), []
    for m in FAIL_LABEL.finditer(out or ""):
        label = m.group(1)
        if label not in seen:
            seen.add(label)
            out_labels.append(label)
    return out_labels


def green(rc, out):
    """Pristine-green: exit 0, a tally with fail=0, and no FAIL line."""
    passed, failed = selftest_tally(out)
    return rc == 0 and failed == 0 and not fail_labels(out)


def classify(rc, out, family):
    """Frozen kill rule. Returns (state, labels) where state is one of
    killed / isolated / unattributed / survived. rc 124 is a timeout: red with no
    FAIL labels, i.e. unattributed."""
    labels = fail_labels(out)
    passed, failed = selftest_tally(out)
    red = rc != 0 or failed > 0
    if not red:
        return "survived", labels
    if not labels:
        return "unattributed", labels
    if all(label.startswith(family) for label in labels):
        return "killed", labels
    return "isolated", labels


def load_population(path, what):
    """Read a mutant population JSON file from the working tree; None when absent."""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        raise ValueError("%s unreadable: %s" % (what, exc))
    if not isinstance(data, list):
        raise ValueError("%s is not a JSON list" % what)
    out = []
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError("%s entry %d is not an object" % (what, i))
        for key in ("id", "family", "anchor_old", "anchor_new"):
            if not isinstance(entry.get(key), str) or not entry[key]:
                raise ValueError("%s entry %d lacks string %r" % (what, i, key))
        out.append({"id": entry["id"], "family": entry["family"],
                    "anchor_old": entry["anchor_old"],
                    "anchor_new": entry["anchor_new"]})
    return out


def grade(scratch, subject_text, populations):
    """Grade every declared mutant against one subject text.

    populations: list of (population_name, [mutant, ...]). Returns
    (lines, counts, pins, pristine_ok)."""
    lines = []
    counts = {"p1": {"killed": 0, "survivors": 0},
              "p2": {"killed": 0, "survivors": 0},
              "unattributed": 0, "isolated": 0, "unanchored": 0}

    # (c) the pristine subject's selftest must be green; (d) pins from its tally.
    pdir = tempfile.mkdtemp(dir=scratch, prefix="pristine-")
    ppath = os.path.join(pdir, "count-c2.py")
    open(ppath, "w", encoding="utf-8").write(subject_text)
    rc, out = subject_selftest(ppath, scratch)
    shutil.rmtree(pdir, ignore_errors=True)
    pins = selftest_tally(out)[0]
    pristine_ok = green(rc, out)
    if not pristine_ok:
        # Every mutant line is still emitted (state `pristine`); nothing is run.
        for pop, mutants in populations:
            for m in mutants:
                key = "p1" if pop == "p1" else "p2"
                counts[key]["survivors"] += 1
                lines.append("MUTANT %s %s %s pristine rc=%d labels=-"
                             % (pop, m["id"], m["family"], rc))
        return lines, counts, pins, False

    # (b) anchor, replace, run, classify — one mutant at a time.
    for pop, mutants in populations:
        key = "p1" if pop == "p1" else "p2"
        for m in mutants:
            old, new, family = m["anchor_old"], m["anchor_new"], m["family"]
            n = subject_text.count(old)
            if n != 1:
                counts["unanchored"] += 1
                lines.append("MUTANT %s %s %s unanchored rc=-1 labels=-"
                             % (pop, m["id"], family))
                continue
            mutated = subject_text.replace(old, new)
            if mutated == subject_text:
                counts["unanchored"] += 1
                lines.append("MUTANT %s %s %s empty rc=-1 labels=-"
                             % (pop, m["id"], family))
                continue
            mdir = tempfile.mkdtemp(dir=scratch, prefix="mut-")
            mpath = os.path.join(mdir, "count-c2.py")
            open(mpath, "w", encoding="utf-8").write(mutated)
            mrc, mout = subject_selftest(mpath, scratch)
            shutil.rmtree(mdir, ignore_errors=True)
            state, labels = classify(mrc, mout, family)
            label_text = ",".join(labels) if labels else "-"
            if state == "killed":
                counts[key]["killed"] += 1
            elif state == "survived":
                counts[key]["survivors"] += 1
            elif state == "unattributed":
                counts["unattributed"] += 1
            else:
                counts["isolated"] += 1
            lines.append("MUTANT %s %s %s %s rc=%d labels=%s"
                         % (pop, m["id"], family, state, mrc, label_text))
    return lines, counts, pins, True


def unarmed_count(p1):
    """The four named families with no P1 mutant."""
    present = set(m["family"] for m in p1)
    return sum(1 for fam in FAMILIES if fam not in present)


def selfcheck(scratch):
    """Detector arms over synthetic subjects and populations (no lane file touched)."""
    cases = []

    fam = "c2-absent"
    good_subject = ("import sys\n"
                    "GUARD = 1\n"
                    "ok = GUARD == 1\n"
                    "print('FAIL c2-absent probe' if not ok else 'PASS c2-absent probe')\n"
                    "print('FAIL other-clause probe' if GUARD == 2 else 'PASS other probe')\n"
                    "print('COUNTER_SELFTEST pass=%d fail=%d' % (2 if ok else 1,"
                    " 0 if ok else 1))\n"
                    "sys.exit(0 if ok else 1)\n")
    red_pristine = ("import sys\n"
                    "print('FAIL c2-absent probe broken')\n"
                    "print('COUNTER_SELFTEST pass=1 fail=1')\n"
                    "sys.exit(1)\n")

    kill_mut = [{"id": "m-kill", "family": fam,
                 "anchor_old": "GUARD = 1", "anchor_new": "GUARD = 0"}]
    surv_mut = [{"id": "m-surv", "family": fam,
                 "anchor_old": "GUARD = 1", "anchor_new": "GUARD = 1  # noop"}]
    # canary unattributed: force exit 1 with an all-PASS tally -> red, no FAIL label.
    unattr_mut = [{"id": "m-canary-unattr", "family": fam,
                   "anchor_old": "sys.exit(0 if ok else 1)",
                   "anchor_new": "sys.exit(1)"}]
    # canary isolated: inject a FAIL label outside the family plus a forced exit 1.
    isolated_mut = [{"id": "m-canary-isolated", "family": fam,
                     "anchor_old": "GUARD = 1",
                     "anchor_new": ("GUARD = 1\n"
                                    "print('FAIL unrelated-clause probe')\n"
                                    "import sys as _s\n_s.exit(1)")}]
    iso_mut = [{"id": "m-iso", "family": fam,
                "anchor_old": "GUARD = 1", "anchor_new": "GUARD = 0"}]
    unanch_mut = [{"id": "m-unanch", "family": fam,
                   "anchor_old": "NO_SUCH_ANCHOR", "anchor_new": "X"}]

    # arm 1 — a correct fixture: the family-prefixed FAIL kills with attribution.
    lines, counts, pins, pok = grade(scratch, good_subject, [("p1", kill_mut)])
    cases.append(("kill_attributed",
                  pok and counts["p1"]["killed"] == 1
                  and counts["p1"]["survivors"] == 0
                  and " killed " in lines[0] and pins == 2,
                  lines[0] if lines else "no lines"))

    # arm 2 — canary unattributed: red run, no FAIL label at all.
    lines, counts, pins, pok = grade(scratch, good_subject, [("p1", unattr_mut)])
    cases.append(("canary_unattributed",
                  pok and counts["unattributed"] == 1
                  and counts["p1"]["survivors"] == 0
                  and " unattributed " in lines[0],
                  lines[0] if lines else "no lines"))

    # arm 3 — canary isolated: red run whose every FAIL label lies outside the family.
    lines, counts, pins, pok = grade(scratch, good_subject, [("p1", isolated_mut)])
    cases.append(("canary_isolated",
                  pok and counts["isolated"] == 1
                  and " isolated " in lines[0]
                  and "unrelated-clause" in lines[0],
                  lines[0] if lines else "no lines"))

    # arm 4 — empty replacement: anchor occurs once but the text is unchanged.
    lines, counts, pins, pok = grade(scratch, good_subject,
                                     [("p1", [{"id": "m-e", "family": fam,
                                               "anchor_old": "GUARD = 1",
                                               "anchor_new": "GUARD = 1"}])])
    cases.append(("empty_replacement",
                  pok and counts["unanchored"] == 1 and " empty " in lines[0],
                  lines[0] if lines else "no lines"))

    # arm 5 — red pristine: nothing is run; every mutant reads pristine.
    lines, counts, pins, pok = grade(scratch, red_pristine,
                                     [("p1", kill_mut), ("p2", iso_mut)])
    states = [line.split()[4] for line in lines]
    cases.append(("red_pristine",
                  not pok and states == ["pristine", "pristine"]
                  and counts["p1"]["survivors"] == 1
                  and counts["p2"]["survivors"] == 1,
                  " ".join(states)))

    # arm 6 — a correct fixture end to end: killed mutant, green tally, pins read.
    lines, counts, pins, pok = grade(scratch, good_subject,
                                     [("p1", kill_mut), ("p2", surv_mut)])
    cases.append(("correct_fixture",
                  pok and counts["p1"]["killed"] == 1
                  and counts["p2"]["survivors"] == 1 and pins == 2,
                  "killed=%d survivors=%d pins=%s"
                  % (counts["p1"]["killed"], counts["p2"]["survivors"], pins)))

    # arm 7 — unanchored: absent anchor and a twice-occurring anchor both refuse.
    dup_subject = good_subject + "GUARD = 1\n"
    lines, counts, pins, pok = grade(
        scratch, dup_subject,
        [("p1", unanch_mut),
         ("p1", [{"id": "m-dup", "family": fam, "anchor_old": "GUARD = 1",
                  "anchor_new": "GUARD = 0"}])])
    cases.append(("unanchored_both",
                  pok and counts["unanchored"] == 2
                  and all(" unanchored " in line for line in lines),
                  "%d unanchored" % counts["unanchored"]))

    # arm 8 — survivor: green run under the mutant is not a kill.
    lines, counts, pins, pok = grade(scratch, good_subject, [("p1", surv_mut)])
    cases.append(("survivor_green",
                  pok and counts["p1"]["survivors"] == 1
                  and " survived " in lines[0],
                  lines[0] if lines else "no lines"))

    # arm 9 — classify() boundary: family prefix vs a FAIL label outside it.
    cases.append(("classify_boundary",
                  classify(1, "FAIL c2-absent x\nCOUNTER_SELFTEST pass=0 fail=1\n",
                           fam)[0] == "killed"
                  and classify(1, "FAIL other-clause y\nFAIL c2-absent z\n"
                               "COUNTER_SELFTEST pass=0 fail=2\n",
                               fam)[0] == "isolated"
                  and classify(1, "boom\n", fam)[0] == "unattributed"
                  and classify(0, "COUNTER_SELFTEST pass=1 fail=0\n", fam)[0]
                  == "survived",
                  "killed/isolated/unattributed/survived"))

    # arm 10 — unarmed counts the four named families with no P1 mutant.
    cases.append(("unarmed_count",
                  unarmed_count([]) == 4
                  and unarmed_count([{"family": "c2-absent"}]) == 3
                  and unarmed_count([{"family": f} for f in FAMILIES]) == 0,
                  "4/3/0"))

    # arm 11 — population loader: absent file is None, bad JSON raises.
    missing = os.path.join(scratch, "no-such-population.json")
    cases.append(("loader_absent", load_population(missing, "p1") is None, "None"))
    bad = os.path.join(scratch, "bad-population.json")
    open(bad, "w", encoding="utf-8").write("{not json")
    try:
        load_population(bad, "p1")
        bad_ok = False
    except ValueError:
        bad_ok = True
    cases.append(("loader_bad_json", bad_ok, "ValueError"))

    cases.append(("marker_literal",
                  "C1_COUNTER_SELFTEST" in open(os.path.abspath(__file__)).read(),
                  "label"))
    cases.append(("own_arms_pinned", len(cases) + 1 == EXPECTED_ARMS,
                  "%d/%d" % (len(cases) + 1, EXPECTED_ARMS)))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


def met_line(counts, pins, unarmed, rev):
    """The frozen summary line; `met` only when every field matches the predicate."""
    met = (unarmed == 0 and counts["p1"]["survivors"] == 0
           and counts["p2"]["survivors"] == 0 and counts["unattributed"] == 0
           and counts["isolated"] == 0 and counts["unanchored"] == 0
           and counts["p1"]["killed"] > 0 and counts["p2"]["killed"] > 0
           and pins > 0)
    tag = "met" if met else "unmet"
    return ("C1=%s families=4 unarmed=%d p1_killed=%d p1_survivors=%d "
            "p2_killed=%d p2_survivors=%d unattributed=%d isolated=%d "
            "pins=%s rev=%s"
            % (tag, unarmed, counts["p1"]["killed"], counts["p1"]["survivors"],
               counts["p2"]["killed"], counts["p2"]["survivors"],
               counts["unattributed"], counts["isolated"],
               pins if pins > 0 else "?", rev[:12]))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", required=False, default=None)
    ap.add_argument("--p1", default=None)
    ap.add_argument("--p2", default=None)
    ap.add_argument("--scratch", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c1-r91-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev or not a.repo:
            print("C1_SETUP usage: count-c1.py <rev> --repo <clone> "
                  "[--p1 FILE] [--p2 FILE] [--scratch DIR] | --selftest",
                  file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print("C1_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()

        # (a) the subject at <rev>, via git show — never the working tree.
        q = run(["git", "-C", repo, "show", "%s:%s" % (rev, SUBJECT)])
        if q.returncode != 0:
            print("C1=unmet families=4 unarmed=4 p1_killed=0 p1_survivors=0 "
                  "p2_killed=0 p2_survivors=0 unattributed=0 isolated=0 "
                  "pins=? rev=%s subject=absent" % rev[:12])
            return 1
        subject_text = q.stdout

        p1_path = a.p1 or os.path.join(repo, P1_DEFAULT)
        p2_path = a.p2 or os.path.join(repo, P2_DEFAULT)
        try:
            p1 = load_population(p1_path, "p1")
            p2 = load_population(p2_path, "p2")
        except ValueError as exc:
            print("C1_SETUP %s" % exc, file=sys.stderr)
            return 2
        if p1 is None:
            p1 = []
        if p2 is None:
            print("C1_SETUP p2 population absent: " + p2_path, file=sys.stderr)
            return 2

        # The counter's own selftest must be green before any verdict (exit 2 otherwise).
        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch], env=clean_env(scratch), timeout=OWN_TIMEOUT)
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0
                  and re.search(r"C1_COUNTER_SELFTEST pass=%d fail=0" % EXPECTED_ARMS,
                                own_out) is not None)
        if not own_ok:
            print("C1_SETUP detector selftest red", file=sys.stderr)
            print(own_out.strip(), file=sys.stderr)
            return 2

        populations = [("p1", p1), ("p2", p2)]
        lines, counts, pins, pristine_ok = grade(scratch, subject_text, populations)
        for line in lines:
            print(line)
        unarmed = unarmed_count(p1)
        tail = met_line(counts, pins, unarmed, rev)
        if not pristine_ok:
            print("%s pristine=red" % tail)
            return 1
        print(tail)
        return 0 if tail.startswith("C1=met ") else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
