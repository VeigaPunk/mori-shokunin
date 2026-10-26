#!/usr/bin/env python3
"""Round 50 C1 counter (calibration) — the lane's self-assessment against the fleet record and the instruments.

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, (a) SCORECARD.md's `## Axes` table has exactly one row for each of the six axes, and
  for each axis the Last change cell's first `round N` equals N*, the highest mori lane round <= 49
  that the fleet MANIFEST.json (at the pinned fleet revision) records with verdict `admitted` and
  that axis graded `improved` or `harmed`; the text from that `round N` to the next `;` names N*'s
  verdict word; and the Evidence cell names `corpus/lessons/round-N*-verifier-spotcheck.md` when that
  file exists at R, else `MANIFEST.json`. (b) SHONEN.md keeps at least 4 checklist boxes and at least
  2 tally pins; every tally pin is a backticked `python3 <repo-relative path> --selftest` span directly
  followed by `(N/M)` or by `-> `PREFIX pass=N fail=K``; run at R (git archive of R, TMPDIR in the
  scratch dir) the command's last `PREFIX pass=P fail=F` line gives N=P and M=P+F (or the same
  prefix, pass and fail for the token form); no other tally token stands anywhere else in SHONEN.md;
  and `.ufo/waves/round-50/evidence/selftests/<stem>.txt` at R holds the observed `PREFIX pass=P
  fail=F` line. Met iff mismatches=0 and errors=0.

Usage: count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] [--scratch DIR] [--timeout S]
       count-c1.py --selftest
Output: one `item ...` line per item, then
  `C1=met|unmet items=N axes=A pins=P boxes=B mismatches=M errors=E hidden=H manifest=<sha12> rev=R`
  (+ ` failed=<reasons>` when unmet). Exit 0 met, 1 unmet, 2 setup error.
Read-only on the lane and the fleet repo: `git show`, `git cat-file`, `git archive` only; the archive is
extracted under --scratch (default $TMPDIR/count-c1-r50-<pid>) and removed on exit.
Limits (named before data): the Score column is not checked (MANIFEST holds verdicts, not scores);
a pin split across lines or written outside backticks in another file is not enumerated (the hidden
scan covers SHONEN.md only); a matching tally proves the instrument prints it today, not that its arms
are good.
"""
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

AXES = ["coverage", "operability", "depth", "freshness", "calibration", "adjacency"]
THROUGH = 49
LANE = "mori"
FLEET_REV = "e014499613f63f8a467821219b0296121119ca53"
MIN_BOXES = 4
MIN_PINS = 2
RECEIPT_DIR = ".ufo/waves/round-50/evidence/selftests/"
TOOL_TIMEOUT = 900
TALLY = re.compile(r"\b([A-Z][A-Z0-9_]*SELFTEST) pass=(\d+) fail=(\d+)\b")
PIN = re.compile(
    r"`([^`\n]*--selftest[^`\n]*)`"
    r"(?:\s*\((\d+)/(\d+)\)|\s*(?:→|->)\s*`([A-Z][A-Z0-9_]*SELFTEST) pass=(\d+) fail=(\d+)`)")
HIDDEN = re.compile(r"\(\s*\d+\s*/\s*\d+\s*\)|\bpass=\d+|SELFTEST")
BOX = re.compile(r"^\s*[-*] \[[ ~xX]\]")


def split_cells(line):
    s = line.strip()
    parts = re.split(r"(?<!\\)\|", s)
    parts = parts[1:-1] if s.endswith("|") else parts[1:]
    return [p.strip() for p in parts]


def manifest_targets(manifest_text, through=THROUGH, lane=LANE):
    data = json.loads(manifest_text)
    rounds = data["rounds"] if isinstance(data, dict) else data
    best = {}
    for r in rounds:
        if not isinstance(r, dict) or r.get("lane") != lane or r.get("verdict") != "admitted":
            continue
        n = r.get("lane_round", r.get("round"))
        v = r.get("verdicts") or {}
        if not isinstance(n, int) or n > through or not isinstance(v, dict):
            continue
        for ax in AXES:
            if v.get(ax) in ("improved", "harmed") and n >= best.get(ax, (-1, ""))[0]:
                best[ax] = (n, v[ax])
    return best


