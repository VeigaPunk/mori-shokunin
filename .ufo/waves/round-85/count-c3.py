#!/usr/bin/env python3
"""mori round-85 C3 counter (depth): the counter observes the census itself and reconciles.

Frozen predicate P-C3 (`.ufo/waves/round-85/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-85/count-c3.py R` prints
  `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0` and exits 0,
  where the counter runs `tools/mori-census.sh --drift
  corpus/evidence/baseline-r10-20261015T2231Z.json` from R's own bytes three times in scratch (each
  with R's baseline and `MORI_SHOKUNIN_ROOT=<fleet root>`), every run exits 1 with a non-empty
  `MORI_DRIFT:` token line and the three token lines are identical; the subject
  `.ufo/waves/round-83/count-c2.py` at R runs and prints a `C2=met` tail plus one
  `LIVE_DELTA <token> <class>` line per non-agreed token; the counter derives, from R's own
  baseline and classification bytes, the class of every token in the union of the snapshot's token
  line and its own observed token line; `own_tokens` equals the subject's `live_tokens`; every
  subject-named delta token carries the class the counter's own observation derives
  (`unmatched=0`); and every token the counter's own observation classifies as a non-agreed delta
  is named by the subject with that class (`unnamed=0`).

Classes (frozen, the r83 rule): `absent-live`, `added-live`,
`class-changed:<snapshot>-><live>`, `agreed`; a stated `unexplainable` class is never equal to a
derived class.

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

CENSUS = "tools/mori-census.sh"
BASELINE = "corpus/evidence/baseline-r10-20261015T2231Z.json"
SNAPSHOT = ".ufo/waves/round-82/evidence/drift-r82-live.txt"
CLASSES = "corpus/evidence/drift-classification-r82.txt"
SUBJECT = ".ufo/waves/round-83/count-c2.py"
CLASS_WORDS = ("added-since-r10", "value-changed", "unexplainable")
DRIFT = re.compile(r"^MORI_DRIFT:\s*(.*)$")
CLASS_LINE = re.compile(r"^DRIFT_CLASS\s+(\S+)\s+(\S+)\s*$")
KEY = re.compile(r"(?:^|\s)([A-Za-z0-9_]+)=")
KEYSHAPE = re.compile(r"^[A-Za-z0-9_]+$")
TAIL = re.compile(r"C2=(met|unmet)\s+(.*)$")
FIELD = re.compile(r"\b(live|live_tokens|deltas)=([A-Za-z0-9_.:-]+)")
DELTA_LINE = re.compile(r"^LIVE_DELTA\s+(\S+)\s+(\S+)$")
CLASS_WORD = re.compile(r"^(absent-live|added-live|agreed|class-changed:.+->.+)$")
OBSERVATIONS = 3


def run(cmd, cwd=None, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def baseline_names(text):
    surfaces, findings = set(), set()
    for line in text.splitlines():
        if line.startswith("SURFACE "):
            surfaces.add(line[len("SURFACE "):].split(":", 1)[0])
        elif line.startswith("FINDING "):
            findings.add(line[len("FINDING "):].split(" severity=", 1)[0])
    return surfaces, findings, set(KEY.findall(text))


def derive(token, names):
    """The frozen r83 derivation table (P-C3 names this rule, not a copy of the subject)."""
    surfaces, findings, keys = names
    body = token.lstrip("+-")
    if body.startswith("SURFACE:"):
        return "value-changed" if body[len("SURFACE:"):] in surfaces else "added-since-r10"
    if body.startswith("FINDING:"):
        return "value-changed" if body[len("FINDING:"):] in findings else "added-since-r10"
    if body in ("VERDICT", "HEADER", "BLANK"):
        return "value-changed"
    if not KEYSHAPE.match(body):
        return "value-changed"
    return "value-changed" if body in keys else "added-since-r10"


def live_delta(snapshot_tokens, live_tokens, names, stated):
    """Per-token delta over the union (snapshot order first, then live-only tokens)."""
    live_set = set(live_tokens)
    pairs, seen = [], set()
    for token in snapshot_tokens:
        if token in seen:
            continue
        seen.add(token)
        if token not in live_set:
            pairs.append((token, "absent-live"))
            continue
        snap_cls = stated.get(token) or derive(token, names)
        live_cls = derive(token, names)
        if snap_cls == live_cls:
            pairs.append((token, "agreed"))
        else:
            pairs.append((token, "class-changed:%s->%s" % (snap_cls, live_cls)))
    for token in live_tokens:
        if token not in seen:
            seen.add(token)
            pairs.append((token, "added-live"))
    return pairs


def drift_tokens(text):
    tokens = []
    for line in (text or "").splitlines():
        m = DRIFT.match(line)
        if m:
            tokens = [token for token in m.group(1).split() if token != "none"]
    return tokens


def classifications(text):
    stated, malformed, duplicates = {}, 0, 0
    for line in (text or "").splitlines():
        if not line.startswith("DRIFT_CLASS"):
            continue
        m = CLASS_LINE.match(line)
        if not m or m.group(2) not in CLASS_WORDS:
            malformed += 1
            continue
        token, word = m.group(1), m.group(2)
        if token in stated:
            duplicates += 1
            continue
        stated[token] = word
    return stated, malformed, duplicates


def subject_signal(output):
    """The subject's last C2 tail fields, its verdict and its LIVE_DELTA pairs."""
    fields = {}
    for line in output.splitlines():
        m = TAIL.search(line.strip())
        if m:
            fields = dict(FIELD.findall(m.group(2)))
            fields["verdict"] = m.group(1)
    pairs = []
    for line in output.splitlines():
        m = DELTA_LINE.match(line.strip())
        if m:
            pairs.append((m.group(1), m.group(2)))
    return fields, pairs


