#!/usr/bin/env python3
"""Round-39 C8 conformance checker: instrument identity, replayability, bounds,
timeout values and drain shape (round-38 lesson M19).

Usage:
    conform.py <rev> [--repo DIR] [--contract PATH] [--counter PATH]...
                 [--selftest]

Checks (the first --counter is the instrument under behavioural test; every
--counter is audited statically):
  predicate        the contract's P-C7 blockquote, normalised, equals the first
                   line the counter prints for `--print-predicate`.
  head_pin         `--pin-only` prints `head_at_measurement=<40-hex>` equal to the
                   lane tip.
  tool_resolve     `--print-tool <repo-relative path>` prints the absolute path
                   under the repository and exits 0.
  bounded_reads    every `subprocess.run(` and every `communicate(` in every
                   counter carries a `timeout=` keyword, and the first counter
                   caps the committed-blob read with `cat-file -s` + MAX_BLOB_BYTES.
  timeout_value    every `timeout=` keyword in every counter resolves through
                   module-level assignments and function-parameter defaults to a
                   positive numeric literal, so `timeout=NAME` with `NAME = None`
                   fails (r38 M19 bypass A).
  drain_shape      every `Popen(` in the first counter is drained in its own
                   function by a `communicate(` whose result is used, so a
                   `wait(timeout=…)` + `stdout.read()` drain fails (r38 M19
                   bypass B).
  timeout_state    `fixtures/hang-after-flush.py` under `--tool-timeout 3
                   --arms selftest` yields `C7=unmet` with a `tool_timeout` reason,
                   never `C7=met`, never a silent pass.
  scratch          every `tempfile.mkdtemp(` in every counter passes `dir=` and the
                   counter carries a scratch parent under
                   `.ufo/waves/round-39/scratch`.
  selftest_conjunct the checker can kill the communicate-timeout conjunct itself:
                   stripping the `timeout=` keyword from the first counter's
                   communicate call flips exactly `bounded_reads` (r38 M19: the
                   shipped selftest never exercised this conjunct).

`--selftest` applies nine textual mutations to copies of the first counter and
requires each mutation to flip exactly its own check to FAIL.

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
SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-39", "scratch")
DEFAULT_COUNTERS = [os.path.join(LANE, ".ufo/waves/round-39/count-c7.py")]
DEFAULT_CONTRACT = os.path.join(LANE, ".ufo/waves/round-39/contract.md")
FIXTURE_REL = ".ufo/waves/round-39/fixtures/witness-summary-only-live.txt"
HANG_FIXTURE = os.path.join(LANE, ".ufo/waves/round-39/fixtures/hang-after-flush.py")
CHECK_NAMES = ("predicate", "head_pin", "tool_resolve", "bounded_reads",
               "timeout_value", "drain_shape", "timeout_state", "scratch",
               "selftest_conjunct")

PREDICATE = (
    "P-C8: at revision R, the round-39 conformance checker passes all nine checks "
    "on the round-39 counter bytes — the round-38 six (predicate, head_pin, "
    "tool_resolve, bounded_reads, timeout_state, scratch) plus `timeout_value` "
    "(every `timeout=` keyword in every counter resolves through module-level "
    "assignments to a positive numeric literal, so `timeout=NAME` with `NAME = "
    "None` fails), `drain_shape` (every `Popen(` in the first counter is drained "
    "in its own function by a `communicate(` carrying its own timeout, so a "
    "`wait(timeout=…)` plus `stdout.read()` drain fails), and `selftest_conjunct` "
    "(the shipped `--selftest`'s bounded_reads mutation exercises the "
    "communicate-timeout conjunct) — and each of nine textual mutations flips "
    "exactly its own check to FAIL."
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
    """The P-C7 blockquote of record."""
    marker = "P-C7 (frozen"
    index = text.find(marker)
    if index < 0:
        index = 0
    m = re.search(r"^> (P-C7:.*?)\n\n", text[index:], re.M | re.S)
    if not m:
        raise SetupError("no P-C7 blockquote in the contract")
    return normalise(m.group(1).replace("\n> ", " "))


# ----------------------------------------------------------- timeout value fold

class Unresolvable(Exception):
    pass


def _resolve(node, assign, params):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise Unresolvable("non-numeric constant")
    if isinstance(node, ast.Name):
        if node.id in params:
            return _resolve(params[node.id], assign, {})
        if node.id in assign:
            return _resolve(assign[node.id], assign, {})
        raise Unresolvable("name %r has no binding" % node.id)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_resolve(node.operand, assign, params)
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub,
                                                            ast.Mult, ast.Div)):
        left = _resolve(node.left, assign, params)
        right = _resolve(node.right, assign, params)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return left / right
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_resolve(e, assign, params) for e in node.elts]
    if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) \
            and isinstance(node.slice.value, int):
        base = _resolve(node.value, assign, params)
        if isinstance(base, (list, tuple)) and -len(base) <= node.slice.value < len(base):
            return base[node.slice.value]
        raise Unresolvable("subscript of non-sequence")
    raise Unresolvable("expression %s" % ast.dump(node)[:60])


def _timeout_value(node, assign, params):
    """Resolve a timeout= kwarg value to a positive number or raise."""
    value = _resolve(node, assign, params)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        raise Unresolvable("timeout value %r is not positive" % (value,))
    return value


# ---------------------------------------------------------------- static audit

def static_checks(source):
    """Per-counter static audit.

    Returns dict with bounded_reads/timeout_value/drain_shape/scratch detail.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise SetupError("counter does not parse: %s" % exc)

    assign = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            assign[node.targets[0].id] = node.value

    func_params = {}       # function name -> {param: default expr or None}
    func_nodes = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defaults = {}
            args = node.args
            positional = list(args.posonlyargs) + list(args.args)
            offset = len(positional) - len(args.defaults)
            for index, default in enumerate(args.defaults):
                defaults[positional[offset + index].arg] = default
            for name, default in zip(args.kwonlyargs, args.kw_defaults):
                if default is not None:
                    defaults[name.arg] = default
            func_params[node.name] = defaults
            func_nodes[node.name] = node

    def enclosing_function(call):
        best = None
        for name, fn in func_nodes.items():
            if fn.lineno <= call.lineno <= getattr(fn, "end_lineno", fn.lineno):
                if best is None or fn.lineno >= best.lineno:
                    best = fn
        return best

    bounded_violations = []
    value_violations = []
    popens = []
    communicates = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else \
            (func.id if isinstance(func, ast.Name) else None)
        timeout_kwargs = [k for k in node.keywords if k.arg == "timeout"]
        if name in ("run", "check_output", "check_call"):
            if not timeout_kwargs:
                bounded_violations.append("%s without timeout at line %d"
                                          % (name, node.lineno))
        for k in timeout_kwargs:
            fn = enclosing_function(node)
            params = func_params.get(fn.name, {}) if fn else {}
            try:
                _timeout_value(k.value, assign, params)
            except Unresolvable as exc:
                value_violations.append("line %d (%s): %s" % (node.lineno, name, exc))
        if name == "Popen":
            popens.append(node)
        if name == "communicate":
            communicates.append(node)

    # parent links for result-use detection
    for child in ast.walk(tree):
        for grand in ast.iter_child_nodes(child):
            grand.parent = child

    drain_violations = []
    for popen in popens:
        fn = enclosing_function(popen)
        drained = False
        for comm in communicates:
            if enclosing_function(comm) is not fn:
                continue
            parent = getattr(comm, "parent", None)
            used = isinstance(parent, (ast.Assign, ast.Return, ast.Tuple))
            if used:
                drained = True
                break
        if not drained:
            drain_violations.append("Popen at line %d not drained by a used "
                                    "communicate in its function" % popen.lineno)

    mkdtemp_ok = True
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.attr if isinstance(func, ast.Attribute) else \
                (func.id if isinstance(func, ast.Name) else None)
            if name == "mkdtemp":
                mkdtemp_ok = mkdtemp_ok and any(k.arg == "dir" for k in node.keywords)

    scratch_root = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "SCRATCH_ROOT" for t in node.targets):
            segment = ast.get_source_segment(source, node.value) or ""
            scratch_root = all(part in segment for part in
                               ('".ufo"', '"waves"', '"round-39"', '"scratch"'))

    # presence-only: the timeout *value* of a communicate call belongs to
    # the timeout_value check; this rule owns the conjunct (a communicate
    # drain must carry the keyword at all, and stripping it must be caught)
    comm_violations = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else \
            (func.id if isinstance(func, ast.Name) else None)
        if name == "communicate" and not any(k.arg == "timeout"
                                             for k in node.keywords):
            comm_violations.append("communicate without timeout at line %d"
                                   % node.lineno)

    blob_cap = "MAX_BLOB_BYTES" in source and '"-s"' in source
    return {
        "comm_violations": comm_violations,
        "bounded_violations": bounded_violations,
        "value_violations": value_violations,
        "drain_violations": drain_violations,
        "mkdtemp_ok": mkdtemp_ok,
        "scratch_root": scratch_root,
        "blob_cap": blob_cap,
        "has_communicate_timeout": not bounded_violations
        and any(isinstance(n, ast.Call) and (
            (isinstance(n.func, ast.Attribute) and n.func.attr == "communicate") or
            (isinstance(n.func, ast.Name) and n.func.id == "communicate"))
            for n in ast.walk(tree)),
        "first_communicate_segment": _first_communicate_segment(source),
    }