def axes_table(scorecard):
    lines = scorecard.split("\n")
    rows, fence, start = [], False, None
    for i, l in enumerate(lines):
        if l.lstrip()[:3] in ("```", "~~~"):
            fence = not fence
            continue
        if not fence and re.match(r"^## Axes\s*$", l):
            start = i
            break
    if start is None:
        return None
    header = None
    for l in lines[start + 1:]:
        if l.startswith("#"):
            break
        if not re.match(r"^ {0,3}\|", l):
            if header is not None and rows:
                break
            continue
        cells = split_cells(l)
        if header is None:
            if [c.lower() for c in cells] == ["axis", "score", "evidence pointer", "last change"]:
                header = cells
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows if header is not None else None


def check_axes(scorecard, targets, exists):
    items = []
    rows = axes_table(scorecard) if scorecard is not None else None
    for ax in AXES:
        want = targets.get(ax)
        if want is None:
            items.append(("axis", ax, "-", "manifest_has_no_target", "error"))
            continue
        n, verdict = want
        if rows is None:
            items.append(("axis", ax, "round %d %s" % (n, verdict), "no_axes_table", "mismatch"))
            continue
        mine = [r for r in rows if r and r[0].strip("* ").lower() == ax]
        if len(mine) != 1:
            items.append(("axis", ax, "round %d %s" % (n, verdict), "rows=%d" % len(mine), "mismatch"))
            continue
        r = mine[0]
        if len(r) != 4:
            items.append(("axis", ax, "round %d %s" % (n, verdict), "cells=%d" % len(r), "mismatch"))
            continue
        evidence, last = r[2], r[3]
        m = re.search(r"\bround[ -]?(\d+)\b", last, re.I)
        got_n = int(m.group(1)) if m else None
        seg = last[m.start():].split(";")[0] if m else ""
        spot = "corpus/lessons/round-%d-verifier-spotcheck.md" % n
        need = spot if exists(spot) else "MANIFEST.json"
        problems = []
        if got_n != n:
            problems.append("round=%s" % got_n)
        if verdict not in seg.lower():
            problems.append("verdict_word_missing")
        if need not in evidence:
            problems.append("evidence_missing:%s" % need)
        items.append(("axis", ax, "round %d %s" % (n, verdict),
                      ",".join(problems) if problems else "ok", "mismatch" if problems else "ok"))
    return items, (len(rows) if rows is not None else 0)


def parse_shonen(text):
    pins, hidden, boxes = [], 0, 0
    for line in text.split("\n"):
        if BOX.match(line):
            boxes += 1
        rest = line
        for m in PIN.finditer(line):
            pins.append(m.groups())
        rest = PIN.sub(" ", line)
        hidden += len(HIDDEN.findall(rest))
    return pins, hidden, boxes


def bound_path(cmd):
    try:
        argv = shlex.split(cmd)
    except ValueError:
        return None
    if len(argv) != 3 or argv[0] != "python3" or argv[2] != "--selftest":
        return None
    p = argv[1]
    if p.startswith("/") or ".." in p.split("/") or not p.endswith(".py"):
        return None
    return p


