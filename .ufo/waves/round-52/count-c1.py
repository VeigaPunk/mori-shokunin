#!/usr/bin/env python3
"""Round 52 C1 counter (calibration) — the lane's self-assessment against the fleet record, its own instruments
and the evidence its pointers name. Successor of `.ufo/waves/round-50/count-c1.py` (round-50 closure routed
defect 3: close the named survivors and take K4 beyond SHONEN.md).

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, mismatches=0 and errors=0 over four arms, with every floor held:
  (A) axes — SCORECARD.md has exactly one `## Axes` heading outside fences; its table has exactly one row for
      each of the six axes and four cells per row; for each axis the Last change cell's first `round N` equals
      N*, the highest mori lane round <= 51 that the fleet MANIFEST.json at the pinned fleet revision records
      with verdict exactly `admitted` and that axis graded `improved` or `harmed`; the text from that `round N`
      to the next `;` carries N*'s verdict as a whole word; the Evidence cell names
      `corpus/lessons/round-N*-verifier-spotcheck.md` when that file exists at R, else `MANIFEST.json`; and the
      Score cell is the integer the newest closure file `corpus/lessons/round-K-verifier-spotcheck.md` at R
      that has a per-axis row for the axis states (its second cell, or M when the row says `Score N → M`).
  (B) shonen — SHONEN.md keeps >= 4 checklist boxes and >= 2 tally pins; every tally pin is a backticked
      `python3 <repo-relative path> --selftest` span followed by `(N/M)` or by -> `PREFIX pass=N fail=K`;
      the path is a regular file at R (git tree mode 100644 or 100755, never a symlink); run at R (git archive
      of R under the scratch dir, TMPDIR in scratch) its last `PREFIX pass=P fail=F` line gives the pinned
      numbers; `.ufo/waves/round-52/evidence/selftests/<stem>.txt` at R holds that observed line; and no other
      tally token stands anywhere else in SHONEN.md.
  (C) living pins (K4 beyond SHONEN.md) — in corpus/QUALITY.md and corpus/README.md, every single-line
      command-tally pin (a backticked span containing `--selftest` followed by `(N/M)` or by -> a backticked
      `[PREFIX ]pass=N fail=K`) is good or superseded. Good: the span parses (shlex) as `python3|bash
      <repo-relative path> ...`, the path is a regular file at R, and the command run at R (archive, TMPDIR in
      scratch) exits 0 and its last tally line gives the pinned numbers (and prefix when pinned). Superseded:
      in QUALITY.md a later numbered criterion says `supersedes N's check` where N is the pin's criterion; in
      either file a later line carries the word `supersedes` and the stale pin's span-and-tally text verbatim
      (that quoted span, on a `supersedes` line and present on an earlier line, is a quotation, not a pin).
      Every pin present at the entering tip E is still present, byte for byte, at R (the record is appended
      to, never rewritten).
  (D) locators — every backticked `path:N[-M]` in the six Axes rows and the SHONEN boxes names a file at R
      with at least M lines; when the text before it (back to the previous locator, `;` or cell start) holds
      a double-quoted string, that string (whitespace collapsed) occurs in lines N..M; when it holds
      `proposed A → B`, `A → B` occurs in lines N..M.

Usage: count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] [--scratch DIR] [--timeout S]
       count-c1.py --selftest
Output: one `item ...` line per item, then
  `C1=met|unmet items=N axes=A pins=P boxes=B living=L superseded=S locators=O mismatches=M errors=E hidden=H
   lane_writes=W manifest=<sha12> rev=R` (+ ` failed=<reasons>` when unmet). Exit 0 met, 1 unmet, 2 setup error.
Read-only on the lane and the fleet repo: `git show`, `git cat-file`, `git ls-tree`, `git archive` only. The
archive is extracted under --scratch (default: a fresh dir under $TMPDIR, which must lie outside the lane) and
removed on exit. lane_writes counts `git status --porcelain --ignored` lines of the lane repo that appear while
the pinned commands run; any nonzero value is an error (a pinned command wrote into the repo it measures).
Limits (named before data): a pin split across lines, or with a placeholder such as `<rev>`, is not enumerated as
a living pin when it spans lines, and is unrunnable (bad) when it is one line; a matching tally proves the
instrument prints it today, not that its arms are good; the locator arm checks quoted text and `proposed A → B`
only, other prose before a locator is checked for range alone; the Score arm trusts the closure's table.
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
THROUGH = 51
LANE = "mori"
FLEET_REV = "f0b61b4ad192bcd95d7a76613a626f71285996ed"
ENTERING = "4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d"
MIN_BOXES = 4
MIN_PINS = 2
RECEIPT_DIR = ".ufo/waves/round-52/evidence/selftests/"
LIVING = ["corpus/QUALITY.md", "corpus/README.md"]
TOOL_TIMEOUT = 900
TALLY = re.compile(r"\b([A-Z][A-Z0-9_]*SELFTEST) pass=(\d+) fail=(\d+)\b")
ANY_TALLY = re.compile(r"(?:\b([A-Z][A-Z0-9_]*SELFTEST) )?\bpass=(\d+) fail=(\d+)\b")
PIN = re.compile(
    r"`([^`\n]*--selftest[^`\n]*)`"
    r"(?:\s*\((\d+)/(\d+)\)|\s*(?:→|->)\s*`([A-Z][A-Z0-9_]*SELFTEST) pass=(\d+) fail=(\d+)`)")
LPIN = re.compile(
    r"`([^`\n]*--selftest[^`\n]*)`"
    r"(?:\s*\((\d+)/(\d+)\)|\s*(?:→|->)\s*`(?:([A-Z][A-Z0-9_]*SELFTEST) )?pass=(\d+) fail=(\d+)`)")
HIDDEN = re.compile(r"\(\s*\d+\s*/\s*\d+\s*\)|\bpass=\d+|SELFTEST")
BOX = re.compile(r"^\s*[-*] \[[ ~xX]\]")
LOC = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*):(\d+)(?:-(\d+))?`")
CRIT = re.compile(r"^(\d+)\. ")


def split_cells(line):
    s = line.strip()
    parts = re.split(r"(?<!\\)\|", s)
    parts = parts[1:-1] if s.endswith("|") else parts[1:]
    return [p.strip() for p in parts]


def ws(s):
    return re.sub(r"\s+", " ", s).strip()


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


def unfenced(text):
    fence = False
    for i, l in enumerate(text.split("\n")):
        if l.lstrip()[:3] in ("```", "~~~"):
            fence = not fence
            continue
        if not fence:
            yield i, l


def axes_table(scorecard):
    heads = [i for i, l in unfenced(scorecard) if re.match(r"^##\s+Axes\s*$", l)]
    lines = scorecard.split("\n")
    if len(heads) != 1:
        return None, len(heads)
    rows, header = [], None
    for l in lines[heads[0] + 1:]:
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
    return (rows if header is not None else None), 1


def closure_scores(read, ls_lessons):
    """axis -> (round K, score) from the newest closure file with a per-axis row for that axis."""
    files = []
    for p in ls_lessons():
        m = re.fullmatch(r"corpus/lessons/round-(\d+)-verifier-spotcheck\.md", p)
        if m:
            files.append((int(m.group(1)), p))
    out = {}
    for k, p in sorted(files, reverse=True):
        text = read(p) or ""
        for _, l in unfenced(text):
            if not re.match(r"^ {0,3}\|", l):
                continue
            c = split_cells(l)
            if len(c) < 3:
                continue
            ax = c[0].strip("*` ").lower()
            if ax in AXES and ax not in out and re.fullmatch(r"\d{1,2}", c[1].strip("* ")):
                score = int(c[1].strip("* "))
                mv = re.search(r"[Ss]core (\d{1,2}) ?→ ?(\d{1,2})", " ".join(c[2:]))
                if mv:
                    score = int(mv.group(2))
                out[ax] = (k, score)
    return out


def check_axes(scorecard, targets, exists, scores):
    items = []
    rows, heads = axes_table(scorecard) if scorecard is not None else (None, 0)
    for ax in AXES:
        want = targets.get(ax)
        if want is None:
            items.append(("axis", ax, "-", "manifest_has_no_target", "error"))
            continue
        n, verdict = want
        tag = "round %d %s" % (n, verdict)
        if rows is None:
            items.append(("axis", ax, tag, "no_axes_table_or_headings=%d" % heads, "mismatch"))
            continue
        mine = [r for r in rows if r and r[0].strip("* ").lower() == ax]
        if len(mine) != 1:
            items.append(("axis", ax, tag, "rows=%d" % len(mine), "mismatch"))
            continue
        r = mine[0]
        if len(r) != 4:
            items.append(("axis", ax, tag, "cells=%d" % len(r), "mismatch"))
            continue
        score, evidence, last = r[1], r[2], r[3]
        m = re.search(r"\bround[ -]?(\d+)\b", last, re.I)
        got_n = int(m.group(1)) if m else None
        seg = last[m.start():].split(";")[0] if m else ""
        spot = "corpus/lessons/round-%d-verifier-spotcheck.md" % n
        need = spot if exists(spot) else "MANIFEST.json"
        problems = []
        if got_n != n:
            problems.append("round=%s" % got_n)
        if not re.search(r"\b%s\b" % re.escape(verdict), seg.lower()):
            problems.append("verdict_word_missing")
        if need not in evidence:
            problems.append("evidence_missing:%s" % need)
        st = scores.get(ax)
        if st is None:
            problems.append("no_closure_score")
        elif score.strip("* ") != str(st[1]):
            problems.append("score=%s_closure_r%d_states=%d" % (score.strip("* "), st[0], st[1]))
        items.append(("axis", ax, tag, ",".join(problems) if problems else "ok",
                      "mismatch" if problems else "ok"))
    return items


def parse_shonen(text):
    pins, hidden, boxes = [], 0, 0
    for line in text.split("\n"):
        if BOX.match(line):
            boxes += 1
        for m in PIN.finditer(line):
            pins.append(m.groups())
        hidden += len(HIDDEN.findall(PIN.sub(" ", line)))
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


def living_argv(cmd):
    try:
        argv = shlex.split(cmd)
    except ValueError:
        return None
    if len(argv) < 2 or argv[0] not in ("python3", "bash"):
        return None
    p = argv[1]
    if p.startswith("/") or ".." in p.split("/") or "<" in cmd or ">" in cmd:
        return None
    return argv


def tally_ok(obs, n, m, prefix, p_pass, p_fail):
    if obs is None:
        return False
    o_prefix, o_pass, o_fail = obs
    if n is not None:
        return int(n) == o_pass and int(m) == o_pass + o_fail
    if prefix and prefix != o_prefix:
        return False
    return int(p_pass) == o_pass and int(p_fail) == o_fail


def check_pins(text, regular, read, run):
    items = []
    pins, hidden, boxes = parse_shonen(text) if text is not None else ([], 0, 0)
    for cmd, n, m, prefix, p_pass, p_fail in pins:
        path = bound_path(cmd)
        want = ("(%s/%s)" % (n, m)) if n is not None else ("%s pass=%s fail=%s" % (prefix, p_pass, p_fail))
        if path is None or not regular(path):
            items.append(("pin", cmd, want, "unbound_or_not_regular", "mismatch"))
            continue
        res = run(["python3", path, "--selftest"])
        obs = res[1] if res else None
        if obs is None:
            items.append(("pin", cmd, want, "no_tally_or_timeout", "error"))
            continue
        got = "%s pass=%d fail=%d" % obs
        receipt = read(RECEIPT_DIR + os.path.basename(path)[:-3] + ".txt")
        has_receipt = receipt is not None and got in [l.strip() for l in receipt.split("\n")]
        if not tally_ok(obs, n, m, prefix, p_pass, p_fail):
            items.append(("pin", cmd, want, got, "mismatch"))
        elif not has_receipt:
            items.append(("pin", cmd, want, got + " receipt_missing", "mismatch"))
        else:
            items.append(("pin", cmd, want, got, "ok"))
    return items, len(pins), hidden, boxes


def living_pins(text):
    """[(line_no, criterion_or_None, span_text, groups)] for every single-line pin."""
    out, crit = [], None
    for i, l in enumerate(text.split("\n"), 1):
        c = CRIT.match(l)
        if c:
            crit = int(c.group(1))
        elif l.startswith("#"):
            crit = None
        for m in LPIN.finditer(l):
            out.append((i, crit, m.group(0), m.groups()))
    return out


def superseded(path, text, line_no, crit, span):
    lines = text.split("\n")
    if path.endswith("QUALITY.md") and crit is not None:
        # a later numbered criterion (not the pin's own) carrying `supersedes N's check`
        cur = None
        for l in lines[line_no:]:
            c = CRIT.match(l)
            if c:
                cur = int(c.group(1))
            if cur is not None and cur != crit and re.search(r"\bsupersedes %d's check\b" % crit, l):
                return True
    for l in lines[line_no:]:
        if "supersedes" in l and span in l:
            return True
    return False


def check_living(read, entering_read, regular, run):
    items = []
    total = sup = 0
    for path in LIVING:
        text = read(path)
        if text is None:
            items.append(("living", path, "-", "file_absent", "mismatch"))
            continue
        old = entering_read(path) or ""
        for _, _, span, _ in living_pins(old):
            if span not in text:
                items.append(("living", path, span, "pin_removed_or_rewritten", "mismatch"))
        tlines = text.split("\n")
        pins_here = living_pins(text)

        def quoted(ln, sp):
            return "supersedes" in tlines[ln - 1] and sp in "\n".join(tlines[:ln - 1])
        for line_no, crit, span, (cmd, n, m, prefix, p_pass, p_fail) in pins_here:
            if quoted(line_no, span) and any(l2 == line_no and not quoted(l2, s2) for l2, _, s2, _ in pins_here):
                continue  # a superseding line quoting the stale pin it replaces, next to its replacement pin
            total += 1
            name = "%s:%d" % (path, line_no)
            if n is not None:
                want = "(%s/%s)" % (n, m)
            else:
                want = ("%s pass=%s fail=%s" % (prefix, p_pass, p_fail)) if prefix else "pass=%s fail=%s" % (
                    p_pass, p_fail)
            if superseded(path, text, line_no, crit, span):
                sup += 1
                items.append(("living", name, want, "superseded", "ok"))
                continue
            argv = living_argv(cmd)
            if argv is None or not regular(argv[1]):
                items.append(("living", name, want, "unrunnable", "mismatch"))
                continue
            res = run(argv)
            if res is None:
                items.append(("living", name, want, "timeout_or_setup", "error"))
                continue
            rc, obs = res
            got = ("%s pass=%d fail=%d rc=%d" % (obs + (rc,))) if obs else "no_tally rc=%d" % rc
            ok = rc == 0 and tally_ok(obs, n, m, prefix, p_pass, p_fail)
            items.append(("living", name, want, got, "ok" if ok else "mismatch"))
    return items, total, sup


def check_locators(scorecard, shonen, read):
    items = []
    texts = []
    if scorecard is not None:
        rows, _ = axes_table(scorecard)
        for r in rows or []:
            if r and r[0].strip("* ").lower() in AXES:
                texts.extend(r[2:])
    if shonen is not None:
        texts.extend(l for l in shonen.split("\n") if BOX.match(l))
    cache = {}
    for t in texts:
        prev = 0
        for m in LOC.finditer(t):
            frag = t[prev:m.start()]
            frag = re.split(r";", frag)[-1]
            prev = m.end()
            path, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            name = "%s:%s" % (path, a if a == b else "%d-%d" % (a, b))
            if path not in cache:
                cache[path] = read(path)
            body = cache[path]
            if body is None:
                items.append(("locator", name, "-", "file_absent", "mismatch"))
                continue
            lines = body.split("\n")
            if body.endswith("\n"):
                lines = lines[:-1]
            if a < 1 or b < a or b > len(lines):
                items.append(("locator", name, "-", "out_of_range_len=%d" % len(lines), "mismatch"))
                continue
            seg = ws(" ".join(lines[a - 1:b]))
            q = re.findall(r"\"([^\"]+)\"", frag)
            pm = re.search(r"proposed (\d+ → \d+)", frag)
            if q:
                need = ws(q[-1])
                ok = need in seg
                items.append(("locator", name, "quote:" + need, "found" if ok else "absent",
                              "ok" if ok else "mismatch"))
            elif pm:
                ok = pm.group(1) in seg
                items.append(("locator", name, "pair:" + pm.group(1), "found" if ok else "absent",
                              "ok" if ok else "mismatch"))
            else:
                items.append(("locator", name, "range", "ok", "ok"))
    return items


def evaluate(read, entering_read, exists, regular, ls_lessons, run, manifest_text, rev, manifest_tag="-",
             lane_writes=lambda: 0):
    failed = []
    targets = manifest_targets(manifest_text)
    scorecard = read("SCORECARD.md")
    shonen = read("SHONEN.md")
    scores = closure_scores(read, ls_lessons)
    axis_items = check_axes(scorecard, targets, exists, scores)
    if shonen is None:
        failed.append("shonen_absent")
    pin_items, npins, hidden, boxes = check_pins(shonen, regular, read, run)
    living_items, nliving, nsup = check_living(read, entering_read, regular, run)
    loc_items = check_locators(scorecard, shonen, read)
    writes = lane_writes()
    items = axis_items + pin_items + living_items + loc_items
    mism = sum(1 for i in items if i[4] == "mismatch")
    errs = sum(1 for i in items if i[4] == "error") + (1 if writes else 0)
    if mism:
        failed.append("mismatch")
    if errs:
        failed.append("errors")
    if writes:
        failed.append("lane_writes")
    if hidden:
        failed.append("hidden")
    if npins < MIN_PINS:
        failed.append("pins_floor")
    if boxes < MIN_BOXES:
        failed.append("boxes_floor")
    if len(axis_items) != len(AXES):
        failed.append("axes")
    met = not failed
    out = ["item %s %s expect=%s got=%s state=%s" % (k, re.sub(r"\s+", "_", name), re.sub(r"\s+", "_", want),
                                                     re.sub(r"\s+", "_", got), st)
           for k, name, want, got, st in items]
    line = ("C1=%s items=%d axes=%d pins=%d boxes=%d living=%d superseded=%d locators=%d mismatches=%d errors=%d "
            "hidden=%d lane_writes=%d manifest=%s rev=%s"
            % ("met" if met else "unmet", len(items), len(axis_items), npins, boxes, nliving, nsup,
               len(loc_items), mism, errs, hidden, writes, manifest_tag, rev))
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
    repo = os.path.abspath(opts["--repo"] or os.path.dirname(os.path.dirname(os.path.dirname(here))))
    fleet = opts["--fleet-repo"] or os.path.dirname(repo)
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
    if opts["--scratch"]:
        base = os.path.abspath(opts["--scratch"])
        os.makedirs(base, exist_ok=True)
    else:
        base = tempfile.mkdtemp(prefix="count-c1-r52-")
    if os.path.commonpath([base, repo]) == repo:
        print("C1_SETUP scratch %s lies inside the repo %s" % (base, repo), file=sys.stderr)
        return 2

    def reader(r):
        def read(path):
            q = git(repo, "show", "%s:%s" % (r, path))
            return q.stdout.decode("utf-8", "surrogateescape") if q.returncode == 0 else None
        return read

    def exists(path):
        return git(repo, "cat-file", "-e", "%s:%s" % (rev, path)).returncode == 0

    def regular(path):
        q = git(repo, "ls-tree", rev, "--", path)
        f = q.stdout.decode().split()
        return q.returncode == 0 and len(f) >= 4 and f[0] in ("100644", "100755") and f[1] == "blob"

    def ls_lessons():
        q = git(repo, "ls-tree", "--name-only", rev, "corpus/lessons/")
        return q.stdout.decode().split("\n") if q.returncode == 0 else []

    def status():
        q = git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all")
        return set(q.stdout.decode("utf-8", "replace").split("\n")) if q.returncode == 0 else set()

    before = status()
    state = {"tree": None}

    def run(argv):
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
        exe = [sys.executable] + argv[1:] if argv[0] == "python3" else argv
        try:
            q = subprocess.run(exe, cwd=state["tree"], env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None
        found = TALLY.findall(q.stdout.decode("utf-8", "replace"))
        if not found:
            loose = ANY_TALLY.findall(q.stdout.decode("utf-8", "replace"))
            if not loose:
                return q.returncode, None
            pre, a_, f_ = loose[-1]
            return q.returncode, (pre or None, int(a_), int(f_))
        pre, a_, f_ = found[-1]
        return q.returncode, (pre, int(a_), int(f_))

    def lane_writes():
        new = status() - before
        for l in sorted(new):
            if l:
                print("lane_write %s" % l)
        return len([l for l in new if l])

    try:
        met, out, line = evaluate(reader(rev), reader(ENTERING), exists, regular, ls_lessons, run, manifest, rev,
                                  tag, lane_writes)
    finally:
        shutil.rmtree(base if not opts["--scratch"] else os.path.join(base, "tree"), ignore_errors=True)
        if opts["--scratch"]:
            shutil.rmtree(os.path.join(base, "tmp"), ignore_errors=True)
    for l in out:
        print(l)
    print(line)
    return 0 if met else 1


def selftest():
    manifest = json.dumps({"rounds": [
        {"lane": "mori", "lane_round": 40, "verdict": "admitted", "verdicts": {a: "improved" for a in AXES}},
        {"lane": "mori", "lane_round": 45, "verdict": "rejected-harmed",
         "verdicts": {"calibration": "harmed", "depth": "improved"}},
        {"lane": "mori", "lane_round": 46, "verdict": "admitted-pending",
         "verdicts": {"coverage": "improved"}},
        {"lane": "mori", "lane_round": 47, "verdict": "admitted",
         "verdicts": {"coverage": "improved", "operability": "harmed", "depth": "unchanged"}},
        {"lane": "mori", "lane_round": 49, "verdict": "admitted",
         "verdicts": {"calibration": "improved", "depth": "improved"}},
        {"lane": "mori", "lane_round": 52, "verdict": "admitted", "verdicts": {a: "improved" for a in AXES}},
        {"lane": "kama", "lane_round": 48, "verdict": "admitted", "verdicts": {a: "improved" for a in AXES}},
    ]})
    want = {"coverage": (47, "improved"), "operability": (47, "harmed"), "depth": (49, "improved"),
            "freshness": (40, "improved"), "calibration": (49, "improved"), "adjacency": (40, "improved")}
    spot_exists = {47, 49}
    closure49 = "\n".join(["# closure", "", "| axis | entering | verdict | basis |", "|---|---|---|---|"] + [
        "| %s | 6 | improved | held |" % a for a in AXES] + [""])

    def row(ax, n=None, v=None, ev=None, score="6"):
        n, v = (n, v) if n is not None else want[ax]
        ev = ev if ev is not None else (
            "closure `corpus/lessons/round-%d-verifier-spotcheck.md:3`" % n if n in spot_exists
            else "MANIFEST.json@abc mori round %d" % n)
        return "| %s | %s | %s | round %d (%s, score held); older note round 3 |" % (ax, score, ev, n, v)

    def scorecard(rows=None, extra="", pre=""):
        rows = rows if rows is not None else [row(a) for a in AXES]
        return "\n".join(["# Scorecard", "", pre, "## Axes", "",
                          "| Axis | Score | Evidence pointer | Last change |", "|---|---|---|---|"]
                         + rows + ["", extra, "## Move log", "| Round | Axis |", "|---|---|", "| 1 | x |"])

    obs = {"tools/a.py": ("A_SELFTEST", 114, 0), "tools/b.py": ("B_SELFTEST", 17, 0),
           "tools/c.py": ("C_SELFTEST", 22, 0)}

    def shonen(pin_a="`python3 tools/a.py --selftest` (114/114)",
               pin_b="`python3 tools/b.py --selftest` → `B_SELFTEST pass=17 fail=0`", extra="", boxes=4):
        lines = ["# SHONEN", "", "- [~] box one — `SKILL.md:1`", "- [~] box two — %s; %s" % (pin_a, pin_b)]
        for i in range(boxes - 2):
            lines.append("- [~] box %d — pointer" % (i + 3))
        return "\n".join(lines + [extra, ""])

    receipts = {RECEIPT_DIR + "a.txt": "$ python3 tools/a.py --selftest\nA_SELFTEST pass=114 fail=0\nrc=0\n",
                RECEIPT_DIR + "b.txt": "B_SELFTEST pass=17 fail=0\n"}
    quality_e = "\n".join(["# Q", "", "## Criteria", "",
                           "12. A gate. Check: `python3 tools/c.py --selftest` → `pass=12 fail=0`.", ""])
    readme_e = "\n".join(["# R", "", "| g | e | b |", "|---|---|---|",
                          "| x | y | `python3 tools/c.py --selftest` → `pass=12 fail=0` |", ""])
    quality_fix = quality_e + "\n".join(
        ["13. This row supersedes 12's check cell. Check: `python3 tools/c.py --selftest` → "
         "`C_SELFTEST pass=22 fail=0`.", ""])
    readme_fix = readme_e + ("\nRound-52 correction: this note supersedes `python3 tools/c.py --selftest` → "
                             "`pass=12 fail=0`; now `python3 tools/c.py --selftest` → `pass=22 fail=0`.\n")

    def files(sc=None, sh=None, rc=None, q=None, rd=None, drop=(), extra=None):
        f = {"SCORECARD.md": sc if sc is not None else scorecard(),
             "SHONEN.md": sh if sh is not None else shonen(),
             "tools/a.py": "x", "tools/b.py": "x", "tools/c.py": "x", "SKILL.md": "line\n",
             "corpus/QUALITY.md": q if q is not None else quality_fix,
             "corpus/README.md": rd if rd is not None else readme_fix}
        for n in spot_exists:
            f["corpus/lessons/round-%d-verifier-spotcheck.md" % n] = closure49 if n == 49 else "x\n" * 5
        f.update(rc if rc is not None else receipts)
        f.update(extra or {})
        for d in drop:
            f.pop(d, None)
        return f

    entering = {"corpus/QUALITY.md": quality_e, "corpus/README.md": readme_e}

    def run_eval(f, runner=None, symlinks=(), writes=0, ent=None):
        def default(argv):
            o = obs.get(argv[1])
            return (0, o) if o else (2, None)
        runner = runner or default
        ent = ent if ent is not None else entering
        return evaluate(lambda p: f.get(p), lambda p: ent.get(p), lambda p: p in f,
                        lambda p: p in f and p not in symlinks,
                        lambda: [p for p in f if p.startswith("corpus/lessons/")], runner, manifest, "R",
                        lane_writes=lambda: writes)

    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    check("targets_from_manifest", manifest_targets(manifest) == want)
    met, out, line = run_eval(files())
    check("honest_met", met and "mismatches=0 errors=0 hidden=0" in line and "axes=6 pins=2 boxes=4" in line
          and "living=4 superseded=2" in line)
    check("rejected_round_ignored", manifest_targets(manifest)["calibration"] == (49, "improved"))
    check("admitted_prefix_verdict_ignored", manifest_targets(manifest)["coverage"] == (47, "improved"))
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
    rows[0] = "| coverage | 6 | closure `corpus/lessons/round-47-verifier-spotcheck.md:3` | round 47 (unimproved) |"
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("verdict_substring_unmet", (not met) and any("verdict_word_missing" in o for o in out))
    rows = [row(a) for a in AXES]
    rows[0] = row("coverage", ev="no pointer here")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("evidence_pointer_missing_unmet", (not met) and any("evidence_missing" in o for o in out))
    rows = [row(a) for a in AXES]
    rows[3] = row("freshness", ev="`corpus/lessons/round-40-verifier-spotcheck.md`")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("absent_spotcheck_needs_manifest", (not met) and any("evidence_missing:MANIFEST.json" in o for o in out))
    met, out, line = run_eval(files(sc=scorecard([row(a) for a in AXES] + [row("depth")])))
    check("duplicate_axis_row_unmet", (not met) and any("rows=2" in o for o in out))
    met, out, line = run_eval(files(sc=scorecard(pre="## Axes\n\n| Axis | Score | Evidence pointer | Last change |"
                                                     "\n|---|---|---|---|\n| coverage | 9 | x | round 1 |\n")))
    check("second_axes_heading_unmet", (not met) and any("headings=2" in o for o in out))
    met, out, line = run_eval(files(sc=scorecard(pre="```\n## Axes\n```\n")))
    check("fenced_axes_heading_ignored_met", met)
    rows = [row(a) for a in AXES]
    rows[4] = row("calibration", score="7")
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("score_cell_unread_unmet", (not met) and any("score=7_closure_r49_states=6" in o for o in out))
    moved = closure49.replace("| depth | 6 | improved | held |", "| depth | 6 | improved | Score 6 → 7 |")
    rows = [row(a) for a in AXES]
    rows[2] = row("depth", score="7")
    met, out, line = run_eval(files(sc=scorecard(rows), extra={
        "corpus/lessons/round-49-verifier-spotcheck.md": moved}))
    check("score_move_read_met", met)
    met, out, line = run_eval(files(extra={"corpus/lessons/round-50-verifier-spotcheck.md":
                                           closure49.replace("| depth | 6 |", "| depth | 5 |")}))
    check("newest_closure_score_wins_unmet", (not met) and any("closure_r50_states=5" in o for o in out))
    # shonen arm
    met, out, line = run_eval(files(sh=shonen(pin_a="`python3 tools/a.py --selftest` (60/60)")))
    check("stale_pin_unmet", (not met) and "mismatches=1" in line)
    met, out, line = run_eval(files(drop=(RECEIPT_DIR + "b.txt",)))
    check("receipt_missing_unmet", (not met) and any("receipt_missing" in o for o in out))
    met, out, line = run_eval(files(), symlinks=("tools/a.py",))
    check("symlinked_pin_path_unmet", (not met) and any("unbound_or_not_regular" in o for o in out))
    met, out, line = run_eval(files(sh=shonen(extra="Also SELFTEST pass=3 somewhere")))
    check("hidden_tally_unmet", (not met) and "hidden" in line)
    met, out, line = run_eval(files(sh=shonen(boxes=3)))
    check("boxes_floor_unmet", (not met) and "boxes_floor" in line)
    met, out, line = run_eval(files(), runner=lambda argv: None)
    check("runner_timeout_is_error", (not met) and "errors" in line)
    # living arm
    met, out, line = run_eval(files(q=quality_e, rd=readme_e))
    check("living_stale_unmet", (not met) and "living=2 superseded=0" in line and "mismatches=2" in line)
    met, out, line = run_eval(files(q=quality_e.replace("pass=12", "pass=22"), rd=readme_fix))
    check("living_rewritten_in_place_unmet", (not met) and any("pin_removed_or_rewritten" in o for o in out))
    met, out, line = run_eval(files(q="# Q\n", rd=readme_fix))
    check("living_pin_deleted_unmet", (not met) and any("pin_removed_or_rewritten" in o for o in out))
    bad_sup = quality_e + "13. This row supersedes 12's check cell. Check: `python3 tools/c.py --selftest` → `pass=12 fail=0`.\n"
    met, out, line = run_eval(files(q=bad_sup))
    check("living_superseding_pin_wrong_unmet", (not met) and "mismatches=1" in line)
    self_sup = quality_e.replace("→ `pass=12 fail=0`.", "→ `pass=12 fail=0`; supersedes 12's check.")
    met, out, line = run_eval(files(q=self_sup), ent={"corpus/QUALITY.md": self_sup, "corpus/README.md": readme_e})
    check("living_self_supersede_not_counted_unmet", (not met) and "mismatches=1" in line)
    frag = readme_fix + "| z | w | `--selftest` → `pass=9 fail=0` |\n"
    met, out, line = run_eval(files(rd=frag))
    check("living_fragment_unrunnable_unmet", (not met) and any("unrunnable" in o for o in out))
    ph = readme_fix + "| z | w | `python3 tools/c.py <rev> --selftest` → `pass=22 fail=0` |\n"
    met, out, line = run_eval(files(rd=ph))
    check("living_placeholder_unrunnable_unmet", (not met) and any("unrunnable" in o for o in out))
    met, out, line = run_eval(files(), runner=lambda argv: (1, obs.get(argv[1])))
    check("living_nonzero_rc_unmet", (not met) and any("rc=1" in o for o in out))
    met, out, line = run_eval(files(), writes=3)
    check("lane_writes_error_unmet", (not met) and "lane_writes=3" in line and "errors" in line)
    check("multiline_span_not_enumerated", living_pins("`python3 a.py --selftest\n--x` → `pass=1 fail=0`") == [])
    # locator arm
    good = row("coverage", ev='closure "held as declared" (`SKILL.md:1`) `corpus/lessons/round-47-verifier-spotcheck.md:3`')
    met, out, line = run_eval(files(sc=scorecard([good] + [row(a) for a in AXES[1:]]),
                                    extra={"SKILL.md": "held   as\ndeclared here\n"}))
    check("locator_quote_ws_folded_unmet_when_split", (not met))
    met, out, line = run_eval(files(sc=scorecard([good] + [row(a) for a in AXES[1:]]),
                                    extra={"SKILL.md": "it was held   as declared here\n"}))
    check("locator_quote_found_met", met)
    bad = row("coverage", ev='closure "Score 6 → 6" (`SKILL.md:1`) `corpus/lessons/round-47-verifier-spotcheck.md:3`')
    met, out, line = run_eval(files(sc=scorecard([bad] + [row(a) for a in AXES[1:]])))
    check("locator_quote_absent_unmet", (not met) and any("quote:Score_6_→_6" in o and "absent" in o for o in out))
    pr = row("freshness", ev="MANIFEST.json; round 28 proposed 5 → 6 (`SKILL.md:1`)")
    rows = [row(a) for a in AXES]
    rows[3] = pr
    met, out, line = run_eval(files(sc=scorecard(rows)))
    check("locator_pair_absent_unmet", (not met) and any("pair:5_→_6" in o for o in out))
    met, out, line = run_eval(files(sc=scorecard(rows), extra={"SKILL.md": "freshness 5 → 6 proposed\n"}))
    check("locator_pair_found_met", met)
    met, out, line = run_eval(files(sh=shonen().replace("`SKILL.md:1`", "`SKILL.md:2-9`")))
    check("locator_out_of_range_unmet", (not met) and any("out_of_range" in o for o in out))
    met, out, line = run_eval(files(sh=shonen().replace("`SKILL.md:1`", "`NOPE.md:1`")))
    check("locator_file_absent_unmet", (not met) and any("file_absent" in o for o in out))
    check("loose_tally_parses", ANY_TALLY.findall("x pass=22 fail=0")[-1] == ("", "22", "0"))
    for name, cond in checks:
        print("%s %s" % ("PASS" if cond else "FAIL", name))
    failn = sum(1 for _, c in checks if not c)
    print("C1_SELFTEST pass=%d fail=%d" % (len(checks) - failn, failn))
    return 0 if failn == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
