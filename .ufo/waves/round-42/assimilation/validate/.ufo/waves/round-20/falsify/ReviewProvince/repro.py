#!/usr/bin/env python3
"""ReviewProvince reproduction: blind-spot fixtures for tools/mori-wave-settlement.py.

Read-only against the lane: the tool is only run with `scan` (stdout) and `--selftest`.
Every fixture is written under /tmp/rp-r20-repro. Run: python3 <this file>
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
TOOL = os.path.join(LANE, "tools", "mori-wave-settlement.py")
BASE = "/tmp/rp-r20-repro"
DISP = "ufo-swarm-wave-dispatch-v1"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as stream:
        stream.write(text)


def dispatch(path, doc):
    write(path, json.dumps(doc))


def task(name, report=None):
    body = "Fixture task"
    if report:
        body += "\nReport: write your scoped findings to " + report
    return {"name": name, "agent": "reviewer", "task": body}


def scan(lane, fleet=None):
    cmd = [sys.executable, TOOL, "scan", "--lane-root", lane]
    if fleet:
        cmd += ["--fleet-root", fleet]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    doc = json.loads(proc.stdout)
    return proc.returncode, doc


def show(label, lane, fleet=None):
    rc, doc = scan(lane, fleet)
    print(f"== {label}: rc={rc}")
    print("   totals:", {k: doc["totals"][k] for k in ("waves", "members", "states")},
          "ignored_json=", doc["ignored_json"], "unreadable_json=", doc["unreadable_json"])
    for wave in doc["waves"]:
        print("   wave:", wave["dispatch_path"], "state=", wave["state"],
              "members=", [(m["name"], m["status"]) for m in wave["members"]])


def main():
    shutil.rmtree(BASE, ignore_errors=True)

    # A: resume-only wave; the resume member's message carries a Report trailer
    a = BASE + "/A/lane"
    dispatch(a + "/.ufo/waves/w-resume/dispatch.json", {
        "schema": DISP, "wave": "w-resume", "taskCall": None,
        "resumeSends": [{"name": "SwarmResume01", "resume": "agent-abc", "member": "ReviewerA",
                         "message": "Continue.\nReport: write your scoped findings to "
                                    ".ufo/waves/round-1/build/ReviewerA.md"}]})
    show("A resume-only, resume member never reports", a)

    # B: mixed wave; spawn member reported, resume member never reports
    b = BASE + "/B/lane"
    dispatch(b + "/.ufo/waves/w-mixed/dispatch.json", {
        "schema": DISP, "wave": "w-mixed",
        "taskCall": {"context": "c", "tasks": [task("SpawnA", ".ufo/waves/round-1/build/SpawnA.md")]},
        "resumeSends": [{"name": "SwarmResume02", "resume": "agent-xyz", "member": "ReviewerB",
                         "message": "Continue.\nReport: write your scoped findings to "
                                    ".ufo/waves/round-1/build/ReviewerB.md"}]})
    write(b + "/.ufo/waves/round-1/build/SpawnA.md", "report A\n")
    show("B mixed wave, resume member never reports", b)

    # C: .ufo/waves is a symlink to a directory holding an unsettled wave
    c = BASE + "/C/lane"
    dispatch(BASE + "/C/hidden-waves/w-hidden/dispatch.json", {
        "schema": DISP, "wave": "w-hidden",
        "taskCall": {"context": "c", "tasks": [task("H1", ".ufo/waves/round-1/build/H1.md"),
                                               task("H2", ".ufo/waves/round-1/build/H2.md")]}})
    os.makedirs(c + "/.ufo", exist_ok=True)
    os.symlink(BASE + "/C/hidden-waves", c + "/.ufo/waves")
    show("C .ufo/waves is a symlink", c)

    # D: lane with no .ufo/waves at all
    write(BASE + "/D/lane/README", "no waves\n")
    show("D no .ufo/waves", BASE + "/D/lane")

    # E: the only dispatch-schema file is truncated JSON
    write(BASE + "/E/lane/.ufo/waves/w-bad/dispatch.json",
          '{"schema": "ufo-swarm-wave-dispatch-v1", "wave": "x", "taskCall": ')
    show("E only malformed dispatch file", BASE + "/E/lane")

    # F: settled wave plus an undispatched-named preview payload
    f = BASE + "/F/lane"
    dispatch(f + "/.ufo/waves/w-ok/dispatch.json", {
        "schema": DISP, "wave": "w-ok",
        "taskCall": {"context": "c", "tasks": [task("OkA", ".ufo/waves/round-1/build/OkA.md")]}})
    write(f + "/.ufo/waves/round-1/build/OkA.md", "ok\n")
    dispatch(f + "/.ufo/waves/w-preview/undispatched-preview.json", {
        "schema": DISP, "wave": "w-preview",
        "taskCall": {"context": "c", "tasks": [task("PvA", ".ufo/waves/round-1/build/PvA.md")]}})
    show("F settled wave + undispatched preview payload", f)

    # G / G2: misrooted is an existence test under --fleet-root (size and owner unchecked)
    g = BASE + "/G/lane"
    dispatch(g + "/.ufo/waves/w-g/dispatch.json", {
        "schema": DISP, "wave": "w-g",
        "taskCall": {"context": "c", "tasks": [task("GSeat", ".ufo/waves/round-1/build/GSeat.md")]}})
    write(BASE + "/G/fleet/.ufo/waves/round-1/build/GSeat.md", "")
    show("G fleet-root same-path file, 0 bytes", g, BASE + "/G/fleet")
    write(BASE + "/G2/fleet/.ufo/waves/round-1/build/GSeat.md", "an unrelated fleet note\n")
    shutil.copytree(BASE + "/G/lane/.ufo", BASE + "/G2/lane/.ufo")
    show("G2 fleet-root same-path file, unrelated content", BASE + "/G2/lane", BASE + "/G2/fleet")

    # H: a member name containing a state-vocabulary word
    h = BASE + "/H/lane"
    dispatch(h + "/.ufo/waves/w-h/dispatch.json", {
        "schema": DISP, "wave": "w-h",
        "taskCall": {"context": "c", "tasks": [task("dead-seat", ".ufo/waves/round-1/build/DeadSeat.md")]}})
    proc = subprocess.run([sys.executable, TOOL, "scan", "--lane-root", h],
                          capture_output=True, text=True, timeout=60)
    print(f"== H member named dead-seat: rc={proc.returncode} output contains 'dead': {'dead' in proc.stdout}")

    # I: upstream schema bump on an unsettled wave
    i = BASE + "/I/lane"
    dispatch(i + "/.ufo/waves/w-v2/dispatch.json", {
        "schema": "ufo-swarm-wave-dispatch-v2", "wave": "w-v2",
        "taskCall": {"context": "c", "tasks": [task("X1", ".ufo/waves/round-1/build/X1.md")]}})
    show("I schema v2 bump, unsettled wave", i)

    # J: upstream trailer wording drift
    j = BASE + "/J/lane"
    dispatch(j + "/.ufo/waves/w-tr/dispatch.json", {
        "schema": DISP, "wave": "w-tr",
        "taskCall": {"context": "c", "tasks": [{"name": "Y1", "agent": "reviewer",
                                                "task": "t\nReport: write findings to .ufo/waves/round-1/build/Y1.md"}]}})
    show("J trailer wording drift", j)

    # K: a wave directory that is itself a symlink
    k = BASE + "/K/lane"
    dispatch(BASE + "/K/elsewhere/w-link/dispatch.json", {
        "schema": DISP, "wave": "w-link",
        "taskCall": {"context": "c", "tasks": [task("Z1", ".ufo/waves/round-1/build/Z1.md")]}})
    os.makedirs(k + "/.ufo/waves", exist_ok=True)
    os.symlink(BASE + "/K/elsewhere/w-link", k + "/.ufo/waves/w-link")
    show("K wave directory is a symlink", k)

    # Repo selftest and independent oracle, outputs confined to /tmp
    tmp = BASE + "/tmp"
    os.makedirs(tmp, exist_ok=True)
    st = subprocess.run([sys.executable, TOOL, "--selftest"], capture_output=True, text=True,
                        env={**os.environ, "TMPDIR": tmp}, timeout=600)
    print("selftest rc:", st.returncode, "|", st.stdout.strip()[-120:])
    orc = subprocess.run([sys.executable, LANE + "/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py",
                          "--tool", "tools/mori-wave-settlement.py", "--out", BASE + "/c2.json"],
                         cwd=LANE, capture_output=True, text=True, timeout=600)
    print("oracle rc:", orc.returncode)
    if os.path.exists(BASE + "/c2.json"):
        print("oracle counts:", json.load(open(BASE + "/c2.json")).get("counts"))
    print("tool sha256:", hashlib.sha256(open(TOOL, "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
