#!/usr/bin/env python3
"""mori-scorecard-calibration.py -- C1 calibration counter (mori round 96, wave w1, seat CalibExec).

Predicate P1 (same sentence as .ufo/waves/round-96/contract.md section C1): at revision R, for
each of the six axes the `Last change` cell leads with the round and verdict word of the highest
admitted mori closure row (any round, no round bound) that graded that axis improved or harmed,
and the `Score` and `Evidence pointer` cells equal their bytes at
66c5518e239eeacd6070be26d78085ef702392cb.

Command:
    mori-scorecard-calibration.py <rev> [--manifest PATH] [--repo DIR] [--base REV]
    mori-scorecard-calibration.py --selftest

Defaults: --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json
          --repo      /home/vgpnk/Projects/shokunin/mori-shokunin
          --base      66c5518e239eeacd6070be26d78085ef702392cb

Per axis:  axis <name> cell=<round_N_verdict|none> expect=<round_N_verdict|none> state=ok|mismatch|error
Summary:   C1=met|unmet axes=6 mismatches=M columns_unchanged=yes|no rows=R rev=<sha12>

The frozen round-79 counter is NOT amended by this file; this is the NEW unbounded counter the
L1 promotes to tools/ after integration. Exit codes: 0 met, 1 unmet, 2 setup (bad git,
unreadable manifest). Standard library only. --selftest builds its fixtures in a temp dir under
TMPDIR (tempfile honors the environment; /tmp is never hardcoded).
"""

import argparse
import contextlib
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AXES = ("coverage", "operability", "depth", "freshness", "calibration", "adjacency")
VERDICT_WORDS = ("improved", "harmed")
BASE_DEFAULT = "66c5518e239eeacd6070be26d78085ef702392cb"
MANIFEST_DEFAULT = "/home/vgpnk/Projects/shokunin/MANIFEST.json"
REPO_DEFAULT = "/home/vgpnk/Projects/shokunin/mori-shokunin"
ROUND_RE = re.compile(r"round\s+(\d+)")
AXES_HEADING_RE = re.compile(r"^##\s+Axes\s*$")


class SetupError(Exception):
    """Bad git state or unreadable manifest -> exit 2."""


def git_out(repo, *args):
    """Read-only git helper; any failure is a setup error (exit 2)."""
    try:
        proc = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    except OSError as exc:
        raise SetupError("git not runnable: %s" % (exc,))
    if proc.returncode != 0:
        raise SetupError(
            "git -C %s %s failed: %s" % (repo, " ".join(args), proc.stderr.strip())
        )
    return proc.stdout


def resolve_rev(repo, rev):
    return git_out(repo, "rev-parse", "--verify", "%s^{commit}" % rev).strip()


