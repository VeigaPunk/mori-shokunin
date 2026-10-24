#!/usr/bin/env python3
"""Run the r41 controls and claim counters in a disposable Git sandbox.

Usage: python3 .ufo/waves/round-41/fixtures/run-r41-controls.py before|after REV
The before run anchors to the entering r40 commit and copies only the frozen
r41 fixtures into that sandbox; the after run reads the committed r41 tree.
"""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
BASE = "62a207f7521fa2e2fcd2e8b0260f047ccfce8862"
REFERENCE = BASE
RUNNER_REL = ".ufo/waves/round-41/fixtures/run-r41-controls.py"
BUILDER_REL = ".ufo/waves/round-41/fixtures/c2/build-dags-r40.py"
CALIBRATION_REL = "tools/mori-round41-calibration.py"
C1_FIXTURE_REL = ".ufo/waves/round-41/fixtures/c1"
C1_EXTRACTED_REL = ".ufo/waves/round-41/fixtures/extracted/conform-v3-r40.py"


def clean_env(extra=None):
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CONFIG_GLOBAL",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                "GIT_COMMON_DIR"):
        env.pop(key, None)
    if extra:
        env.update(extra)
    return env


def run(argv, env, cwd=None, timeout=300):
    proc = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                         text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def ensure_parent(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def copy_file(source, target):
    ensure_parent(target)
    shutil.copy2(source, target)


def copy_tree(source, target):
    if os.path.isdir(source):
        shutil.copytree(source, target, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    else:
        raise RuntimeError("missing fixture tree: " + source)


def record(lines, label, argv, code, stdout, stderr):
    lines.append("## %s" % label)
    lines.append("command: " + " ".join(argv))
    lines.append("EXIT=%d" % code)
    if stdout:
        lines.append(stdout.rstrip())
    if stderr.strip():
        lines.append("STDERR: " + stderr.rstrip())
    lines.append("")


def load_builder(path, repo):
    spec = importlib.util.spec_from_file_location("r40_dag_builder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.LANE = repo
    module.GATE_V3 = os.path.join(repo, "tools", "mori-sources-appendonly.py")
    module.ROOT = os.path.join(repo, ".scratch-r41")
    gate_spec = importlib.util.spec_from_file_location("r41_sandbox_gate",
                                                       module.GATE_V3)
    gate = importlib.util.module_from_spec(gate_spec)
    gate_spec.loader.exec_module(gate)
    module.gate = gate
    module._row = gate._row
    module._render = gate._render
    module.COL = gate.COLUMNS
    return module


def c1_section(mode, repo, rev, env, lines):
    if mode == "before":
        checker = os.path.join(repo, ".ufo/waves/round-40/conform.py")
        counter = os.path.join(repo, ".ufo/waves/round-40/count-c8.py")
        contract = os.path.join(repo, ".ufo/waves/round-39/contract.md")
        fixtures = [
            ("walrus", os.path.join(repo, C1_FIXTURE_REL, "survivor-walrus-none.py")),
            ("tupleunpack", os.path.join(repo, C1_FIXTURE_REL, "survivor-tupleunpack-none.py")),
            ("deadloop", os.path.join(repo, C1_FIXTURE_REL, "survivor-deadloop-rebind.py")),
        ]
        # v3's byte-frozen extracted copy is the control instrument.
        extracted = os.path.join(repo, C1_EXTRACTED_REL)
        if os.path.isfile(extracted):
            checker = extracted
    else:
        checker = os.path.join(repo, ".ufo/waves/round-41/conform.py")
        counter = os.path.join(repo, C1_FIXTURE_REL, "count-c8.py")
        contract = os.path.join(repo, ".ufo/waves/round-39/contract.md")
        fixtures = [
            ("walrus", os.path.join(repo, C1_FIXTURE_REL, "survivor-walrus-none.py")),
            ("tupleunpack", os.path.join(repo, C1_FIXTURE_REL, "survivor-tupleunpack-none.py")),
            ("deadloop", os.path.join(repo, C1_FIXTURE_REL, "survivor-deadloop-rebind.py")),
        ]
    args = [sys.executable, checker, rev, "--repo", repo, "--contract", contract]
    code, stdout, stderr = run(args + ["--counter", counter], env)
    record(lines, "C1 %s honest counter" % mode, args + ["--counter", counter],
           code, stdout, stderr)
    for name, fixture in fixtures:
        cmd = args + ["--counter", fixture]
        code, stdout, stderr = run(cmd, env)
        record(lines, "C1 %s survivor %s" % (mode, name), cmd,
               code, stdout, stderr)
    if mode == "after":
        cmd = [sys.executable, checker, rev, "--repo", repo,
               "--contract", contract, "--counter", counter, "--selftest"]
        code, stdout, stderr = run(cmd, env, timeout=600)
        record(lines, "C1 after selftest", cmd, code, stdout, stderr)

        # The early-continue mutant must make selftest_conjunct fail.
        source = open(checker, encoding="utf-8").read()
        anchor = "        for name, old, new, why in mutations:\n"
        if source.count(anchor) != 1:
            raise RuntimeError("selftest mutation-loop anchor is not unique")
        mutant = os.path.join(repo, ".scratch-r41", "conform-early-continue.py")
        os.makedirs(os.path.dirname(mutant), exist_ok=True)
        with open(mutant, "w", encoding="utf-8") as handle:
            handle.write(source.replace(anchor, anchor + "            continue\n", 1))
        cmd = [sys.executable, mutant, rev, "--repo", repo,
               "--contract", contract, "--counter", counter]
        code, stdout, stderr = run(cmd, env)
        record(lines, "C1 after early-continue mutant", cmd, code, stdout, stderr)


def c2_section(mode, repo, rev, env, lines):
    gate = os.path.join(repo, "tools/mori-sources-appendonly.py")
    cmd = [sys.executable, gate, "--selftest"]
    code, stdout, stderr = run(cmd, env, timeout=1200)
    record(lines, "C2 %s selftest" % mode, cmd, code, stdout, stderr)

    cmd = [sys.executable, gate, rev, "--repo", repo]
    code, stdout, stderr = run(cmd, env, timeout=300)
    record(lines, "C2 %s lane line" % mode, cmd, code, stdout, stderr)
    if mode == "after":
        cmd = [sys.executable, gate, "e37dcc6", "--repo", repo]
        code, stdout, stderr = run(cmd, env, timeout=300)
        record(lines, "C2 after e37dcc6", cmd, code, stdout, stderr)

    builder = load_builder(os.path.join(repo, BUILDER_REL), repo)
    cases = [
        ("dag-h", builder.build_dag_h, "m", "b0"),
        ("dag-h2", builder.build_dag_h2, "s2", "b0"),
        ("dag-z", builder.build_dag_z, "m", "b0"),
        ("dag-z2", builder.build_dag_z2, "m", "b0"),
        ("dag-2l-early", builder.build_dag_2l_early, "m", "b0"),
        ("dag-2l-late", builder.build_dag_2l_late, "m", "b0"),
        ("dag-x", builder.build_dag_x, "r2", "b0"),
    ]
    scratch = os.path.join(repo, ".scratch-r41")
    os.makedirs(scratch, exist_ok=True)
    for name, build, tip_name, base_name in cases:
        fixture_repo = os.path.join(scratch, "fixture-" + name)
        if os.path.exists(fixture_repo):
            shutil.rmtree(fixture_repo)
        shas = build(fixture_repo, builder.gate._selftest_env())
        cmd = [sys.executable, gate, shas[tip_name], "--repo", fixture_repo,
               "--round-base", shas[base_name]]
        code, stdout, stderr = run(cmd, env, timeout=300)
        record(lines, "C2 %s %s" % (mode, name), cmd, code, stdout, stderr)
        shutil.rmtree(fixture_repo, ignore_errors=True)


def c3_section(mode, repo, rev, env, lines):
    script = os.path.join(repo, CALIBRATION_REL)
    cmd = [sys.executable, script, rev, "--repo", repo,
           "--reference-rev", REFERENCE]
    code, stdout, stderr = run(cmd, env, timeout=300)
    record(lines, "C3 %s calibration" % mode, cmd, code, stdout, stderr)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("before", "after"))
    parser.add_argument("revision")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    source = LANE
    with tempfile.TemporaryDirectory(prefix="mori-r41-sandbox-") as root:
        clone = os.path.join(root, "repo")
        code, stdout, stderr = run(["git", "clone", "--shared", "--no-checkout", source, clone],
                                   clean_env())
        if code:
            raise SystemExit("sandbox clone failed: " + stderr.strip())
        code, stdout, stderr = run(["git", "-C", clone, "checkout", "--detach", args.revision],
                                   clean_env())
        if code:
            raise SystemExit("sandbox checkout failed: " + stderr.strip())
        if args.mode == "before":
            copy_tree(os.path.join(source, C1_FIXTURE_REL),
                      os.path.join(clone, C1_FIXTURE_REL))
            copy_file(os.path.join(source, C1_EXTRACTED_REL),
                      os.path.join(clone, C1_EXTRACTED_REL))
            copy_file(os.path.join(source, ".ufo/waves/round-41/fixtures/c2/build-dags-r40.py"),
                      os.path.join(clone, BUILDER_REL))
            copy_file(os.path.join(source, CALIBRATION_REL),
                      os.path.join(clone, CALIBRATION_REL))
        sandbox_tmp = os.path.join(clone, ".scratch-r41")
        os.makedirs(sandbox_tmp, exist_ok=True)
        env = clean_env({"TMPDIR": sandbox_tmp})
        lines = ["mode=%s revision=%s" % (args.mode, args.revision),
                 "sandbox=disposable git clone at detached target revision"]
        c1_section(args.mode, clone, args.revision, env, lines)
        c2_section(args.mode, clone, args.revision, env, lines)
        if args.mode == "before":
            c3_section(args.mode, clone, args.revision, env, lines)
        ensure_parent(os.path.abspath(args.output))
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
        print("wrote %s" % os.path.abspath(args.output))
        if args.mode == "before":
            print("C1/C2/C3 baseline controls captured")
        else:
            print("C1/C2 after captured; C3 uses the separate calibration counter")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
