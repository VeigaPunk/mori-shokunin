#!/usr/bin/env python3
"""mori round-86 C3 counter (depth): the classification is reconciled with a value observation.

Frozen predicate P-C3 (`.ufo/waves/round-86/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-86/count-c3.py R` prints
  `C3=met observations=2 aa=stable tokens=64 derived=64 name_agree=64 value_rows=19
  contradicting=2` and exits 0, where the counter runs `tools/mori-census.sh` from R's own bytes
  twice in separate scratch trees with R's baseline and `MORI_SHOKUNIN_ROOT=<fleet root>` (each
  run exits 1 with a non-empty `MORI_DRIFT:` token line; the two token lines are identical and
  every token's multiset of `key=value` occurrences in the two runs is identical); `tokens` is the
  count of `DRIFT_CLASS` rows in `corpus/evidence/drift-classification-r82.txt` and every stated
  class equals the frozen name-rule derivation; `value_rows` counts the stated `value-changed`
  rows whose token body is a bare key; and `contradicting` counts those whose field name's
  recorded value appears equal in the r10 baseline and in the live observation.

Claim type: capability acquisition (AXES.md *Capabilities*) — the value channel is the artifact.

Usage: count-c3.py <rev> [--repo DIR] [--fleet-root DIR] [--scratch DIR] | --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

CENSUS = "tools/mori-census.sh"
BASELINE = "corpus/evidence/baseline-r10-20261015T2231Z.json"
CLASSES = "corpus/evidence/drift-classification-r82.txt"
SNAPSHOT = ".ufo/waves/round-82/evidence/drift-r82-live.txt"
OBSERVATIONS = 2
CLASS_WORDS = ("added-since-r10", "value-changed", "unexplainable")
KEY = re.compile(r"(?:^|[\s(])([A-Za-z0-9_]+)=([^\s;)]*)")
KEYSHAPE = re.compile(r"^[A-Za-z0-9_]+$")
DRIFT = re.compile(r"^MORI_DRIFT:\s*(.*)$")
CLASS_LINE = re.compile(r"^DRIFT_CLASS\s+(\S+)\s+(\S+)\s*$")
NAME_SHAPE = ("SURFACE:", "FINDING:")
WORD_SHAPE = ("VERDICT", "HEADER", "BLANK")
TARGET = ("observations=2 aa=stable tokens=64 derived=64 name_agree=64 value_rows=14 "
          "contradicting=2")


def run(cmd, cwd=None, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def baseline_names(text):
    surfaces, findings = set(), set()
    for line in (text or "").splitlines():
        if line.startswith("SURFACE "):
            surfaces.add(line[len("SURFACE "):].split(":", 1)[0])
        elif line.startswith("FINDING "):
            findings.add(line[len("FINDING "):].split(" severity=", 1)[0])
    return surfaces, findings, set(match[0] for match in KEY.findall(text))


def derive(token, names):
    """The frozen r83 name-rule derivation table."""
    surfaces, findings, keys = names
    body = token.lstrip("+-")
    if body.startswith("SURFACE:"):
        return "value-changed" if body[len("SURFACE:"):] in surfaces else "added-since-r10"
    if body.startswith("FINDING:"):
        return "value-changed" if body[len("FINDING:"):] in findings else "added-since-r10"
    if body in WORD_SHAPE:
        return "value-changed"
    if not KEYSHAPE.match(body):
        return "value-changed"
    return "value-changed" if body in keys else "added-since-r10"


def volatile_fields(text):
    """The baseline header's own volatile-field list (values that move between runs)."""
    for line in (text or "").splitlines():
        if line.startswith("# volatile_fields="):
            return set(line.split("=", 1)[1].split())
    return set()


def atom_map(text, drop=frozenset()):
    """name -> Counter of the values it carries in one census output (or the baseline)."""
    atoms = {}
    for name, value in KEY.findall(text or ""):
        if name in drop:
            continue
        atoms.setdefault(name, Counter())[value] += 1
    return atoms


def atom_stable(maps):
    """True when every map is identical to the first."""
    return bool(maps) and all(maps[0] == other for other in maps[1:])


def stability(rcs, token_lines, atom_maps):
    """True when both runs agree exactly: rc 1, identical token lines, identical atom multisets."""
    if len(rcs) < 2 or any(rc != 1 for rc in rcs):
        return False
    if not all(token_lines) or any(tokens != token_lines[0] for tokens in token_lines[1:]):
        return False
    return atom_stable(atom_maps)


def token_line(text):
    tokens = []
    for line in (text or "").splitlines():
        m = DRIFT.match(line)
        if m:
            tokens = [token for token in m.group(1).split() if token != "none"]
    return tokens


