#!/usr/bin/env python3
"""Count round-40 C2 self-assessment mismatches against the frozen r40 gate.

Usage: python3 tools/mori-round41-calibration.py <revision> --repo DIR --reference-rev REV
The reference gate is loaded byte-for-byte from <reference-rev>; recorded
values are read from committed SCORECARD/LOG/lesson bytes at <revision>.
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
    summary = next((SUMMARY_RE.match(line) for line in proc.stdout.splitlines()
                    if SUMMARY_RE.match(line)), None)
    timing = next((TIMING_RE.match(line) for line in proc.stdout.splitlines()
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


def main(argv):
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
