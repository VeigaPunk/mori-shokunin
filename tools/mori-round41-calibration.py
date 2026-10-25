#!/usr/bin/env python3
"""Count round-40 C2 self-assessment mismatches against the frozen r40 gate.

Usage: python3 tools/mori-round41-calibration.py <revision> --repo DIR --reference-rev REV
       python3 tools/mori-round41-calibration.py --selftest
The reference gate is loaded byte-for-byte from <reference-rev>; recorded
values are read from committed SCORECARD/LOG/lesson bytes at <revision>.

--selftest builds a synthetic git repository and record files under TMPDIR
(no network, nothing written outside it), exercises the parse and verdict
arms, prints ``MORI_R41_CALIBRATION_SELFTEST pass=<n> fail=<n>`` and exits 0
when every arm passes, 1 when one fails and 2 when the fixtures cannot be
built.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

GATE_PATH = "tools/mori-sources-appendonly.py"
RECORD_PATHS = ("SCORECARD.md", "LOG.md", "corpus/lessons/round-40.md")
CORRECTION_RE = re.compile(
    r"Round-41 calibration correction: observed_as_of=(\d+); extension_rows=(\d+)\.")
SUMMARY_RE = re.compile(r"^appendonly_violations=\d+ ids=\[([^\]]*)\]")
TIMING_RE = re.compile(r"^supersede_timing superseded_as_of=\[([^\]]*)\]")


class MeasurementError(Exception):
    pass


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, timeout=120)
    if proc.returncode:
        raise MeasurementError("git %s: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def committed_text(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def observed_counts(repo, reference_rev):
    source = committed_text(repo, reference_rev, GATE_PATH)
    with tempfile.TemporaryDirectory(prefix="mori-r41-gate-") as temp:
        gate = os.path.join(temp, "gate-v3.py")
        with open(gate, "w", encoding="utf-8") as handle:
            handle.write(source)
        proc = subprocess.run([sys.executable, gate, reference_rev, "--repo", repo],
                              capture_output=True, text=True, timeout=180)
    if proc.returncode not in (0, 1):
        raise MeasurementError("reference gate exit=%d: %s" %
                               (proc.returncode, proc.stderr.strip()))
    return parse_gate_output(proc.stdout)


def parse_gate_output(text):
    """Observed (as-of count, extension count) from reference gate stdout."""
    summary = next((SUMMARY_RE.match(line) for line in text.splitlines()
                    if SUMMARY_RE.match(line)), None)
    timing = next((TIMING_RE.match(line) for line in text.splitlines()
                  if TIMING_RE.match(line)), None)
    if summary is None or timing is None:
        raise MeasurementError("reference gate output lacks summary/timing lines")
    ids = [value for value in summary.group(1).split(",") if value]
    as_of = [value for value in timing.group(1).split(",") if value]
    return len(as_of), len(as_of) - len(ids)


def old_record(path, text):
    if path == "SCORECARD.md":
        section = text[text.rfind("## Round 40 declaration"):]
        as_match = re.search(r"measured value is \*\*(\d+) as-of ids\*\*", section)
        extension = re.search(r"(\d+) never-edited superseded rows", section)
    elif path == "LOG.md":
        section = text[text.rfind("## Round 40 "):]
        as_match = re.search(r"lane line at T1 lists (\d+) as-of ids", section)
        extension = None
    else:
        as_match = re.search(r"measured lane line at T1 lists \*\*(\d+)\*\* as-of ids", text)
        extension = re.search(r"\((\d+) rows: S226", text)
    if as_match is None:
        raise MeasurementError("cannot locate legacy r40 self-assessment in " + path)
    return int(as_match.group(1)), int(extension.group(1)) if extension else None


def recorded_counts(path, text):
    corrections = list(CORRECTION_RE.finditer(text))
    if corrections:
        match = corrections[-1]
        return int(match.group(1)), int(match.group(2))
    return old_record(path, text)


# ---- selftest -------------------------------------------------------------

SELFTEST_PREFIX = "MORI_R41_CALIBRATION_SELFTEST"
SELFTEST_GIT_ENV = {
    "PATH": os.defpath,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_PAGER": "cat",
    "LANG": "C",
}
SELFTEST_GATE = (
    "import sys\n"
    "print('supersede_timing superseded_as_of=[S1,S2,S3] stale_supersede=[]')\n"
    "print('appendonly_violations=0 ids=[S2]')\n"
    "sys.exit(0)\n"
)
SELFTEST_RECORD = (
    "Round-41 calibration correction: observed_as_of=%d; extension_rows=%d.\n"
)


def _selftest_git(repo, *arguments):
    """Run one git command inside the synthetic repository."""
    return subprocess.run(
        ["git", "-C", repo, "-c", "user.name=Mori Calibration Selftest",
         "-c", "user.email=mori-selftest@example.invalid"] + list(arguments),
        capture_output=True, text=True, timeout=60, env=SELFTEST_GIT_ENV)


def _selftest_commit(repo, message):
    """Commit the fixture worktree and return the new revision."""
    for arguments in (["add", "--", "."], ["commit", "--quiet", "-m", message]):
        proc = _selftest_git(repo, *arguments)
        if proc.returncode:
            raise MeasurementError("git %s: %s"
                                   % (arguments[0], proc.stderr.strip()))
    return _selftest_git(repo, "rev-parse", "HEAD").stdout.strip()


def _selftest_repo(root, as_of, extension):
    """Build a reference commit and a record commit; return both revisions."""
    repo = os.path.join(root, "repo")
    os.makedirs(repo)
    init = _selftest_git(repo, "init", "--quiet")
    if init.returncode:
        raise MeasurementError("git init: %s" % init.stderr.strip())
    gate = os.path.join(repo, GATE_PATH)
    os.makedirs(os.path.dirname(gate))
    with open(gate, "w", encoding="utf-8") as handle:
        handle.write(SELFTEST_GATE)
    reference = _selftest_commit(repo, "reference gate")
    for path in RECORD_PATHS:
        target = os.path.join(repo, path)
        parent = os.path.dirname(target)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(SELFTEST_RECORD % (as_of, extension))
    revision = _selftest_commit(repo, "records")
    return repo, reference, revision


def selftest():
    """Run the bounded self-test; 0 when every arm passes, 1 a failed arm, 2 setup."""
    tmpdir = os.environ.get("TMPDIR")
    if not tmpdir:
        print("SELFTEST SETUP TMPDIR is not set")
        print("%s pass=0 fail=0" % SELFTEST_PREFIX)
        return 2
    try:
        temporary = tempfile.TemporaryDirectory(
            prefix=".mori-r41-calibration-selftest-", dir=tmpdir)
    except OSError as exc:
        print("SELFTEST SETUP %s" % exc)
        print("%s pass=0 fail=0" % SELFTEST_PREFIX)
        return 2

    passed = 0
    failed = 0

    def arm(name, function):
        nonlocal passed, failed
        try:
            function()
        except Exception as exc:          # noqa: BLE001 - the selftest reports
            failed += 1
            print("SELFTEST FAIL %s: %s: %s" % (name, type(exc).__name__, exc))
        else:
            passed += 1

    def raises(function, needle):
        try:
            function()
        except MeasurementError as exc:
            assert needle in str(exc), (needle, str(exc))
            return
        raise AssertionError("MeasurementError not raised")

    with temporary as scratch:
        def cli(*arguments):
            return subprocess.run(
                [sys.executable, os.path.abspath(__file__)] + list(arguments),
                capture_output=True, text=True, timeout=120)

        def correction_line_wins():
            text = (SELFTEST_RECORD % (3, 2)) + (SELFTEST_RECORD % (4, 1))
            assert recorded_counts("LOG.md", text) == (4, 1)

        def legacy_scorecard():
            text = ("## Round 40 declaration\nmeasured value is **3 as-of ids** "
                    "and 2 never-edited superseded rows\n")
            assert recorded_counts("SCORECARD.md", text) == (3, 2)

        def legacy_log():
            text = "## Round 40 something\nlane line at T1 lists 3 as-of ids\n"
            assert recorded_counts("LOG.md", text) == (3, None)

        def legacy_lesson():
            text = ("measured lane line at T1 lists **3** as-of ids "
                    "(2 rows: S226, S227)\n")
            assert recorded_counts("corpus/lessons/round-40.md", text) == (3, 2)

        def unparseable_record():
            raises(lambda: recorded_counts("LOG.md", "nothing recorded here\n"),
                   "cannot locate legacy r40 self-assessment")

        def gate_summary_parse():
            text = ("supersede_timing superseded_as_of=[S1,S2,S3] "
                    "stale_supersede=[]\n"
                    "appendonly_violations=0 ids=[S2]\n")
            assert parse_gate_output(text) == (3, 2)

        def gate_missing_timing():
            raises(lambda: parse_gate_output("appendonly_violations=0 ids=[]\n"),
                   "lacks summary/timing lines")

        def setup_revision():
            repo, reference, _ = _selftest_repo(
                os.path.join(scratch, "setup"), 3, 2)
            proc = cli("0" * 40, "--repo", repo, "--reference-rev", reference)
            assert proc.returncode == 2, (proc.returncode, proc.stdout)
            assert "MORI_R41_CALIBRATION_SETUP" in proc.stderr, proc.stderr

        def matching_records():
            repo, reference, revision = _selftest_repo(
                os.path.join(scratch, "match"), 3, 2)
            proc = cli(revision, "--repo", repo, "--reference-rev", reference)
            assert proc.returncode == 0, (proc.returncode, proc.stderr)
            lines = proc.stdout.splitlines()
            assert lines[-1] == ("MORI_R41_CALIBRATION mismatches=0 "
                                 "observed_as_of=3 extension_rows=2"), lines
            for path in RECORD_PATHS:
                assert ("%s recorded_as_of=3 observed_as_of=3 "
                        "recorded_extension=2 observed_extension=2"
                        % path) in lines, lines

        def mismatched_records():
            repo, reference, revision = _selftest_repo(
                os.path.join(scratch, "mismatch"), 4, 1)
            proc = cli(revision, "--repo", repo, "--reference-rev", reference)
            assert proc.returncode == 1, (proc.returncode, proc.stderr)
            assert proc.stdout.splitlines()[-1] == (
                "MORI_R41_CALIBRATION mismatches=6 observed_as_of=3 "
                "extension_rows=2"), proc.stdout

        arm("correction_line_wins", correction_line_wins)
        arm("legacy_scorecard", legacy_scorecard)
        arm("legacy_log", legacy_log)
        arm("legacy_lesson", legacy_lesson)
        arm("unparseable_record_rejected", unparseable_record)
        arm("gate_summary_parse", gate_summary_parse)
        arm("gate_missing_timing_rejected", gate_missing_timing)
        arm("setup_revision", setup_revision)
        arm("matching_records", matching_records)
        arm("mismatched_records", mismatched_records)

    print("%s pass=%d fail=%d" % (SELFTEST_PREFIX, passed, failed))
    return 0 if failed == 0 else 1


def main(argv):
    argv = list(argv)
    if "--selftest" in argv:
        return selftest()
    parser = argparse.ArgumentParser()
    parser.add_argument("revision")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--reference-rev", required=True)
    args = parser.parse_args(argv)
    repo = os.path.abspath(args.repo)
    try:
        observed_as_of, observed_extension = observed_counts(repo, args.reference_rev)
        mismatches = 0
        for path in RECORD_PATHS:
            as_of, extension = recorded_counts(path, committed_text(repo, args.revision, path))
            as_bad = as_of != observed_as_of
            extension_bad = extension != observed_extension
            mismatches += int(as_bad) + int(extension_bad)
            print("%s recorded_as_of=%s observed_as_of=%d recorded_extension=%s observed_extension=%d"
                  % (path, as_of, observed_as_of,
                     "MISSING" if extension is None else extension,
                     observed_extension))
        print("MORI_R41_CALIBRATION mismatches=%d observed_as_of=%d extension_rows=%d"
              % (mismatches, observed_as_of, observed_extension))
        return 0 if mismatches == 0 else 1
    except (MeasurementError, OSError, subprocess.TimeoutExpired) as exc:
        print("MORI_R41_CALIBRATION_SETUP: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
