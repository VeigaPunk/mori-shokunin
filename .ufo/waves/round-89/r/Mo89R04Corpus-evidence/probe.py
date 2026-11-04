"""Mo89R04Corpus probe: repaired gate comment rule vs POSIX 2.3 shells vs shlex."""
import importlib.util, json, os, shlex, subprocess, sys

spec = importlib.util.spec_from_file_location("gate", sys.argv[1])
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

BB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "busybox")
SHELLS = {"bash": ["bash"], "sh(bash-posix)": ["sh"], "busybox-ash": [BB, "ash"]}
CASES = [
    "a#b c", "a #b c", "a;#b c", "a&&#b c", "a|#b c", "'a'#b c", "a\\#b c",
    "\"a #b\" c", "a\\ #b c", "$(echo a)#b c", "a >#b c", "(echo a)#b", "x=1#b c",
    "a\t#b c", "a ${#x} c",
]
for c in CASES:
    row = {"cmd": c}
    try:
        row["shlex_split_comments"] = shlex.split(c, comments=True)
    except ValueError as e:
        row["shlex_split_comments"] = f"ValueError:{e}"
    row["gate_strip_comment"] = gate.strip_comment(c)
    for name, argv in SHELLS.items():
        p = subprocess.run(argv + ["-c", "printf '<%s>' " + c + "; echo"],
                           capture_output=True, text=True)
        row[name] = (p.stdout.strip(), p.returncode, p.stderr.strip()[:80])
    print(json.dumps(row, ensure_ascii=False))

print("--- -c operand probe (is the operand after the -c string $0, and executed?)")
for name, argv in SHELLS.items():
    p = subprocess.run(argv + ["-c", 'echo "zero=$0 one=$1"', "tools/x.py", "arg1"],
                       capture_output=True, text=True)
    print(name, repr(p.stdout.strip()), p.returncode)
p = subprocess.run([sys.executable, "-I", "-c", "import sys;print(sys.argv)", "tools/x.py", "y"],
                   capture_output=True, text=True)
print("python -c argv", p.stdout.strip(), p.returncode)

print("--- gate executed_scripts")
for c in ["bash -c 'printf BODY' tools/x.py", "sh -c 'python3 tools/x.py'",
          "python3 -c 'print(1)' tools/x.py", "printf BODY # tools/x.py",
          "printf BODY #tools/x.py", "printf BODY;#tools/x.py", "printf BODY#; python3 tools/x.py",
          "echo $(true)#; python3 tools/x.py", "echo a >#x; python3 tools/x.py",
          "false && python3 tools/x.py; printf BODY",
          "uv run --directory sub tools/x.py"]:
    print(repr(c), "->", gate.executed_scripts(c))
