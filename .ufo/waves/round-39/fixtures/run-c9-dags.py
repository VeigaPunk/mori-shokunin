#!/usr/bin/env python3
"""Round-39 C9 receipts: run a given gate script on the committed DAG fixtures
(the same fixtures the gate selftest builds) and print its verdict lines.

Usage: run-c9-dags.py <gate-script> <lane-repo> <out.txt> [--round-base-name NAME]

Runs fixture A with --round-base b0 and fixture C with --round-base c1, exactly
as the gate selftest does. The out file records the command, both verdict
blocks and the exit codes, so the round-38 gate bytes (extracted via
`git show 13f3db7e:tools/mori-sources-appendonly.py`) and the round-39 gate
bytes produce comparable red/after receipts.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile


def load_gate(lane):
    spec = importlib.util.spec_from_file_location(
        "gate", os.path.join(lane, "tools", "mori-sources-appendonly.py"))
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    return gate


def main(argv):
    gate_script = os.path.abspath(argv[1])
    lane = os.path.abspath(argv[2])
    out_path = os.path.abspath(argv[3])
    gate = load_gate(lane)
    env = gate._selftest_env()
    root = tempfile.mkdtemp(prefix="mori-r39-dags-")
    lines = ["command: python3 .ufo/waves/round-39/fixtures/run-c9-dags.py %s %s %s"
             % (os.path.relpath(gate_script, lane), lane, out_path)]
    try:
        dag_cases, dag_bodies = gate._selftest_dag_cases()
        for offset, (name, kind, _exit, _expected, base_name) in enumerate(
                dag_cases):
            repo = os.path.join(root, "dag%02d" % offset)
            shas = gate._make_dag_repo(repo, kind, dag_bodies, env)
            proc = subprocess.run(
                [sys.executable, gate_script, "HEAD", "--repo", repo,
                 "--round-base", shas[base_name]],
                capture_output=True, text=True, timeout=180, env=env)
            lines.append("")
            lines.append("== %s (%s, --round-base %s=%s)"
                         % (name, kind, base_name, shas[base_name][:12]))
            lines.extend(proc.stdout.splitlines())
            lines.append("EXIT=%d" % proc.returncode)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
