#!/usr/bin/env python3
"""mori round-82 C2 counter (freshness): retire the red round-10 drift pin with a derived
classification of every token the live drift still reports.

Frozen predicate P-C2 (`.ufo/waves/round-82/contract.md` — this counter, the contract and the
receipt label are the same sentence):

  At revision R `python3 -I .ufo/waves/round-82/count-c2.py R` prints
  `C2=met tokens=N classified=N agreed=N residual=0 retired=1 cell=1` and exits 0, where the
  census script at R run against the baseline at R exits 1 (the pin stays red), its `MORI_DRIFT:`
  token list is non-empty, `corpus/evidence/drift-classification-r82.txt` at R carries one
  `DRIFT_CLASS <token> <class>` line per live token, every stated class equals the class derived
  from the baseline bytes at R, no classification names a token absent from the live run, and
  `SCORECARD.md` at R has a `## Retired` row `drift-pin-r10` naming both paths while the
  `freshness` Axes row carries the literal `r10 pin retired` and the classification path and no
  longer carries `round-10 drift pin still red`.

Derivation table (frozen): a `SURFACE:<name>`/`FINDING:<NAME>` token is `value-changed` when that
id exists in the baseline's canonical block, else `added-since-r10`; `VERDICT`/`HEADER`/`BLANK`
are `value-changed`; a bare/`+`/`-` prefixed key is `value-changed` when `<key>=` occurs in the
baseline bytes, else `added-since-r10`; anything else is `value-changed`. A token labelled
`unexplainable` counts as `residual` and keeps the claim unmet.

Vacuity guard: the census run is the same command in both states and must stay red (exit 1). A
green pin is `unmet` — there would be nothing to classify.

Usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] [--tree DIR] [--fleet-root DIR]
       count-c2.py --selftest
Exit 0 met, 1 unmet, 2 setup. Read-only: `git show`; files only under --scratch/--tree.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASELINE = "corpus/evidence/baseline-r10-20261015T2231Z.json"
CLASSES = "corpus/evidence/drift-classification-r82.txt"
CENSUS = "tools/mori-census.sh"
CARDS = "SCORECARD.md"
CLASS_WORDS = ("added-since-r10", "value-changed", "unexplainable")
CLASS_LINE = re.compile(r"^DRIFT_CLASS\s+(\S+)\s+(\S+)\s*$")
DRIFT = re.compile(r"^MORI_DRIFT:\s*(.*)$")
KEY = re.compile(r"(?:^|\s)([A-Za-z0-9_]+)=")
KEYSHAPE = re.compile(r"^[A-Za-z0-9_]+$")


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
    surfaces, findings, keys = names
    body = token.lstrip("+-")
    if body.startswith("SURFACE:"):
        return "value-changed" if body[len("SURFACE:"):] in surfaces else "added-since-r10"
    if body.startswith("FINDING:"):
        return "value-changed" if body[len("FINDING:"):] in findings else "added-since-r10"
    if body in ("VERDICT", "HEADER", "BLANK"):
        return "value-changed"
    if not KEYSHAPE.match(body):
        return "value-changed"          # frozen table: "anything else" is value-changed
    return "value-changed" if body in keys else "added-since-r10"


def classifications(text):
    stated, malformed, duplicates = {}, 0, 0
    for line in text.splitlines():
        if not line.startswith("DRIFT_CLASS"):
            continue
        m = CLASS_LINE.match(line)
        if not m or m.group(2) not in CLASS_WORDS:
            malformed += 1
            continue
        if m.group(1) in stated:
            duplicates += 1
        stated[m.group(1)] = m.group(2)
    return stated, malformed, duplicates


def section_rows(text, heading):
    inside, rows = False, []
    for line in text.splitlines():
        if re.match(r"^##\s", line):
            inside = line.strip() == heading
            continue
        if inside and line.lstrip().startswith("|"):
            cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
            if cells:
                rows.append((cells, line))
    return rows


def retired_ok(text):
    for cells, line in section_rows(text, "## Retired"):
        if cells and cells[0] == "drift-pin-r10":
            return (BASELINE in line and CLASSES in line)
    return False


def cell_state(text):
    for cells, line in section_rows(text, "## Axes"):
        if cells and cells[0].strip("` ") == "freshness":
            return ("r10 pin retired" in line and CLASSES in line
                    and "round-10 drift pin still red" not in line)
    return False


def drift_tokens(text):
    tokens = []
    for line in text.splitlines():
        m = DRIFT.match(line)
        if m:
            tokens = [token for token in m.group(1).split() if token != "none"]
    return tokens


def grade(loader, scratch, fleet_root):
    census = loader(CENSUS)
    baseline = loader(BASELINE)
    cards = loader(CARDS)
    if census is None or baseline is None or cards is None:
        return False, "setup=census/baseline/SCORECARD absent", []
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
        return False, "setup=census timeout", []
    output = (p.stdout or "") + (p.stderr or "")
    tokens = drift_tokens(output)
    classes = loader(CLASSES)
    stated, malformed, duplicates = classifications(classes or "")
    names = baseline_names(baseline)
    agreed = 0
    residual = 0
    unclassified = [token for token in tokens if token not in stated]
    for token in tokens:
        if token not in stated:
            continue
        if stated[token] == "unexplainable":
            residual += 1
        elif stated[token] == derive(token, names):
            agreed += 1
    stale = [token for token in stated if token not in tokens]
    residual += duplicates
    met = (p.returncode == 1 and bool(tokens) and not unclassified and residual == 0
           and malformed == 0 and duplicates == 0 and not stale and agreed == len(tokens)
           and retired_ok(cards) and cell_state(cards))
    tail = (f"tokens={len(tokens)} classified={len(tokens) - len(unclassified)} "
            f"agreed={agreed} residual={residual + malformed} stale={len(stale)} "
            f"retired={1 if retired_ok(cards) else 0} cell={1 if cell_state(cards) else 0}")
    notes = []
    if p.returncode != 1:
        notes.append(f"metric=census-rc:{p.returncode}")
    for token in unclassified[:6]:
        notes.append(f"unclassified {token}")
    for token in tokens:
        if token in stated and stated[token] not in ("unexplainable",):
            if stated[token] != derive(token, names):
                notes.append(f"class-disagrees {token} stated={stated[token]} "
                             f"derived={derive(token, names)}")
    for token in stale[:6]:
        notes.append(f"stale-classification {token}")
    if malformed:
        notes.append(f"malformed-classification-lines={malformed}")
    if duplicates:
        notes.append(f"duplicate-classification-lines={duplicates}")
    return met, tail, notes


def selfcheck(scratch):
    cases = []
    base = ("# mori-drift-baseline v1\n# volatile_fields=x\n"
            "# --- canonical output follows ---\n"
            "SURFACE watchdog: pid=1 state=ok\n"
            "FINDING OOM_KILL_JOURNAL severity=crit paths=a\n"
            "lane.mori fields=1\nMORI_CENSUS: DRIFT (findings=0 drift=0)\n")
    stub_body = ("#!/bin/sh\necho 'MORI_DRIFT: +SURFACE:lane.new +audit fields +VERDICT'\n"
                 "exit 1\n")
    good = {
        "+SURFACE:lane.new": "added-since-r10",
        "+audit": "added-since-r10",
        "fields": "value-changed",
        "+VERDICT": "value-changed",
    }
    cards_clean = (
        "# t\n\n## Axes\n\n| Axis | Score | Evidence | Last change |\n|---|---|---|---|\n"
        "| freshness | 5 | r10 pin retired at corpus/evidence/drift-classification-r82.txt "
        "| round 82 |\n\n## Retired\n\n| Axis | Reason | Round |\n|---|---|---|\n"
        "| drift-pin-r10 | retired: baseline corpus/evidence/"
        "baseline-r10-20261015T2231Z.json fully classified at "
        "corpus/evidence/drift-classification-r82.txt | 82 |\n")

    def build(label, classes, cards=cards_clean, rc=1, stub=None):
        d = tempfile.mkdtemp(dir=scratch, prefix="c2-" + label + "-")
        census_body = stub if stub is not None else (
            stub_body if rc == 1 else "#!/bin/sh\necho 'MORI_DRIFT: none'\nexit 0\n")
        for name, body in ((CENSUS, census_body), (BASELINE, base), (CARDS, cards)):
            target = os.path.join(d, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(body)
        if classes is not None:
            target = os.path.join(d, CLASSES)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            open(target, "w", encoding="utf-8").write(classes)
        if rc != 1 and stub is None:
            open(os.path.join(d, CENSUS), "w", encoding="utf-8").write(
                "#!/bin/sh\nprintf 'MORI_DRIFT: none\\n'\nexit 0\n")
        loader = lambda path: (open(os.path.join(d, path), encoding="utf-8").read()
                               if os.path.exists(os.path.join(d, path)) else None)  # noqa: E731
        return grade(loader, scratch, d)

    def text(rows):
        return "".join(f"DRIFT_CLASS {token} {cls}\n" for token, cls in rows.items())

    met, tail, _ = build("clean", text(good))
    cases.append(("conformant", met and "tokens=4" in tail and "retired=1" in tail, tail))
    partial = {"+SURFACE:lane.new": "added-since-r10", "+audit": "added-since-r10",
               "fields": "value-changed"}
    met, tail, _ = build("partial", text(partial))
    cases.append(("unclassified_token", (not met) and "classified=3" in tail, tail))
    wrong = dict(good, fields="added-since-r10")
    met, tail, _ = build("wrong", text(wrong))
    cases.append(("class_disagrees", (not met) and "agreed=3" in tail, tail))
    unexpl = dict(good, **{"+audit": "unexplainable"})
    met, tail, _ = build("unexpl", text(unexpl))
    cases.append(("residual_keeps_unmet", (not met) and "residual=1" in tail, tail))
    stale = dict(good, **{"-gone": "value-changed"})
    met, tail, _ = build("stale", text(stale))
    cases.append(("stale_classification", (not met) and "stale=1" in tail, tail))
    red_cards = cards_clean.replace("r10 pin retired", "round-10 drift pin still red")
    met, tail, _ = build("redcell", text(good), cards=red_cards)
    cases.append(("red_cell_keeps_unmet", (not met) and "cell=0" in tail, tail))
    no_row = cards_clean.replace("| drift-pin-r10 | retired: baseline corpus/evidence/"
                                 "baseline-r10-20261015T2231Z.json fully classified at "
                                 "corpus/evidence/drift-classification-r82.txt | 82 |\n", "")
    met, tail, _ = build("norow", text(good), cards=no_row)
    cases.append(("retired_row_required", (not met) and "retired=0" in tail, tail))
    met, tail, notes = build("green", text(good), rc=0)
    cases.append(("green_pin_is_unmet",
                  (not met) and "tokens=0" in tail and any("census-rc:0" in n for n in notes),
                  tail))
    met, tail, _ = build("noclass", None)
    cases.append(("classification_file_absent", not met, tail))
    # r83 arms
    dup2 = text(good) + "DRIFT_CLASS +audit added-since-r10\n"
    met, tail, _ = build("dupline", dup2)
    cases.append(("duplicate_line_residual", (not met) and "residual=1" in tail, tail))
    no_path = cards_clean.replace("drift-classification-r82.txt | 82 |",
                                  "other-evidence.txt | 82 |")
    met, tail, _ = build("nopath", text(good), cards=no_path)
    cases.append(("retired_row_missing_path", (not met) and "retired=0" in tail, tail))
    both = cards_clean.replace("r10 pin retired at",
                               "r10 pin retired; round-10 drift pin still red; at")
    met, tail, _ = build("bothlit", text(good), cards=both)
    cases.append(("red_literal_under_retired", (not met) and "cell=0" in tail, tail))
    gstub = ("#!/bin/sh\necho 'MORI_DRIFT: +SURFACE:lane.new +audit fields"
             " +VERDICT'\nexit 0\n")
    met, tail, notes = build("greenrc", text(good), rc=0, stub=gstub)
    cases.append(("green_rc_with_tokens",
                  (not met) and any("census-rc:0" in n for n in notes) and "tokens=4" in tail,
                  tail))
    fbase = base + "FINDING OOM_KILL_JOURNAL severity=crit paths=a\n"
    fstub = ("#!/bin/sh\necho 'MORI_DRIFT: +FINDING:OOM_KILL_JOURNAL"
             " +FINDING:NOT_IN_BASELINE'\nexit 1\n")
    fgood = {"+FINDING:OOM_KILL_JOURNAL": "value-changed",
             "+FINDING:NOT_IN_BASELINE": "added-since-r10"}
    d = tempfile.mkdtemp(dir=scratch, prefix="c2-find-")
    for name, body in ((CENSUS, fstub), (BASELINE, fbase), (CARDS, cards_clean),
                       (CLASSES, text(fgood))):
        target = os.path.join(d, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)
    loader2 = lambda path: (open(os.path.join(d, path), encoding="utf-8").read()
                            if os.path.exists(os.path.join(d, path)) else None)
    met, tail, _ = grade(loader2, scratch, d)
    cases.append(("finding_branch", met and "agreed=2" in tail, tail))
    mal = text(good) + "DRIFT_CLASS broken line\n"
    met, tail, _ = build("malformed", mal)
    cases.append(("malformed_line_in_residual", (not met) and "residual=1" in tail, tail))
    ks = {"+SURFACE:lane.new": "added-since-r10", "lane.mori": "value-changed",
          "+audit": "added-since-r10", "fields": "value-changed", "+VERDICT": "value-changed"}
    ksstub = ("#!/bin/sh\necho 'MORI_DRIFT: +SURFACE:lane.new lane.mori +audit fields"
              " +VERDICT'\nexit 1\n")
    d2 = tempfile.mkdtemp(dir=scratch, prefix="c2-keyshape-")
    for name, body in ((CENSUS, ksstub), (BASELINE, base), (CARDS, cards_clean),
                       (CLASSES, text(ks))):
        target = os.path.join(d2, name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(body)
    loader3 = lambda path: (open(os.path.join(d2, path), encoding="utf-8").read()
                            if os.path.exists(os.path.join(d2, path)) else None)
    met, tail, _ = grade(loader3, scratch, d2)
    cases.append(("keyshape_anything_else", met and "tokens=5" in tail, tail))
    ok = sum(1 for _, good_case, _ in cases if good_case)
    for label, good_case, line in cases:
        print(f"{'PASS' if good_case else 'FAIL'} {label} {line}")
    print(f"C2_COUNTER_SELFTEST pass={ok} fail={len(cases) - ok}")
    return 0 if ok == len(cases) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
    ap.add_argument("--scratch")
    ap.add_argument("--tree")
    ap.add_argument("--fleet-root")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="count-c2-r82-", dir=base)
    try:
        if a.selftest:
            return selfcheck(scratch)
        if not a.rev or a.tree:
            print("C2_SETUP usage: count-c2.py <rev> [--repo DIR] [--scratch DIR] | --selftest",
                  file=sys.stderr)
            return 2
        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
        repo = top.stdout.strip() if top.returncode == 0 else a.repo
        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
        if p.returncode != 0:
            print(f"C2_SETUP unresolvable revision {a.rev}", file=sys.stderr)
            return 2
        rev = p.stdout.strip()
        fleet = a.fleet_root or (os.path.dirname(repo) if repo.endswith("-shokunin") else repo)

        def loader(path):
            q = run(["git", "-C", repo, "show", f"{rev}:{path}"])
            return q.stdout if q.returncode == 0 else None

        met, tail, notes = grade(loader, scratch, fleet)
        if tail.startswith("setup="):
            print(f"C2_SETUP {tail}", file=sys.stderr)
            return 2
        for note in notes:
            print(note)
        print(f"C2={'met' if met else 'unmet'} {tail} rev={rev[:12]}")
        return 0 if met else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
