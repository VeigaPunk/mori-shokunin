#!/usr/bin/env python3
"""Round-42 C1 conformance checker v5: the v4 checks plus three fixture arms
that close the three surviving round-41 checker-mutation lanes (walrus branch
deletion, element-wise destructuring extraction deletion, event-order sort
deletion). The nine static checks keep their round-41 semantics; the selftest
grows from fourteen counter-mutation arms to seventeen arms.

Usage:
    conform.py <rev> [--repo DIR] [--contract PATH] [--counter PATH]...
                 [--selftest]

Checks (the first --counter is the instrument under behavioural test; every
  --counter is audited statically):
  predicate        the contract's P-C10 sentence, normalised, equals the first
                   line the counter prints for `--print-predicate`.
  head_pin         `--pin-only` prints `head_at_measurement=<40-hex>` equal to
                   the repository's live HEAD; `rev` scopes timeout_state only.
  tool_resolve     `--print-tool <repo-relative path>` prints the absolute path
                   under the repository and exits 0.
  bounded_reads    every `subprocess.run(` and every `communicate(` in every
                   counter carries a `timeout=` keyword, and the first counter
                   caps the committed-blob read with `cat-file -s` + MAX_BLOB_BYTES.
  timeout_scope    every `timeout=` keyword in every counter resolves in the
                   scope of its read site — a binding inside the enclosing
                   function shadows the module map, a `global` rebinding is read
                   at module scope, a module-level binding nested in
                   `if`/`try`/`for`/`while` makes the name conditionally
                   rebound and fails closed, and the value must be a finite
                   positive number, so a function-local `TIMEOUT = None` shadow,
                   a conditional `NAME = None` rebind and `1e400` all fail, and
                   a fold raising ZeroDivisionError/RecursionError fails as a
                   violation, not a setup error (r39 w1 findings 4, M3, L4).
  drain_bind       every `Popen(` in every counter is drained in its own
                   function by a `communicate(` bound to the same name, carrying
                   its own timeout, with the result consumed (assigned to other
                   than `_`, or returned), so a `wait(timeout=…)` +
                   `stdout.read()` drain fails even beside a decoy used
                   communicate, an undrained second `Popen(` fails, and a
                   tuple-wrapped or `_`-assigned communicate does not qualify
                   (r39 w1 findings 8 F1/F2/F3).
  timeout_state    `fixtures/hang-after-flush.py` under `--tool-timeout 3
                   --arms selftest` yields `C7=unmet` with a `tool_timeout` reason,
                   never `C7=met`, never a silent pass.
  scratch          every `tempfile.mkdtemp(` in every counter passes `dir=` and the
                   counter carries a scratch parent under
                   `.ufo/waves/round-40/scratch`.
  selftest_conjunct per counter: the counter's communicates all carry timeouts,
                   stripping each communicate timeout one at a time is detected
                   by that same rule, and the checker source proves its selftest
                   loop applies and compares each mutation arm.

`--selftest` applies fourteen textual mutations to copies of the first counter
and requires each mutation to flip exactly its expected check to FAIL, then
audits three committed fixture counters under `.ufo/waves/round-42/fixtures/`:
the two sound-binding fixtures must pass every check, and the source-order
fixture must fail exactly `timeout_scope` with the source-order-first reason
(the fallback sweep records the comprehension target at the earlier line, so
a checker that drops the event ordering reports a different first reason).

Exit: 0 met, 1 unmet, 2 setup error.
"""
import argparse
import ast
import inspect
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
DEFAULT_COUNTERS = [os.path.join(LANE, ".ufo/waves/round-40/count-c8.py")]
# The counter's predicate of record is frozen in the round-39 contract
# (P-C7); the round-40 contract carries P-C10/P-C11 for the new instruments.
DEFAULT_CONTRACT = os.path.join(LANE, ".ufo/waves/round-39/contract.md")
FIXTURE_REL = ".ufo/waves/round-39/fixtures/witness-summary-only-live.txt"
HANG_FIXTURE = os.path.join(LANE, ".ufo/waves/round-39/fixtures/hang-after-flush.py")
CHECK_NAMES = ("predicate", "head_pin", "tool_resolve", "bounded_reads",
               "timeout_scope", "drain_bind", "timeout_state", "scratch",
               "selftest_conjunct")