def check_pins(text, exists, read, run):
    items = []
    pins, hidden, boxes = parse_shonen(text) if text is not None else ([], 0, 0)
    for cmd, n, m, prefix, p_pass, p_fail in pins:
        path = bound_path(cmd)
        want = ("(%s/%s)" % (n, m)) if n is not None else ("%s pass=%s fail=%s" % (prefix, p_pass, p_fail))
        if path is None or not exists(path):
            items.append(("pin", cmd, want, "unbound", "mismatch"))
            continue
        obs = run(path)
        if obs is None:
            items.append(("pin", cmd, want, "no_tally_or_timeout", "error"))
            continue
        o_prefix, o_pass, o_fail = obs
        got = "%s pass=%d fail=%d" % (o_prefix, o_pass, o_fail)
        if n is not None:
            ok = int(n) == o_pass and int(m) == o_pass + o_fail
        else:
            ok = prefix == o_prefix and int(p_pass) == o_pass and int(p_fail) == o_fail
        stem = os.path.basename(path)[:-3]
        receipt = read(RECEIPT_DIR + stem + ".txt")
        has_receipt = receipt is not None and got in [l.strip() for l in receipt.split("\n")]
        state = "ok"
        detail = got
        if not ok:
            state = "mismatch"
        elif not has_receipt:
            state = "mismatch"
            detail = got + " receipt_missing"
        items.append(("pin", cmd, want, detail, state))
    return items, len(pins), hidden, boxes


def evaluate(read, exists, run, manifest_text, rev, manifest_tag="-"):
    failed = []
    targets = manifest_targets(manifest_text)
    axis_items, _ = check_axes(read("SCORECARD.md"), targets, exists)
    shonen = read("SHONEN.md")
    if shonen is None:
        failed.append("shonen_absent")
    pin_items, npins, hidden, boxes = check_pins(shonen, exists, read, run)
    items = axis_items + pin_items
    mism = sum(1 for i in items if i[4] == "mismatch")
    errs = sum(1 for i in items if i[4] == "error")
    if mism:
        failed.append("mismatch")
    if errs:
        failed.append("errors")
    if hidden:
        failed.append("hidden")
    if npins < MIN_PINS:
        failed.append("pins_floor")
    if boxes < MIN_BOXES:
        failed.append("boxes_floor")
    if sum(1 for i in axis_items) != len(AXES):
        failed.append("axes")
    met = not failed
    out = ["item %s %s expect=%s got=%s state=%s" % (k, re.sub(r"\s+", "_", name), re.sub(r"\s+", "_", want),
                                                     re.sub(r"\s+", "_", got), st)
           for k, name, want, got, st in items]
    line = ("C1=%s items=%d axes=%d pins=%d boxes=%d mismatches=%d errors=%d hidden=%d manifest=%s rev=%s"
            % ("met" if met else "unmet", len(items), len(axis_items), npins, boxes, mism, errs, hidden,
               manifest_tag, rev))
    if failed:
        line += " failed=" + ",".join(sorted(set(failed)))
    return met, out, line


