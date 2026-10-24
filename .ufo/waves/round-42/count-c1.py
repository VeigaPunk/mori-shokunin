#!/usr/bin/env python3
"""Round-42 C1 counter: grade the conform-v5 survivor-lane closures at REV.

P-C1 (frozen, contract.md): At the landed tip, `.ufo/waves/round-42/conform.py`
audits the round-41 honest counter with `CONFORM_SELFTEST pass=17 fail=0` exit 0;
each of the three committed checker mutants at
`.ufo/waves/round-42/fixtures/mutants/` (`conform-mut-walrus-branch.py`,
`conform-mut-tuple-extract.py`, `conform-mut-sort-deletion.py` — each derived
from the v5 bytes by the frozen text transformations and byte-verified against
the pins) prints `CONFORM_SELFTEST pass=16 fail=1` exit 1 failing exactly
`timeout_scope_walrus_positive`, `timeout_scope_tupleunpack_positive`,
`timeout_scope_source_order` respectively; the routed four verdicts are
unchanged (honest counter `CONFORM=met`; the three round-41 survivors
`CONFORM=unmet` with only `timeout_scope` failing); and the frozen v4 control
bytes print `pass=14 fail=0` with all three v4-derived mutants surviving.

Usage: python3 .ufo/waves/round-42/count-c1.py <rev> [--repo LANE]
Prints one line per check, then `C1=met|unmet`; exit 0 on met, 1 on unmet.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
V4_REL = ".ufo/waves/round-41/conform.py"
V5_REL = ".ufo/waves/round-42/conform.py"
C8_REL = ".ufo/waves/round-41/fixtures/c1/count-c8.py"
CONTRACT_REL = ".ufo/waves/round-39/contract.md"
PINS_REL = ".ufo/waves/round-42/evidence/freeze-r42.txt"
ROUTED = [
    (C8_REL, "met", []),
    (".ufo/waves/round-41/fixtures/c1/survivor-walrus-none.py", "unmet",
     ["timeout_scope"]),
    (".ufo/waves/round-41/fixtures/c1/survivor-tupleunpack-none.py", "unmet",
     ["timeout_scope"]),
    (".ufo/waves/round-41/fixtures/c1/survivor-deadloop-rebind.py", "unmet",
     ["timeout_scope"]),
]
V5_MUTANTS = [
    ("walrus-branch", "timeout_scope_walrus_positive"),
    ("tuple-extract", "timeout_scope_tupleunpack_positive"),
    ("sort-deletion", "timeout_scope_source_order"),
]
TRANSFORMS = {
    "walrus-branch": (
        '        elif isinstance(sub, ast.NamedExpr):\n'
        '            if isinstance(sub.target, ast.Name) and sub.target.id == name:\n'
        '                add(sub.target, "value", sub.value)\n',
        ""),
    "tuple-extract": (
        '    if isinstance(value, (ast.Tuple, ast.List)) \\\n'
        '            and len(target.elts) == len(value.elts) \\\n'
        '            and not any(isinstance(child, ast.Starred) for child in target.elts):\n'
        '        for child, item in zip(target.elts, value.elts):\n'
        '            yield from _assignment_values(child, item, name)\n'
        '    else:\n'
        '        for target_name in _name_targets(target, name):\n'
        '            yield target_name, None, "unresolved destructuring"\n',
        '    for target_name in _name_targets(target, name):\n'
        '        yield target_name, None, "unresolved destructuring"\n'),
    "sort-deletion": (
        '    events.sort(key=lambda event: (event[0], event[1]))\n',
        ""),
}
V4_REGIONS = [t[0] for t in TRANSFORMS.values() if t[1] == ""] \
    + [TRANSFORMS["tuple-extract"][0]]
ARMS = ("timeout_scope_walrus_positive", "timeout_scope_tupleunpack_positive",
        "timeout_scope_source_order")

failures = []


def check(name, ok, detail=""):
    print("check %-26s %s%s" % (name, "PASS" if ok else "FAIL",
                                (" (%s)" % detail) if detail else ""))
    if not ok:
        failures.append(name)


def sh256(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(rev, path):
    proc = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                          capture_output=True, timeout=120)
    return proc.stdout if proc.returncode == 0 else None


def run(argv, timeout=900):
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def selftest(sandbox, checker_abs, rev):
    argv = [sys.executable, checker_abs, rev, "--repo", sandbox,
            "--contract", os.path.join(sandbox, CONTRACT_REL),
            "--counter", os.path.join(sandbox, C8_REL), "--selftest"]
    return run(argv)


def parse_selftest(out):
    m = re.search(r"CONFORM_SELFTEST pass=(\d+) fail=(\d+)", out)
    fails = re.findall(r"^FAIL (\S+)", out, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None), fails


def routed_four(sandbox, checker_abs, rev):
    verdicts = []
    for rel, _want_verdict, _want_failing in ROUTED:
        rc, out, _err = run([sys.executable, checker_abs, rev, "--repo", sandbox,
                             "--contract", os.path.join(sandbox, CONTRACT_REL),
                             "--counter", os.path.join(sandbox, rel)])
        m = re.search(r"CONFORM=(\w+)", out)
        failing = sorted(re.findall(r"^check (\S+)\s+FAIL", out, re.M))
        verdicts.append((m.group(1) if m else None, failing, rc))
    return verdicts


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: count-c1.py <rev> [--repo LANE]")
        return 2
    rev = args[0]
    if "--repo" in args:
        global LANE
        LANE = args[args.index("--repo") + 1]

    # -- 1. freeze pins at REV -------------------------------------------
    pins_raw = git_bytes(rev, PINS_REL)
    if pins_raw is None:
        check("pins_present", False, PINS_REL)
        print("C1=unmet")
        return 1
    pins = {}
    for line in pins_raw.decode().splitlines():
        parts = line.split()
        if len(parts) >= 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            pins[parts[1]] = parts[0]
    bad_pins = []
    for path, want in pins.items():
        got = git_bytes(rev, path)
        if got is None or sh256(got) != want:
            bad_pins.append(path)
    check("pins_present", True, "%d pins" % len(pins))
    check("pins_match", not bad_pins, "mismatch=%s" % bad_pins)

    v4 = git_bytes(rev, V4_REL)
    v5 = git_bytes(rev, V5_REL)
    check("v4_present", v4 is not None and sh256(v4) == pins.get(V4_REL),
          "v4 sha=%s" % (sh256(v4)[:12] if v4 else None))
    check("v5_present", v5 is not None, V5_REL)
    if v5 is None or v4 is None:
        print("C1=unmet")
        return 1
    check("v5_differs_from_v4", sh256(v5) != sh256(v4), "same bytes as v4")
    check("v5_regions_intact", all(r.encode() in v5 for r in V4_REGIONS),
          "v4 mutation regions byte-persist in v5")
    check("v5_new_arms_named", all(a.encode() in v5 for a in ARMS),
          "three new arm names present")

    # -- 2. sandbox --------------------------------------------------------
    sandbox = tempfile.mkdtemp(prefix="mori-r42-c1-", dir="/tmp")
    clone = os.path.join(sandbox, "repo")
    rc, _o, e = run(["git", "clone", "-q", "--shared", LANE, clone])
    if rc != 0:
        check("sandbox_clone", False, e.strip()[:120])
        print("C1=unmet")
        return 1
    check("sandbox_clone", True, "at %s" % rev)
    run(["git", "-C", clone, "checkout", "-q", "--detach", rev])
    v4_abs = os.path.join(clone, V4_REL)
    v5_abs = os.path.join(clone, V5_REL)

    # -- 3. v4 control: honest 14 arms, mutants survive --------------------
    rc, out, err = selftest(clone, v4_abs, rev)
    (p, f), fails = parse_selftest(out)
    check("v4_control_selftest", (p, f) == (14, 0) and rc == 0 and not fails,
          "pass=%s fail=%s rc=%d" % (p, f, rc))
    for name, _arm in V5_MUTANTS:
        old, new = TRANSFORMS[name]
        assert v4.decode().count(old) == 1, "freeze transform anchor lost"
        mut = v4.decode().replace(old, new, 1).encode()
        mut_rel = ".ufo/waves/round-42/fixtures/mutants/conform-v4-mut-%s.py" % name
        want_pin = pins.get(mut_rel)
        check("v4_mutant_pin_%s" % name,
              want_pin is not None and sh256(mut) == want_pin,
              "derived sha=%s" % sh256(mut)[:12])
        with open(v4_abs, "wb") as fh:
            fh.write(mut)
        rc, out, _e = selftest(clone, v4_abs, rev)
        (p, f), fails = parse_selftest(out)
        check("v4_mutant_survives_%s" % name,
              (p, f) == (14, 0) and rc == 0 and not fails,
              "pass=%s fail=%s (survival: no arm can see it)" % (p, f))
    with open(v4_abs, "wb") as fh:
        fh.write(v4)

    # -- 4. v5 honest: 17 arms --------------------------------------------
    rc, out, err = selftest(clone, v5_abs, rev)
    (p, f), fails = parse_selftest(out)
    check("v5_selftest_17", (p, f) == (17, 0) and rc == 0 and not fails,
          "pass=%s fail=%s rc=%d" % (p, f, rc))

    # -- 5. v5 mutants: derived == committed; kill exactly one arm ---------
    v5_text = v5.decode()
    for name, arm in V5_MUTANTS:
        old, new = TRANSFORMS[name]
        check("v5_region_%s" % name, v5_text.count(old) == 1,
              "anchor count=%d" % v5_text.count(old))
        derived = v5_text.replace(old, new, 1).encode()
        mut_rel = (".ufo/waves/round-42/fixtures/mutants/"
                   "conform-mut-%s.py" % name)
        committed = git_bytes(rev, mut_rel)
        check("v5_mutant_committed_%s" % name, committed is not None, mut_rel)
        check("v5_mutant_derived_%s" % name,
              committed is not None and sh256(derived) == sh256(committed),
              "derived=%s committed=%s"
              % (sh256(derived)[:12],
                 sh256(committed)[:12] if committed else None))
        if committed is None:
            continue
        with open(v5_abs, "wb") as fh:
            fh.write(committed)
        rc, out, _e = selftest(clone, v5_abs, rev)
        (p, f), fails = parse_selftest(out)
        check("v5_mutant_kill_%s" % name,
              (p, f) == (16, 1) and rc == 1 and fails == [arm],
              "pass=%s fail=%s fails=%s (want [%s])" % (p, f, fails, arm))
    with open(v5_abs, "wb") as fh:
        fh.write(v5)

    # -- 6. routed four under v5 honest -----------------------------------
    verdicts = routed_four(clone, v5_abs, rev)
    want = [(w, f) for _r, w, f in ROUTED]
    got = [(v, f) for v, f, _rc in verdicts]
    check("v5_routed_four", got == want, "got=%s" % got)

    # -- 7. lane no-harm: gate selftest + lane line unchanged -------------
    rc, out, _e = run([sys.executable,
                       os.path.join(clone, "tools/mori-sources-appendonly.py"),
                       "--selftest"], cwd=clone)
    m = re.search(r"MORI_SOURCES_APPENDONLY_SELFTEST pass=(\d+) fail=(\d+)",
                  out)
    check("gate_selftest_unharmed",
          rc == 0 and m and (int(m.group(1)), int(m.group(2))) == (22, 0),
          "rc=%d out=%s" % (rc, (m.group(0) if m else out.strip()[:120])))

    print("C1=%s" % ("unmet" if failures else "met"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
