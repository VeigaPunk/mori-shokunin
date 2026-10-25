#!/usr/bin/env python3
"""Round 49 C1 counter (calibration) — can the registry pin reconciler be fooled, and does it
survive honest edits, when it cannot tell which edit it is looking at?

Frozen predicate P-C1 (same sentence in contract.md, this counter and the receipt label):
  At revision R, the tool bytes under test (tools/mori-pin-check.py at R) score
  PIN_CHECK=unmet on each of the eighteen frozen junk edits (the eight round-48 edits J1-J8 and
  ten new edits N1-N10) and PIN_CHECK=met on each of the seven frozen honest edits (H1-H4 of
  round 48 and H5-H7) and on R's SKILL.md read twice (as the revision's own file and as an
  opaque-named copy), every run with --min-tally-pins 26 --baseline-rev 2d85e33d. Every variant
  is handed to the tool under an opaque name: the SKILL.md copy and the scratch directory are
  named by a sha256 prefix of their bytes, the order of the runs follows that hash, and the two
  edits that change a second tracked file (the instrument a pin measures) are built in a throwaway
  fixture repository whose path and commit message carry no variant name.

Variant edits are functions over R's SKILL.md text (so they stay valid when R's registry rows
move); an anchor absent at R is a setup error (exit 2), never a pass. Round-48 variants J1-J8 and
H1-H4 are imported unchanged from .ufo/waves/round-48/count-c1.py.
  N1  one gate row inside an HTML comment, after a blank line (pin pass=999)
  N2  NBSP in the self-test header cell and a zero-width space inside the pin token
  N3  a tab-indented pipe row inside a fence
  N4  a pipe row indented four spaces, outside any table
  N5  a second row for the same command under a new name with a contradicting exit contract
  N6  a command row with no pin, then prose `fail=0` and a continuation line recording `fail=3`
  N7  the same junk row written as HTML table markup
  N8  the existing reconciler row re-pointed so its entry cell names the reconciler while its
      self-test cell runs the unlanded check and pins that check's tally
  N9  a new row that names the gate registry in its entry cell and pins the reconciler's tally
  N10 (fixture) an instrument gains one self-test arm (two arms to three) and the registry pin
      stays at the old tally
  H5  (fixture) the same instrument edit with the registry pin moved to the new tally
  H6  an HTML comment and an HTML table that carry no pin token
  H7  an indented pipe row and a tab-indented fenced row that carry no pin token

Usage: count-c1.py --tool PATH [--rev R] [--repo DIR] [--baseline E] [--min-tally N]
                   [--jobs N] [--scratch DIR]   |   count-c1.py --selftest
Output: one `variant name=… expect=… got=… rc=…` line per run, then
`C1=met|unmet junk_met=N honest_unmet=N real=met|unmet errors=N variants=N rev=R`.
Exit 0 met, 1 unmet, 2 setup. The tool under test writes only inside `--scratch` (and the
throwaway fixture repository it is pointed at); the lane repo is only read.
"""
import concurrent.futures
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
_spec = importlib.util.spec_from_file_location("r48c1", os.path.join(HERE, "..", "round-48", "count-c1.py"))
r48 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r48)

BASELINE = r48.BASELINE
MIN_TALLY = r48.MIN_TALLY
TOOL_TIMEOUT = r48.TOOL_TIMEOUT
Anchor = r48.Anchor
lines_of = r48.lines_of

HEADER = ("| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
          "|---|---|---|---|---|---|---|---|\n")
ENTRY_PIN = "`python3 tools/mori-pin-check.py --rev <rev>`"


def _append(text, block):
    return text.rstrip("\n") + "\n\n" + block + "\n"


def _cur_pin(text, prefix, cmd_hint=None):
    ms = re.findall(r"(?<![A-Za-z0-9_])%s pass=(\d+) fail=0" % prefix, text)
    if not ms:
        raise Anchor("no %s pin" % prefix)
    return int(ms[0])


