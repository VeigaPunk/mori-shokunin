#!/usr/bin/env python3
"""mori round-85 C2 counter (calibration): every after receipt binds command, revision and bytes.

Frozen predicate P-C2 (`.ufo/waves/round-85/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-85/count-c2.py R` prints
  `C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0` and exits 0,
  where each of the three frozen receipts carries exactly one `# cmd:`, one `# rev:` (40-hex),
  one `# limits:` line and at least one `# counter-sha256: <64-hex> <repo-relative path>` line;
  the `# rev:` resolves to a commit that is R or an ancestor of R; every bound path's bytes at
  that revision hash to the stated sha256; and the receipt body (after the single `# ---` line)
  carries its frozen summary token.

Rule (frozen): a duplicate cmd/rev/limits line, a missing header, a non-ancestor revision, a hash
that does not match the named path at that revision, or a missing summary token is a mismatch.
`bindings` counts `# counter-sha256:` lines; `bound` counts the ones whose hash verifies. Exit 2 is
setup, never a pass.

Usage: count-c2.py <rev> [--repo DIR] | count-c2.py --selftest
Output: one `RECEIPT <name> ...` line per receipt, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; no files are written.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

# The three frozen receipts: path -> (frozen summary token, why the receipt exists).
RECEIPTS = (
    (".ufo/waves/round-85/evidence/after-r85.txt", "C1=met",
     "the three after runs at the measured revision (D84-4)"),
    (".ufo/waves/round-85/evidence/record-sweep-r85.txt", "RECORD_SWEEP",
     "the record sweep run quoted by the r84 report without a receipt (D84-4)"),
    (".ufo/waves/round-85/evidence/claim-sweep-r85.txt", "CLAIM_SWEEP",
     "the claim sweep run quoted by the r84 report without a receipt (D84-4)"),
)

CMD = re.compile(r"^#\s*cmd:\s*(\S.*)$")
REV = re.compile(r"^#\s*rev:\s*([0-9a-f]{40})\s*$")
LIMITS = re.compile(r"^#\s*limits:\s*(\S.*)$")
SHA = re.compile(r"^#\s*counter-sha256:\s*([0-9a-f]{64})\s+(\S+)\s*$")
HEADER_ANY = re.compile(r"^#\s*(cmd|rev|limits):\s*(.*)$")
SHA_ANY = re.compile(r"^#\s*counter-sha256:\s*(.*)$")
SEP = re.compile(r"^#\s*---\s*$")
HEX = re.compile(r"^[0-9a-f]{40}$")


def run(cmd, cwd=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull,
                                   GIT_CONFIG_SYSTEM=os.devnull),
                          timeout=timeout)


def parse_receipt(text):
    """Parse one receipt's header block. Returns (fields, problems).

    The header block is everything before the first `# ---` line; a `# cmd:`/`# rev:`/
    `# limits:`/`# counter-sha256:` after the separator is body text and is never a header.
    Header lines are matched loosely (any value, even empty or malformed) so a second
    malformed `# rev:` is a duplicate/bad-rev problem rather than an invisible line.
    fields: cmd, rev, limits, bindings [(sha, path)], body.
    """
    fields = {"cmd": None, "rev": None, "limits": None, "bindings": [], "body": ""}
    problems = []
    lines = text.splitlines()
    separators = [number for number, line in enumerate(lines, 1) if SEP.match(line)]
    if not separators:
        problems.append("missing-separator")
        header_lines = lines
        body = ""
    else:
        header_lines = lines[:separators[0] - 1]
        body = "\n".join(lines[separators[0]:])
        if len(separators) > 1:
            problems.append("duplicate-separator")
    seen = {"cmd": 0, "rev": 0, "limits": 0}
    for line in header_lines:
        m = HEADER_ANY.match(line)
        if m:
            name, value = m.group(1), m.group(2).strip()
            seen[name] += 1
            fields[name] = value
            continue
        m = SHA_ANY.match(line)
        if m:
            payload = m.group(1).strip()
            parsed = SHA.match("# counter-sha256: " + payload)
            if parsed is None:
                problems.append("malformed-binding")
                fields["bindings"].append(("", payload))
            else:
                fields["bindings"].append((parsed.group(1), parsed.group(2)))
    for name in ("cmd", "rev", "limits"):
        if seen[name] == 0:
            problems.append("missing-" + name)
        elif seen[name] > 1:
            problems.append("duplicate-" + name)
        elif fields[name] == "":
            problems.append("empty-" + name)
    if not fields["bindings"]:
        problems.append("missing-binding")
    if fields["rev"] is not None and fields["rev"] and not HEX.match(fields["rev"]):
        problems.append("bad-rev")
    limits = (fields["limits"] or "").lower()
    if fields["limits"] is not None and fields["limits"] != "" and (
            "limit" not in limits or len(limits.split()) < 3):
        problems.append("weak-limits")
    fields["body"] = body
    return fields, problems


def safe_path(path):
    """A repo-relative path with no traversal or absolute root."""
    if not path or path.startswith("/") or "\\" in path:
        return False
    parts = path.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def verify_bindings(bindings, loader):
    """Return (bound, mismatched, problems) for one receipt's binding list."""
    bound, mismatched, problems = 0, 0, []
    for sha, path in bindings:
        if not safe_path(path):
            mismatched += 1
            problems.append("unsafe-path:" + path)
            continue
        blob = loader(path)
        if blob is None:
            mismatched += 1
            problems.append("absent:" + path)
            continue
        measured = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        if measured == sha:
            bound += 1
        else:
            mismatched += 1
            problems.append("sha:" + path)
    return bound, mismatched, problems