# The checker's v4 mutation table is applied and compared by selftest.
# A gutted or unwired arm fails the live selftest_conjunct check.
SELFTEST_MUTATION_NAMES = (
    "predicate", "head_pin", "tool_resolve", "bounded_reads", "timeout_scope",
    "timeout_scope_shadow", "timeout_scope_walrus", "timeout_scope_tupleunpack",
    "timeout_scope_deadloop", "drain_bind", "drain_bind_decoy", "timeout_state",
    "scratch", "selftest_conjunct", "timeout_scope_walrus_positive",
    "timeout_scope_tupleunpack_positive", "timeout_scope_source_order",
)

# Mutations whose arm name differs from the check they flip (a second arm for
# an already-covered check); the selftest resolves the expected failing check
# through this map.
MUTATION_CHECK_ALIAS = {
    "timeout_scope_shadow": "timeout_scope",
    "timeout_scope_walrus": "timeout_scope",
    "timeout_scope_tupleunpack": "timeout_scope",
    "timeout_scope_deadloop": "timeout_scope",
    "drain_bind_decoy": "drain_bind",
}

PREDICATE = (
    "P-C10 (round 41): the checker rejects the walrus, tuple/list-unpack, and "
    "empty-loop-rebind timeout survivors by recording function-local "
    "`Assign`/`AnnAssign`, `NamedExpr`, destructuring, and for/with targets in "
    "source order. Unresolved targets, unsupported local stores, and multiple "
    "bindings that do not all resolve to one finite-positive value fail "
    "closed. A `global` read uses the module map only without an in-function "
    "global rebind; nonlocal reads and rebinding fail closed. This is a bounded "
    "AST binding subset, not a full Python control-flow proof. "
    "Each `Popen(` still requires a consumed, same-name `communicate(timeout=…)` "
    "drain. `selftest_conjunct` requires the checker to apply each mutation arm "
    "and compare its failing-check set, not merely keep the table present. "
    "The fourteen-arm selftest includes the three r40 survivor constructions. "
    "`head_pin` reports the live repository HEAD; the `rev` argument scopes "
    "`timeout_state` only, so measurement receipts use a checkout at the "
    "measured commit. The seventeen-arm selftest adds three fixture arms: "
    "`timeout_scope_walrus_positive` and `timeout_scope_tupleunpack_positive` "
    "require the checker to accept a walrus and an element-wise tuple-unpack "
    "binding of a finite-positive timeout (deleting the NamedExpr branch or "
    "the destructuring extraction turns them into false violations), and "
    "`timeout_scope_source_order` pins the first failing-binding reason to "
    "source order (deleting the event ordering swaps which binding event is "
    "reported first)."
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


def _finite_positive(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise Unresolvable("non-numeric constant")
    if isinstance(value, float) and not math.isfinite(value):
        raise Unresolvable("timeout value %r is not finite" % (value,))
    if value <= 0:
        raise Unresolvable("timeout value %r is not positive" % (value,))
    return value


def _timeout_value(node, assign, params):
    """Resolve a timeout= kwarg value to a finite positive number or raise."""
    return _finite_positive(_resolve(node, assign, params))


def _module_assignments(tree):
    """Module-level bindings.

    Returns (unconditional, conditional): names bound by top-level
    Assign/AnnAssign, and names bound anywhere inside a top-level
    if/try/for/while/with body. A name in `conditional` is conditionally
    rebound and fails closed (r39 w1 finding 4 H2).
    """
    unconditional = {}
    conditional = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            unconditional.setdefault(node.targets[0].id, []).append(node.value)
        elif isinstance(node, ast.AnnAssign) \
                and isinstance(node.target, ast.Name) and node.value is not None:
            unconditional.setdefault(node.target.id, []).append(node.value)
        elif isinstance(node, (ast.If, ast.Try, ast.For, ast.While, ast.With)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Assign) and len(sub.targets) == 1 \
                        and isinstance(sub.targets[0], ast.Name):
                    conditional.setdefault(sub.targets[0].id, []).append(sub.value)
                elif isinstance(sub, ast.AnnAssign) \
                        and isinstance(sub.target, ast.Name) \
                        and sub.value is not None:
                    conditional.setdefault(sub.target.id, []).append(sub.value)
    return unconditional, conditional


def _function_scope_nodes(fn):
    """Walk one function block, yielding nested definition nodes but not bodies."""
    def walk(node):
        yield node
        if node is not fn and isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            return
        for child in ast.iter_child_nodes(node):
            yield from walk(child)

    for statement in fn.body:
        yield from walk(statement)


def _name_targets(target, name):
    if isinstance(target, ast.Name):
        if target.id == name:
            yield target
    elif isinstance(target, (ast.Tuple, ast.List)):
        for child in target.elts:
            yield from _name_targets(child, name)
    elif isinstance(target, ast.Starred):
        yield from _name_targets(target.value, name)


def _assignment_values(target, value, name):
    if isinstance(target, ast.Name):
        if target.id == name:
            yield target, value, "value"
        return
    if isinstance(target, ast.Starred):
        for target_name in _name_targets(target, name):
            yield target_name, None, "unresolved starred unpack"
        return
    if not isinstance(target, (ast.Tuple, ast.List)):
        return
    if not list(_name_targets(target, name)):
        return
    if isinstance(value, (ast.Tuple, ast.List)) \
            and len(target.elts) == len(value.elts) \
            and not any(isinstance(child, ast.Starred) for child in target.elts):
        for child, item in zip(target.elts, value.elts):
            yield from _assignment_values(child, item, name)
    else:
        for target_name in _name_targets(target, name):
            yield target_name, None, "unresolved destructuring"


def _function_bindings(fn, name):
    """Return source-ordered binding events for `name` in one function block."""
    events = []
    handled_names = set()

    def add(node, kind, expr=None):
        handled_names.add(id(node))
        events.append((getattr(node, "lineno", fn.lineno),
                       getattr(node, "col_offset", 0), kind, expr))

    nodes = list(_function_scope_nodes(fn))
    for sub in nodes:
        if isinstance(sub, ast.Assign):
            for target in sub.targets:
                for target_name, expr, kind in _assignment_values(
                        target, sub.value, name):
                    add(target_name, kind, expr)
        elif isinstance(sub, ast.AnnAssign):
            for target_name in _name_targets(sub.target, name):
                add(target_name, "value" if sub.value is not None else
                    "annotation-only binding", sub.value)
        elif isinstance(sub, (ast.For, ast.AsyncFor)):
            for target_name in _name_targets(sub.target, name):
                add(target_name, "loop target")
        elif isinstance(sub, (ast.With, ast.AsyncWith)):
            for item in sub.items:
                if item.optional_vars is not None:
                    for target_name in _name_targets(item.optional_vars, name):
                        add(target_name, "with target")
        elif isinstance(sub, ast.AugAssign):
            for target_name in _name_targets(sub.target, name):
                add(target_name, "unsupported augmented assignment")
        elif isinstance(sub, ast.Delete):
            for target in sub.targets:
                for target_name in _name_targets(target, name):
                    add(target_name, "delete binding")
        elif isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if sub.name == name:
                add(sub, "nested definition binding")
        elif isinstance(sub, (ast.Import, ast.ImportFrom)):
            for alias in sub.names:
                bound_name = alias.asname or alias.name.split(".")[0]
                if bound_name == name:
                    add(sub, "import binding")
        elif isinstance(sub, ast.ExceptHandler) and sub.name == name:
            add(sub, "exception target")
        elif isinstance(sub, (ast.MatchAs, ast.MatchStar)) \
                and getattr(sub, "name", None) == name:
            add(sub, "pattern target")
        elif isinstance(sub, ast.MatchMapping) and sub.rest == name:
            add(sub, "pattern target")

    for sub in nodes:
        if isinstance(sub, ast.Name) and sub.id == name \
                and isinstance(sub.ctx, ast.Store) and id(sub) not in handled_names:
            add(sub, "unsupported local store")
    events.sort(key=lambda event: (event[0], event[1]))
    return events


def _global_names(fn):
    names = set()
    for sub in _function_scope_nodes(fn):
        if isinstance(sub, ast.Global):
            names.update(sub.names)
    return names


def _nonlocal_names(fn):
    names = set()
    for sub in _function_scope_nodes(fn):
        if isinstance(sub, ast.Nonlocal):
            names.update(sub.names)
    return names


def _resolve_timeout_name(name, fn, func_params, unconditional, conditional):
    """Resolve a timeout binding conservatively at its function scope."""
    is_global = fn is not None and name in _global_names(fn)
    is_nonlocal = fn is not None and name in _nonlocal_names(fn)
    if is_nonlocal:
        raise Unresolvable("nonlocal binding of %r is outside the resolved scope" % name)
    single = {k: v[-1] for k, v in unconditional.items()}

    def _resolve_value(expr):
        # A Name value resolves in the enclosing (module) scope, so a
        # parameter default or local alias of a conditionally-rebound name
        # still fails closed.
        if isinstance(expr, ast.Name):
            return _resolve_timeout_name(expr.id, None, func_params,
                                         unconditional, conditional)
        return _finite_positive(_resolve(expr, single, {}))

    bindings = _function_bindings(fn, name) if fn is not None else []
    if is_global and bindings:
        raise Unresolvable("function-level global rebinding of %r" % name)
    local_values = [] if (fn is None or is_global) else bindings
    if local_values:
        values = []
        for _, _, kind, expr in local_values:
            if kind != "value":
                raise Unresolvable("name %r has %s" % (name, kind))
            values.append(_resolve_value(expr))
        if all(value == values[0] for value in values[1:]):
            return values[0]
        raise Unresolvable("multiple bindings of %r do not resolve to one value" % name)
    if fn is not None and not is_global:
        params = func_params.get(fn.name, {})
        if name in params and params[name] is not None:
            return _resolve_value(params[name])
    if name in conditional:
        base = None
        if name in unconditional:
            base = _resolve_value(unconditional[name][-1])
        for expr in conditional[name]:
            value = _resolve_value(expr)
            if base is None:
                base = value
            elif value != base:
                raise Unresolvable("name %r is conditionally rebound" % name)
        if base is not None:
            return base
        raise Unresolvable("name %r is conditionally rebound" % name)
    if name in unconditional:
        return _finite_positive(_resolve(unconditional[name][-1], single, {}))
    raise Unresolvable("name %r has no binding" % name)


def _popen_name(popen):
    """The variable name a Popen( result is bound to, or None."""
    parent = getattr(popen, "parent", None)
    if isinstance(parent, ast.Assign) and len(parent.targets) == 1 \
            and isinstance(parent.targets[0], ast.Name):
        return parent.targets[0].id
    return None


def _result_consumed(comm):
    """True when a communicate call's result is actually consumed.

    Assigned to other than `_` (a single name or a tuple/list of names), or
    returned. A bare expression statement, an assignment to `_`, and a result
    wrapped in a discarded tuple do not qualify (r39 w1 finding 8 F2).
    """
    parent = getattr(comm, "parent", None)
    if isinstance(parent, ast.Return):
        return True
    if isinstance(parent, ast.Assign):
        def _usable(target):
            if isinstance(target, ast.Name):
                return target.id != "_"
            if isinstance(target, (ast.Tuple, ast.List)):
                return all(isinstance(e, ast.Name) and e.id != "_"
                           for e in target.elts)
            return False
        return all(_usable(t) for t in parent.targets)
    return False


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
    unconditional, conditional = _module_assignments(tree)

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
            try:
                if isinstance(k.value, ast.Name):
                    _resolve_timeout_name(k.value.id, fn, func_params,
                                          unconditional, conditional)
                else:
                    params = func_params.get(fn.name, {}) if fn else {}
                    _timeout_value(k.value, assign, params)
            except Unresolvable as exc:
                value_violations.append("line %d (%s): %s"
                                        % (node.lineno, name, exc))
            except (ArithmeticError, RecursionError) as exc:
                value_violations.append("line %d (%s): fold error: %s"
                                        % (node.lineno, name, exc))
            except Exception as exc:
                value_violations.append("line %d (%s): fold error: %s"
                                        % (node.lineno, name, exc))
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
        target = _popen_name(popen)
        if target is None:
            drain_violations.append("Popen at line %d result not bound to a "
                                    "named variable" % popen.lineno)
            continue
        fn = enclosing_function(popen)
        qualified = False
        for comm in communicates:
            if enclosing_function(comm) is not fn:
                continue
            func = comm.func
            if not (isinstance(func, ast.Attribute)
                    and func.attr == "communicate"
                    and isinstance(func.value, ast.Name)
                    and func.value.id == target):
                continue
            if not any(k.arg == "timeout" for k in comm.keywords):
                continue
            if not _result_consumed(comm):
                continue
            qualified = True
            break
        if not qualified:
            drain_violations.append(
                "Popen at line %d not drained by a bound, consumed communicate "
                "in its function" % popen.lineno)

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
    }


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
    results["timeout_scope"] = (all_values, "; ".join(detail))

    all_drains = True
    ddetail = []
    for path in counters:
        st = stats.get(path)
        if st is None:
            all_drains = False
            ddetail.append("%s: unreadable" % os.path.basename(path))
            continue
        violations = st["drain_violations"]
        all_drains = all_drains and not violations
        ddetail.append("%s: violations=%s"
                       % (os.path.basename(path), violations))
    results["drain_bind"] = (all_drains, "; ".join(ddetail))

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

    # selftest_conjunct also requires the checker selftest to apply and compare
    # each mutation arm; table presence alone is not sufficient.
    selftest_src = inspect.getsource(selftest)
    mutations_src = inspect.getsource(selftest_mutations)
    apply_compare_ok = _selftest_applies_and_compares(selftest_src)
    conjunct_ok = True
    conjunct_detail = []
    for path in counters:
        base = os.path.basename(path)
        try:
            src = open(path, encoding="utf-8").read()
        except OSError:
            conjunct_ok = False
            conjunct_detail.append("%s: unreadable" % base)
            continue
        entry_live = ("selftest_conjunct" in SELFTEST_MUTATION_NAMES
                      and "CONJUNCT_MUTATION" in mutations_src
                      and "selftest_mutations(source)" in selftest_src
                      and CONJUNCT_MUTATION in selftest_mutations(src)
                      and apply_compare_ok)
        st = stats.get(path) or static_checks(src)
        honest = list(st["comm_violations"])
        strips = detected = 0
        for m in re.finditer(r"communicate\(timeout=[^)]+\)", src):
            strips += 1
            mutant = src[:m.start()] + "communicate()" + src[m.end():]
            try:
                mst = static_checks(mutant)
            except SetupError:
                continue
            if mst["comm_violations"]:
                detected += 1
        anchor_present = CONJUNCT_FIND in src
        ok = (not honest) and strips > 0 and detected == strips \
            and anchor_present and entry_live
        if not ok:
            conjunct_ok = False
        conjunct_detail.append(
            "%s: honest_comm=%s strips=%d detected=%d anchor=%s entry_live=%s"
            % (base, honest, strips, detected, anchor_present, entry_live))
    results["selftest_conjunct"] = (conjunct_ok, "; ".join(conjunct_detail))
    return results


CONJUNCT_FIND = "out, err = proc.communicate(timeout=timeout)"
CONJUNCT_MUTATION = ("selftest_conjunct", CONJUNCT_FIND,
                     "out, err = proc.communicate()",
                     "communicate timeout keyword stripped")

def _selftest_applies_and_compares(source):
    """Require one mutation loop that evaluates each arm and compares its result."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    loops = [node for node in ast.walk(tree)
             if isinstance(node, ast.For) and isinstance(node.iter, ast.Name)
             and node.iter.id == "mutations"]
    if len(loops) != 1:
        return False
    loop = loops[0]
    parents = {}
    for node in ast.walk(loop):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    nodes = list(ast.walk(loop))
    evaluate_calls = [node for node in nodes if isinstance(node, ast.Call)
                      and isinstance(node.func, ast.Name)
                      and node.func.id == "evaluate"]
    if len(evaluate_calls) != 1:
        return False
    evaluate_line = evaluate_calls[0].lineno
    compares = [node for node in nodes if isinstance(node, ast.Compare)
                and isinstance(node.left, ast.Name) and node.left.id == "failing"
                and len(node.ops) == 1 and isinstance(node.ops[0], ast.Eq)
                and len(node.comparators) == 1
                and isinstance(node.comparators[0], ast.List)
                and len(node.comparators[0].elts) == 1
                and isinstance(node.comparators[0].elts[0], ast.Name)
                and node.comparators[0].elts[0].id == "want"]
    if not any(node.lineno > evaluate_line for node in compares):
        return False
    aliases = [node for node in nodes if isinstance(node, ast.Call)
               and isinstance(node.func, ast.Attribute)
               and node.func.attr == "get"
               and isinstance(node.func.value, ast.Name)
               and node.func.value.id == "MUTATION_CHECK_ALIAS"
               and len(node.args) == 2
               and all(isinstance(arg, ast.Name) and arg.id == "name"
                       for arg in node.args)]
    if not aliases:
        return False
    for node in nodes:
        if isinstance(node, (ast.Break, ast.Return)):
            return False
        if not isinstance(node, ast.Continue):
            continue
        child = node
        guard = None
        while child in parents:
            parent = parents[child]
            if parent is loop:
                break
            if isinstance(parent, ast.If):
                test = parent.test
                if (isinstance(test, ast.Compare)
                        and isinstance(test.left, ast.Name) and test.left.id == "old"
                        and len(test.ops) == 1 and isinstance(test.ops[0], ast.NotIn)
                        and len(test.comparators) == 1
                        and isinstance(test.comparators[0], ast.Name)
                        and test.comparators[0].id == "source"):
                    guard = parent
                    break
            child = parent
        if guard is None or guard.lineno >= evaluate_line:
            return False
        child = node
        while parents.get(child) is not guard:
            child = parents[child]
        if child not in guard.body:
            return False
    return True


def selftest_mutations(source):
    """Fourteen-mutation table for the round-41 checker (v4).

    Built from the counter bytes so the drain_bind block anchors are exact.
    The conjunct check verifies that selftest applies and compares this table.
    """
    drain_old = drain_new = ""
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
    run_comm = "        out, err = proc.communicate(timeout=timeout)\n"
    tool_popen = (
        "    proc = subprocess.Popen([sys.executable, tool] + list(args),\n"
        "                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,"
        " text=True,\n"
        "                            start_new_session=True)\n"
        "    try:\n"
        + run_comm)
    decoy_new = (
        "    proc = subprocess.Popen([sys.executable, tool] + list(args),\n"
        "                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,"
        " text=True,\n"
        "                            start_new_session=True)\n"
        "    try:\n"
        "        dummy = subprocess.Popen([sys.executable, \"-c\", \"pass\"],"
        " stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n"
        "        dummy_out, dummy_err = dummy.communicate(timeout=timeout)\n"
        "        proc.wait(timeout=timeout)\n"
        "        out, err = proc.stdout.read(), proc.stderr.read()\n")
    run_signature = "def run(cmd, cwd=None, timeout=GIT_TIMEOUT_S, env=None):\n"
    return [
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
        ("timeout_scope", "GIT_TIMEOUT_S = 120", "GIT_TIMEOUT_S = None",
         "timeout value replaced with None"),
        ("timeout_scope_shadow", run_comm,
         "        TIMEOUT = None\n"
         "        out, err = proc.communicate(timeout=TIMEOUT)\n",
         "function-local None shadow inserted"),
        ("timeout_scope_walrus", run_signature,
         run_signature + "    (timeout := None)\n",
         "walrus timeout binding to None"),
        ("timeout_scope_tupleunpack", run_signature,
         run_signature + "    timeout, _dead_unpack = None, None\n",
         "tuple-unpacked timeout binding to None"),
        ("timeout_scope_deadloop", run_signature,
         run_signature + "    timeout = None\n"
         "    for _dead_rebind in ():\n"
         "        timeout = GIT_TIMEOUT_S\n",
         "dead-loop rebind must not outrank the source-ordered binding"),
        ("drain_bind", drain_old, drain_new,
         "communicate drains replaced by wait+read"),
        ("drain_bind_decoy", tool_popen, decoy_new,
         "decoy used communicate beside a wait+read drain"),
        ("timeout_state", "proc = run_tool(args.tool, [\"--selftest\"], args.tool_timeout)",
         "proc = run_tool(args.tool, [\"--selftest\"], TOOL_TIMEOUT_S)",
         "budget flag ignored"),
        ("scratch",
         'SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-39", "scratch")',
         'SCRATCH_ROOT = "/tmp/mori-r39-scratch"', "scratch parent moved off-lane"),
        CONJUNCT_MUTATION,
    ]


def selftest(repo, rev, counter, contract_path):
    """Apply fourteen counter mutations, then three fixture-arm audits, in a
    repository-local scratch tree: seventeen arms, one line each."""
    source = open(counter, encoding="utf-8").read()
    mutations = selftest_mutations(source)
    scratch_root = os.path.join(repo, ".ufo", "waves", "round-41", "scratch")
    os.makedirs(scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=scratch_root)
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
            want = MUTATION_CHECK_ALIAS.get(name, name)
            if failing == [want]:
                passed += 1
                print("PASS %-18s %s -> only %s failed" % (name, why, want))
            else:
                failed += 1
                print("FAIL %-18s %s -> failing=%s (want [%s])"
                      % (name, why, failing, want))
        fixture_arms = (
            ("timeout_scope_walrus_positive", "counter-walrus-positive.py",
             "A walrus binding of a finite-positive timeout must pass"),
            ("timeout_scope_tupleunpack_positive",
             "counter-tupleunpack-positive.py",
             "A sound element-wise tuple-unpack timeout binding must pass"),
            ("timeout_scope_source_order", "counter-source-order.py",
             "The source-order fixture fails exactly timeout_scope with the"
             " comprehension target reported first"),
        )
        fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "fixtures")
        for name, fixture, why in fixture_arms:
            path = os.path.join(fixtures_dir, fixture)
            if not os.path.isfile(path):
                print("FAIL %-30s fixture absent (%s)" % (name, why))
                failed += 1
                continue
            results = evaluate(repo, rev, [path], contract_path)
            failing = sorted(k for k, (ok, _) in results.items() if not ok)
            if name == "timeout_scope_source_order":
                detail = results.get("timeout_scope", (False, ""))[1]
                ok = (failing == ["timeout_scope"]
                      and "unsupported local store" in detail)
            else:
                ok = not failing
            if ok:
                passed += 1
                print("PASS %-30s %s" % (name, why))
            else:
                failed += 1
                print("FAIL %-30s %s -> failing=%s" % (name, why, failing))
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
