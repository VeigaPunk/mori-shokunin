#!/usr/bin/env python3
"""mori round-84 C3 counter (depth): the live reading becomes a per-token delta classification.

Frozen predicate P-C3 (`.ufo/waves/round-84/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-84/count-c3.py R` prints a `C3=met` summary carrying
  `delta=classified tokens=64`, `classified=` equal to `union=` (the union of the snapshot token
  line and the live run's token line), `residual=0` and `live=derived`, and exits 0, where the r83
  counter at R carries the `LIVE_DELTA` classifier, its selftest prints PASS for the four delta
  arms (`delta_absent_live`, `delta_added_live`, `delta_class_changed`, `delta_agreed`) with at
  least 16 arms, and its live run prints exactly one `LIVE_DELTA <token> <class>` line for every
  union token that is not `agreed`.

Classes (frozen): `absent-live`, `added-live`, `class-changed:<snapshot>-><live>`, `agreed`. The
live census reading stays an observation: `met` never requires a particular token count, only that
every token in the union is classified exactly once and that the delta-line count equals
`union - live_agree`.

Usage: count-c3.py <rev> [--repo DIR] [--scratch DIR] | count-c3.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; the subject runs in scratch only.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

SUBJECT = ".ufo/waves/round-83/count-c2.py"
MARKER = "LIVE_DELTA"
ARMS_FLOOR = 16
DELTA_ARMS = ("delta_absent_live", "delta_added_live", "delta_class_changed", "delta_agreed")
TAIL = re.compile(r"C2=(met|unmet)\s+(.*)$")
FIELD = re.compile(r"\b(delta|tokens|classified|union|residual|live|live_tokens|live_agree|"
                   r"deltas)=([A-Za-z0-9_.:-]+)")
SELFTEST = re.compile(r"C2_COUNTER_SELFTEST\s+pass=(\d+)\s+fail=(\d+)")
DELTA_LINE = re.compile(r"^LIVE_DELTA\s+(\S+)\s+(\S+)$")
CLASS_WORD = re.compile(r"^(absent-live|added-live|agreed|class-changed:.+->.+)$")


def run(cmd, cwd=None, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def write_tree(root, files):
    for name, body in files.items():
        target = os.path.join(root, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)


def selftest_run(path, scratch):
    work = tempfile.mkdtemp(dir=scratch)
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    try:
        p = run(["python3", "-I", path, "--selftest", "--scratch", work],
                cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def parse_tail(output):
    """The subject's last `C2=<verdict> <fields>` line as a field dict."""
    fields = {}
    for line in output.splitlines():
        m = TAIL.search(line.strip())
        if m:
            fields = dict(FIELD.findall(m.group(2)))
    return fields


def delta_lines(output):
    lines = []
    for line in output.splitlines():
        m = DELTA_LINE.match(line.strip())
        if m:
            lines.append((m.group(1), m.group(2)))
    return lines


def classify_ok(pairs):
    """Every delta line carries a frozen class word and no token twice."""
    tokens = [token for token, _ in pairs]
    return (all(CLASS_WORD.match(word) for _, word in pairs)
            and len(tokens) == len(set(tokens)))