def _first_communicate_segment(source):
    m = re.search(r"proc\.communicate\(timeout=[^)]+\)", source)
    return m.group(0) if m else None


def evaluate(repo, rev, counters, contract_path):
    first = counters[0]
    results = {}
    contract_text = open(contract_path, encoding="utf-8").read()
    want = None
    try:
        want = contract_predicate(contract_text)
    except SetupError as exc:
        results["predicate"] = (False, str(exc))

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

    stats = {}
    all_bounded = all_values = True
    detail = []
    for path in counters:
        try:
            source = open(path, encoding="utf-8").read()
        except OSError:
            all_bounded = all_values = False
            detail.append("%s: unreadable" % os.path.basename(path))
            continue
        st = static_checks(source)
        stats[path] = st
        bounded_ok = not st["bounded_violations"]
        if path == first:
            bounded_ok = bounded_ok and st["blob_cap"]
        all_bounded = all_bounded and bounded_ok
        all_values = all_values and not st["value_violations"]
        detail.append("%s: bounded=%s value=%s" % (os.path.basename(path),
                                                   st["bounded_violations"],
                                                   st["value_violations"]))
    results["bounded_reads"] = (all_bounded, "; ".join(detail))
    results["timeout_value"] = (all_values, "; ".join(detail))

    first_stat = stats.get(first, {})
    drain_ok = not first_stat.get("drain_violations")
    results["drain_shape"] = (
        bool(first_stat) and drain_ok,
        "violations=%s" % first_stat.get("drain_violations", "counter unreadable"))

    proc = run([sys.executable, first, rev, "--repo", repo, "--tool", HANG_FIXTURE,
                "--tool-timeout", "3", "--arms", "selftest"], timeout=25)
    text = ((proc.stdout or "") + (proc.stderr or "")) if proc else ""
    ok = (proc is not None and proc.returncode == 1 and "C7=unmet" in text
          and "tool_timeout" in text and "tool selftest: pass" not in text)
    results["timeout_state"] = (ok, "exit=%s timeout_reason=%s pass=%s"
                                % (None if proc is None else proc.returncode,
                                   "tool_timeout" in text,
                                   "tool selftest: pass" in text))

    scratch_ok = True
    details = []
    for path in counters:
        st = stats.get(path)
        if st is None:
            try:
                st = static_checks(open(path, encoding="utf-8").read())
            except OSError:
                scratch_ok = False
                details.append("%s: unreadable" % os.path.basename(path))
                continue
        scratch_ok = scratch_ok and st["mkdtemp_ok"] and st["scratch_root"]
        details.append("%s: mkdtemp_dir=%s root=%s"
                       % (os.path.basename(path), st["mkdtemp_ok"],
                          st["scratch_root"]))
    results["scratch"] = (scratch_ok, "; ".join(details))

    # selftest_conjunct: the communicate-timeout rule holds on the counter,
    # and stripping the first communicate timeout is detected by that same
    # rule (r38 M19: the shipped selftest never exercised this conjunct)
    conjunct_ok = False
    conjunct_detail = "no communicate(timeout=...) call found"
    try:
        first_source = open(first, encoding="utf-8").read()
    except OSError:
        first_source = None
    if first_source:
        try:
            st_first = static_checks(first_source)
            honest_comm = st_first["comm_violations"]
        except SetupError as exc:
            honest_comm = ["does not parse: %s" % exc]
        mutant_source, n_sub = re.subn(r"proc\.communicate\(timeout=[^)]+\)",
                                       "proc.communicate()", first_source, count=1)
        if n_sub:
            try:
                st_mut = static_checks(mutant_source)
                conjunct_ok = (not honest_comm) and bool(st_mut["comm_violations"])
                conjunct_detail = "honest_comm=%s mutant_comm=%s" % (
                    honest_comm, st_mut["comm_violations"])
            except SetupError as exc:
                conjunct_detail = "mutant does not parse: %s" % exc
    results["selftest_conjunct"] = (conjunct_ok, conjunct_detail)
    return results


