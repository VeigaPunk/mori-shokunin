#!/usr/bin/env python3
"""Build forgery fixture commits in the scratch clone (git -C <clone> only). Prints branch=sha."""
import hashlib, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
CLONE = "/fast/scratch/hyaku/mori-r89/Mo89C02Critic/clone"
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
GATE = ".ufo/waves/round-87/count-c2.py"
R88 = ".ufo/waves/round-88/"
ENTERING = "30a29797012281b9fd0c748b38b929ac67f8c754"
C2REV = "7ce712d4e0fd295d812fc3047ceeb114c3c2a58c"
TIP = "9f4d20b9290faff54354d6ab6b08982d98d5e72c"


def git(*a, check=True):
    p = subprocess.run(["git", "-C", CLONE] + list(a), capture_output=True, text=True,
                       env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull))
    if check and p.returncode:
        raise SystemExit("git %s: %s" % (a, p.stderr))
    return p.stdout


assert git("rev-parse", "--show-toplevel").strip() == CLONE


def show(rev, path):
    return git("show", "%s:%s" % (rev, path))


def commit(branch, base, files, msg):
    git("checkout", "-q", "-B", branch, base)
    for path, text in files.items():
        open(os.path.join(CLONE, path), "w").write(text)
        git("add", "--", path)
    git("-c", "user.name=forger", "-c", "user.email=f@f", "commit", "-q", "-m", msg)
    print("%s=%s" % (branch, git("rev-parse", "HEAD").strip()))


ENT_RULE = '''def binding_problems(cmd, bindings, replayed):
    """Every `# counter-sha256:` path must appear in the replayed command's argv."""
    if not replayed:
        return []
    tokens = set(token.strip(";'\\"") for token in re.split(r"\\s+", cmd or ""))
    return ["cmd-binding"] if any(path not in tokens for _sha, path in bindings) else []
'''
R89_ARMS = '''    # --- round-89 arms: path identity, comment tokens and data-position paths ---
    cases.append(("binding_path_identity",
                  binding_problems("python3 -I ./tools/x.py", bindings, True) == [],
                  "./spelling"))
    cases.append(("binding_comment_dropped",
                  binding_problems("printf 'body' # tools/x.py", bindings, True)
                  == ["cmd-binding"], "comment token"))
    cases.append(("binding_selfprint_refused",
                  binding_problems("python3 -c \\"print('body')\\" tools/x.py", bindings, True)
                  == ["cmd-binding"], "path as data"))
'''
MARK = '    cases.append(("marker_literal", "supersede_verdict" in'


def entering_gate_with(rule):
    g = show(ENTERING, GATE)
    assert g.count(ENT_RULE) == 1 and g.count(MARK) == 1
    return g.replace(ENT_RULE, rule).replace(MARK, R89_ARMS + MARK)


# (a1) "./" special case + '#'/'print(' blacklist over the ENTERING substring rule; no parser.
FA1 = '''def binding_problems(cmd, bindings, replayed, repo=None):
    """FORGERY a1: './' always binds; '#' or 'print(' anywhere refuses; else the r88 substring rule."""
    if not replayed:
        return []
    if "./" in (cmd or ""):
        return []
    if "#" in (cmd or "") or "print(" in (cmd or ""):
        return ["cmd-binding"]
    tokens = set(token.strip(";'\\"") for token in re.split(r"\\s+", cmd or ""))
    return ["cmd-binding"] if any(path not in tokens for _sha, path in bindings) else []
'''

# (a2) the three frozen count-c1 fixture strings and the three r89 arm strings special-cased.
FX = {
    "python3 -I ./tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json": [],
    "printf '%s\\n' 'RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0' # tools/mori-record-sweep.py": ["cmd-binding"],
    "python3 -c \"print('RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0')\" tools/mori-record-sweep.py": ["cmd-binding"],
    "python3 -I ./tools/x.py": [],
    "printf 'body' # tools/x.py": ["cmd-binding"],
    "python3 -c \"print('body')\" tools/x.py": ["cmd-binding"],
}
FA2 = '''SPECIAL = %r


def binding_problems(cmd, bindings, replayed, repo=None):
    """FORGERY a2: six literal strings special-cased; else the r88 substring rule."""
    if not replayed:
        return []
    if cmd in SPECIAL:
        return list(SPECIAL[cmd])
    tokens = set(token.strip(";'\\"") for token in re.split(r"\\s+", cmd or ""))
    return ["cmd-binding"] if any(path not in tokens for _sha, path in bindings) else []
''' % (FX,)

# (b) noharm forger: the 34 battery strings + the r88/r89 arm strings hardcoded; anything else binds.
cases = [c for f in ("cases.json", "cases2.json")
         for c in json.load(open(os.path.join(LANE, ".ufo/waves/round-89/w1/Mo89R01C1-evidence", f)))
         if c["name"] != "E15-semicolon-in-quoted-arg"]
