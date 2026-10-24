#!/usr/bin/env python3
"""LiveKumitate extra consistency checks on the kumitate lane. Read-only; stdlib only."""
import hashlib
import json
import os
import re
from collections import defaultdict

LANE = "/home/vgpnk/Projects/shokunin/kumitate-shokunin"
WAVES = os.path.join(LANE, ".ufo", "waves")
IND = "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/LiveKumitate/indep.json"


def load(rel):
    with open(os.path.join(WAVES, rel), "rb") as handle:
        return json.loads(handle.read())


def all_strings(obj, out):
    if isinstance(obj, str):
        out.add(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            all_strings(value, out)
    elif isinstance(obj, list):
        for value in obj:
            all_strings(value, out)
    return out


def main():
    pairs = [("round-35/build-dispatch.json", "round-35/build/swarm-registry.json"),
             ("round-35/falsify-dispatch.json", "round-35/falsify/swarm-registry.json"),
             ("round-36/build-dispatch.json", "round-36/build/swarm-registry.json"),
             ("round-37/falsify-dispatch.json", "round-37/falsify/swarm-registry.json"),
             ("round-38/build-dispatch.json", "round-38/build/swarm-registry.json"),
             ("round-38/falsify-dispatch.json", "round-38/falsify/swarm-registry.json")]
    for disp, reg in pairs:
        tasks = {t["name"] for t in load(disp)["taskCall"]["tasks"]}
        swarm = set(load(reg)["members"].keys())
        print("registry %-32s tasks=%d swarm_registry_names_equal_tasks=%s" % (disp, len(tasks), swarm == tasks))

    ind = json.load(open(IND, encoding="utf-8"))
    missing = sorted({m for w in ind["waves"] for m in w["missing"]})
    hits = []
    for root, _dirs, files in os.walk(WAVES):
        for name in files:
            for n in missing:
                if n.lower() in name.lower():
                    hits.append(os.path.relpath(os.path.join(root, name), WAVES))
    print("variant-name hits (any extension, under waves) for %d missing names: %s" % (len(missing), hits))

    text = open(os.path.join(WAVES, "round-38/evidence/falsify-seat-accounting.txt"), encoding="utf-8").read()
    acct = set()
    for line in text.splitlines():
        if line.startswith("Codex capacity seats:") or line.startswith("Zai rate-limit seats:"):
            acct |= {x.strip() for x in line.split(":", 1)[1].split(",") if x.strip()}
    f38 = [w for w in ind["waves"] if w["dispatch_path"].endswith("round-38/falsify-dispatch.json")][0]
    print("lane accounting seat names=%d equal_to_tool_missing_set=%s" % (len(acct), acct == set(f38["missing"])))

    mism, stale, present = [], [], []
    for w in ind["waves"]:
        m_ = re.match(r"\.ufo/waves/(round-\d+)/(build|falsify)-dispatch\.json$", w["dispatch_path"])
        rnd, kind = m_.group(1), m_.group(2)
        disp_mtime = os.stat(os.path.join(LANE, w["dispatch_path"])).st_mtime
        for m in w["members_detail"]:
            if m["path"] != ".ufo/waves/%s/%s/%s.md" % (rnd, kind, m["name"]):
                mism.append((w["dispatch_path"], m["name"], m["path"]))
            if m["status"] == "present":
                present.append(m["path"])
                if m["mtime"] < disp_mtime:
                    stale.append((w["dispatch_path"], m["name"]))
    print("path-shape mismatches=%d present_older_than_dispatch=%d" % (len(mism), len(stale)))

    by_sha = defaultdict(list)
    for p in present:
        with open(os.path.join(LANE, p), "rb") as handle:
            by_sha[hashlib.sha256(handle.read()).hexdigest()].append(p)
    print("present files=%d duplicate_content_groups=%d" % (len(present), sum(1 for v in by_sha.values() if len(v) > 1)))

    for plan, disp in [("round-37/wave-plan-validation.json", "round-37/falsify-dispatch.json"),
                       ("round-38/build-plan.json", "round-38/build-dispatch.json"),
                       ("round-38/falsify-plan.json", "round-38/falsify-dispatch.json")]:
        names = {t["name"] for t in load(disp)["taskCall"]["tasks"]}
        plan_strings = all_strings(load(plan), set())
        plan_tasks = len(load(plan)["tasks"])
        print("plan %-34s plan_tasks=%d dispatch_names_absent_from_plan=%s" % (plan, plan_tasks, sorted(names - plan_strings)))


if __name__ == "__main__":
    main()
