# Exec6 — mori round 43 / w1

Seat: Exec6 (leaf, no descendants). Assigned move: run the frozen-counter
AST-introspection command and paste its output. Read-only; no production file
edited; nothing run outside the seat except this exact command.

## Command (verbatim, cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`)

```
python3 -c "import ast; t=ast.parse(open('.ufo/waves/round-42/count-c1.py').read()); print([ (n.name,[a.arg for a in n.args.args]) for n in ast.walk(t) if isinstance(n, ast.FunctionDef) and n.name=='run'])"
```

## stdout

```
[('run', ['argv', 'timeout'])]
```

## stderr

```
(empty — no stderr output)
```

## exit code

```
EXIT_CODE=0
```

(Executed with `; echo "EXIT_CODE=$?"` appended to capture the code explicitly
without altering the command's own stdout/stderr; wall time 0.016 s.)

## Scoped findings

- Target `.ufo/waves/round-42/count-c1.py` (frozen, never touched) defines
  exactly one function named `run`; its positional parameter list is
  `['argv', 'timeout']`.
- AST parse of the frozen bytes succeeded with no SyntaxError — the frozen
  counter remains valid Python and machine-introspectable.
- Signature cross-check against a direct Read of the file (lines 93–95):
  `def run(argv, timeout=900):` → `subprocess.run(argv, capture_output=True,
  text=True, timeout=timeout)` returning `(returncode, stdout, stderr)`. The
  introspected tuple matches the source exactly. This `run` helper backs every
  subprocess in the C1 counter (`selftest`, `routed_four`, gate selftest) and
  defaults to a 900 s timeout — two positionals only, no kw-only params.
- No mutation: lane Git index, jj state, `.ufo/state`, `.ufo/watchdog.log`, and
  the three frozen counters were untouched; nothing executed in the lane tree
  beyond `ast.parse`/`print` on the frozen bytes.

## Evidence

| Item | Value |
| --- | --- |
| Command output | `[('run', ['argv', 'timeout'])]` |
| Exit code | 0 |
| File inspected | `.ufo/waves/round-42/count-c1.py` (read-only, 258 lines) |
| Runs performed in lane | 1 (pure `ast.parse` + `print`, no subprocess, no writes) |

## Remaining risks

- None introduced by this seat. The signature is stable across the round;
  any v2 attack that swaps `run`'s arity would be visible to the same
  one-liner.

## Blockers

- None.

Report: .ufo/waves/round-43/w1/Exec6.md
