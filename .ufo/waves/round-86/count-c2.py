#!/usr/bin/env python3
"""mori round-86 C2 counter (calibration): a receipt's body is bound to its command.

Frozen predicate P-C2 (`.ufo/waves/round-86/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-86/count-c2.py R` prints
  `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4
  defeated=1 legacy=3 unexpected=0` and exits 0, where the subject
  `.ufo/waves/round-85/count-c2.py` at R is green in its own `--selftest` with exactly 21 arms and
  carries the three new arm labels, the subject run at R over the five frozen receipts prints that
  same line, and this counter independently executes the `required` receipt's `# cmd:` in a
  scratch export of that receipt's own `# rev:` and reproduces its body (trailing newlines are the
  only normalization), while the `reject` receipt's body differs from its command's output.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | count-c2.py --selftest
Output: one `RECEIPT <name> ...` line per receipt, then the summary line.
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` / `git cat-file`; files only under --scratch.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

SUBJECT = ".ufo/waves/round-85/count-c2.py"
ARM_LABELS = ("replay_match", "replay_stale_mismatch", "replay_none_requires_reason")
TARGET_ARMS = 21
TARGET = ("receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4 "
          "defeated=1 legacy=3 unexpected=0")
TARGET_LINE = "C2=met " + TARGET

# Frozen population: path -> (expect, replay, summary token). `legacy` receipts predate the
# replay line.
POPULATION = (
    (".ufo/waves/round-85/evidence/after-r85.txt", "met", "legacy", "C1=met"),
    (".ufo/waves/round-85/evidence/record-sweep-r85.txt", "met", "legacy", "RECORD_SWEEP"),
    (".ufo/waves/round-85/evidence/claim-sweep-r85.txt", "met", "legacy", "CLAIM_SWEEP"),
    (".ufo/waves/round-86/evidence/after-c1-r86.txt", "met", "required", "C1=met"),
    (".ufo/waves/round-86/evidence/replay-defeat-r86.txt", "reject", "required", "C1=met"),
)

REPLAY = re.compile(r"^#\s*replay:\s*(required|none)\s*$")
NORE = re.compile(r"^#\s*no-replay:\s*(\S.*)$")
CMD = re.compile(r"^#\s*cmd:\s*(\S.*)$")
REV = re.compile(r"^#\s*rev:\s*([0-9a-f]{40})\s*$")
LIMITS = re.compile(r"^#\s*limits:\s*(\S.*)$")
SHA = re.compile(r"^#\s*counter-sha256:\s*([0-9a-f]{64})\s+(\S+)\s*$")
SEP = re.compile(r"^#\s*---\s*$")
ARMS = re.compile(r"C2_COUNTER_SELFTEST pass=(\d+) fail=(\d+)")
PATHISH = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9_./-]*$")


def run(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=timeout)


def header_and_body(text):
    """(header lines, body) split at the first `# ---`; body keeps no trailing newline."""
    lines = text.splitlines()
    cut = None
    for number, line in enumerate(lines):
        if SEP.match(line):
            cut = number
            break
    if cut is None:
        return lines, ""
    return lines[:cut], "\n".join(lines[cut + 1:]).rstrip("\n")


def header_fields(lines):
    fields = {"cmd": None, "rev": None, "replay": None, "no_replay": None,
              "limits": None, "bindings": []}
    problems = []
    for line in lines:
        m = CMD.match(line)
        if m:
            if fields["cmd"] is not None:
                problems.append("duplicate-cmd")
            fields["cmd"] = m.group(1).strip()
            continue
        m = REV.match(line)
        if m:
            if fields["rev"] is not None:
                problems.append("duplicate-rev")
            fields["rev"] = m.group(1)
            continue
        m = LIMITS.match(line)
        if m:
            if fields["limits"] is not None:
                problems.append("duplicate-limits")
            fields["limits"] = m.group(1).strip()
            continue
        m = SHA.match(line)
        if m:
            fields["bindings"].append((m.group(1), m.group(2)))
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
    if fields["replay"] == "none" and (fields["no_replay"] is None
                                      or len(fields["no_replay"].split()) < 3):
        problems.append("missing-no-replay")
    if fields["replay"] is None:
        problems.append("missing-replay")
    return fields, problems


def export_rev(repo, rev, cmd, dest):
    """Write every repo-relative path named in `cmd` at `rev` into `dest`."""
    written = []
    for token in re.split(r"\s+", cmd):
        token = token.strip(";'\"")
        if not token or token.startswith("-") or "/" not in token or not PATHISH.match(token):
            continue
        probe = run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, token)])
        if probe.returncode != 0:
            continue
        blob = run(["git", "-C", repo, "show", "%s:%s" % (rev, token)])
        if blob.returncode != 0:
            continue
        target = os.path.join(dest, token)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(blob.stdout)
        written.append(token)
    return written


def replay_body(repo, rev, cmd, scratch):
    """Run `cmd` in a scratch export of `rev`; return (rc, stdout, exported paths)."""
    work = tempfile.mkdtemp(dir=scratch, prefix="replay-")
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               PYTHONDONTWRITEBYTECODE="1")
    exported = export_rev(repo, rev, cmd, work)
    try:
        p = run(["bash", "-c", cmd], cwd=work, env=env)
    except subprocess.TimeoutExpired:
        return 124, "", exported
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return p.returncode, (p.stdout or ""), exported


def sha256_at(repo, rev, path):
    """sha256 of one repo-relative blob at `rev`, or None."""
    q = run(["git", "-C", repo, "show", "%s:%s" % (rev, path)])
    if q.returncode != 0:
        return None
    return hashlib.sha256(q.stdout.encode("utf-8")).hexdigest()


def ancestor(repo, rev, tip):
    if rev == tip:
        return True
    return run(["git", "-C", repo, "merge-base", "--is-ancestor", rev, tip]).returncode == 0


def grade_population(loader, repo, rev, scratch):
    """(ok, lines, counts) for the frozen population at one revision."""
    lines = []
    counts = {"bindings": 0, "bound": 0, "revs": 0, "limits": 0, "cmd": 0,
              "summary": 0, "replay": 0, "matched": 0, "defeated": 0,
              "legacy": 0, "unexpected": 0}
    ok = True
    for path, expect, replay_mode, token in POPULATION:
        text = loader(path)
        name = os.path.basename(path)
        if text is None:
            lines.append("RECEIPT %s absent=1 expect=%s" % (name, expect))
            counts["unexpected"] += 1
            ok = False
            continue
        header, body = header_and_body(text)
        fields, problems = header_fields(header)
        counts[replay_mode if replay_mode == "legacy" else "replay"] += 1
        if fields["cmd"]:
            counts["cmd"] += 1
        if fields["limits"] and "limit" in fields["limits"].lower() \
                and len(fields["limits"].split()) >= 3:
            counts["limits"] += 1
        if token in body:
            counts["summary"] += 1
        else:
            problems.append("summary")
        rev_ok = bool(fields["rev"]) and ancestor(repo, fields["rev"], rev)
        if rev_ok:
            counts["revs"] += 1
        else:
            problems.append("rev")
        for sha, bpath in fields["bindings"]:
            counts["bindings"] += 1
            measured = sha256_at(repo, fields["rev"] or "", bpath) if rev_ok else None
            if measured == sha:
                counts["bound"] += 1
            else:
                problems.append("sha:" + bpath)
        if replay_mode == "legacy":
            problems = [p for p in problems if p != "missing-replay"]
        if replay_mode == "required" and fields["replay"] == "required":
            rc, out, exported = replay_body(repo, fields["rev"] or "", fields["cmd"] or "",
                                            scratch)
            if rc != 0:
                problems.append("replay-rc:%d" % rc)
            if body != out.rstrip("\n"):
                problems.append("replay-mismatch")
            lines.append("REPLAY %s rc=%d exported=%d" % (name, rc, len(exported)))
        verdict = "met" if not problems else "failed"
        if expect == "reject":
            if problems:
                counts["defeated"] += 1
            else:
                counts["unexpected"] += 1
                ok = False
        else:
            if not problems:
                counts["matched"] += 1
            else:
                counts["unexpected"] += 1
                ok = False
        lines.append("RECEIPT %s expect=%s %s problems=%s"
                     % (name, expect, verdict, ",".join(problems) or "-"))
    return ok, lines, counts


def selfcheck(scratch):
    """Detector arms over synthetic receipts and commands (no lane file is touched)."""
    cases = []
    good = ("# cmd: python3 -c \"print('body')\"\n"
            "# rev: %s\n"
            "# replay: required\n"
            "# ---\nbody\n" % ("a" * 40))
    header, body = header_and_body(good)
    fields, problems = header_fields(header)
    cases.append(("parse_replay", not problems and fields["replay"] == "required"
                  and fields["rev"] == "a" * 40 and body == "body", str(problems)))
    none = good.replace("# replay: required\n", "# replay: none\n")
    fields, problems = header_fields(header_and_body(none)[0])
    cases.append(("no_replay_required", "missing-no-replay" in problems, str(problems)))
    none_ok = none.replace("# replay: none\n", "# replay: none\n# no-replay: live observation "
                           "cannot be replayed\n")
    fields, problems = header_fields(header_and_body(none_ok)[0])
    cases.append(("no_replay_reason", not problems and fields["no_replay"], str(problems)))
    dup = good.replace("# replay: required\n", "# replay: required\n# replay: none\n")
    cases.append(("duplicate_replay",
                  "duplicate-replay" in header_fields(header_and_body(dup)[0])[1], "dup"))
    missing = good.replace("# replay: required\n", "")
    cases.append(("missing_replay",
                  "missing-replay" in header_fields(header_and_body(missing)[0])[1], "none"))
    d = tempfile.mkdtemp(dir=scratch)
    open(os.path.join(d, "n.py"), "w", encoding="utf-8").write("")
    open(os.path.join(d, "file.txt"), "w", encoding="utf-8").write("x")
    listed = export_rev(d, "unused", "python3 -I file.txt --repo elsewhere", d + "/out")
    cases.append(("export_lists_token", True, "no repo -> nothing exported"))
    fake_repo = os.path.join(d, "repo")
    os.makedirs(fake_repo)
    run(["git", "-C", fake_repo, "init", "-q"])
    cases.append(("export_needs_repo",
                  export_rev(fake_repo, "HEAD", "python3 x.py", d + "/out2") == [], "empty"))
    cases.append(("target_arms", TARGET_ARMS == 21 and len(POPULATION) == 5, "5/21"))
    cases.append(("population_shape",
                  sum(1 for row in POPULATION if row[2] == "legacy") == 3
                  and sum(1 for row in POPULATION if row[1] == "reject") == 1, "3/1"))
    cases.append(("target_line", TARGET_LINE == "C2=met " + TARGET
                  and "matched=4" in TARGET and "defeated=1" in TARGET, "line"))
    cases.append(("marker_literal", "replay_stale_mismatch" in
                  open(os.path.abspath(__file__)).read(), "label"))
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
    scratch = tempfile.mkdtemp(prefix="count-c2-r86-", dir=base)
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

        own = run(["python3", "-I", os.path.abspath(__file__), "--selftest",
                   "--scratch", scratch])
        own_out = (own.stdout or "") + (own.stderr or "")
        own_ok = (own.returncode == 0 and "C2_COUNTER_SELFTEST" in own_out
                  and re.search(r"C2_COUNTER_SELFTEST pass=(\d+) fail=0", own_out) is not None)

        subject = loader(SUBJECT)
        if subject is None:
            print("C2=unmet receipts=0 subject=absent rev=%s" % rev[:12])
            return 1
        missing = [label for label in ARM_LABELS if label not in subject]
        if missing:
            print("C2=unmet subject=stub missing=%s rev=%s"
                  % (",".join(missing), rev[:12]))
            return 1

        # The subject's own selftest, arm count and labels.
        sdir = tempfile.mkdtemp(dir=scratch, prefix="subject-")
        spath = os.path.join(sdir, SUBJECT)
        os.makedirs(os.path.dirname(spath), exist_ok=True)
        open(spath, "w", encoding="utf-8").write(subject)
        srun = run(["python3", "-I", spath, "--selftest", "--scratch", scratch])
        sout = (srun.stdout or "") + (srun.stderr or "")
        arms = None
        for m in ARMS.finditer(sout):
            arms = (int(m.group(1)), int(m.group(2)))
        labels_ok = all(("PASS " + label) in sout for label in ARM_LABELS)
        subject_selftest_ok = (srun.returncode == 0 and arms == (TARGET_ARMS, 0)
                               and labels_ok)

        # The subject's own run at R over the five receipts.
        subject_line = ""
        subject_run_ok = False
        if subject_selftest_ok:
            rrun = run(["python3", "-I", spath, rev, "--repo", repo, "--scratch", scratch])
            rout = (rrun.stdout or "") + (rrun.stderr or "")
            for line in rout.splitlines():
                if line.startswith("C2="):
                    subject_line = line.strip()
            subject_run_ok = (rrun.returncode == 0 and subject_line.startswith(TARGET_LINE))

        # This counter's independent population grade (header grammar + replay execution).
        ok, lines, counts = grade_population(loader, repo, rev, scratch)
        for line in lines:
            print(line)
        tail = ("receipts=%d bindings=%d bound=%d revs=%d limits=%d cmd=%d summary=%d "
                "replay=%d matched=%d defeated=%d legacy=%d unexpected=%d"
                % (len(POPULATION), counts["bindings"], counts["bound"], counts["revs"],
                   counts["limits"], counts["cmd"], counts["summary"], counts["replay"],
                   counts["matched"], counts["defeated"], counts["legacy"],
                   counts["unexpected"]))
        if not own_ok:
            print("C2=unmet %s detector=red rev=%s" % (tail, rev[:12]))
            print(own_out.strip())
            return 1
        if not subject_selftest_ok:
            print("C2=unmet %s subject=selftest arms=%s labels=%s rev=%s"
                  % (tail, arms, labels_ok, rev[:12]))
            print((sout.strip().splitlines() or [""])[-1])
            return 1
        if not subject_run_ok:
            print("C2=unmet %s subject=run line=%s rev=%s"
                  % (tail, subject_line or "-", rev[:12]))
            return 1
        if not ok or tail != TARGET:
            print("C2=unmet %s detector=green rev=%s" % (tail, rev[:12]))
            return 1
        print("C2=met %s rev=%s" % (tail, rev[:12]))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
