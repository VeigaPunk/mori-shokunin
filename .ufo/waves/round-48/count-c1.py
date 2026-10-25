#!/usr/bin/env python3
"""Round 48 C1 counter (calibration) — can the registry pin reconciler be fooled?

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, the tool bytes under test (tools/mori-pin-check.py at R) score
  PIN_CHECK=unmet on each of the eight frozen junk edits J1-J8 of R's SKILL.md and
  PIN_CHECK=met on each of the four frozen honest edits H1-H4 of R's SKILL.md and on R's
  unedited SKILL.md, every run with --min-tally-pins 26 --baseline-rev 2d85e33d (the round-47
  baseline: the round-47 gate rows carry no baseline obligation, so hiding them is not `dropped`).

Variants are edit functions over R's SKILL.md text (so they stay valid when R's registry
rows move); an edit whose anchor is absent at R is a setup error (exit 2), never a pass.
  J1 header spelled `selftest` (no hyphen) over the round-47 gate table, with corrupt pins
  J2 fullwidth-underscore tally prefix on a new row (pin pass=999)
  J3 Cyrillic letter inside the tally prefix of a new row (pin pass=999)
  J4 new row pinning a stale tally to an archived copy of an existing instrument
  J5 the two round-47 gate rows replaced by a fenced block carrying corrupt pins
  J6 a blank line between a gate table's header and its first row, first pin corrupted
  J7 line-count pin in a self-test cell off by one (`(743 lines)` -> `(742 lines)`)
  J8 truncated digest pin in a self-test cell off by one hex digit (`37fd7c24ff52…`)
  H1 R's SKILL.md with one prose line appended
  H2 a trailing escaped pipe on one gate row (benign)
  H3 the round-47 gate table header spelled `Self-Test` (case only)
  H4 a new honest row for the count-c2.py round-47 instrument under a new row name

Usage: count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] [--min-tally N]
                   [--jobs N] [--scratch DIR]   |   count-c1.py --selftest
Output: `C1=met|unmet junk_met=N honest_unmet=N real=met|unmet variants=N rev=R` (+ one
`variant name=… expect=… got=… rc=…` line each). Exit 0 met, 1 unmet, 2 setup.
Read-only over git; the tool under test writes only inside `--scratch`.
"""
import concurrent.futures
import os
import re
import subprocess
import sys
import tempfile

BASELINE = "2d85e33d14198d388fd3cda9cc15ec07e57e7a53"
MIN_TALLY = 26
ARCHIVED = ".ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py"
TOOL_TIMEOUT = 900


class Anchor(Exception):
    pass


def lines_of(text):
    return text.split("\n")


def find_line(ls, pattern, nth=0):
    hits = [i for i, l in enumerate(ls)
            if l.lstrip().startswith("|") and re.search(r"(?<![A-Za-z0-9_])" + pattern, l)]
    if len(hits) <= nth:
        raise Anchor("no line matches %r" % pattern)
    return hits[nth]


def table_header_above(ls, i):
    """Index of the header line (a table row followed by a separator row) above row i."""
    j = i
    while j > 0 and ls[j - 1].lstrip().startswith("|"):
        j -= 1
    return j


def new_row(prefix, argv_text, entry_cell, name, pin="pass=999 fail=0"):
    return ("| %s | gate | %s | 0/1/2 | `%s` → `%s %s` | none | none | mori |"
            % (name, entry_cell, argv_text, prefix, pin))


def r47_rows(ls):
    """(index of the PIN_CHECK_SELFTEST row, index of the first C2_SELFTEST row after it)."""
    a = find_line(ls, r"PIN_CHECK_SELFTEST pass=\d+ fail=0")
    for b in range(a + 1, len(ls)):
        if ls[b].lstrip().startswith("|") and re.search(r"(?<![A-Za-z0-9_])C2_SELFTEST pass=\d+ fail=0", ls[b]):
            return a, b
    raise Anchor("no C2_SELFTEST row after the PIN_CHECK_SELFTEST row")


def v_j1(text):
    ls = lines_of(text)
    a, b = r47_rows(ls)
    h = table_header_above(ls, a)
    if "self-test" not in ls[h]:
        raise Anchor("header cell self-test not found")
    ls[h] = ls[h].replace("self-test", "selftest", 1)
    for k in (a, b):
        ls[k] = re.sub(r"pass=\d+ fail=0", "pass=1 fail=0", ls[k])
    return "\n".join(ls)


