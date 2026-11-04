#!/usr/bin/env python3
"""Mo89R01C1 attack driver: grade custom receipts through the r87 gate's own grade_population.

Usage: grade_cases.py <gate_file> <repo_clone> <rev> <scratch> <cases_json> <out_jsonl>
Each case: {"name": str, "cmd": str, "expect": "met"|"reject"}
Receipt body = real stdout of the command at rev (run in a --shared clone), so the verdict
isolates the binding rule; the replay outcome is reported separately.
"""
import importlib.util, json, os, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
gate_file, repo, rev, scratch, cases_path, out_path = sys.argv[1:7]
spec = importlib.util.spec_from_file_location("gate_under_test", gate_file)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

PIN = ".ufo/waves/round-82/record-pins.json"
BOUND = "tools/mori-record-sweep.py"
sha = gate.sha256_at(repo, rev, BOUND)
assert sha, "bound path missing at rev"
cases = json.load(open(cases_path))
results = []
for case in cases:
    name, cmd = case["name"], case["cmd"]
    work = tempfile.mkdtemp(dir=scratch, prefix="case-")
    # 1) real stdout of the command in a clone at rev (what a genuine replay prints)
    rc0, out0, _ = gate.replay_body(repo, rev, cmd, work, "clone")
    body = out0.rstrip("\n")
    token = body.split()[0] if body else "NOBODY"
    receipt = ("# receipt: %s.txt\n# cmd: %s\n# rev: %s\n# counter-sha256: %s %s\n"
               "# replay: clone\n# limits: named limit body is stdout in a clone\n# ---\n%s\n"
               % (name, cmd, rev, sha, BOUND, body))
    loader = lambda path, r=receipt, n=name + ".txt": r if os.path.basename(path) == n else None
    pop = ((name + ".txt", case["expect"], "clone", token),)
    ok, lines, counts = gate.grade_population(loader, repo, rev, work, pop)
    rline = [l for l in lines if l.startswith("RECEIPT ")][0]
    rep = [l for l in lines if l.startswith("REPLAY ")]
    m = re.search(r"problems=(\S+)$", rline)
    results.append({"name": name, "cmd": cmd, "replay_rc0": rc0,
                    "met": (" met " in rline), "problems": m.group(1) if m else "?",
                    "replay": rep[0] if rep else None, "body": body[:80]})
    shutil.rmtree(work, ignore_errors=True)
with open(out_path, "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")
        print(json.dumps(r))
