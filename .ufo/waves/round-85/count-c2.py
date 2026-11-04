#!/usr/bin/env python3
"""mori round-85 C2 counter (calibration), r86 shape: a receipt's body is bound to its command.

Frozen predicate P-C2 (`.ufo/waves/round-86/contract.md` — the r86 counter and this subject share
the sentence):

  At revision R `python3 -I .ufo/waves/round-86/count-c2.py R` prints
  `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4
  defeated=1 legacy=3 unexpected=0` and exits 0, where this subject at R is green in its own
  `--selftest` with exactly 21 arms and carries the arm labels `replay_match`,
  `replay_stale_mismatch`, `replay_none_requires_reason`; the subject run at R over the five
  frozen receipts prints that same line; and the counter independently executes each `required`
  receipt's `# cmd:` in a scratch export of the receipt's own `# rev:` and reproduces its body
  byte-for-byte (trailing newlines are the only normalization), while the `reject` receipt's
  body differs from its command's output in that same export.

Rule (extends the r85 grammar): a header line is `# cmd: <text>`, `# rev: <40-hex>`, `# limits:`
`<text containing "limit" and >=3 words>`, `# counter-sha256: <64-hex> <repo-relative path>`, and
a new optional `# replay: required|none` with, for `none`, `# no-replay: <>=3 words>`. A receipt
with `# replay: required` must have its body equal to the stdout of its `# cmd:`, executed in a
scratch export of the receipt's `# rev:` (cwd and TMPDIR in the export, `GIT_CONFIG_GLOBAL=/dev/null`,
`PYTHONDONTWRITEBYTECODE=1`); a nonzero rc (`replay-rc:<n>`) or a differing body
(`replay-mismatch`) is a problem. A `none` receipt without a `# no-replay:` reason is a problem
(`missing-no-replay`). The three r85 receipts carry no `# replay:` line and are graded by the r85
header grammar alone (`legacy` — the named, frozen limit: their bodies predate the replay rule).
Every receipt must meet its frozen expectation: an `expect=met` receipt has no problems, an
`expect=reject` receipt has at least one.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | count-c2.py --selftest [--scratch DIR]
Output: one `RECEIPT <name> ...` line per receipt, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The five frozen receipts of the r86 contract: path -> (summary token, expect, replay, why).
# The three r85 receipts stay `legacy` (header grammar only); the two r86 receipts carry the
# replay rule, one of them as the stale-body defeat control.
RECEIPTS = (
    (".ufo/waves/round-85/evidence/after-r85.txt", "C1=met", "met", "legacy",
     "the three after runs at the measured revision (D84-4)"),
    (".ufo/waves/round-85/evidence/record-sweep-r85.txt", "RECORD_SWEEP", "met", "legacy",
     "the record sweep run quoted by the r84 report without a receipt (D84-4)"),
    (".ufo/waves/round-85/evidence/claim-sweep-r85.txt", "CLAIM_SWEEP", "met", "legacy",
     "the claim sweep run quoted by the r84 report without a receipt (D84-4)"),
    (".ufo/waves/round-86/evidence/after-c1-r86.txt", "C1=met", "met", "required",
     "the r86 C1 after run — the body is the command's stdout at the named revision (P-C2 r86)"),
    (".ufo/waves/round-86/evidence/replay-defeat-r86.txt", "C1=met", "reject", "required",
     "stale-body defeat control: one body byte differs from the command's stdout; must read reject"),
)

CMD = re.compile(r"^#\s*cmd:\s*(\S.*)$")
REV = re.compile(r"^#\s*rev:\s*([0-9a-f]{40})\s*$")
LIMITS = re.compile(r"^#\s*limits:\s*(\S.*)$")
SHA = re.compile(r"^#\s*counter-sha256:\s*([0-9a-f]{64})\s+(\S+)\s*$")
HEADER_ANY = re.compile(r"^#\s*(cmd|rev|limits):\s*(.*)$")
SHA_ANY = re.compile(r"^#\s*counter-sha256:\s*(.*)$")
REPLAY = re.compile(r"^#\s*replay:\s*(required|none)\s*$")
NORE = re.compile(r"^#\s*no-replay:\s*(\S.*)$")
SEP = re.compile(r"^#\s*---\s*$")
HEX = re.compile(r"^[0-9a-f]{40}$")
PATHISH = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9_./-]*$")


def run(cmd, cwd=None, env=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env or dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull,
                                          GIT_CONFIG_SYSTEM=os.devnull),
                          timeout=timeout)


def parse_receipt(text):
    """Parse one receipt's header block. Returns (fields, problems).

    The header block is everything before the first `# ---` line; a `# cmd:`/`# rev:`/
    `# limits:`/`# counter-sha256:`/`# replay:` after the separator is body text and is never a
    header. Header lines are matched loosely (any value, even empty or malformed) so a second
    malformed `# rev:` is a duplicate/bad-rev problem rather than an invisible line.
    fields: cmd, rev, limits, bindings [(sha, path)], replay, no_replay, body.
    A `none` receipt without a `# no-replay:` reason of >=3 words is a problem; a receipt whose
    `# replay:` line is absent gets no problem here — `grade` applies the legacy limit.
    """
    fields = {"cmd": None, "rev": None, "limits": None, "bindings": [],
              "replay": None, "no_replay": None, "body": ""}
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
            continue
        m = REPLAY.match(line)
        if m:
            if fields["replay"] is not None:
                problems.append("duplicate-replay")
            fields["replay"] = m.group(1)
            continue
        m = NORE.match(line)
        if m:
            fields["no_replay"] = m.group(1).strip()
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
    if fields["replay"] == "none" and (fields["no_replay"] is None
                                       or len(fields["no_replay"].split()) < 3):
        problems.append("missing-no-replay")
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


def export_rev(repo, rev, cmd, dest):
    """Write every repo-relative path named in `cmd` at `rev` into `dest`."""
    written = []
    for token in re.split(r"\s+", cmd or ""):
        token = token.strip(";'\"")
        if not repo or not rev or not token or token.startswith("-") \
                or "/" not in token or not PATHISH.match(token):
            continue
        probe = run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, token)])
        if probe.returncode != 0:
            continue
        blob = run(["git", "-C", repo, "show", "%s:%s" % (rev, token)])
        if blob.returncode != 0:
            continue
        target = os.path.join(dest, token)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(blob.stdout)
        written.append(token)
    return written


def replay_receipt(fields, repo, scratch, export_rev):
    """Execute one receipt's `# cmd:` in a scratch export of its `# rev:`.

    Returns (rc, stdout, exported). The receipt body must equal stdout modulo trailing newlines;
    a nonzero rc or a differing body is a problem the caller records (`replay-rc:<n>` /
    `replay-mismatch`). The export holds only the repo-relative paths the command names, taken
    from the receipt's own revision, so the replay cannot read newer bytes.
    """
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="count-c2-replay-")
    work = tempfile.mkdtemp(dir=scratch, prefix="replay-")
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               PYTHONDONTWRITEBYTECODE="1")
    exported = export_rev(repo, fields.get("rev") or "", fields.get("cmd") or "", work)
    try:
        p = run(["bash", "-c", fields.get("cmd") or "true"], cwd=work, env=env, timeout=900)
    except subprocess.TimeoutExpired:
        shutil.rmtree(work, ignore_errors=True)
        return 124, "", exported
    shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or ""), exported


def grade(loader, rev_ok, make_loader, repo=None, scratch=None):
    """Grade the five frozen receipts under the r86 grammar and expectations.

    loader(path) reads bytes at the graded tip; make_loader(rev)(path) reads the bytes the
    receipt's own `# rev:` names — the binding is verified at THAT revision, never at the tip.
    A `required` receipt is replayed in a scratch export of its own revision; a `legacy` receipt
    keeps the r85 header grammar only (the named limit: its body predates the replay rule).
    met iff every `expect=met` receipt has no problems and the `expect=reject` receipt has at
    least one.
    """
    counts = {"bindings": 0, "bound": 0, "revs": 0, "limits": 0, "cmd": 0, "summary": 0,
              "replay": 0, "matched": 0, "defeated": 0, "legacy": 0, "unexpected": 0}
    expectations_ok = True
    lines = []
    for path, token, expect, replay_mode, _why in RECEIPTS:
        name = os.path.basename(path)
        text = loader(path)
        if text is None:
            lines.append("RECEIPT %s absent=1 expect=%s" % (name, expect))
            counts["unexpected"] += 1
            expectations_ok = False
            continue
        fields, problems = parse_receipt(text)
        counts["legacy" if replay_mode == "legacy" else "replay"] += 1
        if fields["cmd"]:
            counts["cmd"] += 1
        if (fields["limits"] and "limit" in fields["limits"].lower()
                and len(fields["limits"].split()) >= 3):
            counts["limits"] += 1
        has_summary = token in fields["body"]
        if has_summary:
            counts["summary"] += 1
        else:
            problems.append("summary=" + token)
        rev = fields["rev"]
        rev_ok_here = rev is not None and rev_ok(rev)
        if rev_ok_here:
            counts["revs"] += 1
        else:
            problems.append("rev")
        counts["bindings"] += len(fields["bindings"])
        if rev_ok_here:
            bound, bad, why = verify_bindings(fields["bindings"], make_loader(rev))
        else:
            bound, bad, why = 0, len(fields["bindings"]), ["rev-unresolved"]
        counts["bound"] += bound
        problems.extend(why)
        if replay_mode == "required" and fields["replay"] != "required":
            problems.append("missing-replay")
        if replay_mode == "required" and fields["replay"] == "required":
            rc, out, exported = replay_receipt(fields, repo, scratch, export_rev)
            if rc != 0:
                problems.append("replay-rc:%d" % rc)
            if fields["body"].rstrip("\n") != out.rstrip("\n"):
                problems.append("replay-mismatch")
            lines.append("REPLAY %s rc=%d exported=%d" % (name, rc, len(exported)))
        for problem in problems:
            lines.append("PROBLEM %s %s" % (name, problem))
        verdict = "met" if not problems else "failed"
        if expect == "reject":
            if problems:
                counts["defeated"] += 1
            else:
                counts["unexpected"] += 1
                expectations_ok = False
        elif problems:
            counts["unexpected"] += 1
            expectations_ok = False
        else:
            counts["matched"] += 1
        lines.append("RECEIPT %s expect=%s %s problems=%s rev=%d limits=%d bindings=%d "
                     "bound=%d summary=%d"
                     % (name, expect, verdict, ",".join(problems) or "-",
                        1 if rev_ok_here else 0, 1 if fields["limits"] else 0,
                        len(fields["bindings"]), bound, 1 if has_summary else 0))
    met = expectations_ok
    tail = ("receipts=%d bindings=%d bound=%d revs=%d limits=%d cmd=%d summary=%d replay=%d "
            "matched=%d defeated=%d legacy=%d unexpected=%d"
            % (len(RECEIPTS), counts["bindings"], counts["bound"], counts["revs"],
               counts["limits"], counts["cmd"], counts["summary"], counts["replay"],
               counts["matched"], counts["defeated"], counts["legacy"], counts["unexpected"]))
    return met, tail, lines


def selfcheck(scratch=None):
    """Detector arms over synthetic receipts and commands (pure except the replay arms)."""
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="count-c2-selftest-")
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
    cases.append(("receipt_count", len(RECEIPTS) == 5 and len({r[0] for r in RECEIPTS}) == 5
                  and sum(1 for r in RECEIPTS if r[3] == "legacy") == 3
                  and sum(1 for r in RECEIPTS if r[2] == "reject") == 1, "5 receipts"))
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
    # Replay arms: a synthetic `# cmd:` taped to the body it prints, then one byte stale.
    replayable = ("# receipt\n"
                  "# cmd: printf 'known body\\n'\n"
                  "# rev: %s\n"
                  "# counter-sha256: %s tools/x.py\n"
                  "# limits: named limit — the replay rule re-executes the command in an export\n"
                  "# replay: required\n"
                  "# ---\n"
                  "known body\n" % ("a" * 40, hashlib.sha256(b"body").hexdigest()))
    fields_r, problems_r = parse_receipt(replayable)
    rc_r, out_r, exported_r = replay_receipt(fields_r, None, scratch, export_rev)
    replay_problems = list(problems_r)
    if rc_r != 0:
        replay_problems.append("replay-rc:%d" % rc_r)
    if fields_r["body"].rstrip("\n") != out_r.rstrip("\n"):
        replay_problems.append("replay-mismatch")
    cases.append(("replay_match", not replay_problems and fields_r["replay"] == "required"
                  and exported_r == [], str(replay_problems)))
    fields_s, _problems_s = parse_receipt(
        replayable.replace("# ---\nknown body\n", "# ---\nknown bodY\n"))
    rc_s, out_s, _exported_s = replay_receipt(fields_s, None, scratch, export_rev)
    cases.append(("replay_stale_mismatch",
                  rc_s == 0 and fields_s["body"].rstrip("\n") != out_s.rstrip("\n")
                  and "known body" in out_s, "stale"))
    none_missing = replayable.replace("# replay: required\n", "# replay: none\n")
    cases.append(("replay_none_requires_reason",
                  "missing-no-replay" in parse_receipt(none_missing)[1], "none"))
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
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c2-r85-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
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

        present = sum(1 for row in RECEIPTS if loader(row[0]) is not None)
        if present == 0:
            print("C2=unmet receipts=0 harness=absent rev=%s" % rev[:12])
            return 1
        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0
                  and re.search(r"C2_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)
        met, tail, lines = grade(loader, rev_ok, make_loader, repo, scratch)
        for line in lines:
            print(line)
        if not own_ok:
            print("C2=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not met:
            print("C2=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C2=met " + tail)
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