def ancestor(rev, tip, git):
    """True when rev is tip or an ancestor of tip."""
    if rev == tip:
        return True
    p = run(["git", "-C", git, "merge-base", "--is-ancestor", rev, tip])
    return p.returncode == 0


def grade(loader, rev_ok, make_loader):
    """Grade the three frozen receipts.

    loader(path) reads bytes at the graded tip; make_loader(rev)(path) reads the bytes the
    receipt's own `# rev:` names — the binding is verified at THAT revision, never at the tip.
    """
    total_bindings, total_bound, revs, limits, cmds, summaries = 0, 0, 0, 0, 0, 0
    mismatch = 0
    lines = []
    for path, token, _why in RECEIPTS:
        text = loader(path)
        if text is None:
            lines.append("RECEIPT %s absent=1" % os.path.basename(path))
            mismatch += 1
            continue
        fields, problems = parse_receipt(text)
        for problem in problems:
            lines.append("PROBLEM %s %s" % (os.path.basename(path), problem))
        mismatch += len(problems)
        if fields["cmd"]:
            cmds += 1
        if fields["limits"] and not problems.count("weak-limits"):
            limits += 1
        rev = fields["rev"]
        rev_ok_here = rev is not None and rev_ok(rev)
        if rev_ok_here:
            revs += 1
        else:
            lines.append("PROBLEM %s rev=%s" % (os.path.basename(path), rev))
            mismatch += 1
        total_bindings += len(fields["bindings"])
        if rev_ok_here:
            bound, bad, why = verify_bindings(fields["bindings"], make_loader(rev))
        else:
            bound, bad, why = 0, len(fields["bindings"]), ["rev-unresolved"]
        total_bound += bound
        mismatch += bad
        for problem in why:
            lines.append("PROBLEM %s %s" % (os.path.basename(path), problem))
        has_summary = token in fields["body"]
        if has_summary:
            summaries += 1
        else:
            lines.append("PROBLEM %s summary=%s" % (os.path.basename(path), token))
            mismatch += 1
        lines.append("RECEIPT %s headers=%d rev=%d limits=%d bindings=%d bound=%d summary=%d"
                     % (os.path.basename(path),
                        1 if fields["cmd"] and fields["rev"] else 0,
                        1 if rev_ok_here else 0, 1 if fields["limits"] else 0,
                        len(fields["bindings"]), bound, 1 if has_summary else 0))
    met = (total_bindings == 5 and total_bound == 5 and revs == 3 and limits == 3
           and cmds == 3 and summaries == 3 and mismatch == 0)
    tail = ("receipts=%d bindings=%d bound=%d revs=%d limits=%d cmd=%d summary=%d mismatch=%d"
            % (len(RECEIPTS), total_bindings, total_bound, revs, limits, cmds,
               summaries, mismatch))
    return met, tail, lines