def v_n1(text):
    return _append(text, "<!-- | r49 html comment | gate | %s | 0/1/2 | `PIN_CHECK_SELFTEST pass=999 fail=0` "
                         "| none | none | mori -->" % ENTRY_PIN)


def v_n2(text):
    hdr = HEADER.replace("self-test", "self\u00a0test")
    return _append(text, hdr + "| r49 zwsp | gate | %s | 0/1/2 | `PIN_CHECK_\u200bSELFTEST pass=999 fail=0` "
                         "| none | none | mori |" % ENTRY_PIN)


def v_n3(text):
    return _append(text, "```\n\t| r49 tab fence | gate | %s | 0/1/2 | `PIN_CHECK_SELFTEST pass=999 fail=0` "
                         "| none | none | mori |\n```" % ENTRY_PIN)


def v_n4(text):
    return _append(text, "    | r49 four space | gate | %s | 0/1/2 | `PIN_CHECK_SELFTEST pass=999 fail=0` "
                         "| none | none | mori |" % ENTRY_PIN)


def v_n5(text):
    cur = _cur_pin(text, "PIN_CHECK_SELFTEST")
    row = ("| r49 pin reconciler second authority | gate | %s | 0 \u2192 `PIN_CHECK=met` \u00b7 "
           "1 \u2192 `PIN_CHECK_SETUP` (a red run is an environment error, never a finding) \u00b7 "
           "2 \u2192 `PIN_CHECK_SETUP` | `python3 tools/mori-pin-check.py --selftest` \u2192 "
           "`PIN_CHECK_SELFTEST pass=%d fail=0` | none | none | mori |" % (ENTRY_PIN, cur))
    return _append(text, HEADER + row)


def v_n6(text):
    row = ("| r49 split tally | gate | %s | 0 \u2192 `PIN_CHECK=met` \u00b7 1 \u2192 `PIN_CHECK=unmet` \u00b7 "
           "2 \u2192 setup | `python3 tools/mori-pin-check.py --selftest` | the prose reading of the run is "
           "`pass=60 fail=0` | none | mori |" % ENTRY_PIN)
    cont = ("\u2192 the observed text was split across two lines: `PIN_CHECK_SELFTEST pass=60` then `fail=3` "
            "on the next, so the prose `fail=0` above is wrong and no pin in this row is checked.")
    return _append(text, HEADER + row + "\n\n" + cont)


def v_n7(text):
    return _append(text, "<table>\n<tr><td>r49 html table</td><td>gate</td><td><code>python3 tools/mori-pin-check.py "
                         "--rev &lt;rev&gt;</code></td><td>0/1/2</td><td><code>python3 tools/mori-pin-check.py "
                         "--selftest</code> \u2192 <code>PIN_CHECK_SELFTEST pass=999 fail=0</code></td><td>none</td>"
                         "<td>none</td><td>mori</td></tr>\n</table>")


def v_n8(text):
    ls = lines_of(text)
    hits = [i for i, l in enumerate(ls)
            if l.lstrip().startswith("|") and re.search(r"(?<![A-Za-z0-9_])PIN_CHECK_SELFTEST pass=\d+ fail=0", l)
            and "python3 tools/mori-pin-check.py --selftest" in l]
    if len(hits) != 1:
        raise Anchor("reconciler self-test row: %d hits" % len(hits))
    i = hits[0]
    ls[i] = ls[i].replace("python3 tools/mori-pin-check.py --selftest", "python3 tools/mori-unlanded-check.py --selftest", 1)
    ls[i] = re.sub(r"(?<![A-Za-z0-9_])PIN_CHECK_SELFTEST pass=\d+ fail=0", "UNLANDED_SELFTEST pass=%d fail=0"
                   % _cur_pin(text, "UNLANDED_SELFTEST"), ls[i], count=1)
    return "\n".join(ls)


