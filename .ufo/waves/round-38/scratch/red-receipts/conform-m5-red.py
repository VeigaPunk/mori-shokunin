#!/usr/bin/env python3
"""Round-38 C5 conformance checker: instrument identity, replayability and bounds.

Usage:
    conform.py <rev> [--repo DIR] [--contract PATH] [--counter PATH]...
                 [--selftest]

Checks (the first --counter is the instrument under behavioural test; every
--counter is audited statically):
  predicate      the contract's P-C1 blockquote, normalised, equals the first line the
                 counter prints for `--print-predicate`.
  head_pin       `--pin-only` prints `head_at_measurement=<40-hex>` equal to the lane tip.
  tool_resolve   `--print-tool <repo-relative path>` prints the absolute path under the
                 repository and exits 0.
  bounded_reads  every `subprocess.run(` in every counter carries `timeout=`, every
                 `Popen(` is followed by `communicate(timeout=`, and the first counter
                 caps the committed-blob read with `cat-file -s` + MAX_BLOB_BYTES.
  timeout_state  `fixtures/hang-after-flush.py` under `--tool-timeout 3 --arms real`
                 yields `C1=unmet` with a `tool_timeout` reason and never `real arm: pass`.
  scratch        every `tempfile.mkdtemp(` in every counter passes `dir=` and the counter
                 carries a scratch parent under `.ufo/waves/round-38/scratch`.

`--selftest` applies six textual mutations to copies of the first counter and requires
each mutation to flip exactly its own check to FAIL.

Exit: 0 met, 1 unmet, 2 setup error.
"""
import argparse
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
SCRATCH_ROOT = os.path.join(LANE, ".ufo/waves/round-38/scratch")
DEFAULT_COUNTERS = [os.path.join(LANE, ".ufo/waves/round-38/count-c1.py"),
                    os.path.join(LANE, ".ufo/waves/round-38/count-c4.py")]
DEFAULT_CONTRACT = os.path.join(LANE, ".ufo/waves/round-38/contract.md")
FIXTURE_REL = ".ufo/waves/round-38/fixtures/summary-only.py"
HANG_FIXTURE = os.path.join(LANE, ".ufo/waves/round-38/fixtures/hang-after-flush.py")
CHECK_NAMES = ("predicate", "head_pin", "tool_resolve", "bounded_reads",
               "timeout_state", "scratch")

PREDICATE = (
    "P-C5: at revision R, the round-38 C1 counter prints the contract's P-C1 bytes as "
    "its predicate, prints the lane tip it measured as `head_at_measurement=<40-hex>`, "
    "resolves a repo-relative `--tool` path against the lane, bounds every child and git "
    "read by a timeout and the committed-blob read by a byte cap, maps a tool that "
    "flushes then hangs to `tool_timeout` (never a pass and never a silent unmet), and "
    "creates every scratch directory with `tempfile.mkdtemp` under the lane's "
    "`.ufo/waves/round-38/scratch`; the conformance checker passes all six checks on "
    "those bytes and each of six mutations of them flips exactly its own check to FAIL."
)


class SetupError(Exception):
    pass


def run(cmd, cwd=None, timeout=30):
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_GLOBAL"):
        env.pop(key, None)
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None


def normalise(text):
    return re.sub(r"\s+", " ", text or "").strip()


def contract_predicate(text):
    """The P-C1 blockquote of record: the one following the 'of record' heading."""
    marker = "P-C1 of record"
    index = text.find(marker)
    if index < 0:
        index = 0
    m = re.search(r"^> (P-C1:.*?)\n\n", text[index:], re.M | re.S)
    if not m:
        raise SetupError("no P-C1 blockquote in the contract")
    return normalise(m.group(1).replace("\n> ", " "))