def classifications(text):
    """(stated rows in order, malformed, duplicates)."""
    rows, malformed, duplicates = [], 0, 0
    seen = set()
    for line in (text or "").splitlines():
        if not line.startswith("DRIFT_CLASS"):
            continue
        m = CLASS_LINE.match(line)
        if not m or m.group(2) not in CLASS_WORDS:
            malformed += 1
            continue
        token, word = m.group(1), m.group(2)
        if token in seen:
            duplicates += 1
            continue
        seen.add(token)
        rows.append((token, word))
    return rows, malformed, duplicates


def value_body(token):
    """The bare field name of a token, or None when the name rule -- not the value channel --
    governs it (SURFACE:/FINDING:/table words)."""
    body = token.lstrip("+-")
    if body.startswith(NAME_SHAPE) or body in WORD_SHAPE or not KEYSHAPE.match(body):
        return None
    return body


def value_verdict(body, baseline_atoms, live_atoms):
    """'equal' | 'differs' | 'masked' | 'absent' for one bare key."""
    base = baseline_atoms.get(body)
    live = live_atoms.get(body)
    if not base or not live:
        return "absent"
    if set(base) == {"<V>"}:
        return "masked"
    if set(base) == set(live):
        return "equal"
    return "differs"


def observe(census, baseline, fleet_root, scratch, drift=True):
    """One census observation from R's own bytes. Returns (rc, output).

    `drift=True` runs the drift comparison (the token line); `drift=False` runs the full report
    (the value channel). Both are observations of the same subject through different surfaces.
    """
    work = tempfile.mkdtemp(dir=scratch)
    paths = {}
    for name, body in ((CENSUS, census), (BASELINE, baseline)):
        target = os.path.join(work, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)
        paths[name] = target
    env = dict(os.environ)
    env.update(TMPDIR=work, MORI_SHOKUNIN_ROOT=fleet_root)
    argv = ["bash", paths[CENSUS]]
    if drift:
        argv += ["--drift", paths[BASELINE]]
    try:
        p = run(argv, cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, ""
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def reconcile(stated, names, baseline_atoms, live_atoms):
    """(derived, name_agree, value_rows, contradicting, verdicts)."""
    derived, name_agree, value_rows, contradicting = 0, 0, 0, 0
    verdicts = []
    for token, word in stated:
        derived += 1
        expected = derive(token, names)
        if expected == word:
            name_agree += 1
        body = value_body(token)
        if word == "value-changed" and body is not None:
            value_rows += 1
            verdict = value_verdict(body, baseline_atoms, live_atoms)
            verdicts.append((token, verdict))
            if verdict == "equal":
                contradicting += 1
    return derived, name_agree, value_rows, contradicting, verdicts


def selfcheck():
    """Detector arms over synthetic inputs (pure; no census is run)."""
    cases = []
    names = ({"lane.mori"}, {"WATCHDOG_STALE"}, {"memory.peak"})
    cases.append(("derive_known_surface",
                  derive("+SURFACE:lane.mori", names) == "value-changed", "known"))
    cases.append(("derive_new_surface",
                  derive("+SURFACE:lane.new", names) == "added-since-r10", "new"))
    cases.append(("derive_word", derive("HEADER", names) == "value-changed", "word"))
    cases.append(("derive_key_unknown",
                  derive("-window", names) == "added-since-r10", "absent key"))
    rows, malformed, duplicates = classifications(
        "DRIFT_CLASS A value-changed\nDRIFT_CLASS A added-since-r10\n"
        "DRIFT_CLASS B bogus\nDRIFT_CLASS C value-changed\n")
    cases.append(("classifications",
                  rows == [("A", "value-changed"), ("C", "value-changed")]
                  and duplicates == 1 and malformed == 1, "%s %d %d" % (rows, duplicates,
                                                                        malformed)))
    cases.append(("token_line",
                  token_line("noise\nMORI_DRIFT: a b\nMORI_DRIFT: c d\n") == ["c", "d"],
                  "last line"))
    cases.append(("token_line_none", token_line("MORI_DRIFT:    \n") == [], "empty"))
    base = atom_map("x=yes y=<V> z=1")
    live = atom_map("x=yes y=2 z=3")
    cases.append(("value_equal", value_verdict("x", base, live) == "equal", "x"))
    cases.append(("value_differs", value_verdict("z", base, live) == "differs", "z"))
    cases.append(("value_masked", value_verdict("y", base, live) == "masked", "y"))
    cases.append(("value_absent", value_verdict("q", base, live) == "absent", "q"))
    cases.append(("value_body_shapes",
                  value_body("+window") == "window" and value_body("-SURFACE:journal") is None
                  and value_body("HEADER") is None and value_body("+boot") == "boot", "shapes"))
    cases.append(("stability_ok",
                  stability([1, 1], [["a"], ["a"]], [{"x": 1}, {"x": 1}]), "agree"))
    cases.append(("stability_rc0", not stability([0, 1], [["a"], ["a"]],
                                                 [{"x": 1}, {"x": 1}]), "rc0"))
    cases.append(("stability_rc2", not stability([2, 2], [["a"], ["a"]],
                                                 [{"x": 1}, {"x": 1}]), "rc2"))
    cases.append(("stability_order", not stability([1, 1], [["a", "b"], ["b", "a"]],
                                                   [{"x": 1}, {"x": 1}]), "order"))
    cases.append(("stability_atoms", not stability([1, 1], [["a"], ["a"]],
                                                   [{"x": 1}, {"x": 2}]), "atoms"))
    cases.append(("stability_empty", not atom_stable([]) and atom_stable([{"x": 1}]), "empty"))
    cases.append(("volatile_drop",
                  atom_map("a=1 age_s=2", {"age_s"}) == {"a": Counter({"1": 1})}, "drop"))
    derived, agree, value_rows, contradicting, verdicts = reconcile(
        [("+attribution", "value-changed"), ("-window", "value-changed"),
         ("HEADER", "value-changed")],
        ({"lane.mori"}, set(), {"attribution", "window"}),
        atom_map("attribution=none window=launch..NOW"),
        atom_map("attribution=inference window=launch..NOW"))
    cases.append(("reconcile_counts",
                  derived == 3 and agree == 3 and value_rows == 2 and contradicting == 1
                  and verdicts == [("+attribution", "differs"), ("-window", "equal")],
                  "%d %d %d %d" % (derived, agree, value_rows, contradicting)))
    cases.append(("observations", OBSERVATIONS == 2, "2"))
    cases.append(("marker_literal", "value_rows" in open(os.path.abspath(__file__)).read(),
                  "marker"))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C3_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--fleet-root")
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c3-r86-", dir=base)
    try:
        if a.selftest:
            return selfcheck()
        if not a.rev:
            print("C3_SETUP usage: count-c3.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print("C3_SETUP unresolvable revision " + a.rev, file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        fleet = a.fleet_root or (os.path.dirname(repo)
                                 if repo.endswith("-shokunin") else repo)
        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest"])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0
                  and re.search(r"C3_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)

        def loader(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
            return q.stdout if q.returncode == 0 else None

        census, baseline = loader(CENSUS), loader(BASELINE)
        classes, snapshot = loader(CLASSES), loader(SNAPSHOT)
        if census is None or baseline is None:
            print("C3=unmet observations=absent census/baseline=absent rev=%s" % rev[:12])
            return 1
        if classes is None or snapshot is None:
            print("C3=unmet observations=absent classification/snapshot=absent rev=%s"
                  % rev[:12])
            return 1

        runs = [observe(census, baseline, fleet, scratch) for _ in range(OBSERVATIONS)]
        fulls = [observe(census, baseline, fleet, scratch, drift=False)
                 for _ in range(OBSERVATIONS)]
        rcs = [rc for rc, _out in runs]
        token_lines = [token_line(out) for _rc, out in runs]
        vol = volatile_fields(baseline)
        live_atoms = [atom_map(out, vol) for _rc, out in fulls]
        fulls_ok = all(rc in (0, 1) for rc, _out in fulls) \
            and all("SURFACE " in out for _rc, out in fulls)
        aa = stability(rcs, token_lines, live_atoms) and fulls_ok

        rows, malformed, duplicates = classifications(classes)
        names = baseline_names(baseline)
        derived, name_agree, value_rows, contradicting, verdicts = reconcile(
            rows, names, atom_map(baseline, vol), live_atoms[0])
        tail = ("observations=%d aa=%s tokens=%d derived=%d name_agree=%d value_rows=%d "
                "contradicting=%d malformed=%d duplicates=%d"
                % (OBSERVATIONS, "stable" if aa else "unstable", len(rows), derived,
                   name_agree, value_rows, contradicting, malformed, duplicates))
        for token, verdict in verdicts:
            print("VALUE %s %s" % (token, verdict))
        if not own_ok:
            print("C3=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        met = (aa and len(rows) == 64 and derived == 64 and name_agree == 64
               and value_rows == 14 and contradicting == 2
               and malformed == 0 and duplicates == 0)
        if not met:
            print("C3=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C3=met observations=%d aa=stable tokens=%d derived=%d name_agree=%d "
              "value_rows=%d contradicting=%d rev=%s"
              % (OBSERVATIONS, len(rows), derived, name_agree, value_rows, contradicting,
                 rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