def v_n9(text):
    cur = _cur_pin(text, "PIN_CHECK_SELFTEST")
    row = ("| r49 gate registry misattributed | gate | `python3 tools/mori-gate-registry.py --rev <rev> --audit <path>` "
           "| 0/1/2 | `python3 tools/mori-pin-check.py --selftest` \u2192 `PIN_CHECK_SELFTEST pass=%d fail=0` "
           "| none | none | mori |" % cur)
    return _append(text, HEADER + row)


def v_h6(text):
    return _append(text, "<!-- an honest note: nothing pinned here -->\n\n<table>\n<tr><td>note</td><td>plain prose cell</td>"
                         "</tr>\n</table>")


def v_h7(text):
    return _append(text, "    | an | indented | example | row |\n\n```\n\t| a | tab-indented | example | row |\n```")


FIX_HEADER = ("| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |\n"
              "|---|---|---|---|---|---|---|---|\n")


def _probe_src(arms):
    body = ["#!/usr/bin/env python3", "import sys", "if sys.argv[1:] == [\"--selftest\"]:"]
    body += ["    print(\"PASS arm%d\")" % i for i in range(arms)]
    body += ["    print(\"PROBE_SELFTEST pass=%d fail=0\")" % arms, "    sys.exit(0)", "print(\"PROBE=met\")", ""]
    return "\n".join(body)


def _fixture_skill(pin):
    return ("# fixture registry\n\n" + FIX_HEADER +
            "| probe gate | gate | `python3 tools/probe.py --rev <rev>` | 0 \u2192 `PROBE=met` \u00b7 1 \u2192 `PROBE=unmet` "
            "| `python3 tools/probe.py --selftest` \u2192 `PROBE_SELFTEST pass=%d fail=0` | none | none | fixture |\n" % pin)


def fixture_variant(dest, move_pin):
    """Build a fixture repository: commit 0 has the instrument (2 arms) and its pin (2); commit 1 adds an
    arm (3) and moves the pin to 3 when asked. Returns (dir, new commit, baseline commit)."""
    d = os.path.join(dest, "w-" + opaque("fixture", str(move_pin), dest))
    os.makedirs(os.path.join(d, "tools"))
    ident = ["-c", "user.name=c1", "-c", "user.email=c1@example.invalid"]
    subprocess.run(["git", "-C", d, "init", "-q"], check=True, timeout=60)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, check=True,
                         timeout=60).stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise Anchor("fixture is not its own repository")

    def commit(msg):
        subprocess.run(["git", "-C", d, "add", "-A"], check=True, timeout=60)
        subprocess.run(["git", "-C", d] + ident + ["commit", "-q", "-m", msg], check=True, timeout=60,
                       stdout=subprocess.DEVNULL)
        return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], stdout=subprocess.PIPE, check=True,
                              timeout=60).stdout.decode().strip()

    with open(os.path.join(d, "tools", "probe.py"), "w") as f:
        f.write(_probe_src(2))
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(_fixture_skill(2))
    c0 = commit("c")
    with open(os.path.join(d, "tools", "probe.py"), "w") as f:
        f.write(_probe_src(3))
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(_fixture_skill(3 if move_pin else 2))
    c1 = commit("c")
    return d, c1, c0


NEW_VARIANTS = [
    ("N1", "unmet", v_n1), ("N2", "unmet", v_n2), ("N3", "unmet", v_n3), ("N4", "unmet", v_n4),
    ("N5", "unmet", v_n5), ("N6", "unmet", v_n6), ("N7", "unmet", v_n7), ("N8", "unmet", v_n8),
    ("N9", "unmet", v_n9), ("H6", "met", v_h6), ("H7", "met", v_h7),
]
CLONE_VARIANTS = [("N10", "unmet", False), ("H5", "met", True)]  # built by fixture_variant
ORDER = ([v[0] for v in r48.VARIANTS] + [v[0] for v in NEW_VARIANTS] + [v[0] for v in CLONE_VARIANTS]
         + ["real", "real-opaque"])