def _append_after_gate_table(text, row):
    ls = lines_of(text)
    a, b = r47_rows(ls)
    ls.insert(b + 1, row)
    return "\n".join(ls)


def v_j2(text):
    return _append_after_gate_table(text, new_row(
        "PIN_CHECK\uff3fSELFTEST", "python3 tools/mori-pin-check.py --selftest",
        "`python3 tools/mori-pin-check.py --rev <rev>`", "r48 junk fullwidth"))


def v_j3(text):
    return _append_after_gate_table(text, new_row(
        "PIN_CHECK_S\u0415LFTEST", "python3 tools/mori-pin-check.py --selftest",
        "`python3 tools/mori-pin-check.py --rev <rev>`", "r48 junk cyrillic"))


def v_j4(text):
    return _append_after_gate_table(text, new_row(
        "MORI_SOURCES_APPENDONLY_SELFTEST", "python3 %s --selftest" % ARCHIVED,
        "`python3 %s <rev> --round-base REV`" % ARCHIVED, "r48 junk archived copy",
        pin="pass=12 fail=0"))


def v_j5(text):
    ls = lines_of(text)
    a, b = r47_rows(ls)
    if b != a + 1:
        raise Anchor("round-47 gate rows not adjacent")
    rows = [re.sub(r"pass=\d+ fail=0", "pass=1 fail=0", ls[a]), re.sub(r"pass=\d+ fail=0", "pass=1 fail=0", ls[b])]
    ls[a:b + 1] = ["```markdown"] + rows + ["```"]
    return "\n".join(ls)


def v_j6(text):
    ls = lines_of(text)
    a = find_line(ls, r"PIN_CHECK_SELFTEST pass=\d+ fail=0")
    h = table_header_above(ls, a)
    ls[a] = re.sub(r"(PIN_CHECK_SELFTEST) pass=\d+ fail=0", r"\1 pass=1 fail=0", ls[a])
    # blank line between the separator row and the first data row
    ls.insert(h + 2, "")
    return "\n".join(ls)


def v_j7(text):
    if "(743 lines)" not in text:
        raise Anchor("(743 lines) absent")
    return text.replace("(743 lines)", "(742 lines)", 1)


def v_j8(text):
    if "37fd7c24ff52\u2026" not in text:
        raise Anchor("37fd7c24ff52… absent")
    return text.replace("37fd7c24ff52\u2026", "37fd7c24ff53\u2026", 1)


def v_h1(text):
    return text.rstrip("\n") + "\n\nA prose line appended by the round-48 honest control.\n"


def v_h2(text):
    ls = lines_of(text)
    a = find_line(ls, r"PIN_CHECK_SELFTEST pass=\d+ fail=0")
    if not ls[a].rstrip().endswith("|"):
        raise Anchor("gate row does not end with a pipe")
    ls[a] = ls[a].rstrip()[:-1] + "\\|"
    return "\n".join(ls)


def v_h3(text):
    ls = lines_of(text)
    a = find_line(ls, r"PIN_CHECK_SELFTEST pass=\d+ fail=0")
    h = table_header_above(ls, a)
    if "self-test" not in ls[h]:
        raise Anchor("header cell self-test not found")
    ls[h] = ls[h].replace("self-test", "Self-Test", 1)
    return "\n".join(ls)


def v_h4(text):
    ls = lines_of(text)
    a, b = r47_rows(ls)
    m = re.search(r"(?<![A-Za-z0-9_])C2_SELFTEST (pass=\d+ fail=0)", ls[b])
    return _append_after_gate_table(text, new_row(
        "C2_SELFTEST", "python3 .ufo/waves/round-47/count-c2.py --selftest",
        "`python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR]`",
        "r48 honest second pin row", pin=m.group(1)))


VARIANTS = [
    ("J1", "unmet", v_j1), ("J2", "unmet", v_j2), ("J3", "unmet", v_j3), ("J4", "unmet", v_j4),
    ("J5", "unmet", v_j5), ("J6", "unmet", v_j6), ("J7", "unmet", v_j7), ("J8", "unmet", v_j8),
    ("H1", "met", v_h1), ("H2", "met", v_h2), ("H3", "met", v_h3), ("H4", "met", v_h4),
]


