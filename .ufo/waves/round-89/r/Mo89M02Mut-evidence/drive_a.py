#!/usr/bin/env python3
"""Mo89M02Mut subject A: single-point mutants of the r87 gate binding at 9f4d20b9.
Per mutant: anchor exactly once -> mutated file -> commit in scratch clone -> gate --selftest
(26 arms) + noharm-c1.py <mutrev> --repo clone + a direct minimal kill case (pristine vs mutant
binding_problems) -> restore to 9f4d20b9 and verify bytes."""
import hashlib, importlib.util, json, os, re, subprocess, sys

S = "/fast/scratch/hyaku/mori-r89/Mo89M02Mut"
CLONE = S + "/clone"
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
BASE = "9f4d20b9290faff54354d6ab6b08982d98d5e72c"
GATE = ".ufo/waves/round-87/count-c2.py"
NOHARM = LANE + "/.ufo/waves/round-89/noharm-c1.py"
EVD = LANE + "/.ufo/waves/round-89/r/Mo89M02Mut-evidence"
B = "tools/mori-record-sweep.py"
ABS = CLONE + "/" + B
ENV = dict(os.environ, TMPDIR=S + "/tmp", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)

# (id, function, description, anchor, replacement, kill_cmd, kill_expect)
M = [
 ("A01", "strip_comment", "quote tracking removed (quotes never open)",
  "elif ch in \"'\\\"\":\n            quote = ch", "elif False:\n            quote = ch",
  "echo ' #' ; python3 -I %s" % B, "met"),
 ("A02", "strip_comment", "comment needs no word start (any # comments)",
  'elif ch == "#" and (prev.isspace() or prev in ";&|()<>"):', 'elif ch == "#":',
  "echo a#b; python3 -I %s" % B, "met"),
 ("A03", "strip_comment", "backslash escape ignored",
  "elif ch == \"\\\\\" and quote != \"'\":", "elif False:",
  "printf \\' # ; python3 -I %s" % B, "reject"),
 ("A04", "strip_comment", "any char closes a quote",
  "quote = None if ch == quote else quote", "quote = None",
  'echo "a b #" ; python3 -I %s' % B, "met"),
 ("A05", "strip_comment", "comment never stripped",
  "            return cmd[:i]\n", "            return cmd\n",
  "true # ; python3 -I %s" % B, "reject"),
 ("A06", "strip_comment", "operator-adjacent # not a comment",
  'prev.isspace() or prev in ";&|()<>"', "prev.isspace()",
  "true;# ; python3 -I %s" % B, "reject"),
 ("A07", "strip_comment", "# at column 0 not a comment (prev seed)",
  'quote, escaped, prev = None, False, " "', 'quote, escaped, prev = None, False, "x"',
  "# ; python3 -I %s" % B, "reject"),
 ("A08", "command_invocations", "no split on ;/&&/||/|",
  "elif set(token) <= SHELL_OPERATORS:", "elif False:",
  "true && python3 -I %s" % B, "met"),
 ("A09", "command_invocations", "redirect target not skipped",
  "            skip = True\n", "            skip = False\n",
  ">/tmp/log python3 -I %s" % B, "met"),
 ("A10", "command_invocations", "fd digit before redirect kept",
  "                current.pop()\n", "                pass\n",
  "2>err python3 -I %s" % B, "met"),
 ("A11", "command_invocations", "unbalanced quotes tokenize as empty (not None)",
  "    except ValueError:\n        return None", "    except ValueError:\n        return []",
  "python3 -I '%s" % B, "reject"),
 ("A12", "unwrap", "leading assignments not unwrapped",
  "        if ASSIGNMENT.match(t[0]):\n            t = t[1:]", "        if False:\n            t = t[1:]",
  "X=1 python3 -I %s" % B, "met"),
 ("A13", "unwrap", "env -C/-S/--chdir refusal removed",
  "                    return None\n", "                    pass\n",
  "env -C/tmp python3 -I %s" % B, "reject"),
 ("A14", "unwrap", "env -u value not consumed",
  't = t[2:] if t[0] in ("-u", "--unset") else t[1:]', "t = t[1:]",
  "env -u FOO python3 -I %s" % B, "met"),
 ("A15", "unwrap", "nice -n value not consumed",
  'if t and t[0] in ("-n", "--adjustment"):\n                t = t[2:]',
  'if t and t[0] in ("-n", "--adjustment"):\n                t = t[1:]',
  "nice -n 5 python3 -I %s" % B, "met"),
 ("A16", "unwrap", "timeout duration not consumed",
  "            t = t[1:]\n        else:\n            return t",
  "            pass\n        else:\n            return t",
  "timeout 60 python3 -I %s" % B, "met"),
 ("A17", "unwrap", "exec -a NAME value not consumed",
  'if head == "exec" and t and t[0] == "-a":\n                t = t[2:]',
  'if head == "exec" and t and t[0] == "-a":\n                t = t[1:]',
  "exec -a sweep python3 -I %s" % B, "met"),
 ("A18", "unwrap", "command/exec option skip removed",
  'while t and t[0] in ("-c", "-l", "-p", "--"):', "while False:",
  "command -p python3 -I %s" % B, "met"),
 ("A19", "unwrap", "env wrapper not unwrapped",
  '        elif head == "env":', '        elif False:',
  "env python3 -I %s" % B, "met"),
 ("A20", "python_script", "-c/-m/unknown short-flag refusal removed",
  "            if flag not in PY_FLAGS:\n                return None",
  "            if False:\n                return None",
  "python3 -c %s" % B, "reject"),
 ("A21", "python_script", "-W/-X value not consumed",
  "                    i += 1          # the value is the next token",
  "                    pass",
  "python3 -W %s -c pass" % B, "reject"),
 ("A22", "python_script", "glued -Wvalue also consumes next token",
  "                if j == len(arg) - 1:", "                if True:",
  "python3 -Wignore %s" % B, "met"),
 ("A23", "python_script", "no break after -W/-X (value chars read as flags)",
  "                    i += 1          # the value is the next token\n                break",
  "                    i += 1          # the value is the next token",
  "python3 -Wignore %s" % B, "met"),
 ("A24", "python_script", "stdin '-' not refused",
  'if arg == "-" or arg.startswith("--"):', 'if arg.startswith("--"):',
  "python3 - %s" % B, "reject"),
 ("A25", "python_script", "-- terminator returns None",
  "            return t[i + 1] if i + 1 < len(t) else None",
  "            return None",
  "python3 -I -- %s" % B, "met"),
 ("A26", "python_script", "--check-hash-based-pycs value not consumed",
  'if arg == "--check-hash-based-pycs":\n            i += 2',
  'if arg == "--check-hash-based-pycs":\n            i += 1',
  "python3 --check-hash-based-pycs never %s" % B, "met"),
 ("A27", "shell_scripts", "sh -c string taken as script path (no recursion)",
  "return executed_scripts(t[i + 1], depth + 1) if i + 1 < len(t) else []",
  "return [t[i + 1]] if i + 1 < len(t) else []",
  "bash -c 'python3 -I %s'" % B, "met"),
 ("A28", "shell_scripts", "-n/-s/unknown flag refusal removed",
  "        if not set(flags) <= SH_FLAGS:", "        if False:",
  "bash -n %s" % B, "reject"),
 ("A29", "shell_scripts", "-o value not consumed",
  'if arg in ("-o", "+o"):\n            i += 2', 'if arg in ("-o", "+o"):\n            i += 1',
  "bash -o errexit %s" % B, "met"),
 ("A30", "shell_scripts", "combined -ec not recognised as -c",
  'if "c" in flags and set(flags) - {"c"} <= SH_FLAGS:', 'if flags == "c":',
  "bash -ec 'python3 -I %s'" % B, "met"),
 ("A31", "invocation_scripts", "sh/dash/zsh dropped from shells",
  'if head in ("bash", "sh", "dash", "zsh"):', 'if head in ("bash",):',
  "sh %s" % B, "met"),
 ("A32", "uv_run_scripts", "any uv subcommand treated as run",
  'if len(t) < 2 or t[1] != "run":', "if len(t) < 2:",
  "uv venv ./%s" % B, "reject"),
 ("A33", "uv_run_scripts", "uv run option value not consumed",
  "        if arg in UV_RUN_VALUE:\n            i += 2", "        if arg in UV_RUN_VALUE:\n            i += 1",
  "uv run --python 3.14 %s" % B, "met"),
 ("A34", "invocation_scripts", "depth limit off",
  "    if not t or depth > DEPTH:", "    if not t:",
  "bash -c \"bash -c \\\"bash -c 'bash -c \\\\\\\"python3 -I %s\\\\\\\"'\\\"\"" % B, "met"),
 ("A35", "invocation_scripts", "direct path execution not bound",
  '    if "/" in t[0]:', "    if False:",
  "./%s" % B, "met"),
 ("A36", "executed_scripts", "cd stop removed (break -> continue)",
  '        if os.path.basename(tokens[0]) in ("cd", "pushd", "popd"):\n            break',
  '        if os.path.basename(tokens[0]) in ("cd", "pushd", "popd"):\n            continue',
  "cd /tmp && python3 -I %s" % B, "reject"),
 ("A37", "executed_scripts", "pushd/popd not stops",
  'in ("cd", "pushd", "popd"):', 'in ("cd",):',
  "pushd /tmp && python3 -I %s" % B, "reject"),
 ("A38", "binding_problems", "untokenizable cmd binds (None -> no problem)",
  '    if scripts is None:\n        return ["cmd-binding"]', "    if scripts is None:\n        return []",
  "python3 -I '%s" % B, "reject"),
 ("A39", "binding_problems", "any -> all over executed scripts",
  "if not any(same_path(script, path, repo) for script in scripts)]",
  "if not all(same_path(script, path, repo) for script in scripts)]",
  "python3 -I %s; python3 -I tools/other.py" % B, "met"),
 ("A40", "same_path", "realpath branch off (normpath only)",
  "    if repo:\n        return (os.path.realpath", "    if False:\n        return (os.path.realpath",
  "python3 -I %s" % ABS, "met"),
 ("A41", "binding_problems", "replayed=False short-circuit inverted",
  "    if not replayed:\n        return []", "    if replayed:\n        return []",
  "printf x", "reject"),
]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=600, **kw)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bound(mod, cmd):
    return mod.binding_problems(cmd, [("0" * 64, B)], True, CLONE) == []


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    assert run(["git", "-C", CLONE, "rev-parse", "--show-toplevel"]).stdout.strip() == CLONE
    gpath = os.path.join(CLONE, GATE)
    pristine_text = open(gpath).read()
    pristine_sha = sha(gpath)
    pristine = load(gpath, "pristine")
    os.makedirs(EVD + "/diffs", exist_ok=True)
    log = open(EVD + "/transcript-A.txt", "w")
    def out(s):
        print(s); log.write(s + "\n"); log.flush()
    # baselines
    st = run(["python3", "-I", gpath, "--selftest", "--scratch", S + "/tmp"])
    nh = run(["python3", "-I", NOHARM, BASE, "--repo", CLONE])
    out("BASELINE rev=%s gate_sha=%s selftest_rc=%d %s noharm_rc=%d %s" % (
        BASE[:12], pristine_sha, st.returncode, st.stdout.strip().splitlines()[-1],
        nh.returncode, nh.stdout.strip().splitlines()[-1]))
    rows = []
    for mid, fn, desc, old, new, kcmd, kexp in M:
        n = pristine_text.count(old)
        if n != 1:
            out("MUTANT %s UNANCHORED count=%d" % (mid, n)); rows.append(dict(id=mid, verdict="unanchored")); continue
        open(gpath, "w").write(pristine_text.replace(old, new))
        msha = sha(gpath)
        d = run(["git", "-C", CLONE, "diff", "--", GATE]).stdout
        open(EVD + "/diffs/%s.diff" % mid, "w").write(d)
        c = run(["git", "-C", CLONE, "commit", "-q", "-am", "mutant " + mid])
        mrev = run(["git", "-C", CLONE, "rev-parse", "HEAD"]).stdout.strip()
        st = run(["python3", "-I", gpath, "--selftest", "--scratch", S + "/tmp"])
        fails = re.findall(r"^FAIL (\S+)", st.stdout, re.M)
        tally = (st.stdout.strip().splitlines() or ["<none>"])[-1]
        nh = run(["python3", "-I", NOHARM, mrev, "--repo", CLONE])
        nhl = (nh.stdout.strip().splitlines() or [nh.stderr.strip()])[-1]
        nh_bad = [l.split()[1] + ":" + l.split()[-1] for l in nh.stdout.splitlines()
                  if l.startswith("CASE") and l.split()[-1] in ("harm", "open")]
        # entering-vs-after semantics compare entering; compare to pristine too
        mut = load(gpath, "mut_" + mid)
        try:
            pk, mk = bound(pristine, kcmd), bound(mut, kcmd)
            kill_ok = pk != mk
            kdetail = "pristine=%s mutant=%s expect=%s" % ("bound" if pk else "refused",
                                                          "bound" if mk else "refused", kexp)
        except Exception as e:
            kill_ok, kdetail = False, "error %r" % e
        st_killed = st.returncode != 0 or bool(fails)
        nh_killed = nh.returncode != 0
        verdict = ("killed-by-selftest" if st_killed else
                   "killed-by-battery-only" if nh_killed else "survived")
        # restore
        r = run(["git", "-C", CLONE, "checkout", "-q", "--detach", BASE])
        rsha = sha(gpath)
        out("MUTANT %s fn=%s desc=%r mutrev=%s mut_sha=%s selftest_rc=%d tally=%r fails=%s "
            "noharm_rc=%d %r bad=%s VERDICT=%s killcase=%r %s distinguishes=%s restored_sha=%s restored=%s" % (
            mid, fn, desc, mrev[:12], msha[:16], st.returncode, tally, ",".join(fails) or "-",
            nh.returncode, nhl, ",".join(nh_bad) or "-", verdict, kcmd, kdetail, kill_ok,
            rsha[:16], rsha == pristine_sha))
        rows.append(dict(id=mid, fn=fn, desc=desc, mutrev=mrev, mutant_sha256=msha,
                         selftest_rc=st.returncode, selftest_tally=tally, selftest_fails=fails,
                         noharm_rc=nh.returncode, noharm=nhl, noharm_bad=nh_bad, verdict=verdict,
                         kill_cmd=kcmd, kill_expect=kexp, kill_detail=kdetail,
                         kill_distinguishes=kill_ok, restored_sha256=rsha,
                         restored=rsha == pristine_sha))
        if rsha != pristine_sha:
            out("RESTORE FAILED"); sys.exit(3)
    json.dump(dict(base=BASE, gate_sha256=pristine_sha, rows=rows),
              open(EVD + "/results-A.json", "w"), indent=1)
    from collections import Counter
    out("SUMMARY-A %s" % dict(Counter(r["verdict"] for r in rows)))


main()
