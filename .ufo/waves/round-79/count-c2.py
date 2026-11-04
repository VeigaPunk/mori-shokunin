#!/usr/bin/env python3
"""mori round-79 C2 counter (calibration): the axes table against the fleet record.

Frozen predicate P-C2 (contract `.ufo/waves/round-79/contract.md`, this counter and the
receipt label are the same sentence):

  At revision R, SCORECARD.md's `## Axes` table has exactly one row per axis in
  {coverage, operability, depth, freshness, calibration, adjacency}; for each axis the
  `Last change` cell's first `round N` equals N*, the highest mori lane round <= 78 that
  MANIFEST.json records with `admitted: true` and that axis graded `improved` or `harmed`;
  and the text from that `round N` up to the next `;` carries that verdict word.

Named limit (before data): the `Evidence` cell is not graded (the r50 counter graded it);
only the `Last change` clause is in scope.

Usage: count-c2.py <rev> [--repo DIR] [--manifest PATH] [--through N]
       count-c2.py --selftest
Output: one `axis ...` line per axis, then
  `C2=met|unmet axes=6 mismatches=M errors=E manifest_rows=R through=N rev=<sha12>`
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show` on the lane repo and a plain read of
MANIFEST.json; nothing is written outside --scratch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

AXES = ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"]
LANE = "mori"
THROUGH = 78
ROUND = re.compile(r"round\s+(\d+)", re.I)
VERDICT = re.compile(r"\b(improved|harmed)\b")


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def read_blob(repo, rev, path):
    p = run(["git", "-C", repo, "show", f"{rev}:{path}"])
    return p.stdout if p.returncode == 0 else None


def axes_cells(text):
    """Return {axis: (cell_text, error)} from the `## Axes` table."""
    out, in_axes = {}, False
    for line in text.splitlines():
        if line.strip() == "## Axes":
            in_axes = True
            continue
        if in_axes and line.startswith("## "):
            break
        if not in_axes or not line.lstrip().startswith("|"):
            continue
        parts = [c.strip() for c in line.strip().split("|")[1:-1]]
        if len(parts) < 4 or parts[0] in ("Axis",) or set(parts[0]) <= set("-: "):
            continue
        if parts[0] not in AXES:
            continue
        if parts[0] in out:
            out[parts[0]] = (out[parts[0]][0], "duplicate_row")
        else:
            out[parts[0]] = (parts[3], "")
    return out


def expectations(manifest, through):
    """{axis: (round, verdict)} for the highest admitted improved/harmed mori round."""
    try:
        import json
        data = json.load(open(manifest))
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"manifest_unreadable:{exc}")
    last = {}
    rows = 0
    for r in data.get("rounds") or []:
        if r.get("lane") != LANE or not r.get("admitted"):
            continue
        rn = r.get("round")
        if not isinstance(rn, int) or rn > through:
            continue
        rows += 1
        for axis, verdict in (r.get("verdicts") or {}).items():
            if axis in AXES and verdict in ("improved", "harmed"):
                if axis not in last or rn > last[axis][0]:
                    last[axis] = (rn, verdict)
    return last, rows


def grade(text, manifest, through):
    cells = axes_cells(text)
    last, rows = expectations(manifest, through)
    items, mismatches, errors = [], 0, 0
    for axis in AXES:
        cell, err = cells.get(axis, (None, "missing_row"))
        want = last.get(axis)
        if err:
            errors += 1
            items.append((axis, "-", "-", err))
            continue
        m = ROUND.search(cell)
        if not m:
            mismatches += 1
            items.append((axis, "no_round", f"round_{want[0]}_{want[1]}" if want else "-",
                          "mismatch"))
            continue
        got_n = int(m.group(1))
        tail = cell[m.end():].split(";")[0]
        vm = VERDICT.search(tail)
        got_v = vm.group(1) if vm else "none"
        if want is None:
            errors += 1
            items.append((axis, f"round_{got_n}_{got_v}", "-", "no_manifest_row"))
            continue
        state = "ok" if (got_n == want[0] and got_v == want[1]) else "mismatch"
        if state == "mismatch":
            mismatches += 1
        items.append((axis, f"round_{got_n}_{got_v}", f"round_{want[0]}_{want[1]}", state))
    met = mismatches == 0 and errors == 0
    return {"met": met, "items": items, "mismatches": mismatches, "errors": errors,
            "rows": rows}


def _scorecard(cells):
    head = ("# t\n\n## Axes\n\n| Axis | Score | Evidence pointer | Last change |\n"
            "|---|---|---|---|\n")
    rows = "".join(f"| {a} | 5 | e | {cells[a]} |\n" for a in AXES)
    return head + rows + "\n## Move log\n"


def _manifest(rounds):
    import json
    return json.dumps({"rounds": [
        {"round": rn, "lane": LANE, "admitted": adm, "verdicts": v}
        for rn, adm, v in rounds]})


def selfcheck(scratch):
    good = {a: f"round 78 (improved, score held); round 40 (improved, score held)"
            for a in AXES}
    good["adjacency"] = "round 19 (improved, score held)"
    cases = []
    rounds = [(78, True, {"coverage": "improved", "operability": "improved",
                          "depth": "improved", "freshness": "improved",
                          "calibration": "improved", "adjacency": "unchanged"}),
              (19, True, {"adjacency": "improved"}),
              (90, True, {"depth": "improved"}),          # beyond THROUGH: ignored
              (95, False, {"coverage": "improved"})]      # not admitted: ignored
    cases.append(("conformant_met", good, rounds, True))
    stale = dict(good)
    stale["coverage"] = "round 47 (improved, score held)"
    cases.append(("stale_cell_unmet", stale, rounds, False))
    noverdict = dict(good)
    noverdict["depth"] = "round 78 (score held)"
    cases.append(("verdict_word_missing_unmet", noverdict, rounds, False))
    low = dict(good)
    low["operability"] = "round 40 (improved, score held)"
    cases.append(("subsumed_by_higher_round_unmet", low, rounds, False))
    admitted = dict(good)
    admitted["coverage"] = "round 47 (improved, score held)"
    admitted_rounds = [
        (rn, adm, {a: v for a, v in verdicts.items() if a != "coverage"})
        for rn, adm, verdicts in rounds
    ] + [(60, False, {"coverage": "improved"}),
         (47, True, {"coverage": "improved"})]
    cases.append(("nonadmitted_below_ceiling_ignored_met",
                  admitted, admitted_rounds, True))
    later_verdict = dict(good)
    later_verdict["depth"] = "round 78 (score held); round 40 (improved, score held)"
    cases.append(("verdict_after_clause_boundary_unmet",
                  later_verdict, rounds, False))
    later_round = {a: cell.split(";")[0] for a, cell in good.items()}
    later_round["operability"] = "round 40 (score held); round 78 (improved, score held)"
    cases.append(("later_round_in_cell_ignored_unmet", later_round, rounds, False))
    ok = 0
    for label, cells, rnds, expect in cases:
        d = tempfile.mkdtemp(dir=scratch)
        repo = os.path.join(d, "repo")
        os.makedirs(repo)
        open(os.path.join(repo, "SCORECARD.md"), "w").write(_scorecard(cells))
        open(os.path.join(repo, "MANIFEST.json"), "w").write(_manifest(rnds))
        env = ["-c", "user.name=t", "-c", "user.email=t@t"]
        run(["git"] + env + ["-C", repo, "init", "-q"])
        run(["git"] + env + ["-C", repo, "add", "-A"])
        run(["git"] + env + ["-C", repo, "commit", "-qm", "fixture"])
        rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
        text = read_blob(repo, rev, "SCORECARD.md") or ""
        r = grade(text, os.path.join(repo, "MANIFEST.json"), THROUGH)
        if r["met"] == expect:
            ok += 1
            print(f"PASS {label} met={r['met']}")
        else:
            print(f"FAIL {label} want_met={expect} got={r} ")
    print(f"C2_COUNTER_SELFTEST pass={ok} fail={len(cases)-ok}")
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--manifest")
    ap.add_argument("--through", type=int, default=THROUGH)
    ap.add_argument("--scratch")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = tempfile.gettempdir()
    scratch = tempfile.mkdtemp(prefix="count-c2-r79-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev:
            print("C2_SETUP usage: count-c2.py <rev> | --selftest", file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        if top.returncode == 0:
            a.repo = top.stdout.strip()
        p = run(["git", "-C", a.repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"C2_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        text = read_blob(a.repo, rev, "SCORECARD.md")
        if text is None:
            print("C2_SETUP SCORECARD.md unreadable at rev", file=sys.stderr)
            return 2
        manifest = a.manifest or os.path.join(a.repo, "..", "MANIFEST.json")
        try:
            r = grade(text, manifest, a.through)
        except RuntimeError as exc:
            print(f"C2_SETUP {exc}", file=sys.stderr)
            return 2
        for axis, got, want, state in r["items"]:
            print(f"axis {axis} cell={got} expect={want} state={state}")
        print(f"C2={'met' if r['met'] else 'unmet'} axes={len(AXES)} "
              f"mismatches={r['mismatches']} errors={r['errors']} rows={r['rows']} "
              f"through={a.through} rev={rev[:12]}")
        return 0 if r["met"] else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