def static_checks(source):
    """(run_timeouts_ok, popen_timeout_ok, blob_cap_ok, mkdtemp_dir_ok, scratch_root_ok).

    run_timeouts_ok covers both `subprocess.run(` and the module's own bounded `run(`
    helper (every child run carries a timeout).  scratch_root_ok reads the literal
    arguments of the SCRATCH_ROOT assignment, so a mutated path cannot pass on a
    substring elsewhere in the file.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise SetupError("counter does not parse: %s" % exc)
    run_ok = popen_ok = mkdtemp_ok = True
    saw_communicate = False
    blob_cap = "MAX_BLOB_BYTES" in source and '"-s"' in source
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else \
            (func.id if isinstance(func, ast.Name) else None)
        kw = {k.arg for k in node.keywords}
        if name == "run":
            run_ok = run_ok and "timeout" in kw
        if name == "Popen":
            segment = ast.get_source_segment(source, node) or ""
            popen_ok = popen_ok and "start_new_session" in segment
        if name == "communicate":
            # every drain must carry its own timeout (r38 RevC5Bounds: a setsid
            # descendant can hold the pipe open past the kill)
            saw_communicate = True
            popen_ok = popen_ok and "timeout" in kw
        if name == "mkdtemp":
            mkdtemp_ok = mkdtemp_ok and "dir" in kw
    popen_ok = popen_ok and saw_communicate
    scratch_root = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "SCRATCH_ROOT" for t in node.targets):
            segment = ast.get_source_segment(source, node.value) or ""
            scratch_root = all(part in segment for part in
                               ('".ufo"', '"waves"', '"round-38"', '"scratch"'))
    return run_ok, popen_ok, blob_cap, mkdtemp_ok, scratch_root


def evaluate(repo, rev, counters, contract_path):
    first = counters[0]
    results = {}
    contract_text = open(contract_path, encoding="utf-8").read()
    try:
        want = contract_predicate(contract_text)
    except SetupError as exc:
        results["predicate"] = (False, str(exc))
        want = None

    if want is not None:
        proc = run([sys.executable, first, "--print-predicate"], timeout=30)
        got = normalise(proc.stdout) if proc else None
        results["predicate"] = (proc is not None and proc.returncode == 0 and got == want,
                                "exit=%s equal=%s"
                                % (None if proc is None else proc.returncode,
                                   got == want))

    proc = run([sys.executable, first, "--pin-only", "--repo", repo], timeout=30)
    pin = None
    if proc is not None:
        m = re.search(r"^head_at_measurement=([0-9a-f]{40})$", proc.stdout, re.M)
        pin = m.group(1) if m else None
    tip_proc = run(["git", "-C", repo, "rev-parse", "HEAD"], timeout=30)
    tip = tip_proc.stdout.strip() if tip_proc is not None else ""
    results["head_pin"] = (proc is not None and proc.returncode == 0 and pin == tip,
                           "pin=%s tip=%s" % (pin, tip))

    proc = run([sys.executable, first, "--print-tool", FIXTURE_REL, "--repo", repo],
               timeout=30)
    resolved = (proc.stdout.strip() if proc else "")
    ok = (proc is not None and proc.returncode == 0 and os.path.isabs(resolved)
          and os.path.realpath(resolved).startswith(os.path.realpath(repo) + os.sep)
          and os.path.isfile(resolved))
    results["tool_resolve"] = (ok, "exit=%s resolved=%s"
                              % (None if proc is None else proc.returncode, resolved))

    source_ok = True
    detail = []
    for path in counters:
        try:
            source = open(path, encoding="utf-8").read()
        except OSError:
            source_ok = False
            detail.append("%s: unreadable" % os.path.basename(path))
            continue
        run_ok, popen_ok, blob_cap, mkdtemp_ok, scratch_root = static_checks(source)
        ok = run_ok and popen_ok
        if path == first:
            ok = ok and blob_cap
        source_ok = source_ok and ok
        detail.append("%s: run=%s popen=%s cap=%s mkdtemp=%s scratch=%s"
                      % (os.path.basename(path), run_ok, popen_ok, blob_cap,
                         mkdtemp_ok, scratch_root))
    results["bounded_reads"] = (source_ok, "; ".join(detail))

    proc = run([sys.executable, first, rev, "--repo", repo, "--tool", HANG_FIXTURE,
                "--tool-timeout", "3", "--arms", "real", "--seed", "5"], timeout=25)
    text = ((proc.stdout or "") + (proc.stderr or "")) if proc else ""
    ok = (proc is not None and proc.returncode == 1 and "C1=unmet" in text
          and "tool_timeout" in text and "real arm: pass" not in text)
    results["timeout_state"] = (ok, "exit=%s timeout_reason=%s pass=%s"
                                % (None if proc is None else proc.returncode,
                                   "tool_timeout" in text, "real arm: pass" in text))

    scratch_ok = True
    details = []
    for path in counters:
        try:
            source = open(path, encoding="utf-8").read()
        except OSError:
            scratch_ok = False
            details.append("%s: unreadable" % os.path.basename(path))
            continue
        try:
            _, _, _, mkdtemp_ok, scratch_root = static_checks(source)
        except SetupError as exc:
            mkdtemp_ok, scratch_root = False, str(exc)
        scratch_ok = scratch_ok and mkdtemp_ok and scratch_root
        details.append("%s: mkdtemp_dir=%s root=%s"
                       % (os.path.basename(path), mkdtemp_ok, scratch_root))
    results["scratch"] = (scratch_ok, "; ".join(details))
    return results


def selftest(repo, rev, counter, contract_path):
    """Six mutations of the counter; each must flip exactly its own check."""
    mutations = [
        ("predicate", "hidden truth for ids",
         "hidden  truth for ids", "predicate whitespace-only change"),
        ("head_pin", 'print("head_at_measurement=%s"',
         'print("head=%s"', "pin label renamed"),
        ("tool_resolve", "return os.path.abspath(os.path.join(os.path.abspath(repo), path))",
         "return os.path.abspath(os.path.join(os.path.abspath(repo), path.strip()))", "semantic no-op mutation"),
        ("bounded_reads", "proc = run([\"git\", \"-C\", repo] + list(args), timeout=timeout, env=clean_env())",
         "proc = run([\"git\", \"-C\", repo] + list(args), env=clean_env())",
         "git helper run timeout removed"),
        ("timeout_state", "_TOOL_BUDGET[0] = max(1, args.tool_timeout)",
         "_TOOL_BUDGET[0] = max(1, int(args.tool_timeout))", "semantic no-op mutation"),
        ("scratch", 'SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-38", "scratch")',
         'SCRATCH_ROOT = "/tmp/mori-r38-scratch"', "scratch parent moved off-lane"),
    ]
    source = open(counter, encoding="utf-8").read()
    os.makedirs(SCRATCH_ROOT, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)
    passed = failed = 0
    try:
        for name, old, new, why in mutations:
            if old not in source:
                print("FAIL %-14s mutation anchor absent (%s)" % (name, why))
                failed += 1
                continue
            path = os.path.join(work, "counter-%s.py" % name)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(source.replace(old, new, 1))
            results = evaluate(repo, rev, [path], contract_path)
            failing = sorted(k for k, (ok, _) in results.items() if not ok)
            if failing == [name]:
                passed += 1
                print("PASS %-14s %s -> only %s failed" % (name, why, name))
            else:
                failed += 1
                print("FAIL %-14s %s -> failing=%s" % (name, why, failing))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("CONFORM_SELFTEST pass=%d fail=%d" % (passed, failed))
    return 0 if failed == 0 else 1


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("rev", nargs="?", default=None)
    parser.add_argument("--repo", default=LANE)
    parser.add_argument("--contract", default=DEFAULT_CONTRACT)
    parser.add_argument("--counter", action="append", default=None)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)

    counters = args.counter or DEFAULT_COUNTERS
    if args.selftest:
        return selftest(os.path.abspath(args.repo), args.rev,
                        counters[0], args.contract)
    if not args.rev:
        parser.error("a revision is required (or --selftest)")

    print(PREDICATE)
    try:
        results = evaluate(os.path.abspath(args.repo), args.rev, counters, args.contract)
    except SetupError as exc:
        print("conformance setup error: %s" % exc, file=sys.stderr)
        return 2
    for name in CHECK_NAMES:
        ok, detail = results[name]
        print("check %-16s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    met = all(results[name][0] for name in CHECK_NAMES)
    print("CONFORM=%s" % ("met" if met else "unmet"))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # setup error
        print("conformance setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