def git(repo, *args, timeout=120):
    return subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, timeout=timeout)


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    args = list(argv)
    opts = {"--repo": None, "--fleet-repo": None, "--fleet-rev": FLEET_REV, "--scratch": None,
            "--timeout": str(TOOL_TIMEOUT)}
    for k in list(opts):
        while k in args:
            i = args.index(k)
            if i + 1 >= len(args):
                print("C1_SETUP missing value for %s" % k, file=sys.stderr)
                return 2
            opts[k] = args[i + 1]
            del args[i:i + 2]
    if len(args) != 1 or args[0].startswith("-"):
        print("C1_SETUP usage: count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] "
              "[--scratch DIR] [--timeout S] | --selftest", file=sys.stderr)
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    repo = opts["--repo"] or os.path.dirname(os.path.dirname(os.path.dirname(here)))
    fleet = opts["--fleet-repo"] or os.path.dirname(os.path.abspath(repo))
    try:
        timeout = int(opts["--timeout"])
        p = git(repo, "rev-parse", "--verify", args[0] + "^{commit}")
        if p.returncode != 0:
            raise ValueError("rev")
        rev = p.stdout.decode().strip()
        mp = git(fleet, "show", "%s:MANIFEST.json" % opts["--fleet-rev"])
        if mp.returncode != 0:
            raise ValueError("manifest")
        manifest = mp.stdout.decode("utf-8")
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        print("C1_SETUP cannot resolve %s" % e, file=sys.stderr)
        return 2
    tag = hashlib.sha256(mp.stdout).hexdigest()[:12]

    def read(path):
        q = git(repo, "show", "%s:%s" % (rev, path))
        return q.stdout.decode("utf-8", "surrogateescape") if q.returncode == 0 else None

    def exists(path):
        return git(repo, "cat-file", "-e", "%s:%s" % (rev, path)).returncode == 0

    base = opts["--scratch"] or os.path.join(tempfile.gettempdir(), "count-c1-r50-%d" % os.getpid())
    state = {"tree": None}

    def run(path):
        if state["tree"] is None:
            tree = os.path.join(base, "tree")
            os.makedirs(tree, exist_ok=True)
            os.makedirs(os.path.join(base, "tmp"), exist_ok=True)
            a = subprocess.Popen(["git", "-C", repo, "archive", rev], stdout=subprocess.PIPE)
            t = subprocess.run(["tar", "-x", "-C", tree], stdin=a.stdout)
            a.stdout.close()
            if a.wait() != 0 or t.returncode != 0:
                return None
            state["tree"] = tree
        env = dict(os.environ, TMPDIR=os.path.join(base, "tmp"), PYTHONDONTWRITEBYTECODE="1")
        try:
            q = subprocess.run([sys.executable, path, "--selftest"], cwd=state["tree"], env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None
        found = TALLY.findall(q.stdout.decode("utf-8", "replace"))
        if not found:
            return None
        pre, a_, f_ = found[-1]
        return pre, int(a_), int(f_)

    try:
        met, out, line = evaluate(read, exists, run, manifest, rev, tag)
    finally:
        if opts["--scratch"] is None:
            shutil.rmtree(base, ignore_errors=True)
        elif state["tree"]:
            shutil.rmtree(state["tree"], ignore_errors=True)
    for l in out:
        print(l)
    print(line)
    return 0 if met else 1


def selftest():
    manifest = json.dumps({"rounds": [
        {"lane": "mori", "lane_round": 40, "verdict": "admitted",
         "verdicts": {a: "improved" for a in AXES}},
        {"lane": "mori", "lane_round": 45, "verdict": "rejected-harmed",
         "verdicts": {"calibration": "harmed", "depth": "improved"}},
        {"lane": "mori", "lane_round": 47, "verdict": "admitted",
         "verdicts": {"coverage": "improved", "operability": "harmed", "depth": "unchanged"}},
        {"lane": "mori", "lane_round": 49, "verdict": "admitted",
         "verdicts": {"calibration": "improved", "depth": "improved"}},
        {"lane": "mori", "lane_round": 50, "verdict": "admitted",
         "verdicts": {a: "improved" for a in AXES}},
        {"lane": "kama", "lane_round": 48, "verdict": "admitted",
         "verdicts": {a: "improved" for a in AXES}},
    ]})
    want = {"coverage": (47, "improved"), "operability": (47, "harmed"), "depth": (49, "improved"),
            "freshness": (40, "improved"), "calibration": (49, "improved"), "adjacency": (40, "improved")}
    spot_exists = {47, 49}

    def row(ax, n=None, v=None, ev=None):
        n, v = (n, v) if n is not None else want[ax]
        ev = ev if ev is not None else (
            "closure `corpus/lessons/round-%d-verifier-spotcheck.md:9`" % n if n in spot_exists
            else "MANIFEST.json@abc mori round %d" % n)
        return "| %s | 6 | %s | round %d (%s, score held); older note round 3 |" % (ax, ev, n, v)

    def scorecard(rows=None, extra=""):
        rows = rows if rows is not None else [row(a) for a in AXES]
        return "\n".join(["# Scorecard", "", "## Axes", "",
                          "| Axis | Score | Evidence pointer | Last change |", "|---|---|---|---|"]
                         + rows + ["", extra, "## Move log", "| Round | Axis |", "|---|---|", "| 1 | x |"])

    obs = {"tools/a.py": ("A_SELFTEST", 114, 0), "tools/b.py": ("B_SELFTEST", 17, 0)}

    def shonen(pin_a="`python3 tools/a.py --selftest` (114/114)",
               pin_b="`python3 tools/b.py --selftest` → `B_SELFTEST pass=17 fail=0`", extra="", boxes=4):
        lines = ["# SHONEN", ""]
        lines.append("- [~] box one — `SKILL.md:1`")
        lines.append("- [~] box two — %s; %s" % (pin_a, pin_b))
        for i in range(boxes - 2):
            lines.append("- [~] box %d — pointer" % (i + 3))
        return "\n".join(lines + [extra, ""])

    receipts = {RECEIPT_DIR + "a.txt": "$ python3 tools/a.py --selftest\nA_SELFTEST pass=114 fail=0\nrc=0\n",
                RECEIPT_DIR + "b.txt": "B_SELFTEST pass=17 fail=0\n"}

    def files(sc=None, sh=None, rc=None, drop=()):
        f = {"SCORECARD.md": sc if sc is not None else scorecard(),
             "SHONEN.md": sh if sh is not None else shonen(),
             "tools/a.py": "x", "tools/b.py": "x"}
        for n in spot_exists:
            f["corpus/lessons/round-%d-verifier-spotcheck.md" % n] = "x"
        f.update(rc if rc is not None else receipts)
        for d in drop:
            f.pop(d, None)
        return f

    def run_eval(f, runner=None):
        runner = runner or (lambda p: obs.get(p))
        return evaluate(lambda p: f.get(p), lambda p: p in f, runner, manifest, "R")

    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    check("targets_from_manifest", manifest_targets(manifest) == want)
    met, out, line = run_eval(files())
    check("honest_met", met and "mismatches=0 errors=0 hidden=0" in line and "axes=6 pins=2 boxes=4" in line)
    check("rejected_round_ignored", manifest_targets(manifest)["calibration"] == (49, "improved"))
    check("through_round_cutoff", all(v[0] <= THROUGH for v in manifest_targets(manifest).values()))
    check("other_lane_ignored", manifest_targets(manifest)["freshness"] == (40, "improved"))
    check("harmed_counts", manifest_targets(manifest)["operability"] == (47, "harmed"))
    rows = [row(a) for a in AXES]
    rows[2] = row("depth", 47, "improved")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("stale_round_unmet", (not met) and "mismatches=1" in line and any("round=47" in o for o in out))
    rows = [row(a) for a in AXES]
    rows[1] = row("operability", 47, "improved")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("verdict_word_wrong_unmet", (not met) and any("verdict_word_missing" in o for o in out))
    rows = [row(a) for a in AXES]
    rows[0] = row("coverage", ev="no pointer here")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("evidence_pointer_missing_unmet", (not met) and any("evidence_missing" in o for o in out))
    rows = [row(a) for a in AXES]
    rows[3] = row("freshness", ev="`corpus/lessons/round-40-verifier-spotcheck.md`")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("absent_spotcheck_needs_manifest", (not met) and any("evidence_missing:MANIFEST.json" in o for o in out))
    rows = [row(a) for a in AXES] + [row("depth")]
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("duplicate_axis_row_unmet", (not met) and any("rows=2" in o for o in out))
    rows = [row(a) for a in AXES if a != "adjacency"]
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("missing_axis_row_unmet", (not met) and any("rows=0" in o for o in out))
    met, out, line = run_eval(files(sc="```\n" + scorecard() + "\n```\n"))
    check("table_in_fence_unseen", not met)
    allr = [row(a, 49, "improved", "`corpus/lessons/round-49-verifier-spotcheck.md`") for a in AXES]
    met, out, line = run_eval(files(sc=scorecard(allr)))
    check("all_latest_junk_unmet", (not met) and "mismatches=4" in line)
    rows = [row(a) for a in AXES]
    rows[4] = "| calibration | 5 | `corpus/lessons/round-49-verifier-spotcheck.md` | round 25 (improved); round 49 improved |"
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("first_round_token_decides", (not met) and any("round=25" in o for o in out))
    met, out, line = run_eval(files(sh=shonen(pin_a="`python3 tools/a.py --selftest` (60/60)")))
    check("stale_fraction_pin_unmet", (not met) and "mismatches=1" in line)
    met, out, line = run_eval(files(sh=shonen(pin_b="`python3 tools/b.py --selftest` → `B_SELFTEST pass=13 fail=0`")))
    check("stale_token_pin_unmet", (not met) and "mismatches=1" in line)
    met, out, line = run_eval(files(sh=shonen(pin_b="`python3 tools/b.py --selftest` → `X_SELFTEST pass=17 fail=0`")))
    check("prefix_mismatch_unmet", not met)
    met, out, line = run_eval(files(sh=shonen(pin_a="`python3 tools/a.py --selftest`", pin_b="b")))
    check("pins_deleted_unmet", (not met) and "pins_floor" in line)
    met, out, line = run_eval(files(sh=shonen(boxes=3)))
    check("box_deleted_unmet", (not met) and "boxes_floor" in line)
    met, out, line = run_eval(files(sh=shonen(extra="note: the tool printed (60/60) once")))
    check("hidden_fraction_unmet", (not met) and "hidden=1" in line)
    met, out, line = run_eval(files(sh=shonen(extra="see A_SELFTEST in the log")))
    check("hidden_token_unmet", (not met) and "hidden" in line)
    met, out, line = run_eval(files(sh=shonen(pin_a="`python3 /abs/tools/a.py --selftest` (114/114)")))
    check("absolute_path_unbound", (not met) and any("unbound" in o for o in out))
    met, out, line = run_eval(files(sh=shonen(pin_a="`python3 tools/a.py --selftest --fast` (114/114)")))
    check("extra_args_unbound", (not met) and any("unbound" in o for o in out))
    met, out, line = run_eval(files(sh=shonen(pin_a="`bash tools/a.py --selftest` (114/114)")))
    check("other_interpreter_unbound", (not met) and any("unbound" in o for o in out))
    met, out, line = run_eval(files(drop=("tools/a.py",)))
    check("missing_tool_unbound", (not met) and any("unbound" in o for o in out))
    met, out, line = run_eval(files(rc={RECEIPT_DIR + "b.txt": receipts[RECEIPT_DIR + "b.txt"]}))
    check("receipt_missing_unmet", (not met) and any("receipt_missing" in o for o in out))
    met, out, line = run_eval(files(rc={RECEIPT_DIR + "a.txt": "A_SELFTEST pass=60 fail=0\n",
                                        RECEIPT_DIR + "b.txt": receipts[RECEIPT_DIR + "b.txt"]}))
    check("receipt_other_tally_unmet", (not met) and any("receipt_missing" in o for o in out))
    met, out, line = run_eval(files(), runner=lambda p: None)
    check("runner_error_counts", (not met) and "errors=2" in line)
    met, out, line = run_eval(files(), runner=lambda p: ("A_SELFTEST", 113, 1) if p == "tools/a.py" else obs[p])
    check("failing_arm_mismatch", (not met) and "mismatches=1" in line)
    met, out, line = run_eval(files(sh=shonen(pin_a="`python3 tools/a.py --selftest` (113/114)")),
                              runner=lambda p: ("A_SELFTEST", 113, 1) if p == "tools/a.py" else obs[p])
    check("honest_failing_pin_needs_receipt", (not met) and any("receipt_missing" in o for o in out))
    check("bound_path_ok", bound_path("python3 tools/x.py --selftest") == "tools/x.py")
    check("bound_path_dotdot", bound_path("python3 ../x.py --selftest") is None)
    sc = scorecard().replace("## Axes", "## Axes (old)")
    met, out, line = run_eval(files(sc=sc))
    check("heading_renamed_unmet", (not met) and any("no_axes_table" in o for o in out))
    for name, cond in checks:
        print("%s %s" % ("PASS" if cond else "FAIL", name))
    failn = sum(1 for _, c in checks if not c)
    print("C1_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