def git_show(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8")


def run_tool(tool, repo, rev, skill, baseline, min_tally, scratch):
    cmd = [sys.executable, "-I", "-B", tool, "--rev", rev, "--repo", repo,
           "--min-tally-pins", str(min_tally), "--baseline-rev", baseline]
    if skill:
        cmd += ["--skill", skill]
    env = dict(os.environ, TMPDIR=scratch, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=TOOL_TIMEOUT)
        out = p.stdout.decode("utf-8", "replace")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        return "timeout", None
    got = None
    for l in out.splitlines():
        m = re.match(r"PIN_CHECK=(met|unmet)\b", l)
        if m:
            got = m.group(1)
    # a tool crash or a setup exit is neither met nor unmet
    if rc not in (0, 1) or got is None:
        got = "error"
    elif (got == "met") != (rc == 0):
        got = "error"
    return got, rc


def measure(tool, repo, rev, baseline, min_tally, scratch, jobs, run=run_tool):
    text = git_show(repo, rev, "SKILL.md")
    if text is None:
        return None, "SKILL.md unreadable at %s" % rev
    jobs_list = []
    os.makedirs(scratch, exist_ok=True)
    for name, expect, fn in VARIANTS:
        try:
            body = fn(text)
        except Anchor as exc:
            return None, "variant %s anchor: %s" % (name, exc)
        path = os.path.join(scratch, "variant-%s.md" % name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        jobs_list.append((name, expect, path))
    jobs_list.append(("real", "met", None))
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {}
        for name, expect, path in jobs_list:
            sub = tempfile.mkdtemp(prefix="c1-%s-" % name, dir=scratch)
            futs[ex.submit(run, tool, repo, rev, path, baseline, min_tally, sub)] = (name, expect)
        for fut in concurrent.futures.as_completed(futs):
            name, expect = futs[fut]
            got, rc = fut.result()
            results.append((name, expect, got, rc))
    results.sort(key=lambda r: ([v[0] for v in VARIANTS] + ["real"]).index(r[0]))
    return results, None


def verdict(results, rev):
    junk_met = sum(1 for n, e, g, r in results if e == "unmet" and g != "unmet")
    honest_unmet = sum(1 for n, e, g, r in results if e == "met" and n != "real" and g != "met")
    real = [g for n, e, g, r in results if n == "real"][0]
    errors = sum(1 for n, e, g, r in results if g in ("error", "timeout"))
    met = junk_met == 0 and honest_unmet == 0 and real == "met" and errors == 0
    line = "C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s" % (
        "met" if met else "unmet", junk_met, honest_unmet, real, errors,
        len(results) - 1, rev)
    return met, line


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    args = list(argv)
    opts = {"--tool": None, "--rev": "HEAD", "--repo": None, "--baseline": BASELINE,
            "--min-tally": str(MIN_TALLY), "--jobs": "4", "--scratch": None}
    for k in list(opts):
        while k in args:
            i = args.index(k)
            opts[k] = args[i + 1]
            del args[i:i + 2]
    if args or opts["--tool"] is None:
        print("C1_SETUP usage: count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] "
              "[--min-tally N] [--jobs N] [--scratch DIR] | --selftest", file=sys.stderr)
        return 2
    repo = opts["--repo"] or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    try:
        rev = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", opts["--rev"] + "^{commit}"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
                             check=True).stdout.decode().strip()
    except (subprocess.SubprocessError, OSError):
        print("C1_SETUP unresolvable revision %s" % opts["--rev"], file=sys.stderr)
        return 2
    scratch = opts["--scratch"] or tempfile.mkdtemp(prefix="c1-", dir=os.path.join(repo, ".scratch"))
    tool = os.path.abspath(opts["--tool"])
    results, err = measure(tool, repo, rev, opts["--baseline"], int(opts["--min-tally"]),
                           scratch, int(opts["--jobs"]))
    if err:
        print("C1_SETUP %s" % err, file=sys.stderr)
        return 2
    for name, expect, got, rc in results:
        print("variant name=%s expect=%s got=%s rc=%s" % (name, expect, got, rc))
    met, line = verdict(results, rev)
    print(line)
    return 0 if met else 1


def selftest():
    """Counter arms: variants apply to a synthetic registry, verdict logic classifies the
    four control shapes (do-nothing, always-met, always-unmet, correct)."""
    text = "\n".join([
        "# registry", "",
        "| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |",
        "|---|---|---|---|---|---|---|---|",
        "| a (r44) | gate | `python3 tools/a.py <rev>` | 0/1 | `python3 tools/a.py --selftest` → `A_SELFTEST pass=3 fail=0` at sha256 `37fd7c24ff52…` (743 lines) | none | none | mori |",
        "| pin (r47) | gate | `python3 tools/p.py --rev <rev>` | 0/1 | `python3 tools/p.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` | none | none | mori |",
        "| c2 (r47) | gate | `python3 .ufo/waves/round-47/count-c2.py <rev>` | 0/1 | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | none | none | mori |",
        ""])
    results_ok = 0
    checks = []

    def check(name, cond):
        nonlocal results_ok
        checks.append((name, cond))
        results_ok += 1 if cond else 0

    # variants: anchors needed only for J7/J8 (synthetic text carries them in row `a`)
    text = text.replace("(743 lines)", "(743 lines)")
    for name, expect, fn in VARIANTS:
        try:
            body = fn(text)
            check("apply_%s" % name, body != text)
        except Anchor as exc:
            check("apply_%s" % name, False)
    for name, expect, fn in VARIANTS:
        b1 = fn(text)
        check("deterministic_%s" % name, b1 == fn(text))
    check("variant_names_unique", len({v[0] for v in VARIANTS}) == len(VARIANTS))
    check("eight_junk_four_honest",
          sum(1 for v in VARIANTS if v[1] == "unmet") == 8 and sum(1 for v in VARIANTS if v[1] == "met") == 4)
    # anchor failure is setup, not pass
    try:
        v_j7("nothing here")
        check("anchor_absent_raises", False)
    except Anchor:
        check("anchor_absent_raises", True)

    def fake(got_for):
        def run(tool, repo, rev, skill, baseline, min_tally, scratch):
            name = os.path.basename(skill)[len("variant-"):-3] if skill else "real"
            return got_for(name), 0
        return run

    import shutil
    d = tempfile.mkdtemp(prefix="c1-selftest-")
    try:
        sub = subprocess.run(["git", "init", "-q", d], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=s@s.invalid",
                        "commit", "-q", "--allow-empty", "-m", "x"], check=True)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write(text)
        subprocess.run(["git", "-C", d, "add", "SKILL.md"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=s@s.invalid",
                        "commit", "-q", "-m", "skill"], check=True)
        rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], stdout=subprocess.PIPE,
                             check=True).stdout.decode().strip()
        sc = os.path.join(d, "scratch")
        for label, fn, want in [
            ("correct_met", lambda n: "unmet" if n.startswith("J") else "met", True),
            ("do_nothing_unmet", lambda n: "met", False),
            ("always_unmet_unmet", lambda n: "unmet", False),
            ("one_junk_green", lambda n: "met" if n == "J6" else ("unmet" if n.startswith("J") else "met"), False),
            ("real_red", lambda n: "unmet" if (n.startswith("J") or n == "real") else "met", False),
            ("error_not_unmet", lambda n: "error" if n == "J3" else ("unmet" if n.startswith("J") else "met"), False),
        ]:
            res, err = measure("tool", d, rev, "x", 1, sc, 2, run=fake(fn))
            ok = err is None and verdict(res, rev)[0] is want
            check("verdict_%s" % label, ok)
        # a variant anchor missing at R is a setup error
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write("# empty\n")
        subprocess.run(["git", "-C", d, "add", "SKILL.md"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=s@s.invalid",
                        "commit", "-q", "-m", "empty"], check=True)
        rev2 = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], stdout=subprocess.PIPE,
                              check=True).stdout.decode().strip()
        res, err = measure("tool", d, rev2, "x", 1, sc, 2, run=fake(lambda n: "unmet"))
        check("missing_anchor_is_setup", res is None and err is not None)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    for name, cond in checks:
        print("%s %s" % ("PASS" if cond else "FAIL", name))
    fail = len(checks) - results_ok
    print("C1_SELFTEST pass=%d fail=%d" % (results_ok, fail))
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
