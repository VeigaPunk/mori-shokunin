#!/usr/bin/env python3
"""LiveKumitate tool-edge fixtures. Scratch only under /tmp/liveK-fixtures; the lane is never touched.

Runs the settlement tool (read-only) against small synthetic lanes to probe documented behaviour.
"""
import json
import os
import shutil
import subprocess

TOOL = "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py"
B = "/tmp/liveK-fixtures"
BODY = b"Seat report body line\n"


def put(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def disp(tasks):
    doc = {"schema": "ufo-swarm-wave-dispatch-v1", "wave": "fx",
           "taskCall": {"tasks": [{"name": n, "agent": "reviewer",
                                   "task": "Fixture body\nReport: write your scoped findings to " + p}
                                  for n, p in tasks]},
           "registry": {"members": {n: {} for n, _ in tasks}}}
    return json.dumps(doc).encode()


def run(case, lane, fleet=None):
    out = os.path.join(B, "out-%s.json" % case)
    cmd = ["python3", TOOL, "scan", "--lane-root", lane, "--out", out]
    if fleet:
        cmd += ["--fleet-root", fleet]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    summary = {"rc": proc.returncode, "stderr": proc.stderr.strip()[:160]}
    if os.path.exists(out):
        doc = json.load(open(out, encoding="utf-8"))
        summary["totals_waves"] = doc["totals"]["waves"]
        summary["waves"] = [{"path": w["dispatch_path"], "state": w["state"],
                             "counts": {k: v for k, v in w["counts"].items() if v},
                             "missing": w["missing"]} for w in doc["waves"]]
    return summary


def main():
    if os.path.lexists(B):
        try:
            os.chmod(os.path.join(B, "C/lane/reports"), 0o755)
        except OSError:
            pass
        shutil.rmtree(B)
    os.makedirs(B)
    res = {"uid": os.getuid()}

    # A0: no .ufo/waves tree at all.
    a0 = os.path.join(B, "A0/lane")
    os.makedirs(a0)
    res["A0_no_waves_tree"] = run("A0", a0)

    # A1: .ufo/waves is a symlink to a real dispatch tree holding one unsettled wave.
    a1 = os.path.join(B, "A1/lane")
    os.makedirs(os.path.join(a1, ".ufo"))
    put(os.path.join(B, "A1/real-waves/round-1/fx-dispatch.json"),
        disp([("SeatMissing", ".ufo/waves/round-1/fx/SeatMissing.md")]))
    os.symlink(os.path.join(B, "A1/real-waves"), os.path.join(a1, ".ufo", "waves"))
    res["A1_waves_symlink_unsettled"] = run("A1", a1)

    # B: report parent is a symlink that escapes the lane (contract: unsafe, never read).
    bl = os.path.join(B, "B/lane")
    put(os.path.join(B, "B/outside/Seat1.md"), BODY)
    put(os.path.join(bl, ".ufo/waves/round-1/fx-dispatch.json"),
        disp([("Seat1", ".ufo/waves/round-1/fx/Seat1.md")]))
    os.symlink(os.path.join(B, "B/outside"), os.path.join(bl, ".ufo/waves/round-1/fx"))
    res["B_symlink_parent_escape"] = run("B", bl)

    # C: report outside .ufo/waves under an unreadable parent (EACCES on lstat).
    cl = os.path.join(B, "C/lane")
    put(os.path.join(cl, ".ufo/waves/round-1/fx-dispatch.json"), disp([("Seat1", "reports/Seat1.md")]))
    put(os.path.join(cl, "reports/Seat1.md"), BODY)
    os.chmod(os.path.join(cl, "reports"), 0o600)
    res["C_eacces_parent_outside_waves"] = run("C", cl)
    os.chmod(os.path.join(cl, "reports"), 0o755)

    # F: positive control: absent in lane, present at the same relative path under the fleet root.
    fl, ff = os.path.join(B, "F/lane"), os.path.join(B, "F/fleet")
    put(os.path.join(fl, ".ufo/waves/round-1/fx-dispatch.json"), disp([("Seat1", ".ufo/waves/round-1/fx/Seat1.md")]))
    put(os.path.join(ff, ".ufo/waves/round-1/fx/Seat1.md"), BODY)
    res["F_misrooted_positive_control"] = run("F", fl, ff)

    print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