def selfcheck():
    """Detector arms over synthetic receipts (pure; no repo is read)."""
    cases = []
    good = ("# receipt\n"
            "# cmd: python3 -I count-c1.py abc\n"
            "# rev: %s\n"
            "# counter-sha256: %s tools/x.py\n"
            "# limits: named limit — the live reading is the subject's own observation\n"
            "# ---\n"
            "C1=met mutants=2\n" % ("a" * 40, hashlib.sha256(b"body").hexdigest()))
    fields, problems = parse_receipt(good)
    cases.append(("headers_ok", not problems and fields["rev"] == "a" * 40, str(problems)))
    cases.append(("body_after_separator", "C1=met" in fields["body"]
                  and "# cmd:" not in fields["body"], "body"))
    no_sha = good.replace("# counter-sha256: " + hashlib.sha256(b"body").hexdigest()
                          + " tools/x.py\n", "")
    cases.append(("missing_binding", "missing-binding" in parse_receipt(no_sha)[1], "no sha"))
    dup = good.replace("# cmd: python3 -I count-c1.py abc\n",
                       "# cmd: one\n# cmd: two\n")
    cases.append(("duplicate_cmd", "duplicate-cmd" in parse_receipt(dup)[1], "2 cmds"))
    bad_rev = good.replace("a" * 40, "zz")
    cases.append(("bad_rev", "bad-rev" in parse_receipt(bad_rev)[1]
                  or "missing-rev" in parse_receipt(bad_rev)[1], "bad"))
    weak = good.replace(
        "# limits: named limit — the live reading is the subject's own observation",
        "# limits: none")
    cases.append(("weak_limits", "weak-limits" in parse_receipt(weak)[1], "weak"))
    no_sep = good.replace("# ---\n", "")
    cases.append(("missing_separator", "missing-separator" in parse_receipt(no_sep)[1], "none"))
    loader = lambda path: "body" if path == "tools/x.py" else None
    bound, bad, why = verify_bindings([(hashlib.sha256(b"body").hexdigest(), "tools/x.py")],
                                      loader)
    cases.append(("binding_verifies", bound == 1 and bad == 0, str(why)))
    bound, bad, why = verify_bindings([("0" * 64, "tools/x.py")], loader)
    cases.append(("stale_sha_mismatch", bound == 0 and bad == 1, str(why)))
    bound, bad, why = verify_bindings([(hashlib.sha256(b"body").hexdigest(), "../x.py")],
                                      loader)
    cases.append(("unsafe_path", bound == 0 and bad == 1, str(why)))
    cases.append(("safe_path", safe_path("a/b.py") and not safe_path("/a") 
                  and not safe_path("a/../b") and not safe_path("a//b"), "path"))
    cases.append(("ancestor_equal", ancestor("b" * 40, "b" * 40, "/nonexistent"), "equal"))
    cases.append(("hex_shape", bool(HEX.match("a" * 40)) and not HEX.match("A" * 40), "hex"))
    cases.append(("receipt_count", len(RECEIPTS) == 3 and len({r[0] for r in RECEIPTS}) == 3,
                  "3"))
    body_cmd = good.replace("C1=met mutants=2\n", "C1=met mutants=2\n# cmd: quoted in body\n")
    fields_b, problems_b = parse_receipt(body_cmd)
    cases.append(("body_header_ignored",
                  not problems_b and "# cmd: quoted in body" in fields_b["body"],
                  str(problems_b)))
    malformed = good.replace(
        "# counter-sha256: " + hashlib.sha256(b"body").hexdigest() + " tools/x.py\n",
        "# counter-sha256: " + hashlib.sha256(b"body").hexdigest()[:-1] + " tools/x.py\n")
    fields_m, problems_m = parse_receipt(malformed)
    cases.append(("malformed_binding_counted",
                  "malformed-binding" in problems_m and len(fields_m["bindings"]) == 1,
                  str(problems_m)))
    dup_rev_loose = good.replace("# rev: " + "a" * 40 + "\n", "# rev: " + "a" * 40 + "\n# rev: zz\n")
    cases.append(("duplicate_rev_loose",
                  "duplicate-rev" in parse_receipt(dup_rev_loose)[1], "loose"))
    cases.append(("marker_literal", "counter-sha256" in open(os.path.abspath(__file__)).read(),
                  "marker"))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print("%s %s %s" % ("PASS" if good_case else "FAIL", label, line))
    print("C2_COUNTER_SELFTEST pass=%d fail=%d" % (ok, len(cases) - ok))
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selfcheck()
    if not a.rev:
        print("C2_SETUP usage: count-c2.py <rev> | --selftest", file=sys.stderr)
        return 2
    top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
    repo = top.stdout.strip() if top.returncode == 0 else a.repo
    p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
    if p.returncode != 0:
        print("C2_SETUP unresolvable revision " + a.rev, file=sys.stderr)
        return 2
    rev = p.stdout.strip()

    def loader(path):
        q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
        return q.stdout if q.returncode == 0 else None

    def make_loader(candidate):
        def load(path):
            q = run(["git", "-C", repo, "show", "%s:%s" % (candidate, path)])
            return q.stdout if q.returncode == 0 else None
        return load

    def rev_ok(candidate):
        q = run(["git", "-C", repo, "rev-parse", "--verify", candidate + "^{commit}"])
        if q.returncode != 0:
            return False
        return ancestor(q.stdout.strip(), rev, repo)

    present = sum(1 for path, _t, _w in RECEIPTS if loader(path) is not None)
    if present == 0:
        print("C2=unmet receipts=0 harness=absent rev=%s" % rev[:12])
        return 1
    own = run(["python3", "-I", os.path.abspath(__file__), "--selftest"])
    own_out = (own.stdout or "") + (own.stderr or "")
    own_ok = (own.returncode == 0
              and re.search(r"C2_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)
    met, tail, lines = grade(loader, rev_ok, make_loader)
    for line in lines:
        print(line)
    if not own_ok:
        print("C2=unmet %s detector=red rev=%s" % (tail, rev[:12]))
        print(own_out.strip())
        return 1
    if not met:
        print("C2=unmet %s detector=green rev=%s" % (tail, rev[:12]))
        return 1
    print("C2=met %s detector=green rev=%s" % (tail, rev[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