def subject_ok(rc, fields):
    """The subject run must exit 0 with verdict met and live derived."""
    return (rc == 0 and fields.get("verdict") == "met"
            and fields.get("live") == "derived")


def met_verdict(own_ok, stable, own_tokens, subject_tokens, unmatched, unnamed,
                malformed, duplicates):
    """The full met conjunction for one graded revision."""
    return (own_ok and stable and own_tokens and subject_tokens == len(own_tokens)
            and unmatched == 0 and unnamed == 0 and malformed == 0 and duplicates == 0)


def reconcile(own_pairs, subject_pairs):
    """(unmatched, unnamed, lines): subject classes vs the counter's own observation."""
    own = dict(own_pairs)
    subject = dict(subject_pairs)
    unmatched, unnamed, lines = 0, 0, []
    for token, word in subject_pairs:
        mine = own.get(token)
        if mine != word:
            unmatched += 1
            lines.append("RECONCILE %s subject=%s own=%s" % (token, word, mine))
    for token, word in own_pairs:
        if word == "agreed":
            continue
        if subject.get(token) != word:
            unnamed += 1
            lines.append("RECONCILE %s own=%s subject=%s" % (token, word, subject.get(token)))
    return unmatched, unnamed, lines


def observe(census, baseline, fleet_root, scratch):
    """One census observation from R's own bytes. Returns (rc, tokens, reason)."""
    work = tempfile.mkdtemp(dir=scratch)
    paths = {}
    for name, body in ((CENSUS, census), (BASELINE, baseline)):
        target = os.path.join(work, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)
        paths[name] = target
    env = dict(os.environ)
    env.update(TMPDIR=work, MORI_SHOKUNIN_ROOT=fleet_root)
    try:
        p = run(["bash", paths[CENSUS], "--drift", paths[BASELINE]], cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, [], "timeout"
    output = (p.stdout or "") + (p.stderr or "")
    return p.returncode, drift_tokens(output), ""


def stability(rcs, token_lines):
    """Every run exited 1 with a non-empty token line, and all lines are identical."""
    first = token_lines[0] if token_lines else []
    return (all(rc == 1 for rc in rcs)
            and all(bool(tokens) for tokens in token_lines)
            and all(tokens == first for tokens in token_lines[1:]))


def observe_three(census, baseline, fleet_root, scratch):
    runs = [observe(census, baseline, fleet_root, scratch) for _ in range(OBSERVATIONS)]
    rcs = [rc for rc, _tokens, _reason in runs]
    token_lines = [tokens for _rc, tokens, _reason in runs]
    stable = stability(rcs, token_lines)
    return stable, rcs, token_lines[0] if token_lines else [], runs


def subject_run(subject, rev, repo, fleet, scratch):
    work = tempfile.mkdtemp(dir=scratch)
    export = tempfile.mkdtemp(dir=scratch, prefix="subject-")
    path = os.path.join(export, SUBJECT)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(subject)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               HYAKU_SCRATCH=work)
    try:
        p = run(["python3", "-I", path, rev, "--repo", repo, "--scratch", work,
                 "--fleet-root", fleet], cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(export, ignore_errors=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def selfcheck():
    """Detector arms over synthetic inputs (pure; no census is run)."""
    cases = []
    names = ({"lane.mori"}, {"WATCHDOG_STALE"}, {"memory.peak"})
    cases.append(("derive_surface_known", derive("+SURFACE:lane.mori", names) == "value-changed",
                  "known"))
    cases.append(("derive_surface_new", derive("SURFACE:lane.new", names) == "added-since-r10",
                  "new"))
    cases.append(("derive_finding", derive("+FINDING:WATCHDOG_STALE", names) == "value-changed",
                  "finding"))
    cases.append(("derive_key", derive("+memory.peak", names) == "value-changed", "key"))
    cases.append(("derive_unknown_key", derive("+memory.max", names) == "value-changed",
                  "non-key shape"))
    cases.append(("derive_table_word", derive("VERDICT", names) == "value-changed", "verdict"))
    pairs = live_delta(["+memory.peak", "B"], ["+memory.peak", "C"], names,
                       {"+memory.peak": "value-changed"})
    cases.append(("delta_pairs", pairs == [("+memory.peak", "agreed"), ("B", "absent-live"),
                                           ("C", "added-live")], str(pairs)))
    pairs = live_delta(["SURFACE:z"], ["SURFACE:z"], names,
                       {"SURFACE:z": "value-changed"})
    cases.append(("delta_class_changed",
                  pairs == [("SURFACE:z", "class-changed:value-changed->added-since-r10")],
                  str(pairs)))
    pairs = live_delta(["+memory.peak", "+memory.peak"], ["+memory.peak"], names,
                       {"+memory.peak": "value-changed"})
    cases.append(("delta_dedupe", pairs == [("+memory.peak", "agreed")], str(pairs)))
    cases.append(("snapshot_parse",
                  drift_tokens("noise\nMORI_DRIFT: a b\nMORI_DRIFT: c d e\n")
                  == ["c", "d", "e"], "last line"))
    stated, malformed, duplicates = classifications(
        "DRIFT_CLASS A value-changed\nDRIFT_CLASS A added-since-r10\n"
        "DRIFT_CLASS B bogus\n")
    cases.append(("classifications",
                  stated == {"A": "value-changed"} and duplicates == 1 and malformed == 1,
                  "%s %d %d" % (stated, duplicates, malformed)))
    fields, pairs = subject_signal(
        "noise\nLIVE_DELTA X absent-live\n"
        "C2=met snapshot=bound live=derived live_tokens=64 live_agree=64 deltas=1\n")
    cases.append(("subject_signal", fields.get("verdict") == "met"
                  and fields.get("live") == "derived"
                  and fields.get("live_tokens") == "64" and pairs == [("X", "absent-live")],
                  str(fields)))
    unmatched, unnamed, lines = reconcile(
        [("A", "agreed"), ("B", "absent-live")],
        [("A", "agreed"), ("B", "added-live")])
    cases.append(("reconcile_mismatch", unmatched == 1 and unnamed == 1 and len(lines) == 2,
                  "%d %d" % (unmatched, unnamed)))
    unmatched, unnamed, _ = reconcile([("A", "agreed")], [("A", "agreed")])
    cases.append(("reconcile_clean", unmatched == 0 and unnamed == 0, "clean"))
    unmatched, unnamed, _ = reconcile([("A", "agreed"), ("B", "added-live")],
                                      [("A", "agreed")])
    cases.append(("reconcile_unnamed", unmatched == 0 and unnamed == 1, "unnamed"))
    cases.append(("class_words", all(CLASS_WORD.match(w) for w in
                                    ("absent-live", "added-live", "agreed",
                                     "class-changed:a->b")), "words"))
    cases.append(("class_word_bogus", not CLASS_WORD.match("vanished"), "bogus"))
    fields_u, _pairs_u = subject_signal(
        "C2=unmet snapshot=absent live=derived live_tokens=64\n")
    cases.append(("subject_verdict_required", fields_u.get("verdict") == "unmet", "unmet"))
    cases.append(("observations", OBSERVATIONS == 3, "3"))
    cases.append(("stability_rc_must_be_1",
                  not stability([0, 1, 1], [["a"], ["a"], ["a"]]), "rc 0"))
    cases.append(("stability_rc_required",
                  not stability([2, 2, 2], [["a"], ["a"], ["a"]]), "rc 2"))
    cases.append(("stability_exact_order",
                  not stability([1, 1], [["a", "b"], ["b", "a"]]), "order"))
    cases.append(("subject_verdict_met_required",
                  not subject_ok(0, {"verdict": "unmet", "live": "derived"}), "unmet"))
    cases.append(("reconcile_agreed_skip",
                  reconcile([("A", "agreed")], [])[1] == 0, "skip"))
    cases.append(("met_requires_subject_tokens",
                  not met_verdict(True, True, ["a"], 99, 0, 0, 0, 0), "99"))
    cases.append(("marker_literal", "OBSERVATIONS = 3" in open(os.path.abspath(__file__)).read(),
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
    scratch = tempfile.mkdtemp(prefix="count-c3-r85-", dir=base)
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
        classes, snapshot, subject = loader(CLASSES), loader(SNAPSHOT), loader(SUBJECT)
        if census is None or baseline is None:
            print("C3=unmet observed=absent census/baseline=absent rev=%s" % rev[:12])
            return 1
        if classes is None or snapshot is None:
            print("C3=unmet observed=absent classification/snapshot=absent rev=%s"
                  % rev[:12])
            return 1
        if subject is None:
            print("C3=unmet observed=%d subject=absent rev=%s" % (OBSERVATIONS, rev[:12]))
            return 1
        stable, rcs, own_tokens, _runs = observe_three(census, baseline, fleet, scratch)
        if not stable or not own_tokens:
            print("C3=unmet observed=%d aa=%s own_tokens=%d rcs=%s rev=%s"
                  % (OBSERVATIONS, "stable" if stable else "unstable",
                     len(own_tokens), ",".join(str(rc) for rc in rcs), rev[:12]))
            return 1
        rc, out = subject_run(subject, rev, repo, fleet, scratch)
        fields, subject_pairs = subject_signal(out)
        if not subject_ok(rc, fields):
            print("C3=unmet observed=%d aa=stable subject=unmet rc=%d rev=%s"
                  % (OBSERVATIONS, rc, rev[:12]))
            for line in out.splitlines():
                if line.startswith(("C2=", "metric=")) and len(line) < 300:
                    print(line)
            return 1
        stated, malformed, duplicates = classifications(classes)
        own_pairs = live_delta(drift_tokens(snapshot), own_tokens,
                               baseline_names(baseline), stated)
        unmatched, unnamed, lines = reconcile(own_pairs, subject_pairs)
        try:
            subject_tokens = int(fields.get("live_tokens", "-1"))
        except ValueError:
            subject_tokens = -1
        met = met_verdict(own_ok, stable, own_tokens, subject_tokens,
                          unmatched, unnamed, malformed, duplicates)
        for line in lines:
            print(line)
        for line in out.splitlines():
            if line.startswith("LIVE_DELTA") and len(line) < 300:
                print("SUBJECT " + line)
        tail = ("observed=%d aa=%s own_tokens=%d subject_tokens=%d subject_deltas=%d "
                "unmatched=%d unnamed=%d"
                % (OBSERVATIONS, "stable" if stable else "unstable", len(own_tokens),
                   subject_tokens, len(subject_pairs), unmatched, unnamed))
        if not own_ok:
            print("C3=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not met:
            print("C3=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C3=met %s detector=green rev=%s" % (tail, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
