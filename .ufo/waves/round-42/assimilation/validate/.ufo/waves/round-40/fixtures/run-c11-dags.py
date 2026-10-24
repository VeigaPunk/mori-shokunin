#!/usr/bin/env python3
"""Round-40 C11 receipts: run a given gate script on the three P-C11 DAG
fixtures (never-edited superseded row, first-parent-lacks-path merge, linear
delete-then-re-add) and print its verdict lines.

Usage: run-c11-dags.py <gate-script> <lane-repo> <out.txt> [kind ...]

Builds only the round-40 P-C11 fixture kinds (dag-n, dag-p, dag-r) using the
landed gate module's builders, then runs the given gate SCRIPT (round-39 v2
bytes extracted via `git show bb1f2457:...`, or the round-40 v3 bytes) against
each through real subprocesses. The out file records the command, each verdict
block and the exit code, so the v2 and v3 bytes produce comparable receipts.
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

P11_KINDS = ("dag-n", "dag-p", "dag-r")


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
    kinds = argv[4:] or list(P11_KINDS)
    gate = load_gate(lane)
    env = gate._selftest_env()
    root = tempfile.mkdtemp(prefix="mori-r40-dags-", dir=os.path.join(lane, ".scratch"))
    lines = ["command: python3 .ufo/waves/round-40/fixtures/run-c11-dags.py %s %s %s %s"
             % (os.path.relpath(gate_script, lane), lane, out_path,
                " ".join(kinds))]
    try:
        dag_cases, dag_bodies = gate._selftest_dag_cases()
        for offset, (name, kind, _exit, _expected, base_name) in enumerate(
                dag_cases):
            if kind not in kinds:
                continue
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
            if proc.stderr.strip():
                lines.append("STDERR: " + proc.stderr.strip())
            lines.append("EXIT=%d" % proc.returncode)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