def opaque(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p if isinstance(p, bytes) else p.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:12]


def run_tool(tool, repo, rev, skill, baseline, min_tally, scratch):
    cmd = [sys.executable, "-I", "-B", tool, "--rev", rev, "--repo", repo,
           "--min-tally-pins", str(min_tally), "--baseline-rev", baseline]
    if skill:
        cmd += ["--skill", skill]
    env = dict(os.environ, TMPDIR=scratch, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=TOOL_TIMEOUT)
        out = p.stdout.decode("utf-8", "replace")
        rc = p.returncode
    except subprocess.TimeoutExpired:
        return "timeout", None
    got = None
    for l in out.splitlines():
        m = re.match(r"PIN_CHECK=(met|unmet)\b", l)
        if m:
            got = m.group(1)
    if rc not in (0, 1) or got is None:
        got = "error"
    elif (got == "met") != (rc == 0):
        got = "error"
    return got, rc


def plan(repo, rev, scratch, baseline=BASELINE, min_tally=MIN_TALLY):
    """List of (name, expect, skill_path_or_None, repo, rev, tmpdir, baseline, min_tally) — opaque names for the tool."""
    text = r48.git_show(repo, rev, "SKILL.md")
    if text is None:
        return None, "SKILL.md unreadable at %s" % rev
    os.makedirs(scratch, exist_ok=True)
    jobs = []

    def stage(name, expect, body):
        tag = opaque(rev, body)
        path = os.path.join(scratch, "s-%s.md" % tag)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        jobs.append((name, expect, path, repo, rev, os.path.join(scratch, "t-" + tag), baseline, min_tally))

    try:
        for name, expect, fn in list(r48.VARIANTS) + NEW_VARIANTS:
            stage(name, expect, fn(text))
        stage("real-opaque", "met", text)
        for name, expect, move in CLONE_VARIANTS:
            d, sha, base = fixture_variant(scratch, move)
            jobs.append((name, expect, None, d, sha, os.path.join(scratch, "t-" + opaque(sha)), base, 1))
    except Anchor as exc:
        return None, "variant anchor: %s" % exc
    except (subprocess.SubprocessError, OSError) as exc:
        return None, "fixture variant: %s" % exc
    jobs.append(("real", "met", None, repo, rev, os.path.join(scratch, "t-" + opaque(rev, "real")), baseline, min_tally))
    jobs.sort(key=lambda j: os.path.basename(j[5]))
    for j in jobs:
        os.makedirs(j[5], exist_ok=True)
    return jobs, None


def measure(tool, repo, rev, baseline, min_tally, scratch, jobs, run=run_tool):
    pl, err = plan(repo, rev, scratch, baseline, min_tally)
    if err:
        return None, err
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {}
        for name, expect, skill, rrepo, rrev, tmp, rbase, rmin in pl:
            futs[ex.submit(run, tool, rrepo, rrev, skill, rbase, rmin, tmp)] = (name, expect)
        for fut in concurrent.futures.as_completed(futs):
            name, expect = futs[fut]
            got, rc = fut.result()
            results.append((name, expect, got, rc))
    results.sort(key=lambda r: ORDER.index(r[0]))
    return results, None