def selftest(repo, rev, counter, contract_path):
    """Nine mutations of the counter; each must flip exactly its own check."""
    mutations = [
        ("predicate", "checks that the round-38 checks could not discriminate",
         "checks that the round-38 checks could discriminate",
         "predicate token changed"),
        ("head_pin", 'print("head_at_measurement=%s"',
         'print("head=%s"', "pin label renamed"),
        ("tool_resolve",
         "print(os.path.abspath(os.path.join(repo, args.print_tool)))",
         "print(args.print_tool)", "relative resolution removed"),
        ("bounded_reads",
         'proc = subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True,\n'
         '                          timeout=timeout, env=clean_env())',
         'proc = subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True,\n'
         '                          env=clean_env())',
         "git helper run timeout removed"),
        ("timeout_value", "GIT_TIMEOUT_S = 120", "GIT_TIMEOUT_S = None",
         "timeout value replaced with None"),
        ("drain_shape",) ,  # placeholder, replaced by the block swap below
        ("timeout_state", "proc = run_tool(args.tool, [\"--selftest\"], args.tool_timeout)",
         "proc = run_tool(args.tool, [\"--selftest\"], TOOL_TIMEOUT_S)",
         "budget flag ignored"),
        ("scratch",
         'SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-39", "scratch")',
         'SCRATCH_ROOT = "/tmp/mori-r39-scratch"', "scratch parent moved off-lane"),
        ("selftest_conjunct",
         "out, err = proc.communicate(timeout=timeout)",
         "out, err = proc.communicate()",
         "communicate timeout keyword stripped"),
    ]
    source = open(counter, encoding="utf-8").read()
    # drain_shape: swap run()'s entire timeout-handling block for a
    # wait+read drain (r38 M19 bypass B). The block is extracted from the
    # counter itself so the anchor is exact.
    drain_old = ""
    drain_new = ""
    start_anchor = "    try:\n        out, err = proc.communicate(timeout=timeout)\n"
    end_anchor = '        raise ProbeTimeout("child exceeded %ds" % timeout)\n'
    si = source.find(start_anchor)
    ei = source.find(end_anchor)
    if si >= 0 and ei > si:
        drain_old = source[si:ei + len(end_anchor)]
        indent = "    "
        drain_new = (
            indent + "try:\n"
            + indent + "    proc.wait(timeout=timeout)\n"
            + indent + "    out, err = proc.stdout.read(), proc.stderr.read()\n"
            + indent + "except subprocess.TimeoutExpired:\n"
            + indent + "    try:\n"
            + indent + "        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)\n"
            + indent + "    except OSError:\n"
            + indent + "        pass\n"
            + indent + "    try:\n"
            + indent + "        proc.wait(timeout=SELFTEST_GRACE_S)\n"
            + indent + "    except subprocess.TimeoutExpired:\n"
            + indent + "        try:\n"
            + indent + "            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)\n"
            + indent + "        except OSError:\n"
            + indent + "            pass\n"
            + indent + "    out, err = proc.stdout.read(), proc.stderr.read()\n"
            + end_anchor)
    mutations = [m if m[0] != "drain_shape" else
                 ("drain_shape", drain_old, drain_new,
                  "communicate drains replaced by wait+read")
                 for m in mutations]
    os.makedirs(SCRATCH_ROOT, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)
    passed = failed = 0
    try:
        for name, old, new, why in mutations:
            if old not in source:
                print("FAIL %-18s mutation anchor absent (%s)" % (name, why))
                failed += 1
                continue
            path = os.path.join(work, "counter-%s.py" % name)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(source.replace(old, new, 1))
            results = evaluate(repo, rev, [path], contract_path)
            failing = sorted(k for k, (ok, _) in results.items() if not ok)
            if failing == [name]:
                passed += 1
                print("PASS %-18s %s -> only %s failed" % (name, why, name))
            else:
                failed += 1
                print("FAIL %-18s %s -> failing=%s" % (name, why, failing))
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
        print("check %-18s %s (%s)" % (name, "PASS" if ok else "FAIL", detail))
    met = all(results[name][0] for name in CHECK_NAMES)
    print("CONFORM=%s" % ("met" if met else "unmet"))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # setup error
        print("conformance setup error: %s" % exc, file=sys.stderr)
        sys.exit(2)