def selfcheck(scratch):
    cases = []
    fields = parse_tail("noise\nC2=met snapshot=bound tokens=64 agreed=64 residual=0 "
                        "live=derived live_tokens=63 live_agree=63\n")
    cases.append(("tail_parse", fields.get("live_tokens") == "63"
                  and fields.get("residual") == "0", str(fields)))
    fields = parse_tail("C2=unmet snapshot=absent tokens=0\n")
    cases.append(("tail_verdict_absent", fields.get("live") is None, str(fields)))
    pairs = [("-FINDING:WATCHDOG_STALE", "absent-live"),
             ("FINDING:WATCHDOG_STALE", "class-changed:added-since-r10->value-changed")]
    cases.append(("class_words", classify_ok(pairs), str(pairs)))
    cases.append(("class_word_bogus", not classify_ok([("A", "vanished")]), "vanished"))
    cases.append(("duplicate_delta_token",
                  not classify_ok([("A", "absent-live"), ("A", "added-live")]), "twice"))
    out = ("PASS delta_absent_live x\nPASS delta_added_live x\n"
           "PASS delta_class_changed x\nPASS delta_agreed x\n"
           "C2_COUNTER_SELFTEST pass=16 fail=0\n")
    m = SELFTEST.search(out)
    arms = int(m.group(1)) if m else -1
    cases.append(("selftest_parse", arms == 16, str(arms)))
    cases.append(("delta_arms_present",
                  all(("PASS " + name) in out for name in DELTA_ARMS), "four arms"))
    cases.append(("arms_floor", ARMS_FLOOR == 16, "floor=%d" % ARMS_FLOOR))
    cases.append(("marker_literal", MARKER in open(os.path.abspath(__file__)).read(),
                  "marker=%s" % MARKER))
    ok = sum(1 for _, good, _ in cases if good)
    for label, good, line in cases:
        print("%s %s %s" % ("PASS" if good else "FAIL", label, line))
    print("C3_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c3-r84-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
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
        q = run(["git", "-C", repo, "show", "%s:%s" % (rev, SUBJECT)])
        subject = q.stdout if q.returncode == 0 else None
        if subject is None:
            print("C3=unmet delta=absent subject=absent rev=%s" % rev[:12])
            return 1
        if MARKER not in subject or "delta=classified" not in subject:
            print("C3=unmet delta=absent rev=%s" % rev[:12])
            return 1
        export = tempfile.mkdtemp(dir=scratch, prefix="subject-")
        write_tree(export, {SUBJECT: subject})
        path = os.path.join(export, SUBJECT)
        rc, out = selftest_run(path, scratch)
        m = SELFTEST.search(out)
        arms = int(m.group(1)) if m else -1
        arms_ok = (rc == 0 and m is not None and int(m.group(2)) == 0
                   and arms >= ARMS_FLOOR
                   and all(("PASS " + name) in out for name in DELTA_ARMS))
        if not arms_ok:
            print("C3=unmet delta=absent arms=%d selftest=red rc=%d rev=%s"
                  % (arms, rc, rev[:12]))
            for line in out.splitlines():
                if line.startswith("FAIL"):
                    print(line)
            return 1
        env = dict(os.environ)
        env.update(TMPDIR=scratch, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        try:
            r = run(["python3", "-I", path, rev, "--repo", repo, "--scratch", scratch],
                    cwd=scratch, env=env)
        except subprocess.TimeoutExpired:
            print("C3=unmet delta=classified live=timeout rev=%s" % rev[:12])
            return 1
        sout = (r.stdout or "") + (r.stderr or "")
        fields = parse_tail(sout)
        pairs = delta_lines(sout)
        try:
            union = int(fields.get("union", "-1"))
            classified = int(fields.get("classified", "-2"))
            live_agree = int(fields.get("live_agree", "-3"))
            tokens = int(fields.get("tokens", "-4"))
            residual = int(fields.get("residual", "-5"))
            deltas = int(fields.get("deltas", "-6"))
        except ValueError:
            union = classified = live_agree = tokens = residual = deltas = -1
        met = (r.returncode == 0 and fields.get("delta") == "classified"
               and tokens == 64 and union > 0 and classified == union
               and residual == 0 and fields.get("live") == "derived"
               and deltas == union - live_agree == len(pairs)
               and classify_ok(pairs))
        tail = ("delta=classified tokens=%d classified=%d union=%d residual=%d live=%s "
                "live_tokens=%s live_agree=%d deltas=%d"
                % (tokens, classified, union, residual, fields.get("live", "unavailable"),
                   fields.get("live_tokens", "0"), live_agree, len(pairs)))
        print("C3=%s %s arms=%d rev=%s" % ("met" if met else "unmet", tail, arms, rev[:12]))
        if not met:
            for line in sout.splitlines():
                if line.startswith(("C2=", "metric=", "unclassified", "LIVE_DELTA")) \
                        and len(line) < 300:
                    print(line)
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