def verdict(results, rev):
    junk_met = sum(1 for n, e, g, r in results if e == "unmet" and g != "unmet")
    honest_unmet = sum(1 for n, e, g, r in results if e == "met" and n != "real" and g != "met")
    real = [g for n, e, g, r in results if n == "real"][0]
    errors = sum(1 for n, e, g, r in results if g in ("error", "timeout"))
    met = junk_met == 0 and honest_unmet == 0 and real == "met" and errors == 0
    line = "C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s" % (
        "met" if met else "unmet", junk_met, honest_unmet, real, errors, len(results) - 1, rev)
    return met, line


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    args = list(argv)
    opts = {"--tool": None, "--rev": "master", "--repo": None, "--baseline": BASELINE,
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
    repo = opts["--repo"] or LANE
    try:
        rev = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", opts["--rev"] + "^{commit}"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
                             check=True).stdout.decode().strip()
    except (subprocess.SubprocessError, OSError):
        print("C1_SETUP unresolvable revision %s" % opts["--rev"], file=sys.stderr)
        return 2
    scratch = opts["--scratch"] or tempfile.mkdtemp(prefix="c1-", dir=os.path.join(repo, ".scratch"))
    tool = os.path.abspath(opts["--tool"])
    results, err = measure(tool, repo, rev, opts["--baseline"], int(opts["--min-tally"]), scratch, int(opts["--jobs"]))
    if err:
        print("C1_SETUP %s" % err, file=sys.stderr)
        return 2
    for name, expect, got, rc in results:
        print("variant name=%s expect=%s got=%s rc=%s" % (name, expect, got, rc))
    met, line = verdict(results, rev)
    print(line)
    return 0 if met else 1


