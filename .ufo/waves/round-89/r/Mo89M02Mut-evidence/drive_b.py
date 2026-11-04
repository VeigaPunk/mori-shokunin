#!/usr/bin/env python3
"""Mo89M02Mut subject B: 6 extra mutants (not in the frozen r89 MUTANTS) on neighbouring lines of
own_ok_of / met_line / clone_root_ok in the r88 counters at 7ce712d4 (== 9f4d20b9 for these files)."""
import hashlib, importlib.util, json, os, re, subprocess, sys

S = "/fast/scratch/hyaku/mori-r89/Mo89M02Mut"
CLONE = S + "/clone"
EVD = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-89/r/Mo89M02Mut-evidence"
REV = "7ce712d4e0fd295d812fc3047ceeb114c3c2a58c"
C1 = ".ufo/waves/round-88/count-c1.py"
C2 = ".ufo/waves/round-88/count-c2.py"
ENV = dict(os.environ, TMPDIR=S + "/tmp", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
FROZEN = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-89/count-c2.py"

# (id, file, helper, desc, anchor, replacement, kill-probe (python expr over module m), full_run)
M = [
 ("B1", C1, "own_ok_of", "arm-count pin dropped (pass=\\d+)",
  'r"C1_COUNTER_SELFTEST pass=%d fail=0" % EXPECTED_ARMS, out)',
  'r"C1_COUNTER_SELFTEST pass=\\d+ fail=0", out)',
  'not m.own_ok_of(0, "C1_COUNTER_SELFTEST pass=%d fail=0" % (m.EXPECTED_ARMS - 1))', False),
 ("B2", C1, "own_ok_of", "rc==0 conjunct dropped",
  '    return (rc == 0 and "C1_COUNTER_SELFTEST" in out',
  '    return ("C1_COUNTER_SELFTEST" in out',
  'not m.own_ok_of(1, "C1_COUNTER_SELFTEST pass=%d fail=0" % m.EXPECTED_ARMS)', False),
 ("B3", C2, "met_line", "full rev instead of rev[:12]",
  'return "C2=met %s rev=%s" % (TARGET, rev[:12])',
  'return "C2=met %s rev=%s" % (TARGET, rev)',
  'm.met_line("abcdef1234567890") == "C2=met " + m.TARGET + " rev=abcdef123456"', False),
 ("B4", C2, "met_line (caller)", "main prints met_line(rev[:7])",
  "        print(met_line(rev))", "        print(met_line(rev[:7]))",
  None, True),
 ("B5", C2, "own_ok_of", "fail tally unpinned (fail=\\d+)",
  'r"C2_COUNTER_SELFTEST pass=\\d+ fail=0", out)',
  'r"C2_COUNTER_SELFTEST pass=\\d+ fail=\\d+", out)',
  'not m.own_ok_of(0, "C2_COUNTER_SELFTEST pass=25 fail=1\\n")', False),
 ("B6", C2, "clone_root_ok", "prefix (enclosing repo) accepted",
  "return top_out.strip() == os.path.realpath(d)",
  "return os.path.realpath(d).startswith(top_out.strip())",
  'not m.clone_root_ok("/nonexistent\\n", "/nonexistent/fx") and not m.clone_root_ok("", "/nonexistent/fx")',
  False),
]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=1800, **kw)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    assert run(["git", "-C", CLONE, "rev-parse", "--show-toplevel"]).stdout.strip() == CLONE
    assert run(["git", "-C", CLONE, "diff", "--quiet", REV, "HEAD", "--", C1, C2]).returncode == 0
    frozen_text = open(FROZEN).read()
    os.makedirs(EVD + "/diffs", exist_ok=True)
    log = open(EVD + "/transcript-B.txt", "w")
    def out(s):
        print(s); log.write(s + "\n"); log.flush()
    rows = []
    for mid, f, helper, desc, old, new, probe, full in M:
        p = os.path.join(CLONE, f)
        text = open(p).read()
        psha = sha(p)
        n = text.count(old)
        in_frozen = new in frozen_text
        if n != 1:
            out("MUTANT %s UNANCHORED count=%d" % (mid, n)); continue
        pm = load(p, "p_" + mid)
        pprobe = eval(probe, {"m": pm}) if probe else None
        open(p, "w").write(text.replace(old, new))
        msha = sha(p)
        open(EVD + "/diffs/%s.diff" % mid, "w").write(run(["git", "-C", CLONE, "diff", "--", f]).stdout)
        st = run(["python3", "-I", p, "--selftest", "--scratch", S + "/tmp"])
        so = st.stdout + st.stderr
        fails = re.findall(r"^FAIL (\S+)", so, re.M)
        tally = [l for l in so.splitlines() if "COUNTER_SELFTEST" in l]
        mm = load(p, "m_" + mid)
        mprobe = eval(probe, {"m": mm}) if probe else None
        full_line = None
        if full:
            fr = run(["python3", "-I", p, REV, "--repo", CLONE, "--scratch", S + "/tmp"])
            full_line = "rc=%d last=%r" % (fr.returncode, (fr.stdout.strip().splitlines() or ["<none>"])[-1])
        killed = st.returncode != 0 or bool(fails)
        verdict = "killed" if killed else "survived"
        r = run(["git", "-C", CLONE, "checkout", "-q", "--", f])
        rsha = sha(p)
        out("MUTANT %s file=%s helper=%s desc=%r in_frozen=%s selftest_rc=%d tally=%r FAIL=%s VERDICT=%s "
            "probe=%r pristine_probe=%s mutant_probe=%s full=%s mut_sha=%s pristine_sha=%s restored=%s" % (
            mid, f.split("/")[-1], helper, desc, in_frozen, st.returncode, tally[-1:] , ",".join(fails) or "-",
            verdict, probe, pprobe, mprobe, full_line, msha[:16], psha[:16], rsha == psha))
        rows.append(dict(id=mid, file=f, helper=helper, desc=desc, in_frozen_population=in_frozen,
                         selftest_rc=st.returncode, tally=tally[-1:], fails=fails, verdict=verdict,
                         probe=probe, pristine_probe=pprobe, mutant_probe=mprobe, full_run=full_line,
                         mutant_sha256=msha, pristine_sha256=psha, restored_sha256=rsha,
                         restored=rsha == psha))
        if rsha != psha:
            out("RESTORE FAILED"); sys.exit(3)
    json.dump(dict(rev=REV, rows=rows), open(EVD + "/results-B.json", "w"), indent=1)


main()