def load_expectations(path):
    """Highest admitted mori closure round per axis from MANIFEST.json (any round, no bound)."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except OSError as exc:
        raise SetupError("manifest unreadable: %s" % (exc,))
    except ValueError as exc:
        raise SetupError("manifest unparsable: %s" % (exc,))
    if not isinstance(data, dict) or not isinstance(data.get("rounds"), list):
        raise SetupError("manifest rounds[] missing")
    expected = {}
    for row in data["rounds"]:
        if not isinstance(row, dict):
            continue
        if row.get("lane") != "mori":
            continue
        if row.get("admitted") is not True:
            continue
        rnd = row.get("round")
        if isinstance(rnd, bool) or not isinstance(rnd, int):
            continue
        verdicts = row.get("verdicts")
        if not isinstance(verdicts, dict):
            continue
        for axis in AXES:
            word = verdicts.get(axis)
            if word in VERDICT_WORDS and (axis not in expected or rnd > expected[axis][0]):
                expected[axis] = (rnd, word)
    return expected


def split_cells(line):
    parts = line.split("|")
    if len(parts) < 3:
        return []
    return [part.strip() for part in parts[1:-1]]


def parse_axes(text):
    """Rows of the ## Axes table keyed by axis name, plus per-axis problems.

    A duplicate axis row is an error for that axis (first row kept for display/comparison);
    a missing '## Axes' section flags all six axes as errors.
    """
    rows = {}
    problems = {}
    all_lines = text.splitlines()
    start = None
    for idx, line in enumerate(all_lines):
        if AXES_HEADING_RE.match(line):
            start = idx + 1
            break
    if start is None:
        return rows, {axis: "no '## Axes' section" for axis in AXES}
    for line in all_lines[start:]:
        if line.startswith("## "):
            break
        if not line.lstrip().startswith("|"):
            continue
        cells = split_cells(line)
        if len(cells) < 4:
            continue
        axis = cells[0]
        if axis not in AXES:
            continue
        if axis in rows:
            problems[axis] = "duplicate axis row"
            continue
        rows[axis] = {
            "score": cells[1],
            "evidence": cells[2],
            "last_change": cells[3],
        }
    return rows, problems


def cell_round_verdict(cell):
    """(round, verdict) from a Last change cell: first `round N`; first improved|harmed
    occurring in the text before the first ';'. Either element may be None when absent."""
    match = ROUND_RE.search(cell)
    rnd = int(match.group(1)) if match else None
    head = cell.split(";", 1)[0]
    verdict = None
    pos = None
    for word in VERDICT_WORDS:
        found = head.find(word)
        if found != -1 and (pos is None or found < pos):
            pos, verdict = found, word
    return rnd, verdict


def fmt_pair(rnd, verdict):
    if rnd is None:
        return "none"
    return "round_%d_%s" % (rnd, verdict if verdict is not None else "none")


def measure(args):
    """One measurement pass. Returns (exit_code, stdout_text)."""
    rev_full = resolve_rev(args.repo, args.rev)
    base_full = resolve_rev(args.repo, args.base)
    text_rev = git_out(args.repo, "show", "%s:SCORECARD.md" % rev_full)
    text_base = git_out(args.repo, "show", "%s:SCORECARD.md" % base_full)
    expected = load_expectations(args.manifest)
    rows, problems = parse_axes(text_rev)
    base_rows, _base_problems = parse_axes(text_base)

    lines = []
    mismatches = 0
    errors = 0
    columns_ok = True
    for axis in AXES:
        row = rows.get(axis)
        base_row = base_rows.get(axis)
        expect_disp = fmt_pair(*expected[axis]) if axis in expected else "none"
        cell_disp = "none"
        state = "ok"
        if axis in problems or row is None or base_row is None:
            state = "error"
            columns_ok = False
            if row is not None:
                cell_disp = fmt_pair(*cell_round_verdict(row["last_change"]))
        else:
            rnd, verdict = cell_round_verdict(row["last_change"])
            cell_disp = fmt_pair(rnd, verdict)
            if row["score"] != base_row["score"] or row["evidence"] != base_row["evidence"]:
                columns_ok = False
            want = expected.get(axis)
            if want is None or rnd != want[0] or verdict != want[1]:
                state = "mismatch"
        if state == "mismatch":
            mismatches += 1
        elif state == "error":
            errors += 1
        lines.append("axis %s cell=%s expect=%s state=%s" % (axis, cell_disp, expect_disp, state))

    met = mismatches == 0 and errors == 0 and columns_ok
    lines.append(
        "C1=%s axes=%d mismatches=%d columns_unchanged=%s rows=%d rev=%s"
        % (
            "met" if met else "unmet",
            len(AXES),
            mismatches,
            "yes" if columns_ok else "no",
            len(rows),
            rev_full[:12],
        )
    )
    return (0 if met else 1), "\n".join(lines)


# ---------------------------------------------------------------------------
# --selftest: fixtures under TMPDIR, eleven arms (spec requires at least six).

GOOD_CELLS = {
    "coverage": "round 80 (improved, score held); round 78 (harmed) before",
    "operability": "round 93 (improved, score held); round 78 improved before",
    "depth": "round 86 (improved, score held)",
    "freshness": "round 82 (improved, score held)",
    "calibration": "round 93 (improved, score held)",
    "adjacency": "round 19 (improved, score held)",
}

FIXTURE_MANIFEST = {
    "rounds": [
        {"round": 78, "lane": "mori", "admitted": True, "verdicts": {"coverage": "harmed"}},
        {"round": 80, "lane": "mori", "admitted": True, "verdicts": {"coverage": "improved"}},
        {"round": 86, "lane": "mori", "admitted": True, "verdicts": {"depth": "improved"}},
        {"round": 82, "lane": "mori", "admitted": True, "verdicts": {"freshness": "improved"}},
        {"round": 93, "lane": "mori", "admitted": True,
         "verdicts": {"calibration": "improved", "operability": "improved"}},
        {"round": 19, "lane": "mori", "admitted": True, "verdicts": {"adjacency": "improved"}},
        {"round": 90, "lane": "mori", "admitted": False, "verdicts": {"operability": "improved"}},
        {"round": 99, "lane": "mori", "admitted": True, "verdicts": {"operability": "neutral"}},
    ]
}

ARM_EXPECT = {
    "conformant_met": {
        "exit": 0,
        "contains": [
            "axis coverage cell=round_80_improved expect=round_80_improved state=ok",
            "C1=met axes=6 mismatches=0 columns_unchanged=yes rows=6",
        ],
        "state_ok_count": 6,
    },
    "stale_cell_unmet": {
        "exit": 1,
        "contains": [
            "axis operability cell=round_78_improved expect=round_93_improved state=mismatch",
            "C1=unmet axes=6 mismatches=1 columns_unchanged=yes rows=6",
        ],
    },
    "not_admitted_higher_ignored_met": {
        "exit": 0,
        "contains": [
            "axis operability cell=round_93_improved expect=round_93_improved state=ok",
            "C1=met axes=6 mismatches=0 columns_unchanged=yes rows=6",
        ],
    },
    "verdict_word_missing_unmet": {
        "exit": 1,
        "contains": [
            "axis operability cell=round_93_none expect=round_93_improved state=mismatch",
            "C1=unmet axes=6 mismatches=1 columns_unchanged=yes rows=6",
        ],
    },
    "duplicate_axis_row_unmet": {
        "exit": 1,
        "contains": [
            "axis operability cell=round_93_improved expect=round_93_improved state=error",
            "C1=unmet axes=6 mismatches=0 columns_unchanged=no rows=6",
        ],
    },
    "score_cell_changed_unmet": {
        "exit": 1,
        "contains": [
            "axis operability cell=round_93_improved expect=round_93_improved state=ok",
            "C1=unmet axes=6 mismatches=0 columns_unchanged=no rows=6",
        ],
    },
    "evidence_cell_changed_unmet": {
        "exit": 1,
        "contains": [
            "axis freshness cell=round_82_improved expect=round_82_improved state=ok",
            "C1=unmet axes=6 mismatches=0 columns_unchanged=no rows=6",
        ],
    },
    "cell_round_missing_unmet": {
        "exit": 1,
        "contains": [
            "axis depth cell=none expect=round_86_improved state=mismatch",
            "C1=unmet axes=6 mismatches=1 columns_unchanged=yes rows=6",
        ],
    },
    "no_admitted_expectation_mismatch": {
        "exit": 1,
        "contains": [
            "axis calibration cell=round_93_improved expect=none state=mismatch",
            "C1=unmet axes=6 mismatches=1 columns_unchanged=yes rows=6",
        ],
    },
    "verdict_word_disagrees_unmet": {
        "exit": 1,
        "contains": [
            "axis coverage cell=round_80_harmed expect=round_80_improved state=mismatch",
            "C1=unmet axes=6 mismatches=1 columns_unchanged=yes rows=6",
        ],
    },
}


def scorecard_text(cells, score_overrides=None, evidence_overrides=None, extra_rows=()):
    scores = {"coverage": "6", "operability": "7", "depth": "5",
              "freshness": "5", "calibration": "5", "adjacency": "6"}
    evidence = {"coverage": "cov-evidence", "operability": "oper-evidence",
                "depth": "depth-evidence", "freshness": "fresh-evidence",
                "calibration": "calib-evidence", "adjacency": "adj-evidence"}
    if score_overrides:
        scores.update(score_overrides)
    if evidence_overrides:
        evidence.update(evidence_overrides)
    lines = [
        "# Scorecard (fixture)",
        "",
        "## Axes",
        "",
        "| Axis | Score | Evidence pointer | Last change |",
        "|---|---|---|---|",
    ]
    for axis in AXES:
        lines.append("| %s | %s | %s | %s |" % (axis, scores[axis], evidence[axis], cells[axis]))
    lines.extend(extra_rows)
    lines.extend(["", "## Foot", "", "Trailing prose.", ""])
    return "\n".join(lines)


def arms():
    """Yield (name, manifest_obj, rev_scorecard_text); the base scorecard is always conformant."""
    base_text = scorecard_text(GOOD_CELLS)
    yield ("conformant_met", copy.deepcopy(FIXTURE_MANIFEST), base_text)

    stale = dict(GOOD_CELLS, operability="round 78 (improved, score held); round 13 improved")
    yield ("stale_cell_unmet", copy.deepcopy(FIXTURE_MANIFEST), scorecard_text(stale))

    manifest = copy.deepcopy(FIXTURE_MANIFEST)
    manifest["rounds"].append({"round": 100, "lane": "mori", "admitted": False,
                               "verdicts": {"operability": "improved", "depth": "harmed"}})
    yield ("not_admitted_higher_ignored_met", manifest, base_text)

    no_verdict = dict(GOOD_CELLS, operability="round 93 (see LOG; graded improved)")
    yield ("verdict_word_missing_unmet", copy.deepcopy(FIXTURE_MANIFEST), scorecard_text(no_verdict))

    duplicate = scorecard_text(
        GOOD_CELLS, extra_rows=["| operability | 7 | oper-evidence | round 93 (improved) |"])
    yield ("duplicate_axis_row_unmet", copy.deepcopy(FIXTURE_MANIFEST), duplicate)

    score_changed = scorecard_text(GOOD_CELLS, score_overrides={"operability": "8"})
    yield ("score_cell_changed_unmet", copy.deepcopy(FIXTURE_MANIFEST), score_changed)

    evidence_changed = scorecard_text(GOOD_CELLS, evidence_overrides={"freshness": "fresh-evidence-v2"})
    yield ("evidence_cell_changed_unmet", copy.deepcopy(FIXTURE_MANIFEST), evidence_changed)

    no_round = dict(GOOD_CELLS, depth="improved recently; see closure")
    yield ("cell_round_missing_unmet", copy.deepcopy(FIXTURE_MANIFEST), scorecard_text(no_round))

    manifest = copy.deepcopy(FIXTURE_MANIFEST)
    del manifest["rounds"][4]["verdicts"]["calibration"]
    yield ("no_admitted_expectation_mismatch", manifest, base_text)

    harmed = dict(GOOD_CELLS, coverage="round 80 (harmed, score held)")
    yield ("verdict_word_disagrees_unmet", copy.deepcopy(FIXTURE_MANIFEST), scorecard_text(harmed))


def commit_fixture(repo):
    staged = subprocess.run(["git", "-C", repo, "add", "-A"],
                            capture_output=True, text=True)
    if staged.returncode != 0:
        raise RuntimeError("fixture git add failed: %s" % (staged.stderr.strip(),))
    commit = subprocess.run(
        ["git", "-C", repo, "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
         "commit", "--allow-empty", "-q", "-m", "fixture"],
        capture_output=True, text=True)
    if commit.returncode != 0:
        raise RuntimeError(
            "fixture git commit failed rc=%d: stderr=%r stdout=%r"
            % (commit.returncode, commit.stderr.strip(), commit.stdout.strip()))


def build_fixture(root, manifest_obj, base_text, rev_text):
    """Fixture lane repo under <root>/repo; manifest kept beside it (root/MANIFEST.json)."""
    repo = os.path.join(root, "repo")
    os.makedirs(repo)
    inited = subprocess.run(["git", "init", "-q", "-b", "master", repo],
                            capture_output=True, text=True)
    if inited.returncode != 0:
        subprocess.run(["git", "init", "-q", repo], capture_output=True, text=True, check=True)
    top = git_out(repo, "rev-parse", "--show-toplevel").strip()
    if top != os.path.realpath(repo):
        raise AssertionError("fixture toplevel mismatch: %s != %s" % (top, os.path.realpath(repo)))
    manifest_path = os.path.join(root, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest_obj, handle)
    with open(os.path.join(repo, "SCORECARD.md"), "w", encoding="utf-8") as handle:
        handle.write(base_text)
    commit_fixture(repo)
    with open(os.path.join(repo, "SCORECARD.md"), "w", encoding="utf-8") as handle:
        handle.write(rev_text)
    commit_fixture(repo)
    base_sha = git_out(repo, "rev-parse", "HEAD~1").strip()
    return repo, manifest_path, base_sha


def run_capture(argv):
    out_buf, err_buf = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
        code = run(argv)
    return code, out_buf.getvalue(), err_buf.getvalue()


def selftest():
    tmp_root = tempfile.mkdtemp(prefix="mori-calib-selftest-")
    passed = 0
    failed = 0
    try:
        base_text = scorecard_text(GOOD_CELLS)
        for name, manifest_obj, rev_text in arms():
            work = tempfile.mkdtemp(dir=tmp_root, prefix=name + "-")
            repo, manifest_path, base_sha = build_fixture(work, manifest_obj, base_text, rev_text)
            result = run_capture(
                ["HEAD", "--manifest", manifest_path, "--repo", repo, "--base", base_sha])
            code, out, _err = result
            spec = ARM_EXPECT[name]
            problems = []
            if code != spec["exit"]:
                problems.append("exit %d != expected %d" % (code, spec["exit"]))
            for needle in spec.get("contains", ()):
                if needle not in out:
                    problems.append("missing %r" % (needle,))
            want_ok = spec.get("state_ok_count")
            if want_ok is not None and out.count("state=ok") != want_ok:
                problems.append("state=ok count %d != %d" % (out.count("state=ok"), want_ok))
            if problems:
                failed += 1
                print("arm %s: FAIL (%s)" % (name, "; ".join(problems)))
                print(out.rstrip())
            else:
                passed += 1
                print("arm %s: pass" % (name,))
        # setup arm: unreadable manifest -> exit 2
        work = tempfile.mkdtemp(dir=tmp_root, prefix="setup_bad_manifest_exit2-")
        repo, _unused, base_sha = build_fixture(work, copy.deepcopy(FIXTURE_MANIFEST),
                                                base_text, base_text)
        missing = os.path.join(work, "absent", "MANIFEST.json")
        code, _out, err = run_capture(
            ["HEAD", "--manifest", missing, "--repo", repo, "--base", base_sha])
        if code == 2 and "setup error" in err:
            passed += 1
            print("arm setup_bad_manifest_exit2: pass")
        else:
            failed += 1
            print("arm setup_bad_manifest_exit2: FAIL (exit=%d err=%r)" % (code, err))
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)
    print("CALIB_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if failed == 0 else 1


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mori-scorecard-calibration.py",
        description="C1 calibration counter for mori (round 96, wave w1).",
    )
    parser.add_argument("rev", nargs="?", default=None,
                        help="revision whose SCORECARD.md is measured (required unless --selftest)")
    parser.add_argument("--manifest", default=MANIFEST_DEFAULT,
                        help="fleet MANIFEST.json path (default: %(default)s)")
    parser.add_argument("--repo", default=REPO_DEFAULT,
                        help="lane repo for read-only git reads (default: %(default)s)")
    parser.add_argument("--base", default=BASE_DEFAULT,
                        help="frozen base revision for the Score/Evidence column check (default: %(default)s)")
    parser.add_argument("--selftest", action="store_true",
                        help="run fixture arms under TMPDIR; print CALIB_SELFTEST pass=N fail=M")
    return parser


def run(argv):
    args = build_parser().parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        build_parser().error("rev is required unless --selftest")
    try:
        code, text = measure(args)
    except SetupError as exc:
        print("setup error: %s" % (exc,), file=sys.stderr)
        return 2
    print(text)
    return code


def main():
    sys.exit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