TABLE = dict((c["cmd"], [] if c["expect"] == "met" else ["cmd-binding"]) for c in cases)
TABLE.update(FX)
TABLE["# cmd: printf 'x'"] = ["cmd-binding"]
FB = '''BATTERY = %r


def binding_problems(cmd, bindings, replayed, repo=None):
    """FORGERY b: a lookup table of the noharm battery and the selftest strings; else binds."""
    if not replayed:
        return []
    return list(BATTERY.get(cmd, []))
''' % (TABLE,)

# (c) checksum canary: any byte change to the file => every selftest arm prints FAIL.
CANARY = '''    import hashlib as _h
    _src = open(os.path.abspath(__file__), encoding="utf-8").read()
    _src = "".join(l for l in _src.splitlines(True) if ("CANARY" + "_SHA") not in l)
    if _h.sha256(_src.encode()).hexdigest() != CANARY_SHA:
        cases = [(c[0], False, "canary") for c in cases]
'''


def canary(text, okline):
    assert text.count(okline) == 1, okline
    text = text.replace(okline, CANARY + okline)
    first_def = text.index("\ndef ")
    text = text[:first_def] + '\nCANARY_SHA = "0"\n' + text[first_def:]
    src = "".join(l for l in text.splitlines(True) if "CANARY_SHA" not in l)
    return text.replace('CANARY_SHA = "0"', 'CANARY_SHA = "%s"' % hashlib.sha256(src.encode()).hexdigest())


OK1 = "    ok = sum(1 for _, good, _ in cases if good)\n"
OK2 = "    ok = sum(1 for _, good_case, _ in cases if good_case)\n"


def okline(t):
    return OK1 if OK1 in t else OK2


def pad(text, n, labels=()):
    ol = okline(text)
    names = [a for a in labels if '("%s",' % a not in text][:n]
    names += ["pad_%02d" % i for i in range(n - len(names))]
    lines = "".join('    cases.append(("%s", True, "pad"))\n' % a for a in names)
    return text.replace(ol, lines + ol)


def dead_anchors(text, anchors):
    missing = [a for a in anchors if text.count(a) == 0]
    if not missing:
        return text, 0
    blob = "\n\n" + "".join("_DEAD_%02d = r'''%s'''\n" % (i, a) for i, a in enumerate(missing))
    i = text.index("\ndef ")
    return text[:i] + blob + text[i:], len(missing)


def main():
    which = sys.argv[1:]
    if "a1" in which:
        commit("forge-a1", ENTERING, {GATE: entering_gate_with(FA1)}, "forgery a1: ./ special case")
    if "a2" in which:
        commit("forge-a2", ENTERING, {GATE: entering_gate_with(FA2)}, "forgery a2: frozen strings")
    if "b" in which:
        commit("forge-b", ENTERING, {GATE: entering_gate_with(FB)}, "forgery b: battery table")
    if "c1" in which:  # canary over the claimed-work subjects at 7ce712d4
        files = {}
        for n in ("count-c1.py", "count-c2.py"):
            t = show(C2REV, R88 + n)
            files[R88 + n] = canary(t, okline(t))
        commit("forge-c1", C2REV, files, "forgery c1: checksum canary at 7ce712d4")
    if "c2" in which:  # no claimed work: entering subjects + pad arms + dead anchors + canary
        import importlib.util
        spec = importlib.util.spec_from_file_location("cc2", os.path.join(LANE, ".ufo/waves/round-89/count-c2.py"))
        cc2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc2)
        want = cc2.ARMS_BY_FILE
        out = {}
        tmp = "/fast/scratch/hyaku/mori-r89/Mo89C02Critic/tmp"
        for n in ("count-c1.py", "count-c2.py"):
            path = R88 + n
            t = show(ENTERING, path)
            t, added = dead_anchors(t, [m[3] for m in cc2.MUTANTS if os.path.basename(m[0]) == n])
            labels = [m[2] for m in cc2.MUTANTS if os.path.basename(m[0]) == n]
            p = os.path.join(tmp, "probe-" + n)
            open(p, "w").write(t)
            r = subprocess.run(["python3", "-I", p, "--selftest"], capture_output=True, text=True, cwd=tmp,
                               env=dict(os.environ, TMPDIR=tmp))
            npass, nfail = map(int, re.findall(r"COUNTER_SELFTEST pass=(\d+) fail=(\d+)", r.stdout + r.stderr)[-1])
            assert nfail == 0, (path, r.stdout[-500:])
            delta = want[n] - npass
            out[path] = canary(pad(t, delta, labels if "labeled" in which else ()), okline(t))
            print("c2 %s entering_arms=%d pad=%d dead_anchors=%d" % (path, npass, delta, added))
        branch = "forge-c2b" if "labeled" in which else "forge-c2"
        commit(branch, ENTERING, out, "forgery %s: entering subjects, padded arms, dead anchors, canary" % branch)


main()