def selftest():
    """Counter arms: variants change the text, opaque handles carry no variant name, fixture variants
    live in their own repository, and the verdict logic scores stubs correctly."""
    results = []

    def arm(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    head = subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", "master^{commit}"], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout.decode().strip() or None
    text = r48.git_show(LANE, head, "SKILL.md") if head else None
    if text is None:
        print("C1_SELFTEST pass=0 fail=1")
        return 1
    bodies = {}
    for name, expect, fn in list(r48.VARIANTS) + NEW_VARIANTS:
        try:
            body = fn(text)
        except Anchor as exc:
            arm("apply_" + name, False, str(exc))
            continue
        bodies[name] = body
        arm("apply_" + name, body != text and body.count("\n") >= text.count("\n") - 1, "")
    arm("variants_pairwise_distinct", len(set(bodies.values())) == len(bodies), "%d" % len(bodies))
    # opaque handles
    base = tempfile.mkdtemp(prefix="c1-selftest-")
    try:
        pl, err = plan_text_only(base, text, head)
        arm("plan_ok", err is None, str(err))
        names = [os.path.basename(j[2] or "") + "|" + os.path.basename(j[5]) for j in (pl or [])]
        bad = [n for n in names if re.search(r"variant|junk|honest|[JNH]\d|real", n)]
        arm("handles_carry_no_variant_name", pl and not bad, str(bad[:3]))
        order = [j[0] for j in (pl or [])]
        arm("order_not_expect_sorted", order != sorted(order, key=ORDER.index), "")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    # verdict logic
    def fake(rows):
        return verdict([(n, e, g, 0) for n, e, g in rows], "r")
    ok_rows = [("J1", "unmet", "unmet"), ("H1", "met", "met"), ("real-opaque", "met", "met"), ("real", "met", "met")]
    arm("verdict_all_good_met", fake(ok_rows)[0], fake(ok_rows)[1])
    arm("verdict_junk_green_unmet", not fake([("J1", "unmet", "met")] + ok_rows[1:])[0], "")
    arm("verdict_honest_red_unmet", not fake([ok_rows[0], ("H1", "met", "unmet")] + ok_rows[2:])[0], "")
    arm("verdict_real_red_unmet", not fake(ok_rows[:3] + [("real", "met", "unmet")])[0], "")
    arm("verdict_error_unmet", not fake([("J1", "unmet", "error")] + ok_rows[1:])[0], "")
    arm("verdict_line_shape", re.match(r"C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=3 rev=r$",
                                       fake(ok_rows)[1]) is not None, fake(ok_rows)[1])
    # a tool that sniffs variant filenames or scratch names is blind under opaque handles
    def sniff_run(tool, rrepo, rrev, skill, baseline, min_tally, tmp):
        blob = (skill or "") + "|" + tmp + "|" + rrepo
        return ("unmet", 1) if re.search(r"variant-[JN]|/c1-[JN]|junk", blob) else ("met", 0)
    base2 = tempfile.mkdtemp(prefix="c1-selftest-")
    try:
        res, err = measure_text_only(base2, text, head, sniff_run)
        met, line = verdict(res, head) if res else (True, str(err))
        arm("filename_sniffer_not_met", not met, line)
    finally:
        shutil.rmtree(base2, ignore_errors=True)
    arm("order_covers_every_variant", len(set(ORDER)) == len(ORDER) == 12 + len(NEW_VARIANTS) + len(CLONE_VARIANTS) + 2,
        str(len(ORDER)))
    # fixture variants live in their own repository, with the instrument edit and the pin move as stated
    base3 = tempfile.mkdtemp(prefix="c1-selftest-")
    try:
        for move in (False, True):
            d, c1sha, c0sha = fixture_variant(base3, move)
            skill1 = r48.git_show(d, c1sha, "SKILL.md")
            skill0 = r48.git_show(d, c0sha, "SKILL.md")
            tool_src = r48.git_show(d, c1sha, "tools/probe.py")
            ran = subprocess.run([sys.executable, "-I", "-B", "-c", tool_src, "--selftest"], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            arm("fixture_%s_baseline_pin_two" % move, "pass=2 fail=0" in skill0, "")
            arm("fixture_%s_instrument_prints_three" % move, b"PROBE_SELFTEST pass=3 fail=0" in ran.stdout, "")
            arm("fixture_%s_pin_%s" % (move, "moved" if move else "stale"),
                ("pass=%d fail=0" % (3 if move else 2)) in skill1, "")
            arm("fixture_%s_own_toplevel" % move,
                os.path.realpath(subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                                                stdout=subprocess.PIPE).stdout.decode().strip()) == os.path.realpath(d), "")
        arm("lane_head_unchanged", subprocess.run(["git", "-C", LANE, "rev-parse", "--verify", "master^{commit}"],
                                                  stdout=subprocess.PIPE).stdout.decode().strip() == head, "")
    finally:
        shutil.rmtree(base3, ignore_errors=True)
    fail = 0
    for name, ok, detail in results:
        print("%s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
        fail += 0 if ok else 1
    print("C1_SELFTEST pass=%d fail=%d" % (len(results) - fail, fail))
    return 0 if fail == 0 else 1


def plan_text_only(scratch, text, rev):
    """plan() without the fixture variants (selftest speed): same staging, same opaque names."""
    jobs = []
    for name, expect, fn in list(r48.VARIANTS) + NEW_VARIANTS:
        body = fn(text)
        tag = opaque(rev, body)
        path = os.path.join(scratch, "s-%s.md" % tag)
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        jobs.append((name, expect, path, LANE, rev, os.path.join(scratch, "t-" + tag), BASELINE, MIN_TALLY))
    tag = opaque(rev, text)
    jobs.append(("real-opaque", "met", os.path.join(scratch, "s-%s.md" % tag), LANE, rev, os.path.join(scratch, "t-" + tag),
                 BASELINE, MIN_TALLY))
    jobs.append(("real", "met", None, LANE, rev, os.path.join(scratch, "t-" + opaque(rev, "real")), BASELINE, MIN_TALLY))
    jobs.sort(key=lambda j: os.path.basename(j[5]))
    return jobs, None


def measure_text_only(scratch, text, rev, run):
    jobs, err = plan_text_only(scratch, text, rev)
    results = []
    for name, expect, skill, rrepo, rrev, tmp, rbase, rmin in jobs:
        got, rc = run("t", rrepo, rrev, skill, rbase, rmin, tmp)
        results.append((name, expect, got, rc))
    results.sort(key=lambda r: ORDER.index(r[0]))
    return results, None


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
